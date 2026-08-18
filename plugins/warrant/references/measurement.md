# Measurement — the arithmetic, and the number that lies

Read this before reporting any number out of this plugin. Most of it is one rule applied in five
places.

## The rule: a rate never travels without its population

Published proficiency-test failure rates for the same kind of testing differ by more than twentyfold
depending on what was counted: 1.4% of 670,489 challenges across 665 laboratories, against 32.4% of
lab-parameter results across three hospital laboratories (`C19`). Both figures are correct. The
difference is the denominator.

That is the shape almost every misleading number out of a verification pipeline takes, so it is
enforced mechanically rather than left to judgement:

- `_cli.rate()` renders a percentage with its numerator and denominator or refuses to render one.
- `lot_report.py` exits 2 if the population is absent from a report.
- `escape_report.py` refuses to print a rate at all, and exits 1 with the reason if asked.

## Risk-limited lot acceptance

`lot_plan.py` sizes a sample from a declared tolerable error rate with sequential stopping: a clean
early sample ends the audit, a dirty one escalates it. The tolerable error rate comes from the warrant
rather than the command line, because a rate passed at invocation is a risk appetite nobody signed.

Three properties worth understanding before arguing with a sample size:

- **The sample bounds the lot, not the item.** A passing lot audit says the lot's error rate is below
  the declared limit with the stated confidence. It says nothing about any particular item in it,
  including the ones sampled.
- **Sequential stopping changes the arithmetic.** Stopping early on a clean run is only valid if the
  stopping rule was declared before looking. `lot_plan.py` emits the rule with the plan for that
  reason.
- **Census classes are outside the sample.** Disclosure content and every `inconclusive` verdict are
  reviewed in full, so they neither contribute to nor benefit from the sample's confidence.

## Seeded defects

Seeds estimate **reviewer sensitivity**, not prevalence. A reviewer who recovers 8 of 10 seeds has a
measured recall on seeded classes; the lot's real defect rate is a different quantity and the seeds do
not estimate it.

Two operational rules follow. The seeding rate lives in a side file rather than in the warrant,
because a reviewer who learns the rate stops being blind. And the seed classes rotate, because a
reviewer who learns the classes is only blind to the rate.

## The control chart

`westgard.py` runs a multirule chart over the regression corpus pass rate across runs: 1-3s, 2-2s,
R-4s, 4-1s and 10-x.

The multirule form is not sophistication for its own sake. A single-threshold alarm on a
true-negative-heavy queue either never fires or fires constantly, which is the reason clinical
laboratories moved off one. The rules catch different failure shapes: a single outlier, a sustained
shift, a widening spread, and a slow drift that never breaches a limit.

A drift is the interesting case here, because a corpus pass rate that slides from 100% to 94% over ten
runs never trips a threshold and is exactly what a reversioning model looks like.

## What this plugin does not measure, and would need in order to

Four quantities, named so that nobody reports them by accident:

| Quantity | Why it is absent | What would supply it |
|---|---|---|
| Human verifier sensitivity per defect class | the reader study was cut as self-defeating (`C1`) | a labelled case set and reader time |
| False-rejection rate | an item wrongly failed and never reviewed is invisible | a blind review of machine-failed items |
| Effective reader count across lanes | needs paired verdicts on a labelled set | the same case set as row 1 |
| Escaped-defect rate | feedback is a numerator with no denominator | seeded items at a known rate in production |

The `falsealarm_proxy.py` churn signal is the only one of the four that has even a partial
substitute, and it is a proxy: same evidence digest across a fail and a later pass is suggestive
rather than dispositive.

## Reporting style

State a count as a count. State a rate with both terms. State an absence as an absence — "no escapes
reported in this class" rather than "this class is reliable", because a class nobody has exercised has
produced no evidence about itself either way.

Where a number is an inference rather than a measurement, say so in the same sentence. The plugin's
whole claim to being auditable rests on that distinction holding in the output as well as in the
reference files.
