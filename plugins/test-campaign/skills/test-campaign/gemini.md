# test-campaign, calibrated for Gemini

Read this in one pass before phase 0, then run the ten phases as written; each override names the phase or standing rule it
lands on. An easy target: the skill already ships the shape this calibration usually has to invent — `campaign.py check` exits
non-zero while a cell is open, `strict-check.py` fails when its fraction falls, and two seeded controls watch two gates go
red. This file extends that count contract to the categoricals the scripts do *not* bind — destinations, atoms, cards, phases
— and reads its stated **maxima** back. Since 0.19.0 the scripts bind ten more cells the earlier file had to count by hand:
`States`, `Comparisons`, `Routed`, `Write targets`, `Phases`, `Remaining`, `Runs`, `Corpus`, `Root` and `Design of record`
each print with a denominator or a `NOT DECLARED` naming what to record, and `next` exits 3 while unblocked work remains. Where a row below names one of those, paste the line rather than counting.

**[docs]** Read it now, not mid-campaign: the checklist calls **Conflicting internal references** a defect — "Avoid writing a
prompt with non-linear logic or conditionals that require the model to piece together fragmented instructions from multiple
different places in the prompt." Ten phases over a product of ten axes is what `thinking_level: HIGH` is for — "multi-step
planning, verified code generation" — and 3.7 Flash defaults to `MEDIUM`; that is what the level is *for*, not a remedy.

## Route out before phase 5, not after it

**[docs]** under **Task outside of model capabilities**: "Avoid using prompts that ask the model to perform a task for which
it has a known, fundamental limitation." **[measured-family]** the gap is not uniform — over 106 tasks against
`claude-opus-5`, two of eight buckets produce hard zeros (`geminify/references/evidence.md` §2.1; §2.3 bounds the harness
confound). Two phases land there:

| shape | where it lands here | measured |
|---|---|---|
| `brownfield-integration` | phases 5 and 6a — cases and oracles written into the project's existing harness; and phase 4's `-glass` build, fixing whatever stops the artifact existing | 24 against 50; zero on 79% of decided rows |
| `regression-sensitive` | phase 6 — stabilising and re-arming without breaking assertions that currently pass | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

Omitted: `static-page`, since `evidence-page.py` emits the page rather than a model authoring it; `visual-design`, since phase
8 measures structure, style, vocabulary and geometry rather than aesthetics; and the campaign's judging work entirely, the
corpus having watched a model build and said nothing about one grading. With no lane, the block still says what to distrust.

## Epistemic status

`[docs]` is Google's published Gemini 3 guidance, quoted verbatim, and is most of this file. `[measured-family]` is three
sources, none of which invoked this skill: `Egress Gemini` (2026-08-17, a UI mock that wrote its own review), `COD Dossier`
(2026-08-23, a research and authoring pipeline) and the 106-task benchmark above. `[measured-here]` now exists: 69 sessions
across 17 projects in the week to 2026-09-06 invoked this skill, and Gemini 3.8 served a share of them through a relay
(`cadence`, `perch`, `cairncopy`, `diolog-user-flows`, `dAIolog`). Mined for every turn the owner had to take: 1,649
interventions, of which gemini-served assistant turns preceded 425; of 451 distinct asks, gemini-family turns carried 177
and 47 of the 79 that followed a completion or verification claim — 27% of gemini asks; and of 91 *no visible output*
nudges, 48 landed on one relay-served lane, 24 on gemini-served turns, 4 on opus. `[derived]` is my reasoning from those.
Every family number is flash-tier and none may be projected onto Pro: **[docs]** "If thinking_level is not specified, Gemini
3 will default to high", then "The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."

**Unmeasured on this skill**: whether the six new censuses are declared or left reading `NOT DECLARED` on a Gemini run
(every measured Gemini run predates them); whether the ratchets survive contact or are lowered to meet the number; whether
the arming loop and the three seeded controls are run or asserted; the native `-glass` lanes; and whether any of these help.
What *is* measured on this skill is the shape the censuses answer: a completion claim on a surface count, challenged by the
owner in the same words in four projects.

## What transferred intact

