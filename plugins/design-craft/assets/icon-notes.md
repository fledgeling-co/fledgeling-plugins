# Icon notes — `design-craft`

Direction 2 (Tahoe gel-glass), sub-register (a): a porcelain cushion carrying gel
objects. Same register as `deck-craft`, `create-test-suite`, `whats-left`,
`proctor` and `report`, which it sits beside in the marketplace lineup.

Replaces the 2026-08-18 template icon — a light bezelled landscape frame holding
five pale vertical bars with one vermilion, 0.174 RMS luminance contrast at 16px.
That number sat on the family median and flattered the tile: at 16px it read as a
grey barcode rather than as an object, and the device was category clip-art for
"design" that said nothing about what the skill does. It also spent the accent on
one bar in five, when the house rule is one warm accent on the focal element, and
it collided with `deck-craft`, which was the same light frame holding pale panels.

## The idea

**The sample fan.** Three material leaves are pinned on one rivet and splayed.
Two of them cluster 19° apart: a matte warm-slate sample and a frosted cream one,
which are the two looks this skill's own `ai-slop-check.md` §9 names as the
category's defaults — the dark moody slab every dev-tool brief lands on, and the
blank cream minimal that is its predictable opposite. The third leaf stands 40°
clear of both and is the only one finished: poured vermilion gel with a specular
sliver, a rim catch and its own contact shadow.

The signature move is the **gap**. A rut and its predictable opposite are the same
neighbourhood, so the rejects sit next to each other; the committed direction is
the one that leaves the neighbourhood. The ratio between the two gaps — 19° inside
the cluster, 40° out to the commitment — is the argument, and it is a hole in the
silhouette rather than a difference in colour, so it survives to 16px.

The second claim is carried by material rather than geometry: **only the committed
leaf is finished.** The rejects keep their gradients, seat edges, rim and cast
shadows, so they are real objects, but they have no specular and no bloom. Three
material families explored, one taken to a finish — which is what the skill does
before it generates anything, performed rather than illustrated.

Device #16 from the bank (the icon performs the verb) crossed with #21
(overlap-as-identity: the frosted leaf's translucency is only visible because the
slate leaf lies behind it). Runner-up direction, recorded rather than built: **the
tri-state chip** — three sample chips where the third is a void showing the
cushion through it, drawing the gate's UNMEASURABLE verdict. It is the honest
heart of the skill and the least drawable thing in it: a hole reads as a hole at
128px and as nothing at 16px.

### Separation from `design-review`

The pair is deliberate — design-craft authors, design-review judges — so they have
to stay separable at 32px. design-review is orthogonal: cool-tinted glass panels
in the upper left with a vermilion crosshair reticle badged over them, an
inspection instrument on a cool ground. This one has no frame, no panel and no
reticle: a radial splay of capsule paddles on a warm porcelain ground, pinned at
one rivet, whose accent is a whole object rather than a badge. At 32px one is a
rectangle-in-a-rectangle with a cross on it and the other is a three-lobed fan.
The register is warm here and cool there (`#FDFAF4` against design-review's
`#FAFCFD`).

## Palette, sampled rather than guessed

Read out of the corpus captures and the sibling PNGs before anything was authored.

| | value | source |
|---|---|---|
| cushion | `#FDFAF4` → `#F0EADD` → `#DCD3C0` | deck-craft `#FAF7F0`→`#EDE7DA`, proctor `#FBF9F3`→`#EFEADF`, whats-left `#FCFAF6`→`#EFEBE0` |
| inner rim | `#FFFDF8` | every Tahoe capture carries one; a flat ground is previous-era |
| vignette | `#8B7F66` at 0.24 | corpus apple-23 / apple-26 / apple-28 / apple-31, all porcelain register |
| slate (the rut) | `#5E5339` → `#28200E`, edge `#120E06` | warm graphite, deliberately browner than `improve-skill`'s charcoal whetstone and `anvil-errand`'s cool graphite, the two siblings close enough to collide |
| cream (its opposite) | `#FCF7EB` → `#CEBF9C`, edge `#9C8E70` | a warm off-white, not a white: engine C2 proved a true white frost dissolves at 32px |
| accent | `#E5793C` → `#CE4A18` → `#93300E` | proctor `#E35721`, clarify `#DF6435`, report `#D65B30`, mockup-fidelity `#BA3D10` — hue 16-21°, sat 0.67-0.85; kin to Fledgeling `#C4622D` |
| accent rim | `#FFDCC0` | apple-31's darkest gel pixel is `#E64A5E`, the accent's own hue deepened, never a grey |
| shadow | `#3B3327` | warm — the corpus's shaded faces are warm at matching luminance |

Light axis: **112°**, one soft key from above and slightly left. Sampled, not
picked: across apple-23 / 26 / 28 / 31 the brightest 0.5% of the tile sits at
x = 0.43-0.50, y = 0.01-0.03 of the tile box.

