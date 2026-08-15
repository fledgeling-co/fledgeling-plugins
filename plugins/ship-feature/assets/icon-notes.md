# ship-feature icon — "The Launch"

Commissioned through `create-mac-icon`. Working directory:
`.rebuild-workspace/icons/ship-feature/`. Everything below is measured off the
files in it; the numbers are reproducible with the scripts named.

## The brief, and the one thing it did not say

ship-feature takes **one** feature from a rough idea to merged, verified,
production code. One vessel, taken all the way to launch. The chosen concept
was the launch instant itself — stern still on the slipway, bow already cutting
water, the ember accent on the bow wave.

The sibling list handed over named ship-armada (three hulls in echelon), the
shipyard icon (a hull mid-build on a cradle) and trawl (the dark trawler). It
did not name **`create-swe-project`**, which already owns an amber dinghy poised
on pale-blue slipway trestles above water — a genuine near-neighbour of this
exact concept, found by looking at the shelf rather than at the list. The
separation was therefore designed rather than assumed, and it is deliberate on
five axes:

| | create-swe-project | ship-feature |
|---|---|---|
| vessel | open dinghy, no deck | decked vessel, sheer + wheelhouse |
| moment | poised, dry, at rest | launch instant, hull already wet |
| accent | amber, on the hull | ember, on the water |
| ground | cool blue-white | warm porcelain |
| view | high three-quarter | low, near-elevation |

That separation is complete at 128px and above. At 16px both reduce to a raked
hull, and that residual collision is recorded as a liability rather than
claimed away.

## Direction

**Chosen:** Tahoe gel-glass, sub-register (a) — porcelain cushion tile carrying
one gel object with a real contact shadow — crossed with the Big-Sur object
tile's 3D-miniature idiom in its Tahoe-softened form (matte satin, real contact
shadow, no gloss).

**Runner-up:** Direction 4, Dark-Field Emissive. An ember bow wave burning on
black water is the more dramatic picture and it was rejected on one fact about
the shelf, not on taste: the dark register belongs to trawl alone.

**Devices:** #16 the icon performs the verb (the composition physically enacts
launching), #21 overlap-as-identity (the water plane painted over the hull),
#22 emissive interior under glass (the wave is the sanctioned second light).

**Signature move — the waterline crosses the hull.** One object in two states
at once: the stern half is dry gel above the line, the bow half reads *through*
a translucent water plane below it, and the ember wave breaks exactly where the
two meet. It is authored as a literal overlap — the hull is drawn whole, then
the water plane is painted over it at 0.90 — so the blend is real geometry
rather than a baked gradient. That is what keeps rubric #10 honest.

## Corpus values this master was built from

Sampled inside the tile on `references/corpus/apple-2026/` captures 06 (Home),
18 (telescope), 28 (Photos) and 30 (the box miniature), before the first line
of the build script:

- Porcelain ground ramps **1.000 at top centre → 0.922 at bottom centre** — a
  0.078 luminance drop, key light top and very slightly left. The brightest
  pixel is at the top edge, not at a specular.
- The warm gel object's median is **`#FFBD4A`** (hue 38, S 0.71) and its shadow
  end is **`#F69E37`** (hue 32, S 0.78). **Saturation rises as value falls.** A
  gel that desaturates in shadow reads opaque.
- The contact shadow under a warm object is **warm, not dark**: (235, 226, 213)
  against a (235, 235, 235) ground — ΔL only 0.034 at contact, recovered by
  ~20px on a 412 tile (~50px at 1024). It is ambient bounce, not occlusion.

The accent was pulled to the shelf rather than to Apple: the family's warm
accents cluster at hue 10–22, S 0.65–0.80, V 0.80–0.92 (ship-armada `#CC4127`,
create-skill `#E77432`, dossier-report `#EA663F`). This icon's ember body is
`#E9682F` with a `#FF8A3D` core.

## Spec

- **Canvas** 1024 full-bleed; the set's exact superellipse from
  `squircle-path.txt` used as the clip and as the tile's rim-light stroke.
- **Palette, two families.** Warm neutral: ground `#FAF7F1 → #E4DBCB`, water
  `#C6BDAC → #8E8572`, stone `#DED5C6 → #93866F`, rails `#7A6E5C`, hull
  `#5A616A → #181A20` with warm AO `#2C2420`, deck and wheelhouse `#F2ECE1`.
  Ember, reserved entirely for the wave and the light it throws: `#B93C19` /
  `#E9682F` / `#FF8A3D` / `#FFD9B6`.
- **Light.** One soft top light tilted slightly left, rim highlights and soft
  AO, zero hard speculars, plus the sanctioned second source: the emissive
  wave, which lights the hull's bow flare and streaks down the water.
