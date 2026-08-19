# Icon: Shake it On

- **Era:** Big Sur unified (3D-render idiom) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 400×400 web render — sub-master resolution; squircle baked into PNG as transparent corners) · **Category:** Utility · **App does:** mouse jiggler ("keeps your Mac wide awake") — the icon has to say "shake" and "cursor" at once.

| Dimension | Reading |
|---|---|
| Background | ramp `#40A8E8` → `#2870C8` (measured), light sky-blue top → deeper blue bottom, single hue ~205°, sky-logic vertical ramp |
| Glyph | scene/object: two 3D-rendered wooden maracas held in a fist, warm tan wood `#E0B880` shading to `#906838`, orange tips `#E08040`, dark navy band `#385878`; a brown rubber-duck engraving `#906838` stamped on each bulb. Optically centred, cluster fills the upper-two-thirds with the fist anchoring the lower-centre |
| Overlay device | other — a flat black macOS arrow pointer (white outline) as a prop bottom-right, plus flat-vector motion/sound arcs flanking the maracas. Maracas themselves are held diagonally (the Apple "tool at an angle" tradition) |
| Light model | soft top / top-left key light; baked ambient-occlusion contact shadows where the hand grips; short soft drop shadows; matte clay render — no glass specular or refraction |
| Layer stack | blue gradient squircle → motion arcs → two crossed maracas → gripping hand → shirt sleeve → macOS cursor glyph |
| Palette economy | 2 hue families: blue (bg, sleeve, arcs, navy band) + warm wood/tan (maracas, hand, duck); orange tips `#E08040` are the single saturated accent, reserved for the focal maraca caps |

## Signature devices
- **[GOLDEN-NUGGET] The shake-pun made literal.** A mouse-jiggler is named and drawn as maracas — the app's whole function (physically shaking something to keep the Mac awake) compressed into one instantly-readable object. This is subject-mining, not a generic tool-on-gradient.
- **[GOLDEN-NUGGET] The cursor caught in the scene.** The macOS black arrow pointer is pulled in as a physical prop bottom-right, so the OS's own UI element becomes a character being "shaken awake." The icon references what the app *acts on*, not just its metaphor.
- **Rubber-duck engraving.** A brown duck stamped on each maraca bulb — a mascot/easter-egg brand detail (echoed nowhere else, likely the dev's signature). Invisible below ~64px.
- **Flat motion arcs.** Two-to-three flat-vector "shake" waves flank each maraca to inject movement into a static frame — a comic-strip motion convention.
- **3D clay-render object on gradient squircle** — the base Big Sur indie-utility idiom (matte-rendered object, baked AO, soft top light).

## Failures
- **#10 background-dependence (variant robustness):** the blue shirt sleeve (`#57A3D9`) and the blue motion arcs (`#3E9DDF`) are the same hue as the blue background field — they read only because of a soft edge, not a colour break. Under a dark, clear, or tinted render (or on a blue-tinted wall) the sleeve and arcs would dissolve into the ground. Not a Liquid Glass icon so the check is strictly out-of-era, but the fragility is real and worth logging.

## Soft passes (borderline — flagged, not failed)
- **#1 mask:** artwork is designed for the squircle and sits inside the safe zone, but the squircle is *baked into the PNG* (transparent corners) rather than delivered as a square unmasked layer — risks double-rounding / a hairline mask mismatch on macOS 26, which rounds the corners itself.
- **#2 grid:** maraca tips reach close to the top safe-zone margin (~8–10%); the composition is busy at the edges.
- **#3 silhouette:** filled solid black, the composite (two bulbs-on-sticks + fist + arrow + arcs) is busy for a single anchor — but "a hand shaking maracas" does read.
- **#4 16px squint:** at menu-bar size the duck engraving, motion arcs, and cursor all smear to noise; only the two wooden bulbs + the fist survive. The primary object is graspable; every secondary storytelling layer is lost. This matters because a jiggler likely lives *in the menu bar* at exactly this size.
- **#7 figure-ground:** warm tan maracas hold well against blue in grayscale, but the duck engraving is brown-on-tan (~1.8:1) and near-invisible without colour — acceptable as it is secondary detail only.
- **#9 era coherence:** the flat-vector cursor and motion arcs sit in a different rendering register (flat 2D) than the 3D-rendered maracas and hand. Deliberate (cursors are always flat UI glyphs) but it is a mixed idiom.

## Rhymes with
- The Big Sur 3D-render **object-in-a-hand** indie-utility family: matte-clay props on a saturated gradient squircle, warm-object-on-cool-field, one saturated accent reserved for the focal detail. Menu-bar utilities that lean on a playful literal mascot/prop rather than an abstract glyph.
- Warm-wood-on-blue palette pairing (warm figure / cool ground) is the recurring figure-ground move to watch for across the corpus.

*(Rhymes-with is a hint for synthesis, not a cluster assignment — ICONS.md owns clustering.)*
