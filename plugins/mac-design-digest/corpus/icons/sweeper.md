# Icon: Sweeper

- **Era:** skeuomorphic-quote (free-standing rendered object; pre-Big-Sur idiom, flat-transition adjacent) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 512×512 — half the 1024 master; a downscaled web render, so photo-card imagery and the document chart are soft — fine detail `(estimated)`, silhouette and body ramp `(measured)`)
- **Subject fit:** literal — app does "uninstall apps and clean up the leftovers"; the icon is the macOS Trash can stuffed with app tiles, a document card, and photo prints. Icon-to-subject mapping is direct and legible.

| Dimension | Reading |
|---|---|
| Background | none / transparent (`#00000000` at all four corners `(measured)`) — no squircle plate; free-form object silhouette |
| Glyph | object — a gray waste bin (macOS Trash quote), cylindrical, tapering; optically dead-centre (bbox x82–428, y30–474 on 512 → centre ≈255,252 `(measured)`); fills ~68% width, ~87% height (runs tall) |
| Overlay device | none diagonal tool; instead an **overflowing mouth** — colourful cards poking above the rim, front wall occluding their base |
| Light model | top-down with slight front-left key; baked specular hotspot on the front rim lip (`#EAEBED` `(measured)`), soft vertical body highlight, soft contact shadow beneath — all **baked**, not system-generated |
| Layer stack | contact shadow (baked) → bin back wall / dark cavity (`#4F5558`) → card jumble (app tiles + document + photo prints) → bin front wall with specular rim |
| Palette economy | vessel is monochrome desaturated gray (one hue family, ramp below); **contents are polychrome** — 4+ saturated hue families (blue app tile, green/orange/blue doc, blue/orange/purple photos). Gray dominates ~70% of pixels; colour is spatially contained to the bin mouth |

**Palette `(measured/estimated)`**
- Bin body ramp: `#8C9094` (upper body) → `#5A6064` (belly, darkest) → `#71747A` (base bounce-light) `(measured)`
- Front rim specular: `#EAEBED` · inner cavity: `#4F5558` `(measured)`
- App tile: `#1CA5F2` face → `#1B94E4` lower, white glyph `#FFFFFF` (a rounded bone / crossbones-like mark) `(measured)`
- Document card: `#E9EAE9` ground + green/orange/blue chart chips `~#3FB34D / #F2A03C / #2E8BD6` `(estimated)`
- Photo prints (white-bordered thumbnails): warm `#AF5038`, cool `#2078BA`, purple `#42425F` `(measured/estimated)`
- Accent: **none reserved** — polychrome; brightest focal is app-tile blue `#1CA5F2`

## Signature devices
- **Trash-can quote** — repurposes the macOS system Trash silhouette as the container. Instantly legible, but see Failures (identity collision).
- **Overflowing mouth** — app icons, a document, and photo prints spill above the rim; the front wall occludes their lower edge for real depth/occlusion (not a flat sticker stack).
- **Monochrome vessel / polychrome contents** — a desaturated gray bin frames a rainbow of discarded colourful items; the colour *is* the message ("your colourful apps and photos, thrown away").

## Failures
- **#1 Mask discipline — FAIL.** Fully transparent background, no squircle plate; artwork is a free-standing object designed for the pre-Big-Sur Dock. Era-appropriate for Yosemite–Catalina, but by macOS 26 standards it floats unmasked/plateless and breaks grid unison with modern squircle icons.
- **#10 Variant robustness — FAIL.** Baked specular + contact shadow, single flat PNG, no Icon Composer layer authoring. A mono/tinted render would flatten the gray bin into an unreadable blob (the polychrome cards carry the meaning and can't tint); no dark/clear/tinted survivability.
- **#4 16px squint — SOFT PASS (flagged).** The bin reads as a gray bucket at Dock/Spotlight size and doesn't smear, but at 16px it is **indistinguishable from the system Trash icon** — the app/photo differentiator dissolves into colour noise at the rim. Identity collision, not detail smear.
- **#6 Palette economy — SOFT PASS (flagged).** Strictly, 4+ saturated hue families in the contents exceed the ≤2 + reserved-accent rule; passes only because the gray vessel dominates the pixel budget and colour is contained to the mouth. Subject-motivated, not a reserved focal accent.
- **#7 Figure-ground — SOFT PASS (flagged).** Mid-gray body (`#5A6064`–`#8C9094`) against a light Dock/wallpaper is only moderate contrast; separation leans on the baked contact shadow + rim highlight — which macOS 26 would strip, weakening the read on Tahoe.
- **#2 Grid — SOFT PASS (flagged).** Optically centred but runs tall (~87% canvas height); would crowd the safe zone if a squircle mask were applied.

Passing clean: #3 silhouette (nameable "bin with stuff"), #5 single light model, #8 depth coherence (correct occlusion order), #9 era coherence (consistent pre-Big-Sur rendering), #11 personality (the stuffed-Trash device), #12 no-text (stylised glyphs, not screenshots/photos).

## Brand-palette note (icon vs cover)
Cover is white ground + near-black SF headline with a single **rust-orange** strikethrough accent (`~#C0491F`). The icon does **not** carry that brand orange — its colour is incidental app/photo content, and its hero object is neutral gray. Coherence is partial: both are restrained/monochrome-forward, but the brand's one signature accent is absent from the icon.

## Rhymes with
- Pre-Big-Sur free-object **utility/cleaner** icons: AppCleaner, TrashMe, AppZapper, CleanMyMac-adjacent — rendered vessel + discarded contents, floating on transparency. Style family guess: *skeuomorphic free-object cleaner lineage (Yosemite–Catalina)*. (First icon in the corpus — no in-corpus rhyme yet; hint only.)