- **Layers.** `bg` cushion + vignette · `mid` slipway, rails, cast shadows ·
  `fg` hull, deck plane, wheelhouse · a water plane over the hull (the
  crossing) · `highlight` wave, lip, hollow, beads, rims. Maps 1:1 onto Icon
  Composer.
- **Geometry.** Everything lives in the hull's own keel frame (`u` along the
  keel 0→1, `v` down from the sheer) and reaches the canvas through one
  rotation and translation. The deck is the same frame displaced by one shared
  `FAR` vector, so the top face exists without a second projection to keep in
  register. The wave's anchor is **derived**, not placed: a bisection finds
  where the forefoot pierces the waterline, and every wave element is rooted
  there, so changing the rake moves the wave with it.

## Engines

| Take | Engine | Outcome |
|---|---|---|
| **A** `icon.svg` | hand-authored layered SVG via `build_icon.py` | **ships**, 11/12 |
| A0 | Engine A before the loop | 9/12 — kept as the "before" row |
| B | media-gen-pro `svg: true` (Arrow 1.1) | 6/12 — lost |
| C1 | media-gen-pro raster, GPT Image 2, 4 corpus references | 9/12 — **material target** |
| C2 | second raster take | 8/12 — lost on register |

C1 won the material judgment, as the skill's own evidence predicts it will.
C2, from the identical prompt, drifted its ground to cool photographic grey —
trawl's register, not this one — which is worth recording as a fact about how
far the raster engine wanders on ground colour.

B's failure was useful before it was discarded: it split the tile 50/50 on a
hard horizon and drew an open dinghy, which is both the sibling collision and
the "identity is a colour relationship" failure. Seeing it early is why the
master's waterline crosses the *object* rather than the *frame*.

## The fidelity loop — 14 scored rounds, `fidelity-runs/r00 … r13`

Mean composite **0.5827 → 0.6177**; 1024 (the material gap) 0.4909 → 0.5090;
32px 0.7307 → 0.7673; 16px 0.7648 → 0.7861.

Four rounds were rejected by the gate. Two of those were kept anyway, on the
documented authority that the rubric outranks the gate:

- **r02** (−0.0034, noise) restrained an ember bounce that had turned the whole
  bow bronze. The composite could not see it; the palette and figure-ground
  checks could.
- **r11** (−0.0451) scaled the vessel into its own headroom for 16px identity.
  The reference frames its vessel smaller, so converging on it was costing
  check #4, which is non-negotiable. r12 then pulled the overshoot back from
  72% to 69% of tile width.

**The bow wave took three separate scaffolds and that is the round-cost worth
recording.** A smooth envelope-driven mound (r03–r04) read as molten wax. A
comb of 21 hard-edged filaments (r05–r06) read as a sea urchin, then as flame
once the value ramp was added. Only an explicit asymmetric control polyline —
long windward rise, peak just forward of the stem, short steep fall, with a lip
that overhangs its own hollow — reads as breaking water (r08). The final round
then cut its height by a third (r10), because the shelf, not the reference, is
the judge of how much accent a tile can carry.

## Rubric: 11/12

Passes 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12. The one lost point is **#2 grid**:
the vessel spans 69% of tile width against the catalogue's 55–65% band. It was
bought deliberately for 16px identity and it is the first number a future round
should test.

Measured on the real renders: figure-ground **4.04:1** at 48px (hull darkest 5%
0.199 against porcelain 0.958), 3.67:1 at 32px; whole-image self-contrast 0.415.

## Known liabilities

1. **69% tile width** — over the band, traded for small-size identity.
2. **The wave is the least-resolved element.** Three scaffolds in, the third is
   the least wrong rather than clearly right; at 128px it still reads slightly
   as a lit mass rather than as broken water.
3. **`create-swe-project` collision at 16px.** Fully separated at 128px and
   above; at menu-bar size both are a raked hull.
4. **The three wave-train arcs** are the only element that reads as drawn
   rather than lit. Dimmed by a third in r11; they could still go.
5. **No blind panel was run.** The shipping decision rests on the gate, the
   12-point rubric, and repeated looking at the 16/32/48px renders and at the
   whole 22-icon shelf — not on `judge_panel.py`.

## Files

- `icon.svg` — the layered master that ships
- `build_icon.py` — the generator; every geometry and material value is a named
  constant, so a future round is a parameter edit
- `icon.png` (1024) · `icon-256.png` · `icon-128.png`
- `audit.html` + `audit-renders/` — the contact sheet, all five takes scored
  including the losers; passes `audit_sheet.py check` with exit 0
- `fidelity-runs/r00 … r13` — per-round `score.json`, residual and edge maps,
  and the `build_icon.py` snapshot that produced each. Trajectory data; keep it.
- `icon-engineB-arrow-b549df.svg`, `icon-engineC-dcf6f9.png` (= `reference-C1.png`),
  `icon-engineC-0b4986-2.png` — the alternates
