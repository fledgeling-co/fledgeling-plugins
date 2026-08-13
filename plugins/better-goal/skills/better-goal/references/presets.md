# Presets

Two recipes that were previously hand-typed slash commands. They are kept here so
the shape survives; adapt the worklist and gates to the repo you are in rather
than pasting them verbatim.

## Backlog to zero, driven by ship-fleet

The most-used shape by a wide margin. It was
`~/.claude/commands/create-fleet-goal.md`, which set the goal condition to a
prose instruction and produced the failures in `failure-modes.md` (#1, #2, #4).
The recipe survives; the framing changes.

**Brief** (`docs/goals/goal-ship-remaining-work.md`) carries:

1. The orchestrator file refreshed first, so the worklist is real before anything
   counts against it.
2. Every remaining item, gap and issue moved into a brief in
   `docs/features-to-triage/` — check for `docs/features-for-triage/` too; both
   spellings exist across the portfolio, and writing to the wrong one produces a
   queue-empty gate that passes while the work sits in the other directory.
3. Delivery through `/ship-fleet:ship-fleet` at a stated concurrency.
4. The per-item gate for each ID.

**Gates** in `verify[]`:

| name | cmd |
|---|---|
| typecheck | `pnpm typecheck` |
| tests | `pnpm test -- --run` |
| queue-empty | `test "$(ls docs/features-to-triage/*.md docs/features-for-triage/*.md 2>/dev/null \| wc -l)" -eq 0` |
| agents-alive | the repo's workflow-resume check, where a fleet run is in flight |

The `agents-alive` gate and `watch.sh` between them are what the old command was
reaching for with "a monitor that validates you're still going". A delivery agent
dying is independent of whether the work is done, and a run that dies mid-turn
never reaches its own gates at all — the gate covers the first, the watcher the
second.

The worked example in `gate-craft.md` is this recipe.

## Finish what the previous run did not

Was `~/.claude/commands/create-goal.md`: *"Create a suitable goal under 4k chars …
that will keep you going until every single remaining item is done and the
previous goal I've given you is met, with a monitor that validates you're still
going."*

Everything in it is now structural rather than prose:

| The old ask | Where it lives now |
|---|---|
| "under 4k chars" | Not a constraint — gates are commands, not a condition string |
| "utilising existing skills where needed" | Preflight resolves each one and flags the non-model-invocable ones |
| "keep you going until every item is done" | The guard blocks on a failing gate; the block cap is raised so it can |
| "a monitor that validates you're still going" | `watch.sh` under `Monitor`, plus the ledger and `status.sh` |
| "the previous goal is met" | Read the prior brief and ledger, carry the unfinished worklist rows forward |

When continuing a previous run, read the old `docs/goals/goal-<slug>.md` and its
ledger first: rows already marked merged do not need re-verifying, and the parked
ones carry reasons that would otherwise be rediscovered the hard way. Use a new
slug — per-slug state means the old run's file stays readable as the record.

---

## Appendix: the originals, verbatim

Kept because `~/.claude/commands/` is not version-controlled, so deleting these
was otherwise irreversible. Both were removed on 2026-08-09 in favour of this
skill.

### `create-goal.md`

```text
Create a suitable goal under 4k chars, utilising existing skills where needed that will keep you going until every single remaining item is done and the previous goal i've given you is met, with a monitor that validates you're still going (as you currently seem to stop working despite the goal being set)
```

### `create-fleet-goal.md`

```text
/goal Ensure that the orchestrator file is up to date and move any remaining items, gaps or issues into md files within docs/features-to-triage (or docs/features-for-triage if applicable) then use /ship-fleet:ship-fleet to orchestrate and carry the remaining items through the pipeline until there's no remaining work. utilise existing skills where needed that will keep you going until every single remaining item is done, with a monitor that validates you're still going (as you currently seem to stop working despite the goal being set and not met)
```
