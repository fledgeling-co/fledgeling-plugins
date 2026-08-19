# Icon: Notion

- **Era:** custom (brand logomark, era-agnostic — flat-transition adjacency) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/notion/icon.png`, 1024×1024, alpha) · **Category:** Productivity
- **Provenance caveat:** the delivered asset is the **transparent brand logomark**, not the shipping macOS Dock render. The actual Notion.app icon composites this black cube onto a solid **white squircle field**; macapp.supply served the field-less web mark. Rubric below scores the composed shipping design where the field matters, and flags every place the raw asset diverges. Art is clean vector (alpha histogram bimodal 0/255, thin AA fringe) — no resolution smear.

| Dimension | Reading |
|---|---|
| Background | flat — transparent as delivered; **#FFFFFF** field when composed as the app icon (measured) |
| Glyph | object+monogram hybrid — isometric 3D block bearing a serif capital **N**; pure **#000000** on **#FFFFFF** (measured). Optically centered horizontally (content bbox x 18→1006, center ~512); **full vertical bleed (y 0→1024)** — no safe-zone margin as a raw asset |
| Overlay device | none (no diagonal tool/badge). A recessed rounded-rect white "label plate" frames the N inside the front face |
| Light model | Flat / 2.5D axonometric — **no modeled light source**. The left face is a flat solid-black tonal plane (not a cast shadow); top + front faces white. No gradient, no specular, no baked drop shadow |
| Layer stack | (white field, when composed) → black isometric cube shell + left/dark face → white top face (parallelogram, black keyline) → white front panel (rounded-rect, black keyline) → black serif "N" monogram |
| Palette economy | Achromatic — **zero hue families**, black + white only, no accent. Maximal figure-ground (21:1) |

## Signature devices
- **The "N-block":** a serif capital N seated on the front face of an isometric notebook-block — an object-monogram hybrid that literally draws "a block of notes." Notion's product primitive (the block) rendered as its mark. `[GOLDEN-NUGGET]`
- **Monochrome-only identity:** the mark carries zero color; brand accent (cornflower blue, seen in the cover's "Think" pill) lives only in UI chrome, never in the logo. An austere, ink-on-paper posture rare among Productivity icons that reach for gradient squircles.
- **Isometric projection instead of front-facing:** breaks the Big Sur "front plane + diagonal tool" convention entirely; depth is pure axonometric geometry.
- **Keyline-as-depth-system:** one chunky uniform black outline does all the structural work — line-art weight, not shading or bevel.
- **Serif letterform in a geometric shell:** a bookish, editorial N (bracketed serifs, tapered strokes) inside a hard geometric block — the whole warmth/coolness contrast in one decision.

## Failures
- **#10 Variant robustness (Liquid Glass era) — FAIL.** The mark is black keylines + black left-face on a white-dependent field. In dark/tinted/clear renders the black shell and rim collapse into a dark background; the design has no baked dark or tinted variant and depends entirely on a light ground. (Notion ships an inverted mark separately, but this asset is single-appearance.)

### Soft passes (flagged, scored as pass)
- **#1 Mask discipline** — composes cleanly and centered onto a white squircle, but **delivered field-less**; dropped raw into an .icns it would read as a floating cube fighting the Dock's uniform squircle grid.
- **#2 Grid adherence** — optically centered on the horizontal, but **bleeds to y=0 and y=1024** with no safe-zone margin; relies on the compositing step to inset it.
- **#3 Silhouette** — the outer form reads as "a block/cube" filled solid black, but the identity-carrying N and white faces are negative space that **vanish in a true solid silhouette**; identity is figure-ground dependent, not silhouette-dependent.
- **#5 Single light model** — passes by having *no* modeled light (flat isometric); internally consistent, but offers none of the era's specular/refraction cues.
- **#9 Era coherence** — internally consistent flat mark, but **era-detached** from macOS: not a Big Sur squircle, not Liquid Glass. A brand-first logomark that ignores platform icon language.
- **#12 No-text** — a single-letter serif monogram with strong shape logic (acceptable per icon-anatomy monogram rule), not a word or screenshot.

## Rhymes with
- **Monochrome monogram/logomark family** — letter-forward brand marks that rely on a white field and ignore macOS era conventions (favicon-class marks promoted to app icons). No corpus peers yet.
- **Isometric-object marks** — logos built from an axonometric 3D primitive rather than a front-facing glyph. Distinct from the Big Sur diagonal-tool squircle family (Preview/TextEdit lineage) and the Liquid Glass layered-glass family.
- Nearest *contrast*: any Productivity icon that adopts the platform's gradient squircle + baked lighting — Notion deliberately refuses both.
