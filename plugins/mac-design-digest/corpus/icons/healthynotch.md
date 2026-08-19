# Icon: HealthyNotch

- **Era:** big-sur (unified squircle + framed inner tile; glyph deliberately quotes 8-bit game art) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, **128×128 web render** (SHA-1 `2f996458`). Category: Productivity. App: a menu-bar/notch wellness tool — balance score, breaks, and reminders, "all native, all on-device" (tagline "Work shouldn't cost you your health").
- **Resolution caveat:** only a 128px render was available, not the 1024 master. Hex values below are sampled from the 128px original and are reliable for **colour**; fine geometry is not — the pixel-art heart's individual cells blur together and the two-pixel sparkle is at the edge of legibility. Any Icon Composer glass/layer treatment is far below the resolution floor. Bezel/edge lighting is `(estimated)`, not `(measured)`.

| Dimension | Reading |
|---|---|
| Background | **Two stacked fields.** (1) Blue squircle base plate, top-lit vertical ramp **#ACDAFF → #559FFF → #428EFC → #3B86F6** (bright specular top edge → mid cornflower bottom). (2) Inset near-black **navy inner tile**, ramp **#010203 → #071B31 → #0D305C → #153B70** (dark at top → blue bloom at bottom) |
| Glyph | **8-bit / pixel-art heart** (retro-videogame HP heart). Vertical ramp **#CE3158 (red-pink) → #AD2E65 (magenta) → #9C387B (purple)**, pink outline ~**#BD3162**. Optically centred on the dark tile (span ~x42–84 / y37–89 on the 128 canvas; centre ≈ 63,63) |
| Overlay device | **Frame / nested tile** — a dark "screen" tile recessed inside a bright blue squircle plate (~10–11px blue border each side), plus two white 8-bit sparkle pixels **#F3F9FF** top-left of the heart |
| Light model | Primary **top-down**: blue plate bright at top (#ACDAFF lip), heart brightest at top, top-left sparkle. The inner tile inverts this — dark-top → blue-bloom-bottom — reading as **emitted screen glow**, not a second external source. No long shadows; short baked micro-highlights only |
| Layer stack | (system squircle mask + system shadow) → blue base plate (top-lit ramp) → inset dark navy tile (upward blue bloom) → pixel-art heart (red→magenta→purple ramp + pink outline) → two white 8-bit sparkle pixels |
| Palette economy | Exactly **2 hue families**: blue (plate + tile) and red/magenta (heart). Saturation reserved for the heart; the sparkle is the only near-white. Passes the ≤2-hue economy cleanly |

## Signature devices
- **[GOLDEN-NUGGET] The 8-bit HP heart.** A pixel-art heart with the classic two-pixel specular sparkle (top-left), quoting Zelda/arcade "health" hearts. This is committed subject-mining, not template default: the app gamifies work-health ("balance **score**"), and the retro-game heart fuses *health* + *score* into one metaphor. It is the entire personality budget, spent in one place.
- **Nested "screen" tile.** A dark navy inner tile framed inside a bright blue squircle plate — the heart reads as glowing *on a screen*, which suits a menu-bar/notch app that lives on the display edge.
- **Inverted inner glow.** The dark tile is lit from the bottom (dark-at-top → blue-bloom-bottom), the opposite of Big-Sur "sky logic," reading as screen bloom rising under the heart. Committed direction.

## Failures
- **#10 Variant robustness — FAIL (era-conditional).** Identity is welded to the specific dark-navy tile: the pink heart's punch depends on that near-black ground. In tinted/clear/light Liquid-Glass modes the dark tile and blue plate would be replaced and the magenta heart on a light/tinted field would lose contrast and read. Not authored as robust Icon Composer light/dark/mono layers — it is a fixed-appearance mark. (Recorded as a fail against the macOS-26 tinted-mode bar; for a pure Big-Sur icon this check is only partly applicable.)

## Soft passes (flagged for synthesis)
- **#4 16px squint.** Reads as "a pink heart on a dark screen" at menu-bar size, so it survives — but the nested blue frame consumes ~20% of the canvas, shrinking the heart to ~40% of the icon; the individual pixels and the two-pixel sparkle fully smear below ~32px. The frame costs glyph size where glyph size is scarcest.
- **#5 Single light model.** Passes only under the "glowing screen" reading — strictly the blue plate + heart are top-lit while the inner tile emits from the bottom (two implied directions). Narratively coherent (screen bloom), technically dual.
- **#9 Era coherence.** The container is clean Big Sur (uniform squircle, framed tile, baked micro-highlights) and the pixel-art is a deliberate *content* quotation, not an era clash. But the bright baked top-edge specular on the blue plate gestures at Liquid Glass without committing to real translucency/refraction — a mild era straddle, and a baked-highlight the macOS-26 system would rather apply itself.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | pass (full-bleed squircle, art inside mask) |
| 2 | Grid adherence | pass (heart optically centred on tile ≈63,63) |
| 3 | Silhouette | pass (unmistakable heart, even stair-stepped) |
| 4 | 16px squint | soft pass (frame shrinks glyph; pixels/sparkle smear) |
| 5 | Single light model | soft pass (top-lit plate/heart vs bottom-glow tile) |
| 6 | Palette economy | pass (2 hue families, accent on heart) |
| 7 | Figure-ground contrast | pass (magenta #AD2E65 on navy #071B31, ≫3:1, survives grayscale) |
| 8 | Depth coherence | pass (plate → tile → heart → sparkle ordered sensibly) |
| 9 | Era coherence | soft pass (Big Sur base; baked bezel flirts with glass) |
| 10 | Variant robustness | **FAIL** (dark-tile-dependent; no robust light/dark/mono) |
| 11 | Personality | pass (the 8-bit HP heart — strong nameable device) |
| 12 | No-text | pass (no words/UI/photo) |

**Total: 11/12, 1 failure (#10).**

## Rhymes with (hint only — for icon-cluster synthesis)
- **Alcove** (same notch/menu-bar niche, digested 2026-07-19) — shares the **inverted inner glow** (dark-top → lit-bottom) and the **dark recessed field inside a frame**. Where Alcove has no glyph and fails silhouette, HealthyNotch lands a real subject (the heart) inside the same structural idea — a useful contrast pair for the "framed-glow utility" family.
- **Retro-pixel / 8-bit game-glyph icons** — emulator and indie-game icons that put a chunky pixel sprite on a dark tile.
- **"Glyph-on-dark-screen" dev/terminal icons** — a saturated glyph glowing on a near-black tile. Style-family guess: **"pixel glyph on framed dark screen."** Palette-family rhyme: cornflower-blue plate + magenta/pink glyph.

## Brand-context note (cover coherence)
The cover places this exact icon on a blue Liquid-Glass panel over a blue-teal-cream mesh wallpaper, with a white SF-Pro-style headline. The icon's cornflower blue (#428EFC) is coherent with the cover's blue field and the magenta heart is the single warm pop against it — palette discipline holds between icon and marketing. Note a **missed subject-mining thread**: the app is named for the *notch*, but neither icon nor cover carries a notch motif — the heart-as-HP idea is the stronger metaphor and rightly wins, but the name goes unillustrated.
