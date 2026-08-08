---
title: "Engineering Single-Page Scrollytelling Data Journalism Reports"
run_id: dr_2b9923b4dd8b1594
question: "How do practitioners build single-page, evidence-dense scrollytelling web reports — the narrative-visualisation form used by newsroom graphics desks and independent data-journalism sites — and what measurably works versus fails? Cover: (1) documented production patterns and narrative structures for long-form scroll-driven report pages (author-driven vs reader-driven martini-glass / interactive-slideshow / drill-down structures, section pacing, the \"one idea per scroll state\" discipline); (2) empirical findings on comprehension, recall and engagement in narrative visualisation and scrollytelling, including where animation and scroll-linked transitions measurably help understanding and where they measurably hurt; (3) citation, provenance and trust UX in evidence-dense pages — inline citation affordances, footnote/popup patterns, source-list design, and what makes readers actually verify a claim; (4) production practice for GSAP ScrollTrigger and three.js/WebGL on narrative pages: performance budgets, Core Web Vitals and INP impact, scroll-linked animation techniques, WebGL fallbacks and progressive enhancement, and when a 3D scene earns its cost versus being decoration; (5) accessibility for scroll-driven and animated content — prefers-reduced-motion, keyboard and screen-reader access to scroll-triggered content, motion-triggered vestibular disorders, and the WCAG criteria that apply; (6) the documented failure modes: scrolljacking, mobile performance collapse, unlabelled or misleading charts, visual homogeneity and template sameness across pages from one producer, and reports whose claims outrun their sources. Prioritise measured results, published post-mortems from graphics desks, and peer-reviewed narrative-visualisation research over listicles and vendor marketing."
provider: gemini
model: deep-research-max-preview-04-2026
tier: max
archetype: technical
sources: 77
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 7.00
completed: 2026-08-08T04:39:24.783Z
---
# Building Single-Page, Evidence-Dense Scrollytelling Web Reports

Developing an automated agentic skill capable of transforming a multi-backend research corpus into a self-contained, highly credible HTML scrollytelling report requires navigating a precarious tightrope. On one side lies the immersive engagement of narrative visualization; on the other, the catastrophic failure modes of scrolljacking, accessibility exclusion, and mobile performance collapse.

*   Scrollytelling is quantitatively proven to increase reader engagement and data retention, provided it employs strict structural scaffolding rather than free-form visual chaos.
*   Heavy JavaScript scroll listeners (like legacy implementations of GSAP) directly threaten Core Web Vitals—specifically Interaction to Next Paint (INP)—mandating a transition to native CSS scroll-driven animations wherever possible.
*   Integrating 3D elements (Three.js/WebGL) must be justified by explanatory necessity, governed by strict 60fps performance budgets, and equipped with progressive degradation fallbacks to avoid alienating mobile users.
*   Trust in evidence-dense pages relies heavily on methodological transparency and frictionless inline citation UX, moving away from aggregated end-notes that break narrative immersion.

This investigation establishes the citable design rules, performance budgets, and narrative structures required to build an automated scrollytelling generator that avoids the visual homogeneity typical of templated outputs, delivering bespoke, performant, and accessible data journalism.

## Executive Summary

*   **(High Confidence)** The "Martini Glass" narrative structure—beginning with tightly authored, linear storytelling before opening into reader-driven data exploration—is the most consistently effective framework for complex data journalism [cite: 1, 2] `[vis.stanford.edu](http://vis.stanford.edu/papers/narrative)`.
*   **(Medium Confidence)** While raw scrolling interfaces without spatial cues can harm comprehension for users with low working memory, scrollytelling that anchors motion strictly to narrative meaning acts as a tacit tutorial, significantly enhancing factual recall compared to static text formats [cite: 3, 4, 5].
*   **(High Confidence)** Accessibility is a non-negotiable legal and UX floor; any scroll-linked animation must respect the `prefers-reduced-motion` media query to protect users with vestibular disorders, as mandated by WCAG 2.2 guidelines [cite: 6, 7] `[webdesignerindia.medium.com](https://webdesignerindia.medium.com/ui-design-trends-2026-37568f0115f8)`.
*   **(Medium Confidence)** JavaScript-based scroll animation libraries (e.g., GSAP ScrollTrigger) running on the main thread introduce severe Interaction to Next Paint (INP) latency on mid-tier mobile devices, driving a necessary shift toward native CSS `animation-timeline: scroll()` [cite: 8] `[blog.gitbutler.com](https://blog.gitbutler.com/the-great-css-expansion)`.
*   **(High Confidence)** 3D (WebGL/Three.js) is a high-risk inclusion that only "earns its place" when static media cannot effectively convey scale, spatial relationships, or systemic behavior; otherwise, it degrades into decorative bloat that damages trust [cite: 9, 10] `[clodron.com](https://www.clodron.com/en/services/3d-experiences)`.
*   **(Medium Confidence)** The most effective citation UX for evidence-dense pages utilizes inline, expandable footnotes (e.g., the FiveThirtyEight model) that reveal methodological context and sourcing without forcing the reader to lose their place in the narrative flow [cite: 11] `[topfunky.com](https://topfunky.com/2018/good-web-538/)`.
*   **(Medium Confidence)** Automated, LLM-generated narrative visualizations frequently suffer from visual homogeneity and a lack of distinctive authorial voice, making them recognizable as generated templates rather than bespoke journalistic artifacts [cite: 12] `[arxiv.org](https://arxiv.org/html/2606.11176v1)`.

## Answer this decisively: How do practitioners build single-page, evidence-dense scrollytelling web reports — the narrative-visualisation form used by newsroom graphics desks and independent data-journalism sites — and what measurably works versus fails?

To successfully engineer an automated generator of scrollytelling pages, one must codify the often-tacit rules utilized by top-tier newsroom graphics desks. The architecture of these pages can be broken down into critical components: narrative structure, cognitive impact, trust UX, rendering performance, accessibility, the avoidance of known failure modes, and automated operationalization.

### 1. Documented Production Patterns and Narrative Structures

The foundational architecture of narrative visualization relies on balancing authorial control with reader agency. Segel and Heer’s seminal research established the dominant design patterns used by data journalists to guide readers through complex datasets without overwhelming them [cite: 13, 14]. 

