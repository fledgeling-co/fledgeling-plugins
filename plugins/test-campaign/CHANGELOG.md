# Changelog

All notable changes to the `test-campaign` plugin.

## 0.16.1 — 2026-09-01

Swift blind-pass candidates now use balanced function bodies. A following private
helper no longer contributes its writes to the preceding test; nested declarations
cannot supply their parent with readers. Comments and literal text are masked,
while executable ordinary/raw/multiline string interpolation remains visible.
Modifiers, attributes, generic signatures and default closures retain body boundaries.

The gate reports unsupported or malformed Swift files as NOT MEASURED, with a
file/reason and a separate denominator, including mixed corpora. Empty scans fail.
Regex and ambiguous slash operators remain outside the bounded lexer; ordinary
arithmetic division is supported. Named functions are candidates, not a test-runner
census: called-helper exclusions remain heuristic, while @Test and test* entries
are retained. This does not establish control flow, transitive effects or reader
independence. Other-language extraction and provider rules are unchanged.

The portable fixture group runs in the standing gate. An actual next-declaration
mutant fails the nested-body falsifier. Two stale control-diagnostic expectations
now name their respective missing-drive and driven-without-passing-effect errors;
an actual structural-actuation-credit mutant still fails. The historical pinned
baseline remains 111 passed / 2 failed, rather than being rewritten as green.

## 0.16.0 — 2026-08-28

**A board is a different starting question from a diff.** "Is this product
correct" selects by surface; "these 228 tasks say they are done, prove it"
selects by task, and the campaign had no entry point for the second. It has one
now, measured over 228 closed cards on one product across three weeks.

`references/task-bound-flows.md` carries the chain: discovering the flows a task
corpus needs, binding a task to a flow, extending a flow without breaking the
precondition that walks it, reading a mock for intent, and comparing the result.
The findings that changed how it is written:

- **Binding by route is not evidence.** One card bound to 67 flows, another to
  55. That says the card touches a page some flows visit — shared vocabulary, not
  a check. A binding is a card id in the title of ONE live case whose assertion
  fails when that card's producer breaks. A card id in a COMMENT over-reported by
  18 cards, because comments are invisible to the runner.
- **One contract entry failed eighteen specs.** An entry pointed at a region the
  pinned tenant could never render; the warm-up precondition waited its full 90s
  ceiling and Playwright skipped every dependent spec. All eighteen reported
  `passed=4 failed=1`, identical — and identical counts across independent specs
  mean one shared cause. Read the counts before the verdicts.
- **A written assertion can measure nothing.** One case asserted no sparkline
  painted a flat rule, passed, was armed against the exact defect, and passed
  again: it had matched 107 ICON paths and parsed arc parameters as coordinates,
  over a surface that rendered no sparkline at all. Only arming finds this.
- **An environmental fault contaminates every verdict.** 44 failures across one
  suite traced to a single endpoint 400ing on an exhausted model credential — 36
  of one spec's 52. Those specs were not broken, and a run in that state cannot
  say whether they are.
- **A tracked-file gate cannot see an untracked file.** Instruments enumerating
  via `git ls-files` are blind to a new spec until it is staged.

`scripts/geometry-gate.py` is new and portable by construction — pure image maths
over a pair of same-size images, no browser and no project layout. It decides a
visual difference on its bounding box and the fill density inside it rather than
a whole-frame ratio, because a real one-step spacing change is 558 pixels of
1,296,000: a ratio of 0.00043 that every threshold passes, in a 114x13 box at
density 0.377 that is unmistakable. `--stable` scores two renders and reports
`agrees` / `defect` / `unstable`, because a defect needs two renders that agree.
7 of 7 selftest rules fire without any files.

Also: a third capture verdict. A picture that cannot prove its subject is
`invalid-capture` — not a pass, not a failure. On its first run it caught a
capture of `/dashboard?settings=account` filed as `/settings`, which is real
redirect behaviour rather than a gate to relax.

**One manifest, not two.** test-campaign carried both `plugin.json` and
`.claude-plugin/plugin.json`. The second is the one that counts —
`site/scripts/build-catalogue.mjs` reads it and fails the build when it is
missing, and nothing reads the root copy — so the root copy is gone. Its only
extra key was `category`, which lives in marketplace.json where it is actually
consumed. Manifest and marketplace now agree at 0.16.0, checked across all 52
entries.

Worth knowing if you maintain another plugin here: 22 of the 26 plugins carrying
both files have drifted, and in every case the root copy is BEHIND the canonical
one. Not one is ahead, which is what marks the root file as a copy that stopped
being maintained rather than a second source.

