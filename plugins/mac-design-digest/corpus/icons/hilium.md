# Icon: Hilium

- **Source:** macapp.supply (icon.png, 180×180 pre-masked PNG) · **Category:** Utility (control your Mac wirelessly from iPhone) · **Era:** Big Sur unified (template execution) · **Rubric:** 9/12 · **Digested:** 2026-07-19

Single-hue cyan gradient squircle carrying a bright-aqua radial "wireless burst" (rounded-cap spinner/aperture segments) with an inward-pointing cursor arrow, over faint concentric ring ripples. The concept is legible — *point-and-control a signal* — but the glyph is rendered in the same hue family as the field, so figure-ground contrast collapses to ~1.5–2.4:1: the icon's ambition (energetic connectivity mark) is undercut by its execution (aqua-on-cyan, near-invisible in grayscale and at Dock size).

| Dimension | Reading |
|---|---|
| Background | Diagonal ramp `#00C6FF` (upper-left, bright cyan) → `#009BFA` (lower-right, blue) `(measured)`(inferred) — sky-logic inverted to a light-source-upper-left diagonal |
| Glyph | Abstract dual motif: radial burst of ~8 rounded-cap segments (spinner/aperture) + bold cursor arrow pointing up-left into the burst centre. Aqua `#00FFFF`–`#00FEFF`. Optically centred, generous safe-zone margins |
| Overlay device | Inward cursor arrow crossing the radial burst (loose kin to the Big Sur "diagonal tool" tradition — here a pointer, not a pen) |
| Light model | Minimal/flat. Diagonal gradient ramp only; faint top-brighter shading inside strokes; **no** committed top-down shadow, no baked micro-shadows, no specular |
| Layer stack | back→front: (1) cyan→blue gradient field · (2) faint concentric ring ripples (wireless-wave texture) · (3) aqua radial burst segments · (4) aqua cursor arrow |
| Palette economy | One hue family (cyan→blue) + aqua glyph. Extremely economical — to a fault: no reserved contrasting accent, so the glyph never separates from the ground |

## Signature devices

- **Wireless-wave concentric rings** — faint darker-cyan ripples radiating from centre, encoding the "wireless" in the tagline without a literal Wi-Fi arc `[GOLDEN-NUGGET]`.
- **Radial aperture/spinner burst** — rounded-cap segments fanning outward; reads as signal/energy. Consistent with the app's wordmark (same burst appears white in the cover's bottom-left logo — mark-consistent brand).
- **Inward cursor arrow (point-to-control)** — a pointer aimed *into* the burst, literalising "control your Mac." Pairs the destination (signal) with the instrument (cursor).

## Failures

- **#4 16px squint test** — at menu-bar/Spotlight size the ~1.5–2.4:1 glyph/field contrast plus fine rounded segments smear into a flat cyan tile; the dual motif is unresolvable.
- **#7 Figure-ground contrast** — glyph `#00FFFF` vs field `#00ADFF` ≈ **1.99:1**; worst case ~**1.46:1** over the bright centre, best ~**2.37:1** over the deepest blue. All below the 3:1 floor; near-vanishes in grayscale.
- **#10 Variant robustness** — not authored as Liquid Glass layers; the (already weak) separation depends entirely on the cyan field. A tinted/clear/dark render would collapse the aqua-on-cyan further. No dark/mono variant evident.

**Soft passes (flagged, scored as pass):**
- **#3 Silhouette** — two competing motifs (radial burst *and* cursor arrow); as solid black it reads as a cluttered asterisk-plus-arrow, nameable but not a single clean object.
- **#5 Single light model** — consistent, but the "model" is a flat diagonal ramp; no committed Big Sur top-down lighting to cohere against.
- **#8 Depth coherence** — ordering is sensible but depth is near-flat; the concentric rings are the only spatial cue and they are faint.

## Rhymes with

- Generic iOS/utility **gradient-squircle + monoline-glyph** icons (the cross-platform template look). 180×180 = iOS 60pt@3x — likely the iOS icon reused for the Mac listing.
- Connectivity/remote-control utilities that lean on **radial signal motifs** (Wi-Fi arcs, aperture bursts) and cool cyan-blue ramps — a "network/remote" style family.
- Awaiting a corpus peer with a *high-contrast* glyph-on-cyan to contrast against; Hilium is currently the cautionary example of the family (monochrome collapse).

## Resolution & provenance caveats

- 180×180 **pre-masked** PNG (rounded superellipse corners already applied, transparent outside): the 1024 full-bleed master and any mask-fighting cannot be verified — mask discipline assessed on the render only.
- Hex values are indicative from a small web render, not exact master samples; the concentric rings are faint enough that some could be compression.
- Cover art is austere black/white and reuses the burst mark in white — brand *mark* is coherent across surfaces, but the icon's cyan palette does **not** carry into the cover (palette-divergent).
