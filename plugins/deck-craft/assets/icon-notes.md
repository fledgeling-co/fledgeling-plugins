# Icon notes — `deck-craft`

Direction 2 (Tahoe gel-glass), sub-register (a): porcelain cushion carrying gel
objects. Same register as `test-campaign`, `whats-left`, `proctor` and
`report`, which it sits beside in the marketplace lineup.

Replaces the 2026-08-18 template icon — a blank `#FAF9F4` rectangle in a flat
grey bezel with a vermilion underline, 74.7% locally-uniform interior and 0.087
RMS luminance contrast at 16px. That one was category clip-art twice over: it
collided with `design-craft` (a light bezelled frame holding pale panels) and it
spent its accent on decoration.

## The idea

**The running order.** Four identical 16:9 slide plates stand in sequence: the
one you are on in front as a warm graphite gel slab — deck-craft's own dark-canvas
register — and the rest of the deck receding behind it in frosted porcelain. Every
plate carries the *same* vermilion title band, at the same height on its own face.

The signature move is that the accent belongs to the sequence rather than to a
slide. One mark, repeated, and its climb from front to back **is** the running
order; re-order a plate and the climb breaks. That is deck-craft's own claim —
the title sequence is written before any slide, because the titles read in order
are the deck's argument — performed by the artwork instead of illustrated by it.
The plates are congruent and unscaled on purpose: fixed-size content is the
skill's founding constraint, so every plate is the same plate.

Device #20 from the bank (data-as-glyph abstraction, one accent datum) crossed
with #16 (the icon performs the verb) and #13 (a sequence resolving into a
direction). Differentiated from its neighbours by what the accent is doing:
`report` is stacked document cards with a rule on the top card only,
`armada-sync` is a column of slate bars with one lit, `test-campaign` is a
matrix with one drawn absence. Here the mark is on *every* element and the
information is in its position.

Runner-up direction, recorded rather than built: **the throw** — a gel projector
body at the lower left casting a translucent wedge onto a 16:9 stage cut by the
tile's right edge. It read instantly at 16px in the silhouette test and no
sibling owns a wedge, but it is a picture of a deck being presented rather than
something the skill does to a deck, and at three props (body, beam, stage) it
sits on failure mode #5.

## Palette, sampled rather than guessed

Read out of the corpus captures and the sibling PNGs before anything was authored.

| | value | source |
|---|---|---|
| cushion | `#FCFAF4` → `#F3EDE1` → `#DED5C2` | test-campaign `#F8F5EE`→`#E4DDCB`, whats-left `#F6F3EA`→`#E0D9C8`, proctor `#F8F4EC`→`#E9E2D4` |
| inner rim | `#FFFDF8` | every Tahoe capture carries one; a flat ground is previous-era |
| vignette | `#8B7F66` at 0.26 | corpus apple-23 / apple-28, both porcelain register |
| leading plate | `#6E6353` → `#413929`, edge `#241E13` | apple-24 (black gel binoculars): a near-black object stays readable on a lit tile via rim light |
| deck behind | `#FFFEFB`→`#EFE7D5`, `#F7F1E3`→`#E2D9C4`, `#EDE6D6`→`#D3C9B4` | three value steps, each flatter as it recedes |
| accent | `#F79155` → `#DE5A28` → `#A63B14` | report `#E46235`, whats-left `#DF612E`, clarify `#E0612E`, dossier-report `#EA5B34`; kin to Fledgeling `#C4622D` |
| shadow | `#3B3327` | warm, never blue — the corpus's darkest gel pixels are warm at matching luminance |

Sibling interior luminance runs 88–255 with medians 170–241; this icon sits
inside that range.

## Layer plan

Four named `<g>` groups, mapping 1:1 onto Icon Composer layers:

