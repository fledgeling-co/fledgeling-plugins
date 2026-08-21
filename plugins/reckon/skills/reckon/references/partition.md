# The partition

Every entity on both sides of the reckoning lands in exactly one class. That
totality is not tidiness — it is the mechanism. A filter can drop an item
silently; a partition cannot, because there is nowhere to drop it to.

`scripts/reckon.py` enforces this with two checks that both exit 1: every id
appears in exactly one row, and the evidence behind a row must legally support
the class it was given.

## The entities

Five kinds go in, from two sources.

From the brief queue: **briefs** — one markdown file each, id is the slug.

From the campaign registry: **requirements** (what the product claims, each
with an evidence grade), **cases** (a designed check, each with a status and
an oracle rung), **defects** (a recorded negative result), **surfaces** (a
place in the product).

Cases and surfaces are not work. A case is a measurement and a surface is a
location, so both carry `is_work_item: false` and roll up — a failing case to
the defect it evidences, a blocked case to the blocker behind it, a surface to
the cases on it. They still get rows, because the partition has to be total or
the gate proves nothing. A surface becomes work in exactly one situation:
nothing claims it, which makes it a question about whether it should exist.

This is why the report carries two counts. **Rows** is every entity and is
total by construction. **Work** is what somebody would schedule. Conflating
them is how a remaining-work list doubles itself — counting `DEF-0015` and the
four failing cases that cite it as five jobs — and stops being believed.

## The classes

### `unbuilt` — product work

A brief names it and nothing in the registry answers to it.

The honest reading is narrower than the name: this means **registry-silent**,
not proven-absent. A campaign that never designed a case for something leaves
it looking identical to something that does not exist. Where the difference
matters, `spec-validation` settles it; this skill is not entitled to that
verdict from documents alone.

### `broken` — product work

A campaign `fail`, or a recorded defect, or a brief whose subject one of those
lands on. Measured, and the answer was no.

This is the only class an ordinary backlog sweep finds reliably, which is why
a list containing only these looks complete and is not.

### `unmeasured` — evidence work

The class the skill exists for. It holds:

- cases at `blocked`, `inconclusive`, `unoracled`, `unselected` (carried from
  an older run) or `open`
- requirements whose evidence is `reported` or `unknown` — the project's own
  account of itself, which is a different thing from a checked claim
- surfaces with cases where none reached a verdict

Test standards have carried this state for decades rather than inventing it
here: TTCN-3's verdict set is `none`, `pass`, `inconc`, `fail`, `error`, and
`inconc` exists precisely because "neither clearly passing nor definitively
violating" is a real outcome. Runtime-verification logics add
`presumably true`/`presumably false` for the same reason.

The remedy differs per source, and the ledger carries it per row, because one
"test this properly" item sends five different jobs to the same wrong place:

| Source | What the work actually is |
|---|---|
| `blocked` | Reach the state — credentials, a non-destructive route, a hook that forces it |
| `inconclusive` | Add observability — it ran and could not read the answer |
| `unoracled` | Build an oracle — nothing decides what a pass looks like |
| `unselected` | Re-run — this verdict is carried, against older code |
| `open` | Run it — designed, never attempted |
| `reported` | Obtain independent evidence |
| `unknown` | Obtain any evidence at all |

Scheduled as blockers, not cases. See "Clustering" below.

### `unnamed` — decision work

The campaign found a surface; no brief and no requirement claims it. Either
the documents are behind the product or the product grew something nobody
asked for, and those have opposite fixes — write the spec, or delete the
surface. A person decides which.

Every `unnamed` row is also proof the denominator is a floor: the intent space
is demonstrably larger than the documents describe.

### `undecided` — decision work

The documents and the evidence disagree, and no instrument settles it:

- a requirement graded `contradicted` or `vacuous`
- a brief that looks done, but only at an oracle rung below the retirement
  floor, or only through a guessed join

The second is deliberate conservatism. An item that looks finished on weak
evidence is routed to `spec-validation` rather than retired, because retiring
is destructive to somebody's stated intent and the cost of being wrong is
asymmetric.

`undecided` rows are `whats-left`'s natural input — they are the questions
only the owner can burn down.

### `retirable` — bookkeeping

The campaign observed the brief's subject working, at rung `outcome` or above,
on a **cited** join.

Three conditions, all of them load-bearing. `presence` proves a thing is on
screen, which is compatible with it doing nothing, so retiring on it retires
intent on the weakest evidence the ladder has. A token-overlap join is a
guess, and the gate refuses a retirement that rests on one. And where the join
as a whole is weak — under half the briefs tied to anything — retirement
claims are withheld across the board and the briefs stay in their documentary
class.

That last one is a deliberate choice about how to fail: a weak join degrades
the claim rather than blocking the run. A gate that refuses to produce output
gets switched off, and a switched-off gate catches nothing.

### `waived` — exception

Somebody decided not to. Campaign statuses `n/a` and `skip`; briefs declaring
`waived`, `deferred`, `wontfix`, `declined` or `out of scope`.

Not remaining and not done. Regulated regimes keep a separate deviation
register for exactly this, and a waiver that closes an item still leaves the
item visible. Two consequences here:

- `n/a` and `skip` are **excluded from the adjudicated numerator**. A decision
  is not a measurement, and counting it as one is how a campaign closed by
  decision reads as a campaign closed by evidence.
- A waiver with no recorded reason fails the gate. A decision names why; an
  omission does not, and the two are indistinguishable afterwards.

Waivers stay on the ledger because their reasons expire. A state with no hook
may get one; an account that could not be reached may become reachable.

### `verified-done` — not remaining

Measured working. Kept in the ledger so the denominator is honest, and
excluded from the work count.

## The legality table

The gate's core. A case status on the left may only ever produce a class on
the right:

| Status | May only be |
|---|---|
| `blocked`, `inconclusive`, `unoracled`, `unselected`, `open` | `unmeasured` |
| `fail` | `broken` |
| `pass` | `verified-done` or `retirable` |
| `n/a`, `skip` | `waived` |

Plus: a requirement resting on `reported` or `unknown` evidence may not be
`verified-done` or `retirable` — self-reported evidence cannot retire itself.

The first row is the whole point. A blocked case classed as anything other
than `unmeasured` is the silent-done failure caught in the act, and
`selftest.py` demonstrates it firing.

## Precedence

An item can qualify for two classes. Evidence beats naming, so a defect on an
unnamed surface is `broken` rather than `unnamed` — the fix is the defect
either way. Resolution order:

1. `waived` — a decision on the record overrides an inference about it
2. `broken` — measured negatives outrank everything unmeasured
3. `undecided` — a live disagreement outranks a documentary guess
4. `unmeasured`
5. `retirable`
6. `unbuilt`, `unnamed` — the documentary classes, last

## Worked examples

**A brief with a matching defect.** `SCR-0071` (capability columns have no
backfill) cites `DEF-0001`. Both get rows; the brief is `broken`, the defect
is `broken` and is the work item, and the brief rolls into it. One job, two
rows, and the gate can still account for both.

**Ten cases, one dead credential.** Each case is `unmeasured`,
`is_work_item: false`, and clusters into one blocker carrying all ten ids and
the coverage recovering the credential returns. One scheduled job.

**A brief that looks finished.** Its requirement is `observed`, but the
strongest case on that surface is `presence`. Not `retirable` — `undecided`,
with the reason recorded and a route to `spec-validation`. The alternative is
deleting a stated requirement on evidence that the thing appeared on screen.

**A surface nobody asked for.** Forty surfaces, one with no case and no brief.
`unnamed`, decision work, and the report says the denominator is a floor
because of it.
