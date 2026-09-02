# Campaign artefact schemas

Seven JSON Schema (draft 2020-12) files describing the artefacts a UI test campaign leaves behind. They exist so a reader — the native flow reader, a dashboard, another agent — can consume a campaign it has never seen, and so a campaign in any repository produces the same shapes.

Nothing here is specific to one project. `featureArea`, `lane`, `priority`, tracker `state`, `severity` and `origin` are open vocabularies a project declares; real values from the campaign these were derived from appear in `examples`, never in `enum`. What *is* closed is methodological: the three coverage statuses, the eight-class reconciliation partition, the five work kinds, the estimate tiers, and — above all — the eight coverage axes.

## The files

| Schema | Artefact it describes |
|---|---|
| `flow-specification.schema.json` | the journey catalogue |
| `coverage-axes.schema.json` | what is known about that catalogue |
| `instrument-calibration.schema.json` | what the instruments can and cannot see |
| `remaining-work.schema.json` | what is left, sized from measured rates |
| `reckon-ledger.schema.json` | intent reconciled against evidence |
| `defect-cards.schema.json` | the tracker items being reconciled |
| `work-schedule.schema.json` | the plan over what remains |

### flow-specification

The catalogue of journeys a project intends to be true — one entry per journey, written before and independently of whether any test exists. A journey belongs here the moment somebody can name it, and stays whether it is tested, untestable or broken. Each entry carries an entry point, preconditions, an ordered action sequence with expected outcomes, its variants and observational edge cases, exactly one oracle, its provenance, and what coverage already existed. Read wrongly it becomes a coverage report, which is the single most expensive misreading in the set: `flows.length` is a denominator, not an achievement, and a project that treats an enumerated journey as a covered one has manufactured its entire coverage figure out of an act of imagination. The second misreading is `lanesSpecified`: a lane absent from it has not been declared empty, it has not been looked at, and counting it as zero work reports an unexamined area as finished.

### coverage-axes

What is actually known about that catalogue, as eight separately denominated axes — named anywhere, bound to a test title, enforced by a blocking CI step, run in report mode only, in no CI step at all, distinct recorded case passes, frames captured, surfaces judged. The schema closes `axes` and forbids `coverage`, `pct`, `overall`, `score`, `total` and `summary` at the top level, so a single blended number is unrepresentable rather than merely discouraged. That is the whole point of the file. The axes count four different populations against four different denominators; averaging any two destroys the only information they carry, and the specific damage is that `named_any_mention` — which a comment satisfies — absorbs `ci_enforced_blocking`, which is the only axis on which a regression is caught by machinery. `isFloor` is fixed to `true`: every figure is a lower bound on what is known and an upper bound on nothing.

### instrument-calibration

A specimen of deliberately planted defects and, per instrument per defect, what a correct instrument *would* say (`truth`) against what this one *does* say (`known`). `known != truth` is a standing condemnation — every figure that instrument has published on that axis is void — and it is printed on every run and never silenced. Drift (`actual != known`) is what sets the checker's exit code, so the checker is green while the record is honest and goes red the moment behaviour changes in either direction. Two rules make the pair mean anything, and the schema states both: never edit `known` to quieten a break, and raise `known` toward `truth` only in the same change as the fix that earns it. Reading this file as a defect list costs everything it is for. It is a statement about the *instruments*; an instrument declared `absent` is an axis nobody is watching, and omitting that declaration turns silence into apparent health.

### remaining-work

What is left, sized from rates this campaign actually observed rather than from an estimate — each row naming its count, its unit, which measured rate applies and the evidence for applying it, plus a `blocked` half carrying each obstruction's lifting condition and owner. Every wall-clock figure is a range for *one lane*, carries no failure rate, and counts a lane that produced work later rejected identically to one that landed. Summing the ranges assumes lanes run serially and that no lane loses an agent; both were false in the campaign this came from, where 4 of 12 lanes lost an agent. The costly misreading of `blocked` is treating a harness fault as a product defect: a blocker whose owner is the harness will otherwise be filed in the engineering backlog and sit there behind work nobody can start.

### reckon-ledger