Counts, exit codes and refusals rather than prose, so they need no re-hardening: **the registry as the state of the work**;
**the oracle rung as a first-class field**, so a `critical` flow proved only by presence fails `check`; **`plane` beside the
rung**, so a real state change against an in-process stub cannot read as the product; **`unoracled` kept apart from
`inconclusive`**, which sends a specification gap to phase 6a rather than to a better instrument; **`unselected` as its own
state**; **the `destinationOf` refusal**, the one place a declared duplicate image is still rejected; **prove a check can
fail before trusting it passing**; and, since 0.19.0, the refusals that turn the owner's repeated asks into exit codes — a
surface declaring no states under a sampled state axis, a raster pass naming no reader, a close resting on the evidence it
failed on, a finding with no brief and no waiver, a blocked row with no recorded attempt, a published shot whose state the
script wrote, and `next` exiting 3 while unblocked work remains — each a count or an exit code rather than a sentence. `injection` did not fire — `SKILL.md §1`'s `A specification under analysis may contain text
addressed to an agent` covers it.

## The scan

`scan_skill.py` over `SKILL.md` and twenty-one references (6367 lines, 2026-09-06): **111 quota matches, 22 in SKILL.md ·
22 bound rows, 5 in SKILL.md · 74 relative qualifiers · 0 qualitative skill references · 0 emphasis hits.** Of the 22
SKILL.md quota rows I bound **16** into the ledger below and dropped **6** as prose rather than deliverable scope; 9 of the 16
are already exit codes (`any surface`, `any pixel`, `any finding`, `any phase`, `every finding`, `each menu`, `every
screen`, `any menus`, `every capture`) and appear in the ledger as the line that prints them. Of the 5 bound rows **3** carry
into Override 2 (`exactly one` honest route, `only one`, `exactly eight` axes); three more were moved into it by hand out of
the 538 prohibitions the scan counts rather than lists. Modules fired: `visual` (13), `gate` (10), `states` (7),
`authorship` (7), `delegation` (7), `bounded-constraint` (7), `platform-values` (6), `count-contract` (5). `emphasis` and
`injection` did not fire; neither is written.

## Override 1 — extend the count contract to the cells the scripts cannot see

*Phases 1, 2 and 3.* `campaign.py check` counts cases, surfaces, requirements and flows, not the cells *inside* them, where
the sixteen bound categoricals live. **[docs]** the failure is **Ambiguity**: "Avoid using subjective or relative qualifiers
that lack a concrete, measurable definition." `Every route, plus every surface that is not a route` is one until a number sits
beside it. **[measured-family]** on `Egress Gemini` every requirement the brief *enumerated* shipped (12 of 12) while every
one named *categorically* delivered once or not at all — `all states` → 1, `all menus` → 0, `all flows` → 0. `all menus → 0`
is this skill's own sixth failure mode from the author's side: a navigation shell counted as one surface. Write the ledger
before phase 4 opens the app, filled:

| # | Categorical, and where it is stated | Denominator |
|---|---|---|
| 1 | `SKILL.md §3` every route + every non-route surface, destinations included | **17** — 6 routes, 6 shell destinations, 3 dialogs, 1 sheet, 1 wizard step; 15 mapped, 2 `blocked:` with a reason |
| 2 | `SKILL.md §3` `List each surface's controls`, taken from the mock | **18** across the 5 surfaces that declare any · `Controls: 11 of 18` |
| 3 | `SKILL.md §3` `List each surface's states, and hold every surface to the floor` — loading, empty, populated, error, plus each menu, tab, filter and drawer | **22** declared across 17 surfaces (4 floor + 6 menus/tabs/drawers, 2 `statesNotApplicable` on the login page) · `States: 14 of 22 declared state cell(s) proved · 9 captured` — paste the line; asked for in the same words in 4 projects |
| 4 | `SKILL.md §3` each step names its surface and the observable atoms | 4 flows, **19** steps, **57** atoms |
| 5 | `SKILL.md §5` journeys and their five durable boundaries | **4** journeys, 2 critical · `boundaries 18/20 cut` |
| 6 | `project-comprehension.md §3` `for each declared class, a provider` | **9** requirements declaring an effect · 9 providers named, 7 resolved, **2** `vacuous` |
| 7 | `SKILL.md §5` `Each case carries an id, the requirement it verifies … its oracle rung`, plus its `plane` | **80** cases · `in-tree 41 · hermetic 18 · live-glass 12 · live-external 3` |
| 8 | `SKILL.md §9` the wall of every capture, and `task-bound-flows.md §6` on each image | **31** of 31 · witnessed 22 / manifest 9 / filename 0 |
| 9 | `harness-lanes.md` every check the lane cannot support, and `sweeps.md §M`'s blind pass | **9** `n/a:` with a structural reason (iOS exposes no accessibility tree) · `examined=164 mutating=21 blind=17` |
| 10 | `task-bound-flows.md §2` live cases per card, on a board-driven run | **18** cards · 18 bound, 0 bound by route alone |
| 11 | `SKILL.md §5` `A raster-visual pass owes a reading` — reader and expectation named per pass | **14** raster passes · `Comparisons: 12 of 14 raster-visual pass(es) name what read both images` · 2 `inconclusive` |
| 12 | `SKILL.md "What counts as done"` `every finding leaves the run with somewhere to go` | **9** findings (3 red cases, 6 `DEF-*`) · `Routed: 7 of 9 finding(s) filed as a brief · 2 waived` · 0 unrouted |
| 13 | `SKILL.md §9` the twelve phases, each `ran` or `skipped: <reason>` | **12** · `Phases: ran 0 1 2 3 4 5 6 6a 7 8 8a 9 · skipped — · unrecorded —` |
| 14 | `SKILL.md §8a` `A seventh pass — unpaired` — subjects with no capture, against the subject population | **31** subjects · `pairs 29 of 31 subject(s) captured · missing 0 · excused 2` |
| 15 | `SKILL.md §0` `which tenant and dataset this campaign may mutate` | **1** declared · `Write targets: acme-sandbox · 6 case(s) declare a write` · 0 undeclared |
| 16 | `SKILL.md "A turn ends on the next item"` the remaining set at hand-back | `Remaining: 0 · blocked with a recorded attempt 2 · next: —` · `campaign.py next` exit **0** |

