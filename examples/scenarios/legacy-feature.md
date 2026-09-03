# Recipe — Feature in a legacy codebase

Profile [`legacy-feature`](../../sdd/profiles/legacy-feature.yaml) · budget **bounded** · workflow standard.

1. `Initialize SDD.` + Source (or `SDD: new spec` if already bootstrapped).
2. Legacy analysis runs before readiness: blast radius + existing contracts attach to the spec.
3. Spec READY ≥ 80; scope OUT lists neighboring behavior explicitly.
4. Implement authorized tasks; regression mode tests protect the neighbors.
5. Review + drift; evidence includes blast-radius-check.

**Watch for:** budget creep into "cleanup" (route to technical-debt) · INFERRED couplings
treated as facts · tests passing while neighboring behavior silently changed (regression suite
must cover the HIGH blast-radius rows).
