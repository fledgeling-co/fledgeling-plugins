# Charts on slides — the point, and the honesty gate

A chart on a slide is read at distance, for a few seconds, by someone who cannot
zoom or scroll back. That makes two things sharper than they are on a web page:
the chart must show **one point**, and it must not overstate that point. The
second is not a taste rule. On a results slide, a board pack, a health surface
or anything priced off, an overstated chart is a compliance exposure, and
polish makes it worse — fluency reads as credibility, so a beautifully drawn
misleading chart is more dangerous than an ugly one.

Read this before authoring the first chart on any deck that carries figures.

## 1. Length is the encoding

**Bar and column charts start at zero.** Bar length is the whole message; a
truncated axis makes a small change look like a large one, and nothing on the
slide tells the reader it happened. Line charts may zoom the y-range to show
variation — label the range when you do, and don't dramatise noise.

The failure has a measured signature, and it is worth knowing what it looks
like because it is invisible to every other check. A real quarterly deck drew
net debt of $37.8m / $38.9m / $36.6m as bars of 51 / 57 / 43 px. Ratio of
length to value: 1.35, 1.47, 1.18 — not constant, so not zero-based. Solving
`len = k(value − base)` gives a baseline of **30.2**. A 5.9% reduction was
drawn as a 24.6% drop in bar height: a **4.2× exaggeration** of the deck's own
headline claim. The same deck's hire-rate chart exaggerated 6.4% as 29.8%. Both
slides passed every layout, overflow, contrast and type check that ran on them,
and the deck's own validation report scored that slide as fixed and verified.

The test is arithmetic and takes no judgment:

```
Within one bar group, len / value must be constant.
Where it is not, the implied baseline is:
    base = (len₁ · value₂ − len₂ · value₁) / (len₁ − len₂)
```

`scripts/deck-preflight.js` runs it. Two other honesty rules travel with it:
no dual y-axes used to imply correlation (small multiples or an indexed series
instead), and aspect ratio chosen so the average slope sits near 45° — a tall
narrow line chart manufactures drama from the same numbers.

## 2. Declare the chart, so the check is exact

Mark the group and its bars. It costs two attributes, makes the deck
self-documenting, and turns the axis check from a heuristic into a
measurement:

```html
<div class="plot" data-chart="bars"
     role="img" aria-label="Net debt: December 2025 $37.8m, March 2026 $38.9m,
                            June 2026 $36.6m. The axis begins at zero.">
  <div class="col"><span class="v">37.8</span><span class="b" data-value="37.8" style="height:84.0%"></span></div>
  <div class="col"><span class="v">38.9</span><span class="b" data-value="38.9" style="height:86.4%"></span></div>
  <div class="col"><span class="v">36.6</span><span class="b" data-value="36.6" style="height:81.3%"></span></div>
</div>
<p class="note">Axis begins at zero. Cash balance of $13.6m at 30 June 2026.</p>
```

Check it by hand in one line: 84.0/37.8 = 2.222, 86.4/38.9 = 2.221,
81.3/36.6 = 2.221. Constant, so zero-based.

**Write the declared percentage, and let the gate read it rather than the
rendered box.** Rendering engines diverge on percentage heights inside flex and
absolutely-positioned plots — Obscura resolves `height:84.0%` and
`height:86.4%` to the same computed px and returns a bounding rect matching
neither, which turns an honest chart into a false axis-truncation finding. A
declared value is exact, engine-independent, and is the number the author
actually wrote. When a capture accuses a chart you believe is honest, check the
declared geometry before changing anything: suspect the engine before the page.

## 2.1 Pure Deterministic SVG Charts (Banned: External JS/Canvas Libraries)

**Never use external JS chart libraries (like Chart.js) for presentation decks.**
In local file runs, headless browser reviews, and offline presentation laptops, CDN scripts fail silently or delay, rendering blank canvas cards. Pure inline SVG charts are deterministic, zero-dependency, and instantly responsive.

