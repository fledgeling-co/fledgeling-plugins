# Oracle construction — what to do when nothing can settle a case

A case resolves to `unoracled` when no property is specified that any check could
read. That is not a measurement failure and no better instrument fixes it. It is a
specification gap, and the remedy is to build the missing oracle before any
authority tries to close the item.

This file is the ladder for building one, and the order matters: each rung is
cheaper and more durable than the one below it, so stop at the first that holds.

## Why this is a separate status from `inconclusive`

The two arrive looking identical and have opposite remedies.

| Status | The check | The fix |
|---|---|---|
| `inconclusive` | a property exists; the instrument was applied and could not measure it | a better instrument, or a lane that can observe it |
| `unoracled` | no property was ever named that a check could read | write one |

Reading them as one status sends half the work to the wrong place. A verification
pipeline that cannot tell "nobody looked" from "there is nothing to look at" will
keep applying authority to the second, which is the case that cannot be settled by
authority at any tier.

The distinction is not new here. A screenshot-judging pass over fifty surfaces once
returned inconclusive on all fifty, and the record of it was careful to say the
verdicts were "for want of a judge rather than for want of an oracle" — the two
halves named, in one sentence, and then collapsed into one status by every tool
downstream.

## The ladder

Work down it. The first rung that holds is the answer; do not build two.

### 1. A specification-sourced outcome assertion

Where the requirement inventory names an effect, assert the effect. This is the
strongest rung and usually the one people skip, because reading the specification
is slower than reading the build.

Source it from the specification, never from the implementation. Test-generation
tools demonstrably validate faulty behaviour, and code already in context biases
later generation toward mutually consistent but incorrect implementation/test
pairs. An oracle read off the build is a description of the bug.

This rung is unavailable when the specification names no effect. That is a finding
about the specification and worth reporting as one.

### 2. A metamorphic relation

Where no absolute answer is available, a relation between two runs often is. This
is the standard answer to the oracle problem and it is what makes an unoracled case
tractable without a baseline.

Two shapes carry most of the value:

- **Invariance** — a transformation that must not change a property. Rotating a
  device does not change the number of items in a list; switching locale preserves
  every affordance; re-running an idempotent action leaves one record.
- **Monotonicity** — a transformation with a guaranteed direction. Applying a
  filter never increases the result count; adding a permission never removes a
  control; sorting is a permutation of the same set.

A relation is worth more than a hardcoded assertion because it survives the data
changing, which is the usual reason a UI assertion rots.

The published evidence here is directional rather than settled: the component-level
work is a 2026 preprint without independent replication, and no quantitative
return-on-effort figure exists for metamorphic testing in UI-driven enterprise
applications. Treat the technique as sound and the sizing as unmeasured.

### 3. A property-based invariant

Where the surface has a contract expressible as a logical property, state the
property and let a generator attack it. This works on contracts — round-trips,
normalisation, serialisation, state-machine legality — and it works badly on
appearances.

The known failure mode is trying to express nuanced visual behaviour as a rigid
property. Where a shrinker exists, it earns the rung on its own: a failure reduces
to the minimal input sequence that caused it, which turns a long agent trace into
something a person can act on in a minute.

### 4. Record it as permanently unoracled

When no rung holds, say so in structural terms that survive: *this lane exposes no
accessibility tree*, *the only reachable database is production*, *the requirement
names a judgement no property expresses*. Then let it count against the total.

The move to resist is marking it `n/a`. `n/a` says the check does not apply here;
`unoracled` says it applies and nothing can perform it. Converting the second into
the first raises the score and lowers what the campaign knows.

## Two constraints on generating oracles

**Generate against the coverage model, never free-form.** Roughly half of
LLM-generated test plans are duplicates of cases that already exist — one study
classified 50.5% duplicates and 22.5% invalid or out of scope, leaving 27% valuable
and new. Deduplication is therefore most of the work rather than a polish step, and
the way to get it is to hand the model a cell from the coverage model and ask for
an implementation, rather than asking it what to test.

**The model that wrote the code may not be the sole oracle for it.** Use a separate
context given the requirements and the public contracts, not the implementation
output. Where the item's own ticket is the specification, note that the same
pipeline may have written both, and prefer a relation from rung 2 over an assertion
read off either.

## What this unblocks downstream

A case that reaches an effect rung — `outcome`, `metamorphic`, `raster-visual` or
`interactive-glass` — counts as `sourced` in the file
`campaign.py export-warrant` writes, which is what lets a defect class earn oracle
coverage in a warrant. A campaign that leaves cases unoracled exports a lower
number and the warrant refuses the tier, which is the correct outcome rather than a
bug in either tool.
