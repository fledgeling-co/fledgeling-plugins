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
  5. A lane that claims the app was running and drawn proves it once, with the
     artifact, the command that built it and what witnessed it attaching. A
     campaign once reported 100% checked over two native apps while no GUI
     process had ever existed; every number in it was true.

Ids are stable and referenceable, because the evidence page, the report and a
later conversation all need to point at the same thing: SURF-001, FLOW-001.03,
CMP-001, CASE-0001, DEF-001.

Usage:
    campaign.py init   <dir> --project NAME --lanes web,macos-glass [--sample "..."]
    campaign.py lane   <dir> --lane macos-glass --artifact build/App.app \\
                             --built-by "xcodebuild -scheme App" \\
                             --attached "pid 4412 owns window 'App'" \\
                             --capture "ScreenCaptureKit, SCFrameStatus=complete"
    campaign.py add    <dir> --kind surface --file surfaces.json
    campaign.py add    <dir> --kind case    --file cases.json
    campaign.py set    <dir> --case CASE-0007 --status pass \\
                             --evidence evidence/shots/dash.png --armed
    campaign.py carry  <dir> --ran CASE-0007 --basis "unchanged since v2.3.1"
    campaign.py check  <dir> [--json]
    campaign.py report <dir> [--json]

State lives in <dir>/campaign.json (facts), inventory.json (what exists) and
cases.json (what was checked). ledger.md is generated from them for a human.
"""

from __future__ import annotations

import argparse
import hashlib
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

# Recognised, explained, and still a blocker. These exist because a check that
# COULD NOT RUN and a check that RAN AND PASSED must never reach the report
# wearing the same face. `equal(a, b)` is only a legal claim when both sides
# were measured; where one was not, the honest verdict is "we do not know",
# which is a weaker claim than "no difference found" and a different one from
# "this does not apply here".
#
#   n/a           the lane structurally cannot support this check, ever
#   skip          this case should not run
#   inconclusive  it was attempted and the instrument could not measure it
#   blocked       the thing under test never ran, so nothing downstream is valid
#
# n/a and skip are decisions. inconclusive and blocked are unfinished business,
# so they hold the gate shut while still being counted and explained rather
# than sitting in the report as an unexplained dash. See references/on-glass.md.
UNRESOLVED_REASONED = ("inconclusive", "blocked")

# What a case actually checks, weakest first. The rung is a field rather than a
# judgement because UI suites execute behaviour far more often than they assert
# it — inferred metamorphic relations across 214 components were exercised at
# high rates and explicitly validated only 42.5%-47.6% of the time. A plan can
# therefore look complete while proving very little, and no count of tests shows
# it. See references/coverage-model.md §3.
#
# `visual` split into two rungs, because one word was covering both halves of a
# distinction that decides whether a campaign is honest. Asserting that a card's
# title property equals "AGGREGATE CPU" is a data-model assertion; it was
# claiming the visual rung, counting as an effect, and carrying a campaign to
# 100% while no window had ever been drawn.
#
#   structural-visual  labels, hierarchy tokens and structural metadata exist
#   raster-visual      pixels were captured off a display server and compared
#   interactive-glass  synthetic UI events actuated and state transitions verified on-glass
ORACLE_RUNGS = ("touch", "presence", "structural", "structural-visual",
                "outcome", "metamorphic", "raster-visual", "interactive-glass", "visual")
# A critical flow promises an effect. Only these rungs assert one.
EFFECT_RUNGS = ("outcome", "metamorphic", "raster-visual", "interactive-glass")
# Retained so an existing campaign loads rather than silently re-rating its
# cases as `unrated`, and reported as a migration blocker so the split is made
# deliberately. It buys no effect credit in the meantime.
LEGACY_RUNGS = ("visual",)
# These rungs claim pixels, so they must produce pixels. See `inspect_raster`.
RASTER_RUNGS = ("raster-visual",)

# A lane whose name ends in `-glass` claims the application was verified while
# actually running and drawn by a display server — a real window, composited,
# photographed. That is a much stronger claim than the same lane run headless,
# and it is the one claim a campaign can make that nothing else can check for
# it, so the lane carries the burden of proving it. See `cmd_lane`.
GLASS_SUFFIX = "-glass"

# Raster magic numbers, so "is this actually an image" is read from the bytes
# rather than trusted from the extension. A .png written by a failed capture is
# frequently an HTML error page or a zero-byte file.
RASTER_MAGIC = {
    b"\x89PNG\r\n\x1a\n": "png",
    b"\xff\xd8\xff": "jpeg",
    b"RIFF": "webp",
}


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
    """pass | fail | skip | n/a | unselected | inconclusive | blocked | open.

    Unrecognised is open, deliberately.
    """
    s = (status or "").strip().lower()
    if s in RESOLVED:
        return s
    for r in REASONED + UNRESOLVED_REASONED:
        if s.startswith(r):
            return r
    return "open"


def inspect_raster(path: Path) -> dict:
    """Read what a capture file actually is, from its bytes.

    A `raster-visual` case claims pixels came off a display server, and the
    cheapest way that claim goes wrong is an artifact that is not an image:
    a zero-byte file from a capture that failed, an HTML error page saved with
    a .png suffix, or a path that no longer resolves. Those are decidable from
    the first eight bytes and the file length, so they are decided here.

    What this deliberately does NOT do is score the picture. A density,
    entropy or unique-colour floor cannot separate a failed capture from a
    legitimately sparse screen — an empty-state surface is mostly background
    by design, and a shell error message has much the same ink as the empty
    state it replaced. So `bytesPerPixel` is recorded as a regression signal
    for runs already known to have launched, and it never gates. What gates is
    provenance: did a process run, did it attach, what did the capture channel
    say about the frame. See references/on-glass.md.
    """
    out = {"path": str(path), "exists": path.exists(), "kind": None,
           "width": None, "height": None, "bytes": None, "sha256": None,
           "bytesPerPixel": None, "reason": None}
    if not out["exists"]:
        out["reason"] = "no file at that path"
        return out

    raw = path.read_bytes()
    out["bytes"] = len(raw)
    out["sha256"] = hashlib.sha256(raw).hexdigest()
    if not raw:
        out["reason"] = "zero-byte file — the capture wrote nothing"
        return out

    for magic, kind in RASTER_MAGIC.items():
        if raw.startswith(magic):
            out["kind"] = kind
            break
    if not out["kind"]:
        head = raw[:40].decode("utf-8", "replace").strip().replace("\n", " ")
        out["reason"] = (f"not a raster image — starts {head[:32]!r}. A capture "
                         f"that failed often writes an error page to the path "
                         f"the test expected a screenshot at")
        return out

    if out["kind"] == "png" and len(raw) >= 24 and raw[12:16] == b"IHDR":
        out["width"] = int.from_bytes(raw[16:20], "big")
        out["height"] = int.from_bytes(raw[20:24], "big")
        if out["width"] and out["height"]:
            out["bytesPerPixel"] = round(len(raw) / (out["width"] * out["height"]), 5)
        if out["width"] <= 1 or out["height"] <= 1:
            out["reason"] = (f"{out['width']}x{out['height']} — a capture this "
                             f"size is a placeholder, not a window")
    return out


def lane_needs_glass(lane: str) -> bool:
    return (lane or "").strip().lower().endswith(GLASS_SUFFIX)


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
            # The field is `req`, and the prose everywhere calls it a requirement.
            # A case written with `requirement:` used to be stored intact and then
            # reported as a requirement nothing checks — a blocker pointing at the
            # wrong thing, which cost a round of debugging. Accept the word the
            # documentation uses instead of silently disagreeing with it.
            if "requirement" in item and "req" not in item:
                item["req"] = item.pop("requirement")
                print(f"note: 'requirement' read as 'req' ({item['req']}); "
                      f"the registry field is `req`.")
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
    if args.capture_method or args.frame_status:
        cap = hit.setdefault("capture", {})
        if args.capture_method:
            cap["method"] = args.capture_method
        if args.frame_status:
            cap["frameStatus"] = args.frame_status
    if args.note:
        hit["note"] = args.note

    save(d, "cases", cases)
    print(f"{hit['id']}: {hit['status']}"
          + (f" · {len(hit['evidence'])} evidence" if hit["evidence"] else "")
          + (" · armed" if hit.get("armed") else "")
          + (f" · {hit['capture']['method']}" if (hit.get("capture") or {}).get("method") else ""))
    return 0


# ── the artifact under test, and whether it ever ran ────────────────────────

def cmd_lane(args) -> int:
    """Record what this lane actually tested, and what proved it was running.

    A campaign once reported 100% checked, 22 armed cases and 59 passing tests
    for two native desktop applications while no GUI process had ever attached
    to a window server. The Swift half initialised SwiftUI view structs in
    memory — value types, so nothing renders; the Windows half was C# that had
    never been compiled; and the screenshots on the evidence page came from an
    HTML mock photographed in a browser. Every individual number was true.

    Nothing in the ledger could catch that, because the ledger only ever asked
    whether cases resolved. So a lane claiming `-glass` names three things
    here, and the gate refuses to clear without them:

      --artifact    what was tested, as a path that exists
      --built-by    the command that produced it, so "never compiled" is visible
      --attached    what proved a process from that artifact reached a display
                    server — a window id, a pid owning a window, a frame status

    `--cannot-attach` is the honest alternative and is not a failure of
    diligence: it records the lane as unreachable with a structural reason, and
    its cases then resolve to `blocked: <reason>` rather than to a pass nobody
    could have earned.
    """
    d = Path(args.dir).resolve()
    campaign = load(d, "campaign", {})
    lanes = campaign.setdefault("laneProof", {})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if args.cannot_attach:
        lanes[args.lane] = {"attached": False, "reason": args.cannot_attach,
                            "declaredAt": now}
        save(d, "campaign", campaign)
        print(f"{args.lane}: NOT attached — {args.cannot_attach}")
        print("Its cases resolve to `blocked: <reason>`. A lane that never ran "
              "cannot hold a pass.")
        return 0

    missing = [f for f, v in (("--artifact", args.artifact),
                              ("--built-by", args.built_by),
                              ("--attached", args.attached)) if not v]
    if missing:
        sys.exit(f"A lane claiming on-glass verification needs {', '.join(missing)}. "
                 f"Use --cannot-attach '<reason>' if it genuinely could not be "
                 f"reached; that is a recorded limit, not a failure.")

    artifact = Path(args.artifact)
    if not artifact.exists():
        sys.exit(f"--artifact {artifact} does not exist. This is the failure the "
                 f"command is for: source that was authored and never built "
                 f"cannot carry a case, and its absence is checkable.")

    lanes[args.lane] = {
        "attached": True,
        "artifact": str(artifact),
        "artifactBytes": artifact.stat().st_size if artifact.is_file() else None,
        "builtBy": args.built_by,
        "attachedBy": args.attached,
        "captureChannel": args.capture or "",
        "declaredAt": now,
    }
    save(d, "campaign", campaign)
    print(f"{args.lane}: attached · {artifact}")
    print(f"  built by  {args.built_by}")
    print(f"  proved by {args.attached}")
    if args.capture:
        print(f"  capture   {args.capture}")
    else:
        print("  capture   none declared — a raster-visual case on this lane will "
              "have no channel to cite")
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

    counts = {"pass": 0, "fail": 0, "skip": 0, "n/a": 0, "unselected": 0,
              "inconclusive": 0, "blocked": 0, "open": 0}
    open_ids, unevidenced, armed = [], [], 0
    carried_unbased = []
    legacy_rung, bad_raster, unwitnessed_raster = [], [], []
    invalid_interactive_glass = []
    seen_artifacts: dict[str, list[str]] = {}
    lane_proof = campaign.get("laneProof", {})
    glass_lanes_unproved: dict[str, list[str]] = {}
    glass_lanes_unattached: dict[str, str] = {}
    for c in cases:
        st = state_of(c.get("status", "open"))
        counts[st] += 1
        if st == "open":
            open_ids.append(c["id"])
        if st == CARRIED and not (c.get("selectionBasis") or ":" in (c.get("status") or "")):
            carried_unbased.append(c["id"])
        if c.get("oracle") in LEGACY_RUNGS:
            legacy_rung.append(c["id"])

        # A lane that claims the application was running and drawn has to have
        # said so once, with an artifact and a witness. Checked for every case
        # on the lane, not only the passing ones, because a lane that never
        # attached makes its failures uninterpretable too.
        lane = c.get("lane") or ""
        if lane_needs_glass(lane):
            proof = lane_proof.get(lane)
            if not proof:
                glass_lanes_unproved.setdefault(lane, []).append(c["id"])
            elif not proof.get("attached"):
                glass_lanes_unattached[lane] = proof.get("reason", "no reason recorded")
                if st not in ("blocked", "n/a", "skip"):
                    unwitnessed_raster.append(
                        f"{c['id']} ({lane} never attached, so its status "
                        f"'{st}' cannot mean what it says)")
        elif c.get("oracle") == "interactive-glass":
            invalid_interactive_glass.append(
                f"{c['id']} claims interactive-glass on non-glass lane '{lane}' — "
                f"interactive-glass requires an on-glass lane ending in '{GLASS_SUFFIX}'")

        if st == "pass":
            if not c.get("evidence"):
                unevidenced.append(c["id"])
            if c.get("armed"):
                armed += 1

        # A rung that claims pixels must produce pixels, and they must be this
        # case's pixels. One screenshot attached to twelve cases is the cheapest
        # way a wall of captures comes to mean nothing, and it is exact to
        # detect, so it is detected rather than trusted.
        if c.get("oracle") in RASTER_RUNGS and st == "pass":
            shots = [e for e in c.get("evidence", [])]
            if not shots:
                bad_raster.append(f"{c['id']} claims raster-visual and names no artifact")
            for e in shots:
                info = inspect_raster((d / e) if not Path(e).is_absolute() else Path(e))
                if info["reason"]:
                    bad_raster.append(f"{c['id']} → {e}: {info['reason']}")
                elif info["sha256"]:
                    seen_artifacts.setdefault(info["sha256"], []).append(f"{c['id']}:{e}")
            if not (c.get("capture") or {}).get("method"):
                unwitnessed_raster.append(
                    f"{c['id']} names no capture method, so nothing says these "
                    f"pixels came off a display server")

    duplicate_artifacts = {h: ids for h, ids in seen_artifacts.items() if len(ids) > 1}

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

    # Flow atom validation: when a critical flow declares observable atoms, its
    # effect cases must trace the interactive execution sequence rather than presence.
    flow_atom_gaps = []
    for f in flows:
        atoms = f.get("atoms") or []
        if f.get("critical") and atoms:
            flow_cases = by_flow.get(f["id"], [])
            if not any(c.get("oracle") in EFFECT_RUNGS for c in flow_cases):
                flow_atom_gaps.append(
                    f"{f['id']} declares {len(atoms)} atom(s) with no effect-rung or "
                    f"interactive-glass case verifying the sequence")

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
    # A gate that cannot fail on the emptiest possible input is the failure this
    # skill's first rule describes: a check that matches nothing returns clean and
    # is indistinguishable from a clean surface. `init` followed by `check` used to
    # exit 0 on zero requirements, zero surfaces and zero cases, with every count a
    # truthful zero, so a run that crashed straight after init left a directory
    # that cleared the gate.
    if not cases:
        blockers.append("no cases at all — an empty campaign is not a passing one. "
                        "Every count here is a truthful zero, which is exactly why "
                        "this cannot be allowed to read as clear")
    if not surfaces:
        blockers.append("no surfaces enumerated — nothing has a denominator, so "
                        "there is nothing for a case to be a sample of")
    if open_ids:
        blockers.append(f"{len(open_ids)} case(s) still open")
    if counts["inconclusive"]:
        blockers.append(f"{counts['inconclusive']} case(s) inconclusive — attempted, "
                        f"and the instrument could not measure. Not a pass and not "
                        f"an n/a: 'we do not know' is a weaker claim than 'no "
                        f"difference found' and a different one from 'does not apply'")
    if counts["blocked"]:
        blockers.append(f"{counts['blocked']} case(s) blocked — the thing under test "
                        f"never ran, so nothing downstream of it is valid")
    if glass_lanes_unproved:
        blockers.append(f"{len(glass_lanes_unproved)} lane(s) claim on-glass "
                        f"verification with no proof recorded "
                        f"({', '.join(sorted(glass_lanes_unproved))}) — run "
                        f"`campaign.py lane` with the artifact, how it was built "
                        f"and what witnessed it attaching")
    if legacy_rung:
        blockers.append(f"{len(legacy_rung)} case(s) still on the legacy `visual` "
                        f"rung ({', '.join(legacy_rung[:5])}) — split each into "
                        f"`structural-visual` (labels and hierarchy exist) or "
                        f"`raster-visual` (pixels captured off a display server). "
                        f"`visual` buys no effect credit until you do")
    if bad_raster:
        blockers.append(f"{len(bad_raster)} raster-visual claim(s) whose artifact is "
                        f"not a usable capture — a visual claim without pixels is a "
                        f"structural assertion in disguise")
    if duplicate_artifacts:
        n = sum(len(v) for v in duplicate_artifacts.values())
        blockers.append(f"{n} raster-visual case(s) share {len(duplicate_artifacts)} "
                        f"identical artifact(s) byte for byte — one screenshot cannot "
                        f"be evidence for two different assertions")
    if unwitnessed_raster:
        blockers.append(f"{len(unwitnessed_raster)} pixel claim(s) with nothing saying "
                        f"where the pixels came from")
    if invalid_interactive_glass:
        blockers.append(f"{len(invalid_interactive_glass)} case(s) claiming interactive-glass "
                        f"on non-glass lane(s)")
    if uncovered:
        blockers.append(f"{len(uncovered)} surface(s) with no case at all")
    if unevidenced:
        blockers.append(f"{len(unevidenced)} pass(es) naming no evidence artifact")
    if untested_reqs:
        blockers.append(f"{len(untested_reqs)} requirement(s) no case traces to")
    if presence_only:
        blockers.append(f"{len(presence_only)} critical flow(s) proved only by "
                        f"presence-level cases")
    if flow_atom_gaps:
        blockers.append(f"{len(flow_atom_gaps)} critical flow(s) with declared atoms "
                        f"lacking effect-level or interactive-glass verification")
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

    # Observation coverage, kept apart from the verdict on purpose. "34 of 42
    # measured and all 34 equal" is not 100% agreement, it is a result over a
    # population of 34 with 8 observations missing, and the two read identically
    # unless the denominator is printed beside them. So the campaign reports what
    # it asked for, what it actually measured, and what it could not.
    measured = counts["pass"] + counts["fail"]
    unavailable = counts["inconclusive"] + counts["blocked"] + counts["n/a"]
    deferred = counts["skip"] + counts["unselected"] + counts["open"]

    return {
        "project": campaign.get("project", ""),
        "lanes": campaign.get("lanes", []),
        "laneProof": lane_proof,
        "glassLanesUnproved": {k: v for k, v in glass_lanes_unproved.items()},
        "glassLanesUnattached": glass_lanes_unattached,
        "sample": campaign.get("sample", ""),
        "observations": {
            "requested": len(cases),
            "measured": measured,
            "unavailable": unavailable,
            "deferred": deferred,
            "coverage": (f"{measured}/{len(cases)}" if cases else "0/0"),
        },
        "legacyRungCases": legacy_rung,
        "badRasterClaims": bad_raster,
        "duplicateArtifacts": duplicate_artifacts,
        "unwitnessedPixelClaims": unwitnessed_raster,
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
    o = a["observations"]
    print(f"{a['project']} · lanes: {', '.join(a['lanes']) or 'none declared'}")
    print(f"Requirements: {a['requirements']} inventoried, {len(a['requirementsUntested'])} with no case")
    print(f"Surfaces:   {a['surfaces']} enumerated, {len(a['surfacesUncovered'])} with no case")
    print(f"Cases:      {c['pass']} pass · {c['fail']} fail · {c['skip']} skip · "
          f"{c['n/a']} n/a · {c['unselected']} carried · {c['inconclusive']} inconclusive · "
          f"{c['blocked']} blocked · {c['open']} open  (of {a['cases']})")
    print(f"Observed:   {o['coverage']} cases produced a measurement · "
          f"{o['unavailable']} could not be measured · {o['deferred']} not attempted")
    for lane, proof in sorted(a["laneProof"].items()):
        if proof.get("attached"):
            print(f"On glass:   {lane} → {proof.get('artifact', '?')} "
                  f"({proof.get('attachedBy', 'no witness recorded')})")
        else:
            print(f"On glass:   {lane} → NOT attached: {proof.get('reason', '?')}")
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
    if a["glassLanesUnproved"]:
        for lane, ids in sorted(a["glassLanesUnproved"].items()):
            print(f"\n  Lane '{lane}' claims on-glass verification and has no proof "
                  f"({len(ids)} case(s), e.g. {', '.join(ids[:4])}).")
        print("  Record it once:  campaign.py lane <dir> --lane <lane> --artifact <path> \\")
        print("                     --built-by '<build command>' --attached '<what witnessed it>'")
        print("  Or say it could not be reached:  --cannot-attach '<structural reason>'")
    if a["badRasterClaims"]:
        print("\n  Pixel claims with no usable pixels:")
        for line in a["badRasterClaims"][:10]:
            print(f"    · {line}")
    if a["duplicateArtifacts"]:
        print("\n  The same capture standing in for several cases:")
        for ids in list(a["duplicateArtifacts"].values())[:6]:
            print(f"    · {', '.join(ids)}")
    if a["unwitnessedPixelClaims"]:
        print("\n  Pixels with no stated origin:")
        for line in a["unwitnessedPixelClaims"][:10]:
            print(f"    · {line}")
    if a["legacyRungCases"]:
        print(f"\n  On the legacy `visual` rung: {', '.join(a['legacyRungCases'][:12])}")
        print("  Asserting that a card's title property equals a string is a data-model "
              "check, not a visual one. Split each into structural-visual or "
              "raster-visual; the second needs a capture off a display server.")
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
                        "unselected: <basis> | inconclusive: <reason> | "
                        "blocked: <reason>")
    s.add_argument("--evidence", action="append")
    s.add_argument("--armed", action="store_true",
                   help="This assertion was watched to fail with the behaviour removed.")
    s.add_argument("--capture-method",
                   help="How these pixels were obtained, e.g. 'ScreenCaptureKit "
                        "window-scoped'. Required for a raster-visual pass.")
    s.add_argument("--frame-status",
                   help="What the capture channel said about the frame, e.g. "
                        "SCFrameStatus=complete. An idle or blank frame is not "
                        "evidence of anything.")
    s.add_argument("--note")
    s.set_defaults(fn=cmd_set)

    ln = sub.add_parser("lane", help="Record the artifact a lane tested and what "
                                     "proved it was running.")
    ln.add_argument("dir")
    ln.add_argument("--lane", required=True,
                    help="Lane name. A name ending in '-glass' claims the app was "
                         "running and drawn, and must carry the three proofs below.")
    ln.add_argument("--artifact", help="The built thing under test, as a path.")
    ln.add_argument("--built-by", help="The command that produced it.")
    ln.add_argument("--attached", help="What witnessed a process from that artifact "
                                       "reaching a display server.")
    ln.add_argument("--capture", help="The capture channel and its per-frame status "
                                      "signal, where the platform has one.")
    ln.add_argument("--cannot-attach", help="A structural reason the lane could not be "
                                            "reached. Its cases become blocked, which "
                                            "is honest; a pass would not be.")
    ln.set_defaults(fn=cmd_lane)

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
