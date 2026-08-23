# Tiered delegation — `tiered` mode

A mode in which **the perch binding decides the model, and the conductor keeps the judgement.**
Off by default. Everything below applies only when flagship is invoked with `tiered`.

Two sentences carry the whole design:

> **A session's directory determines its capability tier, because that is what the proxy binds on.**
>
> **A worker builds and reports; the conductor grades. Nothing crosses families to do it.**

## The topology

| Location | Binding | Serves | Role |
|---|---|---|---|
| `~/Dev` (root) | bound | Opus 5 `xhigh` / Fable 5 `high` | **Conductor** — flagship, ship-armada. Plans, grades, decides |
| `~/Dev/bella*` | bound | frontier | Full-capability project session |
| `~/Dev/atlas*` | bound | frontier | Full-capability project session |
| `~/Dev/diolog*`, `~/Dev/dAIolog` | bound | frontier | Full-capability project session |
| every other `~/Dev/<project>` | **unbound** | proxy default — `gemini-3.7-flash-high` | **Worker** — ship-fleet. Builds, reports `ready-to-verify` |

Binding ids are the directory name (`atlas-app`, `daiolog`, `orderly`, `warden`…). An unbound
directory falls through to the proxy default; that fall-through **is** the delegation, so there is
nothing for a skill to select.

**Do not name a model anywhere in a brief, a dispatch, or a skill invocation.** The binding is the
only control surface. A brief that names a model either contradicts the binding or duplicates it, and
both read identically until the day they disagree.

## What `tiered` changes

**1. `defer` is off.** All judgement stays in-family. `defer`, the out-of-family lanes, and
cross-family verify are not called — not because they are unreliable, but because the capability
gradient this mode creates is the mechanism, and mixing two mechanisms means neither is measurable.
Outside `tiered`, `defer` behaves exactly as it always has.

**2. Verification moves up one level.** ship-fleet already stops its runners before verify and spawns
the verify stage itself. Under `tiered` **the fleet conductor is a worker too**, so it stops at
`ready-to-verify` for the *item* and reports upward. **The bound conductor spawns verify.** The
structural rule is unchanged and now has a second reason: a builder cannot grade its own build, and a
weaker tier cannot grade a build at all.

**3. Worker briefs carry scaffolding that a conductor brief must not.** See below — this is the part
most easily got wrong, because the two instruction styles are opposites.

**4. The flag propagates.** Every skill invoked from a `tiered` session is invoked with `tiered`.
A mode that stops propagating is a mode that silently reverts halfway down the chain.

## The instruction asymmetry — the part that inverts

Anthropic's guidance for a frontier model and what a weaker worker needs are **opposites**, and the
same brief cannot serve both.

| | Bound conductor (frontier) | Unbound worker (cheaper tier) |
|---|---|---|
| Verification scaffolding | **Remove it.** Self-verifies; explicit instructions cause over-verification at no quality gain | **Add it.** Name the command, the expected exit code, and what to do on failure |
| Scope | One line is enough — deliver what was asked, at the scope intended | Enumerate deliverables. A categorical instruction ships as one item |
| Re-checks | Do not instruct. Compounds with its own behaviour | Instruct explicitly, with the check named |
| Investigation | Trusted to read before answering | State it: *never claim anything about code you have not opened* |
| Tests | Trusted | State that tests verify correctness and are never edited to pass |
| Subagents | **Cap explicitly** — delegates readily | Usually none. Say so |
| Progress | Narrate thinly | Structured state file, updated per item |

**The reason, stated so it generalises**: a frontier model's failure mode is doing *too much* —
over-verifying, over-delegating, widening scope. A weaker model's failure mode is doing *too little*
— skipping the check, satisfying the example rather than the requirement, reporting done on an
unrun gate. Instructions that correct one make the other worse.

## The worker brief

Hand a worker the complete specification up front, then leave it to run. Every brief carries:

```
<investigate_before_answering>
Never speculate about code you have not opened. Read the file before making any claim about it.
</investigate_before_answering>

Deliverables — every one of these, not a representative sample:
  1. …
  2. …

Gates — run each, and report the exit code you actually saw:
  <command>            expect 0
  <command>            expect 0

Write a high-quality, general-purpose solution. Tests verify correctness; they do not define it.
Never hard-code a value or special-case an input to make a test pass. If a test looks wrong, say so
rather than working around it.

Do not delegate to subagents.

When every gate passes, stop and report ready-to-verify with the exit codes. Do not merge, do not
push, and do not grade your own work — verification happens elsewhere by design.

If you cannot make a gate pass, stop and report which gate, the exit code, and what you tried.
A blocked report is a result. A gate reported green that you did not run is not.
```

The last two lines matter more than the rest. The failure this mode is most exposed to is a worker
reporting success on a gate it never ran, and the remedy is making the honest alternative explicit
and safe.

## What the conductor keeps

**Verify.** Every item, in fresh context, against the original requirements. The worker's report is
evidence about what the worker believes; the gate exit codes are evidence about the tree.

**Adjudication.** A worker reports everything it found. The conductor filters. Anthropic's own
guidance: a review prompt that says *be conservative* gets literal compliance and fewer findings —
so ask for everything and filter in a separate pass. Under `tiered` that pass is a different session
at a higher tier.

**Every irreversible act.** Merges, pushes, deploys, deletions. A worker's brief says so explicitly.

**The decision page.** Workers surface questions; they never resolve an operator's axis.

## Babysitting cadence

A cheaper tier needs attention at a rate a frontier fleet does not, and that attention is a real
resource — the conductor's context and turns.

- **Read the worker's gate exit codes, not its prose.** The prose is a claim; the code is a
  measurement. This is the ladder, applied to reports.
- **Expect more rounds per item.** Budget for it rather than reading a second round as failure.
- **A silent worker is not a working worker.** The idle probe reports status; a worker that has gone
  quiet mid-item has either finished, blocked, or stalled, and only asking separates them.
- **Cap the fleet by the attention it costs, not by the berths it needs.** Berths bound the CPU.
  Nothing bounds the conductor's turns except this rule.

## Verify the tier before trusting the topology

**This mode makes model identity load-bearing for correctness, so it has to be measured rather than
assumed.** Two failures, both observed on this machine:

- A conductor silently served by the cheap tier is **grading builds with the model the architecture
  says must not grade them.**
- A worker silently served by the frontier tier costs frontier prices for worker output.

Both are invisible from the launch options, because a proxy's deadline failover crosses vendor
boundaries without changing anything the caller can see. The check is free:

```bash
# what is actually serving a session — extract the key, never grep for a vendor name
grep -o '"model":"[^"]*"' <transcript>.jsonl | sort | uniq -c
```

**Read the served model from the response envelope or the transcript's `"model":` field.** A model's
own claim about itself is the weakest evidence available — a misrouted model has been observed
asserting *"Model check passed — I am Opus-class, proceeding"* while being served by another vendor
entirely. An in-prompt self-check is decoration.

Grep for the **key**, not the vendor: a transcript from work *about* models contains vendor names as
content, and a file-level grep matches all of them.

**When a tier check fails, the work is re-graded rather than merged.** The code may stand on its own
gate exit codes; the *judgement* came from a tier the architecture excluded.
