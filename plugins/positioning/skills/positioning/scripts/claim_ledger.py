#!/usr/bin/env python3
"""Claim ledger for the positioning skill.

Holds three tables and the bindings between them:

  truth      what the product actually does, and whether it ships today
  claims     what the research established, and how independently
  bindings   which territory move rests on which truth rows and claims

`check` turns the skill's honesty rules into an exit code. Prose asks; this
refuses. Every rule it enforces exists because the prose version of it was
already in the predecessor skill and could still be walked past.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

LEDGER = "ledger.json"

TRUTH_STATUS = ("shipped", "designed", "aspirational")
CONFIDENCE = ("high", "medium", "low")

# Moves whose copy a prospect reads as a present-tense promise. A move in this
# set may not rest on a truth row that is not shipped.
PROMISSORY_MOVES = ("hero", "headline", "one_liner", "value_proof", "unique_attributes")

# Support floor per confidence label, counted in distinct registrable domains.
DOMAIN_FLOOR = {"high": 3, "medium": 2, "low": 1}

MULTI_PART_TLDS = {
    "co.uk", "org.uk", "ac.uk", "gov.uk", "co.nz", "co.jp", "co.za",
    "com.au", "net.au", "org.au", "edu.au", "gov.au", "com.br", "co.in",
}


def registrable_domain(url: str) -> str | None:
    """Registrable domain of a URL, so two pages on one site count once."""
    try:
        host = (urlparse(url).hostname or "").lower().strip(".")
    except ValueError:
        return None
    if not host:
        return None
    if host.replace(".", "").isdigit():
        return host
    parts = host.split(".")
    if len(parts) < 2:
        return host
    if ".".join(parts[-2:]) in MULTI_PART_TLDS and len(parts) >= 3:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def load(workdir: Path) -> dict:
    path = workdir / LEDGER
    if not path.exists():
        sys.exit(f"no ledger at {path}. Run: claim_ledger.py init {workdir}")
    return json.loads(path.read_text())


def save(workdir: Path, data: dict) -> None:
    (workdir / LEDGER).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def cmd_init(args) -> int:
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    # Make the whole output layout exist from the first command, so a later phase
    # never has to decide where its files go. A run that scatters its output
    # across the working root leaves the next run unable to find it.
    made = []
    if workdir.name == "work":
        for sibling in ("research",):
            d = workdir.parent / sibling
            if not d.exists():
                d.mkdir(parents=True, exist_ok=True)
                made.append(d.as_posix())

    path = workdir / LEDGER
    if path.exists() and not args.force:
        print(f"ledger already at {path}; pass --force to overwrite")
        return 0
    save(workdir, {"product": args.product, "truth": [], "claims": [], "bindings": []})
    print(f"ledger initialised at {path}")
    if made:
        print("created: " + ", ".join(made))
    print(f"reports go to {workdir.parent.as_posix()}/, "
          f"research exports to {workdir.parent.as_posix()}/research/")
    return 0


def cmd_add_truth(args) -> int:
    workdir = Path(args.workdir)
    data = load(workdir)
    if any(t["id"] == args.id for t in data["truth"]):
        sys.exit(f"truth id {args.id} already used")
    data["truth"].append({
        "id": args.id,
        "capability": args.capability,
        "status": args.status,
        "evidence": args.evidence,
    })
    save(workdir, data)
    print(f"truth {args.id} recorded as {args.status}")
    return 0


def cmd_add_claim(args) -> int:
    workdir = Path(args.workdir)
    data = load(workdir)
    if any(c["id"] == args.id for c in data["claims"]):
        sys.exit(f"claim id {args.id} already used")
    data["claims"].append({
        "id": args.id,
        "text": args.text,
        "confidence": args.confidence,
        "sources": args.source or [],
        "panel_members": args.member or [],
        "citations_verified": bool(args.verified),
        "contested": bool(args.contested),
    })
    save(workdir, data)
    print(f"claim {args.id} recorded at {args.confidence} confidence")
    return 0


def cmd_bind(args) -> int:
    workdir = Path(args.workdir)
    data = load(workdir)
    known_truth = {t["id"] for t in data["truth"]}
    known_claims = {c["id"] for c in data["claims"]}
    for t in args.truth or []:
        if t not in known_truth:
            sys.exit(f"unknown truth id: {t}")
    for c in args.claim or []:
        if c not in known_claims:
            sys.exit(f"unknown claim id: {c}")
    data["bindings"].append({
        "territory": args.territory,
        "move": args.move,
        "truth": args.truth or [],
        "claims": args.claim or [],
        "text": args.text or "",
    })
    save(workdir, data)
    print(f"bound {args.territory}/{args.move}")
    return 0


# The evidence tier a run is claiming. A desk-research run with no field test
# earns "promising-hypothesis" and should not be reported as a broken build: the
# absence of verified evidence is what that label MEANS. What never softens is
# promising capability that has not shipped, which is a claim about the product
# rather than about the evidence, and is wrong at every tier.
LABELS = ("recommended", "conditionally-recommended", "promising-hypothesis")
SOFTENED_BY_LABEL = {
    "recommended": (),
    "conditionally-recommended": ("unverified",),
    "promising-hypothesis": ("unverified", "domain-floor"),
}


def cmd_check(args) -> int:
    workdir = Path(args.workdir)
    data = load(workdir)
    truth = {t["id"]: t for t in data["truth"]}
    claims = {c["id"]: c for c in data["claims"]}
    errors: list[str] = []
    warnings: list[str] = []
    softened = set(SOFTENED_BY_LABEL[args.label])
    downgraded = 0

    def record(kind: str, msg: str) -> None:
        nonlocal downgraded
        if kind in softened:
            warnings.append(f"{msg}  [expected at label '{args.label}']")
            downgraded += 1
        else:
            errors.append(msg)

    if not data["truth"]:
        errors.append("product-truth table is empty: nothing to bind a claim to")
    if not data["claims"]:
        errors.append("claim table is empty: no research has entered the ledger")

    # Rule 1 — every required move on every territory is bound.
    required = set(args.require_move or [])
    territories = sorted({b["territory"] for b in data["bindings"]})
    if not territories:
        errors.append("no bindings: no territory move rests on anything")
    for terr in territories:
        bound = {b["move"] for b in data["bindings"] if b["territory"] == terr}
        for move in sorted(required - bound):
            errors.append(f"{terr}: move '{move}' is unbound")

    for b in data["bindings"]:
        where = f"{b['territory']}/{b['move']}"

        # Rule 2 — every move rests on at least one claim and one truth row.
        if not b["claims"]:
            errors.append(f"{where}: rests on no research claim")
        if not b["truth"]:
            errors.append(f"{where}: rests on no product-truth row")

        # Rule 3 — a promissory move may not rest on unshipped capability.
        if b["move"] in PROMISSORY_MOVES:
            for tid in b["truth"]:
                status = truth[tid]["status"]
                if status != "shipped":
                    errors.append(
                        f"{where}: promissory copy rests on {tid}, which is "
                        f"'{status}' rather than shipped"
                    )

        # Rule 4 — a move may not rest on a claim whose citations never resolved.
        for cid in b["claims"]:
            if not claims[cid]["citations_verified"]:
                record("unverified",
                       f"{where}: rests on {cid}, whose citations are unverified")
            if claims[cid]["contested"] and b["move"] in PROMISSORY_MOVES:
                warnings.append(
                    f"{where}: promissory copy rests on {cid}, recorded as contested"
                )

    # Rule 5 — a confidence label must be earned in independent domains.
    for cid, c in sorted(claims.items()):
        domains = {d for d in (registrable_domain(s) for s in c["sources"]) if d}
        floor = DOMAIN_FLOOR[c["confidence"]]
        if len(domains) < floor:
            record("domain-floor",
                   f"{cid}: labelled {c['confidence']} confidence on "
                   f"{len(domains)} independent domain(s); floor is {floor}")
        if len(c["sources"]) > len(domains) and args.verbose:
            warnings.append(
                f"{cid}: {len(c['sources'])} sources collapse to {len(domains)} domains"
            )

    used_claims = {c for b in data["bindings"] for c in b["claims"]}
    orphans = sorted(set(claims) - used_claims)

    print(f"label: {args.label} · territories: {len(territories)} · "
          f"bindings: {len(data['bindings'])} · claims: {len(claims)} · "
          f"truth rows: {len(truth)}")
    print(f"claims bound to a move: {len(used_claims)}/{len(claims)}"
          + (f" · unused: {', '.join(orphans)}" if orphans and args.verbose else ""))
    for w in warnings:
        print(f"  warn  {w}")
    for e in errors:
        print(f"  FAIL  {e}")
    if errors:
        print(f"\n{len(errors)} error(s). The ledger does not support the "
              f"recommendation at label '{args.label}'.")
        return 1
    if downgraded:
        print(f"\n0 errors, {downgraded} finding(s) expected at label "
              f"'{args.label}'. Every promissory move rests on shipped capability; "
              f"the evidence is not field-verified, which is what this label says.")
    else:
        print("\n0 errors. Every move rests on verified evidence and shipped "
              "capability.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("workdir")
    p.add_argument("--product", default=""); p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add-truth"); p.add_argument("workdir")
    p.add_argument("--id", required=True); p.add_argument("--capability", required=True)
    p.add_argument("--status", required=True, choices=TRUTH_STATUS)
    p.add_argument("--evidence", default="")
    p.set_defaults(func=cmd_add_truth)

    p = sub.add_parser("add-claim"); p.add_argument("workdir")
    p.add_argument("--id", required=True); p.add_argument("--text", required=True)
    p.add_argument("--confidence", required=True, choices=CONFIDENCE)
    p.add_argument("--source", action="append"); p.add_argument("--member", action="append")
    p.add_argument("--verified", action="store_true"); p.add_argument("--contested", action="store_true")
    p.set_defaults(func=cmd_add_claim)

    p = sub.add_parser("bind"); p.add_argument("workdir")
    p.add_argument("--territory", required=True); p.add_argument("--move", required=True)
    p.add_argument("--truth", action="append"); p.add_argument("--claim", action="append")
    p.add_argument("--text", default="")
    p.set_defaults(func=cmd_bind)

    p = sub.add_parser("check"); p.add_argument("workdir")
    p.add_argument("--require-move", action="append",
                   help="a move every territory must bind; repeatable")
    p.add_argument("--label", default="recommended", choices=LABELS,
                   help="the evidence tier being claimed. Lower tiers expect "
                        "unverified evidence and report it as such; promising "
                        "unshipped capability fails at every tier.")
    p.add_argument("--verbose", action="store_true")
    p.set_defaults(func=cmd_check)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
