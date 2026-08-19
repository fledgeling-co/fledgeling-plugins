# Icon: Screen Studio

- **Era:** Big Sur unified (dark-luminous variant, leans toward custom) · **Rubric:** 12/12 (5 soft passes, no failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp`, SHA-1 `a7bf5c48`. **Resolution caveat: 102×102px web render**, not a 1024 master. Grid, glass refraction, and micro-shadow detail are `(estimated)`, not `(measured)`.
- **Subject:** screen-recording app ("Beautiful screen recordings in minutes"). The glyph is a **record-button "O" / lens aperture** — a subject-mined metaphor, not a generic mark.

| Dimension | Reading |
|---|---|
| Background | Vertical ramp, dark indigo top → near-black bottom: `#1F1340` (top) → `#070310` (bottom-right corner). Top-lit "sky logic". `(measured, low-res)` |
| Glyph | Abstract **ring / torus** (annulus), emissive violet. Not lit top-down — reads as a self-luminous neon ring. Gradient around the ring: `#6939C4` (top-right, dimmer) → `#A136FC` (left, brightest) → `#8436DE` (bottom). Optically centered (vertical dead-on; outer Ø ~78% of canvas). |
| Overlay device | None (no diagonal tool, no badge, no frame). Single centered glyph. |
| Light model | Two-part: background lit from top (lighter indigo up top), ring is **emissive** (its own light source) with a soft radial **bloom** behind it. Center aperture faintly lit (`#130D26`). No hard cast shadow. |
| Layer stack | back→front: (1) near-black squircle w/ vertical indigo→black ramp · (2) radial violet glow/bloom behind ring · (3) emissive violet ring/torus · (4) faintly-lit central aperture |
| Palette economy | **Single hue family** — purple/violet/indigo end to end. Saturated accent (`#A136FC`) reserved entirely for the ring. Textbook economy. |

## Signature devices
- **[GOLDEN-NUGGET] The luminous record-ring on a void.** A self-illuminated violet torus with a soft bloom, floating on a near-black indigo ground. This is a committed *neon-glyph-on-void* direction (subject-mined: the "O" = record), not the Big Sur convention of a soft-top-lit surface object with a tool-at-an-angle. The whole identity is one glowing shape against darkness.
- **Monochrome-purple discipline.** Ground, glow, and glyph are all one hue at different values — no second color anywhere. The brand's purple ring is consistent across surfaces (cover wordmark logo, in-app sidebar mark, app icon), so the icon reads as brand, not decoration.
- **Emissive-over-lit.** The glyph emits rather than reflects; the bg gradient obeys top-down light while the ring obeys its own emission — coherent only under the "the ring is a light source" reading.

## Failures
- None hard. Five **soft passes**, all flagged for synthesis:
  - **#2 Grid** (soft): optical centering good, vertical center dead-on; horizontal centroid pulled left is a brightness artifact of the emissive gradient, not a real offset. Ring outer Ø ~78% of canvas — on the large side of "bold single glyph." True Apple-grid overlay unverifiable at 102px.
  - **#3 Silhouette** (soft): a plain ring is instantly nameable *as a ring/O*, so it passes — but the shape alone is generic (target / lens / spinner / loading-ring / letter O). Subject-communication ("screen recording") rests on color+context, not silhouette. Distinctiveness is carried by the neon-void treatment (check #11), not the outline.
  - **#5 Single light model** (soft): background is top-lit; the ring's own shading is brightest lower-left, contradicting a top-down source. Passes only under the emissive/self-luminous exemption — the direction is artistic, not physical.
  - **#8 Depth coherence** (soft): the bloom/glow is **baked in**. HIG explicitly says don't bake glows into an app-icon layer (the system applies effects) — but for this shipping icon the baked bloom is systematic, purposeful, and accessible → recorded as a **signature move, not a defect**.
  - **#10 Variant robustness** (soft): the ring silhouette survives dark/clear/tinted (shape isn't background-color-dependent), but the entire *identity* is color-bound — a tinted mono render keeps the O and loses the neon soul. No evidence of authored Icon Composer Default/Dark/Mono variants (single web render).

## Rhymes with
- **Neon-glyph-on-void family** (hint for synthesis, not yet a promoted cluster): dark near-black squircle + one glowing brand mark (ring/orb/wave/bolt) in a single saturated hue, emissive with a soft bloom. The current wave of creative/AI/recording pro-tools reach for this. Closest reference peers: dark-mode Raycast-adjacent utility icons, nocturnal audio/creative tools that put a single luminous brand primitive on black. Needs ≥2 more independent dark-luminous icons in the corpus before this becomes an icon cluster.