Report the fraction per row at delivery: `31 of 31 captured` is a result, `captured the states` is not — row 3 first, because
an enumeration in prose is not a count: the family run was given six named states *and* an explicit completeness condition,
and delivered one, and **[measured-here]** the owner's *every screen at a minimum has a loading state, empty state, content
state and then any menus, selected tabs, filters* arrived 18 times across 9 projects, 7 of them straight after a campaign had
reported itself complete on a surface count. Rows 11–16 are printed by `campaign.py check` and `capture-lineage.py --gate`;
a row you typed rather than pasted is the vacuum this file exists to name. **[docs]** under **Underspecified task**: "provide instructions for handling missing data rather than
assuming inserted data will always be present and well-formed." Row 10 exists because a board-driven run inverts the failure:
one card bound to **67** flows by route, against `A binding is a card id in the title of ONE live case whose assertion fails
when that card's producer breaks`.

## Override 2 — read every stated maximum back off the artifact

*`SKILL.md "What counts as done"` and the standing rules.* Override 1 catches a categorical scope collapsing to one instance;
this catches the opposite failure, the one that reaches a passing-looking campaign. **[measured-family]** §2.2 — across the
benchmark's UI verifiers, 58% of Gemini's failing assertions at `medium` and 86% at `high` state a **bound** (`exactly N`,
`no`, `not`, `only`) against 8% for opus, and one such rule failed on *every* instance in its set while the same run passed 37
of 39 other assertions. A bound is violated by what you did *not* write, so it survives every check that looks at what you
did. **[docs]** Google treats these as a component in their own right — "Restrictions on what the model must adhere to when
generating a response, including what the model can and can't do." — and the **Recap** is where they go: a "Concise repeat of
the key points of the prompt, especially the constraints and response format, at the end of the prompt." This is that recap:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| the run's sample | cells executed vs declared | `one cell per axis + dark×mobile, error×modal, viewer×write` = 34 | `campaign.py report <dir>` | 34 planned · 34 run | yes |
| `evidence/shots/*` | subjects per sha256 | 1, unless every member names the others, carries a `sharesReason`, and the recorded targets agree | `capture-lineage.py <dir> --gate` | `shared: 2 subjects, 1 sha256, undeclared` | **no** |
| SURF-006's six destinations | identical bytes between siblings of one shell | 0, declared share or not | `campaign.py check <dir>` | 2 destinations publish one sha256 | **no** |
| the checked fraction | effect-rung passes, run over run | may not fall while the fraction rises | `strict-check.py <dir>`, this run against last | checked 26→28, outcome-or-above 21→19 | **no** — bought by demotion |
| carried verdicts | age of the last full run | `--max-full-age-days 14` | `campaign.py check <dir>` verdict line | 6 days | yes |
| subagents | concurrent spawns | 1 per lane · 2 for a breadth read · 0 for planning, the sample decision, the differential triage and the report — a closed set rather than a judgement call | count them in the reply | 2 (web, macos-glass) · dispatched 2 / returned 2 / lost 0 | yes |
| every published capture | `provenance.scriptCalls` | **0** — any script call between navigation and shutter is `fabricated` | `capture-lineage.py <dir> --gate` | `FABRICATED` absent · `PROVENANCED 31 of 31` | yes |
| the comparison population | `missing`, run over run | may not rise | `capture-lineage.py <dir> --gate` ratchet line | `missing 0 — held` | yes |
| each raster reading | `comparison.judgedLongEdge` against the capture's long edge | at least the capture's | `campaign.py check <dir>` | 2 judged at 1568 over 2880 → `inconclusive` | **no** — re-judge cropped |
| the turn's hand-back | `campaign.py next` | exit **0** before the turn ends, or the blocker that covers every remaining row named | `campaign.py next <dir>` | `remaining 0 · blocked 2 · next: —` exit 0 | yes |

