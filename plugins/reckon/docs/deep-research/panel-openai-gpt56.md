---
title: "Closed-world reconciliation rules for software verification remaining work"
run_id: dr_9fbb26d3a28e4eaf
question: "How should a \"remaining work\" determination be constructed and gated when the evidence base is a partially-completed verification campaign — when a large fraction of planned checks were blocked, inconclusive, or carried forward rather than executed, and most stated requirements are self-reported rather than independently observed? I need: (1) established taxonomies and standards for requirements traceability and verification status — how DO-178C/DO-330, ISO 26262, IEC 62304, FDA software validation, ISO/IEC/IEEE 29119 and ECSS distinguish \"verified present\", \"verified absent\", \"not yet verified\", \"unverifiable with available means\" and \"deviation/waiver\"; what artefacts they mandate (requirements traceability matrix, verification cross-reference index, coverage analysis, deviation register) and what each requires before an unverified requirement may be closed or deferred; (2) empirical evidence on how status, coverage and completion reporting drifts or misleads in software projects — the \"90% done\"/last-10% effect, watermelon or green-shift status reporting, coverage-metric gaming and Goodhart effects, silent test skipping and flaky-test suppression, and which interventions measurably reduced the drift; (3) how coverage denominators are defined honestly — percentage of what was executed versus what was planned versus the specified behaviour space, and published guidance or measured results on declaring sampled or partial coverage so a partial result cannot be read as complete; (4) the epistemology and practice of recording \"unknown\" as a first-class verification outcome — three- and four-valued logics in verification, \"undetermined\" verdicts in test standards and formal methods, known-unknowns registers, and evidence on whether making unknowns explicit changes decisions; (5) what is documented about deriving new work items from verification gaps — turning a blocked or unmeasurable check into a testability work item (test hooks, seams, dependency injection for unreachable states), the software testability literature on controllability and observability, and measured results on the cost of retrofitting testability versus designing it in."
provider: openai
model: gpt-5.6-sol
tier: max
archetype: technical
sources: 57
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 9.00
completed: 2026-08-21T14:34:33.896Z
---
## Executive Summary

