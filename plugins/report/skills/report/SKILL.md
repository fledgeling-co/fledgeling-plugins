---
name: report
description: Turn what a Claude session already worked out into a designed, cited report — one self-contained HTML page that reads as a rich scrolling document on screen and paginates to a clean A4 PDF, plus a stripped-back one-page TLDR. Compiles the session's own evidence trail (files read, commands run, research already in the repo, URLs fetched) into a claim ledger first, so every number and attribution carries a locator and anything reasoned is labelled as inference. Leads with the conclusion, cites claim-locally with source popups and a persistent registry, uses the project's DESIGN.md when one exists and generates one from the topic when it doesn't, and keeps motion on screen and out of the print. Use this whenever someone wants what just happened written up — "write this up as a report", "give me a summary with a TLDR at the top", "/report", "/report tldr", "turn this session into something I can send", "make me a page about what we found", "I need a one-pager on this for the team", "document this investigation properly" — and also when they ask for charts, visualisations or a PDF of work the session already did. Prefer this over a plain markdown summary whenever the write-up needs to look designed, needs citations, or needs to leave the terminal. Not for research that has not happened yet (use dossier-report), Diolog-branded A4 guides (use create-diolog-guides), or slide decks (use deck-craft).
---

# Writing the session up

One session in, one report out: argued from what the session actually
established, designed around its own subject, and written to disk as a
page you can read and a PDF you can send.

## The failure this exists to prevent

A session reads forty files, runs a dozen commands, and reaches a
conclusion. Asked for a write-up, the obvious move is to narrate the
conclusion in confident prose. The result reads well and is unusable,
because three very different things render identically:

- **"the queue drops 12% of events"** — measured, from a command whose
  output is in the transcript
- **"the queue drops 12% of events"** — read off one log sample and
  generalised
- **"the queue drops 12% of events"** — inferred from two facts that were
  each established separately

A week later nobody can tell which. Neither can the person you sent it
to, and they have less reason to trust you than you do.

So the spine of this skill is: **compile the ledger before you design
anything.** Every claim gets a locator or a label. The citation UI is
then generated from the ledger rather than retrofitted onto finished
prose, which is the only way the two stay honest with each other.

`references/evidence.md` carries the research behind every rule below.
Read it when you need to justify or tune a rule, not on every run.

## The shape of a run

| # | Phase | Routes to |
|---|---|---|
| 0 | Scope the report | — |
| 1 | Harvest the evidence trail into a claim ledger | — |
| 2 | Resolve the design system | project `DESIGN.md`, or `design-craft` |
| 3 | Compose the argument as page-safe blocks | `ux-craft` |
| 4 | Build the page | `design-craft`, `create-luke-content`, `dataviz` |
| 5 | Derive the TLDR one-pager | — |
| 6 | Export, audit, fix | `scripts/`, `design-review` |

Output lands in `<project>/docs/reports/<slug>/`. The run ends when the
files are written. Publishing and deploying are somebody's deliberate
next act, not this skill's.

**`/report tldr` asks for the one-pager, so the one-pager is the
deliverable.** Phases 0 to 2 still run in full, because the ledger and the
design system are what the one-pager is built from. Phases 3 and 4 shrink
to whatever the single page needs. Build the long report as well only if
the argument turned out to need more room than one sheet gives it, and say
so rather than shipping it silently.

## Phase 0 — Scope it from what you already have

Answer these from the conversation before asking anything:

- **What is the report about**, and what is its one-sentence finding?
- **Who reads it** — the user alone, a teammate, someone outside the
  project? This sets register and how much context the prose assumes.
- **What decision does it inform?** A report with a decision behind it
  has an argument; one without it has sections.
- **The slug**, derived from the subject rather than the project, so
  several reports coexist.

Ask only what genuinely changes the report, batched into one
`AskUserQuestion` with recommendations. A run that interrogates the user
about a report they just asked for has misread the request.

