# Change Budget

The change budget is the *authorized blast radius* of a piece of work. It is set by the profile
(or explicitly by a human) before implementation and is a hard contract:

> **An agent never raises its own change budget.** Needing more budget is a finding to report,
> not a decision to make.

## Levels

| Level | Meaning | Typical use |
|---|---|---|
| `minimal` | Touch exclusively what the task requires. No renames, no drive-by cleanup, no formatting of untouched lines | hotfix, bugfix, legacy-refactor start |
| `bounded` | Adjacent changes allowed when required to complete the task (e.g. update a caller's signature) | legacy-feature, api-change |
| `moderate` | Small structural improvements allowed inside touched modules (extract function, rename local) | standard features, technical-debt |
| `architectural` | Structural change is the point: moving boundaries, new modules, contract redesign | architecture-change, migration |
| `unrestricted` | Anything — only under explicit human authorization, typically greenfield | greenfield bootstrap |

## Enforcement

- The budget appears in the spec header and in every task authorization.
- The reviewer checks the diff against the budget: files/changes outside it = `spec-drift`
  finding (`out-of-scope change`), even if the change is "good".
- Wanting to exceed budget: stop, record the reason and the proposed scope as an Open Question or
  decision request, and continue only with the parts inside budget (if independent).

## Budget vs. initiative

Improving something adjacent is not forbidden forever — it is forbidden *silently and now*.
The correct move is a debt/opportunity entry in EVIDENCE.md, which can become its own spec.
