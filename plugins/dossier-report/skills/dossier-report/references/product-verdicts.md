# Product verdicts — categories, top threes, and one winner

When the question is *which one should I get*, a page that surveys the
field and stops has not answered it. This file is the contract for the
recommendation layer: which categories exist, three ranked picks in each,
and one overall winner with the reasons written out.

It applies whenever the research is about choosing between things people
can actually acquire or adopt — hardware, appliances, software, models,
services, vendors, plans. Signals in the brief: *best*, *which*,
*compare*, *shortlist*, *worth it*, *should I buy*, *recommend*, *versus*.

## The failure this prevents

A panel returns 200 sources on eight vacuum cleaners. The page renders
eight sections, one per machine, each with its specifications, its
strengths and its weaknesses, all cited. Every gate passes. The reader
leaves without knowing what to buy.

That page is a survey wearing a recommendation's clothes. It is the
default output, because ranking is the one part of the work that cannot
be lifted from any single source — it is a judgement assembled from the
whole corpus, and assembling it is the only part that is actually yours.

The second failure is subtler and shows up in the tidy version: a
recommendation set where every category has exactly three picks, every
pick has exactly three pros and three cons, and the overall winner is
whichever product the corpus mentioned most often. Symmetry is the tell.
Real fields have categories with two credible options and categories with
six, and frequency in a corpus measures marketing spend and SEO
saturation, not quality.

## The shape of the verdict

Three artifacts, in this order, and the first one is the one most runs
skip.

### 1. Categories, derived from how buyers actually differ

Name **3–6 categories**, each with a one-line statement of who it is for.
A category is a *different reader with a different constraint*, not a
price band and not a spec-sheet heading:

> **The one to buy** — no unusual constraints, wants it to work for years.
> **Small flat, no storage** — under 30cm folded, weight matters more than suction.
> **Allergies** — sealed filtration is the binding requirement; noise is not.
> **Cheapest that is not a false economy** — the floor below which the thing fails at its job.

Derive the categories from the corpus, not from a template. If the
evidence keeps separating machines on a dimension the brief never
mentioned — repairability, subscription lock-in, whether the app is
required — that dimension is a category, and finding it is the most
valuable thing this phase produces.

**A category the corpus did not examine does not ship.** If nobody tested
for cat hair, there is no cat-hair category, however obviously a reader
might want one. Say that the gap exists instead; a named gap is useful and
a fabricated category is not.

### 2. A top three in each category

Ranked, not a set. Each pick carries:

| Field | What it holds |
|---|---|
| `rank` | 1, 2 or 3 — or a declared tie |
| `pick` | the thing, named as a buyer would search for it |
| `bestAt` | the one sentence naming what it wins on |
| `cost` | in the currency that matters here — money, and also setup time, lock-in, running cost, licence terms |
| `basis` | the claim ids the ranking rests on |
| `wouldChange` | what would move it down: a use case it is wrong for, a price move, a firmware regression |
| `runnerUpAdvantage` | the genuine thing rank 2 does better than rank 1 |

`runnerUpAdvantage` is not a courtesy. A ranking with nothing good to say
about the runner-up is a ranking that did not compare them — and it is the
field that most often exposes a pick assembled from one enthusiastic
review rather than from the corpus.

**Fewer than three is a legitimate answer.** Two credible options and a
sentence saying the third is not close beats padding the list with
something you would not recommend. Say `"only two qualify"` and why.

### 3. One overall winner, with the reasoning written out

The winner is a **separate decision from the category winners**, and it is
allowed to be none of them — the machine that wins no category can be the
one that is second in five. State which it is, and write the summary of
reasons as prose a reader can disagree with:

> **Overall: the Miele C3.** It wins the allergy category outright and
> comes second in three others, which is the shape you want when you do
> not know which constraint will bind in three years. It is not the
> cheapest, and the bagless picks beat it on running cost — but bags are
> the reason its filtration holds, so that cost is buying the thing it
> wins on. Against the Dyson: better filtration, worse on stairs, and a
> decade more service history.

Three rules keep the winner honest:

- **It names what it loses on.** A winner with no stated weakness is a
  product page.
- **It says what would change it.** A recommendation with no conditions
  is a recommendation that has not been thought about.
- **"No overall winner" is publishable.** Where the categories genuinely
  do not resolve to one — the field splits on a constraint with no
  dominant side — say so and say what the split is. Forcing a winner to
  satisfy a template is overclaiming against your own corpus, which is
  the one form of it this skill has already shipped once.

## A ranking is an inference, so it is marked as one

This is the point where the recommendation layer meets the claim graph,
and it is not a formality. Every measured fact behind a pick is a
`direct` claim with its source. **The pick itself is assembled by
reasoning across those claims, so it is an `inference`** — it names the
claims it rests on, and it renders on the page visibly as a judgement
rather than as a finding.

