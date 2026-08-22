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

## Safe for a reason other than the one you would cite (23 Aug 2026)

Three repos audited their id allocation after one filed a defect against it. **All three were
safe. None was safe for the reason its own session would have given.**

| Repo | Would have cited | Actually why |
|---|---|---|
| A | "the lock holds" | The lock is in the git common dir — true, and it covers 6 of 7 id spaces; the markdown ledger every triage touches has no lock at all |
| B | "the guard refuses runner branches" | True for 2 of 7 spaces. The other 5 are written only by one script, run serially from the main checkout |
| C | "LEDGER.md already solved this shape" | It solved the same-checkout case. Two worktrees each `mkdir` their own lock path and neither blocks |

So the family has **three** members, not two, and they weaken in order:

- **A lock** proves mutual exclusion over the critical section, never over the state that
  section reads.
- **A guard** proves neither — only that nobody was *allowed* to try.
- **A serial-by-script habit** proves less still. Repo B's five uncovered spaces are written
  only by one finalize script under one merge lock, measured across all history: 63 touches,
  every one on a completion commit, none reachable from a runner branch. That is a habit
  encoded in a script rather than in a person, **which makes it more durable and no more
  enforced.** A future fleet that lets runners mint ids gets no guard and no lock in the same
  move.

The miniature that carries the whole family: inside repo B's campaign directory the *ratchet*
file is refused by the guard, as derived, while the registry it ratchets is not. **The guarded
thing is the summary; the unguarded thing is the source.**

The question to ask is not *is it safe* but *what would have to change for it to stop being
safe, and does anything record that the answer is load-bearing.* Repo B wrote its coverage
table into the guard file itself rather than into a report, because that file is what somebody
edits when they widen the permission.

## A survivor has two readings, and so does a red suite (23 Aug 2026)

Arming is this corpus's standard of proof: a check that has been shown to fail is worth more
than one that has only been shown to pass. Two findings narrow what an arming actually buys.

**A mutation reported INERT and was not.** Its anchor string appeared in the source *and* in
the test asserting it, so the mutator aborted, nothing was mutated, and the harness ran
against **pristine code** and reported a live guard as decorative. A failed setup step
reported as a measurement — the same shape as every other entry here, arriving at the one
instrument built to catch it. **An aborted mutator and a genuinely decorative guard produce
identical output**, so the harness has to prove the mutation landed before it grades the
outcome. A unique anchor reddens it immediately.

The consequence for a gate: raising a mutation bound to convert a survivor into a kill is the
gate-moving move in its purest form, and it is worse when the survivor is an artifact. **A
survivor means the guard is decorative, or the mutation never happened**, and only one of
those is a finding.

**And one mutation proves one property.** A first arming folded a decision function back to
its defect and reddened exactly one test, which nearly recorded three untouched guards as
proven. Arming each property separately found a real hole — nothing tested the catch arm at
all, and a mutation restoring the old behaviour passed every test that existed.

> **"The suite went red" is evidence that one property is covered, never that the suite
> covers the change.**

Count the properties the change has, arm each one, and report the count. Four mutations were
needed where one was run.

## Fix the join, do not fabricate the citations (23 Aug 2026)

An item filed to fix a 12.8% join rate was about to do the wrong thing, and the correction is
the general one. Measured on that repo's 117 briefs: **13 cite a campaign-registry id, 91
(77.8%) cite a PRD requirement id**, and 115 cite a sibling item. The reckoning joins on the
**registry's** id space while the brief template mandates the **PRD's**. The briefs are doing
exactly what the convention asks and the instrument cannot read it.

So the fix is to join on the id space three quarters already carry, **not** to add citations
to 117 briefs — that fights the repo's own convention to satisfy a tool, and it is 117 edits
that go stale. Where a join rate is low, ask **which id space the population actually uses**
before concluding the population is under-cited.

Two constraints came with it, both worth carrying:

- **The existing bridge resolved by line number** — 18 of 32 rows pointed at a PRD line and
  only 11 resolved — which another item had already recorded as drifted. Never build a join
  on a positional reference.
- **A better join rate must not silently promote anything to done.** Source evidence may
  demote a claim, never promote one. A join that retires items quietly is worse than the low
  rate it replaced.

