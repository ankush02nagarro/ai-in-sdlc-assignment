#!/usr/bin/env python3
"""Windows-friendly baseline capture (no gh/jq/bash required).

Usage:
  python capture_baseline.py [path/to/ai-in-sdlc-assignment] [OWNER/REPO]

Defaults: sibling ../ai-in-sdlc-assignment and NITIN1670/ai-in-sdlc-assignment
Writes ../baseline-output/
"""
from __future__ import annotations

import csv
import json
import statistics
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve()
OUT = SCRIPT.parent.parent / "baseline-output"
REPO_DIR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (SCRIPT.parents[3] / "ai-in-sdlc-assignment")
SLUG = sys.argv[2] if len(sys.argv) > 2 else "NITIN1670/ai-in-sdlc-assignment"


def get_json(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "baseline-capture"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO_DIR), *args], text=True, stderr=subprocess.STDOUT).strip()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary_lines: list[str] = []

    # --- Lead time: commit authored → first successful CI on default branch (proxy; 0 PRs) ---
    runs = get_json(f"https://api.github.com/repos/{SLUG}/actions/runs?per_page=20&branch=main&event=push")
    success_runs = [r for r in runs.get("workflow_runs", []) if r.get("conclusion") == "success"]
    first_green = min((parse_iso(r["updated_at"]) for r in success_runs), default=None)

    commits_raw = git("log", "main", "--format=%H|%cI|%s")
    lead_rows = []
    hrs = []
    if commits_raw and first_green:
        for line in commits_raw.splitlines():
            sha, ciso, subj = line.split("|", 2)
            committed = parse_iso(ciso)
            h = (first_green - committed).total_seconds() / 3600
            hrs.append(h)
            lead_rows.append({"sha": sha[:12], "committed_at": ciso, "first_green_at": first_green.isoformat(), "hours": f"{h:.1f}", "subject": subj})
    with (OUT / "lead_time_raw.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sha", "committed_at", "first_green_at", "hours", "subject"])
        w.writeheader()
        w.writerows(lead_rows)
    if hrs:
        hrs_sorted = sorted(hrs)
        lead_s = (
            f"proxy=commit_to_first_main_CI_green n={len(hrs)} "
            f"median={statistics.median(hrs):.1f}h min={min(hrs):.1f}h max={max(hrs):.1f}h "
            f"note=0_PRs_so_PR_lead_time_undefined"
        )
    else:
        lead_s = "no commits or no successful CI run"
    (OUT / "lead_time_summary.txt").write_text(lead_s + "\n", encoding="utf-8")
    summary_lines.append("LEAD_TIME: " + lead_s)

    # --- Change failure rate: GitHub Actions ---
    all_runs = get_json(f"https://api.github.com/repos/{SLUG}/actions/runs?per_page=50")
    scored = [r for r in all_runs.get("workflow_runs", []) if r.get("conclusion") in ("success", "failure")]
    fail = sum(1 for r in scored if r["conclusion"] == "failure")
    total = len(scored)
    rate = f"{fail / total:.1%}" if total else "n/a"
    try:
        reverts = len([l for l in git("log", "--oneline", "-i", "--grep=revert").splitlines() if l])
        hotfixes = len([l for l in git("log", "--oneline", "-i", "--grep=hotfix").splitlines() if l])
    except subprocess.CalledProcessError:
        reverts = hotfixes = 0
    cfr_gh = f"github_actions runs={total} failed={fail} failure_rate={rate} revert_commits={reverts} hotfix_commits={hotfixes}"
    (OUT / "change_failure_summary.txt").write_text(cfr_gh + "\n", encoding="utf-8")
    (OUT / "deploy_runs.json").write_text(json.dumps(all_runs.get("workflow_runs", []), indent=2), encoding="utf-8")
    summary_lines.append("CHANGE_FAILURE_GITHUB: " + cfr_gh)

    # --- Ops fictional pipeline timings (scenario evidence) ---
    timings = REPO_DIR / "ops" / "pipeline" / "run-timings.csv"
    if timings.exists():
        by_run: dict[str, dict] = {}
        with timings.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rn = row["run_number"]
                by_run.setdefault(rn, {"branch": row["branch"], "event": row["event"], "conclusion": row["conclusion"]})
        main_push = [v for v in by_run.values() if v["branch"] == "main" and v["event"] == "push"]
        main_fail = sum(1 for v in main_push if v["conclusion"] == "failure")
        ops_s = f"ops_run_timings main_push_runs={len(main_push)} failed={main_fail} failure_rate={main_fail/len(main_push):.1%}" if main_push else "ops_run_timings empty"
        (OUT / "change_failure_ops_timings.txt").write_text(ops_s + "\n", encoding="utf-8")
        summary_lines.append("CHANGE_FAILURE_OPS: " + ops_s)

    # --- Review turnaround ---
    prs = get_json(f"https://api.github.com/repos/{SLUG}/pulls?state=all&per_page=50")
    rev_s = f"pull_requests={len(prs)} review_turnaround=n/a (zero PRs)" if isinstance(prs, list) else "pull_requests=error"
    if isinstance(prs, list) and prs:
        rev_s = f"pull_requests={len(prs)} — compute reviews separately"
    (OUT / "review_turnaround_summary.txt").write_text(rev_s + "\n", encoding="utf-8")
    summary_lines.append("REVIEW_TURNAROUND: " + rev_s)

    captured = datetime.now(timezone.utc).isoformat()
    (OUT / "CAPTURED_AT.txt").write_text(captured + f"\nrepo={REPO_DIR}\nslug={SLUG}\n", encoding="utf-8")
    (OUT / "SUMMARY.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print("\n".join(summary_lines))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
