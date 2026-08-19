# Icon: Picmal

- **Era:** custom (modern squircle mask, flat abstract field — declines both Big Sur baked-depth and Liquid Glass layers) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/picmal/icon.png`, 256×256 — resized web render, not the 1024 master) · **Category:** Utility (media converter/compressor)

| Dimension | Reading |
|---|---|
| Background | Flat electric blue `#1B5BFF` (estimated) anchoring all four corner regions; not a vertical ramp — each tone is a flat fill |
| Glyph | None. An abstract full-bleed **marbled flow field**: pale-periwinkle `#CBDEFF` and near-white `#F2F6FF` ribbons weave S-curves corner-to-corner. No optical-centre glyph — the field *is* the mark |
| Overlay device | None (no tool/badge/frame). A thin saturated-blue keyline `~#0078FF` (~1px @256, ≈4px @1024) rims the squircle edge |
| Light model | Flat / ambient — opaque flat fills, no directional light, no baked micro-shadows, no specular. Commits to no era light model |
| Layer stack | (all coplanar flat shapes, z-order back→front) 1 electric-blue base field → 2 pale-periwinkle ribbons → 3 near-white ribbon highlights → 4 saturated-blue hairline keyline on the mask edge |
| Palette economy | Single hue family (one blue), three lightness stops: `#1B5BFF` → `#CBDEFF` → `#F2F6FF`. Accent = the electric blue itself (both ground and focal). Very economical |

## Signature devices
- **Marbled flow field** `[GOLDEN-NUGGET]` — a full-bleed fluid ribbon motif (loose S-curves) instead of a centred object; the entire icon is one abstract tonal composition. Reads as flowing/transforming — a plausible (if oblique) nod to media *conversion*.
- **Single-hue tonal ramp** — the whole icon built from one blue at three stops; no second hue anywhere. Maximum palette discipline.
- **Saturated keyline** — a thin electric-blue outline traces the squircle. Baked into the artwork (HIG says let the system stroke/mask) — minor, but a nameable choice.
- **Full-bleed, no margin** — declines the safe-zone; the field bleeds to the mask edge (a deliberate, allowed choice for a background-field icon).
- **Brand coherence with the app** — the electric `#1B5BFF` is the app's accent everywhere in the cover (Convert button, corner wedges, list checkboxes, footer wordmark lockup). Icon↔UI palette is one system.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black it collapses to a bare squircle; no nameable subject. This is an abstract-field icon *by choice*, but it fails the test as written — nothing communicates "media / convert / image." (This is a non-negotiable check when *generating* — spec would not clear the bar.)
- **#10 Variant robustness — FAIL.** Opaque, fixed blue+white field, not a layered Icon Composer design; no dark/clear/tinted adaptation to draw on. The near-white ribbons would glare in a dark render; there is no dark-adapted variant.

## Soft passes (flagged)
- **#1 Mask** — artwork is designed for the squircle and fills it edge-to-edge, but the ~1px saturated-blue keyline is a **baked stroke** (system should own the edge treatment).
- **#4 16px squint** — survives only as a *blue-and-white colour blob*; ribbon detail smears. Identity is colour, not form — and "blue tile" is a crowded field at Dock/Spotlight size.
- **#7 Figure-ground** — the blue-vs-pale contrast holds (`#1B5BFF` vs `#F2F6FF` ≈ 5.4:1), but the pale-periwinkle-vs-near-white ribbons collapse in grayscale (`#CBDEFF` vs `#F2F6FF` ≈ 1.2:1). Interior structure vanishes without colour.
- **#9 Era coherence** — internally consistent, but it declines the current-era (Tahoe / Liquid Glass) material vocabulary entirely; the flat opaque construction reads as a web-graphic tile rather than a mac-native layered/glass icon.

## Rhymes with
- Abstract **fluid / marble-field** icons — single-hue tonal tiles and flow motifs rather than glyph-on-gradient. Kin to wallpaper-style abstract utility icons and the "brand-blob" school. (Hint only — needs ≥2 more members before any icon-cluster claim.)

## Notes for synthesis
- **Resolution caveat:** 256×256 resized web render, not the 1024 master. Fine ribbon-edge quality, any true texture/specular, and sub-pixel keyline width can't be verified; all hex values `(estimated)` from the downscaled PNG.
- The strength here is **palette discipline + brand coherence**; the weakness is **legibility of purpose** — a converter icon that says "blue" but not "media." Distinct in colour, anonymous in function.
