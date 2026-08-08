---
title: "Design and performance standards for evidence-dense scrollytelling reports"
run_id: dr_3ff340ccb9bd5b3d
question: "How do practitioners build single-page, evidence-dense scrollytelling web reports — the narrative-visualisation form used by newsroom graphics desks and independent data-journalism sites — and what measurably works versus fails? Cover: (1) documented production patterns and narrative structures for long-form scroll-driven report pages (author-driven vs reader-driven martini-glass / interactive-slideshow / drill-down structures, section pacing, the \"one idea per scroll state\" discipline); (2) empirical findings on comprehension, recall and engagement in narrative visualisation and scrollytelling, including where animation and scroll-linked transitions measurably help understanding and where they measurably hurt; (3) citation, provenance and trust UX in evidence-dense pages — inline citation affordances, footnote/popup patterns, source-list design, and what makes readers actually verify a claim; (4) production practice for GSAP ScrollTrigger and three.js/WebGL on narrative pages: performance budgets, Core Web Vitals and INP impact, scroll-linked animation techniques, WebGL fallbacks and progressive enhancement, and when a 3D scene earns its cost versus being decoration; (5) accessibility for scroll-driven and animated content — prefers-reduced-motion, keyboard and screen-reader access to scroll-triggered content, motion-triggered vestibular disorders, and the WCAG criteria that apply; (6) the documented failure modes: scrolljacking, mobile performance collapse, unlabelled or misleading charts, visual homogeneity and template sameness across pages from one producer, and reports whose claims outrun their sources. Prioritise measured results, published post-mortems from graphics desks, and peer-reviewed narrative-visualisation research over listicles and vendor marketing."
provider: openai
model: gpt-5.6-sol
tier: max
archetype: technical
sources: 44
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 9.00
completed: 2026-08-08T04:38:12.399Z
---
## Executive Summary

