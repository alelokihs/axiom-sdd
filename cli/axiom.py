#!/usr/bin/env python3
"""AXIOM SDD — spec-driven development, um comando, qualquer SO.

    python3 cli/axiom.py                      # interativo (detecta, pergunta, compoe)
    python3 cli/axiom.py install --target ../proj --profile backend-feature --runtimes claude-code --yes
    python3 cli/axiom.py doctor  --target ../proj
    python3 cli/axiom.py update  --target ../proj
    python3 cli/axiom.py remove  --target ../proj
    python3 cli/axiom.py add-tool | add-profile <nome> | add-template <NOME>

Python 3.8+, somente stdlib. O CLI coleta INTENCAO; a composicao e declarativa:
profiles (o que), workflows (como), registry + adapters (para quem).
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from axiomcli import compose, detect, doctor, gitexclude, scaffold, shims, ui  # noqa: E402

TEAM_MODE_PATTERNS = ["/CLAUDE.local.md", "/sdd/_tmp/", "/sdd/environment.json",
                      "/sdd/devin-playbook.md"]
MANIFEST = "sdd/manifest.json"


def _load_manifest(target: Path) -> dict:
    p = target / MANIFEST
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            pass
    return {}


def _save_manifest(target: Path, data: dict) -> None:
    p = target / MANIFEST
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _hello(registry: dict, runtimes: list) -> list:
    return [f"  {t['name']}:\n     {t.get('hello', 'SDD: init')}"
            for t in registry["tools"] if t["id"] in runtimes]


def cmd_install(a, registry) -> int:
    target = Path(a.target).resolve()
    if not target.exists():
        print(f"erro: alvo {target} nao existe", file=sys.stderr)
        return 2
    interactive = (not a.yes) and sys.stdin.isatty()

    env = doctor.run(registry, target)
    detection = detect.run(target)
    if interactive:
        ui.banner()
    print(doctor.report(env))
    print("\nProjeto detectado:")
    for ln in detect.summary_lines(detection):
        print(ln)
    if interactive and not ui.confirm("\nDeteccao razoavel? (nao decide nada sozinha — voce ajusta tudo a seguir)"):
        print("Ok — ignore as sugestoes e escolha manualmente nos proximos passos.")

    # ---- profile ----------------------------------------------------------
    all_profiles = compose.list_profiles()
    profile = a.profile
    if not profile:
        if interactive:
            intent = ui.menu("O que deseja fazer?", ui.INTENTS)
            profile = ui.resolve_intent(intent, detection, all_profiles)
        else:
            profile = detection["suggested_profiles"][0]
    if profile != "base" and profile not in all_profiles:
        print(f"erro: profile '{profile}' inexistente. Validos: base, {', '.join(all_profiles)}",
              file=sys.stderr)
        return 2

    # ---- runtimes ---------------------------------------------------------
    detected = [t["id"] for t in env["tools"] if t["detected"]]
    if a.runtimes:
        runtimes = [r.strip() for r in a.runtimes.split(",") if r.strip()]
    elif interactive:
        runtimes = ui.checkboxes("Runtimes (IAs agenticas) para configurar:",
                                 [(t["id"], f"{t['name']}"
                                   + ("  <- detectado" if t["id"] in detected else ""))
                                  for t in registry["tools"]], set(detected))
    else:
        runtimes = detected
    valid = {t["id"] for t in registry["tools"]}
    unknown = [r for r in runtimes if r not in valid]
    if unknown:
        print(f"erro: runtimes desconhecidos {unknown}. Validos: {sorted(valid)}", file=sys.stderr)
        return 2

    git_mode = a.git_mode or (ui.ask("Modo git (stealth/team/none)", "stealth")
                              if interactive else "stealth")

    # ---- compose core -----------------------------------------------------
    print(f"\n>> Compondo o core (profile: {profile})...")
    result = compose.install(target, profile, update=False)
    print(f"   {len(result['copied'])} arquivo(s) em {target / 'sdd'}")

    # ---- shims ------------------------------------------------------------
    print(">> Gerando shims...")
    sh = shims.generate(target, runtimes, registry)
    for path, action in sh["log"].items():
        print(f"   {action}: {path}")
    if a.write_global:
        print(">> Ponteiros globais (--write-global)...")
        for path, action in shims.write_globals(runtimes, registry, env["os_key"]).items():
            print(f"   {action}: {path}")

    # ---- git exclude ------------------------------------------------------
    excl = {"skipped": "git-mode=none"}
    if git_mode == "stealth":
        excl = gitexclude.apply(target, registry["git_exclude"],
                                registry["git_exclude_if_generated"], sh["generated"])
    elif git_mode == "team":
        excl = gitexclude.apply(target, TEAM_MODE_PATTERNS, [], set())
    print(f">> git exclude ({git_mode}): {excl.get('file', excl.get('skipped'))}")
    for cft in excl.get("tracked_conflicts", []):
        print(f"   AVISO: '{cft}' ja RASTREADO pelo git — exclude sem efeito; "
              f"use git rm --cached ou --git-mode team.")

    # ---- manifest + environment ------------------------------------------
    doctor.save(env, target)
    _save_manifest(target, {
        "axiom_version": registry.get("version", "?"), "profile": profile,
        "workflow": result["profile"]["workflow"] if result["profile"] else None,
        "runtimes": runtimes, "git_mode": git_mode,
        "installed_at": _load_manifest(target).get("installed_at") or datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "shims": sh["shims"], "detection": {k: detection[k] for k in
                                            ("stacks", "frameworks", "infra", "testing", "legacy")},
    })

    # ---- report + hello world --------------------------------------------
    print(f"""
