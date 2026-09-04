# Changelog

Notable changes to the plugins in this marketplace. Newest first.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); each plugin carries its own version in its `plugin.json`, and this file records what moved and why.

## 2026-09-04

### status-update 1.1.0: roadmaps and measured time estimates

- **What is coming next.** Adds roadmap and estimation support so reports model what is ahead as well as what just landed.
- **Empirical estimation from `reckon:reckon`.** Sizing is grounded in reckon's measured 1,842-agent benchmark across 31 projects: task size tiers S (3–25m, median 8m), M (7–56m, median 15m), L (14–68m, median 25m), and XL (25–155m, median 45m). Wave parallel arithmetic accounts for the slowest member × 1.1–1.8. Point estimates are explicitly banned in favor of p25–p90 ranges with medians.
- **Visual roadmap zone in project report.** Renders an estimated duration hero banner with basis provenance, an SVG Gantt timeline diagram (following `visualization:visualization`'s `type-gantt` and `type-timeline` conventions), and a companion table view.
- **Next round & time in portfolio dashboard.** Derives upcoming round goals and parallel wall-clock ranges into `portfolio.json`, adding a dedicated "Next round & time" column to the dashboard projects table.
- **Decision work carries zero duration.** Waiting on humans or credentials is not priced as agent time.

### status-update 1.0.1: living HTML status reports and portfolio dashboard

- **The page is the report.** Replaces scrolling chat status updates with two living HTML pages: `<project>/STATUS.html` for single-project reporting, and `~/Dev/STATUS.html` for a master dashboard across all projects.
- **One data write, everything derived.** Agents write only `<project>/.status/project.json`; `scripts/render.py sync <project>` renders the project report, derives its dashboard row, and updates the portfolio dashboard automatically to prevent drift.
- **Derived from 2,400 real status reports.** Mined from 14 days of transcripts across 27 projects (634 concerns, 8,959 occurrences). Sections match what agents already write — including the first-class self-correction block that nine independent mining passes found to be the most consistent section after the headline.
- **Real chart forms from visualization.** Uses Sankey task flow, dumbbell alarm checks, beeswarm problem severity, slopegraph correction comparisons, treemap unmeasured scopes, and heat-strip cross-project check matrices.
- **Plain words over developer jargon.** Replaces internal terms (gate, armed, mutation, sha, verdict) with plain English explanations and defines remaining terms via `<dfn>`.
- **Active data correction.** Overrules false green claims: checks over 0/0 counts are forced to `unmeasured`, and alarms that caught 0 faults are forced to `armed: false`.
- **Brand treatment.** Uses the Engine C split-flap mid-turn icon (`icon-engineC-0e8378.png`) across the 1024, 256, 128, and 48px exports and the 3200×1040 banner.

## 2026-09-02

### `reckon` 1.9.4 — two defects that made the ledger stop being a closed world

**A reserved filename was matched as a prefix.** `read_briefs` skipped anything whose name
merely *began* with `BRIEF-TEMPLATE`, `README`, `00-INDEX` or `LEDGER`, where only those four
exact basenames are scaffolding. On perch that dropped nine consumed briefs named
`LEDGER-<TOPIC>-<slug>.md` at discovery — and a file dropped at discovery is not in the
partition, so no downstream gate can report it missing. The run gated clean over a ledger that
had lost nine rows. The names are now compared exactly.

**The ratio that gates retirement counted briefs the join is never consulted about.** A brief
declaring a waived-or-archived status is classed from that status before `classify` reads the
join, so counting it rates the inferential step on rows it never touched — and the more
history a project archives, the less it can retire. Perch published 98/224 = 43.8%, withheld
every retirement claim, and had in fact joined 56 of 56 of the briefs whose class the join
decides; four briefs its own orchestrator records as merged sat `undecided`. The ledger now
publishes both denominators — `briefs_joined` over every brief and
`briefs_joined_adjudicated` over the population the join decides — and `join.weak` reads the
second. Publishing only the first is the defect; publishing only the second would hide how
much of a queue is archive.

Measured on perch after both: 233 briefs discovered instead of 224, adjudicated join
56/56 = 100.0%, warning gone, and 43 brief rows move `undecided` → `retirable`. Two selftest
sections pin the pair, each shown red against 1.9.3 first, and one of them pins the opposite
direction — a genuinely weak adjudicated population still warns, and names its population.

## 2026-09-01 (later)

### The gemini.md sweep's audit findings, closed

The sweep earlier today shipped 29 files of which 10 carried auditor findings. A second
workflow fixed them: 10 fixers, each handed its own file's findings, pipelined into 10 fresh
re-auditors that re-ran the gate and checked whether each finding was actually closed. 6 came
back fully closed; 4 carried residue the fixers introduced, which the conductor then fixed by
hand. All 29 files now sit inside the 150-250 line bound with `verify_quotes.py` at exit 0 and
14-23 checked `[docs]` claims each.

What the findings were is worth recording, because they are the class of defect prose review
does not catch. `flagship` shipped a machine-state exemplar labelled `1m<5m, falling` over the
figures `1m 14.2 · 5m 11.8` — rising, not falling, and its own `max/core 0.89` confirmed which
figure was the max. Its bound ledger reported `4 of 6 within, 2 breached` over rows that read 3
and 3. `whats-left` counted `reckon`'s partition as 6 classes when it has eight, in the one row
whose purpose is to stop a partition being counted short. `create-luke-content` attributed a
worked example to a `SKILL.md` line that says something else, and put two paraphrases in
backticks as if they were the skill's own strings. Five overrides across four skills asked for
a table, ledger or note and shipped an empty schema or a description instead of a filled one.

Two findings were rejected rather than actioned, both traceable to the authoring brief rather
than to the files. That brief banned the `[measured-here]` tier outright on the grounds that no
Gemini run of these skills had been read, which was too broad: `ux-craft` cites a real recorded
run (`Egress Gemini`, 17 Aug 2026, n=1, `geminify/references/evidence.md` §1.1), so its use of
the tier is earned. `whats-left` and `ux-craft` each carried one genuinely mis-tiered claim —
an observation about `geminify`'s own gate, not about a run of the host skill — and those were
re-tiered to `[measured-family]` rather than deleted.

Still true of the whole sweep: no Gemini run of any of these files has been observed, so their
effect remains reasoned rather than measured, and the corpus behind them is flash-tier only.

## 2026-09-01

### tailings 0.2.0: Codex transcript attribution and fail-closed pairing

- **Codex Desktop transcripts are first-class input.** `signals.py` reads `response_item`
  envelopes while preserving the Claude message parser and its controls.
- **Subagent ownership is explicit.** The scan begins at the first `agent_message` addressed to
  the transcript's declared `agent_path`, excludes inherited parent history, and reports the
  boundary and parent thread id.
- **Model attribution follows the owned turn.** Parent model context is excluded, and a model
  change inside the child session updates later calls before the T7 family comparison.
- **The first child turn keeps its governing context.** A context directly before the addressed
  task message seeds the child only when no intervening response item belongs to parent history.
- **Unknown reviewer models fail closed.** T7 names the model-less call and exits 4 instead of
  borrowing a model observed later in the session.
- **Unknown families also fail closed.** A nonempty but unrecognized running or lane model is
  disclosed as uncheckable rather than silently treated as independent.
- **Calls cannot disappear silently.** Stable one-based ordinals pair every custom or function
  call with its output; zero recognized activity and orphan calls or outputs fail closed.
- **Repository evidence stays attributable.** Cross-reference probes distinguish accessed paths
  from modified paths and refuse broad capture/commit attribution from concurrent work.
- **Adds a Gemini-calibrated gemini.md**, so the conditional pointer already in SKILL.md now resolves to a real file instead of a missing one. Written by the geminify Mode A procedure and gated by verify_quotes.py.

### Gemini support swept across 26 plugins: 5 new `gemini.md`, 24 refreshed

A workflow ran the `geminify` Mode A procedure over every skill in this marketplace whose
Gemini layer was missing or had fallen behind its `SKILL.md`. 68 skills carry a `SKILL.md`;
63 already had a `gemini.md`, and of those, 24 predated their skill's last change by 1 to 8
days. Those 24 plus the 5 with none were the work set. The other 39 were already current and
were left alone rather than churned.

The five that had none — `eli5`, `positioning`, `tailings`, `visualization`,
`create-luke-content` — were worse off than "missing a file": each already carried the
conditional `Running as a Gemini model?` pointer in its `SKILL.md`, aimed at a `gemini.md`
that did not exist. A Gemini runner following that pointer found nothing and continued. Those
five now resolve, and take a minor bump; the 24 refreshes take a patch.

Every file was written by an agent that read the target `SKILL.md` and its references in full,
ran `scan_skill.py --refs`, and looped `verify_quotes.py` to exit 0 — so each quoted vendor
sentence is verbatim from Google's bundled corpus. `[docs]` claim counts per file run 14 to 28.
Authors wrote only their own `gemini.md`: 29 files changed and no `SKILL.md` touched, verified
against `git status`, because `install_pointer.py` writes this file and `marketplace.json` and
29 agents editing one file corrupt it. Pointers and version bumps were applied serially
afterwards.

Each file was then graded by an independent auditor that re-ran the gate and checked ten of
`geminify`'s own rules. **19 of 29 passed; 10 carry findings that are not yet fixed** — a
miscounted lint-format set in `create-luke-content`, a worked example attributed to the wrong
`SKILL.md` line, backticked "quotes" that paraphrase rather than quote, two files with no
`unmeasured on this skill` list, and `ship-fleet` at 277 lines against the 150–250 target
(down from 288, so improved rather than introduced). Those are queued, not resolved, and the
files ship as an improvement on what was there rather than as finished work.

One caveat on the whole sweep: no Gemini run of any of these new files has been observed. Their
effect is reasoned from the corpus behind `geminify`, not measured, and that corpus is
flash-tier only.

## 2026-08-31

### generate-investor-portal 1.3.0: a kind's props are claims, not fields

Six defects from one real tenant, an unlisted Australian company, and the rules that follow. Full
measurements in `references/what-shipped-wrong.md`.

- **The blocker: prose in `governanceGroup.docs[]` asserted eleven documents nobody publishes.**
  That array's renderer draws a PDF affordance per row, counts the rows into an "N documents"
  heading, and reserves a date column. Five prose commitments and six third-party standards
  inherited all three claims, on a governance page, for a company whose own source material says it
  publishes no documents at all. The array validated, the route returned 200, the tokens were right.
  The new rule sits in SKILL.md rather than only in a reference: read what a kind **asserts** about
  what you hand it, because a field that accepts your data is not a field that means it.
- **Six fields whose rendering contract is not what their type suggests**, each with a visible
  defect behind it: a hero `headline` array is LINES (a trailing "." got a line of its own) while
  `identity.freeHeadline` is inline runs; `prose` draws no eyebrow and renders an array body run-on;
  a `§` ordinal on a kind that renders no eyebrow puts a gap in the *rendered* index; a badge string
  does not wrap and scrolled a document sideways at 375px; and the ledger joins to the page by
  **label**, so a qualified ledger label silently reads as an undisclosed value.
- **Writing `chrome` replaces it wholesale.** `header ?? headerFromRecord(record)` — omit `mark` and
  the masthead publishes `AE`, the reference tenant's monogram, under another company's name. The
  footer merges and the header does not, from the same-looking edit.
- **Three renderer defects recorded so nobody reintroduces them**: a disclosure marker tested against
  `from === 'mock'`, a value `ValueProvenanceSchema` cannot carry, so it was dead on every tenant
  while the line above it claimed the rows were marked; a venue fallback of `'the exchange'` that
  reintroduced, for unlisted tenants, the defect the venue derivation had just removed; and a 4:3
  `object-fit: cover` on unit media that cropped 26%, 44% and 26% off three product diagrams.
- **And the instrument, not the page.** A probe reading `getBoundingClientRect()` cannot see an
  absolutely-positioned `::before`, so it reported four link classes at 15–20px whose real hit area
  was 14px larger. One target-size class genuinely needed the fix; two did not. Check for the
  existing extension before enlarging a target, and report a padding change as making the
  measurement honest rather than as fixing an accessibility defect.

### deck-craft 1.17.0: the collision check could not see a container

- **`chromeCollisions` walked a list of text tags, so a panel through the footer rule read as
  clean.** The selector was `p,li,td,th,h1,h2,h3,h4,figure,table`. A `<div class="panel">`
  crossing the footer matches none of them, so the check stepped over it and the slide passed.
  Measured on a real twelve-slide deck: three panels crossing the rule on three separate slides,
  by 15.7px, 7.3px and 2.0px, with `chromeCollisions: 0` and a `PASS` verdict. A reader found it
  by looking at the screen, which is the outcome the gate exists to make unnecessary.
  - The walk is now every element in the slide, kept if a viewer can *see* it land on the chrome:
    it carries a background, a visible border, or text of its own.
  - **The threshold moved to authored pixels, at a hairline.** It was four *rendered* pixels,
    which at a stage scale of 0.667 is six authored ones, so a box genuinely through the rule by
    two or three sat in a dead zone the gate could not report.
  - **A full-height layout wrapper is excluded, on height alone.** Its padding box legitimately
    extends past the footer; that is what the padding is for. Width is not a discriminator, and
    testing it was itself a bug — an editorial cover whose copy column is 1290px of a 1920px
    stage is still a wrapper, and a width test excused every slide except that one.
  - **The outermost crossing box is reported, not every descendant.** A panel through the rule
    otherwise arrives once per line of text it holds: five findings for two crossings.
- **Two new eval assertions, and the second is the control.** `A18` fails the old probe and passes
  the new one on `evals/fixtures/chrome-boxes.html` — the real deck cut to three slides, one clean,
  one panel through by 34 authored px, one card through by 4. `A19` asserts the widened walk still
  reports zero on the clean fixture, because widening a selector is exactly where false positives
  arrive; it caught the width-test bug above before it shipped.
- **The general shape, for the next check.** A gate scoped by an enumerated tag list is a hole
  rather than a scope, and it fails in the direction that reads as success. Scope by what an
  element *does* — paints, carries text, is chrome — and exclude by a stated property, so a new
  kind of node is covered the day it is authored rather than the day somebody remembers the list.

## 2026-08-30

### reckon 1.9.0: the remaining work, scheduled into waves with measured durations

- **The ledger becomes a wave plan**, using `ship-fleet:ship-fleet`'s model so the two skills
  describe one shape of work rather than two: nodes are work items, edges are dependencies,
  and a wave is everything whose dependencies sit in earlier waves. Two things differ, and
  both are about entitlement. A `cited` edge is a citation somebody wrote into the registry
  and it blocks; an `inferred` edge is reckon reading a shared surface and it only *orders*
  the work, because a false edge costs somebody's parallelism and a guess is not entitled to
  spend it. And decision work is never scheduled at all — an `undecided` row is a person
  reading two documents and ruling, so giving it an agent duration would report waiting on a
  human as though a machine were busy.
- **Durations are measured, not assumed.** A new corpus, parsed from Claude Code's own
  transcripts: 2,230 subagent transcript files, 2,572 units extracted, **1,842 on Opus 4.8 or
  Opus 5** inside the analysis band, over 88 sessions and 31 projects, 14 Jul – 30 Aug 2026.
  A unit is one sidechain tree, timed first record to last. Provenance, method, exclusions and
  limits in `skills/reckon/references/estimation.md`.
  - *Edit volume predicts duration better than stage label does.* Read-only units run a 3.0 min
    median; 1–4 files 7.9; 5–14 19.2; 15–39 32.0; 40+ **63.7**. That drives the S/M/L/XL tiers.
  - *Everything is a range, never a number.* Measured p90 ÷ median is 3.4 for build work and
    3.1 for research, so a point estimate is wrong by a factor of three in the ordinary case
    and reads as precision.
  - *Opus 5 and Opus 4.8 are pooled, and the data says to.* Within the 30–80 tool-call band
    their medians are 10.5 and 11.2 minutes — a gap smaller than the spread inside either, so
    separate tables would imply precision the corpus does not carry.
  - *Wave arithmetic, from 253 real overlapping clusters.* Wall-clock ÷ slowest member is 1.05
    at the median and 1.8 at p90; speedup over serial is 2.2× median and 4.0× p90; peak
    concurrency actually reached was median 5, p90 10, max 16. Above 8 members the
    slowest-member property degrades to 1.55, and a wave that large widens its own upper bound
    and says so.
- **No schedule may beat what was observed.** Twenty items across eight slots can be
  arithmetically fast; it has never happened, so the wave estimator holds its low bound to the
  4.0× measured ceiling rather than to perfect packing. A randomised audit over 500 trials
  caught a real defect before release: rounding a low bound *down* by half a minute produced a
  4.03× schedule, fractionally faster than the ceiling it had just been held to. Bounds now
  round away from optimism, and the self-test checks every wave size from 1 to 60 rather than
  one.
- **Three artifacts from one gated ledger.** `ledger.json` is the source and the other two
  render from it, which is what stops the presentable half drifting from the gated half.
  `reckoning.md` keeps everything and grows per-wave item tables with each tier and the basis
  for it, the dependency edges with their provenance, and the rows excluded from scheduling.
  `reckoning.html` is new: one self-contained page, no build step and no external assets, with
  shipped features beside remaining ones, the waves between them with sub-tasks nested under
  the item that cites them, and the caveats placed where a reader hits them rather than in a
  footnote. `--no-html` skips it; `--max-concurrency` sets the slots.
- **The gate covers the schedule too.** An item in two waves, an item in none, a scheduled id
  that is not work in the ledger, a total that is not the sum of its waves, an inverted bound,
  a tier outside the table, or a duration attached to corroboration all fail it. A board that
  disagrees with the rows it was built from is this tool's own failure mode arriving through
  its presentation layer. A ledger written before the schedule existed still passes, because
  refusing there would report the ledger's age as a defect in the project.
- **Wall-clock includes waiting and carries no failure rate**, and both reports say so where a
  reader meets a number. A unit that ran forty minutes and produced work later rejected counts
  the same as one that landed: these answer how long an agent will be busy, not how long until
  the work is accepted.
- Nine skill cross-references in reckon's SKILL.md qualified to `plugin:skill` — the file was
  missed by the sweep below.
- `plugins/reckon/.claude-plugin/plugin.json` reaches 1.9.0, which also closes a mismatch the
  marketplace manifest had carried alone: it named reckon 1.9.0 while the plugin still said
  1.8.0, and `build-catalogue.mjs` fails on exactly that. The gate stops at its first finding,
  so it is worth enumerating the rest rather than reading one line as the whole answer.

### All plugins: skill names written in full, `plugin:skill`

- **Every skill name in a prompt or cross-reference now carries its `plugin:skill` form.** The
  Skill tool resolves that and nothing else, so a bare name fails with `Unknown skill` and the
  runner continues without the skill it was told to use. Nothing raises an error to anyone.
- **Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
  a 68% failure rate.**
  - *Bare names, 27 failures.* `ship-feature` alone was 17, tracing to one line of ship-fleet's
    SKILL.md telling a conductor its runner prompt should invoke `ship-feature`. ship-feature's
    own stage list had five more, so a runner that guessed the qualified form would still have
    hit `Unknown skill: triage` at stage 1 — the pipeline was unreachable from its first step.
  - *Invented prefixes, 4 failures.* `plugin:agent-voice:agent-voice`,
    `fledgeling-plugins:ship-feature`. Agents that knew a prefix was needed guessed the
    marketplace name or the literal word `plugin:`; omitting it leaves the right form
    undiscoverable rather than merely absent.
  - *Correctly-formed names for skills that no longer exist, 13 failures.*
    `create-test-suite:create-test-suite` failed 10 times against a skill in neither
    marketplace; `goal-harness` is now `better-goal`; `mac-studio-dossier` exists nowhere.
    Left in place and flagged rather than repointed at a plausible successor.
- Prose is treated the same as imperatives: a model acting on "the `whats-left` skill" fails
  exactly as one told "Invoke `whats-left`". Records are left alone — changelog entries,
  eval-run answers and committed research reports say what was written at the time.
- 108 references qualified across 80 files, plus four stage invocations carrying an `<ID>`
  argument. 21 plugins bumped a patch version.

## 2026-08-27

### create-luke-content 3.0.0: empirical B2B copywriting craft layer under marketing route

- **Rebuilt marketing route on empirical research**: Bundled a 208-source, 232k-character
  copywriting evidence base from a 4-backend Dossier deep-research panel (OpenAI gpt-5.6-sol,
  Perplexity, Gemini, Claude Code). Replaced the predecessor's single consumer parenting-app
  basis with B2B SaaS artifact schemas for announcements, landing pages, release notes, and
  campaign emails.
- **Outcome and mechanism pairing**: Replaced generic benefit-before-feature dogma with
  paired outcome and causal mechanism in the opening message unit; enforced voluntary
  two-sided limitation disclosures and preserved specialist domain terminology.
- **Activated voice-lint configuration**: Shipped `voice-lint.json` to activate Australian
  spelling, stylometric comparison, and hard failures on self-narrating meta-labels.
- **Proven with evals & blind quality panel**: 98.2% structural assertion pass rate (54/55);
  20 to 7 blind judge panel win across OpenAI, xAI, and Claude; unanimous flip on Eval 7
  after schedule accuracy constraint was added.
- **Brand package**: Tahoe gel-glass icon ("Voice over craft") passing `audit_sheet.py check`
  at exit 0; composed HTML retina banner rendered at 3200x1040.

### reckon 1.8.0 · test-campaign 0.15.0: a stated ceiling is not a gap

- **`EVIDENCE_CEILING` in reckon, and `limited` admitted to test-campaign's
  `REQ_EVIDENCE`.** A requirement whose subject no harness can watch — somebody looked,
  recorded what cannot be observed from here, and said when that would change — was
  reaching `unmeasured` and being explained to every reader as *"the project's own
  account of itself"*. It is neither a self-report nor the absence of a look, and
  collapsing it into either destroys the distinction the word exists to make.
- **reckon's own source has been carrying the evidence for this.** The `else` branch it
  falls through recorded that `REQ-072` in one repository carries `inconclusive`, a
  ceiling recorded deliberately, and that the pre-fix branch told every reader it was a
  self-report. Both words are now in the bucket.
- **A ceiling earns `waived` only when the decision is on the row** — a reason and a
  horizon of at least 24 characters each, the floor `test-campaign`'s own limit checks
  already use. Without them it stays `unmeasured` and says exactly how short it fell,
  because a bare `limited` would otherwise be a free pass out of the work count. Four
  new selftest assertions cover both sides plus the two readings that must not occur.
- **The unclassifiable-word fixture had to move.** It used `inconclusive`, which is now
  classified; a word the tool has learned cannot go on standing for one it has never
  heard of, so that assertion now uses a word that is still unclassifiable.
- **Why it changed:** the `warden` repository declared `limited` on two requirements
  under its WAR-0048 / WAR-0052 work, and both tools refused the word — `campaign.py` at
  the `add` path and `reckon` at exit 4 — so the rows survived only because they were
  written into `inventory.json` directly. Admitting the word closes that hole rather than
  widening it: such a row is now validated like any other. Measured against that
  repository, `REQ-003` moves from `unmeasured` to `waived` and `reckon check` goes from
  exit 4 to exit 0.

## 2026-08-26

### launch-craft 0.1.0: end-to-end product synthesis & interactive launch conductor

- **New plugin for full-lifecycle launch delivery**: Takes raw brief files in
  `docs/features-to-triage/`, mock HTML, and application code, executing a 4-phase
  pipeline to produce updated documentation and a high-craft launch marketing site.
- **Phase 1: Gemini 3.7 Flash High synthesis via agy**: Aggregates codebase intelligence
  into trace-verified `OVERVIEW.md` and `PRD.md` with 100% brief requirement mapping.
- **Phase 2: Grounded positioning & authentic Luke Rhodes voice**: Targeted to home network
  administrators and gamers, incorporating Mobbin MCP flow patterns and `/trawl` ideation,
  with dual pricing ($9.99 perpetual BYOK vs $4.99/mo SaaS) and 0 em dashes in copy.
- **Phase 3: Interactive marketing site via /design-craft & /ux-craft**: Authoring an
  engaging site featuring a Three.js 3D hero telemetry canvas, GSAP scroll timelines,
  interactive mock UI slices (packet filtering, latency sliders, ROI calculator), and
  explicit 5-platform support badges (Windows, Mac, iPad, iPhone, Linux).
- **Phase 4: Deterministic quality gates**: Validated with `validate_site.py` for WCAG
  contrast, em-dash compliance, and multi-platform presence.
- **Brand asset suite**: Telemetry Gantry icon across 1024, 256, 128 raster renders,
  layered SVG master, and 3200x1040 launch banner with `audit_sheet.py` and `banner_sheet.py`
  checks exiting 0.

All four entries below come from one instrumented run — 122 tickets, 891 agents,
147 workflows over two days — measured afterwards rather than recalled. The
evidence is `~/Dev/dAIolog/docs/retro-2026-08-26/`.

### defer 1.3.0 → 1.4.0: a second bench, and the value lane it freed

- **DeepSWE 1.1 is now a first-class evidence source** (`EXTERNAL_BENCH`), beside
  `diolog-swe-bench`. They answer different questions and are kept apart: the local
  matrix grades eleven work *shapes* head-to-head and is what the shape gate reads;
  DeepSWE grades 113 tasks with a measured **cost per task** across eighteen models,
  which is the number the local bench is worst at. **Only the relative ordering
  transfers** — `sol@max` is $6.46 a task on one and $0.47 on the other.
- **`gpt-5.6-luna@max` gets a lane.** It sat in `DECLINED` as *dominated and dearer*,
  and half of that was wrong: DeepSWE measures 67% ±4 for **$0.61 a task** — the same
  score as `grok-4.6@xhigh` to within both error bars at 11% of the cost, and two
  points ahead of `gemini-3.7-flash` at under a third. The capability half survives
  (`sol@max` is 73% and genuinely ahead), so the `DECLINED` entry is kept with the
  cost half marked superseded rather than deleted. `bench_key` stays `None`: the local
  matrix has no honest row for it, and borrowing one is how a lane acquires a grade it
  never earned. **Probed 2026-08-26 and answering** — the lane ships observed rather
  than assumed, and the selftest now refuses a lane with no probe date.
- **gemini drops behind glm, grok and sol on every class**, and carries a 12-point
  `DELIVERY_PENALTY` applied before the equivalence filter. Deliberately *not* a
  capability score — it failed 8 of 12 autonomous-builder dispatches and produced one
  fabricated completion report, and a bench cannot see that because a fabricated
  report grades as a delivered artefact. The entry names its measurement and the
  condition for lifting it.
- **`PREFERENCE_ORDER` runs last**, only between lanes already agreed equivalent on
  the measured number, so policy never overrules a lane that is better at the shape in
  front of it.
- **New: opus does not need `xhigh` for everything.** Effort buys thinking tokens —
  terra at `max` and `medium` bill at the same rate and differ 4.8× on the bill — with
  a table of when to drop, and an explicit refusal to drop it on the judgement classes,
  where verify rejected three of three ready-to-verify claims.
- `CODEX_LANES` and `TIER1` became derivations after a literal silently omitted the new
  lane. Three selftest assertions changed *with* the policy rather than around it.

### ship-fleet 2.8.0 → 2.9.0: paste the guardrails, and stop barriering the wave

- **The context contract now says paste, not reference.** The project `CLAUDE.md` was
  injected into **0 of 409 subagent contexts**; 69 briefs told a runner to read it and
  **3 did**. The control that makes this a finding rather than a counting artefact: 3
  of 49 *parent* transcripts do carry the block, so a transcript records it when
  present. A table splits what must be inlined as text from what may go by path.
- **Five concurrent agents is a correctness limit, not a throughput preference.** 92
  agents died silently, 88 at exactly 180.0s, with `error_rows` at 0 across all 147
  journals. Corroborated externally: accuracy peaks near five and timeout errors climb
  from ~3 to 50 after it.
- **Derive failure from `started − results`**, and group starts by item key — a retry
  appears as a fresh start with no error and is otherwise invisible.
- **Assert that a fan-out fanned out.** Seven runs delivered a speedup of exactly 1.00
  and nothing noticed. `sum(durations) ÷ wall clock` under 1.2 is a defect.
- **Verify per item via `pipeline()`.** Phase 5 is 42.6 of 54.3 agent-hours; an
  independent study puts 17.6–35.1% on this change, and nothing when queues are shallow.

### stocktake 0.7.0 → 0.8.0: the failure mode is a gate that never runs

On a sweep that graded 53 cards and banked 32 warrant rows, `gates.py` was invoked
**once, with `--help`** — all six gate points unchecked, `warrant_column.py` never
called while the ledger it reads was written to, and the sweep reported success. The
same run measured stocktake at **57.2% deciding and 0.6% gating**, which is why. The
close-out now names the command, requires the exit code to be reported, and says
plainly that a gate nobody read and a gate that passed serialise identically — seven
of the nine checks that "never failed" in that window never failed because nothing
read them.

### warrant 0.3.0 → 0.3.1: the most-failed invocation in the toolkit

**19 of 46** real `snapshot_evidence.py` calls produced no snapshot, across **30
agents**, and the documented flags were never the problem: an invented flag, or a
script path that does not resolve from the agent's own working directory. The fix is
to resolve the absolute path once in the conductor and pass it down, because a spawned
agent does not reliably inherit `CLAUDE_PLUGIN_ROOT`. The three most commonly invented
flags are named so the next agent recognises its own mistake.

## 2026-08-24

### reckon 1.3.0 → 1.4.0: scope-narrowing trap defense and recursive brief discovery

Learnings from the Scrim `Google Drive Fixes` session: when a broad architectural brief
(e.g. multi-backend dual-mode serving, background daemons, cross-platform targets) is narrowed
during triage to in-tree model mocks, unit tests pass and test-campaign passes. Reckon now detects
the scope-narrowing trap, retaining unfulfilled outer intent in `undecided` or `unbuilt` rather than
retiring full briefs on in-tree mock test evidence alone.

- **Recursive & Consumed Brief Discovery**: `read_briefs` now recursively crawls subdirectories
  (e.g. `consumed/`, `archived/`) and treats historical scaffolding briefs as declared `waived/consumed`,
  preventing pollution of unjoined queues.
- **Direct Whats-Left Handoff**: Formalized the emission pipeline so `ledger.json`'s `undecided`
  rows, `unmeasured` blocker clusters, and `unbuilt`/`broken` rows map directly into `whats-left`.
- **Opus 5 Prompting & Migration**: Updated instructions with calm trigger language, explicit task
  scoping, length calibration without filler, subagent delegation caps (join review >150 files only),
  and removal of over-verification scaffolding.

### whats-left 0.2.0 → 0.3.0: full-stack capability completeness & direct reckon ingestion

- **Full-Vertical Capability Stack**: Upgraded survey discipline across five distinct rungs (UI on-glass
  vs HTML mock, in-tree logic vs runtime controllers, standalone background daemons/binaries, cross-platform
  environments, and live system effect boundaries) to prevent false 100% completion claims when daemons
  or OS integration layers remain unbuilt.
- **Direct Reckon Ingestion**: Added structured ingestion of `docs/reckoning/<date>/ledger.json` (`undecided` →
  questionnaire decisions, `BLOCK-*` clusters → evidence work, `unbuilt`/`broken` → product work).
- **Opus 5 Migration**: Calibrated deliverable length, calm trigger language, and subagent delegation limits.

### ship-fleet 2.7.0 → 2.7.1: reckon verification before declaring backlogs drained

- Added explicit `reckon` verification step to reconcile remaining work against test campaigns and route
  undecided forks to `whats-left` before declaring a backlog drained.

## 2026-08-22

### recover-claude-code 1.0.0 → 1.1.0: the sessions that outlive the terminal

A Ghostty crash took 22 sessions down, and four of them were still running twenty
minutes later — two `busy`, one re-arming a `caffeinate` child to keep the machine
awake. The skill had no step for that, so a recovery would have opened a second
process against the same transcript and the same worktrees. New `kill_orphans.py`
and a new §2 stop them first. The test is the controlling terminal rather than
parentage: every healthy tab is parented to `login`, so "not in my own process
tree" would condemn all of them, while a survivor reports no tty at all. It leaves
a detached session that is working alone unless told otherwise, because Claude
Code runs genuine background sessions the same way.

Stopping a survivor is also what *creates* the recovery: a run inside a live
session holds no interrupted work, and the busy egress session here only entered
the recovery set once its process died. So the order is scan, stop, scan again.

Three silent failures found in the same run, each now covered by the selftest:

- **`tab group 1 of window 1` does not exist on a single-tab window.** Ghostty
  builds the tab group only at two tabs, so the count probe raised `-1719` and
  failed all ten tabs before clicking anything. A missing tab group now reads as
  one tab, and the confirmation polls rather than sleeping a fixed 1.2s.
- **"Owed a result" is not "interrupted".** A long-lived session accumulates
  journals from runs abandoned days earlier; one carried 21, of which 3 belonged
  to the crash, and another 11 of which none did. `--fresh-within` counts a run as
  interrupted only when one of its agents was still writing near the crash, so a
  recovered session is pointed at real work rather than a graveyard.
- **A session driving subagents directly was dropped from the target list.** No
  workflow run means nothing owed, and the filter keyed on runs. One such session
  held six in-flight agents, two planners and a runner among them.

Also: `--include-idle` reopens sessions that were owed nothing, with no prompt and
`CLAUDE_CODE_RESUME_PROMPT` set to a stand-down line, because Claude Code
auto-submits a continue prompt whenever it classifies the restored transcript as an
interrupted turn. That guard is measured rather than assumed: of four idle sessions
reopened this way, two stayed idle and one had the auto-continue fire and record the
stand-down text as its injected turn, which is what the variable is for. The brief now lists every agent that was in flight rather than
only the ones that died loudly — an agent that ended without returning a result
leaves no error anywhere and is the one whose context is most worth promoting. And
a session whose transcript tail carries no `cwd` no longer resolves to `None`: the
value is read from the transcript body, because the project directory name
replaces separators with dashes and `Dev/mcp-router` already contains one.

## 2026-08-21

### email-digest 1.7.0: a block for the research behind the items

Some items exist because a piece of research said they should, and that research
is a different class of thing from the items around it: longer, older than the
week, read for a different reason. It now gets its own block, two tiles across at
260px, set on their own ground so a reader can see at a glance they have left the
list. `research.palette` sets that ground, and it should match wherever the
research is actually published, because a tile that does not resemble the page it
leads to is a worse tile than a plain one.

Two tiles rather than three. Each carries a headline and a sentence of what was
found, and at the three-across width of 168px that sentence sets to four or five
words a line. One reads as an orphan rather than a section, so the gate warns
outside two.

`research:ground` is the new error, and it exists because this block inverts the
usual failure. The tile is dark against a light email, so a dark field delivered
as artwork becomes light text on the email's paper the moment images are blocked,
which is a client default rather than an error state. The ground goes on the cell
where a blocked image cannot take it, everything textual stays live text, and the
check fails a render that leaves either to the image.

The block sits between the middle tier and the tail. Kong et al. found ordering
the tail changes nothing, so that is the last position in the email where
placement is still worth something.

### email-digest 1.6.0: the voice skill writes every word, not the headline only

Step 3 said to route prose to the project's voice skill, and in practice that
meant the subject line and the two featured paragraphs. Everything below them
kept the register of the source it was generated from, so a digest could open in
someone's voice and finish in a changelog's.

The step is now binding across every tier, including the one-line tail, and the
routing table splits by byline: a named person or brand takes their own skill
because the byline is the specification, and `agent-voice` covers the case where
nobody's name is on it.

Two failure modes are recorded with it, because both showed up here. Item copy
drifts technical the further down the list it is written, which is why the tail
is named explicitly rather than left implied. And the lines start rhyming with
each other once one template lands, which a per-item lint cannot see; running
the voice lint over the whole set at once catches it, and it caught two real
repeats in this issue.

### email-digest 1.5.0: the summary reads as a summary

Three bulleted lines read as three items to work through. The same three read as
one block the reader takes in and moves past when the bullets come off, the
linked name carries the weight, and the whole thing sits on a tinted panel with
the issue heading inside it and a rule above the counts.

It deliberately stops short of prose. NN/g measured 67% of readers with zero
fixations on a three-line intro, and that finding indicts prose specifically:
separate short lines are the object the same heatmaps show people reading. So
this changes the register and keeps the shape, and `prose-intro` still gates the
paragraph it would otherwise become.

### email-digest 1.4.3: the featured headline leads its banner

The headline sat under the banner, a full image-height away from the section
heading that introduced it, so the reader met the artwork before they met the
thing it was for. With images blocked it moved again. It now leads, which makes
it the first text in the card in both states.

It is still a text node beside the image rather than the image's alt, for the
reason it always was: the banner's failure modes all land on one element and
take the AI-generated inbox summary with them.

That put two adjacent serif bolds five points apart, reading as one two-line
heading, so the space under each section heading opens from 16-18px to 22-26px.
Space rather than size, because the sizes are the ones the design asked for.

### email-digest 1.4.2: the display weight moves from the issue line to the sections

The issue heading held the 28px display type and the section headings sat under
it as 11px mono eyebrows, which spent the largest thing on the page on the line
a reader already knows the answer to. The two swap: sections take the display
face at 28px, the issue heading becomes a small bold line at 14px.

Level and size are separate claims, so the `h1` stays an `h1` and the outline
stays intact for a screen reader while the eye is sent to the sections instead.
The tail's category headings are unchanged at 11px mono caps, and now read as a
clear third level rather than as a repeat of the second.

### email-digest 1.4.1: a double quote inside a style attribute, and the gate for it

1.4.0's font stacks were written `font-family:"Instrument Sans", ...` and landed
inside `style="..."`. The attribute closes at the first inner quote, the browser
keeps the truncated declaration and discards every one after it, and the whole
email rendered in Times at a size nobody set. Single quotes are valid CSS and
are the fix.

Sixteen checks passed it, `fonts:fallback` among them, because that check reads
the raw text with a regular expression rather than the parsed attribute, so it
saw a well-formed stack where the parser saw a truncated one. Opening the render
is what caught it. `css:quoted-attr` gates it now and is demonstrated firing on
a fixture.

Also spaces the tail's separator with non-breaking spaces, since a plain space
after an inline link collapses against the link box and welds the dot to the
title, and moves the wordmark separator's padding to longhands.

### email-digest 1.4.0: icons where a banner has no room, and one primary action

Routed through `ux-craft` and `design-craft`, which is what the SKILL.md has
asked for since 1.1.0.

**The spotlight row leads with a large icon rather than a banner.** A banner is
a wide crop and a wide crop at 168px is a strip of colour with an illegible
wordmark inside it; an icon is drawn to survive being small. The tail rows carry
the same icon at 24px. This is not the shape NN/g measured badly: that finding
is about a thumbnail beside a paragraph, competing with the text it sits next
to, and an icon four times that size leading a column with its title underneath
is a different object.

The tail points at a 48px derivative rather than the 256px card icon, because
eighteen rows of the latter cost the recipient most of a megabyte to render a
24px square. `email_assets.py --icon <src> --size 24` writes them at about 3KB
each, and `build-catalogue.mjs` now copies any `assets/icon-email-48.png` into
`public/icons/<name>-48.png` alongside the banner derivatives it already copied.

**Two calls to action became one primary and one subordinate on a single row.**
Stacked as separate rows they read as a list of two similar choices, which is
the shape one-primary-action exists to prevent. The item's own page takes the
filled accent, because a digest reader is deciding whether this is worth their
attention rather than deciding to install, and the install route demotes to the
muted foreground with an underline. An accent-coloured link beside an
accent-filled button is two claims on the same emphasis.

**The type is the project's own.** Newsreader, Instrument Sans and IBM Plex Mono
in place of Georgia and the system stack, linked from Google Fonts behind a
downlevel-revealed comment so the Word engine never sees the tag. Gmail ignores
the link entirely, so every stack still ends web-safe: that fallback is what
most Gmail readers actually see, not a formality. Pass stacks through
`brand.fonts`. The masthead now builds its wordmark the way a site header does,
splitting on the middle dot, and the mark goes from 28px to 44px.

Also untracks `site/public/banners/`, which `build-catalogue.mjs` generates from
each plugin's committed derivative and which was being committed twice.

### email-digest 1.3.0: the middle tier is a row, and install is a route

The three spotlight items sat stacked, which spent three full-width bands on the
tier that exists to cost less than the one above it. They are now one row of
three columns: a real table with pixel widths, since Outlook has no flex and no
grid but lays a table out correctly, collapsing to full width under 620px for
the clients that read the media query.

That change made a latent asset problem visible. Banner sources drift off
whatever house ratio a project keeps, and at full width nobody notices; three in
a row align at the top and finish at three different heights, which reads as a
broken layout rather than a mismatched file. `email_assets.py --aspect 1000:325`
conforms them, padding a short banner with the colour of the edge row it is
extending rather than cropping the artwork.

`install` now accepts `{label, url}` alongside the existing command string, and
the link is the better default wherever a route exists: a shell line asks the
reader to copy it into the right window, and a phone cannot act on it at all.

A summary highlight may now be composed of `parts`, so one line can name the
work in plain text and still link each destination it mentions separately. That
is what lets the summary say what the items were *used on* rather than only what
they are, which is the relevance signal the Kong result turns on.

Also corrects three stale references the tier rename left behind in 1.2.0: the
payload reference still documented a `compact` tier and an `iconUrl` that no
longer render, and two gate messages quoted defaults the code had moved off.

### email-digest 1.2.1: the tail separator is a middot, not an em dash

One character, changed because it goes out under a name that does not use em
dashes. The one-line tier separated its title from its summary with `&mdash;`;
it now uses `&middot;`, matching the separator the category-counts line already
carried.

### email-digest 1.2.0: the middle tier carries a banner, not a thumbnail

The compact tier put a square icon beside text, and that is the shape NN/g
tested badly: thumbnails rated less valuable than full-width photography, and a
thumbnail newsletter re-classified as cluttered on re-test. It is replaced by a
`spotlight` tier carrying the same wide banner crop at 360px, which is a
reduction in prominence rather than a change of object.

`scripts/email_assets.py` generates the derivatives, because a 3200px source
banner is not a 600px email banner: the sources in this marketplace average
663KB and the derivatives run 38 to 142KB. `site/scripts/build-catalogue.mjs`
copies any `assets/banner-email-<width>.png` into `public/banners/`, so a
committed derivative is served without a build-time image library.

Defaults are now two featured and three spotlight. The hard error on more than
three banners is downgraded to a warning at six: the rule was wrong about its
own reason, since the clip threshold counts HTML only and banners never pushed
against it.

### email-digest 1.1.0: routing to the skills that already own this surface

1.0.0 shipped without routing to `ux-craft` or `design-craft`, which was a miss
rather than a decision. `ux-craft` names emails among the surfaces it covers,
`create-skill`'s own rules say route rather than reimplement, and the same
pairing had been applied correctly to a research page in the same session.

The cost was concrete. Run against this skill's own 24-item fixture,
`ux-lint.py` found dead CSS the email gate missed: an `outline:none` left on the
featured banner after that element stopped being a link. Fixed here.

Tier decisions now route through `ux-craft`, visual treatment through
`design-craft` with `ux-craft`'s lens on it, and the SKILL.md carries the
division of labour as a table: this skill gates the email medium (clipping,
Word-engine CSS, SVG stripping, dark-mode inversion, image blocking, anchor
failure, tier shape), and `ux-lint.py` gates the reading surface (contrast,
touch targets, link labels, alt). Contrast and touch-target size are removed
from this skill's remit entirely, because implementing them twice would produce
two gates disagreeing about one standard.

Two of `ux-lint.py`'s checks do not transfer to email and are recorded as
not-applicable with the reason rather than suppressed: `no-focus-visible`,
because Gmail's published allowlist has no pseudo-class support so the treatment
cannot render at all, and `state-coverage`, because an email has no states.

### email-digest 1.0.0: a digest that tiers the list instead of trimming it

A digest went out with twenty-four items and came back described as unreadable.
The obvious fix is fewer items, and it is wrong. MailerLite's 317,000 campaigns
and 2.9 billion emails put the twenty-one-or-more-links bucket at the highest
click-to-open rate in the dataset, Campaign Monitor found click rate rising with
link count while expecting the opposite, and the choice-overload meta-analysis
pools across 63 conditions to a mean effect size of virtually zero. The defect is
that every item costs the reader the same effort to evaluate inside about fifty
seconds, with nothing on the page saying where to stop.

So the skill tiers the list and the item count stays whatever it is. The absence
of a cap is asserted as a rule in the linter, because a cap is the first thing
anybody reintroduces from instinct rather than evidence.

The split is not arbitrary either. Kong et al. is the only causal study in a
182-source corpus: featuring relevant items raised their detail-reading from 13%
to 22%, while reordering everything below the featured block did nothing
significant. Prominence earns the investment and ranking the tail does not, which
is exactly a small featured set over a compressed remainder.

Sixteen gate checks, each carrying the class of evidence behind it so a
controlled test and a convention do not fail the same way. It also refuses to
gate a text-to-image ratio: Email on Acid tested against twenty-three spam
filters and found that above 500 characters the ratio does not affect
deliverability, and Badsender files the rule under deliverability myths. One
research backend proposed enforcing it and three rejected it. The gate checks the
email survives with every image stripped instead, which is the constraint that
actually bites.

Four defects were caught during its own construction and are recorded in
EVALS.md, including one the gate missed: the whole email rendered centre-aligned
without anyone writing `text-align:center` once, because the markup that centres
the card cascades into everything inside it. Looking at the render caught it, and
`a11y:alignment` was added afterwards so the next one is caught by machine.

No comparative benchmark was run. EVALS.md opens with that fact rather than
omitting the subject, and names the three tasks that would close it.

The argument behind every rule is published at
https://dossier.fledgeling.app/uniform, and the four research reports are in
`docs/deep-research/`.


### should-compact 0.3.0: the residue floor, corrected, and a check for a gate that never speaks

Recounted against 3,778 transcripts and 1,522 automatic compactions over seven days, on the same
machine the earlier 90-day fit came from.

**The residue is nearly a constant, not affine.** `26,783 + 0.015 x pre` at R² 0.045, with a median
of 31,189 tokens whether the session came in at 180k or 900k. The R² is the finding rather than a
weakness of it: knowing the pre-context tells you almost nothing about the post-context beyond
"roughly 30,000". The earlier fit (`50,958 + 0.117 x pre`) over-predicts this corpus by a median of
52,510 tokens, high across the whole distribution rather than on a tail. Both fits are kept in
`references/evidence.md`, with the reason to prefer the second.

**So the hard-hold floor moves from ~58,000 to ~20,000**, and here it is observed rather than
extrapolated. The automatic corpus contains no small compactions — 0 of 1,522 started below 58,000
— but the 58 manual events reach down to 673. Fourteen of them returned a larger context than they
were given and every one started below 17,757 tokens, while one at 16,534 already shrank. The old
floor was refusing compactions in the 20k-58k band that measurably work: a conservative error, and
the reason it survived four months unnoticed.

**Base rates, which the skill had never stated.** At the moment those 1,522 compactions fired, an
open tool chain was present 4.7% of the time and a skill had loaded within three turns 7.0% of the
time. The 98.07% figure is the share of *holds* attributable to one signal, not a prior that a veto
is warranted, and a scorer reading it as one will manufacture the signal. The seam signals are also
flat — compactions near a skill load had a median pre-context of 266,383 against 267,313 for the
whole corpus — so an early compaction after a skill load is what an evenly-distributed trigger
looks like rather than evidence of a bad seam-picker.

**Read the "median 99.8% of the window" claim as a fraction, never an absolute.** The wall moves: a
proxy that arms `autoCompactWindow` sets it, and the identical trigger against a lower wall put the
median at 267,313 rather than 987,636. A gate that substitutes the hardware window for the
caller-supplied one will read a session at its limit as one with 700k to spare.

**New section: a silent gate is not a gate that agreed.** A `PreCompact` hook that never blocks is
indistinguishable from one that examined every compaction and approved it — both exit 0 and print
nothing. One did exactly that for 1,522 consecutive compactions, because the session fact it
branched on was looked up by an id its caller does not have; its own veto text appears zero times
in 3,778 transcripts. Two outside checks are given, since nothing inside such a gate can detect it,
and the rule generalises: any rule here that depends on a caller supplying a fact can fail the same
way.

### code-review 1.1.0: the sources it was built from, made checkable

An audit of what this skill actually drew on against what it was asked to draw on found two things
missing and one that turned out not to be missing at all.

Six measurements in `references/evidence.md` were marked `M (inherited)`, meaning quoted from a
predecessor with no citation a reader could open. The reports backing them were sitting in this
repository the whole time, under `docs/deep-research/`. They now carry an `R` class naming the
report: the judge-panel result and the automation-bias and evolvability findings to
`code-review-deputy.md`, the agent-authored-commit census and the coverage-ledger census to
`code-review-vacuous.md`, and the lost-agent fan-out measurement to `code-review-workflows.md`.
Exactly one is still inherited, the process-count ceiling behind the 8-shard cap, and the file now
says so rather than leaving a reader to count. The distinction is the whole point of the marker:
`R` can be checked by opening a file, `M (inherited)` cannot be checked at all.

The `debt` lens gained the code-smell baseline from Fowler's *Refactoring* ch.3, adapted from the
two-axis `code-review` skill in `~/Dev/skills`. The lens was structural before this: layering
violations, god objects, duplication, abstraction mismatches. It carried nothing for naming or
coupling, which is half of what makes a diff hard to live with. Twelve named smells now sit under
it, each written as what it is and how to fix it, bound by two rules that stop it becoming a style
cudgel: a documented repo standard always overrides the baseline, and every smell is a labelled
judgement call rather than a violation. That skill's Spec axis was deliberately left behind, since
spec-conformance belongs to `spec-validation` and `shipyard:gap-fix` and a second opinion on it
here would only put two skills in disagreement.

`~/Dev/knowledge-work-plugins/engineering/skills/code-review` was assessed and contributed nothing.
Its dimensions are a strict subset of the security and logic checklists already here, and its
distinctive move is a connector story rather than a deeper review. `evidence.md` records that
assessment so it is not repeated.

## 2026-08-20

### code-review 1.0.0, atlas-publish 2.0.0: the release skill splits, and its review half becomes general

`atlas-publish` shipped inside the Atlas repo, served over its admin MCP connector, in 99 lines. In
those 99 lines it merged branches, decided whether a change could go out over the air or needed a
full App Store build, archived a binary, uploaded it, exported a JavaScript bundle and registered the
result. Every one of those steps can fail quietly, and a procedure that short has no room to say how
you would know.

The case that set the rebuild's shape is `apps/atlas-api/tests/unit/lib/ota-cert-parity.test.ts`. It
checks the public certificate baked into the app against the private signing key held in Vercel, and
it guards its only real comparison behind `it.runIf(!!parityKey)` with a companion asserting
`expect(true).toBe(true)`. With `OTA_CERT_PARITY_KEY` unset the file exits 0 having compared nothing.
That is deliberate in the test, and it keeps a key-less CI run honest. It was not deliberate in the
release skill, which read the green and moved on. Gates now report passed, failed and not-run as
three states, and not-run does not roll up into a pass. The skill is 231 lines with 178 non-empty,
and draft is the last state it writes: publishing to users stays a founder action.

The review half was never about Atlas. It ships as `code-review`, its own plugin, at 381 lines, 298 of them non-empty, over 4,229 lines of depth across 16 reference files opened per phase rather than carried
on every call. Fourteen named angles, a three-verdict verify that keeps a PLAUSIBLE finding with its
confirming step named rather than dropping it, and a coverage ledger that records what was not looked
at. `atlas-code-review` survives as a trigger alias, so the old name still reaches it.

Both are sourced. The research reports behind them are exported to `docs/deep-research/`, so every
citation is readable without leaving the repo, and `references/evidence.md` in each maps each rule to
the report it came from. Neither eval suite has been run, and both `EVALS.md` files open by saying so.

### create-mac-icon 1.5.0, create-skill 1.3.2: the halo every icon was carrying

An icon exported with transparent corners stores RGB (0,0,0) in every fully transparent pixel.
Nothing shows it at 1:1, because alpha is 0. But a browser, a README and the site all downscale it,
and downscaling filters RGB and alpha independently in straight alpha, so that black gets averaged
into the silhouette's edge pixels. The fringe appears only at display size, which is why it survived
every gate this repo has.

`alpha_bleed.py` floods edge colour outward into the transparent region for 24 passes, leaves alpha
untouched, and asserts both invariants before writing. Its offender test is neighbour-relative rather
than an absolute darkness threshold, because `trawl`'s artwork runs near-black right up to the
silhouette and an absolute test called correctly-bled pixels offenders three times running. 105 icon
files across 35 plugins were dirty; all 123 shipped icons now pass `--check` at exit 0. PIL does not
reproduce the artifact, so the proof is in the render path: one banner went from 25 pixels below
luminance 200 to none, and its darkest edge pixel from 191.2 to 231.6.

27 banners were re-rendered. Eighteen moved by 0.027 to 0.107 mean pixel difference, which is the
fringe and nothing else. Three moved a great deal, because their sources reference artwork this
engine will not fetch from a `file://` page, so the render had been failing quietly and every icon
rebuild since had stopped short of the banner. `create-swe-project` had gone past stale and was
carrying the improve-skill design outright. Six had shadows the August engine painted and this one
does not, so each is now a seated element with a plain box-shadow whose alpha is fitted against the
shipped banner rather than copied, landing within 0.62 luminance of it on the shadow band.

Fitting them corrected two things in `render_banner.py`, whose guard had been naming the wrong fix.
An inline SVG `feDropShadow` does not rescue a drop-shadow: the artwork renders and the shadow band
comes out identical to no shadow at all. And box-shadow colour alpha is quantised coarsely, every
value from 0.03 to 0.13 rendering byte-identical while 0.20 differs, so a faint shadow has to be
tuned by blur and negative spread instead. Both are recorded in the guard's own comment with the
date they were measured.

### mockup-fidelity: eval 9 run, and two of its assertions do not bite

The first prompt in the suite to be run rather than defined. With the skill, 9 of 11 assertions;
without it, 2 of 11 — same model on both arms, both blind to the fixture's answer key, graded out
of family with a quoted sentence per assertion. The baseline reached for pixel crops and a read of
the Swift source to settle corner radius and shadow, which is the exact substitution the Tier B
rule refuses.

The two assertions the baseline also passed are recorded as findings about the eval set rather
than as wins, and a third failed on both arms because a headless runner has no proctor tools and
both arms therefore answered on paper. Full table, and the two limits on the run, in
`plugins/mockup-fidelity/EVALS.md`.

### test-campaign 0.8.0, shipyard 0.3.0, ship-feature 2.2.0, ship-fleet 2.2.0: what a picture is of

**The gap.** A campaign built with `test-campaign` 0.7.0 published 20 surface captures and
cleared every gate the plugin owned: `campaign.py check` reported every case accounted for,
`strict-check.py` reported 46 of 49 checked, and both `-glass` lanes were proved, artifact-named
and attach-witnessed. The captures were of three unrelated documents — a project status report,
the mock browser's own index page, and a design accessibility doc. Twenty files held **six
distinct images**; four groups of four were byte-identical. A flow step captioned "Open pairing
QR code sheet" showed a questionnaire about Apple developer credentials.

Nothing was broken, which is the part worth recording. `attach-shots.py` binds a picture to a
surface on a slug of its **filename** — string identity, not evidence. `evidence-page.py`
rendered it with `alt` taken from the label, so a wrong image arrived under a right-sounding
caption. `campaign.py check` ran `inspect_raster` and its shared-artifact detector over
`RASTER_RUNGS` case evidence only, and the `shot` field the page actually renders was inspected
by nothing. **The gated part of the campaign was sound and the ungated part was the part people
look at.**

The prose was already right and unenforced: `attach-shots.py`'s own docstring says a screenshot
filed against the wrong surface "is worse than one filed against none, because it looks right",
and the code guarded only the ambiguous-filename case. A rule stated and not gated is a rule the
next run does not have.

**`test-campaign` gains the plane, borrowed intact from `warrant:oracle`.** That plugin had
solved the same problem one domain over for numbers: a displayed figure without a
`data-source-ref` is the defect its lineage plane exists to find. Substitute *picture* for
*figure* and the apparatus transfers, down to the tick-and-tie step. `capture-lineage.py` runs
four passes, all exact, none needing a model — **unsourced** (no manifest entry, or no recorded
target), **untied** (the target does not resolve to the subject's route), **shared** (two
subjects, one sha256, undeclared), **unjudged** (published with no `be-my-witness` verdict, which
ratchets rather than blocks). `--seed-swap` swaps two subjects and asserts the tie pass goes red,
because a tie check nobody has watched fail is indistinguishable from one that reads nothing.

Determinism is a requirement here rather than a preference. `be-my-witness`'s `prescan.py`
returns `isEvidence: true, settled: true`, exit 0 against the worst capture in that campaign — a
real, contentful, settled image of the wrong document. Image statistics cannot answer the subject
question, and `mockup-fidelity`'s measurement puts frontier vision near 40% recall on
fine-grained UI diffs and under 23% on hard cases. Provenance answers it, and only if it is
recorded while the shutter is open, which is why `capture-pairs.template.mjs` now writes
`captures.json` as it shoots and records the URL the browser *ended up at* rather than the one it
was sent to.

**The rest of the chain, because one gate in a content-blind pipeline moves the hole rather than
closing it.** `campaign.py check` audits published shots and blocks on three new shapes;
`attach-shots.py` refuses a write no manifest corroborates and stamps `shotProvenance` under
`--filename-only`; `evidence-page.py` badges every capture witnessed/manifest/filename and
anchors a flow step on its own id rather than the loop index, which used to renumber every anchor
after a reordered step; `witness-worklist.py` demotes a reference that was never rendered to an
image, which is why that campaign's 20 "judgeable" pairs — every reference an unrendered `.html`,
`evidence/shots/mock/` absent — had produced no verdict and nothing had said so.

**The pipeline gains the same three questions about its own evidence.** `evidence-rules.md`,
canonical for worker, verifier, gap-fix and both conductors, adds: the screenshot-subject rule
with its two exact checks; artifact-forcing from `mockup-fidelity`, as a precondition rather than
an exhortation because agents under effort pressure rationalise the shortcut and models trained
against reward-hacking learn to conceal it; and the cannot-fail scan from `warrant:assay`, where
over half of more than 15,000 generated mutants survived a passing unit, integration and system
suite. `verify` gains structural rule 5, the subject checks on its visual lane, the scan before
it spends a suite's green, and step 3a — a completeness critic reading only the bundle and the
requirement table with the app, the diff and the ticket closed. `work` runs the scan over the
specs it touched before writing its completion record. `ship-fleet` runs the capture gate once
per repo rather than once per item, because a fleet multiplies whatever the evidence layer gets
wrong.

**Evidence.** `capture-lineage.py --gate` against the campaign that produced this exits 2 naming
41 unsourced captures and 6 shared images; `campaign.py check` exits 1 where it exited 0.
`tests/run.sh` covers every new blocker in both directions plus the seeded swap: **33 passed, 0
failed**, 12 of them new. Four evals were added — one per plugin — and **none has been run**;
each plugin's EVALS.md says so rather than folding them into an existing total.

### mockup-fidelity 3.3.0: the fixture that withdrew a claim

3.2.0 shipped eval 9 defined and unrunnable — it asks what a second measurement engine can answer
about a native target, and every fixture in the suite was an HTML file. `evals/fixtures/mac-settings`
is now a real macOS app whose Settings pane diverges from its mock in eight recorded ways, built
Tier B by default so `proctor_inspect` answers `reflectorUnavailable` and the style classes stay
inconclusive.

Its answer key is four-valued, and the fourth outcome is **OVER-CLAIM**: reporting the accent-colour
divergence while at Tier B is a failure rather than a catch, because an eyedropped colour is not a
declared value. A fixture whose only failure mode is missing something cannot test the failure mode
of claiming too much.

**Building it withdrew a claim 3.2.0 had made.** That version asserted `proctor_assert`'s `agree`
catches a control-shaped region with no accessibility node, from the tool's documentation and its
worked example at 96×28. The fixture plants exactly that, and across three runs `agree` produced six
to seven findings and **none was `unexposedControl`** — at 38×22 and again at 96×28 with a label —
while `exists` on the same control returned `found: false` and the capture showed it painted.
`ghostNode`, its mirror image, fired correctly in the same runs. Both reference files now record the
capability as unconfirmed. Stating a capability from documentation before anything exercises it is
the habit this skill exists to break, and it did it.

The fixture also found an unplanted defect in itself: an `NSButton` with a `.rounded` bezel
constrained to 20pt reports `h: 22` in the accessibility tree and paints nothing, which `agree`
correctly called a `ghostNode`.

### mockup-fidelity 3.2.0: the ceiling belonged to the engine

A fidelity report reading zero findings beside nine inconclusive classes was honest and useless. The
classes obscura cannot measure — `boxShadow`, `backgroundImage`, `textTransform`, transitions,
animations, `flex`, pseudo-elements, `getBBox()` — were unmeasured for every target the skill had, and
the reader was left holding a screen nobody could close. **That ceiling belonged to the engine rather
than to the build**, which is the same confusion the skill exists to prevent, arriving one level up.

**A second measurement engine, driving `proctor`.** It covers a native macOS app built to a mock, an
Electron app shipped as a Mac app, a React build inside a Mac web view — and a plain web build whose
divergence sits in a class the browser engine returns `""` for. That last case is why this is a second
engine rather than a native-only lane: a shadow CSSOM reports as an empty string is a `shadowRadius`, a
`shadowOffset` and a `shadowOpacity` on a `CALayer`, and those are readable.

**The lane has its own capability preflight, with two tiers, and the tier is measured rather than
assumed.** `proctor_inspect` returns a resolved hierarchy for an app embedding `ProctorReflector` and
`reflectorUnavailable` for one that does not. Tier B leaves every style class inconclusive with that
reason, because an eyedropped colour is not a declared value. It is not a degraded Tier A that can be
talked up, and the ledger records which set of questions it answered.

**Three questions the browser lane cannot ask at all.** Whether a capture is current — a stale frame is
pixel-identical to a correct one and obscura attaches no signal, where every proctor capture carries
`SCFrameStatus`, `dirtyRectCount`, `framesWaited` and `trustworthy`. Whether an animation is in flight —
`getAnimations()` returns 0 while one runs, and the layer's model and presentation values differ exactly
while it does. And whether a control-shaped region has no accessibility node behind it, which is a
present-in-mock, absent-in-build finding the skill could not previously produce, and which neither a tree
dump nor a screenshot review reaches because each is one observer agreeing with itself.

**`UNSTABLE` becomes the fourth state.** The research behind this skill names four — `MEASURED`,
`UNAVAILABLE`, `UNSTABLE`, `ERROR` — and three were implemented. A 2026 study of 262 web
visual-flakiness cases split them 59.9% structure-related and 40.1% style-related, so a value that will
not hold still is a classification rather than noise to tolerate away. `proctor_stability` measures it,
and its variance is where a defensible geometry tolerance comes from: every assertion kind defaults
`tolerance` to 1.0, and the research is explicit that a numeric tolerance is defensible only after
repeated-run measurement proves non-zero variance.

The capability facts live in `engine-capability-matrix.md` rather than in the new file, because that is
their single home and six copies of one paragraph is how nine classes stayed hidden for nine versions.
Eval 9 was added and **cannot be run against the current fixtures** — its target is a running Mac app
rather than an HTML file — which `EVALS.md` states rather than leaving to be found later.

## 2026-08-19

### warrant 0.2.0, test-campaign 0.7.0, shipyard 0.2.0, ship-feature 2.1.0, ship-fleet 2.1.0: the oracle gap

**The gap.** `warrant` and `test-campaign` did not reference each other — `grep` both ways
returned nothing — so neither could produce or consume the other's state. A repository could hold
a mature campaign and a tier-0 warrant at the same time, permanently, with each tool correct on
its own terms.

Found by running the pipeline for real rather than by reading it. A `warrant:lot` audit of a
211-item Done column returned **143 items unverifiable in either direction**, and nothing in
either plugin could say why or what to do next. Two failures were arriving as one status, and the
corpus behind `warrant` had already named the distinction: a screenshot-judging pass over fifty
surfaces returned inconclusive on all fifty, "stated each time as being for want of a judge
rather than for want of an oracle". Want of a judge is an authority gap and `warrant` is the
instrument; want of an oracle is a coverage gap and `test-campaign` is. Neither skill asked which
it faced.

**`test-campaign` gains the status and the remedy.** `unoracled` splits from `inconclusive`,
because the two look identical and want opposite fixes — a better instrument, or a specification
that names something checkable. Phase 6a builds the missing oracle down a four-rung ladder
(specification-sourced outcome assertion → metamorphic relation → property-based invariant →
recorded permanent limit), with `references/oracle-construction.md` behind it. Metamorphic
relations are the standard answer to the oracle problem; the reference states that the evidence
for them is directional rather than sized.

**The bridge existed and was unwired.** `charter_validate.py` already documented the two files it
reads and `rollup_classes.py` already existed to map surfaces onto defect classes. What was
missing was anything writing them. `campaign.py export-warrant` now does, from numbers the
campaign already held — the armed ratio, and the effect-rung count per surface. The first cut
keyed coverage by surface id, which matched no glob and rolled up to zero on every class,
indistinguishable from a campaign that measured nothing; caught by running the chain rather than
by reading the schema, and it now emits the row shape `rollup_classes.py` consumes.

**`warrant` stops permitting the order it calls forced.** `lot_plan.py` exits 3 without
`.warrant/suite-health.json`, naming `assay`. The rule was in the skill's prose and enforced
nowhere: the run that prompted all of this skipped `oracle` and `assay`, went straight to
`panel` over 219 positions, passed every gate, and then measured its own reviewer at 2-of-8 seed
recall — the number the skipped plane exists to predict. `lot_report.py` gains a sixth required
field, the oracle mix of the sampled items, and says so when nothing in a sample stands on a rung
that asserts an effect. `ratchet.py` emits the surfaces, the file and the commands that would
clear a refusal, turning a permanent tier-0 into a finite task list.

**The delivery ladder stops building unauditable columns.** `shipyard:verify` types each
requirement's evidence by its oracle rung and puts it in the verdict table; a requirement proved
only by a weak rung reads `Unverified` rather than `Done`, and a new terminal shape
`Unverified — no oracle` cannot reach Done at all. `ship-feature` routes phase 6 to
`test-campaign` where installed and sends a no-oracle requirement back to phase 6 rather than to
gap-fix, which closes a different kind of gap. `ship-fleet` carries the oracle mix across the run
and exports to the warrant once at the end.

**What none of it fixes.** `C1` still bounds everything: no powered non-inferiority reader study
exists for code review or UI acceptance, so there is no measured human baseline and no amount of
test construction creates one. Tier 3 also stays out of reach in the near term — 200 items closed
in a class with zero escapes over 90 days is a volume-and-time requirement, not an evidence one.
These changes make tiers 1 and 2 earnable, which they previously were not.

Analysis and the six proposals it came from: `docs/oracle-gap-warrant-test-campaign.md`.

### create-skill 1.3.1, create-mac-icon 1.4.1, stocktake 0.2.1: patch bumps the rename earned

Three plugins carried content changes across the `create-test-suite` to `test-campaign` rename and the conformance pass without their versions moving. `stocktake` matters most of the three: its SKILL.md and `references/testing-adequacy.md` route to the skill by name, so the old name there was a dangling reference rather than stale prose. `create-skill`'s `references/brand-and-docs.md` and `scripts/banner_sheet.py` and `create-mac-icon`'s `references/material-recipes.md` cite it as a worked example. Nothing behavioural moved in any of the three.

### create-test-suite → test-campaign, 0.4.0 → 0.5.0: the suite that never ran, and the rung that let it pass

**Renamed.** `create-` implied a one-shot generator and "suite" named the smallest of the things the skill leaves behind. It sets the test strategy, decides what a given run needs to cover, keeps the suite alive across runs, and publishes the evidence — and `campaign` was already the word the code used throughout (`campaign.py`, `docs/test-campaign/`, `CASE-0001`). Put to gemini-3.7-flash-high and grok-4.6 with the candidates in swapped order; both landed on the campaign noun and split only on whether to keep a `test-` prefix. The old name stays in the entries above, because rewriting history is worse than a stale name in it.

**A third failure mode, and it is the worst of the three.** A campaign reported 100% checked, 22 armed cases and 59 passing tests across a macOS app and a Windows app. No GUI process had ever attached to a window server: the Swift half initialised SwiftUI view structs in memory, which are value types and render nothing; the Windows half was C# that had never been compiled; the screenshots came from an HTML mock photographed in a browser. Every individual number was true, and nothing in the ledger could catch it, because the ledger only ever asked whether cases *resolved*. The generalisation is not a desktop problem — jsdom puts layout "outside the scope of jsdom" and returns "zeros for many layout-related properties", so a geometry assertion there compares zero against zero and agrees.

**`visual` split into `structural-visual` and `raster-visual`.** One word was covering both "a label exists in the view hierarchy" and "pixels arrived from a compositor", and the first is a data-model check. A case asserting a card's title property equalled `"AGGREGATE CPU"` claimed the visual rung, counted as proof of an effect, and was watched to fail — honestly, and about a struct in memory. Only `raster-visual` buys effect credit now. Existing campaigns keep loading and are told to migrate rather than silently re-rated, and because this makes real scores fall, `strict-check.py` now refuses to lower its ratchet without a recorded reason.

**A lane has to prove it ran.** A lane named `*-glass` claims the app was running and drawn, and `campaign.py lane` makes it name the built artifact as a path that exists, the command that produced it, and what witnessed a process reaching a display server. `--cannot-attach "<reason>"` is the honest alternative and drops the lane's cases to `blocked`. Pixel claims are checked from the bytes: a non-image, a zero-byte file, a placeholder, or two cases sharing one screenshot byte for byte all fail. What it deliberately does not do is score the picture — no density or entropy floor separates a failed capture from a legitimately sparse screen, since an empty state is mostly background by design.

**`inconclusive` and `blocked` as first-class blocking statuses.** Where an engine returns nothing, `"" === ""` is true and vacuously certifies that two layouts are identical. "We do not know" is a weaker claim than "no difference found" and a different one from "does not apply here", so they get separate states and `check` prints its own population: `6/8 cases produced a measurement · 2 could not be measured`.

**Sweeps K and L, and native desktop lanes for Windows and Linux.** Desktop shell invariants (scaling, window limits, popover anchoring, a theme toggled mid-run, occlusion) and live process/IPC chaos (peer dies, peer returns, privilege separation, startup order). Both are justified by structure rather than by yield, and say so — no formal measurement of scaling-induced layout defects exists, which was searched for and reported missing. The lane matrix gained Windows and Linux from a commissioned research pass, after a sweep of 452 existing reports found nothing usable on either. Highlights: `SendInput` fails under Windows UIPI and, per Microsoft's own reference, *"neither GetLastError nor the return value will indicate the failure was caused by UIPI blocking"*; Windows has no per-frame validity signal at all, so black frames from minimised, off-desktop, capture-excluded and hybrid-GPU cases are indistinguishable from the image; deep UIA enumeration in WinUI 3 can raise a native `0xc0000005`; Wayland's portal raises a consent dialog that halts an unattended run; and a hosted `windows-latest` runner defaults to 1024×768, which clips layouts and looks like a build defect.

Four detector defects added (11–14), the research disagreement over SSIM-as-verdict recorded rather than resolved in the skill's favour, and gemini.md's fourteen hard line-number pointers into `SKILL.md` converted to text anchors, since a line reference breaks silently on every edit — which is the failure class the skill catalogues.

### mac-craft 1.2.0, mac-design-digest 1.2.0: the corpus stops being optional, and ships

**The gap.** `mac-craft` listed the live corpus under *External, if installed* with the words
"prefer it when present", and a real design run never looked. It built a macOS mock from the
bundled snapshots while a 135-app corpus sat unread on the same machine. The cost was not
abstract: on first read that corpus caught a canon violation the mock had shipped through three
review rounds — two accent fills on one screen, against the *single-accent economy* rule its
`TASTE.md` evidences across 15 apps and names in its tells table as selection-grammar drift.
An optional dependency phrased as a preference is one nobody loads.

**The fix is a lookup, not a reminder.** Corpus resolution is now the first block of
`mac-craft`'s Knowledge sources, ahead of its own bundled references: `./design-corpus/` first,
then `plugins/mac-design-digest/corpus/`, then absent — and absent is stated in the delivery
rather than passed over. Four things get loaded and no more (`TASTE.md`, the one cluster whose
audience matches the brief, the 1–2 profiles that cluster names under *Read for depth*, the
`patterns/` entries for the surfaces being drawn), and the chosen cluster and its runner-up are
named in the delivery beside the direction. `mac-design-digest` already specified that handoff
from its side; the pull was what was missing.

**The corpus ships with the marketplace.** 135 apps, 209 surfaces, the macOS 27 kit, nine style
clusters and the pattern entries, at `plugins/mac-design-digest/corpus/`. Screenshots are
resized to a 1600px long edge and re-encoded WebP q80, which takes 132MB to 16MB;
`sources/_scale-manifest.tsv` records every original dimension and its scale factor, because the
corpus's `(measured)` marks are pixel reads and a resize without a recorded scale silently
invalidates them.

**It ships with its own gate red, and that is stated rather than fixed.** `corpus_check.py`
returns 330 failures on the migrated corpus and the identical 330 on the source, so the
migration is faithful and the failures predate it. All 330 are `lineage-gate` on `ICONS.md` —
icon canon rules citing apps whose profiles record `unknown` or `web-electron` lineage, which is
exactly the contamination that check exists to catch. Repairing them is a corpus-editing job with
its own evidence requirements, not a side effect of a move.

### create-skill 1.3.1, create-mac-icon 1.4.1, stocktake 0.2.1: patch bumps the rename earned

Three plugins carried content changes across the `create-test-suite` to `test-campaign` rename and the conformance pass without their versions moving. `stocktake` matters most of the three: its SKILL.md and `references/testing-adequacy.md` route to the skill by name, so the old name there was a dangling reference rather than stale prose. `create-skill`'s `references/brand-and-docs.md` and `scripts/banner_sheet.py` and `create-mac-icon`'s `references/material-recipes.md` cite it as a worked example. Nothing behavioural moved in any of the three.

### create-test-suite → test-campaign, 0.4.0 → 0.5.0: the suite that never ran, and the rung that let it pass

**Renamed.** `create-` implied a one-shot generator and "suite" named the smallest of the things the skill leaves behind. It sets the test strategy, decides what a given run needs to cover, keeps the suite alive across runs, and publishes the evidence — and `campaign` was already the word the code used throughout (`campaign.py`, `docs/test-campaign/`, `CASE-0001`). Put to gemini-3.7-flash-high and grok-4.6 with the candidates in swapped order; both landed on the campaign noun and split only on whether to keep a `test-` prefix. The old name stays in the entries above, because rewriting history is worse than a stale name in it.

**A third failure mode, and it is the worst of the three.** A campaign reported 100% checked, 22 armed cases and 59 passing tests across a macOS app and a Windows app. No GUI process had ever attached to a window server: the Swift half initialised SwiftUI view structs in memory, which are value types and render nothing; the Windows half was C# that had never been compiled; the screenshots came from an HTML mock photographed in a browser. Every individual number was true, and nothing in the ledger could catch it, because the ledger only ever asked whether cases *resolved*. The generalisation is not a desktop problem — jsdom puts layout "outside the scope of jsdom" and returns "zeros for many layout-related properties", so a geometry assertion there compares zero against zero and agrees.

**`visual` split into `structural-visual` and `raster-visual`.** One word was covering both "a label exists in the view hierarchy" and "pixels arrived from a compositor", and the first is a data-model check. A case asserting a card's title property equalled `"AGGREGATE CPU"` claimed the visual rung, counted as proof of an effect, and was watched to fail — honestly, and about a struct in memory. Only `raster-visual` buys effect credit now. Existing campaigns keep loading and are told to migrate rather than silently re-rated, and because this makes real scores fall, `strict-check.py` now refuses to lower its ratchet without a recorded reason.

**A lane has to prove it ran.** A lane named `*-glass` claims the app was running and drawn, and `campaign.py lane` makes it name the built artifact as a path that exists, the command that produced it, and what witnessed a process reaching a display server. `--cannot-attach "<reason>"` is the honest alternative and drops the lane's cases to `blocked`. Pixel claims are checked from the bytes: a non-image, a zero-byte file, a placeholder, or two cases sharing one screenshot byte for byte all fail. What it deliberately does not do is score the picture — no density or entropy floor separates a failed capture from a legitimately sparse screen, since an empty state is mostly background by design.

**`inconclusive` and `blocked` as first-class blocking statuses.** Where an engine returns nothing, `"" === ""` is true and vacuously certifies that two layouts are identical. "We do not know" is a weaker claim than "no difference found" and a different one from "does not apply here", so they get separate states and `check` prints its own population: `6/8 cases produced a measurement · 2 could not be measured`.

**Sweeps K and L, and native desktop lanes for Windows and Linux.** Desktop shell invariants (scaling, window limits, popover anchoring, a theme toggled mid-run, occlusion) and live process/IPC chaos (peer dies, peer returns, privilege separation, startup order). Both are justified by structure rather than by yield, and say so — no formal measurement of scaling-induced layout defects exists, which was searched for and reported missing. The lane matrix gained Windows and Linux from a commissioned research pass, after a sweep of 452 existing reports found nothing usable on either. Highlights: `SendInput` fails under Windows UIPI and, per Microsoft's own reference, *"neither GetLastError nor the return value will indicate the failure was caused by UIPI blocking"*; Windows has no per-frame validity signal at all, so black frames from minimised, off-desktop, capture-excluded and hybrid-GPU cases are indistinguishable from the image; deep UIA enumeration in WinUI 3 can raise a native `0xc0000005`; Wayland's portal raises a consent dialog that halts an unattended run; and a hosted `windows-latest` runner defaults to 1024×768, which clips layouts and looks like a build defect.

Four detector defects added (11–14), the research disagreement over SSIM-as-verdict recorded rather than resolved in the skill's favour, and gemini.md's fourteen hard line-number pointers into `SKILL.md` converted to text anchors, since a line reference breaks silently on every edit — which is the failure class the skill catalogues.


## 2026-08-18

### create-test-suite 0.2.0 → 0.3.0: unchecked is failed, and the screenshots were never attached

Four changes, all from running the skill against a large monorepo and then against eleven other campaigns on disk.

**A definition of done that a pass cannot slip through.** `campaign.py check` asks whether every case is accounted for, and a campaign can clear it with 187 passes that were never watched fail and prove only that an element exists. The skill now states the stricter bar in its own terms — a case is CHECKED only if it passes, was watched to fail, and asserts an effect — and `strict-check.py` reports it. Two real campaigns the same day scored 62 of 70 and 20 of 262, so the bar is reachable and a low score is a fact about the campaign. It ratchets rather than gating on 100% immediately, because a gate that opens 97% red is switched off inside a week. The one honest route to a higher number is checking more things, and the section says so: raising it by weakening an assertion, dropping a rung or marking a reachable case `n/a` raises the score and lowers what the suite knows.

**Arming that scales.** Arming cases by hand does not survive a generated family of 83 surfaces sharing one predicate, and marking them all armed from one observation claims a uniformity nobody measured. Phase 6 now shows the sweep running its own positive control inline, first, every run — plant the defect, require it to fire, then measure. On the campaign that prompted this it took armed from 12 of 187 to 107, in two edits.

**`attach-shots.py`, because the evidence pages were empty beside their evidence.** A surface gains a wall cell only when its inventory entry names a `shot`, and nothing ever wrote one. Measured across twelve campaigns: one had 22 surfaces, 22 PNGs on disk and zero attached, and its page rendered no images at all. The script wires them by id and then by an unambiguous lane-plus-keyword match, refusing to guess where two surfaces both fit, and prints images that matched no surface alongside surfaces that got no image. `evidence-page.py` now refuses to render that silently too: where images exist unattached it says so instead of "no captures yet".

**`capture-pairs.template.mjs` and `witness-worklist.py`, so the mock comparison happens at all.** Phase 8 reads the DOM and cannot see what a person sees; `be-my-witness` can, but needs a shot and a reference. Eleven of twelve campaigns had captured no mock. The template photographs both halves at the same viewport and settle and records them, because a difference the capture caused is read as design drift by whatever judges it, and the worklist counts surfaces that cannot be judged rather than letting an uncompared surface pass for a compared one.


### agent-voice 0.1.0 → 0.1.1: how to make it the default rather than an option

Documentation only; the skill and its lint are unchanged. Installing the plugin makes the skill available, and the README stopped there — so the routing decision was left to whoever happened to remember the skill existed mid-task. The new *Making it the default* section carries a pasteable prompt that puts the routing in a user-scoped `CLAUDE.md` or `AGENTS.md`, where it loads before the first reply of a session rather than halfway through one.

- **The routing is by authorship, not by format.** The agent as author takes agent-voice, including chat replies, and that is the default whenever no voice or persona is named; a named person or brand takes their own content skill, and content published under their name takes their voice even when the request never names it. One skill per piece, a named voice wins, and a request spanning both is two pieces.
- **A probe, because a global instruction file that failed to load looks exactly like one being followed.** The prompt adds an agreed emoji at the front of every chat response, excluded from files, commits, PR bodies and anything written for another agent. A missing emoji on the next reply is the signal. The exclusion is what makes it a probe rather than a decoration: it also tests whether the session distinguishes a conversation from a deliverable, which is the distinction all seven registers turn on.

## 2026-08-16

### clarify 1.2.0 → 1.3.0: the gate now ends in a decision, not a question

Referral to another model family stops being an option and becomes a step, and the last gate stops asking "are you sure" and starts asking "whose decision is this". A fork sitting on the agent's axis (craft, convention, anything reversible, anything where the alternative simply loses) gets settled and reported in a clause. Only taste, cost, scope, risk tolerance, the user's own systems, and anything irreversible reach the user.

- **Lanes pin their model and their effort.** `claude --model claude-fable-5 --effort high`, `codex exec -m gpt-5.6-sol` at high, `agy --model gemini-3.7-flash-high`, `grok -m grok-4.6 --effort xhigh`. The last two were previously unpinned and silently inherited whatever the CLI config held. Three CLI facts are recorded with how each was established, including that codex validates neither flag: `-m bogus` prints `model: bogus` in the header and fails later at the API, which is why an empty output file rather than a clean header is that lane's real failure signal.
- **Dossier demoted from a rung to a branch.** It is for questions whose answer lives outside the repo and needs sourcing, not for residual uncertainty about a design call. Free lanes first (`research_plan`, `research_local_start`); the paid panel when the decision earns it, with the cost stated.
- **`(Recommended)` retreated to one shape of question.** A grounded fork no longer reaches the user, so the mark now belongs only on an unrecoverable-action question, on the reversible path. `"irreversible": true` is a declared field and the linter errors on a mark without it, because destructiveness cannot be read out of prose: *"delete the stale flags, or quarantine them?"* is a scope question carrying a destructive verb, and a keyword rule would demand a mark on exactly the question that must not have one.
- **Two options by default, a third when the referral earns it**, with the linter warning at three rather than erroring.
- **The release was put through its own gate, and the panel refused two things.** The codex lane hit a usage limit and is recorded as a failure rather than dropped. grok-4.6 and gemini-3.7 both answered and both independently rejected the same two proposals. One changed the design: the gate was going to read "if you can name a recommendation, take it", which collapses into never asking, since you can nearly always name one. The other, the two-option default, shipped against their advice with the cost written into `references/evidence.md` rather than talked around: it sharpens the single eval this skill loses 4-0, and whether gate 4's new "is there a better approach than the ones listed" question recovers that case is unmeasured. All three reviews are committed under `plugins/clarify/docs/deep-research/`.

### proctor 0.3.0 → 0.4.0: the skill describes what the server actually became

The proctor-mcp server stopped competing on actuation and now delegates it to Cua Driver, an MIT-licensed project doing the same job across three platforms with far more behind it. Proctor keeps observation, and that half is not a preference: Cua's screenshots carry no frame-status metadata, while Apple defines six `SCFrameStatus` values and makes checking them a precondition of trusting a frame. A layer that exists to catch other people's silent failures needs at least one channel it can trust. Proctor also keeps the verdict layer and the whole supervised-run surface. This release is the skill catching up with all of it: 772 insertions across `SKILL.md` and `references/tools.md`, and no code change, because the code was right and its description was not.

- **"Two planes" is now "Planes and lanes".** Six plane values rather than four, including `routedEvent` for an injected event delivered to one process, and `unknown` for a delivery mode this build does not recognise. A `backend` field says who actuated. The honesty rule survives intact: a synthetic-plane result still proves the narrower claim.
- **A new iOS section, leading with its ceiling.** An iOS target is not a window, and the Mac's accessibility API does not reach into the simulator, so there is no tree, no elements and no geometry assertions. A model that assumes parity with the macOS lane will waste a campaign, so the limit is stated before the capability.
- **`doctor` went from two grants to five questions.** It reports a toolchain now, with a table mapping each missing piece to the lane it disables.
- **What Proctor observes is a section rather than a footnote.** It is the centre of the product now, and captures carrying frame trustworthiness is the reason a Proctor capture is worth more than a screenshot from anything else.
- **Six drifts, found by checking every claim against the source rather than against the brief.** The tool count was 19 and is 20. The `scripting` profile was documented as carrying `policy`, which is `full` only. The `ax` profile was undocumented. "Sixteen assertion kinds" is seventeen, and `horizontalAlignment` was missing from the enum. `snapshot`'s `maxNodes` default is 600, not 2000. And the honesty section described a synthetic-plane step as the server falling back, which is true only for `type` and `scroll`; an outright refusal fails the step, which is the opposite guarantee and the one a reader would have acted on wrongly.
- **Three supervision regressions the project's own direction document had implied away.** It said supervision holds intact under delegation. Reading the implementation spec instead: an off-Space window is refused on the Cua lane and reachable on the native one; the takeover statement goes up after an unrequested foreground escalation rather than before it; and a batch whose driver Proctor cannot identify arms no input block, so click-to-Stop is never consulted and the person keeps Escape, the menu bar and the gaps between steps. All three are in the text.
- **The caveat is in the text, not in a commit message.** `which cua-driver` returns nothing on the machine this was written on, so the skill tells anyone selecting that lane to treat the first delegated step as a probe. `maestro` and `simctl` both resolve, so the Maestro lane carries no such caveat and was verified live against maestro 2.4.0 and a real simulator.

## 2026-08-15

### resume-session 1.0.0 : Universal Multi-CLI Session Continuity Engine

Upgraded and rebranded from `resume-claude-session` into a universal multi-agent session discovery and handover engine across Claude Code, Google Antigravity (AGY), Cursor IDE, Codex / OpenAI CLI, Grok / X.AI CLI, and repository workspace ledgers.

- **Universal Multi-CLI Engine (`find_session.py`):** Pure Python 3 standard library script with discovery adapters across all five major agent platforms. Extracts the 6-dimensional takeover state: session ID & provenance, initial user prompt, terminal error state, modified files, technical config keys (Apple Team IDs, OAuth Client IDs, bundle identifiers, ports), and actionable immediate next steps.
- **Brand Asset Suite (Concept A: The Golden Thread):** Master SVG generated via `build_icon.py` in the Fledgeling porcelain house palette (`#F8F5EE` to `#E4DDCB`), pairing a muted obsidian transcript strata card on the left with an energized golden-vermilion filament on the right via a Tahoe gel-glass coupler node. Multi-scale renders generated down to 16px along with an audit contact sheet (`audit.html`) and high-res banner (`banner.png`).
- **Comprehensive Documentation & Benchmark (`EVALS.md`):** Complete 4-phase guide and per-CLI cheatsheet in `SKILL.md`, structural evals demonstrating 100% discovery recall and 0-token local context recovery vs the 45,000+ token cost of raw transcript ingestion.

### design-review 1.7.0 → 1.8.0 — the sweep no longer dies on a large page

`run_review.py` crashed with a `TimeoutError` traceback on its **third viewport**
against a 3.2 MB, 12-slide single-file deck: no probes written, two captures
orphaned, and nothing in the output naming what was responsible.

- **Root cause, measured rather than guessed.** Timing each probe individually:
  `probeLayoutIntegrity` took **26.8s of a 27.6s sweep**, and inside it
  `probeTextOverlap` was the whole cost. It is an O(n²) pair loop that called
  `floatLayer()` — which walks ancestors calling `getComputedStyle` — **twice per
  pair**. On ~250 text nodes that is ~62,500 ancestor walks. The 30s CDP socket
  timed out mid-frame.
- **Fix:** resolve `floatLayer()` once per node, and sweep-line the pair loop —
  sorted by top edge, the inner loop breaks as soon as a candidate starts at or
  below the current node's bottom. The cheap rect test now runs before
  `contains()` and the layer comparison. **26.8s → 0.77s** for the whole
  layout-integrity probe; 1.6s for the full sweep. Output verified
  **byte-identical** against the previous implementation on a fixture built with
  genuine overlaps, nested pairs and separate float layers (41 records, 6.61s →
  0.41s), and the results are re-sorted into document order so `cap()` keeps the
  same subset run to run.
- **Per-probe isolation.** `runAll()` is now driven one probe per round trip.
  A probe that throws or overruns the socket costs its own key instead of the
  whole review: it is recorded as `null` and named in `probeErrors`, which is
  deliberately distinguishable from a probe that ran and found nothing.
- **`Page.recover()` and `CDP.reconnect()`.** After a read timeout the reply is
  still in flight, so the next command reads the *previous* reply and every
  result afterwards is attributed to the wrong probe — plausible numbers, wrong
  labels. The socket is now rebuilt. Two engine facts, both measured 15 Aug 2026
  and now in `references/browser-drivers.md`:
  - **Obscura scopes the Target domain to the connection.** On a fresh socket
    `Target.getTargets` returns an empty list and `Target.attachToTarget` answers
    "Target not found" — while `GET /json/list` still lists the page. The HTTP
    listing is not evidence a target is reachable, so recovery must create a
    *new* target and re-navigate. Probes taken after that ran on a re-loaded
    document, and the output records which ones in `reloadedAfter`.
  - **`Emulation.setDeviceMetricsOverride` works, but only with the session id.**
    Sent on the bare browser connection it is accepted and silently does nothing,
    which is indistinguishable from an engine that ignores the domain. The
    viewport matrix was verified genuinely varying (375/768/1024/1280/1920 each
    report the requested `innerWidth`) rather than assumed.
  - Recovery retries with 0/2/4/8s backoff, because the renderer is usually still
    finishing the call that overran. An infinite loop in page JS is not
    recoverable at all; that is reported rather than marked clean.

 
### be-my-witness 0.1.0 → 0.2.0 · Dual-Oracle Visual Governance & Component Slice Diffing

- **Dual-Oracle Visual Governance**: Clarified authority model so that while test expectations govern behavioral logic, the **Design Mock is the visual Oracle** for spatial layout, typography ramps, control hierarchy, padding, and iconography. Structural deviations (e.g. centered button text vs leading-aligned row with trailing chevron) are classified as High-Severity Visual Regressions rather than stale mocks.
- **Component Slice Diffing**: Mandated component/row-level bounded slice diffs to prevent local layout defects from hiding behind global image noise and anti-aliasing.

### proctor 0.3.0 → 0.4.0 · Native Layout & Geometry Inspection

- **Live Window & Popover Life-Cycle**: Mandated that macOS UI tests attach to live AppKit/SwiftUI windows and menu extras rather than headless SPM rasterizers (`ImageRenderer`) which emit placeholder glyphs for native controls.
- **Element Geometry & Layout Inspection**: Added guidance for element bounding box, horizontal text alignment, and child offset verification.

### Antigravity & Strict YAML 1.2 Frontmatter Normalisation

- **Antigravity CLI Compatibility**: Added top-level `plugin.json` manifests across all plugins in the marketplace to enable seamless zero-config discovery in Google Antigravity CLI (`agy`).
- **Strict YAML 1.2 Frontmatter Formatting**: Formatted description frontmatters in all `SKILL.md` files to standard YAML 1.2 block scalars (`description: >-`), preventing strict YAML parsers from dropping skills containing colons or quotation marks.

## 2026-08-14 — proctor catches up with its own MCP server

### proctor 0.2.0 → 0.3.0

The skill described an eleven-tool server that now ships nineteen, and it was missing every
capability added since it was written. This is the catch-up pass, plus the operational traps that
cost real time in a live campaign.

- **Added** `proctor_zoom` and the reason to reach for it. `proctor_capture` normalises to the
  vision ceiling by default, and the pixels a label or a numeric field is written in do not survive
  that downscale, so a whole-window capture is the wrong instrument for "what does that say".
  Iterative crop-and-zoom lifts GUI grounding accuracy on high-resolution desktop software from
  roughly 19% to 48-73%; the compose path is find → zoom → assert.
- **Added** `proctor_menu`: the whole menu bar in one accessibility read, reaching a background or
  other-Space app, with each item carrying both the `menuPath` that actuates on the accessibility
  plane and the `key` plus `modifiers` pair a synthetic shortcut needs.
- **Added** capture normalisation and formats. `normalization.scale` is the factor to map a
  coordinate back with (`native = normalised / scale`), and PNG stays the default because OCR
  recovered 94% of words from PNG against 78% at JPEG q50, with words misread as a *different real
  word* rising sixfold.
- **Added** `proctor_apps action: "activate"`, and named the symptom it answers. An attach returning
  an empty `windows` array reads as an unreachable app and usually means every window is closed;
  activate is the only way in, because the menu item that would reopen a window cannot be reached
  without the window it creates.
- **Added** the `--profile` cost table. The catalogue is re-sent every turn and survives compaction,
  so `core` at ~6.8k against `full` at ~11.3k is a standing cost paid before any work happens.
- **Added** a section on the cursor overlay, which draws the cause of what a run is doing. Three
  things matter to a campaign: it never appears in a capture (window-scoped, so it cannot move a
  state hash), `PROCTOR_CURSOR=0` turns it off, and it draws one panel per display because a panel
  spanning the union of several is accepted by the window server, reported onscreen with alpha 1,
  and never presented.
- **Added** "Traps that cost real time", each of which has cost an hour somewhere. The sharpest:
  an accessibility press on an Electron outline row selects it, reports `ok: true`, sets focused and
  selected, and does not navigate — Slack, VS Code and Discord all do this, and the fix is a
  synthetic click with `foreground: true`. Also: node ids die when the agent restarts, `diffEach`
  defaults true and will overrun the tool result on a Chromium tree, and `find` beats a screenshot
  for "did that land".
- **Added** an honest warning to Scale. The server is one process behind one socket and does not yet
  arbitrate between MCP clients, so two campaigns on one Mac interleave their steps. Reads are safe;
  actuation is not.

## 2026-08-13 — the harnesses stop borrowing mechanisms

`goal-harness` and `loop-harness` are now **`better-goal`** and **`better-loop`**. Both were
hardening layers over `/goal` and `/loop`; both now arm mechanisms they create themselves, and
neither built-in is load-bearing any more. The rename is not cosmetic — a skill whose whole job
was "make the built-in survive" is a different thing from one that replaces it.

### goal-harness 1.0.3 → better-goal 2.0.0

- **Changed** the armed mechanism from `/goal`'s prompt Stop hook to a `command` Stop hook the
  skill writes and registers itself. Gates are judged by exit code rather than by a small model
  reading the transcript, so "all screens now match the mock" no longer passes.
- **Added** a stall watcher under `Monitor`. A Stop hook fires when a turn *ends*; a run wedged on
  a permission prompt never ends one, so nothing was reported. The watcher reads the ledger's
  timestamp from outside and emits `STALL` when it goes stale, with exponential backoff capped
  at four hours.
- **Added** stuck-detection, which is the cost fix on this side. The guard fingerprints the failing
  set: an identical second failure blocks with the output **withheld** — it is already in the
  context verbatim — and an identical third disarms the run and says so. `stuck_after` is
  configurable; a run making progress never reaches it.
- **Changed** state from a single `.claude/goal-state.json` to per-slug `.claude/goals/<slug>.json`,
  after two runs in one repo collided over the shared file.
- **Added** `disarm.sh` restoring the block cap it raised, so teardown is one command rather than a
  settings edit by hand.
- **Renamed** `goal-guard.sh` → `guard.sh` and `condition-craft.md` → `gate-craft.md`, which is the
  same shift in one word: the artifact is a gate that can fail, not a condition to be judged.

### loop-harness 1.0.2 → better-loop 2.0.0

- **Changed** the armed mechanism from a session cron to a `Monitor` running `watch.sh`, which polls
  a probe command outside the session. Polling costs nothing; only a change wakes anything. No cron
  means no seven-day expiry, no missed fires while the session is busy, and nothing in settings to
  clean up.
- **Added** the known-state register, for the defect that prompted this work: five of twelve of the
  heaviest measured sessions re-sent the same unmet condition and the same failing tasks turn after
  turn, re-billing the whole prefix each time, and accounted for 91% of input between them. A state
  seen before is suppressed and backed off rather than re-reported, and the suppression is written
  to the ledger so a quiet loop can prove it was working.
- **Added** three more bounds beside it: a wake budget per rolling hour, a dry-stop after N
  unchanged polls, and `--stop-when`. A wake now carries **the delta** rather than the whole probe
  output.
- **Added** `--tick-cmd`, which dispatches a detached `claude -p` on a change so the session is
  never woken at all — the cheapest tick available, at the cost of failing quietly.
- **Added** probe determinism as a blocking preflight check: it runs the probe twice and compares.
  A probe carrying a timestamp or a PID turns a change-gated watcher back into a cron with extra
  steps, and nothing else would have caught it.
- **Added** a wake-to-poll ratio warning to `status.sh`, which is the number that says whether the
  gate is doing any work.

### Both

- **Rewrote** every reference and script against the current Opus 5 prompting guidance — complete
  spec up front, no verification scaffolding, an explicit subagent cap, calm trigger language.
- **Kept** composition with the built-ins where it still helps (`/goal /better-goal …`), and kept
  back-compatibility with the old state-file layout so a run armed by 1.x still disarms cleanly.
- **Re-rendered** both banners, which surfaced three obscura gaps now recorded in
  `banner-src.html`: no file:// sub-resource loads at all, remote web fonts never load, and
  `obscura fetch` has no viewport flag.

## 2026-08-11 — measurement pass

A head-to-head against the built-in `/compact`, run two ways: the skill's own 12 eval scenarios
(controlled ground truth) and 8 real compaction events sampled across length bands from 61k to
2.9M characters. Both arms wrote every summary; nothing here is a re-read of an old number. The
run found more wrong with the *instrument* than with the skill, and one real defect in the skill.

### braindump 2.2.0 → 2.3.0

- **Fixed** a defect the skill's own eval caught it committing: the pinned tier was collecting file
  contents. Handed a distinctive header comment, "preserve exactly, never paraphrase" overrode
  "file contents are on disk, point at them", and the paste landed *inside* the pinned block as a
  Tier-1 item. Both the skill arm and the plain baseline did it, and both blew the length cap.
  SKILL.md now states plainly that the pinned tier never contains file contents, and that "the user
  quoted it in this conversation" is not a reason to pin it — Tier 1 is what a successor cannot
  re-derive, and anything on disk is re-derivable by definition.
- **Added** a contamination filter to `benchmark_vs_compact.py`. The free `cli` baseline poisons
  itself once the addendum ships: a harness that splices the pinned-block instruction into live
  compactions leaves *its* summaries on disk looking like any other `/compact` event. **27 events**
  in this operator's corpus already carried the addendum marker, and one of six sampled baseline
  summaries was one of them. `find_events` now excludes them by default and reports the count;
  `--include-treated` keeps them when the wire arm is what you mean to measure.
- **Added** the honest limit that most constrains the benchmark: on real sessions the detectors
  usually find nothing. Measured over 30 random compaction events, corrections yield zero spans in
  **93%** of events (median 0, max 1) and rejected approaches in **70%** (median 0, max 13); a fifth
  of events have no span in any of the three classes. That is why the 121-event table's correction
  row rests on 34 events, and why a controlled eval set is the better instrument for "does the
  method work" while the transcript benchmark is the better one for length, extractiveness and
  structure.
- **Added** `references/evidence.md § Why the built-in drops these classes`, read out of the
  installed Claude Code 2.1.227 rather than inferred. Its nine sections never ask for a rejected
  approach anywhere (§4 asks for errors "and how you fixed them" — the opposite category); it
  instructs recency bias twice, explicitly; it scopes verbatim preservation to "security-relevant"
  constraints only; and §3 and §8 both ask for "full code snippets where applicable". So 0.3%
  retention is the prompt working as written, and the baseline's greater length is compliance
  rather than sloppiness — which bounds the claim as much as it supports the design.
- **Added** eval 13, covering the REREAD list that addendum v3 already ships on the wire and that
  nothing tested. Its first draft pre-sorted the files into "steering" and "background", which
  telegraphed the answer well enough that the baseline passed it too; the shipped version presents
  them undifferentiated, because sorting them is the thing being tested.
- **Changed** ConstraintRot's 0%/38% from "Measured:" to a stated-but-unreplicated figure in
  SKILL.md, matching the errata already recorded in `references/evidence.md`. The direction is what
  the two-tier design rests on and the paired case supports it independently; the percentages were
  read from an abstract.
- **Fixed** `evals.json`'s `skill_name`, still `compaction-quality` after the rename.

**What the run measured.** On the 12 eval scenarios: baseline 53/59 mechanically checkable
assertions against the skill's 55/59, at identical median length (4,785 vs 4,788 chars) — a narrow
margin, and the design's own ceiling, since a prompt that hands over the facts lets both arms retain
them. The separation is structural: across those 12, a pinned block in 100% of skill summaries
against 0%, a REREAD list in 100% against 25% incidental, and 4.2 file paths cited against 0.7, at
the same length. On 7 usable real transcripts: 31% shorter (15,737 vs 22,946 median chars), pinned
in 80% of cases against 16%, REREAD in 100% against 0%, rejected approaches 50% against 0% — n=2,
a hint rather than a result. Two figures go the other way and are reported rather than buried: the
skill is *more* extractive (0.171 against 0.132), and identifier recall is lower (80% against 86%).
An eighth transcript was discarded: on a 944-row session the skill arm returned a continuation of
the conversation's subject instead of a summary, which is a harness failure in the benchmark
driver, not a summary-quality datum, and it was the sole source of an otherwise striking
`CORRECTIONS` row.

## 2026-08-11

A grounding pass driven by 90 days of this operator's own transcripts (1,037 compaction events,
counting rules from INSAV-RECON) plus a review of the four deep-research reports against what the
data now shows. Every number that moved traces to `perch/scratch-contextcost/`.

