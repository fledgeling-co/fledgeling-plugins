# stocktake, calibrated for Gemini

Read this in one pass before step 1, then run the sweep as written. Each override names the step it lands on, because
a side-file is otherwise the shape the checklist warns about — **[docs]** *"Avoid writing a prompt with non-linear
logic or conditionals that require the model to piece together fragmented instructions from multiple different places
in the prompt."*

## What transferred intact — change none of it

Built against a worker it does not trust, this skill already carries much of this discipline.

- **The oracle order** — `Write the numbered requirement list now, and do not read further until it exists.` A step
  whose completion condition is a file that exists survives the family change; a step phrased as a standard does not.
- **`Inconclusive is a result, not a retry.`**, `--verdict ungraded`, and `A lane that is rate-limited, signed out, or
  returns an empty output file with a clean exit is a lane failure, not a quiet pass` — three first-class ways to
  record that the method did not run, where most skills have none. The last is Override 2's rule already written.
- **The close-out prints its own exit code** — `echo "gates rc=$?"`, and `Report the exit code you actually saw.` A
  claim carrying the command that produced it is this file's core requirement, already written into the skill;
  Override 8 only fills in the row's shape.
- **`gates.py selftest` runs 38 cases over fixture ledgers**, each checked against a reverted gate: the negative
  control the `gate` module asks for. And `classified`, `banked` and `dispatched` ask whether an act happened, not
  whether the record claims it.
- **The verdict shape is a closed set of three words.** **[docs]** the documented remedy for a model that answered
  correctly but *"didn't stay within the bounds of the options"* — *"you can rephrase the instructions as a multiple
  choice question and ask the model to choose an option."*

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, quoted verbatim from `geminify/references/gemini-corpus.md` |
| `[measured-family]` | Gemini runs of *other* skills: `Egress Gemini` (2026-08-17, **n=1**), `COD Dossier` (2026-08-23, **n=1**), and the 106-task `diolog-2.0` benchmark |
| `[derived]` | reasoning from those, and the third-party reports in `geminify/references/evidence.md` §7 |

**The tier the evidence is about.** Every measured claim below was observed on **`gemini-3.7-flash`** — both effort
levels on the benchmark, plus one `gemini-3.7-flash-high` session. On the Pro tier these overrides hold as
`[docs]`-grounded discipline and every rate is an open question. The family's own defaults moved mid-generation —
**[docs]** *"The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."* — so a level
written against one tier gets a different budget on another.

**Unmeasured on this skill:** no Gemini run of `stocktake` exists, and no paired run with and without a `gemini.md`
has been made against any skill, so nothing here is measured to work. The corpus measures a model **building, never
judging**, so every rate below is evidence about *authoring a sweep record* rather than about whether the verdicts in
one are right; `Egress Gemini`'s fabricated review (Override 2) is the closest analogue, at one session. The two rules
the skill added on 27 August — cache-replay arming, and the gate that never runs — come from a sweep whose model
family it does not name, so Overrides 8 and 9 are `[docs]` discipline over a family-agnostic finding. The skill's own
evidence (Kohli, the mammography study, the 110-ticket corpus, METR) is about automated judgement in general.

## No route-out block, and which shapes were omitted

**[docs]** *"Avoid using prompts that ask the model to perform a task for which it has a known, fundamental
limitation."* No shape can honestly be named. All four the corpus measured behind — `static-page`,
`brownfield-integration`, `visual-design`, `regression-sensitive` — describe *producing* an artifact, while this skill
authors no page, is `Audit-only on product code while judging.`, judges no rendered surface, and hands implementation
to `ship-fleet`; `lane_pick.py` returns the policy answer unchanged for its `verification`, `completeness` and
`referral` classes.

## Override 1 — the sweep's own numbers are cells, not sentences

Lands on step 1 and step 3. **[measured-family]** On one recorded run of another skill, every requirement stated as a
count landed — twelve named features, all present — while every requirement named *categorically* landed once or not
at all: all states → 1, all menus → 0, all flows → 0. Here that is a card whose newest comment was read, whose
attachments were not, and whose list came from whatever the diff addressed.

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition."*
`scan_skill.py --refs` returned 5 categorical rows: two prose (a path precondition `snapshot_evidence.py` enforces
itself, a note about the selftest), one bound in Override 3's ledger, and `evidence`'s `every row`, a receipt in
Override 8's table. The one left, plus four the regex could not see:

