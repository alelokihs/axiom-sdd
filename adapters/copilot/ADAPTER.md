# Adapter — GitHub Copilot

## Capabilities assumed
`.github/copilot-instructions.md` auto-loaded · prompt files `.github/prompts/*.prompt.md` as
slash commands (agent mode) · edits + terminal in agent mode · smaller effective context than
long-session tools — the adapter leans hardest on pointers.

## Files bootstrap generates

**`.github/copilot-instructions.md`** (~25 lines): same shape as the Claude entry file — project
pointer block + the six locks + "discover your agent role in `sdd/agents/`, obey its Mandatory
Reading/Forbidden". Keep it short: Copilot pays this cost on every request.

**`.github/prompts/<name>.prompt.md`** — one per ready prompt, front-matter `mode: agent`,
body = the canonical shortcut pattern (proven in the reference implementation):

```markdown
---
mode: agent
description: Implement ONLY explicitly authorized tasks
---
# /sdd-implement
> Canonical behavior: sdd/agents/implementer.agent.md — read it fully before acting.
Input: FEATURE <NNN>-<slug> · TASKS: TASK-00X[, ...]
Locks: no explicit task list = no authorization · DoR must pass · stay in change budget ·
divergence recorded, never fixed silently · no secrets.
```

## Runtime notes
- Copilot won't reliably hold the whole methodology — that's fine: the locks travel in the
  prompt file, everything else is read from `sdd/` when the prompt says so.
- Context packs matter most here: reference the CONTEXT-PACK.md and let Copilot open files.
- Non-agent (inline) Copilot: still benefits from instructions file; SDD flow needs agent mode.

## Model tiers
Copilot's model picker resolves the `models:` block (names as offered by the org's Copilot
plan — record the actual pick in `sdd.yaml`):

| Tier | Resolve to |
|---|---|
| fast | the default/fast completion model |
| balanced | a mid-tier agent-mode model (e.g. current GPT/Claude standard option) |
| frontier | the strongest reasoning model the picker offers |

Set the model in the Copilot chat picker before running a prompt file; prompt files can note
the expected tier in their description.
