# Example — Jira → Spec (requirement-analyst + spec-writer chain)

**Scenario.** Fastest path: developer pastes a Jira issue, wants a scored spec.

**Prompt.** [`prompts/jira-to-spec.md`](../prompts/jira-to-spec.md) with the raw issue.

**Context received.** The issue text only (+ project manifest facts). The chain runs analyst →
writer → validator in one pass.

**Expected behavior.** Analyst normalizes and classifies gaps; writer instantiates the profile's
spec form; validator scores. A well-written issue → READY directly; a poor one → the example in
[requirement-analyst.md](./requirement-analyst.md) (low score + precise questions). Either way
the developer gets a NEXT ACTION, not an essay.

**Expected output.** `sdd/specs/<NNN>-<slug>/SPEC.md` + score + verdict + (if < 80) the
shortest list of questions that would raise it.

**Common errors.** Filling business context from imagination when the issue lacks it ·
readiness theater (score 85 with three untouched UNKNOWNs — the cap rule catches this).

**Token tips.** The issue is quoted once in SPEC §1; later steps reference the spec, never
re-paste the ticket.
