# Evidence: the Diolog UI-flow campaign, 30 Aug – 2 Sep 2026

Mined 2026-09-02 for the `test-campaign` skill. Lane A of three: this file carries the
measurements, lane C writes rules from them.

**What this is.** Over four days a campaign in `~/Dev/dAIolog` took end-to-end UI-flow
coverage of a Next.js app from 52 journeys run to a 925-journey specification with 889
bound to a test and 552 able to fail a build. Everything below is either a repo path or a
session id plus a quoted line. A figure with no source is not here; §7 lists what I looked
for and could not find.

**Sources.** Claude Code journals under
`/Users/lukerhodes/.claude/projects/-Users-lukerhodes-Dev-dAIolog/`:

| short id | file | size | date |
|---|---|---|---|
| `943ee869` | `943ee869-5879-4c01-88bf-aab6085b65ba.jsonl` | 86 MB | 2 Sep (live) |
| `ede5bc94` | `ede5bc94-4ea8-479d-b3ba-58788764b48d.jsonl` | 61 MB | 2 Sep |
| `09dc5677` | `09dc5677-74f7-4f2f-8d16-b524480be745.jsonl` | 71 MB | 29 Aug |
| `7d585913` | `7d585913-df5a-4299-8a71-6b0be656c68b.jsonl` | 74 MB | 27 Aug |
| `c055ffc6` | `c055ffc6-726d-430c-ab06-b0cc1b79bd07.jsonl` | 205 MB | 26 Aug |

The richest seam is the compaction summaries in `943ee869`, which open with a
`📌 PINNED — STANDING CONSTRAINTS, CORRECTIONS, AND REJECTED APPROACHES (VERBATIM)` block
reproducing standing constraints verbatim. 47 lines in that session match
`REJECTED|CORRECTIONS I MADE|PINNED`; the largest single block is 57,426 characters and
carries 144 numbered "how to work" rejections, 74 "what to build" rejections and 75
self-corrections. Where a claim below cites `943ee869 PINNED #n`, that is the numbered item
in that block.

Repo artefacts cited (read-only; the campaign repo was not modified):

- `docs/test-campaign/specimen/README.md` and `pathologies.json` — the calibration standard
- `docs/reckoning/2026-09-02/flow-campaign-axes.json` — the eight axes, measured
- `docs/reckoning/2026-09-02/flow-campaign-remaining.json` — throughput and remaining work
- `docs/reckoning/2026-09-02/progress.html` — the non-technical report
- `docs/plans/plan-100-percent-ui-flow-coverage.md` — the five conditions
- `docs/test-campaign/defects.json`, `flow-findings.json`, `flow-specification.json`
- `scripts/test-campaign/*.mjs` — the seven instruments
- `docs/features-to-triage/BRIEF-*.md` — the failure-to-card artefacts

---

## 1. The coverage model — eight axes that must never be blended

### 1.1 The eight axes, as measured

`docs/reckoning/2026-09-02/flow-campaign-axes.json`, generated 2026-09-02 over a population
of 925 flows (292 p0, 451 p1, 182 p2) sourced from
`docs/test-campaign/flow-specification.json`. `sessionStart` is the same axis measured at
the start of that day.

| # | axis key | `means` (verbatim from the file) | end | start |
|---|---|---|---|---|
| 1 | `named_any_mention` | "a spec file mentions the flow id anywhere, including in comment prose" | 925 / 925 | — |
| 2 | `bound_to_a_test_title` | "a test or describe TITLE carries the id, so a case is tied to the flow" | 889 / 925 | 689 |
| 3 | `ci_enforced_blocking` | "listed in a CI step that can fail a build AND that step passes its project flag" | 552 / 925 (p0 130/292) | 418 (p0 30) |
| 4 | `report_mode_only` | "runs in CI and cannot fail a build" | 185 | — |
| 5 | `in_no_ci_step` | "never executed by CI at all" | 188 (p0 45, p1 123, p2 20) | 293 |
| 6 | `distinct_recorded_passes` | "a case id observed passing in a recorded run" | 1,160 of 6,056 cases | 123 |
| 7 | `frames_captured` | "a screenshot exists, filed under a flow" | 3,217 frames over 593 flows | 0 |
| 8 | `surfaces_judged` | "an AI verdict recorded against a frame, over two runs" | 75 | 3 |

Three properties of the model are declared in the file itself and are the load-bearing part:

- `"isFloor": true` — **"Every axis is a lower bound on coverage and an upper bound on
  nothing."**
- The floor note explains why axis 1 is published *beside* axis 2 rather than instead of it:
  **"'Named' counts a comment mention, which is why the bound figure is published beside it —
  36 flows are still named only in prose."**
- Axes have different populations and cannot be averaged: **"A recorded pass is a case id,
  not a flow, and the two populations are different sizes."** 925 flows against 6,056 cases.

### 1.2 The five conditions the axes decompose

`docs/plans/plan-100-percent-ui-flow-coverage.md` derives the model from the owner's own
statement of the goal, quoted in the plan: *"automated user flows for every task that include
screenshots of the steps in the flow, and then have an ai model verify that nothing looks
wrong in the model and have the automated user flows programmatically check for the outcome
that's expected."*

> That is five separate conditions per flow, not one. A flow is finished when all five hold:
> 1. a spec names it;
> 2. that spec **runs**, and is observed passing;
> 3. a screenshot exists for each step;
> 4. an AI verdict records that nothing looks wrong in that picture;
> 5. the programmatic assertion checks the outcome the flow specification names, and **can
>    fail a build**.
>
> Reporting one blended percentage across those five hides whichever is weakest, and the
> weakest is currently condition 2 at 2%. So this plan tracks them as five denominators and
> never averages them.

The eight axes are that five refined: condition 1 splits into *named* and *bound*, condition
5 splits into *blocking* / *report-mode* / *not in CI at all*.

### 1.3 The distinctions that carry the axes

**NAMED versus BOUND — a comment is a claim, a title is a binding.**
`943ee869` key-concepts section: *"a comment claiming coverage is a claim; a flow id inside a
test title is a binding. Only a binding can be counted, screenshotted or promoted."*
The consequence when this was blended: `943ee869 PINNED` REJECTED-how-to-work #2, **"A card id
in a COMMENT is not evidence. Over-reported by 18 cards."** And #122, a four-part
self-correction: **"I counted PROSE and called it CODE — four times"** — `.auth/` in
`*.spec.ts` where "all 12 hits are comments, real blind count is **ZERO**"; a
`blob\.example\.com` grep matching `consoleGuard.allow(/blob\.example\.com/)`; and
`test.skip('…')` where **"9 of my 244 were prose mentions inside comments."**
The measurement rule that follows: strip comments before counting. The plan states its inert
count was **"counted after stripping comments so prose mentions are excluded."**

