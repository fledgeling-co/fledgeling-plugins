# Icon: Viaduct

- **Era:** big-sur (iOS-style baked render quoting Liquid-Glass materiality) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, 256×256 web render (SHA-1 `cdabed8d`). Category: Productivity. App: "Run any Chrome extension in Safari directly from Webstore" (Magic Elk Labs) — a converter that ports Chrome extensions to native Safari.
- **Resolution caveat:** only a 256px render was available, not the 1024 master. The bevel, specular catch, and inner-arch recess are judged from a downscaled raster — edge/glass treatment is `(estimated)`, not `(measured)`. Sub-pixel rim anti-aliasing is soft.
- **Delivery tell:** corners are fully transparent (alpha 0) — the icon ships **pre-masked** as an iOS superellipse with a baked edge-rim light, baked specular, and a baked ambient-occlusion drop shadow. This is an iOS App Store icon reused on Mac, not an Icon Composer full-bleed square. HIG says provide unmasked square layers and let the system apply effects; this bakes all three.

| Dimension | Reading |
|---|---|
| Background | Near-black charcoal field, subtle vertical ramp **#313131 (top) → #131313 (bottom)** with a baked light edge-rim/bevel (#5D5D5D–#9F9F9F) along the top-left of the squircle |
| Glyph | **Object** — a viaduct/aqueduct portal: two piers + an arched opening capped by a horizontal lintel beam. Teal-glass extrusion with beveled top faces. Optically centred, slightly heavy (fills ~60% width) but inside the safe zone |
| Overlay device | **None** — a single centred glyph, no diagonal tool, no badge, no frame |
| Light model | Top-down. Baked specular catch **#BFFCF4** on the lintel top-left face and arch crown; lit body **#458C83**, undersides fall to **#295D5F**. Glyph casts a soft baked ambient-occlusion shadow onto the field; the arch opening is a modeled dark recess (a tunnel/passage) |
| Layer stack | (baked squircle mask + baked edge rim) → charcoal ramp field → baked glyph AO shadow → teal-glass viaduct (piers + lintel, beveled) → baked specular catch + inner-arch recess shadow |
| Palette economy | Neutral near-black field + **one** hue family (teal/viridian glass ramp). The glyph *is* the accent; no separate reserved accent. Passes ≤2-hue economy |

## Signature devices
- **Literal-monument glyph.** The app is named *Viaduct* and the icon is a literal viaduct/aqueduct arch — subject-mining taken to the limit: the name is the picture. A committed direction, not a template SF-symbol-on-gradient.
- **Teal-glass extrusion.** The arch reads as a physical extruded object with beveled top faces and a bright specular catch (#BFFCF4), giving it dimensional weight rather than a flat fill.
- **Dark-field spotlight.** A single luminous teal object on a near-black shelf — the field is dark and quiet so the one glowing form carries all the identity. Atypical for Big Sur (which favours light gradient fields); a deliberate moody read.
- **Modeled inner-arch recess.** The arch's negative space is a dark tunnel (inner shadow), reinforcing "passage/portal" — an honest metaphor for the product (passing extensions *through* from Chrome into Safari).

## Failures
- **#10 Variant robustness — FAIL.** A baked raster with no separable Icon Composer layers: the identity depends on its one baked near-black field and baked teal glyph. On macOS 26 dark/clear/tinted renders there is nothing to recompose — the dark field can't invert and the teal can't recolor. Direct evidence: transparent-cornered flat PNG, baked shadow/specular, no layer separation.

## Soft passes (flagged for synthesis)
- **#1 Mask discipline.** Geometry fits a standard iOS superellipse and the glyph doesn't fight the mask — but the mask, the edge-rim light, the specular, and the drop shadow are all baked in. If macOS applies its own squircle + specular on top, the baked rim can conflict (double-treatment / faint inset). Passes on shape, flagged as non-native authoring.
- **#7 Figure-ground contrast.** The lit upper glyph is far above 3:1 on black, but the shadowed lower piers (#32615E/#295D5F, L≈0.10) against the darkest bottom field (#131313, L≈0.006) dip to ~2.5:1 — the pier bases soften into the field. Silhouette survives via the lit portions.
- **#9 Era coherence.** Internally consistent (all glossy-teal, all top-lit) but era-ambiguous: Big Sur construction (front-facing squircle, baked micro-shadow, soft top light) quoting Liquid-Glass materiality (specular, translucency) while baking it as a raster. Coherent as a look, not as an era.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | soft pass (baked mask + effects) |
| 2 | Grid adherence | pass (optically centred, safe-zone) |
| 3 | Silhouette | pass (arch/portal instantly nameable) |
| 4 | 16px squint | pass (arch shape holds at 32px; inner bevel smears but silhouette reads) |
| 5 | Single light model | pass (consistent top light) |
| 6 | Palette economy | pass (one hue + neutral) |
| 7 | Figure-ground contrast | soft pass (lit portions >3:1; shadowed pier bases ~2.5:1) |
| 8 | Depth coherence | pass (field → shadow → glyph → recess ordered; no z-fighting) |
| 9 | Era coherence | soft pass (Big Sur build quoting baked glass) |
| 10 | Variant robustness | **FAIL** |
| 11 | Personality | pass (literal teal-glass monument) |
| 12 | No-text | pass |

**Total: 11/12, 1 failure (#10).** Checks 1–4 (the non-negotiables) all clear.

## Rhymes with (hint only — for icon-cluster synthesis)
- Dark-field indie utility/dev-tool icons that spotlight **one glowing glassy object on near-black** (rather than a light Big Sur squircle). Style-family guess: **"dark-field glowing-object utility."**
- Extruded-3D-object-on-black family; and literal-monument/architecture glyphs where the app name is drawn as its namesake structure. Palette-family rhyme: teal/viridian glass ramps (#BFFCF4 → #295D5F).

## Brand-context note (cover coherence)
Cover is a teal→mint gradient field (viridian brand hue, ~#0D9488 family) with a white slab display + italic serif lockup ("Run any Chrome extension. / Now native in Safari.") over a dark app-window mock whose primary button is the same teal. The icon's teal glyph (#458C83/#3F8179) and near-black field both echo the cover — **coherent brand palette** (teal identity hue + dark UI surface run across icon and marketing). The icon is the darker, moodier sibling of the brighter teal cover.
</content>
</invoke>
