# Example — Reviewer

**Scenario.** Spec 003 implemented + tested; single review pass (standard workflow).

**Prompt.** [`prompts/review.md`](../prompts/review.md) → `code+compliance+drift`.

**Context received.** SPEC, TASKS (authorized set), the **diff**, test results, guardrails,
EVIDENCE.md. Not the unchanged sources.

**Expected behavior.** Walks AC→change→test→evidence (all mapped); walks diff→tasks and finds
a renamed helper in a file no task lists → `out-of-scope-change` (budget bounded, rename not
required) · finds error message leaking an internal path (severity Medium, route: implementer)
· re-runs the test command (cheap) to verify the claim. Changes nothing.

**Expected output.**
```
Findings:
1. [drift/out-of-scope] util.rename in src/format.ts — not in TASK-001/002 — route: human (revert or absorb)
2. [code/Medium] error string exposes /internal/path — AC-02 area — route: implementer
Drift: SPEC_DRIFT_DETECTED (1) · ACs: 3/3 proven · Gates: tests-passing PASS, acceptance-criteria PASS
```

**Common errors.** Fixing finding 2 itself ("it's one line") — reviewers change nothing ·
softening findings · reviewing intentions ("they probably meant…") instead of the diff.

**Token tips.** Diff + signatures only; whole files only when a hunk is unintelligible.
