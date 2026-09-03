# Project Profiles

A profile is the packaged answer to "what kind of work is this?" — it selects workflow, agents,
change budget, gates, context requirements, DoR/DoD extras and expected evidence. Bootstrap
classifies the request and picks one; humans can override with `Profile: <name>`.

## Resolution

Every profile `extends: _defaults` ([_defaults.yaml](./_defaults.yaml)). A profile file lists
**only its deltas**; list fields marked `+` are additive, others replace. Consumers get one
resolved `sdd/profile.yaml` copied into the project — the resolution is done once, at bootstrap.

## Classification table (bootstrap uses this)

| Signals in the request | Profile |
|---|---|
| new capability, empty/new repo | [greenfield-feature](./greenfield-feature.yaml) |
| new capability, established repo | [legacy-feature](./legacy-feature.yaml) · or [backend-feature](./backend-feature.yaml) / [frontend-feature](./frontend-feature.yaml) / [fullstack-feature](./fullstack-feature.yaml) when clearly one-sided/both |
| restructure without behavior change | [legacy-refactor](./legacy-refactor.yaml) |
| defect, normal urgency | [bugfix](./bugfix.yaml) |
| defect, production-urgent | [hotfix](./hotfix.yaml) |
| production incident, remediation + prevention | [incident-remediation](./incident-remediation.yaml) |
| platform/framework/data move | [migration](./migration.yaml) |
| schema/query/storage change | [database-change](./database-change.yaml) |
| connect two systems | [integration](./integration.yaml) |
| endpoint/contract change | [api-change](./api-change.yaml) |
| vulnerability / security hardening | [security-fix](./security-fix.yaml) |
| latency/throughput/cost | [performance-improvement](./performance-improvement.yaml) |
| logging/metrics/tracing | [observability-change](./observability-change.yaml) |
| boundaries, layering, style of the system | [architecture-change](./architecture-change.yaml) |
| bump libraries/runtimes | [dependency-upgrade](./dependency-upgrade.yaml) |
| cleanup with small behavior latitude | [technical-debt](./technical-debt.yaml) |
| add tests only | [test-coverage](./test-coverage.yaml) |
| docs only | [documentation-change](./documentation-change.yaml) |

Ambiguous classification → present top 2 with one line each and ask (or, unattended, pick the
more conservative one — smaller budget — and mark `INFERRED`).

## Schema

```yaml
profile: <name>
summary: <one line>
extends: _defaults
workflow: full | standard | fast | hotfix
change_budget: minimal | bounded | moderate | architectural | unrestricted
implementer_specialization: <mode of implementer.agent.md>
test_modes: [unit, integration, contract, regression, e2e, characterization]
agents+: [...]          # added to defaults
gates+: [...]           # added to defaults
readiness_threshold: <60-100, never below 60>
context_requirements: [...]   # what the context pack must include
dor_extra: [...]
dod_extra: [...]
evidence_expected+: [...]
token_budget: S | M | L
```
