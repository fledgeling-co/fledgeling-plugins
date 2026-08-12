---
title: "Validating VLM UI Screenshot Judgement Design Decisions"
run_id: dr_b266c481b9a87f39
question: "How should an AI agent validate a UI screenshot against a test's expected output and a design mock using vision-language-model judgement? Required with measured numbers and primary sources: (1) VLM-as-judge failure modes on UI images specifically — position bias magnitude and how order-swapping mitigates it, self-preference, verbosity bias, and sensitivity to image resolution and downscaling; (2) does cropping or zooming into regions measurably improve UI defect detection versus judging a full-page image, and by how much; (3) how to separate legitimate differences (different data, crop, viewport, anti-aliasing) from genuine visual regressions; (4) where SSIM, MS-SSIM, LPIPS, DISTS and perceptual hashes each fail on UI screenshots as opposed to natural images; (5) how Percy, Chromatic, Applitools, Playwright toMatchSnapshot and reg-suit actually handle anti-aliasing, dynamic content and flake, with their documented thresholds; (6) decomposed rubric atoms versus a single overall score, and inter-rater agreement achieved against human labels (Cohen's kappa, Krippendorff's alpha); (7) measured attack success rates for prompt injection delivered through text rendered inside an image."
provider: local-claude
model: Claude Code
tier: max
archetype: technical
sources: 46
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 0.00
completed: 2026-08-11T07:51:57.662Z
---
# UI Screenshot Validation with VLM Judgement — Evidence Panel

## Executive Summary

- **(High Confidence)** Every one of the skill's five design decisions survives the evidence, but three of them are currently specified in the wrong units. "Crop to 2–3×" should become **"crop so the region's long edge lands at or under the model's no-resize ceiling (1568 px standard tier, 2576 px on Claude 4.7+), and so body text renders at ≥7 px"** — the 7 px figure is the measured cliff below which VLM text reading collapses [LLaVAR, arXiv:2306.17107](https://arxiv.org/pdf/2306.17107), and the resize ceilings are documented API behaviour [Anthropic vision docs](https://platform.claude.com/docs/en/docs/build-with-claude/vision).

