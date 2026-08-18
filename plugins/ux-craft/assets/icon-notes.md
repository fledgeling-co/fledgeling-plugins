# Icon notes — `ux-craft`

Direction 2 (Tahoe gel-glass), sub-register (a): a porcelain cushion carrying gel
objects. Same register as `create-test-suite`, `deck-craft`, `mac-craft`,
`whats-left` and `report`, which it sits beside in the marketplace lineup.

Replaces the 2026-08-18 template icon — a 3×2 panel of pale porcelain keys with
one vermilion key and one cell cut through as a void. That one had two problems
and only one of them was visual: it measured **0.086** RMS luminance contrast at
16px, about half the family median, so on a shelf it was a white square with a
fleck; and at 256px it was the same object as `create-test-suite`, which is also
a panel of rounded tiles with exactly one vermilion tile. Its palette was
inherited rather than mined — `#E9562A` on `#FDFCFA`/`#E7E4DC`/`#D8D3C9`, shared
verbatim with five siblings.

## The idea

**The Spacing Circle.** Two touch targets sit on a porcelain bench, and each one
wears its reach envelope as a low puck of graphite gel — the region a fingertip
claims, rather than the rectangle a designer drew. At the centre of each puck a
frosted porcelain key stands proud: the control you can actually see. The two
envelopes cross, which is precisely what WCAG 2.5.8's Spacing exception forbids,
and the crossing is the only lit thing in the tile — where two reaches double,
the gate fires and the doubled gel glows vermilion.

The signature move is that **the accent exists only in the crossing.** It is
painted on neither object; it is a property of their relationship. Move either
control forty units apart and the tile goes dark. That is the skill's own gate
drawn as light — only exit 0 is a pass — rather than as a badge stuck on a thing.

Provenance, all of it from the skill's own text rather than from "UX":

- The envelopes are sized to the **two figures that disagreed**, at their true
  44:24 ratio: 44 (WCAG 2.5.8 AAA, and Apple's 44 pt) against 24 (WCAG 2.5.8 AA
  minimum, the only target-size number the skill permits calling a WCAG failure).
  Three such figures had disagreed across three of its own files at the exact
  point the accessibility claim was made; that incident is why it now carries a
  table where every number names its standard, its level and its unit.
- The crossing is the **normative** form of the spacing rule as the skill states
  it: a 24px-diameter circle centred on a target must overlap no other target's
  circle. Not a flat 8px gap.
- Device #21 from the bank (overlap-as-identity: two translucent primitives whose
  blend zone is the mark) crossed with #22 (emissive interior under glass, the
  grammar's one sanctioned second light source).

Runner-up directions, recorded rather than built:

- **The Thumb's Measure** — built anyway as a second hand-authored take
  (`build_alt_thumb.py`, 8/12) because the brief named it: the human is the unit,
  a graphite thumb cut by the bottom edge landing on a key plainly narrower than
  its own pad. It reads at every size and it is stock tap-target art; the size
  comparison it states literally, the shipping take states as geometry.
- **The three nested measure squares** (24/44/48, the AA one in ember) — killed
  on measurement at the flat-mock stage: 0.125 RMS at 16px, and at 32px it
  collapses into a focus ring.
- **The stepped clearance boss** — a fused coaxial or square boss whose three
  risers are the three standards, with the control as a chip on its crown. This
  was what two out-of-family lanes independently recommended (below). Rejected on
  family adjacency: `anvil-errand` already owns an extruded machined graphite
  solid with a hot element on its top face, and at 96px the two would read as
  siblings from one toolbox.

## The referral, and the collision it did not catch

