# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `SPEC_NOT_READY` and you disagree | Readiness < threshold or blocking Open Question | Read the 10 one-liners in SPEC §Readiness — answer the questions or lower ambiguity; never edit the score |
| Agent implemented something extra | Change budget violated or tasks not explicit | Reviewer flags it as `out-of-scope-change`; revert or absorb via explicit spec update. Check the authorization prompt listed tasks |
| Agent "fixed" a spec↔code divergence silently | Constitution conflict-rule violation | Restore, record the divergence in EVIDENCE.md, route the decision to a human. Re-read locks in your runtime entry file |
| Runtime ignores the methodology | Adapter entry file missing/stale | Regenerate adapter files (bootstrap phase 4); confirm the runtime actually loads its native file |
| Context pack keeps growing | Spec too big or lazy discovery | >~20 files ⇒ split the spec; rebuild the pack from spec nouns, use `(signature only)` |
| Detection got the stack wrong | INFERRED taken as fact | Fix `sdd/sdd.yaml` value, set `CONFIRMED`; bootstrap never blocks on this |
| Bootstrap wants to overwrite my files | You customized framework-owned files | Move customizations to project-owned files (guardrails, constitution amendments); see [ownership model](../bootstrap/INSTALL.md) |
| Wrong model doing heavy planning | Tier mis-selected | Edit `models:` in `sdd/sdd.yaml`; agents may self-escalate one tier (recorded in evidence), never de-escalate |
| Tests can't run in this environment | Sandbox/network limits | Record `NOT_RUN: <reason>` in evidence; CI re-runs. Never fake results |
| Hotfix left a mess | Follow-up skipped | `hotfix` workflow has `followup_required: true` — create the follow-up spec; gitflow gate should have flagged it |
| Two profiles both fit | Genuine ambiguity | Bootstrap self-resolves (smaller budget, INFERRED) and reports the runner-up; override with `Profile:` next time |
| Framework update changed behavior | Version bump | Read the template CHANGELOG; project-owned files were untouched; re-run generators |
