<p align="center">
  <img src="assets/banner.png" alt="Fledgeling: a cream fledgeling-bird mark on warm charcoal beside the wordmark, with the line: tools for people building from nothing" width="100%" />
</p>

<p align="center"><strong>SWE Skills from <a href="https://www.fledgeling.app">Fledgeling</a>.</strong><br />
Built and used daily by <a href="https://github.com/lprhodes">Luke Rhodes</a>; shipped when they've earned it.</p>

<p align="center">
  <img alt="43 skills" src="https://img.shields.io/badge/skills-43-C4622D">
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

Fifty-odd skills is a lot to meet at once, so they are grouped by what you are trying to do rather than by how they work. Every one carries its own README, and the ones marked **Uses another AI** may ask a model outside Claude's family for a second opinion — [`defer`](plugins/defer/README.md) decides which.


<br clear="left" />

## Making something

_Design it, write it, or build it from nothing._

<br clear="left" />

<a href="plugins/agent-voice/README.md"><img src="plugins/agent-voice/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [agent-voice](plugins/agent-voice/README.md)

Your agent already has a voice; nobody chose it. This gives agent-authored text a register, and splits it by who reads the text, because the reader decides the failure mode. Text a person reads fails as padding: a closing summary, a self-congratulation, a preamble before the answer. Text a model reads fails as ambiguity: an unmeasurable qualifier, a scope nobody counted, a verification instruction the runner did not need. Both halves are gated by a script, so "I checked" means checked, and the two gates deliberately disagree with each other. Length is a stated rule rather than an attitude, because nothing else controls it: effort governs how much a model thinks rather than how much it says, and sampling parameters are rejected outright now, so prose is the only lever left. The bound on all of it is a measurement rather than a taste: a response-compression style over 106 paired agentic tasks cut cost by a third and score by 7.61 points, and about 78% of that saving was the agent investigating less rather than writing more tersely, so every rule here changes how much gets written and never how much gets done. Uncertainty, risk, security implications and verification that actually happened are content, and they stay. There is a dialects layer too, carrying the one rule that inverts between families: Claude verifies its own work and its verification instructions get deleted, while a Gemini runner needs the check named with its command attached, and one recorded run there satisfied every categorically-named requirement with exactly one instance. Every rule carries a marker naming its evidence, and a script checks each attributed quote verbatim against the vendor document, because a sibling skill in this repo once shipped three of its own sentences in quotation marks with Google's name on them. Worth knowing before you lean on it: the A/B evidence is three tasks on one model family, and the Claude arm was contaminated by inherited instructions and thrown away rather than reported, so this has never been measured on the family it is mainly written for.

<br clear="left" />

<a href="plugins/create-mac-icon/README.md"><img src="plugins/create-mac-icon/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-mac-icon](plugins/create-mac-icon/README.md)

macOS app icons, measured against the reference instead of eyeballed. A direction catalogue distilled from 532 real icons, three generation engines with a written audit sheet, then a scoring harness that iterates the shipped SVG against the winning raster at five sizes until the material matches. Every confirmed construction feeds a recipe library, so it gets better with each commission.

<br clear="left" />

<a href="plugins/create-swe-project/README.md"><img src="plugins/create-swe-project/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-swe-project](plugins/create-swe-project/README.md)

A complete, working new project from an idea. One front-loaded interview, then scripts render the whole scaffold: monorepo, auth, admin, native apps, testing harnesses, deploy config, and a launch pipeline that researches, seeds feature briefs and mocks every surface. The LLM only interviews; scripts make the files.

<br clear="left" />

<a href="plugins/deck-craft/README.md"><img src="plugins/deck-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [deck-craft](plugins/deck-craft/README.md)

Builds, reviews and converts slide decks across three targets (a self-contained HTML presentation on a fixed 16:9 stage, editable PowerPoint through a JSON round-trip, and investor decks assembled from a bundled library of 200 layouts) and treats a deck as what it is: fixed-size content, read at distance, on someone else's clock. What makes it unusual is the gate, and specifically what the gate refuses to do. A preflight probe measures what nobody eyeballs correctly, and it is built so that failing to run cannot look like passing. It asserts the configuration it was handed is the configuration the probe received, because on the previous version reformatting two lines of the probe defeated the substitution and a regulated results deck printed a clean pass with all four disclosure checks never having run. Six summary keys that gated nothing now gate, including the type floor, the skill's loudest rule, previously computed and unable to fail a build. A check that throws is reported NOT RUN and counted, and a run that examined zero slides refuses rather than passing. Seventeen assertions: 17 against the predecessor's 3, with its three genuine passes preserved.

<br clear="left" />

<a href="plugins/design-craft/README.md"><img src="plugins/design-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [design-craft](plugins/design-craft/README.md)

Designs or reviews a user-facing visual artifact as an opinionated designer rather than a code generator, and roots every hi-fi build in whatever design context already exists, lifting a matched system's resolved values exactly instead of rounding them to a 4/8px grid and reporting the rounding as a fix. It names the category's rut and its predictable opposite before generating, then derives seven candidates across at least three material families, because a model asked for something distinctive reaches for the same small set every time. The direction it picks is written into the artifact as a five-block contract its own critique gate audits promise by promise, since more than a quarter of one generative UI tool's stated rationales were measured not to appear in what it built. Its gate computes WCAG contrast from source across hex, rgba, hsl and oklch, follows tokens to their :root definitions, composites opacity, and reproduces this skill's own recorded incidents to two decimal places. Contrast is tri-state: a gradient, an image or an undeclared ground is reported UNMEASURABLE rather than skipped, because an unmeasured pair and a passing pair otherwise serialise identically. Twenty-five assertions against the version it replaces: 23 against 9, with two the predecessor won kept in the table.

<br clear="left" />

<a href="plugins/generate-investor-portal/README.md"><img src="plugins/generate-investor-portal/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [generate-investor-portal](plugins/generate-investor-portal/README.md)

