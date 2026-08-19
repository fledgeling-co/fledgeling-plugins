# Icon: SpacePeek

- **Era:** Big Sur unified (baked-light) — glass-curious hybrid · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 512×512, `2c54338a`) · **Category:** Utility (disk-usage / Finder space visualiser)

| Dimension | Reading |
|---|---|
| Background | ramp #97C3FC → #5C68F7, top-light periwinkle → bottom indigo, slight diagonal (lightest top-left, coolest bottom-right) — sky logic, one blue hue family (estimated) |
| Glyph | object-scene: translucent folder + segmented disk-usage donut + glass magnifier. Ring optically ~10px above geometric centre; magnifier handle weights bottom-right so the cluster balances (estimated) |
| Overlay device | diagonal tool — glass magnifier handle crossing to the bottom-right corner, with the donut ring doubling as its lens (Preview/Loupe lineage) |
| Light model | top-down soft; baked specular on ring rim + magnifier glass; short soft contact shadows under ring and folder. One consistent direction (upper-left). Specular is *baked*, not system-deferred (Big Sur convention, not Liquid Glass) |
| Layer stack | bg ramp → translucent folder (body + top tab) → multicolor segmented ring → glass magnifier handle (+ baked micro-shadows between each) |
| Palette economy | 1 background hue family (blue) + a 6-hue meaningful multicolor ring (#E8F1FE / #4088FC / #886CFC / #FEC541 / #43E0B7 / #63E7FC). No single accent — the ring *is* the accent, multicolour by data-metaphor intent |

## Signature devices
- **Ring-as-lens (the whole idea in one shape):** the disk-usage donut chart doubles as the magnifying-glass lens. One circle carries both meanings — "what's taking space" (segmented pie) and "peek / inspect" (loupe). This double-duty is the icon's soul and its one genuinely non-template move.
- **Diagonal glass tool overlay:** magnifier handle breaks the front plane to the bottom-right corner — Apple's own Preview/loupe tradition, textbook Big Sur "tool at an angle".
- **In-product artifact quotation:** the ring's segment palette is a direct quote of the app's own multicolor donut chart (see cover — blue/teal/gold/purple/green segments). Icon and product cohere; the icon shows you the exact object you'll use.
- **Ghosted glass folder:** the folder is rendered translucent so the background ramp reads through it — a Liquid-Glass flourish grafted onto a Big-Sur composition.

## Failures
- **#7 Figure-ground (hard fail):** the folder is #69BBFC on a #69ADFB field — **1.13:1**, far below the 3:1 floor. The folder, a primary narrative element ("in any folder"), is defined *only* by baked edge shadow and vanishes in grayscale and at small size. Every ring segment is also weak against the field (blue 1.46:1, gold 1.48:1, white 2.06:1) — the ring survives on internal hue variety and its baked rim, not on figure-ground.

## Soft passes (counted as passes, flagged for synthesis)
- **#1 Mask discipline:** squircle is *baked into the PNG* (transparent corners at a0) rather than delivered full-bleed unmasked; the system would double-mask. Corner curve reads slightly rounder/tighter than the macOS 26 continuous squircle. Reads correct, but not authored per HIG ("provide square, unmasked layers").
- **#3 Silhouette:** filled black it's busy — folder tab + ring + handle stack up; the magnifier reads, but a viewer needs the colour to fully parse it as a loupe-over-folder.
- **#4 16px squint:** the multicolour ring still telegraphs "colour gauge," but the folder (1.13:1) and the thin glass handle collapse — at menu-bar size you lose two of the three narrative elements. Carried entirely by the ring.
- **#6 Palette economy:** 6 hues in the focal ring exceed the ≤2-family guideline. Justified as *meaningful multicolour* (disk segments, SF-Symbols-multicolor logic) in a single focal element — but it does dilute the "one reserved accent" discipline.
- **#9 Era coherence:** hybrid. Composition is pure Big Sur (front-facing squircle, diagonal tool, baked top-down light); translucency + glass handle reach for Liquid Glass; yet specular/shadow are *baked*, which Liquid Glass forbids. The two conventions aren't reconciled.
- **#10 Variant robustness:** as a fixed-background baked raster with an intrinsically-multicolour focal element, there is no coherent tinted/mono path — a monochrome render would lose both the disk-segment metaphor and the already-invisible folder. (Lightly weighted since this is a Big-Sur-class icon, not a true Icon Composer glass icon.)

## Clean passes
- **#2 grid** (optically centred cluster, safe-zone margins), **#5 single light model** (consistent top-down + baked specular), **#8 depth coherence** (bg→folder→ring→handle stack ordered, shadows track the light), **#11 personality** (the ring-as-lens device), **#12 no-text** (no words/photos/UI).

## Production notes (resolution / craft honesty)
- 512×512 web render from macapp.supply, not the 1024 master — fine at this size, but detail/edge fidelity can't be trusted for micro-measurement.
- Effects (specular, translucency, contact shadows, squircle) are all baked into the raster; this is a *rendered/likely-AI-generated* app icon (over-smooth gradients, softly imprecise folder edges), not a hand-authored layered Icon Composer file. Do **not** treat as a native-craft exemplar — treat as a competent-but-generated indie utility icon whose one real idea (ring-as-lens) is worth remembering.

## Rhymes with
- Disk-usage analyser icons that render storage as a **colourful segmented ring/pie** (DaisyDisk / GrandPerspective lineage) — but re-housed on a friendly blue squircle instead of black.
- Apple's **loupe/magnifier-over-content** utility family (Preview, Finder search) — the diagonal-glass-tool convention.
- Style-family hint for clustering: *multicolour-diagnostic utility on a blue glass field* — a candidate "colourful-data-glyph over single-hue ramp" icon cluster if ≥2 more corpus icons share it.
