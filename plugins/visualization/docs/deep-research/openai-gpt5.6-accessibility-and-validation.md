---
title: "Accessibility and Validation Standards for Automated SVG Data Visualisations"
run_id: dr_5f56a2de679b07cc
question: "What does the empirical evidence say about producing high-quality static and interactive data visualisations and technical diagrams as code (SVG/HTML) — specifically: (1) graphical perception and encoding-accuracy findings that should govern chart-form selection and mark design; (2) colour design for categorical, sequential and diverging scales including colour-vision-deficiency separation thresholds, perceptual colour spaces (CIELAB/OKLab/CAM16-UCS) and measurable pass/fail criteria; (3) accessibility requirements for charts and diagrams (WCAG 2.2 non-text contrast, redundant encoding, screen-reader/ARIA patterns for SVG, alt-text and data-table equivalents); (4) automated quality checks and verifiable linting for generated visualisations (label collision, occlusion, geometry, axis truncation, deceptive encodings); (5) documented failure modes of LLM-generated charts and diagrams and what measurably reduces them; and (6) how visualisation quality is evaluated (task-based comprehension studies, published benchmarks, automated metrics, rubric and judge protocols)."
provider: openai
model: gpt-5.6-sol
tier: max
archetype: technical
sources: 81
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 9.00
completed: 2026-08-30T06:24:05.086Z
---
## Executive Summary

