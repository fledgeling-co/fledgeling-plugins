# Icon — "The Fold"

The direction below is shared by both hand-authored takes. The palette and regeneration notes in
this first section describe the **porcelain** take, which shipped 9–19 Aug 2026 and is now
`icon-A1-porcelain.svg`. What ships from 19 Aug is the inverted take, in `icon.svg` — see
*The swap, 19 Aug 2026* at the foot of this file.

**Concept.** One sheet, creased once across its width, doing two things at once. Above the crease
it is a single uninterrupted column of ruling — the report as it reads on screen, continuous, no
seams. Below the crease the same sheet has separated into stacked leaves — the same document
paginated onto A4. The crease is the only place the two states meet, and it is where the colour
comes out.

That is the skill's architecture in one silhouette: **one source, two renderings.**

**Why not dossier-report's icon.** That one is also a page with a fold, so the distinction
had to be deliberate rather than incidental. Its fold is a *diagonal corner flap* revealing
the page's own underside. This crease is *horizontal*, spans the full width, and what it
reveals is a *stack* — a different axis, a different object, the same family.

**What the small size forced.** The first cut used three leaves of the same width as the
sheet above, separated by 20px gaps. At 1024 that read exactly as intended. At 32 it read
as one document with a red line through it: a 20px gap survives a 32× reduction as 0.6 of
a pixel, so the pagination simply disappeared and the metaphor went with it.

The fix was not bigger gaps — it was making the two halves **differ in silhouette**, which
is the one property that survives any reduction. The paginated half is now inset and steps
inward leaf by leaf, so even when every internal rule has blurred away the shape still
says: wide block, coloured band, narrower stepped blocks. Two leaves instead of three,
because the third bought nothing once the gaps had to be that wide.

**Palette.** Warm porcelain ground, paper faces, one vermilion accent at the crease —
the family's single warm note, the same register as `dossier-report` and `create-mac-icon`.
Everything else is neutral, so the crease is the only thing the eye is sent to.

**Regenerating.** `python3 build_icon.py` writes `icon.svg` and rasterises 1024 / 256 / 128
via `rsvg-convert`; `python3 build_icon_a1_porcelain.py` writes `icon-A1-porcelain.svg` and
rasterises nothing. Every proportion is a named constant at the top of each file; a fidelity
round is a parameter edit, never path surgery on the output. The squircle silhouette is
read from `create-mac-icon/assets/squircle-path.txt` so the whole family shares one tile.

## The engines, run 19 Aug 2026

The icon shipped on 9 Aug from Engine A alone. The other two were commissioned on 19 Aug and
one of them came back.

- **Engine B (Arrow 1.1, `svg: true`) refused** — "A positive credit balance is required for
  all requests, including BYOK". There is no independent vector take, and nothing was salvaged
  from one.
- **Engine C returned two rasters** (GPT Image 2, one call, `n: 2`), steered with
  `apple-23` / `apple-28` / `apple-31` / `apple-27` from `create-mac-icon`'s
  `references/corpus/apple-2026/` — the porcelain register. `icon-engineC-c04596.png` and
  `icon-engineC-b88abc-2.png`. Both carry the best *material* in the set and both fail check 4
  outright: at 16px the panel is a ghost at 1.05:1 against the ground and only the accent
  survives. Both also read the crease as a cylindrical rod laid across the front of the sheet,
  which is a highlighter marking a page rather than a fold generating the pagination below it.
- **Engine A was widened instead**, per the skill's own fallback clause, into what the audit sheet
  called take A2: the same fold with its values inverted — graphite sheet on the same porcelain
  ground, ruling knocked out in porcelain, crease as a recessed slit of light. It answers the
  porcelain take's figure-ground failure by 9.2× and loses a point of its own, because the slit
  touches neither plane it is supposed to join. That take is now the shipping master, `icon.svg`
  built by `build_icon.py`; the names `build_icon_a2.py` and `icon-A2-fold-inverted.svg` no longer
  exist.