**WIRED versus ABLE TO FAIL A BUILD.** Two mechanical conditions, both required, evaluated
per step. `943ee869` key concepts: *"a spec must be in a step's explicit file list AND that
step must pass a matching `--project=` flag — evaluated per step, and the project is
`testMatch` MINUS `testIgnore`."* Sources of error, each measured: PINNED #7 **"Assuming a
matching Playwright project means CI runs it"**; #90 **"`--project=spreadsheets` was never
passed anywhere in `ci.yml`"**; #116 **"`ci-wired.sh` unioned BOTH CI steps' `--project=`
flags. Check per step, never on a union."**
A third state sits between wired and blocking: `continue-on-error: true`. The plan measures
**"507 flows have a spec that cannot fail a build. 213 of them run in a CI step marked
`continue-on-error: true`; the other 294 appear in no CI step at all, and 117 of those are
p0. A spec in report mode finds a defect only when a person opens the report."**

**PARKED AT THE DECLARATION versus SELF-SKIPPING AT RUNTIME.** These look identical in a
coverage count and are opposite in meaning. `943ee869` key concepts: *"`test.skip('title',
fn)` never runs; `test.skip(expression, reason)` inside a body is a runtime guard that does
run."* The plan measures both populations: **"200 cases are inert by construction — 185
`test.fixme(title, body)` and 15 `test.skip(title, body)`, spread over 97 files… They are
distinct from the 641 *conditional* skips, which are guards that let a case decide at runtime
whether its precondition holds; those are working as intended."**
The runtime behaviour was verified rather than assumed — PINNED #119: **"`test.fixme(title,
body)` skips BEFORE the body runs. Verified with a marker file: `1 skipped`, marker
absent."**
And the rule that follows, PINNED REJECTED-what-to-build #68: **"Do NOT ban `test.skip`
outright. Floored on soundness in the intake divergent pass: this campaign has just built 52
legitimate runtime guards that use `test.skip(<expression>, reason)` inside a body."**
A parked case that self-skips forever is its own pathology — specimen P5: *"What it selects
on no longer exists, so the guard is true every run. The journey keeps its place in a
coverage count for months after the control it gripped was removed."*

**A TITLED PLACEHOLDER — a name and nothing else.** `flow-campaign-axes.json` under
`knownWeak`: `titled_placeholders: n 29, ofInert 97, sessionStart 62`, meaning **"the parked
body has ZERO statements — a title and nothing else"**. `943ee869` key concepts:
*"`test.fixme(title, fn)` whose body has zero statements once comments are stripped — a name
with no check, counted by every title-reading instrument."* The specimen plants this as **P3**
and notes the aggravating variant: *"Planted on a **live** declaration, not a parked one. A
parked empty body is honest about being unfinished; a live one is counted as a pass by every
runner."*

**A CASE THAT COMPUTES AND ASSERTS NOTHING.** Specimen **P4**: *"a test whose title reads as
covering a journey while it asserts nothing… Worse than P3, because the body computes. A
reader skimming the file sees a populated test, and no product change can make it fail."*
This is the axis with **no instrument at all** — see §2.4.

**A WAIVER POINTING AT A PARKED TEST.** Specimen **P6**: *"The waiver is the
`existingCoverage` entry in the fixture flow specification: status `covered`, naming a file
whose only case is parked. Both halves read as fine in isolation; only following the pointer
shows the hole."* Also unguarded.

### 1.4 Two further model rules

**Weak coverage found by reading the oracle against the assertions.**
`flow-campaign-axes.json` `knownWeak.oracle_gaps_found: n 63` — **"flows whose bound case
holds only part of the oracle, found by reading oracle against assertions during the binding
pass"**. This was not found by an instrument: `943ee869` self-correction #72 records that a
matcher-name instrument returned **"3 of 3 false positives, because the dominant idiom puts
the literal in the LOCATOR and a structural matcher on the end. The instrument that DOES
work is per-flow oracle-vs-assertion reading, which surfaced 63 gaps as a side effect of
binding."**

**Blocked is a third class, not a failure and not unbuilt.** `flow-campaign-axes.json`
carries a `blockedNotUnbuilt` map with four entries, one of which is a recorded *wrong*
belief kept visible: `"secure_context": "CI runs on http://localhost:3100 which IS a secure
context, so this is NOT a blocker — recorded because it was wrongly believed to be one"`.

---

## 2. The instrument failures

### 2.1 One number, wrong four times in one day

The specimen README states this as the reason the specimen exists:

> Every coverage figure in this campaign comes from an instrument, and the instruments have
> been wrong more often than the product. In a single day one number was measured wrong four
> separate times, each reading plausible and each published:
>
> 1. project membership counted without list membership;
> 2. `--project=` flags checked against the union of two CI steps rather than per step;
> 3. steps parsed by fixed line offset, which rotted the moment a path was inserted;
> 4. `testMatch` read without `testIgnore`.
>
> A CI step name that states its own counts drifted four times the same day. A backlog cut
> from those figures inherits their error.

