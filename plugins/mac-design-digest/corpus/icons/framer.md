# Icon: Framer

- **Era:** Big Sur unified (with a skeuomorphic chrome material-quote) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, 102×102 web render — see resolution caveat) · **Category:** Design (AI website builder)
- **Subject fit:** the icon *is* the Framer logomark — brand-literal. It communicates "Framer the brand," not "website builder the task"; a naive viewer reads an abstract angular F, not the product's job. Acceptable for a strong-brand app, but the subject (site-building) is absent by choice.

| Dimension | Reading |
|---|---|
| Background | ramp #383838 (top) → #151515 (bottom), true corner ~#131313 — neutral/achromatic, top-lit (sky logic) `(measured)` |
| Glyph | monogram — the Framer "F" (two offset folded angular bands), chrome/silver ramp #EFEFEF → #C6C6C6 → #484848, optically centred, fills inner safe zone `(measured)` |
| Overlay device | none |
| Light model | top-down; background and glyph both brighten toward the top; brushed-metal specular banding on the upper facets; no baked drop shadow (system-applied); **no glass refraction/translucency** |
| Layer stack | back→front: (1) near-black squircle field with top-lit neutral ramp; (2) chrome/metallic F logomark with its own top-lit silver ramp. Two opaque planes. Possible faint baked top rim-light on the mask edge — unconfirmable at 102px |
| Palette economy | **zero hue families** — fully achromatic. Two greyscale ramps (dark field + chrome glyph). Accent: none. Maximally economical |

## Signature devices
- **[GOLDEN-NUGGET] Chrome/brushed-metal material quote.** The mark is rendered as reflective silver metal — bright specular top facets falling to dark grey — a skeuomorphic material laid over Big Sur front-facing grammar. This is the icon's entire personality in one decision: the brand's flat white F (see cover) reinterpreted as machined metal.
- **Monochrome brand discipline.** Not one pixel of hue. Contrast and metal do all the work; the icon would look identical in a colourblind or grayscale render because it already *is* grayscale.
- **Logomark-as-glyph.** The geometric Framer F used directly as the icon subject — no additional metaphor, no tool overlay. Confident when the brand mark is this recognizable; mute when it isn't.

## Failures
- **#10 Variant robustness (Liquid Glass era) — FAIL.** Not authored as Icon Composer glass layers. The composition depends on the baked near-black background for figure-ground; there is no distinct translucent foreground the system could recomposite. In tinted/clear modes there is no colour to tint and no glass to refract; in a "clear" render the achromatic F would lose its ground. For a current-macOS (Tahoe / Liquid Glass) shipping icon this is the honest era-lag.

## Soft passes (flagged, scored as pass)
- **#1 Mask discipline.** Artwork sits inside the safe zone and doesn't fight the squircle, but there is a possible faint baked top rim-light/bevel on the mask edge — HIG says leave specular/edge effects to the system. Cannot confirm vs. compression at 102px.
- **#4 16px squint test.** The bright upper bands of the F carry the mark down to menu-bar size, but the lower band darkens to ~#484848 and starts to dissolve into the field — the bottom of the glyph is where small-size legibility frays.
- **#7 Figure-ground contrast.** Upper glyph vs. field ≈ 11:1 (excellent); lower band (~#484848) vs. field (~#151515) ≈ 2:1, below the 3:1 floor *locally*. The mark as a whole still reads, so it's a soft pass, but the dark-bottom-of-glyph is the one measurable weak point.

## Rubric ledger
| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Mask discipline | soft pass | inside safe zone; possible faint baked top rim-light (unconfirmed at 102px) |
| 2 | Grid adherence | pass | F optically centred, balanced margins, fills inner square |
| 3 | Silhouette test | pass | two offset angular bands read as an F / the Framer mark, filled solid |
| 4 | 16px squint | soft pass | bright upper bands survive; lower band darkens toward the field |
| 5 | Single light model | pass | one top-down source across field and glyph |
| 6 | Palette economy | pass | achromatic, two greyscale ramps, no competing hues |
| 7 | Figure-ground | soft pass | 11:1 upper, ~2:1 lower band — below floor locally |
| 8 | Depth coherence | pass | single raised metal plane, shadows consistent with top light, no z-fighting |
| 9 | Era coherence | pass | Big Sur grammar throughout; the chrome is a deliberate, consistent material-quote |
| 10 | Variant robustness | **FAIL** | not glass-layered; depends on baked dark ground; no tinted/clear/dark system variants |
| 11 | Personality | pass | the brushed-chrome material quote is a nameable distinctive device |
| 12 | No-text check | pass | logomark, not lettering; no UI/photo elements |

## Rhymes with
- Dark achromatic pro-tool / **chrome-monogram-on-black** family: icons that render a brand logomark as machined metal on a near-black top-lit field (metallic wordmark utilities, dark-mode dev-tool marks). *Hint only — no other icon digested yet to confirm the cluster.*

## Notes for synthesis
- **Resolution caveat:** subject is a 102×102 web `webp`, not a 1024 master. Fine specular detail, the exact mask corner-continuity, and any real edge bevel are below the confidence floor — all glyph/field hex values are `(measured)` off the small render and should be treated as ±. Do not promote pixel-exact values.
- **Possibly not the official shipping icon.** Framer's brand mark (see `cover.png`) ships as a *flat pure-white* F on black; this metallic chrome reinterpretation may be a community/store render rather than Framer's Icon-Composer master. Flag before treating as canonical Framer.
- **Palette coherence with cover:** strong — both are strict black/white/achromatic. The icon's only addition over the brand is metal.
- **Era-lag signal:** a monochrome-metal Big Sur composition shipping into the Liquid Glass era. If ≥2 more digested icons show the same "chrome monogram on black" move, that's an icon-cluster candidate; a single achromatic-metal icon promotes nothing.
