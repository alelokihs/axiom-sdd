# Definition of Ready (DoR)

Entry gate for implementation. A task starts only when every item holds; otherwise the task is
`BLOCKED` and the result is `SPEC_NOT_READY` — not "let's figure it out as we go".

## Checklist

### Clarity
- [ ] What must change — one sentence
- [ ] Why it must change — traceable to the source requirement
- [ ] Scope delimited: what is explicitly OUT is written down
- [ ] Task small enough to implement in isolation

### Behavior
- [ ] Acceptance criteria defined and verifiable (Given/When/Then or equivalent)
- [ ] Error behavior defined
- [ ] Relevant edge cases identified

### Technical
- [ ] Input/output contracts known
- [ ] Affected components identified (blast radius for legacy work)
- [ ] Dependencies identified and unblocked
- [ ] Relevant architecture/guardrails read; conflicts resolved or logged

### Risk & constraints
- [ ] Main risks listed
- [ ] Change budget assigned and understood
- [ ] Expected tests declared

### Blockers
- [ ] No blocking Open Question
- [ ] No pending architectural decision

## Proportionality

`fast`/`hotfix` workflows check the same items but accept them in compressed form (a single short
spec section can satisfy several boxes). What can never be compressed away: acceptance criteria,
scope boundary, error behavior.

> A blocking question left open *prevents* the start. Starting anyway moves the ambiguity into the
> code, where it becomes invisible.
