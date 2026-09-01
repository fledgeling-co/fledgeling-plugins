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
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

KINDS = {"requirement": "REQ", "surface": "SURF", "flow": "FLOW", "component": "CMP",
         "case": "CASE", "defect": "DEF", "journey": "JRN"}
WIDTH = {"REQ": 3, "SURF": 3, "FLOW": 3, "CMP": 3, "CASE": 4, "DEF": 3, "JRN": 3}

# The durable boundaries of a journey step, in order. A journey declares which of
# these it cut at; the gate counts the ones it did not. Named rather than free
# text because the census that follows is mechanical, and a boundary nobody can
# enumerate is a boundary nothing checks. See references/sweeps.md sweep O.
JOURNEY_BOUNDARIES = ("request-issued", "server-committed", "provider-effect",
                      "client-persisted", "user-acknowledged")

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
#   unoracled     no property is specified that any check could read
#   blocked       the thing under test never ran, so nothing downstream is valid
#
# `unoracled` is split from `inconclusive` because the two have opposite
# remedies and one word was sending both to the wrong place. `inconclusive`
# is an instrument problem: a property exists and the measurement failed, so
# the fix is a better instrument. `unoracled` is a specification problem:
# nothing was ever named that a check could read, so no instrument will help
# and the fix is to construct an oracle. A verification pipeline reading one
# status cannot tell "nobody looked" from "there is nothing to look at", and
# the second is the one that needs a test written before any authority can
# close it. See references/oracle-construction.md.
#
# n/a and skip are decisions. inconclusive, unoracled and blocked are
# unfinished business, so they hold the gate shut while still being counted and
# explained rather than sitting in the report as an unexplained dash. See
# references/on-glass.md.
UNRESOLVED_REASONED = ("inconclusive", "unoracled", "blocked")

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
                "outcome", "metamorphic", "effect-witness",
                "raster-visual", "interactive-glass", "visual")
# NOT ON THE LADDER ABOVE, AND DELIBERATELY. `ORACLE_RUNGS` is one axis — what
# the case checked against the running product, weakest first. A check over
# source text runs none of that, so it is neither weaker than
# `structural-visual` nor stronger than `presence`; it is off the axis, and
# giving it a position would invent a comparison coverage-model.md §3 does not
# have.
#
# It exists because the alternative was worse. Four cases arrived recording an
# oracle the ladder did not know, so they counted `unrated` — the bucket meaning
# "the tool does not know what this checked" — while being real, armed,
# red-provable instruments: a Swift-source classifier that reports a violation
# and exits 1 on a one-line mutation and exits 0 on the file as written. Their
# clause has no product-side observable at all: a hardcoded `Text("Open log")`
# and a `Text(Copy.openLog)` render identically, so re-expressing them against
# the built product is not available. Recorded as DEF-057.
#
# It buys no effect credit — it is absent from EFFECT_RUNGS and stays absent.
# `covered_source_only` below is the guard that stops it becoming the cheap rung
# a campaign fills up on.
SOURCE_RUNGS = ("source-analysis",)
# A critical flow promises an effect. Only these rungs assert one.
EFFECT_RUNGS = ("outcome", "metamorphic", "effect-witness",
                "raster-visual", "interactive-glass")
# This rung claims an effect landed outside the product's own memory, so it owes
# a recorder and a non-zero count the same way `raster-visual` owes a capture
# method. See `inspect_witness` and references/effect-boundary.md.
WITNESS_RUNGS = ("effect-witness",)

# What a requirement's evidence field may say. `vacuous` is the fifth, and it is
# the one a campaign reaches for after finding that a guarantee held only because
# the capability it constrains never runs: `G(communication -> outbound_443)` is
# true in a product that never communicates. It records a finding rather than
# holding the gate, exactly as `contradicted` does — what holds the gate is the
# dishonest configuration below, an external-effect claim recorded as `observed`
# with no witness behind it.
# `limited` is a STATED CEILING: somebody looked, recorded what no harness here can
# watch, and said when that would change. It is not `reported` — that is the
# project's own account of itself — and it is not the absence of a look. The
# distinction was built in another repository under WAR-0048/WAR-0052, refused
# this schema on the way in, and survived only because rows written straight into
# `inventory.json` never reach the `add` path that validates. Admitting the word
# closes that hole rather than widening it: a row carrying it is now validated
# like any other, and `reckon` grades it `waived` only when the reason and the
# horizon are actually on the row.
REQ_EVIDENCE = ("observed", "reported", "contradicted", "unknown", "vacuous",
                "limited")

# The closed list a requirement declares when its text names an effect outside the
# product's own process. Closed rather than free text because the census that
# follows is mechanical, and a class nobody can enumerate is a class nothing can
# check. `none` is a real answer and the common one.
EFFECT_CLASSES = ("subprocess", "outbound-socket", "inbound-socket", "packet-filter",
                  "multicast", "filesystem-write", "device", "ipc", "none")
EXTERNAL_EFFECTS = tuple(e for e in EFFECT_CLASSES if e != "none")
# Retained so an existing campaign loads rather than silently re-rating its
# cases as `unrated`, and reported as a migration blocker so the split is made
# deliberately. It buys no effect credit in the meantime.
LEGACY_RUNGS = ("visual",)
# These rungs claim pixels, so they must produce pixels. See `inspect_raster`.
RASTER_RUNGS = ("raster-visual",)
# Every rung a case may declare: the product ladder plus the off-axis sets.
ALL_RUNGS = ORACLE_RUNGS + SOURCE_RUNGS

# WHICH PLANE THE EVIDENCE CAME FROM, weakest first.
#
# The oracle rung says what a case checked; the plane says what it checked it
# AGAINST. They are independent, and conflating them is how seven separate
# projects reported "implemented, verified, tested and working" over an in-tree
# mock. A case can stand at `outcome` — a real state change, properly asserted —
# while the thing it changed was a fake peer in the same process.
#
#   in-tree        production code, but the collaborator is a stub or in-memory
#                  double. Proves the state machine; proves nothing about the
#                  world.
#   hermetic       production code against a real protocol peer that is local and
#                  deterministic: a loopback listener, a stdio child, a temp
#                  filesystem, a seeded database.
#   live-glass     the built artifact, running, drawn by a display server, driven
#                  by synthetic events.
#   live-external  the real external system — the vendor's API, the user's
#                  account, the physical device.
#
# A requirement declares the planes its intent actually spans. `check` refuses to
# clear when a declared plane has no passing case on it, which is the mechanical
# form of "an API test does not retire a macOS brief".
EVIDENCE_PLANES = ("in-tree", "hermetic", "live-glass", "live-external")

# A lane whose name ends in `-glass` claims the application was verified while
# actually running and drawn by a display server — a real window, composited,
# photographed. That is a much stronger claim than the same lane run headless,
# and it is the one claim a campaign can make that nothing else can check for
# it, so the lane carries the burden of proving it. See `cmd_lane`.
GLASS_SUFFIX = "-glass"

# `--cannot-attach` is for a structural block that survives a successful
# build (no interactive desktop, no signing identity, Session 0). A reason
# that describes a missing binary is a build job, and recording it as a
# finished limit is how a campaign once left glass closed while the source
# sat unbuilt. See references/on-glass.md §2.
BUILDABLE_GAP_RE = re.compile(
    r"(?is)("
    r"\bnot (?:on disk|built|compiled|yet built)\b|"
    r"\bnever (?:been )?(?:built|compiled|signed)\b|"
    r"\bno (?:signed )?(?:app|binary|artifact|bundle|ipa|apk|exe)\b|"
    r"\bmissing (?:app|artifact|binary|bundle|ipa|apk)\b|"
    r"\bsource (?:only|authored)\b|"
    r"\bglass stays closed\b|"
    r"\bnot yet (?:built|compiled|signed)\b"
    r")"
)


