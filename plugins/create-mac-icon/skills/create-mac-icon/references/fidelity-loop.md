# The fidelity loop — closing a hand-authored SVG against a raster reference

The single most consistent finding across this marketplace's icon commissions:
at equal audit scores, the raster take's *material* (volumetric shading,
lighting, contact shadows, translucency) beats the hand-authored SVG's, while
the SVG wins composition, silhouette and 16px survival. The deep-research
panel (three verified reports, committed in the marketplace's
`docs/deep-research/`) confirmed the mechanism: SVG can express everything the
rasters show — models fail because they author flat paths, and naïve
"look at a screenshot and improve it" loops measurably make output *worse*.
This loop is the structured alternative. Its full evidence base:
`docs/svg-icon-fidelity-plan.md` at the marketplace root.

## When to run it

Whenever a raster take (Engine C) wins the material judgment and the Engine A
master must be rebuilt to match it — which the pipeline requires before
shipping (a flat raster master re-creates rubric failure #10). Also usable
against any raster reference the user supplies ("make the icon look like
this").

## The mechanics

`scripts/fidelity.py` is the deterministic core. Per round:

```bash
python3 scripts/fidelity.py structure --candidate icon.svg          # static gate FIRST
python3 scripts/fidelity.py score --candidate icon.svg \
    --reference engineC.png --outdir runs/r03 --label "round 3: material"
python3 scripts/fidelity.py gate --candidate runs/r03/score.json \
    --baseline runs/r02/score.json                                  # Pareto accept/reject
```

- `structure` runs **before** any render: it rejects `<image>` embeds (the
  base64 mimicry exploit), scripts, missing layer groups, and candidates over
  the complexity envelope (defaults 400 paths / 200KB — raise the flags
  deliberately for programmatic builds, never silently).
- `score` renders both sides at 1024/256/128/32/16 on a canvas the harness
  owns (the candidate's viewBox is never trusted), computes luminance-field
  delta + SSIM + edge F1 + mask IoU per size (plus LPIPS when torch+lpips are
  installed — the JSON's `tier` field records which stack ran), and writes
  `residual-1024.png` + edge maps for the critique step.
- `gate` is **Pareto, not a weighted total**: ACCEPT only if no size's
  composite regresses beyond tolerance and the 32/16px edge floors hold. It
  also rejects edits whose render hash didn't change (oscillation guard).

Interpreting the numbers: small-size composites converge early (composition
is the easy half); the 1024 composite is the material gap. On the calibration
fixture (improve-skill A vs its C1 raster) a well-composed but materially
flat master scored 0.83 at 16px and only 0.45 at 1024 — the loop's job is to
raise the 1024 number without letting the small sizes slip.

## The round schedule — bounded, one edit class per round

| Round | Edit class | Allowed changes | Exit check |
|-------|-----------|-----------------|------------|
| 1 | Coarse structure | Silhouette, centring, object scale, major colour fields | edge F1 at 1024/256 improves |
| 2 | Material | Gradient stacks, opacity stops, blur radii, highlight/shadow shapes | 1024 composite improves, 32/16 stable |
| 3 | Detail | Micro-geometry, texture accents, local control points | residual shrinks in the edited region, nothing regresses |
| 4 | Small-size repair | Simplify/strengthen what aliases at 32/16 | 32/16 gates pass, 1024 within tolerance |
| +N | Only while the gate keeps accepting | One class per extra round | Hard ceiling: 10 rounds total |

Rules that make it converge (each one earned by a documented failure mode):

- **One edit class per round.** Unconstrained edits oscillate; a rejected
  round rolls back to the accepted state and the next round tries a different
  class or a smaller change.
- **Critique from residuals, not raw screenshots.** Read
  `residual-1024.png` and the edge maps beside the renders; name localised,
  non-overlapping defects (silhouette / proportions / layer order / shadow /
  highlight / material / small-size legibility). Score each 0-2 against the
  reference independently — never side-by-side comparison scoring, never 1-5
  scales (both are documented bias sources).
- **Edit the parameters, not the paths.** Author the master through a build
  script (`build_icon.py` pattern: geometry and material as named constants,
  script emits the SVG) so each round is a named parameter change the log can
  record. Free-form path surgery is how masters rot.
- **Two consecutive rejections = stop or branch.** Grinding one scaffold past
  two rejects buys nothing (documented plateau behaviour); branch to a fresh
  scaffold or ship the accepted state with the gap stated.
- **Keep round state on disk** (`runs/rNN/` with score.json per round). Each
  round's editor works from the accepted SVG + the latest residuals + the
  open defect list — not the accumulated conversation (context bloat degrades
  editing quality by round 8-10).

## After the loop — feed the skill

A win is not finished until it is generalised:

1. **Record the recipe.** Whatever material construction closed the gap
   (gradient stack, blur discipline, contact-shadow recipe) gets added to
   `references/material-recipes.md` with the fixture it came from — same
   session, while the diff is fresh.
2. **Keep the trajectory.** The `runs/` directory (candidates, scores,
   accept/reject, critiques) is training data for a future vector model —
   the marketplace plan's Phase 4. Don't delete it; leave it in the
   commission's working directory.
3. **A recurring recipe becomes a build-script default.** If three
   commissions all hand-write the same soft-shadow construction, it belongs
   in the scaffold every Engine A master starts from.
