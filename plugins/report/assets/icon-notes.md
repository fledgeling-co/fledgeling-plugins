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
