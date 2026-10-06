# Axiom SDD

> **2.1.0 preview:** [English article + Português](docs/articles/axiom-sdd-from-intent-to-evidence.md) · [Launch post](docs/launch/social-post-en-pt.md) · [Evidence metrics](docs/METRICS.md) · [Change review](https://github.com/alexandrehenrique-dev/axiom-sdd/pull/1)
>
> A repository-based contract for AI-assisted development: specifications, bounded tasks and reviewable evidence. Screenshots in the article show a consumer prototype, not an Axiom application UI.

> **Spec-Driven Development para times que trabalham com IAs agenticas.**
> Um comando, qualquer sistema operacional, zero dependencias: detecta seu projeto e suas
> ferramentas de IA, compoe a metodologia certa e configura Copilot, Claude Code, Codex e
> Devin para trabalharem sob specs, gates e evidencias — nunca "do pedido direto ao codigo".

Nascido da unificacao de `template-sdd` (metodologia) e `sdd-setup` (ambiente).
Historico e decisoes: [docs/DECISIONS.md](docs/DECISIONS.md) · [CHANGELOG.md](CHANGELOG.md)

---

## Sumario

- [Requisitos](#requisitos)
- [Instalacao rapida](#instalacao-rapida)
- [O que e instalado no seu projeto](#o-que-e-instalado-no-seu-projeto)
- [Fluxo de uma feature](#fluxo-de-uma-feature)
- [Comandos do CLI](#comandos-do-cli)
- [Guia de pastas](#guia-de-pastas)
- [Estendendo o framework](#estendendo-o-framework)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)

## Requisitos

**Python 3.8+** (somente biblioteca padrao — nenhum `pip install`) e, para a camada git,
um repositorio git no projeto alvo. Nada mais, em nenhum sistema operacional.

## Instalacao rapida

Clone este repositorio e rode o setup apontando para o projeto onde quer usar SDD:

| SO | Comando |
|---|---|
| **Linux / macOS** | `./install.sh --target /caminho/do/projeto` |
| **Windows (PowerShell)** | `.\install.ps1 --target C:\caminho\do\projeto` |
| **Qualquer SO (direto)** | `python3 cli/axiom.py install --target /caminho/do/projeto` |

Sem flags adicionais o setup e **interativo**: mostra o diagnostico da maquina
(`AXIOM DOCTOR`), detecta o projeto (linguagens, frameworks, Terraform, automacao de
testes, indicios de legado — sempre confirmavel, nunca decidido por voce), pergunta a
intencao, os runtimes e o modo git, compoe tudo e termina com o **primeiro comando**
("Hello World") da IA que voce escolheu.

Para automacao / CI (sem perguntas):

```bash
python3 cli/axiom.py install --target ../meu-projeto \
  --profile legacy-refactor --runtimes claude-code,copilot-vscode --git-mode stealth --yes
```

Modos git: `stealth` (default — tudo via `.git/info/exclude`, nada e commitado),
`team` (arquivos de entrada commitaveis) e `none`.

## O que e instalado no seu projeto

```
<projeto>/
  AGENTS.md                        # entrada CANONICA (todo runtime 2026 le nativamente)
  CLAUDE.md                        # @AGENTS.md + notas Claude
  .github/copilot-instructions.md  # ponteiro (Copilot antigo, Visual Studio, Xcode)
  .github/prompts/sdd-*.prompt.md  # /sdd-init, /sdd-spec... no VS Code
  .github/agents/sdd-*.agent.md    # os 11 agentes SDD no dropdown do Copilot Chat
  .claude/commands/sdd-*.md        # /sdd-* no Claude Code
  .claude/agents/sdd-*.md          # subagentes no Claude Code (/agents)
  .codex/skills/sdd-*/SKILL.md     # skills do Codex
  sdd/
    core/ templates/ agents/       # metodologia (framework-owned: update sobrescreve)
    profile.yaml workflow.yaml     # composicao resolvida para ESTE projeto
    gitflow.md                     # SEU gitflow (project-owned — customize a vontade)
    guardrails.md sdd.yaml         # config do projeto (project-owned)
    specs/ decisions/              # seu trabalho (project-owned — nunca tocado)
    manifest.json                  # lockfile da instalacao (versao, profile, runtimes)
    devin-playbook.md              # texto pronto para o app do Devin
```

Todo arquivo compartilhado usa **bloco gerenciado**: se ja existia, so o bloco e
adicionado/substituido. Re-executar e sempre seguro (idempotente).

## Fluxo de uma feature

1. `axiom install` uma unica vez no projeto (ou `update` apos atualizar o framework).
2. Abra sua IA no projeto e rode o Hello World exibido no fim do setup — ex.: `/sdd-init`.
3. **Spec primeiro**: `/sdd-spec 001` — o spec-writer estrutura a demanda, aponta lacunas
   (`UNKNOWN` / `NEEDS_CONFIRMATION`) e so libera com readiness acima do limiar do profile.
4. **Implementacao autorizada**: `/sdd-implement 001 TASK-1` — o implementer so toca o que
   a task autoriza, dentro do change budget.
5. **Review + evidencias**: `/sdd-review 001` — gates do workflow (testes, seguranca,
   drift de spec) antes de qualquer merge.
6. **Entrega**: `/sdd-finish 001` — branch, commits e PR conforme `sdd/gitflow.md`, com o
   agente se identificando no trailer do commit.

## Comandos do CLI

| Comando | Faz |
|---|---|
| `axiom install [--target] [--profile] [--runtimes] [--git-mode] [--yes]` | setup completo (interativo sem flags) |
| `axiom doctor [--target]` | diagnostico da maquina + deteccao do projeto; nao escreve nada |
| `axiom update [--target]` | re-copia arquivos framework-owned e regenera shims; project-owned intocado |
| `axiom remove [--target]` | desfaz shims, exclude e manifest (specs e decisions ficam) |
| `axiom add-tool` | registra uma nova IA agentica (wizard) |
| `axiom add-profile <nome>` / `axiom add-template <NOME>` | scaffolds no padrao da casa |
| `axiom list-profiles` | lista os 22 profiles |

(`axiom` = `./install.sh` no Linux/macOS, `.\install.ps1` no Windows, ou `python3 cli/axiom.py`.)

## Guia de pastas

| Pasta | Conteudo | Quem edita |
|---|---|---|
| `core/` | metodologia agnostica: constitution, gates, lifecycle, evidencias, token economy | mantenedores |
| `profiles/` | 22 manifestos declarativos de composicao (`extends: _defaults`) | `axiom add-profile` |
| `workflows/` | fast · standard · full · hotfix | mantenedores |
| `agents/` | 11 agentes canonicos + capability-matrix | mantenedores |
| `adapters/` | 1 pasta por IA; `tool.json` (fonte executavel) + `docs/` (doc oficial do vendor) | `axiom add-tool` |
| `templates/` | SPEC, PLAN, TASKS, ADR, EVIDENCE... | `axiom add-template` |
| `gitflow/` | gitflow default instalado como `sdd/gitflow.md` (project-owned) | seu time |
| `cli/` | o motor: axiom.py + axiomcli (doctor, detect, ui, compose, shims, gitexclude, scaffold) | mantenedores |
| `examples/` | cenarios e prompts prontos — nunca instalados no consumidor | todos |
| `docs/` | decisoes, metodologia, historia | mantenedores |

## Estendendo o framework

**Nova IA agentica**: `axiom add-tool` pergunta id, tipo, deteccao e shims, cria
`adapters/<id>/tool.json` (mesclado ao registry automaticamente) e `adapters/<id>/docs/`
— cole ali a documentacao oficial baixada do vendor; os agentes a consultam quando
precisam de detalhes do runtime. Nenhuma linha de codigo do motor muda.

**Novo profile ou template**: `axiom add-profile meu-cenario` / `axiom add-template MEU-DOC`
geram arquivos pre-comentados no padrao da casa; preencha e pronto.

## FAQ

**Como o Axiom se comporta com Terraform / IaC?**
A deteccao reconhece `*.tf` e sugere o profile `infrastructure-change`: change budget
minimo, `terraform plan` anexado a spec ANTES de implementar, gate de revisao humana do
plan antes de qualquer apply, evidencias de apply por ambiente e checagem de drift entre
codigo e state. Agentes `architect` e `security` entram no roster automaticamente.

**Como fica um projeto de automacao de testes?**
Cypress/Playwright/Robot/Selenium/Karate sao detectados; o profile sugerido e
`test-coverage`, cujo Definition of Done exige suites verdes e cobertura rastreada na
spec. Em projetos legados, o `test-engineer` comeca por testes de caracterizacao que
congelam o comportamento atual antes de qualquer mudanca.

**Posso usar meu proprio gitflow?**
Sim — `sdd/gitflow.md` e project-owned: substitua pelo seu. Os agentes detectam qual
runtime sao e seguem os trailers e regras do SEU arquivo.

**Stealth mode funciona com agentes cloud (Devin, Codex cloud)?**
Nao — eles clonam do remoto e nao enxergam arquivos escondidos localmente. Use
`--git-mode team`, ou o `sdd/devin-playbook.md` colado no app do Devin.

## Troubleshooting

- **`/sdd-*` nao aparece no VS Code**: recarregue a janela; habilite `chat.promptFiles` e
  `chat.useAgentsMdFile` (se estiverem travados, e policy corporativa); use o modo Agent.
- **IntelliJ nao mostra nada**: por design — nao ha prompt files de repo no plugin
  JetBrains; o vocabulario `SDD: ...` viaja no `AGENTS.md` (plugin ≥ mar/2026).
- **`axiom doctor`** e sempre o primeiro passo: mostra o que foi detectado, com evidencia.
- Instalacoes antigas feitas pelo `sdd-setup` sao reconhecidas (marcadores compativeis):
  rode `axiom install` por cima e os blocos serao migrados.

---

Mantido pelo time. Contribuicoes seguem o proprio metodo: spec antes de codigo.
