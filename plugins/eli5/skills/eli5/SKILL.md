---
name: eli5
description: >-
  Build an interactive, self-contained HTML explainer that makes a hard idea genuinely
  click — a thing you operate, not a document you read. Lets the mechanism pick the shape of
  the page from eight that recur (Machine, Field, Solid, Ladder, Fork, Trace, Assembly,
  Reveal) rather than giving every topic the same tabs, and commits to a palette and type
  pairing of its own. Grounded in the cognitive
  science of how people form mental models: a structure-mapping analogy carrying the
  boundary where it stops being true, a Predict-Observe-Explain beat where the reader
  commits a guess before the reveal, and readouts inside the diagram rather than beside it.
  Draws SVG against a declared geometry contract, reaches for canvas at field scale,
  inlines Three.js when the mechanism is spatial and GSAP when it is a transformation, and
  inlines generated imagery when the analogy's source domain is a real thing. A
  deterministic linter fails the build on external assets, missing viewBox, uncaptured
  pointer drags, leaked animation frames, motion with no reduced-motion path, buried
  analogy limits, absent prediction beats, thin visuals, single-mode interaction, prose
  over budget, condescending register and copied template headings. Use whenever someone
  wants a hard thing explained visually — "/eli5 <topic>", "explain how X works", "make me
  an explainer for Y", "I still don't get Z", "build an interactive diagram of this". Not
  for API reference or narrative slide decks (use deck-craft), and not for a general-purpose
  UI (use design-craft).
---

# eli5

Explaining something is not simplifying it. It is finding the one relationship the whole
thing turns on, building a bridge to something the reader already owns, saying exactly where
that bridge stops carrying weight, and then handing the reader the controls.

This skill builds a **single self-contained HTML file** that does that. Every rule traces to
a row in `references/evidence.md`, which carries the citations from a four-backend research
panel and marks where the panel disagreed.

Three things it refuses. It does not ship an analogy without its boundary, because an
unbounded analogy is how a confident misconception gets installed. It does not ship a
document with a diagram in it: the reader operates the mechanism, and prose is what is left
over. And it does not write for someone who already knows.

## Who is reading, and it decides everything else

**A curious sixteen-year-old, or an adult who is sharp and has never worked on this.** They
can follow a real mechanism. They do not know your vocabulary, and they will not look
anything up — they will close the page.

That has one consequence, and it is the rule the whole skill turns on: **every word specific
to this topic is defined where it first appears, or replaced with a plain one.** Mark each
definition with `<dfn>`. Definitions cost nothing against the prose budget, so there is never
a reason to leave one out.

The failure this replaces was not baby-talk. It was the opposite, and the gate could not see
it — one artifact passed every check at 200 words while reading like this:

| What shipped | What the reader needed |
|---|---|
| "193 of 200 cards carry evidence that bites. Verified is a different axis." | "193 of the 200 tasks now have a test behind them. That was never what was blocking us." |
| "which classes to add, each one's oracle, and the closure count with its window" | "which kinds of bug to look for, how you would know you had found one, and how long to watch" |
| "every class at rung zero · coverage 65.9%" | "no category has got past the first of four levels. Two thirds of the code is watched." |

Every term in that left column — *card*, *class*, *rung*, *oracle*, *assay*, *closure*,
*escape*, *coverage* — is an ordinary English word carrying a private meaning. That is the
hardest kind of jargon to notice, because nothing about it looks technical.

**Aphorisms are not explanations.** *"Verified is a different axis."* is a sentence somebody
writes when they already understand. It states a conclusion and shows no mechanism, and it
is what compression produces when a hard idea meets a word budget. Meet the budget by cutting
claims and moving explanation onto the diagram, never by shortening sentences until they turn
into slogans. One line in the whole page may land like that; a page of them explains nothing.

The register is still not baby-talk: no "grown-up word", no magic, no cartoon monsters in
your RAM. Same reading age as before. The difference is that the reader can follow it.

**The word budget exempts `<svg>` text; the register does not.** Labels inside a diagram cost
nothing to write, which makes them where dense unexplained lines collect. One measured
artifact kept its worst there — *"inapplicable, not slow"*, *"approval is a one-way door"*,
*"a regulator is external"* — free against every count and read by nobody who was not already
on the project. `plain-statements` reads all visible text, diagram labels included.

