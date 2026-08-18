# better-goal icon — the held needle

Rebuilt 2026-08-19. This icon was never put through the pipeline: its sheet carried
**one take against a floor of three**, so there was no comparison behind its
verdict, and a retrospective scoring on 2026-08-19 put it at **8/12** against a
10/12 delivery bar. It was the last icon in the marketplace below the bar.

Two things had already been fixed that morning and were not redone here: the
generator was given named `#bg` / `#mid` / `#fg` / `#highlight` groups so both SVGs
passed `fidelity.py structure`, verified pixel-identical before and after; and
`audit-renders/` was refilled with real renders of the master rather than
byte-identical copies of the shipped PNGs.

The defect that cost it the bar was **figure-ground**: a pale cream dial on a pale
cream cushion, measured at **1.05:1** face-against-tile where check 7 asks for 3:1,
and **0.1142** RMS contrast at 16px, rank 35 of 38. The hub and the accent were
fine; the disc simply was not there.

**The device was not in question.** `better-loop` was rebuilt on 2026-08-18
specifically to stop being this icon — the two shipped as the same cream dial with
the same charcoal hub, the same needle and the same vermilion top mark, and at 16px
they were one icon. better-loop moved to a machined graphite rail, and better-goal
keeps the dial and the target band, which is recorded as its device in the set's
shelf register. So this was a **material and value** problem inside a decided
device, not a search for a new metaphor.

## Direction

**Direction 2, Tahoe gel-glass, sub-register (a): a porcelain cushion carrying one
gel/graphite object**, hybridised with device #20 (data-as-glyph — the reading with
a single accent datum) and, at the one place the stop stands proud of the bezel,
#18 (edge-bleed physicality). Runner-up was Direction 8, Instrument Emblem, and it
is what the predecessor was: the app's own artifact at icon scale with nothing
added. The reason to move off it is the predecessor's own #11 deduction — a
tick-ring dial with a needle is one step from a stock speedometer, and the element
that made it specific was the first to disappear as the icon shrank.

Matching the fledgeling set: porcelain ground, one ember accent, the shared
superellipse from `plugins/create-mac-icon/assets/squircle-path.txt`, exports at
1024 (`icon.png`), 256 and 128.

## Device and signature move

**A machined graphite dial, with a vermilion accept band cut through its face and
out to the rim, and a graphite pawl straddling the band's counter-clockwise end and
standing proud of the bezel.** Cream graduations run from the foot of the travel,
clockwise up the left flank, and stop where the band starts. A porcelain needle
stands inside the band with the pawl behind it.

The signature move is that **the band is open on one side and stopped on the
other**, so the tile says the needle can only arrive. That is the skill performed
rather than illustrated: `better-goal` arms a `command` Stop hook judged by exit
code, and a gate judged that way closes once — a goal that has been met is not
allowed to fall back. The empty sector clockwise of the band is the part of the
circle the reading never visits.

The accent is spent exactly **once**, at 2.52% of the tile in one contiguous piece,
and it sits **on the object's silhouette edge** rather than as linework floating in
a light field. That is `better-loop`'s acid test, taken here, and the sheet has the
counter-example: the Arrow vector take independently put the same band *inside* the
tick ring, and at 16px it is a smear.

**Deliberately not encoded: the disarm-after-three-identical-failures rule.** Three
decaying pawls were sketched and dropped. Each spends the family's one warm hue
three times, or reads as a set of ratchet teeth that dither to grey by 48px — the
same finding `better-loop` recorded for the doubling backoff. One gate, one stop.

## Palette

Every value below was sampled off the corpus or off the family before the first
line of the build script, not reasoned about.

