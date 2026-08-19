# Revone — profile

- **Source:** macapp.supply · **Surfaces digested:** main window dashboard (dark), from marketing cover · **Last updated:** 2026-07-19
- **One-sentence identity:** Linear/Raycast's dark neo-grotesque restraint applied to a Stripe-style revenue tracker — one electric-indigo neon chart against near-black, everything else monochrome.
- **Cluster:** unassigned (proposed: *nocturnal-electric-dashboard* / dark neo-grotesque)
- **Lineage:** native — SwiftUI, heavily custom-skinned (med confidence) — non-native evidence never feeds macOS canon
- **Era (chrome):** custom (dark-native); not clearly Liquid Glass — floating nav capsule *may* be Regular glass but dark-glass humility → `(insufficient-evidence)`; content layer is opaque

> **Provenance caveat:** the only asset is a **marketing composite** (2400×1260). Left third is brand backdrop (deep-indigo gradient, white "All Your Revenue in One Place for macOS" headline, Revone wordmark + icon) = brand evidence. The dark app window (right two-thirds) is the design evidence. It is a scaled ~2× render, so **absolute pt sizes are unrecoverable — all sizes below are proportional `(estimated)` with wide ranges**; only colours are cleanly `(measured)`. The app icon (`icon.png`) is present but out of scope for this UI digest (Workflow B / later icon pass owns it).

## Lineage evidence
- **Native tells:** icon set reads as canonical SF Symbols (`house.fill`, calendar/grid, `globe`, `list.bullet`, `person.crop.circle`, `gearshape`); SF Pro throughout; genuine coloured traffic lights top-left at correct inset; borderless monochrome toolbar glyphs.
- **Counter-risk:** the whole surface is custom-drawn (bespoke nav capsule, neon chart, deep-black canvas) which a web/Electron wrapper could also do — but SF Symbols + real chrome + SF Pro outweigh, hence *native (med)* not *high*.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#171717` (measured)(inferred) | | near-black canvas; **darker than kit dark window `#1E1E1E`** — HIG dark-mode guidance is to avoid near-black; app runs deeper for OLED-dashboard contrast (see Defects) |
| surface/card | `#242424` (measured)(inferred) | | single elevated floating breakdown card |
| accent/primary | electric indigo, core `~#6155F5`, saturated edge `#522BE5` (measured)(inferred) | | matches macOS 27 system **Indigo `#6155F5`** family, pushed slightly more violet/saturated; also the brand-backdrop hue → coherent brand↔product colour |
| text/primary | near-white `~#F2F2F2`→`#FFF` (estimated)(inferred) | | hero numeral, names, values |
| text/secondary | gray `~#8E8E93` (estimated)(inferred) | | "Revenue", "Monday", axis labels — matches kit Gray `#98989D`(dark) |
| text/tertiary | dim gray `~#6A6A6E` (estimated)(inferred) | | "Previous period", $17.50 — de-emphasised |
| status/positive | green text `~#34C759` on `~15%` green capsule fill (estimated)(inferred) | | "↗ 38%" delta pill — matches system Green; colour paired with up-arrow glyph (not colour-alone) |
| radius/card | `~20px` (estimated)(inferred) | | matches kit **popover-body radius 20** |
| radius/badge, nav-capsule | capsule / infinite (measured)(inferred) | | delta pill + nav container fully rounded — matches kit capsule-bezel convention |
| chrome/nav | centered floating **icon capsule**, 6 monochrome SF Symbols, translucent lighter-gray fill `~#26262A` (estimated)(inferred) | | selected item (home) = inset rounded fill in **neutral gray, NOT accent-tinted** |
| chart/primary | indigo spline w/ bloom/glow + gradient area fill (measured)(inferred) | | ~3px stroke, heavy outer glow |
| chart/secondary | ghost gray comparison series, hairline `<3:1` (measured)(inferred) | | plus white current-point dot + dashed vertical guide |

