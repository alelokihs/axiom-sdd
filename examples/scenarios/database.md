# Recipe — Database change

Profile [`database-change`](../../sdd/profiles/database-change.yaml) · budget bounded ·
readiness 85.

1. Spec lists consumers of the changed schema, and classifies: additive / narrowing /
   destructive.
2. Migration ordered and **reversible** — or irreversibility declared and human-accepted.
3. Forward AND rollback both run locally; outputs in evidence.
4. Data integrity checks (counts, constraints) recorded.

**Watch for:** destructive steps hidden in "cleanup" migrations · code deployed before/after
window (sequencing section is mandatory) · rollback that was never actually executed once.
