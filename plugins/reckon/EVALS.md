# EVALS — reckon

## No A/B benchmark was run

**Nothing in this file reports a comparison against a no-skill baseline,
because none was executed.** The `create-skill` pipeline's Phase 3 calls for
running each eval prompt twice — once with the skill, once with no skill at
all — and grading both blind. That did not happen here: this session operates
under an instruction not to spawn subagents unless asked, and the A/B protocol
needs eight of them.

So the open question this skill exists to answer — *does a model given these
instructions actually separate unmeasured work from failing work, where a
model without them does not?* — is **unsettled**. The eval prompts that would
settle it are written and committed at `evals/evals.json` with their
assertions; they have not been run.

An unevaluated skill that says so is honest. One whose EVALS.md merely omits
the subject reads to every later reader as though the pipeline ran, so the
absence is stated first, before anything that did pass.

## What was verified mechanically

All of the following was executed, and the exit codes are real.

### The gates fire, and they stay silent when they should

`scripts/selftest.py` builds 21 fixtures and asserts each gate on a ledger
that is wrong in exactly one way. A gate nobody has seen fail is
indistinguishable from a gate that cannot fail, so this includes a clean
control — a gate that fires on everything would be caught by it.

```
clean ledger passes                            exit=0 ok
duplicate id caught                            exit=1 ok
row with no id caught                          exit=1 ok
blocked case presenting as done                exit=1 ok
inconclusive case presenting as broken         exit=1 ok
carried case presenting as done                exit=1 ok
self-reported requirement retiring itself      exit=1 ok
unknown-evidence requirement retiring itself   exit=1 ok
class outside the partition                    exit=1 ok
retirement on a token-overlap guess            exit=1 ok
n/a presenting as verified-done                exit=1 ok
waiver with no recorded reason                 exit=1 ok
absent denominator caught                      exit=2 ok
summary disagreeing with rows                  exit=2 ok
weak join warns without blocking               exit=0 ok
ratchet catches a silent reclassification      ok
ratchet catches an item that vanished          ok
ratchet allows an earned transition            ok
orphan surface -> unnamed; reported -> unmeasured ok
contradicted evidence -> undecided             ok
every class is reachable                       ok
```

The fourth line is the one that matters: **a blocked case classed as
`verified-done` fails by name**, which is the failure the whole skill is built
against, demonstrated happening.

### It runs on real data, not a fixture

Built against `~/Dev/scrim` — 31 briefs in `docs/features-to-triage`, and the
`2026-08-21` campaign — on 22 August 2026. Pasted from the run, not
reconstructed:

```
161 rows · unbuilt 14 · broken 41 · unmeasured 73 · undecided 2 ·
waived 1 · verified-done 30
gate: clean

85 piece(s) of work remain — 40 product, 43 evidence, 2 decision — across 161
ledger rows. This reckoning speaks for 43% of the campaign's designed cases and
13% of its stated requirements; the rest is not known to be done, it is simply
not known.
```

That campaign's files were being rewritten while this was built — `cases.json`
went from 42 cases to 58 mid-session — so any figure here is true of the
21 August run as it stood on the morning of the 22nd and not of a frozen
fixture.

Two things this surfaced that a fixture would not have:

- **The headline double-counted.** A failing case and the defect it evidences
  were two remaining items. Fixed by splitting rows (total, for the gate) from
  work items (what somebody schedules), which moved the count from 127 to 88
  on the then-current data.
- **Blocker clustering was too fine.** 29 clusters over 32 cases, i.e. barely
  clustering. Replaced exact-key grouping with single-link agglomeration on
  token overlap; 24 clusters, largest 4. Threshold swept over {0.25, 0.30,
  0.34, 0.40, 0.50} on that data and set at 0.30.

The clustering remains the weakest mechanism and the skill says so: it is a
mechanical first pass a human regroups, and every case id stays listed.

### The registration is complete

`node site/scripts/build-catalogue.mjs` → **exit 0**, 45 skills, 45 icons.
This checks the four registrations, the icon set, version agreement between
`plugin.json` and the marketplace manifest, and the banner.

`render_banner.py` → 3200×1040, font loaded, no broken images, no overflow. It
also **caught a real defect**: the first banner drew the hollow rod's ring with
`inset box-shadow`, which this engine accepts and never paints. That banner
would have rendered with no ring at all and passed every other check.

## The estimates (1.9.0)

The durations the schedule prints were measured, not assumed. The corpus, the
method and the exclusions are in `skills/reckon/references/estimation.md`:
2,230 subagent transcript files parsed, 2,572 units extracted, 1,842 on Opus 4.8
or Opus 5 inside the analysis band, over 88 sessions and 31 projects, 14 Jul –
30 Aug 2026.

What that measurement supports, and what it does not:

- **Supported.** The stage and edit-volume tables, the tier ranges, and the wave
  arithmetic (wall-clock ÷ slowest member 1.05 median / 1.8 p90 over 253 real
  waves; speedup over serial 2.2× median / 4.0× p90; peak concurrency reached
  median 5, p90 10, max 16).
