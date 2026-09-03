# Adapter — OpenAI Codex

## Capabilities assumed
Reads `AGENTS.md` at repo root natively (also nested per-directory AGENTS.md; nearest wins) ·
cloud tasks and CLI sessions · runs commands/tests in sandbox · per-task delegation model.

## Files bootstrap generates

**`AGENTS.md` (repo root)** — Codex's native entry file IS the generated SDD roster: the
[generator](../../bootstrap/agents-md-generator.md) output is written to the root for Codex
projects (axiom-sdd rule: root `AGENTS.md` is ALWAYS the canonical copy for every runtime;
nothing is duplicated under `sdd/`). It contains: project pointer block,
the six locks, the roster (role → file → allowed writes), workflow summary, and the command
vocabulary (`SDD: spec 001`, `SDD: implement 001 TASK-002`, …).

Optionally, nested `AGENTS.md` in high-risk directories (e.g. `migrations/AGENTS.md`:
"changes here require the database-change profile — check sdd/specs/ for authorization").

## Runtime notes
- Codex tasks are delegation-shaped: one task = one lifecycle step (or one collapsed workflow
  step), with the task text naming spec + step + agent role. Keep tasks small; the evidence
  file is the cross-task memory.
- Cloud sandbox may lack your private network: mark unrunnable validations `NOT_RUN: <reason>`
  in evidence rather than faking results; CI re-runs them.
- Codex proposes diffs/PRs — the gitflow agent rules still apply: a human merges.

## Model tiers
Resolution for the `models:` block (use the org's available Codex/OpenAI models; record actual
names in `sdd.yaml`):

| Tier | Resolve to |
|---|---|
| fast | the light/mini codex model available |
| balanced | the standard codex/agent model |
| frontier | the highest-reasoning model available (max reasoning effort) |

In Codex CLI, set the model per session/config; cloud tasks follow workspace defaults — note
deviations in evidence.
