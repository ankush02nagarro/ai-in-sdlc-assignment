# Baseline measurement plan (capture BEFORE the rotation starts)

| Metric | Definition (exact) | Source / query | Captured now? | Value |
|--------|--------------------|----------------|---------------|-------|
| Lead time for changes | **Proxy used:** each commit on `main` → first successful Actions run on `main` (push). True “first PR commit → merge” is undefined: **0 PRs**. | `scripts/capture_baseline.py` → `baseline-output/lead_time_summary.txt` | ✅ | **median 215.4h** (n=6; min 47.4h; max 215.4h) — single late push of six commits |
| Change failure rate | GitHub Actions runs with conclusion success\|failure that failed ÷ those runs; plus ops scenario CSV main-push failures | `change_failure_summary.txt` + `change_failure_ops_timings.txt` | ✅ | **GitHub: 0/1 = 0%**; **ops timings main push: 0/8 = 0%** (scenario). Note: INC-2047 still shows green CI ≠ no change failure |
| Review turnaround | PR ready-for-review → first review submitted | GitHub pulls API | ☐ | **n/a — 0 PRs** |
| Time to restore (needs prod telemetry) | incident open → resolved | incident tool / App Insights alerts | ☐ not available today | n/a |

## Caveats
- Lead time is inflated by batching six commits into one push days later; it is not PR cycle time.
- Dependabot/bots: none observed on this repo.
- Ops `run-timings.csv` is **scenario evidence**, not the GitHub repo’s real history — report both, do not mix into one denominator.
- Incident-linked failure (optional narrative): in the 14-day ops window, release 2.15.1 caused INC-2047 → change failure by incident ≠ CI failure rate.

## Captured numbers
Raw output in `baseline-output/`. Window: commits from 2026-10-05 through CI green 2026-10-14 (`CAPTURED_AT.txt`). Re-run:

```powershell
python 05-risk-and-measurement\scripts\capture_baseline.py ..\ai-in-sdlc-assignment NITIN1670/ai-in-sdlc-assignment
```
