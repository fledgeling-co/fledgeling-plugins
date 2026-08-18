#!/usr/bin/env python3
"""A stand-in verdict source for regress_run.py's selftest.

regress_run.py never calls a model. It shells out to a command that receives a
case directory and prints a verdict JSON on stdout, so the fixture that proves
the script works is a script rather than a recorded model response.

    verdict_source.py --mode catch|miss|garbage|crash|unnamed|slow [--miss-case ID] CASE_DIR

catch    print the verdict the case says should have been returned
miss     print `pass`, which is what the pipeline did when the escape happened
garbage  print something that is not JSON
crash    exit non-zero without printing a verdict
unnamed  print the right verdict without naming the class it was for
slow     never answer inside a sane timeout
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--mode", default="catch",
                   choices=["catch", "miss", "garbage", "crash", "unnamed", "slow"])
    p.add_argument("--miss-case", action="append", default=[],
                   help="only these case ids are missed; others are caught")
    p.add_argument("case_dir")
    args = p.parse_args(argv)

    case_path = pathlib.Path(args.case_dir) / "case.json"
    case = json.loads(case_path.read_text())
    expected = case.get("expected_verdict", {})
    mode = args.mode
    if args.miss_case and case.get("case_id") not in args.miss_case:
        mode = "catch"

    if mode == "crash":
        print(f"verdict source refused {case.get('case_id')}", file=sys.stderr)
        return 3
    if mode == "slow":
        time.sleep(30)
        return 0
    if mode == "garbage":
        sys.stdout.write("no verdict here, just a banner\n")
        return 0
    if mode == "miss":
        json.dump({"verdict": "pass", "summary": "nothing found"}, sys.stdout)
        return 0
    if mode == "unnamed":
        json.dump({"verdict": expected.get("verdict", "fail"),
                   "summary": "something is wrong but I will not say what"}, sys.stdout)
        return 0

    json.dump({"verdict": expected.get("verdict", "fail"),
               "defect_class": expected.get("defect_class"),
               "summary": f"re-caught {case.get('case_id')}"}, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
