---
name: warrant
description: >-
  The warrant pipeline's router and map — explains the eight skills (charter, oracle, assay,
  panel, feedback, lot, ratchet, ledger), the authority ladder they move defect classes up and
  down, and which skill a given situation calls for. Use when someone asks how to stop reviewing
  every item by hand, how much authority a model currently holds, why a class was revoked, or
  invokes /warrant without naming a skill. It routes and explains; the eight skills do the work.
---

# Warrant — the map

This plugin removes the human from **per-item** verification. Under it, nobody looks at an item.
What survives is one standing signature on a policy file, plus whatever the owner reports when
the pipeline gets something wrong.

That residual is deliberate and it is the one thing here that cannot be automated away. Four
independent research backends searched for a regulated software vendor whose all-machine
verification step had been accepted as the control of record and none found one (`C21`). The
obstruction is administrative. A Part 11 electronic signature, under the US Code of Federal
Regulations title 21, must be unique to one individual, and a model identifier is not an
individual (`C11`). And PCAOB, the US public-company audit regulator, permits leaning on last
period's testing of an automated control only where the auditor verifies the control has not
changed, which a silently reversioned model cannot satisfy (`C12`). Neither cuts a standing
scope with a named person answerable for it. Both cut a per-item machine verdict.

Every claim id resolves in `docs/deep-research/claims.json`, and `references/evidence.md`
separates the direct findings from the inferences.

## The eight skills

| Skill | What it does | When to run it |
|---|---|---|
| `charter` | writes and validates `.warrant/warrant.toml`, the signed authority | first, and at every renewal |
| `oracle` | lineage, tick-and-tie, taxonomy validation | before the panel plane runs |
| `assay` | mutation survival, cannot-fail scan, selection gap | before believing any verdict |
| `panel` | one out-of-family grader, orthogonal lenses, an adjudicator | per item, once the two planes above are green |
| `feedback` | turns a reported escape into a permanent regression case | whenever the pipeline was wrong |
| `lot` | risk-limited acceptance of a queue of finished items | on a backlog, or on a cadence |
| `ratchet` | computes earned tiers, applies revocations | after any of the above, and on a schedule |
| `ledger` | appends and verifies the hash-chained decision record | continuously; verified before an audit |

## The order is forced

Run the planes in this sequence, because each one's output is the next one's input and a verdict
built on an unmeasured suite means nothing.

1. **`charter`** — nothing else runs without a valid warrant. `charter_validate.py` is the
   outermost gate and every other skill checks it.
2. **`oracle`** — the deterministic plane, and it comes before the model plane rather than after
   it. The highest-consequence failure for a data-dense product is a correctly rendered screen
   stating a figure no source supports, and a vision judge is structurally unable to catch that
   because nothing on the screen looks wrong (`I7`). Arithmetic catches it.
3. **`assay`** — over half of more than 15,000 generated mutants survived a passing unit,
   integration and system suite (`C18`), and nobody has measured that for browser suites at all.
   A green suite is not evidence until its fault sensitivity is a number.
4. **`panel`** — the only plane that calls a model.
5. **`lot`** — for a queue rather than an item.
6. **`rollup_classes.py`** — maps per-surface and per-target measurements onto the
   defect classes authority is held against, using the warrant's own globs. Without it
   every class reads as having no evidence.
7. **`ratchet`** — reads what the others produced and moves authority.

`feedback` and `ledger` run continuously rather than in sequence.

## The ladder

Authority is held per defect class, earned by evidence, and lost automatically.

| Tier | The machine may close | Earned by | Lost on |
|---|---|---|---|
| 0 | nothing; it advises | a signed warrant and a writing ledger | — |
| 1 | classes where the oracle plane is green and no perceptual judgement is needed | oracle coverage at or above the warrant's threshold | any lineage gap |
| 2 | tier 1 plus perceptual classes with a declared miss rate | assay green, and the grader re-catches every historical escape in the class | a model version change, or any new escape in the class |
| 3 | tier 2 across all non-disclosure surfaces | the warrant's item count closed in the class with zero escapes over its window | one escape in a tier-3 class |
| 4 | tier 3 plus disclosure content | unreachable on current evidence | — |

Two properties of this table are load-bearing. A class the warrant does not name sits at tier 0,
so a class nobody wrote down is a class no machine may close. And entry to tiers 2 and 3 is by
absence of escapes rather than by a measured sensitivity, which is weaker evidence: absence is
bounded by what got noticed, so it gains weight from volume and time and never becomes a rate.
`references/tiers.md` carries why tier 4 is in the table at all.

## What this pipeline is not

**Not a jury.** Nine frontier judges from seven families supply about two effective independent
votes, panel accuracy falls 8 to 22 percentage points short of genuinely independent voting, the
best single judge matches or outperforms the whole panel across every tested condition, and
established aggregation closes at most 11% of that gap even when given the correct answers
(`C2`). `panel` therefore runs one grader on the verdict, lenses on orthogonal questions, and an
adjudicator whose output is a routing decision rather than a winner.
`references/why-not-a-jury.md` carries the test for whether a proposed lane is a lens or a second
vote.

**Not a place to show a reviewer the machine's answer first.** Where a human does look at a
sampled item, they look blind. In 323,973 women, screening with a computer aid produced no
accuracy improvement on any metric, and among radiologists who read both with and without it
sensitivity was significantly lower with the aid, odds ratio 0.53 (`C8`).
`references/positioning.md` carries the mechanism.

## Where the depth lives

| Reference | Read it when |
|---|---|
| `references/evidence.md` | before changing any number in any skill |
| `references/script-contract.md` | before writing or editing a script |
| `references/admissibility.md` | writing or renewing a warrant |
| `references/why-not-a-jury.md` | someone proposes adding a model |
| `references/positioning.md` | building a surface where a human sees a machine verdict |
| `references/tiers.md` | proposing a tier change |
| `references/measurement.md` | before reporting any number |
| `references/opus5-authoring.md` | writing or editing a runner prompt in this plugin |

## Delegation

Use a subagent for a wide read across many files where you need only the conclusion, or for two
genuinely independent tracks each larger than a handful of tool calls. Do the work yourself
otherwise: a delegated agent pays for its own copy of the context.

Cap: at most three subagents for one task in this plugin. Work that looks like it needs more is
work that should be split into phases with a checkpoint between them.
