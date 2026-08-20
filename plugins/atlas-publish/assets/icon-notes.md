# atlas-publish — icon notes

What was built, what was tried, and what the losing take was better at. The
commission is `ICON-BRIEF.md`; the scored contact sheet is `audit.html`.

## What shipped

**The stroke that stops at the gate.** The capital A of the Atlas script
wordmark, cut at the exact point where the letterform hands over to the `t`,
re-poured as a soft-extruded graphite gel monoline on warm porcelain. A
vermilion gate slab stands where the next stroke would begin, and the script's
exit stroke butts flush against its flat left face. The porcelain beyond the
gate is bare, and the object sits 25px left of centre so that emptiness is
wider than the margin in front of the letter.

The signature move is the cut at the handover. The word is drawn as far as it
can be drawn without a person, and stopped by something deliberate rather than
by running out. `atlas-publish` archives, uploads and registers a release and
then refuses to make it live; draft is its terminal state, and that refusal is
the only thing in the tile.

Direction: Tahoe Gel-Glass, porcelain sub-register, hybridised with Monochrome
Logomark through device #19, re-materialised brand mark. Runner-up: Object Tile,
which would have made the release bundle the noun. Matching the fledgeling set —
warm porcelain ground `#FCFAF4 → #DED5C2`, one ember accent on the family's
measured luminance (`#DE5A28`, L≈0.447), shared squircle from
`assets/squircle-path.txt`, exports at 1024 / 256 / 128.

## The two concepts, and why this one

The brief named two candidate directions and asked for the decision to rest on
renders. Both were built through Engine C against the same corpus references.

**The losing take: a sealed bundle held at the lip of a stage**
(`icon-engineC-lip-b9426d.png`, 5/12). It is better than the winner at exactly
one thing, and it is not a small thing: **it says "held" without needing to be
read.** A slab poised over a drop beside an un-pressed button is legible as
withheld action to someone who has never heard of Atlas, where the shipped icon
asks you to notice that a letter has stopped. If the plugin were generic release
tooling, that take would ship.

Three measured reasons it lost anyway:

1. **16px.** Half the tile goes to an empty pale stage, and the release control
   is small by the logic of the idea. At 16px it is a grey blob with a
   sub-pixel dot. That is a hard fail on a non-negotiable check.
2. **The metaphor is the most crowded in the marketplace.** `ship-feature`,
   `ship-fleet`, `shipyard` and `create-swe-project` already own ramps,
   slipways, cradles and hulls between them, and `better-loop` owns a block
   held on a track. A dark rounded slab is additionally the ground shared by
   `agent-voice`, `tui-craft`, `mac-design-digest` and `should-compact`.
3. **It rendered as a perspective 3D scene**, which breaks the family's
   front-facing grammar and reads as a lunchbox on a countertop.

The winner is unclaimed on every axis that matters: across forty sibling icons
there is not one letterform, and this is the only brand-specific plugin in the
marketplace, so being unmistakably one product is the point rather than a
liability.

## What was tried and dropped

- **The whole word.** "Atlas" is 810 × 272 in the mark's own space. Rendered at
  16px it is a horizontal smear with no mass — measurably worse than any
  sibling, whose 16px reads are all *mass plus accent* rather than legible
  glyphs. It also trips the catalogue's own no-text rule (rubric #12, failure
  mode #4). "At" and "Atl" were both built and both already illegible at 16px.
  A single letterform is the sanctioned form.
- **A pill-shaped gate.** With `BAR_R = BAR_W/2` the accent reads as a text
  caret sitting after a letter, which is very nearly the opposite meaning. A
  slab with a flat left face gives the stroke something to press against.
  `icon-engineC-gate-0eb2a6.png` is kept in the audit sheet precisely because
  the pill/slab comparison only exists there.
- **Darkening the glyph's bottom edges.** Reversed after looking at the corpus:
  `apple-12` holds its dark body's bottom edge at V 0.318 against a middle of
  V 0.133, because the porcelain bounces into it. The band along the bottom is
  now a lift, not a shade.
- **The family's pooled composition shadow.** It is a stacked-object
  construction. Under one compact body it renders as a visible soft box behind
  the artwork. Dropped; the three-part cast carries the seat on its own.
- **A cool grey rim light.** `#FFFFFF` and cool greys on a warm-lit body read as
  a gloss streak rather than as volume. The rim is `#FFF3E2` at 0.44, decaying
  along the one shared key axis.
