# The three.js hero is rejected — and what to build instead

I haven't set up the particle field. `dossier-report` gates three.js behind six
tests in `references/page-craft.md` §3, and a scroll-reactive particle field on
a citation-behaviour report fails all three **evidence** tests. Failing an
evidence test rejects 3D *outright* — it isn't the "ship the fallback until it
passes" branch, which is only for the release tests.

Here is the ruling, the alternative hero, and what the page still needs before
any hero gets built.

---

## 1. The gate, run honestly

| # | Test | Verdict |
|---|---|---|
| 1 | **Spatial claim** — a major claim depends on depth, volume, orientation, topology, occlusion, assembly, or movement through physical space | **FAIL** |
| 2 | **Viewpoint necessity** — changing viewpoint *reveals evidence* rather than showcasing an object | **FAIL** |
| 3 | **2D insufficiency** — no map, cutaway, orthographic diagram, annotated image or small multiple can carry the claim at least as clearly | **FAIL** |
| 4 | Narrative mapping — every camera/object transition maps to a claim id | not reached |
| 5 | Equivalent fallback | not reached |
| 6 | Performance and reduced motion | not reached |

**Test 1.** The subject is a set of proportions: what share of page views produce
a citation click, what share of cited URLs are never opened, how that splits by
device. Rates and ratios have no depth, no volume, no occlusion and no physical
extent. There is nothing here that lives in space.

**Test 2.** There is no viewpoint from which a reader learns something new about
a percentage. Orbiting the field would showcase the field, which is precisely
the failure the test is written to catch.

**Test 3.** A unit grid renders "1 in 345" more clearly than any 3D scene, and
does it at a glance, on a phone, without WebGL. 2D is not merely sufficient
here — it is *better*, which makes test 3 fail decisively rather than narrowly.

Two independent rules in the skill land on the same answer:

- **The theme-proof test** (`references/aesthetic-direction.md`) names this exact
  artifact: *"Random palettes, generic particle fields and interchangeable dark
  'cinematic' heroes fail — not because they are ugly, but because they would fit
  any subject, which means they express none."* A particle field would sit just
  as happily on a page about shipping logistics or protein folding. That is the
  disqualifying property.
- **The motion budget** (§2) admits an animation only if you can finish *"this
  motion lets the reader perceive ___ that would otherwise require a difficult
  mental comparison."* For a scroll-reactive particle field the blank is
  "energy" or "immersion" — explicitly listed as decoration, not evidence.

And the authored review (§"The authored review") would fail the page on
*"the hero is more specific than the evidence beneath it"*: a dense, kinetic,
high-production hero over a finding that is fundamentally one ratio overstates
what the page knows.

Worth noting on the underlying evidence: Kim et al. built four data stories in
static, animated and immersive variants — immersive rated **more interesting and
more persuasive, and no more understandable or trustworthy**. On a page whose
entire subject is *readers not checking things*, buying persuasiveness without
comprehension is the wrong trade to make in public.

Neither published page (`~/Dev/dossier/undervolt/`, `~/Dev/dossier/workflows/`)
loads three.js, GSAP or a canvas at all — so there is also no precedent to
match here.

### What would flip this

This is not a blanket ruling against 3D. If the page's argument moved to, say,
the *topology* of a citation network — how sources cluster, which are structurally
load-bearing, where circular citation loops close — tests 1 and 2 could genuinely
pass, and the release tests would then decide it. Note the counterweight even
then: Kwon et al. found **2D better than 3D for spatial-memory tasks in
networks**. So a network topology claim gets 3D a hearing, not a pass.

---

## 2. Record the rejection on the page

The skill requires this — *"When 3D is rejected, say so in the page's own notes.
Recording the rejection is what stops the gate decaying into a formality."*
Drop this into the methods note:

> **On 3D.** A WebGL hero was considered and rejected. This page's central claims
> are proportions, not structures: nothing in them depends on depth, orientation
> or occlusion, and a unit grid states the ratio more clearly than a rendered
> scene at a fraction of the battery. The gate is recorded here rather than
> quietly skipped.

---

## 3. The hero that is actually defensible

The strongest device is already sitting in the page: **its own citation layer,
at scale.**

**The device.** A dense grid of citation markers — the same `<button class="cite">`
component the prose uses, multiplied. Inked markers are sources a reader opened;
outlined markers are sources nobody touched. The hero *is* the page's own
apparatus, drawn at the scale of the finding. Change the subject noun and the
metaphor collapses, which is exactly what the authored review asks for.

**The one admissible motion.** Not ambient drift — a scrub between **two states
of one encoding**, which is the case Heer & Robertson (n=24) found reduces
tracking error across every transition type tested:

- State A: every marker inked — *the sources this page offers you*.
- State B: the ~0.3% that get opened remain inked; the rest drop to outline.

Fill the blank honestly: *"this motion lets the reader perceive the gap between
sources offered and sources consulted, which would otherwise require holding
1,000 and 3 in mind at once."* That passes. Object identity is preserved, the
scale never changes, and no claim exists only in an intermediate frame — both
end states render directly from their ids.

**Reduced-motion branch** (built first, per §5's reduced-first rule): the two
states as static small multiples side by side, numbers set beside each. Every
fact survives; nothing is a zeroed-out duration.

**Tier.** IntersectionObserver for the state swap, or CSS `animation-timeline:
scroll()` behind an `@supports` guard. This does not need GSAP scrub — and a page
with no scrub does not need GSAP at all.

**Editorial tension** — the page needs one, and this subject hands you a good one:
verification clicks are reportedly *more* common on shorter, lower-quality pages.
Readers verify when the page fails them, which inverts the intuition that
verification signals an engaged audience. Pair it with the honest limit: the claim
that better citation UX makes readers verify is unsupported in **either**
direction. A page that resolves everything reads as generated.

---

## 4. Sequencing — the hero is downstream of work not yet done

The request jumps to Phase 6. Phases 0–5 haven't run, and the hero is a Phase 5–6
artifact for a structural reason: the visual device must map to a named concept in
the topic corpus, and there is no corpus yet.

Still outstanding: **Phase 0** `/clarify` on the brief (what decision does this
page inform, for whom); **Phase 1** `/trawl` on research angles; **Phase 2** the
Dossier panel, read end to end — never from the merged distillation; **Phase 3**
the claim graph, which is what the citation UI is generated *from* rather than
retrofitted onto; **Phase 4–5** slug, aesthetic and `/trawl` on visual direction.

One flag on sourcing. The figures I reasoned from above — ~0.29% of page views
producing an external reference click, 93% of cited URLs unclicked in a two-month
window, 0.56% desktop against 0.13% mobile, and the lower-quality-page inversion —
come from `references/page-craft.md` §4 citing Piccardi et al.'s instrumentation of
96 million Wikipedia citation events. That is the skill's own evidence base for how
to build citation UX. **It is not a research panel run for your page**, and it is
Wikipedia-specific. It tells you the *shape* the hero should take; it does not
license the page to state those numbers as its finding. Under the Phase 3 rule, a
quantitative claim ships only against a source read in full for this page.

Per the task constraints I ran no Dossier research, so nothing above is a
substitute for Phase 2.

---

## In one line

The particle field is rejected on all three evidence tests — the subject has no
spatial dimension, and a generic field would fit any topic, which is the
disqualifier. Build the hero from the page's own citation markers instead, scrubbed
between "offered" and "opened" — but build it after the research and the claim
graph, not before.
