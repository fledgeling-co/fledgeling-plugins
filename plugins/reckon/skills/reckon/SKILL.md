---
name: reckon
description: >-
  Work out what actually remains in a project by reconciling what it promised against what
  anybody proved — the feature briefs and PRD in docs/features-to-triage on one side, a
  test-campaign registry of cases, requirements, surfaces and defects on the other — and
  resolve every item on both sides into exactly one class of a total partition, so nothing
  can quietly fall out of the list. The classes carry different fix-shapes and different
  owners: named-but-unbuilt, named-but-unjoinable, measured-and-broken, never-measured, never-named, disputed,
  already-done-so-retire-it, and deliberately-waived. The one that matters most is
  never-measured, because a blocked or inconclusive check is not a pass and not a failure,
  and a remaining-work list that silently drops it reports a partial campaign as a finished
  product. That class is scheduled as the blockers behind it rather than case by case, each
  with the coverage it returns, because twenty blocked cases are usually three causes.
  Publishes a denominator per axis and never one blended percent, marks every figure as a
  floor, refuses to retire stated intent on weak-oracle or guessed evidence, refuses to let
  a requirement leave never-measured on its own evidence word when no passing case cites it,
  keeps waivers visible as exceptions rather than folding them into done, and gates the
  whole ledger with an exit code so a report that lost an item cannot pass. Then schedules
  what remains: ship-fleet's wave model over the ledger, so items whose dependencies are
  met run in parallel, with sub-tasks nested under the item that cites them and a
  wall-clock range per item and per wave drawn from 1,842 measured Opus 4.8 and Opus 5
  agent runs — always a range and never a number, because the measured p90 is over three
  times the median, and never a schedule implying a speedup better than the 4.0x ever
  observed. Emits three artifacts from one gated ledger: ledger.json, a comprehensive
  technical reckoning.md, and a self-contained reckoning.html board showing shipped
  features beside remaining ones and the waves between them. Use whenever someone asks what is
  left, what still needs doing, where the project stands, what the test campaign leaves
  open, whether a feature is actually finished, which briefs are stale, what to work on
  next, how long the remaining work will take, what can be built in parallel, or asks to
  reconcile specs against test results — and after any test-campaign run,
  to turn its findings into work. Not for producing the evidence (test-campaign), tracing a
  spec to the code that produces its data (spec-validation), a whole-product survey against
  a stated goal (product-gap-analysis), a tracker-board sweep (stocktake), or a decision
  questionnaire for a non-technical owner (whats-left).
---

# Reckon

A reckoning is a settling of accounts. This one settles what a project said it
would do against what anybody actually established, and reports the difference
in a form somebody can schedule.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It converts the adjudication step's categorical scopes into denominators the ledger prints, and forbids any figure in the report that did not come from ledger.json or the gate's exit code. Other models skip it.

## The failure this exists to prevent

A remaining-work list is built by filtering: take everything, drop what is
done, report the rest. The filter is where it fails, because **"not done" and
"not known" are different things that both look like absence.**

The campaign this skill was written against is the ordinary case, not a bad
one. Fifty-eight designed cases: 25 reached a verdict, 32 did not — blocked on
a dead credential, on a state with no hook to force it, on a surface that
could only be reached by signing the owner out of their only account. Fifteen
stated requirements: two observed, thirteen standing on the project's own
account of itself. Filter that to failures and you get a tidy list of 14
things, and 43% coverage disappears without leaving a mark.

Regulated verification calls the fix a **closed-world reconciliation**: freeze
the baseline, enumerate every requirement, planned case and open defect, and
partition that universe into verified, remaining, exception, or
not-applicable. An item absent from the partition does not make the
determination complete — it makes it invalid. That is the whole design here,
and `scripts/reckon.py` enforces it with an exit code rather than asking you
to be careful. Sources in `references/evidence.md`.

## The partition

Eight classes, and every entity on both sides lands in exactly one. Full
definitions, the legality table and worked examples are in
`references/partition.md`; this is the shape.

