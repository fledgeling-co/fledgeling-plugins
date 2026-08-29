# mockup-fidelity icon - spec, decisions and audit notes

Direction **"The Overlay"**. Built with the `create-mac-icon:create-mac-icon` skill: its
`icon-directions.md` pipeline (three engines, written audit sheet),
`material-recipes.md` for the constructions, `assets/squircle-path.txt` for the
family silhouette, and `scripts/fidelity.py` for the measured rounds.

---

## The spec

**Concept.** The reference is scribed into the tile itself - a rectangle cut in
porcelain with registration brackets at its corners - because in this skill the
mock is the authority, and an authority is not another card. The implementation is
a clay-gel slab of exactly the same size and corner radius, laid over it and
misregistered by a measured `(100, 76)`. Nothing else is on the tile.

That one misregistration carries the plugin's whole ledger, all three states at
once, with no extra props:

| State | What you are looking at |
|---|---|
| **PRESENT** | where the slab covers the scribed rectangle - and the scribed line and the far bracket are visible *through* the gel, so the mock is still readable under the implementation |
| **DIVERGENT** | the slab riding proud past the scribed line at the bottom right, with its own contact shadow on the porcelain: the app-extra element |
| **ABSENT** | the L of exposed reference at the top left, lit ember. Drawn to scale, so the icon reports the size of the difference rather than asserting a match |

**Signature move.** *The exposed sliver is the mark.* The accent is spent on the
gap between the two objects and never on either object, so the first thing the eye
lands on is the disagreement - and the sliver's width **is** the misregistration,
not a symbol for it.

