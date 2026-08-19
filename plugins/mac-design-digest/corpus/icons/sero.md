# Icon: Sero

- **Era:** custom (dark emissive emblem — Big-Sur squircle container quoting Liquid-Glass luminosity) · **Rubric:** 12/12 (5 soft passes, 0 failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, **1024×1024** (SHA-1 `d7db62a3`). Category: AI. App: Sero — "Search with zero resistance. Private local AI retrieval for documents, research, and developer knowledge." (local/offline RAG search).
- **Resolution caveat:** clean native 1024 master, no visible compression banding on the gradient. **But the PNG is pre-masked** — corners carry alpha 0 (transparent squircle), and a soft drop shadow + a faint top-edge rim highlight are **baked into the raster**. This is a fixed web/AppKit-style render, *not* a square unmasked Icon Composer layer set. So variant behaviour (Default/Dark/Clear/Tinted) is `(inferred)` from the single artwork, not observed.

| Dimension | Reading |
|---|---|
| Background | Near-black cool ground, essentially **flat #161616 (edges) → #14283C (center navy)** with a subtle radial vignette; squircle corners transparent (baked mask). Not a Big-Sur "sky" ramp — it's a dark void the ring lights |
| Glyph | **Abstract ring / aperture** (a torus). Optically dead-centre (center ≈ 512,520 — ~8px low, correct optical nudge). Round glyph uses the larger grid circle: outer Ø ≈ 684px ≈ **67% of canvas**, band stroke ≈ 100px (~10%). Reads as the "**O**" of Sero and the **zero** of "zero resistance" |
| Overlay device | **None** — no diagonal tool, no badge, no frame. The glyph carries the whole icon |
| Light model | **Emissive / self-luminous:** the ring *is* the light source, blooming outward into the black ground; a faint baked top-rim environment highlight on the squircle edge; a radial vignette darkens the aperture's eye. No top-down scene light |
| Layer stack | (baked squircle mask + baked drop shadow) → near-black ground → emissive bloom halo → **conic blue→lavender ring (focal)** → radial center vignette (inside the ring's eye) → faint top-edge rim highlight |
| Palette economy | Near-black neutral ground + **one adjacent-hue sweep** (electric blue → periwinkle → pale lavender-white). Saturation reserved entirely for the ring. Passes ≤2-hue economy comfortably |

## Palette (sampled hex, `(measured)`)
- **Ground:** `#161616` (left edge) · `#1C2225` (upper) · `#101C28` (lower) · `#14283C` (center vignette). Corners `alpha 0`.
- **Ring — conic sweep** (0°=right/3-o'clock, sweeping clockwise): `#E0D1FF` (right, palest lavender) → `#D1CDFF` (lower-right) → `#92BCFD` (bottom) → `#41A8FC` (bottom-left, brightest cyan-blue) → `#189FFC` (left, electric blue) → `#119DF9` (top) → `#62B0FF` (upper-right) → `#ADC4FE` (top-right periwinkle). Bluest at 9-o'clock, palest at 3-o'clock.
- **Accent:** electric blue `#189FFC` is the identity hue; lavender-white `#E1D1FF` is the jewelry highlight.

## Signature devices
- **The emissive aperture (glyph-as-light-source).** The ring doesn't sit *in* a lit scene — it *is* the light, bleeding a bloom halo into the black. This is the whole personality in one move, and it's a committed direction, not template glyph-on-gradient. Subject-mining is honest: **ring = the O of Sero = zero (zero resistance) = a search lens/portal**, three readings from one shape.
- **Conic blue→lavender gradient sweep.** The ring rotates through electric blue on the left to pale lavender-white on the right — an iridescent tint that rhymes with Liquid-Glass specular colour, applied to a 2D emissive ring rather than a refracting glass layer.
- **Radial center vignette ("the eye").** The aperture darkens toward its middle, giving the flat ring depth — you read *into* it, like a lens barrel or a void. Cheap, effective dimensionality without a second object.
- **Baked Big-Sur container hygiene.** Pre-masked squircle + soft drop shadow + faint top rim highlight — the container is drawn in the Big-Sur front-facing idiom, but statically raster-baked (the effects HIG says to let the system apply). A native-hygiene deviation worth flagging, not a composition flaw.

## Failures
- **None.** No check falls below its bar. The five borderline checks are recorded as soft passes below.

## Soft passes (flagged for synthesis)
- **#1 Mask discipline.** Artwork fits the squircle cleanly with no corner-radius mismatch — but it **bakes the drop shadow, the top-rim highlight, and the mask into the raster**. HIG: provide square unmasked layers and let the system apply shadow/rounding. Passes the check as written (doesn't fight the mask); flagged because it's a fixed render, not layered artwork.
- **#4 16px squint.** Glyph survives — a bright ring on dark is identifiable at menu-bar size and the center detail loss is harmless. Flagged: the ~10% stroke thins toward ~1.6px at 16px (the bloom rescues it), and the near-black container edge is defined only by the baked shadow, so on a dark Dock/wallpaper it can read as a floating ring rather than a bounded tile.
- **#5 Single light model.** Predominantly one coherent emissive story (ring lights the void). Flagged: a faint top-rim highlight implies a *second*, top-down environment light on the container — two sources coexisting (an emissive object in a top-lit room), consistent but not strictly single.
- **#9 Era coherence.** Internally consistent as a contemporary dark emblem. Flagged: it's a **hybrid** — a Big-Sur front-facing squircle container, a custom dark-emissive treatment, and a Liquid-Glass-adjacent iridescent tint — belonging to no single system era.
- **#10 Variant robustness.** **Passes where its cousin fails** (cf. alcove #10 FAIL): Sero has a **carrying glyph** — the ring silhouette survives mono/tinted/clear renders because identity rests on the *shape*, not the background colour. Flagged: the *drama* (bloom + blue→lavender iridescence) is contingent on the black ground and would collapse to a plain tinted ring; and as a baked raster it doesn't actually participate in the system's Default/Dark/Clear/Tinted layer generation.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | soft pass (baked mask/shadow/rim) |
| 2 | Grid adherence | pass (optically centred, ~67% round-glyph fill, safe-zone) |
| 3 | Silhouette | pass (an annulus/ring — instantly nameable; the O/zero) |
| 4 | 16px squint | soft pass (thin stroke, dark-on-dark bound) |
| 5 | Single light model | soft pass (emissive + faint top rim) |
| 6 | Palette economy | pass (near-black + one adjacent-hue sweep) |
| 7 | Figure-ground contrast | pass (ring L≈70–210 vs ground L≈20, ≫3:1, survives grayscale) |
| 8 | Depth coherence | pass (ground → bloom → ring → vignette ordered, no z-fight) |
| 9 | Era coherence | soft pass (Big-Sur container + custom emissive + LG tint hybrid) |
| 10 | Variant robustness | soft pass (glyph survives; glow drama is ground-dependent) |
| 11 | Personality | pass (emissive aperture — nameable, subject-mined) |
| 12 | No-text | pass (geometric ring, not a set letterform) |

**Total: 12/12, 0 failures, 5 soft passes.**

## Rhymes with (hint only — for icon-cluster synthesis)
- **Dark luminous-emblem** icons: a single geometric glyph rendered as its own light source on a near-black ground. Style-family guess: **"emissive glyph on black"** (AI/utility register — the Raycast/Arc/terminal-dark neighbourhood).
- Direct corpus cousin: **alcove** — both are dark grounds with a glowing focal and an iridescent cool ramp, both raster-baked. Sero is the stronger of the pair: it has a carrying silhouette and a subject-linked glyph where alcove leans wholly on the gradient field (which is why alcove fails #3 and #10 and Sero doesn't).
- Palette-family rhyme: **electric-blue → lavender iridescence** — the Liquid-Glass specular-tint palette borrowed onto flat emissive art.

## Brand-context note (cover coherence)
The cover pairs the same dark UI (`sero` lowercase wordmark, near-black chrome) against a **blue → pale-lavender/pink gradient sky** — the exact hue axis of the icon's ring sweep. The ring mark reappears bottom-right on the cover as a dark squircle with the blue ring. Strong palette coherence: the icon's `#189FFC → #E1D1FF` ramp *is* the brand's sky. This is a committed, product-linked colour system, not an incidental icon palette.
