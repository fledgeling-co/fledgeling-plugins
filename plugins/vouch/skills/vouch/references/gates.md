# Gates

`scripts/validate.py` exits non-zero on any blocking failure. It is the run's exit condition, not advice.

Each check below names the defect that motivated it. A check with no defect behind it is a check nobody has proven
can fail.

## Blocking

| # | Check | The defect it catches |
|---|---|---|
| 1 | Header row equals the expected column list, found by scanning for the header cell rather than by index | A form with a preamble block shifts every positional read |
| 2 | Every line is exactly the expected width | A colgroup/column mismatch that renders as overlapping text |
| 3 | Data-row count equals source-row count | The CSV and the source drifting apart between builds |
| 4 | Every date parses in the form's own format **and** sits inside the claim period | A row from the prior year surviving a filter |
| 5 | Rows are in date order | — |
| 6 | Per row, `excl + tax == incl` (±0.005) | **Caught a real column transposition**: summing the tax column gave a figure larger than the inclusive total |
| 7 | Sign convention holds on every amount | A positive row in a negative-convention form sums wrong and looks fine |
| 8 | Money fields match `-?\d+\.\d\d` or the literal zero | A `-` sentinel reading as zero downstream |
| 9–11 | Each of the three totals equals the sum of its rows | Hardcoded totals rotting after rows are added |
| 12 | Invoice numbers are unique | Two rows claiming one document |
| 13 | Every CSV invoice number exists in the source rows | A hand edit |
| 14 | Every row's file exists on disk | "A number was typed" is not "a document exists" |
| 15 | **Every filename matches an invoice id printed inside that document** | Fourteen rows on the wrong month, from keying to a billing email |
| 16 | No orphan files, and no two rows citing one file | A superseded document left in the folder |
| 17 | CSV fields equal their source rows, field by field | Any silent transform in the writer |
| 18 | File is valid UTF-8; BOM and line endings reported | — |
| 19 | Footer carries every expected block | A truncated write |
| 20 | Classification values are `TRUE`/`FALSE`/empty only, and no verdict lacks a reason | A half-filled column |
| 21 | On every tax-bearing row, the tax is the **smaller** of the two components | The transposition #6 is blind to — see below |

## The blind spot #6 has, and the check that covers it

Check 6 is the one that found a real transposed column, and it cannot find the next one. Swapping two values
**preserves their sum**: `309.09 + 30.91` and `30.91 + 309.09` both reach `340.00`, so a row with the tax figure
under the ex-tax header passes check 6 cleanly. It was the *totals* that gave the first one away, and only because
the total row had been written before the transposition happened.

Proved on this skill's own fixture: transposing one row of a real 88-row claim left check 6 green and tripped only
9–11. Transpose the whole column and recompute the totals from it, and every check up to 20 passes.

What catches it is **magnitude**, not arithmetic. Under a headline rate `r`, the tax on a taxable supply is
`incl × r/(1+r)` — a tenth of the inclusive figure at 10%, a ninth of the ex-tax figure — and it is always the
smaller of the two. So:

```python
if tax > excl:                              # blocking: the columns are the wrong way round
if abs(tax - incl * r/(1+r)) > tolerance:   # advisory: mixed, exempt, or overseas supply
```

The second is advisory on purpose. A claim spanning foreign suppliers has rows with a legitimate zero tax and rows
where the supplier charged a different rate, and blocking on those would train the operator to pass `--tax-rate 0`,
which disarms the first check too. `--tax-rate 0` is still offered, for a jurisdiction where the whole idea does
not apply; it says so in the help.

## The one that earns its keep

**Check 15.** For every row: open the filed document, extract every invoice-id-shaped string with the full pattern
set, and require the **filename stem** to be among them.

```python
ok      = stem in ids_found or re.sub(r'\s+','',stem) in flattened_text
buckets = matched | filename-not-in-document | file-missing | file-unreadable
```

Report all four buckets plus orphans. On a real run this returned **88 of 88 matched, 0 missing, 0 unreadable, 0
orphans**, and it is what made "name every attachment by its invoice number" a safe convention rather than a
hopeful one.

