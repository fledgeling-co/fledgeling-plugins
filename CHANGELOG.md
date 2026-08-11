# Changelog

Notable changes to the plugins in this marketplace. Newest first.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); each plugin carries its own version in its `plugin.json`, and this file records what moved and why.

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
