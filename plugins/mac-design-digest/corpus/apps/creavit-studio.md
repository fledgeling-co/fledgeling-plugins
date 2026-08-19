# Creavit Studio — profile

- **Source:** macapp.supply (cover + icon only; no in-app shots supplied) · **Surfaces digested:** marketing cover composite (with a bokeh-blurred, 3D-tilted app-window glimpse) · **Last updated:** 2026-07-19
- **One-sentence identity:** A Screen Studio / Cap-class screen-recording beautifier whose *only* supplied evidence is a drenched-black OG-card marketing hero — so we know its brand (amber-graphite two-tone, rounded-geometric display) but essentially nothing measurable about its app.
- **Cluster:** unassigned (brand-only evidence; no app-UI surface to cluster)
- **Lineage:** unknown (low) — no native chrome (traffic lights / sidebar / toolbar) is visible; the single app glimpse is bokeh-blurred beyond classification. Category peers split both ways (Screen Studio = native SwiftUI; Cap = Tauri/web), so lineage is genuinely undecidable from this image. Non-native-or-native cannot be asserted → contributes **zero to macOS canon**.
- **Era (chrome):** unknown — the blurred glimpse shows only a dark editor panel with a clip title + waveform; no material/chrome cues survive the depth-of-field and chromatic-aberration styling.

## Evidence caveat (read first)

This is a **marketing composite**, 1200×630 (standard social/OG card), almost certainly @1x. The left third is a brand lockup + headline + CTA on near-pure black; the right two-thirds is a heavily blurred, tilted, lens-flared 3D product render. The app window inside it is **not analyzable** — every pixel of real UI is out of focus. All app-UI readings below are `(estimated)`/`(insufficient-evidence)`. The brand layer *is* legitimate evidence and is analyzed as such. Per the skill's boundary rule for "no actual app UI": recorded honestly, digest proceeds on the brand layer, and the corpus should treat this app as **awaiting real in-app screenshots**.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | `#020202`–`#030306` near-pure black, faintly cool | (measured)(inferred) | drenched-black stage; blue channel ~3pts over red at midtones |
| brand/accent-amber | `#F2BF00` (242,191,0) | (measured)(confirmed) | icon field colour; the one committed identity hue — warm golden/amber |
| brand/graphite | `#2B2B2B` (43,43,43) | (measured)(confirmed) | icon dark panels; also the tone of the blurred app editor |
| brand/blue | `#1722BD` (23,34,189) saturated | (measured)(inferred) | appears in the blurred product render; likely a secondary in-app accent |
| brand/headline-white | `#F8F8F8` | (measured)(inferred) | display headline |
| brand/cta-fill | `#F6F5F6` off-white pill | (measured)(inferred) | capsule CTA |
| brand/cta-text | `#111111` on white | (measured)(inferred) | Apple glyph + "Download for free" |
| brand/subtext | `#656565` on near-black ≈4.0:1 | (measured)(inferred) | "No sign-up required · Free to try" — under the 4.5:1 floor (see Defects) |
| type/display | rounded-geometric bold sans (Poppins / Gilroy / SF Rounded-class), ~52–56px cap-tuned, leading ~60px (~1.08×) | (estimated)(inferred) | "Turn boring screen recordings into beautiful videos", 2 lines, tight display leading |
| type/wordmark | same family, semibold, ~28–32px | (estimated)(inferred) | "Creavit Studio" |
| type/cta | ~18–20px, medium | (estimated)(inferred) | |
| type/subtext | ~14–15px | (estimated)(inferred) | |
| layout/left-rail | ~68px left margin, shared by icon+wordmark, headline, CTA, subtext | (measured)(inferred) | one clean vertical axis (≈8pt grid) |
| icon/silhouette | rounded-square (superellipse) on transparent corners; two graphite panels split by a full-height white divider, side handle-notches | (measured)(inferred) | flat two-tone, no gradient/depth; reads as a before/after screen frame (boring→beautiful) |
| app/editor-glimpse | dark near-black editor; a clip element titled "Clip …" over a waveform row | (insufficient-evidence) | bokeh-blurred + chromatic aberration; not measurable |

## Layout skeletons

**Marketing cover composite (1200×630, @1x).** Left rail on a ~68px axis: brand lockup (28–32px icon + "Creavit Studio" wordmark) → generous gap → two-line rounded-geometric display headline (~54px) → large gap → capsule CTA (white pill, Apple glyph + label, ~72–80px tall) → tight gap → muted 15px reassurance subtext. Right two-thirds: full-bleed near-black bleeding into a depth-of-field 3D render of a device/panel showing the app's dark editor (a "Clip" media item + waveform), a yellow+blue object matching the brand, and a vertical lens-flare streak. No app window is legible.

**App window:** not reconstructable from this evidence.

## Signature moves

- **[GOLDEN-NUGGET] Amber-graphite two-tone identity (`#F2BF00` + `#2B2B2B`).** In a video/screen-recording category that defaults to electric blue, violet and gradient meshes (Screen Studio, Descript, Loom), committing to warm golden-amber on graphite is a deliberate, category-differentiating rotation — the app's whole recognizability in one hue pair. The icon's split-panel-with-white-divider carries a legible before/after-screen metaphor (the product's actual job).
- Otherwise **competent but anonymous**: the cover is the current template-default creator-tool hero — drenched black + one rounded-geometric headline + a single white pill CTA + a bokeh 3D product render. Well-executed, but the composition itself is not a committed direction; only the palette is.

## Defects

- **Marginal text contrast** → the "No sign-up required · Free to try" subtext measures `#656565` on ~`#050505` ≈ **4.0:1**, under the 4.5:1 WCAG floor for normal text → canon would lift it to ~`#8A8A8A`+ or enlarge it into large-text territory. (Only observable design miss; everything else on the composite passes.)
- **Data-quality, not an app defect:** the app window is bokeh-blurred / 3D-tilted / chromatic-aberration-styled → no app-UI evidence. Not counted against the app; recorded so synthesis doesn't mistake absence for a pass.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| marketing cover composite | 9/10 applicable | #9 subtext contrast ≈4.0:1. Checks #6/#12/#13/#14 N/A (no paragraphs/inputs/labels/focus). Native-tells audit **N/A** — no app chrome visible; app window unanalyzable. |
