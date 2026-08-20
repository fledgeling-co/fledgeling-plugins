# Outputs

Three artefacts, all generated from one source on every build. Nothing is edited by hand, and no figure is typed
into prose.

## The single source of truth

`claim_rows.json` — one object per claimed charge:

```json
{
  "date": "2025-08-10",
  "desc": "Issue tracking subscription",
  "vendor": "Linear",
  "cat": "Productivity & Business Tools",
  "why": "Issue tracking for the engineering team.",
  "inv": "3IFUYPUC-0002",
  "ex": 47.45, "gst": 0.0, "inc": 47.45,
  "file": "3IFUYPUC-0002.pdf",
  "file_rel": "2025-08/3IFUYPUC-0002.pdf"
}
```

`vendor` groups the reports; `why` is a plain-English sentence on what the supplier does for the company, and a
build **fails** if any supplier lacks one. `cat` groups the category table.

**Every count in every template derives from this file.** Hardcoded counts have rotted twice on real runs: a report
whose `Total` row read 66 while the rows above it summed to 68, and a lede reading "Sixty-eight charges" over
eighty-eight rows. Derive `N`, derive the word form, derive the largest category and its average, derive the two
biggest suppliers and the single dominant invoice.

## The claim CSV

Match the employer's form, including its conventions. Copy its column headers **byte for byte**, spacing included.

```csv
Expense Claim Form,,,,,
Applicant Name: ,<name>,,,,
,,,,,
Expense Period :,<M/YYYY - M/YYYY>,,,,
,,,,,
Date,Description,Invoice No.,Amount    (excl. GST),GST,Amount      (incl. GST)
10/08/2025,Issue tracking subscription,3IFUYPUC-0002,-47.45,0,-47.45
...
,,Total,-6543.47,-393.22,-6936.69
,,,,,
,,,,Bank Account,
,,,,Account Name:,<name>
,,,,BSB: ,<bsb>
,,,,Account No: ,<acct>
,,,,,
,,,,Applicant Signature,
,,,,Date:,
```

Conventions that matter and are easy to lose:

- Dates `dd/mm/YYYY`.
- **All money negative**, if that is what the employer's form does. A zero is the bare string `0`, not `-0.00`.
- Trailing spaces in `"Applicant Name: "`, `"BSB: "`, `"Account No: "` are deliberate; they byte-match the form.
- Written with `csv.writer` and `newline=''`, so CRLF. Excel-friendly, and not a defect.
- Every line padded to the full column count, including the blank separator rows.

**Where the employer's form transposes two columns against their headers**, write the values in header order and
**state the divergence prominently** in the accountant's report, with the concrete example. A column-by-column
comparison against last year then reads as deliberate rather than as an error. This is real: one form held the GST
figure under the ex-GST header on every row.

### Optional classification columns

Where `VOUCH_CLASSIFY` is set, append two columns and a subtotal row:

```csv
...,Amount      (incl. GST),<Class>,<Class> reason
...,-47.45,TRUE,"Supporting activity; apportion on ..."
,,Total,-6543.47,-393.22,-6936.69,,
,,<Class>-eligible total,-5152.63,,69 of 88 charges,,
```

Values are `TRUE`/`FALSE`/empty only, and a row carrying a verdict must carry a reason. Build the columns as
**dormant plumbing** keyed on an optional file, so all three artefacts build clean whether or not the
classification exists — that pattern lets the schedule ship while the research runs.

## The directory

```
<out-dir>/
├── 2025-08/ … 2026-06/          one folder per calendar month, YYYY-MM
│     <invoice-number>.pdf       named for the number printed INSIDE the document
│     <invoice-number>.eml       where a vendor issues no PDF
├── <employer's form name>.csv
├── Approval.html
└── Accounting.html
```

**Invariant, asserted by the gate:** every row cites exactly one file, every file is cited by exactly one row, and
no file is orphaned.

Naming by invoice number rather than by date-and-slug makes the attachment path derivable from the row
(`<month>/<invoice no.>`), which lets the schedule drop its attachment column entirely.

## Report 1 — the approver

For a manager or CFO deciding whether to pay. Templates in `assets/report-approval.html`.

| Block | Content |
|---|---|
| **Masthead** | What this is, in one sentence. The claimant's own voice. |
| **Fact bar** | Total incl. tax · tax included · charge count · invoices attached |
| **§01 What this is, and what it is not** | Why the costs sit on a personal card; the three gates; a category table with amounts; a "shape of it" card naming the two largest suppliers and the single dominant invoice, all derived |
| **§02 Every supplier, and what it does** | One row per supplier by amount descending: name, the purpose sentence, period total, charge count |
| **§03 Items worth a moment of your attention** | The judgement calls, each with both treatments named and a recommendation. Not errors — decisions that belong to the reader |
| **Sign-off** | Navy panel: the total, one sentence restating count/period/evidence, two signature lines |
| **Footer** | Prepared date, the CSV filename, where invoices are filed, pointer to the companion report |

The approver's report answers one question: **is this number a result or an assertion?** Everything in it serves
that.

## Report 2 — the accountant

Templates in `assets/report-accounting.html`.

| Block | Content |
|---|---|
| **Masthead + fact bar** | Total incl. · total excl. · tax · rows carrying tax |
| **§01 Things to know before reading the schedule** | The column-order divergence with its concrete example; the sign convention; the no-overlap proof with both tests and the sequence-continuity evidence |
| **§02 Tax, and the question it raises** | Tax by supplier; the never-derive rule; non-resident suppliers stating local tax, handed to the accountant rather than decided |
| **§03 How each figure was established** | Three cards: the invoice sets the identity; the card sets the ownership (the full card map); foreign currency |
| **§04 By month** | Monthly totals |
| **§05 Full schedule** | The line-item table, plus the attachment convention with a worked example |