| Role | Hex | Provenance |
|---|---|---|
| cushion, lit | `#FCFAF4` | family: deck-craft, test-campaign, whats-left |
| cushion, mid | `#F3EDE1` | " |
| cushion, corners | `#DED5C2` | " |
| inner rim light | `#FFFDF8` | the cushion tell every Tahoe tile carries |
| vignette | `#8B7F66` at 0.24 | " |
| cast shadow | `#3B3327` | warm, even under a cool object — corpus behaviour |
| face, lit crown | `#454B57` | apple-12's satin charcoal body on porcelain measures `#343233` against a `#CECECC` ground: **8.11:1**. This dial takes that relation |
| face, mid | `#2C313A` | " |
| face, shaded foot | `#161A20` | " |
| seat edge | `#0B0D11` | |
| bezel, lit | `#7C848F` | the raised rim's top-left, where the key lands |
| bezel, mid | `#3D434C` | |
| bezel, down-light | `#191D23` | |
| machined catch | `#CBD3DE` | the hairline the key leaves on a cut edge |
| dome bloom | `#8FA3BE` at 0.30 | apple-23's dial face "reads as domed glass with a soft top bloom" |
| graduation, major | `#FFF8EA` | cream, not white; value-separated as apple-23 does it |
| graduation, minor | `#CFC6B0` | |
| needle, lit | `#FFFCF4` | porcelain — the object carries the ground's own hue into its brightest element |
| needle, mid | `#EFE8D8` | |
| needle, shaded | `#B9B09A` | |
| needle edge | `#7C7361` | |
| bearing, lit | `#A9B2BE` | a small steel collar. Deliberately **not** the predecessor's 112px graphite hub with a 34px cream centre — better-loop shipped that same part, which is how the two became one icon |
| bearing, mid | `#6E7784` | |
| bearing, shaded | `#3A414A` | |
| bearing core | `#12151A` | |
| **accent** | `#DE5A28` | family band (report `#E46235`, whats-left `#DF612E`, deck-craft `#DE5A28`, better-loop `#DE5A28`), kin to Fledgeling `#C4622D`; inside apple-05's measured hue 9–32° at sat 0.81–0.85 |
| accent, lit | `#F2823C` | |
| accent, shaded | `#C9481C` | over 58° of arc, `#BC3A14` drags the band's open end towards brown; this keeps the saturation and loses only the last few points of value |
| accent, deep seat | `#BC3A14` | apple-05's darkest accent pixel is `#D22D1E` — still saturated, still warm |
| accent catch | `#F6D3AC` | apple-05's lightest accent pixel is `#EDD0A3`: the catch on a vermilion gel edge is warm cream, never white |

Light: one soft key at **118°**, `LIGHT_AXIS ≈ (-0.47, +0.88)` — the same lamp as
`better-loop` and `anvil-errand`, so a shelf of them is lit once. Sampled rather
than assumed: across apple-05, apple-10, apple-23 and apple-28 the brightest ground
pixel sits in the top-left quadrant in every one. Every face gradient hangs on one
shared user-space axis so the parts read as one object under one light rather than
as adjacent panels.

**What the corpus said about a dial on porcelain, and why this one ignored it.**
apple-23 (Safari) is the exact analogous case and it takes the cheaper route: a
saturated blue face measuring **2.01:1** at the crown to **2.80:1** at mid against
its `#F5F5F5` ground — *under* the rubric's own 3:1. apple-12 (Calculator) is the
corpus's dark-object-on-porcelain exemplar at **8.11:1**. The reference that looks
most like this icon is the one that would have kept it below the bar, which is the
skill's own rule that the rubric outranks the reference, met in the wild.

## Layer plan

| Layer | Contents |
|---|---|
| `bg` | cushion gradient, vignette, inner rim light on the squircle |
| `mid` | the instrument — the disc's and the boss's cast shadows, the raised rim, the domed face with its bloom and its down-light terminator, the graduations, the rim's lit catch and its continuous inner lip, the travel groove, the accept band with its cream catch and deep seat, the pawl wall and boss with their flank catches and the band's warm bounce, and the rim's seat edge re-run over the band |
| `fg` | the reading — the needle's cast shadow, its body and its dark edge, the bearing collar and its core |
| `highlight` | the key's catch along the needle's up-light flank, the bearing's specular crescent, the band's faint spill into the daylight outside the rim |

