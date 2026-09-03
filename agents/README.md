# Agent Catalog

12 agents cover the whole lifecycle. Roles were **deliberately consolidated**: an agent is worth
its file only when it has distinct capabilities, distinct forbidden behavior, or a distinct place
in the pipeline. Specializations are *modes* selected by the profile, not separate agents — fewer
files, fewer duplicated rules, fewer tokens.

## The catalog

| Agent | Covers (requested roles) | Plane |
|---|---|---|
| [bootstrap](./bootstrap.agent.md) | Bootstrap Agent | meta |
| [requirement-analyst](./requirement-analyst.agent.md) | Requirement Analyst, Jira Requirement Parser | planning |
| [spec-writer](./spec-writer.agent.md) | Spec Writer, Spec Validator (readiness scoring) | planning |
| [architect](./architect.agent.md) | Solution Architect, Software Architect, Architecture Reviewer, ADR Agent (approval) | planning |
| [codebase-analyst](./codebase-analyst.agent.md) | Legacy Analyst, Codebase Explorer, Context Discovery, Context Pack Builder | planning |
| [implementer](./implementer.agent.md) | Feature/Backend/Frontend/API/Integration/Refactoring/Bugfix/Migration/Database/Event-Driven/Performance/Observability Implementation Agents — via `specialization` | execution |
| [test-engineer](./test-engineer.agent.md) | Test Engineer, Unit/Integration/Contract/Regression/E2E Test Agents — via `mode` | execution |
| [reviewer](./reviewer.agent.md) | Code Reviewer, Spec Compliance Reviewer, Spec Drift Detector, architecture check execution | verification |
| [security](./security.agent.md) | Security Agent, Security Reviewer | verification |
| [docs](./docs.agent.md) | Documentation Agent, ADR Agent (writing), Evidence curation | support |
| [gitflow](./gitflow.agent.md) | Gitflow Agent, Release Agent | support |
| — evidence | Evidence Collector is **not an agent**: every executing agent writes its own evidence ([core/evidence.md](../core/evidence.md)); reviewer and gitflow verify it | — |

## Planes and the prime separation

> **Planning agents don't implement. Execution agents don't redefine requirements.
> Verification agents don't fix.**

```
planning:      requirement-analyst → spec-writer → architect → codebase-analyst
execution:     implementer → test-engineer
verification:  reviewer · security
support:       docs · gitflow
meta:          bootstrap
```

## Capability matrix

Machine-readable, least-privilege: [capability-matrix.yaml](./capability-matrix.yaml).
An agent file never grants more than the matrix; on conflict the matrix wins.

## Agent file contract

Every `*.agent.md` has the same sections — runtimes rely on this:

```
Role · Modes (if any) · Mandatory Reading · Inputs · Procedure · Forbidden · Deliverables · Handoff
```

Global rules for all agents live once, in the [constitution](../core/constitution.md) — agent
files reference it and never restate it.
