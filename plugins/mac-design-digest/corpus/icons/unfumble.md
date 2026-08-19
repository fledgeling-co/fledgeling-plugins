# Icon: Unfumble

- **Era:** Big Sur unified (flat-gradient squircle) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, SHA-1 `23c76c50`) · **App:** Unfumble — "automatic keyboard language switcher for Mac" (Utility, menu-bar) · **website:** unfumble.app
- **Resolution caveat:** delivered at **512×512**, not the 1024 master `(measured)`. Corners are transparent with a soft **baked system drop shadow** composited underneath — i.e. this is a web render (masked + shadowed), not a raw full-bleed layer. Glass/specular judgements are made on the masked render, but there is unambiguously no glass treatment to miss.

| Dimension | Reading |
|---|---|
| Background | **ramp #0C76FE → #4F5CF6** `(measured)` — diagonal two-stop, top-left brighter **azure** → bottom-right deeper **indigo**. Not just value-darkening: hue cools ~213°→~230° top→bottom (sky logic + hue drift). Center column runs #1871FC (top) → #4061F8 (bottom). |
| Glyph | **object** — a white wireframe **globe** (meridian + parallel grille, line-art, open not solid), #FFFFFF `(measured)`. Optical centre pushed slightly **low-left** (~240,260) to counterweight the sparkle mass upper-right — defensible optical compensation. |
| Overlay device | **badge** — a white four-point **sparkle** pinned to the globe's upper-right, with a small knockout halo where it crosses the grille. Reads "automatic / magic". |
| Light model | **Flat / non-dimensional.** Gradient field implies soft top-left sky light; glyph is flat white line-art — no cast shadow, no specular, no bevel, no refraction. One consistent (flat) model. Baked system shadow behind the mask is a render artifact, not authored depth. |
| Layer stack | back → front: (1) azure→indigo gradient field · (2) white wireframe globe · (3) white sparkle badge (knocks out the globe strokes beneath it) · [+ baked system drop shadow behind the squircle] |
| Palette economy | **One hue family** (blue→indigo) + white glyph. No third hue. **No reserved saturated accent** — the sparkle is white, identical to the glyph, so the "magic" cue is shape-only, not colour-differentiated. |

## Signature devices
- **Sparkle-on-globe** — a 4-point sparkle badge attached to a wireframe globe: globe = language/international, sparkle = automatic/effortless. It is the single identity move. `[GOLDEN-NUGGET, weak]` — nameable, but it is the two stock SF-Symbol primitives (`globe` + `sparkle`) composited, i.e. a template pairing rather than a committed, subject-mined drawing. The subject (keyboard language switching) is nowhere in the mark — no key, no glyph-pair, no cursor; it defaults to the generic "internationalisation = globe" reflex.
- **Hue-drifting ramp** — the field doesn't merely darken top→bottom, it cools azure→indigo along the diagonal. Slightly more considered than a single-hue value ramp.
- **Brand-colour coherence** — the icon's azure IS the brand accent: the cover (`cover.png`) sets the same icon and a white "Unfumble" wordmark on a dark charcoal keyboard-key field, with the tagline tinted in the icon's blue. Icon ↔ cover palette is coherent; the blue is load-bearing brand identity.

## Failures
- **#4 16px squint test — FAIL (borderline).** At 16px the wireframe grille collapses into an indistinct light blob; the meridian/parallel lines (thin strokes) do not survive, and identity degrades to "round white shape + faint star." The round silhouette persists, so "globe-ish" survives — but the *globe-ness* (the grid that makes it a globe) is lost. This matters acutely here: Unfumble is a **menu-bar utility** that lives at ~16–18px, exactly where this glyph is weakest. Fix: fewer, thicker meridians (2 lat / 2 long), or a solid-hemisphere globe, so the metaphor survives Dock/menu-bar duty.

## Soft passes (flagged, not scored as failures)
- **#2 grid** — glyph optically low-left; reads as intentional sparkle-counterweight, so passes, but it is a nudge worth noting.
- **#3 silhouette** — nameable as globe+sparkle, but the silhouette is carried by *interior strokes* (line-art), not a filled outline — which is precisely why #4 breaks.
- **#10 variant robustness** — the white glyph is background-independent and would survive dark/tinted renders, so it passes; but the icon ships **no authored Liquid-Glass / dark / tinted variant**, and its entire mood rests on the blue field.
- **#11 personality** — a device exists (sparkle badge), so pass; but it is template-default (stock-symbol pairing on a blue gradient), the single most common indie-utility icon formula.

## Rhymes with
- The large **"SF-Symbol glyph on a blue→indigo gradient squircle"** utility family — translation / VPN / network / menu-bar tools that reach for the `globe`. Style family: *blue-gradient-squircle utility template.* Nearest reference reflex: Apple Translate / Safari-adjacent globe motifs. First icon of this family in the corpus — a natural anchor for a future "stock-symbol utility" icon cluster once ≥2 more land.
