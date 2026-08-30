---
title: "Constraints for Automated Data Visualization and Diagram Generation"
run_id: dr_b1ce9203a3ab98d0
question: "What does the empirical evidence say about producing high-quality static and interactive data visualisations and technical diagrams as code (SVG/HTML) — specifically: (1) graphical perception and encoding-accuracy findings that should govern chart-form selection and mark design; (2) colour design for categorical, sequential and diverging scales including colour-vision-deficiency separation thresholds, perceptual colour spaces (CIELAB/OKLab/CAM16-UCS) and measurable pass/fail criteria; (3) accessibility requirements for charts and diagrams (WCAG 2.2 non-text contrast, redundant encoding, screen-reader/ARIA patterns for SVG, alt-text and data-table equivalents); (4) automated quality checks and verifiable linting for generated visualisations (label collision, occlusion, geometry, axis truncation, deceptive encodings); (5) documented failure modes of LLM-generated charts and diagrams and what measurably reduces them; and (6) how visualisation quality is evaluated (task-based comprehension studies, published benchmarks, automated metrics, rubric and judge protocols)."
provider: gemini
model: deep-research-max-preview-04-2026
tier: max
archetype: technical
sources: 72
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 7.00
completed: 2026-08-30T06:26:02.100Z
---
# Empirical Evidence on Automated Diagram and Data Visualization Generation

*Disclaimer: This report synthesizes technical benchmarks, automated linting protocols, and accessibility standards for informational purposes. Implementing these findings into production software architecture should involve rigorous internal testing and compliance validation according to your specific enterprise and regulatory requirements.*

## Executive Summary
*   **(High Confidence) Visual Encoding Accuracy**: Position along an aligned scale yields the lowest perceptual error (<2%), dictating that quantitative chart generation must prioritize positional encodings over area (5–10% error) or color saturation (>15% error).
*   **(High Confidence) Technical Diagram Layout**: Heuristic-based Sugiyama frameworks (e.g., Dagre, ELK) are mandatory for deterministic layout generation; relying on LLMs for spatial coordinates fails. ELK improves dense graph routing (minimizing edge-crossing) at the cost of a 100–300 ms latency penalty.
*   **(High Confidence) Color and CVD Validation**: Color Vision Deficiency (CVD) compliance must be programmatically verified using standard transformation matrices (e.g., Viénot 1999 or Brettel 1997) within CAM16-UCS or CIELAB spaces, where a $\Delta E > 5$ guarantees distinct categorical separation.
*   **(High Confidence) Accessibility Mandates**: Web Content Accessibility Guidelines (WCAG) 2.2 strictures require a 3:1 non-text contrast ratio for structural elements, supplemented by the W3C Web Accessibility Initiative - Accessible Rich Internet Applications (WAI-ARIA) Graphics Module roles for SVG Document Object Model (DOM) trees.
*   **(Medium Confidence) Deterministic Linting**: Formalizing visualization heuristics via Answer Set Programming (ASP) (e.g., Draco) or custom DOM-based linters (e.g., VizLinter) can autonomously trap label collision, axis truncation, and deceptive occlusions prior to final render.
*   **(High Confidence) LLM Failure Modes & Architecture**: End-to-end LLM visualization generation suffers from "hidden hallucinations," where visually flawless code execution masks underlying data extraction and mathematical reasoning failures. A multi-stage Extract-Reason-Visualize (ERV) pipeline targeting a strict JSON schema (e.g., Vega-Lite v6) is required to isolate and verify these steps.

The transition from arbitrary diagram generation to verifiable, high-fidelity data visualization requires replacing soft design guidelines with hard geometric, colorimetric, and semantic constraints. By evaluating graphical perception literature, accessibility legislation, color science mathematics, and Large Language Model (LLM) benchmarking, this analysis provides the numeric thresholds and failure-mode mitigations required to build resilient visual-generation architectures.

## Graphical Perception and Encoding-Accuracy Findings

The foundation of automated chart-form selection lies in matching data types to visual channels based on human perceptual accuracy. Rather than relying on aesthetic preference, a visualization agent must algorithmically select encodings that minimize decoding error.

### The Hierarchy of Visual Variables
The empirical baseline for graphical perception was established by Cleveland and McGill's controlled experiments on human decoding accuracy, which ranked visual channels by the magnitude of error they induce in quantitative judgments [cite: 1, 2][cstopics.com](https://cstopics.com/encyclopedia/hci/information-visualization/visualization-principles/perceptual-accuracy-of-visual-encodings). Mackinlay later formalized this into the Automated Presentation Tool (APT) algorithm, establishing strict rules for "expressiveness" (representing only the data) and "effectiveness" (utilizing the most accurate channel available) [cite: 3, 4][scribd.com](https://www.scribd.com/document/918339731/ak-DV-CAE1).

<INFERENCE from="[cite: 1, 4, 5, 6]">An algorithmic rule engine for chart generation must iterate through the following hierarchy when assigning quantitative data to visual marks, defaulting to the highest available channel: 1) Position on a common scale; 2) Position on unaligned scales; 3) Length; 4) Angle/Slope; 5) Area; 6) Volume; 7) Color Saturation; 8) Color Hue.</INFERENCE>

