# Matching

Pairing charges to invoices. The failure here is quiet: a wrong pairing produces a row that has a number, has a
document, and is wrong about which document.

## Assignment, never per-charge lookup

This is the rule the whole file exists for.

Two identical subscription top-ups four days apart will **both** match whichever invoice the lookup returns first.
One write lands, the second's filter matches nothing and silently does nothing, and a tally taken from the plan
reports two. Measured on a real run: independent lookup matched 7 of 10 and reported two as ambiguous; one-to-one
assignment matched 9 of 10 and correctly identified the tenth as belonging to a different account entirely.

```python
pairs = sorted(
    (gap_days(inv['date'], chg['day']), ci, ii)
    for ci, chg in enumerate(charges)
    for ii, inv in enumerate(invoices)
    if gap_days(inv['date'], chg['day']) <= WINDOW
)                                        # nearest first
used_c, used_i, assigned = set(), set(), {}
for gap, ci, ii in pairs:
    if ci in used_c or ii in used_i:
        continue
    used_c.add(ci); used_i.add(ii); assigned[ci] = (ii, gap)
```

**Report the written count from the database, never an echo of the plan.** `modifiedCount`, not `len(plan)`.

## Windows and tolerances

| Parameter | Value | Why |
|---|---|---|
| Date window | ≤ 4 days for a tight per-supplier pass, ≤ 6 for a sweep | A card posts 1–3 days after the invoice; more than 6 admits the next cycle |
| Amount tolerance | 0.02 in the invoice's own currency | Rounding only |
| Implied FX band | 1.35 – 1.75 for AUD/USD | Rejects a coincidental amount match across currencies |
| Direction | debits only (`amount < 0`) | A credit is a refund, not a purchase |

Match on the invoice's **own** currency figure where the statement supplies it:

```python
target = charge['foreign_amount'] if charge.get('foreign_amount') else charge['local_amount']
```

An amount-only match is worthless for subscriptions. One charge produced **25 PDF hits** because the same figure
recurs monthly and the statement PDFs themselves contain it.

## The FX band as an independent check

After assignment, compute `charge_local ÷ invoice_foreign` across every pair and look at the series. It should be
smooth and move slowly with time. Measured on nine pairs across eight months: 1.4657 to 1.5885, monotone with the
market.

**An outlier is a wrong pairing, not a wrong rate.** This has caught real mis-assignments, and it costs one line.

## Sequence gaps prove a missing invoice exists

Supplier invoice numbers are usually sequential per account. A gap is positive evidence that a document exists and
has not been collected:

```
SBIE-11443117 (19 Apr) → SBIE-11985248 (19 Jun)     nothing between → a May invoice exists
```

When the missing one arrives, it should **fill the gap exactly**. That is a stronger confirmation than any date or
amount match, and it is the same technique that proves the prior-claim boundary (R12).

## A vendor × month matrix is the cheapest completeness check

Build a grid of suppliers against months and print it. A monthly subscription with a blank cell is either a missing
invoice or a real gap in the relationship, and both are worth knowing:

```
vendor            08  09  10  11  12  01  02  03  04  05  06
Slack              1   1   1   1   1   1   1   1   1   1   1
Redis Cloud        .   1   1   .   1   1   1   1   .   1   1
```

High yield for one screen of output.

## Coverage census per supplier

List every invoice date held on disk per supplier before hunting. This tells you where to spend effort, and it is a
denominator rather than a queue:

```
Ref.tools   12 invoices  2025-09 .. 2026-08   consecutive
Redis        3 invoices  2025-05, 2026-05     gaps
Paddle       0 invoices                        nothing at all
```

## Charges with no invoice, and invoices with no charge

Both are findings and they mean different things.

- **Charge with no invoice** → chase it: mail, portal, then the wanted-invoices hand-off. It stays out of the claim
  until a document exists.
- **Invoice with no charge** → the account was paid by someone else, or on a card outside the feed. Do **not** add
  it. On a real run several suppliers had invoices for months with no charge anywhere in 2,642 feed rows; the right
  conclusion was that the company paid them directly.

Both get counted and reported. Neither gets silently dropped.

## Verification needs the same one-to-one pin the matching did

Assignment is not only how rows are built; it is how they are *checked*. A row verified
against "a transaction of the right amount near the right date" is not verified when the
supplier charges the same amount several times a week. On a real run one subscription row
matched **four** separate identical charges in a single week, and every one of the four
would have supported the claim on its own.

So the verification pass runs the same greedy nearest-date assignment with a `used` set,
over the claimed rows, and reports the pinned transaction. Two rows cannot then rest on
one debit, which is the failure a per-row lookup produces silently.

## Confirm in two records, not one

Three independent places a transaction can be found, and they fail differently:

- **the accounting provider's feed** — complete until an account stops reporting
- **the app's or the household's own ledger** — a second copy, written by a different pass
- **the card statement** — the only record that survives a feed outage

A row found in two of the three is solid. A row found only in the feed is fine until the
feed is the thing that broke. Report the split as a count: *N in the feed, M on a
statement, K somewhere else* — and derive it, because it moves every time a row is added
or removed.

**Never verify against a statement by substring.** Searching a statement's text for
`34.00` also matches inside `340.00`, and where a supplier bills the same amount monthly a
matching line does not identify *which* charge. Match a line carrying both the merchant
and the amount, restrict to the statement whose period covers the row, and where the
supplier repeats a figure, say the statement cannot settle it rather than implying it did.

## The invoice almost never names the card

Measured over a full claim: **1 document in 96 named the card that paid it.** Everything
else states what is owed and is silent on settlement.

That is the evidence model, and it is worth saying out loud in the reports: an invoice
proves what was billed and to whom, a transaction record proves who paid, and no single
document does both. A claim is the pair. Where a receipt *does* print the card, treat it
as a bonus rather than as the norm the others have failed to meet.
