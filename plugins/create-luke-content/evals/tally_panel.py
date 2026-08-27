#!/usr/bin/env python3
"""
tally_panel.py — Un-blind and tally the panel results.
"""

import collections
import json
import os
import pathlib
import re

BASE_DIR = pathlib.Path("/tmp/luke-evals")
MAP_FILE = BASE_DIR / "unblinding-map.json"
VERDICTS_DIR = BASE_DIR / "verdicts"

if not MAP_FILE.exists():
    print("unblinding-map.json does not exist yet")
    exit(1)

MAP = json.load(open(MAP_FILE))["map"]
LANES = {
    "codex": "OpenAI (gpt-5.6-sol)",
    "grok": "xAI (grok-4.6)",
    "fable": "Claude (claude-fable-5)"
}

def parse_verdict(path):
    if not os.path.exists(path):
        return None, "not run"
    t = open(path, encoding="utf-8", errors="replace").read().strip()
    if not t:
        return None, "empty output"
    m = re.findall(r"^\s*OVERALL:\s*\**\s*(A|B|TIE)\b", t, re.M | re.I)
    if not m:
        # Check if OVERALL appears anywhere
        m2 = re.findall(r"OVERALL:\s*\[?(A|B|TIE)\]?", t, re.I)
        if m2:
            return m2[-1].upper(), "ok (inline)"
        return None, "no OVERALL line"
    return m[-1].upper(), "ok"

def main():
    rows = []
    tally = collections.Counter()
    lane_tally = collections.defaultdict(collections.Counter)

    for eid_str in sorted(MAP.keys(), key=lambda x: int(x)):
        eid = int(eid_str)
        row = {"eval": eid}
        for lane in LANES:
            v_path = VERDICTS_DIR / f"{eid}.{lane}.md"
            v, status = parse_verdict(v_path)
            if v is None:
                row[lane] = f"-- ({status})"
                lane_tally[lane]["no_verdict"] += 1
            else:
                arm = MAP[eid_str][v] if v in ("A", "B") else "tie"
                row[lane] = f"{v} -> {arm}"
                lane_tally[lane][arm] += 1
                tally[arm] += 1
        rows.append(row)

    print("\n=== UN-BLINDED PANEL RESULTS ===")
    print(f"{'Eval':<8} {'OpenAI (gpt-5.6-sol)':<25} {'xAI (grok-4.6)':<25} {'Claude (fable-5)':<25}")
    print("-" * 85)
    for r in rows:
        print(f"{r['eval']:<8} {r.get('codex','--'):<25} {r.get('grok','--'):<25} {r.get('fable','--'):<25}")

    print("\n=== SUMMARY TALLY ===")
    print(f"Candidate wins:   {tally['candidate']}")
    print(f"Predecessor wins: {tally['predecessor']}")
    print(f"Ties:             {tally['tie']}")

    print("\nPer-lane breakdown:")
    for lane, name in LANES.items():
        print(f"  {name}: {dict(lane_tally[lane])}")

if __name__ == "__main__":
    main()
