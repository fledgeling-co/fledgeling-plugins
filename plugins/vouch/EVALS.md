# Evals

**No eval run happened.** No blind judge panel, no A/B against a no-skill baseline, no
scored comparison of any kind. This skill was built from one real claim rather than
benchmarked, at the request of the person it was built for, and the honest reading is
that nothing here tells you whether the skill beats doing the same work without it.

What follows is what *was* verified, mechanically, and what would settle the question.

## What was verified

Everything below was run against a real 88-charge claim covering 7 August 2025 to
30 June 2026, and against fixtures deliberately broken to watch each check fail.

### The gate suite goes green on a correct claim

```
PASS 24   WARN 1   FAIL 0
```

The single warning is CRLF line endings, which the employer's own form uses and which
the suite reports rather than treats as a defect.

### The gate suite goes red on each defect it claims to catch

Eight fixtures, each one a copy of the real claim with a single defect introduced. The
column shows only the failures attributable to the fixture.

| Fixture | What was broken | What fired |
|---|---|---|
| R1 | Ex-tax and tax transposed on one row, totals untouched | The magnitude check, plus two of the three totals |
| R2 | **The whole column transposed and the totals recomputed from it** | The magnitude check alone, on all 88 rows. Every other check passed |
| R3 | One date moved a year earlier | Date outside the period, plus the CSV/source field comparison |
| R4 | An invoice number duplicated onto a second row | Duplicate invoice numbers, plus the field comparison |
| R5 | One row's amount edited by 100.00 | Two of the three totals, plus the field comparison |
| R6 | Two rows swapped out of date order | Date order, plus six field comparisons |
| R7 | One row's signs flipped | Sign convention, plus two of the three totals |
| R8 | A filed document renamed | File missing, plus one orphan on disk |

R2 is the one worth reading. It passed every check the suite had until the magnitude
check was added, because **transposing two values preserves their sum** and the totals
were recomputed from the transposed column. The suite's own oldest check, the one that
found a real transposition in a prior year's form, is blind to it.

### Two absences that were one transaction

A later sweep asked a different question of the finished claim: not "is any row wrong" but
"is any transaction in neither list". Three were, and the reason is the one this section
exists to record.

The run ends with two lists described as opposites: charges with no document, documents
with no charge. A supplier prints its receipts as `$24.20` with an Australian GST line
underneath; the extractor recorded the currency as AUD. The card had converted the same
US$24.20 to A$36.17, so the two figures never matched, the receipt went to one list and
its charge to the other, and **each list was internally consistent**. Every gate passed.
Both pages read as thorough. The transaction was in neither the claim nor anywhere a
reader would look for it.

`scripts/cross_check.py` now pairs the two lists on supplier, a few days and a ratio
inside the observed conversion band, and exits non-zero on a hit. Shown red against the
real files (three pairs, ratios 1.4909, 1.4946 and 1.4649) and green once the three rows
moved into the claim. V-20 holds it to a fixture that must pair and one that must not, so
a hit-nothing run is distinguishable from a check that stopped working.

The general lesson outlives the currency bug: **two errors in opposite directions look
like two findings**, and a report listing both reads as more thorough than one listing
neither. Any run ending with two "missing" lists over one population should test them
against each other before publishing either.

### One of this skill's own checks was found vacuous, and re-armed

The filename-versus-document audit reported 88 of 88 matched. It was then given a
fixture with two documents' filenames swapped, each verified to hold the other's
invoice number, and it **still reported 88 of 88**.

The extractor prints a `=== <path> ===` banner ahead of each document so a batch can be
split. The audit's fallback arm looked for the filename anywhere in the extracted text,
and the banner is the filename, so every file matched its own name whatever was inside
it. It would have returned 88 of 88 on 88 randomly named files.

With the banner stripped, the same fixture reports 86 matched and names both
mismatches with the id it found instead. The real claim re-runs at 88 of 88 with the
check armed, which is the part that mattered: the claim was genuinely correct, not
passing through a hole.

### The builders reproduce the delivered artefacts