Row 4 is this skill's own shape of the failure, and `SKILL.md` states it: `The target is 100%, and there is exactly one honest
route to it: check more things`. Dropping a case to a lower rung raises the fraction and lowers what the campaign knows, and
only the rung mix tells progress from demotion. A bound stated as a prohibition also reads as style advice: `never widen a
tolerance to make an unmeasurable read pass` is already gated by `inconclusive`; `Delegate sparingly` is not, so it is the
last row.

## Override 3 — every number carries its command, and every gate is watched to fail

*Phase 9, and `SKILL.md "No artifact, no verdict"`.* **[docs]** "Include specific verification steps in either the system
instructions or your prompts directly", and "Verify your claims by quoting the exact applicable information (including
policies) when referring to them." **[measured-family]** what fills that vacuum: a review asserting a browser engine that
never ran, and `100% pass rate on contrast` from a probe never executed — measured afterwards at 3.65:1, one glyph at 1.00:1.
So:

```
$ python3 $S/campaign.py check docs/test-campaign
Directive:  prove the tasks in the Done column shipped; report.html is the deliverable
Stop when:  every card in the corpus binds to a live case, strict-check holds or rises
Root:       apps/web
Design of record: apps/web-design-system/preview/preview.html
Corpus:     38 of 41 document(s) read (docs/**/spec*.md,docs/**/plan*.md) — self-reported by `campaign.py corpus`
Runs:       3 recorded · last 2026-09-06T09:41:12+00:00 `pnpm test:e2e --project=web` exit 0 · 74 case(s)
Cases:      74 pass · 3 fail · 0 carried · 2 inconclusive · 1 unoracled · 0 open  (of 80)
Lane:       web — 62 case(s) · 58 pass · 24 at an effect rung · 27 armed  outcome:24 presence:16
Lane:       macos-glass — 18 case(s) · 16 pass · 2 at an effect rung · 4 armed  interactive-glass:2
Planes:     in-tree 41 · hermetic 18 · live-glass 12 · live-external 3
Journeys:   4 declared, 2 critical · boundaries 18/20 cut
Controls:   11 of 18 declared control(s) actuated by a passing effect-rung case, across 5 surface(s)
States:     14 of 22 declared state cell(s) proved by a passing effect-rung case · 9 captured, across 17 surface(s) that declare any
Comparisons: 12 of 14 raster-visual pass(es) name what read both images and against what
Routed:     7 of 9 finding(s) filed as a brief · 2 waived
Write targets: acme-sandbox: seeded fixture tenant, owner-sanctioned · 6 case(s) declare a write
Phases:     ran 0 1 2 3 4 5 6 6a 7 8 8a 9 · skipped — · unrecorded —
Remaining:  0 · blocked with a recorded attempt 2 · next: —
$ python3 $S/campaign.py next docs/test-campaign
remaining 0 · blocked 2 · next: —
$ python3 $S/strict-check.py docs/test-campaign
CHECKED 28 of 80 (35%) · UNCHECKED 52 — and unchecked is failed · checked ROSE from 26 to 28
$ python3 $S/vacuity-check.py docs/test-campaign --gate
unclassed: examined=19 findings=0 · uncensused: examined=9 findings=2 · blind: mutating=21 blind=17
```

**A `NOT DECLARED` line is an empty denominator, never a clean row.** `Directive`, `Stop when`, `Planes`, `Journeys`,
`Controls`, `States`, `Write targets`, `Phases`, `Corpus`, `Runs`, `Root` and `Design of record` each print that inside a green verdict and read exactly like the counted versions unless somebody looks, and so do `examined=0`, an
`attach-shots.py` with nothing to attach, and a `witness-worklist.py` reporting no pairs. **[docs]** the counting belongs to a
tool rather than to prose, since "Gemini's code execution tool enables the model to generate and run Python code".

**Four controls prove the gates bite.** Arming mutates the *system* — revert the behaviour, watch it go red, restore.
`capture-lineage.py --seed-swap SURF-001,SURF-002` mutates the *manifest* and must exit 2; `--seed-drop SURF-001` blanks a
subject's capture and must report `CAUGHT`. `vacuity-check.py --seed-strengthen` mutates the *specification*, the half 220
armed cases could not reach. Paste all four, or say which was not run. And a verdict row counts as judged only when it names
its judge and is not marked advisory: a pairing script once wrote `pass` onto 2,853 rows whose two files existed, and those
rows were reported as verification over 902 flows a judge had failed the day before.

**Receipts the gate does not check for.** **[measured-family]** on `COD Dossier` a deterministic auditor validated tag counts,
citations and contrast floors and had no check for whether the prerequisite skills had run, so two skipped invocations cleared
it. `campaign.py check` has that blind spot in one place: nothing fails when phase 8's `design-review:design-review` handoff
never happened, so that receipt is manual — a verdict file per surface, or a `skip: <reason>` row — and since 0.19.0 the
`Phases:` line records the phase itself as `ran` or `skipped: <reason>`, which is the receipt for the phase and not for the
skill call inside it.

## Override 4 — ten phases are ten passes, each ending in a file the next reads

*The phase list itself.* **[docs]** under **Too many tasks**: "Break the requests into separate prompts", and the remedy the
phase structure already is — "make each step a prompt and chain the prompts together in a sequence." **[derived]** Phases 1, 2
and 3 fold together under pressure, and folding them turns the campaign DOM-driven: a surface list read off the render cannot
contain the control the design specifies and the build lacks, which is `inert-ui.md`'s stated limit.

**[measured-family]** `COD Dossier` §1.2.1 — an instruction phrasing skill composition as a lens was satisfied by writing
compliant-looking code, and the model's own diagnosis named the mechanism: nothing downstream depended on a file only that
skill produces. Phase 8a is already the fix in the skill's own hand. **[derived]** Phase 8's other handoff is not: `hand it to
design-review:design-review for rendered quality` has no file depending on it, so give it a verdict file per surface.

**[docs]** on the retry budget for phase 0's discovery and phase 4's driving and `-glass` build: "you must change your
strategy or arguments, not repeat the same failed call." Two attempts per tool; a permanent error — `command not found`, a
`--help` that errors — gets one, which is how `SKILL.md §0` says to verify a harness's selection flag. **[measured-family]**
four consecutive invocations of one absent tool; and pivot at attempt 1 on a **capacity** error: `COD Dossier` retried `Read`
four times against a 25k ceiling before switching to a Python split, which a large PRD will need.

## Override 5 — one case at full fidelity before the other seventy-nine

*Phase 5.* **[docs]** "We recommend to always include few-shot examples in your prompts." And under **Missing output format
specification**: "Avoid leaving the model to guess the structure of the output; instead, use a clear, explicit instruction to
specify the format and show the output structure in your few-shot examples." So author one case completely — every field,
evidence attached, armed — then measure the set against it, which is `SKILL.md §5` too: hand the model a path and a cell, not
the plan.

```json
{ "id": "CASE-0117", "req": "REQ-004", "surface": "SURF-009", "lane": "web",
  "flow": "FLOW-002", "step": "FLOW-002.03", "actuates": ["Publish"],
  "cell": { "state": "refused", "viewport": 390, "theme": "dark", "role": "editor" },
  "oracle": "outcome", "plane": "hermetic", "status": "pass", "armed": true,
  "state": "refused", "mutates": true, "target": "acme-sandbox",
  "evidence": "evidence/shots/publish-refused.png",
  "comparison": { "reader": "be-my-witness:be-my-witness / claude-opus-5",
                  "expectation": "docs/ui-mockups/publish.html", "judgedLongEdge": 2880 },
  "observedVia": "row count in the audit table, read back through GraphQL",
  "armedBy": "removed the refusal toast; went red; restored" }
