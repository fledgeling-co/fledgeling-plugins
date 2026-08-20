# Configuration and the operator interview

The claim cannot be decided without the operator's own facts. Guessing any of them corrupts every downstream row,
and two of them have been guessed wrong on a real run and corrected by a human.

## Environment variables

Every value below can be supplied as an environment variable so an unattended monthly run needs no interview. A
variable that is absent becomes a question; a variable that is present is trusted and echoed back in the run's
opening output so a wrong one is visible before any work depends on it.

| Variable | Shape | Example | What it decides |
|---|---|---|---|
| `VOUCH_PERIOD_START` | ISO date | `2025-08-07` | The window, applied to the **charge** date |
| `VOUCH_PERIOD_END` | ISO date | `2026-06-30` | Same |
| `VOUCH_CLAIMANT_NAME` | string | `Jane Smith` | The claim form and both reports |
| `VOUCH_CARDS_MINE` | comma-separated last-4 | `3003,2005` | Claimable |
| `VOUCH_CARDS_JOINT` | comma-separated last-4 | `7328` | Claimable — still personal money |
| `VOUCH_CARDS_COMPANY` | comma-separated last-4 | `7812` | **Never** claimable |
| `VOUCH_COMPANY_DOMAINS` | comma-separated | `example.com.au` | An invoice naming any address at these domains is a company account |
| `VOUCH_COMPANY_EMAILS` | comma-separated | `jane@example.com.au,eng@example.com.au` | Specific addresses, where the domain rule is too broad |
| `VOUCH_COMPANY_NAME` | string | `Example Pty Ltd` | An invoice naming the company beats a personal contact address |
| `VOUCH_COMPANY_ADDRESS` | string | `56 Pitt Street, Sydney` | Same, for invoices that carry an address and no email |
| `VOUCH_ACCOUNTS` | comma-separated account names | `Amex Platinum,Westpac Choice` | The accounting-MCP accounts belonging to the claimant |
| `VOUCH_PRIOR_CLAIMS` | comma-separated paths | `~/claims/2024-25.xlsx` | De-duplication targets |
| `VOUCH_FORM_TEMPLATE` | path | `~/claims/form.xlsx` | The employer's layout to copy |
| `VOUCH_OUT_DIR` | path | `~/claims/2025-26` | Where the deliverable is written |
| `VOUCH_DOWNLOADS` | path | `~/Downloads` | Where manually-saved invoices land |
| `VOUCH_BANK_DETAILS` | `name\|bsb\|acct` | `Jane Smith\|737 012\|631 471` | The claim form's footer block |

Optional, and only where the operator wants the classification columns:

| Variable | Shape | What it does |
|---|---|---|
| `VOUCH_CLASSIFY` | `off` \| `rd` \| `deductible` | Adds two columns and a per-supplier basis table |
| `VOUCH_CLASSIFY_CORPUS` | path to a directory | Research the classification is derived from; cited in the report |

## The interview, when the variables are absent

Ask in **one** `AskUserQuestion` round, not a conversation. Lead each question with the value you would pick and
why. Free text on every answer, because the real constraint usually arrives in the note rather than the choice.

Things worth asking that an operator will not volunteer:

- **The owner of every card ending you found**, including ones they did not list. Show the endings you saw in the
  invoices and the feed and ask them to classify each. A card ending appearing on vendor invoices but on **no**
  account in the feed is almost certainly the company's own card, and that inference is worth stating so they can
  correct it.
- **Whether a joint card counts.** It does, in every case seen: joint money is still partly the claimant's. But it
  has been read the wrong way round by an agent and had to be corrected, so ask rather than assume.
- **Whether the prior claim's form has known defects** worth reproducing for continuity. One real form transposed
  two column values against their headers on every row. The right move is to write values in header order and state
  the divergence, not to reproduce the defect silently.

## What to do when a fact is missing and cannot be asked

An unattended run that hits a missing fact does **not** guess. It:

1. Completes every stage that does not depend on the missing fact.
2. Writes the rows it could decide, and a named list of the rows it could not, with what each needs.
3. Emits the wanted-invoices page and a `NEEDS-A-DECISION.md` naming each open fact and the rows it blocks.
4. Reports the denominator: `decided N of M rows; M-N blocked on <fact>`.

A claim delivered with four rows held back and named is a finished run. A claim delivered with four rows guessed is
not, and the guess is invisible in the output.

## Reading the environment safely

Echo what you read, never the secrets:

```
[vouch] period 2025-08-07 .. 2026-06-30 · claimant Jane Smith
[vouch] cards mine=3003,2005 joint=7328 company=7812
[vouch] company domains=example.com.au · accounts=4 · prior claims=2
```

An operator scanning that line catches a wrong card classification before it has decided eighty rows.
