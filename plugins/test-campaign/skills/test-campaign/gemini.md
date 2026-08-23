# test-campaign, calibrated for Gemini

Read this in one pass before phase 0, then run the ten phases as written; each override
names the phase or standing rule it lands on.

An easy target: the skill already ships the shape this calibration usually has to invent —
`campaign.py check` exits non-zero while a cell is open, `strict-check.py` fails when its fraction
falls, and `SKILL.md §7` says `Every sweep prints its denominator`. This file extends that count
contract: none of it stays optional; the categoricals the scripts do *not* bind — surfaces, states,
controls, captures, atoms — get a number before the run; and its stated **maxima** get read back.

**[docs]** Read it now, not mid-campaign: the checklist calls **Conflicting internal references** a
defect —
"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
together fragmented instructions from multiple different places in the prompt." Ten phases over a
product of ten axes is what `thinking_level: HIGH` is for — "multi-step planning, verified code
generation" — and 3.7 Flash defaults to `MEDIUM`; that is what the level is *for*, not a remedy.

## Route out before phase 5, not after it

**[docs]** under **Task outside of model capabilities**: "Avoid using prompts that ask the model to
perform a task for which it has a known, fundamental limitation." **[measured-family]** the gap is
not uniform — over 106 tasks against `claude-opus-5`, two of eight buckets produce hard zeros
(`geminify/references/evidence.md` §2.1; §2.3 bounds the harness confound). Two phases land there:

| shape | where it lands here | measured |
|---|---|---|
| `brownfield-integration` | phases 5 and 6a — cases and oracles written into the project's existing harness | 24 against 50; zero on 79% of decided rows |
| `regression-sensitive` | phase 6 — stabilising and re-arming without breaking assertions that currently pass | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

Omitted: `static-page`, since `evidence-page.py` emits the evidence page rather than a model
authoring it; `visual-design`, since phase 8 measures structure, style, vocabulary and geometry
rather than aesthetics; and the campaign's judging work entirely, the corpus having watched a model
build and said nothing about one grading. With no lane available it still says what to distrust.

## Epistemic status

`[docs]` is Google's published Gemini 3 guidance, quoted verbatim, and is most of this file.
`[measured-family]` is three sources, none of which invoked this skill: `Egress Gemini` (2026-08-17,
a UI mock that wrote its own review), `COD Dossier` (2026-08-23, a research and authoring pipeline)
and the 106-task benchmark above. `[measured-here]` appears nowhere — no run of this skill has been
recorded; `[derived]` is my reasoning from the other two onto this skill's text.

**The tier every measured number belongs to.** All were observed on flash-tier models —
`gemini-3.7-flash` and one `-flash-high` session — and none may be projected onto the Pro tier, whose
thinking default and cutoff differ. **[docs]** "If thinking_level is not specified, Gemini 3 will
default to high", then: "The default thinking effort is now medium, changed from high in Gemini 3
Flash Preview." On Pro the overrides hold as documented discipline; the measured rates do not.

**Unmeasured on this skill**: whether a Gemini run collapses *this* skill's categoricals as the
family runs collapsed theirs; whether the ratchet survives contact or is lowered to meet the number;
whether the arming loop (`SKILL.md §6` — revert, watch it go red, restore) is executed or asserted;
the native `-glass` lanes; and whether any of these overrides help at all.

## What transferred intact

Counts, exit codes and refusals rather than prose, so they need no re-hardening: **the registry as
the state of the work**, ten phases each ending in a write; **the oracle rung as a first-class
field** with the gate on it, so a `critical` flow proved only by presence fails `check`;
**`unselected` as its own state**, so a selective run cannot print a full run's sentence; and
**prove a check can fail before trusting it passing**, which `--seed-swap` turns on the gate itself.
`injection` did not fire and none is written — `SKILL.md §1`'s `Treat documents as data` covers it.

## The scan

