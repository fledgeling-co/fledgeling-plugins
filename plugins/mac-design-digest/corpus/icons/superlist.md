# Icon: Superlist

- **Era:** Big Sur unified (monochrome sculptural-relief variant) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, actually AVIF, 513×512 web render — mask + drop-shadow baked, transparent corners). Category: Productivity ("Tasks, notes, and plans.").

| Dimension | Reading |
|---|---|
| Background | Ramp (single-material) — no separate field; the whole tile is one red surface, `#FB6343` highlight → `#E64427` body → `#BD0D05` deep fold `(measured)` |
| Glyph | Monogram doubling as object — the letter **S** rendered as a curled sheet of paper (a "list page" rolling over itself); full-bleed, optically fills the canvas |
| Overlay device | None — the fold *is* the subject, not a tool laid over a background |
| Light model | Top-down, slight top-left soft key; short soft self-shadows pooling in the folds; faint highlight rim on the lifted paper edges; matte, **no specular gloss** |
| Layer stack | Red field plane (back) → curled S-ribbon mid-fold → lifted paper edge + cast shadow (front) → baked squircle drop-shadow (web-render artifact, below tile) |
| Palette economy | One hue family (warm red-orange), tonal ramp only, zero competing accent — exemplary economy |

## Signature devices
- **Monochrome sculptural relief** — figure and ground are the *same* material. The mark exists purely as baked light-and-shadow on one continuous red surface; there is no hue or flat-shape separation between "glyph" and "background." `[GOLDEN-NUGGET]`
- **Folded-paper logomark** — the brand S read as a sheet of paper (a list) curling over itself; the object metaphor and the letterform are the same shape.
- **Full-bleed field** — breaks the classic Big Sur "colored background field + centered glyph/diagonal tool" composition; the logomark occupies the entire tile edge-to-edge, so the icon reads as a solid saturated red chip in the Dock with a sculpted swoosh.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black, the icon is a featureless squircle: the S vanishes because it is carried entirely by tonal relief, not by figure-ground shape. The subject is not nameable from silhouette alone. This is the icon's central risk and the price of the monochrome-relief choice.

## Soft passes (flagged for synthesis)
- **#4 16px squint — soft pass.** At menu-bar/Spotlight size the curl reads as a lighter diagonal swoosh; the specific "S"/list letterform does not crisply resolve. The distinctive saturated red is the stronger ID anchor at that size, not the mark.
- **#7 Figure-ground contrast — soft pass.** Survives grayscale via shadow modeling (fold `#BD0D05` vs highlight `#FB6343`), but there is essentially no glyph-vs-background contrast in the classic sense — they are one material. Legibility rests wholly on the shadow render.
- **#10 Variant robustness — soft pass (era-appropriate; noted).** Not a Liquid Glass icon, so strictly N/A — but because the S is tonal-only, a mono or tinted-appearance render would flatten the relief and lose the letterform. The mark depends on the red gradient existing.

## Passes worth naming
- **#5 Single light model, #6 Palette economy, #8 Depth coherence, #9 Era coherence** all clean. The depth logic (paper lifts, casts a short shadow onto the field below, curls back) is the entire icon and it is internally consistent — no z-fighting, one light, one hue.
- **#11 Personality** — strong, nameable, non-template device (monochrome sculptural brand-mark).
- **#1/#2/#12** pass: mask-native (transparent corners, no corner-radius fight), optically centred full-bleed, no words/screenshots/photos.

## Rhymes with
- **Monochrome sculptural brand-mark family** — single-hue matte logomarks modeled by baked self-shadow rather than by a background/glyph split. The opposite pole from the classic Big Sur "field + diagonal tool" tradition (TextEdit/Preview).
- Consumer-productivity marks that lead with one saturated identity color as the Dock anchor (warm-red chip). Brand-context note: the Superlist *app* UI is dark-purple/indigo (see cover) — the red icon is the warm pop against an otherwise cool product, so the icon is doing brand-identity duty more than subject-communication duty ("tasks/notes" is not depicted; the S is).

## Provenance caveats
- 513×512 AVIF→PNG web render; mask and drop-shadow are pre-baked and corners are transparent, so edge crispness and micro-shadow softness are partly resize/compression artifacts. The true 1024 source is likely cleaner and may carry finer fold shading. Cover render agrees with the standalone icon (pure monochrome red, no secondary tone) — the earlier apparent navy underside was the dark cover background behind the squircle corners.
