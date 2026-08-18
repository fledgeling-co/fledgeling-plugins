<p align="center">
  <img src="assets/banner.png" alt="Fledgeling: a cream fledgeling-bird mark on warm charcoal beside the wordmark, with the line: tools for people building from nothing" width="100%" />
</p>

<p align="center"><strong>SWE Skills from <a href="https://www.fledgeling.app">Fledgeling</a>.</strong><br />
Built and used daily by <a href="https://github.com/lprhodes">Luke Rhodes</a>; shipped when they've earned it.</p>

<p align="center">
  <img alt="36 skills" src="https://img.shields.io/badge/skills-36-C4622D">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-6B665D">
</p>

---

Fledgeling makes AI-native software for founders and developers; these are the SWE skills that come out of building it. Each one exists because a real workflow needed it, and each carries its own README, evals or references where the work justified them. Every icon below sits on the same measured family silhouette, and the three-engine pipeline with its scored audit sheet is the standard they are held to, with a gate that says which ones do not meet it yet.

**[skills.fledgeling.app](https://skills.fledgeling.app)** is the same set, searchable: describe the problem you have and it finds the skill, without you knowing its name.

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

<a href="plugins/mockup-fidelity/README.md"><img src="plugins/mockup-fidelity/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mockup-fidelity](plugins/mockup-fidelity/README.md)

Does the built screen actually match the mock? Measures the rendered tree rather than eyeballing a screenshot or reading the source, treats the mock as the authority, and inverts the burden of proof so a difference is a defect until a citation proves it deliberate. Every element of the mock ends up in one of three states, present, divergent or absent, so a ledger of agreements cannot hide the thing nobody looked at. It also refuses to certify a property the engine cannot measure: a preflight proves each detector class can run, and a class that cannot is reported inconclusive with its reason rather than counted as a match. On this machine all nine classes are silenced by the browser engine, which its own EVALS.md says out loud.

<br clear="left" />

<a href="plugins/tui-craft/README.md"><img src="plugins/tui-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [tui-craft](plugins/tui-craft/README.md)

Design, mock and review terminal interfaces against what a terminal actually draws, not the code or the sketch that meant to draw it. Two skills over one cell grid. Before the app exists, you declare what a screen holds and a compiler does the width arithmetic, because drawing a layout by hand means counting characters and `len("🚀 Deploy")` is 8 where the screen spends 9; then it gates the design on a role ladder, on selection that survives losing colour, and on focus signalled twice. Once it runs, it captures the app through a pty and runs the arithmetic nobody eyeballs correctly: a box that opens and never closes, a row shoved past its neighbours by a double-width glyph, text cut with no ellipsis to say so. Every finding lands on a row and a column. Both halves share one width function, so a mock and its capture never disagree for reasons that are not about the design.

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

<a href="plugins/create-skill/README.md"><img src="plugins/create-skill/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-skill](plugins/create-skill/README.md)

The sibling of improve-skill, for when there is nothing to improve yet. It interviews you properly first, because an unstated intention is the usual reason a new skill misses, then researches the domain, builds through skill-creator with every rule traced to evidence, and proves it against the honest baseline: the same prompts with no skill at all.

<br clear="left" />

<a href="plugins/geminify/README.md"><img src="plugins/geminify/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [geminify](plugins/geminify/README.md)

A skill is a prompt, and most skills here were tuned against a Claude model's habits. Point this one at any of them and it writes the sibling `gemini.md` that recalibrates it for Gemini: every categorical scope in the target turned into a counted row, the verification put back with its command attached, and every claim about Gemini tagged with whether Google published it, someone measured it, or you reasoned your way to it. A script checks each quoted claim appears verbatim in Google's own corpus, because a paraphrase in quotation marks got attributed to them three times before it existed.

<br clear="left" />

<a href="plugins/create-mac-icon/README.md"><img src="plugins/create-mac-icon/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-mac-icon](plugins/create-mac-icon/README.md)

macOS app icons, measured against the reference instead of eyeballed. A direction catalogue distilled from 532 real icons, three generation engines with a written audit sheet, then a scoring harness that iterates the shipped SVG against the winning raster at five sizes until the material matches. Every confirmed construction feeds a recipe library, so it gets better with each commission.

<br clear="left" />

<a href="plugins/dossier-report/README.md"><img src="plugins/dossier-report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [dossier-report](plugins/dossier-report/README.md)

A research question in, one published page out. It runs a paid and free research panel, reads every report end to end rather than the merged summary, turns the corpus into a list of claims with sources attached, then designs the page from scratch around its own subject so consecutive pages do not converge on one look. Every claim carries a citation you can open, and the build fails on one that does not resolve. The page now renders in three registers, Primer, Brief and Technical, and the reader chooses which one they're in; each is independently cited from that same registry, and where the backends disagreed, the disagreement survives into all three rather than being tidied away for the simpler one. A vertical rule has to sit in a real gap too, measured from the text's ink rather than from the box the padding was declared on; that check found twenty violations on a page this skill had already published. Every page now opens with a TLDR, and a buying question gets an actual answer: the categories buyers split on, three ranked picks in each, one overall winner with what it loses on. A ranking is reasoning rather than a measurement, so it renders as reasoning and names the claims it rests on, and a paywalled Which? or RTINGS verdict counts as evidence with the paywall stated instead of being dropped for an affiliate listicle. Pictures come from the sources with their provenance attached, charts go through dataviz in plain CSS, hand-drawn SVG or TanStack Charts compiled to static SVG at build time, and the motion layer is no longer optional.

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

`/goal` looks like it keeps working until the job is done, and it does not: the condition is judged by a small model reading the transcript, so it grades what the run said rather than what is true, and Claude Code overrides the hook after eight consecutive blocks and reports that turn as completed. Nine turns of real work trips it, silently. This arms its own guard instead, a command Stop hook that runs the gates and decides by exit code, plus a watcher outside the turn loop, because a run that dies mid-turn never reaches a Stop hook at all. It also knows when to give up: a gate failing identically turn after turn disarms the run rather than re-sending the same failure at the price of the whole session prefix. Built from 114 real goal runs, where the most common follow-up was the word "resume", six times in a row.

<br clear="left" />

<a href="plugins/better-loop/README.md"><img src="plugins/better-loop/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [better-loop](plugins/better-loop/README.md)

A loop that fires on a clock re-sends the same unmet condition and the same six failing tasks turn after turn, and each fire re-bills the session's whole accumulated prefix, and five of twelve heavy sessions did that and accounted for 91% of input between them. Nothing about a smaller context window stops a loop from restarting. So this arms a watcher instead of a schedule: it polls one deterministic probe command in the background, wakes the session only when the answer changes, sends the delta rather than the state, and goes progressively quieter about a failure it has already reported. A quiet system costs nothing at all, and a tick that needs no conversation can run detached, where there is no prefix to pay for.

<br clear="left" />

<a href="plugins/report/README.md"><img src="plugins/report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [report](plugins/report/README.md)

A session works something out over two hours, you ask for the write-up, and what comes back reads well and can't be checked. Three different things leave a session looking identical on the page: a number that was measured, one read off a single sample, and one worked out from two other facts. This compiles the session's own evidence trail into a claim ledger before it designs anything, so the page is generated from the ledger rather than cited afterwards, and reasoning renders visibly as reasoning. It now writes the same argument three ways over that one ledger, Primer, Brief and Technical; each is independently and fully cited from the same registry, and switching between them works with JavaScript off. A reading can change the words; it can't change what's claimed, so the confidence and the limits travel into all three. One self-contained HTML file that paginates to a real A4 PDF with the motion stripped out, plus a one-page TLDR derived from the same ledger so the two can't disagree. Its own blind panel went 4-2 for it and told it what it was missing: an ask. So the TLDR is now a named section carrying one, and on a comparison the ask is the verdict itself: the categories readers split on, three ranked picks in each, one winner sized and owned. Rankings render as reasoning and name their ledger rows; paywalled lab testing counts as evidence with the paywall stated; pictures come from the evidence trail with provenance; and charts build in plain CSS, hand-drawn SVG or TanStack Charts compiled to static SVG, so nothing loads at runtime and it all still prints.

<br clear="left" />

<a href="plugins/clarify/README.md"><img src="plugins/clarify/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [clarify](plugins/clarify/README.md)

Decides whether to interrupt you at all, and mostly the answer is no. It sweeps the conversation and the repo for the answer first, drops anything whose answer wouldn't change the work, then sends what's left to a different model family before it ever reaches you: fable-5 for speed, gpt-5.6-sol, gemini-3.7 and grok-4.6 at xhigh for independence, a three-family panel when the call is open enough to deserve one. Each lane pins its model and its effort, because a lane that inherits its config default isn't the lane you picked. Then the last gate, which isn't "are you sure" but "whose decision is this": if the axis is craft or convention it gets settled and reported in a clause, and only taste, cost, scope, risk and the genuinely irreversible reach you. Two options, and no recommendation to nudge you, since the fork it could have recommended on was one it should have taken. A mark now appears on one shape of question only, the one you're asked despite the agent knowing the answer because the action can't be undone. Two out-of-family reviewers argued against the two-option default and their reports ship with it; one of them changed the gate, and the other is a cost written into the evidence file rather than talked around.

<br clear="left" />

<a href="plugins/whats-left/README.md"><img src="plugins/whats-left/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [whats-left](plugins/whats-left/README.md)

Asks what's left on a project and gets back two documents that immediately start lying to each other: the status report says a feature shipped, the open questions ask whether to switch it on, and nothing shows you the second is why the first is wrong. This is one page where they're the same graph: every blocked item links down to the decision that releases it, every decision links back up and says how much it actually releases. Stage is a word rather than a percentage, so built, deployed and accepted stay three different things instead of averaging into ninety per cent. Agreeing with a recommendation means clicking the option already selected, which fires no change event and is exactly how a page exports your agreement as "never looked at", so confirmation is bound to the click too, and anything you never touch exports as unconfirmed rather than as your decision. Send the JSON back and it does the work your answers unblocked. Six structural properties to nil against the same request with no skill at all.

<br clear="left" />

<a href="plugins/stocktake/README.md"><img src="plugins/stocktake/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [stocktake](plugins/stocktake/README.md)

A board is a set of claims about a codebase, and nobody checks them. Cards drift into review and stay there, work gets finished on a branch nobody merged, and a ticket reads as done because somebody wrote a comment saying so. The uncomfortable part is that checking looks like it already happened: the surface renders, the schema validates, the suite is green, and none of that is the same as the number on the screen having been produced by code somebody wrote. So this goes card by card and, before it opens any diff, rebuilds the numbered requirement list from the description, every comment and every attached image — because a diff read first supplies the frame, and whatever the change quietly dropped never enters the list. Then it finds where the work actually is (merged, on a branch nobody merged, finished but never pushed, in a worktree, or never started — four different problems), traces each requirement to the code that produces its value rather than the screen that shows it, and asks whether the tests behind it could ever have failed: which rung of oracle each one stands on, armed and unarmed assertions counted apart, and a denominator for what the gate really runs. It grades out of family with one judge rather than a panel, because nine frontier judges across seven families supply about two independent votes and the best single judge beats the group. “I could not tell” is a real answer that blocks rather than rounding up. Cards with work left get a brief for ship-fleet; cards with an open question get it referred or decided with a reason instead of parked on you; and it promotes to Done and stops — a human’s column stays a human’s until eight named preconditions hold, which a bundled gate refuses by default and tells you which are missing.

<br clear="left" />

<a href="plugins/proctor/README.md"><img src="plugins/proctor/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [proctor](plugins/proctor/README.md)

Tests a native Mac app the way an instrument does rather than the way a screenshot does. A screenshot you looked at is an impression; a screenshot carrying a frame status and a dirty-rect summary is a reading, and only one of those can be wrong in a way you would notice. It ships with its own MCP server, which actuates through the accessibility plane rather than by injecting events, so it drives windows that are behind other windows, on another Space, or simply not in front, without stealing focus, and while you keep using the machine. Where the accessibility tree, the layer geometry and the captured pixels disagree about the same instant, that disagreement is the defect: an unexposed control, a ghost node, a control you can focus but cannot see. Waiting is a conjunction of quiet frames, quiet notifications and the app's own idle signal, never a sleep, and each wait reports which of those it actually got; an app with a blinking caret can never go pixel-quiet, so it says so instead of claiming agreement it did not have. Flows replay N times to separate a race from a bug before either gets filed. An iOS Simulator is a second lane rather than a port: deep links through `simctl` and Maestro flow files, scored for determinism the same way, with the ceiling stated up front, since the Mac's accessibility API does not reach into a simulated device and so there is no tree to assert against. For apps you own, an embeddable debug-only reflector returns resolved colours, fonts and radii, because macOS has no cross-process computed style and guessing one is worse than saying so.

<br clear="left" />

<a href="plugins/create-test-suite/README.md"><img src="plugins/create-test-suite/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-test-suite](plugins/create-test-suite/README.md)

Runs a UI test campaign and leaves a page behind that says what it actually proved. It reads the project before it reads the DOM: the overview, the PRD, the feature specs, the design notes and the latest mocks, so the denominator for "is this tested" is what the product claims it does rather than what the build happens to render, which is the only way a campaign can notice a control the design specifies and the build never had. Then it states the correctness space out loud, samples it deliberately, and says which cells it took. Every case declares which rung of oracle it stands on, from touch and presence up through outcome and metamorphic relations, and a flow you have marked critical that carries no case above presence fails the gate; not a model reviewing the suite afterwards and offering a view, a script exiting non-zero with the flow ids in it. A pass has to name an artifact on disk, armed and unarmed assertions are counted apart and never summed, and the ledger's exit code is the verdict, so a partial campaign cannot read as a finished one. The sweeps go after what no requirement named, including the one this was built for: force the server to refuse and check the interface says so, which is where four production defects were sitting behind a client that resolves refusals instead of throwing them. It knows the ways its own checks lie, ten of them, each measured. It compares the build against its design of record on structure, resolved style, vocabulary and quantised geometry rather than on pixels. And it plans to each lane's ceiling across web, React Native, macOS, iOS and SwiftUI, so an iOS Simulator with no accessibility tree is marked not-applicable with the structural reason rather than left open looking like neglect.

<br clear="left" />

<a href="plugins/anvil-errand/README.md"><img src="plugins/anvil-errand/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [anvil-errand](plugins/anvil-errand/README.md)

One verb for work that belongs on another machine. `anvil errand` sends a Claude Code agent into a container on your node or spare PC and, before anything starts, asks whether every piece of the path is actually there: a node, a link to it, the image, the credential, the proxy. It reports the first blocker in that order and only the first, because a list assembled past the first failure carries entries nobody measured; the image lives on the node, so asking about it before the link is up returns an answer about the link wearing the image's words. Each of the six refusal kinds is a stable identifier carrying the one next step that clears it, and `--check` runs the whole preflight while changing nothing. The failure it removes isn't the errand not working; it's finding the missing piece halfway through a container start, from a symptom that points somewhere else. After that it's the ordinary job verbs, and `anvil attach` is read-only on purpose: the container starts detached, so PID 1's stdin is at EOF from the first instant. It provisions nothing, deliberately; standing up the node, engine, image, pairing and proxy from scratch is the runbook in the anvil repo, which stays the source of record. Worth knowing before you lean on it: `--check` passing is not the errand working, and the verb has not yet been driven against a live node from the gate.

<br clear="left" />

<a href="plugins/agent-voice/README.md"><img src="plugins/agent-voice/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [agent-voice](plugins/agent-voice/README.md)

Your agent already has a voice; nobody chose it. This gives agent-authored text a register, and splits it by who reads the text, because the reader decides the failure mode. Text a person reads fails as padding: a closing summary, a self-congratulation, a preamble before the answer. Text a model reads fails as ambiguity: an unmeasurable qualifier, a scope nobody counted, a verification instruction the runner did not need. Both halves are gated by a script, so "I checked" means checked, and the two gates deliberately disagree with each other. Length is a stated rule rather than an attitude, because nothing else controls it: effort governs how much a model thinks rather than how much it says, and sampling parameters are rejected outright now, so prose is the only lever left. The bound on all of it is a measurement rather than a taste: a response-compression style over 106 paired agentic tasks cut cost by a third and score by 7.61 points, and about 78% of that saving was the agent investigating less rather than writing more tersely, so every rule here changes how much gets written and never how much gets done. Uncertainty, risk, security implications and verification that actually happened are content, and they stay. There is a dialects layer too, carrying the one rule that inverts between families: Claude verifies its own work and its verification instructions get deleted, while a Gemini runner needs the check named with its command attached, and one recorded run there satisfied every categorically-named requirement with exactly one instance. Every rule carries a marker naming its evidence, and a script checks each attributed quote verbatim against the vendor document, because a sibling skill in this repo once shipped three of its own sentences in quotation marks with Google's name on them. Worth knowing before you lean on it: the A/B evidence is three tasks on one model family, and the Claude arm was contaminated by inherited instructions and thrown away rather than reported, so this has never been measured on the family it is mainly written for.

<br clear="left" />

<a href="plugins/design-craft/README.md"><img src="plugins/design-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [design-craft](plugins/design-craft/README.md)

Designs or reviews a user-facing visual artifact as an opinionated designer rather than a code generator, and roots every hi-fi build in whatever design context already exists, lifting a matched system's resolved values exactly instead of rounding them to a 4/8px grid and reporting the rounding as a fix. It names the category's rut and its predictable opposite before generating, then derives seven candidates across at least three material families, because a model asked for something distinctive reaches for the same small set every time. The direction it picks is written into the artifact as a five-block contract its own critique gate audits promise by promise, since more than a quarter of one generative UI tool's stated rationales were measured not to appear in what it built. Its gate computes WCAG contrast from source across hex, rgba, hsl and oklch, follows tokens to their :root definitions, composites opacity, and reproduces this skill's own recorded incidents to two decimal places. Contrast is tri-state: a gradient, an image or an undeclared ground is reported UNMEASURABLE rather than skipped, because an unmeasured pair and a passing pair otherwise serialise identically. Twenty-five assertions against the version it replaces: 23 against 9, with two the predecessor won kept in the table.

<br clear="left" />

<a href="plugins/ux-craft/README.md"><img src="plugins/ux-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ux-craft](plugins/ux-craft/README.md)

The UX half of the pair design-craft completes: flows, forms, states, interface copy, email and mobile behaviour, in three modes over eleven references. It resolves the accessibility floor against the standards themselves rather than against habit: 24x24 CSS px is WCAG 2.2 SC 2.5.8 at AA and is the only target-size number a WCAG failure may cite, 44x44 is SC 2.5.5 at AAA, and Apple's 44pt and Android's 48dp are craft targets in density-independent units that are not WCAG numbers at all. The three figures had disagreed across three files, at the exact point the accessibility claim was made. It ships a stdlib-only lint that runs static over HTML, JSX and CSS and probes a rendered page, where only exit 0 is a pass and a run that examined zero files refuses rather than reporting a clean sheet. Research deleted rules as well as adding them: the seven-item navigation limit is gone, because Miller measured recall and a navigation is recognition. Its blind panel is an honest draw. Honesty about limits won 10-0 across both families and every case, and actionability lost and stayed lost, which became the rule that the fix comes before the caveat.

<br clear="left" />

<a href="plugins/deck-craft/README.md"><img src="plugins/deck-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [deck-craft](plugins/deck-craft/README.md)

Builds, reviews and converts slide decks across three targets (a self-contained HTML presentation on a fixed 16:9 stage, editable PowerPoint through a JSON round-trip, and investor decks assembled from a bundled library of 200 layouts) and treats a deck as what it is: fixed-size content, read at distance, on someone else's clock. What makes it unusual is the gate, and specifically what the gate refuses to do. A preflight probe measures what nobody eyeballs correctly, and it is built so that failing to run cannot look like passing. It asserts the configuration it was handed is the configuration the probe received, because on the previous version reformatting two lines of the probe defeated the substitution and a regulated results deck printed a clean pass with all four disclosure checks never having run. Six summary keys that gated nothing now gate, including the type floor, the skill's loudest rule, previously computed and unable to fail a build. A check that throws is reported NOT RUN and counted, and a run that examined zero slides refuses rather than passing. Seventeen assertions: 17 against the predecessor's 3, with its three genuine passes preserved.

<br clear="left" />

<a href="plugins/mac-craft/README.md"><img src="plugins/mac-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-craft](plugins/mac-craft/README.md)

Designs and reviews macOS application interfaces against the platform's own published values rather than a web habit that happens to run on a Mac. It replaces seven prose audits that graded themselves: one recorded run reported a 100% contrast pass rate while the artifact it had just built put a glyph at 1.00:1, the same colour on the same colour, invisible. Contrast is now computed from the declared cascade with alpha compositing across four appearance contexts, exit 2 means unmeasurable, and examined=0 is never a pass. It also corrects three things the platform documentation actually says, each measured: the kit's own secondary label tier is 3.98:1 and cannot be a body-text colour, white 13pt on the kit's Blue is 3.52:1 so Apple's accent button is itself sub-AA, and the HIG specifies title case for menu items where the previous version asserted sentence case everywhere. Its corpus went from 35 MB to 608 K by cutting what nothing routed into, including 500 gallery images at a resolution that could never serve their stated purpose. It cedes icon work entirely to create-mac-icon and stops rather than running a weaker second pipeline.

<br clear="left" />

<a href="plugins/mac-design-digest/README.md"><img src="plugins/mac-design-digest/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-design-digest](plugins/mac-design-digest/README.md)

Maintains a machine-written corpus of macOS design evidence across sessions, reading screenshots, kits and design files, and writing findings that the interface skills then build against. Provenance is a type system rather than a habit: two orthogonal mark families compose, one for how precisely a value is known and one for how strongly, with promotion running along the strength axis only, so a guess never becomes a specification by being seen more often. Its gate enforces seventeen parser invariants, because a wrong number in a corpus outlives the conversation that created it. The result worth reading is a loss: its rebuild improved its structural assertions from 35 to 43 and then lost its blind panel 4-1, because having built a check for a class of problem it stopped looking past the check. Two of the three defects the panel found became checks the same day, which took a defective fixture from 10 failures to 17 and immediately revealed that its own clean control was incomplete. The third became a rule, that the gate is a floor and not a ceiling, carrying that panel loss as its evidence.

<br clear="left" />

<a href="plugins/generate-investor-portal/README.md"><img src="plugins/generate-investor-portal/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [generate-investor-portal](plugins/generate-investor-portal/README.md)

Generates a shareholder or investor portal from a company's own material, and treats a fabricated figure as the worst failure available to it. The refusal that matters is structural: a currency amount, percentage, thousands-number or date appearing in any prose slot outside a provenance object is refused outright, because a fabricated figure arrives as a sentence rather than as a marked value with a bad source, and nothing reading the provenance fields can see it. A number that is genuinely unavailable carries one of six reason codes and a readable placeholder, since one state cannot say both not obliged to hold this and obliged and missing. Its record gate runs entirely offline against a JSON file with no crawl, no database and no spend, mutation-tested at 39 of 39, and it reproduces the accent-contrast failure this skill recorded against production. The republish refusal now fires as the third of three exits before anything is crawled or generated, where it previously sat 420 lines below the inputs and let a run spend twice before refusing.

<br clear="left" />

> [!NOTE]
> Some skills depend on each other by design: ship-armada dispatches through ship-fleet and ship-feature, which conduct the shipyard stage skills, and armada-sync is the maintenance half of ship-armada. Each README states what it expects.

## Licence

MIT. Do what you like; attribution appreciated.

## Elsewhere

Fledgeling is [Luke Rhodes](https://www.linkedin.com/in/lukerhodes/), also co-founder of [Diolog](https://diolog.app).

[fledgeling.app](https://www.fledgeling.app) · [GitHub](https://github.com/lprhodes) · [X](https://x.com/lp_rhodes) · [LinkedIn](https://www.linkedin.com/in/lukerhodes/) · [hello@fledgeling.app](mailto:hello@fledgeling.app)
