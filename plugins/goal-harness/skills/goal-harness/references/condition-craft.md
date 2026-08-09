# Writing the condition

The condition is the only text the evaluator ever sees besides the transcript.
It has 4,000 characters and it is read by a small fast model with no tools. Both
facts should shape it.

## The five parts

```
<end state>. Verify by <commands whose output lands in the transcript>.
Work from <brief path>; re-read it each turn.
Echo `GOAL-PROGRESS: <slug> <done>/<total> | <last item> | <blocked count>`
every turn before stopping.
If blocked: <policy>. Stop after <N> turns or <deadline>, reporting what remains.
```

**End state** — one measurable thing. "Every spec in docs/specs has status
Merged and `pnpm test` exits 0" beats "the backlog is complete". The judge is
answering yes or no; give it one question.

**Stated check** — the exact commands. The evaluator cannot run them, but a run
that has been told to run them will, and the output will be in the transcript
where the evaluator can read it. This is the whole trick.

**Pointer** — the brief holds the worklist. Re-reading it each turn is what stops
a long run drifting from the list it started with, and it survives compaction
where transcript narration does not.

**Progress line** — a fixed, greppable shape. It is what `status.sh` reads, what
the evaluator counts against, and what makes "has the goal been met?" answerable
in one line rather than a re-read of the session.

**Bound and blocked policy** — see below.

## Bounds

Always include one. `or stop after 40 turns` / `or stop at 2026-08-10T09:00`.
The run reports progress against the bound each turn and the evaluator can
settle it from the transcript, which means the goal ends by agreement rather
than by the block cap overriding it at turn nine.

The guard enforces the same bound independently from `.claude/goal-state.json`,
so the run is bounded whether or not the evaluator honours the clause.

## The blocked-item policy

A goal never pauses for input. A condition without a blocked policy produces a
run that asks a question, burns a turn, and asks again. State the fallback:

> If an item needs a decision only the user can make, write the question and
> your recommendation to the `## Open questions` section of the brief, mark the
> item `parked` in the worklist, and continue with every item that does not
> depend on it. Do not stop to ask.

## Length

Count before proposing. If it does not fit, the fix is always the same: move
detail into the brief and keep the pointer. Detail in the condition is read by a
small model every turn; detail in the brief is read by the run when it needs it.

```bash
printf '%s' "$CONDITION" | wc -c   # must be ≤ 4000
```

## Worked example

Rough intent, as typed:

> divide the remaining work/fixes into md files in docs/features-to-triage then
> use /ship-fleet:ship-fleet to orchestrate and work on the entire remaining
> work until all items are complete

What is wrong with it as a condition: "all items" names no items, so nothing can
count them; there is no check, so the judge reads narration; there is no bound,
so the block cap ends it; there is no blocked policy, so it stalls on the first
question; and `/ship-fleet:ship-fleet` may or may not be model-invocable on a
fire.

Hardened, 1,180 characters:

```text
Every brief in docs/features-to-triage/ has been triaged, planned, built and
merged, and all three gates pass on the integration branch: `pnpm typecheck`
exits 0, `pnpm test -- --run` exits 0, and `ls docs/features-to-triage/*.md`
returns no files. Run all three and show their output before claiming the
condition is met.

Work from docs/goals/goal-ship-remaining-work.md — re-read it at the start of
every turn; it holds the worklist, the per-item gates, the resource ledger and
the concurrency cap. Drive delivery with /ship-fleet:ship-fleet at a concurrency
of 3.

Echo this line every turn before stopping:
GOAL-PROGRESS: ship-remaining-work <merged>/<total> | <last item merged> |
blocked:<n>

If an item needs a decision only the user can make, append the question and your
recommendation to the `## Open questions` section of the brief, mark the item
`parked` in the worklist, and continue with every item that does not depend on
it — do not stop to ask. If a delivery agent has died, resume it through
workflow-resume before starting new work.

Stop after 60 turns or at 2026-08-10T09:00 local, whichever comes first, and
report the merged, parked and remaining counts.
```

Every clause traces to a failure in `failure-modes.md`: the three gates to #3,
the brief pointer to #10, the progress line to #6, the blocked policy to #4, the
resume clause to #5, the bound to #1.

## Shapes to avoid

| Shape | Why it fails |
|---|---|
| "until there's no remaining work" | No list, no count, nothing to settle |
| "and it looks good / feels polished" | No command can settle it and narration always claims it |
| "/some-skill-name" | Not a condition; see failure mode #2 |
| Five clauses joined by "and" | Judged by a small model; one clause fails and the reason names the wrong one |
| "keep going until I say stop" | Never met, so it runs to the cap and stops anyway — use a deadline instead |
| Anything with no bound | Ends at the block cap, silently |

## When nothing can be run

Some goals are genuinely narration-checkable — a research sweep, a document.
That is fine, but say so when you propose it: the run is being judged on what it
reports about itself, the guard can only bound it, and the honest verification
is a human reading the artifact. Put the artifact path in the condition so at
least its existence and size are checkable.
