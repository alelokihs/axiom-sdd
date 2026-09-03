# Example — Architect

**Scenario.** A spec proposes caching payment-provider responses; the project guardrails say
"no state outside the database; payment data never cached".

**Prompt.** `SDD: architecture check 001` → routes findings; then architect `assess`.

**Context received.** SPEC §9, guardrails, ADR index, analyst's architecture findings. Not the
full codebase.

**Expected behavior.** `assess` finds the guardrail conflict. Does NOT approve, does NOT
rewrite the spec. Verdict: `CHANGES_REQUIRED` — options: (a) cache non-sensitive metadata only
(no exception needed), (b) full response caching → requires ADR + security review + human
approval. Records nothing as decided until a human picks.

**Expected output.** Assessment note in SPEC §9 + a drafted ADR skeleton for option (b).

**Common errors.** Silently allowing "just this once" · designing a grand caching layer
(gold-plating) · implementing the cache (planning agents don't implement).

**Token tips.** Reads the guardrails file it owns, not every source file; ADR drafts are ≤ 1
page.
