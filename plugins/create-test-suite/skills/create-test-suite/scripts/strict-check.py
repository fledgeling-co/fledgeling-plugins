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

    python3 strict-check.py <campaign-dir>
    python3 strict-check.py <campaign-dir> --set-ratchet
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

EFFECT_RUNGS = {"outcome", "metamorphic", "visual"}
RATCHET_FILE = "strict-ratchet.json"


def main() -> int:
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/test-campaign")
    cases = json.loads((d / "cases.json").read_text())
    total = len(cases)

    checked, reasons = [], Counter()
    for c in cases:
        armed = bool(c.get("armed"))
        effect = c.get("oracle") in EFFECT_RUNGS
        passing = c.get("status") == "pass"
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

    ratchet_path = d / RATCHET_FILE
    if "--set-ratchet" in sys.argv:
        ratchet_path.write_text(json.dumps({"checked": n, "total": total}, indent=1) + "\n")
        print(f"\nratchet set to {n}")
        return 0

    if not ratchet_path.exists():
        print(f"\nno ratchet recorded yet — run with --set-ratchet to pin {n}")
        return 1

    floor = json.loads(ratchet_path.read_text())["checked"]
    print(f"\nratchet: {floor}")
    if n < floor:
        print(f"FAILED — checked fell from {floor} to {n}. Something was unarmed, "
              f"dropped below an effect rung, or stopped passing.")
        return 1
    if n > floor:
        print(f"checked ROSE from {floor} to {n} — raise the ratchet with --set-ratchet "
              f"in the same commit, so it cannot fall back.")
    else:
        print("held.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