Read non-PDF attachments as text rather than through the PDF extractor, or a `.eml` reports as absent while sitting
on disk. That exact bug fired once and also forced a prose correction, because the report claimed all attachments
were PDFs.

**Strip the extractor's own banner before matching anything.** `pdftext.swift` prints `=== <path> ===` ahead of each
document so a batch can be split, and the fallback arm of this check looks for the filename anywhere in the text.
The banner IS the filename, so every file matched its own name whatever was inside it. Measured on this skill's own
fixture: two documents' filenames were swapped, each verified to hold the other's invoice number, and the audit
still reported **88 of 88 matched**. Armed, the same fixture reports 86 matched and names both mismatches with the
id it found instead.

That is this skill's own rule turned on itself. A check whose pass and whose cannot-run look identical will read as
green forever, and the only way to know which one you have is to break the thing on purpose and watch it go red.

## Reported, not blocking

These are denominators. They move as the data moves, and none of them is a queue.

- **Feed-blind days**, and what was found in them.
- **Rows with no bank charge behind them** — legitimate, but the accountant should see the count.
- **Invoices with no matching charge** — the company paid them directly, or a card sits outside the feed.
- **Suppliers with no stated purpose** — a build error in practice, since the report cannot render them.
- **Documents that produced no supplier, no date or no total**, named individually.
- **Charges still without a document**, which is the wanted-invoices hand-off list.
- **Rows whose tax is not the headline share of the inclusive figure**, which is ordinary on a foreign or
  input-taxed supply and worth an eye on a domestic one.

## Rendered-output gates

Route to `design-review` against a served copy, not `file://`. Then lint the prose extracted from the built HTML.

The three findings from a real run, all invisible in source:

1. A 1.96:1 contrast failure on the document's most important number.
2. Horizontal overflow at 375px that survived the first plausible fix.
3. A leftover `word-break: break-all`, correct when the last column was a number, chopping prose mid-word once a
   text column was appended.

**Verify a fix by re-running the probe and reading the recomputed value**, never by confirming the CSS rule exists.
A rule added at equal specificity but earlier in the file loses to the one it was meant to beat, and looks correct
in the stylesheet.

## Prose gates

Read the prose against the data before shipping. Three stale facts on a real run survived every automated check:

- Two hardcoded charge counts.
- A sentence describing a filing convention (`YYYY-MM-DD_supplier_invoice`) that was never used.
- A claim about when a supplier started charging tax, contradicted by every invoice in the folder.

None is detectable without reading the sentences against the source. Do it once, at the end, deliberately.

## Recovery and idempotence

- **Snapshot the employer's form before any rewrite.** A hand-rolled parser that trims cells silently normalises
  the original padding. Diff on parsed values, not bytes.
- **Recount after every mutation.** Row counts and totals drift across passes; derive at the moment of reporting.
- **The run is re-runnable.** Filing an invoice already filed is a no-op; re-deciding a row already decided reaches
  the same verdict from the same documents. If a second run produces a different claim from the same inputs,
  something read a clock or a directory listing order.

## Prose rots on removal, not only on addition

Everything in the prose-gates section above was learned by adding rows. Removing them is
worse, because a removal invalidates every count that described the set *and* every claim
that described a row now gone. One real review removed rows five times and each pass left
something behind:

- `93 match a transaction in the bank feed, 16 more…` — three literals summing to a row
  count two removals out of date.
- *"Every Anthropic invoice states a GST line, the two from 2025 included"* — one of the
  two had been removed.
- *"Seven rows are `INV` invoices"* — a literal.
- A lede opening *"Every one of them is a company account"* while the report's own caveats
  three sections later withdrew it for the largest row on the schedule.

The rule that covers all four: **no integer and no money figure appears as a literal in
report prose, including spelled-out numbers.** Derive the word too — a speller covering
60 to 99 returns the digits outside that range, so a claim crossing 100 prints
`110 charges` in a sentence written to read as words.

And the lede is bound by the caveats: if a later section withdraws a claim, the opening
sentence may not make it. Say the narrower true thing at the top and let the detail follow.

## A worked example in prose is derived from the artefact it describes

