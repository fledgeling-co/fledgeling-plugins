# Icon: Creavit Studio

- **Era:** Big Sur unified squircle — but a *flat* rendition (no baked lighting/shadow, no glass) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 512×512, SHA-1 `fb413657`) · **Category:** Video · **App does:** "Turn boring screen recordings into beautiful videos"

| Dimension | Reading |
|---|---|
| Background | Flat gold field `#F2BF00` (measured) — no ramp; the brighter `#FCC700` at the mask edge is anti-alias, not sky-logic gradient |
| Glyph | Abstract. Large charcoal `#2B2B2B` rounded-rect card, centred, ~x96–425 · y58–452 at 512 (≈64% of canvas width). Optically centred, symmetric. Twin charcoal capsule rails in the side margins (~184px tall, vertically centred). |
| Overlay device | Frontmost white `#FFFFFF` vertical bar (~21px wide at 512) bisecting the card, running full-height y37–473 — pokes past the card top and bottom into the gold field |
| Light model | Flat / none. No cast shadow, no baked micro-shadow, no specular highlight. Two-tone graphic; system supplies the drop shadow externally. |
| Layer stack | back → front: (1) gold squircle field · (2) twin charcoal side capsule rails · (3) charcoal card · (4) white bisecting divider |
| Palette economy | 1 hue family (gold) + charcoal neutral + white. No saturated accent reserved for a focal detail — the focal element is a neutral. Contrast charcoal-on-gold is high and survives grayscale. |

## Signature devices
- **The bisecting seam** — a single white vertical bar splitting the dark panel and running past its ends into the field. This is the whole personality; it turns a plain dark card into a "framed screen split down the middle."
- **Twin side rails** — two charcoal capsules floating in the gold margins, reading as grips/handles or the side buttons of a device. Committed, symmetric, nameable device (not template glyph-on-gradient).
- **Monochrome-on-saturated-field** — charcoal + white mark on a single bright brand hue; identity carried by shape and one saturated field, not by depth or lighting.

## Failures
- **#3 Silhouette / subject communication (FAIL):** filled solid black the icon is a rounded rectangle with a thin gap and two side tabs — not instantly nameable, and it does not communicate "video." For a Video-category app that is the load-bearing miss: the mark reads as an abstract framed panel, could be a book / split-view / device face, but says nothing about screen recording. Committed and distinctive, but cryptic.

## Soft passes (flagged for synthesis)
- **#4 16px squint:** the dark card survives as "dark rounded square on gold," but the divider and side rails — the entire distinguishing identity — smear away at Dock/Spotlight size, collapsing the icon to a generic charcoal-on-gold blob. Pass on legibility, fail on identity-retention.
- **#5 Single light model / #8 Depth coherence:** internally consistent because it is entirely flat — no z-fighting, but also no modeled light or depth. Its strict Big Sur squircle format implies top-down baked lighting the artwork never delivers.
- **#10 Variant robustness:** not authored as Icon Composer glass layers, so it forfeits the Liquid Glass dynamic treatment — but being shape-driven two-tone, the composition *would* survive dark/tinted renders trivially.

## Passes (evidence)
- #1 Mask discipline: full-bleed gold, squircle pre-masked cleanly (transparent corners); side rails sit inside the safe zone. #2 Grid: card optically centred and symmetric (divider ~4px right of true centre at 512 — negligible). #6 Palette economy: ≤2 hue families. #7 Figure-ground: charcoal-on-gold, high contrast, grayscale-robust. #9 Era coherence: one consistent flat-squircle language. #11 Personality: yes — bisecting seam + side rails. #12 No-text: clean, no words/photo/UI screenshot.

## Notes / caveats
- **Resolution:** 512×512, half the 1024 master — a resized web export. Fine specular/shadow can't be distinguished from resize flattening, but there is unambiguously no glass and no baked depth: this is a flat two-tone design, not a downsampled Liquid Glass icon.
- **Palette coherence with app marketing:** the cover hero shows a blurred 3D render of this same icon with an **electric-blue** inner panel (≈ cobalt) where the shipped `icon.png` uses charcoal. Brand intent appears to be **gold + blue**; the shipped icon is gold + charcoal + white only. Accent-blue lives in the cover, absent from the icon — partial coherence.
- The white seam extends beyond the card into the field (y37–473 vs card y58–452), reading as a stand/seam rather than an inset stripe.

## Rhymes with
- Flat "monochrome abstract mark on one saturated brand field" utility icons (charcoal/white glyph on a single bright hue), **not** the diagonal-tool Big Sur family and **not** the Liquid Glass specular family. Style-family guess: indie-utility flat-squircle. (Left as a hint for synthesis — needs ≥2 more members before any cluster.)
