# Changelog

Notable changes to the plugins in this marketplace. Newest first.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); each plugin carries its own version in its `plugin.json`, and this file records what moved and why.

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
