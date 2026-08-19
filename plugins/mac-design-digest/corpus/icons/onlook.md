# Icon: Onlook

- **Era:** custom (atmospheric emissive scene — quotes the Big Sur front-facing squircle discipline but rejects its top-down light model) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, SHA-1 `e7e13c57`) · **Subject:** menu-bar utility that streams Ring doorbell/security cameras onto the Mac ("Ring cameras in your Mac menu bar")

| Dimension | Reading |
|---|---|
| Background | scene — a dark interior room, near-black warm-charcoal walls `#292A21`→`#2D3021` falling off at the mask edges, warming toward the centre bloom `#48452D` (estimated) |
| Glyph | object rendered as pure light: a glowing doorway/threshold, aperture blown to pale chartreuse-cream `#F2FCA2`→`#F0FCA6`; optically centred, nudged **above** centre to seat the receding floor below it |
| Overlay device | none |
| Light model | **emissive** — the doorway *is* the light source; warm bloom radiates outward into the dark room, spills onto a lit floor; no system top-down light, no glass specular edge (estimated) |
| Layer stack | dark room walls → warm bloom halo → lit orange threshold floor → blown-highlight doorway aperture |
| Palette economy | one warm ramp (cream→amber→terracotta) on a neutral-dark field; the entire warm glow is the accent, reserved to the focal doorway — disciplined |

## Signature devices
- **Emissive doorway** `[GOLDEN-NUGGET]` — the subject is a *hole of light*, not a lit object. Inverts the icon convention of glyph-on-field: here the "glyph" is negative space that emits, and the field is the drawn matter. The Ring-camera metaphor made atmospheric — a watched front door.
- **Warm bloom into dark** — cinematic bloom bleeds the doorway's glow into the surrounding charcoal walls (top-centre reads `#48452D`, up from the `#292A21` corners), so figure and ground dissolve into each other rather than meeting at a hard edge.
- **Lit threshold floor** — an orange light-spill (`#EBB75E`→`#B1613A`) recedes from the bottom edge toward the door, a one-point-perspective floor that supplies the icon's only depth cue and its warmest hue.
- **Drenched-dark atmosphere** — committed direction: near-black field, single warm luminous focal, zero decorative element. The boldness budget is spent entirely on the glow.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black, the icon is just a squircle. The subject is defined *only* by luminance and colour, never by shape; there is no nameable silhouette. This is the structural cost of the emissive-scene approach.

## Soft passes (borderline, flagged for synthesis)
- **#1 Mask discipline** — design is mask-appropriate (dark field bleeds to the edge as a background), but this render has **baked-in rounded corners on an opaque white background** (`#FFFFFF` at all four corners, no alpha) — a pre-masked web resize, not a full-bleed 1024 square. Shipping asset presumed full-bleed; can't verify from this source.
- **#4 16px squint** — survives as a clean, high-contrast bright-warm-centre-in-dark mark (does not smear to mud), but the *door* reading is lost — at menu-bar size it reads "a warm glow," not "a doorway." Distinctive presence, weak subject identity.
- **#9 Era coherence** — internally consistent, but the register is custom/cinematic, not a committed quotation of any named Apple era; it borrows only the front-facing uniform squircle.
- **#10 Variant robustness** — structure (luminance aperture on dark) would survive dark/clear/mono, but the icon's entire *identity* is its warmth; a tinted (blue/green) render would strip its soul. Colour-dependent by design.

## Rhymes with
- Atmospheric **scene/emissive-focal** family, not the Big-Sur object-on-gradient or Liquid-Glass layered-glyph families. Nearest peers: ambient/meditation and portal-launcher icons that render a single glow on a black field (Endel-/Portal-class), and dark-drenched game-launcher marks. First of its kind in this corpus — no digested sibling yet; a hint, not a cluster.
