# Home battery economics in Australia — visual direction and page structure

Planning only. No research has been run, so **every number in this document is a
placeholder for a shape, not a figure**. The claim graph (Phase 3) gates the
page, and the structure below has slots where claims go, not claims.

---

## 1. What the existing pages have already taken

Phase 5 says read the published pages first and treat their silhouettes as
spent. I read all three.

| | `cold-flu-evidence` | `dossier/undervolt` | `dossier/workflows` |
|---|---|---|---|
| **Register** | Pharmacy shelf-talker / consumer-affairs verdict board | Workshop settings manual for two specific machines | Incident post-mortem |
| **Ground** | Warm newsprint `#F2F1EC` | Dark charcoal `#0E1013` | Cold bone `#EDEEF1` |
| **Accent logic** | Acid lime + alarm red | Bipolar hot `#C7472C` / cool `#3EBBAE` + amber caution | Single marine blue `#2438C8` |
| **Display type** | Archivo Black, huge, stacked, second line offset | IBM Plex Sans, quiet | Bricolage Grotesque |
| **Hero** | Grain canvas + giant two-line headline + **4-up stat numeral band** | Quiet eyebrow / h1 / two ledes, no stats | Eyebrow / h1 / standfirst + **4-up stat numeral band** |
| **Signature device** | Tabbed leaderboard of **ranked horizontal bars on a shared track** | **Sticky segmented switch** setting `body[data-sys]`, whole page follows one of two builds | **Syntax-highlighted code figures** + numeric tables |
| **Chart grammar** | Ranked bars, common track, pip ticks | One hand-authored SVG voltage curve with a shaded wedge; spec tables | Tables and code listings, almost no drawn chart |
| **Motion** | GSAP + ScrollTrigger + SplitText | None | None |

Four things are now **spent** and the new page cannot touch them:

1. **The 4-up stat numeral band directly under the hero.** Two of three pages
   open with it. It is the single strongest sameness signal in the set.
2. **The centered `.wrap` column.** All three are a 1,080–1,180px centered
   single column with occasional 2-col `split` and 3-col grids. Same skeleton,
   three palettes. Re-colouring this would be exactly the failure
   `aesthetic-direction.md` warns about.
3. **Sticky two-state switch reconfiguring the whole page** (undervolt) and
   **tabbed panels** (cold-flu). Both interaction devices are used.
4. **Bricolage Grotesque and Space Mono**, which appear in all three font
   stacks, and IBM Plex / JetBrains / Archivo besides.

Also worth noting: all three are **atemporal**. Nothing published so far has a
time axis. That is the opening.

---

## 2. Slug

| Slug | Reads as | Verdict |
|---|---|---|
| **`payback`** | `payback.fledgeling.app` — the actual question a reader arrives with | **Recommended.** One word, decision-shaped, not product-shaped, and it survives the page being updated when the rebate changes |
| `battery` | Plain and searchable | Generic; says nothing about the argument |
| `kwh` | Short, unit-native | Ambiguous — could be any energy page |

Directory: `~/Dev/dossier/payback/index.html`, plus a row added to
`~/Dev/dossier/home/index.html`.

---

## 3. Three visual directions

### Direction A — "The Load Curve" (recommended)

**Register.** A network operator's dispatch chart printed as a broadsheet. The
page pretends to be the daily load-shape trace that utilities actually publish,
annotated by hand.

**The one visual device — the day strip.** A single page-wide horizontal
24-hour axis, midnight to midnight. Every state of the argument re-renders
*that same strip* with a different band on it: solar generation, household
draw, the export window where a kilowatt-hour is worth almost nothing, the
evening peak where it is worth a lot, and finally the battery's charge and
discharge shading occupying the gap between them.

Why it is subject-native rather than decorative: the entire economic case for a
home battery is arbitrage across the hours of **one day**. The unit of the
argument *is* the day. The device cannot be lifted to another subject — swap
the noun and the strip is meaningless, which is the theme-proof test.

**Skeleton — and this is the part that must not match.** Desktop is a
**two-track layout**: a sticky day strip occupying the upper band of the
viewport, and prose running beneath it in a narrower reading rail offset to one
side, with figures breaking out into the full width. Horizontal and temporal,
not a centered stack of cards. Mobile stacks the strip above the prose but
keeps it as one continuous object rather than fragmenting it per section.

**Palette logic.** Three values, each mapped to a named state of a kilowatt-hour
in the corpus — not to a mood:

- **generate** — saturated amber
- **store** — deep indigo
- **buy** — the same indigo at full density, against
- **export-for-nothing** — a deliberately flat grey, because the visual point
  is that exported energy is worth almost nothing

Ground is a pale **zinc/blueprint white** — deliberately not cold-flu's warm
newsprint and not workflows' cold bone. Certainty is never encoded by colour
alone (1.4.1).

