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

Fifty-odd skills is a lot to meet at once, so they are grouped by what you are trying to do rather than by how they work. Every one carries its own README, and the ones marked **Uses multiple models** may ask an AI outside Claude's family for a second opinion, because a reviewer from the same family tends to agree with it. [`defer`](plugins/defer/README.md) decides which one.


<br clear="left" />

## Making something

_Design it, write it, or build it from nothing._

<br clear="left" />

<a href="plugins/agent-voice/README.md"><img src="plugins/agent-voice/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [agent-voice](plugins/agent-voice/README.md)

Claude writes in a default voice nobody chose. This gives it one, and it writes differently depending on whether a person or another AI is reading, because the two go wrong in different ways. Mostly it means shorter replies that do the same work.

<br clear="left" />

<a href="plugins/create-mac-icon/README.md"><img src="plugins/create-mac-icon/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-mac-icon](plugins/create-mac-icon/README.md)

A proper Mac app icon rather than a picture of one. It studies 532 real icons, generates several takes three different ways, then keeps reworking the winner until it holds up at every size it will actually be seen at.

<br clear="left" />

<a href="plugins/create-swe-project/README.md"><img src="plugins/create-swe-project/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-swe-project](plugins/create-swe-project/README.md)

Turns an idea into a project you can open and run. One conversation up front, then it builds the lot: the app, sign-in, an admin area, tests, and everything needed to put it online.

<br clear="left" />

<a href="plugins/deck-craft/README.md"><img src="plugins/deck-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [deck-craft](plugins/deck-craft/README.md)

Builds, reviews and converts slide decks, including PowerPoint you can still edit afterwards. It checks what nobody catches by eye, like text too small to read from the back of the room, and it will not report a pass on a check that never ran.

<br clear="left" />

<a href="plugins/design-craft/README.md"><img src="plugins/design-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [design-craft](plugins/design-craft/README.md)

Designs a screen the way a designer would rather than the way a code generator does. It works out what everything else in the category looks like and deliberately goes elsewhere, then checks its own colours are actually readable instead of assuming.

<br clear="left" />

<a href="plugins/generate-investor-portal/README.md"><img src="plugins/generate-investor-portal/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [generate-investor-portal](plugins/generate-investor-portal/README.md)

Builds a shareholder portal out of a company's own documents. Its main job is refusing to invent anything: a figure with no traceable source is blocked outright, and a number that genuinely is not available is labelled as missing rather than guessed.

<br clear="left" />

<a href="plugins/mac-craft/README.md"><img src="plugins/mac-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-craft](plugins/mac-craft/README.md)

Designs and reviews Mac app screens against Apple's own published values, not web habits that happen to run on a Mac. It caught one of its own builds putting text on a background of exactly the same colour, invisible, while reporting a perfect score.

<br clear="left" />

<a href="plugins/tui-craft/README.md"><img src="plugins/tui-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [tui-craft](plugins/tui-craft/README.md)

For apps that run in a terminal window. It does the character counting nobody gets right by hand, then checks what the terminal actually drew: a box that never closes, a row shoved out of line by an emoji, text cut off with nothing saying so.

<br clear="left" />

<a href="plugins/ux-craft/README.md"><img src="plugins/ux-craft/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ux-craft](plugins/ux-craft/README.md)

The other half of design-craft: how a thing behaves rather than how it looks. Flows, forms, error states, the wording on buttons, and whether a person can really tap the thing on a phone.


<br clear="left" />

## Checking it before anyone sees it

_Catch the problems while they are still cheap to fix._

<br clear="left" />

<a href="plugins/be-my-witness/README.md"><img src="plugins/be-my-witness/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [be-my-witness](plugins/be-my-witness/README.md)

Looks at a screenshot and tells you what is genuinely in it. Handy when a test says it passed and you want to know whether the screen really showed what it was meant to. It crops in rather than squinting at a thumbnail.

<br clear="left" />

<a href="plugins/code-review/README.md"><img src="plugins/code-review/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [code-review](plugins/code-review/README.md) · **Uses multiple models**

Reviews a change and, unusually, tells you what it did not look at. Three findings then silence could mean the rest is clean or that it never opened those files. So every run ends with what it checked, what it could not, and why.

<br clear="left" />

<a href="plugins/design-review/README.md"><img src="plugins/design-review/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [design-review](plugins/design-review/README.md)

