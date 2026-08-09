#!/usr/bin/env python3
"""Score the blind panel: join judge verdicts to the withheld key and report per-arm wins.

A verdict is only counted when the judge named a side. NONE is reported, never silently dropped —
a judge that failed to answer is a fact about the panel, not a tie.
"""
import collections
import json
import sys
from math import comb
from pathlib import Path


def sign_test(a: int, b: int) -> float:
    n = a + b
    if n == 0:
        return 1.0
    p = sum(comb(n, k) for k in range(min(a, b) + 1)) / 2**n * 2
    return min(p, 1.0)


def main() -> None:
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/td-blind")
    key = json.loads((d / "_key.json").read_text())

    per_judge: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    overall = collections.Counter()
    by_pair: dict[str, list[str]] = collections.defaultdict(list)

    for line in (d / "results.tsv").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        pair, judge, verdict = parts
        if pair not in key:
            continue
        if verdict in ("A", "B"):
            arm = key[pair][verdict]
        elif verdict == "TIE":
            arm = "tie"
        else:
            arm = "no-answer"
        per_judge[judge][arm] += 1
        overall[arm] += 1
        by_pair[pair].append(arm)

    print("Blind A/B panel — caveman vs pure, real diolog-swe-bench final reports")
    print("Judges saw anonymised pairs only: no skill files, no arm labels, no bench grade.\n")

    print(f"{'judge':<10} {'pure':>6} {'caveman':>8} {'tie':>5} {'no-answer':>10}")
    for judge in sorted(per_judge):
        c = per_judge[judge]
        print(f"{judge:<10} {c['pure']:>6} {c['caveman']:>8} {c['tie']:>5} {c['no-answer']:>10}")
    print(f"{'TOTAL':<10} {overall['pure']:>6} {overall['caveman']:>8} "
          f"{overall['tie']:>5} {overall['no-answer']:>10}")

    p = sign_test(overall["pure"], overall["caveman"])
    print(f"\nDecisive verdicts: {overall['pure'] + overall['caveman']}"
          f"  sign test p = {p:.4f}")

    # Per-pair majority — the unit the benchmark scores on.
    maj = collections.Counter()
    for pair, arms in by_pair.items():
        votes = collections.Counter(a for a in arms if a in ("pure", "caveman"))
        if not votes:
            maj["undecided"] += 1
        elif len(votes) == 2 and votes["pure"] == votes["caveman"]:
            maj["split"] += 1
        else:
            maj[votes.most_common(1)[0][0]] += 1
    print(f"\nPer-pair majority: pure {maj['pure']}, caveman {maj['caveman']}, "
          f"split {maj['split']}, undecided {maj['undecided']}")


if __name__ == "__main__":
    main()
