# SVG icon fidelity plan

**Status: v2 (2026-08-07), panel complete.** Built from the full deep-research panel (three of six members produced reports: GPT-5.6 with 43 sources, Gemini with 59, Grok with 22; every report read end-to-end, fabrication checks PASS on all three with zero fabricated citations), the fixtures already on disk in this repo, and what mac-design-studio's manual iterations have taught us. The local-claude, local-codex and perplexity members failed on startup at $0 with no reports.

**The goal:** hand-authored Engine A SVGs that match the detail, fidelity and material quality of the Engine C diffusion rasters, reached by an eval harness that can score an SVG against a raster reference and a `/loop` that iterates until it passes, with everything captured as future training data for a vector model better than Arrow 1.1.

---

## 1. Ground truth: what the gap actually is

Across every icon shipped in this marketplace, the pattern is consistent: **at equal audit scores, the user judged the raster's material better than the vector's.** The gap is not composition (Engine A wins layout, silhouette and 16px survival routinely). It is **material richness**: volumetric shading, texture, lighting, contact shadows, translucency.

The research corroborates this exactly. GPT-5.6's central finding: "SVG realism is principally a representation, grammar, and optimisation-budget problem, not an inherent limitation of SVG." Native SVG can express everything the rasters show (gradient stacks, masks, blur filters, lighting, turbulence); models fail because they author flat paths and single fills. The fix is a grammar that *demands* material construction plus a loop that scores the render against the raster.

### Fixture pairs on disk today

| # | Pair | A (vector) | C (raster reference) | Signal |
|---|------|-----------|----------------------|--------|
| 1 | create-swe-project "First Water" | `plugins/create-swe-project/assets/icon.svg` (11/12, visibly flatter) | `icon-engineC1.png` (10/12, material winner) · `icon-engineC2.png` (8/12, **user shipped this over A**) | Strong |
| 2 | improve-skill "Honed Edge" | `plugins/improve-skill/assets/icon.svg` (rebuilt volumetric 12/12; shaving-curl rebuild in progress) | `icon-engineC-cfd884.png` (9/12) · `icon-engineC-f5665d-2.png` (7/12, user preferred material) | Strong |
| 3 | trawl, compaction-quality, ship-armada, armada-sync, design-review, fledgeling mark | A masters rebuilt toward C across manual iterations | C takes in each `assets/` | Weaker (already converged manually; useful as "solved" references) |

Pair 3's manual rebuilds (trawl v2 to v4, compaction A-v5) are exactly the loop this plan automates, done by hand. Their diffs are the seed for the material recipe library in Phase 2.

---

## 2. What the research settled (evidence base)

Full reports committed beside this plan: `docs/deep-research/svg-fidelity-openai-gpt56.md` (43 sources), `svg-fidelity-gemini.md` (59 sources) and `svg-fidelity-xai-grok.md` (22 sources).

**All three reports agree on:**

- **Hybrid beats pure generation.** LLM owns semantic decisions (layer decomposition, path topology, material assignment); numeric optimisation owns continuous matching (gradient stops, opacities, blur radii, control points). Chat2SVG (CVPR 2025), RLRF (NeurIPS 2025), Render-in-the-Loop (2026) all follow this split. One autoregressive pass produces either clean-but-flat icons or uneditable path soup.
- **No single metric.** LPIPS/DISTS for large-size material similarity; MS-SSIM plus edge/silhouette measures for small-size legibility; CLIP/DINO only as semantic guardrails; a reference-aware VLM rubric for defects numbers miss. All metrics degrade at 32/16px without multi-scale treatment.
- **Loops converge in 3-5 bounded rounds**, and fail by plateau, oscillation, and metric gaming.
- **Distillation from a teacher can't beat the teacher by imitation alone.** It needs extra signal: raster ground truth, accept/reject trajectories, and render-based rewards (RLRF: SFT on 1.7M pairs then render-reward RL on just 16k images took Qwen2.5-VL-7B from LPIPS 16.58 to 3.08 on SVG-Stack-Hard, source-specific scale).

**Hard numbers worth keeping in view:**

