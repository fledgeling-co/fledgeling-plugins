---
name: eli5
description: >-
  Build an interactive, self-contained HTML explainer that makes a hard idea genuinely
  click — grounded in the cognitive science of how people actually form mental models,
  not in baby-talk. Runs a five-phase pipeline: find the causal invariant and the
  misconception worth defeating; build a structure-mapping analogy that carries a
  stated boundary where it stops being true; stage three disclosure tiers around a
  Predict-Observe-Explain beat where the reader commits a guess before the reveal;
  draw against a declared geometry contract so the SVG does not warp; then pass a
  deterministic linter that fails the build on external assets, missing viewBox,
  uncaptured pointers, leaked animation frames, buried analogy limits, absent
  prediction beats and condescending register. Use whenever someone wants a hard
  thing explained visually — "/eli5 <topic>", "explain how X works", "make me an
  explainer for Y", "I still don't get Z", "build an interactive diagram of this" —
  and whenever an explanation needs to survive contact with a reader who will act on
  it. Not for API reference or narrative slide decks (use deck-craft), and not for a
  general-purpose UI (use design-craft).
---

# eli5

Explaining something is not simplifying it. It is finding the one relationship the
whole thing turns on, building a bridge to something the reader already owns, and
then saying exactly where that bridge stops carrying weight.

This skill builds a **single self-contained HTML file** that does that. Every rule
below traces to a row in `references/evidence.md`, which carries the citations from a
four-backend research panel and marks the places the panel disagreed.

Two things it refuses. It does not talk down — the register is a brilliant colleague
from a different field, never a five-year-old. And it does not ship an analogy without
its boundary, because an unbounded analogy is how a confident misconception gets
installed.

## The register, first

Get this wrong and nothing downstream matters.

| Anti-pattern | What this skill writes instead |
|---|---|
| "Imagine a little hungry monster eating cookies inside your RAM!" | "Memory is a grid of numbered lockers, each holding one letter." |
| Surface attributes: colours, cute names, anthropomorphism | Causal relationships: what drives what, what conserves, what feeds back |
| One omnibus metaphor, stated as truth | A mapped analogy with its non-alignable parts named |
| Emoji standing in for a diagram | Inline SVG where every mark encodes a real variable |

Same reading age. The difference is that one of them is true. Measured failure: ELI5
prompting reliably degrades into condescending baby-talk and superficial metaphor
(`evidence.md` §1.11).

## Phase 1 — Deconstruct

Before any analogy, name three things in your own working notes:

1. **The causal invariant.** The one relationship the system turns on — the thing that,
   once seen, makes the rest follow. Raft's is *a term with a majority is authoritative;
   a term without one is a proposal*. Not a feature list; a mechanism.
2. **The misconception worth defeating.** What does a smart person wrongly believe here?
   Explainers that don't target one produce agreeable prose that changes nothing. Virtual
   memory's is *that addresses are places*. Attention's is *that the model looks things up*.
3. **The reader's likely entry point.** What they already know that is structurally close.

If the topic has more than one mechanism, pick the one that unlocks the others and say
in the artifact that you are doing so. Breadth is how explainers become inventories.

## Phase 2 — Map the analogy, and bound it

Structure-mapping (Gentner) is the constraint: analogy aligns **relational systems**, not
object attributes. "Both are large" is worthless. "Both have a quantity that flows under a
difference and meets resistance" is the whole explanation. All four research backends
converged here (`evidence.md` §1.1).

Write the mapping table before writing prose:

| Source (familiar) | Target (the topic) | Relation carried |
|---|---|---|
| Water pressure | Voltage | Drives flow |
| Flow rate | Current | Quantity per unit time |
| Pipe constriction | Resistance | Opposes flow |

Then write the row the analogy is *for*: **where it breaks.** Cut a pipe and water
sprays out; break a wire and current stops entirely. Electrons do not leak into the room.

This becomes the artifact's **Boundary Card**, and it is not optional. Analogy-induced
misconceptions are durable and hard to correct once formed; the named mitigation across
the literature is an explicit limits-of-the-analogy segment. It lives at tier 1 or tier 2
— never tier 3, because a caveat the reader never reaches is a caveat that does not exist
(`evidence.md` §1.6).

**When the topic has more than one mechanism, add a second lens** that is structurally
different rather than a restatement — a single analogy collapses multi-factor systems into
single-cause models (`evidence.md` §1.2).

## Phase 3 — Stage the disclosure, around a prediction

**Exactly three tiers. No nesting.** Tabs or a stepper, never expanders inside expanders;
nested disclosure buries content readers then never find (`evidence.md` §1.6).

1. **The turn** — the causal invariant, one live variable, the Boundary Card in reach.
2. **The mechanism** — the steps, reader-paced, with state changes signalled.
3. **The real thing** — what production systems actually do, edge cases, and an explicit
   statement of what this account still leaves out.

Tier 3 owes the reader that last sentence. Simplification without a marker of its own
incompleteness produces the illusion of explanatory depth — readers who believe they
understand more than they do, and act on it (`evidence.md` §1.12).

**Include a skip-ahead control.** Scaffolding that lifts novices measurably impedes
experts (`evidence.md` §1.5). Nobody is made to walk through tier 1 to reach tier 3.

