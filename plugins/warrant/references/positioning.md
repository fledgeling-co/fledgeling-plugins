# Positioning — where the machine's answer sits relative to the human's

Read this before building any surface where a person will see a machine verdict. It carries the
strongest evidence in the corpus, and the design rule it produces cuts against the cheapest thing to
build.

## The evidence

Computer-aided detection in mammography is the closest thing to a natural experiment for what this
plugin does: an accurate automated aid, deployed at scale, alongside expert human readers.

After it was introduced across 43 facilities and 429,345 mammograms, specificity fell from 90.2% to
87.2%, positive predictive value from 4.1% to 3.2%, the biopsy rate rose 19.7%, and the area under
the operating-characteristic curve fell from 0.919 to 0.871 — with no statistically significant
sensitivity gain (`C7`).

Then, in 323,973 women, digital screening with the same class of aid showed no accuracy improvement
on any metric. And among radiologists who read both with and without it, sensitivity was
significantly **lower** with the aid, odds ratio 0.53 (`C8`).

Both studies are observational rather than randomised. The within-radiologist comparison in the
second is the sharpest number in the whole corpus, because it compares a reader against themselves
and so removes the obvious confound.

## What it does and does not mean

**It is not evidence that automated verification is harmful.** Both papers are routinely miscited
that way. What they measure is the effect of *where the automated output sits in the human's
workflow*: the aid's output was present before the reader formed their own judgement. That is
concurrent-read positioning, and it is the arrangement that produced these results.

**Sequential-read designs are not covered by either study.** A blind first pass followed by a reveal
is the defensible form, and "blind throughout" is the conservative one. Neither is measured here, so
the plugin takes the conservative option and says why.

## The rule

**Where a human looks at a sampled item, they look blind (`I5`).**

`blind_queue.py` enforces it mechanically: the queue it writes carries no verdict field, and the
script asserts that before writing rather than trusting the caller. A queue that would leak a verdict
exits 2.

This cuts directly against the cheapest possible build. Pre-populating a reviewer's queue with the
machine's verdict and asking them to confirm it is a few lines of work, feels like a courtesy to the
reviewer, and is the one arrangement this evidence forbids. The audit exists to measure the machine;
a reviewer who has seen the verdict is no longer measuring anything.

## What leaks a verdict without looking like it

Six channels, all of which have to be closed for the queue to be blind. The first two are obvious and
the rest are the ones that survive a review:

- a verdict field in the queue payload
- a colour, icon or badge derived from the verdict
- **ordering** — a queue sorted by verdict, or with failures grouped, carries it in the sequence
- **the sample itself** — if only machine-failed items are sampled, membership is the verdict
- filenames, directory names or ids that encode the outcome
- a linked artefact whose first line is the verdict

Seeded known-bad items are the counterweight to the fourth. They are what makes a blind sample say
something about reviewer sensitivity rather than only about the items the machine already doubted,
and their rate lives in a side file rather than in the warrant because a reviewer who learns the rate
stops being blind.

## Where the machine's answer may appear

After the human's pass is recorded, and in the ledger. Not before, and not beside.

For a reviewer working through a lot, that means the interface records their judgement first and then
may show what the machine said — which is also the only ordering under which a disagreement is
informative, because it is the only one where the two judgements were formed independently.
