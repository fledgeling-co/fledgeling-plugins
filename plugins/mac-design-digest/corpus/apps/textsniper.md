# TextSniper — profile

- **Source:** macapp.supply · **Surfaces digested:** marketing cover composite (1 image); app icon present but out of scope (Workflow B) · **Last updated:** 2026-07-19
- **One-sentence identity:** A menu-bar OCR utility whose only supplied evidence is a candy-bright marketing banner — brand energy of a Raycast/CleanShot-era indie utility, but zero native window chrome to digest.
- **Cluster:** unassigned (no native UI evidence to place it)
- **Lineage:** native (low confidence) — **inferred from product category + icon grammar, NOT from any observed window.** TextSniper is a Vision-framework menu-bar OCR tool; its icon follows Apple's squircle grammar. No traffic lights, toolbar, menu-bar extra, settings, or capture-overlay chrome was actually shown, so this lineage call cannot feed macOS canon.
- **Era (chrome):** unknown for UI (no chrome seen); the **icon** reads Big-Sur-era squircle (glossy central lens dome, not a flat Icon-Composer/Liquid-Glass treatment) `(estimated)`.

## What was actually provided (honesty note)

Only two images exist for this app: `cover.png` (2400×1260 marketing composite) and `icon.png` (1024-canvas app icon). **Neither is a screenshot of the running application.** The cover is a promo collage; the icon is icon-workflow evidence. There is therefore **no native surface to measure** — no window background, no control heights, no sidebar/toolbar, no selection grammar. Everything below is BRAND evidence off the composite, marked as such, and must not be promoted as macOS design taste.

The composite is worth reading for two things only: (1) the product's brand aesthetic, and (2) the one genuine product-design idea it depicts — the capture overlay.

## Tokens (BRAND evidence — marketing composite, NOT app UI)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | indigo→violet vertical-wave gradient, ~#6055B9 deep → #8E80CA light, darkening to ~#493FA2 lower-right | (estimated)(inferred) | soft moiré wave striations; the banner's whole ground |
| brand/headline | pure white #FFFFFF, heavy grotesque, ~2-line tight leading | (measured)(inferred) | "Copy text from anywhere" — brand display type, not a UI label |
| brand/card-green | bg ~#D5F297 chartreuse, deep-teal-green title text | (estimated)(inferred) | "Scan QR codes on Mac" feature card |
| brand/card-pink | vivid magenta ~#E63FA6 bg (QR panel), white QR modules | (estimated)(inferred) | sample polluted by pale QR overlay; magenta read visually |
| brand/card-blue | bg ~#B6D6F4 pale sky, navy title, violet waveform ~#6D4CFF→#8F8BFD | (estimated)(inferred) | "Text-to-Speech / Recognize and Read Aloud" |
| brand/accent-lime | ~#C5D600 chartreuse display type over orange | (estimated)(inferred) | inside the mock video ("Salehe Bembury") |
| brand/card-radius | large soft ~24–34px rounded rects | (estimated)(inferred) | marketing card radius, NOT a native control radius |
| icon/base | pale-blue rounded squircle, glossy blue→purple lens dome, 4 white serif-bracket "T" marks in an expand/X arrangement | (estimated)(inferred) | icon = Workflow B; recorded here only as brand context |

No native tokens (bg/canvas, type/body, space/base, chrome/*) are recordable — none were observable.

## Layout skeletons

**cover.png — marketing composite (not a UI surface):** Indigo wave backdrop. Top-left white headline block (2 lines). A center-weighted collage of a fake YouTube thumbnail (orange gradient + sneaker photo + lime title) wrapped in a thin white marquee-selection rectangle with a crosshair reticle at its lower-right and a white rounded result strip beneath (YouTube glyph + crosshair). Three feature cards fan out at the edges: green QR card top-right, magenta QR-code card right, pale-blue Text-to-Speech card bottom-left. Deliberately overlapping collage depth — NOT an 8pt-grid layout, NOT app chrome.

## Signature moves

- **[GOLDEN-NUGGET] The capture overlay mirrors the OS's own screenshot tool.** The one depicted product surface — a thin marquee-selection rectangle plus a crosshair/target reticle over dimmed content — is a deliberate copy of macOS's native `⌘⇧4` screen-capture affordance. That is a real, defensible product-design decision (Jakob's Law: reuse the mental model the user already owns for "select a region of the screen") — but it is depicted inside a marketing collage, so it cannot be measured as native chrome. If a real capture-overlay screenshot arrives, this is the surface to digest.
- **Brand: jewel-bright feature isolation.** Each capability gets its own saturated card in a distinct hue (chartreuse / magenta / sky) against a calm indigo ground — Von Restorff isolation applied to a feature list. Brand-layer only.

## Defects

- **No app UI supplied** — not a design defect, an evidence gap. Cannot run the native-tells audit at all.
- **Contrast (marketing, minor):** deep-teal title on chartreuse card ("Scan QR codes on Mac") is the one marginal text pair in the composite; readable but the lowest-contrast label present. Brand asset, not held to WCAG UI floors here.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.png (marketing composite) | ~7/14 applicable, remainder N/A | The 14-pt UI rubric largely does not apply to a promo collage: #1 grid, #2 alignment (deliberate overlap), #8/#11/#12/#13/#14 (no controls/inputs/focus) all N/A. Of applicable checks — #3 proximity, #4 scale, #5 leading, #6 measure, #7 de-emphasis — it reads competently; #9 contrast marginal on the green card. Native-tells audit: N/A (no native chrome). |

## Knowledge gaps for this app (what to bring next)

Everything native. Needed to actually profile TextSniper: the **menu-bar-extra dropdown**, the **capture crosshair overlay** in situ, and the **Settings/Preferences window** (light and dark). Until then this profile is brand-only and contributes nothing to canon.