The most prominent and effective structural model is the **Martini Glass Structure**. `<INFERENCE from="[cite: 1, 2, 13]">`This model dictates that a page must begin with a tightly authored, linear narrative (the "stem" of the glass) to establish context, explain visual encodings, and present the primary thesis, before "opening up" (the bowl of the glass) into a highly interactive, reader-driven exploratory interface.`</INFERENCE>` [cite: 1, 2, 13] `[computer.org](https://www.computer.org/csdl/journal/tg/2010/06/ttg2010061139/13rRUxAAST1)`. 
*   *Real-World Case Study:* *The New York Times* piece "Steroids Or Not, the Pursuit is On," detailing Major League Baseball home run statistics, expertly utilizes this structure. It guides the reader through a specific chronological analysis of the steroid era before allowing open-ended exploration of the data [cite: 15, 16].



Two other prevalent structures provide alternative pacing mechanisms:
*   **Interactive Slideshow:** The narrative progresses in discrete, locked steps (often using CSS scroll-snapping), allowing mid-narrative interaction within the confines of a single "slide" or scroll-state before moving forward [cite: 2, 15] `[medium.com](https://medium.com/@nikebuzz101/narrative-visualization-data-visualization-on-steroids-935271eab497)`. 
    *   *Real-World Case Study:* Minnesota Public Radio's "The Minnesota Employment Explorer" allows users to determine the pace via a progress bar, pausing the slideshow to mouse-over areas of interest before advancing [cite: 16].
*   **Drill-Down Story:** Presents a macro-level theme (e.g., a national map) and requires the user to select specific micro-instances (e.g., clicking their hometown) to reveal the narrative details [cite: 2, 13] `[medium.com](https://medium.com/@ks157/when-data-becomes-a-story-understanding-narrative-visualization-f31c91bda198)`.

Practitioners also rely on the **Two-Layer Model** of visual storytelling, which separates the *image layer* (composition, contrast, and visual hierarchy within a single frame) from the *sequence layer* (the chronological pacing of charts that walks a reader through cause and effect) [cite: 17] `[storyflow.so](https://storyflow.so/blog/what-is-visual-storytelling-complete-guide)`. A generated page must adhere to the "one idea per scroll state" discipline, ensuring cognitive load remains manageable.

### 2. Empirical Findings on Comprehension, Recall, and Engagement

The utility of scrollytelling is not merely aesthetic; empirical evidence demonstrates a measurable impact on how humans process and retain data. However, the evidence regarding scrolling interfaces is highly contested depending on the cognitive load and execution.

`<CONFLICTING_EVIDENCE>`
*   **Position 1: Scrolling harms comprehension.** Foundational research by Sanchez (2009) demonstrated that raw scrolling formats reduce the understanding of complex topics compared to discrete, paginated text, particularly for readers with lower Working Memory Capacity (WMC), because scrolling strips away spatial and reference cues [cite: 4, 5, 18] `[pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/20196297/)`. 
*   **Position 2: Scrollytelling enhances recall.** Modern empirical studies, such as Tjärnhage (2023), indicate that when scrolling is explicitly linked to narrative visualization (scrollytelling), it leads to significantly more extensive factual recall than audio and static text formats, effectively holding reader attention through controversial or complex policy data [cite: 3, 19] `[researchgate.net](https://www.researchgate.net/publication/374109425_The_Impact_of_Scrollytelling_on_the_Reading_Experience_of_Long-Form_Journalism)`.
`</CONFLICTING_EVIDENCE>`

The synthesis of these findings dictates a strict design rule: **Motion must be anchored to meaning.** Animation aids comprehension when it acts as a "tacit tutorial"—such as drawing a trend line chronologically or highlighting a data cluster—but hurts comprehension when it is purely decorative, as the latter exhausts the user's working memory [cite: 2, 10] `[innoraft.ai](https://www.innoraft.ai/blog/interactive-microsite-design-trends)`.

### 3. Citation, Provenance, and Trust UX

In evidence-dense reports, the user experience of verification is as critical as the visualization itself. Declining public trust in media requires that data journalism shift its credibility markers from perceived institutional authority to observable, transparent methodologies [cite: 20] `[tandfonline.com](https://www.tandfonline.com/doi/full/10.1080/17524032.2026.2668593)`.

Best practices for trust UX completely eschew traditional academic bibliographies clustered at the bottom of a page, as this separates the claim from its evidence [cite: 11, 21] `[topfunky.com](https://topfunky.com/2018/good-web-538/)`. Instead, practitioners employ:
*   **Inline Contextual Footnotes:** Utilizing superscript toggles (e.g., the FiveThirtyEight model) that open small, inline popups or margin notes containing the source link and methodological caveats without forcing the reader to navigate away from the primary narrative flow [cite: 11] `[topfunky.com](https://topfunky.com/2018/good-web-538/)`.
*   **Raw Data Access:** Linking directly to machine-readable public databases or GitHub repositories containing the Jupyter notebooks and scripts used to clean the data, ensuring absolute provenance [cite: 21, 22] `[datajournalism.com](https://datajournalism.com/read/handbook/two/working-with-data/experiencing-data/searchable-databases-as-a-journalistic-product)`.
*   `<MISSING_DATA>`Precise quantitative metrics on exactly what percentage of readers actually click to verify a claim via these inline affordances were sought but unavailable; however, qualitative assessments indicate the mere *presence* of detailed methodological transparency increases baseline perceived trustworthiness [cite: 20].`</MISSING_DATA>`

### 4. Production Practice: GSAP, Three.js, and Performance Budgets

The technical execution of these pages represents the highest risk of failure. A page that takes more than 3 seconds to load will suffer massive bounce rates, neutralizing any narrative effort [cite: 23] `[scrollytelling.ai](https://scrollytelling.ai/what-is-scrollytelling/)`. Specifically, Google research demonstrates that 53% of mobile visitors abandon pages taking longer than 3 seconds. The bounce rate probability increases exponentially: a 32% increase as load time moves from 1 to 3 seconds, a 90% increase from 1 to 5 seconds, and a 106% increase from 1 to 6 seconds [cite: 24, 25, 26, 27]. When analyzing absolute average bounce rates, a 1-second load yields a 9% bounce rate, 3 seconds jumps to 32%, and 10 seconds reaches 65% [cite: 24].



