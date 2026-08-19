# The oracle gap between `test-campaign` and `warrant`

`warrant` and `test-campaign` do not reference each other. `grep -rn "warrant"` across
`test-campaign/` returns nothing, and `grep -rn "test-campaign"` across `warrant/` returns one
incidental line in `claims.json` citing a local artifact. Neither skill can produce or consume the
other's state, so a repository can hold a mature campaign and a tier-0 warrant simultaneously, and
nothing connects them.

That gap has a cost, and this session paid it. A `warrant:lot` audit of 211 items returned 143 that
could not be verified in either direction, and the pipeline had no way to say why or what to do
about it. This document locates the gap against both research corpora and proposes six changes.

Read against: `warrant/0.1.1` (source and cache agree) and `test-campaign/0.6.0` (source; the
installed cache is 0.5.0, which differs only by the `interactive-glass` rung).

## What was read

The full corpus is smaller than it appears. `create-test-suite`'s three versions carry
byte-identical research, and it is byte-identical to `test-campaign`'s for all three shared
reports — confirmed by `md5`. `create-test-suite` is the predecessor name; the shared
`meta-pass-gap-analysis.md` is subtitled "running `acceptance-e2e`'s own method on
`acceptance-e2e`". So the unique corpus is roughly 655KB, not 1.5MB.

Read in full: `warrant/references/evidence.md`, `warrant/docs/deep-research/readings.md` and
`direction.md`, `test-campaign/docs/meta-pass-gap-analysis.md`, and
`test-campaign/references/coverage-model.md`. Read targeted, by section and by grep against the
oracle question: the four warrant panel reports, and the three test-campaign research reports.
The warrant panel reports were not read line by line; their substance reaches this document
through `readings.md` and `claims.json`, which are authored from the claim graph.

## Finding 1 — The corpus already names the distinction neither skill acts on

`readings.md` §2 records the product's own screenshot-judging pass holding fifty surfaces with
captures and expectation atoms present, returning `inconclusive` on all fifty, "stated each time as
being for want of a judge rather than for want of an oracle."

That sentence is the whole problem, and it was written before either skill shipped. Two failures
arrive wearing one status:

**Want of a judge.** A property exists, a check could read it, and nobody with standing has read
it. This is an authority gap, and `warrant` is the correct instrument. More tests do not help.

**Want of an oracle.** No property is being checked at all, because none was ever specified. This is
a coverage gap, and `test-campaign` is the correct instrument. More authority does not help.

Neither skill asks which one it faces. `test-campaign`'s `inconclusive: <reason>` carries free text
where the reason should be typed, and `warrant`'s verdict schema has no field for it. So the fifty
surfaces in the corpus, and the 143 items in this session's audit, are recorded as one condition
when they are two, and the remedy for each is the other skill.

**Confidence: high.** The distinction is quoted from the corpus; the absence of any field carrying
it is verified by reading both schemas.

## Finding 2 — The two skills dispose of `inconclusive` in opposite directions, and neither repairs it

`warrant` makes `inconclusive` a valid terminal result, and it is right to. `I4` derives it from
`C13` — ISO/IEC 17025 requires declared measurement uncertainty and treats an inconclusive result as
valid — and `warrant_column.py` returns exit 4, "no move", with the reason recorded. The design
intent is explicit in `readings.md` §4: forcing them binary "would manufacture certainty the
pipeline doesn't have."

`test-campaign` makes `inconclusive` blocking. `campaign.py` lists it in `UNRESOLVED_REASONED`, and
`check` refuses to clear while any case is inconclusive.

Both dispositions are defensible and they compose badly. `warrant` has no mechanism that ever
resolves an inconclusive, because its ladder is climbed on absence of escapes rather than on
acquisition of oracles — so a repository can sit at tier 0 indefinitely while `ratchet.py` correctly
reports the same blocker forever. `test-campaign` blocks on the same condition but offers no remedy
path either: no phase takes an inconclusive case and builds the missing oracle.

The result is a stable standoff. Nothing in either skill converts "we cannot tell" into "here is the
check that would tell us."

**Confidence: high.** Verified against `campaign.py` constants, `warrant_column.py` exit codes, and
the `ratchet.py` output on this repository, which named `oracle_coverage: no oracle coverage
recorded for this class` for all seven classes.

## Finding 3 — The bridge is half-built and unwired

`charter_validate.py` documents three input files it reads from `.warrant/`:

```
oracle-coverage.json  {"classes": {"<class>": {"figures": N, "figures_with_source": K}}}
                      or {"classes": {"<class>": {"coverage": 0.98}}}
suite-health.json     {"green": true}
regression-run.json   {"classes": {"<class>": {"cases": N, "recaught": K}}}
```

`rollup_classes.py` exists solely to map per-surface measurements onto per-class answers using the
warrant's own globs, and its docstring says why: "without it the planes cannot talk … a class with
no rollup reads as a class with no evidence."

`test-campaign` produces the substance of two of those three files and writes it nowhere `warrant`
looks. `cases.json` carries a per-case oracle rung and an `armed` boolean; `strict-check.py` already
computes the number that `suite-health.json` wants. The coverage model's per-axis cell coverage is
the shape `oracle-coverage.json` wants.