def refuse_buildable_cannot_attach(reason: str) -> None:
    """Exit if `--cannot-attach` is being used to skip a missing build."""
    if BUILDABLE_GAP_RE.search(reason or ""):
        sys.exit(
            f"--cannot-attach refused: {reason!r} describes a missing "
            f"build, not a structural block. Build the artifact with the "
            f"project's documented command, launch it, and record "
            f"--artifact / --built-by / --attached. Use --cannot-attach "
            f"only when a structural block remains after that build "
            f"(no interactive desktop, no signing identity in the "
            f"keychain, Session 0, a display server this host cannot "
            f"reach)."
        )

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
            plane = item.get("plane")
            if plane and plane not in EVIDENCE_PLANES:
                sys.exit(f"case plane '{plane}' is not a plane. One of: "
                         f"{', '.join(EVIDENCE_PLANES)}.")
            rung = item.get("oracle")
            if rung and rung not in ALL_RUNGS:
                sys.exit(f"case oracle '{rung}' is not a rung. One of: {', '.join(ALL_RUNGS)}.")
            # The field is `req`, and the prose everywhere calls it a requirement.
            # A case written with `requirement:` used to be stored intact and then
            # reported as a requirement nothing checks — a blocker pointing at the
            # wrong thing, which cost a round of debugging. Accept the word the
            # documentation uses instead of silently disagreeing with it.
            if "requirement" in item and "req" not in item:
                item["req"] = item.pop("requirement")
                print(f"note: 'requirement' read as 'req' ({item['req']}); "
                      f"the registry field is `req`.")
    elif kind == "requirement":
        # Both fields decide what `check` can conclude, so a typo in either is
        # refused here rather than silently reducing the gate to nothing.
        for item in incoming:
            ev = item.get("evidence")
            if ev and ev not in REQ_EVIDENCE:
                sys.exit(f"requirement evidence '{ev}' is not a class. "
                         f"One of: {', '.join(REQ_EVIDENCE)}.")
            for pl in (item.get("planes") or []):
                if pl not in EVIDENCE_PLANES:
                    sys.exit(f"requirement plane '{pl}' is not a plane. One of: "
                             f"{', '.join(EVIDENCE_PLANES)}.")
            fx = item.get("effect")
            if fx and fx not in EFFECT_CLASSES:
                sys.exit(f"requirement effect '{fx}' is not a class. "
                         f"One of: {', '.join(EFFECT_CLASSES)}.")
    if kind != "case":
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
    if args.recorder or args.effect_class or args.effect_count is not None:
        w = hit.setdefault("witness", {})
        if args.recorder:
            w["recorder"] = args.recorder
        if args.effect_class:
            if args.effect_class not in EFFECT_CLASSES:
                sys.exit(f"effect class '{args.effect_class}' is not a class. "
                         f"One of: {', '.join(EFFECT_CLASSES)}.")
            w["effect"] = args.effect_class
        if args.effect_count is not None:
            w["count"] = args.effect_count
    if args.note:
        hit["note"] = args.note

    save(d, "cases", cases)
    print(f"{hit['id']}: {hit['status']}"
          + (f" · {len(hit['evidence'])} evidence" if hit["evidence"] else "")
          + (" · armed" if hit.get("armed") is True else "")
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

    `--cannot-attach` is for a structural block that survives a successful
    build: no interactive desktop, no signing identity, Session 0, a display
    server this host cannot reach. A missing binary is not that block — build
    it, then attach. The command refuses a cannot-attach reason that describes
    a missing build, so a campaign cannot record glass as finished while the
    source sits unbuilt.
    """
    d = Path(args.dir).resolve()
    campaign = load(d, "campaign", {})
    lanes = campaign.setdefault("laneProof", {})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if args.cannot_attach:
        refuse_buildable_cannot_attach(args.cannot_attach)
        lanes[args.lane] = {"attached": False, "reason": args.cannot_attach,
                            "declaredAt": now}
        save(d, "campaign", campaign)
        print(f"{args.lane}: NOT attached — {args.cannot_attach}")
        print("Its cases resolve to `blocked: <reason>`. A lane that never ran "
              "cannot hold a pass. This is a structural limit, not a missing "
              "build.")
        return 0

    missing = [f for f, v in (("--artifact", args.artifact),
                              ("--built-by", args.built_by),
                              ("--attached", args.attached)) if not v]
    if missing:
        sys.exit(f"A lane claiming on-glass verification needs {', '.join(missing)}. "
                 f"If the artifact is not on disk, build it with the project's "
                 f"documented command and re-run with --artifact / --built-by / "
                 f"--attached. Use --cannot-attach only for a structural block "
                 f"that remains after that build (no interactive desktop, no "
                 f"signing identity, Session 0).")

    artifact = Path(args.artifact)
    if not artifact.exists():
        sys.exit(f"--artifact {artifact} does not exist. Build it with "
                 f"{args.built_by!r}, then re-run this command with the same "
                 f"path. --cannot-attach is for a structural block (no "
                 f"interactive desktop, no signing identity), not for a binary "
                 f"that has not been compiled yet.")

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
              + capped(protected, 10))
    return 0


# ── printing a list without lying about its size ────────────────────────────

def capped(items, limit: int) -> str:
    """A joined list that carries its own denominator, truncated or not.

    A capped list read as a population under-scoped a whole wave of work by ten
    items: this gate printed twelve unwitnessed requirements out of eighteen,
    nothing in the output said so, and the twelve were taken for the set.
    Recorded as DEF-041. The denominator was one `len()` away the whole time.

    The count prints even when nothing was cut — `(showing 3 of 3)` — because a
    reader who has to work out whether truncation happened is back in the
    position that caused the loss. Raising the cap would not have helped: the
    next set is always bigger than the next cap.
    """
    items = list(items)
    text = ", ".join(str(i) for i in items[:limit])
    if len(items) > limit:
        return f"{text} … (showing {limit} of {len(items)})"
    return f"{text} (showing {len(items)} of {len(items)})"


def capped_tail(items, limit: int, indent: str = "    ") -> str:
    """The same denominator for a list printed one row per line.

    Returns the trailing line to print after the rows, always — an empty string
    would be a truncation the reader cannot see.
    """
    items = list(items)
    if len(items) > limit:
        return f"{indent}… (showing {limit} of {len(items)})"
    return f"{indent}(showing {len(items)} of {len(items)})"


def contained_dependency(root: Path, relative: str) -> Path | None:
    """Resolve one declared file without allowing a symlink to leave sourceRoot."""
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            return None
    try:
        resolved = (root / relative).resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None
    return resolved if resolved.is_file() else None


def validated_control_exceptions(d: Path, campaign: dict, trust: dict | None = None) -> tuple[dict[str, set[str]], list[str]]:
    """Run an independently anchored repository validator and verify its complete receipt."""
    published_receipt = d / "control-exception-validation.json"
    if trust is None and not published_receipt.exists():
        return {}, []
    if trust is None:
        return {}, ["control exceptions require an independently anchored validator execution"]
    validator = Path(str(trust.get("validator") or "")).resolve()
    manifest = Path(str(trust.get("manifest") or "")).resolve()
    validator_sha = trust.get("validatorSha256")
    manifest_sha = trust.get("manifestSha256")
    for label, path, digest in (("validator", validator, validator_sha),
                                ("dependency manifest", manifest, manifest_sha)):
        if (not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or
                not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest):
            return {}, [f"control exception {label} does not match its independent trust anchor"]
    try:
        manifest_value = json.loads(manifest.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"control exception dependency manifest is unreadable: {exc}"]
    if (not isinstance(manifest_value, dict) or set(manifest_value) != {"schema", "dependencies"} or
            manifest_value.get("schema") != "control-exception-dependencies/1" or
            not isinstance(manifest_value.get("dependencies"), list) or
            not manifest_value["dependencies"]):
        return {}, ["control exception dependency manifest has fields outside its exact v1 schema"]
    required_dependencies: set[str] = set()
    for relative in manifest_value["dependencies"]:
        if (not isinstance(relative, str) or not relative or Path(relative).is_absolute() or
                ".." in Path(relative).parts or relative in required_dependencies):
            return {}, ["control exception dependency manifest contains an invalid or duplicate path"]
        required_dependencies.add(relative)
    source_root_raw = campaign.get("sourceRoot")
    if not isinstance(source_root_raw, str) or not source_root_raw:
        return {}, ["control exception validation requires campaign.sourceRoot"]
    root = (d / source_root_raw).resolve()
    for relative in required_dependencies:
        if contained_dependency(root, relative) is None:
            return {}, [f"control exception dependency escapes sourceRoot or uses a symlink: {relative}"]
    try:
        validator_relative = str(validator.relative_to(root))
    except ValueError:
        return {}, ["control exception validator is outside campaign.sourceRoot"]
    if validator_relative not in required_dependencies:
        return {}, ["control exception dependency manifest omits the anchored validator"]
    with tempfile.TemporaryDirectory(prefix="control-exception-") as temporary:
        receipt = Path(temporary) / "receipt.json"
        try:
            run = subprocess.run(
                [sys.executable, str(validator), "--campaign", str(d), "--root", str(root),
                 "--write-validation", str(receipt)], cwd=root, stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
                check=False)
        except subprocess.TimeoutExpired:
            return {}, ["control exception validator did not complete before the timeout"]
        except OSError:
            return {}, ["control exception validator could not be executed"]
        if type(run.returncode) is not int or run.returncode != 0:
            return {}, [f"control exception validator failed with exit {run.returncode}; "
                        "validator output was suppressed"]
        if not receipt.is_file():
            return {}, ["control exception validator exited successfully without writing its receipt"]
        try:
            value = json.loads(receipt.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            return {}, [f"control exception validation receipt is unreadable: {exc}"]
    problems: list[str] = []
    expected_keys = {"schema", "validatorExit", "dependencies", "exceptions"}
    if not isinstance(value, dict) or set(value) != expected_keys:
        return {}, ["control exception validation receipt has fields outside its exact v1 schema"]
    if (value.get("schema") != "control-exception-validation/1" or
            type(value.get("validatorExit")) is not int or value.get("validatorExit") != 0):
        problems.append("control exception validation receipt does not record a successful v1 validator run")
    dependencies = value.get("dependencies")
    if not isinstance(dependencies, dict) or not dependencies:
        problems.append("control exception validation names no hashed dependencies")
    else:
        for relative, digest in dependencies.items():
            if (not isinstance(relative, str) or not relative or Path(relative).is_absolute() or
                    ".." in Path(relative).parts or not isinstance(digest, str) or
                    re.fullmatch(r"[0-9a-f]{64}", digest) is None):
                problems.append("control exception validation contains an invalid dependency entry")
                continue
            path = contained_dependency(root, relative)
            if path is None:
                problems.append(
                    f"control exception dependency escapes sourceRoot or uses a symlink: {relative}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                problems.append(f"control exception dependency changed after validation: {relative}")
        if set(dependencies) != required_dependencies:
            problems.append("control exception validator receipt does not match the complete required dependency manifest")
        for required in (d / "inventory.json", d / "cases.json"):
            try:
                relative = str(required.resolve().relative_to(root))
            except ValueError:
                problems.append(f"control exception validation cannot bind {required.name} outside sourceRoot")
                continue
            if relative not in dependencies:
                problems.append(f"control exception validation does not bind {relative}")
    inventory = load(d, "inventory", {"surface": []})
    declared = {row["id"]: set(map(str, row.get("controls") or []))
                for row in inventory.get("surface", [])}
    statuses = {row["id"]: state_of(row.get("status", "open")) for row in load(d, "cases", [])}
    exceptions = value.get("exceptions")
    index: dict[str, set[str]] = {}
    seen: set[tuple[str, str]] = set()
    if not isinstance(exceptions, list):
        problems.append("control exception validation exceptions must be an array")
    else:
        for row in exceptions:
            keys = {"id", "surface", "control", "containment", "disposition"}
            if not isinstance(row, dict) or set(row) != keys:
                problems.append("control exception validation contains a malformed exception row")
                continue
            if row.get("disposition") != "permanent-exception" or any(
                    not isinstance(row.get(key), str) or not row[key]
                    for key in ("id", "surface", "control", "containment")):
                problems.append("control exception validation contains an invalid permanent exception")
                continue
            key = (row["surface"], row["control"])
            if key in seen:
                problems.append(f"control exception validation duplicates {row['surface']}::{row['control']}")
                continue
            seen.add(key)
            if row["control"] not in declared.get(row["surface"], set()):
                problems.append(f"control exception names an undeclared control on {row['surface']}")
                continue
            if statuses.get(row["containment"]) != "pass":
                problems.append(f"control exception containment {row['containment']} is not passing")
                continue
            index.setdefault(row["surface"], set()).add(row["control"])
    return ({}, problems) if problems else (index, [])


# ── the gate ────────────────────────────────────────────────────────────────

def audit(d: Path, control_exception_trust: dict | None = None) -> dict:
    campaign = load(d, "campaign", {})
    inventory = load(d, "inventory", {"requirement": [], "surface": [], "flow": [], "component": []})
    cases = load(d, "cases", [])
    permanent_exceptions, exception_validation_problems = validated_control_exceptions(
        d, campaign, control_exception_trust)

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
              "inconclusive": 0, "unoracled": 0, "blocked": 0, "open": 0}
    open_ids, unevidenced, armed = [], [], 0
    invalid_armed: list[str] = []
    hollow_witness: list[str] = []
    hollow_source: list[str] = []
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

        if "armed" in c and type(c["armed"]) is not bool:
            invalid_armed.append(
                f"{c['id']} has armed={c['armed']!r}; armed must be a JSON boolean")
        if st == "pass":
            if not c.get("evidence"):
                unevidenced.append(c["id"])
            if c.get("armed") is True:
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

        # A rung that claims an effect landed outside the product must say what
        # saw it and how many. Zero is a reading and it is not a pass: the whole
        # condition this rung exists for is a suite that cannot tell "did the
        # right thing" from "did nothing". references/effect-boundary.md §5.
        if c.get("oracle") in WITNESS_RUNGS and st == "pass":
            w = c.get("witness") or {}
            if not w.get("recorder"):
                hollow_witness.append(
                    f"{c['id']} claims effect-witness and names no recorder")
            if not w.get("effect"):
                hollow_witness.append(
                    f"{c['id']} claims effect-witness and names no effect class")
            elif w["effect"] not in EFFECT_CLASSES:
                hollow_witness.append(
                    f"{c['id']} names effect class '{w['effect']}', which is not one of "
                    f"{', '.join(EFFECT_CLASSES)}")
            if not isinstance(w.get("count"), int) or w.get("count", 0) < 1:
                hollow_witness.append(
                    f"{c['id']} claims effect-witness with count {w.get('count')!r} — "
                    f"a witness that saw nothing is the condition, not the proof")

        # The same obligation shape one axis over. A source-analysis pass owes
        # the analyzer that ran and the denominator it ran over, because "the
        # grep found nothing" is the reading a grep gives when it is pointed at
        # the wrong file, and the two are indistinguishable without the count.
        if c.get("oracle") in SOURCE_RUNGS and st == "pass":
            src = c.get("source") or {}
            if not src.get("analyzer"):
                hollow_source.append(
                    f"{c['id']} claims source-analysis and names no analyzer")
            if not isinstance(src.get("examined"), int) or src.get("examined", 0) < 1:
                hollow_source.append(
                    f"{c['id']} claims source-analysis over {src.get('examined')!r} "
                    f"unit(s) — a search with no denominator cannot tell an empty "
                    f"result from an empty search")

    duplicate_artifacts = {h: ids for h, ids in seen_artifacts.items() if len(ids) > 1}

    # THE PUBLISHED SHOTS, WHICH ARE THE PART PEOPLE LOOK AT.
    #
    # Everything above audits case evidence on the raster rungs. The evidence
    # page renders a different set: the `shot` field on each surface and each
    # flow step. Measured 20 Aug 2026: a campaign passed every check here while
    # 20 published shots showed three unrelated documents and 20 files held six
    # distinct images — because no rule in this function had ever read a `shot`.
    # Provenance is `capture-lineage.py`'s job; what is decidable from the bytes
    # is decided here, where the rest of the artifact rules already live.
    published_shots: dict[str, str] = {}
    for srec in inventory.get("surface", []):
        if srec.get("shot"):
            published_shots[srec["id"]] = srec["shot"]
    for frec in inventory.get("flow", []):
        for step in frec.get("steps", []):
            if step.get("shot") and step.get("id"):
                published_shots[step["id"]] = step["shot"]

    bad_shots, shot_hashes, filename_only = [], {}, []
    for sid, shot in sorted(published_shots.items()):
        info = inspect_raster((d / shot) if not Path(shot).is_absolute() else Path(shot))
        if info["reason"]:
            bad_shots.append(f"{sid} → {shot}: {info['reason']}")
        elif info["sha256"]:
            shot_hashes.setdefault(info["sha256"], []).append(sid)
    for srec in inventory.get("surface", []):
        if srec.get("shot") and srec.get("shotProvenance") == "filename":
            filename_only.append(srec["id"])
    # A share can be legitimate, and the blocker below used to be unfollowable when it
    # was: it said "declare a genuine share in captures.json" while nothing here read
    # the declaration, and re-capturing a genuinely shared surface reproduces the same
    # bytes, so neither branch of the instruction could clear it. Read the same
    # `sharesWith` declaration capture-lineage.py's shared pass reads — every member of
    # the group must name the others, so declaring one side is not enough.
    manifest_path = d / "evidence/shots/captures.json"
    shares: dict[str, set[str]] = {}
    if manifest_path.exists():
        try:
            for e in json.loads(manifest_path.read_text()):
                sid_for_path = {v: k for k, v in published_shots.items()}.get(str(e.get("path", "")))
                if sid_for_path and e.get("sharesWith") and e.get("sharesReason"):
                    shares[sid_for_path] = set(e["sharesWith"])
        except (json.JSONDecodeError, OSError):
            shares = {}

    def share_declared(ids: list[str]) -> bool:
        return all(set(ids) - {s} <= shares.get(s, set()) for s in ids)

    duplicate_shots = {h: ids for h, ids in shot_hashes.items()
                       if len(ids) > 1 and not share_declared(ids)}
    declared_shares = {h: ids for h, ids in shot_hashes.items()
                       if len(ids) > 1 and share_declared(ids)}

    uncovered = [sid for sid, cs in by_surface.items() if not cs]

    # ── THE LANE LEDGER ─────────────────────────────────────────────────────
    #
    # A campaign-wide oracle mix hides a lane. Measured 24 Aug 2026: a campaign
    # over a web app and a native macOS app reported `32 pass · 32/32 armed ·
    # Oracles: structural 10 · outcome 14 · effect-witness 8` and cleared every
    # gate. The web lane carried 156 driven specs; the native lane carried three
    # cases, all of them socket and layer telemetry, none of them at an effect
    # rung. The app shipped with six sidebar destinations rendering one
    # placeholder view and every button wired to an empty closure, and no number
    # on the verdict page was false. references/inert-ui.md.
    #
    # So the mix is reported per lane as well as in total, and a lane whose every
    # passing case sits below `outcome` holds the gate. That is the third failure
    # mode at lane granularity: the parts were checked on paper and the lane was
    # reported as the product.
    lane_ledger: dict[str, dict] = {}
    for c in cases:
        lane = c.get("lane") or "unassigned"
        row = lane_ledger.setdefault(
            lane, {"cases": 0, "pass": 0, "effect": 0, "armed": 0, "rungs": {}})
        row["cases"] += 1
        rung = c.get("oracle") if c.get("oracle") in ALL_RUNGS else "unrated"
        row["rungs"][rung] = row["rungs"].get(rung, 0) + 1
        if state_of(c.get("status", "open")) == "pass":
            row["pass"] += 1
            if c.get("armed") is True:
                row["armed"] += 1
            if c.get("oracle") in EFFECT_RUNGS:
                row["effect"] += 1
    lanes_presence_only = [f"{lane} ({row['pass']} passing case(s), none above `structural`)"
                           for lane, row in sorted(lane_ledger.items())
                           if row["pass"] and not row["effect"]]

    # ── THE JOURNEY LEDGER ──────────────────────────────────────────────────
    #
    # A journey is a history rather than a state, so it gets a denominator of its
    # own: no other count in this file can say whether the multi-step task was
    # ever driven end to end. Optional — absent means NOT DECLARED rather than
    # clean — because a product with no multi-step task owes no journeys.
    #
    # Two gates, and both come from measured results rather than from taste.
    # A journey declaring `critical` owes a boundary cut at every one of the five
    # durable boundaries: the Android data-loss benchmark holds 110 reproducible
    # faults of exactly this shape, and TimeMachine's client-only state
    # restoration is why a client snapshot alone cannot close one. And a
    # differential claim owes a change-intent manifest, because RegDroid measured
    # a 64% false-positive rate on previous-build diffs of which 93% were
    # intended changes — an ungoverned diff wall is not a gate, it is a queue.
    journeys = inventory.get("journey", [])
    by_journey: dict[str, list[dict]] = {j["id"]: [] for j in journeys}
    for c in cases:
        jid = c.get("journey")
        if jid in by_journey:
            by_journey[jid].append(c)

    bad_boundary, journeys_uncut, journeys_uncased = [], [], []
    for j in journeys:
        cut = [str(b) for b in (j.get("boundariesCut") or [])]
        strays = [b for b in cut if b not in JOURNEY_BOUNDARIES]
        if strays:
            bad_boundary.append(
                f"{j['id']} names boundary {capped(strays, 3)}, not one of "
                f"{', '.join(JOURNEY_BOUNDARIES)}")
        if not by_journey.get(j["id"]):
            journeys_uncased.append(j["id"])
        if j.get("critical"):
            missing = [b for b in JOURNEY_BOUNDARIES if b not in cut]
            if missing:
                journeys_uncut.append(f"{j['id']} ({len(missing)} of "
                                      f"{len(JOURNEY_BOUNDARIES)} uncut: {capped(missing, 3)})")
    boundaries_total = len(journeys) * len(JOURNEY_BOUNDARIES)
    boundaries_cut = sum(
        len({str(b) for b in (j.get("boundariesCut") or [])} & set(JOURNEY_BOUNDARIES))
        for j in journeys)

    # A case claiming it compared this build against the previous one owes the
    # manifest that says which differences were intended. Without it the run
    # cannot separate a regression from a shipped change, and 93% of what it
    # reports will be the second.
    differential_unmanifested = [
        c["id"] for c in cases
        if c.get("comparedAgainstBuild") and not c.get("changeIntentManifest")]

    # ── THE CONTROL CENSUS ──────────────────────────────────────────────────
    #
    # A surface may list the controls it offers under `controls`, and a case
    # records which of them it actuated under `actuates`. Both are optional and
    # absent means NOT DECLARED rather than clean, because a census over an
    # undeclared population is the empty-denominator failure this file already
    # carries three instances of.
    #
    # The defect this counts: `Button("Pull Proof") {}` compiles, renders, carries
    # a role and an accessible name, passes a contrast gate, accepts a click, and
    # runs an empty closure. Every presence-rung and structural-rung check passes.
    # Only actuating it and reading a state the control was supposed to change
    # separates a wired control from an inert one.
    declared_controls: dict[str, list[str]] = {
        s["id"]: [str(x) for x in (s.get("controls") or [])]
        for s in surfaces if s.get("controls")}
    actuated: dict[str, set[str]] = {sid: set() for sid in declared_controls}
    # Driven is a weaker fact than actuated and it is the one that separates the
    # two ways a surface can sit at zero: a control nobody has touched, and a
    # control that was pressed and did nothing. Any case naming a declared control
    # under `actuates` drove it, whatever its rung and whatever its status —
    # a failing case that pressed a button and found the button dead is the whole
    # measurement, and reading it as "nobody looked" is the report defect below.
    driven: dict[str, set[str]] = {sid: set() for sid in declared_controls}
    unknown_actuations: list[str] = []
    for c in cases:
        names = c.get("actuates") or []
        if not names:
            continue
        sid = c.get("surface")
        if sid not in declared_controls:
            unknown_actuations.append(
                f"{c['id']} actuates {len(names)} control(s) on "
                f"{sid or 'no surface'}, which declares none")
            continue
        known = set(declared_controls[sid])
        strays = [n for n in names if n not in known]
        if strays:
            unknown_actuations.append(
                f"{c['id']} actuates {capped(strays, 4)} — not among "
                f"{sid}'s declared controls")
        driven[sid] |= (set(names) & known)
        # Only a passing case at an effect rung actuated anything. A presence-rung
        # pass that clicked a control and asserted the control is still there has
        # measured the click and not the effect.
        if state_of(c.get("status", "open")) == "pass" and c.get("oracle") in EFFECT_RUNGS:
            actuated[sid] |= (set(names) & known)
    controls_total = sum(len(v) for v in declared_controls.values())
    controls_actuated = sum(len(actuated[sid]) for sid in declared_controls)
    surfaces_inert = [
        f"{sid} ({len(declared_controls[sid])} control(s) declared, 0 actuated)"
        for sid in sorted(declared_controls) if not actuated[sid]]
    # Both halves of that list still block, and neither is a waiver: the split is
    # in what the refusal SAYS, not in what it decides. It exists because one
    # sentence covered two findings that owe opposite work. A surface nobody drove
    # owes a RUN — the campaign has not looked. A surface whose every declared
    # control was driven and where not one drive produced a passing effect-rung
    # result owes a REPAIR — the campaign looked, and the product is what failed.
    # Telling the second it has not been actuated is the report defect: it reads
    # as an incomplete campaign when it is a complete measurement of dead controls.
    # There is no per-surface field behind this. A surface moves between the two
    # lines only by a case naming its controls, which the stray check above already
    # governs, and neither line is a route to a green verdict.
    declared_count = {sid: len(set(v)) for sid, v in declared_controls.items()}
    owed_controls = {
        sid: set(names) - permanent_exceptions.get(sid, set())
        for sid, names in declared_controls.items()
    }
    surfaces_inert_undriven = [
        f"{sid} ({declared_count[sid]} declared, {len(driven[sid])} driven, "
        f"{len(owed_controls[sid] - driven[sid])} non-excepted never driven)"
        for sid in sorted(declared_controls)
        if not actuated[sid] and owed_controls[sid] - driven[sid]]
    surfaces_inert_measured = [
        f"{sid} ({len(driven[sid])} of {declared_count[sid]} control(s) driven, 0 actuated)"
        for sid in sorted(declared_controls)
        if not actuated[sid] and owed_controls[sid] and not (owed_controls[sid] - driven[sid])]

    # ── DESTINATION DISTINCTNESS ────────────────────────────────────────────
    #
    # A surface that is one destination of a navigation shell names the shell
    # under `destinationOf`. For destinations of one shell, two captures with the
    # same bytes are the defect rather than a saving: it is the shell rendering
    # one view under every label. A declared share does not excuse it here, which
    # is the one place this gate is stricter than the general duplicate rule
    # above — elsewhere two surfaces can legitimately be one address, and between
    # two destinations of one menu they cannot.
    shells: dict[str, list[str]] = {}
    for s in surfaces:
        shell = s.get("destinationOf")
        if shell:
            shells.setdefault(str(shell), []).append(s["id"])
    sid_of_hash = {sid: h for h, ids in shot_hashes.items() for sid in ids}
    collapsed_destinations: list[str] = []
    for shell, dests in sorted(shells.items()):
        groups: dict[str, list[str]] = {}
        for sid in dests:
            h = sid_of_hash.get(sid)
            if h:
                groups.setdefault(h, []).append(sid)
        for h, ids in groups.items():
            if len(ids) > 1:
                collapsed_destinations.append(
                    f"{shell}: {', '.join(sorted(ids))} publish one identical image")
    destinations_uncased = [
        f"{shell}: {capped([s for s in dests if not by_surface.get(s)], 6)}"
        for shell, dests in sorted(shells.items())
        if any(not by_surface.get(s) for s in dests)]

    # A requirement with no case is the campaign's real gap: it is something the
    # project says it does that nothing checked. Deferred requirements are exempt,
    # because not building them is the recorded decision.
    reqs = inventory.get("requirement", [])
    traced = {r for c in cases for r in ([c["req"]] if isinstance(c.get("req"), str)
                                         else c.get("req", []) or [])}
    untested_reqs = [r["id"] for r in reqs
                     if r["id"] not in traced and r.get("class") != "deferred"]

    # THE EFFECT CENSUS.
    #
    # Until 0.9.0 this function never read a requirement's `evidence` field at
    # all: the only requirement-level rule was "does some case cite this id".
    # A campaign therefore recorded "runner communication is outbound pull only
    # via HTTPS/WSS on TCP 443" as `observed` over a product with no HTTP client
    # in its dependency tree, and cleared every gate — 230 cases, 220 of them
    # mutation-armed. Arming mutates the system; a guarantee that holds because
    # the constrained capability never runs is only visible by mutating the
    # specification. references/effect-boundary.md.
    #
    # What blocks is the dishonest configuration, not the honest one. A
    # requirement recorded `vacuous` is a finding and is reported like
    # `contradicted`. A requirement claiming an external effect AND recorded
    # `observed` AND backed by no effect-witness case is the configuration that
    # produced the failure above, so that is the one that holds the gate.
    by_req: dict[str, list[dict]] = {}
    for c in cases:
        for rid in ([c["req"]] if isinstance(c.get("req"), str) else c.get("req", []) or []):
            by_req.setdefault(rid, []).append(c)

    vacuous_reqs = [r["id"] for r in reqs if r.get("evidence") == "vacuous"]
    effect_reqs = [r for r in reqs if r.get("effect") in EXTERNAL_EFFECTS]
    # `add` refuses an unrecognised effect class, but a registry edited by hand
    # never passes through it — and an unrecognised class simply fails the
    # membership test above and drops out of the census, which is
    # indistinguishable from a requirement that claims no external effect at all.
    bad_effect_class = [
        f"{r['id']} declares effect '{r['effect']}', which is not one of "
        f"{', '.join(EFFECT_CLASSES)}"
        for r in reqs if r.get("effect") and r["effect"] not in EFFECT_CLASSES]
    unbacked_effects = [
        f"{r['id']} claims a {r['effect']} effect and is recorded `observed`, and no "
        f"case backing it stands at effect-witness"
        for r in effect_reqs
        if r.get("evidence") == "observed"
        and not any(c.get("oracle") in WITNESS_RUNGS and state_of(c.get("status", "open")) == "pass"
                    for c in by_req.get(r["id"], []))
    ]
    # Counted, never derived. This was `len(effect_reqs) - len(unbacked) - len(vacuous)`,
    # which credited every requirement that was neither as witnessed — so one recorded
    # `reported`, with an external effect and no witness anywhere, was reported as an
    # effect somebody had seen. A number that reads as a measurement and is a subtraction
    # is the failure this whole file is built against.
    witnessed_effects = sum(
        1 for r in effect_reqs
        if any(c.get("oracle") in WITNESS_RUNGS and state_of(c.get("status", "open")) == "pass"
               for c in by_req.get(r["id"], [])))
    unwitnessed_effects = [
        f"{r['id']} ({r.get('evidence')})" for r in effect_reqs
        if not any(c.get("oracle") in WITNESS_RUNGS and state_of(c.get("status", "open")) == "pass"
                   for c in by_req.get(r["id"], []))
        and r.get("evidence") != "vacuous"
        and r["id"] not in {u.split()[0] for u in unbacked_effects}]

    # THE GUARD ON THE OFF-AXIS RUNG. A requirement may rest on source analysis
    # alone only where it claims no effect outside the process — a property OF
    # the source, like "no user-facing copy is hardcoded in this view", is what
    # this rung is for. A requirement that names an external effect and is
    # covered only by a reader of source text has had its effect checked by
    # nothing, and that is the campaign's founding failure wearing a new label.
    covered_source_only = []
    for r in reqs:
        passing = [c for c in by_req.get(r["id"], [])
                   if state_of(c.get("status", "open")) == "pass"]
        if not passing or not all(c.get("oracle") in SOURCE_RUNGS for c in passing):
            continue
        if r.get("effect") in EXTERNAL_EFFECTS:
            covered_source_only.append(
                f"{r['id']} claims a {r['effect']} effect and every passing case "
                f"backing it stands on source-analysis, which reads text and runs "
                f"nothing")

    # ── THE EVIDENCE-PLANE CENSUS ───────────────────────────────────────────
    #
    # Measured across seven projects in one week: every one reported its backlog
    # implemented, verified and tested, and every one turned out to have retired
    # stated intent on evidence from a weaker plane than the intent lived on. A
    # compiler suite retiring a desktop app. A mock Drive peer retiring live
    # sync. 2,375 green unit tests over an app whose buttons were empty closures.
    #
    # Nothing in the registry could see it, because the oracle rung was honest
    # every time: those cases really did assert an outcome. They asserted it
    # against a double.
    plane_of: dict[str, str] = {}
    for c in cases:
        if c.get("plane"):
            plane_of[c["id"]] = c["plane"]
    plane_counts = {p: 0 for p in EVIDENCE_PLANES}
    for c in cases:
        pl = c.get("plane")
        if pl in plane_counts and state_of(c.get("status", "open")) == "pass":
            plane_counts[pl] += 1

    unreached_planes = []
    for r in reqs:
        declared = [p for p in (r.get("planes") or []) if p in EVIDENCE_PLANES]
        if not declared:
            continue
        reached = {c.get("plane") for c in by_req.get(r["id"], [])
                   if state_of(c.get("status", "open")) == "pass"}
        missing = [p for p in declared if p not in reached]
        if missing:
            unreached_planes.append(
                f"{r['id']} declares {capped(declared, 4)} and has no passing case on "
                f"{capped(missing, 3)}")
    cases_unplaned = [c["id"] for c in cases
                      if state_of(c.get("status", "open")) == "pass" and not c.get("plane")]

    # What the cases actually check. A case with no declared rung counts as
    # unrated, never as adequate — the whole point is that a plan cannot look
    # complete by omission.
    mix = {r: 0 for r in ALL_RUNGS}
    mix["unrated"] = 0
    for c in cases:
        mix[c.get("oracle") if c.get("oracle") in ALL_RUNGS else "unrated"] += 1

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
    # Reported beside the blockers and counted apart from them: a thing worth a
    # reader's attention that the gate has no mechanical case for refusing on.
    # Kept out of `clear` deliberately, so an advisory can never quietly become a
    # gate and a gate can never quietly become an advisory.
    blockers_advisory: list[str] = []
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
    if invalid_armed:
        blockers.append(f"{len(invalid_armed)} case(s) have non-boolean armed values "
                        f"({capped(invalid_armed, 3)}) — truthiness is not mutation evidence")
    if exception_validation_problems:
        blockers.append(f"control exception validation failed: "
                        f"{capped(exception_validation_problems, 3)}")
    if open_ids:
        blockers.append(f"{len(open_ids)} case(s) still open")
    if counts["inconclusive"]:
        blockers.append(f"{counts['inconclusive']} case(s) inconclusive — attempted, "
                        f"and the instrument could not measure. Not a pass and not "
                        f"an n/a: 'we do not know' is a weaker claim than 'no "
                        f"difference found' and a different one from 'does not apply'")
    if counts["unoracled"]:
        blockers.append(f"{counts['unoracled']} case(s) unoracled — no property is "
                        f"specified that any check could read, so no instrument will "
                        f"settle them. These need an oracle built before any authority "
                        f"can close them; see references/oracle-construction.md")
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
                        f"rung ({capped(legacy_rung, 5)}) — split each into "
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
    if bad_shots:
        blockers.append(f"{len(bad_shots)} published shot(s) that are not usable captures "
                        f"— the evidence page renders these as the product")
    if duplicate_shots:
        n = sum(len(v) for v in duplicate_shots.values())
        blockers.append(f"{n} published shot(s) across {len(duplicate_shots)} image(s) "
                        f"show the same picture under different subjects "
                        f"({'; '.join(capped(v, 4) for v in list(duplicate_shots.values())[:3])}"
                        f"{'; …' if len(duplicate_shots) > 3 else ''}) "
                        f"— a wall whose cells repeat is a gallery, not a survey. Declare a "
                        f"genuine share in captures.json, or capture each subject")
    if filename_only:
        blockers.append(f"{len(filename_only)} shot(s) bound to their subject by filename "
                        f"alone ({capped(filename_only, 5)}) — run "
                        f"`capture-lineage.py <dir> --gate`; a filename is not evidence "
                        f"of what a picture depicts")
    if invalid_interactive_glass:
        blockers.append(f"{len(invalid_interactive_glass)} case(s) claiming interactive-glass "
                        f"on non-glass lane(s)")
    if uncovered:
        blockers.append(f"{len(uncovered)} surface(s) with no case at all")
    if lanes_presence_only:
        # Reported, not blocked, and the distinction is a measurement rather than
        # a softening. On the campaign this ledger was written against, the native
        # lane DID carry an effect-witness case — a loopback socket recorder — so a
        # rule of the form "every lane owes one effect rung" would have cleared it
        # and the app would still have shipped with six dead destinations. The two
        # blockers that follow are the ones aimed at that defect. This line is here
        # because a lane at zero is worth a reader's attention even where the gate
        # has nothing mechanical to say about it.
        blockers_advisory.append(
            f"{len(lanes_presence_only)} lane(s) whose every passing case sits below "
            f"`outcome` ({capped(lanes_presence_only, 3)}) — proved to render, not to work")
    if surfaces_inert_undriven:
        blockers.append(f"{len(surfaces_inert_undriven)} surface(s) declaring control(s) "
                        f"nothing has driven ({capped(surfaces_inert_undriven, 3)}) — a "
                        f"control renders, carries a name and accepts a click whether or "
                        f"not its handler does anything, so this owes a RUN")
    if surfaces_inert_measured:
        blockers.append(f"{len(surfaces_inert_measured)} surface(s) whose every declared "
                        f"control was driven and not one drive produced a passing "
                        f"effect-rung result ({capped(surfaces_inert_measured, 3)}) — the "
                        f"campaign pressed them and read nothing back, so this owes a "
                        f"REPAIR rather than a run, and stays red until the control does "
                        f"something a case can pass on")
    if unknown_actuations:
        blockers.append(f"{len(unknown_actuations)} case(s) actuating a control their surface "
                        f"never declared ({capped(unknown_actuations, 2)}) — add the control "
                        f"to the surface, so the census has a denominator to count against")
    if unreached_planes:
        blockers.append(f"{len(unreached_planes)} requirement(s) declaring a plane no passing "
                        f"case reaches ({capped(unreached_planes, 2)}) — evidence from one "
                        f"plane does not retire intent on another, which is how a compiler "
                        f"suite comes to stand for a desktop application")
    if bad_boundary:
        blockers.append(f"{len(bad_boundary)} journey(s) naming a boundary that is not one "
                        f"of the five ({capped(bad_boundary, 2)}) — a boundary nobody can "
                        f"enumerate is a boundary nothing cuts at")
    if journeys_uncut:
        blockers.append(f"{len(journeys_uncut)} critical journey(s) not cut at every durable "
                        f"boundary ({capped(journeys_uncut, 3)}) — an uninterrupted journey "
                        f"proves the happy path and says nothing about partial completion, "
                        f"which is where the measured fault corpus for this shape lives")
    if journeys_uncased:
        blockers.append(f"{len(journeys_uncased)} journey(s) with no case at all "
                        f"({capped(journeys_uncased, 4)})")
    if differential_unmanifested:
        blockers.append(f"{len(differential_unmanifested)} case(s) comparing against a previous "
                        f"build with no change-intent manifest "
                        f"({capped(differential_unmanifested, 3)}) — a measured 64% of such "
                        f"differences are intended changes, so an unmanifested diff cannot "
                        f"separate a regression from a shipped feature")
    if collapsed_destinations:
        blockers.append(f"{len(collapsed_destinations)} navigation shell(s) whose destinations "
                        f"publish one identical image ({capped(collapsed_destinations, 2)}) — "
                        f"between two destinations of one menu, identical bytes are the "
                        f"defect rather than a share")
    if destinations_uncased:
        blockers.append(f"{len(destinations_uncased)} navigation shell(s) with a destination "
                        f"no case reaches ({capped(destinations_uncased, 2)})")
    if unevidenced:
        blockers.append(f"{len(unevidenced)} pass(es) naming no evidence artifact")
    if untested_reqs:
        blockers.append(f"{len(untested_reqs)} requirement(s) no case traces to")
    if hollow_source:
        blockers.append(f"{len(hollow_source)} source-analysis claim(s) with no analyzer "
                        f"or no examined count — a search with no denominator cannot "
                        f"tell an empty result from an empty search")
    if covered_source_only:
        blockers.append(f"{len(covered_source_only)} requirement(s) claiming an external "
                        f"effect and covered by source-analysis alone — source analysis "
                        f"is off the product ladder and runs nothing, so it cannot be the "
                        f"only thing standing behind an effect")
    if hollow_witness:
        blockers.append(f"{len(hollow_witness)} effect-witness claim(s) with no recorder, "
                        f"no effect class, or a count of zero — a witness that saw nothing "
                        f"is the condition this rung exists to detect")
    if bad_effect_class:
        blockers.append(f"{len(bad_effect_class)} requirement(s) declaring an effect class "
                        f"the census does not recognise — an unrecognised class drops out "
                        f"of the count rather than failing, so it reads as no effect at all")
    if unbacked_effects:
        blockers.append(f"{len(unbacked_effects)} requirement(s) claiming an effect outside "
                        f"the product and recorded `observed` with no effect-witness case "
                        f"behind them — the shape that passed 230 cases over a product that "
                        f"performed no external I/O")
    if presence_only:
        blockers.append(f"{len(presence_only)} critical flow(s) proved only by "
                        f"presence-level cases")
    if flow_atom_gaps:
        blockers.append(f"{len(flow_atom_gaps)} critical flow(s) with declared atoms "
                        f"lacking effect-level or interactive-glass verification")
    if critical_carried:
        blockers.append(f"{len(critical_carried)} critical flow(s) whose every effect "
                        f"case was carried forward rather than re-run "
                        f"({capped(critical_carried, 5)}) — a critical flow is the "
                        f"always-run floor")
    if carried_unbased:
        blockers.append(f"{len(carried_unbased)} carried case(s) naming no selection "
                        f"basis ({capped(carried_unbased, 5)}) — "
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
    unavailable = (counts["inconclusive"] + counts["unoracled"]
                   + counts["blocked"] + counts["n/a"])
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
        "badShots": bad_shots,
        "duplicateShots": duplicate_shots,
        "declaredShares": declared_shares,
        "filenameOnlyShots": filename_only,
        "publishedShots": len(published_shots),
        "distinctPublishedImages": len(shot_hashes),
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
        "requirementsVacuous": vacuous_reqs,
        "effectRequirements": len(effect_reqs),
        "effectRequirementsWitnessed": witnessed_effects,
        "effectRequirementsUnbacked": unbacked_effects,
        "effectRequirementsUnwitnessed": unwitnessed_effects,
        "effectClassUnrecognised": bad_effect_class,
        "hollowWitnesses": hollow_witness,
        "hollowSourceClaims": hollow_source,
        "requirementsSourceOnly": covered_source_only,
        "surfaces": len(surfaces),
        "surfacesUncovered": uncovered,
        "planeCounts": plane_counts,
        "unreachedPlanes": unreached_planes,
        "casesUnplaned": cases_unplaned,
        "journeys": len(journeys),
        "journeysCritical": sum(1 for j in journeys if j.get("critical")),
        "journeysUncut": journeys_uncut,
        "journeysUncased": journeys_uncased,
        "boundariesCut": boundaries_cut,
        "boundariesTotal": boundaries_total,
        "badBoundaryNames": bad_boundary,
        "differentialUnmanifested": differential_unmanifested,
        "laneLedger": lane_ledger,
        "lanesPresenceOnly": lanes_presence_only,
        "controlsDeclared": controls_total,
        "controlsActuated": controls_actuated,
        "surfacesDeclaringControls": len(declared_controls),
        "surfacesInert": surfaces_inert,
        "surfacesInertUndriven": surfaces_inert_undriven,
        "surfacesInertMeasured": surfaces_inert_measured,
        "controlExceptionsValidated": sum(len(v) for v in permanent_exceptions.values()),
        "controlExceptionValidationProblems": exception_validation_problems,
        "unknownActuations": unknown_actuations,
        "navigationShells": {k: sorted(v) for k, v in shells.items()},
        "collapsedDestinations": collapsed_destinations,
        "destinationsUncased": destinations_uncased,
        "flows": len(flows),
        "flowsPresenceOnly": presence_only,
        "components": len(inventory.get("component", [])),
        "cases": len(cases),
        "counts": counts,
        "oracleMix": mix,
        "armed": armed,
        "invalidArmed": invalid_armed,
        "armedOfPassing": f"{armed}/{counts['pass']}",
        "openCases": open_ids,
        "unevidencedPasses": unevidenced,
        "orphanCases": orphans,
        "blockers": blockers,
        "advisories": blockers_advisory,
        "clear": not blockers,
    }


def cmd_check(args) -> int:
    d = Path(args.dir).resolve()
    supplied = [args.control_exception_validator, args.control_exception_validator_sha256,
                args.control_exception_manifest, args.control_exception_manifest_sha256]
    trust = None
    if any(supplied):
        if not all(supplied):
            print("all four control-exception trust-anchor arguments are required together", file=sys.stderr)
            return 2
        trust = {"validator": args.control_exception_validator,
                 "validatorSha256": args.control_exception_validator_sha256,
                 "manifest": args.control_exception_manifest,
                 "manifestSha256": args.control_exception_manifest_sha256}
    a = audit(d, trust)
    if args.json:
        print(json.dumps(a, indent=2))
        return 0 if a["clear"] else 1

    c = a["counts"]
    o = a["observations"]
    print(f"{a['project']} · lanes: {', '.join(a['lanes']) or 'none declared'}")
    print(f"Requirements: {a['requirements']} inventoried, {len(a['requirementsUntested'])} with no case")
    print(f"Surfaces:   {a['surfaces']} enumerated, {len(a['surfacesUncovered'])} with no case")
    if a["effectRequirements"] or a["requirementsVacuous"]:
        print(f"External effects: examined={a['effectRequirements']} "
              f"witnessed={a['effectRequirementsWitnessed']} "
              f"vacuous={len(a['requirementsVacuous'])} "
              f"unwitnessed={len(a['effectRequirementsUnwitnessed'])} — armed proves the "
              f"suite bites, and only a witness proves the product acted.")
        if a["requirementsVacuous"]:
            print(f"  Vacuous (the capability the claim constrains never runs): "
                  f"{', '.join(a['requirementsVacuous'])}")
        if a["effectRequirementsUnwitnessed"]:
            print(f"  Effect claimed, no witness: "
                  f"{', '.join(a['effectRequirementsUnwitnessed'])}")
    print(f"Cases:      {c['pass']} pass · {c['fail']} fail · {c['skip']} skip · "
          f"{c['n/a']} n/a · {c['unselected']} carried · {c['inconclusive']} inconclusive · "
          f"{c['unoracled']} unoracled · {c['blocked']} blocked · {c['open']} open  "
          f"(of {a['cases']})")
    print(f"Observed:   {o['coverage']} cases produced a measurement · "
          f"{o['unavailable']} could not be measured · {o['deferred']} not attempted")
    for lane, proof in sorted(a["laneProof"].items()):
        if proof.get("attached"):
            print(f"On glass:   {lane} → {proof.get('artifact', '?')} "
                  f"({proof.get('attachedBy', 'no witness recorded')})")
        else:
            print(f"On glass:   {lane} → NOT attached: {proof.get('reason', '?')}")
    mix = a["oracleMix"]
    product = {k: v for k, v in mix.items() if v and k not in SOURCE_RUNGS}
    offaxis = {k: v for k, v in mix.items() if v and k in SOURCE_RUNGS}
    print("Oracles:    " + " · ".join(f"{k} {v}" for k, v in product.items()))
    if offaxis:
        # Apart rather than folded in: these read source text and run nothing,
        # so a campaign must not be able to look product-adequate on them.
        print("Off-ladder: " + " · ".join(f"{k} {v}" for k, v in offaxis.items())
              + " — reads source, runs nothing, buys no effect credit")
    print(f"Armed:      {a['armedOfPassing']} passing cases have been watched to fail")
    # Per lane as well as in total, because a campaign-wide mix hides a lane that
    # was only ever checked on paper. The `effect` column is the one to read: a
    # lane at 0 there is proved to render and not to work.
    for lane, row in sorted(a["laneLedger"].items()):
        print(f"Lane:       {lane} — {row['cases']} case(s) · {row['pass']} pass · "
              f"{row['effect']} at an effect rung · {row['armed']} armed · "
              + " ".join(f"{k}:{v}" for k, v in sorted(row["rungs"].items())))
    pc = a["planeCounts"]
    if any(pc.values()) or a["unreachedPlanes"]:
        print("Planes:     " + " · ".join(f"{k} {v}" for k, v in pc.items() if v)
              + (f" · {len(a['casesUnplaned'])} passing case(s) name no plane"
                 if a["casesUnplaned"] else ""))
    else:
        print("Planes:     NOT DECLARED — no case says what it was checked against, so a "
              "green suite over in-process doubles is indistinguishable from one over the "
              "running product.")
    if a["journeys"]:
        print(f"Journeys:   {a['journeys']} declared, {a['journeysCritical']} critical · "
              f"boundaries {a['boundariesCut']}/{a['boundariesTotal']} cut")
    else:
        print("Journeys:   NOT DECLARED — no multi-step task is modelled, so nothing here "
              "counts one. A journey is a history, and no per-surface count can see it.")
    if a["surfacesDeclaringControls"]:
        print(f"Controls:   {a['controlsActuated']} of {a['controlsDeclared']} declared "
              f"control(s) actuated by a passing effect-rung case, across "
              f"{a['surfacesDeclaringControls']} surface(s) that declare any")
    else:
        print("Controls:   NOT DECLARED — no surface lists its controls, so nothing here "
              "counts them. A control renders and accepts a click whether or not its "
              "handler does anything.")
    if a["navigationShells"]:
        print(f"Shells:     {len(a['navigationShells'])} navigation shell(s), "
              f"{sum(len(v) for v in a['navigationShells'].values())} destination(s)")
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

    if a.get("advisories"):
        # Printed before the verdict on a clear run as well as a red one. The
        # campaign this rule came from was green, and the thing worth knowing was
        # only visible in a number nobody printed.
        print("\nWorth reading, not blocking:")
        for line in a["advisories"]:
            print(f"  · {line}")

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
        print(f"\n  Requirements nothing checks: "
              f"{capped(a['requirementsUntested'], 12)}")
        print("  Each is something the project says it does. Write the case, or mark the "
              "requirement `deferred` with its citation.")
    if a["effectRequirementsUnbacked"]:
        print(f"\n  External-effect claims with no witness "
              f"({a['effectRequirementsWitnessed']} of {a['effectRequirements']} witnessed):")
        for line in a["effectRequirementsUnbacked"][:12]:
            print(f"    · {line}")
        print(capped_tail(a["effectRequirementsUnbacked"], 12))
        print("  Drive the effect from a production entry point with a recorder attached and")
        print("  record it:")
        print("    campaign.py set <dir> --case CASE-0001 --status pass --oracle effect-witness \\")
        print("      --recorder 'strace -f -e trace=network' --effect-class outbound-socket \\")
        print("      --effect-count 3")
        print("  Where the product does not perform the effect at all, the requirement is")
        print("  `vacuous`, not `observed` — a guarantee that holds because nothing does the")
        print("  thing is a finding, and recording it clears this blocker honestly.")
    if a["hollowWitnesses"]:
        print(f"\n  Effect witnesses that witnessed nothing: "
              f"{capped([w.split()[0] for w in a['hollowWitnesses']], 12)}")
        for line in a["hollowWitnesses"][:6]:
            print(f"    · {line}")
        print(capped_tail(a["hollowWitnesses"], 6))
    if a.get("hollowSourceClaims"):
        print(f"\n  Source-analysis claims with no analyzer or no denominator: "
              f"{capped(a['hollowSourceClaims'], 12)}")
    if a.get("requirementsSourceOnly"):
        print(f"\n  Requirements resting on source analysis alone: "
              f"{capped(a['requirementsSourceOnly'], 12)}")
        print("  Source analysis reads text and runs nothing. Add a case on the "
              "product ladder, or record the requirement's effect honestly.")
    if a["surfacesUncovered"]:
        print(f"  Surfaces with no case: {capped(a['surfacesUncovered'], 12)}")
    if a["flowsPresenceOnly"]:
        print(f"\n  Critical flows proved only by presence: "
              f"{capped(a['flowsPresenceOnly'], 12)}")
        print("  Each promises an effect. Add a case whose oracle is outcome, metamorphic "
              "or visual, or drop the flow's `critical` flag and say why.")
    if a["unevidencedPasses"]:
        print(f"  Passes with no artifact: {capped(a['unevidencedPasses'], 12)}")
        print("  A pass you reached by looking is not a measurement. Attach the artifact "
              "or reopen the case.")
    if a["glassLanesUnproved"]:
        for lane, ids in sorted(a["glassLanesUnproved"].items()):
            print(f"\n  Lane '{lane}' claims on-glass verification and has no proof "
                  f"({len(ids)} case(s): {capped(ids, 4)}).")
        print("  Build the artifact if it is not on disk, launch it, then record:")
        print("    campaign.py lane <dir> --lane <lane> --artifact <path> \\")
        print("      --built-by '<build command>' --attached '<what witnessed it>'")
        print("  --cannot-attach is for a structural block after that build "
              "(no interactive desktop, no signing identity), not a missing binary.")
    if a["badRasterClaims"]:
        print("\n  Pixel claims with no usable pixels:")
        for line in a["badRasterClaims"][:10]:
            print(f"    · {line}")
        print(capped_tail(a["badRasterClaims"], 10))
    if a.get("publishedShots"):
        print(f"Wall:       {a['publishedShots']} published shot(s) · "
              f"{a['distinctPublishedImages']} distinct image(s)")
    if a.get("duplicateShots"):
        print("   published shots showing the same picture under different subjects:")
        for ids in list(a["duplicateShots"].values())[:6]:
            print(f"      {', '.join(ids)}")
        print(capped_tail(a["duplicateShots"], 6, indent="      "))
    if a.get("declaredShares"):
        # Counted apart rather than folded into the wall's distinct-image number: a
        # declared share is admissible, and a reader still needs to see that these
        # cells repeat on purpose.
        print(f"   declared shares ({len(a['declaredShares'])} image(s) carrying a reason "
              f"in captures.json):")
        for ids in list(a["declaredShares"].values())[:8]:
            print(f"      {', '.join(ids)}")
        print(capped_tail(a["declaredShares"], 8, indent="      "))
    if a["duplicateArtifacts"]:
        print("\n  The same capture standing in for several cases:")
        for ids in list(a["duplicateArtifacts"].values())[:6]:
            print(f"    · {', '.join(ids)}")
        print(capped_tail(a["duplicateArtifacts"], 6))
    if a["unwitnessedPixelClaims"]:
        print("\n  Pixels with no stated origin:")
        for line in a["unwitnessedPixelClaims"][:10]:
            print(f"    · {line}")
        print(capped_tail(a["unwitnessedPixelClaims"], 10))
    if a["legacyRungCases"]:
        print(f"\n  On the legacy `visual` rung: {capped(a['legacyRungCases'], 12)}")
        print("  Asserting that a card's title property equals a string is a data-model "
              "check, not a visual one. Split each into structural-visual or "
              "raster-visual; the second needs a capture off a display server.")
    if a["openCases"]:
        print(f"  Open: {capped(a['openCases'], 20)}")
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
                f"{'yes' if c.get('armed') is True else ''} | {len(c.get('evidence', []))} |")

    text = "\n".join(lines) + "\n"
    paths(d)["ledger"].write_text(text)
    print(text)
    print(f"Written to {paths(d)['ledger']}")
    return 0


def cmd_export_warrant(args) -> int:
    """Write the campaign's measurements where the `warrant` plugin reads them.

    The two plugins measure the same repository and neither can see the other's
    state, so a mature campaign and a tier-0 warrant coexist indefinitely:
    `charter_validate.py` treats an absent evidence file as an unmet condition
    by design, which makes "never measured" and "measured badly" identical to
    it. This writes the two files it names, from numbers the campaign already
    holds.

    `suite-health.json` carries the armed ratio, because an unarmed pass is not
    known to bite and the assay plane exists to put a number on exactly that.
    `oracle-coverage.json` is keyed by surface rather than by defect class:
    warrant's own `rollup_classes.py` maps surfaces onto classes using the
    warrant's globs, and duplicating that mapping here would put the same
    decision in two places.

    Nothing is inferred. A campaign that measured little exports little, and
    the warrant refuses the tier — which is the correct outcome and the reason
    this is an export rather than an attestation.
    """
    d = Path(args.dir).resolve()
    root = Path(args.root).resolve()
    a = audit(d)
    cases = load(d, "cases", [])
    counts = a["counts"]

    armed = a.get("armed", 0)
    passing = counts["pass"]
    effect = sum(1 for c in cases
                 if c.get("status") == "pass" and c.get("oracle") in EFFECT_RUNGS)

    # `green` is deliberately NOT written here. In warrant, that flag means the
    # mutation score is holding at or above its high-water mark, and this plugin
    # does not do mutation testing — `rollup_classes.py` recomputes it from a
    # `mutation` block and would overwrite anything written here anyway. Claiming
    # it from the campaign's own gate would assert a fault-sensitivity measurement
    # nobody made, which is the exact conflation this export exists to end.
    #
    # What the campaign does measure is the armed ratio: passes that have been
    # watched to fail. That is real evidence about whether the suite bites, and it
    # is recorded under its own name so a reader can see which measurement they
    # have and which they still owe.
    suite = {
        "source": "test-campaign",
        "campaign_dir": str(d),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "campaign_gate_clear": bool(a["clear"]),
        "cases": len(cases),
        "passing": passing,
        "armed": armed,
        "armed_ratio": (round(armed / passing, 4) if passing else None),
        "effect_rung_passes": effect,
        "unoracled": counts.get("unoracled", 0),
        "inconclusive": counts["inconclusive"],
        "blocked": counts["blocked"],
        "mutation_measured": False,
        "note": ("armed_ratio is passes watched to fail over passes; an unarmed pass "
                 "is not known to bite. `green` is not set here: in warrant it means "
                 "the mutation score is holding, and this plugin does not measure "
                 "mutation survival. Run warrant:assay for that number."),
    }

    # Per surface: how many of its cases stand on a rung that asserts an effect.
    # That is the campaign's analogue of lineage coverage — the share of a
    # surface's checks that could actually catch a wrong answer.
    #
    # The shape is warrant's, not the campaign's: `rollup_classes.py` reads a
    # LIST of rows and matches `file` against the warrant's class globs. Keying
    # this by surface id instead would match no glob and roll up to zero
    # coverage on every class, which reads identically to a campaign that
    # measured nothing.
    # `file` must hold a FILESYSTEM path, because that is what the warrant's class
    # globs match — `**/*.spec.ts`, `**/page.tsx`, `**/captures/**`. Falling back to
    # a route put `/admin/[pane]` in a field named `file`, which matches no glob and
    # rolls every class up to zero. That reads identically to a campaign that
    # measured nothing, so five of seven classes sat at tier 0 permanently while 132
    # surfaces and 203 figures were sitting right there. Measured on dAIolog,
    # 2026-08-25; three out-of-family lanes independently said the export is the side
    # that changes, because the warrant is signed and reinterpreting a signed glob in
    # the reader would be a silent grant of scope.
    #
    # A surface with no declaring file OMITS `file` rather than inventing one. A
    # route group, a drawer or a not-found page genuinely has none, and inventing a
    # path would make "unmatched" and "unmeasured" indistinguishable again — the very
    # confusion this fixes. `route` always travels, so nothing is lost.
    inventory = load(d, "inventory", {})
    meta_of = {}
    for s in inventory.get("surface", []):
        if not s.get("id"):
            continue
        # Only a value that looks like a path in this tree counts as one.
        path = s.get("path") or s.get("file") or s.get("source") or s.get("component")
        path = str(path) if path and not str(path).startswith("/") else None
        meta_of[s["id"]] = {"path": path,
                            "route": str(s.get("route") or s.get("name") or s["id"])}

    tally: dict[str, dict] = {}
    for c in cases:
        sid = c.get("surface") or c.get("surfaceId")
        if not sid:
            continue
        meta = meta_of.get(str(sid), {"path": None, "route": str(sid)})
        key = meta["path"] or meta["route"]
        block = tally.setdefault(key, {"figures": 0, "sourced": 0,
                                       "path": meta["path"], "route": meta["route"]})
        block["figures"] += 1
        if c.get("oracle") in EFFECT_RUNGS:
            block["sourced"] += 1
    surfaces = []
    for key, block in sorted(tally.items()):
        row = {"route": block["route"],
               "figures": block["figures"],
               "sourced": block["sourced"],
               "unsourced": block["figures"] - block["sourced"]}
        if block["path"]:
            row["file"] = block["path"]
        surfaces.append(row)
    unmapped = sum(1 for r in surfaces if "file" not in r)
    coverage = {
        "source": "test-campaign",
        "campaign_dir": str(d),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "surfaces": surfaces,
        "unmapped_surfaces": unmapped,
        "note": ("`figures` is cases on that surface and `sourced` is those on an "
                 "effect rung — a check that could catch a wrong answer. `file` is a "
                 "filesystem path and is ABSENT where the surface has no declaring "
                 "file; the warrant's class globs match `file`, so a surface without "
                 "one is genuinely unmatched rather than quietly miscounted. `route` "
                 "always travels. Run warrant's rollup_classes.py to key this by "
                 "defect class using the warrant's own globs."),
    }

    out = root / ".warrant"
    out.mkdir(parents=True, exist_ok=True)

    # warrant:assay writes a `mutation` block into suite-health.json, and this export
    # rewrites that file wholesale. Without carrying the block forward, every campaign
    # export silently deletes the mutation mark the assay plane earned — and the mark
    # is what the ratchet compares against, so losing it reads as "never measured"
    # rather than as a deletion. Measured on dAIolog 2026-08-25, where a corrected
    # mark vanished on the next export. This file has two writers; neither owns all
    # of it.
    prior = {}
    health_path = out / "suite-health.json"
    if health_path.exists():
        try:
            prior = json.loads(health_path.read_text())
        except (OSError, ValueError):
            prior = {}
    for key in ("mutation",):
        if key in prior and key not in suite:
            suite[key] = prior[key]

    # `mutation_measured` above is this plugin's own answer: the campaign never
    # runs a mutation pass, so it writes False. But the file it writes is shared
    # with warrant:assay, and once that plane has left a mark here the flag is a
    # statement about the FILE rather than about this writer. Leaving it False
    # made `lot_plan.py` print "mutation survival not measured" over a suite-health
    # holding a real score — measured on dAIolog 2026-08-25, where 12.5% over 168
    # production mutants sat two keys away from a line denying it existed.
    mark = suite.get("mutation")
    if isinstance(mark, dict) and mark.get("score") is not None:
        suite["mutation_measured"] = True
        suite["mutation_measured_by"] = "warrant:assay"

    written = []
    for name, payload in (("suite-health.json", suite),
                          ("oracle-coverage.json", coverage)):
        path = out / name
        path.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n")
        written.append(str(path))

    if args.json:
        print(json.dumps({"written": written, "suite": suite,
                          "surfaces": len(surfaces)}, indent=2))
        return 0

    print(f"exported to {out}")
    print(f"  suite-health.json      armed={armed} of {passing} passing  "
          f"effect-rung passes={effect}  campaign gate "
          f"{'clear' if suite['campaign_gate_clear'] else 'HOLDING'}")
    if suite.get("mutation_measured"):
        m = suite["mutation"]
        print(f"                         mutation survival {m['score']:.1%} "
              f"({m.get('killed')} of {m.get('run')}) — carried from warrant:assay, "
              f"not measured by this export")
    else:
        print("                         mutation survival NOT measured here — warrant:assay "
              "still owes that number, and tier 2 needs it")
    if suite["unoracled"]:
        print(f"                         {suite['unoracled']} case(s) unoracled — a "
              f"warrant tier over these would rest on nothing")
    print(f"  oracle-coverage.json   {len(surfaces)} surface(s), keyed by surface")
    if unmapped:
        print(f"                         {unmapped} of them carry NO `file` — the warrant's class "
              f"globs cannot match those, and")
        print(f"                         that is honest rather than hidden. Give a surface a `path` "
              f"in inventory.json to map it.")
    print("  next: warrant's rollup_classes.py, then warrant:ratchet")
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
    s.add_argument("--recorder",
                   help="What observed the effect, e.g. \"strace -f -e trace=network\" "
                        "or 'loopback listener logging accepts'. Required for an "
                        "effect-witness pass.")
    s.add_argument("--effect-class",
                   help=f"Which effect was recorded. One of: {', '.join(EFFECT_CLASSES)}.")
    s.add_argument("--effect-count", type=int,
                   help="How many events of that class the recorder saw. Zero is a "
                        "reading, and it is not a pass.")
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
                                            "reached after the artifact was built (no "
                                            "interactive desktop, no signing identity, "
                                            "Session 0). A missing-binary reason is "
                                            "refused — build the artifact, then attach.")
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
    c.add_argument("--control-exception-validator")
    c.add_argument("--control-exception-validator-sha256")
    c.add_argument("--control-exception-manifest")
    c.add_argument("--control-exception-manifest-sha256")
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser("report")
    r.add_argument("dir")
    r.add_argument("--json", action="store_true")
    r.set_defaults(fn=cmd_report)

    ew = sub.add_parser("export-warrant",
                        help="Write suite-health.json and oracle-coverage.json where "
                             "the warrant plugin reads them, so a campaign can earn a "
                             "tier instead of the warrant refusing one forever.")
    ew.add_argument("dir")
    ew.add_argument("--root", required=True,
                    help="The repository holding .warrant/ — the files are written there.")
    ew.add_argument("--json", action="store_true")
    ew.set_defaults(fn=cmd_export_warrant)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
