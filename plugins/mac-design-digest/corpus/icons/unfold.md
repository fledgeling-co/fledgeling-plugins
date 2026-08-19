# Icon: Unfold

- **Era:** Big Sur unified (front-facing embossed glyph on a top-lit gradient field) — see resolution caveat re: possible minimalist Liquid Glass · **Rubric:** 12/12 (10 clean + 2 soft, 0 failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 256×256 — a resized web render, not the 1024 master) · **App:** Unfold — "Quick Look Almost Anything on Your Mac" (Utility)

| Dimension | Reading |
|---|---|
| Background | Ramp `#29292D` (top) → `#09090B` (bottom) — near-black charcoal, top-lit vertical ramp, opaque matte field full-bleeding the squircle `(measured)` |
| Glyph | Object: a **spacebar keycap** rendered as a shallow ⊔ well. Light-gray body `#CFCFCF`–`#DEDEDE`, crisp `#FFFFFF` specular on the upper bevel edges. Optically dead-centre (bbox x44–211 → cx≈128; y107–150 → cy≈128), ~17% side margins `(measured)` |
| Overlay device | None — single glyph, no diagonal tool, no badge, no frame |
| Light model | Single top-down source: field lightens upward (sky logic), glyph carries `#FFFFFF` specular only on its top-facing bevels with a mid-gray face → reads as a keycap / engraved well catching one overhead light |
| Layer stack | back → front: (1) dark charcoal squircle field, top-lit vertical ramp; (2) embossed spacebar-keycap glyph, mid-gray body with ambient occlusion into the field; (3) `#FFFFFF` specular top-edge highlight on the glyph bevels |
| Palette economy | Fully **achromatic** — zero hue families, no saturated accent. Presence is built entirely from value + top-light, not colour |

## Signature devices
- **[GOLDEN-NUGGET] The glyph IS the trigger gesture.** Quick Look is invoked on macOS by pressing the **spacebar** — so the icon depicts the keystroke, not the file/preview/eye metaphor its category peers (looq's chrome spectrum, glance's block-cursor eyes) reach for. Subject-mining at its purest: the icon shows what your thumb does, not what the app renders.
- **Stealth monochrome** — a black key on a near-black field, separated only by a top-lit bevel. The icon deliberately spends its budget on restraint; it whispers in the Dock rather than shouting a hue.
- **Debossed key, not a free object** — the keycap is *engraved into* a filled squircle as a ⊔ well, the inverse of the photoreal free-object keycap family (klack, keeby) that drop the squircle entirely and sit on transparent. Unfold keeps the mask and carves into it.
- **`#FFFFFF` specular top-line as the sole material cue** — one crisp highlight edge does all the "this is physical" work on an otherwise matte, textureless field.

## Failures
- None outright. Two **soft passes**:
  - **#3 Silhouette / subject-naming (soft).** The ⊔ shape is a single, clean silhouette that holds as solid black — but it names its subject only to viewers who know the spacebar=Quick Look trick. In isolation it reads as a bracket / tray / staple, not "a preview utility." The cleverness (gesture-as-icon) is also the cost (cryptic to the uninitiated). The cover art compensates by floating the key over a cloud of file extensions — the icon alone does not.
  - **#10 Variant robustness / presence (soft).** Achromatic design is inherently tint- and dark-mode robust (nothing depends on a background hue). But a near-black icon risks **low presence on dark Docks/wallpapers** — the squircle edge can melt into a dark desktop, leaving only the light glyph. (Check is only partly applicable given the Big Sur classification.)

## Rubric detail
| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Mask discipline | pass | Art designed for the squircle; dark field full-bleeds to the system mask, no corner-radius fight. Faint edge-gradient *may* be a baked bevel (HIG discourages) — can't disambiguate art vs system-render at 256px |
| 2 | Grid adherence | pass | Glyph optically centred (cx≈128, cy≈128), safe-zone margins ~17% each side |
| 3 | Silhouette | **soft** | Clean single ⊔ shape, but subject nameable only with insider knowledge |
| 4 | 16px squint | pass | One bold, chunky, high-contrast shape; silhouette survives, only fine specular smears |
| 5 | Single light model | pass | Top-down throughout — field lightens upward, glyph specular on upper bevels only |
| 6 | Palette economy | pass | Monochrome; zero hue families; no accent — a committed achromatic choice |
| 7 | Figure-ground contrast | pass | Light-gray glyph on near-black ≈ 12:1+, survives grayscale (already achromatic) |
| 8 | Depth coherence | pass | Coherently embossed well; bevel highlights track the top light; no z-fighting |
| 9 | Era coherence | pass | All devices one language (embossed glyph + gradient field + top light) |
| 10 | Variant robustness | **soft** | Tint/dark-robust, but near-black field risks low Dock presence on dark desktops |
| 11 | Personality | pass | Strong nameable device (spacebar-as-trigger) + stealth-monochrome register |
| 12 | No-text | pass | No words, UI screenshots, or photographic elements |

## Rhymes with
- **klack** — its closest sibling: a subject-mined black keyboard keycap, warm-neutral-vs-neutral aside. But klack is a *photoreal free 3D object on transparent that refuses the squircle*; Unfold is the **flat, debossed, squircle-keeping minimalist inverse** of that same idea.
- **keeby** — keycap-as-whole-subject, but glossy-orange candy vs Unfold's stealth monochrome.
- **looq**, **glance** — Quick Look category peers, both **achromatic / colour-free**: looq is polished silver-on-black chrome, glance is soft-embossed light. Unfold shares their achromatic restraint but inverts to a dark matte field and picks a *gesture* subject rather than an eye/spectrum metaphor.
- **Style family:** achromatic utility icons + subject-mined keyboard hardware. Reference peers outside the corpus: the stealth-black developer-tool icon register (a dark monochrome key that trusts the viewer to lean in).
