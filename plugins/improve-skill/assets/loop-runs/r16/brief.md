<context>
You are running one round of a measured icon-fidelity loop. A hand-authored SVG
icon is being iterated toward a diffusion-raster reference until its material
quality matches. Each round makes ONE class of edit, scores the result at five
sizes against the reference, and a Pareto gate accepts or rejects it.

This is round r16 on this fixture. The round's edit class is small-size repair.

Why the loop exists: hand-authored masters reliably win composition and
small-size legibility but lose material richness (volumetric shading, lighting,
translucency, contact shadows) to the rasters. Closing that gap is the work.
</context>

<fixture>
Working directory: /Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets

- `build_icon.py` — the generator. Geometry and material are named constants here; it
  emits `icon.svg`. Every edit goes through this script; never hand-edit the SVG.
- `icon.svg` — the current master (generated).
- `icon-engineC-f5665d-2.png` — THE REFERENCE this round scores against.
- `icon-notes.md` — the decision log across prior rounds. Read its tail first.
- `/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r14/` — the baseline this round is measured against: `score.json`,
  `residual-1024.png` (bright = disagreement), `edges-candidate.png`,
  `edges-reference.png`, `candidate-1024.png`, `reference-1024.png`.
- `measure.py` — split-polarity check; the trued side must read brighter than the un-planed side
- `render_audit.py` — re-renders every take and the three shipped PNGs
- `audit.html` — the contact sheet; the A row is this master's


Do not read these files; they are generated output, they are large enough to exhaust the context window, and nothing in this round needs their text: `icon.svg` (299KB). Judge the artwork from its PNG renders and edit the build script. If you must confirm a fragment, grep it or read a bounded byte range.
</fixture>

<baseline_numbers>
Current master vs the reference:

| size | composite | lum_delta | ssim | edge_f1 |
|---:|---:|---:|---:|---:|
| 1024 | 0.5060 | 0.1274 | 0.6168 | 0.3504 |
| 256 | 0.4716 | 0.1231 | 0.5778 | 0.2513 |
| 128 | 0.5167 | 0.1205 | 0.5560 | 0.4520 |
| 32 | 0.7886 | 0.1165 | 0.5951 | 0.9073 |
| 16 | 0.8362 | 0.1119 | 0.6288 | 1.0000 |

Metric tier: numpy (no torch: luminance+ssim+edges only).

The shape of these numbers is the brief. Where small sizes score well above
large ones, composition has converged and material has not, and the gain has to
come from 1024 and 256.

CONTRAST BUDGET, and it binds. The reference carries LESS contrast than this
master at small sizes, so converging on it lowers yours, and the gate enforces
an absolute floor at 6% below the baseline's:

  32px: your master 0.604, the reference 0.449, floor 0.567
  16px: your master 0.593, the reference 0.427, floor 0.557

This is a real conflict, not a trap: the composite asks you to match the
reference and the rubric refuses to let this icon go mushy at menu-bar size.
Do not spend the round converging ground contrast, and check your p90-p10
spread before you commit to an approach. Gains have to come from something
other than lowering the master toward the reference's flatness.
</baseline_numbers>

<prior_learnings>
Confirmed, measured findings. Apply what fits this round's edit class:

1. Check the dark end's hue, not only the ramp's endpoints. A lit or translucent
   material must keep its SATURATION in shadow, not just its luminance; a shadow
   that desaturates reads opaque. Invisible to a range check, obvious to a
   darkest-pixel check.
2. Measure the reference's actual values rather than assuming them. Assumed
   relationships ("the highlight is lighter than its surroundings") have cost
   this loop three failed attempts where the reference had no such relationship.
3. Fade material where no boundary lives, never across one. Copying a
   reference's fade wholesale once dropped a master's figure-ground to 1.02:1.
4. Contact shadows are the highest ratio-of-effect-to-bytes layer.
5. Attitude is a taper, not a lifted copy; keep lifts affine so materials follow
   the geometry for free.

The full recipe table is at /Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/references/material-recipes.md. Read it.
</prior_learnings>

<task>
Make ONE class of edit: small-size repair. In scope: simplifying or strengthening features that alias or smear at 32 and 16px, and only those. Out of scope: anything that changes the 1024 read beyond tolerance.

Start by finding where the gap actually is, from the artifacts rather than from
assumption: open the residual map, the two edge maps, and the candidate and
reference at 1024. Crop and zoom into the regions the residual says are worst,
and sample actual pixel values out of both images wherever a relationship
matters (face luminances, each material's darkest pixel and its hue there, the
ground's local values beside each object). The reference is ground truth for
material relationships, and reading numbers off it beats reasoning about what it
probably looks like.

Run the instrument as you go:

    cd /Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets
    python3 /Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts/fidelity.py structure --candidate icon.svg --max-paths 3000 --max-bytes 350000
    python3 /Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts/fidelity.py score --candidate icon.svg --reference icon-engineC-f5665d-2.png --outdir /Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r16 --label "r16 small-size repair"
    python3 /Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts/fidelity.py gate --candidate /Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r16/score.json --baseline /Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r14/score.json

The gate is the round's verdict, and the harness applies it. If it REJECTs,
LEAVE your candidate in place and report the rejection with its numbers; the
harness reverts from its own snapshot. Do not revert the files yourself: the
harness re-scores independently after you finish, and a reverted file makes it
score the baseline instead of your work, losing the round's real numbers. A
rejected round is a real result; the next round takes a different class. Do not
keep editing to chase an ACCEPT.

This fixture carries an extra invariant. Run it and keep it satisfied:

    python3 measure.py icon.png 33.0 543 604 640

A material edit that inverts the trued/un-planed polarity breaks the icon's signature regardless of what it scores. The declared path envelope (3000 paths / 350KB) is this fixture's: the shaving curl's 96 swept bands are construction, not path soup.


The 12-point rubric holds authority over the gate. The reference itself can fail
checks the master passes, so converging on it can drag the master below the
rubric floor. If a change raises the composite while breaking figure-ground, the
16px read, or the single light model, that change loses. Say so when it happens;
that disagreement is worth more than the point.

Make the material physically right and let the score follow. Tuning constants
against the composite without a physical reason is how this loop breaks, and the
score is a proxy for a judgment a human will make on the render.
</task>

<constraints>
- Edit `build_icon.py` only. Regenerate the SVG and its PNG renders from it.
- You have no git tools and no network; do not attempt either.
- Do not delegate to subagents. This is a single track; spawn none.
- Deliver what was asked, at the scope intended: one small-size repair round on this
  fixture. Make routine judgment calls yourself. If the brief looks mistaken or
  a better approach exists, say so in a sentence and carry on with the round as
  asked rather than quietly widening or transforming it.
- Append a round entry to `icon-notes.md`: what you measured off the reference, what
  changed and why, the before/after table, what it cost. Cover the substance
  without padding it.
</constraints>

<reporting>
Your final message is a plain report of about 200 words: the gate verdict with
the five before/after composites, what you changed and the measurement that
motivated it, whether the rubric score moved, and any construction confirmed
well enough to be reusable (named precisely enough that another icon could
apply it).
</reporting>