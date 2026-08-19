# Icon: Purge

- **Era:** big-sur (monogram-on-gradient-squircle, quoting Liquid Glass frosted-glass material on the glyph) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, 240×240 web render (SHA-1 `93de43fa`). Category: Utility. App: an open-source Mac disk cleaner — "Reclaim disk space by clearing caches macOS leaves behind" / "Clean your Mac. Safely."
- **Resolution caveat:** only a 240px render was available, not the 1024 master. Frosted-glass grain, bevel radius, and any true specular are below the resolution floor — edge/material treatment is `(estimated)`. The squircle mask is baked into the PNG as transparent corners (corner alpha 0; ~52px radius at 240px ≈ 0.22×width, a plausible continuous-curvature squircle). Contrast values below are computed from this render; JPEG-free PNG so hue is trustworthy, but the sub-3:1 finding is structural (light frosted glyph on light blue), not a compression artifact.

| Dimension | Reading |
|---|---|
| Background | Vertical ramp **#60A4FF → #5AA0FF → #3B86F7** (light sky-blue top → deeper blue bottom), single hue, "sky logic" light-top→dark-bottom. Softened/lighter than macOS system Blue (`#0088FF`) — reads as a tinted sky-blue |
| Glyph | **Monogram "P"** — large, chunky, geometric, treated as a frosted translucent glass slab. Top-down internal gradient **#FEFFFF → #E1F1FF → #A0CAF7 → #98C7FA** (bright white crown fading to a bluish base). Optically ~centred but oversized: fills ~60–65% of canvas width, crowding the safe-zone margins. Details: a small vertical **counter tick** inside the bowl (bg shows through, #3A84F3) and a subtle **arched notch** cut into the base of the stem |
| Overlay device | **None** — pure monogram on gradient field; no diagonal tool, badge, or frame |
| Light model | Top-down dominant: bg ramp light-top→dark-bottom, glyph bright-crown→bluer-base, short soft baked drop shadow to lower-right + subtle inner bevel. One minor tension — the lower-right drop cast implies upper-left light while the ramp implies straight-overhead. Baked top-edge rim highlight on the squircle (system should supply this) |
| Layer stack | (system squircle mask + system shadow) → blue squircle field with vertical ramp → baked edge rim highlight + faint inner shadow → P drop shadow → frosted-glass P monogram (internal top-down gradient + bevel) → counter tick + specular crown edge |
| Palette economy | **One** hue family (blue) + white glyph. Monochromatic — no separate reserved saturated accent (the app's functional green "Safe to Clean" accent never appears in the mark). Passes ≤2-hue economy; arguably over-economical (nothing focal reserved) |

## Signature devices
- **Frosted-glass letterform.** The P is rendered as a piece of translucent frosted glass — internal top-down gradient, bright specular crown, bluish translucent base — rather than a flat fill. This is the icon's one committed move and its Liquid Glass aspiration, executed as a *baked* single-layer material (not authored as Icon Composer layers).
- **Counter tick + stem arch.** Two small shape-logic details: a vertical accent bar sitting in the P's bowl (a cursor-like tick) and an arched tunnel cut into the base of the stem. Both are lost below ~32px but add close-up character.
- **Sky-ramp brand blue.** Light-top→dark-bottom single-hue blue field — textbook Big Sur "sky logic," and the app's brand blue (reused on the cover and in the app sidebar).

## Failures
- **#7 Figure-ground contrast — FAIL.** Frosted-white glyph on light-blue field never clears the 3:1 floor. Measured: crown #FEFFFF vs bg #60A4FF ≈ **2.5:1**; base #A0CAF7 vs bg #3B86F7 ≈ **2.1:1**. Light-on-light by construction; contrast is worst exactly where the glyph is most detailed (lower stem/counter). Survives grayscale only as a faint mass.
- **#10 Variant robustness — FAIL (judged against its glass aspiration).** Single baked render; the white glyph depends entirely on the blue background for separation. No layered light/dark/clear/tinted authoring — in a tinted or mono system render the frosted P would collapse into the field. The baked rim highlight and drop shadow would also fight the system's own glass effects.

## Soft passes (flagged for synthesis)
- **#2 Grid adherence.** Optically centred but the monogram is oversized — runs close to the safe-zone margins with little breathing room; a wide glyph that could sit on the inner square with more air.
- **#4 16px squint.** The light mass survives as a P-ish blob, but internal detail (counter tick, stem arch) vanishes and the low contrast (#7) muddies the letter — at menu-bar size it reads as "a light shape on blue," weak on specific P-identity. A monogram that softens at its one legibility-critical size.
- **#5 Single light model.** Top-down dominant, but the glyph's lower-right drop cast implies upper-left light — a minor two-source tension.
- **#8 Depth coherence.** Layers ordered sensibly (field → shadow → glyph), no z-fighting, but the baked bevel + inner shadow are slightly muddy at this resolution.
- **#9 Era coherence.** Big Sur construction grammar (gradient field + centred monogram + baked top-down micro-shadow) reaching for Liquid Glass with a frosted-glass glyph material — but baking the highlights/shadows that authentic Liquid Glass forbids. Coherent as a Big-Sur-quoting-glass hybrid, not as either era cleanly.
- **#11 Personality.** The frosted-glass material is a real gesture, but the underlying composition — a single letter on a blue gradient squircle — is the archetypal template-default. One committed move over a stock skeleton.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | pass (designed for squircle; baked rim highlight noted) |
| 2 | Grid adherence | soft pass (oversized, tight margins) |
| 3 | Silhouette | pass (reads as "P") |
| 4 | 16px squint | soft pass (mass survives, ID weakens) |
| 5 | Single light model | soft pass (minor two-source) |
| 6 | Palette economy | pass (one hue + white) |
| 7 | Figure-ground contrast | **FAIL** (2.1–2.5:1, <3:1 floor) |
| 8 | Depth coherence | soft pass (baked bevel muddy) |
| 9 | Era coherence | soft pass (Big Sur quoting glass, baked) |
| 10 | Variant robustness | **FAIL** (baked single-layer, bg-dependent) |
| 11 | Personality | soft pass (one move over template skeleton) |
| 12 | No-text | pass (monogram, not a word) |

**Total: 10/12, 2 failures (#7, #10).**

## Communicates-subject note
A monogram communicates the **brand initial**, not the **subject**. Purge cleans/reclaims disk space — a broom, trash, sparkle, or drained-disk glyph would say what the app does; the "P" says only the name and leans on the wordmark to carry meaning. Not a rubric failure (single-letter monograms are permitted with strong shape logic, and the P's shape logic is adequate), but a missed chance to make the Dock tile self-explaining.

## Rhymes with (hint only — for icon-cluster synthesis)
- **Monogram-on-gradient-squircle utility tiles** — the single-letter brand-initial family (CleanMyMac-adjacent cleaner/utility branding).
- **Frosted-glass-glyph icons quoting Liquid Glass** — glassy translucent foreground on a saturated field, baked rather than layered.
- Palette-family rhyme: **tinted sky-blue single-hue ramps** (softened system-Blue utility icons). Style-family guess: **"frosted-monogram blue-ramp utility."**

## Brand-context note (cover/UI coherence)
The icon's blue is the brand blue: the cover places this exact tile on a near-black cache-grain background under a white "Purge / Clean your Mac. Safely." lockup, and the app sidebar reuses the same mark. Palette coherence is strong across icon → cover → UI. The app UI is dark-mode and introduces a **functional green** ("Safe to Clean") as its accent — deliberately *not* in the icon, so the mark stays a calm monochrome blue while the product's action color lives only in the interface.