## Attack a claim, do not check a list (23 Aug 2026)

A round-1 verifier found a live-deletion hole by **trying four attacks, three of which held**.
A location environment variable outranked the signed bundled binary, so a four-line shim armed
live deletion with both arming variables absent — and a comment three lines above asserted
that could not happen. No checklist finds that; the comment would have satisfied it.

Two siblings from the same wave:

- **A verifier that builds a stronger plant than the round did.** One disabled a guard
  outright rather than widening its regex, and found ten cases stayed green under *both* — so
  they cannot detect the **total absence** of the layer they are named for. Sharper than "they
  did not bind it", and the same hole the one-mutation-one-property rule protects against,
  reached from the other end.
- **A restatement that swapped the denominator without saying so**, keeping the numerator's
  name and dropping a rate from 20.5% to 16.7%. Both figures were correct for their own
  population. A census read as another census — inside the item whose subject was exactly
  that.

## The safety is real, and it is not the mechanism anyone would name (23 Aug 2026)

Five members now, from five repos, and they are one family:

- An id-allocation lock safe only because one person allocated serially, by habit.
- Five id spaces safe only because one script writes them from the main checkout.
- A locked registry beside an unlocked ledger that every triage touches.
- An arming script safe only because the path it would have destroyed was already deleted.
- A ledger lock made unreachable by a permission guard that refuses runner branches.

Every one was found by asking **"why has this not fired?"** rather than "is this correct?" —
a cheaper question than it looks, and one that appears in no checklist. The answer names the
real mechanism, and in five of five cases it was not the mechanism the owning session would
have cited.

The follow-up that makes it actionable: **what would have to change for this to start
firing, and does anything record that the answer is load-bearing?** One repo wrote its
coverage table into the guard file itself, because that file is what somebody edits when they
widen the permission.

## `ping` is not a liveness oracle (23 Aug 2026)

An entire execution plane was reported unavailable for an evening because `ping 192.168.3.91`
returned 100% packet loss. **Windows blocks ICMP by default.** The same host answered
`ssh -o BatchMode=yes -i <key> luke@192.168.3.91 'echo SSH_OK'` immediately.

A host that is down and a host that is up with ICMP filtered are **indistinguishable to
ping**, and the reachable case is the one that reads as failure. The oracle is whatever the
code actually uses to reach it: that plane's `remote_argv` uses ssh, so ssh is the test.

## The first blocker is not the last one (23 Aug 2026)

A preflight designed to report the **first** blocker in dependency order, and only the first,
reported a missing credential file. This conductor read it as *the* blocker and was one step
from recommending a long-lived admin key be written to disk.

Clearing it would have **advanced the refusal, not cleared it**: the node config pointed at a
route refused by a measured mechanism rather than a config gap — a Docker Desktop container's
outbound socket belongs to the host's own LAN address and never crosses the vNIC the firewall
filters, so the egress guarantee is unenforceable and the route is refused before anything
starts. Fail-closed and correct.

So a preflight that names one blocker is answering *"what stops you first"*, and reading it as
*"what stops you"* is the narrower-question rule again. **Ask for the whole chain before
paying for the first link** — especially when the price of the first link is a secret at rest.

Two things came with it, both worth carrying:

- **A restart lands on whatever the daemon is holding.** That one held 23 jobs, 8 running, and
  nobody had mentioned it. A config read once at start-up cannot be tested without a bounce,
  so establish whose work is in flight before bouncing it.
- **Reachable and useful are different questions.** The plane is a model-agent lane — a
  containerised CLI reaching a model through a key-holding proxy on the host — so it cannot
  take CPU work off that host however well it works, because subscription-CLI routes
  authenticate against the host's own sessions. "Yes it can be stood up, and it should not be
  stood up for that" is a legitimate answer and only the plane's owner can give it.

## The artefact that describes the work is what stops anyone looking beside it (23 Aug 2026)

A card asserted that sensitive-source disclosure was citation-scoped. It was not: every
retrieval already resolved and disclosed. The real defect was the opposite shape — the footer
passed an **empty** source list whenever a turn carried an inline `Sources:` line, and that
emptied list was also the disclosure's only input. **So the sensitive-source notice vanished
on precisely the turns that cited the most**, and a draft written from a sensitive document
published with no notice it had been used. A compliance surface, surviving three prior passes
because the card's own framing pointed away from it.

