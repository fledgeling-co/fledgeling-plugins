---
name: lot
description: >-
  Accept a queue of finished items as a lot under a declared risk limit rather than signing each one —
  size the sample from the warrant's tolerable error rate with sequential stopping, build a review
  queue that carries no machine verdict, mix in seeded known-bad items, and report the decision with
  its population. Use on a backlog of items awaiting sign-off, or on a cadence. Every rate it emits
  carries its denominator.
---

# Lot — the queue, under a risk limit

Two bad options and one good one. Signing every item individually is what nobody finishes; promoting
the whole queue at once is not checking. The third way is a century old in manufacturing and in
clinical laboratories: accept the lot under a declared risk limit (`I2`).

## Procedure

1. **Size the sample.**

   ```bash
   python3 scripts/lot_plan.py --root <repo> --lot <n> --lot-id <id>
   ```

   The tolerable error rate comes from the warrant rather than from the invocation, so a run cannot
   quietly loosen it. The plan emits the initial sample size, the sequential stopping rule and the
   escalation path, and shows the arithmetic in the human output so the number can be argued with.

2. **Build the queue blind.**

   ```bash
   python3 scripts/blind_queue.py --root <repo> --items <items.json> --lot-id <id> \
       --seeds <seeds.local.json>
   ```

   The reviewer artifact is built from an allowlist rather than by stripping fields, so a verdict
   cannot reach it by construction. Forcing one through is possible only with `--carry verdict`,
   and that is refused: exit 2, naming every way the field would have leaked, by field name and by
   value. It writes a second file, an operator key at mode 600, holding the seed positions the
   reviewer must not see.

   This is the most important ordering constraint in the plugin. In 323,973 women, digital screening
   mammography with a computer aid showed no accuracy improvement on any metric, and among
   radiologists who read both with and without it, sensitivity was significantly lower with the aid,
   odds ratio 0.53 (`C8`). The earlier cohort across 43 facilities and 429,345 mammograms found
   specificity falling from 90.2% to 87.2%, positive predictive value from 4.1% to 3.2%, the biopsy
   rate rising 19.7%, and the area under the operating-characteristic curve falling from 0.919 to
   0.871, with no statistically significant sensitivity gain (`C7`). Pre-populating the reviewer's
   queue with the machine's verdict is the cheapest thing to
   build and the one thing this evidence forbids (`I5`). `references/positioning.md` carries the
   mechanism.

3. **Mix in the seeds.** Known-bad items at a rate held in a side file rather than in the warrant,
   with the classes rotated. Seeded defects estimate reviewer sensitivity but not prevalence, and a
   reviewer who learns the rate stops being blind.

4. **Census-review two classes rather than sampling them**, both named in the warrant: disclosure
   content, and every item the panel marked `inconclusive`.

5. **Report the decision.**

   ```bash
   python3 scripts/lot_report.py --root <repo> --plan <plan.json> --result <result.json> \
       --review <review.json> --key <operator-key.json>
   ```

   Five required fields, and the script exits 2 if any is absent: the population with its size, the
   tolerable error rate, the sample size, the seed recovery count, and the decision.

## What the numbers can and cannot say

The nearest available human baseline is wide: two evaluators using the same method on the same system
agree on between 5% and 65% of the problems found (`C5`). A sample whose two reviewers disagree is
the expected result rather than a failed run.

Roughly three quarters of what code review finds does not affect visible functionality at all
(`C6`), so a lot audited only on functional defects has been audited on the minority of what a
reviewer would produce. Say which classes the audit covered.

## Output

`lot_plan.py` prints the sample size, the stopping rule, the escalation path and the arithmetic
behind them. `blind_queue.py` writes the reviewer queue plus a mode-600 operator key, and exits 2
if a carried field would leak a verdict. `lot_report.py` prints the five required fields and exits 2
if any is absent.

## Constraints

Never print a bare percentage. Published proficiency-test failure rates differ by more than
twentyfold depending on the denominator — 1.4% of 670,489 challenges across 665 laboratories against
32.4% of lab-parameter results across three, both correct (`C19`) — so every rate travels with its
numerator and denominator.

Take the tolerable error rate from the warrant on every run. A rate passed on the command line is a
risk appetite nobody signed.

Report a seed the reviewer missed as a finding about the review, not about the item. That is what the
seeds are for.
