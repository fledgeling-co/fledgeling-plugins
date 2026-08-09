#!/usr/bin/env python3
"""Tabulate an eval iteration: who asked, how long the question was, lint errors.

    python3 tabulate_run.py /tmp/clarify-evals/iteration-2
"""
import json
import pathlib
import subprocess
import sys

RUNS = pathlib.Path(sys.argv[1])
LINT = pathlib.Path(__file__).resolve().parent.parent / "skills/clarify/scripts/lint_questions.py"

rows, totals = [], {"skill": [0, 0, 0], "baseline": [0, 0, 0]}  # asked, clean, failed

for d in sorted(p for p in RUNS.iterdir() if p.is_dir()):
    for arm in ("skill", "baseline"):
        payload = d / arm / "payload.json"
        if not payload.exists():
            rows.append((d.name, arm, "no-ask", "-", "-", "-"))
            continue
        try:
            qs = json.loads(payload.read_text()).get("questions", [])
        except Exception:
            rows.append((d.name, arm, "UNPARSEABLE", "-", "-", "-"))
            continue
        nq = len(qs)
        longest = max((len(q.get("question", "").split()) for q in qs), default=0)
        longest_desc = max(
            (len(o.get("description", "").split()) for q in qs for o in q.get("options", [])),
            default=0,
        )
        out = subprocess.run(
            [sys.executable, str(LINT), str(payload)], capture_output=True, text=True
        )
        errs = sum(1 for line in out.stdout.splitlines() if line.startswith("ERROR"))
        rows.append((d.name, arm, f"asked({nq}q)", longest, longest_desc, errs))
        totals[arm][0] += 1
        totals[arm][1 if errs == 0 else 2] += 1

w = max(len(r[0]) for r in rows)
print(f"{'EVAL':<{w}}  {'ARM':<9}{'ASKED':<12}{'MAX Q WORDS':>12}{'MAX DESC':>10}{'ERRORS':>8}")
for name, arm, asked, qw, dw, e in rows:
    print(f"{name:<{w}}  {arm:<9}{asked:<12}{str(qw):>12}{str(dw):>10}{str(e):>8}")

print()
for arm, (asked, clean, failed) in totals.items():
    print(f"{arm:<9} asked {asked}  lint-clean {clean}  lint-fail {failed}")
