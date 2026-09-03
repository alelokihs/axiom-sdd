# Architecture Guardrails — <project>

> The project's invariants. Agents read this BEFORE implementation; violating an entry requires
> an approved ADR, never improvisation. Owned by the architect role. Filled at bootstrap from
> detection (labels: CONFIRMED = observed, INFERRED = probable, NEEDS_CONFIRMATION = proposed
> default) — confirm or edit the non-CONFIRMED ones.

## Stack
Allowed languages/frameworks/build: … <label>
Forbidden: …

## Layering & boundaries
Modules and allowed dependency directions (e.g. `api -> application -> domain`;
`infrastructure -> domain`; domain imports no framework): … <label>

## Dependencies
Rules for adding libraries (decision entry required) · forbidden dependencies: …

## APIs & contracts
Style (REST/gRPC/events), versioning rule, error contract shape: … <label>

## Data & persistence
Databases in play, migration rules (ordered, reversible), sensitive data classes: …

## Security
Authn/authz mechanism · secret handling (never in code/logs/prompts) · input validation stance ·
what must never be logged: …

## Errors & logging
Error taxonomy · logging conventions · correlation/tracing rules: …

## Naming & conventions
The 3–7 conventions that actually matter here (the linter handles the rest): …

## Testing
Frameworks, layout, what every change must carry: … <label>

## Observability
Baseline instrumentation expected for new behavior: …
