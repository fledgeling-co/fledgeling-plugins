# Series palette — validated, and how it got that way

The diagram skin (`style-guide.md`) owns `paper`, `ink`, `muted`, `accent` and the
rest of the single-accent editorial roles. This file owns the one thing that skin
could not do: **a categorical palette for charts that carry more than one series.**

Charts and diagrams fail differently. A diagram's accent is editorial — one or two
focal nodes, and everything else recedes. A multi-series chart spends colour on
*identity*, and identity is a perceptual claim: the reader has to tell Ember from
Cobalt, including the roughly 1 in 12 men and 1 in 200 women with a colour-vision
deficiency. That claim is measurable, so it is measured rather than eyeballed.

## The gate

```bash
python3 scripts/validate_palette.py "<hex,hex,...>" --mode light
python3 scripts/validate_palette.py "<hex,hex,...>" --mode dark --surface "#2d3142"
```

Exit 0 means no hard FAIL. Add `--pairs all` for scatter, bubble, choropleth and
small multiples, where any two marks can end up adjacent; use `--ordinal` for a
one-hue ordered ramp. Read the **exit code**, not the output — piping the run
through `tail` or `grep` reports that tool's status instead, which is how a
failing palette gets recorded as passing.

## The palette

Five slots, in this order. The order is part of the safety mechanism, not a
preference.

| Slot | Family | Light | Dark |
|---|---|---|---|
| 1 | sage | `#3f7a33` | `#63954f` |
| 2 | violet | `#5b4a8f` | `#8878cc` |
| 3 | mustard | `#b07d18` | `#bd8a25` |
| 4 | blue | `#2a6ea8` | `#5089d2` |
| 5 | rust | `#a4552c` | `#c96e40` |

Both modes pass all five computable checks. Worst adjacent pair: CVD ΔE 18.4
protan light / 18.7 deutan dark; normal-vision ΔE 22.8 light / 23.2 dark, against
a floor of 15 (OKLab ×100).

`accent` stays reserved for the focal series. These five cover the rest.

## Why it changed — the measurement that forced it

The predecessor shipped five "desaturated, editorial-tone" series colours chosen
by eye: sage `#7c8f6f`, dusty-blue `#5e7a9b`, mustard `#b8915a`, rust-brown
`#9c6b50`, slate `#6e6479`. Run against the gate they fail in both modes:

| Check | Light (predecessor) | Dark (predecessor) |
|---|---|---|
| Chroma floor | **FAIL** — 5 of 5 below 0.10 (0.035–0.086); they read as grey | **FAIL** — 5 of 5 below floor |
| Normal-vision floor | **FAIL** — worst pair ΔE 10.3 vs floor 15 | **FAIL** — ΔE 9.1 |
| Lightness band | pass | **FAIL** — 4 of 6 outside the dark band |
| Contrast vs surface | WARN — mustard 2.83:1 | pass |

The chroma failure is the interesting one, because it is exactly what
"desaturated and editorial" means when you measure it: a hue below the chroma
floor has stopped doing identity work and is a grey with a tint. Five near-greys
that a reader must tell apart is not a restrained palette; it is a palette that
has quietly stopped functioning while still looking tasteful in a swatch.

## How these values were derived

Snap-to-passing, per the method — hold the hue family, move lightness and chroma,
then let *order* separate what stepping cannot:

1. **Step each family for chroma ≥ 0.10 and the mode's lightness band.** This
   alone was not enough: mustard and rust are adjacent warm hues and stayed at
   ΔE 11.0, still under the 15 floor.
2. **Enumerate the orderings** of the five stepped hues and keep only those that
   clear every gate in both modes, picking the survivor with the highest worst
   adjacent normal-vision ΔE. Separating the two warm hues is what the winning
   order does — sage, violet, mustard, blue, rust — and it lifts the worst pair
   from 11.0 to 22.8.
3. **Re-step the one slot the second mode rejected.** Dark mustard at `#d3a03a`
   sat at L 0.736 against a 0.67 ceiling; darkening that slot alone to `#bd8a25`
   cleared the band with no change to the other four and no change to the worst
   pair.

The families are the predecessor's. What changed is that they are now saturated
enough to encode identity, and ordered so that no two neighbours collapse.

## Rules that come with the palette

- **Assign slots in fixed order, never cycled.** A sixth series is not a
  generated hue: fold the tail into "Other", facet into small multiples, or use
  composite encoding.
- **Colour follows the entity, not its rank.** Filtering a series out must not
  repaint the survivors.
- **Never colour nominal bars by their value.** One series is one colour; a
  value ramp on nominal categories re-encodes what bar length already shows and
  fails the categorical checks by construction. Ordered categories take a one-hue
  ramp validated with `--ordinal`.
- **A legend is always present for two or more series**, so identity never rests
  on colour alone; direct labels supplement it selectively.
- **Sequential is one hue light→dark; diverging is two opposed hues with a
  neutral grey midpoint.** Never a rainbow, never a hue at the midpoint.
- **Status colours are reserved** (good / warning / serious / critical) and never
  reused as "series 6"; they always ship with an icon and a label.

## Swapping in a brand palette

Onboarding a brand's hues follows the same three steps, in order: step each hue
into the band and over the chroma floor, enumerate orderings and keep a passing
one, then re-step whichever slot the second mode rejects. Run the validator
against **the brand's own surfaces** with `--surface`, not the defaults — a
contrast result against the wrong background is not a result.

If no ordering passes, the honest finding is that the brand cannot carry that
many simultaneous series. Cut the series count or facet; do not lower the floor.