| Class | What it means | Kind of work |
|---|---|---|
| `unbuilt` | A brief cites registry ids and the registry holds none of them, or outer intent was scoped out | product |
| `unjoined` | A brief names it; the join reached nothing, so its state is unknown | decision |
| `broken` | Measured, and the answer was no | product |
| `unmeasured` | Nobody found out | **evidence** |
| `unnamed` | The campaign found it; no document claims it | decision |
| `undecided` | The documents and the evidence disagree, or intent was narrowed at triage | decision |
| `retirable` | Already done, to a standard that carries the claim | bookkeeping |
| `waived` | Somebody decided not to, or historical scaffold marked consumed | exception |

Three of these are the reason the skill exists, because a backlog sweep finds
none of them:

**`unmeasured` is work, and it is not the feature's work.** The job behind a
blocked case is reaching the state; behind an inconclusive one, being able to
read the answer; behind an unoracled one, deciding what a pass would even look
like. Those are test-hook and instrument jobs, and they belong to whoever owns
the harness. Sending them to a feature backlog as "test X properly" sends five
different jobs to one wrong place, so each carries its own remedy.

**`waived` is neither remaining nor done.** A decision to skip is a third
thing, and it stays on the ledger because the reason for it expires — a state
with no hook may get one. Folding waivers into done is how a campaign closed
by decision reads as a campaign closed by evidence. Historical scaffolding
briefs (e.g. `consumed/` or `archived/`) are recognized here rather than polluting
active queues.

**`retirable` is remaining work in reverse.** A brief whose subject the
campaign proved works should be closed, not built. Reports that never retire
anything over-count for as long as the project runs.

### The scope-narrowing trap

A major blind spot in closed-world reconciliation occurs when a brief originally
specified a broad multi-system capability (e.g. dual-mode serving, background
daemons, cross-platform services, or kernel integrations), but triage narrowed
the implementation spec to an in-tree mock or partial model. When in-tree tests
pass, the test campaign marks the case green and reckon risks retiring the entire
brief even though the outer capability remains unbuilt.

When reconciling, evaluate whether the brief's full acceptance sketch was
satisfied or merely its narrowed in-tree subset. If outer capabilities (such as
standalone background daemons, platform targets, or system drivers) were
deferred or scoped out at triage, keep those outer capabilities tracked as
`undecided` or `unbuilt` rather than retiring the full intent on in-tree unit test
evidence alone.

## Waves, and what a duration is

The ledger says what remains. The schedule says what can happen at the same time
and roughly how long it takes, using **`ship-fleet:ship-fleet`'s model** so the two skills
describe one shape of work rather than two: nodes are work items, edges are
dependencies, and a wave is everything whose dependencies all sit in earlier
waves.

Two things differ from ship-fleet, and both are about entitlement.

**Edges here are weaker, and they are labelled.** That skill reads specs with
"depends on" lines. reckon reads a ledger, so a `cited` edge is a citation
somebody wrote into the registry and it blocks, while an `inferred` edge is this
tool reading a shared surface and it only *orders* the work. A false edge costs
somebody's parallelism, and this tool is not entitled to spend that on a guess.

**Decision work is never scheduled.** An `undecided` or `unjoined` row is a
person reading two documents and ruling. It has no agent duration, and giving it
one would report waiting on a human as though an agent were busy. Those rows are
listed beside the waves as what gates them.

### Where the durations come from

A corpus of **1,842 measured Opus 4.8 and Opus 5 subagent runs** across 88
sessions and 31 projects, taken from Claude Code's own transcripts. Full
provenance, method, tables and limits: `references/estimation.md`.

Three properties are load-bearing, and each exists because its absence produces
a specific lie:

- **Everything is a range, never a number.** Measured p90 ÷ median is 3.4 for
  build work and 3.1 for research. A point estimate is wrong by a factor of
  three in the ordinary case and reads as precision.