## Phase 1 — Harvest the evidence trail

Full protocol, including what counts as a locator and how to handle
memory: `references/evidence-harvest.md`.

Walk back through the session and record what it actually did. Every
claim the report will make gets a row in `claims.json`:

```json
{
  "id": "c7",
  "text": "The ingest worker retries three times before dropping.",
  "kind": "direct",
  "confidence": "high",
  "sources": ["s3"],
  "support": "lib/ingest/worker.ts:88-104, `maxRetries = 3` guarding the catch",
  "limits": "Read from source; no runtime measurement."
}
```

`kind` is `direct` or `inference`, and the distinction is the whole
point. A direct claim points at something the session saw. An inference
is assembled from claims that did, names them, and renders on the page
visibly marked as reasoning rather than finding.

**What counts as a source**: a file with a line range, a command with its
output, a research report in the repo, a URL that was actually fetched, a
test run, a screenshot. **What does not**: recollection, a plausible
figure, a statistic you know but did not check here. Those are either
labelled inference with their basis named, or cut.

The build fails on three things, and each has burned a real page: a
quantitative or attributed claim with no source; a source that supports
something adjacent rather than the claim itself; an inference rendered as
a finding. The middle one is the sneakiest, because the citation resolves
and only reading the source catches it.

Where the session was uncertain, the report says so. A report that
resolves everything reads as generated, because a human with real sources
almost always has something they are unsure about.

## Phase 2 — Resolve the design system

If the project has a `DESIGN.md`, use it — the report should look like it
belongs to the product it is about. Copy it into the report directory so
the report stays readable after the project moves on.

If it does not, generate one from the **subject**, and save it beside the
report. `references/design-system.md` carries the shape.

The generated system is derived from the topic, not chosen from taste.
Every major visual decision should map to a named concept in the
material: the register the document pretends to be (a field notebook, a
control panel, an incident log, a specimen sheet), the one visual device
the page is built around, palette logic with something in the subject
justifying it, a type pairing that belongs to this material, and a motion
signature with a perceptual job.

**Look at real editorial and data-heavy pages before settling the
skeleton.** Where the Mobbin MCP is installed, `search_sections`
(`platform: web`) returns shipped versions of the blocks a report is made
of — comparison tables, stat rows, evidence callouts, long-form reading
surfaces. Two searches, images opened, and a line in the report's
direction comment naming what you took. The trawl feeds structure and
density, never identity; the palette still comes from the subject.

**Between reports, vary the skeleton, not the palette.** Layout
similarity across the web fell 44% in a decade and the strongest
correlate was shared libraries, not shared colour — so re-theming a
previous report changes nothing that reads as sameness. Read any sibling
reports in `docs/reports/` and treat their section silhouettes, hero
shapes and chart grammars as taken.

## Phase 3 — Compose the argument as page-safe blocks

`references/report-craft.md` carries the buildable rules and the evidence
behind each.

The structural constraint that shapes everything: **the same source has
to read as a continuous page on screen and paginate cleanly to A4.** So
the report is a sequence of blocks, each one an argument step that can
survive a page break at its boundary and never inside a figure, a table
row group, or a caption away from its chart.

