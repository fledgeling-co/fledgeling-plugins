# Mole — profile

- **Source:** macapp.supply (mole.fit) · **Surfaces digested:** Status dashboard (dark), Clean hero (dark) — both from the marketing cover composite · **Last updated:** 2026-07-19
- **One-sentence identity:** htop's monospace telemetry density wrapped in a warm, screensaver-like cosmos — iStat Menus by way of a hacker console, with CleanMyMac's whimsy.
- **Cluster:** unassigned (cluster hint: *warm-terminal-telemetry* / "cosmic-console")
- **Lineage:** native (low confidence) — reads as a heavily custom-themed SwiftUI/AppKit app; **web-Electron cannot be excluded from a marketing still.** Its surface grammar departs from AppKit on multiple axes (see Defects), so per the lineage/era gate this evidence must NOT feed macOS canon as "native taste" — it supports timeless rules (hierarchy, grid, label-value) only.
- **Era (chrome):** custom design language over genuine macOS chrome (real coloured traffic lights, native arrow cursor). Not a Liquid-Glass build — no lensing/glass chrome observed; content sits on custom tinted gradients.

> **Measurement caveat (load-bearing):** both surfaces are scaled-down window mockups inside a 1200×630 non-retina OG composite. Absolute pt/px values are **unrecoverable**; every metric below is proportional/relative, `(estimated)` with wide ranges. Do not promote any absolute number from this profile.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas · Status | warm espresso→charcoal vertical gradient, ~#242018 → ~#1A1611 (estimated)(inferred) | | full-window tinted gradient, not neutral #1E1E1E — a deliberate warm cast |
| bg/canvas · Clean | navy-dusk vertical gradient, ~#0F1B2E → ~#0A1017, horizon mountain silhouette at base (estimated)(inferred) | | per-surface theming: each tab paints its own gradient sky |
| type/body | monospace, SF Mono-class, small (~11px-class), lh ~1.4 (estimated)(confirmed) | | **the whole UI is monospace** — labels, metadata, tables, chips |
| type/section-header | monospace, UPPERCASE, tracked +, tinted (green/teal) (estimated)(confirmed) | | e.g. `HEALTH` `CPU` `NAME (50)` — tracked-uppercase, a non-native tell |
| type/figure | bold, proportional (SF Pro-class), ~2.2–2.6× body (estimated)(confirmed) | | hero numbers (`90`, `77`, `86.4 GB`) break from mono to a bold proportional face for contrast |
| accent/good | system-green-class ~#40CC7A / #34C759 (estimated)(inferred) | | health/CPU labels, bars, "Excellent", battery — the primary status hue |
| accent/warn | amber ~#E8934A (estimated)(inferred) | | GPU/thermal warm tags, sun sphere |
| accent/info-teal | ~#3FB8C4 (estimated)(inferred) | | network sparkline |
| accent/info-blue | ~#3B82C4 (estimated)(inferred) | | disk progress bar; "Return to Earth" button fill/border |
| selection/tab | **white #FFFFFF filled pill, dark text** (estimated)(confirmed) | | active toolbar tab — NOT the native accent-tinted inset selection |
| card/fill | subtle tonal lift over gradient, translucent ~#2E2820-class (estimated)(inferred) | | 4×2 stat-card grid |
| card/border | faint hairline, ~white @6–10% (estimated)(inferred) | | very low-contrast — borderline <3:1 |
| card/radius | ~10–14px (estimated)(inferred) | | stat cards + tag chips (chips read capsule) |
| chip/tag | capsule, translucent fill, tinted mono text (estimated)(confirmed) | | `M2` `16 GB` `macOS 26.4` `98% Health` `Wi-Fi` `Normal` |
| chrome/toolbar | centred tab group: mole glyph in rounded container + 5 text tabs (Clean/Apps/Optimize/Analyze/Status) (estimated)(confirmed) | | segmented navigation living in the toolbar |
| row/table | dense, ~24–28px-class rows, icon + bold name + dimmed process-id + right-aligned numeric cols + `⋯` kebab (estimated)(inferred) | | process monitor; no visible zebra; hairline/none dividers |

## Layout skeletons

