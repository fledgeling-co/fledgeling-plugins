# Evidence

Every rule in this skill traces to one of three things: a defect measured on a real run, a measured fact about a
tool, or a published source. Nothing here is instinct. Where a rule has no evidence behind it, it is marked as a
default rather than a finding.

## The run this skill is derived from

One claim, assembled and delivered in August 2026, covering 7 August 2025 to 30 June 2026.

| | |
|---|---|
| Charges claimed | 88 at first delivery; 95 after four operator review passes tightened the account test |
| Suppliers | 18 |
| Months | 11 |
| Documents filed | 88 (87 PDF, 1 `.eml`) |
| Claim | A$6,936.69 at first delivery; A$7,477.27 after extension to date and four rounds of exclusions |
| Gate result | `PASS 24 · WARN 1 · FAIL 0` (re-run after the banner fix below, so the audit was armed) |
| Filename-versus-content audit | 88 matched · 0 mismatch · 0 missing · 0 unreadable · 0 orphans |

The claim went out with a schedule, a folder of month-foldered invoices, and two HTML reports. Every number in
this file was read off that run rather than estimated.

## Defects the run produced, and the rule each became

| What happened | Rule |
|---|---|
| A keyword search whose date filter was silently ignored returned a confident wrong answer; enumerating the index directly retracted it | Every negative result states its instrument (SKILL.md, "The one rule") |
| 14 rows were filed under the wrong month, keyed to a vendor's monthly billing email rather than to the invoice | Gate 15: filename must appear inside the document |
| Two identical top-ups four days apart both matched whichever invoice returned first: 7 of 10 assigned, 2 ambiguous | Assignment with a `used` set on both sides: 9 of 10, and the tenth correctly identified as another account's |
| Two feed gaps of 38 and 44 days on the primary card, invisible until computed, held claimable charges | `scripts/find_blind_days.py`, run before any matching |
| A 333-row extract stood in for a 2,444-row feed and had dropped 5 claimable charges | Never reason from a pre-filtered extract |
| One vendor billed three separate accounts from the same cards; only one was the company's | The invoice-number prefix discriminates accounts, not the vendor name |
| Two charges were about to be claimed from a rate no document states | The claimed amount is what the card was charged; the statement was found and it was 34c and 21c above the derived figure |
| The prior year's form held its tax figures under the ex-tax header on every row | Write in header order; state the divergence; gate 21 catches the shape |
| A tax-inclusive classification subtotal sat under the ex-tax heading in the delivered CSV | Every subtotal sits under its own header (`build_csv.py`) |
| Five hardcoded counts survived a move from 66 rows to 68; one then survived the move to 88 | No figure is typed into prose; all are derived at render |
| Two rebuilds landed in `/tmp` while the delivered folder kept stale copies | Absolute output paths in every builder; both refuse a relative one |
| A report's data file drifted from the row source and rendered stale totals with no error | One source of truth, regenerated on every build |
| A report claimed a filing convention that was never used, and named the wrong supplier as billing from overseas | Read the prose against the data once, deliberately, at the end |
| A row/file reconciliation globbed only `*.pdf`, so an `.eml` reported absent while sitting on disk | Audit every filed extension; read non-PDFs as text |
| A `<colgroup>` declared six columns against seven headers, and long ids overlapped the next column | Assert before replace on every builder patch |
| `word-break: break-all`, correct while the last column was a number, chopped prose mid-word once a text column was appended | Scope it to `td.n:last-child` |
| `overflow-wrap: anywhere` rendered a category as "Developm / ent & / Infrastruct / ure" at 375px | `break-word`: only an unbreakable word breaks, so the table scrolls instead |
| `.grid2 .card{overflow-x:auto}` alone did not fix a 467px overflow at 375px (467 → 439) | Both the card *and* the grid track: `.card:has(table){overflow-x:auto}` **and** `.grid2>*{min-width:0}` |
| A 1.96:1 contrast failure on the single most important number in the document | The accent that passes on white fails on the inverted band; each band gets its own token |
| A 300-character classification reason repeated on 88 rows produced ten identical paragraphs | A short operative clause per row, one basis entry per supplier |
| **A regex that could not fire.** The personal-email pattern required a trailing dot, so `luke@rhodes.gg` never matched and the check reported clean over four review passes | Anchor on the domain; prove every pattern against a document it should match AND one it should not |
| **A case-sensitive bill-to matcher.** `Bill To` missed a supplier printing `BILL TO`, fell through to the page header, and reported the vendor's own address as the addressee | `re.I`, and enumerate every label a real supplier uses |
| **A tax pattern that captured the base.** On `GST - Australia (10% on A$309.09) A$30.91` it returned 309.09 | Capture after the rate clause; gate 21 caught it, which is the argument for the magnitude check |
| **One row matched four identical charges** in a single week, any of which would have supported it | Verification runs the same one-to-one pin the matching does |
| **A statement checked by substring.** `34.00` matches inside `340.00`, and a repeated monthly figure identifies no particular charge | Match a line carrying merchant and amount; where the supplier repeats a figure, say the statement cannot settle it |
| **Prose rotted on removal, five times.** Three literals summing to a stale row count, a "two from 2025" where one remained, a hardcoded "seven rows", and a lede claiming what the caveats withdrew | No integer or money literal in report prose, spelled numbers included; the lede is bound by the caveats |
| **An invented worked example.** A note illustrating a prior form's transposed columns quoted a figure that appears nowhere in that file; read properly, its tax column was empty on 92 of 93 rows | Compute the example from the artefact, or give none |
| **A whole supplier sat one rung too high.** Eleven rows, A$1,579.45, showed "company named, no email" because the email check could not fire; they were "company named, personal contact" | `classify_accounts.py`: all six rungs, per supplier, with counts and values |
| **This skill's own filename audit was vacuous.** The extractor prints a `=== <path> ===` banner and the fallback match searched it, so every file matched its own name whatever was inside it | Strip the banner in `read()`; proved red by swapping two documents' filenames (88/88 before, 86/88 and both named after) |