- **Lead with the conclusion, and with the ask.** Median scroll depth is
  around half the page, roughly 38% of arrivals leave immediately, and
  only a quarter pass the 1,600th pixel of a 2,000-pixel article. A
  report that withholds its finding until block nine is written for
  readers who never arrive. The TLDR is the top of the full report, not
  only a separate file.

  **The finding is not the whole job.** A blind panel of six judges split
  cleanly: the editorial and design lenses preferred this skill's output
  four times out of four, and both judges reading as *the person receiving
  the document* preferred a rival that named the next action up front.
  Same reason both times — better provenance, no ask. So the opening box
  carries one line saying what should happen and who decides, and the
  detail earns its place underneath. A reader who agrees with you and
  does not know what to do has been handed a diagnosis, not a report.

  A second round after that fix flipped one of the two and narrowed the
  other, and sharpened what the ask has to be:

  - **It carries the cheapest high-payoff action, not a secondary one.**
    One report's top-box ask requested a benchmark sweep while "export
    the loss counters" — the cheap change that makes the problem visible
    at all — sat at item 2 of section 09. A reader who stops at the fold
    never learns production is blind.
  - **It is the last content block, unless the page is one sheet.** On a
    scrolling report, sources and the methods note are apparatus and
    follow it. On a one-pager the constraint inverts: a third round put
    the ask last, the sheet spilled to two, and the ask opened page two.
    The judge's words: "whoever reads only the sheet I was handed first
    never sees the ask." One page beats correct ordering. If it spills,
    the ask moves up.
  - **It is sized and owned.** "Under an hour, needs an owner and your
    yes" is what a decision-maker praised over four unpriced imperatives.
    Give the cheapest item a cost and a named decision.
- **One claim per block**, with one visual delta that supports it.
  Adjacent blocks reuse scales, objects and positions unless changing one
  of those *is* the evidence.
- **Motion is semantic or it is cut.** Admissible only if you can finish
  "this motion lets the reader perceive ___ that would otherwise require
  a difficult mental comparison." If the blank is energy, delight or
  polish, it is decoration — and decoration is what gets stripped at
  print anyway, so it earns its place twice or not at all.
- **Every block renders from its own state.** Readers skip faster than
  animations complete, and the printer does not run them at all. No claim
  may exist only inside an animated intermediate frame.
- **Reduced-motion is the baseline.** Static first; motion added under
  `prefers-reduced-motion: no-preference` so an unsupporting browser
  fails safe.
- **Native scrolling is untouched.** No wheel, momentum, direction or
  history override; `normalizeScroll()` is prohibited.

## Phase 4 — Build the page

Route the layout to `design-craft` and the flow and states to
`ux-craft`. Route **every word of prose** to `create-luke-content` —
headline, standfirst, block copy, chart captions, the closing note.
Charts go through `dataviz` for form and colour.

Where one of those isn't installed, use this skill's own
`references/report-craft.md` and `references/design-system.md` in its
place and say which substitution you made in the methods note. A run
that silently writes its own prose and a run that had no voice skill
available look identical otherwise, and only one of them is fine.

**Citations are claim-local**, in three layers, all three required
because any design where a source exists only inside a hover state has,
by that rule, no sources:

```html
<a class="cite" href="#r12" data-cite="r12" data-n="9" aria-describedby="r12">9</a>
```

The marker is an anchor, never a button — a `<button>` is inert with
JavaScript off, which breaks the claim-to-source bond in exactly the case
the page is supposed to survive. The anchor jumps to the registry
unaided; the hover, focus and tap preview is enhancement layered on top.
The registry at the foot is real DOM with full metadata and backlinks.

**Imagery** through `media-gen-pro`, only where a picture genuinely
carries something prose does not, and never for charts, numbers, labelled
diagrams, tables or anything with exact text — image models garble those
and re-prompting garbles them differently. Say what a run will spend
before spending it.

Two things measured by putting a real generated image through the whole
path. **Resize it to the width it displays at** before wiring it in: a
614KB hero arrived at 1408px and nearly doubled the PDF on its own, and a
report with three of them is several megabytes of attachment. And **the
finding still comes first** — a full-width hero at the top pushes the
conclusion below the fold on screen and onto page two in print, which
costs more than the picture is worth. Put imagery after the finding, or
beside it.

**Self-contained**: one file, aiming at zero network requests. Inline the
CSS, the data and the static fallbacks. A webfont is a live CDN
dependency on a document meant to outlast the CDN; prefer a system stack
or subset and inline the one face carrying the report's identity.

