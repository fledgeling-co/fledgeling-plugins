# `warrant` — a plugin for removing the human from the verification loop

A build plan for a Claude Code plugin of eight skills, their scripts and their reference
documents. It is written against the claim graph in
`~/Dev/dAIolog/docs/research/verifier-substitution/claims.json`, and every claim id below
(`C2`, `I5`, and so on) resolves there.

## What this removes, and the one thing it does not

The plugin removes the human from **per-item** verification. Today 194 items sit in `Done`
waiting on one person to look at each of them (`C23`). Under this plugin nobody looks at an
item. What survives is a single standing signature on a policy document, renewed on a schedule,
plus whatever you tell it when it gets something wrong.

That residual is not a hedge, and it is worth being exact about why it is there, because it is
the one place this plan disagrees with its own title. Four independent research backends looked
for any regulated software vendor whose all-machine verification step had been accepted as the
control of record and none found one (`C21`). The obstruction is administrative rather than
perceptual: a 21 CFR Part 11 electronic signature must be unique to one individual, and a model
identifier is not an individual (`C11`); and PCAOB AS 2201 permits leaning on last period's
testing of a fully automated control only where the auditor verifies the control has not changed,
which a silently reversioned model can never satisfy (`C12`). Neither of those cuts a standing
scope with a named person answerable for it. Both cut a per-item machine verdict.

So the design target is: **one signature, once, on a warrant — instead of 194 signatures on
items.** If you want the signature gone too, the cheapest point to change course is Step 1
below, before anything downstream depends on `warrant.yaml` having an owner field. After Step 6
the ledger's audit value rests on that field and removing it is a migration.

The second reason is that the measurement which would justify removing the signature does not
exist and this plan does not build it. No powered non-inferiority reader study has ever been run
on code review or UI acceptance (`C1`), so "as good as a human" has no right-hand side. An
earlier draft of this plan included a prospective reader study to supply one; it was cut because
it inverted the whole point, spending human review time in order to remove human review time.
The replacement, `warrant:feedback`, learns from escapes instead. That is cheaper and never goes
stale, and the honest consequence is that it strengthens the case for keeping the standing
signature rather than weakening it: you cannot retire a control on the grounds that it has been
measured when you have chosen not to measure it.

## Architecture — five planes and a ladder

The plugin is not a jury. Adding models is the intuitive lever and the measured evidence says it
buys little: nine frontier judges from seven families supply about two effective independent
votes, panel accuracy falls 8 to 22 percentage points short of genuinely independent voting, the
best single judge matches or outperforms the whole panel across every tested condition, and
established aggregation closes at most 11% of that gap even when given the correct answers
(`C2`). The 1986 multiversion-programming result is the older half of the same lesson: 27
independently developed versions of one specification failed correlatedly and the independence
hypothesis was rejected (`C3`).

What replaces the jury is five planes, applied in this order because each one's output is the
next one's input:

| Plane | Closes | Depends on a model |
|---|---|---|
| **Oracle** — source-to-render lineage, tick-and-tie, taxonomy validation | the highest-consequence class: a correctly rendered surface asserting a figure no source supports (`I7`) | no |
| **Assay** — mutation survival, cannot-fail patterns, selection gap | whether any downstream verdict means anything (`I6`) | no |
| **Panel** — the machine verdict, evidence-channel hardened | perceptual defect classes, with a published ~16% miss ceiling (`C17`) | yes |
| **Feedback** — escape corpus, regression re-verification, false-alarm proxy | whether the machine still catches everything it has ever missed | measures the machine |
| **Lot** — risk-limited acceptance of the queue | the 194, without 194 signatures and without a batch promotion (`I2`) | no |

The ladder is how authority moves. A tier is entered by evidence and left automatically:

| Tier | Machine may close | Entry condition | Automatic exit |
|---|---|---|---|
| 0 | nothing; it advises | warrant signed, ledger writing | — |
| 1 | items where the oracle plane is green and no perceptual judgement is needed | oracle coverage ≥ 95% of rendered figures on the surface | any lineage gap |
| 2 | tier 1 plus perceptual classes with a declared miss rate | assay green, and the grader re-catches every historical escape in the class's regression corpus | model version change, any new escape in the class |
| 3 | tier 2 across all non-disclosure surfaces | a declared item count closed in the class with zero escapes over a declared window | one escape in a tier-3 class |
| 4 | tier 3 plus disclosure-content surfaces | reserved, and deliberately unreachable on current evidence | — |

Entry to tiers 2 and 3 is by absence of escapes rather than by a measured sensitivity, and that
is weaker evidence. Absence of escapes is bounded by what got noticed, so it grows more
convincing with volume and time and never becomes a rate. The ladder is written this way because
the alternative was a reader study nobody was going to run twice; recording the weakness is what
stops a later reader mistaking a clean run for a measured one.

Tier 4 is in the table so its absence is explicit rather than an oversight. Nothing in the corpus
supports letting a machine close disclosure content: the transfer argument for image-borne
prompt injection is that tenant-authored text renders into the very screenshot a vision judge
reads (`C16`), and that channel is unmeasured here.

## The skills

Eight skills in one plugin. Each is a directory with a `SKILL.md`, and the scripts named under
it live in that directory's `scripts/`.

### 1. `warrant:charter` — write and sign the warrant

Produces `.warrant/warrant.yaml`: the tier table above instantiated for this repository, the
named defect classes and which tier each sits in, the pinned model id and version for every lane,
the policy owner, the escalation routes, the revocation triggers, and the renewal date. This is
the only human-signed artifact in the system.

The reason it is a file rather than a setting is `C12`. An auditor benchmarking an automated
control has to be able to see that the control has not changed, and a signed, diffable,
version-pinned document is the form of that. DO-330 Criterion 2 asks the same thing in tool
terms: operational requirements, a qualification plan, and re-qualification whenever the tool
changes (`C10`).

Scripts: `charter_init.py` writes a first draft from the repository (it enumerates surfaces,
spec files and defect classes rather than asking). `charter_validate.py` exits non-zero on a
warrant with an unpinned model, a class assigned to a tier whose entry condition is unmet, a
missing owner, or an expired renewal date. That script is the plugin's outermost gate: everything
else refuses to run if it fails.

Acceptance: `charter_validate.py` exits 0, and `git log` shows the warrant signed by a named
person rather than by an agent.

### 2. `warrant:oracle` — the deterministic plane, built first

The order matters and it is counter-intuitive. The instinct is to start with the screenshot judge,
because that is the part that looks like verification. But the highest-consequence failure for an
IR product is not a misaligned button; it is a well-rendered page stating a number no source
supports, and a vision judge is structurally unable to catch it because nothing on the screen
looks wrong (`I7`). That class is closable with arithmetic.

Three checks, none of which needs a model and none of which reversions:

- **Lineage.** Every rendered figure carries a provenance token back to the record it came from.
  `lineage_extract.py` walks the render tree and emits `figure -> source` pairs;
  `lineage_gate.py` fails on any figure with no pair.
- **Tick-and-tie.** `tick_and_tie.py` re-computes each figure from the originating disclosure and
  compares. Tolerances are declared in the warrant, not in the script.
- **Taxonomy.** `taxonomy_check.py` validates classified fields against the schema that governs
  them, which catches a valid-looking value in the wrong field.

Acceptance: on a surface with a deliberately corrupted figure, `lineage_gate.py` and
`tick_and_tie.py` both exit non-zero and name the figure. Ship the corrupted fixture with the
plugin so this is checkable rather than asserted.

### 3. `warrant:assay` — measure the tests before believing them

Every downstream number inherits the suite's fault sensitivity, and a green suite can have very
little. More than half of over 15,000 generated mutants survived a rigorous unit, integration and
system suite that was passing (`C18`). Nobody has measured mutation survival for browser or
end-to-end suites at all, which is precisely why this has to be measured here rather than assumed
from the literature.

Three measurements, written to `.warrant/suite-health.json` with a ratchet so the numbers can
only improve:

- `mutate.py` — mutation survival over the 420 tests CI actually selects, not the 3,011 authored
  (`C23`). The selected set is what gates a merge, so it is the set whose sensitivity matters.
- `cannotfail_scan.py` — the pattern scan across all 137 spec files: assertions that cannot fail,
  `expect` with no subject, a soft assertion whose result is discarded, a try/catch that swallows
  the failure. This is the check that catches a suite passing because it is not looking.
- `selection_gap.py` — which authored tests never run in CI, grouped by the surface they cover.
  A surface whose tests are all outside the selection is a surface with no gate on it.

Acceptance: the mutation score for the selected set is recorded with its date, and
`cannotfail_scan.py` returns a count. A first run that returns a bad number is a success; a first
run that returns no number is not.

### 4. `warrant:panel` — the machine verdict, with the evidence channel hardened

This is the only plane that uses a model, and its design problem is not accuracy. It is that every
artifact the verdict rests on is reachable by the thing being judged. Frontier coding agents
modify tests, overwrite timers and monkey-patch evaluators to return success; 30.4% of RE-Bench
runs exhibited reward hacking and on some tasks every successful run did (`C14`). An audit of a
benchmark built specifically to be trustworthy found 59.4% of the audited subset materially flawed
and retired it (`C15`).

Four hardening measures, each answering one of those:

- `snapshot_evidence.py` takes a content-addressed, read-only snapshot of the diff, the test files
  and the captures **before** any judging, and the verdict records the digest. A verdict whose
  digest does not match the snapshot is void.
- `neutralise_render.py` renders the surface with tenant-authored text replaced by
  length-matched neutral filler for the judge's pass, and separately with real text for the
  human-facing capture. This is the mitigation for `C16`, and it is a mitigation rather than a
  fix: the transfer from oncology imaging to IR screenshots is an argument, not a measurement, and
  the reference document says so.
- The judge runs with the repository read-only and no write, commit or test-execution tools.
- Three lane roles, and none of them vote. The next section owns why.

#### Lanes, lenses and an adjudicator — the shape that is not a jury

Multiple models belong here, in three roles that are architecturally different from each other.
Conflating them is how a verification pipeline ends up paying panel prices for single-judge
accuracy.

**One primary grader, out of family.** A single accountable verdict, from a family other than the
one that built the work. The out-of-family requirement is not about accuracy either: author-judged
acceptance is how roughly half of a 110-ticket corpus shipped not-as-specified while reading as
complete (`C24`), and one grader that did not write the code fixes that. A second grader on the
same question does not fix it twice. `C2` is the reason to stop at one: the best single judge
matched or outperformed the full nine-judge panel across every tested condition, so a second lane
asking the same question is spending money on an effect the measurement did not find.

**Lens lanes, on orthogonal questions.** This is where extra models earn their cost. "Does this
figure tie to its source", "does this screen match the mock", "does this leak across tenants" and
"does this omit something the spec required" are different propositions, so there is no
correlated-error problem to inherit from `C2` — the lanes are not voting, they are dividing the
work. Two rules keep it honest: a lens is only a lens if its question can be answered without
reference to the others, and a lens whose question a deterministic check can answer belongs in the
oracle plane instead, where it costs nothing per run and cannot reversion.

**An adjudicator over disagreement, whose output is a route rather than a verdict.** When two
lanes conflict, majority logic is exactly the failure `C2` measures. The adjudicator's job is to
decide which deterministic check would settle the disagreement, run it, and record the answer —
the software equivalent of stopping the reading and going to look at the artifact. The evidence
that this role is worth paying for comes from this project's own research panel: the one
contaminated lane was useless as corroboration and useful as a cross-check, and four of its
discards were confirmed against the primary reports (`M4`). Catching another lane's mistake does
not require independence from it.

Two construction notes. Lane counts stay even, or a single grader plus lenses, because an odd
number of lanes invites someone to count them. And `lanes.yaml` pins a model id and version per
lane, which is what `warrant:ratchet` watches: a lane whose model moves has changed the control
(`C12`) and drops its classes to tier 0.