**The Animation Layer and INP Budgets:**
Historically, complex scroll animations relied heavily on JavaScript libraries like GSAP ScrollTrigger. While GSAP remains the industry standard for complex timeline sequencing, running heavy listeners on the browser's main thread blocks other execution tasks. This directly degrades **Interaction to Next Paint (INP)** (a Core Web Vital measuring the millisecond delay between a user's tap, click, or key press and the subsequent visual update on the screen) [cite: 8, 28] `[blog.gitbutler.com](https://blog.gitbutler.com/the-great-css-expansion)`. 

Any JavaScript execution exceeding 50 milliseconds is classified as a "long task" that blocks the main thread [cite: 29, 30, 31]. To achieve a "Good" INP rating under Google's 2026 Core Web Vitals standards, the interaction latency must remain at 200 milliseconds or less for the 75th percentile of user visits [cite: 28, 32, 33, 34]. Interactions taking between 200ms and 500ms are flagged as "Needs Improvement," and anything exceeding 500ms is "Poor" [cite: 33, 35].

The modern standard dictates replacing JS listeners with the native CSS `animation-timeline: scroll()` and `animation-timeline: view()` APIs wherever possible. These run exclusively on the **GPU compositor thread** (a dedicated graphics processing lane that bypasses the main processor, allowing smooth animations without interrupting interactivity), guaranteeing 60fps performance with zero main-thread contention [cite: 8, 36] `[cloudways.com](https://www.cloudways.com/blog/what-is-parallax-scrolling/)`.

**The 3D Layer (WebGL/Three.js) Budgets:**
The inclusion of 3D is a massive performance liability and must pass a strict utility test: **A 3D scene only earns its cost when static media cannot show form, behavior, scale, or the system around it** [cite: 9] `[clodron.com](https://www.clodron.com/en/services/3d-experiences)`. 
When 3D is justified, practitioners enforce rigorous performance budgets:
*   Aggressive asset compression, frequently utilizing **Draco compression** (an open-source library for compressing 3D geometric meshes and point clouds) for **GLTF models** (Graphics Language Transmission Format, a standard file format for 3D scenes).
*   Enforcing a strict 256 MB to 384 MB limit on the WebGL heap memory. Mobile operating systems, particularly iOS Safari, enforce hard limits around 300–500 MB before forcibly crashing the browser tab [cite: 37, 38, 39, 40].
*   Lazy loading 3D canvases only via **Intersection Observers** (a browser API that asynchronously monitors when an element enters or exits the visible screen) [cite: 40, 41, 42].
*   Implementing graceful degradation by detecting GPU capabilities and serving a static image or CSS fallback to lower-end mobile devices [cite: 9, 41] `[designrush.com](https://www.designrush.com/agency/website-design-development/trends/web-design-trends)`.

### 5. Accessibility for Scroll-Driven Content

Visual spectacle that excludes segments of the audience is a failure of both ethics and design. Furthermore, non-compliant pages expose publishers to legal risks under WCAG frameworks.

*   **Vestibular Disorders and `prefers-reduced-motion`:** Approximately 35% of adults over 40 experience some form of vestibular disorder, making them susceptible to motion sickness, nausea, and vertigo triggered by unexpected digital motion (especially parallax and scroll-scrubbing) [cite: 43, 44] `[alistapart.com](https://alistapart.com/article/paint-the-picture-not-the-frame/)`. WCAG 2.2 guidelines strictly mandate that any scroll animation must detect and respect the operating system's `prefers-reduced-motion` media query [cite: 6, 7, 45] `[educationalvoice.co.uk](https://educationalvoice.co.uk/easily-interactive-animations/)`. A compliant page must automatically disable complex interpolations and swap them for static, high-contrast states [cite: 45, 46] `[flourish.studio](https://flourish.studio/blog/accessibility-improvements/)`.
*   **Flashing and Seizures:** WCAG Success Criterion 2.3.1 strictly prohibits content from flashing more than three times per second [cite: 7] `[educationalvoice.co.uk](https://educationalvoice.co.uk/easily-interactive-animations/)`.
*   **Screen Readers and Keyboard Navigation:** Scrollytelling content frequently traps keyboard users. To pass accessibility floors, all interactive chart elements (legends, tooltips) must be focusable via the `Tab` key, and content cannot be hidden in `<canvas>` elements without visually hidden, screen-reader-accessible HTML DOM equivalents acting as shadows [cite: 7, 45] `[flourish.studio](https://flourish.studio/blog/accessibility-improvements/)`.

### 6. Documented Failure Modes

A programmatic generator must explicitly guard against several well-documented failure states that instantly mark a page as untrustworthy or poorly engineered:

*   **Mobile Performance Collapse:** Attempting to render unoptimized WebGL or heavy DOM manipulation on mobile processors results in **layout thrashing** (a performance bottleneck where the browser is forced to repeatedly recalculate the positions and geometries of elements before the screen paints), battery drain, and broken layouts. The exact threshold of this collapse is rigidly defined on Apple devices: iOS Safari operates on a strictly enforced 300–500 MB limit for the WebGL heap [cite: 37, 38]. If a 3D scene attempts to allocate memory beyond this hard ceiling, the browser silently crashes to a blank page or performs a forced reload without an error message, completely breaking the experience [cite: 37, 39]. A page must be "gated" (serving a simplified narrative structure to mobile devices) if 60fps cannot be maintained or if the strict 256 MB safe memory budget is exceeded.
*   **Scrolljacking:** Hijacking native scroll wheel physics to force a specific scrolling speed. This is universally despised by users as a loss of control and is a primary accessibility violation. Practitioners instead use "scroll-synced" animations that stop instantly when the user stops scrolling [cite: 23, 43] `[scrollytelling.ai](https://scrollytelling.ai/what-is-scrollytelling/)`.
*   **Visual Homogeneity:** Out-of-the-box templates (e.g., unmodified Shorthand or raw D3 defaults) strip a publisher of their unique authorial voice. Studies evaluating LLM-driven data journalism generation (such as the Data2Story agent) show that while machines excel at evidence-grounding, they fail to match the bespoke, creative aesthetic of human teams (like *The Pudding*), resulting in a recognizable "template sameness" [cite: 12, 47] `[arxiv.org](https://arxiv.org/html/2606.11176v1)`.
*   **Claims Outrunning Sources & Misleading Charts:** Truncated Y-axes, distorted aspect ratios, and semantic ambiguity (where textual claims exaggerate the statistical reality of the chart) are the fastest ways to destroy a report's credibility. Generative systems must ensure strict parity between the visual representation and the analytical text [cite: 48, 49] `[arxiv.org](https://arxiv.org/html/2607.10523v1)`.