- OmniSVG-8B LPIPS on complex illustrations: 0.231 vs DiffVG 0.065 vs plain VTracer 0.035. Clean autoregressive SVG is still far behind trace/optimise pipelines on complex targets.
- **Naïve visual feedback can make things worse**: Render-in-the-Loop measured GPT-5's illustration LPIPS degrading 0.345 to 0.388 when just handed intermediate screenshots. Structured residuals and constrained edit classes are required, not optional.
- IntroSVG caps at three refinement iterations with monotonic gains (FID 29.76 to 26.18); zero-shot loops help frontier models too (GPT-5: 35.87 to 32.68).
- Documented reward hacks from RLRF: shrinking the `viewBox` to cheapen the comparison, and collapsing output length when compactness is rewarded. Both have direct mitigations (harness owns the render canvas; complexity is a constraint, never a reward).

**Gemini's distinct contributions** (not covered by the other two):

- **LPIPS is adversarially gameable.** Iterative optimisers can inject imperceptible high-frequency noise that lowers the LPIPS score without improving geometry (documented stAdv/PGD attacks on VGG-based metrics). DISTS explicitly separates structure from texture and resists this; at 16/32px, MS-SSIM becomes the most reliable scalar because tiny-icon recognition is silhouette and contrast, not deep-feature texture.
- **Judge protocol:** side-by-side VLM comparison carries positional bias; score each candidate independently against the reference (anchor-referenced), and use categorical 0-2 scales per rubric item rather than 1-5 continuous scores, which drift lenient.
- **Context rot is a loop failure mode in its own right:** appending full loss logs, prior SVGs and critiques degrades reasoning by iteration 8-10. Mitigation: on-disk round counters, a hard iteration ceiling, and fresh state-isolated subagents that receive only the failing `<g>` group plus the residual summary.
- **Two more metric-gaming exploits:** invisible overlapping paths that manipulate regional contrast, and base64 raster blobs inside `<image>` tags that mimic the target perfectly while containing no vector work. Static analysis must run before rendering.
- **Distillation recipe:** DPO alone drifts out of distribution; pair it with Statistical Rejection Sampling Optimization (RSO) sampling from the harness-passing policy, and use "Drawing-with-Thought" prefixes (the teacher states layers, lighting direction and primitive relationships before emitting code) so the student learns geometric logic, not syntax. Corpus target for beating Arrow-class: 500k+ curated (prompt, chosen, rejected) triplets.

Source-quality caveat on Gemini: its "coordinate hallucination" framing and Arrow's "33.3% cost reduction" trace to a design blog and vendor/market reporting respectively, weaker than the other reports' conference-paper base. The mechanisms are used here only where they align with peer-reviewed evidence.

**Where the reports disagree** (held loosely, not resolved): Grok expects VLM loops to converge in 3-5 rounds generally; GPT-5.6's evidence says untrained/naïve loops can degrade and only structured ones converge; Gemini adds that unbounded loops reliably fail (oscillation, context rot, leniency plateau). The harness below sides with the structured-loop position (residual maps, one edit class per round, Pareto rollback, hard ceilings) since that design is safe under every reading. On preference optimisation, Gemini favours DPO+RSO for efficiency while GPT-5.6 leans on RLRF-style online render rewards; the plan sequences DPO+RSO first, render-reward RL after, which both endorse.

---

## 3. Phase 1: the icon-fidelity eval harness

The deterministic core. Build this **before** touching the generator; without it we optimise anecdotes.

**Where it lives:** prototype under `tools/icon-fidelity/` in this repo against the fixture pairs; once stable, land it in mac-design-studio (`diolog-plugins`) as `scripts/` so every future icon run gets it. The improve-skill agent's `measure.py`/`compare.py` (in `plugins/improve-skill/assets/`) are the seed: they already compute per-region luminance deltas and polarity checks between A renders and C rasters.

### 3.1 Reference normalisation (once per fixture)

