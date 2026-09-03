# Spec Readiness Score

A cheap, deterministic-ish gate for spec quality. Computed by the spec-writer (validation mode)
before Gate 1. It exists to *block confidently bad specs*, not to gold-plate good ones.

## Scoring — 10 criteria × 0–10

| # | Criterion | 0 | 10 |
|---|---|---|---|
| 1 | Clarity of objective | vague intent | one testable sentence |
| 2 | Acceptance criteria | none | complete, verifiable, numbered |
| 3 | Scope boundary | absent | in and OUT both explicit |
| 4 | Expected behavior | prose hand-wave | inputs/outputs/errors described |
| 5 | Dependencies | unexamined | listed with status |
| 6 | Risks | none | identified with mitigation/acceptance |
| 7 | Architecture impact | unknown | assessed against guardrails |
| 8 | Security impact | unconsidered | assessed; untrusted input identified |
| 9 | Test strategy | none | test types + AC mapping declared |
| 10 | Ambiguity handling | silent gaps | every gap is UNKNOWN / ASSUMPTION / NEEDS_CONFIRMATION |

Score = sum (0–100). Any **blocking Open Question caps the score at 59**.

## Thresholds

```
 < 60    NOT_READY          -> back to requirement-analyst / requester
60–79    REVIEW_REQUIRED    -> a human (or architect) must approve explicitly
80–89    READY              -> implementation may start
90–100   HIGH_CONFIDENCE    -> implementation may start; light review workflow allowed
```

Profiles may raise the bar (e.g. `migration` requires ≥ 85). They may not lower it below 60.

## Anti-gaming rule

The score is justified per criterion in one line each, in the SPEC's Readiness section.
A number without the ten one-liners is invalid.
