# Producing high-quality data visualisations and technical diagrams as code: the encodable evidence

**Date:** 2026-08-30
**Scope:** empirical findings that convert into hard rules, numeric thresholds and verifier exit codes for a merged `visualization` skill (39 diagram types + absorbed data-visualisation skill).
**Method:** primary literature retrieved and text-extracted directly (arXiv, author-hosted PDFs, W3C normative specs); vendor and aggregator material excluded except where explicitly labelled.

---

## Executive Summary

- **(High Confidence)** Colour separation has a published, size-parameterised threshold model that a linter can evaluate in closed form. Szafir's TVCG 2018 models give the ΔE needed for a 50% just-noticeable difference as a function of mark geometry: for a 6 px scatterplot point it is **8.37 ΔE on L\*, 16.11 on a\*, 19.46 on b\***, falling to 5.47 / 6.84 / 7.99 at 50 px, with elongated marks gaining 5–10 ΔE and reaching asymptote at a **2:1 length-to-thickness ratio** <cite url="https://danielleszafir.com/colordiff_vis2017.pdf">. This is the single most important finding for a verifier: *a palette is not "accessible" independently of the marks it is painted on*, and almost every generated chart applies one palette to points, bars and 1–2 px lines indiscriminately.

- **(High Confidence)** For categorical palettes there are two independent, directly-encodable threshold sets. Petroff (2021) enforces **minimum CAM02-UCS ΔE of 20 / 18 / 16 for 6 / 8 / 10-colour sets**, computed as the *minimum across deuteranomaly, protanomaly and tritanomaly at every severity 1–100* using Machado (2009) matrices applied to **linear** sRGB, plus minimum lightness distance ΔJ′ of **5.0 / 4.2 / 3.6** and lightness ranges J′ ∈ [40,80] / [40,82] / [40,84] <cite url="https://arxiv.org/pdf/2107.02270">. Colorgorical enforces a coarser noticeable-difference gate — at least one axis exceeding **ΔL = 22.747, Δa = 31.427, Δb = 44.757** — plus lightness clamped to **L\* ∈ [25, 85]** and exclusion of the disliked dark-yellow region **L ∈ [35,75], H ∈ [85°, 114°]** <cite url="https://gramaz.io/pdf/gramazio-2016-ccd.pdf">.

- **(High Confidence)** The strongest measured lever on LLM chart quality is not prompt wording but **library choice and an execution-feedback loop**. On VisEval, GPT-4's invalid rate rises from **3.29% (Matplotlib) to 25.41% (Seaborn)** — a **22.12 percentage-point** swing from the same model and prompt <cite url="https://arxiv.org/html/2407.00981v1">. On PandasPlotBench, a self-debug loop lifts GPT-4o's Plotly execution pass rate from **77.7% to 97.7%** and GPT-4o-mini's from **69.1% to 97.7%** <cite url="https://arxiv.org/pdf/2506.03930">. Both effects are larger than any reported prompt-engineering gain.

- **(High Confidence)** Alt-text generation has a counter-intuitive, measured rule. Across 3,600 ranked descriptions from **30 blind and 90 sighted readers**, blind readers rank Level 2 (statistics) and Level 3 (perceptual trends) content **most** useful and Levels 1 (encoding enumeration) and **4 (contextual/domain insight) least** useful — while sighted readers rank Levels 3 and 4 most useful <cite url="https://arxiv.org/pdf/2110.04406">. **63% (n=19) of blind readers were emphatic that descriptions must not contain the author's subjective interpretation or editorialising.** A model asked to "write good alt text" optimises for the sighted-reader preference and produces exactly the Level 4 content BLV readers rank worst.

- **(High Confidence)** The "truncate line charts freely, never truncate bars" rule is empirically false. Correll, Bertini and Franconeri found a very large effect of truncation on perceived effect size (**F(2,76) = 89, p < 0.0001**) and **no significant difference between bar and line charts (F(1,38) = 0.5, p = 0.50)**; broken-axis and gradient mitigations did not reliably debias viewers (**F(2,60) = 3.1, p = 0.05**, weak post-hoc) <cite url="https://arxiv.org/pdf/1907.02035">. A verifier should therefore flag truncation on *both* forms and must not accept an axis-break glyph as a remediation.

- **(High Confidence)** Geometry and legality checks are reliably automatable; aesthetic judgement is not. VisEval's browser-simulated **layout check (overflow / overlap) scored 100% accuracy** against three expert raters and its scale-and-ticks check **99%** (dropping to 92% when the deconstructed tick values were withheld from the model), whereas its GPT-4V readability rating reached only **SRCC 0.843** — above the **0.782** inter-expert agreement, but a rating rather than a gate <cite url="https://arxiv.org/html/2407.00981v1">. This is the clean automatable/judge boundary for the skill's verifier scripts.

- **(Medium Confidence)** LLMs used as *misleading-chart detectors* over-flag badly. Across four multimodal models, recall reached 1.00 with precision as low as 0.52–0.63; one model answered the neutral midpoint on a 5-point Likert scale in **78%** of cases, and in a later prompt returned "Misleading" for **99%** of test cases <cite url="https://arxiv.org/pdf/2407.17291">. An LLM judge must not be the sole gate on deceptive-encoding checks; deterministic rules over the CALVI misleader taxonomy should carry that load.

- **(Medium Confidence)** Encode WCAG 2.x contrast, not APCA. The WCAG 3.0 Editor's Draft of **8 April 2026** still lists the contrast test as *Exploratory* with an editor's note that "the contrast algorithm used in WCAG 3 is yet to be determined"; APCA was dropped from the July 2023 working draft under the six-month exploratory-removal rule and no replacement has been adopted <cite url="http://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html">.

---

## Detailed Findings

### 1. Graphical perception and encoding-accuracy findings that should govern chart-form selection and mark design

**The Cleveland–McGill ranking survives replication, with two documented exceptions.** Heer and Bostock replicated the 1984 position-length experiment on Mechanical Turk using the original error measure, `log2(|judged percent − true percent| + 1/8)`, summarised by midmeans, and report that "the ranking of types by accuracy is consistent between the two experiments" with position significantly outperforming length <cite url="https://www.cs.kent.edu/~javed/class-P2P12F/papers-2012/PAPER2012-2010-MTurk-CHI.pdf">. Two results do *not* match theory. First, angle did not perform worse than length: "Theory also suggests that angle should perform worse than length, but the results do not support this" — and the authors note Cleveland and McGill also failed to find that ordering <cite url="https://www.cs.kent.edu/~javed/class-P2P12F/papers-2012/PAPER2012-2010-MTurk-CHI.pdf">. Second, and directly useful for treemap and packed-layout generation, **aspect ratio 1:1 produced the *worst* area-comparison accuracy** (p < 0.05), robust across both plain-rectangle and treemap conditions, consistent with viewers using 1D side-length as a proxy for area — which maximises error at squares <cite url="https://www.cs.kent.edu/~javed/class-P2P12F/papers-2012/PAPER2012-2010-MTurk-CHI.pdf">. There was no significant difference between the rectangle and treemap display conditions, so treemap chrome does not itself interfere with judgement.

<INFERENCE from="Heer & Bostock's 1:1-aspect-ratio finding; their finding that rectangle and treemap conditions did not differ">A treemap linter should *not* target squarified-optimal 1:1 tiles as a quality goal. The layout property that a squarified algorithm is normally praised for is the one that measured worst. A defensible encodable rule is to flag tiles whose aspect ratio falls within a narrow band around 1.0 when the task is area comparison, rather than flagging tiles far from 1.0.</INFERENCE>

**Effectiveness is task-conditional, which means a single static chart-type ranking is not encodable as a hard rule.** Saket, Endert and Demiralp ran five chart types (Table, Line, Bar, Scatterplot, Pie) across ten Amar-style low-level tasks on two datasets at 5–34 data points, and found "the effectiveness of these visualization types significantly varies across task"; scatterplot was among the best for the majority of tasks, and the authors trained a decision tree over the collected data to drive a recommender <cite url="https://arxiv.org/pdf/1709.08546">. They also report that "perceived accuracy does not always match with task accuracy" — user preference and measured performance diverge <cite url="https://arxiv.org/pdf/1709.08546">.

