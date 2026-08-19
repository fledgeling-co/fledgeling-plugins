# Super Shortcuts — profile

- **Source:** macapp.supply · **Surfaces digested:** marketing OG card (cover.png) only — **no app UI window supplied** · **Last updated:** 2026-07-19
- **One-sentence identity:** A Raycast/Vercel-register dark OG card for a keyboard-automation utility — near-black desaturated-green ground, one electric emerald accent, bold grotesk — whose one non-template move is demonstrating the product with real macOS modifier keycaps (`^⌥⌘R → make text red`).
- **Cluster:** unassigned (brand-only evidence; not eligible for a macOS UI style cluster — no app surface seen)
- **Lineage:** **unknown (low)** — the only image is a 1200×630 marketing composite with no app window, chrome, sidebar, toolbar, or controls. Nothing to classify. Non-native by construction (it's a web/OG social card), but that says nothing about the app's own framework. **Zero native-app evidence — nothing here feeds macOS canon.**
- **Era (chrome):** unknown for the app. The *brand backdrop* is contemporary dark-product-marketing (2023–2026 dev-tool OG-card idiom), not app chrome.

> **Provenance caveat (read first):** every value below is from a marketing composite, i.e. **brand evidence**, never design-of-the-app-window evidence. The app icon, wordmark, palette, and type personality are legitimately learned; the app's actual UI (windows, lists, settings, native-tells) is entirely unseen. Treat this profile as a brand card, not a UI profile.

## Tokens

All measured at the OG native raster (1200×630, treated as @1x per the OG spec — no retina halving applied).

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/ground | radial-ish `#0C120E` (corners) → `#111A14` (centre) (measured)(inferred) | | near-black, desaturated green; subtle centre glow behind headline |
| accent/emerald-fill | `#25AF69` (measured)(inferred) | | icon square fill; darker/more saturated than macOS system green `#34C759` — a **brand** green, not the system accent |
| accent/emerald-bright | `#5FD08D` (measured)(confirmed) | | headline line 2 **and** URL — same hex twice → confirmed accent token; mint tint of the fill |
| text/primary | `#F2F0EC` warm off-white (measured)(confirmed) | | headline line 1, wordmark, chip glyphs — **not pure #FFF**; deliberate warm softening |
| text/secondary | `#B8B6B0` warm gray (measured)(inferred) | | subhead body |
| text/mono | `#AEB0AB` neutral gray (measured)(inferred) | | "make text red" command demo |
| text/tertiary-meta | `#454942` dim gray-green (measured)(inferred) | | "Free to try · Local · One-time purchase" — near-invisible, ~2:1 (intentional de-emphasis) |
| surface/chip | fill `#1C241E`, ~1px border a shade lighter (measured)(inferred) | | keycap fill; border ~1.2:1 vs ground — barely visible (decorative) |
| type/headline | bold grotesk, cap-height ~44px → ~58–62px size, leading ~1.05–1.1 (estimated)(inferred) | | reads **SF Pro Display Bold-class**; Inter Bold a fallback possibility — mark estimated |
| type/wordmark | bold sans, ~28–30px (estimated)(inferred) | | "Super Shortcuts" |
| type/subhead | regular sans, ~24–26px, leading ~1.4 (estimated)(inferred) | | |
| type/mono | monospace, ~20px (estimated)(inferred) | | command demo + URL — SF Mono / Menlo-class |
| icon/app | 64×64px green squircle (radius ~14px ≈ 0.22×), white lightning bolt centred (measured)(inferred) | | brand lockup only; full icon digest (Workflow B) NOT run — see Knowledge gaps |
| chip/keycap | ~56×56px rounded square, radius ~12px, ~8px gaps, 4-up row (estimated)(inferred) | | `^ ⌥ ⌘ R` — authentic macOS modifier glyphs |
| layout/margin | ~80px left rail (measured)(inferred) | | icon/wordmark/headline/subhead/chips all share it; URL+meta right-aligned to ~1120px |

## Layout skeletons

**Marketing OG card (1200×630, dark, single column, left-aligned):**
- **Brand lockup** top-left (~y65): 64px icon + ~16px gap + "Super Shortcuts" wordmark, baseline-aligned.
- **Headline block** (~y180–320): two lines, tight leading. L1 warm-white "Stop doing the same 20 clicks by hand." / L2 emerald "Save up to 2 hours, every week." Scale is the whole hierarchy engine here.
- **Subhead** (~y365–435): two lines, secondary gray, ~55ch measure.
- **Footer row** (~y500–545): **left** — 4 keycap chips (`^⌥⌘R`) + `→ make text red` mono; **right** (right-aligned to margin) — `super-shortcuts.com` in emerald above `Free to try · Local · One-time purchase` in dim meta gray.
- Consistent 80px left rail; generous vertical rhythm; one accent moment (emerald) reused on the one headline line and the URL.

## Signature moves
- **[GOLDEN-NUGGET] The live keyboard-shortcut demonstration.** Rendering the actual macOS modifier symbols (`^ ⌥ ⌘`) as keycaps followed by `R → make text red` in monospace *shows* the product's core interaction (keystroke fires a local automation) inside the promo image itself. Subject-mined (the keyboard-command / terminal world), and the one thing lifting the card above its category's default OG look. Demonstrate-don't-describe made visual.
- **Disciplined single-accent economy.** Exactly one hue (emerald) carries all the "energy" — icon, one headline line, URL — against a near-black desaturated-green ground. Von Restorff by construction; the green never appears as noise.
- **Warm off-white instead of #FFF** (`#F2F0EC`) — a small, consistent softening that keeps the dark card from feeling clinical.

## Defects
- **Contrast Dilution (tertiary, intentional but flagged):** meta line `#454942` on `#0E1810` ≈ ~2:1 — below the 4.5:1 body floor. Defensible as decorative de-emphasis on a promo card; would fail as functional UI text. Canon would lift to ~`#7A7E77` (≥4.5:1) if this were app copy.
- **UI-contrast (decorative):** chip borders `#1C241E` vs ground ≈ ~1.2:1, below 3:1. Fine as an illustration; a real keycap control would need a ≥3:1 edge.
- **Category-default palette/type (not a defect, a limitation):** dark-neutral + one electric-green + bold grotesk + mono is precisely the Linear/Vercel/Raycast dev-tool OG reflex (`frontend-aesthetic-direction.md` flags this as a default-model reach). Brand-appropriate here, but "committed direction" only in the keycap signature — otherwise template-register for its category.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| marketing OG card | 11/14 (applicable checks only; #11–14 N/A — static promo, no interactive controls) | #9 partial — meta text ~2:1; #10 — chip border ~1.2:1 (both decorative/intentional) |
| — native-tells audit | **N/A** | No native surface present — cannot audit lineage/glass/selection/chrome. Not scored. |

## Knowledge gaps (this app)
- **No app UI whatsoever.** Lineage, era, density, native-tells, and every UI pattern are unknown. To profile Super Shortcuts as a *mac app* the corpus needs real window screenshots (main window, list/table of automations, settings, trigger editor).
- **Icon not formally digested.** The 64px lockup icon (green squircle + white bolt) is recorded as brand context only; a proper Workflow-B icon digest (12-point rubric, layer/light model) is outstanding.
