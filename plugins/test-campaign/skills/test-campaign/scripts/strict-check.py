#!/usr/bin/env python3
"""The stricter gate: if it hasn't been checked, it has failed.

WHY THIS EXISTS ALONGSIDE `campaign.py check`
---------------------------------------------
The campaign's own gate asks whether every case is accounted for — nothing open,
every surface covered, every critical flow above presence. That is a real bar and
it passes. It is not the same question as "has this actually been checked".

A case counts as CHECKED here only if both are true:

  1. It was watched to fail.   An assertion nobody has seen go red is
     indistinguishable from one that cannot go red. A smoke alarm is quiet in a
     house that isn't burning and quiet with a flat battery.
  2. It asserts an effect.     presence and structural rungs prove something was
     rendered, not that the product did what it promised. The campaign exists
     because a suite of 524 assertions stayed green for months over tenants that
     shipped with no header, no navigation and no footer.

Everything else — an unarmed pass, a skip, an n/a, a fail — is unchecked, and
unchecked is failed.

THE RATCHET
-----------
A gate that is 97% red on day one gets switched off by the end of the week, and a
switched-off gate checks nothing. So this reports the honest number and enforces
only that it never goes DOWN. The bar rises as the suite earns it, and a change
that quietly unarms a case or drops it to presence fails immediately.

Lowering the ratchet therefore needs a reason, recorded in the file. There is
exactly one good one, and it is not "the gate was inconvenient": the definition
of checked got stricter, so the old number was measuring something laxer. That
happened once already — `visual` used to buy effect credit, which let a case
asserting `card.title == "AGGREGATE CPU"` count as visual proof, and a campaign
reach 100% while no window had ever been drawn. Splitting it into
`structural-visual` and `raster-visual` made those scores fall. The fall was the
correction.

    python3 strict-check.py <campaign-dir>
    python3 strict-check.py <campaign-dir> --set-ratchet
    python3 strict-check.py <campaign-dir> --set-ratchet --reason "..."
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# Only these assert an effect. `visual` is deliberately absent: it covered both
# "a label exists in the view hierarchy" and "pixels were captured off a display
# server", and the first of those is a data-model check. See campaign.py.
# `effect-witness` was added to campaign.py in 0.9.0 and never added here, so the
# rung that most strongly proves an effect — a recorder outside the product saw it
# — scored as "only proves something rendered", the weakest bucket on the page.
# A campaign that built a real witness watched its strict score stay flat, which
# is precisely the wrong incentive to attach to the most expensive rung.
EFFECT_RUNGS = {"outcome", "metamorphic", "effect-witness",
                "raster-visual", "interactive-glass"}
LEGACY_RUNGS = {"visual"}
RATCHET_FILE = "strict-ratchet.json"


def main() -> int:
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/test-campaign")
    cases = json.loads((d / "cases.json").read_text())
    total = len(cases)
    if not total:
        print("No cases. An empty campaign is not a passing one.")
        return 1

    checked, reasons = [], Counter()
    legacy = []
    for c in cases:
        armed = bool(c.get("armed"))
        effect = c.get("oracle") in EFFECT_RUNGS
        passing = c.get("status") == "pass"
        if c.get("oracle") in LEGACY_RUNGS:
            legacy.append(c.get("id", "?"))
        if passing and armed and effect:
            checked.append(c)
        elif not passing:
            reasons[f"status is {str(c.get('status', '?')).split(':')[0]}"] += 1
        elif not armed and not effect:
            reasons["never watched to fail, and only proves something rendered"] += 1
        elif not armed:
            reasons["never watched to fail"] += 1
        else:
            reasons["only proves something rendered"] += 1

    n = len(checked)
    print(f"CHECKED   {n} of {total} cases ({100 * n / total:.0f}%)")
    print(f"UNCHECKED {total - n}  — and unchecked is failed\n")
    for reason, count in reasons.most_common():
        print(f"  {count:>4}  {reason}")
    if legacy:
        print(f"\n  {len(legacy):>4}  on the legacy `visual` rung, which buys no effect "
              f"credit: {', '.join(legacy[:8])}")

    ratchet_path = d / RATCHET_FILE
    prior = json.loads(ratchet_path.read_text()) if ratchet_path.exists() else None

    if "--set-ratchet" in sys.argv:
        reason = ""
        if "--reason" in sys.argv:
            i = sys.argv.index("--reason")
            reason = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
        if prior and n < prior["checked"] and not reason:
            print(f"\nREFUSED — that would lower the ratchet from {prior['checked']} to "
                  f"{n} with no reason recorded. Lowering it is sometimes right, and it "
                  f"is never routine: pass --reason \"...\" and it goes in the file, so "
                  f"the next reader sees why the bar moved rather than finding a bar "
                  f"that quietly drops whenever it is inconvenient.")
            return 1
        record = {"checked": n, "total": total,
                  "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        if reason:
            record["loweredBecause" if prior and n < prior["checked"] else "reason"] = reason
        if prior:
            record["previous"] = prior["checked"]
        ratchet_path.write_text(json.dumps(record, indent=1) + "\n")
        print(f"\nratchet set to {n}"
              + (f" (was {prior['checked']})" if prior else "")
              + (f" — {reason}" if reason else ""))
        return 0

    if not prior:
        print(f"\nno ratchet recorded yet — run with --set-ratchet to pin {n}")
        return 1

    floor = prior["checked"]
    print(f"\nratchet: {floor}"
          + (f" — lowered on {prior.get('at', '?')}: {prior['loweredBecause']}"
             if prior.get("loweredBecause") else ""))
    if n < floor:
        print(f"FAILED — checked fell from {floor} to {n}. Something was unarmed, "
              f"dropped below an effect rung, or stopped passing.")
        if legacy:
            print(f"  {len(legacy)} case(s) sit on the legacy `visual` rung. If this fall "
                  f"is the rung split rather than a regression, re-pin with "
                  f"--set-ratchet --reason and say so.")
        return 1
    if n > floor:
        print(f"checked ROSE from {floor} to {n} — raise the ratchet with --set-ratchet "
              f"in the same commit, so it cannot fall back.")
    else:
        print("held.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
