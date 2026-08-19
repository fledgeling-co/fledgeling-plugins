# Icon: Soulver

- **Era:** Big Sur unified (with a light skeuomorphic notepad quote) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 1024×1024, full-res original — SHA-1 `710aa306`). Clean render, no resize artefacts.
- **Subject fit:** Soulver is "a natural-language notepad calculator" — the icon literally builds that: a **notepad** (yellow header sheet on white paper) whose page is a **2×2 calculator keypad**, each key a domain glyph (`$` currency, `%` percent, clock time/dates, `=` math). The icon *spells the feature set*. Strong subject-to-icon communication.

| Dimension | Reading |
|---|---|
| Background | Scene/object — warm-white paper field `#F9F8F4 → #F6F6F5` (near-flat, top→bottom) with a yellow header sheet `#F8D246 → #F6CF39` occupying the top ~25% |
| Glyph | Object cluster — a 2×2 keypad of saturated rounded-rect keys, each carrying a white symbol; optically centred low in the paper field (mass sits ~8% below icon centre, pushed down by the header) |
| Overlay device | Notepad header + page-fold (a torn/folded top sheet); no diagonal-tool/badge crossing the glyph |
| Light model | Soft top-down; short soft drop shadows beneath keys and beneath each glyph; warm cast under the folded header edge; **matte, no specular** — Big Sur baked-shadow model, not Liquid Glass |
| Layer stack | (back) white paper field → yellow header sheet w/ fold shadow → four rounded-rect keys w/ soft drop shadows → white glyphs w/ micro drop shadows (front) |
| Palette economy | **5 hue families** (yellow header + red/green/purple/blue keys) + white glyphs — well over the ≤2 rule; saturation is *not* reserved for one focal element (deliberate multicolor-keypad choice, see Signature) |

## Palette (measured)

| Element | Hex |
|---|---|
| Header sheet ramp | `#F8D246` (top) → `#F6CF39` (bottom); fold-edge crease `#FAAB1D`, warm cast onto paper `#F9F0CF` |
| Paper field | `#F9F8F4` → `#F6F6F5` (warm near-white) |
| Red key | `#F44F58` (softer/pinker than system Red `#FF383C`) |
| Green key | `#45D45D` (close to system Green `#30D158`) |
| Purple key | `#AB6DD7` (lavender — softer than system Purple `#CB30E0`) |
| Blue key | `#48A4FD` (lighter than system Blue `#0088FF`) |
| Glyphs | `#FFFFFF` |

Keys read as *softened, tinted* system hues — deliberately friendlier than the raw macOS system palette.

## Signature devices

- **[GOLDEN-NUGGET] Notepad page-fold header** — the yellow top sheet is torn/folded to reveal white paper beneath (crisp `#FAAB1D` crease + soft warm shadow). This is the "natural-language *notepad*" made literal, and the only skeuomorphic move — controlled, era-consistent.
- **[GOLDEN-NUGGET] Multicolor 2×2 keypad as the glyph** — four equally-saturated hues, each a domain symbol. The rainbow *is* the brand signal ("this calculates money, percentages, time, and math"), the same logic Apple's own Calculator/Numbers icons use. It breaks palette economy on purpose.
- **Domain-glyph storytelling** — `$ / % / clock / =` narrate the app's four calculation domains in one glance; no other icon in a keypad grid needs to.
- **Concentric mask-echo corner** — the bottom-right (blue `=`) key's *outer* corner radius is enlarged to nest inside the squircle mask, so the keypad feels fitted to the icon rather than pasted on. Quiet, expensive detail.

## Failures

- **#6 Palette economy — FAIL (purposeful).** 5 hue families, no single reserved accent; every key equally saturated. By the letter of the ≤2-hue rule this fails — but it's a *systematic, subject-driven signature* (multicolor keypad = the app's multi-domain calc), not sloppiness. Record as signature-over-defect; still counts against the score honestly.
- **#10 Variant robustness (Liquid Glass) — FAIL.** Not authored for Liquid Glass. The whole meaning rides on (a) the white paper background and (b) four *distinct* key colours; under tinted/mono/clear rendering the keys collapse to four identical blobs and the paper field loses its ground. A future Tahoe/Liquid-Glass redraw would need to re-solve the color-coding.

## Soft passes (flagged, scored as pass)

- **#3 Silhouette — soft pass.** Filled solid black it's a plain squircle (full-bleed); the subject is carried by internal colour blocks + fold, not a free silhouette. Nameable in *grayscale* as "keypad on a notepad," not from pure silhouette. Typical of full-bleed Big Sur icons; leans entirely on colour.
- **#4 16px squint — soft pass.** At 16px the yellow-header + 2×2 colour-block gestalt survives and is distinctive, but the four glyphs (`$/%/clock/=`) smear to unreadable blobs. Communicates "colourful calculator" by colour, not by glyph; glyphs become legible ~32px+.

## Passing checks (evidence)

- #1 Mask discipline — full-bleed inside the mask; bottom-right key corner made concentric with the squircle (embraces, not fights, the mask).
- #2 Grid adherence — balanced 2×2 grid; minor low bias from the header (soft).
- #5 Single light model — all shadows fall down/soft from one top-down source.
- #7 Figure-ground — saturated keys on warm-white (high contrast); white glyphs on saturated keys (>3:1). Grayscale note: the four key *colours* collapse to similar mid-values, but glyph legibility holds.
- #8 Depth coherence — sensible plane order, no z-fighting, shadows track the light.
- #9 Era coherence — all-Big-Sur language with a controlled skeuomorphic notepad quote; no mixed-era tells. (Not yet updated to Liquid Glass — a currency observation, not a defect.)
- #11 Personality — four nameable devices (above); far beyond generic glyph-on-gradient. This is where the icon earns its keep.
- #12 No-text — no words; `$ % =` are math symbols, clock is an object, no photo/UI-screenshot.

## Rhymes with

- **Big Sur multicolor-utility family** — front-facing squircle carrying a saturated multi-hue element on a paper/neutral field. Peers: Apple **Calculator** and **Numbers** (multicolor grids), Apple **Notes**/Stickies (yellow-paper header). Style-cluster hint only — needs ≥3 independent icons before any canon.

## Notes for synthesis

- **Source caveat:** `cover.webp` in the source folder is a **mismatch** — it depicts "Supaste / Clipboard history" (a different app), not Soulver. Could not assess icon-to-app palette coherence from the cover. Icon itself is a clean full-res original.
- The softened-system-hue observation (keys are tinted-friendlier versions of macOS system colours) is worth watching across other multicolor icons — possible recurring device.
