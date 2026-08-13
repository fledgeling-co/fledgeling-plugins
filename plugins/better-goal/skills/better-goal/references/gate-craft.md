# Writing the gates

A gate is a shell command plus a name. The guard runs it at the end of every
turn and reads the exit code; the run cannot end while one fails. This is the
whole of the harness's judgement, so the quality of a run is the quality of its
gates.

## The shape

```json
{ "name": "typecheck",
  "cmd": "pnpm typecheck",
  "detail": "pnpm typecheck 2>&1 | tail -n 20" }
```

**`name`** — short and greppable. It appears in the ledger, in the block reason,
and in `stuck_on` if the run ends on it.

**`cmd`** — exit 0 means passed. Nothing else about its output matters, which is
why it can be as noisy as it likes.

**`detail`** — optional, run only when `cmd` fails, and the only thing the run
sees about the failure. Keep it to the actionable tail: `tail -n 20`, a count,
the failing test names. The guard withholds it entirely on a repeated identical
failure, so it is a first-look aid, not the record.

## Four properties a gate needs

**Deterministic.** The same tree gives the same exit code. A gate that depends on
a live server, a network call or a booted simulator turns an infrastructure blip
into a failed gate, and the run then tries to fix code that was never broken.
Where a gate must touch a running thing, start it in the command and tear it down
in the same command.

**Fast enough to run every turn.** The guard's hook timeout is 1200s for all
gates together. A 20-minute suite as a gate means every turn ends 20 minutes
late; run the fast subset as the gate and the full suite as the final one.

**Scoped to this run.** `pnpm test` in a repo with pre-existing failures blocks
forever on work the run was never asked to do. Scope it — `pnpm test --
--run src/checkout`, or a grep for the specific regression — and say in the brief
what was excluded.

**Failing at the start.** Run each gate by hand before arming. A gate that
already passes verifies nothing; a gate that cannot pass is worse than no gate,
because the run will grind against it until `stuck_after` disarms.

## Ordering

Gates run in order and the guard reports every failure, not just the first — so
put the cheapest first for the common case where one obvious thing is broken, and
the slowest last. A run whose typecheck fails does not need to wait for the
browser pass to learn that.

## What to gate on, by kind of work

| Work | Gate |
|---|---|
| A feature | its own tests, scoped; typecheck; the acceptance spec exits 0 |
| A backlog sweep | `ls docs/features-to-triage/*.md` returns nothing; suite passes |
| A refactor | suite passes **and** a diff-shape check — no new `any`, no skipped tests |
| UI work | the design-review script's exit code, not a screenshot anyone reads |
| A migration | the old symbol has zero call sites **and** the suite passes |
| Docs or research | the artifact exists at a named path and exceeds a size floor |

That last row is the honest edge. Some work is genuinely narration-checkable;
say so when proposing it, gate on what can be gated (the file exists, the section
headings are present, the link check passes) and tell the user the real
verification is a human reading it.

## The brief carries what the gates cannot

Gates settle *whether* the run may stop. The brief at `docs/goals/goal-<slug>.md`
carries everything about *what to do*, and the run re-reads it each turn:

- the worklist, with per-item status — this is the run's memory, and it survives
  compaction where transcript narration does not
- the blocked-item policy (below)
- the resource ledger: which port, which simulator, which branch this run owns
- model and effort, where a script spawns runners
- `## Open questions`, appended to rather than asked aloud

## The blocked-item policy

An armed run does not pause for input. Without a stated fallback it asks a
question, burns a turn, and asks again. State it in the brief:

> If an item needs a decision only the user can make, write the question and your
> recommendation to the `## Open questions` section of this brief, mark the item
> `parked` in the worklist, and continue with every item that does not depend on
> it. Do not stop to ask.

## Bounds

Set all three in the state file. They are independent and each covers a different
way a run goes wrong:

- `max_iterations` — a run that makes no progress but keeps ending turns cleanly
- `deadline` — a run that grinds against a rate limit or an outage
- `stuck_after` — a run where the same gate fails identically, turn after turn

Without a bound the run ends at the block cap, silently, reported as completed.

## Shapes to avoid

| Shape | Why it fails |
|---|---|
| A gate that greps the transcript | Narration always claims success; that is failure mode #3 |
| `pnpm test \|\| true` | Exits 0 always. Verifies nothing and reads as a gate |
| One gate combining four checks with `&&` | The reason names the whole chain, not the broken link |
| A gate that writes to the repo | It runs every turn; a gate with side effects is a mutation loop |
| `sleep 300 && curl localhost:3000` | Slow, non-deterministic, and needs `--allow-private-network` reasoning it does not have |
| No gate at all, "just keep going" | That is a loop, not a goal — use better-loop |

## Worked example

Rough intent, as typed:

> divide the remaining work/fixes into md files in docs/features-to-triage then
> use /ship-fleet:ship-fleet to orchestrate and work on the entire remaining work
> until all items are complete

"All items" names no items, so nothing can count them; there is no check, so only
narration would settle it; there is no bound; and there is no blocked policy, so
it stalls on the first question. The gates that answer it:

```json
"verify": [
  { "name": "queue-empty", "cmd": "! ls docs/features-to-triage/*.md >/dev/null 2>&1",
    "detail": "ls -1 docs/features-to-triage/*.md | head -n 20" },
  { "name": "typecheck",  "cmd": "pnpm typecheck",
    "detail": "pnpm typecheck 2>&1 | tail -n 20" },
  { "name": "tests",      "cmd": "pnpm test -- --run",
    "detail": "pnpm test -- --run 2>&1 | grep -E '✕|FAIL' | head -n 20" }
],
"max_iterations": 60,
"deadline": "2026-08-10T09:00:00Z",
"stuck_after": 3
```

with the worklist, the `/ship-fleet:ship-fleet` concurrency of 3, the resource
ledger and the blocked policy in `docs/goals/goal-ship-remaining-work.md`.

Every part traces to a failure in `failure-modes.md`: the three gates to #3, the
brief pointer to #12, the blocked policy to #4, the bounds to #1, `stuck_after`
to #11.

## When composing with `/goal`

`/goal /better-goal <intent>` is supported and additive. The built-in's condition
is capped at 4,000 characters and judged on transcript text by a small model with
no tools, so keep it to one sentence naming the end state and the brief path, and
let the gates do the work:

```text
Every gate in .claude/goals/ship-remaining-work.json passes and the guard has
disarmed itself with end_reason=met. Worklist: docs/goals/goal-ship-remaining-work.md
```

`printf '%s' "$CONDITION" | wc -c` before proposing it.
