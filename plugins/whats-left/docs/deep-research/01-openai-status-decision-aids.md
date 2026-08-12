---
title: "Designing software project status and decision aids for non-technical owners"
run_id: dr_5cdf910fb86f38c8
question: "How should a status-and-decision document be designed so that a single non-technical owner can, in one sitting, understand what remains before a software project is complete and settle every decision that is blocking the work? Cover, with evidence and measured results where they exist: (1) how practitioners today communicate remaining work and project state to a non-technical decision-maker — the formats that measurably improve comprehension and decision speed, and the documented failure modes of status reporting (status flattering / watermelon reporting, optimism and planning-fallacy bias, \"90% done\" syndrome, ambiguity about what is genuinely deployed versus merely built); (2) decision-elicitation and questionnaire design for a single expert respondent rather than a survey population — the measured effects of pre-selected defaults and pre-filled recommendations on answer quality and anchoring, when a default improves versus degrades the decision, optional free-text notes and non-response, satisficing, question ordering and batching, and how to distinguish an actively-confirmed answer from one merely left as found; (3) how blocking dependencies and critical path are best surfaced to a non-specialist — showing what a single decision unblocks, sequencing by cheapest-high-payoff, and evidence on whether ranked or grouped presentation produces better decisions; (4) asynchronous decision instruments in place of meetings — what evidence exists on decision latency, quality, and completion rates for written decision briefs, RFC/ADR-style decision records, and self-serve decision forms; (5) machine-readable round-trip of human decisions — schema design for capturing an answer plus its provenance, confidence and free-text caveats so an automated agent can act on it safely, and the documented failure modes of agents acting on human answers (over-reading a terse answer, ignoring an attached caveat, treating a default as a decision); (6) failure modes and integrity of AI-generated project status artefacts specifically — fabricated or unverifiable completeness claims, provenance and citation practices, and what is known about how readers calibrate trust in machine-written status reports; and (7) accessibility, print and self-containment constraints for a single-file HTML document used as a durable decision record. Exclude general agile ceremony advocacy, vendor project-management tool marketing, and large-population survey methodology that does not transfer to a single respondent."
provider: openai
model: gpt-5.6-sol
tier: max
archetype: technical
sources: 47
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 9.00
completed: 2026-08-12T08:20:07.698Z
---
## Executive Summary

