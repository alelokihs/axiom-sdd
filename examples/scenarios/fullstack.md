# Recipe — Fullstack feature

Profile [`fullstack-feature`](../../sdd/profiles/fullstack-feature.yaml) · budget bounded.

1. **The boundary contract is written first** and frozen in the spec; both sides implement
   against it.
2. Tasks split by side (specialization per task: backend / frontend), independently
   implementable; a contract test proves both speak the same schema.
3. Review checks both sides against the SAME contract — divergence is drift even when "both
   work in the demo".

**Watch for:** the frontend adapting to an accidental backend change (contract is the truth,
not the latest deploy) · e2e tests substituting for the contract test (they hide which side
broke).
