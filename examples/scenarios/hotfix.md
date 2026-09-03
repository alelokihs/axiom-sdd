# Recipe — Hotfix

Profile [`hotfix`](../../sdd/profiles/hotfix.yaml) · budget minimal · workflow **hotfix**
(single doc) · readiness floor 60.

1. One HOTFIX-DOC: failure, impact, root cause (provisional ok), minimal fix, evidence inline.
2. Regression test pins the failure mode — even under time pressure (it's 10 minutes that
   prevents the re-occurrence at 3am).
3. Drift-lite review → gitflow (project's hotfix branch convention).
4. **Follow-up is mandatory** (`followup_required: true`): deferred cleanup/root-cause work
   becomes the next spec, referenced in evidence.

**Watch for:** the follow-up quietly never happening — the gitflow gate checks the reference.