### should-compact 0.1.0 → 0.2.0

- **Changed** the residue model. "A compaction leaves ~51,000 behind" was the intercept read as the
  value: the fitted relation is `post ≈ 50,958 + 0.117 × pre` (n=1,037), so the residue at the 1M
  wall is ~168k, 3.3× the intercept. The floor row now carries the relation, and the crossover below
  which compaction grows the context is confirmed at ~57.7k on 4.4× the original sample.
- **Fixed** `precompact_gate.sh`'s token estimate to match its own comment: `bytes * 2 / 7`
  (~3.5 chars/token) where the code divided by 4 — a 14% under-count in the direction that made
  `at_the_wall` fire late, which is the unsafe direction for a headroom rule.
- **Added** guidance to point `SHOULD_COMPACT_WINDOW_TOKENS` at an enforced proxy budget (Relay
  ships one) rather than the hardware window: auto-compaction fires at the enforced wall, so
  headroom against the 1M window reasons about a wall the session never reaches.
- **Added** to the evidence: the 90-day trigger recount (median 987,636; bimodal — 59.3% above
  900k, 29.1% below 200k), the wall-clock cost of a compaction (median 171.6 s against 12.1 s for
  an ordinary turn, n=219), and the cross-reference to the time-priced budget analysis.

### braindump 2.1.0 → 2.2.0