## Rendering both

Serve over HTTP and route to `design-review`. Two findings from a real run that no source reading would have caught:

- The most important number in the document, the sign-off total, rendered at **1.96:1** against a 3:1 floor,
  because a nested `em` inherited an accent colour the parent override never reached.
- Horizontal overflow at 375px that survived the obvious fix, because the grid track was still sizing to content —
  it needed `overflow-x: auto` on the card **and** `min-width: 0` on the grid child.

Then lint the prose extracted from the **built HTML**, not from the builder source, so the check covers what the
reader sees.

## The templates, and what makes them unbranded

There is no logo, no employer name and no colour that belongs to anybody. The reports
identify the claimant and the period and nothing else, so the same pair serves any
company. What varies lives in two config files, both shipped as examples:

- `assets/form.example.json` — the employer's claim form as data: preamble, column
  headings copied verbatim, the date format, the sign convention, and the footer blocks.
  Copy their headings exactly, whitespace and all. A heading retyped tidily no longer
  matches the form somebody will compare this against.
- `assets/report.example.json` — the claimant, the period label, the currency, the name
  of the consumption tax and its rate, and an optional classification column. Set
  `tax_name` to `VAT` and `currency` to `£` and nothing else changes.

`assets/report.css` is shared by both reports. Every rule in it carrying a comment is
there because the plain version shipped a defect that a rendered-output review caught,
and the comment names the defect. Read those before simplifying one away.

Omit the `classification` block and both reports drop the column, the verdict cells and
the per-supplier basis table, with no other change. A classification column that is
half-filled is worse than no column, so it is all or nothing.

**The approver's report shows amounts including tax, the accountant's shows all three.**
That is not a style choice: the approver is signing off a payment, which is the
inclusive figure, and the accountant needs the split. Where a deduction is at issue, the
ex-tax column is the one to work from and the accountant's report says so.

## An exclusion needs somewhere to go, and a reason

A row that comes out is not deleted. Three destinations, and the choice says which:

- **`<claim>-excluded/`** — the document moves out of the claim folder so the orphan gate
  stays meaningful, and it stays on disk so the decision is reversible. Every removal on a
  real run was reversed at least once.
- **The reports** — the reason, in a sentence, in the section that covers judgement calls.
  A number that reads as a result rather than an assertion is one whose exclusions are
  visible.
- **The wanted-invoices page** — but only where the row could still come back. A row
  excluded because its *account* is not the company's never comes back, and putting it
  there re-proposes it.

## The hand-off page has four kinds, not one

Each is a different problem with a different repair, and summing them into one number
makes the page's own opening sentence untrue:

| kind | The state | The repair |
|---|---|---|
| `portal` | a charge with no invoice anywhere | sign in and download |
| `mail` | the invoice is attached to a message the client never downloaded | open the message |
| `account` | charge and invoice both exist, and the invoice names a non-company contact | change the billing contact, re-issue |
| `statement` | the invoice exists and no charge has reached the feed | a card statement |

`account` is the one added last and the one worth having: it takes the whole supplier with
it, both the documented rows and the charges that have no invoice yet, because any invoice
those produce carries the same contact.

Where several accounts exist at one supplier and only some are the company's, say so on
each row of the page. An invoice recovered and filed on the supplier's name alone will
quietly re-introduce the account that was excluded.

## The hand-off page lists only what would actually enter the claim

A work list that contains work nobody will use is not a work list. An item stays on the
page only where the supplier already has a **verified company account in the claim** —
otherwise recovering the invoice produces a document for an account nobody has established
belongs to the company, and the recovered row then has to be argued about from scratch.

On a real run that filter removed 47 of 87 items worth A$6,489.02: a supplier excluded for
naming a personal contact, and four suppliers whose invoices had never been checked against
a company account at all. Report the removal as a count and name the suppliers in the
report, because a page that silently shrinks reads as work completed.

The rule also runs backwards. When an *account* is excluded, drop every outstanding item
that would resolve to it — other invoices on the same number prefix, charges with no
invoice that belong to it, and any orphan invoice waiting on a statement. On a real run two
orphan invoices carried the prefix of an account excluded ten minutes earlier, and chasing
a statement for them would have put the row back.

## Facts the operator already holds are read, not asked for

The statement cycle is the worked example. A charge on the 1st and a charge on the 20th of
one month sit in **different** statements wherever the cycle closes mid-month, so a page
that says "check the July statement" sends someone to the wrong document half the time.

The closing day is not a question to put to the operator. They have the statements, and
the day is a fact those files carry: `statement_cadence()` reads an ISO date out of each
filename, falls back to a closing date inside the document text, and infers the cycle from
what it finds. Asking for it as a flag invites a typo that misroutes every row silently.

Two behaviours make it safe to rely on:

- **Fewer than two statements, or observed days that disagree, means no cadence.** The
  column is dropped and the run says why. A cycle guessed from conflicting evidence is
  worse than no cycle, because it looks like knowledge.
- **The periods already held are derived from the same read**, so each row says not merely
  which statement covers it but whether that one is missing. That is the difference between
  a list of work and a list of facts.

The general rule: where the operator's own material already carries a fact, read it. A flag
that restates something on disk is a second source of truth with no gate between them.
