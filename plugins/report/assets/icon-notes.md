# Icon — "The Fold"

**Concept.** One sheet, creased once across its width, doing two things at once. Above
the crease it is a single uninterrupted column of ruling — the report as it reads on
screen, continuous, no seams. Below the crease the same sheet has separated into stacked
leaves — the same document paginated onto A4. The crease is the only place the two states
meet, and it is where the colour comes out.

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
via `rsvg-convert`. Every proportion is a named constant at the top of the file; a fidelity
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
- **Engine A was widened instead**, per the skill's own fallback clause, to
  `build_icon_a2.py` → `icon-A2-fold-inverted.svg`: the same fold with its values inverted —
  graphite sheet on the same porcelain ground, ruling knocked out in porcelain, crease as a
  recessed slit of light. It answers the shipping take's figure-ground failure by 9.2× and
  loses a point of its own, because the slit touches neither plane it is supposed to join.

`audit.html` carries all four takes with their scores, the measurements behind them, and the
Dark and Tinted variant renders that `variants.py` produces. The recommendation there is A2 at
11/12 against the master's 11/12, on the substance of the two failures rather than the count —
and nothing was swapped, because which take ships is not a decision this pass gets to make.

