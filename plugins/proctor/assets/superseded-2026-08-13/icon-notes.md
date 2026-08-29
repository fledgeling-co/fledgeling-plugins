# proctor icon — spec, decisions and audit notes

Direction **"Out of True"**. Built with the `create-mac-icon:create-mac-icon` skill: its
`icon-directions.md` pipeline (three engines, written audit sheet),
`material-recipes.md` for the constructions, and the skill's
`assets/squircle-path.txt` for the mask on the raster takes and the shipped
PNGs.

---

## The spec

**Concept.** One macOS window form registered **three times**, once per
observer, offset by a hair. Where the three agree the tile is quiet porcelain;
where they disagree the delta is vermilion. That is the skill's tri-observer
check drawn rather than described — the accessibility tree, the layer geometry
and the captured pixels each describe the same instant, and the disagreement is
the finding.

| Observer | Material | What it can see |
|---|---|---|
| The accessibility tree | a slate keyline, no fill | structure and controls — it is the only one that knows what a button is, so it is the only plane carrying the traffic lights |
| The layer geometry | a solid porcelain plane | rectangles. Dead centre; the one with mass |
| The captured pixels | discrete square samples | pixels, and only pixels |

The signature move is that **the accent is the disagreement**, and nothing
else. Vermilion appears in exactly two places: the run of samples where the
capture reports content the geometry says is not there, and a short fading
segment of keyline where the tree strays outside the true form. Both are
*findings*, not decoration.

**Direction.** Tahoe gel-glass, sub-register (a) — porcelain cushion tile
carrying coloured objects. Device bank **#21 overlap-as-identity** (Photos'
petals, Shortcuts' diamonds: two translucent primitives whose blend zone *is*
the mark) crossed with **#16, the icon performs the verb**. Runner-up was
Direction 8, Instrument Emblem — declined because the subject is not a reading,
it is a *comparison of three readings*, and a gauge has no grammar for a delta.

**What was rejected before rendering, and why.** Two of the three briefed
concept directions collapse into the sibling `design-review`, whose icon is a
translucent window stack with a vermilion registration reticle over it:

- *A registration mark over a window form* is that icon, near enough exactly.
- *An invigilator's sightline over a hall of windows* shares its window-stack
  composition and would have read as its variant.

Direction 1 — three registrations of one form, slightly out of true — was both
the most honest to the subject and the only one that is not already owned.
The separation from `design-review` now rests on three things and is worth
protecting: **register** (this tile is warm porcelain, `design-review` is the
one cool-ground sibling in the marketplace at `#F0F3F6`), **the distinction
carried** (three *materials* of one form, versus three identical panes at
different depths), and **no reticle**.

**Silhouette.** A window with a stepped, echoed edge. Nameable at 128 and 32.

**Ground register.** Porcelain / daylight, matching the marketplace default.
The dark register belongs to the sibling `trawl`.

**Palette.** Two hue families — warm neutral and vermilion — plus a
near-neutral cool slate, which is the same three-part scheme `armada-sync`,
`should-compact` and `clarify` use.

| Role | Hexes |
|---|---|
| Cushion ground | `#FCFAF5` → `#F3EEE3` → `#DCD3C1`, vignette `#8A7A62` |
| Geometry plane, face | `#FEFDFA` → `#F2ECE0` → `#DBD2C0` |
| Titlebar / content field | `#FEFCF8` → `#F4EFE4` / `#F1EBDF` → `#DBD2BF` |
| Tree keyline | `#333C4A` at 0.72 |
| Solid traffic dots | `#D8CEBB` (the dark sidebar was removed — see Revision) |
| Capture samples | `#E7ECF3` .12 · `#E0E5ED` .12 · `#8B97A9` .50 |
| Delta (the one accent) | `#FF7C33` → `#F4551C` → `#D33E0B` |
| Exterior spill (delta onto porcelain) | `#FF9257` |

**Light model.** One soft key up and to the left, on every plane and on the
cushion, plus a restrained bloom under the delta and soft inter-plane shadows
that carry the depth stack.