- **A wave costs its slowest member, and no schedule may beat what was
  observed.** Measured wall-clock ÷ slowest member is 1.05 at the median and 1.8
  at p90 over 253 real waves; measured speedup over serial is 2.2× median, 4.0×
  p90. The wave estimator holds its low bound to that ceiling, because perfect
  packing across eight slots is arithmetic that no run has achieved and printing
  it would put a duration on the page that has never happened.
- **Wall-clock includes waiting, and carries no failure rate.** These answer how
  long an agent will be busy — not how much model time it costs, and not how long
  until the work is accepted.

The measured concurrency ceiling is 8 (peak reached: median 5, p90 10). Above it
the slowest-member property degrades to 1.55, so a wave larger than that widens
its own upper bound and says so.

Re-measure when the corpus has grown or a new model lands; the method is written
down at the end of `references/estimation.md`.

## Running it

### 1 · Find the inputs

The brief queue is `docs/features-to-triage/` in most repos here; the campaign
registry is a directory holding `campaign.json`, `cases.json` and
`inventory.json`, usually under `docs/test-campaign/`. Take the newest run
unless told otherwise, and say which one you took — a reckoning against a
stale campaign is a reckoning about a codebase that no longer exists.

If there is no campaign at all, read `references/no-campaign.md` before going
further. The skill still works and the answer is much weaker, and the report
has to say so rather than looking the same.

### 2 · Build the ledger

```bash
S=<this-skill-dir>/scripts
python3 $S/reckon.py build \
    --briefs docs/features-to-triage \
    --campaign docs/test-campaign/<newest-run> \
    --out docs/reckoning/<date>
```

This writes three files and returns the gate's exit code:

- **`ledger.json`** — every row, the reason for its class, the estimate attached
  to each work item and the wave schedule. Everything else is rendered from it.
- **`reckoning.md`** — the comprehensive technical record. Every row, every
  dependency edge with how it was made, the per-wave item tables, the join's
  near-misses, and what this reckoning could not classify.
- **`reckoning.html`** — one self-contained page, no build step and no external
  assets: what is shipped, what remains, what can run in parallel and roughly
  how long each wave takes. It is the artifact somebody shows a room.

The two reports are deliberately different documents rather than one document at
two lengths. The markdown is the record an engineer works from and it holds
everything. The HTML is the same data at a distance somebody can read across a
room, and it is rendered **from `ledger.json` alone** — which is what keeps the
presentable half from drifting away from the gated half.

`--max-concurrency N` sets how many agents may run at once (default 8, the
measured ceiling). `--no-html` skips the page.

### 3 · Adjudicate what the script could not

The script does the mechanical work and stops where judgement starts. Two
places need you, and both are cheap:

**The join.** Briefs do not share ids with requirements, so tying them
together is the one inferential step in an otherwise deterministic pipeline. A
brief citing `DEF-0015`, or a registry note naming `SCR-0075`, is a citation
somebody wrote on purpose; token overlap is a guess, and the ledger labels
them differently. Read the `overlap` edges, confirm or cut them, and read the
the `unjoined` rows — a brief joined to nothing is either genuinely unbuilt or
a join the script missed, and those are opposite conclusions, so the script
refuses to pick one and hands you the three nearest candidates it scored and
rejected. Detail in `references/joining.md`.

**The blocker clusters.** The script groups blocked cases by token overlap
because the useful unit is the cause, not the case. It groups conservatively
and will leave clusters that are one cause wearing two descriptions. Merge
them, and split any it over-grouped. Every case id stays listed under its
cluster, so regrouping loses nothing.

Where a brief's status is genuinely undetermined and it matters, route it to
`spec-validation:spec-validation` rather than deciding from the documents. That skill traces a
claim to the code that produces its data; this one reconciles claims against
evidence and is not entitled to that verdict.

### 4 · Check the estimates against what you know

The schedule is generated, and it reads a row's wording rather than the work
behind it. Two things are worth a minute:

**The tiers.** Each work item carries `S`/`M`/`L`/`XL` with a p25–p90 range, and
the `basis` field says why it landed there. Where you know a row is bigger or
smaller than its wording suggests, change its tier in `ledger.json` and re-gate —
the gate checks the arithmetic, not your judgement.

**The inferred edges.** A `cited` edge is a citation somebody wrote and it blocks.
An `inferred` edge is this tool reading a shared surface, and it only orders the
work. Cut the inferred ones you disagree with; each costs parallelism if wrong
and nothing else.

Every duration is wall-clock for one agent unit, drawn from 1,842 measured Opus
4.8 and Opus 5 runs. `references/estimation.md` carries the corpus, the method
and what the figures cannot say — read it before defending a number to anybody.

### 5 · Re-gate and report

```bash
python3 $S/reckon.py check docs/reckoning/<date>/ledger.json   # exit 0 required
```

Exit 1 means the ledger lost an item or placed one illegally, and the numbers
in it cannot be trusted. Exit 2 means a headline figure the rows do not
support. Exit 4 means an input this tool cannot classify — a status word, an
evidence word or an id-shaped token no rule here covers — reported with the rows
carrying it. All three are defects in the reckoning, not in the project.

Exit 4 is the one worth reading rather than retrying. The row was still placed,
because the partition has to be total, but it was placed by this tool's
fail-closed default and not by anything the registry said. Give the word a rule
or correct the rows; a longer list of words only moves the edge one word along.

Where a previous reckoning exists, run the ratchet:

```bash
python3 $S/reckon.py ratchet <previous>/ledger.json docs/reckoning/<date>/ledger.json
```

An item may leave `unmeasured` only by being measured. Snapshot gates catch a
bad run; this catches the slow version, where an item is quietly reclassified
across runs until nothing remembers it was never checked.

**A requirement leaves it on the cases that cite it, not on its own evidence
word.** `observed` is a word in a registry a person can edit, and until 1.5.0 the
word alone released the row. Measured 24 August 2026: one session moved eight
requirements from `unmeasured` to `observed` with no case having run in between,
in the same session that carried the brief join from 6.2% to 100% by writing
`requirement:` citations into 81 briefs — and both `check` and `ratchet` exited
0. Each requirement row now carries `backed_by`, the ids of the passing cases
citing it, computed from the campaign rather than from the requirement's account
of itself; a move to `observed` with that list empty is refused as a re-label.
A ledger written before the field existed carries no such key and is let through,
because refusing there would report the ledger's age as a defect in the project.

A join is the same shape of claim and the report says so rather than gating it:
a citation somebody wrote is stronger than token overlap, and a citation somebody
wrote *during this reckoning* is a document edited to satisfy the tool. Read the
`cited` edge count against the campaign's adjudicated case count before believing
a join percentage that moved a long way in one run.

## What the report has to say

Enumerate everything and let the ranking do the filtering. Asked to be
selective about what counts as remaining, a capable model will under-report,
and under-reporting is the failure the whole design is built against.

**Publish a denominator per axis, and never one blended percent.** Cases
adjudicated, decisions taken, requirements observed, surfaces spoken for,
briefs joined — these disagree with each other, and a single number hides
whichever is weakest. A pass rate among executed cases is not coverage and
is never labelled as such.

**State that denominators are a floor.** Every `unnamed` row is a surface the
documents never described, proving the intent space is larger than the
documents can measure.

**Lead with what the reckoning cannot speak for**, in the same breath as what
remains. "83 pieces of work remain, over 43% of the designed cases" is honest;
the first half alone is not.

**Say what a duration is a duration of.** Every estimate on either report is
wall-clock for one agent unit, it is a range and not a number, and it carries no
failure rate — an agent that ran an hour and produced work later rejected counts
the same as one that landed. Both reports print those three qualifications
already; do not restate them in prose, and do not narrow a printed range to a
point when you talk about it.

Match the report length to what the task needs. Both reports are generated. What
you add is a short assessment of what they mean — the two or three high-leverage
items worth doing first and why, in a few paragraphs. Do not pad with filler or
restate the tables in prose.

