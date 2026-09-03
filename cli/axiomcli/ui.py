"""Interactive UI — stdlib only (ANSI + input()), same look on Windows Terminal,
PowerShell 5+, macOS Terminal and Linux. Collects INTENT; composition stays
declarative (profiles + registry) — the UI never decides what goes where.
"""
import os
import sys

_ANSI = sys.stdout.isatty() and (os.name != "nt" or "WT_SESSION" in os.environ
                                 or os.environ.get("TERM_PROGRAM") or os.system("") == 0)

def c(text, code):
    return f"\033[{code}m{text}\033[0m" if _ANSI else text

BOLD, DIM, CYAN, GREEN, YELLOW = "1", "2", "36", "32", "33"


def banner():
    line = "═" * 46
    print(c(f"╔{line}╗", CYAN))
    print(c(f"║{'AXIOM SDD'.center(46)}║", CYAN))
    print(c(f"║{'setup do ambiente de spec-driven development'.center(46)}║", CYAN))
    print(c(f"╚{line}╝", CYAN))


def ask(question, default=""):
    suffix = f" [{default}]" if default else ""
    ans = input(f"{question}{suffix}: ").strip()
    return ans or default


def confirm(question, default=True):
    d = "S/n" if default else "s/N"
    ans = input(f"{question} [{d}]: ").strip().lower()
    if not ans:
        return default
    return ans in ("s", "sim", "y", "yes")


def menu(title, options, default=1):
    """options: list of (label, value). Returns chosen value."""
    print(f"\n{c(title, BOLD)}\n")
    for i, (label, _) in enumerate(options, 1):
        print(f"  [{i}] {label}")
    while True:
        raw = ask("\nEscolha", str(default))
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1][1]
        print(c("  opcao invalida", YELLOW))


def checkboxes(title, items, checked, allow_empty=False):
    """items: list of (id, label). Toggle by number; ENTER confirms. Returns ids."""
    state = {i: (i in checked) for i, _ in items}
    while True:
        print(f"\n{c(title, BOLD)}  {c('(numeros para alternar, ENTER confirma)', DIM)}\n")
        for n, (i, label) in enumerate(items, 1):
            mark = c("[x]", GREEN) if state[i] else "[ ]"
            print(f"  {mark} {n}. {label}")
        raw = input("\nAlternar (ex.: 1,3) ou ENTER: ").strip()
        if not raw:
            chosen = [i for i, _ in items if state[i]]
            if chosen or allow_empty:
                return chosen
            print(c("  selecione ao menos um item", YELLOW))
            continue
        for tok in raw.replace(",", " ").split():
            if tok.isdigit() and 1 <= int(tok) <= len(items):
                key = items[int(tok) - 1][0]
                state[key] = not state[key]


INTENTS = [
    ("Instalar SDD base (core, sem especializacao)",          ("base", None)),
    ("Desenvolvimento de feature",                            ("feature", None)),
    ("Refatoracao",                                           ("refactor", None)),
    ("Analise / feature em projeto legado",                   ("legacy", None)),
    ("Bugfix / Hotfix",                                       ("fix", None)),
    ("Infraestrutura (Terraform / IaC)",                      (None, "infrastructure-change")),
    ("Automacao de testes",                                   (None, "test-coverage")),
    ("Challenge / POC",                                       (None, "greenfield-feature")),
    ("Custom (escolher entre todos os profiles)",             ("custom", None)),
]


def resolve_intent(intent, detection, all_profiles):
    """Map an intent + detection to a concrete profile (asking when ambiguous)."""
    kind, direct = intent
    if direct:
        return direct
    fw = set(detection.get("frameworks", []))
    front = {"react", "angular", "vue", "next"} & fw
    back = {"spring", "spring-boot", "django", "flask", "fastapi", "express", "nest"} & fw
    if kind == "base":
        return "base"
    if kind == "feature":
        if detection.get("legacy"):
            return "legacy-feature"
        if front and back:
            return "fullstack-feature"
        if front:
            return "frontend-feature"
        return "backend-feature"
    if kind == "refactor":
        return "legacy-refactor" if detection.get("legacy") else "technical-debt"
    if kind == "legacy":
        return menu("Projeto legado — o que descreve melhor o trabalho?",
                    [("Nova feature em codigo legado", "legacy-feature"),
                     ("Refatorar preservando comportamento", "legacy-refactor"),
                     ("Pagar divida tecnica mapeada", "technical-debt")])
    if kind == "fix":
        return menu("Que tipo de correcao?",
                    [("Bug normal (com spec compacta)", "bugfix"),
                     ("Hotfix urgente em producao", "hotfix"),
                     ("Correcao de seguranca", "security-fix")])
    if kind == "custom":
        return menu("Profiles disponiveis:", [(p, p) for p in all_profiles],
                    default=1)
    return "backend-feature"