**Status dashboard** — Genuine window chrome (traffic lights leading; centred toolbar tab-bar). Below: a **4-column × 2-row stat-card grid** (HEALTH · CPU · GPU · MEMORY / BATTERY · DISK · NETWORK · THERMAL), gaps consistent (~12–16px-class). Each card = header row (tinted glyph + tracked-uppercase mono label, trailing status chip) → hero figure + unit → one-line mono metadata → an inline visualization (mini bar-array, area graph, sparkline, progress bar, or a thematic sphere). Beneath the grid: a full-width **process table** — sortable columns `NAME (50) · PID · CPU · PWR · MEM`, tracked-uppercase headers with sort carets, dense rows, trailing per-row `⋯`.

**Clean hero** — Same chrome/toolbar. Content is a centred vertical hero over the navy-dusk sky: a photoreal 3D **Earth** globe → bold figure `86.4 GB` → dimmed mono caption (`≈ 345 min 4K · All caches cleared · Lifetime: 1.2 TB`) → a single primary capsule button **Return to Earth** (blue-tinted). Reads as a reclaimable-space "empty/ready" state, not a list.

**Brand/icon (context, not UI evidence):** flat 2-tone mole silhouette — espresso-brown (~#2E241C) mark with a cream negative-space eye + haunch line on a cream (~#F2EBDD) circle. Logo-like, warm, single-weight; **not** a Liquid-Glass layered app-icon render (shown circular, so likely the brand mark rather than the shipped squircle). Marketing wordmark pairs a serif "One" with a sans remainder — brand evidence only.

## Signature moves

- **[GOLDEN-NUGGET] Monospace-everywhere telemetry.** Every label, chip, metadatum, and table cell is set in a coding monospace with tracked-uppercase section headers; only the hero figures break to a bold proportional face. Systematic across both surfaces — this single decision *is* the app's "instrument-panel / htop" character. (It is also the root of the non-native tells and the contrast risk — the same choice earns the identity and costs the audit.)
- **[GOLDEN-NUGGET] Thematic celestial visualizations + playful copy.** A photoreal 3D Earth for *Clean*, a plasma **sun sphere** for *Health*, a per-surface gradient sky with a horizon mountain silhouette — dry maintenance reframed as a warm cosmos, sealed with copy like "Return to Earth." Turns a category people distrust (system cleaners) into something calm and inviting (aesthetic-usability trust play).
- **Per-surface tinted canvas.** Each tab paints its own full-window gradient (warm espresso for Status, navy dusk for Clean) rather than a flat neutral window background — coherent brand atmosphere, at the price of legibility headroom.

## Defects

- **Contrast Dilution** → tertiary monospace metadata at ~30–40% opacity over the dark gradient (secondary process-ids `WeChatAppEx`, `since Jun 24`, card footnotes) likely falls <4.5:1 → canon: primary→~85% label, secondary→step, keep tertiary ≥4.5:1 on its actual background, not the darkest point of the gradient.
- **Tracked-uppercase headers** (non-native tell) → card + column headers are UPPERCASE tracked mono; the #1 sidebar/table authenticity tell → canon: system font, semibold, secondary colour, sentence/title case.
- **Toolbar-is-a-tab-bar** → segmented text navigation lives in the toolbar with a white-filled-pill active state → canon: a toolbar is not a tab bar; use a real tab view / sidebar, and native selection is accent-tinted inset, not a white fill.
- **Non-accent selection / unbound accent** → active tab = white pill; status hues are per-metric (green/amber/teal/blue) with no single system-accent binding selection+focus+primary → canon: bind selection/focus/one-primary to the system accent; identity colours stay separate (and each is paired with a glyph/label here — that part is correct).
- **Kebab (⋯) row menus** → web/Electron tell for row actions → canon: right-click context menu / hover reveal.
- **Target Starvation (borderline)** → per-row `⋯` and column sort carets are sub-24px glyphs; acceptable-ish on a pointer-first pro table but worth padding hit areas.

## Rubric history

| Surface | Rubric | Native-tells | Failures |
|---|---|---|---|
| Status dashboard (dark) | 12/14 | 5/10 | #9 contrast (tertiary mono on gradient), #10 UI contrast (hairline card borders <3:1); native fails #1 lineage-custom, #3 non-accent white-pill selection, #4 tracked-uppercase headers, #6 accent unbound, #9 toolbar-as-tabbar |
| Clean hero (dark) | 12/14 | 5/10 | #9 contrast (dim caption on navy); #10 borderline button/border; native fails same as above (shared chrome) |
