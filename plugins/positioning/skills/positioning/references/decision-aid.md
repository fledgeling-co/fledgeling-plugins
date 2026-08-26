# The decision instrument — why the scorer had to go

The predecessor's decision page centred on an interactive *weigh-what-matters
scorer*: the user moves sliders for seven dimensions, the page multiplies and
sums, and the territories re-rank live. It is a good-looking instrument and it
is the single thing in that skill this rebuild had to remove, because all four
research panel members independently identified the family it belongs to as
documented-unsafe for exactly this job.

The rest of this file is what replaces it, and why.

## What the panel found

**Rank reversal.** In sum-normalised weighted models and in AHP's distributive
mode, adding or removing an irrelevant alternative changes the denominator
differentially across criteria and can flip the order of the top two unchanged
options — a violation of independence of irrelevant alternatives, proved by
Belton and Gear in 1983 and re-derived for weighted-sum normalisation as
recently as 2023. Monte Carlo work finds reversal probability rises precisely
when the alternatives are few and their values are close, which is the shape of
every positioning shortlist.

**Splitting bias.** Decomposing one criterion into sub-criteria inflates its
total weight. Weber, Eisenführ and von Winterfeldt measured an attribute at
~0.25 as a single criterion and 0.40–0.48 when split into three. So the person
who drafts the dimension list decides the winner, before anybody moves a slider.

**Range insensitivity.** Evaluators weight on the *conceptual importance of the
word* rather than the actual spread of performance across the options. A
criterion where every territory scores 80–85 gets overweighted; one ranging
10–90 gets underweighted. The UK Treasury's own MCDA guidance says weights must
represent the value of the swing between worst and best observed consequences,
not importance in the abstract.

**Preference construction and anchoring.** People do not retrieve stable utility
functions; they construct preferences in response to the task's structure.
Sliders that start at a default anchor produce weights compressed toward that
anchor, which neutralises the instrument's discriminating power. A 2022
experiment across five elicitation methods found equalising bias in all five.

**Compensability.** A weighted sum lets a strong score on a minor dimension
offset a fatal failure on a major one. "Founder emotion: 5" should never be able
to rescue a territory the company cannot deliver.

**And the honest limit on all of it:** no alternative method has been shown to
pick commercially more successful positions, because strategy choices are rarely
repeated with observable counterfactuals. The panel's own words —
`<INSUFFICIENT_EVIDENCE>`. So the replacement is not a better oracle. It is an
instrument that *exposes* the assumptions the score used to hide.

## What replaces it — seven stages, in order

Build the interactive surface around this sequence. Each stage either eliminates
options or characterises uncertainty; none of them produces a single number.

**1 · Vetoes, evaluated first and non-compensable.** A territory is eliminated,
not penalised, when it fails any of: the product cannot deliver it (bound to a
`shipped` or realistically-shippable truth row), the company cannot be credible
in it, the go-to-market motion it implies does not match the unit economics, or
it violates a stated constraint. Show which veto fired. A veto is the thing a
weighted sum structurally cannot express.

**2 · The consequence table, in natural units.** Every surviving territory, every
decision-relevant consequence, in the unit it actually comes in: expected
conversion as a percentage, CAC in currency, sales-cycle length in days, gross
margin, months of market education required, and the evidence tier behind each
cell. No normalising, no 1–10. The table is the primary artifact; a founder can
read it and disagree with a specific cell, which is the whole point.

**3 · Dominance screening.** Eliminate any territory that is no better than
another on every consequence and worse on at least one. This is arithmetic, it
needs no weights, and it usually removes at least one option for free.

**4 · Even swaps on what survives.** Where two territories each win on something,
ask the trade directly: *how much of consequence X would you give up to gain
this much of consequence Y?* Adjust one to parity, cancel that consequence out,
repeat. The value judgment is made explicitly by the person who owns it, in
units they understand, rather than being encoded as a slider position.

**5 · Rank stability rather than a rank.** If a weighted view is shown at all —
and showing one is reasonable, because people expect it — it is a *sensitivity
display*, not a recommendation. Sweep the weights across the plausible ranges
the user is willing to defend and report **how often each territory comes
first**, not where it lands at one setting. A territory that wins under 90% of
plausible weightings is a finding. One that wins at exactly the default slider
positions and nowhere else is an artifact, and the display should say so in
those words.

**6 · Scenario regret.** Show the loss if the load-bearing assumption is wrong —
if the category takes twice as long to educate, if the sales cycle is double, if
the beachhead is a third the size. The territory that is least catastrophic
across plausible futures is often not the one that is best in the expected one.

