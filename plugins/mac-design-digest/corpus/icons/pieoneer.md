# Icon: Pieoneer

- **Era:** Skeuomorphic-quote (glossy metal-on-black, on a modern squircle) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.webp, 204×204 — a downscaled web render; cover.png 1920×1080 marketing render used for material/brand context only)
- **Subject:** app switcher / launcher utility ("Switch, launch, and control apps"). Glyph is a camera **aperture / iris diaphragm** whose blades double as **pie slices** — the "Pie-" pun in Pieoneer, and a radial pie-menu metaphor for the app-switcher.

| Dimension | Reading |
|---|---|
| Background | Near-black field, subtle corner vignette: ~#222222 mid → #141414 edges → #000000 corners (measured, 204px render). Reads as flat matte black with a slight darkened-corner ramp, not a hue ramp. |
| Glyph | Object (camera aperture, ~8 overlapping blades spiralling around a central black hole). Silver/neutral ramp #F1F1F1 (lit upper-left blade) → #CBCBCB → #9A9A9A (shadowed lower/right blades). Optically centred on the larger grid circle (round glyph), fills most of the safe zone; slight downward/rotational bias from the spiral asymmetry. Central hole #212121 = base showing through. |
| Overlay device | None (no diagonal tool). The aperture *is* the whole glyph — a centred radial object, not a badge or frame. |
| Light model | Shipped webp: soft, roughly top-down sheen on the blades with thin dark shadow gaps between overlapping blades (baked micro-shadows). Cover render: heavier — dual specular sweep (top + bottom gloss) on a puffy 3D black base plus per-blade bevels and cast shadows. Marketing render embellishes the lighting the shipped icon states quietly. |
| Layer stack | back → front: (1) black glossy squircle base with corner vignette; (2) inter-blade shadow gaps; (3) silver aperture blades (each blade overlapping its neighbour clockwise); (4) central hole punched to base. Single baked render — not layered Icon-Composer glass. |
| Palette economy | Zero hue — pure neutral. One "family" (grayscale): black base + silver glyph. No saturated accent at all; the glyph is the accent by being the only light mass. Contrast does 100% of the hierarchy work. |

## Signature devices
- **Aperture-as-pie-slices double read** — the shutter-blade diaphragm simultaneously reads as pie wedges, carrying the "Pieoneer" pun and the radial pie-menu launcher metaphor in one glyph. [GOLDEN-NUGGET] the rare icon where the glyph *is* the wordmark joke.
- **Glossy skeuomorphic quote on a modern squircle** — beveled silver metal + glossy black plastic base is pre-flat "Aqua / Web 2.0" material language, deliberately quoted inside the current squircle mask. Dark, metallic, dimensional — the opposite of Big Sur's matte pastel restraint.
- **Monochrome-in-a-colourful-Dock** — an all-neutral icon is a deliberate identity bet: it reads as minimal/pro against colourful neighbours, at the cost of zero colour recall.

## Failures
- **#10 Variant robustness (Liquid Glass era):** not authored as Icon Composer layers. It is a single baked render with gloss/bevel/shadow **baked in** — which HIG explicitly forbids ("let the system handle blurring and effects; don't bake in specular highlights, drop shadows, bevels"). The monochrome palette *would* tint cleanly, but the baked black base collapses under clear-mode and no dark/tinted variant is designed. This is the one non-soft failure.

### Soft passes (flagged, scored as pass)
- **#4 16px squint:** high white-on-black contrast survives, but the 8-blade detail smears — at menu-bar size it reads as a generic light gear/flower/pinwheel, losing the specific "aperture" identity.
- **#5 single light model:** clean in the shipped webp; the cover render competes a top **and** bottom specular sweep — mixed-lighting tendency visible only in the marketing render.
- **#1 mask discipline / #9 era coherence:** shipped webp is a clean flat squircle; the cover bakes a puffy 3D bevel into the squircle edge itself (fighting what the system does). Shape-era (squircle) vs material-era (glossy skeuo) are mixed, but that mixing *is* the skeuomorphic-quote genre, so it reads as coherent-by-genre.
- **#6 palette economy:** passes trivially (one neutral family) but note the total absence of accent — no focal colour, contrast-only hierarchy.

## Rhymes with
- Dark, monochrome **pro/utility** icons with a metallic dimensional glyph on a glossy black base (the "black-based developer/menu-bar tool" family — screenshot tools, window managers, launchers).
- **Camera/aperture glyph** icons (Kaleidoscope-adjacent iris motifs) — but rendered skeuomorphic-metal rather than flat.
- Style-family guess for synthesis: *glossy-skeuomorphic-quote, neutral-monochrome utility* — distinct from the corpus's expected Big-Sur-matte and Liquid-Glass clusters. Hint only until ≥3 icons corroborate.