- **Added** the REREAD list: the pinned block now ends with the path of every CLAUDE.md, SKILL.md,
  plan, spec or rules file whose instructions were steering the session, so the successor re-reads
  them instead of following the summary's paraphrase of them. Anthropic's prompting guidance names
  compaction as a hydration point, and auto re-reading memory files after compaction is the
  most-requested compaction fix in Claude Code's issue tracker (#21925, #31409, #9796). Addendum
  bumped to v3 (1,099 bytes) carrying the same instruction on the wire; v2 retained under a
  superseded fence.
- **Changed** the opening framing, which the data contradicted: the summary is the only
  *deliberate* survivor, not the only survivor — ~168k tokens of residue carry through a wall
  compaction, and what the residue keeps is the recent end, which is why the middle of a long
  window is the true one-chance region (U-shaped summariser faithfulness, PoSum-Bench).
- **Changed** the sweep guidance to name the middle as the danger zone and to sweep by meaning
  rather than keyword (low-lexical-overlap constraints are what retrieval misses).
- **Added** a Tier-1 item ceiling with its number: follow-rate falls 0.964 → 0.447 between 1 and 20
  stacked instructions, so ~20 pinned items is the ceiling and consolidation beats accumulation.
- **Added** errata to the deep-research corpus: the auto-compaction trigger claims in all four
  files are superseded by the 99.8% measurement; `compaction-xai-grok.md` is marked superseded
  outright (both its concrete Claude Code figures were wrong) with its one distinctive result —
  parallel compaction's output-invariance — lifted into `references/evidence.md`; ConstraintRot's
  0%/38% flagged as read-from-abstract-only; CogCanvas flagged single-source.