**7 · The output may be "no decision".** When the intervals overlap, or the
winner flips across plausible weights, the instrument's answer is: *these are
practically tied on current evidence; here is the one experiment that would
separate them.* A tool that always produces a winner produces a winner from
noise.

## The label the recommendation is allowed to carry

This is the rule that turns evidence quality into something checkable. A
territory may be described as:

| Label | Requires |
|---|---|
| **Recommended** | Every veto cleared, plus at least one revealed-behaviour test and one replication or holdout |
| **Conditionally recommended** | Perception and relative-choice evidence pass; behavioural or delivery evidence still incomplete |
| **Promising hypothesis** | Qualitative, survey, MaxDiff or hypothetical-WTP evidence only |
| **Not recommended** | Fails a veto, loses to the control, fails economics, or depends on an implausibly narrow assumption set |
| **No decision** | Underpowered evidence, or candidates practically tied |

**A skill run that has done desk research and no field test produces "promising
hypothesis" at best.** That is almost always where this pipeline lands on its
first pass, and saying so is not a weakness of the output — it is the difference
between this and a confident deck. Write the label in `00-decision.md` and in
the HTML, in those words.

## Always include the status quo as an option

Every comparison carries the incumbent position — what the product says today,
or what a competent marketer would write from the product page in thirty seconds
— as a labelled option in the table, not as background. Trawl's boss-gate does
the same thing for ideas, for the same reason: a shortlist that cannot lose to
doing nothing has not been tested against the cheapest available choice.

## Pre-commitment tests: the thresholds that make a test real

`80-pre-commitment-tests.md` is generated from this. The numbers below are the
ones the panel supplied; each carries its bound.

**Stated preference is not demand.** A meta-analysis of 77 studies and 115
effect sizes found hypothetical willingness-to-pay exceeded real willingness-to-pay
by 21% on average, and — against the conventional assumption — indirect methods
carried about 10 percentage points *more* bias than direct ones in the full
model. A separate meta-analysis of payment experiments puts the overstatement
nearer a factor of three. **These do not agree, and the disagreement is the
finding**: the direction is certain, the magnitude is not, and any pricing number
derived from a survey travels with that caveat attached.

**Intentions move further than behaviour.** Changing intention by d = 0.66
produced behaviour change of d = 0.36. Purchase intentions predict worst exactly
where positioning work happens: new products, long horizons, category-level
questions.

**Van Westendorp is not a gate.** It measures price perceptions in a vacuum with
no competitive trade-off and no purchase probability; no independent criterion
validity against realised purchase prices was located. Use it to bound an
exploratory range and say that is what it is. Gabor-Granger is exploratory unless
order is randomised and it is calibrated.

**Landing-page tests need the arithmetic done first.** Approximate per-arm
visitors for a two-sided test at 80% power, α = 0.05:

| Control conversion | Worthwhile treatment conversion | Visitors per arm |
|---:|---:|---:|
| 10% | 15% | ~685 |
| 10% | 12% | ~3,838 |
| 5% | 7% | ~2,211 |
| 2.0% | 2.6% | ~13,850 |

A B2B smoke test running 200–500 clicks per variant has power below 0.15. It is
not a weak signal; it is no signal, and it will still produce a winner. Write the
required N and the pass threshold **before** the test runs — a test whose
threshold is set afterwards returns whatever the reader wants.

**And fake doors have a selection problem in B2B**: ad clicks over-sample
curiosity-driven individual searchers, who are frequently not the economic buyer
and never the buying committee. Prefer the highest-friction ethical endpoint
available — qualified application, scheduled call, card-authorised preorder,
refundable deposit, paid pilot — over a click.

**Survey instruments, with their floors.** MaxDiff is scale-free and good for
ranking claims inside a stable frame, at roughly 150–300 per segment (a review of
165 best-worst studies found 65.6% gave no sample-size justification at all, so
common practice is not a standard). Choice-based conjoint captures trade-offs
when respondents see a realistic competitive set, real prices and a none/status-quo
option; the Johnson-Orme `n ≥ 500c/(ta)` rule is a minimum, not a power
calculation. Both are supporting evidence, never a commitment gate.

## What none of this fixes

Better decision architecture does not improve bad criteria or bad evidence. It
makes the dependence on them visible. If the consequence table's cells are
guesses, stages 3 through 7 operate on guesses with more ceremony. That is why
Phase 0's truth ledger and Phase 2's verification gates come first: the
instrument is downstream of the evidence, and it cannot rescue it.
