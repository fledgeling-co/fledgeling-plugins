---
title: "Evaluating UI screenshots against test oracles and design mocks using vision language models"
run_id: dr_14f0ab27c8806524
question: "How should an AI agent reliably validate a UI screenshot against (a) a test's expected output and (b) a design mock, using vision-language-model judgement? Cover: measured failure modes of VLM-as-judge on UI images (position bias, self-preference, verbosity bias, sensitivity to image scale and resolution); whether cropping and zooming into regions materially improves defect detection versus judging a full-page thumbnail, with any measured numbers; how to distinguish legitimate differences (different data, different crop, different viewport) from genuine regressions; where SSIM, MS-SSIM, LPIPS, DISTS and perceptual hashes each fail on UI screenshots specifically; how Percy, Chromatic, Applitools, Playwright toMatchSnapshot and reg-suit handle anti-aliasing, dynamic data and flake; decomposed rubric atoms versus a single overall score; agreement with human labels (Cohen's kappa, Krippendorff's alpha) and what levels are actually achieved; and prompt-injection risk when the judged image contains text."
provider: local-codex
model: Codex CLI
tier: fast
archetype: technical
sources: 30
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 0.00
completed: 2026-08-11T07:31:55.373Z
---
Reading additional input from stdin...
2026-08-11T07:21:10.318140Z ERROR codex_models_manager::cache: failed to load models cache: missing field `base_instructions` at line 94 column 5
OpenAI Codex v0.146.0
--------
workdir: /Users/lukerhodes/Dev/dAIolog
model: gpt-5.6-luna
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: xhigh
reasoning summaries: none
session id: 019fefb2-5938-77c0-84b4-ce6b6d4bfad8
--------
user
<role>
You are a senior research analyst evaluating software stacks, infrastructure, APIs, or model architectures. Your output will directly Grounding a shipped Claude Code skill (be-my-witness) that validates a screenshot against a test expectation and a design mock. The test expectation is the oracle; the mock is advisory. It returns a pass/fail gate plus severity-ranked findings, classifies each difference as framing, data, structure, styling or state, runs every comparison in both orders to catch position bias, and crops to 2-3x rather than judging a full-page thumbnail. Findings become an evidence.md reference and may revise the thresholds already encoded in its prescan script..
</role>

<context>
This investigation supports a concrete decision. Keep this context tight, context bloat degrades long-running agentic output; domain knowledge belongs in the analysis lens below.
</context>

<core_directive>
Answer this decisively: How should an AI agent reliably validate a UI screenshot against (a) a test's expected output and (b) a design mock, using vision-language-model judgement? Cover: measured failure modes of VLM-as-judge on UI images (position bias, self-preference, verbosity bias, sensitivity to image scale and resolution); whether cropping and zooming into regions materially improves defect detection versus judging a full-page thumbnail, with any measured numbers; how to distinguish legitimate differences (different data, different crop, different viewport) from genuine regressions; where SSIM, MS-SSIM, LPIPS, DISTS and perceptual hashes each fail on UI screenshots specifically; how Percy, Chromatic, Applitools, Playwright toMatchSnapshot and reg-suit handle anti-aliasing, dynamic data and flake; decomposed rubric atoms versus a single overall score; agreement with human labels (Cohen's kappa, Krippendorff's alpha) and what levels are actually achieved; and prompt-injection risk when the judged image contains text.
</core_directive>

<research_questions>
Primary:
1. Answer this decisively: How should an AI agent reliably validate a UI screenshot against (a) a test's expected output and (b) a design mock, using vision-language-model judgement? Cover: measured failure modes of VLM-as-judge on UI images (position bias, self-preference, verbosity bias, sensitivity to image scale and resolution); whether cropping and zooming into regions materially improves defect detection versus judging a full-page thumbnail, with any measured numbers; how to distinguish legitimate differences (different data, different crop, different viewport) from genuine regressions; where SSIM, MS-SSIM, LPIPS, DISTS and perceptual hashes each fail on UI screenshots specifically; how Percy, Chromatic, Applitools, Playwright toMatchSnapshot and reg-suit handle anti-aliasing, dynamic data and flake; decomposed rubric atoms versus a single overall score; agreement with human labels (Cohen's kappa, Krippendorff's alpha) and what levels are actually achieved; and prompt-injection risk when the judged image contains text.

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
- general LLM benchmarking unrelated to vision
- vendor marketing without measured data
</exclude>
<time_horizon>
Most recent authoritative data, with any relevant forward outlook.
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
- measured failure modes with numbers, not vendor claims
- what breaks specifically on UI screenshots rather than natural images
- practical thresholds a skill can encode as rules
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
Answer this decisively: How should an AI agent reliably validate a UI screenshot against (a) a test's expected output and (b) a design mock, using vision-language-model judgement? Cover: measured failure modes of VLM-as-judge on UI images (position bias, self-preference, verbosity bias, sensitivity to image scale and resolution); whether cropping and zooming into regions materially improves defect detection versus judging a full-page thumbnail, with any measured numbers; how to distinguish legitimate differences (different data, different crop, different viewport) from genuine regressions; where SSIM, MS-SSIM, LPIPS, DISTS and perceptual hashes each fail on UI screenshots specifically; how Percy, Chromatic, Applitools, Playwright toMatchSnapshot and reg-suit handle anti-aliasing, dynamic data and flake; decomposed rubric atoms versus a single overall score; agreement with human labels (Cohen's kappa, Krippendorff's alpha) and what levels are actually achieved; and prompt-injection risk when the judged image contains text.
</core_directive>
warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
codex
I’m treating this as a source-led research brief for the skill, with the test expectation as the hard oracle and the mock as advisory. I’ll separate measured evidence from synthesis, and I’ll use official docs or primary papers for each integrated claim.
  → Collect primary evidence on VLM-as-judge failure modes and UI screenshot evaluation
  • Collect primary evidence on image metrics, visual-regression tools, rubric design, and prompt injection
  • Synthesize decisive operating rules, thresholds, evidence table, gaps, and next steps
web search: 
web search: site:arxiv.org vision-language model as judge position bias self-preference verbosity bias image scale resolution ...
web search: 
web search: 
web search: 
web search: 
web search: 
web search: vision language model screenshot crop zoom benchmark UI defect detection resolution image scale quantitative ...
web search: 
web search: "GUIZoom-Bench" paper ...
web search: 
web search: 
web search: 
web search: "Visual Test-time Scaling for GUI Agent Grounding" crop accuracy ScreenSpot-Pro ...
web search: 
web search: SSIM UI screenshot visual regression anti-aliasing limitations paper ...
2026-08-11T07:22:18.582924Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: Wang Bovik Sheikh Simon 2004 image quality assessment structural similarity index paper IEEE ...
2026-08-11T07:22:27.292265Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-11T07:22:32.491026Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: site:percy.io docs visual testing anti aliasing dynamic content diff threshold animations ...
2026-08-11T07:22:39.370630Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: site:percy.io/docs snapshot comparison anti aliasing ignore regions dynamic content ...
2026-08-11T07:22:45.004914Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: site:percy.io/docs "ignore" regions snapshot dynamic ...
2026-08-11T07:22:51.249690Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: site:playwright.dev/docs/api/class-snapshotassertions toHaveScreenshot maxDiffPixels threshold animations caret ...
2026-08-11T07:22:57.730551Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: reg-suit visual regression testing docs threshold diff pixel ignore dynamic ...
2026-08-11T07:23:03.371426Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: VLM screenshot evaluation human agreement Cohen's kappa UI visual regression ...
2026-08-11T07:23:10.242898Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: website screenshot visual quality benchmark human agreement VLM judge UI design ...
2026-08-11T07:23:17.980331Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: Zheng 2023 Judging LLM-as-a-Judge position bias verbosity bias self-enhancement ACL ...
2026-08-11T07:23:26.268103Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: site:arxiv.org/abs/2306.05685 Judging LLM-as-a-Judge MT-Bench Chatbot Arena ...
2026-08-11T07:23:31.980298Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: site:platform.openai.com/docs/models vision image input context window pricing GPT-4.1 GPT-4o ...
2026-08-11T07:23:47.467844Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-11T07:23:52.889646Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-11T07:23:58.572949Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-11T07:24:07.640633Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 'Gemini 2.5 Flash'
web search: 
web search: 
web search: 
web search: visual prompt injection attack multimodal LLM image embedded text paper attack success rate GPT-4V ...
warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
context compacted
codex
The evidence now supports a clear design: deterministic preflight and oracle checks first, then a blind, order-swapped VLM review over decomposed atoms and targeted crops. The main evidence gap is direct UI-regression data comparing full-page thumbnails with 2–3× crops; I’ll mark that explicitly rather than treating GUI-grounding gains as defect-detection measurements.
Primary benchmark, UI crop/scale proxies, image metrics, vendor controls, agreement, model, and injection evidence are collected. Moving to synthesis with explicit evidence gaps.
  ✓ Collect primary evidence on VLM-as-judge failure modes and UI screenshot scale/cropping
  ✓ Collect evidence on image metrics, visual regression tools, rubric agreement, model choices, and prompt injection
  → Synthesize the evidence into the requested report and operational recommendations
2026-08-11T07:28:53.696509Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
codex
## Executive Summary

