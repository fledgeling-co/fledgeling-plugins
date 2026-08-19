# Icon: Keeby

- **Era:** skeuomorphic-quote (visual language) — contemporary glossy-3D-render dialect, structurally non-conforming to macOS 26 layered delivery · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/keeby/icon.webp`, a 312×312 WebP web render — not a 1024 master) · **Category:** Utility
- **Subject the icon must communicate:** an app that plays mechanical-keyboard sounds for Mac ("Your keyboard, but better"). The icon must say *keyboard* and *fun/pleasant*.

| Dimension | Reading |
|---|---|
| Background | **transparent — no field** (alpha 0 at all four corners). The whole icon is a single free-standing 3D **keycap** object; the keycap's own orange crown is the surface the glyph sits on. Because the object is a full rounded-square, the transparent corners are the mask corners, not under-fill. `(measured)` |
| Glyph | An embossed cream **smiley face** on the keycap crown: two round eyes (`#FCFBF0`/`#FFFAE4`, centres ≈ x120/x196, y110 of 312) + an upward arc smile (mid ≈ x156,y175). Sits in the **upper-centre** of the face (eyes above true centre) — correct optical placement for a crown domed toward the viewer. `(measured)` |
| Overlay device | none (no diagonal tool, badge, or frame). The smiley is inset into the crown, not overlaid across the plane. |
| Light model | **top-left key light, glossy plastic.** Tight speculars blown to `#FFFFFF` on the crown and a bright rim band along the top edge; soft falloff down the domed face; the keycap **skirt** (side walls) recedes into `#711D03` at the bottom-right. One coherent light — but **all of it is baked in**, not system-applied. `(measured)` |
| Layer stack | transparent ground → keycap **skirt / side-walls** (receding, shadowed) → keycap **crown face** (orange gloss ramp) → **embossed cream smiley** → **specular gloss highlights** (crown hotspot + top rim). |
| Palette economy | one hue family (orange, `#FFB057`→`#FF8B18`→`#F9770A`→`#BB4609`→`#711D03`) + one warm neutral (cream glyph `#FCFBF0`) + a pure-white specular. Two "colours", one hue. Textbook economy. |

## Palette
- **Specular hotspot:** `#FFFFFF` (255,255,255) — blown gloss highlight on the crown `(measured)`
- **Bright gloss / top rim:** `#FFB057` (255,176,87) — lit upper zone `(measured)`
- **Crown body (mid):** `#FF8B18` (255,139,24) / `#FB8718` — the icon's identity orange `(measured)`
- **Crown lower curve:** `#F9770A` (249,119,10) — deeper orange as the dome turns away `(measured)`
- **Skirt (side wall):** `#EC6A0B` (lit left) → `#BB4609` (front) → `#A93A0C` (right) `(measured)`
- **Skirt deep shadow:** `#711D03` (113,29,3) — burnt orange, bottom-right recess `(measured)`
- **Glyph (smiley):** `#FCFBF0` / `#FFFAE4` (253,251,240) — warm cream, near-white `(measured)`
- **Background:** transparent (0,0,0,0) `(measured)`

## Signature devices
- **[GOLDEN-NUGGET] Keycap-as-icon.** The app's entire subject — a mechanical keyboard — is compressed into one literal keycap rendered as the whole icon. Pure subject-mining: the mark *is* the thing the app touches. Rare clarity for a utility.
- **[GOLDEN-NUGGET] Embossed smiley on the crown.** A sound-utility could have shown a speaker or a soundwave; instead the keycap wears a face. The smile carries the app's whole "but better / pleasant" promise in two dots and an arc, and turns a tool into a character.
- **Candy-gloss injection-moulded plastic.** Pure-white specular hotspot + short, hard speculars + a bright top rim = glossy ABS keycap material. The gloss is the personality substrate — this reads as a physical, tactile, *fun* object, not a flat pictogram.
- **Visible keycap skirt.** The receding, shadowed side-walls (down to `#711D03`) sell real 3D depth; without the skirt this would be a flat orange rounded square. The skirt is what makes it unmistakably a *keycap*.

## Failures
- **#10 Variant robustness — FAIL.** Not built as Liquid Glass layers. It is an opaque, baked, single-object render with no separable foreground layer for the system to re-tint. In dark/clear/tinted macOS 26 renders it cannot be re-lit or re-coloured — a tinted/mono pass collapses the whole thing to a flat monochrome rounded-square-plus-smiley, losing the gloss, the depth, and the orange identity that *are* the icon. The baked specular/shadow (HIG: "let the system handle blurring and effects… don't bake in specular highlights, drop shadows") is the root cause.

### Soft passes (flagged, scored as pass)
- **#1 Mask discipline — soft.** The keycap silhouette is a rounded square that fills the frame and reads cleanly as a squircle in the Dock — far better mask conformance than a floating-object icon. But it is delivered as a free object on transparency with **baked** gloss/highlight/skirt-shadow rather than as a flat, unmasked square layer for the system to light. Reads fine today; deviates from macOS 26 layered delivery.
- **#3 Silhouette test — soft.** Filled solid black, the shape reads only as a generic **rounded square / keycap** — nameable as a key, but the differentiating smiley is interior cream-on-orange and vanishes in pure silhouette. The icon's identity lives in the interior glyph + gloss, neither of which survives a silhouette isolation.

## Rhymes with
- **Glossy 3D single-object render icons** — the Spline/Blender indie wave (claymorphism-adjacent), where one candy-material object floats as the whole mark. Keeby is a tight member: literal object, blown speculars, no background tile.
- **Playful/toy single-glyph icons** — the embossed-friendly-face-on-object motif (a smiley pressed into a form) belongs to the toy family, not the pro-utility flat-glyph family its category ("Utility") would predict. The mismatch is deliberate warmth.
- Cross-note for synthesis: shares the **transparent free-object, baked-lighting, #10-fail** structure with AutoShelf — but conforms to the mask far better (fills the frame as a squircle vs. floating at ~52% width). If 2+ more glossy-3D-object icons appear, split a "glossy-3D-render object" cluster distinct from the flat "floating-object utility" one.

## Notes (resolution & synthesis)
- **Resolution caveat:** source is a 312×312 WebP web render (converted via `sips -s format png`); no 1024 master. Flat-face hex and the gloss ramp are reliable; fine gloss micro-gradients, exact specular edges, and the emboss depth of the smiley are soft at this scale.
- **Transparency is genuine** as far as can be told — all four corners are cleanly alpha-0, consistent with a rounded-square keycap silhouette (the corners are simply outside the shape). Either the shipping icon ships as a free object, or macapp.supply stripped a tile; the near-full-frame keycap makes this low-risk for Dock reading regardless.
- **Brand coherence with the cover is strong.** The cover's `keeby` wordmark, the download-button accent, the app-window gradient, and the menu-bar glyph all use this same orange; the cover reproduces the keycap icon verbatim at the hero. The icon is the brand's whole colour identity — one committed orange + cream — not a detached render.
- **Adjectives (committed):** glossy-candy · friendly · tactile. This is a *committed* direction (toy/glossy family), not a template-default flat utility glyph — the boldness budget is spent entirely on material + face.
