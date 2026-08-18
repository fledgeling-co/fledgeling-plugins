# `resume-session` icon — "The Kept Place"

Commissioned 2026-08-19, replacing the icon that shipped with the plugin on
2026-08-15. Everything here is reproducible from `build_icon.py` and the renders
in `audit-renders/`; the scored contact sheet is `audit.html`.

## Why it was re-commissioned

The predecessor's own honest audit scored it **8/12** with a non-negotiable among
the failures. Two numbers carried the case: the coupler node — the device the
whole concept rested on — measured **1.03:1** against the ground it sat on and
was gone entirely by 16px, and the right-hand card measured 1.48:1. The concept
was sound (a session handed from one context to another) and the execution was
pale-on-porcelain, which is the same failure `better-goal` had. Its shipped
composition also sat in the most crowded corner of this shelf: two cards with a
dot between them is `clarify`'s device, and its 16px signature correlated 0.658
with `should-compact`.

So the device changed rather than being re-shaded. The subject stayed: what
survives a break, and what is carried across it.

## Direction and device

**Direction:** Tahoe gel-glass, porcelain sub-register (a) — a warm porcelain
cushion carrying one dark object with a soft cast shadow. Runner-up was
Direction 1 (Object Tile, Tahoe-softened); the cushion register won because five
siblings already share it and the shelf has to read as one family.

**Device:** a closed bound ledger lying on the cushion, seen in a mild oblique
from above and in front, with a single vermilion register ribbon slipping out
from between the leaves at the fore-edge, folding over the edge and lying flat
on the tile.

