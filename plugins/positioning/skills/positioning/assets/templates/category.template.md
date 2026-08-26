# {{PRODUCT}} — Category and competitors

**Source:** {{PANEL_REF}} · Every row cites a claim id. A cell with no citation
reads `<MISSING_DATA>` rather than a plausible guess.

## The category line today

{{CATEGORY_PARAGRAPH}}

**The label buyers use:** {{BUYER_LABEL}} `[{{BUYER_LABEL_CLAIM}}]`
**The label vendors use:** {{VENDOR_LABEL}} `[{{VENDOR_LABEL_CLAIM}}]`
**The gap between them:** {{LANGUAGE_GAP}}

The gap is load-bearing. Where buyers and vendors use different words, the vendor
word is a red ocean and the buyer word is usually the opening.

## Competitor matrix

Built with `research_wide` — entities and fields declared up front, every cell
filled, cited, or explicitly marked uncertain. Asking a prose research backend
for a table returns an essay with no table in it, which is why this is a
different tool rather than a different prompt.

| Competitor | Category line | One-liner | Pricing model | Beachhead | Trajectory (12mo) | Could take our position? |
|---|---|---|---|---|---|---|
| {{COMPETITOR_ROWS}} | | | | | | |

## Where each candidate position is contested

For every shortlisted territory: who else is moving toward it, how far along they
are, and what the head start is worth in months.

| Territory | Who else is moving there | Evidence | Head start | Defensible after 12mo? |
|---|---|---|---|---|
| {{CONTESTED_ROWS}} | | | | |

A position a competitor can occupy next quarter is not a position; it is a head
start, and the territory file says so in its risks section rather than selling it
as a moat.

## Category-label availability

| Candidate label | Status | Evidence |
|---|---|---|
| {{LABEL_ROWS}} | | |

Status is `open`, `saturated`, `owned by <name>`, or `poisoned` (the label carries
a documented negative association). A label that needs explaining fails the
ten-second test regardless of its status.

## Category distance, and what it costs

Where each territory sits on the axis, and the market-education burden that
comes with it.

| Territory | Existing category / subcategory / new category | Months of education implied | Who pays for it |
|---|---|---|---|
| {{DISTANCE_ROWS}} | | | |

Historical analysis of ~500 brands across 50 categories found 47% of pioneers
failed and surviving pioneers averaged ~10% share, while early leaders entering
roughly 13 years later failed ~8% and averaged ~28%. The counter-claim that
category kings capture 76% of category value selects dominant survivors first, so
it describes winners rather than estimating a success rate. Both belong in
`40-evidence-register.md`; neither settles the choice on its own.

## Pricing and packaging signal

{{PRICING}}

Anchor any pricing read to displaceable spend and to documented billing reactions,
never to a desired number. Where the figure came from a survey rather than a
transaction, it carries the hypothetical-bias caveat from
`80-pre-commitment-tests.md`.

## What this could not establish

{{GAPS}}
