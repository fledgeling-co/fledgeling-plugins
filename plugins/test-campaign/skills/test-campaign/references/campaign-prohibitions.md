# What a red may not be turned into

Use this file two ways: as the rules to follow while making a failing case pass, and as a
checklist to read a diff against before it lands. Every row is a move somebody made and
had to undo.

The general principle underneath all of them: **a test states what the product should do,
so any edit that makes a red green by changing the statement rather than the product has
made the defect the specification.** That is the reason to generalise from, and it covers
the cases not listed here.

## 1 · Reviewing a diff against this file

Read the test-side changes in a diff that also claims to fix a failure, and for each one
ask what the assertion could no longer catch. Five shapes are worth locating directly:

| in the diff | ask |
|---|---|
| a removed or commented `expect` | what did it assert, and what now covers that? |
| `.first()`, `.nth()`, `.filter()` added to a locator | was the extra match the finding? |
| a literal replaced by a matcher, or a regex widened | what does the new form still refuse? |
| `test.skip` / `test.fixme` / `.only` added or moved | is a red being parked? |
| a changed selector on a case that was failing | is the claim still about the thing that failed? |

## 2 · Never weaken an assertion to make it pass

| refused move | do this instead | why |
|---|---|---|
| Deleting an assertion | Fix the product, or characterise the defect (§3) | the suite loses the only record of the requirement |
| Replacing a value check with a presence check | Assert the value, or an ordered list | presence passes on wrong contents |
| **Adding `.first()` when the duplicate is the finding** | Assert the count, then fix the duplicate | `.first()` makes the defect invisible to the case that found it |
| Widening a regex until it matches anything | Narrow to the string the requirement names | a pattern that refuses nothing measures nothing |
| Parking the case | Leave it red, or characterise it | a parked case keeps its place in a coverage count while checking nothing |
| **Re-pointing a failing claim at a nearby selector** | Keep the claim on the element that failed | the claim stops being about the thing under test |
| Selecting an unnamed control by its fill class or CSS position | Give the control an accessible name in the product | the selector routes around the accessibility defect and hides it |
| Asserting a count where a value was meant | Prefer a value or an ordered list | a count passes on the wrong contents |
| Asserting a literal that encodes one data state | Assert the relation, or seed the state the assertion names | a claim pinned to one data state is a tripwire on data, not a guard on behaviour |
| Closing a criterion with a subjective oracle ("reads naturally") | Name an observable a second reader would agree on | a subjective oracle closes anything |
| A conditional early `return` in a test helper | Let the precondition fail loudly | the case passes without reaching its check |

## 3 · Characterising a defect, which is the sanctioned alternative

When a red is a real product defect and the fix is not yours to make: write the case so it
describes behaviour **as it is**, give the defect an id, and let the fix flip the case.

Two things that do not do this job. **An expected-failure marker (`test.fail()`) passes on
any failure, including the wrong one** — the suite goes green on the defect, so it is
refused for characterising a new one. And **a known-defect tag stays until the fix lands**:
the tag is the only record that a green is conditional, so removing it on an agent's word
converts a conditional pass into an unconditional one.

Three readings that are not verdicts about the product, and each needs re-running rather
than recording: a red at **setup**, a **precondition's** error message, and `no-result`,
which is absence rather than success. The general form: a probe weaker than the claim it
would overturn does not overturn it.

## 4 · Never weaken the evidence or the gate

- Leave coverage-registry rows and their enforcing spec intact; a registry row removed to
  make a coverage metric clean removes the requirement, not the gap.
- Leave security guards in place while measuring coverage. One campaign's route to a clean
  metric was deleting an open-redirect guard.
- Change build inputs, seed defaults and cache keys as their own decision, never in passing
  to make a gate agree.
- **Ratchet only on run evidence.** Promoting report-mode specs into a blocking step, or
  adding the missing filter flags, is a change that needs a recorded run first — five specs
  that looked like free coverage returned 11 failed when run.
- A pass ledger records runs. Re-recording it from a contaminated run, or hand-editing a
  spec hash inside it, makes it a record of nothing.
- A gate that cries wolf gets switched off within a week and then checks nothing, so tune
  it to fire on the defect rather than on the neighbourhood.
- Raising a job's timeout to make a suite fit is a change to what the suite proves about
  duration; treat it as one.
- **Stage test files by path, one at a time.** A bulk add of a test directory swept an
  unaudited scratch file into a commit five separate times in one campaign.
- A signed compliance document is signed by the person who commits it. An agent committing
  it is not a signature.
- Never edit an instrument's recorded `known` value to quieten a break
  (`instrument-calibration.md` §1).

## 5 · What a model judge may never be

- **A judge verdict does not gate a build.** Its measured ceiling as a non-crash oracle is
  around half of known bugs, with false positives. Nightly and advisory.
- Design the judge so it cannot fail a build on ignorance: per-atom verdicts of
  `held | violated | not-observable | inconclusive`, with only `violated` counting. A judge
  that cannot see something says so.
- Bound it by construction — a concurrency cap, a maximum call count, and a refusal to run
  without credentials rather than a silent degrade to nothing.
- **Derive visual atoms from what a frame can settle, not from the behaviour catalogue.**
  Deriving them per flow from a behavioural specification emitted 1,600 atoms across 770
  flows, most of them unanswerable from a picture. One atom per line keeps the judge off the
  verbosity bias a paragraph introduces.
- **A screenshot is evidence only if it is of a product surface.** Reject captures taken on
  the browser's own error page, `about:blank` or an empty URL. Both of the two candidate
  findings a 75-surface judging pass produced were exactly this class.

## 6 · What may not be done to the environment

- Intercept an outbound effect at the boundary rather than letting the step fire, and keep
  the interception blind to test tags — a tag-aware mock is one typo from a live send.
- A console-error allow-list entry for a seed-data fault hides the fault in every future run.
  Fix the seed.
- Seeding around a bad precondition, or planting the token an assertion looks for, means the
  case asserts a value the test itself wrote.
- Match a mutating-write tag exactly. A prefix match added to satisfy one case would also
  match a future tag naming a live customer tenant.
- Editing application source while a browser run is in flight makes the run's verdict
  unattributable.

## 7 · Ordering and scope

- **Author no more flow specs while the current ones are not known to run**
  (`flow-coverage-axes.md` §6).
- Rewriting freshly merged specs to adopt a new driver, and briefing every environment tier
  at once, both convert working coverage into a large in-flight change nobody can review.
- Surface stale worktrees and branches rather than deleting them: one of 229 worktrees in
  that campaign held two unmerged commits.
- Edit line-anchored on content, never on index. Removing one offending line shifts the
  indices and can re-qualify its neighbour.

## 8 · Two rules that came from an out-of-family review

Both say the same thing — **an assertion placed on the wire before the defect's location
cannot witness the defect**:

- intercepting a request and asserting its shape is not coverage for a server-side write
  defect;
- replaying a recorded response, or seeding through an API, is not coverage for a feature
  whose defect is in generating the content.