And a third CI state, because the two that existed were both bad: wired, where
one environmental red trains everyone to ignore the build, or not run at all —
which is how an 867-step flow apparatus came to exist and execute nowhere. A
suite can now run and record without being able to fail the job, and earns the
blocking list by running clean.

## 0.14.0 — 2026-08-24

**Seven projects, one week, the same false finish.** Each was orchestrated to a
drained backlog and reported implemented, verified and tested. Asked directly
whether every feature worked, the honest answer in all seven was no: a compiler
suite standing for a desktop application, a mock peer standing for live Drive
sync, 2,375 passing Swift tests over an app whose buttons ran empty closures, an
in-tree slice retiring a brief whose stated intent was a system daemon.

None of those campaigns was lying, and that is the point. Every case really did
assert an outcome, really was armed, really was watched to fail. It asserted it
against a double. The registry had no field for the difference.

**`plane` is that field, and it is orthogonal to the oracle rung.** The rung says
what a case checked; the plane says what it checked it against — `in-tree`,
`hermetic`, `live-glass`, `live-external`. A requirement declares the planes its
intent spans, and `check` refuses to clear when a declared plane has no passing
case on it. `add` refuses a plane outside the closed list, and the census prints
on every run: `Planes: in-tree 12 · hermetic 4 · live-glass 6`, or NOT DECLARED
where nothing says what it was measured against.

Each of the seven sessions independently proposed roughly this fix and none of
them landed it, which is why it is a gate rather than a paragraph.

113 gate tests, four of them new: an in-tree pass does not satisfy a live-glass
requirement; reaching the declared plane clears it; the census prints; an
unrecognised plane is refused at `add`.

## 0.13.0 — 2026-08-24

**The history axis, built rather than described.** 0.12.0 added one sweep and a
reference file naming thirteen methods; that changed what the skill *said* and
not what it *ran*. This adds the sweeps and the gates.

Six new sweeps, each with its own mechanics, assertions and printed denominator:
**O** journey prefix, interruption and process death · **P** previous-build
differential · **Q** event order, adjacency and repetition · **R** mid-session
revocation, offline, time and pseudo-locale · **S** telemetry contract · **T**
resource slope and endurance · and **U** event races and schedule interleaving.

Four mechanical gates in `campaign.py`, on the ranks the research says may gate
rather than advise. `journey` is a registry entity (`JRN-*`) with its own
denominator, because no per-surface count can see a history. A **critical journey
uncut at any of the five durable boundaries** blocks — `request-issued`,
`server-committed`, `provider-effect`, `client-persisted`, `user-acknowledged`. A
**previous-build comparison with no `changeIntentManifest`** blocks. A journey no
case drives blocks, and a boundary name outside the closed list blocks. 109 gate
tests, eight of them new, each proved to fire and then proved to clear.

The numbers that decided each gate, and their limits. **RegDroid**: 121
adjacent-version pairs, 205 reports, 73 true and 132 false — a **64%
false-positive rate of which 93% were intended changes** — yielding 14 unique
functional bugs, ten previously unknown and all ten fixed. That is why P carries
three dispositions and the manifest is a gate. **The Android data-loss
benchmark**: 110 reproducible faults across 54 releases of 48 apps, 98 with an
automated oracle — prevalence and reproducibility, explicitly not a yield trial.
**TimeMachine**: 199 unique crashes against 140/121/48 for Sapienz, Stoat and
Monkey over 68 apps, and its client-only state restoration is why O keeps the
effect ledger outside the restored snapshot. **AjaxRacer**: 152 tests, 65 harmful
races across 12 of 20 pages, 7 false positives — the only addition whose measured
false-positive rate is low enough to block on directly. **NIST**: 14 tests cover
all three-event orderings of ten events against 10! exhaustive, and one
eight-step system went from ~7,000 permutations to a 19-case suite.

The model-oracle section is rewritten from the panel and corrects both CLI lanes.
The `~96%` figure is **GenA11y at 95.2% precision / 87.69% recall on semantic
accessibility**, against axe-core's 12.74% recall on the same corpus — 148 pages
deliberately seeded with known issues, so a conformance benchmark rather than a
live distribution. Precision is not a false-positive rate, and the class-
conditional rates are recorded `MISSING_DATA`. The architecture: model-assisted,
deterministically executed — the model selects journeys, generates input and
ranks diffs; the trace is replayed without it; a deterministic confirmation
precedes any release-blocking verdict.

`references/journeys.md` records where the four backends disagreed, unresolved:
pseudo-localisation at rank 1 or rank 6, race detection at 4 / 7 / gate-worthy,
and record-replay as useful or a maintenance sink. With 111 sources at 1% overlap
between members, disagreement is the stronger signal and it is kept rather than
averaged away.

