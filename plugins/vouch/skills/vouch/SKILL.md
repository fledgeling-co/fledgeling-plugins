---
name: vouch
description: >-
  Reconcile and substantiate a personal-expense reimbursement claim end to end, repeatably — the monthly or annual
  run that turns a year of card charges into a claim form, a folder of invoices, and two reports somebody can sign.
  Vouching is the audit term for tracing a record back to its source document, and that is the mechanism here: every
  claimed charge is keyed to the supplier's own invoice, and every invoice is read for the account it was issued to,
  because the card that paid a charge does not decide whose expense it is. Sweeps a personal-accounting MCP
  (PocketSmith or any equivalent), the Apple Mail index through the Sift MCP, card statement PDFs and a downloads
  folder; finds the days on which the bank feed holds nothing at all and backfills them from statements, which is
  where the charges nobody noticed are hiding. Drives supplier portals through proctor when a login is needed, and
  emits a wanted-invoices page — date, supplier, estimated amount, portal link, account address — whenever a portal
  refuses automation. Produces a claim CSV in the employer's own layout, invoices filed by month and named for the
  invoice number printed inside them, and two unbranded reports for the approver and the accountant. Use when
  someone asks to prepare, reconcile, substantiate, check or re-run an expense claim or reimbursement, asks which
  invoices are still missing, asks whether a claim is complete, or says the monthly claim is due.
---

# Vouch

You are assembling a reimbursement claim that somebody will sign, an accountant will check, and a tax office may
one day read. The standard is not "the numbers add up". It is **every row traces to a document, and every document
was read**.

Three failures make a claim worse than useless, and each has happened on a real run:

- **A number nobody can source.** An invoice reference invented from a Stripe account id, a figure derived from an
  exchange rate no document states, a count retyped into prose and left behind by the next pass. Each one looks
  exactly like a sourced number.
- **A row in the wrong bucket.** A personal subscription claimed as company spend, or a company expense quietly
  dropped. Only the first gets caught by a reviewer, which is why exclusions are reported rather than deleted.
- **A search that found nothing and was read as proof there is nothing.** The instrument was wrong, or its date
  filter was silently ignored, or the index does not hold what you searched for. Absence needs an instrument.

Everything below exists to make one of those three impossible.

## The one rule the rest follow

**Every negative result states its instrument, and every count states its denominator.**

"Searched and found no invoice" is not a finding. "Enumerated 767 messages from the index between these dates and
filtered on sender domain, zero matched" is. The difference has flipped a real conclusion: a keyword search whose
date filter was being silently dropped returned a confident wrong answer, and enumerating the index directly
retracted it.

So: print `examined=N` beside every `found=M`. A tool that can succeed while doing nothing needs an external
witness — click, then check the filesystem; navigate, then re-read the URL; extract, then count the files that
produced no field and name them.

## Stage 0 — Get the operator's facts before touching anything

The claim cannot be decided without these, and guessing any of them corrupts every downstream row. Ask in one
`AskUserQuestion` round, or read them from the environment variables in `references/configuration.md`.

| Fact | Why it decides rows |
|---|---|
| **Claim period** | Fixed start and end, applied to the *charge* date. |
| **Card endings, each with an owner** | `mine` / `joint` / `company` / `other`. A joint card is claimable; the company's own card never is. |
| **Company email addresses and domains** | The addresses an invoice may name for the charge to be a company expense. |
| **Company legal name and registered address** | An invoice naming the company beats a personal contact address on the same document. |
| **Prior claim files** | To de-duplicate against, on two independent keys. |
| **The employer's claim form** | Its column order and conventions are copied, including its defects. |

Two of these are commonly wrong on the first pass and both were corrected by a human on a real run: a joint card
read as somebody else's, and an old card of the claimant's read as a stranger's. **Ask for the owner of every card
ending you find, including ones the operator did not list.**

Then state the three gates back to the operator before you start, because they are the claim's own standard and
they belong in the report:

