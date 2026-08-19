# Icon: Tellie

- **Era:** Big Sur unified (framed-tile quotation) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 512×512 — a half-res web render of the 1024 master; sub-pixel detail on the caption tracks is therefore softened, read hex as ±3) · **Category:** Design
- **Subject fit:** Tellie is a Mac teleprompter/live-caption utility that "gives every Mac a notch" and lights up the exact word you're saying. The icon draws its own UI — a notch and a word-by-word transcript — so subject communication is unusually literal (confirmed against cover.png: same brand orange, same "current word highlighted, upcoming words dim" mechanic).

| Dimension | Reading |
|---|---|
| Background | Vertical ramp orange `#EE9550` (top) → `#DD7838` (bottom) (measured) — sky-logic, one hue. Enclosed by a raised light-silver bevel frame `#EFEFEF`→`#DEDEDE`→`#D0D0D0` (measured) |
| Glyph | Scene / UI-mimic: black notch pill (top-centre), one full-width white title bar, then 3 centre-aligned white caption pills of varying width. Optically centred on the vertical axis; motif is top-weighted (notch pinned to the field's top edge, as it would sit on a screen) |
| Overlay device | Frame (raised silver bezel ring) + badge-like black notch. No diagonal tool. |
| Light model | Top-down (Big Sur). Frame bevel highlights top / darkens bottom; orange ramp light-top→dark-bottom; white pills carry a short soft micro-shadow. One consistent source. |
| Layer stack | (1) baked drop shadow under tile → (2) silver bevel frame ring → (3) orange ramp field → (4) black notch pill → (5) beige "pending word" tracks `#E5C19C` → (6) white caption pills `#FFFFFF` → (7) white title bar |
| Palette economy | 1 hue family (orange) + neutral frame (gray/white) + beige tracks (desaturated orange, same family). No separate saturated accent — white pills are the focal element. Passes ≤2 families. |

## Signature devices
- **The notch as protagonist** `[GOLDEN-NUGGET]` — a black rounded pill pinned to the top edge of the orange field, literalizing the product premise ("gives every Mac a notch"). It is the one device that survives shrink and disambiguates the icon.
- **Live-caption transcript** — centre-aligned white pills of varying width flanked by quiet beige track lines; reads as words appearing / lighting up word-by-word (current word = bright white pill, upcoming = dim beige track). Directly mirrors the cover's "Word by [word]" highlight mechanic.
- **Raised silver bevel frame** — a beveled light ring enclosing the field; a framed-tile motif that is pre-Tahoe in feel (Big Sur fields are usually edge-to-edge, not ringed).
- **Baked squircle + drop shadow** — the artwork self-masks to a rounded square and bakes its own shadow into a ~10% transparent margin (older delivery convention), rather than shipping a full-bleed unmasked layer.

## Failures
- **#10 Variant robustness (Liquid Glass):** FAIL — single baked raster with a hardcoded orange field and baked shadow; not authored as separable Icon Composer layers, so it cannot yield clean dark / clear / tinted renders. macOS 26 will shadow the baked shadow and tint a fixed-orange tile. An era-appropriate limitation, but a real one: this icon lags the current kit (the exact "shipping apps trail Liquid Glass" delta noted in kit/macos-27.md).

## Soft passes (flagged for synthesis)
- **#1 Mask discipline:** reads correctly as a squircle with no corner-radius fighting, but bakes the drop shadow the system should apply — a Tahoe-era mismatch.
- **#3 Silhouette:** filled solid black the tile is just a rounded square; all identity lives in internal value/colour (notch contrast, orange field), not in outer shape. Nameable only as "a screen with captions," not instantly as one object.
- **#4 16px squint:** brand gestalt survives (orange field + dark top notch), but the transcript detail — three caption rows plus thin beige tracks — smears to mush; the app's actual subject (live captions) is unreadable at menu-bar size.
- **#7 Figure-ground:** white pills and black notch clear 3:1 easily, but the beige tracks `#E5C19C` on orange `#E5813F` are near-isoluminant and wash out in grayscale — intentional "quiet/pending" read, but sub-floor for those elements.
- **#9 Era coherence:** predominantly Big Sur (squircle, vertical gradient, front-facing, top-down light, baked micro-shadows), but the raised bevel frame + baked tile shadow read as a flat-transition / framed-tile quotation. Single consistent quotation, so coherent — just not current-era.

## Passed clean
- #2 grid (optically centred), #5 single light model, #6 palette economy, #8 depth coherence (frame > field > pills ordered sensibly), #11 personality (the notch is a genuine nameable device), #12 no-text (pills are abstract word-shapes, no real glyphs/photo).

## Rhymes with
- **UI-mimic utility icons** — icons whose glyph is a miniature of the app's own interface (dictation/transcription/menu-bar tools). Style-family guess, not yet corpus-backed (single icon).
- Big-Sur framed-tile icons (light bevel ring around a saturated field) and warm-orange productivity icons. Needs ≥2 more warm-orange or UI-mimic icons before any of this promotes.

## Notes for synthesis
- Resolution caveat: 512px web render, not the 1024 master — treat all hex as ±3 and the beige-track edges as softened by downscale.
- Strongest single lesson: **subject-mining done right** — the icon draws the product's defining behaviour (notch + word-by-word) instead of a generic glyph-on-gradient, which is exactly the "committed direction vs template-default" distinction. The cost is that this literalism is detail-dense and doesn't survive the 16px/silhouette tests as cleanly as a single-object glyph would.
- Candidate cross-icon pattern to watch: "the app's own UI as the icon glyph" and "current-vs-pending state shown as bright-fill-vs-dim-track."