### Pattern A: Deterministic SVG Bar Chart
```html
<svg viewBox="0 0 300 160" style="width: 100%; height: 160px; overflow: visible;" role="img" aria-label="Net debt bar chart">
  <!-- Dashed Grid Lines -->
  <line x1="40" y1="20" x2="290" y2="20" stroke="#E2DFDD" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="40" y1="60" x2="290" y2="60" stroke="#E2DFDD" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="40" y1="100" x2="290" y2="100" stroke="#E2DFDD" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="40" y1="130" x2="290" y2="130" stroke="#C4C0BE" stroke-width="1.5" />
  
  <!-- Y-Axis Labels -->
  <text x="32" y="24" font-family="'IBM Plex Mono', monospace" font-size="10" fill="#6E6968" text-anchor="end">$40m</text>
  <text x="32" y="64" font-family="'IBM Plex Mono', monospace" font-size="10" fill="#6E6968" text-anchor="end">$38m</text>
  <text x="32" y="104" font-family="'IBM Plex Mono', monospace" font-size="10" fill="#6E6968" text-anchor="end">$36m</text>

  <!-- Bars (with rx rounded tops) -->
  <rect x="70" y="64" width="42" height="66" rx="5" fill="#6E6968" />
  <text x="91" y="56" font-family="'IBM Plex Mono', monospace" font-weight="700" font-size="11" fill="#1C1B1B" text-anchor="middle">$37.8m</text>
  <text x="91" y="146" font-family="'Figtree', sans-serif" font-weight="600" font-size="11" fill="#6E6968" text-anchor="middle">Q2 FY26</text>

  <rect x="145" y="42" width="42" height="88" rx="5" fill="#A8A29E" />
  <text x="166" y="34" font-family="'IBM Plex Mono', monospace" font-weight="700" font-size="11" fill="#1C1B1B" text-anchor="middle">$38.9m</text>
  <text x="166" y="146" font-family="'Figtree', sans-serif" font-weight="600" font-size="11" fill="#6E6968" text-anchor="middle">Q3 FY26</text>

  <!-- Focal Accent Bar -->
  <rect x="220" y="88" width="42" height="42" rx="5" fill="var(--color-primary, #D72229)" />
  <text x="241" y="80" font-family="'IBM Plex Mono', monospace" font-weight="700" font-size="11" fill="var(--color-primary, #D72229)" text-anchor="middle">$36.6m</text>
  <text x="241" y="146" font-family="'Figtree', sans-serif" font-weight="700" font-size="11" fill="#1C1B1B" text-anchor="middle">Q4 FY26</text>
</svg>
```

### Pattern B: Deterministic SVG Line / Area Trend Chart
```html
<svg viewBox="0 0 300 160" style="width: 100%; height: 160px; overflow: visible;" role="img" aria-label="Daily hire rate trend">
  <!-- Grid -->
  <line x1="40" y1="20" x2="290" y2="20" stroke="#E2DFDD" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="40" y1="60" x2="290" y2="60" stroke="#E2DFDD" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="40" y1="100" x2="290" y2="100" stroke="#E2DFDD" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="40" y1="130" x2="290" y2="130" stroke="#C4C0BE" stroke-width="1.5" />

  <!-- Semi-transparent Area Fill & Line Path -->
  <polygon points="91,100 166,44 241,32 241,130 91,130" fill="rgba(215, 34, 41, 0.08)" />
  <polyline points="91,100 166,44 241,32" fill="none" stroke="var(--color-primary, #D72229)" stroke-width="3" stroke-linecap="round" />

  <!-- Nodes and Direct Tabular Labels -->
  <circle cx="91" cy="100" r="5" fill="var(--color-primary, #D72229)" stroke="#fff" stroke-width="2" />
  <text x="91" y="88" font-family="'IBM Plex Mono', monospace" font-weight="700" font-size="11" fill="#1C1B1B" text-anchor="middle">$76.2k</text>

  <circle cx="166" cy="44" r="5" fill="var(--color-primary, #D72229)" stroke="#fff" stroke-width="2" />
  <text x="166" y="32" font-family="'IBM Plex Mono', monospace" font-weight="700" font-size="11" fill="#1C1B1B" text-anchor="middle">$80.7k</text>

  <circle cx="241" cy="32" r="6" fill="var(--color-primary, #D72229)" stroke="#fff" stroke-width="2" />
  <text x="241" y="20" font-family="'IBM Plex Mono', monospace" font-weight="700" font-size="11" fill="var(--color-primary, #D72229)" text-anchor="middle">$81.4k</text>
</svg>
```

### Pattern C: Shared-Scale Horizontal Comparison Bars (ROI / Cost vs Benefit)
When comparing a one-off cost against ongoing savings (e.g. $0.4m restructuring cost vs ~$8.0m annualised benefit), draw both bars on a **shared scale from zero**. The visual disparity instantly demonstrates the return:
```html
<div class="hbars" role="img" aria-label="Restructuring cost of $0.4m against targeted benefit of ~$8.0m on a shared scale from zero.">
  <div class="hbar">
    <p class="lab"><span>Restructuring cost incurred</span></p>
    <div class="track"><span class="fill" style="width: 5%"></span><span class="v">$0.4m</span></div>
  </div>
  <div class="hbar key">
    <p class="lab"><span>Targeted annualised pre-tax cash benefit</span></p>
    <div class="track"><span class="fill" style="width: 100%"></span><span class="v">~$8.0m</span></div>
  </div>
</div>
```

