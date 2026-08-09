#!/usr/bin/env python3
"""Un-blind the panel and tally it.

Reads results.tsv (pair, judge, verdict) and _key.json (which arm was A), and
reports wins per arm, per judge family, and per eval.

A judge that returned nothing is counted as NONE and reported, never dropped —
a silent exclusion turns a broken harness into a clean-looking result. Ties are
reported as ties rather than split.

Usage: score_blind_panel.py <bundle_dir>
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def main() -> None:
    d = Path(sys.argv[1])
    key = json.loads((d / "_key.json").read_text())
    rows = [
        line.split("\t")
        for line in (d / "results.tsv").read_text().splitlines()
        if line.strip()
    ]

    arm_wins = collections.Counter()
    by_judge = collections.defaultdict(collections.Counter)
    by_eval = collections.defaultdict(collections.Counter)
    none = collections.Counter()

    for pair, judge, verdict in rows:
        k = key.get(pair)
        if not k:
            continue
        ev = k["eval"]
        if verdict in ("A", "B"):
            arm = k[verdict]
            arm_wins[arm] += 1
            by_judge[judge][arm] += 1
            by_eval[ev][arm] += 1
        elif verdict == "TIE":
            arm_wins["tie"] += 1
            by_judge[judge]["tie"] += 1
            by_eval[ev]["tie"] += 1
        else:
            none[judge] += 1
            by_judge[judge]["none"] += 1
            by_eval[ev]["none"] += 1

    decided = arm_wins["skill"] + arm_wins["baseline"]
    total = decided + arm_wins["tie"] + sum(none.values())

    print("=== overall ===")
    print(f"judgments cast : {total}")
    print(f"skill wins     : {arm_wins['skill']}")
    print(f"baseline wins  : {arm_wins['baseline']}")
    print(f"ties           : {arm_wins['tie']}")
    print(f"no verdict     : {sum(none.values())}")
    if decided:
        print(f"skill share of decided pairs: {arm_wins['skill'] / decided:.1%}")
    else:
        print("skill share of decided pairs: n/a — nothing was decided")

    print("\n=== by judge family ===")
    print(f"{'judge':<10}{'skill':>7}{'base':>7}{'tie':>6}{'none':>6}")
    for j in sorted(by_judge):
        c = by_judge[j]
        print(f"{j:<10}{c['skill']:>7}{c['baseline']:>7}{c['tie']:>6}{c['none']:>6}")

    print("\n=== by eval ===")
    for e in sorted(by_eval):
        c = by_eval[e]
        print(f"{e}\n  skill={c['skill']}  baseline={c['baseline']}  tie={c['tie']}  none={c['none']}")

    if none:
        print("\nNOTE: judges returning no parseable verdict are reported above, not dropped.")
        for j, n in none.items():
            print(f"  {j}: {n}")


if __name__ == "__main__":
    main()