Generates a shareholder or investor portal from a company's own material, and treats a fabricated figure as the worst failure available to it. The refusal that matters is structural: a currency amount, percentage, thousands-number or date appearing in any prose slot outside a provenance object is refused outright, because a fabricated figure arrives as a sentence rather than as a marked value with a bad source, and nothing reading the provenance fields can see it. A number that is genuinely unavailable carries one of six reason codes and a readable placeholder, since one state cannot say both not obliged to hold this and obliged and missing. Its record gate runs entirely offline against a JSON file with no crawl, no database and no spend, mutation-tested at 39 of 39, and it reproduces the accent-contrast failure this skill recorded against production. The republish refusal now fires as the third of three exits before anything is crawled or generated, where it previously sat 420 lines below the inputs and let a run spend twice before refusing.

<br clear="left" />

<a href="plugins/mac-craft/README.md"><img src="plugins/mac-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-craft](plugins/mac-craft/README.md)

Designs and reviews macOS application interfaces against the platform's own published values rather than a web habit that happens to run on a Mac. It replaces seven prose audits that graded themselves: one recorded run reported a 100% contrast pass rate while the artifact it had just built put a glyph at 1.00:1, the same colour on the same colour, invisible. Contrast is now computed from the declared cascade with alpha compositing across four appearance contexts, exit 2 means unmeasurable, and examined=0 is never a pass. It also corrects three things the platform documentation actually says, each measured: the kit's own secondary label tier is 3.98:1 and cannot be a body-text colour, white 13pt on the kit's Blue is 3.52:1 so Apple's accent button is itself sub-AA, and the HIG specifies title case for menu items where the previous version asserted sentence case everywhere. Its corpus went from 35 MB to 608 K by cutting what nothing routed into, including 500 gallery images at a resolution that could never serve their stated purpose. It cedes icon work entirely to create-mac-icon and stops rather than running a weaker second pipeline.

<br clear="left" />

<a href="plugins/tui-craft/README.md"><img src="plugins/tui-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [tui-craft](plugins/tui-craft/README.md)

Design, mock and review terminal interfaces against what a terminal actually draws, not the code or the sketch that meant to draw it. Two skills over one cell grid. Before the app exists, you declare what a screen holds and a compiler does the width arithmetic, because drawing a layout by hand means counting characters and `len("🚀 Deploy")` is 8 where the screen spends 9; then it gates the design on a role ladder, on selection that survives losing colour, and on focus signalled twice. Once it runs, it captures the app through a pty and runs the arithmetic nobody eyeballs correctly: a box that opens and never closes, a row shoved past its neighbours by a double-width glyph, text cut with no ellipsis to say so. Every finding lands on a row and a column. Both halves share one width function, so a mock and its capture never disagree for reasons that are not about the design.

<br clear="left" />

<a href="plugins/ux-craft/README.md"><img src="plugins/ux-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ux-craft](plugins/ux-craft/README.md)

The UX half of the pair design-craft completes: flows, forms, states, interface copy, email and mobile behaviour, in three modes over eleven references. It resolves the accessibility floor against the standards themselves rather than against habit: 24x24 CSS px is WCAG 2.2 SC 2.5.8 at AA and is the only target-size number a WCAG failure may cite, 44x44 is SC 2.5.5 at AAA, and Apple's 44pt and Android's 48dp are craft targets in density-independent units that are not WCAG numbers at all. The three figures had disagreed across three files, at the exact point the accessibility claim was made. It ships a stdlib-only lint that runs static over HTML, JSX and CSS and probes a rendered page, where only exit 0 is a pass and a run that examined zero files refuses rather than reporting a clean sheet. Research deleted rules as well as adding them: the seven-item navigation limit is gone, because Miller measured recall and a navigation is recognition. Its blind panel is an honest draw. Honesty about limits won 10-0 across both families and every case, and actionability lost and stayed lost, which became the rule that the fix comes before the caveat.


<br clear="left" />

## Checking it before anyone sees it

_Catch the problems while they are still cheap to fix._

<br clear="left" />

<a href="plugins/be-my-witness/README.md"><img src="plugins/be-my-witness/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [be-my-witness](plugins/be-my-witness/README.md)

Look at a screenshot and say what it actually shows. Validates a UI capture against what a test expected and against a design mock, and hands back both a gate a build can act on and findings a person can read. Measures first (is this even evidence, did the screen finish loading, are the two framings comparable), then crops in at 2-3x rather than squinting at a thumbnail, looks at every pair in both orders because vision models flip on ordering, and classifies each difference as framing, data, structure, styling or state so a different crop or one extra row cannot turn a build red. The test wins over the mock.

<br clear="left" />

<a href="plugins/code-review/README.md"><img src="plugins/code-review/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [code-review](plugins/code-review/README.md) · **Uses another AI**

A review that lists three findings and stops has told you almost nothing, because you cannot tell whether it read the auth code and found it clean or never opened the file, and both come out as silence. So every run here ends with a coverage ledger: what it checked, what it could not, and why, naming the shard that came back empty, the checklist that never loaded, the gate that could not run and the contract boundary with no guard test on either side, and saying so explicitly when that column is empty, because an empty section and a missing section look identical on a screen. It picks up your repository before it reviews it rather than carrying a map somebody wrote into a skill: gate commands out of the package scripts and the CI config, since a review that runs a bare compiler has gated on something CI does not, frameworks out of the installed dependency versions, global controls and cross-package boundaries out of grep. Fourteen named angles surface candidates and are forbidden from suppressing each other, so two reasons for flagging one line both survive to be judged and deduplication happens afterwards on evidence rather than in whichever finder looked first. Verification returns three verdicts and only the refuted one drops, so a concurrency race or a falsy zero read as missing stays in as plausible with the step that would settle it named, instead of leaving with the noise and taking a real bug with it. Each depth prints its own budget at the top of the report, large diffs shard across parallel agents with the fan-out reconciled against the bucket list it dispatched, and there is deliberately no panel of judges, because nine frontier judges across seven model families measured as roughly two effective votes and the best single one matched the whole panel.

<br clear="left" />

<a href="plugins/design-review/README.md"><img src="plugins/design-review/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [design-review](plugins/design-review/README.md)

