# Templates

Instantiated on demand (when the lifecycle reaches them), into `sdd/specs/<NNN>-<slug>/` unless
noted. Fill only meaningful fields — explicit `N/A` beats invented filler.

> Cross-references inside templates use root-anchored `sdd/...` paths so they stay unambiguous
> after instantiation, wherever the file lands.

| Template | Instantiated as | When |
|---|---|---|
| [SPEC.md](./SPEC.md) | `SPEC.md` | workflows with `spec_form: full` |
| [SPEC-COMPACT.md](./SPEC-COMPACT.md) | `SPEC.md` | `spec_form: compact` (fast workflow — absorbs PLAN+TASKS) |
| [HOTFIX-DOC.md](./HOTFIX-DOC.md) | `SPEC.md` | `spec_form: single-doc` (hotfix — spec+tasks+evidence in one) |
| [PLAN.md](./PLAN.md) | `PLAN.md` | full/standard workflows |
| [TASKS.md](./TASKS.md) | `TASKS.md` | full/standard workflows |
| [EVIDENCE.md](./EVIDENCE.md) | `EVIDENCE.md` | always (except hotfix single-doc, which embeds it) |
| [CONTEXT-PACK.md](./CONTEXT-PACK.md) | `CONTEXT-PACK.md` | when codebase-analyst builds the pack |
| [TEST-PLAN.md](./TEST-PLAN.md) | `TEST-PLAN.md` | only when profile/test complexity justifies a separate doc |
| [SECURITY-REVIEW.md](./SECURITY-REVIEW.md) | `SECURITY-REVIEW.md` | when profile includes the security agent |
| [DECISION.md](./DECISION.md) | appended to `sdd/decisions/LOG.md` | any non-trivial decision |
| [ADR.md](./ADR.md) | `sdd/decisions/ADR-NNN-slug.md` | durable architectural decisions |
| [GUARDRAILS.md](./GUARDRAILS.md) | `sdd/guardrails.md` (project root of SDD) | at bootstrap |
| [project-sdd.yaml](./project-sdd.yaml) | `sdd/sdd.yaml` | at bootstrap |