- **(High Confidence)** Quantitative comparison should default to **position on a common scale**—aligned dot plots, bars or points—before unaligned position, length/angle and area. Cleveland and McGill’s ordering has been broadly replicated, but later studies show that no chart ranking is task-independent: chart choice must be conditioned on whether the user is comparing, retrieving, ranking, finding trends or assessing correlation. Stacked bars, pies, bubbles and other area encodings should therefore be rejected for precise comparison when an aligned-position alternative exists. [doi.org](https://doi.org/10.1080/01621459.1984.10478080)[doi.org](https://doi.org/10.1145/1753326.1753357)[doi.org](https://doi.org/10.1111/cgf.13409)[doi.org](https://doi.org/10.1109/TVCG.2018.2829750) ([faculty.washington.edu](https://faculty.washington.edu/aragon/classes/hcde511/s12/readings/cleveland84.pdf?utm_source=openai))

- **(High Confidence)** Use categorical, sequential and diverging colour scales only for their intended data semantics. Sequential scales need monotonic perceptual lightness; diverging scales need a declared, meaningful midpoint; categorical scales need unordered, pairwise-distinguishable colours. A six-class map experiment found over 95% comparison accuracy at adjacent CIEDE2000 distance \(\Delta E_{00}=10\), versus under 80% at \(\Delta E_{00}=2\), but this is not a universal colour-vision-deficiency threshold. [colorbrewer2.org](https://colorbrewer2.org/learnmore/schemes.html)[doi.org](https://doi.org/10.1080/23729333.2015.1055643) ([colorbrewer2.org](https://colorbrewer2.org/learnmore/schemes.html?utm_source=openai))

- **(High Confidence)** Colour accessibility cannot be reduced to “use a colour-blind-safe palette.” WCAG 2.2 requires meaningful graphical objects to achieve at least **3:1 contrast against adjacent colours**, ordinary text **4.5:1**, and large text **3:1**; a computed ratio of 2.999:1 fails. Colour also cannot be the sole visual means of conveying information. Require direct labels, shape, dash, texture, position or explicit symbols whenever colour identifies a category or state. [w3.org](https://www.w3.org/TR/WCAG22/)[w3.org](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast)[w3.org](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color) ([w3.org](https://www.w3.org/TR/WCAG22/?utm_source=openai))

- **(High Confidence)** Static SVG charts and diagrams need an accessible name plus a two-part alternative: a concise identification/summary and a long description or equivalent structured data. For inline static SVG, use `role="img"` with `aria-labelledby`/`aria-describedby`, backed by `<title>` and `<desc>`; `<title>`/`<desc>` alone still have inconsistent assistive-technology support. Complex charts should expose the encoded data in an HTML table where practical. [w3.org](https://www.w3.org/WAI/tutorials/images/complex/)[w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/7d6734)[w3.org](https://www.w3.org/TR/svg-aam-1.0/) ([w3.org](https://www.w3.org/WAI/tutorials/images/complex/?utm_source=openai))

- **(High Confidence)** The merged skill should use a **two-layer verifier**: inspect the authoritative chart/diagram specification and source-data provenance first, then inspect the rendered SVG/HTML. Image-only linting cannot reliably prove that marks encode the right values. Hard checks should cover source-to-mark fidelity, scale equations, axes, labels, clipping, collisions, contrast, accessible names, keyboard operation, node/edge completeness and geometry. [dig.cmu.edu](https://dig.cmu.edu/publications/2018-draco.html)[arxiv.org](https://arxiv.org/abs/2108.10299)[vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/visualint/) ([dig.cmu.edu](https://dig.cmu.edu/publications/2018-draco.html?utm_source=openai))

- **(Medium Confidence)** LLM chart and diagram generation remains materially unreliable. Recent benchmarks document non-executable code, omitted or hallucinated labels and values, wrong chart structure, layout collisions and low visual fidelity. In Chart2Code, even GPT-5 reportedly averaged only **0.57 on code-based evaluation and 0.22 on chart-quality evaluation** for editing tasks. Compiler/debugger and visual-verification loops measurably reduce errors: removing DiagramAgent’s compiler reduced diagram-to-code Pass@1 by **15.56 percentage points**, while removing its GPT-4o verification reduced it by **6.30 points**. [arxiv.org](https://arxiv.org/abs/2510.17932)[openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/html/Wei_From_Words_to_Structured_Visuals_A_Benchmark_and_Framework_for_CVPR_2025_paper.html)[openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Wei_From_Words_to_CVPR_2025_supplemental.pdf) ([arxiv.org](https://arxiv.org/abs/2510.17932?utm_source=openai))

- **(High Confidence)** Quality must be evaluated in layers: deterministic correctness gates, task-based comprehension, accessibility tests and only then perceptual or aesthetic judging. Code execution, SSIM/LPIPS/CLIP or a general VLM score cannot establish data correctness. A strong evaluation asks users or models factual questions whose answers are known from the data, records accuracy and response time, and separately evaluates visual clarity. [arxiv.org](https://arxiv.org/abs/2405.07990)[github.com](https://github.com/chartmimic/chartmimic)[arxiv.org](https://arxiv.org/abs/2508.21675)[arxiv.org](https://arxiv.org/abs/2304.07905) ([arxiv.org](https://arxiv.org/abs/2405.07990?utm_source=openai))

---

## Detailed Findings

### 1. What does the empirical evidence say about producing high-quality static and interactive data visualisations and technical diagrams as code (SVG/HTML)?

#### 1.1 Graphical perception and encoding accuracy

**(High Confidence)** Cleveland and McGill’s foundational order is: position on a common scale; position on non-aligned scales; length/direction/angle; area; volume/curvature; and shading or colour saturation. Later replication found area worse than angle and both worse than position, but did **not** establish angle as reliably worse than length. The defensible rule is therefore a partial ordering, not a claim that every adjacent pair has a stable universal effect. [doi.org](https://doi.org/10.1080/01621459.1984.10478080)[doi.org](https://doi.org/10.1145/1753326.1753357) ([scribd.com](https://www.scribd.com/document/697470806/cleveland1984?utm_source=openai))

**(High Confidence)** Task and data characteristics modify effectiveness. Kim and Heer studied **1,920 participants**, 12 trivariate encodings and variations in cardinality and entropy, finding effects from task, distribution and interactions between channels. Saket, Endert and Demiralp compared five visualisation types across ten tasks using datasets of **5–34 points** and likewise found strongly task-dependent performance. [doi.org](https://doi.org/10.1111/cgf.13409)[doi.org](https://doi.org/10.1109/TVCG.2018.2829750) ([idl.cs.washington.edu](https://idl.cs.washington.edu/files/2018-TaskDataEffectiveness-EuroVis.pdf?utm_source=openai))

**(High Confidence)** Bar-chart comparisons become less accurate when values do not share a baseline. Follow-up experiments broadly confirmed that stacked bars are worse than aligned bars and that widely separated bars, especially short bars, are harder to compare than adjacent bars. [doi.org](https://doi.org/10.1109/TVCG.2014.2346320) ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26356929/?utm_source=openai))

##### Encodable chart-selection policy

| Analytical requirement | Default form | Reject or downgrade | Verifiable rule | Confidence |
|---|---|---|---|---|
| Compare or rank quantitative values | Aligned dot plot or bar chart using one common scale | Stacked segments without a shared baseline; bubbles; 3D volumes | All compared marks share one scale transform and aligned baseline | High |
| Retrieve exact values | Table, direct labels, or position plus ticks | Unlabelled area/angle encoding | Each requested value is present as text or recoverable from a labelled scale | High |
| Show change over ordered time or another ordered continuum | Line or aligned points | Connecting unordered categories; silently bridging missing observations | X values are monotonic; gaps are broken or explicitly marked | High |
| Assess association between two quantitative variables | Scatterplot with common Cartesian axes | Bubble chart unless the third variable is essential | X and Y each map to one quantitative field; optional size encoding is separately verified | Medium |
| Compare parts of a whole | Aligned proportion bars or 100% stacked bars | Pie/donut when precise comparison is required | Parts sum to the declared whole within rounding tolerance | High |
| Encode magnitude by area | Area only where exact reading is not central | Radius proportional to value | Rendered area—not radius—must be proportional to value | High |
| Technical architecture/process diagram | Typed nodes and explicit directed/undirected edges | Purely decorative spatial proximity as the only relationship cue | Graph extracted from SVG exactly matches requested node/edge graph | High |

`<INFERENCE from="Cleveland & McGill 1984; Heer & Bostock 2010; Talbot et al. 2014; Kim & Heer 2018; Saket et al. 2018">For the merged skill, chart choice should be implemented as task-conditioned hard defaults with explicit override metadata, not as one global chart-ranking table.</INFERENCE>` ([faculty.washington.edu](https://faculty.washington.edu/aragon/classes/hcde511/s12/readings/cleveland84.pdf?utm_source=openai))

##### Axis truncation: use a scoped rule, not dogma

**(High Confidence)** Five studies of truncated bar charts reported that **83.5% of participants** exhibited a truncation effect, judging differences in truncated charts as larger; warning participants reduced but did not eliminate the effect. [arxiv.org](https://arxiv.org/abs/1907.02035) ([researchgate.net](https://www.researchgate.net/publication/395125457_Is_this_chart_lying_to_me_Automating_the_detection_of_misleading_visualizations?utm_source=openai))

**(High Confidence)** Newer evidence adds task dependence. A 2026 CHI study across seven bar-chart tasks found that truncation increased ratio-calculation error, but could improve value retrieval or filtering; direct labels materially mitigated negative effects in that experimental setting. [doi.org](https://doi.org/10.1145/3772318.3790617) ([doi.org](https://doi.org/10.1145/3772318.3790617?utm_source=openai))

`<INFERENCE from="The persistent truncation effect in ratio judgements; the 2026 task-dependent findings">Use the following policy: a non-zero bar baseline is an ERROR for magnitude, ratio or proportional-comparison tasks. Permit it only through an explicit exception carrying direct labels on every bar, a conspicuous break/truncation indicator, the full numerical range, and a declared retrieval/filtering task; route the exception to human review.</INFERENCE>`

For line charts and scatterplots, a non-zero axis should be a **warning rather than an automatic failure**, provided the axis minimum, maximum, ticks and units are visible. A log scale must be explicitly labelled and must reject zero or negative values.

##### Geometry invariants

**(High Confidence)** If a circle’s area encodes \(v\), radius must follow \(r=k\sqrt{v}\), because area is \(\pi r^2\). Testing only radius equality will accept a mathematically deceptive bubble chart.

Recommended deterministic checks:

```text
bar_height_ratio(i,j) == value_ratio(i,j)       # for linear zero-based bars
circle_area_ratio(i,j) == value_ratio(i,j)       # not radius_ratio
pie_angle(i) / 2π == value(i) / sum(values)
position(i) == scale(value(i))                   # within render tolerance
```

`<INFERENCE from="The empirical weakness of area judgements plus the geometry of area marks">Area-encoded charts should require both correct area scaling and an accessible numerical alternative; correct geometry does not make area a precise perceptual channel.</INFERENCE>`

---

#### 1.2 Colour design, perceptual spaces and pass/fail criteria

##### Scale semantics

**(High Confidence)** ColorBrewer’s established taxonomy remains valid: sequential schemes communicate ordered low-to-high values primarily through lightness; diverging schemes place emphasis around a meaningful critical midpoint and use contrasting arms; qualitative schemes represent nominal categories without implying magnitude. [colorbrewer2.org](https://colorbrewer2.org/learnmore/schemes.html) ([colorbrewer2.org](https://colorbrewer2.org/learnmore/schemes.html?utm_source=openai))

| Scale | Required semantic condition | Required perceptual behaviour | Automatic failure |
|---|---|---|---|
| Categorical | Values are nominal/unordered | Pairwise separation; no systematic lightness order that falsely implies rank | Two categories rely on colour alone or collapse under required CVD simulations |
| Sequential | Values have one ordered direction | Monotonic perceptual lightness; preferably monotonic cumulative colour distance | Any material lightness reversal; cyclic/rainbow discontinuity |
| Diverging | A meaningful centre exists: zero, target, mean, legal limit, etc. | Each arm changes monotonically away from the centre; centre is visually identifiable | No declared midpoint; asymmetric clipping that changes the meaning of equal deviations |
| Cyclic | Data are genuinely periodic | Endpoints join without a perceptual discontinuity | Use for non-periodic ordered data |

##### CIELAB, CAM16-UCS and OKLab

| Space/metric | Best use in the skill | Evidence-backed strength | Limitation | Decision |
|---|---|---|---|---|
| CIELAB + CIEDE2000 | Threshold checks and reproducible palette audits | Widely implemented; \(\Delta E_{00}\) has direct experimental use in visualisation/cartography | Mark size, background and viewing conditions change discrimination; CIELAB is not uniformly perceptual everywhere | **Required baseline metric** |
| CAM16-UCS | Offline palette optimisation and equal-step paths | A 2023 comprehensive comparison reported CAM16-UCS significantly outperforming the other tested models across groups of visual datasets | More computation and implementation complexity; not itself a CVD guarantee | **Preferred optimiser** |
| OKLab/OKLCH | CSS-native interpolation and web authoring | W3C CSS Color 4 identifies OKLab as perceptually uniform and documents improved hue behaviour over CIELAB/LCH, especially around blue/purple | Its simple Euclidean distance should not be presented as a universal discrimination threshold; recent work still finds limitations relative to fitted colour-difference formulae | **Preferred CSS interpolation space, not sole audit metric** |

CAM16-UCS was introduced in 2017 as a replacement for CAM02-UCS; a later comprehensive test reported it significantly outperforming the other tested models across all groups. [doi.org](https://doi.org/10.1002/col.22131)[doi.org](https://doi.org/10.1002/col.22844) ([onlinelibrary.wiley.com](https://onlinelibrary.wiley.com/doi/abs/10.1002/col.22131?utm_source=openai))

W3C CSS Color 4 states that OKLab and the older Lab are designed for perceptually even spacing, while also documenting CIELAB/LCH hue curvature and visible blue-region shifts that OKLCH avoids. [w3.org](https://www.w3.org/TR/css-color-4/) ([w3.org](https://www.w3.org/TR/css-color-4/?utm_source=openai))

`<CONFLICTING_EVIDENCE>[OKLab is operationally attractive and standardised for CSS interpolation, but CAM16-UCS has stronger broad colour-difference validation and CIEDE2000 has more direct threshold evidence. Do not name one space “best” for every operation.]</CONFLICTING_EVIDENCE>`

##### Measurable thresholds

**(High Confidence)** In a two-stage six-class map experiment with **211 online and 32 laboratory participants**, \(\Delta E_{00}=10\) produced over **95% accuracy**, while \(\Delta E_{00}=2\) produced under **80% accuracy**. The authors called 10 a safe distance within that study but explicitly noted its restricted colours, number of classes and tasks. [doi.org](https://doi.org/10.1080/23729333.2015.1055643) ([tandfonline.com](https://www.tandfonline.com/doi/full/10.1080/23729333.2015.1055643?utm_source=openai))

**(High Confidence)** Colour difference increases as mark size decreases; points are generally more sensitive than elongated bars and lines. A single palette-level distance threshold therefore cannot guarantee equal discrimination across mark types. [danielleszafir.com](https://www.danielleszafir.com/colordiff_vis2017.pdf) ([unc-visualab.org](https://unc-visualab.org/papers/colordiff_vis2017.pdf?utm_source=openai))

**Recommended policy:**

| Check | Threshold | Status | Epistemic basis |
|---|---:|---|---|
| Meaningful graphic vs adjacent background | Contrast ratio ≥ 3:1, unrounded | Hard fail | WCAG 2.2 |
| Ordinary text vs background | ≥ 4.5:1 | Hard fail | WCAG 2.2 |
| Large text vs background | ≥ 3:1 | Hard fail | WCAG 2.2 |
| Discrete palette, normal-vision audit | Minimum pairwise \(\Delta E_{00} \ge 10\) | Hard default; override requires review | Scoped six-class map evidence |
| Discrete palette, \(\Delta E_{00}<2\) | Fail | Hard fail | Consistently poor performance in cited study |
| Sequential discrete classes | Adjacent \(\Delta E_{00}\ge10\), monotonic CAM16 \(J'\) or OKLab \(L\) | Hard default | Distance threshold is scoped; monotonicity is a design invariant |
| Continuous sequential ramp | Sample 256 positions; no lightness sign reversal exceeding numerical epsilon | Hard fail | Engineering invariant, not a published 256-sample threshold |
| Diverging ramp | Declared midpoint; each arm monotonic away from it | Hard fail | Semantic and perceptual invariant |
| CVD | Machado simulation at full protan, deutan and tritan severity, plus redundant non-colour encoding | Hard fail if colour alone carries meaning | Validated simulation model plus WCAG colour redundancy |

WCAG’s contrast thresholds and no-rounding rule are normative for WCAG conformance. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast)[w3.org](https://www.w3.org/TR/WCAG22/) ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast?utm_source=openai))

Machado, Oliveira and Fernandes provide a physiologically based model covering normal trichromacy, anomalous trichromacy and dichromacy, with validation involving colour-vision-deficient and normal-vision participants. [doi.org](https://doi.org/10.1109/TVCG.2009.113) ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/19834201/?utm_source=openai))

`<INSUFFICIENT_EVIDENCE>[No corroborated peer-reviewed evidence establishes a universal ΔE00 threshold that guarantees categorical separation under real or simulated protan, deutan and tritan vision across chart types, mark sizes, backgrounds and displays.]</INSUFFICIENT_EVIDENCE>`

`<INFERENCE from="ΔE00=10 scoped normal-vision evidence; Machado CVD simulation; WCAG prohibition on colour-only meaning">As a conservative project policy, require minimum pairwise ΔE00≥10 after each full-severity CVD simulation where feasible, but label this as an engineering threshold rather than a WCAG or universal psychophysical requirement. Redundant encoding remains mandatory even when the threshold passes.</INFERENCE>`

**(High Confidence)** Recent real-user work reinforces that simulations are insufficient as the sole validation method: CVD participants depend on structural cues, redundancy and layout scaffolding when hue is unreliable. [doi.org](https://doi.org/10.1109/TVCG.2025.3634261) ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/41289094/?utm_source=openai))

---

#### 1.3 Accessibility requirements for SVG/HTML charts and diagrams

##### Normative minimums

| Requirement | Skill rule | Automated? | Confidence |
|---|---|---:|---|
| WCAG 1.1.1 Non-text Content | Every meaningful chart/diagram has an equivalent text alternative | Partly | High |
| WCAG 1.4.1 Use of Color | Colour is never the only visual discriminator | Mostly | High |
| WCAG 1.4.3 Contrast Minimum | Text meets 4.5:1 or 3:1 for large text | Yes | High |
| WCAG 1.4.11 Non-text Contrast | Required graphical objects meet 3:1 against adjacent colours | Mostly | High |
| WCAG 2.1.1 Keyboard | Every interaction works without a pointer | Partly | High |
| WCAG 2.4.7 Focus Visible | Every focusable chart control has a visible focus state | Mostly | High |
| WCAG 2.5.8 Target Size Minimum | Interactive targets meet 24×24 CSS px or a documented exception | Yes | High |
| WCAG 4.1.2 Name, Role, Value | Custom controls expose accessible names, roles, values and state changes | Mostly | High |

WCAG 2.2 defines the above success criteria; target-size exceptions must be evaluated rather than ignored. [w3.org](https://www.w3.org/TR/WCAG22/)[w3.org](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)[w3.org](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value) ([w3.org](https://www.w3.org/TR/WCAG22/?utm_source=openai))

##### Static SVG pattern

```html
<figure aria-labelledby="fig-cap">
  <svg
    role="img"
    aria-labelledby="chart-title chart-desc"
    viewBox="0 0 800 500">
    <title id="chart-title">
      Quarterly revenue by product, 2024–2026
    </title>
    <desc id="chart-desc">
      Grouped bar chart. Product A rises from 14 to 23 million dollars;
      Product B remains between 9 and 11 million. Full values follow.
    </desc>

    <!-- rendered chart -->
  </svg>

  <figcaption id="fig-cap">
    Quarterly revenue by product. <a href="#chart-data">View data table</a>.
  </figcaption>
</figure>

<table id="chart-data">
  <caption>Quarterly revenue used in the chart, USD millions</caption>
  <!-- accessible headers and exact encoded values -->
</table>
```

**(High Confidence)** WAI guidance treats charts, flowcharts, organisation charts and other diagrams as complex images requiring a short description plus a long textual representation of essential information. Where practical, actual chart data should be provided in a table. [w3.org](https://www.w3.org/WAI/tutorials/images/complex/)[w3.org](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) ([w3.org](https://www.w3.org/WAI/tutorials/images/complex/?utm_source=openai))

**(High Confidence)** An SVG with an explicit image role must have a non-empty accessible name. W3C’s ACT rule notes inconsistent support for `<title>` and `<desc>` alone and recommends an explicit ARIA role and accessible name for non-decorative SVG. [w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/7d6734) ([w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/7d6734?utm_source=openai))

##### Alt-text and long-description content rules

A chart alternative must include:

1. chart type, subject and population;
2. purpose or central takeaway;
3. axes, units, scale type and relevant range;
4. major trends, extrema, outliers and exceptions;
5. uncertainty or missing-data treatment;
6. a route to exact data.

A technical diagram alternative must include:

1. diagram purpose;
2. principal components and groups;
3. reading or flow direction;
4. typed relationships or arrows;
5. loops, exceptions and boundary crossings;
6. any state or deployment distinction communicated visually.

`<INFERENCE from="WCAG equivalent-purpose requirement and WAI complex-image guidance">A generated alt description should be verified against the same source-data and graph representation as the visual; a fluent description generated only from the rendered image can repeat visual omissions or hallucinate relationships.</INFERENCE>`

##### Interactive charts

**(Medium Confidence)** Do not make every SVG mark an independent `Tab` stop in a dense chart. Rich-access systems such as Olli render a chart as an accessible ARIA tree, while Data Navigator separates the navigation structure from the SVG, raster or canvas renderer. [vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/olli/)[dig.cmu.edu](https://dig.cmu.edu/data-navigator/) ([vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/olli/?utm_source=openai))

Recommended pattern:

- `Tab` enters or leaves the visualisation as one region.
- Arrow keys navigate values, series or hierarchy through a roving-focus tree/grid.
- Search, summary and “view data” are available without traversing every point.
- Hover tooltips are also available on keyboard focus.
- Filtering changes update the semantic view and data table.
- State changes are exposed programmatically; use a restrained live region for consequential updates.
- The visual SVG may be `aria-hidden="true"` if a complete, synchronised semantic navigation layer is supplied.

`<INSUFFICIENT_EVIDENCE>[No universal empirical threshold defines how many marks may be exposed as individual screen-reader objects before navigation becomes unusable. Use task testing rather than a fabricated mark-count limit.]</INSUFFICIENT_EVIDENCE>`

---

#### 1.4 Automated quality checks and verifiable linting

**(High Confidence)** Draco demonstrates that visualisation guidance can be represented as hard and weighted soft constraints. VizLinter and prior visualisation-linting work demonstrate detection and correction from declarative specifications, while VisuaLint shows that users often struggle to identify construction errors unaided. [dig.cmu.edu](https://dig.cmu.edu/publications/2018-draco.html)[arxiv.org](https://arxiv.org/abs/2108.10299)[vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/visualint/) ([dig.cmu.edu](https://dig.cmu.edu/publications/2018-draco.html?utm_source=openai))

##### Required verifier architecture

```text
source data / requested graph
        ↓
canonical intermediate representation
        ↓
code generation
        ↓
schema + execution validation
        ↓
SVG/HTML DOM and scene-graph extraction
        ↓
data/geometry/axis/colour/a11y checks
        ↓
headless-browser render + OCR/pixel checks
        ↓
task questions and optional blinded judge
```

The canonical representation should record at least:

```json
{
  "kind": "chart | diagram",
  "source_hash": "...",
  "task": "compare | retrieve | trend | correlate | explain-flow | ...",
  "marks": [
    {
      "id": "m1",
      "datum_ids": ["row-17"],
      "geometry": {},
      "encoding": {},
      "label_ids": []
    }
  ],
  "scales": [],
  "axes": [],
  "legends": [],
  "nodes": [],
  "edges": [],
  "interactions": [],
  "accessibility": {}
}
```

`<INFERENCE from="Draco constraint representations; VizLinter specification analysis; benchmark failures of image-only systems">Preserving source-row-to-mark provenance is the most important architectural addition for the merged skill: it makes data correctness decidable without relying on OCR or an LLM judge.</INFERENCE>`

##### Hard-rule set suitable for scripts

| Rule ID | Pass/fail condition | Severity | Confidence |
|---|---|---:|---|
| `ARTIFACT_PARSE` | SVG/XML/HTML parses; no unresolved references; renderer exits successfully | Fatal | High |
| `DATA_MARK_FIDELITY` | Every required datum or graph element maps to the intended rendered element; no extras unless declared | Fatal | High |
| `NUMERIC_LABEL_FIDELITY` | Parsed label equals source value within half a unit of the displayed least-significant digit | Fatal | High |
| `SCALE_FIDELITY` | Inverse-scaled mark positions reproduce source values within a declared one-pixel render tolerance | Fatal | Medium |
| `BAR_BASELINE` | Linear bar baseline is zero for comparison/ratio tasks | Error | High |
| `AREA_SCALING` | Area ratio, not radius/diameter ratio, matches value ratio | Error | High |
| `PIE_WHOLE` | Non-negative parts sum to the declared whole; angles sum to \(2\pi\) within floating-point tolerance | Error | High |
| `TICK_INTERVALS` | Linear ticks have constant data-space intervals within \(10^{-6}\) of axis range; irregular intervals are explicitly labelled | Error | Medium |
| `LOG_DOMAIN` | Log axis is labelled and contains only valid positive values | Fatal | High |
| `TEXT_CLIP` | No meaningful text extends outside viewport or clipping path | Error | High |
| `LABEL_COLLISION` | No unintended positive-area intersection between text bounding boxes after transforms | Error | Medium |
| `LABEL_MARK_OCCLUSION` | Text does not cover unrelated critical marks; intentional inside labels are declared | Error | Medium |
| `NODE_EDGE_COMPLETENESS` | Requested diagram-node and edge sets exactly match extracted graph | Fatal | High |
| `EDGE_NODE_CROSSING` | An edge does not pass through a non-endpoint node | Error | High |
| `ARROW_ATTACHMENT` | Directed edge terminates on its target boundary within one CSS pixel; arrowhead remains visible | Error | Medium |
| `COLOUR_CONTRAST` | WCAG contrast thresholds pass without rounding | Error | High |
| `COLOUR_REDUNDANCY` | Semantically meaningful colour has a second visible encoding | Error | High |
| `SVG_NAME` | Meaningful static SVG has role and non-empty accessible name | Error | High |
| `LONG_DESCRIPTION` | Complex chart/diagram has a synchronised long description or equivalent | Error | High |
| `KEYBOARD_OPERATION` | Every pointer operation has a keyboard route and visible focus | Fatal for interactive output | High |
| `TARGET_SIZE` | Required targets satisfy WCAG 2.5.8 or record a valid exception | Error | High |

The one-pixel, \(10^{-6}\)-range and zero-overlap tolerances above are engineering tolerances, not measured human-perception thresholds.

`<CONFIDENCE:LOW>[A universal minimum inter-label gap, maximum occlusion percentage or maximum permissible edge-crossing count cannot currently be justified empirically. Start with zero unintended overlap and calibrate warnings using the skill’s own benchmark.]</CONFIDENCE:LOW>`

##### Deceptive-encoding checks

Misviz supplies **2,604 real-world charts** annotated for 12 misleader types and **81,814 synthetic charts**; its authors found that rule-based systems and classifiers performed best on synthetic charts, whereas multimodal models were stronger on real-world charts, with the overall task remaining difficult. [arxiv.org](https://arxiv.org/abs/2508.21675) ([arxiv.org](https://arxiv.org/abs/2508.21675?utm_source=openai))

Automate at least:

- truncated bar axes;
- inverted axes without explicit direction;
- inconsistent tick intervals;
- unequal-width histogram bins treated as equal;
- shuffled temporal categories;
- dual axes used to imply direct comparison;
- 3D perspective applied to quantitative marks;
- numeric labels inconsistent with geometry;
- missing units or scale type;
- selective omission relative to supplied source data;
- colour legend categories absent from marks or vice versa.

**(Medium Confidence)** MisVisFix reported overall F1 **0.96**, compared with **0.69** for its LLM-only baseline and **0.61** for VizLinter on the comparable subset; structural issues such as truncated axes, 3D effects and dual axes scored F1 **0.98**, **0.97** and **0.96** respectively. These are single-system, benchmark-specific results and need independent replication. [arxiv.org](https://arxiv.org/abs/2508.04679) ([www3.cs.stonybrook.edu](https://www3.cs.stonybrook.edu/~mueller/papers/MisVisFix%20TVCG.pdf?utm_source=openai))

##### Exit-code contract

```text
0   PASS
2   PASS_WITH_WARNINGS
20  INVALID_OR_NON_RENDERING_ARTIFACT
21  DATA_OR_SEMANTIC_FIDELITY_FAILURE
22  GEOMETRY_LAYOUT_OR_OCCLUSION_FAILURE
23  SCALE_AXIS_OR_DECEPTIVE_ENCODING_FAILURE
24  COLOUR_OR_CONTRAST_FAILURE
25  ACCESSIBILITY_SEMANTICS_OR_ALTERNATIVE_FAILURE
26  KEYBOARD_OR_INTERACTION_FAILURE
27  REQUIRED_CONTENT_OR_DIAGRAM_GRAPH_INCOMPLETE
70  VERIFIER_INTERNAL_ERROR
```

If several categories fail, emit every finding in machine-readable JSON and return the lowest-numbered applicable hard-failure category according to the above precedence.

---

#### 1.5 Documented failure modes of LLM-generated charts and diagrams

| Failure mode | Evidence | Measurable reduction | Required defence |
|---|---|---|---|
| Non-executable code, missing imports, invalid syntax or API use | Plot2Code, ChartMimic and DiagramGenBenchmark use code-pass/Pass@1 because execution failure remains common | DiagramAgent compiler loop: +15.56 Pass@1 points for diagram-to-code relative to ablation | Execute in sandbox; return compiler/runtime trace to generator |
| Wrong or omitted labels, legends and values | Plot2Code reports difficulty on text-dense plots; DiagramAgent identifies content-understanding errors | Structured source-data and OCR/DOM diff | Require exact label/value ledger |
| Correct-looking but data-wrong chart | Image metrics do not directly test source-to-mark mapping | Provenance and inverse-scale validation | No visual score may override data failure |
| Wrong chart type or encoding | Benchmarks show cross-modal reasoning remains difficult | Task- and data-schema-constrained generation | Choose form before style/code generation |
| Label collision, clipping and hidden arrowheads | Recurrent diagram and chart-generation failure; image similarity may underweight small text | Rendered bounding-box and edge geometry verifier | Fail on unintended intersections or clipping |
| Missing diagram nodes/edges or wrong direction | Diagram benchmarks explicitly separate code, structure and image fidelity | Planner plus graph extraction and comparison | Validate requested graph exactly |
| Inaccessible SVG | Generic code models omit names, alternatives and keyboard semantics unless constrained | Fixed accessible templates and accessibility linting | Accessibility wrapper generated outside free-form model output |
| Misleading scale or axis | VLMs perform poorly on critical-visualisation-literacy tests | Deterministic axis metadata checks | Rule system has authority over model judgement |
| Inconsistent self-review | General VLM critiques can be incorrect or contradictory | Deterministic checks first; visual critic only on residual issues | Require judge agreement across randomised presentations |

Plot2Code contains **132 plots across six types** and evaluated **14 multimodal models**, using code pass rate, text-match ratio and GPT-4V visual rating. It found substantial difficulty with text-dense plots and reliance on textual instructions. [arxiv.org](https://arxiv.org/abs/2405.07990) ([arxiv.org](https://arxiv.org/abs/2405.07990?utm_source=openai))

ChartMimic contains **4,800 human-curated chart/instruction/code triplets**, covering 18 regular and four advanced chart types and **201 subcategories**. [github.com](https://github.com/chartmimic/chartmimic)[proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2025/hash/42806406dd99e30c3796bc98b2670fa2-Abstract-Conference.html) ([github.com](https://github.com/chartmimic/chartmimic?utm_source=openai))

DiagramAgent reported generation Pass@1 **58.15**, compared with **49.81** for GPT-4o and **55.56** for a 33B DeepSeek-Coder model. For diagram-to-code, removing GPT-4o verification reduced Pass@1 by **6.30 points**, removing compiler debugging reduced it by **15.56 points**, and removing both reduced it by **16.30 points**. [openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/html/Wei_From_Words_to_Structured_Visuals_A_Benchmark_and_Framework_for_CVPR_2025_paper.html)[openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Wei_From_Words_to_CVPR_2025_supplemental.pdf) ([chengtan9907.github.io](https://chengtan9907.github.io/assets/publications/cvpr25_diagram.pdf?utm_source=openai))

**(Medium Confidence)** Structured reinforcement learning reported a **6.2% improvement** in high-level ChartMimic metrics over its comparison point, indicating that rewards combining execution and structured visual feedback are a productive direction. [proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b95c7e24501f5d1dddbc5e8526cda7ae-Abstract-Conference.html) ([proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b95c7e24501f5d1dddbc5e8526cda7ae-Abstract-Conference.html?utm_source=openai))

##### Operational model/tool comparison

| System or layer | Parameter Count | Context Window | Reported latency | Cost | License | Relevant evidence |
|---|---:|---:|---:|---|---|---|
| DiagramAgent core | 7B | `<MISSING_DATA>[Not reported in the cited benchmark]</MISSING_DATA>` | `<MISSING_DATA>[No end-to-end latency reported]</MISSING_DATA>` | Local inference cost depends on hardware | Repository licence not verified at synthesis time | Strong ablation evidence for compiler and verifier modules |
| GPT-4o verification in DiagramAgent | Undisclosed | Not reported for experiment | Not reported | Proprietary API cost; experiment cost not reported | Proprietary service | Improved Pass@1 and image-fidelity metrics |
| VizLinter | N/A: rule/constraint system | N/A | Not reported | Open research prototype | Rules repository is BSD-3-Clause | Detects and proposes fixes from Vega-Lite specifications |
| Draco | N/A: answer-set constraint system | N/A | Not reported | Open-source research implementation | ``UNVERIFIED (unusable citation URL)`` | Formal hard/soft constraints; learned weights |
| Misviz rule-based linter | N/A | N/A | Not reported | Open research code | ``UNVERIFIED (unusable citation URL)`` | High precision for axis-metadata rules; limited rule coverage |
| General proprietary VLM judge | Undisclosed | Model-specific and mutable | Model-specific | Mutable API pricing | Proprietary | Useful for residual visual comparison, unreliable as sole correctness judge |

`<MISSING_DATA>[The primary papers generally do not report stable API schemas, rate limits, per-chart latency or per-chart monetary cost. Those properties are model-provider and deployment specific and should be benchmarked in the intended execution environment rather than copied from mutable product documentation.]</MISSING_DATA>`

##### Architecture decision

`<INFERENCE from="DiagramAgent ablations; Chart2Code and Plot2Code failure rates; Draco/VizLinter constraint systems">Use an agent pipeline of Plan → Generate → Execute → Deterministic Verify → Render → Visual Verify → Repair. Do not allow a free-form model to choose whether deterministic findings matter, and do not ask the same model to generate and finally certify its own output.</INFERENCE>`

---

#### 1.6 How visualisation quality is evaluated

##### Published benchmarks and their coverage

| Benchmark | Scale | Evaluates | Metrics | Main limitation |
|---|---:|---|---|---|
| Plot2Code | 132 plots, six types, 14 models | Scientific-plot-to-code | Code pass, text match, GPT-4V rating | Small curated set; visual judge dependence |
| ChartMimic | 4,800 triplets, 22 broad types, 201 subcategories | Chart-to-code | Multi-level code and rendered-chart metrics | Primarily reproduction, not end-user comprehension |
| Chart2Code | 2,023 tasks, 22 chart types, three levels | Reproduction, editing, long-table generation | Code correctness and chart quality | 2025 preprint; judge calibration still developing |
| DiagramGenBenchmark | Eight diagram categories | Text-to-diagram generation and editing | Pass@1, code similarity and image metrics | Image metrics can miss semantic graph errors |
| DiagramEval | Diagram-as-graph evaluation | Node and path alignment | Structural node/path metrics | Research-diagram scope; not yet a complete aesthetic/accessibility metric |
| Misviz/Misviz-synth | 2,604 real and 81,814 synthetic charts; 12 misleaders | Misleading-chart detection | F1, exact match, category detection | Synthetic-to-real generalisation gap |
| VLAT | 53 items, 12 visualisation types | Basic visualisation literacy | Multiple-choice accuracy | Long; targets people rather than generated artefacts |
| CALVI | 45 items | Critical reasoning about misleading visualisations | Item-response-theory assessment | Does not directly measure code/render quality |
| Mini-VLAT | 12 items | Short literacy screening | Reliability and validity measures | Less complete chart-type coverage |

Chart2Code reports that GPT-5 averaged **0.57** on code evaluation and **0.22** on chart-quality assessment across editing tasks. [arxiv.org](https://arxiv.org/abs/2510.17932) ([arxiv.org](https://arxiv.org/abs/2510.17932?utm_source=openai))

DiagramEval represents diagrams as graphs and measures node and path alignment, directly addressing failures that raster similarity may not localise or explain. [aclanthology.org](https://aclanthology.org/2025.emnlp-main.640.pdf) ([arxiv.org](https://arxiv.org/abs/2510.25761?utm_source=openai))

Mini-VLAT is a **12-item** form of the **53-item** VLAT; it reported coefficient omega **0.72** and validation by five experts with average content-validity ratio **0.6**. [arxiv.org](https://arxiv.org/abs/2304.07905) ([arxiv.org](https://arxiv.org/abs/2304.07905?utm_source=openai))

Adaptive A-VLAT and A-CALVI use **27 and 15 items** respectively and reported test-retest ICC values of **0.98** for both instruments. [arxiv.org](https://arxiv.org/abs/2308.14147) ([arxiv.org](https://arxiv.org/abs/2308.14147?utm_source=openai))

##### Recommended quality protocol

**Gate 1 — deterministic correctness**

Pass only if:

- artifact executes and renders;
- all data and graph semantics match;
- no fatal geometry failures;
- all scale and axis equations pass;
- WCAG-computable requirements pass;
- required alternatives and keyboard operations exist.

**Gate 2 — task correctness**

Create task questions from the source data or requested graph:

- exact value retrieval;
- maximum/minimum identification;
- pairwise comparison;
- trend direction;
- outlier identification;
- path tracing;
- upstream/downstream dependency;
- component count and group membership.

`<INFERENCE from="Task-based graphical-perception studies and the fact that ground-truth answers are known">Generated artefacts should achieve 100% accuracy on machine-answerable factual task probes. Any wrong answer identifies a semantic or rendering defect, not an acceptable aesthetic trade-off.</INFERENCE>`

**Gate 3 — comprehension study**

Measure:

- answer accuracy;
- completion time;
- confidence calibration;
- error type;
- accessibility-mode parity;
- subjective workload only as a secondary measure.

Accuracy and completion time are standard measures of effectiveness and efficiency in task-based visualisation studies. [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8059811/) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC8059811/?utm_source=openai))

**Gate 4 — residual visual-quality rubric**

Suggested rubric after all hard gates pass:

| Dimension | Weight | Judge question |
|---|---:|---|
| Data/semantic fidelity | 35 | Does the visual communicate exactly the supplied data or graph? |
| Task effectiveness | 20 | Can the intended task be completed quickly and correctly? |
| Legibility/layout | 15 | Are labels, marks, edges and hierarchy readable without collision? |
| Encoding appropriateness | 10 | Are visual channels appropriate for the task and data type? |
| Accessibility | 15 | Are visual, keyboard and non-visual alternatives complete? |
| Aesthetic coherence | 5 | Is styling consistent and free of distracting decoration? |

`<CONFIDENCE:LOW>[The proposed weights and an 85/100 quality threshold are project-governance values, not empirically universal constants. Use 85/100 only after hard gates pass, then calibrate against human pairwise judgements on the 39 supported types.]</CONFIDENCE:LOW>`

##### Model-judge protocol

1. Give the judge the rendered output, source data/graph and declared task.
2. Ask factual questions separately from style judgements.
3. Use blinded pairwise comparison against a reference or previous version.
4. Randomise left/right order and repeat.
5. Require agreement across both orders; disagreement routes to human review.
6. Never let a visual-similarity score override a deterministic data or accessibility failure.
7. Record model, prompt, temperature, date and raw response.

**(Medium Confidence)** Current VLMs should not certify misleadingness unaided. One standardised evaluation reported a maximum of only **30.0% accuracy on CALVI**, despite stronger basic VLAT performance, indicating a substantial gap between reading ordinary charts and detecting deceptive ones. [arxiv.org](https://arxiv.org/abs/2503.16632) ([visualdata.wustl.edu](https://visualdata.wustl.edu/assets/pdf/pandey2025benchmarking.pdf?utm_source=openai))

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** As of **August 30, 2026**, the evidence is mature enough to establish hard rules for common-scale encodings, area geometry, colour semantics, WCAG contrast, accessible naming, keyboard operation and source-to-mark fidelity. It is not mature enough to establish universal numeric thresholds for label spacing, clutter, CVD palette separation or overall aesthetic quality.

The strongest evidence hierarchy is:

1. **W3C Recommendations and ACT rules** for accessibility requirements.
2. **Replicated graphical-perception experiments** for position, length/angle and area.
3. **Task-conditioned experiments** for chart selection and axis truncation.
4. **Peer-reviewed colour-discrimination studies**, carefully scoped to marks and study conditions.
5. **Constraint/linter systems** demonstrating automatable implementation.
6. **Recent open benchmarks** for LLM chart and diagram generation.
7. **Model-judge and image-similarity metrics**, which are useful but least authoritative for semantic correctness.

**(High Confidence)** The correct build-vs-buy decision is to **build the canonical representation, provenance ledger and deterministic verifier**, while reusing standards-compliant browsers, colour libraries, accessibility engines and existing chart grammars. A black-box commercial VLM should not be the primary verifier because model behaviour, cost, latency and critical-chart reasoning remain unstable.

**(Medium Confidence)** Existing systems are reference architectures rather than drop-in production solutions:

- Draco is the strongest precedent for explicit hard and soft constraints.
- VizLinter is the strongest precedent for lint-plus-fix over declarative charts.
- Olli and Data Navigator are the strongest precedents for renderer-independent accessible navigation.
- Misviz is the strongest current open misleading-chart detection corpus.
- ChartMimic, Chart2Code and DiagramGenBenchmark are the strongest relevant code-generation benchmarks.

All integrated sources are W3C publications, peer-reviewed literature, official conference proceedings, official research repositories or primary benchmark papers. SEO aggregators and promotional comparison pages were discarded.

---

### 3. What are the contrasting viewpoints or competing evidence?

| Issue | Position A | Position B | Resolution for the skill |
|---|---|---|---|
| Universal perceptual ranking | Position is better than length/angle, which is better than area | Task and distribution can change relative chart effectiveness | Keep the channel ranking as a default prior, then condition on task |
| Bar axes must start at zero | Truncation persistently exaggerates perceived differences | Truncation may improve retrieval/filtering and direct labels mitigate harm | Fail truncation for comparison tasks; allow reviewed exceptions for retrieval tasks |
| One colour-distance threshold | \(\Delta E_{00}=10\) was safe in a six-class map study | Mark size, palette, display, CVD and context change discrimination | Use 10 as a conservative scoped default, never as a universal guarantee |
| Best perceptual colour space | CAM16-UCS performs strongly on broad colour-difference datasets | OKLab is simpler and CSS-native; CIEDE2000 has more direct threshold precedent | CAM16-UCS for optimisation, OKLab for CSS interpolation, CIEDE2000 for audits |
| A data table is enough | Tables provide exact values and broad compatibility | Tables are inefficient for patterns, trends and hierarchy; rich navigation improves access | Supply summary + table + structured navigation for complex interactive charts |
| Image similarity measures quality | SSIM, LPIPS and CLIP support scalable evaluation | They can score a semantically wrong chart highly | Use only after data and graph fidelity pass |
| LLM visual critic vs rules | VLMs can recognise contextual and visual defects missed by fixed rules | VLMs remain inconsistent and poor on misleading-chart reasoning | Rules are authoritative; VLM critique is advisory |
| Automatic fixing | Fixers can rapidly repair conventional violations | Context-free fixes may change communicative intent | Auto-fix only mathematically or normatively unambiguous violations |

`<CONFLICTING_EVIDENCE>[Axis truncation is not categorically harmful across every task, but its benefit in value retrieval does not negate its documented distortion of ratio and magnitude judgements.]</CONFLICTING_EVIDENCE>` [arxiv.org](https://arxiv.org/abs/1907.02035)[doi.org](https://doi.org/10.1145/3772318.3790617) ([arxiv.org](https://arxiv.org/abs/1907.02035?utm_source=openai))

`<CONFLICTING_EVIDENCE>[Simple colour-distance thresholds are operationally useful, but Szafir’s size-sensitive findings and recent real-CVD research show that a palette may satisfy a numerical metric and still fail in small marks or structurally weak charts.]</CONFLICTING_EVIDENCE>` [danielleszafir.com](https://www.danielleszafir.com/colordiff_vis2017.pdf)[doi.org](https://doi.org/10.1109/TVCG.2025.3634261) ([danielleszafir.com](https://www.danielleszafir.com/colordiff_vis2017.pdf?utm_source=openai))

---

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** From 2020 onward, visualisation quality assurance moved from informal guidelines toward explicit lints, constraints and repair systems. VisuaLint, VizLinter and Draco establish the technical pattern now suitable for a SKILL.md verifier: machine-readable rules, localised findings and constrained fixes. [vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/visualint/)[arxiv.org](https://arxiv.org/abs/2108.10299)[dig.cmu.edu](https://dig.cmu.edu/publications/2018-draco.html) ([vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/visualint/?utm_source=openai))

**(High Confidence)** Accessibility research moved beyond static alt text toward navigable semantic structures, exemplified by Olli and Data Navigator. The likely trajectory is renderer-independent semantic mirrors over SVG, canvas and raster outputs rather than assuming raw SVG child semantics provide a usable experience. [vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/olli/)[arxiv.org](https://arxiv.org/abs/2308.08475) ([vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/olli/?utm_source=openai))

**(Medium Confidence)** From 2024–2026, chart-to-code evaluation expanded from small plot-reproduction sets to thousands of real-world, editing and long-table tasks. Results continue to show a large gap between executable code and high-quality, data-faithful visualisation. [arxiv.org](https://arxiv.org/abs/2405.07990)[github.com](https://github.com/chartmimic/chartmimic)[arxiv.org](https://arxiv.org/abs/2510.17932) ([arxiv.org](https://arxiv.org/abs/2405.07990?utm_source=openai))

**(Medium Confidence)** Diagram evaluation is shifting from raster similarity toward structural graph metrics. DiagramEval’s node/path alignment is directly relevant to architecture, flow, network and process diagrams, where one missing or reversed edge is more important than small styling differences. [aclanthology.org](https://aclanthology.org/2025.emnlp-main.640.pdf) ([aclanthology.org](https://aclanthology.org/2025.emnlp-main.640.pdf?utm_source=openai))

**(Medium Confidence)** The generation trajectory favours verifier-guided agents rather than single-pass prompting. Compiler feedback, structured rewards and visual verification all show measurable improvements, but the evidence also indicates diminishing returns unless the verifier checks semantics rather than only visual resemblance. [openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Wei_From_Words_to_CVPR_2025_supplemental.pdf)[proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b95c7e24501f5d1dddbc5e8526cda7ae-Abstract-Conference.html) ([openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Wei_From_Words_to_CVPR_2025_supplemental.pdf?utm_source=openai))

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| **[High]** Position on a common scale is the strongest default quantitative channel; area and volume are weaker. [doi.org](https://doi.org/10.1080/01621459.1984.10478080) | Cleveland & McGill, *Graphical Perception* | 1984 | Peer-reviewed foundational experiment; primary source | https://doi.org/10.1080/01621459.1984.10478080 |
| **[High]** Crowdsourced replication broadly confirmed position over angle/area, but not a strict angle-vs-length difference. [doi.org](https://doi.org/10.1145/1753326.1753357) | Heer & Bostock | 2010 | Peer-reviewed replication experiment | https://doi.org/10.1145/1753326.1753357 |
| **[High]** Stacked and spatially separated bars impair comparison relative to aligned/adjacent bars. [doi.org](https://doi.org/10.1109/TVCG.2014.2346320) | Talbot, Setlur & Anand | 2014 | Peer-reviewed four-experiment study | https://doi.org/10.1109/TVCG.2014.2346320 |
| **[High]** Encoding effectiveness varies with task and data distribution in a 1,920-person study. [doi.org](https://doi.org/10.1111/cgf.13409) | Kim & Heer | 2018 | Peer-reviewed crowdsourced experiment | https://doi.org/10.1111/cgf.13409 |
| **[High]** Basic chart effectiveness varies across ten tasks and five chart forms. [doi.org](https://doi.org/10.1109/TVCG.2018.2829750) | Saket, Endert & Demiralp | 2018 | Peer-reviewed task experiment | https://doi.org/10.1109/TVCG.2018.2829750 |
| **[High]** Truncated bar axes persistently exaggerate perceived differences. [arxiv.org](https://arxiv.org/abs/1907.02035) | Correll, Moritz & Heer | 2019 | Primary multi-study empirical paper | https://arxiv.org/abs/1907.02035 |
| **[High]** Truncation effects are task-dependent, and direct labels mitigate some harm. [doi.org](https://doi.org/10.1145/3772318.3790617) | *Taking Truncation to Task* | 2026 | Peer-reviewed CHI experiment | https://doi.org/10.1145/3772318.3790617 |
| **[High]** Sequential, diverging and qualitative scales have different semantic uses. [colorbrewer2.org](https://colorbrewer2.org/learnmore/schemes.html) | Brewer/ColorBrewer | Current | Authoritative primary design resource | https://colorbrewer2.org/learnmore/schemes.html |
| **[High, scoped]** \(\Delta E_{00}=10\) exceeded 95% accuracy and 2 fell below 80% in a six-class map study. [doi.org](https://doi.org/10.1080/23729333.2015.1055643) | Brychtová & Çöltekin | 2015 | Peer-reviewed web and eye-tracking experiment | https://doi.org/10.1080/23729333.2015.1055643 |
| **[High]** Colour discriminability depends on mark size and shape. [danielleszafir.com](https://www.danielleszafir.com/colordiff_vis2017.pdf) | Szafir | 2018 | Peer-reviewed visualisation perception experiments | https://www.danielleszafir.com/colordiff_vis2017.pdf |
| **[High]** Machado supplies a validated physiological CVD simulation model. [doi.org](https://doi.org/10.1109/TVCG.2009.113) | Machado, Oliveira & Fernandes | 2009 | Peer-reviewed model plus experimental validation | https://doi.org/10.1109/TVCG.2009.113 |
| **[Medium-High]** CAM16-UCS is a stronger general colour-difference space than older alternatives in broad dataset comparisons. [doi.org](https://doi.org/10.1002/col.22844) | Luo et al. | 2023 | Peer-reviewed comparative colour-science study | https://doi.org/10.1002/col.22844 |
| **[Medium]** OKLab is standardised for CSS and improves perceptual interpolation/hue behaviour over CIELAB in documented regions. [w3.org](https://www.w3.org/TR/css-color-4/) | W3C CSS Color 4 | 2026 draft | Authoritative web specification | https://www.w3.org/TR/css-color-4/ |
| **[High]** WCAG requires 3:1 non-text contrast and prohibits colour-only meaning. [w3.org](https://www.w3.org/TR/WCAG22/) | W3C WCAG 2.2 | 2023 | W3C Recommendation; authoritative standard | https://www.w3.org/TR/WCAG22/ |
| **[High]** Complex charts and diagrams need short and long textual alternatives. [w3.org](https://www.w3.org/WAI/tutorials/images/complex/) | W3C WAI Complex Images | Updated 2026 | Authoritative implementation guidance | https://www.w3.org/WAI/tutorials/images/complex/ |
| **[High]** Explicitly-role-bearing SVG needs a non-empty accessible name; `<title>`/`<desc>` support alone is inconsistent. [w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/7d6734) | W3C ACT Rule 7d6734 | 2023 | W3C accessibility conformance test rule | https://www.w3.org/WAI/standards-guidelines/act/rules/7d6734 |
| **[Medium-High]** Olli exposes visualisations through an accessible ARIA tree. [vis.csail.mit.edu](https://vis.csail.mit.edu/pubs/olli/) | Blanco, Zong & Satyanarayan | 2022 | IEEE VIS research system and source code | https://vis.csail.mit.edu/pubs/olli/ |
| **[High]** Visualisation knowledge can be expressed as executable hard and soft constraints. [dig.cmu.edu](https://dig.cmu.edu/publications/2018-draco.html) | Moritz et al., Draco | 2018 | Peer-reviewed system and open implementation | https://dig.cmu.edu/publications/2018-draco.html |
| **[Medium-High]** VizLinter demonstrates linting and automatic fixes over declarative chart specifications. [arxiv.org](https://arxiv.org/abs/2108.10299) | Chen et al. | 2021 | Primary system paper and user study | https://arxiv.org/abs/2108.10299 |
| **[High]** Readers have substantial difficulty identifying chart-construction errors unaided. [doi.org](https://doi.org/10.1111/cgf.13975) | Hopkins, Correll & Satyanarayan | 2020 | Peer-reviewed N=62 experiment | https://doi.org/10.1111/cgf.13975 |
| **[Medium-High]** Misviz provides 2,604 real and 81,814 synthetic charts covering 12 misleading-design categories. [arxiv.org](https://arxiv.org/abs/2508.21675) | Tonglet et al. | 2025/2026 | ACL 2026 benchmark paper and open code | https://arxiv.org/abs/2508.21675 |
| **[Medium]** Plot2Code documents execution, text and visual-fidelity failures on scientific plot-to-code tasks. [arxiv.org](https://arxiv.org/abs/2405.07990) | Wu et al. | 2024/2025 | NAACL Findings benchmark | https://arxiv.org/abs/2405.07990 |
| **[Medium-High]** ChartMimic contains 4,800 real scientific-chart triplets and multi-level evaluation. [proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2025/hash/42806406dd99e30c3796bc98b2670fa2-Abstract-Conference.html) | Yang et al. | 2025 | Peer-reviewed ICLR benchmark and repository | https://proceedings.iclr.cc/paper_files/paper/2025/hash/42806406dd99e30c3796bc98b2670fa2-Abstract-Conference.html |
| **[Medium]** Chart2Code shows a large gap between code success and chart quality on editing and long-table tasks. [arxiv.org](https://arxiv.org/abs/2510.17932) | Tang et al. | 2025 | Primary preprint benchmark; not yet broadly replicated | https://arxiv.org/abs/2510.17932 |
| **[Medium-High]** Compiler and visual-verification modules materially improve diagram-code generation. [openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/html/Wei_From_Words_to_Structured_Visuals_A_Benchmark_and_Framework_for_CVPR_2025_paper.html) | Wei et al., DiagramAgent | 2025 | Peer-reviewed CVPR paper with ablations | https://openaccess.thecvf.com/content/CVPR2025/html/Wei_From_Words_to_Structured_Visuals_A_Benchmark_and_Framework_for_CVPR_2025_paper.html |
| **[Medium]** DiagramEval evaluates node and path alignment rather than relying only on raster similarity. [aclanthology.org](https://aclanthology.org/2025.emnlp-main.640.pdf) | Liang & You | 2025 | Peer-reviewed EMNLP metric paper | https://aclanthology.org/2025.emnlp-main.640.pdf |
| **[High]** Mini-VLAT is a validated 12-item short form of the 53-item VLAT. [arxiv.org](https://arxiv.org/abs/2304.07905) | Pandey & Ottley | 2023 | Psychometric validation study | https://arxiv.org/abs/2304.07905 |

---

## Knowledge Gaps

### Missing empirical thresholds

- `<MISSING_DATA>[A universal minimum inter-label distance or maximum tolerable overlap. Existing lint systems detect collisions, but the literature does not establish one task-independent perceptual threshold.]</MISSING_DATA>`
- `<MISSING_DATA>[A validated maximum number of categorical colours across real CVD populations, mark sizes, backgrounds and displays.]</MISSING_DATA>`
- `<MISSING_DATA>[A universal threshold for edge crossings, bend count or diagram density that predicts comprehension across the existing 39 diagram types.]</MISSING_DATA>`
- `<MISSING_DATA>[A validated overall visualisation-quality score with stable weights spanning data fidelity, comprehension, accessibility and aesthetics.]</MISSING_DATA>`

### External-validity limitations

- Colour-distance evidence is often derived from controlled patches or limited map palettes; it does not automatically transfer to tiny scatter points, thin lines or dark-mode interfaces.
- Chart-to-code benchmarks overrepresent reproduction from a reference image and underrepresent open-ended selection from raw data, accessibility and adversarially deceptive outputs.
- Diagram benchmarks remain concentrated on flowcharts, model diagrams and research illustrations rather than the full set of technical-diagram conventions.
- Synthetic misleading-chart datasets produce materially different system rankings from real-world charts.

### Accessibility interoperability

- `<MISSING_DATA>[A current browser × screen-reader interoperability matrix for generated inline SVG, including VoiceOver/Safari, NVDA/Firefox, JAWS/Chrome and mobile combinations.]</MISSING_DATA>`
- Graphics-specific ARIA semantics remain less mature than ordinary HTML widget semantics; semantic HTML mirrors are therefore safer than relying on experimental graphics roles.

### Model and operational reporting

- `<MISSING_DATA>[Stable per-artifact latency, token consumption, API schema, rate limit and monetary cost for the benchmarked proprietary models. Primary papers do not report enough detail and provider values change.]</MISSING_DATA>`
- `<INSUFFICIENT_EVIDENCE>[Single-paper F1 scores for LLM-based chart repair cannot yet establish production reliability without independent replication and out-of-distribution testing.]</INSUFFICIENT_EVIDENCE>`

---

## Recommended Next Steps

1. **Build a canonical test corpus covering all 39 existing diagram types plus the absorbed data-visualisation types.**  
   **Rationale:** Current public benchmarks do not match the skill’s complete type distribution. Each fixture should include source data or graph, intended tasks, canonical SVG/HTML, accessibility alternative and adversarial mutations such as missing edges, truncated axes, wrong labels, collisions and inaccessible colour.

2. **Implement the deterministic verifier before modifying generation prompts.**  
   **Rationale:** Source-to-mark provenance, graph equality, scale equations, contrast and geometry checks provide stable reward signals. Prompt iteration without those signals will optimise subjective appearance while allowing semantic regressions.

3. **Run a threshold-calibration study for colour and layout.**  
   **Rationale:** Test \(\Delta E_{00}\) values, CAM16-UCS distance, mark size, label spacing and collision severity with normal-vision, low-vision and real CVD participants. This is the evidence needed to replace provisional thresholds with skill-specific empirical values.

4. **Create an assistive-technology acceptance matrix and reusable semantic wrapper.**  
   **Rationale:** Validate one static `role="img"` pattern and one interactive tree/grid pattern across major browser/screen-reader pairs. Keep these wrappers outside free-form LLM generation and fail builds when the semantic and visual states diverge.

5. **Calibrate the residual judge against blinded human comparison.**  
   **Rationale:** Build a stratified set of valid-but-differently-styled and subtly-invalid artefacts. Compare model-judge decisions with human task accuracy, randomise A/B order, and retain the judge only for dimensions where agreement is adequate. Deterministic failures should remain non-overridable.

## Sources

- [Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Me...](https://faculty.washington.edu/aragon/classes/hcde511/s12/readings/cleveland84.pdf?utm_source=openai)
- [https://colorbrewer2.org/learnmore/schemes.html?utm_source=openai](https://colorbrewer2.org/learnmore/schemes.html?utm_source=openai)
- [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/?utm_source=openai)
- [Complex Images | Web Accessibility Initiative (WAI) | W3C](https://www.w3.org/WAI/tutorials/images/complex/?utm_source=openai)
- [Formalizing Visualization Design Knowledge as Constraints: Actionable and Extensible Models in Dr...](https://dig.cmu.edu/publications/2018-draco.html?utm_source=openai)
- [From Charts to Code: A Hierarchical Benchmark for Multimodal Models](https://arxiv.org/abs/2510.17932?utm_source=openai)
- [Plot2Code: A Comprehensive Benchmark for Evaluating Multi-modal Large Language Models in Code Gen...](https://arxiv.org/abs/2405.07990?utm_source=openai)
- [Cleveland 1984 | PDF | Chart | Experiment](https://www.scribd.com/document/697470806/cleveland1984?utm_source=openai)
- [Volume 37 (2018), Number 3](https://idl.cs.washington.edu/files/2018-TaskDataEffectiveness-EuroVis.pdf?utm_source=openai)
- [Four Experiments on the Perception of Bar Charts.](https://pubmed.ncbi.nlm.nih.gov/26356929/?utm_source=openai)
- [(PDF) Is this chart lying to me? Automating the detection of misleading visualizations](https://www.researchgate.net/publication/395125457_Is_this_chart_lying_to_me_Automating_the_detection_of_misleading_visualizations?utm_source=openai)
- [Taking Truncation to Task: A Task-Based Exploration of Axis Truncation in Bar Charts | Proceeding...](https://doi.org/10.1145/3772318.3790617?utm_source=openai)
- [Comprehensive color solutions: CAM16, CAT16, and CAM16‐UCS - Li - 2017 - Color Research & Applica...](https://onlinelibrary.wiley.com/doi/abs/10.1002/col.22131?utm_source=openai)
- [CSS Color Module Level 4](https://www.w3.org/TR/css-color-4/?utm_source=openai)
- [Full article: Discriminating classes of sequential and qualitative colour schemes](https://www.tandfonline.com/doi/full/10.1080/23729333.2015.1055643?utm_source=openai)
- [Modeling Color Difference for Visualization Design](https://unc-visualab.org/papers/colordiff_vis2017.pdf?utm_source=openai)
- [Understanding Success Criterion 1.4.11: Non-text Contrast | WAI | W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast?utm_source=openai)
- [A physiologically-based model for simulation of color vision deficiency.](https://pubmed.ncbi.nlm.nih.gov/19834201/?utm_source=openai)
- [The Hue-Man Factor: An Empirical Evaluation of Visualization Perception and Accessibility Across ...](https://pubmed.ncbi.nlm.nih.gov/41289094/?utm_source=openai)
- [SVG element with explicit role has non-empty accessible name | ACT Rule | WAI | W3C](https://www.w3.org/WAI/standards-guidelines/act/rules/7d6734?utm_source=openai)
- [Olli: An Extensible Visualization Library for Screen Reader Accessibility | MIT Visualization Group](https://vis.csail.mit.edu/pubs/olli/?utm_source=openai)
- [Is this chart lying to me? Automating the detection of misleading visualizations](https://arxiv.org/abs/2508.21675?utm_source=openai)
- [MisVisFix: An Interactive Dashboard for Detecting, Explaining, and Correcting Misleading Visualiz...](https://www3.cs.stonybrook.edu/~mueller/papers/MisVisFix%20TVCG.pdf?utm_source=openai)
- [GitHub - ChartMimic/ChartMimic: ICLR 2025 ChartMimic: Evaluating LMM’s Cross-Modal Reasoning Ca...](https://github.com/chartmimic/chartmimic?utm_source=openai)
- [Table 2. Main results for diagram generation (Code Agent). The best result in each metric is bolded.](https://chengtan9907.github.io/assets/publications/cvpr25_diagram.pdf?utm_source=openai)
- [Breaking the SFT Plateau: Multimodal Structured Reinforcement Learning for Chart-to-Code Generation](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b95c7e24501f5d1dddbc5e8526cda7ae-Abstract-Conference.html?utm_source=openai)
- [DiagramEval: Evaluating LLM-Generated Diagrams via Graphs](https://arxiv.org/abs/2510.25761?utm_source=openai)
- [Mini-VLAT: A Short and Effective Measure of Visualization Literacy](https://arxiv.org/abs/2304.07905?utm_source=openai)
- [Adaptive Assessment of Visualization Literacy](https://arxiv.org/abs/2308.14147?utm_source=openai)
- [A comparison of the performance on extrinsic and intrinsic cartographic visualizations through co...](https://pmc.ncbi.nlm.nih.gov/articles/PMC8059811/?utm_source=openai)
- [Benchmarking Visual Language Models on Standardized Visualization Literacy Tests](https://visualdata.wustl.edu/assets/pdf/pandey2025benchmarking.pdf?utm_source=openai)
- [Truncating the Y-Axis: Threat or Menace?](https://arxiv.org/abs/1907.02035?utm_source=openai)
- [Modeling Color Difference for Visualization Design](https://www.danielleszafir.com/colordiff_vis2017.pdf?utm_source=openai)
- [VisuaLint: Sketchy In Situ Annotations of Chart Construction Errors | MIT Visualization Group](https://vis.csail.mit.edu/pubs/visualint/?utm_source=openai)
- [DiagramEval: Evaluating LLM-Generated Diagrams via Graphs](https://aclanthology.org/2025.emnlp-main.640.pdf?utm_source=openai)
- [Ablation Study  Table 10 presents the ablation study results, which evaluate the contributions of...](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Wei_From_Words_to_CVPR_2025_supplemental.pdf?utm_source=openai)