Research provenance in `docs/deep-research/2026-08-24-panel-*.md`: four backends
at max tier, 111 sources over 38 independent domains. Gemini's 57 citations are
~45 opaque grounding redirects and its identifiable sourcing is nearer 12; the
OpenAI member was citation-checked at 42 dereferenced, 0 fabricated, 0 dead. The
`agy` lane refused to start on an unidentified binary.

## 0.12.0 — 2026-08-24

**A campaign cleared every gate over an application whose every control was
inert.** 32 of 32 cases passing and armed, 19 of 19 requirements cited, 8 of 8
surfaces covered, 8 of 8 external effects witnessed, `reckon` at 0 unmeasured and
0 unjoined, the repository gate 19 of 19. The owner opened the signed build and
found three defects in nine minutes: six sidebar destinations opening one
placeholder view, every button running an empty closure, and a folder picker that
set a banner and read nothing. Nothing in the campaign was false.
`references/inert-ui.md` records the measurement, why each of six instruments
passed, and the three shapes.

Three things a surface and a case may now declare, all optional, all reported as
NOT DECLARED rather than clean when absent: `controls` on a surface, `actuates` on
a case, `destinationOf` on a destination surface. `check` refuses to clear on a
surface whose declared controls no passing effect-rung case actuates, on a case
actuating a control its surface never declared, on two destinations of one shell
publishing one identical image — a declared share does not excuse it there — and
on a destination no case reaches. A case below `outcome` that names an actuation
does not move the census: driving a control and asserting the control is still
there has measured the click and not the effect.

Two denominators now print on every run, green or red, because the campaign this
came from was green and what mattered sat in a number nobody printed: a per-lane
row carrying that lane's cases, passes, effect-rung passes, armed count and
oracle mix, and the control census. A lane with no effect-rung pass is reported
and **not** blocked, and that is a measurement rather than a softening — the
native lane on that campaign did carry an effect-witness case, so a rule of the
form "every lane owes one effect rung" would have cleared it and the app would
still have shipped.

**The blind-mutation pass could not see an arrow-style test.** `pass_blind`
matched `fn|def|func|function` only, so `it('…', () => {` and
`test("…", async () =>` were invisible. Measured on two repositories: one
monorepo's API tests held 224 declaration-style blocks against 2,179 arrow-style
ones, so `blind=0` there was a statement about 9% of the corpus; a second held
4,741 arrow-style blocks and zero declarations, where the false clean was total.
The pass now reads both, prints the split (`blocks: declaration-style 224 ·
arrow-style it/test 2179`), and reports `NOT MEASURED` rather than `blind=0` when
it recognises no block in a corpus that has files in it.

`references/journeys.md` is new, and it is the first axis this skill has added
that is not a state. Two model families were asked independently what still
escapes the methodology and both ranked the same answer first: model the journey,
generate action sequences over it with sequence covering arrays, cut at every
durable boundary, and replay each sequence against the previous accepted build.
The file carries the journey state model and its four properties, the thirteen
ranked additions the two lanes converged on, and the measured ceiling on
model-based oracles with citations — OwlEye at 85/84 on its own corpus, Nighthawk
at 0.59 AP for localisation, MLLMs near random on WiserUI-Bench, axe-core at
57.38% by Deque's own count. Sweep N in `sweeps.md` is the runnable half. The two
panels and their prompt are in `docs/deep-research/`.

Sweep C gains the control census, the acknowledgement-only shape and a native
lane block, including the AX finding carried over from `acceptance-e2e`: 13
sidebar identifiers all resolved while the element carrying one of them was an
`AXStaticText` with an empty actions list, so `name of every action of e` must
contain `AXPress` for anything interactive. The promotion section gains two rules
from the same skill: a gate nothing invokes is documentation, and a promoted
sweep derives its subject list from the router or manifest rather than a
hand-list. `detector-defects.md` gains §15 and §16. 101 gate tests, 13 of them
new and each proved in both directions.

## 0.9.6 — 2026-08-22

**The provider census resolved on its own prose.** Providers are written
`<claim> — <what it does>`, and `provider_targets` offered *every word of the
description* to the symbol matcher. `has_symbol` accepts any token of three
characters or more that appears anywhere in production source, and English
source is full of English — so `the`, `file`, `that` and `there` all matched,
and a provider resolved on its adjectives rather than on its claim. Measured on
a real campaign the moment 0.9.5's census was first pointed at a source root:
**nine of nine providers reported resolved**, one of them via the symbol `the`,
and `totally/made/up/path.swift — the window server is another process` resolved
just as happily as a real file. The census 0.9.5 added to catch a dead predicate
had become one on its first run.