### Pattern D: Tabular Progress Completion Bars
Inside project execution or equipment build tables, pair numeric percentage labels with visual horizontal progress tracks:
```html
<div class="barcell" style="display: flex; align-items: center; gap: 16px;">
  <div class="bar" style="width: 200px; height: 10px; background: var(--surface-sunken); border-radius: 9999px; overflow: hidden; position: relative;">
    <span style="position: absolute; inset: 0 auto 0 0; width: 75%; background: var(--ink); border-radius: 9999px;"></span>
  </div>
  <span class="d" style="font-family: var(--font-mono); font-weight: 500;">~75%</span>
</div>
```

## 3. Cut to the point

- **Every series and column that doesn't support the slide's one idea comes
  out.** A chart nobody can read at distance is decoration with error bars.
- **Direct-label the bars** rather than shipping a legend the audience must
  hunt through. A legend costs a saccade per lookup and the speaker has already
  moved on.
- **Value labels sit with their bars**, close enough to read as one object.
  Labels floating over gridlines belong to nothing.
- **Type in the chart obeys the deck's scale.** Axis and value labels are
  slide type, not chart-library type: on a 1920 canvas that is ≥24px, and an
  axis label must never be the largest text in the panel — that inverts the
  hierarchy and makes the category outrank the number.
- **Tabular figures** (`font-feature-settings: "tnum"`) for anything compared
  column to column, so digits line up and the eye can scan.

## 4. Colour carries meaning, once

One bar is the point; the rest are context. Give the focal bar the accent and
leave the others neutral — that is the whole encoding, and it does the job a
legend would otherwise do.

**Never let colour be the only signal.** Red-vs-green for
behind-vs-ahead fails for roughly 8% of men, and on a projector at the back of
a room it fails for everyone. Pair colour with position, a label, a shape or a
value. A status column that reads correctly in greyscale reads correctly
everywhere.

Watch the accent budget specifically here: a chart panel is where an accent
quietly gets spent four times — the focal bar, the headline figure, a status
pill and a trend arrow. Pick one.

## 5. Say what the chart says

Every chart carries a text alternative stating the **message**, not the
encoding: "Net debt fell to $36.6m, down $2.3m on the prior quarter, on an axis
beginning at zero" — never "a column chart of net debt". Put it in
`aria-label` or a visually-hidden caption. It is the accessibility floor, and
it doubles as the test of whether the chart has a point: a chart whose message
you cannot write in one sentence is a chart that hasn't decided what it is for.

## 6. Provenance travels with the figure

On any deck a reader will act on, **where a number came from is part of the
number.** A figure with no stated provenance is not neutral — it reads as
authoritative, because that is the default a reader applies. Three states, and
the third is the one decks skip:

| State | What the slide shows |
|---|---|
| From the record | the value, its as-at date, and the source document |
| Illustrative | the value, visibly marked, with what it stands in for |
| Not available | "not available" — never a placeholder, a zero, or a last-known value |

Precision is itself a claim: if the source publishes month-and-year, show
month-and-year. Inventing a day to tidy a timeline fabricates specificity the
record does not support.

For a regulated deck, four things belong somewhere in it and their absence is
a defect rather than an omission — an audit qualifier ("unaudited · not subject
to external audit or review"), the as-at date, the axis disclosure on any
chart, and a marker on illustrative or generated material including
photography. `run-preflight.sh --regulated` checks that all four are present
somewhere in the deck. It cannot check that they are *correct*, or that they
sit near the figures they qualify — that is yours to look at.

## 7. States, when the chart is live

A static chart drawn from figures in the file needs no states. A chart bound to
a live source is an async component and needs the same five as any other:
loading (a skeleton in the chart's own shape, not a spinner in a void), empty
(a designed message with a next action), error (what failed, and retry),
sparse (one or two points get a stat tile, not a line pretending to be a
trend), and populated.

## The gate

Before the slide is done:

1. Bar group zero-based — ratio constant, or the range labelled and the reason
   stated.
2. Every value traces to the source material.
3. The chart's message written in one sentence, and present as a text
   alternative.
4. One accent, and no colour-only distinction.
5. Chart type on the deck's scale, axis labels not outranking the values.
6. Provenance: as-at date, and a marker on anything illustrative.
