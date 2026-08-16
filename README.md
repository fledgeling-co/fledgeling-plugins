<p align="center">
  <img src="assets/banner.png" alt="Fledgeling: a cream fledgeling-bird mark on warm charcoal beside the wordmark, with the line: tools for people building from nothing" width="100%" />
</p>

<p align="center"><strong>SWE Skills from <a href="https://www.fledgeling.app">Fledgeling</a>.</strong><br />
Built and used daily by <a href="https://github.com/lprhodes">Luke Rhodes</a>; shipped when they've earned it.</p>

<p align="center">
  <img alt="16 skills" src="https://img.shields.io/badge/skills-16-C4622D">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-6B665D">
</p>

---

Fledgeling makes AI-native software for founders and developers; these are the SWE skills that come out of building it. Each one exists because a real workflow needed it, and each carries its own README, evals or references where the work justified them. Every icon below came through the same three-engine design pipeline with its audit sheet committed beside it.

**[skills.fledgeling.app](https://skills.fledgeling.app)** is the same sixteen, searchable — describe the problem you have and it finds the skill, without you knowing its name.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
```

Then install what you want:

```text
/plugin install trawl@fledgeling-plugins
```

Third-party marketplaces have auto-update off by default, so refreshing is something you do:

```text
/plugin marketplace update fledgeling-plugins
```

## The skills

<a href="plugins/trawl/README.md"><img src="plugins/trawl/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [trawl](plugins/trawl/README.md)

Divergent ideation that converges on something you can ship. Isolated thinkers under genuinely different frames, the obvious answer written down first, and a creative pick recommended only when it beats that answer blind. Receipts committed: structural evals (96.4% vs its predecessor's 49.0%), a four-judge blind panel, and the research corpus it was built from.

<br clear="left" />

<a href="plugins/design-review/README.md"><img src="plugins/design-review/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [design-review](plugins/design-review/README.md)

The last pass before a human looks at AI-built UI. Deterministic gates first (accessibility, contrast, target size, motion, layout integrity), then judged passes over hierarchy, states, flows and system coherence, on real renders at a viewport matrix. Findings come severity-ranked with pasteable fixes and an explicit list of what was never checked.

<br clear="left" />

<a href="plugins/be-my-witness/README.md"><img src="plugins/be-my-witness/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [be-my-witness](plugins/be-my-witness/README.md)

Look at a screenshot and say what it actually shows. Validates a UI capture against what a test expected and against a design mock, and hands back both a gate a build can act on and findings a person can read. Measures first (is this even evidence, did the screen finish loading, are the two framings comparable), then crops in at 2-3x rather than squinting at a thumbnail, looks at every pair in both orders because vision models flip on ordering, and classifies each difference as framing, data, structure, styling or state so a different crop or one extra row cannot turn a build red. The test wins over the mock.

<br clear="left" />

<a href="plugins/tui-craft/README.md"><img src="plugins/tui-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [tui-craft](plugins/tui-craft/README.md)

Design and review terminal interfaces against what the terminal actually drew, not the code that meant to draw it. Captures the running app through a pty into a typed cell grid, then runs the arithmetic nobody eyeballs correctly: a box that opens and never closes, a row shoved past its neighbours by a double-width glyph, text cut with no ellipsis to say so. Every finding lands on a row and a column. On top sits a pattern catalogue built from 48 shipped TUIs, an anti-pattern list where each entry shipped in a real app, and terminal constraints cited rather than asserted. A claim about a screen needs a captured frame; capture failure is reported as the result rather than papered over by reading the source.

<br clear="left" />

<a href="plugins/create-swe-project/README.md"><img src="plugins/create-swe-project/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-swe-project](plugins/create-swe-project/README.md)

A complete, working new project from an idea. One front-loaded interview, then scripts render the whole scaffold: monorepo, auth, admin, native apps, testing harnesses, deploy config, and a launch pipeline that researches, seeds feature briefs and mocks every surface. The LLM only interviews; scripts make the files.

<br clear="left" />

<a href="plugins/shipyard/README.md"><img src="plugins/shipyard/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [shipyard](plugins/shipyard/README.md)

The feature-delivery stage skills: intake, triage, plan, design, work, verify and gap-fix, on one tracker adapter and one complete status machine. Built on a 110-ticket audit of its predecessors, with typed evidence rules and a cross-family verifier as the only path to done. The report card and blind-panel results ship in the repo.

<br clear="left" />

<a href="plugins/ship-feature/README.md"><img src="plugins/ship-feature/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-feature](plugins/ship-feature/README.md)

The end-to-end conductor: one feature from rough idea to merged, verified code, running the shipyard stages in order with plan and design in parallel, a fresh-context cross-family verifier before merge, and a fail-closed gate where every box is checked now rather than recalled.

<br clear="left" />

<a href="plugins/ship-fleet/README.md"><img src="plugins/ship-fleet/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-fleet](plugins/ship-fleet/README.md)

The backlog orchestrator: surveys everything left in a repo, writes one durable ledger before any execution, then conducts concurrent ship-feature runners under a global agent budget, with per-item verification and merges serialized. Done means the ledger says so, never that a dispatch returned.

<br clear="left" />

<a href="plugins/ship-armada/README.md"><img src="plugins/ship-armada/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-armada](plugins/ship-armada/README.md)

The portfolio-level orchestrator. Reads the manifest of record, verifies it against git, then surveys, plans, routes single directives into the right project's pipeline, and dispatches per-repo backlogs as dependency-ordered campaigns with capped concurrency.

<br clear="left" />

<a href="plugins/armada-sync/README.md"><img src="plugins/armada-sync/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [armada-sync](plugins/armada-sync/README.md)

The surgical counterpart to ship-armada: after work happens anywhere in the portfolio, it updates that one project's manifest entry, stamps it fresh, and stops. The smallest skill here, on purpose.

<br clear="left" />

<a href="plugins/braindump/README.md"><img src="plugins/braindump/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [braindump](plugins/braindump/README.md)

Gets everything load-bearing out of a session and onto the page before the context holding it is thrown away. Measured across 121 real compaction events, the built-in prompt keeps 0.3% of the approaches you ruled out and 33.8% of your standing constraints; violations run 0% when a rule survives into the summary and 38% when it doesn't. Writes a pinned verbatim tier ahead of the narrative, and ships a deterministic scorer plus a head-to-head benchmark whose baseline arm costs nothing. Published as `compaction-quality` until 2026-08.

<br clear="left" />

<a href="plugins/should-compact/README.md"><img src="plugins/should-compact/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [should-compact](plugins/should-compact/README.md)

Scores 0-10 whether now is a good moment to compact, and says why in one line. It judges the seam in the work rather than the fullness of the window: an open tool chain or a half-finished edit is a hard zero however full the context is, and that one signal decided 98.07% of holds across 1,089 measured turns. Reads only a hot buffer plus an append-only session log it maintains itself, so it is cheap enough for Haiku and fast enough to sit in a `PreCompact` hook, where it can veto an ill-timed automatic compaction. It never vetoes at the wall, because blocking at 99.8% full loses the session rather than saving it. Beat the no-skill baseline 10-0 on a two-family blind panel.

<br clear="left" />

<a href="plugins/resume-session/README.md"><img src="plugins/resume-session/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [resume-session](plugins/resume-session/README.md)

When an AI coding session ends unexpectedly (a token limit, an API timeout, an unexpected context compaction, or simply switching between tools like Claude Code, Antigravity, Cursor, Codex, or Grok), the next agent typically starts blind. This scans your local machine to discover past sessions across all major agent CLIs, parses their exact transcripts on disk, extracts the 6-dimensional takeover state (original goal, terminal errors, modified files, config keys, decisions, and immediate next steps), and produces an uncorrupted continuity handover without redundant re-discovery.

<br clear="left" />

<a href="plugins/improve-skill/README.md"><img src="plugins/improve-skill/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [improve-skill](plugins/improve-skill/README.md)

The pipeline that built half this marketplace, as a skill. Point it at an existing skill plus your complaints; it runs paid and free deep research, rebuilds the skill with every change traced to evidence, proves the rebuild with comparative evals and a blind multi-family judge panel, then ships the full brand treatment. You choose the name and the icon concept before anything gets generated.

<br clear="left" />

<a href="plugins/create-skill/README.md"><img src="plugins/create-skill/assets/icon-c1-256.png" align="left" width="110" alt="" /></a>

### [create-skill](plugins/create-skill/README.md)

The sibling of improve-skill, for when there is nothing to improve yet. It interviews you properly first, because an unstated intention is the usual reason a new skill misses, then researches the domain, builds through skill-creator with every rule traced to evidence, and proves it against the honest baseline: the same prompts with no skill at all.

<br clear="left" />

<a href="plugins/create-mac-icon/README.md"><img src="plugins/create-mac-icon/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-mac-icon](plugins/create-mac-icon/README.md)

macOS app icons, measured against the reference instead of eyeballed. A direction catalogue distilled from 532 real icons, three generation engines with a written audit sheet, then a scoring harness that iterates the shipped SVG against the winning raster at five sizes until the material matches. Every confirmed construction feeds a recipe library, so it gets better with each commission.

<br clear="left" />

<a href="plugins/dossier-report/README.md"><img src="plugins/dossier-report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [dossier-report](plugins/dossier-report/README.md)

A research question in, one published page out. It runs a paid and free research panel, reads every report end to end rather than the merged summary, turns the corpus into a list of claims with sources attached, then designs the page from scratch around its own subject so consecutive pages do not converge on one look. Every claim carries a citation you can open, and the build fails on one that does not resolve. The page now renders in three registers, Primer, Brief and Technical, and the reader chooses which one they're in; each is independently cited from that same registry, and where the backends disagreed, the disagreement survives into all three rather than being tidied away for the simpler one. A vertical rule has to sit in a real gap too, measured from the text's ink rather than from the box the padding was declared on; that check found twenty violations on a page this skill had already published.

<br clear="left" />

<a href="plugins/mac-doctor/README.md"><img src="plugins/mac-doctor/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-doctor](plugins/mac-doctor/README.md)

Your Mac did not fill up because of one thing, it filled up because a hundred sensible defaults each left something behind and nothing was counting. Five scheduled jobs, from every fifteen minutes to weekly, with what each may do on its own widening as the gap between runs grows. Running low makes it check sooner, never delete more. The two short tiers are plain shell, so ninety-six runs a day cost no tokens at all. It ties a no-skill baseline on reasoning and says so in its evals; what it adds is that the reasoning runs while you are asleep.

<br clear="left" />

<a href="plugins/discipline/README.md"><img src="plugins/discipline/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [discipline](plugins/discipline/README.md)

Drop a short block at the top of a session and Claude spends less without doing less. It targets the three habits that quietly run up the bill: re-printing plans and diffs already on your screen, opening a whole file to find one line, and handing small jobs to sub-agents that each pay for a fresh context. The nearest alternative is caveman, and the choice between them is measured rather than argued. On the same 106 tasks caveman cut output tokens 41% against this skill's 16%, so caveman is better at the thing both are for. It also gave up 7.6 points of task score where this one gives up nothing detectable, because 78% of caveman's saving came from the agent taking fewer steps rather than writing more tersely. Pick caveman if the token count is all you are optimising; pick this one if the agent is doing long work you intend to trust.

<br clear="left" />

<a href="plugins/better-goal/README.md"><img src="plugins/better-goal/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [better-goal](plugins/better-goal/README.md)

`/goal` looks like it keeps working until the job is done, and it does not: the condition is judged by a small model reading the transcript, so it grades what the run said rather than what is true, and Claude Code overrides the hook after eight consecutive blocks and reports that turn as completed. Nine turns of real work trips it, silently. This arms its own guard instead — a command Stop hook that runs the gates and decides by exit code — plus a watcher outside the turn loop, because a run that dies mid-turn never reaches a Stop hook at all. It also knows when to give up: a gate failing identically turn after turn disarms the run rather than re-sending the same failure at the price of the whole session prefix. Built from 114 real goal runs, where the most common follow-up was the word "resume", six times in a row.

<br clear="left" />

<a href="plugins/better-loop/README.md"><img src="plugins/better-loop/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [better-loop](plugins/better-loop/README.md)

A loop that fires on a clock re-sends the same unmet condition and the same six failing tasks turn after turn, and each fire re-bills the session's whole accumulated prefix — five of twelve heavy sessions did that and accounted for 91% of input between them. Nothing about a smaller context window stops a loop from restarting. So this arms a watcher instead of a schedule: it polls one deterministic probe command in the background, wakes the session only when the answer changes, sends the delta rather than the state, and goes progressively quieter about a failure it has already reported. A quiet system costs nothing at all, and a tick that needs no conversation can run detached, where there is no prefix to pay for.

<br clear="left" />

<a href="plugins/report/README.md"><img src="plugins/report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [report](plugins/report/README.md)

A session works something out over two hours, you ask for the write-up, and what comes back reads well and can't be checked. Three different things leave a session looking identical on the page: a number that was measured, one read off a single sample, and one worked out from two other facts. This compiles the session's own evidence trail into a claim ledger before it designs anything, so the page is generated from the ledger rather than cited afterwards, and reasoning renders visibly as reasoning. It now writes the same argument three ways over that one ledger, Primer, Brief and Technical; each is independently and fully cited from the same registry, and switching between them works with JavaScript off. A reading can change the words; it can't change what's claimed, so the confidence and the limits travel into all three. One self-contained HTML file that paginates to a real A4 PDF with the motion stripped out, plus a one-page TLDR derived from the same ledger so the two can't disagree. Its own blind panel went 4-2 for it and told it what it was missing: an ask.

<br clear="left" />

<a href="plugins/clarify/README.md"><img src="plugins/clarify/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [clarify](plugins/clarify/README.md)

Decides whether to interrupt you at all, and mostly the answer is no. It sweeps the conversation and the repo for the answer first, drops anything whose answer wouldn't change the work, then sends what's left to a different model family before it ever reaches you: fable-5 for speed, gpt-5.6-sol, gemini-3.7 and grok-4.6 at xhigh for independence, a three-family panel when the call is open enough to deserve one. Each lane pins its model and its effort, because a lane that inherits its config default isn't the lane you picked. Then the last gate, which isn't "are you sure" but "whose decision is this": if the axis is craft or convention it gets settled and reported in a clause, and only taste, cost, scope, risk and the genuinely irreversible reach you. Two options, and no recommendation to nudge you, since the fork it could have recommended on was one it should have taken. A mark now appears on one shape of question only, the one you're asked despite the agent knowing the answer because the action can't be undone. Two out-of-family reviewers argued against the two-option default and their reports ship with it; one of them changed the gate, and the other is a cost written into the evidence file rather than talked around.

<br clear="left" />

<a href="plugins/whats-left/README.md"><img src="plugins/whats-left/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [whats-left](plugins/whats-left/README.md)

Asks what's left on a project and gets back two documents that immediately start lying to each other: the status report says a feature shipped, the open questions ask whether to switch it on, and nothing shows you the second is why the first is wrong. This is one page where they're the same graph — every blocked item links down to the decision that releases it, every decision links back up and says how much it actually releases. Stage is a word rather than a percentage, so built, deployed and accepted stay three different things instead of averaging into ninety per cent. Agreeing with a recommendation means clicking the option already selected, which fires no change event and is exactly how a page exports your agreement as "never looked at" — so confirmation is bound to the click too, and anything you never touch exports as unconfirmed rather than as your decision. Send the JSON back and it does the work your answers unblocked. Six structural properties to nil against the same request with no skill at all.

<br clear="left" />

<a href="plugins/proctor/README.md"><img src="plugins/proctor/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [proctor](plugins/proctor/README.md)

Tests a native Mac app the way an instrument does rather than the way a screenshot does. A screenshot you looked at is an impression; a screenshot carrying a frame status and a dirty-rect summary is a reading, and only one of those can be wrong in a way you would notice. It ships with its own MCP server, which actuates through the accessibility plane rather than by injecting events, so it drives windows that are behind other windows, on another Space, or simply not in front, without stealing focus, and while you keep using the machine. Where the accessibility tree, the layer geometry and the captured pixels disagree about the same instant, that disagreement is the defect: an unexposed control, a ghost node, a control you can focus but cannot see. Waiting is a conjunction of quiet frames, quiet notifications and the app's own idle signal, never a sleep, and each wait reports which of those it actually got; an app with a blinking caret can never go pixel-quiet, so it says so instead of claiming agreement it did not have. Flows replay N times to separate a race from a bug before either gets filed. An iOS Simulator is a second lane rather than a port: deep links through `simctl` and Maestro flow files, scored for determinism the same way, with the ceiling stated up front, since the Mac's accessibility API does not reach into a simulated device and so there is no tree to assert against. For apps you own, an embeddable debug-only reflector returns resolved colours, fonts and radii, because macOS has no cross-process computed style and guessing one is worse than saying so.

<br clear="left" />

<a href="plugins/anvil-errand/README.md"><img src="plugins/anvil-errand/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [anvil-errand](plugins/anvil-errand/README.md)

One verb for work that belongs on another machine. `anvil errand` sends a Claude Code agent into a container on your node or spare PC and, before anything starts, asks whether every piece of the path is actually there: a node, a link to it, the image, the credential, the proxy. It reports the first blocker in that order and only the first, because a list assembled past the first failure carries entries nobody measured; the image lives on the node, so asking about it before the link is up returns an answer about the link wearing the image's words. Each of the six refusal kinds is a stable identifier carrying the one next step that clears it, and `--check` runs the whole preflight while changing nothing. The failure it removes isn't the errand not working; it's finding the missing piece halfway through a container start, from a symptom that points somewhere else. After that it's the ordinary job verbs, and `anvil attach` is read-only on purpose: the container starts detached, so PID 1's stdin is at EOF from the first instant. It provisions nothing, deliberately; standing up the node, engine, image, pairing and proxy from scratch is the runbook in the anvil repo, which stays the source of record. Worth knowing before you lean on it: `--check` passing is not the errand working, and the verb has not yet been driven against a live node from the gate.

> [!NOTE]
> Some skills depend on each other by design: ship-armada dispatches through ship-fleet and ship-feature, which conduct the shipyard stage skills, and armada-sync is the maintenance half of ship-armada. Each README states what it expects.

## Licence

MIT. Do what you like; attribution appreciated.

## Elsewhere

Fledgeling is [Luke Rhodes](https://www.linkedin.com/in/lukerhodes/), also co-founder of [Diolog](https://diolog.app).

[fledgeling.app](https://www.fledgeling.app) · [GitHub](https://github.com/lprhodes) · [X](https://x.com/lp_rhodes) · [LinkedIn](https://www.linkedin.com/in/lukerhodes/) · [hello@fledgeling.app](mailto:hello@fledgeling.app)
