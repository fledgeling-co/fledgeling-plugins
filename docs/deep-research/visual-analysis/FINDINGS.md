# Iterative VLM icon refinement — panel findings

Five Dossier deep-research runs, read in full and citation-verified 2026-08-08. Structured by what it changes, not by who said it. Every claim names its backing backend(s).

## Backend keys

| Key | Run | Backend | Cited | Fabrication check | Live | Usable domains |
|---|---|---|---|---|---|---|
| **O-sol** | `dr_e7b148cea3d2b28a` | openai `gpt-5.6-sol` (max) | 61 | ATTENTION — 2 malformed | 87% (53/61) | ~20 |
| **Codex** | `dr_748d2e04fa12bc31` | local-codex (max) | 48 | ATTENTION — 1 dead, 1 malformed | 90% (43/48) | ~14 |
| **O-terra** | `dr_ac17fa30ad85a308` | openai `gpt-5.6-terra` (fast) | 44 | PASS | 86% (38/44) | ~10 |
| **G-fast** | `dr_3e2d45a8cc8f070d` | gemini `deep-research-preview` (fast) | 29 | PASS | 93% (27/29) | ~9 |
| **G-max** | `dr_e1fa03cf10457b13` | gemini `deep-research-max` (max) | 61 | ATTENTION — 4 malformed | 82% (50/61) | **~7** |

### Two corrections to the headline source count

**G-max's 61 citations are not 61 sources.** 52 of its 61 are `vertexaisearch.cloud.google.com/grounding-api-redirect/...` opaque redirects, which are unattributable to a domain and corroborate nothing. Its only attributable sources are the 9 URLs in its Evidence Table, one of which (`successfulsoftware.net`) does not resolve. **G-max effectively contributes ~7 independent domains, not 61.** Weight it accordingly — it is the most expensive run in the panel ($7) and the thinnest evidentiary contributor.

**The "malformed URL" verdicts are mostly local DNS, not fabrication.** Every host flagged `invalid_url` with *"resolves to a private address"* — `macworld.com`, `9to5mac.com`, `weblog.rogueamoeba.com`, `successfulsoftware.net` — is a real, well-known site. This is almost certainly an ad-blocking resolver on this machine, not a fabricated citation. Do not read those as invented. The one genuine dead link in the panel is Codex's CVF URL for Kim et al. (404 — the paper exists, the `/papers/....pdf` path is wrong; its `/html/` sibling resolves).

### Counting rule applied throughout

Support is counted in **independent domains and distinct primary works**, never in backends. Where two backends cite the same paper through different URLs (project page vs arXiv), that is one source. Where a claim rests on one backend only, it is labelled **single-sourced**. Anything reached by combining sources is labelled **synthesised**.

---

## 1. What binds a generator to a visual target

### The blunt answer: none of the conditioning literature transfers to this pipeline

**Corroborated — 4 of 5 backends, stated explicitly and independently.**

Every method the panel surfaced for binding a generator to a visual target — IP-Adapter, StyleDrop, DreamBooth, textual inversion, InstantStyle, LoRA, Diffusion-DPO — operates *inside a diffusion pipeline*. This skill hand-authors SVG through a code model. The mechanism these methods use (injecting reference features into cross-attention during denoising) has no counterpart in a model emitting `<path d="..."/>`.

- **O-sol**: "Fine-tuning a diffusion style adapter will not fix a Claude Code agent that is editing SVG text." Adds the only constructive alternative: fine-tuning the *language/VLM agent* would need data in the actual task form — `(reference image, current SVG/render, measured differences, expert edit, preferred outcome)`.
- **Codex**: "IP-Adapter's 22-million-parameter image adapter, DreamBooth, textual inversion, StyleDrop, and InstantStyle operate inside diffusion-generation pipelines; they do not directly teach a proprietary code model to write better SVG."
- **O-terra**: IP-Adapter "does not produce editable SVG grammar"; StyleDrop's "evidence is from its own model/task setting, not proof for SVG icons"; both DreamBooth and StyleDrop are "generation-model adaptation methods, not substitutes for a calibrated critic."
- **G-max**: agrees on the economics — Diffusion-DPO's ~1M-pair ViPO dataset is "operationally impossible" for a solo developer — and lands on rubric + in-context exemplars.

**G-fast dissents by not engaging.** It recommends LoRA (15–30 images at 1024²), DuoLoRA and EST-LoRA adapter fusion as the path to durable style, and never raises the transfer problem. It answered the question as though the pipeline were diffusion. **Do not act on G-fast's LoRA recommendation.** Its supporting sources for the 15–30 figure are `dev.to` and `help.trypencil.com` — vendor/blog tier, uncorroborated by any other backend.

Reference figures, for the record, so nobody re-litigates this: StyleDrop tunes <1% of parameters and can work from one style image (O-sol, Codex, O-terra — arXiv 2306.00983 / NeurIPS proceedings, same work). IP-Adapter is ~22M parameters (O-sol, Codex, O-terra — arXiv 2308.06721, same work). DreamBooth needs 3–5 images (O-terra, O-sol). Diffusion-DPO used ~851k pairs (O-sol, Codex — same work, arXiv 2311.12908); HPSv2 798,090 choices over 433,760 pairs (O-sol, Codex). G-max's alternative figure of 1,000,000 pairs for Poly-DPO/ViPO is a different dataset and single-sourced through a redirect.

### What does transfer: a retrieved, annotated exemplar corpus plus a written rubric

**Corroborated — 4 backends converge on the architecture, disagree on the number.**

| Backend | Store | Retrieve per run |
|---|---|---|
| O-sol | ~24–40 icons | 4–8 |
| O-terra | 12–40, grouped by material / object class | not specified |
| Codex | "small, versioned, annotated" — no number | most relevant only |
| G-max | 3–5 in context | 3–5 |

