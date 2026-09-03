# HOTFIX — <name>  *(single-doc: spec + tasks + evidence)*

- **Spec:** `<NNN>-<slug>` · **Profile:** hotfix/incident-remediation · **Budget:** minimal
- **Source:** <incident/ticket> · **Impact:** <who/what is hurting now>

## Failure
Observed behavior · expected behavior · reproduction (or why not reproducible).

## Root cause
Hypothesis → confirmed cause (update as learned; provisional is fine, silent is not).

## Fix (the task)
Minimal change, files listed. **AC-01** — regression scenario passes; **AC-02** — no adjacent behavior change.

## Evidence  *(filled during execution)*
- Changed files:
- Commands + real results:
- Regression test (fails before / passes after):
- Drift verdict:
- Assumptions that survived:

## Follow-up (mandatory)
What was deferred (root-cause hardening, cleanup, missing tests) → follow-up spec: `<NNN+1>` or "none, justified: …"
