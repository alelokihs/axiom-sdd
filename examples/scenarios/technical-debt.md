# Recipe — Technical debt

Profile [`technical-debt`](../../sdd/profiles/technical-debt.yaml) · budget moderate.

1. The debt entry being paid is identified — from evidence-pack debt lists or the backlog.
   Debt without an entry gets an entry first (that's free); work without a spec doesn't start.
2. Any allowed behavior change is listed EXPLICITLY (default: none — then it's a refactor with
   latitude on structure only).
3. Characterization tests where coverage is thin; then the cleanup.
4. DoD extra: the debt entry is closed/updated, and no NEW unrecorded debt appears.

**Watch for:** debt work expanding to "everything annoying nearby" · deleting safety nets
(tests, feature flags) as "debt" — those need their own justification.
