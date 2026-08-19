# Icon: Room Service

- **Era:** Liquid Glass (baked 3D pre-render quotation) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (Dev) · **Master:** clean native 1024×1024 PNG — no upscale smear, values below are reliable `(measured)`
- **App does:** dev disk-cleanup / project-health utility (Health Check, Space Map, Clean Up, recurring routines, local servers). See subject note under Failures — the icon communicates none of this.

| Dimension | Reading |
|---|---|
| Background | flat `#08060E` — violet-tinted near-black, perfectly uniform (no vignette, no gradient) `(measured)` |
| Glyph | abstract 3D glass ring / torus, seen at a slight tilt; dead-centered (bbox 834×842 at center 509,511; ~9% margins all sides); graphite ramp `#FEFEFA → #BBBFC8 → #787F8C → #50545F → #272A33 → #1B1E27`, light-at-top |
| Overlay device | none |
| Light model | single key from top / upper-left; top-down glass logic; razor specular on the upper rim (`#FEFEFA`); short soft drop shadow lower-left; body gradient light-at-top → dark-at-bottom `(measured)` |
| Layer stack | violet-black field → soft contact shadow (lower-left) → extruded glass torus body → top-rim specular; the center aperture is a cutout revealing the field |
| Palette economy | ~0 hue families — monochrome cool-graphite glass on violet-black; **no chroma accent** |

## Signature devices
- **Backlit glass washer** — a 3D-extruded translucent ring rendered at a slight perspective tilt (elliptical, not front-facing), with visible band thickness. This is the whole icon.
- **Razor top-rim specular** — a near-white `#FEFEFA` highlight tracing only the upper edge; the single brightest event, doing most of the silhouette work.
- **Hole = ground** — the center aperture is the *exact* background colour (`#08060E`), so the ring reads as a portal cut into the black field rather than a solid disc.
- **Monochrome-on-violet-black** — a committed, chroma-free glass direction; austere and premium.

## Failures
- **#7 figure-ground contrast** — the lower ring body (`#1B1E27`, 27/30/39) against the ground (`#08060E`, 8/6/14) is ≈**1.2:1**, well under the 3:1 floor. The bottom arc dissolves into the field; in grayscale the silhouette is carried almost entirely by the top specular and the two side lobes. Top-weighted, not a clean closed loop.
- **#10 variant robustness (Liquid Glass)** — shipped as a single flattened, dark-committed PNG. The composition *depends* on the black ground: the aperture is background-coloured and the graphite body needs black behind it to read. It is not authored as separable Icon Composer layers, so it would not survive system light / clear / tinted re-renders. Dark-mode-first by construction.

## Soft passes (scored as pass, flagged)
- **#4 16px squint** — the ring shape survives, but as the low-contrast bottom fades it degrades to a top-weighted bright **arc** (reads closer to a "C" than a closed "O") at menu-bar / Spotlight size. Passes on shape recognition; loses closure.
- **#9 era coherence** — every device is Liquid-Glass vocabulary (translucency, specular, refractive gradient), but it is a **baked 3D pre-render** quoting the material — specular highlights are baked in, which HIG says to leave to the system. Internally consistent (one era's language), so a pass, but it's a *rendered quotation* of Liquid Glass, not a system-composed icon.

## Passes worth naming
- **#1 mask** clean (full-bleed dark field, artwork inside safe zone, no baked corner radius). **#2 grid** clean (optically dead-centered, ~9% margins). **#5 single light model** (one top/upper-left key throughout). **#6 palette economy** (exemplary — zero chroma, one graphite ramp). **#8 depth** coherent (field → shadow → body → specular, no z-fighting). **#11 personality** — a committed, nameable device (the backlit glass washer) beyond generic glyph-on-gradient. **#12 no-text** clean.

## Brand-context note (vs cover)
- The app UI (cover.png, 3894×2352) is a dark near-black dashboard whose **primary accent is orange** (`~#F59E0B` score ring + "Needs attention" badges) with multi-hue semantic status dots. The icon shares only the dark ground — it **drops the orange brand identity entirely** and carries no chroma. Coherence is partial: same darkness, none of the app's signature colour. The icon reads as generic premium-glass, not specifically "Room Service."

## Rhymes with
- The current **3D-glass-render icon family** — Spline/Blender translucent single-object forms on black (glass rings, loops, knots, blobs) that the current indie/AI-tool wave reaches for. Also rhymes with Apple's own Liquid Glass demo forms.
- *Hint only (synthesis owns clustering):* candidate "monochrome glass-object on near-black" cluster — trend-committed, subject-mute abstract glass. Needs ≥2 more members before it's a cluster.
