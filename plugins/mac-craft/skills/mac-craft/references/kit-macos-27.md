# Kit: Apple macOS 27 UI Kit (Sketch)

- **Source:** `Apple macOS 27 UI Kit.sketch` (Apple Design Resources, Sketch 2026.2 build 231037, ~4,600 symbols across 37 pages) · **Ingested:** 2026-07-19 · **Authority:** `(specified)` — overrides screenshot estimates corpus-wide
- **Method:** deconstructed directly from the file's JSON (shared swatches, text styles, symbol frames, shape corner radii) — not from rendered exports. Values below are exact kit data unless marked otherwise.
- **Coverage:** colours, full type ramp, control size ladder for 14 control families, per-tier radii, window chrome anatomy, sidebar/menu metrics, state vocabulary. Not extractable from JSON: bezel fills/blur recipes baked into layer styles, window corner radius (see Gaps).

## Structural grammar (how the kit thinks)

- **Five-tier size ladder everywhere:** `1 Mn / 2 Sm / 3 Rg / 4 Lg / 5 XL`. One height ladder is shared by *all* control families — see Control metrics.
- **Content Area vs Over-glass duality:** every button variant exists twice — for placement in window content and for placement on Liquid Glass surfaces (toolbars, floating bars). Generated mocks must pick the context-correct variant; over-glass controls use the vibrant colour tiers.
- **State vocabulary:** `1 Idle / 2 Selected / 3 Clicked / 4 Disabled` × `Active/Inactive` (window focus) × `On/Off`. Inactive-window variants exist for nearly everything — native apps visually mute when unfocused.
- **Vibrant colour tiers** carry blending instructions in their names: Light Vibrant = "use plus darker", Dark Vibrant = "use plus lighter" — vibrancy is a compositing mode, not just a palette swap.

### Colour system `(specified)` — 106 shared swatches

**System colours** (per-mode values; vibrant tiers are for content over materials):

| Hue | Light | Dark | Light Vibrant | Dark Vibrant |
|---|---|---|---|---|
| Red | `#FF383C` | `#FF4245` | `#F52F32` | `#FF4747` |
| Orange | `#FF8D28` | `#FF9230` | `#F58625` | `#FF9E33` |
| Yellow | `#FFCC00` | `#FFD600` | `#F5C200` | `#FFE014` |
| Green | `#34C759` | `#30D158` | `#26BF4D` | `#3BDB63` |
| Mint | `#00C8B3` | `#00DAC3` | `#00BDA9` | `#2DE0CD` |
| Teal | `#00C3D0` | `#00D2E0` | `#00B3BF` | `#2DD7E0` |
| Cyan | `#00C0E8` | `#3CD3FE` | `#00ABCF` | `#47D8FC` |
| Blue | `#0088FF` | `#0091FF` | `#0078F0` | `#0A99FF` |
| Indigo | `#6155F5` | `#6D7CFF` | `#5C50E6` | `#7163FF` |
| Purple | `#CB30E0` | `#DB34F2` | `#B72BC9` | `#E647FC` |
| Pink | `#FF2D55` | `#FF375F` | `#F5234B` | `#FF4169` |
| Brown | `#AC7F5E` | `#B78A66` | `#9E7354` | `#C29672` |

**Labels (text hierarchy — 6 tiers):**

| Tier | Light | Dark | Light Vibrant | Dark Vibrant |
|---|---|---|---|---|
| 1 Primary | `#000000` @85% | `#FFFFFF` | `#363636` | `#FFFFFF` @96% |
| 2 Secondary | `#000000` @50% | `#FFFFFF` @55% | `#737373` | `#8A8A8A` |
| 3 Tertiary | `#000000` @25% | `#FFFFFF` @25% | `#B2B2B2` | `#4C4C4C` |
| 4 Quaternary | `#000000` @10% | `#FFFFFF` @10% | `#D9D9D9` | `#262626` |
| 5 Quinary | `#000000` @5% | `#FFFFFF` @5% | `#E6E6E6` | `#121212` |
| 6 Seximal | `#000000` @3% | `#FFFFFF` @3% | `#FAFAFA` | — |

