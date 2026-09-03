# Changelog — axiom-sdd

## 2.0.0 — 2026-09
- **Projeto nasce da unificacao de `template-sdd` (metodologia) + `sdd-setup` (ambiente).**
- Estrutura achatada: `core/ profiles/ workflows/ agents/ adapters/ templates/` na raiz;
  o layout do CONSUMIDOR permanece `sdd/**` (compatibilidade total com instalacoes existentes).
- CLI unico `cli/axiom.py` (install interativo/CI, doctor, update, remove, add-tool,
  add-profile, add-template) + wrappers `install.sh` / `install.ps1`.
- Deteccao dinamica do projeto alvo (Java/Spring, Python, Node, Go, COBOL, Terraform,
  automacao de testes, heuristica de legado) com rotulos CONFIRMED/INFERRED.
- `sdd/manifest.json` no consumidor: lockfile de instalacao (profile, runtimes, versao).
- `registry.json` promovido a fonte unica dos adapters; extensivel por `adapters/*/tool.json`.
- Todos os 11 agentes canonicos agora sao rendidos em `.github/agents/` e `.claude/agents/`,
  cada um apontando para seu canonico em `sdd/agents/*.agent.md`.
- Correcao de inconsistencia herdada: toda referencia a `sdd/AGENTS.md` (inexistente) foi
  corrigida — canonico e `AGENTS.md` na RAIZ; roster e `sdd/agents/README.md`.
- Novo profile `infrastructure-change` (Terraform/IaC) e `gitflow/` com deteccao de agente.
- Marcadores gerenciados retrocompativeis: blocos gerados pelo antigo sdd-setup sao
  reconhecidos e migrados no proximo install/update.
