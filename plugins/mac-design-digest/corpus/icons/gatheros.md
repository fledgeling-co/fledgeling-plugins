# Icon: GatherOS

- **Era:** Liquid Glass (macOS 26 Tahoe+) · **Rubric:** 12/12 (4 soft passes, 0 failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp` **204×204** (small web render; see resolution caveats) · app is "The Mac app for design inspiration" (a moodboard / save-and-organize inspiration tool, gatheros.co)
- **One-line:** a frosted-glass monogram on a charcoal field, its only colour the light refracting through it — a logo-as-icon that reads as brand, not function.

| Dimension | Reading |
|---|---|
| Background | Dark diagonal ramp `#3E3E3E` (top-left) → `#030303` (bottom-right) (measured) — light source top-left, inverting the Big Sur light-sky convention |
| Glyph | Bold rounded letterform (reads "D"/"G", ambiguous) with a circular counter and a squared notch cut into the left edge; frosted-glass body ~`#AEB2B5` (measured); optically centred, generously sized |
| Overlay device | None (no diagonal tool / badge / frame); the chromatic dispersion is a material property, not a compositional overlay |
| Light model | Environmental Liquid-Glass: top-left key drives the bg ramp and specular catches on upper/left glass edges (`#C4C8CB`–`#D8DCDD`); short soft baked inner-shadow in the counter; prismatic dispersion stands in for a coloured bounce |
| Layer stack | dark diagonal-gradient field → frosted-glass letterform body → prismatic dispersion tint (blue/violet/warm caustics) → specular edge highlights |
| Palette economy | One neutral glass hue + a dark neutral field; three **desaturated** dispersion tints (blue `#84AABB`, violet `#9786B7`, warm-cream `#B7B395`) belong to one material, not competing accents. No saturated accent |

## Signature devices
- **[GOLDEN-NUGGET] Prismatic glass dispersion** — chromatic aberration painted across a frosted neutral letterform: cool blue pools lower-left, violet on the upper-right, a warm olive-cream patch on the right edge. This reads as white light refracting through a solid glass shape — the whole personality of the icon in one move, in lieu of a flat accent colour.
- **Dark full-bleed field with diagonal top-left light** (`#3E3E3E`→`#030303`) — inverts the Big Sur light-at-top sky ramp; the glyph is read by luminance, not by hue, so it survives tinting.
- **Bold rounded monogram, counter + side-notch** — a single geometric letterform mass; the same mark is used as the app's wordmark logo in marketing (logo-as-icon strategy).

## Failures
- None outright. Four soft passes:
  - **#2 grid** — glyph is sized generously and crowds the safe-zone margins (right curve and left arm sit close to the field edge) but stays inside; optically centred.
  - **#3 silhouette** — holds as a single bold mass with a clear counter when filled solid, but the subject is an ambiguous letterform (D? G? a plug/connector?), not *instantly nameable* as an object. For a design-inspiration tool, the icon communicates brand, not function — the subject-mining miss.
  - **#6 palette economy** — the frosted body is one neutral, but the dispersion introduces three hues; defensible only because they are one glass material's caustics (all low-saturation), not three accents.
  - **#10 variant robustness** — the glyph is luminance-driven and would survive dark/clear/tinted, but the dark field and dispersion are baked; true Icon Composer light/clear/tinted layer behaviour is unverifiable at 204px.

## Resolution caveats
- 204×204 web render, **below Dock/@2x resolution.** Specular and dispersion analysis is from an upscale; edge micro-detail, true layer separation, and whether the glass/specular are system-applied (Icon Composer) vs baked into the artwork cannot be confirmed. The 16px and 32px squint tests (done by downscaling the render) both hold: bold mass + counter survive at 16px, the notch and faint tints return by 32px, high figure-ground contrast throughout.
- **Palette/brand coherence** (from `cover.png`): the app UI is white with a black wordmark and a black pill CTA; the icon's dark field + single prismatic moment coheres with that black/white brand while the iridescence rhymes with the colourful inspiration thumbnails the app collects.

## Rhymes with
- The **dark-glass monogram** family: current-era utility icons that render a single frosted-glass glyph on a near-black field with baked specular and chromatic dispersion (Raycast-adjacent dark-glass, Arc-ish glass marks). Style guess: "glass monogram on charcoal" — pending ≥2 more members before any icon-canon promotion.
