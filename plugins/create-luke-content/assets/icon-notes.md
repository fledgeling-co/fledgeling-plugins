# create-luke-content icon — spec, decisions, and audit notes

Direction **"Voice over Craft"**. Built with the `create-mac-icon` skill: its
`icon-directions.md` pipeline (three engines, written audit sheet),
`material-recipes.md` for Tahoe gel-glass constructions,
`assets/squircle-path.txt` for the shared marketplace superellipse, and
`scripts/fidelity.py` for measured rounds against corpus-steered rasters.

---

## The spec

**Concept.** Ghostwriting in Luke Rhodes' authentic voice requires two stacked
layers: the voice layer on top (cadence, tone, prose), resting on the structural
craft layer underneath (message hierarchy, grounded claims, measurement). The
icon visualises this argument directly: **there are two planes, and the one you
can see is resting on the one you cannot.**
1. **Lower plane (Craft):** An ember-orange precision measuring plate with fine
   millimeter graduations, metric tick marks, and a dashed calibration grid.
2. **Upper plane (Voice):** A soft-extruded translucent frosted glass sheet
   carrying left-aligned ragged-right prose lines (the corpus's reliable signal
   for prose: stacked capsule lines with a trailing short last line).
3. **Through-translucency:** The ember measuring rule and tick graduations show
   clearly *through* the frosted sheet from underneath, creating an authored
   overlap blend (Tahoe tell 5) that flat rasters cannot fake.
4. **The semicolon detail:** Luke's signature punctuation habit (semicolon over
   em dash) embossed cleanly at the end of the second prose line.

**Direction.** Tahoe gel-glass, sub-register (a): porcelain cushion tile
carrying a warm ember measuring plate beneath a frosted glass document sheet.

**Runner-up, declined.** **"The Matrix"** — a grid of voice attributes with a
highlighted cell; rejected because it reads as an analytics/data table rather
than ghostwritten prose, and the marketplace already carries grid instruments
(`ship-fleet`, `test-campaign`). Also considered: **"The Press"** — a movable
type block; dropped as a historical/print anachronism that conflicts with Tahoe
digital-native grammar.

**Device bank.** Bank #20 (data-as-glyph abstraction: prose reduced to capsule
lines with a short trailing terminal line) crossed with #21 (overlap-as-identity:
the blend zone between translucent glass and the underlying ember rule is the
mark), #7 (punctuation-as-identity: Luke's signature semicolon), and #16 (the
icon performs the verb: voice resting on craft).

**Signature move.** *Craft seen through voice.* The glowing ember measuring
rule and calibration grid are visible through the translucent frosted glass
body, establishing that the prose is grounded in structural discipline.

**Differences from `mockup-fidelity`.** `mockup-fidelity`'s "The Overlay" uses
two same-sized clay slabs off-register by a measured `(100, 76)`, with the accent
spent entirely in the exposed sliver gap between them, and the reference cut into
the porcelain. `create-luke-content`'s "Voice over Craft" consists of two
functionally distinct planes: an underlying precision ruled measuring plate
(Craft) glowing in ember, and an upper translucent frosted glass sheet carrying
left-aligned ragged-right prose lines and a semicolon mark (Voice). The accent
belongs to the lower measuring plane, and the hero relationship is *through*
rather than *beside*.

**Ground register.** Porcelain / daylight (`#F9F6EE -> #F3EFE4 -> #E4DDCB` with
warm `#4A3F2E` vignette and `#FFFDF8` inner perimeter rim light), matching the
fledgeling set default.

**Palette.** Two hue families, strictly disciplined:

| Role | Hexes |
|---|---|
| Cushion ground | `#F9F6EE` &rarr; `#F3EFE4` &rarr; `#E4DDCB`, vignette `#4A3F2E` at 15% |
| Inner rim light | `#FFFDF8` |
| Ember measuring plate (Craft) | `#F98848` &rarr; `#E15A20` &rarr; `#A62808`, wall `#8E2608` &rarr; `#541202` |
| Ember highlights & ticks | Core `#FFD8AB`, edge `#781E04`, engraved rule `#5A1402`, glow `#F79A61` |
| Frosted prose sheet (Voice) | `#FFFFFF` (94% opacity) &rarr; `#FAF5EC` (86%) &rarr; `#EDE3D0` (80%) |
| Glass wall & shadow | Wall `#887A68`, contact shadow `#241B12` |
| Prose capsule lines | Body `#4E4234` &rarr; `#362C20` &rarr; `#20180F`, lit top catch `#FFFDF8` |

**Light model.** One soft key up and to the left; soft AO under the frosted sheet
and contact shadow on the porcelain cushion; zero hard speculars.