**Never average these.** All three of O-sol, Codex and O-terra explicitly flag the count as unvalidated. Codex is blunt: *"Corpus size should therefore be selected through an internal learning curve, not asserted from diffusion-personalization papers."* Start at the overlap (~24), measure, adjust.

Three details of the corpus design carry real weight:

1. **Counterexamples are not optional.** *Corroborated — Codex + O-sol independently.* Codex: without them "the model can imitate superficial shared traits — squircles, gloss, blue gradients — without learning the boundary between coherent Liquid Glass and generic 'AI glass.'" O-sol: include paired *"good versus generic"* and *"good versus overworked"* examples with a one-sentence reason each. This is the most actionable single item in this section and it costs nothing but curation.

2. **Annotate structurally, not descriptively.** Codex: store each exemplar with its 1024 render, 64/32/16 renders, silhouette, layer decomposition, palette, light direction, positive style tags, and explicit failure tags. O-terra adds reference-to-rule mappings ("all foreground objects use a 3/4 top-left view; no ambient shadow detached from contact edges"). O-sol adds edge density and the 16/32px crops.

3. **In-context exemplars are not durable.** *Single-sourced — O-terra, stated most clearly.* "In-context images do not create durable weights; they condition one run." O-terra separates three things routinely conflated as "learning style": run-time conditioning (no persistent weights), generator adaptation (LoRA/adapters), and **critic calibration** (training a judge to rank by a visual grammar). For an SVG-refinement agent the first and third are the valuable ones.

### The one form of training that does apply: calibrate the judge, not the generator

**Single-sourced — O-sol.** VAB (arXiv 2605.12684) reports ~2,000 expert examples brought a 35B model near a 397B open model on comparative aesthetic judgement. O-sol's conclusion: *"A task-specific judge is the more architecturally aligned future investment."* Codex corroborates the direction with a different work — VisJudge (arXiv 2510.22373): on 3,090 expert-annotated non-photographic visualizations, GPT-5 scored MAE .553 / correlation .428 against experts, while the specialized VisJudge reached MAE .421 / correlation .687.

*Synthesised:* two independent works, in two different visual domains, both find that modest domain-specific supervision of a **judge** beats a much larger general model. Neither is about icons. But this is the only training investment in the panel whose mechanism survives the move from diffusion to SVG authoring — because a judge consumes rasters either way.

---

## 2. How to compare two images reliably

### This loop's own result, and what explains it

Measured here: crude metrics (SSIM, edge F1, luminance delta) failed to reproduce three of four defects a human named by eye, and **inverted** the fourth. The panel offers four distinct mechanisms. All four are single-sourced, but they are mutually reinforcing and three come from peer-reviewed work.

**(a) Spatial-frequency mismatch — explains the three missed defects.** *Single-sourced — Codex, citing Kauffmann et al. 2014 (Frontiers, peer-reviewed).* Human vision extracts coarse global shape from **low** spatial frequencies first, and only later resolves high-frequency detail. SSIM and edge F1 are high-frequency-weighted by construction. A defect a human names at a glance ("the mass sits wrong", "it reads soft") lives in a frequency band those metrics barely sample. Codex's operational consequence: small-size tests must be **actual raster outputs, not a zoomed 1024px image**, and blur/downsample checks are first-class, not decorative.

**(b) Context-blindness — explains why a composite cannot localise anything.** *Single-sourced — Codex, citing Kim et al., CVPR 2025 (AugCLIP).* Preservation metrics (LPIPS, DINO, CLIP-I) ignore the requested modification; CLIP-T ignores source preservation; **and fixed combinations of them remain context-blind.** A global metric has no way to distinguish the region that *should* change from the region that *should* stay, so a local defect is averaged into nothing. This is the sharpest mechanistic account in the panel of why a composite fidelity score is structurally incapable of reproducing a human's defect list. *(Caveat: this is the run's one dead URL — the CVF `/papers/*.pdf` path 404s. The `/html/` sibling that Codex also cites resolves. The paper is real; the link is wrong.)*

**(c) Blurry structural averaging — the most likely explanation for the inversion.** *Single-sourced — O-sol.* Its metric table states SSIM *"penalizes benign translations and rasterization differences; may reward blurry structural averaging."* If the human-named defect was softness or a lost edge, SSIM can score the **blurrier** candidate higher, because reducing local variance reduces local variance mismatch. That is an inversion by construction, not by accident. O-terra corroborates the adjacent half: *"A pixel residual over-penalizes benign antialiasing, rasterization variance, and intentional SVG simplification"* — the false-positive side of the same coin.

**(d) Two concrete measurement bugs, either of which alone can invert a score.**
- **Luminance delta pooled over antialiased boundaries.** *Corroborated — O-sol + Codex.* Both require colour/luminance statistics be computed **inside stable interior region masks, excluding antialiased boundaries** (O-sol rule `COL-01`; Codex "region-matched CIEDE2000"). In a vector icon most of the raw difference energy sits in the boundary pixels, so a global delta measures rasterizer behaviour, not design.
- **Perimeter-to-area is scale-dependent.** *Single-sourced — Codex, citing Pelli et al.* Perimetric complexity must be **perimeter² / ink area**, not perimeter/area, "because the latter changes with scale." Any edge-density or complexity term computed at a fixed raster size against a reference at a different effective scale is measuring scale, not shape.

### What a VLM judge can and cannot see

**Corroborated — 4 of 5 backends, 6+ distinct primary benchmarks, 5+ independent domains.** This is the best-evidenced finding in the panel.

