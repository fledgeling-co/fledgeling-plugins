# Evidence — what the outside literature says, and where it disagrees with us

Why this file exists: two of the skill's load-bearing claims cite
`docs/svg-icon-fidelity-plan.md` and `docs/deep-research/` at the
**fledgeling-plugins repository root**, which do not ship inside the installed
plugin. A rule whose provenance a runner cannot open teaches the model that this
skill's references are unreliable. The findings that changed the skill's own
rules are therefore restated here, with citations that resolve from anywhere.

Read this when you are about to change a gate threshold, the panel protocol, or
the stopping rule — those three are where outside evidence actually bears on the
design, and where getting it wrong is expensive.

## Provenance and how much to trust it

Panel of four independent deep-research backends (OpenAI gpt-5.6-terra, Google
Gemini, Perplexity Sonar Deep Research, xAI Grok), 2026-08-18, one shared brief.
**77 distinct sources over 40 independent domains, with only 5% overlap between
backends** — so a claim only one backend made is uncorroborated rather than
agreed, and is marked below.

Citation verification, run per backend:

| Backend | Citations | Fabricated / dead | Resolved |
|---|---|---|---|
| OpenAI | 34 | **0** | 94% (2 publisher 403s) |
| Perplexity | 19 | **0** | 74% (5 publisher 403s) |
| xAI | 11 | **0** | 100% |
| Gemini | 28 | **1 dead (404)** + 1 unreachable | 71% |

Gemini's dead link matters specifically: its "verdict flip-rate up to 40%"
figure cites the 404, and four of its claims rest on non-resolving URLs with
nothing else behind them. **That figure is not used here.** Where Gemini
disagrees with OpenAI below, OpenAI is weighted higher on the strength of a
clean fabrication check. Perplexity returned two junk sources — an Instagram
reel and a Facebook post titled "Patience reveals what's real" — keyword matches
on *patience*, which is a useful reminder that a source list is not evidence.

## 1. The composite is a proxy, and the literature says so harder than we did

