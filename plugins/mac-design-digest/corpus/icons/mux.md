# Icon: Mux

- **Era:** Liquid Glass · **Rubric:** 12/12 (4 soft passes) · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 522×522 — web-resized render, not full 1024) · **App:** Mux, a menu-bar utility for automatic priority-based network switching (parcse.com/mux)
- **One-line read:** A single blue glass "diverging path" glyph on a clear white plate — wayfinding signage rendered as an extruded glass rod.

| Dimension | Reading |
|---|---|
| Background | Flat clear/white plate — reads pure `#FFFFFF` at this resolution (estimated) — full-res likely carries a faint cool-white ramp not recoverable here |
| Glyph | Abstract directional glyph: a forked/branching path. Blue glass, vertical ramp `#72B4FF` (top / arrow tip) → `#3E8EFF` (saturated stem base), mid `#5AA6FF`. Optically ~centred on grid, bounding box centre ≈ (255,265) of 522, but visual mass sprawls lower-centre → upper-right with a thin left tail |
| Overlay device | None — the fork glyph *is* the whole composition; no separate tool/badge/frame |
| Light model | Top-down. Specular highlight baked along the top edge of every glass rod; short soft drop shadow below each stroke (clearest under the T-foot terminal). One consistent source |
| Layer stack | (back) clear white glass plate → blue extruded-glass fork glyph with baked specular + rounded rod terminals (front). System specular/shadow implied but baked into this render |
| Palette economy | One hue family (blue) + white ground + neutral drop-shadow grey. Saturation reserved entirely for the glyph — textbook accent discipline |

## Signature devices
- **Diverging path / fork junction** — a curved branch sweeps up-left, a vertical stem drops to a T-terminus, and a straight diagonal arrow branches up-right from the same junction. A literal picture of "priority-based switching": traffic routes split at a decision point.
- **Mismatched terminals as meaning** `[GOLDEN-NUGGET]` — one branch ends in an outward **arrowhead** (redirect / switch away to the better route), the other two in plain **rounded T/foot caps** (the anchored, stay-put paths). The terminal shapes carry the switch semantics, not colour or a badge. This is subject-mined, not template.
- **Glass-rod extrusion** — rounded line caps, top specular rim, saturated underside; consistent Liquid-Glass rod treatment across all strokes; the left branch cleanly passes *under* the diagonal arrow (no z-fighting).
- **Monochrome menu-bar derivative** — the cover shows the same glyph as a mono template symbol in the menu bar; the icon system has a working single-tint reduction (evidence its silhouette survives tint/flatten).

## Failures
- None (no hard failures).
- **Soft passes flagged:**
  - **#2 Grid/optical centring** — bounding box centres well, but visual weight is a diagonal lower-centre→upper-right sprawl with a thin left tail rather than a symmetric grid-seated glyph. Deliberate wayfinding asymmetry, not a defect.
  - **#3 Silhouette** — "a forked/branching arrow" is nameable but abstract; filled solid it reads as a junction of three termini, not an instantly-literal object.
  - **#4 16px squint** — thick high-contrast strokes carry the gesture, but the up-right **arrowhead** (the element encoding "switch") is both the smallest feature *and* the lowest-contrast (`#72B4FF` ≈ luma 180 on white); the thin left tail is the first casualty at menu-bar size.
  - **#10 Variant robustness** — glyph is self-coloured (survives dark/tinted, per the mono menu-bar version), but the composition leans on a light/white base for the blue ramp's legibility; a dark render shifts, though it holds.

## Rhymes with
- Style family: **single-glyph glass utility** — one SF-Symbol-family directional glyph (kin to `arrow.triangle.branch` / `arrow.triangle.turn.up.right`) rendered as an extruded glass rod on a clear plate. Rhymes with Apple's own system-utility and network/VPN menu-bar icons, and with transit/wayfinding-arrow marks.
- First icon in the corpus — no digested peers yet. Flag for an icon cluster once 2+ more single-glyph-glass utilities land.
