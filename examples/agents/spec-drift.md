# Example — Spec Drift Detection (reviewer mode)

**Scenario.** After implementation of spec 002, someone "helpfully" added retry logic not in
the spec, and AC-03 has no test.

**Prompt.** [`prompts/detect-drift.md`](../prompts/detect-drift.md).

**Context received.** SPEC (ACs, scope), TASKS, diff, test list/results, guardrails.

**Expected behavior.** AC walk: AC-01, AC-02 proven; AC-03 → no test → `missing-test`.
Diff walk: retry block in `client.py` maps to no task → `unspecified-behavior` +
`out-of-scope-change`. Guardrail check: retry loop violates "timeouts handled by platform
layer" → `architecture-divergence`.

**Expected output.**
```
SPEC_DRIFT_DETECTED
- [missing-test] AC-03 uncovered — route: test-engineer
- [unspecified-behavior/out-of-scope] retry logic in client.py — spec silent — route: human (remove or spec absorbs)
- [architecture-divergence] retry vs platform-layer guardrail — route: architect
```

**Common errors.** Removing the retry logic itself (drift detector never fixes) · classifying
the good-looking retry as "fine" because it's useful · passing drift because tests are green.

**Token tips.** The AC walk + diff walk needs the diff, not the repository.
