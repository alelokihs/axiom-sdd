"""sdd doctor — scan the developer machine for AI tools/IDEs and report what
each one supports, with the framework's confidence labels:
CONFIRMED (observed) / INFERRED (probable, evidence cited) / UNKNOWN.

Read-only by design. Output feeds shims.py (which shims to generate).
"""
import json
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path

OS_KEY = {"Windows": "windows", "Darwin": "darwin", "Linux": "linux"}.get(platform.system(), "linux")


def expand(p: str) -> Path:
    """Expand ~ and %WINDOWS% style env vars on any OS."""
    p = os.path.expandvars(re.sub(r"%([^%]+)%", r"${\1}", p))
    return Path(os.path.expanduser(p))


def _version_from_glob(spec: dict) -> tuple:
    """Best-effort version from a directory glob (e.g. VS Code extension folders)."""
    if not spec:
        return None, None
    base = expand(spec["dir"])
    if not base.exists():
        return None, None
    hits = sorted(base.glob(spec["pattern"]))
    if not hits:
        return None, None
    last = hits[-1]
    m = re.search(r"-(\d+\.\d+[\w.\-]*)$", last.name)
    return (m.group(1) if m else None), str(last)


def _cli_version(cmd: str) -> str:
    exe = shutil.which(cmd)
    if not exe:
        return None
    try:
        out = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=15)
        return (out.stdout or out.stderr).strip().splitlines()[0][:80] or "present"
    except Exception:
        return "present (version check failed)"


def scan_tool(tool: dict) -> dict:
    """Scan one registry tool entry. Returns a finding dict with a confidence label."""
    finding = {"id": tool["id"], "name": tool["name"], "kind": tool.get("kind", ""),
               "detected": False, "confidence": "UNKNOWN", "evidence": [],
               "version": None, "reads": tool.get("reads", []), "notes": tool.get("notes", "")}

    if tool.get("kind") == "cloud":
        finding.update(detected=bool(tool.get("always_offer")), confidence="INFERRED",
                       evidence=["cloud runtime — no local footprint; offered by default"])
        return finding

    for raw in tool.get("detect", {}).get(OS_KEY, []):
        p = expand(raw)
        if p.exists():
            finding["detected"] = True
            finding["evidence"].append(str(p))

    if tool.get("which"):
        v = _cli_version(tool["which"])
        if v:
            finding["detected"] = True
            finding["version"] = v
            finding["evidence"].append(f"$PATH: {tool['which']} -> {v}")

    ver, where = _version_from_glob(tool.get("version_glob"))
    if where:
        finding["evidence"].append(where)
        if ver and not finding["version"]:
            finding["version"] = ver

    if finding["detected"]:
        finding["confidence"] = "CONFIRMED" if finding["evidence"] else "INFERRED"
    return finding


def scan_jetbrains_ides() -> list:
    """List installed JetBrains IDEs (config dirs) — evidence for the copilot-jetbrains entry."""
    roots = {"windows": ["%APPDATA%/JetBrains"],
             "darwin": ["~/Library/Application Support/JetBrains"],
             "linux": ["~/.config/JetBrains"]}[OS_KEY]
    ides = []
    for raw in roots:
        base = expand(raw)
        if base.exists():
            ides += sorted(d.name for d in base.iterdir()
                           if d.is_dir() and re.match(r"^[A-Za-z]+\d{4}\.\d", d.name))
    return ides


def scan_target(target: Path) -> dict:
    """Facts about the target project relevant to setup."""
    git_dir = target / ".git"
    return {
        "path": str(target),
        "is_git_repo": git_dir.is_dir(),
        "has_sdd": (target / "sdd" / "sdd.yaml").exists(),
        "existing_ai_files": [f for f in
                              ("AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md",
                               ".cursorrules", ".windsurfrules")
                              if (target / f).exists()],
    }


def run(registry: dict, target: Path) -> dict:
    findings = [scan_tool(t) for t in registry["tools"]]
    env = {
        "sdd_setup_version": registry.get("version", "?"),
        "os": platform.system(),
        "os_key": OS_KEY,
        "python": platform.python_version(),
        "git": _cli_version("git") or "NOT FOUND",
        "jetbrains_ides": scan_jetbrains_ides(),
        "tools": findings,
        "target": scan_target(target),
    }
    return env


def report(env: dict) -> str:
    lines = ["SDD DOCTOR", "=" * 60,
             f"SO:              {env['os']} (python {env['python']})",
             f"git:             {env['git']}"]
    if env["jetbrains_ides"]:
        lines.append(f"JetBrains IDEs:  {', '.join(env['jetbrains_ides'])}")
    lines.append("-" * 60)
    for t in env["tools"]:
        mark = "OK " if t["detected"] else "-- "
        ver = f"  [{t['version']}]" if t.get("version") else ""
        lines.append(f"{mark}{t['name']}  ({t['confidence']}){ver}")
        for ev in t["evidence"][:3]:
            lines.append(f"     evidencia: {ev}")
        if t["notes"]:
            lines.append(f"     nota: {t['notes']}")
    tg = env["target"]
    lines += ["-" * 60,
              f"Projeto alvo:    {tg['path']}",
              f"  repo git:      {'sim' if tg['is_git_repo'] else 'NAO (git exclude sera pulado)'}",
              f"  sdd/ presente: {'sim' if tg['has_sdd'] else 'nao (rode SDD: init depois)'}"]
    if tg["existing_ai_files"]:
        lines.append(f"  config IA pre-existente: {', '.join(tg['existing_ai_files'])} "
                     f"(sera feito merge por bloco gerenciado — nunca sobrescrita silenciosa)")
    return "\n".join(lines)


def save(env: dict, target: Path) -> Path:
    out = target / "sdd" / "environment.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(env, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out