<CONFLICTING_EVIDENCE>Pie charts. The Cleveland–McGill effectiveness ranking, embedded structurally in APT and inherited by most modern recommenders, places angle/area encodings well below position and length, and is the basis of the common "never use a pie chart" rule. Against this: Saket et al. found pie charts effective for particular tasks and note prior work (Eells; Simkin & Hastie; Spence et al.) in which pie charts were as fast as or more accurate than divided bar charts for proportional comparison, and in which divided bars degrade as component count rises while pies do not <cite url="https://arxiv.org/pdf/1709.08546">. Heer & Bostock separately failed to reproduce the predicted angle-worse-than-length ordering <cite url="https://www.cs.kent.edu/~javed/class-P2P12F/papers-2012/PAPER2012-2010-MTurk-CHI.pdf">. The disagreement is about *task*, not about method: the classic ranking measures proportion-of-a-whole magnitude estimation, the pro-pie results measure part-to-whole comparison. Encode this as a task-gated warning, not a prohibition.</CONFLICTING_EVIDENCE>

**Diagram (node-link) layout has its own aesthetics hierarchy, and it is dominated by one metric.** Purchase's 1997 graph-drawing study tested five aesthetics — edge crossings, bends, symmetry, minimum angle, orthogonality — and found edge-crossing minimisation by far the largest effect on human understanding, with bends and symmetry secondary and minimum angle and orthogonality not producing significant improvements <cite url="https://espace.library.uq.edu.au/view/UQ:8ead24b" note="primary PDF was paywalled at synthesis time; findings taken from indexed abstracts and the citing literature">. <CONFIDENCE:LOW>The specific significance values and effect sizes for each aesthetic could not be verified from the primary text.</CONFIDENCE:LOW> The practically useful downstream artefact is *greadability*, whose `crossing-angle` and `angular-resolution-min` metrics McNutt and Kindlmann explicitly propose turning into lint rules by "placing thresholds on each of the metrics of interest" <cite url="https://c4pgv.dbvis.de/McNutt_Kindlmann_2018.pdf">.

<INFERENCE from="Purchase's crossing-dominance ranking; McNutt & Kindlmann's legible-graph rule proposing greadability thresholds">For the 39 diagram types, edge-crossing count is the highest-yield single deterministic metric, and it is cheap: for a rendered SVG it is a segment-intersection count over the edge paths. Bends per edge is the natural second metric. Orthogonality and minimum-angle checks should be low-severity style warnings at most, since they did not measure as comprehension-relevant.</INFERENCE>

---

### 2. Colour design for categorical, sequential and diverging scales

#### 2a. The size-dependent discriminability model (the load-bearing finding)

Standard colour-difference metrics assume large uniform patches at 2° or 10° of visual angle. Szafir measured 461 Mechanical Turk participants across three mark geometries and fitted regression models of the ΔE needed for a given proportion `p` of viewers to detect a difference <cite url="https://danielleszafir.com/colordiff_vis2017.pdf">. The composite test is:

```
ΔE(p,s) = sqrt( (ΔL / ND_L(p,s))² + (Δa / ND_a(p,s))² + (Δb / ND_b(p,s))² )
```
where a value of **1.0 means the difference is detectable by p% of viewers at mark size s** <cite url="https://danielleszafir.com/colordiff_vis2017.pdf">.

| Mark | Model | Notes |
|---|---|---|
| Point (scatter) | `ND_L = p / (0.0937 − 0.0085/diameter)`; `ND_a = p / (0.0775 − 0.0121/diameter)`; `ND_b = p / (0.0611 − 0.0096/diameter)` | R² = .90 / .97 / .90 <cite url="https://danielleszafir.com/colordiff_vis2017.pdf"> |
| Bar (elongated) | `ND_L = p / (0.1061 − 0.0107/thickness − 0.003/r)`; `ND_a = p / (0.0895 − 0.0111/thickness − 0.0037/r)`; `ND_b = p / (0.0751 − 0.0113/thickness − 0.003/r)`, `r = length/thickness` | R² = .73 / .77 / .81; gains asymptote around **r ≈ 2:1**, worth **5–10 ΔE** <cite url="https://danielleszafir.com/colordiff_vis2017.pdf"> |
| Line | `ND_L = p / (0.0742 − 0.0023/thickness)`; `ND_a = p / (0.0623 − 0.0015/thickness)`; `ND_b = p / (0.0425 − 0.0009/thickness)` | R² = .89 / .82 / .77 <cite url="https://danielleszafir.com/colordiff_vis2017.pdf"> |

Tabulated 50% JND values (ΔE), which are the numbers to hard-code if the closed form is not implemented:

| Mark and size | ND(50%) L\* | ND(50%) a\* | ND(50%) b\* |
|---|---|---|---|
| Point, 6 px (0.25°) | 8.37 | 16.11 | 19.46 |
| Point, 12 px | 6.74 | 9.98 | 13.34 |
| Point, 25 px | 5.75 | 7.81 | 10.03 |
| Point, 50 px (2°) | 5.47 | 6.84 | 7.99 |
| Line, 2 px | 15.35 | 13.92 | 19.47 |
| Line, 4 px | 8.69 | 10.28 | 15.17 |
| Line, 9 px | 6.92 | 7.79 | 11.05 |

<cite url="https://danielleszafir.com/colordiff_vis2017.pdf">

Two consequences fall straight out. First, the b\* (blue–yellow) axis is consistently the worst channel at small sizes — 19.46 ΔE for a 6 px point versus 8.37 on lightness — which is the small-field tritanopia regime. Second, **a 1 px or 2 px stroke is the worst case in the entire table**: a 2 px line needs 19.47 ΔE on b\* to reach a 50% JND, far above the separation most default palettes provide.

<INFERENCE from="Szafir's per-mark ND tables; the observation that generated charts apply one palette across mark types">The verifier rule is: take the palette, take the *smallest rendered mark dimension per series* from the SVG, and evaluate ΔE(p,s) pairwise. A palette that passes for 50 px bars can fail for the same chart's 2 px gridline-overlaid series. A single palette-level ΔE check that ignores mark size will pass charts that are measurably indiscriminable.</INFERENCE>

#### 2b. Categorical palette construction constraints

| Constraint | Value | Space | Source |
|---|---|---|---|
| Min perceptual distance, 6-colour set | ΔE′ ≥ 20 | CAM02-UCS | <cite url="https://arxiv.org/pdf/2107.02270"> |
| Min perceptual distance, 8-colour set | ΔE′ ≥ 18 | CAM02-UCS | <cite url="https://arxiv.org/pdf/2107.02270"> |
| Min perceptual distance, 10-colour set | ΔE′ ≥ 16 | CAM02-UCS | <cite url="https://arxiv.org/pdf/2107.02270"> |
| Min lightness distance (grayscale/monochromacy), 6 / 8 / 10 | ΔJ′ ≥ 5.0 / 4.2 / 3.6 | CAM02-UCS | <cite url="https://arxiv.org/pdf/2107.02270"> |
| Lightness range, 6 / 8 / 10 | J′ ∈ [40,80] / [40,82] / [40,84] | CAM02-UCS | <cite url="https://arxiv.org/pdf/2107.02270"> |
| CVD evaluation | min over deuteranomaly, protanomaly, tritanomaly at **every severity 1–100** | Machado et al. 2009 matrices on **linear** sRGB | <cite url="https://arxiv.org/pdf/2107.02270"> |
| Noticeable-difference gate (coarser) | at least one axis above ΔL=22.747, Δa=31.427, Δb=44.757 | CIELAB | <cite url="https://gramaz.io/pdf/gramazio-2016-ccd.pdf"> |
| Lightness clamp (visible on black *and* white) | L\* ∈ [25, 85] | CIELAB | <cite url="https://gramaz.io/pdf/gramazio-2016-ccd.pdf"> |
| Disliked-region exclusion (dark yellow-green) | exclude L ∈ [35,75] ∧ H ∈ [85°, 114°] | CIE LCh | <cite url="https://gramaz.io/pdf/gramazio-2016-ccd.pdf"> |
| Practical palette ceiling | ~22 colours before CIELAB space is exhausted; "inadvisable to use that many" | CIELAB | <cite url="https://gramaz.io/pdf/gramazio-2016-ccd.pdf"> |

Petroff's paper is also explicit that WCAG text-contrast ratios are the *wrong* instrument for chart marks: "While no minimum-contrast standards exist for visualizations, such standards do exist for text… but these guidelines are not a good fit for visualizations… The guidelines also define color contrast in terms of the (linear) sRGB color space, which is not perceptually uniform" — and following even the large-text ratio "eliminates the use of most lighter colors", forcing a *smaller* minimum perceptual distance, which is the opposite of the goal <cite url="https://arxiv.org/pdf/2107.02270">. This is a genuine tension for a verifier that must also satisfy WCAG 1.4.11 (see §3), and is called out as such in Knowledge Gaps.