### Where these rules come from

The slogan rules are lifted from `agent-voice`'s `references/ai-writing-signs.md` §1.7, which
names this failure as *"the epigram used in place of a plain statement"* and sets the budget
at roughly one landing line per page, and §2.3 on negative parallelism. Read that file when
prose here needs to sound less machine-made; it is the better source on the subject than
anything restated here.

Running an eli5 artifact through `agent-voice` itself does not help, and that is measured
rather than assumed: its seven registers are all agent-to-developer text, and its gate passed
the unreadable artifact above cleanly, flagging only em dashes on both it and a readable one
(`evidence.md` §4.8). The rules that apply are in the field guide, not in that gate.

## What is fixed, and what is yours

**Fixed: the numbers the gate checks.** Those name defects that are measurable — prose over
budget, a drag with no pointer capture, motion with no reduced-motion path, an analogy with
no stated limit. They bound the artifact; they do not design it.

**Yours: everything about how the page looks and behaves.** The form, the layout, the
palette, the type, what the reader touches first, where the delight lives. The references
carry precedents and the traps each one falls into, and a choice you can justify from the
mechanism beats the closest match in any table here. Where you depart from a suggestion, one
sentence of why in the artifact source is enough.

The failure this version was built to fix came from prescription: one mandated architecture
produced three artifacts with identical headings (`references/forms.md`). A second template
would do the same thing.

## Deliver what was asked, at the scope intended

One topic, one file. Build it in this session rather than delegating — the artifact is a
single file whose whole content is the mechanism you just worked out, and a subagent would
pay for a fresh context to re-derive it. Where the topic is genuinely several mechanisms,
say which one you took and why, in the artifact.

## Phase 1 — Deconstruct

Name three things in your working notes before any analogy:

1. **The causal invariant.** The one relationship the system turns on. Raft's is *a term
   with a majority is authoritative; a term without one is a proposal*. A mechanism, not a
   feature list.
2. **The misconception worth defeating.** What a smart person wrongly believes here.
   Explainers with no target produce agreeable prose that changes nothing. Virtual memory's
   is *that addresses are places*. Attention's is *that the model looks things up*.
3. **The reader's likely entry point** — what they already hold that is structurally close.

Breadth is how explainers become inventories. Pick the mechanism that unlocks the others.

## Phase 2 — Map the analogy, and bound it

Structure-mapping is the constraint: analogy aligns **relational systems**, not object
attributes. "Both are large" is worthless. "Both have a quantity that flows under a
difference and meets resistance" is the whole explanation. All four backends converged here
(`evidence.md` §1.1).

Write the mapping before the prose — source, target, and the relation each pair carries.
Then write the row the analogy exists for: **where it breaks.** Cut a pipe and water sprays
out; break a wire and current stops entirely. Electrons do not leak into the room.

That boundary ships in the artifact, in reach of a reader who stops early rather than at the
end. Analogy-induced misconceptions are durable and hard to correct once formed, and the
mitigation named across the literature is an explicit limits-of-the-analogy segment
(`evidence.md` §1.6). Give it its own visual treatment; name it in the topic's own words.

When the topic has more than one mechanism, add a second lens that is structurally different
rather than a restatement — one analogy collapses multi-factor systems into single-cause
models (`evidence.md` §1.2).

## Phase 3 — Let the mechanism pick the shape

**Read `references/forms.md`**, which carries eight shapes that recur — Machine, Field,
Solid, Ladder, Fork, Trace, Assembly, Reveal — with what each one tends to need. Take the
one that fits the invariant, adapt it, or build something the list does not have. Skipping
this phase is what produced three consecutive artifacts with identical headings over an
identical three-tab strip.

Whatever you pick decides the layout, the library and what the reader reaches for first.
Commit to a palette, a type pairing and a ground in `:root` before any markup, so the file
inherits one decision rather than forty.

**Headings come from the topic's vocabulary.** A Raft explainer has sections about terms,
quorums and logs. Copied stage names are what the gate's `no-template-boilerplate` rule
fails on, at three or more.

## Phase 4 — Stage the depth, around a prediction