`verdict.schema.json` constrains the output through Structured Outputs rather than a prefill,
which current models reject. The schema's terminal states are `pass`, `fail` and
`inconclusive` — and `inconclusive` routes to a person rather than to a retry. That is not a
concession: ISO/IEC 17025 requires measurement uncertainty to be declared and treats an
inconclusive result as a valid result (`C13`), and the product's own screenshot pass already
returns `inconclusive` on all 50 surfaces that have both captures and expectations present
(`C22`). Forcing those to binary would manufacture certainty the pipeline does not have.

Acceptance: a verdict cannot be written without a matching evidence digest, and the judge's
tool list contains no write tool. Both are checkable from the run log.

### 5. `warrant:feedback` — calibration from escapes, not from a study

The skill an earlier draft called `calibrate`, rebuilt around a cheaper signal. Instead of running
a prospective reader study to establish a baseline, it learns from the cases where the pipeline was
wrong and you said so: a defect it failed to identify, or an outcome that did not match what the
task asked for.

Three things happen when you report one:

- `feedback_record.py` writes the escape against its defect class, the item, the warrant version
  and the model versions that were live at the time, and the evidence digest the verdict was
  written from. The digest matters because it makes the escape reproducible rather than anecdotal.
- `regress_build.py` turns it into a permanent case in `.warrant/regression/`, with the inputs
  that produced the wrong verdict.
- `regress_run.py` re-runs every historical escape against the current lanes and exits non-zero if
  any one of them is no longer caught. That is the plugin's self-validation, and it is the tier-2
  entry condition: a class may only be closed by machine while the machine demonstrably catches
  everything it has previously missed in that class.

This is strictly better than a one-off study in one respect and strictly worse in three, and the
skill text says which is which because the difference decides what the ratchet may conclude.

Better: it never goes stale. A study measures a model version on a date; the regression corpus
re-measures every version against every escape ever found, and it grows.

Worse, and each of these is a stated limit rather than a gap to be closed later:

- **No false-rejection rate.** If the pipeline wrongly fails a good item and nobody reviews it, the
  error is invisible. `falsealarm_proxy.py` recovers part of it by watching for churn — an item
  that fails, is resubmitted without a substantive change, and then passes is a probable false
  alarm — and it is a proxy, not a measurement.
- **A numerator with no denominator.** You learn about escapes that were noticed. `C19` is the
  cautionary case: published proficiency-test failure rates differ by more than twentyfold
  depending on what is counted, 1.4% of 670,489 challenges across 665 laboratories against 32.4% of
  lab-parameter results across three. `escape_report.py` therefore emits counts, classes and trends,
  and refuses to print a rate.
- **No bound on what is still hidden.** Without seeded items there is no way to estimate the misses
  nobody found. The regression corpus proves the pipeline catches known failure modes; it says
  nothing about novel ones, and the tier ladder's entry conditions are worded so they cannot be
  read as if it did.

Acceptance: reporting one escape produces a regression case that fails against the model version
that missed it and passes against the current one, and `regress_run.py` exits non-zero when a
historical escape stops being caught.

### 6. `warrant:lot` — the 194, as a lot rather than a queue

Two bad options and one good one. Signing 194 items individually is what nobody will finish;
promoting all 194 at once is not checking. The third way is a century old in manufacturing and in
clinical laboratories: accept the lot under a declared risk limit (`I2`).

`lot_plan.py` sizes the sample from a tolerable error rate stated in the warrant, using
risk-limiting-audit arithmetic with sequential stopping, so a clean early sample ends the audit and
a dirty one escalates it. `blind_queue.py` builds the reviewer's queue in an order that carries no
verdict, with seeds mixed in.

Two classes are census-reviewed rather than sampled, and both are named in the warrant: disclosure
content, and every item the panel marked `inconclusive`.

