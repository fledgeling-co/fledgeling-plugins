# better-loop icon — the stepped rail

Rebuilt 2026-08-18. The commission was not a polish pass. The shipped icon was
**the same object as `better-goal`**: same cream dial, same charcoal hub with a
cream centre, same needle, same vermilion dot at the top, separated only by a
grey sweep arc and the rim's tick pattern. Measured at 16px the pair were
0.1135 and 0.1142 RMS luminance contrast, and in a listing they sat next to each
other. `better-goal` keeps the dial, so the job was to find a different object
rather than to adjust this one.

The second defect was the accent. The predecessor's warm pixels were **0.75% of
the tile spread across a 123×98px bounding box** — rim ticks, a sweep, a top dot —
which is decoration rather than placement. The shipping take's are **2.41% inside
29×59px**: one piece, in one place, on the element that carries the meaning.

## Direction

**Direction 2, Tahoe gel-glass, sub-register (a): porcelain cushion carrying gel
objects**, hybridised with two devices from the bank — #17 tile-as-machine and
#18 edge-bleed physicality. Runner-up was Direction 8, Instrument Emblem, and it
was dropped for exactly the reason this commission exists: the app's own artifact
is a reading, and every instrument that displays a reading is a dial, a gauge or
a ring. `better-goal` owns the dial and `mac-doctor` owns the ring with one hot
arc.

Matching the fledgeling set: porcelain ground, one ember accent, the shared
superellipse from `plugins/create-mac-icon/assets/squircle-path.txt`, exports at
1024 (`icon.png`), 256 and 128.

## Device and signature move

**A machined graphite rail crosses the tile, dead level for most of its width,
and rises once.** It bleeds off both the left and right edges, because the state
it carries started before this window and continues after it — you watch a slice.
A **vermilion gel shim** is set in at the step, standing exactly the height of the
rise. A **steel follower saddle** is clipped over the raised run just past it: it
has already climbed.

The signature move is that **the accent is the height difference, not the
height**. The shim is a separate physical piece whose whole dimension is the
change, so what the tile hands the reader is the delta rather than the state —
which is the skill's own operating rule, performed instead of illustrated.
Everything else is quiet by construction: the long flat run carries a hairline
catch and nothing else, so the one place the profile moves is the one place there
is anything to look at.

**Deliberately not encoded: the doubling backoff.** Two and three decaying risers
were sketched. Each spends the family's one warm hue two or three times and the
tile becomes a bar chart at 48px. One event, one accent.

## Where the device came from

The first pick was a **strip-chart recorder** — a charcoal body, a porcelain strip
feeding out of a slot, a dead-flat thin low-contrast trace taking one thick
vermilion step. It was put to `claude-fable-5` at high effort with the taken-device
list and the 16px constraint, and that lane rejected it on a mechanical ground
worth keeping: **a trace that is low-contrast by design is the first thing to die
at 16px, so the icon's whole idea disappears exactly where it has to survive.**
Its counter-proposal was to carry the flat-run-and-one-step in the *silhouette
boundary* instead of in a drawn line, and its acid test generalises past this
commission: *does the accent sit on the silhouette edge, or as linework floating
in a light field?* Only the first survives. The lane also ranked a punched-tape
reader last, on the grounds that repeated small holes dither to grey at 16px. That
call was taken.

## Palette

Every value below was sampled off the corpus or off the family before the first
line of the build script, not reasoned about.

| Role | Hex | Provenance |
|---|---|---|
| cushion, lit | `#FCFAF4` | family: deck-craft, create-test-suite, whats-left |
| cushion, mid | `#F3EDE1` | " |
| cushion, corners | `#DED5C2` | " |
| inner rim light | `#FFFDF8` | the cushion tell every Tahoe tile carries |
| vignette | `#8B7F66` at 0.24 | " |
| cast shadow | `#3B3327` | warm, even under a cool object — corpus behaviour |
| rail, lit | `#5E6570` | apple-10's dark mass on porcelain: hue 228–233, sat 0.20 |
| rail, mid | `#3A4048` | " |
| rail, base | `#1C2027` | " |
| rail seat edge | `#111419` | |
| tread, lit | `#7A828E` | the second face the key reaches |
| tread, shaded | `#4A515B` | |
| key hairline | `#CBD3DE` | |
| **accent** | `#DE5A28` | family band (report `#E46235`, whats-left `#DF612E`, deck-craft `#DE5A28`), kin to Fledgeling `#C4622D`; inside apple-05's measured hue 9–32° at sat 0.81–0.85 |
| accent, lit | `#F2823C` | |
| accent, shaded | `#BC3A14` | apple-05's darkest accent pixel is `#D22D1E` — still saturated, still warm |
| accent catch | `#F6D3AC` | apple-05's lightest accent pixel is `#EDD0A3`: the catch on a vermilion gel edge is warm cream, never white |
| steel, lit | `#AEB7C3` | one value band above the rail, well below the cushion |
| steel, mid | `#828C9B` | |
| steel, shaded | `#565E6B` | |
| steel edge | `#262B33` | |

