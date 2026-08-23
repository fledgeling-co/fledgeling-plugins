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

## `/` passes every plausibility check a script can apply to itself (23 Aug 2026)

The runaway `cp -R //.` was **not** an empty variable, which is what it looked like and what
this conductor reported. The script computed
`CAMP="$(cd "$(dirname "$0")/.." && pwd)"` — and it had been copied to `/tmp`, so `dirname`
was `/tmp`, `..` was **`/`**, and `"/"/.` is `//.`.

That distinction is the whole repair:

- **An empty variable is a missing input.** `set -u`, a non-empty test, almost any defensive
  habit catches it.
- **`/` is a real, existing, readable, absolute directory.** It passes every plausibility
  check a script could apply to itself. The only check that catches it is one asking whether
  the resolved path is *the right tree*.

So the sharper form of the shell-layer rule: **a wrong path and a right path are
indistinguishable to everything except a check that knows what it is looking for.**
`available` reads as a count; `/` reads as a directory. Both are true, and neither is the
thing meant.

### A guard is not a fix for a class until something makes new code use it

The same session had built exactly that check — an arming-tree guard — **an hour earlier**,
for a sibling defect. It then wrote a new arming script without it, and copied another to
`/tmp` where the fault fired. **Four scripts had the guard, four did not, and nothing said
so.**

The two defects are opposite ends of one fault, and the asymmetry is the argument for a
census rather than a guard:

| | Path behaviour | Failure mode | Visibility |
|---|---|---|---|
| Pinned a path that stopped existing | fails **closed** | armed nothing | loud — an exit code |
| Derived a path that always exists | fails **open** | copied a volume | silent — printed nothing |

**The one that armed nothing was loud. The one that ate a disk was silent.** A guard protects
the code that calls it; only a census over every call site tells you which code does. That
session's census reads `examined=19 unguarded=0` — after it first committed a message
claiming "18 scripts, 0 unguarded" **before running it**, when the true figure was 2 of 19.
It re-ran the census before the sentence the second time and put the correction in the commit
message rather than the corrected number alone.

## `ps %CPU` cannot see the present, and `held_for_sec` cannot see the past (23 Aug 2026)

`ps -Ao %cpu` reports CPU **averaged over a process's whole lifetime**. A daemon reported at
**170.6%** across five and a half hours was sampling at **0.0%** — busy at some point, idle
since, and the figure cannot tell those apart. A second daemon read **166%** by lifetime
average and **33%** when sampled live over three seconds.

That is the exact mirror of the thermal rule already in this corpus, where `held_for_sec`
describes only the *current* state and one quiet minute flips a verdict. **A scheduling
decision needs both the present and the past, and each of those instruments has exactly one
of them.**

The live rate needs no `top`: read cumulative CPU seconds twice, N seconds apart, and divide
the delta by the wall clock between them. It is the same construction as reading a berth's CPU
time against its elapsed time to find a leak.

### And the control that could not fire

The first version of that detector was armed with a one-shot harness — and the check requires
**two consecutive samples** before it speaks, so at one iteration the control could never fire.
It produced no output, which read as "nothing above threshold" and was really "the test cannot
pass". A control that cannot fire proves nothing, in exactly the way an exempted control proves
nothing and an aborted mutator proves nothing.

**When a control comes back silent, check that it could have spoken** — the same rule as *when
a probe says absent, check that it could have said present*, arriving one layer up in the
harness rather than in the subject.

## A control needs its own control (23 Aug 2026)

**A control that fails looks exactly like the defect it was built to find.**

A session testing whether another repo's gate-location defect applied to its own built the
clean tree with `git archive main | tar -x` — which gives the branch's content and **no
`.git`**. So `git show HEAD:<path>` resolved nothing, the provenance check reported a source
file "recorded at capture, HEAD has no such file" for a file plainly sitting there, and the
gate exited 1. It read precisely like the defect landing, and it was one step from being
reported as such.

The construction had **no power to return the answer it was hoping to trust**: an extract
without `.git` could never distinguish a real provenance failure from its own missing one.
`git worktree add --detach` carries branch content *and* a resolvable HEAD, and has the power.

The cheap discipline: **ask what your control would do against a subject known to be good.**
That session counted four mis-built controls in one day — a probe placed outside the tree, a
realpath mismatch firing the wrong assertion before the one under test could be reached, an
arming leg whose mutation was a no-op, and this one. Each passed or failed for a reason other
than the one claimed.

Two sharper statements of the same thing, from two other sessions the same night:

> **A control that cannot fail has not been run, it has been performed.**
>
> **A predicate proven to fire can still be pointed at the wrong field, and it prints
> identically to one pointed at the right one.**

The second came from a session whose two probes were both live and both wrong in the same
direction — one over-matched prose containing a word, the other under-read the object where
the literal string actually lived, and the two summaries agreed with each other. What caught
it was going to look at where the string was, not writing a better regex.

## A gate must run where the merge lands, not where the work was done (23 Aug 2026)

A pre-merge gate was accepted having run **inside the item's own worktree** — exit 0, a true
result about the wrong tree. The evidence its cases cited existed in exactly one place on the
machine, that worktree, and `evidence/` was gitignored wholesale. After the merge the
integration branch failed with **51 findings**, and no branch could pass a pre-merge gate
until it was fixed.

Worse than the 51: **507 citations that *did* resolve resolved by accident**, from untracked
logs left in that checkout by earlier runs. On a fresh clone all 558 would have been absent.

**Any check reading a file git does not carry produces an exit code that is true about the
checkout and silent about the branch**, and the two are indistinguishable from outside.

Three sessions checked themselves against it, and the negative results were worth more than
the rule:

- One found `evidence/` **not** gitignored, 382 of 384 files tracked, 0 untracked in a fresh
  worktree, and had already been running the full sweep on merged `main` after every merge.
- One found its gate *does* read an untracked per-machine file — but into a **NOT COVERED
  report, never a PASS/FAIL step**, so it printed "has never run here" rather than inheriting
  a green. **A gate step reading an untracked file is silent about the branch; a coverage
  report degrades to honest absence.** That distinction is what separates the two shapes.
- One found the fault in the worst possible object: a `laneProof` structure whose entire job
  is witnessing that a lane attached to a real artifact, citing an **absolute path** to a
  **generated, gitignored** bundle with `artifactBytes: null`. Three ways unverifiable at
  once. It fixed the paths, and recorded the missing size as a limitation rather than
  back-filling a number that would have described tonight's regeneration instead of the
  original attachment.

**A rule that fires in one repo and provably does not in another is worth more than the rule
alone**, because the difference names the property that matters.

## The leak detector's own leak (23 Aug 2026)

The berth-leak check in `scripts/starvation_watch.sh` read the **claimant's** CPU time against
its elapsed time — and a wrapper that delegates spends almost none. Measured: a claimant at
**0.05 seconds over 11 minutes** reported as a leak, whose tree (`governor-run` → `gate.sh` →
`cargo test` → a test binary) had burned **29.2 CPU seconds** and was working correctly.

The detector built to find *a live process that is not doing work* could not tell it from *a
live process whose children are doing the work*. It now sums CPU across the whole process
tree, and both legs are demonstrated: a sleeping claimant fires, the real busy-tree wrapper
does not.

Third instrument this conductor armed in one night that was wrong on its first version, all
three the same family, all three found by a peer or a false alarm rather than by review.

### And its second leak: an empty read reported as a zero one

The tree-summed fix had a defect of its own within the hour. The sum ran in shell arithmetic,
and **a child that exits between the `pgrep` and the `ps` returns an empty string** — so
`$(( total + ))` was a syntax error, the function returned nothing at all, and the empty
result was compared as though it were **zero CPU**. The claimant was reported leaked with a
blank figure where its CPU number should have been.

A failed measurement presented as a measurement, in the detector built for exactly that. Two
repairs, and the second is the general one: sum in `awk` so a missing value contributes 0
rather than breaking the expression, and **refuse to classify a claimant whose CPU could not
be read** — an unmeasurable figure is not a zero one, and skipping is the only honest verdict.

The tell was in the emitted line the whole time: `pid 99992 14:04 elapsed,  CPU,` with
nothing between the commas. **A blank where a number belongs is a failed read**, and it took
a second false alarm to look at it.

### Version five, and the honest scorecard

The leak check needed five versions in one night, and the last defect is the sharpest:
**cumulative CPU is not conserved across a process tree whose members change.** A gate wrapper
running cargo, then python, then a toolchain measured 29.2 seconds at one moment and 0.10 two
minutes later — not because it stopped working, but because the long child exited and took its
total with it. That is the *lifetime-versus-live* error again, and it had already been found
and fixed in the daemon check **twenty lines away in the same file**. Fixing an error in one
place and leaving it in its neighbour is its own failure mode.

The construction that survives: sample the tree's CPU twice and take the **delta** (immune to
turnover), and require the **descendant pid set to be unchanged** across the window. A tail
holds one child forever and accrues nothing; a working pipeline either burns CPU or changes
its children, and either clears it. Three controls: fires on an idle claimant, silent on a
CPU-burner, silent on the real turnover wrapper.

**And the scorecard, because a detector's history is evidence about it.** Across the night
this check produced **three false positives and zero true positives** — the leak it was built
for was found by a peer reading `ps` before the detector existed. It is correct against three
controls now, which is not the same as having caught anything. State that when handing an
instrument over: *armed and demonstrated* and *proven in the field* are different claims, and
only one of them is available on the night you write it.

## A gate whose pass condition is "you are the author" (23 Aug 2026)

The gate-location finding got much larger when it was measured rather than predicted.

The original report was **51 citations failing** on the integration branch. Tested properly
with `git worktree add --detach` — which keeps `.git` resolution, so `git show HEAD:` works —
the real figure is **`examined=558 absent=558`**. *Every* citation fails on a fresh checkout.
The 51 were merely the ones that also failed on the author's own machine; the other 507 were
carried by **94 untracked logs sitting in that working copy from earlier runs**.

So it is not a defect in 51 citations. **`check-case-citations` has never been able to run
anywhere but a machine that generated the artifacts, and it has been reporting green on that
basis since it was written.** A gate whose pass condition is *you are the author*.

A second repo measured the same class on one commit in two checkouts: `campaign.py check`
exits **0** in the working directory and **1** on a fresh checkout of that same commit — three
cases citing PNGs git does not carry, resolving only because earlier runs left them on disk.
Its scope was 2 cases and 3 files rather than 51, and it corrected its own earlier report in
the same breath: **"when I told you main was green, that was true of this checkout and not of
the repository."**

Two things make it actionable:

- **It prints a denominator that reads as coverage and is really a citation count.**
  `examined=558` looks like a measurement of how much was checked; it is how many rows exist.
  A gate step reading an untracked file must be made to **degrade to honest absence** rather
  than pass by authorship — which is Errand's step-versus-report distinction turned into a
  requirement.
- **The caution that saved it did not prevent a wrong answer; it prevented a right answer with
  unusable provenance.** The session was about to build its clean tree with
  `git archive main | tar -x`, which carries no `.git` and manufactures provenance failures
  identical to the real defect. It would have reached `558 absent` **for the wrong reason** and
  filed a correct conclusion on evidence that would not survive review. That is harder to
  notice afterwards than being wrong.

## A runner reporting a pre-existing failure is a claim like any other (23 Aug 2026)

A gap-fix runner reported two baselines: that a check exited 1 as a standing condition, and
that a doc was already stale at 110/66/44. On `main` the check exits **0** with 42 cases and
the doc is **correct** at 108/66/42. The branch had 44 because **its own two new cases filled
the id gaps** — so both "pre-existing failures" were the runner's own work, misattributed to
the world.

Verify a claimed baseline against the base, not against the branch reporting it.

## A pass-shaped summary over an empty denominator (23 Aug 2026)

The sharpest instance of the whole corpus, found by auditing **all 24** standalone gate steps
on `main` against a clean `git worktree add --detach` tree. Twenty-two behaved identically.
Two did not, and they fail in **opposite** directions:

| Step | on main | on a clean tree | |
|---|---|---|---|
| citation check | exit 1 | exit 1 | red everywhere — it announces itself |
| surface-grounds check | **exit 0** | **exit 1** | **green here, red on a clean tree** |

The second had been passing silently since it was written. On the author's machine it prints
`5 of 5 capture(s) measured … failures=0`. On a clean tree it prints
`0 of 5 capture(s) measured … failures=0`.

**The same `failures=0` while having measured nothing.** The two lines differ only in a number
nobody reads, and the exit code that *does* change is swallowed the moment the step runs inside
a `&&` chain.

> **A check that cannot see its subject must say so where a reader looks, and must never print
> a pass-shaped summary over an empty denominator.**

That is the requirement both instances need, and it reframes scope elsewhere: a repo that
found a *visible* instance should ask whether it has a **silent** one, because this was found
only by diffing exit codes across two trees — never by reading output.

Reported alongside the good news, which belongs in the same message: **22 of 24 steps are
clean in both trees.** A class of two, not systemic rot.

### And the clean room that was not clean

Its first comparison produced **identical output in both trees**, and it nearly recorded that
as the finding. A `cd` had persisted, so both halves ran in the same tree. What caught it was
the **exit codes disagreeing with the output**.

> **A clean room that is not clean produces agreement, and agreement is the least suspicious
> result there is.**

Same failure as building a comparison tree with `git archive` and getting manufactured
provenance errors — reached from the opposite direction, by a session that had just been
warned about it.

## A document that quietly heals reads as though it was never wrong (23 Aug 2026)

An edit inserted a note **between** two sentences that belonged together — "a real interrupted
connection end to end" and "Producing one needs a daemon killed mid-request" — so the second
read as though it were about something else entirely. The repair rejoined them **and said so
in the text**, rather than closing the gap silently.

That is the right instinct and it generalises past documents: a correction that leaves no
trace is indistinguishable from a document that was always right, and the next reader inherits
neither the fix nor the reason for it. The same discipline as keeping a withdrawn changelog
line with a dated withdrawal beneath it, and as putting a census correction in the commit
message rather than only the corrected number.

## A failed edit that changes nothing beats a fuzzy match that changes the wrong line

A scripted edit asserted on an anchor that no longer matched, and **wrote nothing**. That is
the behaviour to want. An edit tool that falls back to a near match will eventually change a
line nobody looked at, and the failure is silent because the file still parses and the diff
still looks plausible.

Assert the anchor; let the edit fail loudly. This is the same rule as *a mutation that did not
apply is not a measurement*, applied to authoring rather than to testing.

## A directory-scoped binding does not inherit into a child launched elsewhere (23 Aug 2026)

A session bound to a non-default model by a **project-scoped** settings file — base URL plus a
routing header in `<project>/.claude/settings.local.json` — spawned a fleet runner, and the
runner ran **unbound on the default model**: ~93k tokens on the wrong model before it was
killed, no commits.

The cause, measured in both directions against a local header sink: **a child `claude` reads
its own working directory's settings and ignores the parent's process-environment headers.**
So the parent is bound, every check the parent runs says so, and the child silently is not.

Two rules:

- **Launch runners from the bound directory and reach the work with `--add-dir`**, rather than
  launching in the work tree and expecting the binding to travel.
- **Prove the lane per runner, not once per session.** "The session is bound" is a claim about
  the parent. A binding that cannot be verified in the child is the same class as an
  unverified binding in the parent — and the failure is identical from outside, because the
  wrong model succeeds and returns something entirely plausible.