The denominator is where this goes wrong quietly, so the skill says it twice. Published proficiency
test failure rates differ by more than twentyfold depending on what is counted: 1.4% of 670,489
challenges across 665 laboratories, against 32.4% of lab-parameter results across three hospital
laboratories (`C19`). Both figures are correct. `lot_report.py` therefore prints the denominator
beside every rate it emits, and refuses to emit a bare percentage.

Acceptance: a lot report names its population, its tolerable error rate, its sample size, the seed
recovery rate, and the decision. A report missing any of the five does not validate.

### 7. `warrant:ratchet` — the self-validation loop

The skill that makes this a system rather than a checklist. It reads `suite-health.json`, the
regression-corpus result and the oracle coverage report, computes the tier each defect class has
currently earned, and writes it back into `warrant.yaml` as a proposed change for the owner to
sign — except for revocations, which apply immediately and need no signature.

Revocation triggers, all automatic:

- A pinned model id or version changes. This is `C12` mechanised: the control changed, so the
  benchmark no longer holds and the class drops to tier 0 until recalibrated.
- Calibration older than the warrant's staleness window.
- A control-chart violation on the regression corpus's pass rate across runs. `westgard.py`
  implements the multirule form clinical laboratories use, because a single-threshold alarm on a
  true-negative-heavy queue either never fires or fires constantly.
- One escaped defect in a class the machine was closing.

`ratchet.py` is a plain script rather than a model call, and that is deliberate: the component
deciding how much authority a model has should not be the model.

Acceptance: changing a pinned model id in `warrant.yaml` and re-running `ratchet.py` drops the
affected classes to tier 0 without asking anything.

### 8. `warrant:ledger` — what an auditor reads instead of 194 signatures

Append-only, hash-chained, one row per decision: the item, the warrant version, the model id and
version, the evidence digest, the verdict, the tier that authorised it, and the outcome if one
later emerged. `ledger.py` appends and never rewrites; `ledger_verify.py` walks the chain and
exits non-zero on a break.

This is the artifact that replaces per-item signatures in an audit conversation, and its integrity
property is the whole point: a ledger that can be edited after the fact is a ledger that proves
nothing. The repository already has this shape in
`apps/api/src/modules/audit-log/audit-capture.ts`, and the plugin should emit into that rather
than building a second chain.

Acceptance: `ledger_verify.py` detects a single flipped byte in any historical row.

## Scripts

| Script | Skill | What it does | Exit contract |
|---|---|---|---|
| `charter_init.py` | charter | drafts `warrant.yaml` from the repository | 0 on write |
| `charter_validate.py` | charter | outermost gate on the warrant | non-zero on any unmet precondition |
| `lineage_extract.py` | oracle | emits figure→source pairs | 0 with a JSON report |
| `lineage_gate.py` | oracle | fails on an unsourced figure | non-zero, names the figure |
| `tick_and_tie.py` | oracle | recomputes figures from source | non-zero on a mismatch outside tolerance |
| `taxonomy_check.py` | oracle | validates classified fields | non-zero on a schema violation |
| `mutate.py` | assay | mutation survival on the CI-selected set | 0 with a score; non-zero below the ratchet |
| `cannotfail_scan.py` | assay | finds assertions that cannot fail | 0 with a count |
| `selection_gap.py` | assay | authored-but-never-run tests by surface | 0 with a report |
| `snapshot_evidence.py` | panel | content-addressed evidence snapshot | 0 with a digest |
| `neutralise_render.py` | panel | length-matched neutral text for the judge's capture | 0 with two captures |
| `lane_run.py` | panel | runs one lane against a pinned model id and version | 0 with a verdict |
| `adjudicate.py` | panel | routes a lane disagreement to the check that settles it | 0 with the settling check's result |
| `feedback_record.py` | feedback | records an escape with class, digest and live model versions | 0 |
| `regress_build.py` | feedback | turns an escape into a permanent regression case | 0 |
| `regress_run.py` | feedback | re-verifies every historical escape | non-zero if any is no longer caught |
| `falsealarm_proxy.py` | feedback | flags fail/resubmit/pass churn as a probable false alarm | 0 with a candidate list |
| `escape_report.py` | feedback | counts, classes and trends | 0; refuses to print a rate |
| `lot_plan.py` | lot | risk-limited sample plan with sequential stopping | 0 with a plan |
| `blind_queue.py` | lot | verdict-free review order with seeds | 0 with a queue |
| `lot_report.py` | lot | the audit report | non-zero if any of the five required fields is absent |
| `ratchet.py` | ratchet | computes earned tiers; applies revocations | 0; 2 when a revocation fired |
| `westgard.py` | ratchet | multirule control chart on seed recovery | non-zero on a violation |
| `revoke.py` | ratchet | drops a class to tier 0 and writes the reason | 0 |
| `ledger.py` | ledger | appends a hash-chained row | 0 |
| `ledger_verify.py` | ledger | verifies the chain | non-zero on a break |

