---
title: "Designing HTML Status and Decision Documents for Non-Technical Owners"
run_id: dr_0fa01080b4467438
question: "How should a status-and-decision document be designed so that a single non-technical owner can, in one sitting, understand what remains before a software project is complete and settle every decision that is blocking the work? Cover, with evidence and measured results where they exist: (1) how practitioners today communicate remaining work and project state to a non-technical decision-maker — the formats that measurably improve comprehension and decision speed, and the documented failure modes of status reporting (status flattering / watermelon reporting, optimism and planning-fallacy bias, \"90% done\" syndrome, ambiguity about what is genuinely deployed versus merely built); (2) decision-elicitation and questionnaire design for a single expert respondent rather than a survey population — the measured effects of pre-selected defaults and pre-filled recommendations on answer quality and anchoring, when a default improves versus degrades the decision, optional free-text notes and non-response, satisficing, question ordering and batching, and how to distinguish an actively-confirmed answer from one merely left as found; (3) how blocking dependencies and critical path are best surfaced to a non-specialist — showing what a single decision unblocks, sequencing by cheapest-high-payoff, and evidence on whether ranked or grouped presentation produces better decisions; (4) asynchronous decision instruments in place of meetings — what evidence exists on decision latency, quality, and completion rates for written decision briefs, RFC/ADR-style decision records, and self-serve decision forms; (5) machine-readable round-trip of human decisions — schema design for capturing an answer plus its provenance, confidence and free-text caveats so an automated agent can act on it safely, and the documented failure modes of agents acting on human answers (over-reading a terse answer, ignoring an attached caveat, treating a default as a decision); (6) failure modes and integrity of AI-generated project status artefacts specifically — fabricated or unverifiable completeness claims, provenance and citation practices, and what is known about how readers calibrate trust in machine-written status reports; and (7) accessibility, print and self-containment constraints for a single-file HTML document used as a durable decision record. Exclude general agile ceremony advocacy, vendor project-management tool marketing, and large-population survey methodology that does not transfer to a single respondent."
provider: local-codex
model: Codex CLI
tier: max
archetype: technical
sources: 34
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 0.00
completed: 2026-08-12T08:14:32.277Z
---
Reading additional input from stdin...
OpenAI Codex v0.146.0
--------
workdir: /Users/lukerhodes/Dev/fledgeling-plugins
model: gpt-5.6-luna
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: xhigh
reasoning summaries: none
session id: 019ff4fd-cd67-79b1-b7c2-9193d7062db0
--------
user
<role>
You are a senior research analyst evaluating software stacks, infrastructure, APIs, or model architectures. Your output will directly Building a tool that generates ONE self-contained HTML page: a plain-English remaining-work report for a project's non-technical owner, plus an embedded decision questionnaire covering everything blocked on them, with pre-selected recommendations, multi-select, optional notes, and a JSON export an agent reads back and acts on. Need defensible rules for: whether to pre-select recommendations, marking confirmed-versus-default, linking a blocked item to the decision that releases it, ordering and grouping, honesty guarantees, and what the export schema must record for acting on it to be safe..
</role>

<context>
This investigation supports a concrete decision. Keep this context tight, context bloat degrades long-running agentic output; domain knowledge belongs in the analysis lens below.
</context>

<core_directive>
Answer this decisively: How should a status-and-decision document be designed so that a single non-technical owner can, in one sitting, understand what remains before a software project is complete and settle every decision that is blocking the work? Cover, with evidence and measured results where they exist: (1) how practitioners today communicate remaining work and project state to a non-technical decision-maker — the formats that measurably improve comprehension and decision speed, and the documented failure modes of status reporting (status flattering / watermelon reporting, optimism and planning-fallacy bias, "90% done" syndrome, ambiguity about what is genuinely deployed versus merely built); (2) decision-elicitation and questionnaire design for a single expert respondent rather than a survey population — the measured effects of pre-selected defaults and pre-filled recommendations on answer quality and anchoring, when a default improves versus degrades the decision, optional free-text notes and non-response, satisficing, question ordering and batching, and how to distinguish an actively-confirmed answer from one merely left as found; (3) how blocking dependencies and critical path are best surfaced to a non-specialist — showing what a single decision unblocks, sequencing by cheapest-high-payoff, and evidence on whether ranked or grouped presentation produces better decisions; (4) asynchronous decision instruments in place of meetings — what evidence exists on decision latency, quality, and completion rates for written decision briefs, RFC/ADR-style decision records, and self-serve decision forms; (5) machine-readable round-trip of human decisions — schema design for capturing an answer plus its provenance, confidence and free-text caveats so an automated agent can act on it safely, and the documented failure modes of agents acting on human answers (over-reading a terse answer, ignoring an attached caveat, treating a default as a decision); (6) failure modes and integrity of AI-generated project status artefacts specifically — fabricated or unverifiable completeness claims, provenance and citation practices, and what is known about how readers calibrate trust in machine-written status reports; and (7) accessibility, print and self-containment constraints for a single-file HTML document used as a durable decision record. Exclude general agile ceremony advocacy, vendor project-management tool marketing, and large-population survey methodology that does not transfer to a single respondent.
</core_directive>

<research_questions>
Primary:
1. Answer this decisively: How should a status-and-decision document be designed so that a single non-technical owner can, in one sitting, understand what remains before a software project is complete and settle every decision that is blocking the work? Cover, with evidence and measured results where they exist: (1) how practitioners today communicate remaining work and project state to a non-technical decision-maker — the formats that measurably improve comprehension and decision speed, and the documented failure modes of status reporting (status flattering / watermelon reporting, optimism and planning-fallacy bias, "90% done" syndrome, ambiguity about what is genuinely deployed versus merely built); (2) decision-elicitation and questionnaire design for a single expert respondent rather than a survey population — the measured effects of pre-selected defaults and pre-filled recommendations on answer quality and anchoring, when a default improves versus degrades the decision, optional free-text notes and non-response, satisficing, question ordering and batching, and how to distinguish an actively-confirmed answer from one merely left as found; (3) how blocking dependencies and critical path are best surfaced to a non-specialist — showing what a single decision unblocks, sequencing by cheapest-high-payoff, and evidence on whether ranked or grouped presentation produces better decisions; (4) asynchronous decision instruments in place of meetings — what evidence exists on decision latency, quality, and completion rates for written decision briefs, RFC/ADR-style decision records, and self-serve decision forms; (5) machine-readable round-trip of human decisions — schema design for capturing an answer plus its provenance, confidence and free-text caveats so an automated agent can act on it safely, and the documented failure modes of agents acting on human answers (over-reading a terse answer, ignoring an attached caveat, treating a default as a decision); (6) failure modes and integrity of AI-generated project status artefacts specifically — fabricated or unverifiable completeness claims, provenance and citation practices, and what is known about how readers calibrate trust in machine-written status reports; and (7) accessibility, print and self-containment constraints for a single-file HTML document used as a durable decision record. Exclude general agile ceremony advocacy, vendor project-management tool marketing, and large-population survey methodology that does not transfer to a single respondent.

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
- Agile ceremony advocacy
- PM tool vendor marketing
- Large-population survey sampling methodology
</exclude>
<time_horizon>
2015 to present, weighted to the last five years
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
- Contested findings: where evidence on defaults, recommendations and anchoring disagrees
- Convert each finding into a concrete design rule or an explicitly discarded option
- Documented failure modes of doing this by hand today
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
Answer this decisively: How should a status-and-decision document be designed so that a single non-technical owner can, in one sitting, understand what remains before a software project is complete and settle every decision that is blocking the work? Cover, with evidence and measured results where they exist: (1) how practitioners today communicate remaining work and project state to a non-technical decision-maker — the formats that measurably improve comprehension and decision speed, and the documented failure modes of status reporting (status flattering / watermelon reporting, optimism and planning-fallacy bias, "90% done" syndrome, ambiguity about what is genuinely deployed versus merely built); (2) decision-elicitation and questionnaire design for a single expert respondent rather than a survey population — the measured effects of pre-selected defaults and pre-filled recommendations on answer quality and anchoring, when a default improves versus degrades the decision, optional free-text notes and non-response, satisficing, question ordering and batching, and how to distinguish an actively-confirmed answer from one merely left as found; (3) how blocking dependencies and critical path are best surfaced to a non-specialist — showing what a single decision unblocks, sequencing by cheapest-high-payoff, and evidence on whether ranked or grouped presentation produces better decisions; (4) asynchronous decision instruments in place of meetings — what evidence exists on decision latency, quality, and completion rates for written decision briefs, RFC/ADR-style decision records, and self-serve decision forms; (5) machine-readable round-trip of human decisions — schema design for capturing an answer plus its provenance, confidence and free-text caveats so an automated agent can act on it safely, and the documented failure modes of agents acting on human answers (over-reading a terse answer, ignoring an attached caveat, treating a default as a decision); (6) failure modes and integrity of AI-generated project status artefacts specifically — fabricated or unverifiable completeness claims, provenance and citation practices, and what is known about how readers calibrate trust in machine-written status reports; and (7) accessibility, print and self-containment constraints for a single-file HTML document used as a durable decision record. Exclude general agile ceremony advocacy, vendor project-management tool marketing, and large-population survey methodology that does not transfer to a single respondent.
</core_directive>
warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
codex
I’m treating this as an evidence review for a concrete document design, not a generic project-management overview. I’ll prioritize peer-reviewed research, standards, and primary engineering/AI sources; where the evidence does not directly transfer from populations to one owner, I’ll label the design rule as an inference.
  → Collect primary evidence on status reporting, decision aids, dependencies, async decisions, AI integrity, and accessibility
  • Synthesize findings into explicit design rules and safety schema
  • Draft exact-format report with inline citations, evidence table, gaps, and next steps
  • Check citation coverage, confidence labels, and unresolved evidence conflicts