Colorgorical additionally separates **Perceptual Distance (CIEDE2000)** from **Name Difference** — computed via Hellinger distance over Heer and Stone's colour-name model built on the XKCD survey — on the grounds that "as the difference between colors increases, perceptual distance metrics become less useful", while name difference remains discriminating at larger separations <cite url="https://gramaz.io/pdf/gramazio-2016-ccd.pdf">. The two are strong positive predictors of each other but not redundant, and pair preference is a **strong negative** predictor of both, so a "prettiest" palette and a "most discriminable" palette are genuinely in tension rather than incidentally so <cite url="https://gramaz.io/pdf/gramazio-2016-ccd.pdf">.

#### 2c. Palette *family* choice for multi-class charts (2024 evidence)

A EuroVis-track study of relative-mean judgements in multi-class scatterplots at 2–10 categories gives accuracy by palette family: **multi-hue categorical 91.44%, diverging 86.78%, perceptually-uniform sequential 86.67%, multi-hue sequential 82.56%, single-hue sequential 81.11%** <cite url="https://arxiv.org/pdf/2404.03787">. Number of categories had a significant effect (**F(8, 91) = 20.68, p < .001**) with accuracy falling as categories rose, though the categorical family degraded least <cite url="https://arxiv.org/pdf/2404.03787">.

#### 2d. Colour space selection

| Space | L RMS | C RMS | H RMS | L 95th | C 95th | H 95th |
|---|---|---|---|---|---|---|
| **Oklab** | **0.20** | **0.81** | 0.49 | **0.44** | **1.78** | 1.06 |
| CIELAB | 1.70 | 1.84 | 0.69 | 3.16 | 3.96 | 1.56 |
| CIELUV | 1.72 | 2.32 | 0.68 | 3.23 | 5.03 | 1.51 |
| OSA-UCS | 2.05 | 1.28 | 0.49 | 4.04 | 2.73 | 1.08 |
| IPT | 4.92 | 2.18 | 0.48 | 9.89 | 4.64 | 1.02 |
| JzAzBz | 2.38 | 1.79 | **0.43** | 4.55 | 3.77 | **0.92** |
| HSV | 11.59 | 3.38 | 1.10 | 23.17 | 7.51 | 2.42 |
| CAM16-UCS | 0.00* | 0.00* | 0.59 | 0.00* | 0.00* | 1.31 |

\*CAM16-UCS zeros are an artefact: two of the three fitting datasets were generated *from* CAM16, so it cannot be scored against itself <cite url="https://bottosson.github.io/posts/oklab/">.

Oklab's motivating defect in CIELAB is specific and directly relevant to gradient generation: "Largest issue is their inability to predict hue. In particular blue hues are predicted badly," and white-to-blue blends in CIELAB, CIELUV and HSV "all show hue shifts towards purple" <cite url="https://bottosson.github.io/posts/oklab/">. The fitted exponent γ landed at 0.323 and was pinned to exactly 1/3 with a constraint preventing blues folding inward, at negligible accuracy cost <cite url="https://bottosson.github.io/posts/oklab/">.