The device was a genuinely open fork, so it went out to other model families with
the taken-devices list, the subject material and three measured mocks. **Fable
(claude, high)** and **gemini-3.7-flash-high** both answered and converged on the
same shape — the clearance envelope as a solid mass with the small control inside
it — and both named the same failure mode: at 16px it collapses to dark-circle-
plus-hot-dot, which is a record button, and the arithmetic is private. **Codex
(gpt-5.6-sol) was usage-capped** until 2026-08-20 and returned nothing; the
**grok-4.6** lane was cut off mid-run by my own 900-second alarm. Their
suggestions worth keeping on record: a go/no-go limit gauge ("only exit 0 is a
pass" as a physical fact), a shear-gate held open by a drop pin, and the empty
socket that refuses.

What no lane could catch, because it needs the pixels: **the first framing of
this device was two overlapping shapes with a hot seam, and that is taken twice
over.** Rendered at 96px between its siblings, it sat exactly between `geminify`
(two overlapping translucent capsules with a warm blend zone) and
`should-compact` (two dark slabs squeezing a vermilion seam). The rescue was
material rather than conceptual: foreshortening the envelopes into pucks with
edge bands, contact shadows and a seat moved them out of both neighbourhoods,
because neither sibling renders a physical object standing on the tile. Read the
shelf strip before believing a device is free; the collision exists only there.

## Palette, sampled rather than guessed

Read out of the corpus captures and the sibling PNGs before anything was authored.

| | value | source |
|---|---|---|
| cushion | `#FDFBF6` → `#F4EFE3` → `#E1D9C8` | apple-28 (Photos) measures V 0.999 under the key, 0.960 mid, 0.923 at the far edge — near-neutral warm white falling about 0.08 across the tile |
| inner rim | `#FFFEFA` at 0.72 | every Tahoe capture carries one; a flat ground is previous-era |
| vignette | `#8B7F66` at 0.22 | apple-23 / apple-28, both porcelain register |
| gel, top faces | `#98917F` → `#4A443A` → `#1E1B16` | apple-12 (Calculator) satin charcoal body, normalised to this brighter tile: lit shoulder V 0.36, face V 0.23, far rim V 0.14 |
| gel, edge bands | `#514A3E` → `#302B23` → `#1B1813` | a step darker than the face it belongs to |
| rim light | `#BDB1A0` | apple-12's body rim reads about 2× its own face |
| porcelain bounce | `#D8CBB2` at 0.14 → 0.38 | apple-12's bottom edge reads 1.7× its middle — the tile throws light back up |
| frosted keys | `#FFFEFB` → `#E7DFD0`, edge `#B0A691`, at 0.92 alpha | apple-12's white gel keys; white is a material, so the gel bleeds through |
| accent | `#FFC08C` → `#F5793C` → `#EA4A24` → `#4E1605` | luminance from the family (`#E9562A` sits at HSL L 0.539; `#EA4A24` at 0.529), hue from the subject at H 11.5 — redder than mac-craft's 18.8 and deck-craft's 16.5 |
| shadow | `#3A3126` | warm, never blue — the corpus's darkest gel pixels are warm at matching luminance |

## Layer plan

Four named `<g>` groups, mapping 1:1 onto Icon Composer layers:

- `bg` — cushion radial and edge vignette.
- `mid` — both pucks' contact shadows (a wide soft one and a tight one, each
  offset along the light axis), then the 44 envelope complete: edge band,
  porcelain bounce along the far band, top face, occlusion crescent inside the
  far rim, one soft catch on the lit shoulder, rim light on the lit arc, and its
  frosted key with its own band and micro shadow.
- `fg` — the 24 envelope, nearer the viewer, same construction; the warm kiss on
  the flanks that face the crossing; then the crossing itself — the light showing
  in the band it passes through, the doubled gel, the trapped light, its lit edge.
- `highlight` — the bloom, clipped to each puck so it lights the gel that traps
  it rather than painting over an occluder; the faint halo that escapes onto the
  porcelain; the tile's inner rim.