## Layout skeletons

**Main window (dark dashboard)**
- **Chrome:** standard titlebar, real traffic lights top-left. Title/toolbar zone holds a single **centered floating icon-capsule nav** (6 items: home · calendar · globe · list · person · gear). **No sidebar.**
- **Content (near-black canvas):** top-left stack — "Revenue" secondary label → giant `$4,973` display numeral with an inline-right green `↗38%` delta capsule. Below, a full-width neon spline chart: x-axis date labels only (Mar 20 / Mar 25 / Mar 30 / Apr 4 / Apr 9), **no y-axis, no gridlines**, ghost comparison series behind, white end-point marker on a dashed vertical guide.
- **Overlay:** a rounded (~20px) elevated card floats over the chart's right edge — daily breakdown: date header (`Apr 13, 2026` bold / `Monday` secondary) · 3 product rows (circular token logo + name left-aligned, **bold value right-aligned** on a shared axis) · 1px divider · `Total  $391` · 1px divider · `Previous period  $17.50` (dim). Values use tabular right-alignment.

## Signature moves
- **[GOLDEN-NUGGET] Neon-bloom accent chart.** An indigo spline with a genuine glow/bloom and gradient area-fill on a `#171717` canvas, with a ghosted gray comparison series behind — the app's entire character in one element. Data-ink-minimal (no axes/grid) traded for glanceable drama.
- **Centered floating icon-capsule navigation** in the title zone instead of a sidebar/tab view — compact single-window dashboard identity. Systematic + purposeful, so a signature; but also the app's principal native-tell (see Defects: "toolbar is not a tab bar").
- **One-accent discipline:** the only saturated colour in the whole content area is the indigo chart + a single green delta pill; everything else is a monochrome gray ramp. Von-Restorff-clean.

## Defects
- **Selection not accent-bound** → home nav selection is a neutral-gray inset rounded fill, not indigo-tinted; the accent lives only decoratively on the chart. Native selection grammar wants the selected glyph/text accent-tinted. → canon: bind selection + focus + primary action to the system accent.
- **Toolbar-as-tab-bar** → top-level navigation is a segmented icon capsule ("a toolbar is not a tab bar" — HIG routes primary nav to a sidebar or tab view). Also weakens information scent: 6 unlabeled icons rely on recognition (Pirolli–Card).
- **Near-black window bg (`#171717`)** deviates from HIG dark-mode guidance (avoid near-black; `#1E1E1E` base with spread tonal levels). Aesthetic choice, mild — records as a cluster trait, not a hard defect.
- **UI-contrast dilution (rubric #10)** → ghost comparison line and dim inactive nav icons read `<3:1`.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark) | 13/14 | #10 UI contrast (ghost comparison series & dim inactive icons <3:1); #14 focus-appearance n/a (static render) |

**Native-tells audit:** 6/10 — fails #3 (selection neutral-gray, not accent-tinted), #6 (accent decorative-only, not bound to selection/focus), #9 (nav capsule is a tab-bar-in-toolbar); #4 sidebar n/a. Passes lineage, glass discipline (content opaque), density (proportional), single-action, concentric corners, real chrome.

## Aesthetic
- **Adjectives (committed):** electric · nocturnal · minimal
- **Direction:** Neo-grotesque product / dark dashboard (dark neutral ramp + one electric accent, glow accents, dense-calm layout).
- **Peers:** Linear, Raycast, Vercel dashboard.
- **Note:** this is the current **model-default dev-tool look** (dark + electric accent — flagged in frontend-aesthetic-direction.md). Competent and coherent, but not off-distribution; its distinctiveness rests entirely on the neon-chart execution, not on the direction.
- **Audience:** consumer-utility / prosumer indie-maker revenue tracker (row items Frameblox/Runey/Supaframe read as indie SaaS products aggregated à la Stripe/Gumroad).