The fourth, in the session's own words (`943ee869 PINNED` #139): **"`testMatch` without
`testIgnore` is the fourth way this one number has been got wrong. `chromium`'s testMatch is
the broad `tests/.*\.spec\.ts` while its testIgnore excludes nine directories including
spreadsheets and multi-user. Reading only the first reported 24 files in the BLOCKING step as
running when they resolve to zero tests, and inflated CI-enforced from 434 to 460."**
The third (#138): **"`max()` over path lines lands on the LAST step in the file. My 15
demoted specs went into 'compiled claims, report mode' (2 flags) instead of 'storyboard
suites, report mode' (16 flags), so they were just as inert. Find steps by NAME, never by
position."**
And the self-documenting-step-name failure (#144): **"A step name that carries its own counts
drifts silently. `ci.yml`'s blocking step claimed 515, then 532, 545, 589, 601 while listing
something else, four times in one day. The fix is a check comparing the claim against the
parsed YAML — and it fired on my own very next edit."**

### 2.2 Wrong readings that were published and then corrected

From `943ee869`'s ⚠️ CORRECTIONS I MADE TO MYSELF block, each naming the commit:

| # | wrong reading | correct reading |
|---|---|---|
| 64 | commit `e6a974dcd` published **CI-enforced 460/925, p0 57/292** | true figures **434** and **55**; corrected in `4f44e5745` |
| 65 | **546** distinct recorded passes written into a commit message | measurement said **524**; amended |
| 66 | campaign baseline reported as **689** | **"52 journeys run by the storyboard suite and 12 declared by the registry on 30 August"** (commit `1dd453798`); 689 was two days of prior work |
| 63 | commit `b0dbba5f3` said a flow showed an error banner *"while the case's own programmatic assertions passed"* | **the case FAILED** — failure 105 at `web-5126-briefing-journeys.spec.ts:228`; corrected in `081260691` |
| 70 | screenshot binding order reached **827** | shipped `flowIdFromTest` order reached **716**, and **113 of the 829 ids it emitted were not flows at all** (`flow-cc1-056-…` → `FLOW-CC1-056` where the flow is `FLOW-CROSS-CUTTING-1-056`) |
| 75 | p0-flow ceiling of **126** | **123 unique p0 flows** — "three are bound to two files each, so summing batch yields double-counts" |
| 61 | "the flow-shots directory had lost 576 screenshots" | cwd drift — 642 PNGs intact; **"Third occurrence of this class this session"** |
| 67 | an earlier lane "DELETED seven assertions" | every one had been **rewritten stronger or corrected**; corrected in `3f618e409` |

Two are generalisable measurement rules rather than arithmetic slips. #20 in the REJECTED
block: **"Summing per-card flow steps double-counts. Count DISTINCT flows."** And #140:
**"'Does this exact string appear anywhere in the file' cannot distinguish a rewrite from a
removal. It reported seven assertions as deleted when every one had been replaced by a
stronger or corrected form."**

### 2.3 The calibration specimen

`docs/test-campaign/specimen/` — a fixture root carrying six planted defects, a
`pathologies.json` recording per instrument per defect what a correct instrument *would* say
(`truth`) and what the real one *does* say (`known`), and `scripts/test-campaign/check-specimen.mjs`
which runs every instrument across it.

Its stated licence to break the repo's own no-mocks guardrail, verbatim:

> **Everything under `docs/test-campaign/specimen/` is a deliberate, permanent exception, and
> the defects are the product rather than a shortcut.** A calibration standard with no known
> defects measures nothing. Deleting these fixtures to satisfy the guardrail removes the only
> thing in the repository that can tell you a coverage instrument has stopped working.

The six defects, verbatim from the README table:

| | defect | what it does in the wild |
|---|---|---|
| P1 | a journey whose test genuinely passes | The control. If an instrument cannot report this one cleanly, nothing it says about the other five means anything. |
| P2 | a journey whose test genuinely fails | Statically indistinguishable from P1. Every static instrument calls it covered and is right on its own axis. Only a run separates them — which is why a static coverage figure is not a coverage figure. |
| P3 | a test whose body is empty once comments are stripped | Planted on a **live** declaration, not a parked one. |
| P4 | a test whose title reads as covering a journey while it asserts nothing | Worse than P3, because the body computes. |
| P5 | a test unparked in the source that self-skips every run | The journey keeps its place in a coverage count for months after the control it gripped was removed. |
| P6 | a journey exempted by a waiver pointing at a test that is itself parked | Both halves read as fine in isolation; only following the pointer shows the hole. |

**Three outcomes, and they are not the same thing** (README, verbatim):

- **DRIFT** — an instrument's behaviour changed since it was last recorded. *"This is the
  only thing that sets the exit code, so the checker is green on a healthy tree and red the
  moment an instrument moves in either direction."*
- **CONDEMNED** — an instrument misses a defect on its own stated axis. *"Printed every run,
  never silenced, figures void on that axis. A standing fact about the instrument set, not a
  regression."*
- **UNGUARDED** — no instrument in the set has an axis covering this defect at all.

The ratchet rule: *"**Never edit `known` to quieten a break.** If an instrument was improved
and now matches `truth`, raise `known` to `truth` in the same commit as the fix; that
ratchets."*

### 2.4 What the specimen condemned, measured 2026-09-02

Nine instrument/defect pairs condemned. From the README:

- **`measure-empty-bodies.mjs` misses P3**, *"the exact defect it is named for. Its
  declaration regex accepts only a parked declaration, so a live empty body is invisible to
  it."*
- **`measure-inert-cases.mjs` misses P5.** *"Its axis is every case that never executes; this
  case never executes. It matches only a park at the declaration, so a runtime self-skip does
  not register."*
- **`measure-ci-enforcement.mjs` reports 6 of 6 enforced when only 2 can fail a build.** *"It
  is correct as a wiring figure… and wrong under the headline it prints, `flows CI-ENFORCED
  (can fail a build)`. An empty body, a test that asserts nothing, a self-skipping test and a
  parked test cannot fail anything."*
- **P4 and P6 are UNGUARDED.** `pathologies.json` declares this machine-readably rather than
  in prose, with `script: null` and an `absent` string: for `assertion-presence`, *"NO SUCH
  INSTRUMENT EXISTS. Pathology 4 is unguarded: nothing in this repo can tell a test that
  asserts from one that only computes."* For `waiver-integrity`, *"NO SUCH INSTRUMENT EXISTS.
  Pathology 6 is unguarded: existingCoverage.status is read as covered without following the
  pointer…"*
- **`measure-title-binding.mjs` is correct on its own axis** *"and its figure is still not a
  coverage figure: it binds all six specimen flows, including the four that cannot fail a
  build."*

A defect found while building the specimen and not fixed: *"`measure-empty-bodies.mjs` finds
its declarations in **raw** source, so a `test.fixme(` written inside a comment matches. The
first draft of P3's header comment made the instrument report P3 correctly for entirely the
wrong reason."*

**Containment is structural, and proven rather than asserted.** *"The specimen lives outside
every path any real instrument walks… The checker proves it rather than asserting it: it runs
all four static instruments against the real repo root as well as the specimen, and fails on
any `FLOW-SPECIMEN-*` id or `specimen/` path that appears in a real count. The real figures
with the specimen in the tree are unchanged — 552 flows enforced, 913 bound, 97 inert cases,
29 empty bodies."*

**The declared weakness of the whole idea**, verbatim: *"A conservator's standard is inert and
shares no material with the painting. This one is made of the same stuff as the suite and
lives in the same repository… It is not independent of what it calibrates. That is a real
weakness, not a caveat — the specimen can tell you an instrument changed, and it cannot tell
you the whole toolchain drifted together."*

The instrument set as shipped: `scripts/test-campaign/` holds `check-specimen.mjs`,
`derive-flow-atoms.mjs`, `measure-ci-enforcement.mjs`, `measure-empty-bodies.mjs`,
`measure-enforceable-flows.mjs`, `measure-inert-cases.mjs`, `measure-title-binding.mjs`,
`measure-unguarded.mjs`.

The seventh pathology the README nominates: *"a file listed in a CI step under a project that
ignores it — the fourth historical mis-measurement, `testMatch` read without `testIgnore`."*

### 2.5 Generic instrument pathologies worth carrying into any project

All from `943ee869 PINNED` REJECTED-how-to-work, each measured here:

- #39 **"An instrument that COUNTS is not an instrument that MATCHES."**
- #34 **"A gate reading different arithmetic from its instrument is worse than no gate."**
- #62 **"A gate glob can read the wrong population."**
- #26 **"Identical counts across independent specs mean ONE shared cause."**
- #4 **"`card_evidence.py` reads `git ls-files` — UNTRACKED SPECS ARE INVISIBLE."**
- #3 **"File-level inertness over-reports. Called 26 cards INERT when one `test.skip` sat in
  a 40-case spec."**
- #45 **"The card-evidence `e2e_specs` list includes specs ALREADY in CI."**
- #23 **"String-comparing two readouts to decide 'do they agree' marked the WORKING case as a
  lie."**
- #89 **"`cannotfail_scan` matches patterns, not semantics."**
- #97 **"A hand-rolled reimplementation of a gate's matcher returned 0 sites on BOTH trees."**
- #112 **"A regex-based JSON extractor keyed on field ORDER missed 3 of 17 records. Use
  `raw_decode`."**
- #102 **"'first list found in the JSON' picked the wrong key. Key on the NAMED field."**
- #103 **"The `defects-carded` gate reads `existingCard`; agents wrote `card`, one wrote
  `cardId`."**
- #104 **"`campaign-remaining.json` goes stale. Derive it from the spec tree."**
- #58/#61/#123 — shell instrument traps: `grep -c` prints `0` and exits 1, so
  `$(grep -c … || echo 0)` yields `"0\n0"`; `grep -cE '^PASS'` reported a working 7/7
  selftest as 0/7 because the output is indented; `rc=$?` after a pipeline reads the *last*
  command's status.

**Arming — the only way to know a test can fail.** `943ee869` key concepts define it:
*"`cp` backup verified by size → break the thing → watch RED for the intended reason →
restore → watch GREEN."* Three failure modes are recorded: #46 **"An arming that PASSES is
not a pass — it is an unfinished arming."**; #82 **"An arm can go red for the WRONG
REASON."**; #81 **"A false RED is the mirror of an inert arm."** And the destructive trap,
#96: **"`io.open(p,'w').write(io.open(p+'.armbak').read())` TRUNCATES THE TARGET BEFORE
evaluating the read. Back up with `cp`, verify the copy's size."**
Nx caching interacts with arming — from `dAIolog/CLAUDE.md`: a cached target replays its
previous PASS, so arming must use `--skip-nx-cache` or invoke the runner directly.

---

## 3. The estimates — measured throughput

### 3.1 The three shapes of work

`docs/reckoning/2026-09-02/flow-campaign-remaining.json`, whose `basis` field reads
**"measured from this session's 140 agents across 12 lanes, 1311 units"**:

| shape | units per agent | wall minutes per lane | source field, verbatim |
|---|---|---|---|
| **read-and-rule** | 8.2 (median) | 8 – 25 | "median of 6 triage/binding lanes today" |
| **write-a-body** | 1.0 – 4.1 | 10 – 36 | "4 authoring/conversion lanes today" |
| **run-and-promote** | *not agent-limited* | 10 – 36 | "tier-limited, not agent-limited"; `tiersUsable: 3`, `tiersDeclared: 4` |

Worked instances, from the same file's per-row `measured` fields and `progress.html`'s
estimate table:

- binding: **"binding did 146 flows / 19 agents / 8 min"** (`progress.html`: "145 attached by
  19 workers in 8 minutes")
- guard conversion: **2.8 – 3.9 units/agent**
- body authoring: **"14 bodies written by 14 workers across 2 batches today"**
- ruling on inert cases: **"82 reasons recorded by 10 workers in 7 minutes"**
- run-and-promote: **"six run lanes today moved 293->188, i.e. 105 flows across ~6 lanes"**;
  `progress.html` states the same as "134 promoted today across 6 run batches on 3 machines"

**The caveat is part of the figure**, verbatim: *"Every wall-clock figure is a RANGE for one
lane, measured today, and carries no failure rate: 4 of 12 lanes lost an agent, all recovered
by resume-from-cache or by splitting. A lane that ran 36 minutes and produced work later
rejected counts the same here as one that landed."*

### 3.2 Serial versus parallel totals

`progress.html`'s estimate table sums the eight remaining pieces to **5.6 – 32.2 h** run one
after another, and **2.0 – 9.6 h** run in parallel where *"the top row governs; it waits on
machines, not people"*. The top row is "373 journeys that cannot fail a build". The report
also declares what the ranges exclude: *"The two decisions waiting on a person… have no
worker time attached, because waiting is not w[ork]"*, and *"No allowance for review or
release."*

### 3.3 Concurrency — what happened at what width

Two measurements that appear to conflict and do not. **Report both.**

**Five slots for fleet runners.** `943ee869 PINNED` REJECTED-what-to-build #73: **"Do NOT run
the fleet wider than five slots. harbourmaster offers 6 and the machine has 12 cores, but 92
runners died silently on 2026-08-26, 88 of them at exactly 180.0 seconds, with no error row
in any counter. *'Treat a request to run wider as a request to lose work silently.'*"**
The fuller record is in `09dc5677`: *"a correctness limit, not a throughput preference. Going
wider does not slow a wave down — it kills agents that never emit a token. Measured
2026-08-26: **92 agents died silently, 88 of them at exactly 180.0 seconds**, each leaving a
four-line transcript ending `[Request interrupted by user]` with no assistant message and no
error row anywhere. A wave of eight that loses three is slower than a wave of five that loses
none *and looks identical in every counter*."*

**Nineteen lightweight agents held.** `943ee869 PINNED` CORRECTIONS #83: **"19 concurrent
agents held with 0 deaths. The 'five concurrent is a correctness limit' rule was wrong by
nearly four times. The honest test is the 180s probe, which costs four minutes. Ramp
deliberately and probe."** The same session's assistant turn: *"this session measured 19
concurrent agents holding without loss, so I'm ramping rather than waiting."*
Also #83 in the how-to-work block: **"The 8-subagent cap is PER WORKFLOW, not session-wide."**

**How deaths present in the counters — the detection rules.** From `09dc5677`:
**"Derive failure from `started − results`. Never from the error field."** And:
**"Assert that a fan-out actually fanned out.** After every wave, compute
`sum(agent durations) ÷ wall clock`; **under 1.2 the wave ran serially** and should be
reported as a defect rather than a result. It costs two timestamps."*
Corroborating rules from `943ee869 PINNED`: #8 **"Resuming a workflow with `results=0`. Replay
is a sticky prefix."**; REJECTED-what-to-build #30 **"Do not resume a workflow whose
`started=17 results=3`."**; #84 **"A concurrency verdict must only count runs in THIS
session's window."**; #64 **"Liveness is NOT journal mtime."**; #74 **"A liveness filter that
enumerates today's wave names goes stale."**; #75 **"Widening a liveness filter to any
`web-5` string matched 26 worktrees from other sessions."**

**What actually kills a lane.** #135: **"Unbounded WORK, not brief length, is what kills
lanes. Prompts of 2.4–3.5k characters died at ~128 tool uses / ~176k tokens. Cap iterations,
report incrementally, prefer one Playwright invocation over many. Re-confirmed: G07 died TWICE
as one agent over six files; split one file per lane, six of six returned with zero deaths."**
One fleet lost **14 of 17 agents to a single API error** (`943ee869`).

**Two invisibility traps.** #142: **"`nohup … &` inside a Bash call detaches the process from
the harness. No task exists, so no completion notification ever fires and the run is invisible
in the task list."** The user saw this directly — *"i dont see any runs going"* and *"how will
you know when they're done"* (`943ee869` user turns). And #141: **"A 120-second tool timeout
turns a slow success into a reported failure."**

### 3.4 The throughput ceiling was the harness, not the model

`flow-campaign-remaining.json` `blocked` names four harness blockers, one of which cost a
third of run throughput all session: *"tier 4 wedged on the Edge instrumentation compile —
blocks a third of run throughput, all session — its own log says Slow filesystem detected,
1050ms benchmark — it is starved, not broken — owner: harness"*. That reading was itself
corrected later (CORRECTIONS #68: *"The recycle DID fix it; it exceeded my 120s tool
timeout."*). The other three: a standalone seed mongod that cannot open transactions
(WEB-5327, ~11 spec files), a mock email sink present in the repo and wired into no seed tier
(so every email-token journey is unwritable *and* the seed API can send real mail, WEB-5333),
and a queue with no product writer at all.

---

## 4. The reporting shape

The artefact: `docs/reckoning/2026-09-02/progress.html`. Its eight `<h2>` sections, in order:

1. Testing the 925 journeys a customer can take
2. The campaign from its start, not from this morning
3. Where the eight measures stand today
4. What the AI screen-checking actually found
5. Problems in the app the tests found today
6. Four things are stuck on the environment, not on work
7. Two phrases from the earlier report, in plain words
8. What is left, and what it would take

### 4.1 How it was arrived at — the reader's own complaints

An earlier version was rejected. The user's verbatim message (`943ee869`):

> **"There's no mention of the visual verifications in the report. It's also not clear what
> `cases ruled out by decision` means. I'd also like /visualization:visualization to be used
> to make the report easier to see how things are progressing. Update to be non-technical and
> include estimates for all of the web app issues that the tests have already found if any."**

Five distinct complaints: a measured axis was missing; a term of art went unexplained; the
numbers were not visual; the register was technical; the defects had no sizing. Sections 3, 4,
5 and 7 of the shipped report each answer one, and section 4 opens by saying so — *"This was
missing from the previous report, and it is the part with the least flattering answer."*

Two more corrections from the same reader:

> **"`up from 689` - we started at near zero so perhaps you need to look through previous
> sessions for more data"**

which produced section 2 ("The campaign from its start, not from this morning") and the
correction recorded at CORRECTIONS #66. And, earlier:

> **"`CI-enforced — in a step that can fail │ 418/925 (45.2%), p0 30/292 (10.3%)` `Cases with
> a current recorded pass │ ~51 of 5,621` this seems very low considering our aim for 100%
> coverage"**

— the reader reading the weakest axis rather than an average, which is the behaviour a
per-axis denominator is for.

### 4.2 "Denominator per axis, never one blended percent" — what it does in practice

The report states the rule twice in its own words. In the lede: *"the report keeps the
measures apart rather than averaging them — because an average would hide the weakest."*
Above the dumbbell chart: *"Each row is shown against its own total, printed on the right,
because the raw counts are not comparable — 925 journeys and 6,056 test steps are different
things."*

Mechanically, four things:

**Every figure carries its own denominator on the row.** The eight-row table reads
`Measure | Start | End | Out of | Change`: 889/925, 552/925, 130/292, 737/925, 1160/6056,
593/925, 75/593, 5959/6056. Three different denominators (flows, p0 flows, cases) and one
sub-population (frames judged out of flows with frames).

**A missing measurement is drawn as missing.** *"Nobody measured the release-blocking line on
31 August or 1 September, so it is drawn dashed rather than interpolated — the line between
two points is not a claim about the days between them."*

**A figure measured against a different denominator says so rather than being rescaled.**
*"1 September's 79.9% and 64.9% are against 633 journeys, the number judged to owe coverage at
the time, not against 925."*

**Another campaign's percentages are refused outright.** Section 7: *"The reconciliation tool
covers an older, separate testing effort — its own records say it looks at 11 of the 946 test
files. This campaign is the other 935. Its numbers were correct and about something else, so
quoting them here would have been the exact mistake it exists to prevent."* The machine-readable
form is `flow-campaign-axes.json`'s `whyNotReckon` field, and the standing rule is
`943ee869 PINNED` REJECTED-what-to-build #70.

**The third category is kept visible.** Section 7 explains "cases ruled out by decision"
(48 of 369): *"It is deliberately not counted as tested, and not counted as remaining either.
It is a third category, kept visible because the reason can expire: something ruled out today
may be worth checking after the next change."*

### 4.3 Register — what "non-technical" meant here

Every axis is renamed to an outcome a reader owns: `bound_to_a_test_title` → "journeys with a
test attached"; `ci_enforced_blocking` → "a broken test stops a release"; `distinct_recorded_passes`
→ "test steps watched passing"; `surfaces_judged` → "screens an AI has checked";
`inert_cases` → "test steps able to run". Defects are titled by what a user would notice
("Renaming yourself saves, and every screen still shows the old name"), with columns
`What a user would notice | Where | Size`. Sizes are defined inline — *small under half a day ·
medium half a day to two days · needs a decision first: someone must choose the intended
behaviour* — and sized from *"how long comparable changes took in this codebase — not a
commitment, and it excludes review and release."*

Every chart carries a long-form textual description of itself before the SVG (readable in the
extracted text of every figure), and every chart is followed by a table headed "Same figures
as a table, with where each one comes from" whose last column is the source.

### 4.4 The report is willing to publish a negative result

Section 4 is the model. 75 screens, 600 questions, 8 questions per screenshot; *"534 answers
came back healthy (89%), 18 flagged a problem, and 17 said 'I cannot see that from this
picture' — which at 2.8% is the number that matters most, because it says the questions are
answerable from a screenshot at all."* Then:

> **It has not yet caught anything the ordinary tests missed.** Of the 18 flags, two were on
> screens where the ordinary test had already passed — the only kind that would be new
> information. Both turned out to be the camera, not the app: one screenshot was of the
> browser's own error page, because that test deliberately cancels its navigation; the other
> showed a "Publish failed" message on a test whose entire purpose is to prove the app refuses
> bad input, so the refusal is the correct outcome.
>
> So the honest verdict is **not proven** rather than **proven useless**.

The machine-readable twin is `flow-campaign-axes.json`'s
`knownWeak.visual_marginal_value.status: "UNPROVEN"` — *"over 75 judged surfaces, 0 violations
survived being read as a defect the programmatic half missed; 2 candidates were both instrument
artefacts."*

### 4.5 Proposed work is marked as proposed

The estimate chart's footnote: *"blue labels: proposed, not asked for — delete one to decline
it."* Three of the eight rows are marked `(proposed)`, including the specimen itself
(6 items, 0.3–1.2 h) and the 3,142 unexamined screenshots, whose basis line says *"75 examined
today; the cost arithmetic should be redone before committing."*

---

## 5. The defects the suite found

### 5.1 Counts, by lane and artefact

| artefact | n | what it holds |
|---|---|---|
| `docs/test-campaign/defects.json` (25 Aug) | **61** | campaign defects with `id`, `title`, `severity`, `class`, `where`, `evidence`, `why`, `status`. Severity: 20 high, 28 medium, 11 low, 2 informational. Status: 45 fixed, 6 partially-fixed, 4 open, 3 "by design", 3 invalid. |
| `docs/test-campaign/flow-findings.json` (31 Aug) | **469 findings, 11 confirmed** | a code-vs-spec reading pass. `kind`: 287 `gap`, 182 `doc-vs-code`. The 11 `confirmed` are product defects with file:line evidence. |
| `docs/features-to-triage/BRIEF-defect-*.md` | **29** | one brief per defect |
| `docs/features-to-triage/BRIEF-flow-*.md` | **12** | the flow-analysis lane's defects (uncommitted at session start) |
| `progress.html` §5 | **17** | defects found *on 2 September alone*, each sized |

Three of the 61 are classed `invalid` and 3 "by design" — the register keeps a false positive
visible rather than deleting it. One was explicitly recorded as such: `943ee869 PINNED` #88,
**"The `empty_catch` finding in `flow-inbox-006-thread-render.spec.ts:82` is a FALSE
POSITIVE."**

### 5.2 The kinds

The 11 confirmed flow findings, verbatim keys from `flow-findings.json`, are a fair sample of
what a UI-flow suite finds that a unit suite does not:

- *"console nav renders 7 sections, INVESTOR_PORTAL-004 asserts 6"* — `ConsoleNav.tsx:100`
  adds Custom domains; spec pins `toHaveCount(6)`. **A test contradicting the product.**
- *"perception-studies Retry is a NextLink to /dashboard"* — a control that navigates away and
  retries nothing. **A dead affordance.**
- *"video-library widget cannot play a video"* — *"renders title/category/duration; 0 iframes,
  0 anchors, 0 hrefs"*. **A feature with no mechanism behind it.**
- *"logout skips the cookie clear when Auth0 is unconfigured"* — a `Response.redirect` returned
  before the clearing branch. **A security-relevant early return.**
- *"bare /tasks 404s"* — no `page.tsx` under the route group. **A route named nowhere it is
  linked from.**

`progress.html`'s 17 span the same range plus accessibility (*"Sixteen settings fields are
unnamed to a screen reader"*, *"There is no 'skip to content' link anywhere"*), locale
(*"The calendar's week label follows the browser, not Australian format"*), z-order
(*"The export tray sits on top of the Guardian drawer's controls"*), responsive
(*"A narrow window promises a keyboard reorder with nothing to reorder"*), outbound
(*"An internal note is emailed to the investor"*), and one defect in the evidence itself:
**"Twenty-four journeys were marked as covered by tests that do not cover them."**

Three of the 17 are sized `decision` — *"someone must choose the intended behaviour"* — and the
report says why that ordering matters: *"the three decisions should be settled before any of
them starts, because two of those change what the fix is."*

### 5.3 How a failure became a filed card

The pipeline, as the user specified it (`943ee869`, standing instruction):

> **"Until all user test are implemented, checked and any failures logged in diolog-tasks as a
> Todo and gone through /intake. Once that's all done, utilise /ship-fleet:ship-fleet to work
> through all of the new issues - the goal is met when all issues are resolve, committed,
> merged to staging and pushed"**

Mechanically: **test failure or spec-vs-code finding → evidence with file:line in
`flow-findings.json` → a brief in `docs/features-to-triage/BRIEF-*.md` → `shipyard:intake` →
a card on the tasks board → `ship-fleet`.**

A brief carries a fixed front-matter block —
`docs/features-to-triage/BRIEF-flow-perception-studies-retry-does-nothing.md`:

```
- card: WEB-5246
- origin: flow-specification analysis · 2026-08-31
- audience: IR teams whose perception study failed and who currently have no way to run it again
- platforms: web
- proposed-by-ai: false
```

then **What and why** (naming the file and line on both sides — page and service), an
**Acceptance sketch** whose bullets are observable outcomes, and **Assumptions made writing
this**.

The part that makes this a *test-campaign* artefact rather than a bug report is this section,
verbatim from that brief:

> **Two tests pin the broken behaviour as correct and must be rewritten as part of the fix**,
> not worked around:
>
> - `apps/web/e2e/tests/perception-studies/perception-studies.spec.ts` — `PERCEPTION_STUDIES-013`,
>   whose title is *"Retry" appears only on failed rows and links to /dashboard*, plus its row
>   in `apps/web/e2e/test-plan/perception-studies.md`.
> - `apps/api/src/modules/perception-study/perception-study.service.spec.ts` — `it('refuses to
>   reclaim a failed study')`, which asserts the throw that blocks a requeue.

A green test asserting the defect is itself part of the defect, and the brief names it so the
fix cannot pass by leaving it green. Its acceptance sketch closes the loop: *"`PERCEPTION_STUDIES-013`
asserts the new behaviour, and its title no longer names `/dashboard`."*

### 5.4 The gate that stops a defect being found and then lost

`scripts/goal/flow-campaign/defects-carded.sh` — a goal gate whose own comment reads *"Every
product-defect a triage confirmed has a board card."* Its observed output line:
`defects-carded rc=1 0/15 product-defects carded`. Three recorded failures of the linkage it
guards, from `943ee869 PINNED`:

- #92 **"Card ids filed by intake existed only in the agent's reply."**
- #93 **"`docs/features-to-triage/BRIEF-defect-*.md` do NOT carry their own card ids."**
- #103 **"The `defects-carded` gate reads `existingCard`; agents wrote `card`, one wrote
  `cardId`."**
- #60 **"Always assert the returned object's own `issueId`, and read `stateId` back after a
  write."**

### 5.5 What makes a suite able to find things

Three findings bear directly on this:

- **Weak oracles are found by reading, not by matching.** 63 oracle gaps surfaced as a side
  effect of the binding pass; the matcher-name instrument built to find them returned 3 of 3
  false positives (CORRECTIONS #72).
- **Wiring an unrun spec is not free coverage.** REJECTED-what-to-build #2: *"Wiring 'free
  coverage' specs. Five candidates returned **11 failed, 8 passed**. **Run before wiring.**"*
- **A serially-clean file can fail under CI parallelism.** `flow-campaign-remaining.json`, the
  report-mode promotion row: *"needs a run at CI worker count, not serial: the report-mode
  evidence caveat is explicit that a serially-clean file can fail at 4 workers."*

---

## 6. The prohibitions

### 6.1 What may never be done to a test to make it pass

The core rule, `943ee869 PINNED` REJECTED-what-to-build #39, verbatim:

> **Do not weaken an assertion to fix a spec bug.** Forbidden: deleting an assertion;
> replacing a value check with a presence check; **adding `.first()` when the duplicate IS the
> finding**; widening a regex until it matches anything; parking a case.

And #29, which supplies the reason:

> **Do not relax an assertion to match a bug.** *"Relaxing it to match would make the defect
> the specification."*

Supporting rules, each with its own learned reason:

| # | rule | reason it was learned |
|---|---|---|
| 41 | **"Prefer asserting a VALUE or an ordered list over a COUNT."** | a count passes on the wrong contents |
| 44 | **"Do not assert a literal that encodes one data state."** | see #38: *"A claim pinned to one data state is a tripwire on data, not a guard."* |
| 43 | **"Do not select an unnamed control by its fill class — fix the product's accessible name."** | the selector hides the accessibility defect it routes around |
| 14 | **"Do not re-point a failing claim at a nearby selector."** | the claim stops being about the thing that failed |
| 13 | **"Do NOT close a criterion with `reads_naturally`."** | a subjective oracle closes anything |
| 15 | **"`test.fail()` is refused for characterising a NEW defect."** | #51: *"An expected `test.fail()` is NOT a failure"* — the suite goes green on the defect |
| 40 | **"Do not remove a `@known-defect` tag on an agent's word."** | the tag is the only record that a green is conditional |
| 34 | **"Do not park a healthy item to satisfy a stuck detector."** | parking converts an instrument fault into lost coverage |
| 12 | **"Route-level flow binding is NOT evidence."** | a route is not a journey |
| 105 (how-to-work) | **"A conditional early-`return` in a test control makes the assertion skippable."** | the case passes without reaching its check |
| 50 (how-to-work) | **"`no-result` is NOT a pass."** | absence read as success |
| 36 | **"Do not treat a red at SETUP as evidence about the behaviour under test."** | a harness failure is not a product verdict |
| 27 (how-to-work) | **"A precondition's error message is not evidence."** | same class, on the other side |
| 65 (how-to-work) | **"A probe weaker than the claim it would overturn must not be treated as a refutation."** | the general form of all of the above |

### 6.2 What may never be done to the evidence or the gates

- #24 **"Do not weaken `audit-coverage.spec.ts` or remove a registry row."**
- #46 **"Do not delete a CWE-601 guard to make a coverage metric clean."**
- #19 **"Do not change `namedInputs`/`seedDefaults` in passing to make a gate agree."**
- #35 (how-to-work) **"Never ratchet on unrun evidence."**
- #45 **"Do not promote the 150 report-mode specs without run evidence."**
- #55 **"Do not add the missing `--project=` flags to CI's blocking step without run evidence."**
- #28 **"Do not re-record a pass ledger from a contaminated run."**
- #37 **"Do not hand-edit `specSha256` in a pass ledger."**
- #58 **"Do not build a ratchet that cries wolf."**
- #61 **"Do NOT raise `timeout-minutes` on the e2e job."**
- #38 **"Do not commit agent scratch files as tests."** With the mechanism, how-to-work #33:
  **"`git add apps/web/e2e` swept an unaudited lane file into a commit. HIT FIVE TIMES."**
- #25 **"Do not edit a signed compliance document."** — the same reason `warrant.toml` is
  quoted in the session as *"this file is signed when a named person commits it; an agent
  committing it is not a signature."*
- Specimen README: **"Never edit `known` to quieten a break."**

### 6.3 What the AI judge may never be

- #64 **"Do NOT gate CI on the visual judge. The repo's rule is that the model is never the
  release gate."** Also stated as #9: **"The AI model must NEVER be the release gate."**
- The judge's own design enforces it: `judge.ts` returns per-atom verdicts
  `held | violated | not-observable | inconclusive`, and *"Only `violated` fails a surface —
  `compare.spec.ts:518-528` gates on contradicted expectations alone… a judge that cannot see
  something says so rather than failing the build"*
  (`docs/test-campaign/runs/visual-judge-scope-2026-09-02.md`).
- It is bounded by construction: `JUDGE_CONCURRENCY` 3, `JUDGE_MAX_CALLS` 400, and
  `assertJudgeReady()` *"refuses to run without gateway credentials rather than silently
  degrading."*
- Atom shape is a bias control, not a formatting choice: `capture-manifest.ts:293` builds one
  atom per line because *"fixed-length atoms neutralise the verbosity bias a paragraph of prose
  introduces into a judge."*
- #63 **"Do NOT derive per-flow visual atoms from `flow-specification.json`. Emits 1,600 atoms
  across 770 flows, most unusable, because the specification describes BEHAVIOUR and a frame
  settles APPEARANCE."**
- A screenshot must be proven to be of a product surface. `flow-step-capture.ts` carries a
  `notEvidenceReason(url)` guard rejecting `chrome-error://`, `about:blank` and `''` —
  *"the browser is on its own error page… so no product surface was rendered"*. Both false
  positives in §4.4 were exactly this class.

### 6.4 What may never be done to the environment to make a test pass

- #10 **"Do not unblock an outbound-risk step by letting it fire. Intercept at the boundary."**
- #48 **"Do not make the outbound mock tag-aware."**
- #49 **"Do not add a `KNOWN_CONSOLE_ERROR_ALLOWLIST` entry for a seed-data fault."**
- #56 **"Do not seed around a bad precondition."**
- #57 **"Do not plant a citation tag in seeded memory content."**
- #22 **"Do not run a seeder against production from a background agent."**
- #53 **"Do not import unverified rows from `diolog-seed-raw`."**
- #60 **"Do NOT fix WEB-5326 with `tags.some(t => t.startsWith('@mutating'))` — it would match
  a future `@mutating-nh3` and grant a write to a live customer tenant."**
- #17 **"Do not edit under `apps/web` while a Playwright run is in flight."**

### 6.5 Ordering and scope prohibitions

- #54 **"Do not author more flow specs before the current ones are known to run."** — the
  single most transferable sequencing rule here: axis 2 (bound) moved 200 in a day while axis
  6 (recorded pass) sat at 2%.
- #33 **"Do not rewrite 154 freshly-merged specs to adopt the `Flow` driver."**
- #32 **"Do not brief every remaining tier at once."**
- #74 **"Do NOT clean the 229 worktrees or 582 `ai/*` branches speculatively. One
  (`ai/conversations-ui-4947`) holds 2 unmerged commits. Surface, never guess-delete."**
- #1 (how-to-work) **"Always edit line-anchored on (line number, exact indent), verified by
  content not index."** With #86: **"Removing one offending line shifts indices and can
  re-qualify its neighbour. Match by content, never position."**

### 6.6 Two out-of-family referrals that became prohibitions

Recorded in the PINNED block as `(referral, codex/gpt-5.6-sol high)`:

- #20 **"intercept-and-assert-request is NOT coverage for a server-side write defect."**
- #21 **"replaying the BFF response or seeding via API do NOT cover AI-generation cards."**

Both say the same thing: an assertion placed on the wire before the defect's location cannot
witness the defect.

---

## 7. What I looked for and could not find

Stated so lane C does not write a rule against a figure that is not there.

1. **A defect count for the whole campaign.** Four registers exist with different scopes and
   dates (61 / 469+11 / 29+12 briefs / 17 today) and no artefact reconciles them. I have not
   asserted a total.
2. **A per-defect attribution to the axis that caught it.** Nothing records "this defect was
   found by a screenshot, that one by an assertion, that one by reading". Only the visual
   judge's marginal value is measured (0 of 75, §4.4) — the equivalent figure for programmatic
   assertions versus spec-reading is not measured anywhere I found.
3. **A false-positive rate for the suite.** `defects.json` has 3 `invalid` of 61 and one
   named false positive (#88), but nothing states a rate or a denominator.
4. **A cost figure in tokens or dollars for any lane.** `flow-campaign-remaining.json` is in
   agents and wall minutes only. Two failed runs are recorded with token counts
   (`175.1k tok · failed`, `175.9k tok · failed`) and a death threshold of *"~128 tool uses /
   ~176k tokens"*, but no per-unit cost.
5. **Minutes-per-lane for run-and-promote as a distinct figure.** The file declares the shape
   `"tier-limited, not agent-limited"` and its rows reuse the write-a-body range (10–36 min).
   That range is inherited, not separately measured; I have flagged it as such in §3.1.
6. **Any published JSON Schema.** `flow-specification.json`, `journeys.json`, `flows.json`,
   `defects.json`, `cases.json` and `pathologies.json` all have stable de-facto shapes, and no
   `$schema`, no schema file and no validator exists in `docs/test-campaign/` or
   `scripts/test-campaign/`. Making these into published schemas is the lane-B/lane-C work the
   brief describes; nothing in the campaign has done it.
7. **A stated retention or expiry policy for waivers.** `progress.html` proposes *"an expiry on
   every disabled check"* as row 8 of the remaining work, marked `(proposed)` — so the policy
   is nominated and does not exist.
8. **`c055ffc6` (26 Aug, 205 MB) and `7d585913` (27 Aug) yielded nothing on the flow-campaign
   terms I searched.** The 2026-08-26 concurrency measurement is quoted in `09dc5677` and
   `943ee869` rather than present in the session it describes; I have cited the sessions that
   carry the text.
