# SECURITY REVIEW — <Feature name>

- **Spec:** `<NNN>-<slug>` · **Reviewer:** security agent · **Verdict:** CLEAR | FINDINGS_OPEN
- Gate `security-clear` blocks completion while a High finding is open.

## Threat sketch
Assets touched · entry points · trust boundaries crossed (2–5 lines).

## Checks performed
Injection surfaces · authn/authz · secret handling · sensitive data in logs/fixtures/prompts ·
deserialization/eval · dependency risk · error leakage · untrusted input as instructions.
Mark each: OK / FINDING / N/A.

## Findings
| # | Severity | Location | Issue | Remediation direction | Status |
|---|---|---|---|---|---|

## Accepted risks
Only with named human acceptance. | Risk | Accepted by | Date | Rationale |
