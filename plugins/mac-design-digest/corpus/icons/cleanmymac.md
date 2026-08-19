# Icon: CleanMyMac

- **Era:** Big Sur unified (glossy front-facing object + diagonal tool overlay) — **not** Liquid Glass, despite shipping on macOS 15+/Tahoe; the gloss and specular are *baked into the artwork*, which Liquid Glass explicitly forbids · **Rubric:** 11/12 (3 soft passes, 1 hard failure) · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png` that is actually an **AVIF container** (`ftyp` header), 384×384 web render. Squircle mask + pale field baked into the bitmap (corners are opaque near-white, not transparent). Full-bleed 1024 master and any authored Icon-Composer layers **not seen** — treat the baked field/gloss/shadow as the site's ship render, not verified source layers. Metal-arm hexes are region-averaged from thin strokes, so `(estimated)`.
- **Subject:** MacPaw's Mac cleaning & maintenance software ("the best Mac cleaner & maintenance software"). The icon must say *"clean/service your Mac"* — and it does so **literally**: a miniature iMac is the object, a chrome maintenance tool is the verb.

| Dimension | Reading |
|---|---|
| Background | Ramp — pale near-white lavender field, corners `#FEFEFE` → mid-band `#F3EDFF` (very low-chroma periwinkle, ~hue 265), plus a **hot-pink ambient bloom** `#FF7BEE` glowing off the display's upper-right onto the field. Sky-logic is inverted-soft: edges lighter, centre carries the object's colour cast |
| Glyph | Object — a stylised **iMac / desktop display** at a slight front-3⁄4 tilt. Screen is a candy-magenta vertical gradient: highlight `#FF72E9` (top-left) → body `#EC2DCB` → deep `#D816B8` (bottom), ~hue 315. Stand is periwinkle: lit face `#AFA9E7`, neck `#7679BC`, foot `#6067BC`. Optically centred, object mass upper-centre, stand anchoring the bottom third |
| Overlay device | **Diagonal tool** — a jointed chrome/silver arm (reads as a wiper/brush/caliper) laid corner-to-corner across the screen, top-left down to lower-right. The Apple TextEdit/Preview "tool at an angle" tradition |
| Light model | Soft top / top-left, baked (not system-composed). Specular bloom on the screen's top-left, bright top edges on the metal `#EDEBF4`, short cast shadow down-right beneath the display. One coherent source |
| Layer stack | back → front: [1] pale-lavender squircle field + pink ambient bloom · [2] cast drop-shadow · [3] periwinkle stand + foot with embossed `C` monogram · [4] glossy magenta display · [5] chrome diagonal tool |
| Palette economy | Two hue families — **magenta** (screen, the sole saturated accent) + **periwinkle/lavender** (field, stand, metal). Chrome ramps `#EDEBF4` → `#DAD5EE` → `#C1BED9` pick up the lavender cast. Accent saturation is correctly reserved for the focal screen |

## Signature devices
- **The subject *is* the object** — the app cleans Macs, so the icon draws a Mac. Depicting the target appliance (a magenta iMac) rather than an abstract "freshness" glyph is a committed, non-template choice; it communicates the noun ("your Mac") where sparkle/broom icons only communicate the adjective ("clean") `[GOLDEN-NUGGET]`.
- **Diagonal chrome maintenance tool crossing the plane** — the jointed silver arm over the screen is the verb, and it uses Apple's own diagonal-tool grammar (TextEdit pencil, Preview loupe). The one device that carries the "maintenance" read.
- **Candy-gloss screen** — an ultra-glossy magenta gradient with baked specular bloom: a skeuomorphic quote (wet, lit glass) inside an otherwise Big Sur composition. This is the MacPaw house saturation — the icon's entire warmth (and its brand equity) lives in that magenta.
- **Embossed brand monogram** — the MacPaw/CleanMyMac `C` broom mark rendered tone-on-tone in the stand: a logo glyph, not text, so it survives the no-text rule while quietly branding the base.

## Failures
- **#10 Variant robustness (hard, out-of-era) — FAIL.** No authored dark/clear/tinted layers; the read *depends* on the pale-lavender field and the baked magenta gloss. Rendered tinted or clear (macOS-26 Liquid Glass appearances) the whole thing collapses — this is a Big Sur bitmap, not a Liquid-Glass composition. Era-appropriate, but it is genuinely not macOS-26-ready, so it fails the current-era check honestly.
- **Soft passes** (the score never travels without the asterisk):
  - **#3 Silhouette** — filled solid black, "screen on a stand" is nameable, but the jointed metal arm reads as an ambiguous stick/hand, not obviously a *cleaning* tool. The maintenance metaphor is silhouette-fragile.
  - **#4 16px squint** — at menu-bar/Spotlight size the thin chrome arms smear into the magenta screen and vanish; you're left with "a pink iMac." Glyph still identifiable so it functions, but the entire cleaning verb is lost at Dock size — the icon becomes a colour-blob brand mark.
  - **#2 Grid** — the diagonal tool pushes visual mass to the upper-right; the stand counterweights but the composite sits marginally off optical centre, reading slightly top-heavy before the shadow settles it.

## Rhymes with
- The **Big Sur glossy-object + diagonal-tool utility** family: literal-appliance maintenance icons (a device being serviced by a tool), and the wider skeuomorphic-quote object icons that keep baked gloss on macOS 15+. Sibling in this corpus: **cachesweep** (same "clean my Mac" register, opposite strategy — cachesweep abstracts to `sparkles`-on-indigo and communicates only "clean"; CleanMyMac draws the Mac and communicates "your Mac + a tool"). The pair is a clean literal-vs-abstract contrast for the same job.
- Palette coherence with the app: the cover is this same icon floated on a **pink/lavender blurred floral landscape** — magenta+periwinkle icon on magenta+periwinkle scene, one brand system. MacPaw's signature magenta is the through-line.
- Hint: seed of a probable **"literal-appliance, diagonal-tool"** icon cluster — needs ≥2 more members before promotion.
