# Icon: Orchard

- **Era:** skeuomorphic-quote (Passbook/Wallet leather-and-barcode revival) · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp`, 204×204 web render (SHA-1 `bdbad7c9`). Category: AI. App: "Bridge AI to Your Apple Ecosystem" — an MCP bridge that lets any MCP-compatible assistant drive native macOS apps (Mail, Messages, Calendar, Reminders, Notes, Music, Maps, Weather…). Website orchard.5km.tech.
- **Resolution caveat:** only a 204px render was available, not the 1024 master — roughly 1/5 linear scale. Fine detail (barcode bars, the mini app-icon glyphs, leather stitching) sits at or below the resolution floor, so some smear I read as "busy" is partly downscaling; per-element values are `(estimated)`, not `(measured)`. The PNG's corners are **transparent (alpha 0)** — the squircle mask is baked into the delivered asset, so I cannot confirm whether the true master is the HIG-required full-bleed *unmasked* square.

| Dimension | Reading |
|---|---|
| Background | **Not a ramp — a modeled object.** A caramel/tan **leather bi-fold folio** filling the frame. Leather field ramps by lighting, not gradient fill: bright top edge **#E3A273** → mid field **#D08B59** → shadowed centre hinge/fold **#9A734E**. A vertical seam splits the panel left/right down the middle (the fold spine) |
| Glyph | **Scene, not a single glyph.** Left panel: a card pocket holding a tucked stack of real macOS app icons, only their tops showing (Weather blue, Mail #E7EFF8-on-blue, Messages green, Music pink **#FF7FA3**, Calendar white+red, Reminders white+dots, Notes yellow, Maps + arrow). Right panel: a debossed tonal **Apple logo** (#D7905D-on-leather, ~1 stop lighter than field) and a white loyalty/membership card |
| Overlay device | **Badge + object composite** — a white membership card (**#FFFFFD**) clipped onto the right leaf, carrying a black **barcode** across the top and Orchard's looping **logomark** (a continuous cursive knot, muted olive-taupe ink ~#8A8378) below it |
| Light model | Soft **top / top-left** key. Short baked contact shadows under the pocketed app cards and beneath the membership card; a gentle emboss highlight on the Apple logo; matte leather, **no hard specular** (not a glass icon). One consistent source |
| Layer stack | (system squircle mask + system shadow) → caramel leather bi-fold base with centre fold seam → debossed Apple logo on right leaf → left-leaf card pocket + tucked mini app-icon stack → white membership card (barcode + logomark) on right leaf → micro contact shadows |
| Palette economy | Chrome is **one** hue family (warm caramel/brown leather) + neutral white paper. But the tucked app cards inject a full spectrum (blue/green/pink/red/yellow). Diegetic — the rainbow *is* the subject ("your apps") — but it breaks the ≤2-hue floor on a strict read |

## Signature devices
- **The Passbook quotation.** Leather folio + barcode + loyalty card is a near-literal revival of Apple's own 2012 iOS 6 **Passbook/Wallet** skeuomorph — stitched-leather-and-ticket. Choosing a decade-old discarded Apple visual language, in the Liquid-Glass era, is a committed direction, not a template default. Subject-mining is honest: the app *bridges to Apple's ecosystem*, so it wears an Apple-heritage material.
- **"Your apps in a wallet."** Reproducing the actual macOS system app icons as cards tucked in a pocket is the whole concept in one move — the icon literally shows what it connects. Distinctive and immediately story-telling at hero size.
- **Debossed tonal Apple mark.** The Apple logo pressed into the leather (~1 stop lighter, no colour) reads as an ecosystem/authenticity stamp without stealing focus — the same tonal-emboss trick classic leather-bound Apple icons used.
- **The fold-spine as "bridge."** The centre seam divides *your Apple apps* (left) from *Apple + Orchard's mark* (right); the fold is the join. A quiet narrative device, not just a texture line.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black the icon is a featureless rounded square. The wallet-ness lives entirely in interior colour, texture, and the vertical seam — all of which silhouette discards. No nameable object-shape survives. This is the structural cost of a full-bleed object icon.
- **#4 16px squint test — FAIL.** The busiest liability. At menu-bar/Spotlight size the ~8 miniature app icons collapse into coloured mush, the barcode and logomark become specks, and the emboss vanishes. What survives is "a two-tone brown tile with a white patch bottom-right" — legible as *a* tile, not identifiable as Orchard. The personality is bought with detail that the Dock cannot render.
- **#10 Variant robustness — FAIL.** Identity is colour- and texture-dependent with no carrying monochrome glyph. A tinted/clear/mono render would strip the leather warmth and the app-card colours (which *carry the meaning*), leaving an anonymous stamped rectangle. Not authored as Icon Composer light/dark/mono layers; the concept doesn't reduce to a single-colour mark.

## Soft passes (flagged for synthesis)
- **#1 Mask discipline.** Composition respects the squircle and doesn't fight it — but the asset ships **pre-masked** (baked alpha corners), and I can't verify a full-bleed unmasked master exists. Web-render artifact, likely fine in the real deliverable, but unconfirmed.
- **#2 Grid adherence.** Optically centred on the fold, but the object **bleeds to the mask edge** on all sides (Wallet/Books "object-fills-frame" convention) rather than sitting inside a safe-zone margin — a deliberate object-icon choice, noted not faulted.
- **#6 Palette economy.** Passes on chrome (one hue + white) only by treating the multicolour app cards as diegetic content; on a literal hue count it's 5+ families.
- **#7 Figure-ground contrast.** Strong for the white card on brown leather (>4.5:1); muddy for the app cluster on leather, which turns to mid-grey jumble in grayscale.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | soft pass (ships pre-masked; master unverified) |
| 2 | Grid adherence | soft pass (full-bleed, bleeds to mask edge) |
| 3 | Silhouette | **FAIL** |
| 4 | 16px squint | **FAIL** |
| 5 | Single light model | pass (one top/top-left key, matte) |
| 6 | Palette economy | soft pass (diegetic rainbow) |
| 7 | Figure-ground contrast | soft pass (card strong, cluster muddy) |
| 8 | Depth coherence | pass (pocket/emboss/clip ordering + shadows all consistent with the light) |
| 9 | Era coherence | pass (uniformly skeuomorphic — leather, stitch, emboss, barcode, paper) |
| 10 | Variant robustness | **FAIL** |
| 11 | Personality | pass (multiple nameable devices — Passbook quote, apps-in-pocket, tonal Apple emboss) |
| 12 | No-text | pass (no words; barcode is graphic — but note it *reproduces other apps' icons*, unusual) |

**Total: 9/12, 3 failures (#3, #4, #10).**

## Rhymes with (hint only — for icon-cluster synthesis)
- **Skeuomorphic-revival object icons** built from literal materials (leather / paper / stitching): Apple's own Passbook & Wallet, Find My Friends (leather), Contacts (leather book), Game Center (felt). Style-family guess: **"leather-and-ticket Passbook-lineage skeuomorph."**
- Icons whose concept is **"a container holding recognisable smaller things"** (a wallet of app cards, a shelf of covers) — identity via contents, not silhouette. These reliably fail #3/#4 the same way.

## Brand-context note (cover coherence)
Cover ground is a warm peach/cream ramp **#FFE2D0 → #FFF0E3** with a faint squircle-grid watermark; the "Orchard" wordmark is warm brown. This coheres tightly with the icon's caramel leather — the whole brand sits in one warm terracotta/tan temperature. The cover also floats the *connected* app icons (a burst, a cube, a green quote bubble, a heart-swirl, "…") wired by dashed lines into the Orchard wallet — restating the icon's "hub that holds your apps" thesis. Palette coherence between icon and brand: **high**.
