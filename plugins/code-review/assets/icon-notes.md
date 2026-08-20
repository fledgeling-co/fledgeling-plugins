# code-review icon — what shipped, and what lost

## The concept that shipped

**The Open Column.** A graphite gel slab carrying four faint engraved rows, with
a tall column cut clean through it on the right. The porcelain the slab stands on
shows through the opening, the cut wall is chamfered in vermilion, and light that
got through lands on the ground past the slab's foot.

The signature move is the through-cut: an absence that was machined rather than
one that merely happened. The rows run up to the opening and stop. That is the
skill's coverage ledger with its not-checked column, made physical — the review
that prints its own blind spot rather than letting a skipped check read as a
clean one.

Nothing else in the marketplace has a hole through a solid body. That was checked
against all forty-one existing icons rather than assumed.

## The concept that lost, and what it was better at

**Three Finders On One Seam.** A single hot vermilion seam across the porcelain —
the flagged line — with three chunky graphite wedges driven in from three
different angles, each stopping with its point on the seam, none of them
overlapping or occluding another, the seam unbroken beneath all three. That is
the skill's other distinctive property: many independent finder angles that are
forbidden from suppressing each other.

**It was better at two things.** It is a livelier composition at 1024, with real
diagonal energy where the winner is orthogonal and still. And it says the thing
about *plurality* that the winner cannot say at all: the shipped icon shows one
ledger with one gap, and carries no trace of the many-angles idea.

**It lost on the renders, decisively, and not on the description.** Both concepts
were built in both engines and shrunk. At 16px the wedges collapse into three
indistinct dark smudges and the seam thins to a single warm pixel row; at 1024
the fat tapered shapes read as exclamation marks rather than as probes, which
inverts the tone from careful to alarming. It scored 8/12 as a raster and 7/12 as
vector, failing checks 3 and 4, both non-negotiable. The winner scored 11/12 with
1 to 4 clean. Both losing takes are retained in `audit.html` with their scores.

The lesson is the one the recipe library keeps recording: three separate objects
of the same weight have no hierarchy to collapse to, so at small sizes there is
nothing left. One object with one event in it survives.

## What the measurements said, and where they were overruled

Four scored rounds ran against the raster take with the full metric tier engaged
(torch and lpips installed into a scratch venv — the system Python is
PEP 668 managed and was left alone).

- **r02 was accepted**, +0.1724 composite across five sizes. It carried the
  measured corrections: the body lightened and neutralised from (41,42,47) toward
  the reference's (55,52,53), the accent's shadow deepened toward the reference's
  measured floor of (151,30,2), the specular re-tinted warm because a pure white
  one over vermilion blew out to (255,255,170), and the through-light glow moved
  underneath the body so it is occluded correctly instead of painted across the
  slab's own foot.
- **r03, r04 and r05 were all rejected**, at every size. r03 added a cushioned
  top-left highlight and an inner occlusion ring together; r04 and r05 split it
  into one edit each and both still lost, the cushion by -0.0736 and the inner
  ring by -0.0164. The reference's body is darker and flatter than either
  instinct wanted.
- **The blind panel could not settle it.** cursor-agent's judge failed to run, so
  an out-of-family substitute was used and reported as one: gpt-5.6-sol at high
  effort, asked in both presentation orders. It picked the candidate in one order
  and the baseline in the other, which the panel protocol records as a tie rather
  than as support. The in-family Claude judge preferred the candidate and is
  excluded from the majority by the self-preference rule.
- **So the gate stood.** Three consecutive non-wins after a promotion exhausts
  the loop's patience, and what ships is the best take the measurements ever
  promoted rather than the last one authored. The rollback is bit-identical to
  r02 by render hash. `SLAB_CUSHION` and `SLAB_INNER_AO` are left in
  `build_icon.py` as named zeros so the finding survives.

Composite against the raster tops out at 0.57 at 1024, and that is expected
rather than a shortfall: the raster is tilted in three-quarter perspective and
the master is orthogonal, so structural agreement is capped by a deliberate
difference. The raster is the material target, never the structural one.

## The shelf decision

`shelf_check` puts this tile at **0.667** structure correlation against
`mockup-fidelity`, its nearest of forty. That is above the 0.633 of one known
real duplicate and below the 0.80 threshold the script flags, so it is a prompt
to look rather than a verdict. Looked at: rendered at 16px beside
`mockup-fidelity`, `tui-craft`, `agent-voice`, `test-campaign` and
`atlas-publish`, this reads as a dark tile with a bright warm slot through it,
against a warm square behind an olive square, a dark panel with a tiny warm dot,
two warm strokes on dark, a nine-tile grid, and a letterform against a bar. No
collision. The pair to re-check is `code-review` and `mockup-fidelity` if either
is ever revised.

`test-campaign` is the closer call semantically and does not show up in the
metric at all: it already owns "a grid with one blank cell", which is the obvious
way to draw a coverage gap. That is precisely why the absence here is a hole cut
through a solid rather than a tile left out of a grid.

## Known liabilities

**Check 10, variant robustness, genuinely fails.** The identity is a void that
reads brighter than the body around it, so it is hostage to a light ground.
Invert the register and the hole reads as a filled panel, which is the opposite
of what it means. Survivable here because every icon in this marketplace is a
decorative PNG with no compositor downstream and only the Default variant ever
renders — but it would have to be redrawn before this became an Icon Composer
package.

**The chamfer's own boundary is weak on its shaded face**, 1.48:1 against the
body at the bottom of the cut. It survives on the seat edge re-stroked over it
and on the aperture floor's 5.76:1 against the body, not on the accent's own
contrast. Body to ground is 8.00:1 and the greyscale delta across the opening is
137, so the tile survives desaturation.

**The material is close to the raster but not equal to it.** The raster body is
rounder and its contact shadow deeper, and two attempts to close that gap were
measured and rejected. Anyone reopening this should re-score rather than trust
the instinct, because the instinct has now lost three times.
