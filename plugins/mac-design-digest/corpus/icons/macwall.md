# Icon: MacWall

- **Era:** Big Sur unified · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, SHA-1 `5adee9e1`) · **Category:** Utility (cinematic live wallpaper) · app: macwall.app

> Resolution caveat: source is a **192×192 web render** with the squircle already baked in as **alpha-transparent corners** (a=0) — not the 1024 master. Region-level hex is reliable; sub-pixel edge treatments (specular, snow micro-texture, shadow softness) are read from a 4× upscale and are `(estimated)`. Cannot confirm whether the master ships full-bleed square or pre-masked.

| Dimension | Reading |
|---|---|
| Background | Near-white cool **ramp #FDFEFE→#E7F3FE** (`estimated`) — almost flat; pure-white crown cooling to faint ice-blue at the base where clouds sit. Fills to the mask edge. |
| Glyph | **Scene** (illustrated landscape): triple snow-capped peak in slate-navy (`#2A334C`, `#343F59`), snow caps `#F8FCFE`, mid-tone rock `#B0B7C4`; a rising red-sun disc behind; a cloud bank in front. Optically centred horizontally; composition is bottom-weighted (busy base, empty white crown). |
| Overlay device | **none** — no diagonal tool, badge, or frame; it is a self-contained vignette. |
| Light model | Soft ambient upper light; snow highlights fall on the **right/upper** peak faces; a warm orange sun-glow (`#F8593E`) blooms where the red disc meets the ridgeline; short, soft baked shadows; no hard specular. |
| Layer stack | white/ice-blue field → red sun disc (internal red→warm-orange ramp) → snow-capped slate-navy massif → cloud bank (front-most, occluding the peak bases) |
| Palette economy | **2 hue families** — saturated red (sun) + cool slate-blue (mountain/cloud/field) + white. Accent saturation reserved entirely for the focal sun; disciplined. |

## Signature devices
- **Rising red-sun disc as backlight** — a single saturated red circle (`#F91715`) behind the peaks; the icon's only accent and its entire personality budget spent in one move.
- **Ukiyo-e / Hokusai-Fuji quotation** — red-sun-behind-snow-peak is the Japanese woodblock / rising-sun motif; a deliberate cultural reference, not a generic mountain.
- **Cotton cloud-bank base** — soft white clouds (`#EDF6FE` / `#E3EBF6` shadow) wrap the mountain feet, anchor the composition, and hide the peak/ground seam.
- **Near-invisible cool field ramp** — the white→ice-blue vertical ramp reads as flat but supplies just enough atmosphere to seat the clouds.

## Failures
- **#10 Variant robustness (Liquid Glass):** authored as a **single light appearance** whose whole read depends on the **white background**. It is not a layered Icon Composer composition — pale clouds and the cool field would collapse under dark / clear / tinted renders on macOS 26 Tahoe. This is the canonical Big-Sur-era icon miss on the new platform.

## Soft passes (flagged, scored as passes)
- **#2 Grid:** optically centred but **bottom-heavy** — busy cloud/mountain base against an empty white crown pushes the visual centre of mass low.
- **#4 16px squint:** the **sun-over-mountain gestalt survives** but three-peak separation and cloud detail smear into one dark lump under a red blob; snow modelling is lost.
- **#5 Light model:** mild narrative tension — the sun sits *behind* the peaks (backlight) yet snow faces are **front/right-lit**; reads naturally but is not physically consistent.

## Brand-context note
Icon (cool white + red + slate scene) and the marketing cover (**warm-cream editorial** ground, dark-olive/espresso serif type, B&W laptop photo) do **not** share a palette family — the app's icon and its brand system diverge. Flag for synthesis if MacWall's UI is later digested.

## Rhymes with
- Illustrated-scene-on-white **nature/weather** utility icons (soft-3D-gradient Big Sur illustration idiom).
- Landscape-vignette icons where the whole tile is a self-contained scene rather than a glyph-on-field.
- The **red-sun / Fuji** motif family — icons quoting Japanese woodblock imagery.
- *(No prior corpus icons to compare — first icon digested; peers are external references pending more digests.)*
