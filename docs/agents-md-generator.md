# AGENTS.md Generator

`AGENTS.md` is **generated, contextual and small** — never a static copy of the catalog. It is
the per-project agent roster: only the agents the profile selected, each with its scope in this
project, plus the locks and the command vocabulary.

Location: **repo root `AGENTS.md`, always** (axiom-sdd decision: every 2026 runtime reads it
natively there — Codex, Devin, Copilot VS Code/IntelliJ — and Claude via `CLAUDE.md` import) —
other adapters point to the root copy.

## Inputs
`sdd/profile.yaml` (agents, specialization, gates, budget) · `sdd/sdd.yaml` (stack, gitflow,
`models:` block) · capability matrix · guardrails headline.

## Generation rules
1. Include ONLY roster agents. The full catalog stays in the template.
2. One entry per agent, ≤ 5 lines: role in THIS project (stack-specialized wording), file
   pointer, allowed writes (from matrix, concretized to real paths), the one thing it must
   never do here, and its recommended model tier (from the `models:` block, by plane).
3. Restate the six locks verbatim (the tolerated duplication) — nothing else from core.
4. Include the command vocabulary and the active profile line.
5. Regenerate whenever profile or roster changes; never hand-edit (it's framework-owned —
   customizations belong in guardrails/constitution amendments).

## Skeleton

```markdown
# AGENTS — <project>

SDD project (profile: <profile>, budget: <level>). Config: sdd/sdd.yaml · Rules:
sdd/constitution.md · Invariants: sdd/guardrails.md · Work: sdd/specs/

## Locks
<the six locks>

## Roster
### implementer — <specialization> (<stack>)
File: sdd/agents/implementer.agent.md · Writes: src/**, tests/** (own tasks) · Never: change
specs, exceed budget <level>, touch <protected areas from guardrails> · Model: balanced (<resolved>).
### <next agent…>

## Commands
SDD: refine spec <NNN> · SDD: implement <NNN> TASK-x · SDD: review <NNN> · SDD: finish <NNN>
(full list: sdd/prompts — or runtime shortcuts per adapter)
```

## Worked examples

**Legacy Java Spring Boot + feature** → roster: requirement-analyst, codebase-analyst (legacy),
spec-writer, implementer (backend/Java Spring), test-engineer (unit+regression/JUnit), reviewer,
gitflow. No architect (no flagged impact), no security (no auth/input surface — else added).

**New Next.js app** → architect (design), spec-writer, implementer (frontend/Next.js),
test-engineer (unit+e2e), reviewer, gitflow, docs. No codebase-analyst legacy mode (nothing to
excavate), analyst added the moment the codebase grows.

**Refactor** → codebase-analyst (legacy), spec-writer, architect, implementer (refactoring),
test-engineer (characterization+regression), reviewer, gitflow. Budget minimal is stated in
EVERY roster entry.
