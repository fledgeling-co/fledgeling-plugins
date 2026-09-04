# The progress report a non-technical reader can act on

Use this file when a campaign owes somebody a status report rather than a gate result. The
contract below is what a report has to contain to be honest; the shape came from a real
report being rejected and rewritten.

## 1 · What the reader asked for that the first version did not have

The first report was returned with five distinct complaints, in the reader's words:

> *"There's no mention of the visual verifications in the report. It's also not clear what
> `cases ruled out by decision` means. I'd also like the visualization skill to be used to
> make the report easier to see how things are progressing. Update to be non-technical and
> include estimates for all of the web app issues that the tests have already found if any."*

Five failures, each with a general form: **a measured axis was missing; a term of art went
unexplained; the numbers were not visual; the register was technical; the defects had no
sizing.** A sixth arrived separately — the report opened at a figure two days into the work
and called it the start, and the reader answered *"we started at near zero so perhaps you
need to look through previous sessions for more data."*

Each maps to a section the shipped report then carried, and one of them opens by saying so:
*"This was missing from the previous report, and it is the part with the least flattering
answer."*

## 2 · The eight things a report owes

1. **Every axis that was measured, including the unflattering ones.** A judging pass that
   found nothing is a result; omitting it is a claim that it was not run.
2. **A denominator on every row.** Different populations get different denominators and say
   so on the row rather than being rescaled to a common one.
3. **The campaign's own start, not this session's.** Establish the baseline from the record
   rather than from the first figure you personally measured.
4. **Every term of art defined where it is used**, including the ones that sound obvious.
5. **A size against every defect**, with the size scale defined inline and its basis named.
6. **Proposed work marked as proposed** and separable from work that was asked for.
7. **What the figures exclude** — review, release, and time waiting on a person.
8. **Charts with their figures repeated as a table**, each row naming its source, because a
   chart is unreadable to anyone consuming the text.

## 3 · Denominator per axis, never one blended percent

Four mechanics make this real rather than stated:

**Every figure carries its own denominator on its own row.** One eight-row table read
`Measure | Start | End | Out of | Change`, spanning three denominators — flows, p0 flows,
cases — plus one sub-population (frames judged, out of flows that have frames).

**A missing measurement is drawn as missing.** Nobody measured the release-blocking line on
two of the days, so that segment is dashed rather than interpolated: the line between two
points is not a claim about the days between them.

**A figure measured against a different denominator says so rather than being rescaled.**
An earlier day's 79.9% was against the 633 journeys then thought to owe coverage, not
against the later 925, and the report says that beside the number.

**Another effort's percentages are refused outright.** A separate reconciliation tool
covered 11 of 946 test files; this campaign was the other 935. Its numbers were correct and
about something else, so quoting them would have been precisely the error the per-axis rule
exists to prevent.

## 4 · "Ruled out by decision" is a third category, and it is kept visible

48 of 369 cases in one report were neither tested nor remaining: somebody decided they were
not worth checking. The report explains the term where it appears:

> It is deliberately not counted as tested, and not counted as remaining either. It is a
> third category, kept visible because the reason can expire: something ruled out today may
> be worth checking after the next change.

Two properties make it honest rather than a hiding place. It has **its own count with its
own denominator**, so folding it into either neighbour is visible. And each entry carries
**the reason**, because a reason is what a later reader re-evaluates. An expiry on each one
is the natural next step and was proposed rather than built.

## 5 · The visual-verification axis, reported including a negative result

The axis a reader asks about most is the one a picture settles, so it gets its own section
whatever it found. What that one found, over 75 judged surfaces and 600 questions at 8
questions per screenshot: 534 answers healthy (89%), 18 flagged a problem, and 17 said *"I
cannot see that from this picture"*.

**The 2.8% not-observable rate is the number that matters most**, because it says the
questions are answerable from a screenshot at all. And the flags were then read for the
only thing that would be new information — a flag on a screen whose ordinary test already
passed. Two qualified, and both turned out to be the camera rather than the app: one
capture was of the browser's own error page on a test that deliberately cancels its
navigation, the other showed a failure message on a test whose whole purpose is to prove
the app refuses bad input.

The verdict the report published: **not proven, rather than proven useless.** Its
machine-readable twin records `visual_marginal_value: UNPROVEN` with the same two counts.

A campaign that cannot yet say whether an axis earns its cost says that, and keeps the axis
running or stops it as a decision somebody makes with the number in front of them.

## 6 · Register — what "non-technical" means

Rename every axis to an outcome the reader owns: *journeys with a test attached*; *a broken
test stops a release*; *test steps watched passing*; *screens an AI has checked*; *test
steps able to run*.

Title defects by what a user would notice — *"Renaming yourself saves, and every screen
still shows the old name"* — under the columns `What a user would notice | Where | Size`.

Define the size scale inline and name its basis: *small under half a day · medium half a
day to two days · needs a decision first: someone must choose the intended behaviour*,
sized from how long comparable changes took in this codebase, excluding review and release,
and not a commitment.

Order by what unblocks the rest. Where several defects are sized *needs a decision*, say
which decisions change what the other fixes are, so they are settled before any of them
starts.

Give every chart a long-form textual description before the image, so the figures survive
extraction, and follow each with a table headed with where each figure comes from.

## 7 · A defect in a report is not filed until it has a card

A report that lists defects and leaves them in the report loses them. The pipeline that
held: **a failing case or a spec-versus-code finding → an entry with file:line evidence →
a brief in the project's intake folder → the intake stage → a card on the board → the
delivery pipeline.**

Three linkage failures worth guarding, all measured: card ids that existed only in an
agent's reply and never in a file; briefs that carried no card id of their own; and a gate
reading one field name while writers used three (`existingCard`, `card`, `cardId`). Agree
the field name before the writers run, assert the returned object's own id after a write,
and read the state back.

**A green test asserting the defect is part of the defect.** Where a test pins the broken
behaviour as correct, the brief names that test and its file, so the fix cannot pass by
leaving it green. One brief's acceptance sketch closes the loop explicitly: the case
*"asserts the new behaviour, and its title no longer names /dashboard."*

Keep false positives visible rather than deleting them. One register held 61 defects of
which 3 were invalid and 3 by design, and a later reader needs those six to calibrate the
other 55.
