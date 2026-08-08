---
title: "Empirical Production Rules for Scrollytelling Web Reports"
run_id: dr_344b02598105d6e9
question: "How do practitioners build single-page, evidence-dense scrollytelling web reports — the narrative-visualisation form used by newsroom graphics desks and independent data-journalism sites — and what measurably works versus fails? Cover: (1) documented production patterns and narrative structures for long-form scroll-driven report pages (author-driven vs reader-driven martini-glass / interactive-slideshow / drill-down structures, section pacing, the \"one idea per scroll state\" discipline); (2) empirical findings on comprehension, recall and engagement in narrative visualisation and scrollytelling, including where animation and scroll-linked transitions measurably help understanding and where they measurably hurt; (3) citation, provenance and trust UX in evidence-dense pages — inline citation affordances, footnote/popup patterns, source-list design, and what makes readers actually verify a claim; (4) production practice for GSAP ScrollTrigger and three.js/WebGL on narrative pages: performance budgets, Core Web Vitals and INP impact, scroll-linked animation techniques, WebGL fallbacks and progressive enhancement, and when a 3D scene earns its cost versus being decoration; (5) accessibility for scroll-driven and animated content — prefers-reduced-motion, keyboard and screen-reader access to scroll-triggered content, motion-triggered vestibular disorders, and the WCAG criteria that apply; (6) the documented failure modes: scrolljacking, mobile performance collapse, unlabelled or misleading charts, visual homogeneity and template sameness across pages from one producer, and reports whose claims outrun their sources. Prioritise measured results, published post-mortems from graphics desks, and peer-reviewed narrative-visualisation research over listicles and vendor marketing."
provider: local-codex
model: Codex CLI
tier: max
archetype: technical
sources: 46
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 0.00
completed: 2026-08-08T04:38:44.072Z
---
Reading additional input from stdin...
OpenAI Codex v0.146.0
--------
workdir: /Users/lukerhodes/Dev
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019fdfa0-fe73-7b73-ad25-3d11eb76baa3
--------
user
<role>
You are a senior research analyst evaluating software stacks, infrastructure, APIs, or model architectures. Your output will directly Building a Claude Code skill that turns a multi-backend research corpus into ONE self-contained HTML report page per topic, published to a subdomain. Every page must look genuinely different from the last, themed to its subject, with GSAP as a standing motion layer and three.js only when the subject earns it. Need citable rules for narrative structure, motion budget, the test for when 3D earns its place, inline-citation and source-list UX, accessibility floors, and the failure modes that make a page untrustworthy or recognisably templated..
</role>

<context>
This investigation supports a concrete decision. Keep this context tight, context bloat degrades long-running agentic output; domain knowledge belongs in the analysis lens below.
</context>

<core_directive>
Answer this decisively: How do practitioners build single-page, evidence-dense scrollytelling web reports — the narrative-visualisation form used by newsroom graphics desks and independent data-journalism sites — and what measurably works versus fails? Cover: (1) documented production patterns and narrative structures for long-form scroll-driven report pages (author-driven vs reader-driven martini-glass / interactive-slideshow / drill-down structures, section pacing, the "one idea per scroll state" discipline); (2) empirical findings on comprehension, recall and engagement in narrative visualisation and scrollytelling, including where animation and scroll-linked transitions measurably help understanding and where they measurably hurt; (3) citation, provenance and trust UX in evidence-dense pages — inline citation affordances, footnote/popup patterns, source-list design, and what makes readers actually verify a claim; (4) production practice for GSAP ScrollTrigger and three.js/WebGL on narrative pages: performance budgets, Core Web Vitals and INP impact, scroll-linked animation techniques, WebGL fallbacks and progressive enhancement, and when a 3D scene earns its cost versus being decoration; (5) accessibility for scroll-driven and animated content — prefers-reduced-motion, keyboard and screen-reader access to scroll-triggered content, motion-triggered vestibular disorders, and the WCAG criteria that apply; (6) the documented failure modes: scrolljacking, mobile performance collapse, unlabelled or misleading charts, visual homogeneity and template sameness across pages from one producer, and reports whose claims outrun their sources. Prioritise measured results, published post-mortems from graphics desks, and peer-reviewed narrative-visualisation research over listicles and vendor marketing.
</core_directive>

<research_questions>
Primary:
1. Answer this decisively: How do practitioners build single-page, evidence-dense scrollytelling web reports — the narrative-visualisation form used by newsroom graphics desks and independent data-journalism sites — and what measurably works versus fails? Cover: (1) documented production patterns and narrative structures for long-form scroll-driven report pages (author-driven vs reader-driven martini-glass / interactive-slideshow / drill-down structures, section pacing, the "one idea per scroll state" discipline); (2) empirical findings on comprehension, recall and engagement in narrative visualisation and scrollytelling, including where animation and scroll-linked transitions measurably help understanding and where they measurably hurt; (3) citation, provenance and trust UX in evidence-dense pages — inline citation affordances, footnote/popup patterns, source-list design, and what makes readers actually verify a claim; (4) production practice for GSAP ScrollTrigger and three.js/WebGL on narrative pages: performance budgets, Core Web Vitals and INP impact, scroll-linked animation techniques, WebGL fallbacks and progressive enhancement, and when a 3D scene earns its cost versus being decoration; (5) accessibility for scroll-driven and animated content — prefers-reduced-motion, keyboard and screen-reader access to scroll-triggered content, motion-triggered vestibular disorders, and the WCAG criteria that apply; (6) the documented failure modes: scrolljacking, mobile performance collapse, unlabelled or misleading charts, visual homogeneity and template sameness across pages from one producer, and reports whose claims outrun their sources. Prioritise measured results, published post-mortems from graphics desks, and peer-reviewed narrative-visualisation research over listicles and vendor marketing.

Secondary:
2. What is the current state, and what is the strongest supporting evidence for it?
3. What are the contrasting viewpoints or competing evidence?
4. What changed recently, and what is the trajectory?
</research_questions>

<scope_and_boundaries>
<include>
- Entities, technologies, geographies, segments, and time windows directly relevant to the core directive.
</include>
<exclude>
- Tangential background material, SEO aggregator content, and pre-scope introductory explainers.
- SEO content-marketing and blog-post-writing advice
- BI dashboard tool comparisons (Tableau/PowerBI/Looker)
- no-code website builder and CMS template reviews
- general React/framework tutorials unrelated to narrative pages
</exclude>
<time_horizon>
2019 to present, with foundational narrative-visualisation research (Segel & Heer and successors) included regardless of date
</time_horizon>
</scope_and_boundaries>

<source_discipline>
<prioritise>
- Primary and authoritative sources: official documentation, peer-reviewed literature, regulators, government databases, published benchmarks, raw datasets, court filings, filed financials.
- Official documentation, source repositories (including issues and PRs), vendor engineering blogs, peer-reviewed benchmarks, architecture whitepapers.
</prioritise>
<deprioritise>
- Aggregator sites, SEO-optimised listicles, marketing blogs, vendor comparison pages, and content farms. Do not rely on these as primary evidence; if cited at all, label them `[SECONDARY: promotional]` and corroborate from a primary source.
- Vendor landing pages, "top 10 tools" listicles, influencer posts, and vendor-commissioned analyst reports (label these `[SECONDARY: promotional]`).
</deprioritise>
<criteria_match_validator>
For each source integrated into the synthesis, briefly justify why it met the source-discipline criteria. Discard sources that cannot be justified rather than including them with a caveat.
</criteria_match_validator>
</source_discipline>

<depth_requirements>
- Factual findings with quantitative data where available (numbers, dates, specific named entities).
- Contrasting viewpoints or competing evidence wherever it exists.
- Named sources (author or organisation, publication date, URL).
- A confidence qualifier on every non-trivial claim: High, Medium, or Low.
- Extract exact latency numbers, API schemas, rate limits, and documented architectural trade-offs verbatim where available.
</depth_requirements>

<analysis_lens>
Apply these analytical frames where relevant, they tell you how to think about the findings, not only what to find:
- Build-vs-buy and operational trade-offs for the stated team size and constraints.
- What converts directly into a design rule a build agent can follow
- Where the evidence is contested rather than settled
- What distinguishes a page that reads as authored from one that reads as generated
</analysis_lens>

<epistemic_bounding>
When data is unavailable, unreliable, or contested, use these tags inline. Do not estimate, extrapolate, or paper over gaps:
- `<MISSING_DATA>[what was sought, what was unavailable, what would be needed]</MISSING_DATA>`
- `<INSUFFICIENT_EVIDENCE>[claim that could not be corroborated, and why]</INSUFFICIENT_EVIDENCE>`
- `<CONFLICTING_EVIDENCE>[the positions, their sources, the nature of the disagreement]</CONFLICTING_EVIDENCE>`
- `<CONFIDENCE:LOW>[the claim]</CONFIDENCE:LOW>` for weakly-supported but load-bearing estimates
- `<INFERENCE from="[the cited claims it rests on]">[claim derived by reasoning; show the chain]</INFERENCE>`, this tag is required for every statement you assembled rather than read. A conclusion drawn from three sourced facts is an inference even when all three are correct, and naming which facts it rests on is what lets a reader check the step you took between them.
Do not present extrapolated or synthesised numbers as empirical findings.
</epistemic_bounding>

