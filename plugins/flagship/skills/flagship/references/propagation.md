# Propagation — the job only you can do

You are the only party that sees across sessions. A session knows its own repo; it cannot know
that the tool it just characterised is failing the same way in nine others.

## The measurement that justifies the whole skill

One evening, twelve repos, sixteen sessions. Independently, with no session aware of any other:

- **Three sessions** found the same defect in `reckon`: it classed every defect row `broken`
  without reading its `status` field, so a register of 148 defects with 126 fixed reported 183
  broken. One found it as `reckon.py:463`, one as "108 defect records all `broken`, 88 fixed",
  one as an inflated headline it declined to re-run against.
- **Three sessions** found a second defect in the same tool: its `check` gate compares `summary`
  against `rows` and never reads `headline`, so a stale headline survives a clean exit while the
  correct counts print directly beneath it.
- **Two sessions** reached one architectural conclusion by different routes — that a
  mock-driven fidelity gate has no opinion on what the build adds beyond the mock, and *no
  opinion reads exactly like agreement*. One got there by driving the shipped app and finding a
  defect three green instruments could not see; the other from a worker's handover.

None of that reached anyone. A conductor that relays it converts three private findings into
one portfolio fix — and in that case the fix already existed at source, version-bumped, while
nine projects were still running the broken copy from an installed cache that had never been
updated.

**So the mechanical rule: when a session reports a finding, ask which other sessions it
invalidates, and send it there with attribution.** Attribution matters — the finding travels
better when the receiving session can ask the source directly.

## The one shape behind almost every failure

Fifteen instrument failures surfaced in that evening. Every one was **absence read as
success**:

| Failure | Mechanism |
|---|---|
| Defect class assigned without reading `status` | a field not read |
| `check` gate never reading the field that was wrong | an assertion that cannot fail on the wrong field |
| Capture-lineage gate exiting 0 over **zero** images | empty population, clean exit |
| Same gate exiting 0 over an unparseable manifest | writer wrote `file`+dict, reader read `path`+string |
| A firewall anchor whose positive control **could never resolve** | the suite could not have passed on any host, behind a hardware excuse that was true and irrelevant |
| An assertion detector blind to `XCTAssertEqual(a, b)` where both names hold one value | matched syntactically identical expressions only |
| `\binstalled\b` unable to match inside `_installed_` | underscore is a word character |
| A mock-driven fidelity gate | no opinion on what the build adds |
| A join iterating one level too deep | empty map **manufactured** a finding on every dependent row |
| A join with no population assertion | had the register failed to load, **every** fixed defect would report uncited — a maximal finding set from an instrument that read nothing |
| An integrity gate where **a silent deletion passes all five passes** | a check for silent writes with a silent-write hole |
| A verifier that cannot execute what it grades | judgement over artifacts reported as verification |
| A `git init` grep defeated by `Command::new("git").arg("init")` | dead predicate |
| A zsh glob matching nothing, **aborting the command line** | two of three searches died; "no matches" read as clean |
| A catalogue sync recording success while dropping **100%** of updates | all items failed validation, all skipped, cursor advanced |

Plus one for reading the machine: `df -h /` reports ~5% used on an APFS system volume while the
data volume is at 87% — wrong by an order of magnitude *in the reassuring direction*.

## The two rules that cover all of it

> **A check that returns nothing has two readings, and the instrument must say which.**
>
> **A set that returns members has two readings too, and "I know why these belong" is not one
> of them.**

The second is subtler and came later: a session offered seven defects as instances of a
category, and per-row measurement showed four. A populated result *feels* like evidence in a
way an empty one does not, which is why it survived longer.

Ask both of every number, including your own. Three sessions handed over figures that later
moved; two said outright that their numbers were **right by luck rather than by construction**
once they added the assertion. That is the reporting standard.

## The derived rules worth propagating on sight

**Arm the predicate before believing it.** A zero from a predicate proven to fire is a result;
a zero from an unproven one is a claim, and the two print identically. One session fired each
git predicate against planted bait first — literal form found 3, argv form found 1, the repo
found 0 — which is the only reason its clearance can be trusted.

**"The assertion went red" and "the assertion I care about went red" are different claims, and
the first reads like the second.** A session built two drifts to prove a sanitiser; both fired
the *shape* assertion rather than the *leak* assertion, so the security property was still
unproven after two reds that looked like proof.

**Assert the invariant rather than enumerate the violations.** An inventory of where a
dependency calls git is true of today's versions only. One line unsetting the whole `GIT_*`
prefix holds across updates and demotes the inventory to a diagnostic.

**A gap-fix handed a verdict rebuilds; a gap-fix handed the findings converges** — and route it
conditionally, because verdict shapes fail in opposite directions. Count the citations
**before** reading the findings, since reading first primes you to see coordinates as the work
list. Citation-dense verdicts risk a bloated work list built from measurement citations;
prose-dense ones risk under-counting findings that live only in prose headings.

**A Done verdict's non-AC findings have no destination.** Gap-fix takes failures, merge takes
passes, and findings attached to a pass fall between the stages. One fleet had run that shape
for sixteen waves and recorded the admission rather than quietly correcting forward. The fix:
the brief comes **before** the merge is recorded — after the merge is exactly when they
evaporate. The retroactive version that costs nothing is writing residuals into the merge body.