- `bg` — cushion radial, edge vignette, inner rim light on the family squircle.
- `mid` — the deck behind, furthest plate first: cast shadow, side face
  (the slab's own thickness), translucent gel face, sheen, title band, seat edge,
  key-light catch on the top and left edges only.
- `fg` — the plate you are on, same construction with a heavier contact shadow.
- `highlight` — the warm bounce the leading band throws forward.

Named constants for the things a banner will need: `LIGHT_ANGLE_DEG` /
`LIGHT_AXIS` (118°, one key light, every cast and rim derived from it),
`Spec.plate_w` with `PLATE_ASPECT` (the 16:9 cell), `Spec.step_x` / `step_y`
(the sequence), and `ACCENT` / `ACCENT_HI` / `ACCENT_DEEP`.

## Three engines

| | take | score | outcome |
|---|---|---|---|
| **A** | `icon.svg` (+ `build_icon.py`) | **11 / 12** | **ships.** Four named layers, 25 paths, 16.8 KB, `fidelity.py structure` PASS. |
| **B** | `icon-engineB-arrow-e21b68.svg` | 5 / 12 | Arrow 1.1. Lost on two non-negotiables: it bakes its own corner radius (not the family superellipse) and draws the title bands as 0.75px hairlines that vanish by 32px. Nothing salvaged. |
| **C1** | `icon-engineC-9a8f54.png` | 8 / 12 | GPT Image 2 with four references (corpus apple-23 / 28 / 26 plus the test-campaign tile). **Won the material and composition read** and is why A was rebuilt twice. Fails #10 by construction and #1 as delivered (opaque square corners). |
| **C2** | `icon-engineC-aa7201-2.png` | 7 / 12 | Second raster take, kept for the record. Flatter, and its band runs off the plate edges so it wraps the slab instead of titling a face. |

`audit.html` carries the scored contact sheet with all four takes and every
liability; `audit_sheet.py check` passes on it (28 local image references, all
resolve).

## What Engine C caught that four hand-authored sweeps did not

Six geometry sweeps were rendered and measured before the raster takes came back,
and all six failed the same way: **congruent rectangles overlapped in the plane
read as one slab, not as a deck.** The failures are worth keeping because each one
looked reasonable as a parameter change:

1. **Lateral offsets only (step_y = 0)** put every plate's top and bottom edge on
   the same line, so the union silhouette was a single rounded rectangle with
   interior seams. It renders as an eraser, and the value ramp reads as one
   object shading darker to the right rather than as four plates.
2. **Collinear title bands are geometrically impossible with visible separation.**
   For the bands to be straight, at the same place on every plate, *and* parallel
   to the plates' own edges, the offsets have to run along the bands — which is
   the slab in (1). Two rounds were spent proving that three of those constraints
   can hold at once and never all four.
3. **A single deck-axis stroke fixed the line and broke the object.** Extending it
   past the plates turned the icon into cards on a skewer — and a corner-to-corner
   diagonal is the most template-worn move in the corpus (direction 7).
4. **The raster chose the fourth option and it was the right one:** drop
   collinearity, keep the mark. Per-plate bands that *climb* read as a sequence
   at every size, because each one is a chunky mark attached to its own plate,
   and the composition then needs recession in depth and real occlusion rather
   than a bigger accent.

Generalises: when three of four constraints on one element can hold at a time,
the one to drop is the one no viewer can check. Nobody can see that four bands
are collinear; everybody can see that four marks climb.

## What measurement caught that the eye did not

1. **The warm bounce under each band was browning whole faces.** At
   `rule_h × 2.6` of blurred accent at 0.40 alpha the graphite plate's lower half
   went bronze while every palette hex was still correct — the same wide,
   low-amplitude, hue-only defect `material-recipes.md` records for the
   ship-feature hull and the dossier-report specular. Cut to `rule_h × 0.85` at
   0.26: a kiss on the face just under the band, not a veil over it.
2. **A hand-placed figure-ground sample would have passed this icon.** The
   dilated-ring measure (every pixel of a colour mask against a 45px `MaxFilter`
   dilation of that mask, median to median) says the deck reads **4.41:1** against
   its own surround, the accent **2.01:1** — but the three porcelain plates alone
   are **1.18:1** against the cushion. They are carried by their seat edges and
   cast shadows, nothing else.
3. **The porcelain-only value ramp measured 0.103 RMS at 16px** — flatter than the
   icon it replaces. The graphite leading plate is not a taste choice; it is what
   takes the tile from 0.10 to 0.179.

## Fidelity

Take A scored against take C1 at five sizes, numpy tier (no torch, so luminance +
SSIM + edges only — the material metric never ran, so these numbers are evidence
about structure and small-size legibility and not about material):

```
                1024      256      128       32       16
composite     0.5837   0.5618   0.5549   0.7846   0.8448
own contrast  0.4731   0.4687   0.4608   0.4858   0.4538
C1 contrast   0.5508   0.5488   0.5479   0.5323   0.5274
```

The loop was stopped deliberately after porting C1's composition by hand. C1 is
more contrasty at every size — a real material gap — but converging on it would
drag in three things it gets wrong: 4:3 plates instead of the 16:9 stage the
skill's first rule is about, a dished tray instead of a cushion, and a flat
construction that fails #10 by definition. The rubric outranks the gate, and a
gate ACCEPT is evidence rather than a verdict.

## 16px contrast

Alpha-masked RMS relative luminance on a 16px downsample, the family metric:

| | value |
|---|---|
| the icon this replaces | 0.087 |
| shipped `icon-256.png` | **0.174** |
| direct 16px render of `icon.svg` | 0.179 |
| family median across 35 plugin icons | 0.176 |

## Known liabilities

- The three porcelain plates measure 1.18:1 against the cushion, so at 16px the
  deck behind the leading slab is carried almost entirely by its cast shadows. A
  deeper cushion or a taupe register for the rearmost plate would fix it and would
  cost the daylight read; the trade has not been swept.
- Measurably flatter than the raster at every size. The gel faces are a linear
  ramp plus one sheen; a later round could add an inner top glow and a soft
  ambient-occlusion crescent at each overlap without touching geometry.
- #10 is satisfied by construction rather than by test. The Dark, Clear and Tinted
  variants have not been rendered.
- Four rounded rectangles is one step from a card stack, and `report` owns stacked
  document cards. At 16px the climbing title band is doing all the differentiating
  work.
- `design-craft` is being rebuilt in parallel. This icon was made distinct on its
  own terms — tilt, depth recession, graphite leading plate, repeated accent — but
  the pair has not been read side by side after both land.

## Rendering notes

The icon renders through `rsvg-convert`. `audit.html` was served on port 9320 and
captured, which proved its images resolve and its scores are in place, but the
Obscura engine does not implement flex, so the sheet's `.renders` row stacks
vertically there instead of laying out side by side. The judgement behind the
scores was made on the PNG renders themselves at 128 / 64 / 48 / 32 / 16, not
through the sheet.

The banner is still owed (dated debt, 2026-08-18) and a separate pass owns it.

```bash
python3 build_icon.py                       # writes icon.svg
for s in 1024 256 128; do rsvg-convert -w $s -h $s icon.svg \
  -o $([ $s = 1024 ] && echo icon.png || echo icon-$s.png); done
SK=../../create-mac-icon/skills/create-mac-icon/scripts
python3 $SK/audit_sheet.py render . --take engineA=icon.svg \
  --take engineB=icon-engineB-arrow-e21b68.svg \
  --take engineC1=icon-engineC-9a8f54.png:raster-mask \
  --take engineC2=icon-engineC-aa7201-2.png:raster-mask
python3 $SK/audit_sheet.py check .          # must exit 0
```