Note: light-mode primary text is **85% black, not #000** — the kit itself avoids Contrast Dilution.

**Fills (5 tiers — used for bezels, tracks, subtle surfaces):**

| Tier | Light | Dark | Light Vibrant | Dark Vibrant |
|---|---|---|---|---|
| 1 Primary | `#000000` @10% | `#FFFFFF` @10% | `#000000` @15% | `#FFFFFF` @14% |
| 2 Secondary | `#000000` @8% | `#FFFFFF` @8% | `#000000` @7% | `#FFFFFF` @8% |
| 3 Tertiary | `#000000` @5% | `#FFFFFF` @5% | `#000000` @5% | `#FFFFFF` @5% |
| 4 Quaternary | `#000000` @3% | `#FFFFFF` @3% | `#000000` @3% | `#FFFFFF` @4% |
| 5 Quinary | `#000000` @2% | `#FFFFFF` @2% | `#000000` @2% | `#FFFFFF` @3% |

**Grays:** Light `#8E8E93` · Dark `#98989D` · Light Vibrant `#848489` · Dark Vibrant `#A2A2A7`
**Separators:** Light `#3C3C43` @29% (no dark swatch shipped — dark separators use Fills tiers)
**Window backgrounds:** Light `#FFFFFF` · Dark `#1E1E1E`

### Type ramp `(specified)` — SF Pro, 11 roles × 3 leadings

| Role | Default weight | Emphasized weight | Size | Line height (Default / Loose / Tight) |
|---|---|---|---|---|
| LargeTitle | Regular | Bold | 26pt | 32 / 34 / 30 |
| Title1 | Regular | Bold | 22pt | 26 / 28 / 24 |
| Title2 | Regular | Bold | 17pt | 22 / 24 / 20 |
| Title3 | Regular | Semibold | 15pt | 20 / 22 / 18 |
| Headline | **Bold** | Heavy | 13pt | 16 / 18 / 14 |
| Body | Regular | Semibold | 13pt | 16 / 18 / 14 |
| Callout | Regular | Semibold | 12pt | 15 / 17 / 13 |
| Subheadline | Regular | Semibold | 11pt | 14 / 16 / 12 |
| Footnote | Regular | Semibold | 10pt | 13 / 15 / 11 |
| Caption1 | Regular | Semibold | 10pt | 13 / 15 / 11 |
| Caption2 | Regular | Semibold | 10pt | 13 / 15 / 11 |

