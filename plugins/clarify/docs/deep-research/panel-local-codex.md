---
title: "Designing effective clarifying questions for AI coding agents"
run_id: dr_5611aacec4ff0a5d
question: "What does the evidence say about how to ask a person a decision question well — so they answer accurately, quickly, and without decision fatigue — and what are the documented failure modes of asking badly? Cover: (1) requirements-elicitation research in software engineering on ambiguity detection, unstated assumptions, and the measured cost of building the wrong thing from an under-specified brief; (2) survey and questionnaire methodology on question wording — question length and verbosity effects on response accuracy, jargon and readability effects on comprehension, satisficing and response-order effects, the measured cost of vague or double-barrelled questions; (3) judgment and decision-making research on choice architecture — choice overload and the optimal number of options, anchoring and default effects when a recommendation is presented first, whether recommending an option improves or degrades decision quality, and how offering a free-text escape hatch changes response behaviour; (4) human-computer interaction research on interruption cost — when interrupting someone is worth it, how question batching versus serial prompting affects total cost and answer quality, and how attention and context-switching costs are measured; (5) plain-language and readability research on the measured effect of simplifying wording on comprehension, response rate and error rate, including any measured word-count thresholds; (6) recent work on conversational AI and LLM agents asking clarifying questions — measured benefits and harms, over-asking versus under-asking, ambiguity detection before asking, and any benchmarks or evaluations of clarification quality in agentic systems."
provider: local-codex
model: Codex CLI
tier: max
archetype: academic
sources: 21
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 0.00
completed: 2026-08-09T07:59:26.089Z
---
Reading additional input from stdin...
2026-08-09T07:54:47.690932Z ERROR codex_models_manager::cache: failed to load models cache: missing field `base_instructions` at line 94 column 5
OpenAI Codex v0.146.0
--------
workdir: /Users/lukerhodes/Dev
model: gpt-5.6-terra
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019fe584-68f7-7522-900f-264be37d515b
--------
user
<role>
You are a senior research analyst synthesising scientific literature or reviewing methodology. Your output will directly Building a skill that decides when an AI coding agent should stop and ask its user a question, then composes it. Must defend with evidence: how many questions per batch; how many options each; whether to lead with a marked recommendation; how short and plain the text must be, with a word target; what test decides a question is worth asking rather than defaulting; and whether inviting a free-text note beside a chosen option improves what is learned..
</role>

<context>
This investigation supports a concrete decision. Keep this context tight, context bloat degrades long-running agentic output; domain knowledge belongs in the analysis lens below.
</context>

<core_directive>
Answer this decisively: What does the evidence say about how to ask a person a decision question well — so they answer accurately, quickly, and without decision fatigue — and what are the documented failure modes of asking badly? Cover: (1) requirements-elicitation research in software engineering on ambiguity detection, unstated assumptions, and the measured cost of building the wrong thing from an under-specified brief; (2) survey and questionnaire methodology on question wording — question length and verbosity effects on response accuracy, jargon and readability effects on comprehension, satisficing and response-order effects, the measured cost of vague or double-barrelled questions; (3) judgment and decision-making research on choice architecture — choice overload and the optimal number of options, anchoring and default effects when a recommendation is presented first, whether recommending an option improves or degrades decision quality, and how offering a free-text escape hatch changes response behaviour; (4) human-computer interaction research on interruption cost — when interrupting someone is worth it, how question batching versus serial prompting affects total cost and answer quality, and how attention and context-switching costs are measured; (5) plain-language and readability research on the measured effect of simplifying wording on comprehension, response rate and error rate, including any measured word-count thresholds; (6) recent work on conversational AI and LLM agents asking clarifying questions — measured benefits and harms, over-asking versus under-asking, ambiguity detection before asking, and any benchmarks or evaluations of clarification quality in agentic systems.
</core_directive>

<research_questions>
Primary:
1. Answer this decisively: What does the evidence say about how to ask a person a decision question well — so they answer accurately, quickly, and without decision fatigue — and what are the documented failure modes of asking badly? Cover: (1) requirements-elicitation research in software engineering on ambiguity detection, unstated assumptions, and the measured cost of building the wrong thing from an under-specified brief; (2) survey and questionnaire methodology on question wording — question length and verbosity effects on response accuracy, jargon and readability effects on comprehension, satisficing and response-order effects, the measured cost of vague or double-barrelled questions; (3) judgment and decision-making research on choice architecture — choice overload and the optimal number of options, anchoring and default effects when a recommendation is presented first, whether recommending an option improves or degrades decision quality, and how offering a free-text escape hatch changes response behaviour; (4) human-computer interaction research on interruption cost — when interrupting someone is worth it, how question batching versus serial prompting affects total cost and answer quality, and how attention and context-switching costs are measured; (5) plain-language and readability research on the measured effect of simplifying wording on comprehension, response rate and error rate, including any measured word-count thresholds; (6) recent work on conversational AI and LLM agents asking clarifying questions — measured benefits and harms, over-asking versus under-asking, ambiguity detection before asking, and any benchmarks or evaluations of clarification quality in agentic systems.

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
- general prompt-engineering advice for LLMs
- UI visual design and aesthetics
- market research on consumer purchasing
</exclude>
<time_horizon>
emphasise work from 2015 to present, and 2023 to present for the conversational-AI subtopic, while including foundational older results in survey methodology and decision science where they remain the standard citation
</time_horizon>
</scope_and_boundaries>

<source_discipline>
<prioritise>
- Primary and authoritative sources: official documentation, peer-reviewed literature, regulators, government databases, published benchmarks, raw datasets, court filings, filed financials.
- Peer-reviewed journals, conference proceedings from reputable venues, preprints clearly labelled as preprints, government research-agency publications, and systematic reviews.
</prioritise>
<deprioritise>
- Aggregator sites, SEO-optimised listicles, marketing blogs, vendor comparison pages, and content farms. Do not rely on these as primary evidence; if cited at all, label them `[SECONDARY: promotional]` and corroborate from a primary source.
- Popular-science summaries and news coverage as primary evidence for scientific claims.
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
- For each cited study extract the experimental methodology, sample size, statistical significance (p-values, confidence intervals, effect sizes where reported), and stated limitations, do not summarise only the abstract.
</depth_requirements>

<analysis_lens>
Apply these analytical frames where relevant, they tell you how to think about the findings, not only what to find:
- Explicitly distinguish points of scholarly consensus from points of active debate; do not equate preliminary preprints with peer-reviewed longitudinal data.
- convert each finding into a concrete authoring rule with a number attached where the evidence supports one
- flag where the evidence is contested or where lab findings may not transfer to expert users answering questions about their own work
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
Append an inline ``... (unusable citation URL)`` to every quantitative claim, every attributed statement, and every regulatory or legal reference, at the point of the claim itself. Do not aggregate citations at the end of a paragraph or into a bibliography, that is where source attribution is lost. If a URL is not verifiable at synthesis time, use ``UNVERIFIED (unusable citation URL)`` rather than omitting or inventing one.
</citation_protocol>

<output_format>
Structure the report exactly as follows:
- ## Executive Summary, 5-8 bullets, each led by a `(High Confidence)` / `(Medium Confidence)` / `(Low Confidence)` qualifier; usable as a standalone briefing.
- ## Detailed Findings, one section per research question, using the question as the heading; narrative prose with inline citations, tables for comparative data.
- ## Evidence Table, | Claim | Primary Source | Publication Date | Evidence Type | URL |, mapping every major claim to a verifiable source.
- ## Knowledge Gaps, what could not be answered, categorised by cause.
- ## Recommended Next Steps, 3-5 follow-up investigations, each with a stated rationale.
- Include a Methodological Comparison table wherever more than three studies address the same question.
</output_format>

<constraints>
- Do not fabricate citations, URLs, authors, or dates; use the unverified citation form when a source cannot be verified.
- Where data conflicts, present both positions with their evidence, do not silently pick one.
- Keep prose dense but readable; avoid filler phrases.
- Cite inline at the point of the claim, never aggregated at the end.
</constraints>

