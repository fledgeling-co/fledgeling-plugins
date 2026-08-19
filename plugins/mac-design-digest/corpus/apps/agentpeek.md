# AgentPeek — profile

- **Source:** macapp.supply (meta.json + cover.jpg + icon.webp) · **Surfaces digested:** none (no app-UI surface supplied) · **Last updated:** 2026-07-19
- **One-sentence identity:** A monochrome mascot utility that lives in the Mac notch — brand identity carried entirely by a black notch-as-face glyph and the system typeface, with no shipped-UI evidence to place it against peers yet.
- **Cluster:** unassigned (insufficient evidence — brand/icon only, zero UI surfaces)
- **Lineage:** unknown (low) — no UI shown; strong *prior* toward AppKit/SwiftUI-native because notch/menu-bar dwelling requires native macOS APIs (Electron can't easily occupy the notch), but that is inference from the product concept, **not** image evidence, so it never feeds macOS canon.
- **Era (chrome):** unknown — no window chrome shown. Icon container is Big Sur squircle era (superellipse rounded-rect), flat monochrome treatment (not a layered Liquid Glass icon).

## What was actually supplied (honesty note)

Two images, **neither containing app UI**:
1. **cover.jpg** — 1200×630 (measured), the exact OpenGraph/social-share ratio (1.91:1). A marketing composite only: blurred grayscale fluid-mesh backdrop + centred app icon + "AgentPeek" wordmark. No app window, no controls, no surface.
2. **icon.webp** — 102×102 (measured) app icon.

Per the cover-handling rule: the backdrop and wordmark are **brand evidence**, the icon is **icon evidence**, and there is **no design evidence of the app's UI**. The 14-point rubric and 10-point native-tells audit are therefore **not applicable** — you cannot score a surface that isn't present. Marketing copy (tagline "Your coding agents, in the Mac notch") is context, not evidence.

## Tokens

All values are brand/icon evidence — **no app-UI tokens are recoverable**. Every value `(estimated)` (small compressed webp / JPG composite) `(inferred)` (single exposure).

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/wordmark-type | SF Pro Display, ~Medium (500) | (estimated)(inferred) | The system font used *as the logo* — a deliberate native-Mac signal. Diagnostic letterforms: two-story `g` with open ear, `G` spur, `t`/`k` terminals |
| brand/wordmark-color | #FFFFFF, camelCase "AgentPeek", tight optical tracking | (estimated)(inferred) | White on the dark mesh; no custom logotype — leans on the platform typeface |
| brand/backdrop | grayscale blurred fluid-mesh gradient, monochrome (0 hue), heavy blur | (estimated)(inferred) | Black↔white↔mid-gray organic waves; the "abstract soft-mesh" marketing default, in its monochrome variant |
| cover/aspect | 1200×630 (OG social card, 1.91:1) | (measured)(inferred) | Confirms cover is a marketing/OG asset, not a screenshot |
| icon/container | Big Sur squircle (superellipse), white ground ~#FFFFFF→#F0F0F0 faint top-down gradient | (estimated)(inferred) | Standard rounded-rect app-icon plate; not layered glass |
| icon/glyph | black ~#0D0D0D notch/snout blob + two white cartoon eyes (dark pupils, tiny speculars) | (estimated)(inferred) | Reads doubly as the Mac notch shape *and* a peeking creature's face |
| icon/depth | soft gray rim-light around the black shape + faint drop shadow | (estimated)(inferred) | Slight raised/glossy feel; minimal, single soft top light |
| icon/palette | monochrome — black + white + one gray; **0 hues** | (measured)(inferred) | Extreme palette economy; hue is clearly absent, not merely muted |

## Layout skeletons

**No app-UI surface digested** — nothing to skeleton.

*Cover composite (brand layout, for the record):* centred vertical stack on a full-bleed 1200×630 mesh ground — icon (~200px squircle) above the wordmark, both optically centred; classic OG-card composition. Not an app layout.

## Signature moves

- **[GOLDEN-NUGGET] The Mac-notch-as-face.** The icon's single idea: one black rounded shape reads simultaneously as the physical notch (a pill hanging from the top with rounded corner "lips") and as a creature peeking down with two cartoon eyes. The entire product thesis — coding agents that peek at you from the notch — compressed into one monochrome glyph. Boldness budget spent entirely on this mark; everything around it (palette, type, backdrop) stays disciplined monochrome. Concept-driven, memorable, on-brand.
- **System typeface as logotype.** Using SF Pro Display straight as the wordmark is a deliberate native-affiliation move — cheap, and it inherits the platform's "crafted/native" first-impression prior. Common indie-Mac-utility choice; not distinctive, but coherent with the monochrome restraint.

## Defects

- **None scorable** — no UI surface to evaluate against the rubric or native-tells audit.
- *Icon legibility note (not a UI defect):* the two peeking eyes are small relative to the glyph; at 16px menu-bar/Dock size the eye detail + soft rim may collapse into a near-solid black blob (squint-test risk). `(estimated)` — would confirm against a real 16px render. The silhouette (notch/snout) survives; the "face" reading may not at the smallest sizes.
- *Marketing backdrop only:* the blurred grayscale fluid-mesh is the current default-model "abstract soft-mesh" backdrop; monochrome saves it from full template-generic, but it's a brand-asset observation, not an app finding.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| (none — no app UI supplied) | n/a | 14-point rubric + 10-point native audit both N/A: no surface present. Only a marketing OG cover + app icon were provided. |

## Knowledge gap this app leaves open

To place AgentPeek at all, the corpus needs its **actual UI**: the notch panel / menu-bar-extra popover, its agent-status list, any settings window. Everything above is brand + icon. Bring one screenshot of the live notch surface and this becomes a real profile.
