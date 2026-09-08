# EVALS: atlas-review

**No comparison against the no-skill baseline has been run.** This section says so first
because a missing evals section reads to a later reader as though the pipeline ran and
passed. It did not run, and inventing numbers would be the exact failure this skill is built
to catch.

## What was verified

- **Every rule traces to a source.** Field findings carry a figure and a citation in
  `references/evidence.md`, drawn from the research panel exported to `docs/deep-research/`.
  Atlas-specific measurements are labelled as measurements from one repo rather than as
  general findings.
- **Every file passes the voice gate.** `voice_lint.py --format review` is clean on the hard
  checks for SKILL.md and all eight references, which is the same gate the skill imposes on
  its own output.
- **SKILL.md is 157 lines**, inside the convention that depth belongs in references.
- **The composition is real.** Every skill named in the routing table is installed, and each
  is called for the thing it already owns rather than reimplemented.

## What has not been verified

- **That the skill beats not having it.** The honest comparison is the same task with no
  skill loaded, graded on structural assertions by an independent judge, then a blind panel
  on anonymised pairs. Neither was run.
- **That a fresh session follows the nine stages in order.** The stages come from the product
  owner's own description of what they ask for, so the order is an instruction rather than a
  finding, but nothing has tested adherence.
- **That the mutation rule is affordable in practice.** It is well grounded as a detector,
  and its cost on a large diff has not been measured here.

## The three tasks that would settle it

1. Hand a fresh session a real Atlas pull-request stack with no skill loaded, and the same
   stack with it. Grade both on: did it fix what the review found, did it gate the merged
   tree, did it prove a touched test can fail, did it act on the owner's notes.
2. Plant one unfailable check of each shape in `references/void-checks.md` in a branch and
   measure how many each arm finds.
3. Plant a semantic conflict that is clean textually and green on both branches, and see
   which arm catches it.
