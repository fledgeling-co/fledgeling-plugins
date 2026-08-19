# Icon: MacRest

- **Era:** Big Sur unified (pre-Tahoe) · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, SHA-1 `e1498846`) · **App:** MacRest, Utility — "Let your Mac actually sleep." (a sleep/wake-control utility)
- **Resolution caveat:** source is **208×208px**, a resized web render — not the 1024 master. All hex values are `(estimated)` from the render; sub-16px behaviour and full-bleed-vs-baked-rim mask discipline are `(inferred)`, not measured.

| Dimension | Reading |
|---|---|
| Background | Vertical ramp `#ED5F82` (top) → `#FF85A7` (bottom) — one rose hue. **Inverted ramp**: darker/more-saturated at top, lighter at bottom, contra the Big Sur light-top→dark-bottom sky convention. |
| Glyph | Crescent moon (object), pale-pink gradient `#FFF1F6` (upper-left highlight) → `#F8C9D7` (lower), edge `#F9DCE4`. Dominant, optically centred slightly left-of-centre, ~55% of canvas. |
| Overlay device | Gear **badge**, pale pink `#F9CED2`, top-right, seated in the crescent's opening with its own soft drop shadow. Reads as "settings/control" affordance. |
| Light model | **Mixed / contradictory.** Moon lit top-left; background ramp brightens toward the *bottom*. Baked soft ambient drop shadows under moon and gear (short, soft, no direction cue). No specular / no glass. |
| Layer stack | back → front: (1) rose squircle + vertical ramp + faint rim highlight; (2) crescent moon w/ baked drop shadow; (3) gear badge w/ own soft shadow, overlapping the moon notch. |
| Palette economy | **One hue family** (rose) end to end — background, moon, and gear are all pink. No reserved accent: the gear, which should be the focal "control" detail, is the same pale pink as the moon, so it does not pop. |

## Signature devices
- **Moon + gear pairing** — subject communication is legible: crescent = sleep, gear = *you* control it. The single clearest thing this icon does right; the glyph tells you the app's job.
- **Monochrome high-key rose** — the whole icon in one soft, pastel rose. This is the committed aesthetic direction and it is genuinely distinctive: sleep/power utilities almost universally go dark, blue, or graphite; a warm high-key pink is an off-distribution choice for the category. It is also the source of two rubric failures (contrast, variant robustness) — the boldness and the flaw are the same decision.
- **Bottom-lit inverted ramp** — darker top, lighter bottom; a deliberate glow-from-below rather than the Big Sur sky ramp.

## Failures
- **#5 Single light model (fail):** moon highlight is top-left while the background ramp brightens toward the bottom — the two elements disagree on light direction. Mixed lighting per icon-anatomy §3.
- **#7 Figure-ground contrast (fail):** high-key pink-on-pink. Measured `(estimated)` moon-vs-background **2.09–2.92:1**, gear-vs-background **2.25:1** — both under the 3:1 floor. The moon only separates because of its baked drop shadow, not fill contrast; in grayscale the fills wash together.
- **#10 Variant robustness (fail):** not an Icon Composer layered design; glyph/background separation is entirely hue-and-shadow dependent on the one rose background. Would collapse under tinted / clear / dark Liquid Glass renders — there is no light/dark/mono variant set.

## Soft passes (flagged, scored as pass)
- **#4 16px squint:** the crescent moon survives at menu-bar size, but the gear's teeth smear into a nub below ~24px and its low contrast (2.25:1) makes it read as an ambiguous blob. The app is still identifiable from the moon alone.
- **#1 Mask discipline:** artwork lives inside the squircle, but the render shows a self-drawn rounded-rect rim highlight — at 208px I cannot confirm whether a full-bleed 1024 layer was delivered for the system to mask, or a pre-masked squircle was baked in (the latter fights macOS 26's own masking).

## Rhymes with
- Big Sur "glyph-on-gradient-squircle" family: a single nameable object floating on a one-hue vertical ramp with baked micro-shadows. Style-family guess: **monochrome-pastel Big Sur utility** — the consumer-wellness/sleep register (soft, domestic, non-technical) rather than the graphite pro-utility register. *(Hint only — needs ≥2 more single-hue-ramp icons in the corpus before this is a real cluster.)*

## Cross-icon / synthesis notes
- **Brand-coherence divergence (worth a synthesis flag):** the marketing `cover.webp` renders the *same* icon **inverted** — a near-black charcoal squircle with a **pink** crescent + pink gear. That version has strong figure-ground (pink pops on dark) and would survive dark/tinted modes — i.e. the marketing art quietly fixes the shipped icon's #7 and #10 failures. The shipped app icon and the app's own hero art disagree, and the hero art is the better icon. Palette coherence between icon and cover is *thematic* (rose + moon) but *tonal-inverted*.
- **Era lag:** a Big Sur-era icon shipping into macOS 26 (Liquid Glass). No glass layers, no specular, no variant annotations — a generation behind the platform.
