# Optional ledger format

The helper reads a JSON file; it never fetches sources, changes accounts, infers
consent or writes the file. Keep it in the private task workspace. Version 1:

```json
{
  "schema_version": 1,
  "goal": "Review the selected operational notices",
  "stop_condition": "Every selected notice has an outcome or next action",
  "as_of": "2026-09-30T12:00:00Z",
  "sources": [{
    "id": "billing-1",
    "kind": "current",
    "scope": "example-project",
    "locator": "fixture://billing/project-1",
    "observed_at": "2026-09-30T11:58:00Z",
    "event_at": "2026-09-30T11:58:00Z"
  }],
  "items": [{
    "id": "notice-1",
    "domain": "ops",
    "scope": "example-project",
    "identity": "credit-expiry-1",
    "state": "actionable",
    "summary": "A credit expires before the next planned workload",
    "evidence": ["billing-1"],
    "volatile": true,
    "max_age_hours": 1,
    "next_action": "Prepare the workload timing options",
    "owner": "operator"
  }]
}
```

Domains: `ops`, `household`, `decision`, `commitment`. States: `unverified`,
`actionable`, `waiting`, `blocked`, `completed`, `dismissed`. A dismissed item
needs a `reason`; a completed item needs `completion_evidence` naming current
sources plus `outcome` describing the observed result. Completion evidence must
also appear in `evidence`. A draft or sent message only completes a request whose
agreed outcome was exactly that draft or send.

Kinds: `current` (direct source state), `reported` (a message or assertion),
`history` (recorded observation). All source timestamps must include a timezone.
`observed_at` is the source observation/check time, not the ledger creation time.
`event_at` may be omitted when genuinely unavailable. For email, use `reported`
with its message time; use `current` only for a direct current-state source.
For volatile items, only current evidence checked within `max_age_hours` supports
an actionable/waiting/completed state. Future timestamps, missing or stale
evidence and unresolved duplicates fail validation; downgrade affected rows to
`unverified` or `blocked` until checked. The helper validates the stated contract,
not the truth of the source or whether the chosen freshness window is suitable.

Duplicate `(domain, scope, identity)` rows fail rather than silently merging.
Consolidate their evidence and reconcile the state yourself. Source scope must
match item scope: if a decision spans accounts, explicitly use a shared decision
scope and retain each actual account in the locator or source metadata. Do not
invent a join across accounts. Unknown rows can have no evidence and must name
the missing source in `next_action`.
