# Model Selection

Bootstrap proposes — **without asking a human** — the best LLM model for each plane of the
selected workflow, according to the spec/profile, and embeds the result in `sdd/sdd.yaml`
(`models:` block) and in the generated `AGENTS.md` (per-roster-entry tier). Runtimes resolve
tiers to concrete models via their adapter table.

## Tiers (runtime-neutral)

| Tier | Use for | Traits |
|---|---|---|
| `fast` | mechanical, low-ambiguity steps: gitflow, docs formatting, context-pack assembly, detection | cheapest, lowest latency |
| `balanced` | standard implementation, tests, standard review | good code quality / cost ratio |
| `frontier` | planning under ambiguity, architecture, legacy analysis, security review, drift on large diffs | strongest reasoning |

## Selection rules (deterministic)

Inputs: profile (workflow, budget, token_budget), spec signals (readiness score, ambiguity count,
blast radius, security surface).

```
planning      = frontier if (workflow in {full} or readiness < 80 or ambiguity high) else balanced
execution     = balanced by default
              | frontier if budget in {architectural} or specialization in {migration, refactoring on large blast radius}
              | fast     if profile in {documentation-change, test-coverage} and scope trivial
verification  = frontier if security agent in roster or budget >= architectural else balanced
support       = fast (gitflow, docs), always
bootstrap/detection = fast for scanning, balanced for classification
```

Escalation without humans: any agent may **escalate one tier upward** when it detects it is
failing the task (two consecutive gate failures, or self-assessed low confidence) — recording
the escalation in EVIDENCE.md. De-escalation is never automatic.

## Embedding

`sdd/sdd.yaml`:
```yaml
models:
  selected_by: bootstrap (auto)     # no human in the loop; edit to override
  planning:     {tier: frontier, resolved: <adapter table>}
  execution:    {tier: balanced, resolved: <…>}
  verification: {tier: balanced, resolved: <…>}
  support:      {tier: fast,     resolved: <…>}
```

`AGENTS.md` roster entries carry `· model: <tier> (<resolved>)`.

## Resolution tables

Live in each adapter (concrete names change faster than this framework — adapters own them):
[claude](../adapters/claude/ADAPTER.md#model-tiers) · [copilot](../adapters/copilot/ADAPTER.md#model-tiers) ·
[devin](../adapters/devin/ADAPTER.md#model-tiers) · [codex](../adapters/codex/ADAPTER.md#model-tiers).
If the org restricts available models, resolve to the nearest available tier and record the
substitution in `sdd.yaml` — never silently.