Only the claim before the em dash, en dash or ` - ` now supplies paths and
symbols. The description is prose and is read by people, not by the matcher.

**A provider naming a module directory could not resolve.** `SourceIndex`
indexed files only, so `crates/core/src/tui` — a legitimate way to name a module
— failed against a tree that plainly contains it, which would have pushed
authors to name an arbitrary file inside it instead. Directories are indexed
too.

Four tests, and the fixture is the point: the first version of them passed with
the fix reverted, because a one-line fixture file contains none of the English
the description uses, so the defect could not fire and the test measured
nothing. The fixture source now carries an ordinary comment, and the tests are
red without the fix and green with it. 84 → 88.

## 0.9.5 — 2026-08-22

Four checks that read a field without reading what the field pointed at, all four found by
running this plugin's own gates over a real campaign and reading the numbers rather than the
verdicts.

**A provider that named nothing counted as a provider.** `vacuity-check.py`'s census reported a
requirement whose `provider` was *empty* and never asked whether a non-empty one resolved to
anything, so `isolation/macos.rs:88 spawn_guest` cleared whether or not that file or that symbol
existed anywhere. A census could then report every external-effect requirement as provided while
several of them named a file nobody had written — the same vacuity the script exists to find, one
level up. A provider now has to resolve: a path that exists under the campaign's `sourceRoot`, or
a symbol some production file under it contains, with the test tree excluded because a test double
naming itself as the thing it stands in for is not a provider. The run prints
`providers: 2 of 2 named, 1 resolved`, and prints `NOT CHECKED` rather than a clean line when no
root says where production source is.

**A capture authorised its own duplicate.** `capture-lineage.py`'s shared pass exempted two
subjects publishing one image when each named the other in `sharesWith` — a declaration written
into the very registry the pass reads. `sharesReason` was demanded by the blocker's own remedy
text and read by no code at all, so the reason was required by documentation and enforced nowhere,
while `campaign.py` has required it since 0.9.3 and the two gates disagreed about the same
declaration. A share is now admissible only where every member names every other member, every
member records a reason, and something outside the declaration agrees they are one address: the
target the channel recorded at capture time, falling back to the subjects' declared routes. Two
shutters pointed at two addresses whose bytes happen to match no longer clear on a note the
photographer wrote about their own photograph.

**A gate whose whole population was the published captures.** `unsourced`, `untied` and `shared`
are all derived from captures a subject publishes, so an image sitting in the shots directory that
no manifest entry names contributed to no finding. Measured: `published captures: 0 · files in
shots dir: 11`, exit 0, and the sentence "Every published capture names a target that ties to its
subject" — true, and covering nothing. An image nothing publishes is now a finding; a campaign
that means to keep one records `unpublishedReason` on its `captures.json` entry, so the escape is
in the file rather than in somebody's memory. And a ratchet of 0 is refused the way
`strict-check.py` refuses an empty campaign, because a floor nothing has ever passed under cannot
fall and pinning it records an armed gate where there is none.

**A corpus that could disagree with the vocabulary silently.** The blind pass's test root was a
command-line argument and lived nowhere else, while the vocabulary that has to match it lived in
`campaign.json`. Pointing a campaign whose vocabulary is one language at another language's test
tree produced 32 findings, identical in shape and confidence to genuine ones; the same command
against its own corpus returned 0, and nothing warned, because the generic half of the vocabulary
matched and the project's own half never did. `campaign.json` now carries `testRoot` beside
`blindVocabulary`, `--tests` overrides it and says so, and when fewer than a quarter of the
declared mutators appear anywhere under the root the run reports the mismatch instead of a number.

Seventeen new gate tests in `tests/run.sh`, each watched red on a fixture built to trip it and
green on one that should pass. One existing fixture changed with them: the declared-share case
wrote `shareReason`, a key no script has ever read, over two subjects at two different addresses —
its assertion is unchanged and the fixture now describes a share that is one.

`plugin.json` said 0.9.3 while `.claude-plugin/plugin.json` and this file said 0.9.4, and 0.9.4's
code is what shipped. Both files carry 0.9.5.

## 0.9.4 — 2026-08-21

Two ways this gate could report a clean result over a population it never examined.

**A capped list read as a population.** `check` printed at most twelve unwitnessed requirements
and said nothing about the cut. A team scoped a wave of work off that printed list against a real
set of eighteen, and ten requirements were named by no item. Raising the cap does not fix it —
the next set outgrows the next cap — so every capped list now carries its own denominator:
`… (showing 12 of 18)` when it truncates, and `(showing 3 of 3)` when it does not, because a
reader who has to work out whether anything was cut is back in the position that caused the loss.
That covers the unwitnessed-requirement list, the hollow witnesses, the unevidenced passes, the
legacy-rung cases, the open cases, the duplicate and declared-share groups, the pixel claims, and
the lists carried inside blocker sentences.

