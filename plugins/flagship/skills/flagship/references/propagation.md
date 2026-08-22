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

## The instrument that answered a narrower question (22 Aug 2026)

The third rule in SKILL.md came from this corpus. It is a different failure from
absence-read-as-success: nothing malfunctioned, no gate could have caught it, and the
instrument was read as answering a question it was never asked.

| Instrument | Asked | Answered | Cost |
|---|---|---|---|
| `reckon` 1.0.0 | what was never built | what could not be *joined* to the registry | product axis 155→49, 64→2, 48→0 |
| `inventory.json` `evidence` | was this observed | did somebody type `observed` | requirements-observed 3/32 → 29/32 |
| `reckon.py check` | is the reckoning sound | is `summary` consistent | readers were quoting `headline` |
| `berths.py` | what is running | what has *claimed* a berth | `in_use 0` with five runners live |
| `df -h /` | how full is the disk | how full is the read-only system volume | 5% against a data volume at 87% |

The reckon row is the expensive one. In three repos independently — 23, 48 and 64 rows —
**every single brief classed `unbuilt` was merely unjoined**, and the class inflates the
product axis in the direction that manufactures work. Both sessions holding the anomaly
("18 of 23 unbuilt are already merged") filed it as staleness rather than asking why a
merged brief would be classed unbuilt.

Two preconditions the corpus produced, both of the check-before rather than check-after
shape:

- **Invoke a versioned tool by explicit path.** 1.0.0 and 1.1.0 sat in the plugin cache
  together, both looking installed, and nobody established which a bare invocation picks.
  Testing both paths tells you what exists; it does not tell you what would run. The cache
  also gained 1.1.0 mid-evening, so **a cache measurement has a shelf life** — a session
  quoting its own note from earlier in the night should re-take it.
- **`git ls-remote --heads origin` before ordering a push, not after.** One repo's push
  could never have completed: the remote did not exist. Its quality gate had also been red
  on `main` for some time — the missing remote and the red gate were hiding each other.

## Destructive calls that establish their target elsewhere (22 Aug 2026)

Four members from four repos, one shape: the call resolves its target from somewhere other
than immediately before the call, so the damage lands outside what the author was looking at.

- `git init` under an inherited `GIT_DIR` — unset the whole `GIT_*` prefix rather than
  naming variables; naming `GIT_DIR` and `GIT_WORK_TREE` leaves `GIT_INDEX_FILE`,
  `GIT_PREFIX`, `GIT_OBJECT_DIRECTORY` and `GIT_CEILING_DIRECTORIES` behind.
- `git config core.bare=true` into a shared config — the predicate is any git *write*, and
  `git config <key> <value>` hides best.
- An arming script `cd`-ing to a stale absolute path, then `git add && git commit -q`
  followed by `git reset --hard "$BASE"` against whatever repo it landed in.
- **`git checkout -- <file>` as an arming restore.** It resolves from HEAD, so on
  **uncommitted** work it reverts the fix rather than the mutation — and the control leg
  then fails in a way that impersonates a broken test. Commit the fix before arming, and
  make every runner brief name its restore mechanism rather than saying "restore
  byte-for-byte". A `cp` backup with a sha verified afterwards is safe rather than lucky.

Prove one with a **control and a block**, both legs required: with the guard removed the
write must LAND, with it applied the write must be refused and the value unchanged. A
control that does not land proves nothing — that is the unarmed predicate in miniature.

## A lock that serialises execution but not state (22 Aug 2026)

A `mkdir` lock guarding id allocation holds only within one checkout. Two worktrees branched
from one commit each read their own copy: A mints 101 under the lock, B takes the
uncontended lock straight after, reads its own copy still at 100, and mints 101 as well.
**Any project allocating ids from a worktree under a local lock has this**, and it does not
fire while one person allocates serially from the main checkout — which is a habit, not a
guarantee. The fix is a journal in `git rev-parse --git-common-dir`.

The general form is worth more than the instance: a lock proves mutual exclusion over the
*critical section*, never over the *state the section reads*.

## A correct intent through an incorrect instance (22 Aug 2026)

A test asserted `192.0.2.1` must be allowed "because it is not RFC1918". True, and
irrelevant — it is TEST-NET-1, so it was never routable either. The intent (a half-matching
prefix must not be blocked) was sound and its other cases were genuinely public; only the
example was wrong. Flipping the assertion to match new code would have destroyed the intent
while looking like a fix.

