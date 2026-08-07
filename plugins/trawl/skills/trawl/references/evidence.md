# Evidence — the research grounding for this skill's mechanisms

Every structural choice in SKILL.md traces to a measured result or a
documented failure mode. This file is the map from mechanism to evidence.
Read it when tuning the skill, defending a design choice, or deciding
whether a proposed change would help. Findings below were gathered via a
five-backend deep-research panel (Gemini Deep Research, GPT-5.6,
Perplexity Sonar, Grok, Claude) in August 2026; citations were
dereferenced and none were fabricated.

## Contents

1. [The homogenization problem is measured, not vibes](#1-homogenization)
2. [What measurably increases diversity (ranked)](#2-what-works)
3. [What measurably fails or backfires](#3-what-fails)
4. [Frames and personas: ordinary beats exotic](#4-frames)
5. [Why gates and pairwise comparison replaced 1–10 scores](#5-scoring)
6. [Why the baseline boss gate exists](#6-boss-gate)
7. [Architecture: islands, quality-diversity, and where debate fits](#7-architecture)
8. [Open questions and contested findings](#8-contested)

## 1. The homogenization problem is measured, not vibes {#1-homogenization}

- **Within-model saturation:** over-generating 4,000 research ideas from
  one aligned model left ~5% unique after semantic dedup at cosine 0.8;
  uniqueness decays toward a plateau — "just sample more" hits a wall
  (Si, Yang & Hashimoto, ICLR 2025, arxiv.org/abs/2409.04109).
- **Cross-user homogenization:** ChatGPT-assisted users produced ideas
  measurably more similar *to each other* (d=0.47) than users of a
  non-LLM tool (Anderson et al., ACM C&C 2024, arxiv.org/abs/2402.01536);
  a Nature Human Behaviour reanalysis found 94% concept overlap — nine
  independent users produced the identical product name
  (nature.com/articles/s41562-025-02173-x).
- **Cross-model:** LLM outputs are more similar to other LLMs' outputs
  than humans' are to each other — swapping models does not restore
  diversity (arxiv.org/abs/2501.19361).
- **Root cause:** typicality bias in human preference data; RLHF/DPO
  sharpen the distribution around familiar outputs. Alignment reduced a
  "Creativity Index" ~30% (arxiv.org/abs/2410.04265); the mechanism
  persists even under a perfect reward model (arxiv.org/abs/2510.01171).
- **Trajectory:** newer/larger aligned models are not more diverse —
  NoveltyBench found all 20 frontier models less diverse than human
  writers, with larger models often *less* diverse than smaller siblings
  (arxiv.org/abs/2504.05228). Diversity engineering lives in the harness,
  not the model pick. This is why this skill exists.

## 2. What measurably increases diversity (ranked) {#2-what-works}

1. **Generate-then-differentiate.** The best of 35 strategies in the
   Wharton benchmark: batch-generate, then "modify the ideas to make them
   bolder and more different; no two the same". Pooled cosine similarity
   0.377 → 0.255, near the human-group benchmark of 0.243
   (arxiv.org/abs/2402.01727). This is the second pass inside every
   branch prompt.
2. **Verbalized Sampling** — ask for a distribution of k responses with
   probabilities, select from the tail: 1.6–2.1× diversity on aligned
   models (arxiv.org/abs/2510.01171). Contested at the margin: at least
   one follow-up found it roughly equal to plain batch generation, which
   is why this skill uses batch generation as the base and treats VS as
   optional seasoning rather than load-bearing.
3. **Heterogeneous parallel personas in separate contexts.** Parallel ≈
   sequential, both beat all-personas-in-one-prompt (Feng, Hélie &
   Panchal, Design Science 2025). Persona *breadth* beats depth —
   one-sentence occupational personas capture most of the gain
   (arxiv.org/html/2607.20429v1).
4. **Population structure** (islands/archives) for sustained search —
   see §7.
5. **Semantic dedup** at embedding cosine ~0.8 (a convention set by
   manual inspection, not a validated constant). In a markdown skill with
   no embedding pipeline, mechanism-level dedup by the critic is the
   equivalent move.

## 3. What measurably fails or backfires {#3-what-fails}

From the same 35-strategy benchmark (arxiv.org/abs/2402.01727) and
related work — these are the intuitively-good ideas the skill must not
reintroduce:

- **Showing the model the similarity of existing ideas:** worst strategy
  tested (0.432 vs 0.377 baseline).
- **Seeding with previous top ideas:** 0.403 — worse than doing nothing.
- **Pasting brainstorming best-practice articles into the prompt:**
  worse than baseline.
- **Temperature:** weak correlation with novelty, moderate with
  incoherence (arxiv.org/abs/2405.00492). Not a creativity dial.
- **Generic "be diverse" instructions, tips, threats, emotional
  appeals:** approximately no effect.
- **Mid-flight sharing between agents:** dense interaction and shared
  intermediate context cause diversity collapse and premature consensus;
  blind writing and subgroup isolation preserved diversity
  (ACL Findings 2026, aclanthology.org/2026.findings-acl.13.pdf).

These four lines are why the isolation invariant is absolute during
divergence, and why the skill never feeds one branch's output to another.

## 4. Frames and personas: ordinary beats exotic {#4-frames}

- Ordinary occupational personas ("municipal procurement officer",
  "night-shift support lead") partition knowledge better than
  celebrity/"creative genius" personas (arxiv.org/abs/2602.20408; the
  Wharton benchmark found Steve Jobs personas no better than generic
  creative ones).
- Personas are a **diversity** lever, not a quality lever — 162 personas
  across 4 model families gave no accuracy benefit on factual tasks
  (arxiv.org/abs/2311.10054). Expect frames to widen the pool, not to
  make individual ideas smarter.
- Cross-domain analogy frames earn their place only when they transplant
  a *mechanism*; decorative metaphors add wording variety, not idea
  variety. Hence the "name the mechanism, state where the analogy
  breaks" requirement.
- The predecessor skill's field observation — a child persona attached to
  deeply technical output — is the visible symptom of tag-based frame
  selection with no fit check. The fit floor + apoptosis pair fixes it
  from both ends: don't spawn catastrophic mismatches, and never render
  a frame whose entire yield failed the floors.

## 5. Why gates and pairwise comparison replaced 1–10 scores {#5-scoring}

- **Central-tendency collapse:** direct rubric scores from LLM judges
  cluster in the middle (arxiv.org/abs/2405.01724); the Stanford ideation
  study abandoned direct scoring as uncalibrated and used a pairwise
  Swiss tournament (71.4% accuracy predicting acceptance)
  (arxiv.org/abs/2409.04109).
- **Novelty scores are near-noise:** against ~25k expert novelty ratings,
  every automated proxy — embedding distance, perplexity, LLM-as-judge —
  sat near chance; best retrieval-augmented judge r≈0.35
  (arxiv.org/pdf/2604.15145).
- **Judges don't model the novelty–feasibility tension:** human raters
  show r=−0.42 between the two; LLM judges ~0 (arxiv.org/pdf/2601.08901).
  A judge scoring both on one card isn't modeling the trade-off that
  makes the numbers informative — hence separate pass/fail floors.
- **Known judge biases** (CALM taxonomy, arxiv.org/abs/2410.02736;
  MT-Bench, arxiv.org/abs/2306.05685): position bias (GPT-4 only 65%
  order-consistent — always swap A/B), verbosity bias, self-enhancement,
  authority/citation bias, bandwagon. Defenses in convergence.md.
- **Panels beat single judges:** three small heterogeneous judges beat
  one GPT-4 judge at ~1/7 cost (PoLL, arxiv.org/abs/2404.18796) —
  relevant to the companion CLI; inside a markdown skill, order-swapped
  pairwise + blinding is the practical subset.

## 6. Why the baseline boss gate exists {#6-boss-gate}

- **The ideation–execution gap:** when 43 experts actually executed AI
  vs human ideas (>100h each), the AI ideas' pre-execution novelty
  advantage reversed — ratings dropped −1.98 vs −0.63 and rankings
  flipped (arxiv.org/abs/2506.20803). Feasibility is the dimension where
  LLM ideas systematically disappoint.
- **Judged novelty anti-correlates with real impact:** ideas LLM judges
  rated more novel were *less* likely to correspond to real, cited
  future research (ρ=−0.29, HindSight, arxiv.org/html/2603.15164v2).
- **The predecessor's one benchmark loss** (llm-hang-cli) was exactly
  this shape: a creative pick that didn't solve the core reliability
  problem, losing to a boring shippable baseline on builder_usefulness.
- The gate therefore judges *only* the stated ask, blind and
  order-swapped, with novelty excluded — and an honest "the baseline
  wins, here's the exploration anyway" is a first-class outcome.
- **Phrase-level bans are unmeasured:** no study isolates "ban the first
  N obvious answers"; the differentiation step is measured and works.
  Freezing the actual baseline text converts the ban from a phrase
  filter into a testable mechanism-difference requirement.

## 7. Architecture: islands, quality-diversity, and where debate fits {#7-architecture}

- **Strongest anti-convergence evidence is population structure:**
  FunSearch's island model (independent islands, periodic worst-half
  reset) produced publishable mathematics (Nature,
  nature.com/articles/s41586-023-06924-6); QDAIF's MAP-Elites archive
  beat non-QD baselines across three creative domains (ICLR 2024,
  arxiv.org/abs/2310.13032); AlphaEvolve generalized it
  (arxiv.org/abs/2506.13131). The skill's frames-as-islands +
  one-elite-per-cluster shortlist is the lightweight, single-pass
  adaptation of quality-diversity selection: protect the best of each
  *kind*, not the top of one global ranking.
- **Global weighted top-N is the wrong objective** for divergence — it
  can select three near-duplicate safe ideas. Max-min / one-per-cluster
  selection targets "several high-quality, materially different ideas".
- **Debate is a repair tool, not a divergence tool.** Debate ≤
  self-consistency at matched cost on convergent tasks
  (arxiv.org/abs/2311.17371); model heterogeneity is the one lever that
  reliably helps (arxiv.org/abs/2502.08788); role-play *discussion*
  scored higher AUT originality than adversarial debate
  (arxiv.org/abs/2405.06373). Placement: after clustering, as bounded
  adversarial repair of shortlist winners — never during divergence.
- **ToT/GoT are search-control for verifiable problems** (Game of 24,
  sorting), with no ideation evidence; their transferable idea is
  aggregation, which the 100%-tier hybridization pass borrows.

## 8. Open questions and contested findings {#8-contested}

Hold these loosely; update the skill when they resolve:

- **VS vs plain batch generation** — marginal gain contested; ICML 2026
  camera-ready may settle it.
- **Min-p sampling** — ICLR oral claims vs a direct statistical rebuttal
  (arxiv.org/abs/2506.13681); unresolved, and inapplicable inside a
  markdown skill anyway.
- **Cluster-then-select vs threshold-dedup-then-tournament** — no
  controlled comparison exists for idea selection specifically; this
  skill uses clustering because the cluster labels double as output
  structure the reader needs.
- **Semantic-distance thresholds** (0.7–0.99 across papers) are
  domain-dependent conventions; mechanism-level judgment by the critic
  sidesteps the constant.
- **"Ban the first N obvious answers"** as an isolated variable remains
  unmeasured — which is why this skill grounds the ban in the frozen
  baseline rather than trusting the phrase.