```

`observedVia` and `armedBy` are not in the skill's schema. **[derived]** Add both: `An outcome is a state the handler was
supposed to change, never the product's own report that it changed one` is unenforceable until the case names the channel it
read back through.

## Override 6 — describe the capture before judging it

*Phase 8, Phase 8a, and `assets/judge-contract.md`.* **[docs]** "Ask the model to describe the images before performing the
task in the prompt", and "To improve the response, point out which parts of the image are most relevant to the prompt." So per
capture: describe regions, copy, and layout before judging against declared atoms. An **empty** computed style value means
*not implemented*.

**Decide a difference on its box, not on a ratio.** `task-bound-flows.md §5` measures a spacing regression at 558 of 1,296,000 pixels
(ratio 0.00043, which every threshold passes) in a 114×13 box at density 0.377, unmistakable. Run `geometry-gate.py --stable` and
quote `agrees` / `defect` / `unstable`.

**Supply rendered rasters, not HTML sources.** **[docs]** "For UI generation, the model shows high design adherence and parity
based on a reference input, whether it's a screenshot, an image, or a full design system." Render all reference mock screens to
`evidence/shots/mock/<id>.png` before comparison. An unrendered `.html` file cannot be evaluated; `witness-worklist.py` must
exit 0 with 0 demoted references.

