---
name: report
description: >-
  Turn what a Claude session already worked out into a designed, cited report — one self-contained HTML page that reads as a rich scrolling document on screen and paginates to a clean A4 PDF, plus a stripped-back one-page TLDR. Ships three readings of the same argument over one claim ledger — Primer, Brief and Technical — that the reader toggles between, each one fully cited from the same shared registry, and every report opens with a named TLDR section carrying the finding, its supporting claims, the one thing that would change it and the ask. Compiles the session's own evidence trail (files read, commands run, research already in the repo, URLs fetched, renders captured) into a claim ledger first, so every number and attribution carries a locator and anything reasoned is labelled as inference. Comparison and evaluation work additionally ships a verdict layer: three ranked picks in each of the categories readers actually differ on, plus one overall winner with its cost, its weaknesses and a named decision — and independent lab verdicts from Which?, RTINGS, Choice or Consumer Reports count as high-value evidence even where the raw measurements sit behind a paywall. Leads with the conclusion, cites claim-locally with source popups, ships light and dark with the PDF always light, animates throughout with GSAP including the micro-interaction feedback on every control, builds figures through dataviz in native CSS/DOM, hand-authored SVG, or TanStack Charts compiled to static SVG at build time, uses imagery from the evidence trail with full provenance, and routes every visual and flow decision through design-craft and ux-craft with a Mobbin trawl behind the layout. Use this whenever someone wants what just happened written up — "write this up as a report", "give me a summary with a TLDR at the top", "/report", "/report tldr", "turn this session into something I can send", "make me a page about what we found", "I need a one-pager on this for the team", "document this investigation properly", "which of these should we use" — and also when they ask for charts, visualisations or a PDF of work the session already did. Prefer this over a plain markdown summary whenever the write-up needs to look designed, needs citations, or needs to leave the terminal. Not for research that has not happened yet (use dossier-report), Diolog-branded A4 guides (use create-diolog-guides), or slide decks (use deck-craft).
---

# Writing the session up

One session in, one report out: argued from what the session actually
established, designed around its own subject, written to disk as a page
you can read and a PDF you can send, and offered in three registers so
the same evidence reaches a specialist, a decision-maker and someone
meeting the subject for the first time.


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
| 2 | Write the three readings of every claim | `create-luke-content` |
| 3 | Resolve the design system, light and dark | project `DESIGN.md`, or Mobbin MCP + `/trawl` + `design-craft` |
| 4 | Compose the argument as page-safe blocks | `ux-craft` |
| 5 | Build the page | `design-craft`, `ux-craft`, `dataviz`, `media-gen-pro`, `create-luke-content` |
| 6 | Derive the TLDR one-pager | — |
| 7 | Export, audit, fix | `scripts/`, `design-review` |

Output lands in `<project>/docs/reports/<slug>/`. The run ends when the
files are written. Publishing and deploying are somebody's deliberate
next act, not this skill's.

**`/report tldr` asks for the one-pager, so the one-pager is the
deliverable.** Phases 0 to 3 still run in full, because the ledger, the
three readings and the design system are what the one-pager is built from.
Phases 4 and 5 shrink to whatever the single page needs. Build the long
report as well only if the argument turned out to need more room than one
sheet gives it, and say so rather than shipping it silently.

**Design work goes through `design-craft` with `ux-craft`'s lens**, not
straight into markup — layout, the reading control, theme, motion and
every visual decision. `design-craft` owns the visual craft and the
anti-slop discipline; `ux-craft` owns flow, states, and the copy that
labels a control. Neither is a gesture at a skill name: load `design-craft`
and read its `references/mobbin-trawl.md` before settling the skeleton, its
`references/gsap-motion.md` before writing a timeline, its
`references/data-viz.md` before the first figure, and
`references/visitor-modes.md` for the Read-surface rules that govern a
document whose reader is here to understand something. From `ux-craft`, the
non-negotiables and its state grid bind the controls. Where either is not
installed, say which substitution you made in the methods note.

