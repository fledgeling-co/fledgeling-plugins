# Icon: Grape

- **Source:** macapp.supply (`icon.png`, SHA-1 `339249eb`) · **App:** Grape — "The AI note taking app that thinks with you" (Productivity) · grape.cool
- **Era:** Custom / off-model — **the raw Apple Color Emoji grapes glyph (🍇) shipped as-is**, not a designed macOS app icon · **Rubric:** 10/12 (two hard failures, incl. a check-1 non-negotiable) · **Digested:** 2026-07-19
- **Resolution caveat:** source is only **100×100px** with a transparent (RGBA, corner alpha = 0) background — a low-res web render. All hex values are `(estimated)` from a downscaled render; fine specular/edge detail is anti-aliased away and not assessable. This is the single most important honesty note on this entry.

| Dimension | Reading |
|---|---|
| Background | **None — transparent PNG, no field.** No squircle, no gradient, no scene. The object floats. `(measured)` — corners are alpha 0 |
| Glyph | **Object** — a bunch of grapes. Purple sphere-cluster ramp `#2A1560 → #58388F → #6A48A8 → #B38CE4` `(estimated)`; single green leaf `~#527541` upper-left; curved brown stem `~#A46127` upper-right. Optically centred by the emoji's own bounding box, pulled slightly up-left by the leaf/stem crown |
| Overlay device | None |
| Light model | Single top / top-left source; each grape is a glossy 3D sphere with an upper-left specular highlight and short soft contact shadows where spheres overlap. Consistent Apple-emoji glossy render — the one place this asset shows real discipline |
| Layer stack | transparent canvas → leaf + stem (upper crown) → rear grape spheres → mid grape spheres → front/lower grape spheres with speculars |
| Palette economy | 2 hue families (purple grapes + green leaf) + 1 brown accent (stem), each with a ramp. Economical — but that economy is Apple's, not the developer's |

## Signature devices
- **The raw OS emoji as the entire icon.** [GOLDEN-NUGGET, cautionary] The icon *is* U+1F347 grapes rendered in Apple's emoji style — a found object, not authored art. Its only "device" is a literal name pun (app "Grape" → 🍇). Strong, instantly-nameable silhouette; zero committed design personality.
- **Glossy skeuomorphic spheres** — the emoji's glassy 3D shading reads in the pre-Yosemite photoreal-object register, a visual language that clashes with every current macOS icon era.

## Failures
- **#1 Mask discipline (FAIL — non-negotiable):** artwork is a free-floating transparent object with no squircle background. macOS will not tile it; in the Dock it appears as a floating grape cluster with a system shadow but no rounded-rect base — visually inconsistent with every neighbouring app icon. This is the check the system *does to the icon*, so its failure is fatal for Dock/Launchpad duty.
- **#10 Variant robustness (FAIL):** not a layered Icon Composer design. The system cannot synthesise sensible Dark / Clear / Tinted variants from a flat emoji PNG; on a dark wallpaper the deep-purple lower grapes (`~#2A1560`) muddy toward the background.

### Soft passes (flagged)
- **#2 Grid:** centred, but only by the emoji glyph's default bbox — no evidence of Apple-grid safe-zone design; leaf/stem crown skews the optical centre up-left.
- **#4 16px squint:** survives as "grapes" (silhouette + purple/green colour-coding carry), but individual sphere separations smear into one purple mass and the thin brown stem vanishes.
- **#7 Figure-ground:** silhouette survives grayscale, but with a transparent background contrast is undefined and delegated to wherever it lands — at risk on dark wallpapers.
- **#9 Era coherence:** internally consistent *as an emoji*, but off-model for every macOS app-icon era (no squircle, no Big Sur plane, no Liquid Glass layers).
- **#11 Personality:** a specific nameable object beats a generic glyph-on-gradient — but the personality is **borrowed from the OS**, not designed. Template-default in the most literal sense.

## Brand coherence (cover glance)
- The app UI (cover.jpg) is a **sober dark-charcoal, monochrome, bold-sans** register — near-black ground, white/gray "The AI note taking app" headline, a "Now in Beta" pill. **No purple anywhere.** The playful glossy emoji icon shares no palette and no mood with the serious dark AI-notes product — a clear icon-to-brand incoherence.

## Rhymes with
- The **emoji-drop-in / found-object** icon family (apps that ship the OS glyph matching their name) — a template shortcut, not a style.
- The **classic skeuomorphic glossy-object** register (pre-Yosemite photoreal objects, free silhouettes) by rendering language only.
- Consumer-playful icons by palette (saturated purple + rounded spheres) — accidentally, since the developer chose none of it.
