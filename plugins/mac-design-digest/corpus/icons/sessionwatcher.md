# Icon: SessionWatcher

- **Era:** Big Sur unified (front-facing squircle, top-lit gradient glyph, baked contact shadows — **not** Liquid Glass: no specular edge highlights, no refraction, no translucency) · **Rubric:** 11/12 (1 failure, 2 soft passes) · **Digested:** 2026-07-19
- **Source:** macapp.supply web render. `icon.png` is **256×256px, pre-masked** (corners ship transparent, alpha 0 — the squircle radius is baked into the raster, not a full-bleed layer). No 1024 master; all hex/geometry `(estimated)` from the 256px render. `cover.png` (2400×1260) confirms brand-coherence and the wordmark-logo reuse.

| Dimension | Reading |
|---|---|
| Background | **Ramp** — near-black charcoal, subtle top-down vertical gradient `#313131` (top) → `#131313` (bottom), with a faint lighter inner-edge rim (~`#4C4C4C` at the mask border, a soft inner bevel). Single hue, essentially achromatic gray (estimated) |
| Glyph | **Abstract** — a three-bar ascending chart (short → tall, left → right), each a vertical rounded-cap bar. Silver/pewter metallic fill, top-lit gradient `#ECECEC` (top) → `#888888` (bottom), mid ~`#C9C9C9`. Group optically centred horizontally, baseline-aligned, seated slightly below vertical centre with balanced safe-zone margins (estimated) |
| Overlay device | None — no diagonal tool, no badge, no frame. Just the centred data glyph |
| Light model | Top-down. Each bar lighter at its top, darker at its foot; a short soft **contact shadow** pools beneath/behind each bar (`~#131313` on the `#1F1F1F` field). No specular glass highlight, no long dramatic shadow — Big-Sur baked-micro-shadow habit (estimated) |
| Layer stack | charcoal squircle tile (top-down ramp + faint inner-edge rim) → per-bar baked contact shadows → three top-lit silver bars (each its own vertical gradient + slight top-edge bevel), front |
| Palette economy | **Achromatic** — 0 hue families, 2 grayscale ramps (dark charcoal ground + silver glyph). No accent, no saturation anywhere. Figure-ground contrast is very high (silver `#D9D9D9` on `#1A1A1A` ≈ 13:1) by monochrome default rather than reserved-accent discipline |

## Signature devices
- **Ascending-bars-as-subject** — the app tracks live AI-coding usage, cost and rate limits in the menu bar; the icon *is* the growth/analytics bar chart it draws. Direct subject-mining: the glyph names the function. `[GOLDEN-NUGGET]`
- **Monochrome-metal restraint** — the entire personality budget is spent on a silver-on-charcoal grayscale with zero colour. Most utility icons reach for a saturated accent; the deliberate absence reads "pro instrument / menu-bar native" and is the one committed direction here.
- **Baked contact shadows + top-lit bars** — soft short shadows lift each bar off the field; a Big-Sur-era depth move (the kind of shadow the Liquid Glass system would rather apply itself).

## Failures
- **#10 variant robustness** — the composition is authored as a single Big-Sur raster, not layered/appearance-aware construction. The silver glyph's legibility is **load-bearing on the dark field**: silver bars only read against the near-black ground. In a macOS 26 Clear/Light-tinted render the dark tile would lift and the silver-on-light bars would collapse toward invisibility. No invert/light variant is evident. (The monochrome nature *does* help Dark/Mono tinting — it is only the light-tinted case that breaks — but the check asks for background-independence, which this lacks.)

## Soft passes (borderline — scored pass, flagged for synthesis)
- **#1 mask discipline** — composition clearly respects the squircle safe zone (centred glyph, generous margins), but the render is **pre-masked with a baked corner radius**; I cannot verify a full-bleed square layer, so mask-fighting is unobservable rather than confirmed-absent. Passed on composition evidence.
- **#11 personality** — the three-ascending-bar chart is the single most off-the-shelf "stats/analytics" glyph; on device choice alone this reads template. It clears the check only on the committed **monochrome-metal** execution (the no-colour restraint + top-lit silver treatment), not on the glyph itself. This is the icon's template-risk axis.

## Rhymes with
- *(hint only)* **Achromatic data-glyph utility** icons — an abstract chart/meter symbol rendered in metallic gray on near-black, no accent (the "pro menu-bar instrument" family) rather than the diagonal-tool (TextEdit/Preview) or mascot (AgentPeek) families. Shares AgentPeek's *achromatic, subject-literal, dark-field-dependent* logic but swaps mascot for abstract chart and white-ground for black-ground. Confirm against future digests before clustering.

## Provenance / caveats
- All hex `(estimated)` from a 256px render; `(inferred)` — single icon, single source.
- Mask corner radius unmeasurable at this resolution; corners ship transparent (baked squircle), so the delivered-to-Apple full-bleed layer is not observable here.
- **Brand-coherence with `cover.png`:** deliberate and strong on the glyph, split on accent. The site wordmark logo reuses the **exact bar-chart mark** in a small dark rounded square beside "SessionWatcher" — icon and logo are one system. The cover ground is the same near-black charcoal the icon uses. **But** the site's only saturated colour is an Apple-blue CTA (`~#0088FF`) that appears **nowhere in the icon** — the icon is stricter (pure monochrome) than the brand environment. Palette coherence: dark-ground + silver/white type, yes; accent, no.
- **Era-lag note for synthesis:** like AgentPeek and 1Password, SessionWatcher ships a flat Big-Sur-era icon in the Liquid Glass era — further evidence that shipping third-party dev/utility icons lag the current icon language and are not authored for tinted/clear variants.
