# Icon: Presentify

- **Era:** Big Sur unified (3D single-object on gradient field) · **Rubric:** 12/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, 256×256 pre-masked web render (SHA-1 `8add3189`). Category: Productivity. App: a screen-annotation / live-presentation tool ("Annotate, Highlight, Spotlight, and Zoom in real-time" — meta.json / cover).
- **Resolution caveat:** only a 256px render was available, delivered **pre-masked** (transparent outside the squircle, alpha≈0 at corners) — this is a downscaled shipping render, not the 1024 full-bleed master. Palette hexes below are reliable `(measured)`; bevel radii, edge-highlight softness, and sub-pixel ambient-occlusion are below the resolution floor → `(estimated)`.

| Dimension | Reading |
|---|---|
| Background | Vertical violet ramp **#9B64E8 (top) → #8D54DC → #7C42CB → #6C35BC → #6027AE → #561DA4 (bottom)** — one hue family, light-at-top → dark-at-bottom (Big-Sur "sky logic"). Left/right edges track the same ramp (symmetric, no side lighting) |
| Glyph | **Object** — a presentation easel / whiteboard on a tripod, front-facing, rendered in soft matte plastic. Frame + tripod in light lavender-white (**#EAE1F7 → #F6F4FB** highlights); inner screen a recessed purple panel with its own top-lit ramp (**#8F54E2 top → #7A3ECD → #6A2FBD bottom**). Optically centred; board mass sits upper-middle, tripod extends to lower third to balance |
| Overlay device | **None** — a centred hero object, not a diagonal-tool overlay or badge |
| Light model | Single **top-down**, soft/diffuse. Board frame top edge lightened, lower edge shadowed; short baked ambient-occlusion where board meets tripod and behind the legs. No specular glass rim, no refraction, no long dramatic shadow (system supplies the drop shadow) |
| Layer stack | (system squircle mask + system shadow) → violet ramp field → tripod legs (lavender, behind board, with occlusion shadow) → board frame (lavender-white rounded rect) → inset screen panel (purple ramp) → top knob/bar (small lavender pill above the frame) |
| Palette economy | **One** hue family (violet) doing double duty: saturated for the field, tinted-to-white for the object. No separate reserved accent — the composition is fully monochrome-tonal. Passes ≤2-hue economy easily |

## Signature devices
- **The presentation easel.** A whiteboard/screen-on-tripod object rendered front-facing — a literal, instantly-nameable depiction of "presenting." Honest subject-mining (the app annotates live presentations), and it rhymes directly with the Apple Keynote lectern/easel lineage. This is the one nameable device carrying the icon's identity.
- **Soft-plastic claymorphic render.** Rounded bevels, matte diffuse surfaces, gentle occlusion — the Big-Sur SF-Symbols-3D idiom (a tool rendered as a friendly 3D toy), not a flat glyph and not a glass layer stack.
- **Monochrome-tonal composition.** Object and field are the same violet, separated only by lightness (lavender-white object vs saturated-violet ground). Committed to tonal restraint — but see #11: it's also why the icon reads as template-default rather than distinctive.

## Failures
- **None.** No hard failures; the icon is on-language and technically clean. Three checks are **soft passes** (below) and carry the honest signal to synthesis: competent, but anonymous.

## Soft passes (flagged for synthesis)
- **#4 16px squint.** The board-on-stand gestalt survives at menu-bar size, but the inset purple screen (purple-on-purple, see #7) and the individual tripod legs smear/merge — you keep "a board on an easel," you lose all internal detail. Legible, low internal differentiation.
- **#7 Figure-ground — dominant figure passes, internal detail is weak.** The lavender-white easel frame (L≈90) vs violet field (L≈40) is a strong >3:1 contrast that survives grayscale. But the **inner screen panel** (#7A3ECD) sits on the field-adjacent purple and nearly vanishes in grayscale — a secondary element the composition can't afford to lean on. Flagged, not failed, because the carrying silhouette is the frame, not the screen.
- **#10 Variant robustness.** The light easel is background-colour-independent (would survive on a dark field), which is the good half. The bad half: this is a **Big-Sur-authored flat render**, not layered Icon Composer light/dark/mono/tinted art — the monochrome-violet scheme has no committed dark or tinted variant, and in macOS-26 tinted/clear modes the purple-on-purple internal read collapses. Passes on the glyph's independence; noted as un-authored for the current era.
- **#11 Personality.** The easel *is* a nameable device (so it passes), but the committed direction is **thin**: a stock 3D productivity object centred on a stock same-hue gradient, no secondary detail, no reserved accent, no idiosyncratic move. Template-default in the design-craft sense — it reads as "a purple productivity icon" before it reads as "Presentify."

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | pass (art inside safe zone; field bleeds to mask; no baked corner mismatch) |
| 2 | Grid adherence | pass (object optically centred, board mass balanced by tripod) |
| 3 | Silhouette | pass (easel-on-tripod instantly nameable filled solid) |
| 4 | 16px squint | soft pass (gestalt survives, internal detail smears) |
| 5 | Single light model | pass (consistent top-down, diffuse) |
| 6 | Palette economy | pass (one hue family + tints) |
| 7 | Figure-ground contrast | pass (frame L≈90 vs field L≈40, >3:1, grayscale-safe; inner screen weak — flagged) |
| 8 | Depth coherence | pass (field → tripod → frame → screen ordering; occlusion tracks top-down light) |
| 9 | Era coherence | pass (uniformly Big-Sur unified 3D-object language) |
| 10 | Variant robustness | soft pass (light glyph bg-independent; no authored dark/tinted variant) |
| 11 | Personality | soft pass (nameable device, but template-default direction) |
| 12 | No-text | pass (no words, no UI screenshot, no photo) |

**Total: 12/12, 0 failures. Three soft passes (#4, #10, #11) + an internal-contrast flag under #7.**

## Rhymes with (hint only — for icon-cluster synthesis)
- **Apple Keynote / iWork lectern-easel lineage** — a presentation-furniture object rendered front-facing on a same-hue field.
- The broad **Big-Sur single-object claymorphic** family: one soft-plastic tool centred on a light-top → dark-bottom gradient of a single hue, top-down lit, no glass. Style-family guess: **"Big-Sur monochrome-tonal single-object productivity icon."**
- Palette-family rhyme: **violet/indigo productivity gradients** (shares the exact hue register with corpus-mate Alcove's violet→magenta ramp, though Alcove inverts the light direction and drops the glyph).

## Brand-context note (cover coherence)
Cover art is a **violet gradient** field (light lavender → saturated purple) with white marketing copy over device mockups — the icon's background ramp is the same brand violet, so icon and marketing are palette-coherent (unlike split-palette marks). The product accent seen *inside* the app on the cover (an orange "This is Presentify!" annotation label, a red spotlight ring) does **not** appear in the icon — the icon commits fully to the violet identity and reserves no accent, which is coherent branding but reinforces the #11 thin-personality read: the icon shows the *stage* (easel) but none of the app's actual annotation-color energy.