<core_directive>
Answer this decisively: What does the evidence say about how to ask a person a decision question well — so they answer accurately, quickly, and without decision fatigue — and what are the documented failure modes of asking badly? Cover: (1) requirements-elicitation research in software engineering on ambiguity detection, unstated assumptions, and the measured cost of building the wrong thing from an under-specified brief; (2) survey and questionnaire methodology on question wording — question length and verbosity effects on response accuracy, jargon and readability effects on comprehension, satisficing and response-order effects, the measured cost of vague or double-barrelled questions; (3) judgment and decision-making research on choice architecture — choice overload and the optimal number of options, anchoring and default effects when a recommendation is presented first, whether recommending an option improves or degrades decision quality, and how offering a free-text escape hatch changes response behaviour; (4) human-computer interaction research on interruption cost — when interrupting someone is worth it, how question batching versus serial prompting affects total cost and answer quality, and how attention and context-switching costs are measured; (5) plain-language and readability research on the measured effect of simplifying wording on comprehension, response rate and error rate, including any measured word-count thresholds; (6) recent work on conversational AI and LLM agents asking clarifying questions — measured benefits and harms, over-asking versus under-asking, ambiguity detection before asking, and any benchmarks or evaluations of clarification quality in agentic systems.
</core_directive>
warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
codex
I’ll ground this in primary studies and systematic reviews, separating solid design rules from plausible but unproven thresholds. I’ll prioritise methods and limitations rather than abstracts.
web search: 
web search: requirements engineering ambiguity underspecified requirements cost rework empirical study software requirements elicitation ...
web search: 
web search: site:pmc.ncbi.nlm.nih.gov survey question wording readability comprehension experiment jargon question length ...
web search: 
web search: 2024 2025 LLM agents clarification questions benchmark asking clarifying questions ambiguity detection paper ...
2026-08-09T07:55:13.912703Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-09T07:55:19.767392Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 'Participants'
2026-08-09T07:55:24.902054Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-09T07:55:29.490912Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: Lenzner Kaczmirek Lenzner 2010 cognitive burden survey questions question length wording response times experiment ...
2026-08-09T07:55:40.157188Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: default effect meta analysis choice architecture default option effect size systematic review ...
2026-08-09T07:55:45.794598Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: HCI interruption batching notifications batch versus immediate interruption experiment cost performance ...
2026-08-09T07:55:51.674242Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: software requirements errors cost rework empirical 32 industrial projects Kamata Tamai 2007 requirements quality ...
2026-08-09T07:56:01.002853Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-09T07:56:20.389072Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: "ClarifyGPT" "requirements clarification" benchmark sample results ...
2026-08-09T07:56:29.892829Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
codex
The strongest pattern is emerging: clarification has real value when it resolves a decision-critical unknown, but the research does not support universal “magic” counts or word limits. I’m treating those as explicit operational defaults, not pretending they are measured laws.
web search: 
web search: 
2026-08-09T07:56:40.340716Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
codex
## Executive Summary

