# Evidence — what the panel established, and what it did not

Five backends, one brief, all read end-to-end. Gemini ($7.00) · OpenAI
gpt-5.6 ($9.00) · Perplexity Sonar ($4.00) · Claude Code ($0) · Codex CLI
($0). **$20.00 total**, 397,000 chars, 225 cited sources.

Citation verification: Claude Code **PASS** (0 fabricated / 50). OpenAI
**ATTENTION** (1 dead of 44 — a 404 mirror of Robertson 2008, which the
same report also cites by working DOI and which Claude Code cites
independently). No load-bearing claim rests on a URL that does not exist.

Source quality is not even across the panel. Claude Code, OpenAI and
Codex carry peer-reviewed work with participant counts and p-values.
Gemini leans on marketing blogs for several numbers and asserts one
statistic that turns out to be unsourced (§8). Perplexity returned the
fewest sources (20, including a Facebook group post and two vendor
blogs) but found two peer-reviewed papers nothing else did (§12).

Every rule in SKILL.md traces to a row here. A finding with no design
consequence was not a finding worth keeping.

---

## 1. The headline result, agreed by all five

**Scrollytelling buys engagement, perceived clarity and lower cognitive
load. It does not buy comprehension.** This is the single most repeated
finding in the corpus and it constrains everything the skill claims.

| Study | n | Result |
|---|---:|---|
| Méndez & Such, CHI 2026 | 454 | Scrollytelling matched plain text and two other formats on comprehension accuracy and confidence; beat text on cognitive load and engagement; trust differences **statistically inconclusive** |
| McKenna et al., 2017 | 240 | Animated transitions beat static on perceived engagement (`p<.001`); comprehension ~4/5 with **no major condition difference**; scroller vs stepper inconclusive |
| Obie et al., 2019 | 40 | Narration improved value-message comprehension (`p=.04`) and short-term recall (`p=.04`), **not** long-term recall |
| Boy, Détienne & Fekete, 2015 | 3 field expts | Introductory stories **did not** increase later exploration; only 40.9% / 41.5% of qualifying sessions traversed all sections |
| Kim et al., 2024 | within-subj | Immersive (3D, cinematic camera) rated more interesting and **more persuasive**, but **no more understandable or trustworthy** |
| Rogha et al., 2024 | 2 expts | Contrasting narratives raised surprise and interest **and raised recall error** |

**Design consequence.** The page's job is attention management, not
proof of learning. Never report dwell time or completion as evidence of
understanding. And Kim et al. is the sharpest line in the corpus: motion
that raises persuasiveness without raising understanding is rhetoric
charged to the reader's battery.

---

## 2. Narrative structure

Segel & Heer's taxonomy (IEEE TVCG 2010, derived from 58 examples) is
settled and all four backends default to the same choice.

- **Martini glass is the default**: authored stem establishing the
  claim, then opening to reader-driven exploration, sources and data.
- **Interactive slideshow** for bounded explainers and mobile steppers.
- **Drill-down** *after* the main finding, never instead of it.
- **Free exploration is never the sole delivery mode.**

Hullman et al. 2013 (42 professional narrative visualisations) adds
**parallelism**: repeated structural relationships between adjacent
states aid memory and preference. Keep scales, objects and spatial
positions stable across states unless changing one *is* the evidence.

**Where the conclusion goes.** Chartbeat/Slate instrumentation: ~38% of
arrivals leave immediately, median scroll depth ~50% (Slate) to ~60%
(web), only 25% pass the 1,600th pixel of a 2,000-pixel article, and the
relationship between scroll depth and sharing is **only very weak**. A
structure that withholds the finding until state twelve is built for the
quarter of readers who get there. Lead with the conclusion.

**One idea per scroll state** is a production discipline, not a measured
law — OpenAI and Codex both flag this explicitly as
`<INSUFFICIENT_EVIDENCE>`. Keep the rule; drop the pretence that a study
supports the phrasing.

---

