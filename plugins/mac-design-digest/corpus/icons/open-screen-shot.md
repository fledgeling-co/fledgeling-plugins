# Icon: Open Screen Shot

- **Era:** Big Sur unified · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 512×512 web render — half of the 1024 master; sub-pixel edges soft, metrics `(estimated)`)
- **App:** menu-bar utility for long/scrolling screenshots (macOS 14+). One-line: *an icon that draws the macOS desktop it captures.*

| Dimension | Reading |
|---|---|
| Background | Dual-hue vertical ramp: `#3596FD` (blue, top) → `#EFEEEA` (near-white, mid) → `#F9AE6B` (warm orange, bottom). Sunrise/sunset logic, breaks Big Sur single-hue convention. |
| Glyph | `scene` — a white browser/app window (fill `#FAFBFD`) carrying macOS traffic-light dots, a four-corner crop-bracket frame, and a centred descending-dots→down-arrow mark in blue `#1C83FF`. Window is horizontally dead-centre (x-centre 255/512). |
| Overlay device | `frame` — four blue L-shaped corner brackets = the screen-capture selection marquee, quoted literally from the subject. |
| Light model | Top-down soft; ramp brightens toward a white mid-band; window casts a short soft **baked** drop-shadow downward. No specular highlights — Big Sur baked-shadow model, not Liquid Glass. |
| Layer stack | (back→front) blue→white→orange squircle ramp · baked soft drop-shadow · warm rounded-square dock strip · white window card w/ traffic-light dots · blue crop-brackets + descending dots + down-arrow. |
| Palette economy | Strained: 2 ramp hues (blue + orange) **plus** multicolour traffic-light dots (red `#F95D4A` / yellow `#F9BC22` / green `#4BC338`). Accent blue `#1C83FF` correctly reserved for the focal glyph. |

## Signature devices
- **[GOLDEN-NUGGET] "OS-in-a-box":** the icon depicts the macOS desktop itself — window chrome + traffic lights + a dock strip — instead of an abstract mark. A self-referential move: a screenshot utility drawing the thing it screenshots.
- **Crop-bracket frame:** four corner L-brackets = the capture selection marquee, pulled straight from the subject's vernacular (subject-mining, not template glyph).
- **Frozen-motion arrow:** two dots descending into a solid down-arrow reads as "capture keeps scrolling downward" — motion implied in a static glyph, the app's *long*-screenshot promise in one mark.
- **Dual-hue sunrise ramp:** blue-top → warm-orange-bottom, unusual against the single-hue Big Sur ramp convention; supplies the icon's warmth.

## Failures
- **#4 16px squint (load-bearing):** the down-arrow + dots — the *actual subject* — smear into an indistinct vertical blob at Dock/Spotlight size. What survives is a generic light window with a coloured band on top and a warm band below; it reads as "a browser window", not "a screenshot tool". The semantic payload lives in fine interior linework that does not survive downscaling.
- **#10 variant robustness (Liquid Glass):** authored as Big Sur (baked window shadow, white window fill dependent on the light ramp, multicolour traffic-light dots). It would not survive macOS 26 dark/clear/tinted glass renders — not layer-separated for Icon Composer.

## Soft passes (flagged, counted as pass)
- **#2 grid:** optical centring is carried by the window+dock *system*, not the window alone — the window sits above geometric centre (y-centre ~240) to leave room for the dock strip below. Balanced, but not a single centred glyph.
- **#3 silhouette:** filled solid, it reads as a plain "window" — the screenshot-capture meaning is entirely interior linework and vanishes. Clean silhouette, generic subject.
- **#6 palette economy:** the dual-hue ramp is already 2 families; the red/yellow/green traffic-light dots push past the ≤2-hue economy. Conventional macOS multicolour, but gratuitous decoration.

## HIG note
- Apple app-icon guidance says *don't replicate UI components*; this icon replicates a window + traffic lights + dock wholesale. Recorded as a deliberate signature (self-reference), not a defect — but it's why the icon leans skeuomorphic-literal rather than iconic.

## Rhymes with
- Literal-UI-depiction capture utilities — CleanShot X, Shottr, Xnapper: a window-in-a-squircle with a crop marquee.
- Big Sur "mini-desktop / window-on-a-sky-ramp" motif icons; distinguished here by the dual-hue (blue→orange) ramp and the descending-arrow subject mark.
- Style family for a future icon cluster: **literal-desktop utility icons** (front-facing macOS window as the glyph, baked shadow, sky ramp).