Loose = +2pt leading, Tight = −2pt leading, uniformly. **Body is 13pt** (macOS, not iOS's 17pt). No tracking values shipped (SF Pro handles optically). Footnote/Caption1/Caption2 share 10pt metrics — they differ by usage role, not size.

### Control metrics `(specified)`

**The universal height ladder** — one ladder for all control families:

| Tier | Height | Used by |
|---|---|---|
| 1 Mn | **16** | buttons, pop-ups, switches, segmented controls, dials (checkboxes/radios: 14) |
| 2 Sm | **20** | same (checkboxes/radios: 18; slider knobs 18–20) |
| 3 Rg | **24** | same + text/search/combo fields (default tier) |
| 4 Lg | **28** | same |
| 5 XL | **36** | same — the toolbar tier |

- Push button (Bordered Default, Rg): 66×24 with label inset **16px horizontally**, i.e. 16px padding each side `(specified)`; button style families: Bordered, Bordered Default, Bordered Tinted, Bordered Destructive, Bordered Default Destructive, Borderless, Toggle.
- Text/search/combo fields: default width 120, value text inset 6px (Rg). Steppers pair per-tier: up/down buttons 20×12 (Rg) to 30×18 (XL).
- Switches: 44×20 (Sm) · 64×28 (Lg) · 80×36 (XL) — knob is capsule.
- Progress: circular 16 (Sm) / 32 (Rg); linear track 6 (Sm) / 10 (Rg).
- Scrollbar: 12pt gutter, 6pt capsule thumb.

**Radius vocabulary:**

| Element | Radius |
|---|---|
| Search fields, switches, slider knobs/tracks, scrollbar thumbs, circular progress | **capsule** (infinite) `(specified)` |
| Text-field/combo focus rings by tier | Mn 4 · Sm 5 · Rg 6 · Lg 7 · XL 9 `(specified)` |
| Combo/text field bezels by tier | ~2.5 (Mn) → 6.5 (XL) `(specified)` |
| Menu item selection | 8 (on 24pt row) `(specified)` |
| Sidebar row selection | 8 (on 40pt Large row) `(specified)` |
| Popover body | 20 `(specified)` |
| Menu-bar item selection | 13 (on 25pt) — capsule `(specified)` |
| Push-button bezel | capsule `(estimated)` — no shape data in JSON; inferred from the capsule pattern of sibling controls (search fields, switches) and Liquid Glass conventions |

### Window chrome anatomy `(specified)`

| Element | Metrics |
|---|---|
| Titlebar (Default style) | **33pt**; title = Title3-size text at y=9; traffic lights 68×14 cluster at (9, 9.5) |
| Panel titlebar | 24pt; panel traffic lights 44×10 |
| Unified toolbar | **52pt** = 8 + 36 (XL controls) + 8 |
| Unified compact toolbar | **40pt** = 8 + 24 (Rg controls) + 8 |
| Expanded toolbar | titlebar 33 + toolbar row 44 (36-high controls) = **77pt** total |
| Toolbar composition | leading nav cluster (20×20 buttons in a 73×36 glass group), centre title, trailing button group + search field (159×36) |
| Scroll Edge Effect | dedicated symbol overlaying content-top under the glass toolbar (34–78pt tall, matches chrome) — the Liquid Glass "content scrolls under glass" treatment; include it in mocks with unified/expanded toolbars |
| Sidebar | **256pt wide** (examples); rows full-bleed minus 4px insets (248 wide), selection radius 8 |
| Sidebar row heights | Small **24** · Medium **32** · Large **40**; section headers 18–20 |
| Menu | items: Mini 19 · Small 22 · Regular **24**; menu inner padding 12–14; item selection radius 8; separators ~11.5pt tall zones |
| Window sizes in examples | standard example window 840×400; full-screen examples 1512×982 (14″ MacBook Pro logical resolution) |
| Alert buttons | 228×28 (Cancel, stacked layout) |
| Tooltips | min 98×19 |
| Notification tile | 80×80 BG, 32×32 icon |
| Dock/menu-bar app icons | 72×72 (at example scale) |

### Materials & modes

- Every component ships Light + Dark; most ship Active/Inactive (window focus) — four visual states per control before interaction states.
- Vibrant swatch tiers exist specifically for over-material rendering with named blend directions (plus-darker / plus-lighter).
- Material *recipes* (blur radii, saturation) are baked into Sketch layer styles (285 shared styles, organised as `Content Area|Over-glass / Light|Dark / style / state`) and aren't numerically recoverable from JSON — treat material appearance as `(estimated)` from renders when needed.

### Deltas vs. Big Sur–Sequoia era (high value — shipping apps will lag)

- **Control ladder normalised**: Regular controls are 24pt tall (previously ~20–22pt); XL 36pt tier is new, purpose-built for toolbars.
- **Capsule as the default bezel** for search fields/switches (and likely buttons) — the era's shape signature, replacing 5–6pt rounded rects.
- **Over-glass variant set doubled the kit**: designing "on glass" is now a first-class context, not an edge case.
- **Scroll Edge Effect** codified as a component — content legibility under floating glass chrome is a designed artifact.
- **Toolbar heights**: unified 52pt (was ~52 similar) but compact 40pt and expanded 77pt with the new control tiers inside.
- Primary light-mode text is 85% black (softened from pure black eras).

### Gaps

- Window corner radius: rendered via layer styles/masks, not shape data — `(unknown)`, measure from a screenshot when one is digested.
- Button bezel fills/blur and all material recipes: in layer styles only — `(estimated)` pending rendered-frame digestion (Workflow C on exported PNGs would close this).
- Kit ships no spacing/grid page — inter-control layout rhythm must come from app digestion (Forms examples 1440×900 exist in the kit and could be digested as layouts later).
