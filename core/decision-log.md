# Decision Log

Non-trivial decisions leave a trace. Trivial ones don't get bureaucracy.

## Two formats

**Decision entry (default)** — 5 lines in `sdd/decisions/LOG.md`
(template: [templates/DECISION.md](../templates/DECISION.md)):

```
## D-014 — Use library X for retries (2026-08-27)
Context: task 003 needs retry with backoff; project has no util for it
Reason: X already transitively present; hand-rolling = more surface
Alternatives: hand-rolled loop (rejected: reinvention), library Y (rejected: new dep)
Consequences: X becomes a direct dependency
```

**Full ADR** — file `sdd/decisions/ADR-NNN-slug.md`
(template: [templates/ADR.md](../templates/ADR.md)) — only when the decision is architectural,
durable, or overrides a guardrail.

## When to write what

| Situation | Format |
|---|---|
| Picked between two reasonable implementations | Decision entry |
| New direct dependency | Decision entry |
| New module/boundary, changed layering, changed contract style | ADR |
| Guardrail exception | ADR (and link it from the guardrail) |
| Obvious/idiomatic choice with no real alternative | Nothing — noise |

## Who writes

Any agent that decides. The docs agent curates format; the architect approves ADRs.
Agents never *retroactively edit* past decisions — superseding gets a new entry that references
the old one.
