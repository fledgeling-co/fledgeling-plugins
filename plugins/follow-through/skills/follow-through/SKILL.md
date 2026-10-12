---
name: follow-through
description: Reconcile a bounded set of operational alerts, household follow-ups, research decisions or colleague commitments into evidenced next actions. Use when loose ends span these areas; route a single area to its dedicated skill. Does not start a monitor or contact anyone merely because an item is open.
---

# Follow through

Turn the requested loose ends into a short account of what is known, what changed,
and what can be done next. Keep the original request, time window and completion
condition: a review of yesterday's activity is not permission to manage the whole
inbox or start recurring work.

| Requested outcome | Skill |
|---|---|
| Errors, billing notices, cloud credits, operational inbox | `follow-through:ops-triage` |
| Parcels, returns, appointments, household administration | `follow-through:household-follow-up` |
| A choice supported by product or tool research | `follow-through:decision-brief` |
| Promises, dependencies and handoffs with colleagues | `follow-through:commitments` |
| Existing agents or a release session need continuation | `flagship:fleet-console` |
| Repeatable navigation, keyboard, theme and width checks | `test-campaign:ui-regression` |

Read [references/evidence-contract.md](references/evidence-contract.md) before
collecting sources or writing a ledger. Domain skills use the same contract; load
only the domain needed. Verify a referral is installed in the receiving runtime.
If it is absent, report the missing dependency and complete the bounded read-only
portion directly with this contract; do not claim the referral ran.

For a mixed request, keep one local ledger with domain-labelled items and one
summary, rather than four independent lists that repeat the same thread. An alert
about a delivery can belong to the household domain while retaining its email
source. Do not dispatch domain agents automatically.

The optional deterministic helper checks source links, duplicate identities,
freshness and completion claims, then prints the actionable and unresolved rows:

```bash
python3 <plugin-root>/scripts/ledger.py check <ledger.json>
python3 <plugin-root>/scripts/ledger.py summary <ledger.json>
```

Use [references/ledger-format.md](references/ledger-format.md) when retaining
state between runs. For a small one-off request a concise cited table is enough.
Store working evidence outside this reusable plugin, in the task's permitted
private workspace. No accounts, personal history or messages belong in plugin
examples.

For the design basis and limits of the evidence checks, see
[references/evidence.md](references/evidence.md).

Stop when the requested set has been reconciled and each row has either a proven
outcome, a next action, or a named blocker. If authorised execution is part of the
request, carry it through to the agreed outcome and verify it. A draft, scheduled
task, accepted handoff and completed outcome are different states. For future
work, use the runtime's supported scheduling tools only when the user asked for
it; check required connector access and existing schedules first.
