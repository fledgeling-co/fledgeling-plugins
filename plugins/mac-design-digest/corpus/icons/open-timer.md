# Icon: Open Timer

- **Era:** Skeuomorphic-quote (photoreal object) framed on a Big-Sur squircle · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/open-timer/icon.png`) · **App:** Open Timer — "native macOS menu-bar time tracker for freelancers" (Productivity)
- **Resolution caveat:** delivered as a **584×554 non-square PNG** with transparent corners — NOT the 1024² master. It is a resized web render; fine detail (tick marks, brushed-metal grain, blueprint linework) is already softened by downscaling, and the slightly-wider-than-tall frame means the true squircle geometry and mask fit can't be measured. All hexes `(measured)` from this render, treat ±3 per channel.

| Dimension | Reading |
|---|---|
| Background | Blue field, ramp `#3179BB` (top) → `#214984` (lower-left), lighter fall-off to `#66A2D8` lower-right; overlaid with a lighter `#72B6E7` **blueprint grid** (concentric circles + rectilinear rule lines + diagonal corner guides) |
| Glyph | **Object, not glyph** — a photoreal brushed-steel wristwatch/chronograph, front-facing with slight top-down perspective. Optically centred, sized large (case nearly reaches left/right safe margins). Steel bezel `#D7DCDF`→`#B1B7BB`; silver dial `#DDE1E5`; white hands + an **"F" monogram** on the dial `#EDEFF1` |
| Overlay device | None crossing the mask; instead an **emissive teal timer-ring** ( `#69BABE`→`#5EA7AD`, tick-marked) wraps the dial, and a **winding crown** nub sits on the right edge |
| Light model | Single top-down key: specular hotspots on the steel bezel crown, soft occlusion shadow beneath the case onto the field. Second, *material* light source: the teal glass ring is self-illuminated (emissive/backlit). Drop shadow under the case is soft and moderately long — heavier than a mac-native baked micro-shadow |
| Layer stack | blue gradient field → blueprint grid linework → brushed-steel squircle watch-case → emissive teal timer-ring w/ ticks → silver dial + "F" monogram → hour/minute hands → winding crown |
| Palette economy | 2 hue families (blue field, teal accent — both cool/adjacent) + neutral steel. Teal correctly reserved for the focal ring. Economical for how ornate it looks |

## Signature devices
- **Chronograph-in-a-squircle** — the watch *case itself* is a rounded-square whose silhouette rhymes with the app-icon squircle; the object and its container share a shape. `[GOLDEN-NUGGET]`
- **Emissive teal timer-ring** — a backlit mint/teal glass band with tick marks around the dial; the icon's one saturated moment and its only literal nod to "timer" vs "watch."
- **Blueprint-grid technical field** — concentric circles + rule lines + diagonal guides behind the object, quoting engineering-drawing paper. This is the tell of the current **generative-icon house style** (photoreal hero object floated on a blueprint squircle).
- **Winding crown breaking the right margin** — a small skeuomorphic detail that pushes the object off perfect centre.
- **"F" monogram on the dial** — a committed brand device, but see Failures: it does not match the app name "Open Timer."

## Failures
- **#4 16px squint test — FAIL.** Tick marks, brushed-metal grain, blueprint linework, the teal ring, and the "F" all collapse into noise at menu-bar/Spotlight size; only a pale silver disc on a blue square survives. It reads "a clock," but every device that gives it character is Dock-invisible.
- **#9 Era coherence — FAIL.** A photoreal, heavily-textured skeuomorphic watch (a 2010–2013 iOS-clock visual language) is composited over a flat vector blueprint grid (a 2020s generative-flat language) inside a Big-Sur squircle. Three eras' languages share one frame — nameable tension, not one voice.
- **#10 Variant robustness — FAIL.** A single baked raster with no layer separation, baked bevels/specular/shadow, and a hard-coded blue field. There is no mono/tinted/clear path; in macOS 26 tinted or dark-glass modes this cannot recompose. It is not a Liquid Glass layered icon — it fights HIG's "provide unmasked layers, let the system apply effects."

### Soft passes (scored pass, flagged for synthesis)
- **#1 Mask** — blue field bleeds to a clean squircle, but the whole icon bakes in effects HIG says the system should apply.
- **#2 Grid** — optically centred, but the case is oversized (near the L/R safe margins) and the crown pushes it right.
- **#3 Silhouette** — a rounded-square case + crown nub reads "watch/clock," but the case blob is generic; nothing says "menu bar" or "tracker."
- **#8 Depth** — coherent stack, but the case drop-shadow is softer/longer than a mac baked micro-shadow, drifting toward web-graphic.
- **#12 No-text** — passes (no words) but the **"F" monogram is a letterform mismatched to "Open Timer"** — subject-communication miss (freelance-F? a foundry mark? unclear), and letterforms in icons are risky.

## Subject & brand-coherence notes
- **Subject overshoot.** The app is a lightweight flat menu-bar utility (see `cover.png`: an electric-blue neo-grotesque hero + a dark flat timer card with a `#2E7BFF` pause button). The icon depicts an ornate luxury *wristwatch*. It communicates "time" but overshoots into "premium horology" and says nothing about menu-bar / tracking / lightness.
- **Palette coheres, personality doesn't.** Icon blue and cover blue are the same hue family, so the brand *colour* is consistent — but the cover carries no teal, and the icon's photoreal-kitsch register is divorced from the product's clean flat-modern UI. Icon-vs-product personality mismatch.

## Adjectives (committed direction, honestly named)
Ornate · metallic · blueprinted — a maximalist, photoreal, over-rendered direction, the opposite of mac-native restraint.

## Rhymes with
- The current **AI/generative-icon house style**: a photoreal hero object floated on a blueprint-grid squircle with baked specular and a saturated accent ring (a Midjourney/Icon-generator signature). *Hint for synthesis — needs ≥2 more members before this becomes an icon cluster.*
- Quotes early-iOS **skeuomorphic clock/watch app icons** (the original iOS Clock, luxury-watch utilities) — the photoreal-timepiece lineage.
