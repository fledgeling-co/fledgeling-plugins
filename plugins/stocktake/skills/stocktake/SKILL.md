---
name: stocktake
description: >-
  Sweep a tracker board card by card and decide, with evidence, what each one actually needs
  next — reading every comment and attached image, rebuilding the requirement list from the
  ticket BEFORE opening any diff, finding whether the work sits on the main branch, an
  unmerged branch, a worktree or nowhere at all, tracing each requirement to the code that
  PRODUCES it rather than to a surface that renders, judging whether the tests standing
  behind it can actually fail, and then moving the card to the column its evidence supports.
  Every verdict is graded out of family by a single strongest judge rather than a panel,
  because a panel of nine frontier judges buys about two independent votes. An inconclusive
  result is a first-class blocking outcome, never a pass. Cards with work left get a brief
  written to docs/features-to-triage and are handed to ship-fleet to run; cards with open
  decisions get referred to another model family or decided with a named recommendation
  rather than parked on the reader; cards whose evidence holds are promoted. Use this
  whenever someone asks to triage, sweep, review or clean up a board or backlog, asks what
  is left on a set of tickets, asks whether tickets in a review column are genuinely done,
  asks which tickets are in the wrong status, wants a board reconciled against the codebase,
  or says a column has piled up and needs going through.
---

# Stocktake

A stocktake counts what is on the shelf against what the books say. Here the board is
the books and the codebase is the shelf, and the count is the thing that finds the
books wrong.

Three failure modes shape the whole design, and each of them produces a board that
reads as healthy:

**The card says done and nothing produces the data.** A surface renders, the schema
validates, the suite is green, and no code ever wrote the value. `spec-validation`
exists because roughly half of a 110-ticket corpus shipped not-as-specified while
reading as complete.

**The tests behind the card cannot fail.** An assertion comparing a value with
itself, a case satisfied by the wrong exception type, a fixture in a shape the
product never stores. All three were found in a single session's own work, by an
out-of-family reader, after the author had declared each one red-armed.

**The evidence is authored by the party being judged.** The worker writes the tests,
the completion record and the comment that says it is finished. METR documents
frontier agents editing tests and monkey-patching evaluators. So the ticket is the
oracle and the worker's record is the defendant, and the order they are read in is
load-bearing rather than stylistic.

---

## The order that makes this work

**Build the numbered requirement list from the description, every comment and every
attached image BEFORE opening the completion record, the plan, or the diff.**

Read in the other order and the diff tells you what to look for, so you find it. This
is the single rule most worth keeping; `references/the-oracle-order.md` carries why,
and the mechanics of reading image attachments as requirements rather than decoration.

---

## The sweep

One card at a time, resumable, because a full board is hours of serial verification
and no single session survives it. `scripts/board_ledger.py` owns the state — a row
per card, so a fresh session continues rather than restarting.

```bash
S=<this-skill-dir>/scripts
python3 $S/board_ledger.py init <dir> --columns "Needs More Work,Todo,Developer Review"
python3 $S/board_ledger.py next <dir>          # the next unfinished card
python3 $S/board_ledger.py record <dir> --key WEB-1234 --verdict … --note …
python3 $S/board_ledger.py record <dir> --key WEB-1234 --dispatch "ship-fleet <run-id>"
```

`--verdict ungraded` is the row for a card the method never ran on — a lane that stayed down,
a packet that never returned. It takes a `--note` naming which of steps 1-6 were skipped, and
it sits outside the needs-work count, where it would otherwise read as a defect someone could
go and fix. A card nobody graded and a card graded as broken are different findings.

### 1 · Read the card, whole

Description, every comment oldest to newest, and every attached image. Comments are
where the requirements actually live — a card's body is usually its first draft, and
the acceptance criteria that matter were negotiated underneath it.

**Read the images.** A screenshot in a bug report is frequently the only statement of
the expected behaviour, and a card that reproduces a defect in a picture cannot be
triaged from its text.

Write the numbered requirement list now, and do not read further until it exists.

### 2 · Find where the work is

A card can be complete on a branch nobody merged. `scripts/locate_work.sh` reports,
for a card key: commits on the integration branch, commits on unmerged `*` branches,
live worktrees, and whether the branch is an ancestor of the remote.

Four outcomes, and they are different problems: **merged**, **built but unmerged**,
**built but unpushed**, **not built**. A card sitting at "in review" whose work is on
a branch that never merged is a delivery failure, not an implementation one.

### 3 · Trace each requirement to its producer

`spec-validation`'s method, unchanged: classify every claimed-done requirement as
**REAL**, **AUTHORED** or **MOCK**, with `file:line` for each verdict, by finding the
code that produces the value rather than the code that displays it. An honest empty
state is not a gap; a missing producer is.

Invoke that skill where it is installed rather than reimplementing it.

### 4 · Judge whether the tests could fail

A green suite is a claim, and `references/testing-adequacy.md` carries the checks that
test it, drawn from `test-campaign`:

- **Which rung of oracle** each critical requirement stands on. "The element exists"
  under a flow that moves money fails the gate rather than passing quietly.
- **Armed and unarmed assertions counted apart.** A self-comparing expect, a
  type-only assertion where two paths raise the same type, and a fixture in a shape
  the product never stores are all unarmed and all read as coverage.
- **A denominator.** Cases run over cases that exist, and the skipped set named. A
  suite reporting green across 13.9% of itself is reporting on 13.9% of itself.
