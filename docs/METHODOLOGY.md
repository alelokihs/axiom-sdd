# Methodology

## The problem this solves
AI-assisted development fails in repeatable ways: assistants go request→code and guess the gaps;
two sessions implement two interpretations; "done" is declared, not proven; context windows get
stuffed with whole repositories; and every process is welded to one vendor's file format.

## The operating model
Four moves, each mechanical enough for any competent runtime:

1. **Specify before building.** Interpretation happens once, in writing, gated by a readiness
   score — not N times, silently, in each session ([lifecycle](../core/lifecycle.md),
   [readiness](../core/spec-readiness.md)).
2. **Constrain the executor.** Roles with least-privilege capabilities
   ([matrix](../agents/capability-matrix.yaml)), an authorized-tasks-only rule, and a
   [change budget](../core/change-budget.md) that the executor cannot raise.
3. **Prove, then close.** [Evidence](../core/evidence.md) replaces claims;
   [drift detection](../core/spec-drift.md) reconciles spec ↔ code ↔ tests;
   [traceability](../core/traceability.md) makes "why does this exist" greppable.
4. **Feed context surgically.** [Context packs](../core/context-engineering.md) and the
   [token economy rules](../core/token-economy.md) keep prompts small and repositories rich.

## The vendor-independence principle
> The project knows SDD. SDD does not know Claude, Copilot, Devin or Codex.

Everything above lives in runtime-neutral markdown/YAML in the project. Vendors get thin
[adapters](../adapters/README.md): pointer files + six restated locks. Switching or mixing
runtimes changes adapter files only.

## Proportionality
The pipeline is logical, not ceremonial: [profiles](../profiles/README.md) pick a
[workflow](../workflows/README.md) that collapses steps for small work. A hotfix is one compact
document — but it still has ACs, evidence and a drift check. The floor never drops to zero;
it drops to *cheap*.

## What deliberately doesn't exist (v1)
No CLI, no orchestrator service, no policy engine, no database, no Jira/CI integration —
conventions, markdown, YAML and one small installer script do the job. The structure leaves
room for those later (declarative workflows and profiles are machine-readable on purpose)
without paying for them now.