The session that hit it had already proved its own binding three ways (env plus config, a
probe-with-header against a control that routed elsewhere, and the broker's own ledger). That
is why it noticed: it had a standard to fail against. **A verification done once at the top is
a verification of the top.**

### And the same root cause one level up: introspection is not the instrument

There were **two** incidents, not one. The second was a runner's own self-check firing on a
**correctly bound** runner — because it trusted the harness's model claim, and **that text is
inherited from the default vendor even when the wire is bound elsewhere.**

So the failure has two faces and one cause:

| | What was asked | What answered |
|---|---|---|
| The unbound runner | *am I bound?* | its own cwd's settings — correctly, and it was not |
| The bound runner's self-check | *what model am I?* | the harness's system text — the default vendor's name |

**Asking a model what it is does not tell you what it is.** The answer comes from the prompt
it was handed, not from where its tokens went. This conductor's own brief said *"ask yourself
what model you are and say so"*, which is that instrument exactly; what actually caught both
incidents was the header probe against a control and the broker's ledger.

> **The wire is the authority. Introspection is a claim the harness wrote.**

The corrected self-check is environment-only, with the wire as the authority — and the general
form is the third top-level rule arriving in a new place: an instrument answered a narrower
question (*what does my prompt say I am*) than the one asked (*where did my tokens go*), and
printed it as the answer to the broad one.


## Threshold flapping is a wake carrying nothing new (23 Aug 2026)

A daemon alert keyed on a single threshold produced 91% → cleared → 80% → fired → cleared
across four minutes, because the value was hovering at the bar. Each event was true and none
carried information.

Two thresholds, not one: fire at the high bar, clear only below a lower one, so the subject
has to genuinely settle before the watch speaks again. Same discipline as keying the state on
*which* daemons are over rather than on their percentages — both are the rule that **a wake
must carry new information**, applied to the two ways a monitor manufactures noise from a
single real condition.

## Do not invent the threshold an instrument already owns (23 Aug 2026)

The watch called `OVERLOADED` off a hand-picked load figure — 3.0 per core — and fired on a
machine that was **working, not overloaded**: 3.45 per core, memory healthy, **zero swap**,
three berths free, load falling in every window. Nothing was warranted, and an alert that
warrants nothing teaches its reader to skip the next one.

The number that actually matters was already being computed by somebody else.
`harbourmaster`'s `pressure.cpu` is what collapses the berth ceiling and refuses admission, so
`critical` **is** the overloaded state by definition rather than by estimate. The watch now
reads that and keeps the invented threshold only as a fallback for when pressure cannot be
read.

Proved by stub rather than by waiting for a bad night: forcing `pressure.cpu = critical`
produces OVERLOADED at **2.72 per core**, and the real machine at the same moment stays
WORKING. The state tracks the gate, not a guess.

This is the skill's own *never invent a concurrency number — ask harbourmaster* rule, which it
had been applying to dispatch and not to its own instruments.

### The control could not fire, for the third time

Control B produced nothing on its first run and read as "the stub did not work". The state
machine requires **two consecutive samples** before it speaks, and the harness had been given
one. Re-run at three iterations it fired immediately.

Third occurrence of the same harness limitation in one night, each time read as a result
before being read as a defect. **A silent control is a claim about the harness until proven
otherwise** — and the cheapest guard is to make the control's iteration count exceed every
streak requirement in the thing under test, rather than remembering which check needs what.

## `git checkout --` as a restore step is a silent no-op on anything untracked

The arming harness built to catch tonight's shape contained tonight's shape.

Its restore step was `git checkout -- <path>` on a register that is **untracked**. Against an
untracked file that command does nothing and says nothing. So three mutations **accumulated**
across three legs while the harness printed **6 of 6**, every guard firing against the wreckage
left by the previous one rather than against a clean subject. It was caught only by re-running
the checks afterwards, and restoration is now a byte snapshot with an assertion.

This is the third distinct way that one command has cost something in a single night — it
reverts an *uncommitted* fix to HEAD, it resolves a path from HEAD rather than from the moment
of the call, and it silently succeeds at doing nothing on an untracked target. **Name the
restore mechanism, snapshot the bytes, and assert the restore happened.** A restore that cannot
fail is not a restore.

## One composer, so the bad shape cannot be reconstructed

The repair for *a pass-shaped summary over an empty denominator* was not "fix the two scripts".
It was to make the shape **structurally impossible**: a single `coverage()` composer — with a
Python twin — is the only place a coverage line may be built, and its `measured === 0` branch
is taken **first** and emits no pass token at all. A caller cannot assemble the old shape even
by accident.

The zero-measured output now contains **zero `failures=` tokens**, and that is the property
that was checked rather than the exit code, because the exit code was never the problem. Both
checks now say what they did rather than how it went:

- `NOT MEASURED IN THIS TREE — 0 of 558 opened here, 558 attested by the committed register ·
  this run verified the RECORD, not the artifacts`
- surfaces marked `n/a` with `(recorded 151680 px, not re-measured here)`

**Fixing the instances leaves the rule unenforced and it drifts back; fixing the composer
enforces it.** Anyone repairing a visible instance of this class should ask whether their fix
has a single composer or two edited call sites.

And nothing was copied into the tree to achieve it — the artifacts were *registered from* the
worktree that produced them, `evidence/` stays gitignored, and the register carries 95 rows.
Three limits were declared rather than buried, including the honest one: the register moves
trust from this machine's disk to the author's recording step.

---

## Any narrowing instrument answers about its own window — the generalised form

*Found by Atlas in a diff packet, generalised by Splice in a grep with no diff involved.
Independently held by Diolog Tasks from earlier work, at the cost of a wasted grading round.*

**A verifier given only a diff returns confident findings about code that is not in the packet.**
Atlas, three occurrences in one evening: a reported-missing `cancelQueries` that was on the first
line of the function, and a reported-absent failure notification sitting at the call site rather
than in the hook. The second was queued as a work item before anyone checked it.

Splice's generalisation supersedes the diff framing: **any narrowing instrument answers about its
own window, and the answer gets read as being about the code.** Its own case had no diff — a
`^run_link` grep could not match the two Apple builds invoked through a `run_apple_link` wrapper,
so 22 + 2 = 24 read as a 24-link discrepancy, and it was one step from reporting the Apple builds
absent and DEF-064 therefore not closed. *"My grep was the crop."*

**Diolog Tasks' sharpening, which explains why no gate catches it:** an absence claim over a diff
**cannot be falsified from inside the diff**. A presence claim is self-checking; an absence claim
is not — and only absence claims become work items.

**The asymmetry is the operational half, and two sessions reached it by different routes:**

| Direction | Produces | Survival rate |
|---|---|---|
| Over-matching | A large number (70 locks where there were 2) | Low — a big number invites interrogation |
| Under-matching | An **absence** | High — an absence reads as a finding |

sidetone found the same asymmetry from the reporting side: **a false alarm gets forwarded because
it is urgent; a false negative gets checked because it is disappointing.** So the failure mode
that propagates is the one that feels like news, which is why this class needs a rule rather than
care.

**The rules:**

- **Establish the positive control before reporting the negative.** Grep for a case known to be
  present and confirm the predicate sees it. Thirty seconds, and it is the difference between a
  note and a false rejection.
- **Ship the enclosing function whole, the call sites, and the file's exports** — never the
  changed lines alone.
- **Require any absence finding to name where it looked**, so "not in the packet" and "not in the
  codebase" are distinguishable on the face of the report.
- **An absence claim from a packet-only reviewer is inadmissible.** Splice's out-of-family lane is
  worse than a diff: it inlines every fact and *forbids tool use* (a crosstalk fix), so the
  reviewer cannot check an absence even in principle.
- **A false absence entering a queue stops being a claim and becomes a fact**, because everything
  downstream reads it as scope rather than as evidence.

---

## A cited path is reliably real and unreliably current — drift and transcription, not fabrication

*Atlas found it; Diolog Tasks measured the population.*

Atlas copied a file path out of a runner's report into its ledger and the file does not exist.
Diolog Tasks then ran the check across four waves: **253 distinct cited paths, 19 unresolved,
zero fabricated.** The breakdown is what makes it worth keeping:

- **10 were `e2e/`-relative** — `e2e/tests/chat/chat.spec.ts` is real at `apps/web/e2e/...`. The
  runner used the path its own command line used, correct from `apps/web` and wrong from the repo
  root. Quoted into a ledger verbatim, a reader gets "no such file" on a file that exists.
- **4 contained a literal `...`** — prose abbreviation, not a claim.
- 1 build artefact, 1 `node_modules` path — both correctly absent.
- **1 genuinely stale, and it is the new rule.** `rail-star-contrast.spec.ts` was renamed to
  `.spec.tsx` because the fix made it render instead of parsing source. The report cited the path
  it was true at when written and false by the time it merged. **A path can be accurate at
  authorship and wrong on arrival, with no error in either.**

**And the session that raised it withdrew its own framing once the population was measured**, which
is the correction worth having. Its instance — a cited `apps/atlas-api/lib/beautyProfile.ts` with
zero commits touching it on any branch — looked like an invention. The real file is
`app/api/me/beauty-profile/route.ts`, so it was **a mangling of a real path**, which fits 253 cited
with zero fabricated exactly.

So *"a runner report is a claim, including its paths"* is too strong as first written. **The accurate
form: cited paths are reliably real and unreliably current-or-exactly-spelled.** The failure is drift
and transcription, never invention — and the remedy is unchanged and cheap either way: **resolve,
never transcribe.** Worth stating precisely, because "runners fabricate paths" and "runners mangle
paths" imply very different amounts of distrust in everything else a runner says.

---

## Two independent faults in one value, and fixing the first would have shipped nothing

*Atlas, after 83 days of a dead production sync.*

A base URL was wrong in **two independent ways at once**: the documented host had **no DNS record**,
and the path was also wrong — the service serves `app/api/v1/*` with no rewrite while the consumer
builds `${base}/v1/...`. The DNS fault was found first. **Stopping there would have shipped a
confident fix that changed nothing, and then required re-diagnosing from scratch** with the obvious
cause already crossed off.

The general shape: **a single wrong value can carry more than one fault, and the first one found is
the one that stops the search.** When a fix is about to ship on a diagnosis, ask whether the
remaining evidence is fully explained by it — an 83-day outage explained by a missing DNS record is
explained, right up until you notice the path never matched either.

**The probe that separated them is the transferable part: against a key-gated endpoint, 401 is the
healthy answer and 307 is the alarming one.** Sending a *deliberately fake* bearer to two candidate
bases, the wrong one redirected to `/login` and the right one returned **401** — reached the handler,
rejected the key. A 307 to a login page reads as *"you lack credentials"* and actually means *"you
missed the route entirely"*. So when probing a service-to-service URL, send a knowingly-bad key and
**treat a redirect as a miss rather than as an auth failure.**

---

## The wrong reference point produces an alarming number, and the alarm is what convinces

*sidetone.*

`git diff main..<branch>` on three unreviewed branches read **~23,000 deletions each** — which
reads as three branches having gutted the repo, and it was one step from being reported. They
delete nothing: main had moved **33 commits ahead**, so *main's additions render as the branch's
deletions*. The merge-base diff is the real work: +2268/−68, +1238/−40, +973/−113.

Same class as the persisting `cd`, `git archive` with no `.git`, and an HTTP 200 on every failed
attempt. **Before reporting a shocking diff statistic, name the reference point you measured
from.**

Merge consequence, kept because it is perishable: merge those branches **at record level by id,
not line level** — the measured result on the same registry conflict was 79 line conflicts and
zero record overlap.

---

## An instrument correct for one invocation style and blind in the one it ships to

*Google Drive Fixes, root-caused to the line.*

`pressure.py:147` — `"claude": re.compile(r"(^|/)claude(\s|$)")`, matched against
`ps -Axo state=,command=`. `argv[0]` is the **bare PATH-resolved name**, so the line reads
`'S    claude --dangerously-skip-permissions …'` and `claude` is preceded by the state column's
whitespace, which is neither `^` nor `/`. Both alternatives fail. Measured on a 1,459-process
snapshot: **20 real, 0 matched.**

**And the fix first published here was wrong — corrected by a third session with its own
measurement, which is the whole point of routing a finding rather than acting on it.** Over 1,425
processes:

| predicate | matches |
|---|---:|
| `(^\|/)claude(\s\|$)` | 0 |
| `\bclaude\b` | **38** |
| `pgrep -x claude` (ground truth) | **15** |

`\b` does not catch twenty — it catches 38, of which **22 merely mention `.claude` somewhere in a
path**: shell snapshot sources, a ruby gem, node invocations. Only 16 have `claude` as argv0.

**The cause is also not primarily PATH resolution.** In the verbatim lines the string mostly appears
as **`.claude`, a dot-directory component** — so `(^|/)` fails on the leading dot and `(\s|$)` fails
on the trailing slash. The bare-name observation still holds for `node` in some form
(`(^|/)node(\s|$)` gets 5, `\bnode\b` gets 9, and node *is* invoked by absolute path there), but
the mechanism behind that one is unchased.

**The fix that is not another wrong number: match argv0, not the command line.** Split the line,
take field 1 after the state column, compare its basename. Anything regex-over-the-whole-line trades
one wrong count for another — *this evening's pattern arriving in the instrument everyone reads.*

**The part that generalises: it is not uniformly broken.** In the same snapshot `xcodebuild`
matched, because it was invoked by absolute path. So the instrument **works in any test that
launches a tool by full path and fails silently in production, where a person or a shell launches
it by name** — the same shape as the `GIT_DIR` trap, in a second instrument.

And a sharper reading than "a narrower question reported as the broad one": it answers *"how many
processes were launched by a path ending in `/claude`"*, which **is not a question anybody would
ask**. There is no reading under which `0` is true and useful while twenty are live. A distinct
class — not a smaller version of the right question, but a question nobody wanted.

Two things not to fix by widening the regex: a process **count** is a poor proxy for a family
whose children do the work (one `xcodebuild` and forty `swift-frontend`s are the same admission
decision), and **a family count of zero must be distinguishable from a family the matcher cannot
see** — right now they are the same integer, which is what let this survive.

**It is the whole family table, not one pattern.** Fresh 1,459-process read, same regex shape
applied per family:

| family | real | matched | how `argv[0]` was written |
|---|---:|---:|---|
| `claude` | 20 | **0** | bare name |
| `node` | 22 | **7** | 7 absolute path, 15 bare name |
| `cargo` | 1 | 1 | absolute |
| `python3` | 3 | 3 | absolute |

**`node` loses 15 of 22**, and `node` is admission-relevant — dev servers, MCP servers, the harness
itself. Anyone sizing headroom off it on this machine is reading a third of it. So the defect is not
a bad pattern for one family; it is the table silently under-reporting whichever families a machine
happens to invoke through PATH.

**And the staleness marker is absent rather than false.** `pressure.py` can return
`"from_cache": true`, but a fresh read has **no `from_cache` key at all**. A consumer testing
`d.get('from_cache')` gets the right answer; one testing `'from_cache' in d` — to decide whether
staleness is even *knowable* — gets nothing. That is how two sessions read `xcodebuild` as 3 and 1
minutes apart and each believed their own number, and why a `swift-frontend` reading of 1 against 0
live processes cannot be classified: **"the process ended" and "the number is old" are
indistinguishable from the output.**

The structural fix ranks above any matching fix: **a family count of zero must be distinguishable from
a family the matcher cannot see.** They are the same integer today, which is what let this survive
being read by twenty sessions rather than being noticed once.

---

## A fix that satisfies the accounting while leaving the claim false

*Warden Design, measured against a routed finding rather than adopting it.*

sidetone measured its own register at 95 of 95 rows carrying `sha256`, `bytes`, `recorded_at` and
`recorded_from`, 0 of 95 unfindable — which suggested a third option beside commit-the-captures
or drop-the-evidence-rung. Routed to Warden with an instruction to measure before adopting.

**It measured, and refused.** `sha256` on 5 of 34 rows and 4 of 13; `capturedAt` 5 of 34 and 2 of
13; **`bytes` and `recorded_from` absent entirely.** 30 of 34 and 12 of 13 rows are a path plus an
`unpublishedReason` — a declaration file, not an attestation register.

**And the second reason, which measuring cannot reach.** Warden's own gate rules that *a visual
claim without pixels is a structural assertion in disguise*, and the two affected cases claim the
`raster-visual` rung. A hash names a capture; it does not let a reader see one. So a register row
would satisfy the **accounting** on both silent denominators while leaving the **rung** claim
false — *"that passes, which makes it worse than the defect it replaces."*

The only instance in this corpus where **the proposed fix was itself the vector**, turning a
visible failure into a silent pass. The third option is a prerequisite, not a narrowing.

---

## A correction that introduces an error

*Google Drive Fixes, self-caught.*

It generalised SCR-0102's true statement about **its five cases** into a claim about all
fifty-eight, and wrote that into `ARMADA.md` **as a correction to the entry it had just fixed**.
Measured: 58 cases, 10 passing, four lanes; scrim's two lines only.

Nastier than the original error, because **a correction carries more authority than what it
replaces** — a later reader treats it as the settled version. Three properties compound, and the
session that made it named them: SCR-0102's sentence was **true**, so a reader following the
citation finds it confirmed; *"all five of its cases"* and *"all"* differ by a word no numeric or
paraphrase sweep flags; and the correction gets **less** scrutiny at exactly the moment it deserves
more. The rule that would have stopped it: **carry a finding's denominator when you quote it.** Sibling of Diolog Tasks' rule that a
false claim "gets worse with repetition", with the repetition happening inside the fix.

---

## A silent fallback is a correctness bug wearing resilience as a costume

*Diolog Presentations.*

**Every failed deploy attempt returned HTTP 200 and status `ready`.** The same allow-list for the
needed field existed in **three places** — an extracted TS module, an inline copy inside a
`String.raw` template which is what actually ships, and a zod request schema that strips unnamed
keys — and the two that were not load-bearing got fixed first. *A deploy that changes nothing is
indistinguishable from one that works if you check the exit code instead of the artifact.*

**What broke the loop was making the failure loud**: a missing browser now throws with a named
reason rather than falling back to the old renderer, which turned the next attempt from a mystery
into a one-line diagnosis. Result: 11,443 characters extract from the new output against **10**
from the old on the same deck — the old was pictures of missing-glyph boxes, because `sharp`
rasterises SVG through resvg, which reads fontconfig and cannot fetch a webfont, in a sandbox with
no fonts.

---

## The stricter the mutation rule, the more certainly the control fails

*Egress, with Errand arriving at the same conclusion independently.*

A harness requiring **every** mutation to apply can never pass its own control, and the natural
repair deletes the only leg proving the harness can report green for the right reason. Egress:
*"an exempted control proves nothing — it is excused from the rule rather than satisfying it."*
Errand, separately: *"a control that cannot fail has not been run, it has been performed."*

The cheap discipline that catches the whole family: **ask what your control would do against a
subject known to be good.** `git archive main | tar -x` fails that before it is ever run — and it
did not produce a wrong answer, it produced **a right answer with unusable provenance**.

Two sweep corrections from the same session, both worth copying as worked examples:

- A predicate grepping `sys.argv[1]` missed two tools taking `sys.argv[1:]`, so they ran
  argument-less, **exited 2, printed their docstrings, and were counted as passing.**
- A denominator column took the **first** `examined=` per tool, reading 19 where the tool's own
  total says 168.

---

## A count over a field with no declared grammar is not computable, and everyone picks one silently

*Splice, correcting a figure it had already sent as fact.*

It relayed **13 of 30** declared source paths rotted. Its verifier could not reproduce it: **8**
strictly, **11** on a wider reading, with its own out-of-family lane reaching 8/11 independently.
Splice then counted again itself and got **11 with three different members** — `SURF-035/-036/-041`
where the verifier had `-048/-054/-055`.

**Four careful readers, four answers.** The root cause: the `source` field holds **four distinct
grammars and has no parser**. Measured on `main` across the 76 records carrying one:

| grammar | count | example |
|---|---:|---|
| plain path | 54 | `docs/PRD.md` |
| path + section anchor | 20 | `docs/PRD.md §1.2` |
| several paths in one string | 1 | `REQ-023` |
| `path:line` | 1 | `docs/MARKETING-FEATURES.md:23` |

A naive existence check over all 76 returns **37**, almost all false, because a section anchor is
not a path. **No count over that field was ever computable without first declaring the grammar,
and each reader silently picked one.**

So the correction is not 8 or 11. **The figure needs its predicate published beside it.** That
repo had already learned this once — a `32` and a `25` in the same document were *both derivable
under different predicates*, and the recorded lesson was **the defect was never the value, it was
the missing predicate.** Same shape, one field lower.

The sting: the number was asserted in **five places including inside `inventory.json` itself**, in
an item titled *the campaign's own records must not lie*. The thesis failed on itself, and it was
propagated before it was checked.

---

## "It has never fired" is a claim about your attention, not about the hazard

*Splice.*

Its own note read that DEF-084 *"has never fired because every id was allocated serially from the
main checkout."* Then the new gate ran for the first time and found `LEDGER.md` reading
`Last allocated: 76` over a table **already holding SPL-0078** — the lost-write signature, present
in the tree at base, before the item touched anything.

**The defect had already fired and nobody had noticed.** The register held the evidence the whole
time. A hazard reasoned about in the abstract had a live instance sitting in the file being
reasoned about.

Companion measurement from the same run: **13 of 30 declared source paths had already rotted** —
43% silent decay, which is what the `(path, symbol)` pair was built to catch and what nothing had
been looking at.

---

## A critic catches the flaw at the top level and the same flaw survives one layer down

*Splice, and the strongest single argument in this corpus for keeping the out-of-family lane
mandatory even when it is single-lane and degraded.*

An out-of-family critic broke the item's central claim and was right: the first `id-allocation.py`
was a **static register parser that never invoked the allocator**, so reverting the lock would have
left every assertion green. DEF-068 and DEF-084 were closed *by arming*, not *by construction*.

**The repair then reproduced the flaw one level down.** `test-allocate-id.py` drives `--kind
feature` only. The lock, journal and floor are shared across kinds, which is why the three reverts
correctly go red — but the **campaign-kind write path is driven by nothing**, and reintroducing
DEF-068's read-modify-write for `DEF-` ids leaves both new instruments at exit 0. So the defect the
item is *named for* is constructional for the half it shares and armed-once-by-hand for the
delegation half.

**Third time in one evening the out-of-family lane earned its cost by breaking a decision rather
than confirming one.** A lane that only ever agrees is not paying for itself; these three did the
opposite, and that is the argument for keeping it even at a downgrade.

---

## A field that records what goes red for open defects records nothing for closed ones

*Splice, measured after flagging it as a suspicion.*

The `reproduction` field was designed to move from `owed` to `oracle` or `case`. **That is
unsatisfiable for a fixed defect**: both kinds verify against registers of *standing red* signals,
and a fixed defect has none. So the field records what would go red for **open** defects and
**nothing at all for the guards protecting closed ones** — which makes every such guard exactly
the accidentally-load-bearing assertion the design was built to eliminate.

Confirmed by reverting it rather than arguing it: `reproduction-obligation.py` **`continue`s on a
missing record**, so deleting a defect's `reproduction` block leaves the gate at **exit 0** with
its population silently 6 → 5. The binding is removable without a sound.

**This design has been propagated to three repos.** They need a sixth state before building
further — *this is fixed, and this is what catches it coming back*.

---

## The trigger was a linked worktree, and the general claim hid the condition

*Google Drive Fixes, correcting a brief it had asked to be distributed.*

Its brief said *"Git exports `GIT_DIR` into hook processes."* Measured over four real pushes on git
2.50.1, then reproduced independently against a sacrificial repo and a bare local remote:

| pushed from | `GIT_DIR` in the hook |
|---|---|
| a normal checkout (root or subdirectory) | **unset** |
| a **linked worktree** (`git worktree add`) | **set**, to `<main>/.git/worktrees/<name>` |
| a caller-set value | passes through |

**So the trigger is a linked worktree, and that alone explains sixty-two green runs followed by one
destructive push** — the check was exercised from a normal checkout; the push that broke things came
from a worktree.

The general phrasing was worse than wrong, it was *misdirecting in both directions*: a project that
never uses linked worktrees is not at risk at all and would have patched something it does not have,
while a worktree-using project reading the corrected table could conclude the general claim was the
overstatement rather than the condition being the point. **Every fleet here works in `.worktrees/`,
so every fleet is permanently in the affected case.**

**And the correction carried the same shape it was correcting.** The runner fixed the measured table
at lines 39-47 and the runner block, and left **line 14's headline** reading the old general claim —
in the one file whose entire purpose is being copied verbatim, where a reader may take only the
opening sentence. *Detail corrected, headline left.* Re-pull any brief circulated before that fix.

---

## `${VAR:-default}` cannot distinguish unset from empty

*Google Drive Fixes. One character, and it fails toward under-reporting.*

A probe printed `GIT_PREFIX=[UNSET]`; the runner reported it **set but empty**. The runner was
right. `${GIT_PREFIX:-UNSET}` substitutes for **unset or empty**; `${GIT_PREFIX-UNSET}` — no colon —
distinguishes them. Anyone probing environment inheritance hits this, and it under-reports what a
child actually receives, which is the direction that manufactures a false absence.

---

## A coverage mechanism that asserts the union cannot see a substitution

*Google Drive Fixes, found inside the mechanism written to make a trim visible.*

Its coverage check asserted the **union** of tags, so a retag stayed green because two other cases
carried the same name. The same substitution shape as SCR-0080 — appearing inside the instrument
built to catch it.

Alongside it, a refutation worth keeping because the direction was right and the accounting wrong:
*"the seconds are 62 process spawns, not 62 checks"* — actually **40 of the 62 checks cost 37 ms
between them**, while `build_fixture` was 1.412 s over ~65 git spawns (50%) and per-case `sh`
spawning 1.166 s (41%). Acting on the framing alone would have recovered 41% and called it done.
The quoted `3.5-4.3 s` did not reproduce either: 2.19-2.97 s.

Result after repair: **2.19-2.73 s → 0.73-0.97 s**, measured old-against-new in **alternating runs
so both figures share a load window** — the right answer on a machine that moved between 0.5 and 441
in one day. Fixture rebuilt as `git init` + `git fast-import`: 1.412 s → 0.068 s. Checks 62 → 86,
nothing dropped, and the port checked against the script it replaces over 1,593 distinct paths with
**1 difference, the intended one**.

---

## Two blockers that both present as an unarmed case

*Graft.*

**"The harness cannot express this cell" and "the product has no such distinction" are different
blockers and they look identical from the register.** Closing BLOCK-0002 split into three causes:
the config gap (real, fixed — `playwright.config.ts` carried only `use: { baseURL }`, so the suite
could be green over every spec and never reach a 1440-dark cell); an absolute
`file:///Users/…/index.html` route resolving on one machine only (**the file tracked, the recorded
path not**); and the deciding one — `design/marketing/index.html` has **zero `prefers-color-scheme`
blocks and zero width media queries**, so at 1440-dark it renders identically to 390-light and a
test there would pass while distinguishing nothing.

Arming that case was the easy half and the dishonest one. It needs an owner decision — the cell is
wrong for a surface with no theme axis, **or** marketing is missing dark mode and that is a product
gap — not a test. Recorded unarmed *with the cause*.

**The test for the split: whether every case in a cluster fails for the same reason, not whether
the cluster's summary reads coherently.** Graft split four cells into two clusters on their recorded
reasons and still merged two causes inside one of them. Splitting once was not enough.

The arming pair it produced is the shape worth copying, because **each mutant fails on its own
axis**:

```
mutant-light  (1440, light)  -> BOTH tests fail
mutant-narrow (390,  dark)   -> ONLY the width test fails; matchMedia correctly still passes
restored                     -> 2 passed
```

Two-way assertions throughout, because a dark check that only asserts the dark value passes on a
page that hardcodes it. And a `default` project deliberately carrying **no** viewport or
colorScheme, so the 149 existing specs run exactly as before — **a suite that changes under a
config edit cannot be the control for that edit.**

---

## A signal visible to every runner and disbelieved by the only party who could act

*Warden Design, correcting itself.*

Two runners reported a pre-existing gate failure. Warden refuted them — and was wrong, having
checked `main`, where the untracked files happen to sit on disk, rather than a worktree, where they
do not. It made **exactly the error it had just finished documenting**: reading a green from a
checkout that carries files git does not.

**The instrument that settles it is a branch that could not have caused the failure.** WAR-0054
touched no captures, so its exit 1 is the baseline with nothing of its own mixed in: 3 claims, all
CASE-002 and CASE-020. Neither reading the report nor checking main separates the two.

So: **a runner reporting a pre-existing failure is a claim like any other — and so is an
orchestrator refuting one.** The right scepticism applied in the wrong direction, needing a third
branch to settle.

And the defect sharpens one more turn: **`campaign.py check .campaign` has been failing in every
runner worktree this whole fleet while passing in the orchestrator's working directory.** Not merely
invisible to the gate on main — *visible to every runner and explained away by the one party
positioned to act on it.*

The separable remainder is a schema problem rather than a missing capture: two cases carry **prose**
in an `evidence` field that a `raster-visual` artifact check resolves as a filename, so
`marketing-frame.py --gate -> 7 checks, 0 failed; …` is reported as a missing pixel artifact.

---

## A schema problem wearing a missing-capture's clothes

*Warden Design, acting on "say it on the case".*

A gate resolved **every** entry of a `raster-visual` case's `evidence` field as an artifact path.
Two cases listed the captured frame's path *and then a sentence* describing what the measurement
found — so the sentence was reported as a missing pixel artifact, printed **directly beside two
genuinely absent captures and indistinguishable from them**.

The reported "5 pixel claims with no usable pixels" was **3 real and 2 schema**, and the schema pair
made a real pre-existing defect look half again as large as it is. Moved to `note` and kept rather
than deleted, with the note saying why.

**The transferable shape: two different defects printed under one heading, where the louder one
recruits the quieter one into its count.** It inflates a real number rather than inventing a fake
one, which is exactly why nobody questions it. Look wherever a gate resolves a free-form field as a
path.

Same session, the register question one turn further: warden's *new* capture row carries `sha256`,
`bytes`, `capturedAt`, `derivedFrom` and the full CDP channel spelled out — written at the shutter
by a runner that did not know the register question existed. **So the register is thin in the old
rows and correct in the new one: the gap is historical rather than structural.** It still does not
move the decision, for the reason measuring cannot reach — a hash is not pixels, and the rung claims
pixels.

---

## Code inside a string has two parsers, and the outer one wins silently

*Diolog Presentations.*

A file generating JavaScript inside a `String.raw` template bit three distinct ways in one session:

- a **backtick in a comment** closed the template;
- a bare **`${`** inside a regex character class opened an interpolation;
- **slicing the block out to test it kept the source-level escapes**, so the extracted copy behaved
  differently from the shipped one — a control that was not the thing it controlled for.

**None of the three produced an error where the mistake was.** The general form: code-in-a-string
has two parsers, the outer one wins, and it wins quietly. Sibling of the same session's three copies
of one allow-list, where the copy that actually shipped was the one inside the template.

---

## An idle session is not necessarily yours to fill

*Diolog Presentations, declining work.*

Offered something to do while idle, it refused on grounds worth keeping: *"My queue is Luke's to
fill. A peer handing me work would route around the person who decided this session's scope, and
'the session looked idle' is not a reason to change what it is for."*

**Idle is a legitimate state for a session between its user's instructions**, and a conductor's
starvation watch cannot tell an under-fed session from a correctly-scoped one that is waiting. The
same session had been excluded from the fleet by its user at the outset — so a conductor apologising
for not dispatching to it was apologising for respecting a boundary it did not know existed.

Ask what a quiet session needs. Do not assume the answer is work, and do not assume it is yours to
supply.

It also declined the berth for the reason worth copying: *"nothing in flight, so a berth I hold is
one Graft or Warden cannot."*

---

## Resolve the conflict in a tree you own, so the shared branch takes a fast-forward

*Diolog Tasks, landing 251 unmerged commits onto a branch another session had work on.*

The obvious order is to merge your branch into the shared one. It puts every conflict resolution
**on the shared branch — a place nobody owns** — and whoever else has work there inherits a merge
they did not perform and cannot audit.

The order it took instead: **merge `staging` into the fleet branch.** Conflicts resolve in its own
worktree, under its own gates (clean auto-merge, zero conflicted files, 0 typecheck errors on both
apps). `staging` is then an **ancestor** of its HEAD, so updating the remote is a **fast-forward with
nothing to resolve**.

What that buys the other party, and it is worth saying to them explicitly because it is not obvious:
a push moves only the remote ref, so **their working tree and uncommitted work are untouched** and
they pick the commits up on their next pull. The risk stayed entirely on the branch of the session
that chose to take it.

Generalises past git: **do the reconciling in a tree you own, and hand the shared thing a change
that cannot fail.**

---

## A card with no requirement trace is a card a runner has to guess at

*Diolog Tasks, declining to dispatch runners at ten cards.*

Ten cards had never had a graded requirement list, and the fast move is to send fix runners at them
anyway. It graded the requirements first instead, and the reason is the corpus's central pattern one
stage earlier than everyone else met it: **the runner would return something confident and
fix-shaped, and nothing downstream could distinguish it from work that was actually specified.**

Everyone else tonight paid for this by finding it in a verifier's output — an absence claim over a
crop, a finding about code that was not in the packet. Grading the specification first is the cheap
version of the same check: **an under-specified brief and a well-specified one produce output that
looks identical, and only one of them is answering the question.**

---

## Ask what the instrument does not read

*Proctor Design, via an out-of-family reviewer that was the only one to ask.*

`shot_disposition.py` checks `captures.json` against the files on disk — correctly, and it passes.
**It never reads `cases.json`.** So a case citing an image that is unpublished, misnamed or absent
is invisible to it, and two separately-filed defects turned out to be instances of a class the
instrument structurally cannot see.

This is a **different probe** from the three already in this corpus, and it is the one that finds
what they cannot. Those ask what a result means: a check returning nothing has two readings; a set
returning members has two; an instrument can answer a narrower question than the one asked. All
three interrogate the **output**. This one interrogates the **inputs** — and it fires on an
instrument whose output is entirely correct.

**Its form: name every register the check reads, then name the registers it does not, and ask what
class of defect lives only in the gap.** A gate comparing A against B is silent about C by
construction, and nothing in its output will ever hint that C exists.

It took a reviewer to find it, and it took a reviewer *from another family* — one that had not seen
the in-family reasoning and therefore had no reason to inherit its frame. A gate cannot ask this
question about itself.

---

## Independent agreement is worth as much as disagreement, when the family was unexposed

*Proctor Design, refining the case for the out-of-family lane.*

The standing argument for that lane is that it **breaks** decisions — three times in one evening it
refuted a claim the in-family work had settled, which is what a lane that only ever agrees can never
do.

The refinement: the same reviewer **agreed** with the item's central judgement — that inspecting a
bitmap can verify the subject but cannot establish the capture target without fabricating metadata —
independently, in its own words, and it was *the judgement its author was least sure of*.

**That agreement carries real weight precisely because the family had not seen the in-family
reasoning.** Two Claude instances agreeing may be one frame counted twice; a different family
arriving at the same conclusion without the reasoning is evidence about the conclusion rather than
about the frame.

So the lane's value is not "it disagrees". It is that **its agreement and its disagreement are both
informative**, which is only true while its inputs are genuinely independent — the same condition
that makes any two-instrument agreement mean anything.

---

## A correction that arrives through a channel the rule was built for

*Proctor Design, on the standing-grant relay it had declined.*

It refused a relayed authorisation, correctly, and held that position for hours. The operator then
answered **in that session's own channel**, and the position ended immediately.

Worth recording because it is the rule succeeding rather than failing: *"your rule held right up to
the point it stopped applying, which is what a good rule does."* A refusal to act on a peer's relay
is not a commitment to the refusal — it is a statement about the **channel**, and it expires the
moment a channel that can carry the decision does.

The conductor's job around that is narrow: relay the *fact* that a decision exists so the peer knows
what is coming, never the authority, and then get out of the way of the channel that can settle it.

---

## Two instruments partition a question, and neither knows the partition exists

*Splice, filed as DEF-091. Not revealed by a merge — **created** by one.*

Two branches each bound their closed defects to a guard, by different mechanisms. Of **71 closed
defects, seven carry a `reproduction`**: six of kind `guard` — exactly one author's own — plus one
`owed`. The other author's five closed defects carry `null` and are bound the other way, by **case
rows citing their guard files**.

**So there are two binding mechanisms, each with a population of exactly its own author's work, and
neither is aware of the other.** A closed defect bound by a case row is invisible to the ratchet; one
bound by a `guard` is invisible to the evidence check. **Each instrument reports honestly over what
it can see. No instrument sees both, so none can answer the question both were built to answer.**

This is distinct from *an instrument answering a narrower question*: nothing here is narrow, and both
answers are complete over their own population. The defect is the **partition** — and it is invisible
from either side, because from inside either mechanism the coverage looks total.

**The second author's choice was correct, which is what makes this structural rather than a fault.**
The ratchet did not exist on `main` when it needed a binding, so adopting it would have made one
branch depend on an unmerged other. It recorded a composition caveat saying the two held at the
mechanism layer and were unproven at the register layer. They *do* compose — clean at row level,
every gate green. **What the caveat did not anticipate is that they compose without covering each
other.** Composition and coverage are different properties and passing the first says nothing about
the second.

**And the reason that is not obvious**: passing composition *feels* like evidence for coverage,
because both are answered by "do these work together", and a merge clean at row level with every gate
green is exactly what a coverage proof would look like. The caveat that was written was not lazy — it
**named the right axis and then tested its neighbour**. *A caveat that names the risk and measures its
neighbour is worse than none, because it reads as discharged.*

**The merge did not reveal these — it created them, and the distinction changes the advice.**
Measured: **0 + 0 = 15.** Both branches were individually green *on the very instruments that fired*,
each verified by its own fresh-context verifier; the merged tree produced fifteen findings. The
allocator and its bypass detector did not exist on one branch; the six hand-written case rows did not
exist on the other. **The finding was not present in either** — six ids written by hand were a fact
about that branch and *not a defect until a bypass detector existed*, and the partition did not exist
until both mechanisms did.

*"Not reachable from any single branch"* invites looking harder in branches, which cannot work.
**"Created by the merge" gives the actual instruction, and it is cheap: resolve, run everything on the
merged tree, fix, then commit — in that order.** Committing first and gating after would have put a
fifteen-finding tree into `main`, to be found later or not at all.

Two of the fifteen are worth naming:

- The shared allocator caught **six hand-written case ids** the moment both halves met, written by
  hand because the allocator did not exist yet, and named all six with its own `--adopt` remedy.
- The artifact oracle caught the merge making the published pages stale — 171 cases printed against
  a register of 177 — and **the first regeneration produced a page with no embedded images, on which
  the oracle exited 2 rather than passing.** *A page with no pictures is not a page with correct
  pictures*: an empty-population floor firing on its own author. **And the floor was not written for
  that case** — it was written so an empty *capture* population could not read as clean, and it caught
  an empty *embed* population produced by a forgotten regeneration flag. **A floor written for one
  empty population caught a different one**, which argues floors should be structural rather than
  per-case: classify the whole space, refuse the unclassified, and you catch what you did not
  enumerate.

And the register merged **row-level with zero both-changed rows**, where `-X ours` would have kept
six false findings.

---

## Resolve the name before reporting the absence

*sidetone, catching its own third reference-point error of one night — the second inside one piece of
work.*

Three cited guard scripts looked dead: `scripts/check-spec.mjs`, `scripts/mutation-lock.mjs`,
`scripts/check-literals.mjs`. **All three exist**, at `packages/design-tokens/scripts/`. The citations
name a bare `scripts/X` for files that live elsewhere, and the check tested the cited path
**literally** instead of resolving the filename.

`check-literals.mjs` is in `gate:checks` right now, so the most load-bearing of the three would have
been the first false positive.

**The rule: when a measurement produces an alarming absence, check the resolution rule before
reporting the absence.** It joins the family — the persisting `cd`, `git archive` with no `.git`,
HTTP 200 on every failed attempt, `git diff main..branch` reading 23,000 phantom deletions — and it
shares the property that makes that family dangerous: *the alarming reading is the believable one.*

**Design consequence, and it is the useful part:** a checker over guard citations must **resolve
filenames rather than test cited paths**, or it reports vanished guards that are present. Any new
obligation kind that fires on a path string will fail on its first real corpus.

**Prior art worth having before building one:** that repo already tried the obvious version —
extending `check-case-citations` to read `repro` — and **reverted it**, because the checker reported
one defect's own account of its adrift citations *as* adrift citations. So the naive widening has
been attempted and failed for a real reason, which is an argument that the fix must be a **distinct
field** rather than a widening of an existing scan.

Measured population there: **105 defects marked `fixed`, 57 name a guard, nothing verifies any of the
57, and no guard has actually vanished.** The hole is real and nothing has fallen through it yet — a
useful state to catch, and only visible to someone who measured rather than reasoned.

---

## A residency is not work, and admission control that counts residencies shuts the door on an idle machine

*sidetone, on the berth pin.*

A dev server held 2 of 10 berths on **0.28 seconds of CPU across 37 seconds**, while load sat at
**0.468 per core** and `available` read **0**. Eight sessions were idle behind it.

**A dev server is not work, it is a residency.** The governor should meter *work that finishes*;
anything long-lived needs a different lane or no lane at all. The invocation rule — *wrap the test
command, never the server* — follows from that rather than being a separate tip.

And the supervised-tail wrinkle: the holder pid **moves** when a runner restarts the server, so the
pin recurs per restart. Watching for a long-lived pid finds nothing; the tell is that **the berth
count never drops between holders.**

**And a residency has two sub-cases that read identically on the board — only `ppid` separates them.**
Measured on one claimant set: a `coordinator obs server` held deliberately by a live parent that
intends to kill it at handback, beside a `vite preview --port 5399 --strictPort` at **0.29 s of CPU
over 11 minutes whose parent was `launchd`**. Both are long-elapsed, near-zero-CPU claimants; one has
an owner who will clean it up and one has been **reparented and has nobody left to stop it**.

`--strictPort` sharpens it: the orphan also poisons its own port for the next run, which fails rather
than picking another.

**And the first version of this rule was wrong in the direction that breaks things — corrected the
same hour, by the session that was told to act on it.** It read *"a deliberate hold is a wait, an
orphan is a leak."* It is not. That session checked before killing and found the orphaned preview was
**in active use**: 25 references to its port across the last 200 events of the run's transcript, the
most recent one being the transcript's own last write. The web-observation phase was reading it at
that moment. Acting on the rule as written would have killed a load-bearing service mid-run.

**`ppid` answers who will clean it up. It says nothing about whether anyone is using it.** Two
independent questions, and only the pair decides:

| | nobody using it | in active use |
|---|---|---|
| **live parent** | it will be cleaned up; leave it | wait |
| **orphan (`ppid 1`)** | **kill it — nothing else will** | hold, and put it on an explicit kill list |

The bottom-right cell is the one the first version erased, and it is the common case for a service a
run depends on: no parent to reap it *and* load-bearing right now. It needs **both** actions — hold
now, and record it for explicit termination at handback with berth verification, because the thing
that would normally clean it up is gone.

**The consumption evidence is what settles "in use", and it is not on the process.** CPU is near zero
for an idle *and* a serving preview. What decided it was the consumer's own record — the run's
transcript referencing the port, recently. So: read `ppid` for ownership, read the consumer for
liveness, and never infer the second from the first.

---

## A caveat a consumer cannot see is not a caveat

*MCP Router, auditing the instrument the whole fleet reads for admission.*

`berths.py` emits `occupants` as **one row per slot**, each repeating its job's declared `weight`. So
the obvious consumer operation — `sum(o["weight"] for o in occupants)` — counts a weight-8 job eight
times. Measured: **10 rows, 2 distinct pids, and that sum returns 68 against a capacity of 12.** Not
subtly wrong; 5.7× the machine, with nothing in the output to say so.

**The source already carried the warning**, in a comment directly above the line: *"summing the field
would count it three times over."* The JSON did not. **A caveat that lives where the consumer cannot
read it has not been given** — and the consumer of a script is whatever parses its stdout, never
whatever opens its source.

Fixed by making the correct operation the obvious one: a deduplicated `claims` array, one row per
distinct claim carrying the `slots` it holds, where `sum(c["slots"]) == in_use` by construction.

Three more results from the same audit, and the discipline is as valuable as the findings:

- **A negative result, stated as a result.** The memory and disk blocks answer the question their key
  names claim — `free_pct` 41 against `vm_stat`'s 40%, `free_gib` 231.9 against `df`'s 232Gi — and
  disk correctly reads `/System/Volumes/Data` rather than the read-only volume that reports 5%.
  "Audited and found nothing" is a finding; leaving it unsaid makes the audit look narrower than it was.
- **`ceiling` moved 10 → 12 between two reads minutes apart with the same two claimants**, so
  `available` went 0 → 2 **with nothing released**. Whatever drives the ceiling is not occupancy, and a
  consumer reading `available` as "slots I may take" watches it move for reasons the output does not carry.
- **`held_by_descendants` recorded as UNTESTED rather than correct.** The key exists and reads 0; a
  descendant case could not be constructed without starting work the session was held from starting.
  *"I would rather leave it visibly open than let a 0 stand as a pass"* — the whole exercise in one
  line, since a 0 from an untested predicate is exactly the absence-read-as-success this corpus is about.

And its closing read on its own tooling: *"berths currently reads `available 2`, which after tonight I
am reading as 'do not trust the 2' rather than 'take both'."*

---

## The thing that ran is not the thing you inspected

*This skill's own author, and the second time in one night for the same family.*

The berth-leak watch kept re-announcing an unchanged condition. An hour went into fixing it: three
real defects found and repaired, each control run, each passing.

**The live watcher is a copy at `~/.claude/flagship/armada_watch.sh`. Every edit and every control
ran against the repo source at `plugins/flagship/.../starvation_watch.sh`.** Measured when the two
were finally compared: **live 265 lines carrying the old dedup; repo 316 lines carrying the fix; zero
occurrences of the new form in the live file.**

**Every control passed, against a file nobody was executing.** And the failure presented as the fix
being *incomplete* — the events kept arriving unchanged — rather than as the fix being *elsewhere*,
which sent an hour into deeper repairs of an already-correct file.

Same family as reading a plugin's behaviour from a Dev checkout while a session loads the installed
cache. **A fix verified against the source is not a fix to the running system, and the two are
indistinguishable from the test output.** Before debugging a live symptom, establish *which file the
running thing actually loaded* — `TaskStop` naming the command, a `ps` line, an install manifest —
and diff it against the one being edited.

**Three routes to the same failure, measured on this machine in one night, and the third is the one
no diff would have caught:**

| route | what you inspect | what runs |
|---|---|---|
| **Installed copy** | the repo source | a copy under `~/.claude/`, or a plugin cache |
| **Stale cache** | a Dev checkout | the version a session actually loaded |
| **PATH shadowing** | `find`'s behaviour | `bfs`, answering to the name you typed |
| **Mid-run edit** | the file you just fixed | the *old* code, until it resumes **into your edit** |

**Two axes, not one route.** A peer separated them and the distinction is what makes the fourth
findable: the first three are **spatial** — the artifact that ran sits at a different *path* — so a diff
or a `type -a` finds them. The fourth is **temporal**: same path, same file, edited *mid-execution*, and
**nothing about the path would have warned you.**

**The mechanism, and it is the fix**: `cp` writes **through the inode** a running process is mid-read of,
so the process resumes into new bytes at an old offset. `mv` swaps the **directory entry** — the running
process keeps reading the old inode to completion, and the next start gets the new file. **So: write to a
temp path, then `mv` it into place.** Never `cp` over a script that may be executing.

**And this one inverts the usual failure.** Everything else in this corpus is *a green that meant less
than it looked*; this is **a red that meant less than it looked** — a task marked failed over a mechanism
that had already fired correctly and written its output, with a syntactically valid file left behind and
nothing to reproduce.

**The fourth is the nastiest and it is this file's author's**: a running watcher's script was
**overwritten while it ran**. zsh reads a script incrementally from a file offset, so the process
continued on its old logic and then **resumed into the middle of the new file** and died on a parse
error — *after* it had already done its job and written its output. The result was a task marked
**failed** over a mechanism that **succeeded**, with a syntactically valid file left on disk and nothing
to reproduce. **Never edit a script that is currently executing**: write to a new path and swap, or stop
the process first.

The third is glm-cf's: **`bfs` shadowing `find` broke a wait-loop invisibly** — the script was
correct, the binary was not the one it was written against, and nothing in the failure named a
different program. A file diff cannot find that one, because there is no second file to diff; the
check is `type -a <name>` before trusting a tool's semantics in a script that others will run.

**What unites all three: the artifact you reasoned about and the artifact that executed were different
objects, and every test you ran was honest about the wrong one.** The general discipline is to
establish identity before behaviour — which file, which version, which binary — and to do it *first*,
because every symptom afterwards is consistent with both the bug you are hunting and the one you
cannot see.

The three defects underneath were real and are worth keeping, because each was found only because the
fix before it was controlled rather than assumed:

1. **The dedup compared the rendered message**, which embeds elapsed time and CPU. Both move every
   iteration, so it could never equal itself: the same held server announced at 10:19, 11:41, 13:02,
   15:47 — nothing changed but the clock.
2. **Keying on the pid *set* was still wrong, because the set flaps.** A claimant whose children turn
   over during a sample is correctly excluded that round and re-qualifies the next, while the registry
   underneath sat stable at `{77393, 81187}` across five consecutive reads. So the unit is the **pid**
   and the event is **entry**.
3. **Fixing (2) broke a working detector.** The edit replaced the *first* matching `print -r -- "$out"`
   in the file, which belonged to a different function — so the daemon check emitted a stray line and
   the leak check never emitted its key at all. Repaired by line number, because pattern-matching is
   what caused it.

**And the controls were configuring nothing.** They passed `MIN_HELD_SEC` where the script reads
`FLAGSHIP_MIN_HELD_SEC`, so both ran on defaults and the *negative* control returned 2 where it must
return 0. With the right names: 1 announcement across 4 iterations, and 0 when nothing qualifies.

**No exception was added for the known deliberate hold**, on a peer's argument that settles it: *an
observation server held on purpose and a berth genuinely leaked look identical from outside, and the
one that matters is the one you cannot see.* A first true positive after three false ones is a
detector earning its keep, not one needing a filter.

---

## Check reachability before an ordinary operation destroys it

*MCP Router, cleaning up spent worktrees.*

Seventeen verifier worktrees were removed and disk went 232 → 245 GiB free. Before removing any of
them it checked that **every worktree HEAD was reachable from a branch or a tag** — and that check is
what mattered: **seventeen verdicts existed only as detached-HEAD commits inside those directories,
reachable from nothing.** Every Done, every Needs More Work, every finding from that wave, one
`git worktree remove` from being unreachable.

The cleanup was routine. The check was not, and it is the transferable half: **evidence living
somewhere that does not survive the ordinary operation about to be performed on it.** Tag first, then
remove.

---

## Git's empty-commit refusal protects one file and protects two not at all

*Splice, auditing its own commits after a disclosure — and the rule that would have caught mine.*

The hazard both sessions were running all night: a `python3 - <<'PY' … PY` heredoc followed by
`git add -A && git commit`, with the shell carrying on past a throw. **What saved one of us was
ordering** — every heredoc asserts its anchor *before* writing, so a failure happens before any
change, `git add -A` stages nothing, and git refuses the empty commit. **A script that wrote and then
asserted would have committed the half.**

**And the refusal is a much weaker net than it looks, because it only ever guards a single-file
change.** In a two-file commit, one file's edit can silently no-op while the other succeeds: the
commit lands with a message describing both, **nothing empty, nothing refused**. That is exactly what
happened here — a `harbourmaster 0.4.0` commit whose message carried a whole `flagship:` section
describing changes that were not in the tree, because the heredoc threw an assertion and the commit
ran anyway. Caught on the next read and amended; nothing would have caught it automatically.

**Two rules, and the second is the one with teeth:**

- **Assert before writing**, so a failure cannot leave a partial change staged.
- **Verify a multi-file commit against its own message, not against its exit code.** `git show --stat`
  and read it back. The exit code answers "did git accept this", never "does this contain what I said
  it contains".

Same shape as everything else here: *a step that failed while the step after it succeeded, and
nothing in between to say so.*

---

## A caveat is a hypothesis and needs the same discipline as a check

*Splice, on why the composition-versus-coverage failure is not hindsight.*

The caveat that missed DEF-091 **named the right axis and then measured its neighbour** — it doubted
whether two mechanisms composed, tested that they composed, and stopped. *A caveat that names the
risk and measures its neighbour is worse than none, because it reads as discharged.*

The framing worth keeping for whoever writes the next one: **the aim was right.** The failure is not
that they doubted the wrong thing; it is that a caveat was treated as a note rather than as a claim
requiring evidence. **A caveat is a hypothesis**, and it earns the same question every other
instrument here does — what would it look like if this were false, and did I measure that or its
neighbour?

---

## Read the weight off the brief, not off an impression

*MCP Router, declining two berths.*

Offered 2 slots for six verification runs, it read the weight **off the briefs it had actually
written** rather than estimating: each run does `make lint` — swiftlint and swiftformat across 549
files plus eight component gates — and several also `make test`, a Swift build and 1786 tests in 222
suites. **A verifier there is not a light serial agent; it is a compile.**

So it waited. *"My six are not light and I would rather say so than take two slots and find out."*

The general rule: **a session is the only party that can price its own work, and a conductor offering
capacity must not also estimate the demand.** Declaring a weight that fits the available slots gets
the inner `governor-run` refused at exit 75 and the work runs unwrapped — a degraded run wearing a
governed one's clothes, invisible to everyone reading the governor.

And the corollary for a conductor: **issue a clearance as an offer with the board attached, never as
an instruction.** Say what is free, what holds the rest, and let the session decide whether its work
fits.

---

## Derive the invariant from the data, not from a list kept beside it

*Warden Design, on a merge that went red where both branches were green.*

Two branches merged clean and two gates then failed: one branch had invented a **required `probe`
field** while unable to see three cases the other branch was adding. Neither could have caught it —
the field was consistent on each side.

**`campaign-preflight.py` caught it because it derives the required field set from the other 69
records rather than from a list maintained beside the checker.** So it noticed a field *it had never
been told existed*. **A hardcoded list would have been silent**, and would have stayed silent
forever, because nobody updates a list for a field they did not know was added.

The principle, and it is the same one behind the status vocabulary and the empty-population floors:
**a check whose expectations are derived from the population adapts to what the population actually
contains; a check whose expectations are written down goes stale the moment someone adds something.**
Prefer derivation wherever the population is the authority.

---

## A green control cannot distinguish "the fix works" from "the fix is not loaded"

*Warden Design, naming this session's own failure more precisely than it did.*

Two failures were compared and the difference is worth keeping:

- **A signal arriving and being disbelieved** — a gate failing in every runner worktree while passing
  in the orchestrator's working directory, with two runners reporting it and being explained away.
- **A signal arriving, being believed, and the *fix* going somewhere the signal could not reach** —
  an hour of repairs, every control green, against a file nobody was executing.

**The second is worse, because the symptom was correct the entire time and so was the reading of it.
Only the address was wrong.** And no amount of care in the fix or rigour in the control detects it:
*a green control cannot distinguish "the fix works" from "the fix is not loaded", and nothing in the
output tells you which.*

So the check has to come first and it has to be about identity rather than behaviour: **verify the
artifact you edited is the artifact that runs, before believing any control over it.**

---

## The tool refused and the shell was not asked

*Warden Design, twice in one night, in its own orchestration rather than in a gate.*

`merge-registry.py` **refused** a merge and wrote nothing — correctly, three records were touched on
both sides. The chained `git add && git commit` ran anyway and committed `cases.json` **with six
conflict markers in it**: invalid JSON, on main. Caught, reset, redone with a `--diff-filter=U` check
before the commit and a parse check after; it never left the machine.

The same night, in the same session: `git merge -F -` **does not read stdin**, so an echo reported
`merged` four times at the same sha.

**Both were its own instruments reporting success over a command that had failed** — this corpus's
central class, arriving in the orchestrator rather than in a gate, where nothing downstream is
watching. The repair is the pair: **check the failure mode before the commit (`--diff-filter=U`) and
the result after it (parse the file)**, because a chained `&&` only knows about the exit code of the
step immediately before it.

**And the refusal deserved defending against impatience with it.** The two branches were disjoint *by
field* — one changed `evidence` and `note`, the other added `probe`, nothing touched by both — and a
field-level three-way merge found **zero genuine conflicts across 69 records**. `merge-registry`
refuses at *record* granularity by design; it named the three needing judgement and declined to pick.
That coarseness looks like a false positive and is precisely what stopped a silent loss of one
branch's credit.

---

## A partial view fails toward alarm — so widen the window before reporting anything urgent

*sidetone, generalising four of its own errors in one night. This supersedes the narrower
"check the resolution rule" phrasing and explains why this whole family propagates.*

Four insufficient looks, three of them inside one stretch of work:

| the too-small look | what it manufactured |
|---|---|
| `head -5` of a script whose `set -euo pipefail` is on **line 9** | "the release path's assess is decorative" |
| testing cited guard paths **literally** rather than resolving filenames | "three guard scripts have vanished" |
| `git diff main..branch` with main 33 commits ahead | "three branches gutted the repo, ~23,000 deletions each" |
| a `^run_link` grep blind to a `run_apple_link` wrapper | "the Apple builds are absent, DEF-064 not closed" |

**None of these is randomly wrong. Every one is wrong toward alarm.** That is not coincidence and it
is the part worth carrying: **a partial view manufactures absence and omission**, because those are
precisely what you get when you look at less than the whole thing — and **absence reads as danger.**

Which completes the causal account of this corpus's most common failure, and joins it to the
propagation asymmetry already recorded:

1. A truncated look produces an **absence**.
2. The absence reads as an urgent **finding** rather than as a gap in the looking.
3. **A false alarm gets forwarded because it is urgent; a false negative gets checked because it is
   disappointing.** So the failure mode selects for travel.

**The rule is cheap and would have caught all four: widen the window before reporting anything that
sounds urgent.** Read the whole file, not five lines. Resolve the name, do not test the string. Name
the reference point. Establish the positive control. Every one of those is seconds of work standing
between a note and a false rejection.

**And the corrected finding is worth having on its own**, because it corrected in the *reassuring*
direction, which is the harder one to catch: that project's release path **does** assess —
`notarize.sh` runs `spctl --assess --type execute --verbose=4` under `set -euo pipefail`, so the
assess is blocking and the success line is unreachable past a rejection. The real gap is narrower and
still real: `notarize.sh` needs notary credentials, so it runs rarely and late, and **no step of
`gate:checks` mentions `spctl` at all**.

Grounding the item also turned up a genuinely broken artifact nobody was looking at — a built
`.app` failing *both* tools with `code has no resources but signature indicates they must be
present`. Not the ad-hoc case; a malformed signature. Which gave the work a real red to arm against
instead of a fixture.

---

## A report that swallows arguments will impersonate a gate for anyone who asks it to

*Warden Design, found by poking rather than by the sweep it was running.*

`nonfailing-assertions.py` **parses no arguments at all**, so `--gate` and `--nonsense-flag` were
equally ignored and both exited 0. As a *report* that is legitimate — it always exits 0, it
over-reports shapes, a human reads them. **What is not legitimate is that it will answer to `--gate`.**
Wire it into a chain and you have a step that **can never fail while looking exactly like one that
can**, and nothing in the chain, the output or the exit code says which it is.

The same defect, independently, in this fleet's own admission instrument: `pressure.py` accepted
`--fresh`, `--no-cache` and `--help` alike, exiting 0 with a cached snapshot. Anyone reaching for a
fresh read got a stale one and never learned the flag did not exist.

**So the rule is about the boundary rather than the tool: a report and a gate are different contracts,
and an argument parser is what keeps a tool from being conscripted across that line.** Refusing an
unknown flag is not pedantry — it is the only thing preventing a report from being installed as a
guarantee. Both tools now refuse an unrecognised argument; both refusals were one-line changes.

And that file had **two independent reasons its green meant less than it looked**: it reported clean
over an empty population, *and* it cannot see the defect class it is named for, because the
equal-to-self shape it matches is syntactic only — which is why it missed both assertions a verifier
caught by reading. Only the first had been found. **When one reason for a weak green turns up, look
for the second**; they are not mutually exclusive and the second is usually the older one.

---

## An empty-population refusal is necessary and not sufficient

*Warden Design, caveating its own sweep — and it applies to every floor this corpus has recommended.*

A sweep ran every local probe against an empty registry. **Five of six refuse it**; the sixth exited 0
printing `examined: 0 file(s), 0 assertion call(s)` — a denominator it computed and never acted on.
Fixed.

**Then the caveat that matters more than the result: the sweep tests the empty case, which is the loud
end.** A population that *shrinks* from 13 to 1 is not caught by an empty-population floor at all,
because **1 is not 0** — and two of that repo's probes do exactly that on a clean checkout. They still
pass, with their denominators collapsed twelvefold.

So every floor recommended here — refuse an empty population, refuse a zero join, refuse an absent
subject — **catches the collapse to nothing and misses the collapse to almost nothing**, which is the
more likely failure and the quieter one. *"I would rather say that than let five-of-six read as
solved."*

What would catch it is a **ratchet on the denominator** rather than a floor under it: record what the
population was, and refuse a run whose population fell without an explanation. Not built anywhere yet;
recorded as the shape of the gap rather than as a design.

---

## Derive from the population — the fifth arrival, and the mechanism stated plainly

*Warden Design, joining four earlier ones.*

The five probes that refuse an empty population **all compute their denominator from the corpus**
rather than being told what to expect. `campaign-preflight` catching a field it had never heard of,
`signature-vs-policy` refusing an absent subject, and `evidence-class` refusing a zero join are one
mechanism wearing three names.

**A checker that derives its expectations cannot be silently outgrown; a checker holding a list can
only ever be as current as the last person who remembered it.**

Five independent arrivals at that principle in one night — the status vocabulary, the empty-population
floors, `campaign-preflight`'s derived field set, the id-space classification, and this sweep — is the
strongest signal in the corpus that it is a real design rule rather than a local habit.

---

## The engine paints DIFFERENTLY, not merely less — one declaration, opposite defects

*Warden Design, 2026-08-22. This amends a documented rule rather than adding to it.*

The recorded guidance is that obscura **paints more than it reports** — `boxShadow`,
`backgroundImage`, `textTransform`, `outline` and `flex` serialize to `""` while painting correctly —
and that an empty computed value means *unreported*. The advice that followed: **trust the pixels over
the readback.**

**Measured case that inverts it.** One declaration — `height: 100%` on a child of a 3px
`overflow:hidden` parent, a percentage height with no definite ancestor — produced **opposite** defects
in two engines:

| engine | result |
|---|---|
| **obscura** | resolved the percentage against the option row, drew the bar at `h:52` — solid rectangles **over the option text** |
| **WebKit** | drew it at `h:0` — nothing at all |

**Same bytes.** So the pixels were not trustworthy either: each engine was wrong in a *different
direction*, and **a single-engine capture cannot say which kind of wrong you are looking at.** The
visual gate correctly returned `fail` on the obscura frame, and the frame was held unpublished rather
than shipped to move a number.

**The instrument that separated them is the transferable part.** A `webkitshot.swift` driving WebKit
through the system framework — no browser, no window, so it stays inside the browsers-via-obscura
rule — used as a **comparison instrument only**, with nothing it produces ever published as a capture.
With two engines the three-way split became readable: **the rectangles were the engine, and the
missing meter was absent in BOTH and therefore the page's own defect.** One frame could not have
separated those. After a `display:block` and a literal `3px`, both engines measure the meters at
`x=462, h=3`, widths `17/83/322` against `17/83/320`.

A third divergence found in the same pass, non-gating: **obscura does not paint an `inset`
box-shadow**, so a selected radio renders as a solid disc where WebKit draws a ring.

**So the amended rule: an empty computed value means unreported, and a *painted* value can still be
the engine rather than the page.** Any capture a visual gate will grade wants a second-engine
comparison lane — not to publish, only to tell an engine artifact from a real defect.

---

## A second manifest nobody reads drifts, and the gate cannot see it

*This repo, found while filing someone else's brief in it.*

Bumping a plugin's version, the edit went into `plugins/<name>/plugin.json` — which exists for **29 of
this repo's plugins** and is not the file anything reads. The canonical manifest is
`plugins/<name>/.claude-plugin/plugin.json`, and `build-catalogue.mjs` compares **that** against the
marketplace entry. **The gate caught the mismatch it checks for and was structurally silent about the
file that had actually been edited.**

Audited across the repo afterwards: **13 of 29 pairs disagree** — `flagship` at 1.1.0 against 1.3.0,
`harbourmaster` at 0.1.0 against 0.4.0, `create-mac-icon` at 1.4.1 against 1.6.0. Every one of those
drifted silently, because nothing compares the two.

Two things worth separating. **The drift is probably harmless** — if nothing reads the stray, a wrong
number in it costs nothing. **What is not harmless is that it is an equally plausible edit target**:
it has the same name, sits one directory up, and the gate's error message names `plugin.json` without
saying which. That is the *third* route from the identity family, arriving as **two files with the
same name in one repo** rather than as a stale copy or a shadowed binary.

Not fixed here: deleting 29 files or teaching the gate a second comparison is a repo-shape decision for
its owner, and the drift has been harmless so far. Recorded so the next person who edits the wrong one
finds this instead of rediscovering it.

---

## One field consulted, a state inferred, the inference wrong toward action

*Three instances in one day, from three sessions, in three different instruments. Named as a family
because the individual entries kept reading as unrelated bugs.*

| field read | state inferred | what was true | who caught it |
|---|---|---|---|
| `claimant_alive: false` on a held berth | the claim is dead, reap it | a shell script had exited; **its descendants held the lock legitimately** | Graft — and it did not act |
| `ppid == 1` on a long-idle claimant | it is an orphan, therefore a leak | orphaned **and load-bearing**: 25 references to its port in the consumer's last 200 events | glm-cf — checked before killing |
| `proctor_doctor` reporting a lane `ready` | the lane works | **the readiness signal is the presence of a name, not a working lane** — the one guest was state `invalid` | sidetone, via a runner |

**All three fail in the same direction: toward doing something destructive or expensive.** Reaping a
live berth, killing a serving process, dispatching a run into a lane that cannot execute. That is not
coincidence — it is the alarm asymmetry again, one level in. A field that *looks* like it answers the
question produces a confident answer, and the confident answers here are all "act".

**And the fix is identical in all three, and it is never a better field: try the thing.** A lock's
descendants are found by looking for them; a service's liveness is in *its consumer's* record, not on
the process; a lane's readiness is established by running something through it. sidetone's runner
*"caught it by trying the lane rather than reading the field, which is the only thing that works."*

The general form: **a status field describes what something declared, and an attempt describes what it
does.** Where the two can diverge, only the second is evidence — and a field that has never been
wrong in your presence is not evidence that it cannot be.

---

## When a two-platform repo keeps missing the same twin, it is one process gap not N feature gaps

*sidetone, from two independently-triaged items.*

Two unrelated P1s resolved to the same sentence. iOS ships an onboarding microphone permission ask
and macOS has none; `verify-ios-capture.py` exists and the macOS twin does not. **Two items, both
"iOS has it, macOS does not."**

Filed separately they are two features to build. Seen together they are **one process gap**: someone
builds the iOS half and the macOS half is never asked for. Fixing them one at a time leaves the
mechanism that generated them running, and the next pair arrives the same way.

**Worth a sweep in any repo here shipping paired surfaces** — the check is cheap and it is a
different question from "what is on the backlog": *for every capability one platform has, does the
other?* A backlog cannot answer that, because the missing halves were never filed.

---

## A dependency on something the dependency does not know it can deliver

*sidetone, removing a declared blocker rather than waiting on it.*

A brief declared *"Depends on: X for the capture mechanism."* Reading X's own spec on its branch: the
lane it would supply reports `ready` and is not, its one guest is state `invalid`, and whether that
lane can do the job at all is recorded **INCONCLUSIVE, each instrument ruled out by name**.

**So the dependency was on a capability its provider had explicitly not established.** And it was
unnecessary on the merits: *isolation stops a capture being disturbed; a subject check proves a
capture is of what it claims.* Different guarantees, and only the second was the defect. Blocking
there **left an open defect open for an unrelated reason** — and kept an item on a critical path it
did not belong to.

The check before honouring a declared dependency: **read the provider's own status for the specific
capability, not its overall state.** A component can be healthy, merged and green while the one thing
you need from it is recorded as unproven.

---

## "The control ran" and "the control took effect" are two claims, and only one is usually checked

*Errand, sharpening a rule this skill's author had learned the expensive way the same night.*

A negative control returned 2 where it had to return 0. The cause was not the logic: the invocation
passed `MIN_HELD_SEC` where the script reads `FLAGSHIP_MIN_HELD_SEC`, so **the control configured
nothing and ran against defaults.** It produced output, the output looked like a measurement, and it
was a measurement of the unmutated system.

Errand's generalisation, from hitting the same shape from the mutation side — its own harness reported
`INERT` and it nearly filed a live guard as decorative:

> **A control that silently configures nothing is exactly a mutation that did not apply.** The harness
> runs, produces output, and the output is about the unmutated system.

So the rule that covers both: **a control must prove it changed something before its result means
anything.** Not "did the control run" — that is answered by an exit code and answers nothing — but
*did the thing I was controlling for actually differ.* Print the value the control set, or assert the
mutated state, before believing what the run reports.

This is the third distinct route into the same hole: an exempted control, a control that cannot fail,
and now a control whose configuration never arrived. All three produce a green that is honest about
the wrong subject.

---

## The artifact advertises the property; the mechanism does not implement it

*Google Drive Fixes, found by its own out-of-family lane. The sibling of the argument-swallowing class,
and probably the commoner form.*

A coverage page was **headed "every figure is recomputed"**. Its figure reader took only the **first
integer of each table row**. So **16 published figures — the whole case-lane table, twelve lane cells
and every percentage — sat under that heading asserted by nothing.**

Same shape as a report answering to `--gate`: **the artifact advertises the property, the mechanism
does not implement it, and both look identical from outside.** A reader takes the guarantee from the
heading, which is the one part nothing checks.

The generalisation worth carrying: **a document that states its own guarantee needs that guarantee
tested like any other claim.** "Every figure is recomputed", "all paths verified", "generated from the
register" — each is an assertion about a mechanism, made in the place least likely to be checked
against it.

---

## A count can be arithmetically correct and attached to the wrong predicate

*Google Drive Fixes, auditing four of its own published figures. The most useful self-audit in this
corpus, because none of these were miscounts.*

| published | actual | the predicate that slipped |
|---|---|---|
| "seven cases blocked on the five conditions" | **five** | matched words anywhere in a row's JSON, not in the `surface` field |
| "no case closed at its own rung, all `macos-glass`" | 10 of 58 pass, four lanes | true of one item's **five** cases, generalised to fifty-eight |
| "28 of 40 surfaces have no case" | **0** have none; 28 have no *armed* case | `armed: true` read as *has a case* |
| "merged tree will be 2277" | 2282 | quoted the **branch's** total instead of computing the merged one |

**Three went into dispatch prompts, two reached documents outside the repo, and every one was caught
by the runner it was handed to — never by re-reading.** The last was made *while writing the entry
telling others to carry a finding's denominator.*

**The tell was available every time and it is one tell: the number came from a one-line query that was
never checked against a known quantity.** The verification query for the 28 returned
`surfaces enumerated: 0` — obviously false for a repo that states 40 elsewhere — and it was read past,
because the wrong key was the bug being hunted.

Two rules:

- **Check a count against something you already know before publishing it.** Not a second query — a
  quantity you already hold. A query that agrees with a broken query is two broken queries.
- **Carry the predicate when you quote someone else's number.** *"28 with no armed case" survives being
  copied; "28 with no case" does not.* A figure travels without its predicate by default, and the
  stripped version is the one that reaches a decision.

**And a third instrument misfire from the same session, on a question it was answering *about*
instruments**: checking whether an unknown-flag refusal was live, it piped through `head -c 200` and
read **`head`'s** exit status, so the refusal looked like exit 0 and the fix was nearly reported
absent. That is this repo's own documented pipeline-exit trap, hit by the session that documented it.
**`$?` after a pipe is the last command's**, and every gate in this corpus that has been read through
a pipe has been read wrong.

---

## A backlog written from notes overstates how much of it is code

*Errand, after three items in a row resolved to a corrected premise.*

An item asked for a colour-scheme oracle because obscura's `setEmulatedMedia` is accepted and inert,
so a dark-mode assertion measures a light render and **passes**. The trap is real, documented, and
**absent from that codebase**: `grep -rl prefers-color-scheme` over the design, website and package
trees returns **0 files**. The mocks express appearance with an explicit `?appearance=dark|light`
query parameter, so there is no media-query assertion for an inert emulation to silently pass.

**And the instrument the brief asked for already existed, built better than emulation** — fetching each
surface twice under the two query values and comparing *rendered* readings field by field, with a live
control in the same run and the pre-fix files served from a **separate tree**, so the old behaviour was
measured rather than inferred from a diff.

Three items in a row from that queue were a corrected premise rather than code. The diagnosis, which
is the transferable part: **briefs written from a campaign's notes describe the general trap, and only
grounding them against the tree establishes whether this repo has it.** That is not a failing backlog
— it is what a notes-derived backlog is. But it means **a row count overstates the code remaining**,
and a conductor sizing work from row counts will over-estimate every notes-derived queue in the
portfolio.

The cheap check before dispatching a runner at any such item: **grep for the thing the brief says is
wrong.** If it is not there, the item is a re-scope and wants a reader, not a builder.

**And that repo's existing instrument had independently reached this corpus's control rule, a week
earlier and better stated:** it reports the *attribute* **beside** the tokens rather than instead of
them, *"because the attribute changing is exactly what the previous grep believed and exactly what was
false."* Same as *a control must prove it changed something before its result means anything* — arrived
at from the observable side rather than the harness side.

**What survived the re-scope is the honest remainder**: `prefers-reduced-motion` and `prefers-contrast`
have no query-parameter equivalent and emulation genuinely cannot set them, so an assertion about
either measures the default and passes. And the first step there is establishing whether *any* channel
can set them at all — **because if none can, the right outcome is a named permanent limit rather than
an instrument.** A limit recorded is a deliverable; an instrument that cannot work is not.

---

## The ladder: a declaration, a behaviour, an attestation

*sidetone, synthesising three findings from three sessions into the rung order.*

> **A status field is a declaration. An attempt is behaviour. A third-party attestation is neither and
> beats both.**

- **Rung 1 — declaration.** `claimant_alive`, `ppid`, `doctor` reporting `ready`, a `--version` string,
  a heading saying *"every figure is recomputed"*. Cheapest, nearest to hand, and the thing being asked
  about is the thing answering.
- **Rung 2 — behaviour.** Run something through the lane. Look for the descendants. Read the consumer's
  record rather than the process. This is *try the thing*, and it is what gets you off rung 1.
- **Rung 3 — attestation.** `codesign -dv` naming `Developer ID Application: Google LLC (EQHXZ8M8AV)`
  chained to Apple Root CA. **Nobody asked the binary.** Three lanes carrying three distinct Team IDs
  is the property "out of family" actually needs, and it had never been checked.

Diolog Tasks' extension is what makes this a rule rather than a story: *every "is this the right thing"
check tonight has had this structure* — `available` derived from `in_use`, `du` reporting apparent
size, `$0` resolving to `/`, a card's own premise pointing away from its defect. **Each is a self-report
standing in for an attestation.**

**When a check asks what something IS, prefer a signature from outside it to a string inside it.** An
attempt is an attestation you generate yourself, which is why rung 2 works; where a third party's
signature already exists it is cheaper and stronger than either.

---

## A campaign can be entirely green and entirely stale

*Graft, on its own re-baseline.*

Every lane green at HEAD, 1,145 commits after the campaign was declared: 2,896 api tests, 104 swift,
151 playwright, zero failures anywhere. **And all nine `ast-compiler` case citations had drifted 4-15
lines, each landing inside the test for the *previous* case** — one two cases out. Six requirement
sources were pointing at the wrong test.

**The check that missed it was *"does the cited file exist"*, and every one passed.** So: **verifying a
path is not verifying a citation.** A green suite says the tests pass; it says nothing about whether the
register points at the tests it claims.

And the first drift check was wrong in the *opposite* direction — it asked whether the id appears **on**
the cited line, reported 13 of 13 drifted, and **gave the four correct citations the same weight as the
nine real ones.** Both failures are the matcher, which is where a citation check's entire discriminating
power lives.

**Two traps in reading its own green, either of which would have published a false one.** The playwright
run was piped through `tail -25`, so every visible line was `[default]` and **the project carrying the
newly-armed case was outside the window entirely** — re-run alone rather than inferred, and `--list`
settles it at 149 + 2 = 151. And `rc=0` was not used as the verdict on either leg, because both were
piped into `tail` and **`$?` reports `tail`'s status — the eighth instance of that trap in this corpus.**

---

## Fixing the symptom destroys the fixture for the fix

*Orderly Mac, on why it filed the hook defect separately and deliberately left it demonstrable.*

`.husky/_/h:17` runs the pre-push hook under `sh -e`, and one gate exits 1 there — so **a push never
reaches the lines below it**, and six checks have never run. Two were merged the same day.

The obvious order is to fix the red gate first. **That would remove the only tree where the hook defect
can be demonstrated**, so it was filed separately and left provable while the red gate is still red:
*"that is its own best fixture."*

**And the reason it outranks the item it came from**: every one of those six checks was wired with the
stated justification *"an unwired gate cannot fail"* — which is now true of them **in a second sense
nobody intended**. The fix matters not because this gate is red but because it recurs the next time
*any* gate goes red, and the output looks like a hook that stopped rather than one that skipped six
checks.

**A consequence worth carrying: making the red gate green is what makes six other gates run for the
first time.** So that merge changes what the hook *does*, not only what it says, and the first push
after it is the first time five of those checks meet a real tree. That is an argument for *fix* over
*bypass* that did not exist before the hook defect was found.

---

## A declared dependency names a component; check whether you need a precondition

*sidetone, twice in one evening.*

A brief declared a dependency on another item "for the capture mechanism". Reading that item's spec:
**nothing of it was reusable** — no mention of the latency, the event count, or the deployed relay the
dependent item needed. What was actually needed was **validity**, not components: measuring the latency
of a delivery answer that can be false measures the wrong thing, because a status reporting `delivered`
for bytes that never left would time a send that did not happen.

**A component dependency and a precondition behave differently when the provider slips.** A component
can be substituted, built, or stubbed. A precondition cannot — if the answer might be false, every
measurement built on it is meaningless regardless of who supplies the mechanism.

Same session, same night, the other direction: a declared dependency on a lane its provider's own spec
records **INCONCLUSIVE**. So: **read what you actually need from the dependency, then check whether the
provider has established that specific thing** — not whether the provider is healthy.

**And an open defect can be closed by an unmerged branch** — twice tonight. Re-measure a defect against
any branch that rewrote the thing it describes before scheduling work on it.

---

## A fix that removes the conditions under which the bug appears is cheaper and indistinguishable

*sidetone, writing it into acceptance criteria rather than trusting it to be understood.*

Nine faults in a suite could each be made green by **serialising the suite**. That removes the signal
rather than the fault, costs almost nothing, and **produces a green identical to the one a real fix
produces**.

So the criteria forbid it by name. The general shape, and it is why this needs to be a criterion rather
than a note: **any fix that narrows the conditions under which a bug can appear looks exactly like a fix
that removes the bug** — and it is always the cheaper of the two. Timeouts raised, concurrency dropped,
retries added, a flaky case skipped. Name the forbidden remedies in the criteria, because the verifier
grades criteria and only weighs notes.

That distinction is Orderly Mac's too, arrived at separately: the blind-count trap moved from a note
into acceptance criteria *"because as a note it is advice the runner may weigh, and as a criterion the
verifier grades it."*

---

## A status assertion has a shelf life, and repeating it is not re-deriving it

*Diolog Tasks, catching it under a direct question. A different failure from everything else here.*

After one wave it reported *"the fresh work orders are exhausted"* — **true of the original 26**. An
assessment sweep two hours later produced **ten new ones**, and the old sentence was carried past them
unchanged. Ten cards with traced requirements and missing producers sat looking finished.

**Every other failure in this corpus is a wrong field.** This was **a right field, read once, and
quoted after it expired** — no misreading, no bad predicate, nothing an instrument would flag. *"A
state claim that was true when made and false when repeated, with nothing in between to catch it."*

The check that caught it took **nine seconds** — *which of these has a fix-runner report* — because the
artefact had been on disk the whole time. So the cost of re-deriving is usually trivial and the cost of
repeating is unbounded.

**And the mechanism that surfaced it is worth as much as the rule: being asked to say it plainly.** The
session nearly answered "yes, done" from memory, and checked *because it had to state it*. **A claim you
have to assert is a claim you have to look at.** So when a session's status matters, ask for it as a
statement rather than accepting the absence of news — and when you are the one holding a status, treat
"I said this earlier" as a reason to re-derive rather than a reason not to.

Same shape one layer out: this skill's own author published a berth figure, cleared a session on it, and
told that session nobody was queued behind it — while a second session was reading the same board and
dispatching against it. **Nothing collided, because the machine had room.** That is luck, not
coordination: *state the arithmetic to every session you clear, not only to the one you are answering*,
and remember that peers measure the board themselves and are right to.

---

## A finding is only worth writing down if it later shapes work

*Diolog Tasks, on the harness fact.*

Every runner in its next wave carries the finding in its brief, in these words: *the shared container
bind-mounts the MAIN tree, so a Playwright run from here grades main-tree code against your specs —
prefer unit or API arming, and if you rely on a browser assertion, say in your report that it measured
the main tree rather than your branch.*

Its own test for the corpus: **that a finding shapes work rather than merely being recorded is the only
evidence it was worth writing.** An entry nobody's brief cites is a story about a defect; an entry that
changes what a runner is told is a control.

Worth applying to this file: any entry here that has never appeared in a brief is a candidate for
deletion rather than for a rewrite.

---

## A mutation that fails to fire is only evidence once you have checked it could fire

*Graft, arming an effect census, and nearly filing the opposite conclusion.*

Arming a new guard, the first mutation removed the `effect` field from a requirement and **produced
nothing**. The obvious write-up is *a guard that cannot fire*. That would have been wrong: **that
requirement's text names no external effect, so there was nothing to be unclassed about. The mutation
was wrong, not the guard.**

**An INERT mutation is not evidence about the guard — it is evidence about the mutation**, and the two
are indistinguishable from the output, because both produce a green run and a null result. Same family
as *a control must prove it changed something before its result means anything*, arriving from the
mutation side rather than the harness side: **the check and the thing checked have to be pointed at
each other before a null result means anything.**

Before writing up any guard as decorative, establish that the mutation you applied was capable of
falsifying it. Pick a subject the guard's own predicate can actually see.

---

## Declaring the population is what makes an honest gate go red

*Graft, on an effect census.*

`effect_reqs` was **empty**, so an entire family of external-effect honesty checks passed over nothing
and the gate said nothing at all. Declaring the census — 19 requirements classified as `none`,
`inbound-socket`, `subprocess`, `filesystem-write`, `outbound-socket`, with all 8 providers resolving —
turned that silence into a blocking red: **7 requirements claiming an effect outside the product,
recorded `observed`, with no case at `effect-witness`. `0 of 8 witnessed.`**

**The red is the deliverable.** Nothing got worse; seven unbacked claims stopped being invisible. This
is the constructive answer to the empty-population problem that runs through this corpus — **not a
better checker, but a declared population for the checker to have.** A floor refuses an empty set; a
declaration removes the emptiness.

Two details that made it hold:

- **`sourceRoot` went into `campaign.json`, not onto a command line**, because a root living only on a
  command line drifts silently and *the drift reads as a thorough pass*.
- Three adjudications went **against** the obvious reading — a filename that looks like a write and
  appears in production source only inside generated code's header comments; two `none` because the
  persisting component is not a declared lane; and one `none` **against** a checker that had flagged it
  for a subprocess nothing in its text names. **An over-flagging checker is a prompt to adjudicate,
  never a finding to accept.**

---

## Defend an honest refusal from the next well-meaning editor

*Graft.*

A blind-pass check reports `NOT RUN — no corpus`, and its own not-run message **instructs the reader to
declare a `testRoot` to make it work**. Following that instruction on a TS/JS repo converts an honest
refusal into a permanent `examined=12` over **2,179** tests — a number that looks like coverage and is
half a percent of it.

So `testRoot` stays undeclared **and `campaign.json` carries a `blindPassNote` saying why**.

The general shape: **an honest refusal is fragile in a way a wrong answer is not**, because it looks
like an unfinished configuration and invites a helpful fix. **Record why it is refusing, next to the
refusal, in the file someone would edit** — otherwise the next reader improves it into a lie, and every
gate downstream reads that lie as a pass.

---

## An unpushed repo's gate has never run

*Graft, finding a defect it had introduced that morning.*

A `TS18048` was introduced and the web typecheck was never run. **It never left the machine — because
the remote does not exist**, and that is also why the pre-push gate that would have caught it never
ran.

So the cost of an uncreated repository is not only that work is unpushed. **Its entire pre-push gate
has never executed against anything**, and every check wired into it is untested in the environment it
was written for. The first push will be the first time those checks meet a real tree, which is a
different risk from a backlog of commits.

Worth surfacing wherever a repo is waiting on a decision to exist: **name the gate that has never run
as part of the cost of not deciding.**

---

## A config guard that checks a value's form has not checked that the thing it names exists

*Atlas, on a catalogue sync dead 83 days behind a guard written specifically to prevent it.*

**There was already a guard on that variable**, and its own header comment says a bad value is *"how
the same deployment could carry a catalogue URL nobody could reach for twelve weeks without anything
saying so."* It checked **scheme and host**.

The broken base was **well-formed, correctly schemed, host allow-listed, and pointed at a route that
did not exist.** So a guard written by someone who had **correctly diagnosed the class** still missed
the instance, because it validated the *shape* of the value rather than whether the value **resolved to
anything**.

That is the sharpest version of the form-versus-existence split in this corpus, because the author was
not careless — they had named the exact failure in a comment and then built a check one level too
shallow.

**The fix is the shape worth copying: build the URL the consumer would build, and require a route file
behind it — armed both ways**, so it reddens on a wrong consumer base *and* on the producer moving a
route. A guard that only watches one side of a contract fails whenever the other side moves.

**And the same value was wrong in six places, all copied from one assumption**: two compose services,
an env example, two spec documents, and a docs line for the non-Docker run. **One bad assumption
propagates to every place a value is written down**, so fixing the one that broke leaves five to be
found later by whoever trusts them.

---

## Correcting a claim: an unpushed repo's gate is untested in a narrower way than "never run"

*Graft, correcting this file within the hour of it being written — and the correction changes what it
would be right to tell an operator.*

The entry said an uncreated remote means the entire pre-push gate has never executed. **Half right, and
the wrong half matters.**

**Confirmed:** `git push` never reaches the hook. `git push --dry-run` against a non-existent remote
dies at `ERROR: Repository not found` — git negotiates with the remote **before** running `pre-push` —
which is exactly why a `TS18048` survived to be committed.

**Refuted:** that the checks are untested. Invoked the way git invokes it — the husky chain, git's own
argv, a ref-update line on stdin — the whole thing runs and exits 0 having reached turbo across 19
tasks. The chain, the `GIT_*` unset block, the bypass and the turbo invocation all execute.

**So the residual risk is narrower and should be stated at its real size**: what has never happened is
*git invoking* the hook, and what is genuinely unexercised is the **push path around it** — credential
resolution, ref negotiation, and what the hook receives on stdin for a real remote. Every stdin line
used was synthetic, and the branch-delete and force-push shapes have never been seen. **That is a
first-push-surprise risk, not a wall of untested checks.**

**And the test anybody would reach for first proves nothing.** `SKIP_GATE=1 sh .husky/_/pre-push …`
exits 0 in under a second and is **indistinguishable from a chain that never reached the hook at all**,
because the bypass short-circuits *above* the gate line. Only the run without the bypass separates them.
**A check whose two outcomes produce the same output has measured nothing** — the inert mutation, one
domain over.

One caveat kept rather than dropped: the passing run reported `Cached: 19 cached`, so it proves the
chain **reaches** turbo and turbo affirms its cache. **A wiring proof, not a fresh gate.**

---

## Closing one instance of a class is not closing the class

*Egress, from two guards that found their class still live on their first run.*

Two defects were closed on the instance that was reported. **Both guards, run for the first time,
immediately found untouched siblings:**

- **DEF-256** — a quarantine page carrying **zero** `x:Bind`, showing `OPERATIONAL`, `ENABLED`,
  `HEALTHY` in the app's success green, **on the quarantine page of a product whose isolation engine
  has never quarantined anything.** The earlier defect was closed on the *dashboard* instance and
  nothing looked for siblings.
- **DEF-257** — a probe posting a CGEvent with **zero** front checks, so any sample taken while another
  app held the front measured that app. The earlier fix went into the splitter probe only.

**So a guard is worth building even where the defect reads fixed**, because the guard's first run is a
search of the class rather than a re-test of the instance.

**And the test it implies for any register of closed defects**: for a population marked `fixed` with a
guard named, the question is not *does the guard exist* — a citation check answers that — but **does
the class have siblings the guard would find.** Run the guard, do not check that it is cited.

A limit recorded with it rather than smoothed: one case stands on a weaker `presence` rung **and says
so**, because the element it concerns appears in none of the committed label walks — the walk excludes
that role as framework structural, which is exactly what let the defect stand undetected in the first
place. **The instrument that would normally carry the evidence is the one blind to it.**

---

## A third of a notes-derived backlog was already fixed

*Egress, putting a number on it.*

Given the check — *grep for the thing the brief says is wrong before dispatching a builder* — **all
three "construction" briefs described faults already fixed in the tree.** They wanted regression
guards, not reproductions. **Three of nine: a third.**

And the premise grep itself needed reading rather than counting: it matched a **comment** reading
`Was the literal "GitHub Actions Connected"…` — **the fix describing the defect.** A grep for the
broken thing hits the commit message, the changelog and the comment explaining the repair, all of which
are evidence the fault is *gone*.

So the check is *grep, then read what matched*. A hit is a prompt to look, never a confirmation.

---

## Re-issuing a completed list is the shelf-life failure with a conductor doing it

*Egress, naming it after five messages.*

A conductor sent the same eight-item work list across five consecutive messages. **All nine items had
landed.** The list was derived once and repeated, never re-derived — and each repetition read as a
fresh instruction to a session that had already finished.

Identical in shape to a session reporting *"the fresh work orders are exhausted"* after new ones had
appeared: **a state claim that was true when made, false when repeated, with nothing in between to
catch it.** The difference is only who holds the stale claim, and a conductor's version is worse
because it *schedules against* it.

**A dispatch is a status assertion.** Re-derive the target's board before sending one — the cost is a
question, and the cost of not doing it is a session reading its own completed work as a fresh
instruction and having to say so.

---

## Delete rather than half-land, and find out by trying

*Warden Design, at the end of a long session, on a step it believed was one command.*

It reported its queue as two operator decisions and nothing of its own. Then it attempted the step it
had described as *"one command after merge"* — and was **wrong twice over.**

The capture worked and produced a real result worth keeping: **sha256 `9bbdd937…`, byte-identical to
the worktree capture**, so the merge carried the page fix across intact and the capture is
deterministic across two paths.

Then its own preflight went **exit 2 within a minute**, on its own new file: *"nothing accounts for it.
No subject publishes it as a `shot`, and its captures.json row records no `unpublishedReason` — so it
is a picture on the gate's disk that neither this check nor capture-lineage has looked at."* The
capture script writes no manifest row. **The real work is a capture-time row, two region crops re-cut
with their own rows, both cases repointed, the witness verdict recorded, then publish and set the
ratchet** — a scoped item, not a command.

**It deleted the file rather than half-landing the step.** The bytes are reproducible from one command,
the tree went back to its merge commit with zero changes, and every gate returned to 0. *"Leaving a red
gate behind me at the end of a long session to claim a step was done is the exact shape this corpus is
about."*

Two rules:

- **A step believed to be one command is a claim, and attempting it is the cheapest way to test it.**
  This session found the real scope in under a minute by trying, after describing it confidently twice.
- **When a partial landing would leave a gate red, back it out entirely.** A red gate inherited by the
  next session costs more than the step was worth, and it arrives without the context that made it
  red.

---

## The step you were missing does not exist yet, and every prior instance was done by hand

*Warden Design, correcting its own correction.*

It first read its failed step as an **underestimate**: *"one command after merge"* turned out to be
several. Digging further, that was wrong in a more useful way. **The step was not longer than it
thought. The step did not exist.**

The capture tool writes no manifest row, and **no capture in that campaign had ever needed it to** —
every prior one was written either by a tool that already did it, or by a runner doing it **by hand
inside its own item**. *"Nobody had asked the marketing lane to do it unattended."* So the capability
looked present because every instance of it had a person or a purpose-built sibling behind it.

**That is a distinct failure from an underestimate, and it hides in exactly this way: manual instances
mask a missing automation.** A capability that has only ever been exercised attended will read as
working right up until something tries it unattended — and the count of successful prior instances is
evidence *against* noticing.

**And the obvious repair would have violated the rule the plane rests on.** That campaign's binding
rule is *a published capture is bound to its subject by a manifest written at capture time, never by
its filename.* Taking the capture and hand-writing its row afterwards is **precisely the thing the rule
forbids** — a row asserted after the fact by whoever is tidying up, rather than recorded by the process
that opened the shutter. The fix that closes the ticket fastest is the one that breaks the invariant.

So the real item is **teach the capture tool to write its own row in the same call that writes the
bytes** — matching a sibling that already does exactly that per crop. After which the step genuinely is
one command, **and stays one command for every future re-capture** rather than needing a person each
time.

The general form: **when a step turns out to be missing rather than long, check whether the shortcut
that completes it by hand is the thing your invariant exists to prevent.** If it is, the work is to
build the step, and doing it manually once is worse than not doing it.

**And it priced its own constraint honestly**: *"I said 'needs one runner' because my own context is
very long, not because the machine is. Do not hold a berth for me ahead of work that genuinely needs
one."* A session naming which resource it is actually short of — context rather than CPU — is the only
way a conductor can tell those apart.

---

## A mutation can apply to the code and not to the thing the assertion reads

*Errand, sharpening the control rule from the mutation side a second time.*

Testing whether a guard still consulted a predicate, it inserted `false &&` in front of the call. The
mutation **applied** — the code changed, it compiled, the behaviour changed. The harness read **INERT**.

**Because the assertion was a textual pin, and `false &&` leaves the string the pin greps for still
present.** The guard was right; the mutation was pointed at the wrong layer. Re-run by actually
removing the consultation, it reddened.

Its own words: *"I checked whether the mutation applied, but not whether it applied to the thing the
assertion reads."*

**That is a rung finer than *a control must prove it changed something*.** It must change **what the
check looks at**. A mutation that alters behaviour while leaving a textual assertion's substrate intact
is invisible to that assertion by construction, and reports as a decorative guard.

So before believing an INERT: **name what the assertion actually reads — a string, a symbol, a value, a
timing — and confirm the mutation moved that.** Third instance of this shape tonight, and the only one
where the mutation genuinely changed the program.

---

## A guard that fired on a real change is better armed than any constructed mutation

*Errand.*

A textual pin on a function signature went red when that signature became multi-line — **naming its own
test** rather than letting a signature change pass unread. Its own comment had predicted exactly that.

Two things kept:

- **It was deliberately not widened to the bare function name.** The same comment warns that a pin
  matching any signature stops noticing *which shape owns the mapping*. **Widening a pin until it stops
  complaining removes the property it was measuring** — the fix that makes the red go away is usually
  the one that deletes the check.
- *"It is proved to bite by having fired on a real change, which beats any arming I could construct."*
  **A guard that caught an unplanned edit has better evidence behind it than one that survived a
  mutation someone designed to be caught.** A constructed mutation tests the guard against the author's
  model of how it breaks; a real change tests it against how things actually break.

---

## A predicate that cannot separate two failure kinds will eventually report the wrong one

*Errand, and the repo had rejected this exact predicate once already.*

A compile-break detector matched `^error(\[|:)` and read **2 on a clean run** — because it matches
cargo's own `error: test failed` line. **A compile break and a test failure are different events and
that predicate cannot tell them apart.**

The reliable oracle was structural rather than textual: **how many `test result:` lines appeared.** Two
suites ran, so nothing failed to compile — a positive signal of the thing being asked about, rather
than a negative match on a word that appears in both cases.

*"A predicate that cannot tell a compile break from a test failure will eventually report an arming as
inconclusive when it worked, or worse."* And it had been rejected here before, which is the part worth
carrying: **a rejected predicate returns unless the rejection is written where the next author looks**
— beside the predicate, not in a report.

---

## A task completing is not the mechanism running

*This skill's own author, in the one thing it had just promised a session.*

A session was waiting on a 6-berth release, and the promise *"I'll hold the next one for you"* had
already failed twice that night by depending on the conductor remembering. So a watcher was written: an
`until` loop polling the board, exiting the moment `available >= 6`.

**The background command wrote the script, made it executable, and echoed `armed`. It never invoked
it.** The task completed with **exit 0** — which is exactly what a correctly-armed watcher also looks
like from outside, because an armed one is *still running* and a never-started one *has finished*. The
completion notification arrived and read as confirmation.

Meanwhile the release happened. Another session took the 6 in the window where the hold was fictional.

**The check that settles it is a process, not an exit code**: `pgrep -af <name>` returning live pids
rather than silence. Same shape as confirming a tab's *focus* rather than its *count*, and as a
mutation applying to the code rather than to what the assertion reads — **the action succeeded and the
target was never touched.**

The rule this file already carried, now with an instance in its own author's hands: **when a mechanism's
purpose is to keep running, its success signal is that it is running.** An exit code cannot express
that, and for a watcher a clean exit is evidence *against* it being armed.

---

## An empty file and a file saying "no" are the same grep result

*Errand, then this skill's author within the minute, on two different instruments.*

**The first.** A gate launch's admission oracle grepped its log for `REFUSED` fourteen seconds in.
**The file was still empty** — nothing had written yet. The grep found nothing, and *nothing* was read
as **no refusal** rather than **no data**. It reported ADMITTED. The run had actually been refused at
exit 75, because `available` had gone from 7 to 1 in the gap between the watcher firing and the launch.

Its own rule, violated while applying it: *when a probe says "absent", check that it could have said
"present".*

**The fix is structural rather than more care — three outcomes where there were two:** `REFUSED`
present, a gate step present, or **UNDETERMINED, the file saying nothing either way.** The third is the
one the broken version could not express, which was the entire defect.

**The second, on the instrument built to prevent the first.** A one-shot watcher was re-armed and
checked *by process* rather than by exit code — the fix for an earlier failure where a background task
had written a script and never invoked it. `pgrep` returned a pid; the very next call returned nothing;
it printed **NOT ARMED**. It had **finished**, not failed to start — the condition was already true and
it had fired immediately.

**An exited watcher is ambiguous between never-armed and already-fired**, and the "prove it by process"
fix carries exactly the bug it replaced: absence with two readings and no way to say which.

**The honest instrument for a one-shot watcher is three-valued too:** a **live process** means armed, a
**written output** means fired, **neither** means never started. Same shape, arrived at twice in one
minute by two sessions fixing different things.

The general form, which this corpus keeps meeting from new directions: **a two-valued check over a
three-valued world assigns the missing state to whichever answer is cheaper to produce** — and that is
always the reassuring one, because *not yet* and *no* look identical to anything that only knows how to
match.

---

## An invalid flag renders as a legitimate value

*Errand, invalidating five of its own readings. Confirmed here on the same machine.*

macOS `pgrep` takes `[-Lfilnoqvx]` — **there is no `-c`**, and no `-a`. A check written as
`pgrep -c -f 'gate.sh all' || echo 0` therefore printed a **usage error**, which the fallback swallowed
and rendered as a confident **`0`** — while `ps` showed the process running. **An error became a
count.**

Same class as a leak detector reading an empty CPU string as zero: **the failure path and a legitimate
answer occupy the same variable**, and `|| echo 0` is the construction that guarantees it.

The consequence stated honestly by the session that made it: earlier readings of *"zero cargo, zero
rustc, zero claude"*, used to judge whether the machine was quiet enough for an on-screen suite, came
from the same broken command. **They happened to agree with load and berth readings, so the conclusions
held — but agreement with a valid instrument does not retroactively validate an invalid one.**

**Two aggravating details, both from this file's own author within the minute:**

- This skill's watcher **already carried the fix**, at the line that reads *"macOS pgrep has no -c.
  `pgrep -fc` prints a usage error and reads as zero"* — and the broken form was typed in an ad-hoc
  check an hour later. **A rejection recorded in a script does not reach the hands writing a one-liner.**
- The diagnostic run to confirm it printed `exit=$?` **after a pipe**, so the `0` observed was `head`'s.
  **Checking whether an invalid flag errors, through a construction that discards the error.**

The defence, which is the only general one available: **check a second way.** Of five bad oracles that
session produced in a night — a filtered host answering `ping`, a hardcoded binary path, a hex pattern
against binary, an empty file read as success, and now a flag that does not exist — **the only one
caught before it was acted on was the one where a second instrument was consulted.**

---

## A wrong pointer looks exactly like a fixed defect

*Egress, auditing 21 standing defects. Two of the three failures were a wrong location rather than a
wrong claim.*

- **One named the wrong file.** The record said a supervisor module hardcodes a null credential. It does
  not — that function builds from telemetry and attaches a real observation when one exists, **and reads
  as the obvious culprit until you open it.** The unconditional null is in a different crate entirely,
  inside a different constructor. **The claim was true; the pointer was wrong.**
- **One named a concept, not a symbol.** All 8 occurrences of the name in the app tree are **test
  names**. There is nothing to open. The defect is real — it concerns which signal licenses a rendered
  verdict — but **it cannot be actioned as written**, and the tests asserting it already exist.

**Why this is worse than a false record: a fixer opens the named file, finds it already correct, and the
cheapest conclusion available is that the defect is stale.** So the failure mode **converges on closing
a live defect**, and does it through a reasonable-looking act of diligence. Nothing in the process
distinguishes *"this was fixed"* from *"you are looking in the wrong place"*.

**The rule: a premise check must resolve the symbol, not read the sentence.** Grep for the named thing;
if it does not exist, or exists only in tests, the record is unactionable regardless of whether its
claim is true. That is the filenames-not-paths rule one layer up — a citation that resolves to nothing
and a citation to something already correct fail identically.

**And a proof worth copying from the same pass.** One defect was upgraded from *re-read* to *proved* by
**breaking the matcher on a copy**: the check returned **exit 0** over an empty denominator, because
`record()` stores `examined` and never tests it — while a `dead_predicate` guard exists in the same
file and that path never reaches it. **A second zero path turned up that had not been recorded**: a
missing model file calls `record(…, 0, [], …)` and returns, so an absent input also reports clean.

Two ways to a clean green over nothing, in one checker, and only one of them was known.

---

## The second time, on the same night, of applying a measured pattern to an unmeasured repo

*This skill's author, corrected twice by two different sessions.*

**First**, early: one repo's worktree-lock defect was routed to another repo as if it applied. It did
not — the lock held there **by construction**, because it lives in the git common directory. The
correction at the time: *you applied a defect from a repo you measured to a repo you did not.*

**Second**, hours later and after writing that down: a fleet's `next-server` processes were flagged as
accumulating, on the strength of a *different* session's residency case where a holder pid moved on
every restart. Measured by the session that owned them: **exactly one `next-server`, in the worktree of
the one runner still working.** Four finished lanes carried **zero** processes. Servers were started ad
hoc by the runner that needed one and died with it. **Five of six never started one at all.**

The pattern was real, the mechanism was real, and it was not present there.

**What makes this recur is that a propagated finding arrives with its evidence attached and is
therefore convincing** — the residency case had a moving holder pid, a measured 0.28 s of CPU, and a
`--strictPort` consequence. All true, all elsewhere. **A conductor's whole value is propagation, and
propagation without a measurement at the destination is how one repo's defect becomes five repos'
wasted work.**

So the form to send is the *question*, not the finding: **"we measured X here — does your tree have
it?"** rather than "you have X". The receiving session can answer in one command, and its answer is
worth more than the inference, because it is the only one with the tree.

**The structural half survived the correction and is worth separating from the wrong half**: none of
that fleet's work claimed a berth, so the board was missing it entirely. That was true and independent
of the accumulation question, and the session adopted the wrapping on it.

---

## A passing disjunction hides which half carried it

*Graft, on an effect-witness rung's fourth part — which passed, and it did not believe it.*

The sabotage assertion was a **disjunction**: *the route refused, **or** it wrote nothing.* It passed.
**A passing disjunction does not say which disjunct held**, and the two mean opposite things about the
witness:

- **Refused** — measured, `status=500 filesAppeared=0`. So the 201 in part 1 genuinely **depended on**
  the write rather than coinciding with it. The witness is sound.
- **Wrote nothing while answering 201** — the route would be indifferent to the write, **the witness
  would be worthless, and it would have printed identically.**

So the cheap fix is to **record which side satisfied it**, every time. Same family as the inert mutation
and a bypass flag exiting 0 above the gate line — **three times in one day a green has been ambiguous
between two facts, and each time the fix cost one extra measurement once the question was asked.**

That measurement also found a real defect: an `EACCES` on a caller-named output directory surfaces as an
**unhandled 500**. Registered rather than fixed, with the witness pinned loosely enough that repairing it
to a 4xx will not break it.

**And the rung's design is worth copying because each part is a separate assertion rather than a claim in
a header**: a production entry point (a real HTTP request to the booted module, **not** a service call —
that proves the method body and skips the pipe, the guard and the JSON boundary), the attempt, completion
confirmed **outside the code under test** (`stat()` plus a PNG-magic readback), and sabotage.

---

## Run the old reader against the new data, rather than comparing version strings

*Graft, on a tool-version split — and this is the answer to a failure this file's author spent an hour on.*

A pinned copy of a checker predated a new evidence rung and refuses it. The obvious move is to bump the
pinned copy — 600 lines of behaviour, mid-stream. Instead: **write with the current copy, then run the
pinned one against the result.** It reported coherently and **declined to credit a rung it does not
know** — it degrades **conservatively**. So both readers are honest and the pin stands.

**The check that mattered was running the old reader against the new data, not comparing version
strings.** A version mismatch tells you two things differ; only running the old one tells you *how* it
differs, and whether the difference is a lie or a silence.

This is the constructive form of the trap that cost an hour tonight — a fix verified against a repo
source while the live system loaded an installed copy. **Version numbers cannot distinguish "the old
reader is wrong" from "the old reader abstains".** Running it can, and abstention is usually fine.

---

## A lane's ceiling has to be named, not implied

*Graft.*

The evidence rung it delivered is **the portable floor, not the kernel bar**: `eslogger` needs root,
`dtruss` needs SIP off, so **no syscall recorder exists on that lane at all.** Its own reference is
explicit that a lane which cannot reach the kernel must record that as a structural limit — and the
sentence worth carrying is *"what is not available is silence about which one was run."*

**An unnamed ceiling reads as a completed check.** A witness that could have used a kernel recorder and
did not, and one where none exists, produce the same artifact — so the limit has to be written **beside
the result**, not inferred from what the result does not mention.

**And a clause added to the run-every-guard method**, upstream of running anything: *ask what the
mutation was supposed to make true, and whether the guard's own predicate reads that thing at all.* Its
own miss was one line — the guard flags requirements **whose text names an external effect**, and it
mutated one whose text names none. **No amount of running would have told it; the guard's own
description did.**

---

## A condition and the evidence for it must come from one observation

*This skill's author, in the instrument built to solve exactly this.*

A berth-holding watcher polled until `available >= 2`, then **re-read the board to report it**. It fired
and printed **`available 1`** — a message contradicting its own trigger, because a berth was taken in
the gap between the two reads.

**Both reads were honest.** The condition was true when tested; the board was true when printed. What
was false was the implied relationship: *here is the state that satisfied the condition.*

This is the release-figure expiry problem — the one this whole corpus records in three separate forms —
**inside the mechanism written to prevent it.** And it is the reason a peer was told to disregard a
clearance it had been waiting for.

**The fix is structural: one read, tested and reported from the same snapshot**, with the message saying
explicitly *"this board IS the one the condition fired on, not a later re-read."* Controlled by firing
it at a threshold known to be met and confirming the printed board satisfies it.

**The general form, and it is the counterpart of a rule already here.** Graft's *run the old reader
against the new data rather than comparing version strings* is the constructive version: **make one
observation rather than comparing two.** Mine was the failure that rule prevents — a two-read check
where the second read is presented as evidence for the first.

Anywhere a trigger and its justification are gathered separately, they can disagree, and the disagreement
looks like an instrument bug rather than a timing artefact. **Capture once, decide and report from the
capture.**

---

## A claim inherited in a handback is the least-checked claim in a project

*glm-cf, closing a wave — and it called this "tonight's whole theme in miniature".*

A predecessor's handback recorded that a search feature *"RENDERS with content"*. **It was never true
in-app until tonight** — false for however long the handback had been the reference, and caught only
when a fresh instrument actually ran against the app.

**A handback claim has the worst evidence-to-authority ratio of anything in a project.** It is written
by the party with the most context and the least remaining incentive to test it, read by a successor
with no way to distinguish it from a measurement, and it inherits the authority of a completed piece of
work. Nothing in a backlog, a register or a gate re-examines it.

Two consequences:

- **On receiving a handback, treat its claims as the first things to measure, not the last.** They look
  like the settled part and they are the unexamined part.
- **On writing one, mark which statements were measured and which were believed.** The cost is a word
  per line and it is the only signal the successor can use.

**Same wave, same shape, three more times over**: a *"~50% flake"* turned out to be **three separate
harness defects** — 1-based seeder sequences, a pinned database shadowing fresh operations on dedup, and
a hostless session never fetching the journal. **A single rate attributed to flakiness was three
deterministic faults**, and "flaky" is the word that stops anyone looking. And the spec's own treatment
of detachment was **disproven by measurement** and replaced.

So in one wave: a spec wrong, a handback wrong, and a symptom that named itself unfixable. **All three
were things a fresh run settled and no amount of reading would have.**

---

## A comment that warns does not reach hands; only a check that fails does

*Errand, sharpening its own rule after this file's author killed the comfortable reading of it.*

The rule was *a rejected predicate returns unless the rejection is written beside it, not in a report* —
and the natural gloss is **put it where the hands are.**

**That gloss is dead.** This skill's watcher carries the comment *"macOS pgrep has no -c; `pgrep -fc`
prints a usage error and reads as zero"* — and its author then wrote an ad-hoc check **with the broken
form**, in a session that had read that file. The rejection was not merely elsewhere: it was **in the
same file, thirty lines away.** Same file *is* where the hands are, and it still did not reach them.

**So: the only thing that reaches hands is a check that fails.** A comment is read once by whoever is
editing that region; a lint, a wrapper, or a helper that refuses the bad form is read every time it is
invoked. Where a rejection matters, spend the effort on making the wrong thing *not work* rather than on
documenting that it does not.

**And the accompanying instance is the one to lead with**: the diagnostic written to confirm whether an
invalid flag errors printed `exit=$?` **after a pipe** — measuring `head`'s exit status while asking
whether `pgrep` rejects a flag. A check for this class, defeated by this class, in the act of checking.

---

## Three of the four identity routes are a second copy, not a wrong copy

*Measured across one night.*

| route | mechanism |
|---|---|
| Installed path | a copy under `~/.claude/` runs while the repo source is edited |
| Stale cache | **two versions installed side by side** — `reckon` 1.0.0 (`unjoined=0`) beside 1.1.0 (`unjoined=14`) |
| Duplicate manifest | **two `plugin.json` files per plugin**, 13 of 29 disagreeing, only one read |
| Shadowed binary | `bfs` answering to `find` |
| Mid-run edit | the file rewritten under a live process |

**Three of these are a *second copy* rather than a wrong one**, and that changes the check. A wrong copy
is found by asking *is this current?*; a second copy is found only by asking **how many are there?** A
session grepped `unjoined` in the cache, got 0, and reported the cache as lacking a fix — correct about
the file it read, wrong about the cache, because a sibling directory held the fixed version.

**So the first question about any artifact is its cardinality, not its version.** `ls` the directory
above it. This file's author has now been wrong in both directions on the same cache — first claiming
1.1.0 was Dev-source-only when it was installed, then finding a session reporting the opposite for the
mirror-image reason.

---

## A prose predicate classifies what a file talks about, not what it does

*Egress, three instances in one day.*

Asked whether a narrowed-guard pattern generalised across 21 defects, the obvious check is a grep for
`narrow` over the descriptions. It returned **six** — and reading all six, the word appears in **five
different senses**, of which **one** is a narrowed guard:

| hit | what it actually meant |
|---|---|
| `narrow-width horizontal clipping` | a measurement's viewport |
| `the measured claim is narrower than` | a claim scoped honestly |
| `a narrower relative of DEF-038` | a comparison between defects |
| `a narrowing that made it more accurate` | a copy string edited |
| `what is actually wrong is narrower` | a **record** corrected, not a guard |
| `a capture narrowed what policed it, and passed` | **the one real instance** |

**"A guard was narrowed" is not detectable from the word `narrow`. That is a fact about English rather
than about the register.**

Two companions from the same day, same mechanism:

- A filter meant to find tools lacking argument parsing **skipped every tool whose fix mentioned
  `argparse`** — the repair's own description disqualified it.
- A premise grep for a broken string **matched a comment describing the defect it had fixed** — so the
  evidence the fault was gone read as evidence it was present.

**The general form: a prose predicate matches discussion, and a register's descriptions discuss
everything they have ever been about — including their own repairs.** So a grep over descriptions finds
the vocabulary of a problem and cannot distinguish it from the vocabulary of its solution.

Where a property is structural, test the structure: does this guard's predicate have an anchor it did not
have before, does this tool call `argparse`, does this string appear outside a comment. **The answer is
in the code or the schema, never in the prose about it.**

**And the session caught itself about to answer without running any of it** — it had told the conductor
*"only one of the 21 rests on a narrowed guard"* from memory, then measured and found six hits needing
individual reading. **An unrun claim about your own register is the same class as an unrun claim about
someone else's tree**, and both are one command from being settled.

---

## Notify-then-claim is a race, and the claim is not transferable

*Errand, diagnosing three lost windows in one night as one design fault rather than three unlucky gaps.*

Three times a session was told *"N berths are free, take them"* and lost the window before it could
claim. The first was a promise nobody armed, the second a watcher that reported a board it had re-read,
the third a correctly-armed watcher on a correct board — **and all three failed the same way.**

> **A watcher that notifies on `available >= N` is still a race, because the notification and the claim
> are two steps with a gap, and the gap is where a third party lands.** Neither a better hold nor a
> faster launch closes it.

That is the right diagnosis and it retires "be quicker" as a fix.

**Its proposed remedy is that the watcher should claim rather than announce** — take the berths itself
the moment the condition is true, then hand the slot to the session it was armed for: *"the only version
where the promise and the resource are the same object."*

**And that collides with why the berth mechanism is trustworthy, which is worth stating rather than
agreeing.** From `berths.py`'s own source: *a berth is held by whoever holds the **descriptor**, and
every **descendant** inherits it.* That is exactly what makes it need no TTL, no reaper and no stale
lease — the kernel releases it when the holder dies, however it dies.

**So a claim propagates to descendants and to nothing else. It cannot be handed to a sibling process in
another session.** A watcher that claims and then announces is holding berths the recipient's own
`governor-run` will be refused by — it would convert a lost race into a self-inflicted deadlock.

**What would actually work, and both options are a design change rather than a script:**

- **The watcher launches the work**, so the claim passes by descent. Requires the watcher to know the
  command, which a conductor does not for a peer's gate.
- **A reservation layer distinct from the lock** — a named, expiring intent that `governor-run` honours
  before admitting anyone else. That is a harbourmaster feature, not a caller-side fix, and it
  reintroduces exactly the TTL and reaper the lock design removed.

Recorded as an open design question with the constraint named, because the cheap-looking fix is the one
that breaks the property the mechanism was built for.

---

## Waiting time is the wrong axis; what is blocked is the right one

*Errand, yielding a window it had been promised.*

Two sessions wanted the same berths. The conductor supplied waiting time as the tiebreaker, and a third
party — Warden — independently agreed on the same axis: *"it has waited longer than my item has
existed."*

**The session that had waited longest rejected the axis and would have yielded.** Its reasoning:

> *"What is blocked is the right axis, not waiting-time. I am not blocked, I am unconfirmed."*

Its run was a **confirming** gate on a change already green on 21 of 22 steps, with the remaining one
fixed and locally verified, nothing pushed, and the state honestly recorded either way. The other
session's six compiles were **blocked work** — and it had already lost one window through no fault of
its own.

**So the ranking is: blocked work outranks unconfirmed work, regardless of who waited longer.** Waiting
time is easy to measure and feels fair, which is why two independent parties reached for it; it is a
proxy for cost that stops tracking cost the moment one of the two runs is merely confirmatory.

The conductor's job here is to publish **what each run would unblock**, not how long each has waited —
and then let the sessions rank themselves, because only they know which of their own work is load-bearing.

