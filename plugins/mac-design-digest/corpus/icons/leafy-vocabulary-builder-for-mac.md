# Icon: Leafy: Vocabulary Builder for Mac

- **Era:** custom (flat hand-lettered wordmark — off-model, no macOS era material language) · **Rubric:** 7/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, 180×180 web render (SHA-1 `7984b29c`). Category: Productivity. App: a systemwide word-lookup utility ("Press ⌥A to lookup any word on mac, auto save in vocab"). Website leafyapp.uk.
- **Resolution caveat:** only a 180px, pre-masked render was available (transparent squircle corners — the rounded mask is already baked into this PNG, not delivered full-bleed as a real macOS 26 icon would be). The 1024 master was not provided. Brush-stroke edge texture is heavily anti-aliased at this size; fine detail is `(estimated)`. Core palette hexes are `(measured)` from the render.

| Dimension | Reading |
|---|---|
| Background | Near-flat vertical ramp **#333333 → #000000** (charcoal at top edge → pure black at bottom). The lift is faint and reads as a top-down ambient wash on an otherwise black field |
| Glyph | The full word **"LEAFY"** hand-lettered in a brush/marker style, filled bright chartreuse (core **#AFF85E**, ramp **#A6F252 → #B3F963**, anti-alias highlight to **#D5FC99**). No safe-zone margin — lettering runs full-bleed to all four mask edges. Reads simultaneously as text and, via a long diagonal stroke, as a leaf blade with a central vein |
| Overlay device | **Other — a diagonal leaf-midrib stroke** sweeping lower-left → upper-right, crossing/anchoring the letterforms (the "vein" that turns the wordmark into a leaf). Not a tool, but occupies the diagonal-tool position |
| Light model | Effectively **flat / no model** — the glyph is an unlit flat green fill with no baked shadow or specular. Only the background carries a faint top-lighter charcoal→black gradient. No mixed sources (nothing to conflict), but nothing modelled either |
| Layer stack | (baked squircle mask) → charcoal→black field → green hand-lettered "LEAFY" wordmark + diagonal midrib. Two planes only; no glass, no tool overlay, no discrete shadow plane |
| Palette economy | Neutral field (charcoal→black) + **one** hue (acid chartreuse). The green *is* the accent; no second reserved accent. Passes the ≤2-hue economy floor comfortably |

## Signature devices
- **The word-as-leaf wordmark.** The whole icon is the brand name hand-lettered so the letterforms + a diagonal midrib stroke resolve into a leaf silhouette — a genuine subject-mining move (leaf = the app's name and mascot). This is a *committed direction*, not a template glyph-on-gradient; the personality is entirely here.
- **Highlighter-on-black palette.** One high-voltage acid green (#AFF85E) on pure black — a streetwear/marker-sticker temperature, not the Big-Sur "sky-ramp" convention. Contrast is enormous (green L≈89 vs black L≈0, >15:1).
- **Full-bleed lettering, zero safe zone.** The brush strokes deliberately touch every mask edge — a poster/logo instinct, which is also the source of most of its failures below.

## Failures
- **#2 Grid adherence — FAIL.** No safe-zone margin at all; the lettering is full-bleed and crowds the mask on all four sides. Nothing is optically centred on the Apple grid — it's a poster wordmark scaled to fill, so at the Dock it will feel edge-cramped next to grid-disciplined neighbours.
- **#3 Silhouette test — FAIL.** Filled solid black, the mark is an illegible tangle of overlapping brush strokes — neither a clean nameable object nor readable text. The dual leaf/word reading means the silhouette resolves to a busy blob, not a single figure.
- **#4 16px squint — FAIL.** At menu-bar/Spotlight size the word collapses into an unreadable green smear on black; letters merge, the leaf read is lost. It becomes "a green blob," failing Dock/Spotlight/menu-bar duty — the most damaging miss for a utility that lives in the menu bar.
- **#10 Variant robustness — FAIL.** Identity is 100% dependent on acid-green-on-black. Not authored as Icon Composer light/dark/clear/tinted layers; in tinted or clear modes the green-vs-black contrast that *is* the design would not translate. No carrying silhouette survives a recolour.
- **#12 No-text check — FAIL.** The icon **is** a full word ("LEAFY"). Words in icons are the archetypal defect — they shrink badly (see #4) and read as a logo dropped into a squircle rather than a system icon.

## Soft passes (flagged for synthesis)
- **#1 Mask discipline.** The render is pre-masked (baked squircle, transparent corners) rather than full-bleed square, and the lettering fights the mask by crowding into the corners. Fits the squircle shape, but doesn't respect it.
- **#5 Single light model.** Passes only because it's flat — there's no modelled light to be inconsistent. The absence is itself the note: no depth, no specular, no baked micro-shadow.
- **#9 Era coherence.** Internally consistent (uniformly flat), but belongs to no macOS era — a flat brand-sticker execution that specifically ignores the current Liquid Glass layer/material language. Uses the system squircle mask and nothing else of the platform vocabulary.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | soft pass (pre-masked; edge crowding) |
| 2 | Grid adherence | **FAIL** (no safe zone, full-bleed) |
| 3 | Silhouette | **FAIL** (brush-tangle blob) |
| 4 | 16px squint | **FAIL** (unreadable green smear) |
| 5 | Single light model | soft pass (flat, no model) |
| 6 | Palette economy | pass (1 hue + neutral) |
| 7 | Figure-ground contrast | pass (>15:1, survives grayscale) |
| 8 | Depth coherence | pass (2 flat planes, no z-fight) |
| 9 | Era coherence | soft pass (off-era flat) |
| 10 | Variant robustness | **FAIL** (green-on-black dependent) |
| 11 | Personality | pass (word-as-leaf, committed) |
| 12 | No-text | **FAIL** (full word "LEAFY") |

**Total: 7/12, 5 failures (#2, #3, #4, #10, #12).** Note: three of the four non-negotiable checks (#2, #3, #4 — grid, silhouette, 16px) fail. As a generation reference this is a cautionary example, not a model: a strong brand mark that is a weak app icon.

## Rhymes with (hint only — for icon-cluster synthesis)
- **Wordmark / logo-sticker icons** — the "brand logo poured into a squircle" family: identity carried by lettering, not by a small-legible object. Antithesis of the Big-Sur tool-on-gradient tradition.
- Palette-family rhyme: **acid-green-on-black**, adjacent to the terminal/hacker aesthetic (black + highlighter green) but hand-brushed rather than mono/pixel. Style-family guess: **"hand-lettered brand-sticker on black."**

## Brand-context note (cover coherence)
Cover is the same black ground + same acid green, with a soft **green glow halo** behind the icon (website compositing, not part of the icon file). Beside it the brand sets a refined **white serif "Leafy" logotype** — elegant, high-contrast display serif. That serif is a much stronger, more legible brand asset than the crude brush icon; the palette coheres (black + #AFF85E throughout) but the *lettering* tone does not — the marketing logotype and the icon look authored by two different hands. If the serif logotype (or a single leaf glyph derived from it) were the icon subject, most of the failures above would resolve.
