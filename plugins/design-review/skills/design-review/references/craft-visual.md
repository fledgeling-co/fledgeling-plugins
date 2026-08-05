# Craft — visual judgment

Tier 2, and the stage where automated review is least reliable. Three rules make it work.

**Decompose to binary.** Every judgment is MET or UNMET against a named criterion. Never a 1–10 score. Cross-model agreement on free-form visual scoring is worse than chance; on atomic binary checklists it approaches human levels. The decomposition is doing all the work.

**Inspect crops, not pages.** At page scale a 161px void reads as generous whitespace and an orphaned chip is a few ragged pixels. Judging from thumbnails is looking at an image in which the defect cannot exist and concluding there is none.

**Ask "what is wrong with this?"** — never "is this done?". Same pixels, opposite answers. Answering "nothing" requires first naming the three most likely failure modes for that component and ruling each out by pointing at pixels. If you can't name three, you don't know the component well enough to clear it.

---

## Hierarchy

Built from **five vectors**, not size alone: scale, weight, spacing, tracking, alignment. The dominant element needs **at least two working in the same direction**. Size-only hierarchy is fragile — any layout constraint that collapses the size contrast destroys it.

Identify primary, secondary, tertiary. If you can't tell, hierarchy is broken. One dominant entry point per visual region, not two.

**Two failure modes, diagnose which:**

- **Flat** — everything at similar visual weight. Scale steps under 1.25× between levels with no compensating weight or spacing jump. Fix by increasing contrast on ≥2 vectors
- **Noise** — several elements competing as co-primaries. Everything bold, large, or accented. Fix by promoting one deliberately and demoting the rest, including things that feel important. Hierarchy is relative

**Iso-styled competing actions are a hard failure.** When two or three adjacent actions render at identical visual weight ("Keep my plan" / "Remind me later" / "Cancel" as three matching buttons), the first-glance read literally cannot locate the intended action — the equality *is* the obstruction. One filled primary; the rest step down to outline, then text.

**Colour is read pre-attentively**, before any text. A wrong affordance colour cannot be rescued by its label — a destructive action styled in the confirm colour reads as "confirm" no matter what it says. Fix the colour, don't caption it.

**Weight hierarchy** — three weights do the work: Read (400/450) for body, Emphasize (510/550) for UI text, labels and nav, Announce (590/600) for headlines and buttons. 700+ is rarely needed; bold used for "emphasis on emphasis" means weight discipline failed elsewhere. Weight should *jump* between levels, not step — a regular→medium→semibold→bold ladder reads as a default scale, not authored hierarchy.

**Position** — in LTR, eyes start top-left. Logo, primary headline, primary CTA belong in prime real estate. Flag a primary element buried bottom-right.

**Density signals** — loose spacing around important elements says "pay attention"; tight spacing says "supporting". Flag the reverse: important content crammed while unimportant content breathes.

**Label/value pairs** — on stat tiles, dashboards and metadata rows the **value outranks its label**. Flag "Sales" set larger or bolder than "591". The label whispers; the number speaks. Pair with `font-variant-numeric: tabular-nums` on comparable columns.

**Five-second test.** A first-time user should understand what to look at and what to do within five seconds. On navigation-bearing surfaces also run the trunk test on an interior page in isolation: what site is this, what page am I on, what are the major sections, what are my options, where am I in the scheme. Any unanswerable question is a wayfinding gap.

---

## Typography numerics

The most specific checkable set in the whole review.

**Letter-spacing** — the most-skipped rule in generated design:

| Context | Tracking |
|---|---|
| Body text 14–18px | `0` |
| Small text 11–13px | `+0.01` to `+0.02em` |
| UI labels, button text | `+0.02em` |
| **ALL CAPS** | `+0.06` to `+0.1em` — required |
| Headings ≥32px | `−0.01` to `−0.02em` |
| Display ≥48px | `−0.02` to `−0.03em`, hard floor `−0.04em` |

Tighter than the caps range and the counters collide; wider and the word disintegrates. Tighter than −0.04em on display and the letters touch, which reads cramped rather than designed.

**Untracked caps and untracked display are the two most reliable typographic tells.** Untracked caps look cramped and amateur; untracked display looks loose and weak.

**Leading and measure:**
- Display / H1 (≥32px): line-height 1.0–1.2
- Body: 1.5–1.6
- Measure 50–75 characters per line (`max-width: 65ch`)
- Never justify body text on the web — it creates rivers. `text-align: start` with a ragged edge

