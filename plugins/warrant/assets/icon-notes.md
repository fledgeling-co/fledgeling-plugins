# warrant — icon notes

**What it is.** The marketplace tile for `warrant`, the verification-governance
plugin: eight skills that take the human out of per-item verification by writing
down what a machine may decide and revoking it when the evidence stops
supporting it. The icon has to say *authority narrowing to the scope it has
earned*, on a shelf that already owns several porcelain tiles with a lit slate
object on them.

Deliverables in this directory: `icon.svg` (the layered master, emitted by
`build_icon.py`), `icon.png` / `icon-256.png` / `icon-128.png` (squircle-masked
exports, written by the same script), `icon-A-v1.svg` and `icon-A-left.svg` (the
audit sheet's losing takes, also emitted by `build_icon.py --variant`), and
`audit.html` + `audit-renders/`.

There is no `runs/` directory here, and that is a deviation worth stating rather
than leaving as an absence: no raster reference exists to converge on (see
**Engines** below), so the fidelity loop was never armed. The eight rounds
recorded below were driven by looking at renders and by the script's own
measurements, not by `fidelity.py`.

---

## Direction

**Tahoe gel-glass, porcelain sub-register (a)** — lit slate objects on a
porcelain cushion tile with one bounded accent. Chosen over a
document/card treatment of the same subject (a signed warrant page, a stamped
authority card), which lost on two counts: a card is a *record* of authority
where the plugin's central mechanism is a *ladder* that moves, and a page of any
kind pushes straight into rubric #12 and into `report`'s territory two tiles
along.

Ground register is porcelain/daylight, per the family rule in the repo's
`CLAUDE.md`. The ground constants are lifted verbatim from
`plugins/shipyard/assets/build_icon.py` rather than re-derived, as is the key
light's axis, so the two tiles are lit by the same lamp and stand on the same
floor. The dark register belongs to `trawl`.

**One deliberate break with the shelf.** `CLAUDE.md` says "one warm accent". This
tile's accent is teal — `#186A73` in the light register and `#63C3CC` lifted —
because those are the values on the published research page this plugin came out
of, and the tile is the plugin's mark before it is the shelf's. Everything else
about the accent obeys the family rule: one hue family, spent on one element.
`trawl` is the only other tile carrying a teal, and it carries it as a dark
*ground* rather than as an accent, so the two do not collide.

**Glyph device** (subject-mined, not category clip-art): the authority ladder
itself. Five slabs, stacked, each narrower than the one above. The widest is the
scope nobody had to earn; the narrowest is the scope that was. Authority narrows
as consequence rises, so the width schedule accelerates as it descends — −15%,
−19%, −27%, −40% — because even steps are a chart's tick spacing.

**Signature move — "the ladder, settling."** Each slab's stand-off from the tile
decays as the slabs narrow: 40px, 27, 16, 7, 0. The widest floats clear of the
porcelain and throws a soft displaced copy of itself down and to the right; the
narrowest has landed and has a tight dark contact line welded to its base
instead. The gaps close on the same schedule (62, 52, 42, 32). So the tile reads
as authority *settling* into the smallest scope it has earned rather than as a
stack of stripes. It is the same grammar as shipyard's "the next plank arrives
lit", deliberately: there, one strake's stand-off decays *along its own length*;
here, five slabs' stand-off decays *down the stack*. One shelf, one idea about
what a lit object at a height means.

The palette was authored against numbers sampled out of
`references/corpus/apple-2026/`, not out of prose:

| property | sampled | source |
|---|---|---|
| porcelain ground | L 1.000 top-left → 0.913 mid → 0.831 bottom, neutral | apple-26 (Reminders) |
| porcelain, warm-neutral variant | `#E0DFDE` H30 S0.01 → `#BDBCB9` H45 S0.02 | apple-12 (Calculator) |
| non-accent element vs accent | rules `#C1C1C1` L 0.533; keys `#D8D9D7` L 0.691 — present, never competing | apple-26, apple-12 |
| accent core → its lit rim | `#406CE8` L 0.176 → `#7FACFF` L 0.412 — the rim runs **2.3×** the core | apple-26 |
| accent core → its lit rim | `#FF9417` L 0.425 → `#FFB642` L 0.551 | apple-12 |
| halo well | `#B6D4F1` H209 **S0.24** L0.634, dying to S0.02 within ~30px of a 468px tile | apple-26 |
| stacked slab, own internal ramp | body L 0.931, top rim L 1.000, its own base L 0.614 | apple-13 |
| stacked slabs, across the stack | L 0.931 → 0.359 → 0.202 as they narrow, S 0.01 → 0.30 → 0.54 | apple-13 |
| dark object's shadow face | rgb(29,32,35) H210 S0.17 · rgb(29,34,39) H210 S0.26 — **cool**, not warm | apple-26, apple-08 |

Two of those rows are load-bearing and pull in opposite directions.

**apple-13 is the composition analogue and the trap in one file.** It is three
stacked slabs of decreasing width, each with its own bright top rim — exactly
this tile's construction. And it makes the **widest** slab the brightest and
dissolves the narrowest into the ground. That is the inversion this tile exists
to refuse: narrowest must read as *earned*, not as *faded*. So the four slate
slabs are given **one material with no value ramp down the stack** — a ramp would
say "more is better" — and only width and stand-off vary. The stand-off decay is
what buys the right to invert apple-13's value logic, because it gives the
narrowing a physical cause.

**apple-26 is where "emissive on porcelain" is actually defined**, and it is not
what it looks like. Its accent dot is *darker* than the grey rules beside it. The
emission is carried by two things: a lit rim at 2.3× the core's luminance, and a
low-saturation high-value **halo well** tinting the porcelain around it. That is
why the two named teal registers are not interchangeable here — `#186A73`, the
light register, is the body; `#63C3CC`, the lifted register, is the face that
catches the light. Reversed, it is a pale sticker.

## The sibling collision, and what carries the separation

`report` already owns *stacked horizontal bars on porcelain with one accent
rule*. Checked side by side at 128px in a strip with `shipyard`, `proctor`,
`clarify`, `trawl` and `better-goal`, it is the closest neighbour on the shelf and
it was not one this direction anticipated. What separates this tile:

- **Inverted value.** Dark slate slabs here; pale cards there. At 128px the two
  read as opposite masses, which is the same separation shipyard uses against
  `create-swe-project`.
- **The bars are the objects, not the contents.** `report`'s rules are ruled
  *inside* a card; here each bar is a slab standing at its own height.
- **Opposite accent temperature.** Teal against its warm orange.
- **Nothing is at rest.** `report`'s cards lie flat; four of these five are in the
  air, and the shadows say so.

This is recorded as a known liability rather than as a solved problem: at 128px
the separation is carried by value and by hue, not by outline.

## What the rounds changed

Eight rounds, one edit class each. All of them came from looking at the render and
asking what was wrong with it; three came from the script's own measurements
contradicting what the render seemed to show.

1. **r01, the signature move was absent.** Shadows drawn straight below each slab
   and scaled only by blur: all five read as the same grey smear on the porcelain
   and nothing floated. The one thing the direction is *for* was not in the file.
2. **r02, the slabs were not objects.** 50+26px read as a stripe with a highlight
   painted on it. Raised to 62+32, giving the lit top face a third of the object,
   which is the proportion apple-13's slabs carry. This is also what stops five
   centred bars reading as a **loading skeleton** — a skeleton bar is thin and
   flat; a 94px slab with its own lit top is a physical thing.
3. **r03, cast rather than smeared.** The shadow became a displaced copy of its
   own slab, offset *along the key* down-and-right, so it lands on clear
   porcelain instead of pooling underneath. Both halo wells were re-centred on the
   slab's middle: centred on its base they pooled downward, and the brightest
   softest thing in the tile ended up in empty porcelain pulling the eye off the
   object. The fold between top face and front face got a real AO band — a 2.4px
   hairline had disappeared at 1024 — and the rim light got a falloff instead of
   running at one opacity end to end.
4. **r04, the displacement cost the thing the tile is graded on.** A 94px shadow
   offset 34px down pokes below its own slab, and the countability probe read
   **six** bars at 128px. Traded the vertical component for horizontal — a higher
   key light, the same read — and the shadow slides sideways instead of stacking.
   Back to five, with 11–12 device px per bar.
5. **r05, the accent's fold was a join, not a fold.** It measured 3.43:1 across
   its own fold where every slate slab measures 2.23:1, so its pale top read as a
   mint cap stuck onto a dark body. The body now starts **bright immediately
   under the fold** and deepens from there — apple-06's emissive-from-within tell
   — and the lit face was kept chromatic rather than near-white, per the gel rule.
6. **r06, rubric #7.** The slate lit top faces measured 2.89:1 against the tile,
   under the 3:1 floor, with a third of each slab's area below the bar. Darkened
   ~12% → 3.48:1, which also widened the accent's lit face against the slate ones
   from 1.51:1 to 1.82:1. One constant, paid twice.
7. **r07, the mono-tint check.** Flattened to grey, the accent slab was the
   **palest** mass in the tile — apple-13's inversion, arrived at from the other
   direction. Deepened its body and raised the well, on the reasoning that a pool
   on the ground can say "lit" where an object's own luminance can only say "pale".
8. **r08, the well was painted and then covered.** Its radius (118) barely
   exceeded the slab's own half-width (101), so almost none of it was visible and
   it measured 1.08:1 on a well that plainly existed. Both wells re-proportioned
   off the slab — apple-26's well radius is ~1.9× its dot's — and squashed to
   ellipses, because a circular pool around a 202×94 slab either misses the sides
   or floods above and below.

**Three things worth carrying back into `material-recipes.md`** (not written there
from this session — the commission was scoped to this directory):

- **Stand-off is a shadow's *displacement*, not its blur.** Scaling blur and
  opacity with height produces five smears that all read as contact. Offsetting a
  copy of the object's own silhouette along the key axis reads as height
  immediately, and it costs no vertical room — which matters, because vertical
  room is exactly what a stack does not have. Keep the offset mostly *sideways*:
  a vertical component large enough to read is also large enough to poke below the
  object and add a phantom element at small sizes.
- **A halo well has to be proportioned off the object it rings, and shaped like
  it.** Twice in this commission the well was authored at a radius that put nearly
  all of it behind the object. For a wide, short object a circular well is wrong
  in both directions at once; squash it. And the well is a *chroma* shift at
  near-equal luminance, so it will not survive a grayscale flatten — do not rely
  on it for variant robustness.
- **When a reference is the composition analogue, check whether it is also the
  inversion.** apple-13 hands over the whole stacked-slab construction and, in the
  same file, the value logic that destroys this tile's meaning. Lifting the
  construction while explicitly refusing the value ramp was the single most
  important decision here, and nothing in the corpus flags it — the file looks
  like a straightforward win.

## Engines

Engine A only, widened to three genuinely different hand-authored takes, which is
the skill's stated fallback. Engines B (media-gen-pro Arrow) and C (media-gen-pro
raster) were **not** run: this commission was scoped to a fixed deliverable list
that admits no alternate-engine files. That is a real cost and it is stated rather
than hidden — the skill's whole premise is that raster takes usually win the
material judgment, and without one there is no material target and no fidelity
loop. `torch` is also absent on this machine, so the loop's gate would have
refused as a degraded tier had a reference existed.

