#!/usr/bin/env python3
"""Turn captured pairs into a be-my-witness worklist, and count what cannot be judged.

WHY THIS SITS BETWEEN THE TWO SKILLS
------------------------------------
`be-my-witness` judges ONE screenshot against ONE reference. A campaign has
dozens of surfaces, and the failure mode is not a bad verdict — it is a surface
that was never submitted for one, which then reads as covered because nothing in
the report distinguishes "compared and fine" from "never compared".

So this reads `pairs.json` and produces two things: a worklist of pairs that CAN
be judged, and an explicit list of surfaces that cannot, each with the reason it
has no design of record. The second list is the one that matters — it is the part
a reader would otherwise assume away.

    python3 witness-worklist.py <campaign-dir> [--pairs evidence/shots/pairs.json]

The worklist is JSON so the caller can drive be-my-witness per pair:

    python3 <be-my-witness>/scripts/prescan.py <shot> --reference <reference> --json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    d = Path(args[0])
    rel = args[args.index("--pairs") + 1] if "--pairs" in args else "evidence/shots/pairs.json"
    pairs_path = d / rel

    # Merge every worker's file. A single pairs.json cannot survive a worker
    # recycle — Playwright restarts a worker after a failing test, so the last
    # writer clobbers the rest. Measured: 61 captures produced a pairs.json with
    # one entry in it. The template writes pairs-<pid>.json; this joins them.
    shards = sorted(pairs_path.parent.glob("pairs-*.json")) if pairs_path.parent.exists() else []
    if shards:
        merged = []
        for sh in shards:
            try:
                merged += json.loads(sh.read_text())
            except (ValueError, OSError):
                print(f"   ! unreadable shard: {sh.name}")
        by_surface = {p.get("surface"): p for p in merged}
        pairs_path.write_text(json.dumps(list(by_surface.values()), indent=1) + "\n")
        print(f"merged {len(shards)} worker file(s) -> {len(by_surface)} unique surfaces")

    if not pairs_path.exists():
        print(f"no pairs at {pairs_path}.")
        print("Nothing has been captured for comparison, so NO surface in this campaign has")
        print("been judged against its design of record. That is a coverage gap, not a clean")
        print("result — capture with assets/capture-pairs.template.mjs first.")
        return 1

    pairs = json.loads(pairs_path.read_text())
    judgeable = [p for p in pairs if p.get("reference")]
    blind = [p for p in pairs if not p.get("reference")]

    print(f"pairs={len(pairs)}  judgeable={len(judgeable)}  WITHOUT a reference={len(blind)}")
    if pairs:
        print(f"comparable fraction: {100 * len(judgeable) / len(pairs):.0f}%")

    # Conditions travel with the verdict: a comparison whose viewport and settle
    # are unknown cannot be reproduced, and an irreproducible verdict is an opinion.
    conditions = {(p.get("viewport", {}).get("width"), p.get("viewport", {}).get("height"),
                   p.get("settleMs")) for p in pairs}
    if len(conditions) > 1:
        print("\nWARNING — pairs were captured under DIFFERENT conditions:")
        for c in sorted(conditions, key=lambda x: str(x)):
            print(f"   viewport={c[0]}x{c[1]} settle={c[2]}ms")
        print("Differences produced by the capture will be reported as design drift.")

    if blind:
        print("\nSURFACES THAT CANNOT BE JUDGED — no design of record:")
        for p in blind:
            print(f"   {p.get('surface', '?'):<12} {p.get('name', '')} — {p.get('reason', 'no reason recorded')}")

    out = d / "witness-worklist.json"
    out.write_text(json.dumps(judgeable, indent=1) + "\n")
    print(f"\nwrote {out} ({len(judgeable)} pair(s) to judge)")
    print("A pair with reference:null is an UNCOMPARED surface. It is not a pass.")
    return 0 if judgeable and not blind else 1


if __name__ == "__main__":
    raise SystemExit(main())