1. The supplier's invoice names a company account.
2. The payment landed on a card the claimant owns personally.
3. The charge is absent from the prior claim.

`references/configuration.md` carries the env-var names, the defaults, and what to do when a fact is missing.

## Stage 1 — Build the charge universe, then find its holes

Pull every charge in the period from the accounting MCP, filtered to the claimant's own accounts. That set is
**not** the truth; it is one instrument's view of it.

**Then find the feed-blind days.** A feed-blind day is a date on which the account holds no transaction at all.
Two real gaps of 38 and 44 days on the primary business card were invisible until this was computed, and they
contained charges that belonged in the claim.

```python
blind = {d for d in period_days if d not in {r['day'] for r in feed if r['acct'] == account}}
```

Backfill those windows from card statement PDFs, which state the AUD amount **and** the foreign amount and the
conversion commission for a foreign charge. `scripts/parse_statement.py` handles the year rollover, the two-line
foreign-amount form, and credit markers.

Never reason from a pre-filtered extract. On one run a 333-row extract stood in for a 2,444-row feed and had
silently dropped five claimable charges.

`references/sources.md` covers the accounting MCP (any provider), the mail index, statements and the downloads
sweep, with the measured quirks of each.

## Stage 2 — Find the invoice for every charge

Four sources, in decreasing order of authority: **a PDF invoice**, an emailed receipt whose body carries the
figures, a vendor portal, nothing.

Prefer the PDF. An email proves delivery and names a recipient; only the invoice is authoritative for the number,
the period and the account.

Read the mail index rather than searching it blind: find the real billing senders first (`invoice+statements@…`
amid thousands of `notifications@…`), then query by sender and date window. `references/sources.md` §Mail carries
the schema, the join column that is *not* called `key`, and the reason attachment bytes are usually absent.

For portals, route to **`proctor`**, which drives the operator's own signed-in browser through the macOS
accessibility tree rather than a separate automation profile. That distinction is load-bearing: Cloudflare blocks
headless and profile-copy automation on several supplier portals, and the operator's real browser is the only thing
that gets through. `references/portals.md` carries the verified URLs, the ones that 404 even when signed in, and
the hand-off protocol.

**When a portal cannot be driven, stop and emit the wanted-invoices page** rather than retrying. `scripts/wanted_invoices.py`
writes an HTML page listing, per outstanding charge: the date, the supplier, the amount as charged and in the
invoice's own currency, the portal link, and the account address the invoice is expected to name. On a real run
that page came back with nineteen invoices attached within minutes. A named hand-off beats an hour of automation.

## Stage 3 — Decide each row

Read the **`Bill to` block of the invoice**, never the delivery address of the email that carried it. The two are
different facts and they disagree often enough to matter: one supplier delivers receipts to a personal address
while billing to the company's registered address on the document itself.

The decision ladder, in order, stopping at the first that answers:

1. **The invoice names a company address or the company's legal name** → company expense.
2. **The invoice names a personal email account** → not a company expense, whatever card paid it.
3. **The invoice names neither** → settle it from same-day vendor correspondence to a company address, and *record
   the disagreement* rather than hiding it. Where nothing settles it, escalate to the operator and add nothing.
4. **The card is the company's own** → never reimbursable, even when gates 1 and 3 pass.

One supplier routinely holds several billing accounts, and the **invoice-number prefix is the discriminator**. On a
real run one vendor billed three separate accounts off the same cards; only one was the company's, and the other
two would have gone in undetected on a vendor-name match.

Then run `scripts/classify_accounts.py` and put the whole claim on the evidence ladder in one table: how many rows
and how much money sit on a company email, on the company domain, on the company's name alone, on a company name
beside a personal contact, on a personal address, and on nothing at all. **The operator sets the bar; the run applies
it to every row.** The rung that catches people is "company named AND a personal contact email" — it is invisible
until the pattern that finds the email actually fires, and it was worth eleven rows on a real claim.