Calibrate length to the argument. A report covers its substance and stops
— padding it with restated summaries, a boilerplate methodology preamble
and a section per heading you thought of is how a three-block finding
becomes twelve blocks nobody finishes.

## Phase 5 — Derive the TLDR

`assets/tldr-template.html` is the starting structure. Same ledger, same
design system, same citation contract, one page:

brand band · the finding in one sentence · one hero visual · three to six
cited claims · sources footer.

It is a **derivation, not a summary written separately** — every line
traces to a ledger row that also appears in the full report. Two
documents that disagree about the finding is the failure mode here, and
generating both from one ledger is what prevents it.

Aim for one A4. Spilling to a second page is acceptable when the source
list is long; spilling because the prose is loose is not.

## Phase 6 — Export, audit, fix

```bash
node scripts/export_pdf.mjs docs/reports/<slug>/index.html --out docs/reports/<slug>/report.pdf
node scripts/export_pdf.mjs docs/reports/<slug>/tldr.html  --out docs/reports/<slug>/tldr.pdf
python3 scripts/audit_report.py docs/reports/<slug>/
```

The exporter checks the PDF it produced rather than assuming it: page
count against block count, real A4 geometry, surviving link annotations,
and no transient animation text frozen into the ink. The auditor checks
citation integrity both ways, ledger-to-page agreement, self-containment,
reduced-motion, print rules, and accessibility basics. Errors block;
warnings are for the reader.

Then `design-review` against the real render, and open the PDF and look
at it. Rendering a page and reading a tool's exit code is not the same as
seeing it — the defects that survive automated gates are the ones a human
catches instantly, a void where a panel got pushed down, a chart clipped
at a page boundary, a caption orphaned from its figure.

## Scope and delegation

Deliver the report that was asked for, at the scope intended. Make the
routine calls yourself and check in only where two readings would produce
materially different documents.

Delegate only where the work is genuinely independent and sizeable — a
wide sweep across many files to reconstruct what a long session did is
worth one subagent; drafting a block is not. Keep the count low; a
report is one argument and splitting it across agents costs coherence
before it saves time.

## Operating rules

- **The ledger is the source of truth.** Prose that outruns it is
  rewritten, not re-cited.
- **"The session did not establish this" is publishable.** Reaching for
  a weaker source, or a remembered figure, is not.
- **Characterise uncertainty no more strongly than the evidence does.**
  Overclaiming about the corpus is the same defect as overclaiming from
  it.
- **Engagement is not comprehension.** This format buys attention and
  perceived clarity; the measured evidence does not show it buys
  understanding. Never claim otherwise in the report's own copy.
- **The methods note is not a disclaimer, and not a changelog.** State
  what the session did, what was read, what was verified, what a human
  reviewed, and what the report could not establish. Disclosing machine
  involvement has no reliable credibility cost; vagueness about it does.
  What *does* cost is narrating the pipeline instead of the evidence. A
  judge reading as the recipient singled out a closing note saying the
  prose had passed a voice lint and no imagery had been generated: "the
  genuinely useful half of that paragraph deserves to be a line near the
  top; the rest belongs in a commit message." Which skills ran is not
  news to the reader. What the report cannot tell them is.

  **The narration comes back in disguise, so watch for the second form.**
  With the tooling names gone, the next round's judge found the same
  defect wearing evidence-gathering clothes: a sources header announcing
  "five files read in full, every figure recomputed from the raw counts",
  a footnote printing the `grep` command that was run, and a read-date
  stamped on every source. That is the document describing how it looked
  rather than what it found. The provenance belongs in `claims.json`,
  where it is inspectable; the page cites the source and stops.

- **Never let the working path into a source label.** The same judge hit
  `./fixture` in a sources line and reacted with "you analysed a fixture,
  not our repo?" — which undercut the strongest claim on the page. Cite
  the path as the reader's repo sees it, or cite the file alone.
- **Never publish or deploy.** Writing the files ends the run.
- **Subagents never run git operations.**