Named constants a banner can be derived from: `LIGHT_ANGLE_DEG` (118°, one key,
every rim/cast/occlusion/bounce derived from it), `ENVELOPE_AAA` / `ENVELOPE_AA`
with `R_BIG` / `R_SMALL`, `SQUASH` and `THICK` (the foreshortening and the edge
band), `OFFSET_X` / `OFFSET_Y` (which set how much of the crossing there is),
`KEY_FRAC` / `KEY_THICK`, and `ACCENT_CORE` / `ACCENT_HI` / `ACCENT` /
`ACCENT_DEEP`.

## Four engines

| | take | score | outcome |
|---|---|---|---|
| **A** | `icon.svg` (+ `build_icon.py`) | **11 / 12** | **ships.** Four named layers, 34 paths, 25.6 KB, `fidelity.py structure` PASS. |
| **A2** | `icon-engineA2-thumb.svg` (+ `build_alt_thumb.py`) | 8 / 12 | The thumb composition, hand-authored. Clears 1–4 and measures 0.243, so it lost on craft and ownability: one across-the-digit ramp gives the pad no form, the nail plate reads as a patch, and a finger on a button is failure mode #1. |
| **B** | `icon-engineB-arrow-e6712a.svg` | 5 / 12 | Arrow 1.1, briefed with the spec verbatim. No ground field at all, bakes its own circular shadow, grey keys on grey circles at 0.194, and it discarded the 44:24 ratio for two near-equal circles — which turns the subject into goggles. Nothing salvaged. |
| **C1** | `icon-engineC-crossing-04a62e.png` | 9 / 12 | GPT Image 2 with three corpus references. **Won the material and composition read and is why A was rebuilt twice.** Fails #1 as delivered (opaque corners, masked for the sheet), #2 (85% of the tile width) and #10 by construction. Most contrasty take at 0.299. |
| **C2** | `icon-engineC-thumb-6a977a.png` | 7 / 12 | The thumb composition rendered by the material engine, and the best-looking thumb of the four — which settled that composition rather than rescuing it. Its accent is a slab of flat orange at a tenth of the tile, and it touches the bottom edge with no safe zone. |

`audit.html` carries the scored contact sheet with all five takes and every
liability; `audit_sheet.py check` passes on it (35 local image references, all
resolve).

## What Engine C caught that two hand-authored rounds did not

Both hand-authored attempts before the raster came back were *plan-view* circles
with radial gradients, and both failed the same way at 1024: **they render as ball
bearings, and the crossing reads as a leaf stuck on top of them.** Two material
rounds — flattening the value range, killing the sheen, containing the lens light
— improved the surface and did not touch the problem, which is the tell that the
fault was in the construction rather than in the parameters.

The raster take solved it with two moves, both now in `material-recipes.md`:

1. **A reach zone is a foreshortened puck with an edge band, not a circle.** An
   ellipse at 0.66 squash, its outline dropped by a 32-unit thickness to give a
   visible band, plus a seat and a contact shadow. The band is what makes it an
   object standing on the bench; without it the same ellipse is a hole or a decal.
2. **One user-space ramp across both pucks, not one radial per puck.** The faces
   then read as two objects under one light. A per-object radial makes each one
   its own little sun, which is exactly the sphere read.

## What measurement caught that the eye did not

1. **The crossing's own gradient was two-thirds dark.** With the core radius set
   from the lens's half-*width* and a 1.9× vertical stretch, the trapped light
   fell to `ACCENT_DEEP` well inside the lens, so at 1024 the accent looked like a
   half-sized blob clipped by an invisible edge. Sizing the gradient off the
   lens's half-*height* and squeezing it in x by `lens_w / lens_h` fills the
   crossing properly. The lens's aspect is 1:2.4 — a radial gradient on it needs
   the anisotropy written down, not eyeballed.
2. **The accent is weaker than it looks, and the grayscale render is where you
   see it.** Dilated-ring: the gel pucks read **6.45:1** against their surround,
   but the crossing reads only **1.45:1** against the gel it sits in, because its
   own boundary is near-black by construction. In grayscale the crossing survives
   as a visibly lighter lens, so #7 holds — but part of the signature is carried
   by hue, which is what makes #10 an honest fail rather than a formality.