`references/inclusion-rules.md` carries all fourteen rules with the reasoning and the real counter-example that
produced each.

## Stage 4 — Match charges to invoices, one to one

**Assignment, not lookup.** Two identical subscription top-ups days apart will both match whichever invoice comes
back first, one write lands, the second silently does nothing, and the tally reports two. Use greedy nearest-date
assignment with a `used` set on both sides.

```python
pairs = sorted((gap(inv, chg), ci, ii) for ...)   # nearest first
for gap, ci, ii in pairs:
    if ci in used_c or ii in used_i: continue
    ...
```

Then check the implied FX series across the whole claim. Charge ÷ invoice in the invoice's own currency should form
a smooth band; an outlier is a wrong pairing, not a wrong rate. This has caught real mis-assignments.

The AUD figure is **always what the card was charged**. Never convert from the invoice. Where a supplier bills in
USD, the card statement states the AUD amount with the conversion commission inside it, and that is the number.

`references/matching.md` carries the tolerances, the windows, and the sequence-gap technique that proves a missing
invoice exists.

## Stage 5 — Emit, from one source

`claim_rows.json` is the single source of truth. The CSV and both reports are generated from it on every build, and
**every count in every template is derived**. Hardcoded counts have rotted twice on real runs, leaving a report
whose total row disagreed with the rows above it.

- **CSV** in the employer's own layout, including its conventions and its defects. Where the prior form transposes
  two columns, write the values in header order and *state the divergence prominently* so a column-by-column
  comparison reads as deliberate.
- **Invoices** filed as `<YYYY-MM>/<invoice-number>.<ext>`, named for the number printed inside the document.
- **Two reports**, unbranded templates in `assets/`: one for the approver, one for the accountant.

`references/outputs.md` carries the exact CSV layout, the directory structure, and the section list of both reports.

## Stage 6 — Gate it

`scripts/validate.py` is the gate and it exits non-zero on failure. It is not advisory.

**Blocking:** per-row `excl + GST == incl`; sign convention; every date inside the period and in order; three totals
equal the sum of their rows; invoice numbers unique; every row's file exists; every filename matches an invoice id
*printed inside that document*; no orphan files; no two rows citing one file; CSV fields equal their source rows.

**Reported, not blocking:** rows with no bank charge behind them; rows whose invoice was unreadable; suppliers with
no stated purpose; the count of feed-blind days and what was found in them.

**Run `scripts/card_on_document.py` over every filed document.** A minority state the card. On a *receipt* that is
proof of who paid; on an *invoice* it is the card on file at issue, so a declined payment can retry onto another card
and the invoice never says so — a foreign card on an invoice excludes the row only where a statement covers the
window a retry could have landed in. It is the only check that sees a supplier move from the claimant's card to the
company's own: same supplier, same amount, same cadence, and the charge just stops appearing on a personal card,
which reads as a feed gap. Measured on a real run at 11 of 105 documents, one of them in a mask form the first
version of the pattern missed — so the census prints the forms it read, because a narrowed pattern and a clean
result look the same.

**Then run `scripts/cross_check.py` over the two leftover piles before publishing either.** Charges with no document
and documents with no charge are opposites only if nothing is on both; a misparsed currency puts one transaction on
both lists, and each list is internally consistent while it happens. It proposes rather than decides — a hit names
the file to open, since only the document says which of the two figures was wrong.

The filename-versus-content audit is the one that earns its keep. On a real run it was what made "name every
attachment by its invoice number" safe, after an earlier pass had put fourteen rows on the wrong month by keying
them to a billing email instead of the invoice.

Then look at the rendered reports. Route to `design-review` for the deterministic gates; it found a contrast
failure of 1.96:1 on the single most important number in a document that had passed every other check.

`references/gates.md` carries every check with the defect that motivated it.

## Working posture

- **Recount after every mutation.** Row counts and totals drift across passes. Derive every figure at the moment of
  reporting; never restate one from an earlier message.