When evaluating error rates, position judgments exhibit less than 2% error, whereas area judgments demonstrate 5–10% error, and color saturation exceeds 15% error for the same ratio comparison [cite: 1][cstopics.com](https://cstopics.com/encyclopedia/hci/information-visualization/visualization-principles/perceptual-accuracy-of-visual-encodings). The mathematical driver behind area misperception is modeled by Stevens' Power Law. Human perception of areas and volumes is conservative; we underestimate large values relative to small ones [cite: 7][stat.auckland.ac.nz](https://www.stat.auckland.ac.nz/~ihaka/courses/120/Lectures/lecture11.pdf). For area encodings (e.g., Bubble Charts), the exponent $\beta$ is approximately 0.7. Consequently, when comparing an area of size 2 to an area of size 1, the perceived ratio is $2^{0.7} / 1^{0.7} = 1.62$, rather than the true mathematical ratio of 2.0 [cite: 7][stat.auckland.ac.nz](https://www.stat.auckland.ac.nz/~ihaka/courses/120/Lectures/lecture11.pdf).

### Encoding Thresholds for the Agent Linter
To translate these findings into hard rules for an LLM agent, chart-selection scripts should enforce the following pass/fail criteria:
*   **Expressiveness Violation**: Bar charts (length encodings) must anchor at zero. An LLM generating a bar chart with a truncated Y-axis violates length perception and must trigger a linter failure [cite: 4][scribd.com](https://www.scribd.com/document/918339731/ak-DV-CAE1).
*   **Resolution Constraints**: For length encoding, a 10% difference requires physical space exceeding the Just-Noticeable Difference (JND)—the minimum threshold at which a change in a stimulus can be perceived by the human eye. For area, the same data ratio requires a 32% diameter change [cite: 1][cstopics.com](https://cstopics.com/encyclopedia/hci/information-visualization/visualization-principles/perceptual-accuracy-of-visual-encodings).

<CONFLICTING_EVIDENCE>While the Cleveland-McGill 10-tier hierarchy remains the standard, recent hierarchical modeling suggests that depending on the specific comprehension task, there may only be 3 to 4 statistically distinct accuracy rankings, with shading and color saturation sometimes outperforming their theoretical ranking in complex spatial transformation tasks [cite: 8][academia.edu](https://www.academia.edu/3302739/An_Examination_of_Cleveland_and_McGills_Hierarchy_of_Graphical_Elements).</CONFLICTING_EVIDENCE> Despite this, for deterministic agent rules, treating position and length as the undisputed primary quantitative encodings remains the most reliable engineering choice.

## Technical Diagrams and Layout Algorithms

While data visualizations map quantitative values to visual marks, technical diagrams (e.g., architecture maps, flowcharts, UML) rely on topological structure to convey meaning. The agent must not attempt to explicitly position nodes via absolute (X,Y) coordinates; this mathematically guarantees layout failure due to spatial blindness. Instead, the generation skill must delegate spatial rendering to deterministic layout algorithms.

### Edge Crossing and Node Occlusion
To evaluate the goodness of graph layouts in technical diagrams, algorithms optimize against widely agreed aesthetic criteria: minimizing the number of edge crossings, maximizing the minimum crossing angle, and eliminating node occlusion (overlaps) [cite: 9, 10]. Node-link diagrams that minimize these artifacts are strongly correlated with higher human comprehension speeds [cite: 9, 10]. However, optimizing edge crossings and crossing angles simultaneously in a straight-line drawing is an NP-hard problem, necessitating heuristic approximations [cite: 10]. 

### The Sugiyama Framework and Layout Engines
Production-grade diagramming tools like Mermaid.js rely on the Sugiyama framework to solve this NP-hard problem via four discrete phases: 1) cycle removal (reversing back edges to create a Directed Acyclic Graph), 2) layer assignment (grouping nodes into ranks and inserting dummy nodes for long edges), 3) crossing minimization (typically using barycenter sweeps), and 4) coordinate assignment [cite: 11]. 

*   **Dagre (Default Engine)**: The default layout engine in Mermaid is `dagre` (a JavaScript Sugiyama implementation). It is fast and requires zero installation overhead, making it ideal for graphs under approximately 50 nodes [cite: 12, 13].
*   **ELK (Eclipse Layout Kernel)**: For dense, hierarchical, or nested graphs, Dagre's quality degrades sharply, producing severe edge crossings and awkward spacing [cite: 12]. The agent must dynamically detect graph size/complexity and inject a frontmatter directive to switch the layout engine to `elk` (`@mermaid-js/layout-elk`). This provides superior edge routing and handles deep subgraphs at the cost of a measurable 100–300 ms processing latency penalty [cite: 12, 13]. 

## Colour Design and Measurable Pass/Fail Criteria

A production-grade visualization skill cannot rely on hardcoded hexadecimal arrays or LLM-hallucinated color strings. It must dynamically generate and verify colors using perceptually uniform color spaces (UCS) and enforce distinct separation for Color Vision Deficiency (CVD).