`audit.html` carries all four takes with their scores, the measurements behind them, and the
Dark and Tinted variant renders that `variants.py` produces. The recommendation there is A2 at
11/12 against the master's 11/12, on the substance of the two failures rather than the count —
and nothing was swapped, because which take ships is not a decision this pass gets to make.

## The swap, 19 Aug 2026

**A2 now ships.** The user made the call, and made it against the recommendation put to them,
which was to keep the porcelain master. Recording it as a decision rather than as a
measurement, because no measurement moved: the two takes still tie at 11/12 and every figure
in the sheet is the one that was there before the columns changed places.

The reason given was the one asymmetry in the comparison. Both takes fail in exactly one
register and they are opposite registers — porcelain measures **1.04:1** face-to-ground on
Default and **11.72:1** on Dark; the inverted take measures **10.03:1** on Default and
**1.10:1** on Dark. Default is what people see: the README row, the marketplace tile, the
digest email, the Finder list. Legibility bought on Dark is bought where almost nobody is
looking. The counter-argument was real and was overruled — the takes tie on count, the
porcelain artwork was already shipping in three rasters and two surfaces, and the inverted
take arrives with a deduction of its own plus a lineup risk against `tui-craft`.

Two liabilities ship with it, and neither is hidden:

1. **#8, the floating accent.** The slit spans y=512–536 with a 7px gap to the sheet above and
   a 27px gap to the first leaf below, so the crease touches neither of the two planes the
   direction says it joins. Invisible below 128px, bridged by the glow at 1024. One named
   constant in `build_icon.py` fixes it and it is the cheapest remaining point in the set.
2. **Dark at 1.10:1.** Not a rubric deduction, since #10 passes on all three rendered
   registers, but the graphite sheet nearly merges into a dark ground and legibility there
   rests entirely on the ruling's 6.90:1 against its own face. The porcelain take was 11.72:1
   in that register. This is the icon to look at first if the family ever ships a Dark-first
   surface.

**File layout after the swap.** The canonical names did not move, the artwork behind them did.
`build_icon.py` now builds the inverted fold into `icon.svg` and rasterises 1024 / 256 / 128,
so the three shipped rasters come from the new master and match it byte for byte.
`build_icon_a1_porcelain.py` builds the porcelain artwork into `icon-A1-porcelain.svg` and
rasterises nothing, so running it cannot touch a shipped file. `build_icon_a2.py` and
`icon-A2-fold-inverted.svg` are gone rather than kept — after the promotion each would have
been a second name for a file that already exists, which is the confusion the rename was meant
to avoid. The contact sheet renders the shipping take under the id `master` and the porcelain
take under `A1`, in `audit-renders/` and `variant-renders/` both.

### Two new shelf flags, unresolved

`shelf_check.py` was clean before the swap — no undecided pair at or above the 0.80 flag. The
swap created two, and neither is the one the audit predicted:

| pair | before | after |
|---|---|---|
| `report` vs `agent-voice` | +0.446 | **+0.809** |
| `report` vs `generate-investor-portal` | +0.432 | **+0.808** |
| `report` vs `tui-craft` | +0.428 | +0.534 |

The predicted collision did not happen. The audit named `tui-craft` as the lineup risk and
measured +0.477 on the SVG; on the shipped 256px raster it is +0.534, up but nowhere near the
flag. What did move is the pair the audit was not watching, and both new flags land inside a
cluster `shelf_check`'s own `DECIDED` list already characterises: `agent-voice` vs
`generate-investor-portal` at 0.827 and `agent-voice` vs `mockup-fidelity` at 0.819 are both
recorded there as **false positives** — "two vertical warm bars against a dark panel with an
interior glow", an artefact of concentrating dark mass centre-right on porcelain. The inverted
fold is now a third dark panel on porcelain, so it has joined that cluster on the same
signature. The script's own calibration puts precision on this set at roughly 50%.

**Nothing has been written into `DECIDED` for either pair, and nothing should be until someone
looks at a 16px strip of the three side by side.** A collision the user has not ruled on is a
finding, not a fix, and the metric is explicitly a prompt rather than a verdict.

