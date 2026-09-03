# Context Engineering

The framework's most important economic rule: **agents get targeted context packs, never
repositories.**

```
Context Discovery  →  Relevant Files Detection  →  Context Pack  →  Agent Execution
```

## Context pack

A context pack (template: [templates/CONTEXT-PACK.md](../templates/CONTEXT-PACK.md)) is a short
manifest — *paths and reasons, not contents* — listing exactly what an agent should load:

- the active SPEC (and only the sections its step needs);
- the applicable global rules (constitution amendments, guardrails — by reference);
- relevant source files (the ones the change touches + their direct contracts);
- related interfaces/types the change must respect;
- related tests;
- relevant decisions/ADRs (by ID);
- relevant conventions (linter config, naming doc section).

The pack is built once per spec by the codebase-analyst (discovery mode) and updated when scope
changes. Executing agents open the pack, load what's listed, and nothing else.

## Discovery heuristics

1. Start from spec nouns: entities, endpoints, components named in the SPEC.
2. Search by symbol, route, table, config key — not by reading directories top-down.
3. Follow one level of imports/references from each hit (contracts), then stop.
4. Include the *tests* of every file included.
5. Prefer interfaces/signatures over full implementations when only the contract matters —
   note `(signature only)` in the pack.
6. Cap: a pack that lists more than ~20 files is a smell — either the task is too big
   (split the spec) or discovery was lazy (tighten it).

## Per-step trimming

| Step | Needs | Does NOT need |
|---|---|---|
| spec writing | requirement, guardrails summary, similar existing spec | source code (except contract sketches) |
| planning | SPEC, architecture notes, pack file list | file contents beyond signatures |
| implementation | SPEC ACs + its task, listed files, conventions | other specs, full docs tree |
| testing | ACs, changed files, existing test patterns | PLAN internals |
| review/drift | SPEC, TASKS, **diff**, test results, guardrails | unchanged files |
| gitflow | EVIDENCE.md, diff stat, git conventions | source contents |

See [token-economy.md](./token-economy.md) for the global rules.
