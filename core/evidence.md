# Evidence Model

> Agents don't declare tasks complete; they present evidence.

Every executed spec has one `EVIDENCE.md` (template: [templates/EVIDENCE.md](../templates/EVIDENCE.md)),
filled incrementally by the agents that did the work and verified by the reviewer/gitflow gates.

## The evidence pack

| Section | Filled by | Proof of |
|---|---|---|
| Changed files | implementer | what was touched (paths + why) |
| Executed commands | implementer / test-engineer | build/lint/test actually ran (command + result line) |
| Tests | test-engineer | what exists, what passed, what's not covered and why |
| AC mapping | implementer + reviewer | every AC → change → test → result |
| Architecture validation | reviewer/architect | guardrails checked, deviations recorded |
| Security validation | security (when in profile) | findings + status |
| Drift verdict | reviewer | `SPEC_DRIFT_NONE` or detected list |
| Known risks & limitations | any | what could still bite |
| Assumptions | any | every `ASSUMPTION`/`NEEDS_CONFIRMATION` that survived |
| Decisions | any | pointers into the decision log |
| Technical debt left | any | recorded debt, never silent debt |

## Rules

- Evidence references **real outputs** (test summary line, command exit) — never "tests pass"
  without having run them. If a command couldn't run, say so: `NOT_RUN: <reason>`.
- Claims map to proof. An AC without a mapped test/verification is `UNPROVEN`, and Gate
  `acceptance-criteria` fails.
- Evidence is append-friendly and diff-friendly: short lines, stable ordering.
- The evidence pack is the input for commit messages and PR descriptions (gitflow agent) —
  write it once, reuse it.
