# TEST PLAN — <Feature name>   *(only when a separate doc earns its keep)*

- **Spec:** `<NNN>-<slug>` · usually the SPEC §11 is enough — use this when test complexity is
  itself a risk (migrations, integrations, E2E suites).

## Strategy
Modes in play (unit/integration/contract/regression/e2e/characterization) and what each proves.

## AC coverage map
| AC | Mode | Test (planned name) | Data/fixtures |
|---|---|---|---|

## Edge & adversarial cases
Inputs that should hurt: empty, huge, malformed, concurrent, hostile (when untrusted input).

## Environment & data
What the tests need; how fixtures avoid real/PII data.

## Out of test scope
What is knowingly not verified, and why that's acceptable.
