# SPEC — <Feature name>

- **Spec:** `<NNN>-<slug>` · **Status:** DRAFT | IN_REVIEW | APPROVED | IN_PROGRESS | IMPLEMENTED | VALIDATED | DONE | BLOCKED | OBSOLETE
- **Profile:** `<profile>` · **Change budget:** `<level>` · **Date:** <YYYY-MM-DD>
- **Source:** <Jira key / link / "verbal request from X">

## 1. Context
Why this exists. 2–5 lines. Link the source verbatim text if long.

## 2. Objective
One testable sentence: what the system does after this that it didn't before.

## 3. Requirements
| ID | Requirement | Origin | Status |
|---|---|---|---|
| FR-1 | | source §… | CONFIRMED / INFERRED / ASSUMPTION |
| NFR-1 | | | |
| SEC-1 | | | |

## 4. Expected behavior
Observable behavior: inputs → transformation → outputs. Include error behavior — what happens
on invalid input, dependency failure, timeout.

## 5. Contracts
Conceptual (not implementation). New/changed interfaces, schemas, events. For changed contracts:
who consumes them (feeds `api-change`/`integration` gates).

## 6. Acceptance criteria
Verifiable, numbered, stable after approval (deprecate, never renumber).
- **AC-01** — Given … when … then …
- **AC-02** —

## 7. Scope boundary
**In:** …
**Out (explicitly):** …

## 8. Dependencies
| Dependency | Type | Status |
|---|---|---|

## 9. Architecture & guardrails impact
Touched boundaries/layers; guardrails at risk; ADR needed? (yes → which decision).

## 10. Security
Untrusted input involved? Sensitive data? Auth changes? What must never be logged?
(Profiles with the security agent expand this in SECURITY-REVIEW.md.)

## 11. Test strategy
Test modes (from profile) and what each proves. AC ↔ test-type mapping sketch.

## 12. Risks
| Risk | Likelihood | Mitigation / acceptance |
|---|---|---|

## 13. Implementation constraints
Hard constraints the implementer must respect (perf targets, compat, deadlines, sequencing).

## 14. Open questions
| # | Question | Classification | Blocking? | Status |
|---|---|---|---|---|
| 1 | | UNKNOWN / ASSUMPTION / NEEDS_CONFIRMATION | Yes/No | Open |

> A blocking open question caps readiness at 59 (SPEC_NOT_READY).

## 15. Readiness
Filled by spec-writer (validate mode) — 10 criteria × one line + score + verdict.
See `sdd/core/spec-readiness.md`.
