# Candidates — where the options come from, and why not three

## The number three was arbitrary, and the panel disagreed about the right one

The predecessor produced exactly three positioning territories, every time, for
every product. It applied three as the *generation* target rather than the
*shortlist* target, and those are different jobs. Generating three means the
first three the model thinks of, and the research on divergent ideation is blunt
about what those are: when 4,000 ideas were over-sampled from one aligned model,
around 95% were semantic duplicates.

**The research panel did not settle on a replacement number, and that is worth
carrying rather than hiding.** One member cited Gruber, MacMillan and Thompson
(*Management Science*, 2008, N = 112 emerging technology firms) finding an
inverted-U between pre-entry opportunity-set size and venture performance, with
2–4 opportunities optimal (p < 0.01), single-opportunity fixation and over-search
both worse. Another searched for a validated optimum specifically for
*positioning candidates*, found none, and said so:
`<MISSING_DATA>No validated optimal number of positioning territories exists.</MISSING_DATA>`
— proposing five generated, three advanced. A third recommended three to five.

The operating rule, with the disagreement recorded in `40-evidence-register.md`:

> **Generate wide under frames. Shortlist 3–4. Always carry the status quo as a
> labelled fifth option.** The Gruber finding supports a bounded portfolio rather
> than an exact count; no study establishes an exact count for this decision.

## Always carry the status quo

Every comparison includes the incumbent position — what the product says today,
or what a competent marketer would write from the product page in thirty seconds
— as a labelled option in the table, not as background. It is the control arm.
A shortlist that cannot lose to doing nothing has not been tested against the
cheapest available choice, and trawl's boss-gate exists for the same reason.

## Sample the axes that have evidence behind them

A shortlist of four that varies only in wording is one option. Vary the axes the
research actually distinguishes:

| Axis | Positions along it | Why it earns a slot |
|---|---|---|
| **Category distance** | existing category → legible subcategory → new category | Moderate discrepancy produces differentiation inside the category; strong discrepancy produces a subtype. The default is a recognisable category or legible subcategory with a sharp point of difference. |
| **Value basis** | feature → functional outcome → economic/risk outcome → user identity | Benefit-based and user-based positions generally outperformed feature-based positions in controlled comparison, though no type won on every dimension. |
| **Target specificity** | broad ICP → underserved segment → urgent situation or job | The beachhead axis. Narrow enough to be reachable through a specific channel. |

Reserve **at most one slot** for the new-category hypothesis, and label it as the
expensive one. Historical analysis of ~500 brands across 50 categories found 47%
of pioneers failed and surviving pioneers averaged ~10% share, while early
leaders entering roughly 13 years later failed ~8% of the time and averaged ~28%.
The counter-claim that category kings capture 76% of category value is
conditional on first selecting dominant survivors — it is a description of
winners, not a success rate. Both go in the evidence register; neither settles it.

## What every candidate must carry regardless of axis

- a **competitive alternative** it displaces, including at least one that is not
  software;
- a **proof or mechanism** for the claim;
- **deliverability**, bound to the truth ledger;
- and **economic value** to the customer, stated in their units.

Favorability without differentiation is not positioning, and differentiation
without credibility is not either.

## Generate with trawl, under positioning-shaped frames

Route candidate generation through `/trawl:trawl` at standard tier. It exists to
solve exactly this problem — isolated parallel frames, explicit differentiation
against a frozen baseline, mechanism-level clustering, and a boss-gate that
makes the winner beat the obvious answer or openly recommend the obvious answer.

**Freeze the baseline first.** The baseline here is the positioning the product
has today, or, where it has none, the position a competent marketer would write
in thirty seconds from the product page. Write it verbatim. Every candidate must
differ from it in *category frame, named enemy, or beachhead* — not in wording.
A candidate that differs only in adjectives is the baseline with a new coat.

**Fill the five seats with positioning-native personas.** Trawl's portfolio
shape, instantiated for this job:

| Seat | Persona for a positioning run | What it is there to surface |
|---|---|---|
| **Ordinary stakeholder** | the person who lives with the consequence of the current position — the founder who repeats the pitch forty times a week, the AE losing the same objection, the support lead answering the same confusion | the position's felt cost, which never appears in market research |
| **Operational constraint** | the buyer with no budget line for this category, or ninety seconds of attention, or an incumbent contract with eighteen months left | positions that survive a real purchasing reality rather than an ideal one |
| **Adversary** | the strongest competitor's head of product, briefed to take the intended position first, or to make it sound ridiculous | which positions are defensible over twelve months and which are borrowed |
| **Cross-domain mechanism** | a named mechanism from outside software — the assay office's hallmark, the pilot boat, insurance underwriting, a maître d's seating plan — mapped onto the product and told where the analogy breaks | category frames nobody in the category has used |
| **Wild seat** | deliberately unfit, exempt from fit judgment | the reframe that looks wrong until it does not |

The adversary seat is the highest-yield one here and the one a generic ideation
pass skips. A position a competitor can occupy next quarter is not a position;
it is a head start, and it should be labelled as such in the territory file
rather than sold as a moat.

**Personas are one sentence and ordinary.** The finding trawl is built on is
that one-sentence *ordinary* occupational personas partition knowledge better
than celebrity or exotic ones. "A night-shift support lead at a 40-person
logistics SaaS" beats "Steve Jobs".

## Shortlist on distinctness, never on a score

Cluster the candidates by **mechanism**, not by theme. Two candidates belong to
one cluster when they would produce the same hero line under different words.
Then take at most one per cluster, and check the shortlist against four axes —
a shortlist that shares any of these is not three options, it is one option and
two decoys:

- **the word owned** (Ries & Trout)
- **the named enemy**
- **the category frame** (Dunford)
- **the beachhead** (Baker)

`positioning_lint.py` checks that four-way distinctness mechanically across the
territory files, because "genuinely distinct, not three flavours of one idea"
was a prose instruction in the predecessor and prose instructions about
distinctness are the ones a model most reliably satisfies in appearance.

## Name the candidates before the research runs

This is the ordering that makes the research worth buying. A panel asked "what
should this company's positioning be" returns a survey. A panel asked "here are
four candidate positions; find the evidence that discriminates between them"
returns a decision.

So candidate generation comes *first*, and the candidate names go into each
panel's `decisionContext` and into the brief itself. The predecessor got this
right in one line — *"name the candidate positions explicitly so Gemini tests
them"* — and then generated the candidates after the research came back, which
inverted it.

## What gets cut, and where the cuts go

Every candidate that does not make the shortlist gets one line in
`candidates-cut.md`: the candidate, the axis it duplicated or the evidence that
killed it, and who killed it (a frame, a panel finding, the ledger). Two reasons
this is not bookkeeping:

- A founder's first question about a shortlist of three is nearly always "did
  you consider X" — and X is usually on the cut list with a reason.
- A cut made on missing evidence is a research question, not a dead end. When
  the panel could not separate two candidates, that is the thing to say, and it
  is what the pre-commitment test in `decision-aid.md` is for.
