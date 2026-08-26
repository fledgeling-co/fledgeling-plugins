# {{PRODUCT}} — What research was bought, and what was not

## The gate

| Question | Already in the repo? | Would it change the decision? | Free lane enough? | Bought? |
|---|---|---|---|---|
| {{GATE_ROWS}} | | | | |

A skipped panel is a decision with a reason. This table is the reason.

## Panels dispatched

| Panel | Archetype | Members | Completed | Cost band | Reconciled |
|---|---|---|---|---|---|
| {{PANEL_ROWS}} | | | | | |

**Reserved:** {{RESERVED}} at band-top · **Reported actual:** {{ACTUAL}}
Budget ledgers reserve high and reconcile lower. Both numbers are here because
only one of them is the invoice.

## Members that did not complete

| Member | Why | Cost |
|---|---|---|
| {{FAILED_ROWS}} | | |

A CLI refusing at startup on a binary-identity check costs $0 and is recorded
rather than chased.

## Free lane

{{FREE_LANE}}

What `research_local_start`, `reddit_gather` and `youtube_gather` covered
without spending anything, and what they could not reach.

## Grounding and disclosure

**Product documents shared with a third-party API:** {{UPLOADED}}
**Kept local:** {{LOCAL_ONLY}}

`corpusStores` uploads to Google. Anything unpublished went through
`research_ground` with the local destination instead, or was not shared.

## Verification run

| Gate | Scope | Result |
|---|---|---|
| `research_verify_citations` | {{CITE_SCOPE}} | {{CITE_RESULT}} |
| `research_verify_claims` (judged) | {{JUDGE_SCOPE}} | {{JUDGE_RESULT}} |
| `research_counter_review` | {{CR_SCOPE}} | {{CR_RESULT}} |
| `research_synthesise` | {{SYN_SCOPE}} | {{SYN_RESULT}} |

Four counter-review lenses finding nothing is a failed review, not a clean bill
of health.

## What was deliberately not researched

{{NOT_RESEARCHED}}
