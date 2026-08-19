# Icon: Runey

- **Era:** skeuomorphic-quote (legacy glossy) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply · **Category:** Business (time tracking / invoicing / proposals)
- **Asset fidelity:** genuine 1024×1024 PNG, clean alpha, crisp bevels — *not* a resized web render (measured). Provenance of hex values: (measured) from pixel samples.

| Dimension | Reading |
|---|---|
| Background | Vertical black ramp `#313131 → #000000` with a baked glossy specular band (upper third, peaks ~`#3E3E3E`/`#333333` top-centre). Reads as a faux-glass "gloss dome", but pre-rendered — not Icon Composer glass. |
| Glyph | Monogram — a stylised **"R"**. Beveled chrome: white top face `#FFFFFF`, silver body `#EEEEEE`/`#BDBDBD`, dark under-bevel `#191919`. Optically centred, runs large (margins ~11%; descender leg swings near the mask edge). |
| Overlay device | None (no diagonal tool, no badge). The gloss sheen is a surface treatment, not an overlay. |
| Light model | Top-down. Bevel lit from top (white top edge → dark under-edge); glossy sheen concentrated upper-third; a short, soft **baked** cast shadow sits beneath the glyph legs. Specular present but pre-baked, not system-applied. |
| Layer stack | (back→front) pre-masked squircle envelope w/ baked top rim highlight → black vertical gradient field → baked glossy sheen → beveled chrome "R" → baked soft drop-shadow under glyph. |
| Palette economy | One family: neutral grayscale only. Black field + silver/chrome glyph, no accent. Maximal figure-ground; economical to the point of dropping the brand colour entirely. |

## Signature devices
- **The running-R** `[GOLDEN-NUGGET]` — the bowl doesn't fully close and the leg curves out like a stride; a subject-echo of the name *Runey* (run). This is the one genuinely committed, ownable choice; the same letterform reappears as the in-app sidebar logo, so the mark is consistent across surfaces.
- **Baked gloss dome** — a pre-rendered specular sheen across the upper third; the iOS-6-era glossy signature.
- **Beveled chrome letterform** — 3D metallic bevel (white top face, dark under-edge), the skeuomorphic material tell.
- **Pre-masked squircle envelope** (defect-device) — artwork delivered inside its own rounded-rect with transparent corners (alpha 0) and a baked edge rim, rather than a full-bleed square for the system to mask.

## Failures
- **#1 Mask discipline — FAIL.** Art is pre-masked into its own rounded-rect (corners sampled at alpha 0) with a baked top rim highlight. Against the macOS 26 system squircle this double-rounds / clips the baked rim; HIG asks for square, unmasked layers. This is the load-bearing miss for a macOS-native context.
- **#10 Variant robustness — FAIL.** A flat pre-rendered PNG with baked gloss, bevel and drop-shadow on a solid black field. It cannot be recomposed into dark/clear/tinted glass variants; in tinted mode the black field + chrome won't adapt and the baked specular would double with the system's.

### Soft passes (counted as passes, flagged for synthesis)
- **#2 Grid** — optically centred but runs large; descender leg sits near the mask edge, margins only ~11%.
- **#4 16px squint** — the letterform survives and stays nameable as "R", but the chrome bevel/gloss smears to a flat gray blob; all material nuance is wasted below ~64px.
- **#5 Single light model** — bevel and gloss share a top source, but the extra baked cast shadow adds a second implied depth cue.
- **#8 Depth coherence** — planes order sensibly and don't z-fight, but the coherence is bought with baked bevel/shadow the platform forbids.
- **#11 Personality** — one ownable device (the running-R); undercut by an otherwise generic glossy-black + chrome-initial template.

### Clean passes
- #3 Silhouette (nameable "R" filled solid), #6 Palette economy (single grayscale family), #7 Figure-ground (silver-on-black, far exceeds 3:1, already grayscale), #9 Era coherence (all devices belong to one legacy glossy language — internally consistent, just the wrong era for macOS 26), #12 No-text (a single logotype glyph, no words/UI/photo — the riskier monogram end, but not a words defect).

## Brand-coherence note
The brand's signature is **black + lime/chartreuse green** (the cover is a green glass swirl; the in-app sidebar renders this *exact* R letterform in green). The icon is **black + chrome silver with zero green** — so it under-communicates both the brand palette and the subject (invoicing / time-tracking). The letterform carries brand continuity across surfaces; the colour does not.

## Rhymes with
- Legacy iOS-6-era glossy monogram icons and "app-icon-generator" chrome-letter-on-black outputs — the beveled-metal initial-on-black logotype family (old utility/finance apps that leaned on a chrome initial).
- Style family guess: **glossy-skeuomorphic monogram** (baked gloss + bevel + pre-mask). Distinct from the Big Sur "squircle + diagonal tool" family and from Liquid Glass layered-glass icons — this is a pre-flat holdout.