Depth is staged in three passes, and the **form decides how** — scroll position, a depth
control, what the reader unlocks, tabs where tabs genuinely fit. No nesting: nested
disclosure buries content readers then never find (`evidence.md` §1.6).

1. **First pass** — the causal invariant, one live variable, the boundary in reach. **Under
   120 words of prose.** A reader who stops here leaves with the mechanism.
2. **Second pass** — the steps, reader-paced, with state changes signalled.
3. **Third pass** — what production systems do, the edge cases, and a plain statement of
   what this account still leaves out. Simplification with no marker of its own
   incompleteness produces the illusion of explanatory depth (`evidence.md` §1.12).

Give experts a route past the first pass. Scaffolding that lifts novices measurably impedes
them (`evidence.md` §1.5).

### The prediction beat — the highest-leverage rule here

At least one interaction asks the reader to **commit a guess before the reveal.**

A slider that merely responds is close to decorative: dragging without hypothesising is
*Active* engagement, d ≈ 0.20–0.40 over passive. Committing a prediction first is
*Constructive*, d ≈ 0.40–0.60 over active — roughly double (`evidence.md` §1.3). It is the
single change most likely to make an explainer teach rather than entertain, and the one most
often skipped.

Shape it as: *"Three of five nodes can see each other. Two cannot. Who wins the election?"*
→ reader picks → the simulation runs → the answer, plus the one assumption that made the
wrong pick a sound inference and where that assumption stops holding.

**One live variable in the first pass.** Novices handed a fifteen-slider sandbox tinker
without forming causal models; multi-parameter exploration belongs in the third pass or
nowhere (`evidence.md` §1.4).

## Phase 5 — Build it

`references/artifact-engineering.md` carries the geometry contract, the library recipes, the
media pipeline and the accessibility floor. The parts that decide whether the file works at
all:

- **Decide geometry before emitting markup.** Models predict coordinate tokens and never
  render what they wrote, so valid SVG routinely draws arrows through text — Gemini's panel
  names this *open-loop visual blindness* (`evidence.md` §1.9). Declare a viewBox and a grid
  of your own choosing, write it into a comment, and place every element against a named line
  in it. The mitigation is committing to the geometry first; the particular grid is yours.
- **Everything inline, Google Fonts excepted.** No CDN scripts, remote images or `fetch`. A
  blocked request fails *silently* in sandboxed runtimes, so the page half-renders and
  reports nothing (`evidence.md` §1.10). GSAP and Three.js are inlined from a vendored copy
  by `scripts/vendor_lib.py`; generated images are inlined as data URIs by
  `scripts/embed_media.py`.
- **Reach for a library when the form asks for one.** Three.js when the mechanism is spatial,
  GSAP with ScrollTrigger when it is a transformation the reader scrolls through, canvas past
  roughly 500 elements, plain SVG otherwise. A vendored library costs 72 KB to 690 KB in the
  file; that buys nothing on a Machine or a Fork, so those stay on SVG.
- **Generated imagery carries the analogy's source domain**, or it does not belong. A
  photograph of a lock and a key anchors better than a rectangle labelled "lock". Cap it at
  three images per artifact, caption each with what it depicts and that it was generated, and
  say in your reply what the run spent — `media-gen-pro` bills per image. `svg: true` routes
  to Arrow and returns real vector you can inline and edit, which suits diagrams.
- **Never ship a dead control.** A button with no handler invites an action that does
  nothing, and the reader blames themselves. One recorded run of the first version shipped 25
  controls and zero JavaScript, and it looked finished.
- **Every mark encodes a real variable.** Readouts sit inside the diagram, not in a card
  underneath (spatial contiguity, d = 0.72–1.19); steps are reader-paced (segmenting,
  d = 0.79–0.98); state changes are signalled (g = 0.46–0.53); ambient motion and decorative
  art are cut (coherence, d = 0.65–0.86) (`evidence.md` §1.7).
- **Motion is the reader's.** Steppable, scrubbable or scroll-driven, and inspectable at
  rest — transience is why animation often loses to a static diagram (`evidence.md` §1.8).
  Every artifact with motion carries a `prefers-reduced-motion: reduce` path that lands each
  state statically.

### The prose budget, and it is the point

