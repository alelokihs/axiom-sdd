# Example — Spec Writer

**Scenario.** Analyst output for the checkout-latency issue exists; profile
`performance-improvement` (workflow standard).

**Prompt.** `SDD: refine spec 001` after the human answers "target p95 < 800ms, payment step".

**Context received.** Analyst sections, profile, guardrails summary, answers. No source code
(contract sketches only if needed).

**Expected behavior.** Writes full SPEC: objective ("checkout p95 < 800ms at payment step"),
ACs (AC-01 baseline recorded; AC-02 p95 < 800ms same methodology; AC-03 no behavior change),
scope OUT ("no UI changes"), risks, test strategy (regression + benchmark), constraints.
Then validate mode: 10 one-liners, score 86 → READY.

**Expected output.** SPEC.md + readiness block. Then PLAN/TASKS when workflow reaches them.

**Common errors.** Scoring without the 10 justifications · weakening AC-02 to "faster" to pass
the gate · absorbing the UNKNOWNs silently instead of carrying them.

**Token tips.** Compact forms for fast/hotfix profiles; `N/A` for empty sections; never paste
the whole guardrails file into the spec.
