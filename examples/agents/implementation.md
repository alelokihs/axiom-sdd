# Example — Implementer

**Scenario.** Spec 003 (legacy-feature, budget bounded), TASKS ready. Developer authorizes two.

**Prompt.** [`prompts/implement.md`](../prompts/implement.md):
`SDD: implement 003 TASKS: TASK-001, TASK-002`.

**Context received.** SPEC ACs + the two task entries + CONTEXT-PACK files + guardrails +
conventions. Nothing else.

**Expected behavior.** DoR self-check passes → implements exactly TASK-001/002 following
existing patterns; runs lint+tests with the project's real commands; notices TASK-003's file
would "only take a minute" — and does NOT touch it. Discovers the spec missed a null case →
records Open Question + handles per spec's error section (or stops if blocking). Fills
evidence: files, commands with real results, AC mapping, one decision entry (chose existing
util over new dep).

**Expected output.** Diff limited to authorized scope + EVIDENCE.md sections + updated task
statuses.

**Common errors.** "While I'm here" refactors (budget violation) · editing the SPEC to match
the code · inventing the null-case behavior · `tests pass` without a real run line.

**Token tips.** Loads only pack files; asks for the diff of its own change when reviewing
itself, not re-reads of whole files.
