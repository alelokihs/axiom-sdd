# Spec Drift Detection

Final consistency check between the three sources that must agree:

```
Specification  ↕  Code  ↕  Tests
```

Run by the reviewer (drift mode) after implementation and tests, before evidence is accepted.

## What to detect

| Drift type | Question |
|---|---|
| `unimplemented-requirement` | Spec/AC promises behavior the code does not deliver |
| `unspecified-behavior` | Code delivers observable behavior no spec describes |
| `missing-test` | An AC or declared edge case has no verifying test |
| `out-of-scope-change` | The diff touches files/behavior outside authorized tasks + change budget |
| `architecture-divergence` | Implementation contradicts guardrails or the approved PLAN |
| `unproven-criterion` | AC claimed satisfied but no evidence maps to it |

## Procedure (token-cheap)

1. Load the context pack: SPEC (ACs, scope, edge cases), TASKS (authorized set), the **diff**
   (not whole files), test list/results, guardrails. Nothing else.
2. Walk each AC → find implementing change → find verifying test → find evidence entry.
3. Walk the diff → map each hunk to a task. Unmapped hunk = candidate drift.
4. Compare structure of the change against PLAN and guardrails.

## Verdict

```
SPEC_DRIFT_NONE
```

or

```
SPEC_DRIFT_DETECTED
- [type] <one-line description> — spec says X · code/tests do Y — suggested route: <agent>
```

Routing: unimplemented/missing-test → implementer/test-engineer; unspecified or out-of-scope →
human decides (remove, or spec absorbs it via explicit update); architecture-divergence → architect.

**The drift detector never fixes anything.** It reports.