`build_csv.py`, driven from a form spec and the row source, reproduces the delivered
claim form **byte for byte**. `build_reports.py` renders both HTML reports from the same
source, and its output was probed at 1440, 768 and 375 pixels: no horizontal page
scroll at any width, with the tables scrolling inside their own cards as intended.

Building them found one defect in the delivered CSV that no gate had: the classification
subtotal carried a tax-**inclusive** figure under the ex-tax header, which is the one
column a notional deduction has to be read from. Fixed in both the delivered file and
the builder.

### The scripts run

`pdftext.swift` compiles clean under `swiftc -O`. `validate.py`, `audit_invoices.py`,
`match.py`, `find_blind_days.py`, `parse_invoices.py`, `parse_statement.py`, `build_csv.py`,
`build_reports.py` and `wanted_invoices.py` all run against real data and print a
denominator.

## What would settle the open question

Three tasks, in the order they would be worth running.

1. **The same claim, no skill.** Hand a model the same folder, the same accounting
   access and the same mailbox, and ask for a reimbursement claim. Score both outputs on
   structural properties rather than on quality: does every row cite a document, does
   every filed document match the row that cites it, is the arithmetic internally
   consistent, and is the count of excluded charges reported. This is the comparison
   that decides whether the skill earns its place in a context window.

2. **A second claimant, a different employer's form.** Everything about the form layout
   here is data rather than code, and that has been asserted rather than exercised. One
   run against a different form, a different tax vocabulary and a different accounting
   provider would tell you which parts generalised and which were written to one case.

3. **An unattended monthly run.** Every stage has run and every gate has been shown red
   and green, but the operator was present throughout. The claim in this skill is that
   an unattended run reaches the same standard, and that claim has not been tested once.

## What four review passes added

The claim this skill was built from was then reviewed by its owner four times, and each
pass tightened the account test. **No pass found an arithmetic error; every pass found an
attribution error.** The arithmetic had been gated from the first run and never moved,
while the account test was being applied one row at a time, so each pass met one more
shape of it for the first time.

That is the case for `classify_accounts.py`, added in 0.2.0: it puts every row on the
evidence ladder at once, per supplier, with counts and values. What four rounds bought,
one census would have.

Three defects in this skill's own instruments were found the same way and are fixed:

- A personal-email pattern requiring a trailing character, so a bare domain never matched
  and the check reported clean across four passes.
- A case-sensitive bill-to matcher that missed an uppercase label, fell through to the
  page header, and reported the vendor's own address as the addressee.
- A tax pattern that returned the base a tax was computed on rather than the tax.

All three are now held by `evals/check_patterns.py`, which asserts a fixture each pattern
must match **and** one it must refuse. It found a fourth on its first run: the tax pattern
only handled dollar signs, which made this skill's claim to work outside one jurisdiction
quietly untrue.

## Process notes

Recorded so a later reader can tell which checkpoints ran, and which did not.

- **The discovery interview ran**, and its two answers were the skill's name and the
  depth of the build.
- **No research panel was bought for the skill's domain.** The corpus is one real run,
  plus a five-backend panel on the Australian R&D Tax Incentive already run for the claim
  itself, exported into `docs/deep-research/` and cited from `references/evidence.md`.
- **skill-creator was not invoked.** Its requirements were met directly and can be checked:
  SKILL.md is under 300 lines with depth in references, every deterministic step is a
  bundled script, and the tests were written and run before anything was claimed working.
  This is a substitution, not a pass, and it is recorded here rather than implied.
- **The naming and icon checkpoints both ran.** The icon direction was chosen by the
  person from three subject-mined options.
- **The icon commission ran three engines and one failed.** Engine A is the hand-authored
  master that ships, widened to a second take to test the axis the raster raised. Engine C
  (a corpus-referenced raster) succeeded and won the material comparison; its findings were
  salvaged and its needle-thin filament was not, because it disappears by 32px. Engine B
  (Arrow, vector) **failed on the first attempt for want of gateway credit**, was rerun
  after the credit was added, and its take is in the sheet. `audit_sheet.py check` exits 0
  over four takes and the shipping take scores 11 of 12; the check it does not take is
  variant robustness, which is untested rather than passed.
