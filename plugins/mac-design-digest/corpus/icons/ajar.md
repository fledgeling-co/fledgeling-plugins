# Icon: Ajar

- **Era:** Liquid Glass (Big-Sur-adjacent) · **Rubric:** 12/12 (4 soft passes, 0 failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply / user · **Subject:** Utility — "Lid Angle Sync & Keep Awake for AI Agents on Mac"
- **Resolution caveat:** 256×256 PNG, a downsized web render (Apple masters at 1024). Value ramps and the specular rim read cleanly at this size; 16px degradation and true per-layer glass effects are **extrapolated, not verified**. The squircle mask is baked into the file's alpha (pre-masked corners are transparent) — so the full-bleed square source layers cannot be confirmed, only that the composition respects the mask.

| Dimension | Reading |
|---|---|
| Background | Vertical ramp `#6864F6` (top) → `#534CD3` (bottom) `(measured)` — single indigo/periwinkle hue (~248°), sky-logic light-at-top |
| Glyph | Rounded-corner **wedge/triangle**, translucent lavender glass; own top-down ramp `#EAE9FD` apex → `#A39FE8` base `(measured)`; optically centred horizontally, mass sits low-third (base ~78% down) — correct optical weighting for a base-heavy shape |
| Overlay device | None (no diagonal tool / badge / frame) — the glyph *is* the subject |
| Light model | Top-down, soft. Both field and wedge ramp light→dark vertically (one coherent source). Short, subtle contact shadow beneath the wedge's base; **specular rim-light** along the wedge's curved lower edge (glass refraction keel) + apex sheen |
| Layer stack | 1) indigo squircle field (ramp) → 2) contact shadow under wedge base → 3) translucent lavender glass wedge (own ramp) → 4) specular edge-highlight on wedge's lower curve + apex |
| Palette economy | **Monochromatic** — one hue family, glyph is a lighter *value* of the field. No second hue, no saturated accent. Exemplary economy |

## Signature devices
- **Wedge-as-lid-ajar** `[GOLDEN-NUGGET]` — the rounded triangle is a laptop viewed in side profile with the lid open at an angle: the literal subject (the app reads lid angle). "Ajar" made geometric.
- **Double-read glyph** — the same wedge is an upward arrow / mountain, i.e. "light rises with the lid" (the brightness-sync function). One shape, two true meanings, no clutter.
- **Curved-belly base with specular keel** — not a flat triangle base; the bottom is a convex curve carrying a near-white refraction rim, which is what pushes the reading from Big-Sur opaque-object toward Liquid-Glass translucent-slab.
- **Single-hue tint system** — the glyph is defined by *luminance* against the field, not by a contrasting hue; the whole icon lives in one periwinkle-indigo column.

## Failures
- None outright. **Soft passes** (pass, but flagged for synthesis):
  - **#9 Era coherence** — classified Liquid Glass, but a single glyph on a vertical gradient is equally a **Big Sur** trope. The glass reading rests on two modest tells (wedge tinting toward the field at its base = translucency; specular rim on the lower curve), both extrapolated at 256px. Recorded liquid-glass with big-sur as the honest adjacent reading.
  - **#10 Variant robustness** — because the composition is *entirely one hue*, dark/clear/tinted survival is **inferred, not verified**. The glyph is luminance-defined (light wedge on dark field), which is the property that *should* carry into tinted renders — but with no layered source, a tinted-mode contrast collapse can't be ruled out.
  - **#2 Grid** — mass is base-heavy and sits in the lower third; reads optically centred because the wide base anchors it, but it is not geometrically centred.
  - **#4 16px squint** — core wedge holds and stays nameable; the specular rim and contact shadow are lost by menu-bar size (they don't need to survive — the silhouette carries it).

## Rhymes with
- Single-glyph-on-single-hue-gradient utility icons; the periwinkle/indigo glass-wedge family; Big-Sur-descended minimalist geometric-glyph icons that quote one abstract shape rather than a literal tool. (Hint only — no ≥3-icon cluster yet; first member on record.)

## Cross-icon / brand notes
- **Palette coherence with cover:** the cover is Swiss-minimal (white ground, black/gray SF-bold headlines, black pill CTA); the icon's indigo squircle is the **only colour on the whole sheet**. Brand = periwinkle-indigo deployed as jewelry against monochrome. The icon carries the entire brand hue — strong coherence.
