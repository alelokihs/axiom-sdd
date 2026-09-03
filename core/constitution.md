# SDD Constitution

The highest-authority document of the methodology. Every spec, plan, task, implementation and
review must obey it. Project-specific exceptions require an entry in the decision log.

## Hierarchy of truth

When sources conflict, higher wins:

```
1. Law / regulation / official business requirements
2. This constitution (+ the project's amendments to it)
3. Project guardrails            -> sdd/guardrails.md
4. Approved decisions / ADRs     -> sdd/decisions/
5. Active SPEC                   -> sdd/specs/<NNN>-<slug>/SPEC.md
6. PLAN, then TASKS
7. Existing code
```

**Conflict rule:** if code and spec diverge, no agent decides silently which one is right.
The divergence is recorded (EVIDENCE.md or an Open Question) and surfaced. Existing code has
**no automatic priority** over an approved spec — and vice versa.

## Principles

1. **Spec first.** No implementation without a minimally approved specification. The path
   `request -> code` is forbidden. Proportionality applies: a one-line bugfix gets a one-page
   spec, not a waiver.
2. **Never invent.** Ambiguity becomes an Open Question, a gap becomes `UNKNOWN`, a guess becomes
   `ASSUMPTION` or `NEEDS_CONFIRMATION` — never a silent fact.
3. **Least privilege.** Every agent has explicit capabilities (capability matrix). Planning agents
   don't implement; execution agents don't redefine requirements; reviewers don't fix.
4. **Change budget is a contract.** Agents never expand their own budget
   (see [change-budget.md](./change-budget.md)).
5. **Evidence over declaration.** "Done" is a claim; an evidence pack is proof
   (see [evidence.md](./evidence.md)).
6. **Guardrails before implementation.** Agents read `sdd/guardrails.md` before writing code.
   Violating a guardrail requires a recorded decision, never an improvisation.
7. **Deterministic before generative.** If a step can be done reliably by a script or convention,
   don't spend model tokens on it.
8. **Token economy.** Context is a budget. Send agents targeted context packs, not repositories
   (see [context-engineering.md](./context-engineering.md)).
9. **Traceability.** Requirement -> AC -> task -> code -> test -> evidence -> commit must be
   walkable in both directions (see [traceability.md](./traceability.md)).
10. **Safety.** No secrets in prompts, code or logs. No destructive Git operations without explicit
    human authorization. No changes outside the workspace. No real personal data in specs/fixtures.
11. **Human accountability.** The framework produces analysis, code and evidence. Merge, release
    and requirement decisions belong to humans.
12. **Runtime independence.** Nothing in `core/`, `profiles/`, `workflows/` or `templates/` may
    reference a specific AI vendor. Vendor specifics live only in `adapters/`.

## Process rules

- SDD accelerates, it doesn't bureaucratize. A short document that unblocks execution beats a
  long one that delays it.
- Explicit `N/A` beats invented filler. Never fill a template field out of obligation.
- Stopping to register a blocking question is correct behavior. Inventing behavior is the failure.
- Scope creep ("while I'm here…") is a budget violation, not initiative.
