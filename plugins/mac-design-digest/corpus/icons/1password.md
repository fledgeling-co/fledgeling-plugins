# Icon: 1Password

- **Era:** Big Sur unified (front-facing squircle, matte material, baked micro-shadow — **not** Liquid Glass) · **Rubric:** 12/12 (3 soft passes) · **Digested:** 2026-07-19
- **Source:** macapp.supply web render, `icon.webp` 102×102px — a small resized render, not a 1024 master. Fine specular/glass detail (if any) would be flattened at this size; readings below are honest to what 102px shows.

| Dimension | Reading |
|---|---|
| Background | Ramp — cool silver/aluminium field, `#C5CAD6` (top) → `#A6B1C2` (mid-edge), lighter at top with a faint inward edge vignette (estimated) |
| Glyph | Abstract **vault-dial / keyhole** — concentric electric-blue ring around a near-white inner disc `#EAEEFD`, centred navy keyhole "1" `#16192F`. Optically dead-centre on the canvas, sits on the grid's large circle. The "1" doubles as a monogram *and* the keyhole slot (estimated) |
| Overlay device | None — centred concentric composition, no diagonal tool, no badge |
| Light model | Top-down soft; short baked shadow/halo ringing the blue dial where it meets the silver field; no specular gloss or glass refraction visible (estimated) |
| Layer stack | silver squircle field → recessed shadow halo → electric-blue dial ring (`#166BE5` top → `#0B9EFC` cyan bottom) → white inner disc → navy keyhole "1" (front) |
| Palette economy | 2 hue families: cool-neutral silver field + electric-blue dial. Accent (`#0B9EFC` electric blue) reserved for the one focal ring; navy `#16192F` for the glyph. Disciplined. |

## Signature devices
- **Numeral-as-keyhole double reading** — the brand "1" is drawn as the keyhole slot, so the monogram and the security metaphor are the same shape. Subject-mining at its cleanest for a password manager. `[GOLDEN-NUGGET]`
- **Concentric vault-dial motif** — ring + inner disc + centred mark reads as a combination-lock dial / keyhole. A centred-concentric composition where most Big Sur icons reach for the diagonal-tool overlay; this icon anchors on rotational symmetry instead.
- **Electric-blue-on-silver focal economy** — the entire saturation budget lives in the ring; the field stays desaturated cool-gray, same de-emphasis logic macOS UI uses for surfaces.

## Failures
- None (no hard rubric failures). Soft passes flagged below.

## Soft passes (borderline — scored pass, flagged for synthesis)
- **#4 16px squint:** ring + dark-centre gestalt survives, but the numeral "1" inside the keyhole loses legibility at menu-bar size — it reads as a generic dial/slot, not a "1". The lock reading holds, so it passes, but the monogram is a large-size-only reward.
- **#10 variant robustness:** this is a flat baked Big-Sur icon, **not** an Icon Composer layered composition. The navy glyph carries its own white inner disc so it isn't dependent on the outer field for contrast (good), but there are no authored Default/Dark/Clear/Tinted layers — the system could only crudely recolour the whole bitmap for tinted/monochrome modes. Robust *within* its era, not forward-compatible with macOS 26 tinting.
- **#12 no-text:** the "1" is a numeral, but it functions as the brand's core keyhole glyph (like a monogram), not as a word/label — acceptable, noted for completeness.

## Rhymes with
- *(hint only)* Big-Sur-era **security/utility** icons that put a subject-mined lock or dial glyph, front-facing, on a neutral matte field — the concentric-badge family rather than the diagonal-tool family (TextEdit/Preview). Also rhymes with any "electric accent reserved to one focal ring on a desaturated field" icon. Confirm against future digests before clustering.

## Provenance / caveats
- All hex `(measured)` from the 102px render; `(inferred)` — single icon, single source.
- Vertical seam faintly visible when upscaled = webp compression/upscale artifact, not a design element.
- **Era lag note for synthesis:** 1Password ships a Big Sur icon in the Liquid Glass era — evidence that shipping third-party utilities lag the current icon language. Brand-coherence with `cover.jpg` is strong: the in-app account row and wordmark reuse the same navy keyhole "1"; the cover's cool-blue palette matches the icon's blue family (the plain navy keyhole on the wordmark vs the blue-ring treatment on the app icon is the one deliberate split).