web search: 
web search: peer reviewed software project status reporting watermelon effect red amber green status optimism 90% complete syndrome ...
web search: 
web search: peer reviewed asynchronous decision making written brief decision latency meeting replacement experiment software teams ...
2026-08-12T08:02:19.299857Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: meta-analysis default effects preselected options decision quality anchoring 2015 2024 peer reviewed ...
2026-08-12T08:02:24.738335Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: pre-filled recommendations decision aid anchoring recommendation quality randomized experiment software configuration ...
2026-08-12T08:02:30.773902Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: software dependencies visualization critical path nontechnical stakeholders decision prioritization empirical study ...
2026-08-12T08:02:37.685771Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: decision prioritization value of information cost effort decision analysis empirical study expected value of information ...
2026-08-12T08:02:43.739511Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: W3C PROV data model provenance entities activities agents recommendation decision record ...
2026-08-12T08:02:50.354820Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: benchmark LLM agents instruction following constraints tool use safety ambiguous user requests 2024 paper ...
2026-08-12T08:02:59.492931Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: AI generated project status report hallucination completeness claims provenance citations trust calibration readers empirical study ...
2026-08-12T08:03:04.938794Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-12T08:03:10.009835Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: W3C WCAG 2.2 contrast minimum 4.5 3.0 keyboard accessible forms labels official ...
2026-08-12T08:03:16.944158Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: W3C CSS media queries print official recommendation @media print ...
2026-08-12T08:03:22.952263Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-12T08:03:32.242201Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: watermelon effect project status reporting red amber green peer reviewed source ...
2026-08-12T08:03:37.782168Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: official documentation continuous delivery deployment distinction software built deployed release candidate ...
2026-08-12T08:03:48.719679Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: meta-analysis asynchronous versus face-to-face group decision quality time communication 2015 2024 ...
2026-08-12T08:03:56.084040Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: empirical study architecture decision records practitioners adoption documentation software architecture decisions 2019 2024 ...
2026-08-12T08:04:02.458523Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: explicit confirmation versus default left unchanged user interface accidental decisions empirical study confirmation dialog ...
2026-08-12T08:04:09.867410Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-12T08:04:29.802472Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 'd = 0.68'
2026-08-12T08:04:35.662299Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-12T08:04:41.544271Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: "Assessing the effect of questionnaire design on unit and item-nonresponse" results percentage mandatory skip allowed ...
web search: 
web search: "The power of rank information" study results top ranked overlook options 2021 journal ...
web search: 
web search: 
web search: 
web search: 
web search: 
web search: 2020 2021 2022 empirical asynchronous decision making software team written communication decision latency ...
2026-08-12T08:05:22.573722Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: 
2026-08-12T08:05:56.898204Z ERROR codex_models_manager::manager: failed to renew cache TTL: missing field `base_instructions` at line 94 column 5
web search: 
web search: "Understanding the “90% syndrome”" authors 1988 ...
warning: Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
context compacted
codex
The evidence base supports a clear product rule: recommendations should be visible and prefilled, but the export must distinguish “left at default” from “explicitly confirmed.” I’m now turning that rule into the document structure, state model, and safety contract, while keeping population-level questionnaire evidence explicitly bounded where it does not transfer cleanly to one owner.
codex
## Executive Summary

- **(High Confidence)** Build a layered owner brief: plain-English outcome, explicit completion gates, evidence-backed status ledger, then decision cards ordered by what they unblock.
- **(High Confidence)** Never use a single “90% complete” or green/red status as the source of truth. Separate built, tested, deployable, deployed, and accepted states, each with evidence and verification time.
- **(High Confidence)** Show recommendations pre-selected, but never treat an untouched default as a human decision. Export `default_left_unchanged` separately from `explicitly_confirmed`.
- **(High Confidence)** Every blocked item should link to the exact decision that releases it, the consequence of delay, and the next action enabled by confirmation.
- **(Medium Confidence)** Order decisions by downstream importance and decision effort, then group them by dependency and urgency. Avoid a global rank that encourages anchoring and neglect of lower-ranked options.
- **High Confidence** Preserve raw answers, notes, caveats, evidence references, source snapshots, timestamps, and confirmation events in JSON. Agents should act only on explicit confirmations or explicit overrides.
- **High Confidence** Treat AI-generated prose as a view over an evidence ledger, never as evidence itself. Unsupported claims must remain “unknown” or “not evidenced.”
- **Medium Confidence** A single-file HTML document is a strong delivery format for durability and asynchronous completion, but direct evidence for this exact product pattern is missing and should be validated with usability, accessibility, print, and adversarial agent tests.

## Detailed Findings

### 1. How should a status-and-decision document be designed so that a single non-technical owner can, in one sitting, understand what remains before a software project is complete and settle every decision that is blocking the work?

The decisive design is an evidence-led owner brief with four layers:

1. **Outcome summary:** what the software does today, what remains, and whether it is usable by its intended users.
2. **Completion ledger:** each deliverable with a separate state and proof.
3. **Decision queue:** only decisions that block or materially change remaining work.
4. **Machine-readable export:** an explicit, provenance-preserving record of what the owner decided and what remains unresolved.

#### Status communication and its failure modes

