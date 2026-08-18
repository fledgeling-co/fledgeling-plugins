#!/usr/bin/env python3
"""Decide which column a card may reach, from the warrant's own state.

Done is what an out-of-family verdict grants. Whether a card may go further is a
question about *authority* rather than about the card, and the `warrant` plugin is
where that authority is written down and revoked. This script reads its state and
returns the column.

It reads `.warrant/` in the target repository rather than importing warrant's
code. Two separately installed plugins cannot resolve each other's paths, and the
state files are in the repo under verification anyway, so this needs nothing but
stdlib.

    warrant_column.py --warrant-root <repo> --class <defect-class>
    warrant_column.py --warrant-root <repo> --class <c> --card-gate-failed 'tick_and_tie: rev-q2'
    warrant_column.py --warrant-root <repo> --class <c> --verdict inconclusive

Exit codes are the answer:

    0  Verified is permitted for this card
    1  could not run: bad usage, unreadable state
    2  Needs More Work — a gate on this card's own evidence failed
    3  Done at most — the authority is not there, and the reasons are named
    4  the card does not move — the verdict was inconclusive, which blocks

The substitution this rests on is printed on every grant rather than assumed. The
warrant's tier ladder is climbed on absence of escapes, not on a measured
sensitivity, because no powered non-inferiority reader study exists for code or UI
review. A signed warrant is a person accepting that substitution in advance; it is
not the study. Saying so on every promotion is the only thing that stops a tier
reading as a measurement later.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import tomllib

VERIFIED, CANNOT_RUN, NEEDS_MORE_WORK, DONE_AT_MOST, NO_MOVE = 0, 1, 2, 3, 4

# The tier at which the warrant's strongest evidence exists. Below this, a class
# has authority to close an item (Done) but not to stand in for the human column.
VERIFIED_TIER = 3


def _read_toml(path: pathlib.Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _read_json(path: pathlib.Path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default


def assess(root: pathlib.Path, klass: str) -> tuple[int, list[str], dict]:
    """Return (exit code, reasons, detail). Reasons are what to write on the card."""
    d = root / ".warrant"
    reasons: list[str] = []
    detail: dict = {"class": klass, "warrant_root": str(root)}

    warrant_path = d / "warrant.toml"
    if not warrant_path.exists():
        return DONE_AT_MOST, [
            f"no signed warrant at {warrant_path}: without one no class has authority "
            "beyond advisory, so Done is the furthest this card goes",
            "run warrant:charter to draft and sign one",
        ], detail

    warrant = _read_toml(warrant_path)
    detail["warrant_version"] = warrant.get("version")

    owner = warrant.get("owner", {}) or {}
    if not (owner.get("name") or "").strip():
        reasons.append("the warrant names no owner, so nobody is answerable for the policy "
                       "this promotion would rest on")

    entry = next((c for c in warrant.get("classes", [])
                  if isinstance(c, dict) and c.get("name") == klass), None)
    if entry is None:
        return DONE_AT_MOST, [
            f"the warrant does not name the class {klass!r}, and an unnamed class holds "
            "tier 0 by default — a class nobody wrote down is a class no machine may close",
        ], detail

    if entry.get("census"):
        return DONE_AT_MOST, [
            f"{klass!r} is a census class: every item in it is reviewed by a person, so it "
            "has no machine path past Done",
        ], detail

    held = int(entry.get("tier", 0) or 0)
    detail["tier_held"] = held

    # ratchet's own last word, where it has run. Its report carries the earned tier
    # and any revocation, and a revocation is disqualifying whatever the warrant says.
    report = None
    for candidate in sorted((d / "reports").glob("*ratchet*.json"), reverse=True):
        report = _read_json(candidate)
        if report:
            detail["ratchet_report"] = candidate.name
            break

    earned = held
    if report:
        block = (report.get("classes") or {}).get(klass) or {}
        if "earned_tier" in block:
            earned = int(block["earned_tier"])
        for trigger in block.get("triggers", []):
            reasons.append(f"ratchet trigger {trigger.get('trigger')}: {trigger.get('reason')}")
        for blocker in block.get("blockers", []):
            reasons.append(f"blocker: {blocker}")
    else:
        reasons.append("no ratchet report found, so the tier in the warrant has not been "
                       "checked against current evidence; run warrant:ratchet")
    detail["tier_earned"] = earned

    if earned < VERIFIED_TIER:
        reasons.insert(0, f"{klass!r} holds tier {held} and has earned tier {earned}; "
                          f"Verified needs tier {VERIFIED_TIER}, which is the strongest "
                          f"evidence the warrant can produce")
        return DONE_AT_MOST, reasons, detail

    if reasons:
        return DONE_AT_MOST, reasons, detail

    return VERIFIED, [
        f"{klass!r} holds tier {earned} under warrant version "
        f"{warrant.get('version')}, owned by {owner.get('name')}",
        "SUBSTITUTION, recorded on every promotion: this tier was earned by absence of "
        "escapes over a declared window, not by a measured non-inferiority study. No such "
        "study exists for code or UI review. The signed warrant is a person accepting that "
        "substitution in advance, and it is not the study.",
    ], detail


def selftest() -> int:
    """Every path is observed both granting and refusing.

    A gate only ever seen refusing is as unwritten as one only ever seen passing:
    the six cases below are the ones that decide whether a card can leave Done.
    """
    import tempfile
    cases: list[tuple[str, bool]] = []

    def repo(tier: int = 3, census: bool = False, owner: str = "Luke Rhodes",
             named: bool = True, report: dict | None = None) -> pathlib.Path:
        d = pathlib.Path(tempfile.mkdtemp()) / "r"
        (d / ".warrant" / "reports").mkdir(parents=True)
        cls = (f'[[classes]]\nname = "figure-lineage"\ntier = {tier}\n'
               f'census = {"true" if census else "false"}\n') if named else ""
        (d / ".warrant" / "warrant.toml").write_text(
            f'version = "3"\n[owner]\nname = "{owner}"\nemail = "l@r.gg"\n' + cls)
        if report is not None:
            (d / ".warrant" / "reports" / "r-ratchet.json").write_text(json.dumps(report))
        return d

    clean = {"classes": {"figure-lineage": {"earned_tier": 3, "triggers": [], "blockers": []}}}

    code, _, _ = assess(pathlib.Path(tempfile.mkdtemp()), "figure-lineage")
    cases.append(("no warrant refuses", code == DONE_AT_MOST))

    code, _, _ = assess(repo(report=clean), "figure-lineage")
    cases.append(("tier 3, ratchet clean, grants", code == VERIFIED))

    code, _, _ = assess(repo(tier=3), "figure-lineage")
    cases.append(("no ratchet report refuses", code == DONE_AT_MOST))

    low = {"classes": {"figure-lineage": {"earned_tier": 2, "triggers": [], "blockers": ["x"]}}}
    code, _, _ = assess(repo(report=low), "figure-lineage")
    cases.append(("earned below tier 3 refuses", code == DONE_AT_MOST))

    fired = {"classes": {"figure-lineage": {"earned_tier": 3, "blockers": [],
             "triggers": [{"trigger": "model_drift", "reason": "moved"}]}}}
    code, _, _ = assess(repo(report=fired), "figure-lineage")
    cases.append(("a revocation refuses even at tier 3", code == DONE_AT_MOST))

    code, _, _ = assess(repo(census=True, report=clean), "figure-lineage")
    cases.append(("a census class refuses", code == DONE_AT_MOST))

    code, _, _ = assess(repo(report=clean), "unnamed-class")
    cases.append(("a class the warrant does not name refuses", code == DONE_AT_MOST))

    code, _, _ = assess(repo(owner="", report=clean), "figure-lineage")
    cases.append(("an unowned warrant refuses", code == DONE_AT_MOST))

    _, reasons, _ = assess(repo(report=clean), "figure-lineage")
    cases.append(("a grant states the substitution",
                  any("SUBSTITUTION" in r for r in reasons)))

    width = max(len(n) for n, _ in cases)
    bad = 0
    for name, ok in cases:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:<{width}}")
        bad += 0 if ok else 1
    print(f"{len(cases)} case(s), {bad} failure(s)")
    return 0 if bad == 0 else 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--warrant-root",
                   help="the repository holding .warrant/")
    p.add_argument("--class", dest="klass",
                   help="the defect class this card falls in")
    p.add_argument("--verdict", choices=("pass", "fail", "inconclusive"),
                   help="the out-of-family verdict on this card, where one exists")
    p.add_argument("--card-gate-failed", action="append", default=[],
                   help="a warrant gate that failed on this card's own evidence; repeatable")
    p.add_argument("--json", action="store_true")
    p.add_argument("--selftest", action="store_true",
                   help="run this script's own cases; every path observed both ways")
    a = p.parse_args()

    if a.selftest:
        return selftest()

    if not a.warrant_root or not a.klass:
        p.error("--warrant-root and --class are required unless --selftest is given")
    root = pathlib.Path(a.warrant_root).expanduser().resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return CANNOT_RUN

    # A failed gate on this card's own evidence is about the card, and it outranks
    # every question about authority: there is nothing to promote.
    if a.card_gate_failed:
        column, reasons = "Needs More Work", [
            "a warrant gate failed on this card's own evidence: "
            + "; ".join(a.card_gate_failed)]
        code = NEEDS_MORE_WORK
    elif a.verdict == "inconclusive":
        column, reasons = "no move", [
            "the verdict is inconclusive, which is a valid terminal result and blocks. "
            "It never rounds up to a pass; the card stays where it is with the reason "
            "and what would settle it recorded",
        ]
        code = NO_MOVE
    elif a.verdict == "fail":
        column, reasons = "Needs More Work", ["the out-of-family verdict is fail"]
        code = NEEDS_MORE_WORK
    else:
        code, reasons, detail = assess(root, a.klass)
        column = {VERIFIED: "Verified", DONE_AT_MOST: "Done"}.get(code, "Done")
        if a.json:
            json.dump({"column": column, "exit": code, "reasons": reasons, **detail},
                      sys.stdout, indent=1)
            sys.stdout.write("\n")
        else:
            print(f"column: {column}")
            for r in reasons:
                print(f"  - {r}")
        return code

    if a.json:
        json.dump({"column": column, "exit": code, "reasons": reasons},
                  sys.stdout, indent=1)
        sys.stdout.write("\n")
    else:
        print(f"column: {column}")
        for r in reasons:
            print(f"  - {r}")
    return code


if __name__ == "__main__":
    sys.exit(main())
