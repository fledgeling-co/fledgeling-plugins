---
title: "Encodable thresholds for visualization and diagram quality"
run_id: dr_a47eb527e3776868
question: "What does the empirical evidence say about producing high-quality static and interactive data visualisations and technical diagrams as code (SVG/HTML) — specifically: (1) graphical perception and encoding-accuracy findings that should govern chart-form selection and mark design; (2) colour design for categorical, sequential and diverging scales including colour-vision-deficiency separation thresholds, perceptual colour spaces (CIELAB/OKLab/CAM16-UCS) and measurable pass/fail criteria; (3) accessibility requirements for charts and diagrams (WCAG 2.2 non-text contrast, redundant encoding, screen-reader/ARIA patterns for SVG, alt-text and data-table equivalents); (4) automated quality checks and verifiable linting for generated visualisations (label collision, occlusion, geometry, axis truncation, deceptive encodings); (5) documented failure modes of LLM-generated charts and diagrams and what measurably reduces them; and (6) how visualisation quality is evaluated (task-based comprehension studies, published benchmarks, automated metrics, rubric and judge protocols)."
provider: local-claude
model: Claude Code
tier: max
archetype: technical
sources: 0
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 0.00
completed: 2026-08-30T06:33:57.233Z
---
🫥 Report written to `2026-08-30-visualisation-and-diagram-quality-encodable-thresholds.md` (+ `.sources.md`), following the repo's dated-pair convention. 27 sources, 25 retrieved as full primary text via curl+pdftotext or W3C HTML; 2 marked lower-confidence because the primary PDF was paywalled or unretrievable.

The four findings that change what you build:

**Colour separation is a function of mark geometry, not of the palette.** Szafir's TVCG 2018 models give closed-form ΔE thresholds per mark type and size — a 6 px scatter point needs 8.37 ΔE on L\* but 19.46 on b\*, and a 2 px line needs 19.47 on b\*. A palette-level check that ignores the marks it paints will pass charts that are measurably indiscriminable. The verifier should read the smallest rendered dimension per series out of the SVG and evaluate pairwise.

**"Never truncate bars, lines are fine" is refuted, and axis-break glyphs don't fix it.** Truncation F(2,76)=89, p<0.0001; bar-vs-line F(1,38)=0.5, p=0.50; broken-axis and gradient mitigations F(2,60)=3.1, p=0.05. Flag both forms; don't accept a break marker as remediation.

**Alt text has an inverted preference, and it's the one an LLM will get wrong.** Blind readers rank Level 4 (contextual/domain insight) *least* useful; sighted readers rank it *most*. 63% of blind participants were emphatic that descriptions must not editorialise. A model optimising for "good alt text" produces exactly the wrong register — systematically, so it's checkable.

**Deterministic pre-checks are what make a judge usable.** VisEval's browser-simulated layout check scored 100% against experts; its GPT-4V readability rating reached SRCC 0.843 *with* those checks and 0.507 without — roughly half the rank correlation for ~half the tokens.

The comparison table lists 26 candidate checks with substrate, threshold, and an automatable / judge-required / human-required column. Two honest holes: there is no published label-occlusion threshold anywhere in the literature (VisEval validates a *binary* overlap check, so encode zero-tolerance plus OCR round-trip rather than inventing a percentage), and no benchmark exists for diagram-as-code substrates — every LLM chart benchmark targets Python plotting or Vega-Lite, so whether the 22-point Matplotlib→Seaborn corpus-frequency penalty transfers to Mermaid-vs-D2 is plausible but unmeasured. That's recommendation #2.