Software status reporting is demonstrably vulnerable to systematic optimism. Snow, Keil and Wallace found that status reports were biased in approximately 60% of cases; optimistic bias was about twice as common as pessimistic bias. Their information-theoretic model estimated that only roughly 10–15% of biased reports were accurate, with pessimistic bias partly offsetting reporting error. [sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0378720606001145)[Snow, Keil & Wallace, “The effects of optimistic and pessimistic biasing on software project status reporting,” 2007](https://www.sciencedirect.com/science/article/abs/pii/S0378720606001145) (unusable citation URL)` **(High Confidence)**

A 561-project-manager study similarly found that optimistic bias damages reporting quality, while trust, communication quality and executive power affect selective status reporting. [Iacovou, Thompson & Smith, “Selective Status Reporting in Information Systems Projects,” 2009(https://aisel.aisnet.org/misq/vol33/iss4/11/)](https://aisel.aisnet.org/misq/vol33/iss4/11/) **(High Confidence)**

The “90% syndrome” is not merely a communication cliché. A simulation-based software project study attributed it to underestimation and imprecise measurement caused by poor project visibility. [“Understanding the ‘90% syndrome’ in software project management,” 1988(https://www.sciencedirect.com/science/article/pii/0164121288900155)](https://www.sciencedirect.com/science/article/pii/0164121288900155) **(High Confidence)**

Therefore, the page should not report “percentage complete” except as a clearly labelled, non-authoritative estimate. It should instead use a status ledger:

| Owner-facing state | Meaning | Required evidence |
|---|---|---|
| Not started | Work has not begun | Identified owner and scope |
| In progress | Work exists but is not ready for acceptance | Current artifact or activity |
| Built | Implementation exists | Commit, build, or artifact identifier |
| Tested | Defined tests have passed | Test result and timestamp |
| Deployable | Can be released safely on demand | Release/build evidence |
| Deployed | Running in the named environment | Environment, deployment ID, timestamp |
| Accepted | Owner or acceptance authority has verified the outcome | Acceptance record |
| Blocked | Cannot proceed without a named decision, input, or external dependency | Linked blocker and releasing decision |

DORA defines change lead time as the period from code committed to version control until deployment in production, and distinguishes continuous delivery from continuous deployment. It also asks whether software is in a deployable state throughout its lifecycle and whether it can be deployed at any time. [DORA metrics guide(https://dora.dev/guides/dora-metrics/)](https://dora.dev/guides/dora-metrics/) [DORA, “Continuous delivery”(https://dora.dev/capabilities/continuous-delivery/)](https://dora.dev/capabilities/continuous-delivery/) **(High Confidence)**

<INFERENCE from="Snow, Keil & Wallace 2007; Iacovou, Thompson & Smith 2009; 90% syndrome study 1988; DORA metric definitions">The document should make “built,” “deployable,” “deployed,” and “accepted” visibly different fields. This directly prevents a reassuring implementation status from being mistaken for a usable product.</INFERENCE> **(High Confidence)**

A useful top-of-page summary is:

| Question | Answer format |
|---|---|
| Can the intended user use it today? | Yes / Partly / No / Not evidenced |
| What remains before acceptance? | Three to seven owner-readable outcomes |
| What is blocking progress? | Decision IDs, missing inputs, external dependencies |
| What must the owner decide now? | Number of unresolved blocking decisions |
| What happens after each decision? | Unblocked work and expected consequence |

Release notes are a useful supporting format but not a complete project-status instrument. A mixed-method study examined 32,425 release notes from 1,000 GitHub projects, interviewed 15 practitioners and surveyed 314 respondents. It identified eight information categories and found generally positive perceived impact, but also significant disagreement between stakeholders about how release notes should be written and used. [Bi et al., “An empirical study of release note production and usage in practice,” 2022(https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/)](https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/) **(High Confidence)**

<INSUFFICIENT_EVIDENCE>There is no strong direct study comparing a single self-contained HTML status brief against a dashboard, email, or meeting for one non-technical software owner, using comprehension, decision latency and decision correctness as outcomes.</INSUFFICIENT_EVIDENCE>

#### Plain language and progressive disclosure

A CHI 2024 study found that lower-complexity machine-generated summaries were significantly easier to read, with effect size `d = 0.535`, and easier to understand, with `d = 0.323`, than higher-complexity summaries. [August et al., “Know Your Audience,” CHI 2024(https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf)](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) **(High Confidence)**

The same study found a trade-off: simplified summaries omitted more information, particularly when there were multiple findings or limitations. [August et al., “Know Your Audience,” CHI 2024(https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf)](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) **(High Confidence)**

The document should therefore use:

- a short plain-English explanation in the main flow;
- expandable technical evidence beneath each claim;
- a complete evidence appendix for durable review;
- explicit labels for `observed`, `inferred`, and `unknown`.

Plain language should reduce cognitive load, not remove decision-relevant limitations.

#### Questionnaire design for one expert respondent

Defaults are powerful but not uniformly beneficial. A meta-analysis of 58 default studies involving 73,675 participants found an overall default effect of `d = 0.68`, with a 95% confidence interval of `0.53–0.83`. The majority of studies showed positive effects, but several were null and two were negative. In binary-choice studies, defaults increased selection by an average of 27.24 percentage points. [Jachimowicz et al., “When and why defaults influence decisions,” 2019(https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0)](https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0) **(High Confidence)**

Defaults work through several mechanisms: perceived endorsement, reduced effort, and the tendency to retain an existing state. Their effectiveness varies substantially by domain and decision context. [Jachimowicz et al., 2019(https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0)](https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0) **(High Confidence)**

A 2024 study found that experience can reverse default effects. In a protective-default condition, participants rejected the default on 90% of trials because the alternative produced a higher expected payoff. [“The impact of experience on the tendency to accept recommended defaults,” 2024(https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46)](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46) **(Medium Confidence)**

The design rule is:

> Preselect a recommendation when the recommendation is evidence-backed, reversible, low-risk, and clearly explained. Require explicit confirmation before treating it as a decision. Do not hide the alternatives or make the owner clear a default merely to demonstrate agency.

For material, irreversible, safety-sensitive, legal, financial, or scope-defining decisions, use an active confirmation action such as:

> “I have reviewed this recommendation and confirm it.”

An active-choice randomized trial with 1,279 eligible participants found advance-directive completion of 35.1% in the active-choice group versus 20.4% in control, a 14.7 percentage-point difference. [“Active Choice Intervention Increases Advance Directive Completion,” 2018(https://pmc.ncbi.nlm.nih.gov/articles/PMC6132204/)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6132204/) **(Medium Confidence; transfer from healthcare to software decisions is limited)**

Each decision card should contain:

| Field | Purpose |
|---|---|
| Decision ID | Stable machine-readable identity |
| Plain-English question | The choice the owner must settle |
| Why this is needed now | Immediate blocker |
| Recommendation | Preselected option and rationale |
| Alternatives | At least the viable alternatives, not a token “other” |
| Consequences | What changes for cost, scope, time, risk, or users |
| Unblocks | Work released by this answer |
| Evidence | Links to source claims and project artifacts |
| Answer control | Radio, checkbox, numeric field, or explicit skip |
| Optional note | Caveat, condition, exception, or context |
| Confirmation action | Explicitly records review and decision |

Use radio buttons for mutually exclusive choices and checkboxes only where multiple options genuinely compose. Do not use a multi-select control to conceal an unresolved trade-off.

Optional notes should never substitute for the structured answer. Open-text questions have materially higher nonresponse than structured items; one 2024 study reported written final-comment nonresponse of 55.8%. [Höhne & Claassen, “Examining final comment questions,” 2024(https://doi.org/10.1177/14707853241229329)](https://doi.org/10.1177/14707853241229329) **(Medium Confidence; population survey evidence)**

The export should distinguish:

- unanswered;
- intentionally skipped;
- default left unchanged;
- explicitly accepted recommendation;
- explicitly overridden;
- needs clarification.

A blank note means “no note supplied,” not “no caveat exists.”

#### Ordering, batching and dependency visibility

A decision should be shown in the context of the work it releases:

> **D-004: Choose the supported payment provider**  
> Blocks: checkout integration, end-to-end test, production launch  
> If confirmed: implementation can begin  
> If unanswered: launch remains blocked  
> Recommendation: Provider A  
> Basis: existing account, tested integration, lower migration cost

Formal requirements-prioritization research shows that dependencies are often omitted from stakeholder prioritization, even though direct and transitive dependencies determine implementation order. DRank combines stakeholder preferences with dependency extraction; CDBR models execute-before-after relationships and dependency propagation. [DRank, “A semi-automated requirements prioritization method,” 2017(https://doi.org/10.1016/j.jss.2016.09.043)](https://doi.org/10.1016/j.jss.2016.09.043) [CDBR, “Dependency-based requirement prioritization,” 2019(https://link.springer.com/article/10.1016/j.jksuci.2018.10.004)](https://link.springer.com/article/10.1016/j.jksuci.2018.10.004) **(Medium Confidence; the underlying studies are technical rather than owner-facing)**

Information has value only when it changes an actionable decision. NIST’s value-of-information framework explicitly compares the benefit of acquiring information with its cost and frames decisions as pathways with consequential actions. [NIST, “Value of information and decision pathways,” 2022(https://www.nist.gov/publications/value-information-and-decision-pathways-concepts-and-case-studies)](https://www.nist.gov/publications/value-information-and-decision-pathways-concepts-and-case-studies) **(High Confidence)**

<INFERENCE from="NIST value-of-information framework; DRank; CDBR">Order decision cards using a visible “why now” rule: downstream consequence, owner effort, reversibility, and whether the answer releases critical-path work. A defensible heuristic is `downstream importance × urgency ÷ decision effort`, but this exact formula is not empirically validated for software owners.</INFERENCE> **(Medium Confidence)**

Do not display one global rank for every decision. Ranking information changes attention: an experiment found that rank information affected preferences beyond the underlying ratings and caused attention to concentrate on top-ranked items. [Chun et al., “The Power of Rank Information,” 2021(https://doi.org/10.1037/pspa0000289)](https://doi.org/10.1037/pspa0000289) **(High Confidence)**

Conversely, an interactive decision-search experiment found that sorting by one category did not improve search outcomes, while showing relative rank across attributes improved search. [“An experimental study of the decision process with interactive technology,” 2016(https://doi.org/10.1016/j.jebo.2016.06.004)](https://doi.org/10.1016/j.jebo.2016.06.004) **(Medium Confidence)**

Use dependency groups instead:

- **Must decide to release work**
- **Changes scope or user promise**
- **Reduces operational or security risk**
- **Can wait without blocking completion**
- **Needs more evidence before a decision is safe**

Within each group, show one recommended next decision and its downstream effects. The owner should be able to see why a decision is first without interpreting the ordering as objective truth.

#### Asynchronous decision instruments

Written decision instruments have useful evidence, but little of it directly matches this exact use case.

A field experiment comparing face-to-face and asynchronous group decision-making found that asynchronous groups produced broader discussions and more complete reports, while both conditions omitted approximately 15% of issues. [“A comparative content analysis of face-to-face vs asynchronous group decision making,” 2003(https://doi.org/10.1016/S0167-9236(02)00072-6)](https://doi.org/10.1016/S0167-9236(02)00072-6) **(Medium Confidence; group evidence, not single-owner evidence)**

An observational healthcare study found that asynchronous communication reduced task completion time by an average of 20.1 minutes, or 58.8%, compared with existing communication methods. [“Examining the impact of an asynchronous communication platform,” 2021(https://pmc.ncbi.nlm.nih.gov/articles/PMC7808296/)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7808296/) **(Low Confidence for software transfer)**

Architecture Decision Record research is more cautious. A 2023 action-research study found that teams perceived ADRs as useful, but reported challenges involving culture, tacit knowledge, process, tool support, appropriate detail, prioritization, placement and maintenance. [Ahmeti, Linder & Wohlrab, “Exploring the Adoption and Effectiveness of Architecture Decision Records,” 2023(https://research.chalmers.se/en/publication/538920)](https://research.chalmers.se/en/publication/538920) **(Medium Confidence)**

The document should therefore function as both:

- an asynchronous decision brief for the owner;
- a compact ADR-like record after confirmation.

Each confirmed decision should automatically retain context, alternatives, rationale, consequences, evidence and timestamp. A meeting may still be useful for exceptional ambiguity, but the page should make a meeting unnecessary for ordinary blocking choices.

#### Machine-readable round-trip and safe agent action

Use W3C PROV concepts for provenance: entities, activities and agents, with relationships such as `used`, `wasGeneratedBy`, `wasInformedBy` and `wasDerivedFrom`. [W3C PROV Primer(https://www.w3.org/TR/prov-primer/)](https://www.w3.org/TR/prov-primer/) [W3C PROV-O(https://www.w3.org/TR/prov-o/)](https://www.w3.org/TR/prov-o/) **(High Confidence)**

Validate the export against a strict JSON Schema with enumerated states and rejected unknown fields. JSON Schema supports object constraints and controlled structural validation, but schema validation alone cannot establish that a decision is wise or that a caveat was understood. [JSON Schema object reference(https://json-schema.org/understanding-json-schema/reference/object)](https://json-schema.org/understanding-json-schema/reference/object) **(High Confidence)**

A minimum export should look like this:

```json
{
  "schema_version": "1.0",
  "document": {
    "id": "project-status-2026-08-12",
    "generated_at": "2026-08-12T00:00:00Z",
    "source_snapshot": {
      "captured_at": "2026-08-11T23:00:00Z",
      "content_hash": "sha256:...",
      "evidence_refs": ["SRC-001", "SRC-002"]
    }
  },
  "decisions": [
    {
      "id": "D-004",
      "type": "single_select",
      "question": "Which payment provider should launch support?",
      "options": [
        {"id": "provider_a", "label": "Provider A"},
        {"id": "provider_b", "label": "Provider B"}
      ],
      "recommendation": {
        "option_id": "provider_a",
        "basis_refs": ["PROJ-ARTIFACT-17", "SRC-009"]
      },
      "answer": {
        "selected_option_ids": ["provider_a"],
        "raw_value": "provider_a"
      },
      "answer_status": "default_left_unchanged",
      "selection_origin": "default",
      "confirmation": {
        "explicit": false,
        "event_id": null,
        "confirmed_at": null
      },
      "notes": [
        {
          "raw_text": "Use Provider B if international expansion is brought forward.",
          "kind": "condition",
          "actionability": "requires_review"
        }
      ],
      "unblocks": [
        {
          "item_id": "WORK-021",
          "relation": "direct",
          "consequence": "Begin checkout integration"
        }
      ],
      "scope": {
        "applies_to": "launch_v1",
        "expires_at": null,
        "review_trigger": "international_expansion"
      },
      "agent_policy": {
        "allowed_actions": ["start_checkout_integration"],
        "approval_required": true,
        "forbidden_actions": ["change_provider_contract"]
      }
    }
  ],
  "events": [
    {
      "type": "page_loaded",
      "decision_id": "D-004",
      "at": "2026-08-12T00:05:00Z"
    }
  ]
}
```

The required distinction is:

| Export state | Meaning | Agent action |
|---|---|---|
| `unanswered` | Owner has not answered | Ask or wait |
| `skipped` | Owner intentionally deferred | Preserve blocker |
| `default_left_unchanged` | Recommendation remained selected without explicit confirmation | Do not execute material action |
| `explicitly_confirmed` | Owner explicitly accepted the selected answer | Act within policy |
| `explicitly_overridden` | Owner explicitly chose another answer | Act within policy, preserving override |
| `needs_clarification` | Answer or caveat is ambiguous or conditional | Ask a targeted follow-up |

Agent benchmarks document weaknesses in long-horizon reasoning, decision-making and instruction following. AgentBench evaluated 29 models across eight environments and identified these as major obstacles. [AgentBench, ICLR 2024(https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html)](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html) **(High Confidence)**

NIST’s agent-evaluation work explicitly tests citation faithfulness, citation completeness and citation sufficiency, and produces a structured audit trail. [NIST, “Building Evaluation Probes for Agentic AI,” 2026(https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai)](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) **(High Confidence)**

<INFERENCE from="W3C PROV; JSON Schema; AgentBench; NIST agentic evaluation">The agent must never infer confirmation from selection alone, never discard raw notes after extracting a summary, and never execute an irreversible action when a caveat is conditional, blocking, stale or unparsed. It should validate the document hash, schema, option IDs, answer state, scope and action policy before acting.</INFERENCE> **(High Confidence)**

The most important failure cases to test are:

- terse answer interpreted as unconditional;
- caveat stored but ignored;
- default mistaken for explicit consent;
- decision applied outside its scope;
- stale answer applied to a changed project snapshot;
- multi-select interpreted as an ordered preference;
- “yes” applied to the wrong decision ID;
- unsupported agent summary replacing the owner’s raw note.

#### Integrity of AI-generated status artefacts

NIST defines confabulation as confidently presented erroneous or false content, including fabricated logic or citations that can mislead users. [NIST, Generative AI Risk Management Profile, 2024(https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) **(High Confidence)**

A CHI study likewise states that no automated method guarantees factual accuracy or fidelity in plain-language generation. In its experiment, 14 of 120 generated summaries contained incorrect information; the correct replacement was found within at most six alternatives, with an average of 2.36 generations. [August et al., CHI 2024(https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf)](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) **(High Confidence)**

A 2025 Nature Machine Intelligence study found that users can overestimate model accuracy when explanations are provided by default; longer explanations increased confidence without necessarily improving accuracy, while uncertainty-aligned explanations improved calibration. [“What large language models know and what people think they know,” 2025(https://www.nature.com/articles/s42256-024-00976-7)](https://www.nature.com/articles/s42256-024-00976-7) **(High Confidence)**

The honesty contract should be:

- every status claim has a source reference, source timestamp and verification state;
- every claim is classified as `observed`, `inferred`, or `unknown`;
- “complete” requires named acceptance evidence;
- an absent source produces “not evidenced,” never a guessed status;
- generated prose cannot overwrite the underlying status ledger;
- citations open to durable source snapshots, not only live URLs;
- the export records the hash of the snapshot from which the document was generated.

NIST’s newer agentic-evaluation approach is a useful model: test whether sources support claims, whether relevant evidence was omitted, and whether the sources are sufficient for the conclusion. [NIST agentic evaluation probes(https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai)](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) **(High Confidence)**

#### Accessibility, printing and self-containment

The HTML should be a single offline-capable file with inline CSS and JavaScript, no CDN dependencies, no remote fonts, no external images and no required network request.

Use semantic headings, landmarks, tables, `fieldset`/`legend`, labels, keyboard navigation, visible focus, and text labels in addition to color. WCAG 2.2 requires, at Level AA, a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text, and requires content to remain usable when text is resized to 200%. [W3C Web Content Accessibility Guidelines 2.2(https://www.w3.org/TR/WCAG22/)](https://www.w3.org/TR/WCAG22/) **(High Confidence)**

Every control needs an explicit label association; W3C’s forms guidance recommends programmatically associating labels with their controls. [W3C WAI, “Labels,”(https://www.w3.org/WAI/tutorials/forms/labels/)](https://www.w3.org/WAI/tutorials/forms/labels/) **(High Confidence)**

Use print-specific CSS for page size, margins, page breaks and print-only elements. CSS Paged Media defines page layout controls, while Media Queries support print-targeted styling. [CSS Paged Media Module(https://www.w3.org/TR/css-page-3/)](https://www.w3.org/TR/css-page-3/) [Media Queries Level 3(https://www.w3.org/TR/mediaqueries-3/)](https://www.w3.org/TR/mediaqueries-3/) **(High Confidence)**

Print output should include:

- project identity and source-snapshot hash;
- all unresolved blockers;
- selected answers and answer states;
- raw notes and caveats;
- confirmation timestamp;
- export instructions or an embedded JSON text appendix.

`localStorage` may improve convenience but must not be the only persistence mechanism. The durable record is the saved HTML plus exported JSON.

<MISSING_DATA>Cross-browser behavior, screen-reader behavior, PDF pagination, offline file restrictions and keyboard completion rates require testing in the target browser and assistive-technology matrix. Standards compliance alone does not establish usability.</MISSING_DATA>

#### Implementation-pattern comparison

No model, provider or hosting target was specified, so model parameter counts, context windows, latency, cost and licenses cannot be filled defensibly.

| Implementation pattern | Parameter Count | Context Window | Latency | Cost | License/Portability | Fit |
|---|---:|---:|---:|---:|---|---|
| Static self-contained HTML + vanilla JavaScript | N/A | N/A | Local; measure on target devices | Zero runtime API cost | Highly portable; standards-based | Best durable decision record |
| Generate once from a verified project snapshot, then freeze HTML | Model-specific | Model-specific | Generation-time only; `<MISSING_DATA>` | `<MISSING_DATA>`; provider/model unspecified | Depends on chosen model | Best balance of automation and auditability |
| Remote interactive agent with JSON export | `<MISSING_DATA>` | `<MISSING_DATA>` | Network- and model-dependent | Hosting plus model usage; `<MISSING_DATA>` | Provider-dependent | Useful for preparation and follow-up |
| Client-side model embedded in HTML | `<MISSING_DATA>` | `<MISSING_DATA>` | Device-dependent | Model distribution and compute cost | License and browser support uncertain | Avoid for core status truth |
| Static HTML with server-side action executor | N/A for page; executor-specific | Executor-specific | Action/API-dependent | Infrastructure-dependent | Must define API and authorization | Suitable only behind explicit confirmation gates |

## 2. What is the current state, and what is the strongest supporting evidence for it?

The strongest current position is a hybrid:

- structured state ledgers outperform vague narrative for truthfulness;
- plain-language summaries improve comprehension but can omit limitations;
- defaults improve completion in many settings but can impair decisions when the recommendation is protective, unfamiliar, irreversible or poorly matched;
- dependency-aware ordering is technically well established but weakly tested for nontechnical owner comprehension;
- asynchronous records improve durability and can improve coverage, but direct evidence for one-owner software decisions is sparse;
- provenance and auditability are becoming explicit requirements for agentic systems;
- AI-generated status should be treated as probabilistic synthesis requiring evidence checks.

The most direct evidence is stronger for component behaviors than for the complete product pattern. Defaults, plain-language summaries, provenance, status bias and agent instruction failures have substantial evidence. The exact combination—single-file HTML, one nontechnical owner, blocker-linked questionnaire, preselected recommendations and safe JSON round-trip—does not yet have a mature empirical literature.

<INSUFFICIENT_EVIDENCE>The field lacks a benchmark dataset measuring one owner’s comprehension, decision quality, latency, completion rate and later correction rate across status formats.</INSUFFICIENT_EVIDENCE>

The practical design should therefore be evidence-constrained rather than evidence-claimed: use known behavioral effects, explicitly label inferences, and instrument the product for validation.

## 3. What are the contrasting viewpoints or competing evidence?

**Defaults versus active choice.** The default meta-analysis shows a large average effect, but the 2024 evidence demonstrates that defaults can reverse when people understand the payoff structure. The correct compromise is a visible recommendation with an explicit acceptance event. <CONFLICTING_EVIDENCE>Defaults often increase completion and selection, but can reduce decision quality when the default is poorly matched, protective, irreversible or insufficiently understood.</CONFLICTING_EVIDENCE>

**Plain language versus completeness.** Simpler summaries improve readability and understanding, but may omit limitations and secondary findings. The page should use progressive disclosure rather than choosing either extreme. [August et al., CHI 2024(https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf)](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) **(High Confidence)**

**Ranking versus grouping.** Rank information attracts attention to the top option, which can speed selection but can also suppress consideration of alternatives. Choice-overload research finds that overload depends on set complexity, task difficulty, preference uncertainty and the decision-maker’s goal; a 2015 meta-analysis covered 99 observations and 7,202 participants. [Chernev, Böckenholt & Goodman, “Choice overload,” 2015(https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2014.08.002)](https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2014.08.002) **(High Confidence)**

An older meta-analysis found little average choice-overload effect, indicating that overload is conditional rather than universal. <CONFLICTING_EVIDENCE>The evidence supports controlling complexity and uncertainty, but does not justify a universal maximum number of choices or a universal “rank everything” rule.</CONFLICTING_EVIDENCE>

**Async versus synchronous decisions.** Asynchronous records can provide broader written coverage and durable rationale, but may leave ambiguity unresolved and lack the immediate repair mechanism of conversation. ADR evidence is currently mostly action research and perception-based rather than controlled measurement of decision latency or quality. [Ahmeti, Linder & Wohlrab, 2023(https://research.chalmers.se/en/publication/538920)](https://research.chalmers.se/en/publication/538920) **(Medium Confidence)**

**AI explanation versus calibrated trust.** More explanation is not automatically more truthful or better calibrated. The document should show evidence and uncertainty, not merely produce longer prose. [Nature Machine Intelligence study, 2025(https://www.nature.com/articles/s42256-024-00976-7)](https://www.nature.com/articles/s42256-024-00976-7) **(High Confidence)**

## 4. What changed recently, and what is the trajectory?

From 2019 onward, default research moved from asking whether defaults work to asking when they reverse, how experience changes them and whether the default is genuinely beneficial. [Jachimowicz et al., 2019(https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0)](https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0) [Judgment and Decision Making study, 2024(https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46)](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46) **(High Confidence)**

During the same period, software documentation research increasingly examined release-note usefulness and stakeholder disagreement rather than treating documentation as a single audience problem. [Bi et al., 2022(https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/)](https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/) **(High Confidence)**

Since 2024, authoritative AI guidance has emphasized confabulation, citation faithfulness, citation completeness, provenance and audit trails. NIST’s 2026 agentic-evaluation work is especially close to the required round-trip: it evaluates whether cited sources actually support claims and whether evidence is sufficient. [NIST Generative AI Profile, 2024(https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) [NIST agentic evaluation probes, 2026(https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai)](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) **(High Confidence)**

<INFERENCE from="NIST GenAI Profile 2024; Nature Machine Intelligence 2025; NIST agentic probes 2026; W3C PROV">The trajectory is from “AI-generated status narrative” toward evidence-linked, provenance-preserving, auditable decision artifacts. A product designed now should assume that source traceability and explicit uncertainty will become normal requirements for agent-mediated work.</INFERENCE> **(Medium Confidence)**

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL | Source-discipline fit |
|---|---|---:|---|---|---|
| Status reports are frequently biased; optimism is common | Snow, Keil & Wallace | 2007 | Peer-reviewed empirical study and model | [Source](https://www.sciencedirect.com/science/article/abs/pii/S0378720606001145) | Direct software-project status research |
| Selective reporting degrades project reporting quality | Iacovou, Thompson & Smith | 2009 | Peer-reviewed survey study of 561 managers | [Source](https://aisel.aisnet.org/misq/vol33/iss4/11/) | Direct information-systems evidence |
| “90% syndrome” arises from poor visibility and imprecise measurement | Journal of Systems and Software study | 1988 | Simulation-based software case study | [Source](https://www.sciencedirect.com/science/article/pii/0164121288900155) | Direct software-project evidence |
| Built, deployable and deployed are distinct states | DORA | Current documentation | Official engineering/research guidance | [Metrics](https://dora.dev/guides/dora-metrics/), [CD](https://dora.dev/capabilities/continuous-delivery/) | Authoritative operational definitions; vendor-affiliated caveat |
| Release notes have multiple audiences and stakeholder disagreement | Bi et al. | 2022 | Mixed-method peer-reviewed empirical study | [Source](https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/) | Direct software documentation research |
| Plain-language summaries improve readability and understanding | August et al. | 2024 | CHI experiments | [Paper](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) | Peer-reviewed human-computer interaction research |
| Simplification can omit limitations and findings | August et al. | 2024 | CHI experiment | [Paper](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) | Direct evidence on machine-generated summaries |
| Defaults have a large average effect but variable direction | Jachimowicz et al. | 2019 | Peer-reviewed meta-analysis; 58 studies, 73,675 participants | [Source](https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0) | Strong decision-science synthesis |
| Experience can reverse default effects | Judgment and Decision Making study | 2024 | Peer-reviewed preregistered experiments | [Source](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46) | Direct experimental evidence |
| Active confirmation can increase completion | Active-choice randomized trial | 2018 | Randomized controlled trial | [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC6132204/) | Strong causal evidence, but healthcare transfer |
| Question format changes selection and satisficing | Pew Research Center | 2019 | Randomized survey experiment; 4,581 adults | [Source](https://www.pewresearch.org/methods/2019/05/09/when-online-survey-respondents-only-select-some-that-apply/) | Original research; limited transfer to one owner |
| Forced answering and explicit nonresponse can increase missingness | Kmetty & Stefkovics | 2021 | Online questionnaire experiment | [Source](https://www.tandfonline.com/doi/full/10.1080/13645579.2021.1929714) | Original methods research; limited transfer |
| Rank information changes attention and preference | Chun et al. | 2021 | Peer-reviewed experiments | [DOI](https://doi.org/10.1037/pspa0000289) | Direct decision-presentation evidence |
| Choice overload is conditional | Chernev, Böckenholt & Goodman | 2015 | Meta-analysis; 99 observations, 7,202 participants | [Source](https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2014.08.002) | Strong synthesis; not software-specific |
| Dependencies affect implementation ordering | DRank and CDBR studies | 2017–2019 | Peer-reviewed software-engineering methods and experiments | [DRank](https://doi.org/10.1016/j.jss.2016.09.043), [CDBR](https://link.springer.com/article/10.1016/j.jksuci.2018.10.004) | Direct technical dependency research |
| Information should be evaluated by decision value and acquisition cost | NIST | 2022 | Government research framework | [Source](https://www.nist.gov/publications/value-information-and-decision-pathways-concepts-and-case-studies) | Authoritative decision-analysis source |
| Async communication can improve written coverage but has trade-offs | Decision-support and healthcare studies | 2003–2021 | Field experiment and observational study | [2003](https://doi.org/10.1016/S0167-9236(02)00072-6), [2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7808296/) | Primary studies; transfer explicitly limited |
| ADR adoption is useful but empirically undermeasured | Ahmeti, Linder & Wohlrab | 2023 | Action research | [Source](https://research.chalmers.se/en/publication/538920) | Direct software-architecture research |
| Decision aids improve knowledge and reduce decisional conflict | Cochrane review | 2024 | Systematic review; 107 studies for knowledge outcome | [PubMed](https://pubmed.ncbi.nlm.nih.gov/38284415/) | High-quality synthesis, healthcare transfer |
| Provenance should record entities, activities and agents | W3C | Current standard | International technical standard | [PROV Primer](https://www.w3.org/TR/prov-primer/), [PROV-O](https://www.w3.org/TR/prov-o/) | Authoritative interoperability standard |
| Agents fail at long-horizon reasoning and instruction following | AgentBench | 2024 | Peer-reviewed benchmark across 29 models and eight environments | [ICLR paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html) | Direct benchmark evidence |
| AI can confidently produce false content and fabricated citations | NIST | 2024 | Government risk profile | [PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Authoritative AI-risk source |
| Users can be overconfident in AI-generated explanations | Nature Machine Intelligence study | 2025 | Peer-reviewed human-model calibration study | [Source](https://www.nature.com/articles/s42256-024-00976-7) | Direct trust-calibration evidence |
| Citation faithfulness, completeness and sufficiency can be evaluated | NIST | 2026 | Government evaluation framework | [Source](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) | Current authoritative agent-evaluation source |
| Accessible forms require labels and sufficient contrast | W3C | Current standards | WCAG and WAI guidance | [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Form labels](https://www.w3.org/WAI/tutorials/forms/labels/) | Authoritative accessibility standards |
| Print layout can be controlled with paged-media CSS | W3C | Current standards | CSS standards | [Paged Media](https://www.w3.org/TR/css-page-3/), [Media Queries](https://www.w3.org/TR/mediaqueries-3/) | Authoritative web-platform standards |

## Knowledge Gaps

**Direct product evidence**

< MISSING_DATA >No controlled study was found for the complete target artifact: a single self-contained HTML status-and-decision page used by one nontechnical software owner in one sitting.</MISSING_DATA>

Needed measures include comprehension, time to first correct decision, completion rate, decision reversals, clarification requests, missed caveats and agent execution errors.

**Default and recommendation evidence**

<INSUFFICIENT_EVIDENCE>Existing default studies do not establish the optimal presentation of a software recommendation where the respondent is the project owner and the recommendation is generated from project evidence.</INSUFFICIENT_EVIDENCE>

Needed evidence compares blank forms, visible defaults, visible recommendations and explicit active-confirmation flows using decisions with known correct or preferred outcomes.

**Dependency ordering**

<INSUFFICIENT_EVIDENCE>Technical requirements-prioritization research supports dependency graphs, but does not establish whether nontechnical owners understand or prefer critical-path, effort-adjusted, value-adjusted or grouped ordering.</INSUFFICIENT_EVIDENCE>

**Asynchronous decision quality**

<INSUFFICIENT_EVIDENCE>Evidence supports durability and broader written coverage, but direct measurements of decision latency, quality and completion for software owners using RFC/ADR-style self-serve forms are scarce.</INSUFFICIENT_EVIDENCE>

**AI-generated status trust**

Current studies establish hallucination, overconfidence and citation-quality risks, but not how owners calibrate trust in a project-completion report containing source-linked evidence and explicit unknowns.

**Accessibility and printing**

<MISSING_DATA>Target-browser, screen-reader, keyboard-only, offline-file, print-to-PDF and large-document performance remain implementation questions requiring testing rather than literature review.</MISSING_DATA>

## Recommended Next Steps

1. **Run a task-based usability study with representative nontechnical owners.** Measure whether participants can identify what remains, find the highest-impact blocker, and complete the export without assistance.

2. **Compare four answer states experimentally:** blank, preselected recommendation, preselected recommendation with rationale, and recommendation plus explicit confirmation. Measure completion, override rate, correctness, time, later regret and caveat recall.

3. **Test dependency ordering against global ranking.** Compare blocker-linked groups, critical-path order, effort-adjusted order and unranked chronological order. Measure decision latency, missed dependencies and unnecessary deferrals.

4. **Build an adversarial JSON round-trip test suite.** Include defaults left untouched, terse answers, contradictory notes, conditional caveats, stale source snapshots, multi-select ambiguity and unknown option IDs. The agent must abstain or ask for clarification whenever the export is not action-safe.

5. **Perform a standards and real-device accessibility pass.** Test keyboard navigation, screen readers, contrast, zoom, print pagination, offline opening, JSON download, reload recovery and `noscript` behavior before treating the HTML as a durable project record.
tokens used
287,653
## Executive Summary

- **(High Confidence)** Build a layered owner brief: plain-English outcome, explicit completion gates, evidence-backed status ledger, then decision cards ordered by what they unblock.
- **(High Confidence)** Never use a single “90% complete” or green/red status as the source of truth. Separate built, tested, deployable, deployed, and accepted states, each with evidence and verification time.
- **(High Confidence)** Show recommendations pre-selected, but never treat an untouched default as a human decision. Export `default_left_unchanged` separately from `explicitly_confirmed`.
- **(High Confidence)** Every blocked item should link to the exact decision that releases it, the consequence of delay, and the next action enabled by confirmation.
- **(Medium Confidence)** Order decisions by downstream importance and decision effort, then group them by dependency and urgency. Avoid a global rank that encourages anchoring and neglect of lower-ranked options.
- **High Confidence** Preserve raw answers, notes, caveats, evidence references, source snapshots, timestamps, and confirmation events in JSON. Agents should act only on explicit confirmations or explicit overrides.
- **High Confidence** Treat AI-generated prose as a view over an evidence ledger, never as evidence itself. Unsupported claims must remain “unknown” or “not evidenced.”
- **Medium Confidence** A single-file HTML document is a strong delivery format for durability and asynchronous completion, but direct evidence for this exact product pattern is missing and should be validated with usability, accessibility, print, and adversarial agent tests.

## Detailed Findings

### 1. How should a status-and-decision document be designed so that a single non-technical owner can, in one sitting, understand what remains before a software project is complete and settle every decision that is blocking the work?

The decisive design is an evidence-led owner brief with four layers:

1. **Outcome summary:** what the software does today, what remains, and whether it is usable by its intended users.
2. **Completion ledger:** each deliverable with a separate state and proof.
3. **Decision queue:** only decisions that block or materially change remaining work.
4. **Machine-readable export:** an explicit, provenance-preserving record of what the owner decided and what remains unresolved.

#### Status communication and its failure modes

Software status reporting is demonstrably vulnerable to systematic optimism. Snow, Keil and Wallace found that status reports were biased in approximately 60% of cases; optimistic bias was about twice as common as pessimistic bias. Their information-theoretic model estimated that only roughly 10–15% of biased reports were accurate, with pessimistic bias partly offsetting reporting error. [Snow, Keil & Wallace, “The effects of optimistic and pessimistic biasing on software project status reporting,” 2007(https://www.sciencedirect.com/science/article/abs/pii/S0378720606001145)](https://www.sciencedirect.com/science/article/abs/pii/S0378720606001145) **(High Confidence)**

A 561-project-manager study similarly found that optimistic bias damages reporting quality, while trust, communication quality and executive power affect selective status reporting. [Iacovou, Thompson & Smith, “Selective Status Reporting in Information Systems Projects,” 2009(https://aisel.aisnet.org/misq/vol33/iss4/11/)](https://aisel.aisnet.org/misq/vol33/iss4/11/) **(High Confidence)**

The “90% syndrome” is not merely a communication cliché. A simulation-based software project study attributed it to underestimation and imprecise measurement caused by poor project visibility. [“Understanding the ‘90% syndrome’ in software project management,” 1988(https://www.sciencedirect.com/science/article/pii/0164121288900155)](https://www.sciencedirect.com/science/article/pii/0164121288900155) **(High Confidence)**

Therefore, the page should not report “percentage complete” except as a clearly labelled, non-authoritative estimate. It should instead use a status ledger:

| Owner-facing state | Meaning | Required evidence |
|---|---|---|
| Not started | Work has not begun | Identified owner and scope |
| In progress | Work exists but is not ready for acceptance | Current artifact or activity |
| Built | Implementation exists | Commit, build, or artifact identifier |
| Tested | Defined tests have passed | Test result and timestamp |
| Deployable | Can be released safely on demand | Release/build evidence |
| Deployed | Running in the named environment | Environment, deployment ID, timestamp |
| Accepted | Owner or acceptance authority has verified the outcome | Acceptance record |
| Blocked | Cannot proceed without a named decision, input, or external dependency | Linked blocker and releasing decision |

DORA defines change lead time as the period from code committed to version control until deployment in production, and distinguishes continuous delivery from continuous deployment. It also asks whether software is in a deployable state throughout its lifecycle and whether it can be deployed at any time. [DORA metrics guide(https://dora.dev/guides/dora-metrics/)](https://dora.dev/guides/dora-metrics/) [DORA, “Continuous delivery”(https://dora.dev/capabilities/continuous-delivery/)](https://dora.dev/capabilities/continuous-delivery/) **(High Confidence)**

<INFERENCE from="Snow, Keil & Wallace 2007; Iacovou, Thompson & Smith 2009; 90% syndrome study 1988; DORA metric definitions">The document should make “built,” “deployable,” “deployed,” and “accepted” visibly different fields. This directly prevents a reassuring implementation status from being mistaken for a usable product.</INFERENCE> **(High Confidence)**

A useful top-of-page summary is:

| Question | Answer format |
|---|---|
| Can the intended user use it today? | Yes / Partly / No / Not evidenced |
| What remains before acceptance? | Three to seven owner-readable outcomes |
| What is blocking progress? | Decision IDs, missing inputs, external dependencies |
| What must the owner decide now? | Number of unresolved blocking decisions |
| What happens after each decision? | Unblocked work and expected consequence |

Release notes are a useful supporting format but not a complete project-status instrument. A mixed-method study examined 32,425 release notes from 1,000 GitHub projects, interviewed 15 practitioners and surveyed 314 respondents. It identified eight information categories and found generally positive perceived impact, but also significant disagreement between stakeholders about how release notes should be written and used. [Bi et al., “An empirical study of release note production and usage in practice,” 2022(https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/)](https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/) **(High Confidence)**

<INSUFFICIENT_EVIDENCE>There is no strong direct study comparing a single self-contained HTML status brief against a dashboard, email, or meeting for one non-technical software owner, using comprehension, decision latency and decision correctness as outcomes.</INSUFFICIENT_EVIDENCE>

#### Plain language and progressive disclosure

A CHI 2024 study found that lower-complexity machine-generated summaries were significantly easier to read, with effect size `d = 0.535`, and easier to understand, with `d = 0.323`, than higher-complexity summaries. [August et al., “Know Your Audience,” CHI 2024(https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf)](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) **(High Confidence)**

The same study found a trade-off: simplified summaries omitted more information, particularly when there were multiple findings or limitations. [August et al., “Know Your Audience,” CHI 2024(https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf)](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) **(High Confidence)**

The document should therefore use:

- a short plain-English explanation in the main flow;
- expandable technical evidence beneath each claim;
- a complete evidence appendix for durable review;
- explicit labels for `observed`, `inferred`, and `unknown`.

Plain language should reduce cognitive load, not remove decision-relevant limitations.

#### Questionnaire design for one expert respondent

Defaults are powerful but not uniformly beneficial. A meta-analysis of 58 default studies involving 73,675 participants found an overall default effect of `d = 0.68`, with a 95% confidence interval of `0.53–0.83`. The majority of studies showed positive effects, but several were null and two were negative. In binary-choice studies, defaults increased selection by an average of 27.24 percentage points. [Jachimowicz et al., “When and why defaults influence decisions,” 2019(https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0)](https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0) **(High Confidence)**

Defaults work through several mechanisms: perceived endorsement, reduced effort, and the tendency to retain an existing state. Their effectiveness varies substantially by domain and decision context. [Jachimowicz et al., 2019(https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0)](https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0) **(High Confidence)**

A 2024 study found that experience can reverse default effects. In a protective-default condition, participants rejected the default on 90% of trials because the alternative produced a higher expected payoff. [“The impact of experience on the tendency to accept recommended defaults,” 2024(https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46)](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46) **(Medium Confidence)**

The design rule is:

> Preselect a recommendation when the recommendation is evidence-backed, reversible, low-risk, and clearly explained. Require explicit confirmation before treating it as a decision. Do not hide the alternatives or make the owner clear a default merely to demonstrate agency.

For material, irreversible, safety-sensitive, legal, financial, or scope-defining decisions, use an active confirmation action such as:

> “I have reviewed this recommendation and confirm it.”

An active-choice randomized trial with 1,279 eligible participants found advance-directive completion of 35.1% in the active-choice group versus 20.4% in control, a 14.7 percentage-point difference. [“Active Choice Intervention Increases Advance Directive Completion,” 2018(https://pmc.ncbi.nlm.nih.gov/articles/PMC6132204/)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6132204/) **(Medium Confidence; transfer from healthcare to software decisions is limited)**

Each decision card should contain:

| Field | Purpose |
|---|---|
| Decision ID | Stable machine-readable identity |
| Plain-English question | The choice the owner must settle |
| Why this is needed now | Immediate blocker |
| Recommendation | Preselected option and rationale |
| Alternatives | At least the viable alternatives, not a token “other” |
| Consequences | What changes for cost, scope, time, risk, or users |
| Unblocks | Work released by this answer |
| Evidence | Links to source claims and project artifacts |
| Answer control | Radio, checkbox, numeric field, or explicit skip |
| Optional note | Caveat, condition, exception, or context |
| Confirmation action | Explicitly records review and decision |

Use radio buttons for mutually exclusive choices and checkboxes only where multiple options genuinely compose. Do not use a multi-select control to conceal an unresolved trade-off.

Optional notes should never substitute for the structured answer. Open-text questions have materially higher nonresponse than structured items; one 2024 study reported written final-comment nonresponse of 55.8%. [Höhne & Claassen, “Examining final comment questions,” 2024(https://doi.org/10.1177/14707853241229329)](https://doi.org/10.1177/14707853241229329) **(Medium Confidence; population survey evidence)**

The export should distinguish:

- unanswered;
- intentionally skipped;
- default left unchanged;
- explicitly accepted recommendation;
- explicitly overridden;
- needs clarification.

A blank note means “no note supplied,” not “no caveat exists.”

#### Ordering, batching and dependency visibility

A decision should be shown in the context of the work it releases:

> **D-004: Choose the supported payment provider**  
> Blocks: checkout integration, end-to-end test, production launch  
> If confirmed: implementation can begin  
> If unanswered: launch remains blocked  
> Recommendation: Provider A  
> Basis: existing account, tested integration, lower migration cost

Formal requirements-prioritization research shows that dependencies are often omitted from stakeholder prioritization, even though direct and transitive dependencies determine implementation order. DRank combines stakeholder preferences with dependency extraction; CDBR models execute-before-after relationships and dependency propagation. [DRank, “A semi-automated requirements prioritization method,” 2017(https://doi.org/10.1016/j.jss.2016.09.043)](https://doi.org/10.1016/j.jss.2016.09.043) [CDBR, “Dependency-based requirement prioritization,” 2019(https://link.springer.com/article/10.1016/j.jksuci.2018.10.004)](https://link.springer.com/article/10.1016/j.jksuci.2018.10.004) **(Medium Confidence; the underlying studies are technical rather than owner-facing)**

Information has value only when it changes an actionable decision. NIST’s value-of-information framework explicitly compares the benefit of acquiring information with its cost and frames decisions as pathways with consequential actions. [NIST, “Value of information and decision pathways,” 2022(https://www.nist.gov/publications/value-information-and-decision-pathways-concepts-and-case-studies)](https://www.nist.gov/publications/value-information-and-decision-pathways-concepts-and-case-studies) **(High Confidence)**

<INFERENCE from="NIST value-of-information framework; DRank; CDBR">Order decision cards using a visible “why now” rule: downstream consequence, owner effort, reversibility, and whether the answer releases critical-path work. A defensible heuristic is `downstream importance × urgency ÷ decision effort`, but this exact formula is not empirically validated for software owners.</INFERENCE> **(Medium Confidence)**

Do not display one global rank for every decision. Ranking information changes attention: an experiment found that rank information affected preferences beyond the underlying ratings and caused attention to concentrate on top-ranked items. [Chun et al., “The Power of Rank Information,” 2021(https://doi.org/10.1037/pspa0000289)](https://doi.org/10.1037/pspa0000289) **(High Confidence)**

Conversely, an interactive decision-search experiment found that sorting by one category did not improve search outcomes, while showing relative rank across attributes improved search. [“An experimental study of the decision process with interactive technology,” 2016(https://doi.org/10.1016/j.jebo.2016.06.004)](https://doi.org/10.1016/j.jebo.2016.06.004) **(Medium Confidence)**

Use dependency groups instead:

- **Must decide to release work**
- **Changes scope or user promise**
- **Reduces operational or security risk**
- **Can wait without blocking completion**
- **Needs more evidence before a decision is safe**

Within each group, show one recommended next decision and its downstream effects. The owner should be able to see why a decision is first without interpreting the ordering as objective truth.

#### Asynchronous decision instruments

Written decision instruments have useful evidence, but little of it directly matches this exact use case.

A field experiment comparing face-to-face and asynchronous group decision-making found that asynchronous groups produced broader discussions and more complete reports, while both conditions omitted approximately 15% of issues. [“A comparative content analysis of face-to-face vs asynchronous group decision making,” 2003(https://doi.org/10.1016/S0167-9236(02)00072-6)](https://doi.org/10.1016/S0167-9236(02)00072-6) **(Medium Confidence; group evidence, not single-owner evidence)**

An observational healthcare study found that asynchronous communication reduced task completion time by an average of 20.1 minutes, or 58.8%, compared with existing communication methods. [“Examining the impact of an asynchronous communication platform,” 2021(https://pmc.ncbi.nlm.nih.gov/articles/PMC7808296/)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7808296/) **(Low Confidence for software transfer)**

Architecture Decision Record research is more cautious. A 2023 action-research study found that teams perceived ADRs as useful, but reported challenges involving culture, tacit knowledge, process, tool support, appropriate detail, prioritization, placement and maintenance. [Ahmeti, Linder & Wohlrab, “Exploring the Adoption and Effectiveness of Architecture Decision Records,” 2023(https://research.chalmers.se/en/publication/538920)](https://research.chalmers.se/en/publication/538920) **(Medium Confidence)**

The document should therefore function as both:

- an asynchronous decision brief for the owner;
- a compact ADR-like record after confirmation.

Each confirmed decision should automatically retain context, alternatives, rationale, consequences, evidence and timestamp. A meeting may still be useful for exceptional ambiguity, but the page should make a meeting unnecessary for ordinary blocking choices.

#### Machine-readable round-trip and safe agent action

Use W3C PROV concepts for provenance: entities, activities and agents, with relationships such as `used`, `wasGeneratedBy`, `wasInformedBy` and `wasDerivedFrom`. [W3C PROV Primer(https://www.w3.org/TR/prov-primer/)](https://www.w3.org/TR/prov-primer/) [W3C PROV-O(https://www.w3.org/TR/prov-o/)](https://www.w3.org/TR/prov-o/) **(High Confidence)**

Validate the export against a strict JSON Schema with enumerated states and rejected unknown fields. JSON Schema supports object constraints and controlled structural validation, but schema validation alone cannot establish that a decision is wise or that a caveat was understood. [JSON Schema object reference(https://json-schema.org/understanding-json-schema/reference/object)](https://json-schema.org/understanding-json-schema/reference/object) **(High Confidence)**

A minimum export should look like this:

```json
{
  "schema_version": "1.0",
  "document": {
    "id": "project-status-2026-08-12",
    "generated_at": "2026-08-12T00:00:00Z",
    "source_snapshot": {
      "captured_at": "2026-08-11T23:00:00Z",
      "content_hash": "sha256:...",
      "evidence_refs": ["SRC-001", "SRC-002"]
    }
  },
  "decisions": [
    {
      "id": "D-004",
      "type": "single_select",
      "question": "Which payment provider should launch support?",
      "options": [
        {"id": "provider_a", "label": "Provider A"},
        {"id": "provider_b", "label": "Provider B"}
      ],
      "recommendation": {
        "option_id": "provider_a",
        "basis_refs": ["PROJ-ARTIFACT-17", "SRC-009"]
      },
      "answer": {
        "selected_option_ids": ["provider_a"],
        "raw_value": "provider_a"
      },
      "answer_status": "default_left_unchanged",
      "selection_origin": "default",
      "confirmation": {
        "explicit": false,
        "event_id": null,
        "confirmed_at": null
      },
      "notes": [
        {
          "raw_text": "Use Provider B if international expansion is brought forward.",
          "kind": "condition",
          "actionability": "requires_review"
        }
      ],
      "unblocks": [
        {
          "item_id": "WORK-021",
          "relation": "direct",
          "consequence": "Begin checkout integration"
        }
      ],
      "scope": {
        "applies_to": "launch_v1",
        "expires_at": null,
        "review_trigger": "international_expansion"
      },
      "agent_policy": {
        "allowed_actions": ["start_checkout_integration"],
        "approval_required": true,
        "forbidden_actions": ["change_provider_contract"]
      }
    }
  ],
  "events": [
    {
      "type": "page_loaded",
      "decision_id": "D-004",
      "at": "2026-08-12T00:05:00Z"
    }
  ]
}
```

The required distinction is:

| Export state | Meaning | Agent action |
|---|---|---|
| `unanswered` | Owner has not answered | Ask or wait |
| `skipped` | Owner intentionally deferred | Preserve blocker |
| `default_left_unchanged` | Recommendation remained selected without explicit confirmation | Do not execute material action |
| `explicitly_confirmed` | Owner explicitly accepted the selected answer | Act within policy |
| `explicitly_overridden` | Owner explicitly chose another answer | Act within policy, preserving override |
| `needs_clarification` | Answer or caveat is ambiguous or conditional | Ask a targeted follow-up |

Agent benchmarks document weaknesses in long-horizon reasoning, decision-making and instruction following. AgentBench evaluated 29 models across eight environments and identified these as major obstacles. [AgentBench, ICLR 2024(https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html)](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html) **(High Confidence)**

NIST’s agent-evaluation work explicitly tests citation faithfulness, citation completeness and citation sufficiency, and produces a structured audit trail. [NIST, “Building Evaluation Probes for Agentic AI,” 2026(https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai)](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) **(High Confidence)**

<INFERENCE from="W3C PROV; JSON Schema; AgentBench; NIST agentic evaluation">The agent must never infer confirmation from selection alone, never discard raw notes after extracting a summary, and never execute an irreversible action when a caveat is conditional, blocking, stale or unparsed. It should validate the document hash, schema, option IDs, answer state, scope and action policy before acting.</INFERENCE> **(High Confidence)**

The most important failure cases to test are:

- terse answer interpreted as unconditional;
- caveat stored but ignored;
- default mistaken for explicit consent;
- decision applied outside its scope;
- stale answer applied to a changed project snapshot;
- multi-select interpreted as an ordered preference;
- “yes” applied to the wrong decision ID;
- unsupported agent summary replacing the owner’s raw note.

#### Integrity of AI-generated status artefacts

NIST defines confabulation as confidently presented erroneous or false content, including fabricated logic or citations that can mislead users. [NIST, Generative AI Risk Management Profile, 2024(https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) **(High Confidence)**

A CHI study likewise states that no automated method guarantees factual accuracy or fidelity in plain-language generation. In its experiment, 14 of 120 generated summaries contained incorrect information; the correct replacement was found within at most six alternatives, with an average of 2.36 generations. [August et al., CHI 2024(https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf)](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) **(High Confidence)**

A 2025 Nature Machine Intelligence study found that users can overestimate model accuracy when explanations are provided by default; longer explanations increased confidence without necessarily improving accuracy, while uncertainty-aligned explanations improved calibration. [“What large language models know and what people think they know,” 2025(https://www.nature.com/articles/s42256-024-00976-7)](https://www.nature.com/articles/s42256-024-00976-7) **(High Confidence)**

The honesty contract should be:

- every status claim has a source reference, source timestamp and verification state;
- every claim is classified as `observed`, `inferred`, or `unknown`;
- “complete” requires named acceptance evidence;
- an absent source produces “not evidenced,” never a guessed status;
- generated prose cannot overwrite the underlying status ledger;
- citations open to durable source snapshots, not only live URLs;
- the export records the hash of the snapshot from which the document was generated.

NIST’s newer agentic-evaluation approach is a useful model: test whether sources support claims, whether relevant evidence was omitted, and whether the sources are sufficient for the conclusion. [NIST agentic evaluation probes(https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai)](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) **(High Confidence)**

#### Accessibility, printing and self-containment

The HTML should be a single offline-capable file with inline CSS and JavaScript, no CDN dependencies, no remote fonts, no external images and no required network request.

Use semantic headings, landmarks, tables, `fieldset`/`legend`, labels, keyboard navigation, visible focus, and text labels in addition to color. WCAG 2.2 requires, at Level AA, a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text, and requires content to remain usable when text is resized to 200%. [W3C Web Content Accessibility Guidelines 2.2(https://www.w3.org/TR/WCAG22/)](https://www.w3.org/TR/WCAG22/) **(High Confidence)**

Every control needs an explicit label association; W3C’s forms guidance recommends programmatically associating labels with their controls. [W3C WAI, “Labels,”(https://www.w3.org/WAI/tutorials/forms/labels/)](https://www.w3.org/WAI/tutorials/forms/labels/) **(High Confidence)**

Use print-specific CSS for page size, margins, page breaks and print-only elements. CSS Paged Media defines page layout controls, while Media Queries support print-targeted styling. [CSS Paged Media Module(https://www.w3.org/TR/css-page-3/)](https://www.w3.org/TR/css-page-3/) [Media Queries Level 3(https://www.w3.org/TR/mediaqueries-3/)](https://www.w3.org/TR/mediaqueries-3/) **(High Confidence)**

Print output should include:

- project identity and source-snapshot hash;
- all unresolved blockers;
- selected answers and answer states;
- raw notes and caveats;
- confirmation timestamp;
- export instructions or an embedded JSON text appendix.

`localStorage` may improve convenience but must not be the only persistence mechanism. The durable record is the saved HTML plus exported JSON.

<MISSING_DATA>Cross-browser behavior, screen-reader behavior, PDF pagination, offline file restrictions and keyboard completion rates require testing in the target browser and assistive-technology matrix. Standards compliance alone does not establish usability.</MISSING_DATA>

#### Implementation-pattern comparison

No model, provider or hosting target was specified, so model parameter counts, context windows, latency, cost and licenses cannot be filled defensibly.

| Implementation pattern | Parameter Count | Context Window | Latency | Cost | License/Portability | Fit |
|---|---:|---:|---:|---:|---|---|
| Static self-contained HTML + vanilla JavaScript | N/A | N/A | Local; measure on target devices | Zero runtime API cost | Highly portable; standards-based | Best durable decision record |
| Generate once from a verified project snapshot, then freeze HTML | Model-specific | Model-specific | Generation-time only; `<MISSING_DATA>` | `<MISSING_DATA>`; provider/model unspecified | Depends on chosen model | Best balance of automation and auditability |
| Remote interactive agent with JSON export | `<MISSING_DATA>` | `<MISSING_DATA>` | Network- and model-dependent | Hosting plus model usage; `<MISSING_DATA>` | Provider-dependent | Useful for preparation and follow-up |
| Client-side model embedded in HTML | `<MISSING_DATA>` | `<MISSING_DATA>` | Device-dependent | Model distribution and compute cost | License and browser support uncertain | Avoid for core status truth |
| Static HTML with server-side action executor | N/A for page; executor-specific | Executor-specific | Action/API-dependent | Infrastructure-dependent | Must define API and authorization | Suitable only behind explicit confirmation gates |

## 2. What is the current state, and what is the strongest supporting evidence for it?

The strongest current position is a hybrid:

- structured state ledgers outperform vague narrative for truthfulness;
- plain-language summaries improve comprehension but can omit limitations;
- defaults improve completion in many settings but can impair decisions when the recommendation is protective, unfamiliar, irreversible or poorly matched;
- dependency-aware ordering is technically well established but weakly tested for nontechnical owner comprehension;
- asynchronous records improve durability and can improve coverage, but direct evidence for one-owner software decisions is sparse;
- provenance and auditability are becoming explicit requirements for agentic systems;
- AI-generated status should be treated as probabilistic synthesis requiring evidence checks.

The most direct evidence is stronger for component behaviors than for the complete product pattern. Defaults, plain-language summaries, provenance, status bias and agent instruction failures have substantial evidence. The exact combination—single-file HTML, one nontechnical owner, blocker-linked questionnaire, preselected recommendations and safe JSON round-trip—does not yet have a mature empirical literature.

<INSUFFICIENT_EVIDENCE>The field lacks a benchmark dataset measuring one owner’s comprehension, decision quality, latency, completion rate and later correction rate across status formats.</INSUFFICIENT_EVIDENCE>

The practical design should therefore be evidence-constrained rather than evidence-claimed: use known behavioral effects, explicitly label inferences, and instrument the product for validation.

## 3. What are the contrasting viewpoints or competing evidence?

**Defaults versus active choice.** The default meta-analysis shows a large average effect, but the 2024 evidence demonstrates that defaults can reverse when people understand the payoff structure. The correct compromise is a visible recommendation with an explicit acceptance event. <CONFLICTING_EVIDENCE>Defaults often increase completion and selection, but can reduce decision quality when the default is poorly matched, protective, irreversible or insufficiently understood.</CONFLICTING_EVIDENCE>

**Plain language versus completeness.** Simpler summaries improve readability and understanding, but may omit limitations and secondary findings. The page should use progressive disclosure rather than choosing either extreme. [August et al., CHI 2024(https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf)](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) **(High Confidence)**

**Ranking versus grouping.** Rank information attracts attention to the top option, which can speed selection but can also suppress consideration of alternatives. Choice-overload research finds that overload depends on set complexity, task difficulty, preference uncertainty and the decision-maker’s goal; a 2015 meta-analysis covered 99 observations and 7,202 participants. [Chernev, Böckenholt & Goodman, “Choice overload,” 2015(https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2014.08.002)](https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2014.08.002) **(High Confidence)**

An older meta-analysis found little average choice-overload effect, indicating that overload is conditional rather than universal. <CONFLICTING_EVIDENCE>The evidence supports controlling complexity and uncertainty, but does not justify a universal maximum number of choices or a universal “rank everything” rule.</CONFLICTING_EVIDENCE>

**Async versus synchronous decisions.** Asynchronous records can provide broader written coverage and durable rationale, but may leave ambiguity unresolved and lack the immediate repair mechanism of conversation. ADR evidence is currently mostly action research and perception-based rather than controlled measurement of decision latency or quality. [Ahmeti, Linder & Wohlrab, 2023(https://research.chalmers.se/en/publication/538920)](https://research.chalmers.se/en/publication/538920) **(Medium Confidence)**

**AI explanation versus calibrated trust.** More explanation is not automatically more truthful or better calibrated. The document should show evidence and uncertainty, not merely produce longer prose. [Nature Machine Intelligence study, 2025(https://www.nature.com/articles/s42256-024-00976-7)](https://www.nature.com/articles/s42256-024-00976-7) **(High Confidence)**

## 4. What changed recently, and what is the trajectory?

From 2019 onward, default research moved from asking whether defaults work to asking when they reverse, how experience changes them and whether the default is genuinely beneficial. [Jachimowicz et al., 2019(https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0)](https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0) [Judgment and Decision Making study, 2024(https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46)](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46) **(High Confidence)**

During the same period, software documentation research increasingly examined release-note usefulness and stakeholder disagreement rather than treating documentation as a single audience problem. [Bi et al., 2022(https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/)](https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/) **(High Confidence)**

Since 2024, authoritative AI guidance has emphasized confabulation, citation faithfulness, citation completeness, provenance and audit trails. NIST’s 2026 agentic-evaluation work is especially close to the required round-trip: it evaluates whether cited sources actually support claims and whether evidence is sufficient. [NIST Generative AI Profile, 2024(https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) [NIST agentic evaluation probes, 2026(https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai)](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) **(High Confidence)**

<INFERENCE from="NIST GenAI Profile 2024; Nature Machine Intelligence 2025; NIST agentic probes 2026; W3C PROV">The trajectory is from “AI-generated status narrative” toward evidence-linked, provenance-preserving, auditable decision artifacts. A product designed now should assume that source traceability and explicit uncertainty will become normal requirements for agent-mediated work.</INFERENCE> **(Medium Confidence)**

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL | Source-discipline fit |
|---|---|---:|---|---|---|
| Status reports are frequently biased; optimism is common | Snow, Keil & Wallace | 2007 | Peer-reviewed empirical study and model | [Source](https://www.sciencedirect.com/science/article/abs/pii/S0378720606001145) | Direct software-project status research |
| Selective reporting degrades project reporting quality | Iacovou, Thompson & Smith | 2009 | Peer-reviewed survey study of 561 managers | [Source](https://aisel.aisnet.org/misq/vol33/iss4/11/) | Direct information-systems evidence |
| “90% syndrome” arises from poor visibility and imprecise measurement | Journal of Systems and Software study | 1988 | Simulation-based software case study | [Source](https://www.sciencedirect.com/science/article/pii/0164121288900155) | Direct software-project evidence |
| Built, deployable and deployed are distinct states | DORA | Current documentation | Official engineering/research guidance | [Metrics](https://dora.dev/guides/dora-metrics/), [CD](https://dora.dev/capabilities/continuous-delivery/) | Authoritative operational definitions; vendor-affiliated caveat |
| Release notes have multiple audiences and stakeholder disagreement | Bi et al. | 2022 | Mixed-method peer-reviewed empirical study | [Source](https://research.monash.edu/en/publications/an-empirical-study-of-release-note-production-and-usage-in-practi/) | Direct software documentation research |
| Plain-language summaries improve readability and understanding | August et al. | 2024 | CHI experiments | [Paper](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) | Peer-reviewed human-computer interaction research |
| Simplification can omit limitations and findings | August et al. | 2024 | CHI experiment | [Paper](https://wildlab.cs.washington.edu/Publications_files/August_CHI2024.pdf) | Direct evidence on machine-generated summaries |
| Defaults have a large average effect but variable direction | Jachimowicz et al. | 2019 | Peer-reviewed meta-analysis; 58 studies, 73,675 participants | [Source](https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0) | Strong decision-science synthesis |
| Experience can reverse default effects | Judgment and Decision Making study | 2024 | Peer-reviewed preregistered experiments | [Source](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/impact-of-experience-on-the-tendency-to-accept-recommended-defaults/48A391D40E7A5A54347BFDC757240F46) | Direct experimental evidence |
| Active confirmation can increase completion | Active-choice randomized trial | 2018 | Randomized controlled trial | [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC6132204/) | Strong causal evidence, but healthcare transfer |
| Question format changes selection and satisficing | Pew Research Center | 2019 | Randomized survey experiment; 4,581 adults | [Source](https://www.pewresearch.org/methods/2019/05/09/when-online-survey-respondents-only-select-some-that-apply/) | Original research; limited transfer to one owner |
| Forced answering and explicit nonresponse can increase missingness | Kmetty & Stefkovics | 2021 | Online questionnaire experiment | [Source](https://www.tandfonline.com/doi/full/10.1080/13645579.2021.1929714) | Original methods research; limited transfer |
| Rank information changes attention and preference | Chun et al. | 2021 | Peer-reviewed experiments | [DOI](https://doi.org/10.1037/pspa0000289) | Direct decision-presentation evidence |
| Choice overload is conditional | Chernev, Böckenholt & Goodman | 2015 | Meta-analysis; 99 observations, 7,202 participants | [Source](https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2014.08.002) | Strong synthesis; not software-specific |
| Dependencies affect implementation ordering | DRank and CDBR studies | 2017–2019 | Peer-reviewed software-engineering methods and experiments | [DRank](https://doi.org/10.1016/j.jss.2016.09.043), [CDBR](https://link.springer.com/article/10.1016/j.jksuci.2018.10.004) | Direct technical dependency research |
| Information should be evaluated by decision value and acquisition cost | NIST | 2022 | Government research framework | [Source](https://www.nist.gov/publications/value-information-and-decision-pathways-concepts-and-case-studies) | Authoritative decision-analysis source |
| Async communication can improve written coverage but has trade-offs | Decision-support and healthcare studies | 2003–2021 | Field experiment and observational study | [2003](https://doi.org/10.1016/S0167-9236(02)00072-6), [2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7808296/) | Primary studies; transfer explicitly limited |
| ADR adoption is useful but empirically undermeasured | Ahmeti, Linder & Wohlrab | 2023 | Action research | [Source](https://research.chalmers.se/en/publication/538920) | Direct software-architecture research |
| Decision aids improve knowledge and reduce decisional conflict | Cochrane review | 2024 | Systematic review; 107 studies for knowledge outcome | [PubMed](https://pubmed.ncbi.nlm.nih.gov/38284415/) | High-quality synthesis, healthcare transfer |
| Provenance should record entities, activities and agents | W3C | Current standard | International technical standard | [PROV Primer](https://www.w3.org/TR/prov-primer/), [PROV-O](https://www.w3.org/TR/prov-o/) | Authoritative interoperability standard |
| Agents fail at long-horizon reasoning and instruction following | AgentBench | 2024 | Peer-reviewed benchmark across 29 models and eight environments | [ICLR paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html) | Direct benchmark evidence |
| AI can confidently produce false content and fabricated citations | NIST | 2024 | Government risk profile | [PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Authoritative AI-risk source |
| Users can be overconfident in AI-generated explanations | Nature Machine Intelligence study | 2025 | Peer-reviewed human-model calibration study | [Source](https://www.nature.com/articles/s42256-024-00976-7) | Direct trust-calibration evidence |
| Citation faithfulness, completeness and sufficiency can be evaluated | NIST | 2026 | Government evaluation framework | [Source](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) | Current authoritative agent-evaluation source |
| Accessible forms require labels and sufficient contrast | W3C | Current standards | WCAG and WAI guidance | [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Form labels](https://www.w3.org/WAI/tutorials/forms/labels/) | Authoritative accessibility standards |
| Print layout can be controlled with paged-media CSS | W3C | Current standards | CSS standards | [Paged Media](https://www.w3.org/TR/css-page-3/), [Media Queries](https://www.w3.org/TR/mediaqueries-3/) | Authoritative web-platform standards |

## Knowledge Gaps

**Direct product evidence**

< MISSING_DATA >No controlled study was found for the complete target artifact: a single self-contained HTML status-and-decision page used by one nontechnical software owner in one sitting.</MISSING_DATA>

Needed measures include comprehension, time to first correct decision, completion rate, decision reversals, clarification requests, missed caveats and agent execution errors.

**Default and recommendation evidence**

<INSUFFICIENT_EVIDENCE>Existing default studies do not establish the optimal presentation of a software recommendation where the respondent is the project owner and the recommendation is generated from project evidence.</INSUFFICIENT_EVIDENCE>

Needed evidence compares blank forms, visible defaults, visible recommendations and explicit active-confirmation flows using decisions with known correct or preferred outcomes.

**Dependency ordering**

<INSUFFICIENT_EVIDENCE>Technical requirements-prioritization research supports dependency graphs, but does not establish whether nontechnical owners understand or prefer critical-path, effort-adjusted, value-adjusted or grouped ordering.</INSUFFICIENT_EVIDENCE>

**Asynchronous decision quality**

<INSUFFICIENT_EVIDENCE>Evidence supports durability and broader written coverage, but direct measurements of decision latency, quality and completion for software owners using RFC/ADR-style self-serve forms are scarce.</INSUFFICIENT_EVIDENCE>

**AI-generated status trust**

Current studies establish hallucination, overconfidence and citation-quality risks, but not how owners calibrate trust in a project-completion report containing source-linked evidence and explicit unknowns.

**Accessibility and printing**

<MISSING_DATA>Target-browser, screen-reader, keyboard-only, offline-file, print-to-PDF and large-document performance remain implementation questions requiring testing rather than literature review.</MISSING_DATA>

## Recommended Next Steps

1. **Run a task-based usability study with representative nontechnical owners.** Measure whether participants can identify what remains, find the highest-impact blocker, and complete the export without assistance.

2. **Compare four answer states experimentally:** blank, preselected recommendation, preselected recommendation with rationale, and recommendation plus explicit confirmation. Measure completion, override rate, correctness, time, later regret and caveat recall.

3. **Test dependency ordering against global ranking.** Compare blocker-linked groups, critical-path order, effort-adjusted order and unranked chronological order. Measure decision latency, missed dependencies and unnecessary deferrals.

4. **Build an adversarial JSON round-trip test suite.** Include defaults left untouched, terse answers, contradictory notes, conditional caveats, stale source snapshots, multi-select ambiguity and unknown option IDs. The agent must abstain or ask for clarification whenever the export is not action-safe.

5. **Perform a standards and real-device accessibility pass.** Test keyboard navigation, screen readers, contrast, zoom, print pagination, offline opening, JSON download, reload recovery and `noscript` behavior before treating the HTML as a durable project record.
