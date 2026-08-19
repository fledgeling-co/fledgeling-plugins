# Icon: Code Meter

- **Era:** Skeuomorphic-quote (a photoreal glossy dashboard **tachometer/redline gauge** with baked specular + reflections, dropped into a Big-Sur front-facing squircle — **not** Liquid Glass) · **Rubric:** 9/12 (3 failures, 3 soft passes) · **Digested:** 2026-07-19
- **Source:** macapp.supply web render. `icon.png` is **256×256** with **transparent corners** (delivered pre-masked as the squircle; alpha=0 outside the mask, so macOS's own rounding is pre-baked). No 1024 master; gloss/specular are **baked raster**, not system-applied. All hex `(estimated)` from the downscaled/compressed render; arc colour stops approximate. `(inferred)` — single icon, single source.

| Dimension | Reading |
|---|---|
| Background | Full-bleed warm **ramp**, light-at-top → dark-at-bottom (sky logic): peach `~#D88B65` (top) → terracotta/rust `~#A64B2C` (bottom) (estimated). No texture; soft vertical/radial gradient fills the entire squircle behind the dial |
| Glyph | **Object** — a glossy black circular **dial/gauge** (car tachometer / VU-meter / volume-knob idiom) nearly edge-to-edge. A ~270° coloured progress arc runs the inner rim from **bottom-left up the left side and over the top** to a bright endpoint pip at ~1–2 o'clock; the right/lower-right rim is a dark unfilled track. Centre: a large orange **"%"** monogram; below it a two-line **"CODE / METER"** wordmark in bold condensed caps. Optically centred, mass slightly high; rim margin to the L/R safe zone is tight |
| Overlay device | None (no diagonal tool, no badge, no frame) — the gauge *is* the whole face |
| Light model | Baked studio/environment gloss, key light upper-left: a bright specular highlight on the raised bezel rim (upper-left), secondary reflections lower-left and right (environment reflections of a glossy 3D object), and a soft inner vignette on the recessed dial face. Background is a separate soft top-down gradient. Short baked shadows — coherent single key, but **rendered-object gloss the current system would rather apply itself** (estimated) |
| Layer stack | peach→terracotta gradient field → glossy raised black bezel (specular rim) → recessed dark inner dial face (vignette/inner glow) → coloured gauge arc (yellow→orange→red) + bright endpoint pip → orange "%" monogram → tan/bronze "CODE / METER" wordmark (front) |
| Palette economy | **Warm-monochrome** — effectively **one** extended warm hue family: the peach→rust background ramp and the yellow→orange→red gauge arc are all warm siblings, over a near-black dial. Accent (saturated orange/red) is reserved for the arc + "%". Very economical; the icon's warmth is a single committed decision |

## Palette (estimated)
- **Background ramp:** `#D88B65` (top peach) → `#C66D4C` (mid) → `#A64B2C` (bottom rust)
- **Dial body:** `#362927` recessed centre → near-black bezel
- **Gauge arc ramp:** `#DA8F3B` (yellow, bottom start) → `#DC863E` (orange, left) → `#D5543A` (red, top) → light peach/white **endpoint pip**
- **"%" monogram:** `~#D6663B` (orange)
- **Wordmark:** `~#5A4438`–`#45332E` (muted tan/bronze) — sits on the dark centre, low contrast

## Signature devices
- **Redline quota gauge** — the arc ramps **yellow → orange → red toward "full,"** the universal fuel/tachometer redline. Pure subject-mining: the app monitors AI-subscription **quota burn**, so the icon is the instrument you'd read to see how close you are to the limit. The colour semantics *are* the product. `[GOLDEN-NUGGET]`
- **Glossy skeuomorphic dial** — a dimensional black knob with a raised bezel, baked specular rim highlight, environment reflections and a recessed vignetted face. A deliberate quotation of the pre-flat skeuomorphic instrument-panel era, wrapped in a modern squircle.
- **Endpoint pip** — a single bright light dot terminating the filled arc (the "current value" marker), the one high-key accent that draws the eye to *where on the gauge you are*.
- **Baked wordmark** — "CODE METER" set literally into the dial face (see Failures #12).

## Failures
- **#4 16px squint** — at menu-bar/Spotlight size the "%" collapses to an indistinct orange blob and the two-line "CODE METER" wordmark smears to mud; only "dark disc + faint warm arc on orange" survives. The informational payload (the reason it's a *meter*) and half the composition (the wordmark) die. Reads acceptably only from ~32px up.
- **#10 variant robustness** — a single-appearance **baked raster**, not authored as Icon Composer layers. The whole reading depends on the warm peach ground + baked gloss; there is no light/dark/clear/tinted construction. macOS 26 Dark/Tinted renders would flatten or muddy it — not forward-compatible with Liquid Glass tinting without a rebuild.
- **#12 no-text check** — contains a baked **"CODE METER" wordmark** (two lines) *and* a "%" symbol. Words in an icon are a classic defect: they shrink illegibly (see #4), don't localise, and duplicate the app label shown beneath the icon anyway.

## Soft passes (borderline — scored pass, flagged for synthesis)
- **#2 grid adherence** — dial is optically centred but **very large**: the bezel nearly touches the left/right safe-zone edges, so margin discipline is tight and the composition reads slightly cramped. Mass also sits marginally high.
- **#3 silhouette test** — the internal figure is a **bare circle**, which reads as a generic dial/knob/clock/lens rather than *instantly* "a usage meter." The meter identity is carried by the arc's **colour and position**, not by shape — so it survives as "a dial" (right family) but not as a unique silhouette.
- **#9 era coherence** — the skeuomorphic glossy dial is a *consistent* quotation (one rendered object, one light), so it holds together; but it's a photoreal instrument inside an otherwise-modern Big-Sur squircle, and the baked specular directly contradicts current HIG ("let the system apply highlights"). Coherent as a quote, dated as a choice.

Also flagged inside a pass: **#7 figure-ground** — the *dial* on peach is high-contrast and survives grayscale, but the tan/bronze **wordmark on the dark centre is low contrast** (`~#45332E` on `~#2E2422`), the weakest link in an otherwise strong figure-ground.

## Rhymes with
- *(hint only)* **Skeuomorphic instrument-gauge** icons — glossy tachometer / speedometer / VU-meter / volume-knob dials with baked bezels and reflections (the dimensional-object family), rather than the flat diagonal-tool (TextEdit/Preview) or concentric-badge (1Password) families.
- **Warm-monochrome terracotta-ground** icons (single warm hue family, peach→rust ramp).
- **Ring/arc-gauge monitor** utilities — icons for usage/quota/time monitors that draw a percentage arc. Loosely rhymes with dashboard/monitor tools in the corpus (e.g. AgentPeek's monitor register, though AgentPeek is flat-mascot not skeuomorphic-gauge). Confirm against future digests before clustering.

## Provenance / caveats
- All hex `(estimated)` from a 256×256 compressed render; `(inferred)` — one icon, one source. No 1024 master; mask corner radius unmeasurable at this resolution.
- Transparent corners mean the file ships **pre-masked** (squircle baked in) — a mild negative signal for layered/appearance-aware authoring; combined with baked gloss, #10 fails on evidence.
- **Brand-coherence with `cover.png`:** strong on the **device**, partial on palette. The cover (dark-mode UI, `~#0E0B09` ground) is wall-to-wall **ring/arc gauges** (42%, 88%, 96% …) — the icon's central motif is the app's core UI element, a genuine subject→icon match. The cover's warning colour (orange/red for high burn) is exactly the icon's ramp. But the cover adds a **green "healthy/under-pace"** accent and a dark ground that the icon omits — the icon shows only the warm/"burning" half of the app's palette. So: same gauge device, warm-subset palette.
- **Era-lag note for synthesis:** another shipping third-party utility icon that is **not** Liquid Glass — but where 1Password/AgentPeek lag *flat* (Big Sur), Code Meter lags *backward past* flat into skeuomorphic quotation. Different failure mode, same root: no Icon Composer layer authoring, so #10 fails.
</content>
</invoke>
