# Icon: Obsidian

- **Era:** Big Sur unified · **Rubric:** 12/12 (3 soft passes, 0 failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.webp, 204×204 web render — see resolution caveat) · **Category:** Writing
- **One-line:** A faceted violet gemstone (the "obsidian" crystal) centred on a graphite squircle — an object-as-logo mark, monochrome-violet on neutral dark.

| Dimension | Reading |
|---|---|
| Background | Dark charcoal squircle, subtle top-down vignette ramp `#252525`→`#1A1A1A` (near-flat, reads as one graphite field). Corners `#000` are outside the pre-applied mask. |
| Glyph | Object type — abstract faceted crystal/gem, optically centred (reads slightly high; base sits near the vertical mid). Occupies ~55% of the safe zone. |
| Overlay device | None — no diagonal tool, no badge, no frame. Single centred object. |
| Light model | Top / upper-left. Facet gradients brighten to a near-white specular catch on the upper-left face and darken toward the base; consistent across every facet. Background field a touch lighter at top. Baked, short, soft — no resolvable cast shadow. |
| Layer stack | back → front: (1) graphite squircle field, (2) crystal body / lower-base facets in mid-dark violet, (3) upper facets + specular highlight in light lavender→near-white. |
| Palette economy | One chromatic hue family (violet ramp `#F2DFFF`→`#1C102F`) on an achromatic dark field. The glyph hue *is* the accent — no second hue. Textbook economy. |

## Palette (measured, res-caveated)
- **Field:** `#252525`→`#1A1A1A` graphite squircle (achromatic).
- **Violet ramp (light→dark):** `#F2DFFF` (specular) · `#CCBAF4` · `#C1AAF4` · `#A683EC` · `#7549CC` · `#6332C6` · `#5C30B3` · `#5529AC` · `#1C102F` (deepest crevice).
- **Accent:** none separate — the violet glyph carries the whole chromatic budget.

## Signature devices
- **Object-as-logo faceted gemstone** — the app's entire identity is one nameable object (the obsidian crystal), not a generic glyph-on-gradient. `[GOLDEN-NUGGET]`
- **Low-poly gem rendering** — internal planes drawn as flat linear-gradient faces rather than a photoreal cut stone; the "cut" reads from gradient direction changes at facet seams, not from texture.
- **Near-white specular catch** on the upper-left facet — the single brightest note, giving the flat gem its glassy-mineral read.
- **Monochrome-violet on neutral-dark** — one hue does all the chromatic work; the field stays achromatic. The whole personality is temperature + facet, nothing else.

## Failures
- None (0 hard failures).

## Soft passes (flagged, scored as pass)
- **#2 Grid adherence** — horizontally centred and safe-zone-respecting, but the crystal's optical mass reads slightly *high*; base terminates near the vertical midline rather than below it. Within tolerance, worth noting.
- **#4 16px squint** — internal facet seams smear to a single violet blob at menu-bar size; the mark survives on colour + silhouette (bright violet on near-black), so identity holds, but the "cut gem" detail is a >64px story only.
- **#10 Variant robustness (Liquid Glass)** — not authored as layered glass; the light lavender faces and the whole violet ramp depend on the dark field for contrast and would wash on a *clear/light* or flatten under a *tinted* render. The solid silhouette alone yields a usable mono variant, so it clears the "glyph not silhouette-dependent on bg" bar — but the colour story is background-bound. Era-appropriate (this is a Big Sur mark, not a Tahoe one), flagged for forward-compat honesty.

## Resolution caveat
Source is a **204×204 WebP web render** (not a 1024 master). Facet edges show compression/anti-alias softness; boundary hex is approximate; any baked drop shadow or sub-facet micro-shadow is below the resolution floor. Squircle corners are **pre-masked** in this render (corners already black) — I am reading the final composite, not unmasked layers. Palette hex marked `(measured)` but treat as `(estimated)` given res + WebP.

## Rhymes with (hint — for synthesis, not canon)
- The **dark-tile brand-glyph** family: a single saturated brand object centred on a graphite squircle (developer-tool / note-app icons that drop one luminous mark on a near-black field). Style-family neighbours: single-object marks that lean on colour + silhouette rather than a diagonal-tool overlay.
- The **faceted-object logo** cluster: low-poly gem/crystal/mineral marks rendered as flat gradient facets. Rhymes on the "no scene, no tool, one luminous object" composition and the monochrome-hue-on-neutral economy.
