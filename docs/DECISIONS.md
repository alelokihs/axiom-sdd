# Decisoes de arquitetura — unificacao (2026-09)

Registro das decisoes que criaram o axiom-sdd. Contexto completo: docs/history/PROPOSTA-ETAPA-3.md.

| # | Questao | Decisao | Racional |
|---|---|---|---|
| 1 | Nome | **Axiom SDD** (`axiom-sdd`) | escolha do time |
| 2 | Historico git | **repo limpo** | template-sdd e sdd-setup ficam como arquivo congelado |
| 3 | Inventario sdd-setup | quase tudo unico → migrado para `cli/axiomcli` | doctor, shims, gitexclude, registry eram a Etapa 2 implementada |
| 4 | Lockfile | **`sdd/manifest.json`** no consumidor | leve; da base para update/remove limpos; blocos gerenciados cobrem os shims |
| 5 | TUI | **Python stdlib pura** | promessa de zero dependencias mantida pelos dois repos de origem |
| 6 | Estrutura | raiz achatada no framework; consumidor mantem `sdd/**` | repo mais legivel sem quebrar instalacoes existentes |
| 7 | Deteccao do alvo | **dinamica em `detect.py`** (linguagens, frameworks, infra, testes, legado), sempre confirmavel | "detecta, sugere, nunca decide" |
| 8 | Fonte dos adapters | **`registry.json` unico e executavel**, extensivel por `adapters/*/tool.json`; ADAPTER.md vira doc conceitual | elimina duplicacao (locks, capacidades) entre docs e codigo |

## Refinamentos incorporados (backlog do time, 2026-09-03)

| Pedido | Onde foi parar |
|---|---|
| Comportamento com Terraform | deteccao `*.tf` + profile `infrastructure-change` (plan-before-apply) + FAQ no README |
| Instalar novas ferramentas de IA com documentacao em pasta propria | `axiom add-tool` → `adapters/<id>/tool.json` + `adapters/<id>/docs/` para a doc oficial |
| Projeto de automacao de testes | deteccao (cypress/playwright/robot/selenium/karate) → profile `test-coverage`; FAQ no README |
| Pasta de gitflow proprio + agente detecta qual IA esta usando e commita de acordo | `gitflow/GITFLOW.md` → instalado como `sdd/gitflow.md` (project-owned); trailer por runtime; secao "Git & commits" no AGENTS.md gerado |
| Instrucoes para criar nova feature | README "Fluxo de uma feature" + comandos `/sdd-*` |
| Hello World ao final do setup | bloco "PRIMEIRO COMANDO" com o comando inicial por runtime selecionado |
| Instalar novas IAs com arquivos-modelo + fluxo no setup | wizard interativo `axiom add-tool` |
| Instalar novos templates no padrao do projeto | `axiom add-profile <nome>` e `axiom add-template <NOME>` |
| README corporativo exemplar | `README.md` (raiz) |

## Auditoria de consistencia (2026-09-03)

1. **`sdd/AGENTS.md` fantasma**: docs e adapters herdados referenciavam um `sdd/AGENTS.md`
   que o setup nunca gera. Corrigido em todo o repo: o canonico e **`AGENTS.md` na raiz**
   (todo runtime 2026 le nativamente); o roster de agentes e **`sdd/agents/README.md`**.
2. **Agents do `.github` orfaos**: o registry rendia so 4 dos 11 agentes canonicos.
   Agora os 11 sao rendidos em `.github/agents/` e `.claude/agents/`, todos apontando para
   `sdd/agents/<id>.agent.md` como comportamento canonico.
