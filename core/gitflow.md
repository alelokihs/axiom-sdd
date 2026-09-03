# Git Integration

The gitflow agent adapts to the project — it never imposes a branching religion.

## Detection first

Bootstrap detects (labels: CONFIRMED / INFERRED / UNKNOWN):

- branch model: `main`-only, GitHub Flow, GitFlow (`develop` present), trunk-based, custom;
- naming pattern from recent branches (`feature/*`, `feat/*`, `JIRA-123-*`, …);
- commit convention from `git log` (Conventional Commits? ticket prefixes? free-form);
- merge policy hints (merge commits vs squash vs rebase in history);
- hooks/CI expectations (`.pre-commit-config`, `husky`, CI config files).

Detected convention is recorded in `sdd/sdd.yaml` (`gitflow:` block). If `UNKNOWN`, the bootstrap
proposes a default (GitHub Flow, Conventional Commits, branch `sdd/<NNN>-<slug>`) and marks it
`NEEDS_CONFIRMATION`.

## The gitflow agent does

- create/validate the work branch: `<detected-prefix>/<NNN>-<slug>`;
- pre-commit validation: lint/tests per project, diff review vs change budget, staged-files
  audit (nothing out of scope, no secrets, no junk files);
- write the commit message from EVIDENCE.md: convention + `SDD: <NNN> TASK-…` trailer;
- prepare push/PR description from the evidence pack;
- report status precisely (branch, ahead/behind, dirty files).

## Never (hard safety rules)

- `push --force` in any form on shared branches
- merge to protected/long-lived branches without explicit human authorization
- history rewrites (`rebase` of shared branches, `filter-branch`, forced tag moves)
- deleting branches/stashes/files outside the workspace
- committing secrets, `.env` values, credentials, or generated junk

When one of these seems necessary, the agent stops and asks, presenting the exact commands for a
human to run.