## 3. Motion — when it helps and when it hurts

The contested area, and it **resolves by unit of analysis**, not by
compromise.

- **Supported**: animated transitions *between two states of one
  encoding*. Heer & Robertson 2007 (n=24): tracking error reduced across
  all transition types (`p<0.001`), object-tracking animations 1.25s,
  value-change 2s.
- **Not supported**: animation as an explanatory medium replacing static
  graphics. Tversky, Morrison & Bétrancourt 2002: apparent advantages
  were confounds (animated conditions carried more information); after a
  week, text-studying participants **improved** while animation-studying
  participants **declined**.
- **More staging is not better**: extreme staging was *worse* than direct
  animation for donut value changes (`p=0.024`); stacked bars showed no
  effect (`p=0.224`). Axis rescaling increased errors — keep common
  scales and persistent landmarks.
- **Static wins for analysis**: Robertson et al. 2008 found animated
  trends inferior to static traces and small multiples for analysis
  tasks, though preferred for presentation.

**The motion test** (Codex's formulation, the most usable):
> An animation is admissible only when a reviewer can finish the
> sentence *"this motion lets the reader perceive ___ that would
> otherwise require a difficult mental comparison."* If the blank is
> "energy", "delight", "premium quality" or "immersion", it is
> decoration.

---

## 4. The GSAP question — the one genuine conflict

**Gemini says** replace GSAP with native CSS `animation-timeline: scroll()`
because GSAP runs on the main thread and degrades INP.
**OpenAI and Codex say** ScrollTrigger is a sound standing orchestration
layer: it precomputes trigger positions, debounces scroll, syncs to
`requestAnimationFrame`, and throttles resize recalculation to a 200ms
gap. The risk is the producer's own `onUpdate` handlers, not GSAP.

**Claude Code adjudicates it and is right**: every specific INP claim on
*both* sides traces to commercial or vendor-adjacent blogs
(`[SECONDARY: promotional]`), and the widely repeated "≤30 active
triggers" figure has **no traceable empirical basis**. What *is*
primary-sourced is the mechanism — CSS scroll timelines run off the main
thread (Chrome for Developers); GSAP timelines do not.

**Held loosely, resolved as a three-tier stack:**

| Tier | Use | Why |
|---|---|---|
| CSS `animation-timeline` | Entrance reveals, progress bars, sticky-header states — anything expressible as transform/opacity over scroll progress | Off main thread; `@supports` guard degrades cleanly. Not Baseline in 2026, so never the only carrier of meaning |
| IntersectionObserver | Discrete state changes: step *n* selects chart state *n* | Low cost, universal |
| GSAP ScrollTrigger | **Scrub** and pinning that CSS cannot express | The technique with the strongest comprehension evidence behind it |

Reaching for GSAP by default buys main-thread cost the page does not
need; abandoning GSAP loses scrub. The user's brief mandates GSAP as the
standing layer, which is compatible with this: GSAP orchestrates, and
simple reveals still compile to CSS where they can.

**Unresolved and worth stating**: no published reproducible benchmark
compares INP across the three implementations on mid-tier mobile. Claude
Code's recommendation #1 is to run it. The skill should not pretend the
magnitude is known.

---

## 5. Performance floor — externally fixed, not a matter of taste

All four agree. LCP ≤2.5s · INP ≤200ms · CLS ≤0.1, at the **75th
percentile of CrUX field data over a rolling 28-day window**, measured
per device class, **all three must pass** (two of three is a fail).

- Frame budget 16.7ms at 60fps; MDN estimates ~10ms remains after
  browser rendering work.
- Any main-thread task >50ms is formally a long task.
- INP replaced FID on **12 March 2024** and reports the *worst*
  interaction of the whole visit — so a report's last scroll state is as
  load-bearing as its first.
- INP does not directly measure scrolling, but script and animation work
  occupying the main thread delays the next click, tap or keypress.

**No universal asset budget exists.** All four returned
`<MISSING_DATA>` on JS-kilobyte, ScrollTrigger-count, polygon, texture
and draw-call limits. Gemini's 256–384MB WebGL heap figure and the
~0.1ms-per-draw-call rule of thumb are uncorroborated. Derive from a
device matrix; do not copy a number from an unrelated production.

---

## 6. Citation and provenance UX

**Verification is rare, and that is the finding.** Piccardi et al. 2020
instrumented 96 million Wikipedia citation events over two months:
external-reference clicks in **0.29% of page views** — 0.56% desktop,
0.13% mobile — and **93% of cited URLs received no click** that month.
Clicks were *more* common on shorter, lower-quality pages, suggesting
readers verify when the page fails them.

So the citation layer is not built to be clicked. It is built so the
claim–source bond is inspectable and the page cannot quietly overclaim.

**The three-layer interface**, agreed by OpenAI, Codex and Claude Code:

1. **Inline marker** adjacent to the smallest claim span the source
   supports — never bolted to a paragraph carrying several propositions.
2. **Preview** on hover, keyboard focus *and* tap: title, author or
   organisation, date, evidence type, one sentence on what the source
   supports, and "open original". Escape closes; focus returns.
3. **Persistent registry**: deduplicated, full metadata, access date,
   and backlinks to every claim using that source.

**Tse's rule constrains all of it**: *"if you make a tooltip or rollover,
assume no one will ever see it."* Any design where a source exists only
inside a hover state has, by that rule, no sources. Redundancy is the
point, not cleverness.

Trust evidence is weaker than it looks: a *single* transparency feature
had almost no effect on credibility; multiple co-present indicators did
(1,183 adults, small but significant improvements on 4 of 15 measures).
Only 34% could identify the journalist and 26% recall a detail of an
explanation they had seen. And a 2026 study found displaying reliability
information could *reduce* map trust and accuracy — transparency can
appropriately lower confidence when it reveals uncertainty.

`<INSUFFICIENT_EVIDENCE>` The claim "good citation UX makes readers
verify" is unsupported in either direction. What is supported is
narrower: preview affordances lower exploration cost, and multiple
co-present signals raise perceived credibility more than one.

---

## 7. The three.js gate

Every backend independently converged on a conjunctive test. Merged, with
OpenAI's evidence/release split and Codex's comparative test:

**Evidence tests — all must pass, or reject 3D outright:**
1. **Spatial claim.** A major claim depends on depth, volume,
   orientation, topology, occlusion, assembly, or movement through
   physical space.
2. **Viewpoint necessity.** Changing viewpoint *reveals evidence*
   rather than showcasing an object.
3. **2D insufficiency.** A map, cutaway, orthographic diagram, annotated
   image or small multiple cannot communicate the claim at least as
   clearly.

**Release tests — all must pass, or ship the fallback until they do:**
4. **Narrative mapping.** Every camera or object transition maps to a
   claim. No decorative idle orbit.
5. **Equivalent fallback.** Static images, diagrams and text carry the
   same conclusion without WebGL — because **device capability cannot be
   reliably feature-detected** (14islands: some browsers claim WebGL
   support and are too weak to use it; they infer from screen size).
6. **Performance and reduced motion.** Passes the CWV budget on the
   target mobile tier and fully disables non-essential camera motion
   under `prefers-reduced-motion`.

Counter-evidence to keep in view: Kwon et al. 2020 found 2D better for
spatial-memory tasks in networks, and systematic work identifies
occlusion, clutter, distortion and scalability as persistent 3D
trade-offs.

**If approved**: dynamic-import after narrative content; render on demand
rather than an unconditional loop; `dispose()` textures, geometries and
materials between chapters (GPU memory otherwise grows until the tab
crashes — survives in demos because sessions are short); cap device pixel
ratio; KTX2/Basis over PNG/JPEG (stays compressed in VRAM); never
raycast against all objects on every mouse move; handle
`webglcontextlost`; keep labels, transcript and sources outside the
canvas in normal DOM order.

---

## 8. Accessibility floor

- **2.2.2 Pause, Stop, Hide — Level A.** Auto-starting motion over 5
  seconds shown in parallel with other content needs a pause/stop/hide
  mechanism. Mandatory under ADA Title II/III, Section 508, EN 301 549
  and the European Accessibility Act. A control that appears only on
  hover **fails** — users who navigate by voice may never trigger it.
- **2.3.3 Animation from Interactions — Level AAA.** Explicitly covers
  scroll parallax. Not contractually required at AA, but increasingly
  expected in government, healthcare and education procurement.
- **2.3.1 Three Flashes — Level A.** Distinct from 2.2.2; seizure risk,
  not distraction. Reduced motion is not a substitute.
- **1.4.13 Content on Hover or Focus — AA.** Hover content must be
  hoverable, dismissible and persistent. This is the criterion naive
  citation tooltips fail.
- Also in scope: 1.3.1/1.3.2 meaningful sequence, 2.1.1 keyboard, 2.4.3
  focus order, 2.4.7 focus visible, 2.4.11 focus not obscured, 1.4.1
  colour alone, 1.4.3/1.4.11 contrast, 1.4.10 reflow at 400% zoom,
  4.1.2 name/role/value.

**Reduced-first, not motion-first.** Static baseline; motion added only
under `@media (prefers-reduced-motion: no-preference)`. This **fails
safe**: a browser that does not support the query ignores the block and
leaves the static baseline. The reduced branch is a first-class narrative
mode, not every duration set to zero after authoring — replace parallax
with fixed positioning, camera travel with annotated stills, scrubbed
morphs with discrete states, ambient loops with static composition.

**Canvas and 3D** need a short description plus a structured long
description or data table; structured data stays structured rather than
compressed into `aria-describedby`. Do not fire an `aria-live`
announcement per scroll state — stable prose carries the narrative;
live regions are for deliberate control actions.

**A number to state carefully — and a correction to this file.** The
claim that vestibular disorders affect ~35% of adults over 40 is repeated
across accessibility guides. Gemini asserted it flatly; Claude Code
flagged it `<CONFIDENCE:LOW>` as having **no traceable epidemiological
citation**, and this file originally repeated that. **The flag was
wrong.**

It traces to Agrawal, Carey, Della Santina, Schubert & Minor, *Disorders
of balance and vestibular function in US adults: NHANES 2001–2004*, Arch
Intern Med 2009;169(10):938–944, n=5,086 — a real and heavily cited study
reporting 35.4% of US adults aged 40+ with vestibular dysfunction.

What is wrong is the sentence usually built around it:

- It measured **failure of a modified Romberg standing-balance test**, a
  screening proxy, not diagnosed "vestibular disorders". About a third of
  those who failed reported no dizziness at all.
- It is **US-only, 2001–2004**; the unqualified phrasing reads as a
  standing global rate.
- Its outcome is **falls** — adjusted odds ratio 12.3 per the published
  correction at Arch Intern Med 2009;169(15):1419 — **not sensitivity to
  on-screen motion**. "35% have this, therefore reduced motion matters"
  is a bridge the study does not build.
- The "70 million Americans" figure quoted alongside it is the *same
  study*, so citing both reads as corroboration that is not there.

**Design consequence, and the more useful lesson.** The failure mode is
not a fabricated statistic. It is a real statistic wearing a claim it
does not support — "claims outrunning sources" (§9) at sentence level,
which is harder to catch than invention because the citation resolves.
Either state it with the measurement named, or make the case on WCAG
2.2.2, 2.3.3, 2.3.1 and SCR40, which survive a click-through unaided.

> Provenance of this correction: it was found by an eval baseline running
> with **no skill at all**, which checked a figure the panel had
> dismissed, and independently by a with-skill run that audited its own
> reference file rather than trusting it. Recorded because a skill that
> hides where its research was wrong is worth less than one that shows
> it — and because "no traceable citation" is a warning that collapses
> the moment someone finds Agrawal, where "the study measures something
> else" survives contact.

---

## 9. Failure modes to gate against

| Failure | Evidence | Rule |
|---|---|---|
| **Scrolljacking** | NN/g 2023: majority experienced at least mild disorientation; on a *fully* scrolljacked page **every participant was disoriented**. Murano 2026 (n=20): no speed benefit, significantly **lower accuracy and satisfaction** | Never alter wheel/touch distance, direction, momentum or history. GSAP `normalizeScroll()` is prohibited. Short scrolljacks also create an *illusion of completeness* — readers assume the page ended |
| **Misleading charts** | Pandey et al. CHI 2015 (n=330): deceptive charts produced interpretations **58.5%–129.5% larger**; inverted axis made **97.5% respond incorrectly**. Okan et al. 2021: 83.5% showed a truncation effect and **instruction did not eliminate it** | Validate axes, baselines, units, intervals, legends, uncertainty at generation time. Reader sophistication is not a mitigation — chart familiarity and education showed no protective correlation |
| **Intermediate-state dependency** | The Pudding: readers skip states faster than animations complete | Every state renders directly and idempotently from its id; never depend on a prior animation having finished. No claim exists only inside an animated intermediate frame |
| **Mobile collapse** | WaPo eclipse scroller: **30MB+** image load before lazy loading and <10KB thumbnails. Newsday: browser-bar changes altered viewport height and **cut off non-scrolling text** | Size steps in `px` from `window.innerHeight`, **never `vh`**. Pin with CSS `position: sticky`, not JS. Stack instead of scroll when transitions carry no meaning |
| **Hover-only content** | Tse, Malofiej 2016 | No hover-only content; stray taps during scroll cause accidental triggers |
| **Template sameness** | Goree et al. CHI'21: ~2M pairwise comparisons — layout similarity distance **declined 44% from 2010–2019**, and the strongest correlate was **shared use of a small number of frameworks and libraries** | See §10 |
| **Claims outrunning sources** | Hullman & Diakopoulos: narrative design adds, omits and prioritises at data, visual, annotation and interaction layers | Build fails if a quantitative or attributed claim lacks a source, if a source supports only a nearby proposition, or if an inference renders as a direct finding |
| **Engagement mistaken for learning** | §1 | Never cite dwell time as comprehension |

---

## 10. What makes a page read as authored rather than generated

The most important section for this skill, and the one with the least
settled evidence — all four flag it `<INSUFFICIENT_EVIDENCE>`: there is
**no validated metric** for "recognisably templated".

What *is* measured is the opposite. Goree et al. found homogenisation is
driven by **shared libraries**, and the invariant that reads as sameness
is **layout skeleton and motion signature — not palette**. Recolouring
does not fix it.

**The system boundary**, stated three different ways by three backends
and identical each time:

> Standardise the hidden infrastructure. Derive the visible rhetoric
> from the subject.

Reuse freely: the content model, provenance graph, citation components,
focus styles, accessibility harness, performance gates, grid utilities,
test infrastructure. Never reuse: hero composition, sticky-graphic
layout, chart grammar, illustration system, transition metaphor,
typography.

**The authored-review failure list** (Codex, the most operational):
a page fails if its section silhouette matches the preceding report once
colour and copy are stripped; if changing the subject noun leaves the
visual metaphor intact; if motion is repeated fade/slide/reveal recipes;
if typography and texture are unrelated to the source material; if the
hero is more specific than the evidence beneath it; if the same chart
grammar appears regardless of data type; or if there is no explicit
editorial tension, uncertainty or counterargument.

**The theme-proof test** (OpenAI): every major visual choice maps to a
named concept in the topic corpus. Random palettes, generic particle
fields and interchangeable dark "cinematic" heroes fail.

Precedent worth copying: the Financial Times built reusable story
patterns around **specific reader questions** rather than generic
layouts, introducing each only after it had worked on a prominent story.

One caution against pure distinctiveness: Song et al. 2025/26 found
cartoon styling and hand-drawn fonts **reduced perceived credibility**,
while embellishment improved recognition in other work. Distinctive is
not the same as arbitrary.

---

## 11. What Perplexity added that nothing else found

Two peer-reviewed findings no other member surfaced, both load-bearing
for a page that is openly machine-assembled.

**Disclosing AI involvement does not reliably cost credibility.**
Licenji & Hoxha's systematic review of **47 studies** on how audiences
respond to news presented as "written by artificial intelligence" found
effects on perceived credibility are **predominantly null or
conditional**. There is no uniform "AI penalty", and disclosure cues do
not act as warning labels that reduce trust; observed effects depend on
topic, cue wording and study design.

Their recommendation is the usable part: treat transparency as one
element of an **accountability package** — say what the automation
actually did, say what review it received, and state who is responsible
and how corrections happen. A vague "AI-assisted" badge is not that.

**Design consequence.** Every page carries a methods and provenance note
saying which backends ran, what they cost, what was read, what was
verified, and what a human reviewed. This is not a liability disclaimer
bolted on; the evidence says it does not cost trust, and the alternative
— a page that hides how it was made — is worse on every axis that
matters.

**Hyperlinks raise perceived credibility, most on value-framed claims.**
Johnson & Wiedenbeck (JCMC) found a statistically significant if small
increase in perceived credibility for stories carrying hyperlinks, and
the effect was strongest in **value-framed conditions** — where the
framing emphasises normative stakes rather than bare fact.

**Design consequence.** The claims that most need a visible source are
the ones making a normative or evaluative move, not just the ones
carrying a number. Cite the "this is worse than it should be" sentence,
not only the "it is 38%" sentence.

### Corroborating detail worth keeping

- **The double-edged sword, from practitioners.** The narrative-vis
  practitioner survey records designers describing scrollytelling as
  "overly structured", constraining freedom, with readers stopping
  halfway when the path feels long or rigid. Mitigations they name:
  keep pinned spans short, provide alternate navigation (contents or
  jump links), and **ensure core claims also exist in static sections
  outside any pinned zone**.
- **HTML-first, stated as a mantra**: every meaningful page state must
  exist as crawlable markup before the renderer ever boots. This is the
  same conclusion Codex reached via ONS's pre-rendered-HTML practice.
- **Reuse the frame *within* a page.** Many scrollers are variations on
  highlighting or transitioning inside one fixed visual frame rather
  than a new scene per step. Reusing a small number of frames across
  states aids comparison and cuts implementation cost.

  This does not contradict §10. Reuse the frame **within** a page so
  states are comparable; vary the frame **between** pages so the
  producer does not converge on one look. The two operate at different
  scopes and both are load-bearing.
- **ProPublica's rule**: make the editorial "nut" the most noticeable
  thing on the page, keep legends and labels adjacent to what they
  describe, and match the chart type to the data.
- **Under-visualised uncertainty** (Hullman): authors routinely omit it,
  and readers then read point estimates as precise. Show it where it
  exists.

## 12. Recommendations the panel made that this skill does not yet do

Recorded honestly rather than quietly dropped:

1. **Run the motion benchmark.** One report in three implementations
   (CSS timelines / IntersectionObserver / GSAP scrub), INP and
   long-task count on throttled mid-tier Android. This is the one
   decision where the literature contradicts itself and no primary
   measurement exists.
2. **Build the sameness detector.** Goree et al.'s method — grayscale and
   blurred full-page screenshots plus structural state maps, scored
   pairwise against every previous page — turns "every page must look
   different" from an unfalsifiable goal into a gate.
3. **Instrument step-level scroll telemetry.** No newsroom publishes
   per-step funnels; a producer of many topic pages is unusually well
   placed to close the field's central empirical gap.
4. **A/B the citation affordances.** Marker only vs marker+preview vs
   marker+preview+registry, measuring actual follow-through.