The last look before you see AI-built screens yourself. Automatic checks first (can people read it, can they tap it), then judged passes on whether it hangs together, with fixes you can paste and an honest list of what nobody checked.

<br clear="left" />

<a href="plugins/mockup-fidelity/README.md"><img src="plugins/mockup-fidelity/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mockup-fidelity](plugins/mockup-fidelity/README.md)

Does the thing that got built actually match the design? It measures rather than eyeballs, treats the design as correct, and assumes a difference is a mistake until something proves it deliberate. What it cannot measure is never counted as a match.

<br clear="left" />

<a href="plugins/proctor/README.md"><img src="plugins/proctor/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [proctor](plugins/proctor/README.md)

Drives a Mac app the way an instrument does. It works windows sitting behind others or on another desktop without stealing your screen, so you can carry on using the machine while it runs. And when it waits, it names what it waited for.

<br clear="left" />

<a href="plugins/test-campaign/README.md"><img src="plugins/test-campaign/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [test-campaign](plugins/test-campaign/README.md)

Runs a round of testing and leaves behind a page saying what it genuinely proved. It reads what the product is meant to do before looking at what got built, which is the only way to notice a feature the design asked for and nobody made.

<br clear="left" />

<a href="plugins/vouch/README.md"><img src="plugins/vouch/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [vouch](plugins/vouch/README.md)

Checks an expense claim against the actual invoices rather than the bank feed. On a real claim it found two stretches of 38 and 44 days where a card recorded nothing at all, and eleven rows worth A$1,579.45 that four earlier reviews had missed.

<br clear="left" />

<a href="plugins/warrant/README.md"><img src="plugins/warrant/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [warrant](plugins/warrant/README.md)

Writes down exactly what a machine is allowed to sign off without you, then takes that permission back on its own when something slips through or the model changes underneath it. You read one ledger instead of checking every item yourself.


<br clear="left" />

## Handing over a pile of work

_Give Claude a list and let it work through it on its own._

<br clear="left" />

<a href="plugins/anvil-errand/README.md"><img src="plugins/anvil-errand/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [anvil-errand](plugins/anvil-errand/README.md)

Sends a job to another machine you own, a spare PC or a node, so your Mac stays free. Before anything starts it checks every link in the chain and names the first missing piece, rather than failing halfway through for a misleading reason.

<br clear="left" />

<a href="plugins/armada-sync/README.md"><img src="plugins/armada-sync/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [armada-sync](plugins/armada-sync/README.md)

After you finish something anywhere in your portfolio, this updates that one project's entry in your notes, stamps it fresh, and stops. The smallest thing here, deliberately.

<br clear="left" />

<a href="plugins/atlas-publish/README.md"><img src="plugins/atlas-publish/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [atlas-publish](plugins/atlas-publish/README.md)

The one plugin here built for a single app. It walks a release right up to the moment of going live and then stops, because putting something in front of users is your call rather than its.

<br clear="left" />

<a href="plugins/flagship/README.md"><img src="plugins/flagship/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [flagship](plugins/flagship/README.md) · **Uses multiple models**

For when you already have a dozen Claude sessions running at once. It tracks what each is doing, works out how much your Mac can carry, batches their questions so only the ones needing your judgement reach you, and tells each what the others found.

<br clear="left" />

<a href="plugins/ship-armada/README.md"><img src="plugins/ship-armada/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-armada](plugins/ship-armada/README.md)

Works across every project you have rather than one. It reads your portfolio notes, checks them against what is really in each repo, then plans and hands out work a few projects at a time.

<br clear="left" />

<a href="plugins/ship-feature/README.md"><img src="plugins/ship-feature/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-feature](plugins/ship-feature/README.md) · **Uses multiple models**

Takes one feature from a rough idea to finished, verified code. A different AI family checks the work before anything merges, and a claim of done has to survive being checked itself.

<br clear="left" />

<a href="plugins/ship-fleet/README.md"><img src="plugins/ship-fleet/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-fleet](plugins/ship-fleet/README.md) · **Uses multiple models**

Hand it a repo's whole backlog and it works through it. It writes down everything left before starting anything, runs several items at once, and done means the written record says so rather than a job simply returning.

<br clear="left" />

<a href="plugins/shipyard/README.md"><img src="plugins/shipyard/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [shipyard](plugins/shipyard/README.md) · **Uses multiple models**