## Measured tool facts

Each was measured on this machine during the run. A tool that can succeed while doing nothing is the recurring
shape, so each fact names the control that exposed it.

**`timeout` does not exist on macOS.** `(eval):2: command not found: timeout`. Use
`perl -e 'alarm shift @ARGV; exec @ARGV' <secs> <command>`.

**The mail MCP's `search` silently ignores `after` / `before`.** The parameters it reads are
`afterEpochSeconds` / `beforeEpochSeconds`, and a filters-only search with no `query` falls back to a subject-only
mode returning zero. Enumerate the index SQLite instead. `occurrences` joins on `doc_key` to `docs.key`; there is
no `key` column on `occurrences`.

**Apple Mail `.partial.emlx` carries zero-byte attachment payloads.** `attachment_parts.size_bytes` reads `0` even
where `outcome` is `extracted`. The filename is still identity, and the `text/plain` body still carries the
figures; opening the message in Mail makes it fetch the bytes.

**Stripe hosted-invoice links from email expire, and the failure exits 0.** `curl -sL '<url>/pdf?s=em'` returned
745 bytes of HTML reading "This link expired". Check the body, never the exit code.

**Cloudflare blocks an automated browser even with the operator's real Chrome profile.** Two supplier portals
returned a verification interstitial and a block page respectively. This is a hard boundary; hand off.

**A vendor changed its invoice-id label mid-series** — `Invoice number:` through April 2026, then
`Invoice reference:` from June. The first parse returned `(none in pdf)` for 15 of 19 documents.

**PocketSmith's `per_page=500` returned exactly 500.** A response equal to the limit is a truncation signal, not a
count. Paginate.

**`swift -e '<code>'` under a subprocess returns empty stdout with a clean exit.** Write a `.swift` file; compile
once with `swiftc -O` for repeated batches.

**BSD `find -newermt '-12 minutes'` returns nothing on macOS.** Use `ls -1t` with `stat -f '%Sm'`.

**Obscura serves a blank page over loopback without `--allow-private-network`, and the capture still succeeds.**
A 70KB all-white PNG was written with no error. The control is the file size and the DOM: a probe reporting
`tables: 0` on a page with three tables is the instrument failing, not the page.

**Obscura's `canvas.measureText` is not a measurement.** Measured 20 August 2026: it returns a fixed
`0.42 × fontSize` per character regardless of glyph — `i` and `W` both 6px at 14px, `48px serif` giving 30px for a
single `i` — and the layout engine puts eight monospace characters at 68px where canvas says 48. A text-fitting
probe built on it returns numbers in the right units that are not measurements of anything. The layout engine is
correct: measure with an absolutely positioned `white-space: pre` span.

**Obscura's computed-style shorthands under-report.** `padding`, `margin` and `borderRadius` return `0px` where
the CSS sets real values; the longhands are correct. Expand every shorthand before asserting on spacing.

## What four review passes cost, and why that is the finding

The claim was delivered, then reviewed by its owner four times. Each pass moved the account
bar and each removed rows the pass before had not questioned: a supplier billing the company
with a personal contact, two model-API accounts, a personal subscription bought on a work
address. **No pass found an arithmetic error and every pass found an attribution error.**

That asymmetry is the case for `classify_accounts.py`. The arithmetic was gated from the
first run and never moved. The account test was applied one row at a time, so each pass saw
one more shape of it for the first time, and four rounds bought what one census would have.

## Published sources

The R&D classification shipped with the run rests on a five-backend research panel run in August 2026 at a metered
cost of US$20.32 across 110 sources. Its load-bearing findings, each traced to primary law or ATO material:

- Division 355 of the *Income Tax Assessment Act 1997* — the notional-deduction regime. There is no eligible-vendor
  list; eligibility attaches to activities, not to suppliers.
- s 355-225(2) — expenditure on **core technology** is excluded from notional deductions.
- The **dominant purpose** test for supporting activities.
- TA 2017/5 — the Commissioner's alert on software-development claims.
- Notional deductions are **GST-exclusive** where the entity is registered and entitled to an input tax credit.
- The **A$20,000 minimum** aggregate notional deduction before the offset is available.
- The named apportionment method for period-of-use expenditure is **R&D hours over total employee hours**.

The consequence for this skill is the rule in SKILL.md: a classification column is a **default position on the face
of the expense**, never a percentage and never a characterisation. The skill states arithmetic and cites documents;
the characterisation belongs to the accountant.

## What has not been measured

Named so a later reader can tell a gap from a finding.

- **No jurisdiction but Australia has been exercised.** The tax-rate checks are parameterised and the vocabulary is
  configurable, but no run has produced a VAT claim.
- **No accounting provider but PocketSmith has been driven**, and that through its REST API rather than its MCP.
  The provider-neutral shape in `references/sources.md` is a design, not a measurement.
- **No mail source but the Sift Apple Mail index has been read.**
- **The reports have not been read by their intended audiences.** They passed a rendered-output review; approval
  and bookkeeping are the tests they exist for and neither has run.
- **No unattended end-to-end run has happened.** Every stage has run, and the gates have been shown red and green,
  but the operator was present throughout.
