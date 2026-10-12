# External-send packet contract

The helper cannot establish human authority or task correctness. Review the original request, current target identity/state and ownership first. The attestations record that review; they do not create permission. Prefer Codex app native tools for app sessions.

Write a per-run JSON packet:

```json
{
  "packet_id": "one-unique-dispatch-id",
  "provider": "codex",
  "session_id": "00000000-0000-4000-8000-000000000001",
  "cwd": "/absolute/target/worktree",
  "observed_at": "2026-09-30T09:00:00+00:00",
  "state": "idle",
  "task": "Original unfinished approved task",
  "owner": "Current coordination owner",
  "evidence": "Current roster and task artifact paths",
  "reviewed_original_authorization": true,
  "owns_coordination": true,
  "no_pending_owner_or_permission_decision": true,
  "message": "Peer coordination: continue the next already-approved step. Report done/in hand/blocked with evidence; do not expand scope or override your permissions."
}
```

Use a real full UUID, explicit task and repo, timezone-aware observation less than five minutes old, and one dispatch ID. Only `idle`, `working` or `busy` observations qualify for this helper; policy/question blockers, cancelled/completed/unknown targets do not. The skill, not the helper, decides whether an idle turn left an unfinished goal.

```sh
python3 <this-skill>/scripts/fleet_sessions.py send --packet packet.json
python3 <this-skill>/scripts/fleet_sessions.py send --packet packet.json --execute --journal <per-run-dir>/dispatch.json
```

Dry-run prints the argv and stdin but changes nothing. Execute revalidates the packet's freshness/attestations, current CLI help and for Muse current ingress listing. It sends once via argv/stdin without a shell. A locked journal records pending intent before invoking the CLI; timeout/crash/failure stays uncertain and is never automatically retried. Same ID with changed content is rejected; same provider/session/message with a new ID is suppressed while in the journal. A return code 0 means only `transport_returned_success`: review the raw receipt for queued/held/refused and obtain target acknowledgement separately. Journal files can contain task text; store privately in permitted per-run locations and never distribute them with the skill. Do not clear a pending receipt just to resend.