**An oracle rung that was not on the ladder.** Four cases arrived recording `static-analysis` and
counted `unrated` — the bucket meaning the tool does not know what a case checked — while being
real, armed instruments: a source classifier that exits 1 on a one-line mutation and 0 on the file
as written. `source-analysis` is now a rung, and it sits off `ORACLE_RUNGS` rather than at a
position on it. The ladder is one axis, what a case checked against the running product, weakest
first; a reader of source text is neither weaker than `structural-visual` nor stronger than
`presence`, and giving it a rank would invent a comparison the coverage model does not have.
`SOURCE_RUNGS` is a parallel set alongside `EFFECT_RUNGS` and `RASTER_RUNGS`, printed on its own
`Off-ladder:` line, absent from `EFFECT_RUNGS` and staying absent.

Two guards keep it from becoming the cheap rung a campaign fills up on. A passing source-analysis
case owes the analyzer that ran and the number of units it examined, the same obligation shape
`effect-witness` carries for its recorder and count, because a search with no denominator cannot
tell an empty result from an empty search. And a requirement claiming an effect outside the
process may not rest on source analysis alone.

Five new gate tests in `tests/run.sh`, each watched red on a fixture built to trip it and green
once the fixture is repaired.

## 0.9.3 — 2026-08-21

`campaign.py check` and `capture-lineage.py --gate` disagreed about declared shares, and the
disagreement made one of them unfollowable.

**The blocker told you to do something it could not read.** Two published surfaces resolving to
one address produce one image under two subject ids, which the shared pass is built to accept
once it is declared: `capture-lineage.py` reads `sharesWith` + `sharesReason` from
`captures.json` and counts the group apart. `check` read neither, blocked unconditionally, and
printed *"Declare a genuine share in captures.json, or capture each subject"* — where the first
branch was ignored and the second reproduces the same bytes, because a genuinely shared surface
photographs identically however many times you point the shutter at it. Neither branch of the
instruction could clear the gate it was attached to. Measured on a real campaign where
`/settings` and `/settings/account` both resolve to `/dashboard?settings=account`: seven share
groups, all declared, gate green, `check` red with nothing to do about it.

`check` now reads the same declaration, requires every member of a group to name the others —
declaring one side of a pair is not a declaration — and reports declared shares as their own
counted line rather than folding them into the duplicate-shot blocker. An undeclared duplicate
still blocks, and still blocks with the same message, so the only thing that changed is that
the message now has a satisfiable branch.

## 0.9.2 — 2026-08-20

The blind-mutation check from 0.9.0 was measuring itself. Run against a real suite it reported
26 blind tests of 32 mutating; four defects in the detector accounted for 19 of them, and each
one made the pass report a larger number, which reads as thoroughness rather than as a broken
instrument.

**`--reader` replaced the seven defaults instead of extending them.** `tuple(args.reader) or
DEFAULT_READERS` means a project naming one reader of its own silently loses `assert_eq`,
`get_telemetry` and the other five, so every test reading through them is reclassified blind.
The flag that exists to teach the detector about a project made it blinder, and the resulting
rise in the count is indistinguishable from a thorough pass. Both flags now extend; `--only`
replaces, for the case where the defaults genuinely do not apply.

**The mutator pattern had no left word boundary.** `re.escape("record") + r"\w*\s*\("` matches
`record` inside `job_record(`, so a test whose only "mutation" was constructing a fixture was
reported as mutating-and-blind. Anchored with `(?<![A-Za-z0-9_])`, which still fires on
`.record(` and no longer fires inside an identifier.

**Fixture helpers were counted as tests.** A helper like `log_with_two_jobs()` mutates and
returns, leaving its callers to do the reading — so it is blind by construction and its callers
are not. Counting it inflated the denominator (168 where 141 is true) and added a finding about
a function nobody wrote as a test. A function called more than once in its own file is now
treated as a helper and excluded.

**The vocabulary could only come from the command line.** A project has to re-pass its flags on
every invocation or silently get the defaults, and a CI job that forgets them reports a clean
sweep. `campaign.json` now carries a `blindVocabulary` block with `mutators`, `readers` and an
optional `only`, and the run prints which source it used and how many terms it holds.

**`strict-check.py` never learned `effect-witness`.** The rung was added to `campaign.py` in
0.9.0 and its `EFFECT_RUNGS` set was not — so the rung that most strongly proves the product
acted scored in the same bucket as "something rendered", and building a real witness moved the
strict score by nothing.

