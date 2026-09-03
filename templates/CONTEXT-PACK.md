# CONTEXT PACK — <NNN>-<slug>

> Manifest, not content: paths + one-line reasons. Agents load what's listed and nothing else.
> Built by codebase-analyst (context-pack mode). Cap ~20 files — more means split the spec or
> tighten discovery. Rules: `sdd/core/context-engineering.md`.

## Always
- `sdd/specs/<NNN>-<slug>/SPEC.md` — the contract of this work
- `sdd/guardrails.md` — invariants (summary sections: …)

## Source files
| Path | Why | Load |
|---|---|---|
| `src/…` | to be modified by TASK-001 | full |
| `src/…` | contract the change must respect | signature only |

## Related tests
| Path | Why |
|---|---|

## Decisions & conventions
- `sdd/decisions/ADR-00X-…` — constrains …
- lint/format config: `…`

## Per-step trimming
- implementer: everything above
- test-engineer: SPEC §6/§11 + changed files + related tests
- reviewer: SPEC + TASKS + **diff** + test results + guardrails (not the sources)