The individual stages of getting a feature built: sorting it, planning it, designing it, doing it, then checking it. Reach for one when you only need that step. Nothing reaches done until an AI from another family has graded it.


<br clear="left" />

## Knowing where things stand

_What is finished, what is not, and what nobody has actually checked._

<br clear="left" />

<a href="plugins/dossier-report/README.md"><img src="plugins/dossier-report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [dossier-report](plugins/dossier-report/README.md)

Ask a research question, get back a proper page you can share. It runs several research services, reads every report end to end, and gives you the same findings written three ways so you pick the depth. Every claim carries a link you can open.

<br clear="left" />

<a href="plugins/reckon/README.md"><img src="plugins/reckon/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [reckon](plugins/reckon/README.md)

Answers what is actually left, and refuses to blur not done with nobody checked. Every item lands in exactly one category so nothing quietly falls off the list, and it never hands you a single percentage that averages the difference away.

<br clear="left" />

<a href="plugins/report/README.md"><img src="plugins/report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [report](plugins/report/README.md)

You ask for the write-up after a long session and get something that reads well and cannot be checked. This builds the page from the session's own evidence, so a measured number, a single sample and a piece of reasoning stop looking identical.

<br clear="left" />

<a href="plugins/stocktake/README.md"><img src="plugins/stocktake/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [stocktake](plugins/stocktake/README.md) · **Uses multiple models**

A project board is a set of claims about the code, and nobody checks them. This goes card by card and finds where the work really is: merged, sitting on a branch nobody merged, finished but never pushed, in progress, or never started.

<br clear="left" />

<a href="plugins/trawl/README.md"><img src="plugins/trawl/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [trawl](plugins/trawl/README.md)

For when you want more than the first idea. It thinks through several genuinely different angles separately, writes the obvious answer down first, and only recommends something more creative when it beats that obvious answer blind.

<br clear="left" />

<a href="plugins/whats-left/README.md"><img src="plugins/whats-left/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [whats-left](plugins/whats-left/README.md)

Asks what is left and gives you one page where the status and the open questions stop contradicting each other. Every blocked item links down to the decision that would release it, and every decision says how much it actually releases.


<br clear="left" />

## Keeping a long job alive

_For work that outlasts one sitting, one usage limit, or one crash._

<br clear="left" />

<a href="plugins/better-goal/README.md"><img src="plugins/better-goal/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [better-goal](plugins/better-goal/README.md)

Keeps a job running until it is genuinely finished. The built-in version looks like it does this and does not; it gives up quietly after eight rounds and reports the run as complete. This one checks the real result, and knows when to stop.

<br clear="left" />

<a href="plugins/better-loop/README.md"><img src="plugins/better-loop/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [better-loop](plugins/better-loop/README.md)

For work that needs checking on again and again. Rather than waking on a timer and re-reading everything each time, it watches quietly in the background and only interrupts when the answer changes. A quiet system costs you nothing at all.

<br clear="left" />

<a href="plugins/braindump/README.md"><img src="plugins/braindump/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [braindump](plugins/braindump/README.md)

Gets everything important out of a session and onto the page before the older part of the conversation is thrown away. Measured across 121 real cases, what Claude does by default keeps almost none of the approaches you had already ruled out.

<br clear="left" />

<a href="plugins/recover-claude-code/README.md"><img src="plugins/recover-claude-code/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [recover-claude-code](plugins/recover-claude-code/README.md)

Your terminal crashed and it is all still on disk, just unattached. Reopening the sessions is the easy half. This also reattaches the work that was mid-flight, so it carries on with what it had already worked out instead of starting again empty-handed.

<br clear="left" />

<a href="plugins/resume-session/README.md"><img src="plugins/resume-session/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [resume-session](plugins/resume-session/README.md)

Picks up where a previous AI session left off, including one from a different tool entirely. It reads the transcripts already on your machine and works out the goal, the errors, the files touched and the decisions made, so nobody rediscovers it all.

<br clear="left" />

<a href="plugins/should-compact/README.md"><img src="plugins/should-compact/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [should-compact](plugins/should-compact/README.md)

Scores out of ten whether now is a good moment to trim the conversation, and says why in a line. It looks at whether you are mid-thought rather than how full the window is, and never blocks right at the end, which loses the session rather than saving it.


