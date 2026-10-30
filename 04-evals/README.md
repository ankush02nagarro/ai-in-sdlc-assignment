# Review evaluation

Fixed set: 10 cases in `ops/evals` (codebase) + 2 added here = 12.
Procedure: one review prompt (`prompt-v1.md`) × whole set × **3 runs** → change **exactly one** thing (prompt, model, or context file) → run again.

Definitions:
- **Caught** = defective case flagged for the right reason. **Missed** = defective case not flagged (or flagged for the wrong reason).
- **False alarm** = clean case flagged.

Record every case verdict in `results/runs.csv`, then `python3 summarize.py results/runs.csv` and paste into `results/results.md`.
