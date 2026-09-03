# Recipe — Performance improvement

Profile [`performance-improvement`](../../sdd/profiles/performance-improvement.yaml) · budget
bounded.

1. **Baseline first**, recorded with methodology (tool, load, environment) — no baseline, no
   spec approval.
2. Target is a number (`p95 < 800ms`), never an adjective.
3. Change; measure after with the SAME methodology; both numbers into evidence.
4. Regression tests prove behavior unchanged — performance work loves to change semantics.

**Watch for:** optimizing the unmeasured hot path (profile first) · benchmark-only-on-my-
machine evidence (label the environment) · caching that changes correctness (that's a
behavior change → back to spec).
