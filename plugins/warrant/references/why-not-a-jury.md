# Why not a jury

Read this before adding a lane. It carries the measurement that makes a voting panel a bad buy, the
three roles that are worth paying for, and the test that tells them apart.

## The measurement

Nine frontier judges drawn from seven model families supply about **two effective independent
votes**. Panel accuracy falls 8 to 22 percentage points short of what genuinely independent voting
would give. The best single judge matches or outperforms the full panel across every tested
condition. And established aggregation methods close at most 11% of that gap even when handed the
correct answers (`C2`).

Two bounds on it, both stated because the conclusion rests on them. It is a preprint, and it was
measured on natural-language inference and RewardBench rather than on software acceptance, so the
transfer is an assumption. The direction of the assumption's risk is favourable: if it is wrong,
`warrant:panel` is more frugal than it needed to be.

The older half of the same lesson is not about models at all. Twenty-seven independently developed
versions of one specification, run under about a million tests, failed correlatedly, and the
hypothesis of independent failure was rejected (`C3`). Independence is a property you demonstrate,
not one you get by using different suppliers.

## What the measurement does not say

It says nothing against multiple models. It says something quite narrow: **aggregating several
judges' answers to the same question buys much less accuracy than the count suggests.** Three
patterns sit outside that finding entirely, and two of them are worth money.

## The three roles

### One grader, out of family

A single accountable verdict, produced by a family other than the one that built the work.

The out-of-family requirement is not an accuracy argument either, which is the part most often
misread. Author-judged acceptance is how roughly half of a 110-ticket corpus shipped
not-as-specified while reading as complete (`C24`). One grader that did not write the code fixes
that. A second grader that also did not write the code does not fix it twice, and by `C2` it does not
meaningfully raise accuracy either.

So: one. Adding a second grader on the same question is the purchase this document exists to stop.

### Lens lanes, on orthogonal questions

This is where extra models earn their cost. "Does this figure tie to its source", "does this screen
match the mock", "does this leak across tenants" and "does this omit something the spec required" are
different propositions. The lanes are not voting; they are dividing the work, so there is no
correlated-error problem to inherit from `C2`.

Two rules keep the category honest, and both are testable:

- **A lens whose question depends on another lane's answer is a second vote wearing a lens's name.**
  If lane B needs lane A's verdict to answer, they are grading the same thing.
- **A lens whose question a script could answer belongs in `warrant:oracle` instead.** A lens costs a
  model call per item forever and can reversion; a script costs nothing per run and cannot. Moving a
  check out of the panel is always the better trade when it is available.

### An adjudicator over disagreement, routing rather than deciding

When two lanes conflict, majority logic is precisely the failure `C2` measures. The adjudicator's job
is to decide **which deterministic check would settle the disagreement**, run it, and record the
answer. It is the software equivalent of stopping the argument and going to look at the artefact.

The evidence that this role earns its keep comes from the corpus's own construction. The one
contaminated lane in the research panel — the run that read its siblings' reports instead of doing
its own work — was useless as corroboration and useful as a cross-check: four of its discards were
confirmed against the primary reports, including a misattributed journal byline and a
transfer-effectiveness figure traced to a missile-aerodynamics paper (`M4`). **Catching another
lane's mistake does not require independence from it.** That asymmetry is what makes an adjudicator
worth running even where a second grader is not.

## The test for a proposed lane

Four questions, in order. A lane that fails any of the first three is not a lens.

1. Can its question be answered without reference to any other lane's answer?
2. Could a script answer it instead? If yes, write the script.
3. Does it produce a verdict on the same proposition as the grader? If yes, it is a second vote.
4. Is its cost per item, forever, worth what it covers?

## Construction notes

**Keep lane counts even, or a single grader plus lenses.** An odd number invites someone to count
them, and counting is the thing to avoid.

**Add a lens on evidence, not on intuition.** The trigger worth acting on is a defect class that has
produced an escape, recorded in `warrant:feedback`. Adding lenses speculatively is how a pipeline
ends up paying panel prices for single-judge accuracy.

**What the plugin cannot tell you.** Whether two lanes on the same question are genuinely more than
one reader is measurable — a Kish-style effective reader count over paired verdicts on a labelled
set — and this plugin does not measure it, because the reader study that would supply the labelled
set was cut. So the one-grader default is a decision taken on `C2`'s number from a different domain
rather than on a local measurement. If a second grader ever looks necessary, that measurement is the
thing to build first.
