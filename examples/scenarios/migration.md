# Recipe — Migration (platform/framework/data)

Profile [`migration`](../../sdd/profiles/migration.yaml) · budget architectural · workflow
full · readiness 85.

1. Strategy decision first (big-bang vs incremental) → ADR.
2. Compatibility matrix in the spec: what must keep working, for whom, until when.
3. Characterization tests pin behavior on the OLD side before anything moves.
4. Sequencing + rollback path per step; security review included (surface changes).
5. Evidence: rollback-verification + compatibility-matrix results.

**Watch for:** "we'll write the rollback later" · incremental migrations that stall at 60%
(each step must leave the system consistent) · silent behavior "improvements" during the move.
