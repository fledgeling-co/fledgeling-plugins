---
title: "Implementing quality-diversity selection and semantic clustering for LLM ideation"
run_id: dr_d6ac726ae3c63ef2
question: "What are the most effective, evidence-backed techniques for maximizing idea diversity and quality in LLM-based divergent ideation and multi-agent brainstorming systems, and what known failure modes should such systems defend against? Cover: (1) measured homogenization/mode-collapse of LLM idea generation and mitigations (persona/frame diversity, sampling strategies, semantic de-duplication, novelty search); (2) structured multi-agent ideation architectures (tree-of-thought, graph-of-thought, debate, evolutionary/quality-diversity approaches like MAP-Elites and FunSearch, island models); (3) scoring and convergence: how to score novelty/feasibility reliably with LLM judges, known judge biases, cluster-then-select methods; (4) creativity evaluation benchmarks and metrics for LLMs (e.g., Torrance-style tests, semantic diversity metrics, human-comparison studies); (5) practical prompt-level findings from 2024-2026 research and practitioner writing on making LLM brainstorming less generic."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: technical
sources: 37
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-07T05:59:35.191Z
---
## Executive Summary

- **(High Confidence)** Keep the skill’s core invariant—**blind, isolated divergence before convergence**—but change the convergence objective from “top three global weighted scores” to **quality-diversity selection**: retain the best viable idea in each distinct mechanism/approach niche, then choose a mutually dissimilar shortlist. The current `adhd` implementation already isolates five branches, but its global `novelty × viability × fit` ranking can still select three near-duplicate safe ideas. [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) ([github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md))