<br clear="left" />

## Fewer interruptions

_When Claude should ask you, which AI answers, and what it all costs._

<br clear="left" />

<a href="plugins/clarify/README.md"><img src="plugins/clarify/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [clarify](plugins/clarify/README.md) · **Uses multiple models**

Decides whether to interrupt you at all, and mostly the answer is no. It hunts for the answer in the conversation and the code first, then asks a different AI, so only the genuinely yours reach you: taste, cost, risk, and the irreversible.

<br clear="left" />

<a href="plugins/defer/README.md"><img src="plugins/defer/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [defer](plugins/defer/README.md)

One place that decides which AI a job goes to, so a dozen skills stop each deciding it slightly differently. It picks whichever has the most headroom left on your plan rather than whichever is best, then proves the job really ran where it said.

<br clear="left" />

<a href="plugins/discipline/README.md"><img src="plugins/discipline/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [discipline](plugins/discipline/README.md)

Drop a short block at the top of a session and Claude spends less without doing less. It targets re-printing what is already on your screen and opening a whole file to find one line. There is a blunter alternative, and this says where that one wins.


<br clear="left" />

## Making your own skills

_Turn something you do often into a skill you can reuse._

<br clear="left" />

<a href="plugins/create-skill/README.md"><img src="plugins/create-skill/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-skill](plugins/create-skill/README.md)

For building a skill that does not exist yet. It interviews you properly first, because not saying what you actually wanted is the usual reason a new one misses, then proves it earns its place by running the same prompts with no skill at all.

<br clear="left" />

<a href="plugins/geminify/README.md"><img src="plugins/geminify/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [geminify](plugins/geminify/README.md) · **Uses multiple models**

The skills here were written against Claude's habits. Point this at one and it writes a companion version tuned for Gemini instead, then checks every claim it makes about Gemini against what Google actually published.

<br clear="left" />

<a href="plugins/improve-skill/README.md"><img src="plugins/improve-skill/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [improve-skill](plugins/improve-skill/README.md)

The pipeline that built half of this marketplace. Point it at a skill plus your complaints and it researches, rebuilds, proves the rebuild is better with independent judges, then does the icon and the write-up. You choose the name before anything gets made.


<br clear="left" />

## Sending things to people

_Work that leaves your machine and reaches somebody._

<br clear="left" />

<a href="plugins/email-digest/README.md"><img src="plugins/email-digest/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [email-digest](plugins/email-digest/README.md)

Builds an email digest people actually read. When one gets called unreadable the instinct is fewer items, and the evidence says that is the wrong fix, so it ranks them instead and leaves the count alone. Sixteen checks for the things that break email silently.

<br clear="left" />

<a href="plugins/mac-design-digest/README.md"><img src="plugins/mac-design-digest/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-design-digest](plugins/mac-design-digest/README.md)

Keeps a running set of notes on how Mac apps are designed, built from real screenshots and design files, which the other design skills then work from. It tracks how confidently each thing is known, so a guess never quietly hardens into a rule.


<br clear="left" />

## Looking after your Mac

_Stop it grinding to a halt while all this is running._

<br clear="left" />

<a href="plugins/harbourmaster/README.md"><img src="plugins/harbourmaster/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [harbourmaster](plugins/harbourmaster/README.md) · **Uses multiple models**

Works out where a job should run and whether your Mac can take it yet. It can send work to another machine, to another AI, or run it here under a limit, and it spots your Mac throttling itself while macOS reports nothing wrong.

<br clear="left" />

<a href="plugins/mac-doctor/README.md"><img src="plugins/mac-doctor/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-doctor](plugins/mac-doctor/README.md)

Your Mac did not fill up because of one thing; a hundred sensible defaults each left something behind and nothing was counting. This checks on a schedule and clears up after them. Running low makes it look sooner, never delete more.


## Licence

MIT. Do what you like; attribution appreciated.

## Elsewhere

Fledgeling is [Luke Rhodes](https://www.linkedin.com/in/lukerhodes/), also co-founder of [Diolog](https://diolog.app).

[fledgeling.app](https://www.fledgeling.app) · [GitHub](https://github.com/lprhodes) · [X](https://x.com/lp_rhodes) · [LinkedIn](https://www.linkedin.com/in/lukerhodes/) · [hello@fledgeling.app](mailto:hello@fledgeling.app)