## Layer plan

Four named `<g>` groups, mapping 1:1 onto Icon Composer layers:

- `bg` — cushion radial, edge vignette, inner rim light on the family squircle.
- `mid` — the two rejects, the rut first: cast shadow, the ambient-occlusion
  crescent it drops on whatever it stands on, the masked side face, the gel face
  ramped on the shared light axis, sheen, seat edge, rim catch.
- `fg` — the committed leaf, same construction plus its specular slab, then the
  rivet, which is drawn last because it goes through the stack rather than under it.
- `highlight` — the warm kiss the gel leaf throws onto the frosted face beside it,
  masked out of the gel leaf itself.

Named constants a banner can be derived from: `LIGHT_ANGLE_DEG` / `LIGHT_AXIS`
(112°, one key light, every cast, rim and ramp derived from it), `SHADE_DIR`,
`Spec.leaf_w` / `leaf_len` / `top_r` / `base_taper` (the cell), `Spec.rut_deg` /
`opposite_deg` / `committed_deg` (the splay, with `placement()` re-centring the
fan whenever an angle moves), and `ACCENT` / `ACCENT_HI` / `ACCENT_DEEP`.

## Three engines

| | take | score | outcome |
|---|---|---|---|
| **A** | `icon.svg` (+ `build_icon.py`) | **11 / 12** | **ships.** Four named layers, 33 paths, 18.2 KB, `fidelity.py structure` PASS. Fails #7 on the cream leaf alone. |
| **C1** | `icon-engineC-5db443.png` | 10 / 12 | GPT Image 2 with four corpus references. **Won the material and composition read**; its capsule ends and tapered rivet tab were ported into A. Cannot ship: bakes its own tile, bezel and drop shadow (#1) and is flat (#10). |
| **C2** | `icon-engineC-3a4e16-2.png` | 8 / 12 | Second raster take. Frost at ~1.05:1 on a pure-white ground, gone by 32px; accent drifted to pink-red. Kept as the counter-example that set the cream leaf's value. |
| **B2** | `icon-engineB-arrow-921e96.svg` | 4 / 12 | Arrow 1.1, second take. Confirms the device reads with no material at all, and nothing else: baked corner radius, no light model, cool grey-blue ground, pale leaf out of the silhouette. Nothing salvaged. |
| **B1** | `icon-engineB-arrow-920b9d.svg` | 3 / 12 | Arrow 1.1, first take — its call reported a timeout and the file landed anyway, which is worth knowing about this engine. Pointed lens petals, a tiled grey field baked behind them, the rivet detached below the fan, stray scribble inside the vermilion petal. |

`audit.html` carries the scored contact sheet with all five takes and every
liability; `audit_sheet.py check` passes on it (35 local image references, all
resolve).

## What Engine C caught that the hand-authored take did not

1. **Capsule ends, not corner radii.** The master started with 44px-corner
   paddles, which read as cards — and `report`, `clarify` and `resume-session`
   already own cards. Both raster takes and the Arrow take independently drew the
   leaves as full capsules; at equal contrast (0.1937 against 0.1925) the capsule
   is the better object and the better sibling separation.
2. **The taper into the rivet.** Every other engine narrowed each leaf toward
   its tab. Constant-width paddles read as three bars that happen to meet; a
   tapered leaf reads as one object rotating about a pin, which is what makes the
   fan a fan.
3. **A white frost is not a pale leaf.** C2 rendered the frosted sample as a true
   white on white and it vanished by 32px — the raster engine's named frost
   failure. The master's pale leaf is a warm off-white with a real seat edge
   because of it.

## What measurement caught that the eye did not

1. **Three separate stray-light bugs, each of which looked like a colour bug.**
   The rejects' rim and seat strokes, run as one pass at the end, painted their
   bright edges straight across the gel leaf standing in front of them — a scratch
   on the finished face and a stray arc round the rivet. The gel leaf's ambient
   occlusion, clipped to the leaf behind and painted *after* its own body, covered
   the whole overlap region and read as a hard diagonal cut across the face. The
   warm bounce in `highlight` did the same thing more faintly, because the layer
   plan puts highlights above everything. All three are paint-order defects with
   every hex still correct.
2. **The side face was blocking the transmission it was meant to sit under.** An
   11px offset copy of the leaf covers ~95% of its own body, so the frosted leaf
   was compositing over an opaque pale slab instead of over the dark leaf behind
   it, and its translucency was declared and not visible. Masked to the sliver
   that actually protrudes, the slate reads through the cream and the overlap
   becomes the tile's strongest material tell.
3. **A negative corner radius renders as a straight chord, silently.** The
   specular was cut as a shrunken copy of the leaf, and shrinking took `top_r`
   below zero; `rsvg-convert` drew a hard diagonal across the gel face and did not
   error. Clamp any radius that a `grow` parameter can reach.
4. **The pale leaf measures 1.13:1 against the cushion.** Dilated-ring
   figure-ground (every pixel of a colour mask against a 45px `MaxFilter` dilation
   of that mask, median to median) says the gel leaf reads at 3.37:1 and the slate
   at 3.74:1, but the cream leaf at 1.13:1. It survives small sizes by being
   flanked by two darker leaves, not by separating from the ground.
5. **Geometry was worth ~0.02 of contrast and value was worth ~0.03.** Widening
   and lengthening the leaves from 214×562 to 238×586 moved 16px RMS from 0.185 to
   0.191; deepening the accent to the family's lower band and the slate with it
   moved it to 0.201. Past that, growing the fan buys contrast by breaking the
   composition constant (0.70 of the tile against Tahoe's 0.55-0.65), so it stopped.

## Fidelity

Take A scored against take C1 at five sizes, numpy tier (no torch, so luminance +
SSIM + edges only — the material metric never ran, so these numbers are evidence
about structure and small-size legibility and not about material):

```
                1024      256      128       32       16
composite     0.5599   0.5499   0.5723   0.8542   0.8807
own contrast  0.5566   0.5541   0.5529   0.5490   0.5378
C1 contrast   0.5615   0.5604   0.5604   0.5579   0.5570
ssim          0.8269   0.6583   0.5772   0.7056   0.7441
edge f1       0.0400   0.2677   0.4848   0.9497   1.0000
```

The loop was stopped deliberately after porting C1's two geometry findings by
hand. Own contrast is within 0.005 of the raster's at 1024 and 0.019 at 16px, so
the material gap is small; the low edge agreement at 1024 is mostly C1's baked
bezel, which is one of the two things it fails on. Converging further would drag
in a rounded tile inside the family mask and a flat single-layer construction. The
rubric outranks the gate, and a gate ACCEPT is evidence rather than a verdict.

## 16px contrast

Alpha-masked RMS relative luminance on a 16px downsample, the family metric:

| | value |
|---|---|
| the icon this replaces | 0.174 |
| shipped `icon-256.png` | **0.202** |
| direct 16px render of `icon.svg` | 0.207 |
| family median across the 36 shipped tiles | 0.176 |
| engine C1, the raster that won the material read | 0.211 |

## Known liabilities

- The cream leaf measures 1.13:1 against the cushion. A taupe register for it
  would fix that and would cost the "blank default" reading the pair depends on;
  the trade has not been swept.
- #10 is satisfied by construction rather than by test. Dark, Clear and Tinted
  have not been rendered.
- Measurably flatter than the raster between 128 and 1024. The gel face is a
  three-stop ramp plus one sheen and one specular slab; an inner top glow and a
  tighter ambient-occlusion crescent at each overlap would close most of what is
  left without touching geometry.
- The specular is one authored slab rather than a profile fitted to the reference,
  so it reads glossy at 1024 and has gone by 48px.
- The fan's union silhouette is close enough to a letter V that a fresh viewer may
  name the letter before the object. It was accepted because the letter is not in
  the skill's name and no sibling owns a splayed fan, but it is the first thing to
  revisit if the set ever gains a V-shaped neighbour.
- The rejects are quieter than the accent by design, which means at 16px the tile
  is carried by one hot leaf plus a dark tail. If the marketplace ever renders
  tiles under a system tint, the value order is what has to hold.

## Rendering notes

The icon renders through `rsvg-convert`. `audit.html` was served on port 9334 and
captured with Obscura, which proved its images resolve and its scores are in
place; unlike the note recorded on `deck-craft`, this engine did lay the
`.renders` row out horizontally, because the template now carries the flex on an
inner div rather than on the `<td>`. The judgement behind the scores was made on
the PNG renders themselves at 128 / 64 / 48 / 32 / 16, not through the sheet.

The banner is still owed (dated debt, 2026-08-18) and a separate pass owns it. The
accent is `#CE4A18` with `#E5793C` and `#93300E`, and the light axis is 112°.

```bash
python3 build_icon.py                       # writes icon.svg
for s in 1024 256 128; do rsvg-convert -w $s -h $s icon.svg \
  -o $([ $s = 1024 ] && echo icon.png || echo icon-$s.png); done
SK=../../create-mac-icon/skills/create-mac-icon/scripts
python3 $SK/audit_sheet.py render . --take engineA=icon.svg \
  --take engineB1=icon-engineB-arrow-920b9d.svg \
  --take engineB2=icon-engineB-arrow-921e96.svg \
  --take engineC1=icon-engineC-5db443.png:raster-mask \
  --take engineC2=icon-engineC-3a4e16-2.png:raster-mask
python3 $SK/audit_sheet.py check .          # must exit 0
```