## 2026-08-09

A pass over six weeks of session transcripts — 25,917 files, 1,669 sessions using a plugin skill — reading the human messages that followed each invocation. Six categories of feedback came back; these are the changes they produced. Where a rule already existed and was skipped anyway, it became a command with an exit code rather than a more strongly-worded rule.

### clarify 1.0.0 → 1.1.0

- **Added** gate step 4, *Could another model settle it instead?* A technical question — which library, whether an approach has a flaw, which of two designs holds up — is a question about the world, and the user is not the only thing that can answer it. Two verified lanes: `claude --model claude-fable-5 --effort high` for speed, and `gpt-5.6-sol` via the Codex CLI for a genuinely different model family, which is the one that matters when everything else is Claude checking Claude. Both verified end to end before shipping, including the header assertions that prove the model and effort actually stuck.
- **Added** four rules that keep the lane from becoming theatre: send the evidence rather than the question, verify the lane ran, a failed lane means deciding alone and saying so, and you still decide — forwarding two models' answers to the user is the same abdication as asking, with extra latency.
- **Changed** the description and the gate table to say that what should reach the user is taste, cost, scope and risk, not something another model could have settled.

### create-mac-icon 1.2.0 → 1.3.0

- **Added** `scripts/audit_sheet.py`, with `render` and `check` subcommands. `check` parses `audit.html`, resolves every `<img src>` against the directory, and fails on a missing image, an unfilled `{{PLACEHOLDER}}`, a missing master, or a take short of its retina sources.
- **Added** the 48px row: sources at 256/128/96/64/32 shown at 128/64/48/32/16. A Finder list and a marketplace tile render at 48, and an icon that survives 128 and 16 can still collapse between them.
- **Changed** the audit sheet from an instruction to a gate. It was already required in the skill text, and shipped missing twice anyway — *"why no audit.html? doesn't the skill say to create one?"* An instruction-only rule in this pipeline has a measured history of being skipped.
- **Added** the one-silhouette rule for icon sets, and the reminder that a passing `check` is not a looked-at sheet.

