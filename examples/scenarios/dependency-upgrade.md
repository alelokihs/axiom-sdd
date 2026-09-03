# Recipe — Dependency upgrade

Profile [`dependency-upgrade`](../../sdd/profiles/dependency-upgrade.yaml) · budget bounded ·
workflow fast.

1. Breaking changes listed **from the dependency's changelog** (fetched, not remembered).
2. Advisory check (known CVEs fixed/introduced) — security agent is in the roster.
3. Full regression suite; lockfile updated consistently (one package manager, one lockfile).
4. Evidence: dependency-diff (old→new versions) + advisory-check result + suite run.

**Watch for:** upgrading 14 packages in one spec (blast radius unreadable — batch by risk) ·
code "fixes" sneaking in with the bump (budget: adaptation to the new API only).