Light: one soft key at **118°**, `LIGHT_AXIS ≈ (-0.47, +0.88)`. Sampled rather
than assumed — in apple-05, apple-10 and apple-28 the brightest ground pixel sits
at (0.02–0.05, 0.00), the top-left corner, in every one of them.

Extrusion: `DEPTH = (22, -32)`. Every horizontal surface gets a second, brighter
face, and every face gradient hangs on one shared user-space axis so the faces
read as one object under one light rather than as adjacent panels.

## Layer plan

| Layer | Contents |
|---|---|
| `bg` | cushion gradient, vignette, inner rim light |
| `mid` | the reading — the band's cast shadow, both treads, the front face on one axis, the shim with its top face and cream catch, the shim's shadow along the raised run, the inside-corner occlusion, the key's hairline, the warm bounce |
| `fg` | the watcher — the saddle's cast shadow, its top face and far edge, body, sheen, shadowed lip, bearing line |
| `highlight` | the key's catch on the saddle's lit edges, the wrap arc across its crown, the shim's kiss on the saddle's up-light edge, the shim's faint glow into the daylight above the step |

## Geometry, as named constants

`thick=124` · `low_top=606` · `step_x=552` · `step_h=200` · `shim_w=88` ·
`shim_proud=8` · `shim_over=12` · `yoke_w=142` · `yoke_gap=74` · `yoke_arm=68` ·
`yoke_back=34` · `yoke_corner=26` · `lift=-70` · `bleed=64`.

`step_h` was swept at 178 / 212 / 240 against the 32px render. Under about 190 the
two runs merge into one thick band with a notch; over about 230 they read as two
separate bars, and `armada-sync` already owns a stack of those.

A banner can be derived from these directly: `LIGHT_ANGLE_DEG` and `LIGHT_AXIS`
for the light, `DEPTH` for the extrusion, `step_x` / `step_h` / `shim_w` for the
cell, `ACCENT*` for the one warm hue.

## Takes and scores

| Take | Engine | Score | Why |
|---|---|---|---|
| **A** `icon.svg` | hand-authored layered SVG | **11 / 12** | ships; the only take where the step survives 16px |
| C1 `icon-engineC-2e7a75.png` | GPT Image 2, corpus-referenced | 7 / 12 | the material target; the step is a fifth of the rail's thickness and gone by 48px, the lower half of the tile is dead, flat raster fails #10 |
| C2 `icon-engineC-cc2708-2.png` | GPT Image 2, second take | 6 / 12 | drew two rises, so the accent no longer marks the only event |
| B `icon-engineB-arrow-bf638b.svg` | Arrow 1.1 vector | 3 / 12 | no ground, so it floats in the Dock; read the shim as a slab lying on the raised run, which inverts the one idea in the brief |
| prev `predecessor-dial.svg` | the icon replaced | 8 / 12 | fails #6 on the spread accent and #11 because its one nameable device is `better-goal`'s |

Salvaged from the rasters into the master: the **wrapped crown** on the follower —
both takes drew it as a clip turned over the rail rather than as a block cut flat,
and a generous top radius with one arc catch reads as machined where a boxy block
read as a tray. Also the reading that a **machined top chamfer running the full
length** is what makes graphite look cut rather than drawn; the master already had
it as the extruded tread, which is why that construction stayed.

The 12-point rubric never asks whether an icon differs from its siblings. That is
how the predecessor scored 8/12 and still had to be replaced, and it is worth
saying out loud in a library that generates a family.

## Measurements

Contrast figures are RMS of **gamma-encoded** relative luminance on a 16px
downsample over pixels with alpha > 0.5 — the metric the family's earlier
commissions used. It matters which: linearising first gives 0.2331 → 0.2840 and
shifts the family median from 0.1805 to 0.2380, so a number quoted without the
definition is not comparable. `deck-craft`'s recorded 0.174 reproduces exactly
under the gamma-encoded form.

| | value |
|---|---|
| the icon this replaces | 0.1135 |
| `better-goal`, for the pair | 0.1142 |
| **shipped `icon-256.png`** | **0.2331** |
| direct 16px render of `icon.svg` | 0.2329 |
| family median across 36 marketplace icons | 0.1805 |
| rank in that population | 10 of 36 |

| Figure-ground, on the authored hexes | ratio |
|---|---|
| graphite `#3A4048` vs cushion `#F3EDE1` | 8.98:1 |
| graphite `#1C2027` vs cushion `#DED5C2` | 11.21:1 |
| shim `#DE5A28` vs graphite `#3A4048` | 2.79:1 |
| shim `#DE5A28` vs cushion `#F3EDE1` | 3.22:1 |
| steel `#828C9B` vs graphite `#3A4048` | 3.08:1 |
| steel `#828C9B` vs cushion `#F3EDE1` | 2.92:1 |

Grayscale spread on the shipped 256 render, alpha-masked: p2 0.213, p50 0.896,
p98 0.973. Structure gate: 24 paths, 10 gradients, 4 filters, 4 named layers,
15.0KB — `fidelity.py structure` PASS.

