# Example — Codebase Analyst

**Scenario.** Legacy refactor of a 2,000-line `OrderService` god class; profile
`legacy-refactor`.

**Prompt.** [`prompts/analyze-legacy.md`](../prompts/analyze-legacy.md) with scope
"OrderService split".

**Context received.** The spec draft's scope + the repo (search-first).

**Expected behavior.** `legacy` mode: maps public methods and their callers (CONFIRMED via
grep), hidden couplings ("mutates `Order.status` as side effect — INFERRED, verify"), existing
coverage ("41% on service, 0% on discount branch — characterization gap"), blast radius table
(callers ranked: checkout flow HIGH, admin report LOW). Then `context-pack` mode: 14 files
(5 full, 9 signature-only).

**Expected output.** Findings summary (~40 lines, paths only) + blast-radius table +
CONTEXT-PACK.md.

**Common errors.** Pasting class bodies into findings · trusting names ("looks unused") without
grep — must be labeled INFERRED · packing 60 files "to be safe".

**Token tips.** Symbol search over directory reading; one level of imports then stop; the pack
is a manifest, not content.
