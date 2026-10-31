# Reviewer sessions

Each row of `runs.csv` is one fresh Cursor subagent session (72 in total: 12 cases × 3 runs × 2 variants). Each session received only the harness wrapper,
the prompt (`../prompt-v1.md` or `../prompt-v2.md`) and one diff. No tools, files or context were available to it.
The sessions are viewable as subagent runs in the Cursor chat that produced this submission. `finding_summary` in `runs.csv` records what each one reported.

## Spot check of reviewer arithmetic (case-03)
Several case-03 reviews gave numeric examples. I checked them by hand and all were correct, including
19.99 at 15% (new code 17.00 vs old 16.99) and 0.99 at 33% (new 0.67 vs old 0.66). No review was scored "caught" on an example that was wrong.
