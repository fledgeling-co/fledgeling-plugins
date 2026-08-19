# Icon: Mole

- **Era:** custom (flat two-tone brand-mark) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 500×500 web render — circular crop, corners transparent) · **Category:** Utility · **App:** "A native Mac utility for cleaning, analyzing and optimizing" (mole.fit)

| Dimension | Reading |
|---|---|
| Background | flat cream `#FBF3E7` `(measured)` — no ramp (top `#FAF6E8`, right `#FCF4E8` = antialiasing, not sky-logic gradient) |
| Glyph | mascot — naturalistic side-profile mole (facing left, sitting), espresso `#28190C`→`#2A1A0F` `(measured)`; sits slightly low and left-weighted (snout + forepaw crowd the lower-left), optically centred within ~70% of the field |
| Overlay device | none — no diagonal tool, no badge, no frame |
| Light model | flat / null — pure 2-tone silhouette; zero gradient, zero baked shadow, zero specular. Declines both Big Sur top-down lighting and Liquid Glass environmental refraction |
| Layer stack | back→front: (1) flat cream field; (2) espresso mole silhouette; (3) negative-space cutouts *within* the silhouette (eye dot, 3 claw slits, haunch/hind-leg divider swoosh) that reveal the field beneath — 2 planes + subtractive detail, not stacked layers |
| Palette economy | 2 colours total, 1 warm hue family (espresso on cream); accent: none. Maximally economical |

## Signature devices
- **Negative-space anatomy** `[GOLDEN-NUGGET]` — the eye, the three digging claws, and the haunch/hind-leg divider are all cut *back to the cream field* through the single espresso mass rather than drawn in a second ink. One ink, one field, all internal detail is subtractive. Elegant, but it is exactly what breaks variant robustness (the detail dies if the field changes colour).
- **Digging-claw forepaw as subject-mining** `[GOLDEN-NUGGET]` — the spade-like front paw with three splayed claws is the one detail that disambiguates "mole" from "generic rodent/shrew," and it doubles as the product metaphor: the utility *digs through* your disk to clean it. Subject mined for the one memorable feature.
- **Two-tone flat brand-mark (logo-as-icon)** — this reads as a wordmark's lockup glyph dropped on a field, not an icon built in Icon Composer. Strong brand personality, deliberately no system-native icon dimensionality.
- **Circular-badge presentation** (brand-level) — the mark lives inside a circle across the cover logo and the app's toolbar lozenge; the espresso-on-cream direction inverts to white-on-dark on the (cool, nocturnal) cover.

## Failures
- **#10 Variant robustness (Liquid Glass era)** — the negative-space eye, claws, and haunch divider *depend on the cream field showing through*. There is no layer separation and no Icon Composer authoring, so dark / clear / tinted renders cannot be system-generated cleanly: on a dark field the espresso glyph collapses toward the background and the subtractive detail inverts illegibly. Shipping a Utility in 2026 with a fixed 2-tone mark forgoes the entire current-era variant set.

## Soft passes (flagged, scored as passes)
- **#1 Mask discipline** — presented as a circle on transparency (macapp.supply's crop), so the raw square field and squircle behaviour cannot be verified. The brand uses a circular badge everywhere, so there is a real risk the shipped `.icns` bakes a circle inside the 1024 square (visible corners after the system squircle). Composition itself would mask fine. Re-digest if a true 1024 square appears.
- **#2 Grid adherence** — glyph sits a touch low; the forepaw claws approach the lower-left safe-zone edge. Reads centred, but not optically pinned to the grid.
- **#4 16px squint test** — the animal silhouette survives, but the three thin claw slits, the small eye dot, and the hairline haunch divider all smear at menu-bar size; reads as "a dark creature," loses "mole."

## Rubric ledger
| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Mask discipline | soft pass | circular web crop; can't verify square field / baked-circle risk |
| 2 | Grid adherence | soft pass | sits low-left, claws near lower-left margin |
| 3 | Silhouette test | pass | sitting animal w/ pointed snout + clawed forepaw; claws sell "mole" |
| 4 | 16px squint | soft pass | silhouette survives; claw slits / eye / haunch line smear |
| 5 | Single light model | pass | consistent (null) lighting, no mixed sources |
| 6 | Palette economy | pass | 2 colours, 1 hue family, no accent |
| 7 | Figure-ground contrast | pass | espresso on cream = 15.5:1 `(measured)`; survives grayscale |
| 8 | Depth coherence | pass | single plane, no z-fighting (trivially — zero depth) |
| 9 | Era coherence | pass | internally coherent flat 2-tone language |
| 10 | Variant robustness | **FAIL** | negative-space detail is field-dependent; no dark/clear/tinted path |
| 11 | Personality | pass | hand-crafted naturalistic mascot; not glyph-on-gradient |
| 12 | No-text check | pass | pure vector silhouette, no words/UI/photo |

**Score: 11/12** (1 failure: #10; 3 soft passes: #1, #2, #4)

## Rhymes with (hint only)
- Flat two-tone **animal-mascot brand-marks** presented as icons — the "solid creature silhouette on a warm flat field" family (think Ulysses/Bear-class animal marks, GitHub-Octocat-style solid-silhouette logic). Its lineage is **branding/logo craft**, not Big Sur or Liquid Glass icon craft — file it against a future "logo-mark-as-icon" icon cluster, not the dimensional-squircle cluster.

## Notes for synthesis
- **Resolution caveat:** 500×500 web render, circular crop by macapp.supply; corners transparent. Cannot confirm shipped square field or mask discipline — flag for re-digest at 1024.
- **Palette-temperature split (brand coherence):** the icon is warm (cream + espresso); the app UI and marketing cover are cool-nocturnal (deep navy + teal aurora, dark cards). The **mole animal is the brand through-line, not the palette** — the cover even inverts the mark to white-on-dark. Notable warm-icon / cool-app mismatch worth watching if more of this developer's work is digested.
- One-specimen observation; nothing promotable to canon. Its most transferable lesson is the negative-space-anatomy technique and its exact cost (kills variant robustness) — a clean case for the "flat two-tone mark forgoes the Liquid Glass variant set" trade-off.
