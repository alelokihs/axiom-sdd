# Requirement Traceability

Every change must be walkable end to end, in both directions:

```
Source (Jira / request)
  ↓ recorded in
SPEC (requirement IDs, ACs)
  ↓ decomposed into
TASKS (each cites the ACs it satisfies)
  ↓ produce
Implementation (diff hunks map to tasks)
  ↓ verified by
Tests (each cites the AC it proves)
  ↓ recorded in
EVIDENCE.md (AC mapping table)
  ↓ referenced by
Commit / PR (spec ID + task IDs in message)
```

## Conventions that make it work (zero tooling)

- Spec IDs: `NNN-slug` (sequential). Requirement IDs inside a spec: `FR-x`, `NFR-x`, `SEC-x`.
- ACs numbered `AC-01…` — stable, never renumbered after approval (deprecate, don't reuse).
- Tasks `TASK-001…` citing ACs. Tests reference ACs in their name or docstring where practical.
- Commits reference the spec and tasks: `feat(scope): summary` + body `SDD: 003 TASK-002`.
- EVIDENCE.md holds the closing table: `AC → task → change → test → result`.

The question "why does this code exist?" must be answerable by grep, not by memory.