**Five things carry hard requirements on every run**, each with a gate
behind it rather than a request: `design-craft` and `ux-craft` on every
visual and flow decision, `dataviz` on every figure, the Mobbin trawl
behind the skeleton, GSAP as the motion layer on screen, and the TLDR
section at the top. A run that skipped one says so in the methods note; a
run that skipped one silently is the failure this list prevents.

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

**An independent lab's published verdict counts, even without the raw
numbers.** Which?, RTINGS, Consumer Reports, Choice and Stiftung
Warentest — and their software equivalents, a benchmark with a published
methodology and a private dataset — run the tests nobody else runs, and a
paywall over the measurements does not make the verdict weak evidence.
Cite the ranking as the ranking it is, name the protocol from the free
portion, record in `limits` that the underlying numbers are not public,
and stamp the test year. Declining it leaves the report arguing from
affiliate roundups and vendor claims, which is worse evidence, not more
rigorous. `references/product-verdicts.md` carries the rule.

### The verdict layer, when the report recommends something

Where the session was choosing between things — libraries, vendors,
models, services, hardware, architectures — the ledger gains a verdict
layer, and `references/product-verdicts.md` is the contract: **3–6
categories** derived from how readers actually differ, **three ranked
picks** in each with what they cost and what the runner-up does better,
and **one overall winner** with what it loses on and what would change it.

Two integrations matter. **A ranking is an inference**, so every pick is
`kind: "inference"` with a non-empty `from` — a pick rendered as a finding
is the strongest claim in the document wearing no evidence, and the
auditor fails it. And **the winner is the report's ask**, so it carries a
size and a named decision rather than sitting beside a second summary at
the top of the page.

The build fails on three things, and each has burned a real page: a
quantitative or attributed claim with no source; a source that supports
something adjacent rather than the claim itself; an inference rendered as
a finding. The middle one is the sneakiest, because the citation resolves
and only reading the source catches it.

Where the session was uncertain, the report says so. A report that
resolves everything reads as generated, because a human with real sources
almost always has something they are unsure about.

## Phase 2 — Write the three readings

Full contract, markup and gates: `references/readings.md`.

The report ships three registers of one argument over one ledger, and the
reader chooses which they get:

| Reading | Written for | What it does |
|---|---|---|
| **Primer** | someone meeting the subject cold, around an 11-year-old reading level | the finding as something concrete, an analogy doing the work a definition would |
| **Brief** | the informed non-specialist who has to decide | what was found, what it means, what should happen |
| **Technical** | someone who will check the work | mechanism, numbers, method, limits, the shape of the uncertainty |

`brief` is the default — the register a bare link lands on and the one the
PDF exports unless another is asked for.

**The rule that makes three readings honest, and the reason this is a
phase rather than a formatting step:**

> A reading may change the words. It may never change what is claimed.

Simplifying is choosing shorter words for the same proposition. Dropping
the caveat that bounds a number is a *different and stronger* claim, and
it is the one a Primer produces by default, because the simplified
sentence genuinely reads better. Confidence, limits and the inference
mark survive into all three; a re-expressed number stays the same number.

So every claim in `claims.json` gains a `readings` object holding all
three wordings, written from the ledger row rather than by rewriting
another register. Three passes from the ledger produce three registers of
one argument; one pass plus two rewrites produces one register and two
translations of it, and it reads that way.

A claim may be omitted from a register when it genuinely has no useful
form there — declared with `omit` and an `omitReason`. The finding and the
ask may never be omitted from any reading: a register without the
conclusion is a different document, not a simpler one.

Route every word through `create-luke-content`, once per reading. The
voice does not change across registers — Luke writing for an
eleven-year-old is still Luke, not a children's-textbook persona.

## Phase 3 — Resolve the design system, light and dark

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
skeleton.** Where the Mobbin MCP is installed, `search_sections` returns
shipped versions of the blocks a report is made of. It takes only a query
— sections are web by definition, so there is no `platform` parameter to
pass; `search_screens` and `search_flows` do take one. Run two or three
aimed searches, describing what is on the screen rather than how it should
feel:

- `"long-form article with sidenotes and inline citations"`
- `"comparison table with recommended option highlighted"`
- `"statistics section with large figures and short labels"`

