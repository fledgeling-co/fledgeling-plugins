# Open Screen Shot — profile

- **Source:** macapp.supply (cover.png + icon.png only; no real screenshots) · **Surfaces digested:** menu-bar popover (as depicted in the marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** A CleanShot-adjacent menu-bar capture utility whose only visual evidence is a stylised OpenGraph card — a dark mint-accented popover in the Shottr/Xnapper register, but rendered as marketing art, not a shipped screen.
- **Cluster:** unassigned (candidate: dark-neutral mint-accent menu-bar utility — but UI evidence is a mock, so hold)
- **Lineage:** unknown (low) — the "app window" is a stylised illustration inside a 1200×630 marketing composite, not a captured surface; non-native and unclassifiable evidence, never feeds macOS canon.
- **Era (chrome):** pre-Liquid-Glass idiom (flat opaque near-black panel, no lensing) consistent with the cover's own "macOS 14+" (Sonoma) claim — but `(insufficient-evidence)` since it is an illustration, not a render of shipping chrome.

> **CRITICAL CAVEAT.** This profile is built from a single marketing OpenGraph card. The depicted window is a **marketing mock**, evidenced by two tells: (1) the popover's header mini-icon is a plain dark-teal rounded square that does **not** match the actual app icon (a blue scan-frame + download-arrow on a blue→cream ramp); (2) the UI accent is mint/teal while the icon glyph is system-blue — a brand accent that does not survive from icon to UI. Treat every measurement as illustration units (1× web composite), `(estimated)`, `source: mock`. Nothing here may promote macOS UI canon or seed a native style cluster. Real screenshots (the actual menu-bar dropdown, the crop/scroll HUD, Settings) are required to digest this app properly.

## Tokens

### App window (dark menu-bar popover — as depicted, `source: mock`)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/panel | ~#17191B near-black (estimated)(inferred) | | flat opaque floating panel; no glass/vibrancy visible |
| bg/row-card | ~#232629 (estimated)(inferred) | | list-row fill, one step lighter than panel |
| border/row-card | ~#33363B, ~1.5:1 on panel (estimated)(inferred) | | faint hairline — low UI contrast, see Defects |
| accent/primary | mint-teal ~#3ED9A2 (estimated)(inferred) | | sits between system Green #34C759 and Mint #00C8B3; NOT the icon's blue |
| accent/selection-tint | green-tinted row border + faint fill on selected row (estimated)(inferred) | | selection grammar; see Signature/Defects |
| text/primary | #FFFFFF (estimated)(inferred) | | wordmark + row titles |
| text/secondary | ~#8B8E93 (estimated)(inferred) | | "Click to capture" subtitle; ~4:1 on card, borderline |
| thumb/gradient | ~#FBEBD2 → ~#F4C889 cream→amber (estimated)(inferred) | | placeholder capture thumbnails; warm content vs cool chrome |
| radius/panel | ~28–32px illustration units (estimated)(inferred) | | large friendly corner |
| radius/row-card | ~12px (estimated)(inferred) | | |
| radius/thumb | ~8px (estimated)(inferred) | | |
| radius/swatch | ~10px (estimated)(inferred) | | bottom slot squares |
| type/wordmark | ~18px bold white "OpenSS" (estimated)(inferred) | | ~Title2/Headline class |
| type/row-title | ~15px semibold white (estimated)(inferred) | | ~Title3 class |
| type/row-subtitle | ~12px regular gray (estimated)(inferred) | | ~Callout class |
| row/height | ~72px illustration units (estimated)(inferred) | | reads consumer/touch-friendly, not 13pt-AppKit-compact |
| header/icon-tile | ~40×40, dark teal, radius ~10px (estimated)(inferred) | | mini-icon that does NOT match the real app icon |

### Brand backdrop (marketing evidence — NOT app UI, never native canon)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/gradient | royal blue ~#2B44B8 (TL) → periwinkle ~#6C80D4 → warm sand ~#E7C588 (bottom strip) (estimated) | | cool→warm diagonal; the sand strip echoes the thumbnail warmth |
| brand/headline | ~64px bold humanist sans, two-tone (solid white + ~50% lavender continuation) (estimated) | | "Long screenshots," opaque / "from the menu bar" translucent |
| brand/eyebrow | ~14px tracked uppercase + mint dot bullet, "FREE · OPEN SOURCE · macOS 14+" (estimated) | | |
| brand/subhead | ~22px regular muted-white (estimated) | | benefit line |
| brand/accent-dot | mint ~#3ED9A2 (estimated) | | the one place brand + UI accent agree |

## Layout skeletons

**Menu-bar popover (as depicted, right ~37% of the 1200×630 card).** Single vertical stack inside a rounded near-black panel:
1. **Header row** — leading mini app-icon tile (~40²) + "OpenSS" wordmark, left-aligned, ~top padding matching side padding.
2. **Capture-target list** — three equal rounded row-cards, ~10px inter-row gap, each: leading placeholder thumbnail (~52×40, cream→amber) + trailing two-line text block (title over muted "Click to capture"). Row 1 ("Medium article") carries the selected/hover state (green border + faint tint); rows 2–3 ("X / Twitter thread", "Notion doc") idle.
3. **Bottom slot module** — a darker sub-container holding 5 rounded squares in a row (~8px gaps); slot 1 filled mint (active), 4 empty dark — reads as recent-capture slots or a format/palette selector (ambiguous from a static mock).

Alignment: list-cards and bottom module share the same left/right inset off the panel edge; thumbnail-to-text and title-to-subtitle proximities are tight, row-to-row looser — Gestalt proximity honoured.

## Signature moves

- **Warm-content / cool-chrome split:** the only chroma inside the dark popover is the cream→amber thumbnail gradient (warm) against a near-black panel and one mint accent (cool). The captured *content* is warm; the *tool* is cool — a legible figure/ground device that also rhymes with the backdrop's blue→sand gradient. This is the one memorable idea in the composite (as a *marketing* move — not verified native UI).
- **Two-tone continuation headline:** "Long screenshots," in opaque white, "from the menu bar" in ~50% lavender — the important half carries full weight, the qualifier recedes (Von Restorff / de-emphasis in the marketing type). Not app UI, but a clean brand-craft tell.

## Defects

- **Contrast Dilution (UI borders) — faint ~1.5:1 row-card hairlines on the near-black panel** → native/rubric would want ≥3:1 non-text contrast on separators/borders; here they nearly vanish. `(estimated, from a mock — soft finding.)`
- **Brand accent discontinuity — icon glyph is system-blue, UI accent is mint/teal, and the popover's header mini-icon does not match the shipped icon.** In a real product this is an identity leak; here it is the primary evidence the window is marketing art rather than a capture. Corpus consequence: do not treat the mint accent as a confirmed product token.
- **Density reads consumer/iOS-large, not AppKit-compact** — ~72px rows and ~15px titles are touch-friendly popover proportions, not the 13pt-body / 24–28pt-control density of native macOS. Legitimate for a friendly menu-bar utility, but it is a reason this cannot stand in for native evidence.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| menu-bar popover (as depicted in cover, `source: mock`) | ~11/14 (soft) | #10 UI-border contrast (~1.5:1 hairlines); #6/#12/#13/#14 N/A (no paragraphs, inputs, forms, or focus state in a static mock) |
| — native-tells audit | ~5/10 | #1 lineage unconfirmable (illustration, not a capture); #5 density reads consumer-large not 13pt-AppKit; #4/#9 N/A (no sidebar headers, no toolbar). Passes: #2 no glass abuse, #3 rounded accent selection (approx), #6 accent internally consistent, #7 one prominent target, #8 corners step down, #10 correct absence of traffic lights on a popover |