**Layer plan (#10).** Authored as four named groups in `build_icon.py`:
- `#bg`: porcelain cushion, vignette, ambient ember bleed, plate contact shadow.
- `#mid`: lower ember measuring plate, 3D wall, engraved ticks, calibration grid, sheet contact shadow.
- `#fg`: translucent frosted glass sheet, glass wall, through-transmitted ticks and grid, ember bleed, prose capsule lines, embossed semicolon.
- `#highlight`: lit top arris highlights, left edge catches, cushion perimeter rim light.
Maps 1:1 onto Icon Composer layers.

**Geometry.** Measuring plate `216, 256, 540, 500, R=40`; prose sheet
`290, 190, 520, 530, R=36`. Bounding union spans 620&times;566, centred on (508, 455),
occupying 60.5% of tile width inside the 55–65% target safe zone.

---

## Per-take scores

Full contact sheet with real renders at 128 / 64 / 48 / 32 / 16 plus &times;6
squint magnification: `audit.html`.

| Take | Engine | Score | One line |
|---|---|---|---|
| **A** `icon.svg` | hand-authored layered SVG, `build_icon.py` | **11 / 12 — ships** | Clears all four non-negotiables; 16px in-mask luminance spread **0.2481** (47% above marketplace median 0.169); full #10 layer plan; loses #7 on lit frosted top edge (2.3:1 against porcelain) |
| B `icon-engineB-arrow-466c65.svg` | Arrow 1.1 vector | 6 / 12 | Baked its own inner card boundary (#1), floats inset (#2), 30.6% warm orange wash (#6), flat 2D vector without Tahoe depth (#9), single layer (#10) |
| C1 `icon-engineC-69eefc-masked.png` | Gemini 3 Pro raster, corpus-steered | 10 / 12 | **The material target.** Rich volumetric through-read; fails #10 as a baked flat raster and #6 on accent restraint (14.5% warm-saturated share) |
| C2 `icon-engineC-778ac2-2-masked.png` | Gemini 3 Pro raster take 2 | 9 / 12 | Measuring mat spans whole tile, losing the distinct lower plane; fails #10, #3 (diffuse silhouette), and #4 (grid noise at 16px) |
| C3 `icon-engineC-gpt-18fd60-masked.png` | GPT Image 2 raster take | 9 / 12 | Ruler placed beside card rather than underneath, losing the stacked "Voice over Craft" relationship; fails #10 and #6 (22.2% warm share) |

### Measurements on masked 1024 renders

| Metric | Take A (ships) | Take B | Take C1 | Take C2 | Take C3 | Marketplace median |
|---|---|---|---|---|---|---|
| **16px in-mask luminance spread** | **0.2481** | 0.2174 | 0.2394 | 0.2249 | 0.2400 | **0.1690** |
| **Warm-saturated share of tile** | **3.9%** | 30.6% | 14.5% | 6.6% | 22.2% | ~6.5% |
| **Figure-ground (prose vs sheet)** | **4.85:1** | 1.82:1 | 3.60:1 | 2.90:1 | 3.40:1 | >3.0:1 |

---

## Measured rounds

`fidelity.py` scored candidate SVG against reference C1 (`icon-engineC-69eefc-masked.png`)
over three rounds stored in `fidelity-runs/rNN/`:

| Round | Edit class | 1024 composite | 16px composite | 16px self-contrast |
|---|---|---|---|---|
| r00 | baseline initial draft | 0.5088 | 0.7666 | 0.4187 |
| r01 | deeper volumetric ember, enhanced glass transmission, sculpted lines | 0.5053 | 0.7673 | **0.4382** |
| r02 | refined contact AO, graduation catches, highlight polish — **ships** | 0.5053 | **0.7673** | **0.4382** |

---

## Known liabilities

1. **The semicolon punctuation mark is sub-legible below 48px.** It is a diegetic
   craft garnish that resolves cleanly at 128px+ while the ragged-right capsule stack
   carries the small-size read.
2. **Lit top highlight of the frosted sheet sits at 2.3:1 against porcelain ground**,
   standard for the porcelain register.
3. **Metric tier was numpy (no torch on machine)**, so material was confirmed by
   hand-sampled pixel inspection rather than LPIPS.

---

## Deliverables index

| File | What it is |
|---|---|
| `build_icon.py` | Engine A master generator: geometry and material as named constants |
| `icon.svg` | Shipped layered master (four named groups, Icon Composer ready) |
| `icon.png`, `icon-256.png`, `icon-128.png` | Exported pngs for marketplace and READMEs |
| `icon-engineB-arrow-466c65.svg` | Engine B Arrow 1.1 vector take |
| `icon-engineC-69eefc.png` (+ `-masked`) | Engine C1 Gemini 3 Pro raster (material reference) |
| `icon-engineC-778ac2-2.png` (+ `-masked`) | Engine C2 Gemini 3 Pro raster take 2 |
| `icon-engineC-gpt-18fd60.png` (+ `-masked`) | Engine C3 GPT Image 2 raster take |
| `audit.html` + `audit-renders/` | Contact sheet with all 5 takes and retina sources |
| `fidelity-runs/r00..r02/` | Fidelity run history with `score.json`, residual, edge maps |