Once the HTML exists, open it: `open -a "Google Chrome" docs/reckoning/<date>/reckoning.html`,
and say in one sentence what to look at.

### The two reports are for different readers

They hold the same data and they are not two lengths of one document.

**`reckoning.md` is the technical record.** It holds every row, every dependency
edge with how it was made, the per-wave item table with each item's tier and the
basis for it, the join's near-misses, the requirements standing on the project's
own word, and every input the tool could not classify. It is what somebody works
from and what somebody argues with. Length is not a virtue here, but completeness
is: nothing in the ledger is too small for it.

**`reckoning.html` is the picture.** Shipped on one side, remaining on the other,
the waves in the middle with their sub-tasks and their ranges, and the caveats
where a reader will hit them rather than in a footnote. It shows the leading
items per section and points at the ledger for the rest, because a page nobody
scrolls to the end of has not communicated its tail anyway.

## Writing briefs back

Turning findings into briefs is opt-in, because the skill reads the same
directory it would write to and an unstamped brief inflates the next run's
denominator. Write them only when asked, only for `unmeasured` clusters and
`unnamed` surfaces — `unbuilt` items already have briefs, and `broken` ones
have defects — and stamp each with frontmatter so re-runs update rather than
duplicate:

```yaml
---
generated-by: reckon
reckon-sources: [BLOCK-0003, CASE-0014, CASE-0021]
status: to-triage
---
```

Name an evidence-work brief for the capability it buys ("a hook that forces a
full-disk state"), not for the cases it unblocks. The cases are the reason;
the hook is the work.

## What this does not do

Route rather than reimplement — each of these is a dedicated skill:

- **Producing the evidence** → `test-campaign:test-campaign`. This reads its registry; it
  never runs tests.
- **Deciding whether a claimed-done feature is genuinely implemented** →
  `spec-validation:spec-validation`, which traces a field to its producer with file:line.
- **A whole-product survey against a stated goal** → `product-gap-analysis:product-gap-analysis`.
- **A tracker-board sweep, card by card** → `stocktake:stocktake`.
- **A page and a questionnaire for a non-technical owner** → `whats-left:whats-left`.
  Hand it `docs/reckoning/<date>/ledger.json` directly: `undecided` rows become
  its decision questions, `unmeasured` blocker clusters become evidence items,
  and `unbuilt`/`broken` rows become product items.
- **Executing the work** → `ship-fleet:ship-fleet`, or `shipyard:shipyard` per stage.

Reading source is not part of this skill's job and stays capped where it
happens: identifiers from a brief may be grepped to demote a claim or route it
to `spec-validation:spec-validation`, never to promote something to done. A grep hit is weak
evidence, and letting weak evidence close an item is the failure this skill
exists to prevent.

## Delegation and scoping

Deliver what was asked, at the scope intended. This skill runs in the main
context. The reading is a few JSON files and a directory of markdown, and the
script does the arithmetic, so delegating to subagents is generally unnecessary.
Delegate to a subagent only when a brief queue exceeds roughly 150 files where
the join needs reviewing in bulk, and then to a single subagent for the join
alone, handing back confirmed and cut edges. Do not use subagents to verify or
double-check your own work.

## Reference

- `references/partition.md` — the seven classes in full, the legality table,
  precedence when an item qualifies for two, and worked examples.
- `references/joining.md` — how briefs are tied to registry entities, why that
  step is the weak one, and how to strengthen it in a repo.
- `references/no-campaign.md` — running against briefs alone, and how the
  report must weaken its claims when it has no evidence to reconcile against.
- `references/estimation.md` — the corpus behind every duration, how it was
  measured, the tier and wave tables, and what the figures cannot say.
- `references/evidence.md` — the standards and measured results behind every
  rule above, with citations.
- `scripts/selftest.py` — proves each gate fires on a bad fixture and stays
  silent on a good one. Run it after changing `reckon.py`.
