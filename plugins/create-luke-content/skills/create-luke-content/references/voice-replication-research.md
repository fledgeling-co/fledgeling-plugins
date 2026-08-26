# Voice Replication — Empirical Evidence Base

Distilled from a deep-research synthesis on AI voice extraction and reproduction (stylometry, authorship-verification benchmarks, and LLM style-transfer studies, 2017–2026). This is the *why* behind the extraction and lint protocols. Consult it when the user asks why a rule exists, when calibrating expectations of fidelity, or when tempted to trade a mechanical rule for an adjective.

## Load-bearing findings

- **(High) The deepest voice markers are subconscious structure, not vocabulary.** Function-word distribution (articles, prepositions, pronouns, auxiliaries), syntactic constructions (clause types, active/passive habits), punctuation habits, and formatting idiosyncrasies are the most stable, topic-independent authorship signals. Signature phrases matter, but they sit on top of a structural fingerprint the author doesn't know they have.
- **(High) LLMs have their own rigid fingerprint that actively resists a target voice.** Instruction-tuned models use participial clauses at 2–5× human rates and nominalizations at 1.5–2×, almost never use agentless passive, and default to an information-dense corporate-academic register (PNAS, Reinhart et al. 2025). This "style pull" routinely overrides persona instructions — which is why personas must encode *counter-rules* (plain verbs over nominalizations, the person's actual passive/active habit) rather than trust a description to hold.
- **(High) Exemplars beat descriptions, and saturate around five.** Few-shot anchoring outperforms zero-shot persona prompting on every stylistic metric, but gains plateau after ~5 exemplars (Wang et al., EMNLP 2025). Past that point, *diversity* (registers, moods, lengths) buys more than volume. This is the empirical basis for the 5–8 verbatim sample anchors: enough for saturation, chosen for spread.
- **(High) Replication is measurably hardest for informal voice.** LLMs match structured writing (emails, formal documents) well and fail on casual idiolects (blogs, chat, social). The Slack/short-form variants of a persona package need the most corpus evidence and the most conservative fidelity claims — exactly where users assume it's easiest.
- **(High) A model judging its own voice fidelity is circular.** LLM-as-judge scores of style match correlate near zero (|r| < 0.07) with trained authorship-verification models; inference-time personalization scores *below the random-stranger baseline* on LUAR (0.48–0.51 vs the 0.626 cross-author floor; same-author ceiling 0.756). Treat any self-assessed "this sounds like them" as defect-catching, never certification. Fidelity is judged by deterministic checks and by the person themselves.
- **(High) Style–content entanglement is a real failure mode.** Models conflate an exemplar's style with its facts and hallucinate the exemplar's content into new pieces. Anchors are style ground truth only.
- **(Medium) Long generations drift back to the model's baseline.** Persona adherence decays over long outputs; effective mitigations re-anchor in chunks rather than trusting one upfront instruction (drift rates as low as ~3% with per-chunk anchoring vs unchecked decay).
- **(Medium) Low entropy is a tell even when the surface style matches.** LLM text mimicking an author runs at roughly half the perplexity of the real author (15.2 vs 29.5 in matched essays): uniform sentence lengths, predictable word choice. Humans are spiky. Deliberately varying rhythm is a fidelity lever, not a nicety.
- **(High) Word counts, not sample counts, determine profile stability.** Basic syntactic patterns emerge at ~300–500 words; function-word distributions stabilize around ~2,000 words; forensic-grade confidence needs ~2,500+ (Eder 2017 and successors). Grade the corpus in words.

## What this means for the package protocol

| Protocol element | Evidence it rests on |
|---|---|
| Verbatim sample anchors, 5–8, register-diverse | Few-shot saturation at ~5; exemplars-beat-descriptions |
| Mechanics rules stated as mechanical constraints, never adjectives | "Be casual" invites the model's own prior; contraction/lexical/syntax rules transfer |
| Syntactic fingerprint section in the base voice (sentence-length variance, active/passive, nominalization habits) | LLM style pull; perplexity paradox |
| Deterministic lint + stylometric advisories | LLM-as-judge circularity; only mechanical measures are calibrated |
| Corpus tiers measured in words | Stylometric sample-size research |
| Anchors-are-not-facts hard rule | Style–content entanglement |
| Long-form re-anchoring per section | Style drift research |
| Extra evidence demanded for chat/short-form variants | Informal-register failure mode |

## The NNG tone dimensions (for variant register deltas)

Nielsen Norman Group's four tone-of-voice dimensions are the established qualitative frame; position each variant on all four so register deltas are explicit rather than vibes:

1. **Formal ↔ Casual** 2. **Serious ↔ Funny** 3. **Respectful ↔ Irreverent** 4. **Matter-of-fact ↔ Enthusiastic**

The mapping rule from the research: a dimension position is only real once translated into mechanical levers (casual = contractions enforced, simpler lexical choices, sentence-initial conjunctions allowed — not "write casually").

## Out of scope for a prompt-based skill (say so if asked)

- **LoRA/fine-tuning** — the highest-fidelity route for permanent brand voice, but requires training infrastructure and 100s–1000s of curated pairs.
- **Embedding-based verification (LUAR)** — the only calibrated fidelity metric; point users at it as an external validation option if they need measurement beyond the lint.
- **Decoding-time interventions** (neuron steering, contrastive decoding) — research-grade, not reachable from here.

A prompt-based package cannot fully close the measured authorship gap. What it can do — anchor on real exemplars, encode the structural fingerprint as rules, gate mechanically, re-anchor over length — is exactly the subset these studies show works at inference time. Be honest in delivery notes about which registers carry the most risk.
