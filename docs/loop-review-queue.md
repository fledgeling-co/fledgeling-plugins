# Loop review queue

Rounds the runner could not settle on its own. Each needs a human look.

## improve-skill r01 (material): gate and panel disagree

The Pareto gate ACCEPTed at +0.1427 net, the largest gain of any round on this
fixture, and the round fixed two real defects: shadows that read blue in a scene
with no cool light, and the icon's brightest ground sitting furthest from its own
key light. It committed as PROVISIONAL because the blind panel did not agree.

- Gate: ACCEPT. 1024 0.3623 to 0.3950, 16px 0.7595 to 0.7748, nothing regressed.
- Panel: no majority on overall, material and silhouette (1-1, one judge failed);
  baseline won small sizes 2-0. Both judges independently described the block
  collapsing toward mid-grey with a weaker accent at 32 and 16px.
- Polarity +0.146 (was +0.177), sign intact. Rubric holds at 11/12.
- The new self-contrast floor does not fire here (2.7% and 1.6% drops against a
  6% threshold); see fidelity-loop.md for why it was not tuned to force it.

**The question for you:** does the warmer, lifted block still read at menu-bar
size? Review sheet at `plugins/improve-skill/assets/loop-runs/r01/review.html`,
or serve it with review_sheet.py. Keep the round, or revert its commit and let
the loop take a different edit class.

## improve-skill r02: implement agent failed to run

`claude -p` exited 1. First 200 chars of its output:

    Prompt is too long

The loop stopped rather than spending iterations on a broken harness.

## improve-skill r02: implement agent failed to run

`claude -p` exited 1. First 200 chars of its output:

    Prompt is too long

The loop stopped rather than spending iterations on a broken harness.