- **Snapshot before rewriting.** A hand-rolled parser that trims cells will silently normalise the employer's
  padding. Copy the form first and diff on parsed values, not bytes.
- **Report exclusions with their reason**, in the report, so the approved number reads as a result rather than an
  assertion. Delete nothing.
- **Put judgement calls in front of the approver** rather than resolving them: an annual term spanning the period
  end, a row resting on a vendor statement, a column-order divergence. State both treatments and recommend one.
- **Never assert a tax characterisation.** State the arithmetic, cite the document, and hand the characterisation to
  the accountant. Where an optional R&D or deductibility classification is produced, it is a default position
  requiring the company's own apportionment, and it says so.
- **A bar the operator moves applies to the whole claim, not to the rows in front of you.**
  When a rule tightens mid-run, re-classify every row and report the result before acting.
  On a real run a supplier worth A$1,579.45 was found only by re-running the classification
  over all of them; the four passes before it had each looked at the rows under discussion.
- **A later instruction that contradicts an earlier decision gets surfaced, not resolved.**
  The operator may have changed their mind and may not have noticed the collision. Name the
  earlier decision, say what the new instruction does to it, and let them choose.
- **Delegate rarely.** Sub-agents earn their cost on a wide independent sweep (mining a long transcript, reading a
  large corpus). Reading twenty invoices is not delegation-shaped work. Cap at four.

## References

- `references/configuration.md` — env vars, the operator interview, what to do when a fact is missing
- `references/inclusion-rules.md` — the rules, the evidence ladder, and the counter-example behind each
- `references/sources.md` — accounting MCP, mail index, statements, downloads; measured quirks of each
- `references/portals.md` — proctor hand-off, verified URLs, what Cloudflare blocks
- `references/matching.md` — assignment, tolerances, FX bands, sequence gaps
- `references/extraction.md` — PDF text, invoice-id patterns, vendor fingerprints, card detection
- `references/outputs.md` — CSV layout, directory structure, both report structures
- `references/gates.md` — the validation suite and the defect behind each check
- `references/evidence.md` — where every claim in this skill comes from

## Scripts

- `scripts/pdftext.swift` — bulk PDF text extraction via PDFKit; compile once with `swiftc -O`
- `scripts/parse_invoices.py` — supplier, date, invoice id, total, bill-to, card, from a folder of PDFs
- `scripts/parse_statement.py` — card statement PDFs into dated rows with foreign amounts
- `scripts/find_blind_days.py` — the feed-gap detector
- `scripts/match.py` — one-to-one charge/invoice assignment with the FX band check
- `scripts/build_csv.py` — the claim CSV from `claim_rows.json`
- `scripts/build_reports.py` — both HTML reports from the same source
- `scripts/validate.py` — the gate suite
- `scripts/audit_invoices.py` — filename versus document-content audit
- `scripts/classify_accounts.py` — the bill-to census: where every row sits on the evidence ladder
- `scripts/wanted_invoices.py` — the outstanding-invoices hand-off page
- `scripts/card_on_document.py` — reads the card a document names, where it names one; that outranks the
  feed match, and it is the only evidence that catches a supplier moving to the company's own card
- `scripts/cross_check.py` — pairs the charges-with-no-document pile against the documents-with-no-charge
  pile, because a misread currency puts one transaction on both and each page then looks correct

## Assets

- `assets/report.css` — the shared unbranded stylesheet. Every rule carrying a comment is there because the plain
  version of it shipped a defect a rendered-output review caught. Do not simplify one away without re-running the
  probe that found it.

**Verify a rendered fix by re-reading the value, never by confirming the rule exists.** A rule added at equal
specificity earlier in the file loses to the one it was meant to beat and looks correct in the stylesheet. And
check the instrument before the page: a headless browser refused loopback access wrote a 70KB all-white PNG with
no error, and its own text-measurement API returns a fixed width per character rather than a measurement.
`references/evidence.md` carries both, with the controls that exposed them.
