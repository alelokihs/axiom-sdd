# Recipe — Bugfix

Profile [`bugfix`](../../sdd/profiles/bugfix.yaml) · budget **minimal** · workflow fast.

```
SDD: fix bug
Source: <report + expected vs actual + stack trace if any>
```

1. Reproduce (or record why impossible). 2. Root cause written before fixing.
3. **Regression test that fails** on current code. 4. Minimal fix → test passes.
5. Compact spec absorbs plan/tasks; evidence gets root-cause + reproduction steps.

**Watch for:** fixing symptoms (test asserts the output, cause still there) · "improving"
surrounding code · a fix without its failing-first test (that's the whole point).
