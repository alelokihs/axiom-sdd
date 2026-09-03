# Example — Test Engineer

**Scenario.** Spec 003 implemented; profile requires modes `unit, regression`.

**Prompt.** [`prompts/generate-tests.md`](../prompts/generate-tests.md).

**Context received.** SPEC §6/§11, the diff, related tests from the pack (for conventions).

**Expected behavior.** Maps AC-01→`test_export_csv_happy_path` (names cite ACs), AC-02→two
cases, AC-03 (concurrent access) → cannot test in this suite → records `UNPROVEN: needs
integration env, proposed for CI` instead of skipping silently. Uses the project's fixture
style; no new test framework. Runs the suite; pastes the real summary (`47 passed, 0 failed`).

**Expected output.** Test files + EVIDENCE.md test section (counts, results, coverage map,
gaps).

**Common errors.** Deleting a failing existing test ("it was flaky") — a finding, not an
obstacle · asserting nothing to inflate counts · inventing a mock that hides the behavior
under test.

**Token tips.** Doesn't read PLAN; the diff + AC list is the spec of the tests.
