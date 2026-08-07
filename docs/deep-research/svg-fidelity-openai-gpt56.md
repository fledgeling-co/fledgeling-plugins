---
title: "Hybrid inverse-rendering pipelines for raster-to-SVG icon generation"
run_id: dr_1c3ac1c8c061b864
question: "How can an LLM-driven pipeline generate hand-authored SVG icons that match the detail, fidelity and material quality of raster (diffusion-generated) reference icons, and how should an automated eval loop score and iteratively close the gap? Cover: (1) state of the art in LLM/text-to-SVG and image-to-SVG generation 2023-2026 (e.g. StarVector, OmniSVG, IconShop, LLM4SVG, Chat2SVG, Arrow-class models), their measured fidelity ceilings, and what architecturally limits SVG realism (gradients, filters, mesh-like shading, path counts); (2) differentiable/optimisation vectorization for matching a raster target (DiffVG, LIVE, VectorFusion, SVGDreamer and successors) and hybrid approaches combining LLM authoring with optimisation refinement; (3) automated perceptual metrics suitable for icon-scale SVG-vs-raster comparison (LPIPS, DISTS, SSIM/MS-SSIM, CLIP similarity, VLM-as-judge rubrics), their reliability at 1024px and at small sizes (128/32/16), and eval protocols for render-compare-edit iterative refinement loops with a vision model in the loop; (4) evidence on VLM-guided iterative SVG editing/critique loops (agentic render-inspect-edit), convergence behaviour, and known failure modes (plateau, oscillation, metric gaming); (5) distillation: methods and evidence for training or fine-tuning a vector-generation model from a stronger model's outputs (synthetic SVG corpora, rejection sampling, preference optimisation on visual fidelity), including dataset scale/format needed and what it would take to beat a commercial text-to-SVG model of Arrow 1.1's class."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: technical
sources: 43
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-07T12:48:41.104Z
---
## Executive Summary

- **(High Confidence)** An LLM alone will not reliably reproduce the *material* quality of diffusion-raster icon references. The practical architecture is a **hybrid inverse-rendering pipeline**: LLM/VLM creates a layered semantic SVG scaffold; a renderer-in-the-loop critic diagnoses residuals; differentiable or black-box optimisation fits geometry, colour, gradients, opacity, shadows, and highlights to the raster target; acceptance is decided by multi-scale perceptual and structural gates. This matches the division of strengths demonstrated by Chat2SVG, RLRF, Render-in-the-Loop, and RefineSVG. [CVPR 2025 Chat2SVG paper](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.pdf) ([openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.pdf?utm_source=openai)) [RLRF paper](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) [Render-in-the-Loop paper](https://arxiv.org/abs/2604.20730) ([arxiv.org](https://arxiv.org/abs/2604.20730)) [RefineSVG paper](https://arxiv.org/abs/2607.27699) ([arxiv.org](https://arxiv.org/abs/2607.27699))

- **(High Confidence)** “SVG realism” is principally a **representation, grammar, and optimisation-budget** problem—not an inherent limitation of SVG. Native SVG can express gradients, masks, compositing, blur, lighting, displacement, and turbulence filters; however, prominent autoregressive research models simplify SVG into paths, fills, and a few geometric commands, deliberately discarding many of those material controls. OmniSVG, for example, canonicalizes assets to `M/L/C/A/Z` commands plus fill tokens. [OmniSVG, NeurIPS 2025](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263)) [W3C Filter Effects Module Level 1](https://www.w3.org/TR/filter-effects-1/) ([w3.org](https://www.w3.org/TR/filter-effects-1/?utm_source=openai))

- **(High Confidence)** For image-to-SVG reconstruction, direct vectorisers still establish the pixel-fidelity ceiling on many benchmarks: OmniSVG reports icon-set LPIPS `0.050` versus VTracer `0.039`; on its more complex illustration subset, OmniSVG-8B reports LPIPS `0.231`, versus DiffVG `0.065` and VTracer `0.035`. These figures are not universal rankings, but they demonstrate that clean autoregressive SVG remains materially behind dense/trace-style reconstruction on complex raster targets. [OmniSVG Table 2](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263))

