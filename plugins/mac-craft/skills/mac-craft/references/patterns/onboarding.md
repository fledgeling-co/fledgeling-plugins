# Pattern: onboarding

Cross-app synthesis of first-run / guided-flow surfaces. **Thin evidence — only 2 native members** (`onboarding` pattern = 2 native / 2: Bartender 6, macUSB), so nothing here reaches canon (≥3-app gate); rules are `(recurring)` at most and one member (macUSB) carries heavy iOS-idiom tells that are excluded from macOS canon. Kit floor: `kit/macos-27.md` — Setup-Assistant cadence; controls at the 24–36pt tiers; primary text 85% black light; capsule as the default bezel.

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| Bartender 6 | per-pane hero header card (settings, dark) | Every pane opens with an **elevated rounded card** (r~10–12) holding a **centred icon tile + LargeTitle-class pane title (~22–26pt Bold) + one explanatory line** ("Configure the Bartender basics…"); tonal-elevation card (`~#26282C`) one step above window; orients the user inside a config-heavy app — a chapter-title device | (estimated)(confirmed) |
| macUSB | Setup-Assistant wizard (dark) | Fixed portrait window ~550×790pt; single scroll column of **full-width rounded cards** (r~14–16, ~30px margins); centred rule-label section headers (flagged); **persistent flat bottom action bar** with one full-width blue capsule primary + a plain-text secondary (Back) below it; **tinted status-card semantics** (navy=in-progress / green=success / amber=destructive-warning, each glyph+label paired); step cards with ✓/active/pending states + determinate progress | (estimated)(confirmed) |

## Converged rules

- **A guided flow orients each step with a titled hero block: icon + a large bold title + one explanatory sentence** — apps: Bartender 6 (per-pane hero card), macUSB (per-step header + status cards) — **(recurring)**. Both answer "where am I / what is this step" before showing controls.
- **One prominent primary action per step, visually unmissable; the back/secondary action is quiet** — apps: macUSB (full-width capsule primary + plain-text Back), Bartender (single filled action per pane) — **(recurring)**. Corpus warning: macUSB's dual saturated primaries (Analyze + Continue) on one step is the Focal Collision defect — do not repeat.
- **State is communicated by tinted cards + a paired glyph + a label, never colour alone** — apps: macUSB (navy/green/amber status cards, each with glyph+text) — **(inferred, single-app)** but a genuine accessibility strength worth carrying; Bartender's inactive-pane muting rhymes.
- **Elevation by tonal step, not heavy shadow; concentric radii (icon tile < card < window)** — apps: Bartender (card `~#26282C` over window `~#1A1C1E`, tile r~5–6 < card r~10–12), macUSB (card `~#1C1C1E` over `~#0B0B0D`) — **(recurring)**.

## Divergences

- **Density / control sizing splits on lineage.** Bartender uses native 13pt-class density and standard controls; macUSB imports **iOS-scale** controls (~45pt full-width buttons, ~26pt checkboxes, ~34pt pop-ups, ~15px body) and a **floating centred modal** — all flagged native-tells, excluded from macOS canon. The correct native register keeps controls at the 24–36pt kit tiers and anchors modality to a top sheet.
- **Section-header treatment.** Bartender's are Title-Case system-font semibold (native-correct); macUSB's are centred labels flanked by hairline rules with mixed capitalization (flagged non-native).
- **Flow shape.** Bartender embeds orientation *inside* an ongoing settings surface (per-pane hero cards); macUSB is a discrete linear wizard with a persistent bottom action bar. Both are legitimate onboarding shapes; the choice tracks whether onboarding is a one-time flow or continuous in-context guidance.

## Generation guidance

*(Thin evidence — treat as provisional; lead any mock with that caveat, and prefer native controls over macUSB's iOS idioms.)*

- **Per-step structure:** a titled hero block first — centred icon tile + a bold title (LargeTitle/Title1, ~22–26pt) + a single explanatory sentence in secondary text — then the step's controls beneath it. This is the reusable device both members share.
- **Action bar:** one prominent primary per step (a standard-width or, for a consumer flow, capsule button bound to the system accent), with the Back/secondary action rendered quiet (plain text or bordered), never as a second saturated primary. Never make an abort/destructive action the loudest element (macUSB's loud-blue Cancel miss).
- **State cards:** for progress/confirmation, use tinted status cards (in-progress / success / warning) where every colour is paired with a glyph and a label — colour is never the sole signal. Reserve amber/red tints for genuinely destructive steps.
- **Depth + shape:** elevate cards by one tonal step (not a heavy drop shadow); keep radii concentric (icon tile < card < window). Cards ~r12–16, ~24–30px internal padding.
- **Stay native:** keep controls at the 24–36pt kit tiers (not iOS 44–52pt), section headers left-aligned Title-Case system-font (not centred rule-labels), and modality as a **top-anchored sheet** (not a floating centred dialog). Body text 13pt, not 15–17.
