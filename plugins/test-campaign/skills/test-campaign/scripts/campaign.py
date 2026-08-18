#!/usr/bin/env python3
"""
campaign.py — the case registry, and the gate that reads it.

A UI test campaign has two silent failure modes, and they are the same two a
design review has: covering a subset of the surfaces, and running a subset of
the checks. Both produce a report indistinguishable from a finished one — same
headings, same verdict line, and the reader cannot tell.

So the campaign's unit is a CASE with a stable id, every case resolves, and
`check` refuses to clear while one is open. Four rules are enforced here rather
than trusted:

  1. Every surface carries at least one case. A surface with none is unaudited,
     and an unaudited surface that never appears in the report reads as covered.
  2. A case resolves to pass / fail / skip:<reason> / n/a:<reason>. Anything
     unrecognised counts as OPEN, deliberately: an ambiguous cell is not
     evidence that the work happened.
  3. A PASS names at least one evidence artifact on disk. No artifact, no
     verdict — a verdict you reached by looking is not a measurement.
  4. Armed and unarmed passes are counted separately. An assertion nobody has
     watched fail is not known to bite, and a suite that reports one number for
     both is claiming a uniformity it has not measured.

Ids are stable and referenceable, because the evidence page, the report and a
later conversation all need to point at the same thing: SURF-001, FLOW-001.03,
CMP-001, CASE-0001, DEF-001.

Usage:
    campaign.py init   <dir> --project NAME --lanes web,macos [--sample "..."]
    campaign.py add    <dir> --kind surface --file surfaces.json
    campaign.py add    <dir> --kind case    --file cases.json
    campaign.py set    <dir> --case CASE-0007 --status pass \\
                             --evidence evidence/shots/dash.png --armed
    campaign.py check  <dir> [--json]
    campaign.py report <dir> [--json]

State lives in <dir>/campaign.json (facts), inventory.json (what exists) and
cases.json (what was checked). ledger.md is generated from them for a human.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

KINDS = {"requirement": "REQ", "surface": "SURF", "flow": "FLOW", "component": "CMP",
         "case": "CASE", "defect": "DEF"}
WIDTH = {"REQ": 3, "SURF": 3, "FLOW": 3, "CMP": 3, "CASE": 4, "DEF": 3}

RESOLVED = ("pass", "fail")
# unselected is its own state and not a kind of skip. A skip says this case
# should not run; unselected says it did not run *this time* and its previous
# verdict is being carried forward. Folding them together loses the only two
# facts that make a selective run honest: what the selection was based on, and
# how old the carried result is. See references/selection.md.
REASONED = ("skip", "n/a", "unselected")
CARRIED = "unselected"

# What a case actually checks, weakest first. The rung is a field rather than a
# judgement because UI suites execute behaviour far more often than they assert
# it — inferred metamorphic relations across 214 components were exercised at
# high rates and explicitly validated only 42.5%-47.6% of the time. A plan can
# therefore look complete while proving very little, and no count of tests shows
# it. See references/coverage-model.md §3.
ORACLE_RUNGS = ("touch", "presence", "structural", "outcome", "metamorphic", "visual")
# A critical flow promises an effect. Only these rungs assert one.
EFFECT_RUNGS = ("outcome", "metamorphic", "visual")


def paths(d: Path) -> dict[str, Path]:
    return {
        "campaign": d / "campaign.json",
        "inventory": d / "inventory.json",
        "cases": d / "cases.json",
        "ledger": d / "ledger.md",
    }


def load(d: Path, name: str, default):
    p = paths(d)[name]
    if not p.exists():
        return default
    return json.loads(p.read_text())


def save(d: Path, name: str, value) -> None:
    paths(d)[name].write_text(json.dumps(value, indent=2) + "\n")


def state_of(status: str) -> str:
    """pass | fail | skip | n/a | unselected | open. Unrecognised is open, deliberately."""
    s = (status or "").strip().lower()
    if s in RESOLVED:
        return s
    for r in REASONED:
        if s.startswith(r):
            return r
    return "open"


def next_id(kind: str, existing: list[dict]) -> str:
    prefix = KINDS[kind]
    used = [int(x["id"].split("-")[1]) for x in existing if x.get("id", "").startswith(prefix + "-")]
    return f"{prefix}-{max(used, default=0) + 1:0{WIDTH[prefix]}d}"


# ── init ────────────────────────────────────────────────────────────────────

def cmd_init(args) -> int:
    d = Path(args.dir).resolve()
    d.mkdir(parents=True, exist_ok=True)
    if paths(d)["campaign"].exists() and not args.force:
        sys.exit(f"{paths(d)['campaign']} exists. --force replaces it, but shrinking a "
                 f"campaign mid-run is the silent-narrowing failure this file prevents.")

    lanes = [l.strip() for l in args.lanes.split(",") if l.strip()]
    campaign = {
        "project": args.project,
        "startedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lanes": lanes,
        "axes": [a.strip() for a in (args.axes or "").split(",") if a.strip()],
        "sample": args.sample or "",
        "designOfRecord": args.design_of_record or "",
    }
    save(d, "campaign", campaign)
    if not paths(d)["inventory"].exists():
        save(d, "inventory", {"requirement": [], "surface": [], "flow": [], "component": []})
    if not paths(d)["cases"].exists():
        save(d, "cases", [])

    print(f"Campaign '{args.project}' in {d}")
    print(f"Lanes: {', '.join(lanes)}")
    print(f"Sample: {campaign['sample'] or 'none declared — this is a full campaign of what is enumerated'}")
    return 0


# ── add ─────────────────────────────────────────────────────────────────────

def cmd_add(args) -> int:
    d = Path(args.dir).resolve()
    kind = args.kind
    incoming = json.loads(Path(args.file).read_text()) if args.file else json.loads(sys.stdin.read())
    if isinstance(incoming, dict):
        incoming = [incoming]

    if kind == "case":
        store = load(d, "cases", [])
        inventory = load(d, "inventory", {"requirement": [], "surface": [], "flow": [], "component": []})
        known = {s["id"] for s in inventory.get("surface", [])}
        for item in incoming:
            surf = item.get("surface")
            if surf and surf not in known:
                sys.exit(f"case references unknown surface '{surf}'. Add the surface first — "
                         f"a case against a surface nobody enumerated has no denominator.")
            rung = item.get("oracle")
            if rung and rung not in ORACLE_RUNGS:
                sys.exit(f"case oracle '{rung}' is not a rung. One of: {', '.join(ORACLE_RUNGS)}.")
    else:
        inventory = load(d, "inventory", {"requirement": [], "surface": [], "flow": [], "component": []})
        store = inventory.setdefault(kind, [])

    added = []
    for item in incoming:
        item = dict(item)
        item.setdefault("id", next_id(kind, store))
        if kind == "case":
            item.setdefault("status", "open")
            item.setdefault("evidence", [])
            item.setdefault("armed", False)
        store.append(item)
        added.append(item["id"])

    if kind == "case":
        save(d, "cases", store)
    else:
        save(d, "inventory", inventory)

    print(f"Added {len(added)} {kind}(s): {added[0]}..{added[-1]}" if len(added) > 1
          else f"Added {kind} {added[0]}")
    return 0


# ── set ─────────────────────────────────────────────────────────────────────

def cmd_set(args) -> int:
    d = Path(args.dir).resolve()
    cases = load(d, "cases", [])
    hit = next((c for c in cases if c["id"] == args.case), None)
    if not hit:
        sys.exit(f"No case {args.case}.")

    if args.status:
        hit["status"] = args.status
    for e in args.evidence or []:
        if e not in hit["evidence"]:
            hit["evidence"].append(e)
    if args.armed:
        hit["armed"] = True
    if args.note:
        hit["note"] = args.note

    save(d, "cases", cases)
    print(f"{hit['id']}: {hit['status']}"
          + (f" · {len(hit['evidence'])} evidence" if hit["evidence"] else "")
          + (" · armed" if hit.get("armed") else ""))
    return 0


# ── selection ───────────────────────────────────────────────────────────────

def cmd_scope(args) -> int:
    """Declare what this run covered. Full is a decision, so it is stated here."""
    d = Path(args.dir).resolve()
    campaign = load(d, "campaign", {})
    run = campaign.get("run", {})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if args.full:
        run["scope"] = "full"
        run["basis"] = ""
        run["lastFullRun"] = now
        run["decidedBy"] = args.decided_by or "unstated"
    else:
        if not args.basis:
            sys.exit("A selective run needs --basis: what changed, and against which "
                     "reference. A selection nobody can reproduce is a narrowing, which "
                     "is this skill's first failure mode.")
        if not run.get("lastFullRun"):
            sys.exit("No lastFullRun recorded, so there is no full result for a selective "
                     "run to carry. Run the full campaign once and record it with "
                     "`scope --full` before selecting against it.")
        run["scope"] = "selective"
        run["basis"] = args.basis
        run["decidedBy"] = args.decided_by or "default (nothing asked for a full run)"
    if args.max_full_age_days is not None:
        run["maxFullRunAgeDays"] = args.max_full_age_days
    run["declaredAt"] = now

    campaign["run"] = run
    save(d, "campaign", campaign)
    print(f"scope: {run['scope']}"
          + (f" · basis: {run['basis']}" if run.get("basis") else "")
          + f" · decided by: {run['decidedBy']}")
    if run["scope"] == "full":
        print(f"lastFullRun stamped {now}")
    return 0


def cmd_carry(args) -> int:
    """Mark the cases this run did not select, each carrying why that was safe."""
    d = Path(args.dir).resolve()
    campaign = load(d, "campaign", {})
    run = campaign.get("run", {})
    if (run.get("scope") or "full") != "selective":
        sys.exit("Carrying cases only makes sense on a selective run. Declare it first: "
                 "`scope --selective --basis \"...\"`.")

    cases = load(d, "cases", [])
    ran = set(args.ran or [])
    unknown = ran - {c["id"] for c in cases}
    if unknown:
        sys.exit(f"No such case(s): {', '.join(sorted(unknown))}")
    if not ran:
        sys.exit("--ran named no case. A selective run that ran nothing is not a run; "
                 "if the change genuinely affects nothing, say so and run full anyway.")

    carried, protected = [], []
    flows = {f["id"]: f for f in load(d, "inventory", {}).get("flow", [])}
    for c in cases:
        if c["id"] in ran:
            continue
        # The always-run floor is enforced here as well as in the gate, so a
        # protected case cannot be carried by accident and discovered later.
        f = flows.get(c.get("flow") or "")
        if f and f.get("critical") and c.get("oracle") in EFFECT_RUNGS:
            protected.append(c["id"])
            continue
        c["carriedFrom"] = state_of(c.get("status", "open"))
        c["selectionBasis"] = args.basis
        c["status"] = f"{CARRIED}: {args.basis}"
        carried.append(c["id"])

    save(d, "cases", cases)
    print(f"ran {len(ran)} · carried {len(carried)} · protected {len(protected)}")
    if protected:
        print("  always-run floor, left for this run to prove: "
              + ", ".join(protected[:10]) + (" …" if len(protected) > 10 else ""))
    return 0


# ── the gate ────────────────────────────────────────────────────────────────

def audit(d: Path) -> dict:
    campaign = load(d, "campaign", {})
    inventory = load(d, "inventory", {"requirement": [], "surface": [], "flow": [], "component": []})
    cases = load(d, "cases", [])

    surfaces = inventory.get("surface", [])
    by_surface: dict[str, list[dict]] = {s["id"]: [] for s in surfaces}
    orphans = []
    for c in cases:
        sid = c.get("surface")
        if sid in by_surface:
            by_surface[sid].append(c)
        elif sid:
            orphans.append(c["id"])

    counts = {"pass": 0, "fail": 0, "skip": 0, "n/a": 0, "unselected": 0, "open": 0}
    open_ids, unevidenced, armed = [], [], 0
    carried_unbased = []
    for c in cases:
        st = state_of(c.get("status", "open"))
        counts[st] += 1
        if st == "open":
            open_ids.append(c["id"])
        if st == CARRIED and not (c.get("selectionBasis") or ":" in (c.get("status") or "")):
            carried_unbased.append(c["id"])
        if st == "pass":
            if not c.get("evidence"):
                unevidenced.append(c["id"])
            if c.get("armed"):
                armed += 1

    uncovered = [sid for sid, cs in by_surface.items() if not cs]

    # A requirement with no case is the campaign's real gap: it is something the
    # project says it does that nothing checked. Deferred requirements are exempt,
    # because not building them is the recorded decision.
    reqs = inventory.get("requirement", [])
    traced = {r for c in cases for r in ([c["req"]] if isinstance(c.get("req"), str)
                                         else c.get("req", []) or [])}
    untested_reqs = [r["id"] for r in reqs
                     if r["id"] not in traced and r.get("class") != "deferred"]

    # What the cases actually check. A case with no declared rung counts as
    # unrated, never as adequate — the whole point is that a plan cannot look
    # complete by omission.
    mix = {r: 0 for r in ORACLE_RUNGS}
    mix["unrated"] = 0
    for c in cases:
        mix[c.get("oracle") if c.get("oracle") in ORACLE_RUNGS else "unrated"] += 1

    # A critical flow promises an effect, so at least one of its cases must
    # assert one. Presence-only proof of a critical flow is the failure this
    # rule exists for, and it is invisible in every other number on this page.
    flows = inventory.get("flow", [])
    by_flow: dict[str, list[dict]] = {f["id"]: [] for f in flows}
    for c in cases:
        fid = c.get("flow")
        if fid in by_flow:
            by_flow[fid].append(c)
    presence_only = [
        f["id"] for f in flows
        if f.get("critical")
        and not any(c.get("oracle") in EFFECT_RUNGS for c in by_flow[f["id"]])
    ]

    # A critical flow is the always-run floor. Selection may narrow anything else,
    # but a flow that promises an effect must have that effect re-proved on every
    # run: change-to-test mapping is a heuristic, and the case it wrongly drops is
    # indistinguishable from the case that passed. So a critical flow whose every
    # effect case was carried forward is a blocker, not a saving.
    critical_carried = [
        f["id"] for f in flows
        if f.get("critical")
        and any(c.get("oracle") in EFFECT_RUNGS for c in by_flow[f["id"]])
        and all(state_of(c.get("status", "open")) == CARRIED
                for c in by_flow[f["id"]] if c.get("oracle") in EFFECT_RUNGS)
    ]

    # Scope is declared, never inferred from the numbers. A run that selected is a
    # different claim from a run that covered everything, and the age of the last
    # full run is the number that says how much of this verdict is carried.
    run = campaign.get("run", {})
    scope = (run.get("scope") or "full").strip().lower()
    basis = run.get("basis", "")
    last_full = run.get("lastFullRun", "")
    max_age = run.get("maxFullRunAgeDays")
    stale_by = None
    if last_full:
        try:
            age = (datetime.now(timezone.utc)
                   - datetime.fromisoformat(last_full)).total_seconds() / 86400
            if max_age is not None and age > float(max_age):
                stale_by = round(age - float(max_age), 1)
            age_days = round(age, 1)
        except ValueError:
            age_days = None
    else:
        age_days = None

    blockers = []
    if open_ids:
        blockers.append(f"{len(open_ids)} case(s) still open")
    if uncovered:
        blockers.append(f"{len(uncovered)} surface(s) with no case at all")
    if unevidenced:
        blockers.append(f"{len(unevidenced)} pass(es) naming no evidence artifact")
    if untested_reqs:
        blockers.append(f"{len(untested_reqs)} requirement(s) no case traces to")
    if presence_only:
        blockers.append(f"{len(presence_only)} critical flow(s) proved only by "
                        f"presence-level cases")
    if critical_carried:
        blockers.append(f"{len(critical_carried)} critical flow(s) whose every effect "
                        f"case was carried forward rather than re-run "
                        f"({', '.join(critical_carried[:5])}) — a critical flow is the "
                        f"always-run floor")
    if carried_unbased:
        blockers.append(f"{len(carried_unbased)} carried case(s) naming no selection "
                        f"basis ({', '.join(carried_unbased[:5])}) — "
                        f"'unselected: unchanged since <ref>', never bare")
    if scope == "selective" and not basis:
        blockers.append("the run declares scope 'selective' and names no basis — "
                        "a selection nobody can reproduce is a narrowing")
    if scope == "selective" and not last_full:
        blockers.append("a selective run with no recorded lastFullRun — the carried "
                        "verdicts rest on a full run that was never dated")
    if stale_by is not None:
        blockers.append(f"the last full run is {stale_by} day(s) past the declared "
                        f"maxFullRunAgeDays — selection has been carrying this verdict "
                        f"too long; run full")

    return {
        "project": campaign.get("project", ""),
        "lanes": campaign.get("lanes", []),
        "sample": campaign.get("sample", ""),
        "runScope": scope,
        "selectionBasis": basis,
        "lastFullRun": last_full,
        "lastFullRunAgeDays": age_days,
        "maxFullRunAgeDays": max_age,
        "carriedCases": counts["unselected"],
        "selectedOfTotal": f"{len(cases) - counts['unselected']}/{len(cases)}",
        "criticalFlowsCarried": critical_carried,
        "carriedWithoutBasis": carried_unbased,
        "requirements": len(reqs),
        "requirementsUntested": untested_reqs,
        "surfaces": len(surfaces),
        "surfacesUncovered": uncovered,
        "flows": len(flows),
        "flowsPresenceOnly": presence_only,
        "components": len(inventory.get("component", [])),
        "cases": len(cases),
        "counts": counts,
        "oracleMix": mix,
        "armed": armed,
        "armedOfPassing": f"{armed}/{counts['pass']}",
        "openCases": open_ids,
        "unevidencedPasses": unevidenced,
        "orphanCases": orphans,
        "blockers": blockers,
        "clear": not blockers,
    }


def cmd_check(args) -> int:
    d = Path(args.dir).resolve()
    a = audit(d)
    if args.json:
        print(json.dumps(a, indent=2))
        return 0 if a["clear"] else 1

    c = a["counts"]
    print(f"{a['project']} · lanes: {', '.join(a['lanes']) or 'none declared'}")
    print(f"Requirements: {a['requirements']} inventoried, {len(a['requirementsUntested'])} with no case")
    print(f"Surfaces:   {a['surfaces']} enumerated, {len(a['surfacesUncovered'])} with no case")
    print(f"Cases:      {c['pass']} pass · {c['fail']} fail · {c['skip']} skip · "
          f"{c['n/a']} n/a · {c['unselected']} carried · {c['open']} open  (of {a['cases']})")
    mix = a["oracleMix"]
    print("Oracles:    " + " · ".join(f"{k} {v}" for k, v in mix.items() if v))
    print(f"Armed:      {a['armedOfPassing']} passing cases have been watched to fail")
    if a["runScope"] == "selective":
        age = a["lastFullRunAgeDays"]
        print(f"Scope:      SELECTIVE — ran {a['selectedOfTotal']} cases"
              + (f", carried {a['carriedCases']}" if a["carriedCases"] else ""))
        print(f"Basis:      {a['selectionBasis'] or 'NONE DECLARED'}")
        print(f"Last full:  {a['lastFullRun'] or 'never recorded'}"
              + (f" ({age} days ago)" if age is not None else ""))
    else:
        print(f"Scope:      FULL — every case in the campaign was run")
    if a["sample"]:
        print(f"Sample:     {a['sample']}")

    if a["clear"]:
        if a["runScope"] == "selective":
            print(f"\nEvery selected case accounted for. This is a SELECTIVE verdict: "
                  f"{a['selectedOfTotal']} cases ran and {a['carriedCases']} carry a "
                  f"result from an earlier run, on the basis "
                  f"'{a['selectionBasis']}'. It does not say the suite passes — it says "
                  f"what changed passes and the rest is unchanged since "
                  f"{a['lastFullRun']}. The armed ratio ({a['armedOfPassing']}) still "
                  f"bounds what any of it is known to catch.")
            return 0
        print(f"\nEvery case accounted for. The verdict line still carries the fraction "
              f"({a['surfaces']} surfaces, {a['cases']} cases) and the armed ratio "
              f"({a['armedOfPassing']}) — a suite is only known to bite where it was armed.")
        return 0

    print("\nNot ready to report:")
    for b in a["blockers"]:
        print(f"  · {b}")
    if a["requirementsUntested"]:
        print(f"\n  Requirements nothing checks: {', '.join(a['requirementsUntested'][:12])}")
        print("  Each is something the project says it does. Write the case, or mark the "
              "requirement `deferred` with its citation.")
    if a["surfacesUncovered"]:
        print(f"  Surfaces with no case: {', '.join(a['surfacesUncovered'])}")
    if a["flowsPresenceOnly"]:
        print(f"\n  Critical flows proved only by presence: {', '.join(a['flowsPresenceOnly'])}")
        print("  Each promises an effect. Add a case whose oracle is outcome, metamorphic "
              "or visual, or drop the flow's `critical` flag and say why.")
    if a["unevidencedPasses"]:
        print(f"  Passes with no artifact: {', '.join(a['unevidencedPasses'][:12])}")
        print("  A pass you reached by looking is not a measurement. Attach the artifact "
              "or reopen the case.")
    if a["openCases"]:
        print(f"  Open: {', '.join(a['openCases'][:20])}"
              + (" …" if len(a["openCases"]) > 20 else ""))
    print("\nFinish them, resolve each to skip:/n-a: with a reason, or declare the stop with "
          "its resume point — in the reply, the verdict line and the report. Never silently.")
    return 1


# ── report ──────────────────────────────────────────────────────────────────

def cmd_report(args) -> int:
    d = Path(args.dir).resolve()
    a = audit(d)
    inventory = load(d, "inventory", {"requirement": [], "surface": [], "flow": [], "component": []})
    cases = load(d, "cases", [])

    if args.json:
        print(json.dumps({"audit": a, "inventory": inventory, "cases": cases}, indent=2))
        return 0

    by_surface: dict[str, list[dict]] = {}
    for c in cases:
        by_surface.setdefault(c.get("surface", "—"), []).append(c)

    lines = [f"# {a['project']} — campaign ledger", ""]
    lines += [f"Lanes: {', '.join(a['lanes'])}", ""]
    if a["sample"]:
        lines += [f"**Sample:** {a['sample']}", ""]
    lines += [
        f"{a['surfaces']} surfaces · {a['flows']} flows · {a['components']} components · "
        f"{a['cases']} cases",
        f"{a['counts']['pass']} pass · {a['counts']['fail']} fail · {a['counts']['skip']} skip · "
        f"{a['counts']['n/a']} n/a · {a['counts']['open']} open · armed {a['armedOfPassing']}",
        "",
        "| Case | Surface | State | Lane | Status | Armed | Evidence |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in inventory.get("surface", []):
        for c in by_surface.get(s["id"], []):
            lines.append(
                f"| {c['id']} | {s['id']} {s.get('label', '')} | {c.get('state', '')} | "
                f"{c.get('lane', '')} | {c.get('status', 'open')} | "
                f"{'yes' if c.get('armed') else ''} | {len(c.get('evidence', []))} |")

    text = "\n".join(lines) + "\n"
    paths(d)["ledger"].write_text(text)
    print(text)
    print(f"Written to {paths(d)['ledger']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Case registry and gate for a UI test campaign.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init")
    i.add_argument("dir")
    i.add_argument("--project", required=True)
    i.add_argument("--lanes", required=True, help="web,macos,ios,rn,swiftui")
    i.add_argument("--axes", help="Comma-separated axes this campaign varies.")
    i.add_argument("--sample", help="Declare a deliberate sample: which cells, chosen how, "
                                    "and what it cannot speak for.")
    i.add_argument("--design-of-record", help="Path/URL of the mock the build is measured against.")
    i.add_argument("--force", action="store_true")
    i.set_defaults(fn=cmd_init)

    a = sub.add_parser("add")
    a.add_argument("dir")
    a.add_argument("--kind", required=True, choices=list(KINDS))
    a.add_argument("--file", help="JSON array (or object); omit to read stdin.")
    a.set_defaults(fn=cmd_add)

    s = sub.add_parser("set")
    s.add_argument("dir")
    s.add_argument("--case", required=True)
    s.add_argument("--status",
                   help="pass | fail | skip: <reason> | n/a: <reason> | "
                        "unselected: <basis>")
    s.add_argument("--evidence", action="append")
    s.add_argument("--armed", action="store_true",
                   help="This assertion was watched to fail with the behaviour removed.")
    s.add_argument("--note")
    s.set_defaults(fn=cmd_set)

    sc = sub.add_parser("scope", help="Declare what this run covered. Full is a decision.")
    sc.add_argument("dir")
    g = sc.add_mutually_exclusive_group(required=True)
    g.add_argument("--full", action="store_true",
                   help="Every case ran. Stamps lastFullRun, which is what later "
                        "selective runs carry from.")
    g.add_argument("--selective", action="store_true",
                   help="Only the affected cases ran. Requires --basis.")
    sc.add_argument("--basis", help="What changed and against which reference, e.g. "
                                    "'changed: src/pricing/** since v2.3.1'.")
    sc.add_argument("--decided-by", help="Who or what chose this scope: 'user asked for "
                                         "every gate', 'inferred: lockfile changed', "
                                         "'default'.")
    sc.add_argument("--max-full-age-days", type=float,
                    help="Beyond this, a selective run becomes a blocker and the "
                         "campaign demands a full one.")
    sc.set_defaults(fn=cmd_scope)

    cy = sub.add_parser("carry", help="Mark the cases a selective run did not select.")
    cy.add_argument("dir")
    cy.add_argument("--ran", action="append", required=True,
                    help="A case this run actually ran. Repeatable. Everything else is "
                         "carried, except the always-run floor.")
    cy.add_argument("--basis", required=True,
                    help="Why not running it was safe, e.g. 'unchanged since v2.3.1'.")
    cy.set_defaults(fn=cmd_carry)

    c = sub.add_parser("check")
    c.add_argument("dir")
    c.add_argument("--json", action="store_true")
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser("report")
    r.add_argument("dir")
    r.add_argument("--json", action="store_true")
    r.set_defaults(fn=cmd_report)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
