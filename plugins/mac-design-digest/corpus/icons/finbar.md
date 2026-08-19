# Icon: Finbar

- **Era:** Liquid Glass (macOS 26 language — frosted translucent layers, glass fin, edge/rim highlights) · **Rubric:** 8/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/finbar/icon.png`, SHA-1 `3250e299`) · clean native 1024×1024, transparent corners — not a resized web render
- **Subject:** "Menu bar search with superpowers" (Productivity). The icon *is* the pitch: a shark **fin** cutting through water inside a stylized menu/search panel — "Fin" + "bar", a literal double pun.

| Dimension | Reading |
|---|---|
| Background | Frosted gray glass panel, top-lit ramp `#ECECEC` (top highlight) → `#C6CDCD` (measured) — a stylized version of the app's own menu/search window |
| Glyph | Object: mint→teal glass shark fin, ramp `#95E7D9`→`#74D4C6`→`#5EBFB7` (measured), cyan rim-light `~#64C9C0`; anchored lower-right third, rising diagonally. Reads as a **scene/diorama** (panel + waterline + waves + fin), not a clean isolated glyph |
| Overlay device | None per se — the fin *is* the glyph; its diagonal rise echoes the Big-Sur "tool at an angle" tradition. Abstracted UI pills (search-field pill top, list rows, small pill lower-left) sit on the panel as the "bar" |
| Light model | Top-down / frontal glass, single consistent source. Baked soft specular along panel top, pill tops, wave crests and the fin's leading edge; short soft shadows; cyan rim-light on the fin |
| Layer stack | (back→front) frosted gray panel field → abstracted UI rows + top search pill → teal waterline/selected-row band `#4EACC5` → blue wavy water band `#8CD4FF`→`#4088EB` → rim-lit mint→teal glass shark fin |
| Palette economy | 2 hue families — cool blue/cyan (panel-gray, teal band, blue water) + mint-green accent (fin). Saturation reserved for the focal fin + the water; panel stays near-neutral cool. PASS |

## Signature devices

- **[GOLDEN-NUGGET] The Finbar double-pun.** Shark FIN as the literal "fin" + abstracted menu rows/search-field pill as the "bar". Name → image, executed in one composition. Textbook subject-mining.
- **Waterline-as-selection.** The flat teal band (`#4EACC5`) across the middle doubles as (a) a highlighted list row and (b) the water's surface horizon — one shape, two readings. This is the cleverest single move.
- **App's own UI as the icon ground.** The frosted gray panel + pill rows *are* a stylized Finbar search window — the icon communicates the product's surface literally, not by metaphor.
- **Rim-lit translucent glass fin.** Cyan edge-glow + refraction-style inner gradient; the focal shape carries the Liquid-Glass material.

## Failures

- **#3 Silhouette.** Filled solid black the art collapses to a plain squircle — the panel bleeds to every edge, so the fin and waves read *only* via internal colour, never via outline. Not nameable from shape alone.
- **#4 16px squint.** Menu rows vanish; the fin degrades to an unidentifiable green smudge; the whole thing reads as a generic gray-blue glass blob. Recovers by 32px (fin + notch legible). Ironic for a menu-bar app whose Dock/Spotlight/Finder presence is small.
- **#7 Figure-ground / grayscale.** Fin-vs-panel luminance contrast **1.02:1** (measured, floor is 3:1). Water-vs-panel 1.57, teal-band-vs-panel 1.47 — the *entire* icon is a low-contrast value mush. Grayscale confirms the fin nearly disappears; hierarchy is carried by hue and thin rim-lights alone, not luminance.
- **#10 Variant robustness.** Baked raster with specular/glow/shadow painted in (HIG says let the system apply these) — not authored Icon Composer layers. Identity depends on the light-gray panel + the specific blue/mint; dark/clear/tinted renders would not be system-generated and would not survive.

## Soft passes

- **#2 Grid.** Fin anchors the lower-right third, not optical grid centre — legitimate for a scene icon, but it is not glyph-centred, and the off-centre + small-in-frame fin is part of why #4 fails.

## Rhymes with

- (hint only, pending more icons) — "app-UI-as-icon" window-motif family: icons that depict a stylized version of the app's own window/panel as the ground. And pun-driven marine/mascot indie icons. Style family guess: **frosted Liquid-Glass scene-diorama** with a literal-subject anchor. Watch for a shared "low-contrast value mush / hierarchy-by-hue-only" anti-pattern if more glassy scene icons arrive.

## Cross-icon / cover coherence

Cover art abstracts the app's real UI (gray menu list + macOS **system-blue** selected row `~#0A84FF`, blue folder/menu glyphs, count badges) into the icon's frosted panel + blue water + teal selected-band. Icon-to-app palette coheres on **blue** (water ≈ app's selection highlight); the **mint/teal fin is icon-only brand flavour**. Clean thematic translation of product surface → aquatic scene.