| Benchmark | Result | Backends |
|---|---|---|
| BLINK (3,807 Qs, 14 CV tasks) | human **95.70%**, GPT-4V **51.26%**, Gemini **45.72%**; random 38.09% | O-sol, Codex, O-terra |
| BlindTest (elementary geometry) | 4 VLMs averaged **58.57%**, best 74.94% (O-sol, G-max) — **or 58.07%, best 77.84%** (Codex) | O-sol, Codex, G-max |
| MuirBench (multi-image, 2,600 Qs) | GPT-4o **68.0%**, Gemini Pro **49.3%**, open models <33.3% | Codex, O-terra |
| ColorBench (32 VLMs, 11 tasks) | best proprietary **55.4%**, **59.6%** with CoT | O-sol, Codex, O-terra |
| Q-Bench (low-level vision) | MLLM low-level ability "unstable and imprecise" | O-terra |
| NaturalBench (10,000 samples, 53 VLMs) | leading models lag humans (>90%) by 50–70% | O-sol, Codex |
| MMVP | CLIP-blind pairs: visibly different images map close in CLIP space | O-sol, Codex, G-max |

**Note the BlindTest disagreement.** O-sol and G-max report 58.57% / 74.94%; Codex reports 58.07% / 77.84% from the same arXiv ID (2407.06581). Codex dates it *"July 2024; revised March 2025"* — the paper was revised and the figures moved. **Do not average, and do not quote either figure as authoritative.** Cite the range or cite the paper version.

The operational reading, stated in near-identical terms by O-sol, Codex, O-terra and G-max: **treat the VLM as a hypothesis generator and region prioritiser, never as the measurement system.** Geometry, colour, connected components, edges, blur, contrast and small-size survival bypass the VLM entirely. O-sol makes it a hard rule: *if a numeric value is not present in `measurements.json`, the VLM must describe it qualitatively or request a tool measurement* — it may not invent one. O-sol quantifies the gap: specialist CV systems outperform the best VLM by **18–57 points** on evaluated BLINK subtasks.

### Interventions with measured effect

**Corroborated — 3 backends, distinct primary works.**

| Technique | Measured gain | Backends |
|---|---|---|
| Crop-and-zoom (ZoomEye) | +34.57 pts V\*Bench, +17.88 HR-Bench (O-sol); 76.96→89.01 aggregate (Codex) | O-sol, Codex |
| Reference-object reasoning (SpatialPrompt) | +47 Gemini 1.5 Pro, +22 Flash, +30 GPT-4V on Q-Spatial | O-sol |
| Set-of-Mark region labels | zero-shot GPT-4V beat a fully fine-tuned RefCOCOg model | O-sol, Codex, G-max |
| Visual Sketchpad (marks + tools) | +8.6% avg on vision tasks; 83.9% BLINK spatial | Codex |
| Textual scene measurements vs visual embeddings | +18% on PTR | Codex |
| SCAFFOLD dot-matrix coordinate overlay | beat SoM on 3 of 4 metrics | G-max |

Two cautions inside this otherwise-clean picture:
- **Do not ask the VLM to emit raw coordinates.** *Single-sourced — O-sol, citing the SoM paper itself.* Requesting raw coordinates can *impair* performance. Use named 4×4 or 8×8 cells and region IDs; get numbers from code.
- **Do not over-mark.** *Single-sourced — Codex.* "Dense marks can occlude precisely the detail being judged." Label semantically meaningful regions, not every SVG path.

### The one genuine disagreement: side-by-side vs sequential

**This is the finding.** The panel splits, and the split is decidable.

| Position | Backend | Evidence |
|---|---|---|
| Side-by-side **degrades** accuracy in 9/10 visual domains, −3.1pp (71.3→68.2); sequential is superior | **G-fast** | One preprint: `arxiv.org/html/2603.07888v1` ("VLM-SubtleBench") |
| Side-by-side is harmful; it "exacerbates the VLM's poor spatial memory" | **G-max** | Asserted; supporting cite is an opaque redirect |
| Use **aligned side-by-side as the default**; never rely on sequential for fine comparison | **O-terra** | Medium confidence, and explicitly `INSUFFICIENT_EVIDENCE` — no controlled study found |
| **No controlled study exists.** Provide one compact composite *plus* the two originals separately | **O-sol** | `MISSING_DATA`. Cites MMNeedle for the adjacent risk: GPT-4o fell 97.0%→26.9% when image density rose to ~160 sub-images |
| **No controlled primary study found.** Prefer a single composite for registration, but validate internally | **Codex** | `MISSING_DATA` |

**Which evidence is stronger:** the three backends that searched for a controlled study and reported failing to find one (O-sol, Codex, O-terra) outweigh the one that produced a single uncorroborated preprint. G-fast's `2603.07888` is cited by **no other backend**, despite three others searching the same literature on the same question in the same week. Its URL resolves, but resolution proves the page exists, not that it says what G-fast says it says — the verification tool states this limit explicitly.

This matters beyond one design choice: **G-fast's most distinctive claims all rest on arXiv IDs no other run found** (`2603.07888`, `2604.22851`, `2605.24306`, `2603.24224`, `2606.08893`, `2604.13602`, `2606.30219`). Its citations verify clean (29/29, 0 dead), so this is not a fabrication finding — but every headline number G-fast contributes is single-sourced to a paper the rest of the panel did not surface. Treat G-fast as a lead-generator, not a corroborator.

**Practical resolution:** the disagreement is about *presentation*, and all five backends agree on what actually moves the needle — crops, residual maps, region labels and machine measurements. Ship aligned side-by-side plus the separate originals plus crops (the O-sol position, which is a superset), and put the ablation on the backlog. All three of O-sol, Codex and O-terra name this exact ablation as a recommended next step.

### Residual maps: evidence, not verdict

**Corroborated — 4 backends, one dissent.** O-terra, Codex, O-sol and G-max all treat difference maps as *evidence supplied to the critic*. O-terra: "Difference maps should be treated as evidence supplied to the VLM, **not as the final fidelity metric**." Codex: "Never feed only an undifferentiated heatmap" — generate alpha, edge, luminance and colour residuals **separately**.

