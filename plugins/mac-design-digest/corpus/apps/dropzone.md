# Dropzone — profile

- **Source:** macapp.supply (cover.webp) · **Surfaces digested:** menu-bar-extra launcher panel (light) · **Last updated:** 2026-07-19
- **One-sentence identity:** Launchpad's tile-grid metaphor repurposed as a drag-and-drop file router — a Sequoia-era vibrancy popover still wearing glossy-skeuomorphic destination icons; peers: Yoink, Dropover, and the retired Launchpad/Stacks grid.
- **Cluster:** unassigned (candidate: system-vibrancy menu-bar utility)
- **Lineage:** native / AppKit (high) — real menu-bar extra with an up-caret anchored to its status icon, SF Pro, compact 28–30pt controls, NSVisualEffectView popover material. No Catalyst/web tells. Non-native evidence: none.
- **Era (chrome):** big-sur (Big Sur→Sequoia vibrancy) — soft evenly-translucent light material, wallpaper-tinted, ~18pt panel radius; **not** confirmed Liquid Glass (no lensing/refractive edges visible, Sequoia default wallpaper). Content-layer destination icons are glossy-skeuomorphic gel (legacy holdover).

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| chrome/panel-material | translucent light vibrancy (menu/popover material), wallpaper-tinted, subtle top-lighter vertical gradient | (estimated)(inferred) | whole panel is floating chrome by nature (menu-bar popover) |
| radius/panel | ~16–20pt | (estimated)(inferred) | render @2x; corner reads ~18pt |
| chrome/toolbar-height | ~44–48pt | (estimated)(inferred) | one control row + padding, hairline divider below |
| control/height | ~28–30pt (Lg tier, kit=28) | (estimated)(inferred) | +, grid pop-up, window, gear |
| control/pill-radius | capsule / ~14pt | (estimated)(inferred) | "Main Grid" pop-up + grouped containers read capsule |
| tile/icon-size | ~60–64pt | (estimated)(inferred) | 5 per row |
| grid/columns | 5 | (measured)(inferred) | uniform 5-col tile grid per section |
| type/section-header | ~13pt SF Pro Semibold/Bold, dark, sentence/title case | (estimated)(inferred) | "Sharing" / "Folders / Apps" / "Actions" — NOT tracked uppercase |
| type/tile-label | ~11–12pt SF Pro Regular, primary label, centered | (estimated)(inferred) | one/two words under each tile |
| divider/hairline | 1px, very low contrast (<~10% black over vibrancy) | (estimated)(inferred) | section + toolbar separators nearly invisible — see Defects |
| accent/chrome | minimal — glyphs monochrome gray (~secondary label) | (estimated)(inferred) | little system-accent binding; utility-neutral chrome |
| menu-bar/selection | rounded-rect light fill, ~13pt radius | (estimated)(inferred) | status-item open state; matches kit menu-bar selection (13 on 25pt) |

Scale note: cover is ~@2x (menu bar ~48px raw → ~24pt). Panel inner width ~443pt (estimated). All pixel readings halved.

## Layout skeletons

**Menu-bar-extra launcher panel (light):** popover anchored by an up-caret to Dropzone's status-bar download-arrow icon (shown selected). Vertical stack, ~443pt wide:
- **Toolbar row (~44pt):** leading grouped container [ `+` add · `⌄⌄` collapse-all ] sharing one rounded translucent background; centered pop-up button `Main Grid ⌄` (single chevron, shows current grid value — pop-up/pull-down hybrid); trailing grouped container [ window-toggle | gear ] with an internal vertical divider. Faint hairline below.
- **Repeating section blocks** — each: left-aligned section header (SF Pro semibold) with trailing `^ ⌄` paging chevrons pinned to the right edge; then one row of 5 icon-tiles (icon + centered label). Faint hairline separators between sections. Sections observed: **Sharing** (Upload/SFTP · S3 · Email · Imgur · AirDrop) · **Folders / Apps** (Documents · Applications · Downloads · Sketch · Notes) · **Actions** (Merge PDFs · Resize Images · Convert to JPG · Shorten URL · Messages). Panel continues below the frame crop.

## Signature moves
- **[GOLDEN-NUGGET] The drag-target grid as the whole product.** The entire UI is a Launchpad/Stacks-style tile grid repurposed as destinations you throw files at — chunked into labeled sections (Sharing / Folders-Apps / Actions). Large ~64pt tiles are deliberately oversized Fitts targets for drag-drop, not for clicking. The grid *is* the interaction model.
- **Legacy-skeuomorphic soul in modern chrome.** A current Sequoia translucent-vibrancy popover houses glossy gel destination icons (SFTP "Upload") and a glossy 3D app icon — a decade-old skeuomorphic identity retained inside a modern material. The contradiction is the most memorable thing about the app's look; it reads as heritage, not neglect, because it's consistent.
- **Grouped-control containers.** Leading (+ / collapse-all) and trailing (window / gear) controls each share one continuous rounded translucent background with an internal divider — the container-grouping treatment, keeping the toolbar to ~3 visual clusters.

## Defects
- **Low UI contrast (rubric #10).** Section separators and grouped-control borders are near-invisible hairlines (likely <3:1) — the panel's structure leans entirely on the faintest fills over vibrancy. Canon: non-text UI contrast ≥3:1.
- **Borderline glass-on-glass (native audit #2).** Translucent grouped control pills sit on the translucent panel material. Legitimate in big-sur vibrancy grammar; would be a cardinal Liquid Glass defect if this were re-skinned for macOS 26+ without solidifying the controls.
- **Within-app material inconsistency.** Modern translucent chrome + glossy-gel legacy content icons are two different eras on one surface — logged as a signature-with-cost rather than a pure defect (it's systematic and consistent).

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar launcher panel (light) | 13/14 | #10 faint dividers/control borders <3:1 (#14 focus state unverifiable in static shot — not counted) |

| Surface | Native audit | Notes |
|---|---|---|
| menu-bar launcher panel (light) | 9/10 | #2 borderline translucent-on-translucent grouping; strong on lineage, sentence-case headers, borderless grouped toolbar, real chrome |
