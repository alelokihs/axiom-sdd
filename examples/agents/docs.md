# Example — Docs Agent

**Scenario.** Spec 003 done; it added a CLI flag and one decision was taken.

**Prompt.** [`prompts/update-docs.md`](../prompts/update-docs.md).

**Context received.** EVIDENCE.md, the diff, existing README/docs conventions.

**Expected behavior.** Updates README usage section (new flag, exact syntax from code),
appends D-007 to `sdd/decisions/LOG.md` in standard format (the implementer decided, docs
records), leaves architecture docs alone (nothing structural changed). Proposes deleting a
stale wiki paragraph → asks (deletion needs human ok).

**Expected output.** Two small diffs + decision entry; a line in EVIDENCE "Documentation
updated: README §Usage".

**Common errors.** Documenting intended-but-unproven behavior · creating `docs/spec-003.md`
nobody asked for · rewriting the changelog style "while at it".

**Token tips.** Evidence is the source; never re-derives behavior by reading the whole
codebase.