AXIOM SDD — SETUP COMPLETO
{'=' * 60}
Projeto:   {target}
Profile:   {profile}   ·   Runtimes: {', '.join(runtimes)}   ·   Git: {git_mode}
Manifest:  {target / MANIFEST}
{'=' * 60}
PRIMEIRO COMANDO (Hello World) — abra a IA que voce usa e rode:
""")
    for line in _hello(registry, runtimes):
        print(line)
    print("\n  Devin sem acesso local? cole sdd/devin-playbook.md como Playbook no app.")
    return 0


def cmd_doctor(a, registry) -> int:
    target = Path(a.target).resolve()
    env = doctor.run(registry, target)
    print(doctor.report(env))
    print("\nProjeto detectado:")
    for ln in detect.summary_lines(detect.run(target)):
        print(ln)
    return 0


def cmd_update(a, registry) -> int:
    target = Path(a.target).resolve()
    m = _load_manifest(target)
    if not m:
        print("erro: sem sdd/manifest.json — rode 'install' primeiro.", file=sys.stderr)
        return 2
    profile, runtimes = m["profile"], m["runtimes"]
    print(f">> Update (profile {profile}, runtimes {', '.join(runtimes)})...")
    result = compose.install(target, profile, update=True)
    print(f"   {len(result['copied'])} arquivo(s) framework-owned re-copiados")
    sh = shims.generate(target, runtimes, registry)
    print(f"   shims regenerados: {', '.join(sh['shims'])}")
    if m.get("git_mode") == "stealth":
        gitexclude.apply(target, registry["git_exclude"],
                         registry["git_exclude_if_generated"], sh["generated"])
    m.update(axiom_version=registry.get("version", "?"),
             updated_at=datetime.now().isoformat(timespec="seconds"))
    _save_manifest(target, m)
    print("   project-owned intocados:", ", ".join(compose.PROJECT_OWNED))
    return 0


def cmd_remove(a, registry) -> int:
    target = Path(a.target).resolve()
    print(">> Removendo artefatos gerados pelo axiom-sdd...")
    for path, action in shims.remove(target, registry).items():
        print(f"   {action}: {path}")
    print(f"   git exclude: {gitexclude.remove(target)}")
    mp = target / MANIFEST
    if mp.exists():
        mp.unlink()
        print(f"   deleted: {mp}")
    print("   NOTA: sdd/ (core, specs, decisions) e project-owned e fica no lugar; "
          "apague manualmente se quiser remover a metodologia inteira.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="axiom", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    def common(p):
        p.add_argument("--target", default=".", help="raiz do projeto consumidor")
    pi = sub.add_parser("install", help="instala o SDD (interativo sem flags)")
    common(pi)
    pi.add_argument("--profile", help="profile (ex.: backend-feature; 'base' = so o core)")
    pi.add_argument("--runtimes", default="", help="ids: copilot-vscode,claude-code,codex,devin,...")
    pi.add_argument("--git-mode", choices=["stealth", "team", "none"], default=None)
    pi.add_argument("--write-global", action="store_true")
    pi.add_argument("--yes", action="store_true", help="sem perguntas (CI): deteccao + defaults")
    for name in ("doctor", "update", "remove"):
        common(sub.add_parser(name))
    sub.add_parser("add-tool", help="registra uma nova IA agentica (wizard)")
    sub.add_parser("add-profile", help="scaffolda um novo profile").add_argument("name")
    sub.add_parser("add-template", help="scaffolda um novo template").add_argument("name")
    sub.add_parser("list-profiles", help="lista os profiles disponiveis")

    KNOWN = {"install", "doctor", "update", "remove", "add-tool", "add-profile",
             "add-template", "list-profiles"}
    argv = sys.argv[1:]
    if not argv:                       # ./install.sh sem argumentos = install interativo
        argv = ["install"]
    elif argv[0] not in KNOWN and argv[0] not in ("-h", "--help"):
        argv = ["install"] + argv      # ./install.sh --target X = install --target X
    a = ap.parse_args(argv)
    registry = shims.load_registry()

    if a.cmd == "install":
        return cmd_install(a, registry)
    if a.cmd == "doctor":
        return cmd_doctor(a, registry)
    if a.cmd == "update":
        return cmd_update(a, registry)
    if a.cmd == "remove":
        return cmd_remove(a, registry)
    if a.cmd == "add-tool":
        return scaffold.add_tool(registry)
    if a.cmd == "add-profile":
        return scaffold.add_profile(a.name)
    if a.cmd == "add-template":
        return scaffold.add_template(a.name)
    if a.cmd == "list-profiles":
        print("base (so o core)")
        for p in compose.list_profiles():
            print(p)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\ninterrompido")
        sys.exit(130)
    except BrokenPipeError:
        sys.exit(0)
