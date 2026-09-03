"""Target-project detection — dynamic, file-signal based, always confirmable.

Detects languages (Java, Python, Node, Go, Ruby, PHP, .NET, COBOL...), frameworks
(Spring, Django, React...), infrastructure (Terraform, Docker, K8s, CI) and test
automation stacks. Labels follow the framework convention:
CONFIRMED (file observed) / INFERRED (heuristic, evidence cited).
Detection SUGGESTS — the interactive UI always lets the user confirm/correct.
"""
import os
import subprocess
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "target", "build", "dist", "out", ".venv", "venv",
             "__pycache__", ".idea", ".vscode", "vendor", ".terraform", "bin", "obj"}
MAX_DEPTH = 4

LANG_FILES = {  # filename (exact) -> (stack, extra-probe)
    "pom.xml": ("java", "spring"), "build.gradle": ("java", "spring"),
    "build.gradle.kts": ("java", "spring"), "package.json": ("node", "jsfw"),
    "pyproject.toml": ("python", "pyfw"), "requirements.txt": ("python", "pyfw"),
    "setup.py": ("python", None), "go.mod": ("go", None), "Gemfile": ("ruby", "rails"),
    "composer.json": ("php", "laravel"), "Cargo.toml": ("rust", None),
}
LANG_EXTS = {".cbl": "cobol", ".cob": "cobol", ".cpy": "cobol", ".csproj": "dotnet",
             ".sln": "dotnet", ".tf": "terraform", ".robot": "robot-framework"}
TEST_FILES = ("cypress.config.js", "cypress.config.ts", "playwright.config.js",
              "playwright.config.ts", "karate-config.js", "conftest.py")
FRAMEWORK_PROBES = {
    "spring": ("springframework", "spring-boot"), "jsfw": ("react", "angular", "vue", "next", "express", "nest"),
    "pyfw": ("django", "flask", "fastapi", "pytest", "robotframework", "selenium"),
    "rails": ("rails",), "laravel": ("laravel",),
}


def _walk(target: Path):
    for root, dirs, files in os.walk(target):
        rel_depth = len(Path(root).relative_to(target).parts)
        if rel_depth >= MAX_DEPTH:
            dirs[:] = []
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        yield Path(root), files


def _probe_text(path: Path, needles: tuple) -> list:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:200_000].lower()
    except OSError:
        return []
    return [n for n in needles if n in text]


def _repo_age_years(target: Path):
    try:
        out = subprocess.run(["git", "-C", str(target), "log", "--reverse",
                              "--format=%cs", "--max-count=1"],
                             capture_output=True, text=True, timeout=20)
        first = out.stdout.strip().splitlines()
        if first:
            from datetime import date
            y0 = int(first[0][:4])
            return date.today().year - y0
    except Exception:
        pass
    return None


def run(target: Path) -> dict:
    stacks, frameworks, infra, testing, evidence = set(), set(), set(), set(), {}

    def note(key, ev):
        evidence.setdefault(key, [])
        if len(evidence[key]) < 3 and ev not in evidence[key]:
            evidence[key].append(ev)

    for root, files in _walk(target):
        for f in files:
            rel = str((root / f).relative_to(target))
            if f in LANG_FILES:
                stack, probe = LANG_FILES[f]
                stacks.add(stack); note(stack, rel)
                if probe:
                    for hit in _probe_text(root / f, FRAMEWORK_PROBES[probe]):
                        frameworks.add(hit); note(hit, rel)
            ext = Path(f).suffix.lower()
            if ext in LANG_EXTS:
                kind = LANG_EXTS[ext]
                (infra if kind == "terraform" else
                 testing if kind == "robot-framework" else stacks).add(kind)
                note(kind, rel)
            if f in TEST_FILES:
                testing.add(f.split(".")[0].split("-")[0]); note("testing", rel)
            if f == "Dockerfile" or f.startswith("docker-compose"):
                infra.add("docker"); note("docker", rel)
        if root.name == "workflows" and root.parent.name == ".github":
            infra.add("github-actions"); note("github-actions", ".github/workflows/")
        if root.name in ("k8s", "kubernetes", "helm", "charts"):
            infra.add("kubernetes"); note("kubernetes", str(root.relative_to(target)))

    for t in ("selenium", "pytest", "robotframework"):
        if t in frameworks:
            frameworks.discard(t); testing.add(t)

    age = _repo_age_years(target)
    legacy, legacy_why = False, []
    if "cobol" in stacks:
        legacy, legacy_why = True, ["COBOL sources present"]
    if age is not None and age >= 4:
        legacy = True; legacy_why.append(f"first commit ~{age} years ago")

    test_automation_project = bool(testing) and not (stacks - {"node", "python", "java"} or frameworks - {"pytest"}) and len(testing) >= 1 and not frameworks.intersection({"react","angular","vue","next","django","flask","fastapi","spring","spring-boot"})

    suggestions = []
    if "terraform" in infra:
        suggestions.append("infrastructure-change")
    if test_automation_project:
        suggestions.append("test-coverage")
    if legacy:
        suggestions += ["legacy-feature", "legacy-refactor"]
    if not suggestions:
        if {"react", "angular", "vue", "next"} & frameworks and ({"spring", "spring-boot", "django", "flask", "fastapi", "express", "nest"} & frameworks):
            suggestions.append("fullstack-feature")
        elif {"react", "angular", "vue", "next"} & frameworks:
            suggestions.append("frontend-feature")
        else:
            suggestions.append("backend-feature")

    return {"stacks": sorted(stacks), "frameworks": sorted(frameworks),
            "infra": sorted(infra), "testing": sorted(testing),
            "legacy": legacy, "legacy_evidence": legacy_why, "repo_age_years": age,
            "test_automation_project": test_automation_project,
            "evidence": evidence, "suggested_profiles": suggestions}


def summary_lines(d: dict) -> list:
    def lbl(items, conf="CONFIRMED"):
        return f"{', '.join(items)}  ({conf})" if items else None
    lines = []
    if d["stacks"]:     lines.append(f"  Linguagens:   {lbl(d['stacks'])}")
    if d["frameworks"]: lines.append(f"  Frameworks:   {lbl(d['frameworks'])}")
    if d["infra"]:      lines.append(f"  Infra:        {lbl(d['infra'])}")
    if d["testing"]:    lines.append(f"  Testes:       {lbl(d['testing'])}")
    if d["legacy"]:     lines.append(f"  Legado:       sim  (INFERRED: {'; '.join(d['legacy_evidence'])})")
    if d["test_automation_project"]:
        lines.append("  Tipo:         projeto de AUTOMACAO DE TESTES (INFERRED)")
    if not lines:
        lines.append("  (nada detectado — projeto vazio ou stack nao mapeada)")
    return lines
