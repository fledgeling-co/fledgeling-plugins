---
name: dossier-report
description: >-
  Turn a research question into one published, uniquely-themed HTML report page — a Dossier paid+free deep-research panel read in full, compiled into a claim graph, then designed from scratch around its own subject and written out to ~/Dev/dossier/<slug>/index.html for <slug>.fledgeling.app. Ships three readings of the same argument over one claim graph — Primer, Brief and Technical — that the reader toggles between, each fully cited from the same shared registry, and every page opens with a TLDR band carrying the finding, its supporting claims and the one thing that would change it. Product and buying research additionally ships a verdict layer: three ranked picks in each of the categories buyers actually differ on, plus one overall winner with its cost, its weaknesses and the reasons written out — and independent lab verdicts from Which?, RTINGS, Choice or Consumer Reports count as high-value evidence even where the raw measurements sit behind a paywall. Every page gets its own visual language, light and dark, GSAP motion and micro-interactions throughout, conditional three.js, animated and interactive visualisations pitched at each reading — built through dataviz in native CSS/DOM, hand-authored SVG, or TanStack Charts compiled to static SVG at build time — imagery taken from the research sources themselves with full provenance, generated stills and clips where a picture carries what prose cannot, claim-local citations with source popups, a verified source registry, and the Dossier/Margin marketing chrome. Design direction comes from a trawl of real shipped UI via the Mobbin MCP plus divergent ideation, and every visual and flow decision routes through design-craft and ux-craft. Use whenever someone wants a topic researched and published as a page, an infographic, a field report, an evidence page, a buying guide or a write-up — "research X and make a page for it", "build me a page about Y", "turn this research into a report page", "publish a dossier page on Z", "make an infographic about W", "which X should I buy", "compare the best X", "what's the best X for Y" — and also when they hand over an existing research corpus and want it turned into a page. Prefer this over a plain design pass whenever the page's substance has to come from research and every claim needs a source behind it.
---

# Publishing a research page

One topic in, one page out: researched by a panel, argued from a claim
graph, designed around its own subject, published to its own subdomain,
and offered in three registers so the same evidence reaches a specialist,
a decision-maker and a reader meeting the subject for the first time.


The failure this exists to prevent is specific and has happened twice
already in this repo. A panel of five backends ran, `research_synthesise`
reported **"5 never opened"**, and the page was written from the merged
distillation. The distillation is a coverage difference between reports,
not a summary of them. A page built on it describes what the backends did
not share rather than what they found.

So the spine of this skill is: **spend on research, then actually read
it, then let the reading decide the page.** Everything else follows.