- **Pooled deliberately.** Opus 5 and Opus 4.8 are one population. Within the
  30–80 tool-call band their medians are 10.5 and 11.2 minutes, a gap smaller
  than the spread inside either, so separate tables would imply a precision the
  data does not carry.
- **Not measured.** Whether these figures transfer to another machine, operator
  or repo; no correction factor is offered because none was measured. Whether a
  tier assigned from a row's *wording* matches the work behind it — the tiering
  heuristic is unvalidated and the `basis` field exists so a reader can overrule
  it. Whether the estimate improves anybody's planning.
- **Structurally absent.** A failure rate. A unit that ran 40 minutes and
  produced work later rejected counts identically to one that landed.

The scheduler's own arithmetic is verified rather than assumed: a randomised
audit over 500 trials with 1–40 items per run checks that no wave inverts its
bounds, that every work item lands in exactly one wave or on the decision list,
and that no wave size — including under rounding — implies a speedup better than
the 4.0× p90 measured. That last property caught a real defect: rounding the low
bound down produced a 4.03× schedule, fractionally faster than the ceiling it had
just been held to.

## What is not verified

- **Whether the skill changes model behaviour.** See above. This is the
  important one.
- **Whether the blocker clustering matches human judgement** beyond the single
  campaign it was tuned on.
- **Whether the join generalises.** 17 of 31 of scrim's briefs joined, and only
  because that campaign's notes cite brief ids by hand. A repo without that
  habit will join worse, and how much worse is unmeasured.
- **Behaviour on tracker-board projects** rather than markdown brief queues.
  `stocktake` covers that shape; reckon has not been run against one.
- **Whether a tier read off a row's wording matches the work behind it.** The
  keyword heuristic is legible and unvalidated; that is why every estimate
  carries the reason it landed where it did.
- **Whether the HTML board is read the way it is meant to be.** It renders
  correctly in Chromium in both themes at 1280px and 420px with no console
  errors and no horizontal overflow, which is a rendering check rather than a
  comprehension one.

### The three tasks that would settle it

1. Eval 0 (`partial-campaign-not-read-as-finished`) against scrim, both arms.
   The single highest-value run: if the no-skill arm also separates unmeasured
   from failing and publishes a denominator, the skill has not earned its
   context window.
2. Eval 2 (`refuses-to-retire-on-weak-evidence`), because its prompt actively
   pushes toward the failure ("be decisive, I want the list so I can delete
   them"). A skill that folds under that pressure is worse than none.
3. Any repo whose campaign notes do **not** cite brief ids, to measure the
   join's floor rather than its scrim-flattered value.

## Decisions taken without the user

The request was *"use /clarify to make any decisions on my behalf"*, so the
`create-skill` discovery interview (Phase 0) and the name/icon checkpoint
(Phase 4) were **not put to the user**. Recording the substitution, because a
skipped hard gate that leaves no trace reads afterwards as a gate that passed.

**Referral lanes.** Four were attempted; two were down and reported as such
rather than retried:

| Lane | Result |
|---|---|
| `gemini-3.7-flash-high` (agy) | Answered |
| `claude-fable-5 --effort high` | Answered |
| `gpt-5.6-sol` (codex) | **Usage limit**, resets 27 Aug |
| `grok-4.6` + cursor-agent fallback | **402 / out of usage** on both |

Options were sent to the two live lanes in swapped order to control for
first-position bias.

**What they decided.** Both independently proposed the conservation law with an
exit code, both ranked the output ledger-JSON > generated-briefs > HTML page,
both said route the HTML to `whats-left` rather than build one, and both
independently proposed grouping blocked cases by root cause — the strongest
signal in the panel and the mechanism now carrying the most weight.

Fable added five things taken as-is: splitting decision-work out of unmeasured,
the oracle-rung floor on retirement, the precedence rule, "a reconciliation
gate over a bad join is theatre", and the cross-run ratchet.

**Where they disagreed.** On reading source code: Gemini said never (a shallow
grep manufactures false confidence and duplicates `spec-validation`); Fable
said only where documents and registry disagree, capped so code evidence may
demote or route but never promote. Fable's position was taken, because its cap
answers Gemini's objection directly.

**What the research changed.** The Dossier panel (three members, 173 sources,
~$20, 21 Aug) found a class the design was missing: an approved waiver is an
exception, not a pass. `waived` was added, `n/a` and `skip` were moved out of
the adjudicated numerator, and a waiver with no recorded reason now fails the
gate. Full corpus in `docs/deep-research/`, citations in
`references/evidence.md`.

**Decided unilaterally, without a lane.** Standalone plugin rather than a skill
inside `test-campaign`'s (it must run where there is no campaign, and reads a
directory test-campaign does not own). The name `reckon` over `remnant` and
`arrears`. The icon metaphor.

**Left on assumptions the user has not confirmed**, because these turn on taste
and priorities rather than evidence:

- The gate scores *report integrity*, not release-readiness. The OpenAI panel
  member recommended the opposite (any remaining work → non-zero exit). The
  reasoning is in `references/evidence.md` § Where this skill departs; it is a
  judgement call about which failure mode costs more, and it is reversible.
- Brief-writing is opt-in rather than default.
- `docs/reckoning/<date>/` as the output location.
