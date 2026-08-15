# shipyard — icon notes

**What it is.** The marketplace tile for `shipyard`, the feature-delivery stage
plugin: intake → triage → plan → design → work → verify → gap-fix. The icon has
to say *a thing being built, stage by stage*, on a shelf that already owns
several boats.

Deliverables in this directory: `icon.svg` (the layered master, emitted by
`build_icon.py`), `icon.png` / `icon-256.png` / `icon-128.png` (squircle-masked
exports from `render_audit.py`), `audit.html` + `audit-renders/`, and `runs/`
(the fidelity loop's trajectory, one directory per round, each with its
`score.json` and the `build_icon.py` that produced it).

---

## Direction

**Tahoe gel-glass, porcelain sub-register (a)** — a lit object on a porcelain
cushion tile with one bounded warm accent. Runner-up was Direction 1 (Object
Tile), rejected because its Big-Sur candy-gloss grammar reads as previous-era
next to the siblings, and the whole shelf is already committed to the porcelain
cushion.

Ground register is porcelain/daylight, per the family rule. The dark register
belongs to `trawl`. One accent family — ember/amber, kin to `#C4622D` — and it is
spent only on the plank.

**Glyph device** (subject-mined, not category clip-art): a hull mid-build on its
slipway. The stern half is planked into a smooth slate gel skin; the bow half is
still open frames with the porcelain showing between them. Three keel blocks on a
sole plate hold it off the yard floor.

**Signature move — "the next plank arrives lit."** The single strake at the
boundary between the planked and open halves is an emissive ember bar. It stands
proud of the sheer, and its stand-off *decays along its own length* — 30px in the
air at the forward end, 2.5px at the aft end where it has almost landed on the
finished planking. That taper is what makes it read as *arriving* rather than as
a stripe; it is the stage in progress, and it is the only chroma in the tile.

The palette was authored against numbers sampled out of
`references/corpus/apple-2026/`, not out of prose:

| property | sampled | source |
|---|---|---|
| porcelain ground | L p50 0.96, 1.00 top → 0.90 bottom | apple-05, apple-06 |
| contact shadow floor | L 0.88 — shallow and wide, never a dark blob | apple-05, apple-06 |
| warm accent ramp | H 30–48, S 0.39–1.00, V ≈ 1.00, L 0.62 → 0.92 | apple-06 (Home) |
| warm accent, deeper | H 6–36, S 0.63–0.85, L 0.33 → 0.74 | apple-05 (Infuse) |
| dark object's shadow face | rgb(28,36,51), H219 S0.45 V0.20 — **cool**, not warm | apple-12, apple-10 |

That last row is load-bearing and counter to the marketplace's usual lesson: in a
daylight porcelain scene the deep shadow on a dark body reads blue-slate. The
warm shadows recorded elsewhere in `material-recipes.md` came from scenes lit by
an emitter. Here both are true at once, which is why the frames facing the ember
are warmed and every other shaded face stays cool.

## The sibling collision, and what carries the separation

`create-swe-project` already owns *a hull on a slipway going into water* — an
amber canoe on a blue rail over blue water. That is not one of the three
collisions the brief named, and it is the closest neighbour on the shelf. What
separates this tile, checked at 16px beside it:

- **No water, no launch.** Porcelain floor, dry dock, keel blocks. Theirs is the
  moment of launching; this is the moment of building.
- **Inverted value.** Dark slate hull on porcelain here; amber hull on blue
  water there. At 16px the two read as opposite masses.
- **A broken sheer.** The open frames and the gaps between them give this hull a
  ribcage where theirs is a smooth canoe.
- **The accent is a bar, not the body.** Theirs spends amber on the whole hull;
  here it is one lit strake against a dark mass.

This is recorded as a known liability rather than as a solved problem: at 16px
the separation is carried by value and by the ember, not by outline.

## The fidelity loop

