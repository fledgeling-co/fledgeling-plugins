# Icon: Liqoria

- **Era:** skeuomorphic-quote (glossy glass-orb) framed in a Big-Sur squircle — under-committed hybrid · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.webp, 204×204 web render — small; all pixel values `(estimated)` at this scale, pre-masked squircle with transparent corners)
- **App:** "Liqoria — Mac Music Player • Apple Music • Spotify • YouTube and more" (Lifestyle)

| Dimension | Reading |
|---|---|
| Background | Ramp #DCDCDC → #B7B7B7 (light gray, near-white top → mid-gray base), subtle top-down/vertical `(estimated)` |
| Glyph | Object + abstract: a **charcoal play triangle** (#222222, rounded corners) sitting on a **pearlescent glass orb** (grays #A6→#C9). Orb optically centred, glyph centred on orb `(estimated)` |
| Overlay device | None (no diagonal tool/badge/frame) — the orb *is* the whole composition |
| Light model | Top-down, single source. Background lighter at top; orb carries a baked specular highlight near its crown fading to mid-gray at base; weak contact grounding `(estimated)` |
| Layer stack | back → front: light-gray squircle field (top-down ramp) · glossy pearlescent glass sphere (baked specular + soft lower reflection) · charcoal rounded play triangle |
| Palette economy | Zero hue families — fully monochrome/grayscale. No saturated accent anywhere; the "accent" role is filled only by the dark glyph's tonal contrast |

## Signature devices
- **Play button as a glossy glass bubble** — the play triangle is embedded in a 3D pearlescent orb rather than drawn flat. This is the icon's one nameable move, but it's a stock glossy-button trope (Aqua/early-iOS glass lineage), i.e. **template-default**, not a subject-mined or committed direction.
- **Monochrome discipline taken to zero-chroma** — the entire icon is grayscale. Distinctive in a category of colourful music icons, but it reads as absence-of-choice rather than a committed grayscale identity, and it does not connect to the app's actual colourful Liquid-Glass UI.

## Failures
- **#9 Era coherence (FAIL):** one skeuomorphic baked-gloss orb dropped into an otherwise era-neutral flat Big-Sur squircle. It commits to neither language — no rich skeuomorphic texture elsewhere, yet a glossy 3D bubble that a clean Big-Sur/Liquid-Glass icon would never bake. Reads as under-committed, not a deliberate quotation.
- **#10 Variant robustness (FAIL):** baked single-appearance PNG, not a layered Icon Composer icon. The light-gray field + dark-charcoal glyph would not adapt to dark/clear/tinted modes — glyph legibility depends entirely on the light orb behind it; on a dark Dock it would glare as a light slab.

## Soft passes (flagged)
- **#1 Mask discipline:** fills the squircle silhouette correctly, but ships **pre-masked with baked specular gloss** — the shape and the glass effect that macOS 26 wants to own itself are painted in. Passes on silhouette, flagged on pipeline.
- **#4 16px squint:** the charcoal play triangle survives to menu-bar size, so it reads "play." But the orb (~#B0) sits at ~1.1:1 against the field (~#BC), so the entire 3D bubble **dissolves into the background** at small sizes — you're left with a triangle on gray. Glyph carries it; the device does not.
- **#7 Figure-ground:** glyph-vs-orb contrast is strong (#222 on #B0). Orb-vs-field contrast is **<3:1 (~1.1:1)** — the primary depth element barely separates from its own background. Passes on the glyph, fails on the device.
- **#8 Depth coherence:** layer order and top-down lighting are consistent, but the orb's near-zero field contrast and weak grounding collapse the depth illusion at anything below hero size.
- **#11 Personality:** a device exists (glass-bubble play button) but it's a generic gloss trope — `template-default` in aesthetic-direction terms, not a committed or subject-mined choice.

## Rhymes with
- The generic **"glossy orb + play triangle" media-player family** — default music/podcast icons that lean on an Aqua-glass bubble rather than a designed subject.
- Skeuomorphic **glossy-glass-button quotations** (pre-Yosemite Aqua lozenge/orb material) transplanted into a modern squircle without the surrounding texture that would justify them.
- *(Hint only — synthesis owns cluster assignment.)*

## Cross-icon notes for synthesis
- **Palette/brand incoherence:** the app cover is saturated Liquid Glass — a translucent floating media widget on a pink/purple floral wallpaper. The icon is fully grayscale. The icon communicates neither "music" beyond the play glyph nor the product's actual colour world; icon↔cover palette coherence fails.
- **Resolution caveat:** 204×204 source; specular/edge nuance and any faint chroma cast (orb edges read within ±3 of neutral) are below reliable measurement — treat all hexes as `(estimated)`.