## Geometry, as named constants

`scale=0.96` · `r_face=282` · `bezel=36` · `r_tick_out=262` · `tick_a0=-172` ·
`tick_a1=-27` · `tick_step=10` · `band_a0=-21` · `band_a1=37` · `band_r_in=202` ·
`pawl_w=46` · `boss_w=96` · `boss_proud=22` · `needle_deg=8` · `needle_reach=252` ·
`needle_half=30` · `r_hub=58` · `cy=470`.

`scale` multiplies every radial dimension at once, which exists because the
object's diameter turned out to be the single lever on shelf distinctiveness and
hand-scaling fourteen constants to move it is how a sweep stops being
reproducible. A banner can be derived from these directly: `LIGHT_ANGLE_DEG` and
`LIGHT_AXIS` for the light, `ACCENT*` for the one warm hue, `band_a0` / `band_a1` /
`needle_deg` for the cell.

## Takes and scores

| Take | Engine | Score | Why |
|---|---|---|---|
| **a1** `icon.svg` | hand-authored layered SVG | **11 / 12** | ships; the only take that fixes the figure-ground without introducing a new defect |
| a2 `icon-takeA2-latched-bezel.svg` | hand-authored, pale face in a graphite ring | 8 / 12 | the pale face measures **1.00:1** against the tile, so the predecessor's defect survives inside the ring; at 16px it is a wall clock in `mac-doctor`'s neighbourhood |
| a3 `icon-takeA3-sunk-dial.svg` | hand-authored, tile-as-machine | 7 / 12 | the disc reads **1.18:1** against its housing and the two merge into one lump; 52.8% of the tile is dark mass, which is how it got the highest RMS on the sheet and why that number is a trap |
| C `icon-engineC-80617e.png` | GPT Image 2, corpus-referenced | 8 / 12 | the material target and it got the material right; baked its own mask and shadow, dial at ~78% of tile, one flat layer |
| B2 `icon-engineB2-arrow-7676a8.svg` | Arrow 1.1, the first call | 7 / 12 | read the target band as a **tachometer redline** — a ceiling not to be exceeded — which is the inverse of the meaning; baked its own corner mask at a smaller radius than the family's, so masking leaves a cream ring in the corners |
| B `icon-engineB-arrow-48d0c1.svg` | Arrow 1.1, the retry | 5 / 12 | put the band *inside* the tick ring as a floating arc, drew a full 360° clock ring, left a stray slab beside the hub, and baked a bevel frame with no cushion |
| prev `predecessor-dial.svg` | the icon replaced | 8 / 12 | fails #7 at 1.05:1, #4 because the argument dies by 32px, #11 on a stock speedometer read |

One standard on #10 across the whole sheet: **deducted wherever the six appearance
variants have not been rendered**, which is every take, because the browser engine
available accepts `Emulation.setEmulatedMedia` and leaves `prefers-color-scheme`
untouched. B and C would fail it outright anyway, having no layer plan.

**What the vector engine got wrong, twice.** Both Arrow takes put the accent band
*inside* the graduation ring as a floating arc rather than on the object's silhouette
edge, and at 16px both are a smear — independent confirmation of the placement rule
this master is built on. The first take went further and read the band as a
**tachometer redline**, a ceiling not to be exceeded, with the needle pressed against
it from below. That is the inverse of the skill: a redline is a limit you stay under,
a goal is a floor you reach and hold. No palette or geometry instruction in the brief
could have prevented it, and it is worth knowing that a model given "a band the
reading has to be inside, with a stop at one end" produced the opposite meaning on
both vector calls.

