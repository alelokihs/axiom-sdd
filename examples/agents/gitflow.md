# Example — Gitflow Agent

**Scenario.** Spec 003 complete, evidence green. Project convention (detected):
GitFlow, `feature/*`, Conventional Commits, merge --no-ff by humans.

**Prompt.** [`prompts/finish-gitflow.md`](../prompts/finish-gitflow.md).

**Context received.** `sdd/sdd.yaml` gitflow block, EVIDENCE.md, `git status`/diff stat.

**Expected behavior.** Verifies branch `feature/003-csv-export` · staged audit finds
`debug.log` and an unrelated formatting change → unstages, reports · runs lint+tests ·
commit: `feat(export): add CSV statement export` + body from evidence + `SDD: 003 TASK-001
TASK-002` · prepares PR text (summary, AC table, risks) · reports status; push awaits human ok.

**Expected output.** Audited commit + PR body + exact status report.

**Common errors.** Force-pushing to fix a mistake (hard-forbidden; report instead) ·
committing with a red gate "to save progress" · inventing a convention when detection said
UNKNOWN (propose + NEEDS_CONFIRMATION instead).

**Token tips.** Works from diff stat + evidence; never re-reads source contents.
