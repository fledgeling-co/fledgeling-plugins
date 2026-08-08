# create-skill icon - spec, decisions and audit notes

Direction **"The Pour"**. Built with the `create-mac-icon` skill, dogfooded:
its `icon-directions.md` pipeline (three engines, written audit sheet),
`material-recipes.md` for the constructions, `assets/squircle-path.txt` for
the mask, and `scripts/fidelity.py` for the measured loop.

---

## The spec

**Concept (user-approved, not redesigned).** A porcelain casting flask with
molten vermilion being poured into it, the finished form implied beneath. The
signature move is that the pour is caught **mid-air**: a skill is the moment
an intention becomes an object, which is what create-skill does. Its sibling
`improve-skill` sharpens something that exists; this one makes something that
does not.

**Direction.** Tahoe gel-glass, sub-register (a) - porcelain cushion tile
carrying a coloured gel object. Runner-up was Direction 1, Object Tile, and it
was declined: the subject is not a noun sitting still, it is a transition
happening, and Object Tile has no grammar for a moment.

**Device.** Bank #16 (the icon performs the verb) crossed with #18 (edge-bleed
physicality - the stream is cut by the top of the mask, so the tile is a window
on a bigger bench rather than a print) and #22 (emissive interior under glass, where
the melt is the sanctioned second light source and lights its own walls).

**Silhouette.** A stream falling into a squat vessel. Rendered filled black it
is nameable at 160px and still at 32px (`build_icon.py` emits the geometry, so
the test is on the designed shape, not on a luminance threshold).

**Ground register.** Porcelain / daylight, matching the marketplace default.
The dark register belongs to the sibling `trawl` and is not used here.

**Palette.** Two hue families, no more.

| Role | Hexes |
|---|---|
| Cushion ground | `#FFFDF8` → `#F6EFE1` → `#DDD0B7`, vignette `#8A7A62` |
| Porcelain, lit flank | `#FDF7E9` → `#F0E5D0` → `#D2C0A4` |
| Porcelain, shaded flank | `#D8CDB8` → `#A99B80` → `#7C6B54` |
| Melt (the one accent, kin to `#C4622D`) | `#FC8014` → `#EE3E03` → `#D22103` → `#BC1302` → `#6E0901` |
| Interior glow (melt on its own walls) | `#FF4A08` |
| Exterior spill (melt past the rim, onto porcelain) | `#FF9C60` |

**Light model.** One soft key up and to the left, plus the melt as an emissive
second source. The melt lights; it never casts.

