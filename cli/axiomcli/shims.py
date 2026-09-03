"""Shim generator — renders the registry into each tool's native files.

Principles (inherited from template-sdd):
- AGENTS.md is the single canonical entry; every other file is a thin pointer.
- Never silently overwrite pre-existing user/team files: merges happen inside
  an explicit managed block; foreign files are reported, not clobbered.
- Adding a tool = adding a registry entry (+ template), not code.
"""
import json
from pathlib import Path

PKG = Path(__file__).resolve().parent
MD_BEGIN = "<!-- >>> sdd-managed (gerado pelo axiom-sdd; nao edite este bloco) >>> -->"
MD_END = "<!-- <<< sdd-managed <<< -->"
FILE_MARK = "<!-- sdd-managed: arquivo gerado pelo axiom-sdd -->"


def load_registry() -> dict:
    """Base registry + extensions dropped under adapters/<tool>/tool.json (axiom add-tool)."""
    reg = json.loads((PKG / "registry.json").read_text(encoding="utf-8"))
    root = PKG.parents[1]
    known = {t["id"] for t in reg["tools"]}
    for ext in sorted(root.glob("adapters/*/tool.json")):
        try:
            tool = json.loads(ext.read_text(encoding="utf-8"))
        except ValueError as e:
            print(f"AVISO: {ext} ignorado (JSON invalido: {e})")
            continue
        if tool.get("id") and tool["id"] not in known:
            reg["tools"].append(tool)
            known.add(tool["id"])
    return reg


def _tmpl(name: str) -> str:
    return (PKG / "templates" / name).read_text(encoding="utf-8")


def _fill(text: str, project: str, locks: list) -> str:
    return text.replace("{project}", project).replace("{locks}", "\n".join(f"- {l}" for l in locks))


def _strip_md_block(text: str) -> str:
    lines, out, skipping = text.splitlines(), [], False
    for ln in lines:
        if ln.strip().startswith("<!-- >>> sdd-managed"):
            skipping = True
            continue
        if ln.strip().startswith("<!-- <<< sdd-managed"):
            skipping = False
            continue
        if not skipping:
            out.append(ln)
    res = "\n".join(out).strip("\n")
    return res + "\n" if res else ""


def _merge_managed_block(path: Path, content: str) -> str:
    """Write `content` as/inside a managed block. Returns action taken."""
    block = f"{MD_BEGIN}\n{content.strip()}\n{MD_END}\n"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(block, encoding="utf-8")
        return "created"
    base = _strip_md_block(path.read_text(encoding="utf-8"))
    sep = "\n" if base and not base.endswith("\n") else ""
    path.write_text(base + sep + ("\n" if base else "") + block, encoding="utf-8")
    return "merged (managed block)" if base else "rewritten (managed block)"


# ---------------------------------------------------------------- command renderers

def _render_vscode_prompt(cmd: dict) -> str:
    body = "\n".join(cmd["body"])
    for i in cmd.get("inputs", []):
        body = body.replace("{%s}" % i["name"], "${input:%s:%s}" % (i["name"], i["hint"]))
    return (f"---\nmode: agent\ndescription: {cmd['description']}\n---\n{FILE_MARK}\n"
            f"# /sdd-{cmd['id']}\n{body}\n")


def _render_claude_command(cmd: dict) -> str:
    body = "\n".join(cmd["body"])
    hints = " ".join(f"<{i['name']}>" for i in cmd.get("inputs", []))
    for n, i in enumerate(cmd.get("inputs", []), start=1):
        body = body.replace("{%s}" % i["name"], f"${n}")
    return (f"---\ndescription: {cmd['description']}\nargument-hint: {hints}\n---\n{FILE_MARK}\n"
            f"{body}\nIf any argument is missing, ask for it before acting.\n")


def _render_codex_skill(cmd: dict) -> str:
    body = "\n".join(cmd["body"])
    for i in cmd.get("inputs", []):
        body = body.replace("{%s}" % i["name"], f"<{i['name']}>")
    inputs = " · ".join(f"{i['name']}: {i['hint']}" for i in cmd.get("inputs", []))
    return (f"---\nname: sdd-{cmd['id']}\ndescription: {cmd['description']}\n---\n{FILE_MARK}\n"
            f"# sdd-{cmd['id']}\nInputs: {inputs or 'none'} — ask for any missing input.\n\n{body}\n")