**Open the images.** A result you did not look at is a result you did not
use. For each one worth keeping, ask what it is doing that a generated
page would not have thought to do — where the eye lands and what earned
that, how dense the first screen is (generated layouts are reliably
sparser than shipped ones, and sparse reads as unfinished rather than
calm), what carries the identity when the logo is off screen, and what is
deliberately plain.

**Write the ledger into the report's `DESIGN.md`**, because an
instruction-only step has a measured history of being skipped and a ledger
is the difference between a trawl and a claim about one:

```
MOBBIN TRAWL
  q1  "long-form article with inline citations and a source list"  → 14 results, opened 4
  q2  "comparison table with recommended option highlighted"       → opened 3
  TOOK  the recommended column is a raised card, not a badge (q2)
  TOOK  density: 9 elements above the fold, not 4
  LEFT  the tinted full-bleed section bands — identity, not a mechanism
```

`LEFT` matters as much as `TOOK`: it records that you looked at something
distinctive and declined to lift it. **Structure, density, sequence and
state coverage transfer; identity never does** — the palette still comes
from the subject. Where the MCP is not installed, say so in one line and
substitute deliberately rather than implying a reference pass happened.

**Then diverge with `/trawl` where the skeleton is genuinely open**, giving
it the subject matter as frame material. Reference tells you what shipped
pages do; divergence is what stops this report looking like the last one.
Skip it for a report whose project `DESIGN.md` already binds the layout —
there is nothing open to diverge on.

**Between reports, vary the skeleton, not the palette.** Layout
similarity across the web fell 44% in a decade and the strongest
correlate was shared libraries, not shared colour — so re-theming a
previous report changes nothing that reads as sameness. Read any sibling
reports in `docs/reports/` and treat their section silhouettes, hero
shapes and chart grammars as taken.

**Both themes ship, and the PDF is always the light one.** Three rules,
each of which has a failure mode that only shows up in the artifact
nobody previews:

- **Light is defined unconditionally; dark only ever overrides.** A token
  whose only definition sits inside a dark block is undefined when the
  print rules land, and that renders as ink on ink. The auditor fails on
  it because reading the CSS will not.
- **Dark is written twice** — once under `prefers-color-scheme: dark`
  guarded so an explicit light choice wins, and once under
  `[data-theme="dark"]` so the control wins in both directions.
- **Print re-declares the light tokens**, not just `body`'s colours. A
  reader in dark mode otherwise prints dark values onto white.

The theme control is script-created on purpose: with JavaScript off the
page already follows the OS preference, so a dead button would be worse
than no button. The *reading* control is the opposite — it is content,
and works unaided. Three theme states, not two, so "auto" stays reachable
after a manual choice.

**Dark is measured, not assumed.** Contrast, focus visibility and divider
gutters are checked in both themes at Phase 7. A dark palette derived by
inverting a light one passes by luck if it passes at all, and the theme
nobody measured is the one that ships broken.

## Phase 4 — Compose the argument as page-safe blocks

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

  **It is a named section, and every report has one.** Leading with the
  conclusion is a principle and principles get interpreted;
  `<section id="tldr">` as the first content block is the enforceable form.
  It holds the finding in one sentence, three to five cited claims, the one
  thing that would change it, the ask, and — where the report recommends
  something — the verdict with its cost and its as-at date. It is a
  derivation from the ledger rather than a summary written separately, every
  claim in it carries its marker in every register, and its arithmetic is
  recomputed before shipping. `references/report-craft.md` §3 carries the
  contract.

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
- **The report is a Read surface, so comprehension outranks expression.**
  Prose at 45–75 characters, body at 17–19px with 1.5–1.6 leading,
  hierarchy from size and space rather than stacked styles, and the active
  register and the reader's position legible at all times. A reader opening
  the file a month later, or landing on a heading from a search, has to be
  able to tell where they are. Resist the three habits that arrive from
  product UI: a KPI strip where a sentence and one number would do, cards
  around prose that was already readable, and an orchestrated entrance on a
  document someone may open to check one fact.
  `references/report-craft.md` §7 carries the typography, and
  `design-craft`'s `references/visitor-modes.md` the mode it belongs to.