The last pass before a human looks at AI-built UI. Deterministic gates first (accessibility, contrast, target size, motion, layout integrity), then judged passes over hierarchy, states, flows and system coherence, on real renders at a viewport matrix. Findings come severity-ranked with pasteable fixes and an explicit list of what was never checked.

<br clear="left" />

<a href="plugins/mockup-fidelity/README.md"><img src="plugins/mockup-fidelity/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mockup-fidelity](plugins/mockup-fidelity/README.md)

Does the built screen actually match the mock? Measures the rendered tree rather than eyeballing a screenshot or reading the source, treats the mock as the authority, and inverts the burden of proof so a difference is a defect until a citation proves it deliberate. Every element of the mock ends up in one of three states, present, divergent or absent, so a ledger of agreements cannot hide the thing nobody looked at. It also refuses to certify a property the engine cannot measure: a preflight proves each detector class can run, and a class that cannot is reported inconclusive with its reason rather than counted as a match. On this machine the browser engine silences nine of them, which its own EVALS.md says out loud, and that ceiling belongs to the engine rather than to the build, so there is now a second one. Where the target is a native Mac app, an Electron app, or a web build whose divergence sits in a class the browser reports nothing for, the measurement goes through proctor and reads the accessibility tree and the compositor's own resolved layer values: a shadow CSSOM returns an empty string for is a radius, an offset and an opacity on a layer. That engine brings three questions the first cannot ask at all: whether the screenshot you are holding is current, whether something is mid-animation, and whether a control on screen has no accessibility node behind it. It also brings its own measured ceiling, because resolved colours need the app to embed a debug reflector and without one an eyedropped colour is still not a declared value. Its eval now has a real target to run against: a small Mac app, built and exercised, whose Settings pane is wrong in eight recorded ways, and building it withdrew one of the claims the previous version had made, because a capability read off the vendor's documentation turned out not to fire on a textbook case of it. It also adds the fourth answer the first engine had no instrument for: a value that will not hold still is a third way to be unmeasurable, so instability is scored as a number before anyone argues about whether a difference is a defect, and that score is where the geometry tolerance now comes from instead of a default nobody calibrated.

<br clear="left" />

<a href="plugins/proctor/README.md"><img src="plugins/proctor/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [proctor](plugins/proctor/README.md)

Tests a native Mac app the way an instrument does rather than the way a screenshot does. A screenshot you looked at is an impression; a screenshot carrying a frame status and a dirty-rect summary is a reading, and only one of those can be wrong in a way you would notice. It ships with its own MCP server, which actuates through the accessibility plane rather than by injecting events, so it drives windows that are behind other windows, on another Space, or simply not in front, without stealing focus, and while you keep using the machine. Where the accessibility tree, the layer geometry and the captured pixels disagree about the same instant, that disagreement is the defect: an unexposed control, a ghost node, a control you can focus but cannot see. Waiting is a conjunction of quiet frames, quiet notifications and the app's own idle signal, never a sleep, and each wait reports which of those it actually got; an app with a blinking caret can never go pixel-quiet, so it says so instead of claiming agreement it did not have. Flows replay N times to separate a race from a bug before either gets filed. An iOS Simulator is a second lane rather than a port: deep links through `simctl` and Maestro flow files, scored for determinism the same way, with the ceiling stated up front, since the Mac's accessibility API does not reach into a simulated device and so there is no tree to assert against. For apps you own, an embeddable debug-only reflector returns resolved colours, fonts and radii, because macOS has no cross-process computed style and guessing one is worse than saying so.

<br clear="left" />

<a href="plugins/test-campaign/README.md"><img src="plugins/test-campaign/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [test-campaign](plugins/test-campaign/README.md)

Runs a UI test campaign and leaves a page behind that says what it actually proved. It reads the project before it reads the DOM: the overview, the PRD, the feature specs, the design notes and the latest mocks, so the denominator for "is this tested" is what the product claims it does rather than what the build happens to render, which is the only way a campaign can notice a control the design specifies and the build never had. Then it states the correctness space out loud, samples it deliberately, and says which cells it took. Every case declares which rung of oracle it stands on, from touch and presence up through outcome and metamorphic relations, and a flow you have marked critical that carries no case above presence fails the gate; not a model reviewing the suite afterwards and offering a view, a script exiting non-zero with the flow ids in it. A pass has to name an artifact on disk, armed and unarmed assertions are counted apart and never summed, and the ledger's exit code is the verdict, so a partial campaign cannot read as a finished one. The sweeps go after what no requirement named, including the one this was built for: force the server to refuse and check the interface says so, which is where four production defects were sitting behind a client that resolves refusals instead of throwing them. It knows the ways its own checks lie, fourteen of them, each measured. It compares the build against its design of record on structure, resolved style, vocabulary and quantised geometry rather than on pixels. And it makes you prove the thing under test actually ran: a lane that claims the app was running and drawn has to name the built artifact, the command that built it, and what witnessed a process from it reaching a display server, because a campaign once reported 100% checked over two desktop apps where no GUI process had ever existed and every number in that report was true. It plans to each lane's ceiling across web, React Native, iOS and native macOS, Windows and Linux, so an iOS Simulator with no accessibility tree is marked not-applicable with the structural reason rather than left open looking like neglect; and a check the instrument could not perform reads as inconclusive rather than clean, because those two are the same shade of green and only one is a measurement. The newest rule came from the skill catching itself: a campaign it produced published 20 surface captures and passed every gate here, and the pictures were of a status report, a mock browser's index page and a design doc, twenty files holding six distinct images. Nothing had broken; the only thing binding a picture to a surface was its filename. So a published capture now records where the capture channel was actually pointed, at the moment it fires, and four exact passes read it: no recorded target, a target that is not the surface's route, two surfaces sharing one image, and a capture published without a judgement against its reference. None of the four asks a model, because the deterministic pre-scan that exists for exactly this returns a clean settled-and-contentful verdict on an image of entirely the wrong document, and vision tops out near 40% recall on fine-grained interface differences. Provenance answers it and nothing else does, which is why the gate can also be watched to fail: swap two surfaces' records and it has to go red.