- **(High Confidence)** Order-swapping is not optional hygiene, it is the single largest measurable error source. Across 36 models on a controlled paired-preference benchmark the **model-average order-flip rate is 43.0%**, the first-shown pick rate is **64.3%**, and the absolute first-position lift is **15.7 percentage points** [lechmazur/position_bias](https://github.com/lechmazur/position_bias). Position bias is "strongly affected by the quality gap between solutions" [Shi et al., arXiv:2406.07791](https://arxiv.org/abs/2406.07791) — i.e. worst exactly where a screenshot nearly matches its mock. **Treating a flip as inconclusive is correct and should be strengthened to a hard gate.**

- **(High Confidence)** Cropping produces the largest measured gain of any intervention in this report. On ScreenSpot-Pro (screenshots above 1080p, targets averaging 0.07% of screen area), OS-Atlas-7B scores **18.9% on the full screenshot and 48.1% under region-focused search — +29.2 points, a "254% relative improvement"**, with a crop-size ablation of 512²=25.1%, 768²=34.2%, **1024²=40.2%**, 1280²=40.1% [Li et al., ScreenSpot-Pro, arXiv:2504.07981](https://arxiv.org/html/2504.07981v1). This is grounding, not defect detection — see the inference caveat in §2.

- **(High Confidence)** A deterministic pre-scan is justified in exactly one direction. On the WUICC-bench visual-regression benchmark, naive pixel diff scores **change-accuracy 100.00% / no-change-accuracy 0.00%**, and with a 0.1 threshold plus anti-aliasing tolerance **97.93% / 6.72%** [Beyond Pixel Diffs, arXiv:2607.01728](https://arxiv.org/html/2607.01728). Pixel comparison is a near-perfect *detector* and a worthless *discriminator*: use it to prove "not blank / not identical", never to adjudicate.

- **(High Confidence)** The skill's five difference classes map almost exactly onto an independently-derived 37-rule taxonomy whose non-meaningful branch is **geometric shifts, dynamic content, pure style** and whose meaningful branch is **missing / added elements, attribute modification, layout change, reordering, resizing, content update, thematic change, replacement**, built with Cohen's κ = 0.722 [arXiv:2607.01728](https://arxiv.org/html/2607.01728). Adopt those rule names as the class definitions rather than the current ad-hoc five.

- **(Medium Confidence)** Decomposed binary atoms beat a single score, but the gain is modest and the ceiling is human disagreement. Checklist decomposition lifts judge–human exact agreement **46.4% → 52.2%** and human inter-annotator agreement **0.194 → 0.256** [TICK, arXiv:2410.03608](https://arxiv.org/html/2410.03608). On UI design preference specifically, **20 professional designers reach Krippendorff's α = 0.25** on binary preference, falling to **α = 0.104 / κ = 0.114 on a four-way scale** [DesignPref](https://www.researchgate.net/publication/397983364_DesignPref_Capturing_Personal_Preferences_in_Visual_Design_Generation). Benchmark against human–human agreement, not against 1.0.

- **(High Confidence)** Treating rendered text as untrusted is correct and under-stated. Typographic injection lifted attack success **5% → 77%** on MM-SafetyBench and reaches **82.50% average ASR** across six open-source LVLMs [FigStep, AAAI 2025, arXiv:2311.05608](https://arxiv.org/abs/2311.05608); Anthropic measured **23.6% ASR unmitigated → 11.2% mitigated** across 123 browser test cases, with browser-specific vectors (hidden DOM fields, URL text, tab titles) at **35.7% → 0%** [Anthropic, Aug 2025](https://claude.com/blog/claude-for-chrome). VLMs also show a general **text-priority bias**, resolving text-vs-visual conflicts in favour of the text [arXiv:2504.01589](https://arxiv.org/abs/2504.01589).

- **(High Confidence)** Do not add chain-of-thought to the judging step by reflex. On MLLM-as-a-Judge, three-step CoT **degraded every similarity metric**: GPT-4V scoring 0.557 → 0.299, pairwise (no tie) 0.806 → 0.728, batch ranking 0.325 → 0.419 (worse), while reducing hallucination [Chen et al., ICML 2024](https://mllm-judge.github.io/).

---

## Adjudication of the skill's current design

| Skill decision | Verdict | The number that replaces the guess |
|---|---|---|
| Deterministic pre-scan for blank / skeleton / framing | **Confirmed, narrow it** | Pixel diff: 100.00% change-acc, **0.00% no-change-acc** → high-recall gate only, never an adjudicator [arXiv:2607.01728](https://arxiv.org/html/2607.01728) |
| Crop to 2–3× rather than judge a thumbnail | **Confirmed, re-unit it** | Crop long edge ≤ **1568 px** (standard) / **2576 px** (Claude 4.7+) so no downscale occurs [Anthropic docs](https://platform.claude.com/docs/en/docs/build-with-claude/vision); target ≥**7 px** text height [arXiv:2306.17107](https://arxiv.org/pdf/2306.17107); empirical crop optimum ~**1024²** [arXiv:2504.07981](https://arxiv.org/html/2504.07981v1) |
| Both orders; flips reported inconclusive | **Confirmed, strengthen to a gate** | **43.0%** average flip rate; **15.7 pp** first-position lift [position_bias](https://github.com/lechmazur/position_bias); bias peaks when candidates are close in quality [arXiv:2406.07791](https://arxiv.org/abs/2406.07791) |
| Classes: framing / data / structure / styling / state | **Confirmed, re-derive from the 37-rule taxonomy** | 9 meaningful + 3 non-meaningful categories, κ = 0.722 [arXiv:2607.01728](https://arxiv.org/html/2607.01728) |
| Image text is untrusted evidence | **Confirmed, escalate** | **82.50%** typographic ASR [FigStep](https://arxiv.org/abs/2311.05608); **23.6% → 11.2%** with mitigations [Anthropic](https://claude.com/blog/claude-for-chrome) |
| *(not currently in the skill)* single holistic score | **Overturn if present** | Pairwise **0.773** vs scoring Pearson **0.490** vs batch-ranking worst, same models same data [MLLM-as-a-Judge](https://mllm-judge.github.io/) |
| *(not currently in the skill)* CoT on the judge call | **Do not add** | GPT-4V scoring 0.557 → **0.299** with CoT [MLLM-as-a-Judge](https://mllm-judge.github.io/) |

---

## Detailed Findings

### 1. VLM-as-judge failure modes on UI images: position bias, self-preference, verbosity, resolution

**Position bias.** The canonical measurement is swap consistency — the share of pairwise verdicts unchanged when the two candidates are reordered. MT-Bench reported GPT-4 at **65.0% consistency with 30.0% of verdicts biased toward the first answer**, GPT-3.5 at 46.2%/50.0%, and Claude-v1 at **23.8% consistency with 75.0% first-position preference**, improving to 66.2%/51.2%/56.2% under a "rename" prompt variant [Zheng et al., arXiv:2306.05685](https://arxiv.org/pdf/2306.05685). The largest controlled study covers **15 LLM judges across MTBench and DevBench, 22 tasks, ~40 solution-generating models, over 150,000 evaluation instances**, and introduces repetition stability, position consistency and preference fairness as the metric triple; its two load-bearing findings are that position bias "is not due to random chance and varies significantly across judges and tasks", and that it is "weakly influenced by prompt component length but **strongly affected by the quality gap between solutions**" [Shi et al., arXiv:2406.07791](https://arxiv.org/abs/2406.07791).

<INFERENCE from="arXiv:2406.07791's finding that position bias scales with the closeness of the two candidates; the skill's task of comparing a screenshot against a near-identical mock">The screenshot-vs-mock comparison is the maximum-bias regime by construction: the two images are supposed to be nearly identical, so the quality gap is minimal, so position bias is at its worst. A skill that compares in one order only is operating precisely where the literature says single-order judgement is least trustworthy.</INFERENCE>

A recent 36-model benchmark that holds content constant and varies only display order gives the cleanest magnitudes: **"The model-average order-flip rate is 43.0%, and the median model flips in 41.3% of decisive two-view cases"**, **"the model-average first-shown pick rate is 64.3%, with a median of 65.4%"**, **"The model-average absolute first-position lift is 15.7 percentage points"**, and an average first-position rating bonus of **+0.271 on a 1-to-7 scale** [lechmazur/position_bias](https://github.com/lechmazur/position_bias). Direction is not universal — the same benchmark records Mistral Large 3 choosing the first-shown version only 27.4% of the time, i.e. a *last*-position bias.

<CONFLICTING_EVIDENCE>Swap-consistency figures span a wide range depending on task and era: 23.8–65.0% on MT-Bench's 80 pairs (2023), a reported 70.5–77.3% range in follow-up work, and a 57% consistency implied by the 43.0% flip rate in the 36-model 2026 benchmark. The disagreement is mostly task-driven — long-form outputs amplify inconsistency sharply — rather than a genuine dispute about whether the effect exists. No source reports swap consistency above ~80% for pairwise judging.</CONFLICTING_EVIDENCE> <CONFIDENCE:LOW>The specific 70.5% (GPT-3.5-Turbo) to 77.3% (Gemini-Pro) swap-consistency range surfaced in secondary summaries and could not be located verbatim in arXiv:2406.07791, which reports position *consistency* rather than swap consistency.</CONFIDENCE:LOW>

**Position bias in the multimodal setting specifically.** MLLM-as-a-Judge measured a degenerate form: given a batch-ranking prompt containing the sequence 'ABCD', **LLaVA replicated that sequence in 88.2% of responses**, falling to a "reduced Position Bias score of 53.3%" when a second in-context example was added [Chen et al., ICML 2024, arXiv:2402.04788](https://mllm-judge.github.io/). Follow-up multimodal work confirms order sensitivity persists and reports MLLMs as **more vulnerable to verbosity bias than to position bias** [MM-JudgeBias, arXiv:2604.18164](https://arxiv.org/pdf/2604.18164).

**Verbosity bias.** In the multimodal judge setting, artificially lengthening answers raised scores by **0.6 points (GPT-4V) and 0.75 points (Gemini)** on average [arXiv:2402.04788](https://mllm-judge.github.io/). <INFERENCE from="the 0.6–0.75 point verbosity lift; the skill's use of a VLM to compare a screenshot against a written test expectation">Verbosity bias transfers to this skill through the *textual* leg, not the image leg: a verbose expected-output description will pull the verdict toward "match" independent of the pixels. Fixed-length, atom-per-line expectations neutralise this; free-form prose expectations do not.</INFERENCE>

**Self-preference / egocentric bias.** GPT-4V was found to exhibit "a slight degree of Egocentricity" with no numeric magnitude given [arXiv:2402.04788](https://mllm-judge.github.io/). A later study quantifies it with a "philautia score": **all scores exceeded zero in the reference-based setting**, with InternVL2.5-8B highest at **3.02**; removing the reference *increased* self-preference for several models — LLaVA-OneVision-7B 1.19 → 1.83, Qwen2.5-VL-7B 0.49 → 1.12, DeepSeek-VL2 1.33 → 2.00, **GPT-4o 0.55 → 1.08** [arXiv:2604.11589](https://arxiv.org/pdf/2604.11589). The operational reading is that self-preference roughly doubles when the judge has no reference to anchor on — an argument for always supplying the mock even when it is advisory.

**Resolution and downscaling — the most encodable numbers in this report.** Claude's documented image pipeline: "Claude views images in patches instead of pixels. Each patch is a 28×28-pixel block… An image, therefore, costs `⌈width / 28⌉ × ⌈height / 28⌉` visual tokens." Resolution tiers are **high-resolution (Claude 4.7 and later): max long edge 2576 px, max 4784 visual tokens**, and **standard (all other models): max long edge 1568 px, max 1568 visual tokens**. "Images larger than either limit are downscaled before processing" preserving aspect ratio [Anthropic vision docs](https://platform.claude.com/docs/en/docs/build-with-claude/vision). Documented downscale outcomes:

| Source image | Standard tier → | Tokens | High-res tier → | Tokens |
|---|---|---|---|---|
| 1000×1000 | not resized | 1296 | not resized | 1296 |
| 1920×1080 | **1456×819** | 1560 | not resized | 2691 |
| 2000×1500 | **1269×952** | 1564 | not resized | 3888 |
| 3840×2160 | **1456×819** | 1560 | **2576×1449** | 4784 |

[Anthropic vision docs](https://platform.claude.com/docs/en/docs/build-with-claude/vision)

The same page states the failure mode directly: Claude "might hallucinate or make mistakes when interpreting low-quality, rotated, or **very small images under 200 pixels**", warns that "your image might be resized if it is too large… this might, for example, make text less legible", and that "heavy JPEG compression can make text difficult to read" [Anthropic vision docs](https://platform.claude.com/docs/en/docs/build-with-claude/vision).

The legibility cliff has been measured independently. Rescaling images so answer text height ranged from 3 to 19 pixels, **accuracy decreases sharply below 7 pixels of text height** for both 224²- and 336²-input models [LLaVAR, arXiv:2306.17107](https://arxiv.org/pdf/2306.17107). A DPI sweep on GPT-4.1 gives the same shape at document scale: word/character OCR accuracy **0.011/0.018 at 15 DPI → 0.644/0.693 at 30 DPI → 0.821/0.849 at 60 DPI → 0.934/0.956 at 120 DPI**, saturating at 0.985–0.990 by 150–300 DPI [arXiv:2605.07250](https://arxiv.org/pdf/2605.07250). Classical OCR shows a comparable ~6 px floor [arXiv:2506.06918](https://arxiv.org/pdf/2506.06918).

<INFERENCE from="Anthropic's documented 1568/2576 px long-edge ceilings and aspect-preserving downscale; the 7 px text-height cliff from LLaVAR">A full-page screenshot of a 1280 px-wide viewport running to 4320 px tall (the documented WUICC-bench maximum) is downscaled by 0.363× on the standard tier, rendering 14 px body text at ~5.1 px — below the 7 px cliff, i.e. structurally unreadable regardless of prompt. On the high-resolution tier the factor is 0.596× and the same text lands at ~8.3 px, marginally above the cliff. The same page cropped into 1280×720 viewport tiles is not downscaled at all (1280 < 1568), so text stays at 14 px — 2× the cliff. Cost of that choice: ~952 visual tokens for the unreadable full page versus ~1196 tokens per readable tile. This, not any prompt-engineering argument, is the mechanical case for the skill's crop step.</INFERENCE>

### 2. Does cropping or zooming measurably improve UI defect detection versus a full-page image, and by how much?

Yes, by the largest margin of any intervention surveyed — with a domain caveat.

ScreenSpot-Pro is the cleanest measurement because it deliberately isolates the resolution problem: screenshots captured "greater than 1080p (1920×1080)" with scaling off, targets averaging **0.07% of screen area versus 2.01% in ScreenSpot** (a ~29× reduction in relative size), and the paper reports "a universal decrease in accuracy as the target bounding box size becomes smaller" [arXiv:2504.07981](https://arxiv.org/html/2504.07981v1).

| Method (all on OS-Atlas-7B) | Accuracy | Delta vs full-image baseline |
|---|---|---|
| Full screenshot, end-to-end | 18.9% (28.1% text / 4.0% icon) | — |
| Iterative Focusing (3 iters) | 31.0% | +12.1 pp |
| Iterative Narrowing (3 iters) | 31.9% | +13.0 pp |
| ReGround (crop, planner-free) | 40.2% | +21.3 pp |
| **ScreenSeekeR (GPT-4o planner + recursive crop)** | **48.1%** (64.1% text / 22.4% icon) | **+29.2 pp, "254% relative improvement"** |

[arXiv:2504.07981](https://arxiv.org/html/2504.07981v1)

Crop size is not monotonic and is model-dependent — the single most important operational finding here:

| Crop size | OS-Atlas-7B | UGround-7B |
|---|---|---|
| 512² | 25.1% | 27.0% |
| 768² | 34.2% | **28.8%** |
| **1024²** | **40.2%** | 28.2% |
| 1280² | 40.1% | 26.3% |

[arXiv:2504.07981](https://arxiv.org/html/2504.07981v1). "Each model peaks at a different crop size; too-small crops lose context, too-large ones exceed capacity." Corroborating evidence: FocusUI reports **+3.7% over GUI-Actor-7B on ScreenSpot-Pro** from position-preserving token selection [arXiv:2601.03928](https://arxiv.org/html/2601.03928), and CropVLM adds a 256M-parameter learned cropper to a frozen VLM for gains on high-resolution benchmarks [CropVLM, CVPR 2026W, arXiv:2511.19820](https://arxiv.org/abs/2511.19820).

<INFERENCE from="ScreenSpot-Pro's +29.2 pp cropping gain on grounding; the shared mechanism of small-target-in-large-image; the 7 px text cliff">The ScreenSpot-Pro gains are measured on *grounding* (locating a named element), not on *defect detection* (judging whether a rendered element is correct). The transfer argument is that both tasks bottleneck on the same physical constraint — the target occupying too few post-downscale pixels — and the skill's targets (a mis-aligned border, a wrong shade, a truncated label) are typically smaller than a clickable control. The +29.2 pp figure should therefore be read as an upper bound on the achievable gain and as strong directional support, not as a defect-detection measurement.</INFERENCE>

<MISSING_DATA>No study was found that measures UI *defect detection* accuracy as a function of crop factor with everything else held constant. The nearest task-matched numbers are OwlEye's 85% precision / 84% recall for display-issue detection and 90% localisation accuracy on 4,470 labelled screenshots [Liu et al., ASE 2020, arXiv:2009.01417](https://arxiv.org/abs/2009.01417), but that is a purpose-trained CNN with no crop ablation. Closing this gap would need a crop-factor sweep on WUICC-bench or an equivalent.</MISSING_DATA>

A counter-signal worth recording: on ASCII art, "lower resolutions actually helped GPT-4o more accurately recognize visual patterns", the authors suggesting low resolution "may help VLMs by blurring fine textual details and emphasizing overall visual structures" [arXiv:2504.01589](https://arxiv.org/pdf/2504.01589). <INFERENCE from="the ASCII-art resolution inversion; the distinction between global-layout and local-detail judgements">This is a task-specific inversion, and it argues for the skill running *two* passes rather than one: a downscaled whole-page pass for framing/structure judgements, where global gestalt is the signal, and full-resolution crops for data/styling/state judgements, where glyph-level detail is the signal. Judging both from a single image size guarantees one of the two is at the wrong scale.</INFERENCE>

### 3. Separating legitimate differences (data, crop, viewport, anti-aliasing) from genuine visual regressions

The best available artefact is WUICC-bench, which exists specifically to make this separation measurable. It contains **9,906 samples (8,583 meaningful, 1,323 non-meaningful)** split ~70:10:20, built from a **37-rule taxonomy of 9 meaningful and 3 non-meaningful categories**, with pipeline reliability of **Cohen's Kappa 0.722** and generation accuracy **78.09%**; 12,949 of 19,812 screenshots (65.4%) are 1280×720, all rendered at 1280 px viewport width with heights up to 4320 px [arXiv:2607.01728](https://arxiv.org/html/2607.01728).

The taxonomy is directly transplantable into the skill's difference classes:

| Branch | Categories (verbatim rule intents) | Maps to skill class |
|---|---|---|
| **Non-meaningful** — geometric shifts (rules 31–33) | "Apply small positional shifts", "Apply minor spacing or padding adjustments", "Apply subtle alignment changes" | framing |
| **Non-meaningful** — dynamic content (rule 34) | "Update transient content such as usernames, dates, or counters" | data |
| **Non-meaningful** — pure style (rules 35–37) | "Apply small color adjustments", "Apply subtle font-size or font-weight changes", "Apply subtle typography variations" | styling (advisory) |
| **Meaningful** (rules 1–30) | missing elements, adding elements, attribute modification, layout changes, reordering, resizing, content update, thematic changes, replacement | structure / state / styling (blocking) |

[arXiv:2607.01728](https://arxiv.org/html/2607.01728)

The paper draws one boundary the skill should copy verbatim: **thematic changes are global-intentional (e.g. a light-to-dark switch) and count as meaningful, while a single shadow tweak is local-cosmetic noise** [arXiv:2607.01728](https://arxiv.org/html/2607.01728). Scope, not magnitude, decides the class.

The measured separation performance is the decisive result:

| Method | No-Change Accuracy (noise suppression) | Change Accuracy (regression recall) |
|---|---|---|
| Pixel Diff (no tolerance) | **0.00** | **100.00** |
| Pixel Diff (0.1 threshold + AA tolerance) | **6.72** | 97.93 |
| SEN (trained CNN) | 96.27 | 96.16 |
| ICT-Net | 97.01 | 93.80 |
| RSICCformer | 85.82 | 95.33 |
| RMNet | 97.39 | 93.55 |
| **Llama-3.2-11B-Vision-Instruct (zero-shot)** | **21.64** | 79.39 |
| **Qwen2-VL-7B-Instruct (zero-shot)** | **99.63** | **65.68** |

[arXiv:2607.01728](https://arxiv.org/html/2607.01728). The authors' conclusion: off-the-shelf VLMs "do not yet provide the selective suppression VRT needs" — **Qwen over-suppresses, Llama under-suppresses**, and adding anti-aliasing tolerance to pixel diff "lifts suppression by fewer than seven points while beginning to lose genuine changes."

<INFERENCE from="pixel diff at 100.00/0.00 and 97.93/6.72; zero-shot VLMs at 79.39/21.64 and 65.68/99.63; trained models at ~96/96">Three architectural consequences for the skill. (i) The deterministic pre-scan is validated only as a high-recall gate — at 0.00% no-change accuracy it cannot rule anything in, but at 100% change accuracy an *absence* of pixel difference is conclusive proof of no regression, and a blank/skeleton frame is exactly the case where the deterministic signal is unambiguous. (ii) The two zero-shot VLM results straddle the useful operating point in opposite directions, meaning a single VLM verdict on "is this difference real" inherits whichever bias that model has; the skill's difference *classes* are the correction, because forcing the model to name the class before ruling makes the over/under-suppression visible instead of latent. (iii) Nothing in the evidence supports a VLM replacing the pixel stage — the two are complementary, with pixel diff supplying recall and the VLM supplying suppression.</INFERENCE>

<MISSING_DATA>No published evaluation reports production false-positive rates for commercial visual-AI tools against pixel diff on the same suite. The benchmark paper notes commercial tools "are proprietary and lack public evaluation" [arXiv:2607.01728](https://arxiv.org/html/2607.01728). Industry figures of "20–40% pixel-diff false-positive rates" and "up to 95% false-alert reduction" appear only in vendor and vendor-adjacent content marketing with no published methodology — `[SECONDARY: promotional]`, not usable as evidence.</MISSING_DATA>

### 4. Where SSIM, MS-SSIM, LPIPS, DISTS and perceptual hashes fail on UI screenshots specifically

The general failure is that all five were designed and validated on natural-image statistics, while a UI screenshot is dominated by sharp, non-natural edges, large flat regions, and glyph strokes where a few pixels carry all the semantics.

**SSIM / MS-SSIM.** SSIM "assumes local image structures are equally important across the image", a poor fit for screenshots where a large flat background dominates the mean while a truncated label decides pass/fail. The screen-content compression literature is blunter: authors state they are "reluctant to use MS-SSIM as a perceptual metric because it is obviously not aligned with visual quality", noting that in the CLIC codec competition **the best human-rated codec had almost the worst MS-SSIM** — measured on the SCI1K screen-content dataset [PICD, arXiv:2505.05853](https://arxiv.org/pdf/2505.05853). The existence of an entire dedicated SCI-QA literature — SIQAD (20 references, 980 distorted images, 7 distortion types), SCID (40 references, 1800 distorted) and metrics SIQM, SQMS, GSS, ESIM built by *patching* SSIM rather than adopting it — is itself the evidence that the natural-image metrics underperform [Screen content IQA using CNNs, Sig. Proc. Image Comm.](https://www.sciencedirect.com/science/article/abs/pii/S1047320319303669). Measured on SIQAD, general natural-image no-reference metrics reach **NIQE 0.482 SROCC / 0.500 LCC and IL-NIQE 0.517 / 0.540**, versus 0.702/0.721 and 0.725/0.735 for screen-content-trained models [ibid.](https://www.sciencedirect.com/science/article/abs/pii/S1047320319303669).

**LPIPS.** Two independent failure modes. It is not adversarially robust: constructed image pairs show that "the ε-LPIPS ball around a source image contains images wildly different from it", and conversely that attack images "visually highly similar to the source" produce large LPIPS increases [E-LPIPS, arXiv:1906.03973](https://arxiv.org/pdf/1906.03973). And it is a full-reference metric on text: work on text-aware restoration finds FR metrics (PSNR, SSIM, LPIPS, DISTS) penalise *improvements* in character sharpness because those increase deviation from a soft ground truth, and critically that this holds **"even when you isolate the text — even when restored text is structurally accurate, FR scores remain low on cropped text regions"** [arXiv:2512.08922](https://arxiv.org/pdf/2512.08922).

**DISTS.** DISTS is "an adaptation of LPIPS giving more focus on texture" and is deliberately tolerant of texture *resampling* [arXiv:2505.05853](https://arxiv.org/pdf/2505.05853). <INFERENCE from="DISTS' documented texture-resampling invariance; the fact that glyph anti-aliasing and font rendering are texture-like at the patch level">Texture invariance is precisely the wrong invariance for UI validation: a font substitution, a weight change, and a rendering-engine difference all present as texture resampling at the patch scale, so DISTS will tolerate the first two (genuine regressions) for the same reason it tolerates the third (legitimate noise). It cannot be tuned to separate them because the invariance is baked into the architecture.</INFERENCE>

**Perceptual hashes.** <MISSING_DATA>No peer-reviewed evaluation of pHash/dHash/aHash on UI screenshots was located. The structural objection — that perceptual hashes operate on an 8×8 or 32×32 DCT-reduced representation, which for a 1280 px-wide screenshot discards every element smaller than ~40 px and all text — follows from the algorithms' definition but has not been measured on screenshots in any source found. Treat any pHash threshold in the skill as unsupported.</MISSING_DATA>

**What the UI-specific literature uses instead.** Design2Code declines to use a single perceptual metric at all. It computes CLIP-ViT-B/32 similarity **only after inpainting out all detected text boxes (Telea 2004)** so text is excluded from the visual comparison, then adds four element-matching metrics: Block-Match (matched area ratio via bounding-box detection + Jonker-Volgenant optimal pairing), Text similarity (Sørensen-Dice character overlap), Colour similarity (CIEDE2000), and Position similarity. Correlation with human judgement ranges **0.3461 to 0.7605**, and the authors "deliberately do not combine these into an aggregate score" [Si et al., Design2Code, arXiv:2403.03163](https://arxiv.org/pdf/2403.03163). Reported GPT-4V scores: Block-Match 0.624, Text 0.977, Position 0.779, Colour 0.707, CLIP 0.892 [Design2Code repo](https://github.com/NoviScl/Design2Code).

<CONFLICTING_EVIDENCE>Design2Code validated CLIP similarity as correlating with human judgement (up to ρ=0.7605); UI2Code^N reports that reinforcement-learning ablations show "VLM rewards consistently outperform CLIP-based ones", arguing that "purely visual similarity signals are insufficient for capturing the semantic and structural fidelity required in UI-to-code generation and may even misguide optimization" [arXiv:2511.08195](https://arxiv.org/html/2511.08195v2). The positions are reconcilable — CLIP is adequate for *ranking systems* in aggregate and inadequate as a *per-instance reward* — but they should not be collapsed.</CONFLICTING_EVIDENCE>

### 5. What Percy, Chromatic, Applitools, Playwright and reg-suit actually do

| Tool | Difference metric | Documented default threshold | Anti-aliasing | Dynamic content | Flake controls |
|---|---|---|---|---|---|
| **Playwright `toHaveScreenshot`** | "acceptable perceived color difference in the **YIQ color space** between the same pixel" | **`threshold: 0.2`** ("between zero (strict) and one (lax)"); `maxDiffPixels` **unset**; `maxDiffPixelRatio` **unset** | **Not mentioned anywhere in the API page** | `mask` (overlays `#FF00FF`, "also applied to invisible elements"), `stylePath` (pierces Shadow DOM) | `animations: "disabled"` default — finite animations fast-forwarded, infinite cancelled to initial state; `caret: "hide"` default [Playwright docs](https://playwright.dev/docs/api/class-pageassertions) |
| **Chromatic** | "color distance in a 3D color space (YIQ)" at the same (x,y) | **`diffThreshold: .063`**, range 0–1, "balances high visual accuracy with low false positives" | **`diffIncludeAntiAliasing` off by default** — "Chromatic detects anti-aliased pixels and ignores them to prevent false positives" | story/component/project-level threshold scoping | Warns `0.8` "may prevent Chromatic from detecting positioning changes"; notes no "1 pixel = 1 threshold" correspondence due to DPI/gamut variation [Chromatic docs](https://www.chromatic.com/docs/threshold/) |
| **pixelmatch** (the underlying library) | **OKLab** + HyAB colour difference (Ottosson 2020; Abasi et al. 2019) | **`threshold: 0.1`** | **`includeAA: false` by default** — i.e. AA pixels detected and excluded; algorithm cited as **Vyšniauskas 2009, "Anti-aliased pixel and intensity slope detector"** | — | — [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch) |
| **reg-suit** | `matchingThreshold` = "YUV color distance between two pixels", 0–1 | **`thresholdRate: 0`, `thresholdPixel: 0`, `matchingThreshold: 0`** (most sensitive) | **`enableAntialias: false` by default** (AA *not* ignored) | — | `concurrency: 4`; `ximgdiff` for report detail [reg-suit README](https://github.com/reg-viz/reg-suit/blob/master/README.md) |
| **Percy** | Named tiers only | Project: **Strict / Recommended / Relaxed**; per-snapshot: Strict / Moderately strict / Recommended / Moderately relaxed / Relaxed. **"Currently, this setting only affects sensitivity to color differences."** | Strict = "highlight every pixel difference, including image artifacts and font smoothing/antialiasing"; **Safari always renders Relaxed** due to non-deterministic rendering | **Intelli-Ignore** (auto-ignores dynamic content); Percy CSS | Freezes animations and GIFs at capture [Percy diff sensitivity docs](https://www.browserstack.com/docs/percy/project-settings/diff-sensitivity) [Percy snapshot rules](https://www.browserstack.com/docs/percy/build-results/snapshot-rules) |
| **Applitools Eyes** | Match levels, no numeric threshold | **Strict is the default** — "verifies that the page content matches the baseline closely enough that the human eye would not see any difference… while ignoring differences in pixel values that are platform dependent due to the rendering software and hardware" | Handled implicitly by Strict/Content/Layout; only **Exact** (explicitly "not recommended") surfaces AA | **Layout** level "checks only the layout and ignores actual text and graphics" — recommended for dynamic content, localisation, cross-platform; Match Regions apply a different level to a sub-region | Explicitly rejects thresholds: other tools' pixel-count thresholds are called "unreliable and arbitrary" [Applitools match levels](https://applitools.com/tutorials/concepts/best-practices/match-levels) |

Two findings here matter more than the table.

**The tools disagree by 6× on the same metric.** Chromatic's `.063` and Playwright's `0.2` are both "colour distance in YIQ, 0–1", yet Chromatic's default is over three times stricter — and Chromatic ignores anti-aliasing by default while Playwright's API page never mentions it. reg-suit's default of `0` is stricter still, with AA detection *off*. <INFERENCE from="the three documented YIQ/threshold defaults of 0, 0.063 and 0.2 and their differing AA behaviour">There is no consensus numeric threshold to inherit. Any threshold the skill hard-codes is a choice, not a standard, and it must be paired with a stated anti-aliasing policy or it is uninterpretable — a `0.1` threshold with AA ignored and a `0.1` threshold with AA counted are different tests.</INFERENCE>

**Playwright's documented colour space may be stale.** Playwright's page states YIQ; the current pixelmatch README documents **OKLab with the HyAB metric** and cites Ottosson (2020) and Abasi et al. (2019) [pixelmatch](https://github.com/mapbox/pixelmatch) [Playwright](https://playwright.dev/docs/api/class-pageassertions). <CONFIDENCE:LOW>The most likely explanation is that Playwright bundles a pixelmatch version predating the OKLab change, or that its docs lag the dependency. Either way, a `threshold` value tuned against one colour space does not transfer to the other, and the skill should not assume Playwright's 0.2 and pixelmatch's 0.1 are measuring the same quantity.</CONFIDENCE:LOW>

### 6. Decomposed rubric atoms versus a single overall score, and measured agreement with humans

**Decomposition wins, modestly and consistently.** TICK generates instruction-specific checklists decomposing an instruction into YES/NO questions; using it "leads to an increase (**46.4% → 52.2%**) in the frequency of exact agreements between LLM judgements and human preferences, compared to having an LLM directly score an output" — **+5.8 points absolute**. Handing the same generated checklists to *human* evaluators "notably increased inter-annotator agreement (**0.194 → 0.256**)" [TICK, arXiv:2410.03608](https://arxiv.org/html/2410.03608).

**The multimodal evidence is stronger than the text-only evidence.** On the same models, same data, MLLM-as-a-Judge shows a large task-format effect: GPT-4V reaches **0.773 average on pairwise comparison without ties** but only **0.490 average Pearson similarity on absolute scoring** and the worst performance on batch ranking (**0.361 normalised Levenshtein**); six-repeat consistency is **0.675 pairwise, 0.611 scoring, 0.418 batch ranking** [arXiv:2402.04788](https://mllm-judge.github.io/). The paper's summary is that MLLMs "show human-like discernment in Pair Comparison but diverge significantly from human preferences in Scoring Evaluation and Batch Ranking."

<INFERENCE from="pairwise 0.773 vs scoring 0.490 vs batch-ranking worst; consistency 0.675 vs 0.611 vs 0.418; TICK's YES/NO decomposition gain">The reliability ordering is binary/pairwise > graded score > ranked list, on both accuracy and self-consistency, in the multimodal setting. A rubric of binary atoms is therefore two design choices at once — decomposition *and* binarisation — and the evidence supports both independently. A 1–5 "overall fidelity" score is the worst available format on this evidence.</INFERENCE>

Corroboration for binarisation: one rubric benchmark reports "the shift from ternary to binary evaluation increasing agreement by roughly 20 percentage points, suggesting partial credit introduces ambiguity without improving discriminative power", against HealthBench's **0.709 Macro F1** grader–physician agreement baseline [ResearchRubrics, arXiv:2511.07685](https://arxiv.org/pdf/2511.07685). <CONFIDENCE:LOW>The ~20 pp ternary→binary figure was located in a secondary summary of that paper rather than verbatim in the primary text.</CONFIDENCE:LOW>

**The human ceiling is the number that should reset expectations.** On UI design preference, DesignPref collected **12,000 pairwise comparisons from 20 professional designers** and found "substantial levels of disagreement exists (**Krippendorff's alpha = 0.25** for binary preferences)", degrading on four-way labels to **agreement 0.386, κ 0.114, α 0.104**; written rationales showed that "even when designers appeal to similar concepts such as hierarchy or cleanliness, they differ in how they define, prioritize, and apply those concepts" — which led those authors *away* from rubrics toward per-annotator personalisation [DesignPref](https://www.researchgate.net/publication/397983364_DesignPref_Capturing_Personal_Preferences_in_Visual_Design_Generation).

A design-domain equivalence study gives matched expert–expert baselines and VLM performance against them, using weighted Cohen's κ (quadratic) plus ICC rather than α:

| Criterion | Expert–expert κ/ICC | Expert–expert MAE | Best VLM judge (GPT-4o + image + o1 reasoning) |
|---|---|---|---|
| Uniqueness | 0.54 | 1.10 | κ 0.49 (Expert 1) / 0.52 (Expert 2); 8/9 and 9/9 equivalence tests passed |
| Creativity | 0.26 | 1.25 | κ 0.22; 5/9 and 7/9 tests |
| Drawing quality | 0.33 | 1.16 | 8/9 against both experts (avg 8.33/9 and 7.33/9 across runs) |
| Usefulness | 0.59/0.60 | 1.00 | 4/9 and 3/9 — **no judge cleared this metric** |

[AI Judges in Design, arXiv:2504.00938](https://ar5iv.labs.arxiv.org/html/2504.00938). The pattern — VLM judges reach expert equivalence on perceptual criteria (uniqueness, drawing quality) and fail on the criterion requiring domain reasoning (usefulness) — is the most transferable finding for the skill.

**Report the right statistic.** With complete binary judge panels "Krippendorff's α and κ determine each other exactly"; with nominal labels, fixed annotations per item and no missing judgements, "nominal Krippendorff's α is mathematically equivalent to Fleiss' κ." The aggregation protocol is not neutral: "micro-averaging pools every item–criterion verdict, macro-averaging computes per-criterion scores and averages them, and item-level aggregation first combines criterion verdicts into one score. Protocol choice alone can move reported accuracy and shift κ across zero without altering a single verdict." Under skewed label distributions — the normal case for a pass-heavy screenshot suite — "α and Cohen's κ may be deflated by prevalence effects even when judges match frequently" [Agreement Measurement for Rubric-based LLM Judges, arXiv:2606.00093](https://arxiv.org/html/2606.00093).

<INFERENCE from="DesignPref α=0.25 among expert designers; the prevalence-deflation warning; the divergence between item-level and system-level agreement">A screenshot-validation skill will operate on a heavily pass-skewed distribution, where κ and α are deflated by prevalence and a raw-agreement figure alone is inflated by it. The defensible reporting form is therefore three numbers together — raw agreement, a chance-corrected statistic, and the human–human value on the same items — and the target is parity with human–human agreement, not with 1.0. On aesthetic criteria that target may be as low as α≈0.25.</INFERENCE>

<CONFLICTING_EVIDENCE>Item-level and system-level agreement can diverge sharply. CHIRP finds GPT-4V achieves only "slight" to "fair" chance-corrected agreement on open-ended VLM evaluation while "exhibiting very similar trends to human evaluations" [CHIRP, arXiv:2501.09672](https://arxiv.org/pdf/2501.09672), and UI2Code^N reports human vs VLM net-win margins correlating at **Pearson 0.93, Spearman 1.0** at the system level despite weak per-item agreement [arXiv:2511.08195](https://arxiv.org/html/2511.08195v2). A judge can be reliable for ranking builds and unreliable for adjudicating any single screenshot. For a per-test gate, the item-level statistic is the one that binds.</CONFLICTING_EVIDENCE>

### 7. Measured attack success rates for prompt injection delivered through text rendered inside an image

The attack works, at rates that make "treat rendered text as untrusted" the only defensible policy.

| Attack / benchmark | Target | Measured ASR | Source |
|---|---|---|---|
| MM-SafetyBench typographic | safety-aligned LVLMs | **5% → 77%** | [MM-SafetyBench](https://www.emergentmind.com/topics/mm-safetybench-benchmark) |
| FigStep | 6 open-source LVLMs, SafeBench | **82.50% average** (vs 44.80% for vanilla text queries; per-model increase spans 1.80%–78.80%) | [FigStep, AAAI 2025](https://arxiv.org/abs/2311.05608) |
| FigStep / FigStep-Pro | GPT-4V | **34% → 70%** | [ibid.](https://arxiv.org/abs/2311.05608) |
| Image-based Prompt Injection (IPI) | GPT-4-turbo, COCO, 12 prompt strategies | **up to 64%** under human-imperceptibility constraints | [arXiv:2603.03637](https://arxiv.org/abs/2603.03637) |
| Mind-map imagery injection | modern LLMs | **90%** (vs 30.5% best baseline) | [Electronics 14(10):1907](https://www.mdpi.com/2079-9292/14/10/1907) |
| Lingua-SafetyBench by image type | multilingual VLMs | pure visual **21.21%**, typography-only **35.50%**, mixed **40.05%** | [arXiv:2601.22737](https://arxiv.org/html/2601.22737) |
| **Anthropic browser red-team** | Claude for Chrome, 123 test cases / 29 scenarios, autonomous mode | **23.6% unmitigated → 11.2% mitigated** | [Anthropic, Aug 2025](https://claude.com/blog/claude-for-chrome) |
| **Anthropic browser-specific vectors** (hidden DOM form fields, URL text, tab titles) | same | **35.7% → 0%** | [ibid.](https://claude.com/blog/claude-for-chrome) |
| Anthropic current configuration | Claude Opus 4.8 + two classifiers | **<0.08%** against internal combined-technique testing | [Anthropic support](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely) |
| SCAM (utility degradation, not jailbreak) | 99 vision-language models | **up to 42% degradation**; average **26 pp** accuracy drop; individual range 2.67–66.37 pp | [arXiv:2604.12371](https://arxiv.org/abs/2604.12371) |

Two rendering parameters have been isolated. Font size matters non-monotonically: across 1,000 SALAD-Bench prompts on GPT-4o, Claude Sonnet 4.5, Mistral-Large-3 and Qwen3-VL-4B under 6–28 px fonts, **"6px fonts yield near-zero ASR while mid-range fonts peak"** [arXiv:2604.12371](https://arxiv.org/abs/2604.12371). <INFERENCE from="the 6 px near-zero-ASR floor and the 7 px LLaVAR legibility cliff">These are the same threshold seen from two directions — injected text stops working at roughly the size where the model stops being able to read text at all. Consequently, the skill's crop step, which exists to push text *above* the legibility floor, simultaneously pushes any injected text into its effective range. The mitigation for injection cannot be "keep the resolution low", because that would defeat the crop; it has to be a policy rule about how in-image text is used.</INFERENCE>

The underlying disposition is measured independently of any attack: adversarial ASCII art where character-level semantics contradict the global visual pattern shows that **"VLMs consistently prioritize textual information over visual patterns, with visual recognition ability declining dramatically as semantic complexity increases"**, across five state-of-the-art models including GPT-4o, Claude and Gemini, and "various mitigation attempts through visual parameter tuning and prompt engineering yielded only modest improvements, suggesting the limitation requires architectural-level intervention" [arXiv:2504.01589](https://arxiv.org/abs/2504.01589).

<INFERENCE from="the text-priority bias finding; the 82.50% typographic ASR; the fact that a UI screenshot is mostly rendered text by area">A UI screenshot is the worst case for this failure mode, because unlike a natural photograph almost all of its semantic content *is* rendered text, so there is no visual channel for the model to fall back on when the text is adversarial. The operational rule that follows is stronger than "untrusted": in-image text may be quoted as observed evidence ("the button reads 'Submit'") but must never be executed as instruction, and any in-image string that reads as an instruction is itself a reportable finding of the highest severity — because a mock or a test fixture has no legitimate reason to contain one.</INFERENCE>

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---|---|---|
| Model-average order-flip 43.0%; first-shown pick 64.3%; first-position lift 15.7 pp; 36 models | lechmazur/position_bias | 2026 (live) | Controlled benchmark | https://github.com/lechmazur/position_bias |
| Position bias "strongly affected by the quality gap between solutions"; 15 judges, 150k+ instances | Shi, Ma, Liang, Diao, Ma, Vosoughi | 12 Jun 2024, rev. 11 Nov 2025 | Peer-reviewed study | https://arxiv.org/abs/2406.07791 |
| GPT-4 65.0% swap consistency / 30.0% first-biased; Claude-v1 23.8% / 75.0% | Zheng et al., MT-Bench | 2023 | Benchmark paper | https://arxiv.org/pdf/2306.05685 |
| LLaVA replicates 'ABCD' 88.2% → 53.3% with 2 examples; verbosity +0.6/+0.75 pts; pairwise 0.773 vs scoring 0.490; CoT degrades all metrics | Chen et al., MLLM-as-a-Judge, ICML 2024 | Feb 2024 | Peer-reviewed benchmark | https://mllm-judge.github.io/ |
| Philautia self-preference >0 for all MLLMs; InternVL2.5-8B 3.02; GPT-4o 0.55→1.08 reference-free | MLLM-as-a-Judge Exhibits Model Preference Bias | 2026 | arXiv study | https://arxiv.org/pdf/2604.11589 |
| Patch = 28×28 px; standard tier 1568 px/1568 tokens; high-res 2576 px/4784 tokens; documented downscale table; errors "under 200 pixels" | Anthropic, Vision docs | current | Official documentation | https://platform.claude.com/docs/en/docs/build-with-claude/vision |
| Accuracy "sharply decreasing when the height is smaller than 7 pixels" | LLaVAR | Jun 2023 | Peer-reviewed | https://arxiv.org/pdf/2306.17107 |
| GPT-4.1 OCR word accuracy 0.011 @15 DPI → 0.934 @120 DPI → ~0.99 @150–300 DPI | Hard to Read, Easy to Jailbreak | 2026 | arXiv study | https://arxiv.org/pdf/2605.07250 |
| OS-Atlas-7B 18.9% → 48.1% with region search (+29.2 pp, "254%"); crop ablation 512²/768²/1024²/1280² = 25.1/34.2/40.2/40.1 | Li et al., ScreenSpot-Pro | Apr 2025 | Benchmark paper | https://arxiv.org/html/2504.07981v1 |
| CropVLM: 256M learned cropper on frozen VLM improves high-res understanding | Carvalho et al., CVPR 2026W | Nov 2025 | Peer-reviewed | https://arxiv.org/abs/2511.19820 |
| FocusUI +3.7% over GUI-Actor-7B on ScreenSpot-Pro; naive token pruning "yields severe accuracy drops" | FocusUI | Jan 2026 | arXiv study | https://arxiv.org/html/2601.03928 |
| WUICC-bench: 9,906 samples, 37-rule taxonomy (9 meaningful + 3 non-meaningful), κ=0.722; pixel diff 100.00/0.00 and 97.93/6.72; Qwen2-VL 65.68/99.63; Llama-3.2-11B 79.39/21.64 | Beyond Pixel Diffs | 2026 | Benchmark paper | https://arxiv.org/html/2607.01728 |
| pixelmatch: threshold 0.1, includeAA false, Vyšniauskas 2009 AA detector, OKLab + HyAB | mapbox/pixelmatch | current | Source repository | https://github.com/mapbox/pixelmatch |
| Playwright: threshold 0.2 YIQ, maxDiffPixels unset, animations "disabled", caret "hide", mask #FF00FF | Playwright API reference | current | Official documentation | https://playwright.dev/docs/api/class-pageassertions |
| Chromatic: diffThreshold .063, YIQ 3D, AA ignored by default, 0.8 "may prevent detecting positioning changes" | Chromatic docs | current | Official documentation | https://www.chromatic.com/docs/threshold/ |
| reg-suit: thresholdRate 0, thresholdPixel 0, matchingThreshold 0 (YUV), enableAntialias false | reg-viz/reg-suit README | current | Source repository | https://github.com/reg-viz/reg-suit/blob/master/README.md |
| Percy: Strict/Recommended/Relaxed tiers; "only affects sensitivity to color differences"; Safari always Relaxed | BrowserStack Percy docs | current | Official documentation | https://www.browserstack.com/docs/percy/project-settings/diff-sensitivity |
| Applitools: Strict default ignores "platform dependent" rendering; Layout for dynamic content; Exact "not recommended" | Applitools docs | current | Official documentation | https://applitools.com/tutorials/concepts/best-practices/match-levels |
| MS-SSIM "obviously not aligned with visual quality"; CLIC best human-rated codec had almost worst MS-SSIM (SCI1K) | PICD | May 2025 | arXiv study | https://arxiv.org/pdf/2505.05853 |
| FR metrics penalise sharper text even on cropped text regions | Unified Diffusion Transformer for Text-Aware Restoration | Dec 2025 | arXiv study | https://arxiv.org/pdf/2512.08922 |
| ε-LPIPS ball contains "wildly different" images; visually-similar attack images raise LPIPS | E-LPIPS | Jun 2019 | Peer-reviewed | https://arxiv.org/pdf/1906.03973 |
| SIQAD: NIQE 0.482 SROCC/0.500 LCC vs SCI-trained CNN-SWA 0.725/0.735; SIQAD 20/980, SCID 40/1800 | Screen content IQA using CNNs | 2019 | Peer-reviewed | https://www.sciencedirect.com/science/article/abs/pii/S1047320319303669 |
| Design2Code: CLIP with text inpainted out; Block-Match/Text/Position/Colour; human correlation 0.3461–0.7605; no aggregate score | Si et al., Design2Code | Mar 2024 | Benchmark paper | https://arxiv.org/pdf/2403.03163 |
| TICK: 46.4% → 52.2% judge–human exact agreement; human IAA 0.194 → 0.256 | Cook et al., TICK | Oct 2024 | Peer-reviewed | https://arxiv.org/html/2410.03608 |
| DesignPref: 12k comparisons, 20 designers, α=0.25 binary; 4-way α=0.104, κ=0.114 | DesignPref | 2025 | Dataset paper | https://www.researchgate.net/publication/397983364_DesignPref_Capturing_Personal_Preferences_in_Visual_Design_Generation |
| Expert–expert weighted κ/ICC 0.54/0.26/0.59/0.33; VLM judge reaches equivalence on uniqueness + drawing quality, fails usefulness | AI Judges in Design | Apr 2025 | arXiv study | https://ar5iv.labs.arxiv.org/html/2504.00938 |
| Aggregation protocol "can move reported accuracy and shift κ across zero"; α ≡ Fleiss' κ under stated conditions; prevalence deflation | Agreement Measurement for Rubric-based LLM Judges | 2026 | arXiv study | https://arxiv.org/html/2606.00093 |
| FigStep 82.50% avg ASR on 6 LVLMs; GPT-4V 34% → 70% with FigStep-Pro; vanilla text 44.80% | Gong et al., FigStep, AAAI 2025 | Nov 2023, rev. Jan 2025 | Peer-reviewed | https://arxiv.org/abs/2311.05608 |
| 123 test cases / 29 scenarios; 23.6% → 11.2% ASR; browser-specific 35.7% → 0% | Anthropic, Piloting Claude in Chrome | Aug 2025 | Vendor primary red-team | https://claude.com/blog/claude-for-chrome |
| Claude Opus 4.8 + two classifiers: "<0.08%" ASR on internal combined-technique testing | Anthropic support | current | Vendor documentation | https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely |
| VLMs "consistently prioritize textual information over visual patterns"; mitigation via prompting yields "only modest improvements" | Wang et al., Text Speaks Louder than Vision | Apr 2025 | Peer-reviewed | https://arxiv.org/abs/2504.01589 |
| 6 px fonts near-zero ASR, mid-range peaks; 1,000 SALAD-Bench prompts across 4 frontier models | Reading Between the Pixels | 2026 | arXiv study | https://arxiv.org/abs/2604.12371 |
| OwlEye: 85% precision, 84% recall detecting UI display issues; 90% localisation accuracy; 4,470 labelled screenshots | Liu et al., ASE 2020 | Sep 2020 | Peer-reviewed | https://arxiv.org/abs/2009.01417 |
| AgentRewardBench: 1,302 expert-annotated trajectories, 5 benchmarks, 12 LLM judges; rule-based eval "underreports the success rate" | Lù et al. | Apr 2025 | Benchmark paper | https://arxiv.org/abs/2504.08942 |

---

## Knowledge Gaps

**Measured but not for this exact task.** The +29.2 pp cropping gain is measured on *element grounding*, not on *defect detection*; the transfer is argued mechanically (small post-downscale target size) but not demonstrated. No source sweeps crop factor against UI defect-detection accuracy. <MISSING_DATA>What was sought: an ablation of crop factor (1×, 2×, 3×, region-only) against defect detection F1 on a labelled UI-regression set. What is available: crop-size ablations for grounding (ScreenSpot-Pro) and defect-detection accuracy with no crop ablation (OwlEye, WUICC-bench). What would be needed: running WUICC-bench's test split at several crop factors through a frontier VLM.</MISSING_DATA>

**Not published at all.** <MISSING_DATA>Percy exposes no numeric threshold, only named tiers, and explicitly states the setting "only affects sensitivity to color differences" — so its geometry tolerance is undocumented. Applitools publishes no numeric parameters for Strict/Content/Layout at all, by stated design. Neither vendor has published an evaluation of its ML comparison against pixel diff on a shared suite; the academic benchmark that would use one notes both are "proprietary and lack public evaluation".</MISSING_DATA>

**Structurally absent.** <MISSING_DATA>No evaluation of perceptual hashes (pHash/dHash/aHash) on UI screenshots was found in any form. Any pHash threshold in the skill is currently unsupported by evidence.</MISSING_DATA>

**Retrievable but not retrieved.** AgentRewardBench's per-judge precision figures, its rule-based-evaluator comparison, and any screenshot ablation live in the paper's results tables; the abstract, project page and PDF-to-text extraction all failed to surface them. <INSUFFICIENT_EVIDENCE>The claim that "including screenshots in the judge input measurably improves or degrades web-agent trajectory judging" could not be corroborated — the ablation may not exist. The judge-input composition (first and last screenshots + accessibility tree + action list) is documented in downstream work, but its measured contribution is not.</INSUFFICIENT_EVIDENCE>

**Contested rather than missing.** Item-level versus system-level agreement diverge (CHIRP "slight-to-fair" κ alongside UI2Code^N's Pearson 0.93 / Spearman 1.0), and CLIP's validity as a UI similarity signal is affirmed by Design2Code and disputed by UI2Code^N. Both are recorded in §4 and §6 rather than resolved.

**Version drift.** The Playwright-documented YIQ colour space versus pixelmatch's current OKLab/HyAB implementation is an unreconciled discrepancy between two primary sources; it was not possible to determine which pixelmatch version Playwright bundles from documentation alone.

---

## Recommended Next Steps

1. **Instrument the skill's own crop rule against the resize ceilings before changing anything else.** Compute, for the repo's actual screenshot sizes, the post-downscale body-text height on both the standard (1568 px) and high-resolution (2576 px) tiers, and set the crop rule to whatever keeps that above 7 px. *Rationale:* this converts the current guessed "2–3×" into the only threshold in this report that is both documented by the model vendor and independently validated by a measured perceptual cliff, and it is computable from existing fixtures without new experiments.

2. **Run a crop-factor sweep on WUICC-bench's 1,961-item test split.** Feed the same pairs at full-page, half-page and viewport-tile granularity through the judge and record no-change accuracy and change accuracy at each. *Rationale:* this is the one gap that separates a mechanically-argued design choice from a measured one, the benchmark already carries the meaningful/non-meaningful labels the skill needs, and the two zero-shot VLM rows (99.63/65.68 and 21.64/79.39) give ready-made comparison points for whether the skill's prompt sits at a better operating point than a bare model call.

3. **Calibrate the flip-gate cost against the measured 43% flip rate on the repo's own pass-skewed data.** Sample ~100 real screenshot/expectation pairs, judge each in both orders, and record the flip rate and the prevalence of "pass". *Rationale:* a 43% flip rate would make a strict inconclusive-on-flip gate escalate nearly half of all comparisons, which may be unaffordable; the repo's flip rate on near-identical pairs is the number that decides whether the gate is a hard block, a tie-break third call, or a confidence annotation — and it also yields the raw-agreement/κ/human-human triple that §6 says must be reported together.

4. **Reconcile the Playwright/pixelmatch colour-space discrepancy in the repo's own harness.** Check which pixelmatch version `@playwright/test` resolves to and whether its threshold operates in YIQ or OKLab. *Rationale:* the deterministic pre-scan's threshold is uninterpretable until this is settled, and the repo already runs Playwright screenshot assertions, so a stale-threshold assumption is live in CI today, not hypothetical.

5. **Add an in-image-instruction detector as a first-class finding, not a guard.** Before any judging, scan the screenshot's OCR output for imperative language directed at a model, and fail the comparison loudly if found. *Rationale:* the 82.50% typographic ASR and Anthropic's 35.7%→0% browser-vector result both show that the effective defence is a dedicated classifier rather than judge-side instructions, and §7's inference is that a mock or fixture containing such a string is itself a defect worth surfacing — so the detector earns its place twice.
