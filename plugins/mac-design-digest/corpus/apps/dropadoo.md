# dropadoo — profile

- **Source:** macapp.supply (Mac App Store; German developer — UI copy in the prop reads "Suchen / Objekte / verfügbar") · **Surfaces digested:** main window (dark, single marketing-composite render) · **Last updated:** 2026-07-19
- **One-sentence identity:** A friendly-geometric dark utility — charcoal card dashboard of email "drop targets," warmed entirely by a rounded bold sans (Poppins/Nunito-class) and one pistachio-green accent; reads like an indie menu-bar file-sender that chose brand-character over platform fidelity.
- **Cluster:** unassigned (candidate: "friendly-dark-utility" — sole member so far)
- **Lineage:** web-electron (low confidence) — could equally be a custom-drawn cross-platform toolkit (Flutter/Tauri) or a heavily-restyled SwiftUI app; the point is it is **not AppKit-native**, so none of it feeds macOS canon. See Native tells.
- **Era (chrome):** custom (framework-agnostic dark theme; no Liquid Glass, no Big Sur native materials, no system chrome)

> **Evidence caveat (measurement honesty):** the only input is a single **marketing composite** (`cover.png`), not a real @1x/@2x screenshot. The app window is scaled to an unknown factor, so **absolute pt sizes are unrecoverable** — colours are sampled cleanly from flat UI regions and marked `(measured)`; all dimensions are ratios/relative and marked `(estimated)`. The Finder window in the composite is a **platform prop** (a genuine macOS 26 Liquid Glass Finder illustrating the drag *source*) — its tokens are NOT dropadoo's and are recorded only as contrast context.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#2E2E2E` charcoal (measured)(inferred) | | dark window field, not pure black; no wallpaper tint / vibrancy |
| bg/card | `#3B3B3B`–`#4C4B4B` (measured)(inferred) | | card fill ~+13–30 L above window = subtle tonal elevation, no shadow/border |
| accent/green | `#BEE294` pistachio-lime (measured)(confirmed) | | the whole palette's one hue; identical value on wordmark, per-card send glyph, and marketing pills → single-accent discipline |
| text/primary (title) | `#F4EFEF` near-white, bold (measured)(inferred) | | ~10:1 on card — anchors each card |
| text/secondary (email) | `#919191` mid-grey (measured)(inferred) | | ~3.6:1 on card — **fails 4.5:1**, see Defects |
| text/tertiary (caption) | ~`#787878` dim grey (estimated)(inferred) | | "subject: …" metadata; ~2.6:1, fails |
| icon/dim (per-card gear) | ~`#6A6A6A` (estimated)(inferred) | | ~2.1:1 on card — **fails 3:1** non-text |
| type/family | rounded geometric sans, Poppins/Nunito/Baloo-class (estimated)(confirmed) | | double-story rounded `a`, flat-top `t`, monolinear terminals — **not SF Pro**; the app's entire warmth |
| type/ramp | 3 sizes, title : body : caption ≈ 1.35 : 1 : 0.73 (estimated)(inferred) | | bold title / regular body / regular dimmed caption; likely ~Title2 / Body / Subheadline if window is a compact panel `(assumed)` |
| radius/window | large, reads ~20–24px-equiv (estimated)(inferred) | | custom borderless rounded window on wallpaper |
| radius/card | reads ~16px-equiv (estimated)(inferred) | | steps down inside window radius — concentric-plausible |
| chrome/titlebar | custom: grey faux/inactive traffic lights (left) + right-aligned `dropadoo` wordmark + hamburger + gear, 1px hairline divider under (estimated)(inferred) | | non-native composition — see Native tells |
| layout/grid | 2×2 equal card grid, gutter reads ≈ within-card line-gap × ~1.5 (estimated)(inferred) | | equal cards; on-grid-plausible |

## Layout skeletons

**Main window (dark panel):**
- Custom borderless rounded window, charcoal field, no OS toolbar.
- **Title strip:** three grey monochrome dots pinned left (faux/inactive traffic lights); trailing cluster right-aligned = two-tone `dropa`(green)+`doo`(grey) wordmark → hamburger menu glyph (top line tinted green) → outlined gear. 1px hairline separator beneath the strip.
- **Content:** 2×2 grid of equal destination cards. Each card is a self-contained region: **bold near-white title** (1–2 lines) → gap → **grey email address** (truncated with trailing `@`) → **dim "subject: …" caption** → footer icon row with a **green envelope-with-out-arrow "send" glyph leading** and a **dim gear trailing**. One primary (green send) + one recessive (gear) per card.

**Prop (not dropadoo — record as platform reference):** a native macOS 26 Finder window — white body, grey (inactive) traffic lights, circular Liquid Glass toolbar buttons (`»` overflow + magnifier "Suchen"), SF Pro, sortable "Name" column header, file-row list with type icons and one highlighted row, footer status line. Authentic native chrome juxtaposed against dropadoo's custom UI.

## Signature moves
- **[GOLDEN-NUGGET] Rounded geometric bold sans as the sole warmth vector.** On a flat charcoal utility, a Poppins/Nunito-class bold title face is the one decision that makes this read friendly-indie rather than sterile-pro. Everything else is greyscale; the personality is 100% in the typeface + the pistachio accent.
- **Destination-as-card dashboard.** Each predefined email target is a card carrying name / address / subject-template / a big green "send" affordance — turning "configure an SMTP action" into a recognisable, droppable tile (recognition over recall; large Fitts targets for drag-drop).
- **Single-hue accent economy.** Exactly one green (`#BEE294`) does wordmark, primary action, and brand pills — no second accent anywhere. Internally disciplined (even if it's the app's green, not the system accent).
- **Two-tone wordmark** (`dropa` green / `doo` grey) — cheap, legible brand tic echoing the icon's green-paperclip-on-charcoal.

## Defects
- **Contrast Dilution** → secondary email text `#919191` on card `#3B3B3B` ≈ **3.6:1** (fails 4.5:1); "subject:" caption ≈ 2.6:1; dim per-card gear ≈ **2.1:1** (fails 3:1 non-text) → **canon fix:** lift secondary label to ≥4.5:1 (a lighter grey ~`#B0B0B0`) and the recessive gear to ≥3:1; de-emphasis should stop at the contrast floor, not cross it.
- **Native tells (recorded as corrections, excluded from macOS canon — this app is non-native):**
  - Hamburger menu in the title strip → macOS exposes commands through the **menu bar**; an in-window hamburger is a web/mobile import.
  - Grey monochrome traffic lights on the hero window → a focused native window shows **coloured** controls; these read as faux/custom (or an inactive render). → use real `NSWindow` controls.
  - Brand green as the app's accent → native selection/focus/primary should bind to the **user's system accent**; brand hues belong to identity marks, not control accents.
  - Non-SF-Pro brand typeface → legitimate as deliberate brand character, but it is a native-fidelity deviation; native body would be 13pt SF Pro.
  - No native materials/chrome (custom dark theme) → absence of glass is fine, but combined with the above the window does not read as of-the-Mac.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark, composite) | 12/14 | #9 secondary text ~3.6:1; #10 dim gear/faux traffic lights <3:1 |
| main window — native-tells audit | 2/10 | #1 non-native lineage · #5 non-desktop card-dashboard density · #6 app accent not system accent · #9 hamburger not native toolbar · #10 faux/grey traffic-light chrome |
