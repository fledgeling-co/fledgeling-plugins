#!/usr/bin/env python3
"""shelf_check.py — find icons that read as each other on a shelf.

The gap this closes was found by the commission that had to fix its symptom.
`better-loop` and `better-goal` shipped as the same icon: the same cream dial,
charcoal hub, needle and vermilion top dot, differing only in a grey sweep arc.
At 16px they were one icon, and they sit next to each other in every listing.

The 12-point rubric in `references/icon-directions.md` scores an icon against the
house style and against its own subject. Every check is about the tile in front of
you. **Not one of them asks whether the tile already exists**, so a duplicate can
score 11/12 and ship, twice, and the audit sheet is right both times. A rubric
that examines one artifact cannot see a set property, which is why this is a
separate script rather than another row.

An audit on 2026-08-18 found seven duplicated glyph devices across 35 icons, plus
a soft cluster of five that all read as a white card with grey lines. That is a
fifth of the set, so this is not an edge case.

    python3 shelf_check.py <repo-root>              # rank every pair, flag the close ones
    python3 shelf_check.py <repo-root> --plugin foo # just foo against the rest
    python3 shelf_check.py <repo-root> --sheet      # write a shelf strip to look at

What it measures, and what it cannot. Two independent cheap signatures, because
either alone has a known blind spot:

  structure  a 16x16 grayscale signature, mean-centred and normalised, compared
             by correlation. Catches same-shape-same-value pairs. Blind to two
             icons that differ only in hue.
  silhouette IoU of the alpha-thresholded mass at 32px. Catches same-outline
             pairs. Blind to two icons with the same outline and different
             interiors, which is every icon in this family, since they all share
             the squircle and every pair scores 1.000. Reported for context only
             and never used to flag.

**Calibrated against known duplicates, and the result is worth knowing before you
trust a number here.** Measured on the set as it stood on 2026-08-18:

  create-swe-project vs ship-feature   0.633, and it is ship-feature's top match.
                                       A real duplicate (one vessel on a ramp
                                       entering pale water, twice). Caught.
  report vs whats-left                 0.758. Real: both are the white-card-with-
                                       grey-lines substrate. Caught.
  ship-armada vs ship-fleet            **missed entirely.** Not in ship-fleet's
                                       top five, whose best match is `report` at
                                       0.501. Both are vermilion hulls on the same
                                       blueprint-grid ground, so the device is
                                       shared, but three hulls in echelon and one
                                       hull put the mass in different places and
                                       the correlation collapses.

So this measures **how alike two tiles read**, which is the property that decides
16px survival, and not **whether two icons use the same metaphor**, which is a
semantic fact no pixel metric can reach. The seven duplicated devices the audit
found were found by a person looking at thirty-five icons, and that still has to
happen. Use this to catch what the eye misses on a long shelf, not instead of the
eye.

It also surfaced something nobody was looking for, and then looking at the actual
16px strip corrected it, which is the honest version of this finding. Six pairs sit
above 0.80. Rendered at 16px and magnified, roughly half are real:

  mockup-fidelity vs tui-craft  0.860  **real.** Both are a dark rounded square,
                                       centred, carrying one small warm mark.
  be-my-witness vs mac-doctor   0.827  **real.** Both are a ring with a small warm
                                       mark, though mac-doctor is notably cooler.
  braindump vs tui-craft        0.844  partial. A horizontal band against a square;
                                       they share a value recipe, not a shape.
  agent-voice vs gen-inv-portal 0.827  **false positive.** Two vertical warm bars
                                       against a dark panel with an interior glow.
                                       They do not look alike at any size.
  agent-voice vs mockup-fidelity 0.819 **false positive**, same reason.

So call it about 50% precision on this set, which is useful as a prompt and useless
as a verdict. `generate-investor-portal`'s own commission independently reported
that its icon "shares a signature with tui-craft and the new mockup-fidelity" at
16px, so where the metric and a careful reader agree, take it seriously.

The deeper thing the exercise exposed is about the standard rather than the icons.
The house style prescribes porcelain, one warm accent, and a volumetric object,
which means convergence on "dark mass on porcelain with one warm mark" is
structural rather than careless. Distinctiveness in this family has to come from
the object's shape and where the accent sits, because the palette and register are
fixed by the rules. That is worth knowing before treating any single high
correlation as a defect.

Neither number is a judgment. A high correlation means "look at these two side by
side", not "these are duplicates": `ship-armada` and `ship-fleet` are deliberately
near-siblings, and a metric cannot know that a pair is meant to rhyme. Read it as
a prompt to look, and record the decision in both `icon-notes.md` files.

Wired into `site/scripts/check-conformance.mjs` as of 2026-08-19. It was held back
while six pairs sat above the bar undecided, because a gate that is red from the day
it lands teaches people to ignore gates. All six have since been looked at and
recorded in `DECIDED`, so the check is green on the current set and any genuinely
new collision fails the build.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

# Above this structure correlation, two icons are close enough that somebody has
# to look at them together and write down which way it was decided. Calibrated on
# the better-goal/better-loop pair as it shipped, which scored well above it.
FLAG = 0.80

# Pairs a person has looked at side by side and decided. Same contract as the
# repo's other debt lists: a name here is a decision with a reason, visible in
# review, not a silent exemption. An entry says "these two are allowed to read
# alike, and here is why", so a genuinely new collision still trips.
#
# All six pairs that were above FLAG on 2026-08-18 have now been looked at, at 16px
# and magnified, and decided. Two were real and are allowed to stand; four were a
# partial or a false positive of the metric. Because the set is covered, this check
# is wired into site/scripts/check-conformance.mjs, where any genuinely new
# collision now fails the build.
DECIDED: dict[frozenset[str], str] = {
    frozenset(("mockup-fidelity", "tui-craft")): (
        "0.860. Both are a dark rounded mass centred on porcelain carrying one small "
        "warm mark, confirmed by rendering them at 16px rather than by trusting the "
        "metric. Allowed to stand: the shared reading is a value layout, not a shared "
        "device (offset slabs with an ember sliver against a terminal with a block "
        "cursor), and the two skills are never offered as alternatives to each other, "
        "so nothing depends on telling them apart at 16px. The convergence is also "
        "structural: the house style fixes porcelain, one warm accent and a volumetric "
        "object, which leaves shape and accent placement as the only axes of "
        "distinction. Decided 2026-08-19."
    ),
    frozenset(("be-my-witness", "mac-doctor")): (
        "0.827. Both are a ring with a small warm mark. Allowed to stand for the same "
        "reason, with one addition in its favour: mac-doctor is measurably cooler, and "
        "be-my-witness was re-grounded to warm porcelain on 2026-08-18 specifically to "
        "join the family, so the residual similarity is the cost of that correction "
        "rather than a defect introduced by it. A graticule lens and a usage ring are "
        "different devices doing different jobs. Decided 2026-08-19."
    ),
    frozenset(("braindump", "tui-craft")): (
        "0.844, and a partial rather than a real collision. braindump is a horizontal "
        "striated band and tui-craft is a square panel; they share a value recipe (dark "
        "mass, warm stripe) and not a shape, and at 16px the horizontal band is the "
        "distinguishing feature. Recorded rather than acted on. Decided 2026-08-19."
    ),
    frozenset(("braindump", "mockup-fidelity")): (
        "0.840, same reading as the pair above and for the same reason: a striated "
        "horizontal drum against two offset slabs. Both carry a dark mass and one warm "
        "element, which is what the metric is responding to. Decided 2026-08-19."
    ),
    frozenset(("agent-voice", "generate-investor-portal")): (
        "0.827 and a clean false positive. Rendered at 16px these are two vertical warm "
        "bars against a dark panel with an interior glow. They do not look alike at any "
        "size, and the correlation is an artefact of both concentrating dark mass "
        "centre-right on porcelain. Kept as a worked example of the metric's precision "
        "limit rather than deleted. Decided 2026-08-19."
    ),
    frozenset(("agent-voice", "mockup-fidelity")): (
        "0.819 and a false positive for the same reason as the pair above. "
        "Decided 2026-08-19."
    ),
}

SIG = 16          # signature grid
SIL = 32          # silhouette comparison size
ALPHA = 128       # alpha threshold for "this pixel is part of the mark"


def load_pil():
    try:
        from PIL import Image
    except ImportError:
        return None
    return Image


def signature(path: pathlib.Path, Image) -> tuple[list[float], set[tuple[int, int]]] | None:
    """(mean-centred normalised luminance vector, silhouette pixel set)."""
    try:
        im = Image.open(path).convert("RGBA")
    except Exception:
        return None

    small = im.resize((SIG, SIG), Image.LANCZOS)
    px = list(small.getdata())
    # Composite over mid grey so a transparent corner does not read as black and
    # inflate every correlation through a shared dark border.
    lum = []
    for r, g, b, a in px:
        f = a / 255
        r = r * f + 128 * (1 - f)
        g = g * f + 128 * (1 - f)
        b = b * f + 128 * (1 - f)
        lum.append(0.2126 * r + 0.7152 * g + 0.0722 * b)
    mean = sum(lum) / len(lum)
    centred = [v - mean for v in lum]
    norm = sum(v * v for v in centred) ** 0.5 or 1.0
    vec = [v / norm for v in centred]

    mask = im.resize((SIL, SIL), Image.LANCZOS).split()[3]
    sil = {(x, y) for y in range(SIL) for x in range(SIL)
           if mask.getpixel((x, y)) >= ALPHA}
    return vec, sil


def correlation(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def iou(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("repo")
    ap.add_argument("--plugin", help="compare only this plugin against the others")
    ap.add_argument("--sheet", action="store_true", help="write a shelf strip PNG")
    ap.add_argument("--flag", type=float, default=FLAG)
    args = ap.parse_args()

    Image = load_pil()
    if Image is None:
        print("shelf_check needs Pillow", file=sys.stderr)
        return 2

    repo = pathlib.Path(args.repo).resolve()
    icons = sorted((repo / "plugins").glob("*/assets/icon-256.png"))
    if not icons:
        print(f"no plugins/*/assets/icon-256.png under {repo}", file=sys.stderr)
        return 2

    sigs = {}
    for path in icons:
        name = path.parent.parent.name
        s = signature(path, Image)
        if s:
            sigs[name] = s
    names = sorted(sigs)

    pairs = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if args.plugin and args.plugin not in (a, b):
                continue
            corr = correlation(sigs[a][0], sigs[b][0])
            pairs.append((corr, iou(sigs[a][1], sigs[b][1]), a, b))
    pairs.sort(reverse=True)

    flagged = [p for p in pairs if p[0] >= args.flag
               and frozenset((p[2], p[3])) not in DECIDED]

    print(f"{len(names)} icons, {len(pairs)} pairs compared at {SIG}x{SIG}.\n")
    print("closest pairs by structure correlation:")
    for corr, sil, a, b in pairs[:12]:
        decided = frozenset((a, b)) in DECIDED
        mark = "ok  " if decided else ("FLAG" if corr >= args.flag else "    ")
        print(f"  {mark}  {corr:.3f}  silhouette IoU {sil:.3f}   {a}  vs  {b}")

    if args.sheet:
        strip = Image.new("RGBA", (len(names) * 72 + 16, 88), (245, 247, 248, 255))
        for i, name in enumerate(names):
            tile = Image.open(repo / "plugins" / name / "assets" / "icon-256.png")
            strip.alpha_composite(tile.convert("RGBA").resize((64, 64), Image.LANCZOS),
                                  (8 + i * 72, 12))
        out = repo / "site" / "icon-shelf.png"
        strip.save(out)
        print(f"\nshelf strip -> {out}")

    if flagged:
        print(f"\n{len(flagged)} pair(s) at or above {args.flag:.2f}. Look at each one side by "
              f"side and write the decision into both icon-notes.md files: either they are "
              f"meant to rhyme, or one of them needs a different device.")
        return 1

    print(f"\nNo pair at or above {args.flag:.2f}. Nothing reads as its neighbour by this measure, "
          f"which is not the same as nothing reading as its neighbour.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
