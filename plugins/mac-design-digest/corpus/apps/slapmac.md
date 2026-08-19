# SlapMac — profile

- **Source:** macapp.supply (meta.json + cover.jpg + icon.webp) · **Surfaces digested:** none (no app UI supplied — see below) · **Last updated:** 2026-07-19
- **One-sentence identity:** A gag/novelty utility whose only visual artifacts are a comic-mascot app icon and a logo-mockup marketing cover — no shippable UI evidence exists, so this profile is brand-only and feeds nothing into macOS canon.
- **Cluster:** unassigned (insufficient evidence — no UI surface)
- **Lineage:** unknown (low confidence) — **there is no window, chrome, or control in either input, so lineage cannot be classified.** The icon idiom (legacy iOS-6-era rounded-rect frame, monochrome cartoon) is a non-native tell that makes a carefully AppKit-native app *unlikely*, but that is inference from the icon, not observation of the UI. Recorded as unknown, not native.
- **Era (chrome):** n/a — no chrome present. Icon frame reads legacy/pre-Big-Sur (see Icon note), not Liquid Glass, not Big Sur squircle.

## What was actually supplied (provenance boundary)

macapp.supply gave two files, both **brand evidence, not design evidence**:

1. **cover.jpg** (1376×768) — a **marketing composite / logo mockup**: the SlapMac mascot (a cartoon green laptop with an anguished blushing face being slapped by a green hand, "SLAP!" comic burst) rendered as a glossy embossed 3D logo with drop shadow and lime rim-glow, mocked onto a softly-lit off-white studio-wall backdrop, "SlapMac" wordmark below in a bold rounded green sans. This is a stock logo-mockup template — the backdrop and emboss are the mockup, not the product. **No app UI whatsoever.**
2. **icon.webp** (204×204) — the app icon (analyzed as brand/icon evidence below; not run through the 12-point icon rubric, which a later icon-workflow pass owns).

The task scope was Workflow A (digest a UI screenshot). **No UI screenshot was provided** (`gallery: []` in source, `shots: []` in meta.json). Nothing here can be run through the 14-point rubric or the 10-point native-tells audit, because there is no surface to run them against. This is the single most important fact for the synthesis pass: SlapMac contributes **zero UI tokens and zero canon evidence**.

## Tokens

Only brand tokens are observable; none are UI/system tokens. All from a compressed cover render + a compressed 204px webp, so ranges are wide and every value is `(estimated)(inferred)`.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/green-glyph | ~#8DB92E lime-olive | (estimated)(inferred) | mascot fill / wordmark; single-hue brand |
| brand/green-ground | ~#4A5411 → ~#6E7A1E olive radial | (estimated)(inferred) | icon background vignette, dark corners → lighter centre |
| brand/outline | ~#2E3608 dark olive | (estimated)(inferred) | comic outlines on mascot & keys |
| brand/impact | #FFFFFF starburst | (estimated)(inferred) | slap point-of-contact burst |
| brand/wordmark | bold rounded geometric sans, tight tracking | (estimated)(inferred) | "SlapMac" — not SF Pro; a rounded display face |
| icon/frame | legacy rounded-rect squircle, ~22% corner radius, thin light rim + outer glow | (estimated)(inferred) | iOS-5/6-era idiom, NOT Big Sur squircle, NOT Liquid Glass |

No `bg/canvas`, `type/body`, `space/base`, `accent/primary`, `radius/card`, `chrome/*` — because no UI was shown. Do not synthesize these.

## Layout skeletons

None — no app surface was supplied. (Cover skeleton, for completeness: centered logo mockup — mascot lockup upper-two-thirds, wordmark baseline lower-third, full-bleed gradient wall backdrop. This is marketing composition, not product layout, and must not be read as UI.)

## Icon note (brand evidence, not UI)

- **Composition:** 3/4-angle cartoon laptop with an anthropomorphized anguished face, struck by a disembodied hand, white impact starburst at contact. Heavy comic outlines throughout.
- **Frame:** legacy iOS rounded-rect with a thin lighter-green inner rim and a soft outer glow, radial olive vignette (dark corners → lime centre). This is a **pre-Big-Sur icon idiom** — the corner radius and rim treatment predate the current macOS squircle-grid + Icon Composer layered-glass system entirely.
- **Legibility:** low figure-ground contrast — a lime-olive glyph on a mid-olive ground, both similar value. At Dock/Spotlight size the mascot collapses into a muddy green blob; the silhouette does not survive the 16px squint test. This is the icon's dominant defect.
- **Palette economy:** effectively one hue (green) across ground, glyph, and wordmark — monochrome brand, high recognisability but at the cost of internal contrast.

## Signature moves

- The whole product identity is one gag — an anthropomorphized "hurt" laptop mascot. As **brand** it is committed and coherent (single hue, consistent cartoon language between icon and cover). As **native macOS design** there is nothing to evaluate. "Competent brand, zero UI evidence" is the honest verdict.

## Defects

- **No app UI supplied** → the corpus learns nothing about SlapMac's actual interface; flagged so a future pass fetches real screenshots before this entry is trusted for anything.
- **Icon: figure-ground contrast failure** (Contrast Dilution, applied to icon) → lime glyph on olive ground, same value band → illegible at small sizes. Canon icon practice would push the ground darker/desaturated or the glyph brighter to hold a ≥3:1 silhouette contrast.
- **Icon: non-native frame idiom** → legacy iOS rounded-rect instead of the macOS squircle grid / Icon Composer layered treatment → reads as a ported or template icon, not a Mac-native one (Jakob's Law: violates the platform icon schema).

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| (none — no UI surface) | n/a | 14-point rubric and 10-point native audit not runnable: no window, chrome, or controls in any input |
