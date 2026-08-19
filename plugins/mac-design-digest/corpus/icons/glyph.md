# Icon: Glyph

- **Era:** Big Sur unified (with a skeuomorphic dot-matrix-display quotation) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/glyph/icon.png`, 512×512 PNG render, SHA-1 `31d3bbbd`) · **Subject:** markdown notes app for Mac
- **One-line read:** the markdown asterisk (`*`), tripled in a primary-color triad, inset into a dark LED-display strip on a clean white squircle — subject-literal and mechanical, but the metaphor points at "password / rating" as easily as "writing".

| Dimension | Reading |
|---|---|
| Background | Near-flat white squircle; faint top-down tonal shade `#FDFDFD → #FFFFFF (center) → #E5E6E6 (lower)` (measured, 512px render) — reads flat |
| Glyph | Three 6-armed asterisks (`*`), abstract typographic marks; blue `#3B88FF` / red `#EF4B46` / orange `#F5953F` (measured, peaks `#3A89FF`/`#F74F49`/`#FD9B46`); sit centred on the dark plate |
| Overlay device | Dark rounded-rect **display plate** (`#1A1A1A` body, `#2B2B2B` rim, ~`#333` grille dots) with a perforated dot-matrix/grille texture — a frame/screen holding the glyphs |
| Light model | Soft top-down key light, matte finish; plate carries a faint top rim-light and a short soft baked drop shadow onto the white field; asterisks flat-filled with slight vertical brightening. No specular/glass |
| Layer stack | (back→front) off-white squircle field → soft baked drop shadow → dark dot-matrix display plate → three primary-colored asterisk glyphs |
| Palette economy | 2 neutral grounds (white field, near-black plate) + **3** saturated glyph hues (blue/red/orange); accent confined to the focal glyphs but spread across 3 families — no single hero hue |

## Signature devices
- **[GOLDEN-NUGGET] Dot-matrix display plate** — a perforated LED-sign / mechanical-keycap-strip / speaker-grille texture inset into an otherwise flat Big Sur icon. A deliberate, self-consistent skeuomorphic material quotation; it is the icon's mechanical character in one move.
- **[GOLDEN-NUGGET] Markdown asterisk as literal subject** — `*` is the actual markdown emphasis token; three of them nods at `***bold-italic***`. Textbook subject-mining (the app's own vernacular becomes the mark) — but see the mismatch below.
- **Primary color triad as syntax highlighting** — blue/red/orange read like colored code/markdown tokens on a dark editor pane. Distinctive, but no colour owns the brand.
- **Glyphs-on-an-inset-screen framing** — the mark lives on a screen *within* the icon, weight settled low like a nameplate.

## Failures
- **#10 Variant robustness (Liquid Glass era):** the figure is **white-field-dependent** — the near-black plate only reads because it sits on a bright ground; in a dark/tinted render the black-on-dark figure loses separation. Worse, **tinted/mono rendering collapses the blue/red/orange triad**, which is the entire personality — the three glyphs become one flat value. Authored as a Big Sur object icon, not as appearance-aware Icon Composer layers.

## Soft passes (flagged, scored as pass)
- **#2 Grid:** horizontally centred but the plate sits low (centre ~65% down the canvas); the upper ~55% is empty field. Deliberate nameplate framing, but optical weight is low and the top half does no work.
- **#3 Silhouette:** the shape is crisp and nameable — *but as the wrong thing.* Filled solid, three asterisks on a bar read as a **password field** (`***` = masked characters) or a **star rating**, not writing/markdown. The subject is legible only to viewers who already know markdown syntax. This is the single most valuable learning here.
- **#4 16px squint:** survives as a dark bar with three colored dots; the asterisk arms and the grille texture smear below ~64px, so the **color triad carries recognition** and the grille detail is wasted at Dock/Spotlight size.
- **#6 Palette economy:** 3 saturated hue families exceed the ≤2 rule. Confined to the focal glyphs and clearly intentional (systematic + purposeful → signature, not defect per the defect/signature test), so scored a pass — but there is no single hero hue.
- **#9 Era coherence:** flat Big Sur field + skeuomorphic dot-matrix texture is a mixed language, but it is one consistent plate quoting one older era — a quotation, not a clash.

## Passes (no flag)
- **#1 Mask:** clean squircle, ~6% margin (bbox 33–479 of 512); no corner-radius mismatch. (Baked squircle art on a transparent PNG rather than full-bleed square + system mask — typical of a shipping/exported render.)
- **#5 Single light model:** one soft top-down source throughout.
- **#7 Figure-ground:** bright glyphs on near-black plate ≫ 3:1; near-black plate on white ≫ 3:1; survives grayscale (orange > red > blue by value).
- **#8 Depth coherence:** planes ordered sensibly, drop shadow consistent with the light, no z-fighting.
- **#11 Personality:** well above generic glyph-on-gradient — three nameable devices.
- **#12 No-text:** symbols only; no words, UI, or photography.

## Rhymes with (hint for synthesis)
- Big Sur "object-on-white" icons that inset a **dark screen/display panel** — developer/terminal/calculator/keycap-quoting family (colored-glyph-on-black-display). NOT the warm-editorial family and NOT the single-hero-hue product family.
- Cross-context note: the app's **website** brand leans **purple** (`~#7C3AED` "M↓" markdown badge) with an orange "notes" badge; the icon shares only the orange (icon orange asterisk ≈ site "notes" badge) and drops the purple entirely. Icon and site do not share a hero hue — a palette-coherence gap worth watching if more of this app's surfaces are digested.

## Notes / caveats
- **Resolution honesty:** this is a **512×512** render (half the 1024 master). The dot-matrix grille dots sit near the render's resolution floor; they read cleanly here but 1024 crispness cannot be judged from this file. Treat all hex as `(measured)` off a downscaled web export.
- Single icon — no promotions. Feeds ICONS.md era distribution (Big Sur + skeuo-quotation), the "dark inset display panel" device candidate, and the "subject-literal glyph whose metaphor mismatches its category" cautionary pattern.