The three takes and their scores are on `audit.html`. The losers are not
throwaways: `icon-A-v1.svg` is the same widths and palette with the stand-off
removed, and it is the evidence that a flat centred stack of rectangles reads as a
bar chart or a signal meter. `icon-A-left.svg` is the shipped material with one
change — the slabs share a left edge instead of a centre line — and it reads
unmistakably as a horizontal bar chart with the shortest bar highlighted, i.e. as
"the smallest value". The centring is a decision, and that take is why.

## Rubric

**11 / 12**, non-negotiables 1–4 all pass. Docked on **#10**: flattened to a mono
tint, the five-slab structure and the landed slab's contact line both survive — so
the *settling* half of the story is not hostage to hue — but the accent's
**emission** does not, because the well is a chroma shift at near-equal luminance.
In grey the narrowest slab reads as the palest rather than as the lit one, which
is apple-13's inversion. Closing it means darkening the slab that has to look lit
in the register that actually ships. It was left, and it is the first thing to
revisit.

Measured on the shipped 1024 render (`python3 build_icon.py`):

```
slate front face vs tile   7.48:1
slate lit top face vs tile 3.48:1
accent front face vs tile  5.63:1
accent lit top vs its face 2.94:1     (slate slabs: 2.59:1 — matched, so the fold reads)
accent lit top vs slate    1.82:1
ink bbox                   (178,186)-(844,856)  666x670, centre (511,521)
object fills               65% x 65% of the tile
32px luminance spread      0.784
16px luminance spread      0.733
countable bars, centre column   5 at 128px (runs 11/12/11/11/8), 5 at 64, 5 at 48, 5 at 32
```