- **(High Confidence)** <INFERENCE from="GAO schedule guidance; NISTA delivery-confidence guidance; DORA production metrics">Use **two synchronized registers in one page**: an evidence-backed remaining-work register and an explicit decision register. Do not summarize the project with a single percentage or traffic light. For every required outcome, distinguish *built*, *tested*, *deployed to production*, *operationally verified*, and *owner accepted*; show the status date, remaining action, evidence, owner, and blocker.</INFERENCE> [gao.gov](https://www.gao.gov/products/gao-16-89g) [gov.uk](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26) [dora.dev](https://dora.dev/guides/dora-metrics/) ([gao.gov](https://www.gao.gov/products/gao-16-89g))

- **(High Confidence)** Recommendations may be pre-populated only as **unconfirmed proposals**, never as decisions. A meta-analysis of 58 default studies with 73,675 participants found a substantial average default effect, \(d=0.68\), with wide variation and two negative effects; defaults are also commonly interpreted as endorsement. <INFERENCE from="default-effect evidence">The page should visibly separate “Recommended by the project/agent” from “Confirmed by the owner.” A checked recommendation must remain non-actionable until the owner performs a separate confirmation action.</INFERENCE> [doi.org](https://doi.org/10.1017/S2398063X1800043X) [flex.uni-frankfurt.de](https://flex.uni-frankfurt.de/index.php/publications/communicating-through-defaults/) ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html))

- **(High Confidence)** <INFERENCE from="WHATWG form-state semantics; default-effect evidence">Use four explicit decision states: `unanswered`, `draft/proposed`, `confirmed`, and `deferred/needs_clarification`. Changing an answer after confirmation must automatically return it to `draft`. Browser checkedness or interaction logs are insufficient proof of informed confirmation.</INFERENCE> [html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/input.html) ([html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/input.html))

- **(High Confidence)** Every blocker and decision needs stable IDs and bidirectional links. A work item should say `blocked_by: [D-04]`; decision `D-04` should identify the work it releases and whether it **fully releases**, **removes one blocker**, or merely **enables planning**. Critical-path impact must be shown separately from raw “number of tasks unblocked.” [gao.gov](https://www.gao.gov/products/gao-16-89g) ([gao.gov](https://www.gao.gov/products/gao-16-89g))

- **(Medium Confidence)** <INFERENCE from="simultaneous-choice experiments; choice-architecture experiments">Use both grouping and ranking: group decisions by owner-visible outcome, then rank within each group by critical-path impact, time sensitivity, reversibility, answer effort, and unblock fan-out. Present the alternatives for one decision simultaneously, not sequentially or in a dense matrix. Start with one low-effort/high-payoff decision when available, then address irreversible and critical-path choices while attention is still high.</INFERENCE> [doi.org](https://doi.org/10.1016/j.obhdp.2017.01.004) [doi.org](https://doi.org/10.1287/deca.2018.0379) [doi.org](https://doi.org/10.1177/00222429221119086) ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0749597816302060))

- **(Medium Confidence)** Written decision aids have strong cross-domain evidence for improving knowledge and values-congruent choices, but direct evidence that RFCs, ADRs, or owner forms reduce software decision latency is sparse. <INFERENCE from="decision-aid and communication evidence">Use the HTML page asynchronously for bounded, single-owner decisions with known options; escalate to speech when disagreement, emotional conflict, unclear authority, or genuinely novel trade-offs emerge.</INFERENCE> [cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening) [nature.com](https://www.nature.com/articles/s41467-026-71669-5) ([cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening))

- **(High Confidence)** The JSON export must fail closed. It must separately record the recommendation, draft UI state, confirmed answer, answer origin, respondent authority, timestamps, confidence types, caveats, blocker links, execution limits, schema version, evidence provenance, and integrity hashes. An agent may act only on an explicitly confirmed answer whose authority, revision, conditions, caveats, and execution policy all validate. [json-schema.org](https://json-schema.org/draft/2020-12) [w3.org](https://www.w3.org/TR/prov-o/) [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc8785.html) ([json-schema.org](https://json-schema.org/draft/2020-12))

- **(High Confidence)** AI-generated project artefacts cannot honestly guarantee truth merely by sounding precise or including citations. NIST identifies generative-AI confabulation as a core risk; a 2023 citation benchmark found that even its best tested models lacked complete citation support 50% of the time on ELI5; readers shown ordinary LLM explanations were only slightly better than chance at distinguishing correct from incorrect answers in several conditions, with AUCs of 0.589–0.602. <INFERENCE from="AI reliability and trust-calibration evidence">Every material status claim therefore needs claim-level provenance, an epistemic label, a status date, and evidence that can be checked independently of the prose.</INFERENCE> [doi.org](https://doi.org/10.6028/NIST.AI.600-1) [aclanthology.org](https://aclanthology.org/2023.emnlp-main.398/) [doi.org](https://doi.org/10.1038/s42256-024-00976-7) ([nist.gov](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence))

---

## Detailed Findings

### 1. How should a status-and-decision document be designed so that a single non-technical owner can, in one sitting, understand what remains before a software project is complete and settle every decision that is blocking the work?

### 1.1 Decisive design: the page anatomy

**(High Confidence)** <INFERENCE from="project schedule guidance, decision-aid evidence, form standards, and provenance standards">The artefact should be a **decision aid with a status model**, not a status dashboard with a questionnaire appended. Its one-page reading order should be:</INFERENCE>

| Page section | Required content | Non-negotiable rule | Confidence |
|---|---|---|---|
| **1. Header and completion contract** | Project, status-as-of timestamp, scope version, definition of “complete,” source freshness, AI/human authorship | “Complete” must be defined before any completion claim is shown. | High |
| **2. Bottom line** | Plain-English statement of what works now, what does not, earliest credible finish condition, number of owner decisions still blocking work | Separate delivery state, schedule confidence, quality, and owner blockage rather than compressing them into one color. | High |
| **3. Outcome/completion matrix** | Each required owner-visible outcome across `unknown → in progress → built → tested → deployed → operationally verified → accepted` | `Built` and `deployed` are never synonyms. | High |
| **4. Remaining-work register** | Work ID, outcome, remaining action, why it matters, evidence, owner, dependencies, decision blockers, forecast range and assumptions | No subjective “90% done” field without a defined denominator and remaining duration. | High |
| **5. Decision queue** | One card per decision: question, recommendation, options, trade-offs, confidence, what it releases, reversibility, cost/risk boundaries, notes and confirmation | Recommendation and owner answer remain separate data objects. | High |
| **6. Final review** | Confirmed, changed, deferred, and unresolved decisions; work still blocked after those decisions | The page must not say “all blockers settled” while any required decision is unconfirmed. | High |
| **7. Export and durable record** | JSON validation result, hashes, export timestamp, downloadable JSON, optional completed-HTML snapshot and print summary | Agent action is prohibited if validation or authority checks fail. | High |

The schedule/status basis is consistent with GAO guidance requiring actual and planned dates, remaining duration, a status date, and maintained schedule logic. [gao.gov](https://www.gao.gov/products/gao-16-89g) ([gao.gov](https://www.gao.gov/products/gao-16-89g))

### 1.2 Communicating remaining work honestly

| Failure mode | Supporting evidence | Concrete design rule | Confidence |
|---|---|---|---|
| **Watermelon reporting: green outside, red underneath** | A local-government audit account documented a roadmap whose RAG summary oversimplified conditions and described one project as a “watermelon.” This is evidence of the failure mode, not a prevalence estimate. [algaonline.org](https://algaonline.org/page/2020_Summer_Lin_Harvey) ([algaonline.org](https://algaonline.org/page/2020_Summer_Lin_Harvey)) | <INFERENCE from="audit case and NISTA limits on RAG">Never let a manually selected RAG rating stand alone. Show the rule, evidence, unresolved critical blockers, and any management override with actor and reason.</INFERENCE> | Medium |
| **RAG conflates risk, progress and completion** | NISTA says its Delivery Confidence Assessment is not a comprehensive reflection of project performance and is only a snapshot assuming current risks and issues remain unchanged. [gov.uk](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26) ([gov.uk](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26)) | Show separate fields for delivery stage, schedule confidence, quality/acceptance, production state, and decision blockage. | High |
| **Optimism and planning-fallacy bias** | The 2026 UK Green Book describes optimism bias as a systematic tendency to understate costs and duration and overstate benefits, and requires explicit adjustments based on historical forecast errors or reference-class evidence. [gov.uk](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026) ([gov.uk](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026)) | Show forecasts as ranges with assumptions, reference class, and confidence. Keep the original baseline visible beside the current forecast. | High |
| **“90% done” or subjective percent complete** | GAO guidance emphasizes remaining duration, status dates and objective schedule updates because without them it can be impossible to identify what is complete, late, in progress, or on the true critical path. [gao.gov](https://www.gao.gov/assets/gao-16-89g.pdf) ([gao.gov](https://www.gao.gov/assets/gao-16-89g.pdf)) | Percent complete is permitted only when its numerator, denominator, scope version and acceptance rule are displayed. Prefer “7 of 10 required outcomes deployed; 4 accepted.” | High |
| **Built is reported as delivered** | DORA defines change lead time through code successfully running in production; NIST treats deployment as installing on production infrastructure, monitoring the release, verifying security/performance, and supporting rollback. [dora.dev](https://dora.dev/guides/dora-metrics/) [pages.nist.gov](https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html) ([dora.dev](https://dora.dev/guides/dora-metrics/)) | Give each outcome independent `built`, `tested`, `deployed`, `enabled_for_users`, `monitored`, and `accepted` states. | High |
| **Stale evidence** | GAO states that an unmaintained schedule can have inaccurate completion dates and critical paths and cannot reliably support management decisions. [gao.gov](https://www.gao.gov/assets/gao-16-89g.pdf) ([gao.gov](https://www.gao.gov/assets/gao-16-89g.pdf)) | Every status assertion needs `observed_at`, source, environment and expiry/freshness policy. “Unknown” must replace stale claims. | High |

<MISSING_DATA>[A post-2015 controlled estimate of the frequency or error magnitude of the named “90% done syndrome” in software projects was not found. The defensible basis is authoritative schedule guidance against subjective percentage reporting, not a prevalence statistic.]</MISSING_DATA>

#### Recommended completion model

**(High Confidence)** <INFERENCE from="GAO, DORA and NIST lifecycle distinctions">For every owner-visible outcome, use this stage vocabulary:</INFERENCE>

1. `unknown` — evidence is absent or stale.
2. `not_started`.
3. `in_progress`.
4. `built` — an implementation artefact exists.
5. `tested` — defined checks passed in a named environment.
6. `deployed_to_production`.
7. `enabled_for_intended_users`.
8. `operationally_verified` — production health, monitoring and recovery checks passed.
9. `owner_accepted` — acceptance criteria were explicitly confirmed.
10. `not_required` — removed from scope with actor, date and rationale.

A project-level “complete” label should be computed from a project-specific **completion contract**, for example: all mandatory outcomes are in their required terminal states, no release-blocking defects remain, required operational controls exist, and no owner decision remains unresolved. The contract and its version must be included in the report.

### 1.3 Decision elicitation: recommendations, defaults and active confirmation

The default evidence is strong but heterogeneous. Jachimowicz, Duncan, Weber and Johnson’s 2019 meta-analysis included 58 studies and 73,675 participants, reporting \(d=0.68\), 95% CI 0.53–0.83; several studies were non-significant and two had negative effects. [doi.org](https://doi.org/10.1017/S2398063X1800043X) ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html))

Experiments by Altmann, Falk and Grunewald found defaults were more informative when setter and decision-maker interests were aligned, and that participants were more likely to follow defaults than equally informative advice. [flex.uni-frankfurt.de](https://flex.uni-frankfurt.de/index.php/publications/communicating-through-defaults/) ([flex.uni-frankfurt.de](https://flex.uni-frankfurt.de/index.php/publications/communicating-through-defaults/))

<CONFLICTING_EVIDENCE>[Defaults can reduce omission and decision effort, but they can also anchor the respondent, communicate an implied endorsement, and move choices away from latent preferences. Their effect varies by domain, information quality and perceived alignment of interests.]</CONFLICTING_EVIDENCE>

#### Preselection policy

| Decision condition | Show recommendation? | Pre-populate draft? | Confirmation treatment | Confidence |
|---|---:|---:|---|---|
| **Low-risk, reversible, strong evidence, aligned interests** | Yes | Yes, if useful | Label `Suggested — not confirmed`; require a separate Confirm action. | High |
| **Moderate impact or preference-sensitive** | Yes | Preferably no | Show the recommendation and rationale beside neutral answer controls. | High |
| **Irreversible, security-sensitive, high-spend, contractual or weak-evidence** | Yes, if there is a real recommendation | No | Present all options neutrally; require explicit choice, confidence and acknowledgment of major consequences. | High |
| **Recommendation derived from an owner’s earlier policy** | Yes | Yes | Show the prior policy source and date; require confirmation that it still applies. | High |
| **No defensible recommendation** | No fabricated recommendation | No | Say “No recommendation — evidence or preference is insufficient.” | High |
| **Multiple independent selections allowed** | Yes, option by option where justified | Only as draft | Enforce minimum/maximum cardinality and incompatible-option rules. | High |

**Decisive rule:** **never export a preselected value as a confirmed decision merely because it was left unchanged.**

The WHATWG HTML standard distinguishes default checkedness from current checkedness and maintains an internal “dirty checkedness” flag after interaction. That distinction is useful for UI behavior, but it does not establish respondent identity, authority, comprehension or intent. [html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/input.html) ([html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/input.html))

#### Active confirmation workflow

**(High Confidence)** <INFERENCE from="default-effect evidence and HTML control semantics">Use this state machine:</INFERENCE>

```text
unanswered
   ↓ recommendation loaded or owner makes a selection
draft
   ↓ owner activates “Confirm this decision”
confirmed
   ↓ any answer, note, scope or option change
draft
```

- A decision card must display `Recommended`, `Selected but unconfirmed`, `Confirmed by … at …`, or `Deferred — work remains blocked` in text, not by color alone.
- The Confirm action must be attached to the individual decision, not only to a page-level “Submit.”
- A final page-level attestation may confirm the package but must not replace per-decision confirmation.
- If the owner accepts the recommendation unchanged, record `answer_origin: accepted_recommendation`.
- If the owner changes it, record `answer_origin: modified_recommendation`.
- If no recommendation was displayed, record `answer_origin: independent`.
- Any option-set revision invalidates the earlier confirmation unless the schema explicitly proves compatibility.

#### Optional notes, caveats and non-response

**(Medium Confidence)** Web-questionnaire experiments show a real tension. Dense grids can increase straightlining and nonsubstantive answers relative to single-item presentation, but converting everything to separate questions can increase length and burden. Forced-response designs have sometimes produced reactance, earlier dropout or poorer open-ended responses, while other studies report neutral or beneficial effects. [academic.oup.com](https://academic.oup.com/jssam/article/6/3/376/4349665) [doi.org](https://doi.org/10.1080/13645579.2021.1929714) ([academic.oup.com](https://academic.oup.com/jssam/article/6/3/376/4349665))

<INFERENCE from="satisficing and forced-response evidence">For a single owner, make the **decision disposition required**, not the free-text note. Each blocker must end in one of:</INFERENCE>

- `confirmed`;
- `needs_clarification`, with a required question;
- `authority_missing`, naming the needed decision-maker;
- `deferred`, with reason and reconsideration date.

A silent skip is not an answer. A deferred decision remains visibly blocking.

Notes should be optional, but if entered the page should ask:

> **Does this note limit, condition or override the selected answer?**

- `No — context only`: preserve verbatim but do not change execution.
- `Yes — constraint or exception`: require a structured caveat and block automation until the caveat is machine-checkable or reviewed.
- `Unsure`: set `requires_human_review: true`.

### 1.4 Surfacing blockers, dependencies and critical path

GAO’s schedule guidance treats maintained dependency logic, critical paths, near-critical paths, remaining duration and status dates as necessary for credible forecasting and management action. [gao.gov](https://www.gao.gov/products/gao-16-89g) ([gao.gov](https://www.gao.gov/products/gao-16-89g))

**(High Confidence)** <INFERENCE from="critical-path guidance">Represent the remaining work as a directed dependency graph, but translate it into owner language. Every decision card should answer:</INFERENCE>

1. **Why is this decision needed?**
2. **What work cannot proceed without it?**
3. **Does it fully release that work, remove only one blocker, or merely permit planning?**
4. **Is the affected work on the current critical path or near-critical path?**
5. **What happens if the answer arrives later?**
6. **Can the decision be reversed, and at what cost?**

Use stable relationships such as:

```json
{
  "decision_id": "D-04",
  "unblock_relationships": [
    {
      "work_item_id": "W-17",
      "effect": "fully_releases"
    },
    {
      "work_item_id": "W-22",
      "effect": "removes_one_blocker",
      "remaining_blocker_ids": ["EXT-03"]
    }
  ]
}
```

This avoids the common overstatement that a decision “unblocks five tasks” when those tasks remain blocked for other reasons.

#### Ordering and grouping

Simultaneous option presentation produced more optimal choices than sequential presentation across seven experiments in Basu and Savani’s work. Schneider and colleagues also found joint presentation outperformed separate presentation in large choice sets, although the best architecture depended on task and response mode. [doi.org](https://doi.org/10.1016/j.obhdp.2017.01.004) [doi.org](https://doi.org/10.1287/deca.2018.0379) ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0749597816302060))

<CONFLICTING_EVIDENCE>[Pure ranking can make urgency visible but separate related decisions; pure grouping improves context but can hide cross-group priority. Evidence from choice architecture favors useful ordering plus partitioning rather than either mechanism alone, but the results are context dependent.]</CONFLICTING_EVIDENCE> [doi.org](https://doi.org/10.1177/00222429221119086) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.1177/00222429221119086))

**(Medium Confidence)** <INFERENCE from="joint-presentation, ordering and partitioning evidence">Use this ordering tuple, with the factors shown to the owner rather than hidden in an opaque score:</INFERENCE>

1. `authority_check` — can this owner make the decision?
2. `quick_unlock` — low answer effort, high fan-out, reversible;
3. `critical_path_or_time_sensitive`;
4. `irreversible_or_high_consequence`;
5. `near_critical`;
6. `routine_same_domain_batch`;
7. `non_blocking_preference`.

Group cards under owner-visible outcomes such as **Launch**, **Payments**, **Privacy**, or **Operations**, but place a global priority number on each card. Options for each card should be visible together.

### 1.5 Asynchronous decision instruments versus meetings

The strongest measured evidence comes from decision aids rather than software RFC/ADR processes. The 2024 Cochrane review included 209 studies. Decision aids increased informed values-congruent choices, RR 1.75, improved knowledge by 11.90 points on a 100-point scale, and improved accurate risk perception, RR 1.94. Decision aids used before a consultation did not significantly change consultation length; those used during a consultation added about 1.5 minutes on average. [cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening) ([cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening))

**(Medium Confidence)** <INFERENCE from="decision-aid evidence; domain transfer limitation">A structured owner decision page is likely to outperform an unstructured status email because it exposes options, trade-offs, values and confirmation. The measured effect sizes above are from healthcare decisions and should not be treated as software-specific effect sizes.</INFERENCE>

ADR adoption evidence is more modest. A 2023 mining study found adoption remained low and that about 50% of repositories containing ADRs had only one to five records, suggesting trial use rather than sustained adoption. Repositories using ADRs systematically generally involved multiple contributors over time. [doi.org](https://doi.org/10.1109/ACCESS.2023.3287654) ([research.jku.at](https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/))

A 2026 preprint comparing ADR templates used 33 undergraduate software-engineering students; the concise Nygard template outperformed MADR on the study’s aggregate score, while MADR offered more structural detail. This is recent but not direct evidence about non-technical owners or production decision latency. [arxiv.org](https://arxiv.org/abs/2604.27333) ([arxiv.org](https://arxiv.org/abs/2604.27333))

Recent communication evidence also establishes an important limit. 2026 Nature Communications experiments found spoken disagreement generated greater perceived understanding and less conflict than written disagreement; participants incorrectly expected writing to perform better. [nature.com](https://www.nature.com/articles/s41467-026-71669-5) ([nature.com](https://www.nature.com/articles/s41467-026-71669-5))

#### Use the asynchronous page when

- there is one identified owner;
- authority is clear;
- alternatives are known and bounded;
- trade-offs can be stated in plain English;
- the decision is not primarily interpersonal;
- the recommendation and evidence can stand alone;
- the document can define what happens after each option.

#### Escalate to speech when

- authority or accountability is disputed;
- the owner says the options are wrong or incomplete;
- the decision involves unresolved conflict between stakeholders;
- the choice is emotionally or politically sensitive;
- an irreversible decision has low recommendation confidence;
- more than one clarification round is needed;
- free-text caveats cannot be converted into explicit constraints.

<MISSING_DATA>[No strong post-2015 controlled study was found reporting software-project decision latency, completion rate or reversal rate for a self-serve decision form versus a meeting. Practitioner claims that RFCs or ADRs are faster should therefore be treated as plausible but not measured here.]</MISSING_DATA>

### 1.6 Machine-readable round-trip and safe agent action

JSON Schema Draft 2020-12 supports strict object validation, conditionals, cardinality and rejection of unevaluated fields. W3C PROV supplies a model for entities, activities, agents, derivation and responsibility. RFC 8785 defines deterministic JSON canonicalization for repeatable hashing or signing. [json-schema.org](https://json-schema.org/draft/2020-12) [w3.org](https://www.w3.org/TR/prov-o/) [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc8785.html) ([json-schema.org](https://json-schema.org/draft/2020-12/release-notes))

#### Minimum schema requirements

| Field group | Required fields | Safety purpose |
|---|---|---|
| **Report identity** | `report_id`, `project_id`, `schema_version`, `status_as_of`, `scope_version` | Prevents answers being applied to the wrong project or stale scope. |
| **Generator provenance** | generator type/name/version/model, `generated_at`, source manifest | Distinguishes AI-generated proposals from human decisions. |
| **Decision definition** | stable ID, revision, question, type, option IDs, cardinality and incompatibility rules | Prevents label matching, old-option reuse and invalid multi-select combinations. |
| **Recommendation** | recommended option IDs, recommender, rationale, evidence refs, confidence, `preselected_in_ui` | Preserves the proposal without turning it into an answer. |
| **Draft state** | selected option IDs, origin, last-change timestamp | Allows recovery and analysis but remains non-actionable. |
| **Confirmation** | status, confirmed option IDs, explicit-confirmation flag, actor, time, answer origin | Establishes the sole actionable response object. |
| **Confidence** | evidence confidence, recommendation confidence, respondent confidence | Avoids overloading one ambiguous confidence field. |
| **Notes and caveats** | raw text, classification, structured constraints, `blocks_automation` | Prevents attached caveats being lost or treated as instructions. |
| **Authority** | actor ID, authority scope, self-asserted/signed status | Prevents action outside the respondent’s remit. |
| **Blocker relationships** | work IDs, release effect, remaining blockers | Prevents false claims that a decision fully releases work. |
| **Execution policy** | allowed/prohibited actions, spend limit, environments, expiry, review requirement | Bounds agent behavior beyond interpreting the answer. |
| **Integrity and validation** | canonicalization, payload hash, optional signature, schema validation results | Detects accidental or malicious modification and malformed exports. |

#### Illustrative export

```json
{
  "schema_version": "1.0.0",
  "report": {
    "report_id": "R-2026-08-12-001",
    "project_id": "P-001",
    "status_as_of": "2026-08-12T17:00:00Z",
    "scope_version": "scope-17",
    "generator": {
      "type": "ai_assisted",
      "name": "status-decision-builder",
      "version": "2.3.0",
      "model": "recorded-model-id",
      "generated_at": "2026-08-12T16:30:00Z"
    },
    "source_manifest": [
      {
        "source_id": "S-01",
        "uri": "urn:deployment:production:release-184",
        "observed_at": "2026-08-12T15:00:00Z",
        "sha256": "base64url-sha256"
      }
    ]
  },
  "respondent": {
    "actor_id": "owner-001",
    "display_name": "Project Owner",
    "authority_scope": [
      "hosting-region",
      "launch-date",
      "budget-under-5000-usd"
    ],
    "identity_assurance": "self_asserted"
  },
  "decisions": [
    {
      "decision_id": "D-04",
      "revision": 2,
      "question": "Which production hosting region should be used?",
      "type": "single",
      "options": [
        {
          "option_id": "us-east",
          "label": "US East"
        },
        {
          "option_id": "us-west",
          "label": "US West"
        }
      ],
      "cardinality": {
        "min": 1,
        "max": 1
      },
      "recommendation": {
        "option_ids": ["us-east"],
        "recommended_by": "project_agent",
        "rationale": "Lowest migration work under the current architecture.",
        "evidence_refs": ["S-01"],
        "confidence": "medium",
        "preselected_in_ui": true
      },
      "draft": {
        "selected_option_ids": ["us-east"],
        "origin": "recommendation",
        "last_changed_at": "2026-08-12T16:48:00Z"
      },
      "confirmation": {
        "status": "confirmed",
        "confirmed_option_ids": ["us-east"],
        "explicit": true,
        "confirmed_by": "owner-001",
        "confirmed_at": "2026-08-12T16:50:00Z",
        "answer_origin": "accepted_recommendation",
        "respondent_confidence": "high"
      },
      "notes": [
        {
          "note_id": "N-01",
          "text": "Use the standard backup-retention policy.",
          "classification": "constraint",
          "blocks_automation": false,
          "structured_constraint": {
            "policy_id": "backup-standard-v3"
          }
        }
      ],
      "unblock_relationships": [
        {
          "work_item_id": "W-17",
          "effect": "fully_releases"
        }
      ],
      "execution_policy": {
        "agent_may_act": true,
        "allowed_actions": [
          "update_infrastructure_configuration",
          "open_implementation_tasks"
        ],
        "prohibited_actions": [
          "purchase_reserved_capacity"
        ],
        "max_cost_usd": 0,
        "allowed_environments": ["development", "staging"],
        "requires_human_review": false,
        "expires_at": "2026-09-12T00:00:00Z"
      }
    }
  ],
  "validation": {
    "schema_valid": true,
    "all_required_decisions_disposed": true,
    "all_confirmed_answers_authorized": true,
    "referential_integrity_valid": true,
    "blocking_caveat_count": 0
  },
  "integrity": {
    "canonicalization": "RFC8785",
    "hash_algorithm": "SHA-256",
    "payload_sha256": "base64url-sha256",
    "signature": null
  }
}
```

**(High Confidence)** <INFERENCE from="JSON Schema, provenance, canonicalization and agent-security evidence">The acting agent should apply this gate in order:</INFERENCE>

1. Validate against the exact supported schema version, with unknown fields rejected where safety-relevant.
2. Verify the canonical hash and signature if present.
3. Confirm project ID, scope version and decision revision are current.
4. Read only `confirmation.confirmed_option_ids` as the decision.
5. Require `status == confirmed` and `explicit == true`.
6. Verify the actor’s authority covers this decision and intended action.
7. Reject expired decisions.
8. Block action if any note or caveat has `blocks_automation: true`.
9. Verify conditions and remaining dependencies.
10. Check that the intended tool call is allowlisted and within cost/environment limits.
11. After acting, write back action evidence rather than merely marking the work “done.”

#### Documented agent failure modes and schema response

| Failure | Evidence or epistemic status | Required response |
|---|---|---|
| **Default treated as decision** | Defaults materially affect choice; HTML defaults are distinct from active state. | Separate `recommendation`, `draft` and `confirmation`; only confirmation is actionable. |
| **Over-reading a terse answer** | <INSUFFICIENT_EVIDENCE>[No direct benchmark was found for project agents over-interpreting terse owner answers.]</INSUFFICIENT_EVIDENCE> | Record scope, option ID, conditions, authority and execution policy; prohibit inference beyond enumerated fields. |
| **Ignoring a caveat** | <INSUFFICIENT_EVIDENCE>[No direct controlled project-agent study was found measuring ignored attached caveats.]</INSUFFICIENT_EVIDENCE> | Preserve raw notes and require caveat classification; uncertain caveats block action. |
| **Treating notes as instructions** | Indirect prompt-injection research shows LLM applications can blur data and instruction channels and follow malicious instructions embedded in retrieved data. [arxiv.org](https://arxiv.org/abs/2302.12173) ([arxiv.org](https://arxiv.org/abs/2302.12173)) | Notes are untrusted data. They must never enter the agent’s privileged instruction channel and must not directly authorize tool calls. |
| **Acting on stale scope** | Schedule and status guidance requires current data and status dates. | Bind confirmations to project, scope and decision revisions; invalidate superseded decisions. |
| **Assuming interaction proves identity** | Browser event/checkedness semantics do not provide identity assurance. | Label identity assurance; require an external signature or authenticated submission for non-repudiation. |

### 1.7 Integrity of AI-generated status artefacts

NIST’s Generative AI Profile identifies confabulation—plausible but false content—as an inherent generative-AI risk. [doi.org](https://doi.org/10.6028/NIST.AI.600-1) ([nist.gov](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence))

Gao and colleagues’ 2023 ALCE work found that, on ELI5, even the best tested models lacked complete citation support 50% of the time. [aclanthology.org](https://aclanthology.org/2023.emnlp-main.398/) ([aclanthology.org](https://aclanthology.org/2023.emnlp-main.398/))

A Nature Machine Intelligence study found that people using ordinary LLM explanations were only slightly better than chance at discriminating correct from incorrect answers, with AUCs of 0.589, 0.602 and 0.592 across reported conditions. [doi.org](https://doi.org/10.1038/s42256-024-00976-7) ([doi.org](https://doi.org/10.1038/s42256-024-00976-7))

<CONFLICTING_EVIDENCE>[Explanations can improve appropriate trust when carefully designed: a 2022 set of experiments found feature-contribution explanations improved appropriate trust without increasing over- or under-trust in one task. But a 2025 medical-AI preprint reported that explanations increased decision accuracy by 6.3 percentage points when AI was correct, reduced it by 4.9 points when AI was wrong, and caused participants to perceive explained AI as 15.2 points more accurate than it was. Explanation presence alone is therefore not an integrity control.]</CONFLICTING_EVIDENCE> [doi.org](https://doi.org/10.1145/3519266) [arxiv.org](https://arxiv.org/abs/2512.08424) ([doi.org](https://doi.org/10.1145/3519266))

#### Required honesty controls

| Control | Structural guarantee | What it cannot guarantee |
|---|---|---|
| **Claim-level evidence references** | Every material claim can be traced to one or more source IDs. | The underlying source itself may be wrong. |
| **Epistemic state** | Each claim is marked `observed`, `reported_by_team`, `calculated`, `inferred`, `unknown`, or `disputed`. | A dishonest actor may mislabel evidence without independent verification. |
| **Environment and timestamp** | Prevents staging evidence from silently proving production deployment. | Does not prove the observation was complete. |
| **Scope version and change log** | Makes scope additions/removals visible and prevents denominator drift. | Does not decide whether the changed scope was appropriate. |
| **No unsupported completeness claim** | A validator can reject `complete` when required evidence or acceptance is missing. | Cannot ensure acceptance criteria were wisely chosen. |
| **AI-generation disclosure** | Readers know which prose and recommendations were machine-generated. | Disclosure alone does not calibrate trust. |
| **Human override provenance** | Overrides name the actor, time and reason. | Does not prove the override was correct. |
| **Hash/signature** | Detects later changes when checked against a trusted value. | An unsigned local file cannot provide strong identity or non-repudiation. |

**(High Confidence)** <INFERENCE from="AI citation and trust evidence">Citations should attach to individual material claims, not merely to paragraphs. The report should calculate an evidence-coverage indicator, but label it precisely: “percentage of material claims with a valid evidence reference,” not “percentage of the report that is true.”</INFERENCE>

### 1.8 Accessibility, print and self-containment

WCAG 2.2 requires programmatically determinable names, roles, states and values for controls and accessible status messages. W3C form guidance recommends `fieldset` and `legend` for related checkboxes and radio buttons. [w3.org](https://www.w3.org/TR/WCAG22/) [w3.org](https://www.w3.org/WAI/WCAG21/Techniques/html/H71) ([w3.org](https://www.w3.org/TR/WCAG22/))

#### Required implementation constraints

**(High Confidence)**

- Use semantic headings, landmarks, lists, tables and native form controls.
- Place each radio/checkbox group in a `fieldset` with a descriptive `legend`.
- Give every control an explicit label and visible instructions.
- Do not communicate status, recommendation or validation solely by color.
- Keep keyboard focus visible; ensure every action is operable without a pointer.
- Announce validation, confirmation and export results through accessible status regions.
- Avoid custom checkboxes, switches or dropdowns when native controls suffice.
- Preserve a logical reading and tab order.
- Provide inline error messages connected to the affected decision.
- Ensure zoom/reflow does not hide options, notes or confirmation controls.
- Use plain-language option labels; put technical detail in expandable supporting text without making it the only location of material consequences.

**(Medium Confidence)** <INFERENCE from="WCAG and durable-record requirements">For printing, do not rely on the visual appearance of checked controls. Generate a print-only decision summary that writes each decision, selected answer, confirmation state, respondent, timestamp, caveat and work released as text. Use grayscale-safe styling, repeated table headings and controlled page breaks.</INFERENCE>

**(High Confidence)** <INFERENCE from="single-file requirement and integrity standards">For self-containment:</INFERENCE>

- Embed all CSS and JavaScript; require no CDN, external font, analytics or network request.
- Store the JSON Schema, source manifest and report metadata in non-executable JSON script elements.
- Escape all project-derived content; do not insert source text through unsafe HTML rendering.
- Make the report readable without JavaScript; JavaScript may add validation and export.
- Export both:
  1. a canonical JSON decision record for the agent; and
  2. an optional newly generated completed-HTML snapshot for human retention.
- Keep the original questionnaire artefact unchanged; the completed copy is a new record.
- Include visible file/export hashes and generated-at/status-as-of timestamps.
- Print source URLs or stable evidence identifiers where the durable record must remain interpretable offline.
- Treat “self-contained” as meaning the page renders and functions offline—not that it republishes every external source.

### 1.9 Comparative design table

The model-comparison columns requested in the prompt are not meaningful for this document class; the equivalent operational parameters are shown below. Entries are design synthesis rather than benchmark measurements.

| Approach | Context window / reading burden | Decision latency | Implementation cost | License/dependency | Status integrity | Machine-action safety | Verdict |
|---|---|---|---|---|---|---|---|
| **RAG dashboard only** | Low | Fast to view | Low | None | Low: conflates multiple dimensions and permits watermelon reporting | None | Discard as the primary format |
| **Narrative status memo** | Medium/high | Low scheduling latency; clarification often needed | Low | None | Medium if evidence-linked; otherwise low | Low | Retain only as executive summary |
| **Separate RFC/ADR collection** | High for a non-technical owner | No calendar requirement, but discovery and completion can be slow | Medium | Usually Markdown/repository tooling | High for individual decisions; weak project overview | Medium | Use as technical backing records, not owner interface |
| **Live decision meeting** | Context supplied orally | Calendar wait plus meeting time | High recurring human cost | Conferencing/meeting tooling | Low unless separately recorded | Low unless transcribed and structured | Escalation path, not default |
| **Proposed single-file status-and-decision HTML** | Progressive: summary first, evidence on demand | No calendar wait; respondent time only | Moderate initial build, low per report | Vanilla HTML/CSS/JS; no runtime dependency required | High if status rules and provenance validate | High if export fails closed | Recommended |

<INSUFFICIENT_EVIDENCE>[No defensible cross-project dollar-cost or latency benchmark was found for these five formats. Qualitative cost and latency entries are architectural comparisons, not empirical estimates.]</INSUFFICIENT_EVIDENCE>

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

**As of August 12, 2026**, the evidence base is mature in some layers and immature in the integrated system the user proposes.

| Layer | Current state | Strongest evidence | Confidence |
|---|---|---|---|
| **Objective remaining-work and schedule state** | Mature guidance exists: use maintained dependencies, status dates, remaining duration, critical paths and risk analysis. | GAO Schedule Assessment Guide. [gao.gov](https://www.gao.gov/products/gao-16-89g) ([gao.gov](https://www.gao.gov/products/gao-16-89g)) | High |
| **Executive RAG reporting** | Still widely used, but authorities explicitly acknowledge it is a snapshot rather than a comprehensive performance representation. At the March 2026 NISTA snapshot, 58% of projects were amber, 18% red, 15% green and 9% exempt. [gov.uk](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26) ([gov.uk](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26)) | NISTA annual report and delivery-confidence definitions. | High |
| **Optimism controls** | Reference-class and historical-error correction are established government practice, reaffirmed in 2026. | UK Green Book 2026. [gov.uk](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026) ([gov.uk](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026)) | High |
| **Decision-aid structure** | Strong evidence that structured option/trade-off aids improve understanding and values alignment, mainly outside software. | 2024 Cochrane review of 209 studies. [cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening) ([cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening)) | High for the measured domain; Medium for transfer |
| **Defaults and preselection** | Strong evidence that defaults materially shape choices; effects are heterogeneous and can reverse. | Jachimowicz et al. meta-analysis and subsequent default-communication experiments. [doi.org](https://doi.org/10.1017/S2398063X1800043X) ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html)) | High |
| **ADRs/RFCs as asynchronous records** | Accepted practitioner pattern, but systematic adoption is low and outcome evidence is limited. | Buchgeher et al. 2023 repository-mining study. [doi.org](https://doi.org/10.1109/ACCESS.2023.3287654) ([research.jku.at](https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/)) | Medium |
| **Machine-readable decision provenance** | Mature component standards exist—JSON Schema, PROV and canonical JSON—but not a standard integrated owner-decision schema. | JSON Schema 2020-12, W3C PROV, RFC 8785. | High for components; Low for integrated convention |
| **Agent safety with human answers** | Emerging. Prompt injection and instruction/data confusion are documented; robust semantics for owner caveats and defaults are not standardized. | Greshake et al. and subsequent injection benchmarks. [arxiv.org](https://arxiv.org/abs/2302.12173) ([arxiv.org](https://arxiv.org/abs/2302.12173)) | Medium |
| **AI status-report trust** | Confabulation, citation incompleteness and reader miscalibration are established generally; status-report-specific experiments are absent. | NIST AI 600-1, ALCE, Nature Machine Intelligence trust study. | High generally; Low specifically |
| **Accessibility** | Mature normative baseline exists. | WCAG 2.2 and WAI form techniques. [w3.org](https://www.w3.org/TR/WCAG22/) ([w3.org](https://www.w3.org/TR/WCAG22/)) | High |

<INSUFFICIENT_EVIDENCE>[No authoritative standard or validated reference implementation was found that combines evidence-backed software status, single-owner decision elicitation, blocker/critical-path relationships, active confirmation, agent-safe JSON export, accessibility and single-file durability. The proposed design is therefore a synthesis of mature component practices rather than adoption of one existing standard.]</INSUFFICIENT_EVIDENCE>

---

### 3. What are the contrasting viewpoints or competing evidence?

| Issue | Position/evidence A | Position/evidence B | Resolution for this design |
|---|---|---|---|
| **Preselected defaults** | Defaults reduce omission and strongly influence choice, with average \(d=0.68\). [doi.org](https://doi.org/10.1017/S2398063X1800043X) ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html)) | Effects vary substantially; some are null or negative, and defaults can communicate strategic endorsement. | Pre-populate only an explicitly unconfirmed draft in low-risk cases; never infer confirmation from inaction. |
| **Recommendations versus neutral options** | Recommendations can reduce effort and improve decisions where expertise and interests align. | Recommendations and explanations can anchor or produce over-reliance, especially when wrong. [doi.org](https://doi.org/10.1145/3519266) [arxiv.org](https://arxiv.org/abs/2512.08424) ([doi.org](https://doi.org/10.1145/3519266)) | Show recommendation provenance, confidence and rationale. Remove preselection for irreversible or weak-evidence decisions. |
| **Required answers** | Forced dispositions reduce silent missingness and can counter superficial multi-answer selection. | Forced-response designs can cause reactance, poor-quality answers or dropout in some contexts. [doi.org](https://doi.org/10.1080/13645579.2021.1929714) ([tandfonline.com](https://www.tandfonline.com/doi/full/10.1080/13645579.2021.1929714)) | Require an explicit disposition, including clarification or defer; keep free-text notes optional. |
| **One card at a time versus grouped matrix** | Single items reduce straightlining and nonsubstantive answers. | Too many separate screens increase burden and hide context. [academic.oup.com](https://academic.oup.com/jssam/article/6/3/376/4349665) ([academic.oup.com](https://academic.oup.com/jssam/article/6/3/376/4349665)) | One semantic card per decision, several cards visible under a shared outcome heading; avoid grids. |
| **Ranked versus grouped presentation** | Ranking makes urgency visible. | Grouping and partitioning help comparison and reduce overload; joint presentation can improve decision quality. | Group by outcome, rank within groups, and display all alternatives for a decision simultaneously. |
| **Asynchronous versus synchronous** | Written records provide persistence, flexible response time and a machine-readable result; recent hybrid-work evidence indicates asynchronous messages can carry useful, novel information. [aeaweb.org](https://www.aeaweb.org/articles?id=10.1257/pandp.20261010) ([aeaweb.org](https://www.aeaweb.org/articles?id=10.1257%2Fpandp.20261010)) | Spoken disagreement can produce greater understanding and less conflict than writing. [nature.com](https://www.nature.com/articles/s41467-026-71669-5) ([nature.com](https://www.nature.com/articles/s41467-026-71669-5)) | Async by default for bounded decisions; speech as an escalation path for conflict, ambiguity or low-confidence irreversible choices. |
| **Concise versus detailed decision records** | The 2026 ADR preprint favored the concise Nygard template on aggregate score. | Participants valued MADR for structure and architectural detail. [arxiv.org](https://arxiv.org/abs/2604.27333) ([arxiv.org](https://arxiv.org/abs/2604.27333)) | Concise owner-facing card plus expandable evidence and a more detailed technical backing record. |
| **AI explanations and trust** | Certain explanation types can improve appropriate trust. | Persuasive explanations can increase reliance even when AI is wrong, and ordinary explanations are poor signals of correctness. | Evidence and independent checks, not explanation fluency, determine actionability. |

---

### 4. What changed recently, and what is the trajectory?

- **(High Confidence)** The UK Green Book’s 2026 edition reaffirmed that optimism bias must be explicitly corrected using historical forecast error or appropriate generic evidence. NISTA’s 2025–26 report simultaneously retained RAG-style confidence assessments while explicitly warning that they are not comprehensive project-performance measures. [gov.uk](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026) [gov.uk](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26) ([gov.uk](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026))

- **(High Confidence)** The 2024 Cochrane decision-aid update substantially strengthened the evidence that structured, self-serve decision information improves knowledge, risk comprehension, active participation and values-congruent choices without necessarily increasing consultation time when used in advance. [cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening) ([cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening))

- **(Medium Confidence)** Recent ADR work is shifting from advocacy to empirical comparison. The 2023 repository study documented low but increasing adoption; a 2026 preprint directly compared templates, although with only 33 students and no production-owner outcome measures. [doi.org](https://doi.org/10.1109/ACCESS.2023.3287654) [arxiv.org](https://arxiv.org/abs/2604.27333) ([research.jku.at](https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/))

- **(High Confidence)** AI integrity has become more urgent. NIST formalized generative-AI confabulation risk in 2024; 2024–26 trust studies show that fluent explanations are weak correctness signals and may magnify wrong advice. [doi.org](https://doi.org/10.6028/NIST.AI.600-1) [doi.org](https://doi.org/10.1038/s42256-024-00976-7) ([nist.gov](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence))

- **(Medium Confidence)** Agent security is moving from theoretical prompt injection to observed ecosystem risk. A 2026 preprint analyzing 1.2 billion URLs from 24.8 million hosts reported 15,300 validated prompt-injection instances across 11,700 pages. This remains preprint evidence, but it reinforces that retrieved prose and free text cannot safely double as privileged instructions. [arxiv.org](https://arxiv.org/abs/2604.27202) ([arxiv.org](https://arxiv.org/abs/2604.27202))

- **(Medium Confidence)** <INFERENCE from="the recent evidence above">The trajectory is toward artefacts that are structured, provenance-aware, asynchronous and directly consumable by automation—but with clearer separation between AI proposals, human confirmations and machine execution authority. The strongest opportunity is not a more attractive status dashboard; it is a constrained human-to-agent transaction record wrapped in a comprehensible status narrative.</INFERENCE>

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| **(High)** Reliable status requires maintained logic, status dates, remaining duration and critical-path analysis. | U.S. Government Accountability Office, *Schedule Assessment Guide* ([gao.gov](https://www.gao.gov/products/gao-16-89g)) | December 22, 2015 | Authoritative government audit guide; primary practitioner standard | https://www.gao.gov/products/gao-16-89g |
| **(High)** Delivery-confidence colors are snapshots, not comprehensive performance measures. | UK NISTA, *Major Projects Annual Report 2025–26* ([gov.uk](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26)) | 2026 | Current authoritative government portfolio reporting | https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26 |
| **(Medium)** Watermelon reporting is a documented audit failure mode. | Association of Local Government Auditors, Austin audit account ([algaonline.org](https://algaonline.org/page/2020_Summer_Lin_Harvey)) | 2020 | Primary practitioner audit account; not prevalence evidence | https://algaonline.org/page/2020_Summer_Lin_Harvey |
| **(High)** Optimism bias should be corrected using historical error/reference-class evidence. | HM Treasury, *The Green Book 2026* ([gov.uk](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026)) | 2026 | Current authoritative government appraisal guidance | https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026 |
| **(High)** Production deployment is distinct from code completion. | DORA, software-delivery metrics ([dora.dev](https://dora.dev/guides/dora-metrics/)) | 2026 current page | Official practitioner research/metric definition; non-promotional | https://dora.dev/guides/dora-metrics/ |
| **(High)** Deploying includes production installation, monitoring and verification. | NIST NCCoE DevSecOps reference model ([pages.nist.gov](https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html)) | 2025–26 current documentation | Authoritative technical documentation | https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html |
| **(High)** Defaults have a substantial but heterogeneous effect, \(d=0.68\). | Jachimowicz, Duncan, Weber and Johnson ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html)) | 2019 | Peer-reviewed meta-analysis; direct behavioral evidence | https://doi.org/10.1017/S2398063X1800043X |
| **(High)** Defaults can convey endorsement and are followed more readily than equivalent advice. | Altmann, Falk and Grunewald ([flex.uni-frankfurt.de](https://flex.uni-frankfurt.de/index.php/publications/communicating-through-defaults/)) | 2022 online | Peer-reviewed experimental research; university-hosted source record | https://flex.uni-frankfurt.de/index.php/publications/communicating-through-defaults/ |
| **(Medium)** People interpret defaults as recommendations. | Buchanan et al., *International Journal of Consumer Studies* ([digitalcommons.cwu.edu](https://digitalcommons.cwu.edu/cotsfac/830/)) | July 1, 2022 | Peer-reviewed experiments; direct default-perception evidence | https://digitalcommons.cwu.edu/cotsfac/830/ |
| **(High)** Decision aids improve knowledge, risk perception and values-congruent choice. | Stacey et al., Cochrane Review ([cochrane.org](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening)) | January 29, 2024 | Systematic review of randomized trials; strong but cross-domain | https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening |
| **(Medium)** Simultaneous presentation can improve choice quality over sequential presentation. | Basu and Savani ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0749597816302060)) | 2017 | Seven controlled experiments; direct presentation-format evidence | https://doi.org/10.1016/j.obhdp.2017.01.004 |
| **(Medium)** Joint presentation can outperform separate presentation in large choice sets. | Schneider et al. ([pubsonline.informs.org](https://pubsonline.informs.org/doi/10.1287/deca.2018.0379)) | January 31, 2019 | Controlled choice-architecture experiments | https://doi.org/10.1287/deca.2018.0379 |
| **(Medium)** Ordering plus partitioning can improve complex choice. | Dellaert, Johnson, Duncan and Baker ([journals.sagepub.com](https://journals.sagepub.com/doi/10.1177/00222429221119086)) | 2024 issue | Peer-reviewed experimental decision research; domain-limited | https://doi.org/10.1177/00222429221119086 |
| **(Medium)** Dense grids can increase straightlining and nonsubstantive response. | *Mitigating Satisficing in Cognitively Demanding Grid Questions* ([academic.oup.com](https://academic.oup.com/jssam/article/6/3/376/4349665)) | 2018 | Two web experiments; individual response-behavior evidence | https://academic.oup.com/jssam/article/6/3/376/4349665 |
| **(Medium)** Forced response has mixed effects, including possible reactance and quality loss. | *Assessing the Effect of Questionnaire Design on Unit and Item Nonresponse* ([tandfonline.com](https://www.tandfonline.com/doi/full/10.1080/13645579.2021.1929714)) | 2021 | Peer-reviewed online experiment and evidence synthesis | https://doi.org/10.1080/13645579.2021.1929714 |
| **(High)** HTML controls distinguish default and current checkedness. | WHATWG HTML Living Standard ([html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/input.html)) | Current August 2026 | Normative web-platform specification | https://html.spec.whatwg.org/multipage/input.html |
| **(High)** Related controls should be programmatically grouped and labelled. | W3C WAI Technique H71 ([w3.org](https://www.w3.org/WAI/WCAG21/Techniques/html/H71)) | Current 2026 | Authoritative accessibility technique | https://www.w3.org/WAI/WCAG21/Techniques/html/H71 |
| **(Medium)** ADR adoption remains low; about half of ADR repositories had one to five records. | Buchgeher et al., IEEE Access ([research.jku.at](https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/)) | June 2023 | Peer-reviewed repository-mining study | https://doi.org/10.1109/ACCESS.2023.3287654 |
| **(Low/Medium)** Concise Nygard ADR outperformed MADR in a 33-student experiment. | Nogueira, Silva and Conte ([arxiv.org](https://arxiv.org/abs/2604.27333)) | April 30, 2026 | Recent preprint; controlled but small/non-production sample | https://arxiv.org/abs/2604.27333 |
| **(Medium)** Hybrid work can produce useful and novel asynchronous information. | Schirmann et al., AEA Papers and Proceedings ([aeaweb.org](https://www.aeaweb.org/articles?id=10.1257%2Fpandp.20261010)) | May 2026 | Field experiment; peer-reviewed proceedings | https://www.aeaweb.org/articles?id=10.1257/pandp.20261010 |
| **(High)** Spoken disagreement can be more constructive than written disagreement. | *Nature Communications* ([nature.com](https://www.nature.com/articles/s41467-026-71669-5)) | 2026 | Multiple controlled communication experiments | https://www.nature.com/articles/s41467-026-71669-5 |
| **(High)** Strict machine-readable validation can be expressed with JSON Schema. | JSON Schema Draft 2020-12 ([json-schema.org](https://json-schema.org/draft/2020-12)) | December 2020 | Official technical specification | https://json-schema.org/draft/2020-12 |
| **(High)** Provenance can represent entities, activities, agents and responsibility. | W3C PROV-O ([w3.org](https://www.w3.org/TR/prov-o/)) | April 30, 2013 | Normative foundational standard; retained despite pre-2015 date | https://www.w3.org/TR/prov-o/ |
| **(High)** JSON can be deterministically canonicalized for hashing/signing. | RFC 8785 ([rfc-editor.org](https://www.rfc-editor.org/rfc/rfc8785.html)) | June 2020 | RFC technical specification | https://www.rfc-editor.org/rfc/rfc8785.html |
| **(High)** LLM applications can confuse external data with instructions. | Greshake et al. ([arxiv.org](https://arxiv.org/abs/2302.12173)) | February 23, 2023 | Primary security research on indirect prompt injection | https://arxiv.org/abs/2302.12173 |
| **(Medium)** Prompt-injection content is observable in the web ecosystem. | *Indirect Prompt Injection in the Wild* ([arxiv.org](https://arxiv.org/abs/2604.27202)) | April 2026 | Large-scale recent preprint; lower certainty until peer review | https://arxiv.org/abs/2604.27202 |
| **(High)** Generative AI confabulation is a formal risk category. | NIST AI 600-1 ([nist.gov](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)) | July 2024 | Authoritative federal AI risk guidance | https://doi.org/10.6028/NIST.AI.600-1 |
| **(High)** Generated citations often fail to support all claims. | Gao et al., ALCE ([aclanthology.org](https://aclanthology.org/2023.emnlp-main.398/)) | 2023 | Peer-reviewed benchmark with quantitative citation evaluation | https://aclanthology.org/2023.emnlp-main.398/ |
| **(High)** Readers struggle to discriminate correct from incorrect LLM answers from default explanations. | *Nature Machine Intelligence* ([doi.org](https://doi.org/10.1038/s42256-024-00976-7)) | December 2024 | Peer-reviewed human trust-calibration experiments | https://doi.org/10.1038/s42256-024-00976-7 |
| **(Medium)** Explanation type can affect appropriate trust. | ACM Transactions on Interactive Intelligent Systems ([doi.org](https://doi.org/10.1145/3519266)) | November 4, 2022 | Three randomized human-subject experiments | https://doi.org/10.1145/3519266 |
| **(High)** Accessible controls and status messages have normative requirements. | W3C WCAG 2.2 ([w3.org](https://www.w3.org/TR/WCAG22/)) | October 5, 2023 | W3C Recommendation; authoritative accessibility standard | https://www.w3.org/TR/WCAG22/ |

---

## Knowledge Gaps

### Directness of evidence

- <MISSING_DATA>[A controlled comparison of an integrated software status-and-decision HTML page against a meeting, status memo or dashboard, using non-technical project owners and measuring comprehension, decision completion, reversals and downstream delivery time.]</MISSING_DATA>
- <INSUFFICIENT_EVIDENCE>[Healthcare decision-aid effects are directionally relevant but cannot be assumed to have the same magnitude for software architecture, budget or launch decisions.]</INSUFFICIENT_EVIDENCE>
- <INSUFFICIENT_EVIDENCE>[The 2026 ADR template comparison used 33 students, not non-technical owners or experienced production decision-makers.]</INSUFFICIENT_EVIDENCE>

### Decision latency and completion

- <MISSING_DATA>[Measured median time-to-decision, completion rate, clarification rate and abandonment rate for RFCs, ADRs or self-serve owner forms.]</MISSING_DATA>
- <MISSING_DATA>[Evidence for the optimal number of blocking decisions that one owner should answer in a single sitting.]</MISSING_DATA>
- <CONFLICTING_EVIDENCE>[Separating questions can reduce grid satisficing, but longer instruments can increase burden. No project-owner-specific optimum was found.]</CONFLICTING_EVIDENCE>

### Defaults and confirmation

- <CONFLICTING_EVIDENCE>[Defaults improve completion and sometimes outcomes, but also anchor choices and communicate endorsement. Effects depend on interests, information and domain.]</CONFLICTING_EVIDENCE>
- <MISSING_DATA>[A direct experiment comparing “preselected but explicitly unconfirmed” with “recommendation highlighted but no control preselected” for expert, consequential project decisions.]</MISSING_DATA>
- <CONFIDENCE:LOW>[Interaction telemetry alone can establish informed owner intent or identity. It should be treated as supporting metadata, not proof.]</CONFIDENCE:LOW>

### Agent interpretation

- <MISSING_DATA>[A benchmark measuring how often agents over-read terse human decisions, ignore attached caveats or treat defaults as decisions in project-management workflows.]</MISSING_DATA>
- <INSUFFICIENT_EVIDENCE>[A universally safe way to let an LLM interpret arbitrary free-text caveats while retaining autonomous tool authority.]</INSUFFICIENT_EVIDENCE>
- <INFERENCE from="indirect prompt-injection evidence and missing caveat benchmarks">The defensible interim policy is to treat free text as untrusted context and fail closed when it materially changes execution.</INFERENCE>

### AI-generated status trust

- <MISSING_DATA>[Controlled studies specifically testing reader trust, error detection and action quality for AI-written software project status reports.]</MISSING_DATA>
- <INSUFFICIENT_EVIDENCE>[A citation link by itself calibrates trust. Existing evidence shows citation completeness and human discrimination remain weak.]</INSUFFICIENT_EVIDENCE>

### Durability, print and authentication

- <MISSING_DATA>[Cross-browser measured reliability of printing dynamic native form state as a durable record.]</MISSING_DATA>
- <INSUFFICIENT_EVIDENCE>[An unsigned, offline single-file HTML artefact can provide strong respondent authentication or non-repudiation.]</INSUFFICIENT_EVIDENCE>
- <INFERENCE from="web-platform and integrity constraints">Where legal or financial attribution matters, the JSON export must be submitted through an authenticated channel or externally signed.</INFERENCE>

---

## Recommended Next Steps

1. **(High Confidence) Build and test the state model before styling the report.**  
   Specify the allowed work stages, decision states, confirmation invalidation rules, blocker relationship types and project completion contract.  
   **Rationale:** Most dangerous failures—default treated as decision, deployed conflated with built, stale scope and false unblock claims—are data-model failures rather than visual-design failures.

2. **(High Confidence) Publish a strict JSON Schema plus adversarial fixtures.**  
   Include valid confirmed, draft-only, deferred, stale-revision, unauthorized, contradictory multi-select, blocking-caveat, unknown-field and tampered-hash examples.  
   **Rationale:** The agent’s safest behavior can then be tested deterministically rather than delegated to natural-language interpretation.

3. **(High Confidence) Run a measured owner usability pilot.**  
   Compare at least two treatments:  
   - recommendation shown with no option selected;  
   - recommendation pre-populated as an explicitly unconfirmed draft.  
   Measure comprehension, completion time, confirmation rate, recommendation acceptance, later reversal, clarification requests and unnoticed defaults.  
   **Rationale:** This addresses the most consequential unresolved design question with project-specific evidence.

4. **(High Confidence) Red-team the round-trip boundary.**  
   Test prompt injection in notes, hidden HTML, stale exports, option-label changes, duplicate IDs, scope-version mismatch, contradictory caveats, forged interaction records and actions exceeding cost or environment limits.  
   **Rationale:** Existing agent-security evidence shows untrusted data can influence tool-using models; the schema and execution gateway must remain the security boundary.

5. **(High Confidence) Commission accessibility and durability verification as separate acceptance gates.**  
   Test keyboard-only and screen-reader operation, zoom/reflow, status announcements, high-contrast and grayscale output, print summaries, offline operation, JSON download and completed-HTML regeneration.  
   **Rationale:** Conformance cannot be inferred from semantic intent alone, and the printed record should not depend on browser rendering of checked controls.

## Sources

- [https://www.gao.gov/products/gao-16-89g](https://www.gao.gov/products/gao-16-89g)
- [https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html)
- [https://html.spec.whatwg.org/multipage/input.html](https://html.spec.whatwg.org/multipage/input.html)
- [https://www.sciencedirect.com/science/article/pii/S0749597816302060](https://www.sciencedirect.com/science/article/pii/S0749597816302060)
- [https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decis...](https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening)
- [https://json-schema.org/draft/2020-12](https://json-schema.org/draft/2020-12)
- [https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-ar...](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [https://algaonline.org/page/2020_Summer_Lin_Harvey](https://algaonline.org/page/2020_Summer_Lin_Harvey)
- [https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major...](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26/nista-major-projects-annual-report-2025-26)
- [https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-gov...](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026)
- [https://www.gao.gov/assets/gao-16-89g.pdf](https://www.gao.gov/assets/gao-16-89g.pdf)
- [https://dora.dev/guides/dora-metrics/](https://dora.dev/guides/dora-metrics/)
- [https://flex.uni-frankfurt.de/index.php/publications/communicating-through-defaults/](https://flex.uni-frankfurt.de/index.php/publications/communicating-through-defaults/)
- [https://academic.oup.com/jssam/article/6/3/376/4349665](https://academic.oup.com/jssam/article/6/3/376/4349665)
- [https://journals.sagepub.com/doi/10.1177/00222429221119086](https://journals.sagepub.com/doi/10.1177/00222429221119086)
- [https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projec...](https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/)
- [https://arxiv.org/abs/2604.27333](https://arxiv.org/abs/2604.27333)
- [https://www.nature.com/articles/s41467-026-71669-5](https://www.nature.com/articles/s41467-026-71669-5)
- [https://json-schema.org/draft/2020-12/release-notes](https://json-schema.org/draft/2020-12/release-notes)
- [https://arxiv.org/abs/2302.12173](https://arxiv.org/abs/2302.12173)
- [https://aclanthology.org/2023.emnlp-main.398/](https://aclanthology.org/2023.emnlp-main.398/)
- [https://doi.org/10.1038/s42256-024-00976-7](https://doi.org/10.1038/s42256-024-00976-7)
- [https://doi.org/10.1145/3519266](https://doi.org/10.1145/3519266)
- [https://www.w3.org/TR/WCAG22/](https://www.w3.org/TR/WCAG22/)
- [https://www.tandfonline.com/doi/full/10.1080/13645579.2021.1929714](https://www.tandfonline.com/doi/full/10.1080/13645579.2021.1929714)
- [https://www.aeaweb.org/articles?id=10.1257%2Fpandp.20261010](https://www.aeaweb.org/articles?id=10.1257%2Fpandp.20261010)
- [https://arxiv.org/abs/2604.27202](https://arxiv.org/abs/2604.27202)
- [https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html](https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html)
- [https://digitalcommons.cwu.edu/cotsfac/830/](https://digitalcommons.cwu.edu/cotsfac/830/)
- [https://pubsonline.informs.org/doi/10.1287/deca.2018.0379](https://pubsonline.informs.org/doi/10.1287/deca.2018.0379)
- [https://www.w3.org/WAI/WCAG21/Techniques/html/H71](https://www.w3.org/WAI/WCAG21/Techniques/html/H71)
- [https://www.w3.org/TR/prov-o/](https://www.w3.org/TR/prov-o/)
- [https://www.rfc-editor.org/rfc/rfc8785.html](https://www.rfc-editor.org/rfc/rfc8785.html)
