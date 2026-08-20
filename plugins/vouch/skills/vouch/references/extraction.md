# Extraction

Getting a supplier, a date, an invoice number, a total, a bill-to and a card out of a folder of PDFs that share no
format.

## PDF text: PDFKit via Swift

`strings` on a PDF returns metadata only; the content streams are compressed. On macOS, PDFKit is the reliable
extractor and needs no Python dependency.

**Write the code to a file and run it.** `swift -e '<code>'` invoked from a subprocess produced empty stdout for
every file with a clean exit status — a silent success. Compile once for repeated batches:

```bash
swiftc -O scripts/pdftext.swift -o /tmp/pdftext
find "$VOUCH_DOWNLOADS" -maxdepth 2 -name '*.pdf' -mtime -30 -print0 | xargs -0 /tmp/pdftext
```

### What PDFKit does to the text

- **Inserts spaces inside numbers.** `US$17 .50` is real. Never trust a single occurrence of a figure; cross-check
  two places in the same document.
- **Loses table alignment.** Labels arrive as a run, then values as a run, so Subtotal/GST/Total often need
  positional trio matching rather than label-adjacent matching.
- **Breaks the line after a label.** Every label pattern needs `\s*\n?\s*` between the label and its value.

## Supplier resolution, three stages in order

**1. Invoice-number prefix.** The strongest signal, because it is also the *account* discriminator (R3). Build the
map as you go; an unseen prefix is a new account needing classification, not the known one.

**2. Issuer text marker**, lowercased. Note that some suppliers never print their brand name in the extractable
text — one is identified only by its street address. Key on whatever is actually in the document.

**3. Filename shape**, as a last resort: `^\d{10}\.pdf$`, `^INV\d+`, `^invoice_[A-Z]{4}\d+`.

Skip statements in the corpus, or they match every amount in it:

```python
if 'Statement of Account' in t[:600] and '<bank name>' in t[:600]: continue
```

## Invoice-number patterns

Ten, tried in order. The set is wide because vendors disagree on almost everything:

```python
r'Invoice number:?\s*\n?\s*([A-Za-z0-9][A-Za-z0-9\-\._]{2,40})'
r'Invoice reference:?\s*\n?\s*([A-Z0-9\-]{4,40})'
r'Invoice #\s*([A-Za-z0-9\-\._]{2,40})'
r'Invoice no\.?\s*:?\s*([A-Za-z0-9\-\._]{2,40})'
r'Invoice ID[:\s]*([A-Za-z0-9\-\._]{2,40})'
r'Invoice:\s*\n?\s*([0-9a-f]{32})'        # bare hex id after a label block
r'Receipt number\s*\n?\s*([0-9\-]{4,40})'
r'Order number[:\s]*([A-Za-z0-9\-\._]{2,40})'
r'Billing Number\s+(\S+)'
r'Transaction ID\s+(\S+)'
```

**One supplier changed its label mid-series** — `Invoice number:` for eight months, then `Invoice reference:` — and
the first parse returned nothing for fifteen of nineteen documents. Try both, always.

## Date patterns

```python
r'Date paid\s*\n?\s*([A-Za-z]+ \d{1,2}, \d{4})'
r'Date paid\s*\n?\s*(\d{1,2} <Month> \d{4})'
r'Date of issue\s*\n?\s*(...)'
r'Invoice date\s*\n?[\.\s]*\n?\s*(\d{1,2} [A-Z][a-z]{2} \d{4})'   # dotted-leader layouts
r'Issue Date\s*\n?\s*(...)'
r'\b(\d{4}-\d{2}-\d{2})\b'
```

Parse with `('%B %d, %Y','%d %B %Y','%b %d, %Y','%d %b %Y','%Y-%m-%d')`.

**Widen the month abbreviation to `[A-Za-z]{3,}`** — a real date read `30 Sept 2025` and a `{3}` pattern missed it.

## Total patterns

