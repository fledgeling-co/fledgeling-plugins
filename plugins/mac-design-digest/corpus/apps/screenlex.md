# ScreenLex — profile

- **Source:** macapp.supply (meta.json + marketing cover; no dedicated UI shots) · **Surfaces digested:** annotation-editor toolbar (1, light) — from marketing composite · **Last updated:** 2026-07-19
- **One-sentence identity:** CleanShot X's floating-toolbar markup grammar re-drawn with a Lucide-family line-icon set and chunked into four Liquid-Glass capsule pods — a privacy-first screenshot redactor wearing well-tailored mac chrome over an uncertain (possibly web-wrapped) body.
- **Cluster:** unassigned (candidate: screenshot-annotators — peers CleanShot X, Open Screen Shot, CodeShot, Screen Charm)
- **Lineage:** native (**low** confidence) — the chrome *targets* AppKit/Liquid-Glass, but the evidence for a true AppKit runtime is thin; see Lineage note. Non-native evidence never feeds macOS canon, and this entry must not feed canon regardless (single marketing composite, low confidence).
- **Era (chrome):** Liquid-Glass-era styling (macOS 26+ target) — capsule container-morphing toolbar groups, floating pods, coloured traffic lights.

## Lineage note (why low confidence)

Only one surface exists, and it is a **marketing composite** (1200×630 OG image, perspective-tilted, non-retina), not a captured @2x screenshot. What reads native: coloured traffic-light cluster, a unified floating toolbar, capsule-grouped controls (the container-morphing signature), a value+chevron zoom stepper. What reads *non*-native / possibly web-wrapped:
- **Icon set is Lucide/Feather-family**, not SF Symbols: uniform thin stroke, rounded line-caps, and the specific glyph shapes (pushpin, droplet, layers/`square.on.square`-lookalike, download-to-tray, magnifier-plus). SF Symbols render with variable optical weight and, in toolbars, in **secondary-label gray** — these are drawn near-**black** (#2F2F30 measured).
- The **canvas content** being edited is a `localhost:3000` web page (ScreenLex's own landing site), and the product framing ("AI drives efficiency", OCR translation with "your own API keys") is SaaS-shaped — consistent with a Tauri/Electron indie tool.
- No menu bar, no native list/form/sidebar, no body typography is visible to confirm 13pt AppKit density.

Honest verdict: **the styling is native-targeting and competently executed; the runtime cannot be proven from this asset.** Treat as contrast-adjacent until a real screenshot arrives. `(insufficient-evidence)` on lineage.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| chrome/toolbar-bg | #EDEDED (measured)(inferred) | | flat toolbar fill, light mode; reads as light opaque gray, not translucent glass in this render |
| chrome/capsule-fill | #F2F3F4 (measured)(inferred) | | control-group pod fill — only ~1.03:1 lighter than the toolbar; pods read via soft shadow + hairline, **not** fill contrast |
| icon/stroke | ~#2F2F30 near-black (measured)(inferred) | | uniform thin outline (~1.5–2px), rounded caps — Lucide-family, NOT SF Symbols secondary-gray (#8E8E93). The core native-tell finding |
| accent/brand | blue ~#0A84FF–#2F80ED (estimated)(inferred) | | brand blue; seen on canvas "Get early access" chip + window bottom edge — **not** confirmed as a native accent binding (no tinted selection state visible) |
| traffic/red | ~#FE6362 (measured)(inferred) | | standard macOS; coloured = focused window |
| traffic/yellow | ~#FAC51B (measured)(inferred) | | standard macOS |
| traffic/green | ~#2FC650 (measured)(inferred) | | standard macOS (kit green #34C759) |
| control/toolbar-tier | ~34–38px capsule pods (estimated)(inferred) | | reads as the ~36pt XL toolbar tier (kit); composite scale unknown — ranges only |
| radius/capsule | capsule = height/2 (~17–19px) (estimated)(inferred) | | every group pod + the zoom stepper is fully rounded — capsule is the app's default bezel |
| traffic/dot | ~13–15px dia (estimated)(inferred) | | cluster narrower than kit's 68px but composite scale unknown |
| type/numeral | "100%" ~12–13px SF-ish (estimated)(inferred) | | only text in the app chrome; no ramp derivable |
| brand/wordmark | serif display, near-black (estimated)(inferred) | | BRAND evidence, not app UI: transitional/modern serif "ScreenLex" — editorial veneer over a utility |

## Layout skeletons

**Annotation-editor toolbar (single unified floating toolbar, light):**
`[traffic lights] · [MARKUP pod: lasso/cursor · rounded-rect · ellipse · line · arrow · text(A+I-beam) · zoom-in] · [AI/REDACT pod: OCR-scan · translate(²A) · redact-image · eye-slash(hide) · crop/perspective] · ——gap—— · [ACTIONS pod: droplet(color/blur?) · pushpin(pin) · layers(duplicate/copy?) · download(export)] · [ZOOM pod: "100%" + up/down stepper]`

Five semantic clusters, four of them capsule-container pods (the container-morphing grouping); traffic lights ungrouped at leading edge; zoom stepper right-aligned. Canvas below the toolbar holds the screenshot being edited (opaque content — here a captured browser window; not app-UI evidence).

## Signature moves

- **[GOLDEN-NUGGET] Capsule-pod chunking of a dense tool palette.** ~16 markup/redaction/action controls are organised into four fully-rounded container pods by *function* (draw / AI-redact / act / zoom) rather than dumped in one undifferentiated strip. This is the Liquid-Glass container-morphing pattern used for cognitive chunking (Miller): within-pod gaps are tight, between-pod gaps wide, so grouping is pre-attentive. The single strongest design decision in the asset.
- **Brand tension: editorial serif wordmark over utilitarian mac chrome.** The "ScreenLex" wordmark is a serif display face on a Big-Sur-blue wallpaper; the app itself is monochrome line-icon utility. A warm-editorial *brand* veneer over a neo-grotesque *product* — deliberate, and distinctive for a screenshot tool. (Brand evidence, not app-UI canon.)
- **Capture-reticle logo mark:** four corner brackets (scan/screenshot reticle) enclosing a mini window + cursor — on-subject iconography ("capture"). Brand evidence.

## Defects / tells

- **Non-native icon grammar (native-tell fail):** Lucide/Feather-family outline icons rendered near-black instead of SF Symbols in secondary-label gray. On a mac app this deviates from toolbar convention; it is also the loudest single reason lineage can't be confirmed native. → Canon would use SF Symbols, monochrome, secondary-gray, borderless.
- **No visible active-tool selection state.** All tools render at identical black weight; no accent-tinted "selected tool" is shown. Can't confirm the native selection grammar (inset rounded accent fill). Possibly just not captured; flagged as unassessed, not asserted as a defect.
- **Pod-to-toolbar fill contrast ~1.03:1** — the pods lean entirely on shadow/hairline to separate from the bar. Legible here, but a low-contrast choice worth noting.
- Not a defect, a limitation: **chrome-only marketing composite** means most of the 14-point rubric (type scale, measure, forms, lists, de-emphasis, focus) is unassessable.

## Rubric history

| Surface | Score | Failures / N-A |
|---|---|---|
| annotation toolbar (light, composite) | 9/14 assessable-pass; 5 N/A | Passes: #1 grid (soft/est), #2 alignment, #3 proximity (strong — capsule pods), #7 de-emphasis (n/a-leaning — all tools equal by design), #8 action singularity (no focal collision), #9 text contrast, #10 UI contrast, #11 Fitts (macOS toolbar tier), #12 control height. N/A: #4 modular scale, #5 line-height, #6 measure, #13 label proximity, #14 focus — no body content in a chrome-only composite. |

### Native-tells audit (10-point)
1. Lineage AppKit-native? — **UNCERTAIN/fail** — native-styled but Lucide icons + web canvas + composite-only; `(insufficient-evidence)`.
2. Glass only on floating chrome, content opaque, no glass-on-glass? — **pass** — toolbar reads opaque gray, pods opaque white raised (solid-on-solid, not glass-on-glass); canvas opaque.
3. Selection grammar (inset rounded accent fill)? — **N/A** — no selected-tool state visible.
4. Sidebar headers sentence-case? — **N/A** — no sidebar.
5. Density (13pt body, 20–28pt controls, desktop rows)? — **partial** — controls read ~36pt XL toolbar tier (ok); body unassessable.
6. Accent bound consistently? — **N/A/uncertain** — brand blue present but no tinted selection/focus to bind it to.
7. One prominent action per view; dialog grammar? — **pass (soft)** — no over-emphasised action, no dialog.
8. Concentric corners; radii step down? — **pass (est)** — window radius > capsule pods; pods = height/2.
9. Toolbar: borderless monochrome symbols, grouped, single primary? — **partial/fail** — grouped ✓, ≤3-group rule exceeded (5, acceptable for a pro palette), but icons are a custom non-SF set drawn near-black, not borderless secondary-gray SF Symbols.
10. Real chrome (genuine traffic lights, focus states)? — **pass (with caveat)** — coloured correct-cluster traffic lights; but a perspective-tilted marketing render, so "genuine" is inferred not proven.

Net native audit: ~5 pass / 2 partial-fail / 3 N/A — **not** clean-native. Recorded as tells-and-corrections, excluded from macOS canon.
