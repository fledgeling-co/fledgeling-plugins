# Icon: LookAway

- **Era:** Liquid Glass (visual language) — but a *baked raster quotation*, not Icon Composer-authored · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/lookaway/icon.png`, 256×256 web render — downsized, likely from 1024) · **Category:** Productivity (eye-break / rest-your-eyes utility)
- **Subject the icon must communicate:** the app schedules screen breaks so your eyes rest — the icon shows a serene, closed-eyes face (eyes "looking away" / at rest). Subject-mining is on the nose and works.

| Dimension | Reading |
|---|---|
| Background | Near-flat black field, `#000000` → `#151515` (a faint ambient glow lifts the black directly under the blob). No sky-ramp; the field is a dark stage, not a gradient. |
| Glyph | Abstract emissive "orb-face": a single luminous rounded blob bearing two upturned `‿ ‿` arcs (closed, content eyes). Optically centred, biased ~8% above true centre; safe-zone margins clean. Diagonal internal ramp — magenta-pink lower-left → coral → peach/gold upper-right. Eyes near-black `#0C0905`/`#1C140B` as negative-space cutouts. |
| Overlay device | None. No diagonal tool, badge, or frame — the eyes are part of the glyph, not an overlay. |
| Light model | Single warm environmental light from upper-right. A bronze/gold specular rim catches the top squircle edge (brightest upper-right, `#634E30`); the blob's lightest zone (peach) sits upper-right, its pink mass lower-left — consistent. Core reads *emissive* (self-luminous gradient) rather than lit; soft ambient bloom beneath, no hard cast shadow. |
| Layer stack | black field → ambient under-glow (blob bloom onto field) → luminous pink→peach emissive blob → dark eye-arcs (negative detail); + a warm specular rim baked onto the squircle edge. |
| Palette economy | Two adjacent warm hue families (pink + amber) as one diagonal ramp, on a black field, with same-family gold rim. ≤2 hues, disciplined. The blob *is* the accent — no separate saturated spot. |

## Signature devices
- **[GOLDEN-NUGGET] Closed-eyes rest-face** — two upturned arcs read instantly as peaceful/sleeping eyes; a literal, warm depiction of "look away and rest." The app's entire promise in two strokes.
- **Emissive gradient orb** — a self-luminous pink→peach pebble glowing on black with no outline; the wellness/meditation-icon idiom (glow, not object).
- **Warm specular rim** — one bronze/gold light-catch along the top edge, the sole nod to a lit glass environment; everything else is emissive.
- **Dark-field figure-ground** — glow-on-black instead of the Big-Sur light-field convention; the icon lives on luminance contrast, not contour.

## Failures
- **#3 Silhouette test — FAIL (recovers under luminance).** Filled solid black, the contour is an un-nameable rounded pebble and the eyes (also dark) merge away — the identity lives entirely in *interior negative-space* eye-arcs, not the outer shape. It *does* survive a grayscale luminance threshold and the 16px squint (strong blob-on-black figure-ground), so it wins at the Dock by contrast, not by silhouette. This is the design's defining tradeoff, not a careless miss.

## Soft passes (flagged)
- **#1 Mask discipline (soft).** Reads squircle-native and stays inside the safe zone, but the artwork bakes in its own gold specular rim and is delivered as the *pre-masked* appearance (edge outline included) rather than a full-bleed square for the system to mask — against HIG "provide unmasked square layers; let the system apply specular." Corner reads as a continuous-rounded superellipse, slightly rounder than a classic Big Sur squircle (macOS 26 rounder mask, or iOS-style delivery).
- **#10 Variant robustness (soft).** The *composition* would survive tint/mono — meaning rides the eye-arcs + blob shape, not the pink specifically — but as a baked raster it ships no true Icon Composer default/dark/clear/tinted variants; the brand pink→peach ramp would simply be lost in a tinted render with nothing to regenerate it.

Passes: #2 grid, #4 16px squint (eye-arcs still legible small), #5 single light, #6 palette economy, #7 figure-ground contrast (blob-on-black ≫3:1, survives grayscale), #8 depth coherence, #9 era coherence, #11 personality (strong), #12 no-text.

## Rhymes with
- **Style family (hint):** dark-field emissive-orb wellness/mindfulness icons — glowing gradient blob on black, meaning carried by glow + a minimal face. Rhymes with meditation/breathing/AI-assistant "orb" icons (Endel/Calm-adjacent, Oura-dark) more than with any productivity-tool icon. First icon in the corpus — cluster unconfirmed; flag as a candidate "emissive-orb / soft-wellness" icon cluster for synthesis to confirm against ≥2 more.
- **Brand coherence note:** palette matches the cover exactly — the cover's timer-notification glyph reuses the same magenta→gold ramp. Icon and app-context share one warm gradient identity.