**Direction.** Tahoe gel-glass, sub-register (a): porcelain cushion tile carrying
one coloured gel object. Runner-up, declined: **"The Template"** - the
implementation seated inside a shaped aperture cut in a gauge plate, one notch
left unfilled. It says the same thing, but the marketplace already carries two
mould-and-part metaphors (`create-mac-icon`'s tile leaving a mould,
`create-skill`'s pour into a flask) and a third would have read as a house habit
rather than as this skill. The overlay also survives the silhouette test better:
an aperture disappears when a plate is filled black.

**Device.** Bank #16 (the icon performs the verb) crossed with #21
(overlap-as-identity - the blend zone between two translucent primitives is the
mark) and #17 (tile-as-machine: the reference is cut into the tile, not laid on
it). The brackets are sanctioned diegetic garnish (#8 of the Tahoe grammar):
sub-legible, a real feature of the thing being drawn.

**Silhouette.** Two same-sized rounded rectangles out of register, plus the
slab's wall. Filled solid black it is nameable as *two plates off register* at
160px and still separable at 32px - see liability 2 for what that costs.

**Ground register.** Porcelain / daylight, matching the marketplace default. The
dark deep-sea register belongs to `trawl`.

**Palette.** Two hue families, no more.

| Role | Hexes |
|---|---|
| Cushion ground | `#F9F6EE` -> `#F3EFE4` -> `#E4DDCB`, vignette `#4A3F2E` at 13% |
| Inner rim light | `#FFFDF8` |
| Mock floor (the reference's own tone) | `#F0E9D9` -> `#DFD5BE` |
| Scribe (the groove) | `#8A7A61` |
| Gel slab, face | `#8A7D64` -> `#6B6049` -> `#443A2B` |
| Gel slab, wall | `#4B4133` -> `#342C21` |
| The scribe seen through the gel | `#332C21` |
| Ember (the one accent, kin to `#C4622D`) | `#F79A61` · `#E4652E` · `#B8390F` · `#8E2E0C`, core `#FFD3A2` |

**Light model.** One soft key up and to the left, plus the lit gap as the
sanctioned emissive second source - it grazes the two slab faces that look into it
and spills onto the porcelain past the scribe, and it never casts.

**Layer plan (#10).** `#bg` cushion, vignette, the ember's spill on the
porcelain, the mock's floor, its groove, its near/far walls, the top-left bracket
· `#mid` the lit gap (trough fill, deep outer rim, hot seam core) and the
overhang's contact shadow · `#fg` the slab's wall and face, and the mock read
through the gel (floor tone, far wall catch, scribed line, far bracket) ·
`#highlight` satin, the gap's bounce into the gel, the lateral shade, the
ambient occlusion, the transmitted perimeter bevel, the two edge rims, and the
cushion's inner rim. Maps 1:1 onto Icon Composer layers.

**Geometry.** `MX,MY = 196,196`, `MW,MH = 540,540`, `R = 76`, offset
`DX,DY = 100,76`, wall `24`, and `INSET = 26` for the porcelain margin the light
leaves inside the reference's frame. Union 640 x 640, centred on (516, 516),
62.5% of the tile width - inside the corpus's 55-65% band. Both rectangles are the
same size on purpose: *the only difference between the reference and the
implementation is that one of them is in the wrong place.*

---

## What the corpus said before anything was authored

Sampled off `create-mac-icon/references/corpus/apple-2026/` in the porcelain
register (apple-05, apple-11, apple-18, apple-23, apple-26, apple-28):

| Property | Apple's porcelain register | What this icon does |
|---|---|---|
| ground, top | L 0.99-1.00 | 0.96 |
| ground, bottom corners | 0.92-0.93 | 0.82-0.84 |
| contact shadow under the object | a shallow dip, 0.929 -> 0.877 | a tighter dip, blur 14 at 33% |
| saturated pixels | L 0.28-0.52, S 0.64-0.85 | ember median L 0.39 (gamma), S 0.82 |
| darkest in-tile pixel | 0.12-0.14, **cool** (hue 200-214) | 0.06, warm |

Two deliberate divergences from the corpus, both on set kinship: the ground runs
about 0.10 darker at the bottom because `test-campaign` and `resume-session`
measure TL 0.92-0.93 / BL 0.81 / top-mid 0.95 and the shelf is the real judge; and
the shadows are warm because every shadow in this family is warm.

---

## Distinguishing it from the siblings

Every sibling device was checked at render, and three are near neighbours:

- **`improve-skill`** owns a before/after boundary - two states of one object.
  This is two objects, one of which is in the wrong place.
- **`be-my-witness`** owns comparing a capture against an expectation through a
  lens. There is no lens here and no instrument; the comparison is the geometry.
- **`should-compact`** owns two slabs squeezing a symmetric seam, and
  **`resume-session`** two cards with an accent splice between them. Both are
  *symmetric pairs with the accent between equals*. This is an **overlap**, off
  register, with an asymmetric L, and its accent sits inside the exposed
  reference rather than between two peers.

The banned substrate - a white card carrying grey text lines or pill bars, which
five plugins already share - is not used: the slab carries no content of its own,
and what fills it is the mock read through it.

---

## Per-take scores

Full contact sheet with real renders at 128 / 64 / 48 / 32 / 16 plus the x6
squint: `audit.html`.

| Take | Engine | Score | One line |
|---|---|---|---|
| **A** `icon.svg` | hand-authored layered SVG, `build_icon.py` | **11 / 12 - ships** | All four non-negotiables pass; loses #7 because the slab's lightest decile (top rim, lit bevel) is 2.40:1 against the porcelain beside it |
| B `icon-engineB-arrow-fcbac9.svg` | Arrow 1.1 vector | 6 / 12 | Baked its own rounded-square boundary inside the family squircle (#1), floats inset (#2), three hue families (#6), flat isometric (#9), and the two plates fuse at 32px (#4) |
| C1 `icon-engineC-4e2ac1.png` | GPT Image 2, 4 reference images | 10 / 12 | **The material target.** Fails #10 as any flat raster does, and #6 on a measurement: 26.8% of its tile reads warm-saturated because its slab shares the ember's hue family |
| C2 `icon-engineC-d2d9dc-2.png` | GPT Image 2, same brief | 9 / 12 | Halves the misregistration, so the top arm all but disappears and the mark reads as a slab with a hot left edge (#11 as well as #10 and #6) |

Measured on the masked 1024 renders, WCAG relative luminance, object against a
45px dilation of its own mask (median to median), because a hand-placed "ground
beside it" sample has hidden a real figure-ground defect in this marketplace
before:

| | A (ships) | B | C1 | C2 | test-campaign | create-skill |
|---|---|---|---|---|---|---|
| object vs its own surround | **4.03:1** | 5.51:1 | 3.84:1 | 3.79:1 | 2.95:1 | 2.18:1 |
| object's lightest decile vs surround | 2.40:1 | 1.92:1 | 1.70:1 | 1.74:1 | 2.06:1 | 1.48:1 |
| warm-saturated share of the tile | 8.5% | 1.3% | 26.8% | 21.5% | 3.3% | 10.6% |
| 16px in-mask luminance spread | **0.2405** | 0.2036 | 0.2195 | 0.2217 | 0.1728 | 0.1762 |

The 16px figure is the standard deviation of in-mask luminance on the 16px
render. Across the 35 icons in this marketplace the median is **0.169** and the
two weakest sit at **0.0486** and **0.0499**, so this icon clears the median by
42% and the brief's 0.152 bar by 58%.

---

## The measured rounds

`fidelity.py`, take A against take C1, three rounds kept at `fidelity-runs/rNN/`
with `score.json`, the residual and edge maps, the round's `candidate.svg` and a
`brief.md` saying what was sampled and why.

| Round | Edit class | 1024 | five-size mean | 32px self-contrast |
|---|---|---|---|---|
| r00 | baseline | 0.6054 | 0.7317 | 0.563 |
| r01 | material: gel body deepened, dominant axis vertical, transmitted rim on every edge, hotter seam | 0.6167 | **0.7479** | 0.609 |
| r02 | material: perimeter bevel evened, top hairline cooled - **ships** | **0.6185** | 0.7465 | 0.609 |

**The metric tier is numpy, and that matters more than the numbers.** There is no
torch on this machine, so LPIPS never ran - and LPIPS is the only term that sees
material, at exactly the two sizes (256, 1024) where material lives. The skill's
`gate` refuses to grade on that tier by design, and no gate verdict was taken
here. Every edit above was chosen from a hand-sampled profile off C1 and confirmed
by looking; the composites are corroboration, not authority.

### What the reference actually taught

Three properties sampled off C1 on matched geometry, each of which contradicted
the draft:

1. **A gel body's face is flat across its width and lit top to bottom.** C1 runs
   L 0.61 at its top rim to 0.33 at the base, and varies by under 0.02 across the
   middle of its width. The draft had a corner-to-corner diagonal ramp, which
   reads as a *lit opaque plane* rather than as a body. The lateral component
   moved into its own layer, because a gradient carries one axis and a lean
   written into a mostly-vertical vector projects past offset 1 and renders flat.
2. **The transmitted rim is on both side edges, not only the lit one.** C1 reads
   0.43 at its left edge and 0.47 at its right against a 0.37 body. The draft's
   right edge was its *darkest* region - correct for an opaque slab, wrong for
   gel. This is the third time in this marketplace that an assumed
   bright-where-you-expect-bright relationship has failed, and the fix was again
   to measure rather than to reason.
3. **The seam core is brighter than it looks reasonable to author.** C1 peaks at
   L 0.79-0.84 immediately against the slab; the draft peaked at 0.67-0.72.

And one property that was deliberately **not** tracked: C1's accent sits at
S 0.50, a peach rather than an ember, against the family's 0.70-0.90 and this
icon's 0.82. Converging there would have bought fidelity points by walking the
accent out of the family. The rubric outranks the gate, and set kinship outranks
the reference.

---

## Decisions made without asking

- **The reference is cut into the tile, not laid on it.** A second card would have
  put this icon in the middle of the marketplace's most crowded substrate and made
  the mock look like a peer of the build rather than the authority over it.
- **The two rectangles are the same size.** Making the build smaller would have
  read as "incomplete" and dodged the harder, truer statement: it is the same
  thing in the wrong place, which is what drift actually looks like.
- **The lit gap stops 26px inside the reference's frame.** Filling the whole
  exposed strip made the reference read as an orange plate; the porcelain margin
  is what keeps it reading as porcelain that has been cut.
- **The offset is (100, 76), not (88, 88).** A 45-degree shift reads as a
  constructed diagram; an unequal one reads as something observed.
- **r02 shipped over r01 against the score.** The composite fell 0.0014, which is
  noise, and the round is what makes the slab read as a body. Recorded rather than
  hidden.
- **No blind judge panel was run.** The panel is a bounded set of model calls and
  the loop here was two rounds of hand-measured material transfer, not a
  contested schedule of gate ACCEPTs; there was no disagreement for a panel to
  adjudicate. Worth running if this icon is revisited.

---

## Known liabilities

1. **The slab's lit top rim and bevel sit at 2.40:1 against the porcelain beside
   them.** Half the object's boundary is carried by rim light and contact shadow
   alone, so it will soften under a heavy tint or in grayscale. This is the
   porcelain register's standing trade - `test-campaign` sits at 2.06:1 and
   `create-skill` at 1.48:1 on the same measure - and the object as a whole clears
   the #7 floor at 4.03:1.
2. **The silhouette is nameable but generic.** Filled black it is two offset
   rounded rectangles; what makes it *this* icon is the ember in the gap, which a
   silhouette test cannot see. If a future sibling lands on offset plates, this is
   the icon that will need to move.
3. **The brackets and the mock's line read through the gel both vanish below
   about 48px.** The two devices that carry the argument are large-size only; at
   16px the icon is a dark slab with a warm L, which is the right read but a
   shallower one.
4. **The ember is 8.5% of the tile**, generous against this family's usual accent
   restraint (`test-campaign` 3.3%). It is the first thing to reduce if the
   icon shouts on a shelf, and the honest reason it is that big is that the gap is
   drawn to scale.
5. **The material was never measured by an instrument.** numpy tier, no LPIPS, no
   gate verdict. The material decisions rest on hand-sampled profiles off C1 and
   on the eye. If this icon is revisited on a machine with torch, re-score r00
   against r02 first - the ranking may not hold.
6. **The mock's floor tone read through the gel is a 0.10-opacity fill.** It is
   the signature move's own evidence, and it is close to the threshold where two
   renderers could disagree. Both were checked: the master rendered in a browser
   (Obscura, inline SVG at 512) against `rsvg-convert` at the same size differs by
   a mean of **0.75/255**, p99 3.0, with 0.26% of pixels more than 12 apart and
   those confined to anti-aliased edges - so the mask, the filters and every
   gradient agree across the two. Any future round that touches the gel's opacity
   or the `exposed` mask should re-run that comparison rather than assume it.

---

## Files

| File | What it is |
|---|---|
| `build_icon.py` | Engine A. Geometry and material as named constants; a fidelity round is a parameter edit, never path surgery |
| `icon.svg` | the shipped master, four named layers, generated - edit `build_icon.py`, never this |
| `icon.png`, `icon-256.png`, `icon-128.png` | exports, all from the master |
| `icon-engineB-arrow-fcbac9.svg` | Engine B, Arrow 1.1 |
| `icon-engineC-4e2ac1.png` (+ `-masked`) | Engine C take 1 - the material reference the loop scored against |
| `icon-engineC-d2d9dc-2.png` (+ `-masked`) | Engine C take 2 |
| `audit.html` + `audit-renders/` | the contact sheet, every take scored including the losers, plus `render-manifest.json` |
| `fidelity-runs/r00..r02/` | three rounds: `candidate.svg`, `score.json`, residual and edge maps, and a `brief.md` per round |