**Salvaged from the engines into the master:** the bezel's *continuous* inner-lip
hairline. The master had that catch on the lit arc only, so the rim read as a
highlight rather than as a turned part. Both engine takes independently drew the
rim as a complete pale annulus, and an unbroken circle at a sixth of the lit arc's
opacity was the whole fix. Two out-of-family engines agreeing on one construction
is the cheapest evidence this pipeline produces.

## Measurements

Contrast figures are RMS of **gamma-encoded** relative luminance on a 16px Lanczos
downsample over pixels with alpha > 0.5 — the definition `better-loop`'s notes
published, so these are comparable to the family figures there. It matters which:
linearising first shifts every number and a figure quoted without the definition is
not comparable.

| | value |
|---|---|
| the icon this replaces | 0.1142 (rank 35 of 38) |
| **shipped `icon-256.png`** | **0.2929 (rank 3 of 38)** |
| family median across 38 marketplace icons, measured 2026-08-19 | 0.2002 |
| `better-loop`, for the pair | 0.2331 |
| a2, the pale-face take | 0.2166 |
| a3, the sunk take | 0.3216 (52.8% dark mass) |

| Figure-ground, on the shipped 1024 render | ratio |
|---|---|
| graphite face vs the tile beside it | **12.34:1** (the predecessor: 1.05:1) |
| bezel vs the tile below it | 12.59:1 |
| lit bezel vs the tile beside it | 3.76:1 |
| target band vs the tile | 2.44:1 |
| target band vs the graphite face | 2.71:1 |
| the band's seat edge vs the tile | 3.36:1 |
| pawl boss vs the tile | 7.70:1 |
| needle vs the face it stands on | 7.19:1 |
| major graduation vs the face | 12.20:1 |
| minor graduation vs the face | 3.08:1 |
| bearing collar vs the face | 3.49:1 |

