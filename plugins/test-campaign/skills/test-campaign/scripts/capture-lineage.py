#!/usr/bin/env python3
"""Prove every published picture depicts what it is filed under.

WHY THIS EXISTS
---------------
A campaign published 20 surface captures and cleared every gate it had: every
case accounted for, 46 of 49 checked, every `-glass` lane proved and witnessed.
The captures were of three unrelated documents. Twenty files held SIX distinct
images, four groups of four byte-identical. A flow step captioned "Open pairing
QR code sheet" showed a questionnaire about Apple developer credentials.

Nothing was broken. `attach-shots.py` binds an image to a surface on a slug of
its FILENAME, which is string identity and not evidence; `evidence-page.py`
renders the picture with an `alt` taken from the label, so a wrong image arrives
under a right-sounding caption; and `campaign.py check` inspected artifacts only
for `RASTER_RUNGS` cases, never for the `shot` field the page actually renders.
The gated part of the campaign was sound and the ungated part was the part
people look at.

This is `warrant:oracle`'s lineage plane with *picture* substituted for *figure*.
There, a displayed number without a `data-source-ref` is the defect the plane
exists to find. Here, a published capture without a recorded target is.

FOUR PASSES, ALL EXACT, NONE NEEDING A MODEL
--------------------------------------------
  1 unsourced  an image with no manifest entry, or an entry with no target
  2 untied     the target does not resolve to the subject's declared route
  3 shared     two subjects, one sha256, undeclared — or declared with nothing
              outside the declaration agreeing with it
  4 unaccounted an image in the shots directory no subject publishes, and no
              entry declares deliberately unpublished with a reason
  5 unjudged   published with no be-my-witness verdict — ratchets, does not block

A judgement inserted anywhere on this ladder would be the thing the ladder exists
to make unnecessary. Vision tops out near 40% recall on fine-grained UI diffs; a
model is the explanation layer, never the gate. `references/capture-lineage.md`.

    python3 capture-lineage.py <campaign-dir>
    python3 capture-lineage.py <campaign-dir> --gate            # exit 2 on any hard failure
    python3 capture-lineage.py <campaign-dir> --set-ratchet [--reason "..."]
    python3 capture-lineage.py <campaign-dir> --seed-swap SURF-001,SURF-002
    python3 capture-lineage.py <campaign-dir> --json
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif"}
RATCHET_FILE = "capture-ratchet.json"
MANIFEST = "evidence/shots/captures.json"
VERDICTS = "witness-verdicts.json"

# A route that names a source file cannot be photographed by a browser. This is
# not a pedantic check: it is the mechanical reason a real capture step got
# improvised into screenshotting whatever HTML was to hand.
SOURCE_SUFFIXES = {".swift", ".kt", ".java", ".tsx", ".jsx", ".ts", ".js",
                   ".vue", ".svelte", ".dart", ".cs", ".xaml", ".py", ".rb"}

# Channels that record no target by construction. Admissible, counted apart,
# never silently folded into the judged population.
MANUAL_CHANNELS = {"manual", "hand-delivered", "photograph"}


def sha256_of(p: Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def norm_target(t: str) -> str:
    """Reduce a target to the part a harness may not legitimately vary.

    Scheme, host, port, query and fragment are noise — a dev server on :3130 and
    the same route on :3000 are the same surface. Path, bundle id and window
    title are the signal, so they survive.
    """
    if not t:
        return ""
    s = str(t).strip()
    s = re.sub(r"^[a-z][a-z0-9+.-]*://", "", s, flags=re.I)   # scheme
    s = s.split("?")[0].split("#")[0]                          # query, fragment
    if "/" in s:
        head, _, tail = s.partition("/")
        if ":" in head or "." in head or head in ("localhost",):
            s = "/" + tail                                     # host[:port] dropped
    s = re.sub(r"/+", "/", s)
    return s.rstrip("/").lower() or "/"


def route_of(rec: dict) -> str:
    for k in ("route", "path", "url", "bundle", "window"):
        if rec.get(k):
            return str(rec[k])
    return ""


def tie(target: str, route: str) -> tuple[bool, str]:
    """Does this capture's target resolve to the subject's declared route?"""
    if not route:
        return True, "subject declares no route — nothing to tie against"
    nt, nr = norm_target(target), norm_target(route)
    if Path(nr).suffix in SOURCE_SUFFIXES:
        return False, (f"subject's route is a source file ({route}) — no capture channel "
                       f"can photograph one. This lane needs the on-glass channel "
                       f"(a bundle path plus an attach witness), not a browser route")
    if nt == nr or nt.endswith(nr) or nr.endswith(nt):
        return True, ""
    return False, f"target {target!r} does not resolve to route {route!r}"


def subjects_of(inventory: dict) -> dict[str, dict]:
    """Every id a capture may legitimately claim, with the route it must tie to."""
    out: dict[str, dict] = {}
    for s in inventory.get("surface", []):
        if s.get("id"):
            out[s["id"]] = {"kind": "surface", "route": route_of(s),
                            "shot": s.get("shot"), "name": s.get("name") or s.get("label", "")}
    for f in inventory.get("flow", []):
        for step in f.get("steps", []):
            sid = step.get("id")
            if not sid:
                continue
            # A step inherits its surface's route: a step is a state of a
            # surface, not a separate address.
            surf = out.get(step.get("surface", ""), {})
            out[sid] = {"kind": "step", "route": step.get("route") or surf.get("route", ""),
                        "shot": step.get("shot"), "name": step.get("label", "")}
    return out


def share_admissible(sids: list[str], entry_of: dict[str, dict],
                     subjects: dict[str, dict]) -> tuple[bool, str]:
    """May these subjects publish one image?

    Until 0.9.5 the answer was "if each names the others in `sharesWith`" — a
    declaration written into the very registry this script checks, so a capture
    authorised its own duplicate. `sharesReason` was demanded by the blocker's
    own remedy text and read by no code at all, so the reason was required by
    documentation and enforced nowhere; `campaign.py` has required it since
    0.9.3 and the two gates disagreed about the same declaration.

    So: every member names the others, every member records a reason, and
    something OUTSIDE the declaration agrees that these subjects are one
    address. That corroboration comes from the subject records in
    inventory.json and from the target the capture channel recorded at capture
    time — both already read by the tie pass, neither a new source of truth.
    """
    for s in sids:
        e = entry_of.get(s) or {}
        missing = set(sids) - {s} - set(e.get("sharesWith") or [])
        if missing:
            return False, (f"{s} does not name {', '.join(sorted(missing))} in its `sharesWith`"
                           f" — declaring one side of a share is not a declaration")
        if not str(e.get("sharesReason") or "").strip():
            return False, (f"{s} declares a share and records no `sharesReason` — a share "
                           f"with no recorded reason is a duplicate with a label on it")

    # The corroboration, in the order of how close the witness stood to the
    # shutter. A target is what the channel was pointed at, written at capture
    # time; a route is what the subject registry says the subject is. The tie
    # pass already binds each target to its own subject's route, so agreeing
    # targets are the claim "one address served all of them" made by something
    # other than the declaration under test.
    targets = {norm_target(str((entry_of.get(s) or {}).get("target", ""))) for s in sids} - {""}
    routes = {norm_target(str((subjects.get(s) or {}).get("route", ""))) for s in sids} - {""}
    if targets:
        if len(targets) > 1:
            return False, (f"the declaration says one picture depicts all of them, and the "
                           f"capture channel recorded {len(targets)} different targets "
                           f"({', '.join(sorted(targets))})")
        return True, ""
    if routes:
        if len(routes) > 1:
            return False, (f"no member's capture recorded a target, and their inventory records "
                           f"name {len(routes)} different addresses "
                           f"({', '.join(sorted(routes))})")
        return True, ""
    return False, ("nothing outside the declaration corroborates it — no member's capture "
                   "recorded a target and no member declares a route, so the only evidence "
                   "for the share is the share")


def analyse(d: Path) -> dict:
    inv_path = d / "inventory.json"
    if not inv_path.exists():
        return {"fatal": f"no inventory at {inv_path}"}
    inventory = json.loads(inv_path.read_text())
    subjects = subjects_of(inventory)

    man_path = d / MANIFEST
    manifest = json.loads(man_path.read_text()) if man_path.exists() else []
    by_path = {str(e.get("path", "")): e for e in manifest}

    shots_dir = d / "evidence/shots"
    images = sorted(
        str(p.relative_to(d)) for p in shots_dir.rglob("*")
        if p.suffix.lower() in IMAGE_SUFFIXES
        and "mock" not in {q.lower() for q in p.relative_to(shots_dir).parts[:-1]}
    ) if shots_dir.exists() else []

    # Only what the evidence page actually renders is in scope. An image sitting
    # in the directory unpublished is a capture nobody is relying on.
    published = {sid: rec["shot"] for sid, rec in subjects.items() if rec.get("shot")}

    unsourced, untied, manual, reconstructed = [], [], [], []
    by_hash: dict[str, list[str]] = {}

    for sid, shot in sorted(published.items()):
        rec = subjects[sid]
        entry = by_path.get(shot) or {}
        if shot not in by_path:
            unsourced.append(f"{sid} → {shot}: no entry in {MANIFEST}. The capture step "
                             f"recorded nothing, so the only thing binding this picture to "
                             f"{sid} is its filename.")
        elif str(entry.get("channel", "")).lower() in MANUAL_CHANNELS:
            manual.append(f"{sid} → {shot}: channel {entry.get('channel')!r} records no target")
        elif not entry.get("target"):
            unsourced.append(f"{sid} → {shot}: entry names no target")
        elif entry.get("subject") and entry["subject"] != sid:
            untied.append(f"{sid} → {shot}: manifest says this capture depicts "
                          f"{entry['subject']!r}, but it is published as {sid}")
        else:
            ok, why = tie(entry["target"], rec.get("route", ""))
            if not ok:
                untied.append(f"{sid} → {shot}: {why}")

        p = d / shot
        if not p.exists():
            unsourced.append(f"{sid} → {shot}: no file at that path")
            continue
        h = sha256_of(p)
        if h:
            by_hash.setdefault(h, []).append(sid)
        if entry.get("sha256") and h and entry["sha256"] != h:
            reconstructed.append(f"{sid} → {shot}: manifest sha256 disagrees with the bytes "
                                 f"on disk. A manifest written after the fact records what "
                                 f"somebody believed, not what the channel did.")

    entry_of = {sid: (by_path.get(published[sid]) or {}) for sid in published}
    shared = []
    for h, sids in sorted(by_hash.items()):
        if len(sids) < 2:
            continue
        ok, why = share_admissible(sids, entry_of, subjects)
        if ok:
            manual.append(f"declared share: {', '.join(sids)} → one capture, {h[:12]}")
            continue
        shared.append(f"{len(sids)} subjects share one image ({h[:12]}): "
                      f"{', '.join(sids)} — {why}")

    # DEF-117. Everything the gate had was derived from PUBLISHED captures, so an
    # image nobody publishes contributed to no finding: measured on a real
    # campaign as `published captures: 0 · files in shots dir: 11`, exit 0, and
    # the sentence "Every published capture names a target that ties to its
    # subject" — true, and covering nothing. A capture on disk is either shown,
    # or declared unpublished with a reason, or a loose end.
    published_paths = set(published.values())
    unaccounted = []
    for rel in images:
        if rel in published_paths:
            continue
        entry = by_path.get(rel) or {}
        reason = str(entry.get("unpublishedReason") or "").strip()
        if reason:
            manual.append(f"declared unpublished: {rel} — {reason}")
        elif rel in by_path:
            unaccounted.append(f"{rel}: the manifest names it and no subject publishes it, and "
                               f"it records no `unpublishedReason`")
        else:
            unaccounted.append(f"{rel}: no subject publishes it and no manifest entry names it")

    ver_path = d / VERDICTS
    verdicts = json.loads(ver_path.read_text()) if ver_path.exists() else []
    judged_ids = {v.get("subject") for v in verdicts if v.get("verdict")}
    refuted = [v for v in verdicts if str(v.get("verdict", "")).lower()
               in ("fail", "invalid-capture", "not-evidence", "mismatch")]
    judgeable = [s for s in published if s not in {m.split(" ")[0] for m in manual}]
    judged = [s for s in judgeable if s in judged_ids]

    return {
        "published": len(published), "images": len(images),
        "unsourced": unsourced, "untied": untied, "shared": shared,
        "unaccounted": unaccounted,
        "reconstructed": reconstructed, "manual": manual,
        "judged": len(judged), "judgeable": len(judgeable),
        "refuted": [f"{v.get('subject')}: {v.get('verdict')} — {v.get('reason', 'no reason recorded')}"
                    for v in refuted],
        "distinctImages": len(by_hash),
    }


def seed_swap(d: Path, a: str, b: str) -> int:
    """Watch the tie pass fail. An assertion nobody has seen go red is
    indistinguishable from one that cannot go red — the campaign's own rule,
    applied to the gate rather than to the suite."""
    inv = json.loads((d / "inventory.json").read_text())
    subjects = subjects_of(inv)
    if a not in subjects or b not in subjects:
        print(f"seed-swap: {a} or {b} is not a subject in this campaign")
        return 2
    man_path = d / MANIFEST
    if not man_path.exists():
        print(f"seed-swap: no manifest at {man_path} — the tie pass has nothing to read, "
              f"so it cannot be watched to fail. That is pass 1's finding, not this one.")
        return 2
    manifest = json.loads(man_path.read_text())
    ra, rb = subjects[a].get("shot"), subjects[b].get("shot")
    swapped = copy.deepcopy(manifest)
    for e in swapped:
        if e.get("path") == ra:
            e["path"] = rb
        elif e.get("path") == rb:
            e["path"] = ra
    backup = manifest
    try:
        man_path.write_text(json.dumps(swapped, indent=1) + "\n")
        a2 = analyse(d)
        hard = len(a2["unsourced"]) + len(a2["untied"]) + len(a2["shared"])
    finally:
        man_path.write_text(json.dumps(backup, indent=1) + "\n")
    if hard:
        print(f"seed-swap CAUGHT — swapping {a} and {b} produced {hard} hard failure(s). "
              f"The tie pass reads what it claims to read.")
        return 0
    print(f"seed-swap FALSE PASS — swapping {a} and {b} changed nothing. The tie pass is "
          f"not reading the manifest, and every verdict it has ever issued is worthless. "
          f"This is the exact state the campaign was in before capture lineage existed.")
    return 2


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    d = Path(args[0])

    if "--seed-swap" in args:
        pair = args[args.index("--seed-swap") + 1].split(",")
        if len(pair) != 2:
            print("--seed-swap takes two ids: --seed-swap SURF-001,SURF-002")
            return 2
        return seed_swap(d, pair[0].strip(), pair[1].strip())

    a = analyse(d)
    if a.get("fatal"):
        print(a["fatal"])
        return 2
    if "--json" in args:
        print(json.dumps(a, indent=1))
        return 0

    hard = len(a["unsourced"]) + len(a["untied"]) + len(a["shared"]) + len(a["unaccounted"])
    print(f"published captures: {a['published']}  ·  distinct images: {a['distinctImages']}  "
          f"·  files in shots dir: {a['images']}")
    if a["published"] and a["distinctImages"] < a["published"]:
        print(f"   {a['published'] - a['distinctImages']} published cell(s) show a picture "
              f"another cell also shows")

    for label, rows, why in (
        ("UNSOURCED — nothing but the filename binds this picture to its subject", a["unsourced"],
         "Write the manifest at capture time. It cannot be recovered afterwards."),
        ("UNTIED — the recorded target is not the subject's route", a["untied"],
         "Either the capture was pointed at the wrong thing, or the lane needs a "
         "different channel."),
        ("SHARED — one capture published under several subjects", a["shared"],
         "Declare it in captures.json with `sharesWith` naming every other member and a "
         "`sharesReason`, on every member — and only where the subjects are one address, "
         "since that is the one thing outside the declaration that can agree with it. "
         "Otherwise capture each subject."),
        ("UNACCOUNTED — an image in the shots directory that nothing shows or explains",
         a["unaccounted"],
         "Publish it, delete it, or record `unpublishedReason` on its captures.json entry. "
         "Every finding this gate makes is derived from published captures, so a file nobody "
         "publishes is a capture the gate cannot see: one campaign read `published captures: 0 "
         "· files in shots dir: 11` and exited 0."),
        ("RECONSTRUCTED — the manifest disagrees with the bytes", a["reconstructed"],
         "A manifest written after the fact is not provenance."),
        ("REFUTED BY THE WITNESS", a["refuted"],
         "be-my-witness judged these against their reference and rejected them."),
    ):
        if rows:
            print(f"\n{label}:")
            for r in rows[:20]:
                print(f"   {r}")
            if len(rows) > 20:
                print(f"   … and {len(rows) - 20} more")
            print(f"   → {why}")

    if a["manual"]:
        print(f"\nCOUNTED APART ({len(a['manual'])}) — admissible, not judged:")
        for m in a["manual"][:10]:
            print(f"   {m}")

    jn, jd = a["judged"], a["judgeable"]
    print(f"\nJUDGED {jn} of {jd} judgeable capture(s)"
          + (f" ({100 * jn / jd:.0f}%)" if jd else ""))
    if jn < jd:
        print("   An unjudged capture is an uncompared one. It is not a pass.")

    ratchet_path = d / RATCHET_FILE
    prior = json.loads(ratchet_path.read_text()) if ratchet_path.exists() else None

    if "--set-ratchet" in args:
        reason = ""
        if "--reason" in args:
            i = args.index("--reason")
            reason = args[i + 1] if i + 1 < len(args) else ""
        # A ratchet of 0 is `strict-check.py`'s empty campaign wearing a floor's
        # clothes: it can never fall, so it can never fail, and pinning it records
        # that the gate is armed when nothing has ever passed under it.
        if jn == 0:
            print(f"\nREFUSED — a ratchet of 0 pins nothing. {jd} judgeable capture(s) and none "
                  f"judged means this gate has never had anything to check, and a bar that "
                  f"cannot fall is not a bar. Judge a capture with be-my-witness first "
                  f"(witness-worklist.py builds the pairs), then pin what it earned.")
            return 1
        if prior and jn < prior["judged"] and not reason:
            print(f"\nREFUSED — that would lower the ratchet from {prior['judged']} to {jn} "
                  f"with no reason recorded. Pass --reason \"...\" so the next reader sees "
                  f"why the bar moved.")
            return 1
        rec = {"judged": jn, "judgeable": jd,
               "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        if reason:
            rec["loweredBecause" if prior and jn < prior["judged"] else "reason"] = reason
        if prior:
            rec["previous"] = prior["judged"]
        ratchet_path.write_text(json.dumps(rec, indent=1) + "\n")
        print(f"\nratchet set to {jn}" + (f" (was {prior['judged']})" if prior else ""))
        return 0

    if prior and not prior.get("judged"):
        print(f"\nratchet: 0 — a floor of 0 cannot fall, so it has never proved anything. "
              f"Re-pin it with --set-ratchet once a capture has been judged.")
        hard += 1
    elif prior and jn < prior["judged"]:
        print(f"\nratchet: {prior['judged']} — FAILED, judged fell to {jn}")
        hard += 1
    elif prior:
        print(f"\nratchet: {prior['judged']} — {'held' if jn == prior['judged'] else f'rose to {jn}'}")
    else:
        print(f"\nno ratchet recorded yet — run with --set-ratchet to pin {jn}")

    if hard:
        print(f"\n{hard} hard failure(s). A wall of captures whose subjects are unproved is "
              f"a screenshot gallery, and a reader cannot tell one from evidence.")
        return 2 if "--gate" in args else 1
    print("\nEvery published capture names a target that ties to its subject.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