<br clear="left" />

<a href="plugins/vouch/README.md"><img src="plugins/vouch/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [vouch](plugins/vouch/README.md)

Vouching is the audit word for tracing a record back to the document it came from, and it is the part of an expense claim that gets skipped, because the arithmetic balances either way. A claim assembled from a bank feed cannot tell you whether the charge on line forty is the company's expense or your own, whether the invoice behind it exists, or whether you already claimed it last year, and those are facts about documents. So this pulls the period from an accounting MCP and then computes the days on which the account holds no transaction at all, which is how it found two gaps of 38 and 44 days on the card that mattered, invisible until somebody looked and full of charges nobody had noticed. It reads the mail index rather than searching it blind, after a keyword search that was silently dropping its own date filter returned a confident wrong answer. It reads the bill-to block of the invoice and never the delivery address of the email that carried it, because those disagree often enough to matter, and it puts every claimed row on a six-rung ladder of how strongly its document actually names the company, since the rung nobody predicts is the one where the invoice names the company and carries a personal contact address, and on a real claim that rung was worth eleven rows and A$1,579.45 that four review passes had walked straight past. Two identical top-ups four days apart will both match whichever invoice a per-charge lookup returns first, so charges are assigned one to one with a used set on both sides. Twenty-four blocking checks gate the output, and the one that earns its keep opens every filed document and requires its filename to appear inside it, after an earlier pass put fourteen rows on the wrong month by keying them to a billing email. That check was itself vacuous for a while, passing 88 of 88 on a folder where two filenames had been deliberately swapped, because the extractor prints the filename in a banner above the text and the fallback match was finding it there. Where a portal refuses an automated browser it stops and hands back a page listing what it still needs, with the amount and the account each invoice should name, and that page carries only the suppliers whose accounts have already been established as the company's, because recovering an invoice for an account nobody has verified just moves the argument. Nothing enters a claim on an estimate, exclusions are reported rather than deleted, and it never asserts a tax characterisation: it states the arithmetic, cites the document, and leaves the characterisation to the accountant.

<br clear="left" />

<a href="plugins/warrant/README.md"><img src="plugins/warrant/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [warrant](plugins/warrant/README.md)

Takes the human out of per-item verification by writing down exactly what a machine may decide, and revoking that permission automatically when a model version moves, an escape lands or the control chart drifts. Deterministic checks first, one out-of-family grader rather than a jury, and a hash-chained ledger an auditor reads instead of the signatures. Built on a 22-source panel across four research backends, with every rule traceable to a claim id.


<br clear="left" />

## Handing over a pile of work

_Give Claude a list and let it work through it on its own._

<br clear="left" />

<a href="plugins/anvil-errand/README.md"><img src="plugins/anvil-errand/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [anvil-errand](plugins/anvil-errand/README.md)

One verb for work that belongs on another machine. `anvil errand` sends a Claude Code agent into a container on your node or spare PC and, before anything starts, asks whether every piece of the path is actually there: a node, a link to it, the image, the credential, the proxy. It reports the first blocker in that order and only the first, because a list assembled past the first failure carries entries nobody measured; the image lives on the node, so asking about it before the link is up returns an answer about the link wearing the image's words. Each of the six refusal kinds is a stable identifier carrying the one next step that clears it, and `--check` runs the whole preflight while changing nothing. The failure it removes isn't the errand not working; it's finding the missing piece halfway through a container start, from a symptom that points somewhere else. After that it's the ordinary job verbs, and `anvil attach` is read-only on purpose: the container starts detached, so PID 1's stdin is at EOF from the first instant. It provisions nothing, deliberately; standing up the node, engine, image, pairing and proxy from scratch is the runbook in the anvil repo, which stays the source of record. Worth knowing before you lean on it: `--check` passing is not the errand working, and the verb has not yet been driven against a live node from the gate.

<br clear="left" />

<a href="plugins/armada-sync/README.md"><img src="plugins/armada-sync/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [armada-sync](plugins/armada-sync/README.md)

The surgical counterpart to ship-armada: after work happens anywhere in the portfolio, it updates that one project's manifest entry, stamps it fresh, and stops. The smallest skill here, on purpose.

<br clear="left" />

<a href="plugins/atlas-publish/README.md"><img src="plugins/atlas-publish/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [atlas-publish](plugins/atlas-publish/README.md)

The only project-specific plugin here, and a release conductor rather than a script. It takes the open PRs to a registered draft and stops there; publishing to users is a founder action it will not take, and that is the boundary the whole thing is built around rather than a setting you can loosen. It picks the over-the-air lane or the App Store lane out of the native fingerprint instead of out of intent, which matters because the iOS build number sits inside that fingerprint, so bumping it alone forces a store release and an afternoon spent exporting a bundle no device will accept. Six of its steps cannot be undone and each names the observable to go and read afterwards, because a build tool, an upload and an MCP call will all hand back success without having done anything; two witnesses that share a failure mode are not a cross-check. Gates report passed, failed and not-run as three separate states, which is what the rebuild was actually for: the API carries a certificate-parity test that guards its only real assertion behind an environment variable and pairs it with an assertion that true is true, so without that variable it goes green having never compared the shipped certificate to the signing key, and the old skill read the green and moved on. If those two ever drift, every signed update is rejected on real devices and nothing else notices. Eleven steps, each marked with the lanes it applies to and each with an abort path written next to it, and it will stop and ask you for the TestFlight notes before it builds anything, because the old flow silently reused whatever stale text was sitting in the file. The diff review that used to ship alongside it is now its own plugin, code-review, generalised past this one codebase.

<br clear="left" />

<a href="plugins/flagship/README.md"><img src="plugins/flagship/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [flagship](plugins/flagship/README.md) · **Uses another AI**

