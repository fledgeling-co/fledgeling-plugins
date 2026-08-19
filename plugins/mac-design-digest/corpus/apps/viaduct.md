# Viaduct — profile

- **Source:** macapp.supply (cover composite; single app-window surface) · **Surfaces digested:** main window (dark), from marketing cover · **Last updated:** 2026-07-19
- **One-sentence identity:** A neo-grotesque dark utility — Linear's dark-neutral-plus-one-electric-accent discipline shrunk onto a single-task Mac converter, with the twist that the brand owns the actions (teal) while macOS owns the meanings (system green).
- **Cluster:** unassigned (cluster_hint: dark-utility-accent) — first member, no promotions
- **Lineage:** native (med) — genuine coloured traffic lights, transparent full-height titlebar, SF-Pro-class type, system-green semantic pill; SwiftUI reading. Confidence capped at medium because evidence is a *marketing-composite render*, not a retina screenshot, and the CTA carries two cross-platform idioms (full-width filled button + outer glow).
- **Era (chrome):** custom flat-dark (no Liquid Glass, no vibrancy, no toolbar) — a self-styled opaque dark surface with a faint cool/teal vignette; absence of glass is legitimate on a single-view utility, so not a defect.

## Evidence provenance caveat
All pixel values below are `(estimated)` from a 1200×630 marketing cover (OG-image scale), not a native @2x capture. The app window occupies ~560×370px of that canvas; type sizes are render-derived ranges, not measured retina points. Colours are reliable (flat fills sampled directly); geometry is approximate.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | #1A1E20 (top) → ~#222225 (lower) (estimated)(inferred) | | cool/teal-tinted charcoal, *darker & cooler* than kit dark #1E1E1E — a deliberate brand tint, not neutral system background |
| bg/card | #2A2A2E (estimated)(inferred) | | elevated content card; distinguished from window mostly by fill lightness, hairline border barely visible |
| border/card | ~#242427, ≈1px (estimated)(inferred) | | <3:1 vs window bg — reads via fill step, not the stroke |
| accent/brand-primary | #23B7A5 teal (estimated)(inferred) | | fills the one CTA; matches icon + backdrop family. **Brand accent, NOT system accent** — native selection/primary would bind to the user's accent |
| semantic/success | #30D158 (estimated)(inferred) | | exact match to kit dark-mode System Green `#30D158` → platform-fidelity signal; used for the "Installed in Safari" status pill, paired with a ✓ glyph (never colour alone) |
| label/primary | #FFFFFF (estimated)(inferred) | | "Viaduct" title, "Dark Reader" name |
| label/secondary | #7F8086 (~55% white) (estimated)(inferred) | | subtitle; contrast ≈4.3:1 on window bg — borderline under AA 4.5:1 |
| type/title | ~20–22pt equiv, bold (estimated)(inferred) | | centred app name, SF-Pro-class |
| type/body | ~12–13pt secondary; ~16–17pt item name (estimated)(inferred) | | reads as 13pt-class body, macOS density |
| radius/window | ~10–12pt (estimated)(inferred) | | closes the kit's `(unknown)` window-radius gap with a first (soft) data point |
| radius/card | ~12pt (estimated)(inferred) | | |
| radius/button | ~10pt (estimated)(inferred) | | |
| radius/pill | capsule (estimated)(inferred) | | success status pill |
| radius/ext-icon | ~14pt squircle (estimated)(inferred) | | the embedded Dark Reader tile |
| effect/cta-glow | soft teal outer glow around primary button (estimated)(inferred) | | non-native flourish; native buttons don't glow |

## Layout skeletons

**Main window (dark, single-view utility, ~560×370pt render):**
- **Titlebar zone:** transparent/hidden titlebar, content flows to top edge; coloured traffic-light cluster top-left only (focused window). No toolbar.
- **Header (centred column):** app name "Viaduct" (primary, bold) → 1-line secondary subtitle "Convert a Chrome extension and install it in Safari." Tight title→subtitle gap; larger gap to the card below (Gestalt proximity honoured).
- **Content card:** rounded elevated panel inset equally from both window edges. Vertically-stacked, centre-aligned: extension icon (squircle) → extension name (bold) → green capsule status pill "✓ Installed in Safari".
- **Primary action:** full-width filled teal button "Open extension" pinned at the bottom, sharing the card's left/right margins; soft outer glow.
- **Alignment:** single centre axis for header + card contents; card and button share one pair of vertical edges. Reads on an ~8pt vertical rhythm.

## Signature moves
- **[GOLDEN-NUGGET] Brand owns the actions, the OS owns the meanings.** The one CTA is the app's own teal (#23B7A5, matching icon + backdrop); the status state is macOS system green (#30D158, exact kit value) with a ✓ glyph. A tidy discipline: identity colour for the brand's action, system semantic colour for a system-meaning state — the two never blur.
- **Tinted dark surface.** The window ground isn't neutral #1E1E1E — it carries a whisper of cool/teal (#1A1E20), so the whole surface reads as *of the brand* without a single visible accent pixel in the chrome.
- **One-decision surface.** Big centred app name + a single concrete example card (real Dark Reader icon, real install state) + one CTA. Hick's Law taken to its floor; onboarding-flavoured but confident.

## Defects
- **Contrast Dilution (mild)** → subtitle #7F8086 on #1A1E20 ≈ 4.3:1, just under AA 4.5:1 for normal text → canon would push secondary labels to ~60% white (≈#999) or lift to a Callout weight.
- **Non-native CTA idiom** → full-width filled button + outer glow is a web/iOS pattern; a macOS-correct build uses a standard-width push button (or `.borderedProminent .controlSize(.large)` without the glow). Systematic and purposeful for a consumer utility, so a *tell*, not a hard defect — but it, plus the oversized control height, is why lineage confidence is capped at medium.
- **Brand accent over system accent** → primary binds to teal, not the user's system accent; acceptable house style for a branded consumer utility, recorded as deviation not defect.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark) | 12/14 | #9 subtitle text contrast ≈4.3:1 (under 4.5:1); #10 card hairline border <3:1 (boundary carried by fill step, so soft). #12–14 n/a (no inputs/forms/visible focus). |
| main window — native-tells | 8/10 | #5 control density: full-width ~44–52pt CTA departs the 24–28pt macOS ladder; #6 accent is brand teal, not system accent (semantic green is system-correct). #3,#4,#9 n/a (no list/sidebar/toolbar). |

## Brand context (marketing layer — NOT native evidence)
The cover backdrop is a vertical teal→mint gradient (#0F8477 → #65D1C3) with a bold white grotesk headline ("Run any Chrome extension.") paired against an italic serif subhead ("Now native in Safari.") — a grotesk-vs-serif-italic contrast pairing, plausibly SF Pro Display + New York italic. The app icon (icon.png) is a glossy top-lit teal **viaduct arch** on a black squircle — a literal name glyph, Big-Sur-era dimensional treatment. These establish the teal identity the window inherits; digested as brand evidence only (icon not run through Workflow B per task scope).
