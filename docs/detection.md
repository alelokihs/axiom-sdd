# Detection Heuristics

Read-only pass, cheap-first: filenames and manifests before file contents; contents only to
disambiguate. Every result carries `CONFIRMED` / `INFERRED` / `UNKNOWN` — see the
[non-invention rule](../core/constitution.md).

## Signals table

| Dimension | Look at (in order) |
|---|---|
| Language | manifest files (`package.json`, `pyproject.toml`, `pom.xml`, `build.gradle*`, `go.mod`, `Cargo.toml`, `*.csproj`, `composer.json`, `Gemfile`) → extension census as fallback (INFERRED) |
| Framework | dependencies inside the manifest (spring-boot, next, react, fastapi, django, express, rails, …) |
| Build/PM | lockfiles (`package-lock`/`pnpm-lock`/`yarn.lock`, `poetry.lock`/`uv.lock`, `mvnw`/`gradlew`) — wrapper presence beats global assumption |
| Frontend/backend | both manifests present? folder names (`web/`, `api/`, `frontend/`…) are INFERRED only |
| Tests | test dirs + config (`pytest.ini`/`pyproject [tool.pytest]`, `jest`/`vitest` config, `src/test/java`, `*_test.go`) · coverage config if present |
| Lint/format | `.eslintrc*`, `ruff`/`flake8`/`black` config, `.editorconfig`, `checkstyle`, `prettier` |
| Architecture | layer-named dirs (`domain/ application/ infrastructure/ api/`), module manifests, monorepo markers (`nx.json`, `turbo.json`, `pnpm-workspace.yaml`) — always INFERRED unless docs confirm |
| Database/migrations | migration dirs (`migrations/`, `db/migrate`, `flyway`/`liquibase`/`alembic` config), ORM deps |
| Docker/infra | `Dockerfile*`, `docker-compose*`, `k8s/`, `helm/`, `terraform/` |
| CI | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml` |
| Git convention | `git branch -a` patterns · last ~30 `git log --oneline` messages · merge-commit vs squash shape · hooks (`.pre-commit-config.yaml`, `.husky/`) |
| Docs | `README*`, `docs/`, `CONTRIBUTING*`, existing ADR dirs (`adr/`, `docs/decisions/`) |
| Existing AI config | `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md` — NEVER overwrite silently; merge-or-ask |
| Security posture | `.env.example` (good) vs committed `.env` (finding!), secret scanning config, auth deps |
| Observability | logging/tracing deps, otel config |

## Rules

1. Cheap first: one directory listing + manifests answer most dimensions.
2. Evidence with every INFERRED: `architecture: hexagonal (INFERRED: domain/ imports nothing)`.
3. Contradictions are findings, not choices (`README says yarn, lockfile is pnpm-lock.yaml`).
4. A committed secret or `.env` with real values: report immediately as a security finding in
   the bootstrap output — do not paste the value anywhere.
5. Time-box: detection is minutes, not a codebase audit. Deep understanding is the
   codebase-analyst's job, per spec, later.
