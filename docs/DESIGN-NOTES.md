# Design Notes — provenance from the challenge implementation

This framework was distilled from a real SDD implementation (the FinGuard challenge repo).
That repo was treated as architectural reference, not as a literal template. The silent
analysis, recorded:

## KEEP (concepts adopted nearly as-is)
- Constitution with an explicit **hierarchy of truth** and the conflict rule ("divergence is
  recorded, never silently resolved; code has no automatic priority over approved spec").
- Lifecycle with **gates** (SPEC→PLAN→TASKS→impl→tests→review→validation) and DoR/DoD as
  entry/exit checklists.
- Agent files with **Mandatory Reading / Forbidden Behavior** sections and a scope table.
- **Authorized-tasks-only** implementation ("no explicit task list = no authorization").
- Open Questions discipline; "N/A beats invented filler"; "SDD accelerates, not bureaucratizes".
- Traceability chain requirement→AC→task→test→report; IMPLEMENTATION-REPORT as closure.
- The **canonical file + thin runtime shortcut** pattern (challenge: `prompts/*.md` +
  `*.prompt.md` with locks) — generalized into the adapter contract.
- `example/` as a self-contained onboarding layer.

## GENERALIZE (challenge-specific → framework mechanism)
- `copilot-instructions.md` → runtime **adapters** (Claude/Copilot/Devin/Codex), core untouched.
- Fixed 14-agent cast → **12-agent catalog** with modes/specializations + capability matrix
  (the challenge's scope table, made machine-readable and least-privilege).
- Single feature lifecycle → **profiles × workflows** (21 × 4) with proportional ceremony.
- Challenge checklists (backend/frontend/ai/…) → **quality gates** + profile `dod_extra`.
- FinGuard constitution principles that were universal (spec-first, structured-over-freeform,
  cost awareness, security by design) → constitution; the domain-specific ones dropped.
- Live-Share/OneDrive gitflow → **detection-first gitflow** with hard safety list.
- IMPLEMENTATION-REPORT → **Evidence Model** (+ drift verdict, assumptions, debt).

## REMOVE (challenge coupling, deliberately not carried)
- All FinGuard domain content: complaint edge-case IDs (A1…F4), IARA/Bedrock providers,
  Keycloak, LangGraph, requirement IDs catalog, cost-per-complaint budgeting, presentation/
  figma-migration agents, Monday import, 4-hour-challenge adaptations, pt-BR-specific docs.

## ADD (not present in the challenge)
- One-prompt **bootstrap** with detection heuristics + CONFIRMED/INFERRED/UNKNOWN labels,
  fully autonomous (no human in the loop).
- **AGENTS.md generator** (contextual roster instead of static file).
- **Change budget**, **Spec Readiness Score**, **Spec Drift Detection** as named mechanisms.
- **Context packs / token economy** as first-class rules.
- **Model selection** per plane (fast/balanced/frontier) with adapter resolution tables.
- Install/ownership/versioning model (framework-owned vs project-owned; `install.py`).

## Decisions worth recording
- **English artifacts.** The challenge is pt-BR; the framework is English because it is
  consumed primarily by AI runtimes across orgs and stacks. Teams can localize consumer-side
  docs; machine-facing structure stays English.
- **12 agents, not 40.** The requested role list is fully covered (see catalog mapping table);
  merging kept rules single-sourced and cheap. Splitting later is additive.
- **No engine.** Workflows/profiles are YAML interpreted by the runtime — a deliberate
  anti-overengineering stance, kept machine-readable to allow a future CLI/MCP/orchestrator.
