---
name: dossier-report
description: Turn a research question into one published, uniquely-themed HTML report page — a Dossier paid+free deep-research panel read in full, compiled into a claim graph, then designed from scratch around its own subject and written out to ~/Dev/dossier/<slug>/index.html for <slug>.fledgeling.app. Every page gets its own visual language, GSAP motion, conditional three.js, claim-local citations with source popups, a verified source registry, and the Dossier/Margin marketing chrome. Use whenever someone wants a topic researched and published as a page, an infographic, a field report, an evidence page or a write-up — "research X and make a page for it", "build me a page about Y", "turn this research into a report page", "publish a dossier page on Z", "make an infographic about W" — and also when they hand over an existing research corpus and want it turned into a page. Prefer this over a plain design pass whenever the page's substance has to come from research and every claim needs a source behind it.
---

# Publishing a research page

One topic in, one page out: researched by a panel, argued from a claim
graph, designed around its own subject, and published to its own
subdomain.

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

## The shape of a run

Nine phases. Phases 1 and 5 both use `/trawl` for divergence; phases 0,
4 and 8 are the human checkpoints.

| # | Phase | Routes to |
|---|---|---|
| 0 | Sharpen the brief | `/clarify` |
| 1 | Diverge on research angles | `/trawl` |
| 2 | Run the panel, read all of it | Dossier MCP |
| 3 | Compile the claim graph | — |
| 4 | Name, aesthetic and icon concept | `/clarify` |
| 5 | Diverge on visual direction | `/trawl` |
| 6 | Build the page | `design-craft`, `ux-craft`, `create-luke-content` |
| 7 | Build the page icon | `create-mac-icon` |
| 8 | Audit, index, ask before deploy | `design-review` |

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

## Phase 3 — Compile the claim graph

Before any design happens, turn the corpus into a claim ledger. This is
what stops a page's claims outrunning its sources, and it is the artifact
the citation UI is generated from rather than retrofitted onto.

Every claim carries: an id, its exact text, a confidence, whether it is
**direct or inference**, its source ids, the specific passage or table
that supports it, and its scope and limits.

The build fails if a quantitative or attributed claim has no source, if a
cited source supports only a nearby proposition rather than the claim
itself, or if something assembled by reasoning is rendered as an
empirical finding. Inferences are labelled as inferences on the page.

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

Trawl reference before diverging, where the MCP is installed: `search_sections`
(`platform: web`) on the block types this report is made of — evidence callouts,
comparison tables, stat rows, long-form reading surfaces. Two searches, images
opened, and one line in the direction record naming what transferred. Structure
and density transfer; identity does not.

Run `/trawl` on the aesthetic before designing, and give it the subject
matter as the frame material. This is what makes each page different from
the last, and skipping it is how a producer of many pages converges on
one look.

The evidence is blunt about why: measured across ~2M pairwise
comparisons, layout similarity fell 44% over a decade, and the strongest
correlate was **shared use of a small number of libraries**. The
invariant that reads as sameness is **layout skeleton and motion
signature, not palette**. Re-colouring a previous page fixes nothing.

Before designing, read `~/Dev/dossier/*/index.html` — the pages already
published — and treat their section silhouettes, hero shapes, chart
grammars and transition metaphors as **taken**.

## Phase 6 — Build the page

Full craft rules, with the evidence behind each: `references/page-craft.md`.

Route the design to `design-craft` with `ux-craft`'s lens on flow and
states. Route **every word of prose** to `create-luke-content` —
headline, standfirst, section copy, chart captions, the closing band.
The page is published under Luke's name and reads as his.

The rules that matter most, in short:

- **Lead with the conclusion.** Median scroll depth is ~50%, ~38% of
  arrivals leave immediately, and only a quarter pass the 1,600th pixel
  of a 2,000-pixel article. A structure that withholds the finding until
  state twelve is built for the readers who never arrive.
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

Generate the marketing chrome with `scripts/build_chrome.py` rather than
hand-writing it — the sticky masthead marketing Dossier and Margin
discreetly, and the overt closing band. Both are required on every page.
It is the one constant between pages, which is why it is a script.

**GSAP is the standing motion layer and every page loads it.** It owns at
least one scrubbed or pinned episode; simple reveals still compile to CSS
scroll timelines underneath, which run off the main thread. If an
argument genuinely has no scrubbed or pinned moment, say so in the
methods note rather than quietly shipping without GSAP — an eval run
reasoned its way to zero GSAP from the tiering rules alone, which is
defensible on the evidence and is not the house rule.

**three.js is gated** — six tests in `references/page-craft.md`, all of
which must pass, run against a claim id rather than against the topic.
When 3D is rejected, say so in the page's own notes and ship the
annotated static graphic.

## Phase 7 — The page icon

Route to `create-mac-icon` with the chosen concept and the page's own
palette. It returns the layered master, the rasters and `audit.html`
with every take scored. Wire the result in as the favicon, the
`apple-touch-icon`, and the basis of the `og:image` — two of the three
existing pages ship with no `og:image` at all and share as bare links.

## Phase 8 — Audit, index, and stop

1. `python3 scripts/audit_page.py <page>/index.html` — cite↔source
   integrity both ways, self-containment, reduced-motion, WebGL
   fallback, both chrome blocks, share tags, alt text, weight. Errors
   block; warnings are for the reviewer.
2. `design-review` against the real render at multiple viewports.
   **Open the render yourself first** — serve the page, capture it at 1440 and
   390, and read the captures asking *"what is wrong with this?"*. The auditor
   proves structure; only looking proves the page is any good, and a script
   reporting success on a page nobody opened is the failure this step exists
   for. Same rule for the PDF export: render it to images and read them, since
   print CSS breaks in ways the screen version never shows.
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
recipes, if the hero is more specific than the evidence beneath it, or if
there is no editorial tension anywhere on it.

## Operating rules

- **Never write the page from the distillation.** The whole skill exists
  because that has already happened twice.
- **Engagement is not comprehension.** The measured result across six
  studies is that this format buys attention and perceived clarity, not
  understanding. Never claim otherwise in the page's own copy.
- **A claim with no source does not ship.** Say "no public data" rather
  than reaching for a weaker source.
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
