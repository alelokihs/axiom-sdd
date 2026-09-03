# Example — Security Agent

**Scenario.** Integration profile: new webhook endpoint receiving third-party JSON.

**Prompt.** [`prompts/security-check.md`](../prompts/security-check.md).

**Context received.** SPEC security section, the diff, guardrails security invariants,
dependency changes.

**Expected behavior.** Threat sketch (3 lines: untrusted payload → parser → DB). Checks:
signature verification of webhook (FINDING: missing — High), schema validation
(OK: strict parse), secrets (OK), logging (FINDING: full payload logged, may carry PII —
Medium), deps (new `jsonschema` lib — advisory check OK). Verdict `FINDINGS_OPEN`; High blocks
`security-clear`.

**Expected output.** SECURITY-REVIEW.md with the findings table; no fixes implemented.

**Common errors.** Approving with the High open "since it's internal" · pasting a sample real
payload with PII into the review · checklist noise (10 theoretical findings, none exploitable
here).

**Token tips.** Reviews the diff and entry points, not the whole service.
