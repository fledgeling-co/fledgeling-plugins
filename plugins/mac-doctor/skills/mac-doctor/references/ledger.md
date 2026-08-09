# Findings ledger

Two artifacts per run, under `~/.claude/mac-doctor/`:

- `ledger.jsonl` — one JSON object per run, append-only. Machine-readable; this
  is what recurrence detection reads.
- `findings/<UTC timestamp>.md` — the human-readable report for that run.

## Stable finding IDs

Recurrence detection works by matching `id` across runs, so a target recorded as
`worktrees:dAIolog` one week and `stale dAIolog worktrees` the next reads as two
unrelated events and the trend is lost.

Build the `id` as `<kind>:<subject>`:

| kind | subject | example |
| --- | --- | --- |
| `disk` | target name | `disk:derived-data`, `disk:docker-volumes` |
| `worktrees` | repo name | `worktrees:dAIolog` |
| `cache` | tool name | `cache:npm`, `cache:cocoapods` |
| `orphan-family` | executable name | `orphan-family:docker-mcp` |
| `runaway-cpu` | process name | `runaway-cpu:bluetoothd` |
| `runaway-memory` | process name | `runaway-memory:node` |
| `fd-holder` | holder name | `fd-holder:playwright-server` |
| `stale-listener` | name and port | `stale-listener:next-dev:3200` |

Use the executable or tool name, lowercased, with versions and PIDs stripped.
Name a family for the thing that leaked — the leaf, not its wrapper.

## Run record

```json
{
  "run_id": "2026-08-09T05:20:00Z",
  "tier": "1d",
  "host_state": {
    "free_bytes_before": 121332826112,
    "free_bytes_after": 162135998464,
    "free_pct_before": 6.1,
    "free_pct_after": 8.2,
    "load_1m": 23.3,
    "process_count": 1259,
    "swap_used_mb": 6478
  },
  "reclaimed": [
    {
      "id": "cache:npm",
      "kind": "cache",
      "bytes": 10093173145,
      "gate": ["regenerable", "network_refillable"],
      "command": "npm cache clean --force",
      "action": "reclaimed"
    }
  ],
  "kept": [
    {
      "id": "disk:cocoapods",
      "bytes": 13958643712,
      "reason": "slow-refill cache; deferred to 7d proposal"
    },
    {
      "id": "stale-listener:next-dev:3200",
      "reason": "12 established peers; cwd matches active work in diolog-investor-portal"
    }
  ],
  "proposed": [
    {
      "id": "worktrees:dAIolog",
      "bytes_estimated": 48318382080,
      "count": 92,
      "gate_results": {"clean": 71, "uncommitted": 14, "unmerged": 7},
      "note": "only the 71 clean ones offered"
    }
  ],
  "needs_user": [
    {
      "id": "runaway-cpu:bluetoothd",
      "reason": "99 min CPU in 5h (~33% sustained), no connected devices; root-owned",
      "suggested_command": "sudo killall bluetoothd"
    }
  ]
}
```

`action` is one of `reclaimed`, `kept`, `proposed`, `deferred_to_user`,
`observed`.

## Field rules

**Always record bytes**, estimated or measured, and mark which. Over weeks this
is what distinguishes a target that is *growing* from one that is merely large —
and growth is what deserves a fix rather than a recurring sweep.

**Record `kept` as carefully as `reclaimed`.** A target skipped across thirty
runs while always idle is itself a finding, and only the kept entries make that
visible. A ledger that records only actions is a log of what the tool did, not a
picture of the machine.

**Record `needs_user` every run it persists**, not once. The count is the signal:
an item deferred fifteen times means the suggested command is wrong or the fix
needs automating, which is a different recommendation from one deferred once.

Keep `reason` to the specific observation that justified the verdict — counts,
sizes, connection state, gate results. A later run reads it to decide whether
the same thing is happening again, so a vague line costs the ledger its purpose.

## Reading the ledger for recurrence

Group by `id` across records and look for four shapes:

- **Recurrence** — an `id` in three or more runs is a leak, not an incident. It
  has survived being cleaned up, so cleaning it again will not fix it. This is
  the highest-value signal in the file.
- **Growth** — rising `bytes` for the same `id` gives the rate, which is what
  makes the case for a real fix. "43G, growing 4G/week" is an argument; "large"
  is not.
- **Chronic keeps** — always skipped, never serving anything. Either retire it or
  the gate does not understand it.
- **Ignored deferrals** — a `needs_user` item recurring many times means nobody
  is running the command.

Say how many runs the ledger holds and over what period. A conclusion from two
runs is weaker than one from thirty, and the reader should see which they have.