Every script is stdlib Python 3 where it can be, for the same reason the existing gates in this
repository are: a verification tool with a dependency tree is a verification tool that stops
running.

## Reference documents

| File | Carries | Read when |
|---|---|---|
| `references/evidence.md` | the claim graph condensed, with direct findings and inferences marked apart, and the eight sources whose contents are unread | before changing any number in any skill |
| `references/admissibility.md` | 21 CFR Part 11, PCAOB AS 2201, ISO/IEC 17025, DO-330 Criterion 2, and what each demands of the warrant | writing or renewing a warrant |
| `references/why-not-a-jury.md` | `C2`, `C3`, `C4`, the three lane roles, and the test for whether a proposed lane is a lens or a second vote | whenever someone proposes adding a model |
| `references/positioning.md` | `C7`, `C8`, the concurrent-read mechanism, and the blind-first rule | building any surface where a human sees a machine verdict |
| `references/tiers.md` | the ladder with entry and exit criteria per tier, and why tier 4 is unreachable | proposing a tier change |
| `references/measurement.md` | risk-limiting audits, Westgard multirules over the regression corpus, the numerator-without-denominator rule, and the denominator warning from `C19` | before reporting any number |
| `references/opus5-authoring.md` | the prompt-construction rules in the next section | writing or editing any runner prompt in the plugin |

`references/evidence.md` earns its place by being the file that stops a number drifting. Eight of
the twenty-two sources behind this plan are paywalled or challenge-walled with their contents
unread, and four were checked against the primary record. A reference file that does not say which
is which invites a later editor to treat all twenty-two as equally solid.

## Authoring rules for the runner prompts

Claude Opus 5 executes these skills, and several of its documented behaviours change how the
prompts should be written. Read `prompting-claude-opus-5` and the Opus 5 section of the migration
guide before editing any of them; the rules that bite hardest here are:

**Report everything, filter separately.** Anthropic's guidance is explicit that a review prompt
saying "only report high-severity issues" or "be conservative" may be followed literally, and the
model reports less. For a verification plugin that is the worst available failure, so
`warrant:panel` splits into a find pass with no severity instruction at all and a filter pass that
ranks and drops. The two passes are separate prompts, not two paragraphs of one.

**No verification scaffolding.** Opus 5 verifies its own work without being told to, and carried-over
instructions like "double-check your answer" or "use a subagent to verify" cause over-verification
at a cost with no quality gain. That reads as a contradiction in a plugin about verification and it
is not: the pipeline's gates are deterministic scripts with exit codes, and no prompt in the plugin
asks the model to re-check itself.

**Cap delegation explicitly.** Opus 5 delegates more readily than earlier models. Each skill states
which scenarios warrant a subagent, and the plugin sets `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` and
`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` rather than relying on prose. Those need Claude Code 2.1.217
or later.

**Effort per stage, swept rather than assumed.** The default is `high`. `warrant:assay` and
`warrant:ledger` are mechanical and should be tested at `low` or `medium`; `warrant:panel`'s find
pass and `warrant:panel`'s adjudicator are the candidates for `xhigh`. Where a stage runs at
`xhigh` or `max`, set `max_tokens` to at least 64k so there is room to think and act. Run the sweep
on the plugin's own eval suite rather than carrying a number over.

