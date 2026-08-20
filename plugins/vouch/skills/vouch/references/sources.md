# Sources

Four instruments, each with measured quirks. The quirks matter more than the capabilities: every one below is a way
a source can look like it answered when it did not.

---

## 1. The personal-accounting MCP

**Any provider.** The skill needs four fields per transaction and one per account; anything supplying them works.

| Need | Field |
|---|---|
| Transaction date | `date` |
| Signed amount | `amount` (negative = charge) |
| Merchant string | `payee` and/or `original_payee` — match against **both** |
| Owning account | account name or id |
| Card tail per account | the account's `number`, which is the join to card-ownership |

### PocketSmith specifics

Auth is a **developer key header**, not a bearer:

```bash
curl -s -H "X-Developer-Key: $POCKETSMITH_API_KEY" -H "Accept: application/json" \
  https://api.pocketsmith.com/v2/me
  .../v2/users/<uid>/transaction_accounts
  .../v2/transaction_accounts/<id>/transactions?start_date=&end_date=&per_page=100
  .../v2/users/<uid>/transactions?search=<term>&start_date=&end_date=&per_page=100
```

`transaction_accounts[].number` carries the card tail (`33003`, `xxxxxxxxxxxx7328`) — this is how card endings on
invoices become account decisions.

**`per_page=500` returned exactly 500.** A response equal to the limit is a truncation signal, not a count.
Paginate, and compare `len(rows)` to the limit before believing any total.

### The quirk that matters most: the feed has silent holes

Measured on one account over a year: 210 distinct days with data, and gaps of **38 days** and **44 days** with
nothing at all. A second account of the same family held **5 rows for the entire year** and its balance had not
moved in five months — a dead feed that looks exactly like a quiet account.

So compute the blind days and treat them as a coverage denominator:

```python
have = {r['day'] for r in feed if r['acct'] == account}
blind = [d for d in period_days if d not in have]
```

Report `feed-blind days: N of M`. Backfill from statements.

---

## 2. Card statement PDFs

The authority for what was actually charged, and the only source that states the **foreign amount and the
conversion commission** alongside the local one:

```
October 19 SLACK T05TTDDSUAG DUBLIN
13.13 21.00
UNITED STATES DOLLAR
AUD 21.00 includes conversion commission of AUD .61
```

`scripts/parse_statement.py` handles: the statement-period header, the year rollover (a January line on a statement
ending in February belongs to the prior year), the one-line amount form, the two-line foreign form, and the `CR`
credit marker on the following line.

The header also carries the masked account number, which pins the statement to a card ending.

---

## 3. The mail index (Sift MCP over Apple Mail)

The index is at `~/Library/Application Support/sift-apple-mail/index/generations/gen-*/index.db`. **Always take
`| tail -1`** — older generations persist and are stale.

```sql
docs(key, basis, message_id, subject, sender, date_epoch, thread_root, body_chars, fts_rowid)
occurrences(path, doc_key, outcome, inode, mtime_ms, ctime_ms, size_bytes, mailbox, seen_in_build)
attachment_parts(build_id, path, part_id, filename, declared_type, sniffed_type, size_bytes, outcome, chars)
```

The join column is **`occurrences.doc_key`**, not `key`. One message has several paths (INBOX and All Mail), and
`attachment_parts` has one row per build, so `group by docs.key` with `distinct` on filenames is mandatory or every
count doubles.

### Find the billing sender before searching for anything

```sql
select lower(sender), count(*) from docs
 where lower(sender) like '%<vendor>%' group by 1 order by 2 desc limit 30;
```

This is what separates `"Vendor Inc." <invoice+statements@vendor.com>` from six hundred
`notifications@vendor.com` messages. Search by sender, not by keyword.

### Measured quirks, each a silent failure

- **Unknown parameter names are dropped without error.** A search taking `after`/`before` where the API wants
  `afterEpochSeconds`/`beforeEpochSeconds` returns results for the whole mailbox and looks correct. A published
  conclusion was built on this and had to be retracted.
- **A filters-only search with no query term returns zero.** It falls back to subject-only mode. A search with no
  text term is not an enumeration; query the index directly instead.