- **(High Confidence)** <INFERENCE from="ECSS-E-ST-10-02C Rev.1 VCD requirements; FDA 2023 device-software guidance; FAA AC 20-189">A “remaining work” determination must be a **closed-world reconciliation**, not a filtered list of failed tests. Freeze the baseline, enumerate every applicable requirement, planned case, and open defect, then partition that universe into verified, remaining, approved exception, or approved-not-applicable sets. If any item is absent from the partition, the determination is invalid—not complete.</INFERENCE> ECSS requires a Verification Control Document that records each requirement, evidence, compliance as yes/no/partial, close-out as open/closed, and the reason; FDA requires traceable expected results, observed results, pass/fail determinations, and unresolved-anomaly records; FAA explicitly frames problem-report management as preventing loss of visibility of critical issues. [ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf) ([ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf?utm_source=openai)) [fda.gov](https://www.fda.gov/media/153781/download) ([fda.gov](https://www.fda.gov/media/153781/download)) [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf) ([faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf))

- **(High Confidence)** <INFERENCE from="FAA AC 20-189 closure states; FDA objective-evidence requirements; ECSS close-out model">The skill should use separate dimensions for **conformance, execution, evidence provenance, oracle adequacy, and disposition**. A single label such as “carried” or “pass” cannot establish that a requirement is verified.</INFERENCE> “Verified present” should require applicable, baseline-current, independently inspectable or observed evidence at or above the requirement’s oracle threshold, complete mandatory trace links, no contradictory adequate evidence, and no applicable open defect. Self-report alone remains `REPORTED_ONLY`; it does not become independently verified.

- **(High Confidence)** Blocked, inconclusive, carried, weak-oracle, stale, and reported-only items are all remaining work. Each must mechanically produce a child item: unblock the environment, add controllability or observability, build an oracle, rerun against the current baseline, or obtain independent evidence. An approved deferment or waiver is an **exception**, not a pass.

- **(High Confidence)** <INFERENCE from="ECSS VCD partial-compliance fields; FDA intended-coverage and statistical-testing guidance; ISO/IEC/IEEE 29119 test documentation model">No single “coverage percentage” is honest.</INFERENCE> At minimum disclose: planned cases, executed cases, determinate cases, passed cases, each nonpass status, applicable requirements, requirements with adequate observed evidence, reported-only requirements, approved exceptions, and orphans. “Pass rate among executed tests” must never be labelled “coverage” or “percent complete.” [ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf) ([ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf?utm_source=openai)) [fda.gov](https://www.fda.gov/media/73141/download) ([fda.gov](https://www.fda.gov/media/73141/download)) [iso.org](https://www.iso.org/standard/79429.html) ([iso.org](https://www.iso.org/standard/79429.html?utm_source=openai))

- **(High Confidence)** Default exit codes should be: `0 VERIFIED_COMPLETE`; `1 REMAINING_WORK`; `2 INDETERMINATE_INTEGRITY` for missing/unmapped/uncountable evidence; `3 TOOL_OR_POLICY_ERROR`; and `4 EXCEPTIONS_ONLY`. Exit `4` should remain nonzero by default so a campaign closed with waivers or deferments cannot be read as fully done.

- **(Medium Confidence)** Empirical evidence confirms material reporting drift. Snow, Keil, and Wallace found bias in **60%** of surveyed software-project status reports, with optimistic bias twice as likely as pessimistic; only an estimated **10–15%** of biased reports were accurate. The study used 56 usable project-manager surveys, so it is directly relevant but not a population estimate for all software organizations. [doi.org](https://doi.org/10.1016/j.im.2006.10.009) ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0378720606001145?utm_source=openai)) The canonical “90% done” and “watermelon status” labels are well-established practitioner descriptions, but robust software-specific effect-size evidence was not found.

- **(Medium Confidence)** Coverage and green test dashboards are weak evidence when denominators or suppressed results are hidden. Inozemtseva and Holmes generated **31,000** suites across five systems up to **724,000 lines of code** and found only low-to-moderate coverage/effectiveness correlation after controlling for suite size. [doi.org](https://doi.org/10.1145/2568225.2568271) Google reported that about **1.5%** of test runs were flaky, almost **16%** of tests exhibited some flakiness, and approximately **84%** of pass-to-fail transitions involved flaky tests. [testing.googleblog.com](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) ([testing.googleblog.com](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html?m=1&utm_source=openai))

- **(High Confidence)** <INFERENCE from="regulated traceability practices; TTCN-3 verdict semantics; software-testability literature">The most transferable safety-critical practices are not the document volume or certification bureaucracy; they are invariant denominators, bidirectional traceability, explicit unknown/inconclusive states, separate exception registers, independent closure, and generated testability work.</INFERENCE> These should be implemented directly in the agent’s schema and exit gate.

---

## Detailed Findings

### 1. Answer this decisively: How should a “remaining work” determination be constructed and gated when the evidence base is a partially-completed verification campaign?

#### Decisive construction rule

**(High Confidence)** The determination should be produced in nine ordered stages:

1. **Freeze the evaluated baseline.** Record PRD revision, feature-brief queue revision, registry revision, code/build identity, configuration, test environment, and defect snapshot.
2. **Construct the obligation universe.** Include every applicable PRD requirement, accepted feature-brief obligation, planned campaign case, and nonclosed defect. Do not start from executed tests.
3. **Build the trace graph.** Requirement → acceptance criterion → planned case or alternative verification method → evidence → defect/anomaly → disposition.
4. **Run anti-join integrity checks.** Find requirements without cases or approved alternative methods, cases without requirements or exploratory scope, defects without affected obligations, and nonpass cases without generated work.
5. **Evaluate evidence on multiple axes.** Keep verdict, execution state, provenance, oracle rung, baseline currency, and disposition separate.
6. **Derive requirement-level states conservatively.** Any adequate contradiction, open applicable defect, insufficient evidence, stale evidence, or incomplete mandatory verification prevents `VERIFIED_PRESENT`.
7. **Generate work from every gap.** Blocked, carried, inconclusive, reported-only, weak-oracle, and untraceable states each generate an explicit work item.
8. **Compute and disclose independent denominators.** Recompute from raw rows; do not trust precomputed dashboard totals.
9. **Apply exit-code gates.** Integrity failure takes precedence over an ordinary remaining-work result.

<INFERENCE from="ECSS per-requirement VCD; FDA requirement identification/tracking and anomaly records; FAA open-problem reporting">This sequence is the minimum design that mechanically prevents an unmeasured obligation from vanishing.</INFERENCE> [ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf) ([ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf?utm_source=openai)) [fda.gov](https://www.fda.gov/media/153781/download) ([fda.gov](https://www.fda.gov/media/153781/download)) [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf) ([faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf))

#### Closed-world invariants

**(High Confidence)** The implementation should enforce these invariants before ranking anything:

```text
REQ_UNIVERSE =
    VERIFIED_PRESENT
  ∪ ACTIVE_REMAINING
  ∪ APPROVED_EXCEPTIONS
  ∪ APPROVED_NOT_APPLICABLE

All four sets are pairwise disjoint.

Every applicable requirement has exactly one ledger disposition.
Every planned case has exactly one registry status.
Every nonpass planned case has one or more remaining-work or exception links.
Every open defect is represented in the ledger.
Every evidence record identifies the evaluated baseline.
Every reported summary total equals a total recomputed from raw records.
```

**(High Confidence)** A requirement with no evidence row is `UNKNOWN`, not absent from the output. A test removed after campaign start remains in the original planned denominator and receives a supersession, cancellation, or approved-scope-change record. A duplicate or conflicting identifier produces an integrity failure because the agent cannot prove that the universe is complete.

#### Required multi-axis state model

**(High Confidence)** Do not use one overloaded status field.

| Axis | Allowed values | Purpose |
|---|---|---|
| Conformance evidence | `supports_present`, `supports_absent`, `conflicting`, `indeterminate`, `none` | What the evidence says |
| Execution | `not_planned`, `planned_not_run`, `carried`, `blocked`, `executed` | What happened operationally |
| Evidence provenance | `independent_observed`, `observed_nonindependent`, `artifact_inspected`, `self_reported`, `unknown` | Who or what produced the claim |
| Oracle adequacy | `achieved_rung`, `required_rung`, `adequate:boolean` | Whether the verdict is epistemically strong enough |
| Baseline currency | `current`, `stale`, `unknown` | Whether evidence applies to the evaluated revision |
| Disposition | `open`, `satisfied`, `deferred_approved`, `waived_approved`, `deviated_approved`, `not_applicable_approved` | Governance decision |
| Defect state | `none`, `open`, `resolved_unconfirmed`, `closed_verified` | Whether a contradiction remains |

**(High Confidence)** FAA AC 20-189 provides an especially useful distinction: a problem is `resolved` after correction or full mitigation has been verified, but is only `closed` after formal review and confirmation of effective resolution. [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf) ([faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf)) That distinction should transfer directly: “developer says fixed” or even “fix implemented” is `RESOLVED_UNCONFIRMED`, not closed.

#### Taxonomy of remaining work

| Derived class | Mechanical rule | Generated work | Default gate | Confidence |
|---|---|---|---|---|
| `IMPLEMENTATION_DEFECT` | Adequate observed fail or applicable open defect | Fix, regression analysis, retest | Exit `1` | High |
| `CONFLICTING_EVIDENCE` | Adequate evidence supports both present and absent | Reproduce, adjudicate oracle/baseline | Exit `1`; `2` if provenance cannot be resolved | High |
| `NOT_YET_VERIFIED` | Mandatory evidence absent; executable means exist | Execute planned verification | Exit `1` | High |
| `CARRIED_FORWARD` | Case moved to later campaign without completed evidence | Schedule with owner and target baseline | Exit `1`, or `4` only after approved deferment | High |
| `BLOCKED` | Execution prevented by environment, dependency, data, access, or precondition | Remove blocker and rerun | Exit `1` | High |
| `UNVERIFIABLE_CURRENT_MEANS` | No feasible adequate control, observation, or oracle exists | Testability-enablement work | Exit `1` | High |
| `INCONCLUSIVE` | Execution occurred but no determinate adequate verdict resulted | Improve diagnostics/oracle; rerun | Exit `1` | High |
| `WEAK_ORACLE` | Pass/fail recorded below required oracle rung | Build stronger reference, assertion, or independent check | Exit `1` | High |
| `REPORTED_ONLY` | Requirement supported only by author/vendor/team attestation | Inspect artifact or execute independent check | Exit `1` | High |
| `TRACEABILITY_GAP` | Requirement, test, evidence, or defect is orphaned | Repair identifiers and trace links | Exit `2` if completeness is uncertain | High |
| `STALE_EVIDENCE` | Evidence baseline differs from candidate baseline without accepted impact analysis | Regression analysis and selective/full rerun | Exit `1` | High |
| `COVERAGE_GAP` | Declared criterion or required coverage item remains uncovered | Add cases or approved rationale | Exit `1` | High |
| `SCOPE_AMBIGUITY` | Conflicting, incomplete, or duplicate requirements prevent applicability decision | Requirements clarification/change control | Exit `2` | High |
| `APPROVED_DEFERMENT` | Authority accepted later completion with owner, target, rationale, and risk | Track to expiry/target | Exit `4` if no active work | High |
| `APPROVED_WAIVER_OR_DEVIATION` | Explicit authority accepted departure/nonconformance | Residual-risk monitoring and expiry review | Exit `4` if no active work | High |
| `APPROVED_NOT_APPLICABLE` | Applicability decision has authority and rationale | None; retain in total disclosure | Does not block `0` | High |

**(High Confidence)** A `pass` case can support `VERIFIED_PRESENT`; it cannot alone establish it. Requirement closure should require all of the following:

```text
applicable == true
traceability_complete == true
baseline_current == true
all mandatory obligations are:
    adequate observed pass
    OR formally superseded by an approved plan change
no adequate conflicting or failing evidence
no applicable open or resolved-unconfirmed defect
achieved_oracle_rung >= required_oracle_rung
coverage criteria met
final closure review recorded
```

**(High Confidence)** If policy intentionally accepts self-attestation for a low-risk requirement, classify it as `ACCEPTED_ATTESTATION` under approved exceptions, not `VERIFIED_PRESENT`. That preserves the distinction between “management accepted the risk” and “the behavior was independently established.”

#### Standard and regulatory crosswalk

| Standard/framework | Current reference as of August 2026 | Traceability and verification artefacts | Native status/exception semantics | Closure or deferment threshold | Access/license | Confidence |
|---|---|---|---|---|---|---|
| DO-178C / FAA | DO-178C dated December 13, 2011; FAA AC 20-115D remains active, issued July 21, 2017. [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf) ([faa.gov](https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D?utm_source=openai)) | Software Requirements Data, Design Description, source and executable code, Software Configuration Index, Software Accomplishment Summary; project verification data include verification cases/procedures/results, trace data, coverage analysis, and problem reports. FAA Order 8110.49A identifies requirements, design, code, executable, SCI, and SAS as minimum software type-design data. [faa.gov](https://www.faa.gov/documentLibrary/media/Order/FAA_Order_8110.49A.pdf) ([faa.gov](https://www.faa.gov/documentLibrary/media/Order/FAA_Order_8110.49A.pdf?utm_source=openai)) | DO-178C does not provide the proposed five-state requirement verdict enum. Unsatisfied objectives and anomalies remain visible through verification results, trace data, structural-coverage analysis, and problem reports. FAA AC 20-189 adds `recorded`, `classified`, `resolved`, and `closed` problem states. | Applicable assurance objectives must be satisfied. An open significant problem without sufficient mitigation or justification should be resolved before approval; closure follows verified resolution and formal confirmation. [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf) ([faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf)) | RTCA normative text proprietary; FAA recognition/guidance public | High for FAA overlay; Medium for inaccessible DO-178C clause details |
| DO-330 | DO-330 dated December 13, 2011 and recognized by AC 20-115D. [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf) ([faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf?utm_source=openai)) | Tool operational requirements, qualification planning, TQL-specific verification and configuration evidence, and an accomplishment summary; exact list depends on TQL and tool criteria. | Evidence concerns whether the tool can be credited for eliminating, reducing, or automating lifecycle activities. Tool output does not become trustworthy merely because the product appears to work. | Applicable DO-330 objectives must be met for the claimed qualification credit; changed tool or operational environment requires impact analysis and potentially re-verification or requalification. [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf) ([faa.gov](https://www.faa.gov/documentlibrary/media/advisory_circular/ac_20-115c.pdf?utm_source=openai)) | Proprietary normative text; FAA guidance public | Medium |
| ISO 26262 | Second edition, 2018; Parts 6 and 8 remain current while third-edition drafts are progressing. [iso.org](https://www.iso.org/standard/68388.html) ([committee.iso.org](https://committee.iso.org/cms/live/live/es/sites/isoorg/contents/data/standard/06/83/68388.html?browse=tc&utm_source=openai)) [iso.org](https://www.iso.org/standard/68390.html) ([iso.org](https://www.iso.org/standard/68390.html?browse=tc&utm_source=openai)) | Safety requirements specifications, safety planning, verification planning/specification/reporting, configuration/change records, confirmation measures, and the safety case. Part 8 officially covers safety-requirements management, configuration, change, verification, documentation, and tool confidence. | No universal pass/blocked/inconclusive requirement enum. Status is carried through requirements, work products, anomaly/change management, and the safety case. Tailoring or alternative evidence is a safety-governance decision, not a pass verdict. | An unverified safety requirement cannot honestly be marked verified. Any tailoring or residual anomaly must be justified, traceable, risk-assessed, and reconciled in the safety case and confirmation activities. | Paywalled | Medium |
| IEC 62304 | IEC 62304:2006+A1:2015, edition 1.1; IEC lists stability through 2028, and FDA recognizes the complete standard. [webstore.iec.ch](https://webstore.iec.ch/en/publication/22794) ([webstore.iec.ch](https://webstore.iec.ch/en/publication/22794?utm_source=openai)) [accessdata.fda.gov](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfstandards/detail.cfm?standard__identification_no=38829) ([accessdata.fda.gov](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfstandards/detail.cfm?standard__identification_no=38829&utm_source=openai)) | Development plan, requirements, architecture/design, unit verification, integration/system testing, configuration/release records, maintenance records, and software-problem-resolution records. | Uses problem-resolution and anomaly management rather than a universal requirement-verdict enum. | Release requires completion of applicable lifecycle work and evaluation/documentation of unresolved anomalies. Under FDA’s overlay, deferred anomalies need risk-based safety/effectiveness rationale. | Paywalled; official IEC abstract and FDA recognition public | Medium |
| FDA device-software guidance | June 2023 premarket guidance; January 2002 validation guidance remains listed as final. [fda.gov](https://www.fda.gov/media/153781/download) ([fda.gov](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-device-software-functions?utm_source=openai)) [fda.gov](https://www.fda.gov/media/73141/download) ([fda.gov](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-principles-software-validation?utm_source=openai)) | SRS and tracking method; traceability among hazards, requirements, design, tests, and risk controls; expected and actual results; pass/fail determination; test reports; version history; unresolved-anomaly list. | Objective pass/fail for protocols; unresolved anomalies remain a separate explicit list. Guidance is nonbinding but authoritative FDA policy. | Test reports should show acceptable execution and passing results; unresolved anomalies may be deferred only on a risk assessment for the candidate release. Each anomaly record includes description, discovery/root cause, impact, outcome, and rationale for not fixing. [fda.gov](https://www.fda.gov/media/153781/download) ([fda.gov](https://www.fda.gov/media/153781/download)) | Public | High |
| ISO/IEC/IEEE 29119 | Part 3 second edition, October 2021; Part 1 second edition, January 2022. [iso.org](https://www.iso.org/standard/79429.html) ([iso.org](https://www.iso.org/standard/79429.html?utm_source=openai)) [iso.org](https://www.iso.org/standard/81291.html) ([iso.org](https://www.iso.org/standard/81291.html?utm_source=openai)) | Test plan, test-design/case/procedure documentation, execution/results and incident records, test-status reports, and test-completion reports. Part 3 specifies documentation templates generated by Part 2 processes. | Test management records progress, results, incidents, deviations, and completion criteria. It is not a regulatory waiver framework. | Unexecuted or blocked tests may coexist with test-process completion only where the declared completion criteria and residual/deviation reporting make that fact explicit. They do not become passes. | Paywalled | Medium |
| ECSS | ECSS-E-ST-10-02C Rev.1, February 1, 2018; ECSS-Q-ST-80C Rev.2, April 30, 2025. [ecss.nl](https://ecss.nl/standard/ecss-e-st-10-02c-rev-1-verification-1-february-2018/) ([ecss.nl](https://ecss.nl/standard/ecss-e-st-10-02c-rev-1-verification-1-february-2018/?utm_source=openai)) [ecss.nl](https://ecss.nl/standard/ecss-q-st-80c-rev-2-software-product-assurance-30-april-2025/) ([ecss.nl](https://ecss.nl/standard/ecss-q-st-80c-rev-2-software-product-assurance-30-april-2025/?utm_source=openai)) | Verification Plan; Verification Control Document; test and review-of-design reports; software assurance records; problem/nonconformance reports. The VCD records requirement ID/text, traces, levels/stages, method, plan link, compliance evidence, compliance status, close-out status, and reason. | Explicit `yes/no/partial` compliance and `open/closed` close-out; evidence references can include reports, waivers, requests for deviation, and nonconformance records. | The VCD must provide evidence and reason for close-out; a customer/supplier Verification Control Board assesses requirement close-out. [ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf) ([ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf?utm_source=openai)) | Public | High |

<MISSING_DATA>[The full normative texts of DO-178C, DO-330, ISO 26262, IEC 62304, and ISO/IEC/IEEE 29119 were not publicly accessible in this investigation. Exact clause-by-clause field lists and tailoring language require licensed copies. Official regulator, ISO/IEC catalogue, and public ECSS materials were used instead.]</MISSING_DATA>

#### What transfers from regulated practice

**(High Confidence)** The following transfers directly to an ordinary repository:

- Stable IDs and bidirectional traceability.
- A frozen plan denominator and controlled scope-change history.
- Expected result, observed result, verdict, provenance, and baseline identity.
- Explicit partial, open, unresolved, and exception states.
- Independent confirmation before defect closure.
- A separate deviation/waiver register.
- Recomputed completeness and coverage totals.
- Release or merge gates that distinguish verified completion from accepted residual risk.

**(High Confidence)** The following should not be copied blindly:

- DAL/ASIL classifications where the product has no equivalent risk model.
- Certification-authority document volumes.
- Tool qualification unless automated evidence is being credited in place of human verification.
- Mandatory independence at every level regardless of consequence.
- Structural coverage targets treated as proof of behavioral completeness.

#### Required ledger fields

**(High Confidence)** At minimum, each requirement row should contain:

```yaml
requirement_id:
source:
source_revision:
requirement_text_hash:
applicability:
criticality:
owner:

planned_verification:
  method:
  case_ids: []
  required_oracle_rung:
  coverage_criterion:

evidence:
  provenance:
  observer:
  observed_at:
  baseline_id:
  artefact_uri:
  artefact_hash:
  expected_result:
  observed_result:
  verdict:
  achieved_oracle_rung:

campaign:
  execution_state:
  registry_status:
  blocker_code:
  blocker_owner:
  unblock_condition:

defects: []
conformance_state:
derived_remaining_class:
disposition:
disposition_authority:
disposition_rationale:
residual_risk:
target_baseline:
expiry_or_review_date:
generated_work_ids: []
```

**(High Confidence)** Summary values must be derived from these records. A hand-entered “90% complete” field should not be accepted as evidence.

#### Ranking the “actually remaining” ledger

**(High Confidence)** Rank lexicographically rather than by an opaque blended score:

1. **Integrity blockers:** missing baseline, missing obligations, duplicate IDs, orphan records, invalid statuses.
2. **Observed absence:** failing critical requirements and open severe defects.
3. **High-criticality unknowns:** blocked, conflicting, stale, or unverified safety/security/data-integrity requirements.
4. **High-leverage testability work:** one seam, simulator, fixture, or oracle that unlocks many blocked checks.
5. **Inconclusive and weak-oracle checks.**
6. **Unexecuted, carried, and reported-only checks.**
7. **Lower-criticality traceability and coverage gaps.**
8. **Approved exceptions**, ordered by residual risk and expiry.

**(High Confidence)** A useful deterministic sort tuple is:

```text
(
  integrity_failure,
  criticality,
  conformance_priority,
  open_defect_severity,
  number_of_blocked_items_unlocked,
  exception_expiry,
  age
)
```

Do not infer criticality from how many tests exist; sparse testing may itself indicate an evidence deficit.

#### Exit-code gates

| Exit | Symbol | Conditions | Meaning |
|---:|---|---|---|
| `0` | `VERIFIED_COMPLETE` | Universe is complete and partitioned; every applicable requirement is verified present with adequate current evidence; no active defects; no approved deferments/waivers | Fully verified against declared scope |
| `1` | `REMAINING_WORK` | Integrity is sufficient to calculate the ledger, but one or more active remaining classes exist | Ledger is trustworthy and work remains |
| `2` | `INDETERMINATE_INTEGRITY` | Missing/unparseable source, unknown denominator, orphan or duplicate IDs, unmapped requirement/case/defect, missing status, missing baseline, or totals do not reconcile | The agent cannot safely determine what remains |
| `3` | `TOOL_OR_POLICY_ERROR` | Schema failure, unsupported registry version, missing oracle policy, internal execution error | No valid determination produced |
| `4` | `EXCEPTIONS_ONLY` | No active work, but one or more approved deferments, waivers, deviations, or accepted attestations remain | Release may be authorized, but it is not “verified complete” |

**(High Confidence)** Precedence should be `3 > 2 > 1 > 4 > 0`. Exit `4` should be explicitly allowlisted by a release authority; the agent itself should not silently convert it to `0`.

#### Honest denominator disclosure

| Metric | Formula | Permitted label | Forbidden interpretation |
|---|---|---|---|
| Campaign execution | `executed / planned_baseline` | “Planned cases executed” | Percent complete |
| Attempt rate | `attempted / planned_baseline` | “Cases attempted” | Behavioral coverage |
| Determinate-plan coverage | `(adequate_pass + adequate_fail) / planned_baseline` | “Planned cases with determinate adequate verdict” | Pass rate |
| Pass against plan | `adequate_pass / planned_baseline` | “Planned-case pass coverage” | Product quality |
| Pass yield | `adequate_pass / (adequate_pass + adequate_fail)` | “Pass rate among determinate cases” | Test coverage or completion |
| Requirement evidence coverage | `requirements_with_adequate_observed_evidence / applicable_requirements` | “Adequately observed requirement coverage” | Requirements satisfied |
| Verified requirement coverage | `verified_present / applicable_requirements` | “Verified-present requirements” | Complete if unknowns are excluded |
| Reported-only share | `reported_only / applicable_requirements` | “Requirements supported only by report” | Verification coverage |
| Exception share | `approved_exceptions / applicable_requirements` | “Approved exception share” | Passed requirements |
| Trace completeness | `requirements_with_complete_required_links / applicable_requirements` | “Trace-complete requirements” | Behavioral correctness |
| Structural or model coverage | `covered_items / identified_items`, with named criterion | “Branch/MC/DC/state/transition/t-way coverage” | Complete behavior-space coverage |

**(High Confidence)** The report must also print raw counts for every registry status: pass, fail, blocked, inconclusive, carried, and invalid/unrecognized. An aggregate percentage without those counts is insufficient.

**(High Confidence)** For sampled or statistical testing, disclose:

- Population or sample frame.
- Selection method and operational profile.
- Sample size.
- Combination strength, if using t-way testing.
- Random seeds and repetitions.
- Configurations and environments included/excluded.
- What conclusion the sample supports.
- What it does **not** establish.

FDA’s validation guidance describes statistical testing as random data drawn from defined operational, hazardous, or malicious-use distributions and requires controls such as traceability analysis to ensure intended coverage. [fda.gov](https://www.fda.gov/media/73141/download) ([fda.gov](https://www.fda.gov/media/73141/download)) NIST’s combinatorial-testing guidance similarly makes the interaction strength and modeled parameter space part of the coverage claim; t-way coverage is not exhaustive behavioral coverage. [nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-142.pdf)

#### Unknown as a first-class result

**(High Confidence)** TTCN-3 defines five verdict values: `pass`, `fail`, `inconc`, `none`, and `error`; `inconc` is explicitly an inconclusive verdict, `none` is the initial absence of a verdict, and `error` denotes a test-system runtime error. [etsi.org](https://www.etsi.org/deliver/etsi_es/201800_201899/20187301/03.04.01_50/es_20187301v030401m.pdf) ([etsi.org](https://www.etsi.org/deliver/etsi_es/201800_201899/20187301/03.04.01_50/es_20187301v030401m.pdf?utm_source=openai)) These states must not be coerced to pass.

**(Medium Confidence)** Three-valued runtime-verification semantics use true, false, and inconclusive for finite observations that are not yet sufficient to determine an infinite-trace property. Four-valued models such as Belnap’s distinguish evidence for true, evidence for false, both, and neither. [doi.org](https://doi.org/10.1145/2000799.2000800) The practical mapping is:

| Epistemic value | Ledger meaning |
|---|---|
| True only | Adequate evidence supports present |
| False only | Adequate evidence supports absent |
| Both | Conflicting evidence |
| Neither | Unknown/no adequate evidence |

**(High Confidence)** This is preferable to Boolean coercion because conflicting evidence and absent evidence require different work. Conflict generates reproduction/adjudication; absence generates measurement.

<INSUFFICIENT_EVIDENCE>[Direct controlled studies showing that adding an `UNKNOWN` verdict to software-release dashboards alone improves release decisions were not found. Adjacent uncertainty-communication experiments indicate that numerical uncertainty can be communicated without necessarily destroying trust, but this is not a direct evaluation of test-campaign ledgers.]</INSUFFICIENT_EVIDENCE> [doi.org](https://doi.org/10.1098/rsos.181870)

#### Deriving new work from verification gaps

**(High Confidence)** Every nonpass status should have a deterministic work-item rule:

| Gap | Likely cause | Generated work item |
|---|---|---|
| Blocked by external dependency | No control over service response/state | Introduce seam, fake, service virtualization, or contract-test harness |
| State unreachable | Inadequate controllability | Add dependency injection, state setup API, simulator, fault-injection point, controllable clock/random source |
| Result unobservable | Inadequate observability | Add telemetry, structured logs, probe, query API, assertion surface, or deterministic export |
| No trustworthy expected result | Oracle problem | Build reference implementation, invariant, metamorphic relation, differential oracle, or human-reviewed golden set |
| Nondeterministic outcome | Scheduler/time/randomness/environment | Seed randomness, inject clock/scheduler, isolate environment, add repeat protocol |
| Data unavailable | Missing fixtures or prohibited production data | Build synthetic/anonymized fixtures and data-generation validation |
| Safety-critical state cannot be induced | Physical/operational constraints | Simulator, hardware-in-the-loop, model-based evidence, or approved alternative method |
| Self-reported only | Evidence provenance deficit | Independent artifact inspection or observation |
| Evidence stale | Changed code/configuration | Impact analysis plus targeted or full regression run |
| Carried | Scheduling decision | Owner, target baseline, due date, and approved-deferment decision |

**(High Confidence)** Freedman’s domain-testability formulation identifies controllability and observability as central to whether a component can be adequately tested. [doi.org](https://doi.org/10.1109/32.87282) A later systematic survey identifies testability transformation, assertions, improved controllability and observability, refactoring, and architecture/test interfaces as recurrent improvement techniques. [arxiv.org](https://arxiv.org/abs/1801.02201) ([arxiv.org](https://arxiv.org/abs/1801.02201?utm_source=openai))

<MISSING_DATA>[No credible, generalizable multiplier for “cost of retrofitting testability versus designing it in” was found. The literature supports the direction of effect, but measured costs are highly architecture-, domain-, and organization-specific. Repository histories with engineering-hours and blocker-resolution data would be needed for a defensible estimate.]</MISSING_DATA>

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

#### Current state of practice

**(High Confidence)** Standards converge on four principles even though they use different terminology:

1. Verification claims must trace to identified obligations.
2. Verification must produce inspectable evidence, not only assertions of completion.
3. Partial, anomalous, or nonconforming states remain visible.
4. Deferred or accepted nonconformance requires explicit rationale and authority.

The convergence is strongest in ECSS’s literal per-requirement VCD, FDA’s expected/observed/pass-fail and unresolved-anomaly records, and FAA’s distinction between resolved and formally closed problem reports. [ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf) ([ecss.nl](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf?utm_source=openai)) [fda.gov](https://www.fda.gov/media/153781/download) ([fda.gov](https://www.fda.gov/media/153781/download)) [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf) ([faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf))

**(High Confidence)** Standards do **not** generally define one universal requirement-status enum containing “verified present,” “verified absent,” “not verified,” “unverifiable,” and “waived.” Instead, those meanings are distributed across test verdicts, verification reports, traceability records, problem reports, coverage analysis, safety cases, nonconformance processes, and waiver/deviation records.

<INFERENCE from="multi-document standard practices">The agent should therefore normalize those semantics into its own explicit taxonomy rather than copy the status names of any one standard.</INFERENCE>

#### Empirical evidence of status drift

**(Medium Confidence)** Snow, Keil, and Wallace reported that software-project status reports were biased **60%** of the time in their survey, optimistic bias occurred about twice as often as pessimistic bias, and an information-theoretic model estimated only **10–15%** of biased reports were accurate. The sample comprised **56 usable surveys**, making the study relevant but vulnerable to self-report and scenario-design limitations. [doi.org](https://doi.org/10.1016/j.im.2006.10.009) ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0378720606001145?utm_source=openai))

**(Medium Confidence)** Keil, Mann, and Rai found that approximately **30–40%** of sampled information-systems projects exhibited some escalation, and the “completion effect” construct correctly classified more than **70%** of escalated and non-escalated projects in their model. Escalated projects had significantly worse perceived implementation and budget/schedule outcomes. [aisel.aisnet.org](https://aisel.aisnet.org/misq/vol24/iss4/4/) ([aisel.aisnet.org](https://aisel.aisnet.org/misq/vol24/iss4/4/?utm_source=openai)) This supports a last-mile mechanism: proximity to perceived completion can increase continued commitment even when remaining evidence is poor.

**(Medium Confidence)** Experimental and survey research on the “mum effect” shows organizational reluctance to transmit negative project news, especially when reporting threatens relationships, reputation, or responsibility. [jmis-web.org](https://www.jmis-web.org/articles/885) ([jmis-web.org](https://www.jmis-web.org/articles/885?utm_source=openai))

<INSUFFICIENT_EVIDENCE>[The familiar “90% done syndrome” and “watermelon project” labels could not be tied in this investigation to a strong, replicated software-specific estimate of prevalence or magnitude. They should be treated as practitioner shorthand for mechanisms supported by reporting-bias, escalation, and bad-news-suppression research—not as quantified laws.]</INSUFFICIENT_EVIDENCE>

#### Coverage drift and metric gaming

**(Medium Confidence)** Inozemtseva and Holmes’ ICSE study generated **31,000** test suites for five systems, the largest containing up to **724,000 lines of source code**, and found only low-to-moderate correlation between coverage and fault-detection effectiveness once test-suite size was controlled. Stronger coverage forms did not consistently provide stronger insight into effectiveness. [doi.org](https://doi.org/10.1145/2568225.2568271)

**(High Confidence)** <INFERENCE from="coverage/effectiveness evidence and Goodhart's law">A coverage target is useful as a searchlight for missing evidence, but dangerous as a completion objective. Once teams are rewarded for maximizing the number, they can add low-assertion tests, exclude difficult code, or exercise paths without verifying behavior.</INFERENCE>

**(Medium Confidence)** Mutation score is a better complementary measure of whether tests detect seeded behavioral changes, but it is not itself proof of correctness and can also be optimized mechanically. The safe policy is a portfolio: requirement evidence, risk/behavior coverage, structural coverage, mutation or fault-injection evidence where useful, and explicit residual gaps.

#### Silent skipping and flaky-test suppression

**(Medium Confidence)** Google reported that about **1.5%** of all test runs produced a flaky result, almost **16%** of tests had some associated flakiness, and about **84%** of observed pass-to-fail transitions involved flaky tests. Google also observed that legitimate failures can be dismissed when teams become accustomed to false signals. [testing.googleblog.com](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) ([testing.googleblog.com](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html?m=1&utm_source=openai))

**(Medium Confidence)** A Python ecosystem study estimated that, on average, approximately **170 reruns** would be required to obtain 95% confidence that a passing test was not flaky under its model and dataset. [arxiv.org](https://arxiv.org/abs/2101.09077) ([arxiv.org](https://arxiv.org/abs/2101.09077?utm_source=openai)) The number is not a universal rerun prescription; it demonstrates that a small fixed rerun count cannot establish non-flakiness.

**(High Confidence)** The agent should therefore treat:

- `skipped`, `disabled`, `quarantined`, and `filtered_out` as denominator-visible statuses;
- a pass obtained after failures as `pass_with_flaky_history`, not an ordinary clean pass;
- reruns as additional observations, not deletion of the first failure;
- classification as flaky as a hypothesis requiring evidence, not permission to discard the failure.

A recent empirical evaluation of **230,439 test failures** warns that flaky-failure classifiers can mistake true failures for flaky failures that are then ignored. [arxiv.org](https://arxiv.org/abs/2401.15788) ([arxiv.org](https://arxiv.org/abs/2401.15788?utm_source=openai))

#### Which interventions measurably reduced drift?

**(Medium Confidence)** The evidence base is much stronger for the existence of drift than for quantified effects of specific organizational controls.

| Intervention | Evidence status | Finding |
|---|---|---|
| Independent or externally reproducible evidence | Standards prescription; indirect empirical support | Reduces reliance on biased self-report, but no general cross-industry effect size was found |
| Fixed baseline denominators and automatic reconciliation | Strong standards prescription | Mechanically prevents denominator shrinkage; no direct controlled study of this exact agent design |
| Explicit test-status and completion reports | ISO/IEC/IEEE 29119 and ECSS prescription | Makes non-execution and partial compliance auditable |
| Separate anomaly/exception register | FAA/FDA/ECSS prescription | Prevents unresolved problems from being represented as ordinary passes |
| Flaky-test identification and reruns | Industry case evidence | Improves diagnosis, but Google reported that aggregate flake insertion and fix rates remained roughly balanced rather than eliminating flakiness. [testing.googleblog.com](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) ([testing.googleblog.com](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html?m=1&utm_source=openai)) |
| Mutation testing alongside coverage | Empirical construct-validity support | Reduces reliance on execution-only coverage, but no evidence shows immunity to gaming |
| Blame-reducing or face-saving reporting designs | Experimental mum-effect literature | Can affect willingness to report bad news; effect sizes were not verified here for production software campaigns |

<INSUFFICIENT_EVIDENCE>[No strong field experiment was found comparing release decisions with and without a closed-world “remaining work” ledger. The proposed gate is grounded primarily in standards logic, formal verdict semantics, and adjacent empirical evidence on reporting and test drift.]</INSUFFICIENT_EVIDENCE>

---

### 3. What are the contrasting viewpoints or competing evidence?

#### Strict closure versus risk-based acceptance

<CONFLICTING_EVIDENCE>[A strict interpretation says every planned check must execute and pass before completion. FAA/FDA/ECSS practice instead allows some unresolved anomalies, partial compliance, alternative methods, deviations, or waivers where risks and evidence are explicitly assessed and an authorized party accepts the result. The conflict is resolved by separating technical verification from governance disposition: an accepted exception may close active work, but it must not be relabelled as verified conformance.]</CONFLICTING_EVIDENCE>

**(High Confidence)** FAA AC 20-189 says significant open problems without sufficient mitigation or justification should be resolved before approval, which also means sufficiently mitigated and justified problems may remain open under controlled disposition. [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf) ([faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf)) FDA likewise permits unresolved anomalies to be deferred based on candidate-release risk assessment and requires a documented rationale for not correcting each one. [fda.gov](https://www.fda.gov/media/153781/download) ([fda.gov](https://www.fda.gov/media/153781/download))

**(High Confidence)** The agent should consequently maintain two outputs:

- **Technical truth:** verified, contradicted, unknown, conflicting.
- **Governance disposition:** open, deferred, waived, accepted, not applicable.

Mixing the two is the principal mechanism by which “accepted risk” gets misreported as “done.”

#### Scripted traceability versus exploratory or unscripted testing

<CONFLICTING_EVIDENCE>[Traditional regulated practice emphasizes predefined protocols, expected results, traceability, and formal reports. FDA’s February 2026 Computer Software Assurance guidance explicitly accepts scenario, experience-based, error-guessing, and exploratory testing, including cases with no step-by-step script. However, it still requires objective evidence of intended use, risk analysis, testing performed, issues, conclusion, performer, date, and approval where appropriate.]</CONFLICTING_EVIDENCE> [fda.gov](https://www.fda.gov/media/188844/download) ([fda.gov](https://www.fda.gov/media/188844/download))

**(High Confidence)** Therefore, “not scripted” does not mean “unmeasured.” An exploratory session may satisfy a requirement if it has:

- Identified objectives or charter.
- Scope and baseline.
- Observable evidence.
- A credible oracle or pass/fail criterion where applicable.
- Recorded issues and conclusion.
- Trace to the requirement or risk addressed.

It should not be counted as full coverage of unspecified behavior.

#### Coverage as a useful proxy versus a misleading target

<CONFLICTING_EVIDENCE>[Structural and technique coverage are useful for identifying what was not exercised. Empirical evidence shows they are weak proxies for defect detection when treated as stand-alone quality scores. Safety standards nevertheless require some coverage forms because unexecuted structures or untested requirements expose assurance gaps.]</CONFLICTING_EVIDENCE>

**(High Confidence)** The correct transfer is:

- Use coverage thresholds as **minimum evidence obligations**.
- Never treat the threshold as sufficient evidence of product correctness.
- Require meaningful oracles and requirement links.
- Keep exclusions visible.
- Report numerator and denominator origin.

#### Fail-closed unknowns versus risk-based unknowns

<CONFLICTING_EVIDENCE>[Formal verification and safety assurance favor preserving unknown or inconclusive outcomes. Commercial release processes may need to proceed despite some unknowns. Treating every unknown as an absolute prohibition can encourage teams to hide or redefine unknowns; treating unknown as pass creates false completion.]</CONFLICTING_EVIDENCE>

**(High Confidence)** The defensible policy is:

- Unknown is always technically nonpass.
- High-criticality unknowns block by default.
- Lower-criticality unknowns may be accepted only through explicit exception governance.
- Exceptions retain owner, residual risk, target, authority, and review date.
- Default machine exit remains nonzero.

#### Independent observation versus vendor or team attestation

**(Medium Confidence)** FDA’s 2026 assurance guidance allows manufacturers to leverage supplier assessments, vendor development practices, certifications, and existing validation evidence, especially for lower-risk supporting software. [fda.gov](https://www.fda.gov/media/188844/download) ([fda.gov](https://www.fda.gov/media/188844/download)) This supports risk-scaled evidence rather than mandatory re-execution of everything.

**(High Confidence)** It does not justify equating an unsupported statement with observed behavior. The agent should distinguish:

1. Claim only.
2. Inspectable supplier artifact.
3. Reproducible supplier test evidence.
4. Consumer-observed execution.
5. Independent or diverse confirmation.

The closure threshold can vary by criticality, but the provenance label cannot.

#### Designing testability versus retrofitting it

**(Medium Confidence)** The literature consistently treats observability, controllability, isolation, assertions, dependency management, and architecture-level test interfaces as testability factors. [arxiv.org](https://arxiv.org/abs/1801.02201) ([arxiv.org](https://arxiv.org/abs/1801.02201?utm_source=openai)) Recent work continues to study dependency injection and design-pattern refactoring as means of improving design-level testability. [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0950584924001162) ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0950584924001162?utm_source=openai))

<CONFLICTING_EVIDENCE>[Practitioner consensus strongly favors designing these capabilities in early, while generalizable empirical cost comparisons remain weak. Claims that retrofits are always a specific multiple more expensive should not be used without repository- or domain-specific data.]</CONFLICTING_EVIDENCE>

---

### 4. What changed recently, and what is the trajectory?

| Date | Change | Significance | Confidence |
|---|---|---|---|
| September 16, 2022 | FAA issued AC 20-189 on open problem reports. [faa.gov](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf) ([faa.gov](https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1032306?utm_source=openai)) | Adds a public, regulator-backed state model for recorded, classified, resolved, and formally closed problems, with reporting fields and disposition rules | High |
| June 14, 2023 | FDA issued current device-software premarket guidance, replacing the 2005 document. [fda.gov](https://www.fda.gov/media/153781/download) ([fda.gov](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-device-software-functions?utm_source=openai)) | Makes expected/observed/pass-fail evidence, traceability, version history, and unresolved-anomaly evaluation explicit | High |
| April 30, 2025 | ECSS-Q-ST-80C Rev.2 replaced the 2017 software product-assurance standard. [ecss.nl](https://ecss.nl/standard/ecss-q-st-80c-rev-2-software-product-assurance-30-april-2025/) ([ecss.nl](https://ecss.nl/standard/ecss-q-st-80c-rev-2-software-product-assurance-30-april-2025/?utm_source=openai)) | Current ECSS software-assurance baseline; continues the space-sector emphasis on assurance, traceability, test coverage, and problem management | High |
| February 2026 | FDA issued current Computer Software Assurance guidance for production and quality-management-system software, superseding its September 24, 2025 version. [fda.gov](https://www.fda.gov/media/188844/download) ([fda.gov](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-management-system-software?utm_source=openai)) | Moves toward risk-based, least-burdensome evidence and explicitly accepts unscripted testing while preserving objective records | High |
| 2026 | ISO 26262 third-edition drafts progressed for Parts 6 and 8; the 2018 editions remain the current published standards. [iso.org](https://www.iso.org/standard/68388.html) ([committee.iso.org](https://committee.iso.org/cms/live/live/es/sites/isoorg/contents/data/standard/06/83/68388.html?browse=tc&utm_source=openai)) [iso.org](https://www.iso.org/standard/68390.html) ([iso.org](https://www.iso.org/standard/68390.html?browse=tc&utm_source=openai)) | Revision is underway but draft text should not be treated as the current normative baseline | High |
| 2026 planning | IEC’s strategic plan targets IEC 62304 second edition publication in 2028; edition 1.1 remains current. [assets.iec.ch](https://assets.iec.ch/further_informations/1245/SMB_8704_SBP_20260414_135340.html) ([assets.iec.ch](https://assets.iec.ch/further_informations/1245/SMB_8704_SBP_20260414_135340.html?utm_source=openai)) | Medical-device software lifecycle standard is evolving, including pressure from AI/ML-enabled devices, but no second edition is yet normative | High |

**(High Confidence)** <INFERENCE from="FDA 2026, ECSS 2025, FAA 2022, ISO revision activity">The trajectory is toward **risk-scaled and increasingly digital evidence**, not toward accepting unmeasured work as complete.</INFERENCE> FDA expressly supports automated traceability, system logs, audit trails, and other digitally retained objective evidence. [fda.gov](https://www.fda.gov/media/188844/download) ([fda.gov](https://www.fda.gov/media/188844/download))

**(High Confidence)** The architectural implication for the agent is:

- Prefer machine-generated evidence and hashes over prose assertions.
- Permit scripted and unscripted methods.
- Scale oracle thresholds and independence to risk.
- Keep invariant traceability, denominator disclosure, anomaly visibility, and explicit exception authority regardless of method.
- Version the policy so future standard revisions do not retroactively alter historical campaign results.

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| (High) ECSS requires per-requirement compliance status, close-out status, evidence references, and reasons | European Cooperation for Space Standardization, ECSS-E-ST-10-02C Rev.1 | 2018-02-01 | **Primary standard; official ECSS publication.** Meets criteria because normative text and exact VCD fields are publicly available. | https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf |
| (High) FAA distinguishes recorded, classified, resolved, and formally closed problem reports | FAA AC 20-189 | 2022-09-16 | **Regulator guidance; official.** Directly defines states and closure semantics. | https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf |
| (High) Significant aviation OPRs lacking sufficient mitigation or justification should be resolved before approval | FAA AC 20-189 | 2022-09-16 | **Regulator guidance; official.** Direct disposition rule. | https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf |
| (High) FAA recognizes DO-178C and DO-330 as acceptable means of compliance | FAA AC 20-115D | 2017-07-21 | **Regulator guidance; official.** Establishes current recognized standards and dates. | https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf |
| (High) FDA recommends expected results, observed results, objective pass/fail determinations, and test reports | FDA, Content of Premarket Submissions for Device Software Functions | 2023-06-14 | **Regulator guidance; official.** Direct testing-documentation recommendation. | https://www.fda.gov/media/153781/download |
| (High) FDA unresolved-anomaly records include description, discovery/root cause, safety/effectiveness impact, outcome, and rationale for not fixing | FDA, Content of Premarket Submissions for Device Software Functions | 2023-06-14 | **Regulator guidance; official.** Exact anomaly-record fields. | https://www.fda.gov/media/153781/download |
| (High) FDA recommends traceability among hazards, requirements, design, and tests | FDA, Content of Premarket Submissions for Device Software Functions | 2023-06-14 | **Regulator guidance; official.** Exact traceability examples are provided. | https://www.fda.gov/media/153781/download |
| (High) FDA validation guidance states validation cannot be completed without an established SRS and requires intended coverage controls | FDA, General Principles of Software Validation | 2002-01 | **Regulator guidance; official.** Foundational validation policy still listed as final. | https://www.fda.gov/media/73141/download |
| (High) FDA’s 2026 assurance guidance accepts scripted and unscripted testing but requires objective evidence and issue disposition | FDA, Computer Software Assurance for Production and Quality Management System Software | 2026-02 | **Regulator guidance; official and current.** Exact record contents and testing approaches. | https://www.fda.gov/media/188844/download |
| (High) ISO 26262-8 officially covers requirements management, verification, documentation, configuration, change, and tool confidence | ISO 26262-8:2018 | 2018-12 | **Primary standard catalogue; official ISO.** Abstract verifies scope; full normative fields are paywalled. | https://www.iso.org/standard/68390.html |
| (High) ISO 26262-6 covers software safety requirements, unit verification, integration verification, and embedded-software testing | ISO 26262-6:2018 | 2018-12 | **Primary standard catalogue; official ISO.** Scope confirmed by official abstract. | https://www.iso.org/standard/68388.html |
| (High) IEC 62304 edition 1.1 remains current and is recognized in full by FDA | IEC and FDA recognition database | 2015-06 / recognition updated 2026 | **Primary standard catalogue and regulator database.** Current edition and recognition status. | https://webstore.iec.ch/en/publication/22794 |
| (High) ISO/IEC/IEEE 29119-3 specifies test-documentation templates produced by the Part 2 processes | ISO/IEC/IEEE 29119-3:2021 | 2021-10 | **Primary standard catalogue; official ISO.** Exact template content is paywalled. | https://www.iso.org/standard/79429.html |
| (High) TTCN-3 has pass, fail, inconclusive, none, and error verdict values | ETSI ES 201 873-1 | 2008-07 version retrieved | **Primary technical standard; official ETSI.** Exact verdict semantics. | https://www.etsi.org/deliver/etsi_es/201800_201899/20187301/03.04.01_50/es_20187301v030401m.pdf |
| (Medium) Software-project status reports were biased 60% of the time in the study; optimistic bias was twice as common | Snow, Keil, Wallace, *Information & Management* | 2007-03 | **Peer-reviewed empirical study.** Directly studies software-project status bias; limited by 56 usable surveys. | https://doi.org/10.1016/j.im.2006.10.009 |
| (Medium) Approximately 30–40% of sampled IS projects exhibited escalation; completion effect was the strongest classifier | Keil, Mann, Rai, *MIS Quarterly* | 2000 | **Peer-reviewed empirical study.** Direct IS-project survey with comparison group. | https://aisel.aisnet.org/misq/vol24/iss4/4/ |
| (Medium) Negative project news is subject to a mum effect | Smith, Keil, Depledge, *Journal of Management Information Systems* | 2001 | **Peer-reviewed experiment/model.** Directly addresses reluctance to report troubled project status. | https://www.jmis-web.org/articles/885 |
| (Medium) Coverage was not strongly correlated with test-suite effectiveness after controlling for suite size | Inozemtseva and Holmes, ICSE | 2014 | **Peer-reviewed empirical benchmark.** Large generated-suite study; limited number of subject systems. | https://doi.org/10.1145/2568225.2568271 |
| (Medium) Google observed 1.5% flaky runs, flakiness in almost 16% of tests, and flakiness in 84% of pass-to-fail transitions | John Micco, Google Testing Blog | 2016-05-27 | **Vendor engineering evidence.** First-party operational data; organization-specific rather than peer-reviewed. | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html |
| (Medium) Approximately 170 reruns were needed under the study model for 95% confidence that an average passing Python test was not flaky | *An Empirical Study of Flaky Tests in Python* | 2021 | **Primary empirical preprint.** Direct ecosystem study; number is model/dataset-specific. | https://arxiv.org/abs/2101.09077 |
| (Medium) Flaky-failure classifiers can cause true failures to be ignored | *230,439 Test Failures Later* | 2024 | **Primary empirical preprint.** Large failure-classifier evaluation. | https://arxiv.org/abs/2401.15788 |
| (High) Controllability and observability are core dimensions of component testability | Roy S. Freedman, IEEE TSE | 1991 | **Peer-reviewed foundational paper.** Primary formalization of domain testability. | https://doi.org/10.1109/32.87282 |
| (Medium) Testability improvement literature includes assertions, controllability, observability, transformation, refactoring, and test interfaces | Garousi et al., *A Survey on Software Testability* | 2018/2019 | **Systematic literature survey/preprint.** Meets criteria as scholarly synthesis, not vendor material. | https://arxiv.org/abs/1801.02201 |
| (Medium) Finite-trace runtime verification supports inconclusive/unknown verdict semantics | Bauer, Leucker, Schallhart, ACM TOSEM | 2011 | **Peer-reviewed formal-methods paper.** Primary semantics for runtime verification over incomplete observations. | https://doi.org/10.1145/2000799.2000800 |
| (Medium) Numerical uncertainty can be made explicit without necessarily destroying trust | van der Bles et al., *Royal Society Open Science* | 2020 | **Peer-reviewed behavioral experiments.** Adjacent evidence; not a software-release study. | https://doi.org/10.1098/rsos.181870 |
| (High) Combinatorial coverage claims must identify the modeled parameter space and interaction strength | NIST SP 800-142 | 2010 | **Government technical guidance.** Authoritative primary guidance for combinatorial testing. | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-142.pdf |
| (High) ECSS-Q-ST-80C Rev.2 replaced Rev.1 in 2025 | ECSS-Q-ST-80C Rev.2 official page | 2025-04-30 | **Primary standard; official ECSS.** Current revision status. | https://ecss.nl/standard/ecss-q-st-80c-rev-2-software-product-assurance-30-april-2025/ |
| (High) IEC plans IEC 62304 second edition for 2028 | IEC TC 62 Strategic Business Plan | 2026 | **Official standards-body planning document.** Indicates trajectory, not current normative status. | https://assets.iec.ch/further_informations/1245/SMB_8704_SBP_20260414_135340.html |

---

## Knowledge Gaps

### Standards-access limitations

<MISSING_DATA>[Licensed normative copies of DO-178C, DO-330, ISO 26262:2018, IEC 62304:2006+A1:2015, and ISO/IEC/IEEE 29119 were unavailable. A clause-level legal/compliance implementation would require licensed extraction of every applicable objective, work product, required field, tailoring rule, and closure criterion.]</MISSING_DATA>

<MISSING_DATA>[The exact generic deviation/waiver semantics for ISO 26262 and IEC 62304 could not be verified as a standard-wide status model. Both rely on broader safety, anomaly, change, and risk-management processes rather than the explicit ECSS RFD/RFW model.]</MISSING_DATA>

### Empirical limitations

<INSUFFICIENT_EVIDENCE>[No reliable software-specific prevalence or effect-size estimate was found for the named “90% done syndrome” or “watermelon status.” Reporting bias, escalation of commitment, and suppression of negative news are empirically supported; the labels themselves are not sufficiently quantified.]</INSUFFICIENT_EVIDENCE>

<INSUFFICIENT_EVIDENCE>[No strong multi-organization field experiment was found measuring how much invariant denominators, explicit unknown verdicts, or exception-only exit codes improve release decisions.]</INSUFFICIENT_EVIDENCE>

<INSUFFICIENT_EVIDENCE>[No defensible universal cost ratio was found for retrofitting testability versus designing it in.]</INSUFFICIENT_EVIDENCE>

<MISSING_DATA>[A targeted primary-literature review of silently skipped, disabled, or quarantined tests was not completed to a standard sufficient for prevalence estimates. The ledger should support these states regardless, because their omission mechanically changes denominators.]</MISSING_DATA>

### Repository-specific limitations

<MISSING_DATA>[The repository’s actual PRD, feature-brief schema, test-campaign registry, oracle-rung definitions, defect schema, and baseline/version semantics were not supplied. Exact counts, ranking, and exit status cannot be instantiated without those artifacts.]</MISSING_DATA>

<MISSING_DATA>[No policy was supplied mapping requirement criticality to minimum evidence provenance, oracle rung, permitted verification methods, or exception authority.]</MISSING_DATA>

### Epistemic limitations

<INSUFFICIENT_EVIDENCE>[Behavioral uncertainty-communication studies are adjacent evidence only. They do not establish that an explicit `UNKNOWN` status improves software-release outcomes in every organization.]</INSUFFICIENT_EVIDENCE>

<CONFLICTING_EVIDENCE>[Risk-based assurance supports accepting lower-intensity or supplier-provided evidence for low-risk functions, while strict independent verification provides stronger confidence. The appropriate threshold is product-risk dependent; provenance must remain visible under either policy.]</CONFLICTING_EVIDENCE>

---

## Recommended Next Steps

1. **Acquire and extract the licensed normative clauses.**  
   **Rationale:** Build a clause-level crosswalk for DO-178C/DO-330, ISO 26262, IEC 62304, and ISO/IEC/IEEE 29119 covering required records, trace links, anomaly handling, tailoring, and closure. This is necessary before claiming formal conformance rather than adopting analogous controls.

2. **Define and version the oracle/evidence policy.**  
   **Rationale:** For each criticality class, specify minimum provenance, oracle rung, permitted alternative methods, independence requirements, baseline-age limits, and exception authority. Without this, `pass` cannot be consistently converted to `VERIFIED_PRESENT`.

3. **Implement the closed-world invariants and exit codes before ranking.**  
   **Rationale:** The primary failure to prevent is omission. First implement universe construction, anti-joins, partition checks, raw-count reconciliation, and exits `0–4`; only then add prioritization or natural-language synthesis.

4. **Back-test the skill against historical campaigns.**  
   **Rationale:** Compare prior “done” reports with reconstructed ledgers. Measure vanished requirements, hidden nonexecutions, reported-only closures, stale evidence, orphan defects, approved exceptions, and later defect escapes. This supplies organization-specific evidence for whether the gate reduces drift.

5. **Instrument generated testability work.**  
   **Rationale:** Require every blocked or unmeasurable case to classify its deficit as controllability, observability, oracle, environment, data, dependency, nondeterminism, or traceability. Track engineering effort and unlocked checks so future build-versus-retrofit testability decisions are based on repository data rather than unsupported industry multipliers.

## Sources

- [ECSS-E-ST-10-02C Rev.1](https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf?utm_source=openai)
- [Content of Premarket Submissions for Device Software Functions](https://www.fda.gov/media/153781/download)
- [AC 20-189](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf)
- [General Principles of Software Validation - Final Guidance for Industry and FDA Staff](https://www.fda.gov/media/73141/download)
- [ISO/IEC/IEEE 29119-3:2021 - Software and systems engineering — Software testing — Part 3: Test do...](https://www.iso.org/standard/79429.html?utm_source=openai)
- [The effects of optimistic and pessimistic biasing on software project status reporting - ScienceD...](https://www.sciencedirect.com/science/article/pii/S0378720606001145?utm_source=openai)
- [Google Testing Blog: Flaky Tests at Google and How We Mitigate Them](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html?m=1&utm_source=openai)
- [AC 20-115D - Airborne Software Development Assurance Using EUROCAE ED-12( ) and RTCA DO-178( )](https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D?utm_source=openai)
- [FAA Order 8110.49A, Software Approval Guidelines](https://www.faa.gov/documentLibrary/media/Order/FAA_Order_8110.49A.pdf?utm_source=openai)
- [Advisory 
Circular 
 
U.S. Department 
of Transpor](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf?utm_source=openai)
- [AC 20-115C - Airborne Software Assurance](https://www.faa.gov/documentlibrary/media/advisory_circular/ac_20-115c.pdf?utm_source=openai)
- [ISO 26262-6:2018 - Road vehicles — Functional safety — Part 6: Product development at the softwar...](https://committee.iso.org/cms/live/live/es/sites/isoorg/contents/data/standard/06/83/68388.html?browse=tc&utm_source=openai)
- [ISO 26262-8:2018 - Road vehicles — Functional safety — Part 8: Supporting processes](https://www.iso.org/standard/68390.html?browse=tc&utm_source=openai)
- [IEC 62304:2006+AMD1:2015 CSV | IEC](https://webstore.iec.ch/en/publication/22794?utm_source=openai)
- [Recognized Consensus Standards: Medical Devices](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfstandards/detail.cfm?standard__identification_no=38829&utm_source=openai)
- [Content of Premarket Submissions for Device Software Functions | FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-device-software-functions?utm_source=openai)
- [General Principles of Software Validation | FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-principles-software-validation?utm_source=openai)
- [ISO/IEC/IEEE 29119-1:2022 - Software and systems engineering — Software testing — Part 1: General...](https://www.iso.org/standard/81291.html?utm_source=openai)
- [ECSS-E-ST-10-02C Rev.1 – Verification (1 February 2018) | European Cooperation for Space Standard...](https://ecss.nl/standard/ecss-e-st-10-02c-rev-1-verification-1-february-2018/?utm_source=openai)
- [ECSS-Q-ST-80C Rev.2 – Software product assurance (30 April 2025) | European Cooperation for Space...](https://ecss.nl/standard/ecss-q-st-80c-rev-2-software-product-assurance-30-april-2025/?utm_source=openai)
- [ES 201 873-1 - V3.4.1 - Methods for Testing and Specification (MTS); The Testing and Test Control...](https://www.etsi.org/deliver/etsi_es/201800_201899/20187301/03.04.01_50/es_20187301v030401m.pdf?utm_source=openai)
- [A survey on software testability](https://arxiv.org/abs/1801.02201?utm_source=openai)
- ["Why Software Projects Escalate: An Empirical Analysis and Test of Fou" by Mark Keil, Joan Mann e...](https://aisel.aisnet.org/misq/vol24/iss4/4/?utm_source=openai)
- [JMIS - Journal of Management Information Systems](https://www.jmis-web.org/articles/885?utm_source=openai)
- [An Empirical Study of Flaky Tests in Python](https://arxiv.org/abs/2101.09077?utm_source=openai)
- [230,439 Test Failures Later: An Empirical Evaluation of Flaky Failure Classifiers](https://arxiv.org/abs/2401.15788?utm_source=openai)
- [Computer Software Assurance for Production and Quality Management System Software](https://www.fda.gov/media/188844/download)
- [Measuring and improving software testability at the design level - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0950584924001162?utm_source=openai)
- [AC 20-189 - Management of Open Problem Reports (OPRs)](https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1032306?utm_source=openai)
- [Computer Software Assurance for Production and Quality Management System Software | FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-management-system-software?utm_source=openai)
- [SMB/8704/SBP](https://assets.iec.ch/further_informations/1245/SMB_8704_SBP_20260414_135340.html?utm_source=openai)