**A runner that produced nothing needs a channel sweep, and the tool mix is the fifth channel.**
Beyond the run record, the event stream, the token ratio and the granted capability set: a
sweep reading 45 calls, all `Bash`, no `Write` or `Edit`, established the runner was still
surveying — transport failure, not task failure, so relaunch rather than a sharper retry. Its
survey was then recovered from the transcript rather than repeated.

## A verification that passes is not the verification that governs

Three instances, three repos, one shape — and the third was found by a dialog on the operator's
screen rather than by any instrument:

- A signing script reported success over an artifact Apple would refuse: `codesign --verify
  --deep --strict` passes over an ad-hoc **nested** binary. Separately, a DMG that
  `hdiutil create` left assessable was never signed at all.
- A test runner: `codesign --verify --deep --strict` exits 0 and silent while
  `spctl --assess --type execute` returns **rejected**. Ad-hoc signature, no quarantine
  attribute, bundle intact. Gatekeeper phrases that rejection as *"is damaged and can't be
  opened. You should move it to the Bin"* — so the OS's own wording invites deleting a valid
  build product, and the check a project would naturally run says the artifact is fine.

**Ask which tool's opinion actually gates the thing you care about**, and run that one. For
distribution and launch that is `spctl --assess` and `notarytool`, never `codesign --verify`
alone. And read a "damaged" claim about a locally built product as a Gatekeeper refusal until
proven otherwise, rather than as damage.

## Convergence is the evidence a conductor is uniquely placed to produce

When two sessions hit one fault independently, that is evidence the fault belongs to the
**tool** rather than to either repo — and neither session can establish it, because neither can
see the other. Four in one evening:

| Fault | Found by | How they differed |
|---|---|---|
| Defect rows classed `broken` without reading `status` | 3 repos | one by line number, one by count, one by declining to re-run an inflated headline |
| A gate comparing two fields and never reading the third, which was the wrong one | 3 repos | one found the stale field, one warned not to quote it, one filed it P1 |
| A mock-driven fidelity gate having no opinion on what the build adds | 2 repos | one by driving the shipped app, one from a worker's handover |
| A registry tool re-serialising on write | 2 repos | **two different fixes** — one normalises the encoding back after letting the tool validate; the other inserts as text and validates with `json.load` |

That last row is the most useful shape: both fixes are correct, they trade validation against
diff size, and the measurement that makes the case belongs to only one of them — and it re-derived that
measurement before publishing it, which moved it. **The finding is the pair, not the count:**
on an 8,588-line registry, the *same semantic change* costs **402 changed lines written one way
and 1 written the other**, on one argument. (401 lines carry a non-ASCII character; 0 escapes
are currently present.) The count of non-ASCII lines is only where the number comes from. With
six worktrees open, the 402 collides with every other runner's edit to a file none of them
touched.

Its upstream brief also names the regression test neither the tool's `add` nor its `check`
had: **write the registry twice and assert the second write is a no-op diff.** That is the
property both repos actually needed, and its absence is why two sessions had to find it by
being bitten.

**So when a session reports a fix, ask whether anyone else fixed the same thing differently.**
Route one upstream brief carrying both fixes and the measurement, rather than letting two repos
each carry a local patch nobody else inherits.


## Give the convergence claim a denominator

Four convergences is the argument that these faults belong to the tools. It is a weaker
argument than it reads, and the session that produced the fourth said so: **four out of four
instruments examined is a different claim from four out of twenty.** Each session has one
sample; only the conductor can total them, and totalling only the *hits* is the same error as
publishing a pass rate with no denominator — which is the thing this whole corpus is about.

So when you report convergence, also ask every session **what it checked and found clean**, and
publish both numbers. A conductor that reports only the collisions has built the exact instrument
this file warns against.

## An unknown value fails in two directions, and only one announces itself

The zero/members rules cover a check's *result*. This is about its **vocabulary**, and it is the
one place where the safe-looking default is the dangerous one.

A tool classified defect rows by status and treated **any word but `fixed`** as remaining work.
Fail-closed on an unknown word, which is right — but six words in that set mean the opposite of
remaining work (`by design`, `invalid`, `obsolete`, `superseded`, `cannot reproduce`), so the
instrument whose whole purpose is to say what is left over-reported a backlog that reads as real.

A second instrument, checked for the same shape, was worse. It selected its population with a
single status string, `open` — so a register growing a word meaning *still broken*
(`regressed`, `reopened`) would have dropped those rows **out of the obligation entirely** and
gone on printing a clean count over a quietly smaller population.

> **The first over-reports on an unknown word. The second under-reports, silently — and a clean
> green is a worse failure than an inflated backlog.**

Widening the second one's vocabulary immediately surfaced five real defects it had been
excluding, taking its owed count from 19 to 24.

**So classify every value as in-scope or out, and make an unclassified value a finding that
names the value and its row count** — never a default in either direction. And beware the
in-between: `partially-fixed` belongs to neither pole, because a half still broken owes a
reproduction for that half, and forcing it either way loses exactly the half that matters.

**A count-shaped acceptance claim decays; a relation does not.** One item recorded "the ten
defects the classifier calls broken are exactly the ten this registry records as non-fixed" — and
a merge closed six of them within the hour, falsifying it before the ink dried. The durable form
is registry-relative: *the classifier's `broken` set equals the registry's own non-fixed set*,
which held at 115 rows giving 10 and at 111 giving 5. Print counts as the run's instance; quote
the invariant as the acceptance criterion.