### 7. Agentic Operationalization: JSON Schema and Architecture

To instruct an LLM (such as a Claude Code skill) to enforce these rules dynamically without hallucinating layout complexities, the process must rely on a decoupled data model. Systems like Fidyll, DataWeaver, and The Story Scrolls demonstrate that LLMs should not generate raw DOM structures directly [cite: 50, 51, 52]. 

Instead, the agent must output a strictly typed JSON schema representing an Abstract Syntax Tree (AST) of the narrative. In this pattern:
1.  **Schema Enforcement:** The agent outputs a JSON array where each node represents a single "scroll state" or scene. 
2.  **State Decoupling:** Each JSON object isolates the `text_content` from the `visualization_parameters` (e.g., specifying `xAttr`, `yAttr`, or data filters required for that specific frame) [cite: 51].
3.  **Render Abstraction:** A static front-end framework (like Astro, Svelte, or React) ingests this JSON. It uses Intersection Observers [cite: 42] and CSS `animation-timeline: scroll()` to smoothly interpolate the visual parameters between states as the user scrolls, mathematically guaranteeing the "one idea per scroll state" rule while insulating the AI from breaking the CSS logic [cite: 51, 52, 53].

## What is the current state, and what is the strongest supporting evidence for it?

The current state of scrollytelling web reports is marked by a pivot away from raw visual spectacle toward performance-centric, accessible, and evidence-grounded narratives. The strongest supporting evidence for this shift comes directly from the evolution of web standards and search engine algorithms. 

Google's enforcement of Core Web Vitals—specifically the integration of Interaction to Next Paint (INP) as a primary ranking factor—has forced newsrooms to abandon heavy JavaScript scroll manipulation [cite: 8, 29] `[blog.gitbutler.com](https://blog.gitbutler.com/the-great-css-expansion)`. The state-of-the-art now relies on CSS scroll-driven animations, pushing layout calculations off the main thread and onto the browser's GPU compositor. `<INFERENCE from="[cite: 8, 36, 54]">`For an automated agent generating HTML, this dictates that the default rendering engine must compile scroll triggers into raw CSS `animation-timeline` properties, reserving JS libraries like GSAP strictly for complex canvas manipulations or intricate SVG morphing that CSS cannot handle.`</INFERENCE>`

## What are the contrasting viewpoints or competing evidence?

The primary tension in the literature revolves around the cognitive efficacy of scrolling itself.

As noted previously, educational psychology research from 2009 (Sanchez) argues that scrolling is inherently detrimental to deep comprehension because it removes the spatial memory cues afforded by static pagination [cite: 4, 5] `[pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/20196297/)`. Conversely, recent HCI research (Tjärnhage, 2023) argues that in the context of data journalism, the continuous narrative momentum provided by scrollytelling actually *increases* recall and holds user attention longer than static text [cite: 3] `[researchgate.net](https://www.researchgate.net/publication/374109425_The_Impact_of_Scrollytelling_on_the_Reading_Experience_of_Long-Form_Journalism)`. 

A secondary operational conflict exists in the "Build vs. Buy" paradigm. While off-the-shelf tools (Shorthand, Webflow) democratize scrollytelling, data visualization purists argue that these generic UI components fail to capture the nuanced, bespoke nature of true data journalism (as practiced by *The New York Times* or *The Pudding*), which requires raw D3.js, Svelte, and custom DOM engineering to prevent visual homogeneity [cite: 12, 47, 55] `[arxiv.org](https://arxiv.org/html/2606.11176v1)`.

## What changed recently, and what is the trajectory?

Three major technical and cultural shifts define the immediate trajectory of this format:

1.  **The Native CSS Animation Revolution:** The stabilization of the CSS `animation-timeline: scroll()` and `view()` APIs in modern browsers (Chrome, Edge, Opera) represents a tectonic shift. It allows developers to achieve 60fps parallax and progressive reveals with zero JavaScript overhead, fundamentally altering performance budgets [cite: 8, 36] `[cloudways.com](https://www.cloudways.com/blog/what-is-parallax-scrolling/)`.
2.  **Generative AI as an Analytical Co-Pilot:** Experimental systems like Data2Story demonstrate that agents can successfully parse raw datasets, link claims directly to data provenance, and generate auditable HTML reports. However, the trajectory indicates AI will serve as an orchestration and coding layer, while human art directors must still govern the final "authorial voice" to prevent the output from feeling coldly robotic [cite: 12, 51] `[arxiv.org](https://arxiv.org/html/2606.11176v1)`.
3.  **Strict Accessibility Enforcement:** Driven by expanding WCAG 2.2 regulations, implementing `prefers-reduced-motion` fallbacks is no longer an optional "progressive enhancement" but a baseline compliance requirement [cite: 6, 7, 43] `[educationalvoice.co.uk](https://educationalvoice.co.uk/easily-interactive-animations/)`.

## Knowledge Gaps

*   **Granular Citation UX Analytics:** `<MISSING_DATA>`[Quantitative CTR data on inline footnotes, Unavailable, Log-level analytics from a major graphics desk (e.g., NYT or Reuters) comparing engagement rates of hover-states vs click-to-expand inline citations.]`</MISSING_DATA>`
*   **AI Template Hallucination Rates:** `<INSUFFICIENT_EVIDENCE>`[Precise failure rates of autonomous agents generating misleading charts (e.g., truncating axes without prompting), because current benchmarks focus on text grounding rather than visual-statistical integrity.]`</INSUFFICIENT_EVIDENCE>`

## Recommended Next Steps

