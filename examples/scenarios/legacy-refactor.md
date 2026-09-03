# Tutorial — Legacy refactor with a frozen-behavior contract

Project: 8-year-old Java Spring monolith. Goal: split `OrderService` (2,000 lines) so discount
logic becomes testable. Runtime: Copilot.

## 1. Bootstrap

```
Initialize SDD.
Framework: ../sdd-framework
Runtime: Copilot
Source:
Split OrderService: discount calculation must become its own unit-testable component.
No behavior change allowed. This code has burned us twice.
```

→ profile `legacy-refactor` (workflow standard, **budget minimal**, readiness bar 85),
models: planning=frontier (legacy analysis), execution=frontier (large blast radius),
support=fast. Roster includes architect + codebase-analyst(legacy) + test-engineer
(characterization+regression).

## 2. Legacy analysis BEFORE the spec is finished

```
/sdd-analyze-legacy  scope: OrderService split
```
Output (paths, not dumps): 9 public methods and their callers · side effect found
(`applyDiscount` mutates `Order.status` — INFERRED, flagged) · coverage 41%, discount branch
0% → characterization gap · blast radius: checkout HIGH, admin report LOW.

## 3. Spec with a refactoring boundary

SPEC declares: boundary (what moves, what is untouchable), **AC-01: characterization suite
green and unmodified after the refactor**, AC-02: discount logic reachable without HTTP layer,
OUT: any behavior fix (the side effect is recorded as debt, NOT fixed now — budget minimal).
Readiness 87 ✔.

## 4. Characterization first (the non-negotiable step)

```
/sdd-implement 002 TASKS: TASK-001   ← "pin current behavior"
```
test-engineer (characterization mode) writes tests asserting CURRENT behavior — including the
ugly side effect, with a comment linking the debt entry. Suite green = the safety net exists.

## 5. Refactor inside the net

TASK-002/003: extract `DiscountCalculator`, move call sites. Characterization suite stays
green and **unmodified** (modifying it = drift). Reviewer + drift check confirm:
`SPEC_DRIFT_NONE`, structure map before/after in evidence.

## 6. Close

Evidence records: the surviving side effect (debt entry D-011 → future spec), regression run,
structure map. Commit + PR; the PR body warns reviewers exactly where behavior was pinned.

**Why this works.** The budget forbade "fixing" the side effect mid-refactor — that instinct
is how legacy refactors turn into incidents. The debt entry keeps the fix honest and separate.
