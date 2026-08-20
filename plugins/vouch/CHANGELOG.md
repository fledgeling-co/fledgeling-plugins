# Changelog

## 0.3.0

A mailbox sweep for transactions the pipeline had missed, and it found the pipeline
reporting one transaction as two different absences. Both new gates come from that.

- **`scripts/cross_check.py`** — the two leftover piles are now checked against each
  other before either is published. Charges with no document and documents with no charge
  read as opposites, and are only opposites if nothing is on both. A supplier printing US
  dollars as a bare `$` beside an Australian GST line was read as AUD, so its receipt went
  to one pile and the charge it settles went to the other; each page was internally
  consistent and neither could catch it. Three rows were absent from the claim on that
  basis. The check pairs on supplier, a few days, and a ratio inside the observed
  conversion band, and it proposes rather than decides: a hit names the file to open,
  because only the document says which of the two figures was wrong. Eval V-20 holds it to
  a fixture that must pair and one that must not.

- **A statement's cycle is a fact about one card.** `wanted_invoices.py` now reads the
  masked card numbers out of the statements at the same time as the dates, and names a
  missing period only for a card those documents cover. A day-16 Amex cadence had been
  printed against a Mastercard whose statements were never supplied, in a sentence
  indistinguishable from a measured one. Rows on an uncovered card are now said, in words,
  to have no statement behind them.

- **The line item is a third account discriminator** (`references/inclusion-rules.md`).
  The invoice prefix separates accounts and the organisation name separates a
  personal-shaped account from a company one; both miss the case where one supplier sells
  two products. A vendor selling a metered developer API and a consumer chat subscription
  settled both through one processor, on the same card, in the same month, under an
  identical card descriptor. Every claimed row was the API. Only the product named on the
  invoice line separates them.

- **`scripts/card_on_document.py`** — a minority of documents name the card that paid
  them, and where they do the inference stops. It is the only check that sees a supplier
  move onto the company's own card: one stated the claimant's Amex for ten months and the
  company's Visa from the eleventh, with identical subscription ids, amount and cadence, so
  from the feed's side the charge simply stopped appearing — indistinguishable from a gap in
  a feed that had real gaps. Two months would have been claimed against money the company
  had already spent. Measured at 11 of 105 documents on a real claim, one in a mask form the
  first pattern missed, so the census prints the forms it read: a narrowed pattern and a
  clean result look the same from outside. Eval V-22 holds it to a document that must be
  refused and one that must not.

- **A supplier's own rows are now checked against each other** (`classify_accounts.py`,
  eval V-24). The census groups by evidence rung, so a supplier whose rows land in two
  places appeared in two blocks with nothing saying they were one supplier — and a supplier
  seen under "a company address appears" reads as settled. It now names every supplier whose
  rows disagree on the rung they reach or the address they name. On a real claim it found
  two, one of which had taken several rounds of human challenge to find by hand. The same
  rule is written down for any system that offers a decision at supplier or merchant level:
  the number to look for is not how many rows agree but what the rest hold, because only
  that separates a supplier nobody has finished from a supplier that is two things.

- **Every count-bearing section is now rendered at zero before it ships**
  (`references/gates.md`, eval V-23). The outstanding set reaches zero on the last run of a
  claim, which is the run that gets sent, and three artefacts said something untrue there
  without erroring: a page opening *". Each row below says what is needed"* over an empty
  table, a census printing `charges=0 ·  · total=0.00`, and an approver's report drawing a
  warning pill over *"0 more charges, A$0.00, waiting on their invoices … they are listed one
  by one"*. All three were prose written for the non-empty case with the count interpolated.
  The repair is a separate sentence for the empty case, because at zero the thing worth
  saying is different in kind.

- **Pull a contested supplier's whole invoice series, not the month you are short of**
  (`references/inclusion-rules.md`). Two invoices left it open whether a declined payment had
  fallen back to the claimant's card; seventeen settled it in one reading, because the answer
  was in what stayed the same across fifteen months and what changed in the sixteenth. The
  same export separated another supplier's developer API from its consumer subscription.

- **De-duplicate on the invoice sequence, never the calendar** (R12). "One invoice a month"
  is an assumption, and a supplier breaks it the month something changes: one issued a single
  month as two invoices with adjacent numbers on one day, one per subscription, and the prior
  claim cited only the first. A month-level check calls that month covered and the
  boundary-continuity test still passes, because the hole is inside the prior claim's range
  rather than at its edge.

