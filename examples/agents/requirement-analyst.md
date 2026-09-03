# Example — Requirement Analyst

**Scenario.** A vague Jira issue: "Users complain checkout is slow sometimes. Make it better.
AC: checkout fast."

**Prompt.** [`prompts/jira-to-spec.md`](../prompts/jira-to-spec.md) (analyst stage).

**Context received.** The issue text verbatim + `sdd/sdd.yaml` + a keyword search over
existing specs. Not the codebase.

**Expected behavior.** Normalizes: FR candidate ("checkout latency reduced"), notes there is
NO number → `UNKNOWN: target latency`, `UNKNOWN: which step is slow`, `ASSUMPTION: p95 is the
relevant metric (industry default)` , `NEEDS_CONFIRMATION: is this the payment call?`.
Drafts AC candidates only where the source supports them. Flags that "sometimes" needs a
reproduction window.

**Expected output.** Requirement sections of the SPEC draft + a classified gap list; a 3-line
handoff ("solid: user-facing latency complaint · assumed: p95 · blocking: no target number").

**Common errors.** Inventing "checkout must respond in 2s" (gap→fact — the cardinal sin) ·
answering the performance question itself · writing the whole spec (that's spec-writer's job).

**Token tips.** Doesn't load code. A vague ticket produces a SHORT output + questions, not a
long compensating essay.
