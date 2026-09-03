# Tutorial — Greenfield project

Goal: new internal tool ("team-radar", Next.js + small API). Runtime: Claude. Repo: empty.

## 1. Bootstrap in new mode

```
Initialize SDD.
Framework: ../sdd-framework
Mode: new
Context: Next.js 15 + TypeScript; API routes only (no separate backend); Postgres later.
Source:
Business need: weekly team health dashboard. First slice: submit a 3-question pulse
survey and see the team average.
```

## 2. What the bootstrap does differently

Detection is intent-only (nothing to scan). The **architect runs first** (design mode):
minimal structure for the first slice ONLY (no speculative microservices, no Postgres yet —
in-memory store behind an interface, founding ADR-001 records the swap plan), initial
guardrails all `NEEDS_CONFIRMATION`:

```
Layering: app/ (routes) -> lib/ (domain) ; lib imports no Next.js
Data: store behind StorePort interface; no direct DB calls in routes
Testing: vitest; every AC gets a test
```

Profile `greenfield-feature`, budget moderate, models planning=frontier / execution=balanced.
Spec 001 = the pulse-survey slice, readiness 82. Output ends:
`NEXT ACTION: SDD: implement 001 TASK-001`.

## 3. The anti-overengineering gate in action

During TASK-002 the implementer is tempted to add user auth "since every app needs it".
Budget check: auth is not in spec 001 → recorded as opportunity, NOT implemented. It becomes
spec 002 when the business asks.

## 4. First cycle closes

Tests → review → `SPEC_DRIFT_NONE` → evidence → gitflow proposes GitHub Flow +
Conventional Commits (`NEEDS_CONFIRMATION`, human confirms) → first PR.

After three cycles the guardrails lose their `NEEDS_CONFIRMATION` labels — they've been
confirmed by use. The project now has an architecture record instead of an oral tradition.
