#!/usr/bin/env bash
# Usage: capture_baseline.sh /path/to/ai-in-sdlc-assignment [OWNER/REPO] [DEPLOY_WORKFLOW_FILE]
# Needs: git, gh (authenticated), jq. Outputs to ../baseline-output/
set -euo pipefail
REPO_DIR="${1:?path to codebase}"
SLUG="${2:-$(cd "$REPO_DIR" && gh repo view --json nameWithOwner -q .nameWithOwner)}"
WF="${3:-}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/baseline-output"
mkdir -p "$OUT"
cd "$REPO_DIR"

echo "== Lead time: first commit -> merge, per merged PR (hours)"
gh pr list -R "$SLUG" --state merged --limit 500 \
  --json number,mergedAt,commits,author \
  | jq -r '.[] | select(.author.is_bot|not)
      | [.number, .commits[0].committedDate, .mergedAt] | @csv' > "$OUT/lead_time_raw.csv"
python3 - "$OUT" <<'PY'
import csv, sys, statistics as st
from datetime import datetime
out = sys.argv[1]
hrs = []
for n, a, b in csv.reader(open(f"{out}/lead_time_raw.csv")):
    f = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    hrs.append((f(b) - f(a)).total_seconds() / 3600)
hrs.sort()
if hrs:
    p = lambda q: hrs[min(len(hrs)-1, int(q*len(hrs)))]
    s = f"n={len(hrs)} median={st.median(hrs):.1f}h p75={p(.75):.1f}h p90={p(.9):.1f}h"
else:
    s = "no merged PRs found"
open(f"{out}/lead_time_summary.txt", "w").write(s + "\n"); print(s)
PY

echo "== Change failure rate (CI history)"
if [ -n "$WF" ]; then
  gh run list -R "$SLUG" --workflow "$WF" --limit 500 --json conclusion,createdAt,headSha > "$OUT/deploy_runs.json"
else
  gh run list -R "$SLUG" --limit 500 --json workflowName,conclusion,createdAt,headSha > "$OUT/deploy_runs.json"
fi
TOTAL=$(jq '[.[]|select(.conclusion=="success" or .conclusion=="failure")]|length' "$OUT/deploy_runs.json")
FAIL=$(jq '[.[]|select(.conclusion=="failure")]|length' "$OUT/deploy_runs.json")
REVERTS=$(git log --oneline -i --grep='^revert\|hotfix' | wc -l)
printf "runs=%s failed=%s failure_rate=%s reverts_or_hotfix_commits=%s\n" "$TOTAL" "$FAIL" \
  "$(python3 -c "print(f'{$FAIL/$TOTAL:.1%}' if $TOTAL else 'n/a')")" "$REVERTS" | tee "$OUT/change_failure_summary.txt"

echo "== Review turnaround (bonus; computable today)"
gh pr list -R "$SLUG" --state merged --limit 200 --json number,createdAt,reviews \
  | jq -r '.[]|select(.reviews|length>0)|[.number,.createdAt,(.reviews|map(.submittedAt)|sort|first)]|@csv' \
  > "$OUT/review_turnaround_raw.csv"
echo "Done. Outputs in $OUT"