- (High Confidence) Ask only when the answer can change a material action and a safe, reversible default is unavailable. This is an expected-value rule, not a magic ambiguity score: clarify when the likely cost of a wrong build exceeds the interruption and delay cost. <INFERENCE from="Kamata & Tamai (2007) association between weak contextual requirements and overruns; Mark et al. (2008) measured interruption stress; ClarifyGPT (2024) finding that asking on every request burdens users">Use a clarification gate based on decision divergence, reversibility, and expected harm—not on whether wording merely seems vague.</INFERENCE> [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure) [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) [doi.org](https://doi.org/10.1145/3660810)

- (High Confidence) Use one concise decision at a time; batch only independent decisions, with a hard cap of three. Evidence supports reducing repeated interruptions, but does not establish “three questions” as an empirical optimum. The cap is a conservative operational rule: it limits working-memory demands while avoiding serial context switches. [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) <MISSING_DATA>Direct experiments comparing 1, 2, 3, and 4 clarification questions in coding-agent conversations were sought; none were located. A representative benchmark with real coding users and task outcomes is needed.</MISSING_DATA>

- (High Confidence) Offer 2–4 mutually exclusive, collectively useful options; target 3. There is no universal optimal count: choice overload is conditional on complexity, difficulty, uncertainty, and decision goal, while large menus sometimes help. [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002)

- (High Confidence) Do not lead with a marked recommendation for a preference-sensitive decision. A first, preselected, or visibly endorsed option is an anchor/default: defaults have a pooled effect of *d* = 0.68, 95% CI [0.53, 0.83]. State the recommendation after neutral options, label it as advice rather than a selection, and give one short reason. [doi.org](https://doi.org/10.1017/bpp.2018.43) [doi.org](https://doi.org/10.1287/isre.2013.0497)

- (High Confidence) Target one plain-language sentence of ≤25 words for the question stem, with options of ≤10 words; validate a Flesch–Kincaid grade of ≤8 where feasible. The grade-8 target is supported as a survey-design rule of thumb; the 25/10-word limits are deliberately conservative authoring defaults, not measured thresholds. [doi.org](https://doi.org/10.1177/1525822X221124469) [doi.org](https://doi.org/10.1002/acp.1602) <INFERENCE from="Lenzner et al. (2010) found six of seven linguistic complexity features impaired clarity; Chin & Bruine de Bruin (2018) improved experience by simplifying prompts">A short, single-clause cap is a practical way to avoid the measured linguistic sources of burden, while grade level is the testable quality criterion.</INFERENCE> [doi.org](https://doi.org/10.1002/acp.1602) [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/)

- (Medium Confidence) Add an optional “Other / none fits — add a brief note” escape hatch when the listed options may omit a consequential state. It prevents forced misclassification and can surface unknown constraints, but mandatory or prominent free text increases burden and its quality declines late in questionnaires. [doi.org](https://doi.org/10.12758/mda.2019.05) <MISSING_DATA>A randomized comparison of selected-option-plus-optional-note versus selected-option-only in agent clarification has not been located.</MISSING_DATA>

- (High Confidence) Bad questions create measurable error: double-barrelled items changed meaning in six of eight tested items; difficult wording increased skips from 4.3% to 10.5% in one randomized survey experiment; interruption can preserve apparent speed while increasing stress, workload, frustration, time pressure, and effort. [doi.org](https://doi.org/10.2478/JOS-2020-0041) [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/) [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf)

## Detailed Findings

### 1. What does the evidence say about how to ask a person a decision question well — so they answer accurately, quickly, and without decision fatigue — and what are the documented failure modes of asking badly?

**Recommended skill policy**

| Component | Operational rule | Evidence status |
|---|---|---|
| Ask-or-default gate | Ask only if two plausible answers produce materially different implementation, risk, cost, or irreversible action; otherwise state the low-regret assumption and proceed. | <INFERENCE from="requirements-quality evidence; interruption-cost evidence">Decision-theoretic synthesis; no calibrated universal threshold.</INFERENCE> |
| Questions per batch | Ask 1 by default; batch 2–3 only when answers are independent and all are needed before the same next action. Never batch 4+. | <INSUFFICIENT_EVIDENCE>No direct coding-agent experiment identifies an optimum. The cap is a conservative design rule supported indirectly by interruption and choice-load evidence.</INSUFFICIENT_EVIDENCE> |
| Options | Provide 2–4 options, normally 3; include “Other / none fits” when coverage is uncertain. | High confidence against large, complex menus; medium confidence for the exact 2–4 range. |
| Recommendation | For objective, evidence-dominated choices: provide an unselected “Recommended” label after the neutral list with one reason. For preference-sensitive choices: do not recommend first; either ask neutrally or offer a reversible default. | High confidence that recommendation/default placement anchors; medium confidence on the best presentation remedy. |
| Wording | One decision, one sentence, ≤25-word stem; plain words; define unavoidable technical terms; target grade ≤8; option labels ≤10 words. | High confidence for simplicity/readability; exact word caps are operational, not causal thresholds. |
| Free-text note | “Other / none fits — brief note (optional).” Do not require a rationale for a normal choice. | Medium confidence: improves coverage in principle, with an observed burden/quality trade-off. |
| Serial follow-ups | Ask the next question only if it depends on the prior answer or a new decision-critical uncertainty appears. | High confidence as a consequence of interruption costs; direct agent evidence remains limited. |

**A usable question template**

> **Which deployment target should I use?**  
> A. Staging only  
> B. Production with approval  
> C. Production automatically  
> Other / none fits — brief note *(optional)*  
>
> Recommendation: **B**, because it preserves a human release check.

This format does not preselect B. It makes the recommendation inspectable rather than silently converting advice into a default. <INFERENCE from="Jachimowicz et al. (2019) default effects; Adomavicius et al. (2013) recommendation anchoring">Separating the selection control from the recommendation reduces, but cannot eliminate, endorsement/anchoring effects.</INFERENCE> [doi.org](https://doi.org/10.1017/bpp.2018.43) [doi.org](https://doi.org/10.1287/isre.2013.0497)

**Requirements elicitation and wrong-build cost.** Kamata and Tamai examined 32 completed business-application projects in one Tokyo development division, linking SRS-quality assessments to cost and schedule outcomes. Projects with weak context/purpose/overview material and richer functional detail tended toward cost overrun. This is strong evidence that omission of the “why/what context” can matter; it is observational, single-organisation evidence and does not yield a portable percentage cost penalty. [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure)

A 2015 systematic mapping review found 174 ambiguity-related requirements studies published from 1995–2015, but only 28 empirically evaluated studies. The review supports treating ambiguity as a real engineering concern, while also showing that tool-performance and cost-effectiveness claims are much less mature than conventional advice implies. [doi.org](https://doi.org/10.1109/EmpiRE.2015.7431303)

There is meaningful contrary evidence. Ribeiro and Berry’s three case studies, following two earlier studies, found that sampled persistent ambiguities in mature specifications did not cause serious downstream defects, apparently because normal inspections and discussions resolved them. This does not justify “never ask”: it means linguistic ambiguity alone is a poor gate. Ask when ambiguity implies divergent implementation, not merely when a word has multiple readings. The studies are case-based and may miss rare high-severity ambiguities. [doi.org](https://doi.org/10.1016/j.scico.2020.102472)

**Authoring rule.** <INFERENCE from="Kamata & Tamai (2007); Ribeiro & Berry (2020)">Do not ask “What do you mean?” for every ambiguity. Ask a concrete discriminating question only when each plausible interpretation yields a different artefact, interface, data model, safety/compliance outcome, or non-trivial rework path.</INFERENCE> [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure) [doi.org](https://doi.org/10.1016/j.scico.2020.102472)

**Survey wording, verbosity, jargon, and double-barrelling.** Lenzner, Kaczmirek, and Lenzner’s online psycholinguistic experiment compared well-written and degraded questions in one group of 490 respondents. Response time indexed burden; dropout and satisficing indexed quality. At least six of seven text features—including low-frequency words and difficult syntax—impaired question clarity. The study supports simple vocabulary and syntax, but does not establish a universal word count or prove that short questions are always more valid. [doi.org](https://doi.org/10.1002/acp.1602)

Chin and Bruine de Bruin randomly assigned 1,516 older US internet-panel respondents to an original or simplified stock-expectations question. Simplification reduced Flesch–Kincaid grade from 13.5 to 4.5, nonresponse from 10.5% to 4.3%, increased clarity from 5.8 to 6.0 on a seven-point scale, and reduced reported difficulty from 3.0 to 2.8; all reported tests were statistically significant (*p* ≤ .030). But simplification also reduced one self-reported confidence measure, and a second experiment found altered expectation estimates. Plain language improves completion and subjective comprehension; it can also change the construct respondents infer. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/)

Menold’s two controlled German online-panel experiments tested double-barrelled versus single-stimulus items: *N* = 497 and *N* = 435. Six of eight items yielded significant mean differences when their components were answered separately. Reliability differences were not significant, and validity did not uniformly favour either split component. The failure mode is therefore not simply “lower reliability”; it is uninterpretable meaning because respondents may weight one component, both, or neither. [doi.org](https://doi.org/10.2478/JOS-2020-0041)

**Authoring rule.** Ask exactly one decision per question. Treat “and,” “or,” combined objectives, and compound constraints as a defect trigger when a person could reasonably choose different answers to their parts. [doi.org](https://doi.org/10.2478/JOS-2020-0041)

**Satisficing and response order.** Krosnick’s satisficing framework predicts that cognitive demand encourages shortcuts: choosing the first plausible option, agreeing, selecting status quo, giving “don’t know,” straight-lining, or random selection. It is a foundational theory and literature review rather than one new effect-size experiment. [doi.org](https://doi.org/10.1002/acp.2350050305) Krosnick and Alwin’s split-ballot 1984 General Social Survey experiment documented response-order effects and predicted primacy effects particularly among less cognitively sophisticated respondents. [doi.org](https://doi.org/10.1086/268907)

**Authoring rule.** Keep options parallel in wording and length. Do not put the recommended option first for preference-sensitive choices. If ordering itself has no meaning, randomise it where the interface permits; if the agent must recommend, place advice outside the option order. <INFERENCE from="Krosnick & Alwin (1987); Jachimowicz et al. (2019)">This separates response-order bias from endorsement/default bias better than a marked first option.</INFERENCE> [doi.org](https://doi.org/10.1086/268907) [doi.org](https://doi.org/10.1017/bpp.2018.43)

**Choice architecture, number of options, and recommendations.** Scheibehenne, Greifeneder, and Todd meta-analysed 63 conditions from 50 published and unpublished experiments (*N* = 5,036) and found an average choice-overload effect near zero, with substantial heterogeneity and no sufficient condition. Chernev, Böckenholt, and Goodman’s later meta-analysis of 99 observations (*N* = 7,202) found overload after accounting for moderators: complex sets, difficult tasks, uncertain preferences, and an unfocused decision goal were especially risky. Neither meta-analysis identifies a universal optimal count. [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002)

Jachimowicz, Duncan, Weber, and Johnson’s meta-analysis included 58 default studies, pooled *N* = 73,675, and estimated *d* = 0.68, 95% CI [0.53, 0.83]. Effects varied substantially; some studies were null and two negative. Defaults work particularly when they signal endorsement or the status quo—which is precisely why a “Recommended” first option can distort an answer meant to reveal the user’s preference. [doi.org](https://doi.org/10.1017/bpp.2018.43) Adomavicius et al.’s three controlled laboratory studies found that recommender-system ratings anchored ratings of television programs, including a continuous effect across rating perturbations. These were consumer-rating tasks, so transfer to expert software decisions is plausible but not proven. [doi.org](https://doi.org/10.1287/isre.2013.0497)

**Authoring rule.** <INFERENCE from="choice-overload meta-analyses; default-effect meta-analysis">Three options is a good target, not a discovered optimum: it keeps the set small while retaining a meaningful alternative; use four only when omitting one would distort the decision, and split or sequence the decision above four.</INFERENCE> [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) [doi.org](https://doi.org/10.1017/bpp.2018.43)

**Free-text escape hatch.** Schmidt, Gummer, and Roßmann analysed open-ended attitude responses from 29 web surveys. Higher education and motivation predicted better response quality; placing the question later predicted fewer interpretable responses. The design supports a narrow optional note, especially for exceptional constraints, rather than demanding explanations from everyone. It does not test a selected-option-plus-note design, nor does it establish that free text improves final engineering outcomes. [doi.org](https://doi.org/10.12758/mda.2019.05)

**Interruption and batching.** Mark, Gudith, and Klocke conducted a counterbalanced 3×2 laboratory study with 48 participants on email work, comparing no interruption, same-context interruption, and different-context interruption every two minutes. Interrupted participants completed tasks faster but wrote shorter emails; errors were not significantly different. NASA-TLX workload, stress, frustration, time pressure, and effort were significantly higher under interruptions—for example, stress differed by condition, *F*(2,92) = 12.15, *p* < .001. The task was a simulated office task, mostly students, so do not use its time result as proof that interruption improves work. [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf)

Fitz et al.’s two-week randomised field experiment assigned 237 MTurk smartphone users to ordinary notifications, hourly batches, three daily batches, or none. Three daily batches—but not hourly batches—improved reported attention, productivity, mood, and control; disabling alerts increased anxiety/FoMO. This supports batching independent interruptions, but notification wellbeing is not directly equivalent to multi-question agent dialogue. [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) A 2025 web-probing experiment found that delayed retrospective probes required more time to recapitulate the original survey question and produced less interpretable content for one of three probes. Therefore, batch independent questions, but do not defer a question whose answer depends on fresh task context. [doaj.org](https://doaj.org/article/2d52a9f82a2747129cd2dacbce4fa30c)

**Authoring rule.** <INFERENCE from="Mark et al. (2008); Fitz et al. (2019); Hadler (2025)">Batch up to three independent, immediately needed decisions at a natural pause. Ask dependent or context-perishable questions serially and immediately after their prerequisite.</INFERENCE> [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) [doaj.org](https://doaj.org/article/2d52a9f82a2747129cd2dacbce4fa30c)

### 2. What is the current state, and what is the strongest supporting evidence for it?

The strongest current conclusion is selective clarification, not autonomous assumption and not blanket questioning. ClarifyGPT, a peer-reviewed FSE 2024 study, used code-consistency checks to decide whether to ask. On five coding benchmarks, its simulated-feedback version increased average Pass@1 from 62.43% to 69.60% for GPT-4 and from 54.32% to 62.37% for ChatGPT; authors explicitly found that asking on every requirement creates needless human interaction and can harm performance through off-topic questions. [doi.org](https://doi.org/10.1145/3660810)

Its human-feedback experiment on MBPP variants raised GPT-4 average Pass@1 from 61.24% to 70.50%, a relative improvement of 15.35%; the paper reports *p* = 4.3×10⁻⁴ for a 9.52-point MBPP-ET improvement. Ten annotators labelled 427 MBPP-sanitized requirements, with κ = .86; GPT-4-based ambiguity detection achieved precision 88.57%, recall 87.94%, and F1 88.25%. Limitations: curated programming benchmarks, a tiny human-evaluator group, and substantial simulated-user evaluation. [doi.org](https://doi.org/10.1145/3660810)

The broader LLM evidence cautions against trusting a model’s intuitive ambiguity judgement. Liu et al.’s peer-reviewed AmbiEnt benchmark contains 1,645 linguist-annotated examples; crowdworkers judged GPT-4’s generated disambiguations correct only 32% of the time, versus 90% for dataset disambiguations. [aclanthology.org](https://aclanthology.org/2023.emnlp-main.51/) CLAMBER’s approximately 12,000-example benchmark found ChatGPT ambiguity-classification accuracy of 54.25% and F1 of 52.77% in its reported setting, with under- and over-specified clarifying questions among prominent error types. [aclanthology.org](https://aclanthology.org/2024.acl-long.578.pdf)

### 3. What are the contrasting viewpoints or competing evidence?

<CONFLICTING_EVIDENCE>Choice overload is not a universal law. Scheibehenne et al. found a near-zero average effect across 63 conditions, whereas Chernev et al. found a significant conditional effect after modelling moderators. The disagreement is primarily about heterogeneity and moderators, not whether overload can occur.</CONFLICTING_EVIDENCE> [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002)

<CONFLICTING_EVIDENCE>Requirements ambiguity is not always a reason to interrupt. Ribeiro and Berry’s case studies suggest disciplined inspection/discussion can resolve persistent textual ambiguity without serious defects; Kamata and Tamai show a relationship between weak requirements context and overruns. The first concerns sampled wording ambiguities in mature processes; the second concerns project-level completeness and contextual quality. Neither warrants an automatic rule based on surface ambiguity alone.</CONFLICTING_EVIDENCE> [doi.org](https://doi.org/10.1016/j.scico.2020.102472) [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure)

<CONFLICTING_EVIDENCE>Plain wording reliably improves perceived clarity and missingness in the Chin–Bruine de Bruin experiment, but it changed at least one validity-related measure. Simplification should preserve the decision construct, not merely lower readability statistics.</CONFLICTING_EVIDENCE> [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/)

<CONFLICTING_EVIDENCE>Recommendations can reduce search effort when the recommender has better evidence, yet the same visible endorsement can anchor a user away from their own preference. The evidence supports recommendation for objective, auditable choices and neutrality for subjective choices; it does not support a universal “always recommend first” policy.</CONFLICTING_EVIDENCE> [doi.org](https://doi.org/10.1017/bpp.2018.43) [doi.org](https://doi.org/10.1287/isre.2013.0497)

### 4. What changed recently, and what is the trajectory?

Recent work has moved from generating a plausible clarifying question to evaluating the full policy: detect uncertainty, choose whether to ask, formulate a targeted question, incorporate the answer, and complete the task. ClarQ-LLM, a 2024 preprint, evaluates 31 task types × 10 English/Chinese scenarios with interactive provider agents. Its best reported seeker success was 60.05% for Llama 3.1 405B and 50.8% for GPT-4o, versus 85% for human seekers. It is a useful interactive benchmark, but the provider is itself an LLM and the work is a preprint. [arxiv.org](https://arxiv.org/abs/2409.06097)

The trajectory is toward uncertainty-aware, tool-grounded clarification policies rather than a prompt instruction that says “ask if ambiguous.” The evidence is promising for coding tasks, but user-burden, answer quality, preference preservation, and long-horizon coding outcomes remain under-measured. <INFERENCE from="ClarifyGPT (2024); CLAMBER (2024); ClarQ-LLM (2024)">A deployable coding-agent skill should log both false negatives (silent wrong assumptions) and false positives (unnecessary interruptions), then tune its gate against task outcome and user burden rather than question count alone.</INFERENCE> [doi.org](https://doi.org/10.1145/3660810) [aclanthology.org](https://aclanthology.org/2024.acl-long.578.pdf) [arxiv.org](https://arxiv.org/abs/2409.06097)

### Methodological Comparison

| Study | Method, sample, measures | Main result | Statistical reporting | Material limitation |
|---|---|---|---|---|
| Kamata & Tamai (2007) | Observational analysis of 32 completed Tokyo business-software projects; SRS-quality assessments linked to cost/schedule outcomes. | Poor SRS context/purpose with rich function detail associated with cost overrun. [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure) | Exact coefficients/*p* values not available in accessible record. | One division; association, not causal proof. |
| Ribeiro & Berry (2020) | Three post hoc requirements/specification case studies. | Sampled persistent ambiguity did not cause serious downstream defects. [doi.org](https://doi.org/10.1016/j.scico.2020.102472) | No pooled effect size. | May miss rare catastrophic cases; limited generalisability. |
| Lenzner et al. (2010) | Online experiment, *n* = 490; seven degraded text features; response time, dropout, satisficing. | At least six features reduced clarity. [doi.org](https://doi.org/10.1002/acp.1602) | Accessible abstract does not provide feature-specific *p* values. | Response time is a burden proxy; task/context limited. |
| Chin & Bruine de Bruin (2018) | Randomised survey experiment, *n* = 1,516; original versus simplified wording. | Skips 10.5%→4.3%, χ²(1)=20.29, *p*<.001; clarity and difficulty improved. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/) | Reports *t*(1403)=2.97, *p*=.003 and *t*(1403)=−2.18, *p*=.030. | Simplification changed one validity indicator; older online panel. |
| Menold (2020) | Two online-panel experiments, *n* = 497 and *n* = 435; DBQs versus split single-stimulus items. | Components differed significantly in 6/8 items. [doi.org](https://doi.org/10.2478/JOS-2020-0041) | Item-level tests; some validity differences *p*<.05; reliability differences nonsignificant. | German opinion inventories; cannot quantify all DBQ harms. |
| Scheibehenne et al. (2010) | Meta-analysis: 63 conditions, 50 experiments, *N*=5,036. | Mean overload effect virtually zero; high heterogeneity. [doi.org](https://doi.org/10.1086/651235) | Effect near zero; no sufficient conditions. | Published/unpublished mixture and heterogeneous outcomes. |
| Chernev et al. (2015) | Meta-analysis: 99 observations, *N*=7,202. | Conditional overload under complexity/difficulty/uncertainty/unfocused goal. [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) | Significant moderated overall effect; accessible record lacks full coefficient table. | Consumer-choice evidence, not expert engineering choices. |
| Jachimowicz et al. (2019) | Meta-analysis: 58 default studies, pooled *N*=73,675. | Default effect *d*=0.68, 95% CI [0.53, 0.83]. [doi.org](https://doi.org/10.1017/bpp.2018.43) | Several null and two negative studies. | Behavioural selection, not necessarily decision quality. |
| Mark et al. (2008) | Counterbalanced lab study, *n*=48; email task interrupted every two minutes. | Higher stress/workload despite faster completion. [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) | Stress *F*(2,92)=12.15, *p*<.001; workload *F*(2,92)=3.82, *p*<.03. | Mostly university students; simulated task. |
| Fitz et al. (2019) | Two-week randomised field study, *n*=237; notification schedules. | Three daily batches improved wellbeing/productivity reports; hourly did little; no alerts increased anxiety/FoMO. [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) | ANOVA; exact outcome effect values require article table. | MTurk smartphone users; self-report-heavy. |
| ClarifyGPT (2024) | Coding-agent evaluation over five benchmarks; 10-person annotation; human and simulated feedback. | GPT-4 average Pass@1 62.43%→69.60%; detection F1 88.25%. [doi.org](https://doi.org/10.1145/3660810) | One reported gain *p*=4.3×10⁻⁴; κ=.86. | Benchmarks and simulated users; no longitudinal product study. |
| Liu et al. (2023) | Linguist-annotated AmbiEnt benchmark, 1,645 examples; crowdworker evaluation. | GPT-4 disambiguations 32% correct versus 90% dataset disambiguations. [aclanthology.org](https://aclanthology.org/2023.emnlp-main.51/) | Percentage outcome; accessible record lacks CI. | Language ambiguity, not full agent workflow. |
| Gan et al. (2024) | Preprint interactive benchmark: 31 task types × 10 scenarios, bilingual LLM provider/seeker. | GPT-4o 50.8%, Llama 3.1 405B 60.5%, humans 85%. [arxiv.org](https://arxiv.org/abs/2409.06097) | Success rates; no CI reported in accessible record. | Preprint; simulated provider instead of real users. |

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Requirements context quality predicts project outcome in a 32-project industrial dataset. | Kamata & Tamai | 2007 | IEEE RE conference paper; primary industrial observational study. | [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure) |
| Persistent wording ambiguity may be resolved by normal RE practice. | Ribeiro & Berry | 2020 | Peer-reviewed case-study research. | [doi.org](https://doi.org/10.1016/j.scico.2020.102472) |
| Linguistic complexity raises survey-question burden. | Lenzner, Kaczmirek & Lenzner | 2010 | Peer-reviewed psycholinguistic experiment. | [doi.org](https://doi.org/10.1002/acp.1602) |
| Simplification reduced missing answers but may alter response validity. | Chin & Bruine de Bruin | 2018 | Peer-reviewed randomised survey experiments. | [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/) |
| Double-barrelled wording changes item meaning. | Menold | 2020 | Peer-reviewed controlled experiments in an official-statistics journal. | [doi.org](https://doi.org/10.2478/JOS-2020-0041) |
| Option-order shortcuts are a documented survey threat. | Krosnick & Alwin | 1987 | Peer-reviewed split-ballot survey experiment. | [doi.org](https://doi.org/10.1086/268907) |
| Choice overload is conditional, not a fixed option-count rule. | Scheibehenne, Greifeneder & Todd; Chernev et al. | 2010; 2015 | Peer-reviewed meta-analyses. | [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) |
| Defaults/endorsement exert a large pooled selection effect. | Jachimowicz et al. | 2019 | Peer-reviewed meta-analysis. | [doi.org](https://doi.org/10.1017/bpp.2018.43) |
| Recommendation ratings can anchor preferences. | Adomavicius et al. | 2013 | Peer-reviewed controlled laboratory experiments. | [doi.org](https://doi.org/10.1287/isre.2013.0497) |
| Interruptions increase subjective cost even if apparent throughput rises. | Mark, Gudith & Klocke | 2008 | Peer-reviewed CHI controlled experiment. | [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) |
| Predictable three-times-daily batching can improve reported wellbeing. | Fitz et al. | 2019 | Peer-reviewed randomised field experiment. | [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) |
| Selective code-requirements clarification improved benchmark code generation. | Mu et al., ClarifyGPT | 2024 | Peer-reviewed ACM FSE paper. | [doi.org](https://doi.org/10.1145/3660810) |
| Current LLMs remain weak at ambiguity resolution and clarification. | Liu et al.; Gan et al. | 2023; 2024 | Peer-reviewed EMNLP benchmark; clearly labelled preprint benchmark. | [aclanthology.org](https://aclanthology.org/2023.emnlp-main.51/) [arxiv.org](https://arxiv.org/abs/2409.06097) |

## Knowledge Gaps

- **Direct agent UX evidence:** <MISSING_DATA>Randomised studies of question-batch size, option count, recommendation placement, and optional notes in real coding-agent work were not found. Needed: preregistered field experiments measuring completion time, correction rate, user burden, and downstream rework.</MISSING_DATA>

- **Exact word thresholds:** <INSUFFICIENT_EVIDENCE>No defensible universal “maximum words per question” threshold was corroborated. Readability grade and single-decision wording have stronger support than raw word count.</INSUFFICIENT_EVIDENCE>

- **Free-text note value:** <MISSING_DATA>Evidence shows open-text burden and quality variation, but not whether an optional note beside a selected agent option improves implementation correctness. Needed: an A/B test with coding tasks and adjudicated requirement completeness.</MISSING_DATA>

- **Decision quality versus compliance:** <INSUFFICIENT_EVIDENCE>Default and recommendation studies robustly measure changed selections, but many do not establish that the selected option was better for that particular person.</INSUFFICIENT_EVIDENCE>

## Recommended Next Steps

1. Run a preregistered coding-agent field experiment comparing 1, 2–3, and 4-question batches, measuring time-to-answer, abandonment, correction/rework, and NASA-TLX burden. Rationale: this is the most consequential missing evidence.

2. Test recommendation placement: neutral options only; “Recommended” first; and recommendation after options with a one-sentence rationale. Rationale: default/anchoring effects are established, but the least-biasing agent presentation is not.

3. Test optional “Other / note” against no note, using expert-labelled completeness and downstream code correctness. Rationale: it resolves the key coverage-versus-burden uncertainty.

4. Implement the decision-divergence gate with logging: detected ambiguity, question asked, answer, default used, later reversal, rework, and user dismissal. Rationale: it permits calibration against actual false-positive and false-negative costs.

5. Add automated linting before every user question: one decision only, ≤25-word stem, grade ≤8 where possible, 2–4 parallel options, no preselected recommendation, and an escape hatch only where option coverage is uncertain.
tokens used
134,058
## Executive Summary

- (High Confidence) Ask only when the answer can change a material action and a safe, reversible default is unavailable. This is an expected-value rule, not a magic ambiguity score: clarify when the likely cost of a wrong build exceeds the interruption and delay cost. <INFERENCE from="Kamata & Tamai (2007) association between weak contextual requirements and overruns; Mark et al. (2008) measured interruption stress; ClarifyGPT (2024) finding that asking on every request burdens users">Use a clarification gate based on decision divergence, reversibility, and expected harm—not on whether wording merely seems vague.</INFERENCE> [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure) [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) [doi.org](https://doi.org/10.1145/3660810)

- (High Confidence) Use one concise decision at a time; batch only independent decisions, with a hard cap of three. Evidence supports reducing repeated interruptions, but does not establish “three questions” as an empirical optimum. The cap is a conservative operational rule: it limits working-memory demands while avoiding serial context switches. [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) <MISSING_DATA>Direct experiments comparing 1, 2, 3, and 4 clarification questions in coding-agent conversations were sought; none were located. A representative benchmark with real coding users and task outcomes is needed.</MISSING_DATA>

- (High Confidence) Offer 2–4 mutually exclusive, collectively useful options; target 3. There is no universal optimal count: choice overload is conditional on complexity, difficulty, uncertainty, and decision goal, while large menus sometimes help. [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002)

- (High Confidence) Do not lead with a marked recommendation for a preference-sensitive decision. A first, preselected, or visibly endorsed option is an anchor/default: defaults have a pooled effect of *d* = 0.68, 95% CI [0.53, 0.83]. State the recommendation after neutral options, label it as advice rather than a selection, and give one short reason. [doi.org](https://doi.org/10.1017/bpp.2018.43) [doi.org](https://doi.org/10.1287/isre.2013.0497)

- (High Confidence) Target one plain-language sentence of ≤25 words for the question stem, with options of ≤10 words; validate a Flesch–Kincaid grade of ≤8 where feasible. The grade-8 target is supported as a survey-design rule of thumb; the 25/10-word limits are deliberately conservative authoring defaults, not measured thresholds. [doi.org](https://doi.org/10.1177/1525822X221124469) [doi.org](https://doi.org/10.1002/acp.1602) <INFERENCE from="Lenzner et al. (2010) found six of seven linguistic complexity features impaired clarity; Chin & Bruine de Bruin (2018) improved experience by simplifying prompts">A short, single-clause cap is a practical way to avoid the measured linguistic sources of burden, while grade level is the testable quality criterion.</INFERENCE> [doi.org](https://doi.org/10.1002/acp.1602) [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/)

- (Medium Confidence) Add an optional “Other / none fits — add a brief note” escape hatch when the listed options may omit a consequential state. It prevents forced misclassification and can surface unknown constraints, but mandatory or prominent free text increases burden and its quality declines late in questionnaires. [doi.org](https://doi.org/10.12758/mda.2019.05) <MISSING_DATA>A randomized comparison of selected-option-plus-optional-note versus selected-option-only in agent clarification has not been located.</MISSING_DATA>

- (High Confidence) Bad questions create measurable error: double-barrelled items changed meaning in six of eight tested items; difficult wording increased skips from 4.3% to 10.5% in one randomized survey experiment; interruption can preserve apparent speed while increasing stress, workload, frustration, time pressure, and effort. [doi.org](https://doi.org/10.2478/JOS-2020-0041) [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/) [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf)

## Detailed Findings

### 1. What does the evidence say about how to ask a person a decision question well — so they answer accurately, quickly, and without decision fatigue — and what are the documented failure modes of asking badly?

**Recommended skill policy**

| Component | Operational rule | Evidence status |
|---|---|---|
| Ask-or-default gate | Ask only if two plausible answers produce materially different implementation, risk, cost, or irreversible action; otherwise state the low-regret assumption and proceed. | <INFERENCE from="requirements-quality evidence; interruption-cost evidence">Decision-theoretic synthesis; no calibrated universal threshold.</INFERENCE> |
| Questions per batch | Ask 1 by default; batch 2–3 only when answers are independent and all are needed before the same next action. Never batch 4+. | <INSUFFICIENT_EVIDENCE>No direct coding-agent experiment identifies an optimum. The cap is a conservative design rule supported indirectly by interruption and choice-load evidence.</INSUFFICIENT_EVIDENCE> |
| Options | Provide 2–4 options, normally 3; include “Other / none fits” when coverage is uncertain. | High confidence against large, complex menus; medium confidence for the exact 2–4 range. |
| Recommendation | For objective, evidence-dominated choices: provide an unselected “Recommended” label after the neutral list with one reason. For preference-sensitive choices: do not recommend first; either ask neutrally or offer a reversible default. | High confidence that recommendation/default placement anchors; medium confidence on the best presentation remedy. |
| Wording | One decision, one sentence, ≤25-word stem; plain words; define unavoidable technical terms; target grade ≤8; option labels ≤10 words. | High confidence for simplicity/readability; exact word caps are operational, not causal thresholds. |
| Free-text note | “Other / none fits — brief note (optional).” Do not require a rationale for a normal choice. | Medium confidence: improves coverage in principle, with an observed burden/quality trade-off. |
| Serial follow-ups | Ask the next question only if it depends on the prior answer or a new decision-critical uncertainty appears. | High confidence as a consequence of interruption costs; direct agent evidence remains limited. |

**A usable question template**

> **Which deployment target should I use?**  
> A. Staging only  
> B. Production with approval  
> C. Production automatically  
> Other / none fits — brief note *(optional)*  
>
> Recommendation: **B**, because it preserves a human release check.

This format does not preselect B. It makes the recommendation inspectable rather than silently converting advice into a default. <INFERENCE from="Jachimowicz et al. (2019) default effects; Adomavicius et al. (2013) recommendation anchoring">Separating the selection control from the recommendation reduces, but cannot eliminate, endorsement/anchoring effects.</INFERENCE> [doi.org](https://doi.org/10.1017/bpp.2018.43) [doi.org](https://doi.org/10.1287/isre.2013.0497)

**Requirements elicitation and wrong-build cost.** Kamata and Tamai examined 32 completed business-application projects in one Tokyo development division, linking SRS-quality assessments to cost and schedule outcomes. Projects with weak context/purpose/overview material and richer functional detail tended toward cost overrun. This is strong evidence that omission of the “why/what context” can matter; it is observational, single-organisation evidence and does not yield a portable percentage cost penalty. [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure)

A 2015 systematic mapping review found 174 ambiguity-related requirements studies published from 1995–2015, but only 28 empirically evaluated studies. The review supports treating ambiguity as a real engineering concern, while also showing that tool-performance and cost-effectiveness claims are much less mature than conventional advice implies. [doi.org](https://doi.org/10.1109/EmpiRE.2015.7431303)

There is meaningful contrary evidence. Ribeiro and Berry’s three case studies, following two earlier studies, found that sampled persistent ambiguities in mature specifications did not cause serious downstream defects, apparently because normal inspections and discussions resolved them. This does not justify “never ask”: it means linguistic ambiguity alone is a poor gate. Ask when ambiguity implies divergent implementation, not merely when a word has multiple readings. The studies are case-based and may miss rare high-severity ambiguities. [doi.org](https://doi.org/10.1016/j.scico.2020.102472)

**Authoring rule.** <INFERENCE from="Kamata & Tamai (2007); Ribeiro & Berry (2020)">Do not ask “What do you mean?” for every ambiguity. Ask a concrete discriminating question only when each plausible interpretation yields a different artefact, interface, data model, safety/compliance outcome, or non-trivial rework path.</INFERENCE> [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure) [doi.org](https://doi.org/10.1016/j.scico.2020.102472)

**Survey wording, verbosity, jargon, and double-barrelling.** Lenzner, Kaczmirek, and Lenzner’s online psycholinguistic experiment compared well-written and degraded questions in one group of 490 respondents. Response time indexed burden; dropout and satisficing indexed quality. At least six of seven text features—including low-frequency words and difficult syntax—impaired question clarity. The study supports simple vocabulary and syntax, but does not establish a universal word count or prove that short questions are always more valid. [doi.org](https://doi.org/10.1002/acp.1602)

Chin and Bruine de Bruin randomly assigned 1,516 older US internet-panel respondents to an original or simplified stock-expectations question. Simplification reduced Flesch–Kincaid grade from 13.5 to 4.5, nonresponse from 10.5% to 4.3%, increased clarity from 5.8 to 6.0 on a seven-point scale, and reduced reported difficulty from 3.0 to 2.8; all reported tests were statistically significant (*p* ≤ .030). But simplification also reduced one self-reported confidence measure, and a second experiment found altered expectation estimates. Plain language improves completion and subjective comprehension; it can also change the construct respondents infer. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/)

Menold’s two controlled German online-panel experiments tested double-barrelled versus single-stimulus items: *N* = 497 and *N* = 435. Six of eight items yielded significant mean differences when their components were answered separately. Reliability differences were not significant, and validity did not uniformly favour either split component. The failure mode is therefore not simply “lower reliability”; it is uninterpretable meaning because respondents may weight one component, both, or neither. [doi.org](https://doi.org/10.2478/JOS-2020-0041)

**Authoring rule.** Ask exactly one decision per question. Treat “and,” “or,” combined objectives, and compound constraints as a defect trigger when a person could reasonably choose different answers to their parts. [doi.org](https://doi.org/10.2478/JOS-2020-0041)

**Satisficing and response order.** Krosnick’s satisficing framework predicts that cognitive demand encourages shortcuts: choosing the first plausible option, agreeing, selecting status quo, giving “don’t know,” straight-lining, or random selection. It is a foundational theory and literature review rather than one new effect-size experiment. [doi.org](https://doi.org/10.1002/acp.2350050305) Krosnick and Alwin’s split-ballot 1984 General Social Survey experiment documented response-order effects and predicted primacy effects particularly among less cognitively sophisticated respondents. [doi.org](https://doi.org/10.1086/268907)

**Authoring rule.** Keep options parallel in wording and length. Do not put the recommended option first for preference-sensitive choices. If ordering itself has no meaning, randomise it where the interface permits; if the agent must recommend, place advice outside the option order. <INFERENCE from="Krosnick & Alwin (1987); Jachimowicz et al. (2019)">This separates response-order bias from endorsement/default bias better than a marked first option.</INFERENCE> [doi.org](https://doi.org/10.1086/268907) [doi.org](https://doi.org/10.1017/bpp.2018.43)

**Choice architecture, number of options, and recommendations.** Scheibehenne, Greifeneder, and Todd meta-analysed 63 conditions from 50 published and unpublished experiments (*N* = 5,036) and found an average choice-overload effect near zero, with substantial heterogeneity and no sufficient condition. Chernev, Böckenholt, and Goodman’s later meta-analysis of 99 observations (*N* = 7,202) found overload after accounting for moderators: complex sets, difficult tasks, uncertain preferences, and an unfocused decision goal were especially risky. Neither meta-analysis identifies a universal optimal count. [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002)

Jachimowicz, Duncan, Weber, and Johnson’s meta-analysis included 58 default studies, pooled *N* = 73,675, and estimated *d* = 0.68, 95% CI [0.53, 0.83]. Effects varied substantially; some studies were null and two negative. Defaults work particularly when they signal endorsement or the status quo—which is precisely why a “Recommended” first option can distort an answer meant to reveal the user’s preference. [doi.org](https://doi.org/10.1017/bpp.2018.43) Adomavicius et al.’s three controlled laboratory studies found that recommender-system ratings anchored ratings of television programs, including a continuous effect across rating perturbations. These were consumer-rating tasks, so transfer to expert software decisions is plausible but not proven. [doi.org](https://doi.org/10.1287/isre.2013.0497)

**Authoring rule.** <INFERENCE from="choice-overload meta-analyses; default-effect meta-analysis">Three options is a good target, not a discovered optimum: it keeps the set small while retaining a meaningful alternative; use four only when omitting one would distort the decision, and split or sequence the decision above four.</INFERENCE> [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) [doi.org](https://doi.org/10.1017/bpp.2018.43)

**Free-text escape hatch.** Schmidt, Gummer, and Roßmann analysed open-ended attitude responses from 29 web surveys. Higher education and motivation predicted better response quality; placing the question later predicted fewer interpretable responses. The design supports a narrow optional note, especially for exceptional constraints, rather than demanding explanations from everyone. It does not test a selected-option-plus-note design, nor does it establish that free text improves final engineering outcomes. [doi.org](https://doi.org/10.12758/mda.2019.05)

**Interruption and batching.** Mark, Gudith, and Klocke conducted a counterbalanced 3×2 laboratory study with 48 participants on email work, comparing no interruption, same-context interruption, and different-context interruption every two minutes. Interrupted participants completed tasks faster but wrote shorter emails; errors were not significantly different. NASA-TLX workload, stress, frustration, time pressure, and effort were significantly higher under interruptions—for example, stress differed by condition, *F*(2,92) = 12.15, *p* < .001. The task was a simulated office task, mostly students, so do not use its time result as proof that interruption improves work. [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf)

Fitz et al.’s two-week randomised field experiment assigned 237 MTurk smartphone users to ordinary notifications, hourly batches, three daily batches, or none. Three daily batches—but not hourly batches—improved reported attention, productivity, mood, and control; disabling alerts increased anxiety/FoMO. This supports batching independent interruptions, but notification wellbeing is not directly equivalent to multi-question agent dialogue. [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) A 2025 web-probing experiment found that delayed retrospective probes required more time to recapitulate the original survey question and produced less interpretable content for one of three probes. Therefore, batch independent questions, but do not defer a question whose answer depends on fresh task context. [doaj.org](https://doaj.org/article/2d52a9f82a2747129cd2dacbce4fa30c)

**Authoring rule.** <INFERENCE from="Mark et al. (2008); Fitz et al. (2019); Hadler (2025)">Batch up to three independent, immediately needed decisions at a natural pause. Ask dependent or context-perishable questions serially and immediately after their prerequisite.</INFERENCE> [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) [doaj.org](https://doaj.org/article/2d52a9f82a2747129cd2dacbce4fa30c)

### 2. What is the current state, and what is the strongest supporting evidence for it?

The strongest current conclusion is selective clarification, not autonomous assumption and not blanket questioning. ClarifyGPT, a peer-reviewed FSE 2024 study, used code-consistency checks to decide whether to ask. On five coding benchmarks, its simulated-feedback version increased average Pass@1 from 62.43% to 69.60% for GPT-4 and from 54.32% to 62.37% for ChatGPT; authors explicitly found that asking on every requirement creates needless human interaction and can harm performance through off-topic questions. [doi.org](https://doi.org/10.1145/3660810)

Its human-feedback experiment on MBPP variants raised GPT-4 average Pass@1 from 61.24% to 70.50%, a relative improvement of 15.35%; the paper reports *p* = 4.3×10⁻⁴ for a 9.52-point MBPP-ET improvement. Ten annotators labelled 427 MBPP-sanitized requirements, with κ = .86; GPT-4-based ambiguity detection achieved precision 88.57%, recall 87.94%, and F1 88.25%. Limitations: curated programming benchmarks, a tiny human-evaluator group, and substantial simulated-user evaluation. [doi.org](https://doi.org/10.1145/3660810)

The broader LLM evidence cautions against trusting a model’s intuitive ambiguity judgement. Liu et al.’s peer-reviewed AmbiEnt benchmark contains 1,645 linguist-annotated examples; crowdworkers judged GPT-4’s generated disambiguations correct only 32% of the time, versus 90% for dataset disambiguations. [aclanthology.org](https://aclanthology.org/2023.emnlp-main.51/) CLAMBER’s approximately 12,000-example benchmark found ChatGPT ambiguity-classification accuracy of 54.25% and F1 of 52.77% in its reported setting, with under- and over-specified clarifying questions among prominent error types. [aclanthology.org](https://aclanthology.org/2024.acl-long.578.pdf)

### 3. What are the contrasting viewpoints or competing evidence?

<CONFLICTING_EVIDENCE>Choice overload is not a universal law. Scheibehenne et al. found a near-zero average effect across 63 conditions, whereas Chernev et al. found a significant conditional effect after modelling moderators. The disagreement is primarily about heterogeneity and moderators, not whether overload can occur.</CONFLICTING_EVIDENCE> [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002)

<CONFLICTING_EVIDENCE>Requirements ambiguity is not always a reason to interrupt. Ribeiro and Berry’s case studies suggest disciplined inspection/discussion can resolve persistent textual ambiguity without serious defects; Kamata and Tamai show a relationship between weak requirements context and overruns. The first concerns sampled wording ambiguities in mature processes; the second concerns project-level completeness and contextual quality. Neither warrants an automatic rule based on surface ambiguity alone.</CONFLICTING_EVIDENCE> [doi.org](https://doi.org/10.1016/j.scico.2020.102472) [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure)

<CONFLICTING_EVIDENCE>Plain wording reliably improves perceived clarity and missingness in the Chin–Bruine de Bruin experiment, but it changed at least one validity-related measure. Simplification should preserve the decision construct, not merely lower readability statistics.</CONFLICTING_EVIDENCE> [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/)

<CONFLICTING_EVIDENCE>Recommendations can reduce search effort when the recommender has better evidence, yet the same visible endorsement can anchor a user away from their own preference. The evidence supports recommendation for objective, auditable choices and neutrality for subjective choices; it does not support a universal “always recommend first” policy.</CONFLICTING_EVIDENCE> [doi.org](https://doi.org/10.1017/bpp.2018.43) [doi.org](https://doi.org/10.1287/isre.2013.0497)

### 4. What changed recently, and what is the trajectory?

Recent work has moved from generating a plausible clarifying question to evaluating the full policy: detect uncertainty, choose whether to ask, formulate a targeted question, incorporate the answer, and complete the task. ClarQ-LLM, a 2024 preprint, evaluates 31 task types × 10 English/Chinese scenarios with interactive provider agents. Its best reported seeker success was 60.05% for Llama 3.1 405B and 50.8% for GPT-4o, versus 85% for human seekers. It is a useful interactive benchmark, but the provider is itself an LLM and the work is a preprint. [arxiv.org](https://arxiv.org/abs/2409.06097)

The trajectory is toward uncertainty-aware, tool-grounded clarification policies rather than a prompt instruction that says “ask if ambiguous.” The evidence is promising for coding tasks, but user-burden, answer quality, preference preservation, and long-horizon coding outcomes remain under-measured. <INFERENCE from="ClarifyGPT (2024); CLAMBER (2024); ClarQ-LLM (2024)">A deployable coding-agent skill should log both false negatives (silent wrong assumptions) and false positives (unnecessary interruptions), then tune its gate against task outcome and user burden rather than question count alone.</INFERENCE> [doi.org](https://doi.org/10.1145/3660810) [aclanthology.org](https://aclanthology.org/2024.acl-long.578.pdf) [arxiv.org](https://arxiv.org/abs/2409.06097)

### Methodological Comparison

| Study | Method, sample, measures | Main result | Statistical reporting | Material limitation |
|---|---|---|---|---|
| Kamata & Tamai (2007) | Observational analysis of 32 completed Tokyo business-software projects; SRS-quality assessments linked to cost/schedule outcomes. | Poor SRS context/purpose with rich function detail associated with cost overrun. [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure) | Exact coefficients/*p* values not available in accessible record. | One division; association, not causal proof. |
| Ribeiro & Berry (2020) | Three post hoc requirements/specification case studies. | Sampled persistent ambiguity did not cause serious downstream defects. [doi.org](https://doi.org/10.1016/j.scico.2020.102472) | No pooled effect size. | May miss rare catastrophic cases; limited generalisability. |
| Lenzner et al. (2010) | Online experiment, *n* = 490; seven degraded text features; response time, dropout, satisficing. | At least six features reduced clarity. [doi.org](https://doi.org/10.1002/acp.1602) | Accessible abstract does not provide feature-specific *p* values. | Response time is a burden proxy; task/context limited. |
| Chin & Bruine de Bruin (2018) | Randomised survey experiment, *n* = 1,516; original versus simplified wording. | Skips 10.5%→4.3%, χ²(1)=20.29, *p*<.001; clarity and difficulty improved. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/) | Reports *t*(1403)=2.97, *p*=.003 and *t*(1403)=−2.18, *p*=.030. | Simplification changed one validity indicator; older online panel. |
| Menold (2020) | Two online-panel experiments, *n* = 497 and *n* = 435; DBQs versus split single-stimulus items. | Components differed significantly in 6/8 items. [doi.org](https://doi.org/10.2478/JOS-2020-0041) | Item-level tests; some validity differences *p*<.05; reliability differences nonsignificant. | German opinion inventories; cannot quantify all DBQ harms. |
| Scheibehenne et al. (2010) | Meta-analysis: 63 conditions, 50 experiments, *N*=5,036. | Mean overload effect virtually zero; high heterogeneity. [doi.org](https://doi.org/10.1086/651235) | Effect near zero; no sufficient conditions. | Published/unpublished mixture and heterogeneous outcomes. |
| Chernev et al. (2015) | Meta-analysis: 99 observations, *N*=7,202. | Conditional overload under complexity/difficulty/uncertainty/unfocused goal. [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) | Significant moderated overall effect; accessible record lacks full coefficient table. | Consumer-choice evidence, not expert engineering choices. |
| Jachimowicz et al. (2019) | Meta-analysis: 58 default studies, pooled *N*=73,675. | Default effect *d*=0.68, 95% CI [0.53, 0.83]. [doi.org](https://doi.org/10.1017/bpp.2018.43) | Several null and two negative studies. | Behavioural selection, not necessarily decision quality. |
| Mark et al. (2008) | Counterbalanced lab study, *n*=48; email task interrupted every two minutes. | Higher stress/workload despite faster completion. [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) | Stress *F*(2,92)=12.15, *p*<.001; workload *F*(2,92)=3.82, *p*<.03. | Mostly university students; simulated task. |
| Fitz et al. (2019) | Two-week randomised field study, *n*=237; notification schedules. | Three daily batches improved wellbeing/productivity reports; hourly did little; no alerts increased anxiety/FoMO. [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) | ANOVA; exact outcome effect values require article table. | MTurk smartphone users; self-report-heavy. |
| ClarifyGPT (2024) | Coding-agent evaluation over five benchmarks; 10-person annotation; human and simulated feedback. | GPT-4 average Pass@1 62.43%→69.60%; detection F1 88.25%. [doi.org](https://doi.org/10.1145/3660810) | One reported gain *p*=4.3×10⁻⁴; κ=.86. | Benchmarks and simulated users; no longitudinal product study. |
| Liu et al. (2023) | Linguist-annotated AmbiEnt benchmark, 1,645 examples; crowdworker evaluation. | GPT-4 disambiguations 32% correct versus 90% dataset disambiguations. [aclanthology.org](https://aclanthology.org/2023.emnlp-main.51/) | Percentage outcome; accessible record lacks CI. | Language ambiguity, not full agent workflow. |
| Gan et al. (2024) | Preprint interactive benchmark: 31 task types × 10 scenarios, bilingual LLM provider/seeker. | GPT-4o 50.8%, Llama 3.1 405B 60.5%, humans 85%. [arxiv.org](https://arxiv.org/abs/2409.06097) | Success rates; no CI reported in accessible record. | Preprint; simulated provider instead of real users. |

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Requirements context quality predicts project outcome in a 32-project industrial dataset. | Kamata & Tamai | 2007 | IEEE RE conference paper; primary industrial observational study. | [research.ibm.com](https://research.ibm.com/publications/how-does-requirements-quality-relate-to-project-success-or-failure) |
| Persistent wording ambiguity may be resolved by normal RE practice. | Ribeiro & Berry | 2020 | Peer-reviewed case-study research. | [doi.org](https://doi.org/10.1016/j.scico.2020.102472) |
| Linguistic complexity raises survey-question burden. | Lenzner, Kaczmirek & Lenzner | 2010 | Peer-reviewed psycholinguistic experiment. | [doi.org](https://doi.org/10.1002/acp.1602) |
| Simplification reduced missing answers but may alter response validity. | Chin & Bruine de Bruin | 2018 | Peer-reviewed randomised survey experiments. | [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/id/eprint/104232/) |
| Double-barrelled wording changes item meaning. | Menold | 2020 | Peer-reviewed controlled experiments in an official-statistics journal. | [doi.org](https://doi.org/10.2478/JOS-2020-0041) |
| Option-order shortcuts are a documented survey threat. | Krosnick & Alwin | 1987 | Peer-reviewed split-ballot survey experiment. | [doi.org](https://doi.org/10.1086/268907) |
| Choice overload is conditional, not a fixed option-count rule. | Scheibehenne, Greifeneder & Todd; Chernev et al. | 2010; 2015 | Peer-reviewed meta-analyses. | [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) |
| Defaults/endorsement exert a large pooled selection effect. | Jachimowicz et al. | 2019 | Peer-reviewed meta-analysis. | [doi.org](https://doi.org/10.1017/bpp.2018.43) |
| Recommendation ratings can anchor preferences. | Adomavicius et al. | 2013 | Peer-reviewed controlled laboratory experiments. | [doi.org](https://doi.org/10.1287/isre.2013.0497) |
| Interruptions increase subjective cost even if apparent throughput rises. | Mark, Gudith & Klocke | 2008 | Peer-reviewed CHI controlled experiment. | [ics.uci.edu](https://www.ics.uci.edu/~gmark/chi08-mark.pdf) |
| Predictable three-times-daily batching can improve reported wellbeing. | Fitz et al. | 2019 | Peer-reviewed randomised field experiment. | [doi.org](https://doi.org/10.1016/j.chb.2019.07.016) |
| Selective code-requirements clarification improved benchmark code generation. | Mu et al., ClarifyGPT | 2024 | Peer-reviewed ACM FSE paper. | [doi.org](https://doi.org/10.1145/3660810) |
| Current LLMs remain weak at ambiguity resolution and clarification. | Liu et al.; Gan et al. | 2023; 2024 | Peer-reviewed EMNLP benchmark; clearly labelled preprint benchmark. | [aclanthology.org](https://aclanthology.org/2023.emnlp-main.51/) [arxiv.org](https://arxiv.org/abs/2409.06097) |

## Knowledge Gaps

- **Direct agent UX evidence:** <MISSING_DATA>Randomised studies of question-batch size, option count, recommendation placement, and optional notes in real coding-agent work were not found. Needed: preregistered field experiments measuring completion time, correction rate, user burden, and downstream rework.</MISSING_DATA>

- **Exact word thresholds:** <INSUFFICIENT_EVIDENCE>No defensible universal “maximum words per question” threshold was corroborated. Readability grade and single-decision wording have stronger support than raw word count.</INSUFFICIENT_EVIDENCE>

- **Free-text note value:** <MISSING_DATA>Evidence shows open-text burden and quality variation, but not whether an optional note beside a selected agent option improves implementation correctness. Needed: an A/B test with coding tasks and adjudicated requirement completeness.</MISSING_DATA>

- **Decision quality versus compliance:** <INSUFFICIENT_EVIDENCE>Default and recommendation studies robustly measure changed selections, but many do not establish that the selected option was better for that particular person.</INSUFFICIENT_EVIDENCE>

## Recommended Next Steps

1. Run a preregistered coding-agent field experiment comparing 1, 2–3, and 4-question batches, measuring time-to-answer, abandonment, correction/rework, and NASA-TLX burden. Rationale: this is the most consequential missing evidence.

2. Test recommendation placement: neutral options only; “Recommended” first; and recommendation after options with a one-sentence rationale. Rationale: default/anchoring effects are established, but the least-biasing agent presentation is not.

3. Test optional “Other / note” against no note, using expert-labelled completeness and downstream code correctness. Rationale: it resolves the key coverage-versus-burden uncertainty.

4. Implement the decision-divergence gate with logging: detected ambiguity, question asked, answer, default used, later reversal, rework, and user dismissal. Rationale: it permits calibration against actual false-positive and false-negative costs.

5. Add automated linting before every user question: one decision only, ≤25-word stem, grade ≤8 where possible, 2–4 parallel options, no preselected recommendation, and an escape hatch only where option coverage is uncertain.
