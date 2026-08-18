# Report craft — the buildable rules

Every rule here traces to `evidence.md`. Where the evidence is contested
or absent this file says so, because a number nobody can source is a
number nobody should tune against.

## Contents

1. [The page-safe block](#1-the-page-safe-block)
2. [Print and PDF](#2-print-and-pdf)
3. [Narrative structure](#3-narrative-structure)
4. [The motion budget](#4-the-motion-budget)
5. [Citations](#5-citations)
6. [Charts](#6-charts)
7. [Typography](#7-typography)
8. [Accessibility](#8-accessibility)
9. [Self-containment](#9-self-containment)

---

## 1. The page-safe block

The report is one HTML source with two renderings. On screen it is a
continuous document; in print each block maps onto A4. That constraint
decides the markup, so build for it from the first line rather than
retrofitting a print stylesheet at the end.

```html
<section class="block" id="b3" data-claims="c7 c9">
  <h2>…</h2>
  <figure class="fig">…<figcaption>…</figcaption></figure>
  <p>…</p>
</section>
```

Rules that make a block page-safe:

- **A block may break at its boundary and nowhere else.**
  `break-inside: avoid` on figures, tables and caption groups; the block
  itself may break between its children if it is long.
- **A figure and its caption never separate.** They are one
  `<figure>`, and the figure carries `break-inside: avoid`.
- **Nothing is positioned by viewport units.** `vh` is unreliable on
  mobile (browser chrome changes the viewport mid-scroll, which has
  clipped text on real newsroom pages) and meaningless in print. Size
  from content, or in `px` computed from `window.innerHeight` where a
  screen-only step genuinely needs it.
- **No block depends on a sticky or pinned ancestor for its meaning.**
  Sticky positioning is a screen affordance; the printer flattens it.
- **Headings carry `break-after: avoid`** so a heading never lands alone
  at the foot of a sheet.

### The divider gutter

A vertical rule is drawn in a gap, never beside words. Keep **24px** between the
rule and the nearest text at 900px and wider, **16px** below that, applied on
*both* sides of the rule.

The measurement runs from the text's **ink** to the line, and that distinction
is the whole rule rather than a pedantic refinement of it. The gutter is
normally declared on one element and the rule painted on another, so a cell with
`padding-left: 24px` carrying its own `border-left` satisfies any element-box
check by construction — while what the reader sees is the distance from the
glyphs, after the cell's inner wrapper margins and the *neighbouring* cell's
`padding-right`, which is frequently a different number. The declared gutter and
the perceived gutter are two measurements and only one of them is on screen.

Three consequences for the markup:

- **Put the rule and both paddings on the same element.** `.divided > *` with a
  `border-left` and matching `padding-left`/`padding-right` keeps the two numbers
  together where they can be read at once. Drop the rule on the first child, not
  its padding, so every cell's text stays on one rail.
- **`min-width: 0` on grid children.** A grid child's implicit minimum is
  `min-content`, so one long unbroken figure widens the track and walks the row
  past its container instead of wrapping — which is the clipped-last-cell defect,
  and a one-property fix.
- **Nothing in a divided row may clip.** A row that runs out of width wraps or
  stacks; it never cuts a cell's final words.

`design-review`'s `probeDividerProximity` measures the rendered ink and is the
real gate; `scripts/audit_report.py` catches the cheap source-level form — a
rule declared with no gutter on that side at all. Run against an
already-published page in this portfolio, the ink measurement returned **twenty
below-floor violations**, several of them on cells whose declared padding was
doing exactly what it said.

### Blocks that move

A scrubbed or pinned episode has no print equivalent — the printer gets
one frame, and by default it is whatever frame the animation happened to
be sitting in. So a moving block ships an **authored static frame**: the
composition that carries the claim without the motion, chosen
deliberately.

```html
<section class="block" id="b6" data-claims="c14">
  <div class="episode" aria-hidden="false">…animated…</div>
  <figure class="episode-static">…the frame that carries the claim…</figure>
</section>
```

```css
.episode-static { display: none; }
@media print, (prefers-reduced-motion: reduce) {
  .episode { display: none; }
  .episode-static { display: block; }
}
```

The static frame doubles as the reduced-motion branch, which is why it is
cheap: one artifact serving print, reduced motion, and any browser that
does not run the animation.

---

## 2. Print and PDF

Luke's standing instruction, from a session where it was missed:
*micro-interactions and animations that don't show when exporting as
PDF.* Motion is a screen affordance; ink is permanent.

```css
@page { size: A4 portrait; margin: 16mm 15mm 18mm; }

@media print {
  html, body { background: #fff; color: #111; }
  .block { break-inside: auto; }
  .fig, figure, table, .kpi-row, .callout { break-inside: avoid; }
  h1, h2, h3 { break-after: avoid; }
  .nav, .toc-float, .theme-toggle, .scroll-hint { display: none; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 9pt; }
  .cite::after { content: none; }
}
```

Points that repay attention:

- **Print the URL after external links.** Paper has no hyperlinks. Do
  this for the registry's links, not for every inline citation marker —
  markers already carry a number that resolves in the registry.
- **Running headers are pagination artifacts.** Keep them light and out
  of the way, suppress them on the cover block, and note that WCAG PDF14
  asks for them to be marked as artifacts so screen readers skip them.
- **The PDF is the light rendering.** A dark report on paper is a
  different document and an expensive one. Force light in `@media print`
  regardless of the screen theme — and force it by **re-declaring the
  tokens**, not just `body`'s colours. Every `var(--ink)`, `var(--rule)`
  and `var(--panel)` is still holding its dark-scheme value when the print
  rules land, so a reader in dark mode prints dark values onto white.
  Repeat the `[data-theme="dark"]` selector inside the print block too: it
  beats bare `:root` on specificity and would otherwise survive into the
  ink.
- **Light is defined unconditionally; dark only ever overrides.** A token
  whose only definition sits inside a dark block is *undefined* in print,
  which renders as ink on ink in the one artifact nobody previews before
  sending. `audit_report.py` fails on it, because reading the CSS will not
  catch it.
- **Colour is never the only encoding**, which matters more in print
  because a reader may have printed it in greyscale.

`scripts/export_pdf.mjs` prints with `preferCSSPageSize` so `@page`
governs, then checks the file it produced: page count against block
count, A4 geometry, surviving link annotations, and no transient
animation label frozen into the ink. Checking the artifact rather than
the exit code is the point — a PDF that wrote successfully and paginated
wrongly is the normal failure, not a rare one.

---

## 3. Narrative structure

**Lead with the conclusion.** Instrumentation across large samples: about
38% of arrivals leave immediately, median scroll depth is roughly 50–60%,
only a quarter pass the 1,600th pixel of a 2,000-pixel article, and
scroll depth correlates only weakly with sharing. The finding belongs
above the fold and on page one.

**Martini glass.** An authored stem that establishes the claim, then
opening to detail, sources and drill-down. Free exploration is never the
sole delivery mode — introductory stories measurably do *not* increase
later exploration.

### The TLDR section — required on every report

Leading with the conclusion is a principle, and principles get
interpreted. The section is the enforceable form, and **every report ships
one** as the first content block, in every register.

It is a named `<section id="tldr">`, not a hero with a slogan in it, and it
holds:

1. **The finding, in one sentence**, cited. The sentence a reader would
   repeat to someone else.
2. **The ask** — the cheapest high-payoff action, sized, with a named
   decision. On a comparison report this is the overall winner
   (`product-verdicts.md`), so the two are one artifact rather than two
   summaries competing at the top of the page.
3. **Three to five cited claims** carrying the argument — the ones a
   sceptic needs before believing the finding, not the ones that were
   easiest to establish.
4. **The one thing that would change it** — the limit, the untested case,
   the disagreement. A TLDR that reads as settled has hidden the report's
   own uncertainty in the place a reader is most likely to stop.

Four rules keep it honest:

- **It is a derivation, not a summary written separately.** Every line
  traces to a ledger row that also appears further down, and to the same
  row the one-pager uses. Two documents disagreeing about the finding is
  the failure mode here, and generating both from one ledger prevents it.
- **Every claim in it carries its marker, in every register.** It is the
  most-read and most-quoted block, so it is the last place an uncited
  number may sit.
- **Its arithmetic is recomputed before shipping**, in each register. A
  judge recomputed a rival report's opening bullet inside the sixty seconds
  it was built for and found two of its figures wrong; on a report whose
  thesis is that nobody was checking, that is the cheapest possible way to
  lose the reader.
- **It fits on page one with room left**, because the ask sits at the end
  of the scrolling report and the reader who stops at the fold still has to
  leave with the conclusion. If the section fills a sheet on its own, it is
  a section rather than a summary.

**One claim per block.** Each block carries one `claim_id`; its caption
states that claim in a sentence; the visual delta changes only the
encodings supporting it. If a caption contains two independent
propositions, split the block.

**Parallelism aids memory.** Repeated structural relationships between
adjacent blocks let readers compare. Keep scales, positions and object
identity stable unless the change *is* the evidence.

> "One claim per block" is a production discipline, not a measured law.
> Keep the rule; do not cite a study for it.

**No universal length exists.** Words per block, block count and figure
density are unsourced. Derive from the argument. What is sourced is that
padding costs readers — so a report that has said its piece stops.

---

## 4. The motion budget

**Two budgets, and conflating them is why this section used to read as
grudging about motion.** They answer different questions and a report needs
both.

| Budget | Answers | Governed by |
|---|---|---|
| **Evidence motion** | does this movement help the reader *perceive the data* | the test below, and it is strict |
| **Interface feedback** | does the reader know their input registered | the micro-interaction tier, and it is mandatory |

A control that does not acknowledge a press reads as broken; a chart that
animates for delight reads as untrustworthy. The same document owes the
first and must refuse the second — and neither reaches the ink.

### Evidence motion — the test

**The test.** An animation is admissible only when you can finish:

> *"This motion lets the reader perceive ___ that would otherwise
> require a difficult mental comparison."*

If the blank is energy, delight, premium quality or immersion, it is
decoration.

**Where animation measurably helps**: transitions between two states of
*one* encoding reduced tracking error across all tested transition types
(n=24, `p<0.001`); object-tracking around 1.25s, value change around 2s.

**Where it measurably hurts**: animation as a substitute for a static
explanation. Apparent advantages over static graphics turned out to be
confounds — the animated conditions carried more information. After a
week, text-studying participants improved while animation-studying
participants declined. More staging is not better: extreme staging was
*worse* than direct animation for value changes (`p=0.024`).

### Interface feedback — the micro-interaction tier, and it is required

Every interactive element carries **default, hover, `:focus-visible`,
active and disabled**, and every async control carries loading. This is not
decoration and it is not drawn from the evidence budget: it is the answer
to *did that work*. A report whose reading toggle, theme control, citation
markers and disclosures respond to a press with nothing reads as broken
however good its argument is — and unlike the evidence motion, none of this
survives into the ink, so it costs the printed document nothing.

The numbers are tight, because the reader is mid-sentence rather than
watching a show:

- **120–250ms** on a state change, `ease-out` on entry. Under ~100ms reads
  as instant and jarring; past ~400ms reads as laggy. Never
  `transition: all`.
- **The focus ring is never removed without a replacement**, visible in
  both themes — `:focus-visible { outline: 2px solid var(--focus);
  outline-offset: 2px }`.
- **`cursor: pointer` on everything clickable**, including a card or a
  citation marker acting as one.
- **The active reading, the active theme and the reader's position are
  visually distinct**, not merely stored. A reader who cannot see which
  register they are in has lost the control the document is built around.
- **A citation preview appears on hover, focus *and* tap**, is hoverable,
  dismissible and persistent (WCAG 1.4.13), and closes on Escape with focus
  returning to the marker.

Micro-interactions are exempt from the evidence test and bound by
`prefers-reduced-motion` like everything else: under `reduce` a state
change lands instantly rather than not at all. A feedback state that
disappears under reduced motion has removed the feedback, not the motion.

### The stack, and GSAP as the standing layer

**The stack**, cheapest first:

| Tier | Use for | Why |
|---|---|---|
| **Tier 0 — CSS transitions** | every hover, focus, active, disabled and selected state; all of the feedback above | Cheapest possible, no library involved, survives a script failure, absent from print |
| CSS `animation-timeline: scroll()` / `view()` | Entrance reveals, progress, sticky states | Runs off the main thread. Guard with `@supports`; not Baseline, so never the only carrier of meaning |
| IntersectionObserver | Discrete state changes | Low cost, universal |
| GSAP ScrollTrigger | Scrub and pinning CSS cannot express; choreographed sequences needing runtime control | The technique with the strongest comprehension evidence behind it |

Tier 0 stays in CSS even with GSAP loaded. A hover state written as a GSAP
tween is a library call on every pointer move where a declarative
transition would do, and it stops working the moment the script does.

**GSAP is a hard requirement on screen. Every report loads it**, and it owns
the entrance choreography, the reveal sequence as blocks arrive, the
micro-interaction feedback above, any scrubbed or pinned episode the
argument has, and any tween between two compiled figure states.

What makes that safe on a document that prints — and what made this file
previously say "not mandatory" — is the **authored static frame**: every
moving block ships the composition that carries its claim without the
motion, and that one artifact serves print, reduced motion, and any browser
that does not run the animation. With that contract in place, motion costs
the printed document nothing, so the only question left is whether it earns
its place on screen by the test above. Three readings means a static frame
per register wherever the figure differs, not one shared frame that matches
none.

Where an argument genuinely has no scrubbed or pinned moment, say so in the
methods note and spend the layer on the reveal choreography and the feedback
tier rather than reaching for a scrubbed episode to look busy. The layer is
present either way: an earlier version of this file let a report ship
without it, and a page whose controls acknowledge nothing is the result.

**Load it pinned, with SRI.** GSAP's plugins are all free including
commercial use since the Webflow acquisition — no membership, no licence
key, no private registry, so never generate `.npmrc` auth-token
instructions. Pin the version, keep `integrity` and `crossorigin`, and
register plugins once. On a document aiming at zero network requests, GSAP
is a deliberate exception and the alternative is inlining ~70KB into every
report; §9 owns the trade. Where a report genuinely has to be offline-clean,
inline the minified source and say so in the methods note.

**Choreograph with a timeline, not chained delays.** The position parameter
is the craft — `"-=0.35"` to overlap the previous tween's tail, `"<0.15"` to
start just after it began, labels for named beats. Overlapping entrances
read composed; strictly sequential ones read as a slideshow. Use
`autoAlpha` rather than `opacity` so a faded-out element stops eating
clicks, set `gsap.defaults()` once as the motion tokens, and put the
reduced-motion and viewport branches in `gsap.matchMedia()`, which reverts
its own animations when a condition stops matching.

**three.js is gated, and the gate is high.** Six tests, all of which must pass,
run against a *claim id* rather than against the topic:

1. **Spatial claim** — a major claim depends on depth, volume, orientation,
   topology, occlusion, assembly, or movement through physical space.
2. **Viewpoint necessity** — changing viewpoint *reveals evidence*, rather than
   showcasing an object.
3. **2D insufficiency** — a map, cutaway, orthographic diagram, annotated image
   or small multiple cannot communicate the claim at least as clearly.
4. **Narrative mapping** — every camera or object transition maps to a claim id.
   No decorative idle orbit.
5. **Equivalent fallback** — static images, diagrams and text carry the same
   conclusion without WebGL, because device capability cannot be reliably
   feature-detected.
6. **Performance and reduced motion** — meets the CWV budget on the target
   mobile tier, and fully disables non-essential camera motion under
   `prefers-reduced-motion`.

Why the bar is that high: four data stories built in static, animated and
immersive variants found the immersive version rated **more interesting and more
persuasive, and no more understandable or trustworthy**. A scene that raises
persuasiveness without raising understanding is rhetoric charged to the reader's
battery — and on a document whose argument rests on its evidence, that is the
wrong trade. Most reports fail test 3. When 3D is rejected, say so in the
methods note and ship the annotated static graphic; recording the rejection is
what stops the gate decaying into a formality.

If approved: dynamic-import after the content, render on demand rather than in
an unconditional loop, `dispose()` between chapters, cap device pixel ratio,
handle `webglcontextlost`, and keep labels, transcript and sources **outside**
the canvas in normal DOM order.

**Hazards, from GSAP's own docs**, each a build rule: never animate the
pinned element itself; an ancestor with `transform` or `will-change`
breaks `position: fixed`; `content-visibility: auto` breaks trigger
calculation; under `scrub`, child durations are proportions of scroll
distance, so extend `end` rather than lengthening durations; refresh
after fonts and images settle. **`normalizeScroll()` is prohibited** — it
forces scrolling onto the JS thread, which is scrolljacking renamed.

**Never touch native scrolling.** In usability testing a majority of
participants experienced at least mild disorientation, and on a fully
scrolljacked page every participant was disoriented; a controlled study
(n=20) found no speed benefit and significantly lower accuracy and
satisfaction.

**Idempotent states.** Readers skip faster than animations complete, and
the printer runs none of them. Every block renders directly from its own
id.

---

## 5. Citations

**Verification is rare, and that is the design input.** 96 million
Wikipedia citation events over two months: external-reference clicks in
0.29% of page views, and 93% of cited URLs received no click that month.
Clicks were *more* common on shorter, lower-quality pages — readers
verify when the page fails them.

So the citation layer is not built to be clicked. It is built so the
claim-source bond is inspectable and the report cannot quietly overclaim.

**Three layers, all required:**

1. **Inline marker** on the smallest span the source supports.
2. **Preview** on hover, keyboard focus *and* tap: title, locator, what
   this source establishes, and a way to open it. Escape closes, focus
   returns to the marker. Hover content must be hoverable, dismissible
   and persistent (WCAG 1.4.13) — this is the criterion naive tooltips
   fail.
3. **Persistent registry** at the foot: deduplicated, full metadata,
   access date, backlinks to every claim using it.

**The markup contract** the auditor enforces:

```html
<a class="cite" href="#r12" data-cite="r12" data-n="9" aria-describedby="r12">9</a>

<li id="r12">
  <a href="https://…">Title</a>
  <span class="src">Locator · what it establishes · date</span>
</li>
```

`data-cite` is the stable anchor; `data-n` is the number the reader sees.
Separate, so sources can be numbered by first appearance without
renumbering anchors when one is inserted.

**An anchor, never a button.** `<button data-cite>` is inert with
JavaScript disabled, breaking the claim-to-source bond in exactly the
no-JS case the document should survive. The anchor jumps to the registry
unaided; intercept the click and `preventDefault()` only once the preview
has actually rendered.

For internal sources the "open original" affordance is the locator
itself — `lib/ingest/worker.ts:88-104` as text is more useful than a
`file://` link that will not resolve on anyone else's machine.

> Stated honestly: "good citation UX makes readers verify" is unsupported
> in either direction. What is supported is narrower — previews lower
> exploration cost, and multiple co-present transparency signals raise
> perceived credibility more than a single one does.

---

## 6. Charts

Validated at generation, because readers cannot catch these. Deceptive
charts produced interpretations 58.5%–129.5% larger than controls
(n=330), and an inverted axis made 97.5% respond incorrectly. Across five
studies 83.5% showed a truncation effect and **instruction did not
eliminate it** — reader sophistication is not a mitigation.

Check every chart for: zero baseline for bar-length encodings or an
explicit break; honest aspect ratio; area encoding area rather than
radius; consistent intervals; named units; a legend or direct labels;
uncertainty shown where it exists; no dual axes implying correlation.

**Editorial titles, not descriptive labels.** A title stating the
conclusion drives recognition and recall materially more than one naming
the variables. Route form and colour through `dataviz`.

Charts have the same no-JS obligation as citations: ship the static SVG
or the data table in the DOM and let script enhance it, rather than
printing an apology. This is also what makes the chart appear in the PDF.

### Four things a blind panel caught on pages this skill produced

Each was invisible to every automated gate, and each generalises.

**Mark every unmeasured region, not the convenient one.** A chart hatched
the 1,000–3,000 band as never-measured and left an equally untested
3,000–5,000 gap unhatched beside it, so the graphic implied the upper
range was sampled continuously. On a page whose whole argument is
separating known from assumed, the one figure carrying that argument
applied the mark selectively.

**Bound the uncertainty; naming it is not enough.** A report identified
that two counters might overlap, reasoned correctly to the fork, and then
never converted the second branch into a number. A reader sizing a budget
or an SLO got a floor with no ceiling. State the range.

**Say which set contains which.** "18,560 of 300,000 · plus 2,071
overwrites" reads as additive when the overwrites are a subset. Whenever
two figures describe overlapping sets, the containment goes in the label,
because the label is the part that gets quoted.

**SVG annotation type has a floor.** Figures that scale their text with
the artwork drop to ~6px on a 400px viewport, and the mono annotations
carrying the meaning become unreadable while the shapes still look fine.
Either hold the type size independent of the viewBox, re-lay the figure
at narrow widths, or let the table view take over. Check every figure at
400px, not just the page.

**A scale that hides the data is not a finding about the data.** A
latency chart plotted p50, p95 and p99 on a linear axis topping out at
402ms, so six of nine bars rendered under 1% of the scale and were
effectively invisible; the caption defended this as "the point rather
than a rendering problem." It was a rendering problem. A 33× spread
wants a log axis. And an annotation borrowed from a continuous-axis
chart — a hatched "not measured" band — means nothing over three
categories, because there is no interval between them to be unmeasured.

**Front-page arithmetic gets checked, so check it first.** A judge
recomputed a rival's opening bullet inside the sixty seconds the page was
built for and found "9.3×, from 0.66% to 6.88%" (it is 10.4×; 9.3× is the
ratio to a different figure) and "roughly 16% never lands" against the
document's own 85.5% conversion table. Every ratio, percentage and
multiple on the first screen should be recomputed from the ledger's own
numbers before the page ships. On a report whose thesis is that nobody
was checking, this is the cheapest possible way to lose the reader.

---

## 7. Typography

The report is a document before it is a page, so the print research
applies. Hierarchy comes from **size and space**, not from stacking
styles: a card-sorting study found relative size (~20% between levels)
and spatial placement far stronger hierarchy cues than weight or case.

- **Bold** for one or two key phrases per paragraph. It is the least
  destructive emphasis and provides scanning anchors.
- **Italics** only for genuine editorial convention — titles, foreign
  terms. Continuous italic reads ~10% slower, and dyslexic readers show
  significantly longer fixations and strongly dislike it.
- **No all-caps for anything multi-line.** It destroys word shape and
  forces letter-by-letter decoding: 10–20% slower, and older readers were
  29% more likely to misunderstand all-caps contract terms.
- **No underline for emphasis** — it collides with the link convention
  and cuts descenders.
- **Left-aligned, ragged right.** Justified text creates rivers that
  disrupt tracking; centred body text can cost up to 30% reading time
  because the return sweep has no fixed anchor.
- **45–75 characters per line**, leading 1.2–1.5, body 16–18px on
  screen. Contrast 4.5:1 body, 3:1 large.
- **Sentence case headings.**

Against that discipline sits the aesthetic requirement, and they are
compatible: distinctiveness lives in the *choice* of faces, the palette
and the composition, not in decorating the body text. Avoid the
convergent defaults — Inter, Roboto, Arial, and the purple-gradient-on-
white register that reads instantly as machine-made. One counterweight:
cartoon styling and hand-drawn fonts measurably *reduced* perceived
credibility. Distinctive is not the same as arbitrary.

Two numbers the print research adds that a screen-only rule set misses:
**display type is tracked** at −0.02 to −0.03em above 48px with a hard floor
of −0.04em, and all-caps labels at +0.06 to +0.1em. Untracked caps and
untracked display are the two most reliable machine-made tells, and they
survive into the PDF where nothing about the motion does.

### Wayfinding, and the controls as content

A reader opening the file a month later, or landing on a heading from a
search, has to answer *where am I, what can I do here, what happens next*
without scrolling to find out. On a long single document with three
registers:

- **The active register is visible at all times**, not only inside the
  control. A reader who cannot tell which of three readings they are in
  cannot trust what they are reading.
- **Position is legible** — a running header, numbered blocks, or a section
  label. Pick one; three is chrome, and the printer flattens two of them
  anyway.
- **Every heading is a claim rather than a label.** "The reach of the two
  calls is not the same" is something a reader can disagree with; "Process
  topology and the extension contract" is a filing label. A report whose
  headings are all noun phrases has a table of contents where its argument
  should be — and it fails wayfinding too, because a label does not tell a
  scanning reader whether to stop.
- **Deep links land where they say.** Every block and registry entry has a
  stable id, and `scroll-margin-top` clears any sticky chrome so an anchored
  heading is not hidden under it.
- **Persistent chrome reserves its own space.** A floating control that
  overlaps the text is occlusion even when it happens to miss the last
  line, and it will cover whatever the next revision puts there. Reserve
  the band and size the content against the reduced box.

The **reading control** is the document's primary control, so it takes the
treatment one gets: a real `<label>`-wrapped radio group that works with
script off, a visible selected state, a visible focus ring, and hit targets
at **44×44px** as the craft floor — 24×24 is the WCAG 2.2 AA minimum, and it
is a floor rather than a target. The **theme control** is script-created on
purpose, because with JavaScript off the page already follows the OS
preference and a dead button would be worse than none.

**Design the states rather than reading a rule about them.** Fill a grid
before building: rows for the reading control, the theme control, a citation
marker, a figure, an interactive figure and the registry; columns for
default, hover, focus, active, selected, and loading and error wherever the
element fetches anything. Every cell carries its real treatment or `n/a`
with a reason. A categorical instruction — "all states designed" — ships as
one state; a grid with cells in it does not.

---

## 8. Accessibility

| Criterion | Level | Applies to |
|---|---|---|
| 2.2.2 Pause, Stop, Hide | A | Auto-starting motion over 5s alongside other content. A control that appears only on hover fails |
| 1.4.13 Content on Hover or Focus | AA | Citation previews: hoverable, dismissible, persistent |
| 2.3.1 Three Flashes | A | Seizure risk; reduced motion is not a substitute |
| 2.3.3 Animation from Interactions | AAA | Explicitly covers scroll parallax |
| 1.3.1 / 1.3.2 | A | Full narrative in meaningful DOM order |
| 2.1.1 / 2.4.3 / 2.4.7 / 2.4.11 | A/AA | Keyboard, focus order, visible focus, focus not obscured |
| 1.4.1 / 1.4.3 / 1.4.11 | A/AA | Never encode category or certainty by colour alone |
| 1.4.10 Reflow | AA | No 2D scrolling at 400% zoom except for genuinely 2D data |

**Reduced-first, not motion-first.** Static baseline; motion added under
`@media (prefers-reduced-motion: no-preference)`. This fails safe — a
browser without support keeps the static baseline. The reduced branch is
a first-class mode, not every duration set to zero afterwards: parallax
becomes fixed positioning, camera travel becomes annotated stills,
scrubbed morphs become discrete states. Every fact survives.

Charts need short alt naming the chart type and the conclusion, plus a
structured table. Do not fire `aria-live` per scroll state — stable prose
carries the narrative.

---

## 9. Self-containment

One file, aiming at zero network requests. Inline the CSS, the data, the
static fallbacks and the marks.

**Typography is where self-containment usually leaks.** A webfont is a
live CDN dependency on a document meant to outlast the CDN, and a
render-blocking request against LCP. Prefer a well-chosen system stack,
or subset and inline the single face carrying the report's identity. If a
hosted font is genuinely right, say so in the methods note and accept
that the document is no longer self-contained.

Do not base64 heavy video or image sequences — one newsroom scroller
carried 30MB+ of images before adopting thumbnails. Generated imagery
belongs in `assets/` referenced relatively, which keeps the HTML
readable; the PDF embeds it at export.

Performance floor, externally fixed: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 at
the 75th percentile, all three. No universal JS-kilobyte or trigger-count
budget is sourced; derive from the target device rather than copying a
number from an unrelated production.