<citation_protocol>
Append an inline ``` to every quantitative claim, every attributed statement, and every regulatory or legal reference, at the point of the claim itself. Do not aggregate citations at the end of a paragraph or into a bibliography, that is where source attribution is lost. If a URL is not verifiable at synthesis time, use ``UNVERIFIED (unusable citation URL)`` rather than omitting or inventing one.
</citation_protocol>

<output_format>
Structure the report exactly as follows:
- ## Executive Summary, 5-8 bullets, each led by a `(High Confidence)` / `(Medium Confidence)` / `(Low Confidence)` qualifier; usable as a standalone briefing.
- ## Detailed Findings, one section per research question, using the question as the heading; narrative prose with inline citations, tables for comparative data.
- ## Evidence Table, | Claim | Primary Source | Publication Date | Evidence Type | URL |, mapping every major claim to a verifiable source.
- ## Knowledge Gaps, what could not be answered, categorised by cause.
- ## Recommended Next Steps, 3-5 follow-up investigations, each with a stated rationale.
- Include a comparison table with columns such as Parameter Count / Context Window / Latency / Cost / License, technical reality lives in tables, prose buries it.
</output_format>

<constraints>
- Do not fabricate citations, URLs, authors, or dates; use the unverified citation form when a source cannot be verified.
- Where data conflicts, present both positions with their evidence, do not silently pick one.
- Keep prose dense but readable; avoid filler phrases.
- Cite inline at the point of the claim, never aggregated at the end.
</constraints>

<core_directive>
Answer this decisively: How do practitioners build single-page, evidence-dense scrollytelling web reports — the narrative-visualisation form used by newsroom graphics desks and independent data-journalism sites — and what measurably works versus fails? Cover: (1) documented production patterns and narrative structures for long-form scroll-driven report pages (author-driven vs reader-driven martini-glass / interactive-slideshow / drill-down structures, section pacing, the "one idea per scroll state" discipline); (2) empirical findings on comprehension, recall and engagement in narrative visualisation and scrollytelling, including where animation and scroll-linked transitions measurably help understanding and where they measurably hurt; (3) citation, provenance and trust UX in evidence-dense pages — inline citation affordances, footnote/popup patterns, source-list design, and what makes readers actually verify a claim; (4) production practice for GSAP ScrollTrigger and three.js/WebGL on narrative pages: performance budgets, Core Web Vitals and INP impact, scroll-linked animation techniques, WebGL fallbacks and progressive enhancement, and when a 3D scene earns its cost versus being decoration; (5) accessibility for scroll-driven and animated content — prefers-reduced-motion, keyboard and screen-reader access to scroll-triggered content, motion-triggered vestibular disorders, and the WCAG criteria that apply; (6) the documented failure modes: scrolljacking, mobile performance collapse, unlabelled or misleading charts, visual homogeneity and template sameness across pages from one producer, and reports whose claims outrun their sources. Prioritise measured results, published post-mortems from graphics desks, and peer-reviewed narrative-visualisation research over listicles and vendor marketing.
</core_directive>
warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
codex
I’m treating this as a source-led research synthesis, not a general web-design answer. I’ll verify foundational visualization research, recent empirical studies, newsroom production write-ups, browser/performance standards, GSAP/three.js documentation, and WCAG requirements; then I’ll separate documented findings from design rules I infer for the Claude Code skill.
  → Collect foundational and recent empirical narrative-visualisation evidence
  • Collect newsroom production patterns, citation/trust research, and failure post-mortems
  • Collect GSAP/WebGL performance, Core Web Vitals, and accessibility requirements
  • Synthesize citable rules, competing evidence, gaps, and implementation tests
web search: 
web search: Segel Heer Narrative Visualization Telling Stories with Data PDF 2010 ...
web search: 
web search: empirical evaluation scrollytelling comprehension engagement study narrative visualization scroll 2021 PDF ...
web search: 
web search: "Storytelling in Information Visualizations" Boy Fekete Detienne results engagement narrative did not increase exploration ...
web search: 
web search: site:source.opennews.org scrollytelling newsroom graphics scroll production lessons performance ...
web search: 
web search: https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/
web search: 
web search: 
codex
The evidence is already separating into two tiers: strong support for guided sequencing and object-continuity transitions, but weak/contested support for the broader claim that “scrollytelling increases learning.” I’m keeping engagement, comprehension, recall, and exploration as separate outcomes so a polished interaction is not mistaken for better understanding.
web search: 
web search: peer reviewed study inline citations click verify source credibility hyperlinks footnotes web readers claims ...
web search: 
web search: 
web search: 
web search: site:web.dev Core Web Vitals thresholds LCP INP CLS 75th percentile official ...
web search: 
web search: site:gsap.com/docs/v3/Plugins/ScrollTrigger performance ScrollTrigger scroll events requestAnimationFrame scrub matchMedia ...
web search: 
web search: site:threejs.org/docs WebGLRenderer setPixelRatio powerPreference context lost fallback WebGL availability ...
web search: 
web search: site:developer.mozilla.org WebGLRenderingContext isContextLost webglcontextlost fallback canvas accessibility ...
web search: 
web search: site:w3.org/WAI/WCAG22/Understanding animation from interactions vestibular reduced motion 2.3.3 ...
web search: 
web search: site:w3.org/WAI/tutorials/images/complex charts long descriptions data tables accessibility ...
web search: 
web search: newsroom graphics desk postmortem scrollytelling templates sameness visual storytelling design process Source OpenNews ...
web search: 
web search: scrolljacking usability study browser scrolling user control research Nielsen Norman ...
web search: 
web search: Hullman Diakopoulos Visualization Rhetoric framing effects narrative visualization PDF 2011 ...
web search: 
web search: site:developer.mozilla.org CSS scroll-driven animations browser compatibility baseline 2026 animation-timeline ...
web search: 
web search: 
web search: 
web search: 
web search: 
web search: "Investigating user behavior in slideshows and scrollytelling" PDF results comprehension 85 participants ...
web search: 
web search: Tversky Morrison Betrancourt Animation Can It Facilitate 2002 PDF apprehension congruence ...
web search: 
web search: Hullman Drucker A Deeper Understanding of Sequence in Narrative Visualization PDF 2013 sequence order recall ...
web search: 
web search: site:gsap.com licensing GSAP free commercial use 2026 official ...
web search: 
web search: GSAP license free commercial Webflow all plugins official 2025 gsap.com licensing ...
The source base now covers empirical visualization studies, newsroom practice, trust/citation behavior, browser performance, GSAP/three.js, and WCAG. I’m moving into synthesis and converting evidence into explicit skill gates while marking unsupported numeric budgets as gaps.
  ✓ Collect foundational and recent empirical narrative-visualisation evidence
  ✓ Collect newsroom production patterns, citation/trust research, and failure post-mortems
  ✓ Collect GSAP/WebGL performance, Core Web Vitals, and accessibility requirements
  → Synthesize citable rules, competing evidence, gaps, and implementation tests
web search: 
web search: site:web.dev INP does not include scroll hover interactions click tap keyboard definition ...
codex
The central implementation decision is now clear: the skill should generate a durable, readable HTML document first, then add a subject-specific visual argument and measured enhancement layers. GSAP can be standard; three.js cannot be. The 3D decision needs a semantic-and-performance gate, not an aesthetic prompt.
Synthesis is complete: the report distinguishes direct findings from inferred build rules, includes explicit performance/accessibility gates, and records the unsupported areas as knowledge gaps rather than inventing numeric standards.
  ✓ Collect foundational and recent empirical narrative-visualisation evidence
  ✓ Collect newsroom production patterns, citation/trust research, and failure post-mortems
  ✓ Collect GSAP/WebGL performance, Core Web Vitals, and accessibility requirements
  ✓ Synthesize citable rules, competing evidence, gaps, and implementation tests
codex
## Executive Summary

- **(High Confidence)** Build the report as a linear, server-rendered document first. Use scroll states to guide attention through successive claims, then optionally open into exploration—the “martini-glass” structure. Reserve slideshows for bounded branches and drill-down for audiences arriving with their own questions. Segel and Heer derived these structures from 58 narrative visualizations. [scivis.github.io](https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf) (unusable citation URL)`[Segel & Heer (2010)](https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf)

