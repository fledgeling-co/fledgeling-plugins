# Icon: Alcove

- **Era:** custom (skeuomorphic device-bezel quotation) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp`, 204×204 web render (SHA-1 `993c7f2e`). Category: Utility. App: a Dynamic-Island / notch enhancer for Mac ("An entirely new way to experience Mac").
- **Resolution caveat:** only a 204px render was available, not the 1024 master. Bezel bevel and any Icon Composer glass layering are below the resolution floor — edge treatment is `(estimated)`, not `(measured)`.

| Dimension | Reading |
|---|---|
| Background | Vertical ramp **#25126C → #522592 → #A050C1 → #E091E3 → #F7A5F8** (deep indigo-violet top → pale magenta-pink bottom), inside a near-black **#141414** beveled bezel frame |
| Glyph | None discrete — the inner field *is* the subject (abstract gradient). No object, monogram, or tool. Optically centred by symmetry; fills the safe zone edge-to-edge inside the frame |
| Overlay device | **Frame** — a thick rounded-rect black bezel surrounding a recessed inner panel (the "alcove") |
| Light model | Ambiguous two-source: faint top-edge specular on the bezel (light from top) **+** an inner field that brightens toward the bottom, reading as emitted/glowing (bottom-up). Coheres only if read as a lit screen recessed in a frame. No baked drop shadow (system supplies it) |
| Layer stack | (system squircle mask + system shadow) → black beveled bezel frame → recessed inner field (violet→pink vertical ramp) → (no glyph / no tool) |
| Palette economy | Neutral black frame + **one** hue family (violet→magenta→pink adjacent ramp). Accent saturation lives in the field itself; no separate reserved accent. Passes ≤2-hue economy |

## Signature devices
- **The framed recessed glow ("alcove").** A beveled near-black bezel wrapping a luminous inner panel — a nameable move beyond glyph-on-gradient, and a literal read of the app name (alcove = a recess) and its function (the Dynamic-Island black pill / notch nook). Subject-mining is honest here: the metaphor *is* the product.
- **Inverted glow ramp.** Light rises from the bottom edge (dark-at-top, bright-at-bottom) — the opposite of the Big-Sur "sky logic" background ramp (light-top → dark-bottom). Committed direction, not template-default.
- **Wallpaper-echo palette.** The violet→pink field mirrors the Monterey-style desktop shown glowing inside the device mockup on the app's cover — the icon quotes the screen content it overlays.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black the icon is just a rounded square (the frame is already black; the interior carries no distinct figure). No nameable object-shape; identity rests entirely on the interior color, which silhouette discards.
- **#10 Variant robustness — FAIL.** Identity is background-color-dependent with no carrying glyph. Direct evidence: the app's own cover wordmark badge renders this mark as a grayscale bezel-plus-gradient (an effective mono variant) and it collapses to a generic dark-framed tile — anonymous. In tinted/clear modes the violet identity is lost. Not authored as robust Icon Composer light/dark/mono layers (or if it is, the mono layer isn't distinctive).

## Soft passes (flagged for synthesis)
- **#1 Mask discipline.** The baked rounded-rect bezel carries its own corner radius *inside* the system squircle — a frame-within-mask that risks a subtle double-corner under the system round. Fits the mask, doesn't fight it, but the bezel duplicates work the mask already does.
- **#4 16px squint.** Survives with no detail smear (there's no fine detail to lose), but at menu-bar size it reads as "a dark tile with a purple glow" — legible yet low-differentiation; it wouldn't be told apart from any other dark-bezel gradient utility.
- **#5 Single light model.** Passes only under the "lit recessed screen" reading; strictly there are two implied sources (top-lit bezel, bottom-emitting field).
- **#9 Era coherence.** Consistent as a *custom* concept, but hybrid: a mild skeuomorphic device-bezel quotation wrapped around a flat modern gradient — belongs to no single system era.
- **#11 Personality.** The framed-glow device is nameable but thin — one gesture, no secondary detail; leans on color to do the differentiating work that silhouette (#3) can't.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | soft pass (bezel doubles mask rounding) |
| 2 | Grid adherence | pass (symmetric, safe-zone) |
| 3 | Silhouette | **FAIL** |
| 4 | 16px squint | soft pass (legible, low ID) |
| 5 | Single light model | soft pass (two implied sources) |
| 6 | Palette economy | pass |
| 7 | Figure-ground contrast | pass (bezel L≈20 vs field L≈117–199, >3:1, survives grayscale) |
| 8 | Depth coherence | pass |
| 9 | Era coherence | soft pass (custom hybrid) |
| 10 | Variant robustness | **FAIL** |
| 11 | Personality | soft pass (thin) |
| 12 | No-text | pass |

**Total: 10/12, 2 failures (#3, #10).**

## Rhymes with (hint only — for icon-cluster synthesis)
- Dark-bezel **framed-screen / framed-window** utilities (icon-anatomy's "framed-window motif"), executed as a solid recessed bezel rather than an outlined chrome.
- Notch / menu-bar / wallpaper-adjacent utilities that drop a saturated gradient inside a device frame. Style-family guess: **"dark-bezel glowing-field utility."** Palette-family rhyme: violet→magenta→pink synthwave ramps.

## Brand-context note (cover coherence)
Cover paper ground is warm cream **#FEF1DF**; the marketing wordmark badge is a **grayscale** version of this same mark (bezel #0C0A09, field #383330→#989085). So the brand runs two palettes for one mark: neutral for the wordmark lockup, violet-glow for the app icon. The violet is coherent with the product (it echoes the desktop wallpaper the app overlays), but the grayscale lockup is the live proof of the #10 mono-variant weakness.
