# Inclusion rules

Fourteen rules. Each carries the reasoning and, where one exists, the real counter-example that produced it. A rule
without a counter-example is a rule nobody has tested; the ones with counter-examples are the ones that will fire.

## The three gates

Stated in the approver's report as the claim's own standard, so the number being approved reads as a result:

1. **The supplier's invoice names a company account.**
2. **The payment landed on a card the claimant owns personally.**
3. **The charge is absent from the prior claim.**

Anything failing one is **listed with its reason**, never deleted.

---

## R1 — The invoice sets the identity, not the card

Read the `Bill to` block of the invoice. The card that paid a charge does not decide whose expense it is: a
personal card can pay a company account, and a company card can pay a personal one.

*Counter-example that makes this load-bearing:* one supplier delivers its receipts to a personal address while the
invoice PDF bills to the company's registered address. The email recipient is a **signal**; the invoice's own
bill-to block is the **evidence**.

## R2 — A company name or registered address beats a personal contact address on the same document

Three rows on a real run would have been wrongly excluded by a naive email test:

- An invoice reading `Bill to: <Company>, <registered address>` with a personal address as the account contact.
- A receipt reading `Account billed <org-slug> (<personal gmail>)` where the same vendor's tax invoices for that
  enterprise bill to the company by name.
- A receipt delivered to **several** addresses, one of them a company address — the filed copy happened to be the
  personal one.

**A receipt delivered to several addresses counts as company if any recipient is a company address.**

## R3 — One supplier can hold several billing accounts, and the invoice-number prefix is the discriminator

On a real run one vendor billed **three** separate accounts off the same cards. Only one was the company's. A
vendor-name match would have swept all three in.

The prefix of the invoice number is stable per account and is the cheapest discriminator available. Build the
prefix→account map as you read invoices, and treat an unseen prefix as a new account needing classification rather
than as the known one.

## R4 — A company invoice paid on the company's own card is not reimbursable

It passes gate 1 and fails gate 2. Render the amount as an en dash rather than a zero, and say why: it never
touched a personal card, so there is nothing to reimburse.

## R5 — A card appearing on invoices but on no account in the feed is the company's card

This is how the company card gets identified without being told. State the inference to the operator rather than
acting on it silently.

## R6 — A joint card is claimable

Joint money is still partly the claimant's. Only a card belonging solely to someone else, or to the company, puts a
charge outside the claim on the card alone.

*This has been read the wrong way round by an agent and corrected by a human.* Ask.

## R7 — Where the invoice names neither company nor email, settle it from correspondence, and record the disagreement

One real invoice carried a personal postal address and no email, while the vendor's sign-in codes and billing
support cases for that account went to a company address on the invoice date. The account is identified by the
address that signs into it and raises support on it, not by the postal address on the PDF.

**Write the disagreement down in the report.** A row kept on this basis is a row the accountant should be able to
see the reasoning for.

## R8 — Where nothing settles it, escalate and add nothing

On a real run, nineteen invoices from one supplier carried a literally empty `Bill to` block; identity was a Team ID
only. The correct behaviour was to say so, name the two ways to settle it, and **add nothing** until the operator
asserted ownership. Their assertion then became the recorded basis.

## R9 — No document, no claim

Distinguish **absent** from **missing**, and prove which. On a real run a supplier's invoice series for the account
began four months after the charge; the search window was widened back eighteen months before concluding nothing
was ever issued. "Absent, proven by widening the window" is a finding. "Not found" is not.

## R10 — Never invent a figure

The claimed amount is what the card was charged. Where a supplier bills in a foreign currency, the card statement
states the local amount with the conversion commission inside it, and that is the number.

Deriving a figure from an inferred exchange rate is out, unless the operator directs it and the basis is stated in
the report. On a real run two rows were derived at a stated midpoint rate and the card statements later gave the
true figures: the derivations were 34c and 21c low. **The statement supersedes, and the derivation note is deleted
rather than left standing.**

Implied FX is a **consistency check on matching**, never an input to an amount.

## R11 — Key every row to the invoice covering its own period

A vendor's monthly emails look alike. On a real run, thirty-three invoice numbers were wrong and **fourteen landed
on the wrong month** because rows were keyed to a billing email rather than to the invoice that covers the charge's
own period.

Corollaries: an invoice number read off a portal URL is not the invoice number. A payment reference is not an
invoice reference. A number assembled from a vendor's account id plus a serial is not evidence of anything.

## R12 — De-duplicate against the prior claim on two independent keys

Invoice-number set intersection **and** (date, amount) pair intersection, both empty. Then corroborate positively:
supplier invoice sequences should run **continuously across the boundary without repeating** — the last number in
the prior claim and the first in this one adjacent in the series.

