# Icon: Supaste

- **Era:** Big Sur unified (gradient-fill lineage; flirts with glass via a *baked* gloss but is not an Icon Composer Liquid Glass composition) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp`, **256×256** web render (lossy WebP). Resolution caveat: fine specular/translucency/noise at the 1024 master is not observable; at 256 the icon is unambiguously a simple gradient + one opaque glossy element (no refraction, no true translucency).
- **Subject:** clipboard + screenshot history manager ("Supaste" = super-paste).

| Dimension | Reading |
|---|---|
| Background | Vertical ramp #86E1FF → #0533FF (measured) — light cyan at top, electric/pure blue at bottom; sky-logic (light-top → dark-bottom) |
| Glyph | **Abstract single capsule/pill**, white with a top-down gloss ramp #FFFFFD → #E7F6FE → #C6E7FE (measured). Horizontally centred, even L/R margins; anchored **high** (centre ~y58 of 256, upper third) not optically centred |
| Overlay device | None — no diagonal tool, no badge, no frame. The pill *is* the glyph, not an overlay |
| Light model | Top-down, single source. Field gradient light-top/dark-bottom; pill specular white-top → blue-tinted-bottom; subtle bright rim on the squircle's top edge (#86E1FF catch); a soft short micro-shadow reads beneath the pill (partly compression at 256). All consistent — no mixed lighting |
| Layer stack | (1) blue vertical gradient field → (2) top-edge rim highlight → (3) white glossy capsule with baked gloss + soft micro-shadow |
| Palette economy | **One** hue family (cyan→blue ramp) + white glyph; zero competing accent. Maximally economical |

## Signature devices
- **Single glossy capsule as the sole glyph** — reductive to the point of one element on an otherwise empty field. The entire icon is "one white bar on blue."
- **Sky-logic electric-blue ramp** (#86E1FF → #0533FF) — the whole lower two-thirds is open saturated-blue field.
- **Baked specular gloss on the pill** (white-top → blue-tint-bottom) — an old-school iOS/Big-Sur gloss gesture, hand-baked rather than system-applied (the opposite of Liquid Glass authoring, where the system adds specular).
- **Top-anchored bar** — admits two readings: the *clip of a clipboard* (clip always sits at the top → on-theme, defensible as intentional) or simply the *top row of a list*. Charitable reading rescues the top-weight as a clipboard-clip metaphor.

## Rubric (12-point)
1. Mask discipline — **pass**: gradient runs full-bleed to the squircle, glyph well inside the safe zone, no corner-radius fight.
2. Grid adherence — **soft pass**: horizontally centred with clean symmetric margins, but vertically **top-weighted** — a large dead blue field fills the lower two-thirds. Defensible only under the clipboard-clip reading.
3. Silhouette test — **soft pass**: reads cleanly as ONE anchor (a horizontal rounded bar), but the shape is **generic** — filled solid black it names "a bar / a row," not "clipboard history." Clear, not communicative.
4. 16px squint test — **pass**: the single bold high-contrast white bar on blue is exactly what survives downscaling; this reductiveness is the icon's real strength at Dock/Spotlight/menu-bar sizes.
5. Single light model — **pass**: top-down throughout (field, pill gloss, rim).
6. Palette economy — **pass**: one hue family, no accent.
7. Figure-ground contrast — **pass**: white pill on medium-blue field, well above 3:1, survives grayscale.
8. Depth coherence — **pass**: field-behind / pill-in-front, micro-shadow consistent with top-down light, no z-fighting.
9. Era coherence — **pass**: all devices from the Big-Sur gradient vernacular; consistent (leans iOS but doesn't mix eras).
10. Variant robustness — **soft pass**: strong figure-ground means a system tint/mono recolour wouldn't collapse the shape, BUT it is a single baked raster with a hardcoded gradient — **not authored as layers** for default/dark/clear/tinted. In the macOS 26 era this is a real authoring gap; variants would be system-crude, not designed.
11. Personality — **FAIL**: this is glyph-on-gradient at its most template-default. A saturated vertical-blue squircle is among the most common iOS/Big-Sur backgrounds, and a lone white rounded rectangle is minimal to the point of anonymity. It neither establishes a distinctive device nor **communicates its subject** (nothing says clipboard / paste / *history*). Committed to minimalism, but the commitment lands on generic.
12. No-text check — **pass**: pure abstract, no words/UI/photo.

## Failures
- **#11 Personality (template-default)** — "blue vertical gradient + one white pill" is a template silhouette, not a committed direction. The subject (clipboard **history** — plurality, a stack, screenshots) is entirely uncommunicated; a stack of offset bars or a layered-cards motif would have said "history" and earned personality at the same 16px clarity. This one weakness drives the whole score: everything mechanical (mask, light, palette, contrast, 16px) is immaculate; the icon is *technically clean, characterically anonymous*.

## Rhymes with
- The **iOS/Big-Sur "single white glyph on a vertical-blue ramp"** utility family (Messages-blue lineage; generic clipboard/notes/utility icons). Style family: *saturated-gradient minimalist utility*.
- Palette-coherent with its own cover art: the cover's hero **sky gradient** (#73C9FF → #2460DB, measured) is the same ramp as the icon, and the cover surfaces a `#0080FF` brand-blue swatch — icon and brand share one blue. Strong icon↔brand palette coherence; weak icon↔subject communication.