**Layer plan (#10).** `#bg` cushion + vignette + the ground spill · `#mid`
flask body, rim annulus, cavity wall, pool, shadows, parting lines · `#fg` the
pour and the detached droplet · `#highlight` rim lights, the stream's two
flanks, the droplet specular, the cushion's inner rim. Maps 1:1 onto Icon
Composer.

**Geometry.** One dimetric ground plane with a single foreshortening constant
(`KY = 0.515`). Every horizontal surface - the mouth, the rim annulus, the
cavity, the pool - is the same disc at a different height, so they cannot drift
out of register. The pour is a **swept ribbon** (a centreline with a width
profile and a real hemispherical cap), never an outline: an outline reads as a
flat noodle, and the leading drop has to be part of the same body as the stream
or it looks stuck on.

---

## Distinguishing it from the siblings

`create-mac-icon` is the adjacent one and the distinction had to be
unmistakable. Theirs is a **finished tile leaving a mould** - solid, departing,
and built from the set's own superellipse at two removes. Mine is **liquid
entering one** - nothing has set, nothing is leaving, and the vessel is a
**round** two-part casting flask rather than a superellipse, so the two icons
do not share a single silhouette. Every other sibling device was checked at
render: trawl (deep-sea trawler, dark register), create-swe-project (hull at
first water), ship-armada (three hulls in echelon), improve-skill (plane iron
and shaving), design-review (window stack and reticle), armada-sync (list rows
with one lit), compaction-quality (banded disc).

---

## Per-take scores

Full contact sheet with real renders at 128/32/16 plus the ×6 squint: `audit.html`.

| Take | Engine | Score | One line |
|---|---|---|---|
| **A** `icon.svg` | hand-authored layered SVG, `build_icon.py` | **11 / 12 - ships** | Passes all four non-negotiables; loses #7 because the flask's *lit* flank is 1.01:1 against the tile beside it |
| B `icon-engineB-arrow-d2f7ef.svg` | Arrow 1.1 vector | 6 / 12 | Hard-fails #1 (baked corner radius and drop shadow) and #6 (a dusty mauve field is a third hue family) |
| C1 `icon-engineC-4a73ea.png` | GPT Image 2, 3 corpus refs | 9 / 12 | Fails #10 as any flat raster does; group sits low with a thin stream. Source of the two-part keyed flask |
| C2 `icon-engineC2-6c0a72.png` | GPT Image 2, 2 corpus refs | 10 / 12 | Wins the material read; fails #10. **The loop's reference** |

Measured figure-ground on the shipped 1024 render: melt vs tile **3.04:1**,
stream vs tile **3.16:1**, flask shaded flank vs tile **3.98:1**, flask lit
flank vs tile **1.01:1**.

---

## The fidelity loop

`fidelity.py` (numpy tier: luminance field + SSIM + edge F1 + mask IoU), take A
against take C2, round sources kept at `fidelity-runs/rNN.icon.svg`.

| Round | Edit class | 1024 | mean | Gate |
|---|---|---|---|---|
| r00 | baseline | 0.4268 | 0.5434 | - |
| r01 | material: contrast budget, deepen the dark end | 0.4525 | 0.5619 | ACCEPT +0.0924 |
| r02 | material: the melt's dark end | 0.4516 | 0.5604 | ACCEPT −0.0075 |
| r03 | composition: open the mid-air cascade | 0.4527 | 0.5602 | ACCEPT −0.0010 |
| r04 | material: reach the 3:1 figure-ground floor | 0.4525 | 0.5611 | ACCEPT +0.0046 |
| r05 | material: clear 3:1 cleanly - **ships** | 0.4528 | 0.5600 | ACCEPT −0.0054 |

**Baseline 1024 composite 0.4268 → final 0.4528.** Stopped after four
consecutive neutral rounds, which is the loop's stop condition. The residual
floor is composition, not material: C2's flask is larger, lower and lit across
the tile differently, and the metric cannot separate that from a material gap.

Two rounds were kept despite a flat composite, on the reference's own rule that
the score is a proxy for a human judgment: r03 made the signature mid-air
cascade legible, and r05 cleared a rubric floor the composite does not encode.

### What the measurements actually found

The `material-recipes.md` rule ("measure the reference, never assume a
relationship") earned its place twice here, both times against an assumption
that felt obviously true:

1. **Molten is not bright.** The first two drafts authored the melt as
   bright-and-yellow, reasoning that hot means light. Sampled on matched
   geometry, C2's melt sits at luminance **0.42 to 0.53** and hue **5 to 9
   degrees**; the drafts sat at **0.57 to 0.80** and hue **20 to 25**. The whole
   ramp moved 17 degrees toward red and about 0.22 down. That single correction
   is the difference between "peach plastic" and "material at temperature".

2. **A translucent stream is darkest along its axis.** The master was built
   with a bright hot core down the middle, which is what a lit rod looks like.
   C2's stream measures L 0.612 on its lit flank, **0.469 on its axis**, and
   0.504 on its shaded flank - the axis is the *darkest* part, because that is
   where the material is thickest and attenuates most. The core ribbon is now a
   dark axis and both flanks are lit; after the change the master reads
   0.631 / 0.469 / 0.510 against those three numbers.

A third finding is a construction rather than a colour: the two warm veils over
the melt (the stream's glow and the droplet's) were peach `#FF9C60`, the colour
the melt throws *onto porcelain*. Over the melt itself they were lifting it 0.12
in luminance and 8 degrees toward yellow. Light thrown by the melt onto the melt
is the melt's own colour; only what escapes past the rim goes peach.

---

## Decisions made without asking

- **Round flask, not a superellipse one.** Distinctness from `create-mac-icon`
  outranked the appeal of reusing the set's curve, which is that icon's own
  signature.
- **Two-part flask with a keyed parting.** Came out of take C1 and is
  factually right (a casting flask is a cope and a drag). Kept even though the
  key vanishes below ~48px: it earns rubric #11 at large sizes and costs
  nothing at small ones.
- **The stream enters through the top edge rather than from a drawn ladle.**
  A ladle would be a third prop and the anti-checklist's failure mode #5 is
  metaphor pile-up. Edge-bleed is a sanctioned Tahoe device and it buys the
  same information for one less object.
- **Take C2 kept as the reference rather than the ship.** Pipeline rule: a flat
  raster is failure mode #10 by construction, whatever it scores.
- **Ground warmed slightly off the sibling constants** (`#F7F3ED` → `#F6EFE1`,
  `#E8E1D6` → `#DDD0B7`) during r01. Set kinship is preserved; the shift is
  small and it was the measured fix for a field sitting 0.09 lighter than the
  reference's.

---

## Known liabilities

1. **The flask's lit flank is 1.01:1 against the tile beside it.** Half the
   body separates from the ground by rim light and contact shadow alone, so it
   softens under grayscale or a heavy tint. This is the porcelain register's
   standing trade and the sibling `create-mac-icon` icon shares it exactly.
   First thing to look at if a Tinted variant reads weak.
2. **The melt clears the 3:1 figure-ground bar at 3.04:1.** A bare margin.
   Widening it means darkening the accent further, which drifts it away from
   the set's vermilion - the trade was taken deliberately in favour of set
   coherence.
3. **The parting key and the detached droplet both disappear below ~48px.**
   The icon reads correctly at 16px, but the two devices that make it *this*
   icon are large-size only.
4. **The mass sits low** (bottom margin 105px against 227px at the sides),
   because the vessel stands on a ground plane while the pour occupies the
   upper half. Deliberate, but it makes the tile's top-left quadrant the
   emptiest region in the set.
5. **The fidelity composite plateaued at 0.4528 of a theoretical 1.0.** Most of
   the remaining distance is composition, not material, and no further round
   can close it without abandoning this composition for C2's.

---

## Files

| File | What it is |
|---|---|
| `build_icon.py` | Engine A. Geometry and material as named constants; a fidelity round is a parameter edit, never path surgery |
| `icon.svg` | the shipped master, four named layers, generated - edit `build_icon.py`, never this |
| `icon.png`, `icon-256.png`, `icon-128.png` | exports, all from the master |
| `render_audit.py` | renders every take at the sheet's 2× sources, masks the rasters with the exact superellipse, writes the exports |
| `audit.html` + `audit-renders/` | the contact sheet, every take scored including the losers |
| `fidelity-runs/` | six rounds: `rNN.icon.svg`, `rNN/score.json`, residual and edge maps |
| `icon-engineB-arrow-d2f7ef.svg` | Engine B, Arrow 1.1 |
| `icon-engineC-4a73ea.png`, `icon-engineC2-6c0a72.png` (+ `-masked`) | Engine C, GPT Image 2 |
| `banner-src.html`, `banner.png` | the README banner, composed HTML at 1600×520 rendered 2× to 3200×1040 |