This is a **review** hazard rather than an arming one, and it defeats the discipline the rest
of this corpus is built on: arming proves a check *can* fail, and none of that establishes it
fails for the reason its name claims.

## "It has never fired" is evidence about the guard, not the mechanism (22 Aug 2026)

The worktree-lock defect above was present in a second repo's dispatch scripts — same
mechanism, lock file on a tracked path, so every worktree carries its own copy. Its ledger
is nonetheless perfect: 49 rows, 49 distinct, contiguous, zero duplicates.

It never fired because a shared-file guard refused any runner branch touching `LEDGER.md`,
so ids were allocated serially from the main checkout instead. The session's own reading is
the durable part: **it did not solve the lock, it made the lock unreachable — and those look
identical from outside until somebody widens the permission.** Relax the guard to let runners
mint ids and the lock is exactly as broken as the first repo's.

So a clean history is evidence about whatever is standing in front of the mechanism, and
says nothing about the mechanism. Ask what would have to change for the defect to become
reachable, and whether anything records that the guard is load-bearing.

## A live process is not running work (22 Aug 2026)

A wrapped build held four berths for **two hours four minutes** on **0.08 seconds of total
CPU**. Its last child was `docker logs -f`, following a container stream that never closes,
so the wrapper never exited and the kernel never returned the slots.

Every instrument was honest: the claim was real, the claimant alive, no stale lease, and a
file lock cannot distinguish a process that is working from one that is waiting. With CPU
pressure critical the ceiling had also collapsed from 12 to 3, so `in_use 4` exceeded it and
`available` read 0 while load decayed for twenty minutes with nothing admitted.

- **Wrap the work, not the tail.** A `-f` or `--follow` belongs outside the wrapper, or the
  wrapper should release when the work it was admitted for finishes rather than when the
  process does.
- **When a berth is held long and cheap, read its CPU time and its children** before
  concluding the machine is busy. Elapsed time alone cannot tell a two-hour build from a
  two-hour tail.

## An honest producer, a consumer that cannot tell two states apart (22 Aug 2026)

A verdict classifier returned **one exit code for two conditions**: a failure that reproduced
when re-run in isolation, and a suite that broke wholesale and was never re-run at all. The
caller rendered that shared code with the first condition's sentence, so a run that isolated
nothing reported that the failure *"reproduced on every isolated re-run"* — in the summary
line a person reads.

The producer's own text was already correct and its own self-test already proved it: the
"attempted no isolated re-run" case passed before the fix. **The defect was entirely in the
consumer**, and no test of the producer could have found it.

The fix was a fourth exit code rather than a grep for the rendered marker, because matching
on rendering is the same defect one layer up. This is the shape to look for wherever two
outcomes that want opposite next steps share a return value: a wholesale breakage and a
reproduced defect are not the same finding, and a code that cannot separate them guarantees
the caller will eventually pick one meaning and print it for both.

## Telling a killed process from a refused one (22 Aug 2026)

A `pgrep -f` pattern-kill took an out-of-family reviewer process on this machine, and the
victim was attributed to the wrong session — assumed from timing rather than established, so
the finding propagated with the wrong name on it for an hour. The real victim is still
unidentified and does not know why it got an empty return.

The discriminator is cheap and does not need pids: **an empty output file with an empty log
is a kill. An empty output file with a populated log is not a kill — read the log to find out
which non-kill cause it was.** A killed process does not stop to explain itself; everything
else does.

The second half was narrower when first written ("…is a denial") and a third session found
the counter-example within the hour: a 0-byte output whose log read `Error: empty prompt`,
because the packet file lived in `/tmp` and `/tmp` had been cleared. **Caller error, not
denial, and it is the cause most likely to be misread as a lane being down** — "the lane
returned nothing" is true either way and only the log separates them. That session had
already filed it as a lane failure before reading the log. Phrase the rule as *read the log
to find out which*, or it sends people hunting a permission problem that is a malformed
argument.

Test on the pair, never on the log alone: a clean run also has an empty log.

**And the expensive half is what an unexplained silence becomes if nobody checks.** One
runner wrote *"agy returns 0 bytes headless intermittently — that is three of four families
degraded"* **twenty minutes before the first empty return it could have been describing**. An
assumed cause, stated as a property of the lane, which then fed the whole fleet's picture of
which lanes were reachable — including this skill's own repeated claim that one family was
the only working out-of-family lane. Three empties clustered inside 160 seconds, two of them
eight seconds apart, with every other call that night succeeding, is not the shape of
intermittency; it is the shape of something killing processes in a window.