## What each round changed, and what it cost

Five rounds, all of them parameter or construction edits in `build_icon.py`, none
of them path surgery. Recorded because four of the five were failures of a kind
that looks like a colour problem and is not.

1. **A solid stepped plinth, base at a common line.** Its raised half is a 300px
   block of graphite and the tile reads as a floor with a step in it. Rebuilt as
   one constant-section band, which also drops the dark area from 22% of the tile
   to 15%.
2. **Two graphite roller pins under the follower, at 0.26 and 0.74 of its width.**
   They read as a pair of eyes at every size down to 32px; the follower stopped
   being hardware and became a face. Replaced with a sole, then with the wrap.
3. **A yoke the rail passes through, open on its up-light side.** Pale jaws
   interlocking with a dark band is a figure-ground ambiguity, and what it
   resolves to is a belt buckle.
4. **A porcelain follower.** This is a measurement error rather than a taste one:
   a porcelain object on a porcelain ground runs about 1.15:1, so the part of the
   saddle standing above the rail simply was not there. Steel reads against both
   the rail and the cushion, and it keeps the palette to one cool hue family plus
   the one warm accent.
5. **Three overlays stacked on the follower** — a dark lip, a graphite bearing pad
   and the shim's warm spill at 42px wide and 0.22 alpha. Together they read as
   one dirty stripe across the middle of the part, with every hex still correct on
   its own. The accent is 74px away from that part, so what reaches it is an edge
   and not a wash.

Two more, on the rail itself:

- **The seat edge ran after the shim**, so the step's own vertical edge drew a
  dark seam down the shim's up-light side, which reads at 256px as a gap between
  the two. The edge now goes on with the front face, before the shim.
- **The quiet run's tread ran to the shim's far edge**, and its foreshortened far
  corner poked out past the shim as a grey tab, reading as a chipped step. It now
  stops where the shim begins, because behind the shim there is no visible tread.

## Known liabilities

- The shim reads **2.79:1 against the graphite** on its down-light side, under the
  3:1 bar. It survives because its up-light edge sits against porcelain at
  3.22:1, which is where the eye picks it up, but a deeper graphite or a wider
  cream catch would fix it properly rather than by luck.
- The steel saddle is **2.92:1 against the cushion**, so the part of it standing
  above the rail is the weakest element in the tile and the first thing to go at
  32px. It is also the least legible object at 48px.
- The object **bleeds the full tile width** where the composition guidance asks
  for a focal at 55–65%. That is deliberate — the edge-bleed device is carrying
  "the state continues past the window" — but it has not been read in a Dock full
  of inset siblings, only in a seven-icon shelf strip.
- **#10 is satisfied by construction, not by test.** Four named layers, identity
  carried by profile rather than hue, so a grayscale step is still a step. Dark,
  Clear and Tinted have not been rendered.
- The **large empty upper-left quadrant** is load-bearing for the "mostly silent"
  reading and is also the thing most likely to read as an unfinished tile to
  someone who does not know the subject.
- The **backoff is absent**, so one of the skill's three ideas is not in the icon
  at all. Stated rather than hidden.
- **`banner.png` and `banner-src.html` still show the dial.** They were built
  2026-08-13 against the predecessor and are now wrong. That is separately-owned
  banner debt, not fixed here.

## Rendering notes

`rsvg-convert` is the renderer for every export and for the audit sheet. The
sheet's images all resolve over http — 35 of 35, none broken, checked by reading
back `naturalWidth` — but the Obscura engine does not implement flex, so serving
`audit.html` there lays the `.renders` row out as a column and each take reads as
one tall strip. `deck-craft`'s commission recorded the same thing. Every judgement
behind the scores was made on the PNG renders at 128 / 64 / 48 / 32 / 16 and on a
seven-icon shelf strip beside `better-goal`, `armada-sync`, `discipline`,
`improve-skill`, `mac-doctor` and `deck-craft`, not through the sheet.

```bash
python3 build_icon.py                     # writes icon.svg
rsvg-convert -w 1024 -h 1024 icon.svg -o icon.png
rsvg-convert -w 256  -h 256  icon.svg -o icon-256.png
rsvg-convert -w 128  -h 128  icon.svg -o icon-128.png
SK=../../create-mac-icon/skills/create-mac-icon/scripts
python3 $SK/audit_sheet.py render . --take A=icon.svg:svg \
        --take B=icon-engineB-arrow-bf638b.svg:svg \
        --take C1=icon-engineC-2e7a75.png:raster-mask \
        --take C2=icon-engineC-cc2708-2.png:raster-mask \
        --take prev=predecessor-dial.svg:svg
python3 $SK/audit_sheet.py check .        # must exit 0
```

`predecessor-dial.svg` and `predecessor-gen.py` are the replaced icon and its
generator, kept for the sheet's before row. They were `icon-src.svg` and
`icon-gen.py`; renaming them out of the `icon*.svg` glob is required, because
`audit_sheet.py check` runs the structure gate on everything that glob catches and
the predecessor has no layer plan.
