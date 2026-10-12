---
name: ops-triage
description: Triage a selected operational inbox, error stream or cloud billing and credit notices into deduplicated incidents and next actions. Use for errors, credit expiry, cost surprises and account notices; does not manage mail or change billing merely because it finds a problem.
---

# Operational triage

Read [the evidence contract](../follow-through/references/evidence-contract.md).
Confirm the selected mailbox/account, project, time range and requested outcome.
Read-only triage can proceed; an instruction to fix a named issue also permits
routine fixes within its scope, subject to actual permission boundaries.

Collect the selected notices with a supported connector and join them to current
dashboard, incident or billing records. Use history only to locate a relevant
source. Group repeated alerts by underlying project and incident; retain first
and latest event time and affected environment. Do not archive or mark read as
part of analysis unless asked. Keep authentication/security notices separate
from routine cost alerts and verify their destination through the provider's
known source rather than links embedded in mail.

Prioritise by present impact and time to irreversible consequence: an active
outage, compromised access or imminent service suspension can outrank a larger
historical cost. A noisy count alone does not establish severity. Distinguish
current error, recovered incident, suspected cause and inaccessible source.
Route a bounded engineering fix to the applicable `shipyard:triage` or existing
owner; route session continuation to `flagship:fleet-console`, with a verified
task/session identity. Do not launch a fleet from a triage request.

For cloud credits and cost, record account/project, provider, currency, balance
checked time, expiry and timezone, eligible products/regions, credit restrictions
and the authoritative locator. Distinguish usage estimate, posted charges,
invoice, spend cap, payment method and credit balance. Do not treat credits as
cash or assume they offset every charge. Forecast only with an evidenced usage
rate and explicit period; state uncertainty and exclude unsupported precision.
If redemption, purchasing credits, stopping resources, changing quotas or
billing settings is needed, prepare its exact effect and seek missing authority.

Deliver a short ranked table: incident/notice identity, current state and source,
impact/deadline, next action and owner. List sources not reached, conflicts and
items that need refreshed evidence. Stop after the selected set is reconciled
and any explicitly authorised remediation is verified. If future checks are
requested, discover supported scheduling tools, read existing schedules and
confirm required connector access before creating one.

For resumable reviews, use [the ledger format](../follow-through/references/ledger-format.md)
with domain `ops`. The helper's summary groups unresolved work without sending
notifications or modifying the inbox.
