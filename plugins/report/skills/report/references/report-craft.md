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
  regardless of the screen theme.
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

**The stack**, cheapest first:

| Tier | Use for | Why |
|---|---|---|
| CSS `animation-timeline: scroll()` / `view()` | Entrance reveals, progress, sticky states | Runs off the main thread. Guard with `@supports`; not Baseline, so never the only carrier of meaning |
| IntersectionObserver | Discrete state changes | Low cost, universal |
| GSAP ScrollTrigger | Scrub and pinning CSS cannot express | The technique with the strongest comprehension evidence behind it |

GSAP is not mandatory here — unlike a published page, a report's job is
to be read and printed, and most reports have no scrubbed moment. Load it
when an argument genuinely has one, and say in the methods note when it
does not, rather than reaching for it by default.

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