- (High Confidence) Use a fail-closed two-gate validator: deterministic test-oracle checks decide release pass/fail; VLM judgment supplies structured visual findings. A design mock is advisory and must not override the test expectation. <INFERENCE from="Playwright snapshot semantics; MLLM-as-a-Judge benchmark; UI visual-regression tooling documentation">
- (High Confidence) Run every VLM comparison twice with candidate/reference order swapped, blind the model to filenames and model identity, and treat disagreement as instability—not as an average score. Strong judges still show systematic position bias: Claude-3.5-Sonnet’s position-consistency score was 0.82 on MTBench and 0.76 on DevBench. [aclanthology.org](https://aclanthology.org/2025.ijcnlp-long.18.pdf)[Shi et al., 2025](https://aclanthology.org/2025.ijcnlp-long.18.pdf) (unusable citation URL)`
- (Medium Confidence) Targeted 2–3× crops should be used for small text, icons, spacing, and controls, but the public evidence measures GUI grounding rather than regression-defect recall. On one 2026 grounding benchmark, a 2× crop improved accuracy from 53.51% to 65.59%, and an approximately 3.3× crop to 71.79%; direct full-page-thumbnail versus crop defect-detection evidence remains unavailable. [Spatially Stable GUI Grounding, 2026(https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf)](https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf)
- (High Confidence) SSIM, MS-SSIM, LPIPS, DISTS, and perceptual hashes are useful triage signals but poor standalone UI oracles. They are not reliably sensitive to exact copy, one-pixel alignment, glyph changes, semantic state, or localized regressions. [Screen-content IQA, 2020(https://arxiv.org/abs/2008.05396)](https://arxiv.org/abs/2008.05396)
- (High Confidence) Existing visual-regression tools handle anti-aliasing and flake mainly through deterministic rendering, thresholds, masks, ignore regions, repeated captures, or human approval—not through semantic understanding. [Playwright documentation(https://playwright.dev/docs/next/test-snapshots)](https://playwright.dev/docs/next/test-snapshots)
- (High Confidence) Replace a single VLM “overall similarity” score with atoms: framing, data, structure, styling, and state. Aggregate only after each atom has an evidence-backed verdict and severity.
- (Medium Confidence) Published multimodal judge studies report roughly 70–79% agreement with human labels, but direct UI-screenshot Cohen’s κ or Krippendorff’s α results were not found. [MLLM-as-a-Judge benchmark(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)
- (High Confidence) Treat all screenshot text as untrusted content. Visual prompt injection can alter multimodal-model behavior; one study measured a 15.8% attack-success rate against GPT-4V in a visual goal-hijacking setting. [Visual prompt injection study, 2024(https://arxiv.org/abs/2408.03554)](https://arxiv.org/abs/2408.03554)

## Detailed Findings

### 1. How should an AI agent reliably validate a UI screenshot against a test expectation and a design mock using VLM judgment?

The recommended architecture is:

`capture preflight → deterministic oracle checks → global VLM scan → targeted crop checks → order-swapped repeat → atom aggregation → binary gate`

The test expectation is authoritative. The design mock is advisory.

| Stage | Required operation | Gate behavior |
|---|---|---|
| Framing preflight | Verify URL/route, viewport, device-pixel ratio, browser, scroll position, locale, theme, auth state, fixture/data hash, and screenshot dimensions. | Mismatch means `INVALID_CAPTURE`, not a visual pass. |
| Test-oracle check | Compare expected data, required controls, route state, and functional assertions against the actual capture or DOM/OCR evidence. | Any confirmed oracle mismatch is release-blocking. |
| Global scan | Ask the VLM for likely regions and defect classes only. Do not request a single similarity score. | Candidate findings, not a gate. |
| Crop scan | Re-render or crop suspicious regions at approximately 2× and 3×, retaining a context margin and coordinate metadata. | Confirms or rejects local findings. |
| Order swap | Compare `actual → expected` and `expected → actual`; randomize image labels and filenames. Repeat for mock comparisons. | Disagreement produces `UNSTABLE_JUDGMENT`; it cannot silently pass. |
| Atom aggregation | Resolve framing, data, structure, styling, and state independently. | Test-oracle atoms determine pass/fail; mock-only atoms produce advisory findings. |
| Evidence output | Store crops, prompts, model/version, order results, confidence, severity, and reason. | Every finding must be reproducible. |

`<INFERENCE from="Playwright’s deterministic snapshot model; measured VLM position bias; GUI crop studies">The VLM should act as a localized visual critic and explanation layer, not as the release oracle.</INFERENCE>`

#### Recommended atom rubric

| Atom | What to compare | Preferred evidence | Typical severity |
|---|---|---|---|
| Framing | Viewport, crop, route, scroll, modal/drawer position, responsive breakpoint | Capture metadata and DOM state first; VLM second | Blocker |
| Data | Text, numbers, labels, selected values, rows, dates, avatars | Test fixture, DOM/OCR, expected output | Blocker or major |
| Structure | Presence, order, hierarchy, alignment, container boundaries, missing controls | DOM/layout facts plus VLM crops | Major |
| Styling | Colour, typography, border, radius, shadow, spacing, icon treatment | Computed styles/pixel diff plus VLM | Major or minor |
| State | Loading, empty, error, hover, focus, disabled, selected, expanded | State metadata and deterministic interaction capture | Blocker or major |

A practical severity scale is:

- `S0 blocker`: wrong route, viewport, state, crop, missing primary content, or test-oracle mismatch.
- `S1 major`: incorrect structure, control state, data, or large design deviation.
- `S2 minor`: localized typography, spacing, colour, icon, or anti-aliasing issue.
- `S3 advisory`: mock-only divergence, ambiguous evidence, or non-blocking polish.

This severity scheme is an engineering proposal, not a published universal standard.

#### Position bias

Position bias is directly measurable in judge studies. A judge receives the same pair in reversed order; position consistency measures whether it selects the same winner.

Claude-3.5-Sonnet achieved position-consistency scores of 0.82 on MTBench and 0.76 on DevBench. Its preference-fairness scores were 0.01 and 0.22 respectively, showing that bias depends on task and prompt distribution. [Shi et al., 2025(https://aclanthology.org/2025.ijcnlp-long.18.pdf)](https://aclanthology.org/2025.ijcnlp-long.18.pdf)

The earlier MLLM-as-a-Judge benchmark found GPT-4V’s pair-comparison agreement with humans around 78–79.3%, while batch ranking was less reliable. [Chen et al., 2024(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)

The mitigation should therefore be mandatory:

1. Use neutral IDs such as `image_A` and `image_B`.
2. Swap order.
3. Change wording from “which is better?” to atom-specific questions.
4. Require a reason tied to a visible region.
5. Reject order-discordant judgments or send them to a second judge.

#### Self-preference and model-family preference

The foundational MT-Bench work identified position, verbosity, and self-enhancement biases in LLM judges, although that evidence is text-chat rather than UI-specific. [Zheng et al., 2023(https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)

A newer MLLM study using 1.29 million caption-score pairs reports self-preference and family-preference effects across 12 multimodal models; its ensemble mitigation reduced those effects. This is a preprint and not a UI-regression benchmark. [Koyama et al., 2026(https://arxiv.org/abs/2604.11589)](https://arxiv.org/abs/2604.11589)

`<INFERENCE from="self-preference evidence; model identity can correlate with output style">Never expose the judge to the generating model, prompt author, baseline filename, or implementation framework. If multiple judges are used, prefer different model families and report disagreement.</INFERENCE>`

#### Verbosity bias

The evidence for verbosity bias is strong in text judging but lacks a measured UI-screenshot equivalent. Longer UI text blocks may receive more attention than compact but correct controls, while dense screenshots may appear more “detailed” even when wrong.

`<INSUFFICIENT_EVIDENCE>Public studies did not provide a UI-specific effect size for verbosity bias, nor a reliable correction coefficient.</INSUFFICIENT_EVIDENCE>`

Operationally, avoid prompts such as “which screenshot is better?” Require fixed atom outputs:

```json
{
  "atom": "data",
  "verdict": "match | mismatch | unclear",
  "severity": "S0 | S1 | S2 | S3",
  "region": {"x": 0, "y": 0, "width": 0, "height": 0},
  "evidence": "short visible description",
  "confidence": "high | medium | low"
}
```

#### Image scale, resolution, cropping, and zoom

Higher resolution helps when the defect is a small icon, label, or control, but increased visual tokens also increase cost and latency. Apple’s FastVLM work explicitly describes this accuracy/compute trade-off for document and UI recognition. [Apple ML Research, FastVLM(https://machinelearning.apple.com/research/fast-vision-language-models)](https://machinelearning.apple.com/research/fast-vision-language-models)

Microsoft’s Phi-4-reasoning-vision evaluation showed ScreenSpot-Pro accuracy of 9.2% at 2048 visual tokens and 17.5% at 3600 visual tokens. [Microsoft Research, 2026(https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/)](https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/)

RegionFocus reported gains of more than 28 percentage points on ScreenSpot-Pro and more than 24 points on WebVoyager for GUI grounding, with Qwen2.5-VL-72B reaching 61.6% on ScreenSpot-Pro. These are grounding results, not defect-detection results. [Luo et al., ICCV 2025(https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf)](https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf)

A 2026 GUI-grounding study reported the following crop-ratio results for Qwen3-VL-8B on ScreenSpot-Pro:

| Crop scale | Reported accuracy | Change from uncropped |
|---|---:|---:|
| Full image | 53.51% | — |
| 2× zoom | 65.59% | +12.08 points |
| Approximately 3.3× zoom | 71.79% | +18.28 points |

[Spatially Stable GUI Grounding, 2026(https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf)](https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf)

A separate adaptive-zoom preprint reports gains of up to 13.4 points on ScreenSpot-Pro, 10.3 points on UI-Vision, and 4.2 points on ScreenSpot-v2; it also reports larger gains for icon and text targets. [UI-Zoomer, 2026(https://arxiv.org/abs/2604.14113)](https://arxiv.org/abs/2604.14113)

`<MISSING_DATA>Sought a direct benchmark measuring UI-regression defect recall, precision, or human agreement for full-page thumbnails versus 2–3× crops. The available public measurements evaluate GUI grounding or UI perception, not regression diagnosis.</MISSING_DATA>`

`<INFERENCE from="Phi-4 resolution results; RegionFocus; Spatially Stable GUI Grounding; UI-Zoomer">Use a two-pass schedule: one full-page scan for framing and global structure, followed by selective 2× and 3× crops for text, icons, controls, and spacing. Do not crop every region blindly: preserve a parent-context crop because local crops can hide sibling alignment, overflow, and viewport-level defects.</INFERENCE>`

#### Distinguishing legitimate variation from regression

| Apparent difference | Deterministic test | Classification |
|---|---|---|
| Different viewport or device-pixel ratio | Compare capture metadata to expected metadata | Framing; invalidate capture |
| Different route, auth, locale, theme, or scroll state | Compare route/state manifest | Framing/state; invalidate or fail |
| Different data fixture or timestamp | Compare fixture hash, seeded clock, and expected data | Legitimate only if declared; otherwise data regression |
| Different crop or full-page boundary | Compare crop rectangle and scroll offset | Framing; do not judge styling until normalized |
| Font/rendering/anti-aliasing variation | Same browser, OS/container, fonts, DPR; then use calibrated threshold | Usually rendering noise |
| Missing/extra control | DOM expectation plus VLM crop | Structural regression |
| Wrong copy or number | Test expectation, DOM/OCR, exact string comparison | Data regression |
| Mock differs from implementation but test passes | Compare against mock and label advisory | Mock-only finding; not a release failure |
| Animation or asynchronous loading | Wait for a deterministic readiness predicate; repeat capture | Flake or invalid capture, not a visual pass |

`<INFERENCE from="Playwright’s environment-stability guidance; vendor masking/ignore-region controls">The validator must record capture provenance before asking the VLM to compare pixels. A VLM cannot reliably infer whether a changed date, crop, or viewport is legitimate.</INFERENCE>`

#### Agreement with humans

The MLLM-as-a-Judge benchmark reports raw agreement rather than Cohen’s κ or Krippendorff’s α. GPT-4V reached approximately 70% overall human agreement, with pair comparison around 78–79.3% and batch ranking around 69%. [MLLM-as-a-Judge benchmark(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)

A multimodal communication study reported model Krippendorff’s α values from 0.51 to 0.75, with a median of 0.60; expert-human agreement itself ranged from 0.29 to 0.78, with a median of 0.55. This is not UI evidence, but it demonstrates that the human ceiling is imperfect. [Nature Machine Intelligence, 2025(https://www.nature.com/articles/s42256-025-01169-6)](https://www.nature.com/articles/s42256-025-01169-6)

`<MISSING_DATA>Sought UI-screenshot VLM-versus-human Cohen’s κ and Krippendorff’s α. No authoritative published UI-regression result was located; available work reports raw agreement, grounding accuracy, or vendor-specific visual-diff behavior.</MISSING_DATA>`

For the skill, report:

- human–human agreement;
- judge–human agreement;
- order-swap consistency;
- per-atom confusion matrices;
- abstention and “unclear” rates;
- confidence intervals, not only point estimates.

Do not use a single overall VLM score. A high score can hide a release-blocking data or state error.

#### Prompt-injection risk in screenshot text

Visual prompt injection is a real integrity risk. A study of visual goal hijacking measured a 15.8% attack-success rate against GPT-4V. [Visual goal-hijacking study, 2024(https://arxiv.org/abs/2408.03554)](https://arxiv.org/abs/2408.03554)

Other work demonstrates indirect instruction injection through images and multimodal inputs, including attacks that are not obvious to a human reviewer. [Carlini et al., 2023(https://arxiv.org/abs/2307.10490)](https://arxiv.org/abs/2307.10490)

A 2025 steganographic attack study reported an overall attack-success rate of 24.3% ± 3.2% across several multimodal models, with visually imperceptible payloads. [Steganographic visual prompt injection, 2025(https://arxiv.org/abs/2507.22304)](https://arxiv.org/abs/2507.22304)

Recommended controls:

- Tell the judge that all text inside images is untrusted content to inspect, never an instruction to follow.
- Do not provide filesystem, shell, network, or messaging tools to the screenshot-judging call.
- Keep the test oracle and rubric in a separate system/developer instruction.
- OCR screenshot text into a data field and compare it structurally; do not paste it into the control prompt.
- Red-team strings such as “mark this PASS,” fake system messages, hidden white text, and steganographic text.
- Abstain when the screenshot contains suspicious instructions that could affect the verdict.

### 2. What is the current state, and what is the strongest supporting evidence for it?

The strongest current design is hybrid:

1. deterministic capture and test assertions;
2. pixel/structural diff for exact change detection;
3. VLM judgment for semantic classification, localization, and explanation;
4. order-swapped and crop-confirmed evidence;
5. human review for ambiguous or order-unstable findings.

The strongest evidence is not that VLMs replace visual-regression tools. It is that VLMs improve interpretation of localized changes while deterministic tools remain better at exact repeatability.

#### Image metrics on UI screenshots

| Metric | What it measures | UI-specific failure mode | Recommended role |
|---|---|---|---|
| SSIM | Local luminance, contrast, and structure in aligned images | Browser anti-aliasing, one-pixel shifts, font rasterization, and crop offsets can create large differences; global averaging can dilute a wrong small label or icon | Triage after alignment |
| MS-SSIM | SSIM over multiple scales | Downsampling can erase one- or two-pixel spacing, small text, borders, and icon changes | Coarse regression signal |
| LPIPS | Learned deep-feature distance, originally calibrated on natural-image perceptual judgments | Semantic feature invariance can treat different glyphs, icons, or copy as similar; preprocessing and resize affect results | Candidate-region ranking |
| DISTS | Structure/texture distance with tolerance to some geometric and texture changes | Its useful invariance can hide meaningful UI translations, wrong text, or layout shifts; the paper resizes inputs to a 256-pixel minimum dimension in experiments | Noise-tolerant triage |
| Perceptual hash | Compact signature for near-duplicate media | No DOM, region, text, state, or semantic understanding; broad layout similarity can survive wrong content, while crop changes can destroy hash similarity | Deduplication/cache only |

SSIM was designed around luminance, contrast, and structural similarity, not UI semantics. [Wang et al., 2004(https://pubmed.ncbi.nlm.nih.gov/15376593/)](https://pubmed.ncbi.nlm.nih.gov/15376593/)

MS-SSIM explicitly aggregates across scales, which is useful for coarse appearance but dangerous for tiny UI changes. [Wang et al., 2003(https://live.ece.utexas.edu/publications/2003/zw_asil2003_msssim.pdf)](https://live.ece.utexas.edu/publications/2003/zw_asil2003_msssim.pdf)

LPIPS was developed for learned perceptual similarity on natural-image judgments, not exact UI typography or layout. [Zhang et al., 2018(https://arxiv.org/abs/1801.03924)](https://arxiv.org/abs/1801.03924)

DISTS intentionally combines structure and texture while becoming less sensitive to some geometric transformations and texture resampling. That is beneficial for photographs but can conceal UI movement. [Ding et al., 2020(https://arxiv.org/abs/2004.07728)](https://arxiv.org/abs/2004.07728)

pHash describes a perceptual signature of underlying media and is primarily useful for duplicate or near-duplicate detection. [pHash documentation(https://phash.org/docs/howto.html)](https://phash.org/docs/howto.html)

A screen-content IQA paper specifically notes that local single-level structure measures can be unreliable for screen content and that resizing feature maps introduces distortion. [Screen-content IQA, 2020(https://arxiv.org/abs/2008.05396)](https://arxiv.org/abs/2008.05396)

`<INFERENCE from="screen-content IQA; original metric objectives; known scale/alignment behavior">Use metrics as prescan signals to locate candidate changes, never as the final semantic gate. A test expectation should be checked with exact data/DOM assertions, while the VLM should classify the localized visual evidence.</INFERENCE>`

#### How existing tools handle anti-aliasing, dynamic data, and flake

| Tool | Anti-aliasing | Dynamic data | Flake handling | Limitation |
|---|---|---|---|---|
| Percy | Deterministic rendering and a visual engine intended to avoid anti-aliasing false positives | Ignore regions, frozen media, configurable sensitivity, and stabilization controls | Deterministic rendering and baseline review | Vendor documentation does not establish independent defect-recall rates |
| Chromatic | Ignores anti-aliased pixels by default; `diffIncludeAntiAliasing` can include them; default `diffThreshold` is 0.063 | Stable stories, masking, and controlled inputs | Unstable-test detection/flake filtering; recommends deterministic data and fonts | Threshold changes can hide subtle colour or position regressions |
| Applitools | Match levels and region types rather than only a global pixel threshold | Ignore, content, layout, floating, and dynamic match regions | Stabilization through match levels and targeted regions | Semantic behavior depends heavily on region configuration |
| Playwright `toHaveScreenshot` | Pixelmatch thresholding; `threshold` defaults to 0.2 YIQ; masks and stylesheets can remove volatile regions | User supplies masks, `stylePath`, deterministic fixtures, or waits | Captures until two consecutive screenshots match before comparison; same environment is required | No automatic semantic understanding of dynamic content |
| reg-suit | `matchingThreshold`, `thresholdPixel`, `thresholdRate`, and an `enableAntialias` option; ximgdiff reports structural changes | No native understanding of business-dynamic data; upstream stabilization/masking is required | CI comparison, baselines, reports, and external storage | Configuration-driven rather than semantic |

Chromatic documents a default `diffThreshold` of 0.063 and anti-aliased-pixel exclusion by default. [Chromatic threshold documentation(https://www.chromatic.com/docs/threshold/)](https://www.chromatic.com/docs/threshold/)

Chromatic separately documents animations, late fonts, dynamic data, and late resources as causes of unstable tests. [Chromatic unstable-test documentation(https://www.chromatic.com/docs/unstable-tests/)](https://www.chromatic.com/docs/unstable-tests/)

Percy documents deterministic pixel rendering and controls for anti-aliasing and dynamic regions. [Percy anti-aliasing changelog(https://percy.io/changelog/anti-aliasing)](https://percy.io/changelog/anti-aliasing)

Applitools documents `Content`, `Layout`, and `Ignore` match regions for separating content changes from geometry changes. [Applitools match regions(https://help.applitools.com/hc/en-us/articles/360007188151-Match-Regions)](https://help.applitools.com/hc/en-us/articles/360007188151-Match-Regions)

Playwright documents repeated screenshot capture, same-environment requirements, thresholds, masks, and style overrides. [Playwright screenshot assertions(https://playwright.dev/docs/next/test-snapshots)](https://playwright.dev/docs/next/test-snapshots)

reg-suit exposes pixel/color thresholds, anti-aliasing configuration, structural diff reporting, and cloud-storage plugins. [reg-suit repository(https://github.com/reg-viz/reg-suit)](https://github.com/reg-viz/reg-suit)

#### Candidate VLM backends

The following table is a capability and procurement comparison, not a benchmark ranking. Closed-model parameter counts and latency are not publicly disclosed.

| Model | Parameter count | Context window | Latency | API cost | License |
|---|---:|---:|---|---|---|
| GPT-5.6 Terra | Not disclosed | 1.05M tokens | Provider does not publish a fixed latency | $2/M input, $12/M output | Proprietary API |
| Claude Sonnet 4.6 | Not disclosed | 1M tokens | Provider does not publish a fixed latency | $3/M input, $15/M output | Proprietary API |
| Gemini 2.5 Flash | Not disclosed | 1,048,576 input tokens; 65,536 output tokens | Provider does not publish a fixed latency | $0.30/M input, $2.50/M output | Proprietary API |
| Gemini 2.5 Pro | Not disclosed | 1,048,576 input tokens; 65,536 output tokens | Provider does not publish a fixed latency | $1.25/M input up to 200k context, $2.50/M above; output $10/$15 | Proprietary API |
| Qwen2.5-VL-72B | 73B | 32,768 native; 64k YaRN extension with spatial-localization caveats | Hardware- and quantization-dependent | Self-hosting cost is hardware-dependent | Qwen License Agreement |

OpenAI’s current model documentation lists the GPT-5.6 Terra context and prices but not parameter count or fixed latency. [OpenAI model documentation(https://developers.openai.com/api/docs/models)](https://developers.openai.com/api/docs/models)

Anthropic lists Claude Sonnet 4.6 at $3/M input and $15/M output and documents 1M context for Claude 4.6 models. [Anthropic pricing documentation(https://platform.claude.com/docs/en/about-claude/pricing)](https://platform.claude.com/docs/en/about-claude/pricing)

Google lists Gemini 2.5 Flash and Pro context windows and prices in its model and pricing documentation. [Gemini API pricing(https://ai.google.dev/gemini-api/docs/pricing)](https://ai.google.dev/gemini-api/docs/pricing)

Qwen’s model card lists 73B parameters, native context limits, and the Qwen license terms. [Qwen2.5-VL-72B model card(https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct)](https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct)

### 3. What are the contrasting viewpoints or competing evidence?

#### Deterministic diff versus VLM judgment

The deterministic position is that visual regression is fundamentally an image-comparison problem: control rendering, compare pixels, and review differences. This is reproducible and well suited to one-pixel shifts, missing borders, and exact baselines.

The semantic position is that pixel diffs over-report anti-aliasing, font rasterization, dynamic data, and harmless rendering noise. A VLM can classify whether the changed region is a meaningful data, structure, style, or state change.

`<CONFLICTING_EVIDENCE>The two approaches optimize different errors. Deterministic tools provide repeatability and exact localization; VLMs provide semantic interpretation but introduce judge bias, scale sensitivity, and prompt-injection risk.</CONFLICTING_EVIDENCE>`

The correct resolution is not to choose one: use deterministic comparisons for the hard oracle and VLMs for interpretation.

#### Full-page context versus local crops

Full-page images preserve relationships among containers, siblings, responsive layout, and viewport boundaries. Crops make small text and icons legible and materially improve GUI-grounding accuracy in available studies.

`<INFERENCE from="crop-grounding improvements; missing direct defect-detection benchmark">Use both views. The full page is necessary for framing and global structure; 2–3× crops are necessary for fine-grained inspection.</INFERENCE>`

#### Single overall score versus decomposed atoms

A single score is attractive operationally but hides which failure occurred and is vulnerable to verbosity, position, and salience bias. Decomposed atoms make the oracle hierarchy explicit, support severity ranking, and allow test data differences to be separated from mock styling differences.

The MLLM benchmark found pair comparison more consistent than batch ranking, supporting pairwise, focused judgments over a single holistic ranking. [MLLM-as-a-Judge benchmark(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)

#### Vendor controls versus independent evidence

Vendors document useful controls for thresholds, masking, dynamic regions, and flake, but these documents establish product behavior, not independent comparative accuracy. A 2026 Web UI Image Change Captioning benchmark reports that web UI change description remains difficult because of dense text, layout diversity, and fine-grained changes, and notes that industry visual-regression tools lack broad public evaluation. [WUICC benchmark, 2026(https://arxiv.org/abs/2607.01728)](https://arxiv.org/abs/2607.01728)

### 4. What changed recently, and what is the trajectory?

- (High Confidence) 2023 established that LLM judges can reach human-like agreement in some text-chat settings while still exhibiting position, verbosity, and self-enhancement biases. [Zheng et al., 2023(https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)
- (High Confidence) 2024 multimodal judge work quantified imperfect human agreement and showed that pairwise comparison is more reliable than some ranking formats. [MLLM-as-a-Judge benchmark(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)
- (High Confidence) 2025 work demonstrated that position bias remains systematic across capable judges and changes by task, model, and quality gap. [Shi et al., 2025(https://aclanthology.org/2025.ijcnlp-long.18.pdf)](https://aclanthology.org/2025.ijcnlp-long.18.pdf)
- (High Confidence) 2025 GUI-grounding work shifted toward region selection, visual test-time scaling, and adaptive crops rather than single-pass full-screen perception. [RegionFocus, ICCV 2025(https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf)](https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf)
- (Medium Confidence) 2026 work increasingly treats adaptive zoom as a selective operation: useful for small targets, harmful when applied indiscriminately because it adds latency and removes context. [UI-Zoomer, 2026(https://arxiv.org/abs/2604.14113)](https://arxiv.org/abs/2604.14113)
- (Medium Confidence) The trajectory is toward hybrid systems: deterministic capture and diffing, structured VLM critique, crop-based visual test-time scaling, and explicit instability handling. <INFERENCE from="WUICC benchmark; current visual-regression documentation; crop-grounding literature">This is an engineering synthesis, not a directly measured industry-wide outcome.</INFERENCE>

## Evidence Table

Sources were retained when they were peer-reviewed papers, benchmark papers/preprints with public measurements, official API/model documentation, or official product/repository documentation. Vendor documentation is used only to establish documented controls, not comparative efficacy.

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| LLM judges exhibit position, verbosity, and self-enhancement biases; GPT-4 can exceed 80% agreement in text-chat preference settings | Zheng et al., NeurIPS | 2023 | Peer-reviewed benchmark | [URL](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html) |
| GPT-4V pair-comparison agreement is approximately 78–79.3%; batch ranking is weaker | MLLM-as-a-Judge benchmark | 2024 | Public benchmark results | [URL](https://mllm-judge.github.io/) |
| Claude-3.5-Sonnet position consistency is 0.82/0.76 across two benchmarks | Shi et al. | 2025 | Peer-reviewed conference paper | [URL](https://aclanthology.org/2025.ijcnlp-long.18.pdf) |
| MLLMs show self- and family-preference bias over 1.29M caption-score pairs | Koyama et al. | 2026 | Preprint with measured corpus | [URL](https://arxiv.org/abs/2604.11589) |
| Higher visual-token resolution improved ScreenSpot-Pro from 9.2% to 17.5% in one Phi-4 evaluation | Microsoft Research | 2026 | Official engineering evaluation | [URL](https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/) |
| Region selection improved GUI grounding by more than 28 points on ScreenSpot-Pro and more than 24 on WebVoyager | Luo et al., RegionFocus | 2025 | ICCV paper | [URL](https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf) |
| Approximately 2× and 3.3× crops improved ScreenSpot-Pro grounding by 12.08 and 18.28 points | Spatially Stable GUI Grounding | 2026 | OpenReview paper/preprint | [URL](https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf) |
| Adaptive zoom reported gains up to 13.4 points on ScreenSpot-Pro | UI-Zoomer | 2026 | Preprint | [URL](https://arxiv.org/abs/2604.14113) |
| Web UI change captioning remains difficult because of dense text, layout diversity, and fine-grained changes | WUICC benchmark | 2026 | Preprint benchmark | [URL](https://arxiv.org/abs/2607.01728) |
| SSIM compares luminance, contrast, and structure | Wang et al. | 2004 | Peer-reviewed metric paper | [URL](https://pubmed.ncbi.nlm.nih.gov/15376593/) |
| MS-SSIM extends structural comparison across scales | Wang et al. | 2003 | Peer-reviewed metric paper | [URL](https://live.ece.utexas.edu/publications/2003/zw_asil2003_msssim.pdf) |
| LPIPS is a learned perceptual metric calibrated primarily on natural-image judgments | Zhang et al. | 2018 | CVPR paper | [URL](https://arxiv.org/abs/1801.03924) |
| DISTS combines structure and texture and tolerates some geometric changes | Ding et al. | 2020 | Peer-reviewed metric paper | [URL](https://arxiv.org/abs/2004.07728) |
| pHash provides perceptual signatures suitable for duplicate/near-duplicate detection | pHash project | Current | Official documentation | [URL](https://phash.org/docs/howto.html) |
| Chromatic uses a 0.063 default diff threshold and excludes anti-aliased pixels by default | Chromatic | Current | Official product documentation | [URL](https://www.chromatic.com/docs/threshold/) |
| Chromatic identifies animation, fonts, dynamic data, and late resources as instability causes | Chromatic | Current | Official product documentation | [URL](https://www.chromatic.com/docs/unstable-tests/) |
| Applitools provides content, layout, ignore, and dynamic match regions | Applitools | Current | Official product documentation | [URL](https://help.applitools.com/hc/en-us/articles/360007188151-Match-Regions) |
| Percy documents deterministic rendering and anti-aliasing controls | Percy | Current | Official product changelog | [URL](https://percy.io/changelog/anti-aliasing) |
| Playwright waits for two consecutive matching screenshots and supports masks, styles, and thresholds | Playwright | Current | Official documentation | [URL](https://playwright.dev/docs/next/test-snapshots) |
| reg-suit exposes pixel/color thresholds, anti-aliasing configuration, and structural diff reports | reg-suit | Current | Official repository | [URL](https://github.com/reg-viz/reg-suit) |
| Visual goal hijacking achieved 15.8% attack success against GPT-4V | Visual prompt injection study | 2024 | Preprint experiment | [URL](https://arxiv.org/abs/2408.03554) |
| Steganographic visual injection achieved 24.3% ± 3.2% overall attack success | Steganographic visual injection study | 2025 | Preprint experiment | [URL](https://arxiv.org/abs/2507.22304) |
| Multimodal model-human Krippendorff’s α ranged from 0.51 to 0.75 in an out-of-domain communication task | Nature Machine Intelligence study | 2025 | Peer-reviewed study | [URL](https://www.nature.com/articles/s42256-025-01169-6) |
| Current API context windows and prices for candidate judge models | OpenAI, Anthropic, Google, Qwen documentation | 2026/current | Official model/API documentation | [OpenAI](https://developers.openai.com/api/docs/models), [Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), [Google](https://ai.google.dev/gemini-api/docs/pricing), [Qwen](https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct) |

## Knowledge Gaps

### Direct measurement gaps

- <MISSING_DATA>There is no located public benchmark of full-page-thumbnail versus 2–3× crop defect recall and precision for web UI visual regression.</MISSING_DATA>
- <MISSING_DATA>There is no located public UI-specific VLM-as-judge dataset reporting Cohen’s κ or Krippendorff’s α against human labels.</MISSING_DATA>
- <MISSING_DATA>There is no independent, cross-vendor benchmark comparing Percy, Chromatic, Applitools, Playwright, and reg-suit on anti-aliasing false positives, dynamic-data false positives, and flake rates.</MISSING_DATA>

### Calibration gaps

- Thresholds for “minor” versus “major” UI differences are product- and viewport-dependent.
- The impact of different browsers, fonts, operating systems, device-pixel ratios, and GPU rendering paths needs local measurement.
- VLM performance may differ substantially by screenshot density, language, design system, and defect type.

### Model-operation gaps

- Closed-model parameter counts and p50/p95 image latency are not publicly disclosed.
- Published API prices do not capture image-tokenization differences, retries, crop count, or order-swapped calls.
- Prompt-injection attack rates are domain- and payload-dependent; no universal mitigation rate is established.

## Recommended Next Steps

1. Build a stratified gold set covering framing, data, structure, styling, and state defects, including legitimate viewport/data/crop differences. Double-label it with humans and measure κ/α, confusion matrices, and order-swap stability.

2. Implement the capture preflight manifest: route, viewport, DPR, browser, fonts, locale, theme, auth state, scroll position, fixture hash, readiness predicate, and crop rectangle.

3. Add a selective crop schedule: full-page scan, then 2× and 3× crops for VLM-identified regions, plus one parent-context crop. Record whether each crop confirms, weakens, or contradicts the global finding.

4. Run a local model bakeoff using the candidate table. Measure per-atom recall, false-positive rate, abstention, order consistency, p50/p95 latency, token cost, and prompt-injection susceptibility—not overall similarity.

5. Feed the resulting false-positive and false-negative rates into `evidence.md` and revise prescan thresholds empirically. Keep mock-only differences advisory and preserve the test expectation as the release gate.
tokens used
290,450
## Executive Summary

- (High Confidence) Use a fail-closed two-gate validator: deterministic test-oracle checks decide release pass/fail; VLM judgment supplies structured visual findings. A design mock is advisory and must not override the test expectation. <INFERENCE from="Playwright snapshot semantics; MLLM-as-a-Judge benchmark; UI visual-regression tooling documentation">
- (High Confidence) Run every VLM comparison twice with candidate/reference order swapped, blind the model to filenames and model identity, and treat disagreement as instability—not as an average score. Strong judges still show systematic position bias: Claude-3.5-Sonnet’s position-consistency score was 0.82 on MTBench and 0.76 on DevBench. [Shi et al., 2025(https://aclanthology.org/2025.ijcnlp-long.18.pdf)](https://aclanthology.org/2025.ijcnlp-long.18.pdf)
- (Medium Confidence) Targeted 2–3× crops should be used for small text, icons, spacing, and controls, but the public evidence measures GUI grounding rather than regression-defect recall. On one 2026 grounding benchmark, a 2× crop improved accuracy from 53.51% to 65.59%, and an approximately 3.3× crop to 71.79%; direct full-page-thumbnail versus crop defect-detection evidence remains unavailable. [Spatially Stable GUI Grounding, 2026(https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf)](https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf)
- (High Confidence) SSIM, MS-SSIM, LPIPS, DISTS, and perceptual hashes are useful triage signals but poor standalone UI oracles. They are not reliably sensitive to exact copy, one-pixel alignment, glyph changes, semantic state, or localized regressions. [Screen-content IQA, 2020(https://arxiv.org/abs/2008.05396)](https://arxiv.org/abs/2008.05396)
- (High Confidence) Existing visual-regression tools handle anti-aliasing and flake mainly through deterministic rendering, thresholds, masks, ignore regions, repeated captures, or human approval—not through semantic understanding. [Playwright documentation(https://playwright.dev/docs/next/test-snapshots)](https://playwright.dev/docs/next/test-snapshots)
- (High Confidence) Replace a single VLM “overall similarity” score with atoms: framing, data, structure, styling, and state. Aggregate only after each atom has an evidence-backed verdict and severity.
- (Medium Confidence) Published multimodal judge studies report roughly 70–79% agreement with human labels, but direct UI-screenshot Cohen’s κ or Krippendorff’s α results were not found. [MLLM-as-a-Judge benchmark(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)
- (High Confidence) Treat all screenshot text as untrusted content. Visual prompt injection can alter multimodal-model behavior; one study measured a 15.8% attack-success rate against GPT-4V in a visual goal-hijacking setting. [Visual prompt injection study, 2024(https://arxiv.org/abs/2408.03554)](https://arxiv.org/abs/2408.03554)

## Detailed Findings

### 1. How should an AI agent reliably validate a UI screenshot against a test expectation and a design mock using VLM judgment?

The recommended architecture is:

`capture preflight → deterministic oracle checks → global VLM scan → targeted crop checks → order-swapped repeat → atom aggregation → binary gate`

The test expectation is authoritative. The design mock is advisory.

| Stage | Required operation | Gate behavior |
|---|---|---|
| Framing preflight | Verify URL/route, viewport, device-pixel ratio, browser, scroll position, locale, theme, auth state, fixture/data hash, and screenshot dimensions. | Mismatch means `INVALID_CAPTURE`, not a visual pass. |
| Test-oracle check | Compare expected data, required controls, route state, and functional assertions against the actual capture or DOM/OCR evidence. | Any confirmed oracle mismatch is release-blocking. |
| Global scan | Ask the VLM for likely regions and defect classes only. Do not request a single similarity score. | Candidate findings, not a gate. |
| Crop scan | Re-render or crop suspicious regions at approximately 2× and 3×, retaining a context margin and coordinate metadata. | Confirms or rejects local findings. |
| Order swap | Compare `actual → expected` and `expected → actual`; randomize image labels and filenames. Repeat for mock comparisons. | Disagreement produces `UNSTABLE_JUDGMENT`; it cannot silently pass. |
| Atom aggregation | Resolve framing, data, structure, styling, and state independently. | Test-oracle atoms determine pass/fail; mock-only atoms produce advisory findings. |
| Evidence output | Store crops, prompts, model/version, order results, confidence, severity, and reason. | Every finding must be reproducible. |

`<INFERENCE from="Playwright’s deterministic snapshot model; measured VLM position bias; GUI crop studies">The VLM should act as a localized visual critic and explanation layer, not as the release oracle.</INFERENCE>`

#### Recommended atom rubric

| Atom | What to compare | Preferred evidence | Typical severity |
|---|---|---|---|
| Framing | Viewport, crop, route, scroll, modal/drawer position, responsive breakpoint | Capture metadata and DOM state first; VLM second | Blocker |
| Data | Text, numbers, labels, selected values, rows, dates, avatars | Test fixture, DOM/OCR, expected output | Blocker or major |
| Structure | Presence, order, hierarchy, alignment, container boundaries, missing controls | DOM/layout facts plus VLM crops | Major |
| Styling | Colour, typography, border, radius, shadow, spacing, icon treatment | Computed styles/pixel diff plus VLM | Major or minor |
| State | Loading, empty, error, hover, focus, disabled, selected, expanded | State metadata and deterministic interaction capture | Blocker or major |

A practical severity scale is:

- `S0 blocker`: wrong route, viewport, state, crop, missing primary content, or test-oracle mismatch.
- `S1 major`: incorrect structure, control state, data, or large design deviation.
- `S2 minor`: localized typography, spacing, colour, icon, or anti-aliasing issue.
- `S3 advisory`: mock-only divergence, ambiguous evidence, or non-blocking polish.

This severity scheme is an engineering proposal, not a published universal standard.

#### Position bias

Position bias is directly measurable in judge studies. A judge receives the same pair in reversed order; position consistency measures whether it selects the same winner.

Claude-3.5-Sonnet achieved position-consistency scores of 0.82 on MTBench and 0.76 on DevBench. Its preference-fairness scores were 0.01 and 0.22 respectively, showing that bias depends on task and prompt distribution. [Shi et al., 2025(https://aclanthology.org/2025.ijcnlp-long.18.pdf)](https://aclanthology.org/2025.ijcnlp-long.18.pdf)

The earlier MLLM-as-a-Judge benchmark found GPT-4V’s pair-comparison agreement with humans around 78–79.3%, while batch ranking was less reliable. [Chen et al., 2024(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)

The mitigation should therefore be mandatory:

1. Use neutral IDs such as `image_A` and `image_B`.
2. Swap order.
3. Change wording from “which is better?” to atom-specific questions.
4. Require a reason tied to a visible region.
5. Reject order-discordant judgments or send them to a second judge.

#### Self-preference and model-family preference

The foundational MT-Bench work identified position, verbosity, and self-enhancement biases in LLM judges, although that evidence is text-chat rather than UI-specific. [Zheng et al., 2023(https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)

A newer MLLM study using 1.29 million caption-score pairs reports self-preference and family-preference effects across 12 multimodal models; its ensemble mitigation reduced those effects. This is a preprint and not a UI-regression benchmark. [Koyama et al., 2026(https://arxiv.org/abs/2604.11589)](https://arxiv.org/abs/2604.11589)

`<INFERENCE from="self-preference evidence; model identity can correlate with output style">Never expose the judge to the generating model, prompt author, baseline filename, or implementation framework. If multiple judges are used, prefer different model families and report disagreement.</INFERENCE>`

#### Verbosity bias

The evidence for verbosity bias is strong in text judging but lacks a measured UI-screenshot equivalent. Longer UI text blocks may receive more attention than compact but correct controls, while dense screenshots may appear more “detailed” even when wrong.

`<INSUFFICIENT_EVIDENCE>Public studies did not provide a UI-specific effect size for verbosity bias, nor a reliable correction coefficient.</INSUFFICIENT_EVIDENCE>`

Operationally, avoid prompts such as “which screenshot is better?” Require fixed atom outputs:

```json
{
  "atom": "data",
  "verdict": "match | mismatch | unclear",
  "severity": "S0 | S1 | S2 | S3",
  "region": {"x": 0, "y": 0, "width": 0, "height": 0},
  "evidence": "short visible description",
  "confidence": "high | medium | low"
}
```

#### Image scale, resolution, cropping, and zoom

Higher resolution helps when the defect is a small icon, label, or control, but increased visual tokens also increase cost and latency. Apple’s FastVLM work explicitly describes this accuracy/compute trade-off for document and UI recognition. [Apple ML Research, FastVLM(https://machinelearning.apple.com/research/fast-vision-language-models)](https://machinelearning.apple.com/research/fast-vision-language-models)

Microsoft’s Phi-4-reasoning-vision evaluation showed ScreenSpot-Pro accuracy of 9.2% at 2048 visual tokens and 17.5% at 3600 visual tokens. [Microsoft Research, 2026(https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/)](https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/)

RegionFocus reported gains of more than 28 percentage points on ScreenSpot-Pro and more than 24 points on WebVoyager for GUI grounding, with Qwen2.5-VL-72B reaching 61.6% on ScreenSpot-Pro. These are grounding results, not defect-detection results. [Luo et al., ICCV 2025(https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf)](https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf)

A 2026 GUI-grounding study reported the following crop-ratio results for Qwen3-VL-8B on ScreenSpot-Pro:

| Crop scale | Reported accuracy | Change from uncropped |
|---|---:|---:|
| Full image | 53.51% | — |
| 2× zoom | 65.59% | +12.08 points |
| Approximately 3.3× zoom | 71.79% | +18.28 points |

[Spatially Stable GUI Grounding, 2026(https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf)](https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf)

A separate adaptive-zoom preprint reports gains of up to 13.4 points on ScreenSpot-Pro, 10.3 points on UI-Vision, and 4.2 points on ScreenSpot-v2; it also reports larger gains for icon and text targets. [UI-Zoomer, 2026(https://arxiv.org/abs/2604.14113)](https://arxiv.org/abs/2604.14113)

`<MISSING_DATA>Sought a direct benchmark measuring UI-regression defect recall, precision, or human agreement for full-page thumbnails versus 2–3× crops. The available public measurements evaluate GUI grounding or UI perception, not regression diagnosis.</MISSING_DATA>`

`<INFERENCE from="Phi-4 resolution results; RegionFocus; Spatially Stable GUI Grounding; UI-Zoomer">Use a two-pass schedule: one full-page scan for framing and global structure, followed by selective 2× and 3× crops for text, icons, controls, and spacing. Do not crop every region blindly: preserve a parent-context crop because local crops can hide sibling alignment, overflow, and viewport-level defects.</INFERENCE>`

#### Distinguishing legitimate variation from regression

| Apparent difference | Deterministic test | Classification |
|---|---|---|
| Different viewport or device-pixel ratio | Compare capture metadata to expected metadata | Framing; invalidate capture |
| Different route, auth, locale, theme, or scroll state | Compare route/state manifest | Framing/state; invalidate or fail |
| Different data fixture or timestamp | Compare fixture hash, seeded clock, and expected data | Legitimate only if declared; otherwise data regression |
| Different crop or full-page boundary | Compare crop rectangle and scroll offset | Framing; do not judge styling until normalized |
| Font/rendering/anti-aliasing variation | Same browser, OS/container, fonts, DPR; then use calibrated threshold | Usually rendering noise |
| Missing/extra control | DOM expectation plus VLM crop | Structural regression |
| Wrong copy or number | Test expectation, DOM/OCR, exact string comparison | Data regression |
| Mock differs from implementation but test passes | Compare against mock and label advisory | Mock-only finding; not a release failure |
| Animation or asynchronous loading | Wait for a deterministic readiness predicate; repeat capture | Flake or invalid capture, not a visual pass |

`<INFERENCE from="Playwright’s environment-stability guidance; vendor masking/ignore-region controls">The validator must record capture provenance before asking the VLM to compare pixels. A VLM cannot reliably infer whether a changed date, crop, or viewport is legitimate.</INFERENCE>`

#### Agreement with humans

The MLLM-as-a-Judge benchmark reports raw agreement rather than Cohen’s κ or Krippendorff’s α. GPT-4V reached approximately 70% overall human agreement, with pair comparison around 78–79.3% and batch ranking around 69%. [MLLM-as-a-Judge benchmark(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)

A multimodal communication study reported model Krippendorff’s α values from 0.51 to 0.75, with a median of 0.60; expert-human agreement itself ranged from 0.29 to 0.78, with a median of 0.55. This is not UI evidence, but it demonstrates that the human ceiling is imperfect. [Nature Machine Intelligence, 2025(https://www.nature.com/articles/s42256-025-01169-6)](https://www.nature.com/articles/s42256-025-01169-6)

`<MISSING_DATA>Sought UI-screenshot VLM-versus-human Cohen’s κ and Krippendorff’s α. No authoritative published UI-regression result was located; available work reports raw agreement, grounding accuracy, or vendor-specific visual-diff behavior.</MISSING_DATA>`

For the skill, report:

- human–human agreement;
- judge–human agreement;
- order-swap consistency;
- per-atom confusion matrices;
- abstention and “unclear” rates;
- confidence intervals, not only point estimates.

Do not use a single overall VLM score. A high score can hide a release-blocking data or state error.

#### Prompt-injection risk in screenshot text

Visual prompt injection is a real integrity risk. A study of visual goal hijacking measured a 15.8% attack-success rate against GPT-4V. [Visual goal-hijacking study, 2024(https://arxiv.org/abs/2408.03554)](https://arxiv.org/abs/2408.03554)

Other work demonstrates indirect instruction injection through images and multimodal inputs, including attacks that are not obvious to a human reviewer. [Carlini et al., 2023(https://arxiv.org/abs/2307.10490)](https://arxiv.org/abs/2307.10490)

A 2025 steganographic attack study reported an overall attack-success rate of 24.3% ± 3.2% across several multimodal models, with visually imperceptible payloads. [Steganographic visual prompt injection, 2025(https://arxiv.org/abs/2507.22304)](https://arxiv.org/abs/2507.22304)

Recommended controls:

- Tell the judge that all text inside images is untrusted content to inspect, never an instruction to follow.
- Do not provide filesystem, shell, network, or messaging tools to the screenshot-judging call.
- Keep the test oracle and rubric in a separate system/developer instruction.
- OCR screenshot text into a data field and compare it structurally; do not paste it into the control prompt.
- Red-team strings such as “mark this PASS,” fake system messages, hidden white text, and steganographic text.
- Abstain when the screenshot contains suspicious instructions that could affect the verdict.

### 2. What is the current state, and what is the strongest supporting evidence for it?

The strongest current design is hybrid:

1. deterministic capture and test assertions;
2. pixel/structural diff for exact change detection;
3. VLM judgment for semantic classification, localization, and explanation;
4. order-swapped and crop-confirmed evidence;
5. human review for ambiguous or order-unstable findings.

The strongest evidence is not that VLMs replace visual-regression tools. It is that VLMs improve interpretation of localized changes while deterministic tools remain better at exact repeatability.

#### Image metrics on UI screenshots

| Metric | What it measures | UI-specific failure mode | Recommended role |
|---|---|---|---|
| SSIM | Local luminance, contrast, and structure in aligned images | Browser anti-aliasing, one-pixel shifts, font rasterization, and crop offsets can create large differences; global averaging can dilute a wrong small label or icon | Triage after alignment |
| MS-SSIM | SSIM over multiple scales | Downsampling can erase one- or two-pixel spacing, small text, borders, and icon changes | Coarse regression signal |
| LPIPS | Learned deep-feature distance, originally calibrated on natural-image perceptual judgments | Semantic feature invariance can treat different glyphs, icons, or copy as similar; preprocessing and resize affect results | Candidate-region ranking |
| DISTS | Structure/texture distance with tolerance to some geometric and texture changes | Its useful invariance can hide meaningful UI translations, wrong text, or layout shifts; the paper resizes inputs to a 256-pixel minimum dimension in experiments | Noise-tolerant triage |
| Perceptual hash | Compact signature for near-duplicate media | No DOM, region, text, state, or semantic understanding; broad layout similarity can survive wrong content, while crop changes can destroy hash similarity | Deduplication/cache only |

SSIM was designed around luminance, contrast, and structural similarity, not UI semantics. [Wang et al., 2004(https://pubmed.ncbi.nlm.nih.gov/15376593/)](https://pubmed.ncbi.nlm.nih.gov/15376593/)

MS-SSIM explicitly aggregates across scales, which is useful for coarse appearance but dangerous for tiny UI changes. [Wang et al., 2003(https://live.ece.utexas.edu/publications/2003/zw_asil2003_msssim.pdf)](https://live.ece.utexas.edu/publications/2003/zw_asil2003_msssim.pdf)

LPIPS was developed for learned perceptual similarity on natural-image judgments, not exact UI typography or layout. [Zhang et al., 2018(https://arxiv.org/abs/1801.03924)](https://arxiv.org/abs/1801.03924)

DISTS intentionally combines structure and texture while becoming less sensitive to some geometric transformations and texture resampling. That is beneficial for photographs but can conceal UI movement. [Ding et al., 2020(https://arxiv.org/abs/2004.07728)](https://arxiv.org/abs/2004.07728)

pHash describes a perceptual signature of underlying media and is primarily useful for duplicate or near-duplicate detection. [pHash documentation(https://phash.org/docs/howto.html)](https://phash.org/docs/howto.html)

A screen-content IQA paper specifically notes that local single-level structure measures can be unreliable for screen content and that resizing feature maps introduces distortion. [Screen-content IQA, 2020(https://arxiv.org/abs/2008.05396)](https://arxiv.org/abs/2008.05396)

`<INFERENCE from="screen-content IQA; original metric objectives; known scale/alignment behavior">Use metrics as prescan signals to locate candidate changes, never as the final semantic gate. A test expectation should be checked with exact data/DOM assertions, while the VLM should classify the localized visual evidence.</INFERENCE>`

#### How existing tools handle anti-aliasing, dynamic data, and flake

| Tool | Anti-aliasing | Dynamic data | Flake handling | Limitation |
|---|---|---|---|---|
| Percy | Deterministic rendering and a visual engine intended to avoid anti-aliasing false positives | Ignore regions, frozen media, configurable sensitivity, and stabilization controls | Deterministic rendering and baseline review | Vendor documentation does not establish independent defect-recall rates |
| Chromatic | Ignores anti-aliased pixels by default; `diffIncludeAntiAliasing` can include them; default `diffThreshold` is 0.063 | Stable stories, masking, and controlled inputs | Unstable-test detection/flake filtering; recommends deterministic data and fonts | Threshold changes can hide subtle colour or position regressions |
| Applitools | Match levels and region types rather than only a global pixel threshold | Ignore, content, layout, floating, and dynamic match regions | Stabilization through match levels and targeted regions | Semantic behavior depends heavily on region configuration |
| Playwright `toHaveScreenshot` | Pixelmatch thresholding; `threshold` defaults to 0.2 YIQ; masks and stylesheets can remove volatile regions | User supplies masks, `stylePath`, deterministic fixtures, or waits | Captures until two consecutive screenshots match before comparison; same environment is required | No automatic semantic understanding of dynamic content |
| reg-suit | `matchingThreshold`, `thresholdPixel`, `thresholdRate`, and an `enableAntialias` option; ximgdiff reports structural changes | No native understanding of business-dynamic data; upstream stabilization/masking is required | CI comparison, baselines, reports, and external storage | Configuration-driven rather than semantic |

Chromatic documents a default `diffThreshold` of 0.063 and anti-aliased-pixel exclusion by default. [Chromatic threshold documentation(https://www.chromatic.com/docs/threshold/)](https://www.chromatic.com/docs/threshold/)

Chromatic separately documents animations, late fonts, dynamic data, and late resources as causes of unstable tests. [Chromatic unstable-test documentation(https://www.chromatic.com/docs/unstable-tests/)](https://www.chromatic.com/docs/unstable-tests/)

Percy documents deterministic pixel rendering and controls for anti-aliasing and dynamic regions. [Percy anti-aliasing changelog(https://percy.io/changelog/anti-aliasing)](https://percy.io/changelog/anti-aliasing)

Applitools documents `Content`, `Layout`, and `Ignore` match regions for separating content changes from geometry changes. [Applitools match regions(https://help.applitools.com/hc/en-us/articles/360007188151-Match-Regions)](https://help.applitools.com/hc/en-us/articles/360007188151-Match-Regions)

Playwright documents repeated screenshot capture, same-environment requirements, thresholds, masks, and style overrides. [Playwright screenshot assertions(https://playwright.dev/docs/next/test-snapshots)](https://playwright.dev/docs/next/test-snapshots)

reg-suit exposes pixel/color thresholds, anti-aliasing configuration, structural diff reporting, and cloud-storage plugins. [reg-suit repository(https://github.com/reg-viz/reg-suit)](https://github.com/reg-viz/reg-suit)

#### Candidate VLM backends

The following table is a capability and procurement comparison, not a benchmark ranking. Closed-model parameter counts and latency are not publicly disclosed.

| Model | Parameter count | Context window | Latency | API cost | License |
|---|---:|---:|---|---|---|
| GPT-5.6 Terra | Not disclosed | 1.05M tokens | Provider does not publish a fixed latency | $2/M input, $12/M output | Proprietary API |
| Claude Sonnet 4.6 | Not disclosed | 1M tokens | Provider does not publish a fixed latency | $3/M input, $15/M output | Proprietary API |
| Gemini 2.5 Flash | Not disclosed | 1,048,576 input tokens; 65,536 output tokens | Provider does not publish a fixed latency | $0.30/M input, $2.50/M output | Proprietary API |
| Gemini 2.5 Pro | Not disclosed | 1,048,576 input tokens; 65,536 output tokens | Provider does not publish a fixed latency | $1.25/M input up to 200k context, $2.50/M above; output $10/$15 | Proprietary API |
| Qwen2.5-VL-72B | 73B | 32,768 native; 64k YaRN extension with spatial-localization caveats | Hardware- and quantization-dependent | Self-hosting cost is hardware-dependent | Qwen License Agreement |

OpenAI’s current model documentation lists the GPT-5.6 Terra context and prices but not parameter count or fixed latency. [OpenAI model documentation(https://developers.openai.com/api/docs/models)](https://developers.openai.com/api/docs/models)

Anthropic lists Claude Sonnet 4.6 at $3/M input and $15/M output and documents 1M context for Claude 4.6 models. [Anthropic pricing documentation(https://platform.claude.com/docs/en/about-claude/pricing)](https://platform.claude.com/docs/en/about-claude/pricing)

Google lists Gemini 2.5 Flash and Pro context windows and prices in its model and pricing documentation. [Gemini API pricing(https://ai.google.dev/gemini-api/docs/pricing)](https://ai.google.dev/gemini-api/docs/pricing)

Qwen’s model card lists 73B parameters, native context limits, and the Qwen license terms. [Qwen2.5-VL-72B model card(https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct)](https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct)

### 3. What are the contrasting viewpoints or competing evidence?

#### Deterministic diff versus VLM judgment

The deterministic position is that visual regression is fundamentally an image-comparison problem: control rendering, compare pixels, and review differences. This is reproducible and well suited to one-pixel shifts, missing borders, and exact baselines.

The semantic position is that pixel diffs over-report anti-aliasing, font rasterization, dynamic data, and harmless rendering noise. A VLM can classify whether the changed region is a meaningful data, structure, style, or state change.

`<CONFLICTING_EVIDENCE>The two approaches optimize different errors. Deterministic tools provide repeatability and exact localization; VLMs provide semantic interpretation but introduce judge bias, scale sensitivity, and prompt-injection risk.</CONFLICTING_EVIDENCE>`

The correct resolution is not to choose one: use deterministic comparisons for the hard oracle and VLMs for interpretation.

#### Full-page context versus local crops

Full-page images preserve relationships among containers, siblings, responsive layout, and viewport boundaries. Crops make small text and icons legible and materially improve GUI-grounding accuracy in available studies.

`<INFERENCE from="crop-grounding improvements; missing direct defect-detection benchmark">Use both views. The full page is necessary for framing and global structure; 2–3× crops are necessary for fine-grained inspection.</INFERENCE>`

#### Single overall score versus decomposed atoms

A single score is attractive operationally but hides which failure occurred and is vulnerable to verbosity, position, and salience bias. Decomposed atoms make the oracle hierarchy explicit, support severity ranking, and allow test data differences to be separated from mock styling differences.

The MLLM benchmark found pair comparison more consistent than batch ranking, supporting pairwise, focused judgments over a single holistic ranking. [MLLM-as-a-Judge benchmark(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)

#### Vendor controls versus independent evidence

Vendors document useful controls for thresholds, masking, dynamic regions, and flake, but these documents establish product behavior, not independent comparative accuracy. A 2026 Web UI Image Change Captioning benchmark reports that web UI change description remains difficult because of dense text, layout diversity, and fine-grained changes, and notes that industry visual-regression tools lack broad public evaluation. [WUICC benchmark, 2026(https://arxiv.org/abs/2607.01728)](https://arxiv.org/abs/2607.01728)

### 4. What changed recently, and what is the trajectory?

- (High Confidence) 2023 established that LLM judges can reach human-like agreement in some text-chat settings while still exhibiting position, verbosity, and self-enhancement biases. [Zheng et al., 2023(https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)
- (High Confidence) 2024 multimodal judge work quantified imperfect human agreement and showed that pairwise comparison is more reliable than some ranking formats. [MLLM-as-a-Judge benchmark(https://mllm-judge.github.io/)](https://mllm-judge.github.io/)
- (High Confidence) 2025 work demonstrated that position bias remains systematic across capable judges and changes by task, model, and quality gap. [Shi et al., 2025(https://aclanthology.org/2025.ijcnlp-long.18.pdf)](https://aclanthology.org/2025.ijcnlp-long.18.pdf)
- (High Confidence) 2025 GUI-grounding work shifted toward region selection, visual test-time scaling, and adaptive crops rather than single-pass full-screen perception. [RegionFocus, ICCV 2025(https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf)](https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf)
- (Medium Confidence) 2026 work increasingly treats adaptive zoom as a selective operation: useful for small targets, harmful when applied indiscriminately because it adds latency and removes context. [UI-Zoomer, 2026(https://arxiv.org/abs/2604.14113)](https://arxiv.org/abs/2604.14113)
- (Medium Confidence) The trajectory is toward hybrid systems: deterministic capture and diffing, structured VLM critique, crop-based visual test-time scaling, and explicit instability handling. <INFERENCE from="WUICC benchmark; current visual-regression documentation; crop-grounding literature">This is an engineering synthesis, not a directly measured industry-wide outcome.</INFERENCE>

## Evidence Table

Sources were retained when they were peer-reviewed papers, benchmark papers/preprints with public measurements, official API/model documentation, or official product/repository documentation. Vendor documentation is used only to establish documented controls, not comparative efficacy.

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| LLM judges exhibit position, verbosity, and self-enhancement biases; GPT-4 can exceed 80% agreement in text-chat preference settings | Zheng et al., NeurIPS | 2023 | Peer-reviewed benchmark | [URL](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html) |
| GPT-4V pair-comparison agreement is approximately 78–79.3%; batch ranking is weaker | MLLM-as-a-Judge benchmark | 2024 | Public benchmark results | [URL](https://mllm-judge.github.io/) |
| Claude-3.5-Sonnet position consistency is 0.82/0.76 across two benchmarks | Shi et al. | 2025 | Peer-reviewed conference paper | [URL](https://aclanthology.org/2025.ijcnlp-long.18.pdf) |
| MLLMs show self- and family-preference bias over 1.29M caption-score pairs | Koyama et al. | 2026 | Preprint with measured corpus | [URL](https://arxiv.org/abs/2604.11589) |
| Higher visual-token resolution improved ScreenSpot-Pro from 9.2% to 17.5% in one Phi-4 evaluation | Microsoft Research | 2026 | Official engineering evaluation | [URL](https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/) |
| Region selection improved GUI grounding by more than 28 points on ScreenSpot-Pro and more than 24 on WebVoyager | Luo et al., RegionFocus | 2025 | ICCV paper | [URL](https://openaccess.thecvf.com/content/ICCV2025/papers/Luo_Visual_Test-time_Scaling_for_GUI_Agent_Grounding_ICCV2025_paper.pdf) |
| Approximately 2× and 3.3× crops improved ScreenSpot-Pro grounding by 12.08 and 18.28 points | Spatially Stable GUI Grounding | 2026 | OpenReview paper/preprint | [URL](https://openreview.net/pdf/879ebea95a8b126a2c27d04cd7567b9d4b2019f1.pdf) |
| Adaptive zoom reported gains up to 13.4 points on ScreenSpot-Pro | UI-Zoomer | 2026 | Preprint | [URL](https://arxiv.org/abs/2604.14113) |
| Web UI change captioning remains difficult because of dense text, layout diversity, and fine-grained changes | WUICC benchmark | 2026 | Preprint benchmark | [URL](https://arxiv.org/abs/2607.01728) |
| SSIM compares luminance, contrast, and structure | Wang et al. | 2004 | Peer-reviewed metric paper | [URL](https://pubmed.ncbi.nlm.nih.gov/15376593/) |
| MS-SSIM extends structural comparison across scales | Wang et al. | 2003 | Peer-reviewed metric paper | [URL](https://live.ece.utexas.edu/publications/2003/zw_asil2003_msssim.pdf) |
| LPIPS is a learned perceptual metric calibrated primarily on natural-image judgments | Zhang et al. | 2018 | CVPR paper | [URL](https://arxiv.org/abs/1801.03924) |
| DISTS combines structure and texture and tolerates some geometric changes | Ding et al. | 2020 | Peer-reviewed metric paper | [URL](https://arxiv.org/abs/2004.07728) |
| pHash provides perceptual signatures suitable for duplicate/near-duplicate detection | pHash project | Current | Official documentation | [URL](https://phash.org/docs/howto.html) |
| Chromatic uses a 0.063 default diff threshold and excludes anti-aliased pixels by default | Chromatic | Current | Official product documentation | [URL](https://www.chromatic.com/docs/threshold/) |
| Chromatic identifies animation, fonts, dynamic data, and late resources as instability causes | Chromatic | Current | Official product documentation | [URL](https://www.chromatic.com/docs/unstable-tests/) |
| Applitools provides content, layout, ignore, and dynamic match regions | Applitools | Current | Official product documentation | [URL](https://help.applitools.com/hc/en-us/articles/360007188151-Match-Regions) |
| Percy documents deterministic rendering and anti-aliasing controls | Percy | Current | Official product changelog | [URL](https://percy.io/changelog/anti-aliasing) |
| Playwright waits for two consecutive matching screenshots and supports masks, styles, and thresholds | Playwright | Current | Official documentation | [URL](https://playwright.dev/docs/next/test-snapshots) |
| reg-suit exposes pixel/color thresholds, anti-aliasing configuration, and structural diff reports | reg-suit | Current | Official repository | [URL](https://github.com/reg-viz/reg-suit) |
| Visual goal hijacking achieved 15.8% attack success against GPT-4V | Visual prompt injection study | 2024 | Preprint experiment | [URL](https://arxiv.org/abs/2408.03554) |
| Steganographic visual injection achieved 24.3% ± 3.2% overall attack success | Steganographic visual injection study | 2025 | Preprint experiment | [URL](https://arxiv.org/abs/2507.22304) |
| Multimodal model-human Krippendorff’s α ranged from 0.51 to 0.75 in an out-of-domain communication task | Nature Machine Intelligence study | 2025 | Peer-reviewed study | [URL](https://www.nature.com/articles/s42256-025-01169-6) |
| Current API context windows and prices for candidate judge models | OpenAI, Anthropic, Google, Qwen documentation | 2026/current | Official model/API documentation | [OpenAI](https://developers.openai.com/api/docs/models), [Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), [Google](https://ai.google.dev/gemini-api/docs/pricing), [Qwen](https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct) |

## Knowledge Gaps

### Direct measurement gaps

- <MISSING_DATA>There is no located public benchmark of full-page-thumbnail versus 2–3× crop defect recall and precision for web UI visual regression.</MISSING_DATA>
- <MISSING_DATA>There is no located public UI-specific VLM-as-judge dataset reporting Cohen’s κ or Krippendorff’s α against human labels.</MISSING_DATA>
- <MISSING_DATA>There is no independent, cross-vendor benchmark comparing Percy, Chromatic, Applitools, Playwright, and reg-suit on anti-aliasing false positives, dynamic-data false positives, and flake rates.</MISSING_DATA>

### Calibration gaps

- Thresholds for “minor” versus “major” UI differences are product- and viewport-dependent.
- The impact of different browsers, fonts, operating systems, device-pixel ratios, and GPU rendering paths needs local measurement.
- VLM performance may differ substantially by screenshot density, language, design system, and defect type.

### Model-operation gaps

- Closed-model parameter counts and p50/p95 image latency are not publicly disclosed.
- Published API prices do not capture image-tokenization differences, retries, crop count, or order-swapped calls.
- Prompt-injection attack rates are domain- and payload-dependent; no universal mitigation rate is established.

## Recommended Next Steps

1. Build a stratified gold set covering framing, data, structure, styling, and state defects, including legitimate viewport/data/crop differences. Double-label it with humans and measure κ/α, confusion matrices, and order-swap stability.

2. Implement the capture preflight manifest: route, viewport, DPR, browser, fonts, locale, theme, auth state, scroll position, fixture hash, readiness predicate, and crop rectangle.

3. Add a selective crop schedule: full-page scan, then 2× and 3× crops for VLM-identified regions, plus one parent-context crop. Record whether each crop confirms, weakens, or contradicts the global finding.

4. Run a local model bakeoff using the candidate table. Measure per-atom recall, false-positive rate, abstention, order consistency, p50/p95 latency, token cost, and prompt-injection susceptibility—not overall similarity.

5. Feed the resulting false-positive and false-negative rates into `evidence.md` and revise prescan thresholds empirically. Keep mock-only differences advisory and preserve the test expectation as the release gate.