```python
r'Amount paid\s*\n?\s*(?:US|AU|A)?\$?\s*([\d,]+\.\d\d)'
r'Amount due\s*\n?\s*(?:US|AU|A)?\$?\s*([\d,]+\.\d\d)'
r'\bTotal\s*\n?\s*(?:US|AU|A)?\$?\s*([\d,]+\.\d\d)'
r'Total (?:in )?(?:AUD|USD)\s*\$?\s*([\d,]+\.\d\d)'
r'TOTAL\s*\$\s*([\d,]+\.\d\d)'
r'Total amount\s*\n?\s*(?:AU|US)?\$?\s*([\d,]+\.\d\d)'
```

Layer fallbacks rather than trusting one: a single pattern silently returned `-` on six of thirteen invoices, and a
`-` reads as zero downstream.

## Bill-to and the customer's email

Scope to the block, and note the capital: some suppliers write `Bill To`.

```python
bt = re.search(r'Bill [Tt]o\s*\n(.{0,200})', t, re.S)
```

Extract every email, then **subtract the vendor's own domains**. What is left is the customer's address. Maintain
the denylist as you go; it is short and stable per supplier.

## Card detection

The regex that works, anchored on the scheme name with a permissive gap:

```python
re.findall(r'(American Express|Visa|Mastercard|MasterCard)[^\n]{0,30}?(\d{4})\b', t)
```

A narrower `scheme\s*[-–]\s*(\d{4})` form found 16 cards in a corpus where this form found 46. A bare `\d{4}$`
sweep is worthless: the top hits are years, postcodes and tax registration numbers.

Also seen in real documents: `XXXX-XXXX-XXXX-3003`, `4*** **** **** 7812`, `• • • • 3003` (spaced bullets),
`ending in 3003`.

## GST and tax lines

Extract the three fields **separately** and cross-check `ex + tax == total`. A single regex with a `.last` on the
split returned the base amount where the tax was wanted, on every row, and the error is invisible because both are
plausible figures.

Watch for the local-currency equivalent printed in parentheses on a foreign-currency invoice —
`GST - Australia (10% on $5.00) $0.50` followed by `(A$0.73)` on the next line. The parenthesised figure is the one
the claim needs.

**A foreign-currency total stating local GST is not the same document as a local-currency invoice.** Where the
treatment is ambiguous, state the arithmetic and leave the characterisation to the accountant.

## Vendor CSV exports

Where a vendor offers an account-activity export, it is often better than the invoices for reconciliation because
it records **declines and retries** the bank feed never shows:

```
2026-03-01 DECLINED  →  2026-03-03 auto
2026-04-01 DECLINED  →  2026-04-09 manual
```

The feed shows only the successful charge, on the later date, which is why two identical amounts a month apart are
two payments rather than a duplicate.

These files commonly carry a UTF-8 BOM (`encoding='utf-8-sig'`) and a Unicode minus (U+2212) rather than a hyphen.

## A pattern that cannot fire is worse than no pattern

Three extraction bugs on one real run, all the same shape: the regex ran, matched nothing
or the wrong group, and the result read as a clean measurement.

| Pattern | What happened | Fix |
|---|---|---|
| `@(gmail\|rhodes\.gg\|outlook)\.` | required a trailing dot, so `luke@rhodes.gg` never matched and the personal-email check silently never fired | anchor on the domain, not on a following character |
| `Bill(?:ed)? [Tt]o` | case-sensitive, so a supplier printing `BILL TO` fell through to the page header, which then read as the addressee | `re.I`, and list every label a real supplier uses |
| `GST[^\n]*?\n?\s*([\d,]+\.\d\d)` | on `GST - Australia (10% on A$309.09) A$30.91` it returned **309.09**, the base the tax is computed on | capture *after* the rate clause, and sanity-check the result is smaller than the net |

So: **every extraction pattern is proved against a document it should match and one it
should not.** A pattern with only a positive case is a pattern nobody has tested. The
third bug above was caught by gate 21 rather than by review, which is the argument for
having a magnitude check at all.

And when a check reports a clean result over a whole corpus, ask what it would report on
a corpus built to defeat it. A filename audit that passed 88 of 88 also passed two
documents whose filenames had been deliberately swapped.