The three artifacts that prompted this rewrite ran 1,024, 1,293 and 1,636 words of prose.
All the budgets below are counted **outside `<svg>` and `<canvas>`**, so a sentence of
explanation moved onto the thing it explains costs nothing and satisfies spatial contiguity
at the same time. That is the move to reach for first: most prose that feels necessary is an
annotation in the wrong place.

| Budget | Warns | Fails |
|---|---|---|
| Prose on the page | 300 | **350** |
| Any single text block | 35 | **50** |
| Unbroken run between two things to look at or touch | 80 | **120** |
| Words before the reader can do anything | 60 | **90** |

The block cap is the one that changes how a page reads. A page can sit inside its total and
still open with a wall: measured on an artifact that passed at 367 words, the three blocks a
reader called wordy ran 73, 48 and 38, against captions of 14 to 22 that drew no complaint.

**Text inside `<dfn>` is exempt, like text inside `<svg>`.** These budgets exist to cut the
number of claims a page makes, not to make each claim terser. A page that meets them by
compressing produces the aphorism register above, which is a worse failure than the length
it fixed — plain language costs more words than a slogan, and that trade is the right one.

Alongside them, floors: at least **three visual scenes** and at least **two distinct kinds of
interaction** among drag, slider, step, pick, scroll, orbit and keyboard.

### Markers the gate reads

Four attributes let the gate check staging and vendoring without forcing any particular
chrome on the page, so a scroll-driven Reveal and a tabbed Machine are checked the same way:

| Attribute | Goes on |
|---|---|
| `data-pass="1"`, `"2"`, `"3"` | the container for each depth pass |
| `data-boundary` | the element stating where the analogy stops being true |
| `data-predict` | the element asking the reader to commit a guess |
| `data-vendor="three"` etc. | an inlined library, so it is excluded from the containment and word-count scans |

Artifact code lives outside the `data-vendor` block. Code written inside one is excluded from
the pointer, animation-frame and network scans along with the library.

## Phase 6 — Gate it

```bash
python3 scripts/lint_explainer.py <file.html>     # must exit 0
```

Thirty-one checks across five families — containment, geometry, interaction, pedagogy and
composition. `--self-test` proves every rule can fail against built-in fixtures; run it once
on a new machine, because a gate whose checked count has quietly gone to zero reports green
on everything.

Then open the file and look at it. The linter cannot see a warped diagram, which is exactly
the failure mode in `evidence.md` §1.9. Use a real browser — `open -a "Google Chrome"
<file>` — since Obscura drops whitespace at inline-element boundaries and will make correct
prose look broken.

## What this skill will not claim

Every effect size above comes from human-authored instructional material. No randomised
trial measures learning gains from AI-generated explainers against human-crafted ones; all
four backends flagged that absence (`evidence.md` §3). The evidence justifies these design
choices and does not predict an outcome for any particular artifact.

The three-pass count and the fade rate are defensible defaults rather than findings; the
literature conflicts on both (`evidence.md` §2.4). The position that an enjoyable mechanism
teaches as well as a plain one is a reading of the coherence principle, not a measurement,
and `references/forms.md` says so where it is taken.

## Reporting back

Name the form and why the mechanism chose it, the file path, the lint result, and what any
`media-gen-pro` calls cost. Four to six lines.

## References

- `references/forms.md` — the eight forms, what each owes, and the identity pass.
- `references/pedagogy.md` — ICAP and POE phrasing, structure-mapping worked examples,
  misconception inventories by domain.
- `references/artifact-engineering.md` — geometry contract, library and media recipes,
  pointer and animation lifecycles, theming, accessibility floor.
- `references/evidence.md` — citations, panel convergence, the disagreements, the gaps.
- `scripts/lint_explainer.py` — the deterministic gate.
- `scripts/vendor_lib.py` — inline GSAP or Three.js into a single file.
- `scripts/embed_media.py` — resize and inline a generated image as a data URI.

## Credit

This skill is a rebuild of **`eli5`** by **Thariq Shihipar**, published in Anthropic's
`claude-plugins-community` marketplace under MIT. That skill named the need — a picture
explainer, few words, dead simple — and its framing is the reason this one exists. What is
added here is the pedagogy underneath it and a gate that fails.
