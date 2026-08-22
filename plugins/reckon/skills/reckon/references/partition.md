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

A brief cites registry ids on purpose — `REQ-0004`, `DEF-0015` — and the
registry holds none of them.

That citation is what makes this class safe to assert. Somebody wrote down what
should exist, and it is not there: evidence of absence, rather than an absence
of evidence. Everything weaker than a dangling citation is `unjoined` below.

Where the difference still matters, `spec-validation` settles it; this skill is
not entitled to that verdict from documents alone.

### `unjoined` — decision work

A brief that the join could not tie to anything in the registry at all.

This is the class that keeps `unbuilt` honest, and it exists because the two
carry opposite conclusions. The join is the one inferential step in this
pipeline and it is labelled a guess everywhere else; a guess returning nothing
is not a finding about the product. On one real registry, folding these into
`unbuilt` put 75 of 91 briefs into product work on a 17.6% join — every one of
them naming an item that had shipped — and produced a headline claiming 183
pieces of product work against a true figure in the low tens.

The row carries the three nearest candidates the join scored and rejected, with
their scores, so ruling on it is a read rather than a grep. The remedy is a
person, which is why it is decision work and not product work.

### `broken` — product work

A campaign `fail`, or a defect the registry still records as open, or a brief
whose subject one of those lands on. Measured, and the answer was no.

**A defect carries its own repair, and it is read.** A row at `fixed`,
`resolved`, `closed`, `done` or `verified` is `verified-done` — the same
registry, speaking about the same run, as the `pass` that retires a case. A row
at `wontfix`, `deferred`, `declined` or `duplicate` is `waived`. A row whose
status this tool does not recognise, or that carries none, stays `broken`:
guessing done is the one error in this direction that cannot be recovered from.
Classing every defect row `broken` without reading `status` is how a campaign
that had repaired 100 of its 110 defects reported all 110 as remaining work.

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

| Case status | May only be |
|---|---|
| `blocked`, `inconclusive`, `unoracled`, `unselected`, `open` | `unmeasured` |
| `fail` | `broken` |
| `pass` | `verified-done` or `retirable` |
| `n/a`, `skip` | `waived` |

| Defect status | May only be |
|---|---|
| `open`, `new`, `confirmed`, `reopened`, `regressed`, `in progress` | `broken` |
| `fixed`, `resolved`, `closed`, `done`, `verified` | `verified-done` |
| `wontfix`, `deferred`, `declined`, `duplicate`, `n/a` | `waived` |
| anything else, or absent | unconstrained — the classifier leaves it `broken` |

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
7. `unjoined` — not a conclusion at all: what is left when the join reached
   nothing, and the only class whose remedy is a person reading the brief

## Worked examples

**A brief with a matching defect.** `SCR-0071` (capability columns have no
backfill) cites `DEF-0001`. Both get rows; the brief is `broken`, the defect
is `broken` and is the work item, and the brief rolls into it. One job, two
rows, and the gate can still account for both.

**The same brief, after somebody fixes it.** `DEF-0001` now reads `fixed`. The
defect becomes `verified-done` and stops being a work item, and the brief stops
being `broken` with it — otherwise the repaired work simply reappears one hop
out, under the brief's id instead of the defect's.

**A brief nothing joined.** `SCR-0088` names a surface the campaign never
designed a case for, and no note anywhere cites it. `unjoined`, decision work,
carrying `REQ-0031 (0.14)` as the nearest thing the join looked at and would not
accept. Not `unbuilt`: the registry was not silent about it, the join never
reached the registry.

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
