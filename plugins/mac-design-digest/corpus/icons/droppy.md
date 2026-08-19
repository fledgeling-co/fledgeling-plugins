# Icon: Droppy

- **Era:** custom (device-portrait borrowing Liquid-Glass specular language, Big-Sur baked-effect authoring) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/droppy/icon.png`, 1024×1024, transparent squircle corners — full native resolution, not a web resize)
- **App does:** turns the Mac notch into a productivity hub for files/clipboard/extensions — the icon depicts that subject literally.

| Dimension | Reading |
|---|---|
| Background | Black device bezel filling the squircle, `#010101→#070707` (measured), with a mild top-down bevel highlight (top outer edge `#3E3E3E` vs bottom `#222222`) — a framed **object**, not a gradient field |
| Glyph | No glyph. The subject is a rendered **object**: a front-on backlit screen. Optically centred, symmetric, fills the safe zone; a **MacBook notch** (black tab, ~x400–620, centred) cut into the top inner edge |
| Overlay device | **Frame** — the heavy black bezel wraps the screen (framed-window / device motif); the notch is the signature break in the frame |
| Light model | **Emissive backlit screen**: cyan inner-rim glow brightest at the screen edges (`#ABD6F7` measured), an hourglass/pinched specular bloom — bright lobes upper (`#5EAAE7`) and lower (`#4084C0`) meeting a dark navy waist at centre (`#08376E`). A second, milder top-down bevel on the black frame. Reads as a lit glass display inside a dark device |
| Layer stack | back→front: (1) black device bezel/frame, baked bevel + inner shadow → (2) notched inner-screen recess → (3) blue vertical gradient field `#08376E→#3C99E9` → (4) cyan inner-rim light glow `#ABD6F7` → (5) hourglass specular bloom |
| Palette economy | One hue family (blue, deep navy → cyan-white) + neutral black frame; accent = the cyan rim-light. Clean 2-family economy. Grayscale hierarchy survives (bright centre, dark frame) |

## Palette (measured)
- **Frame:** `#010101` → `#070707` (near-black), bevel highlight to `#3E3E3E`
- **Screen ramp:** waist `#08376E` / `#093B73` → mid `#1E61A4` / `#2876B9` → specular lobes `#3C99E9` / `#5EAAE7` / `#4084C0`
- **Accent / rim-light:** `#ABD6F7` (cyan-white inner-edge glow)

## Signature devices
- **[GOLDEN-NUGGET] Notch-as-subject** — the literal MacBook notch cut into the top of the screen. The whole product concept (a notch productivity hub) compressed into one shape. Textbook subject-mining: the icon could belong to no other app.
- **Device portrait** — the icon *is* a front-on rendering of a screen-in-a-frame, not the Big-Sur convention of a glyph-on-gradient. Rare, committed composition.
- **Backlit glass screen** — inner rim-light + hourglass specular make the flat blue field read as an emissive, glassy display.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black, the icon collapses to a featureless squircle; the notch tab is the only cue and it is tiny. All meaning lives in the blue-on-black *tonal* figure-ground, not in shape. An object icon with no exportable silhouette.
- **#10 Variant robustness — FAIL.** A single baked raster with baked bevel/rim/specular (HIG says the *system* should apply these) — no authored Default/Dark/Clear/Tinted layer story. The black bezel is dark-mode-fragile: against a dark Dock/wallpaper its outer edge dissolves, and there is no path to a legible tinted/mono render.

### Soft passes (flagged, scored as passes)
- **#1 Mask** — respects the mask outline (no protrusions), but bakes an inner-frame bevel + drop-shadow that duplicates the system treatment.
- **#4 16px squint** — survives as a clean blue tile in a dark frame with no detail smear (little detail to lose), but its *identity* does not survive: the notch vanishes and it reads as a generic glowing-blue app tile.
- **#5 Single light model** — dominant read (emissive screen) is coherent, but the frame bevel adds a mild second, top-down cue.
- **#9 Era coherence** — commits to "lit screen in a dark device," yet mixes vocabularies: Big-Sur baked-bevel depth + Liquid-Glass specular/translucency. Hence the *custom* classification rather than either system era.

## Rhymes with
- Notch/menu-bar utility icons that portray the Mac hardware itself (the NotchNook / Boring-Notch family of black-panel-at-the-top motifs) — device-literal rather than glyph-abstract.
- Glossy blue-gradient utility tiles with a rim-lit glass screen. Provisional style-family hint only (single icon so far): **"glossy blue-gradient device-frame utility."** Needs ≥2 more device-portrait icons before any cluster is real.

## Cross-icon / brand notes
- **Icon↔cover coherence:** the through-line is the *notch / black-rounded-panel* motif (cover shows a Dynamic-Island-style black media panel over a wavy wallpaper), not a shared accent hue — the icon is saturated blue, the cover is neutral-black UI over photographic tones. Motif-coherent, palette-divergent.
- **For synthesis:** first "device-portrait" and first "notch-as-subject" entry in the corpus. Do not promote — single app. The baked-effects / no-variant-story issue and the dark-mode-fragile black frame are worth watching as a recurring indie anti-pattern if more baked-raster icons arrive.