So the tier-0 result on this repository is not evidence that the repository lacks test integrity. It
is evidence that nothing has ever written the file, and the two states are indistinguishable to
`charter_validate.py`, which treats absent evidence as an unmet condition by design.

**Confidence: high** for the file shapes and the `rollup_classes.py` purpose, both quoted from
source. **Medium** for the claim that the campaign data would satisfy the schema without
transformation — the mapping is plausible from the field names and has not been implemented.

## Finding 4 — The research names the remedy, and both skills already carry half of it

The oracle problem is named directly in the Gemini lane: "the agent does not inherently know what
the correct visual output should be for an arbitrary interaction," with metamorphic testing offered
as the answer, "validating expected relationships rather than absolute ground truths" — invariance
(rotating a device does not change list length) and monotonicity (a price filter never increases the
result count).

The OpenAI lane reaches the same place from a different direction and adds the operational rule.
Its technique table verdicts metamorphic UI testing as "promote as plan-adequacy and oracle
technique" and notes that "relation coverage identifies weak oracles." Its exploratory-agent finding
is the ordering rule this whole document turns on: agent findings "should remain non-blocking until
converted into a deterministic, independently-oracled replay."

`test-campaign` already carries `metamorphic` as an effect rung, and `sweeps.md` lists metamorphic
relations among the sweeps. What is missing is the trigger: nothing routes an unoracled case to the
technique that would oracle it.

Two constraints on any generation step, both measured, both of which a naive implementation would
violate:

The Mozilla Firefox study classified LLM-generated test plans as 27% valuable and new, 50.5%
duplicates, 22.5% invalid or out of scope; a 2025 industrial pipeline found 60% usable as generated.
`coverage-model.md` draws the right conclusion — "deduplication is not a polish step, it is most of
the value" — so oracle generation must run against the coverage model, never free-form.

The model that wrote the code may not be the sole oracle for it. The OpenAI lane cites test-
generation tools validating faulty behaviour and erroneous code biasing later generation toward
"mutually consistent but incorrect implementation/test pairs." The defence is an oracle sourced from
the specification. This bites hardest on exactly the case that prompted this document: for a
board item, the ticket *is* the specification, and it was written by the same pipeline that wrote
the code.

**Confidence: high** for the quoted findings. **Medium** for the transfer — the Gemini lane's own
knowledge gaps flag the absence of quantitative ROI data for metamorphic testing in UI-driven
enterprise applications, and the component evidence it cites is an August 2026 preprint with no
replication.

## Finding 5 — `lot` can be planned over an unmeasured suite, and was

`warrant`'s stated order is forced: charter, then oracle, then assay, then panel. `I6` gives the
reason — measure test integrity first, because every downstream number inherits it — grounded in
`C18`, where more than half of over 15,000 generated mutants survived a passing suite.

Nothing enforces it. `lot_plan.py` takes a lot size and reads the warrant's tolerable error rate; it
does not read `suite-health.json` and does not refuse when the assay plane has never run. This
session ran `charter`, skipped `oracle`, skipped `assay`, and went straight to `panel` over 219
positions. Every gate passed. The seeded controls then measured the reviewer at 2 of 8 recall, which
is the number the skipped plane existed to predict.

The failure is mine rather than the plugin's, and it is the kind a gate exists to prevent. A skill
whose own documentation calls the order forced, and whose scripts permit any order, has written the
rule in the weakest available place.

**Confidence: high.** Verified by reading `lot_plan.py`'s argument parser and by the run itself.

## Finding 6 — `lot_report.py`'s five fields omit the one that bounds the audit

`lot_report.py` requires population, tolerable error rate, sample size, seed recovery and decision,
and exits 2 without any of them. `lot/SKILL.md` separately instructs, in prose, "say which classes
the audit covered," citing `C6`: roughly three quarters of code-review defects are evolvability
findings rather than functional ones, so a lot audited only on functional defects has been audited
on the minority of what a reviewer produces.

Prose does not gate. The report this session produced names no defect class and no oracle rung, so a
reader cannot tell whether the 57 defects found are functional, structural or perceptual, nor what
the audit was blind to.

**Confidence: high** for the omission. **Medium** for `C6` itself, which `evidence.md` marks as a
range the lanes disagree on, with later replications putting functional findings near 7%.

## Proposed changes

Ordered by dependency. Each names the finding it closes and the evidence behind it.
**All six shipped on 2026-08-19** — warrant 0.2.0, test-campaign 0.7.0, shipyard 0.2.0,
ship-feature 2.1.0, ship-fleet 2.1.0. Two corrections surfaced while implementing them and are
recorded at the end of this section.

### 1. Type the unresolved statuses in `test-campaign` (Findings 1, 2)

Split `inconclusive` into two statuses in `campaign.py`:

| Status | Means | Routes to |
|---|---|---|
| `inconclusive: <reason>` | the instrument was applied and could not measure | fix the instrument |
| `unoracled: <reason>` | no property is specified that a check could read | oracle construction |

