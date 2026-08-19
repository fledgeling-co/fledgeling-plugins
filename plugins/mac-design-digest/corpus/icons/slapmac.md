# Icon: SlapMac

- **Era:** custom (illustrated mascot sticker — quotes no coherent macOS era) · **Rubric:** 8/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply · **Category:** Utility · **Subject:** "your macbook finally has feelings" — a novelty app that anthropomorphises the Mac
- **Resolution caveat:** 204×204 pre-masked `.webp` (alpha squircle already baked in — corners are transparent, not a full-bleed 1024 square master). Hex values reliable; fine anti-aliased edges and the screen-face detail are already smeared at this size. Cannot verify an unmasked square master or any Icon Composer layer structure — this is a resized web render.

| Dimension | Reading |
|---|---|
| Background | ramp, single green hue: **#4C7A0A** (lighter yellow-green, top) → **#1F3300** (dark olive, bottom), sky-logic vertical (measured) |
| Glyph | mascot scene — a 3/4-view laptop with a face being slapped by a disembodied hand. Bright chartreuse fills **#AFD526 / #B1D82E**; dark forest line/shadow work **#183000 / #243500**; mid-green body **#3F6900 / #617349**. Optically sits slightly high-and-right of centre; hand + burst rays crowd the right/upper safe-zone margin (measured) |
| Overlay device | comic **impact starburst** where the hand meets the keyboard + short manga motion-ticks — a cartoon "slap" trope, not a mac tool overlay |
| Light model | inconsistent: short baked drop-shadows under laptop and hand (implies soft front/top light) **plus** a non-directional lime outer-glow rim along the bottom edge (no source). No specular/glass. (estimated) |
| Layer stack | green ramp field → lime outer-glow rim → laptop (screen-face + keyboard base) → impact starburst → slapping hand → motion ticks |
| Palette economy | effectively **monochromatic green** — background, laptop, hand, and burst all sit in one chartreuse→olive family. Extreme economy, but it is also the icon's undoing (see Failures #7). Accent: none in the icon proper (the red cheek-blush that reads on the cover is smeared out at 204px) (measured) |

## Signature devices
- **The comic slap** — disembodied hand + radial impact starburst + motion-ticks: a manga/cartoon-violence trope imported wholesale. This is the whole joke and the whole personality; it is genuinely committed, not template. `[GOLDEN-NUGGET]`
- **Anthropomorphised device** — the laptop screen carries a face (crying/flushed on the cover; a smeared open-mouth blob at icon size). Mascot-with-a-face, not an object glyph.
- **Monochrome-green drench** — one hue carries ~100% of the surface. Reads as a deliberate "toxic/slime green" brand commitment, coherent with the cover.

## Failures
- **#3 Silhouette test** — filled solid black it is a cluttered blob: laptop + overlapping hand + two starbursts + motion ticks give no single nameable shape. Multi-object with no dominant anchor.
- **#4 16px squint test** — the comic detail (starburst, motion ticks, keyboard rows, screen-face) collapses to an olive-green smudge; already visibly smearing at 204px, so Dock/Spotlight/menu-bar duty fails.
- **#9 Era coherence** — baked drop-shadows + a non-directional outer glow + hard cartoon outlines are the web-graphic/sticker tells the anatomy doc explicitly flags as "not mac." It belongs to no macOS era language; classifying it `custom` is honest but it is web-sticker, not a considered older-era quotation.
- **#10 Variant robustness** — a fixed, flat, monochrome-green illustration with no layer separation; in tinted/mono/dark renders the whole green-on-green scene flattens to one indistinct shape. No Icon Composer structure to survive on.

**Soft passes (flagged):**
- **#1 Mask** — art fills the squircle without fighting it, but the master is already pre-masked (can't verify a clean square source).
- **#2 Grid** — the scene is roughly centred but busy; burst rays and the hand press into the right/upper margin rather than sitting on the grid circles.
- **#5 Light** — mostly readable as top/front-lit drop shadows, but the sourceless glow rim muddies it.
- **#7 Figure-ground** — the bright lime laptop lid pops (~2.5–3:1 est.), but the dark-green keyboard/base dissolves into the dark lower field; the lower silhouette is lost.
- **#8 Depth** — planes are ordered sensibly, but the bottom glow rim is a depth cue with no light source.

## Rhymes with
- Web-sticker / Gumroad-style mascot icons and joke-utility icons — illustrated-mascot-sticker family. The **opposite** end of the corpus from Big Sur tool-on-squircle or Liquid Glass layered-glass icons: no clean glyph, no system light model, no variant discipline. Nearest kin would be any other cartoon-mascot novelty icon in the corpus (hint for synthesis — a possible "sticker/mascot novelty" cluster if ≥3 appear).
