# Icon: dropadoo

- **Era:** Big Sur unified (pre-Tahoe; **not** Liquid Glass) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, SHA-1 77cbc663) · **Category:** Productivity ("send files via drop")
- **Resolution caveat:** delivered at **225×225px, 72dpi** — a downscaled web render, not the 1024 master. Fine-detail contrast reads honestly at this size, but sub-pixel edge treatments (any true bevel, the exact drop-shadow recipe) are not recoverable. Hero-size reasoning below is upscaled inference `(estimated)`; the small-size failures are only *worse* at the true master, never better.

| Dimension | Reading |
|---|---|
| Background | flat **#545454** charcoal field, full-bleed to the mask (uniform — no ramp; measured, `(measured)`) |
| Glyph | **scene / still-life**: off-white card **#E7E7E8** emerging from the envelope top, two abstracted text marks in **#000000**, envelope flap/pocket in the same #545454. Optical weight sits upper-centre (card) with a bottom-right pull (paperclip). |
| Overlay device | **diagonal tool** — a sage-green paperclip (**#BDD894**) laid at ~45° across the fold, lower-right quadrant (green bbox x125–189 / y95–176 of 225 → corner-weighted, not optical centre) |
| Light model | soft top-down, **matte/diffuse, zero specular**; one short baked micro-shadow tucking the card behind the flap; envelope rendered as a single flat tone (planar, not modelled) |
| Layer stack | back → front: (1) charcoal envelope back/field #545454 · (2) off-white letter/card #E7E7E8 + black text marks · (3) envelope front flap triangle (same #545454, edges drawn as thin ~1px #000000 outlines) overlapping the card base · (4) sage-green paperclip #BDD894, frontmost |
| Palette economy | 1 accent hue (sage green) on a neutral charcoal/off-white ground — textbook economy; accent reserved for the single focal element (the attachment). White #FFFFFF around the squircle is the render backdrop, not the icon. |

## Signature devices
- **Envelope-as-canvas.** The whole squircle *is* an envelope field rather than a centred glyph-on-gradient — the subject (email delivery) becomes the background plane. `[GOLDEN-NUGGET]`
- **Letter emerging from the top.** A rounded off-white card pushes out of the envelope mouth, carrying two abstracted text lines — the "message" reading without a single real character.
- **Paperclip across the fold.** The sage-green clip laid diagonally over the lower-right fold is a direct Big Sur "tool-at-an-angle" quotation (cf. Preview's magnifier, TextEdit's pen) — and doubles as the literal "attachment" metaphor for a file-sender. The one place the boldness budget is spent.
- **Single desaturated accent.** #BDD894 is a muted pistachio, not a saturated lime — the accent whispers rather than shouts, and it's the only chromatic element in the icon. It ties cleanly to the cover art's green (NEW-version badges, the drag arrow) — icon↔brand palette coherence confirmed.

## Failures
- **#4 · 16px squint test — FAIL (hard four).** The envelope is a flat #545454 field whose flap geometry is drawn in thin ~1px #000000 outlines (measured: the entire fold band is uniform 84,84,84 with ~10 black edge pixels). At Dock/Spotlight/menu-bar size those hairline folds, the two text marks, and the paperclip's interior loops all smear — the icon collapses to "dark squircle + white patch at top + green speck." It is engineered for the hero card and breaks at the size the system actually renders it most.
- **#10 · Variant robustness — FAIL.** A near-solid charcoal mass that assumes a *light* Dock/backdrop for its silhouette to pop. This is a Big Sur-era single-render icon with no Default/Dark/Tinted layer authoring; on a dark backdrop the envelope reads dark-on-dark and only the green paperclip survives a tint pass. (Era-scoped check — expected of a pre-Tahoe icon, but recorded honestly: the composition depends on one background context.)

### Soft passes (scored pass, flagged for synthesis)
- **#2 · Grid adherence** — the scene fills the canvas well, but the *focal* element (paperclip) is pushed into the lower-right corner rather than sitting on an optical grid circle, leaving a mild bottom-right weight bias.
- **#7 · Figure-ground contrast** — the card↔envelope edge is strong (#E7E7E8 on #545454, well over 3:1), and the paperclip #BDD894-on-#545454 clears the floor, **but** the envelope's own flap geometry is ~1:1 (charcoal-on-charcoal). Only the focal shapes hold; the structural drawing does not.
- **#1 · Mask discipline** — clean squircle-native art; the surrounding soft shadow on white is a render/capture artifact of this source, not a baked-in glow. No corner-radius fight.
- **#3 · Silhouette** — filled solid, it reads as a dark square with a card notch and a clip; the paperclip is the nameable anchor. Passes, but leans on the white card because the envelope is tonally invisible.

## Rhymes with (style-family hint only — not a canon claim)
- **Envelope/mail-field icons** (messaging & delivery utilities that make an envelope the whole ground rather than a centred glyph) — a possible mail-adjacent cluster with other digested mail apps.
- **Big Sur "diagonal-tool-over-a-field"** family (Preview, TextEdit lineage) — the paperclip-at-an-angle is the tell.
- **"Single desaturated accent on charcoal" indie-utility** look — quiet, matte, one muted hue doing all the chromatic work.

## Personality (committed direction, per aesthetic-direction vocabulary)
Three cashed-out adjectives:
- **matte** — no specular, no gloss, no glass; flat planar shading throughout (a *committed* choice, not a template default — it deliberately declines the Liquid Glass era it ships into).
- **muted** — the accent is #BDD894 pistachio, not a system-saturated green; the icon's entire chroma budget is one low-saturation hue.
- **literal** — meaning is delivered by stacking real-world objects (envelope + letter + paperclip) rather than an abstract mark; maximum subject-legibility at hero size, at the documented cost of small-size survival.

Notes for synthesis: the standout learning here is the **hero-vs-Dock split** — an icon can be genuinely well-composed at 512px and still fail the non-negotiable #4 because its structural geometry (the envelope folds) is drawn below a contrast floor. Candidate icon-canon probe once ≥3 icons evidence it: *dark-on-dark structural linework needs a ≥3:1 floor or it evaporates at Dock size.* Resolution is a downscaled 225px web render — treat all hero-size claims as `(estimated)`.
