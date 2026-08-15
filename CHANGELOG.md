# Changelog

Notable changes to the plugins in this marketplace. Newest first.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); each plugin carries its own version in its `plugin.json`, and this file records what moved and why.

## 2026-08-15

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