A note explaining a prior year's transposed columns gave an illustration — *"a A$83.74 row
carrying A$7.61 of GST is written `-7.61, -76.13`"* — and there was no `-76.13` anywhere in
that file. Read properly, the tax column was **empty on 92 of its 93 rows** and the tax
figure sat one column left with the tax cell blank, which is a different defect and a
different repair.

An invented illustration in an accountant's document sends them looking for something that
does not exist. Compute the example from the file, or do not give one.

## The two leftover piles are checked against each other before either is published

A run ends with two lists that read as opposites: charges with no document, and documents
with no charge. They are opposites only if nothing is on both, and that is an assumption
rather than a property. On a real run three transactions sat on both.

The supplier prints its receipts as `$24.20` with an Australian GST line underneath, and
the extractor recorded the currency as AUD. The card had converted the same US$24.20 to
A$36.17, so the amounts never matched, the document went to the invoice-with-no-charge
pile, its charge went to the charge-with-no-invoice pile, and both pages were internally
consistent. Neither page could catch it, because each one was describing half of a
transaction and calling that half a gap.

`scripts/cross_check.py` pairs the two piles on supplier, a few days, and a ratio inside
the observed conversion band, and exits non-zero on any hit. It proposes rather than
decides: the hit means one of the two figures was misparsed, and only the document says
which, so it prints the file to open. Run it before emitting the hand-off page.

```bash
python3 scripts/cross_check.py --outstanding outstanding.json --nocharge nocharge.json \
    --fx-low 1.40 --fx-high 1.60          # exit 1 on a plausible pair
```

The general shape is worth keeping: **two errors in opposite directions look like two
findings, and a report that lists both reads as thorough.** Any run that ends with two
"missing" lists over the same population should test them against each other.

## A statement's cycle is a fact about one card

The closing day is derived from the statements on hand, and it is then true of the card
those statements belong to and of no other. A day-16 Amex cadence printed against a
Mastercard whose statements were never supplied names a period no document supports, in a
sentence indistinguishable from a measured one.

`wanted_invoices.py` therefore reads the masked card numbers out of the statements at the
same time as the dates, and names a missing period only for a card those documents cover.
Rows on any other card are said, in words, to have no statement covering them.

## Every count-bearing section is rendered at zero before it ships

A template is proven only for the populations it has actually been rendered with, and the
outstanding set is the one that reaches zero — on the last run of a claim, which is exactly
the run that gets sent.

Rendered empty, three artefacts said something untrue and none of them errored. The hand-off
page opened *". Each row below says what is needed and where to get it."* — a sentence
beginning on a full stop, promising rows over an empty table. Its census printed
`charges=0 ·  · total=0.00`, an empty segment that reads as a census that failed rather than
one that found nothing. And the approver's report drew a warning pill over the headline
*"0 more charges, A$0.00, waiting on their invoices … they are listed one by one"*, which is
good news dressed as a problem and a promise of a list that does not exist.

All three are the same defect: prose written for the non-empty case, with the count
interpolated. The repair is not a conditional around the number, it is a **separate sentence
for the empty case**, because at zero the thing worth saying is different in kind — *nothing
is outstanding* is a result, and a result deserves its own words.

So before shipping, render every report and page once with the outstanding set emptied, and
read them. Cheap to automate:

```bash
echo '[]' > /tmp/empty.json
python3 scripts/wanted_invoices.py /tmp/empty.json --out /tmp/probe.html --currency AUD
# then rebuild the reports against it and grep the output for zero-artefacts:
grep -nE '(^|[^0-9])0 (charges|invoices|rows)|\$0\.00|· +·|>\s*\.' /tmp/probe.html <report>.html
```

The same holds for any section with a denominator — an exclusions list nobody triggered, a
feed-gap census with no gaps, a split-supplier warning with no splits. If it can reach zero,
it gets rendered at zero and read once.

## A card statement is parsed, never grepped

`scripts/parse_statement.py` pairs the foreign and local amounts off the line **following**
the description, because that is where a foreign charge puts its local figure. A `grep` for a
supplier name finds the description line and nothing else, so the amount comes back empty and
whatever consumes it reports the charge as unmatched.

Measured on a real run: four rows already in the claim were reported unclaimed by an ad-hoc
grep over a statement, purely because every one of them was a foreign charge. The grep was
written twice, hours apart, by someone who had already written the parser that handles it.
