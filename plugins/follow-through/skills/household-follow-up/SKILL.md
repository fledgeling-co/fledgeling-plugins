---
name: household-follow-up
description: Reconcile selected deliveries, returns, appointments and household administration into current status and dated next actions. Use when a parcel or household loose end needs follow-up; does not purchase, book, return or contact a provider without applicable authority.
---

# Household follow-up

Read [the evidence contract](../follow-through/references/evidence-contract.md).
Keep the request bounded to the selected orders or household tasks. Use supported
mail/calendar/provider sources to discover identifiers, then confirm current
carrier, retailer or appointment state. Do not collect unrelated inbox content.

Join order, shipment and item identities deliberately. A split order can have
several shipments; one tracking event does not complete all of them. Deduplicate
carrier updates and retailer notices while retaining both locators. Confirm the
actual carrier and tracking id; similarly named vendors are not interchangeable.
Use neutral aliases in the summary rather than repeating addresses or telephone
numbers. Never put private order data in this reusable plugin.

Distinguish estimated arrival, dispatched, delivery attempt, carrier-reported
delivery, received by the household, return requested, handed to carrier and
refund posted. Carrier-reported delivery alone does not establish receipt when
the user is asking about a missing parcel; a return label does not prove a
refund. Resolve conflicting states at their authoritative source or mark them
unverified. Relative dates need the relevant local timezone and an absolute date
before they become reminders. Keep return eligibility and booking availability
separate from whether the user wants to act.

For each open item, give the next cheapest useful step, its deadline/window,
owner, evidence and blocking fact. Prepare a local support-message draft,
return checklist or appointment options when useful. External sends, return
submission, booking, cancellations and purchases require authority for that
action; review-only requests do not grant it. Respect budgets, private locations
and already answered preferences. Use `clarify:clarify` for a deciding fact that
only the user can supply.

Stop after status reconciliation and the authorised outcome is observed, or
after handing over named blockers. A requested reminder can be scheduled through
supported tools once timezone, target and required access are resolved; creating
the skill or finding a deadline does not authorise reminders. Check for an
existing reminder so repeat runs do not create duplicates.

For resumable reviews, use [the ledger format](../follow-through/references/ledger-format.md)
with domain `household`; record receipt/refund completion at the source appropriate
to the requested outcome.