**Check the sequence, never the calendar.** "One invoice a month" is an assumption, and a supplier breaks it the
month something changes: measured, one issued a single month as *two* invoices with adjacent numbers on one day,
one per subscription, and the prior claim cited only the first. A month-level completeness check calls that month
covered, and the boundary test above still passes, because the hole is inside the prior claim's own range rather
than at its edge. Walk the numbers.

## R13 — Refunded and zero-value rows are not rows

A reversed charge is not an expense. A zero-value billing cycle carries nothing. File the document; claim nothing.

Two subtleties, both from real data: where a vendor charges and reverses on the same day, pair the credit to the
**later** charge, or a valid charge is wrongly shown as refunded. And one credit settles exactly one charge —
pairing a credit against every charge it fits reports refunds the bank never made and drops real spend.

## R14 — An annual term inside the window is claimed in full, and the apportionment question is raised

Where a charge inside the period buys a term extending beyond it, the full amount left the claimant's card, so the
row carries the full amount. Whether the company apportions it is a policy decision. **Put it in front of the
approver with both treatments named**, and say the invoice supports either.

---

## Reporting

- Exclusions are grouped by **class**, not listed per charge, with a count and a total.
- Consumer noise (groceries, streaming, transport) is filtered by a business-supplier allowlist and never appears.
  It is not an exclusion; it was never a candidate.
- Where the operator has directed that a class not be discussed, honour it — but move those rows into the
  not-claimed record rather than deleting them.

## The account test is a ladder, and the operator sets the rung

The four-step decision above answers one row at a time. It does not tell the operator
where the *claim* sits, and that is what they actually decide on. Run
`scripts/classify_accounts.py` and put all six rungs in front of them at once:

| | What the document shows | Strength |
|---|---|---|
| 1 | a company email address in the bill-to | strongest |
| 2 | the company domain elsewhere on the page | strong |
| 3 | the company named as addressee, no email at all | moderate |
| 4 | the company named **and** a non-company contact email | weak |
| 5 | a non-company email only | weaker |
| 6 | neither a company name nor an address | weakest |

Rung 4 is the one nobody predicts and it is where the money hides. It is indistinguishable
from rung 3 until the pattern that finds the email actually fires — and on a real run that
pattern could not fire, so eleven rows worth **A$1,579.45** sat in rung 3 for three review
passes. The supplier had billed the company at its registered address with the claimant's
personal address as the contact, on every single invoice.

Rung 2 exists because of hosting and domain invoices: a workspace bill states the domain
it is billing for, which is the company as surely as an email is, and a check looking only
for `@company.com` misses `company.com`.

**Print counts and values per supplier on every rung, and let the operator draw the line.**
The run does not decide where the bar goes. What it must do is apply whatever bar comes
back to **every row in the claim**, not to the supplier under discussion — a rule tightened
mid-run and applied only to the rows in front of you leaves the same defect everywhere
else, and it will be found by whoever reads the schedule rather than by you.

## One supplier, several accounts

Two discriminators, and they answer different questions.

- **The invoice-number prefix** separates accounts at the same supplier. On a real run one
  vendor billed three accounts from the same cards, only one of them the company's.
- **The organisation name** separates a personal-shaped account from a company one even
  when both use a company email. `"someone@company.com's Organization"` and `"Company"`
  are different accounts at the same supplier, and the first is usually an individual
  subscription bought on a work address.
- **The line item** separates two *products* sold by one supplier, which is the case the
  first two discriminators miss. On a real run one vendor sold a metered developer API and
  a consumer chat subscription, both settled through the same payment processor, both
  landing on the card as the identical descriptor and both in the same month. Every claimed
  row was the API; the subscription was personal. Only the product named on the invoice
  line separates them, and the operator spotted it before the pipeline did.

None of the three is visible from the supplier's name, the amount or the card descriptor,
which is why a row is keyed to its invoice and the invoice is read. Treat a supplier as a
folder rather than as an answer: two accounts, two products and two tenants at one vendor
are the normal case, not the exception, and a rule written at supplier level will decide
all of them the same way and be wrong about some.

## A supplier is a folder, and its own rows are checked against each other

The three gates decide one row at a time and the census groups by evidence rung, so a
supplier whose rows land in two different places appears in two different blocks and
nothing says they are the same supplier. That is the reading nobody does: a supplier seen
under *a company address appears* is taken as settled, and its other rows are never
revisited.

`scripts/classify_accounts.py` now names every supplier whose rows disagree — on the rung
they reach, or on the address they name. Measured on a real claim it found two: one whose
invoices name the company while a receipt on the same supplier names a personal address,
and one billing two different company mailboxes. The first had taken several rounds of
human challenge to find by hand.

