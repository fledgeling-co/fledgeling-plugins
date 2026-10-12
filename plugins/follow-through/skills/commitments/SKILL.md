---
name: commitments
description: Recover and reconcile commitments and colleague handoffs from selected conversations or documents, separating proposals, promises, acceptance and completion. Use for what was promised, who owns the next step and what remains outstanding; sends and task updates require applicable authority.
---

# Commitments and handoffs

Read [the evidence contract](../follow-through/references/evidence-contract.md).
Freeze the selected people/conversations, dates and requested outcome. A review
of commitments is read-only; an instruction to carry out a named commitment
permits its bounded work. It does not grant authority to contact every person
mentioned in historical activity.

Read enough of each selected conversation to establish the promise in context,
including later amendments and cancellations. Use a connector/document source
over history whenever available. Capture stable thread/message or document
revision identity, speaker, promised deliverable, owner, recipient/dependency,
due date with timezone, condition and acceptance evidence. Attribute statements
to the speaker; do not turn a suggestion, unanswered request, model proposal or
calendar event into a human promise. A relative date without a resolved timezone
is a missing fact rather than a precise deadline.

Join repeated references to the same deliverable without merging two colleagues'
independent promises. Preserve changes: a later agreement can supersede a date,
but silence does not accept a handoff or cancel a promise. An outbound message
proves attempted delivery, a remote acknowledgement proves acceptance, and the
agreed artifact/effect proves completion. Recheck the current destination and
artifact access before proposing a send; a display name alone is insufficient.

Give a short table of confirmed, proposed, waiting, completed and unverified
commitments, ordered by deadline/dependency. Each row names who owes what to whom,
the evidence, what changed and the next action. Include cancelled/superseded
items when needed to prevent an old promise being revived. Do not declare an
item overdue when its date or current status is unknown.

Prepare a local handoff packet with task, owner, input artifacts, scope, writable
paths, tools, required output, acceptance evidence and stopping condition. A
colleague-facing draft states the actual progress and precise blocker without
promising work the user did not authorise. Sending email/chat, inviting people,
assigning tasks or changing a tracker needs applicable authority. Existing agent
session handoffs route to `flagship:fleet-console`; substantive feature readiness
routes to `shipyard:triage`. Check the receiving runtime exposes the skill before
claiming it ran.

Stop when the requested commitments are reconciled and authorised handoffs or
deliverables have their evidence. If a request includes future reminders, use
supported scheduling and deduplicate existing tasks; never silently start an
ongoing colleague monitor. For retained state use [the ledger format](../follow-through/references/ledger-format.md)
with domain `commitment`; observed completion must match the original deliverable.
