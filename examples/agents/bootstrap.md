# Example — Bootstrap Agent

**Scenario.** Legacy Java Spring Boot monolith; developer has a Jira issue for a new export
endpoint; runtime is Copilot.

**Input / prompt.**
```
Initialize SDD.
Framework: ../sdd-framework
Runtime: Copilot
Source:
[PAY-2311] Export statement as CSV. As an account manager I want ... (full Jira text)
```

**Context received.** The repository itself (detection is read-only and cheap-first) + the
template. Nothing else needed.

**Expected behavior.** Detects `java 17 (CONFIRMED: pom.xml)`, `spring-boot 3.2 (CONFIRMED)`,
`maven wrapper (CONFIRMED)`, `JUnit5 (CONFIRMED)`, layering `INFERRED: controller/service/
repository`, GitFlow `INFERRED: develop branch + feature/* history`. Classifies → profile
`legacy-feature` (or `api-change`; picks `api-change`? endpoint-shaped → reports the tie,
picks smaller budget). Selects models (planning=frontier: ambiguity in Jira; execution=balanced;
support=fast). Installs core, generates `.github/copilot-instructions.md`, prompt files,
AGENTS.md (repo root), spec 001 draft, context pack.

**Expected output.** The `SDD INITIALIZED` block, `Readiness: 72 — REVIEW_REQUIRED`,
`NEXT ACTION: SDD: refine spec 001` (answering the 3 NEEDS_CONFIRMATION items).

**Common errors.** Asking the user things `pom.xml` answers · copying `examples/` into the
project · writing app code ("while I'm here I created the controller") — forbidden.

**Token tips.** Detection reads manifests, not sources. The report is ~30 lines, not a
repository tour.