In the wave before, a test loop had been iterating **zero times** while its two assertions
were counted as coverage.

Both are the same failure at different scales: a card's premise, a spec's shape, a test's
name. **When the assessment feels tidy, check what sits beside the thing it names.**

## When a probe says "absent", check that it could have said "present" (23 Aug 2026)

Three probes in one investigation gave confident wrong answers, all the same shape:

- **`ping`** said a PC was down. It was up with ICMP filtered.
- **`ls /usr/local/bin/anvil-node`** said a distro was unprovisioned. The binary was at
  `/root/src/target/release/`.
- **A hex grep against a raw-binary sqlite column** said a pairing did not match, before
  either side had been encoded.

Each answered a narrower question than the one asked, and each was read as the broad answer.
The rules that fall out:

> **The oracle is whatever the code actually uses.** That plane's `remote_argv` uses ssh, so
> ssh is the liveness test — not ping.
>
> **When a probe says "absent", check that it could have said "present".** Run it against a
> case you know is there. A probe that cannot produce a positive is not measuring absence.

## An exempted control proves nothing (23 Aug 2026)

Adopting *"a mutation that did not apply is not a measurement"* breaks the harness's own
control, and the two interact badly by default: **the stricter you make "every mutation must
apply", the more certainly your control fails**, because the control is the one leg that must
*not* mutate.

The natural repair is to exempt it — and that silently removes the only leg proving the
harness can report green for the right reason. **An exempted control is excused from the rule
rather than satisfying it.**

The fix is to assert the opposite property instead. That harness's control now requires the
digest to be **unchanged** *and* the tool to still exit 1. It is a control because it is
asserted to be one, not because it is skipped.

Three faults hit while building it, every one reported honestly rather than passing, which is
the rule working: a `printf` ate a `\n` and broke a Python literal, reported as *mutator
errored* rather than as a pass; `git checkout --` restored an uncommitted fix to HEAD and
destroyed it, so the control leg failed and read as a broken test — now a **precondition**,
the script refuses to run at all with uncommitted changes; and a no-op control written to
prove the digest check fires had a quoting fault and never ran, which the baseline leg
failing had already proved better.

## Where the same rule was applied per-row (23 Aug 2026)

The one-mutation-one-property rule, applied to an arming already called done: two mutations,
suite red, and it would have recorded **nine assertions as proven when one refusal row was
exercised**. Rebuilt per row — each of five special ranges gets its own mutation and the leg
fails unless *that* row goes red, each of three public controls proved by blocking it. Eight
legs, eight pass.

## An assertion that is accidentally load-bearing (23 Aug 2026)

A session checked its own armings against the exempted-control rule and they held: fifteen
mutations each asserting exit 1, and a control leg asserting exit 0, `findings=0` on the
restored register, **and** a sha equal to the pre-mutation bytes. Asserted rather than
assumed, and correct.

**But it held by luck.** The sha verification had been written as *restore hygiene*, not as a
control, and it was doing control duty because it happened to assert the right thing.

> **An assertion that is accidentally load-bearing is one refactor from being deleted as
> redundant.**

Nothing marks it as the thing proving the harness can report green for the right reason, so
the next person tidying duplicate checks removes it and every leg still passes. Name what an
assertion is *for*, in the assertion, wherever it is carrying more than it appears to.

## A ceiling below the ask is not a queue (23 Aug 2026)

Under critical pressure the berth ceiling drops to 3, so a `--weight 6` claim **cannot be
granted at all**, however long anything waits. A session retrying it collects exit 75
indefinitely with nothing to show for it, and the symptom is indistinguishable from a busy
queue.

The right response is not to wait but to **sample the ceiling and run only once the weight
can actually be granted** — one session armed a retry outside itself that checks every three
minutes. And a gate that could not be admitted **is not a gate that passed**: an item whose
suite owes a re-run stays unmerged rather than inheriting its previous green.

## `du` answers two questions and only one of them is yours (23 Aug 2026)

A session sizing its own lanes measured **1.4GB each** as a `df` delta across five fresh
installs — the honest *marginal* cost. `du -sh` on any individual worktree reports
**4.2–5.8GB**, and the parent tree 48GB. Both measured, neither wrong.