- **`limit` is capped at 200,** and a response of exactly the limit is truncation.
- **Attachment bytes are usually absent.** `.partial.emlx` carries the MIME structure and the text parts with
  **zero-byte attachment payloads** — Mail never downloaded them. `attachment_parts.size_bytes` is `0` even where
  `outcome` is `extracted`.
- **Index coverage is not 100%** (95.6% measured). Every response carries `coverage` and `partial`. Read them.
- **Attachment text is not indexed at all.** A body search can never find a figure that lives only in a PDF.

### What to do when the bytes are absent

Three workarounds, all used successfully:

1. **The attachment filename is still identity.** `Invoice-<PREFIX>-NNNN.pdf` in the index is how three separate
   billing accounts at one supplier were discovered without opening a single PDF.
2. **The `text/plain` part carries every figure** — amount, invoice number, receipt number, card last-4, line items,
   tax. Parse the body.
3. **Ask the operator to open the message** so Mail downloads the attachment. On a real run this returned nineteen
   invoices within minutes.

Reading a `.partial.emlx`: strip the leading bare-integer byte-count line, and the trailing Apple plist beginning
`<?xml version="1.0" encoding="UTF-8"?>`.

```python
raw = open(path, 'rb').read()
nl = raw.find(b'\n')
if raw[:nl].strip().isdigit(): raw = raw[nl+1:]
msg = email.message_from_bytes(raw, policy=email.policy.default)
```

### The rule this section exists for

**Absence of mail is not absence of an account.** On a real run, a vendor had never emailed a company address in a
whole year, and reasoning from that silence pointed at the wrong account entirely. The invoice settled it. Silence
in one channel says nothing about another.

---

## 4. The downloads folder

Where manually-saved and operator-supplied invoices land. Sweep by modification time, not by name:

```bash
cd "$VOUCH_DOWNLOADS" && ls -1t *.pdf | head -40 | while read f; do
  printf '%s  %s\n' "$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$f")" "$f"
done
```

BSD `find -newermt '-25 minutes'` returned nothing on macOS in testing; the `ls -1t` + `stat` form works.

Dedupe on the **invoice number extracted from content**, never on filename — re-downloading produces
`INV91142335 (1).pdf`.

## A card statement is evidence, and it never enters the claim folder

The statement answers one question and it is not "what was this charge for". It answers
**"was this paid personally"**, and it is reached for only when the card's last four digits
cannot be found any other way — the invoice usually does not name a card at all (measured:
1 document in 96 did), and a receipt that names one settles the question without a
statement.

So it is read where it lies. Never copy one into the claim folder, and never cite one as a
row's document:

- **It carries every other transaction on that card for the month.** The folder goes to an
  approver and an accountant. Filing one statement to substantiate an A$26.00 charge
  discloses the cardholder's rent, their medical spend and their groceries to two people
  who asked for none of it.
- **It is not what the row is keyed to.** Every claimed row is keyed to the supplier's
  invoice; a statement proves the payment, not the purchase, and a folder where the two
  are mixed cannot be reconciled by counting.

`validate.py` fails on any filed document carrying a statement marker, so the rule is a
gate rather than a habit. Statements live wherever the operator keeps them, are passed to
the run by path, and the run reads them.

The one thing worth extracting from them is the **cycle**, which
`wanted_invoices.py --statements` reads: the closing day and the periods already held.
That produces one sentence naming the card and the window whose statement is missing,
which is a fact about the card rather than about any charge and belongs at the top of the
page rather than repeated down a column.

## A curated ledger, where the household already keeps one

The sources above are raw: a bank feed, a mailbox, a folder of PDFs. Some households run a
ledger of their own on top of those, and where one exposes its reads over MCP it is a better
starting point than the feed — the rows are already deduplicated, already attributed to an
account, and already carry whatever the household has decided about them.

Read it as a SOURCE and never as a verdict. A ledger's own classification is one more piece
of evidence, at whatever rung its provenance earns: a row a person confirmed is strong, a row
a model proposed is not, and the ledger usually says which. Where such a system writes back,
prefer its own attended importer over direct database access — it will have the idempotence,
the dry run and the ownership rules already, and a claim tool reaching around them is how a
feed clobbers a decision.