### Perceptual Color Spaces (CAM16-UCS vs. CIELAB)
Traditional RGB and HSV color spaces are perceptually non-uniform, meaning mathematical distance does not equal visual distance [cite: 14][frontiersin.org](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2019.00274/full). An agent must evaluate colors in a UCS. While CIELAB is historically standard, empirical testing demonstrates that CAM16-UCS (an evolution of CIECAM02) provides the most accurate prediction of human color perception across the entire color gamut [cite: 15, 16][opg.optica.org](https://opg.optica.org/oe/abstract.cfm?uri=oe-30-24-43872). 

Color difference in these spaces is calculated using the Delta E ($\Delta E$) metric. The interpretation of $\Delta E$ serves as the foundational numeric threshold for your color verifier scripts:
*   **0-1**: Not perceptible.
*   **1-2**: Perceptible through close observation.
*   **2-5**: Noticeable difference.
*   **>5**: Strong, obvious color difference [cite: 17, 18][cols4all.github.io](https://cols4all.github.io/cols4all-R/articles/01_paper.html).

### Enforcing Categorical, Sequential, and Diverging Scales
The agent must categorize the data and apply differing $\Delta E$ rules based on the scale type:
1.  **Categorical (Qualitative) Scales**: Used for unordered data. The script must enforce a minimum $\Delta E > 10$ between all color pairs to ensure they are "substantially different" [cite: 17][cols4all.github.io](https://cols4all.github.io/cols4all-R/articles/01_paper.html). Additionally, to avoid rainbow-washing, the hue spread must exceed a threshold of 90 degrees in a polar color space [cite: 17][cols4all.github.io](https://cols4all.github.io/cols4all-R/articles/01_paper.html).
2.  **Sequential Scales**: Used for ordered numerical data. The generator should fix the hue (hue width < 15 degrees) and interpolate solely along the lightness axis in CAM16-UCS or OKLab [cite: 17][cols4all.github.io](https://cols4all.github.io/cols4all-R/articles/01_paper.html). The $\Delta E$ between discrete steps in a sequential scale can be lower (e.g., 2 to 5) because the sequence relies on relative lightness progression rather than absolute distinctness [cite: 17][cols4all.github.io](https://cols4all.github.io/cols4all-R/articles/01_paper.html).
3.  **Diverging Scales**: Must possess a neutral midpoint that interpolates outward toward two distinct hues with symmetrical lightness profiles. The script must anchor the scale to a neutral gray (e.g., $L^* = 50$ in CIELAB, or representing an 18% visible light reflectance) before ramping outwards to highly saturated endpoints [cite: 19, 20, 21]. Limiting diverging palettes to 3 to 9 discrete steps ensures perceptual legibility [cite: 19].

### Color Vision Deficiency (CVD) Simulation Thresholds
To guarantee accessibility, color palettes must be verified against simulated protanopia, deuteranopia, and tritanopia [cite: 17][cols4all.github.io](https://cols4all.github.io/cols4all-R/articles/01_paper.html). 
*   **The Verifier Protocol**: The agent applies a physiologically-based CVD transformation matrix to the proposed palette. The empirical standards for these matrices are the algorithms defined by Viénot (1999) and Brettel (1997), which handle extreme RGB values effectively by projecting coordinates along the dichromat missing axis [cite: 22, 23]. Algorithms utilizing Machado (2009) are also acceptable, particularly for simulating anomalous trichromacy, but legacy matrices like "Coblis V1 (ColorMatrix)" must be explicitly banned from the pipeline due to documented inaccuracies [cite: 22].
*   **Failure Mode**: If deuteranopia simulation drops the $\Delta E$ of a critical chart distinction (e.g., Target vs. Actual) below 5.0, the visual distinction is lost (the Intersection over Union, or **IoU**—a metric measuring the percentage of spatial overlap between two bounding boxes—drops to zero in spatial recognition tasks) [cite: 24][journals.viamedica.pl](https://journals.viamedica.pl/rpor/article/download/112214/88860).
*   **Exit Code Rules**: The script must return a non-zero exit code if $\Delta E_{cvd} < 5$ for any adjacent or categorical data pairs [cite: 17, 24][cols4all.github.io](https://cols4all.github.io/cols4all-R/articles/01_paper.html).

## Accessibility Requirements for Charts and Diagrams

Visualizations generated as SVG/HTML must natively support users reliant on screen readers and comply with Web Content Accessibility Guidelines (WCAG) 2.2. A pipeline generating raw `<svg>` tags without semantic structuring is fundamentally flawed.

### WCAG 2.2 Non-Text Contrast (1.4.11)
A pervasive failure in automated charting is adequate contrast for structural elements. WCAG Success Criterion 1.4.11 dictates that UI components and graphical objects—including chart axes, data point markers, pie slice boundaries, and trend lines—must maintain a 3:1 contrast ratio against their adjacent background colors [cite: 25, 26][openfieldx.com](https://openfieldx.com/data-visualization-accessibility-tips-for-edtech/). 
*   **Verifier Logic**: The agent must extract the hex codes of the chart background and the geometric marks, pipe them into a WCAG relative luminance formula, and fail generation if the ratio falls below 3.0:1 [cite: 26][testparty.ai](https://testparty.ai/blog/wcag-non-text-contrast-guide). 
*   **Redundant Encoding (1.4.1)**: Color cannot be the sole conveyor of information [cite: 25][openfieldx.com](https://openfieldx.com/data-visualization-accessibility-tips-for-edtech/). The agent must inject redundant encodings, such as varied stroke dashing for lines, varied shapes for scatter points, or direct text labeling.

### SVG Screen-Reader and WAI-ARIA Patterns
SVGs are inherently interpreted as images unless explicitly structured as a "graphics-document" [cite: 27][unimelb.edu.au](https://www.unimelb.edu.au/accessibility/techniques/accessible-svgs). The W3C Web Accessibility Initiative - Accessible Rich Internet Applications (WAI-ARIA) Graphics Module establishes three critical roles that the SVG generator must append:
1.  `role="graphics-document"`: Applied to the root `<svg>` node, signaling a complex graphic whose structure conveys meaning [cite: 28, 29][fizz.studio](https://fizz.studio/blog/accessible-charts-with-aria/).
2.  `role="graphics-object"`: Applied to grouping nodes (`<g>`) that represent logical sub-components, such as an entire X-axis or a specific data series [cite: 28, 29][fizz.studio](https://fizz.studio/blog/accessible-charts-with-aria/).
3.  `role="graphics-symbol"`: Applied to atomic elements (e.g., a single `<rect>` or `<circle>`) representing an individual data point [cite: 28, 29][fizz.studio](https://fizz.studio/blog/accessible-charts-with-aria/).

<CONFIDENCE:HIGH>Furthermore, the SVG DOM must include a `<title>` (providing a short alternative description) and a `<desc>` (providing detailed data summaries) as the immediate first children of the root `<svg>` node. However, screen readers often flatten SVGs, making traversal tedious [cite: 27, 30][unimelb.edu.au](https://www.unimelb.edu.au/accessibility/techniques/accessible-svgs). Therefore, a fully compliant agent must also generate a visually hidden `<table class="sr-only">` containing the raw dataset, linked via `aria-describedby`, ensuring non-visual users have tabular access to the exact values without traversing hundreds of DOM nodes [cite: 30][vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/rich-screen-reader-vis-experiences/).</CONFIDENCE:HIGH>

## Automated Quality Checks and Verifiable Linting

To migrate from probabilistic LLM chart creation to deterministic generation, the visualization skill must implement a rigorous linting phase. Systems like Draco (using the Clingo constraint solver) and VizLinter have proven that Answer Set Programming (ASP) and hard-coded constraint logic can successfully trap deceptive or unreadable outputs [cite: 31, 32, 33].

### Linter Engineering Rules and Exit Codes
The verification script should scan the generated SVG/Vega-Lite JSON against three categories of constraints:

1.  **Validity and Legality (Data Integrity)**:
    *   *Check*: Do the derived data types match the encoding? (e.g., continuous quantitative data mapped to an ordinal color scale is illegal) [cite: 34][computer.org](https://www.computer.org/csdl/journal/tg/2023/01/09903555/1GZonJBJC1y).
    *   *Check*: Axis Truncation. If mark type is `bar` or `area`, and the `y-axis` domain does not start at 0, throw a fatal exit code.

2.  **Readability (Geometry and Label Collision)**:
    *   *Check*: Label Overlap. The linter must compute the bounding boxes of all text elements (`<text>`). If `Box A` intersects `Box B`, it triggers a collision state [cite: 35, 36][arxiv.org](https://arxiv.org/html/2407.00981v1).
    *   *Mitigation*: The agent must be programmed to silently degrade: move labels, add ellipses, skip ticks (e.g., Highcharts' algorithm updates the tick interval to the closest non-colliding point range) [cite: 36][changelog.highcharts.com](https://changelog.highcharts.com/highcharts/), or rotate labels by 45 degrees.
    *   *Check*: Occlusion. For scatter plots, if $>30\%$ of data points overlap, the linter must force the generator to either decrease opacity ($\alpha < 1$) or reduce marker radius [cite: 37][researchgate.net](https://www.researchgate.net/figure/The-Mackinlay-ranking-of-perceptual-task_fig2_221098028).

3.  **Perceptual and Colorimetric Consistency**:
    *   *Check*: Contrast and $\Delta E$ thresholds (as defined in previous sections) using headless color analysis [cite: 38][ieeevis.b-cdn.net](https://ieeevis.b-cdn.net/vis_2024/pdfs/v-full-1290.pdf).

By framing visualizations as a set of logical facts (e.g., `entity(encoding, mark, type)`), the linter can enforce integrity constraints. Any constraint failure should return the exact node and error string to the LLM agent, prompting an automated re-generation loop.

## Documented Failure Modes of LLM-Generated Charts

Current end-to-end LLM visualization benchmarks expose severe failure modes when models map data to visual code. According to zero-shot tests on the VisEval dataset (Text2Chart31), LLMs initially fail on nearly 40% of inputs, with supervised fine-tuning (SFT) reducing code execution failures to below 15% [cite: 39]. However, execution success is deeply misleading.

### Hidden Hallucinations
The most dangerous failure mode is the "hidden hallucination." Because rendering engines (like D3 or Matplotlib) will faithfully execute whatever numbers they are fed, an LLM can produce a chart that executes perfectly but represents mis-extracted or miscalculated data [cite: 40]. 

The *DeepChart* benchmark isolated this phenomenon by scoring models stage-by-stage. Within complex documents (the Ecosystem domain), LLMs achieved an average Execution Rate (ER) of 78.2%, yet their Visual Accuracy Score (VAS)—which tracks if the rendered chart accurately maps the true underlying data—dropped to just 44.7% [cite: 40]. VisEval similarly documented that even after achieving a 95.4% execution success rate (4.6% error rate), manual audits revealed a 6% direct hallucination rate in the rendered visual data [cite: 39].



*   **Real-World Case Study (The "Frisbee" Effect)**: Hidden hallucinations also extend to Multimodal LLMs evaluating diagrams. In a documented causality study on the InstructBLIP model, the LLM hallucinates a non-existent "frisbee" when interpreting an image of a boy on a grass field simply because frisbees frequently co-occur with green fields in its training data [cite: 41]. Similarly, GPT-4 and Gemini exhibit high failure rates on the Visualization Literacy Assessment Test (VLAT) by heavily relying on pre-existing semantic knowledge about the domain rather than accurately reading the geometry of the specific chart presented to them [cite: 42].

### The Extract-Reason-Visualize (ERV) Mitigation Protocol
To programmatically eliminate hidden hallucinations, the generation architecture must abandon the "one-shot prompt-to-chart" approach. The skill must be re-architected into a staged **Extract-Reason-Visualize (ERV)** pipeline, capturing key data-science bottlenecks [cite: 40]:
1.  **Extract**: The LLM isolates source data ($D_{src}$) into a JSON payload.
2.  **Reason**: A secondary prompt (or deterministic script) derives the chart-ready quantities ($D_{der}$).
3.  **Audit**: The verifiable intermediate state $J = (D_{src}, D_{der})$ is saved as an evidence file.
4.  **Visualize**: The downstream renderer (e.g., Vega-Lite) relies on a rigid data contract. To guarantee execution, the generated intermediate state must be strictly typed against an established JSON schema, such as the official Vega-Lite v6 schema (`https://vega.github.io/schema/vega-lite/v6.json`) [cite: 43].

### Visual Overflow and Legality Bugs
At the rendering level, state-of-the-art LLMs consistently struggle with spatial reasoning (spatial blindness), failing to comprehend the canvas dimensions they are writing code for [cite: 44][alphaxiv.org](https://www.alphaxiv.org/abs/2601.14943). This results in legends rendering outside the canvas boundaries, illegal sorting of categorical variables, and overplotting, requiring the headless linting checks defined in Section 4 [cite: 35, 45]. 

## Evaluation of Visualization Quality

For an agent pipeline, knowing *how* to measure success is as important as the generation itself. Empirical visualization evaluation relies on a blend of automated scanning and model-based judgment.

### Automated Metrics and Benchmarks
Modern benchmarks like VisEval deploy heterogeneous checkers to assess output across three vectors:
*   **Validity**: Does the code execute without syntax or runtime errors? [cite: 35]
*   **Legality**: Are the data constraints preserved? (e.g., did the LLM illegally sort a time-series axis alphabetically?) [cite: 35]
*   **Readability**: Are there overlapping DOM elements or canvas overflows? [cite: 35]

### VQA and LLM-as-a-Judge
Because deterministic scripts cannot fully evaluate aesthetic "expressiveness," researchers leverage Visual Question Answering (VQA) models (e.g., using ChartQA or PlotQA datasets) as automated judges [cite: 46][themoonlight.io](https://www.themoonlight.io/en/review/charting-the-future-using-chart-question-answering-for-scalable-evaluation-of-llm-driven-data-visualizations). A generated chart is passed to a multimodal LLM alongside a set of factual questions about the underlying data. Accuracy is evaluated using strict parameters for categorical answers and a relaxed $\pm 5\%$ tolerance for numerical inferences [cite: 46][themoonlight.io](https://www.themoonlight.io/en/review/charting-the-future-using-chart-question-answering-for-scalable-evaluation-of-llm-driven-data-visualizations).

### Human Comprehension (VLAT and Log Error)
Historically, chart effectiveness is evaluated via crowdsourced psychophysical experiments measuring task time and absolute log error in proportion judgments [cite: 47, 48][researchgate.net](https://www.researchgate.net/publication/221515971_Crowdsourcing_graphical_perception_Using_Mechanical_Turk_to_assess_visualization_design). More recently, the Visualization Literacy Assessment Test (VLAT) is used to ensure charts communicate correctly to lay audiences [cite: 49][web.cs.wpi.edu](https://web.cs.wpi.edu/~hmansoor/vizliteracy_poster.pdf). The rubrics from VLAT (testing data retrieval, extremum identification, and trend correlation) can be prompted into the LLM-as-a-Judge to evaluate its own visual drafts [cite: 42, 44, 49][web.cs.wpi.edu](https://web.cs.wpi.edu/~hmansoor/vizliteracy_poster.pdf).

---

## Knowledge Gaps

*   **<MISSING_DATA>Agentic Latency and Token Costs</MISSING_DATA>**: Detailed, real-world benchmarks regarding the total token expenditure and latency overhead for a multi-pass ERV pipeline coupled with self-correcting linting loops were not available in the literature. Establishing operational viability will require internal load testing.
*   **<MISSING_DATA>Optimal SVG Structure for Complex Path Data</MISSING_DATA>**: While ARIA roles handle basic bars and points effectively, there is insufficient standardized consensus on how to make highly complex topographies (e.g., Sankey diagrams or parallel coordinates) accessible beyond dropping to an underlying `<table class="sr-only">`.

## Recommended Next Steps

1.  **Build a CAM16-UCS Headless Color Script**: Implement a lightweight Python or Node module utilizing the Viénot (1999) or Brettel (1997) matrices to programmatically test all agent-generated palettes for $\Delta E > 5$ separation under simulated Protanopia and Deuteranopia. *Rationale*: This is a deterministic rule that completely eliminates a major accessibility failure mode.
2.  **Architect the ERV Checkpoint System**: Separate the agent's workflow so it outputs an intermediate data file typed strictly against the Vega-Lite v6 JSON schema *before* attempting DOM generation. *Rationale*: Literature proves that end-to-end LLM visual rendering obscures mathematical reasoning failures (hidden hallucinations).
3.  **Integrate a Geometric Bounding-Box Linter**: Deploy a headless DOM renderer (e.g., Puppeteer or Playwright) into the verifier script to execute a `.getBoundingClientRect()` overlap check on all SVG `<text>` nodes. *Rationale*: Addressing "spatial blindness" requires an external computational check for label collision, which LLMs inherently cannot perceive.
4.  **Create a Strict Base Template for SVG ARIA**: Hardcode a wrapper template that natively injects `<svg role="graphics-document">`, `<title>`, `<desc>`, and a `<table class="sr-only">` block into every agent prompt. *Rationale*: Eliminates the dependency on the LLM to remember complex, multi-layered WCAG compliance standards.

## Comparison Table: Implementation Frameworks for Visual Linting & Layout

| Feature / Metric | Draco v2 (ASP) | VizLinter | Custom Deterministic Script (Puppeteer/D3) | Dagre & ELK (Diagram Layout) | LLM-as-a-Judge (Multimodal) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Underlying Tech** | Answer Set Programming (Clingo solver) | ASP + Linear Programming | JavaScript / DOM APIs | Sugiyama framework heuristics | Pre-trained VLM (e.g., GPT-4o, Claude 3.5 Sonnet) |
| **Target Operation** | Recommending visual designs; rule constraints | Detecting and automatically fixing layout bugs | Collision detection, WCAG contrast verification | Minimizing edge crossings & node occlusion | Assessing narrative fit, overall aesthetic coherence |
| **Operational Overhead**| Compute intensive (logic solver overhead) | Compute intensive | Low latency (~< 50ms Node execution) | Dagre: near-instant. ELK: +100-300ms latency penalty | Very High (API cost, often >1 second latency overhead per loop) |
| **License** | MIT License | CC BY 4.0 / Apache 2.0 / BSD-3 | Custom / Environment specific | MIT (Standard Mermaid ecosystem) | Proprietary (API) or Open Weights |
| **Suitability for Agent**| Excellent for backend schema validation | Strong, but complex to maintain | **Ideal for CI/CD and script-based verifiers** | **Mandatory for topological architecture diagrams** | Best reserved for final QA pass; too slow for iterative geometric linting |

**Sources:**
1. [cstopics.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHJvRPQW3gJdGIBfUg2eKsucCyU5zxCCxeK573D442v3PFAmbmNIXCdhD2USXh6RMCNvFda01ZJfUNRW1vWvj4oU8-aTSNzlv09h17RS0varpWuOjJ-LTa7WL22psQg5q9zM0rOi-pyd7MZiWsD4VDpSHaNDeNxIi6vE_KTzpSFfWNousxBMMbZc04lAdsCvT-GHbp8miU4JdHPaatrdk6W5QXhozlTgFMeTVeygTJi7zS2HOkzeBw=)
2. [priceonomics.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG3Z30apM1SKBoeYc9kxFEdT861JfcRIObu1n2LUkJRq-6BbpTs9YzAMM8yY0ZiROnx9nuKSljrq3MAP74PVYX6gxsAHH65Ua_xHZzMoo0fzNeHsPPwEo7sPpnOxq4qkiMcU1i9vcys6V6Gpdek07jK3Up_c5xNYj3w0yegVGsU)
3. [columbia.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGQAFApPdgRdSTkY-B1KZm3F1vJOO8U76T3dSFzBX2wjYmgMX-m_TFFUiBEZgZLWNKisDHpeV9jqdoLCXryM3C3JPAwyrWpa48NH44xfiQnBDFMJyOQzI8sOMM3aloHEDFdWZA7s0FEpwHcmOHnHgbMz1kYyO7nui38Zxo79GST)
4. [scribd.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGYSu8aWWIdZ3f8AaGM9nud55Ous7DE8bmSq4LLAkwN_CP9vH5SqbF-1acp1Arm257wnXd3nwl96ekrRRsUfo0vyQvmSdtGLo5gjgVdI9kaTADq5ryeixkrhV-oq6QgG19T976WrXvPmDZ5)
5. [flowingdata.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG_oQsxGP4OsR9jNVU6JRypBI3pyGeCGZ9zGl9EGhKhDAsy9RkU6MSp1pGEKmf60g8IjPJ8F-xPZhrj8AO05CYaCQ2K5xwEAJhn0Q3c07qcVn0Q-_4aPc_oDuTtiGoA5Oukm1r5zV2aZyOuUxdJR8f5QS3Kz90Widc2DXB65A-pwS0MxeHOoGS_fgBY)
6. [namwkim.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHStNL2NsgQw4FhULZqcO1iXaBtdEMjgAFAy78zOTz4-DNh-M3Mge211E5kh8cL0MKQDBOYjdtNr5QWHeCs8Rf9_qTRhpwUcR14rI72CO1Id1pUpy2dgQzs-cbx0BMdf5Bu660o4fWzq_SPalSQrGr9LMnbLnt_wp8Ae1WHbsD508I4dprZOekTxgU=)
7. [auckland.ac.nz](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEtP0PmSMcB8-zvDWVRFDTJXP5OZ4tEFnxKr1ekRYV2lxDZLjivX8S5Z-jKGb6ThKxLyn8vUZdkj-rymkSdalGmzXUuVcsGeNOq20WABOMAP3RKxGtQPDip9jXf4K1hNBTNYJ7K24Z20uKxo9cZOWjmHYJNuDaazFjPH1qB-77S)
8. [academia.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFmIwRYnRUeJChE4dhzoEtXn9_EA8ZGjt9FLOt5Xr1h4TIZkD0FhTV1IvxqRnk6C6JZ4b0TIHH0opbdnzSfkFIQjnlMsoZ8LC7sjbRJWSohJXB_T-t8hr45TCE0wGFsbZHhDsk2Aj8924HugiOPLgQfemR4BJaj9DvlMZzlppzUcenHULhD9XarC1rQCNAEvGw7wRFtsUJ9JJlxc8HQkw==)
9. [computer.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFz9cTnAOm_9RDiEI43qIVU82fRFQdPjXKtnwsamOEzp0UQk9Zp2pwY54QDTA5_-NYS2obp5KcZJcdnBJRtuN6UNSVTenfoCMUkkWHFuWGhDfozlF3r0uO5XkgRvjaORwBfoCEBnmgej9FfZBudc3OMbgriNKVX1MhfoSU=)
10. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFOp8jYNk9MKeE6nlBchiVJyVad38ALhYxA7IJIDKMioB-n3_Hb1zvbTdO6brHyHZ87dXyG0ei_PSiKD6mQhVxpm_eI1xVeK_Djmd10azgXTgwPmYezBb8HwQ==)
11. [codepuz.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGpgV6Hz6qBlPdwD73XZPsIQKYnU-6NimTfWVOOka2OLsgv2WIgn3dkrBD5QVWaQN3eyxntCW4a8kj91ulLbzBubQegfEuHGCJpPpp1PxfLjt-eKMawW7UhMEb6SVY2Dkbx_x2Jv9z0vTUQWkPeODzXybtdTj0t9_vnZvHS)
12. [towardsai.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEyBWaRdFda0gIv_YybE44-gry-TuXwuDUAQbB_sdORPvUN8GtsAmtAeovptpqGUt3XqDaBcONsvukdy03_CDWKTOSSSrqv-Rz0DKMJlxYqgz8UiBQKZtaraF6jD8gUZdH44D06fJb4rTmFAHrTH8QR3atCM2c=)
13. [mermaid.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHW3zWi_DY8G-yV_yeE4FITuGZX0kHvoRF3eIxBGMxrexJH486UvDZ9bGNWpnMfQPM2R5-j7Qaaf6U9KJEa7VJ3xtD0_lNMdRx6miQnhFWBGrAyEcv-li0KTy58X4MjlFktSTJ4ZIts5Q==)
14. [frontiersin.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHbOYs7KKexZjog8fQf5Ds1O4aujUE7B5lsqmjmkpWmCeX6lvXDAIIqDYOpvDV7rcZYX3O1lyx1kL8DKEAM065ambVTo1n1LxKht8sVAn4xkeVEVjBCUa1u_jKKWLIlKheXijbzBAIkapPc3R74gBJm5zvjNdlwXHLzImFboRTdzHFgq4DEK5iuYRvjPloaJQ==)
15. [optica.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEHMaXp2vuWacr97KgncPfoP6N-m8ZynRPd4p7KC418vU4yXR0DWcj1lazF2OibwyzmBqXP5ywRZGcdbvMQClPUbO15dFQqm1BxvBYxp-CmnBbwuFLvxuxjP83f_23xrQJLKRkolE5754Y7Llhpmrw=)
16. [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFFvtkShvD3ac0JKp8nOWTaYvP1VkIi3W00-3jgvNWcE8u1aTs1DQABqUitMyahGQT6lBJGFTgGLDShhp5YkbGj9LLfH4PFY1PTsctNrKEZDkLiTqWjYGDsoq15PYSdj4wQJSS5Brw9sRtJaeYGjdqmSCOFYW_3zPzIzd87OfP1S3rz2INBdjyEkDrHvVCc6yREdvgPadD2hkQtiN6N3n6Z)
17. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHq00cma3NM43qrng2eU8hk22yQGqlpj9KmDvu9E3Xpn3ujL8KTr748_Mx_G_NYeJBoL1muceKl8wwp3rRE6Faxz7TdHyr71pkRzWZRhWkrgKvZJKD14fiGHED6UB2qvPVxXC6EQsOy7zW_tT0-1POXXmU=)
18. [biorxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEThCj7uorR-3tk0AwSCk-ykrf6fg_c69Zus_z4Qxe9wuGPssLoDdlrPMdwYaMxmWaPjc9_QxXfuzmE98z2-_crUdN4wHFtQyJ7-AyKZSw9EMfmbfsi2c1_61vfdnsv8C-CfrnZwFjDtIm_jqeCGYLBPKvWImELiBSbOsw=)
19. [stanford.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrvSm2eU2v6ZNH44pKiBu9tVjeMwpFyvuglbmsVpxhV9mD1y6D2ulMpg3TsoMFTWMMdE5oIIjjH6gyYrMUWj9qmf5ZcimWybNRa1lug-Vu1vrxPK9FhMCVzpg7UPL6Dtiba0CSBKrVLbzDUqbfJuxyow8CtdsGnkdDNN22ovrjfR04-nk=)
20. [scribd.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEuCUwPXXC0EMAy0ThOD5rQOEl3F3gw0afGIK5gsQ6in5KEGCQBA8PzVY3e_H6cIo3fFAUKUq4V48qceWWQwz4frHeZ-Cu71WUJ0TXSDkpo5KUb81iuK0AJE4PVa3CS1-n_lpqOQGUyi75ZC185)
21. [dokumen.pub](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE1h8deLST2Mwjc6KdWU5MSrGagZqRYchRN83Z4JcXgJZjLgnTpp7inTPFMw0s7pxHKsUJekzqWuQd1KL2HXLrQjkgtB-w8035ldPymgPqUL9QEJVdVTQWQ3B_nzUWL6barBDJIxkIgCRBWj_D179Y6Kw9e1A3PDNmcUb2j2Ey2dPoh5XiFfQ0m2f_T_ypI02-jMwcSlY-S6k3a7R2f9jyTeQQriInuSdQj4_GG1rsK3Q8T9IpeKwJAdw==)
22. [google.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEQuRgm-tnBPY3caRhXt0KM1BvuN63ilh2_yElj0MVFSaUxMyjESNNUqZH6RR4q5411iS6TKG4BRyOYUhMlEevQHDXQ9C2hMtRp62rNSe9tUekfrkd4xgDvrrdt7NSf_WvC7UR0u8LisFyElpUjXyN0rH_VBtuj_91Y2gdmEoTjXHnjGbHsCFwxybqZKtzbbX7bQ6i7bBfAr1jImpoVbhEbR4on4EHwOqCf1NA5qH-EXKZYw_upSRJMg67evA4LkzlU-j__YjH_)
23. [daltonlens.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFPFHrXt-nciH85tpIHPoN-KwwYxrM9RtFjaSThGAjeKEaFHf3THBHg-m0WxIHVBzDAi2jDyZKbZPYeOn1bg5OceJ0YCL5oAdfhiTa35PMNhtWqU4dUisCf0n3Aumhk0WPVV0RrOgpjjKxD)
24. [viamedica.pl](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFpuQDwGHEBDYGyjFixzlu9R3g7Qf_6lBhoZSuw349Oo-tOt7FWtACFJSKcWsBKS-nae-K4MXTxNzzZOi5f67EvYKARZ7gMalTeKkqDkBFVtH5T-_DiJTvsnaywFXBM7cF8xgCMsFI3uxhYtpOGY2ayFhL-AJHE)
25. [openfieldx.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFgvE4lASTQeaZLRYqimnib9pKsiboivzzVyIDYYJmr8cR8160wMHWf2M2OBGI2Vd0P2DNIdz82bqlxlQXMwzRidVmQhIV29ds3yiVrXKhhAyWTDtSgb7w-y29Cb3rw-zPb_yEIXhkGPOWivHAB19tMWeJy-Kjl9NdoQaC-ucY=)
26. [testparty.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGL1fs3h1FRjTvqLzKUyQ2O4aJDBiIkVl90WFkhv2-39ZB6_nNEzL9j71BQ5pP5GRFSupT_SQLDuA__iYUo1kUgPmWbN1Y-Xr5X0m-ySMkGM0RiZuw6uD6pf9B6t0B8drwZPX3haIVqX7vhXT0=)
27. [unimelb.edu.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE1G3mkK_2Ahw6JYhO2FKRSZvr2C-wjGbWttJ6TRjLmHJK_rgkHcRF1lZSdWuPq2p3wy-zKTTGyDGMbDRqn-JfbDRHb_fBeHSIZd0R5XkbZXehQniScG8qpc5wbTVJ_GDJsBqVQSY7xb-KSuearWyS6mRxUK1srpjk7)
28. [fizz.studio](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHUm3esw1zdDF6ertC6hz0Sz01DProifBh3xl4mvLQZbMuM56q6zpaztmkLsKs9OQwjYmgKRg008SRL-XVA185l_QuLS0Q2Fy1LQmgOSaFQYGhFpHwOcTXJMYTyL6A4x9zYlMToN3aS0mSBhw==)
29. [w3.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFBuVMrs1HYJKfCOJA7693pBCXAiOn7X5jjM9Zrqe87vqJTDg78E-dIWrF2PfMySrhQi2S9pfGpBfnyKSsbI3zBmN0edumYvFg038dDY0r8UmL6VFQ1Hj4CIi11thcX)
30. [mit.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHHKUcXLlm_l1z3phh-O2Bk72Ib_Wp7UdiaUgV46gz4Pq7SowS15Q8RnvRAN0_h5fuWoKAgEOq8DMv8ciuLmd9BZ9jz26GQhkhmKMRGTMA257Zjda9f1qcoQYq4PvgGe5h_9AmV0hKnsfszayCQPwa0LQrK-m0a9to=)
31. [idvxlab.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFJcXIdwD_AorP8IWcUrJI6lP5apMdvS4ZJUAJnJWV-49ZhhqtITlJVLt4hNLC-6leegkj-3AblzMb5ShXD3rEbcSteg1gApdlyHm8sSciIq6vqSLgmPtRT-ZIGsaJmg7vnvfKUXtPRCnWS4g==)
32. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHn87qPR_I5diNib5tnLdLqE0_Vz8nSKyGo7AqbmmS7GSj-MqQOph_it3Tkfi52JlhKInf6weUl-twL_1p9YIvTb5wij0ZK5ZMKo2y4YuF-6QG-_Qr1p1oYSAnCPD9qPCNUuA==)
33. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF5l05j5rOm6kEXXrFs-q2ygAzvGS7pOi9Kc2GEPHEhrI6FtypMCm9NBNvQMT33Q_M2XjTkkJc5ppMQtoC93XuIa9OeVD_aIAYq8s7UPb72mcIrvJ-f5A==)
34. [computer.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYz-VfWg4VSHMu2Jf0OP5V8elgPmCoyVeGeeF7zkznLEwDAMiLPQFIwTUdv4AjJUZD9IXuei6A9ZFuuhiD8121UqXaLODJyXiIXYvjfKv9TUh-j2w6fNa2imNTMr6-N3MNH3NsHVeoq1I48rtNKNTn7EZTprjlv6UHBoQ=)
35. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEAF0Xvk1-C-r4-EJmQRSudkY9z5Qr4X8qu5Wx4liN2E2dMWg8HAthNjqFP5pWwhzos7lCvZE_ZzcUvA44jJIdLIdUhnde2Nv4AYkCt9H6q5f7XXBkEt9IPsg==)
36. [highcharts.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGoer4TYCqaTjtS16NDpKH62Wxd6Z33j87aRYY4RPRYkegw4wZNiB84sTY-CfHjxwgnXDIznrlQQylt_pAkEEt_WyvKSOogDfrHzpxI_DadipkE64YuVdODGbt4slpIlBhvgA==)
37. [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEac1ClUw2Ubyqx1imjh-b3Hczd42n8RxNFWUOL3GOTKHq28yHPXB9GffIjMZW9BHxJymgk_rK_rQffx_2bzh7FSv8h85-Q5P4AleaSdIGxeZzFLjBLtpqWErk2rW-cnDP7cK4GSDRzo3u3cFYYdLNoxN4qe071pldvDewIDP3RD7I3zt3XGAEh3vrM7JV67qC9)
38. [b-cdn.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFgRUBu_XF90kjzK0FxfQwu-flv6up_lDQXf0gh6jQMCGUsmKBLkeAdG5eOb3b7IN8qmEkIfLW1vgLkyXrf0396NRyK2Ihq6qjOtsJE5At4AXNj6KEM65ieFKgAEQM5MNfyeNAjYZhmD6PcPYw7)
39. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFhNUb9gMippiBzSbL-vgsJL89g8YMmwrPLX_mrgyYiW7u7u43BC9syNmRLkVyzG3kysFw_zAiun_j-bH2LJ_xenrzSpHFYfSBJppZIQB-Q_Hy_ZsyD1IYZpg==)
40. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG-xtnGDsjgtXQaiEam_4FCZJ0WWVWxfovP18A06A5xTKdOUDC-kbhVmHKhX51j_ZWE4xgLlJaisuMVlRG9cluvH4ZVBdzpWImSJjitKX2bMoVfZogYZk4=)
41. [thecvf.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFEZXS2KL0F_Bh0DUYkhM29kIjs_6jFsJqsmfLDohvU97cZZxChMElveIslSeStwR2TUcb5ZlrmcNSH8vRGrt7K7r3lrLsUvWdqlzIpB8TEbp-AkyjEAkei_y7fTJlPnOHghM-6T6JF-eXWhliIkJNrxHaS0uBm20y6cy5WG_a3JOQiM6qOP-8n2UuUp3ayzouQ7BUR4xXAN3azPqszOfx-khS91m7okWUdxLRoougkRtXhX6gzuAlEuBPZaDqYzJbYxc4zx-hxXeIXAw==)
42. [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG0nCssCmwRtkmeAhx_bC7vuAzkIGnCZTGt4fQnNnJMyhNndmpMKLFDYAFKmoSITaLWJaDIg6rf0IPG14qXujneoCYAC5gEnX4kVPh3I4nxWYanv68VZl3TLkU4qZmfIfA3g1K9vPev3NvqGarhTTJPtdeD72jiaj4XRaqLQrmMHh3MSDMktsuzR7f2hmmgzkIxGSe9FyrGzB4sqMCoTexrkvtBj4K0Cqwa2koWfNo08t7jeY1mt9RzaREvpwGIZF6JVWBllHrDendGRL7Wbw==)
43. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGGbhn_MRjgmfvtaEuGQf6X7A6CzYyot_D3FgGZszA0581bwp9UY7LMO7cBYoI7tvVeAGN6DEZpqfmqSE5nmIpxh8g_VkAQ7aM5slPzB90zHMGjzTwd3sB7V0TSRFEfhA5E1an1qA==)
44. [alphaxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHYuiZNP7nYq9JPZmhDfJzLkcBg7FJATpUSJlthYgbsJYThR6hsv4PBM5UKm8WpTQDB3EseTgIaAyb_GUnYzuAoU5EyCZeP3ZnNao4NrV8ihmQWiVMq41TmbN2UeK8=)
45. [wustl.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFSlf8C0wdMhQEPtsB-8l6hRnDjbVJFmvFTZiGhvFQY1-uKNi9QJHJE7RDjaj3hGHqCF1IsSyKWrWoMrvqzHNLoUEPvtKuQA5wHU0ZPEZP1N2eGBq3fp5_4MqOTvQokskw6C77myo9uP2exF_Wv4fSntT0PiPZ8G1c=)
46. [themoonlight.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG7fahTGMmbwh_-usuRoz6j6YLNhq8mDSC-tfJTtLaJzfrLuay7lSZRECJX3maxBWtIj-j6m96hd0JHzZgpTfrlNrkkwQFAiiHiTk2h5-uL1N3dAVzuaQd5eyzS2oBZuL5-VeawjP1vDOYu1YJuXn-ZStf2XhHVgEDSMB7l0JGKlw34miHUvpLTp_1OUFwlN1tgVsVczREMyO9aRy5ENFSGiTL_xDLbtWGQchfKeZPfsCkh9rVzkpokUuIJ3dLYhwFgj_8H-_8kOHo=)
47. [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEde0lMA567QyZQom_X_KuikGH4hUu55u6dza9NrFveA9jbXKnL5NejKjiu1NhB2ApZCvrr_QYkVWvDlC-a5EcQFLAJq3jqUDH46C30gS20DRvSuFN7CX0XHGz41HVjHr7gUbwwT6oi4SB8fDY5WqfRVQiUPdTtK0YU4h4z1MdhVMe6D4jnCQPf--sqyk4rm4T_tdQSAxpmni7-vh8Xi1YWSuAcEX5btYFMUwouFOnmPqY8XyCY6xldjv8PXhyyHEil)
48. [northwestern.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGS_F_99AUQPZUPVKef8f1Kmw8lePBG-Hd5zOcsYYbKofxgSG8-nz4ObnbVLcpiZcaTwa4i8aaxFsMcTgDs3yOZ737njzuT8mDhRG1Tda2KzQaxULS7aXcCLnoYx89b0SaTnpkAjmcdHC9NUZaDLsLD2amJw-U3d1ZXyYy0hePlK2NEGJlt5RmOGlYUtg==)
49. [wpi.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGiAplPeWj8K6D9Aec-1ZKTaq0dA020Dw1-aU5k62htlhZSRQAyDhDVYg4IVx4qZJWoEyZyoFLPdSEb59dN5uCOO_Bztrvh4T0QA-7HfR9Gs21_mZKnRk3g_vXNoA8UlrNX4sNuqLb258SfIgEQ)
