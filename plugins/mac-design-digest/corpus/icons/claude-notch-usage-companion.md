# Icon: Claude Notch Usage Companion

- **Era:** custom (8-bit pixel-art / retro-arcade sprite — not Big Sur, not Liquid Glass) · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply icon crop (`icon.png`, 100×64px, non-square) + `cover.gif` for brand-context · **Category:** Dev
- **Subject:** a menu-bar/notch utility that renders live Claude usage in the Mac notch (GitHub: claude-notch-tracker)

| Dimension | Reading |
|---|---|
| Background | flat `#000000` (fully opaque black — not transparent) `(measured)` |
| Glyph | mascot — a chunky pixel-art creature (Space Invaders "crab"-family alien): rounded body, two knockout-black eye pixels, side nubs (ears/antennae) protruding L+R, 2–3 downward leg nubs. Single flat hue `#CE7D5C` clay/terracotta `(measured)`; darker edge tones `#B66E51`→`#824F3A`→`#372119` are **bilinear-resize anti-aliasing, not an intended ramp** `(estimated)`. Sits slightly high-of-centre in the crop `(measured)` |
| Overlay device | none (no diagonal tool, no badge, no frame) |
| Light model | none — flat pixel-art, zero gradient / specular / top-down shading. Absent *by convention*, coherent with the 8-bit language `(measured)` |
| Layer stack | 2 planes: `[black field]` → `[terracotta sprite w/ 2 knockout eyes]` |
| Palette economy | 1 hue family (Claude clay) on black; no accent needed — the whole glyph is the accent. `#CE7D5C` ≈ Claude's own clay brand tone (~`#CC785C`/`#D97757`) `(estimated)` |

## Signature devices
- **[GOLDEN-NUGGET] Brand-colour subject-mining as the mascot's body.** The creature is rendered in Claude clay `#CE7D5C` — the app tracks *Claude* usage, so the icon says its subject through palette, not through a literal glyph. Non-template: it reads "Claude" without a logo.
- **[GOLDEN-NUGGET] Pixel-art mascot (retro-arcade quotation).** A deliberate 8-bit sprite in a corpus of squircle/glass icons — the personality is entirely carried by the arcade-critter form. Rhymes with the terminal/hacker family crossed with playful/toy.
- **Monochrome-on-black framing.** Single hue on pure black gives >7:1 figure-ground and reads as an arcade sprite lit only by its own colour — the same de-emphasis discipline as a good UI, taken to one-colour extremity.
- **Knockout-pixel eyes.** Two black cut-outs in the body do all the "face" work — the charm mechanism, cheap and legible.

## Failures
- **#1 Mask discipline — FAIL (as-delivered, caveated).** Delivered as a 100×64 non-square banner with an opaque black field; no squircle canvas, no safe-zone, no evidence the art was composed for the system mask. This is very likely a macapp.supply web-render crop of the notch/menu-bar sprite rather than the true 1024² app-icon canvas (a crisp source probably exists in the GitHub repo but was not provided). Treat as *unverifiable*, not proven-bad.
- **#2 Grid adherence — FAIL (unverifiable).** Cannot check against the Apple 1024² grid — no square canvas. Within its crop the sprite is roughly optically centred but sits slightly high.
- **#10 Variant robustness — FAIL (era-appropriate).** The glyph relies on the black ground for its contrast and has no glass layering, so it would not survive clear/tinted Liquid-Glass renders as-is. Expected for a flat pixel sprite — noted, not condemned.

## Soft passes
- **#4 16px squint — SOFT PASS.** As a bold blocky blob it survives to menu-bar/notch size (that is literally its native duty — the cover shows it living in the notch). But the source is already bilinear-smeared, and the thin leg/ear nubs + eye dots would merge below ~24px; recognisability as a *creature* (vs. a clay blob) is borderline at 16px.

## Rhymes with
- Pixel-art / 8-bit indie mascot icons (retro-arcade sprite family) — currently a stylistic outlier in this corpus (squircle & Big-Sur-flat icons dominate).
- Menu-bar / notch utilities by *function* (agentpeek, alcove, bartender-6, backdrop) — but stylistically it shares none of their squircle/glyph vocabulary; it's the pixel-sprite exception in that functional cluster.

## Notes for synthesis
- Resolution honesty: 100×64px, non-square, opaque-black. Edge-hue variance (`#CF7D5C`/`#D07E5D`/`#C77859`/`#372119`) is resize anti-aliasing — the true sprite is a **single flat clay hue**; do not record a glyph ramp.
- Brand coherence with cover is strong: cover shows the same clay sprite in a black notch pill beside white "57%" and a **mint/emerald progress ring ~`#55D29D`–`#62D2A5`** (usage-remaining accent, tinted by the desaturated-green leaf photo behind it) `(estimated)`. That green lives in the *product UI*, not the icon — the icon is clay-on-black only.
- One data point for a possible "pixel-art / retro-mascot dev-utility" icon cluster; needs ≥2 more independent icons before any promotion.
