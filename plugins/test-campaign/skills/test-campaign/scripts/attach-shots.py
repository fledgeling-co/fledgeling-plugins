#!/usr/bin/env python3
"""Wire captured screenshots to the surfaces they depict.

WHY THIS EXISTS
---------------
Measured across twelve campaigns on 18 Aug 2026: one had 22 surfaces, 22 PNGs in
`evidence/shots/`, and **zero surfaces carrying a `shot` field** — so its evidence
page rendered no images at all while the evidence sat on disk beside it. The page
generator was working exactly as written; a surface gains a wall cell only when its
inventory entry names a `shot`, and nothing had ever written one.

That is the campaign's own failure mode turned on itself: the capture step and the
inventory were never connected, and the result looked like "no screenshots were
taken" rather than "screenshots were taken and lost". A reader cannot tell those
apart, and the second is much worse.

WHAT IT DOES
------------
Matches every image under the campaign's shots directory to a surface, by id first
and then by a slug of the surface's name or route, and writes `shot` into
inventory.json. Then it reports BOTH directions:

  * images that matched no surface — a capture whose subject nobody enumerated
  * surfaces that got no image — the gap the wall would otherwise render silently

Neither list is a warning to be skimmed. An unmatched image usually means the
capture step and the surface map disagree about what the surface is called, and
that disagreement is the thing that produced the empty page in the first place.

WHAT THIS TOOL CANNOT DO, AND WHY THAT MATTERS
----------------------------------------------
Matching is by NAME. `SURF-005.png` becomes SURF-005's picture because of its
filename, whatever bytes are behind it — and a later campaign proved how far that
goes wrong: 20 surfaces attached cleanly, every downstream gate passed, and the
images were of three unrelated documents. Twenty files, six distinct pictures.

So a filename match is a hypothesis, not evidence, and this tool now says so. It
refuses to --apply unless every attachment it makes is corroborated by an entry in
`evidence/shots/captures.json` naming what the capture channel was pointed at.
`--filename-only` proceeds without that corroboration and stamps each attachment
`"shotProvenance": "filename"` in the inventory, so the weakness travels with the
data instead of being forgotten at the next read. `references/capture-lineage.md`.

    python3 attach-shots.py <campaign-dir> [--shots evidence/shots] [--apply]
    python3 attach-shots.py <campaign-dir> --apply --filename-only   # records the weakness

Without --apply it prints what it would do and changes nothing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif"}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")


def candidates(surface: dict) -> set[str]:
    """Every name this surface could plausibly have been captured under."""
    out = {slug(surface.get("id", ""))}
    for key in ("name", "label", "route", "path"):
        v = surface.get(key)
        if v:
            out.add(slug(str(v)))
            out.add(slug(str(v).split("?")[0]))
    return {c for c in out if c}


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    d = Path(args[0])
    apply_changes = "--apply" in args
    shots_dir = d / (args[args.index("--shots") + 1] if "--shots" in args else "evidence/shots")

    inv_path = d / "inventory.json"
    inventory = json.loads(inv_path.read_text())
    surfaces = inventory.get("surface", [])
    if not surfaces:
        print(f"no surfaces in {inv_path} — nothing to attach to")
        return 1

    # THE BUILD, NEVER THE MOCK.
    #
    # capture-pairs writes the reference under `mock/` with the SAME surface id,
    # so a naive walk attaches whichever sorts last and the wall then shows the
    # DESIGN while labelling it the product. Measured: 15 of 56 surfaces were
    # pointed at their own mock. A reference belongs to the pair file, which is
    # what be-my-witness reads; it is never the surface's shot.
    images = (
        sorted(
            p for p in shots_dir.rglob("*")
            if p.suffix.lower() in IMAGE_SUFFIXES
            and "mock" not in {part.lower() for part in p.relative_to(shots_dir).parts[:-1]}
        )
        if shots_dir.exists()
        else []
    )
    print(f"surfaces={len(surfaces)}  images={len(images)}  shots dir={shots_dir}")
    if not images:
        print(f"\nNo images under {shots_dir}. This campaign captured nothing, which is a")
        print("different statement from 'the page has no screenshots' — say which one it is.")
        return 1

    man_path = d / "evidence/shots/captures.json"
    manifest_by_path: dict[str, dict] = {}
    if man_path.exists():
        try:
            manifest_by_path = {str(e.get("path", "")): e for e in json.loads(man_path.read_text())}
        except ValueError:
            print(f"! {man_path} is not readable JSON — treating every attachment as uncorroborated")
    uncorroborated: set[str] = set()

    by_candidate: dict[str, dict] = {}
    for s in surfaces:
        for c in candidates(s):
            by_candidate.setdefault(c, s)

    attached, unmatched, ambiguous = 0, [], []
    for img in images:
        stem = slug(img.stem)
        hit = by_candidate.get(stem)
        if hit is None:
            # a capture named `03-dashboard.png` still belongs to `/dashboard`
            trimmed = re.sub(r"^[a-z]*-?\d+[-_]?", "", stem)
            hit = by_candidate.get(trimmed) or next(
                (s for c, s in by_candidate.items() if c and (c in stem or stem.endswith(c))), None
            )
        if hit is None:
            # LANE + KEYWORD, and only when it is UNAMBIGUOUS.
            #
            # Captures are commonly named `<lane>-<ordinal>-<keyword>.png`
            # (`web-01-board.png`, `ios-03-items.png`) while surfaces carry a lane
            # and a prose name. Matching the filename's words against the names of
            # surfaces in that same lane recovers most of them — but ONLY where
            # exactly one surface matches. Two candidates is a disagreement to
            # report, not a coin to toss: a screenshot filed against the wrong
            # surface is worse than one filed against none, because it looks right.
            parts = [w for w in stem.split("-") if w and not w.isdigit()]
            lane = parts[0] if parts else ""
            words = {w for w in parts[1:] if len(w) > 2}
            if lane and words:
                pool = [s for s in surfaces if slug(str(s.get("lane", ""))) == lane]
                hits = [s for s in pool if words & set(slug(s.get("name", "")).split("-"))]
                if len(hits) == 1:
                    hit = hits[0]
                elif len(hits) > 1:
                    ambiguous.append(f"{img.name} → {', '.join(h.get('id','?') for h in hits)}")
        if hit is None:
            unmatched.append(img.name)
            continue
        rel = str(img.relative_to(d))
        if hit.get("shot") != rel:
            hit["shot"] = rel
            attached += 1
        # Provenance travels with the attachment. A capture the channel recorded
        # is evidence; a capture matched on its name is a hypothesis, and the
        # inventory should not present the two identically.
        entry = manifest_by_path.get(rel)
        if entry and entry.get("target"):
            hit["shotProvenance"] = "manifest"
            uncorroborated.discard(hit.get("id", ""))
        else:
            hit["shotProvenance"] = "filename"
            uncorroborated.add(hit.get("id", "?"))

    without = [s for s in surfaces if not s.get("shot")]
    print(f"\nattached={attached}  surfaces still without an image={len(without)}  unmatched images={len(unmatched)}")

    if ambiguous:
        print("\nAMBIGUOUS — more than one surface in the lane matched, so none was chosen:")
        for a in ambiguous:
            print(f"   {a}")

    if unmatched:
        print("\nIMAGES THAT MATCHED NO SURFACE — the capture step and the surface map disagree:")
        for name in unmatched[:20]:
            print(f"   {name}")
        if len(unmatched) > 20:
            print(f"   … and {len(unmatched) - 20} more")

    if without:
        print("\nSURFACES WITH NO IMAGE — the wall renders these as absent:")
        for s in without[:20]:
            print(f"   {s.get('id', '?'):<12} {s.get('name') or s.get('route') or ''}")
        if len(without) > 20:
            print(f"   … and {len(without) - 20} more")

    if uncorroborated:
        print(f"\nUNCORROBORATED — {len(uncorroborated)} attachment(s) rest on the filename "
              f"alone, because {man_path.name} has no entry naming what the channel was "
              f"pointed at:")
        for sid in sorted(uncorroborated)[:20]:
            print(f"   {sid}")
        if len(uncorroborated) > 20:
            print(f"   … and {len(uncorroborated) - 20} more")
        print("   → Have the capture step write captures.json. A filename is not evidence "
              "of a subject, and this is the exact shape in which a wall of 20 captures "
              "came to show three unrelated documents.")

    if apply_changes and uncorroborated and "--filename-only" not in args:
        print("\nREFUSED to write. Pass --filename-only to proceed on filename matching "
              "alone; each attachment is then stamped shotProvenance=filename so the "
              "weakness is visible to everything downstream.")
        return 1

    if apply_changes:
        inv_path.write_text(json.dumps(inventory, indent=1) + "\n")
        print(f"\nwrote {inv_path}")
    else:
        print("\n(dry run — pass --apply to write inventory.json)")
    return 0 if attached and not unmatched else 1


if __name__ == "__main__":
    raise SystemExit(main())
