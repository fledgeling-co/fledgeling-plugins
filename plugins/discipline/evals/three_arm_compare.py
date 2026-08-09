#!/usr/bin/env python3
"""The three-arm paired comparison, run exactly the way the diolog-swe-bench scoring spec defines it.

Deterministic and re-runnable: it reads the Benchwarmer store, applies that repo's canonical rule
(binary fail-to-pass for behavioural dimensions, judge score for optimality/ui, mean of the two most
recent clean decided samples per model and task), and prints the paired table.

Written as a script rather than typed as ad-hoc SQL so the number in EVALS.md can be reproduced by
anyone, including after the arm's sample count changes.

Usage:  python3 three_arm_compare.py [db_path]
"""
import sqlite3
import sys
from math import comb
from pathlib import Path

DB = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    Path.home() / "Library/Application Support/Benchwarmer/benchwarmer.sqlite")

BASE = "claude-opus-5"
ARMS = {"caveman": "claude-opus-5-caveman", "v4": "claude-opus-5-tokendiscipline"}

GRADED = """
WITH ranked AS (
  SELECT taskId, dimension, model, status, score, steps, costUSD, totalTokens,
         ROW_NUMBER() OVER (PARTITION BY model, taskId ORDER BY createdAt DESC, runId DESC) rn
  FROM runs
  WHERE model IN (?, ?) AND status IN ('passed','failed')
    AND (scoreEligible IS NULL OR scoreEligible = 1))
SELECT taskId, model, MAX(dimension),
       AVG(CASE WHEN dimension IN ('optimality','ui')
                THEN COALESCE(score, CASE WHEN status='passed' THEN 1.0 ELSE 0.0 END)
                ELSE (status='passed') END),
       AVG(steps), AVG(costUSD), COUNT(*)
FROM ranked WHERE rn <= 2 GROUP BY taskId, model
"""


def sign_test(a: int, b: int) -> float:
    n = a + b
    if n == 0:
        return 1.0
    return min(sum(comb(n, k) for k in range(min(a, b) + 1)) / 2**n * 2, 1.0)


def compare(con: sqlite3.Connection, arm_label: str, arm_model: str) -> None:
    rows = con.execute(GRADED, (BASE, arm_model)).fetchall()
    base = {r[0]: r for r in rows if r[1] == BASE}
    arm = {r[0]: r for r in rows if r[1] == arm_model}
    shared = sorted(set(base) & set(arm))
    if not shared:
        print(f"\n{arm_label}: no paired tasks yet")
        return

    d = [(t, arm[t][3] - base[t][3]) for t in shared]
    worse = sum(1 for _, x in d if x < 0)
    better = sum(1 for _, x in d if x > 0)
    bs = sum(base[t][3] for t in shared) / len(shared)
    as_ = sum(arm[t][3] for t in shared) / len(shared)
    bc = sum(base[t][5] or 0 for t in shared)
    ac = sum(arm[t][5] or 0 for t in shared)
    bst = sum(base[t][4] or 0 for t in shared) / len(shared)
    ast = sum(arm[t][4] or 0 for t in shared) / len(shared)
    win = sum(arm[t][6] for t in shared) / len(shared)

    print(f"\n=== {arm_label} vs baseline · {len(shared)} paired tasks "
          f"· mean {win:.2f} samples/task in the {arm_label} arm ===")
    print(f"  score      {bs*100:6.1f}%  ->  {as_*100:6.1f}%   ({(as_-bs)*100:+.2f} pp)")
    print(f"  cost       ${bc:8.2f}  ->  ${ac:8.2f}   ({(ac/bc-1)*100:+.1f}%)" if bc else "")
    print(f"  steps/task {bst:6.1f}   ->  {ast:6.1f}    ({(ast/bst-1)*100:+.1f}%)" if bst else "")
    print(f"  direction  {worse} worse, {better} better, "
          f"{len(shared)-worse-better} unchanged   sign test p = {sign_test(worse, better):.4f}")

    # Where the token change came from: fewer steps, or terser output per step.
    if bst and ast and bc and ac:
        step_share = (1 - ast / bst) / (1 - ac / bc) if ac < bc else float("nan")
        print(f"  share of the cost change attributable to step count: {step_share*100:.0f}%")


def main() -> None:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    print(f"diolog-swe-bench three-arm comparison\nstore: {DB}")
    for label, model in ARMS.items():
        compare(con, label, model)
    print("\nA one-sample window is noisier per task than the two-sample window the spec requires "
          "for a rankable row. The samples/task figure above says which you are reading.")


if __name__ == "__main__":
    main()