**Scale discipline:**
- Every font size from a defined scale. Flag arbitrary values (`17px`, `23px` in a design otherwise using 16/20/24)
- Max **3 type sizes above the fold**. More is a composition problem, not a hierarchy opportunity
- Fluid display via `clamp()` is legitimate on marketing surfaces — check the bounds sit on the scale, the max stays **≤6rem (~96px)** (above that the page is shouting), the mid-range doesn't collide with the section below, and the longest headline word survives every breakpoint without overflowing
- A 4-line hero headline is a font-size error, not a copy-length problem

**Micro-typography** — correctness rules, not taste:
- Curly quotes and apostrophes, never straight. Exception: foot and inch marks stay straight
- Three dashes with three jobs: hyphen for compounds, en dash for ranges (1–10), em dash for sentence breaks. Never `--`
- Real ellipsis `…`, not three periods. Real `©`/`™`/`®`
- One space after punctuation
- `&nbsp;` inside measurements and shortcuts (`10&nbsp;MB`, `⌘&nbsp;K`), before numeric references, after honorifics
- Bold **or** italic, never both. Never underline for emphasis — underline means link
- Small caps only if real (`font-variant-caps: small-caps` with a font carrying `smcp`). Scaled-down capitals are fake and look thin
- `text-wrap: balance` on headings, `pretty` on prose
- Tabular figures on any column of comparable numbers, prices, or timers
- **The JSX gotcha:** unicode escapes like `&rsquo;` render *literally* in JSX text content. Paste the real UTF-8 character, or use `{'’'}`. Escapes work inside JS string literals, not in JSX text between tags

---

## Rhythm

**Spacing scale.** All padding, margin and gap values snap to a consistent scale — multiples of 4 or 8. Flag random values (`padding: 7px`, `margin: 18px`, `gap: 13px`). List the scale that's been *implicitly* used and name the outliers.

**Repetition.** Sections that should look alike — cards in a grid, list items, feature blocks — share padding, gap, font sizes and structure. Flag near-duplicates that are subtly different: either they should be identical or deliberately different.

**Strategic variation.** A long page breaks its pattern occasionally — a different background, a wider section, a centred CTA. Flag both extremes: completely uniform reads monotonous; varying every section reads chaotic.

**Palette discipline.** 3–5 colours plus tints and shades across the whole surface. Flag 8+ distinct colours.

Weight *slightly*-different values as the **more severe** finding. A value within ~5% of an existing token reads as "almost right, therefore wrong" — colour perception is non-linear, so a near-miss registers as more wrong than an obviously different colour, which at least might be deliberate. Snap near-misses to the token; only clearly-different values get to argue.

**Reserved-meaning colours, ~3 per surface max.** When one card carries red scarcity plus yellow urgency plus green status plus an accent CTA, the meanings collapse and the card just reads "loud". Demote the rest to neutral.

**Section structure.** Sections visually distinguishable — background change, divider, padding shift — but following a consistent pattern. Flag sections with no separation (content blurs) and sections with too many separation styles (no rhythm).

**Cross-card discipline.** In any card group or comparison layout, shared elements align across all items: CTAs pin to the card bottom so they form one clean line regardless of content length above; titles, prices and feature lists start at the same Y in every column. Misaligned baselines across side-by-side cards read as broken, not as variety.

---

## Five mechanical lint rules

Run regardless of judgment. No two adjacent hierarchy levels may share scale AND weight AND spacing — if all three match the levels are indistinguishable. At least one section gap should be ≥1.5× the others, or the page reads as an undifferentiated list of blocks. Gap inside a group must be visibly smaller than gap between groups, since proximity is the primary grouping signal and when padding-within equals margin-between, grouping collapses. Content max-widths form a 2–3 tier system (full-bleed, content, optionally prose) — a fourth distinct `max-width` is drift, and shifting content rails between sections read as structural incoherence. Border-radius uses at most 3 values — a fourth is drift, not a scale.

---

## Optical alignment

Mathematical centring frequently does not look centred, and this is documented in current icon-system guidance rather than being folklore.

- **Icons beside text** — size the icon to the font's line-height (24px font → 24px icon), then tighten. Icon stroke matched to text weight: 1.5px beside 400, 2px beside 600. One icon set per surface
- **Asymmetric glyphs** — a play triangle centred by its bounding box sits visibly left-heavy. Needs a manual offset
- **Text inside buttons** often needs a 1–2px nudge to *look* centred
- **Concentric radii** — `outerRadius = innerRadius + padding`. A universal `rounded-lg` across nested layers violates this and reads subtly wrong
- Correct optical alignment with `transform: translateY()`, never `margin` — a transform doesn't disturb the box model, so it can't knock a value off the spacing scale