**The same rule holds one layer down, wherever a decision is taken at supplier level.** A
ledger that writes one classification across every row of a merchant has this defect in its
write path rather than its report: a merchant selling two products under one payee gets one
answer, right for some rows and wrong for the rest. If the system you are feeding offers a
bulk decision, the number to look for is not *how many rows agree* but *what the rest hold* —
those are different questions and only the second distinguishes a merchant nobody has
finished from a merchant that is two things.

A split supplier is normal: two accounts, two products, or a billing contact that changed.
It is a description, nothing clears it, and a legitimately split supplier stays listed.

## When a supplier's status is in doubt, pull its whole series rather than the missing month

The instinct is to fetch the document you are short of. It is usually the wrong request, because a single invoice
answers "what does this one say" and the question is almost always "what changed".

Measured twice. Two invoices showed a supplier billing the company's own card and left open whether a declined
payment had fallen back to the claimant's — unanswerable from two documents. The full run of seventeen settled it in
one reading: fifteen consecutive months on the claimant's card, then two on the company's, same subscription ids and
same amount throughout, and the card on file never reverting. Separately, a supplier's nineteen invoices were what
separated its metered developer API from its consumer subscription; either one alone looks like the other.

So when a supplier is contested, ask for **every** invoice it has issued in and around the period. It costs the
operator one export instead of several lookups, it makes the gap analysis exhaustive rather than sampled, and the
answer tends to live in the difference between consecutive documents rather than in any one of them.

## A card named on the document is strong evidence, and a RECEIPT's card is proof

Most documents say nothing about the card, which is why payment is settled from the feed.
A minority name it, and that is the only evidence that catches a supplier moving onto the
company's own card. Measured: one supplier named the claimant's Amex for ten consecutive
months and the company's Visa from the eleventh, with the same subscription ids, amount and
monthly cadence throughout. From the feed's side the charge simply stopped appearing, which
is indistinguishable from a gap in a feed that genuinely had gaps.

**But read which kind of document it is, because the field means different things.** A
receipt names the card that paid: that is proof. An invoice names the card **on file at
issue**, which is a statement of intent — a declined payment can retry onto a different
card, and the invoice is never reissued to say so. The tell is in the document's own words:
*"Payments received after due date shall be subject to a late charge"* is a request for
payment, not a record of one. Both halves of the ten-then-one example above were invoices
in exactly that form.

So the rule is asymmetric, and deliberately so:

- **The document names one of the claimant's cards** — supports the row, and the charge
  still has to corroborate it. Nothing changes.
- **The document names a card the claimant does not pay** — the row stays out *unless* a
  charge on one of their cards corroborates it. On an invoice, add the fallback question:
  is the period in which a retry could have landed actually covered by a statement? If the
  window is open, the row is undecided rather than excluded, and it goes on the hand-off
  page against the statement that will close it.

The mask formats vary enough to matter — `XXXX-XXXX-XXXX-3003`, `- 3003`, `ending in 3003`,
`3*** ****** *3003` — and a pattern that misses one reports a smaller denominator while
looking clean, so the census names the forms it read.

## A corrected card or account re-opens every row excluded on the old reading

The rule above runs one way: an exclusion propagates forward to everything tied to the
account. The reverse case is the one that bites, because it is silent.

An operator correction — *"that card is joint, not theirs"*, *"that address is ours"* — changes
the answer to a test that was already applied. New rows are then decided correctly and the
rows already excluded on the old reading stay excluded, because nothing re-asks them. The
run ends consistent with itself and short of what it should hold.

Measured: four rows were reconciled, priced, rated and marked `deduct` against a card read
as somebody else's. The card was corrected the same day. Every later pass honoured the
correction and none revisited the four, so a sweep two hours afterwards rediscovered them as
*charges with no invoice* while their receipts sat on disk, named in the reconciliation
record beside them. Two independent misreadings of one set of rows, both produced by the
same missing step.

So the decision log is not a log. **Store the REASON with every exclusion, and when the
operator corrects a card's owner, an account's ownership or an address's status, re-run every
row whose stored reason names the thing that changed.** Report the count that came back into
scope, including zero, because zero is the evidence the sweep happened.

Corollary: a row carrying a resolved invoice may never be reported as a row with no invoice.
If the reconciliation record names a document for it, the honest statement is that the row was
excluded and why, not that the document is missing.

## An excluded account takes its whole tail with it

When a row comes out because its *account* is not the company's, everything else tied to
that account goes too: other invoices on the same prefix, charges with no invoice that
would resolve to it, and any orphan invoice waiting on a statement. Leaving those on the
outstanding list quietly re-proposes the row the operator just declined.
