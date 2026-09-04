# Data contract

Two files. You write the first; `render.py` derives the second.

- `<project>/.status/project.json` — one project's data. Written by that project's agent.
- `~/Dev/.status/portfolio.json` — one row per project plus machine state. Derived.

Every field is optional except `project`, `updated` and `verdict`. **Leave a field out
rather than filling it with a zero.** The pages render absent, empty and zero as three
different things, and a false zero is the one that misleads: "no problems found" and
"nobody looked for problems" look identical once both are `0`.

## The six state words

`done` · `in-flight` · `needs-work` · `blocked` · `unmeasured` · `waived`

That is the closed set, collapsed from sixty variants observed in the corpus. Anything else
fails validation. `unmeasured` never renders in the pass colour — a check that examined
nothing is not a pass.

| word | means |
|---|---|
| `done` | finished and checked |
| `in-flight` | being worked on right now |
| `needs-work` | ran, did not pass |
| `blocked` | stuck, waiting on something |
| `unmeasured` | nobody checked this |
| `waived` | left undone on purpose, with a reason |

## project.json

```jsonc
{
  "project": "webhook-relay",              // required · the identity, not the directory name
  "updated": "2026-09-04T09:41:00+10:00",  // required · ISO-8601

  "verdict": {                             // required · the hero line
    "token": "needs-work",                 //   one of the six
    "number": "7 of 14",                   //   the binding number, at display size
    "unit": "tasks finished",              //   what the number counts
    "headline": "Two checks have never been tested.",   // one clause, ~90 chars
    "run_label": "third pass",
    "head_sha": "b7d41ae"                  //   7 chars; shown as "version"
  },

  // Where the work is — the Sankey. Each task appears once.
  "tasks": [{
    "id": "WEB-5081", "title": "Retry queue drains in order",
    "origin": "planned",                   // planned | carried over
    "stage": "code written",               // code written | being checked | not started
    "outcome": "done",                     // done | still going | stuck
    "version": "9c1f22a", "note": "merged",
    "blocked_by": "",                      // fill when outcome is stuck
    "waiting_hours": 0                     // hours stuck — places the dot on the dashboard
  }],

  // Checks that ran — bars against their own limit.
  "gates": [{
    "name": "Types line up",               // plain words, not "typecheck gate"
    "command": "pnpm -r typecheck",
    "exit_code": 0,
    "counts": "412/412",                   // "N/M" · a zero M forces state to unmeasured
    "state": "done",
    "kind": "types"                        // optional · build|tests|types|security|design|sign-off
  }],

  // Do the alarms work — the dumbbell. One row per check that was deliberately broken.
  "armed": [{
    "check": "Text contrast",
    "mutation": "lowered the contrast limit to 1 to 1",   // what we broke, in plain words
    "case_reddened": "no test noticed",
    "red": 0,                              // tests that failed when broken · 0 forces armed false
    "green": 38,                           // tests that pass normally
    "sha": "b7d41ae",
    "armed": false
  }],

  "findings": [{                           // Problems found — the beeswarm
    "id": "F-04",
    "score": 94,                           // 0-100 seriousness · places the dot
    "severity": "high",                    // high | medium | low
    "file_line": "src/gate/counts.ts:88",
    "claim": "a run that examined nothing is reported as a pass",  // one clause
    "state": "needs-work"
  }],

  // What we got wrong — the slopegraph. Four atoms, and all four are needed.
  "corrections": [{
    "earlier_claim": "All 14 tasks verified",
    "said_pct": 100,                       // what we claimed, as a percentage
    "true_pct": 64,                        // what was true
    "true_state": "9 of 14 were re-checked after the rebase; 5 were not.",
    "mechanism": "The run log from before the rebase was read as current.",
    "caught_by": "counts re-measured against the rebased tree"
  }],

  "coverage":    [{ "axis": "Screens on a phone", "covered": 6, "denominator": 24 }],
  "not_checked": [{ "axis": "Screens on a phone", "why_not": "No phone in the test setup." }],
  "not_done":    [{ "action": "Smoke run on Windows", "reason": "No Windows machine here.",
                    "what_would_unblock": "A Windows machine.", "size": "a few days" }],
  "artifacts":   [{ "path": "reports/checks-b7d41ae.md", "kind": "md",
                    "contains": "Every check and what it examined.", "open_first": true }],

  // Waiting on you — surfaces on the dashboard, sorted oldest first.
  "needs_you":   [{ "ask": "Staging database password", "kind": "credential",
                    "waiting_since": "2026-09-02T09:00:00Z",
                    "one_line": "Blocks the last two acceptance checks." }],

  "git": { "branch": "feat/WEB-5088-alarms", "commits_ahead": 7,
           "worktree_clean": false, "pushed": false }
}
```

## portfolio.json — derived, do not hand-edit

`render.py sync` builds each row from that project's own data and replaces the row with the
matching `project` value. The `project` field is the identity, not the directory name, so
renaming a directory keeps the row and changing `project` creates a second one.

```jsonc
{
  "updated": "…",                          // stamped by the script
  "machine": { "load_per_core": 0.78, "mem_free_gb": 6.4, "mem_total_gb": 32,
               "disk_free_gb": 128, "disk_total_gb": 926, "worktrees": 41 },
  "flight":  { "runners_live": 9, "runners_cap": 12, "wave": "round 7",
               "queued": 14, "parked": 3 },
  "projects": [ /* one derived row each — see below */ ]
}
```

`machine` and `flight` are the only hand-maintained parts, and they are portfolio-wide
rather than per-project, so a project run leaves them alone. A fleet orchestrator writes
them; when nothing does, those two zones render as not reported, which is accurate.

### How each row is derived

| row field | derived from |
|---|---|
| `verdict` | `verdict.token` and `verdict.number` |
| `done_of_total` | tasks with `outcome: "done"` over all tasks |
| `defects_open` | findings whose `state` is not `done` |
| `gates` | your checks grouped into the six kinds, **worst state wins** the cell |
| `remaining` | tasks with `outcome: "stuck"`, with their `waiting_hours` |
| `corrections`, `needs_you` | passed through unchanged |
| `coverage` | every axis summed into one covered-over-denominator |

The six gate kinds keep the dashboard heatmap rectangular — every project contributes six
cells however many checks it ran. A check with no `kind` is sorted by keyword from its name
and command, and falls back to `build`. Set `kind` explicitly where that guesses wrong; a
kind with no checks renders `unmeasured`, which is the honest reading.