### design-review 1.5.0 → 1.6.0

- **Added** stage 9, *intent conformance* (`references/intent-conformance.md`), with `intent` as a worklist column so it is enumerated rather than improvised. Three checks the pipeline was blind to, each from a review that came back clean and was then contradicted: direction conformance (the half-converted redesign that passes every gate — *"a mashup of the original and the new chosen design"*), shared chrome as its own worklist row (*"every portal header also has a broken layout"*), and cross-instance differentiation for templated output, where measuring consistency rewards the defect (*"looks almost identical for every company portal"*).
- **Added** a render precondition to `layout-integrity.md`. An empty viewport has nothing to overflow, so an all-green layout report and a page that rendered nothing are the same output. A real app shipped a media query hiding `.app` whose `.gate` counterpart was never ported: a black screen at 390 and 768 on every route, on which `scrollWidth === clientWidth` returned a confident PASS.
- **Added** a two-capture skeleton measurement and an async-action coverage sweep to `states-and-resilience.md`.

### create-swe-project 1.8.0 → 1.9.0

- **Changed** phase D to hand the app icon to `create-mac-icon` whole, rather than routing it to `mac-design-studio` and hand-rolling a contact sheet from a bare `media-gen-pro` call. That shortcut skipped the corpus, the rubric, the fidelity loop and the recipe library, and produced icons described as *"really basic compared to all of the macos icons"*. `media-gen-pro` with `svg: true` is Engine B inside the pipeline, not a replacement for it.
- **Added** the reference trawl to phases D and M, with its ledger in `INDEX.md`.