- Fix the render target: 1024px canvas, sRGB, transparent background, premultiplied alpha.
- Raster reference gets an alpha mask and an edge map (Sobel or Canny at fixed thresholds) stored beside it.
- **The harness owns the canvas**: candidate `viewBox` is normalised before render, never trusted (RLRF's documented viewBox hack).

### 3.2 Deterministic rendering

- One designated renderer, version-pinned, for scoring: `rsvg-convert` (already in the audit pipeline) with Chromium via agent-browser as the secondary cross-check. A construct that renders differently across the two is itself a finding (filter/mask support varies).
- Render sizes: **1024 / 256 / 128 / 32 / 16** (the audit sheet's existing ladder plus 1024).

### 3.3 Metric stack per size

| Size | Metrics | What it guards |
|------|---------|----------------|
| 1024 | LPIPS + DISTS (torch, optional install), luminance-field delta (numpy fallback) | Material: shading gradients, highlight placement, shadow softness |
| 256/128 | MS-SSIM + LPIPS | Mid-scale structure and material together |
| 32/16 | Edge F1 vs reference edge map, alpha-mask IoU, MS-SSIM | Legibility and silhouette survival |
| all | Per-region polarity checks (compare.py pattern: "bevel face lighter than flank", "shadow darker than ground") | Directional lighting correctness that pixel metrics under-weight |
| n/a | SVG structural score: parses, no `<image>`, path/filter/byte budget, semantic groups present | Editability, "hand-authored" guarantee |

LPIPS/DISTS are the strongest material signals per all three reports, but they need torch; the harness must run degraded-but-honest without it (luminance fields + MS-SSIM + edges), reporting which tier ran. Where LPIPS and DISTS disagree, DISTS wins: LPIPS is adversarially gameable by high-frequency noise, and DISTS's structure/texture split resists exactly that. At 32/16px, MS-SSIM plus edge measures carry the verdict; deep-feature metrics are out of their calibrated range there.

### 3.4 The gate is Pareto, not a weighted score

Accept a candidate only if:

1. No size's composite regresses beyond tolerance (1024 material gains may not buy 16px legibility losses).
2. Edge F1 and mask IoU at 32/16 stay above fixture minimums.
3. Structural score passes (complexity envelope, no raster embeds, groups intact).
4. VLM rubric (below) has no unresolved major item.

### 3.5 VLM critic rubric (the judged layer)

A Claude critic reads reference + candidate renders + residual maps and returns **localised, non-overlapping defects** against a fixed rubric: silhouette, proportions, layer order, shadow, highlight, material, small-size legibility. Rules from the evidence:

- The critic never sees raw screenshots alone; it gets residual/edge maps too (naïve screenshot feedback measurably degrades output).
- Critic and editor are separate roles; the critic's output is a defect list, never SVG.
- **Anchor-referenced, not side-by-side**: the critic scores the candidate against the reference independently per rubric item (side-by-side pairing carries positional bias), on categorical 0-2 scales rather than 1-5 (continuous scales drift lenient and plateau the loop at "good enough").

### 3.6 Calibration eval (before trusting any of it)

Score the existing fixture pairs and the manual-loop history (trawl v2/v3/v4 against C1). The harness is calibrated when its ranking matches the user's recorded judgements: C over old A on material; v4 over v2; the rebuilt improve-skill A over its flat predecessor. If the composite disagrees with the human record, fix the weights before the loop ever runs. This is the local human-calibration set both reports say is missing from the literature.

---

## 4. Phase 2: the `/loop` self-improvement design

A bounded render-compare-edit loop that runs Engine A to convergence against a raster reference, as a `/loop`-driven session or an agent following the same schedule.

### 4.1 The iteration schedule (bounded, one edit class per round)

| Round | Edit class | Allowed changes | Exit check |
|-------|-----------|-----------------|------------|
| 1 | Coarse structure | Silhouette, centring, object scale, major colour fields | Edge F1 at 1024/256 improves |
| 2 | Material | Gradient stacks, opacity stops, blur radii, highlight/shadow shapes (in `<defs>`-driven layers) | 1024 LPIPS/luminance delta improves, 32/16 stable |
| 3 | Detail | Micro-geometry, texture accents, local control points | ROI residual shrinks, nothing else regresses |
| 4 | Small-size repair | Simplify/strengthen features that alias at 32/16 | 32/16 gates pass, 1024 within tolerance |
| +N | Only while the Pareto gate keeps improving | One class per extra round | Plateau detector (below) |

This mirrors IntroSVG's bounded three-iteration evidence plus a small-size pass our audit ladder demands.

### 4.2 Loop mechanics (anti-oscillation, anti-gaming)

- **Parameterised authoring**: the SVG is built by a script (`build_icon.py` pattern from the improve-skill rebuild), so edits are named parameter changes, not free-form path surgery. This is our local substitute for DiffVG: a human-legible parameter space the editor can search and the log can record.
- **Static analysis before every render**: reject `<image>` tags (the base64 mimic exploit), invisible/fully-overlapped paths, and anything over the path/filter/byte budget, so gaming is caught before a metric ever sees it.
- **Edit-signature hashing**: reject an edit whose rendered diff is negligible or that repeats a previous signature (Render-in-the-Loop's Render-and-Verify).
- **Rollback on reject**: failed candidates are recorded (they're training data) and the loop restarts from the accepted state.
- **Hard ceiling and on-disk state**: a round counter on disk, a hard iteration cap (10), and a plateau rule: two consecutive rejected rounds ends the loop or branches to a fresh scaffold; never grind one path.
- **Context isolation**: the loop controller keeps a compact state file (accepted SVG, metric history, open defects) and hands each round's editor a fresh context with only the failing layer group plus the residual summary, never the accumulated transcript (context rot degrades reasoning by iteration 8-10).
- **Complexity as constraint**: path/byte budget is a hard cap, never a reward (RLRF's length-collapse hack).

### 4.3 Where the learning lands

Every confirmed win becomes a **material recipe** in mac-design-studio's references, the same day (the improve-skill iteration rule). The recipe table the research validated, seeded with what our manual loops already found:

| Raster look | SVG construction |
|-------------|------------------|
| Soft cast shadow | Duplicated silhouette, dark fill, Gaussian blur, clipped, opacity falloff (never one offset dark path) |
| Translucent gel/glass | Radial+linear gradient stack, low-opacity white highlight, interior shadow, clipped reflection |
| Embossed edge | Base gradient + inner-shadow approximation + rim highlight + local low-radius blur |
| Metallic accent | Multi-stop non-monotonic gradient, narrow specular paths, masked reflections |
| Ambient occlusion | Local dark transparent shapes under overlaps, respecting occlusion order (never a global blur) |
| Curl/ribbon volume | Lit ribbon construction: face/back gradients differ, edge highlight, contact shadow (the improve-skill shaving) |

Deliverable: a `material-recipes.md` reference in mac-design-studio, plus a SKILL.md rule that Engine A must pass the fidelity harness against the winning raster before the audit sheet is final.

---

## 5. Phase 3: fixture corpus (the private benchmark)

Two strong pairs debug the harness; they cannot calibrate metrics or support any model claim. Expand to a private **Material Icon Fidelity** set:

- **Source**: every future icon run contributes its A/C pair automatically (the pipeline already produces both); plus a deliberate sweep using media-gen-pro with the corpus referenceImages to cover material families: opaque plastic, translucent glass, metal, soft-shadow matte, embossed face, flat control (the null case).
- **Target**: 20-30 pairs near-term (enough for metric calibration and loop regression tests), grown opportunistically.
- **Hold-outs**: at least one material family and several object categories never used during loop tuning, reserved for final claims.

---

## 6. Phase 4: distillation toward a better-than-Arrow vector model

Longest horizon, cheapest to start: **the loop's byproduct is the dataset.** Every Phase 2 run must record full trajectories from day one, in the research-validated record shape (see the GPT-5.6 report's JSON schema): reference raster + prompt + every candidate SVG + render + metric vector + critic diagnosis + accept/reject, plus renderer metadata and rights fields.

The evidence-backed sequence when the corpus justifies it:

1. **Corpus SFT** on licensed SVGs + accepted trajectories (StarVector/OmniSVG scale reference: ~2M samples for broad SVG modelling; Grok's minimal-viable estimate for a domain model: 100k-500k pairs; Gemini's threshold for beating Arrow-class: 500k+ curated triplets). Format the teacher traces as **"Drawing-with-Thought"**: the reasoning prefix (layers, lighting direction, primitive relationships) is part of the training target, so the student learns geometric logic rather than syntax.
2. **Rejection sampling** against the full harness; keep near-misses as negatives. This doubles as **RSO**: preference pairs sampled from the harness-passing policy, not just the base policy, which is what keeps the later DPO step in distribution.
3. **Correction SFT**: (reference, current render, residual, critique) to corrected SVG (IntroSVG's construction).
4. **Preference optimisation** (DPO on the RSO-sampled pairs) with winners decided by the Pareto gate + blind adjudication.
5. **Render-reward RL** (RLRF precedent: 64 rollouts/image, 500 steps, 16k images, 4×8×H100 for ~3 days; headless renderer in the reward loop, DISTS + CLIP + bounded code-efficiency terms).
6. **Frozen bake-off** before any claim: Arrow 1.1, Arrow 1.1 Max, Claude scaffold-only, Claude + loop, and the student, on the held-out set, identical prompts/renderer/budgets. Arrow has no public benchmark, so the claim can only be made on our private set, blinded.

**Gates before spending here:** (a) Phase 1-2 must show the loop reliably closes the material gap (otherwise there's nothing worth distilling); (b) legal review of QuiverAI/teacher terms for training on outputs (flagged MISSING_DATA in the research; both reports insist on counsel before distillation).

**Arrow-as-tool meanwhile:** keep Arrow 1.1 in the pipeline as Engine B and as a candidate generator (its image-to-SVG vectorisation endpoint takes a 128-4096px raster; worth testing C-raster → Arrow vectorise → loop-refine as an alternative scaffold source).

---

## 7. Failure-mode ledger (wired into the harness)

| Failure (evidence) | Mitigation (where) |
|--------------------|--------------------|
| Naïve screenshot feedback degrades output (RitL: 0.345→0.388) | Critic gets residual/edge maps + constrained edit classes (3.5, 4.2) |
| Oscillation/repetition (RitL) | Edit-signature hashing, per-round edit-class lock (4.2) |
| Plateau (RLRF reward ablation; VLM leniency plateau per Gemini) | Two-reject branch-or-stop rule, categorical 0-2 rubric scales (3.5, 4.2) |
| Context rot by iteration 8-10 (Gemini) | Hard cap 10, on-disk counters, fresh isolated editors per round (4.2) |
| viewBox shrink hack (RLRF) | Harness normalises canvas from reference (3.1) |
| Length-collapse hack (RLRF) | Complexity is a cap, never a reward (4.2) |
| base64 `<image>` mimicry and invisible-path contrast gaming (Gemini) | Static analysis before render (4.2) |
| LPIPS gamed by adversarial high-frequency noise (stAdv/PGD) | DISTS preferred at large sizes; MS-SSIM + edges at small; Pareto gate (3.3, 3.4) |
| Metric gaming via blur/texture | Multi-size Pareto gate + edge gates + VLM review (3.4) |
| Thin-stroke pixel-metric instability (RLRF SVG-Icons caveat) | Edge F1/IoU carry small sizes, not MSE/SSIM alone (3.3) |
| VLM judge positional bias | Anchor-referenced independent scoring (3.5) |
| Vendor-claim contamination | Arrow treated as unbenchmarked until our frozen bake-off (6) |

---

## 8. Sequencing and cost

1. **Now**: Phase 1 harness prototype against the two strong fixtures; calibration against the manual-loop history. Pure local compute (torch optional). No API spend.
2. **Next**: Phase 2 loop on the improve-skill and create-swe-project pairs; land material recipes + harness into mac-design-studio. Claude tokens only.
3. **Then**: Phase 3 corpus growth rides along with normal icon work; deliberate raster sweeps cost media-gen-pro credits per image.
4. **Later, gated**: Phase 4 distillation. Real cost (GPU training, RLRF-scale reference: multi-day multi-node) and a legal gate. Trajectory capture starts free at step 2 regardless.

Research spend on this track: GPT-5.6 ~$3.50 + Gemini ~$3.00 + Grok ~$1.20 (estimated, panel fast tier); local-claude, local-codex and perplexity members failed at $0.

---

## 9. Open decisions

- The harness's final home after prototype (mac-design-studio `scripts/` vs a shared tools package usable by both marketplaces).
- Whether to install torch locally for LPIPS/DISTS or run the degraded tier until Phase 2 proves the loop; the calibration run (3.6) will show whether the numpy tier's ranking already matches the human record.
- Arrow-as-scaffold experiment (C-raster → Arrow vectorise → loop-refine) vs pure hand-authored scaffolds: cheap to test once the harness exists, worth deciding on data.
- First calibration run results against the fixture history go here when they exist.