`references/evidence.md` carries the research this skill is built on —
225 sources across five backends — and every rule below traces to a row
in it. Read it when you need to justify or tune a rule, not on every run.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. Binds the four scopes this skill states as a class rather than a count — reports read end to end, figures, images, scroll states — to a scope ledger reported as fractions, restores the verification the house style strips (noting that opus-5-prompting.md's removal is written for the Opus children, not for the orchestrator), and makes audit_page.py's pasted output and twelve opened renders the receipt instead of a claim. Other models skip it.

## The shape of a run

Ten phases. Phases 1 and 5 both use `/trawl` for divergence; phases 0,
4 and 9 are the human checkpoints.

| # | Phase | Routes to |
|---|---|---|
| 0 | Sharpen the brief | `/clarify` |
| 1 | Diverge on research angles | `/trawl` |
| 2 | Run the panel, read all of it | Dossier MCP |
| 2.5 | Settle what the panel disputes | the artifact itself |
| 3 | Compile the claim graph, and the verdict where there is one | — |
| 4 | Name, aesthetic and icon concept | `/clarify` |
| 5 | Diverge on visual direction | Mobbin MCP, `/trawl` |
| 6 | Write the three readings | `create-luke-content` |
| 7 | Build the page | `design-craft`, `ux-craft`, `dataviz`, `media-gen-pro`, `create-luke-content` |
| 8 | Build the page icon | `create-mac-icon` |
| 9 | Audit, index, ask before deploy | `design-review` |

**Every design decision goes through `design-craft` with `ux-craft`'s
lens** — the aesthetic direction, the reading control, the theme, layout,
motion, states and the copy that labels a control. `design-craft` owns the
visual craft and the anti-slop discipline; `ux-craft` owns flow, states
and interface words. Neither is a gesture at a skill name: load
`design-craft` and read its `references/mobbin-trawl.md` before committing
a direction, its `references/gsap-motion.md` before writing a timeline,
its `references/data-viz.md` before the first figure, and
`references/visitor-modes.md` for the Read-surface rules that govern a page
whose visitor is here to understand something. From `ux-craft`, the
non-negotiables and its state grid bind the controls. Where either is
unavailable, say which substitution you made in the methods note.

**Six skills carry hard requirements on every run**, and each has a gate
behind it rather than a request: `design-craft` and `ux-craft` on every
visual and flow decision, `dataviz` on every figure, `/trawl` on both the
research angles and the aesthetic, the Mobbin MCP on the layout reference,
and GSAP as the motion layer. A run that skipped one says so in the
methods note; a run that skipped one silently is the failure this list
exists to prevent.


## Phase 0 — Sharpen the brief before spending

Run `/clarify` on the topic. A vague question buys a survey; a
decision-shaped question buys a page with an argument. This costs nothing
and it is the highest-leverage minute in the run, because the research
prompt is fixed once the panel starts and $5–20 rides on it.

Answer from context first — the conversation, the repo, any corpus the
user already handed over — then ask only what is genuinely open, with
recommendations, allowing notes on each answer:

- **What decision does this page inform, and for whom?** This becomes
  `decisionContext` in the Dossier plan and it is the single field that
  most changes what comes back.
- **What is in and out of scope**, and what time horizon.
- **What would change the reader's mind?** The answer names the
  subtopics worth enumerating.
- **Is there a contested question at the centre?** A page with an
  editorial tension reads as authored; a page without one reads as a
  summary.
- **Anything already known** that the research should not re-derive.

## Phase 1 — Diverge on research angles

Run `/trawl` on the sharpened question before writing the Dossier brief.
The first three angles any model produces on a topic are the same three
every time; the enumerated subtopics in a research brief are exactly
where that sameness becomes expensive, because the panel then spends real
money surveying the obvious.

Take the surviving frames and turn them into the numbered subtopics of
the brief. A brief carrying six angles from a portfolio of frames buys a
different corpus from one carrying six angles a model listed unaided.

## Phase 2 — Run the panel, and read every word of it

Protocol, budget rules and the read-in-full gate: `references/research.md`.

The sequence is fixed: `research_budget` → `research_plan` (free — relay
the worst-case band to the user before committing) → `research_start`
with the plan's `contractFingerprint` and **no `provider`**, which is
what assembles the paid+free panel → monitor on a timer without blocking
→ read.

**The gate.** When the panel settles, `research_export` every member,
then read each report end to end with Read. Not the outline, not the
merged distillation. Then `research_verify_citations` on the load-bearing
ones. Where members disagree, the disagreement is the finding — carry it
into the page as stated uncertainty rather than silently picking a side.

A member that finishes early is one backend's answer. Do not read it to
fill the wait and do not report from it: support is counted in
independent domains, not in how many backends agreed.

**When the question is which one to buy, the brief asks for the labs by
name.** Enumerate the independent testing organisations that cover the
category — Which?, RTINGS, Consumer Reports, Choice, Stiftung Warentest,
the relevant trade lab — and ask for their published verdicts and stated
protocols alongside the general findings. **A verdict whose raw
measurements sit behind a paywall is still high-value evidence**, and
often the best available: refusing it because the table is unreachable
leaves the page arguing from affiliate listicles and vendor claims, which
are systematically worse. `references/product-verdicts.md` carries how to
cite one honestly, what to record in `limits`, and why their
disagreements are findings rather than problems.

## Phase 2.5 — When they disagree about what *exists*, go and look

Sort the disagreements into two kinds, because they need opposite
handling:

- **They disagree about what it means.** Carry it onto the page as
  stated uncertainty. Neither you nor the corpus can settle it, and
  pretending otherwise is the overclaiming this skill exists to prevent.
- **They disagree about what exists.** Does this API ship? Is this
  endpoint live? What does this file actually say? That is not a matter
  of interpretation and it is not settled by counting backends. **Stop
  reading and check the artifact.**

The artifact is whatever the claim is ultimately about, and it is
usually already on the machine: an SDK header, a framework's own
availability macros, `--help`, a package's `.d.ts`, a real API response,
the binary, the config file, the repository. Web research locates the
question; a local read answers it.

This is not a nicety. Measured on one run, five backends returned
**three incompatible answers** about what a named OS release had added
to a framework: one said the surface had been frozen for two years and
reasoned it from the vendor's changelog, one announced a new API sourced
to a third-party vendor forum while naming the OS by a version that does
not exist, and one reported a policy documented as Beta. Two `#define`
lines in the shipping SDK settled it in seconds, agreed with none of them
completely, and became the finding the page was built on. The panel cost
$9.70 and 233 sources; the grep cost nothing. **The panel earned its
money by disagreeing** — without three answers there was no reason to
look, and no way to know what to look for.

Three rules keep this honest:

- **Record the environment.** OS and build number, SDK path, tool
  version, the date. A local read is only primary evidence if a reader
  can tell what was read and where. Put it in the claim graph and in the
  methods note.
- **Quote verbatim.** The value of a header over a summary of a header
  is that it is not a summary.
- **Absence is weaker than presence.** "Not in the shipping SDK" is a
  fact about today; it is not proof a symbol never existed, and beta
  seeds carry symbols that are later withdrawn. Say the narrow true
  thing: *it is not callable now*. A backend that reported a
  since-withdrawn API was wrong about the present and may have been
  right about the past — characterise it no more strongly than that.

Where the check is genuinely unavailable — no licence, no hardware, a
paid API you should not call — say so in the methods note and keep the
disagreement live on the page. An unsettled split, declared, is a better
page than a settled one that guessed.

## Phase 3 — Compile the claim graph

Before any design happens, turn the corpus into a claim ledger. This is
what stops a page's claims outrunning its sources, and it is the artifact
the citation UI is generated from rather than retrofitted onto.

Every claim carries: an id, its exact text, a confidence, whether it is
**direct or inference**, its source ids, the specific passage or table
that supports it, its scope and limits, and a `readings` object holding
how each of the three registers says it (Phase 6).

The build fails if a quantitative or attributed claim has no source, if a
cited source supports only a nearby proposition rather than the claim
itself, or if something assembled by reasoning is rendered as an
empirical finding. Inferences are labelled as inferences on the page.

### The verdict layer, when the page recommends something

A page about which thing to get owes an answer, and a survey of the
field is not one. Where the question is a choice — hardware, appliances,
software, models, services, plans — the graph gains a verdict layer and
`references/product-verdicts.md` is the contract:

- **3–6 categories**, each derived from how buyers actually differ rather
  than from a spec sheet's headings, each with a line saying who it is
  for. A category the corpus never examined does not ship; the gap is
  named instead.
- **Three ranked picks per category**, each carrying what it is best at,
  what it costs, the claims it rests on, what would change it, and the
  genuine thing the runner-up does better. Fewer than three is a
  legitimate answer.
- **One overall winner**, with the reasons written out as prose a reader
  can disagree with, what it loses on, and what would change it. "No
  overall winner" is publishable where the field genuinely splits.
- **Every pick is `kind: "inference"` with a non-empty `from`.** A ranking
  is assembled by reasoning across claims, so it is marked as reasoning —
  a pick rendered as a finding is the strongest claim on the page wearing
  no evidence, and the auditor fails it.

The winner is also the page's TLDR first line, so this phase decides what
the reader meets before anything is designed.

## Phase 4 — Name, aesthetic and icon concept

Run `/clarify` again, now that the research is read and you can describe
what the page is actually about.

- **The slug.** One word where possible; it becomes the directory
  `~/Dev/dossier/<slug>/` and the subdomain `<slug>.fledgeling.app`.
  Offer three with rationales.
- **The aesthetic direction.** Offer the shortlist from Phase 5 in
  words, not renders — register, palette logic, type, the one visual
  device the page is built around, and what each says about the subject.
- **The page icon concept.** Two or three subject-mined directions.

## Phase 5 — Diverge on visual direction

Two inputs, in this order: reference evidence from real shipped UI, then
divergence against it. Doing them the other way round produces a direction
that has to be retrofitted onto what real pages actually do.

**Trawl the Mobbin MCP first.** `search_sections` returns shipped web
sections and takes only a query — sections are web by definition, so
there is no `platform` parameter to pass; `search_screens` and
`search_flows` do take one. Run **two or three aimed searches** on the
block types this page is made of, and describe what is on the screen
rather than how it should feel:

- `"long-form article with sidenotes and inline citations"`
- `"comparison table with recommended option highlighted"`
- `"statistics section with large figures and short labels"`
- `"report page with sticky section navigation"`

**Open the images.** A result you did not look at is a result you did not
use, and the metadata names an app without saying why its section works.
For each one worth keeping, ask what it is doing that a generated page
would not have thought to do — where the eye lands and what earned that,
how dense the first viewport is (generated layouts are reliably sparser
than shipped ones, and sparse reads as unfinished rather than calm), what
carries the identity when the logo is off screen, and what is deliberately
plain.

**Write the ledger into the direction record**, because an
instruction-only step in this pipeline has a measured history of being
skipped and a ledger is the difference between a trawl and a claim about
one:

```
MOBBIN TRAWL
  q1  "long-form article with inline citations and a source list"  → 14 results, opened 4
  q2  "comparison table with recommended option highlighted"       → opened 3
  TOOK  the recommended column is a raised card, not a badge (q2)
  TOOK  density: 9 elements above the fold, not 4 — every result was denser than our draft
  TOOK  citation markers sit in the margin, not inline, above 1100px (q1)
  LEFT  the tinted full-bleed section bands — identity, not a mechanism
```

`LEFT` matters as much as `TOOK`: it records that you looked at something
distinctive and declined to lift it, which is the line between reference
and imitation. **Structure, density, sequence and state coverage transfer;
identity never does.** Where the MCP is not installed, say so in one line
in the methods note and substitute deliberately — never imply a reference
pass happened.

**Then run `/trawl` on the aesthetic**, and give it the subject matter as
the frame material. This is what makes each page different from the last,
and skipping it is how a producer of many pages converges on one look.

The evidence is blunt about why: measured across ~2M pairwise
comparisons, layout similarity fell 44% over a decade, and the strongest
correlate was **shared use of a small number of libraries**. The
invariant that reads as sameness is **layout skeleton and motion
signature, not palette**. Re-colouring a previous page fixes nothing.

Before designing, read `~/Dev/dossier/*/index.html` — the pages already
published — and treat their section silhouettes, hero shapes, chart
grammars and transition metaphors as **taken**.

## Phase 6 — Write the three readings

Full contract, markup, toggle and gates: `references/readings.md`.

The page ships three registers of one argument over one claim graph, and
the reader toggles between them:

| Reading | Written for | What it does |
|---|---|---|
| **Primer** | someone meeting the subject cold, around an 11-year-old reading level | the finding as something concrete, an analogy doing the work a definition would |
| **Brief** | the informed non-specialist the page is trying to persuade | what was found, what it means, what follows |
| **Technical** | someone who will check the work | mechanism, numbers, method, limits, where the backends disagreed |

`brief` is the default — the register a bare link lands on and the one
`og:description` quotes.

**The rule that makes three readings honest:**

> A reading may change the words. It may never change what is claimed.

Simplifying is choosing shorter words for the same proposition. Dropping
the caveat that bounds a number is a *different and stronger* claim, and
it is the one a Primer produces by default, because the simplified
sentence genuinely reads better.

On a published page that risk is sharper than on an internal report,
because the page goes out under a real name and its argument is usually
that somebody else overclaimed. **Where the panel disagreed, the
disagreement survives into every register** — the Primer says "the people
who looked at this do not agree yet" rather than picking the tidier side
because a split is hard to say simply. Resolving a split for a simpler
register is overclaiming committed against your own corpus, which is the
one form of it this skill has already shipped once.

Confidence, limits and the inference mark travel into all three. A
re-expressed number stays the same number: Primer may round and change
the unit, never drop it or lose an order of magnitude.

A claim may be omitted from a register with `omit` and an `omitReason`.
The **finding** and the page's **editorial tension** may never be omitted
— a register that resolves the tension the other two leave open is a
different page.

**The TLDR band is written three times, like everything else.** It is the
most-read block on the page, so it takes the same discipline: the finding
in one sentence, three to five cited claims, the one thing that would
change it, and — on a page that recommends something — the verdict with
its cost and its as-at date. Every line is a derivation from a claim that
also appears further down; a TLDR written separately from the graph is how
a page ends up disagreeing with itself about its own finding.
`references/page-craft.md` §1 carries the band's contract.

Route every word through `create-luke-content`, once per reading, from
the claim graph rather than by rewriting another register. The voice does
not change across registers: Luke writing for an eleven-year-old is still
Luke, not a children's-textbook persona.

## Phase 7 — Build the page

Full craft rules, with the evidence behind each: `references/page-craft.md`.

Route the design to `design-craft` with `ux-craft`'s lens on flow and
states. Route **every word of prose** to `create-luke-content` —
headline, standfirst, section copy, chart captions, the closing band.
The page is published under Luke's name and reads as his.

The rules that matter most, in short:

- **The page's skeleton comes from the evidence, never from the brief.**
  This is the single most reliable difference between a page that reads
  as authored and one that reads as generated, and it is invisible from
  inside: a research brief with six numbered subtopics produces six
  sections in that order, each titled with its subtopic, and every gate
  passes. What you have then is the *prompt's* outline with citations
  attached — the same outline any of the backends would have returned.
  Measured on two pages built from one corpus, two blind judges in
  opposite orderings both named this first. Before building, write the
  section list from the claim graph alone, then check it against the
  brief's enumeration: if the two match, the structure was inherited
  rather than found. Sections should be able to appear in an order the
  brief never suggested, and some of the brief's subtopics should be
  absent because the evidence did not support a section on them.
- **Headings are claims, not labels.** "Process topology and the
  extension contract" is a filing label; "The reach of the two calls is
  not the same" is something a reader can disagree with. A page whose
  headings are all noun phrases has a table of contents where its
  argument should be.
- **Lead with the conclusion.** Median scroll depth is ~50%, ~38% of
  arrivals leave immediately, and only a quarter pass the 1,600th pixel
  of a 2,000-pixel article. A structure that withholds the finding until
  state twelve is built for the readers who never arrive.
- **Every page opens with a TLDR band**, and it is the enforceable form of
  the rule above: a named `<section id="tldr">` holding the finding in one
  sentence, three to five cited claims, the one thing that would change it,
  and the verdict where the page recommends something. It is derived from
  the claim graph rather than written separately, every claim in it carries
  its marker in every register, and its arithmetic is recomputed before
  shipping. `references/page-craft.md` §1 owns the contract.
- **The page is a Read surface, so comprehension outranks expression.**
  Prose at 45–75 characters, body at 17–19px with 1.5–1.6 leading,
  hierarchy from size and space rather than stacked styles, and the active
  register and section position legible at all times. A reader landing
  mid-page from a shared link has to be able to tell where they are.
  `references/page-craft.md` §11 carries the reading surface,
  `design-craft`'s `references/visitor-modes.md` the mode it belongs to.
- **Martini glass by default** — authored stem, then open to sources,
  data and drill-down.
- **One claim per scroll state**, with one visual delta that supports it.
  Adjacent states reuse objects, scales and positions unless changing one
  of those *is* the evidence.
- **Motion is semantic or it is cut.** An animation is admissible only
  if you can finish "this motion lets the reader perceive ___ that would
  otherwise require a difficult mental comparison." If the blank is
  energy, delight or immersion, it is decoration.
- **Every state renders directly from its id.** Readers skip faster than
  animations complete, so no claim may exist only inside an animated
  intermediate frame.
- **Reduced-motion first.** Static baseline; motion added under
  `prefers-reduced-motion: no-preference` so an unsupporting browser
  fails safe. The reduced branch is a first-class narrative mode, not
  every duration set to zero afterwards.
- **Never touch native scrolling.** No scroll rate, direction, momentum
  or history override; GSAP's `normalizeScroll()` is prohibited.
- **Citations are claim-local**: inline marker on the smallest span the
  source supports, a preview on hover *and* focus *and* tap, and a
  persistent registry. Nothing may exist only inside a hover state.
- **Every page carries a methods note** — which backends ran, what they
  cost, what was read, what was verified, what a human reviewed, and
  what the page could not establish. Across 47 studies, disclosing AI
  involvement had **no reliable cost to credibility**; what the evidence
  asks for is specificity about what the automation did and who is
  accountable, not a vague "AI-assisted" badge.
- **Charts are validated at generation**: axes, baselines, units,
  intervals, legends, uncertainty. Truncation inflates perceived
  differences by 58–130%, and instructing readers does not fix it.
  **Route every figure's form and colour through `dataviz`** — it owns the
  form heuristic and the palette formula, and a page that argues from
  numbers and picks its own chart colours has spent the credibility its
  evidence bought. `references/visualisation.md` carries the three build
  lanes, which form each register gets, and what may move or be
  interactive in it.
- **A vertical rule is drawn in a gap, never beside words.** At least
  24px between a rule and the nearest text at 900px and wider, 16px
  below, on **both** sides. Measured from the text's ink to the line, not
  from the element box — the padding is usually declared on a different
  element from the border, so a cell with `padding-left: 24px` and its own
  `border-left` passes an element-box check by construction while reading
  as a squeezed table. `design-review` measures the ink; the auditor here
  catches the cheap form. Run against a page already published from this
  skill, the ink measurement returned **twenty below-floor violations**.
- **Light and dark both ship, and both are measured.** Light is defined
  unconditionally on bare `:root`; dark only overrides, written twice so
  the control wins in both directions. No token gets its only definition
  inside a dark block. Contrast, focus and divider gutters are checked in
  each theme, because a dark palette derived by inverting a light one
  passes by luck if it passes at all.

Generate the marketing chrome with `scripts/build_chrome.py` rather than
hand-writing it — the sticky masthead marketing Dossier and Margin
discreetly, and the overt closing band. Both are required on every page.
It is the one constant between pages, which is why it is a script.

**GSAP is a hard requirement. Every page loads it, and it animates
throughout** — the choreographed entrance, the reveal sequence as sections
arrive, the micro-interaction feedback on the reading toggle, theme
control, citation markers, filters and disclosures, at least one scrubbed
or pinned episode where the argument has one, and any tween between two
compiled figure states. `references/page-craft.md` §2 carries the two
budgets and why they do not conflict: **evidence motion** is strict and
must justify itself against a perceptual test, while **interface
feedback** is mandatory because a control that acknowledges a press with
nothing reads as broken however good the argument is. Tier-0 hover and
focus transitions stay in CSS even with GSAP loaded.

The escape hatch that used to sit here is closed. An eval run reasoned its
way from the tiering rules to a page with no GSAP at all — defensible on
the evidence, and not the house rule. Where an argument genuinely has no
scrubbed or pinned moment, record that in the methods note and spend the
layer on the entrance choreography and the feedback tier.

**three.js is gated** — six tests in `references/page-craft.md`, all of
which must pass, run against a claim id rather than against the topic.
When 3D is rejected, say so in the page's own notes and ship the
annotated static graphic.

### Imagery — from the sources first, generated second

`references/source-imagery.md` is the contract. Two requirements sit above
the detail:

**Where the subject has a visible form, the page shows it, and the images
come from the research sources.** A page about products, hardware,
interfaces, places or documents that renders as pure typography has thrown
away evidence the corpus already contains — and on a buying guide it has
withheld the one thing a reader deciding between physical objects needs.
Take the vendor's or publisher's own press asset first, a source's
openly-licensed figure second, a generated illustration third, an honest
placeholder last. An image found by search with no traceable origin is not
admissible on a page published under a real name.

**An image is a claim, so it carries provenance**: a caption naming what
it is, a citation marker into the shared registry, a registry row
recording the origin, the licence basis and the retrieval date, and alt
text describing what matters about it rather than what it is of. Download
into `assets/`, never hotlink, and resize to the width it displays at.

Never reproduce a paywalled publisher's own figures — a Which? or RTINGS
chart is the paid product. Cite the verdict and describe the method.

**Generated stills and clips through `media-gen-pro`**, where a picture
genuinely carries something prose does not, and never for charts, numbers,
labelled diagrams, tables or anything with exact text, which image models
garble and re-prompting garbles differently:

- **Every generated asset is captioned as generated**, in words a skimming
  reader cannot miss, and the methods note records it. An illustration a
  reader could mistake for a photograph of the thing under discussion is a
  provenance failure, not a decoration choice.
- **Diagrams and vector artwork use the `svg: true` path**, which returns
  editable vector rather than a raster imitation of one, scales without
  resampling, and keeps its text as text.
- **Hold one visual language across the set** — pass the first accepted
  illustration back as `referenceImages` on later calls and put the page's
  palette in `context`. Four illustrations prompted from scratch have four
  styles and read as four sources.
- **A generated clip is the narrow case**: `generate_video` earns its place
  only where the change over time *is* the evidence. Generate the still
  first and pass it as `sourceImage` so the poster frame and the clip agree;
  five seconds, one motion; `muted`, `playsinline`, `controls`, a poster
  that is the real static figure, no autoplay under reduced motion, and no
  claim that lives only in the clip.
- **Keep imagery out of the hero and say what a run will spend before
  spending it.** A full-width image at the top pushes the finding below
  the fold, which costs more than the picture is worth.

## Phase 8 — The page icon

Route to `create-mac-icon` with the chosen concept and the page's own
palette. It returns the layered master, the rasters and `audit.html`
with every take scored. Wire the result in as the favicon, the
`apple-touch-icon`, and the basis of the `og:image` — two of the three
existing pages ship with no `og:image` at all and share as bare links.

## Phase 9 — Audit, index, and stop

1. `python3 scripts/audit_page.py <page>/index.html` — cite↔source
   integrity both ways **and once per reading**, the per-claim marker in
   every register that renders it, the default register with script off,
   divider gutters, the theme contract, self-containment, reduced-motion,
   WebGL fallback, both chrome blocks, share tags, alt text, weight.
   Four of its gates are about the argument rather than the markup, and
   each exists because a page passed everything else without it:
   **uncertainty** (a page that never states a limit or a disagreement
   reads as generated — one construction in 3,700 words is effectively
   none), **claim graph** (a `claims.json` no block references means the
   per-claim check has nothing to test and passes vacuously),
   **inference marking** (a claim the ledger calls an inference must be
   labelled as one in the page), and **self-description** (a colophon
   advertising more sources than the registry holds; a reader who checks
   the easiest number once stops believing the rest).

   Five gates cover the hard requirements: **tldr** (the band exists, is
   cited, and renders in every register), **gsap** (the motion layer is
   loaded and the micro-interaction states are declared), **verdict** (every
   pick in a recommendation set is an inference with a non-empty `from`, and
   the winner names what it loses on), **imagery** (every image has a
   caption, a provenance line and a registry row, and generated assets say
   so), and **figures** (every chart carries a text alternative stating the
   conclusion). Errors block; warnings are for the reviewer.
2. `design-review` against the real render at multiple viewports —
   **six passes, not one**: three readings × light and dark.
   **Open the renders yourself first** — serve the page, capture each at 1440 and
   390, and read the captures asking *"what is wrong with this?"*. The auditor
   proves structure; only looking proves the page is any good, and a script
   reporting success on a page nobody opened is the failure this step exists
   for. Set the register in the **served source** rather than by clicking: on
   Obscura, setting `.checked` from script does not re-evaluate the `:has()`
   selector, so a scripted toggle captures the same register three times and
   reports three passes.
3. Fix what both find, then re-run the auditor.
4. Add the row to `~/Dev/dossier/home/index.html`, matching the existing
   markup.
5. **Stop and ask before deploying.** Publishing is outward-facing and
   hard to reverse. Vercel needs git author `luke@rhodes.gg`, and the
   CLI reports the BLOCKED state as UNKNOWN, so check the dashboard when
   a deploy stalls.

## What is reused, and what is never reused

The system boundary the research converged on from three directions:
**standardise the hidden infrastructure, derive the visible rhetoric
from the subject.**

Reuse freely: the chrome script, the citation component's behaviour, the
auditor, focus styles, the accessibility harness, the claim-graph shape.

Never reuse: hero composition, section silhouette, chart grammar,
illustration system, transition metaphor, typography, palette.

A page fails the authored review if its silhouette matches the previous
report once colour and copy are stripped, if changing the subject noun
leaves the visual metaphor intact, if motion is repeated fade-slide-reveal
recipes, if the hero is more specific than the evidence beneath it, if the
subject has a visible form and the page shows none of it, if it asks which
one to buy and never says, or if there is no editorial tension anywhere on
it.

## Operating rules

- **Never write the page from the distillation.** The whole skill exists
  because that has already happened twice.
- **When the panel disputes what exists, check the artifact** before
  writing a word about it. See Phase 2.5. The corpus cannot settle a
  question about the present state of a thing you can open.
- **A page that resolves everything is a page that hid something.** Real
  sources disagree and real corpora have holes; if the draft contains no
  stated limit, no split and no "we could not establish", the honest
  version is still in the reports and did not make it out. The auditor
  fails on this now, and it failed a published page that passed every
  other gate.
- **Engagement is not comprehension.** The measured result across six
  studies is that this format buys attention and perceived clarity, not
  understanding. Never claim otherwise in the page's own copy.
- **A claim with no source does not ship.** Say "no public data" rather
  than reaching for a weaker source.
- **A paywalled lab verdict is a source, and a good one.** Which?, RTINGS,
  Choice, Consumer Reports and Stiftung Warentest run tests nobody else
  runs. Cite the published verdict as the verdict it is, name the protocol
  where they state it, record in `limits` that the underlying measurements
  are not public, stamp the test year, and never redraw their tables. The
  free alternatives — affiliate listicles, vendor claims, retailer star
  averages — are systematically worse evidence, so declining a paywalled
  verdict makes the page weaker rather than more rigorous.
- **A recommendation page recommends.** Where the question is which one to
  get, the categories, the three ranked picks and the overall winner are
  the deliverable, and a survey of the field is not a substitute for them.
  A ranking is an inference and renders as one.
- **Characterise a disagreement no more strongly than the evidence
  does.** A page this skill produced wrote that a backend "invented" a
  figure, when the evidence said only that the figure circulated without
  a traceable citation — and the figure later turned out to be real and
  merely misdescribed. Overclaiming about the corpus is the same defect
  as overclaiming from it, and it is more embarrassing on a page whose
  argument is that others overclaim.
- **Report costs honestly** — the plan's band before the spend, the
  actual after, and any member that failed.
- **Subagents never run git operations**; the orchestrating session owns
  every commit.
