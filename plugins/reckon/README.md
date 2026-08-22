# reckon

**What is actually left, given what anybody actually proved.**

```
/plugin marketplace add h4ckf0r0day/fledgeling-plugins
/plugin install reckon@fledgeling-plugins
```

Then: *"what's left on this project?"*, *"reckon the backlog against the last
test campaign"*, or `/reckon`.

---

## The problem

A remaining-work list is built by filtering. Take everything, drop what is
done, report the rest. The filter is where it breaks, because **"not done" and
"not known" are different things and both look like absence.**

Here is an ordinary campaign — not a bad one — from a macOS file-sync client:

| | |
|---|---:|
| Designed cases | 58 |
| Reached a verdict | 25 |
| Blocked, inconclusive or never run | **32** |
| Stated requirements | 15 |
| Independently observed | **2** |

Filter that to failures and you get a tidy list of fourteen things to fix. It
looks like a plan. What it leaves out is that more than half the campaign
measured nothing at all — blocked on a dead credential, on states with no hook
to force them, on a surface reachable only by signing the owner out of their
only account — and that thirteen of fifteen requirements are the project's own
account of itself rather than anything checked.

Nothing in that list is wrong. It is just a list about 43% of the product,
presented as a list about the product.

## What reckon does instead

It refuses to filter. Every brief, requirement, case, defect and surface on
both sides resolves into exactly one class of a **total partition** — so an
item cannot fall out of the list, because there is nowhere to fall to.

| Class | What it means | Whose job |
|---|---|---|
| `unbuilt` | A brief cites registry ids and the registry holds none | product |
| `unjoined` | A brief names it; the join reached nothing either way | decision |
| `broken` | Measured, and the answer was no | product |
| `unmeasured` | **Nobody found out** | the harness |
| `unnamed` | Found in the product; no document claims it | a person |
| `undecided` | The documents and the evidence disagree | a person |
| `retirable` | Already done — close the brief | bookkeeping |
| `waived` | Somebody decided not to | exception |

Three of these are invisible to any ordinary backlog sweep, and they are the
reason this exists.

**`unmeasured` is work — and it is not the feature's work.** The job behind a
blocked case is reaching the state. Behind an inconclusive one, being able to
read the answer. Behind an unoracled one, deciding what a pass would even look
like. Those are harness jobs, and sending them to a feature backlog as "test
this properly" sends five different jobs to one wrong place. Each row carries
its own remedy.

**`waived` is neither remaining nor done.** A decision to skip is a third
thing, and it stays visible because its reason expires — a state with no hook
may get one. Fold waivers into "done" and a campaign closed by decision reads
as a campaign closed by evidence.

**`retirable` is remaining work in reverse.** A brief whose subject the
campaign proved works should be closed, not built. Reports that never retire
anything over-count forever.

## Twenty blocked cases are usually a handful of problems

Scrim's own stop declaration, from an earlier run of the same campaign,
recorded a single dead OAuth credential sitting behind **ten of its twenty**
blocked cases. Listed case by case, that is twenty line items hiding the one
thing worth doing on Monday.

So blocked cases are scheduled as **the causes behind them**, each carrying
the coverage that resolving it returns. These are the top clusters from a real
run against the campaign above — 32 blocked and inconclusive cases reduced to
24 causes:

| Unblocks | Coverage returned | Cause |
|---:|---:|---|
| 4 cases | +6.9 pts | Onboarding renders only on a first run with no account stored — reaching it means signing the owner out |
| 3 cases | +5.2 pts | Requires a full Drive quota; the live account reads 79.7 GB of 33 TB and no hook forces the state |
| 3 cases | +5.2 pts | The stored account is in `needsReauthorization` from a real `invalid_client` response |
| 2 cases | +3.4 pts | The conflicts table holds 0 rows, so the panel has nothing to draw |

That second column is the number a solo developer actually prioritises on, and
it is computed rather than guessed.

The clustering is token-overlap, so it is deliberately conservative and will
leave one cause wearing two descriptions. Every case id stays listed under its
cluster, so merging them by hand loses nothing — the script does the
mechanical pass and stops where judgement starts.

## It publishes what it cannot speak for

One blended "percent complete" hides whichever axis is weakest, so there
isn't one. There are five, they disagree with each other on purpose, and every
figure is marked as a **floor** — because each `unnamed` row is proof the
intent space is bigger than the documents describe.

A pass rate among executed cases is never labelled coverage. Decisions are
counted apart from measurements, because a decision is not a measurement.

## The gate

`reckon.py check` returns an exit code, and it gates **the integrity of the
report, not the state of the project**:

- **exit 1** — the ledger lost an item or placed one illegally. A blocked case
  presenting as done is caught here, by name.
- **exit 2** — a headline figure the rows do not support.
- **exit 3** — the ratchet: an item left `unmeasured` between two runs with no
  evidence-bearing event behind it.

Remaining work is content, at exit 0. A gate that fires because work exists
fires on every run, and a gate that always fires gets switched off.

That ratchet matters more than it looks. A snapshot gate catches a bad run;
the ratchet catches the slow version, where an item is quietly reclassified
across runs until nothing remembers it was never checked.

Twenty-one self-tests prove each gate fires on a deliberately broken ledger
and stays silent on a sound one — because a gate nobody has seen fail is
indistinguishable from a gate that cannot.

## What it will not do

It reconciles documents against evidence. It does not read your code to decide
whether something works, and it says so rather than guessing: where the
documents and the registry disagree, it routes to `spec-validation`, which
traces a claim to the code that produces its data. Identifier greps may only
ever *demote* a claim or route it, never promote something to done.

- Producing the evidence → **test-campaign**
- Is this claimed-done feature real → **spec-validation**
- Whole-product survey against a goal → **product-gap-analysis**
- Sweeping a tracker board → **stocktake**
- A page and a questionnaire for a non-technical owner → **whats-left**
  (hand it this ledger — the `undecided` rows are its input)
- Actually doing the work → **ship-fleet**

## Grounding

The design is not invented. Regulated verification has partitioned rather than
filtered for decades: **ECSS-E-ST-10-02C** mandates a Verification Control
Document recording every requirement's evidence, compliance, close-out state
and reason; **FDA** device-software guidance requires unresolved anomalies on
the record; **TTCN-3** has carried an `inconc` verdict since long before this.

The empirical case is measured. Status reports carry optimistic bias in
**60%** of cases (Snow, Keil & Wallace, n=56). Coverage correlates only
weakly with suite effectiveness once size is controlled (Inozemtseva & Holmes,
31,000 suites over five systems up to 724k lines). At Google, **84%** of
pass-to-fail transitions involved a flaky test.

Full citations in `skills/reckon/references/evidence.md`, including where two
reviewers disagreed and why one won. The corpus — three deep-research panel
members over 173 sources — is in `docs/deep-research/`.

---

MIT. Part of [fledgeling-plugins](https://skills.fledgeling.app).
