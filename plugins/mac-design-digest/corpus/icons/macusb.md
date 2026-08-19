# Icon: macUSB

- **Era:** Big Sur unified (host) with a flat-transition glyph — mixed · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply submission `icon.jpeg` (1024×1024, JPEG). Category: Utility. App: guided bootable-USB creator for Mac.

| Dimension | Reading |
|---|---|
| Background | Vertical ramp `#FFFFFF` (top) → `#BEC4C2` (bottom) (measured, ±3 JPEG). Cool near-neutral gray, faint green cast; light-at-top → darker-at-bottom sky logic. Squircle mask **baked into the asset** (corners reveal white page). |
| Glyph | Object — a literal USB-A flash drive on a lower-left→upper-right diagonal. Near-black body `#292929`–`#2F2F2F` with a subtle sheen (lightens to `#535554` at the lower tail); light metal connector panel `#E7EBEC`; whole object wrapped in a uniform dark keyline `#424242`–`#525252`. Optically fills the diagonal; mass skews slightly lower-left. |
| Overlay device | None — the drive *is* the glyph; no badge, frame, or tool crossing a separate glyph. |
| Light model | Ambient top-light *implied by the ramp only*. The object itself is rendered flat with a uniform dark keyline and a weak sheen gradient that runs counter to top-down light (lightening toward the lower tail). No specular, no cast/contact shadow — a flat sticker sitting on a lit field. |
| Layer stack | (back→front) 1. squircle ramp field · 2. drive body (near-black flat fill + dark keyline) · 3. connector panel (light metal + keyline + two square contact cutouts). No shadow layer, no glass layer. |
| Palette economy | One near-neutral hue family + a light gray ramp. Essentially monochrome grayscale. **Zero saturated accent** — no brand color anywhere. |

## Signature devices
- **Diagonal object staging** — drive runs corner-to-corner (lower-left → upper-right), the Apple "tool at an angle" tradition (TextEdit/Preview lineage). Generic execution here.
- **Uniform dark keyline outline** around the entire object — the icon's most defining and most off-era trait. Reads as flat-design / iOS-7-sticker clip-art rather than Big Sur material modeling.
- **Fully monochrome palette** — the object communicates the subject (a USB drive) but not the brand; no color commitment at all.

## Failures
- **#5 Single light model** — incoherent. Ramp implies top light; the body's sheen gradient lightens toward the *bottom* tail (against top-down); the keyline is uniform/flat (no light at all). Three treatments, no single source.
- **#9 Era coherence** — mixed languages, not a deliberate quotation. Big Sur host (squircle + light vertical ramp + single diagonal object) fused to a flat-transition glyph (heavy black keyline, flat fill, no form modeling). This is the icon's central craft gap.
- **#10 Variant robustness** — glyph depends entirely on the light background for contrast. A near-black body + dark keyline would collapse on a dark/tinted system render (macOS 26 generates these); not authored as appearance-aware light/dark layers.

### Soft passes (flagged, counted as passes)
- **#1 Mask discipline** — artwork fits the squircle fine, but the mask is *baked into the delivered JPEG* on a white page rather than a clean full-bleed square layer; can't verify the source layer, and HIG wants unmasked square layers.
- **#2 Grid adherence** — occupies the diagonal well and optical centre roughly holds, but mass skews lower-left (connector reaches for the upper-right safe zone).
- **#4 16px squint** — near-black mass on light ground holds the USB-stick gestalt, but the two connector contact cutouts and the keyline detail smear at menu-bar size.
- **#8 Depth coherence** — planes are ordered and there's no z-fighting, but the object floats with no grounding contact shadow and the one internal gradient conflicts with the ramp's implied light.
- **#11 Personality** — the keyline-outlined diagonal drive is nameable as a device but is template-default; no committed direction. Absence of a distinctive move is why it reads as an icon-pack asset, not a crafted mark.

## Notes for synthesis
- **Provenance / resolution:** genuine 1024×1024 but a ~62KB JPEG with the squircle mask baked in — a pre-masked web render, not a source layer. Hexes are `(measured)` off compression, treat as ±3–4.
- **Asset discrepancy (important):** the in-app cover screenshot shows a *different, more polished Liquid-Glass* squircle icon (glossier, layered glass drive, lighter treatment) than this submitted `icon.jpeg`. The submitted asset appears to be an older/lower-fidelity rendition; the shipping icon may already have moved to a glass treatment. This digest covers the submitted asset only.
- **Icon↔brand palette coherence is weak:** the cover/brand leans vivid blue→teal→green with a blue (`~#0088FF`) primary CTA; the icon is fully grayscale and echoes none of it. An icon should carry a thread of the brand palette; this one doesn't.

## Rhymes with
- (hint only) The "underbaked utility object" family — flat, keyline-outlined literal-object icons on a Big-Sur squircle ramp; stock disk/driver/flash-tool utility icons and iOS-7-era flat object art. No other digested icons to bind to yet.