A total partition of everything promised and everything measured, both sides in, every item in exactly one of eight classes so nothing falls out of the list quietly. The class that carries the file is `unmeasured`: a blocked or inconclusive check is neither a pass nor a failure, and a remaining-work list that silently drops it reports a partial campaign as a finished product. `unclassified` must be empty — a non-empty array is the ledger telling you it lost something. Denominators sit one per axis with `means` stating what each figure is *not*; `cases_adjudicated` is the one most often misread as a pass rate, and it counts fails as knowledge. `join.weak` is the other thing to read before anything else: when almost no intent document could be tied to the registry, the ledger is reconciling two lists that barely touch and its `unjoined` class is doing nearly all the work.

### defect-cards

The tracker items a campaign is reconciling, exported flat so a reader can join a journey to its defects without reaching into the tracker. `origin` is the field that earns its place: it separates a defect this campaign raised from one that already existed, and without it a tracker full of pre-existing defects reads as a campaign that found a great deal. `state` is the tracker's opinion and nothing more — a card marked done is not a journey proved, and an unrecognised state must be shown as written and counted separately rather than mapped onto done.

### work-schedule

An ordered plan over what a reconciliation left outstanding: waves whose members' dependencies are met, each named for the reason it exists, every row carrying its class, tier and three-point range. A wave's *name* is a scheduling constraint — "nothing here can be trusted until this lands" is a dependency, and renumbering it into "Wave 0" loses it. Two things cost real work if misread. `cls` distinguishes `broken` from `unmeasured`, which schedule identically and mean opposite things: one is a product to fix, the other a check nobody has run, and losing the difference sends engineers to fix working software. And `decided` records whether a person actually agreed to the ordering; a schedule with `decided: false` is a proposal, and quoting its totals converts it into a commitment nobody made.

## The four invariants these schemas enforce

1. **No project vocabulary is fixed.** Lanes, feature areas, priorities, actors, tracker states and severities are open strings with examples. A project declares its own ordering in `vocabularies` — without it a reader must treat `priority` as an opaque label and may not claim one journey matters more than another.
2. **The axes cannot be blended.** `axes` is closed at exactly eight members and the top level rejects any key a reader would read as one number. Two of the eight count cases and artefacts rather than journeys, and carry their own denominators (`ofCases`, `flows`) so they cannot be quoted against the journey total.
3. **A waiver carries its target and its lifting condition.** `existingCoverage.status: "covered"` requires a non-empty `specFiles`, and `waiverAudit` is where following the pointer is recorded — `followed: true` obliges `targetRuns`, and anything other than `runs` means the waiver is broken. In the reference campaign, 198 of 292 such waivers pointed at a file where no unparked case carried the journey. `waiverIntegrity` publishes that tally so a `covered` count never travels alone.
4. **An instrument declares its own blindness.** Every instrument appears in `instruments`, including ones that do not exist, and every pathology carries a verdict for every instrument. `known: "absent"` requires a `reason`, so an unguarded axis is a written finding rather than a missing row.

## Validating

```
npx --yes ajv-cli@5 validate -s <schema>.schema.json -d <artefact>.json --spec=draft2020 --errors=text
```

Two negative controls worth keeping in a project's own gate, because a schema nobody has seen refuse anything is decoration: an axes file carrying `"coverage": 0.83` at the top level, and a flow whose `existingCoverage` is `{"status":"covered","specFiles":[]}`. Both must fail.

## A minimal conforming project

`examples/` holds a complete two-file campaign for an invented app, both validated against these schemas. Two files are the floor:

```
campaign/
  flow-specification.json   <- the catalogue; everything joins to its flow ids
  coverage-axes.json        <- what is known about it, on eight axes
```

With only those, a generic reader can draw every journey as a diagram, show each node's steps, variants, edge cases and oracle rung, colour by lane and priority, and state — honestly and separately — how many journeys are named, bound, enforced, report-mode, unwatched, and how many recorded case passes, frames and judged surfaces exist behind them. `population.source` in the second file must point at the first; that pointer is the join, and a reader with a mismatched `population.flows` should refuse to render rather than reconcile it.

What each further file adds: `instrument-calibration.json` lets the reader mark which figures are void because the instrument behind them is condemned, and which axes have no instrument at all — without it every axis is presented as trustworthy. `defect-cards.json` puts defects on the journeys they break and separates found from pre-existing. `reckon-ledger.json` adds the intent side, so the reader can show what was promised and never measured rather than only what was measured. `remaining-work.json` and `work-schedule.json` turn the gaps into sized, ordered, owned work.

A project that can produce only the first two files has a readable campaign. A project that produces `coverage-axes.json` without `flow-specification.json` has eight numbers about nothing.