- **(High Confidence)** Enforce one claim per scroll state. Text should be short enough to coexist with its visual; transitions should preserve landmarks and change only the variables needed to communicate that claim. ONS reports that this format works best when presenting one point at a time; controlled animation research similarly favors simple staging over elaborate multi-stage movement. [digitalblog.ons.gov.uk](https://digitalblog.ons.gov.uk/2021/05/24/what-makes-for-a-good-scrollytelling-article/)[ONS Digital (2021)](https://digitalblog.ons.gov.uk/2021/05/24/what-makes-for-a-good-scrollytelling-article/) [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson (2007)](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)

- **(High Confidence)** Animation helps when it explains a transformation: tracking the same entity, sorting, filtering, rescaling, changing time, or moving through genuine space. It does not reliably improve general learning, recall, exploration, or trust. In one controlled study with 24 participants, animated transitions reduced perception errors, but extreme staging sometimes performed worse; broader reviews found no general advantage over informationally equivalent static diagrams. [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson (2007)](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf) [tc.columbia.edu](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)[Tversky, Morrison & Bétrancourt (2002)](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)

- **(High Confidence)** Put a citation beside the exact claim it supports, with a low-friction popover containing source title, author/publisher, date, evidence type, and a direct link. Also provide a deduplicated source list and methods/limitations section. Do not assume readers will verify: Wikipedia instrumentation found an external-reference click in only 0.29% of page views, although merely showing sources and reporting practices can increase perceived trust. [arxiv.org](https://arxiv.org/abs/2001.08614)[Piccardi et al. (2020)](https://arxiv.org/abs/2001.08614) [mediaengagement.org](https://mediaengagement.org/research/trust-in-online-news/)[Center for Media Engagement](https://mediaengagement.org/research/trust-in-online-news/)

- **(High Confidence)** Use GSAP ScrollTrigger as an orchestration layer over native scrolling—not as a replacement for scrolling. The release floor should be field Core Web Vitals at the 75th percentile: LCP ≤2.5 seconds, INP ≤200 milliseconds and CLS ≤0.1; animated frames should target 16.7 milliseconds, with no main-thread task over 50 milliseconds. [web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds)[web.dev Core Web Vitals thresholds](https://web.dev/articles/defining-core-web-vitals-thresholds) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long)[MDN performance timings](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long)

- **(High Confidence)** three.js earns inclusion only if the claim depends on inherently three-dimensional structure, viewpoint, occlusion, volume, or spatial continuity—and a prototype performs better than the best 2D explanation on comprehension or task accuracy. Decorative depth, particle fields, rotating logos, and generic “immersive” scenes fail this test. Every 3D state must have an equivalent DOM/2D fallback.

- **(High Confidence)** Accessibility is architectural. The full narrative and data must exist in meaningful DOM order; charts need short and long descriptions or data tables; all interactions need keyboard equivalents; non-essential motion must honor `prefers-reduced-motion`; and continuous or scroll-started movement may require pause/stop controls under WCAG 2.2.2 and 2.3.3. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions)[W3C: Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions) [w3.org](https://www.w3.org/WAI/tutorials/images/complex/)[W3C: Complex Images](https://www.w3.org/WAI/tutorials/images/complex/)

- **(Medium Confidence)** Reuse an engineering chassis, not an aesthetic template. The shared layer should provide semantics, citations, responsive scrollytelling, accessibility and observability; each topic should derive its typography, visual primitives, chart grammar and motion from the subject. `<INSUFFICIENT_EVIDENCE>There is no validated metric for “recognisably templated” report pages; the recommended similarity tests below are production heuristics.</INSUFFICIENT_EVIDENCE>`

## Detailed Findings

### 1. How do practitioners build single-page, evidence-dense scrollytelling reports, and what measurably works versus fails?

#### Narrative architecture and production pattern

**(High Confidence)** Segel and Heer distinguish author-driven narration from reader-driven exploration and identify three hybrid structures:

| Structure | Control pattern | Best use | Principal failure |
|---|---|---|---|
| Martini glass | Linear author-led sequence, followed by open exploration | Establish context and evidence before offering filtering, comparison or personalization | Exploration is bolted on without explaining what readers can learn from it |
| Interactive slideshow | Author controls chapter order; reader interacts inside bounded scenes | Discrete cases, alternatives, stages or small branches | Hidden “next” controls, no backtracking, content trapped behind clicks |
| Drill-down | Reader chooses sequence and depth | Reference material and expert audiences with distinct questions | No defensible editorial through-line; important evidence can remain undiscovered |

These structures and seven visual genres were derived from 58 examples rather than a controlled effectiveness experiment. [scivis.github.io](https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf)[Segel & Heer (2010)](https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf)

**(High Confidence)** Later sequence research analyzed 42 professional narrative visualizations and found memory and preference benefits from sequences using parallelism—repeated structural relationships that let readers compare states—while emphasizing consistency between adjacent visualizations. [pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24051807/)[Hullman et al. (2013)](https://pubmed.ncbi.nlm.nih.gov/24051807/)

**(High Confidence)** ONS’s production practice uses a reusable component chassis for layout, navigation, charts and maps, but connects changing text, maps and charts through article-specific state. It also identified pre-rendered HTML as necessary for wider compatibility, JavaScript-disabled reading and search indexing. [digitalblog.ons.gov.uk](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/)[ONS Digital: How we build scrollytelling articles](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/)

**(High Confidence)** The Pudding’s post-mortems add three practical constraints: state transitions must be idempotent because readers skip rapidly across steps; mobile may need stacked static charts when transitions do not carry meaning; and hover-dependent annotation should become visible text or explicit controls on touch devices. [pudding.cool](https://pudding.cool/process/how-to-make-dope-shit-part-3/)[The Pudding: Making Internet Things](https://pudding.cool/process/how-to-make-dope-shit-part-3/) [pudding.cool](https://pudding.cool/process/responsive-scrollytelling/)[The Pudding: Responsive scrollytelling](https://pudding.cool/process/responsive-scrollytelling/)

<INFERENCE from="Segel & Heer’s three structures; Hullman et al.’s sequence findings; ONS one-point-at-a-time guidance; The Pudding’s fast-scroll failure report">**Skill rule:** compile the research corpus into a claim graph before designing the page. Each scroll state receives exactly one primary claim, one visual question and one stable end-state. Adjacent states should reuse objects, scales and spatial positions unless changing one of those is itself the evidence.</INFERENCE>

A reliable default narrative is:

1. **Contract:** headline conclusion, scope, update date and evidence quality.
2. **Orientation:** define the system or dataset and show the stable visual frame.
3. **Progressive proof:** one claim per state, ordered context → mechanism → consequence.
4. **Complication:** conflicting evidence, uncertainty and scope limits.
5. **Synthesis:** answer the stated decision.
6. **Exploration:** filters, comparisons, underlying table or drill-down.
7. **Provenance:** methods, limitations, sources, corrections and version history.

This is an inferred production pattern rather than an experimentally validated universal sequence. `<INFERENCE from="Segel & Heer’s martini-glass structure; ONS’s stepwise explanation; Center for Media Engagement transparency study">The order preserves an editorial argument while leaving audit and exploration available after the core evidence has been understood.</INFERENCE>`

#### What animation improves—and what it does not

**(High Confidence)** Heer and Robertson tested static, direct-animated and staged-animated transitions with 24 participants. Their object-tracking animations lasted 1.25 seconds and value-change animations lasted 2 seconds. Animated conditions reduced tracking error across all tested transition types (`p < 0.001`), while semantic value-estimation benefits varied by chart. [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson (2007)](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)

**(High Confidence)** More staging was not monotonically better. Extreme staging was worse than direct animation for donut-chart value changes (`p = 0.024`), and stacked bars showed no significant animation condition effect (`p = 0.224`). Axis rescaling increased errors and “unknown” responses; retaining common scales and persistent landmarks was preferable. [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson (2007)](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)

**(High Confidence)** Tversky, Morrison and Bétrancourt’s review found no general learning advantage for animation when static and animated treatments contained equivalent information. Animation frequently failed because it was transient, too fast or too complex to apprehend; it was most defensible for genuine temporal change, transformation, causal sequence and spatial reorientation. [tc.columbia.edu](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)[Tversky, Morrison & Bétrancourt (2002)](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)

**(Medium Confidence)** McKenna et al.’s 240-participant study found that visuals and navigation feedback, including static versus animated transitions, affected engagement, while discrete versus continuous control may not. This supports useful feedback, but not a general claim that continuous scrollytelling outperforms steppers. [onlinelibrary.wiley.com](https://onlinelibrary.wiley.com/doi/10.1111/cgf.13195)[McKenna et al. (2017)](https://onlinelibrary.wiley.com/doi/10.1111/cgf.13195)

**(High Confidence)** Three field experiments found that adding an introductory story to exploratory visualizations did not increase subsequent exploratory interaction. Narrative consumption and exploratory engagement therefore need separate success metrics. [researchportal.ip-paris.fr](https://researchportal.ip-paris.fr/fr/publications/storytelling-in-information-visualizations-does-it-engage-users-t/)[Boy, Détienne & Fekete (2015)](https://researchportal.ip-paris.fr/fr/publications/storytelling-in-information-visualizations-does-it-engage-users-t/)

**(Medium Confidence)** A 2023 comparison involving 85 participants found slideshow clicking easier and more intuitive than the study’s scrollytelling implementation; its knowledge checks were near ceiling and could not distinguish comprehension. The authors noted that their slow fade-out/fade-in scroll implementation differed from normal newsroom scrolling. [vis.test.uib.no](https://vis.test.uib.no/wp-content/papercite-data/pdfs/mittenentzwei2023userbehavior.pdf)[Mittenentzwei et al. (2023)](https://vis.test.uib.no/wp-content/papercite-data/pdfs/mittenentzwei2023userbehavior.pdf)

**(Medium Confidence)** A 2026 preprint with 454 participants found scrollytelling improved reported engagement, clarity and cognitive load over full privacy-policy text, while comprehension and confidence were broadly equivalent and trust changes were statistically inconclusive. [arxiv.org](https://arxiv.org/abs/2603.04367)[Méndez & Such (2026 preprint)](https://arxiv.org/abs/2603.04367)

| Outcome | Strongest finding | Confidence | Build consequence |
|---|---|---:|---|
| Object tracking | Animation preserves correspondence between related marks | High | Animate persistent objects rather than replacing the whole scene |
| Change estimation | Helps for some transitions; rescaling and over-staging undermine it | High | Keep scales fixed; separate only necessary transformations |
| General comprehension | Mixed; often equal to good static explanations | Medium | Require comprehension testing, not preference alone |
| Recall | Titles, meaningful text, recognizable objects and structural parallelism help | Medium–High | Give every visual an editorial title and stable semantic landmarks |
| Engagement | Visuals and feedback can help; narrative does not guarantee exploration | Medium | Measure completion and exploration separately |
| Trust | Source visibility and transparency help perceived trust; motion does not establish truth | High | Treat provenance as content, not decoration |

**(High Confidence)** Borkin et al. studied 393 visualizations, eye movements from 33 participants and thousands of descriptions. Titles and supporting text materially supported recognition and recall; recognizable objects appeared in 74% of the most recognizable third but 8% of the least recognizable third. [vcg.seas.harvard.edu](https://vcg.seas.harvard.edu/files/pfister/files/infovis_submission251-camera.pdf)[Borkin et al. (2015)](https://vcg.seas.harvard.edu/files/pfister/files/infovis_submission251-camera.pdf)

<INFERENCE from="Heer & Robertson’s object-continuity result; Tversky et al.’s congruence/apprehension principles; Borkin et al.’s title and object findings">**Motion test:** an animation is admissible only when a reviewer can finish the sentence “This motion lets the reader perceive ___ that would otherwise require a difficult mental comparison.” If the blank is “energy,” “delight,” “premium quality” or “immersion,” it is decoration and does not consume the evidence-motion budget.</INFERENCE>

#### Citation, provenance and trust UX

**(High Confidence)** Citation presence and citation verification are different outcomes. Piccardi et al. instrumented 96 million Wikipedia citation-related events over two months and found reference clicks in 0.29% of page views: 0.56% on desktop and 0.13% on mobile. Ninety-three percent of citation links received no click during the measured month. Open-access and recent sources were more likely to be opened. [arxiv.org](https://arxiv.org/abs/2001.08614)[Piccardi et al. (2020)](https://arxiv.org/abs/2001.08614)

**(Medium Confidence)** Citation clicks were more common on shorter and lower-quality Wikipedia pages, suggesting that readers verify when the page itself fails to meet an information need—not merely because a reference marker is visible. This is observational, not causal. [arxiv.org](https://arxiv.org/abs/2001.08614)[Piccardi et al. (2020)](https://arxiv.org/abs/2001.08614)

**(Medium Confidence)** In a randomized experiment with 1,183 adults, a bundle containing inline footnotes, author information, story type, reporting-method disclosure and organizational standards produced small but statistically significant improvements on four of 15 organizational evaluations. The experiment cannot isolate which indicator caused the effect. [mediaengagement.org](https://mediaengagement.org/research/trust-in-online-news/)[Center for Media Engagement](https://mediaengagement.org/research/trust-in-online-news/)

**(Medium Confidence)** An experiment with 517 participants found that source attribution affected perceived credibility and interacted with prior trust in the named institution; actual comprehension did not reliably predict perceived credibility. [jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/)[Li et al. (2018)](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/)

**(Medium Confidence)** Qualitative research on COVID-19 visualizations found clear source identification, correct presentation and contextual notes supported trust; participants frequently said they would not inspect the data even though source links reassured them. Likability did not correspond with trustworthiness. [journals.sagepub.com](https://journals.sagepub.com/doi/10.1177/14648849231190725)[Tong (2024)](https://journals.sagepub.com/doi/10.1177/14648849231190725)

<INFERENCE from="low Wikipedia citation click-through; transparency-indicator experiment; source-attribution and visualization-trust studies">**Citation UI rule:** place an atomic marker immediately after the supported clause. Activating it should open an inline popover—not navigate immediately—with: source title; author/publisher; publication date; evidence type; the specific table/page/section; a one-sentence statement of what the source supports; and “Open original.” Keyboard activation, focus return and escape-to-close are mandatory.</INFERENCE>

<INFERENCE from="same trust and citation findings">The final source list should deduplicate records and expose source tier, publication date, access date, relevant claims and limitations. A methods panel should disclose corpus construction, excluded evidence, conflicts, transformations, corrections and report version. Source visibility must never be treated as evidence that a claim was verified.</INFERENCE>

For the Claude Code skill, every claim should be represented internally as:

```text
claim_id
claim_text
confidence
direct_or_inference
source_ids[]
supporting_excerpt_or_data_location
scope_and_limitations
visual_state_ids[]
```

<INFERENCE from="Hullman & Diakopoulos on additions/omissions at data, visual, annotation and interaction layers; the documented rarity of verification">A build must fail if a quantitative or attributed claim lacks a source, if a cited source supports only a nearby proposition, or if an inference is rendered as a direct finding.</INFERENCE> [vis.csail.mit.edu](https://vis.csail.mit.edu/classes/6.859/readings/pdfs/Hullman-VisualizationRhetoric.pdf)[Hullman & Diakopoulos (2011)](https://vis.csail.mit.edu/classes/6.859/readings/pdfs/Hullman-VisualizationRhetoric.pdf)

#### GSAP, browser performance and the motion budget

| Layer | Primary job | Runtime model | Main risk | Required fallback | License/status |
|---|---|---|---|---|---|
| Semantic HTML/CSS | Full report, headings, tables, citations and reading order | Server-rendered/static | None specific to scrollytelling | This is the baseline | Web standards |
| CSS scroll-driven animation | Simple compositor-friendly progress effects | Browser scroll/view timelines | Incomplete browser support | Static styles or GSAP enhancement | W3C Working Draft; `animation-timeline` not Baseline in 2026 [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)[MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline) |
| GSAP + ScrollTrigger | State orchestration, pinned figures, timelines, responsive/reduced-motion branches | JavaScript coordinated with refresh frames | Main-thread work, pinning errors, altered scrolling | Plain document and stacked visuals | Free for permitted commercial use since April 2025; visual-animation-builder competitors are restricted [webflow.com](https://webflow.com/legal/product-terms)[GSAP licence](https://webflow.com/legal/product-terms) |
| SVG/Canvas | Charts and custom 2D marks | DOM or bitmap rendering | Large DOM, paint cost, inaccessible bitmap | Text summary and table | Web standards |
| three.js/WebGL | Genuine spatial or volumetric explanation | GPU render loop plus JS scene orchestration | Payload, GPU/VRAM, battery, context loss, inaccessible canvas | 2D/static equivalent | MIT [threejs.org](https://threejs.org/license/)[three.js licence](https://threejs.org/license/) |

**(High Confidence)** ScrollTrigger calculates trigger positions, synchronizes updates with screen refresh, supports native media queries, and does not require scroll replacement. Its `normalizeScroll()` option explicitly forces scrolling onto the JavaScript thread; that capability should be prohibited by default in this reporting system. [gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)[GSAP ScrollTrigger documentation](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)

**(High Confidence)** Native CSS scroll timelines can run supported effects off the main thread, but `animation-timeline` remained a limited-availability feature in April 2026. It is suitable as an enhancement, not as the only mechanism conveying report meaning. [developer.chrome.com](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)[Chrome scroll-driven animation documentation](https://developer.chrome.com/docs/css-ui/scroll-driven-animations) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)[MDN compatibility status](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)

**(High Confidence)** INP does not directly measure scrolling or hovering. Nevertheless, script evaluation, rendering and JavaScript animation can occupy the main thread and delay a subsequent click, tap or keypress, thereby degrading INP. [web.dev](https://web.dev/articles/inp)[web.dev: INP](https://web.dev/articles/inp) [web.dev](https://web.dev/articles/optimize-input-delay)[web.dev: Optimize input delay](https://web.dev/articles/optimize-input-delay)

##### Release performance budget

| Metric | Mandatory floor | Diagnostic interpretation |
|---|---:|---|
| LCP | ≤2.5 s at field p75 | Hero imagery, fonts or early 3D must not delay primary content |
| INP | ≤200 ms at field p75 | No expensive state construction or interaction callback |
| CLS | ≤0.1 at field p75 | Pre-allocate charts, canvases, citations and sticky regions |
| Frame time | ≤16.7 ms target | Sustained 60 fps; MDN estimates roughly 10 ms remains after browser rendering work |
| Main-thread task | <50 ms | Anything longer is formally a long task and can block interaction |
| Reduced-motion reading | 100% content parity | No claim exists only inside an animated intermediate frame |
| JavaScript-disabled/static reading | Core narrative complete | Enhancements may disappear; evidence may not |

Threshold sources: [web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds)[web.dev Core Web Vitals](https://web.dev/articles/defining-core-web-vitals-thresholds) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long)[MDN performance timings](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long) [web.dev](https://web.dev/articles/optimize-long-tasks)[web.dev long tasks](https://web.dev/articles/optimize-long-tasks)

`<MISSING_DATA>[A universal JavaScript-kilobyte, animation-count, polygon-count or texture-megabyte budget was sought. No authoritative limit generalizes across devices, scenes and network conditions. Device-tier testing and field telemetry are required.]</MISSING_DATA>`

<INFERENCE from="Core Web Vitals thresholds; 16.7 ms frame target; 50 ms long-task definition; animation-comprehension evidence">**Motion budget:** count semantic transformations, not tweens. One scroll state may contain multiple coordinated marks, but they must express one change. A transition fails review if it changes unrelated dimensions, loses landmarks, cannot be understood when scrubbed quickly in either direction, creates a long task, or conveys information only while in motion.</INFERENCE>

Recommended ScrollTrigger practice:

- Use normal document scrolling and CSS `position: sticky` where possible.
- Build one timeline per coherent visual chapter, not one trigger per individual mark.
- Make every state renderer deterministic from `stateId`; never depend on previous animations having completed.
- Use `scrub` only when animation progress has a meaningful continuous relationship to scroll position.
- Prefer a triggered transition into a stable state for discrete claims.
- Animate `transform` and `opacity`; avoid per-frame layout and paint. [web.dev](https://web.dev/articles/animations-and-performance)[web.dev animation performance](https://web.dev/articles/animations-and-performance)
- Use `gsap.matchMedia()` for mobile, desktop and `prefers-reduced-motion`; clean up timelines when conditions change. [gsap.com](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29/)[GSAP matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29/)
- Lazy-load noncritical chapters, but never delay text or citation availability.
- Test rapid forward/back scrolling, browser zoom, font loading, orientation changes and history restoration.

#### When three.js earns its place

<INFERENCE from="3D occlusion research; three.js/WebGL resource costs; animation congruence principle">three.js should pass all four gates below. Failure at any gate selects SVG, Canvas, CSS or a static figure instead.</INFERENCE>

1. **Semantic necessity:** the evidence is intrinsically spatial or volumetric, or the claim depends on viewpoint, occlusion, depth, topology, rotation or continuous movement through space.
2. **Comparative value:** a prototype beats the best 2D alternative on comprehension, accuracy, completion time or error—not merely preference.
3. **Operational fitness:** it meets the same CWV and frame budgets on the target mobile tier, with capped pixel ratio, compressed assets and bounded draw calls/VRAM.
4. **Equivalent fallback:** a static image, 2D projection, table and narrative description communicate the conclusion when WebGL, motion or JavaScript is unavailable.

**(High Confidence)** three.js recommends on-demand rendering for non-continuously animated scenes because an unconditional render loop wastes power and battery. [threejs.org](https://threejs.org/manual/en/rendering-on-demand.html)[three.js: Rendering on Demand](https://threejs.org/manual/en/rendering-on-demand.html)

**(High Confidence)** WebGL guidance recommends batching draw calls, reducing back-buffer resolution where appropriate, bounding VRAM use and handling context loss. Textures, geometries and materials require explicit disposal in three.js. [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)[MDN WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices) [threejs.org](https://threejs.org/manual/en/how-to-dispose-of-objects.html)[three.js disposal guide](https://threejs.org/manual/en/how-to-dispose-of-objects.html)

**(Medium Confidence)** 3D is not generally superior for abstract data: systematic work identifies occlusion, clutter, distortion and scalability as persistent trade-offs, while a network study found 2D better for spatial-memory tasks. [arxiv.org](https://arxiv.org/abs/2001.06462)[Kwon et al. (2020)](https://arxiv.org/abs/2001.06462)

Practical defaults are therefore: dynamic-import three.js after narrative content; use glTF/GLB; render only while visible or changing; cap device pixel ratio based on measured device performance; avoid dynamic shadows and post-processing unless evidential; monitor `renderer.info`; dispose resources between chapters; and replace the canvas immediately on `webglcontextlost`. [threejs.org](https://threejs.org/manual/en/loading-3d-models.html)[three.js model workflow](https://threejs.org/manual/en/loading-3d-models.html) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/webglcontextlost_event)[MDN context-loss event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/webglcontextlost_event)

#### Accessibility floor

| Requirement | Applied rule | Relevant WCAG |
|---|---|---|
| Reading order | Full story exists in meaningful DOM order; sticky positioning must not alter source order | 1.3.1, 1.3.2 |
| Charts/maps/3D | Short description plus structured long description or accessible data table | 1.1.1 |
| Keyboard | Every filter, popover, playback and exploration function works without pointer timing | 2.1.1, 2.1.2 |
| Motion | Honor `prefers-reduced-motion`; provide a visible site-level motion toggle | 2.3.3 AAA; responsible floor even where AAA is not contractual |
| Continuous movement | Pause, stop or hide automatically or scroll-started movement lasting over five seconds alongside content | 2.2.2 A |
| Flashing | Never exceed the flash thresholds | 2.3.1 |
| Focus | Citation popovers and dialogs receive focus and return it to the invoking control | 2.4.3, 2.4.7, 2.4.11 |
| Visual encoding | Do not use color alone; maintain text and non-text contrast | 1.4.1, 1.4.3, 1.4.11 |
| Reflow | No required two-dimensional scrolling at 400% zoom except legitimately two-dimensional data | 1.4.10 |
| Dynamic results | Announce meaningful changes without moving focus unnecessarily | 4.1.3 |

W3C explicitly identifies scroll-triggered parallax as a possible vestibular trigger and recommends eliminating non-essential movement, providing a control, or respecting reduced-motion preferences. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions)[W3C WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions)

W3C’s complex-image guidance requires a short identifier plus a long textual representation of essential chart, map or diagram information; structured data should remain structured rather than compressed into `aria-describedby`. [w3.org](https://www.w3.org/WAI/tutorials/images/complex/)[W3C Complex Images](https://www.w3.org/WAI/tutorials/images/complex/)

<INFERENCE from="WCAG meaningful sequence, keyboard access and complex-image guidance">Scroll observation must never be the only state machine available to assistive technology. Screen-reader users should encounter the claims, descriptions and tables as ordinary document content; exploratory controls should be native controls with explicit names and states.</INFERENCE>

#### Documented failure modes

| Failure | Evidence | Skill-level prohibition |
|---|---|---|
| Scrolljacking | A 2026 study with 20 participants found no significant speed benefit but significantly lower accuracy and satisfaction with scrolljacking | Never alter wheel/touch distance, direction, momentum or browser history behavior [doi.org](https://doi.org/10.1007/978-3-032-16454-4_6)[Murano (2026)](https://doi.org/10.1007/978-3-032-16454-4_6) |
| Mobile collapse | Practitioners report viewport instability, hover failures and animation/rendering costs | Provide a stacked mobile branch when transitions are not essential |
| Intermediate-state dependency | Readers skip multiple states faster than animations complete | Each state must render directly and idempotently |
| Over-staging | Controlled testing found some elaborate staging less accurate | Prefer the shortest transition that preserves object identity |
| Misleading charts | Across five studies, 83.5% of participants showed a truncation effect; instruction did not eliminate it | Validate axes, units, intervals, baselines, legends and uncertainty [doi.org](https://doi.org/10.1016/j.jarmac.2020.10.002)[Okan et al. (2021)](https://doi.org/10.1016/j.jarmac.2020.10.002) |
| Undetected construction errors | Readers have near-universal difficulty identifying errors such as truncated axes, dual scales and missing legends | Run automated lint plus human statistical review [vis.mit.edu](https://vis.mit.edu/pubs/visualint/)[Hopkins, Correll & Satyanarayan (2020)](https://vis.mit.edu/pubs/visualint/) |
| Attractive but untrustworthy | Likability and trustworthiness did not align in qualitative visualization research | Never use finish quality or interaction as a proxy for evidence quality |
| Claims outrun sources | Narrative design can add, omit and prioritize information at data, visual, annotation and interaction layers | Require clause-level source entailment and explicit inference labels |
| Template sameness | No validated measure found | Reuse code and controls; prohibit default page art direction |

#### What reads as authored rather than generated

**(High Confidence)** The Financial Times built reusable story patterns around specific reader questions rather than generic layouts, introducing each only after it had worked on a prominent story. [source.opennews.org](https://source.opennews.org/articles/story-templates-financial-times-reusable/)[Kwong, Financial Times/OpenNews (2019)](https://source.opennews.org/articles/story-templates-financial-times-reusable/)

<INFERENCE from="FT reader-need templates; Borkin et al.’s distinct recognizable objects; Hullman et al.’s benefit from considering alternative sequences">The shared skill should standardize evidence handling, not appearance. Before rendering, it should generate at least three materially different narrative/visual directions and choose between them using subject fit, evidence fit, mobile feasibility and accessibility.</INFERENCE>

A page should fail the “authored” review if:

- its section silhouette matches the preceding report after colors and copy are removed;
- changing the subject noun leaves the visual metaphor intact;
- motion consists primarily of repeated fade/slide/reveal recipes;
- typography, texture and illustration style are unrelated to the source material;
- the hero is more specific than the evidence beneath it;
- the same chart grammar appears regardless of data type;
- or the page lacks an explicit editorial tension, uncertainty or counterargument.

`<CONFIDENCE:LOW>The proposed grayscale/blurred-screenshot similarity check is a useful production heuristic, not a validated perceptual threshold.</CONFIDENCE:LOW>`

### 2. What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** The mature production model is progressively enhanced, componentized scrollytelling: semantic HTML and reusable accessible primitives underneath; topic-specific charts, maps and narrative states above; JavaScript motion as enhancement. ONS’s published stack and The Pudding’s post-mortems document this operational pattern. [digitalblog.ons.gov.uk](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/)[ONS Digital](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/) [pudding.cool](https://pudding.cool/process/responsive-scrollytelling/)[The Pudding](https://pudding.cool/process/responsive-scrollytelling/)

**(High Confidence)** The strongest causal evidence concerns narrow visual tasks: well-designed animation improves correspondence and change perception between related graphical states. It is not evidence that a fully animated long-form article improves retention, belief accuracy or decision quality. [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)

**(High Confidence)** The strongest standards evidence concerns performance and accessibility: measurable CWV thresholds, compositor-friendly animation, reduced motion, keyboard operability and equivalent text for complex visuals. These can be automated as build gates. [web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds)[web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds) [w3.org](https://www.w3.org/TR/WCAG22/)[WCAG 2.2](https://www.w3.org/TR/WCAG22/)

**(Medium Confidence)** The evidence for better scrollytelling comprehension remains domain-specific and mixed. Recent experiments more consistently show improved experience, perceived clarity or engagement than improved objective comprehension or recall. [arxiv.org](https://arxiv.org/abs/2603.04367)[Méndez & Such (2026 preprint)](https://arxiv.org/abs/2603.04367)

<INFERENCE from="the difference between strong narrow transition studies and mixed whole-article studies">The defensible position is therefore: use scrollytelling to manage attention and explain transformations; prove learning, recall and decision outcomes separately for each report class.</INFERENCE>

### 3. What are the contrasting viewpoints or competing evidence?

`<CONFLICTING_EVIDENCE>[Heer & Robertson found significant benefits for animated transitions between related data graphics, while Tversky, Morrison & Bétrancourt found no general benefit over informationally equivalent static diagrams. The disagreement is principally about task and treatment: object continuity and change perception versus broad system learning.]</CONFLICTING_EVIDENCE>`

`<CONFLICTING_EVIDENCE>[McKenna et al. found visuals and navigation feedback affected engagement, but Boy et al. found introductory narrative did not increase subsequent data exploration. Engagement with the story and exploration of the underlying visualization are different dependent variables.]</CONFLICTING_EVIDENCE>`

`<CONFLICTING_EVIDENCE>[A 2026 privacy-policy preprint found improved experience and equivalent comprehension, while a 2023 medical-visualization study found clicking easier than its slow scrollytelling implementation and could not distinguish comprehension. Topic, implementation quality, participant population and outcome measures differ.]</CONFLICTING_EVIDENCE>`

`<CONFLICTING_EVIDENCE>[Visual embellishment can improve recognition and long-term memorability in some studies, but cartoon styling and hand-drawn fonts reduced perceived credibility in 2025 experiments. Distinctive imagery is not equivalent to arbitrary decoration.]</CONFLICTING_EVIDENCE>` [pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/41264452/)[Song et al. (2025/2026)](https://pubmed.ncbi.nlm.nih.gov/41264452/)

**(High Confidence)** These conflicts do not support a stylistic compromise. They support outcome-specific evaluation: comprehension questions for explanatory states, delayed recall for memorable claims, interaction logs for exploration, citation actions for verification, task accuracy for 3D and field telemetry for performance.

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** INP replaced FID as a Core Web Vital in March 2024, shifting production attention from the first interaction toward responsiveness across the visit. This raises the cost of heavy late-page state construction, charts and WebGL interactions even when initial load appears fast. [web.dev](https://web.dev/blog/inp-cwv-march-12)[web.dev (2024)](https://web.dev/blog/inp-cwv-march-12)

**(High Confidence)** CSS scroll-driven animations entered Chromium in 2023 and offer off-main-thread execution for supported effects, but remained non-Baseline in 2026. The likely trajectory is hybrid: CSS for simple transforms and progress indicators, GSAP for cross-browser narrative orchestration, and static fallbacks throughout. [developer.chrome.com](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)[Chrome for Developers](https://developer.chrome.com/docs/css-ui/scroll-driven-animations) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)[MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)

**(High Confidence)** GSAP’s full plugin set became free for permitted commercial use in April 2025, reducing the procurement argument for building a custom animation engine. Its current licence still restricts using GSAP to create competing visual animation builders, which should be checked if the planned Claude Code skill becomes a commercial visual authoring product. [webflow.com](https://webflow.com/updates/gsap-becomes-free)[Webflow (2025)](https://webflow.com/updates/gsap-becomes-free) [webflow.com](https://webflow.com/legal/product-terms)[Current product terms](https://webflow.com/legal/product-terms)

**(Medium Confidence)** Recent empirical work is moving from “do people like data stories?” toward task-specific comprehension, trust, misleadingness and accessibility. Results increasingly separate perceived clarity from actual comprehension and trust from visual polish.

<INFERENCE from="browser animation APIs, INP, recent trust/comprehension studies and newsroom component practice">The trajectory favors a compiler-like report skill: validated evidence records become semantic HTML, narrative states, subject-specific visualizations and optional enhancements, with automated accessibility/performance/provenance checks. It does not favor a prompt-to-hero-animation generator.</INFERENCE>

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Martini glass, interactive slideshow and drill-down are established narrative structures | Segel & Heer | 2010 | Peer-reviewed systematic analysis of 58 examples; foundational direct taxonomy | https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf |
| Parallelism and transition consistency can benefit narrative sequence reception | Hullman et al. | 2013 | Peer-reviewed corpus analysis plus user studies; direct sequence evidence | https://pubmed.ncbi.nlm.nih.gov/24051807/ |
| Animation improves tracking between related chart states, with limits | Heer & Robertson | 2007 | Peer-reviewed controlled experiments; direct perception/error measures | https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf |
| Animation has no general advantage over equivalent static graphics | Tversky, Morrison & Bétrancourt | 2002 | Peer-reviewed research review; direct competing evidence | https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf |
| Narrative introduction did not increase exploratory interaction | Boy, Détienne & Fekete | 2015 | Peer-reviewed field experiments; direct behavioral measure | https://researchportal.ip-paris.fr/fr/publications/storytelling-in-information-visualizations-does-it-engage-users-t/ |
| Visuals and navigation feedback affect engagement more consistently than control level | McKenna et al. | 2017 | Peer-reviewed corpus, exploratory studies and 240-person experiment | https://onlinelibrary.wiley.com/doi/10.1111/cgf.13195 |
| Slideshow clicking was easier than the tested slow scrollytelling implementation | Mittenentzwei et al. | 2023 | Peer-reviewed between-subject study with 85 participants; implementation-specific | https://vis.test.uib.no/wp-content/papercite-data/pdfs/mittenentzwei2023userbehavior.pdf |
| Scrollytelling improved policy-reading experience but not objective comprehension | Méndez & Such | 2026 | Preprint, randomized online study with 454 participants; recent but not yet peer-reviewed | https://arxiv.org/abs/2603.04367 |
| Titles, text and recognizable imagery support recognition and recall | Borkin et al. | 2015 | Peer-reviewed eye-tracking and recall study; direct cognitive measures | https://vcg.seas.harvard.edu/files/pfister/files/infovis_submission251-camera.pdf |
| Citation click-through is rare and lower on mobile | Piccardi et al. | 2020 | Peer-reviewed large-scale behavioral instrumentation; direct click data | https://arxiv.org/abs/2001.08614 |
| Transparency indicators can modestly improve perceived news trust | Center for Media Engagement | 2018 | Randomized experiment with 1,183 adults; bundled treatment limits attribution | https://mediaengagement.org/research/trust-in-online-news/ |
| Source attribution affects visualization credibility judgments | Li et al. | 2018 | Peer-reviewed experiment with 517 participants; direct credibility measure | https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/ |
| Source clarity and context influence visualization trust | Tong | 2024 | Peer-reviewed qualitative audience study; suitable for mechanisms, not prevalence estimates | https://journals.sagepub.com/doi/10.1177/14648849231190725 |
| Reusable componentized, pre-renderable scrollytelling is documented newsroom practice | ONS Digital | 2021 | Government newsroom production write-up and public code; authoritative practice evidence | https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/ |
| Mobile scrollytelling sometimes should become stacked charts | The Pudding | 2017 | Independent data-journalism production post-mortem; direct practitioner evidence | https://pudding.cool/process/responsive-scrollytelling/ |
| Core Web Vitals good thresholds are LCP 2.5 s, INP 200 ms, CLS 0.1 at p75 | web.dev | Living, updated | Official metric documentation; authoritative technical threshold | https://web.dev/articles/defining-core-web-vitals-thresholds |
| Long tasks exceed 50 ms and smooth 60 fps targets 16.7 ms frames | web.dev / MDN | Living, updated | Official browser performance documentation | https://web.dev/articles/optimize-long-tasks |
| ScrollTrigger provides synchronized scroll orchestration and reduced-motion branching | GSAP | Living | First-party API documentation; authoritative behavior, not effectiveness evidence | https://gsap.com/docs/v3/Plugins/ScrollTrigger/ |
| On-demand three.js rendering avoids unnecessary power use | three.js | Living | First-party implementation guidance; authoritative library practice | https://threejs.org/manual/en/rendering-on-demand.html |
| WebGL needs bounded resources and context-loss handling | MDN | 2025 update | Browser-platform guidance; authoritative implementation constraints | https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices |
| Scroll-linked motion can trigger vestibular symptoms | W3C WAI | 2025 update | Official WCAG understanding document; accessibility authority | https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions |
| Complex visualizations require equivalent text descriptions | W3C WAI | 2026 update | Official accessibility tutorial grounded in WCAG | https://www.w3.org/WAI/tutorials/images/complex/ |
| Scrolljacking reduces accuracy and satisfaction | Murano | 2026 | Peer-reviewed controlled usability study; small sample of 20 | https://doi.org/10.1007/978-3-032-16454-4_6 |
| Truncated bar axes persistently exaggerate perceived differences | Okan et al. | 2021 | Peer-reviewed five-study program; direct perception evidence | https://doi.org/10.1016/j.jarmac.2020.10.002 |
| Readers have difficulty detecting common chart-construction errors | Hopkins, Correll & Satyanarayan | 2020 | Peer-reviewed empirical visualization study | https://vis.mit.edu/pubs/visualint/ |
| Reusable story formats work when tied to reader needs | Financial Times/OpenNews | 2019 | Named newsroom production account; direct organizational practice | https://source.opennews.org/articles/story-templates-financial-times-reusable/ |

## Knowledge Gaps

### Missing comparative experiments

`<MISSING_DATA>[Large preregistered comparisons of evidence-dense static reports, scrollytelling, steppers and drill-down pages using identical content were sought. Existing studies vary in topic, implementation and outcome measures. A multi-condition study measuring comprehension, delayed recall, decision quality and completion is needed.]</MISSING_DATA>`

`<MISSING_DATA>[Direct newsroom evidence that three.js/WebGL improves comprehension over the best 2D treatment was sought. Most available evidence concerns specialized spatial, medical, immersive or network tasks rather than public web reports.]</MISSING_DATA>`

### Missing production thresholds

`<MISSING_DATA>[Universal limits for JavaScript transfer size, number of ScrollTriggers, simultaneous tweens, WebGL draw calls, polygons, texture memory and device-pixel ratio were unavailable. These depend on the target device distribution and visual implementation; field telemetry is required.]</MISSING_DATA>`

### Citation UX uncertainty

`<INSUFFICIENT_EVIDENCE>[No strong causal study was found comparing inline links, numbered footnotes, hover previews, click popovers and side panels for claim verification in long-form visual reports. Wikipedia behavior establishes low verification rates and correlates, not the optimal interface.]</INSUFFICIENT_EVIDENCE>`

### Authorship and visual sameness

`<INSUFFICIENT_EVIDENCE>[No validated metric distinguishes an authored family resemblance from recognisable template sameness across report pages. Screenshot similarity, layout-silhouette comparison and subject-metaphor review are defensible heuristics but need user validation.]</INSUFFICIENT_EVIDENCE>`

### Accessibility in real scrollytelling systems

`<MISSING_DATA>[WCAG supplies clear requirements, but comparative testing of production scrollytelling with VoiceOver, NVDA, TalkBack, keyboard navigation, zoom and reduced motion remains sparse. A task-based assistive-technology study is needed.]</MISSING_DATA>`

## Recommended Next Steps

1. **Build one corpus into four controlled prototypes.** Produce static long-form, stepper, 2D scrollytelling and—only if spatially justified—3D scrollytelling versions. Test immediate comprehension, delayed recall, task accuracy, completion and source verification. This resolves the largest causal gap.

2. **Turn the inferred rules into compiler checks.** Validate clause-level citations, inference labels, one-claim states, deterministic state rendering, chart axes/units, text alternatives, reduced-motion parity, keyboard access, CWV thresholds and 50-millisecond long tasks. The rationale is to make trust and accessibility release conditions rather than review suggestions.

3. **Run a citation-affordance experiment.** Randomize direct inline links, numbered footnotes, popovers and an evidence side panel; measure source-preview use, external opens, successful claim verification and reading disruption. Existing research does not identify a winning interaction.

4. **Establish device-tier motion and WebGL budgets.** Profile representative low-end mobile, median mobile and desktop devices; collect field LCP, INP, CLS, long-animation-frame, memory/context-loss and reduced-motion data. This is the only defensible way to obtain numeric scene limits.

5. **Create a cross-report authorship audit.** Store full-page, grayscale and blurred screenshots plus structural state maps for previous reports. Require a reviewer to identify subject-native visual primitives and justify every repeated layout. Then test whether readers perceive new pages as distinct, coherent and appropriate rather than merely recolored.
tokens used
256,853
## Executive Summary

- **(High Confidence)** Build the report as a linear, server-rendered document first. Use scroll states to guide attention through successive claims, then optionally open into exploration—the “martini-glass” structure. Reserve slideshows for bounded branches and drill-down for audiences arriving with their own questions. Segel and Heer derived these structures from 58 narrative visualizations. [scivis.github.io](https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf)[Segel & Heer (2010)](https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf)

- **(High Confidence)** Enforce one claim per scroll state. Text should be short enough to coexist with its visual; transitions should preserve landmarks and change only the variables needed to communicate that claim. ONS reports that this format works best when presenting one point at a time; controlled animation research similarly favors simple staging over elaborate multi-stage movement. [digitalblog.ons.gov.uk](https://digitalblog.ons.gov.uk/2021/05/24/what-makes-for-a-good-scrollytelling-article/)[ONS Digital (2021)](https://digitalblog.ons.gov.uk/2021/05/24/what-makes-for-a-good-scrollytelling-article/) [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson (2007)](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)

- **(High Confidence)** Animation helps when it explains a transformation: tracking the same entity, sorting, filtering, rescaling, changing time, or moving through genuine space. It does not reliably improve general learning, recall, exploration, or trust. In one controlled study with 24 participants, animated transitions reduced perception errors, but extreme staging sometimes performed worse; broader reviews found no general advantage over informationally equivalent static diagrams. [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson (2007)](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf) [tc.columbia.edu](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)[Tversky, Morrison & Bétrancourt (2002)](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)

- **(High Confidence)** Put a citation beside the exact claim it supports, with a low-friction popover containing source title, author/publisher, date, evidence type, and a direct link. Also provide a deduplicated source list and methods/limitations section. Do not assume readers will verify: Wikipedia instrumentation found an external-reference click in only 0.29% of page views, although merely showing sources and reporting practices can increase perceived trust. [arxiv.org](https://arxiv.org/abs/2001.08614)[Piccardi et al. (2020)](https://arxiv.org/abs/2001.08614) [mediaengagement.org](https://mediaengagement.org/research/trust-in-online-news/)[Center for Media Engagement](https://mediaengagement.org/research/trust-in-online-news/)

- **(High Confidence)** Use GSAP ScrollTrigger as an orchestration layer over native scrolling—not as a replacement for scrolling. The release floor should be field Core Web Vitals at the 75th percentile: LCP ≤2.5 seconds, INP ≤200 milliseconds and CLS ≤0.1; animated frames should target 16.7 milliseconds, with no main-thread task over 50 milliseconds. [web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds)[web.dev Core Web Vitals thresholds](https://web.dev/articles/defining-core-web-vitals-thresholds) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long)[MDN performance timings](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long)

- **(High Confidence)** three.js earns inclusion only if the claim depends on inherently three-dimensional structure, viewpoint, occlusion, volume, or spatial continuity—and a prototype performs better than the best 2D explanation on comprehension or task accuracy. Decorative depth, particle fields, rotating logos, and generic “immersive” scenes fail this test. Every 3D state must have an equivalent DOM/2D fallback.

- **(High Confidence)** Accessibility is architectural. The full narrative and data must exist in meaningful DOM order; charts need short and long descriptions or data tables; all interactions need keyboard equivalents; non-essential motion must honor `prefers-reduced-motion`; and continuous or scroll-started movement may require pause/stop controls under WCAG 2.2.2 and 2.3.3. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions)[W3C: Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions) [w3.org](https://www.w3.org/WAI/tutorials/images/complex/)[W3C: Complex Images](https://www.w3.org/WAI/tutorials/images/complex/)

- **(Medium Confidence)** Reuse an engineering chassis, not an aesthetic template. The shared layer should provide semantics, citations, responsive scrollytelling, accessibility and observability; each topic should derive its typography, visual primitives, chart grammar and motion from the subject. `<INSUFFICIENT_EVIDENCE>There is no validated metric for “recognisably templated” report pages; the recommended similarity tests below are production heuristics.</INSUFFICIENT_EVIDENCE>`

## Detailed Findings

### 1. How do practitioners build single-page, evidence-dense scrollytelling reports, and what measurably works versus fails?

#### Narrative architecture and production pattern

**(High Confidence)** Segel and Heer distinguish author-driven narration from reader-driven exploration and identify three hybrid structures:

| Structure | Control pattern | Best use | Principal failure |
|---|---|---|---|
| Martini glass | Linear author-led sequence, followed by open exploration | Establish context and evidence before offering filtering, comparison or personalization | Exploration is bolted on without explaining what readers can learn from it |
| Interactive slideshow | Author controls chapter order; reader interacts inside bounded scenes | Discrete cases, alternatives, stages or small branches | Hidden “next” controls, no backtracking, content trapped behind clicks |
| Drill-down | Reader chooses sequence and depth | Reference material and expert audiences with distinct questions | No defensible editorial through-line; important evidence can remain undiscovered |

These structures and seven visual genres were derived from 58 examples rather than a controlled effectiveness experiment. [scivis.github.io](https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf)[Segel & Heer (2010)](https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf)

**(High Confidence)** Later sequence research analyzed 42 professional narrative visualizations and found memory and preference benefits from sequences using parallelism—repeated structural relationships that let readers compare states—while emphasizing consistency between adjacent visualizations. [pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24051807/)[Hullman et al. (2013)](https://pubmed.ncbi.nlm.nih.gov/24051807/)

**(High Confidence)** ONS’s production practice uses a reusable component chassis for layout, navigation, charts and maps, but connects changing text, maps and charts through article-specific state. It also identified pre-rendered HTML as necessary for wider compatibility, JavaScript-disabled reading and search indexing. [digitalblog.ons.gov.uk](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/)[ONS Digital: How we build scrollytelling articles](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/)

**(High Confidence)** The Pudding’s post-mortems add three practical constraints: state transitions must be idempotent because readers skip rapidly across steps; mobile may need stacked static charts when transitions do not carry meaning; and hover-dependent annotation should become visible text or explicit controls on touch devices. [pudding.cool](https://pudding.cool/process/how-to-make-dope-shit-part-3/)[The Pudding: Making Internet Things](https://pudding.cool/process/how-to-make-dope-shit-part-3/) [pudding.cool](https://pudding.cool/process/responsive-scrollytelling/)[The Pudding: Responsive scrollytelling](https://pudding.cool/process/responsive-scrollytelling/)

<INFERENCE from="Segel & Heer’s three structures; Hullman et al.’s sequence findings; ONS one-point-at-a-time guidance; The Pudding’s fast-scroll failure report">**Skill rule:** compile the research corpus into a claim graph before designing the page. Each scroll state receives exactly one primary claim, one visual question and one stable end-state. Adjacent states should reuse objects, scales and spatial positions unless changing one of those is itself the evidence.</INFERENCE>

A reliable default narrative is:

1. **Contract:** headline conclusion, scope, update date and evidence quality.
2. **Orientation:** define the system or dataset and show the stable visual frame.
3. **Progressive proof:** one claim per state, ordered context → mechanism → consequence.
4. **Complication:** conflicting evidence, uncertainty and scope limits.
5. **Synthesis:** answer the stated decision.
6. **Exploration:** filters, comparisons, underlying table or drill-down.
7. **Provenance:** methods, limitations, sources, corrections and version history.

This is an inferred production pattern rather than an experimentally validated universal sequence. `<INFERENCE from="Segel & Heer’s martini-glass structure; ONS’s stepwise explanation; Center for Media Engagement transparency study">The order preserves an editorial argument while leaving audit and exploration available after the core evidence has been understood.</INFERENCE>`

#### What animation improves—and what it does not

**(High Confidence)** Heer and Robertson tested static, direct-animated and staged-animated transitions with 24 participants. Their object-tracking animations lasted 1.25 seconds and value-change animations lasted 2 seconds. Animated conditions reduced tracking error across all tested transition types (`p < 0.001`), while semantic value-estimation benefits varied by chart. [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson (2007)](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)

**(High Confidence)** More staging was not monotonically better. Extreme staging was worse than direct animation for donut-chart value changes (`p = 0.024`), and stacked bars showed no significant animation condition effect (`p = 0.224`). Axis rescaling increased errors and “unknown” responses; retaining common scales and persistent landmarks was preferable. [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson (2007)](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)

**(High Confidence)** Tversky, Morrison and Bétrancourt’s review found no general learning advantage for animation when static and animated treatments contained equivalent information. Animation frequently failed because it was transient, too fast or too complex to apprehend; it was most defensible for genuine temporal change, transformation, causal sequence and spatial reorientation. [tc.columbia.edu](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)[Tversky, Morrison & Bétrancourt (2002)](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)

**(Medium Confidence)** McKenna et al.’s 240-participant study found that visuals and navigation feedback, including static versus animated transitions, affected engagement, while discrete versus continuous control may not. This supports useful feedback, but not a general claim that continuous scrollytelling outperforms steppers. [onlinelibrary.wiley.com](https://onlinelibrary.wiley.com/doi/10.1111/cgf.13195)[McKenna et al. (2017)](https://onlinelibrary.wiley.com/doi/10.1111/cgf.13195)

**(High Confidence)** Three field experiments found that adding an introductory story to exploratory visualizations did not increase subsequent exploratory interaction. Narrative consumption and exploratory engagement therefore need separate success metrics. [researchportal.ip-paris.fr](https://researchportal.ip-paris.fr/fr/publications/storytelling-in-information-visualizations-does-it-engage-users-t/)[Boy, Détienne & Fekete (2015)](https://researchportal.ip-paris.fr/fr/publications/storytelling-in-information-visualizations-does-it-engage-users-t/)

**(Medium Confidence)** A 2023 comparison involving 85 participants found slideshow clicking easier and more intuitive than the study’s scrollytelling implementation; its knowledge checks were near ceiling and could not distinguish comprehension. The authors noted that their slow fade-out/fade-in scroll implementation differed from normal newsroom scrolling. [vis.test.uib.no](https://vis.test.uib.no/wp-content/papercite-data/pdfs/mittenentzwei2023userbehavior.pdf)[Mittenentzwei et al. (2023)](https://vis.test.uib.no/wp-content/papercite-data/pdfs/mittenentzwei2023userbehavior.pdf)

**(Medium Confidence)** A 2026 preprint with 454 participants found scrollytelling improved reported engagement, clarity and cognitive load over full privacy-policy text, while comprehension and confidence were broadly equivalent and trust changes were statistically inconclusive. [arxiv.org](https://arxiv.org/abs/2603.04367)[Méndez & Such (2026 preprint)](https://arxiv.org/abs/2603.04367)

| Outcome | Strongest finding | Confidence | Build consequence |
|---|---|---:|---|
| Object tracking | Animation preserves correspondence between related marks | High | Animate persistent objects rather than replacing the whole scene |
| Change estimation | Helps for some transitions; rescaling and over-staging undermine it | High | Keep scales fixed; separate only necessary transformations |
| General comprehension | Mixed; often equal to good static explanations | Medium | Require comprehension testing, not preference alone |
| Recall | Titles, meaningful text, recognizable objects and structural parallelism help | Medium–High | Give every visual an editorial title and stable semantic landmarks |
| Engagement | Visuals and feedback can help; narrative does not guarantee exploration | Medium | Measure completion and exploration separately |
| Trust | Source visibility and transparency help perceived trust; motion does not establish truth | High | Treat provenance as content, not decoration |

**(High Confidence)** Borkin et al. studied 393 visualizations, eye movements from 33 participants and thousands of descriptions. Titles and supporting text materially supported recognition and recall; recognizable objects appeared in 74% of the most recognizable third but 8% of the least recognizable third. [vcg.seas.harvard.edu](https://vcg.seas.harvard.edu/files/pfister/files/infovis_submission251-camera.pdf)[Borkin et al. (2015)](https://vcg.seas.harvard.edu/files/pfister/files/infovis_submission251-camera.pdf)

<INFERENCE from="Heer & Robertson’s object-continuity result; Tversky et al.’s congruence/apprehension principles; Borkin et al.’s title and object findings">**Motion test:** an animation is admissible only when a reviewer can finish the sentence “This motion lets the reader perceive ___ that would otherwise require a difficult mental comparison.” If the blank is “energy,” “delight,” “premium quality” or “immersion,” it is decoration and does not consume the evidence-motion budget.</INFERENCE>

#### Citation, provenance and trust UX

**(High Confidence)** Citation presence and citation verification are different outcomes. Piccardi et al. instrumented 96 million Wikipedia citation-related events over two months and found reference clicks in 0.29% of page views: 0.56% on desktop and 0.13% on mobile. Ninety-three percent of citation links received no click during the measured month. Open-access and recent sources were more likely to be opened. [arxiv.org](https://arxiv.org/abs/2001.08614)[Piccardi et al. (2020)](https://arxiv.org/abs/2001.08614)

**(Medium Confidence)** Citation clicks were more common on shorter and lower-quality Wikipedia pages, suggesting that readers verify when the page itself fails to meet an information need—not merely because a reference marker is visible. This is observational, not causal. [arxiv.org](https://arxiv.org/abs/2001.08614)[Piccardi et al. (2020)](https://arxiv.org/abs/2001.08614)

**(Medium Confidence)** In a randomized experiment with 1,183 adults, a bundle containing inline footnotes, author information, story type, reporting-method disclosure and organizational standards produced small but statistically significant improvements on four of 15 organizational evaluations. The experiment cannot isolate which indicator caused the effect. [mediaengagement.org](https://mediaengagement.org/research/trust-in-online-news/)[Center for Media Engagement](https://mediaengagement.org/research/trust-in-online-news/)

**(Medium Confidence)** An experiment with 517 participants found that source attribution affected perceived credibility and interacted with prior trust in the named institution; actual comprehension did not reliably predict perceived credibility. [jcom.sissa.it](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/)[Li et al. (2018)](https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/)

**(Medium Confidence)** Qualitative research on COVID-19 visualizations found clear source identification, correct presentation and contextual notes supported trust; participants frequently said they would not inspect the data even though source links reassured them. Likability did not correspond with trustworthiness. [journals.sagepub.com](https://journals.sagepub.com/doi/10.1177/14648849231190725)[Tong (2024)](https://journals.sagepub.com/doi/10.1177/14648849231190725)

<INFERENCE from="low Wikipedia citation click-through; transparency-indicator experiment; source-attribution and visualization-trust studies">**Citation UI rule:** place an atomic marker immediately after the supported clause. Activating it should open an inline popover—not navigate immediately—with: source title; author/publisher; publication date; evidence type; the specific table/page/section; a one-sentence statement of what the source supports; and “Open original.” Keyboard activation, focus return and escape-to-close are mandatory.</INFERENCE>

<INFERENCE from="same trust and citation findings">The final source list should deduplicate records and expose source tier, publication date, access date, relevant claims and limitations. A methods panel should disclose corpus construction, excluded evidence, conflicts, transformations, corrections and report version. Source visibility must never be treated as evidence that a claim was verified.</INFERENCE>

For the Claude Code skill, every claim should be represented internally as:

```text
claim_id
claim_text
confidence
direct_or_inference
source_ids[]
supporting_excerpt_or_data_location
scope_and_limitations
visual_state_ids[]
```

<INFERENCE from="Hullman & Diakopoulos on additions/omissions at data, visual, annotation and interaction layers; the documented rarity of verification">A build must fail if a quantitative or attributed claim lacks a source, if a cited source supports only a nearby proposition, or if an inference is rendered as a direct finding.</INFERENCE> [vis.csail.mit.edu](https://vis.csail.mit.edu/classes/6.859/readings/pdfs/Hullman-VisualizationRhetoric.pdf)[Hullman & Diakopoulos (2011)](https://vis.csail.mit.edu/classes/6.859/readings/pdfs/Hullman-VisualizationRhetoric.pdf)

#### GSAP, browser performance and the motion budget

| Layer | Primary job | Runtime model | Main risk | Required fallback | License/status |
|---|---|---|---|---|---|
| Semantic HTML/CSS | Full report, headings, tables, citations and reading order | Server-rendered/static | None specific to scrollytelling | This is the baseline | Web standards |
| CSS scroll-driven animation | Simple compositor-friendly progress effects | Browser scroll/view timelines | Incomplete browser support | Static styles or GSAP enhancement | W3C Working Draft; `animation-timeline` not Baseline in 2026 [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)[MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline) |
| GSAP + ScrollTrigger | State orchestration, pinned figures, timelines, responsive/reduced-motion branches | JavaScript coordinated with refresh frames | Main-thread work, pinning errors, altered scrolling | Plain document and stacked visuals | Free for permitted commercial use since April 2025; visual-animation-builder competitors are restricted [webflow.com](https://webflow.com/legal/product-terms)[GSAP licence](https://webflow.com/legal/product-terms) |
| SVG/Canvas | Charts and custom 2D marks | DOM or bitmap rendering | Large DOM, paint cost, inaccessible bitmap | Text summary and table | Web standards |
| three.js/WebGL | Genuine spatial or volumetric explanation | GPU render loop plus JS scene orchestration | Payload, GPU/VRAM, battery, context loss, inaccessible canvas | 2D/static equivalent | MIT [threejs.org](https://threejs.org/license/)[three.js licence](https://threejs.org/license/) |

**(High Confidence)** ScrollTrigger calculates trigger positions, synchronizes updates with screen refresh, supports native media queries, and does not require scroll replacement. Its `normalizeScroll()` option explicitly forces scrolling onto the JavaScript thread; that capability should be prohibited by default in this reporting system. [gsap.com](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)[GSAP ScrollTrigger documentation](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)

**(High Confidence)** Native CSS scroll timelines can run supported effects off the main thread, but `animation-timeline` remained a limited-availability feature in April 2026. It is suitable as an enhancement, not as the only mechanism conveying report meaning. [developer.chrome.com](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)[Chrome scroll-driven animation documentation](https://developer.chrome.com/docs/css-ui/scroll-driven-animations) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)[MDN compatibility status](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)

**(High Confidence)** INP does not directly measure scrolling or hovering. Nevertheless, script evaluation, rendering and JavaScript animation can occupy the main thread and delay a subsequent click, tap or keypress, thereby degrading INP. [web.dev](https://web.dev/articles/inp)[web.dev: INP](https://web.dev/articles/inp) [web.dev](https://web.dev/articles/optimize-input-delay)[web.dev: Optimize input delay](https://web.dev/articles/optimize-input-delay)

##### Release performance budget

| Metric | Mandatory floor | Diagnostic interpretation |
|---|---:|---|
| LCP | ≤2.5 s at field p75 | Hero imagery, fonts or early 3D must not delay primary content |
| INP | ≤200 ms at field p75 | No expensive state construction or interaction callback |
| CLS | ≤0.1 at field p75 | Pre-allocate charts, canvases, citations and sticky regions |
| Frame time | ≤16.7 ms target | Sustained 60 fps; MDN estimates roughly 10 ms remains after browser rendering work |
| Main-thread task | <50 ms | Anything longer is formally a long task and can block interaction |
| Reduced-motion reading | 100% content parity | No claim exists only inside an animated intermediate frame |
| JavaScript-disabled/static reading | Core narrative complete | Enhancements may disappear; evidence may not |

Threshold sources: [web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds)[web.dev Core Web Vitals](https://web.dev/articles/defining-core-web-vitals-thresholds) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long)[MDN performance timings](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long) [web.dev](https://web.dev/articles/optimize-long-tasks)[web.dev long tasks](https://web.dev/articles/optimize-long-tasks)

`<MISSING_DATA>[A universal JavaScript-kilobyte, animation-count, polygon-count or texture-megabyte budget was sought. No authoritative limit generalizes across devices, scenes and network conditions. Device-tier testing and field telemetry are required.]</MISSING_DATA>`

<INFERENCE from="Core Web Vitals thresholds; 16.7 ms frame target; 50 ms long-task definition; animation-comprehension evidence">**Motion budget:** count semantic transformations, not tweens. One scroll state may contain multiple coordinated marks, but they must express one change. A transition fails review if it changes unrelated dimensions, loses landmarks, cannot be understood when scrubbed quickly in either direction, creates a long task, or conveys information only while in motion.</INFERENCE>

Recommended ScrollTrigger practice:

- Use normal document scrolling and CSS `position: sticky` where possible.
- Build one timeline per coherent visual chapter, not one trigger per individual mark.
- Make every state renderer deterministic from `stateId`; never depend on previous animations having completed.
- Use `scrub` only when animation progress has a meaningful continuous relationship to scroll position.
- Prefer a triggered transition into a stable state for discrete claims.
- Animate `transform` and `opacity`; avoid per-frame layout and paint. [web.dev](https://web.dev/articles/animations-and-performance)[web.dev animation performance](https://web.dev/articles/animations-and-performance)
- Use `gsap.matchMedia()` for mobile, desktop and `prefers-reduced-motion`; clean up timelines when conditions change. [gsap.com](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29/)[GSAP matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29/)
- Lazy-load noncritical chapters, but never delay text or citation availability.
- Test rapid forward/back scrolling, browser zoom, font loading, orientation changes and history restoration.

#### When three.js earns its place

<INFERENCE from="3D occlusion research; three.js/WebGL resource costs; animation congruence principle">three.js should pass all four gates below. Failure at any gate selects SVG, Canvas, CSS or a static figure instead.</INFERENCE>

1. **Semantic necessity:** the evidence is intrinsically spatial or volumetric, or the claim depends on viewpoint, occlusion, depth, topology, rotation or continuous movement through space.
2. **Comparative value:** a prototype beats the best 2D alternative on comprehension, accuracy, completion time or error—not merely preference.
3. **Operational fitness:** it meets the same CWV and frame budgets on the target mobile tier, with capped pixel ratio, compressed assets and bounded draw calls/VRAM.
4. **Equivalent fallback:** a static image, 2D projection, table and narrative description communicate the conclusion when WebGL, motion or JavaScript is unavailable.

**(High Confidence)** three.js recommends on-demand rendering for non-continuously animated scenes because an unconditional render loop wastes power and battery. [threejs.org](https://threejs.org/manual/en/rendering-on-demand.html)[three.js: Rendering on Demand](https://threejs.org/manual/en/rendering-on-demand.html)

**(High Confidence)** WebGL guidance recommends batching draw calls, reducing back-buffer resolution where appropriate, bounding VRAM use and handling context loss. Textures, geometries and materials require explicit disposal in three.js. [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)[MDN WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices) [threejs.org](https://threejs.org/manual/en/how-to-dispose-of-objects.html)[three.js disposal guide](https://threejs.org/manual/en/how-to-dispose-of-objects.html)

**(Medium Confidence)** 3D is not generally superior for abstract data: systematic work identifies occlusion, clutter, distortion and scalability as persistent trade-offs, while a network study found 2D better for spatial-memory tasks. [arxiv.org](https://arxiv.org/abs/2001.06462)[Kwon et al. (2020)](https://arxiv.org/abs/2001.06462)

Practical defaults are therefore: dynamic-import three.js after narrative content; use glTF/GLB; render only while visible or changing; cap device pixel ratio based on measured device performance; avoid dynamic shadows and post-processing unless evidential; monitor `renderer.info`; dispose resources between chapters; and replace the canvas immediately on `webglcontextlost`. [threejs.org](https://threejs.org/manual/en/loading-3d-models.html)[three.js model workflow](https://threejs.org/manual/en/loading-3d-models.html) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/webglcontextlost_event)[MDN context-loss event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/webglcontextlost_event)

#### Accessibility floor

| Requirement | Applied rule | Relevant WCAG |
|---|---|---|
| Reading order | Full story exists in meaningful DOM order; sticky positioning must not alter source order | 1.3.1, 1.3.2 |
| Charts/maps/3D | Short description plus structured long description or accessible data table | 1.1.1 |
| Keyboard | Every filter, popover, playback and exploration function works without pointer timing | 2.1.1, 2.1.2 |
| Motion | Honor `prefers-reduced-motion`; provide a visible site-level motion toggle | 2.3.3 AAA; responsible floor even where AAA is not contractual |
| Continuous movement | Pause, stop or hide automatically or scroll-started movement lasting over five seconds alongside content | 2.2.2 A |
| Flashing | Never exceed the flash thresholds | 2.3.1 |
| Focus | Citation popovers and dialogs receive focus and return it to the invoking control | 2.4.3, 2.4.7, 2.4.11 |
| Visual encoding | Do not use color alone; maintain text and non-text contrast | 1.4.1, 1.4.3, 1.4.11 |
| Reflow | No required two-dimensional scrolling at 400% zoom except legitimately two-dimensional data | 1.4.10 |
| Dynamic results | Announce meaningful changes without moving focus unnecessarily | 4.1.3 |

W3C explicitly identifies scroll-triggered parallax as a possible vestibular trigger and recommends eliminating non-essential movement, providing a control, or respecting reduced-motion preferences. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions)[W3C WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions)

W3C’s complex-image guidance requires a short identifier plus a long textual representation of essential chart, map or diagram information; structured data should remain structured rather than compressed into `aria-describedby`. [w3.org](https://www.w3.org/WAI/tutorials/images/complex/)[W3C Complex Images](https://www.w3.org/WAI/tutorials/images/complex/)

<INFERENCE from="WCAG meaningful sequence, keyboard access and complex-image guidance">Scroll observation must never be the only state machine available to assistive technology. Screen-reader users should encounter the claims, descriptions and tables as ordinary document content; exploratory controls should be native controls with explicit names and states.</INFERENCE>

#### Documented failure modes

| Failure | Evidence | Skill-level prohibition |
|---|---|---|
| Scrolljacking | A 2026 study with 20 participants found no significant speed benefit but significantly lower accuracy and satisfaction with scrolljacking | Never alter wheel/touch distance, direction, momentum or browser history behavior [doi.org](https://doi.org/10.1007/978-3-032-16454-4_6)[Murano (2026)](https://doi.org/10.1007/978-3-032-16454-4_6) |
| Mobile collapse | Practitioners report viewport instability, hover failures and animation/rendering costs | Provide a stacked mobile branch when transitions are not essential |
| Intermediate-state dependency | Readers skip multiple states faster than animations complete | Each state must render directly and idempotently |
| Over-staging | Controlled testing found some elaborate staging less accurate | Prefer the shortest transition that preserves object identity |
| Misleading charts | Across five studies, 83.5% of participants showed a truncation effect; instruction did not eliminate it | Validate axes, units, intervals, baselines, legends and uncertainty [doi.org](https://doi.org/10.1016/j.jarmac.2020.10.002)[Okan et al. (2021)](https://doi.org/10.1016/j.jarmac.2020.10.002) |
| Undetected construction errors | Readers have near-universal difficulty identifying errors such as truncated axes, dual scales and missing legends | Run automated lint plus human statistical review [vis.mit.edu](https://vis.mit.edu/pubs/visualint/)[Hopkins, Correll & Satyanarayan (2020)](https://vis.mit.edu/pubs/visualint/) |
| Attractive but untrustworthy | Likability and trustworthiness did not align in qualitative visualization research | Never use finish quality or interaction as a proxy for evidence quality |
| Claims outrun sources | Narrative design can add, omit and prioritize information at data, visual, annotation and interaction layers | Require clause-level source entailment and explicit inference labels |
| Template sameness | No validated measure found | Reuse code and controls; prohibit default page art direction |

#### What reads as authored rather than generated

**(High Confidence)** The Financial Times built reusable story patterns around specific reader questions rather than generic layouts, introducing each only after it had worked on a prominent story. [source.opennews.org](https://source.opennews.org/articles/story-templates-financial-times-reusable/)[Kwong, Financial Times/OpenNews (2019)](https://source.opennews.org/articles/story-templates-financial-times-reusable/)

<INFERENCE from="FT reader-need templates; Borkin et al.’s distinct recognizable objects; Hullman et al.’s benefit from considering alternative sequences">The shared skill should standardize evidence handling, not appearance. Before rendering, it should generate at least three materially different narrative/visual directions and choose between them using subject fit, evidence fit, mobile feasibility and accessibility.</INFERENCE>

A page should fail the “authored” review if:

- its section silhouette matches the preceding report after colors and copy are removed;
- changing the subject noun leaves the visual metaphor intact;
- motion consists primarily of repeated fade/slide/reveal recipes;
- typography, texture and illustration style are unrelated to the source material;
- the hero is more specific than the evidence beneath it;
- the same chart grammar appears regardless of data type;
- or the page lacks an explicit editorial tension, uncertainty or counterargument.

`<CONFIDENCE:LOW>The proposed grayscale/blurred-screenshot similarity check is a useful production heuristic, not a validated perceptual threshold.</CONFIDENCE:LOW>`

### 2. What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** The mature production model is progressively enhanced, componentized scrollytelling: semantic HTML and reusable accessible primitives underneath; topic-specific charts, maps and narrative states above; JavaScript motion as enhancement. ONS’s published stack and The Pudding’s post-mortems document this operational pattern. [digitalblog.ons.gov.uk](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/)[ONS Digital](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/) [pudding.cool](https://pudding.cool/process/responsive-scrollytelling/)[The Pudding](https://pudding.cool/process/responsive-scrollytelling/)

**(High Confidence)** The strongest causal evidence concerns narrow visual tasks: well-designed animation improves correspondence and change perception between related graphical states. It is not evidence that a fully animated long-form article improves retention, belief accuracy or decision quality. [sites.stat.columbia.edu](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)[Heer & Robertson](https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf)

**(High Confidence)** The strongest standards evidence concerns performance and accessibility: measurable CWV thresholds, compositor-friendly animation, reduced motion, keyboard operability and equivalent text for complex visuals. These can be automated as build gates. [web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds)[web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds) [w3.org](https://www.w3.org/TR/WCAG22/)[WCAG 2.2](https://www.w3.org/TR/WCAG22/)

**(Medium Confidence)** The evidence for better scrollytelling comprehension remains domain-specific and mixed. Recent experiments more consistently show improved experience, perceived clarity or engagement than improved objective comprehension or recall. [arxiv.org](https://arxiv.org/abs/2603.04367)[Méndez & Such (2026 preprint)](https://arxiv.org/abs/2603.04367)

<INFERENCE from="the difference between strong narrow transition studies and mixed whole-article studies">The defensible position is therefore: use scrollytelling to manage attention and explain transformations; prove learning, recall and decision outcomes separately for each report class.</INFERENCE>

### 3. What are the contrasting viewpoints or competing evidence?

`<CONFLICTING_EVIDENCE>[Heer & Robertson found significant benefits for animated transitions between related data graphics, while Tversky, Morrison & Bétrancourt found no general benefit over informationally equivalent static diagrams. The disagreement is principally about task and treatment: object continuity and change perception versus broad system learning.]</CONFLICTING_EVIDENCE>`

`<CONFLICTING_EVIDENCE>[McKenna et al. found visuals and navigation feedback affected engagement, but Boy et al. found introductory narrative did not increase subsequent data exploration. Engagement with the story and exploration of the underlying visualization are different dependent variables.]</CONFLICTING_EVIDENCE>`

`<CONFLICTING_EVIDENCE>[A 2026 privacy-policy preprint found improved experience and equivalent comprehension, while a 2023 medical-visualization study found clicking easier than its slow scrollytelling implementation and could not distinguish comprehension. Topic, implementation quality, participant population and outcome measures differ.]</CONFLICTING_EVIDENCE>`

`<CONFLICTING_EVIDENCE>[Visual embellishment can improve recognition and long-term memorability in some studies, but cartoon styling and hand-drawn fonts reduced perceived credibility in 2025 experiments. Distinctive imagery is not equivalent to arbitrary decoration.]</CONFLICTING_EVIDENCE>` [pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/41264452/)[Song et al. (2025/2026)](https://pubmed.ncbi.nlm.nih.gov/41264452/)

**(High Confidence)** These conflicts do not support a stylistic compromise. They support outcome-specific evaluation: comprehension questions for explanatory states, delayed recall for memorable claims, interaction logs for exploration, citation actions for verification, task accuracy for 3D and field telemetry for performance.

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** INP replaced FID as a Core Web Vital in March 2024, shifting production attention from the first interaction toward responsiveness across the visit. This raises the cost of heavy late-page state construction, charts and WebGL interactions even when initial load appears fast. [web.dev](https://web.dev/blog/inp-cwv-march-12)[web.dev (2024)](https://web.dev/blog/inp-cwv-march-12)

**(High Confidence)** CSS scroll-driven animations entered Chromium in 2023 and offer off-main-thread execution for supported effects, but remained non-Baseline in 2026. The likely trajectory is hybrid: CSS for simple transforms and progress indicators, GSAP for cross-browser narrative orchestration, and static fallbacks throughout. [developer.chrome.com](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)[Chrome for Developers](https://developer.chrome.com/docs/css-ui/scroll-driven-animations) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)[MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)

**(High Confidence)** GSAP’s full plugin set became free for permitted commercial use in April 2025, reducing the procurement argument for building a custom animation engine. Its current licence still restricts using GSAP to create competing visual animation builders, which should be checked if the planned Claude Code skill becomes a commercial visual authoring product. [webflow.com](https://webflow.com/updates/gsap-becomes-free)[Webflow (2025)](https://webflow.com/updates/gsap-becomes-free) [webflow.com](https://webflow.com/legal/product-terms)[Current product terms](https://webflow.com/legal/product-terms)

**(Medium Confidence)** Recent empirical work is moving from “do people like data stories?” toward task-specific comprehension, trust, misleadingness and accessibility. Results increasingly separate perceived clarity from actual comprehension and trust from visual polish.

<INFERENCE from="browser animation APIs, INP, recent trust/comprehension studies and newsroom component practice">The trajectory favors a compiler-like report skill: validated evidence records become semantic HTML, narrative states, subject-specific visualizations and optional enhancements, with automated accessibility/performance/provenance checks. It does not favor a prompt-to-hero-animation generator.</INFERENCE>

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Martini glass, interactive slideshow and drill-down are established narrative structures | Segel & Heer | 2010 | Peer-reviewed systematic analysis of 58 examples; foundational direct taxonomy | https://scivis.github.io/courses/visualstorytelling/segel_heer_2010.pdf |
| Parallelism and transition consistency can benefit narrative sequence reception | Hullman et al. | 2013 | Peer-reviewed corpus analysis plus user studies; direct sequence evidence | https://pubmed.ncbi.nlm.nih.gov/24051807/ |
| Animation improves tracking between related chart states, with limits | Heer & Robertson | 2007 | Peer-reviewed controlled experiments; direct perception/error measures | https://sites.stat.columbia.edu/gelman/communication/HeerRobertson2007.pdf |
| Animation has no general advantage over equivalent static graphics | Tversky, Morrison & Bétrancourt | 2002 | Peer-reviewed research review; direct competing evidence | https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf |
| Narrative introduction did not increase exploratory interaction | Boy, Détienne & Fekete | 2015 | Peer-reviewed field experiments; direct behavioral measure | https://researchportal.ip-paris.fr/fr/publications/storytelling-in-information-visualizations-does-it-engage-users-t/ |
| Visuals and navigation feedback affect engagement more consistently than control level | McKenna et al. | 2017 | Peer-reviewed corpus, exploratory studies and 240-person experiment | https://onlinelibrary.wiley.com/doi/10.1111/cgf.13195 |
| Slideshow clicking was easier than the tested slow scrollytelling implementation | Mittenentzwei et al. | 2023 | Peer-reviewed between-subject study with 85 participants; implementation-specific | https://vis.test.uib.no/wp-content/papercite-data/pdfs/mittenentzwei2023userbehavior.pdf |
| Scrollytelling improved policy-reading experience but not objective comprehension | Méndez & Such | 2026 | Preprint, randomized online study with 454 participants; recent but not yet peer-reviewed | https://arxiv.org/abs/2603.04367 |
| Titles, text and recognizable imagery support recognition and recall | Borkin et al. | 2015 | Peer-reviewed eye-tracking and recall study; direct cognitive measures | https://vcg.seas.harvard.edu/files/pfister/files/infovis_submission251-camera.pdf |
| Citation click-through is rare and lower on mobile | Piccardi et al. | 2020 | Peer-reviewed large-scale behavioral instrumentation; direct click data | https://arxiv.org/abs/2001.08614 |
| Transparency indicators can modestly improve perceived news trust | Center for Media Engagement | 2018 | Randomized experiment with 1,183 adults; bundled treatment limits attribution | https://mediaengagement.org/research/trust-in-online-news/ |
| Source attribution affects visualization credibility judgments | Li et al. | 2018 | Peer-reviewed experiment with 517 participants; direct credibility measure | https://jcom.sissa.it/article/pubid/JCOM_1702_2018_A06/ |
| Source clarity and context influence visualization trust | Tong | 2024 | Peer-reviewed qualitative audience study; suitable for mechanisms, not prevalence estimates | https://journals.sagepub.com/doi/10.1177/14648849231190725 |
| Reusable componentized, pre-renderable scrollytelling is documented newsroom practice | ONS Digital | 2021 | Government newsroom production write-up and public code; authoritative practice evidence | https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/ |
| Mobile scrollytelling sometimes should become stacked charts | The Pudding | 2017 | Independent data-journalism production post-mortem; direct practitioner evidence | https://pudding.cool/process/responsive-scrollytelling/ |
| Core Web Vitals good thresholds are LCP 2.5 s, INP 200 ms, CLS 0.1 at p75 | web.dev | Living, updated | Official metric documentation; authoritative technical threshold | https://web.dev/articles/defining-core-web-vitals-thresholds |
| Long tasks exceed 50 ms and smooth 60 fps targets 16.7 ms frames | web.dev / MDN | Living, updated | Official browser performance documentation | https://web.dev/articles/optimize-long-tasks |
| ScrollTrigger provides synchronized scroll orchestration and reduced-motion branching | GSAP | Living | First-party API documentation; authoritative behavior, not effectiveness evidence | https://gsap.com/docs/v3/Plugins/ScrollTrigger/ |
| On-demand three.js rendering avoids unnecessary power use | three.js | Living | First-party implementation guidance; authoritative library practice | https://threejs.org/manual/en/rendering-on-demand.html |
| WebGL needs bounded resources and context-loss handling | MDN | 2025 update | Browser-platform guidance; authoritative implementation constraints | https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices |
| Scroll-linked motion can trigger vestibular symptoms | W3C WAI | 2025 update | Official WCAG understanding document; accessibility authority | https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions |
| Complex visualizations require equivalent text descriptions | W3C WAI | 2026 update | Official accessibility tutorial grounded in WCAG | https://www.w3.org/WAI/tutorials/images/complex/ |
| Scrolljacking reduces accuracy and satisfaction | Murano | 2026 | Peer-reviewed controlled usability study; small sample of 20 | https://doi.org/10.1007/978-3-032-16454-4_6 |
| Truncated bar axes persistently exaggerate perceived differences | Okan et al. | 2021 | Peer-reviewed five-study program; direct perception evidence | https://doi.org/10.1016/j.jarmac.2020.10.002 |
| Readers have difficulty detecting common chart-construction errors | Hopkins, Correll & Satyanarayan | 2020 | Peer-reviewed empirical visualization study | https://vis.mit.edu/pubs/visualint/ |
| Reusable story formats work when tied to reader needs | Financial Times/OpenNews | 2019 | Named newsroom production account; direct organizational practice | https://source.opennews.org/articles/story-templates-financial-times-reusable/ |

## Knowledge Gaps

### Missing comparative experiments

`<MISSING_DATA>[Large preregistered comparisons of evidence-dense static reports, scrollytelling, steppers and drill-down pages using identical content were sought. Existing studies vary in topic, implementation and outcome measures. A multi-condition study measuring comprehension, delayed recall, decision quality and completion is needed.]</MISSING_DATA>`

`<MISSING_DATA>[Direct newsroom evidence that three.js/WebGL improves comprehension over the best 2D treatment was sought. Most available evidence concerns specialized spatial, medical, immersive or network tasks rather than public web reports.]</MISSING_DATA>`

### Missing production thresholds

`<MISSING_DATA>[Universal limits for JavaScript transfer size, number of ScrollTriggers, simultaneous tweens, WebGL draw calls, polygons, texture memory and device-pixel ratio were unavailable. These depend on the target device distribution and visual implementation; field telemetry is required.]</MISSING_DATA>`

### Citation UX uncertainty

`<INSUFFICIENT_EVIDENCE>[No strong causal study was found comparing inline links, numbered footnotes, hover previews, click popovers and side panels for claim verification in long-form visual reports. Wikipedia behavior establishes low verification rates and correlates, not the optimal interface.]</INSUFFICIENT_EVIDENCE>`

### Authorship and visual sameness

`<INSUFFICIENT_EVIDENCE>[No validated metric distinguishes an authored family resemblance from recognisable template sameness across report pages. Screenshot similarity, layout-silhouette comparison and subject-metaphor review are defensible heuristics but need user validation.]</INSUFFICIENT_EVIDENCE>`

### Accessibility in real scrollytelling systems

`<MISSING_DATA>[WCAG supplies clear requirements, but comparative testing of production scrollytelling with VoiceOver, NVDA, TalkBack, keyboard navigation, zoom and reduced motion remains sparse. A task-based assistive-technology study is needed.]</MISSING_DATA>`

## Recommended Next Steps

1. **Build one corpus into four controlled prototypes.** Produce static long-form, stepper, 2D scrollytelling and—only if spatially justified—3D scrollytelling versions. Test immediate comprehension, delayed recall, task accuracy, completion and source verification. This resolves the largest causal gap.

2. **Turn the inferred rules into compiler checks.** Validate clause-level citations, inference labels, one-claim states, deterministic state rendering, chart axes/units, text alternatives, reduced-motion parity, keyboard access, CWV thresholds and 50-millisecond long tasks. The rationale is to make trust and accessibility release conditions rather than review suggestions.

3. **Run a citation-affordance experiment.** Randomize direct inline links, numbered footnotes, popovers and an evidence side panel; measure source-preview use, external opens, successful claim verification and reading disruption. Existing research does not identify a winning interaction.

4. **Establish device-tier motion and WebGL budgets.** Profile representative low-end mobile, median mobile and desktop devices; collect field LCP, INP, CLS, long-animation-frame, memory/context-loss and reduced-motion data. This is the only defensible way to obtain numeric scene limits.

5. **Create a cross-report authorship audit.** Store full-page, grayscale and blurred screenshots plus structural state maps for previous reports. Require a reviewer to identify subject-native visual primitives and justify every repeated layout. Then test whether readers perceive new pages as distinct, coherent and appropriate rather than merely recolored.
