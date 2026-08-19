# Icon: Bauhaus Clock

- **Era:** custom (flat, material-free — Braun/Max-Bill functionalist, sits outside the macOS icon-era progression) · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, 204×204 web render — see resolution caveat) · **Category:** Utility (premium clock screensaver for Mac + iOS)

| Dimension | Reading |
|---|---|
| Background | flat `#FFFFFF` (opaque, full-bleed square — no drawn squircle; relies on system mask) |
| Glyph | object — a wall-clock face. Charcoal hairline hands `#202322`→`#2E3130`; light-gray tick ring `#A2A2A2` (major ticks) with lighter minute ticks `~#B3B3B3`. Optically centred; three hands radiate from a hub near geometric centre |
| Overlay device | none |
| Light model | none — pure flat 2D vector; zero shadow, zero specular, zero gradient. Flatness by deliberate absence, not by omission |
| Layer stack | white ground → gray tick ring → charcoal hands → open center hub (charcoal ring with a white core) |
| Palette economy | monochrome only; 0 hue families, no accent — grayscale from `#FFFFFF` to `#202322`. Maximally economical |

## Signature devices
- **Braun / Max-Bill functionalist clock face** — the whole icon is a committed quotation of Dieter Rams-era product design (Braun ABW/BN wall clocks, Max Bill Junghans). This is a genuine subject-mined direction, not a template glyph-on-gradient.
- **Open-ring center hub** — the hub is a charcoal annulus with a white core dot, a real horological detail visible only above ~64px.
- **Hairline everything** — hands and tick ring are drawn at near-minimum stroke; the austerity IS the brand.
- **Full-bleed white ground with no drawn squircle** — leans entirely on the macOS mask to become a white tile; deliberate, but see Failures #10.

## Failures
- **#4 16px squint test (FAIL):** the load-bearing failure. At menu-bar/Spotlight size the `#A2A2A2` tick ring dissolves into the white ground and the hairline hands collapse to a faint gray smudge — the icon reads as a near-empty pale tile, not a clock. Detail does not degrade gracefully; it evaporates.
- **#7 figure-ground contrast (FAIL):** hands vs white measure 15.8:1 (excellent), but the tick ring — the element that makes the mark *read as a clock* — is `#A2A2A2` on `#FFFFFF` = **2.55:1**, below the 3:1 icon floor. Half the composition fails the contrast floor.
- **#10 variant robustness (FAIL):** a baked white raster with no layered/dark authoring. On a dark desktop, in Dock, or under tinted/clear mode it is an inert bright-white slab; the composition is 100% dependent on the white background surviving. The app's own cover art proves a dark variant exists in-product — it just isn't in the icon.

**Soft passes (flagged, scored as pass):**
- **#2 grid:** clock face is optically centred and the ring is concentric, but the hub sits at geometric centre with no optical nudge — acceptable for a radially symmetric glyph.
- **#3 silhouette:** filled solid, only hands + hub survive; the clock identity leans on the tick ring, which drops out entirely in pure silhouette, leaving three ambiguous radiating lines. Reads as "clock" only at full resolution with the ring present.
- **#8 depth coherence:** passes only because there is no depth at all — nothing to z-fight. N/A rather than earned.

## Dimension summary

| Check | Verdict | Evidence |
|---|---|---|
| 1 Mask discipline | pass | full-bleed white field masks cleanly to a white squircle; no baked radius |
| 2 Grid adherence | soft pass | optically centred, concentric ring; hub at geometric centre, no optical nudge |
| 3 Silhouette | soft pass | ring drops in silhouette; hands+hub alone read as ambiguous radiating lines |
| 4 16px squint | **fail** | ticks vanish, hands smear to faint gray; near-empty pale tile |
| 5 Single light model | pass | flat, no lighting — trivially consistent |
| 6 Palette economy | pass | monochrome, 0 hues, no accent |
| 7 Figure-ground | **fail** | tick ring 2.55:1 on white, below 3:1 (hands fine at 15.8:1) |
| 8 Depth coherence | soft pass | no depth to be incoherent (N/A) |
| 9 Era coherence | pass | consistently flat/monochrome/functionalist, no mixed devices |
| 10 Variant robustness | **fail** | baked white raster, no dark/tinted layer; dead on dark/tinted grounds |
| 11 Personality | pass | committed Braun/Max-Bill functionalist direction; open-ring hub |
| 12 No-text check | pass | no words/UI/photo (note: cover art clock has numerals + "IC"; the *icon* has none) |

## Rhymes with
- Flat monochrome utility marks that ignore the macOS depth/glass conventions in favour of a functionalist product-design lineage (Braun/Rams, Max Bill, Muji-adjacent).
- Minimalist clock/timer/alarm icons drawn as flat vector faces on white.
- The anti-glass, anti-depth "flat glyph on pure white" family — its virtue (austerity) and its vice (Dock-size invisibility) are the same decision.

## Notes for synthesis
- **Resolution caveat:** 204×204 web-resized `.webp`, not the 1024 master. Hairline stroke widths and hub geometry are approximate; anti-aliasing is soft. Color sampling is reliable (opaque, low compression noise): background `#FFFFFF`, hands `#202322`–`#2E3130`, ticks `#A2A2A2`.
- **Brand coherence with cover:** the cover screensaver renders a cyan-on-black dark scheme and a mint-on-cream light scheme with numerals and an "IC" wordmark. The icon carries *none* of that palette — it is grayscale only. Palette coherence between icon and product is weak: the icon commits harder to monochrome austerity than the product itself does. Not a defect per se, but the icon undersells the product's dual-scheme identity.
- **Icon vs product design gap:** the product is legibly premium; the icon's contrast/variant failures are avoidable — a darker tick ring (≥`#767676` for 3:1) and a dark-mode layer would fix #7 and #10 without touching the direction. #4 needs thicker hands + a heavier ring at small sizes.
- This is a single-app observation. Do not promote the "flat monochrome clock on white" reading to canon on one icon; hold as a style-family hint for the flat-functionalist cluster.
