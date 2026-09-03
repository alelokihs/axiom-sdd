# Recipe — Security fix

Profile [`security-fix`](../../sdd/profiles/security-fix.yaml) · budget minimal · gate
`security-clear`.

1. Understand the exploit path first; write it down with restraint (no weaponized PoC in the
   repo; no secrets/PII in any artifact).
2. Regression test proves the path is closed — asserting the behavior, not the exploit string.
3. Minimal fix; the security agent verifies (review pass separate from the fixing pass, even
   when the same runtime does both).
4. Disclosure constraints (who may know what, when) recorded in the spec header.

**Watch for:** fixing one instance of the pattern and missing the others (the security agent
greps for siblings) · High finding "accepted" without a named human in SECURITY-REVIEW.md.
