# Demo video (8–10 min, MP4 or Teams)

**Link:** TODO — paste Teams/Drive/YouTube link after upload. Do **not** commit the MP4 (`*.mp4` is git-ignored).

**Working directory before recording:**
```powershell
cd "c:\DocX\NAGP\Ai in SDLC\ai-in-sdlc-submission\ai-in-sdlc-submission"
```

---

## Run of show + read-aloud script

| Time | Segment | Open on screen |
|------|---------|----------------|
| 0:00–1:00 | Context | `README.md` |
| 1:00–3:00 | Architecture + test | `01-architecture/` then run test |
| 3:00–5:00 | ADR | `02-decision-record/ADR-001-exactly-once-submission.md` |
| 5:00–6:30 | Eval | `04-evals/results/results.md` + summarize |
| 6:30–7:30 | Autonomy | `03-autonomy-policy/autonomy-policy.md` |
| 7:30–9:00 | Risk + metrics | `05-risk-and-measurement/` |
| 9:00–10:00 | Revisit | `ai-augmentation-logs/INDEX.md` |

### 0:00–1:00 — Context
**Open:** `README.md`

**Say:**
> This is my AI-in-SDLC submission for Invoice Approval. January go-live; PayEx is next. I own as-built versus target architecture, one architecture test, an exactly-once ADR, an autonomy policy, a review-agent eval, a lethal-trifecta risk decision, and two baseline metrics. Trap: `ops/` is planned infrastructure — the code today is still an in-memory ASP.NET API.

### 1:00–3:00 — Architecture + test
**Open:** `01-architecture/as-built.container.mmd` → `as-built.sequence.mmd` → `target-state.mmd` → `corrections.md` → `tests/ArchitectureTests/StructuralRuleTests.cs`

**Say:**
> As-built: session auth, ApprovalsController, ApprovalService, in-memory store. InvoicesController also talks to the store — citation C5. No SQL, no Service Bus, no PayEx in source. Approve is POST `/api/approvals/{id}/approve`. Target adds SQL, outbox, worker, PayEx, audit — all marked NOT BUILT. The agent first drew PayEx as live; I corrected that.

**Run:**
```powershell
dotnet test tests/ArchitectureTests --logger "console;verbosity=normal"
```

**Say:**
> Rule: Domain must not depend on the web host or HTTP, EF, SqlClient, or Service Bus — so PayEx cannot land inside ApprovalService the way INC-2041 did. Second test proves the rule fails on the Api assembly. Both green. Red proof is in `proof-of-run.md`.

### 3:00–5:00 — ADR
**Open:** `02-decision-record/ADR-001-exactly-once-submission.md` (scroll Decision + stress + “Where the agent was wrong”)

**Say:**
> Exactly-once to PayEx. Options: A idempotency plus dedupe, B outbox plus worker, C optimistic plus nightly reconcile. I chose B, with invoice id as the PayEx key, and reconcile as backstop — because a thirty-second timeout is not failure. Preference pushback did not move the agent off B. Three a.m. failure: stale pending after late success — never re-POST without a PayEx lookup. Cost agent picked A on cost alone; I rejected that because A can lose submit intent after Approve. Revisit if duplicates appear or PayEx idempotency is not real.

### 5:00–6:30 — Eval
**Open:** `04-evals/cases/case-11-defect.md`, `case-12-clean.md`, `results/results.md`

**Run:**
```powershell
python 04-evals\summarize.py 04-evals\results\runs.csv
```

**Say:**
> Case eleven: retry payment POST on timeout — defective. Case twelve: trim reject reason — clean. v1 baseline prompt; v2 changes only the prompt. Seventy-two sessions. Both variants: twenty-four of twenty-four caught, zero false alarms. Noise on clean: fifty percent versus seventeen percent; Fisher p about point one nine — not significant. Ceiling effect; keep v2 for less noise; do not claim better recall.

### 6:30–7:30 — Autonomy
**Open:** `03-autonomy-policy/autonomy-policy.md`

**Say:**
> Workflow: first-response incident summaries. Day one: L2 for internal drafts only; L1 for anything that leaves the laptop; production changes L0. Two of six engineers are new — they cannot yet catch a plausible wrong agent narrative. Pairing required before paste into the incident.

### 7:30–9:00 — Risk + measurement
**Open:** `05-risk-and-measurement/risk-audit.md` → `measurement-plan.md` → `baseline-output/SUMMARY.txt`

**Say:**
> `ops/README` has no agent-setup section at the end — I audited the real setup: AGENTS.md plus Playwright MCP. Lethal trifecta is present if incident PII and browser tools share a session. Decision: accept for local workshop use, with mitigations; revisit if MCP meets production credentials or autonomy goes to L3 external post.
>
> Two numbers today: lead-time proxy median two hundred fifteen point four hours, n equals six — zero PRs so true PR lead time undefined. Change failure: GitHub CI zero of one; ops main pushes zero of eight. Review turnaround cannot be captured. Green CI is not no change failure — INC-2047.

### 9:00–10:00 — Close
**Open:** `ai-augmentation-logs/INDEX.md`

**Say:**
> Revisit first: harder eval cases, PayEx landing against the architecture test and ADR, autonomy promotion only with evidence. Augmentation logs list what the agent drafted versus what I kept. Demo link goes in this README — MP4 stays out of git.