3. **Foreshortening costs contrast, and the fix is footprint.** Flattening the
   pucks took the 16px RMS from 0.282 (plan-view circles) to 0.236, because the
   dark mass fell from 30% of the tile to 17%. A 6% scale-up recovered it to
   0.244 at 67% tile width; 12% would have given 0.255 at 73%, which crowds the
   safe zone. The trade was swept rather than argued.

## 16px contrast

Alpha-masked RMS of Rec.709 luminance on a 16px Lanczos downsample, the family
metric:

| | value |
|---|---|
| the icon this replaces | 0.086 |
| shipped `icon-256.png` | **0.243** |
| direct 16px render of `icon.svg` | 0.244 |
| family median across 36 plugin icons | 0.174 |
| family range | 0.084 (this icon, before) → 0.363 (`agent-voice`) |

## Fidelity

No loop rounds were run. Engine C1 won the material read and its two
constructions were ported by hand instead, which is the cheaper half of the same
job; what remains is a measured gap rather than an unexamined one — C1 is more
contrasty at 16px (0.299 against 0.243) and its gel faces carry an inner top glow
this master does not. Converging on it would also drag in three things it gets
wrong: an 85%-wide object with no safe zone, opaque square corners, and a flat
construction that fails #10 by definition. The rubric outranks the gate.

## Known liabilities

- **#10 is satisfied by construction and never tested.** Four named layers,
  identity in shape and value — but Dark, Clear and Tinted were not rendered, and
  the crossing holds only 1.45:1 against the gel in grayscale.
- **The silhouette names the overlap, not the subject.** Filled black it is two
  crossing discs, which is nameable and is the point of the device; but nobody
  reads "targets and their reach" from it. The meaning arrives at 48px and up,
  with the keys.
- **The focal is 67% of the tile width** against the grammar's 55–65%. Deliberate:
  the object is flat (46% tall), so its area is modest and the width is what buys
  the 16px mass.
- **Measurably flatter than the raster at every size.** The gel faces are one
  ramp plus one soft catch; an inner top glow and a stronger ambient-occlusion
  crescent at the crossing would close some of it without touching geometry.
- **Two dark pucks is one step from a pebble pair.** At 16px the crossing is doing
  all the differentiating work, and the small puck's key is effectively gone.
- **`design-craft` is being rebuilt in parallel.** This icon was made distinct on
  its own terms — a physical object standing on the bench, an accent that exists
  only as a relationship — but the standing pair has not been read side by side
  after both land.

## Rendering notes

The icon renders through `rsvg-convert`. The audit sheet's own images could not
be verified through Obscura: the MCP route refuses `127.0.0.1` as a private
address, and over both `file://` and a served `http://` the engine laid the sheet
out correctly while painting none of the local PNGs — empty boxes with alt text
over `file://`, nothing at all over `http://`. The sheet's 35 image references
were verified by `audit_sheet.py check` resolving every one on disk, and the
judgements behind the scores were made on the PNG renders themselves at 128 / 64
/ 48 / 32 / 16.

The banner is still owed (dated debt, 2026-08-18) and a separate pass owns it.
The named constants above are what it should be derived from.

```bash
python3 build_icon.py                       # writes icon.svg
python3 build_alt_thumb.py                  # writes the second hand-authored take
for s in 1024 256 128; do rsvg-convert -w $s -h $s icon.svg \
  -o $([ $s = 1024 ] && echo icon.png || echo icon-$s.png); done
SK=../../create-mac-icon/skills/create-mac-icon/scripts
python3 $SK/audit_sheet.py render . --take engineA=icon.svg \
  --take engineA2=icon-engineA2-thumb.svg \
  --take engineB=icon-engineB-arrow-e6712a.svg \
  --take engineC1=icon-engineC-crossing-04a62e.png:raster-mask \
  --take engineC2=icon-engineC-thumb-6a977a.png:raster-mask
python3 $SK/audit_sheet.py check .          # must exit 0
```
