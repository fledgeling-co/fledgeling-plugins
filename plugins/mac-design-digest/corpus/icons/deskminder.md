# Icon: DeskMinder

- **Era:** Big Sur unified (executed in the puffy-3D / glossy indie dialect; ignores Liquid Glass) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, SHA-1 `662f6fc6`) — 420×420 web render, **not** the 1024 master. All px/hex are `(measured)` off the downscaled render; fine-detail and true-edge readings are `(estimated)`.
- **Subject fit:** the app drops a menu-bar countdown pill ("62 min · Reminder…") — the cover shows the same broken-ring gauge inside that pill, so the icon's glyph is the product's own timer mark. Icon communicates its subject cleanly.

| Dimension | Reading |
|---|---|
| Background | Vertical ramp, one green hue: `#73D768` top → `#1E7D20` bottom (sky-logic, light-at-top) `(measured)`. Interior mid ≈ `#288325`. |
| Glyph | Object/instrument — a broken gauge ring + single off-axis needle. Pale-mint tints of the *same* green: `#AFED96`→`#D8F9CA` `(measured)`. Optically centred; ring concentric with canvas, needle sweeps center→lower-left. |
| Overlay device | Diagonal tool — the needle/dart crosses the dial at a jaunty lower-left angle (Big Sur "tool at an angle" lineage, à la Clock/Stopwatch). |
| Light model | Top / top-left. Ring highlit on its upper-right arc, shadowed lower-left; needle beveled from top-left; background ramp lit top. Baked soft AO where ring meets ground and where needle meets ring. One consistent source. |
| Layer stack | (back) squircle green-ramp field + baked edge-rim highlight → gauge ring (pale 3D tube, gap at top, baked contact shadow) → needle/dart (brightest mint, puffy bevel, own baked drop shadow) (front). |
| Palette economy | One hue family (green), no second hue, **no accent**. Figure-ground rests entirely on lightness. Disciplined to the point of risk (see #7/#10). |

## Signature devices
- **Off-axis gauge needle** `[GOLDEN-NUGGET]` — a single tapered dart crossing the dial toward lower-left; the Big Sur tool-at-an-angle move, mined straight from the subject (a countdown reminder). This is the one committed personality beat.
- **Broken-ring gauge** — the dial ring opens with a gap at 12 o'clock, reading as an open countdown arc rather than a closed clock face.
- **Monochrome tonal figure-ground** — the glyph is a lighter tint of the background hue; a *committed* palette choice (real restraint), unusual for indie utilities.
- **Puffy extrusion** — ring and needle modeled as rounded 3D plastic tubes with baked bevels/AO. This is the *template-default* idiom (the look AI 3D-icon generators and iOS-3D packs reach for unprompted), riding on top of the committed palette.

## Failures
- **#10 Variant robustness (hard fail)** — the composition is a fixed raster with baked shadows/gloss and no layer separation for the system to retint; figure-ground is defined *only* by green-lightness. A tinted/mono/clear render collapses the glyph into the ground. Built for Big Sur, shipped into the Liquid Glass era. This is the load-bearing miss.

## Soft passes (flagged, counted as passes)
- **#1 Mask discipline** — squircle shape is correct, but the icon bakes its own edge-rim highlight and (in the cover) its own drop shadow; under macOS 26 HIG the system supplies mask + shadow, so baked effects risk double-treatment. Big Sur-era-acceptable, current-era deviation.
- **#3 Silhouette** — filled solid, it reads clearly as *a dial/gauge*, but the exact metaphor is ambiguous (clock? speedometer? timer? compass?). Class is legible; specific meaning is not.
- **#4 16px squint** — holds cleanly at 32px (verified on a downscaled proxy); the thin ring stroke and the 12-o'clock gap are marginal at true 16px and may smear/close.
- **#7 Figure-ground** — the needle (focal detail) clears **4.16:1** and bright ring arcs sit at **~3.3–3.8:1** `(measured)`, but shadowed ring segments drop to **~1:1** against the adjacent ground (same-hue tonal cost). The silhouette survives on the bright arcs + needle, not the whole ring.

## Clean passes
- #2 grid (optical centring, safe margins) · #5 single top light · #6 palette economy (one hue) · #8 depth coherence (bg < ring < needle, shadows track the light) · #9 era coherence (all devices Big Sur) · #11 personality (the off-axis needle) · #12 no text/photo.

## Rhymes with (hint for synthesis — not canon)
- The **monochrome-gradient-squircle utility** family: single-hue tile + a lighter same-hue instrument glyph (generic timer/clock/speedometer/gauge app icons).
- Big Sur **tool-at-an-angle** lineage (Apple Clock/Stopwatch) — but rendered in the **AI-3D / puffy-glossy** dialect rather than Apple's flatter restraint.
- Cross-note for ICONS.md (synthesis owns promotion): watch for a recurring "committed palette / template-default rendering-idiom" split — a real design decision (mono-hue) carried on a generic 3D-extrusion idiom.