**G-fast dissents and is wrong.** Its comparison table rates difference-map overlays as having `Non-existent` risk of proxy optimization, calling them "objective mathematical measurement." That is precisely the error that produced this loop's failure: a deterministic number is not an unhackable one, and G-fast's own report elsewhere documents Goodhart's law. Four backends against one, and the dissent contradicts itself.

O-sol's residual set (the most complete): signed alpha difference; edge residual (reference edges cyan / candidate magenta / overlap white); distance-transform heatmap; ΔE2000 heatmap in CIE Lab; luminance residual after blur **at two scales**, separating broad light-model errors from high-frequency texture. That two-scale split is the direct operational answer to mechanism (a) above.

**Not established:** O-sol states plainly that *no* controlled benchmark isolating the effect of residual maps on VLM critique was found. The technique is well-motivated and universally recommended; its measured benefit is unproven.

---

## 3. How to run the loop better

### Champion–challenger, best-ever checkpoint, blind order-reversed gating

**Corroborated — all 5 backends, converging on the same state machine.** This is the panel's consensus fix and it maps exactly onto the observed failure.

Shared rules:
- **Return the best-ever checkpoint, not the latest.** Codex stage 8, verbatim: *"Return best-ever checkpoint, not latest."* O-sol rule `LOOP-01`: *"Never promote the latest automatically; only a challenger that defeats the champion is saved."* O-terra: *"Never overwrite the best human-confirmed version."*
- **Promotion requires winning a blind, order-reversed pairwise comparison.** O-sol's concrete rule for a solo developer: two independent judges, each comparison run in both A/B orders, challenger must win **≥3 of 4 non-tied judgements**; any 2–2 split, order inconsistency or judge disagreement retains the champion. Codex: *"An inconsistent result is 'no decision,' not permission to use the higher metric."*
- **The selector must be blind to round number, metric trajectory, filenames and provenance.** Codex and O-sol both state this; O-terra and G-max both call for a cold-context verifier.
- **Stop after two non-winning rounds.** O-sol `LOOP-02`, Codex stage 7.
- **The final tournament must include an early checkpoint.** O-sol `LOOP-03`: compare baseline, champion, best metric candidate, and one early human-preferred round. *"Directly tests whether optimization moved away from preference."*

### Round count: disagreement, and everyone flags their number as policy

| Backend | Recommendation | Basis |
|---|---|---|
| Codex | max **3** corrective rounds | IntroSVG (3 rounds); Self-Refine used max 4 iterations |
| O-sol | **3 structural + 1 optional polish** | Explicit: *"no defensible universal empirical number"* |
| G-max | **3–4** cap | Degradation threshold asserted at round 4 |
| G-fast | **2–4** cap | `dev.to` blog + `emergentmind.com` |
| O-terra | **4–8** targeted passes **per branch**, with branching | Jaiswal 2026 (arXiv 2601.15286) |

**Do not average to "5."** The two backends presenting a number as established (G-fast, G-max) have the weakest sourcing in the panel — blog-tier for G-fast, redirects for G-max. The three with real sourcing (O-sol, Codex, O-terra) all explicitly label their number an operational policy. O-terra's higher figure is the only one attached to a measured experiment: at total budget 16, **8 iterations plus 2 parallel candidates slightly beat 16 purely sequential iterations** — which is an argument for *branching*, not for more serial rounds, and O-terra says so ("This is relevant evidence, but it is not an icon-specific optimum").

**Convergent practical answer (synthesised):** ~3–4 structural rounds on any one lineage, branch rather than extend, and let the stopping rule — not the round cap — be what actually terminates the loop.

### Reward hacking and proxy gaming

**Corroborated — 4 backends, multiple distinct primary works.**

The most on-point evidence in the entire panel is **single-sourced to O-terra**: Pan et al. 2024 (arXiv 2407.04549), *Spontaneous Reward Hacking in Iterative Self-Refinement* — experimentally, **evaluator ratings improved while human judgement stagnated or deteriorated**, in an iterative self-refinement loop. O-terra is honest that the task domain is textual, but "the causal structure — generator optimizing an imperfect evaluator in an iterative loop — matches the reported failure mode." That is this loop's failure, named and reproduced in a controlled setting.

Second most on-point, also **single-sourced (Codex)**: the IVT audit, Tripathy & Krishnan 2026 (arXiv 2606.13156). A reported **+2.4pp iterative gain vanished entirely under deployable stopping rules**; self-confidence correlated only **r≈.22** with correctness; and **stopping at the initial output beat every shippable iterative policy.** The lesson is not "don't iterate" — it is that an improving trajectory is worthless if the system cannot identify its own best step without hidden ground truth. Codex's framing: *"The loop had an optimizer, but no trustworthy verifier."*

**Corroborated across two backends on the same page:** Hong et al. 2026 (arXiv 2601.03468) — reward ensembles are **only partially** protective; shared artifacts can exploit multiple rewards at once. Cited independently by O-terra and Codex. This kills the tempting fix of "just add more metrics to the composite."

Also corroborated: intrinsic self-correction degrades without external feedback (Huang et al., arXiv 2310.01798 — O-sol, Codex, G-max) versus Self-Refine's ~20pp average gain with iterative feedback (arXiv 2303.17651 — O-sol, Codex). O-sol resolves the conflict correctly: *"The difference is whether feedback carries usable external signal and whether a checkpointed selector rejects regressions."*

**Leading indicators of proxy divergence** — O-terra's table is the most usable artifact in the panel and is worth transcribing into the skill nearly verbatim:

| Signal | Interpretation | Response |
|---|---|---|
| Composite rises, blind A/B win rate falls | Direct proxy divergence | Freeze metric; restore last human-confirmed champion |
| Critic keeps asking for more contrast / sharper highlights / more detail | Generic-aesthetic reward exploitation | Add saturation, highlight-area and edge-density **ceilings** |
| Pixel similarity rises while 32px legibility worsens | Overfit to high-res raster detail | Raise small-size gate weight; simplify |
| VLM praises output but residuals show persistent geometry error | Narrative displaced measurement | Reject the critique; fix geometry |
| Generator and judge agree strongly across rounds | Shared blind spot / self-confirmation | Different model family, specialist metric, or human |
| Later edits touch many regions with no localized error reduction | Drift | Enforce minimal-diff edits and region locks |

Additional anti-Goodhart controls, corroborated across backends:
- **Pareto vector, never a weighted total.** O-sol ("gated Pareto vector"), Codex ("Maintain a Pareto vector, not a weighted total"), O-terra (error budget + protected metrics), G-max (separate L2 / edge / code-efficiency terms). Four backends.
- **Small-size failure is a veto, not a penalty.** O-sol `LEG-02`, Codex, O-terra. Three backends. A candidate either survives 16/32px or it fails, regardless of its high-resolution score.
- **Source anti-cheat.** *Single-sourced — O-sol, and unusually concrete.* Reject `<image>`, `foreignObject`, scripts, external URLs, data URLs and unapproved filters; reject invisible full-canvas elements and near-zero-opacity overlays. Otherwise the generator can embed or trace the reference raster. G-max supplies the vector-specific version of the same attack: an agent can inflate a pixel metric to near-perfect by emitting thousands of microscopic semi-transparent polygons that mimic a blurred shadow — hacking the metric while destroying the vector.
- **Two rasterizers and randomized subpixel phase.** *Single-sourced — O-sol.* Detects candidates tuned to one antialiasing phase or one renderer's filter quirks.
- **Actively test the evaluator with sabotaged candidates.** *Single-sourced — Codex.* Feed it tiny translations, added texture, inflated contrast, blurred edges, excess highlights, duplicated paths. If the judge rewards any of them, the judge is the bug.

### Judge-panel construction

**Corroborated — 4 backends.** Pairwise blind comparison beats scalar scoring and beats batch ranking.

- MLLM-as-a-Judge: GPT-4V averaged **79.3%** human agreement on pairwise comparison vs **69.9%** on score evaluation (O-sol, `mllm-judge.github.io`; Codex, arXiv 2402.04788 — same work, one source).
- VIEScore reached Spearman **ρ=.40** with humans against human-to-human **ρ=.45**, but "specifically struggled on editing rather than generation tasks" (Codex, arXiv 2312.14867). **This distinction is the important one:** matching an existing reference icon is an *editing/reconstruction* task, which is where the judge is weakest. Single-sourced but directly on point.
- VAB 2026: the strongest system identified both best and worst image consistently in only **26.5%** of tasks, versus **68.9%** for human experts (O-sol, arXiv 2605.12684).
- **Documented judge biases:** position bias (one LLaVA batch-ranking setup reproduced the example `ABCD` order **88.2%** of the time), verbosity bias (semantically identical but longer answers gained +0.6 from GPT-4V, +0.75 from Gemini), and self-preference — a 2026 study over **1.29M caption-score pairs from 12 MLLMs** found systematic self- and model-family preference (O-sol). Codex adds multi-image position bias: proprietary models are strongest on the first and last image and weakest in the middle (arXiv 2503.13792).

**Consequence, stated by O-sol, Codex, O-terra and G-fast:** the judge must not be the model that generated the candidate, every consequential comparison must be repeated with A/B reversed, and critic and selector should be separate roles in different model families where possible.

**Conflicting evidence worth carrying:** MJ-Bench reports GPT-4o at **70.9%** overall with strong performance on some image-quality distinctions, while VAB reports **26.5%**. O-sol resolves it correctly — it is task scope, not contradiction: *detecting blur, distortion or misalignment is far more objective than ranking closely-matched artistic quality.* Use the VLM judge for the former; do not trust it for the latter.

---

## 4. What the panel says about macOS icon grammar

Apple primary sources outrank commentary. Sorting on that basis:

### Corroborated, first-party, act on it

- **1024×1024 square source canvas for Mac.** All five backends.
- **Layered source — background plus one or more foreground layers; the system composites them.** O-sol, O-terra, Codex.
- **Do not bake the mask.** *Three backends, first-party.* O-sol: "omit the canvas mask because the system applies it." Codex: "Export square, unmasked layers; **a baked rounded mask damages system highlight rendering**." O-terra: test both unmasked source and system-masked output.
- **Do not bake system-owned material.** ***Four backends — the strongest macOS finding in the panel.*** Apple instructs designers to remove blur, shadow, specular, opacity and translucency decisions that Icon Composer owns (O-sol, citing `developer.apple.com/documentation/xcode/creating-your-app-icon-using-icon-composer`). Codex: "Keep source art flat, opaque and controllable where Icon Composer should supply material effects." O-terra: "Do not bake arbitrary fake highlights that fight system highlights." G-max: "If the skill is attempting to draw these complex specular highlights manually inside a raw SVG file, **it is fighting the OS rendering engine**."
- **Light angle is vertical, from above.** O-sol and Codex both attribute this to `developer.apple.com/icon-composer/` ("vertical light angle from above", with crisp edge-preserving highlights). G-fast asserts the same "12 o'clock" fact but sources it to `linearity.io` (a general design blog) and a **Motion app manual** — the fact is right, its sourcing is not; use the first-party attribution.
- **Convert text to outlines; prefer SVG/PDF vectors.** O-sol, Codex.
- **All appearance variants must work.** Codex is the most current and specific, from the June 8 2026 HIG: default, dark, clear-light, clear-dark, tinted-light, tinted-dark. O-sol says Default/Dark/Mono; O-terra says default/dark/clear/tinted. Use Codex's six.
- **Clearly defined foreground edges, not feathered contours; avoid extremely thin lines; prefer a minimal number of shapes; validate sRGB / Gray Gamma 2.2 / Display P3.** Codex, from the HIG.