**Type.** A **serif display** — all three existing pages use grotesque display
faces, so a serif headline changes the silhouette before a single word is read.
Instrument Serif or similar for the headline, Instrument Sans / Reddit Sans for
text, Geist Mono or Martian Mono for figures. None of these appear on any
existing page.

**Motion signature.** Scrub-driven accumulation along the day axis: as the
reader scrolls, the strip fills left to right and the battery band builds
between the two price traces. This passes the motion test —

> *This motion lets the reader perceive **when in the day the money is made**,
> which would otherwise require a difficult mental comparison between two
> static traces.*

Reduced-motion branch is a first-class mode, not zeroed durations: the strip
renders as **five stacked static day-strips, one per state** — small multiples,
which is the parallelism finding, and arguably the better artefact.

**If it goes wrong.** It becomes a generic analytics dashboard: sparklines
everywhere, the strip demoted to wallpaper, the amber/indigo drifting into a
crypto-chart look. The guard is that the strip must carry a *claim id* in every
state or it gets cut.

---

### Direction B — "The Postcode Ledger"

**Register.** A filed tariff schedule / actuarial rate table.

**Device.** All eight states and territories side by side as a single wide
ledger, each column carrying its subsidy stack, its feed-in tariff and its
typical time-of-use spread, with the payback figure at the foot. The argument
is that **postcode decides this more than the hardware does**.

**Why I am not recommending it.** The material is genuinely strong, but the
execution collides twice: a per-jurisdiction selector is undervolt's sticky
switch generalised, and a static stacked-bar comparison is cold-flu's ranked
board with different labels. It also degrades badly if the research returns
thin coverage for the smaller jurisdictions — a ledger with four empty columns
reads as a failure rather than as honest absence.

**Where it survives.** As Direction A's exploration tier. See §4, section 10.

---

### Direction C — "Warranty Clock"

**Register.** The warranty certificate that comes in the box.

**Device.** Two concentric arcs on one 15-year scale — payback year inside,
warranty term outside — and the page's whole question is whether the inner arc
closes before the outer one runs out.

**Why I am not recommending it as the page.** Two dials is very little visual
bandwidth for a page of evidence, and cold-flu already ships rubber-stamp
graphics on certificate stock, so the official-document register is partly
spent.

**Where it survives.** As Direction A's **closing takeaway state** — the one
place the whole argument resolves into a single image that works with motion
switched off. Absorbed, not discarded.

---

## 4. Page structure (Direction A)

Martini glass: authored stem, then open. Lead with the conclusion, because
~38% of arrivals leave immediately and only a quarter pass the 1,600th pixel.

```
┌──────────────────────────────────────────────────────────┐
│ sticky masthead — Dossier / Margin  (build_chrome.py)     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  DAY STRIP ▁▁▂▄▆█▆▄▂▁  ← the hero IS the chart           │
│  serif headline set over it                              │
│  standfirst: the conclusion, one sentence                │
│  as-at date · jurisdiction scope                         │
├──────────────────────────────────────────────────────────┤
│  VERDICT — three cited sentences. No stat quad.          │
╞══════════════════════════════════════════════════════════╡
│ ┌──────── sticky day strip ─────────┐                    │  ← STEM
│ │  state 1  the spread is the product│                   │
│ └───────────────────────────────────┘                    │
│      ┌── reading rail ──┐   (offset, not centered)       │
│      │ prose + citations│                                │
│      └──────────────────┘                                │
│  ... states 2–5, same strip, one delta each              │
├──────────────────────────────────────────────────────────┤
│  CLOSING ARC — payback yr vs warranty yr (Direction C)   │
╞══════════════════════════════════════════════════════════╡
│  JURISDICTION LEDGER — wide, 8 columns (Direction B)     │  ← BOWL
│  WHAT WOULD CHANGE THIS ANSWER                           │
│  WHAT WE COULD NOT ESTABLISH                             │
│  METHODS NOTE                                            │
│  SOURCE REGISTRY                                         │
├──────────────────────────────────────────────────────────┤
│ closing marketing band  (build_chrome.py)                │
└──────────────────────────────────────────────────────────┘
```

**Greyscale-blur check against the three published pages:** cold-flu blurs to
`wide dark hero → 4 dots → 3 columns → long striped list`; workflows to
`light hero → 4 dots → alternating text/dark-block`; undervolt to `dark hero →
thin bar → numbered stack → wide figure`. Direction A blurs to `full-width
horizontal band held high, with an off-centre narrow text column beneath it,
repeating`. Different band positions, no dot row, asymmetric column. Passes on
the cheap heuristic — to be re-checked against real renders at Phase 8.

### The stem, state by state

Each state carries exactly one `claim_id`, one caption sentence, one visual
delta, and renders completely from its id.

