# Recipe — Architecture change

Profile [`architecture-change`](../../sdd/profiles/architecture-change.yaml) · budget
architectural · workflow full · readiness 85.

1. ADR approved BEFORE implementation — the decision is the deliverable's first half.
2. Migration path for existing code defined (what moves now, what gets a shim, what waits).
3. Characterization + regression suites around affected contracts.
4. Guardrails updated as part of DoD — the new invariant is written where future agents read.
5. Evidence: before/after structure map.

**Watch for:** the "big rewrite" smell (split into incremental architecture-change specs) ·
old and new patterns coexisting with no recorded rule for which one new code uses.