Conduct a dozen concurrent Claude Code sessions as one portfolio — the layer above `ship-armada`, for when the work is already spread across live sessions rather than waiting in a repo's backlog. It builds a roster of every peer session, hands out a heavy-work token taken from `harbourmaster`'s measured berths rather than invented, batches their accumulated decisions so only the ones on your own axes reach you, and propagates each session's findings to the others — which is the return, because on the evening it was built nine sessions independently found the same tool's bug and none knew about the others. It starts new work as a workflow, a subagent, or a fresh Ghostty tab. It holds the map and no authority: it cannot command a peer, close a peer's channel to its user, or relay an authorisation, and all three were refused by the sessions on the receiving end.

<br clear="left" />

<a href="plugins/ship-armada/README.md"><img src="plugins/ship-armada/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-armada](plugins/ship-armada/README.md)

The portfolio-level orchestrator. Reads the manifest of record, verifies it against git, then surveys, plans, routes single directives into the right project's pipeline, and dispatches per-repo backlogs as dependency-ordered campaigns with capped concurrency.

<br clear="left" />

<a href="plugins/ship-feature/README.md"><img src="plugins/ship-feature/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-feature](plugins/ship-feature/README.md) · **Uses another AI**

The end-to-end conductor: one feature from rough idea to merged, verified code, running the shipyard stages in order with plan and design in parallel, a fresh-context cross-family verifier before merge, and a fail-closed gate where every box is checked now rather than recalled. A COMPLETE verdict is itself checked: over a bundle with a screenshot nothing corroborates, a suite whose green comes from an assertion that cannot fail, or a row citing no measurable value, the item does not advance.

<br clear="left" />

<a href="plugins/ship-fleet/README.md"><img src="plugins/ship-fleet/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-fleet](plugins/ship-fleet/README.md) · **Uses another AI**

The backlog orchestrator: surveys everything left in a repo, writes one durable ledger before any execution, then conducts concurrent ship-feature runners under a global agent budget, with per-item verification and merges serialized. Done means the ledger says so, never that a dispatch returned. A ready-to-verify report is treated as a claim about an evidence bundle, and where the repo carries a test campaign its capture gate runs once for the repo rather than once per item, because a fleet multiplies whatever the evidence layer gets wrong.

<br clear="left" />

<a href="plugins/shipyard/README.md"><img src="plugins/shipyard/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [shipyard](plugins/shipyard/README.md) · **Uses another AI**

The feature-delivery stage skills: intake, triage, plan, design, work, verify and gap-fix, on one tracker adapter and one complete status machine. Built on a 110-ticket audit of its predecessors, with typed evidence rules and a cross-family verifier as the only path to done. Typing the evidence settles what kind of thing closes a claim; 0.3.0 adds whether the thing is sound, so a screenshot proves what it depicts rather than being trusted on its filename, a suite is scanned for assertions that cannot fail before its green is spent, and a critic reading only the evidence bundle rejects any row that cites nothing measurable. The report card and blind-panel results ship in the repo.


<br clear="left" />

## Knowing where things stand

_What is finished, what is not, and what nobody has actually checked._

<br clear="left" />

<a href="plugins/dossier-report/README.md"><img src="plugins/dossier-report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [dossier-report](plugins/dossier-report/README.md)

A research question in, one published page out. It runs a paid and free research panel, reads every report end to end rather than the merged summary, turns the corpus into a list of claims with sources attached, then designs the page from scratch around its own subject so consecutive pages do not converge on one look. Every claim carries a citation you can open, and the build fails on one that does not resolve. The page now renders in three registers, Primer, Brief and Technical, and the reader chooses which one they're in; each is independently cited from that same registry, and where the backends disagreed, the disagreement survives into all three rather than being tidied away for the simpler one. A vertical rule has to sit in a real gap too, measured from the text's ink rather than from the box the padding was declared on; that check found twenty violations on a page this skill had already published. Every page now opens with a TLDR, and a buying question gets an actual answer: the categories buyers split on, three ranked picks in each, one overall winner with what it loses on. A ranking is reasoning rather than a measurement, so it renders as reasoning and names the claims it rests on, and a paywalled Which? or RTINGS verdict counts as evidence with the paywall stated instead of being dropped for an affiliate listicle. Pictures come from the sources with their provenance attached, charts go through dataviz in plain CSS, hand-drawn SVG or TanStack Charts compiled to static SVG at build time, and the motion layer is no longer optional.

<br clear="left" />

<a href="plugins/reckon/README.md"><img src="plugins/reckon/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [reckon](plugins/reckon/README.md)

Every remaining-work list is built by filtering — take everything, drop what's done, report the rest — and the filter is where it breaks, because "not done" and "not known" are different things that both look like absence. An ordinary campaign on a file-sync client: 58 designed cases, 25 reached a verdict, 32 blocked or inconclusive on a dead credential and on states no hook can force; 15 stated requirements, 2 independently observed. Filter that to failures and you get a tidy list of fourteen fixes that looks like a plan and is a list about 43% of the product. So this refuses to filter. Every brief, requirement, case, defect and surface resolves into exactly one class of a total partition, because an item can't fall out of a list with nowhere to fall to, and a blocked case classed as anything but unmeasured fails the gate by name. The class that earns its place is unmeasured, whose work isn't the feature's work at all: reaching a state, reading an answer, deciding what a pass would even look like are harness jobs, and one "test this properly" ticket sends five different jobs to the same wrong place, so each row carries its own remedy. Blocked cases are scheduled as the causes behind them rather than one by one — scrim's own stop declaration had a single dead credential behind ten of twenty — each with the coverage points resolving it returns, which is the number a solo developer actually prioritises on. Waivers stay visible as exceptions instead of folding into done, because the reason for a waiver expires. Briefs the campaign proves finished get retired rather than rebuilt, but never on a presence-rung oracle or a guessed join, since retiring deletes somebody's stated intent. Five denominators that disagree with each other on purpose, every one marked a floor, and never one blended percent. And a ratchet across runs, because a snapshot gate catches a bad report while the slow failure is an item quietly reclassified until nothing remembers it was never checked. Twenty-one self-tests prove each gate fires on a broken ledger and stays silent on a sound one.

<br clear="left" />

<a href="plugins/report/README.md"><img src="plugins/report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [report](plugins/report/README.md)

