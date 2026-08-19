# Icon: Atlas

- **Era:** custom (flat monochrome brand-mark, era-agnostic) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — 400×400 JPEG web render (not the 1024 master); values `(estimated)` from this render
- **App:** "Native, local, and blazing fast inspiration library for macOS" (Productivity) — a local moodboard / reference organizer

A logo-on-black treatment, not a native icon composition: a single white six-point asterisk/spark glyph on a near-black ground. It forgoes the entire Big Sur / Liquid Glass craft vocabulary (no dimensional light, no layered glass, no baked micro-shadow) in favour of a flat, emblematic wordmark-glyph. That flatness is the whole personality — and its one real liability (variant robustness).

| Dimension | Reading |
|---|---|
| Background | ramp #000000 → subtle center lift ~#201B21 (`estimated`) — a whisper of a purple-tinted radial/diagonal vignette over near-black; reads as near-flat black at any glance |
| Glyph | abstract six-point asterisk / sparkle mark, pure #FFFFFF fill, optically centred (~55–60% of canvas width), no interior shading; the negative-space wedges between the six arms carry as much of the read as the arms |
| Overlay device | none |
| Light model | flat — no directional source, no specular, no baked shadow on the glyph; only tonal variation is the faint background vignette. A single (null) light model, internally consistent but dimensionless |
| Layer stack | back → front: (1) near-black vignette field, (2) white asterisk glyph. Two planes, no tool overlay |
| Palette economy | monochrome — achromatic white glyph on achromatic near-black + an almost-imperceptible purple tint in the vignette lift; accent: none; the white glyph is the sole focal |

## Signature devices
- **Six-point asterisk / spark mark** — the "spark of inspiration," and doubly apt for a *reference* library, an asterisk being the footnote/reference marker itself. `[GOLDEN-NUGGET]` the glyph's meaning is subject-mined, not decorative.
- **Logo-on-near-black treatment** — a wordless brand glyph dropped onto black, used verbatim as the app icon. Startup/AI-tool idiom rather than mac-native icon idiom.
- **Negative-space radial burst** — the six arms are separated by hard black wedges; the silhouette is built as much from the gaps as the strokes.

## Failures
- **#10 Variant robustness (FAIL):** the black background is baked into a flat raster; there is no separable glyph layer for the system to tint. A white glyph depends entirely on the dark ground for its ~20:1 contrast — on a light/tinted/clear system render it would collapse to invisible. Not authored as layered Icon Composer art (as delivered here). *Caveat: only the flat web render was seen; the shipping app may ship a proper layered asset macapp.supply flattened.*

## Soft passes (flagged for synthesis)
- **#2 Grid:** looks optically centred, but pixel-precise grid adherence can't be verified on a 400px render — `(estimated)`.
- **#4 16px squint:** survives as a fuzzy radial star/spark, but the six-arm count and the crisp negative-space wedges smear together; identity holds as "a burst," count is lost.
- **#5 Light model / #8 Depth:** consistent because there is nothing to be inconsistent *with* — the icon is dimensionless. Passes the "single light model" letter of the check while forgoing the native soft-top-down / environmental-glass depth entirely.

## Rhymes with
- Flat monochrome logo-mark icons — a wordless brand glyph centred on a near-black ground. Style family: modern-startup / AI-tool minimalist marks (Vercel-class monochrome logos, sparkle/asterisk brand glyphs). Candidate seed for an icon cluster "flat monochrome logo-mark on near-black" — needs ≥3 independent icons to promote to ICONS.md canon.
