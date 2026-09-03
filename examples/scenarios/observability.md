# Recipe — Observability change

Profile [`observability-change`](../../sdd/profiles/observability-change.yaml) · budget
bounded · workflow fast.

1. The spec states the QUESTION this instrumentation answers ("which step of checkout fails
   most?") — instrumentation without a question is noise with a storage bill.
2. Follow guardrail conventions (log shape, correlation IDs, metric naming).
3. DoD extra: **no secret/PII/sensitive payload** in any new log, label or trace attribute.
4. Evidence: a sample of the new signal, redacted.

**Watch for:** logging whole request bodies "temporarily" · cardinality bombs in labels ·
alert rules without an owner.
