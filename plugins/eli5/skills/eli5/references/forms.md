# Forms — letting the mechanism pick the shape of the page

Three explainers built by this skill's first version opened with the same four headings in
the same order — `The turn`, `Where this analogy breaks`, `The second lens: …`, `The real
thing` — under the same three-tab strip, over 1,024, 1,293 and 1,636 words of prose and
three or four static SVGs each. Nothing in them was wrong. They were indistinguishable.

The cause is a single mandated architecture. Anthropic names the failure directly: *"You
tend to converge toward generic, 'on distribution' outputs… You still tend to converge on
common choices across generations. Avoid this."* A skill that prescribes one page shape
converges by construction, because the shape is the prescription.

The fix is not a better template. It is to let the mechanism pick the shape, and the eight
below are the shapes that keep recurring rather than the shapes that exist. **Take one when
it fits, adapt it when it nearly fits, and invent one when the mechanism suggests something
not listed** — a form you can justify from the invariant is a better answer than the closest
row in a table. Say in the artifact which you did.

## Eight that recur

Read the causal invariant you named in Phase 1 and ask what kind of thing it is.

| Form | Use when the invariant is | Architecture it suggests | Spine |
|---|---|---|---|
| **Machine** | a discrete process with state, run step by step | control deck above a stage, readouts inside the diagram | step / play / scrub |
| **Field** | continuous quantity spreading under a gradient | full-bleed canvas, controls floating over it | drag a source, watch it propagate |
| **Solid** | genuinely spatial or geometric | 3D viewport with a 2D inset that stays in sync | orbit, slice, unfold |
| **Ladder** | nested layers of abstraction, each hiding the one below | one continuous surface driven by a depth control | peel down a stratum at a time |
| **Fork** | two regimes that diverge under one variable | split screen, both halves on one shared control | move the control, watch them separate |
| **Trace** | causal ordering — what had to happen before what | a scrubber timeline as the page's spine | scrub, branch, replay |
| **Assembly** | compositional: parts that combine under rules | parts bin beside a workbench | drag parts in, get told what you built |
| **Reveal** | one structure transforming through a sequence | vertical scroll with a pinned stage | scroll drives the transformation |

Worked assignments, so the mapping is concrete rather than a category list:

- Raft leader election → **Machine**. Nodes hold state, terms advance in steps.
- TCP congestion control → **Field** or **Trace**; window size over time is a Trace.
- Quaternion rotation → **Solid**. The invariant is orientation; flat pictures lose it.
- What happens when you type a URL → **Ladder**. Each layer hides the one beneath.
- Eventual against strong consistency → **Fork**. One latency control separates them.
- A git rebase → **Trace**. The whole point is which commit preceded which.
- Transformer attention → **Assembly**. Q, K and V combine under a fixed rule.
- How a diffusion model denoises → **Reveal**. One image transforming, step by step.

Record the form and one sentence of why in the artifact's source as an HTML comment, so a
later edit does not drift into a different architecture halfway down.

Which surface each one usually lands on — `motion-and-media.md` carries what to build with
them and the test each has to pass:

| Form | Usual surface |
|---|---|
| Machine, Fork, Ladder, Assembly | plain SVG; GSAP once a state change moves several things in order |
| Field | canvas 2D |
| Solid | Three.js, with a 2D inset |
| Trace | SVG with a GSAP timeline the scrubber drives |
| Reveal | GSAP with ScrollTrigger, one pinned stage |

A rendered clip belongs in any of them when the sequence is too expensive to compute live —
scrubbable, inlined, never autoplaying.

## What each one tends to need

Notes from building them, not requirements. Each is one sentence of the trap the form falls
into and one of what avoids it; the rest of the design is yours.

**Machine.** A reader who overshoots and cannot step backwards re-runs from the start and
stops reading, so give the stepper both directions.

**Field.** A DOM-node grid past roughly 500 cells drops frames, which is the count that
usually forces canvas. One quantity per colour ramp, with the legend keyed to the same ramp.

**Solid.** 3D is easy to make impressive and hard to make legible; a 2D inset showing the
same state projected is usually what does it. Frame the subject to fill the viewport at
first paint.

**Ladder.** Draw every stratum in one coordinate frame, or descending reads as a page change
rather than as depth. Past five strata the depth control is a scrollbar with extra steps.

**Fork.** Both halves on one control and one stated scale. The crossover — where they swap
which is better — is usually the moment worth building.

**Trace.** Real ordering, and both arms where a branch exists. Scrubbing is dragging, so it
needs pointer capture and `touch-action: none`.

**Assembly.** A parts bin holding only the right parts is a button. Wrong assemblies get told
what they built and what it would do, rather than "try again".

**Reveal.** Scroll position is the reader's clock, which is what §1.8 asks of motion, so this
form needs no play button — but it does need a reduced-motion path that lands each state
statically. One object transforming beats a new picture per section.

## Commit to a look, and let it be yours

The architecture is half of not converging. The other half is that the page has an aesthetic
somebody chose. Anthropic's frontend guidance is the source and it is worth reading as
permission rather than as a checklist: *"Commit to a cohesive aesthetic… Dominant colors
with sharp accents outperform timid, evenly-distributed palettes"*, and *"Vary between light
and dark themes, different fonts, different aesthetics."*

Decide the palette, the type and the ground before writing markup, and put them in `:root`
as named tokens so the rest of the file inherits one decision rather than forty. What those
decisions are is yours. Three things that are worth knowing while you make them:

- **Google Fonts is the one permitted external host** (`fonts.googleapis.com`,
  `fonts.gstatic.com`) — what the artifact CSP allows. Every face needs a real fallback
  stack, because the same file opened offline falls back rather than fails. Anthropic names
  Inter, Roboto and Space Grotesk as the choices models converge on.
- **A flat white ground is the strongest single "generated" tell.** Atmosphere carries no
  claim, so §1.7's coherence principle does not bite it.
- **One well-built moment beats scattered micro-interactions**, per the same guidance. Pick
  where the delight lives — a crossover snapping into place, a solid unfolding — and spend
  the effort there.

## Where fun and the coherence principle meet

Mayer's coherence principle costs d = 0.65–0.86 when violated, and it forbids interesting
material that carries no information (`evidence.md` §1.7). That is a real constraint and it
stays.

It does not forbid a page being enjoyable. The distinction that holds both: **delight comes
from operating the mechanism, never from decoration bolted beside it.** A satisfying scrub,
a solid that unfolds under the reader's hand, a field that settles — every one of those is
the mechanism itself being pleasant to drive, so every mark still encodes a real variable.
Ambient particles, drifting gradients that track nothing and motion that plays whether or not
anyone is watching are the ones coherence rules out, and they are ruled out.

This position is a reading of §1.7 rather than a finding. No study in the panel measured
whether an enjoyable explainer teaches better than a plain one carrying the same
information; `evidence.md` §3 records that gap.

## The sameness checks, and why they are mechanical

Two of the gate's rules exist only because of the failure this file addresses.

`no-template-boilerplate` fails when three or more phrases from the first version's
worked examples appear verbatim. Those phrases were never rules — they were illustrations —
and all three sample artifacts reproduced them word for word. Headings come from the topic's
own vocabulary: a Raft explainer's sections are named after terms, quorums and logs.

`prose-budget` and `prose-block` count words outside `<svg>` and `<canvas>` only, so moving
a sentence onto the thing it describes both satisfies spatial contiguity (d = 0.72–1.19) and
spends nothing against the budget. The rules pull the same direction on purpose.
