# Icon: Coreviz Studio

- **Era:** custom (flat two-tone web brand-mark; quotes no macOS icon era) · **Rubric:** 11/12 · **Digested:** 2026-07-19

| Dimension | Reading |
|---|---|
| Background | flat `#000000` full-bleed (no gradient, no ramp, no scene) |
| Glyph | abstract geometric mark — an off-white `#F8F8F8` rounded-hexagon "nut/aperture" ring with a concentric black hex knockout; occupies ~58–62% of canvas, optically centred (x-span 45–160, y-span 38–163 on 200px → centre ~102,100, a few px right of true centre) `(measured on 200px render)` |
| Overlay device | none — single-plane knockout, no diagonal tool / badge / frame |
| Light model | none — flat vector cutout; no baked shadow, no specular, no top-down modelling. Reads as a web/app logo dropped on a black square, not a lit macOS icon |
| Layer stack | black full-bleed field → off-white rounded-hexagon glyph → black rounded-hexagon bore (negative-space knockout) |
| Palette economy | 0 hue families (pure neutral); two tones only, black + off-white `#F8F8F8`; no accent. Maximally economical |

## Signature devices

- **Concentric rounded-hexagon "nut / aperture" ring** — a hexagon with super-elliptical (heavily rounded) vertices, points to the sides (flat-ish top/bottom), with a same-orientation hex bore. Reads as a bolt-head/nut or a camera-iris core. This is the whole mark.
- **Negative-space bore as the only focal detail** — the black centre hole is cut from the glyph rather than drawn, so figure-ground does all the work; no interior shading.
- **Max-contrast two-tone** — `#F8F8F8` on `#000000` ≈ 19:1; the icon is essentially already its own monochrome mask.

## Failures

- **#10 Variant robustness** — the mark is white-on-black and *background-dependent*: the glyph exists only as the light hexagon against the dark field. A system-generated tinted-light or clear-light render would collapse figure-ground (off-white glyph on a light-tinted ground → near-invisible). It is not authored in Icon Composer, so it ships one appearance with no controlled light/dark/tinted layers.

## Soft passes (flagged, still scored as pass)

- **#2 Grid** — optically centred and well-weighted, but the glyph sits a few px right of true centre (x-span 45–160 on a 200px canvas).
- **#4 16px squint** — the bold hex ring survives at menu-bar size, but the interior hex bore risks closing up / muddying at 16px; two-tone max-contrast is what saves it.
- **#5 / #8 Light & depth** — no light model and no depth at all; passes only because a flat cutout has no lighting/z conflict to create. Vacuous passes, not crafted dimensionality.
- **#9 Era coherence** — internally consistent flat two-tone, but it participates in no macOS icon era (not Big Sur soft-lit dimensionality, not Liquid Glass layered translucency). It reads as a Vercel/Linear-adjacent web brand mark on a black square.
- **#11 Personality** — has a nameable device (the hex-nut/aperture ring), clearing the generic-glyph-on-gradient bar — but the rounded-hex mark is a common dev/AI-startup logo shape, so the differentiation is modest.

## Rhymes with

- Flat monochrome geometric brand-marks in the Vercel/Linear web-startup register: black canvas + single off-white glyph + serif-display wordmark (the cover pairs the mark with an italic modern-serif "media workspace." headline and "Backed by Vercel / Antler" — web-first lineage confirmed).
- Within-corpus hint (for synthesis to confirm): rhymes with other flat two-tone abstract/geometric marks rather than any lit Big Sur tool icon; distinct from the dimensional-object cluster.

## Notes

- **Resolution caveat:** subject is a **200×200 web render**, not a 1024 master. Edges are anti-aliased at low res (grays `#525252`/`#717171` appear only as ~1px vertex antialiasing, 76 px max); subpixel geometry is `(estimated)`. Cannot verify a true system squircle mask — the artwork is full-bleed black to all four corners, so it is mask-safe (the system rounds it), but no corner-radius data is recoverable.
- **Brand coherence (strong):** the icon's `#000000` / `#F8F8F8` maps exactly onto the cover's black ground + off-white hex logo + white serif type — one tight two-tone system across icon and site.
- **Subject-communication gap:** the app is an AI photo/video workspace ("understands your photos and videos"), but the mark communicates nothing about media, images, or AI — it is a pure abstract geometric identity. Deliberate brand choice, not a defect, but worth noting for the "an icon should say its subject" rule.
