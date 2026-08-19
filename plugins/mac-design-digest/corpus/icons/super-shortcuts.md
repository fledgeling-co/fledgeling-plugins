# Icon: Super Shortcuts

- **Era:** flat-transition (flat-design language; see caveat) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 512×512 PNG, RGBA) · **Category:** Productivity — local task-automation app
- **One-line read:** A favicon-grade flat brandmark — white lightning bolt on a single flat green field — that ignores every macOS-era icon convention (no depth, no lighting, no glass, no full-bleed square) but reads instantly at any size.

## Era caveat (read before trusting the tag)

This is **not** a faithful macOS-era icon. It commits to the flat-design visual language (flat fill + flat glyph, zero gradient, zero shadow), which the era model buckets nearest to **flat-transition** — but it lacks that era's free-form silhouette and simple gradients, and it predates none of Big Sur's depth or Liquid Glass's layers. In practice it is a **platform-agnostic flat web brandmark** (the same asset would serve as a favicon, an iOS tile, or a web logo unchanged). Synthesis should treat it as the "flat single-glyph-on-color, no-era" reference, not as period evidence for Yosemite-Catalina.

| Dimension | Reading |
|---|---|
| Background | Flat `#1F9D6F` — a single, genuinely uniform fill (17,890 identical samples on a 3px grid; no ramp, no vignette, no texture) `(measured)` |
| Glyph | Object — a white `#FFFFFF` lightning bolt, tilted ~10° right. Bbox 155–369 × 79–431; centre (262, 255) vs field centre (255, 255) → dx **+7px** (accounts for the bolt tilt), dy 0. Sits on optical centre. `(measured)` |
| Overlay device | none |
| Light model | **None.** Flat design — no light source, no baked micro-shadow, no specular, no dimensionality. Internally consistent by absence, but forgoes the macOS depth convention entirely. |
| Layer stack | 2 planes, no shadow layer: (back) flat green field baked into a rounded-rect with transparent corner margins → (front) white bolt glyph |
| Palette economy | 1 hue family (green) + 1 neutral (white glyph), **no accent**. Maximally economical — the entire icon is two colours. |

## Geometry & mask

- **Opaque field:** 38–472 on both axes within a 512 canvas → a **434px rounded-rect with ~7.4% transparent margin per side**. Corners are baked into the artwork (top row at y=38 spans x 124–387, widening downward), not left for the system. `(measured)`
- **Glyph fill:** bolt is 214px wide × 352px tall — ~81% of field height. A thin diagonal, so optical weight stays moderate despite the tall bounding box; top/bottom safe margins ~41px each.
- **Figure-ground:** white on `#1F9D6F` = **3.44:1** `(measured)` — clears the 3:1 graphics/icon floor, below the 4.5:1 text floor (not required for a large glyph). Survives grayscale cleanly.

## Signature devices

- **Lightning-bolt-as-automation** — the speed/power/"instant" metaphor. Nameable, but it is the *category-default* glyph for this problem space (Apple Shortcuts, Tasker, Raycast-adjacent utilities all reach for a bolt). Personality present, commitment generic — subject-mining would have found a less-trodden mark (a keystroke chord, a repeated-action loop — the cover's own `^ ⌥ ⌘ R → make text red` motif is far more distinctive than the bolt).
- **Two-colour flat field** — the whole icon is `#1F9D6F` + `#FFFFFF`. Reads at 16px without smear; that legibility is the icon's one genuine strength.
- **Baked rounded-rect mask** — a web/favicon convention (pre-rounded PNG with transparent corners) transplanted onto a Mac icon that expects a full-bleed square.

## Failures

- **#1 Mask discipline — FAIL.** Ships a pre-masked, pre-rounded, non-full-bleed shape (434px rounded-rect inset in a 512 canvas, transparent corners). Apple's rule is *"provide square, unmasked layers; the system rounds the corners."* In the Dock, macOS applies its own squircle over this: the icon renders as a slightly-inset rounded-rect whose own corner radius (~20% of the shape) does **not** match the system squircle proportion (~22.4% superellipse) of sibling icons — it will read as subtly the wrong shape next to native peers.
- **#10 Variant robustness — FAIL.** A flat raster with baked colours and no layer/mono separation. No Dark, Clear, or Tinted variant is derivable — in tinted/clear appearances there is nothing for the system to recolour gracefully. Not authored in Icon Composer; not appearance-aware.

## Soft passes (flagged, scored as pass)

- **#5 Single light model** — flat, so trivially consistent (zero lighting to contradict), but there is no light model at all; no macOS dimensionality.
- **#8 Depth coherence** — no depth system to be incoherent; a single plane + glyph. Coherent by absence.
- **#11 Personality** — a bolt is nameable, so it passes, but it is the category cliché rather than a committed, mined device.

## Rubric ledger

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Mask discipline | **FAIL** | baked rounded-rect + 7.4% transparent margin; not full-bleed; radius won't match system squircle |
| 2 | Grid adherence | pass | glyph optically centred (dx +7 from tilt, dy 0), ~41px safe margins |
| 3 | Silhouette | pass | a lightning bolt — instantly nameable filled black |
| 4 | 16px squint | pass | bold single bolt on solid green; no detail to smear |
| 5 | Single light model | soft pass | flat; consistent by absence, no lighting |
| 6 | Palette economy | pass | 2 colours total, 1 hue family, no accent |
| 7 | Figure-ground | pass | 3.44:1, clears 3:1 graphics floor; survives grayscale |
| 8 | Depth coherence | soft pass | single plane, no z-fighting; no depth system |
| 9 | Era coherence | pass | uniformly flat language, no mixed-era devices |
| 10 | Variant robustness | **FAIL** | baked colours, no mono/layers; no dark/clear/tinted adaptation |
| 11 | Personality | soft pass | bolt present but the automation-category cliché |
| 12 | No-text | pass | no words, no photo, no UI screenshot |

**Score: 10/12** (2 failures: #1, #10 — both are the non-negotiable/system-facing checks, so the score overstates Dock-readiness; the icon is legible but not macOS-native).

## Brand / palette coherence

Icon green `#1F9D6F` vs the cover: the cover reuses green as its sole accent on a near-black `#0C120E` ground (headline mint `#5FD08D`, embedded icon tile ~`#26B16B`). Same hue family, but the marketing greens are **brighter and more saturated** than the icon's more muted, teal-leaning `#1F9D6F` — a mild palette drift (the shipped icon and the cover's own icon-tile render are not the same hex). Brand identity is coherent at the family level; the exact green is not locked.

## Rhymes with (hint only — for synthesis)

- Flat single-glyph-on-solid-color brandmarks (favicon/app-store-tile grade) — the "no-era flat" family.
- Automation/productivity icons leaning on the lightning-bolt speed metaphor (Apple Shortcuts lineage).
- Awaiting ≥2 corroborating icons before any device or palette promotes.