Mathematically perfect but optically wrong is a finding, not a pass.

---

## Depth and elevation

- **One light source.** Every shadow falls the same direction
- **Layer two or more shadows per level** — tight and dark underneath, wide and faint around. Single-value box-shadows read flat
- **Tint shadows with the surface hue** on coloured backgrounds. Grey shadows on coloured grounds look dirty
- **Dark themes elevate with lightness, not shadow** — each level ~4–6% lighter. Shadows barely register on dark
- 3–4 elevation levels as tokens, every surface mapped to one. Ad-hoc shadows are the depth equivalent of random margins
- Depth cues that cost nothing: overlap, scale, blur-behind
- **If the shadow is the first thing you notice, it's wrong**

Glass and translucency: only when there is something worth blurring behind it. Glass over a flat white page is decoration. The 1px light border and inset top highlight are what make it read as material rather than smudge. Text on glass needs a contrast fallback. One glass layer, never stacked — and adjacent glass elements share one glass region rather than each blurring independently.

**Imitation material.** A surface claiming a physical material the page never actually renders — CSS bevels, embossing, faux letterpress, fake foil, stamped-metal, chalk — reads as machine-made faster than most items on the tell-list, and unlike them it is partly greppable: `box-shadow: inset` plus a gradient plus a border on one element, stacked to fake relief, is a detectable signature.

Two things separate it from legitimate depth. Real elevation says *this sits above that*; imitation material says *this is made of that*, and the second claim needs an asset to be true. And it usually arrives where an asset was wanted and unavailable — a hero, a cover, a card meant to carry texture — so the honest alternatives are a real image or an honestly flat surface, never a gradient standing in.

Tier 2, because whether a bevel is imitation or a deliberate skeuomorphic style is a judgment. Report it as a finding on the *claim*, not on the CSS: name the material being imitated and what the surface would need to make the claim true.

---

## Density

Four axes, not "more or less whitespace":

1. **Visual density** — stuff per screen. Unreliable on its own
2. **Information density** — the data-ink ratio. Every bit of ink requires reason
3. **Design density** — necessary design decisions over total decisions
4. **Temporal density** — actions per unit time

The temporal thresholds are directly actionable:

| Interval | Perception |
|---|---|
| <100ms | Feels simultaneous — **and animation here makes it feel slower** |
| 100ms–1s | Connection breaks; a transition bridges it |
| 1–10s | Abandonment risk; indeterminate loader |
| 10s–1min | Determinate progress bar |
| >1min | Release the user, notify later |

The first row cuts directly against a common generated pattern: adding transitions to interactions that complete instantly.

Density should match task frequency and expertise. Compact rows stay scannable through alignment, typography and restrained colour. Premium density means *more signal*, not smaller everything. Flag both an empty "luxury" dashboard with one datum per card and an undifferentiated wall of controls.

**Decoration density should fall as interaction frequency rises.** Generated UI reliably does the inverse — adding hover transitions, cursor changes and entry animations to everything. This is detectable and worth checking directly.

---

## Content credibility

**The swap test.** Replace the product name with a competitor's. If most copy and illustrations still work, the page has insufficient product specificity.

Catches: "Unlock the future"; fabricated round-number metrics ("10,000+ teams"); "Sarah Chen" testimonials; lorem ipsum; unexplained charts; buttons labelled "Continue" with no destination.

**Sample data** wants to be believable, specific, slightly messy. Locale-appropriate realistic names, never "John Doe". Photo-style avatars, never the SVG egg. Organic numbers (`47.2%`, `+1 (312) 847-1928`) rather than `99.99%` or `50%`. Contextual brand names that sound real, never Acme or SmartFlow. Concrete verbs, never Elevate or Unleash. Testimonial quotes ≤3 lines with real attribution — name, role, company — never "— Sarah".

---

## Work the inventory, not your intuition

This section's coverage used to be discretionary, and that is exactly where reviews lose defects. Everything in this skill with an enumeration gets done; everything without one gets improvised.

So start from `probeComponentInventory()` (stage 5), not from the screenshot. It returns every distinct component type with a count and a crop box. Crop in priority order — layout-flagged, then interactive, then ≥3 instances, then primary task path — and tick each off.

For each crop opened, the finding (or clearance) carries: the component, the viewport, the DPR, what was checked, and the three failure modes considered. A clearance with no named failure modes is not a clearance.

Types you did not open go in the report's Coverage block as the unopened remainder. Never as silence.