<CONFLICTING_EVIDENCE>There is no single space the literature agrees on. Colorgorical (2017) uses CIEDE2000 over CIELAB <cite url="https://gramaz.io/pdf/gramazio-2016-ccd.pdf">; Petroff (2021) uses CAM02-UCS and explicitly notes CIELAB's perceptual problems <cite url="https://arxiv.org/pdf/2107.02270">; Szafir (2018) models in CIELAB but *renormalises* its axes per mark size, effectively rejecting raw CIELAB ΔE as a chart metric <cite url="https://danielleszafir.com/colordiff_vis2017.pdf">; Oklab beats CIELAB on lightness and chroma but loses to JzAzBz on hue <cite url="https://bottosson.github.io/posts/oklab/">. A verifier that hard-codes one space and one threshold inherits that space's failure mode. The defensible engineering position is: interpolate gradients in Oklab/OkLCh (hue linearity, CSS-native), but *test* separation with a CVD-aware metric (Petroff's ΔE_cvd) and *test* mark-level discriminability with Szafir's renormalised CIELAB.</CONFLICTING_EVIDENCE>

#### 2e. Sequential and diverging scales

Crameri, Shephard and Heron's Nature Communications perspective is the standard citation for rejecting rainbow/jet: it distorts data through uneven lightness gradients (in rainbow "the yellow is the brightest"), and red–green maps of similar lightness "cannot be read by a large fraction of the readership", with a general estimate of **0.5% of women and 8% of men** worldwide subject to a colour-vision deficiency <cite url="https://www.nature.com/articles/s41467-020-19160-7.pdf">. It names viridis/magma/plasma/inferno as perceptually uniform, cividis as the closest of currently available maps for red–green CVD appearance while remaining perceptually uniform, and the Scientific colour maps (batlow and family) as perceptually uniform with permanent archival DOIs <cite url="https://www.nature.com/articles/s41467-020-19160-7.pdf">.

---

### 3. Accessibility requirements for charts and diagrams

#### 3a. WCAG 2.2 normative criteria that apply to a chart

| SC | Level | Requirement | Applies to |
|---|---|---|---|
| 1.4.1 Use of Color | A | Colour must not be "used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element" | Every series encoding, every state change |
| 1.4.3 Contrast (Minimum) | AA | Text ≥ **4.5:1**; large text ≥ **3:1**, where large is "at least 18 point or 14 point bold" | Axis labels, titles, legends, data labels, annotations |
| 1.4.11 Non-text Contrast | AA | **3:1** against adjacent colours for UI components and for "Parts of graphics required to understand the content", excepting essential presentation | Bars, lines, points, arrows, node borders, focus rings |
| 1.4.13 Content on Hover or Focus | AA | Dismissible, hoverable, persistent | Tooltips — the default interaction of every interactive chart |
| 2.5.8 Target Size (Minimum) | AA | **24 × 24 CSS px**, or a 24 px-diameter unobstructed circle that does not overlap adjacent targets | Legend toggles, brush handles, clickable points |

<cite url="https://www.w3.org/TR/WCAG22/"> for 1.4.1 / 1.4.3 / 1.4.11 / 1.4.13 verbatim; 2.5.8 values corroborated at <cite url="https://www.w3.org/TR/WCAG22/" note="SC 2.5.8 text was not in the extracted excerpt; 24×24 CSS px and the offset exception are also stated in the Chartability workbook"> and <cite url="https://chartability.github.io/POUR-CAF/">.

The 1.4.11 phrasing matters for a linter: the obligation attaches to "parts of a graphic needed to understand content", so decorative gridlines and background bands are out of scope while a series line, a bar fill boundary and a diagram node border are in. The "essential" exception is the escape hatch a heatmap needs, and a verifier should require it to be declared rather than inferred.

#### 3b. SVG and ARIA structure

The WAI-ARIA Graphics Module defines exactly three roles, with author-supplied fallbacks because the roles are not universally mapped <cite url="https://www.w3.org/TR/graphics-aria-1.0/">:

| Role | SVG element | Fallback pattern | Accessible name required | Children presentational |
|---|---|---|---|---|
| `graphics-document` | `<svg>` root — "structured graphics such as charts, maps, diagrams, technical drawing, blue prints" | `role="graphics-document document"` | **True** | False |
| `graphics-object` | `<g>` for a semantically distinct part | `role="graphics-object group"` | False (name from author *or* contents) | False |
| `graphics-symbol` | `<use>`, `<path>`, atomic marks | `role="graphics-symbol img"` | **True** | **True** |

Two traps: a `<g>` used only for styling or layout should carry `role="none"`, not a graphics role; and because `graphics-symbol` makes children presentational, "the visible text must be included in the label for its parent symbol" — an axis label nested inside a symbol group disappears from the accessibility tree <cite url="https://www.w3.org/TR/graphics-aria-1.0/">. `aria-roledescription` names the symbol *type* separately from the instance label.

#### 3c. Chartability: the only chart-specific heuristic set with numeric criteria

Chartability organises 7 principles (POUR + Compromising, Assistive, Flexible) and **50 heuristics, 14 of them critical** in the current workbook; the 2022 CGF paper had 45 heuristics with 10 critical <cite url="https://chartability.github.io/POUR-CAF/">, <cite url="https://dig.cmu.edu/publications/2022-chartability.html">. Its encodable numbers:

- Geometries and large text **> 3:1**; regular text **> 4.5:1**.
- Interactive state changes **≥ 3:1 against the prior state**, unless a non-colour indicator is supplied — explicitly, "a stroke width change of 2px or more, dash pattern, or added marker".
- Keyboard focus indicator: **4.5:1** against background, **minimum 2px border**, not fully obscured.
- Minimum text size **9pt / 12px**, with 9pt reserved for minor text such as axis labels.
- Pointer/touch target **24px × 24px**.
- Adjacent touching elements (stacked bars, pie slices) need **at least 1px of whitespace** between them.
- Object-constancy animation **no faster than 250ms, no longer than 2s**; animations over 2s or any loop require pause/stop controls. (The workbook notes WCAG permits up to 5s and that it adopted 2s from its own industry studies — a deliberate, documented deviation.)
- Reading grade level **≤ 9** for all text including alt text.
- **No more than one Y or X axis** without first showing two separate charts; no z-axis unless the data is genuinely 3D; recommended ceiling of **5 data categories**, from working-memory research.

<cite url="https://chartability.github.io/POUR-CAF/">

The audit evidence is blunt: **low contrast is the most common failure, at 88% of audits performed** <cite url="https://chartability.github.io/POUR-CAF/">. In the paper's audits, a Tableau dashboard failed 7 of 10 critical tests and 26 of 45 total; a Pudding visual essay failed 22 of 45 including 6 of 10 critical; an infographic explicitly designed for users with disabilities failed 21 of 45 including 5 of 10 critical; and a Highcharts *default demo* failed 13 of 45 including 3 of 10 critical <cite url="https://dig.cmu.edu/publications/2022-chartability.html">. <CONFIDENCE:LOW>These per-system failure counts were retrieved through a search summary of the CMU publication page rather than extracted from the paper PDF, which was not retrievable at synthesis time.</CONFIDENCE:LOW>

#### 3d. Alt text and data-table equivalents

The four-level model of semantic content is the strongest available specification for what generated alt text should contain <cite url="https://arxiv.org/pdf/2110.04406">:

- **Level 1** — construction properties: marks, encodings, axis ranges, colour mappings. Derivable from the spec alone.
- **Level 2** — statistical concepts and relations: extrema, descriptive statistics, correlations. Requires the backing data; "generating sentences at Level 2 is effectively as easy as generating sentences at Level 1" when the software has the data.
- **Level 3** — perceptual and cognitive phenomena: complex trends, clusters, "sharp drop", "visible gap". Perceiver-dependent.
- **Level 4** — contextual and domain-specific insight: explanation, editorialising, external knowledge.

The empirical ranking (Friedman's test, p < 0.001 in both groups; 1,800 rankings per group) is that **blind readers rank Levels 2 and 3 most useful and Levels 1 and 4 least useful**, whereas **sighted readers rank Levels 3 and 4 most useful and Levels 1 and 2 least useful** <cite url="https://arxiv.org/pdf/2110.04406">. Facetting by chart type, topic or difficulty produced no significant differences, so the rule generalises across the 39 diagram types. Level 1 was the only level with a bimodal distribution — a minority of both groups ranked it most useful — so a verifier should treat Level 1 as *optional and toggleable*, not as forbidden. The authors' own architectural suggestion is worth encoding directly: "automatically ARIA tagging web-based charts to surface semantic content at Levels 1 & 2, with human-authors conveying Level 3 content" <cite url="https://arxiv.org/pdf/2110.04406">.

<INFERENCE from="the blind-reader ranking placing Level 4 least useful; the 63% who rejected subjective interpretation; the sighted-reader ranking placing Level 4 most useful">An LLM writing alt text without this constraint will produce Level 4 prose, because Level 4 is what a sighted evaluator — and a sighted-reader-trained model — rates highest. This is a *systematic*, predictable failure rather than a random one, and it is checkable: a verifier can classify generated alt-text sentences by level and fail a description whose Level 4 share exceeds a set fraction, or which contains causal/evaluative constructions.</INFERENCE>

Chartability makes the data-table equivalent a **critical** heuristic in its own right ("No table" under Compromising) <cite url="https://chartability.github.io/POUR-CAF/">, which converts cleanly into a binary verifier check: does the artefact ship a `<table>` (or equivalent structured data) alongside the SVG?

---

### 4. Automated quality checks and verifiable linting

#### 4a. The prior art, and what each proves is buildable

| System | Year | Substrate | Mechanism | Rule count | Evidence of reliability |
|---|---|---|---|---|---|
| `vislint_mpl` (McNutt & Kindlmann) | 2018 | matplotlib figure/axes objects | Runtime inspection + image diffing | Subset of a proposed list implemented | Proof of concept only <cite url="https://c4pgv.dbvis.de/McNutt_Kindlmann_2018.pdf"> |
| Draco (Moritz et al.) | 2019 | Vega-Lite | Answer Set Programming, hard + soft constraints, **weights learned from graphical-perception experiment data** | Knowledge base | Recommends and scores designs <cite url="https://idl.cs.washington.edu/files/2019-Draco-InfoVis.pdf"> |
| VizLinter (Chen et al.) | 2021 | Vega-Lite JSON | ASP linter + linear-programming **fixer** | **41 rules**, refined from Draco | In-lab study, 20 participants <cite url="https://arxiv.org/pdf/2108.10299"> |
| Mirages (McNutt, Kindlmann, Correll) | 2020 | Vega-Lite + backing data | **Metamorphic testing** — perturb data or spec, assert invariance | Test families, not rules | 600 simulated two-column bar charts <cite url="https://arxiv.org/pdf/2001.02316"> |
| VisEval checkers (Chen et al.) | 2024 | Rendered SVG + sandbox | Execution, SVG deconstruction, browser layout simulation, MLLM rating | 3 checker tiers | **Layout 100%, ticks 99%**, readability SRCC 0.843 <cite url="https://arxiv.org/html/2407.00981v1"> |

#### 4b. The rules that are genuinely mechanical

McNutt and Kindlmann's two novel categories are the most transferable, because both are *computed* rather than asserted <cite url="https://c4pgv.dbvis.de/McNutt_Kindlmann_2018.pdf">:

**Computational rules.** `legible-text` — render, run OCR (Tesseract), compare recovered strings against the labels passed to the API; the authors note their implementation "works on especially clear labels, but will need further training to handle labels overlying other marks", which is the exact occlusion case a chart verifier cares about. `no-complex-titles` — Flesch-Kincaid via `textstat` (aligns with Chartability's grade-≤9 rule). `sufficient-data-ink-maximization` — halve and double the charted data, measure pixel change. `legible-graph` — greadability's `crossing-angle` and `angular-resolution-min` with thresholds. `visible-anomalies` — flag histograms whose bin count is low enough to hide gaps or outliers.

**Algebraic (AVD) rules.** `data-dependent-chart` — mutate the data and assert the image changes (catches *confusers*: charts that do not respond to their input). `representation-invariance` — permute the order of series and of data within series, render, and pixel-diff; a difference is a *hallucinator*. `no-connected-categories` — a path drawn between per-category marks asserts an interpolation that does not exist.

The worked example in the paper is instructive for a generated-chart verifier: on a real notebook chart, `vislint_mpl` fired `representation-invariance`, `require-axes-labels`, `max-colors` and `no-indistinguishable-series` simultaneously, and the authors read the conjunction as a single diagnosis — "too many series" <cite url="https://c4pgv.dbvis.de/McNutt_Kindlmann_2018.pdf">.

The Mirages metamorphic families extend this to the data pipeline: **Shuffle** (row permutation), **Bootstrap** (resample within categories), **Contract Records** (downsample all categories to the smallest), **Randomize** (permute value–label assignment as a null test), and specification perturbations to scale baselines and bin widths <cite url="https://arxiv.org/pdf/2001.02316">. One negative result is worth encoding as a known limitation: **MTV: Shuffle "did not yield any variability in the output"** in their evaluation and was excluded <cite url="https://arxiv.org/pdf/2001.02316">.

#### 4c. Geometry and occlusion — what is actually measured

The best-validated occlusion check in the literature is VisEval's, and its design is the finding: the **layout check is done "by simulating a browser environment rather than the model"**, checking overflow and overlap, and it scored **100% accuracy** against three experts with 5+ years of experience <cite url="https://arxiv.org/html/2407.00981v1">. The scale-and-ticks check reached 99%, but only because the deconstructed tick values were injected into the prompt to curb hallucination; **without that auxiliary information it fell to 92%** <cite url="https://arxiv.org/html/2407.00981v1">. Its legality checker parses the saved SVG by `id` attribute to recover chart type, data, axes and legends, and defaults unparseable cases (dual axes, missing ticks) to *illegal* while flagging them <cite url="https://arxiv.org/html/2407.00981v1">.

<MISSING_DATA>What was sought: a published, empirically-justified numeric threshold for acceptable label-on-label or label-on-mark occlusion (e.g. an IoU or percent-occluded cut-off) in charts. What was unavailable: no peer-reviewed source in this search set states one. VisEval's layout check is binary (overflow/overlap present or absent) and is validated *as* a binary. What would be needed: either a perception study relating occlusion fraction to label-reading accuracy, or an OCR round-trip calibration of the kind McNutt & Kindlmann's `legible-text` rule implies. Until then the defensible encoding is zero-tolerance binary overlap plus an OCR round-trip, not an invented percentage.</MISSING_DATA>

#### 4d. Deceptive-encoding checks

The truncation evidence gives a hard rule and refutes the conventional one. Correll, Bertini and Franconeri measured a large main effect of y-axis truncation on subjectively-rated effect size (**F(2,76) = 89, p < 0.0001**, with post-hoc pairwise t-tests separating 0% / 25% / 50% truncation), **no significant effect of chart type** bar versus line (**F(1,38) = 0.5, p = 0.50**), a small framing effect (**F(1,38) = 7.4, p = 0.01**), and — critically for remediation design — no reliable improvement from broken-axis or gradient-bottom designs (**F(2,60) = 3.1, p = 0.05**) <cite url="https://arxiv.org/pdf/1907.02035">. Their own conclusion is not "always start at zero" but that designers should choose the axis range "based on the range and magnitude of effect sizes they wish to communicate" <cite url="https://arxiv.org/pdf/1907.02035">. They also note the separate, purely mechanical harm: truncation means "a viewer inattentive to the axis labels would incorrectly decode the values" <cite url="https://arxiv.org/pdf/1907.02035">.

The CALVI **misleader taxonomy** is the most complete encodable list of deceptive-encoding checks, with 11 categories each defined operationally <cite url="https://mucollective.northwestern.edu/files/2023-CALVI.pdf">:

| Misleader | Detectable from spec/SVG alone? |
|---|---|
| Cherry Picking (subset shown, inference about whole invited) | No — needs the source data |
| Concealed Uncertainty (no uncertainty shown) | Partially — presence of error bars/bands is checkable; whether uncertainty exists is not |
| Inappropriate Aggregation | No — needs the source data |
| Manipulation of Scales — Inappropriate Order | **Yes** — categorical axis order vs. data order |
| Manipulation of Scales — Inappropriate Scale Range (truncation, insufficient colour binning) | **Yes** |
| Manipulation of Scales — Inappropriate Use of Scale Functions (arbitrary non-linear scales) | **Yes** — scale type in spec |
| Manipulation of Scales — Unconventional Scale Directions (inverted axes) | **Yes** |
| Misleading Annotations | Partially |
| Missing Data (representation implies data that is absent) | Partially — gaps vs. zeros |
| Missing Normalization (absolute where relative is wanted) | No — needs intent |
| Overplotting | **Yes** — mark density / overlap |

Six of eleven are decidable from the specification or rendered SVG; five need the backing data or the author's intent. That split *is* the automatable/judge boundary for this dimension.

---

### 5. Documented failure modes of LLM-generated charts, and what measurably reduces them

#### 5a. Failure rates and their taxonomy

VisEval's per-model, per-library table is the cleanest published measurement of where generation breaks <cite url="https://arxiv.org/html/2407.00981v1">:

| Model | Library | Invalid % | Illegal % | Pass % | Readability (1–5) | Quality |
|---|---|---|---|---|---|---|
| GPT-4 | Matplotlib | 3.29 | 21.44 | 75.27 | 3.80 | 2.89 |
| GPT-4 | Seaborn | **25.41** | 15.89 | 58.70 | 3.87 | 2.31 |
| GPT-3.5 | Matplotlib | 8.79 | 29.42 | 61.79 | 3.52 | 2.21 |
| GPT-3.5 | Seaborn | 9.21 | 31.00 | 59.79 | 3.60 | 2.20 |
| Gemini-Pro | Matplotlib | 14.35 | 34.06 | 51.59 | 3.95 | 2.06 |
| Gemini-Pro | Seaborn | 21.09 | 26.82 | 52.09 | 3.88 | 2.06 |
| CodeLlama-7B | Matplotlib | 42.95 | 28.88 | 28.17 | 3.87 | 1.11 |
| CodeLlama-7B | Seaborn | 59.26 | 24.25 | 16.49 | 3.64 | 0.61 |

Note the structure of the failure: for GPT-4 on Matplotlib, **illegal** (renders, but does not satisfy the request) is 6.5× **invalid** (does not render). Code that runs is the easy problem. The dataset is 2,524 queries over 146 databases, 1,150 distinct visualisations <cite url="https://arxiv.org/html/2407.00981v1">.

The paper's five-category failure taxonomy — with no frequency counts reported — is: invalid code (bad or nonexistent API calls, missing imports, hallucinated columns); illegal data transformation; illegal visualisation transformation (wrong chart type, overlapping bars, bad channel mapping, missing or wrong legend); illegal order; and low readability (float years on a discrete axis, inverted y-axis, overflowing axis title, typos) <cite url="https://arxiv.org/html/2407.00981v1">. Charts requiring **three visual channels** (stacked bars, grouped lines, grouped scatter) scored lower than two-channel equivalents <cite url="https://arxiv.org/html/2407.00981v1">.

#### 5b. What measurably reduces them

| Intervention | Measured effect | Source |
|---|---|---|
| **Prefer Matplotlib over Seaborn** | GPT-4 invalid rate 3.29% → 25.41% when switched; attributed to less Seaborn in pretraining corpora | <cite url="https://arxiv.org/html/2407.00981v1"> |
| **Execution-feedback self-debug loop** | GPT-4o Plotly exec pass **77.7 → 97.7%**; GPT-4o-mini Plotly **69.1 → 97.7%**; GPT-4o Seaborn **83.4 → 92.6%**; Matplotlib **94.9 → 99.4%** | <cite url="https://arxiv.org/pdf/2506.03930"> |
| **Visual (rendered-image) feedback + debug, capped at 3 iterations** | GPT-4 MatPlotBench **48.86 → 61.16 (+12.30)**; GPT-3.5 **32.18 → 45.96 (+13.21)** | <cite url="https://arxiv.org/pdf/2402.11453"> |
| **Data-table serialisation format in the prompt** | Swapping to Chat2vis's table format inside CoML4VIS raised pass rate to **70.43%** from 67.55%; disrupting the table cost **7.01–19.79 pp** of pass rate across models | <cite url="https://arxiv.org/html/2407.00981v1"> |
| **Inject deconstructed ground truth into the judge prompt** | Scale-and-ticks check accuracy **92% → 99%** | <cite url="https://arxiv.org/html/2407.00981v1"> |

The self-debug evidence has an important asymmetry. VisCoder-7B's error transitions show structural errors recovering well — Seaborn `AttributeError` **15 → 2**, Plotly `TypeError` **3 → 1** — because "these failures typically result from incorrect method calls, invalid argument types, or simple syntax mistakes, and are often accompanied by clear diagnostic messages" <cite url="https://arxiv.org/pdf/2506.03930">. Semantic failures produce no diagnostic and therefore do not self-repair.

<INFERENCE from="VisEval's illegal:invalid ratio of ~6.5:1 for GPT-4; VisCoder's finding that only diagnostically-signalled errors self-repair">An execution-only retry loop closes the smaller failure class. The verifier must emit *its own* structured diagnostics for illegal and low-readability failures — the same way the interpreter emits an `AttributeError` — or the repair loop has nothing to act on for the 21.44% that renders wrongly. This is the design argument for verifier scripts that exit non-zero *with a machine-readable failure list*, rather than a pass/fail boolean.</INFERENCE>

#### 5c. LLMs as detectors of their own failure mode

Four multimodal models were tested on detecting misleading charts across three experiments escalating from 5 to 21 issue types <cite url="https://arxiv.org/pdf/2407.17291">. Experiment One results show the characteristic pathology: across prompts, "the models showed higher recall and lower precision, suggesting a tendency toward false positives", with recall reaching 1.00 against precision of 0.56–0.63 <cite url="https://arxiv.org/pdf/2407.17291">. Degenerate behaviours are recorded explicitly: one model "chose 3 on a 5-point Likert scale in 78% of cases", and in a later prompt "responded 'Misleading' (# of Major Issues ≥ 1) for 99% of the test cases" <cite url="https://arxiv.org/pdf/2407.17291">. Chain-of-thought helped (relevance rose to 93.33% for one model at Prompt #3), and performance degraded as the issue set expanded from 5 to 21 <cite url="https://arxiv.org/pdf/2407.17291">. The authors' own closing note is that "a benchmark dataset is urgently needed" <cite url="https://arxiv.org/pdf/2407.17291">.

#### 5d. Chart-reproduction benchmarks (relevant to diagram fidelity)

ChartMimic scores 4,800 (figure, code, instruction) triplets across Direct Mimic and Customized Mimic tasks, with a low-level metric decomposing into Text / Layout / Type / Colour F1 obtained by a **code tracer** that monitors execution of both ground-truth and generated code, plus a high-level GPT-4o similarity score 0–100 <cite url="https://arxiv.org/pdf/2406.09961">. **CLIP Score was tested and rejected** for low correlation with human evaluation, leaving GPT-4o Score as the sole high-level metric <cite url="https://arxiv.org/pdf/2406.09961">. GPT-4o reached an overall 81.2 on Direct Mimic; the best open-weight model lagged proprietary models by an average of 20.6 across the two tasks <cite url="https://arxiv.org/pdf/2406.09961">. Failure to execute zeroes both the low-level and high-level scores <cite url="https://arxiv.org/pdf/2406.09961">.

---

### 6. How visualisation quality is evaluated

#### 6a. Human instruments

| Instrument | Year | Items | Construct | Reliability | Admin time |
|---|---|---|---|---|---|
| VLAT | 2017 | 53, over 12 chart types | Standard chart comprehension | High (reported) | ~22 min <cite url="https://washuvis.github.io/minivlat/Mini-VLAT_EuroVIS.pdf"> |
| Mini-VLAT | 2023 | 12 | Same construct, short form | **ω = 0.72**; expert content validity ratio **0.6** from 5 experts | ~5 min <cite url="https://washuvis.github.io/minivlat/Mini-VLAT_EuroVIS.pdf"> |
| CALVI | 2023 | **45-item bank** (from 128 candidates, distilled to 52 then refined) | Critical literacy — resistance to *misleaders* | **ω = 0.81**; 2PL IRT; 497 tryout participants | Not stated <cite url="https://mucollective.northwestern.edu/files/2023-CALVI.pdf"> |

CALVI contributes a metric a skill can borrow directly: the **wrong-due-to-misleader score**, which pairs each misleading item with a well-formed counterpart so that "wrong because misled" is separable from "wrong because the task is hard" <cite url="https://mucollective.northwestern.edu/files/2023-CALVI.pdf">.

#### 6b. Model-as-judge protocols, and how they were validated

| Protocol | Validation method | Agreement achieved | Human baseline |
|---|---|---|---|
| VisEval readability (GPT-4V, decomposed into layout + scale/ticks + 1–5 rating) | 100 sampled visualisations, 3 experts with 5+ years' experience, ratings averaged, Spearman rank correlation | **SRCC 0.843** | **Inter-expert SRCC 0.782** <cite url="https://arxiv.org/html/2407.00981v1"> |
| MatPlotBench (GPT-4V, 0–100 score against reference figure) | Human annotation, Pearson r | **r = 0.876, p = 7.41e-33** (GPT-4 outputs); r = 0.836 (GPT-3.5 outputs) | not reported <cite url="https://arxiv.org/pdf/2402.11453"> |
| ChartMimic high-level (GPT-4o similarity 0–100) | Correlation with human evaluation; CLIP Score rejected on this basis | not quantified in extracted text | — <cite url="https://arxiv.org/pdf/2406.09961"> |

VisEval's ablation is the most useful design guidance for a judge prompt, because it isolates what each component contributes <cite url="https://arxiv.org/html/2407.00981v1">:

| Judge configuration | SRCC | Tokens |
|---|---|---|
| Full (layout + scale/ticks + rating) | **0.843** | 2073.38 |
| Without scale & ticks check | 0.732 | 1071.02 |
| Without layout check | 0.675 | 2063.72 |
| Without both — rating only | **0.507** | 1057.86 |

<INFERENCE from="the VisEval ablation showing rating-only SRCC of 0.507 versus 0.843 with deterministic pre-checks; the layout check's 100% accuracy being achieved by browser simulation rather than by the model">An unaided "ask the model to rate this chart" judge sits at roughly half the rank correlation of the same model handed deterministic measurements first. The verifier scripts and the judge are not alternatives — the scripts are what makes the judge usable, and the token cost of adding them is roughly 2×.</INFERENCE>

---

## Comparison table: candidate verifier checks

| Check | What it measures | Encodable threshold | Substrate needed | Automatable? | Approx. cost | Source authority |
|---|---|---|---|---|---|---|
| Mark-scaled colour separation | ΔE(p,s) per Szafir | `ΔE(p,s) ≥ 1.0` at p=50%, s = smallest rendered mark dim | SVG geometry + palette | **Fully** | O(n²) over palette, µs | Peer-reviewed, TVCG 2018 |
| CVD separation | ΔE_cvd across 3 deficiencies × severities 1–100 | ≥ 20 / 18 / 16 for 6 / 8 / 10 colours (CAM02-UCS) | Palette only | **Fully** | ~300 sims/pair | Peer-reviewed, JCGT 2021 |
| Grayscale separation | ΔJ′ | ≥ 5.0 / 4.2 / 3.6 for 6 / 8 / 10 | Palette only | **Fully** | trivial | Peer-reviewed |
| Lightness bounds | L\*/J′ range | L\* ∈ [25,85] (Colorgorical) or J′ ∈ [40,80–84] (Petroff) | Palette only | **Fully** | trivial | Peer-reviewed ×2 |
| WCAG 1.4.11 non-text contrast | Contrast ratio vs adjacent colour | ≥ 3:1 | Rendered colours | **Fully** | trivial | W3C Recommendation |
| WCAG 1.4.3 text contrast | Contrast ratio | ≥ 4.5:1; ≥ 3:1 at ≥18pt / 14pt bold | Rendered text + bg | **Fully** | trivial | W3C Recommendation |
| Target size | Bounding box of interactive elements | ≥ 24×24 CSS px, or 24px offset circle | Rendered DOM | **Fully** | trivial | W3C Recommendation |
| Redundant encoding | Colour-only distinction | Fail if series distinguished by hue alone | Spec | **Fully** | trivial | WCAG 1.4.1 (Level A) |
| Label overlap / overflow | Bounding-box intersection, clipping | Binary: any overlap or overflow fails | Headless browser | **Fully** (100% validated) | one render | VisEval, TVCG 2024 |
| Label legibility | OCR round-trip vs source strings | Exact match | Raster + Tesseract | **Fully** (partial accuracy) | ~1s/chart | McNutt & Kindlmann 2018 |
| Axis truncation | Baseline ≠ zero on magnitude encodings | Flag on **both** bar and line; do not accept axis break as fix | Spec | **Fully** | trivial | CHI 2020 |
| Inverted / non-conventional axis | Scale direction | Binary | Spec | **Fully** | trivial | CALVI misleader |
| Non-linear scale function | Scale type | Flag `log`/`pow` without explicit declaration | Spec | **Fully** | trivial | CALVI misleader |
| Categorical axis ordering | Rendered order vs data order | Flag reordering that is neither alphabetical, natural, nor value-sorted-with-declaration | Spec + data | **Fully** | trivial | CALVI misleader |
| Representation invariance | Pixel diff under series/row permutation | Zero diff required | Two renders | **Fully** | 2 renders | AVD / McNutt 2018 |
| Data dependence | Pixel diff under data mutation | Non-zero diff required | Two renders | **Fully** | 2 renders | AVD / McNutt 2018 |
| Connected categories | Path between nominal marks | Binary | Spec | **Fully** | trivial | AVD / McNutt 2018 |
| Edge crossings (diagrams) | Segment intersections | Minimise; threshold per diagram type | SVG paths | **Fully** | O(n log n) | Purchase 1997 (Medium conf.) |
| Bends per edge (diagrams) | Vertex count on polylines | Minimise | SVG paths | **Fully** | trivial | Purchase 1997 (Medium conf.) |
| Data-table equivalent present | Structured data alongside SVG | Binary | Artefact | **Fully** | trivial | Chartability *critical* |
| ARIA role structure | `graphics-document` / `-object` / `-symbol` + names | Binary per element | SVG DOM | **Fully** | trivial | W3C ARIA Graphics 1.0 |
| Alt-text semantic level mix | Share of Level 4 sentences | Needs calibration | Generated text | **Partially** — classifier | one classify pass | TVCG 2022 |
| Reading grade | Flesch-Kincaid | ≤ 9 | Text | **Fully** | trivial | Chartability |
| Chart-form appropriateness for task | Task–encoding match | — | Intent | **No** — judge | judge call | Saket 2019 |
| Overall readability / aesthetic | 1–5 rating | SRCC 0.843 achievable *only with* deterministic pre-checks | Render + judge | **Judge** | ~2,073 tokens | VisEval |
| Cherry-picking, aggregation, normalisation | Data-level deception | — | Source data + intent | **No** — judge or human | — | CALVI misleaders |

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---|---|---|
| 50% JND ΔE for a 6px scatter point is 8.37 (L\*), 16.11 (a\*), 19.46 (b\*); 461 MTurk participants | Szafir, "Modeling Color Difference for Visualization Design", IEEE TVCG | 2018 (VIS 2017) | Peer-reviewed crowdsourced experiment + regression models | https://danielleszafir.com/colordiff_vis2017.pdf |
| Elongation gains asymptote at ~2:1 length:thickness, worth 5–10 ΔE | Szafir, TVCG | 2018 | Peer-reviewed experiment | https://danielleszafir.com/colordiff_vis2017.pdf |
| Min CAM02-UCS ΔE 20/18/16 for 6/8/10-colour sets; ΔJ′ 5.0/4.2/3.6; J′ ranges [40,80/82/84] | Petroff, "Accessible Color Sequences for Data Visualization" | 2021 | Peer-reviewed algorithmic construction + preference survey | https://arxiv.org/pdf/2107.02270 |
| CVD simulation via Machado et al. 2009 matrices applied to **linear** sRGB, min over severities 1–100 | Petroff | 2021 | Peer-reviewed method | https://arxiv.org/pdf/2107.02270 |
| WCAG text-contrast ratios are "not a good fit for visualizations" and are defined in a non-perceptually-uniform space | Petroff | 2021 | Peer-reviewed argument | https://arxiv.org/pdf/2107.02270 |
| Colorgorical noticeable difference: ΔL=22.747, Δa=31.427, Δb=44.757 on at least one axis; L\* clamp [25,85]; dark-yellow exclusion L∈[35,75], H∈[85°,114°] | Gramazio, Laidlaw & Schloss, IEEE TVCG 23(1):521–530 | Jan 2017 | Peer-reviewed system + evaluation | https://gramaz.io/pdf/gramazio-2016-ccd.pdf |
| Perceptual Distance (CIEDE2000) and Name Difference (Hellinger over XKCD names) are non-redundant; Pair Preference is a strong negative predictor of both | Gramazio et al. | 2017 | Peer-reviewed regression analysis | https://gramaz.io/pdf/gramazio-2016-ccd.pdf |
| Oklab L RMS 0.20 vs CIELAB 1.70; H RMS 0.49 vs 0.69; JzAzBz better on hue (0.43); γ=0.323 pinned to 1/3 | Ottosson, "A perceptual color space for image processing" | 20 Dec 2020 (matrices rev. 25 Jan 2021) | Author-published derivation with fitted error tables | https://bottosson.github.io/posts/oklab/ |
| Rainbow/jet distorts; ~0.5% of women and 8% of men have a CVD; viridis family and Scientific colour maps are perceptually uniform | Crameri, Shephard & Heron, *Nature Communications* | 28 Oct 2020 | Peer-reviewed perspective | https://www.nature.com/articles/s41467-020-19160-7.pdf |
| Multi-hue categorical palettes 91.44% accuracy vs single-hue sequential 81.11%; category count F(8,91)=20.68 | "Revisiting Categorical Color Perception in Scatterplots" | 2024 | Peer-reviewed crowdsourced experiment | https://arxiv.org/pdf/2404.03787 |
| Cleveland–McGill ranking replicates on MTurk; angle did not perform worse than length; 1:1 aspect ratio worst for area comparison (p<0.05); no rectangle/treemap difference | Heer & Bostock, "Crowdsourcing Graphical Perception", CHI 2010 | Apr 2010 | Peer-reviewed replication | https://www.cs.kent.edu/~javed/class-P2P12F/papers-2012/PAPER2012-2010-MTurk-CHI.pdf |
| Chart effectiveness varies significantly by task across 5 types × 10 tasks; perceived ≠ actual accuracy | Saket, Endert & Demiralp, "Task-Based Effectiveness of Basic Visualizations", IEEE TVCG | 2019 (arXiv 2017) | Peer-reviewed crowdsourced experiment | https://arxiv.org/pdf/1709.08546 |
| Truncation F(2,76)=89 p<0.0001; bar vs line F(1,38)=0.5 p=0.50; mitigations F(2,60)=3.1 p=0.05 | Correll, Bertini & Franconeri, "Truncating the Y-Axis: Threat or Menace?", CHI 2020 | 2020 (arXiv Jul 2019) | Peer-reviewed controlled experiments | https://arxiv.org/pdf/1907.02035 |
| WCAG 2.2: 1.4.1 (A), 1.4.3 4.5:1 / 3:1 at ≥18pt or 14pt bold (AA), 1.4.11 3:1 for graphical objects (AA), 1.4.13 (AA) | W3C, Web Content Accessibility Guidelines 2.2 | 5 Oct 2023 (Rec) | W3C Recommendation (normative) | https://www.w3.org/TR/WCAG22/ |
| ARIA graphics roles, fallback role pairs, name-required and children-presentational values | W3C, WAI-ARIA Graphics Module 1.0 | 2018 (Rec) | W3C Recommendation (normative) | https://www.w3.org/TR/graphics-aria-1.0/ |
| Chartability: 7 principles, 50 heuristics, 14 critical; 3:1/4.5:1, 2px stroke-change alternative, 9pt/12px min text, 24×24px targets, 1px separation, 250ms–2s animation, grade ≤9, ≤5 categories; low contrast fails 88% of audits | Chartability POUR-CAF Workbook (Elavsky) | current (paper: CGF 2022) | Practitioner-maintained heuristic set derived from WCAG + literature | https://chartability.github.io/POUR-CAF/ |
| Chartability audit failure counts per system (7/10 critical, 26/45 total, etc.) | Elavsky, Bennett & Moritz, CGF 2022 — CMU DIG page | 2022 | Peer-reviewed audit study (retrieved via publication page, not PDF) | https://dig.cmu.edu/publications/2022-chartability.html |
| Blind readers rank Levels 2–3 most useful and Levels 1 and 4 least; sighted rank 3–4 most; Friedman p<0.001; 63% (n=19) reject subjective interpretation; 30 blind + 90 sighted, 3,600 rankings | Lundgard & Satyanarayan, "Accessible Visualization via Natural Language Descriptions", IEEE TVCG | 2022 (arXiv Oct 2021) | Peer-reviewed mixed-methods study | https://arxiv.org/pdf/2110.04406 |
| vislint_mpl rule categories: legible-text (OCR), no-complex-titles (Flesch-Kincaid), legible-graph (greadability thresholds), representation-invariance, data-dependent-chart, no-connected-categories | McNutt & Kindlmann, "Linting for Visualization", IEEE VIS VisGuides workshop | Oct 2018 | Peer-reviewed workshop paper + prototype | https://c4pgv.dbvis.de/McNutt_Kindlmann_2018.pdf |
| VizLinter: 41 rules refined from Draco, ASP linter + LP fixer for Vega-Lite; 20-participant study | Chen et al., IEEE TVCG | 2021 (arXiv Aug 2021) | Peer-reviewed system + user study | https://arxiv.org/pdf/2108.10299 |
| Draco: design knowledge as ASP hard/soft constraints with weights learned from perception experiments | Moritz et al., IEEE InfoVis/TVCG | 2019 | Peer-reviewed system | https://idl.cs.washington.edu/files/2019-Draco-InfoVis.pdf |
| Metamorphic testing for visualization; Shuffle yielded no output variability and was excluded; 600 simulated bar charts | McNutt, Kindlmann & Correll, "Surfacing Visualization Mirages", CHI 2020 | 2020 (arXiv Jan 2020) | Peer-reviewed method + simulation study | https://arxiv.org/pdf/2001.02316 |
| VisEval: 2,524 queries / 146 DBs; GPT-4 Matplotlib 3.29% invalid, 21.44% illegal, 75.27% pass; Seaborn 25.41% invalid; layout check 100%, ticks 99% (92% without deconstruction); readability SRCC 0.843 vs inter-expert 0.782; ablation to 0.507 rating-only | Chen et al., IEEE VIS / TVCG | 2024 | Peer-reviewed benchmark | https://arxiv.org/html/2407.00981v1 |
| Self-debug lifts GPT-4o Plotly exec pass 77.7→97.7%; VisCoder-7B Seaborn AttributeError 15→2 | VisCoder (EMNLP Findings 2025) | 2025 (arXiv Jun 2025) | Peer-reviewed benchmark + fine-tuning study | https://arxiv.org/pdf/2506.03930 |
| MatPlotAgent: GPT-4 48.86→61.16 (+12.30); GPT-4V auto-score vs human r=0.876, p=7.41e-33; self-debug capped at 3 iterations | Yang et al., MatPlotAgent / MatPlotBench | 2024 (arXiv Feb 2024) | Peer-reviewed benchmark + agent | https://arxiv.org/pdf/2402.11453 |
| ChartMimic: 4,800 triplets; GPT-4o 81.2 Direct Mimic; open-weight gap 20.6; CLIP Score rejected for low human correlation | Yang et al., ICLR 2025 | 2025 (arXiv Jun 2024) | Peer-reviewed benchmark | https://arxiv.org/pdf/2406.09961 |
| Multimodal LLMs over-flag misleading charts: recall 1.00 / precision 0.52–0.63; 78% midpoint responses; 99% "Misleading" in one prompt; degradation from 5→21 issues | "How Good (Or Bad) Are LLMs at Detecting Misleading Visualizations?" | 2024 (arXiv Jul 2024) | Peer-reviewed empirical study | https://arxiv.org/pdf/2407.17291 |
| CALVI: 11-misleader taxonomy; 45-item bank; ω=0.81; 497 tryout participants; wrong-due-to-misleader score | Ge, Cui & Kay, CHI 2023 | Apr 2023 | Peer-reviewed psychometric instrument | https://mucollective.northwestern.edu/files/2023-CALVI.pdf |
| Mini-VLAT: 12 items, ω=0.72, CVR 0.6, ~5 min vs VLAT's 53 items / ~22 min | Lee, Pandey, Kwon & Ottley, EuroVis / CGF | 2023 | Peer-reviewed psychometric instrument | https://washuvis.github.io/minivlat/Mini-VLAT_EuroVIS.pdf |
| WCAG 3 contrast algorithm "yet to be determined" as of the 8 Apr 2026 Editor's Draft; APCA dropped from the July 2023 WD | Roselli, "WCAG 3 Contrast as of April 2026" | 10 Apr 2026 (upd. 13 Apr) | Practitioner analysis quoting the W3C Editor's Draft and AGWG correspondence | http://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html |
| Edge crossings dominate graph-drawing aesthetics for comprehension | Purchase, "Which Aesthetic Has the Greatest Effect on Human Understanding?", GD 1997 | 1997 | Peer-reviewed experiment (record only; PDF paywalled at synthesis) | https://espace.library.uq.edu.au/view/UQ:8ead24b |

---

## Knowledge Gaps

**Paywalled or unretrievable primary text.**
<MISSING_DATA>Purchase (1997), "Which Aesthetic Has the Greatest Effect on Human Understanding?" — sought for the per-aesthetic significance values and effect sizes that would set thresholds for the 39 diagram types. The Springer chapter redirects to an authentication endpoint and the Glasgow and ResearchGate mirrors returned non-PDF content. What would be needed: institutional access, or the follow-up "Metrics for Graph Drawing Aesthetics" (Purchase 2002) which restates the metrics formally.</MISSING_DATA>
<MISSING_DATA>Elavsky, Bennett & Moritz (2022) Chartability paper PDF — sought for the audit methodology and the per-system failure counts as published. The arXiv identifiers tried resolved to unrelated papers. The workbook (chartability.github.io/POUR-CAF) supplied the current heuristic set and numeric criteria; the CMU publication page supplied the audit counts at lower confidence.</MISSING_DATA>

**No published threshold exists.**
<MISSING_DATA>Label occlusion tolerance. No source in this set states an empirically-derived percent-occluded or IoU cut-off for chart labels. VisEval validates a *binary* overlap check at 100% accuracy but publishes no graded threshold. Any percentage a verifier uses would be invented. Recommended encoding: binary zero-tolerance plus OCR round-trip, with the limitation stated in the skill's own documentation.</MISSING_DATA>
<MISSING_DATA>Minimum contrast for chart marks specifically. WCAG 1.4.11's 3:1 is the only normative number, and Petroff argues explicitly that it is the wrong instrument for visualisation marks. There is no visualisation-specific replacement standard. The two requirements can conflict: a palette optimised for maximum inter-colour CAM02-UCS separation may include light colours that fail 3:1 against a white background.</MISSING_DATA>
<MISSING_DATA>Per-failure-type frequencies in LLM chart generation. VisEval publishes a five-category taxonomy illustrated by example and states no frequency counts, so a verifier cannot be prioritised by measured failure prevalence — only by the aggregate invalid/illegal split.</MISSING_DATA>

**Contested rather than settled.**
<CONFLICTING_EVIDENCE>Colour space for the separation metric: CIEDE2000/CIELAB (Colorgorical), CAM02-UCS (Petroff), size-renormalised CIELAB (Szafir), Oklab (better lightness/chroma) and JzAzBz (better hue) are all defensible, with no cross-comparison study in this evidence set measuring which produces better *chart-reading* outcomes.</CONFLICTING_EVIDENCE>
<CONFLICTING_EVIDENCE>Contrast algorithm: WCAG 2.x relative-luminance is legally operative and normatively stable; APCA is better motivated perceptually but was removed from the WCAG 3 working draft in July 2023 and no successor is adopted as of the 8 April 2026 Editor's Draft. Encoding APCA as the gate would fail automated conformance checkers; encoding only WCAG 2.x accepts known false passes on dark-on-dark pairings.</CONFLICTING_EVIDENCE>
<CONFLICTING_EVIDENCE>Pie charts and angle encodings: the classic effectiveness ranking versus the task-conditional results in Saket et al. and the earlier proportional-comparison literature. Unresolved because the two bodies measure different tasks.</CONFLICTING_EVIDENCE>

**Out of scope of the retrieved evidence.**
<INSUFFICIENT_EVIDENCE>Diagram-as-code specifically (Mermaid, Graphviz, PlantUML, D2) — no peer-reviewed measurement of LLM failure rates or quality on these formats was found. Every LLM chart benchmark in this set targets Python plotting libraries or Vega-Lite. Whether the Matplotlib-versus-Seaborn corpus-frequency effect transfers to Mermaid-versus-D2 is plausible but unmeasured.</INSUFFICIENT_EVIDENCE>
<INSUFFICIENT_EVIDENCE>Interactive-chart quality specifically. WCAG 1.4.13 and 2.5.8 and Chartability's operability heuristics cover the accessibility floor, but no benchmark in this set evaluates generated *interactive* visualisations (hover, brush, zoom, cross-filter) for correctness or comprehension.</INSUFFICIENT_EVIDENCE>

---

## Recommended Next Steps

1. **Calibrate an occlusion threshold locally rather than inventing one.** Generate a fixture set of charts with controlled label-overlap fractions, run Tesseract round-trip against the source strings, and find the occlusion fraction at which OCR recovery fails. *Rationale:* this is the one high-frequency check with no published threshold, it is cheap to calibrate, and it converts McNutt & Kindlmann's `legible-text` rule — which they acknowledged does not yet handle labels overlying marks — into something with a defensible number behind it.

2. **Measure the Matplotlib/Seaborn effect on the actual diagram substrates.** Run the same generation prompts across Mermaid, Graphviz DOT, D2, PlantUML and inline SVG, and record invalid and illegal rates. *Rationale:* the largest measured lever in the whole evidence base (22.12 pp from library choice alone) is a corpus-frequency effect, and the skill's 39 diagram types sit on substrates for which no such measurement exists. If the effect is comparable, substrate selection is a higher-value rule than any prompt guidance.

3. **Build the alt-text level classifier and measure the baseline Level 4 share.** Classify sentences from the skill's current output against the four-level model and measure how much Level 4 content it emits unprompted. *Rationale:* the finding that BLV readers rank Level 4 *least* useful while sighted readers rank it *most* useful predicts a specific, systematic defect. Measuring the baseline share tells you whether a threshold rule is needed or whether the instruction alone suffices.

4. **Resolve the WCAG 1.4.11 versus perceptual-separation conflict on the actual default palette.** Take the skill's palette, compute both WCAG contrast against light and dark backgrounds *and* Petroff's ΔE_cvd, and find whether any colour must be sacrificed to satisfy both. *Rationale:* Petroff states the conflict abstractly; whether it binds depends on the specific palette, and knowing which constraint gives way is a decision that should be made once and recorded rather than rediscovered per chart.

5. **Instrument the verifier to emit structured diagnostics, then measure the repair loop.** Have each failing check emit a machine-readable failure record, feed it back for one repair round, and measure the pass-rate delta separately for invalid, illegal and readability failures. *Rationale:* self-debug on interpreter errors gains 5–28 pp, but only errors with clear diagnostic messages recover. The open question is whether synthetic diagnostics for *illegal* failures — the class that is 6.5× larger than invalid for GPT-4 — produce comparable recovery. That number determines whether the verifier should be a gate or a loop.
