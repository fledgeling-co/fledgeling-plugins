#!/usr/bin/env python3
"""Fixture: a stand-in for an operator's lane command.

`lane_run.py` shells out to a command template from lanes.toml and never calls an
API itself, so its selftest needs something to shell out to. This prints a verdict
from a fixture file, with `--digest` rewriting `evidence_digest` so a test can bind
a verdict to a snapshot it just took.

    --mode verdict   print the fixture (default)
    --mode garbage   print something that is not JSON
    --mode empty     print nothing
    --mode fail      exit non-zero
    --mode slow      sleep, so a --timeout can be observed firing
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--verdict", help="fixture verdict to print")
    p.add_argument("--digest", help="overwrite evidence_digest with this value")
    p.add_argument("--lane", help="overwrite the lane id")
    p.add_argument("--model", help="the model id lane_run.py substituted")
    p.add_argument("--prompt", help="the prompt file lane_run.py substituted")
    p.add_argument("--out", help="write the verdict here instead of to stdout")
    p.add_argument("--mode", default="verdict",
                   choices=("verdict", "garbage", "empty", "fail", "slow"))
    args = p.parse_args()

    if args.mode == "garbage":
        print("thinking… I have reviewed the item and it looks fine to me")
        return 0
    if args.mode == "empty":
        return 0
    if args.mode == "fail":
        print("model unavailable", file=sys.stderr)
        return 4
    if args.mode == "slow":
        time.sleep(30)
        return 0

    if not args.verdict:
        print("--verdict is required in verdict mode", file=sys.stderr)
        return 2
    payload = json.loads(pathlib.Path(args.verdict).read_text())
    if args.digest:
        payload["evidence_digest"] = args.digest
    if args.lane:
        payload["lane"] = args.lane
    text = json.dumps(payload, indent=1, sort_keys=True)
    if args.out:
        pathlib.Path(args.out).write_text(text + "\n")
        return 0
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