### create-skill 1.1.0 → 1.2.0, improve-skill 1.0.0 → 1.1.0

- **Changed** the brand-treatment phase to route icons to `create-mac-icon` and gate with `audit_sheet.py check`.
- **Added** the rule that a written banner is not a looked-at banner: open the sheet and the renders before shipping them.

### report 1.0.0 → 1.1.0, dossier-report 1.0.0 → 1.1.0

- **Added** a reference trawl over the block types these reports are built from — evidence callouts, comparison tables, stat rows, reading surfaces. Structure and density transfer; the palette still comes from the subject.
- **Added** to dossier-report: open your own render before handing it to `design-review`, and render the PDF export to images, because print CSS breaks in ways the screen version never shows.

### goal-harness 1.0.3 → 1.1.0

- **Added** step 6b, an out-of-band heartbeat. The Stop guard only fires at the end of a turn, so a run that dies mid-turn — usage limit, crashed delivery agent, lost session — never reaches a Stop event, and the goal looks armed until somebody checks. The guard cannot close that gap because the guard is inside the thing that died.
- **Added** *status is not an action*: a turn that reads the state, says "still running" and ends satisfies no gate and spends a block against the cap.

### loop-harness 1.0.2 → 1.1.0

- **Added** the rule that a human verdict never blocks a tick. A loop waiting on a person who is asleep is indistinguishable from one that crashed; queue the item, let model-side review gate the round, and apply human verdicts when they land.

### compaction-quality 2.0.1 → 2.0.2

- **Added** the head-to-head benchmark output and run log.

### Repository

- **Fixed** `.gitignore` to exclude `.claude/`, which holds this repo's git worktrees. Committing it would land duplicate plugin trees and worktree metadata in history.
- **Fixed** `marketplace.json` drift: every entry now matches its `plugin.json` on version and description.