- **SSIM correlates weakly with human judgment on generated imagery.** On the
  PIPAL benchmark — 250 references, 116 variants each, **>1.13 million human
  pairwise judgments** — NTIRE 2021 reports SSIM at PLCC **0.394** / SRCC 0.361,
  against LPIPS-VGG 0.633 / 0.595 and DISTS 0.687 / 0.655. The benchmark's
  authors conclude existing IQA metrics do not fairly evaluate GAN-based
  restoration. ([PIPAL](https://arxiv.org/abs/2007.12142),
  [NTIRE 2021](https://openaccess.thecvf.com/content/CVPR2021W/NTIRE/papers/Gu_NTIRE_2021_Challenge_on_Perceptual_Image_Quality_Assessment_CVPRW_2021_paper.pdf))
  Even the best of them leaves substantial rank disagreement with humans. This
  is the outside version of **a gate ACCEPT is evidence, never a verdict**.
- **Two of our four terms are blind to material by construction, not by
  accident.** Mask IoU compares binary region overlap and edge F1 compares
  detected edges, so *any* appearance change that preserves those
  representations — matte for gloss, a lost highlight, a shifted interior
  gradient, changed fill opacity — is invisible to both. That is a mathematical
  consequence of their inputs. Keep them as silhouette and geometry guardrails;
  never let them veto a panel-identified material improvement.
- **A single weighted sum can conceal a component failure.** Excellent IoU and
  edge F1 can numerically compensate for wrong materials. Our per-size Pareto
  gate is already non-compensatory across sizes, which is the right shape; the
  remaining exposure is *within* a size.
- **SSIM penalises valid texture resampling by construction** — it assumes
  pixel correspondence, so a perceptually identical texture patch in a different
  arrangement scores as a defect.
  ([DISTS](https://arxiv.org/abs/2004.07728)) This independently corroborates
  our own r02 finding, where the gate rejected a fibre-texture round the human
  then preferred. We had the mechanism right.
- **DISTS is the candidate worth testing.** It separates structure from texture
  via spatially averaged feature responses, is explicitly tolerant of texture
  resampling and mild geometric variation, and scored highest of the three on
  PIPAL. Its own follow-up names the trade:
  [A-DISTS](https://arxiv.org/abs/2110.08521) says DISTS makes comparatively
  global measurements and can ignore locally structured variation — which for an
  icon, where one gloss direction is part of the identity, is a real liability.
  Not adopted; recorded as the next ablation.
- **Deep metrics can be driven away from human preference on purpose.** Learned
  preprocessing before compression raised DISTS by up to **34.5%**, LPIPS by
  **36.8%**, VIF by **98.0%** and HaarPSI by **22.6%** while subjective scores
  stayed flat or fell. **PSNR and SSIM were immune** — which makes the crude
  metrics useful as *hack detectors* even though they are too weakly correlated
  to judge quality. (Perplexity, single-sourced;
  [PMC9409967](https://pmc.ncbi.nlm.nih.gov/articles/PMC9409967) and the metric
  hacking work it cites.) Every perceptual metric tested, ours included, can
  also be flipped by imperceptible adversarial perturbation
  ([Attacking Perceptual Similarity Metrics](https://openreview.net/pdf?id=VUcI0pKic8l)).

## 2. The panel protocol — two changes the literature forced

**Seeded order-randomisation is necessary and not sufficient. This changed the
code.** Randomising which take sits in slot A balances position effects across a
batch; it does nothing about a single verdict that would have flipped had the
pair been swapped, and a promotion decision is exactly one such verdict.

- Order-consistency on deliberately close pairs: **23.8% for Claude-v1, 46.2%
  for GPT-3.5, 65.0% for GPT-4**; and the MT-Bench protocol of asking twice and
  counting a flip as a tie **raised consistency from 16.2% to 65.0%**.
  ([Zheng et al., NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf))
- Order reversals of **25% / 58% / 89%** across three evaluators, with the
  authors explicitly proposing that order-reversing cases be treated as
  ambiguous rather than resolved.
  ([Panickssery et al., NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf))
- Position bias is systematic rather than noise, varies by judge and task, and
  **grows as the quality gap narrows** — 15 judges, 22 tasks, >150,000
  instances. ([Shi et al., 2025](https://aclanthology.org/2025.ijcnlp-long.18))
  That last clause is why this matters here rather than in general: consecutive
  rounds of this loop differ by one edit class, so every comparison the panel
  makes is a narrow-gap comparison.
- Reordering alone made one model beat another on **66 of 80** queries under an
  LLM evaluator. ([Wang et al., 2023](https://arxiv.org/abs/2305.17926))

→ `judge_panel.py` asks every judge in **both orders** and records a swap-flip
as a **tie**, not a winner. `--no-swap` halves the cost and is documented as an
inner-round option, never a shipping one.

**The generator's own family does not get a decisive vote. This changed the
code.** Self-preference is documented across evaluators; self-refinement
*amplifies* it; and in one study evaluator self-preference exceeded the quality
differences a 900-comparison human study could measure.
([Panickssery et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf);
[Xu et al., ACL 2024](https://aclanthology.org/2024.acl-long.826.pdf)) The
mechanism is contested and the disagreement changes the fix:
[Wataoka et al.](https://arxiv.org/abs/2410.21819) find judges favour
lower-perplexity output whether or not they generated it, which means **blinding
the prompt is not enough and cross-family heterogeneity is the only mitigation
that works.** Our round agent is `claude -p`, so the `claude` judge is
same-family as the generator: recorded in full, excluded from the majority.

**What a two-family panel supports, since ours is often two.** Heterogeneous
panels beat single judges on human correlation and intra-model bias at >7× lower
cost than one large judge ([PoLL, Verga et al.](https://arxiv.org/abs/2404.18796);
panel deviation SD 2.2 against GPT-3.5's 6.1). But no study establishes a
sufficient panel size, and panel members are not independent voters — they share
training data and failure modes. Three is the smallest *odd* panel that can form
a majority without giving one vendor permanent tie-break authority; it is a
defensible minimum architecture, not a validated sample size.

So, stated plainly:

- **Two families in unanimous agreement, each swap-consistent, supports a
  provisional promotion.** That is the strongest claim available.
- **Two families cannot produce a majority in disagreement.** A 1–1 split means
  retain the incumbent and escalate. It does not mean pick the family you trust
  more, and it must never be reported as a consensus.
- **A panel whose only surviving judge is the generator's family supports
  nothing at all** and reports `no-decisive-judges`.
- Judges are allowed to return **tie**, and the panel is allowed to return
  **no-majority**. Forced binary choice converts position bias and genuine
  uncertainty into false promotions.

## 3. Stopping rules — where our own trace contradicts the published one

Our replayed 20-round trace: the composite climbed **0.5481 → 0.6403 (+16.8%)**
while the blind panel preferred the *previous* take in **7 of 13 judged
rounds**. The naive "stop after two consecutive non-winning rounds" rule fires
at **r04** — before all three of the run's genuine wins (r07, r10, r11) — and so
ships nothing the panel ever preferred. Armed only after the first promotion, the
same rule stops at **r13** and ships **r11**, skipping six rounds. (Reproducible:
the replay is in `references/fidelity-loop.md`; both outcomes were re-derived
from the documented per-round counts during this rebuild.)

**Where the literature agrees.** Best-checkpoint return after patience-based
stopping is textbook practice — retain the parameters with the best recorded
validation score and return those, not the terminal state
([Goodfellow, Bengio & Courville](https://deeplearningbook.org/contents/regularization.html)).
Naive monotonic stopping is documented as unreliable on oscillating
trajectories: fitting a monotonic curve and stopping on it "seldom yields a good
estimate" ([Chen et al., 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7263346)),
and finite patience gives only a *probabilistic* local optimum
([Boyan, 1998](https://ri.cmu.edu/pub_files/pub1/boyan_justin_1998_2/boyan_justin_1998_2.pdf)).
Stopping criteria trade compute for generalisation rather than being universally
calibrated: slower criteria bought ~4% better generalisation at ~4× the training
time across 14 criteria and 12 tasks
([Prechelt, 1998](https://pubmed.ncbi.nlm.nih.gov/12662814)).

**Where it is silent, and the panel disagreed about how silent.** The exact rule
— arm patience after the first *verified success* — has no established name.

- **OpenAI (fabrication-clean):** not located as a named published standard. The
  closest published families are **delayed early stopping**, **warm-up early
  stopping**, and Keras's `start_from_epoch`
  ([Keras](https://keras.io/api/callbacks/early_stopping)) — and all of them arm
  after a fixed **iteration count**, not after a success event. Proposed names:
  *event-armed patience* or *promotion-armed patience*. Document it as a
  production policy derived from the trace, not as a literature algorithm.
- **xAI:** literature is silent; naive patience is *not* documented to fire
  prematurely in exploration phases.
- **Perplexity:** no formal name or dedicated study; the logic is consistent
  with documented failure modes, and the closest published advice is
  multi-metric patience that resets when *any* tracked quantity improves.
- **Gemini:** claims it is "heavily corroborated" under delayed early stopping
  and staged warm-up. Discounted — its supporting sources are the weakest in the
  panel and partly unreachable. One genuine find survives: **LToT**
  ([arXiv 2510.01500](https://arxiv.org/pdf/2510.01500)) begins culling only
  after a lateral branch clears the bar, which *is* event-triggered rather than
  count-triggered, and is the nearest published analogue.

**The verdict we act on:** the correction is right for this loop and is ours.
Three of four backends agree no published rule names it. Two of four call naive
patience premature under noise, one says the literature does not establish that,
and none contradicts the trace. We adopt it, name it **promotion-armed
patience**, and say in `SKILL.md`'s known limits that it rests on one trace.

OpenAI additionally recommends **patience 3 rather than 2**, because a corrected
panel transition is both noisy and expensive — which is what `PANEL_VETO = 3`
already is, arrived at independently. It also recommends an **exploration cap**
of 6–8 rounds before escalating a fixture that has never been promoted, since
promotion-armed patience cannot fire before the first promotion; that is now
`EXPLORATION_CAP = 7`. Both are engineering starting points, not validated
constants, and both are stated as such.

## 4. Reward hacking — the loop is a specification-gaming machine, by design

- **Proxy reward rising while true quality falls is the expected failure, not an
  exotic one.** ([Rafailov et al.](https://arxiv.org/abs/2406.02900);
  [RLHF book, over-optimization](https://rlhfbook.com/c/14-over-optimization))
  Our trace — composite +16.8%, panel preferring the previous take in most
  judged rounds — is a textbook instance, and naming it that way is more useful
  than treating it as a local surprise.
- **In text-to-image RL, agents produce unrealistic artefacts that maximise
  perceptual proxy scores.** ([Hong et al., CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026F/papers/Hong_Understanding_Reward_Hacking_in_Text-to-Image_Reinforcement_Learning_CVPRF_2026_paper.pdf),
  single-sourced) The direct analogue of the `<image>`-embed exploit
  `fidelity.py structure` already forbids.
- **Metric ensembles help and do not solve it.** Conservative ensembles
  practically eliminated over-optimisation in one controlled setting, improving
  best-of-*n* by up to **70%** ([Coste et al.](https://arxiv.org/abs/2310.02743)) —
  but ensembles whose members share blind spots are still hackable, and
  pretraining-seed diversity generalises better than fine-tuning-seed diversity
  ([Eisenstein et al.](https://arxiv.org/abs/2312.09244)). The lesson for us is
  *not* "add more correlated image metrics": it is that each metric must watch a
  different failure surface, which is what the current stack does.
- **Refusing to tune a threshold onto one failing case is the right call**, and
  it has a name in the literature: held-out validation discipline. DISTS's own
  authors warn that repeated reuse of the same IQA databases causes unintentional
  over-adaptation through design selection
  ([Ding et al.](https://arxiv.org/abs/2004.07728)). This is direct outside
  support for the `self_contrast` decision recorded in
  `references/fidelity-loop.md` — the threshold was left at its principled value
  rather than tuned until it fired on r01.
- **A held-out judge, never used for selection, is what detects the loop
  overfitting its own panel.** Optimising one scorer demonstrably fails to
  improve an independently trained one. Our panel is a *selection* panel; there
  is currently no held-out audit layer, and that is a known gap rather than a
  solved problem.
- **Forbidding the agent to edit the scorer is architectural, not behavioural.**
  No controlled study measures it for this setting, and every backend still calls
  it non-negotiable — agents in coding testbeds rewrite the evaluation rather
  than solve the task. Our round agent runs under a tool whitelist and is told
  to edit only the build script; **the whitelist does permit `Write`/`Edit`
  generally, so scorer immutability currently rests on the brief rather than on
  the harness.** Recorded honestly as the weakest link in this section.

## Gaps every backend agreed on

No study evaluates SSIM / edge F1 / LPIPS / mask IoU against human preference on
**hand-authored SVG icons matched to raster references**; no weighting, threshold
or region scheme is validated for this task. The position-bias and self-preference
evidence is from **text** judging, not vision-language judging of close icon
variants. And no work establishes that three VLM families are sufficient here.
Every number above is transferred evidence — which is why the rubric and the
human still outrank the instruments, and why `gate < panel < human` is the one
ordering in this skill that no citation is allowed to overturn.