### Disagreement 1 — layer count

- **Codex:** Apple permits **one to four groups and calls four the useful upper bound**, citing WWDC25 session 361 ("Create icons with Icon Composer") directly.
- **O-sol:** "Apple's Landmarks sample uses four layers, but that is an implementation example, **not a documented universal requirement**," and states flatly that no official published maximum layer count exists.

**Which is stronger:** most likely both are correct and they searched different artifacts — Codex found it stated in a WWDC session, O-sol looked in the written HIG and correctly reported it absent there. Codex's claim is more specific and names its source. **Treat four as the working ceiling**, and record that it comes from a WWDC session rather than the written guidelines.

### Disagreement 2 — macOS 27, and it changes the target

- **Codex** cites **`developer.apple.com/videos/play/wwdc2026/102/?id=707`** — first-party Apple — for macOS 27: icon rendering is **sharper and more defined**, refraction is **selective**, multiple Liquid Glass layers are permitted, and already-adopted icons update automatically without recompilation. This is the only first-party macOS 27 source in the entire panel and it resolved live.
- **O-sol** explicitly reports the opposite: `INSUFFICIENT_EVIDENCE` — *"No official Apple macOS 27 icon specification or final release documentation surfaced... 'Golden Gate' claims remain beta-era secondary reporting and should not be encoded as durable skill rules."* It relies on MacRumors and Rogue Amoeba.

**Which is stronger: Codex.** Under the brief's own rule — Apple primary outranks commentary — a resolving first-party WWDC26 session beats an absence-of-evidence finding plus trade press. O-sol's caution should be read as "I did not find it," not "it does not exist." **Verify the WWDC26 session directly before encoding it**, but plan on the direction being real.

**Why this is the most decision-relevant item in this section:** Apple's 2026 change is a *correction* of the 2025 treatment — away from blur and washed-out detail, toward sharper edges and selective refraction. Codex draws the inference the skill needs: *"Optimizing glass effects without protecting silhouette and brand distinctiveness can therefore improve platform-style metrics while degrading the icon."* That is a description of this loop's failure mode written in Apple's own vocabulary.

### Reference fidelity and platform conformity are two different objectives

**Corroborated — O-terra and O-sol independently, and both prescribe the same fix.**

O-terra: if the raster reference is an older skeuomorphic macOS icon, faithfully reproducing it may **conflict** with Apple's current icon language; one SVG cannot be assumed to maximise both. O-sol identifies the specific trap: without separate modes, *"the agent may accurately copy a flattened Liquid Glass screenshot and then cause Icon Composer to apply the same material a second time."*

Both prescribe two explicit output modes:
1. **Reference-fidelity preview** — one flattened SVG/render intended to resemble the supplied raster.
2. **Production Icon Composer package** — clean layered SVGs plus a manifest, with system-owned glass, mask and shadow omitted.

O-sol's suggested package layout: `preview.svg`, `layers/00-base.svg … 30-intrinsic-accent.svg`, `icon-manifest.json`, and a `validation/` directory holding default-light, default-dark, mono, 16/32px renders and `measurements.json`.

### What makes an icon good, per the panel (first-party plus icon-perception literature)

Codex's one-line synthesis is the best in the panel: **"A good current Mac icon is distinctive before it is glassy: recognizable silhouette and colour hierarchy first; simple layered depth second; system material last. A generic icon usually reverses that order."**

Supporting behavioural evidence, corroborated across backends and independent of Apple:
- Concreteness is the strongest predictor of semantic distance; **familiarity with the icon style** is the strongest predictor of aesthetic appeal; the direct aesthetics-usability effect is weak once those are controlled (O-sol, ScienceDirect S1071581926000741, 2026).
- Concreteness significantly improved function understanding with a large effect, **η²ₚ = .30**; simpler variants were rated more appealing, but **complexity did not independently improve function understanding** (O-terra, Collaud et al. 2022).
- **Flat icons support faster visual search; skeuomorphic icons produce better recall** — 64 icons, 40 participants (Codex, Shen et al. 2024). Codex flags the resulting conflict honestly: Liquid Glass adds physical depth while Apple simultaneously advises simpler, flatter source artwork, so the right answer is neither maximal flatness nor maximal realism.
- **Familiarity compensates for complexity** — repeated exposure improved both search and recall, and the initial complexity disadvantage diminished with experience (Codex, Wang et al. 2018). Consequence: *"simpler" is not automatically "more recognizable"; deleting a familiar distinguishing feature may reduce identity.* This is a direct counterweight to any simplification-driven metric.
- Automated structural measures track perceived complexity: structural variability **r_s=.65**, edge information **r_s=.64** against human ratings (Codex, Forsythe et al. 2003).

### Practitioner criticism — real in direction, thin in citation

Three backends surface the "squircle jail" critique (O-sol via Ars Technica and Rogue Amoeba; Codex via Macworld and MacRumors; G-max via redirects to 9to5mac and mjtsai). Consistent in direction, individually weak: O-sol's Rogue Amoeba claim is the **one claim in the panel that the verifier flagged as having nothing else supporting it**, and Codex's Macworld URL also failed. Both failures look like local DNS blocking rather than fabrication.

**Do not encode practitioner criticism as skill rules.** The reliable evidence that the criticism landed is Apple's own 2026 sharpening — a first-party source saying the same thing.

---

## 5. What was NOT established