## 0.9.1 — 2026-08-20

Three defects in 0.9.0's own effect census, all found by running it against the campaign it was
written for. Each read as a clean result, which is the failure mode the census exists to catch.

**`witnessed` was a subtraction, not a count.** It computed
`len(effect_reqs) - len(unbacked) - len(vacuous)`, so a requirement declaring an external effect
and recorded `reported` — claimed, never witnessed, and correctly not blocked — was subtracted
into the witnessed total and reported as an effect somebody had seen. On the egress registry that
printed `witnessed=1` where the true figure is 0. It now counts the requirements that actually
have a passing case at `effect-witness`, and names the rest as `unwitnessed` with their evidence
class beside them.

**The census printed only after the full-run verdict.** It sat past the selective-run `return 0`,
so on this skill's own default scope it never printed at all — a registry with eight vacuous
requirements said nothing about any of them, and the only place the numbers existed was `--json`.
It now prints in the header, beside the requirement and surface counts, on every path including a
blocked one.

**An unrecognised effect class vanished instead of blocking.** `add` refuses one, but a registry
edited by hand never passes through `add`, and an unrecognised class then simply failed the
membership test and dropped out of the census — indistinguishable from a requirement claiming no
external effect. `check` now blocks on it and names the classes it accepts.

`references/effect-boundary.md` §3 said a requirement whose declared effect has no provider is
`contradicted` at phase 1, where §2 of the same file defines `vacuous` for exactly that case.
Corrected, with the distinction spelled out rather than assumed.

Gate tests 48 → 53. The five new ones prove each of the above fires on a fixture built to trip it
and clears when the fixture is corrected.

## 0.9.0 — 2026-08-20

A campaign closed 230 cases over a CI runner built around zero-trust network isolation, armed 220
of them, cleared every gate this plugin owned, and recorded REQ-001 — "runner communication is
outbound pull only over HTTPS/WSS on TCP 443" — as **observed**. A reviewer on a neighbouring
project then read the source: no HTTP client anywhere in the dependency tree, no line of
production code that spawns a subprocess, `tart`, `wsl.exe`, `pfctl` and `nft` never executed, no
mDNS, and a daemon that only ever binds loopback. The isolation engines are rule generators and
state machines. Every network guarantee in the inventory was true because nothing crosses the
boundary they describe.

Nothing was broken here either. **Arming mutates the system** — revert the behaviour an assertion
guards, watch the case go red — and that finds what a suite does not cover. Ball & Kupferman named
it as one of a pair in *Vacuity in Testing* (TAP 2008): mutating the system finds coverage gaps,
and mutating the **specification** finds guarantees that were never exercised at all. This plugin
had shipped one half of a known pair 220 times and the other half never. Beer, Ben-David, Eisner
& Rodeh put the base rate at "typically 20% of formulas are found to be trivially valid, and
trivial validity **always** points to a real problem" (FMSD 18(2), 2001).

The standard toolkit cannot see it either, which is why the gap survived a mature campaign.
`cargo mutants` mutates the code that exists, so a boundary nothing reaches has no mutants;
coverage counts lines executed by the suite, and a rule generator's lines all execute; and the
whole isolation stack — `pytest --disable-socket`, `WebMock.disable_net_connect!`,
`nock.disableNetConnect()` — asserts the *absence* of I/O, so a suite built on it cannot
distinguish "correctly outbound-only" from "never communicates".

Applying the same lens **in-process**, needing no new lane and no privilege, immediately surfaced
a live defect the 230-case campaign passed: `stop_runner` returns `true` twice for the same
runner and never removes it, `stop_all_runners` reports "Stopped 2 runners" with the count
unchanged at 2, and `restart_runtime` returns "…restarted successfully" having restarted nothing.
The case covering it sat at the `outcome` rung, and the outcome it asserted was the arrival of a
sentence.

### Added

- **`references/effect-boundary.md`** — the two directions of mutation, the effect census, why
  mutation testing and coverage are both blind to this, the `effect-witness` rung with its
  four-part causal witness, `--seed-strengthen`, and the two places the research panel disagreed
  about where the floor sits on a machine without root.
- **`vacuity-check.py`**, three exact passes and a control. **unclassed**: a requirement whose own
  words name an effect outside the process and carries no `effect` field — it over-flags on
  purpose, because a false positive costs one `"effect": "none"` and a false negative costs the
  campaign its central claim. **uncensused**: an effect class with no `provider` named in
  production source. **blind**: a test that calls a mutating verb and never reads the observable
  again, so it can only be asserting the call's own return value. On the campaign above that pass
  read 164 test functions and found **26 of 32 mutating tests blind**, five of them in a file
  named for the effect it was not measuring.
