# Pattern: card-grid

Cross-app synthesis of card grids — stat-tile dashboards, thumbnail/masonry galleries, and tiled result/destination grids. Native-lineage evidence only. Kit floor: `kit/macos-27.md` — `radius/card` observed ~10–16 across the corpus; primary text 85% black light / #FFFFFF dark; secondary 50%/55%; concentric radii (child < parent).

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| Room Service | 4-up stat-tile row (dark) | equal-width tiles on shared axes, each = **tinted-square status glyph (r~6–8) + big number + secondary label** (Action Needed / Warnings / Review Notes / Healthy); cards r~10–12 sit ~1 lightness step over canvas, elevation by hairline border | (measured/estimated)(inferred) |
| Letterboxx | stats dashboard (light) | responsive **stat-tile card grid** (Today/Yesterday/This Week…): tile = system-hue glyph + `~26–28pt Bold value` + 13pt secondary sentence-case label; cards r~13, flat tonal fill (no heavy shadow) | (estimated)(inferred) |
| Mole | 4×2 stat-card grid (dark) | consistent ~12–16px gaps; each card = header row (tinted glyph + label + status chip) → hero figure + unit → mono metadata → inline viz (bar/sparkline/progress); cards r~10–14 | (estimated)(inferred) |
| Atlas | gallery canvas (light, Tahoe) | opaque thumbnails r~6–8 with soft shadow (~y+4/blur16); freeform "Infinity" or snapped Grid modes; zero-accent — colour ceded entirely to content items | (estimated)(inferred) |
| Resurf | masonry card library (light) | **variable-height (masonry) preview cards** r~12, inner preview r~8 (concentric step-down), footer = type-icon + title; blue selection ring on the active card | (estimated)(inferred) |
| Inkline | theme-card grid (dark) | theme cards (Dracula Solid / Ayu Dark), selected = violet border, each = "Dark" capsule badge + 4-chip swatch row | (estimated)(inferred) |
| Dropzone | 5-col tile grid (light) | uniform **5-col ~64pt icon-tile grid**, chunked into sentence/title-case sections (Sharing / Folders-Apps / Actions), each tile = icon + centred 1–2 word label; oversized as drag targets | (estimated)(inferred) |
| FolderVitrine | type/files data cards (light) | 2 stacked sections; Types card = header + proportional capsule bar + tinted legend; concentric radii | (estimated)(inferred) |
| Compresto | masonry media grid (light) | ~2-col variable-height thumbnails r~12–16; glass pill badges (`JPG\|1.3MB`) top-left + filename capsule bottom | (estimated)(inferred) |
| Zipic | result row-cards (light) | full-width white rounded row-cards r~14–18 on grey canvas; thumbnail + filename + blue ↓% badge + status | (estimated)(inferred) |

## Converged rules

- **Card radius runs ~10–16; inner elements step down concentrically (preview/glyph/badge radius < card radius)** — apps: Room Service (tile r10–12, glyph r6–8), Resurf (card r12, inner r8), Mole (r10–14), Letterboxx (r13), Compresto (r12–16), FolderVitrine — **(canon)**.
- **Stat-tile anatomy: tinted-square glyph + a large bold value + a secondary sentence-case label, value outranking label by scale** — apps: Room Service, Letterboxx, Mole, Mac 4 Breakfast — **(canon)**. Identity/status hue lives on the glyph; the value is neutral primary text.
- **Tiles sit on shared alignment axes with consistent, generous inter-card gaps (~12–16px)** — apps: Room Service (equal widths, shared axes), Mole (consistent gaps), Letterboxx (responsive grid), Dropzone (uniform 5-col) — **(canon)**.
- **Depth by tonal step + hairline, not heavy shadow — except gallery thumbnails, which carry a soft content-layer shadow** — apps: Room Service (border-as-elevation, cards ~1 step over canvas), Letterboxx (flat tonal fill), Mole (subtle lift) vs Atlas/Compresto (opaque thumbnails with soft shadow) — **(canon)**; the shadow exception is the content-item layer, kept off any glass.
- **Section-chunked grids use sentence/title-case headers** — apps: Dropzone (Sharing/Folders/Actions), FolderVitrine — **(recurring)**; consistent with the sidebar/list header rule.

## Divergences

- **Uniform grid vs masonry vs freeform canvas.** Uniform equal-size tiles (Dropzone 5-col, Room Service 4-up stat row, Mole 4×2) vs **masonry / variable-height** (Resurf, Compresto media grids) vs **freeform spatial canvas** (Atlas Infinity). The masonry/freeform split tracks the content-forward/gallery clusters (heterogeneous visual content wants variable height); uniform tiles track dashboards and destination grids.
- **Card vs flat content.** Individually floating rounded cards (Room Service, Zipic row-cards, Letterboxx tiles) vs opaque low-radius thumbnails on a bare ground (Atlas, Compresto). The floating-card treatment is the System-Settings-adjacent consumer register; the bare-thumbnail treatment is the gallery register that cedes all colour to content.
- **Colour strategy.** Zero-accent, content-carries-colour (Atlas) vs one-accent-on-neutral dashboards (Room Service orange, Mole per-status hues) vs data-viz-as-boldness (Letterboxx, FolderVitrine, SpacePeek — colour is a data channel). Tracks cluster: quiet-gallery vs graphite-dashboard vs data-forward.
- **Selection.** Blue accent ring on the card (Resurf) vs coloured border (Inkline theme cards) vs none (dashboards are display-only) — context-dependent.

## Generation guidance

- **Pick the grid type by content:** uniform equal-size tiles for a dashboard or destination grid (align on shared axes, consistent ~12–16px gaps); **masonry** for heterogeneous visual content (variable-height preview cards); a **freeform canvas** only for a curation/board app.
- **Card:** radius 12–14, with inner previews/glyphs/badges stepping *down* concentrically (e.g. card r12 → inner preview r8 → glyph tile r6). Depth by a one-step tonal lift + a ≥3:1 hairline (Room Service's ~1.1:1 borders are the logged Contrast Dilution miss — lift them). Gallery thumbnails may instead be opaque with a soft content-layer shadow (never on glass).
- **Stat tile:** `[tinted-square SF-Symbol glyph] [large bold value] [secondary sentence-case label]`. Put the status/identity hue on the glyph; keep the value neutral primary text. Values at Title1/LargeTitle scale (22–28pt) so they outrank labels.
- **Section-chunk** tiled grids with sentence/title-case headers (Sharing / Recent / Actions), larger gaps between sections than within.
- **Colour discipline:** decide the strategy up front — zero-accent (let thumbnails be the only colour, Atlas), one-accent-on-neutral (dashboards), or colour-as-data (data-viz cards, always glyph+label paired). Do not scatter generic accent tint across every card.
- **Selection** (if interactive): an accent ring or accent-tinted border on the active card, bound to the system accent.
