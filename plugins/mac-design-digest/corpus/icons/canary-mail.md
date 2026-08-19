# Icon: Canary Mail

- **Era:** custom (Big-Sur white-squircle structure wearing web-2.0 aqua-gel gloss) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, 204×204 web render — see resolution caveat) · **Category:** Productivity (email client)
- **One-line:** the Canary logomark rendered as a glossy blue gel glyph on a near-white tile — brand-forward, era-mixed, and silent about "email."

| Dimension | Reading |
|---|---|
| Background | ramp #FFFFFF (top) → #ECECEC (bottom) (measured) — near-flat white with a faint top-lit vertical fade; "sky logic" but barely present |
| Glyph | abstract brand logomark: a crescent "C" (bird body / Canary monogram) opening right, with two triangular send-darts (wings / paper-plane feathers) fanning off its mouth. Monochrome blue gel. Sits optically centred, mass a touch low-and-right of geometric centre, generous safe-zone margins |
| Overlay device | none (the darts are part of the glyph, not a crossing tool) |
| Light model | baked glossy gel: top-lit specular sweep + internal light-top→dark-bottom gradient per shape, plus a soft baked drop shadow of the glyph on the white ground. Not Big Sur's matte top-down light; not system Liquid Glass — the gloss is painted into the art |
| Layer stack | white squircle ground (#FFF→#ECECEC) → baked glyph drop-shadow → blue gel crescent (C/body) → two blue gel send-darts (front-right) → baked per-shape speculars |
| Palette economy | one hue family (blue). Glyph ramp specular #D0F7FF → light #68D6F8 → mid #3BAAF6 → deep #2166EC (measured). No separate accent — the whole glyph is the accent |

## Signature devices
- **Crescent-C-plus-twin-darts logomark** — a single distinctive mark that reads as bird-in-flight / send-motion / Canary monogram all at once; the crescent is the clear anchor, the darts the movement. [GOLDEN-NUGGET] the icon *is* the wordmark's mark, recoloured — strong brand-to-icon coherence (the cover's black wordmark uses the identical mark).
- **Aqua-gel gloss** — baked specular highlights + internal blue gradient give each shape wet-glass volume. A deliberate web-2.0/aqua quotation, applied consistently across every shape.
- **Monochrome-blue-on-white tile** — palette economy at its cleanest: one hue, white ground, no second colour.
- **Palette coherence with the app** — icon blue (#2166EC–#68D6F8) sits in the same cyan/sky family as the cover's brand field (~#7FD4FF), so icon and product read as one brand.

## Failures
- **#9 Era coherence** — mixes two era languages: a Big-Sur-style white squircle base carrying an aqua/web-2.0 gel gloss glyph whose light model belongs to neither the Big Sur (matte, soft top-down) nor Liquid Glass (system-applied specular) eras. Internally the gel is consistent; the incoherence is base-vs-glyph. This mix is why the era is classified `custom`.
- **#10 Variant robustness** — a single baked flat PNG, blue-glyph-depends-on-white-ground. No layered light/dark/clear/tinted authoring; the composition can't survive tinting or dark mode (the glyph would vanish or invert wrongly against a non-white ground). Also: baked gloss + baked drop shadow are exactly what current HIG says the *system* should apply, not the artwork.

## Soft passes (flagged, scored as pass)
- **#1 Mask** — the white ground fills a rounded-rect that reads as the system squircle; exact superellipse match unverifiable at 204px (a faint edge vignette hints the tile is baked into the art).
- **#2 Grid** — optically centred but glyph mass sits slightly low and right (the right-fanning darts pull weight rightward).
- **#3 Silhouette** — a clean, distinctive silhouette with a clear crescent anchor, but *abstract*: it names as "the Canary mark," not as a concrete metaphor. It does **not** communicate "email/mail" — no envelope, no @, no paper (subject-communication gap for an email app).
- **#5 Light model** — reads as one top-gloss light, but the gel treatment multiplies speculars (crescent + each dart carry their own highlight).
- **#8 Depth** — coherent (shadow under glyph, darts in front of crescent mouth), achieved via baked shadow/gloss that HIG would have the system generate.

## Resolution caveat
204×204 web render (macapp.supply), upsampled to inspect. Hex values sampled from the native 204px source are reliable; edge geometry, exact squircle radius, and sub-pixel gloss detail are soft estimates. Not the 1024px master.

## Rhymes with
- **Glossy brand-logomark-on-white-squircle tiles** (aqua/web-2.0 gel family) — the look many cross-platform / Electron productivity apps ship instead of an Apple-era-native icon.
- Structurally adjacent to the **Big-Sur coloured-glyph-on-white-squircle** family, but distinguished by baked gloss and background-dependence. (Hint only — no other digested icons yet to confirm a cluster.)
