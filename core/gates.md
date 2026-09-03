# Quality Gates

A gate is a named, checkable condition that blocks the next lifecycle step. Profiles declare which
gates apply. An agent that hits a failing gate stops and reports — it never negotiates with itself.

| Gate | Blocks | Passes when | Checked by |
|---|---|---|---|
| `spec-ready` | PLAN / implementation | Spec Readiness Score ≥ profile threshold (default 80) and no blocking Open Question — [spec-readiness.md](./spec-readiness.md) | spec-writer |
| `plan-approved` | TASKS | PLAN reviewed by architect (full/standard workflows) or explicitly waived by the workflow | architect |
| `definition-of-ready` | each task | [definition-of-ready.md](./definition-of-ready.md) satisfied | implementer (self-check) |
| `architecture-compliant` | review completion | No guardrail violation, or violation covered by an approved decision | reviewer / architect |
| `tests-passing` | review completion | Test suite green; every AC has ≥ 1 test (or an explicit recorded waiver) | test-engineer |
| `security-clear` | completion | Security review done when profile requires; no open high-severity finding | security |
| `acceptance-criteria` | completion | Every AC mapped to verifiable proof | reviewer |
| `spec-drift-none` | completion | Drift check returns `SPEC_DRIFT_NONE` — [spec-drift.md](./spec-drift.md) | reviewer |
| `evidence-complete` | gitflow | EVIDENCE.md filled per [evidence.md](./evidence.md) | gitflow (pre-check) |
| `gitflow-clean` | handoff to human | Branch/commits follow project convention; diff reviewed; nothing out of scope staged | gitflow |

## Gate failure protocol

```
1. STOP the blocked step
2. REPORT: gate name, what failed, minimal reproduction/pointer
3. ROUTE: back to the owning agent (spec gap -> spec-writer; guardrail -> architect; ...)
4. RECORD: in EVIDENCE.md if implementation already started
```

A failed gate is a routing event, not an error to hide.