| Row | Where the skill states it | Report as |
|---|---|---|
| Comments read per card, oldest to newest | step 1 | `9 of 9`, in the row's note |
| Attachments opened per card | `the-oracle-order.md` | `2 of 2`; an unfetchable one is **inconclusive** |
| Requirements numbered, each carrying its source | `the-oracle-order.md:53` | `7 of 7 tagged [body] / [comment n] / [image]` |
| Requirements traced to a producer with `file:line` | step 3 | `7 of 7 classified REAL / AUTHORED / MOCK` |
| Critical requirements with an oracle rung recorded | `testing-adequacy.md` | `3 of 3`, rung named per requirement |

Every `n/a` cell carries its reason, and card one is filled at full fidelity as the exemplar — **[docs]** *"Make sure
that the structure and formatting of few-shot examples are the same."*

```
R1  Widget titles render as a heading element    [body]          REAL      web/ui/Title.tsx:44
R2  ...including the empty state                 [comment 3]     MOCK      no producer found
R3  Existing headings are not re-levelled        [comment 5]     n/a       explicit non-goal
R4  Spacing matches the attached mock            [image: shot-2] AUTHORED  tokens.css:19
```

## Override 2 — a verdict row carries the lane's argv and its output, or it is `ungraded`

Lands on step 5 and step 6. **[measured-family]** `Egress Gemini` wrote itself a review of five well-formed rows,
every verdict `PASS`: it named an engine it had invoked four times and never run, reported *100% pass rate on
contrast* from a probe that never executed while every primary button measured 3.65:1, and reported `Interactive
Targets Audited: 47` when nothing produced that number. Not dishonesty: a requested *shape* completed without the
procedure that earns it, and a graded board is a well known shape.

So the ledger note carries the lane's argv, `wc -c` of its output file and the verdict word copied out of it; an empty
output with exit `0` is `--verdict ungraded` with the lane named. And `Take the digest before the lane sees anything.`
— `gates.py` counts that a digest is present, not when it was taken, so the note keeps snapshot and lane in the order
run. **[docs]** *"Include specific verification steps in either the system instructions or your prompts directly."* ·
*"Inhibit your response: only take an action after all the above reasoning is completed."*

## Override 3 — this skill's requirements are mostly maxima, and that is the failure mode

Lands on `references/verification-lanes.md`, step 9 and the operating rules. **[measured-family]** Across 106
benchmark tasks, **58%** of Gemini's failing UI assertions at `medium` and **86%** at `high` were bound-shaped
(`exactly N`, `no`, `not`, `only`), against **8%** for opus and **6%** for the OpenAI lane, and the most-repeated
bound failed on *every* instance in its set. Not a rule forgotten: a default idiom supplies the value underneath a
rule that was read and agreed with, so restating it changes nothing. The grading default idiom is *ask several models
and take the majority*, and this skill's central rule is the prohibition against it — `Do not build a jury.`

**[docs]** Constraints are a component in their own right — *"Restrictions on what the model must adhere to when
generating a response, including what the model can and can't do."* — and the **Recap** component is where they go: a
*"Concise repeat of the key points of the prompt, especially the constraints and response format, at the end of the
prompt."* This is that recap, filled from the run:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| card WEB-1234 | out-of-family lanes asked | exactly 1 | `grep -c '^lane=' <dir>/cards/WEB-1234/lanes.log` | 1 | yes |
| packet to the lane | bytes | < 50KB | `wc -c packet.md` | 86,412 | **no** — re-sent as 4 files, 29,004 |
| brief files | cards per brief | ≤ 3 | `python3 $S/gates.py briefs-written <dir>` | 3 | yes |
| deferrals | cards sharing one reason | ≤ 3 | `python3 $S/gates.py dispatched <dir>` | 61 on one sentence | **no** |
| the pass | product files edited while judging | 0 | `git diff --name-only -- . ':!docs' ':!.stocktake'` | 0 | yes |

