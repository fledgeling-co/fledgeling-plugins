# Product verdicts — categories, top threes, and one winner

When the question is *which one should we use*, a report that surveys the
options and stops has not answered it. This file is the contract for the
recommendation layer: which categories exist, three ranked picks in each,
and one overall winner with the reasons written out.

It applies whenever the session was choosing between things the reader can
actually adopt or acquire — libraries, vendors, models, services, plans,
hardware, architectures. Signals in the request: *which*, *best*,
*compare*, *evaluate*, *shortlist*, *should we use*, *versus*, *worth it*.

## The failure this prevents

A session evaluates six queue libraries, benchmarks four of them, reads
the docs of all six. Asked for a write-up, it produces six sections, one
per library, each with its API shape, its throughput number and its
caveats, every figure cited. Every gate passes. The reader closes the tab
without knowing which one to install.

That report is a survey wearing a recommendation's clothes, and it is the
default output — because the ranking is the one part that cannot be lifted
from any single source. It is assembled from the whole evidence trail, and
assembling it is the only part that is actually yours.

The second failure shows up in the tidy version: every category has
exactly three picks, every pick has three balanced pros and cons, and the
winner is whichever option the session spent the most time on. Symmetry is
the tell. Real fields have categories with two credible options and
categories with six, and time-spent measures where the session got stuck.

## This is also the report's ask

The opening box already has to carry one line saying what should happen and
who decides. On a comparison report **the overall winner is that ask**, so
the two are one artifact rather than two competing summaries at the top of
the page. The rules that govern the ask govern it here too: it is sized,
it is owned, and it names the cheapest high-payoff action.

> **Use BullMQ. One afternoon to port the two producers, needs your yes on
> adding Redis to the deploy.**

A winner with no cost and no named decision is a diagnosis, not a
recommendation, and a reader who agrees with you and does not know what to
do next has been handed the same document twice.

## The shape of the verdict

Three artifacts, in this order, and the first is the one most runs skip.

### 1. Categories, derived from how readers actually differ

Name **3–6 categories**, each with a one-line statement of who it is for. A
category is a *different reader with a different constraint*, not a feature
column and not a price band:

> **The one to use** — no unusual constraints, wants it to still be
> maintained in three years.
> **Already on Postgres, no new infrastructure** — the binding constraint
> is the deploy, not the throughput.
> **Highest throughput, willing to operate it** — the ceiling matters and
> the ops cost is acceptable.
> **Cheapest that is not a false economy** — the floor below which it
> fails at the job.

Derive the categories from the evidence trail, not from a template. If the
session kept separating options on a dimension nobody asked about —
operational burden, licence terms, whether the maintainer is one person —
that dimension is a category, and finding it is the most valuable thing
this phase produces.

**A category the session did not examine does not ship.** If nothing was
measured under burst, there is no burst category however obviously a reader
might want one. Name the gap instead; a named gap is useful and a
fabricated category is not.

### 2. A top three in each category

Ranked, not a set. Each pick carries:

| Field | What it holds |
|---|---|
| `rank` | 1, 2 or 3 — or a declared tie |
| `pick` | the thing, named as the reader would search for it |
| `bestAt` | the one sentence naming what it wins on |
| `cost` | in the currency that matters — money, migration effort, new infrastructure, licence terms, operational burden |
| `basis` | the ledger claim ids the ranking rests on |
| `wouldChange` | what would move it down: a use case it is wrong for, a version bump, a maintainer change |
| `runnerUpAdvantage` | the genuine thing rank 2 does better than rank 1 |

`runnerUpAdvantage` is not a courtesy. A ranking with nothing good to say
about the runner-up is a ranking that did not compare them — and it is the
field that most often exposes a pick assembled from one enthusiastic
README rather than from the trail.

**Fewer than three is a legitimate answer.** Two credible options and a
sentence saying the third is not close beats padding the list with
something you would not recommend. Say `"only two qualify"` and why.

### 3. One overall winner, with the reasoning written out

The winner is a **separate decision from the category winners**, and it may
be none of them — the option that wins no category can be the one that is
second in four. State which it is, and write the summary as prose a reader
can disagree with:

> **Overall: BullMQ.** It wins the throughput category outright and comes
> second in two others, which is the shape you want when the constraint
> that will bind in a year is not known yet. It is not the no-new-infra
> pick — it needs Redis, and pg-boss avoids that entirely — but Redis is
> also the reason its throughput holds, so that cost buys the thing it wins
> on. Against Graphile Worker: three times the measured throughput at
> 3,000/min, a heavier deploy, and a much larger community when something
> breaks at 2am.

Three rules keep the winner honest:

- **It names what it loses on.** A winner with no stated weakness is a
  vendor page.
- **It says what would change it.** A recommendation with no conditions
  has not been thought about.
- **"No overall winner" is publishable.** Where the categories genuinely do
  not resolve to one — the field splits on a constraint with no dominant
  side — say so, and say what the split is. Forcing a winner to satisfy a
  template is overclaiming against your own evidence.

## A ranking is an inference, so it is marked as one

This is where the recommendation layer meets the ledger, and it is not a
formality. Every measured fact behind a pick is a `direct` claim with its
locator. **The pick itself is assembled by reasoning across those claims,
so it is an `inference`** — it names the claims it rests on, and it renders
visibly as a judgement rather than as a finding.

