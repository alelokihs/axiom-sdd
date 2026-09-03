# Recipe — Backend feature

Profile [`backend-feature`](../../sdd/profiles/backend-feature.yaml) · budget bounded.

1. Contracts sketched in SPEC §5 BEFORE implementation (contract-first).
2. Guardrails give layering (e.g. `api -> application -> domain`); the pack includes the error
   taxonomy.
3. Implement; integration-mode tests cover the boundary, unit the domain logic.
4. DoD extra: error mapping consistent with the project taxonomy (no naked 500s).

**Watch for:** business logic drifting into the API layer · schema "temporarily" duplicated
instead of shared · new endpoint not in the spec (drift: unspecified-behavior).
