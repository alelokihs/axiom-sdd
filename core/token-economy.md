# Token Economy

> Small prompt, rich repository context, targeted context pack.
> Never: giant prompt containing the entire methodology.

## Rules

1. **Reference, don't repeat.** Permanent rules live in one file each; prompts point to paths.
   Ask of every line: *does this need to be in the prompt, or can it be referenced?*
2. **Progressive disclosure.** Layered docs; agents load deeper layers only on demand.
3. **Minimal context packs.** See [context-engineering.md](./context-engineering.md).
4. **Short execution prompts.** The ready prompts are ≤ 10 lines; behavior lives in the repo.
5. **Generated, contextual `AGENTS.md`.** Only the agents this project uses, each entry a few
   lines + a path — never the whole catalog inline.
6. **One source per rule.** Guardrails are not restated in every agent file; agent files link.
7. **Diffs over files.** Review and drift work on diffs and signatures, not full sources.
8. **Deterministic before generative.** File copying, detection greps, link checks, scaffold
   creation → scripts/conventions, not model calls.
9. **Summaries with pointers.** When an agent hands off, it writes 5 lines + paths, not a recap.
10. **Load-on-need.** Templates are instantiated when reached in the lifecycle, not upfront.

## Budget accounting (lightweight)

Each profile carries an indicative `token_budget` (S/M/L) driving workflow choice. The evidence
pack notes when an execution blew far past expectation — that's a process smell to fix in
discovery, not a reason to trim safety gates.

## Known duplication (deliberate)

The only tolerated duplication: 3–5 line "locks" inside runtime shortcut files (see
adapters) restating the non-negotiables. Rationale: shortcuts may run without the canonical
file loaded. Everything else: single source.