- **(High Confidence)** The strongest default architecture is an **author-driven evidence spine followed by bounded reader exploration**: establish the claim, change one meaningful visual state at a time, then expose filters, drill-downs, data and methods. Segel and Heer called this the “martini-glass” structure; subsequent studies show that narration can improve immediate comprehension, but does not reliably improve long-term recall or motivate later exploration.[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf)[nzjohng.github.io](https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf)[doi.org](https://doi.org/10.1145/2702123.2702452) ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf))

- **(High Confidence)** Animation works best when it **preserves object identity, explains a state transition, directs attention or lets the reader control time**. It does not confer a general comprehension advantage: controlled studies find higher perceived engagement from animated transitions, but little or no comprehension difference; animated trend displays can be worse than static traces or small multiples for analysis.[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf)[doi.org](https://doi.org/10.1109/TVCG.2008.125) ([narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf))

- **(High Confidence)** The practical motion rule is: **animate relationships, not atmosphere**. Every scroll state should carry one nameable claim and one corresponding visual delta. `<INSUFFICIENT_EVIDENCE>[No controlled study located tests the exact phrase “one idea per scroll state”; it is best treated as an editorial production rule derived from evidence favoring staged, semantically congruent transitions.]</INSUFFICIENT_EVIDENCE>`

- **(High Confidence)** Citation UX must be **claim-local and low-friction**: an inline marker, keyboard- and touch-accessible source preview, then a persistent source/method list with full metadata and claim mappings. Merely placing sources at the bottom is not enough. Wikipedia research found citation clicks on fewer than one in 300 page loads overall, demonstrating that source availability should not be confused with source verification.[arxiv.org](https://arxiv.org/abs/2001.08614) ([meta.wikimedia.org](https://meta.wikimedia.org/wiki/Research%3AWhich_parts_of_an_article_do_readers_read?utm_source=openai))

- **(High Confidence)** GSAP ScrollTrigger is appropriate as a standing orchestration layer, provided the implementation retains native scrolling, precomputes trigger positions, confines per-frame work to transforms or render-state changes, kills unused triggers, and supplies non-motion states. ScrollTrigger itself batches scroll updates with `requestAnimationFrame`; expensive application callbacks, DOM measurement and WebGL rendering remain the producer’s responsibility.[gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) ([gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/?utm_source=openai))

- **(High Confidence)** Release budgets should be outcome-based: at the 75th percentile, **LCP ≤2.5 seconds, INP ≤200 milliseconds and CLS ≤0.1**.[web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds) A self-contained report that misses these thresholds because of inlined video, textures or JavaScript has failed, regardless of visual polish. ([web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds?authuser=5&hl=en&utm_source=openai))

- **(High Confidence)** Three.js earns inclusion only when a core claim is intrinsically spatial and changing viewpoint, depth, assembly or occlusion reveals evidence that a 2D map, diagram, cutaway or small multiple cannot communicate as clearly. Otherwise, 3D is decoration with extra GPU, accessibility, fallback and trust costs. `<INSUFFICIENT_EVIDENCE>[No peer-reviewed study establishes a universal quantitative “3D earns it” threshold; the gate below is an evidence-informed production rule.]</INSUFFICIENT_EVIDENCE>`

- **(High Confidence)** The recurring trust failures are scrolljacking, mobile-only breakage, motion without semantic purpose, inaccessible content gated behind triggers, charts without decoding or provenance, source lists that do not support individual claims, and visible reuse of the same hero–sticky-chart–sources composition. Standardize the hidden infrastructure; do not standardize the visible rhetoric.

---

## Detailed Findings

### 1. Answer this decisively: How do practitioners build single-page, evidence-dense scrollytelling web reports, and what measurably works versus fails?

#### 1.1 Narrative structures and production patterns

**(High Confidence)** Segel and Heer’s analysis of 58 narrative visualizations identified an author–reader continuum and three reusable structures: **martini glass**, **interactive slideshow** and **drill-down story**.[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf) The martini glass begins with an authored path and later opens into exploration; the slideshow allows interaction within bounded narrative stages; drill-down starts with a general theme and lets readers select individual cases. ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf))

**(High Confidence)** More recent newsroom research by Oesch, Renner and Roth classified 50 scrollytelling examples into five implementation techniques: graphic sequences, animated transitions, pan-and-zoom, movie scrollers, and show-and-play content.[doi.org](https://doi.org/10.1075/idj.22005.oes) Their operational contribution is a shared vocabulary and implementation repository, not evidence that all five techniques are equally effective. ([lwc1.benjamins.com](https://lwc1.benjamins.com/catalog/idj.22005.oes?utm_source=openai))

| Narrative structure | Author control | Reader control | Best use in an evidence report | Main failure risk | Decision |
|---|---:|---:|---|---|---|
| **Martini glass** | High initially | High after the argument | Main report spine followed by data, cases or methodology | Exploration feels bolted on or is never used | **Default** — High Confidence |
| **Interactive slideshow / discrete scroller** | High | Medium within each state | Complex transformations, comparisons requiring replay, mobile stepper fallback | Too many modal “slides”; reader loses document context | **Use for bounded explainers** — High Confidence |
| **Continuous scroll scrub** | High | Reader controls time | Spatial travel, temporal progression, construction/deconstruction | State and text desynchronize; fast scrolling makes evidence unreadable | **Use only when continuity is meaningful** — High Confidence |
| **Drill-down** | Low after entry | High | Entity backstories, regional examples, appendices, source inspection | Readers miss the main conclusion or self-select confirming cases | **Use after—not instead of—the main finding** — High Confidence |
| **Free exploration** | Low | High | Expert appendix or reusable dataset | High interaction cost; introductory story does not reliably cause exploration | **Never the sole delivery mode** — High Confidence |

**(High Confidence)** A report should alternate between **normal document flow and bounded visual episodes**. Permanently pinning the entire page sacrifices orientation, accessibility and mobile resilience. Each episode should have:

1. A prose setup that states the question.
2. An orientation state explaining the visual grammar.
3. A sequence of semantically distinct states.
4. A stable takeaway state that remains understandable without motion.
5. Optional exploration, cases, uncertainty and methods.
6. A return to ordinary document flow before the next major argument.

<INFERENCE from="Segel and Heer’s authored-to-exploratory structures; McKenna et al.’s flow results; Newsday’s mobile post-mortem">This alternating rhythm preserves the benefits of guided narration without turning the whole report into a fragile slideshow.</INFERENCE>[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf)[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)[source.opennews.org](https://source.opennews.org/articles/how-we-made-unequal-justice/) ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf))

**(Medium Confidence)** The agent-executable form of “one idea per scroll state” should be:

- Every state has one `claim_id`.
- The caption can summarize the state in one sentence.
- The visual delta changes only the encodings needed to support that claim.
- Objects that represent the same records retain identity across states.
- A new chart grammar and a new substantive finding are not introduced simultaneously unless the transition itself explains their relationship.
- Reverse scrolling restores the prior state correctly.
- If the caption contains two independent propositions, split the state.

<INFERENCE from="Heer and Robertson’s findings on meaningful, staged transitions; Zhi et al.’s results for linked text and visualization">This is a production discipline rather than a measured optimum, but it directly operationalizes semantic congruence and text–visual linking.</INFERENCE>[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf)[visualdata.wustl.edu](https://visualdata.wustl.edu/files/linking.pdf) ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf))

<MISSING_DATA>[An empirically optimal number of states, words per step or viewport-heights per chapter was sought. No generalizable value was found; topic complexity, device height, chart literacy and interaction type confound a universal threshold.]</MISSING_DATA>

#### 1.2 What measured studies say about comprehension, recall and engagement

| Study | Design | Measured result | What it supports | Confidence |
|---|---|---|---|---|
| McKenna et al., 2017 | Crowdsourced study, **240 participants**[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf) | Visual and animated conditions had higher perceived engagement; animated transitions beat static visuals at `p<.001`, but average comprehension was about **4/5 with no major condition differences**.[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf) | Animation may improve engagement without improving comprehension. Scroller versus stepper was inconclusive. | High ([narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)) |
| Zhi, Ottley & Metoyer, 2019 | Crowdsourced study, **180 participants**[visualdata.wustl.edu](https://visualdata.wustl.edu/files/linking.pdf) | Slideshow layout produced better comprehension; text–visual linking increased engagement, and improved recall in the linked slideshow condition.[visualdata.wustl.edu](https://visualdata.wustl.edu/files/linking.pdf) | Explicitly connect prose to the marks or region that supports it. | High ([vispubs.com](https://vispubs.com/?paper=10.1111%2Fcgf.13719&utm_source=openai)) |
| Obie et al., 2019 | Controlled within-subject study, **40 participants**[nzjohng.github.io](https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf) | Author narration improved value-message comprehension (`p=.04`) and short-term fact recall (`p=.04`), but not long-term fact or value-message recall.[nzjohng.github.io](https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf) | Use narration to establish the argument, but reinforce durable takeaways with stable summaries and repetition. | Medium–High ([nzjohng.github.io](https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf)) |
| Boy, Detienne & Fekete, 2015 | Three web field experiments | Introductory stories did not increase later exploration. In two follow-ups, only **40.9%** and **41.5%** of qualifying sessions traversed all narrative sections linearly.[doi.org](https://doi.org/10.1145/2702123.2702452) | Do not assume that narrative automatically produces exploration or linear completion. | High ([researchgate.net](https://www.researchgate.net/publication/278381124_Storytelling_in_Information_Visualizations_Does_it_Engage_Users_to_Explore_Data)) |
| Heer & Robertson, 2007 | Two controlled experiments, **24 participants**[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf) | Carefully designed transitions reduced object-tracking and change-estimation error. Simple transitions around **one second** were favored; complex staging could create new errors.[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf) | Animate related states, retain landmarks and use simple staging. | Medium–High ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf)) |
| Robertson et al., 2008 | Comparison of animation, traces and small multiples | Animation was enjoyable and fast for presentation, but caused errors; for analysis it was least effective, while static views were faster and small multiples more accurate.[doi.org](https://doi.org/10.1109/TVCG.2008.125) | Use motion to present change; provide static views for comparison and analysis. | High ([yonsei.elsevierpure.com](https://yonsei.elsevierpure.com/en/publications/effectiveness-of-animation-in-trend-visualization/?utm_source=openai)) |
| Rogha et al., 2024 | Two experiments on news articles with visualization | Contrasting narratives increased surprise and interest but also increased recall error and did not significantly change attitudes.[doi.org](https://doi.org/10.1109/TVCG.2024.3355884) | Suspense, contrast and surprise can raise engagement while degrading factual memory. | High ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/38241101/)) |
| Méndez & Such, 2026 | Online comparison, **454 participants**[arxiv.org](https://arxiv.org/abs/2603.04367) | Privacy-policy scrollytelling improved perceived engagement, clarity and cognitive load versus text, while comprehension remained similar and trust changes were statistically inconclusive.[arxiv.org](https://arxiv.org/abs/2603.04367) | Recent evidence reinforces an experience benefit, not a general truth or comprehension benefit. | Medium; domain-specific preprint/CHI work ([arxiv.org](https://arxiv.org/abs/2603.04367?utm_source=openai)) |

**(High Confidence)** The measured pattern is therefore not “scrollytelling works.” It is:

- **Guided narration can improve immediate interpretation.**
- **Text–visual linking can improve comprehension and engagement.**
- **Semantically designed animation can improve perception of change.**
- **Animation often increases perceived novelty or engagement.**
- **Scroll input is not measurably superior to button-driven progression in the available comparative evidence.**
- **Long-term recall, attitude change and self-directed exploration do not reliably improve.**

<CONFLICTING_EVIDENCE>[Heer and Robertson found perceptual benefits for transitions between related chart states, while Robertson et al. found animated trend displays inferior to static alternatives for analysis. The disagreement is functional rather than methodological: animation helps track a controlled transformation, but ephemeral animation makes simultaneous comparison harder.]</CONFLICTING_EVIDENCE>

<INFERENCE from="McKenna et al.; Heer and Robertson; Robertson et al.; Rogha et al.">The correct motion budget is semantic: spend motion where it removes change blindness or gives the reader control of time; use persistent static views where the task is comparison, verification or recall.</INFERENCE>

#### 1.3 Citation, provenance and trust UX

**(High Confidence)** Source attribution affects perceived credibility, but readers partly evaluate the source’s reputation rather than independently verifying the data. In an experiment with **517 participants**, Li, Brossard, Scheufele, Wilson and Rose found credibility judgments varied with source attribution and prior trust in the named source.[jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/) This means a prestigious source label is a credibility cue, not proof that the report’s claim accurately represents that source. ([jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/?utm_source=openai))

**(High Confidence)** Metadata is goal-specific. In one experiment, **64 participants** most wanted encoding explanations when trying to understand a chart and source metadata when judging trust; a second experiment with **144 participants** found metadata made visualizations appear more thorough but did not improve extraction accuracy.[pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/37015379/) ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/37015379/?utm_source=openai))

**(High Confidence)** Verification is rare. A large Wikipedia citation study reported an overall external-reference click-through rate of **0.29%**, with **0.56% on desktop** and **0.13% on mobile**; **93% of cited URLs** received no click during the collection month.[arxiv.org](https://arxiv.org/abs/2001.08614) The result has limited external validity for bespoke reports, but decisively shows that the presence of footnotes does not mean readers inspect them. ([researchgate.net](https://www.researchgate.net/publication/338789479_Quantifying_Engagement_with_Citations_on_Wikipedia?utm_source=openai))

**(High Confidence)** Use a three-layer citation interface:

1. **Inline claim marker:** adjacent to the smallest claim span the source supports—not attached to a whole paragraph with several propositions.
2. **Preview:** available by hover, keyboard focus and tap; show title, author or organization, date, evidence type, the supported claim and a direct source action.
3. **Persistent source record:** full bibliographic metadata, method or dataset notes, access date, original and archived locations where applicable, and backlinks to every claim using that source.

<INFERENCE from="low citation click rates; users’ metadata preferences; source-attribution effects">The preview should answer “what is this, why is it credible, and which claim does it support?” without requiring navigation, while the full source remains available for actual verification.</INFERENCE>[arxiv.org](https://arxiv.org/abs/2001.08614)[pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/37015379/)[jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/) ([researchgate.net](https://www.researchgate.net/publication/338789479_Quantifying_Engagement_with_Citations_on_Wikipedia?utm_source=openai))

**(High Confidence)** A bibliography-only design is inadequate for evidence-dense reports because it fails to preserve claim–source integrity. Practitioner research also found strong agreement that data sources and methodology should be disclosed, not just the publication title.[pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10064970/) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10064970/?utm_source=openai))

**Recommended internal provenance contract**

| Record | Required fields | Release failure |
|---|---|---|
| Claim | `claim_id`, exact text, confidence, section, `source_ids`, support type: direct/inference/contested | Claim has no source or inference chain |
| Source | `source_id`, authors/org, title, publisher, date, URL, evidence type, access date | Missing author/date/URL without an explicit `UNVERIFIED` state |
| Support edge | `claim_id`, `source_id`, locator/page/table, support summary, direct/partial/contradictory | Source is relevant to topic but does not support the exact claim |
| Chart | `chart_id`, dataset sources, transformations, exclusions, units, uncertainty, claim IDs | Chart provenance exists only in a global source list |
| Inference | conclusion, parent claim IDs, reasoning step, confidence | Synthesized conclusion is presented as an empirical finding |

<INFERENCE from="the distinction between source visibility, source credibility and claim support">The report generator should compile from this claim graph; citations should not be retrofitted after prose and visuals are complete.</INFERENCE>

#### 1.4 GSAP ScrollTrigger, performance and three.js/WebGL

**(High Confidence)** ScrollTrigger performs substantial setup work up front, tracks scroll position rather than repeatedly measuring every trigger, debounces scroll events, and updates on the next animation frame.[gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) That optimization does not protect a page from expensive `onUpdate` handlers, synchronous layout reads, React rerenders, unbounded canvas draws or continuous WebGL loops. ([gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/?utm_source=openai))

##### Release performance floor

| Metric | “Good” threshold at p75 | Scrollytelling-specific risk | Release response |
|---|---:|---|---|
| LCP | **≤2.5 s**[web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds) | Hero video, poster image, fonts, giant inline SVG or WebGL initialization | Render headline and primary evidence without waiting for nonessential motion |
| INP | **≤200 ms**[web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds) | Heavy scroll callbacks, citation drawers, filter operations, texture decoding | Profile handlers and long tasks; move calculations off the hot path |
| CLS | **≤0.1**[web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds) | Late chart sizing, font swaps, pin spacers, image dimensions | Reserve geometry; refresh triggers only after deterministic layout |

([web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds?authuser=5&hl=en&utm_source=openai))

<MISSING_DATA>[No universal JavaScript-kilobyte, texture-memory, polygon-count or number-of-ScrollTriggers budget is supported across newsroom topics and device populations. Define project budgets from a representative device matrix and enforce the Core Web Vitals outcomes above.]</MISSING_DATA>

**(High Confidence)** GSAP implementation rules for the skill:

- Build one timeline per visual episode instead of unrelated tweens competing over the same state.
- Use `scrub` only when continuous progress itself encodes time, distance, assembly or another meaningful variable.
- Use discrete triggers for categorical claims and state changes.
- Do not animate the pinned element itself; animate children so ScrollTrigger’s measurements stay valid.[gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)
- Use `gsap.matchMedia()` for viewport and reduced-motion branches; it automatically reverts created animations when a condition stops matching.[gsap.com](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29/)
- Use `once: true` or explicitly kill one-shot triggers.
- Pause canvas and WebGL rendering when the scene is offscreen.
- Refresh after fonts, images and chart dimensions settle—not repeatedly during scroll.
- Retain native wheel, touch, scrollbar and keyboard behavior. ScrollTrigger’s documentation explicitly distinguishes the tool from scrolljacking.[gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)

([gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/?utm_source=openai))

**(Medium Confidence)** A self-contained report should mean **one complete semantic document**, not necessarily one enormous physical HTML file. <INFERENCE from="Core Web Vitals thresholds and the Washington Post’s documented 30 MB image problem">Base64-inlining heavy video, textures and image sequences is counterproductive; critical text, CSS, data and static fallbacks may be embedded, while large media should be compressed, responsive and lazy-loaded unless a literal one-file requirement overrides performance.</INFERENCE>[source.opennews.org](https://source.opennews.org/articles/how-we-made-washington-post-eclipse-scroller/)[web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds) ([source.opennews.org](https://source.opennews.org/articles/how-we-made-washington-post-eclipse-scroller/?utm_source=openai))

##### The three.js “earns its place” gate

**All three evidence tests must pass:**

1. **Spatial claim:** a major claim depends on depth, volume, orientation, topology, occlusion, assembly or movement through physical space.
2. **Viewpoint necessity:** changing viewpoint reveals evidence rather than merely showcasing an object.
3. **2D insufficiency:** a map, cutaway, orthographic diagram, annotated image, animation or small multiple cannot communicate the claim at least as clearly.

**All three release tests must also pass:**

4. **Narrative mapping:** every camera or object transition maps to a claim ID; there is no decorative idle orbit.
5. **Equivalent fallback:** static images, diagrams and text communicate the same conclusion without WebGL.
6. **Performance/accessibility:** the scene passes the page’s CWV/device matrix and fully disables nonessential camera motion under reduced-motion preferences.

<INFERENCE from="animation’s benefits when preserving semantic relationships; its costs when ephemeral or decorative; WebGL’s additional rendering lifecycle">If any evidence test fails, reject three.js. If a release test fails, ship the fallback until it passes.</INFERENCE>[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf)[doi.org](https://doi.org/10.1109/TVCG.2008.125)[threejs.org](https://threejs.org/docs/pages/WebGLRenderer.html) ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf))

**(High Confidence)** When three.js is approved:

- Feature-detect WebGL and render the fallback when unavailable.[threejs.org](https://threejs.org/docs/pages/WebGL.html)
- Use the renderer’s supported animation loop API rather than building an unrelated loop.[threejs.org](https://threejs.org/docs/pages/WebGLRenderer.html)
- Stop rendering when no visual state is changing.
- Dispose scene resources and renderer state when leaving or replacing a scene.
- Avoid encoding essential labels only as textures or in the canvas.
- Keep the semantic transcript, source links and data outside the canvas in normal DOM order.

([threejs.org](https://threejs.org/docs/pages/WebGLRenderer.html?utm_source=openai))

#### 1.5 Accessibility floor

**(High Confidence)** WCAG 2.2 is the appropriate current baseline. The most directly applicable criteria include Meaningful Sequence, Keyboard, Pause/Stop/Hide, Three Flashes or Below Threshold, Animation from Interactions, Focus Order, Focus Visible, Focus Not Obscured, non-text contrast, and Name/Role/Value.[w3.org](https://www.w3.org/TR/WCAG22/) ([w3.org](https://www.w3.org/TR/WCAG22/?utm_source=openai))

| Requirement | Applicable WCAG concern | Build rule |
|---|---|---|
| Scroll-triggered text or charts | 1.3.1, 1.3.2, 2.1.1 | All evidence exists in logical DOM order and remains readable without trigger execution |
| Pinned/sticky sections | 1.3.2, 2.4.3, 2.4.11 | Pinning must not change reading or focus order or obscure focused controls |
| Autonomous or scroll-initiated motion | 2.2.2 Level A; potentially 2.3.3 | Provide pause/stop/hide where the criterion applies; reduced motion should replace camera travel, parallax and large transforms |
| Interactive chart controls | 2.1.1, 2.4.7, 4.1.2 | Native controls where possible; visible focus; programmatic name, role, state and value |
| Color encodings | 1.4.1, 1.4.3, 1.4.11 | Never communicate category, direction, certainty or selection by color alone |
| Citation popovers | 1.4.13, 2.1.1, 2.4.3 | Open on focus and tap as well as hover; dismissible without moving focus unpredictably |
| Canvas/WebGL | 1.1.1, 1.3.1 | Provide prose summary, static visual alternative and accessible data or transcript |
| Flashing | 2.3.1 | No effect that breaches the flash threshold; reduced motion is not a substitute |

**(High Confidence)** WCAG 2.2’s explanation of 2.2.2 states that moving content triggered by general interaction such as scrolling may fail when it runs for more than five seconds alongside other content without pause, stop or hide controls.[w3.org](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) Animation from Interactions is Level AAA, but relying on that distinction is unsafe because scroll-triggered movement may also fall under the Level A requirement depending on behavior. ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html?utm_source=openai))

**(High Confidence)** `prefers-reduced-motion` is necessary but not sufficient. The reduced branch must preserve every fact and interaction while replacing:

- Parallax with fixed positioning.
- Camera travel with cuts or annotated stills.
- Scrubbed morphs with discrete states.
- Large zooms and depth movement with opacity or immediate replacement.
- Infinite particles or ambient loops with static composition.

<INFERENCE from="WCAG motion criteria and the need to preserve equivalent information">Reduced motion should be designed as a first-class narrative mode, not implemented by setting every duration to zero after the page has been authored.</INFERENCE>

**(High Confidence)** Screen readers should not receive an `aria-live` announcement for every scroll state. <INFERENCE from="meaningful sequence, focus-order and name/role/value requirements">The stable prose should carry the narrative; live regions should be reserved for deliberate control actions whose results would otherwise be unavailable.</INFERENCE>

#### 1.6 Documented failure modes

| Failure | Evidence or mechanism | Why it makes the page untrustworthy | Prevention |
|---|---|---|---|
| **Scrolljacking or nested page scrolling** | Newsday used an inner scrolling container to stabilize mobile browser bars, but documented clipped text and disabled effects on smaller screens.[source.opennews.org](https://source.opennews.org/articles/how-we-made-unequal-justice/) | Readers lose expected controls; content can be inaccessible or appear missing | Keep document scrolling native; use sticky/pinned enhancement only |
| **Mobile performance collapse** | The Washington Post eclipse project faced an image load of **30 MB or more** before adopting lazy loading and thumbnails under **10 KB**.[source.opennews.org](https://source.opennews.org/articles/how-we-made-washington-post-eclipse-scroller/) | Mobile readers receive a materially worse or unusable report | Responsive assets, lazy loading, poster fallbacks, device testing |
| **Text trapped in pinned states** | Newsday reported that browser-bar changes altered viewport height and cut off non-scrolling text.[source.opennews.org](https://source.opennews.org/articles/how-we-made-unequal-justice/) | Evidence is available only at particular viewport dimensions | Keep explanatory text free-scrolling or provide a static narrow-screen mode |
| **Animation implying false continuity** | Heer and Robertson warn that unrelated objects transformed into one another can imply a false relationship.[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf) | Motion becomes an unsupported causal or identity claim | Preserve semantic identity; cut rather than morph unrelated marks |
| **Engagement mistaken for learning** | Animated narrative flow increased engagement without a major comprehension difference; contrasting narratives increased interest but worsened recall error.[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)[doi.org](https://doi.org/10.1109/TVCG.2024.3355884) | A page feels persuasive while readers remember less accurately | Evaluate comprehension and recall separately from dwell time or novelty |
| **Charts without decoding or provenance** | Users sought encoding metadata for understanding and source metadata for trust.[pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/37015379/) | Readers cannot tell what marks mean, what was transformed or whether the source supports the claim | Direct labels, units, denominators, uncertainty, source and method at chart level |
| **Bibliography without claim mapping** | Citation usage is extremely low even when sources are present.[arxiv.org](https://arxiv.org/abs/2001.08614) | The report appears sourced but individual claims remain unverifiable | Inline claim citations, source previews and bidirectional claim/source links |
| **Template sameness** | A Washington Post post-mortem explicitly warned against copying a successful interactive instead of seeking an approach appropriate to the next story.[source.opennews.org](https://source.opennews.org/articles/how-we-made-behind-bloodshed/) | Repeated composition signals that design preceded evidence | Standardize components and tests, not page composition or visual metaphor |
| **Claims outrunning sources** | Source attribution can raise credibility independently of comprehension.[jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/) | Prestigious citations can launder an inference or unsupported extrapolation | Claim-source coverage tests and explicit inference chains |

([source.opennews.org](https://source.opennews.org/articles/how-we-made-unequal-justice/?utm_source=openai))

<INSUFFICIENT_EVIDENCE>[No controlled research was located that quantifies how much repeated visual structure makes one producer’s reports seem templated. The failure is documented qualitatively by practitioners, but a measurable homogeneity threshold is unavailable.]</INSUFFICIENT_EVIDENCE>

<INFERENCE from="NZZ’s reusable technique vocabulary and the Washington Post’s warning against copying prior success">The correct system boundary is: standardize the content model, provenance graph, accessibility components, performance harness and motion APIs; derive the visible composition, material language, illustration style and transition metaphor from each subject.</INFERENCE>

A build agent can enforce that distinction with a **theme-proof test**:

- Every major visual choice must map to a named concept in the topic corpus.
- Random palettes, generic particle fields and interchangeable dark “cinematic” heroes fail.
- At least one major composition, illustration system or transition metaphor must be topic-specific.
- Reusing citation drawers, focus styles, grid utilities and test infrastructure is encouraged.
- Reusing the same hero, sticky center graphic, alternating text cards and final source wall is rejected unless the content independently calls for it.

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** The current state is a mature production form with a weaker empirical base than its prevalence suggests. Practitioners have stable vocabularies and tooling, but measured results remain conditional: the evidence is strongest for **guidance, text–visual linking, perception of state changes and engagement**, and weaker for **long-term recall, persuasion, trust improvement or increased exploration**.[doi.org](https://doi.org/10.1075/idj.22005.oes)[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)[visualdata.wustl.edu](https://visualdata.wustl.edu/files/linking.pdf) ([lwc1.benjamins.com](https://lwc1.benjamins.com/catalog/idj.22005.oes?utm_source=openai))

**(High Confidence)** The recommended stack for the proposed Claude Code skill is:

| Layer | Build vs. adopt | Decision | Reason |
|---|---|---|---|
| Semantic report document | Build | Compile one accessible HTML narrative with ordinary headings, prose, tables and sources | The no-JS document must remain complete and citable |
| Claim/provenance graph | Build | First-class structured data, not generated footnotes | Prevents claims from outrunning evidence |
| Narrative planner | Build | Select martini glass, stepper, scrub or drill-down per argument | A single template is editorially and visually inadequate |
| Static visualization layer | Build or use focused chart primitives | SVG for labelled marks; Canvas for high mark counts | Static evidence and accessibility come before motion |
| Motion orchestration | Adopt GSAP ScrollTrigger | Standing layer, activated only where a semantic transition exists | Mature trigger, pin, scrub and responsive lifecycle APIs |
| 3D | Adopt three.js conditionally | Instantiate only after the six-part gate passes | Avoid unnecessary GPU and fallback costs |
| Citation UI | Build | Inline markers, previews, source drawer/list and claim backlinks | Existing generic footnote components rarely encode claim coverage |
| Accessibility harness | Build | Keyboard, reduced motion, focus, no-JS and screen-reader checks | Must test the compiled narrative, not just components |
| Performance harness | Build around browser tooling/RUM | CWV plus representative low- and mid-tier mobile tests | Library-level optimization does not ensure page-level performance |
| Visible theme | Generate from subject, then editorially validate | No fixed page skin | Distinctiveness must be semantic, not random |

<INFERENCE from="the measured narrative structures, GSAP’s documented behavior, WCAG and source-integrity evidence">This is a build-the-editorial-compiler/use-the-runtime-libraries decision: the valuable proprietary layer is the system that maps evidence to claims, claims to narrative states, and narrative states to topic-specific visual rhetoric.</INFERENCE>

**(High Confidence)** The minimum compiled state record should be:

| Field | Purpose |
|---|---|
| `state_id` | Stable scroll/step state |
| `claim_id` | Claim supported by the state |
| `visual_delta` | Exact marks/properties that change |
| `trigger_mode` | `discrete`, `scrub`, `manual`, `none` |
| `entry_action` / `exit_action` | Reversible transition behavior |
| `reduced_motion_state` | Complete non-motion equivalent |
| `fallback_asset` | Static SVG/image/HTML alternative |
| `source_ids` | Evidence supporting both caption and chart |
| `accessible_summary` | Prose interpretation independent of rendering |
| `performance_class` | DOM/SVG, Canvas, WebGL, video or image sequence |

**(Medium Confidence)** No team size was specified. `<MISSING_DATA>[A precise build-versus-buy recommendation by staffing level requires the number of editors, designers and engineers; publishing frequency; browser support; and whether literal single-file output is mandatory.]</MISSING_DATA>`

---

### 3. What are the contrasting viewpoints or competing evidence?

**(High Confidence)** The major disagreement is not whether motion is “good” or “bad,” but **which cognitive task it serves**.

<CONFLICTING_EVIDENCE>[McKenna et al. found animated transitions increased perceived engagement, and Heer and Robertson found perceptual benefits for related chart transitions. Robertson et al. found animation inferior to static alternatives for trend analysis. The practical resolution is to use motion for change tracking and static views for comparison.]</CONFLICTING_EVIDENCE>[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)[idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf)[doi.org](https://doi.org/10.1109/TVCG.2008.125) ([narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf))

**(High Confidence)** Author-driven narration also has a bounded advantage.

<CONFLICTING_EVIDENCE>[Obie et al. found better value-message comprehension and short-term fact recall from author narration, while Boy et al. found that introductory stories did not increase subsequent exploratory engagement. Narration can help readers understand what the author means without making them more likely to explore independently.]</CONFLICTING_EVIDENCE>[nzjohng.github.io](https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf)[doi.org](https://doi.org/10.1145/2702123.2702452) ([nzjohng.github.io](https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf))

**(High Confidence)** Scroll is familiar and discoverable, but continuous control is not proven superior.

<CONFLICTING_EVIDENCE>[McKenna et al. found no significant engagement difference between stepper and scroller conditions and documented individual frustration when text and transitions did not align. Zhi et al. found better comprehension in a slideshow layout. Scroll should therefore be a delivery mechanism, not an ideological requirement.]</CONFLICTING_EVIDENCE>[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)[visualdata.wustl.edu](https://visualdata.wustl.edu/files/linking.pdf) ([narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf))

**(High Confidence)** More provenance does not automatically create more trust or understanding.

<CONFLICTING_EVIDENCE>[Source attribution and metadata can increase credibility or perceived thoroughness, yet metadata did not improve extraction accuracy in the cited study, and a 2026 study found that displaying reliability information could reduce map trust, accuracy and confidence. Transparency can appropriately reduce confidence when it reveals uncertainty, but poor uncertainty encodings can also impair interpretation.]</CONFLICTING_EVIDENCE>[jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/)[pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/37015379/)[doi.org](https://doi.org/10.1177/14738716251398423) ([jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/?utm_source=openai))

**(High Confidence)** Engagement is an insufficient success metric.

<CONFLICTING_EVIDENCE>[Animation, novelty and contrasting narratives can increase interest, surprise or aesthetic engagement while leaving comprehension unchanged or increasing recall error. Dwell time, completion and interaction counts must not be reported as evidence of learning without separate comprehension or recall measures.]</CONFLICTING_EVIDENCE>[narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)[doi.org](https://doi.org/10.1109/TVCG.2024.3355884) ([narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf))

---

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** Since 2019, newsroom practice has moved from one-off “special project” mechanics toward **named, reusable scrollytelling primitives**. NZZ’s 2022 taxonomy and repository exemplify the trajectory: shared techniques reduce implementation cost while allowing different editorial combinations.[doi.org](https://doi.org/10.1075/idj.22005.oes) ([lwc1.benjamins.com](https://lwc1.benjamins.com/catalog/idj.22005.oes?utm_source=openai))

**(High Confidence)** The empirical trajectory has become more skeptical of equating narrative intensity with effectiveness. The 2024 Rogha et al. study found increased interest and surprise alongside greater recall error, while 2026 scrollytelling research on privacy policies found better experience and lower perceived cognitive load without a corresponding comprehension or trust improvement.[doi.org](https://doi.org/10.1109/TVCG.2024.3355884)[arxiv.org](https://arxiv.org/abs/2603.04367) ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/38241101/))

**(High Confidence)** Performance evaluation now centers on responsiveness as well as loading and layout stability: the current Core Web Vitals set is LCP, INP and CLS, with the p75 thresholds stated above.[web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds) This makes heavy scroll callbacks and interactive source/chart controls first-class performance concerns, not merely animation polish. ([web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds?authuser=5&hl=en&utm_source=openai))

**(High Confidence)** Accessibility interpretation has also become less permissive toward scroll-triggered movement. WCAG 2.2’s guidance explicitly notes that movement begun by general interactions such as scrolling may require pause, stop or hide controls under 2.2.2, and may implicate Animation from Interactions.[w3.org](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html?utm_source=openai))

**(Medium Confidence)** The trajectory for high-quality reports is therefore toward:

- Native document scrolling with isolated enhanced episodes.
- Fewer but more semantically explicit transitions.
- Static analytical views alongside animated explanatory views.
- Claim-level provenance rather than bibliography-level sourcing.
- Reduced-motion and non-WebGL states authored from the beginning.
- Reusable production infrastructure paired with subject-specific visual systems.
- Performance gates based on field outcomes, not assumptions about a library being “fast.”

<INFERENCE from="the recent empirical studies, NZZ production taxonomy, current CWV and WCAG guidance">The premium differentiator is shifting from the presence of motion to the editorial precision with which motion, evidence and provenance are connected.</INFERENCE>

---

## Evidence Table

The Evidence Type column also states why each source met the source-discipline criteria. Promotional listicles and vendor showcase pages were discarded; vendor documentation is used only for the vendor’s own runtime behavior.

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---|---|---|
| (High) Martini glass, interactive slideshow and drill-down are foundational narrative structures | Segel & Heer, *Narrative Visualization: Telling Stories with Data* ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf)) | 2010 | Peer-reviewed foundational design-space analysis of 58 real examples; directly defines the structures | https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf |
| (High) Newsroom scrollytelling can be represented by five production techniques | Oesch, Renner & Roth, *Scrolling into the Newsroom* ([lwc1.benjamins.com](https://lwc1.benjamins.com/catalog/idj.22005.oes?utm_source=openai)) | December 9, 2022 | Peer-reviewed newsroom design research analyzing 50 published scrollers | https://doi.org/10.1075/idj.22005.oes |
| (High) Animated transitions increased perceived engagement but not comprehension | McKenna et al., *Visual Narrative Flow* ([narrative-flow.github.io](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)) | 2017 | Peer-reviewed crowdsourced experiment with 240 participants | https://narrative-flow.github.io/paper/visual-narrative-flow.pdf |
| (High) Slideshow layout and text–visual linking can improve comprehension, recall or engagement | Zhi, Ottley & Metoyer, *Linking and Layout* ([vispubs.com](https://vispubs.com/?paper=10.1111%2Fcgf.13719&utm_source=openai)) | 2019 | Peer-reviewed controlled comparison with 180 participants | https://visualdata.wustl.edu/files/linking.pdf |
| (Medium–High) Author narration improved immediate comprehension and short-term recall but not long-term recall | Obie et al., *Effects of Narration on Comprehension and Memorability* ([nzjohng.github.io](https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf)) | April 2019 | Peer-reviewed controlled within-subject study; direct measures of accuracy and recall | https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf |
| (High) Introductory stories did not increase subsequent exploration | Boy, Detienne & Fekete, *Storytelling in Information Visualizations* ([researchgate.net](https://www.researchgate.net/publication/278381124_Storytelling_in_Information_Visualizations_Does_it_Engage_Users_to_Explore_Data)) | 2015 | Peer-reviewed CHI paper reporting three real-world web field experiments | https://doi.org/10.1145/2702123.2702452 |
| (Medium–High) Well-designed animation improves tracking between related chart states | Heer & Robertson, *Animated Transitions in Statistical Data Graphics* ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf)) | 2007 | Peer-reviewed controlled experiments; foundational animation evidence | https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf |
| (High) Animated trends can underperform static traces and small multiples for analysis | Robertson et al., *Effectiveness of Animation in Trend Visualization* ([yonsei.elsevierpure.com](https://yonsei.elsevierpure.com/en/publications/effectiveness-of-animation-in-trend-visualization/?utm_source=openai)) | November 2008 | Peer-reviewed comparative experiment; directly tests presentation and analysis tasks | https://doi.org/10.1109/TVCG.2008.125 |
| (High) Contrasting narratives can increase interest while worsening recall error | Rogha et al., *Impact of Elicitation and Contrasting Narratives* ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/38241101/)) | June 27, 2024 online; July 2024 issue | Peer-reviewed two-experiment study in IEEE TVCG | https://doi.org/10.1109/TVCG.2024.3355884 |
| (Medium) Scrollytelling improved privacy-policy experience but not comprehension or trust | Méndez & Such, *Scrollytelling as an Alternative Format for Privacy Policies* ([arxiv.org](https://arxiv.org/abs/2603.04367?utm_source=openai)) | March 4, 2026 preprint | Current direct scrollytelling experiment with 454 participants; domain-specific, so external validity is bounded | https://arxiv.org/abs/2603.04367 |
| (High) Source attribution affects perceived visualization credibility | Li et al., *Communicating Data* ([jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/?utm_source=openai)) | 2018 | Peer-reviewed experiment with 517 participants; directly manipulates source attribution | https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/ |
| (High) Encoding metadata supports understanding goals; source metadata supports trust goals | *From Invisible to Visible: Impacts of Metadata in Communicative Data Visualization* ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/37015379/?utm_source=openai)) | 2024 | Peer-reviewed two-experiment study; directly tests metadata preferences and effects | https://pubmed.ncbi.nlm.nih.gov/37015379/ |
| (High) Citation verification is rare even when references are available | Redi et al., *Quantifying Engagement with Citations on Wikipedia* ([researchgate.net](https://www.researchgate.net/publication/338789479_Quantifying_Engagement_with_Citations_on_Wikipedia?utm_source=openai)) | April 2020 | Large-scale behavioral log study; primary click and hover data rather than self-report | https://arxiv.org/abs/2001.08614 |
| (High) Practitioners regard source and methodology disclosure as core trust requirements | *Evaluating Narrative Visualization: A Survey of Practitioners* ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10064970/?utm_source=openai)) | 2023 | Peer-reviewed practitioner research; directly reports professional evaluation criteria | https://pmc.ncbi.nlm.nih.gov/articles/PMC10064970/ |
| (High) ScrollTrigger precomputes positions and batches updates with animation frames | GSAP ScrollTrigger documentation ([gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/?utm_source=openai)) | Living documentation; accessed August 8, 2026 | Primary vendor technical documentation; used only for GSAP behavior and APIs | https://gsap.com/docs/v3/Plugins/ScrollTrigger/ |
| (High) Good CWV thresholds are LCP ≤2.5s, INP ≤200ms and CLS ≤0.1 at p75 | Google web.dev, *How the Core Web Vitals metrics thresholds were defined* ([web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds?authuser=5&hl=en&utm_source=openai)) | Living guidance; accessed August 8, 2026 | First-party technical performance guidance defining the metrics | https://web.dev/articles/defining-core-web-vitals-thresholds |
| (High) Scroll-triggered movement may require pause, stop or hide controls | W3C, WCAG 2.2 and Understanding 2.2.2 ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html?utm_source=openai)) | October 5, 2023 Recommendation; current guidance accessed August 8, 2026 | Authoritative accessibility standard and normative supporting guidance | https://www.w3.org/TR/WCAG22/ |
| (High) three.js provides WebGL detection, renderer lifecycle and supported animation-loop APIs | Three.js documentation ([threejs.org](https://threejs.org/docs/pages/WebGLRenderer.html?utm_source=openai)) | Living documentation; accessed August 8, 2026 | Primary project documentation; used only for renderer behavior and lifecycle | https://threejs.org/docs/pages/WebGLRenderer.html |
| (High) Mobile scroll layouts can suffer viewport jumps, clipping and fixed-position stutter | Newsday/OpenNews, *How We Made Unequal Justice* ([source.opennews.org](https://source.opennews.org/articles/how-we-made-unequal-justice/?utm_source=openai)) | 2018 | First-person newsroom engineering post-mortem documenting observed failures and fallback | https://source.opennews.org/articles/how-we-made-unequal-justice/ |
| (High) Image-heavy scrollers can create extreme payloads without responsive loading | Washington Post/OpenNews, *How We Made the Eclipse-Scroller* ([source.opennews.org](https://source.opennews.org/articles/how-we-made-washington-post-eclipse-scroller/?utm_source=openai)) | 2017 | First-person graphics-desk post-mortem with concrete asset-size evidence | https://source.opennews.org/articles/how-we-made-washington-post-eclipse-scroller/ |
| (Medium) Producers warn against copying a prior interactive instead of designing for the story | Washington Post/OpenNews, *How We Made Behind the Bloodshed* ([source.opennews.org](https://source.opennews.org/articles/how-we-made-behind-bloodshed/?utm_source=openai)) | 2013 | First-person newsroom post-mortem; qualitative evidence retained as foundational practice | https://source.opennews.org/articles/how-we-made-behind-bloodshed/ |

---

## Knowledge Gaps

### Evidence scarcity

- `<MISSING_DATA>[Controlled studies of complete newsroom-style scrollytelling reports measuring comprehension, delayed recall, trust and source verification together are scarce. Most studies isolate one layout, transition or topic.]</MISSING_DATA>`
- `<MISSING_DATA>[No generalizable optimum was found for words per step, state count, viewport length, pin duration or chapter count.]</MISSING_DATA>`
- `<INSUFFICIENT_EVIDENCE>[The exact “one idea per scroll state” formulation is a defensible production heuristic, but not a directly validated law.]</INSUFFICIENT_EVIDENCE>`
- `<MISSING_DATA>[No quantitative threshold was found for when 3D provides enough explanatory gain to offset its performance and accessibility costs.]</MISSING_DATA>`
- `<INSUFFICIENT_EVIDENCE>[No controlled evidence was found for a measurable visual-template-sameness threshold.]</INSUFFICIENT_EVIDENCE>`

### External-validity limits

- Results from Wikipedia citation behavior may not transfer directly to a bespoke evidence report with more prominent citation previews.
- Studies using machine-learning explainers, medical stories or privacy policies may not generalize to every investigative, scientific or commercial subject.
- Laboratory chart-transition studies do not reproduce weak mobile GPUs, browser chrome changes, interruption, multitasking or low-bandwidth conditions.

### Technical volatility

- `<MISSING_DATA>[A current cross-browser matrix for every combination of sticky positioning, nested transforms, ScrollTrigger pinning, screen zoom and assistive technology was outside the verified source set.]</MISSING_DATA>`
- `<MISSING_DATA>[Current GSAP redistribution terms and the exact license obligations for every deployment configuration were not independently evaluated; consult the official licenses before packaging dependencies into generated reports.]</MISSING_DATA>`
- Universal WebGL polygon, texture and memory budgets remain device- and scene-dependent; they should be derived from test devices rather than copied from an unrelated production.

### Measurement problems

- “Engagement” is measured inconsistently through self-report, time, interactions, completion or preference.
- Source clicks measure verification attempts, not whether readers understood or correctly evaluated the source.
- Lower trust after uncertainty disclosure may represent desirable calibration rather than a failure.

---

## Recommended Next Steps

1. **Run a representative device and accessibility benchmark.**  
   Build one SVG-heavy, one Canvas-heavy and one three.js candidate report; test no-JS, reduced motion, keyboard, screen readers, 200% zoom, low-memory mobile and p75 CWV.  
   **Rationale:** Universal asset and WebGL budgets are unavailable; the skill needs evidence from its actual output and audience.

2. **Pre-register a narrative-format experiment.**  
   Compare the same report as ordinary long-form, discrete scroller and continuous scrubber. Measure immediate comprehension, delayed recall, source verification, task time and motion discomfort—not only completion or dwell time.  
   **Rationale:** Existing evidence does not establish that continuous scrolling is superior to a stepper.

3. **A/B test citation affordances.**  
   Compare superscript-to-endnote, inline preview, and persistent side/drawer citations. Instrument preview opens, external-source clicks, return rate and claim-source matching accuracy.  
   **Rationale:** Existing behavioral data establishes low verification, but not the best citation component for this report form.

4. **Build an automated claim-coverage and motion-lint pipeline.**  
   Fail output when a factual claim lacks a source or inference chain; a scroll state lacks a claim ID; motion lacks a semantic delta; content exists only in canvas/WebGL; or reduced motion removes information.  
   **Rationale:** These checks convert the strongest findings directly into enforceable Claude Code skill rules.

5. **Create a subject-derived distinctiveness audit.**  
   Compare consecutive generated pages using structural and visual fingerprints: hero geometry, scrolly position, typography hierarchy, color distribution, transition types and illustration motifs. Require an editorial explanation linking major choices to the subject.  
   **Rationale:** Standardized infrastructure is valuable, but visible repetition is a documented practitioner concern and currently lacks a measurable industry benchmark.

## Sources

- [https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf](https://idl.cs.washington.edu/files/2010-Narrative-InfoVis.pdf)
- [https://narrative-flow.github.io/paper/visual-narrative-flow.pdf](https://narrative-flow.github.io/paper/visual-narrative-flow.pdf)
- [Research:Which parts of an article do readers read - Meta-Wiki](https://meta.wikimedia.org/wiki/Research%3AWhich_parts_of_an_article_do_readers_read?utm_source=openai)
- [ScrollTrigger | GSAP | Docs & Learning](https://gsap.com/docs/v3/Plugins/ScrollTrigger/?utm_source=openai)
- [How the Core Web Vitals metrics thresholds were defined  |  Articles  |  web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds?authuser=5&hl=en&utm_source=openai)
- [Scrolling into the Newsroom: A vocabulary for scrollytelling techniques in visual online articles](https://lwc1.benjamins.com/catalog/idj.22005.oes?utm_source=openai)
- [https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf](https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf)
- [Linking and Layout: Exploring the Integration of Text and Visualization in Storytelling - VisPubs](https://vispubs.com/?paper=10.1111%2Fcgf.13719&utm_source=openai)
- [https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf](https://nzjohng.github.io/publications/papers/jvlc2019_2.pdf)
- [(PDF) Storytelling in Information Visualizations: Does it Engage Users to Explore Data?](https://www.researchgate.net/publication/278381124_Storytelling_in_Information_Visualizations_Does_it_Engage_Users_to_Explore_Data)
- [Effectiveness of animation in trend visualization - Yonsei University](https://yonsei.elsevierpure.com/en/publications/effectiveness-of-animation-in-trend-visualization/?utm_source=openai)
- [The Impact of Elicitation and Contrasting Narratives on Engagement, Recall and Attitude Change Wi...](https://pubmed.ncbi.nlm.nih.gov/38241101/)
- [Scrollytelling as an Alternative Format for Privacy Policies](https://arxiv.org/abs/2603.04367?utm_source=openai)
- [Communicating data: interactive infographics, scientific data and credibility - Journal of Scienc...](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/?utm_source=openai)
- [From Invisible to Visible: Impacts of Metadata in Communicative Data Visualization - PubMed](https://pubmed.ncbi.nlm.nih.gov/37015379/?utm_source=openai)
- [(PDF) Quantifying Engagement with Citations on Wikipedia](https://www.researchgate.net/publication/338789479_Quantifying_Engagement_with_Citations_on_Wikipedia?utm_source=openai)
- [Evaluating narrative visualization: a survey of practitioners - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10064970/?utm_source=openai)
- [How We Made the Washington Post Eclipse-Scroller - Features - Source: An OpenNews project](https://source.opennews.org/articles/how-we-made-washington-post-eclipse-scroller/?utm_source=openai)
- [WebGLRenderer - Three.js Docs](https://threejs.org/docs/pages/WebGLRenderer.html?utm_source=openai)
- [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/?utm_source=openai)
- [Understanding Success Criterion 2.2.2: Pause, Stop, Hide | WAI | W3C](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html?utm_source=openai)
- [How We Made Unequal Justice - Features - Source: An OpenNews project](https://source.opennews.org/articles/how-we-made-unequal-justice/?utm_source=openai)
- [How We Made "Behind the Bloodshed" - Features - Source: An OpenNews project](https://source.opennews.org/articles/how-we-made-behind-bloodshed/?utm_source=openai)
