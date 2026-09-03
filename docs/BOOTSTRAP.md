# SDD Bootstrap

One prompt initializes everything. This file is the **program the AI runtime executes** when it
receives the start prompt. Deterministic parts are delegated to [`install.py`](./install.py)
when a Python 3 interpreter is available (any OS); otherwise the manual copy list below applies.

## Start prompt (canonical)

```
Initialize SDD.
Framework: <path-or-url-to-this-template>
Source:
<Jira issue text or free description>
```
Optional: `Context:` · `Runtime: Claude|Copilot|Devin|Codex` · `Mode: existing|new` ·
`Profile: <name>`.

Minimal viable prompt: `Initialize SDD.` + `Source:` — everything else is detected or defaulted.

## Phases

### 0 — Resolve inputs
Runtime defaults to the one executing this. Mode defaults: repo has source files → `existing`;
empty/new → `new`. The bootstrap runs **without a human in the loop**: it decides, labels, and
reports — the only question it may ever ask is a missing `Source` in `new` mode (the one
unrecoverable input).

### 1 — Detect  *(existing mode; `new` mode detects only intent + declared stack)*
Run the detection pass per [detection.md](./detection.md). Every finding gets a confidence
label: `CONFIRMED` (observed), `INFERRED` (probable, evidence cited), `UNKNOWN`.
**Never ask what a file can answer; never invent what no file answers.**

### 2 — Classify & select profile
Match the Source against the [classification table](../profiles/README.md). Output: profile
(with workflow, budget, agents, gates resolved from `_defaults` + deltas). Genuine tie →
**no human in the loop**: pick the smaller-budget candidate, mark it `INFERRED`, and list the
runner-up in the final report.

### 2.5 — Select models
Apply [model-selection.md](./model-selection.md): propose the best LLM tier per plane
(planning / execution / verification / support) from the profile + spec signals, resolve tiers
to concrete models via the runtime's adapter table, and embed the result in `sdd/sdd.yaml`
(`models:` block) and in the generated `AGENTS.md`. Autonomous — humans override by editing the
file, not by being asked.

### 3 — Install the minimal core
Run `python3 install.py --target <project> --profile <p> --runtimes <r,…>` (works on Windows,
macOS, Linux), or copy manually per [INSTALL.md](./INSTALL.md). Installs ONLY:
core (14 files) · resolved `profile.yaml` · referenced workflow · the profile's agents +
capability matrix · templates · empty `specs/` + `decisions/`. **Never `examples/`, never other
profiles/adapters.** Nothing existing is overwritten without being listed first.

### 4 — Generate project artifacts
1. `sdd/sdd.yaml` from [templates/project-sdd.yaml](../templates/project-sdd.yaml) + detection.
2. `sdd/guardrails.md` from [templates/GUARDRAILS.md](../templates/GUARDRAILS.md) + detection
   (labels preserved; proposed defaults marked `NEEDS_CONFIRMATION`).
3. `AGENTS.md` per [agents-md-generator.md](./agents-md-generator.md).
4. Runtime adapter files per [adapters/](../adapters/README.md) for each runtime in the list.
5. Spec `001-<slug>` draft: act as requirement-analyst on the Source (normalize, classify gaps),
   instantiate the profile's spec form, fill what's known.
6. `CONTEXT-PACK.md` draft: act as codebase-analyst (discovery from spec nouns).
7. Gitflow block: detect per [core/gitflow.md](../core/gitflow.md); UNKNOWN → propose default
   + `NEEDS_CONFIRMATION`.
8. If the project has a `.gitignore` and scratch dirs are used (`sdd/_tmp/`), append them.

### 5 — Score & report
Run spec-writer validate mode on the draft. Then print exactly:

```
SDD INITIALIZED
Project:         <name> (<mode>)
Runtime:         <runtimes>
Detected stack:  <lang/framework/build — with confidence labels>
Profile:         <profile>  (workflow: <w>)
Change budget:   <level>
Agents:          <roster>
Quality gates:   <gates>
Spec:            sdd/specs/001-<slug>/  (status: DRAFT)
Context pack:    <n> files listed
Gitflow:         <style · branch pattern · convention — labels>
Models:          planning=<tier:model> · execution=<tier:model> · verification=<tier:model> · support=<tier:model>
Readiness:       <score> — <verdict>
NEEDS_CONFIRMATION: <the list, or "none">

NEXT ACTION:
<exactly one command/prompt — e.g. "SDD: refine spec 001" or, if READY, "SDD: implement 001 TASK-001">
```

## New Project mode differences
Phase 1 detects intent only (declared stack in Source/Context). Phase 4 runs the architect in
`design` mode first: minimal structure, initial guardrails (all `NEEDS_CONFIRMATION`), founding
ADR(s). Anti-overengineering rule applies: scaffold only what the first spec needs.

## Re-running bootstrap
Safe. Framework-owned files are regenerated; files under `customized:` in `sdd/sdd.yaml` are
never touched (see [INSTALL.md](./INSTALL.md)). Existing specs are never modified.
