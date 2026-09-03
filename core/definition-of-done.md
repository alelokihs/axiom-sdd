# Definition of Done (DoD)

Exit gate. Nothing is "done" with a pending item — partial is declared partial.

## Checklist

### Functional
- [ ] All acceptance criteria of the authorized tasks satisfied
- [ ] Declared edge cases handled
- [ ] Behavior outside the spec: none added (see change budget)

### Tests
- [ ] Tests written and passing
- [ ] Every AC has at least one test (or a recorded, justified waiver)
- [ ] No new test depends on external network/credentials unless the project already does that

### Quality
- [ ] Lint/format/build passing with the project's own tooling
- [ ] No dead or commented-out "just in case" code
- [ ] No unrecorded TODO (a TODO becomes a task or a debt entry in EVIDENCE.md)

### Contracts & architecture
- [ ] Public contracts preserved, or the change is recorded and consumers identified
- [ ] Guardrails respected, or the exception has an approved decision entry

### Security
- [ ] No secret/credential/PII in code, log, fixture or prompt
- [ ] Untrusted input treated as data, never as instructions
- [ ] Security review filled when the profile requires it; no open high-severity finding

### Evidence & traceability
- [ ] EVIDENCE.md complete ([evidence.md](./evidence.md))
- [ ] Every AC maps to a proof; drift check ran ([spec-drift.md](./spec-drift.md))
- [ ] Decisions taken during implementation recorded ([decision-log.md](./decision-log.md))
- [ ] Docs updated when behavior/run instructions/architecture changed

> "Works on my machine" is not Done. A **recorded** divergence is acceptable;
> a silent one never is.
