"""Core composer — installs/updates the framework core into a consumer project.

Descends from template-sdd's bootstrap/install.py, adapted to axiom-sdd's flat
repo layout (core/, profiles/, ... at the repo root) while the CONSUMER layout
stays `sdd/` (specs, agents and docs keep referencing sdd/**).
Deterministic before generative: copying files is not a job for an LLM.
"""
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # cli/axiomcli/ -> cli/ -> repo root

# framework dir -> consumer subdir (under <target>/sdd/)
CORE_MAP = {"core": "core", "templates": "templates"}
FRAMEWORK_OWNED = ["sdd/core", "sdd/templates", "sdd/agents", "sdd/workflow.yaml"]
PROJECT_OWNED = ["sdd/sdd.yaml", "sdd/guardrails.md", "sdd/constitution.md",
                 "sdd/profile.yaml", "sdd/gitflow.md", "sdd/specs", "sdd/decisions"]


def parse_simple_yaml(path: Path) -> dict:
    """Minimal parser for the flat profile schema (scalars + inline/dash lists)."""
    data, current_list_key = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list_key:
            data[current_list_key].append(line.strip()[2:].strip())
            continue
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            if val.startswith("[") and val.endswith("]"):
                data[key] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
                current_list_key = None
            elif val == "":
                data[key] = []
                current_list_key = key
            else:
                data[key] = val
                current_list_key = None
    return data


def list_profiles() -> list:
    return sorted(p.stem for p in (ROOT / "profiles").glob("*.yaml")
                  if not p.stem.startswith("_"))


def read_profile(name: str) -> dict:
    base = parse_simple_yaml(ROOT / "profiles/_defaults.yaml")
    if name == "base":
        return {"agents": list(base.get("agents", [])),
                "workflow": base.get("workflow", "standard"), "name": "base",
                "summary": "Core only, default workflow, no specialization."}
    prof = parse_simple_yaml(ROOT / "profiles" / f"{name}.yaml")
    agents = list(base.get("agents", []))
    for extra in prof.get("agents+", []):
        if extra not in agents:
            agents.append(extra)
    if "agents" in prof:  # full replacement
        agents = prof["agents"]
    workflow = prof.get("workflow", base.get("workflow", "standard"))
    return {"agents": agents, "workflow": workflow, "name": name,
            "summary": prof.get("summary", "")}


def copy_tree(src: Path, dst: Path, overwrite: bool) -> list:
    copied = []
    for f in sorted(src.rglob("*")):
        if f.is_dir():
            continue
        rel = f.relative_to(src)
        out = dst / rel
        if out.exists() and not overwrite:
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)
        copied.append(str(out.relative_to(dst.parent.parent)))
    return copied


def install(target: Path, profile_name: str, update: bool = False) -> dict:
    """Install (or safely update) the core into <target>/sdd/. Returns summary."""
    sdd = target / "sdd"
    copied = []
    prof = read_profile(profile_name) if profile_name else None

    for src_dir, dst_dir in CORE_MAP.items():
        copied += copy_tree(ROOT / src_dir, sdd / dst_dir, overwrite=update)

    agents_dst = sdd / "agents"
    agents_dst.mkdir(parents=True, exist_ok=True)
    roster = (prof["agents"] + ["bootstrap"]) if prof else []
    for name in roster:
        src = ROOT / "agents" / f"{name}.agent.md"
        if src.exists():
            shutil.copy2(src, agents_dst / src.name)
            copied.append(f"sdd/agents/{src.name}")
    for extra in ("capability-matrix.yaml", "README.md"):
        src = ROOT / "agents" / extra
        shutil.copy2(src, agents_dst / extra)
        copied.append(f"sdd/agents/{extra}")

    if prof:
        shutil.copy2(ROOT / "workflows" / f"{prof['workflow']}.yaml", sdd / "workflow.yaml")
        copied.append("sdd/workflow.yaml")
        # The resolved profile is a project-owned seed, including on reinstall.
        if prof["name"] != "base" and not (sdd / "profile.yaml").exists():
            shutil.copy2(ROOT / "profiles" / f"{profile_name}.yaml", sdd / "profile.yaml")
            copied.append("sdd/profile.yaml")
        shutil.copy2(ROOT / "profiles/_defaults.yaml", sdd / "profile-defaults.yaml")
        copied.append("sdd/profile-defaults.yaml")

    for d in ("specs", "decisions"):
        (sdd / d).mkdir(parents=True, exist_ok=True)
        if not any((sdd / d).iterdir()):
            (sdd / d / ".gitkeep").touch()

    # project-owned seeds: created once, never overwritten
    if not (sdd / "guardrails.md").exists():
        shutil.copy2(ROOT / "templates/GUARDRAILS.md", sdd / "guardrails.md")
        copied.append("sdd/guardrails.md  (seed — bootstrap fills it)")
    if not (sdd / "gitflow.md").exists():
        shutil.copy2(ROOT / "gitflow/GITFLOW.md", sdd / "gitflow.md")
        copied.append("sdd/gitflow.md  (seed — customize freely, project-owned)")
    if not (sdd / "sdd.yaml").exists():
        text = (ROOT / "templates/project-sdd.yaml").read_text(encoding="utf-8")
        text = text.replace("<YYYY-MM-DD>", date.today().isoformat())
        (sdd / "sdd.yaml").write_text(text, encoding="utf-8")
        copied.append("sdd/sdd.yaml  (skeleton — bootstrap fills it)")

    return {"copied": copied, "profile": prof, "updated": update}
