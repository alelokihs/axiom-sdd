# Gitflow — axiom-sdd (default, project-owned after install)

> Instalado como `sdd/gitflow.md` no projeto consumidor. **Project-owned**: o time pode
> substituir este arquivo inteiro pelo gitflow proprio — os agentes seguem o que estiver la.

## Branches

| Tipo | Padrao | Exemplo |
|---|---|---|
| Feature | `feat/spec-<id>-<slug>` | `feat/spec-001-checkout-pix` |
| Bugfix | `fix/spec-<id>-<slug>` | `fix/spec-014-rounding` |
| Hotfix | `hotfix/<slug>` | `hotfix/npe-payment` |
| Refactor | `refactor/spec-<id>-<slug>` | `refactor/spec-007-order-service` |

Nunca commitar direto em `main`/`master`/`develop`. Um branch por spec.

## Commits (Conventional Commits + rastreabilidade SDD)

```
<type>(<escopo>): <resumo imperativo>       # type: feat|fix|refactor|test|docs|chore

Spec: <id>          # spec que autorizou a mudanca
Task: TASK-<n>      # task explicitamente autorizada
```

## Identificacao do agente (obrigatoria)

O agente que gerou o commit DEVE detectar qual runtime ele e — pelo proprio conhecimento
de qual produto esta executando — e assinar com o trailer correspondente:

| Runtime | Trailer |
|---|---|
| Claude Code | `Co-Authored-By: Claude <noreply@anthropic.com>` + `Agent: claude-code` |
| GitHub Copilot | `Co-Authored-By: GitHub Copilot <copilot@github.com>` + `Agent: copilot` |
| OpenAI Codex | `Co-Authored-By: Codex <codex@openai.com>` + `Agent: codex` |
| Devin | `Co-Authored-By: Devin <devin@cognition.ai>` + `Agent: devin` |

Runtime nao listado: use `Agent: <id-do-adapter>` (o id em `adapters/*/tool.json`).

## Regras invioladas

1. Nenhum commit sem task autorizada (locks do AGENTS.md).
2. Nunca `push --force` em branch compartilhado; nunca reescrever historico publicado.
3. PR referencia a spec e anexa as evidencias exigidas pelo profile (`sdd/profile.yaml`).
4. Merge so com os gates do workflow verdes (`sdd/workflow.yaml`).