Both stay blocking. The distinction is what makes the next change addressable, and it is the
corpus's own distinction rather than a new one.

### 2. Add an oracle-construction phase to `test-campaign` (Findings 1, 4)

A phase between "run, stabilise, arm" and "sweep", taking every `unoracled` case and attempting to
oracle it, in a fixed order that reflects what the research supports:

1. **A specification-sourced outcome assertion**, where the requirement inventory names an effect.
   Sourced from the specification rather than the build, per the mutually-consistent-pairs finding.
2. **A metamorphic relation**, where an invariance or monotonicity holds across two runs. The
   research's named answer to the oracle problem.
3. **A property-based invariant**, where the surface has a contract expressible as one. The Gemini
   lane's caveat applies: property-based testing struggles on graphical workflows, so this rung is
   for contracts rather than appearances.
4. **Record it as permanently unoracled**, with the structural reason, and let it count against the
   total rather than disappear from it — which is what `SKILL.md` already requires of an unreachable
   case.

Generation runs against a cell drawn from the coverage model, never free-form, because half of
free-form output is duplicates.

### 3. Make `test-campaign` emit `warrant`'s input files (Finding 3)

A `campaign.py export-warrant <dir> --root <repo>` subcommand writing `.warrant/suite-health.json`
from the armed ratio and the `strict-check.py` figure, and `.warrant/oracle-coverage.json` keyed by
surface for `rollup_classes.py` to map onto classes.

This is the change that produces the ordering asked for: a campaign runs, and the warrant's tier
becomes earnable rather than permanently refused. It requires no new measurement — only writing the
measurement that already exists where the consuming plane looks.

### 4. Make `lot_plan.py` refuse an unmeasured suite (Finding 5)

Exit 3 — the existing precondition-absent code, the same one used for a missing warrant — when
`.warrant/suite-health.json` is absent, naming `assay` as the missing step. `charter_validate.py`
already establishes the pattern of a precondition gate that names its key.

This is the smallest change with the largest effect, because it makes the forced order actually
forced. It would have stopped this session's run before the panel plane spent 6.7M tokens over an
unmeasured suite.

### 5. Add a sixth required field to `lot_report.py` (Finding 6)

**Oracle mix of the sampled items** — the count at each rung across the sample — joining the five.
Absent is exit 2, like the others. A lot report that cannot say what rung its evidence stands on
cannot support the claim it makes, and `C19`'s denominator rule is the same argument applied to a
different number.

### 6. Give `ratchet.py` a work order, not just a refusal (Finding 2)

`ratchet.py` currently reports `oracle_coverage: no oracle coverage recorded for this class, so it
cannot be shown at or above its 95% tier-1 threshold`. It knows the class's surface globs and can
enumerate which surfaces under them have no oracle. Emitting that list turns a permanent refusal
into a finite task list, which is the difference between a ladder that can be climbed and one that
only reports height.

### What implementation changed about the proposal

Two defects in the six as written, both caught by running the chain rather than by reading the
schemas.

**The export keyed coverage by surface id.** `rollup_classes.py` reads a *list* of rows and
matches a `file` path against the warrant's class globs. Keying by `SURF-001` matched no glob and
rolled every class up to zero coverage — which is indistinguishable from a campaign that measured
nothing, and would have shipped a bridge that silently carried no traffic. The export now emits
`{file, figures, sourced, unsourced}` rows.

**The export claimed `green`.** In warrant that flag means the mutation score is holding at or
above its high-water mark, and `test-campaign` does not do mutation testing; `rollup_classes.py`
recomputes it from a `mutation` block and overwrote the value anyway. Writing it from the
campaign's own gate would have asserted a fault-sensitivity measurement nobody made — the same
conflation this document exists to end. The export now writes `campaign_gate_clear` and
`armed_ratio` under their own names, sets `mutation_measured: false`, and both `export-warrant`
and `lot_plan` say on every run that `assay` still owes the mutation number.

## What these changes do not fix

`C1` is untouched. No powered non-inferiority reader study exists for code review or UI acceptance,
so there is still no measured human baseline to be non-inferior to, and no amount of test
construction creates one. Every claim about matching a human remains an argument.

`C2` still bounds the panel. Nine judges give about two effective independent votes, so adding
oracles does not license adding lanes.

And the tier-3 condition stays unreachable in the near term regardless: 200 items closed in a class
with zero escapes over 90 days is a volume-and-time requirement, not an evidence requirement. These
changes make tiers 1 and 2 earnable. `Verified` stays out of reach until the window is served.

## Open questions

Whether `test-campaign`'s per-case data satisfies `oracle-coverage.json` without a transformation
step is unverified; the field names are compatible and nothing has been implemented against them.

Whether an `unoracled` case can be reliably distinguished from an `inconclusive` one by the agent
recording it, rather than in review afterwards, is untested. The distinction is clear in principle
and may be hard at the point of recording.

The seeded-control result from this session — 2 of 8 recovered — is a measurement of one reviewer on
one lot, with one of the eight plants later found invalid. It bounds nothing beyond that run.