```json
{
  "id": "v3",
  "kind": "inference",
  "text": "For a small flat, the Shark HZ400 is the first pick.",
  "from": ["c11", "c14", "c22", "c31"],
  "reasoning": "It is the only machine under 30cm folded (c11) that cleared the carpet-pickup floor (c14); the two smaller units both failed it (c22, c31).",
  "confidence": "medium",
  "limits": "Folded height from vendor spec, not measured independently. Carpet pickup from one lab's protocol.",
  "category": "small-flat",
  "rank": 1
}
```

A reader who disagrees with the ranking can now see exactly which claim
to attack, which is the difference between a verdict and an assertion.
The auditor checks that every pick is `kind: "inference"` with a
non-empty `from`, because a pick rendered as a finding is the strongest
claim on the page wearing no evidence.

## Paywalled labs are evidence, and good evidence

Which?, RTINGS, Consumer Reports, Choice, Stiftung Warentest, HTF, Wirecutter's
test notes — these organisations run the tests nobody else runs, and most
of them put the raw numbers behind a paywall. **A verdict without the raw
data is still high-value evidence**, and refusing it because the table is
not reachable throws away the best-controlled testing in the field in
favour of whatever was published for free, which is systematically worse:
affiliate listicles, vendor claims and single-unit review-unit impressions.

How to use them:

- **Cite the verdict as the verdict it is.** "Which? rates it a Best Buy
  and measured the highest carpet pickup in its 2026 group test" is a
  precise, checkable claim about a named organisation's published
  conclusion. It is not a claim about a number you have seen.
- **Say the number is not public.** One clause. `limits` carries it:
  *"Score published; underlying measurements paywalled."* A reader then
  knows what kind of evidence they have, which is all the honesty this
  requires.
- **Name the protocol where the source names it.** "Tested on the same
  carpet at the same fill level across 14 machines" is what makes a lab
  verdict worth more than an aggregate of reviews, and it is usually
  stated in the free portion.
- **Do not reproduce their figures or lift their charts.** Cite and
  describe. Redrawing a paywalled table as your own graphic is
  republishing someone's paid product, and the page does not need it —
  the verdict is the finding.
- **Treat their disagreements the way you treat the panel's.** Two labs
  ranking the same field differently is a finding about the fragility of
  the ranking, and it belongs on the page rather than being resolved by
  whichever one you found first.
- **Recency matters more here than in most research.** A 2023 group test
  of a product line refreshed in 2025 is evidence about machines you
  cannot buy. Stamp the test year on the claim.

What does *not* get this treatment: a vendor's own testing quoted without
a protocol, an affiliate site's "we tested" with no method, and a
retailer's star average, which measures delivery experience as much as
the product.

## Rendering it, per reading

The verdict is the conclusion, so it leads — above the fold, in every
register. What changes is how much apparatus surrounds it.

| | **Primer** | **Brief** | **Technical** |
|---|---|---|---|
| **The winner** | the pick and the single reason | the pick, who it suits, the trade it makes | the pick, the margin, the claims it rests on |
| **Categories** | two or three, named plainly | all of them, each with its reader | all, with the constraint that defines each |
| **Each pick** | name and one sentence | name, `bestAt`, `cost`, runner-up's advantage | full row, `basis` links, `wouldChange` |
| **Ties** | "these two are equally good" | the tie and what separates them for a reader | the tie, and why the evidence cannot break it |

The winner band is not a hero image with a badge on it. It is the pick,
the sentence, the price with its as-at date, and the link to the reasoning
below. A reader who reads only that band should have the answer and know
it is conditional.

**Stamp prices and availability with a date.** A page that says "£389"
with no date is wrong within a quarter and does not know it. `as at 18
August 2026` beside the figure, and the same date in the methods note.

## Visualising a comparison honestly

Route form and colour through `dataviz`, and `visualisation.md` for what
each register gets. The forms that carry a ranked comparison, and the ones
that do not:

- **Sorted bars, one criterion per chart, small multiples across
  criteria.** The plainest thing that works, and it survives the reader
  caring about a criterion you ranked low.
- **A dumbbell or slopegraph** where the argument is a trade-off between
  two axes — price against measured performance, size against capacity.
  This is the form that makes "the runner-up's advantage" visible rather
  than asserted.
- **A dominance table** — picks as rows, criteria as columns, with the
  measured value in the cell and the winner marked. Dull and unbeatable
  for a reader checking their own priority.
- **Never a radar chart.** It encodes area for magnitude, its shape
  changes with axis order, and it makes a product with one strong axis
  look weak. It is the form a comparison reaches for when it wants to look
  thorough.
- **Never a single composite score as the only figure.** A weighted total
  hides the weights, and the weights are the argument. Show the criteria;
  if a composite is genuinely useful, publish the weighting beside it and
  let a reader re-weight it — that is what the Technical register's
  interaction budget is for.

## The review, before it ships

A recommendation set fails if:

- every category has exactly three picks and every pick has symmetrical
  pros and cons — a template filled, not a field assessed
- the overall winner is the product the corpus mentioned most often
- a pick's `basis` is one source, and that source is a review unit
- no pick names what it loses on
- a category exists that the corpus never tested
- the ranking is rendered as a finding rather than as an inference
- prices carry no date
- the page recommends something it also says it could not evaluate