## Phase 5 — Build the page

Route the layout to `design-craft` and the flow and states to
`ux-craft`. Route **every word of prose** to `create-luke-content` —
headline, standfirst, block copy, chart captions, the closing note, once
per reading. **Route every figure's form and colour through `dataviz`** —
it owns the form heuristic and the palette formula, and a report that
argues from numbers and picks its own chart colours has spent the
credibility its evidence bought. `references/visualisation.md` carries the
three build lanes — native CSS/DOM, TanStack Charts compiled to static SVG
at build time, and hand-authored SVG — plus which form each register gets.

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
The registry at the foot is real DOM with full metadata and backlinks,
and it is **shared across all three readings** — the marker moves with the
wording, the source does not.

**A vertical rule is drawn in a gap, never beside words.** Keep at least
24px between a rule and the nearest text at 900px and wider, 16px below
that, applied on **both** sides of the rule. This is measured from the
text's ink to the line rather than from the element box, because the
padding is usually declared on a different element from the border and
the two numbers disagree — a cell with `padding-left: 24px` and a rule on
its own left border passes an element-box check by construction while
reading as a squeezed table. `design-review` measures the ink; the
auditor here catches the cheap form. A run of this skill against an
already-published page returned twenty violations.

**Motion is standard on screen and absent from the ink, and GSAP is a hard
requirement.** Every report loads it, and it animates throughout on screen
— the entrance choreography, the reveal sequence as blocks arrive, the
micro-interaction feedback on the reading toggle, theme control, citation
markers and disclosures, and any scrubbed or pinned episode the argument
has. `references/report-craft.md` §4 carries the two budgets and why they
do not conflict: **evidence motion** is strict and must justify itself
against a perceptual test, while **interface feedback** is mandatory
because a control that acknowledges a press with nothing reads as broken
however good the argument is. Tier-0 hover and focus transitions stay in
CSS even with GSAP loaded.

What makes that safe on a document that prints is the **authored static
frame**: every moving block ships the composition that carries its claim
without the motion, and that one artifact serves print, reduced motion, and
any browser that does not run the animation. Three readings means a static
frame per register wherever the figure differs. So motion costs the printed
document nothing, and the only question left is whether it earns its place
on screen.

`references/report-craft.md` also carries the GSAP hazards and the six-test
gate before any three.js reaches a report.

### Imagery — from the evidence trail first, generated second

`references/source-imagery.md` is the contract. Two requirements sit above
the detail.

**Where the evidence trail holds images the argument needs, the report uses
them.** A render or screenshot the session itself produced is the strongest
option here — it is the same class of evidence as a command's output, it
can be remade, and the ledger already has a row shape for it. After that:
the vendor's own press asset, a source's openly-licensed figure, a
generated illustration, an honest placeholder. An image found by search
with no traceable origin is not admissible in a document that gets
forwarded.

**An image is a claim, so it carries provenance**: a caption naming what it
is, a citation marker into the shared registry, a registry row recording
the origin, the licence basis and the date, and alt text describing what
matters about it rather than what it is of. Assets live in `assets/`
referenced relatively, and the figure and its caption are one `<figure>`
with `break-inside: avoid` — otherwise the printer separates them and the
caption opens the next sheet describing something the reader can no longer
see.

Never reproduce a paywalled publisher's own figures, and never let the
working path into a caption: `./fixture/dashboard.png` tells the reader you
analysed a fixture.

**Generated stills and clips through `media-gen-pro`**, only where a
picture genuinely carries something prose does not, and never for charts,
numbers, labelled diagrams, tables or anything with exact text — image
models garble those and re-prompting garbles them differently:

- **Every generated asset is captioned as generated**, in words a skimming
  reader cannot miss, and the methods note records it. An illustration a
  reader could mistake for a photograph of the thing under discussion is a
  provenance failure, not a decoration choice — the same rule the ledger
  applies to numbers.
- **Diagrams and vector artwork use the `svg: true` path**, which returns
  editable vector rather than a raster imitation of one, keeps its text as
  text, and survives print at any size.
