# SpacePeek — profile

- **Source:** macapp.supply · **Surfaces digested:** 1 (app window inside marketing cover — Quick Look-style folder-size panel, Overview tab, light) · **Last updated:** 2026-07-19
- **One-sentence identity:** DaisyDisk's chromatic disk-usage storytelling rebuilt as a native-feeling, spacebar-invoked Liquid Glass Quick Look panel — light and translucent where the category reflexively goes dark.
- **Cluster:** unassigned (suggest `chromatic-glass-utility (light)` — synthesis pass owns cluster assignment)
- **Lineage:** native / SwiftUI (med confidence) — Catalyst not fully excluded; iOS-derived styling tells recorded below never feed macOS canon
- **Era (chrome):** Liquid Glass native (macOS 26–27) — whole-window translucent material, capsule pills, rounded-everything

> **Evidence caveat (read first):** the *only* input is the app window composited inside `cover.png` (1280×800) over a warm sunset wallpaper — no standalone screenshots exist. Every value below is `(estimated)` at an unknown downscale; type is read as **roles**, not asserted pt. Translucency is likely exaggerated by the marketing wallpaper. No dark mode, settings, empty, onboarding, selection, or focus evidence. The 512×512 icon was **not** digested (Workflow A / UI only).

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window-material | whole-window translucent light vibrancy; wallpaper visible through content, warm-tinted | (estimated)(inferred) | Quick Look-style floating panel; translucency likely marketing-exaggerated |
| bg/content-card | near-white translucent rounded panel (~#F4F2EE warm-white over material) | (estimated)(inferred) | summary + list container sit slightly lighter than window ground |
| accent/primary | system blue ~#0A84FF/#0088FF | (estimated)(inferred) | segmented selection + brand headline; matches macos-27 kit Blue; used for the one prominent element only |
| palette/identity | system 12-hue — blue, teal/cyan, green, yellow, purple, red, pink, gray | (estimated)(confirmed) | mapped per folder AND echoed in donut arcs (re-evidenced twice in one surface); kept separate from the blue accent — native-correct |
| text/primary | near-black ~85% black | (estimated)(inferred) | names, sizes, '59.5 GB', section header; aligns with kit primary label = 85% black |
| text/secondary | ~50% gray | (estimated)(inferred) | 'Files'/'Folders' sublabels, '/Users', title subtitle |
| text/tertiary | ~40% gray | (estimated)(inferred) | row percentages — contrast-at-risk on translucent ground (see Defects) |
| type/hero-number | '59.5 GB' — LargeTitle/Title1-class SF Pro Bold | (estimated)(inferred) | role read, not exact pt |
| type/section-header | 'Largest items' — Headline/Body 13pt-class Bold, sentence case | (estimated)(inferred) | sentence-case bold header = native-correct |
| type/row-body | folder name + size — Body 13pt-class SF Pro (size medium, name regular) | (estimated)(inferred) | |
| type/caption | percentages / sublabels — Caption/Footnote 10–11pt-class | (estimated)(inferred) | |
| control/segmented | 'Overview \| Contents' capsule; selected = solid blue fill + white text; unselected = neutral translucent track | (estimated)(inferred) | in-view scope switch (legit use); selected-fill styling is iOS-flavored |
| control/status-pill | '⚡ 801k items scanned in 2.91 s' — capsule, bolt glyph + text, translucent fill | (estimated)(inferred) | status paired with glyph (native-correct); sells scan speed |
| chrome/panel-buttons | two dark monochrome circular buttons top-left — ✕ (close) + ⊘ (stop/cancel); share glyph top-right | (estimated)(inferred) | custom panel chrome, NOT traffic lights; OK for a Quick Look panel |
| radius/window | ~14–16px on canvas | (estimated)(inferred) | kit lists window radius as (unknown) — this is a composite estimate |
| radius/card | ~12–14px | (estimated)(inferred) | steps down from window radius |
| radius/row | ~10–12px rounded pills | (estimated)(inferred) | concentric child of the list container |
| radius/pill | capsule | (estimated)(confirmed) | segmented control + status pill; matches kit capsule-as-default-bezel era signature |
| list/row | generous rows (~40–44px equiv); leading colored icon + name, trailing size + % + chevron; full-width colored tint wash | (estimated)(inferred) | tint weight tracks rank/proportion — the signature move |
| chart/donut | ring chart, padded arcs + rounded caps, 12-hue segments + gray 'other', center total | (estimated)(inferred) | colours map 1:1 to list rows |

## Layout skeletons

**Quick Look-style folder panel (Overview) — single window, ~4:3, floating over Finder**

- **Panel header (top strip):** leading dark ✕ + ⊘ circular buttons and window title `wangfu`; below-left a folder glyph with `wangfu` / `/Users` (title + secondary path); horizontal center a capsule **segmented control** `Overview | Contents`; trailing a translucent status **pill** (`⚡ 801k items scanned in 2.91 s`) and a share glyph. Two stacked rows of chrome, borderless monochrome symbols.
- **Body splits into two columns:**
  - **Left column (~62% width):** a **summary card** — hero total `59.5 GB` (Bold display) with two label/value stat pairs beneath (`699,142 Files`, `101,624 Folders`), each with a document/folder glyph, value bold over quieter label. Below it, the **Largest items** list: sentence-case bold section header, then rounded rows sharing one left edge; each row = colored folder icon · name (left) / size · percentage · disclosure chevron (right), with a per-row identity-hue background wash.
  - **Right column (~38% width):** a **donut chart** centered vertically, arcs in the same identity hues, center label `wangfu` + `59.5 GB`.
- **Alignment:** summary card, list header, and rows share a common left axis; donut is a discrete right-hand region. Row internal rhythm is uniform (consistent gaps + paddings).

## Signature moves

- **[GOLDEN-NUGGET] Per-row colored tint wash.** Each `Largest items` row carries its folder's identity hue as a full-width background wash whose weight tracks rank/proportion — the list *is* an inline bar/treemap. The same hue reappears as that folder's donut arc, so a single item's size is triple-encoded (number + row-tint + arc). This is the app's whole character in one decision: color is a data channel, not decoration.
- **[GOLDEN-NUGGET] Quick Look disguise.** The product presents as a native Finder Quick Look panel — spacebar-invoked, translucent, ✕-to-close, no traffic lights — rather than a document window. `Press Space. See everything.` sells a gesture users already own (Jakob's Law); the tool inherits Finder's trust and needs no onboarding.
- **Speed-as-proof status pill.** `⚡ 801k items scanned in 2.91 s` keeps the Rust engine's throughput on-screen as chrome — performance rendered as a persistent trust signal (processing-fluency lever).

## Defects

- **Contrast Dilution (risk)** → tertiary percentages + `/Users` subtitle at ~40–50% gray over a translucent, wallpaper-tinted ground likely fall below 4.5:1 → canon would solidify the panel's secondary-text zones (or lift tertiary to a higher label tier); a floating panel over an arbitrary desktop is the worst case for translucent secondary text.
- **Glass-in-content (low confidence)** → list rows + summary card sit on whole-window translucent material with wallpaper showing through → Liquid Glass golden rule wants content opaque; softened here because this is a *transient Quick Look panel* (the whole surface is arguably floating chrome) and the composite likely exaggerates translucency. Record, don't hard-fail.
- **iOS-flavored controls on macOS (native-tell, not a universal defect)** → saturated-blue selected segment + inset-grouped tinted rows with per-row chevrons follow iOS grammar, not AppKit's neutral elevated segment and flat NSTableView row/selection → excluded from macOS canon per the lineage gate; the native correction is a lighter elevated segment fill and flat rows with inset-rounded *selection* only.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| Quick Look folder panel (Overview, light) | 12/14 · native 6/10 | #9 text contrast (tertiary gray on translucent), #10 UI contrast (light chevrons, no row borders); native #1 iOS-style rows, #3 saturated segment selection, #2 glass-in-content (low-confidence), #10 custom panel chrome (panel-contextual) |
