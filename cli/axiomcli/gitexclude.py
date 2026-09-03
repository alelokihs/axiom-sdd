"""Managed block in .git/info/exclude — the stealth git layer.

Same effect as .gitignore, but local to the clone and never committed.
Idempotent: re-running replaces the block; --remove deletes it. Files already
TRACKED by git are not affected by exclude — those are detected and reported.
"""
import subprocess
from pathlib import Path

BEGIN = "# >>> sdd-managed (gerado pelo axiom-sdd; nao edite este bloco) >>>"
END = "# <<< sdd-managed <<<"


def _exclude_file(target: Path) -> Path:
    return target / ".git" / "info" / "exclude"


def _strip_block(text: str) -> str:
    lines, out, skipping = text.splitlines(), [], False
    for ln in lines:
        if ln.strip().startswith("# >>> sdd-managed"):
            skipping = True
            continue
        if ln.strip().startswith("# <<< sdd-managed"):
            skipping = False
            continue
        if not skipping:
            out.append(ln)
    result = "\n".join(out).rstrip("\n")
    return result + "\n" if result else ""


def tracked_conflicts(target: Path, patterns: list) -> list:
    """Patterns whose file is already tracked — exclude has no effect on them."""
    try:
        out = subprocess.run(["git", "-C", str(target), "ls-files"],
                             capture_output=True, text=True, timeout=30)
        tracked = set(out.stdout.splitlines())
    except Exception:
        return []
    conflicts = []
    for pat in patterns:
        name = pat.strip("/").rstrip("/")
        if name in tracked or any(t.startswith(name + "/") for t in tracked):
            conflicts.append(pat)
    return conflicts


def apply(target: Path, patterns: list, generated_optional: list, generated: set) -> dict:
    """Write/replace the managed block. `generated_optional` entries are included only
    when axiom-sdd itself generated that file (never hide a pre-existing team file)."""
    xf = _exclude_file(target)
    if not xf.parent.is_dir():
        return {"skipped": "target is not a git repository (no .git/info/)"}

    effective = list(patterns)
    for pat in generated_optional:
        if pat.strip("/") in generated:
            effective.append(pat)

    conflicts = tracked_conflicts(target, effective)
    block = "\n".join([BEGIN] + effective + [END])
    base = _strip_block(xf.read_text(encoding="utf-8")) if xf.exists() else ""
    xf.write_text(base + ("\n" if base and not base.endswith("\n") else "") + block + "\n",
                  encoding="utf-8")
    return {"file": str(xf), "patterns": effective, "tracked_conflicts": conflicts}


def remove(target: Path) -> dict:
    xf = _exclude_file(target)
    if not xf.exists():
        return {"skipped": "no exclude file"}
    xf.write_text(_strip_block(xf.read_text(encoding="utf-8")), encoding="utf-8")
    return {"file": str(xf), "removed": True}