Reference: `icon-engineC-b3fcac.png` (Engine C, GPT Image 2, four apple-2026
porcelain exemplars passed as `referenceImages`). It won the material judgment —
deeper hull, a real three-quarter read, frames with cylindrical shading — and
lost the delivery, being a flat pre-masked raster (rubric #1 and #10) whose ink
bbox centres 34px below the tile centre (#2).

Nine rounds, one edit class each. Mean composite across five sizes
**0.6215 → 0.6654**; 1024 composite 0.5377 → 0.5559; the master's own p90–p10
self-contrast **0.379 → 0.678** against the reference's 0.718. Round table and
gate verdicts are in `audit.html`.

**What the loop actually changed:**

1. **r01, coarse structure (+0.2599, the round that mattered).** The draft was a
   flat side elevation. Three changes: the hull deepened from a 3.7:1 crescent to
   a 2.5:1 bowl, the object scaled to 1.08 through one shared group transform, and
   — the volume cue — a **mouth band**: the far sheer drawn as the near sheer
   offset by (+26, −30), with the dark interior between them and a lit far rim on
   top. Self-contrast nearly doubled in one round.
2. **r02/r03, material.** Seams rebuilt as dark grooves (the reference measures
   L 0.04–0.08 at each seam; the draft had paired light/dark lines, which is the
   "highlight is lighter than its surroundings" trap again). The broad 27px sheer
   band became a single lit gunwale line at L 0.58. Per-frame cross-section
   gradients replaced one shared vertical ramp. Both rounds gated REJECT; a blind
   Claude judge preferred r03 on overall and material, and the panel outranks the
   gate.
3. **r04, small-size repair.** Plank thickened to 38px so it holds a pixel at
   16px; contact shadow deepened.
4. **r05, detail.** Seam opacity to 0.82, and a **bounce-up** gradient: the
   reference's hull *rises* from L 0.18 to 0.20 at the bilge, which is light
   coming back off the porcelain. A top-lit ramp alone cannot produce that.
5. **r06, detail.** The two angled shores became a slipway sole plate — they were
   reading as detached grey ticks at 32px. The plank's aft end gained a taper so
   it stops being a blunt cut.
6. **r07, small-size repair.** The blind panel, shown only renders, said the 32px
   version "collapses into an ambiguous dark tub with the ribs and pale cradle
   lost". Measured cause: frames ~26px on ~14px gaps, where the reference runs
   ~40px frames on ~30px gaps — at 32px our gaps were half a pixel and filled in.
   Six frames became four on a 62px pitch, and the cradle dropped a step down the
   value ramp. 32px composite +0.0105, 16px self-contrast +0.012. Gated REJECT on
   a 0.0064 regression at 256px, which is a similarity loss from having four
   frames where the reference has six.
7. **r08, grid.** The ink bbox measured (530, 521), not (512, 512). Moving it
   regressed every size, because the reference's own bbox centres 34px low —
   rubric #2 is non-negotiable and the reference fails it, so the rubric won.
8. **r09, family.** The ground had come out of the corpus neutral-cool,
   (247,248,249) → (229,232,237). Every sibling on this shelf runs warm and
   R>G>B — proctor (245,241,234) → (226,209,191), report (251,249,245) →
   (239,232,220), mac-doctor (252,251,249) → (234,228,219). Warmed to
   (247,246,242) → (231,228,218), which costs 0.016 of composite against a
   reference whose ground is cool and is what makes the tile belong to the set.
   The corpus is right about Apple's tiles and wrong about this shelf.

**Three things worth carrying back into `material-recipes.md`** (not written there
from this session — the commission was scoped to this directory):

- **The mouth band.** For any vessel or container object seen slightly from
  above, draw the far rim as the near rim's offset copy and fill the gap with a
  dark interior ramp. One offset, three paths, and it is the difference between
  an elevation and an object. It bought more self-contrast in one round than
  every material round after it combined.
- **An emitter's spill is a falloff from the emitter, not a curtain over
  everything it might touch.** The r02 reject authored the ember's bounce as a
  vertical gradient clipped to *every* frame, which washed the whole open bay
  warm and spent the accent on decoration (rubric #6). Replacing it with a radial
  centred on the bar, at r=200, warms the two frames the bar actually faces and
  nothing else. The composite barely moved; the blind judge named it immediately.
- **A repeating array's pitch is a small-size parameter.** Gaps narrower than one
  rendered pixel fill in, and the array becomes a solid mass. Count the gap in
  device pixels at 32px before choosing how many members to draw.

## Rubric

**11 / 12**, non-negotiables 1–4 all pass. Docked on #7: the cradle measures
1.56:1 against the tile where the hull holds 8.34:1 and the frames 9.98:1, so
it dissolves by 32px and the hull can read as floating. Darkening it further puts
a second dark mass under the object; it was left, and it is the first thing to
revisit.

Measured on the shipped 1024 render (`python3 render_audit.py`):

```
planked hull vs tile   8.34:1
open frames vs tile    9.98:1
ember plank vs hull    3.26:1
cradle vs tile         1.56:1
32px luminance spread  0.855
16px luminance spread  0.851
```

Layer plan, and why #10 holds: `bg` cushion tile · `mid` floor shadow, sole plate
and keel blocks · `fg` backbone, far-side frames, mouth, near frames, planked
skin · `highlight` the ember plank and everything its light touches. Identity is
carried by the hull's mass and the value break at the plank, so a mono tint keeps
the mark.

## Other liabilities

- The fidelity gate rejects the shipped state at 1024 and 256px against C1. Those
  are registration losses against a reference whose own composition fails rubric
  #2; recorded rather than resolved.
- The master depends on three `feGaussianBlur` filters for its bloom and contact
  shadows. A renderer without filter support shows it flat. Verified in
  `rsvg-convert` and in a browser via a local HTTP serve.
- Engine B produced two takes, both scored in the sheet and neither salvaged
  structurally. The second (`-1a7fde`) contributed one idea: the plank crossing
  the frames at a visible angle, which the master expresses as a decaying lift
  rather than a rotation.