The generalisation is the one worth carrying: **a lane briefly killed by a neighbour looks
exactly like a lane that is flaky, unless somebody has the timestamps.** An instrument's
silence gets read as a property of the instrument, and the reading outlives the incident as
folklore that nothing re-derives.

The attribution error itself is the second top-level rule catching its own author. A set
returned a member, the member looked right, and "I know why it belongs" was doing the work.

## The convergence prevented rather than counted (23 Aug 2026)

Four times in one evening, separate repos independently derived the same finding and none
knew about the others. The fifth was caught in flight, and the difference is worth naming
because it is the whole argument for a conducting session existing.

One repo filed a defect: a `mkdir` lock guarding id allocation serialises execution but not
state, because two worktrees each read their own copy. A second repo confirmed the same shape
in four of its dispatch scripts. A third repo had **already merged the fix** — and its fix
was not a better lock but a different diagnosis: the failure was never two processes
contending for one file, it was **two worktrees each holding the registry at its own inode on
its own branch**, so an flock over the file is invisible to the other and the obvious fix
protects nothing. The lock belongs in the **git common directory**, which every linked
worktree shares by construction. Verified in 12 seconds with no runner: same path, same dir
inode, 12/12 cases.

Routing that as a *fix* rather than as a *finding* is the move. A finding invites the
recipient to derive an implementation; a fix names the mechanism, the measurement and the
check to run before adopting it — here, **is your lock on the registry file itself?**, since
that decides whether the common-dir move closes the bug or imports someone else's.

**Two rules came out of it, and the second is the one that bites after the fix lands.**

- **Do not apply another repo's defect to a repo you have not measured.** This conductor
  wrote "the lock does not hold across worktrees anyway" about the repo where it
  demonstrably does — a claim about one session's code made from another session's defect.
- **"The lock is fixed" and "id allocation is safe" are different claims.** The fixing repo's
  allocator protects six entity kinds and contains **zero references to its feature ledger**,
  so the campaign registry is locked and the markdown ledger is not, and every triage touches
  the unlocked half. A merged item made it believe the whole class was closed. **A fix
  covering half the id spaces looks identical to one covering all of them, until somebody
  allocates in the other half** — so check which spaces the lock actually covers rather than
  which defect it was filed against.

## A count that surprises you, in either direction (23 Aug 2026)

Every predicate failure in this corpus until now returned **nothing** and meant *did not
measure*. This one returned **seventy** and meant *matched a different word*.

A session probing its own allocator for lock primitives ran
`grep -cE 'flock|mkdir|lock|fcntl|O_EXCL'` and got 70. It was one keystroke from reporting
seventy lock primitives in an allocator that has none. The seventy were 33 `blockers`, 17
`block`, 16 `blocked`, 6 `blocker` and 1 `blocks` — the substring `lock` inside `block`.
Word-bounded, the real count is **2**, both `mkdir(parents=True, exist_ok=True)`, which is the
*opposite* of a lock: it never fails, so it cannot serialise anything.

**A populated result reads as evidence, and a populated result from a substring match reads
as strong evidence.** Seventy is a number nobody interrogates. This is the members-have-two-
readings rule in the direction nobody watches, and it is worse than the empty-result case
because an empty result at least prompts the question.

The discriminator costs thirty seconds:

```bash
grep -oE '<pattern>' <paths> | sort | uniq -c | sort -rn
```

**Print the matched tokens before believing the count**, whenever a count surprises you in
either direction. It would have caught this, the `git init` argv-array probe that found
nothing because the call was `Command::new("git").arg("init")`, and a set of seven that was
really four.

## Detect the absence, not the collision (23 Aug 2026)

The acceptance test for an id-allocation lock has to detect a **lost row**, not a duplicate
id. A racing allocator that overwrites leaves **no duplicate and no gap to notice it by**,
which is why the original defect survived as long as it did — every check anyone would
naturally write looks for a collision, and a collision is the failure mode that announces
itself.

And where a repo already locks one id space, extend that lock rather than adding a second
mechanism for the other. A lock per id space is two things to keep in step, and the defect
exists precisely because two things were out of step.
