# Icon: Nox

- **Era:** Flat-transition (Yosemite–Catalina object-icon language), un-updated for Big Sur/Liquid Glass · **Rubric:** 8/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 180×180px web render — no 1024 master; detail reads soft) · **Category:** Utility
- **Subject:** adjustable display filters / therapeutic screen tints for light-sensitive Mac users. The icon communicates this literally: a monitor showing a tinted spectrum, with a crescent moon ("Nox" = Latin *night*).

| Dimension | Reading |
|---|---|
| Background | flat `#FFFFFF` field (opaque corners, alpha=255 — not transparent); soft baked drop shadow under the stand |
| Glyph | **object** — a desktop monitor on an oval-foot stand, bezel `#F3F3F3` warm-white, quoting Apple's legacy "Displays" preference icon. The screen is the canvas |
| Screen scene | diagonal spectrum bands top→bottom: mauve-taupe `#B89878` → tan-gold `#C8B060` → green `#32A84F` → slate `#708888` → deep-slate `#606878`. Reads as the app's tint/filter presets (FL-41, narrow-band green…) |
| Focal element | crescent **moon**, warm-yellow ramp `#FADA58 → #F5CC46`, sitting over the left of the scene |
| Overlay device | moon-over-scene (not a tool/badge/frame) — a foreground glyph laid on the internal band scene |
| Light model | flat top-down; subtle top highlight on bezel, warm inner-rim `#D9CEAD` at screen edge, short soft contact shadow under the oval base; no specular, no glass |
| Layer stack | white field → baked contact shadow → monitor body+stand `#F3F3F3` → spectrum band scene → crescent moon → bezel inner-rim shade |
| Palette economy | **4–5 hue families** (mauve, tan/gold, green, slate, yellow) — well over the ≤2-family floor; the rainbow is intentional (presets) but uneconomical. Warm-gold is the through-line to the brand |

## Signature devices
- **Monitor-as-canvas** — the whole icon is a screen displaying its own output, a direct quote of Apple's classic Yosemite-era *Displays* / System Preferences pane icon. [GOLDEN-NUGGET] the app's function (what your screen looks like *through* Nox) is shown by literally rendering it on a screen.
- **Diagonal spectrum bands** — subject-mining: the tint presets (clinical FL-41, 480nm notch, narrow-band green) become a striped wallpaper. Diagram-as-decoration.
- **Crescent moon = the name made visible** — "Nox" (night) rendered as the one saturated glyph; night/low-light motif.

## Failures
- **#1 Mask discipline — FAIL.** Free-form object floating on a white field with a *baked* drop shadow. Not designed for the squircle; HIG says let the system apply shadow. Under macOS 26 masking, the white becomes a squircle with wide margins and a small centred monitor → reads as a legacy, unmaintained icon.
- **#4 16px squint — FAIL.** At menu-bar/Spotlight size the monitor silhouette survives but the crescent moon and thin diagonal bands smear into a muddy multicolour smudge; the identity-carrying moon is small *within* the screen and is the first thing lost. (Judged conservatively — the 180px source is already degraded.)
- **#6 Palette economy — FAIL.** 4–5 competing hue families on the screen; the yellow accent (moon) is not reserved — the tan/gold band `#C8B060` competes with the moon in the same warm-yellow lane.
- **#10 Variant robustness — FAIL.** Not a Liquid Glass composition. The white field + white bezel collapse in dark mode; no layer separation for tinted/clear renders. No path to Default/Dark/Clear/Tinted variants without a redraw.

## Soft passes (flagged, scored as pass)
- **#2 Grid** — optically centred but the object *under-fills* the canvas; lots of white margin, object reads small. Acceptable within flat-transition norms, not within current-era mask discipline.
- **#3 Silhouette** — filled solid black it is nameable as "a monitor on a stand," but the *meaning* (moon + spectrum) lives inside the screen and vanishes in silhouette. The subject isn't readable from shape alone.
- **#7 Figure-ground** — moon holds ≥3:1 against the green and slate bands, but nearly merges with the tan-gold band `#C8B060` (both warm yellow-gold). Local contrast failure where the moon overlaps gold.

## Passes
- **#5** single flat top-down light · **#8** coherent depth order, no z-fighting · **#9** internally era-coherent (consistent flat-transition object language) · **#11** genuine personality — three nameable committed devices, not template glyph-on-gradient · **#12** no text/UI-shot/photo.

## Brand coherence (cover glance)
The site (`cover.png`) is dark-drenched: near-black ground, cream **serif** display ("Migraine screen filter for *macOS*"), brass/gold CTA and italic accent — a premium, editorial-clinical register. The icon shares only the **warm-gold hue** (moon + tan bands ↔ site brass) but diverges on everything else: light ground vs. dark, flat-illustrative vs. serif-editorial, nostalgic-utility vs. premium-clinical. The icon does not carry the brand's committed direction.

## Rhymes with
- Apple's legacy **Displays / System Preferences** pane icon (monitor showing wallpaper) — the direct ancestor of this composition.
- Flat-transition-era (Yosemite–Catalina) **free-silhouette object icons** — literal devices on transparent/white fields, before the Big Sur squircle reset.
- The "**device-showing-its-own-output**" motif (a screen/phone displaying a scene to explain a display utility).
- *(hint only — synthesis owns cluster assignment once ≥3 icons evidence this family.)*

## Notes for synthesis
- Resolution caveat: 180×180px web render, likely resized by macapp.supply; no 1024 master. Band edges and moon rim are soft — measurements are `(measured)` on this render but the render itself is low-fidelity. Treat 16px judgement as conservative-but-confident.
- This is a **shipping third-party icon**, not a mock — but it is an *un-migrated legacy icon*. Its most valuable lesson for the corpus is negative: a literal "monitor-as-canvas" object icon on a white field is exactly the pattern macOS 26 masking punishes (wide margins, baked shadow, no variant path).
- Full-bleed square but *white-field*, not glass-layered. Opaque corners confirmed (no transparency mask shipped).