| # | Section | Claim slot | Visual delta |
|---|---|---|---|
| 1 | **The spread is the product** | What you're paid to export vs what you pay to import, at the same hour | Two price bands appear on the strip; the gap between them shades |
| 2 | **Your evening is the asset** | How much consumption lands after sunset decides the answer more than the battery does | Household load trace overlays; the strip's shape is unchanged, only the overlay is new (parallelism) |
| 3 | **The subsidy is a declining asset** | The federal discount steps down while installed prices also move | *Orientation state required* — the x-axis changes from hours to program years. New grammar and new finding are not introduced together; the transition explains the swap |
| 4 | **Sizing** | Oversizing buys cycles the household never uses | Capacity band grows against an unchanged load trace; the unused remainder is the visual |
| 5 | **VPP — paid for the cycles that consume the asset** | The editorial tension, stated as tension | Two counters move in opposite directions on one axis |
| 6 | **Closing arc** | Does it close inside warranty | Direction C's twin arcs. Static-safe takeaway |

If a caption ever contains two independent propositions, split the state.

### The bowl

- **10. Jurisdiction ledger** — the wide 8-column table. Cells with no reliable
  public figure are left **explicitly empty and labelled**, never filled with a
  weaker source. This is a genuinely two-dimensional table, so it is the
  permitted 1.4.10 reflow exception, in a labelled overflow container.
- **11. What would change this answer** — input sensitivity: tariff type, load
  shape, whether the rebate is counted, discount rate.
- **12. What we could not establish** — required, and the section that most
  makes the page read as authored.
- **13. Methods note** — which backends ran, what they cost, what was read end
  to end, what was citation-verified, what a human reviewed. Specificity, not
  an "AI-assisted" badge.
- **14. Source registry** — deduplicated, full metadata, access date,
  backlinks to every claim using each source.

---

## 5. Chart integrity, bound now

- Every price in **c/kWh with the unit named**. No dual axes anywhere — the
  temptation here is price-and-payback on one frame, and it implies a
  correlation the data does not carry.
- **Payback is a range with stated uncertainty, never a point estimate.**
  Truncation and false precision inflate perceived differences 58–130%, and
  telling the reader does not fix it.
- Any bar-length encoding starts at zero or carries an explicit break.
- **Nominal or discounted — state which, once, and never mix.** This is the
  most likely place for the page to quietly mislead.
- Every visual gets an **editorial title stating its conclusion** ("The spread
  is the product"), not a descriptive label ("Import vs export prices").
- Every chart: short alt naming chart type + primary conclusion, plus a
  structured data table. Redundant encoding (colour *and* pattern) throughout.

---

## 6. Motion budget and the three.js gate

**three.js: rejected.** Fails evidence test 1 (no claim depends on depth,
volume, occlusion or movement through space) and test 3 (a 2D time axis is
sufficient and clearer). Per the skill, this rejection gets recorded in the
page's own notes, and the annotated static graphic ships.

Three-tier stack:

| Tier | Used for |
|---|---|
| CSS `animation-timeline: scroll()` | Strip fill, section progress. `@supports`-guarded; never the only carrier of meaning |
| IntersectionObserver | Step *n* selects strip state *n* |
| GSAP ScrollTrigger `scrub` | The one accumulation scrub on the day strip — the only transition with a perceptual job |

No SplitText headline reveal (cold-flu owns it, and it fails the motion test).
`normalizeScroll()` prohibited; native scroll untouched. Steps sized in **px
computed from `window.innerHeight`**, never `vh`. Pin with CSS
`position: sticky`. Refresh triggers after fonts and figure dimensions settle.

---

## 7. Icon and share

Two subject-mined directions:

1. **The gap mark** — two horizontal bars, one pale and thin (export), one dark
   and thick (import), the shape being the space between them. Survives 16px,
   and it is literally the page's argument. **Recommended.**
2. **The notched ring** — an incomplete arc with a break where the warranty
   ends. Handsome, but reads as a generic progress ring at favicon size.

Wire the result in as favicon, `apple-touch-icon`, **and `og:image`** — two of
the three existing pages ship with no `og:image` and share as bare links.

---

## 8. What must be settled before anything is built

These go to `/clarify` in Phase 0, before the panel spends anything, because
the brief is fixed once the run starts:

1. **Who is deciding what?** A homeowner with existing solar deciding this
   year, or someone with no solar deciding whether to do both? These buy
   materially different corpora. This becomes `decisionContext`.
2. **Jurisdiction scope** — all states and territories, or NSW/VIC only? This
   decides whether the ledger in §4.10 is the bowl or is cut.
3. **Does the headline payback count the federal rebate?** With, without, or
   both. This is the single most consequential editorial choice on the page.
4. **Time horizon** — does the page project the rebate step-down forward, or
   report only what is legislated as at the publication date?
5. **Nominal or discounted cash flow**, and at what rate.
6. **Is Luke's own household a worked example on the page, or is it generic?**

And the one to hold loosely: **the editorial tension must be chosen from what
the panel actually finds contested**, not from my guess. My candidates are
*payback landing outside the warranty term* and *VPP revenue being paid for
cycles that consume the asset* — but if the panel disagrees with itself
somewhere else, that disagreement is the centre of the page instead.