The gap is pnpm hardlinking into a shared store: **per-directory `du` counts hardlinked
content in full for every tree it walks**, while the bytes an additional lane actually
consumes are the marginal figure.

So the same command produces opposite errors depending on the question:

| Question | `du` says | Reality |
|---|---|---|
| "Can I afford eight more lanes?" | ~40GB — refuse work it could do | ~11GB |
| "How much do I get back by deleting them?" | ~40GB — expect space that will not arrive | ~11GB |

**Ask which question you have before choosing the command.** Marginal cost is a `df` delta
across a real install; reclaimable space is a `df` delta across a real delete. A per-directory
size is neither.

Same family as the rest: a number that looks like it names the thing it means. The session
also flagged that it could not complete the sum-of-parts proof because **`du` itself timed out
at 24 per core** — so the two figures are measured and the mechanism connecting them is
inference, which is the right way to report it.

## A wrapped cleanup can outlive the process that needed it (23 Aug 2026)

The runaway `cp -R //.` left a 43GB partial copy of the root volume in `/var/folders`. Nobody
deleted it: the harness's own `rm -rf "$W"` fired when the leg died, and the directory drained
43GB → 18GB on its own while the disk recovered 183GiB → 209GiB free.

Two things worth carrying. **Check before you reclaim** — a conductor about to `rm -rf` 43GB
by hand would have raced a cleanup already running, on a path built from the same empty
variable that caused the incident. And **a disk trend is not fleet load**: this one read as
evidence of seven sessions working and was one buggy `cp`, and it was quoted upward as
capacity pressure before anyone looked at what was writing.

## A suite summary is an interface (23 Aug 2026)

A conformance firing-test had **measured nothing since the item before it merged**. Its parser
used a `$`-anchored regex against a suite's summary line, and a merged, independently-verified
item added a third number to that line. The regex stopped matching.

**A parser that stops matching reports nothing found rather than erroring, which is
indistinguishable from a clean sweep.** So a verified merge silently blinded the instrument
that proves the conformance guards can fire, and nothing anywhere disagreed.

Two rules: a suite's summary line is an **interface** and changing it is a breaking change; and
any parser reading one needs a positive control — a case it must match — so that "found
nothing" and "matched nothing" stop being the same output.

## Two survivors that were the entire safety argument (23 Aug 2026)

The one-mutation-one-property rule caught a real one on its first application elsewhere. Nine
mutations over a new id-space bridge; the first pass detected seven. **The two survivors were
the whole safety case**: relabelling every bridged edge as `cited`, and forcing the weak-join
flag to false.

Both left all 26 cases green — because **every case ran on fixtures, and neither property is
observable until a ledger is actually built.** Seven end-to-end cases later, the round killed
9 of 9, each reddening exactly one named case. A guard that guarded nothing, found only by
arming its properties separately.

## Line-number anchoring was not fragile, it was already wrong (23 Aug 2026)

A bridge between two id spaces resolved by **line number** into a requirements document. It had
been reported as "real and too weak to carry the traffic" — 18 of 32 rows pointing at a line,
11 resolving — and the 11 treated as usable.

Re-tested: **11 of 11 mismatched.** A requirement about a six-phase guarded reclaim resolved to
one about buffer reallocation on resize; one about WCAG AA palettes resolved to Enter being a
dry run. A second, semantic reading agreed at 10 of 11, the eleventh right by topic and by
luck.

So the finding is not that positional anchoring will drift — it is that **it had already
drifted and was returning confident wrong answers that nothing distinguished from right ones.**
Where any repo bridges id spaces by line citation, sweep it rather than scheduling it.

The replacement is the shape worth copying: **one reviewed crosswalk file**, 36 ids mapped and
13 declared as having no counterpart, each carrying its basis — and **no brief edited**. Join
12.4% → 71.1%, with work total and product count identical on both sides, built in one process
from one read so the two figures cannot be separate runs quoted together.

And three properties kept the better rate from becoming a promotion: bridged edges are marked
`bridged` and never `cited`; the weak-join flag reads the **cited** rate alone, so coverage
cannot unlock retirement as a side effect; and a promotion guard diffs the two ledgers.
