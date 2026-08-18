# Page craft — the buildable rules

Every rule here traces to `evidence.md`. Where the evidence is contested
or absent, this file says so rather than inventing a threshold, because a
number nobody can source is a number nobody should tune against.

## Contents

1. [Narrative structure](#1-narrative-structure)
2. [The motion budget](#2-the-motion-budget)
3. [The three.js gate](#3-the-threejs-gate)
4. [Citation and provenance UX](#4-citation-and-provenance-ux)
5. [Accessibility floor](#5-accessibility-floor)
6. [Performance floor](#6-performance-floor)
7. [Chart integrity](#7-chart-integrity)
8. [Mobile](#8-mobile)
9. [The divider gutter](#9-the-divider-gutter)
10. [Light and dark](#10-light-and-dark)
11. [The reading surface](#11-the-reading-surface)

---

## 1. Narrative structure

**Martini glass is the default.** Segel & Heer's taxonomy, from 58
narrative visualisations: an authored stem that establishes the claim,
then opening to reader-driven exploration, sources and data. Interactive
slideshow for bounded explainers and the mobile stepper. Drill-down
*after* the main finding, never instead of it. Free exploration is never
the sole delivery mode — introductory stories measurably do **not**
increase later exploration.

**Lead with the conclusion.** Chartbeat instrumentation across ~2bn
pageviews: ~38% of arrivals leave immediately, median scroll depth ~50%
(Slate) to ~60% (web-wide), only 25% pass the 1,600th pixel of a
2,000-pixel article, and scroll depth correlates only very weakly with
sharing. The load-bearing finding belongs above the fold or in the first
two states.

### The TLDR band — required on every page

Leading with the conclusion is a principle, and principles get
interpreted. The band is the enforceable form of it, and **every page
ships one**, in every register, as the first content block after the
masthead.

It is a named section (`<section id="tldr">`), not a hero with a slogan in
it, and it holds five things and nothing else:

1. **The finding, in one sentence**, cited. The sentence a reader would
   repeat to someone else.
2. **Three to five cited claims** carrying the argument — the ones a
   sceptic would need before believing the finding, not the ones that were
   easiest to establish.
3. **The one thing that would change it** — the live disagreement, the
   limit, the missing measurement. A TLDR that reads as settled has hidden
   the page's own tension in the place a reader is most likely to stop.
4. **Where the page goes next**, in a clause. Not a table of contents.
5. **On a page recommending something, the verdict** — the pick, its cost,
   and the date the price or version was checked. See
   `product-verdicts.md`; on those pages the winner *is* the TLDR's first
   line.

Three rules keep it honest:

- **It is a derivation, not a summary written separately.** Every line
  traces to a claim in the graph that also appears further down the page. A
  TLDR and a page that disagree about the finding is the failure mode here,
  and generating both from one graph is what prevents it.
- **Every claim in it carries its marker, in every register.** The band is
  the most-read and most-quoted part of the page, so it is the last place
  an uncited number may sit.
- **Its arithmetic is recomputed before shipping.** Every ratio,
  percentage and multiple in the band, in each register — a Primer that
  re-expresses 95.4% as "about 19 in every 20" has done arithmetic the
  graph should record. A judge recomputed a rival page's opening bullet
  inside the sixty seconds it was built for and found it wrong; this is
  the cheapest possible way to lose a reader.

The band earns its space by being short. If it runs past a screen on a
phone, it is a section rather than a summary.

**Section rhythm.** Alternate ordinary document flow with bounded visual
episodes. Pinning the whole page sacrifices orientation, accessibility
and mobile resilience. Each episode:

1. prose setup stating the question
2. an orientation state explaining the visual grammar
3. semantically distinct states
4. a stable takeaway state that survives without motion
5. optional exploration, uncertainty, methods
6. return to normal flow before the next argument

**One claim per scroll state.** Operationally: each state has one
`claim_id`; its caption summarises it in one sentence; the visual delta
changes only the encodings that support it; objects representing the same
records keep their identity across states; a new chart grammar and a new
finding are never introduced together unless the transition explains
their relationship; reverse scrolling restores the prior state; and if a
caption contains two independent propositions, split the state.

**Parallelism aids memory** (Hullman et al., 42 professional narrative
visualisations): repeated structural relationships between adjacent
states let readers compare. Keep scales, positions and objects stable
unless the change *is* the evidence.

> The phrase "one idea per scroll state" is a production discipline, not
> a validated law — three of four backends flagged it explicitly. Keep
> the rule; do not cite a study for it.

**No universal state count exists.** All four backends returned
`MISSING_DATA` on words-per-step, state count, viewport-heights per
chapter and pin duration. Topic complexity, device height and chart
literacy confound it. Derive from the argument, not from a number.

---

## 2. The motion budget

**Two budgets, and conflating them is why this section used to read as
hostile to motion.** They answer different questions, they rest on
different evidence, and a page needs both.

| Budget | Answers | Governed by |
|---|---|---|
| **Evidence motion** | does this movement help the reader *perceive the data* | the test below, and it is strict |
| **Interface feedback** | does the reader know their input registered | the micro-interaction tier, and it is mandatory |

A control that does not acknowledge a press reads as broken; a chart that
animates for delight reads as untrustworthy. The same page owes the first
and must refuse the second.

### Evidence motion — the test

Motion inside a figure, an episode, or a transition between claims is
admissible only when you can finish:

> *"This motion lets the reader perceive ___ that would otherwise
> require a difficult mental comparison."*

If the blank is "energy", "delight", "premium quality" or "immersion", it
is decoration and does not get spent from this budget.

**Where animation measurably helps.** Heer & Robertson (n=24): animated
transitions between two states of *one encoding* reduced tracking error
across all tested transition types (`p<0.001`). Object-tracking
animations ran 1.25s, value-change 2s.

**Where it measurably hurts.** Tversky, Morrison & Bétrancourt: apparent
advantages over static graphics were confounds — the animated conditions
carried more information. After a week, text-studying participants
**improved** while animation-studying participants **declined**.
Robertson et al. found animated trends inferior to static traces and
small multiples for analysis, though preferred for presentation.

**More staging is not better.** Extreme staging was *worse* than direct
animation for donut value changes (`p=0.024`); stacked bars showed no
effect (`p=0.224`). Axis rescaling increased both errors and "unknown"
responses. Prefer the shortest transition that preserves object identity,
and keep scales common.

**The resolution**: animate *between two states of one encoding*; never
animate as a substitute for a static explanation. Provide persistent
static views wherever the task is comparison or verification.

### Interface feedback — the micro-interaction tier, and it is required

Every interactive element carries **default, hover, `:focus-visible`,
active and disabled**, and every async control carries loading. This is
not decoration and it is not drawn from the evidence budget: it is the
answer to *did that work*. A page whose reading toggle, theme control,
citation markers, filters and disclosures respond to a press with nothing
reads as broken regardless of how good its argument is.

The numbers are tight, because the reader is mid-sentence rather than
watching a show:

- **120–250ms** on a state change, `ease-out` on entry. Under ~100ms reads
  as instant and jarring; past ~400ms reads as laggy. Never
  `transition: all`.
- **The focus ring is never removed without a replacement**, and it is
  visible in both themes — `:focus-visible { outline: 2px solid
  var(--focus); outline-offset: 2px }`.
- **`cursor: pointer` on everything clickable**, including a card or a
  citation marker acting as one. A clickable thing with a default cursor
  reads as static text.
- **The active reading, the active theme and the current section are
  visually distinct**, not merely stored. A reader who cannot see which
  register they are in has lost the control the page is built around.
- **A citation preview appears on hover, focus *and* tap**, is hoverable,
  dismissible and persistent (WCAG 1.4.13), and closes on Escape with
  focus returning to the marker.

Micro-interactions are exempt from the evidence test and bound by
`prefers-reduced-motion` like everything else: under `reduce` a state
change lands instantly rather than not at all. A feedback state that
disappears under reduced motion has removed the feedback, not the motion.

### The motion stack, and GSAP as the standing layer

**GSAP is a hard requirement: every page loads it, and it owns the
choreographed reveal sequence, at least one scrubbed or pinned episode
where the argument has one, and any tween between two compiled figure
states.** That is a house rule and it is not an inference from the
evidence above — the evidence sets the *bar for what may move*, and the
house rule sets *what does the moving*. The two do not conflict: a page
that has earned no evidence motion at all has still earned its interface
feedback and its entrance choreography.

> An earlier version of this file let a page ship with no GSAP when its
> argument had no scrubbed moment, and an eval run took that to its
> logical end — a page with **no GSAP at all**, documented and defensible
> on the evidence. That escape hatch is closed. Where an argument
> genuinely has no scrubbed or pinned episode, say so in the methods note
> and spend the layer on the reveal choreography and the micro-interaction
> tier; the layer is present either way.

| Tier | Use for | Why |
|---|---|---|
| **Tier 0 — CSS transitions** | every hover, focus, active, disabled and selected state; all of the feedback above | Cheapest possible, no library involved, survives a script failure |
| CSS `animation-timeline: scroll()` / `view()` | Entrance reveals, progress bars, sticky-header states — anything expressible as transform/opacity over scroll progress | Runs off the main thread; browsers scroll on a separate process. Guard with `@supports (animation-timeline: scroll())`; **not Baseline in 2026**, so never the only carrier of meaning |
| IntersectionObserver | Discrete state changes: step *n* selects chart state *n* | Low cost, universal, no scroll listener |
| GSAP ScrollTrigger | **Scrub** and pinning that CSS cannot express; choreographed multi-element sequences needing runtime control | Precomputes positions, debounces scroll, syncs to rAF, throttles resize to a 200ms gap |

Tier 0 stays in CSS even with GSAP loaded. A hover state written as a
GSAP tween is a library call on every pointer move where a declarative
transition would do, and it stops working the moment the script does.

**Load it pinned, with SRI.** GSAP's plugins are all free including
commercial use since the Webflow acquisition — there is no membership, no
licence key and no private registry, so never generate `.npmrc` auth-token
instructions. Pin the version, keep `integrity` and `crossorigin`, and
register plugins once. GSAP and three.js are this page's only deliberate
CDN exceptions; §6 owns why.

**Choreograph with a timeline, not chained delays.** The position
parameter is the craft — `"-=0.35"` to overlap the previous tween's tail,
`"<0.15"` to start just after it began, labels for named beats. Entrances
that overlap read composed; strictly sequential entrances read as a
slideshow. Use `autoAlpha` rather than `opacity` so a faded-out element
stops eating clicks, set `gsap.defaults()` once as the motion tokens, and
put the reduced-motion and viewport branches in `gsap.matchMedia()`, which
reverts its own animations when a condition stops matching.

> **Contested, and stated as such.** Practitioner sources disagree on
> whether ScrollTrigger materially harms INP, and every specific claim on
> *both* sides traces to vendor-adjacent blogs. The widely repeated
> "≤30 active triggers" figure has **no traceable empirical basis**. What
> is primary-sourced is only the mechanism: CSS scroll timelines run off
> the main thread, GSAP timelines do not. No published benchmark compares
> INP across the tiers on mid-tier mobile. Do not tune against a number
> that does not exist.

### GSAP hazards, from its own documentation

Each converts directly to a build rule:

- Never animate the pinned element itself — it invalidates the
  measurements. Animate nested children.
- Pinning uses `position: fixed` deliberately; do not substitute
  transform-based pinning.
- An ancestor with `transform` or `will-change` breaks `position: fixed`.
  This is a browser behaviour, not a ScrollTrigger bug.
- `content-visibility: auto` prevents correct start/end calculation —
  exclude it from scrollytelling sections.
- Under `scrub`, child tween durations are **proportions of scroll
  distance**, not real time. To slow an animation, extend
  `end: "+=4000"`; never lengthen the durations.
- Create triggers top-to-bottom; pinning distance affects later triggers'
  start and end.
- One ScrollTrigger controls one timeline. Do not have several things
  driving one playhead.
- `once: true` kills the instance and lets it be collected.
- Use `gsap.matchMedia()` for viewport and reduced-motion branches; it
  reverts its animations when a condition stops matching.
- Refresh after fonts, images and chart dimensions settle — not during
  scroll.
- **`normalizeScroll()` is prohibited.** It forces scrolling onto the JS
  thread, which is scrolljacking by another name.

### Never touch native scrolling

NN/g usability testing: the majority of participants experienced at least
mild disorientation, and on a *fully* scrolljacked page **every
participant was disoriented** — some read it as a broken page. Murano
2026 (n=20) found no speed benefit and significantly **lower accuracy and
satisfaction**. Short scrolljacks create an *illusion of completeness*:
readers assume the page ended.

Keep wheel, touch, momentum, scrollbar, keyboard and history behaviour
native. Scrollytelling monitors scroll and changes content; scrolljacking
manipulates the scroll mechanics. The first is the pattern; the second is
the anti-pattern.

### Idempotent states

Readers skip across states faster than animations complete. Every state
must render directly and completely from its id, never depending on a
prior animation having finished. **No claim may exist only inside an
animated intermediate frame.**

---

## 3. The three.js gate

Six tests. All six must pass. Failing any *evidence* test rejects 3D
outright; failing any *release* test means shipping the fallback until it
passes.

**When to run it.** Against a **claim id**, at the end of Phase 3 — not
against the topic at Phase 5. A subject can be spatial while every claim
the corpus actually supports is enumerable in two dimensions, and test 3
is usually the one that decides. If the ledger holds only discrete states
(three seating positions, four configurations), sectioned small multiples
plus a bar chart win on Hullman's parallelism finding and on Kwon et al.
If it holds a sourced *continuous* mapping where two orthogonal sections
each hide the axis the other shows, 3D passes. "The topic is spatial" is
not the test.

**Evidence tests**

1. **Spatial claim.** A major claim depends on depth, volume,
   orientation, topology, occlusion, assembly, or movement through
   physical space.
2. **Viewpoint necessity.** Changing viewpoint *reveals evidence*, rather
   than showcasing an object.
3. **2D insufficiency.** A map, cutaway, orthographic diagram, annotated
   image or small multiple cannot communicate the claim at least as
   clearly.

**Release tests**

4. **Narrative mapping.** Every camera or object transition maps to a
   claim id. No decorative idle orbit.
5. **Equivalent fallback.** Static images, diagrams and text carry the
   same conclusion without WebGL — because **device capability cannot be
   reliably feature-detected**. Some browsers report WebGL support and
   are too weak to use it; practitioners infer from screen size because
   frame-rate probing and feature combinations all have flaws.
6. **Performance and reduced motion.** Meets the CWV budget on the target
   mobile tier, and fully disables non-essential camera motion under
   `prefers-reduced-motion`.

**Why the bar is this high.** Kim et al. built four data stories in
static, animated and immersive variants: immersive was rated **more
interesting and more persuasive**, and **no more understandable or
trustworthy**. A scene that raises persuasiveness without raising
understanding is rhetoric charged to the reader's battery. Kwon et al.
separately found 2D better for spatial-memory tasks in networks.

When 3D is rejected, say so in the page's own notes and ship the
annotated static graphic. Recording the rejection is what stops the gate
decaying into a formality.

**If approved**: dynamic-import after the narrative content; render on
demand rather than an unconditional loop; `dispose()` textures,
geometries and materials between chapters — GPU memory otherwise grows
until the tab crashes, and this survives review because it works fine in
short demo sessions; cap device pixel ratio; KTX2/Basis textures stay
compressed in VRAM where PNG and JPEG decompress fully; never raycast
against every object on every mouse move; handle `webglcontextlost`; and
keep labels, transcript and sources **outside** the canvas in normal DOM
order.

Draw calls are the binding constraint, not triangles. `InstancedMesh`
renders all instances of a geometry in one call. No sourced universal
polygon, texture-megabyte or draw-call budget exists — the ~0.1ms per
draw call figure traces only to commercial blogs. Derive from the target
device.

---

## 4. Citation and provenance UX

**Verification is rare, and that is the design input.** Piccardi et al.
instrumented 96 million Wikipedia citation events over two months:
external-reference clicks in **0.29% of page views** (0.56% desktop,
0.13% mobile), and **93% of cited URLs received no click** that month.
Clicks were *more* common on shorter, lower-quality pages — readers
verify when the page fails them.

So the citation layer is not built to be clicked. It is built so the
claim-source bond is inspectable and the page cannot quietly overclaim.

**Three layers, all three required:**

1. **Inline marker** immediately after the smallest claim span the source
   supports. Not bolted to a paragraph carrying several propositions.
2. **Preview** on hover, keyboard focus *and* tap: source title, author
   or organisation, date, evidence type, one sentence on *what this
   source supports*, and "open original". Escape closes; focus returns to
   the marker.
3. **Persistent registry** at the foot: deduplicated, full metadata,
   access date, and backlinks to every claim using that source.

**Tse's rule caps the whole design**: *"if you make a tooltip or
rollover, assume no one will ever see it."* Any design where a source
exists only inside a hover state has, by that rule, no sources.
Redundancy is the point.

**The markup contract** the auditor enforces. The marker is an **anchor,
not a button**:

```html
<!-- in the prose -->
<a class="cite" href="#r12" data-cite="r12" data-n="9"
   aria-describedby="r12">9</a>

<!-- in the registry -->
<li id="r12"><a href="https://…">Title</a>
  <span class="src">Publisher · what it establishes · year</span></li>
```

`data-cite` is the stable anchor; `data-n` is the number the reader sees.
They are separate so sources can be numbered by first appearance without
renumbering anchors when one is added mid-page.

> **Why an anchor and not a button.** A blind judge caught this on a page
> this skill produced: `<button data-cite>` markers are **inert with
> JavaScript disabled**, so the claim-to-source bond — the one thing the
> citation layer exists to protect — breaks in exactly the no-JS case
> this file tells pages to survive. An `<a href="#rN">` jumps to the
> registry with no JS at all, and the popover is then progressive
> enhancement layered on top: intercept the click, show the preview,
> `preventDefault()` only once the preview has actually rendered.

Charts have the same obligation. A figure drawn by script is absent
without script; ship the static SVG or the table in the DOM and let the
script enhance it, rather than printing a `<noscript>` apology.

**Trust evidence, stated honestly.** A *single* transparency feature had
almost no effect on perceived credibility; multiple co-present indicators
produced small but significant improvements (n=1,183, 4 of 15 measures).
Only 34% could identify the journalist and 26% recall a detail of an
explanation they had seen. A 2026 study found displaying reliability
information could *reduce* map trust and accuracy — transparency can
appropriately lower confidence when it reveals uncertainty.

> The claim "good citation UX makes readers verify" is unsupported in
> either direction. What is supported: previews lower exploration cost,
> and multiple co-present signals raise perceived credibility more than
> one does.

---

## 5. Accessibility floor

| Criterion | Level | Applies to |
|---|---|---|
| **2.2.2 Pause, Stop, Hide** | **A** | Auto-starting motion over 5s shown in parallel with other content. Mandatory under ADA Title II/III, Section 508, EN 301 549, EAA |
| **2.3.3 Animation from Interactions** | AAA | Explicitly covers scroll parallax |
| **2.3.1 Three Flashes** | A | Seizure risk. Reduced motion is not a substitute |
| **1.4.13 Content on Hover or Focus** | AA | Hover content must be hoverable, dismissible, persistent — the criterion naive citation tooltips fail |
| 1.3.1 / 1.3.2 | A | Full narrative in meaningful DOM order; sticky positioning must not alter source order |
| 2.1.1 Keyboard | A | Every filter, popover and control without pointer timing |
| 2.4.3 / 2.4.7 / 2.4.11 | A/AA | Focus order, visible focus, focus not obscured by sticky chrome |
| 1.4.1 / 1.4.3 / 1.4.11 | A/AA | Never encode category, direction or certainty by colour alone |
| 1.4.10 Reflow | AA | No two-dimensional scrolling at 400% zoom except for genuinely 2D data |

**A pause control that appears only on hover fails.** Users who navigate
by voice or cannot aim precisely may never trigger it. Controls are
persistently visible or announced.

**Reduced-first, not motion-first.** Static baseline; motion added only
under `@media (prefers-reduced-motion: no-preference)`. This **fails
safe** — a browser without support ignores the block and keeps the static
baseline. Motion-first fails open.

The reduced branch is a first-class narrative mode, not every duration
set to zero after authoring. Replace parallax with fixed positioning,
camera travel with cuts or annotated stills, scrubbed morphs with
discrete states, large zooms with opacity, ambient loops with static
composition. **Every fact survives.**

**Canvas and 3D** need a short description plus a structured long
description or data table; structured data stays structured rather than
being compressed into `aria-describedby`. Decorative canvas is
`aria-hidden`.

**Do not fire `aria-live` per scroll state.** Stable prose carries the
narrative; live regions are for deliberate control actions whose results
would otherwise be unavailable.

**Charts**: short alt naming chart type and the primary conclusion, plus
a structured table. Redundant encoding (colour *and* line style) with
keyboard-navigable legend items serves everyone without a separate
stripped-down "accessible version".

> **One number to handle carefully.** "Vestibular disorders affect ~35%
> of adults over 40" is real but routinely misstated. It is Agrawal et
> al. 2009 (NHANES 2001–2004, Arch Intern Med 169(10):938–944), and it
> measured **failure of a standing-balance screening test** among **US**
> adults 40+, with **falls** as the outcome — not diagnosed vestibular
> disorders, not a global rate, and nothing about sensitivity to screen
> motion. Either state it with the measurement named, or drop it: the
> WCAG case (2.2.2 Level A, 2.3.1, 1.4.13, 2.3.3, SCR40) is stronger
> because it has no soft spot. See `evidence.md` §8 for why this file
> previously said the figure had no source at all.

---

## 6. Performance floor

Externally fixed. LCP **≤2.5s** · INP **≤200ms** · CLS **≤0.1**, at the
75th percentile of CrUX field data over a rolling 28-day window, per
device class. **All three must pass** — two of three is a fail.

- Frame budget 16.7ms at 60fps; roughly 10ms remains after the browser's
  own rendering work.
- Any main-thread task over 50ms is formally a long task.
- INP replaced FID on 12 March 2024 and reports the **worst** interaction
  of the visit, so a report's last scroll state is as load-bearing as its
  first. INP does not measure scrolling directly, but animation work
  occupying the main thread delays the next tap.

**Self-contained means one semantic document, and aim for zero network
requests.** Inline the critical CSS, the data, the static fallbacks and
the brand marks. Do not base64 heavy video, textures or image sequences —
the Washington Post's eclipse scroller carried **30MB+** of images before
adopting lazy loading and sub-10KB thumbnails.

**Typography is where self-containment usually leaks.** A blind judge
preferred a rival page partly because it made **zero** network requests
where this skill's page pulled four families from Google Fonts. A webfont
is a live CDN dependency on a page meant to outlast the CDN, plus a
render-blocking request against LCP. Prefer a well-chosen system stack,
or subset and inline the one face that carries the page's identity. If a
hosted webfont is genuinely the right call, say so in the methods note
and accept that the page is no longer self-contained.

GSAP and three.js are the deliberate CDN exceptions, because the house
rule requires GSAP and the alternative is inlining ~50KB of library into
every page.

No universal JS-kilobyte, trigger-count, polygon or texture budget is
sourced. Derive from a device matrix.

---

## 7. Chart integrity

Validated at generation time, because readers cannot catch these:
Pandey et al. (n=330) found deceptive charts produced interpretations
**58.5%–129.5% larger** than controls, and an inverted axis made
**97.5% respond incorrectly**. Okan et al. across five studies found
83.5% showed a truncation effect and **instruction did not eliminate
it**. Chart familiarity, visual ability and education showed no
protective correlation — reader sophistication is not a mitigation.

Check every chart for: baseline at zero for bar length encodings, or an
explicit break; honest aspect ratio; area encoding area rather than
radius; consistent intervals; named units; a legend or direct labels;
uncertainty shown where it exists; and no dual axes implying correlation.

Give every visual an **editorial title** stating its conclusion, not a
descriptive label. Borkin et al. (393 visualisations, eye-tracking on 33
participants): titles and supporting text materially drove recognition
and recall, and recognisable objects appeared in 74% of the most
memorable third against 8% of the least.

---

## 8. Mobile

- Size steps in **`px` computed from `window.innerHeight`**, never `vh` —
  mobile browser bars appear and disappear during scroll, changing
  viewport height and making triggers jump. Newsday documented text
  being clipped by exactly this.
- Pin with CSS `position: sticky`, not JS.
- **No steppers, no swipe-to-advance** — they override native behaviour.
- **No hover-only content.** Stray taps during scroll fire accidental
  triggers, and touch has no hover.
- **Stack instead of scroll** when transitions carry no meaning, when
  steps read fine standalone, or when mobile needs a different chart
  type. The test for keeping it scrolly is whether the transitions are
  genuinely meaningful — change over time and spatial movement qualify.
- Expect to redesign the graphic two or three times to work on both
  desktop and mobile. That is the documented cost, not a failure.

---

## 9. The divider gutter

A vertical rule is drawn in a gap, never beside words. Keep **24px**
between the rule and the nearest text at 900px and wider, **16px** below
that, applied on *both* sides of the rule.

The measurement runs from the text's **ink** to the line, and that
distinction is the whole rule rather than a refinement of it. The gutter
is normally declared on one element and the rule painted on another, so a
cell with `padding-left: 24px` carrying its own `border-left` satisfies
any element-box check by construction — while what a reader sees is the
distance from the glyphs, after the cell's inner wrapper margins and the
*neighbouring* cell's `padding-right`, which is frequently a different
number. The declared gutter and the perceived gutter are two
measurements, and only one of them is on screen.

This is not hypothetical here. `design-review`'s `probeDividerProximity`
run against a page already published from this skill returned **twenty
below-floor violations** — one stat cell measuring 14.3px from its rule
with `padding-right: 0` (the gap came from somewhere nobody had decided),
another at 14.5px where the declared padding was 14px and simply below
the floor.

Three consequences for the markup:

- **Put the rule and both paddings on the same element**, so the two
  numbers sit where they can be read at once. Drop the rule on the first
  child, not its padding, so every cell's text stays on one rail.
- **`min-width: 0` on grid children.** A grid child's implicit minimum is
  `min-content`, so one long unbroken figure widens the track and walks
  the row past its container instead of wrapping — which is the
  clipped-last-cell defect, and a one-property fix.
- **Nothing in a divided row may clip.** A row that runs out of width
  wraps or stacks; it never cuts a cell's final words.

`design-review` measures the rendered ink and is the real gate;
`scripts/audit_page.py` catches the cheap source-level form — a rule
declared with no gutter on that side at all.

---

## 10. Light and dark

Both ship, and both are measured.

- **Light is defined unconditionally on bare `:root`.** Dark only ever
  overrides. A token whose only definition sits inside a dark block is
  undefined wherever that branch does not apply, and the failure renders
  as ink on ink.
- **Dark is written twice** — once under `prefers-color-scheme: dark`,
  guarded as `:root:not([data-theme="light"])` so an explicit light
  choice wins, and once under `:root[data-theme="dark"]` so the control
  wins in the other direction.
- **`body` carries an explicit token background.** A transparent body
  borrows whatever is behind it.
- **The theme control is script-created.** With JavaScript off the page
  already follows the OS preference, so a dead button would be worse than
  none — unlike the *reading* control, which is content and works
  unaided. Three states, so "auto" stays reachable after a manual choice.

**Measured, not authored.** Contrast, focus visibility and divider
gutters are checked in each theme at Phase 9. A dark palette assembled by
inverting a light one passes by luck if it passes at all, and the theme
nobody measured is the theme that ships broken. That is six review passes
on a page with three readings, and they are cheap next to publishing a
surface whose dark mode nobody opened.

---

## 11. The reading surface

A report page is a **Read** surface: the visitor is here to understand
something, so comprehension and wayfinding outrank expression, and the
craft goes into making the reading worth staying in. That single
classification decides most of what follows, and it is the one this file
previously left implicit — which is how a page ends up with a beautiful
hero and an unreadable 96-character measure.

Route the layout through `design-craft` with `ux-craft`'s lens on flow and
states. State the mode once in the direction record and let it bind.

### Measure, scale and rhythm

- **45–75 characters per line** for body prose, and check it in the widest
  viewport rather than the design one. A full-bleed 1440px column is the
  most common way an evidence page becomes unreadable while looking
  expensive. Data, tables and code run wider; prose does not.
- **Leading 1.5–1.6** on body text at this length, tightening as the
  measure narrows. Body at **17–19px**, not 16, because the page is asking
  for sustained attention rather than a scan.
- **Hierarchy from size and space, not from stacking styles.** Roughly 20%
  between levels, with spatial separation doing the rest — measured far
  stronger as a hierarchy cue than weight or case.
- **A real spacing scale, stated as numbers**, and everything on it.
  Twenty sections of ad-hoc spacing is not a design; inconsistent alignment
  measurably costs reading speed where a consistent grid buys up to 22%.
- **Left-aligned, ragged right.** Justified prose opens rivers that disrupt
  tracking; centred body text costs up to 30% reading time because the
  return sweep has no fixed anchor.
- **Sentence-case headings**, bold for one or two phrases per paragraph as
  scanning anchors, italics only for genuine editorial convention, and no
  all-caps on anything multi-line — it destroys word shape and forces
  letter-by-letter decoding.
- **Display type is tracked** at −0.02 to −0.03em above 48px, with a hard
  floor of −0.04em, and all-caps labels at +0.06 to +0.1em. Untracked caps
  and untracked display are the two most reliable machine-made tells.
- **Avoid the convergent defaults** — Inter, Roboto, Arial, Space Grotesk,
  and the purple-gradient-on-white register. Distinctiveness lives in the
  choice of faces and the composition, never in decorating body text; and
  cartoon styling and hand-drawn faces measurably *reduce* perceived
  credibility, so distinctive is not the same as arbitrary.

### Wayfinding — the three questions, answered continuously

A reader landing mid-page from a shared link, or returning after a day,
has to be able to answer *where am I, what can I do here, what happens
next* without scrolling to find out. On a long single-page argument with
three registers, that means:

- **The active register is visible at all times**, not only inside the
  control. A reader who cannot tell which of three readings they are in
  cannot trust anything they are reading.
- **Section position is legible** — a progress indicator, a sticky
  section label, or numbered sections. Pick one; three is chrome.
- **Every heading is a claim rather than a label.** "The reach of the two
  calls is not the same" is something a reader can disagree with;
  "Process topology and the extension contract" is a filing label. A page
  whose headings are all noun phrases has a table of contents where its
  argument should be — and it fails wayfinding too, because a label does
  not tell a scanning reader whether to stop.
- **Deep links land where they say.** Every section and every registry
  entry has a stable id, and `scroll-margin-top` clears the sticky
  masthead so an anchored heading is not hidden under it.
- **Persistent chrome reserves its own space.** A sticky masthead or a
  floating control that overlaps the text is occlusion even when it
  happens to miss the last line, and it will cover whatever the next
  revision puts there. Reserve the band in the layout and size the content
  against the reduced box.

### The controls are content, and they have states

The reading toggle is the page's primary control, so it takes the
treatment a primary control gets: a real `<label>`-wrapped radio group
that works with script off, a visible selected state, a visible focus
ring, keyboard operation by arrow keys as a radio group already gives,
and hit targets at **44×44px** as the craft floor (24×24 is the WCAG 2.2
AA minimum, and it is a floor rather than a target).

The theme control is script-created on purpose — with JavaScript off the
page already follows the OS preference, so a dead button would be worse
than none. Three states, so "auto" stays reachable after a manual choice.

**Design the states rather than reading a rule about them.** Fill the grid
before building: rows for the reading control, the theme control, a
citation marker, a figure, an interactive figure, the source registry;
columns for default, hover, focus, active, selected, and — where the
element loads anything — loading and error. Every cell carries its real
treatment or `n/a` with a reason. A categorical instruction ("all states
designed") ships as one state; a grid with cells in it does not.

### What a Read surface does not need

Skip the component-density rules that belong to product UI, and resist
three habits that arrive with them: a dashboard-style KPI strip where a
sentence and one number would do, cards around prose that was already
readable, and an orchestrated entrance on a page a reader may open from a
search result to check one fact. The page's job is to be read.
