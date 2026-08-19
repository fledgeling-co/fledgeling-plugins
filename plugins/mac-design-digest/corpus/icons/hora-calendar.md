# Icon: hora Calendar

- **Era:** Big Sur unified (flat squircle language) carrying a light **calendar-page skeuomorphic quote** · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/hora-calendar/icon.png`, SHA-1 `ecd4d191`) · **Category:** Productivity
- **Subject:** a fast, keyboard-driven native Mac calendar ("The Mac Calendar Google never built"). An icon should communicate its subject — here the calendar is carried by the *background* (red header + ruled agenda lines + a date numeral), while the *foreground* is a brand monogram.
- **Resolution caveat:** input is a **512×512 pre-masked RGBA render** (squircle corners already transparent), **not** the 1024 full-bleed unmasked master. So full-bleed mask authoring can't be verified, the corner radius is baked by the exporter, and fine gradients are compression-flattened. Hex values are `(measured)` from this 512 render; sub-pixel reads are `(estimated)`.

| Dimension | Reading |
|---|---|
| Background | Two-zone: coral header band ramp `#F55552`→`#F96D6B` (top ~22%, flat-ish coral) over a near-white paper field `#F1F2F3`→`#FFFFFF`, with a faint warm coral bleed `#FFEAE9` rising at the bottom edge `(measured)` |
| Glyph | Hand-drawn **brush-script lowercase "h" monogram**, pure `#000000`, occupying ~70% of the canvas; ascender loop reaches into the coral band, tail drops toward the bottom edge, mass weighted low and slightly right — a signature-scale letterform, not optically centered `(measured)` |
| Secondary marks | 3–4 horizontal light-grey **agenda ruled lines** `#BFBEC1`; a small grey **date numeral "18"** `#707070` top-right (Apple Calendar's date-on-icon convention) `(measured)` |
| Overlay device | None in the Big-Sur "diagonal tool" sense; instead a **calendar-page quote** (header band + ruled lines + date) sits *behind* the monogram |
| Light model | Near-flat, front-lit. Only two lighting events: a **soft short drop-shadow** lifting the black script off the paper (anti-alias halo reads `#E5DEDF`), and a **coral ground-glow** halo behind the monogram's base. No specular, no refraction — not a glass model. `(estimated)` |
| Layer stack | (back→front) squircle base (coral band + paper) → grey ruled lines → date numeral "18" → coral ground-glow → black brush-script "h" + soft drop-shadow |
| Palette economy | Two hue families — coral-red accent + neutral (paper/black/grey). Accent (coral) reserved for header + glow; ink-black reserved for the focal monogram. Economical. |

## Signature devices
- **[GOLDEN-NUGGET] Signature-scale brush-script monogram** — the cursive `h` is hand-inked (variable stroke weight, brush terminals) and blown up to fill the frame like a penned signature, deliberately breaking across the header band, the ruled lines and the paper. This is the whole personality in one decision; it's the committed direction vs. the template-default "small glyph on a gradient."
- **Calendar-page quote** — coral header strip + light-grey agenda ruling + grey date numeral "18". A semiotic (not material) skeuomorphic quote of Apple Calendar / a ruled agenda page. Communicates "calendar" without any texture realism.
- **Coral ground-glow** — a soft warm halo rising from the bottom-center behind the monogram; decorative brand-warmth rather than a physically-motivated light.
- **Ink drop-shadow** — short, soft, low-offset shadow lifting the `#000` script off the paper — the icon's only real depth cue.
- **Brand coherence (confirmed via cover):** the same coral-red family and the same script-`h`-in-a-rounded-badge reappear as the wordmark lockup on the marketing cover — the icon's coral + script-h is the brand system, not an arbitrary mark. Icon↔brand palette coherence is strong.

## Failures
- **#10 Variant robustness (Liquid Glass era) — FAIL.** The icon is authored in Big-Sur flat language, not as Icon Composer glass layers. The composition is colour-dependent (ink-black monogram on white paper + a red band); it would not produce clean dark / clear / tinted / mono renders — the black monogram has nothing to invert to and the calendar semantics don't survive a mono tint. This is an **era mismatch** with macOS 26 (Liquid Glass), not a botched glass icon — but in the current era it means the icon won't participate in the system's tinted/mono variant set.

### Soft passes (scored pass, flagged for synthesis)
- **#2 Grid adherence (soft).** The monogram overspills the safe zone — tail nearly meets the bottom edge, ascender enters the coral band, mass leans low-right. Legitimate as a signature-scale device, but it is *not* optically centered and crowds the margins; a stricter reading would fail it.
- **#4 16px squint (soft).** The high-contrast black monogram survives at Dock/Spotlight size (it's the load-bearing element), but the ruled lines, the "18" and the coral glow all smear away — at 16px the icon reads as "red-topped card with a black squiggle," and the *calendar* meaning is lost. The brand survives; the subject does not.
- **#8 Depth coherence (soft).** Clean layer order, but the coral ground-glow behind an ink-black letter is unmotivated by the flat light model — decorative halo, not physics.
- **#12 No-text (soft).** Contains a numeral ("18") and a letterform (the `h`). Both are defensible — the date numeral follows Apple Calendar's own icon convention, and a single-letter monogram is the sanctioned typographic exception — but strictly the icon is not free of text/letters.

## Rhymes with
- **Hand-lettered / monogram-on-stationery brand icons** — the oversized brush-script mark is the family signature (rhymes with wordmark-derived indie icons whose glyph *is* the brand letter).
- **The ruled-paper + date-number calendar/notes family** — Apple Calendar's date-on-icon, Fantastical's date block, Apple Notes' ruled paper. hora quotes these signifiers flatly rather than rendering them skeuomorphically.
- **Style-family guess:** "brush-script monogram over a flattened calendar-page quote" — an indie-warm, high-contrast, ink-forward register. First icon in the corpus; no confirmed cluster yet.
