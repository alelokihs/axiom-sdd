# Adapter — Claude (Claude Code / Claude apps)

## Capabilities assumed
Full file read/write in workspace · shell execution · long agentic sessions · `CLAUDE.md`
auto-loaded · optional subagents & slash commands (`.claude/commands/`, `.claude/agents/`).

## Files bootstrap generates

**`CLAUDE.md`** (repo root, ~30 lines):
```markdown
# <project> — SDD project
This repo uses Spec-Driven Development. Config: sdd/sdd.yaml · Roster: sdd/agents/README.md
Rules: sdd/constitution.md · Invariants: sdd/guardrails.md · Active work: sdd/specs/

## Locks
- Never go from request to code: SPEC -> PLAN/TASKS -> implementation -> review -> evidence.
- Implement only explicitly authorized tasks, within the declared change budget.
- Gaps become UNKNOWN / ASSUMPTION / NEEDS_CONFIRMATION — never invented facts.
- Spec<->code divergence is recorded in EVIDENCE.md, never silently resolved.
- No secrets in code/logs/prompts. No force-push, no merges, no destructive git.

## Working
Assume the agent role the task names (file in sdd/agents/): obey its Mandatory Reading and
Forbidden sections and the capability matrix. Commands: .claude/commands/sdd-*.md
```

**`.claude/commands/sdd-*.md`** — one per ready prompt (`sdd-init`, `sdd-spec`, `sdd-implement`,
`sdd-review`, `sdd-finish`, …): each ≤ 10 lines, argument hint + pointer to the agent file.

## Runtime notes
- Claude reads files on demand — context packs work natively; point, don't paste.
- For heavy phases, suggest subagents mirroring catalog roles (planner vs implementer) so
  planning context doesn't pollute execution context.
- Hooks (if the team uses them) can enforce gitflow safety mechanically; optional.

## Model tiers
Resolution for the `models:` block (use the org's available versions; substitute nearest tier
and record it if restricted):

| Tier | Resolve to |
|---|---|
| fast | Claude Haiku (latest) |
| balanced | Claude Sonnet (latest) |
| frontier | Claude Opus (latest) |

In Claude Code, per-agent model can be pinned via subagent config; otherwise state the model
choice at session start.