**Thinking stays on.** It is on by default on Opus 5, disabling it is capped at effort `high` or
below, and with it disabled the model can emit a tool call as plain text or leak internal XML tags
into visible output. For a plugin whose output is parsed, prefer low effort with thinking over
disabling it.

**Structured Outputs, not prefill.** Prefilled assistant turns are rejected on current models.
`verdict.schema.json` and `escape.schema.json` are the contract.

**Long inputs at the top, the instruction at the end.** Anthropic reports up to 30% better quality
on complex multi-document inputs when the query sits after the documents, which is the normal shape
for a diff plus its spec plus its captures.

**Calm triggers, and the reason with the rule.** "Use X when …" rather than pressure language,
which is measured as making performance worse, and a stated reason so the model generalises to the
cases the skill did not enumerate.

## Build order

Each step's acceptance condition is the gate on starting the next one.

1. **`charter`** — a signed warrant that `charter_validate.py` accepts. Everything refuses to run
   without it.
2. **`ledger`** — writing before anything is decided, so the first decision is already recorded.
   `ledger_verify.py` catches a flipped byte.
3. **`oracle`** — the corrupted-figure fixture fails both gates by name.
4. **`assay`** — a mutation score and a cannot-fail count exist, whatever they say.
5. **`panel`** — a verdict cannot be written without a matching evidence digest, and the judge has
   no write tool.
6. **`feedback`** — one reported escape becomes a regression case that fails against the model
   version which missed it and passes against the current one.
7. **`lot`** — the 194 audited under a declared risk limit, with the denominator on every rate.
8. **`ratchet`** — flipping a pinned model id drops the affected classes to tier 0 unprompted.

All eight steps are buildable with what is in the repository now, and none of them needs a
labelled case set or reader time. The cost of that is recorded above: the ladder is climbed on
absence of escapes rather than on a measured sensitivity, so its weight comes from volume and time
rather than from arithmetic, and it never becomes a rate.

The plugin should ship its own eval suite and run it in CI (`claude plugin eval`). A verification
plugin with no evals is asking for exactly the trust it exists to make unnecessary.

## Open decisions

**The tolerable error rate.** `lot_plan.py` cannot be written without one, and it is a risk-appetite
call rather than a technical one. It sets the sample size and therefore the human time this costs.

**Who signs.** `charter_validate.py` requires a named owner. Whether that is you, or a role, changes
what happens when the person holding it is unavailable — a role with no current holder is a warrant
with no signature.

**Whether the residual signature goes.** Recorded above. Step 1 is the cheapest point to decide it,
and the evidence says keeping it is the defensible option, but the axis is yours.

**The tier-3 thresholds.** Entry needs an item count and a window ("N items closed in this class
with zero escapes over M days"), and both are risk appetite rather than technical facts. Set them
too low and the ladder is decoration; too high and nothing ever reaches tier 3.

**Whether to fund the false-alarm proxy.** `falsealarm_proxy.py` is the only route to noticing a
wrongly-failed item without a human reviewing one, and it is a proxy: it infers a false alarm from
churn. The alternative is accepting that false rejections stay invisible, which is survivable
because their cost is friction rather than escape. I would build the proxy, because the failure it
catches otherwise looks like the pipeline working.

**How many lens lanes, and which.** The three roles are settled; the lens set is not. Each lens
costs a model call per item forever, and a lens whose question a script could answer belongs in the
oracle plane instead. I would start with two lenses and add only on a class that has produced an
escape.

## Out of scope

Anything that changes what the automated verifier already does. The plugin wraps the existing
out-of-family verifier and the existing screenshot pass rather than replacing either; the 50
`inconclusive` verdicts already on disk are its first input, not a defect to fix.

Mobile push, the two Expo islands and the investor backend. They have their own gates and their own
release paths, and a warrant covering surfaces the plugin cannot render is a warrant that cannot be
enforced.

A model-graded replacement for `warrant:ratchet`. The component deciding how much authority a
model holds is the one place a model should not sit, and building it later would undo the property
that makes the ladder trustworthy.