**Layer plan (#10).** `#bg` cushion, vignette, inner rim, ground shadow ·
`#tree` the accessibility keyline (at the back) · `#mid` the solid geometry
plane and the shadow it casts · `#fg` the capture's samples, its cast shadow and
the delta spill · `#highlight` rim lights and the capture's aperture edge.

**Geometry.** One window rect (548 × 380, R 34) drawn three times at identical
size — a stack varies in scale, a misregistration does not — offset
`AX (-70, -62, -1.3°)`, `GEO (0, 0, 0°)`, `CAP (+68, +60, +1.4°)`. The offsets
are large enough now to read as three windows stacked in depth (see Revision);
the rotation keeps the near band a wedge rather than a colourised drop shadow.
Every capture sample is looked
up against the geometry beneath it by `probe()`, so the two planes cannot drift
apart anywhere except where they are offset — the pixel grid is a measurement,
not a texture.

---

## Measured before the first line was authored

Sampled off the marketplace family rather than assumed, per
`material-recipes.md` ("measure the reference; never assume a relationship"):

| Property | Family | Used here |
|---|---|---|
| Ground, top-left → bottom-right | L 0.94 → 0.87, warm | 0.95 → 0.87 |
| Accent | hue 8–20°, S 0.77–0.97, V 0.88–0.98 | hue 12°, S 0.95, V 0.93 |
| Slate | `#171D22`–`#343A45`, S 0.25–0.32 | `#333C4A`, S 0.26 |
| Cool-ground siblings | 1 of 19 (`design-review`) | stays warm |

---

## Per-take scores

Full contact sheet with real renders at 128 / 64 / 48 / 32 / 16 plus the ×6
squint: `audit.html`.

| Take | Engine | Score | One line |
|---|---|---|---|
| **A** `icon.svg` | hand-authored layered SVG, `build_icon.py` | **11 / 12 — ships** | Passes all four non-negotiables; loses #7 on the solid plane at 1.01:1 |
| C1 `icon-engineC-6269c5.png` | GPT Image 2, 3 refs | 9 / 12 | Best material read; its registrations are offset far enough to read as a *stack*, which is `design-review`'s composition |
| C2 `icon-engineC-72c971-2.png` | GPT Image 2, 3 refs | 9 / 12 | Source of the dissolving fringe. Fails #10 as any flat raster does |
| B1 `icon-engineB-arrow-e8b602.svg` | Arrow 1.1 vector | 5 / 12 | Baked squircle; copied `clarify`'s motion lines out of the reference images |
| B2 `icon-engineB-arrow-23b7c2.svg` | Arrow 1.1 vector | 3 / 12 | `clarify`'s icon redrawn. No window, no registration, no delta |

Measured figure-ground on the shipped 1024 render (`render_audit.py` prints
these, so they are read off the artwork rather than remembered): tree keyline
vs tile **4.97:1**, content rows **2.46:1**, delta run **2.50:1**, 32px
luminance spread **0.502**. The solid geometry plane stays near-flat against the
porcelain (the #7 loss), which is the register's standing trade.

---

## Revision — the depth-stack pass

The first cut kept the three registrations offset by only a hair, on purpose: a
wide stack reads like the sibling `design-review` (a translucent window stack
with a registration reticle). Held against the raster takes it lost anyway — the
near-aligned forms ghosted into one muddy double, and the dark sidebar greyed
the focal plane. This pass takes the read C1/C2 won: the offsets open into a
legible depth stack, the dark sidebar is gone (value moves to the tree keyline,
the two content rows and the accent), soft inter-plane shadows carry the depth,
the accent warms toward the takes' vermilion, and the dissolve tightens to a
clean extrusion rather than confetti.

The move toward a stack is checked against the `design-review` differentiation,
which still holds on all three counts the separation always rested on:
**register** (this tile is warm porcelain; `design-review` is the cool-ground
sibling), **the distinction carried** (three *materials* of one form — keyline,
porcelain, pixel-grid — not three identical panes at different depths), and **no
reticle**. And the accent is held to the rule the icon is *about*, borrowed from
`be-my-witness`, the skill that judges a screenshot as testimony: the accent is
the disagreement, located and directional — vermilion only where the capture
overhangs the true edge, and faintly where the tree strays outside it — never a
decorative wash.

---

## What looking at it changed, that measuring would not have

Four rounds, each started by putting a render up and asking what was wrong with
it rather than by reading a number.

1. **The tree was drawn behind the solid plane, so it was 100% vermilion.**
   An outline behind an opaque plane can only ever show its overhang, and the
   overhang is by definition the part that disagrees — so the observer that was
   meant to be the quiet structural one rendered entirely as a finding.
   Fixed by z-order: geometry, then capture, then the tree drawn *over* the top,
   which is also how you would actually overlay an accessibility tree on a
   screenshot.

2. **Twenty-one repeated elements read as a screenshot, not a glyph.**
   The first draft carried four content rows plus three sidebar rows plus
   traffic lights, all drawn three times over. Anti-checklist #4/#5. Cut to two
   content rows, one sidebar division, and one titlebar, and the controls moved
   to the tree alone — each observer now reports only what it can see, which
   both declutters the titlebar (six offset blobs became three circles) and is
   the truer statement.

3. **A clean orange L reads as a border; a disintegrating one reads as an
   instrument disagreeing.** This is take C2's idea and the best thing either
   raster contributed. Rebuilt as geometry: past the capture's own frame the
   delta cells survive with probability `(1 - out/2.6)³`, seeded so the dissolve
   is identical on every build. Two bugs found doing it — measuring the box
   distance in all four directions rings the whole object in confetti, because a
   cell far enough up-left of the capture frame is also outside the geometry and
   scores as a delta it has no business reporting; and without weighting the
   probability by the same corner falloff the band uses, a lone sample strays
   out at the far end of an arm and reads as dirt on the tile.

4. **Porcelain on porcelain has no value separation at 16px.** Set beside the
   eight siblings it will sit next to, the first draft was the palest tile on
   the shelf and its 16px render was featureless. This is the failure already
   recorded against `clarify`, and it has the same fix: move part of the glyph
   down the value ramp and leave the focal plane porcelain. The first attempt
   took the sidebar to warm clay (`#B9AB90`) and was reverted at render — it
   worked on value and introduced a third hue family, and the tile read muddy.
   Slate (`#838D9C` → `#636D7B`) does the same job inside the palette the tree
   keyline already establishes, and it makes the capture's samples legible over
   it as light-on-dark, which is the "this plane is made of pixels" cue the
   porcelain version never had.

A fifth, recorded because it cost nothing here only because it was anticipated:
the `outsideTrue` clip has two subpaths and carries an explicit
`clip-rule="evenodd"`. SVG's nonzero default unions them silently, and a clip
that is quietly wrong reads as a material failure.

---

## Decisions made without asking

- **Warm register, not cool.** `design-review` owns the cool porcelain tile,
  and separation from it is this icon's main constraint.
- **The traffic lights belong to the tree.** Semantically right and it
  declutters; the cost is that the solid plane has no chrome detail of its own.
- **No fidelity loop against a raster reference.** The rasters both lost on
  *composition* rather than on material — their registrations read as a stack —
  so converging the master onto one would have dragged it toward the sibling's
  composition. The pipeline's own rule applies: the rubric outranks the gate,
  and the reference is not the ceiling. C2's one winning idea was rebuilt by
  hand instead.
- **Both Arrow takes kept in the sheet.** They failed badly and instructively:
  given two sibling icons as style references, the engine reproduced the
  *reference's* device rather than the brief's. A contact sheet that hides that
  is not an audit.

---

## Known liabilities

1. **The geometry plane is 1.01:1 against the tile.** Half the object separates
   from the ground by rim light and keyline alone, so it softens under
   grayscale or a heavy tint. The porcelain register's standing trade;
   `create-skill` and `create-mac-icon` share it exactly. First thing to look
   at if a Tinted variant reads weak.
2. **At 16px the three registrations collapse into one form.** The icon still
   reads — pale plane, slate left block, warm near-corner — but the
   tri-observer idea that makes it *this* icon is a 48px-and-up device.
3. **The sample grid and the content bars are legible only from 64px.** 32 and
   16 lean entirely on the sidebar, the keyline and the delta.
4. **A warm fringe on the lower-right of a pale rectangle can still be misread
   as a coloured drop shadow** at a glance. The 1.5° rotation and the dissolve
   are what argue against that reading, and both are large-size cues.
5. **The separation from `design-review` is real but not enormous.** Both are
   window forms. If that icon ever moves to a warm ground, or this one ever
   gains a reticle-like mark, the two will need re-separating.
6. **The banner's field is the weakest part of the pair.** At field scale the
   windows are near-monochrome porcelain-and-slate rectangles, so the right
   half reads as an abstract scatter of cards before it reads as the same
   window checked over and over; the icon carries nearly all the semantic load.

---

## Files

| File | What it is |
|---|---|
| `build_icon.py` | Engine A. Geometry and material as named constants; a fidelity round is a parameter edit, never path surgery |
| `icon.svg` | the shipped master, four named layers, generated — edit `build_icon.py`, never this |
| `icon.png`, `icon-256.png`, `icon-128.png` | exports from the master, squircle-masked |
| `render_audit.py` | writes the exports, masks the raster takes, and prints the figure-ground numbers the audit sheet quotes |
| `audit.html` + `audit-renders/` | the contact sheet, every take scored including the losers. `audit_sheet.py check .` exits 0 |
| `icon-engineB-arrow-e8b602.svg`, `icon-engineB-arrow-23b7c2.svg` | Engine B, Arrow 1.1 |
| `icon-engineC-6269c5.png`, `icon-engineC-72c971-2.png` (+ `-masked`) | Engine C, GPT Image 2 |
| `banner-src.html`, `banner.png` | the README banner, composed HTML at 1600×520 rendered 2× to 3200×1040 |

### The banner

Same structural grammar as the family — 1600×520, porcelain ground, lockup at
`left: 112px` with a 288px icon, wordmark and tagline, and the icon's own
device continued past the right edge. Type is **Space Grotesk**, whose squared
terminals read as a measuring instrument; no sibling uses it.

The field on the right is the rest of the campaign: the same window at the same
misregistration, checked over and over and running off the frame. Four of the
six are clean and two carry findings, which is the honest ratio and the whole
argument — a campaign is mostly quiet, and the report is the short list of cells
where the observers disagreed. Every number in it (`W`, `H`, `R`, both
registration offsets, both rotations, the sample pitch) is read out of
`build_icon.py` and scaled by one constant, so changing the icon re-derives the
banner rather than leaving it out of register.

The first cut ran three rows of five at 0.84× and was rebuilt: at that size the
registration offset is sub-pixel, so the field read as wallpaper and the one
device the banner exists to carry was invisible in every tile of it. Six larger
windows, individually placed rather than on a lattice, is what survives.