### The Predict-Observe-Explain beat — the highest-leverage rule here

At least one interaction must ask the reader to **commit a guess before the reveal.**

A slider that merely responds is close to decorative: dragging without hypothesising is
merely *Active* engagement, d ≈ 0.20–0.40 over passive. Committing a prediction first is
*Constructive*, d ≈ 0.40–0.60 over active — roughly double (`evidence.md` §1.3). This is
the single change most likely to make an explainer teach rather than entertain, and it is
the one most commonly skipped.

Shape it as: *"Three of five nodes can see each other. Two cannot. Who wins the election?"*
→ reader picks → simulation runs → the answer, and why the intuition was reasonable.

**One live variable in tier 1.** Novices handed a fifteen-slider sandbox tinker without
forming causal models; multi-parameter exploration is tier 3 or absent (`evidence.md` §1.4).

## Phase 4 — Draw against a geometry contract

Models do not place shapes; they predict coordinate tokens, and they never render what
they wrote. Syntactically perfect SVG routinely draws overlapping boxes and arrows through
text — Gemini's panel names this **open-loop visual blindness** (`evidence.md` §1.9).

The mitigation is to decide geometry before emitting markup. `references/artifact-engineering.md`
carries the contract in full; in short:

```
viewBox="0 0 960 540"    fixed, declared once, never per-element pixel widths
bands:  header  y   0–72     |  stage  y  72–420     |  readout  y 420–540
columns: 60 · 300 · 540 · 780 · 900     (elements snap to these, nothing floats)
```

Place every element against a named band and column, then write the markup. Text anchors
at a column, boxes centre on one, arrows run band-to-band.

Non-negotiables, all mechanically enforced in Phase 5:

- **Zero external assets.** No remote images, CDN scripts, stylesheets or fonts. A blocked
  request fails *silently* in sandboxed artifact runtimes, so the page half-renders and
  reports nothing (`evidence.md` §1.10). Everything inline.
- **`viewBox` on every `<svg>`**, with `width="100%"`. Hardcoded pixel dimensions clip
  inside constrained panels.
- **Pointer capture on any drag.** `setPointerCapture` plus `touch-action: none`, or the
  interaction dies on touch the moment the finger leaves the element.
- **Cancel your animation frames.** Unbounded `requestAnimationFrame` leaks CPU and
  desynchronises state. Prefer demand-driven rendering — draw when state changes.
- **No autoplay-only motion.** Animation's advantage evaporates on transience; every
  animation is steppable and inspectable at rest (`evidence.md` §1.8).
- **SVG for structure, canvas past ~500 nodes.** SVG gives DOM events, ARIA and crisp
  scaling; canvas earns its place only for continuous particle-scale simulation.

Layout follows the multimedia evidence rather than taste (`evidence.md` §1.7): readouts sit
**inside or adjacent to** the diagram, never in a separate card (spatial contiguity,
d = 0.72–1.19); steps are reader-paced (segmenting, d = 0.79–0.98); every mark encodes a
real variable, and decorative art, background particles and ambient motion are cut
(coherence, d = 0.65–0.86); state changes are signalled (g = 0.46–0.53).

Theme both schemes with CSS custom properties on `:root`, redefined under
`@media (prefers-color-scheme: dark)`. Give `body` an explicit background.

## Phase 5 — Gate it

```bash
python3 scripts/lint_explainer.py <file.html>     # must exit 0
```

Sixteen checks across four families — containment, geometry, interaction and pedagogy.
It fails the build on external assets, missing `viewBox`, uncaptured pointer drags, leaked
animation frames, a missing or buried Boundary Card, an absent prediction beat, wrong tier
count, and baby-talk register.

`--self-test` proves every rule can fail against built-in fixtures before you trust it
passing. Run it once on a new machine; a gate whose checked count has quietly gone to zero
reports green on everything.

Then **open the file and look at it.** The linter cannot see a warped diagram — that is
precisely the failure mode in `evidence.md` §1.9. Open it in a real browser
(`open -a "Google Chrome" <file>`); Obscura drops whitespace at inline-element boundaries
and will make correct prose look broken.

## What this skill will not claim

Every effect size above comes from human-authored instructional material. No randomised
trial measures learning gains from AI-generated explainers against human-crafted ones —
all four backends flagged that absence (`evidence.md` §3). The evidence justifies these
design choices; it does not predict an outcome for any particular artifact.

The three-tier count and the fade rate are defensible defaults, not findings; the
literature conflicts on both (`evidence.md` §2.4).

## References

- `references/pedagogy.md` — the frameworks in operational form: ICAP and POE phrasing,
  structure-mapping worked examples, misconception inventories by domain.
- `references/artifact-engineering.md` — the geometry contract, the SVG idiom set, pointer
  and animation lifecycles, theming, accessibility floor.
- `references/evidence.md` — citations, panel convergence, the disagreements, the gaps.
- `scripts/lint_explainer.py` — the deterministic gate.

## Credit

This skill is a rebuild of **`eli5`** by **Thariq Shihipar**, published in Anthropic's
`claude-plugins-community` marketplace under MIT. That skill named the need — a picture
explainer, few words, dead simple — and its framing is the reason this one exists. What
is added here is the pedagogy underneath it and a gate that fails.
