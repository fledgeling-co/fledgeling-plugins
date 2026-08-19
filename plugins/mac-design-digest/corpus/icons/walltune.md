# Icon: WallTune

- **Era:** Big Sur unified (front-facing squircle, baked soft shadows, gradient card — *not* Liquid Glass) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 512×512, SHA-1 a22424ee) · **App:** WallTune — "animated video lock screens for your Mac" (Utility)
- **Resolution caveat:** 512×512 is half the 1024 master; this is a resized web render. Micro-shadow softness and any faint specular are `(estimated)`, not clean-measured. Corners outside the squircle are baked pure `#000000` in the PNG (mask pre-applied by the render, not a design layer).

| Dimension | Reading |
|---|---|
| Background | Subtle vertical **ramp** `#2A2E35 → #1B1A1A` (estimated) — cool charcoal (faint blue) at top → warmer near-black at bottom; sky-logic dark field that makes the warm focal glow |
| Glyph | **Object pair.** (1) A rolled cream sheet / cylinder, near-white `#FEF7F5` with a soft-pink underside `#FDD8D2 → #F49BAA` and a magenta roll-mouth `#DC3A75` around a dark inner hole; (2) a warm gradient "wallpaper" card behind it. Sits centred-as-a-unit, biased right — the roll on the left safe-zone, card filling centre-right |
| Overlay device | **Other** — the rolled sheet overlaps the front-left edge of the gradient card (a vertical reinterpretation of Apple's "tool crossing the plane" tradition; the roll *is* the tool) |
| Light model | Soft top-down ambient; short soft drop shadows (roll onto card, card onto field). Matte paper + matte gradient — no glass specular, no refraction/translucency. Big Sur baked-shadow lighting, not Liquid Glass environmental |
| Layer stack | 1 dark squircle field (ramp) → 2 warm gradient card (rounded-rect, soft drop shadow) → 3 rolled cream sheet in front, casting a soft shadow onto the card |
| Palette economy | 1 warm ramp family (magenta→orange→yellow) + neutral-dark ground + cream roll. Saturated accent (the magenta roll-mouth + the card) is reserved for the focal; ground stays neutral. Soft pass — the warm arc is wide (pink to yellow) but reads as one continuous ramp |

## Palette (hex)

- **Background field:** ramp `#2A2E35` (top) → `#1B1A1A` (bottom) (estimated)
- **Gradient card ("the wallpaper"):** diagonal ramp — magenta-pink TL `#D13F6E` → coral `#FA7471` → orange `#FFA641`/`#FFBD34` → gold-yellow `#FECE42` (bottom-right brightest) (estimated)
- **Rolled sheet:** cream/near-white `#FEF7F5` body → pink underside `#FDD8D2 → #F49BAA` (estimated)
- **Roll-mouth accent:** magenta `#DC3A75` ring around a dark inner hole (estimated)

## Signature devices

- **[GOLDEN-NUGGET] The unrolling wallpaper** — a rolled cream sheet peeling back to reveal a vibrant gradient field. Committed, subject-mined literalism: WallTune sells wallpapers, and the icon *is* a wallpaper mid-unroll. This is a directional choice, not a template glyph-on-gradient.
- **The roll-mouth** — the visible cylinder opening (magenta ring + dark hole) is what sells the "roll" read in silhouette and drops a focal pop of pink into the lower-left; without it the sheet flattens to a bar.
- **Vibrant gradient as content, neutral field as stage** — the same UI de-emphasis logic applied to an icon: near-black ground exists so the warm ramp reads as *emitted light*. Strong figure-ground (cream-on-black >10:1).
- **Palette coherence with the app** — the cover's wordmark is a miniature of this exact icon and the same magenta→gold ramp washes the page footer; icon and brand share one ramp. `(confirmed)` across icon + cover.

## Failures

- **#10 Variant robustness (Liquid Glass) — FAIL.** The whole metaphor is carried by the multi-hue warm gradient and the dark field. In a tinted/mono system render the gradient collapses and the "wallpaper" reads as a blank card; there is no authored Icon Composer layer set to fall back on. Honest note: this is an *era-expected* miss — the icon is a competent Big Sur-era design that simply predates (or declines) the macOS 26 Liquid Glass variant system, exactly the lag the macos-27 kit deltas predict for shipping apps. Not a craft defect within its own era.

## Soft passes (flagged for synthesis)

- **#2 Grid** — balanced as a unit but biased right; the leftward roll + rightward card read as a left-to-right "unrolling" gesture rather than optical dead-centre. Intentional, but note the asymmetry.
- **#3 Silhouette** — a cylinder beside a rounded rectangle. Nameable as "a roll and a card," but the *wallpaper* meaning only fully lands with colour; filled solid black it is generic. The roll-mouth is what keeps the silhouette from being a plain bar.
- **#6 Palette economy** — one continuous ramp, but it spans a wide magenta→yellow arc; rich rather than economical. Coheres because it is a single gradient, not three separate accents.

## Rhymes with

- Big Sur-era **object-on-charcoal utility icons** where a saturated gradient card is the focal element against a neutral-dark field (warm-gradient-on-charcoal family).
- The **paper/scroll/roll object** lineage (rolled-sheet, poster-tube motifs) — the tactile-object metaphor rather than an abstract mark.
- Style-family guess for clustering: *warm-luminous object-metaphor, Big Sur baked-shadow* — pairs a subject-mined tactile object with a vibrant gradient "screen" on a de-emphasised dark stage.