1.  **Develop a CSS/JS Fallback Compilation Matrix:** Investigate and document the exact build pipeline required for the Claude agent to automatically compile `animation-timeline: scroll()` rules for modern browsers, while injecting a lightweight Intersection Observer polyfill for legacy iOS/Safari clients.
2.  **Define a WebGL "Cost Threshold" Heuristic:** Create a definitive programmatic test the agent can run against the corpus data to definitively answer: *Does this specific dataset require 3D spatial representation, or can it be mapped to a 2D SVG?*
3.  **Prototype the "FiveThirtyEight" Citation Component:** Task the agent with building a reusable, accessible HTML/CSS Web Component (`<inline-citation>`) that houses provenance metadata without trapping keyboard focus or obscuring primary text on mobile viewports.

## Architecture & Infrastructure Comparison Table

*(Note: As this analysis evaluates the infrastructure for building programmatic, scroll-driven web reports rather than comparing LLM model weights, the parameters below reflect the technical reality of the animation and rendering frameworks an agent must deploy).*

| Infrastructure / Library | Primary Execution Context | Size / Footprint (Min+Gzip) | INP / Latency Impact | Optimal Use Case | Cost / License |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CSS `animation-timeline`** | GPU Compositor Thread | 0 KB (Native Browser API) | Zero (Non-blocking) | Basic parallax, progress bars, simple fades | Free / Open Web Standard |
| **GSAP ScrollTrigger** | JavaScript Main Thread | ~44 KB (Core + Plugin) | Medium/High (can cause jank if animating layout) | Complex timeline scrubbing, SVG morphing | Free for commercial (as of 2026) |
| **Motion.dev (fka Framer)** | JavaScript Main Thread | ~8 KB (Modular) | Low/Medium | React-based ecosystems, physics springs | Free / MIT |
| **Three.js / WebGL** | GPU via WebGL API | ~150 KB - 600 KB+ | Extreme (High memory & battery drain) | Spatial storytelling, 3D systemic behavior | Free / MIT |
| **Intersection Observer** | Native Browser API | 0 KB | Very Low | One-time "reveal on scroll" triggers | Free / Open Web Standard |