Four of the skill's own prohibitions became those rows, because a prohibition in prose reads as style advice: `Do not
build a jury.`, `Audit-only on product code while judging.`, `A deferral covers one card, never the set.`, and
`Packets stop working somewhere around 50KB.`

## Override 4 — two attempts, and a hard ceiling pivots on attempt 1

Lands on step 2, step 5 and `verify_queue.sh`. **[measured-family]** Given `File content (28636 tokens) exceeds
maximum allowed tokens (25000)`, `COD Dossier` retried the same `Read` **four consecutive times** before pivoting to a
Python split. **[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed
call."*

So a diff over the packet ceiling pivots immediately — the requirement list plus the changed files, never a trimmed
whole diff — and two attempts per tool, one for a permanent error, then the next family, recorded. `Some lanes refuse
concurrent instances.`: a killed sibling returns an empty log and no error, reading as a lane that answered nothing
rather than one that never ran.

## Override 5 — read the card, then decide

Lands on step 1, step 7 and every reference this skill names. **[measured-family]** Asked a question naming three
skills, `COD Dossier` answered from memory without loading any of them; corrected, it inverted the error and launched
a skill instead of answering. There is no stable mapping from *named in the prompt* to *loaded*, so the rule is two
ordered steps: read what the prompt names, then answer. **[docs]** *"The knowledge cutoff date for Gemini 3.7 Flash is
March 2026"*, with some domains still at *"Your knowledge cutoff date is January 2025."*

So a request naming a column policy, a warrant tier or a lane order loads `references/column-policy.md`, `warrant`'s
own state or `references/verification-lanes.md` first; the tier passed to `ledger.py` is read from the warrant, being
`the authority the verdict was made under, not the one you want`; and Kohli's numbers and the 17025 reading are quoted
from `references/evidence.md`, never recalled.

## Override 6 — `spec-validation` and `clarify` become phases whose output is a file

Lands on step 3 and step 8. `scan_skill.py` flagged **no** qualitative skill references; reading the skill found two —
`Invoke that skill where it is installed rather than reimplementing it.` and `Apply clarify's gate` — each naming a
skill without naming an artifact a later step reads. **[measured-family]** On `COD Dossier` an instruction phrasing
composition as a lens was satisfied by writing compliant-looking code directly, and the model's own diagnosis named
the mechanism: nothing downstream depended on a file only those skills produce; **[derived]** (`evidence.md` §7.2) the
same shape is reported on the Pro tier. **[docs]** *"the output of one prompt in the sequence becomes the input of the
next prompt"* is what holds a chain, so the phases are wired that way:

```javascript
await Skill({ skill: "spec-validation:spec-validation" })   // → <dir>/cards/<KEY>/trace.md
await Skill({ skill: "clarify:clarify" })                   // → <dir>/cards/<KEY>/decisions.md
await Bash({ command: "python3 $S/gates.py evidence <dir>" })   // step 9's brief reads both
```

`trace.md` carries one row per requirement with its verdict and `file:line`; fewer rows than the requirement list, or
a missing file, makes the card **inconclusive** rather than a pass. `decisions.md` may read *no open decisions*, but
an absent file is a step that did not run.

## Override 7 — describe each attachment before extracting requirements from it

Lands on step 1 and `references/the-oracle-order.md` §Read the images. The `visual` module fires on its *input* half
only: the skill renders nothing, so the reference-input lever is dropped and no capture denominator applies.
**[docs]** *"Ask the model to describe the images before performing the task in the prompt."* The worked example is
the argument: *"Describe this image."* returns a one-line caption of an airport board, while naming what to extract
returns thirteen rows. And *"To improve the response, point out which parts of the image are most relevant to the
prompt."*

So per attachment, in this order: name what is in it (surface, state, the verbatim error string), point at the region
the card is about, then write the requirement rows it produces. A screenshot summarised as *a screenshot of the bug*
is a card that was looked at and produced nothing, and an image that cannot be fetched makes the card inconclusive
with the attachment named — **[docs]** *"provide instructions for handling missing data rather than assuming inserted
data will always be present and well-formed."*

## Override 8 — a gate nobody read and a gate that passed serialise identically