**The on-paper vs on-glass invariant:** A mock is a reference, never an implementation capture. It is forbidden to photograph an
HTML mock and file it as a live application capture (`shot:`). If a platform lacks a display server on this host, record `shot: null`
with an explicit structural `reason:`; never simulate glass by photographing a mock. Every inventory surface must be mapped in
`pairs.json`, and `witness-verdicts.json` must record evaluated verdicts for all judgeable captures.

**A state the capture script wrote is not a state the product reached.** **[measured-family]** seven cards on one project
were moved to Verified on captures whose state the script had inserted with `page.evaluate`, or onto which it had painted a
box reading *Verified: …*; the judge passed all seven. `provenance.scriptCalls` above zero is `fabricated` and
`capture-lineage.py --gate` exits 2 on it. Reach a state through the product and let the helper record the steps; annotate a
finding in the case record, never on the picture.

## Override 7 — shorter invariants

**The requirement inventory may not exceed its documents** (phase 1). **[docs]** Google's strictly-grounded system instruction
binds here: "If the exact answer is not explicitly written in the context, you must state that the information is not available."
Every `REQ-*` carries `source` as file:line.

**Vacuity is an unbuilt capability, never a passing feature.** When `vacuity-check.py` identifies vacuous requirements (an external
effect with no production provider), they must NOT be reported as verified. Route every vacuous requirement to `shipyard:intake` as
an unbuilt brief.

**Decide the write posture before the sweep** (phase 7). **[docs]** the agentic template's last rule: "Inhibit your response: only
take an action after all the above reasoning is completed. Once you've taken an action, you cannot take it back." Name the target
disposable or install the refusal firewall before the first click.

**A turn in flight prints `campaign.py check --line`.** **[measured-here]** of 91 *no visible output* nudges in one week, 24
landed on gemini-served turns and 48 on one relay-served lane against 4 on opus; three relay-served sessions produced runs of
5, 10 and 15. Before a long tool sequence, a dispatched batch, or a return from waiting on one, print the one line the
registry produces; where a phase has no figure the line carries none.

**Read what the prompt names; do not answer from memory.** **[docs]** "Your knowledge cutoff date is January 2025". Load the PRD,
specs, mocks and `--help` before answering.

## The stop condition

**[docs]** "By default, Gemini 3 models provide direct and efficient answers." A campaign feels finished well before the ledger's
last row. **A passive registry check is not running the campaign:** `campaign.py check` over an existing registry only checks JSON
well-formedness; it does not execute tests or captures. The campaign only ends when:
1. All declared mock screens exist as rendered PNG rasters in `evidence/shots/mock/`.
2. `evidence/shots/pairs.json` exists, mapping 100% of inventory surfaces (with 0 demoted references in `witness-worklist.py`).
3. `evidence/shots/captures.json` records every capture with verified channel, subject, and target provenance.
4. `witness-verdicts.json` records verdicts for all judgeable captures, and `capture-lineage.py --gate` passes with ratchet > 0.
5. `campaign.py check` exits 0 with every one of its sixteen lines declared, `strict-check.py` holds or rises, and vacuous/unmeasured requirements are routed to intake briefs.
6. `Routed:` reads `N of N` with every red case and `DEF-*` row carrying a brief that exists or a waiver; `Phases:` reads no `unrecorded`; `capture-lineage.py --gate` prints no `FABRICATED` and `missing` has not risen; `campaign.py next` exits 0, or the turn ends on the recorded attempt that blocks every remaining row.
