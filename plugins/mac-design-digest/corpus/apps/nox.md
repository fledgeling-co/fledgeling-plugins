# Nox — profile

- **Source:** macapp.supply (getnoxapp.com) · **Surfaces digested:** marketing website hero (`cover.png`) only · **Last updated:** 2026-07-19
- **One-sentence identity:** A migraine/light-sensitivity display-filter utility whose *marketing* wears an editorial-luxury coat — cream high-contrast serif display + brass accent on warm near-black, the register of a premium wellness brand rather than a system utility.
- **Cluster:** unassigned (brand/web evidence only — no native surface to cluster)
- **Lineage:** unknown (low) — **no macOS app UI was supplied.** The one image is a *web* marketing hero; its web-derived properties never feed macOS canon.
- **Era (chrome):** unknown — no app window, toolbar, sidebar, menu-bar extra, or traffic lights present to classify.

> **Corpus honesty note.** Of the two source files, `cover.png` is a 100%-marketing website hero (headline, sub-copy, two CTAs, disclaimer — no product window inside the composite) and `icon.png` is the app icon. My task is Workflow A (UI screenshot) only, so the icon is **not** digested here (that is Workflow B). The result: this profile carries **brand/aesthetic evidence but zero product-UI evidence.** To actually learn Nox's interface, the corpus needs a screenshot of its real surface — almost certainly a **menu-bar-extra popover** (preset picker + intensity slider) for a filter utility, plus any Settings window.

## Tokens

All values below are **web/brand** tokens measured from the marketing PNG (2648×1318, ~2× capture). They describe the *landing page*, not the app. `platform: web` — excluded from macOS canon.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/hero | `#131110` warm near-black (R>G>B) | (measured)(inferred) | Not pure black — warmed toward espresso; subtle radial lift toward centre-top |
| ink/headline | `#DCD6CB` warm cream/bone | (measured)(inferred) | Display serif fill; the "paper" note against the dark ground |
| accent/gold | `~#B49A5E` brass / old-gold (fill ramps `#8A7234`→`#C6A86C`) | (measured)(inferred) | The single brand colour: italic word "macOS", primary CTA, pill dot, "Buy license" link |
| ink/body | `#9F968C` warm mid-gray | (measured)(inferred) | Sub-copy; ~6:1 on bg — legitimate de-emphasis, still legible |
| ink/disclaimer | `#706962` dim warm gray | (measured)(inferred) | Fine print ~3.3:1 on bg — **below 4.5:1**, see Defects |
| surface/pill | `#201D1A` lifted warm charcoal, capsule | (estimated)(inferred) | Eyebrow badge fill, hairline warm border |
| type/display | High-contrast transitional/modern **serif**, true italic; ~80–90px CSS est., line-height ~1.05–1.1 | (estimated)(inferred) | Fraunces / Canela / Recoleta-class — editorial-luxury display; ball-ish terminals, genuine cursive italic |
| type/body | Humanist **sans** (neo-grotesque), ~18–19px CSS est., line-height ~1.5 | (estimated)(inferred) | Body, pill, buttons, disclaimer — one sans does all UI text |
| type/scale | ~5 sizes: display ~85 · body ~18 · pill/button ~15–16 · disclaimer ~14 | (estimated)(inferred) | Roughly geometric, disciplined |
| button/primary | Brass filled, ~56–64px tall, small radius (~6–8px), semibold dark-ink label | (estimated)(inferred) | "Download Free Trial" |
| button/secondary | Ghost/outlined, warm hairline border `~#9E968B`, same height | (estimated)(inferred) | "How it works" — one filled, one outlined: correct action hierarchy |

## Layout skeletons

**`cover.png` — web marketing hero (dark, centred single column):**
- Vertically stacked, horizontally centre-aligned on one axis, generous max-width on the text block.
- Top→bottom: capsule eyebrow badge (gold dot + "Research-backed spectral filtering for macOS") → two-line serif display headline ("Migraine screen filter for *macOS*", last word italic + gold) → 4-line muted-gray sub-copy wrapped at ~45–55 chars → CTA row (filled brass primary + outlined secondary, side by side) → single dim disclaimer line ("14 days free · No credit card · macOS 14+ · *Already tried it? Buy license*").
- Proximity is correct: within-block gaps < between-section gaps; the CTA sits in its own breathing room. This is a competent, conventional SaaS/utility hero — **web vocabulary, not app vocabulary.**

## Signature moves
- **The one italic gold word.** The entire brand flourish is a single decision: setting the last word of the headline ("*macOS*") in the serif's true italic *and* in the brass accent, while everything else stays upright cream. One Von-Restorff moment; the rest of the type stays quiet. This is the whole personality in one glyph-run.
- **Subject-derived warmth.** The amber/brass-on-warm-black palette isn't a reflex — it *is* the product: therapeutic tint glasses are amber, "Nox" means night, and low-blue-light comfort is the therapeutic promise. The palette mines the subject (per aesthetic-direction doctrine), which redeems what would otherwise be a template look.

## Defects
- **Default-model warm-editorial aesthetic** → cream serif display + gold/amber accent on warm near-black is the *current* AI-reflex look flagged in `frontend-aesthetic-direction.md` (§ warm-editorial default). Partially redeemed by subject-mining (see Signature), but the direction still lands squarely on the most-reached-for family — a stronger brief would rotate the accent (e.g. narrow-band clinical green, which the product literally sells) instead of the safe brass. *Not an anti-pattern; a genericness note.*
- **Contrast Dilution (fine print)** → disclaimer `#706962` on `#131110` ≈ **3.3:1**, under the 4.5:1 floor for ~14px text. Fix: lift to ≥`#8A837A` (~4.6:1) or bump size/weight.
- **No product-UI evidence** → the cover shows zero app interface. Corpus gap, recorded, not a design flaw of the app itself.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| cover.png — web marketing hero (dark) | 11/14 (2 N/A) | #9 fine-print contrast (~3.3:1). N/A: #12 input height, #13 label proximity (no forms); #14 focus not observable in static |
| — native-tells audit | 0/10 applicable | #1 not native — web marketing surface; #2–#10 N/A (no native chrome, glass, sidebar, toolbar) |
