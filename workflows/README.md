# Workflow Definitions

A workflow is a declarative sequence of agent steps and gates. Profiles reference exactly one.
Workflows are interpreted by the AI runtime (via its adapter) — there is no engine. The YAML is
the shared, runtime-neutral description of what runs, in what order, gated by what.

| Workflow | For | Steps | Ceremony |
|---|---|---|---|
| [`full.yaml`](./full.yaml) | architectural / high-risk work | all, nothing collapses | max |
| [`standard.yaml`](./standard.yaml) | normal features | full pipeline, single review pass | normal |
| [`fast.yaml`](./fast.yaml) | small bounded changes | SPEC absorbs PLAN+TASKS; one impl pass | low |
| [`hotfix.yaml`](./hotfix.yaml) | urgent minimal fixes | one compact doc; drift-lite; mandatory follow-up | min |

## Schema

```yaml
workflow: <name>
description: <one line>
spec_form: full | compact | single-doc     # which template variant spec-writer uses
steps:
  - agent: <catalog name>
    mode: <agent mode, optional>
    gate: <gate that must pass before the next step, optional>
    optional: <condition when the step runs, optional>
followup_required: true|false              # hotfix-style workflows must schedule real cleanup
```

Rules: steps run in order; a failing gate triggers the
[gate-failure protocol](../core/gates.md); `optional` steps run when their condition holds
(profile trigger or explicit request). Never removable, whatever the workflow: acceptance
criteria, security question in spec, evidence, drift check.