- **A ghost of the remaining letters debossed beyond the gate.** Considered and
  not built: it re-introduces the wordmark, adds a second metaphor, and muddies
  the right half at every small size. Emptiness beyond the gate says the same
  thing and costs nothing.

## What was measured

| | |
|---|---|
| ink vs ground, WCAG on the 1024 render | 8.64 : 1 |
| gate vs ground | 3.76 : 1 |
| gate vs ink — the one boundary below the 3:1 floor | 2.30 : 1 |
| grayscale tiers, ink / gate / ground | 59 / 113 / 234 |
| 16px luminance spread (gamma-encoded, over white) | 0.2415 |
| — same measure across 40 marketplace siblings | median 0.2146, p75 0.2597 |
| gate's smallest dimension at 16px (needs > 1.5px) | 2.07 px |
| structure gate | PASS — 4 paths, 8 gradients, 7 filters, 4 named groups |
| internal contrast, master vs raster reference | 0.68 vs 0.45–0.47 |

**16px verdict: survives.** The master sits in the upper half of the family
distribution and 27th of 41 on mass. What survives the squint is the
letterform's silhouette and the vermilion tick to its right, in that order — the
same bargain `apple-10` makes, since an 83px monoline is well under the ~190px a
feature needs to resolve individually at 16px. The shelf strip against seven
siblings at 16px and 48px is what settled it; the reference raster was not that
shelf and could not have.

## Two things not measured, and one that could not be

- **The perceptual material metric never ran.** The library it needs is not
  installed on this machine. The scores above cover structure and small-size
  legibility only; the *material* — the part this pipeline exists to get right —
  was never measured, and the fidelity loop was deliberately not run rather than
  run blind. On record, eight rounds on that degraded tier once accepted their
  way to the worst take of a run. What stands in for it is the corpus: values
  were sampled out of `apple-10`, `apple-12`, `apple-26` and four fledgeling
  siblings before the first line of the master was written.
- **The blind panel could not form a majority.** Two of three judge lanes were
  down (no OpenAI key; the cursor lane exited 1), leaving only the generator's
  own family, whose verdict is recorded and excluded by protocol. It preferred
  the master over the Arrow take on all four axes and flagged the object for
  crowding the tile edges, which is why `OBJECT_WIDTH_FRAC` came down from 0.68
  to 0.655. Treat the panel as unrun.
- **Rendering was verified in librsvg only.** The rim and cast-shadow filters
  want a spot-check in Safari and against a real Dock tint before release.

## Known liabilities

1. **The gate reads 2.30:1 against the graphite**, below the 3:1 floor, at
   exactly the boundary the icon's meaning lives on. The two masses separate by
   hue and by a hard edge rather than by luminance, so a viewer with a
   red-green deficiency loses some of that separation. Both still clear 3:1
   against the ground, and the grayscale render holds three distinct tiers, so
   the composition does not collapse — but the *contact* is the weakest reading
   in the tile.
2. **The letterform is text-adjacent.** It passes rubric #12 as a diegetic
   monogram, and that is a judgment rather than a measurement. Someone who does
   not know Atlas sees a decorative script *a*.
3. **The monoline is 83 tile px**, so at 16px the stroke itself does not
   resolve; only its mass does.

## Files

| | |
|---|---|
| `icon.svg` | the layered master that ships (bg / mid / fg / highlight) |
| `build_icon.py` | the generator — geometry and material as named constants |
| `make_glyph.py` | derives `glyph-path.txt` from the Atlas brand mark |
| `svgpath.py` | the minimal path parser those two share |
| `glyph-path.txt` | the traced, cut, outset letterform |
| `squircle-path.txt` | the family silhouette, copied from `create-mac-icon` |
| `audit.html` | the scored contact sheet, losers included |
| `audit-renders/` | every take at 1024 / 256 / 128 / 96 / 64 / 32 |
| `fidelity-runs/r01/` | the baseline score against the raster reference |
| `fidelity-runs/panel/` | the blind panel run, including the two lanes that failed |
| `icon-engineB-arrow-*.svg` | the Arrow vector take |
| `icon-engineC-gate-*.png` | the two raster takes of the shipping concept |
| `icon-engineC-lip-*.png` | the raster take of the losing concept |

A fidelity round is a constant edit in `build_icon.py` and a re-run. Nothing in
`icon.svg` should ever be hand-edited.
