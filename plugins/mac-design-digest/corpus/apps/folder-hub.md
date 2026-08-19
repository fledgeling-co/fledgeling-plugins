# Folder Hub — profile

- **Source:** macapp.supply (finderhub.app) · **Surfaces digested:** notch file-drawer panel (1, light) · **Last updated:** 2026-07-19
- **One-sentence identity:** A Finder icon-grid miniaturised into a notch-anchored translucent drawer — NotchNook's notch-accessory instinct meets Dropover's file-shelf utility, in neutral Big Sur popover clothing.
- **Cluster:** unassigned (candidate: *menu-bar / notch utility — neutral native popover*)
- **Lineage:** native (med) — compact density, inset-rounded selection, borderless SF-Symbol toolbar glyphs, Finder-style icon view; no iOS/web tells. Confidence capped at med because the only evidence is a downscaled marketing render.
- **Era (chrome):** big-sur / legacy-native (med) — opaque-to-translucent light material, soft large radius, raised bordered+shadowed selected tab chip. No Liquid-Glass lensing/refraction visible; notably a floating popover (exactly where LG glass would live) reads as pre-Tahoe opaque light material.

## Provenance caveat

Everything below is drawn from **one 1200×630 marketing composite** (`cover.webp`), inside which the app screen is itself a downscaled illustration on a MacBook render. No standalone app screenshots were supplied (gallery empty). Absolute point sizes are therefore **not recoverable** — all metrics are `(estimated)` with wide ranges and low confidence; colours sampled from the composite are more reliable than dimensions.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/accent (marketing) | `#8C52FE` violet | (measured)(inferred) | brand panel + only saturated hue; **does not appear in the app UI itself** |
| bg/backdrop (marketing) | `#161616` near-black | (measured)(inferred) | softened, not pure #000 — technical dot-grid texture overlaid |
| bg/panel | `#F0F0F2`–`#F5F3F3` light neutral gray | (measured)(inferred) | drawer body; reads as translucent light material |
| sel/grid-item fill | `~#D0D1CE` neutral gray rounded rect | (measured)(inferred) | inset selection behind thumbnail — **neutral, not accent-tinted** |
| sel/tab chip | near-white raised chip + hairline border + soft shadow | (estimated)(inferred) | Big Sur segmented style, not a flat accent inset fill |
| type/tab-label | SF Pro ~11–13pt-class; selected dark/semibold, unselected secondary gray | (estimated)(inferred) | 2 weights |
| type/filename | SF Pro ~10–11pt-class, secondary gray, centered, 2-line wrap | (estimated)(inferred) | Finder icon-view label grammar |
| radius/panel | ~16–20pt (large) | (estimated)(inferred) | can't tie to grid at this scale |
| radius/selection | ~6–8pt rounded rect | (estimated)(inferred) | steps down under panel radius (concentric-plausible) |
| chrome/toolbar | bottom-trailing group of 3 borderless monochrome glyphs (grid-view · figure · account) | (measured)(inferred) | secondary gray |

## Layout skeletons

**Notch file-drawer panel (light).** Wide-short floating popover anchored to the display notch (no traffic lights — correct for a panel).
- **Row 1 — source switcher:** three leading icon+label tabs (`Screenshots` selected · `Downloads` · `Folder Hub`), left-aligned, + a trailing `+` add button top-right. Functions as a segmented scope switch, replacing the sidebar a normal Finder window would carry — a form-factor concession to the wide/short notch shape.
- **Content — icon grid:** Finder-style icon view, ~9 columns × 2 visible rows, each cell = thumbnail/preview + 2-line centered filename below. Selected cell carries a gray rounded-rect fill + emphasised label.
- **Bottom bar — utility toolbar:** trailing cluster of 3 monochrome glyph buttons (grid-view toggle, a "figure" quick-action, account).

## Signature moves

- **Sidebar→top-tabs transposition for the notch form factor.** Because the drawer is wide and short (dictated by the notch), the source list that a Finder window puts on the left is rotated into a horizontal segmented tab row. That single structural inversion is the honest visual signature — the rest is competent-but-anonymous Big Sur popover styling. The product's real signature is *interactional* (hover-the-notch to reveal, move-away to hide), which is out of scope for static analysis and noted, not scored.

## Defects

- **Contrast Dilution (mild)** — unselected tab labels and the secondary-gray filenames sit low-contrast on the `~#F0F0F2` panel; secondary-label contrast likely below 4.5:1 `(estimated)`. Canon: primary→~gray-900, secondary→gray-500 with a checked ≥4.5:1 floor.
- **Selection-grammar deviation from native** — the panel uses a *neutral gray* selection fill and a *raised bordered+shadowed* tab chip, where current native grammar is a flat inset fill with **accent-tinted** text/glyph, and the accent is the user's system accent. No system-accent binding is visible anywhere in the UI (the violet is brand-only). Reads slightly generic rather than wrong.
- **Weak information scent** — the bottom "running figure" glyph has no learned convention (Jakob's Law) and ambiguous meaning (Pirolli/Card information scent); a label or a more conventional symbol would help.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| notch file-drawer panel (light) | 11/14 | #9 secondary-label / filename contrast likely <4.5:1 (est.); #10 hairline border + monochrome glyphs borderline 3:1 (est.); #14 focus state not verifiable from a static render (n/a) |
| — native-tells | 7/10 | #3 selection fill neutral-gray + raised chip, not flat accent inset; #6 no system-accent binding in UI; #4 n/a (no sidebar headers) |