A session works something out over two hours, you ask for the write-up, and what comes back reads well and can't be checked. Three different things leave a session looking identical on the page: a number that was measured, one read off a single sample, and one worked out from two other facts. This compiles the session's own evidence trail into a claim ledger before it designs anything, so the page is generated from the ledger rather than cited afterwards, and reasoning renders visibly as reasoning. It now writes the same argument three ways over that one ledger, Primer, Brief and Technical; each is independently and fully cited from the same registry, and switching between them works with JavaScript off. A reading can change the words; it can't change what's claimed, so the confidence and the limits travel into all three. One self-contained HTML file that paginates to a real A4 PDF with the motion stripped out, plus a one-page TLDR derived from the same ledger so the two can't disagree. Its own blind panel went 4-2 for it and told it what it was missing: an ask. So the TLDR is now a named section carrying one, and on a comparison the ask is the verdict itself: the categories readers split on, three ranked picks in each, one winner sized and owned. Rankings render as reasoning and name their ledger rows; paywalled lab testing counts as evidence with the paywall stated; pictures come from the evidence trail with provenance; and charts build in plain CSS, hand-drawn SVG or TanStack Charts compiled to static SVG, so nothing loads at runtime and it all still prints.

<br clear="left" />

<a href="plugins/stocktake/README.md"><img src="plugins/stocktake/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [stocktake](plugins/stocktake/README.md) · **Uses another AI**

A board is a set of claims about a codebase, and nobody checks them. Cards drift into review and stay there, work gets finished on a branch nobody merged, and a ticket reads as done because somebody wrote a comment saying so. The uncomfortable part is that checking looks like it already happened: the surface renders, the schema validates, the suite is green, and none of that is the same as the number on the screen having been produced by code somebody wrote. So this goes card by card and, before it opens any diff, rebuilds the numbered requirement list from the description, every comment and every attached image, because a diff read first supplies the frame, and whatever the change quietly dropped never enters the list. Then it finds where the work actually is (merged, on a branch nobody merged, finished but never pushed, in a worktree, or never started, which are four different problems), traces each requirement to the code that produces its value rather than the screen that shows it, and asks whether the tests behind it could ever have failed: which rung of oracle each one stands on, armed and unarmed assertions counted apart, and a denominator for what the gate really runs. It grades out of family with one judge rather than a panel, because nine frontier judges across seven families supply about two independent votes and the best single judge beats the group. “I could not tell” is a real answer that blocks rather than rounding up. Cards with work left get a brief for ship-fleet; cards with an open question get it referred or decided with a reason instead of parked on you; and at Done it stops deciding and asks the warrant plugin, which holds the authority: Verified where that class of work has earned warrant’s top tier with nothing revoked, Needs More Work where one of warrant’s own checks failed on the card’s evidence and is quoted onto it, and Done with every reason named otherwise, which is the default. A grant states what it rests on every time, because a warrant tier is earned by nothing having escaped rather than by anyone measuring the machine, and the signature on the warrant is the one part nobody automated away.

<br clear="left" />

<a href="plugins/trawl/README.md"><img src="plugins/trawl/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [trawl](plugins/trawl/README.md)

