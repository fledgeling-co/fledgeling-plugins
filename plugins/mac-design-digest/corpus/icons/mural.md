# Icon: Mural

- **Era:** custom (flat editorial monogram — deliberately abstains from Big Sur / Liquid Glass material conventions) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (pre-masked web render — see Provenance) · **Category:** Utility (dynamic-wallpaper / creative-desktop canvas)

| Dimension | Reading |
|---|---|
| Background | flat `#FFFFFF` — no ramp, no field gradient, no material (all interior samples 255,255,255,255) |
| Glyph | monogram — a single high-contrast **Didone/Modern italic capital "M"**, pure `#000000`; bbox 636×464px, optical centre (510,510) vs canvas (512,512) — dead-centred; fills ~78% of the plate width |
| Overlay device | none |
| Light model | none — flat 2-value mark; the only shading present is the render frame's baked squircle drop shadow (delivery artefact, not artwork) |
| Layer stack | back → front: [flat white background plate] → [black serif "M" glyph]. Two planes, no material, no tool overlay |
| Palette economy | 2 values, 0 hue families (achromatic): `#000000` glyph on `#FFFFFF` ground. Maximally economical; accent: none |

## Signature devices
- **Engraved museum-monogram serif** — a high-contrast Didone/Modern italic capital M (hairline-to-thick stroke contrast, bracketed serifs, a calligraphic swash-curl on the top-left leg). This is a *committed* editorial type choice, not a template Helvetica initial — the entire personality of the icon lives in this one letterform. `[GOLDEN-NUGGET]`
- **Maximal-contrast achromatic field** — pure `#000` on `#FFF` (21:1). Zero colour, zero gradient, zero material. A deliberate reductive statement in a glass era.
- **Confident scale** — glyph fills ~78% of the visible plate width; a big, centred mark that behaves like a gallery placard / letterpress initial rather than a shy corner glyph.

## Failures
- **#10 Variant robustness (FAIL):** black glyph on a white plate is entirely background-dependent — invert the field (dark / tinted / clear appearance) and the black M vanishes or the plate reads as a hard white square. No dark/tinted variant is authored; the construction (black-on-white) is exactly the fragile case Liquid Glass authoring (Icon Composer default/dark/mono) exists to solve.
- **#4 16px squint (SOFT PASS):** the M reads as an M at menu-bar size, but the Didone hairlines and the swash finesse are precisely what thin/smear at 16px — identifiable but the refinement collapses to a generic serif M.
- **#12 No-text (SOFT PASS):** the icon *is* a single letterform. It clears the check because a single-letter monogram with strong shape logic is the sanctioned exception (not a word / UI-shot / photo), but the whole icon riding on one glyph is the borderline of that rule.

## Notes (provenance & subject)
- **Delivered asset is a pre-masked render, not the raw master.** 1024×1024 PNG, but the artwork is inset to an **820×820 squircle (~80% of canvas)** with transparent corners (alpha 0) and a baked soft drop shadow (~45.7k semi-transparent px). The squircle mask + shadow are composited into the PNG — macapp.supply's Dock-render treatment — so mask-discipline (#1) and true-margin readings are of the render, not the submission. The underlying master is presumably a flat white full-bleed field with a centred black M, which would mask cleanly. Pure `#000`/`#FFF`, no colour lost to compression; glyph edges clean.
- **Subject-communication gap:** the monogram signals a brand *initial*, not the app's *function* (turning the Mac desktop into a live/dynamic art canvas). Passes the silhouette test as a nameable shape (an M), but tells you nothing about what the app does.
- **Split brand type-voice:** the cover wordmark is a loose **white brush-script** "Mural" over a Sistine-Chapel "Creation of Adam" composite — a casual, painterly register. The icon's formal Didone serif is a *different* type voice. Both gesture at "art / mural / museum," but the letterforms disagree; the icon is the refined-gallery reading, the wordmark the painterly one.

## Rhymes with
- Editorial / luxury single-glyph monograms: fashion-house serif initials, Bodoni/Didot letterpress marks, museum wordmark placards. Style family = **minimalist-monogram / editorial-serif on flat field** — a hint for synthesis; promote only if ≥2 more icons evidence it.
