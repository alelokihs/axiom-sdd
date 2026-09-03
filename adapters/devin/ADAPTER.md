# Adapter — Devin

## Capabilities assumed
Long autonomous sessions · own VM/shell/browser · Playbooks (reusable task programs) and
Knowledge (persistent org notes) · checkpoint/report cadence · higher autonomy ⇒ tighter
boundaries needed.

## What bootstrap generates

**Playbook: "SDD cycle"** (one per project, from the selected profile) — structure:
```
Overview: run spec <NNN>-<slug> through the SDD lifecycle (profile: <profile>).
Procedure: follow sdd/workflows/<workflow>.yaml step by step; at each step assume the agent
  role from sdd/agents/<agent>.agent.md (Mandatory Reading + Forbidden are binding).
What's needed: repo access; sdd/ initialized; the spec id.
Forbidden: the six locks (verbatim) + never merge/push without human confirmation.
Advice: checkpoint after every gate — post the gate name + verdict + evidence delta.
```

**Knowledge suggestions** (short entries, added by the team): the six locks · project guardrails
pointer · gitflow convention block from `sdd/sdd.yaml`.

## Runtime notes — autonomy discipline
- **Checkpoints = gates.** Devin reports at every gate with the verdict and evidence so far;
  a failing gate PAUSES the session and asks, instead of self-negotiating.
- **DoD is the stop condition.** The session ends at `evidence-complete` + prepared gitflow —
  never at "seems done". Partial work is reported partial.
- **Budget watch.** Long sessions drift; the change budget line in every task authorization is
  the leash. Out-of-budget discoveries go to the debt list, not the diff.
- Give Devin one spec per session; parallel specs = parallel sessions with disjoint file scopes.

## Model tiers
Devin manages models internally — the `models:` block still matters as **effort routing**:

| Tier | Resolve to |
|---|---|
| fast | small scoped session, tight instructions |
| balanced | normal session |
| frontier | high-effort session; enable maximum reasoning/planning options where offered |

Record `resolved: devin-managed (<session shape>)` in `sdd.yaml`.
