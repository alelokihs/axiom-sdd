# Recipe — Frontend feature

Profile [`frontend-feature`](../../sdd/profiles/frontend-feature.yaml) · budget bounded.

1. Spec pins: the API contract consumed (version/schema), and all four states —
   loading / empty / error / success — as ACs.
2. Context pack: design reference, component conventions, the API types.
3. Implement following existing component patterns; e2e mode covers the happy path,
   unit covers state logic.
4. DoD extra: accessibility basics (labels, focus order, contrast per project standard).

**Watch for:** inventing API fields the backend doesn't return (pin the contract first) ·
design drift ("close enough" to the reference is an Open Question, not a call you make).