- **(High Confidence)** Replace “ban the first three obvious answers” as the primary novelty mechanism with a **measured anti-anchor pipeline**: explicitly generate the obvious baseline, create semantic signatures for every candidate, reject/repair near-neighbours, cluster by causal mechanism rather than wording, and use max-min or MAP-Elites-style selection across clusters. Prompt-only novelty bans are insufficient because LLMs show fixation and collective knowledge concentration. [arxiv.org](https://arxiv.org/abs/2602.20408) [frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full) ([arxiv.org](https://arxiv.org/abs/2602.20408?utm_source=openai))

- **(High Confidence)** Do **not** let agents debate during the initial divergent pass. Dense interaction and shared intermediate context can create diversity collapse and premature consensus; blind writing and subgroup isolation produced higher diversity in a 2026 open-ended ideation study. Use debate only after clustering, as a bounded **adversarial feasibility-repair** stage. [aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf) ([aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf))

- **(Medium Confidence)** Upgrade frames from a fixed, mostly metaphorical list to a deliberately balanced portfolio: ordinary stakeholder/constraint personas, causal-mechanism analogies, adversarial inversion, and extreme operating constraints. Evidence supports ordinary personas and chain-of-thought-style decomposition for diversity; evidence also indicates that multiple professional personas work better when prompted independently or sequentially than when blended into one collective persona. [arxiv.org](https://arxiv.org/abs/2602.20408) [cambridge.org](https://www.cambridge.org/core/journals/design-science/article/enhancing-design-concept-diversity-multipersona-prompting-strategies-for-large-language-models/3B346E253508337A4EE899499BE49D9B) ([arxiv.org](https://arxiv.org/abs/2602.20408?utm_source=openai))

- **(High Confidence)** Treat LLM judging as a **triage signal, not ground truth**. LLM judges exhibit position, verbosity, self-preference, authority, and other biases. Use a rubric with independently scored dimensions; blind and order-swap pairwise comparisons; at least two judge families; calibration against a small human-labelled set; and mandatory human escalation for high-impact or low-agreement selections. [arxiv.org](https://arxiv.org/abs/2406.07791) [arxiv.org](https://arxiv.org/abs/2410.02736) [arxiv.org](https://arxiv.org/abs/2410.21819) ([arxiv.org](https://arxiv.org/abs/2406.07791))

- **(Medium Confidence)** The strongest current evidence does not support a universal claim that LLMs are either “creative” or “generic.” In one large blind NLP-research study, AI ideas were rated more novel than expert ideas but not more feasible; other creativity studies find models weak on originality or rarely in the top human-creative tail. The correct engineering target is therefore a **Pareto frontier of distinct, feasible ideas**, not raw novelty. [arxiv.org](https://arxiv.org/abs/2409.04109) [arxiv.org](https://arxiv.org/abs/2401.12491) [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S2713374525000202) ([arxiv.org](https://arxiv.org/abs/2409.04109))

- **(High Confidence)** For `adhd`, the highest-leverage implementation change is a three-stage architecture: **(1) isolated generation islands, (2) deterministic semantic archive + quality-gated diversity selection, (3) adversarial repair/deepening of one winner per cluster**. This preserves the skill’s low-dependency design while directly addressing homogenization, judge bias, and consensus collapse. <INFERENCE from="Deng et al. 2026; Liang et al. 2026; IDEAgent 2026; current ADHD SKILL.md">The recommendation combines the demonstrated risks of fixation and topology-induced collapse with quality-diversity search and the present skill’s isolated-worker architecture.</INFERENCE> [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) [arxiv.org](https://arxiv.org/abs/2602.20408) [arxiv.org](https://arxiv.org/abs/2607.22375) ([github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md))

## Detailed Findings

### What are the most effective, evidence-backed techniques for maximizing idea diversity and quality in LLM-based divergent ideation and multi-agent brainstorming systems, and what known failure modes should such systems defend against?

#### Decisive recommendation for `adhd`

**(High Confidence)** Replace the present “five frames → one critic → globally rank top three” loop with **Blind QD Islands**:

1. **Anchor map:** Generate the three obvious/default approaches once, retain them only as a negative reference set.
2. **Five isolated generation islands:** Each island receives a different frame card, a different sampling seed/configuration where available, and no other island output.
3. **Semantic archive:** Convert every idea into a structured semantic signature plus embedding; de-duplicate and cluster before any quality ranking.
4. **Quality gate:** Independently score non-obviousness, soundness, feasibility, fit, reversibility, and operational risk.
5. **QD shortlist:** Select one best surviving candidate per niche/cluster, then use max-min diversity selection rather than raw global weighted rank.
6. **Adversarial repair:** Give each selected cluster winner to a different critic frame that attacks assumptions and proposes repair.
7. **Deepen only repaired survivors:** Deepen at most one candidate per cluster unless the user explicitly asks for variants.

<INFERENCE from="ADHD SKILL.md global weighted top-three selection; MAP-Elites/QD archive principles; IDEAgent semantic signatures and diversity thresholding; 2026 diversity-collapse topology evidence">This changes the selection pressure from “find the highest average score” to “find several high-quality ideas that are materially different,” which is the appropriate objective for divergent ideation.</INFERENCE> [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) [frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full) [arxiv.org](https://arxiv.org/abs/2607.22375) [aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf) ([github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md))

#### 1. Measured homogenization/mode collapse and mitigations

**(High Confidence)** Homogenization is measurable, not merely anecdotal. A 36-participant comparative study found that people using ChatGPT produced ideas that were less semantically distinct across users than users of an alternative creativity-support tool, even though ChatGPT users produced more detailed ideas. [arxiv.org](https://arxiv.org/abs/2402.01536) ([arxiv.org](https://arxiv.org/abs/2402.01536?utm_source=openai))

**(Medium Confidence)** In GPT-4 product ideation, several plausible prompts generated less diverse idea pools than groups of humans. In that study, chain-of-thought prompting achieved the highest diversity among tested prompt variants and approached human-group diversity. [arxiv.org](https://arxiv.org/abs/2402.01727) ([arxiv.org](https://arxiv.org/abs/2402.01727?utm_source=openai))

**(Medium Confidence)** A 2026 working paper identifies two mechanisms: **within-run fixation**, where early outputs constrain later ones, and **collective knowledge concentration**, where independent LLM samples draw from a more unified semantic distribution than independent humans. It found that structured reasoning mitigated fixation and that ordinary personas, rather than celebrity “creative genius” personas, improved knowledge partitioning; combining them achieved the highest diversity in the paper’s experiments. This is highly relevant but remains a working paper rather than peer-reviewed archival evidence. [arxiv.org](https://arxiv.org/abs/2602.20408) ([arxiv.org](https://arxiv.org/abs/2602.20408?utm_source=openai))

**Recommended architecture change: replace the static novelty ban with an explicit anti-anchor reference set.**

```text
obvious = generate_default_baselines(problem, n=3)

for island in islands:
    candidates += isolated_generate(
        problem,
        frame=island.frame,
        forbidden_mechanisms=semantic_signature(obvious),
        output_schema=IdeaSignature
    )

archive = semantic_dedupe(candidates, threshold=tau_duplicate)
clusters = cluster_by_mechanism(archive)
```

<INFERENCE from="Deng et al. fixation findings; current ADHD first-three ban; IDEAgent explicit comparison against completed, ancestral, and rejected ideas">The first three answers should be stored and compared against, not merely prohibited linguistically. A model can evade a phrase-level ban while proposing the same causal mechanism with new wording.</INFERENCE> [arxiv.org](https://arxiv.org/abs/2602.20408) [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) [arxiv.org](https://arxiv.org/abs/2607.22375) ([arxiv.org](https://arxiv.org/abs/2602.20408?utm_source=openai))

**(High Confidence)** Semantic de-duplication must operate on mechanisms, not lexical overlap. IDEAgent decomposes each research idea along eight dimensions—failure mode, causal diagnosis, intervention, signal source, intervention locus, objective, evaluation regime, and assumption class—then evaluates pairwise distinctness before forming a maximum mutually diverse set above a threshold. [arxiv.org](https://arxiv.org/abs/2607.22375) ([arxiv.org](https://arxiv.org/abs/2607.22375))

**Concrete `adhd` schema change:**

| Field | Current `adhd` output | Proposed required field | Why it matters |
|---|---|---|---|
| Core idea | `text` | `proposal` | Keeps human-readable output. |
| Rationale | `rationale` | `causal_diagnosis` | Separates symptom from cause. |
| — | — | `mechanism` | Enables mechanism-level clustering. |
| — | — | `intervention_locus` | Distinguishes client, API, storage, UX, policy, workflow, and organization changes. |
| — | — | `assumption_removed` | Makes inversion and wild frames auditable. |
| — | — | `descriptor_tags` | Supports MAP-Elites-like archive cells. |
| — | — | `evidence_needed` | Prevents “novel but untestable” ideas from dominating. |
| — | — | `nearest_existing_idea_ids` | Makes similarity decisions inspectable. |

<INFERENCE from="IDEAgent eight-axis semantic signature; current ADHD JSON schema">These fields allow semantic de-duplication without requiring a heavyweight graph database or a trained novelty model.</INFERENCE> [arxiv.org](https://arxiv.org/abs/2607.22375) [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) ([arxiv.org](https://arxiv.org/abs/2607.22375))

**(Medium Confidence)** Higher-temperature sampling can broaden local variation but should not be treated as a sufficient anti-collapse control. A 2026 study reports that diversity collapse can persist under high-temperature sampling when structural formatting constrains the output space. [arxiv.org](https://arxiv.org/abs/2505.18949) <INSUFFICIENT_EVIDENCE>[The available source was an index summary rather than the primary paper text; use this only as directional evidence until the paper is independently reviewed.]</INSUFFICIENT_EVIDENCE>

**Recommended sampling policy.** <INFERENCE from="prompt-diversity studies; QD literature">Use deliberately heterogeneous sampling per island—e.g., some low-variance constraint-driven islands and some high-variance analogy/inversion islands—but make semantic distance, not temperature, the acceptance criterion.</INFERENCE> [arxiv.org](https://arxiv.org/abs/2402.01727) [frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full) ([arxiv.org](https://arxiv.org/abs/2402.01727))

#### 2. Structured multi-agent ideation architectures

| Architecture | Evidence-backed strength | Main failure mode | Recommendation for `adhd` |
|---|---|---|---|
| Independent parallel branches | Preserves independent exploration; `adhd` already implements this. [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) | Same-model semantic convergence despite isolated contexts. | Retain, but use frame portfolio and semantic archive. |
| Tree-of-Thought | Explores multiple intermediate paths and supports backtracking; achieved 74% versus 4% for GPT-4 CoT on Game of 24 in its task-specific evaluation. [arxiv.org](https://arxiv.org/abs/2305.10601) | Search-tree pruning can preserve an early evaluator’s bias; evidence is primarily reasoning/planning, not ideation. | Use only for deepening a selected idea, not the first divergence pass. |
| Graph-of-Thought | Supports aggregation, refinement, feedback, and merging of thought nodes; reported sorting-quality gains over ToT in its benchmark. [arxiv.org](https://arxiv.org/abs/2308.09687) | More graph links can transmit anchors and create context bloat. | Use a sparse provenance graph after clustering, never a fully shared discussion graph. |
| Debate / critic-revision | Can improve feasibility and surface incorrect premises; critic-side diversity improved feasibility in one scientific-ideation study. [arxiv.org](https://arxiv.org/abs/2507.08350) | Sycophancy, disagreement collapse, persuasion over truth. | Delay until after cluster selection; require each critic to attack a distinct failure mode. |
| Evolutionary search / FunSearch | Works strongly where an executable evaluator supplies objective fitness; FunSearch uses an LLM generator plus automated evaluation and evolutionary selection. [deepmind.google](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/) | Not directly transferable when “quality” is subjective and unverified. | Use for coding/API ideas only when tests, benchmarks, simulations, or static analysis exist. |
| MAP-Elites / QD archive | Explicitly maintains many high-performing yet behaviorally different solutions. [frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full) | Bad descriptor design creates meaningless niches. | Use 2–3 simple descriptor axes first; expose them in the result. |
| Island model | Independent populations preserve exploration before occasional migration. | Excessive migration recreates consensus collapse. | Implement “no migration before archive”; permit only structured, one-way cross-pollination after selection. |

**(High Confidence)** Tree-of-Thought and Graph-of-Thought are best interpreted as **search-control methods**, not validated generic brainstorming architectures. Tree-of-Thought’s strong published gains were on planning-style tasks; Graph-of-Thought’s reported cost and quality advantages were on tasks such as sorting. Neither directly establishes superiority for open-ended product or software ideation. [arxiv.org](https://arxiv.org/abs/2305.10601) [arxiv.org](https://arxiv.org/abs/2308.09687) ([arxiv.org](https://arxiv.org/abs/2305.10601?utm_source=openai))

**(High Confidence)** Quality-diversity methods are a better conceptual match for `adhd` than a pure “best idea” search. MAP-Elites retains elites across pre-defined behavioral niches, while novelty search rewards distance from archived behaviours; the relevant engineering adaptation is to preserve high-quality ideas across distinct causal mechanisms and intervention loci. [frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full) ([frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full?utm_source=openai))

**(Medium Confidence)** FunSearch and AlphaEvolve show the strongest case for LLM-guided evolutionary search when a machine-checkable evaluator exists. AlphaEvolve uses a breadth-oriented fast model, a depth-oriented powerful model, and automated verification/scoring; Google reports a deployed scheduler heuristic recovering an average 0.7% of worldwide compute resources. This is compelling evidence for **verifiable software optimization**, not for subjective design ideation. [deepmind.google](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) ([deepmind.google](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/))

**(Medium Confidence)** A July 2026 preprint, IDEAgent, reported a 3.89× advantage on its quality-diversity “Yield” metric across 32 computer-science topics and non-zero Yield on eight times as many topics as its best baseline. Its main reusable design is not its exact score but its principle: repair/refinement for quality plus explicit historical comparison for diversity. [arxiv.org](https://arxiv.org/abs/2607.22375) ([arxiv.org](https://arxiv.org/abs/2607.22375))

**Recommended `adhd` topology.**

```text
                  ┌─────────────── Anchor map ───────────────┐
                  │ obvious defaults + existing decision logs │
                  └──────────────────────┬───────────────────┘
                                         │
          ┌──────────────── blind isolated islands ────────────────┐
          │ frame A │ frame B │ frame C │ frame D │ frame E         │
          └────┬────────┬────────┬────────┬────────┬────────────────┘
               └──────────── semantic archive / de-dupe ────────────┐
                                                                      │
                   descriptor grid + cluster quality gates            │
                                                                      │
             one elite per niche ──> adversarial repair ──> deepen    │
```

<INFERENCE from="2026 diversity-collapse study; MAP-Elites; current ADHD isolated-agent design">Use islands for divergence, an archive for convergence, and critics for repair. Do not use peer dialogue as the mechanism that creates diversity.</INFERENCE> [aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf) [frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full) [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) ([aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf))

#### 3. Scoring and convergence: reliable novelty/feasibility assessment

**(High Confidence)** The existing `adhd` score weights—novelty 0.35, viability 0.40, fit 0.25—are simple and legible, but a single global weighted score inherently rewards compromise solutions and can eliminate diverse high-upside candidates. [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) ([github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md))

**Recommended scoring model.**

| Dimension | Definition | Method | Gate or ranking use |
|---|---|---|---|
| Non-obviousness | Is the problem–mechanism–intervention combination surprising to an informed practitioner? | Blind judge with explicit comparison to anchor map and semantic archive. | Ranking. |
| Soundness | Does the causal mechanism plausibly produce the claimed effect? | Critic must identify causal chain and counterexample. | Hard gate. |
| Feasibility | Can a small team validate/build the first version with stated constraints? | Separate operational judge; must name resources, dependencies, and first test. | Hard gate. |
| Fit | Does it resolve the actual user constraint rather than a generic adjacent problem? | Requirement traceability. | Hard gate. |
| Distinctness | Is it different in causal mechanism, intervention locus, and assumptions from survivors? | Embedding plus structured signature comparison. | Hard gate for final set. |
| Reversibility | Can the team test or roll back the idea cheaply? | Deterministic rubric. | Ranking tie-breaker. |
| Trap risk | Hidden costs, incentive misalignment, untestability, scale failure, or safety issue. | Red-team critic. | Exclusion or repair route. |

<INFERENCE from="IDEAgent dimension separation; FunSearch automated evaluator design; judge-bias studies">Separating soundness, feasibility, fit, and distinctness makes score manipulation harder than asking one judge for a single “best idea” number.</INFERENCE> [arxiv.org](https://arxiv.org/abs/2607.22375) [deepmind.google](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/) [arxiv.org](https://arxiv.org/abs/2410.02736) ([arxiv.org](https://arxiv.org/abs/2607.22375))

**(High Confidence)** LLM-as-a-judge systems have measurable position bias. One 2024 study evaluated 12 judge models across more than 100,000 instances and found non-random position bias that varied by task, model, and the quality gap between compared outputs. [arxiv.org](https://arxiv.org/abs/2406.07791) ([arxiv.org](https://arxiv.org/abs/2406.07791))

**(High Confidence)** Judge bias is broader than ordering. CALM identifies 12 potential biases, including position, verbosity, self-enhancement, authority, bandwagon, distraction, sentiment, chain-of-thought, and diversity-related effects. [arxiv.org](https://arxiv.org/abs/2410.02736) ([arxiv.org](https://arxiv.org/abs/2410.02736))

**(Medium Confidence)** LLM judges may prefer more familiar, lower-perplexity text over genuinely superior alternatives, even when the text was not generated by the judge itself. This creates a direct risk that a judge suppresses unusual but valuable `adhd` ideas. [arxiv.org](https://arxiv.org/abs/2410.21819) ([arxiv.org](https://arxiv.org/abs/2410.21819?utm_source=openai))

**Recommended judge protocol.**

1. **Blind ideas:** Remove frame names, agent IDs, prose styling, and “wildcard” labels before judging.
2. **Order swap:** Run every pairwise comparison as A/B and B/A; discard or escalate unstable decisions.
3. **Two judge families:** Use a different provider/model family from the generator where feasible.
4. **Three independent rubrics:** One judge for soundness/feasibility, one for non-obviousness/distinctness, one red-team trap detector.
5. **Confidence-aware escalation:** If judges disagree materially or cite different mechanisms, mark “human review required.”
6. **Periodic human calibration:** Maintain a task-specific set of blinded human ratings and re-test whenever model, prompt, or rubric changes.

<INFERENCE from="position-bias study; self-preference study; MAST verification failures; current ADHD API critic-model option">A single independent critic is better than self-critique, but not sufficient for novel ideation selection; swapped pairwise judgment and calibration make the remaining error observable.</INFERENCE> [arxiv.org](https://arxiv.org/abs/2406.07791) [arxiv.org](https://arxiv.org/abs/2410.21819) [arxiv.org](https://arxiv.org/abs/2503.13657) [github.com](https://github.com/UditAkhourii/adhd/blob/main/documentation/api.md) ([arxiv.org](https://arxiv.org/abs/2406.07791))

**(Medium Confidence)** On a Japanese Alternative Uses Test study, a GPT-4 protocol using “explain first, rate later” correlated with crowd ground truth at *r* = .62 for novelty, .59 for feasibility, and .33 for value. This supports automated triage for specific, calibrated creativity tasks, but the weak value correlation is a warning against fully automating strategic selection. [bpspsychub.onlinelibrary.wiley.com](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjop.12720) ([bpspsychub.onlinelibrary.wiley.com](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjop.12720?utm_source=openai))

**Recommended convergence rule.**

```text
eligible = ideas where:
  soundness >= S_min
  feasibility >= F_min
  fit >= R_min
  trap_status != "unrepaired"

shortlist = greedy_max_min(
  eligible,
  quality = 0.30*soundness + 0.25*feasibility
            + 0.20*fit + 0.15*non_obviousness
            + 0.10*reversibility,
  diversity = signature_distance,
  max_one_per_cluster = true
)
```

<INFERENCE from="MAP-Elites quality-diversity objective; IDEAgent maximum-clique diverse-set selection; LLM judge bias evidence">The numeric coefficients are proposed defaults, not empirical constants. The essential change is quality floors plus diversity-aware set selection, which avoids selecting three variants of the same high-scoring mechanism.</INFERENCE> [frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full) [arxiv.org](https://arxiv.org/abs/2607.22375) ([frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full?utm_source=openai))

#### 4. Creativity evaluation benchmarks and metrics

**(High Confidence)** Creativity should not be measured by idea count alone. Torrance-style divergent-thinking evaluation uses fluency, flexibility, originality, and elaboration; a 2024 LLM study adapted these dimensions across seven tasks and found models stronger in elaboration than originality. [arxiv.org](https://arxiv.org/abs/2401.12491) ([arxiv.org](https://arxiv.org/abs/2401.12491?utm_source=openai))

**(Medium Confidence)** The Divergent Association Task measures semantic distance among generated unrelated concepts, while the Alternative Uses Task evaluates unusual uses of familiar objects. Both are useful probes of divergent thinking but are incomplete proxies for real software/design ideation because they insufficiently assess implementability and domain fit. [aclanthology.org](https://aclanthology.org/2023.findings-emnlp.858.pdf) ([aclanthology.org](https://aclanthology.org/2023.findings-emnlp.858.pdf))

**(Medium Confidence)** A large 2026 human-versus-LLM creativity comparison reports 9,198 human participants and 215,542 LLM observations on an established divergent-creativity task. The scale is valuable, but benchmark-task results should not be equated with product or architecture innovation. [nature.com](https://www.nature.com/articles/s41562-025-02331-1.pdf) ([nature.com](https://www.nature.com/articles/s41562-025-02331-1.pdf?utm_source=openai))

**(Medium Confidence)** A 2025 study evaluating 14 models on DAT and AUT reported that only 0.28% of LLM-generated responses reached the top 10% of human creativity benchmarks. This conflicts in emphasis with studies finding high average novelty: average semantic novelty and rare, high-end human creativity are different targets. [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S2713374525000202) ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S2713374525000202?utm_source=openai))

**Recommended evaluation dashboard for `adhd`.**

| Metric | What it measures | Use | Failure mode detected |
|---|---|---|---|
| Fluency | Number of valid candidates | Diagnostic only | Under-generation. |
| Flexibility | Number of mechanism/intervention clusters | Primary diversity metric | Superficial variation. |
| Mean pairwise semantic distance | Overall spread | Monitor, not optimize alone | Lexical or semantic collapse. |
| Cluster coverage | Number of descriptor-grid cells with a viable elite | Primary QD metric | Overconcentration in one niche. |
| Yield | Largest mutually distinct set that clears quality floors | Primary release metric | “Novel but unusable” outputs. |
| Human-blind novelty/feasibility | External validity | Periodic benchmark | Judge drift. |
| Trap precision/recall | Whether flagged traps were genuinely problematic | Safety/utility | Performative red-teaming. |
| Shortlist redundancy | Pairwise similarity among final three | Hard acceptance test | Convergence collapse. |

<INFERENCE from="Torrance-style dimensions; IDEAgent Yield; semantic-diversity and human-comparison studies">Use a portfolio rather than a single creativity score: semantic distance measures divergence, while feasibility and soundness guard against random novelty.</INFERENCE> [arxiv.org](https://arxiv.org/abs/2401.12491) [arxiv.org](https://arxiv.org/abs/2607.22375) [arxiv.org](https://arxiv.org/abs/2409.04109) ([arxiv.org](https://arxiv.org/abs/2401.12491?utm_source=openai))

#### 5. Practical prompt-level findings from 2024–2026 research and practitioner writing

**(High Confidence)** Keep a decomposition step before generation. In two separate idea-diversity studies, chain-of-thought-style prompting increased diversity relative to other tested prompts. [arxiv.org](https://arxiv.org/abs/2402.01727) [arxiv.org](https://arxiv.org/abs/2602.20408) ([arxiv.org](https://arxiv.org/abs/2402.01727))

**(Medium Confidence)** Replace celebrity-genius prompts with concrete ordinary roles tied to distinct knowledge distributions: “municipal procurement officer,” “legacy-system maintainer,” “night-shift support lead,” “accessibility tester,” or “bootstrapped founder.” A 2026 working paper found ordinary personas outperformed “creative entrepreneur” prompts for knowledge partitioning. [arxiv.org](https://arxiv.org/abs/2602.20408) ([arxiv.org](https://arxiv.org/abs/2602.20408?utm_source=openai))

**(Medium Confidence)** Use separate persona calls rather than asking one model to merge several personas into a single collective voice. A 2025 design study found parallel and sequential multi-persona strategies produced more diverse concepts than collective prompting; in sequential prompting, the current persona largely dominated each step rather than combining knowledge bases. [cambridge.org](https://www.cambridge.org/core/journals/design-science/article/enhancing-design-concept-diversity-multipersona-prompting-strategies-for-large-language-models/3B346E253508337A4EE899499BE49D9B) ([cambridge.org](https://www.cambridge.org/core/journals/design-science/article/enhancing-design-concept-diversity-multipersona-prompting-strategies-for-large-language-models/3B346E253508337A4EE899499BE49D9B))

**Prompt changes to ship:**

| Current instruction | Replace with | Expected effect |
|---|---|---|
| “The first three obvious answers are banned.” | “First list the three default mechanisms privately. Propose a mechanism that differs from each on cause, intervention locus, or assumption. State which differs.” | Makes anti-anchoring testable. |
| “Generate six short distinct ideas.” | “Generate four ideas from four distinct mechanism families; no two may share the same causal diagnosis.” | Prevents local paraphrase diversity. |
| “Use frame: biology/logistics/game design.” | “Extract one transferable mechanism, state its source-domain constraint, map it to the target, then state where the analogy breaks.” | Prevents decorative analogies. |
| “Do not evaluate.” | “Do not rank. You may state an assumption and falsifier for each idea.” | Preserves divergence while improving later verification. |
| “Deepen top three.” | “Deepen one winner from each of the three most distinct viable clusters.” | Prevents redundant deepening. |

<INFERENCE from="Deng et al. ordinary-persona and CoT findings; Cambridge multi-persona study; existing ADHD prompt">These edits retain `adhd`’s concise JSON-first operation while making “distinct” a causal and structural requirement rather than a stylistic request.</INFERENCE> [arxiv.org](https://arxiv.org/abs/2602.20408) [cambridge.org](https://www.cambridge.org/core/journals/design-science/article/enhancing-design-concept-diversity-multipersona-prompting-strategies-for-large-language-models/3B346E253508337A4EE899499BE49D9B) [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) ([arxiv.org](https://arxiv.org/abs/2602.20408?utm_source=openai))

### What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** The current state is that LLMs can produce many novel-seeming ideas quickly, but reliable diversity and feasibility require system design beyond one-shot prompting. A large blind study recruited more than 100 NLP researchers; AI ideas were rated more novel than human ideas, while feasibility was slightly weaker and LLM self-evaluation/diversity remained open problems. [arxiv.org](https://arxiv.org/abs/2409.04109) ([arxiv.org](https://arxiv.org/abs/2409.04109))

**(Medium Confidence)** Structured multi-agent collaboration can improve final idea quality, but the benefit depends on interaction topology and role diversity rather than agent count alone. A 2025 scientific-ideation study reports that larger cohorts, deeper dialogue, and persona heterogeneity enriched diversity, while critic-side diversity improved feasibility. [arxiv.org](https://arxiv.org/abs/2507.08350) ([arxiv.org](https://arxiv.org/abs/2507.08350))

**(High Confidence)** The strongest counterweight is recent evidence that coupling agents together can reduce diversity. A 2026 ACL Findings study concluded that simply increasing agents does not guarantee idea diversity and found blind-writing/subgroup-isolation designs higher-diversity than structurally coupled alternatives, with only modest quality differences. [aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf) ([aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf))

**(High Confidence)** `adhd` is directionally well aligned with this evidence because it uses a hard isolation boundary during divergence and a separate critic phase. However, its documentation reports a reproducible but maintainer-owned evaluation across six open-ended engineering tasks scored by an LLM judge; that is useful regression evidence, not independent proof of generalized superiority. [github.com](https://github.com/UditAkhourii/adhd/blob/main/documentation/evals.md) [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) ([github.com](https://github.com/UditAkhourii/adhd/blob/main/documentation/evals.md))

**(Medium Confidence)** The current skill claims “about 10 Agent calls, 30 to 90 seconds wall clock, 5 to 10x a single answer.” Its CLI defaults are five frames, six ideas per frame, top-three deepening, and concurrency four. These are operational defaults, not experimentally justified optima. [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) [github.com](https://github.com/UditAkhourii/adhd/blob/main/documentation/api.md) ([github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md))

| Implementation / route | Parameter Count | Context Window | Documented Latency | Documented Cost | License | Technical implication |
|---|---:|---:|---|---|---|---|
| Current Claude Code skill | Model-dependent; not specified | Model-dependent; each branch receives problem, user context, one frame | “30 to 90 seconds wall clock” | “5 to 10x a single answer” | MIT | Good isolation; unknown model-level reproducibility. [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) |
| `adhd-agent` CLI/library | SDK-default model unless overridden | Model-dependent; supports injected file context | Not documented separately | Not documented in currency/token terms | MIT | Supports `--critic-model`, enabling cross-family judging. [github.com](https://github.com/UditAkhourii/adhd/blob/main/documentation/api.md) |
| Proposed Blind QD Islands | Model-dependent | Model-dependent; archive summaries should be compact | <MISSING_DATA>[Benchmark required on selected provider/model pair.]</MISSING_DATA> | <MISSING_DATA>[Token accounting required after schema implementation.]</MISSING_DATA> | MIT-compatible design | Adds archive/judge passes; can reduce wasted deepening by deepening only cluster winners. |

<MISSING_DATA>[Exact parameter counts, context windows, API schemas beyond the local TypeScript options, provider rate limits, token pricing, and latency percentiles were sought for the deployed runtime. The repository delegates model choice to the Agent SDK and does not publish a fixed provider/model configuration. A reproducible benchmark must pin model IDs, regions, SDK version, concurrency, token counts, and rate-limit tier.]</MISSING_DATA>

### What are the contrasting viewpoints or competing evidence?

**(Medium Confidence)** One body of evidence supports LLMs as productive novelty generators: the large NLP study found AI ideas more novel than expert ideas under blind review, with AI novelty means of 5.64 and 5.81 versus 4.84 for human ideas in one analysis. [arxiv.org](https://arxiv.org/abs/2409.04109) ([arxiv.org](https://arxiv.org/abs/2409.04109))

**(Medium Confidence)** Competing evidence warns that LLM originality may be shallow, benchmark-specific, or concentrated below the exceptional human tail. A Torrance-style study found LLM creativity primarily weaker in originality, while a 2025 multi-model study found only 0.28% of outputs reached the top 10% human-creative benchmark. [arxiv.org](https://arxiv.org/abs/2401.12491) [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S2713374525000202) ([arxiv.org](https://arxiv.org/abs/2401.12491?utm_source=openai))

<CONFLICTING_EVIDENCE>[Si, Yang, and Hashimoto’s 2024/2025 research-ideation study finds higher judged AI novelty than expert-human novelty; Torrance-style and divergent-thinking studies find weaker originality or rare top-tail performance. The evidence is not directly contradictory because the tasks, populations, domains, novelty definitions, and human baselines differ. The first measures blinded NLP-research proposal ratings; the latter measures divergent-thinking or verbal-creativity performance.]</CONFLICTING_EVIDENCE>

**(High Confidence)** Debate has competing effects. Multi-agent debate can prevent a single model’s “degeneration-of-thought” during reflective reasoning, but multi-agent interaction can also generate conformity, sycophancy, and diversity collapse. [aclanthology.org](https://aclanthology.org/2024.emnlp-main.992/) [aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf) ([aclanthology.org](https://aclanthology.org/2024.emnlp-main.992/))

<INFERENCE from="Liang et al. 2024 multi-agent debate; Liang et al. 2026 diversity collapse">The operational resolution is not to reject debate, but to sequence it after independent generation and cluster selection, where its role is feasibility repair rather than creative exploration.</INFERENCE> [aclanthology.org](https://aclanthology.org/2024.emnlp-main.992/) [aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf) ([aclanthology.org](https://aclanthology.org/2024.emnlp-main.992/))

**(High Confidence)** More agents are not automatically better. A multi-agent failure analysis across 1,642 execution traces identifies 14 failure modes across specification/system design, inter-agent misalignment, and verification/termination. It found that prompt and topology interventions can help but do not eliminate failures. [arxiv.org](https://arxiv.org/abs/2503.13657) ([arxiv.org](https://arxiv.org/abs/2503.13657))

### What changed recently, and what is the trajectory?

**(High Confidence)** The trajectory from 2023 to 2026 is from generic chain/tree prompting toward **search architectures with explicit external state**: thought trees and graphs, multi-agent role structures, evolutionary archives, verifier-backed optimization, and quality-diversity objectives. [arxiv.org](https://arxiv.org/abs/2305.10601) [arxiv.org](https://arxiv.org/abs/2308.09687) [deepmind.google](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/) [arxiv.org](https://arxiv.org/abs/2607.22375) ([arxiv.org](https://arxiv.org/abs/2305.10601?utm_source=openai))

**(High Confidence)** The 2025–2026 shift is especially clear in the move from “more agents and more dialogue” to “better topology and explicit diversity control.” Recent work simultaneously reports benefits from heterogeneous critic/revision systems and harms from dense structural coupling. [arxiv.org](https://arxiv.org/abs/2507.08350) [aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf) ([arxiv.org](https://arxiv.org/abs/2507.08350))

**(Medium Confidence)** The likely near-term winning pattern for practical agent skills is not an expensive general-purpose agent society. It is a compact architecture that uses cheap independent generation, deterministic clustering/deduplication, selective stronger-model judgment, and human escalation for the narrow set of ideas that matter. <INFERENCE from="AlphaEvolve fast-model breadth plus strong-model depth; MAST multi-agent failure analysis; current ADHD cost profile">This minimizes both correlated exploration and unnecessary multi-agent conversation while maintaining traceability.</INFERENCE> [deepmind.google](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) [arxiv.org](https://arxiv.org/abs/2503.13657) [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) ([deepmind.google](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/))

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| ChatGPT support can increase idea detail while reducing semantic distinction across users. | Anderson, Shah, Kreminski | February 2, 2024 | Comparative 36-participant user study; primary preprint | https://arxiv.org/abs/2402.01536 |
| GPT-4 idea pools were less diverse than human groups; CoT was the strongest tested diversity prompt. | Meincke, Mollick, Terwiesch | January 2024 | Controlled ideation experiment; primary preprint | https://arxiv.org/abs/2402.01727 |
| Fixation and knowledge concentration reduce LLM idea diversity; CoT plus ordinary personas improved diversity. | Deng, Brucks, Toubia | March 2026 | Four-study working paper; primary but not yet peer-reviewed | https://arxiv.org/abs/2602.20408 |
| Parallel/sequential multi-persona prompts produced more diverse design concepts than collective prompting. | Design Science study | 2025 | Empirical design-ideation study; peer-reviewed journal source | https://www.cambridge.org/core/journals/design-science/article/enhancing-design-concept-diversity-multipersona-prompting-strategies-for-large-language-models/3B346E253508337A4EE899499BE49D9B |
| Dense interaction and structural coupling can cause diversity collapse; blind writing/subgroup isolation preserve diversity. | Liang et al. | 2026 | ACL Findings empirical open-ended ideation study; peer-reviewed proceedings source | https://aclanthology.org/2026.findings-acl.13.pdf |
| LLM research ideas were judged more novel, but slightly weaker on feasibility, than expert human ideas. | Si, Yang, Hashimoto | September 2024; ICLR 2025 version | Large blind human study with 100+ researchers; primary research | https://arxiv.org/abs/2409.04109 |
| QD/MAP-Elites maintains many high-performing behaviorally distinct solutions. | Pugh, Soros, Stanley | 2016 | Peer-reviewed QD review; authoritative foundational synthesis | https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full |
| FunSearch combines LLM generation, automated evaluation, evolutionary selection, diversity mechanisms, and parallelism. | Google DeepMind / Fawzi and Romera Paredes | December 14, 2023 | Official research description tied to Nature paper; primary organization source | https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/ |
| AlphaEvolve combines fast breadth models, strong depth models, and automated evaluators. | Google DeepMind | May 2025 | Official primary engineering/research report | https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ |
| IDEAgent uses semantic signatures, quality-diversity Yield, repair/refinement, and explicit historical comparisons. | Gumma et al. | July 28, 2026 | Primary preprint; directly relevant but not independently replicated | https://arxiv.org/abs/2607.22375 |
| Position bias in LLM judges persists across 100,000+ evaluation instances. | Shi et al. | June 2024 | Large-scale systematic judge-bias study; primary preprint | https://arxiv.org/abs/2406.07791 |
| LLM-as-judge systems show multiple biases including verbosity, authority, self-enhancement, and distraction effects. | Ye et al. | October 2024 | Bias taxonomy and experiments; primary preprint | https://arxiv.org/abs/2410.02736 |
| LLM judges favor familiar/lower-perplexity text, creating self-preference risk. | Wataoka, Takahashi, Ri | October 2024 | Quantitative bias study; primary preprint | https://arxiv.org/abs/2410.21819 |
| `adhd` currently uses five isolated branches, six ideas per branch, global scoring, clustering, and top-three deepening. | UditAkhourii/adhd | Accessed August 7, 2026 | Current implementation documentation; authoritative source for product behaviour | https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md |
| `adhd` current evaluation is six engineering problems scored by an LLM judge with randomized A/B order. | UditAkhourii/adhd | Accessed August 7, 2026 | Current project eval documentation; useful but maintainer-owned | https://github.com/UditAkhourii/adhd/blob/main/documentation/evals.md |
| Multi-agent systems exhibit 14 empirically derived failure modes across design, alignment, and verification. | Cemri et al. | March 2025 | Analysis of 1,642 traces across seven frameworks; primary preprint | https://arxiv.org/abs/2503.13657 |

## Knowledge Gaps

### By evidence quality

- <MISSING_DATA>[A peer-reviewed, independently replicated study that directly compares fixed-frame isolated ideation, QD-archive ideation, debate, and single-agent best-of-*N* under equal token/cost budgets for software architecture tasks.]</MISSING_DATA>

- <MISSING_DATA>[A validated universal semantic-distance threshold for “same mechanism” versus “distinct idea.” Thresholds need calibration on `adhd`’s actual task distribution and human annotations.]</MISSING_DATA>

- <INSUFFICIENT_EVIDENCE>[That any fixed score weighting—current `0.35 / 0.40 / 0.25` or the proposed alternative—generalizes across naming, API design, debugging, product strategy, and architecture.]</INSUFFICIENT_EVIDENCE>

### By evaluation validity

- <MISSING_DATA>[Human-labelled `adhd` benchmark with blinded expert ratings of non-obviousness, soundness, feasibility, usefulness, and final-shortlist redundancy.]</MISSING_DATA>

- <INSUFFICIENT_EVIDENCE>[That the current skill’s LLM-judge improvements—breadth 9.00 versus 4.83, novelty 7.83 versus 2.67, and trap detection 9.50 versus 1.83—would persist with independent judges, human evaluators, equal-token best-of-*N* baselines, and unseen tasks.]</INSUFFICIENT_EVIDENCE> [github.com](https://github.com/UditAkhourii/adhd/blob/main/documentation/evals.md) ([github.com](https://github.com/UditAkhourii/adhd/blob/main/documentation/evals.md))

### By operational deployment

- <MISSING_DATA>[Pinned model identifiers, context limits, API request/response schemas beyond local `RunOptions`, token use by phase, provider rate limits, price, and p50/p95 latency for the deployed `adhd` configuration.]</MISSING_DATA>

- <MISSING_DATA>[The team size, deployment environment, preferred provider, and acceptable latency/cost envelope needed to choose between embedding-based semantic de-duplication, LLM-only signatures, or a hybrid implementation.]</MISSING_DATA>

## Recommended Next Steps

1. **Implement a feature-flagged `qd` convergence mode.**  
   **Rationale:** Replace global top-three ranking with semantic signatures, quality floors, one elite per cluster, and max-min selection. Run it alongside the existing scorer so regressions are visible. <INFERENCE from="MAP-Elites; IDEAgent; current ADHD score flow">This is the smallest architectural change with the clearest expected effect on redundant shortlists.</INFERENCE> [frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full) [arxiv.org](https://arxiv.org/abs/2607.22375) [github.com](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md) ([frontiersin.org](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full?utm_source=openai))

2. **Replace frame selection with a tested portfolio generator.**  
   **Rationale:** Require one ordinary stakeholder persona, one operational constraint frame, one adversarial/inversion frame, one cross-domain mechanism frame, and one wildcard. Log each frame’s marginal cluster contribution and retire frames that repeatedly generate redundant ideas. [arxiv.org](https://arxiv.org/abs/2602.20408) [cambridge.org](https://www.cambridge.org/core/journals/design-science/article/enhancing-design-concept-diversity-multipersona-prompting-strategies-for-large-language-models/3B346E253508337A4EE899499BE49D9B) ([arxiv.org](https://arxiv.org/abs/2602.20408?utm_source=openai))

3. **Build a real evaluation harness before changing defaults.**  
   **Rationale:** Compare: single-shot, best-of-*N* single agent, current `adhd`, isolated frames plus QD, and debate-first designs at equal token budgets. Score with human-blind ratings plus diversity/Yield metrics; include position-swapped LLM judges only as supplementary signals. [arxiv.org](https://arxiv.org/abs/2409.04109) [arxiv.org](https://arxiv.org/abs/2406.07791) [aclanthology.org](https://aclanthology.org/2026.findings-acl.13.pdf) ([arxiv.org](https://arxiv.org/abs/2409.04109))

4. **Add a bounded post-cluster adversarial repair pass.**  
   **Rationale:** Assign a different critic frame to each cluster winner—security/on-call, economics, product adoption, or implementation feasibility—and require either a concrete repair or exclusion. Do not expose islands to one another before this point. [arxiv.org](https://arxiv.org/abs/2507.08350) [arxiv.org](https://arxiv.org/abs/2503.13657) ([arxiv.org](https://arxiv.org/abs/2507.08350))

5. **Publish reproducibility metadata with every benchmark run.**  
   **Rationale:** Persist model IDs, sampling settings, frame set, branch outputs, semantic signatures, judge prompts, A/B orders, costs, latencies, clustering thresholds, and human-review disagreements. This is necessary to distinguish genuine ideation improvement from judge preference or provider drift. <INFERENCE from="LLM judge bias literature; current ADHD model-delegating API">Without this metadata, a future model update can silently change apparent novelty, diversity, or judge agreement.</INFERENCE> [arxiv.org](https://arxiv.org/abs/2410.02736) [github.com](https://github.com/UditAkhourii/adhd/blob/main/documentation/api.md) ([arxiv.org](https://arxiv.org/abs/2410.02736))

## Sources

- [adhd/skills/adhd/SKILL.md at main · UditAkhourii/adhd · GitHub](https://github.com/UditAkhourii/adhd/blob/main/skills/adhd/SKILL.md)
- [Examining and Addressing Barriers to Diversity in LLM-Generated Ideas](https://arxiv.org/abs/2602.20408?utm_source=openai)
- [https://aclanthology.org/2026.findings-acl.13.pdf](https://aclanthology.org/2026.findings-acl.13.pdf)
- [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791)
- [Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers](https://arxiv.org/abs/2409.04109)
- [Homogenization Effects of Large Language Models on Human Creative Ideation](https://arxiv.org/abs/2402.01536?utm_source=openai)
- [Prompting Diverse Ideas: Increasing AI Idea Variance](https://arxiv.org/abs/2402.01727?utm_source=openai)
- [IDEAgent: Agentic Quality-Diversity Search for Research Idea Generation](https://arxiv.org/abs/2607.22375)
- [Prompting Diverse Ideas: Increasing AI Idea Variance](https://arxiv.org/abs/2402.01727)
- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601?utm_source=openai)
- [Frontiers | Quality Diversity: A New Frontier for Evolutionary Computation](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full?utm_source=openai)
- [AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms — Google DeepMind](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
- [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge](https://arxiv.org/abs/2410.02736)
- [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819?utm_source=openai)
- [Assessing novelty, feasibility and value of creative ideas with an unsupervised approach using GP...](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjop.12720?utm_source=openai)
- [Assessing and Understanding Creativity in Large Language Models](https://arxiv.org/abs/2401.12491?utm_source=openai)
- [https://aclanthology.org/2023.findings-emnlp.858.pdf](https://aclanthology.org/2023.findings-emnlp.858.pdf)
- [A large-scale comparison of divergent creativity in humans and large language models | Nature Hum...](https://www.nature.com/articles/s41562-025-02331-1.pdf?utm_source=openai)
- [Has the creativity of large-language models peaked?: An analysis of inter- and intra-LLM variabil...](https://www.sciencedirect.com/science/article/pii/S2713374525000202?utm_source=openai)
- [Enhancing design concept diversity: multi-persona prompting strategies for large language models ...](https://www.cambridge.org/core/journals/design-science/article/enhancing-design-concept-diversity-multipersona-prompting-strategies-for-large-language-models/3B346E253508337A4EE899499BE49D9B)
- [Exploring Design of Multi-Agent LLM Dialogues for Research Ideation](https://arxiv.org/abs/2507.08350)
- [adhd/documentation/evals.md at main · UditAkhourii/adhd · GitHub](https://github.com/UditAkhourii/adhd/blob/main/documentation/evals.md)
- [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate - ACL Anthology](https://aclanthology.org/2024.emnlp-main.992/)
- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)
