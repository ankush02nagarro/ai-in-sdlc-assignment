# Review prompt v2 (changed ONE variable)
Variable changed: **prompt**. The model (Claude Opus 5.5, `inherit`), the harness wrapper, the fresh session per case
and "no context file" are all identical to v1.

Diff vs v1: two sentences are added to the end of the v1 prompt.
1. A **defect bar**: a finding must name a concrete input, call sequence or production condition that makes it go wrong.
2. A **checklist** of the failure classes that matter for this service: authorization, concurrency,
   error handling that hides failures, money and rounding, sensitive data in logs, and retries or
   idempotency of external calls.

Hypothesis: the checklist raises the catch rate on the subtle cases (rounding in case-03, the non-idempotent
retry in case-11), and the concrete-failure bar holds false alarms on the clean cases (04, 06, 09, 12) at or below v1.

```
Review this diff for defects. For each finding give the file, the line, what
goes wrong, and how confident you are. If you find nothing, say so
explicitly rather than listing general observations.
Only report something as a defect if you can state a concrete input, call
sequence or production condition under which it goes wrong; otherwise do not
report it. Check specifically for: missing or wrong authorization, thread
safety, error handling that hides failures, money and rounding errors,
sensitive data written to logs, and retries or non-idempotent calls to
external systems.
```
