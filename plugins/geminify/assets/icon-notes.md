# geminify icon — commission notes

Direction **Tahoe Gel-Glass, porcelain sub-register (a)**, composition **"The Second
Leaf"**. Runner-up direction: Object Tile, dropped because the subject has no
physical noun — the thing this skill makes is a second reading of a file.

**Signature move: the count exists only in the overlap.** Two leaves of one page,
splayed into a V from a shared footing. The left is clay and in shade — the
`SKILL.md`, as written. The right is warm tinted glass — the `gemini.md` this skill
produces. Where they cross, and nowhere else, three tally rules are engraved into
the blend, the bottom one filled and lit from inside. A categorical scope stays a
word until a second reading turns it into a number.

## Takes

| Take | Engine | Score | Role |
|---|---|---|---|
| **C** `icon.png` | GPT Image 2, corpus-referenced, masked to the set superellipse | 11/12 | **ships as the tile** |
| **A** `icon.svg` | hand-authored layered SVG (`build_icon.py`) | 10/12 | the editable master |
| **B** `geminify-engineB-arrow-03ba9b.svg` | Arrow 1.1 | 6/12 | loser, kept |

Full sheet with every render and the reasons: `audit.html`
(`audit_sheet.py check` exits 0; 18 image references, all resolve).

C ships because this is a decorative marketplace tile with no macOS compositor
downstream, so the material has to be in the file — and C has it where A does not.
A ships alongside as the layered master every future round edits. C's liability is
the one 76% of the shipping field has: a flat raster's identity is a colour
relationship that dies under Dark/Clear/Tinted, so any variant context needs A.

## Three devices that were rejected before this one

Checked against the set rather than assumed, because the family's ground and accent
are shared and its devices are close together:

- **A companion plate with ruled ledger rows** — the concept this commission opened
  with. `clarify` already owns stacked plates with ruled rows and an ember dot, and
  the two would have been indistinguishable at 48px.
- **A page with a folded corner, the count on the fold's inner face** — `dossier-report`
  is exactly that, ember inner face and all.
- **A split tally stick, notches matching across the split** — the best of the three
  semantically (a debt was recorded by notching a stick and splitting it, so the
  counts had to line up to verify, which is this skill's gate). Rejected on
  silhouette: horizontal it is `improve-skill`'s bar, vertical it is a pause glyph.

## What the fidelity loop measured (r00 → r08)

Reference: take C. Metric tier is numpy only — luminance + SSIM + edges, no
torch/LPIPS on this machine, which is documented as blind to precisely the material
differences this commission turned on. Five-size mean composite:

| Round | Edit | Mean |
|---|---|---|
| r00 | baseline master | 0.6554 |
| r01 | splay from each capsule's own base, lens rim, crown | 0.6201 |
| r06 | geometry fitted to the reference's measured numbers | **0.7026** |
| r07 | lighter clay body for a stronger crown | 0.6957 |
| r08 | clay value restored — **ships** | 0.6989 |

**The geometry had to be solved, not eyeballed, and four rounds were spent
learning that.** Rotating a capsule about a low pivot moves its top outward by
roughly `(pivot_y − top) · sin(lean)`, so every attempt to make the pair splay
produced a pair 74–87% of the tile wide with the lens between them collapsed to a
slot — while the intent read perfectly well in the source. What fixed it was
measuring the raster's own geometry: its capsules are ~300px wide, **disjoint across
the upper third** (left 219–510, right 517–836, a 7px gap at y=315), merging below
it, with a union 60% of the tile wide and about a fifth of that union in the
crossing. Two capsules that overlap all the way up cannot read as a V however far
they lean — the gap at the top is the whole tell. Fitting `(width, height, overlap,
lean, pivot)` to those four numbers gave the shipped constants in one round, worth
+0.047 after four rounds of guessing had cost 0.035.

**r07 is the rubric-outranks-gate case.** Lightening the clay body bought a
stronger crown highlight and lost figure-ground against the porcelain field — the
documented `clarify` failure, where nine gate ACCEPTs bought similarity to a
weakness. Reverted at a cost of 0.004 composite. Measured on the shipped master:
ground-to-darkest is **4.75:1 at 32px and 3.95:1 at 16px**, clearing check #7.

**Two engines agreeing bought the composition.** Arrow was briefed from the same
spec, blind to the master and to the raster, and independently built two
overlapping capsules with a pointed almond and three tally bars. That agreement is
what justified spending rounds on the arrangement rather than treating the raster
as one opinion. Arrow lost on material and on two non-negotiables: it baked a
rounded-corner artboard mask after being told not to, and it applied no lean at
all.

## Construction worth reusing

- **The blend zone is the intersection of two clips, not a shape drawn by hand.**
  `<g clip-path="url(#leafl)"><g clip-path="url(#leafr)">` nests to a real
  intersection, so the wash and the tally rules can only ever land where the two
  bodies actually cross, and they follow automatically when the geometry moves.
  Each `clipPath` holds a single subpath deliberately: a clipPath with two subpaths
  and no `clip-rule` silently unions them.
- **The lens's own lit boundary is each leaf's outline clipped to the other's
  interior.** That was the single largest missing feature against the raster — it
  is what separates two overlapping fills from two crossing bodies — and authoring
  it this way means it cannot drift off the real edge.
- **A capsule has no extrusion band.** `LEAF_WALL` is 0 because with `r = W/2` the
  band the sibling cards use sits entirely inside the round end and draws nothing.
  Volume comes from the body's luminance range plus two side catches, grounding
  from the two-layer contact shadow.

## Not done

No blind panel has judged these takes. A material round on A — translucent clay
body, stronger lens rim — is the named next step, and `fidelity-runs/` holds every
round's score and maps for it to resume from.