def _render_vscode_agent(agent: dict) -> str:
    """Custom agent (.github/agents/*.agent.md) — appears in VS Code's chat agents dropdown."""
    body = "\n".join(agent["body"])
    return (f"---\nname: sdd-{agent['id']}\ndescription: {agent['description']}\n---\n"
            f"{FILE_MARK}\n{body}\n")


def _render_claude_agent(agent: dict) -> str:
    """Claude Code subagent (.claude/agents/*.md) — listed by /agents and delegable."""
    body = "\n".join(agent["body"])
    return (f"---\nname: sdd-{agent['id']}\ndescription: {agent['description']}\n---\n"
            f"{FILE_MARK}\n{body}\n")


RENDERERS = {"vscode-prompt": _render_vscode_prompt,
             "claude-command": _render_claude_command,
             "codex-skill": _render_codex_skill,
             "vscode-agent": _render_vscode_agent,
             "claude-agent": _render_claude_agent}


# ---------------------------------------------------------------- generation

def _write_generated_file(path: Path, content: str) -> str:
    """Overwrite only files we own (marker present) or create new ones."""
    if path.exists() and "sdd-managed" not in path.read_text(encoding="utf-8"):
        return "SKIPPED (arquivo pre-existente sem marca do axiom-sdd — merge manual necessario)"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "written"


def generate(target: Path, runtimes: list, registry: dict) -> dict:
    """Generate all shims for the selected runtime ids. Returns an action log."""
    project = target.name
    locks = registry["locks"]
    shim_defs = registry["shims"]
    wanted = []          # shim ids, dedup, order preserved
    for tool in registry["tools"]:
        if tool["id"] in runtimes:
            for s in tool["shims"]:
                if s not in wanted:
                    wanted.append(s)

    log, generated = {}, set()
    for sid in wanted:
        d = shim_defs[sid]
        if "template" in d:
            content = _fill(_tmpl(d["template"]), project, locks)
            path = target / d["path"]
            if d.get("merge") == "managed-block":
                log[str(path)] = _merge_managed_block(path, content)
            else:  # overwrite-if-managed
                log[str(path)] = _write_generated_file(path, FILE_MARK + "\n" + content)
            generated.add(d["path"].lstrip("/"))
        elif "render" in d:
            render = RENDERERS[d["render"]]
            for cmd in registry.get(d.get("source", "commands"), []):
                rel = Path(d["dir"]) / d["filename"].format(id=cmd["id"])
                path = target / rel
                log[str(path)] = _write_generated_file(path, render(cmd))
                generated.add(d["dir"].strip("/").split("/")[0])
    return {"log": log, "generated": generated, "shims": wanted}


def write_globals(runtimes: list, registry: dict, os_key: str) -> dict:
    """Opt-in only (--write-global): minimal 3-line pointers in machine-global files."""
    from .doctor import expand
    log = {}
    for tool in registry["tools"]:
        if tool["id"] not in runtimes:
            continue
        for g in tool.get("global_shims", []):
            path = expand(g[os_key])
            content = _tmpl(g["template"])
            log[str(path)] = _merge_managed_block(path, content)
    return log


def remove(target: Path, registry: dict) -> dict:
    """Undo: strip managed blocks (delete file if nothing else remains) and
    delete generated command files (marker required)."""
    log = {}
    for sid, d in registry["shims"].items():
        if "path" in d:
            path = target / d["path"]
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            rest = _strip_md_block(text).replace(FILE_MARK, "").strip()
            if "sdd-managed" in text or not rest:
                path.unlink()          # arquivo inteiramente nosso
                log[str(path)] = "deleted"
            else:
                path.write_text(_strip_md_block(text), encoding="utf-8")
                log[str(path)] = "managed block removed (file kept)"
        elif "dir" in d:
            base = target / d["dir"]
            if not base.exists():
                continue
            for f in sorted(p for p in base.rglob("*") if p.is_file()):
                if "sdd-" in str(f.relative_to(base)) and "sdd-managed" in f.read_text(encoding="utf-8"):
                    f.unlink()
                    log[str(f)] = "deleted"
            for sub in sorted(base.rglob("*"), reverse=True):
                if sub.is_dir() and not any(sub.iterdir()):
                    sub.rmdir()
            for d in (base, base.parent):
                if d != target and d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
                    log[str(d)] = "deleted (empty dir)"
    envfile = target / "sdd" / "environment.json"
    if envfile.exists():
        envfile.unlink()
        log[str(envfile)] = "deleted"
    return log
