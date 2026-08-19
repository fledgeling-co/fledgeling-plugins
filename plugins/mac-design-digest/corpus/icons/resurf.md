# Icon: Resurf

- **Era:** Big Sur unified (single front-facing object, squircle, soft baked light) — **not** Liquid Glass, despite shipping in the macOS 26 window · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, SHA-1 `05212ff6`) · **App:** Resurf — "a personal library and quick-capture tool for thoughts, ideas, links, visuals" (Productivity)
- **Resolution caveat:** source is a **204×204 web render** (webp), far below the 1024 master. Facet geometry and any specular fineness are not measurable; hex values are from the 204px render (reliable to ±1 tonal step). All spatial claims `(estimated)`.

| Dimension | Reading |
|---|---|
| Background | Near-flat charcoal field `#2B2B2B`→`#2F2F2F` (reads black in the Dock); no sky-ramp, no scene. Corners sampled `#F5F5F5`/`#E3E3E3` are the page bg outside the squircle mask, not the artwork. |
| Glyph | **Monogram "R"** rendered as a **knockout** (`#2C2C2C`, same tone as the field) cut into a silver gem; geometric R with a kicked-out lower-right leg. Sits low-right of the gem's optical centre, not centred on it. |
| Overlay device | None — no diagonal tool, badge, or frame. The gem is the *substrate*, not an overlay. |
| Light model | Soft **top-left** key (canonical Big Sur is top-*down*; deviated but internally consistent). Baked gradient sheen on the gem: `#F3F3F3` top-left → `#CFCFCF` centre → `#ACACAC` lower-right. No specular hotspot, no cast shadow of note. Opaque (non-translucent) — Big Sur baked-light, **not** Liquid Glass environmental reflection. |
| Layer stack | back → front: (1) charcoal squircle field · (2) silver 3D rounded-hexagon "gem/cube" with diagonal white→silver ramp · (3) "R" knocked out of the gem, revealing/matching the field tone. |
| Palette economy | **Fully achromatic** — one neutral family, zero hue, **no saturated accent**. High figure-ground: silver gem (~`#CFCFCF`) on charcoal (~`#2B2B2B`) is well above the 3:1 floor and survives grayscale trivially (it *is* grayscale). |

## Committed direction (design-craft read)
A **committed monochrome** choice, not a template-default glyph-on-gradient: full achromatic discipline + a knockout-monogram device + dark-field inversion of the brand's airy white cover. But the **gem-on-dark-field** form language is itself a semi-template — the "soft 3D asset-pack gem" that crypto/utility startups reach for (the cover's own in-app AI critique literally calls the app's aesthetic *"a macOS asset pack or settings/utility icon set"*). Execution is committed; the underlying form is a familiar reach.
- **Adjectives:** monochrome · faceted · premium-utilitarian.
- **Subject-mining miss:** the app is a *library / quick-capture / resurfacing* tool; a gem + R communicates **brand identity**, not **function**. An icon should telegraph its subject — this one telegraphs a letterform. Nameable gap for synthesis.

## Signature devices
- **Monogram-as-knockout** — the R is cut *out* of the gem to the substrate tone, rather than sitting on top of it. Gives a "carved crystal" read and keeps the mark achromatic. `[GOLDEN-NUGGET]`
- **Isometric gem / rounded-hexagon substrate** — a single silver crystal as the field for the monogram (cover's pill mark shows the same shape faceted more explicitly; the 204px render smooths the facet fold).
- **Dark-field inversion** — black square against the brand's white-cover world; the icon is the highest-contrast expression of an otherwise airy, muted-neutral brand (coherent, deliberate contrast).

## Failures
- **#10 Variant robustness (Liquid Glass):** the R is a **knockout of the charcoal field** (`#2C2C2C` == bg). Change the background — clear, tinted, or light variant — and the letterform collapses, because the glyph *is* the background colour showing through. The icon is a fixed opaque dark-field render, not authored as adaptive Icon Composer layers, so it does not participate in the dark/clear/tinted system. **Fail.**

## Soft passes (flagged, counted as passes)
- **#2 Grid adherence:** gem fills ~70% of canvas width — reads slightly oversized vs the ~60–65% single-object Big Sur convention; margins are tight and the R sits low-right of centre rather than optically centred. `(estimated)`
- **#4 16px squint:** the object survives (silver gem + dark mark, no mud), but the **R loses its letterform at menu-bar size** — at 16px it reads as an arrow/cursor, not an "R". The gem carries recognition; the monogram does not.
- **#3 note (pass):** filled to solid black the silhouette is a clean hexagon/gem — nameable — but the R vanishes (it's figure-ground-dependent, not silhouette-bearing).

## Passing checks (evidence)
- **#1 Mask:** artwork sits inside the squircle, no corner-radius fight (cannot verify unmasked-layer delivery from a rendered PNG). **#5 Light:** one consistent top-left source. **#6 Palette:** ≤1 hue family (achromatic). **#7 Figure-ground:** silver-on-charcoal ≫3:1, grayscale-proof. **#8 Depth:** field→gem→knockout ordered sensibly, gradient does the volume work, no z-fighting. **#9 Era:** all devices are Big Sur-unified language, no mixed-era tells. **#11 Personality:** the knockout-monogram-in-gem is a nameable device beyond generic glyph-on-gradient. **#12 No-text:** single-letter monogram, no words/UI/photo.

## Rhymes with
- Crypto/web3 and "3D-utility asset-pack" gem marks (isometric crystal + monogram, achromatic or single-hue).
- Big-Sur-era single-object-on-field icons — but **stripped of colour**, which is the distinguishing move.
- (No digested peers yet — first icon in the corpus. Candidate cluster seed: **"achromatic gem monogram"** / **"premium-utility dark-field"**. Needs ≥2 more independent icons before any device promotes to canon.)