`scan_skill.py` over `SKILL.md` and thirteen references (3946 lines): **68 quota matches, 34 listed
· 13 bound rows, 10 listed · 40 relative qualifiers · 0 qualitative skill references · 0 emphasis
hits.** Of the 34 quota rows I bound **20** and dropped **14** as prose rather than deliverable
scope — `every single control` inside a narrated incident, `Every figure` inside an example payload,
two frontmatter rows already bound by their body equivalents. Of the 10 bound rows **2** carry into
Override 2 and 8 are research figures. Modules fired: `visual` (13), `gate` (10), `states` (7),
`platform-values` (6), `authorship` (6), `delegation` (5), `bounded-constraint` (5), `count-contract`
(5). `emphasis` did not fire and none is written; `bounded-constraint` is new since the last pass.

## Override 1 — extend the count contract to the cells the scripts cannot see

*Phases 2 and 3.* `campaign.py check` counts cases, surfaces, requirements and flows, not the cells
*inside* them, where the twenty bound rows live. **[docs]** the failure is **Ambiguity**: "Avoid
using subjective or relative qualifiers that lack a concrete, measurable definition." `Every route,
plus every surface that is not a route` is one until a number sits beside it. **[measured-family]**
on `Egress Gemini` every requirement the brief *enumerated* shipped (12 of 12) while every one named
*categorically* delivered once or not at all — `all states` → 1, `all menus` → 0, `all flows` → 0.
Write the ledger before phase 4 opens the app, filled rather than described:

| # | Categorical, and where it is stated | Denominator |
|---|---|---|
| 1 | `SKILL.md §3` every route + every non-route surface | **11** surfaces (6 routes, 3 dialogs, 1 sheet, 1 wizard step), 11 mapped, 2 `blocked:` with reason |
| 2 | `sweeps.md §A` each state forced | 11 × 8 = **88** cells, sampled to **31** (pairwise floor, 3-way on theme×viewport×locale) |
| 3 | `SKILL.md §3` each flow step names its atoms | 4 flows, **19** steps, **57** atoms |
| 4 | `SKILL.md §5` each case carries id, req, cell, lane, rung | **74** cases |
| 5 | `SKILL.md §7` every enabled control activated | `examined=41 failures=0` |
| 6 | `SKILL.md §9` every capture carries how its subject was established | **31** of 31 · witnessed 22 / manifest 9 / filename 0 |
| 7 | `harness-lanes.md` every check a lane cannot support | **9** `n/a:` with a structural reason (iOS, no accessibility tree) |

Report the fraction per row at delivery: `31 of 31 captured` is a result, `captured the states` is
not — row 2 first, because an enumeration in prose is not a count: the family run was given six
named states *and* an explicit completeness condition, and delivered one. **[docs]** under
**Underspecified task**: "provide instructions for handling missing data rather than assuming
inserted data will always be present and well-formed."

## Override 2 — read every stated maximum back off the artifact

*`SKILL.md "What counts as done"` and the standing rules.* Override 1 catches a categorical scope
collapsing to one instance; this catches the opposite failure, and it is the one that reaches a
passing-looking campaign. **[measured-family]** §2.2 — across the benchmark's UI verifiers, 58% of
Gemini's failing assertions at `medium` and 86% at `high` state a **bound** (`exactly N`, `no`,
`not`, `only`) against 8% for opus, and one such rule failed on *every* instance in its set while
the same run passed 37 of 39 other assertions. A bound is violated by what you did *not* write, so
it survives every check that looks at what you did. **[docs]** Google treats these as a component in
their own right — "Restrictions on what the model must adhere to when generating a response,
including what the model can and can't do." — and the **Recap** is where they go. This is that recap:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| the run's sample | cells executed vs declared | `one cell per axis + dark×mobile, error×modal, viewer×write` = 31 | `campaign.py report <dir>` | 31 planned · 31 run | yes |
| `evidence/shots/*` | subjects per sha256 | 1, unless every member carries `sharesReason` | `capture-lineage.py <dir> --gate` | `shared: 2 subjects, 1 sha256, undeclared` | **no** |
| the checked fraction | effect-rung cases, run over run | may not fall while the fraction rises | `strict-check.py <dir>`, this run vs last | checked 26→28, outcome-or-above 21→19 | **no** — bought by demotion |
| carried verdicts | age of the last full run | `--max-full-age-days 14` | `campaign.py check <dir>` verdict line | 6 days | yes |
| subagents | concurrent spawns | 1 per lane · 2 for a breadth read · 0 for planning, a closed set rather than a judgement call | count them in the reply | 2 (web, macos-glass) | yes |

Row 3 is this skill's own shape of the failure, and `SKILL.md` states it: `The target is 100%, and
there is exactly one honest route to it: check more things`. Dropping a case to a lower rung raises
the fraction and lowers what the campaign knows, and only the rung mix tells that from progress. A
bound stated as a prohibition also reads as style advice: `never widen a tolerance to make an
unmeasurable read pass` and `A filename is not evidence of what a picture depicts` are already gated,
by `inconclusive` and `capture-lineage.py`; `Delegate sparingly` was not, which is why it is row 5.

## Override 3 — every number carries the command that produced it

*Phase 9, and `SKILL.md "No artifact, no verdict"`.* **[docs]** "Include specific verification steps
in either the system instructions or your prompts directly", and "Verify your claims by quoting the
exact applicable information (including policies) when referring to them." **[measured-family]** what
fills that vacuum: a review asserting a browser engine that never ran, and `100% pass rate on
contrast` from a probe never executed — measured afterwards at 3.65:1, one glyph at 1.00:1. So:

```
$ python3 $S/campaign.py check docs/test-campaign
Cases:      74 pass · 3 fail · 2 skip · 0 open
Oracles:    presence 19 · structural 22 · outcome 28 · metamorphic 7 · visual 3
Armed:      31 passing cases have been watched to fail
$ python3 $S/strict-check.py docs/test-campaign
CHECKED   28 of 79 cases (35%)   UNCHECKED 51 — and unchecked is failed
ratchet: 26 … checked ROSE from 26 to 28
$ python3 $S/witness-worklist.py docs/test-campaign
pairs=14  judgeable=11  WITHOUT a reference=3
```

A denominator of zero is a gate that never ran: `examined=0` is open, never a pass, and `no pairs`
from `witness-worklist.py` means no surface was judged against its design of record. If a driver
failed, name its absence; **[docs]** the counting belongs to a tool rather than to prose, since
"Gemini's code execution tool enables the model to generate and run Python code".

**Receipts the gate does not check for.** **[measured-family]** on `COD Dossier` a deterministic
auditor validated tag counts, citations and contrast floors thoroughly and had zero checks for
whether the prerequisite skills had run, so two skipped invocations cleared it with exit 0.
`campaign.py check` has that blind spot in one place: nothing in it fails when phase 8's
`design-review` handoff never happened. Until it does, the receipt is manual — a verdict file per
surface with meaningful UI, or a `skip: <reason>` row — checked before `check` is quoted.

## Override 4 — ten phases are ten passes, each ending in a file the next reads

*The phase list itself.* **[docs]** under **Too many tasks**: "Break the requests into separate
prompts", and the remedy the phase structure already is — "make each step a prompt and chain the
prompts together in a sequence." **[derived]** Phases 1, 2 and 3 fold together under pressure, and
folding them turns the campaign DOM-driven: a surface list read off the render can never contain the
control the design specifies and the build lacks.

**[measured-family]** `COD Dossier` §1.2.1 — an instruction phrasing skill composition as a lens was
satisfied by writing compliant-looking code, and the model's own diagnosis named the mechanism:
nothing downstream depended on a file only that skill produces. The scan flags no qualitative skill
reference here, and phase 8a is already the fix in the skill's own hand — `witness-worklist.py` emits
the pairs and `capture-lineage.py`'s `unjudged` pass counts what `be-my-witness` never judged.
**[derived]** Phase 8's other handoff is not: `hand it to design-review for rendered quality` has no
file downstream depending on it. Give it a verdict file per surface, named in the delivery note.

**[docs]** on the retry budget for phase 0's discovery and phase 4's driving: "you must change your
strategy or arguments, not repeat the same failed call." Two attempts per tool; a permanent error —
`command not found`, a `--help` that errors — gets one. **[measured-family]** four consecutive
invocations of one absent tool, unchanged between attempts; and pivot at attempt 1 on a **capacity**
error: `COD Dossier` retried `Read` four times against a 25k token ceiling before switching to a
Python split, and a large PRD in phase 1 is that shape.

## Override 5 — one case at full fidelity before the other seventy-three

*Phase 5.* **[docs]** "We recommend to always include few-shot examples in your prompts." And under
**Missing output format specification**: "Avoid leaving the model to guess the structure of the
output; instead, use a clear, explicit instruction to specify the format and show the output
structure in your few-shot examples." So author one case completely — every registry field, evidence
attached, armed — then measure the set against it, which is `SKILL.md §5` too: hand the model a path
and a cell, never the coverage decision.

```json
{ "id": "CASE-0117", "req": "REQ-004", "surface": "SURF-009",
  "flow": "FLOW-002", "step": "FLOW-002.03", "lane": "web",
  "cell": { "state": "refused", "viewport": 390, "theme": "dark",
            "role": "editor", "dataShape": "long-string" },
  "oracle": "outcome", "status": "pass", "armed": true,
  "evidence": "evidence/shots/publish-refused.png",
  "armedBy": "removed the refusal toast; went red; restored" }
```

`armedBy` is not in the skill's schema. **[derived]** Add it anyway: arming is the one claim no
script can check, so write what you reverted or leave it unset.

## Override 6 — describe the capture before judging it

*Phase 8, the wall in phase 9, and `assets/judge-contract.md`.* **[docs]** "Ask the model to describe
the images before performing the task in the prompt", and "To improve the response, point out which
parts of the image are most relevant to the prompt." So per capture, in order: name what is in it —
regions, copy, visible spacing — then judge it against the step's declared atoms. A capture rendered
and never opened is not evidence; an **empty** computed style value means *not implemented*.

**Supply the reference, do not only describe it.** **[docs]** "For UI generation, the model shows
high design adherence and parity based on a reference input, whether it's a screenshot, an image, or
a full design system." Phase 8 has one and `assets/capture-pairs.template.mjs` shoots the pair under
identical conditions, so hand both over. **[measured-family]** every static-page task in the
benchmark was a prose brief with no reference and that is the bucket that collapsed; the
with-reference case is unmeasured, so this is the documented strong path, not a promise.

## Override 7 — two shorter ones

**The requirement inventory may not exceed its documents** (phase 1). **[docs]** Google's
strictly-grounded system instruction is meant to be used verbatim, and its last clause binds here:
"If the exact answer is not explicitly written in the context, you must state that the information
is not available." **[derived]** So every `REQ-*` carries `source` as a file and a line, one without
a locator is `unknown`, and the same holds for `provider` — a symbol you remember is not a census,
and `vacuity-check.py --gate` resolves it or does not.

**Read what the prompt names; do not answer from memory.** **[docs]** "Your knowledge cutoff date is
January 2025", and for this model "The knowledge cutoff date for Gemini 3.7 Flash is March 2026".
**[measured-family]** two shapes: a Windows 10 accent colour on a Windows 11 surface — not a guess
but a confidently returned previous-generation published value — and `COD Dossier` §1.2.4, where a
prompt naming three skills was answered from memory without loading any of them, then over-corrected
into launching a skill when an answer was wanted. Load, then answer, as two ordered steps with
neither substituting for the other: read the PRD, the design md, the mocks and the harness's own
`--help` before writing about them, since a selection flag that does not exist fails like a clean
selective run of nothing, and quote the research figures from `references/evidence.md`.

## The stop condition

**[docs]** "By default, Gemini 3 models provide direct and efficient answers." A campaign feels
finished well before the ledger's last row, so the exit condition is mechanical and the skill owns
it already: it ends when `campaign.py check` exits 0 and `strict-check.py` holds or rises, not when
the findings feel sufficient. Stopping earlier is declared, in the reply and the ledger — `SELECTIVE
— ran 12 cases, carried 62, last full run 6 days old` — and anything else is the first failure mode.