- **`--seed-strengthen`**, this plugin's own arming rule turned on its new gate: strengthen a
  requirement's declared constraint until the registry cannot satisfy it, require red, restore the
  registry byte-for-byte. A strengthened constraint that still clears proves the census reads
  nothing.
- **The `effect-witness` oracle rung.** A recorder the product does not control — a packet
  capture, `dtrace`/`strace`, a real listener's accept log, a process table, a sentinel file —
  plus the effect class and the count it saw. `campaign.py set` gained `--recorder`,
  `--effect-class` and `--effect-count`; a claim at this rung with no recorder, no class, or a
  count of zero blocks, because a witness that saw nothing is the condition being tested rather
  than the proof of it.
- **The `vacuous` requirement evidence class**, the fifth beside observed / reported /
  contradicted / unknown. A guarantee that holds because the capability it constrains never runs.
  It is a finding in the same way `contradicted` is, and it clears the gate: a correctly recorded
  `vacuous` is finished honest work, and blocking on it would mean no campaign over a partly-built
  product could ever go green. What blocks is the dishonest configuration — an external effect
  class, recorded `observed`, with no passing `effect-witness` case behind it.
- **Sweep M, reality boundary and vacuity**, in `references/sweeps.md`: census, reachability,
  witness, sabotage, strengthening and blind mutation, with a denominator on each. Two of the six
  cost nothing and need no privilege.
- **Fifteen gate tests**, each proving a new blocker fires on a fixture built to trip it and then
  clears when the fixture is fixed. 33 → 48 passing.

### Changed

- `SKILL.md` carries a fifth failure mode; phase 1 produces the effect census alongside the
  requirement inventory; phase 5's rung table gains `effect-witness`; phase 7 gains sweep M; the
  CHECKED test gains a campaign-level obligation that every requirement claiming an external
  effect is either witnessed or recorded `vacuous`.
- `references/coverage-model.md` gains an **effect boundary** axis (in-process · own process tree
  · kernel · host · network) and connects instrument vacuity to product vacuity — the same shape
  one level up.
- `references/project-comprehension.md` carries the fifth evidence class and the closed effect-class
  list.

### Not settled

The panel split on where the witness floor sits, and the disagreement is recorded rather than
resolved. One reading holds that nothing below a kernel-observed causal effect may be recorded
`observed`; another holds that a machine without root still has a real floor — a genuine loopback
listener logging its accepts, or a real spawned process writing a sentinel — and that setting the
bar at `dtrace` on every host means the rung goes unused. `references/effect-boundary.md` §5
carries both.

## 0.8.0 — 2026-08-20

A campaign published 20 surface captures and cleared every gate this plugin owned — every case
accounted for, 46 of 49 checked under the strict rule, every `-glass` lane proved and witnessed.
The captures were of three unrelated documents: a project status report, the mock browser's own
index page, and a design accessibility doc. Twenty files held **six distinct images**; four groups
of four were byte-identical. A flow step captioned "Open pairing QR code sheet" showed a
questionnaire about Apple developer credentials.

Nothing was broken. `attach-shots.py` binds a picture to a surface on a slug of its **filename**;
`evidence-page.py` rendered it with an `alt` taken from the label, so a wrong image arrived under
a right-sounding caption; `campaign.py check` ran its artifact and duplicate detectors over
`RASTER_RUNGS` case evidence only, and the `shot` field the page actually renders was inspected by
nothing. The gated part of the campaign was sound and the ungated part was the part people look
at.

### Added

- **`references/capture-lineage.md` and `capture-lineage.py`** — `warrant:oracle`'s lineage plane
  with *picture* substituted for *figure*. There, a displayed number without a `data-source-ref`
  is the defect the plane exists to find; here, a published capture without a recorded target is.
  Four passes, all exact, none needing a model: **unsourced** (no manifest entry, or no target),
  **untied** (the target does not resolve to the subject's route), **shared** (two subjects, one
  sha256, undeclared), **unjudged** (published with no `be-my-witness` verdict — this one ratchets
  rather than blocks, for the same reason `strict-check.py` ratchets).
- **`--seed-swap`**, the gate watched to fail. Swapping two subjects' manifest entries must turn
  the tie pass red; a swap that passes means the pass reads nothing and every verdict it ever
  issued is worthless. That is the campaign's own arming rule turned on its own gate.
- **Phase 8a** in `SKILL.md`, between the differential and publication.
- **A fourth failure mode** in the opening: publishing a picture of one thing under the name of
  another.
- **Twelve tests** in `tests/run.sh` covering every new blocker in both directions, plus the
  seeded swap and the manifest it borrows and restores.