**Signature move:** that crossing. The ribbon is the one thing that leaves a shut
session — it is the only saturated element on the tile, its fold carries a lit
rolled edge, and it ends in a swallowtail on the porcelain. The distinction from
the boundary-marking siblings (`should-compact`'s squeezed seam, `better-loop`'s
shim at a step, `improve-skill`'s before/after edge) is that nothing here marks
the break: the break is the shut cover, and the ribbon is what got carried over
it.

**Devices considered and dropped**, each killed on a render rather than in
argument:

- a latching lifting hook — three-value mock read as a **power button** at 512px;
- two cards and a dominant dark coupler (the predecessor's concept, rebuilt) —
  keeps the mark in `clarify` / `should-compact` territory, which is the one thing
  the brief ruled out;
- a weaving shuttle — a pointed oval with a bright core is an **eye**, and
  `be-my-witness` owns the lens;
- a cable-car trolley on a high line — the cable is a hairline and dies by 32px;
- a spool of thread — flanges either side of a wound core is a horizontal
  dark/warm/dark triband, which is `should-compact`, or vertical, which is
  `braindump`.

Two of the discards were built out as full takes and scored on the sheet (the
dovetail key, the baton).

## Light model

One soft key from the upper left, which is the family's own convention rather
than a preference: on all six siblings sampled the ground's brightest point sits
at x0.08 y0.08, and the Engine C raster's ground runs Y 0.804 at the upper left
to 0.590 at the lower right.

| Constant | Value | What it governs |
|---|---|---|
| `KEY_BEARING_DEG` | 48.0 | the direction the light travels across the tile; every gradient axis and both cast shadows are derived from it |
| `KEY_WORLD` | (−0.35, −0.46, 0.82) | the same key as a world vector, for the Lambert term on each face |
| `AMBIENT` | 0.16 | the floor under the Lambert term |

Face values are computed, not chosen: top 0.052 → `#414449`, left (head) face
0.049 → `#33363B`, near (fore-edge) face 0.027 → `#212327`. The left face is the
lighter of the two because its normal turns toward the key — which is also why
the projection shows it at all (see below).

## Cell geometry

An oblique projection in three world axes: `u` along the spine (head → tail),
`v` from spine to fore-edge, `z` up.

| Constant | Value |
|---|---|
| `P_DEG` / `P_DIR` | 6.5° → (0.9936, 0.1132) |
| `Q_DEG` / `Q_FORESHORTEN` / `Q_DIR` | 64°, 0.62 → (0.2718, 0.5573) |
| `BOOK_L` / `BOOK_W` / `BOOK_T` | 452 / 436 / 152 |
| `SQUARE` / `BOARD_T` / `SPINE_W` / `HINGE_IN` | 22 / 34 / 42 / 48 |
| `CORNER_R` / `SPINE_R_K` | 28, ×1.55 on the two spine corners |
| `RIB_W` / `RIB_AT` / `RIB_RUN` / `RIB_SKEW` / `RIB_TAIL` | 110 / 0.545 / 215 / 0.55 / 34 |
| `CENTRE` | (512, 492) — the ink's bbox centre, solved for, not nudged |

Because `Q` travels down-**right**, the tile shows the top face, the near
fore-edge face and the **left** (head) face; the tail face folds back onto the
cover and is never painted. Which faces a projection reveals is a property of the
axes, and getting it backwards left the head unpainted with the silhouette's own
fill showing through as a dark tab.

`BOOK_T` is the one dimension that was swept rather than reasoned: at 98 the tile
reads as a **mortarboard with the ribbon for a tassel**, and no material work
touches that. 152 is a ledger.

## Palette

Every colour is declared as (hue°, saturation, target relative luminance) and
solved to an exact hex by bisection, so a luminance can be stated as a luminance.
Two hue families — one warm, one cool near-neutral — plus one vermilion ramp
reserved for the ribbon (2.15% of the tile).

| Constant | hue / sat / Y | Hex |
|---|---|---|
| `GROUND_LIT` | 36 / 0.070 / 0.845 | `#F3ECE2` |
| `GROUND_DIM` | 34 / 0.165 / 0.615 | `#DBCCB7` |
| `VIGNETTE` | 32 / 0.520 / 0.055 | `#533F28` at 0.155 |
| `RIM_LIGHT` | 40 / 0.030 / 0.960 | `#FDFAF5` |
| `COVER_LIT` → `COVER_DIM` | 218 / 0.12 / 0.063 → 218 / 0.18 / 0.024 | `#44474D` → `#282B31` |
| `HEAD_LIT` → `HEAD_DIM` | 218 / 0.13 / 0.049 → 218 / 0.17 / 0.026 | `#3C3F44` → `#2A2D32` |
| `FORE_LIT` → `FORE_DIM` | 218 / 0.15 / 0.027 → 218 / 0.19 / 0.015 | `#2B2E33` → `#1E2125` |
| `SPINE_LIT` → `SPINE_DIM` | 214 / 0.12 / 0.060 → 218 / 0.17 / 0.028 | `#42464B` → `#2C2F35` |
| `PAGE_LIT` → `PAGE_DIM` | 34 / 0.30 / 0.395 → 33 / 0.37 / 0.255 | `#BEA585` → `#A18665` |
| `PAGE_LINE` | 32 / 0.42 / 0.165 | `#876C4E` |
| `PAGE_LIP` | 36 / 0.20 / 0.560 | `#D4C3AA` |
| `RIB_FLAT_LIT` → `RIB_FLAT_TIP` | 16 / 0.82 / 0.185 → 16 / 0.85 / 0.135 | `#CA5124` → `#B2431B` |
| `RIB_DRAPE_LIT` → `RIB_DRAPE_DIM` | 16 / 0.84 / 0.112 → 15 / 0.88 / 0.075 | `#A23E1A` → `#8A2F11` |
| `RIB_ROLL` | 26 / 0.44 / 0.520 | `#EEB385` |
| `SHADOW` | 28 / 0.50 / 0.030 | `#3E2D1F` |
| `BOUNCE` | 38 / 0.15 / 0.780 | `#F0E3CC` at 0.24 falling to 0 |

Two of these were set by measurement against a first draft that had them wrong:

- **The page block is not ivory.** On the raster it is a warm tan at Y 0.397,
  hue 33, saturation 0.31 — 1.43:1 against the ground beside it and 4.98:1
  against the boards that flank it. The first draft authored it at Y 0.47 and the
  tile read as an open laptop: a dark lid over a bright band.
- **The accent's luminance is set by rubric #7, not by taste.** At Y 0.205 the
  flat run measured 2.87:1 against this ground and failed. At Y 0.185→0.135 its
  median is 0.152, which is 3.58:1 by a clean patch pair — and HSL L 0.44, the
  family's shared accent lightness, so it does not read brown on the shelf. The
  raster's own ribbon sits at Y 0.132.

## Layer plan (#10)

Four real depth planes, not object groups — which is the specific thing the
predecessor failed:

| Group | Contents |
|---|---|
| `bg` | cushion ground, edge vignette, the tile's inner rim light |
| `mid` | both seat shadows, the ribbon's ground shadow, then the whole casting clipped to one rounded silhouette: hull, head face, head page block and its leaves, fore-edge face, fore page block and its leaves, the lip occlusion, the porcelain bounce, the cover's top face, its soft dome bloom, the spine roll, three raised bands, the hinge groove |
| `fg` | the ribbon: its exit slot, the flat run on the tile, the drape down the fore-edge |
| `highlight` | the cover's rim catch, the fold's rolled edge, one faint sheen along the run |

Verified rather than asserted: replacing **only** the `bg` group's ground and
vignette with a flat charcoal, touching nothing else, leaves the mark legible at
256 / 32 / 16px (`audit-renders/dark-probe.png`). A Dark variant would still want
the casting's ramp lifted; nothing is hostage to the porcelain.

## Engines

- **Engine A** — hand-authored layered SVG, three genuinely different devices
  (`icon.svg`, `icon-alt-key.svg`, `icon-alt-baton.svg`), all from `build_icon.py`.
- **Engine B — unavailable.** The Arrow 1.1 vector route returned
  `A positive credit balance is required for all requests, including BYOK` from
  its gateway and wrote no file. Engine A was widened to three takes in its place,
  which is the named deviation.
- **Engine C** — GPT Image 2 on the default route with four porcelain-register
  corpus references (`apple-12`, `apple-23`, `apple-28`, `apple-18`) →
  `icon-raster-c1.png`. Used as a measured material reference by hand; no
  fidelity-loop run directory exists in this plugin, and the audit sheet says so.

## Per-take scores

| Take | Device | Score | Why |
|---|---|---|---|
| **A** `icon.svg` | the shut ledger and its register ribbon | **11 / 12 — ships** | all four non-negotiables clear on real renders; casting 8.11:1, ribbon 3.58:1; nearest shelf neighbour 0.707. Fails #7 on the page block (1.97:1 against the tile, 3.42:1 against the boards) |
| B `icon-alt-key.svg` | a graphite board split, bridged by a vermilion butterfly key | 9 / 12 | #7 (the key is 1.94:1 against the body it sits in), #8 (the split is lit as a raised bar, not a valley), #11 — and its 16px signature correlates **0.891 with `shipyard`**, over the 0.80 shelf bar |
| C `icon-alt-baton.svg` | the carried object half out of its seat | 9 / 12 | #3 non-negotiable — filled black it names a cigarette; #8 (the chock reads as a lump behind it), #11 (a dark bar with a warm band is `better-loop`'s construction). Its ratios are the best on the sheet and its picture the worst |
| D `icon-raster-c1.png` | the same object, diffusion-rendered | 9 / 12 | #2 (77.6% of the tile wide), #7 (ribbon 1.95:1 by ring), #10 (flat raster, nothing to remap). The material target, never the master |

## Shelf decision

`shelf_check.py` at `--flag 0.0`, worst pair for this plugin: **0.707** against
`create-mac-icon`, then 0.685 `proctor` and 0.681 `ux-craft` — all under the 0.80
bar, and the predecessor's own worst pair (0.658 with `should-compact`) was a
correlation between two icons that genuinely shared a device. These three share
only "a dark compact object left of centre on porcelain". No device collision:
nothing else in the set is a bound book, and nothing else spends its accent on a
piece of cloth. Recorded here rather than in `create-mac-icon`'s notes because
none of the three needs changing.

## What would be improved next

1. The page block's 1.97:1 against the tile is the one number under the bar. The
   fix is not a lighter block — that is the predecessor's mistake — but a deeper
   bottom board so the block is flanked by more dark on the near side.
2. The signature crossing does not survive to 16px: at that size the tile reads
   as a book with a bookmark, not as a fold. Widening the drape relative to the
   run would buy some of it back, at the cost of the silk read at 128px.
3. The swallowtail's tip is 30px at its narrowest — under half a pixel at 16px,
   so it simply tapers away. It is craft at 128px and above and nothing below.
4. The ink is 64.6% of the tile wide, at the top of the #2 band, so the accent
   cannot grow without a re-centre.
