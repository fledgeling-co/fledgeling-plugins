# Icon: Toplify

- **Era:** Big Sur unified (dark-field, front-facing glyph, top-down light — **not** Liquid Glass) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply icon.webp, 386×386 (resized web render — see caveats) · **Category:** Marketing · **App does:** tracks App Store ranking positions and pushes notifications.

| Dimension | Reading |
|---|---|
| Background | Near-black vertical ramp #1F1F1F → #0F0F0F (top→bottom, subtle sky-logic within near-black) (measured)(inferred) |
| Glyph | Abstract "burst + rising-arrow" symbol; silver vertical gradient #FFFFFF (top ray) → #DADADA (mid rays) → #8D8D8D (arrow foot). Optically centred, mass sits ~52% vertical — the up-arrow tail adds slight bottom weight. |
| Overlay device | None — the arrow is fused *into* the glyph, not a separate tool/badge/frame overlay. |
| Light model | Single top-down. Glyph gradient reads as light raking a brushed-silver mark (white crown → graphite foot). Short soft baked drop-shadow beneath each stroke = embossed relief on a flat field. No specular glass, no refraction. |
| Layer stack | back → front: (1) dark ramp field · (2) baked soft drop-shadow · (3) silver-gradient glyph (radial burst rays + upward chevron-arrow). |
| Palette economy | Achromatic — 0 hue families. Black field + white/silver glyph. **Accent: none.** Passes economy trivially; the cost is stated under Failures/Notes (brand green is absent). |

## Signature devices

- **Burst-with-rising-arrow fusion glyph** `[GOLDEN-NUGGET]` — a radial spark (vertical + two diagonal + two horizontal rays) whose *lower* rays are deliberately replaced by an upward chevron-arrow with a stem. It fuses two metaphors into one mark: emphasis/notification (the spark) + climbing to the top (the arrow). This is genuine subject-mining — App Store rank tracking = "rising to #1." The one committed, non-template decision in the icon.
- **Metallic vertical gradient on the glyph** — white at the top ray fading to graphite at the arrow foot, so the mark reads as brushed silver under a top light rather than flat fill. Cheap, effective depth signal.
- **Near-black background ramp** — #1F1F1F→#0F0F0F rather than a single flat black; keeps the field from looking like a cut-out sticker.

## Failures

- **#4 16px squint test — FAIL.** At menu-bar/Spotlight size the separated rays close their gaps and merge into a bright blob; the up-arrow metaphor is lost and the mark smears (verified by LANCZOS downscale to 16px). It survives at 32px but not at 16px — the exact sizes where Dock/Spotlight/menu-bar duty lives. The composition's legibility depends on the gaps between thin strokes, which are the first thing to die on downscale.
- **#10 Variant robustness (current era) — FAIL.** Authored as a fixed Big Sur-era flat asset, not as Icon Composer layers. It bakes in its own black field, glyph gradient, and drop-shadow — all of which HIG says the *system* should apply in the Liquid Glass era, and which conflict with system dynamic effects. The white/silver glyph is also figure-ground-dependent on the self-supplied black field: on a clear/light-tinted render it would wash out. Would not survive dark/clear/tinted variants gracefully without a rebuild.

### Soft passes (flagged, scored as passes)
- **#2 Grid** — optically centred, but the arrow tail pulls visual mass slightly below true centre; a nudge up would balance the burst crown against the arrow foot.
- **#3 Silhouette** — nameable, but as a *dual* metaphor (spark + arrow) it is a beat slower to read than a single-anchor glyph; filled solid black it could read as sun / compass / asterisk before "trending up."

## Rhymes with

- **Dark-field monochrome line-glyph utility icons** — black/near-black squircle + a single silver or white geometric mark, no accent hue. Style family of developer/analytics/terminal tools that want to read "precise, technical, no-nonsense." (First member of this family in the corpus — promotion pending ≥2 more.)

## Notes for synthesis

- **Resolution caveat:** 386×386 web render, not a 1024 master. Gradient banding, edge softness, and the pure-black corners are render/flatten artifacts — the corners reading #000000 (vs the #1F–#0F interior) suggest the squircle mask is baked into this web export, so **#1 mask discipline can't be fully verified** from this file (scored a pass on the visible evidence: clean squircle, glyph well inside the safe zone, no corner-radius fight).
- **Palette-coherence gap (icon vs brand):** the cover brand runs a saturated green (stat text ~#04A547, Dock indicator ~#00D957) as its identity accent; the icon carries **zero green** — it is pure monochrome. Icon and app disagree on palette. The icon communicates "up/ranking" only through the arrow, not through any brand-linking colour; a brand-green focal detail on the arrowhead would tie them together and give the 16px form a colour anchor.
- **Era note:** a textbook Big Sur-era dark utility icon that has not been re-authored for macOS 26 Liquid Glass. Both failures (#4, #10) trace to the same root: a flat, thin-stroke, self-contained composition rather than a layered, robust one.
