# Icon: Looq: Preview Files for Mac

- **Era:** Skeuomorphic-quote (chrome-on-black gloss) on a Big-Sur-shape squircle · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 256×256 — downsized web render, SHA-1 56d30115) · **Category:** Utility (Quick Look file renderer/previewer)

| Dimension | Reading |
|---|---|
| Background | Vertical ramp `#313130` (top) → `#000000` (bottom) — near-black charcoal-to-black, sky-logic top-lit (measured) |
| Glyph | Abstract: 5 nested concentric semicircular arcs (a "rainbow" / spectrum), polished chrome. Per-band ramp `#6A6A6A` (lower shadow edge) → `#FFFFFF` (specular crest), mid ~`#BABABA`–`#C4C4C4`. Sits upper-centre, occupying roughly the top two-thirds (measured) |
| Overlay device | None |
| Light model | Top-down. Each arc band carries a baked white specular crest along its top edge fading to grey below — cylindrical/tubular chrome shading. Background also lighter at top. No cast/drop shadow grounding the glyph. Specular is **baked into the art**, not system-applied (estimated) |
| Layer stack | back → front: (1) near-black vertical ramp field · (2) nested chrome arc bands with baked per-band highlights. 2 planes, no tool overlay |
| Palette economy | Achromatic — 0 hue families. Neutral chrome glyph on a black ramp; no saturated accent. A "rainbow" rendered in monochrome — witty, and coherent with the strictly black-and-white cover/brand |

## Signature devices
- **The monochrome chrome rainbow** — a rainbow (spectrum = "renders every file type") drawn as nested concentric arcs but stripped of all colour and cast in polished metal. Subject-mining the QuickLook "preview anything" promise, then deliberately de-saturating it to match a black-and-white brand. `[GOLDEN-NUGGET]`
- **Per-band tubular specular** — each of the 5 arcs reads as a rounded chrome tube via a white crest → grey belly gradient; the light discipline is consistent across all bands.
- **Tenebrous ramp** — glyph legibility is carried entirely by the near-black background; the icon is a high-contrast silver-on-black plate.

## Failures
- **#4 16px squint test** — 5 nested arcs at ~256px means each band+gap is ~10px, i.e. sub-pixel at 16px; the concentric bands merge into a single grey dome and the whole point (the layered rainbow) smears away. This is the classic thin-concentric-line death at Dock/Spotlight size.
- **#10 variant robustness** — composition is baked black-background-dependent and self-lit (baked chrome specular + baked ramp). Not authored as Icon Composer layers; would not survive a tinted/clear render, and the top-lit gloss fights the system's own dynamic effects. Not a Liquid Glass icon by construction.

## Soft passes (flagged, scored as passes)
- **#1 mask discipline** — respects the squircle, but the asset is delivered pre-masked (transparent corners baked into the 256px web render) rather than a full-bleed 1024 square; can't verify true edge behaviour.
- **#2 grid adherence** — horizontally centred and clean, but the arc mass sits high (upper two-thirds), leaving the lower third of the squircle empty; optically top-weighted rather than grid-centred.
- **#8 depth coherence** — bands are internally coherent, but the glyph floats with no grounding shadow, so it reads as a printed plate rather than a stacked object.
- **#9 era coherence** — a modern Big-Sur-shape squircle wrapped around baked skeuomorphic chrome-gloss lighting; the mix is deliberate (a quotation) but it is a mix — both Big Sur and Liquid Glass HIG say not to bake specular/gloss.

## Rhymes with
- Dark-chrome skeuomorphic **utility** icons: polished-metal-on-black marks in the pro-audio / Quicksilver / spectrum-analyser lineage. Style family: monochrome chrome glyph, tenebrous ramp, baked top specular, no hue. (Sole member so far — hint only, no cluster yet.)
