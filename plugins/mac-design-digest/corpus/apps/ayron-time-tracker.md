# Ayron Time Tracker — profile

- **Source:** macapp.supply (`cover.png` marketing composite + `icon.png` brand mark) · **Surfaces digested:** 1 marketing-landing composite containing 3 chrome-less product-concept cards · **Last updated:** 2026-07-19
- **One-sentence identity:** Linear's dark neo-grotesque discipline crossed with a Warp-terminal stopwatch — acid-lime on near-black, monospace metadata, a grotesque display face for the numbers that matter.
- **Cluster:** unassigned (proposed cluster hint: `acid-terminal-dark`)
- **Lineage:** **unknown (low)** — *no native macOS surface was supplied.* The only visual evidence is a **web marketing landing page** (nav: Product/Pricing/FAQ/Blog/Changelog/Docs + Download) and product cards rendered inside it. The tagline calls it "a native Mac timer," but marketing copy is not design evidence and no traffic lights, toolbar, sidebar, menu bar, or system materials appear anywhere. Nothing here may feed macOS canon.
- **Era (chrome):** custom brand aesthetic — not classifiable as Liquid Glass, Big Sur, or legacy-native. Cards are flat opaque graphite panels with a fixed brand accent, not system materials.

## Evidence boundary (read first)

This digest analyses **brand + product-concept design language**, not a shipping native UI. The three cards ("TRACKING", "THIS WEEK", voice-query) are stylized renders embedded in the marketing hero, cut off at the fold, with **zero macOS window chrome**. Treat every reading below as *marketing/concept evidence*, excluded from macOS canon and from native-feel clusters. A real native-window screenshot (settings, main window, menu-bar extra) would be required to classify lineage or run the native-tells audit for real.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| accent/brand | `#D6FF3A` acid lime/chartreuse | (measured)(inferred) | THE identity hue — CTA fill, RUNNING dot+pill, primary data series, icon ground, hero "Invoice out". Fixed brand accent, **not** system `controlAccentColor` |
| data/secondary | `#FF945C` coral-orange | (measured)(inferred) | second data series ("Design" bar/dot); only other saturated hue in the system |
| bg/page | `#050603` near-black | (measured)(inferred) | drenched near-black ground; not pure #000 |
| bg/nav | `#0C0C0D` | (measured)(inferred) | top nav bar, one hair above page black |
| bg/card | `#1A1A1D` graphite | (measured)(inferred) | elevated product cards — depth via lightness step, no shadow/border needed |
| text/primary | `~#F5F4EE` warm off-white | (measured)(inferred) | headlines, time numbers, primary values |
| text/secondary | `~#8E8E8E` gray | (estimated)(inferred) | mono labels; on `#1A1A1D` card ≈ 4:1, borderline |
| stroke/hairline | `#232324` | (measured)(inferred) | card + RUNNING-pill borders; <3:1 vs card fill — near-invisible |
| type/display | grotesque sans, tabular figures (Helvetica Now / Söhne / Geist / Inter-class) | (estimated)(inferred) | hero headline + big time readouts ("01:06:18", "27h 12m"); tight leading |
| type/mono | monospace (SF Mono / JetBrains Mono-class) | (estimated)(inferred) | ALL metadata: uppercase **tracked** section labels + tabular time values ("14h 20m") |
| type/body | grotesque sans, regular + italic | (estimated)(inferred) | subtitles, natural-language query quote (italic) |
| radius/card | ~16–24px | (estimated)(inferred) | scale of the composite is unknown (~2× render) — wide range |
| shape/pill | capsule | (measured)(inferred) | RUNNING status pill, mic button (circle) |
| dataviz/bar | full-width track, category dot + right-aligned mono value + horizontal fill bar | (measured)(inferred) | category breakdown; lime = top series, orange = second |

## Layout skeletons

