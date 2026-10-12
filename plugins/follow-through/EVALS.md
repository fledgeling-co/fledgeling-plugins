# Validation — 2026-09-30

No multi-family benchmark, paid research panel or no-skill baseline was run.
These results establish bounded fixture behavior and packaging, not comparative
productivity or reliability on live accounts. Naming and the compact icon/banner
were routine implementation choices under the authoring brief; no preference
interview or brand panel was run.

## Deterministic helper

`python3 -m unittest discover -s plugins/follow-through/tests -v`: **15 passed**.
Checks cover recent history versus current evidence, freshly reread old reports,
expired observations, future/timezone errors, duplicate identities, separate
accounts, cross-account joins, completion evidence, visible unknown next steps,
missing links, dismissals, unresolved denominators, malformed values and
read-only CLI behavior with nonzero failure exits.

The helper does not collect evidence, infer authority, verify source truth or
determine whether the selected freshness window is suitable. It deliberately
fails duplicate records instead of silently deleting one.

## Independent read-only skill smoke review

An independent subagent read the skills and five neutral cases without live
accounts, network, filesystem mutations or scheduling. Its observed outcomes:

| Fixture request | Result |
|---|---|
| Old credit email reread today; billing unavailable | Current balance/expiry unverified; named billing-access blocker; no redemption |
| Split parcel A reported delivered but missing, B dispatched | Separate shipment states; A receipt disputed; B receipt unknown; no contact |
| Old NAS research, current compatibility/price unknown | Conditional recommendation; exact library compatibility and price need evidence; no purchase/install |
| Drafting offer, later postponed relative deadline | Proposed/unverified promise, unresolved date; no overdue claim or send |
| Three of four UI variant cells pass; last blocked; mock capture | Three fixture-reported passes, one blocked; 3/4 exercised; mock not runtime evidence |

One defect was identified: the mandatory Clarify referral had no explicit fallback
when absent. The evidence contract now states to investigate first and use the
runtime's supported question mechanism for a residual user-owned choice, reporting
the missing skill without inventing a lint pass. No runtime skill-loading or live
connector success is claimed by this review.

## Remaining validation

Actual provider billing semantics, shipment proof, platform-specific compatibility,
colleague acceptance and native keyboard/focus behavior need current permitted
sources in a real invocation. Connector availability is discovered per runtime.
The UI skill is a focused entry point to the existing campaign harness; the
fixture review does not certify an app or approve a release. A future comparative
eval should test stale versus current state, scope preservation under authorised
execution and duplicate notification prevention against the same prompts without
the skills.

## Final repository checks

Seven new/coordinated skill frontmatters and UI metadata passed validation. The
follow-through Codex plugin manifest passed the staged plugin validator and was
verified byte-identical after integration. Repository reference checker: 79
skills, 1042 active files, zero errors; 15 external references remain runtime
discovery obligations. All 21 reference-checker tests passed. Catalogue gate
passed with 57 plugin entries, 9 groups and matching Claude/Cursor versions.
Unrelated existing Cursor manifests were hashed before and after generation and
all stayed unchanged. Diff whitespace checks passed.

Read-only helper smoke: a neutral mixed four-domain ledger passed check and
summary, retaining blocked/unverified items in its four-item denominator;
changing the old reported credit to actionable failed with exit 1 because no
fresh current source supports it. No connector, monitor or external mutation
was used. These smoke receipts are held in the authoring workspace, separate
from reusable plugin content.