Grayscale spread on the shipped 256 render, alpha-masked: p2 0.117, p50 0.876,
p98 0.962 (the predecessor: 0.285 / 0.955 / 0.988). Object width 614px = 60.0% of
the tile on symmetric 205px side margins, with 147px above and 247px below; dark
mass 24.0% of the tile; corner alpha 0 at all four extremes. Structure gate: 24 paths, 12 gradients, 4 filters, 4 named
layers, 17.65KB — `fidelity.py structure` PASS. Warm accent 2.52% of the tile in one
contiguous piece (`better-loop`'s discipline figure is 2.41%).

## Shelf position

`better-loop` is **0.326** against this tile at 16px and is not in its top ten
neighbours. The pair the two icons formed is broken, which was the commission's hard
constraint. `mac-doctor` is 0.568 and `be-my-witness` 0.603, so the ring cluster is
clear too.

Nothing in the set is at or above `shelf_check.py`'s 0.80 flag any more — the whole
703-pair run is green, so no `DECIDED` entry was needed and nothing outside this
plugin was edited. But the margin is **0.003**, and getting there took two swept
constants rather than a design change.

**`scale`, the object's diameter**, against the worst 16px signature correlation
across the other 37 icons (RMS column measured at `cy=498`, before the vertical
sweep below):

| scale | object width | 16px RMS | worst pair |
|---|---|---|---|
| 0.84 | 52.3% | 0.2710 | 0.871 `proctor` |
| 0.88 | 55.1% | 0.2792 | 0.853 `proctor` |
| 0.92 | 57.8% | 0.2867 | 0.827 `proctor` |
| 0.94 | 58.6% | 0.2902 | 0.811 `proctor` |
| **0.96** | **60.2%** | **0.2935** | **0.810 `geminify`** |
| 0.98 | 60.9% | 0.2967 | 0.821 `tui-craft` |
| 1.00 | 62.5% | 0.2998 | 0.840 `mockup-fidelity` |

**No diameter clears the bar.** Shrinking the disc moves the flag from the dark-slab
cluster (`mockup-fidelity`, `tui-craft`) onto `proctor`'s dark box rather than
removing it. `0.96` is where the worst pair is least bad while sitting mid-grammar on
the 55–65% focal band.

**`cy`, the vertical position**, is the second lever and the one that cleared it:

| cy | worst pair |
|---|---|
| 526 | 0.830 `braindump` |
| 498 | 0.810 `geminify` |
| 486 | 0.805 `geminify` |
| 478 | 0.800 `geminify` |
| **470** | **0.797 `shipyard`** |
| 466 | 0.795 `shipyard` |

`470` is the first setting with real headroom, and it costs 0.0006 of 16px contrast.
The lift is 42px on a 1024 canvas, inside what the cast shadow's own reach below the
disc accounts for, so the composition reads no higher — checked at 384px against
cy 498 and cy 486 side by side before taking it.

Two things worth saying plainly. **This is a metric, not a verdict** — its own
docstring records about 50% precision on this set, and rendered at 16px the tiles it
flagged do not look alike: a dark disc against two warm capsules (`geminify`), a dark
terminal panel with a block cursor (`tui-craft`), a pale hull on water (`shipyard`).
And **the convergence is structural**: the house style fixes porcelain, one warm
accent and a volumetric object, so shape and accent placement are the only axes of
distinction left, and "a centred dark mass with one warm mark" is the shared
substrate. A sibling icon changing could put this back over the bar.

## What each round changed, and what it cost

Six rounds, all parameter or construction edits in `build_icon.py`, none of them
path surgery. Four of the six looked like colour problems and were not.

1. **A full 36-tick graduation ring with a pale needle near vertical.** It is a
   stopwatch at every size, whatever the palette does. Opening the scale to a
   190° sweep with a clear sector in the lower right is what makes it an
   instrument with a *travel direction*, and the direction is what the icon is
   about.
2. **The accept band as a 36px inlay in the bezel only.** At 16px that band is
   **0.56px thick** and simply is not there: the tile rendered as a plain dark
   disc and the whole device was gone exactly where it has to survive. Cutting the
   band down to `band_r_in=202` makes it 116px deep, 1.8px at 16px, and it reads.
   This is the single most important measurement in the commission and it is
   invisible at 1024.
3. **The stop as a vermilion radial sector.** A sector fans outward and it read as
   a folded ribbon tab. Rebuilt as a constant-width bar in graphite: parallel
   flanks are the whole difference between hardware and a bookmark, and graphite
   keeps the accent spent once while putting the tile's highest-contrast edge at
   the one place the boundary closes.
4. **That bar at 54px wide and 32px proud** then read as a stick poking out of the
   dial. Split into a 46px wall inside the face and a 96px × 22px boss on the rim:
   short and wide reads as cast into the body, long and narrow reads as bolted on.
5. **The rim's inner shadow on the up-light side.** It fought the face gradient —
   the gradient said the crown was lightest and the shadow said it was darkest, and
   two planes disagreeing about where the lamp is costs #8. Rebuilt as a
   down-light terminator on a dome, which is apple-23's construction.
6. **One flank catch drawn from the wall's foot to the boss's crown at the boss's
   half-width.** It floated clear of the wall for the whole inner half of its
   length and rendered at 256px as a stray pale rectangle beside the block. A
   flank belongs to one part.

Two more, on the accent:

- **The band ran to `ACCENT_DEEP` at its open end** and over 58° of arc the last
  third drifted towards brown. `#C9481C` keeps the saturation and loses only the
  last few points of value.
- **The rim's seat edge ran before the band**, so the band's outer arc touched
  porcelain directly at 2.44:1. Re-running the seat edge *after* the band gives it
  a 3.36:1 boundary instead. The corpus does the same thing: apple-12 puts its
  orange keys inside a charcoal body, so the edge the eye uses is the body's.

## Known liabilities

- **The band is under 3:1 on both sides** — 2.44:1 against the tile and 2.71:1
  against the graphite. A warm gel object squeezed between a Y 0.833 ground and a
  Y 0.084 body cannot clear 3:1 against both, and the corpus does not manage it
  either (apple-12's accent is 2.29:1 against its own body). It works by borrowing
  the rim's seat edge rather than by earning its own separation.
- **#10 is constructed, not tested.** Four named layers, identity carried by shape
  and value, the band at Y 0.311 between the face at 0.084 and the tile at 0.833 so
  a grayscale band is still a band. Dark, Clear and Tinted have not been rendered.
- **The device resolves at 32px, not at 16px.** At 16px what survives is a dark
  disc, a warm crown and a pale needle — a gauge with a marked target. The
  asymmetry that makes it *this* gauge needs the 32px source.
- **The minor graduations are 3.08:1 against the face** and dither to a grey fringe
  by 32px. Texture rather than identity, but the noisiest thing under magnification.
- **The shelf margin is 0.003.** No pair in the set is at or above the 0.80
  collision flag any more, and `better-loop` is 0.326, but the nearest neighbours
  sit at 0.797 `shipyard`, 0.794 `geminify` and 0.790 `proctor` — and clearing the
  bar took two swept constants rather than a design change (table above). A sibling
  icon changing could put it back over.
- **`banner.png` and `banner-src.html` still show the predecessor.** Built
  2026-08-13 against the pale dial and now wrong. Separately-owned banner debt, not
  fixed here.
- **No fidelity loop was run.** The raster take did not win the material read, and
  the two constructions it agreed on with the vector take were salvaged directly
  rather than converged upon. So there is no `loop-runs/` here and no panel verdict:
  the material claim rests on the corpus sampling and the sheet, not on a measured
  convergence.

## Rendering notes

`rsvg-convert` is the renderer for every export and for the audit sheet. Serving
`audit.html` on `localhost:9461` and reading it back through Obscura reports 45 of
45 images resolving and `display: flex` computing correctly on `.renders`, so this
sheet does not hit the column-collapse that `better-loop` and `deck-craft` both
recorded. Every judgement behind the scores was made on the PNG renders at 128 / 64
/ 48 / 32 / 16 and on a 38-icon shelf strip, not through the sheet.

The first Arrow call **reported a timeout to its caller and wrote its SVG anyway**.
It was found on disk afterwards and is scored on the sheet as take B2 rather than
deleted. Check the output directory before believing a reported timeout, and before
treating an engine as unavailable.

```bash
python3 build_icon.py                                        # writes icon.svg (a1)
python3 build_icon.py --variant a2 --out icon-takeA2-latched-bezel.svg
python3 build_icon.py --variant a3 --out icon-takeA3-sunk-dial.svg
rsvg-convert -w 1024 -h 1024 icon.svg -o icon.png
rsvg-convert -w 256  -h 256  icon.svg -o icon-256.png
rsvg-convert -w 128  -h 128  icon.svg -o icon-128.png
SK=../../create-mac-icon/skills/create-mac-icon/scripts
python3 $SK/audit_sheet.py render . --take a1=icon.svg:svg \
        --take a2=icon-takeA2-latched-bezel.svg:svg \
        --take a3=icon-takeA3-sunk-dial.svg:svg \
        --take B=icon-engineB-arrow-48d0c1.svg:svg \
        --take B2=icon-engineB2-arrow-7676a8.svg:svg \
        --take C=icon-engineC-80617e.png:raster-mask \
        --take prev=predecessor-dial.svg:svg
python3 $SK/audit_sheet.py check .        # must exit 0
python3 $SK/shelf_check.py ../../.. --plugin better-goal --flag 0.0
```

`predecessor-dial.svg` and `predecessor-gen.py` are the replaced icon and its
generator, kept for the sheet's before row. They were `icon-src.svg` and
`icon-gen.py`; renaming them out of the `icon*.svg` glob is required, because
`audit_sheet.py check` runs the structure gate on everything that glob catches and
treats it as a master. `predecessor-gen.py` also still carries the `loop_svg()`
provenance of `better-loop`'s own predecessor.
