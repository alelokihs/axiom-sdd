# Recipe — Jira → Spec (standalone)

You just want a spec from a ticket — no implementation yet.

```
Generate SDD spec from this Jira issue.
Act per sdd/agents/requirement-analyst.agent.md, then sdd/agents/spec-writer.agent.md (write+validate).
<PASTE ISSUE VERBATIM>
```

Rules that make it trustworthy: gaps become `UNKNOWN` / `ASSUMPTION` / `NEEDS_CONFIRMATION`
(never facts) · blocking questions cap readiness at 59 · the verdict tells you whether the
ticket is implementable or needs its author.

A poorly-written issue is a **valid input with a low score** — the output is the shortest list
of questions that would raise it. Full worked example:
[../agents/jira-parser.md](../agents/jira-parser.md) · full flow:
[jira-to-feature.md](./jira-to-feature.md).
