# Tutorial — From a Jira issue to a merged feature

The canonical flow, end to end, exactly as a developer experiences it. Project: existing
Python/FastAPI service. Runtime: Claude (any runtime works the same — only shortcuts differ).

## 1. Bootstrap (once per project)

```
Initialize SDD.
Framework: ../sdd-framework
Source:
[BILL-482] Monthly invoice PDF. As a customer I want to download a PDF of my monthly
invoice from the billing page. Must match the web amounts. Finance wants the legal
footer included.
```

The agent detects (`python 3.12 CONFIRMED: pyproject.toml`, `fastapi CONFIRMED`, `pytest
CONFIRMED`, `github-flow INFERRED: main + short branches`), classifies → `backend-feature`
(runner-up `fullstack-feature` reported), selects models (planning=frontier,
execution=balanced, verification=balanced, support=fast), installs `sdd/`, generates
`CLAUDE.md`, `.claude/commands/sdd-*`, `AGENTS.md` (repo root), spec draft, context pack, and prints:

```
SDD INITIALIZED
Project:  billing-svc (existing) · Runtime: Claude
Profile:  backend-feature (workflow: standard) · Change budget: bounded
Spec:     sdd/specs/001-invoice-pdf/ (DRAFT)
Readiness: 74 — REVIEW_REQUIRED
NEEDS_CONFIRMATION: legal footer source? · which amounts are canonical (web vs ledger)?
NEXT ACTION: SDD: refine spec 001   (answer the 2 items above)
```

## 2. Refine to READY

```
SDD: refine spec 001
Footer text comes from settings.LEGAL_FOOTER. Ledger is canonical; web reads the same API.
```
→ readiness 88 (READY). PLAN + TASKS generated (3 tasks). Gate `spec-ready` ✔.

## 3. Context pack & implementation

```
SDD: implement 001 TASKS: TASK-001, TASK-002
```
DoR self-check ✔ → code inside the pack's 11 files, budget bounded, evidence filling as it
goes. TASK-003 (endpoint wiring) authorized next, same shape.

## 4. Tests → review → drift

```
SDD: tests for 001          → AC map complete, 1 UNPROVEN (load test → CI), suite green
SDD: review 001             → 1 Medium finding (route implementer), fixed, re-reviewed
                            → Drift: SPEC_DRIFT_NONE
```

## 5. Evidence + Git

```
SDD: finish 001
```
Audit → commit `feat(billing): add monthly invoice PDF endpoint` (+ `SDD: 001 TASK-001..003`)
→ PR body from evidence (summary, AC table, risks, UNPROVEN note). Human merges.

**Traceability check** (what the framework guarantees): BILL-482 → SPEC 001 → AC-01..04 →
TASK-001..003 → diff hunks → tests → EVIDENCE table → commit trailer. Greppable both ways.