```json
{
  "id": "v2",
  "kind": "inference",
  "text": "For the no-new-infrastructure case, pg-boss is the first pick.",
  "from": ["c8", "c12", "c19"],
  "reasoning": "It is the only candidate that needs no service beyond the Postgres already in the deploy (c8) and it cleared the 1,000/min working figure (c12); Graphile Worker also qualifies but its retry semantics differ from ours (c19).",
  "confidence": "medium",
  "limits": "Throughput measured on one workload on a laptop, not on production hardware.",
  "category": "no-new-infra",
  "rank": 1
}
```

A reader who disagrees can now see exactly which claim to attack, which is
the difference between a verdict and an assertion. The auditor checks that
every pick is `kind: "inference"` with a non-empty `from`, because a pick
rendered as a finding is the strongest claim in the document wearing no
evidence.

## Independent testing behind a paywall is still evidence

Which?, RTINGS, Consumer Reports, Choice, Stiftung Warentest and the
equivalent trade labs run the tests nobody else runs, and most of them put
the raw numbers behind a paywall. The same shape appears in software:
a benchmark suite whose methodology is published and whose full dataset is
not, an analyst report with a public summary, a vendor-independent
evaluation quoted in a press release.

**A verdict without the raw data is still high-value evidence.** Refusing
it because the table is not reachable throws away the best-controlled
testing available in favour of whatever was published free, which is
systematically worse: affiliate listicles, vendor claims, and single-unit
impressions.

How to use one:

- **Cite the verdict as the verdict it is.** "RTINGS ranks it first for
  measured latency in its 2026 group test" is a precise, checkable claim
  about a named organisation's published conclusion. It is not a claim
  about a number you have seen.
- **Say the number is not public**, in `limits`, in one clause: *"Ranking
  published; underlying measurements paywalled."* A reader then knows what
  kind of evidence they have, which is all this requires.
- **Name the protocol where the source names it.** "Every unit tested on
  the same rig at the same fill level" is what makes a lab verdict worth
  more than an aggregate of reviews, and it is usually in the free portion.
- **Do not reproduce their figures or redraw their charts.** Cite and
  describe. Redrawing a paywalled table as your own graphic is
  republishing someone's paid product, and the document does not need it —
  the verdict is the finding.
- **Treat their disagreements as findings.** Two labs ranking the same
  field differently says the ranking is fragile, and that belongs in the
  report rather than being resolved by whichever you found first.
- **Stamp the test year.** A 2023 group test of a line refreshed in 2025 is
  evidence about things you cannot buy.

What does *not* get this treatment: a vendor's own benchmark with no
protocol, an affiliate site's "we tested" with no method, a retailer's star
average, and a figure you remember reading.

## Rendering it, per reading

The verdict is the conclusion, so it leads — page one, in every register.
What changes is how much apparatus surrounds it.

| | **Primer** | **Brief** | **Technical** |
|---|---|---|---|
| **The winner** | the pick and the single reason | the pick, who it suits, the trade, the cost and the decision | the pick, the margin, the claims it rests on |
| **Categories** | two or three, named plainly | all of them, each with its reader | all, with the constraint that defines each |
| **Each pick** | name and one sentence | name, `bestAt`, `cost`, runner-up's advantage | full row, `basis` links, `wouldChange` |
| **Ties** | "these two are equally good" | the tie and what separates them for a reader | the tie, and why the evidence cannot break it |

**Stamp prices, versions and availability with a date.** "£389" or
"v4.2" with no date is wrong within a quarter and does not know it. `as at
18 August 2026` beside the figure, and the same date in the methods note.

**The comparison table is page-safe or it is two tables.** A dominance
table is the most quoted block in a comparison report and the most likely
to break across a sheet: `break-inside: avoid` on the row groups, and if it
genuinely cannot fit one page, split it by category rather than letting the
printer choose where to cut.

## Visualising a comparison honestly

Route form and colour through `dataviz`, and `visualisation.md` for what
each register gets and which lane to build it in. The forms that carry a
ranked comparison, and the ones that do not:

- **Sorted bars, one criterion per chart, small multiples across
  criteria.** The plainest thing that works, it survives a reader caring
  about a criterion you ranked low, and it paginates.
- **A dumbbell or slopegraph** where the argument is a trade-off between
  two axes — cost against measured performance, effort against ceiling.
  This is the form that makes the runner-up's advantage visible rather
  than asserted.
- **A dominance table** — picks as rows, criteria as columns, measured
  value in the cell, winner marked. Dull and unbeatable for a reader
  checking their own priority, and it is the block that survives being
  screenshotted into a chat.
- **Never a radar chart.** It encodes area for magnitude, its shape changes
  with axis order, and it makes an option with one strong axis look weak.
  It is the form a comparison reaches for when it wants to look thorough.
- **Never a single composite score as the only figure.** A weighted total
  hides the weights, and the weights are the argument. Show the criteria;
  if a composite is genuinely useful, publish the weighting beside it.

## The review, before it ships

A recommendation set fails if:

- every category has exactly three picks and every pick has symmetrical
  pros and cons — a template filled, not a field assessed
- the overall winner is the option the session spent the longest on
- a pick's `basis` is one source, and that source is a README
- no pick names what it loses on
- a category exists that the session never examined
- the ranking renders as a finding rather than as an inference
- the winner carries no cost and no named decision
- prices or versions carry no date
- the report recommends something it also says it could not evaluate
