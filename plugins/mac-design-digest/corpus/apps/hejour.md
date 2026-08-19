# Hejour — profile

- **Source:** macapp.supply (meta.json + marketing cover) · **Surfaces digested:** main window (partial — top ~25%, dark), from a scaled marketing composite · **Last updated:** 2026-07-19
- **One-sentence identity:** iA Writer's dimmed-markdown calm applied to a day-per-page journal — a monochrome dark note surface where the only saturated pixel is "done". Reference peers: iA Writer, Bear, Obsidian (live preview), Day One / Reflect (day-as-page).
- **Cluster:** unassigned (candidate: "quiet-editorial-dark" — sole member so far)
- **Lineage:** native (med confidence) — every visible tell reads AppKit-native / macOS-correct SwiftUI (13pt-class body, genuine coloured traffic lights, monochrome SF Symbol controls, hairline divider, rounded-square checkboxes, #1E1E1E window matching the kit). No iOS tells (no 44pt controls, no inset-grouped cards, no UISwitch). Confidence capped at med because only a quarter of one surface is visible and no sidebar/toolbar/settings is present to fully corroborate.
- **Era (chrome):** big-sur family — modern flat-opaque native (softened primary text, rounded window, no legacy bezels / no hard full-bleed blue selection). **Liquid-Glass era not excludable:** the window shows no NSToolbar or floating chrome, so there is no glass material to read; absence of glass on a plain content window is legitimate, not a defect. `(insufficient-evidence)` to place precisely between Big Sur and Tahoe.

## Provenance caveat

The only design evidence is the app window embedded in the marketing cover, cropped to its top ~25% and rendered at an unknown up-scale (body x-height measures far larger than any real logical size, so the window is a magnified render). **All absolute pixel sizes are untrustworthy — sizes below are recorded as ratios / tier-identifications, not measured points.** Colours ARE reliable (sampled from flat fills, unaffected by scale). Everything is single-surface `(inferred)`; `(confirmed)` is used only where a value re-evidences itself across three text runs within this one shot.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#1E1E1E` (measured)(inferred) | | Exact match to kit dark window background `#1E1E1E`. Flat opaque, no visible material/vibrancy. |
| text/primary | `~#DDDDDD` ≈ 85% white, 12.3:1 (estimated)(confirmed) | | "Today", "Plan", "ship the landing page" all sample 221. **Softer than kit dark primary `#FFFFFF`** — Hejour mirrors the kit's light-mode 85%-black softening into dark mode. House choice, not compression (uniform across runs). |
| text/tertiary | `~#565656` ≈ 33% white, **2.27:1** (estimated)(confirmed) | | One token does triple duty: date subtitle ("Friday, July 3"), markdown syntax markers ("##"), and completed-item text. Below the 4.5:1 text floor — see Defects. |
| divider/hairline | `~#343434` ≈ 13% white, 1.34:1 (estimated)(inferred) | | Full-width 1px separator under the header. Concentric with kit dark Fills-primary (10% white). Native-soft. |
| status/done | `~#5BCB02` lime-green, 7.9:1 (estimated)(inferred) | | Checkbox done-fill. Reads more chartreuse/yellow-green than system green `#34C759`/`#30D158` — a small brand deviation (edge sampling may exaggerate). Always paired with a white check glyph + strikethrough (status-with-glyph, per native grammar rule 3). The only saturated hue on the surface. |
| chrome/traffic-lights | red `#FF5C60`, yellow `#FAC800`, green (measured)(inferred) | | Standard, fully coloured → focused window. Generous top-left inset (no unified toolbar → small-inset archetype). |
| type/title | "Today": Title1–LargeTitle tier, Bold; cap height ~1.2–1.3× body cap (estimated)(inferred) | | Restrained title-to-body ratio (no size inflation) — hierarchy carried by weight + the tertiary de-emphasis of everything else. |
| type/body | 13pt-class system sans, reads SF Pro (Text); possibly SF Pro Rounded given the calm positioning — unconfirmed (estimated)(inferred) | | Double-story g, standard SF terminals; not confidently Rounded. |
| control/checkbox | rounded-square (NOT circle, NOT full capsule), ~body height, ~5–6px corner (estimated)(inferred) | | Todo = grey outline box; done = green fill + white check. |
| control/header-actions | borderless monochrome SF Symbols (keyboard toggle, settings gear), trailing, tertiary tint (estimated)(inferred) | | Placed in the content header row, not an NSToolbar — see Defects. |

## Layout skeletons

**Main window (partial, dark).** Plain-titlebar window (no NSToolbar / no unified toolbar visible in crop) · traffic lights top-left with generous inset. Single content column:
- **Header row:** large bold page title ("Today") + inline secondary date ("Friday, July 3") baseline-aligned to the title's right; trailing pair of borderless monochrome SF Symbol controls (keyboard-input toggle, settings gear) pinned right.
- **Hairline divider** (`~#343434`) full-width beneath the header, with a comfortable gap above and below (Gestalt: header group separated from body).
- **Document body:** a live-markdown note. "## Plan" heading with the `##` markers persisting in tertiary grey while "Plan" renders bold. Below it, checklist rows: rounded-square checkbox glyph + task text, all left-aligned to one shared margin axis. Done row = green box + white check + strikethrough dimmed-to-tertiary text; todo row = grey outline box + primary text.
- No sidebar visible in the crop (may exist off-frame — unknown).

## Signature moves

- **[GOLDEN-NUGGET] Dimmed inline markdown syntax.** The literal `##` markers stay visible in tertiary grey while the heading renders bold — the note shows its own plain-text bones. This is the app's entire editorial soul in one decision (iA Writer / Obsidian live-preview lineage).
- **Day-as-document title.** The date IS the page title ("Today / Friday, July 3"), literalising the brand line "every day, its own page." The window has no chrome competing with the page — the document is the interface.
- **Monochrome-plus-one-status palette.** Near-total grayscale (`#1E1E1E` / `~#DDD` / `~#555`) with a single lime-green reserved exclusively for the done state — a textbook Von Restorff use: the only saturated pixel in the frame means "completed".
- **Triple-duty tertiary grey.** One `~#555` token carries date subtitle, syntax markers, and completed text. De-emphasis is the whole hierarchy strategy — nothing is amplified; everything secondary is pushed to one recessive tone.

## Defects

- **Contrast Dilution (over-dim variant)** — the shared tertiary `~#565656` runs at **2.27:1** on `#1E1E1E`, under the 4.5:1 text floor. Acceptable for completed/syntax text (intentionally receding), but the *active* date subtitle "Friday, July 3" is live wayfinding text sitting at 2.3:1. Canon fix: lift persistent-metadata text to kit dark-secondary `#8A8A8A` (~4.5:1); keep the deep dim only for struck-through/inactive content.
- **Sub-3:1 UI borders** — divider `~#343434` (1.34:1) and the unchecked checkbox outline fall below the 3:1 non-text floor. Native-soft hairlines (kit separators are also faint), so a convention-consistent choice rather than a hard error, but at the low edge of legibility.
- **Header-embedded toolbar controls (observation, not defect)** — the keyboard/gear icons live in the content header rather than an NSToolbar. Works and stays quiet, but native grammar expects toolbar actions to also be menu-bar commands (unverifiable from this crop).

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (partial, dark) | 11/14 | #9 secondary/date/completed/syntax text 2.27:1 (<4.5:1); #10 divider 1.34:1 & checkbox border <3:1 (native-soft); #1 grid unverifiable (scaled marketing render) |

*Native-tells audit: 8/10 assessable passes — no violations found; #3 selection & #4 sidebar headers n/a (not visible); soft note on #9 (toolbar controls in header not NSToolbar). Glass discipline (#2) passes vacuously — opaque content, no glass to misuse.*