- **Hold one visual language across the set** — pass the first accepted
  illustration back as `referenceImages` on later calls and put the design
  system's palette in `context`. Four illustrations prompted from scratch
  have four styles and read as four sources.
- **A generated clip is the narrow case and it is screen-only.**
  `generate_video` earns its place where the change over time *is* the
  evidence; generate the still first and pass it as `sourceImage` so the
  poster and the clip agree. Five seconds, one motion, `muted`,
  `playsinline`, `controls`, no autoplay, and the poster is the printed
  figure. No claim lives only in the clip — the PDF has to carry the same
  argument without it.
- **Say what a run will spend before spending it**, and report the actual
  after.

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

## Phase 6 — Derive the TLDR

`assets/tldr-template.html` is the starting structure. Same ledger, same
three readings, same design system, same citation contract, one page:

brand band · the finding in one sentence · one hero visual · three to six
cited claims · sources footer.

It is a **derivation, not a summary written separately** — every line
traces to a ledger row that also appears in the full report. Two
documents that disagree about the finding is the failure mode here, and
generating both from one ledger is what prevents it.

Aim for one A4 **per reading**. The registers differ in length, so check
the sheet count in each rather than in the default one: a Primer that
spills because its analogies run long is the same defect as a loose
Technical, and only rendering all three shows it. Spilling because the
source list is long is acceptable; spilling because the prose is loose is
not.

## Phase 7 — Export, audit, fix

```bash
node scripts/export_pdf.mjs docs/reports/<slug>/index.html --out docs/reports/<slug>/report.pdf
node scripts/export_pdf.mjs docs/reports/<slug>/index.html --reading technical \
     --out docs/reports/<slug>/report-technical.pdf
node scripts/export_pdf.mjs docs/reports/<slug>/tldr.html  --out docs/reports/<slug>/tldr.pdf
python3 scripts/audit_report.py docs/reports/<slug>/
```

The exporter checks the PDF it produced rather than assuming it: page
count against block count, real A4 geometry, surviving link annotations,
and no transient animation text frozen into the ink. `--reading` selects
the register; the default is Brief, and every PDF stamps which one it is,
because a document carrying one of three readings with nothing saying
which becomes ambiguous the moment it is forwarded.

The auditor checks citation integrity both ways, **each reading
independently**, the per-claim marker in every register that renders it,
ledger-to-page agreement, the reading parity of the ledger, divider
gutters, the theme contract, self-containment, reduced-motion, print
rules, and accessibility basics.

Five gates cover the hard requirements: **tldr** (the section exists, leads,
is cited, and renders in every register), **gsap** (the motion layer is
loaded and the micro-interaction states are declared), **verdict** (every
pick in a recommendation set is an inference with a non-empty `from`, and
the winner names what it loses on), **imagery** (every image has a caption,
a provenance line and a registry row, generated assets say so, and no video
autoplays), and **figures** (every meaningful figure carries a text
alternative stating its conclusion). Errors block; warnings are for the
reader.

Then `design-review` against the real render — **six captures, not one**:
three readings × light and dark. The register is set in the served source
rather than by clicking, because setting `.checked` from script does not
re-evaluate the `:has()` selector on Obscura, so a scripted toggle
measures the same register three times and reports three passes.

Then open the PDF and look at it. Rendering a page and reading a tool's
exit code is not the same as seeing it — the defects that survive
automated gates are the ones a human catches instantly, a void where a
panel got pushed down, a chart clipped at a page boundary, a caption
orphaned from its figure.

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
- **A paywalled lab verdict is a source, and a good one.** Cite the
  published ranking as the ranking it is, name the protocol, record in
  `limits` that the measurements are not public, stamp the test year, and
  never redraw their tables. The free alternatives are worse evidence, so
  declining a paywalled verdict makes the report weaker rather than more
  rigorous.
- **A comparison report recommends.** Where the session was choosing
  between things, the categories, the three ranked picks and the overall
  winner are the deliverable — and the winner is the report's ask, sized
  and owned. A ranking is an inference and renders as one.
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