Divergent ideation that converges on something you can ship. Isolated thinkers under genuinely different frames, the obvious answer written down first, and a creative pick recommended only when it beats that answer blind. Receipts committed: structural evals (96.4% vs its predecessor's 49.0%), a four-judge blind panel, and the research corpus it was built from.

<br clear="left" />

<a href="plugins/whats-left/README.md"><img src="plugins/whats-left/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [whats-left](plugins/whats-left/README.md)

Asks what's left on a project and gets back two documents that immediately start lying to each other: the status report says a feature shipped, the open questions ask whether to switch it on, and nothing shows you the second is why the first is wrong. This is one page where they're the same graph: every blocked item links down to the decision that releases it, every decision links back up and says how much it actually releases. Stage is a word rather than a percentage, so built, deployed and accepted stay three different things instead of averaging into ninety per cent. Agreeing with a recommendation means clicking the option already selected, which fires no change event and is exactly how a page exports your agreement as "never looked at", so confirmation is bound to the click too, and anything you never touch exports as unconfirmed rather than as your decision. Send the JSON back and it does the work your answers unblocked. Six structural properties to nil against the same request with no skill at all.


<br clear="left" />

## Keeping a long job alive

_For work that outlasts one sitting, one usage limit, or one crash._

<br clear="left" />

<a href="plugins/better-goal/README.md"><img src="plugins/better-goal/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [better-goal](plugins/better-goal/README.md)

`/goal` looks like it keeps working until the job is done, and it does not: the condition is judged by a small model reading the transcript, so it grades what the run said rather than what is true, and Claude Code overrides the hook after eight consecutive blocks and reports that turn as completed. Nine turns of real work trips it, silently. This arms its own guard instead, a command Stop hook that runs the gates and decides by exit code, plus a watcher outside the turn loop, because a run that dies mid-turn never reaches a Stop hook at all. It also knows when to give up: a gate failing identically turn after turn disarms the run rather than re-sending the same failure at the price of the whole session prefix. Built from 114 real goal runs, where the most common follow-up was the word "resume", six times in a row.

<br clear="left" />

<a href="plugins/better-loop/README.md"><img src="plugins/better-loop/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [better-loop](plugins/better-loop/README.md)

A loop that fires on a clock re-sends the same unmet condition and the same six failing tasks turn after turn, and each fire re-bills the session's whole accumulated prefix, and five of twelve heavy sessions did that and accounted for 91% of input between them. Nothing about a smaller context window stops a loop from restarting. So this arms a watcher instead of a schedule: it polls one deterministic probe command in the background, wakes the session only when the answer changes, sends the delta rather than the state, and goes progressively quieter about a failure it has already reported. A quiet system costs nothing at all, and a tick that needs no conversation can run detached, where there is no prefix to pay for.

<br clear="left" />

<a href="plugins/braindump/README.md"><img src="plugins/braindump/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [braindump](plugins/braindump/README.md)

Gets everything load-bearing out of a session and onto the page before the context holding it is thrown away. Measured across 121 real compaction events, the built-in prompt keeps 0.3% of the approaches you ruled out and 33.8% of your standing constraints; violations run 0% when a rule survives into the summary and 38% when it doesn't. Writes a pinned verbatim tier ahead of the narrative, and ships a deterministic scorer plus a head-to-head benchmark whose baseline arm costs nothing. Published as `compaction-quality` until 2026-08.

<br clear="left" />

<a href="plugins/recover-claude-code/README.md"><img src="plugins/recover-claude-code/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [recover-claude-code](plugins/recover-claude-code/README.md)

A terminal crash leaves every transcript, workflow journal and subagent context on disk but unattached. Reopening the sessions is the easy half; the half that goes wrong is the work that was in flight, because an agent still running when the process died restarts from its original prompt with an empty head and re-derives what its predecessor had already closed. This reattaches instead: a dead subagent's transcript is a sidechain, so rewriting three fields makes it resume with the files it read and the findings it closed intact. It refuses to touch a session that is still live, and refuses to fabricate a journal result to make a resume look clean.

<br clear="left" />

<a href="plugins/resume-session/README.md"><img src="plugins/resume-session/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [resume-session](plugins/resume-session/README.md)

When an AI coding session ends unexpectedly (a token limit, an API timeout, an unexpected context compaction, or simply switching between tools like Claude Code, Antigravity, Cursor, Codex, or Grok), the next agent typically starts blind. This scans your local machine to discover past sessions across all major agent CLIs, parses their exact transcripts on disk, extracts the 6-dimensional takeover state (original goal, terminal errors, modified files, config keys, decisions, and immediate next steps), and produces an uncorrupted continuity handover without redundant re-discovery.

<br clear="left" />

<a href="plugins/should-compact/README.md"><img src="plugins/should-compact/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [should-compact](plugins/should-compact/README.md)

Scores 0-10 whether now is a good moment to compact, and says why in one line. It judges the seam in the work rather than the fullness of the window: an open tool chain or a half-finished edit is a hard zero however full the context is, and that one signal decided 98.07% of holds across 1,089 measured turns. Reads only a hot buffer plus an append-only session log it maintains itself, so it is cheap enough for Haiku and fast enough to sit in a `PreCompact` hook, where it can veto an ill-timed automatic compaction. It never vetoes at the wall, because blocking at 99.8% full loses the session rather than saving it. Beat the no-skill baseline 10-0 on a two-family blind panel.


<br clear="left" />

## Fewer interruptions

_When Claude should ask you, which AI answers, and what it all costs._

<br clear="left" />

<a href="plugins/clarify/README.md"><img src="plugins/clarify/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [clarify](plugins/clarify/README.md) · **Uses another AI**

Decides whether to interrupt you at all, and mostly the answer is no. It sweeps the conversation and the repo for the answer first, drops anything whose answer wouldn't change the work, then sends what's left to a different model family before it ever reaches you: fable-5 for speed, gpt-5.6-sol, gemini-3.7 and grok-4.6 at xhigh for independence, a three-family panel when the call is open enough to deserve one. Each lane pins its model and its effort, because a lane that inherits its config default isn't the lane you picked. Then the last gate, which isn't "are you sure" but "whose decision is this": if the axis is craft or convention it gets settled and reported in a clause, and only taste, cost, scope, risk and the genuinely irreversible reach you. Two options, and no recommendation to nudge you, since the fork it could have recommended on was one it should have taken. A mark now appears on one shape of question only, the one you're asked despite the agent knowing the answer because the action can't be undone. Two out-of-family reviewers argued against the two-option default and their reports ship with it; one of them changed the gate, and the other is a cost written into the evidence file rather than talked around.

<br clear="left" />

<a href="plugins/defer/README.md"><img src="plugins/defer/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [defer](plugins/defer/README.md)

The one place that decides which model a piece of work goes to, so fourteen skills stop each deciding it separately and slightly differently. Six task classes across seven lanes and five families, each pinned to a model *and* an effort: sol never runs at max because it's the referral lane at medium, Fable judges forks but never grades a ticket, design review stays on Opus and Fable, and grok runs at xhigh. Where several lanes are eligible it doesn't pick the best one, it picks the one with the most plan headroom per remaining day — because 60% used with six days left is tighter than 80% that resets tonight — and when two are within 20% the tie breaks on published price rather than on sort order. It's careful about which numbers are real: Claude and Codex both report a utilization percentage the vendor computed, already sitting on disk, while Grok, GLM and Gemini expose no quota to any CLI at all, so those are counted locally, labelled Tier 2, and calibrated from a percentage you read yourself rather than from someone's estimate of your plan. The `api` hook for a real quota endpoint ships deliberately unwired, because a guessed URL turns "we can't measure this" into a confident wrong number. Then it proves the lane ran, which matters most for GLM: that lane is Claude Code with `X-Perch-Binding: glm` on it, and without the header the identical command runs Claude, succeeds, and hands back something plausible.

<br clear="left" />

<a href="plugins/discipline/README.md"><img src="plugins/discipline/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [discipline](plugins/discipline/README.md)

Drop a short block at the top of a session and Claude spends less without doing less. It targets the three habits that quietly run up the bill: re-printing plans and diffs already on your screen, opening a whole file to find one line, and handing small jobs to sub-agents that each pay for a fresh context. The nearest alternative is caveman, and the choice between them is measured rather than argued. On the same 106 tasks caveman cut output tokens 41% against this skill's 16%, so caveman is better at the thing both are for. It also gave up 7.6 points of task score where this one gives up nothing detectable, because 78% of caveman's saving came from the agent taking fewer steps rather than writing more tersely. Pick caveman if the token count is all you are optimising; pick this one if the agent is doing long work you intend to trust.


<br clear="left" />

## Making your own skills

_Turn something you do often into a skill you can reuse._

<br clear="left" />

<a href="plugins/create-skill/README.md"><img src="plugins/create-skill/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-skill](plugins/create-skill/README.md)

The sibling of improve-skill, for when there is nothing to improve yet. It interviews you properly first, because an unstated intention is the usual reason a new skill misses, then researches the domain, builds through skill-creator with every rule traced to evidence, and proves it against the honest baseline: the same prompts with no skill at all.

<br clear="left" />

<a href="plugins/geminify/README.md"><img src="plugins/geminify/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [geminify](plugins/geminify/README.md) · **Uses another AI**

A skill is a prompt, and most skills here were tuned against a Claude model's habits. Point this one at any of them and it writes the sibling `gemini.md` that recalibrates it for Gemini: every categorical scope in the target turned into a counted row, the verification put back with its command attached, and every claim about Gemini tagged with whether Google published it, someone measured it, or you reasoned your way to it. A script checks each quoted claim appears verbatim in Google's own corpus, because a paraphrase in quotation marks got attributed to them three times before it existed.

<br clear="left" />

<a href="plugins/improve-skill/README.md"><img src="plugins/improve-skill/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [improve-skill](plugins/improve-skill/README.md)

The pipeline that built half this marketplace, as a skill. Point it at an existing skill plus your complaints; it runs paid and free deep research, rebuilds the skill with every change traced to evidence, proves the rebuild with comparative evals and a blind multi-family judge panel, then ships the full brand treatment. You choose the name and the icon concept before anything gets generated.


<br clear="left" />

## Sending things to people

_Work that leaves your machine and reaches somebody._

<br clear="left" />

<a href="plugins/email-digest/README.md"><img src="plugins/email-digest/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [email-digest](plugins/email-digest/README.md)

A digest goes out with twenty-four items, somebody calls it unreadable, and the obvious fix is fewer items. That fix is wrong and there is a lot of evidence saying so: MailerLite's 317,000 campaigns and 2.9 billion emails put the twenty-one-or-more-links bucket at the highest click-to-open rate in the whole dataset, and the choice-overload meta-analysis pools across 63 conditions to a mean effect size of virtually zero. The defect is that every item costs the reader the same effort to evaluate inside about fifty-one seconds, with nothing on the page saying where to stop, so this tiers the list rather than trimming it and the item count stays whatever it is. The absence of a cap is itself asserted as a rule, because a cap is the first thing anybody reintroduces from instinct. Sixteen gate checks, each tracing to a source: anchor links that do not act on iPhones where Apple is 62% of opens and cannot be tracked where they do; layout tables missing the role that stops a screen reader reading your scaffolding aloud, which 86% of a 443,585-email audit fails; SVG, which Gmail deletes outright rather than degrading; dark-mode meta tags without dark styles, which is worse than no tags because Apple Mail leaves you alone without them and partially inverts you with them; and centred body text, which nobody writes deliberately because the markup that centres the card cascades into everything inside it. It refuses to gate a text-to-image ratio: Email on Acid tested against twenty-three spam filters and above 500 characters the ratio makes no difference, so it checks the email still works with every image stripped instead, which is the thing that actually breaks. Nobody has published a test of tiered against flat, all four research backends went looking, and the skill says so rather than dressing an inference as a measurement.

<br clear="left" />

<a href="plugins/mac-design-digest/README.md"><img src="plugins/mac-design-digest/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-design-digest](plugins/mac-design-digest/README.md)

Maintains a machine-written corpus of macOS design evidence across sessions, reading screenshots, kits and design files, and writing findings that the interface skills then build against. Provenance is a type system rather than a habit: two orthogonal mark families compose, one for how precisely a value is known and one for how strongly, with promotion running along the strength axis only, so a guess never becomes a specification by being seen more often. Its gate enforces seventeen parser invariants, because a wrong number in a corpus outlives the conversation that created it. The result worth reading is a loss: its rebuild improved its structural assertions from 35 to 43 and then lost its blind panel 4-1, because having built a check for a class of problem it stopped looking past the check. Two of the three defects the panel found became checks the same day, which took a defective fixture from 10 failures to 17 and immediately revealed that its own clean control was incomplete. The third became a rule, that the gate is a floor and not a ceiling, carrying that panel loss as its evidence.


<br clear="left" />

## Looking after your Mac

_Stop it grinding to a halt while all this is running._

<br clear="left" />

<a href="plugins/harbourmaster/README.md"><img src="plugins/harbourmaster/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [harbourmaster](plugins/harbourmaster/README.md) · **Uses another AI**

Decides where a piece of work should run, and whether this Mac can carry it yet. Routes across five execution planes — this machine, a container on another machine, a native-app instrument session, another model, or in-session subagents — by spending whichever resource is least scarce rather than whichever is nearest to hand. Governs the local one with berth admission: heavy work runs through a wrapper that holds its slot on a file lock the kernel returns when the work ends, refuses in bounded time instead of hanging past a tool timeout, and runs under a macOS priority class that its child processes inherit — so wrapping a build also wraps the sixteen compilers it starts. Detects sustained thermal limiting from per-cluster frequency residency, the only method that works on a Mac where every signal the OS reports stays silent while the die sits at 111 °C.

<br clear="left" />

<a href="plugins/mac-doctor/README.md"><img src="plugins/mac-doctor/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-doctor](plugins/mac-doctor/README.md)

Your Mac did not fill up because of one thing, it filled up because a hundred sensible defaults each left something behind and nothing was counting. Five scheduled jobs, from every fifteen minutes to weekly, with what each may do on its own widening as the gap between runs grows. Running low makes it check sooner, never delete more. The two short tiers are plain shell, so ninety-six runs a day cost no tokens at all. It ties a no-skill baseline on reasoning and says so in its evals; what it adds is that the reasoning runs while you are asleep.


## Licence

MIT. Do what you like; attribution appreciated.

## Elsewhere

Fledgeling is [Luke Rhodes](https://www.linkedin.com/in/lukerhodes/), also co-founder of [Diolog](https://diolog.app).

[fledgeling.app](https://www.fledgeling.app) · [GitHub](https://github.com/lprhodes) · [X](https://x.com/lp_rhodes) · [LinkedIn](https://www.linkedin.com/in/lukerhodes/) · [hello@fledgeling.app](mailto:hello@fledgeling.app)