Lands on step 9's close-out and `references/running-long.md`. The skill measures this itself now: on a sweep that
graded 53 cards and banked 32 warrant rows, `gates.py` was invoked once with `--help`, all six gate points went
unchecked, `warrant_column.py` was never called while the ledger it reads was being written to, and the run reported
success — a skill `57.2% deciding and 0.6% gating.` That finding is family-agnostic; what makes it an override is
Override 2 one layer up, where a graded-board shape completed in five `PASS` rows against a procedure with 40 cells. A
gate point is another such cell.

So paste the close-out as receipts — `python3 scripts/gates.py <gate> <dir>` then `echo "gates rc=$?"`, one row each,
filled from the run rather than summarised:

| gate | rc | what it printed |
|---|---|---|
| `covered` | 0 | `44 of 44 cards have a row` |
| `evidence` | 0 | `44 of 44 rows carry a sha, a lane, a verdict word or a question` |
| `briefs-written` | 0 | `17 briefs, 44 cards, max 3 per brief` |
| `dispatched` | 1 | `61 cards share one deferral reason` — 58 handed to ship-fleet, re-run rc=0 |
| `classified` | 0 | `31 graded cards name a defect class` |
| `banked` | 0 | `25 of 25 terminal verdicts in .warrant/ledger.jsonl` |

- **A gate that could not run says so in the same sentence as the result** — `--verdict ungraded` aimed at the gate
  set rather than a card, and the only honest empty cell in that table. Never pipe the command either: a piped rc is
  the pipeline's, not the gate's.
- **`dispatched` and `banked` separate a finished run from a finished audit** — `a sweep that consults the warrant
  without appending contributes zero however many cards it grades — one such run produced 241 verdicts and left the
  counter at 0.` An audit-only run skips `dispatched` in the open with `gates.py covered evidence classified banked
  <dir>`; passing it with wording is what that gate was rewritten to catch.
- **Uniform results across varied cards are a predicate matching nothing**, so `gates.py selftest` (`38 of 38` fixture
  cases) runs before any row above is believed. **[docs]** *"Ensure that all requirements, constraints, options, and
  preferences are exhaustively incorporated into your plan."*

## Override 9 — an arming run replayed from cache is a negative control that never ran

Lands on step 4. The skill's newest rule: `A cached task replays its previous PASS when the inputs hash the same`, and
`the replay is indistinguishable from a real pass`. That is Override 8's trap inside the check step 4 calls the
cheapest real one, so the arming record carries both runs' argv and both outputs rather than the word red:

```
$ npx jest -c apps/web/jest.config.js --testPathPatterns=widget-title   # Title.tsx:44 reverted
  ✕ renders the title as a heading           1 failed, 12 passed                         rc=1
$ git checkout -- apps/web/ui/Title.tsx && npx jest -c apps/web/jest.config.js --testPathPatterns=widget-title
  ✓ 13 passed                                                                            rc=0
```

Two conditions the skill states and that block reads back: the runner is invoked directly or with `--skip-nx-cache`,
because `nx show project <name> --json` prints the resolved cache value and `the presence of inputs proves nothing on
its own`; and the reverted line is named, because `reverting the wrong one of two similar call sites proves nothing`.
A red run with no matching restore, or two runs sharing an argv `nx` could have served from cache, is `--verdict
inconclusive` rather than an armed assertion. **[docs]** *"Verify your claims by quoting the exact applicable
information (including policies) when referring to them."*

## `thinking_level`, and the register

**[docs]** `HIGH` is described for *"multi-step planning, verified code generation"*, which is what a card's
trace-and-grade cycle is; Gemini 3.7 Flash defaults to `MEDIUM`. Write it as what the level is *for*, never as a
remedy — **[measured-family]** paired across 106 tasks, `high` beat `medium` on 24, lost on 24, tied on 58, and failed
*worse* on bounds, 86% against 58%.

**[docs]** *"Higher thinking levels encourage the model to use more tools to explore and verify, so lowering the level
can reduce tool calls."* Read that in the other direction here: the tool calls are the work — every comment, every
attachment, every gate — so lowering the level buys a cheaper run that read less. `scan_skill.py` counted **0**
emphasis tokens in this skill, so there is nothing to read down and nothing here should add any.
