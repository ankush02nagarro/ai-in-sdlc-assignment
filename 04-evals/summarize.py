#!/usr/bin/env python3
"""Summarise review-eval runs: caught / missed / false-alarm rates with 95% Wilson intervals.

CSV columns: variant,run,case_id,label,flagged_correctly
  label=defective -> flagged_correctly=1 means CAUGHT, 0 means MISSED
  label=clean     -> flagged_correctly=1 means FALSE ALARM, 0 means correctly left alone
"""
import csv, math, sys
from collections import defaultdict

def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 2
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - m) / d, (c + m) / d

def main(path):
    agg = defaultdict(lambda: {"caught": 0, "def": 0, "fa": 0, "clean": 0})
    per_case = defaultdict(list)
    with open(path) as f:
        for r in csv.DictReader(f):
            if r["flagged_correctly"].strip() == "":
                continue
            v, flag = r["variant"], int(r["flagged_correctly"])
            a = agg[v]
            if r["label"] == "defective":
                a["def"] += 1; a["caught"] += flag
            else:
                a["clean"] += 1; a["fa"] += flag
            per_case[(v, r["case_id"])].append(flag)

    print("| Variant | Caught | Missed | False alarm |")
    print("|---|---|---|---|")
    for v, a in sorted(agg.items()):
        def fmt(k, n):
            lo, hi = wilson(k, n)
            return f"{k}/{n} = {k/n:.0%} (95% CI {lo:.0%}-{hi:.0%})" if n else "n/a"
        print(f"| {v} | {fmt(a['caught'], a['def'])} | {fmt(a['def']-a['caught'], a['def'])} | {fmt(a['fa'], a['clean'])} |")

    print("\nPer-case consistency (same case, 3 runs; unstable = nondeterminism):")
    for (v, c), flags in sorted(per_case.items()):
        tag = "stable" if len(set(flags)) == 1 else "UNSTABLE"
        print(f"  {v} {c}: {flags} {tag}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/runs.csv")