That last line is the direction's own gate and it lives in the build script rather
than in this file, because it is the check the whole thing turns on: a centre
column of the real export, thresholded, counting dark runs. It caught r04's
phantom sixth bar, which no amount of looking at the 1024 render would have.

Layer plan, and why #10 holds as far as it does: `bg` cushion tile and the
accent's wide well · `mid` the five cast shadows, which are the *only* record of
stand-off in the file · `fg` the four slate slabs · `highlight` the accent slab,
its tight well, and the one rim its light puts on the slab above. Identity is
carried by the width schedule and the settle, so a mono tint keeps the mark even
though it loses the emission.

## Other liabilities

- **At 16px the accent's hue is lost.** The tile reads as a dark narrowing wedge
  with visible banding — the silhouette survives, which is what #4 asks — but the
  "which scope was earned" half of the story goes with the teal. Making it survive
  would mean a lighter or larger accent, and both break the "narrowest" read.
  Verified on the actual 16px export magnified, not inferred.
- **Slate H219 and teal H188 are only 31° apart.** Good for palette economy
  (#6 wants ≤2 hue families and this is arguably one), and it costs the accent
  some separation at 32px and below.
- **The silhouette is close to the standard filter/funnel glyph.** Five centred
  bars narrowing downward is a UI-glyph shape. The metaphor is at least aligned
  rather than misleading — a filter narrows too — but it is a category-adjacency
  the depth and the accent have to carry, and at 16px only the shape is left.
- **Three `feGaussianBlur` filters carry the cast shadows, the contact line and
  the wells.** A renderer without filter support shows the tile flat, which does
  not merely degrade it — it removes the signature move entirely, because the
  stand-off lives nowhere else. Verified in `rsvg-convert` and in a browser over a
  local HTTP serve.
- **`build_icon.py` resolves the squircle from
  `plugins/create-mac-icon/assets/squircle-path.txt`**, with a local copy and the
  installed plugin's copy as fallbacks. It does not carry its own copy, so the
  generator is reproducible where it sits but is not self-contained if this
  directory is moved out of the repo.
