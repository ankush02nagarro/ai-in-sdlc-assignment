# Results: review eval, 12 cases × 3 runs × 2 variants = 72 fresh sessions

Generated with `python 04-evals/summarize.py 04-evals/results/runs.csv` (raw output in `summary-output.txt`).
Every row in `runs.csv` is one fresh reviewer session (see `session-ids.md`). Scoring follows `../answer-key.md`, which was fixed before the first run.

Setup: model Claude Opus 5.5 (subagent), no tools, no context file, diff plus prompt only.
v1 is the `ops/evals` prompt verbatim. v2 changes **only the prompt**: it adds a concrete-failure bar and a checklist (`../prompt-v2.md`).
Cases: the 10 cases from `ops/evals`, plus `case-11` (defective, mine) and `case-12` (clean, mine). That gives 8 defective and 4 clean.

| Variant | Caught | Missed | False alarm |
|---|---|---|---|
| v1 run 1 | 8/8 | 0/8 | 0/4 |
| v1 run 2 | 8/8 | 0/8 | 0/4 |
| v1 run 3 | 8/8 | 0/8 | 0/4 |
| **v1 total** | **24/24 = 100% (95% CI 86–100%)** | **0/24 = 0% (0–14%)** | **0/12 = 0% (0–24%)** |
| v2 run 1 | 8/8 | 0/8 | 0/4 |
| v2 run 2 | 8/8 | 0/8 | 0/4 |
| v2 run 3 | 8/8 | 0/8 | 0/4 |
| **v2 total (changed: prompt)** | **24/24 = 100% (86–100%)** | **0/24 = 0% (0–14%)** | **0/12 = 0% (0–24%)** |

Secondary metric, decided while scoring v1 run 1 and applied the same way to every run: **noise on clean cases**. This counts runs where the review called
something in a clean diff a "defect" or "problem" that is not a code defect. It is not counted as a false alarm under the
`ops/evals` rule that "a false alarm is the review asserting a defect that is not there", because the two things it flagged are real but not code defects.

| Variant | Noise on clean cases | What it was |
|---|---|---|
| v1 | **6/12 = 50%** (95% CI 25–75%) | case-06 ×3: "hunk header line counts are wrong". That is true of the hand-written `.diff`, not of the code. case-09 ×3: "README sign-out reset line is a probable/likely defect", rated medium confidence |
| v2 | **2/12 = 17%** (95% CI 5–45%) | Both in run 1 (case-06 hunk header, case-09 README at low-medium confidence). Runs 2 and 3 said "no defects" and mentioned the README line only as unverifiable |

**Sensitivity check:** if a stricter scorer counted those noise items as false alarms, the false-alarm rate would be v1 50% vs v2 17%.

## Was the change an improvement?
**On the three required numbers, no.** Both variants caught all 24 defect instances with zero misses and zero false alarms. The delta is 0, the intervals overlap completely,
and **no case flipped** between v1 and v2. All 24 case-variant pairs were stable across their three runs. The eval has hit its **ceiling** for this model:
it cannot tell v1 and v2 apart on catch rate.

**On noise, v2 looks better, but I cannot claim it.** Noise fell from 6 of 12 to 2 of 12 clean-case runs, a drop of 33 percentage points. That is two cases
moving from "always noisy" to "noisy once". Fisher exact p = 0.19, and the 95% intervals overlap (25–75% vs 5–45%). Qualitatively, v2 reviews also read shorter
and carried fewer low-confidence asides. That is the behaviour I wanted, but I only judged it by eye and did not score it.

## Confidence at this sample size
Low. The 72 sessions are **not 72 independent samples**. Every case gave the same verdict in all three runs, so the run-to-run variance is about 0
and the effective sample size is the number of **distinct cases**: 8 defective and 4 clean.
- With 8 defective cases, the smallest change I could detect is about 3–4 cases flipping (roughly 40 points). A 10-point drop in catch rate would be invisible.
- With 4 clean cases, a 0/4 false-alarm result is compatible with a true rate of up to about 49% (Wilson, n=4). The low false-alarm rate is the least supported claim here.
- The noise improvement depends on 2 cases (06 and 09). One of them (06) is an artefact of the hand-written eval diffs, not a property of real PRs.

What would raise confidence: more **hard** cases, because today's 8 are all caught every time; more clean cases that look suspicious (at least 10); and a different model as the
next single change, so there is headroom to see a difference. Until then: **keep v2 as the default prompt for lower noise, at no measured cost to catches, and do not claim an
improvement in recall.**

## Things the scorer had to decide (would change numbers if decided differently)
1. **case-09 label (clean).** The README line "sign out and sign in again resets the data" is false against the real code: `InMemoryInvoiceRepository` is a singleton registered in
   `Program.cs`, and sign-out only removes the session in `AuthController.Logout`. If case-09 were relabelled defective, v1 would score *caught* 3/3 and v2 roughly 1/3. That would make v1 *better* on recall,
   the opposite of the conclusion above. I kept the label I committed to before the runs, because the defect cannot be shown from the diff alone.
2. **case-06 hunk header.** Counting it as a false alarm would put v1 at 3 of 12 false alarms and v2 at 1 of 12.