- **(High Confidence)** The eval harness should not use a single score. Use a **multi-resolution Pareto gate** across `1024`, `128`, `32`, and `16` px: LPIPS/DISTS for high-resolution material similarity; MS-SSIM plus edge/silhouette measures for small icon legibility; DINO/CLIP only for semantic guardrails; and a reference-aware VLM rubric for visible defects that numerical metrics miss. Pixel metrics alone can mis-rank thin-stroke SVGs, while semantic metrics can approve the wrong geometry. [RLRF metric analysis and SVG-Icons caveat](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) [LPIPS](https://doi.org/10.1109/cvpr.2018.00068) ([doi.org](https://doi.org/10.1109/cvpr.2018.00068?utm_source=openai)) [DISTS](https://doi.org/10.1109/TPAMI.2020.3045810) ([cns.nyu.edu](https://www.cns.nyu.edu/~lcv/pubs/makeAbs.php?loc=Ding20&utm_source=openai))

- **(Medium Confidence)** Render-inspect-edit loops do converge when the model is trained or constrained to use visual feedback, but naïvely handing a rendered intermediate image back to a general VLM can fail or worsen fidelity. Render-in-the-Loop reports GPT-5 illustration LPIPS worsening from `0.345` to `0.388` under naïve intermediate-image feedback; its trained visual-self-feedback plus render-and-verify design improves results and prevents repetitive drawing loops. [Render-in-the-Loop](https://arxiv.org/pdf/2604.20730) ([arxiv.org](https://arxiv.org/pdf/2604.20730))

- **(High Confidence)** Distillation should treat strong LLM outputs as **proposal data, not ground truth**. Train on accepted `(reference raster, prompt, SVG, render, decomposition, metric vector, critic diagnosis)` trajectories; perform rejection sampling against the full eval suite; then use preference optimisation or rendering-reward RL. RLRF shows a strong precedent: `1.7M` SVG-supervised pairs for SFT followed by rendering-feedback RL on only `16k` high-detail samples materially improved Qwen2.5-VL models. [RLRF training data and compute details](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2))

- **(High Confidence)** Do not claim that a new model “beats Arrow 1.1” until it wins a frozen, hidden, target-domain benchmark against Arrow 1.1 and Arrow 1.1 Max under identical prompts, input images, renderer, SVG restrictions, output-token budget, and latency budget. Arrow 1.1’s provider documentation exposes API controls but no public parameter count, training corpus, independent benchmark, latency SLA, or reproducible quality figures. [Arrow 1.1 provider page](https://vercel.com/ai-gateway/models/arrow-1.1/about) ([vercel.com](https://vercel.com/ai-gateway/models/arrow-1.1/about)) [QuiverAI integration documentation](https://www.promptfoo.dev/docs/providers/quiverai/) ([promptfoo.dev](https://www.promptfoo.dev/docs/providers/quiverai/))

---

## Detailed Findings

### 1. How can an LLM-driven pipeline generate hand-authored SVG icons that match raster reference icons, and how should an automated eval loop close the gap?

#### Decisive recommendation

**Use an LLM as a structured illustrator and code editor, not as the final raster matcher.** The production loop should be:

1. **Normalize the raster reference** into a deterministic target render.
2. **Plan an icon scene graph**: silhouette, layers, materials, lighting direction, occlusion order, shadow groups, highlight groups.
3. **Generate a constrained, editable SVG scaffold** with semantic groups and named material primitives.
4. **Render the SVG identically at multiple sizes.**
5. **Compute residual maps and multi-scale scores.**
6. **Ask a VLM critic for localized, non-overlapping edit instructions.**
7. **Apply one bounded edit class at a time**: composition, silhouette, internal geometry, material, or micro-detail.
8. **Run continuous optimisation only on the affected layer parameters**, then accept/reject using a Pareto gate.
9. **Stop when gains are below a calibrated threshold or edits violate small-size legibility/editability constraints.**

<INFERENCE from="[Chat2SVG’s LLM-template plus diffusion-guided path optimisation; RLRF’s rendering rewards; Render-in-the-Loop’s visual self-feedback and path-verification; SVG’s native filter/gradient capability]">A hybrid system is required because discrete SVG-program decisions—layer decomposition, path topology, filter choice, and paint-server assignment—are suitable for an LLM/VLM, whereas sub-pixel control points, stops, opacities, and blur radii are better optimised against the raster target.</INFERENCE> [Chat2SVG](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.pdf) ([openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.pdf?utm_source=openai)) [RLRF](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) [Render-in-the-Loop](https://arxiv.org/abs/2604.20730) ([arxiv.org](https://arxiv.org/abs/2604.20730))

#### Recommended system architecture

| Stage | Required artifact | Primary mechanism | Acceptance condition | Why it exists |
|---|---|---|---|---|
| A. Reference normalization | `target_1024.png`, alpha mask, edge map, colour-managed variants | Fixed browser renderer; premultiplied RGBA; deterministic background handling | Render reproducibility hash matches | Prevents renderer, alpha, and anti-aliasing differences from appearing as model defects. |
| B. Scene decomposition | JSON layer plan | VLM/LLM with raster reference | Every visible major part assigned to exactly one layer group | LLMs are better at semantic decomposition than raw numeric fitting. |
| C. Scaffold authoring | Layered SVG | Claude Code or equivalent coding agent under a restricted SVG grammar | Valid SVG; no clipped content; semantic groups present | Produces editability and a stable optimisation target. |
| D. Material pass | `<defs>` gradients, masks, filters, highlight/shadow groups | LLM proposes; numerical optimiser tunes parameters | High-resolution material score improves without harming 32/16 px scores | Diffusion references commonly need soft shadows, specular highlights, translucency, and non-flat colour. |
| E. Geometric refinement | Local path-control-point deltas | DiffVG-like differentiable refinement or bounded black-box search | LPIPS/DISTS and edge alignment improve in edited ROI | Performs the fine placement an autoregressive model commonly misses. |
| F. Critique/edit loop | Structured defect list | Separate VLM judge and generator | Candidate passes Pareto gate; no metric gaming | Separates generation from evaluation and retains rollback. |
| G. Export hygiene | Final SVG + render bundle | SVG sanitizer, structural linter, browser render test | Valid XML; no raster embedding; path/filter budgets met | Preserves “hand-authored,” editable, portable output. |

**Confidence: High** for the architectural decomposition; its individual components are supported by current SVG-generation and rendering-feedback research, although the exact combined stack has not been independently benchmarked on macOS-icon fixtures. [Chat2SVG abstract and method](https://arxiv.org/abs/2411.16602) ([arxiv.org](https://arxiv.org/abs/2411.16602?utm_source=openai)) [RLRF](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2))

#### Required SVG representation: permit materials, constrain chaos

A clean SVG grammar should allow:

- semantic groups: `<g id="base">`, `<g id="object">`, `<g id="shadow">`, `<g id="highlight">`;
- paths, circles, ellipses, rounded rectangles, polygons, lines, text only when needed;
- linear and radial gradients with explicit stop positions;
- clipping paths and masks;
- bounded SVG filters for soft shadows, bloom, blur, local grain, and controlled displacement;
- explicit `viewBox`, opacity, compositing, and paint order;
- local reusable `<defs>`.

The grammar should **forbid by default**:

- embedded raster `<image>` content;
- arbitrary JavaScript, external CSS, external hrefs, and remote fonts;
- unbounded filter regions;
- thousands of one-purpose microscopic paths;
- global post-processing filters that improve 1024 px appearance while destroying 16 px clarity.

SVG filters can express blur, compositing, colour matrices, convolution, lighting, morphology, turbulence, and displacement. The W3C specification also warns that some filter operations can impose high processing cost or clip when their filter region is too small. [SVG Filter Effects specification](https://www.w3.org/TR/SVG11/filters.html) ([w3.org](https://www.w3.org/TR/SVG11/filters.html?utm_source=openai))

**Confidence: High:** The key realism limitation in current models is usually *their canonical syntax and training data*, not SVG expressiveness. OmniSVG removes groups, transforms, and general attributes during simplification, retaining five path commands and fills; that makes autoregression tractable but reduces direct capacity for semantic grouping and material effects. [OmniSVG SVG simplification and tokenizer](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263))

#### State of the art: direct LLM/VLM SVG generation and fidelity ceilings

| System | Year / status | Architecture | Measured results reported by source | Ceiling / limitation relevant to raster-class icons |
|---|---:|---|---|---|
| IconShop | 2023, SIGGRAPH Asia | Autoregressive transformer over sequentialized SVG path tokens and text | Reports stronger quantitative and diversity performance than contemporaneous image- and language-based baselines, but the abstract does not provide a direct raster-reconstruction metric. [IconShop](https://arxiv.org/abs/2304.14400) ([arxiv.org](https://arxiv.org/abs/2304.14400?utm_source=openai)) | Icon-oriented and path-token-centric; limited material realism and full SVG feature coverage. |
| StarVector | 2025, CVPR | CLIP-like visual encoding plus StarCoder-family code generation; SVG-Stack `2M` samples | Open models at `1B` and `8B`; designed for image-to-SVG, text-to-SVG, and diagrams. [StarVector](https://arxiv.org/abs/2312.11556) ([arxiv.org](https://arxiv.org/abs/2312.11556?utm_source=openai)) | Strong structured primitives and semantic compactness; later benchmarks show a gap versus high-fidelity tracing on complex images. |
| LLM4SVG | 2025, CVPR | SVG-special tokens added to LLMs; text and optional rendered-image conditioning | On the authors’ text-to-SVG benchmark, GPT-2-XL variant: FID `64.11`, CLIP `0.3496`, aesthetic `5.9836`, HPS `0.2485`, generation time `18s`; SVGDreamer in that table: FID `72.68`, `43m56s`. [LLM4SVG Table 2](https://arxiv.org/pdf/2412.11102) ([arxiv.org](https://arxiv.org/pdf/2412.11102)) | Direct code generation is faster and more structured, but the authors state it may not surpass optimisation-based visual quality. [LLM4SVG qualitative discussion](https://arxiv.org/pdf/2412.11102) ([arxiv.org](https://arxiv.org/pdf/2412.11102)) |
| Chat2SVG | 2025, CVPR | LLM template → SDEdit/ControlNet raster detail target → latent primitive optimisation → point optimisation | The method explicitly combines LLM semantic templates with diffusion-guided shape optimisation. [Chat2SVG project description](https://chat2svg.github.io/) ([chat2svg.github.io](https://chat2svg.github.io/?utm_source=openai)) | Best architectural precedent for your use case; still inherits diffusion target ambiguity and optimiser cost. |
| OmniSVG | 2025, NeurIPS | Qwen2.5-VL backbone, SVG tokens, `2M` SVG corpus; handles SVGs over `30k` tokens | Icon image-to-SVG: OmniSVG-4B DINO `0.993`, SSIM `0.950`, LPIPS `0.050`; VTracer: DINO `0.993`, SSIM `0.966`, LPIPS `0.039`. Illustration image-to-SVG: OmniSVG-8B LPIPS `0.231`; DiffVG `0.065`; VTracer `0.035`. [OmniSVG Table 2](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263)) | Demonstrates long-context SVG generation, but complex-image fidelity remains materially behind trace/optimisation pipelines in its own evaluation. |
| RLRF | 2025, NeurIPS | SVG SFT followed by GRPO using rendered-output reconstruction, semantic, and code-efficiency rewards | On SVG-Stack-Hard, Qwen2.5-VL-7B improved from SFT MSE `8.60`, SSIM `79.40`, LPIPS `16.58` to RLRF MSE `1.03`, SSIM `95.10`, LPIPS `3.08`; table’s scale is source-specific. [RLRF Table 1](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | Strongest public evidence that render-based post-training can close the direct-model fidelity gap without sacrificing code compactness. |
| Render-in-the-Loop | 2026 preprint | Stepwise partial-SVG rendering, visual self-feedback training, Render-and-Verify decoding | On MMSVG-Illustration, VSF+RaV reports LPIPS `0.178`, versus OmniSVG-8B `0.231`; this is within that paper’s protocol. [Render-in-the-Loop Table 1](https://arxiv.org/pdf/2604.20730) ([arxiv.org](https://arxiv.org/pdf/2604.20730)) | Training is required; naïve visual feedback can degrade general VLM output. |
| IntroSVG | 2026 preprint | Generator-critic VLM, SFT on correction data, DPO, three iterative refinements | FID improves `29.76 → 26.18` over three iterations; `92%` of samples were judged higher-quality at iteration 3 than iteration 0 in its reported study. [IntroSVG Tables 3–4 and human evaluation](https://arxiv.org/pdf/2603.09312) ([arxiv.org](https://arxiv.org/pdf/2603.09312)) [IntroSVG abstract](https://arxiv.org/abs/2603.09312) ([arxiv.org](https://arxiv.org/abs/2603.09312)) | Promising closed loop, but preprint evidence and task-specific metrics should be independently reproduced. |
| Arrow 1.1 / Arrow 1.1 Max | 2026, commercial | Closed proprietary SVG generator/vectorizer | Public provider documentation says Arrow outputs structured SVG, supports text-to-SVG and raster vectorization, and positions Max for dense illustrations, logos, and technical drawings. [Arrow 1.1 provider page](https://vercel.com/ai-gateway/models/arrow-1.1/about) ([vercel.com](https://vercel.com/ai-gateway/models/arrow-1.1/about)) | <MISSING_DATA>[No public parameter count, training corpus, independent benchmark, or reproducible quality study was located. A fidelity ceiling cannot be responsibly stated.]</MISSING_DATA> |

**Confidence: High** that the public research frontier has shifted from one-pass SVG code generation toward visual-feedback, RL, and render-in-the-loop systems; **Medium** that the 2026 preprints’ reported gains will transfer unchanged to macOS-style material icons. [RLRF](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) [Render-in-the-Loop](https://arxiv.org/abs/2604.20730) ([arxiv.org](https://arxiv.org/abs/2604.20730))

#### Build-vs-buy comparison

| Parameter | Arrow 1.1 / 1.1 Max | StarVector | OmniSVG | RLRF-style Qwen2.5-VL | Claude Code + custom harness |
|---|---|---|---|---|---|
| Parameter count | <MISSING_DATA>[Not published.]</MISSING_DATA> | `1B`, `8B` public variants. [StarVector repository](https://github.com/joanrod/star-vector) ([github.com](https://github.com/joanrod/star-vector)) | Paper describes `4B`/`8B` reporting variants and scaling experiments around Qwen2.5-VL. [OmniSVG](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263)) | `3B` and `7B` Qwen2.5-VL experiments. [RLRF](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | Model-dependent; proprietary service model size not published. |
| Context / output budget | `max_output_tokens: 1–131,072`; this is an output limit, not a published model context window. [Promptfoo QuiverAI provider docs](https://www.promptfoo.dev/docs/providers/quiverai/) ([promptfoo.dev](https://www.promptfoo.dev/docs/providers/quiverai/)) | Example inference sets `max_length=1000`; published total context limit not confirmed here. [StarVector repo](https://github.com/joanrod/star-vector) ([github.com](https://github.com/joanrod/star-vector)) | Supports SVG parameterizations exceeding `30k` tokens. [OmniSVG](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263)) | RLRF SFT uses `32k` context although Qwen2.5-VL supports up to `128k`. [RLRF training details](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | API/model-specific. |
| Documented generation latency | <MISSING_DATA>[No numeric latency SLA located.]</MISSING_DATA> | <MISSING_DATA>[No comparable published end-to-end latency located.]</MISSING_DATA> | <MISSING_DATA>[No comparable published end-to-end latency located.]</MISSING_DATA> | RLRF SVG-Stack-Hard table reports `63s` for Qwen2.5-VL-7B + RLRF under its evaluation setup. [RLRF Table 1](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | Depends on agent, render count, and provider latency. |
| Cost | Credit-based. A May 2026 documented example used `15` credits/vectorization for Arrow 1.1 and `20` for Max; provider says query live pricing. [Promptfoo QuiverAI provider docs](https://www.promptfoo.dev/docs/providers/quiverai/) ([promptfoo.dev](https://www.promptfoo.dev/docs/providers/quiverai/)) | Self-hosting compute; no managed price. | Self-hosting compute; no managed price. | RLRF training reported four `8×H100` nodes for about `3` days in one configuration. [RLRF details](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | Token/API and engineering cost. |
| License | Proprietary / subject to QuiverAI terms. [Arrow provider page](https://vercel.com/ai-gateway/models/arrow-1.1/about) ([vercel.com](https://vercel.com/ai-gateway/models/arrow-1.1/about)) | Open repository and released weights/data; exact downstream terms require repository/model-card verification before commercial use. | Open research release; exact downstream terms require release verification. | Research code/model-dependent. | Provider terms govern generated output and training-data reuse. |
| Best role | Buy as external baseline and optional teacher only if terms permit. | Open benchmark baseline and compact semantic scaffold. | Long, complex SVG generation research baseline. | Best public evidence for render-reward post-training. | Best immediate route to your fixed-reference icon objective. |

**Decision:** buy Arrow 1.1/Max for benchmark comparison and perhaps candidate generation; build the **eval and refinement harness** because neither Arrow nor public one-pass models offer a verified guarantee of matching specific diffusion-raster material references.

#### Arrow 1.1 API facts relevant to harness integration

| Operation | Endpoint / provider form | Documented controls | Constraint |
|---|---|---|---|
| Text-to-SVG | `POST /v1/svgs/generations`; provider form `quiverai:arrow-1.1` | `temperature`, `top_p`, `presence_penalty`, `max_output_tokens`, `n`, `stream`, `instructions`, `references` | Arrow 1.1 accepts up to `4` references; Arrow 1.1 Max accepts up to `16`. [QuiverAI provider documentation](https://www.promptfoo.dev/docs/providers/quiverai/) ([promptfoo.dev](https://www.promptfoo.dev/docs/providers/quiverai/)) |
| Image-to-SVG | `POST /v1/svgs/vectorizations`; provider form `quiverai:vectorize:arrow-1.1` | `image`, `auto_crop`, `target_size`, sampling controls, output-token limit | `target_size` supports `128–4,096` px. [QuiverAI provider documentation](https://www.promptfoo.dev/docs/providers/quiverai/) ([promptfoo.dev](https://www.promptfoo.dev/docs/providers/quiverai/)) |
| Streaming | Default is documented as enabled | emits `generating`, `reasoning`, and `draft` events, then content | Use `stream: false` for caching in reproducible evals. [QuiverAI provider documentation](https://www.promptfoo.dev/docs/providers/quiverai/) ([promptfoo.dev](https://www.promptfoo.dev/docs/providers/quiverai/)) |
| Rate limit | Error name documented: `rate_limit_exceeded` | Reduce concurrency or delay | <MISSING_DATA>[No published numeric requests-per-minute limit was found.]</MISSING_DATA> [QuiverAI provider documentation](https://www.promptfoo.dev/docs/providers/quiverai/) ([promptfoo.dev](https://www.promptfoo.dev/docs/providers/quiverai/)) |

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

#### Differentiable and optimisation vectorization

**Confidence: High:** Optimisation-based vectorization remains the appropriate finishing system when the requirement is to match a particular raster reference, rather than merely produce a semantically plausible icon.

- **DiffVG** makes vector rasterization differentiable after pixel prefiltering, enabling image-space losses to update vector parameters. Its multisampling option produces unbiased pixel gradients but has higher compute cost; analytical prefiltering is faster but can introduce artifacts. [DiffVG project and technical description](https://people.csail.mit.edu/tzumao/diffvg/) ([people.csail.mit.edu](https://people.csail.mit.edu/tzumao/diffvg/?utm_source=openai))

- **LIVE** progressively adds Bézier paths in a layer-wise process, using component-wise initialization and losses intended to reduce self-intersection. It explicitly identifies layer-wise topology and editability as goals, but notes layer-wise optimisation is less efficient than single-pass approaches. [LIVE, CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/papers/Ma_Towards_Layer-Wise_Image_Vectorization_CVPR_2022_paper.pdf) ([openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2022/papers/Ma_Towards_Layer-Wise_Image_Vectorization_CVPR_2022_paper.pdf?utm_source=openai))

- **VectorFusion** uses score-distillation sampling from a pixel diffusion model plus a differentiable vector rasterizer, with optional image initialization to improve fidelity and speed. [VectorFusion](https://arxiv.org/abs/2211.11319) ([arxiv.org](https://arxiv.org/abs/2211.11319?utm_source=openai))

- **SVGDreamer** adds semantic-driven image vectorization and vectorized particle score distillation to mitigate oversmoothing, oversaturation, limited diversity, and slow convergence. [SVGDreamer](https://arxiv.org/abs/2312.16476) ([arxiv.org](https://arxiv.org/abs/2312.16476?utm_source=openai))

- **Chat2SVG** is the clearest hybrid precursor: it makes an LLM semantic template, uses diffusion to create a detailed raster target, optimizes primitive embeddings and visual attributes, and then performs point-level path optimization. [Chat2SVG project page](https://chat2svg.github.io/) ([chat2svg.github.io](https://chat2svg.github.io/?utm_source=openai))

#### Best hybrid for the two macOS-style fixtures

For the concrete “hand-authored SVG underperforms diffusion raster” pairs, use this order:

1. **LLM/VLM layer plan**: identify base slab, face/object, cast shadow, ambient occlusion, rim light, specular strip, reflective insert, and micro-details.
2. **Semantic SVG scaffold**: enforce explicit groups and named variables for gradient stops, blur, opacity, light direction, and corner radii.
3. **Coarse raster matching**: fit global silhouette, centering, object scale, and major colour fields.
4. **Layer-local material matching**: tune gradients, opacity stops, blur radii, and clipped highlight paths.
5. **Path-local fitting**: optimize control points only for the corresponding visible residual region.
6. **Small-size repair pass**: simplify or strengthen features that disappear or alias at `32`/`16` px.
7. **Freeze and archive** the accepted SVG plus all metric and render artifacts.

<INFERENCE from="[DiffVG permits image-space gradient optimisation; LIVE provides layer-wise topology; Chat2SVG uses LLM templates plus diffusion-guided optimisation; RLRF demonstrates render-based rewards]">The LLM should own semantic layer decisions and the optimizer should own continuous matching because trying to make one autoregressive pass solve both produces either overly simple, clean-but-flat icons or dense, poorly editable path soup.</INFERENCE> [DiffVG](https://people.csail.mit.edu/tzumao/diffvg/) ([people.csail.mit.edu](https://people.csail.mit.edu/tzumao/diffvg/?utm_source=openai)) [LIVE](https://arxiv.org/abs/2206.04655) ([arxiv.org](https://arxiv.org/abs/2206.04655?utm_source=openai)) [Chat2SVG](https://arxiv.org/abs/2411.16602) ([arxiv.org](https://arxiv.org/abs/2411.16602?utm_source=openai))

#### What “raster-class material” requires in SVG

| Raster appearance | SVG construction to prefer | Why a flat-path LLM misses it |
|---|---|---|
| Soft cast shadow | Duplicated silhouette, dark fill, Gaussian blur, clipped mask, opacity falloff | A single dark offset path reads as sticker-like. |
| Rounded translucent glass/plastic | Radial/linear gradient stack, low-opacity white highlight, interior shadow, clipped reflection | Requires coordinated paint layers, not one fill colour. |
| MacOS-style embossed edge | Base gradient, inner shadow approximation, rim highlight, local low-radius blur | Material is conveyed by small luminance transitions and occlusion. |
| Metallic/chrome accent | Multi-stop non-monotonic gradients, narrow specular paths, masked reflections | One linear gradient cannot capture local highlight geometry. |
| Soft ambient occlusion | Local dark transparent shapes under overlaps; not a global black blur | Must respect object topology and occlusion ordering. |
| Fine texture or grain | Optional low-amplitude filter/noise only at large size; suppress at 32/16 px | Easily metric-gamed and visually unstable at icon size. |

**Confidence: Medium:** These are engineering prescriptions rather than directly benchmarked universal requirements. The underlying primitives are supported by SVG and filter standards; whether a particular macOS-style reference needs each effect is fixture-dependent. [W3C Filter Effects](https://www.w3.org/TR/filter-effects-1/) ([w3.org](https://www.w3.org/TR/filter-effects-1/?utm_source=openai))

---

### 3. What automated perceptual metrics and eval protocol are suitable at 1024 px and at 128/32/16 px?

#### Metric suitability

| Metric | Best use | Reliability for 1024 px material comparison | Reliability at 128 px | Reliability at 32/16 px | Do not use it as |
|---|---|---|---|---|---|
| LPIPS | Learned perceptual distance; high-resolution shape/material residuals | High relative to traditional pixel metrics on its human perceptual judgement dataset. [LPIPS](https://doi.org/10.1109/cvpr.2018.00068) ([doi.org](https://doi.org/10.1109/cvpr.2018.00068?utm_source=openai)) | Medium | Low-to-Medium: downsampling and receptive-field effects can dominate tiny icons. | Sole objective or sole acceptance criterion. |
| DISTS | Texture and structure similarity | High for material/texture tolerance, particularly where a pixel-identical texture is not needed. [DISTS](https://doi.org/10.1109/TPAMI.2020.3045810) ([cns.nyu.edu](https://www.cns.nyu.edu/~lcv/pubs/makeAbs.php?loc=Ding20&utm_source=openai)) | Medium | Low-to-Medium; no located SVG-icon-specific 16 px calibration study. | A strict geometry verifier. |
| SSIM / MS-SSIM | Structural and contrast preservation | Medium; MS-SSIM is generally preferable to single-scale SSIM for varying viewing conditions. [MS-SSIM](https://ece.uwaterloo.ca/~z70wang/publications/msssim.html) ([ece.uwaterloo.ca](https://ece.uwaterloo.ca/~z70wang/publications/msssim.html?utm_source=openai)) | Medium-High for silhouette/major structure | Medium if paired with edge measures; single-pixel shifts can destabilize scores. | Material-quality or semantic metric. |
| Edge overlap / distance transform | Contours, silhouette, feature placement | High for geometry | High | High if antialiasing and thresholding are standardized | A measure of colour/material fidelity. |
| CLIP/DINO image embeddings | Semantic guardrail and broad appearance consistency | Medium | Medium | Low for tiny exact details | Strict reference-fidelity score. |
| VLM-as-judge rubric | Visible defects, hierarchy, material plausibility, “does it feel like the reference?” | Medium if rubric is reference-aware and blinded | Medium | Medium when given enlarged crops plus native-size render | Training reward without anti-gaming checks. |
| SVG structural score | Editability, validity, path budget, group semantics, forbidden raster checks | N/A | N/A | N/A | A visual similarity metric. |

**Confidence: High:** Metrics should be complementary. RLRF reports that on sparse line-style SVG-Icons, small thin-stroke misalignments can heavily affect MSE and SSIM even when perceptual metrics improve; it explicitly cautions that pixel metrics can be unreliable in that case. [RLRF SVG-Icons analysis](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2))

<MISSING_DATA>[No peer-reviewed source was located that calibrates LPIPS, DISTS, SSIM/MS-SSIM, CLIP, and VLM judging specifically for raster-vs-SVG macOS-style icons at all four requested sizes—1024, 128, 32, and 16 px. Build a local human-calibration set before treating any composite score as ground truth.]</MISSING_DATA>

#### Proposed multi-scale acceptance score

This is an **engineering recommendation**, not an empirically validated universal formula:

\[
S = 0.35S_{1024} + 0.25S_{128} + 0.25S_{32} + 0.15S_{16}
\]

Where:

\[
S_r =
0.30(1-\text{LPIPS}_r) +
0.20(1-\text{DISTS}_r) +
0.20(\text{MS-SSIM}_r) +
0.20(\text{EdgeF1}_r) +
0.10(\text{VLM-rubric}_r)
\]

Apply these **hard gates**, rather than trusting the weighted scalar:

- candidate SVG parses, sanitizes, and renders;
- no `<image>` raster embedding;
- alpha-mask IoU and edge F1 exceed fixture-specific minimums at `32` and `16` px;
- no individual resolution may decline beyond a tolerated margin;
- path count, point count, filter count, and SVG byte size remain within the allowed complexity envelope;
- VLM judge detects no major unresolved rubric item;
- render in the designated target renderer and at least one secondary renderer.

<INFERENCE from="[LPIPS is trained on human similarity judgments; DISTS explicitly models structure and texture; RLRF uses multiple rewards and documents metric disagreement; small-icon fidelity prioritizes silhouette and edge placement]">A Pareto gate is safer than a weighted score because it prevents 1024 px texture gains from masking regressions in 16 px recognizability, and prevents semantic embedding gains from masking a wrong silhouette.</INFERENCE> [LPIPS](https://doi.org/10.1109/cvpr.2018.00068) ([doi.org](https://doi.org/10.1109/cvpr.2018.00068?utm_source=openai)) [DISTS](https://doi.org/10.1109/TPAMI.2020.3045810) ([cns.nyu.edu](https://www.cns.nyu.edu/~lcv/pubs/makeAbs.php?loc=Ding20&utm_source=openai)) [RLRF reward ablation](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2))

#### Proposed render-compare-edit protocol

```text
for fixture in fixture_set:
  target = normalize_reference(fixture.raster, canvas=1024, alpha="premultiplied")

  svg = author_initial_scaffold(target, prompt, svg_grammar)
  best = evaluate(svg, target, sizes=[1024, 128, 32, 16])

  for iteration in 1..N:
      renders = render(svg, target_renderer, sizes=[1024,128,32,16])
      metrics = score(renders, target)

      critique = vlm_critic(
        reference=target,
        candidate=renders,
        residual_maps=metrics.residual_maps,
        rubric=["silhouette", "proportions", "layers",
                "shadow", "highlight", "material", "small-size legibility"]
      )

      edit_plan = constrain_to_one_edit_class(critique)
      proposal = llm_edit(svg, edit_plan)

      proposal = local_optimize(
        proposal,
        editable_region=edit_plan.region,
        losses=["edge", "LPIPS/DISTS", "colour", "complexity"]
      )

      proposal_score = evaluate(proposal, target)
      if pareto_accept(proposal_score, best) and structural_valid(proposal):
          svg, best = proposal, proposal_score
      else:
          rollback_and_record_failure()

      if plateau(best, k=2) or repeated_edit_signature():
          branch_or_stop()
```

Recommended initial iteration budget: **one coarse structural iteration, one material iteration, one detail iteration, and one small-size repair iteration**; permit more only when the Pareto gate continues to improve. **Confidence: Medium:** IntroSVG uses a maximum of three refinement iterations and reports monotonic aggregate improvements; that supports a short bounded loop, but does not prove an optimal iteration count for your fixtures. [IntroSVG Table 4](https://arxiv.org/pdf/2603.09312) ([arxiv.org](https://arxiv.org/pdf/2603.09312))

---

### 4. What is the evidence on VLM-guided iterative editing, convergence behavior, failure modes, and distillation?

#### Evidence that iterative visual feedback helps

| Evidence | Reported result | Practical implication |
|---|---|---|
| IntroSVG | FID improves from `29.76` at initial draft to `26.18` after three iterations; reported aesthetic and HPS also rise. [IntroSVG Table 4](https://arxiv.org/pdf/2603.09312) ([arxiv.org](https://arxiv.org/pdf/2603.09312)) | A bounded critic-generator loop can improve consistently after dedicated SFT/DPO. |
| IntroSVG zero-shot loop | GPT-4o FID `37.80 → 36.34`; Grok-4 `41.39 → 32.85`; GPT-5 `35.87 → 32.68` over three iterations in the paper’s task. [IntroSVG Table 5](https://arxiv.org/pdf/2603.09312) ([arxiv.org](https://arxiv.org/pdf/2603.09312)) | General VLMs can benefit, but gains differ substantially by model and metric. |
| Render-in-the-Loop | VSF+RaV on MMSVG-Illustration reports LPIPS `0.178`, compared with `0.231` for OmniSVG-8B in the same table. [Render-in-the-Loop Table 1](https://arxiv.org/pdf/2604.20730) ([arxiv.org](https://arxiv.org/pdf/2604.20730)) | Partial render context plus verification can improve direct SVG generation. |
| RLRF | Rendering rewards improve Qwen2.5-VL-7B SVG-SFT to RLRF from MSE `8.60 → 1.03`, SSIM `79.40 → 95.10`, and LPIPS `16.58 → 3.08` on SVG-Stack-Hard. [RLRF Table 1](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | Rendering feedback is strong enough to train policy improvement, not merely rank candidates. |
| Frontend analogue | A VLM critic loop for frontend code reports up to `17.8%` improvement over three refinement cycles on WebDev Arena tasks. [Vision-Guided Iterative Refinement for Frontend Code Generation](https://arxiv.org/abs/2604.05839) ([arxiv.org](https://arxiv.org/abs/2604.05839?utm_source=openai)) | The generate-render-critic-edit paradigm generalizes beyond SVG. |

#### Known failure modes and mandatory mitigations

| Failure mode | Evidence | Harness mitigation |
|---|---|---|
| Blind-generation drift | One-pass models accumulate geometry and semantic errors over long SVG sequences. [RefineSVG](https://arxiv.org/abs/2607.27699) ([arxiv.org](https://arxiv.org/abs/2607.27699)) | Use partial renders, region-of-interest residuals, and staged layers. |
| Naïve feedback degrades output | Render-in-the-Loop reports GPT-5 illustration LPIPS worsening `0.345 → 0.388` with naïve intermediate canvases. [Render-in-the-Loop ablation](https://arxiv.org/pdf/2604.20730) ([arxiv.org](https://arxiv.org/pdf/2604.20730)) | Train feedback use, or provide structured diff maps and constrained edit actions rather than raw screenshots alone. |
| Degenerate repetition / oscillation | Without RaV, the model may repeatedly redraw redundant strokes; RaV rejects paths with negligible pixel differences. [Render-in-the-Loop failure analysis](https://arxiv.org/pdf/2604.20730) ([arxiv.org](https://arxiv.org/pdf/2604.20730)) | Hash edit signatures; reject visually negligible edits; enforce a per-layer action budget; rollback on repeated defect class. |
| Local metric plateau | DreamSim-only reward saturates early and produces weaker reconstruction; RLRF finds composite rewards stronger. [RLRF reward ablation](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | Use mixed fidelity, edge, semantic, and complexity rewards; branch candidates rather than endlessly revise one path. |
| ViewBox reward hack | RLRF observed a model shrinking SVG `viewBox` to create an artificially low-resolution comparison. [RLRF reward-hacking analysis](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | Force render dimensions, aspect ratio, and viewBox normalization from the reference; never let candidate metadata define the metric canvas. |
| Length-collapse reward hack | RLRF observed SVGs becoming progressively shorter until unusable due to an over-incentivized length reward. [RLRF reward-hacking analysis](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) | Treat compactness as a constraint or weak regularizer, never as dominant reward. |
| Metric gaming by texture or blur | <INSUFFICIENT_EVIDENCE>[No SVG-icon-specific controlled study located, but this is a foreseeable consequence of optimizing a proxy score.]</INSUFFICIENT_EVIDENCE> | Require cross-size gates, edge gates, VLM review, and structural constraints before acceptance. |

#### Distillation plan: from strong LLM outputs to a model beyond Arrow-class performance

**Confidence: High:** A model trained only to imitate a stronger LLM cannot be expected to exceed it systematically. It can surpass the teacher on a defined target distribution only if it receives **additional information or a better objective**: raster-ground-truth matching, optimisation trajectories, selection labels, rendering rewards, and task-specific constraints.

<INFERENCE from="[RLRF improves a supervised base using render rewards; IntroSVG trains correction and preference data; OmniSVG and StarVector show multi-million SVG corpora; Arrow’s public quality ceiling is unmeasured]">To exceed an Arrow-class system on your domain, distillation must be target-conditioned and reward-augmented rather than pure teacher-output imitation, and success must be claimed only on a private benchmark that includes Arrow outputs.</INFERENCE> [RLRF](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) [IntroSVG](https://arxiv.org/pdf/2603.09312) ([arxiv.org](https://arxiv.org/pdf/2603.09312)) [StarVector](https://arxiv.org/abs/2312.11556) ([arxiv.org](https://arxiv.org/abs/2312.11556?utm_source=openai))

##### Training-data record format

Every retained example should store:

```json
{
  "id": "fixture-or-synthetic-id",
  "prompt": "icon instruction",
  "reference_png_1024": "content-addressed URI",
  "reference_alpha": "content-addressed URI",
  "teacher_svg_raw": "<svg ...>",
  "teacher_svg_canonical": "<svg ...>",
  "renderer": {
    "engine": "WebKit/Chromium version",
    "canvas": 1024,
    "color_space": "sRGB",
    "background": "transparent"
  },
  "scene_plan": {
    "layers": [],
    "materials": [],
    "light_direction": [],
    "protected_semantics": []
  },
  "trajectory": [
    {
      "svg": "<svg ...>",
      "render": "URI",
      "metrics": {},
      "vlm_critique": {},
      "edit_action": {},
      "accepted": true
    }
  ],
  "final_metrics": {
    "1024": {},
    "128": {},
    "32": {},
    "16": {}
  },
  "structure": {
    "paths": 0,
    "nodes": 0,
    "gradients": 0,
    "filters": 0,
    "bytes": 0
  },
  "rights": {
    "source_license": "",
    "teacher_terms_reviewed": false
  }
}
```

##### Recommended training sequence

1. **Corpus SFT:** Start with licensed human SVGs plus accepted synthetic SVG/reference pairs. StarVector and OmniSVG each demonstrate that `2M`-sample SVG corpora are viable scales for broad SVG modelling. [StarVector SVG-Stack](https://arxiv.org/abs/2312.11556) ([arxiv.org](https://arxiv.org/abs/2312.11556?utm_source=openai)) [OmniSVG MMSVG-2M](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263))

2. **Teacher proposal generation:** For each reference, generate multiple scaffold variants from a stronger coding/VLM system; use a target-image-aware editor and local optimiser to create variants, not a single answer.

3. **Rejection sampling:** Retain only examples passing validity, structural, multi-scale visual, and VLM rubric thresholds. Keep near-miss outputs as rejected examples.

4. **Correction SFT:** Train the model on `(reference, current SVG render, residual map, critique) → corrected SVG`, following the direction of IntroSVG’s generation/correction/critique construction. [IntroSVG method](https://arxiv.org/abs/2603.09312) ([arxiv.org](https://arxiv.org/abs/2603.09312))

5. **Preference optimisation:** Form preference pairs where the winner is determined by the multi-scale Pareto gate plus blinded VLM/human adjudication. Use DPO or equivalent only after the policy can reliably emit valid SVG.

6. **Rendering-feedback RL:** Run grouped rollouts, render each, and optimize a composite reward: reference fidelity, edge alignment, material score, small-size legibility, and constrained complexity. RLRF used `64` rollouts per image, `500` steps, and `16k` unique images in one image-to-SVG RL run after large-scale SFT. [RLRF RL configuration](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2))

7. **Held-out Arrow comparison:** Freeze a private benchmark before training completion. Run Arrow 1.1, Arrow 1.1 Max, teacher LLM, base student, and post-RL student through the same harness. Publish only paired, blinded results.

##### What it would take to beat Arrow 1.1’s class

| Requirement | Why it is necessary | Evidence basis |
|---|---|---|
| A private benchmark of raster references, not only public SVGs | Public SVG benchmarks reward reconstruction of existing vector-native assets; your target is diffusion-raster material quality. | OmniSVG and RLRF benchmarks use different datasets and score scales; their results cannot establish a universal winner. [OmniSVG](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263)) [RLRF](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) |
| More than the two existing fixture pairs | Two pairs are sufficient for debugging but not model selection, metric calibration, or claims of superiority. | <INFERENCE from="[Statistical evaluation requires variation across icon styles, materials, and failure types]">A two-pair set cannot distinguish memorization, renderer overfitting, and general capability.</INFERENCE> |
| Target-domain material diversity | Need examples with soft shadows, glass, metal, translucency, rounded plastic, inset faces, and non-flat gradients. | Current tokenized SVG corpora often simplify SVG syntax and material attributes. [OmniSVG simplification](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263)) |
| Render-reward post-training | Token likelihood alone does not see whether rendered output matches target. | RLRF’s central result. [RLRF](https://arxiv.org/html/2505.20793v2) ([arxiv.org](https://arxiv.org/html/2505.20793v2)) |
| Structural/editability reward | Pure trace fidelity can create thousands of tiny paths and defeat hand-editability. | OmniSVG and Render-in-the-Loop identify redundant/tangled optimisation outputs as a problem. [OmniSVG discussion](https://arxiv.org/pdf/2504.06263) ([arxiv.org](https://arxiv.org/pdf/2504.06263)) [Render-in-the-Loop](https://arxiv.org/abs/2604.20730) ([arxiv.org](https://arxiv.org/abs/2604.20730)) |
| Legal right to retain and train on teacher outputs | Commercial model/provider terms may restrict output reuse or competitive-model training. | <MISSING_DATA>[QuiverAI and teacher-provider terms must be reviewed by counsel before using outputs for distillation.]</MISSING_DATA> |

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| DiffVG enables raster-loss optimisation of vector parameters through differentiable rasterization. | Li, Lukáč, Gharbi, Ragan-Kelley | 2020 | ACM SIGGRAPH/TOG research paper and official project page | [DiffVG](https://people.csail.mit.edu/tzumao/diffvg/) |
| LIVE progressively adds layer-wise paths and optimizes them for vectorization/editability. | Ma et al. | 2022 | CVPR paper | [LIVE](https://openaccess.thecvf.com/content/CVPR2022/papers/Ma_Towards_Layer-Wise_Image_Vectorization_CVPR_2022_paper.pdf) |
| VectorFusion applies SDS and differentiable vector rendering to produce SVG-exportable images. | Jain, Xie, Abbeel | 2023 | CVPR paper | [VectorFusion](https://arxiv.org/abs/2211.11319) |
| IconShop sequentializes SVG paths for autoregressive text-guided icon generation. | Wu, Su, Ma, Liao | 2023 | SIGGRAPH Asia paper | [IconShop](https://arxiv.org/abs/2304.14400) |
| SVGDreamer uses semantic vectorization and particle-based score distillation. | Xing et al. | 2024 | CVPR paper | [SVGDreamer](https://arxiv.org/abs/2312.16476) |
| StarVector uses multimodal VLM/code generation and SVG-Stack with `2M` examples. | Rodriguez et al. | 2025 | CVPR paper/repository | [StarVector](https://arxiv.org/abs/2312.11556) |
| LLM4SVG reports direct-LLM SVG performance and latency against optimization baselines. | Xing et al. | 2025 | CVPR paper | [LLM4SVG](https://arxiv.org/pdf/2412.11102) |
| Chat2SVG combines LLM templates, diffusion raster enhancement, and path optimization. | Wu, Su, Liao | 2025 | CVPR paper | [Chat2SVG](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.pdf) |
| OmniSVG uses VLM tokenization, MMSVG-2M, and supports SVGs beyond `30k` tokens. | Yang et al. | 2025 | NeurIPS paper | [OmniSVG](https://arxiv.org/pdf/2504.06263) |
| RLRF improves SVG generation through rendering-aware GRPO rewards. | Rodriguez et al. | 2025 | NeurIPS paper / arXiv HTML | [RLRF](https://arxiv.org/html/2505.20793v2) |
| Render-in-the-Loop uses partial renders and Render-and-Verify to reduce blind SVG generation failures. | Liang et al. | 2026 | Preprint | [Render-in-the-Loop](https://arxiv.org/abs/2604.20730) |
| IntroSVG applies SFT, DPO, and iterative generator-critic correction. | Wang et al. | 2026 | Preprint | [IntroSVG](https://arxiv.org/abs/2603.09312) |
| LPIPS is evaluated against human perceptual similarity judgements and outperforms traditional metrics on BAPPS. | Zhang et al. | 2018 | CVPR paper | [LPIPS](https://doi.org/10.1109/cvpr.2018.00068) |
| DISTS combines structural and textural similarity and is optimized against human ratings. | Ding et al. | 2020 | IEEE TPAMI paper | [DISTS](https://doi.org/10.1109/TPAMI.2020.3045810) |
| MS-SSIM handles multiple scales and viewing conditions better than single-scale SSIM. | Wang, Simoncelli, Bovik | 2003 | IEEE Asilomar paper | [MS-SSIM](https://ece.uwaterloo.ca/~z70wang/publications/msssim.html) |
| SVG supports filter primitives including blur, compositing, lighting, turbulence, and morphology. | W3C | Current standard | Formal web graphics specification | [Filter Effects Module Level 1](https://www.w3.org/TR/filter-effects-1/) |
| Arrow 1.1 API/provider capabilities, output controls, references, and vectorization constraints. | Vercel AI Gateway; Promptfoo integration documentation | 2026 | Provider and integration documentation; not independent performance validation | [Arrow 1.1](https://vercel.com/ai-gateway/models/arrow-1.1/about); [QuiverAI provider docs](https://www.promptfoo.dev/docs/providers/quiverai/) |

**Source-discipline validation:** Conference papers, journal papers, W3C standards, and official project/repository pages were used for technical and quantitative claims. Arrow-specific API behavior was taken from provider/integration documentation only; no vendor quality assertion was treated as independent evidence. Promotional third-party Arrow claims were excluded from performance conclusions.

---

## Knowledge Gaps

### Benchmark and measurement gaps

- <MISSING_DATA>[A public, independently audited benchmark comparing Arrow 1.1 or Arrow 1.1 Max against OmniSVG, StarVector, RLRF, and commercial coding agents on raster-reference material fidelity was not found.]</MISSING_DATA>

- <MISSING_DATA>[No robust published calibration was found for LPIPS, DISTS, MS-SSIM, CLIP/DINO, and VLM judging specifically on SVG-vs-raster macOS-style icons at 1024/128/32/16 px.]</MISSING_DATA>

- <INSUFFICIENT_EVIDENCE>[The two stated fixture pairs cannot support claims of generalization, metric reliability, or superiority over Arrow-class systems.]</INSUFFICIENT_EVIDENCE>

### Product and operational gaps

- <MISSING_DATA>[Arrow 1.1’s parameter count, architecture, training data, context window, public latency SLA, explicit numeric rate limits, and reproducible benchmark scores were not publicly verified.]</MISSING_DATA>

- <MISSING_DATA>[Current provider terms governing retention, model training, and competitive distillation from Arrow outputs or other proprietary LLM outputs require legal review.]</MISSING_DATA>

### Rendering gaps

- <INSUFFICIENT_EVIDENCE>[Cross-renderer consistency for the exact planned filter, mask, gradient, and blend subset has not been established. The harness should test the macOS-target renderer explicitly rather than assuming browser equivalence.]</INSUFFICIENT_EVIDENCE>

---

## Recommended Next Steps

1. **Build the deterministic four-size eval harness before improving the generator.**  
   **Rationale:** Without a frozen renderer, alpha policy, score bundle, rollback store, and human-calibrated rubric, the team will optimize screenshots and anecdotes rather than icon quality.

2. **Expand the two fixture pairs into a private “Material Icon Fidelity” benchmark.**  
   **Rationale:** Include opaque plastic, translucent glass, metallic accents, soft shadows, embossed faces, and clean flat controls. Hold out at least one style family and several unseen object categories for final testing.

3. **Implement a Claude Code scaffold-plus-local-optimizer prototype rather than training a vector model first.**  
   **Rationale:** It is the fastest way to determine whether the missing quality is due to SVG grammar, material construction, optimisation, or model reasoning. Capture every accepted and rejected trajectory as future training data.

4. **Run a controlled bake-off: Arrow 1.1, Arrow 1.1 Max, Claude Code scaffold-only, Claude Code plus optimizer, StarVector/RLRF baseline.**  
   **Rationale:** Use identical references, prompts, output budgets, renderer, and the same multi-scale Pareto gate. This produces the evidence needed for build-vs-buy.

5. **Only then begin distillation with correction trajectories and rendering-reward RL.**  
   **Rationale:** SFT on teacher SVGs will reproduce teacher behavior; correction pairs, rejected candidates, and multi-scale render rewards are the ingredients that can improve target-domain fidelity beyond a teacher’s raw one-pass output.

## Sources

- [Chat2SVG: Vector Graphics Generation with Large Language Models and Image Diffusion Models](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.pdf?utm_source=openai)
- [Rendering-Aware Reinforcement Learning for Vector Graphics Generation](https://arxiv.org/html/2505.20793v2)
- [Render-in-the-Loop: Vector Graphics Generation via Visual Self-Feedback](https://arxiv.org/abs/2604.20730)
- [RefineSVG: Visual Feedback-Driven Reinforcement Learning for Image-to-SVG Generation](https://arxiv.org/abs/2607.27699)
- [OmniSVG: A Unified Scalable Vector Graphics Generation Model](https://arxiv.org/pdf/2504.06263)
- [Filter Effects Module Level 1](https://www.w3.org/TR/filter-effects-1/?utm_source=openai)
- [The Unreasonable Effectiveness of Deep Features as a Perceptual Metric](https://doi.org/10.1109/cvpr.2018.00068?utm_source=openai)
- [Abstract: Image quality assessment: Unifying structure and texture similarity](https://www.cns.nyu.edu/~lcv/pubs/makeAbs.php?loc=Ding20&utm_source=openai)
- [Render-in-the-Loop: Vector Graphics Generation via Visual Self-Feedback](https://arxiv.org/pdf/2604.20730)
- [Arrow 1.1 About | Vercel AI Gateway](https://vercel.com/ai-gateway/models/arrow-1.1/about)
- [QuiverAI Provider | Promptfoo](https://www.promptfoo.dev/docs/providers/quiverai/)
- [Chat2SVG: Vector Graphics Generation with Large Language Models and Image Diffusion Models](https://arxiv.org/abs/2411.16602?utm_source=openai)
- [Filter Effects – SVG 1.1 (Second Edition)](https://www.w3.org/TR/SVG11/filters.html?utm_source=openai)
- [IconShop: Text-Guided Vector Icon Synthesis with Autoregressive Transformers](https://arxiv.org/abs/2304.14400?utm_source=openai)
- [StarVector: Generating Scalable Vector Graphics Code from Images and Text](https://arxiv.org/abs/2312.11556?utm_source=openai)
- [https://arxiv.org/pdf/2412.11102](https://arxiv.org/pdf/2412.11102)
- [Chat2SVG: Vector Graphics Generation with Large Language Models and Image Diffusion Models](https://chat2svg.github.io/?utm_source=openai)
- [IntroSVG: Learning from Rendering Feedback for Text-to-SVG Generation via an Introspective Genera...](https://arxiv.org/pdf/2603.09312)
- [IntroSVG: Learning from Rendering Feedback for Text-to-SVG Generation via an Introspective Genera...](https://arxiv.org/abs/2603.09312)
- [GitHub - joanrod/star-vector: StarVector is a foundation model for SVG generation that transforms...](https://github.com/joanrod/star-vector)
- [Differentiable Vector Graphics Rasterization for Editing and Learning](https://people.csail.mit.edu/tzumao/diffvg/?utm_source=openai)
- [Towards Layer-wise Image Vectorization](https://openaccess.thecvf.com/content/CVPR2022/papers/Ma_Towards_Layer-Wise_Image_Vectorization_CVPR_2022_paper.pdf?utm_source=openai)
- [VectorFusion: Text-to-SVG by Abstracting Pixel-Based Diffusion Models](https://arxiv.org/abs/2211.11319?utm_source=openai)
- [SVGDreamer: Text Guided SVG Generation with Diffusion Model](https://arxiv.org/abs/2312.16476?utm_source=openai)
- [Towards Layer-wise Image Vectorization](https://arxiv.org/abs/2206.04655?utm_source=openai)
- [Multi-scale Structural Similarity for Image Quality Assessment](https://ece.uwaterloo.ca/~z70wang/publications/msssim.html?utm_source=openai)
- [Vision-Guided Iterative Refinement for Frontend Code Generation](https://arxiv.org/abs/2604.05839?utm_source=openai)