**Sources:**
1. [stanford.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEHTDFrhjRml3t1V_EbINRFQ3cVUMIY_i3qIoNrs_dZ9Xezwj6fzifl-NeGz_BbZPDrdJTz-Q7fHLlRFP314xevKn3FA3bgzdLwsURq4Egs55jABvc1q0ULWWZdH4Lw)
2. [computer.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG-UrY83rzeovMK20Ce6Qa3ENiYP2c9obc2HSPIHhp50n-tHgU25jIeGTWUbtD7yUL5xIosrXewmTkY1FK3M5-XRGZnigkdqEnnYQIGCCj1UywsBopdsGJqTUjjmWTlOarq9tJ6PTTMHXgQQwWeLQmwFvT55LI0G2RsXVeMbClNHw==)
3. [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEdiXnILPYoZ-85x6BEH79-7OuXNEYhYtLjDH5vzXH2XLS1ugar4Jm0ybSqu7DAJXOT1hSMXgotJJ1F1KPieAwTwldO-o3nHAvWagdZKmX2pmzFoswybQ5IMMcUu0Ujsm7iW__jTsKCbbvSGtVBCaKMFRkVQq6eMPj2h0yViB8-jtE-arPkMGNUwl8IUq5LcvWCd02b3vWV5R0wAPKrzk8q6OoWwrMsBkUwTPN3xbTCTHjLwyEzWKd8)
4. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF8Eb6-q2lmtfIntFo_Hwm4yb9INOoDa4age-t8BcRRrRdLldmhCORT87Bwz_uv16XAbhlU3_nDf4A6Xk5X-H-mDIWqLoU_Zwu4FUPV5XIxW8f8-EjvZiY7wfS9SgRetQ==)
5. [twosidesna.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHS-rzskNvfs6nIe1rpxpq9my9E5o7xaJ2G8NWWhVj9eC1gFmUlHJOkt76a-blstCn6OYqH0yaBs87P4E0Z9uLcqV0fv6FCn1ZDVsIgsQwKq21XPH9yMx1tvvtXg5Vj5fgROOP0qWFmIOJDp6RYdFi2_doJHanP0ll510vjfG1O0DXVhOAlVUhBdtsWeJh1jvaTKz8hoeUEedGI-WRBVDJtTfDJisyi_WdVmSfNEQwdyvAj_oE4YBP0UcweF6DqXYVyngN3NLBEv3T3BvEIpCgDAWo=)
6. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG8cgDLGyFeVNdmWTnpotJYO07g8Op5HVHMpkbWIlytjIsHZGyntjCu4Re8vBlyFwY5dKXkZZjsttoxJwXEhJ9zEONm7NptK8a3Y3clzp5gBD8_rKdiIh-GJdbVi5PZcvZ2Poqow6ZkKdIDU8wLB-y6uNmqhbAG09nzF2HR)
7. [educationalvoice.co.uk](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFHshKmQmGwjZtjxY0Djcg570NQmlSFM9HGUh0uJuzM5w3oATfrScdDXUeCU--0nEDmrC6TLV0vZg1xXmjBr-0laiNk1UXYLd_414ThC_zR_1WmGcSf7MBI7Yafhhkbl-NMk_fPI4tZJqTJ-7kxNlWuzOBm)
8. [gitbutler.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHbgVVg-pqQZ8wbagflydd8Tnt82H5n43D1SZA9cKECvvd3mX54ShstT3MvPdN6fdFnbOxbDibjg7PObZPz9OEqu0O6aehuBIF354VypInkEpczUQrLX_McLVeVD--kDMG0ufsIQ0dK4w==)
9. [clodron.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE_q4q5Ixfh2fyc4gA0cAxDSDwMT0GRwejSwlklKEhc7tUgb2TiWaqkDtkufb5SV8TWp_bAm5XoztmjU1FFN3YD-Bhvl7pWOb9ph4_SawSAcJ4Tih-d5xzC-JP6XtyFZDmGRGMw2XAJsQ==)
10. [innoraft.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHtvYmxH4YfZg0DN_PHxuqFbXr1K9p13KR_qt6bdmLVhEZJFhXoi3QPmWmZnoDEw2RfQQaztg81IYcs5wMBptWR0LO39X9WEhD67Cc8IHW-oP6QbwjYP7EjUHP31P9osmvLlYEgag4ez-ZCpPLel3E1mLWAEick)
11. [topfunky.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHELWUVAhh-6QN0wok6ydU5cQ6eJGz7rbkkj8GzMNeuStkO9Xd-vI3-2kEFcuLkeaGT62v_Ayha-UXVeQ38CfHS-2xWX1fNTCcYhsceco6Ob5AdxuOdgk57M8jM64Y=)
12. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFH6GpYvcPne2YzbsMK-CqNSrBrgFZm0Pu351gXGEIN_AUCBLAO88M86qnrP3W3YKJAQfV4ZMazRlhygAQAQvbN076aHWbXXLW8heyY2uTTIL-xNqsk_E-pwA==)
13. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEo1v3mftWZGidLtsPqJHKw-AxrTJs_ROqRQIDSCasbvlsgJh6H0bkdheGwWlUcAQ0SuV-_gGi6pp6Kr4E-7qbp8w1mzEcFEABq1KwXAD1s0AvCiqLAvmmE8YA--2seWiRo5jLHDO7Ws-xpcaoNkbnZ8yaLWJ2OmCTLhpD1GnfHMClwpQMqBfRQjCUYk6EyYHhxZD-di_Y9z8JqOOQ=)
14. [ucsd.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTXafvgExTl-fW8Eb1mLdONt0Yd8rasl_B96JJ3sW4yDmQpiwLdW3BUdHz5C5Tl1BIEusJTC5TQ9J66AaCINOOppMKB3PHxS945TtWcCfA9wj3PJ1AQFvjYeIergP4DdyGeB6PoPdr2Ug=)
15. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFifvPfTRhPlSQ1gajSId58IZfyUhB7WaNHB2sH1BeCfXlbzm437zJUwo7ZTCcikxgOuFjY3rBMIiXRLAuiwNZ4SHamyxG9ZP0JFH_EUWHLxYiPcMsTAhtbYEbbJi0fVtwEJdb87V_Umsrt0YyG6o1GXrMkdhIpJ3LI7jIwysBLVTFEdBcgXpL1eoEKH_7wftSn_kKt61H0jco=)
16. [infogram.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHHWn-zr7OztCN-DT-Rdklk14KJI4ODLx_WE6QwZdRi9xj6K5WEyZp_3ZbEV6YdLyGbVcWKTKstScFIFJLfz83by3oNqMBc9PquQ4OUOOiyUB4Bxj3OKwqDMCFPHwOyKeLHXThmMifa1ZZRwf2Qo3dJ3vWZtuMM88jPv7E6mU-udAxLQvMMBAOUGQ==)
17. [storyflow.so](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEnZ8zqngk_z9LljAngpZfiIquhQ84mbIjFoMy4rbqa6nTG1Aty2rlspjYgSfDU1u_Uyu9_NYAfwzHVVHtTplYUDsJ3YuUI4U84_lsgO5w4JeF12i_ZtcIUCjwsEKr9QgzHa6pxidVmX0IzeXLcHEI2Lb6ks11oleF9aA==)
18. [theaggie.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEOM2ms92vJUzTsR4P5PooExr95qdFoJutAn2RHSCz8o_6O5H_eauKC0NbdVDdszPblpTtcSvbIVjPia19MzksS7TOzmxBDs0HqoSBqHLpi_R8c9NaWLZBGYbNo9OIkLLasGcN8_99Ackv9ptBNVg5_dsAsg8B5ekLSMGb-hCmtVs9Reedegp6jh30BWD_CtF3SDddHe4udrQ==)
19. [cogitatiopress.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTDwlOhfu1u03BLcJIREVjWY-Dimm8YqtmBJ-WZSqZ_H64heTxUFwaCfgT_Qv59lj3_wEcvRQEUbgrD6bBAuXq7ucFsYbKtsZHStA-COTXYFQP73e_9hSGWcEaKCJFejozTDwJQ6n4Y3Cbn0z20fh8PYS7u_78e1qPnR8Zm5IKpjid-iKp)
20. [tandfonline.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFv3aSp6_Zx8tyFlZhJQmufxori-90r-1UPuMtIW7CN3ZD-ni2S-IFiAhKAAK_t5x6DP5dCUTHGlrsqMaZKVjtvwUIOxftLpIpErxakqFaBnTeS8TpuFktceAEA_Svh6NyUNvBmjhU1bm94JET0l8rJ9BGi58zJw2Y=)
21. [oapen.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGu0Nj1jtLet3BI8piV3rN60DLWg0zwb4sQv9ikLL8vjmiALhZkvy8CypEur-SOf3ORVTm9gbrO5RloW6ZUq7vVzqx0jyYCd_jorRE5QHFU0vNcI4BPaWCF_Zp1bXTchgwCQ-w07zy6nEz4ygs13t3EZSsJWWSaMipaGeW0IudxU8YeB1mv)
22. [datajournalism.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEblU1BgvvIQkfYM8kz_wjeNZvRR1yxfKgV-i9yG9xR2XF785d3shyDxpn2-JxfDuzbfUXim9-Sm4X0yW-sGTvylQaG2EsSccfKDegislJiBICsfgRvRMu696tGREL9Cj4UEvgWGJ70KLGqRaw5D5hZ7NOJk5V3qyI3hYUuaslUwDY1m62CBtgUO4LDVbzLTkT4rB_zX6Hpyq6a9KjXjcR43mZ_zYjMfTwibJpUATi_aBghdvLc)
23. [scrollytelling.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHKZWvHfJ5VGqiYPJ3P-gB4G-Lw_E3ob-VArKmEv-tvTUtXNwoDfiwSlgahHdbjSsWGIQx48vtHVPq_hJoTr9rI1D3gqszYCis__KgwTdZpmVzGRJolJs6wpefuXTtW_k9V9jUhQBCm)
24. [easyappsecom.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEG1Y2405SF4_GSq2yB0RfChMEqZ5ZEhEPFGDfSya-u1rISrnP9A4E5vo0gDRM90yy3HxvxeMYwLblEqu6KfatAoLWxUPyNOu3e72NPW7OQ6CnkakB3zbscvRvGipyDR1v2GfDTwm6E5QF6sp0X_FDSB4ddN2VkFZB7SA==)
25. [legitclickmedia.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFPUMXurcZmSSHnG2pAD2BKPx6Z2qWStUBH4dUXKNrdtldopKtRgtCrqByQdxNCtT6QJ-CDttS5iq9JabI3JTB5ejYBSdYjbc0PUarDKnsIEjMrNjzqR9CwIUcMbZfli-EDpCiWTzark0DlN90UHAmliBs2If3WcL5DNpxI3RaHvmusVR90)
26. [scaleflex.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGKldA_Mu9RnkIJSHB9sFHQ33yZ9ES5MCm_fhRTxSLiXL87uxj6Fl_94Qox3hcfjQGLLIpUVBe-56WZcjmRnoTFYpSwMTAyZxNRpmgMvVI4rDoNsMWZ3xPd9aCTuNifN_iYzpcmH8z7FPcC5Hoq261k3A==)
27. [websitespeedy.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFcaEAjp_oGBI_NvFoI7RLcwmHVNlxmGIKSIiP_OEiy1K73Eitd2xSYs44r0dFsx6oDw0C3WaLE0s6MqZWiXaKLFRb98bjPcaPfPNPNUyKF_UXdY9NcMxk09D3wqv_avN-FPu8CmsibNYwhgQhwg0sHG8vG_DYqB9vtNWlRDwjUfBX_F_q63hc5xW0QpnGk1477OsTc_g0urSPgxw==)
28. [corewebvitals.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFq5zP-S4qljrK_zyC0Ba14inDaNuzW6rl3y4BkcOa6qN1SHTDAnQtwZEcRlMwFIU8yEpnZahUOl1a19g29kMsESvOKJWP02gSBI9WCxz7yuHRrEqS0twlkcoqNVjnb_wURGVCyIS16aHKSkUrXge5oQnmhnRyynRWxQugv)
29. [ruskinconsulting.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEA6dASlcGWMZt7x8pWGoA6EOXoIO7l3Jwn0WOd2UxBrXD8u6UrDNLM1ZHXxywkf9Ip7LVEH3XB2yv-_y5QBbLpr4F68b15hE-4eSdaXzT1x2i56itP3_ONapeYZ-d1_Vc0FcEfCFYqI7R17jLVFtIoBaVXMNqdyqjtbUfRqAQ=)
30. [pubperf.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFFdB7FmzOfRrhfDYTpa4uumtD3pLQIBlXcIGRu_LAIPTd38dx7ahX2QZatUTzoTnXeYMgGE279PQNSc2wPyPwL19PU8upPUYkNyT_lgkdhcv4nTVF9SaDoTcrw4U2K6cb4)
31. [conductor.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHtR-XQZOp8-AKg8MQ7kQCXW75gjoiCcKIS1QU0TDG6exRH4s1eubkv1NACyyYeUs2WmlRlLYxYqis69VCmIwWxEFiJwYd9Ah3oKvHf-YbWnBnoExFPA21jg2YUC0rdUfpx-ZZLd3iSow==)
32. [web.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHMFWOdBPU47Shc5kFP5j9q6F_rAbQ7zbWNE4CEVq3SVZ-ndxEjtOGisNOeVTGyJ3mLRPRUnEAA_nDCpGoEQqoMA2_4qJpfuiFQ140DNNlLUPYX)
33. [perfmatters.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGVrqY4RjHK6cpJ6DCNePLoVzO7mJigVWv5-H9kNLeoInPY_Wt07qeU6XnJpX35LcCQDG8sA6gadTyXEgww-qgvqnZ1mK_S4Ig4aidm6XsBsQwh6JcjdzG8N8MAqA-FA2KX3BeGU0ACjvm4KAA=)
34. [coralogix.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHFbD2m-ybQWuDUalYfiKw6npE0WcBVz8c7W4dDvjInjTe250CzzZ7-Iee0UNJJOjtChhe7h8_rmxmJ2qCaQmYcGE1b8zHr9lzD382Eb7kOJ8wAgyvVNUzNEB-RfWsX6yG5yuUUyoV_R6uWbtaoezwonyRBZzvh892VcHgSYwrcInUkVmFFzCwk8ZS_yNoUqRMPvgAsZI0=)
35. [web.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5Ol7slHpxXraYhHLnNQhWf4ZbSCNfhKo9nqtnioou25WcN1tfPpo93l5ICpCRMzcYu0fKC-XEdMVdPihRxcX55ldJs3G67RT-3lj82D7Udbr85ZospEsRi4zS)
36. [cloudways.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHW9LYdzG7uiscepOb7rfDVaS4WQBDPUoj-DLS77fd_WmPyyp6j8oDXJcq625n7qxb5igcgQaswRW9xB1Vxv8T8mjrZUuiu3pffVPefTTFP_NAtQpJwJ_qssSHC8HNOIyb3PFsdCFIMOgqYEZFKF3rh)
37. [bugnet.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEFHgADDDkuUbfONepEz2aMS4_szVfALNuJ6cwu0_aH_6VKCd9HHTP5ObDknLRMUmbJ86PmMKOGtsZhHiYsuU1QavcKQLUMY78GhYEp9Z5GqnvtmjP2w9jDKpKDxXlcMyZBoCAZTUyvjxvrU2TYJhuT5ivaSzBYrXSu--sOZCEvOw==)
38. [unity.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEHZkRxLFhKX6VPTg-q1NdWHEwSDcYFceF0StO9hSHsSPFWL8zVUaZeqGo5n4HCNZxxcFkSSYol7FgpcTvoGrR4_wH60ymYWeNir8pY_RskRcdG1cA5nn6fiam97hzPTvpYFHayt1ef0KPa30gz26Wszbwy4bT2phIAdI4mjIJb7dPRoRaxR8iNd6RjHQ99SUP9oz30CnsBVWJ8o4sveEKkA7An6oMlGktxF_AMSWtc3xOIxjb_)
39. [unity.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFSY_8U6c8PguoVDybfyumvVSUexwnuN2JXs8Z48O_WA2PndrxKcQldAId0r-LqjgJGcqdLGVKHYKBTn6Csu2Jh8AILpX2y-eCeaZxyF7xbIQIYxi2lRbJhYzguKSnzfQGN6jVTQaiojvFJVy9dRKICT6bxnnYDk6pf4x1vFsiphXWzPzdoG5QGKb4=)
40. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFXoAYJ1_fvT-z6UL2J6Bz71dNjIsvQUUsbXwtsD3ahxV0aOjYnitsGRKL9-Nr0RvNYUSD8Tz7N2jJA-e8YFaaQPJnA4aQgOJWkME-aEvFEkXa5PaAL-0K9ABAUK5iQDeAKUjln5M9GWGpb_VSo5_cLxI0R0MMJeWRr1u5fxDC4_UsXJNbPRn5_B3CPjMPmDuox3U0Le1eWyfmc57PQ2yNnFtbU)
41. [designrush.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE68vlwYD-4h-WUnvkj6hm7tiSxw3suLd8SDrSi6oVDxRsjkh_b3ENBKfF00Qh8UTG2Aul4G4BP85XVMnKdNOcmK5cWOqBAcIwMxQovpF9LiWuDTVyFufWdeUzKTf_XB2lYh6NaixZ9Y9QtMNA_ojanSus0LJyMN7_-iZqQhk8_0QPXRfVML5IonCbF)
42. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFpteCew7oCqitKpmvZidjcIhdlwWspq5yEwhO7qCVEkleFIVKMTdGcHwTTRbIh0ZZ_wORzCCITdL-EVyu8wCoiMSGINbCbsTJJAxOx7ce7wtRA97JcSbmfdycPVeYtAbcY6sQkxek=)
43. [alistapart.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFFFC4wq5bsA2X7WFiHCTV-z77ppIPDAE0sjND71Kjp9-2N001smyvWhs0aGV8veope4qKW_RoqCUvyOrxnVgzQpbOXJIq_mIkoLe_Ree1Czy2RAbyGi7DXZh4OB5ZbeA98kE_qxRRlL-HPgEGZ22VJnwBxrhw=)
44. [vezert.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTMisgCfpIeDKq2misfOyeTV0w0ssRjqoyqSMdI4gB4HyAkJHyAVo-QfqA6ATolMO1fAHlWxMTvfOBD9nd6ug2S6SGvaEawOVwdYSWffc2es9eMBsQGWRmJUlchOTW_Q1t7ztdVuis5D7gpp67LTDNeZ0FXkM=)
45. [flourish.studio](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHnAnRkWwBgvWJaYyW-naR2-nD4Tlzp6z-anTwVv4ZQE3ngL2Ta3_QH5pw1BPASAMFgZ1OgKFSivvxs8BTKeQdWpcOPVD9vAzyNbXPJUpi7mSzkPlhXYi8-io1jQINEcmHesc3bhKkVTaqf7f0Y0g==)
46. [zignuts.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEcwqf0ikmfpuyG9ozXa7xm262IficfUnB5UiR8IcHvXXnrxlivg10WPaIWpfwi18HzC1uUHbS656GB12p89zs5YbVEehvquSrngPGUtq4fxV6F5N-DhzQKUB6OMUtMU5pp1o1PlH_W69VzLw==)
47. [shorthand.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGQZozmwhG7n3HOQ4kPCFltHqADsDzuWQNU-KZUPOyWgy1-W62ctnBcoD5a-hKrebcphm8afVRjl2Qs-Op4aKM4r_qoCi7HYfAwE-kkY1-Ih2z4Q2n9gu-_FkyyuwS-bDBbdrB5H2gVow==)
48. [gatech.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF1_E0DBwN2NRDRj_R3ckQqyKcVZMoCGxZECU3DOtAEkfxUeuVNfBKCUZsSXf5ey8bLxu18pKY8KMGrVMjzwFZyqFtAFmscfcyDJO3zMTPlDXsvQcp-7ZWv0FyJ3c6yowuYkORn1lhSWbR0o93JFw==)
49. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFoHkTtFW2KKshbDzU9rh1wnZWKKgogIYPcL0JtjV5_StJqVL-M3IlwBarE8VlWqXPhOzYe2jPECT5xSbZVzR6aXDmrkmxjJkAlohZBLOfVsRZghZicUYPbCQ==)
50. [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEP0Ee1FU2wP39_GBjmCx-9rrGsH9hkaUWpTjTkm-vi4Yi5bmfP0aSlj7zcYwwsQAXX-WVw2tXnn1cb_T0eJ0XUgJJrgxiIX3Wg2vVe4-sgsSdQFHBrmtCkX46Il6MzVSy4)
51. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGHiHVuZOGqSSRGazXCQ_gFJ_gR-K-uiGZ862BokJKEQ06FbOXBzmouRpghvauuMZjZDbCKRooglJRhL3i3PpDU2Zjbo-bWcp4BppaLL-0QRVXgqQDuUCem1g==)
52. [washington.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFTmJ99vaTz7nLN1RiX5G5apzmiiHd6Twuz9ow3FKgDvp2Ah4-5Pm3_93QAfKLH1_W-xA8YM_Ko6m0bzwy2FsjFZT8S4PuHKBU2_X7yC_ZrzRILQw2Q9groThIyDZov3ZL2lg8n_bAPYCy1ZwHndyk=)
53. [cuny.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHngY925WzbbKBdEgxRTVdXOvN46MJkxaAsnr0_9KPUaBOmSrX_-q74GKbr-BBzxtjoZWc4XjJQCfL9gXxszf5bNQenMHcAR4Z-SHQCteJ2AEGJq4lPpzUY_hrtYKoY_PDbEsgmW-c-nW8gO05_qUWa6kCJmIS6hMAdSiA0o_s5T_mR4H_b)
54. [cssauthor.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFcc4hnrEqgQiuJMn2bHKAaLwnCvLxDWVXUpgpt7SrOtFd-F2AP0BG6IlCU34GFPlHmGRKOgLAk-z37mtn6SYnRVQF3EO-gVUTV8lAnbtpwgNZ5LSWKm1f7-NCA0nwH6AdK5Z6149ppdt3iDHZcjyX_HiPrTGfQS2Mz4CeB_wK9YAGY6OeOZA==)
55. [ons.gov.uk](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGiB3bDW_f6lCiUHXGXW4ytkwJDC5MB0OhGhkwjGMBQvrSmZfO_Oi0XNmbmZzqPjUI-QRlKHPXGFwr7fBMqXGcNDS5D3Xo4mxOauhHTJ_MvxZ3Ws8C_pYdUU_K1fjrfsdU3c1Pc3uUcecOOfjwGUkxtfClaA9RsiOx6I9GxOWETB9lbT7vP)
