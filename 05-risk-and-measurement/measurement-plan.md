# Baseline measurement plan (capture BEFORE the rotation starts)

| Metric | Definition (exact) | Source / query | Captured now? | Value |
|--------|--------------------|----------------|---------------|-------|
| Lead time for changes | first commit on a PR → merged to default branch (proxy for deploy) | `scripts/capture_baseline.sh` (gh api / git log) | ✅ | TODO |
| Change failure rate | deploy runs that failed or were followed by revert/hotfix ÷ deploy runs | GitHub Actions: `gh run list --workflow <deploy> --json conclusion` + `git log --grep=revert` | ✅ | TODO |
| Review turnaround | PR ready-for-review → first review submitted | `gh api repos/:o/:r/pulls/:n/reviews` | ☐ (post-rotation capture; also computable today) | TODO |
| Time to restore (needs prod telemetry) | incident open → resolved | incident tool / App Insights alerts | ☐ not available today | n/a |

## Caveats
Proxy vs true definition; sample window; bots/dependabot excluded or included (state which).

## Captured numbers
Raw output committed in `baseline-output/`. Window: TODO to TODO.
