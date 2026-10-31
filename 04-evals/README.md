# Review evaluation

Fixed set: 10 cases in `ops/evals/cases` (codebase) + 2 added here (`cases/case-11.diff` defective, `cases/case-12.diff` clean) = 12.
Procedure: one review prompt (`prompt-v1.md`) × whole set × **3 runs** → change **exactly one** thing (the prompt → `prompt-v2.md`) → 3 more runs.
Each case × run was a fresh subagent session given only the diff and the prompt (see `results/session-ids.md`).

Definitions:
- **Caught** = defective case flagged for the right reason (see `answer-key.md`). **Missed** = defective case not flagged, or flagged for the wrong reason.
- **False alarm** = clean case where the review asserted a code defect.
- **Noise on clean** (secondary) = clean case where the review called something a defect that is not a code defect (hunk-header miscount, an unverifiable README claim).

Result (details and confidence in `results/results.md`):

| Variant | Caught | Missed | False alarm | Noise on clean |
|---|---|---|---|---|
| v1 (3 runs) | 24/24 | 0/24 | 0/12 | 6/12 |
| v2, prompt changed (3 runs) | 24/24 | 0/24 | 0/12 | 2/12 |

Reproduce the table:

```bash
python 04-evals/summarize.py 04-evals/results/runs.csv
```
