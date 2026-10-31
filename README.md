# AI in SDLC Workshop: Submission

Senior-engineer deliverables for the **Invoice Approval service** (tier-2 go-live in January; PayEx integration).

> Target codebase: `ai-in-sdlc-assignment`. Check it out **next to** this repo (or add as a git submodule under `./code`).
> Scenario and evidence packs: `ops/README.md` in that codebase. `ops/` describes the *planned* deployment, not the code as built.

## Hand-in checklist

| # | Deliverable | Location | Status |
|---|-------------|----------|--------|
| 1 | Mermaid as-built + target diagrams, citation list, inferred-items list | `01-architecture/` | ☑ |
| 2 | One architecture test + the command that runs it | `tests/ArchitectureTests/` | ☑ |
| 3 | Exactly-once decision record (incl. *Where the agent was wrong or useless*) | `02-decision-record/ADR-001-exactly-once-submission.md` | ☑ |
| 4 | One-page autonomy policy, day-one level stated | `03-autonomy-policy/autonomy-policy.md` | ☑ |
| 5 | Two added eval cases + results table (3 runs + changed-variable run) | `04-evals/` | ☑ |
| 6 | Risk audit (lethal trifecta) with decision recorded | `05-risk-and-measurement/risk-audit.md` | ☑ |
| 7 | Measurement plan + two captured numbers | `05-risk-and-measurement/measurement-plan.md` | ☑ |
| 8 | 8–10 min demo video, uploaded and linked | `06-demo/README.md` | ☐ paste link after you record |
| 9 | AI augmentation logs | `ai-augmentation-logs/` | ☑ |

## Install / setup (Windows)

1. **Git**, **.NET 8 SDK**, **Python 3.11+** on PATH (`dotnet --version`, `python --version`).
2. Parent folder layout:
   ```text
   ai-in-sdlc-submission/          ← this repo (your hand-in)
   ai-in-sdlc-assignment/          ← clone of the workshop codebase
   ```
3. Clone the codebase next to this repo if missing:
   ```powershell
   cd "c:\DocX\NAGP\Ai in SDLC\ai-in-sdlc-submission"
   git clone https://github.com/NITIN1670/ai-in-sdlc-assignment.git
   ```
4. Optional: `gh` + `jq` + bash/WSL — not required; use `capture_baseline.py` instead of the `.sh` script.

## Run the one test that matters
```powershell
cd ai-in-sdlc-submission
dotnet test tests/ArchitectureTests --logger "console;verbosity=normal"
```
See `tests/ArchitectureTests/README.md` and `proof-of-run.md`.

## Run the eval summary
```powershell
python 04-evals\summarize.py 04-evals\results\runs.csv
```

## Capture the baseline
```powershell
python 05-risk-and-measurement\scripts\capture_baseline.py ..\ai-in-sdlc-assignment NITIN1670/ai-in-sdlc-assignment
```

## Demo
Read-aloud script and commands: [`06-demo/README.md`](06-demo/README.md). Record 8–10 min; paste the link there; do not commit the MP4.

## Working rules
- Every claim in a diagram cites a file or symbol, or goes in `inferred-items.md`.
- Every number in the eval or measurement docs comes from a file in `results/` or `baseline-output/`.
- Write the ADR and policy yourself; log what the agent produced in `ai-augmentation-logs/`.