Every item here was searched for by at least one backend and explicitly reported missing. Two or more backends independently reporting the same gap makes it a real gap, not a search failure.

**Reported missing by 3+ backends:**
- **No icon-specific benchmark of reference-conditioned macOS SVG refinement** with expert pairwise judgements, small-size recognition and geometry ground truth. O-sol, Codex, O-terra. Codex: *"This is the largest practical evidence gap."*
- **No empirical optimum for visual self-refinement round count.** O-sol, Codex, O-terra.
- **No controlled comparison of presentation format** (sequential vs side-by-side vs overlay vs difference map) for fine-grained visual critique. O-sol, Codex, O-terra. Contradicted only by G-fast's single uncorroborated preprint.
- **No controlled comparison of a written style rubric against equally informative visual exemplars.** O-sol, Codex, O-terra. So the rubric-plus-corpus recommendation everyone makes is an *implementation inference, not an empirical winner* (Codex's own words).
- **No quantitative corpus analysis of Apple's current first-party macOS icons** — palette, layer counts, edge density, motif frequency, silhouette complexity. O-sol, Codex, O-terra, G-max. Codex adds a trap worth knowing: **Apple's 327,879-icon machine-learning corpus is small interface glyphs, not app icons, and must not be used as evidence about app-icon style.**

**Reported missing by 2 backends:**
- **No validation of SSIM, LPIPS, DISTS, CLIP-IQA or any weighted combination against human preference for stylized app-icon SVG**, at any size. O-sol, Codex. Existing evidence comes from photographs, generated images, image editing, charts, or generic SVG.
- **No official Apple numeric minimum stroke width, gap, contrast, or maximum layer count** for current layered icons. O-sol, Codex.

**Single-sourced gaps worth carrying:**
- **No measured benefit of residual / edge-XOR / signed-distance / ΔE heatmaps when supplied to frontier VLM critics** (O-sol). The whole difference-map recommendation is well-motivated and unproven.
- **No independently replicated study of self-preference bias for a code-generating VLM judging its own SVG icons** (Codex). *"The final skill should assume this bias exists until tested."*
- **Limited direct benchmark evidence on VLM judgement of specular direction, refraction, translucency and physically coherent shading** (Codex). General perception failures justify caution but do not quantify the material case specifically — which is exactly the case this skill needs.

**Claims too thin to act on:**
- **G-fast's LoRA prescription** (15–30 images, DuoLoRA/EST-LoRA fusion). Wrong pipeline; blog-tier sources; contradicted by four backends.
- **G-fast's "difference maps have non-existent proxy-optimization risk."** Contradicted by four backends and by its own report.
- **G-fast's side-by-side degradation figures** (9/10 domains, −3.1pp). One preprint no other run found.
- **G-max's "L2 + Canny + DreamSim/DINO ensemble is the most resilient reward signal."** G-max labels this **Low Confidence** itself, and Hong et al. (O-terra + Codex) shows ensembles are only partially protective.
- **Any exact BlindTest figure.** O-sol/G-max and Codex disagree (58.57/74.94 vs 58.07/77.84) because the paper was revised.
- **Anything about macOS 27 sourced to trade press.** Use the WWDC26 session or nothing.

### The fourth question: bad loop, or bad model of a macOS icon?

**Disagreement, with a decisive test supplied by O-sol.**

- **O-sol:** the 19-round failure proves *an evaluation-loop defect*, not by itself a deficient style model. Its discriminator: *"if all first-round outputs remain generic despite correct geometry and palette, style knowledge is the next bottleneck; **if early rounds are preferred and later rounds regress, the loop — not the style prior — is the dominant fault**."*
- **Codex (Medium confidence):** *"The skill's underlying concept of 'Mac-like' is probably part of the gap"* — because the skill may be optimizing toward a 2025 blur aesthetic that Apple itself walked back in 2026.
- **O-terra:** a third mechanism — reference fidelity and platform conformity are conflicting objectives, and a single scored artifact silently trades one for the other.

***Synthesised:*** this loop's observed signature is *early rounds preferred, later rounds regress*. By O-sol's own discriminator, **the loop is the dominant fault**, and the style prior is a real but secondary problem. Fix selection, rollback and measurement first; then run the corpus-vs-rubric ablation to size the remaining style gap. This ordering is the panel's strongest practical guidance and it is derived, not quoted — treat it as synthesised.

---

## The five changes to make to the skill

Ranked by expected effect. Each names the finding and the file.

### 1. Replace score-based promotion with champion–challenger and a best-ever checkpoint
**Files:** `references/fidelity-loop.md`, `scripts/judge_panel.py`, `scripts/fidelity.py`

**Finding:** all five backends converge on this state machine, and it is the direct fix for "composite rose, humans preferred earlier." Pan et al. 2024 (O-terra) reproduces the exact failure experimentally; the IVT audit (Codex) shows an improving trajectory is worthless without a trustworthy stopping rule — its +2.4pp gain vanished entirely under deployable stopping, and stopping at round zero beat every shippable iterative policy.

**Concretely:** keep an immutable checkpoint per promotion; promote only on a blind, order-reversed pairwise win (O-sol's rule: ≥3 of 4 non-tied judgements; any 2–2 split or order inconsistency retains the champion); hide round number, metric trajectory, filenames and provenance from the selector; stop after two non-winning rounds; cap at ~3 structural rounds plus one polish; **return the best-ever checkpoint, never the latest**; and make the final tournament include an early checkpoint alongside the champion.

**Acceptance test — three backends name it independently** (O-sol #3, Codex #5, O-terra #1): replay the existing 19-round trace blind, with iteration numbers and metric values hidden, and check whether the new policy selects the checkpoint humans actually preferred. That is the fastest falsifiable test of the whole rewrite.

### 2. Demote every metric to a diagnostic; ship a gated Pareto vector and fix three measurement bugs
**Files:** `scripts/fidelity.py`, `references/fidelity-loop.md`

**Finding:** four backends independently reject a weighted composite (O-sol "gated Pareto vector… no one metric should be allowed to promote a revision"; Codex "Never optimize a scalar 'fidelity' blend"; O-terra error-budget + protected metrics; G-max separate terms). Kim et al. CVPR 2025 (Codex) supplies the mechanism: preservation metrics ignore the requested modification and **fixed combinations remain context-blind** — which is precisely why the composite could not reproduce a human's defect list. Hong et al. 2026 (O-terra + Codex, same paper, two backends) forecloses the "add more metrics" escape: ensembles are only partially protective.

**The three bugs to fix, which together plausibly account for the 3-missed-and-1-inverted result:**
- Compute ΔE2000 and luminance **inside stable interior region masks, excluding antialiased boundaries** (O-sol `COL-01` + Codex, corroborated). A global luminance delta in a vector icon measures the rasterizer.
- Use **perimeter² / ink area** for complexity, never perimeter/area — the latter changes with scale (Codex, single-sourced but a plain mathematical fact).
- Add a **two-scale blurred luminance residual** separating broad light-model error from high-frequency texture (O-sol), because human defect-spotting runs on low spatial frequencies first (Codex / Kauffmann 2014) and SSIM and edge F1 barely sample that band.

Make small-size survival a **binary veto, not a weighted term** (O-sol `LEG-02`, Codex, O-terra — three backends), and add explicit ceilings on saturation, highlight area and edge density to close the "more contrast, sharper highlights" exploitation channel (O-terra).

### 3. Stop authoring system-owned material; split reference-fidelity from production output
**Files:** `SKILL.md`, `references/material-recipes.md`, `references/icon-directions.md`

**Finding:** four backends, all citing Apple first-party, say the source must not bake blur, shadow, specular, translucency or the mask — Icon Composer owns them. G-max: drawing them by hand means "fighting the OS rendering engine." O-sol and O-terra both independently identify the double-application trap: copy a flattened Liquid Glass render, then let Icon Composer apply the same material again. Codex's WWDC26 first-party source shows Apple moving toward **sharper edges and selective refraction** — so a skill tuned to reproduce 2025 blur is optimizing toward a target Apple has already corrected.

**Concretely:** two output modes (flattened reference-fidelity preview; layered unmasked production package with manifest and a `validation/` directory covering all six appearance variants and 16/32px renders). Treat four groups as the working layer ceiling. Move hand-authored specular and glass recipes out of `material-recipes.md` into intrinsic form shading only. This is also the most likely partial answer to "the generator doesn't know what a macOS icon looks like" — it may know perfectly well, and be drawing things it should leave to the system.

### 4. Give the critic an evidence packet, and forbid unmeasured claims
**Files:** `scripts/judge_panel.py`, `references/fidelity-loop.md`

**Finding:** all five backends. The measured gains are real and large — ZoomEye +34.57pts on V\*Bench (O-sol) / 76.96→89.01 (Codex); SpatialPrompt +20–47pts (O-sol); Set-of-Mark beating a fully fine-tuned grounding model zero-shot (O-sol, Codex, G-max); Visual Sketchpad +8.6% (Codex); textual scene measurements beating visual embeddings by 18% (Codex). Against that, specialist CV outperforms the best VLM by 18–57 points on BLINK subtasks (O-sol) — so measurement must bypass the VLM entirely.

**Concretely:** per candidate, emit aligned reference/candidate, a side-by-side composite, the separate originals, five separate residual products (signed alpha, edge overlay in cyan/magenta/white, distance transform, ΔE2000 heatmap, two-scale luminance), region labels on semantic groups, 3–5 crops at ≥4× around the largest residual clusters, a size strip at 128/64/32/16 on light and dark, and `measurements.json`. Then enforce **O-sol's hard rule: if a number is not in `measurements.json`, the critic may not state it** — describe qualitatively or request a tool measurement. Require every observation to name a region ID and every proposed edit to name its expected metric delta and its risked regressions.

Two guardrails: do not ask the critic for raw coordinates (it degrades performance — O-sol, citing the SoM paper), and do not over-mark (dense marks occlude the detail being judged — Codex). Present side-by-side **and** the separate originals rather than picking a side in the unresolved presentation debate.

### 5. Build the annotated exemplar corpus with counterexamples; do not pursue adapters
**Files:** `references/icon-directions.md`, `references/material-recipes.md`, `SKILL.md`

**Finding:** four backends say LoRA/IP-Adapter/StyleDrop/DreamBooth/DPO do not transfer to a hand-authored SVG pipeline; only G-fast recommends them, and it never engaged the transfer question. What does transfer is a retrieved, annotated corpus plus a written rubric — recommended by four backends, with the count unvalidated by all of them.

**Concretely:** store ~24 icons to start (the overlap of O-sol's 24–40 and O-terra's 12–40), retrieve 4–8 per run, and size the corpus by an internal learning curve rather than by importing a number from a diffusion paper. Annotate each with silhouette, layer decomposition, palette, light vector, material treatment, edge density and 16/32px crops. **Include counterexamples** — corroborated independently by Codex and O-sol — as paired "good vs generic" and "good vs overworked" with a one-sentence reason, because without the negative boundary the model imitates squircles, gloss and blue gradients and calls it Liquid Glass.

Record that in-context exemplars condition one run and create nothing durable (O-terra), so retrieval must run every time. If training is ever revisited, the target is a **calibrated judge, not the generator** — VAB's ~2,000 expert examples (O-sol) and VisJudge's expert corpus (Codex) both show modest domain supervision of a judge beating a far larger general model, and a judge consumes rasters regardless of how the SVG was authored.
