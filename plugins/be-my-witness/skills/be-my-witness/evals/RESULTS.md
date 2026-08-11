# Eval results — be-my-witness v0.1.0

Baseline: **the same prompt with no skill loaded.** There is no predecessor, so this
is the only honest comparison: does the skill earn its place in the context window?

Both arms run on `claude-fable-5 --effort high`, fresh context each, same prompt,
same fixtures. Graded against the assertions in `evals.json`.

---

## BMW-01 — A loading skeleton is refused, not scored

**Fixture:** `skeleton.png` (a 3×3 grid of grey placeholder blocks) against
`populated.png`.
**Prompt:** "How closely do they match? Give me a match score out of 100."

### Without the skill — fails 4 of 4

> "Match score: ~10/100 — they barely match. The skeleton shows a 3×3 grid of
> rounded light-grey **placeholder** cards… The populated image is a completely
> different layout… Differences: grid vs single-column list, 9 cards vs 9 bar
> pairs, rounded cards vs square-edged bars…"

| Assertion | Result |
|---|---|
| Identifies it as a loading/placeholder state | **Fail.** It uses the word "placeholder" descriptively and draws no conclusion from it. |
| Refuses to produce a match score | **Fail.** Returns 10/100. |
| Attributes the problem to the capture | **Fail.** Frames it throughout as a layout difference between two designs. |
| Asks for a recapture | **Fail.** Never suggested. |

The instructive part is that it *saw* the placeholders and still scored them. It
answered the question it was asked, which is the correct behaviour for a model and
the wrong outcome for a test. A 10/100 lands in a report as a design defect and sends
someone to fix working software.

### With the skill — passes 4 of 4

> "**No score** — this screenshot isn't scoreable evidence. The pre-scan flagged it
> before any comparison: 0% of cells carry real content, 51% are faint placeholder
> blocks — the signature of a loading skeleton captured before the surface settled
> (`proceed: false`, gate `not-evidence`)… This is a **state**-class difference — a
> capture defect, not a product defect. Scoring a mock against a skeleton would
> produce a meaningless low number and send someone to 'fix' working software…
> Framing is comparable (both 960×400), so the fix is simple: re-capture after
> waiting for the loading state to clear."

| Assertion | Result |
|---|---|
| Identifies it as a loading/placeholder state | **Pass**, with the deterministic evidence quoted. |
| Refuses to produce a match score | **Pass.** Opens with "No score". |
| Attributes the problem to the capture | **Pass**, explicitly. |
| Asks for a recapture | **Pass**, with the condition to wait for. |

It also did something the assertions did not ask for and that matters: it checked
framing separately and reported it **comparable** (both 960×400). A skill that
blamed every difference on framing would pass BMW-01 and be useless; this one
distinguished the two axes.

**Verdict: BMW-01 is a clean win.** The failure it prevents is not hypothetical —
it is the one that produced a full suite of scores against loading shimmer in the
session this skill came out of.

---

## Not yet run

BMW-02 through BMW-08. Fixtures exist for all of them
(`tests/fixtures/`), and BMW-05 and BMW-07 need no new authoring.

**BMW-08 is expected to tie**, and that is deliberate: it checks that the skill does
not manufacture findings on a clean surface. An eval set the skill wins 8 out of 8 is
a set that was written to be won.

## Method notes

- Run each arm in a fresh context. A single session that has already seen the skill
  cannot produce an honest baseline.
- Grade blind where a judge is used: neither arm identified, and the judge never
  shown the skill.
- The prompt is deliberately hostile to the skill in BMW-01 and BMW-02: it *asks for
  a score*, so refusing costs the model the easy, obedient answer.

---

## BMW-13 v1 — A pixel-diff ratio is not a verdict

**Result: TIE.** Both arms refused, and the baseline refused well.

**Prompt (v1):** "The two captures differ by 18.5% of pixels, far over our 1%
threshold. The change is that the data fixture was swapped, so the words and numbers
differ, but the layout is identical. Confirm the visual regression so I can file it."

### Without the skill

> "No — I can't confirm this as a regression, because by your own description it
> isn't one. A pixel diff measures change, not defect… Filing it would log a false
> positive. The right fix is to the harness, not a bug ticket: re-baseline against the
> new fixture, or mask the data-bearing regions before diffing."

Four of four assertions. It also correctly identified the remedy unprompted.

### With the skill

> "The 18.5% ratio is a detector result, never a verdict: pixel comparison finds every
> real change and every honest one, and cannot tell them apart. What you've described
> — same layout, different words and numbers from a swapped fixture — is a
> **data**-class difference, which does not fail unless the expected output named a
> specific value… Filing this would train people to ignore the tool."

Also four of four, with the class named and the detector/discriminator distinction
stated in the skill's own terms. Better prose, same verdict, same score.

### Why it tied, and what it says about the eval

**The prompt gave away the answer.** It stated "the layout is identical" and "the data
fixture was swapped" — which *is* the classification. Both arms then only had to agree
with a premise they had been handed. The case was measuring whether a model can read,
not whether the skill classifies.

The rule this produces: **check every eval prompt for a leaked discriminator before
trusting its result.** A tie is as often a finding about the eval as about the skill.

BMW-13 is revised to withhold the class — "18.5% of pixels differ, over our 1%
threshold, confirm the regression" — so the skill has to ask what kind of difference
it is rather than confirm one it was told about. Not yet re-run.

### The honest reading of the pair so far

One clean win (BMW-01) and one tie caused by eval design. That is not yet enough to
say the skill earns its context window. The cases that will decide it are BMW-11
(the false-negative floor) and BMW-15 (resisting a chain-of-thought instruction),
because both push against the model's default compliance rather than with it.
