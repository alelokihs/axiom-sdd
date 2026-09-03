# Spec Lifecycle

```
Request
  ↓  requirement-analyst        (normalize, detect ambiguity, classify gaps)
SPEC                            ── Gate 1: spec-ready (Readiness ≥ threshold)
  ↓  architect (when needed)    (impact, decisions, guardrail check)
PLAN                            ── Gate 2: plan-approved
  ↓  spec-writer
TASKS                           ── Gate 3: definition-of-ready
  ↓  implementer(s)             (only authorized tasks, within change budget)
Implementation
  ↓  test-engineer
Tests                           ── Gate 4: tests-passing
  ↓  reviewer                   (code + spec compliance + drift)
Review                          ── Gate 5: acceptance-criteria + spec-drift-none
  ↓  executing agents
Evidence                        ── Gate 6: evidence-complete
  ↓  gitflow
Commit / branch / PR prep       ── Gate 7: gitflow-clean
```

## Collapsing steps (proportionality)

The pipeline is logical, not ceremonial. The workflow definition
([workflows/](../workflows/README.md)) selected by the profile decides which steps run as
separate agent executions and which collapse into one:

| Work size | Typical workflow | What collapses |
|---|---|---|
| Hotfix / trivial bugfix | `hotfix` | SPEC+PLAN+TASKS become one short document; review+drift one pass |
| Small bounded change | `fast` | PLAN merges into SPEC; single implementer pass |
| Standard feature | `standard` | Full pipeline, single review pass |
| Architectural change | `full` | Nothing collapses; architect and security are mandatory |

What is **never** skipped, at any size: acceptance criteria, the security question in the spec,
evidence, and drift check.

## State model

Every spec directory `sdd/specs/<NNN>-<slug>/` has a status in its SPEC header:

```
DRAFT -> IN_REVIEW -> APPROVED -> IN_PROGRESS -> IMPLEMENTED -> VALIDATED -> DONE
                                       ↘ BLOCKED (open blocking question)
any state -> OBSOLETE
```

## When something changes mid-flight

| Situation | Correct action |
|---|---|
| Discovery invalidates the spec | Go back to SPEC. Never adjust code and move on |
| New requirement appears | Record it at the source (spec / backlog), then update SPEC |
| Plan proves unviable | Update PLAN, re-check TASKS |
| Ambiguity found | Open Question. Blocking ones stop the affected task |
| Code diverges from spec | Record in EVIDENCE.md; never resolve silently |
