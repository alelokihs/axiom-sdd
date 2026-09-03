# Recipe — Integration between services

Profile [`integration`](../../sdd/profiles/integration.yaml) · budget bounded · security in
roster.

1. Pin the external contract in the spec (version, URL, schema snapshot) — INFERRED remote
   behavior is labeled as such.
2. Define remote failure modes as ACs: timeout, 5xx, schema drift, auth expiry.
3. Contract tests on the boundary, both directions; integration tests may fake the remote —
   the fake derives from the pinned contract, not from wishful thinking.
4. Security: webhook/callback authentication, secret storage, payload logging rules.

**Watch for:** retry/backoff invented ad hoc (guardrails or ADR decide) · credentials in
fixtures · "the sandbox worked" as the only evidence (record which environment ran).
