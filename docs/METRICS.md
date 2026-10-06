# Local progress report

Run `python3 cli/axiom.py metrics --target /path/to/project --stale-hours 24`.
The report is JSON. Exit0 means a report was produced (including unavailable or task findings),
not that acceptance passed. Exit2 means malformed input or invalid options.

Create optional `sdd/progress.json` with this structure (replace the placeholder hash with the
SHA256 of a real saved test output; timestamps must include a timezone):

```json
{"version":1,"tasks":[{"id":"TASK-001","owner":"backend","next_action":"Run browser acceptance",
"blocker":"Test account unavailable","required_mode":"real","observations":[
{"at":"2026-10-01T12:00:00Z","path":"work/tests.txt","sha256":"REPLACE_WITH_64_HEX_DIGITS",
"mode":"simulated","passed":8,"failed":0,"skipped":0}]}]}
```

All fields shown are required. Blocker may be null. Modes: `simulated` or `real`. Observations
must be chronological, with nonnegative integer counts. Use immutable evidence paths. Missing
progress data yields `unavailable`; invalid/dangling/symlink/outside evidence yields
`invalid_evidence`. No observations yields `no_evidence`; failed/skipped/zero-pass checks yield
`incomplete_checks`; simulated evidence for real acceptance yields `real_evidence_required`.
Matching declared passing checks yields `declared_checks_supported`, never release approval.

Duplicate evidence fingerprint (digest, mode and counts) retains its first observation date.
The report trusts declared mode/counts; reviewers must verify them against logs and acceptance.
A hash proves file correspondence, not who ran it, whether execution occurred, or feature quality.
The command never reads channel prose or prints evidence bytes, owners, next actions or blockers.
Secure no-follow file access currently requires POSIX APIs (macOS/Linux); unsupported platforms
fail closed with an invalid report rather than weakening file containment. Install/update remain
cross-platform. Limits:1MiB manifest,16MiB evidence file,256 tasks,4096 total observations.