- **Fault sensitivity** where the stakes justify it — a mutation delta, not a count.

The cheapest real check is to break the thing the test guards and watch it go red. A
test nobody has seen fail is a test nobody has seen work.

### 5 · Grade it out of family — one judge, not a panel

**Do not build a jury.** Nine frontier judges from seven families give roughly two
effective independent votes, panel accuracy falls 8–22 points short of independent
voting, and the best single judge matches or beats the full panel across every
condition tested (`references/evidence.md`).

So: one strongest available out-of-family lane, given the requirement list and the
diff. Lane order, the packet-size ceiling, and the concurrency fact that costs a run
if you miss it are in `references/verification-lanes.md`.

Where only a same-family lane is available, the verdict is recorded as
**in-family (degraded)** and the card does not reach a terminal column on it alone.

### 6 · Decide the column

`references/column-policy.md` is the full table. The parts that are not obvious:

- **Inconclusive is a result, not a retry.** ISO/IEC 17025 treats it as valid output.
  It blocks; it never rounds up to a pass.
- **Needs More Info carries the question**, phrased so a reply unblocks it. A card
  moved there with no question is a card nobody can answer.

Done is where an out-of-family verdict alone can take a card. What happens next is
step 7.

### 7 · At Done, ask the warrant whether the card may go further

Whether a card can leave Done is a question about *authority* rather than about the
card, so it is not answered here. The `warrant` plugin is where that authority is
written down, earned per defect class and revoked on evidence, and this skill reads
its answer:

```bash
S=<this-skill-dir>/scripts
python3 $S/warrant_column.py --warrant-root <repo> --class <defect-class> --verdict pass
```

Its exit code is the column:

| Exit | Column | Why |
|---|---|---|
| 0 | **Verified** | the class holds warrant tier 3, ratchet fired nothing, and the substitution is printed with the grant |
| 2 | **Needs More Work** | a warrant gate failed on this card's own evidence, named in the output |
| 3 | **Done**, and no further | the authority is not there. Every reason is named: no signed warrant, no owner, an unnamed class, a census class, a tier not earned, or a revocation |
| 4 | no move | the verdict was inconclusive, which blocks |

Pass `--card-gate-failed '<gate>: <detail>'` for each warrant gate that failed on
this card, and the answer is Needs More Work with the gap quoted onto the card. A
`tick_and_tie` mismatch already names the figure, both values and the tolerance, so
the card gets something actionable rather than "verification failed".

**What a grant rests on, and it is stated on every one.** A warrant tier is earned by
absence of escapes over a declared window, not by a measured non-inferiority study;
no such study exists for code or UI review. The signed warrant is a person accepting
that substitution in advance. Two consequences worth holding: a class the warrant does
not name can never reach Verified, because an unnamed class defaults to no authority
at all; and a census class has no machine path past Done however good its evidence is.

Where `warrant` is not installed, `scripts/check_verified_gate.py` is the fallback and
it refuses by default. Refusing is the feature.

### 8 · Open decisions get referred, not parked

A decision the reader has to make is a cost to them. Apply `clarify`'s gate: settle it
from the material where it is settled, refer it out of family where it is technical,
and take your own recommendation where you can name one and say why. What survives —
taste, cost, scope, risk, their own systems — reaches them as one question, and
anything irreversible reaches them regardless of how certain you are.

### 9 · Write the briefs, then run them

Cards with work remaining get one brief each in `docs/features-to-triage/`, written so
`ship-fleet` can orchestrate without re-deriving anything: the requirement list, what
is built, what is missing with `file:line`, where the work sits, what the tests do and
do not cover, and the blocked items separated out with their owners named.

Write one brief per card. `ship-fleet` fans out per brief, so a file serving twelve cards is
one work item rather than twelve — `gates.py briefs-written` holds the ratio at 3 cards per
brief and reads each file for the card key it claims to cover.

Then hand the directory to `ship-fleet`, which fans the briefs out and returns each
card to this skill's own gates to decide where it lands. Record where each card went with
`board_ledger.py record --dispatch <run-id>`, or why it is waiting with `--deferred <reason>`;
`gates.py dispatched` reads those fields and fails on a card carrying neither.

This second half is what the run is for, and it is the half a sweep skips. Every other gate
here measures the audit, so a run that graded 241 cards and dispatched none of them passes
them all. Dispatching writes code across branches, so a recorded deferral is a complete answer
where the owner wants to schedule the work themselves.

---

## Arming a full sweep

A whole board is 7–18 hours of serial lane time and will outlive the session. Arm it
with `better-goal` rather than trusting a long run to stay on task: the ledger is the
worklist, `scripts/gates.py` is the gate set, and the run resumes from the ledger.

`references/running-long.md` carries the gate set and the two traps that make a long
run report success while doing nothing.

---

## Operating rules

- **The ticket is the oracle; the worker's record is the defendant.** Requirement list
  first, always.
- **Never show a verdict to a human reviewer before their own pass.** Concurrent-read
  positioning produced no detection gain and worse specificity across 429,345 reads.
- **Audit-only on product code while judging.** A pass that edits the thing it is
  judging has stopped being a pass. Fixes are a separate act, recorded as one.
- **A card only moves on evidence you can point at** — a sha, a `file:line`, a named
  lane and its verdict word. "It looks done" is not a column.
- **Report what was not checked.** A sweep that omits its own gaps reads as complete.