- **A card statement is parsed, never grepped.** A foreign charge puts its local amount on
  the line *after* the description, which `parse_statement.py` has always handled and a grep
  never will. Four rows already in the claim were reported unclaimed by an ad-hoc grep,
  purely because all four were foreign charges.

- **The card sweep reports split suppliers**, because that is the only structural signal
  that a mask form is being missed. One supplier's paperwork comes off one template, so
  "some name a card and some do not" is either a real change in their billing or a gap in
  the pattern list — and the two are identical in the totals. Measured twice on one run:
  the first version missed `3*** ****** *3003` and under-counted by one, then adding
  `Mastercard - 7328` (brand, bare dash, no mask at all) took the census from 11 documents
  to 26. Both misses reported a smaller denominator and a clean result.

- **A corrected card re-opens the rows excluded on the old reading**
  (`references/inclusion-rules.md`). An exclusion already propagates forward to everything
  tied to the account; the reverse never did. Four rows were reconciled, priced and marked
  against a card read as somebody else's, the operator corrected the card the same day, and
  nothing re-asked them. A sweep hours later rediscovered them as charges with no invoice
  while their receipts sat on disk, named in the reconciliation record beside them. The rule:
  store the reason with every exclusion, re-run every row whose reason names the thing that
  changed, and report the count that came back into scope including zero. Its corollary is
  the second half of the same defect — a row the record already pairs with a document may
  never be reported as a row with no document.

- **The outstanding set's span is derived rather than typed.** A report sentence read
  "since 1 July" until a sweep pushed the earliest outstanding row back to August 2025 and
  the sentence stayed put.

## 0.2.0

Four operator review passes over a real claim, each tightening the account test, and
every one of them found an attribution error where none found an arithmetic error. That
asymmetry is what this release is.

- **`scripts/classify_accounts.py`** — the bill-to census. Every claimed row placed on a
  six-rung evidence ladder, per supplier, with counts and values, so the operator sets the
  bar once instead of discovering a new shape of the problem on each pass. The rung that
  matters is "the company named **and** a non-company contact email": it is
  indistinguishable from the rung above until the pattern that finds the email actually
  fires, and it was worth eleven rows and A$1,579.45 that four passes had walked past.
- **`scripts/patterns.py`** — the extraction patterns, defined once. They had been four
  copies in four scripts, which is how one drifted into a shape that could not fire.
- Four new evals, one of which (V-17) holds every pattern to a fixture it must match
  **and** one it must refuse. It immediately found the tax pattern only handled dollar
  signs, which quietly made the skill's claim to work in other jurisdictions untrue.
- The hand-off page gained a fourth kind, `account`, for a charge whose invoice exists and
  names the wrong contact, and now lists only suppliers with a verified company account.
- References updated throughout: the evidence ladder, the organisation-name discriminator,
  one-to-one pinning for verification as well as matching, the three regex bugs, and the
  rule that prose rots on removal as well as on addition.
- Icon and banner, and registration in the marketplace.

Measured: 1 document in 96 named the card that paid it, so the card link always comes from
a transaction record and never from the invoice. That is now stated in the reports.

## 0.1.0

First release. Built from one real reimbursement claim: 88 charges, 18 suppliers,
11 months, A$6,936.69, delivered with a schedule, a folder of invoices filed by month
and two reports.

- The six-stage run: build the charge universe and find its feed-blind days, find the
  invoice for every charge, decide each row against three operator-supplied gates, match
  one to one, emit from a single source, gate it.
- Nine reference documents carrying the inclusion rules, the source quirks, the portal
  hand-off, the matching technique, the extraction patterns, the output formats, the
  gate suite, the configuration, and the evidence behind every claim.
- Ten scripts. `validate.py` is the run's exit condition at 24 blocking checks;
  `audit_invoices.py` reconciles filenames against document content; `build_csv.py` and
  `build_reports.py` emit from one row source with every figure derived at render.
- An unbranded report stylesheet in `assets/report.css`, where every commented rule
  names the defect a rendered-output review caught.
- `wanted_invoices.py`, the hand-off page for whatever a portal will not give an
  automated browser.

Two defects were found while building it and both are fixed here. The delivered claim
form carried a tax-inclusive classification subtotal under its ex-tax header. And this
skill's own filename audit was vacuous: it matched the filename against the extractor's
own path banner rather than against the document, so it would have passed 88 randomly
named files.

Not registered in the marketplace manifest: no icon and no banner yet.
