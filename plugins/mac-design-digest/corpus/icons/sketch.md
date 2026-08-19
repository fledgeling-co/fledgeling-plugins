# Icon: Sketch

- **Era:** Flat-transition (Yosemite–Catalina artwork language), shipped inside the system squircle without a Big Sur / Liquid Glass redesign · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp`, 102×102px web render (heavily downscaled; see caveats)

| Dimension | Reading |
|---|---|
| Background | Near-white flat ground, subtle top-down ramp `#F8F8F8` → `#F5F5F5` (measured, near-imperceptible); absolute corners render pure `#FFFFFF` — a pre-masked web export, not a full-bleed 1024 master |
| Glyph | Single object: a front-facing, symmetrical faceted amber gem (cut diamond / jewel). Optically centred, sized large — crown spans most of the canvas width, bleeds close to the left/right safe-zone margins |
| Overlay device | None — no diagonal tool, badge, or frame; the gem sits alone on the ground |
| Light model | Top-down. Crown top facets carry the pale-yellow highlight (`#F8E867`, specular tip up to `#FAFCFF`); value steps down the pavilion to deep burnt-orange facet edges (`#F65F02` → `#A32B00`); flat per-facet shading, no cast shadow, no true specular glass |
| Layer stack | back → front: (1) near-white subtly-graduated ground · (2) amber faceted gem body (crown + pavilion as one flat illustration) · (3) pale-yellow crown highlight facets. Effectively 2 planes — depth is illustrated, not stacked |
| Palette economy | One hue family: amber/gold → deep orange ramp, plus a near-white ground. The gem *is* the accent; no separate accent hue. Textbook economy |

## Palette (sampled)

- **Background:** `#F8F8F8` → `#F5F5F5` (essentially flat near-white)
- **Gem highlight / crown:** `#FAFCFF` (specular) · `#F8E867` (pale-yellow crown)
- **Gem body (amber):** `#FFAD03` · `#FEAC00` · `#FFCF03`
- **Gem edges (deep orange):** `#F65F02` · `#F35900` · `#A32B00`
- **Grayscale check:** ground 248 · crown 183 · edge 74 · bottom point 187 — figure-ground holds; darkest facet edges (~74) give a firm ≥3:1 against the 248 ground, and the diamond silhouette survives a value-only read

## Signature devices

- **[GOLDEN-NUGGET] The amber faceted "jewel."** A low-poly, front-facing cut-gem is the entire identity — one of the most recognisable marks in design tooling. Personality is maximal from a single abstract object; no glyph-on-gradient anonymity here.
- **Gem-on-white, no background field.** Unlike Big Sur unified icons (which float a glyph on a filled coloured rounded-square), Sketch places the object on a minimal near-white ground. This empty-field composition is a flat-transition-era tell and the reason the icon reads calmer / older than its Dock neighbours.
- **Value-stepped facet shading.** Depth comes from flat per-facet value jumps (crown light → pavilion dark → burnt-orange edges), not gradients-as-glass — a hand-illustrated low-poly language rather than rendered material.

## Failures

- **#10 Variant robustness (Liquid Glass era):** not a Liquid Glass composition — flat raster gem with no glass layers, specular refraction, or Default/Dark/tinted-variant authoring. Compositionally the amber gem *would* survive a dark render (amber pops on dark, doesn't depend on the white ground), but as shipped it reads pre-Tahoe/legacy beside native macOS 26 layered-glass icons. The only genuine miss.

## Soft passes (flagged, counted as pass)

- **#1 Mask discipline:** gem bleeds close to the left/right safe-zone margins — large presence, but does not fight the mask.
- **#4 16px squint:** verified by downscale — silhouette and amber colour identity hold cleanly; internal crown facet lines smear at menu-bar size, but the gem is unmistakable.
- **#8 Depth coherence:** coherent top-down shading, but depth is illustrated via facet value-steps, not stacked planes or true layers.
- **#9 Era coherence:** internally consistent, but it is a flat-transition low-poly gem quoted forward into the system squircle — a legacy language, not a current-era design.

## Rhymes with

- The **single-saturated-object-on-near-white-ground** family: creative-tool marks that put one illustrated object alone on a minimal light field rather than on a colour-filled Big Sur field.
- The **jewel / crystal / gem logo** family — low-poly faceted marks in a single warm hue.
- Style-family hint for synthesis: *flat-transition free-object glyphs*; contrast against the Big Sur "glyph-on-coloured-squircle" cluster and the Liquid Glass "layered-glass" cluster — Sketch is neither, and that's the finding.

## Cross-icon / brand notes

- **Cover coherence:** the cover (`cover.jpg`, 2000×1000) reuses the *same gem silhouette* as a monochrome/black mark against a pink-lilac gradient. Brand constant = the gem shape; colour treatment varies (amber in the app icon, monochrome + pink on marketing). Icon-to-cover palette coherence is moderate — the shape carries the brand, not the hue.
- **Resolution caveat:** 102×102 source. Facet edge hexes are clean but any subtle Big Sur material grain/noise or precise mask corner-radius cannot be confirmed at this scale; era classification rests on the artwork *language*, which is unambiguous even downscaled.