**Marketing landing composite (dark, web):** top nav bar (`#0C0C0D`) — leading logo ("Ayron / TRACKER" wordmark, lime "A" glyph), centre 6-item menu, trailing lime Download button (the one saturated element in the bar). Hero block, left-aligned on the content margin: two-line grotesque display headline ("Time in." white / "Invoice out." lime), a ~3-line sans subtitle capped near ~45ch, then a primary "Download for Mac" button + ghost "See it live →" + mono reassurance line. Below the fold, a row of 3 product-concept cards on the near-black ground, aurora-green blurred light bleed behind them.

**Product card — "TRACKING" (running timer):** tracked-uppercase mono eyebrow ("TRACKING · NORTHWIND") top-left, capsule RUNNING pill (lime dot + mono label) top-right; oversized grotesque tabular time readout ("01:06:18"); sans-gray subtitle line ("Hero redesign v2 · billable · $150/hr").

**Product card — "THIS WEEK" (summary):** mono eyebrow → oversized grotesque total ("27h 12m") → mono "by category" → legend rows (color dot + sans category label, right-aligned mono duration, full-width horizontal bar beneath each).

**Product card — voice/query:** centred circular mic button (graphite fill, lime glyph), italic natural-language query quote, then a sans answer line + large dollar value.

## Signature moves
- **[GOLDEN-NUGGET] Monospace as the metadata voice.** Every label and every tracked-time value is set in a mono face — uppercase-tracked for section eyebrows, tabular for durations ("14h 20m", "6h 30m"). Paired against a grotesque display sans for headlines and the big timer, this makes tracked time read like *instrument output / a stopwatch readout* rather than app copy. The sans+mono pairing sits on a true contrast axis, which is what lifts this above generic dev-tool dark.
- **One acid accent + exactly one data second-hue.** Lime `#D6FF3A` carries identity, state (RUNNING), the primary CTA, and the top data series; coral-orange `#FF945C` is the *only* other saturated colour, reserved for the second series. Disciplined Von-Restorff economy — the lime is remembered because almost nothing else is coloured.
- **Depth by lightness step, not chrome.** Cards separate from the page via a single graphite step (`#050603` → `#1A1A1D`) with hairline borders that barely register — flat, shadowless elevation.

## Defects
- **Contrast Dilution (minor)** → secondary mono labels `~#8E8E8E` on `#1A1A1D` cards read ≈ 4:1, under the 4.5:1 text floor for the smallest tracked labels → bump secondary label to `~#9A9A9A`+ or enlarge.
- **UI-contrast miss** → card and RUNNING-pill hairline borders `#232324` on `#1A1A1D` are <3:1 (WCAG non-text) → they're decorative, not functional; fine as long as the fill step carries separation, but the border adds nothing.
- **Genericness risk (named, not disqualifying)** → "dark neutral + one electric/acid accent" is the look models reach for unprompted on dev-tool briefs (aesthetic-direction §range-map warning). Ayron earns it back with the mono/sans contrast pairing and the single-second-hue discipline — commitment, not default. Flagged so a derived mock doesn't inherit the reflex without the differentiation.
- **Evidence/positioning gap (not a design defect)** → a product sold as "a native Mac timer" whose entire supplied surface set shows *no* native macOS chrome. Cannot verify the native claim from these assets.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| marketing composite + product cards (web, dark) | 11/14 | #9 secondary mono label ≈4:1 on card; #10 hairline borders <3:1; #14 focus state unassessable (static) |

## Native-tells audit
**Not applicable — no native macOS surface supplied.** Of the 10 checks, 8 are N/A (no chrome, sidebar, toolbar, selection, or controls to audit). Two read as explicit non-native *tells* in the aesthetic (correct for a web brand, wrong if transplanted to a native app): section headers are **tracked-uppercase monospace** (native = system-font semibold sentence-case — the #1 sidebar authenticity tell) and the **accent is a fixed brand lime, not the user's system accent** (native = bind selection/focus/primary to `controlAccentColor`). Recorded as tells + corrections; contributes **0** to any native score.