### Changed

- **`campaign.py check` audits the published shots**, not only raster-rung case evidence. Three
  new blockers: a shot that is not a usable capture, a shot repeating another subject's picture,
  and a shot bound to its subject by filename alone. The verdict now prints the wall's distinct-image
  count beside its cell count, so a gallery that repeats itself says so on its face.
- **`attach-shots.py` refuses to write an attachment no capture manifest corroborates.**
  `--filename-only` proceeds and stamps `"shotProvenance": "filename"` into the inventory, so the
  weakness travels with the data rather than being forgotten at the next read.
- **`evidence-page.py` badges every rendered capture** with how its subject was established —
  *witnessed*, *manifest*, or *filename*. It also anchors a flow step on the step's **own** id
  rather than one recomputed from the loop index, which used to renumber every anchor after a
  reordered step and silently repoint links a reader had already shared.
- **`witness-worklist.py` demotes a reference that is not a raster.** The measured campaign
  reported 20 judgeable pairs, 0 blind, every reference an unrendered `.html` path and
  `evidence/shots/mock/` absent — the pair template had never run and `pairs.json` was
  hand-authored metadata describing captures nobody took. Reporting that as judgeable is what let
  the whole comparison be skipped without anything saying so.
- **`assets/capture-pairs.template.mjs` writes `captures.json` as it shoots**, recording the URL
  the browser *ended up at* rather than the one it was sent to — a redirect to a login page is
  exactly the capture that otherwise gets filed as the dashboard.

### Why the four passes are deterministic

`be-my-witness`'s `prescan.py` returns `isEvidence: true, settled: true`, exit 0 against the worst
capture in that campaign: a real, contentful, settled image of the wrong document. Image statistics
cannot answer the subject question, and frontier multimodal models reach roughly 40% recall on
fine-grained UI diffs. Provenance answers it, and only if it is recorded while the shutter is open.

## 0.7.0 — 2026-08-19

A campaign could measure a repository thoroughly and a `warrant` in the same repository would
still refuse every tier, because neither plugin could read the other's state. And a case nothing
could settle resolved to `inconclusive` alongside cases an instrument merely failed to measure,
which sent half the work to the place that cannot fix it.

### Added

- **`unoracled: <reason>`, split from `inconclusive`.** The two arrive looking identical and have
  opposite remedies: `inconclusive` is an instrument problem and wants a better instrument;
  `unoracled` is a specification problem, where nothing was ever named that a check could read,
  and no instrument helps. Both hold the gate. The distinction is not new — a screenshot-judging
  pass over fifty surfaces once returned inconclusive on all fifty and the record said the
  verdicts were "for want of a judge rather than for want of an oracle", then every tool
  downstream collapsed the two halves into one status.
- **Phase 6a, oracle construction**, and `references/oracle-construction.md` behind it: a
  four-rung ladder from a specification-sourced outcome assertion, through a metamorphic relation,
  through a property-based invariant, to a recorded permanent limit in structural terms. Stop at
  the first rung that holds. Metamorphic relations are the standard answer to the oracle problem
  and the reason an unoracled case is tractable without a baseline; the evidence for them is
  directional rather than sized, and the reference says so.
- **`campaign.py export-warrant <dir> --root <repo>`** — writes `.warrant/suite-health.json` (the
  armed ratio, the effect-rung passes, the campaign's own gate) and `.warrant/oracle-coverage.json`
  (per surface, keyed by file path so warrant's `rollup_classes.py` can match it against the
  warrant's class globs). Nothing is inferred: a campaign that measured little exports little and
  the warrant still refuses the tier, which is the outcome that should follow.

### Why the export keys by path

The first cut keyed `oracle-coverage.json` by surface id, which matched no glob and rolled up to
zero coverage on every class — indistinguishable from a campaign that measured nothing. Caught by
running the full chain rather than by reading the schema. `rollup_classes.py` reads a list of rows
carrying `file`, `figures`, `sourced` and `unsourced`, and the export now emits exactly that.

### Changed

- `unoracled` is counted separately in `check` and `report`, named with its remedy in the blocker
  list, and folded into `unavailable` in the observation coverage rather than into `deferred`.

### Evidence

The two constraints on generating an oracle are measured and both are in the reference: roughly
half of LLM-generated test plans duplicate existing cases (50.5% duplicates, 22.5% invalid, 27%
valuable and new), so generation runs against a cell from the coverage model rather than
free-form; and the model that wrote the code may not be its sole oracle, because generated tests
demonstrably validate faulty behaviour and code in context biases later generation toward
mutually consistent but incorrect implementation/test pairs.
