# Icon: Glance

- **Era:** Big Sur unified (soft-shadow tile) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/glance/icon.png`, 1024×1024, indexed-PNG with baked transparent squircle corners — a genuine full-res asset, not a web resize) · **App:** Glance — "native Markdown viewer/editor for macOS"

| Dimension | Reading |
|---|---|
| Background | Near-white ramp #FFFFFF (top) → #E7E7E7 (bottom) (measured); reads as flat at any size. Overlaid with faint notebook/table grid lines ~#EBEBEB–#F2F1F2 (measured), brightness dip of only ~15/255 — a whisper texture that vanishes below ~64px. Grid is asymmetric (one vertical line in the left third, three uneven horizontals), so it reads as a hand-placed paper grid, not a symmetric UI lattice. |
| Glyph | Mascot face — two vertical rounded-rectangle "eyes" (fill #181818, measured; ~130×230px each, symmetric about the 512 centre at x≈385 / x≈630) plus a curved charcoal smile (#333333–#414141, measured) below. The eyes double as code-editor **block cursors** (subject-mining: a Markdown editor), each carrying a faint inner top-down chevron/inset gradient. Optically centred horizontally; the face sits high, leaving quiet space at the chin. |
| Overlay device | Faint full-bleed grid texture (not a diagonal tool/badge). It is behind the glyph, so functionally a background texture rather than an overlay. |
| Light model | Soft ambient, nominally top-down: short, soft baked halos/glows around eyes and smile (edge falloff #757575), a single specular dot on the smile's right terminal, and the background's light-top → darker-bottom ramp. Reads as soft-plastic / clay emboss, not a hard directional drop shadow. One consistent model. |
| Layer stack | back → front: (1) near-white background ramp · (2) faint grid lines · (3) soft glyph halos/shadows · (4) dark eyes + smile glyph |
| Palette economy | **Zero** hue families — fully achromatic (neutral white→grey background, near-black glyphs). No saturated accent anywhere. Radical restraint; economy is not the risk here, colourlessness is the committed bet. |

## Signature devices
- **Block-cursor eyes** `[GOLDEN-NUGGET]` — the two vertical rounded rects read simultaneously as a face's eyes and as text/code block cursors, tying the mascot directly to the "Markdown editor" subject. The strongest move in the icon.
- **Smiley-mascot brand** — a friendly emoji-like face as the whole identity; warmth carried entirely by arrangement, not by colour.
- **Ghost grid** — near-invisible notebook/table gridlines (nods to Markdown tables, shown prominently in the app cover) engineered to survive at hero size and gracefully disappear at Dock/menu-bar size.
- **Soft-plastic emboss** — puffy, omnidirectional soft-shadow halos give the glyph a clay/soft-toy tactility inside an otherwise flat white tile.
- **Achromatic commitment** — a color-free icon in a Dock full of saturated tiles; distinctive by absence.

## Failures
- **#10 Variant robustness (Liquid Glass) — FAIL:** the composition is a dark-glyph-on-white-tile that depends entirely on the light background. No Dark/Mono variants or glass layers are authored; a system dark/clear/tinted render would either leave a jarring pure-white tile or lose the dark face against a dark ground. The icon does not adapt across appearances.

## Soft passes (flagged for synthesis)
- **#1 Mask discipline (soft):** corner radius reads close to the system squircle, but the asset ships **pre-masked** (baked squircle + transparent corners) **with baked soft shadows** — the opposite of macOS 26's "deliver a square, unmasked layer and let the system apply mask + effects." Visually clean today; not Liquid-Glass-ready.
- **#5 Single light model (soft):** the glyph halos are omnidirectional soft glows rather than strictly directional top-down shadows — internally consistent, but the light *direction* is ambiguous rather than declared.

## Era note
Classified **Big Sur unified**, not Liquid Glass: soft top-down baked micro-shadows, uniform front-facing squircle, and — critically — *no* glass tells (no specular refraction, translucency, layer parallax, or authored appearance variants). The baked-shadow, pre-masked delivery is itself the evidence it predates / ignores the Tahoe layer model.

## Rhymes with
- (hint) Mascot / character-face icons and emoji-as-icon indie apps (warmth via arrangement).
- (hint) Achromatic, monochrome minimalist utility tiles (identity by colour-absence).
- (hint) Paper / notebook-grid document icons (the ghost grid).
- No other digested icons yet — this is a candidate seed for a "friendly-minimal mascot" icon cluster; needs ≥2 more members before any promotion.
