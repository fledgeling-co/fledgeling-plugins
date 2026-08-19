# Icon: Cachesweep

- **Era:** Big Sur unified (glyph-on-gradient) — not Liquid Glass, despite shipping on macOS 15+/Tahoe · **Rubric:** 12/12 (5 soft passes, 0 hard failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp`, 256×256 web render (squircle mask + soft drop-shadow baked in; corners transparent). Full-bleed 1024 master **not seen**; treat mask/shadow as the site's render, not verified ship layers.
- **Subject:** menu-bar disk/cache cleaner ("shows you what's eating your space — live").

| Dimension | Reading |
|---|---|
| Background | Diagonal ramp `#89A0F6` (top-left, light) → `#2A3AAD` (bottom-right, dark), midtone `#4053C8` — single indigo/royal-blue hue family (~hue 232), light-at-top-left "sky logic" run along the same diagonal the glyph travels |
| Glyph | Abstract — three white `#FCFEFF` four-pointed concave-sided sparkles (the SF Symbol `sparkles`). Size cascade small (top-center) → medium (upper-left) → large (center-right, low). Optical anchor = the large sparkle, sitting below and right of geometric centre |
| Overlay device | None (no diagonal tool, badge, or frame) |
| Light model | Flat frontal. Gradient supplies a soft top-left→bottom-right luminance sweep, but the glyph is **unlit flat white with no cast/inner shadow** — flatter than the Big Sur era's baked-micro-shadow convention it otherwise quotes |
| Layer stack | back → front: [1] blue diagonal gradient field · [2] three flat white sparkle glyphs. (Render adds baked squircle mask + soft drop shadow outside the artwork.) |
| Palette economy | Exemplary: 1 hue family + white glyph, zero accent. Glyph carries the only bright value |

## Signature devices
- **Sparkle cluster (`sparkles` SF Symbol), size-cascaded along the ramp diagonal** — small→medium→large echoes the top-left→bottom-right light-to-dark sweep, so glyph motion and gradient motion agree. This diagonal rhyme is the one composed decision in an otherwise stock icon `[GOLDEN-NUGGET, minor]`.
- **Monochrome-blue + white restraint** — no second hue, no accent; the whole icon is one ramp and one white mark. Clean, but it is also what makes it interchangeable with a hundred other indigo utility icons.

## Failures
- None hard. **Five soft passes** (score never travels without this asterisk):
  - **#2 Grid** — cluster is bottom-right-heavy; the large-sparkle anchor sits below/right of optical centre. Reads as a deliberate diagonal but weights the icon low; at Dock size it looks slightly bottom-heavy.
  - **#4 16px squint** — the two small sparkles smear into indistinct specks at menu-bar/Spotlight size; only the large sparkle survives. Icon still reads as "a sparkle," so it functions, but the intended three-star composition collapses to one-plus-noise.
  - **#8 Depth** — coherent but very flat; no micro-shadow under the glyph, so it wears the Big Sur squircle+gradient while skipping Big Sur's depth. A mild internal tension, not a defect.
  - **#10 Variant robustness** — no evidence of authored Icon-Composer dark/clear/tinted layers; it is a single flat masked bitmap. The clean silhouette *would* tint/mono-reduce gracefully, but appearance variants are unverified.
  - **#11 Personality** — the central weakness. The device is *precisely* the "generic glyph-on-gradient" the rubric warns about, using the most over-used symbol in the store (`sparkles` = the universal AI/magic/clean mark). It is nameable but not distinctive, and it communicates **"clean/magic," not "disk/cache/sweep."** A broom, dustpan, disk-with-shine, or gauge would have mined the subject; sparkles is category-blind. Passes per the rubric's "absence-of-device is not a failure" rule, but this is why the icon reads as template.

## Rhymes with
- The broad **Big Sur glyph-on-indigo-gradient utility** family: stock AI-assistant icons, cleaner utilities that reach for sparkle/broom "freshness" motifs (CleanMyMac-adjacent register), and the crowd of periwinkle→royal productivity squircles. No digested peers yet — first icon in the corpus; log as the seed of a probable **"indigo utility, SF-Symbol-on-ramp"** icon cluster once ≥2 more arrive.
- Palette coherence with the app: cover shows the same blue family (indigo wallpaper, `#0A84FF`-class "Clean Selected" CTA, blue menu-bar glyph) — icon↔UI hue are one system, a genuine (if monochrome) brand discipline.
