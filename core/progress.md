# Evidence-aware progress

Each active task records an owner, next executable action, blocker and required verification mode.
Coordination messages are activity, not delivery. A newer heartbeat must not refresh the date of
unchanged proof. Escalate a stale blocker with its owner and concrete resolution; keep independent
already-authorized work moving. Do not automatically reassign files or expand permissions.

Optional local `sdd/progress.json` schema version1 is consumed by `axiom metrics --target PROJECT`.
It checks file digests against declared observations; it does not parse test logs, certify execution,
prove runtime deployment, rank agents or measure tokens. Owners still map every AC in EVIDENCE.md.
A green simulated suite does not meet a real-provider/browser requirement. Skips remain unproven.
Keep observations backed by immutable local output files; replacing historical files invalidates
history. Never put secrets or personal data in declarations. Output omits free-text declarations
and evidence contents. No network calls, telemetry or writes are performed by the metrics command.

Stale means the latest evidence fingerprint was first observed at least the configured number of
hours ago (default24). It is a routing hint, not a deadline or evidence of poor performance.
`declared_checks_supported` means only that metadata is valid and the current file matches its hash.
