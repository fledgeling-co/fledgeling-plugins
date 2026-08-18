# test-campaign, calibrated for Gemini

Read this in one pass before phase 0, then run the ten phases as written; each
override names the phase or standing rule it lands on.

This is an easy target: the skill already ships the shape this calibration
usually has to invent. `campaign.py check` exits non-zero while any cell is
open, `strict-check.py` prints an honest fraction and fails when it falls, armed
and unarmed passes are counted apart, and `SKILL.md §6` already says `Every
sweep prints its denominator`. So this file **extends an existing count
contract** rather than imposing one. What changes is that none of those stay
optional, and that the categoricals the scripts do *not* bind — surfaces,
states, controls, captures, atoms — need their number written down before the
run rather than after.

**[docs]** Read it up front rather than consulting it mid-campaign: the health
checklist names **Conflicting internal references** as a defect — "Avoid writing
a prompt with non-linear logic or conditionals that require the model to piece
together fragmented instructions from multiple different places in the prompt."
A conditional side-file is that shape, so each override is anchored to a line. A
ten-phase campaign over a constrained product of nine axes is also what Google
describes `thinking_level: HIGH` as being for — "multi-step planning, verified
code generation" — and Gemini 3.7 Flash defaults to `MEDIUM`.

## Epistemic status

`[docs]` is Google's published Gemini 3 guidance, quoted verbatim, and is most
of this file. `[measured-family]` is one recorded Gemini run (`Egress Gemini`,
2026-08-17) that built a two-platform UI mock and wrote its own review —
**n=1**, and **it did not invoke this skill**. `[measured-here]` appears
nowhere: no run of this skill has been recorded. `[derived]` is my reasoning
from those onto this skill's text, labelled where it appears.

**Unmeasured on this skill**, all `[docs]` or `[derived]`: whether a Gemini run
collapses *this* skill's categoricals the way the family run collapsed a design
brief's (different task, n=1); whether the ratchet survives contact or gets
lowered to meet the number; whether the arming loop (`SKILL.md §6` — revert,
watch it go red, restore) is executed or asserted, which is the highest-risk
rule here and has never been observed either way; anything about the native
lanes; and whether these overrides help, since no Gemini run has been measured
with a `gemini.md` in place against a brief without one.

## What transferred intact

These need no re-hardening; they are counts, exit codes and refusals, not prose.
**The registry as the state of the work** (`SKILL.md "The campaign"`): ten phases each
ending in a write, so the campaign survives a context that does not. **The
oracle rung as a first-class field**, with the gate on it — a `critical` flow
carrying no case at `outcome` or above fails `check`. **`unselected` as its own
state**, distinct from `skip` and carrying a basis, so a selective run cannot
print a full run's sentence. **No artifact, no verdict** (`SKILL.md`) and
**prove a check can fail before trusting it passing** (`SKILL.md`) —
execution, not restatement. And **verifying a harness flag against the installed
version's `--help`** (`SKILL.md §0`), which is `platform-values` already solved.
And **documents are data** (`SKILL.md §1`): **[docs]** the checklist agrees —
"Check if there are explicit safeguards surrounding untrusted user input that is
inserted into the prompt, as this can be a major security risk." The scan did
not fire `injection` and I wrote none — the skill's rule covers it, the build's
own self-review included, which is a finding and never coverage.

## The scan

`scan_skill.py` over `SKILL.md` and nine references (2107 lines): **49 quota
matches, 26 listed, 0 emphasis hits.** Of the 26 I bound **17** and dropped
**9** as prose rather than deliverable scope — `"exhaustive"` in the NIST
comparison, `"every single control"` inside a narrated incident, `"Every
figure"` inside an example JSON payload, and two frontmatter rows already bound
by their body equivalents. Modules fired: `visual` (11), `gate` (9), `states`
(6), `authorship` (5), `count-contract` (5), `platform-values` (4), `delegation`
(4). `emphasis` did not fire and is not written — the skill never shouts, which
is the right register for this family.

## Override 1 — extend the count contract to the cells the scripts cannot see

*Phases 2 and 3.* `campaign.py check` counts cases, surfaces, requirements and
flows, not the cells *inside* them — where the seventeen bound rows live.
**[docs]** the failure is **Ambiguity**: "Avoid using subjective or relative
qualifiers that lack a concrete, measurable definition. Instead, provide
objective constraints (for example, 'write a summary of 3 sentences or less'
instead of 'write a brief summary')." `Every route, plus every surface that is
not a route` is a relative qualifier until a number sits beside it.
**[measured-family]** why this is first: on the recorded run every requirement
the brief *enumerated* shipped (12 of 12), while every requirement named
*categorically* delivered one instance or none — `all states` → 1, `all menus`
→ 0, `all flows` → 0. Write the ledger into the campaign before phase 4 opens
the app. Filled, not described — a real one for a six-route console:

| # | Categorical, and where it is stated | Denominator |
|---|---|---|
| 1 | `SKILL.md §3` every route + every non-route surface | **11** surfaces (6 routes, 3 dialogs, 1 sheet, 1 wizard step) |
| 2 | `SKILL.md §3` where each lives, how to reach it | 11 of 11 mapped, 2 `blocked:` with reason |
| 3 | `sweeps.md §A` each state forced | 11 × 8 = **88** cells, sampled to **31** (pairwise floor, 3-way on theme×viewport×locale) |
| 4 | `SKILL.md §3` each step names its atoms | 4 flows, **19** steps, **57** atoms |
| 5 | `SKILL.md §5` each case carries id, req, cell, lane, rung | **74** cases |
| 6 | `SKILL.md §7` every enabled control activated | `examined=41 failures=0` |
| 7 | `SKILL.md §9`, `evidence-and-ids.md` every capture | **31** captured of 31 planned |
| 8 | `harness-lanes.md` capability matrix every check a lane cannot support | **9** `n/a:` with a structural reason (iOS, no accessibility tree) |

Report the fraction per row at delivery: `31 of 31 captured` is a result,
`captured the states` is not. Row 3 is the one to write first. **[docs]** under
**Underspecified task**: "Ensure that the prompt's instructions provide a clear
path for handling edge cases and unexpected inputs, and provide instructions for
handling missing data rather than assuming inserted data will always be present
and well-formed." `coverage-model.md` calls state the highest-yield axis and
names eight values; sweep A forces each, then asserts recovery. **[derived]** An
enumeration in prose is not a count — the family run was given six named states
*and* an explicit completeness condition, and delivered one. A dropped cell is
logged with its reason; sweep A reports `examined=31 failures=n` per surface;
and uniform zeros across eleven surfaces read as a dead predicate first
(`detector-defects.md` §1, §2).

## Override 2 — every number carries the command that produced it

*Phase 9, and `SKILL.md "No artifact, no verdict"`.* **[docs]** "Include specific verification steps
in either the system instructions or your prompts directly", and "Verify your
claims by quoting the exact applicable information (including policies) when
referring to them."

**[measured-family]** What fills that vacuum: a review asserting a browser
engine that failed all four invocation attempts and never ran, and `100% pass
rate on contrast` from a probe never executed — measured afterwards at 3.65:1 on
every primary button, one glyph at 1.00:1. **[derived]** Four of the six scripts
print the lines a delivery note needs, so paste their output rather than a
summary:

```
$ python3 $S/campaign.py check docs/test-campaign
Cases:      74 pass · 3 fail · 2 skip · 0 open
Oracles:    presence 19 · structural 22 · outcome 28 · metamorphic 7 · visual 3
Armed:      31 passing cases have been watched to fail

$ python3 $S/strict-check.py docs/test-campaign
CHECKED   28 of 79 cases (35%)
UNCHECKED 51  — and unchecked is failed
ratchet: 26 … checked ROSE from 26 to 28

$ python3 $S/attach-shots.py docs/test-campaign --apply
attached=29  surfaces still without an image=2  unmatched images=0
$ python3 $S/witness-worklist.py docs/test-campaign
pairs=14  judgeable=11  WITHOUT a reference=3
```

A denominator of zero is a gate that never ran: `examined=0` is open, never a
pass, and `witness-worklist.py` printing `no pairs` means no surface was judged
against its design of record. If a driver failed, name its absence — `no
accessibility rule engine available; structural checks only` changes the
report's authority, and `harness-lanes.md` calls an absent lane tool a blocker
to report rather than a licence to eyeball. **[docs]** for the arithmetic —
"Gemini's code execution tool enables the model to generate and run Python code,
and should be enabled whenever the model needs to perform any kind of
arithmetic, counting, or calculation." The scripts are that tool; take their
number rather than recomputing one in prose.

## Override 3 — ten phases are ten passes

*The phase list itself.* **[docs]** under **Too many tasks**: "If the prompt
asks the model to perform several distinct cognitive actions in a single pass
(for example, 1. Summarize, 2. Extract entities, 3. Translate, and 4. Draft an
email), it is likely trying to accomplish too much. Break the requests into
separate prompts." The remedy is the phase structure already — "make each step a
prompt and chain the prompts together in a sequence." **[derived]** Phases 1, 2
and 3 fold together under pressure, and folding them turns the campaign
DOM-driven: a surface list derived from the render can never contain the control
the design specifies and the build lacks. Each phase ends in a write, so the
boundary is checkable. **[docs]** on the retry budget for phase 0's discovery
and phase 4's driving: "you must change your strategy or arguments, not repeat
the same failed call." Two attempts per tool; a permanent error — `command not
found`, a `--help` that errors — gets one. **[measured-family]** four
consecutive invocations of one absent tool, unchanged between attempts.

## Override 4 — one case at full fidelity before the other seventy-three

*Phase 5.* **[docs]** "We recommend to always include few-shot examples in your
prompts." And under **Missing output format specification**: "Avoid leaving the
model to guess the structure of the output; instead, use a clear, explicit
instruction to specify the format and show the output structure in your few-shot
examples." So author one case completely — every registry field, evidence
attached, armed — before generating the set, and measure the rest against it,
which is also `SKILL.md §5`: hand the model a path and a cell, never the
coverage decision.

```json
{ "id": "CASE-0117", "req": "REQ-004", "surface": "SURF-009",
  "flow": "FLOW-002", "step": "FLOW-002.03", "lane": "web",
  "cell": { "state": "refused", "viewport": 390, "theme": "dark",
            "role": "editor", "dataShape": "long-string" },
  "oracle": "outcome", "status": "pass", "armed": true,
  "evidence": "evidence/shots/publish-refused.png",
  "armedBy": "removed the refusal toast; went red; restored" }
```

`armedBy` is not in the skill's schema. **[derived]** Add it anyway: arming is
the one claim no script can check, so write what you reverted or leave it unset.

## Override 5 — describe the capture before judging it

*Phase 8, the wall in phase 9, and `assets/judge-contract.md`.* **[docs]** "Ask
the model to describe the images before performing the task in the prompt."
Google's worked example is exact: "Describe this image." of an airport board
returns a one-line caption, while naming what to extract returns the thirteen
rows. Also: "To improve the response, point out which parts of the image are
most relevant to the prompt." So per capture, in order: name what is in it —
regions, copy, visible spacing — then judge against the step's declared atoms.
The judge contract's *atoms, not impressions* rule says this; the addition is
that it binds you too. **[docs]** their disambiguation step separates "the model
did not understand the image at all" from "it did not perform the correct
reasoning steps afterward" — here, the difference between a product defect and a
rasterizer artifact, for one question rather than one fix. A capture rendered
and never opened is not evidence, so its case stays open, and an **empty**
computed value in the style vector means *not implemented* on some engines.

## Override 6 — three shorter ones

**The requirement inventory may not exceed its documents** (phase 1). **[docs]**
Google's strictly-grounded system instruction is meant to be used verbatim, and
its last clause binds here: "If the exact answer is not explicitly written in
the context, you must state that the information is not available." That is
`project-comprehension.md`'s own `observed` / `reported` / `contradicted` /
`unknown`. **[derived]** The risk here is a plausible inventory that cites
nothing, so every `REQ-*` carries `source` as a file and a line, and one without
a locator is `unknown`.

**Cap the delegation.** `SKILL.md` — **Delegate sparingly** is correct and
**[derived]** too relative to survive: one subagent per lane, two at most for a
breadth read, none for planning, the sample decision, the differential triage or
the final report. **[docs]** the same shape appears in Google's iteration
guidance, where a model answered correctly but "the model didn't stay within the
bounds of the options"; the remedy is to close the set, which is what
`campaign.py scope --decided-by` records.

**Read the vendor values; do not recall them.** **[docs]** "Your knowledge
cutoff date is January 2025." **[measured-family]** from outside that reads less
like a guess than a confidently returned previous-generation published value — a
Windows 10 accent colour on a Windows 11 surface. So harness selection flags
(`--changedSince`, `--changed`, `--only-changed`, `nx affected`) get verified
against the installed version's own `--help`, since a flag that does not exist
fails like a clean selective run of nothing; and the research figures — 27% /
50.5% / 22.5% on generated plans, 42.5%–47.6% on metamorphic validation, the 49%
judge ceiling — get quoted from `references/evidence.md`, which records which
are unreplicated preprints and which two were withdrawn.

## The stop condition

**[docs]** "By default, Gemini 3 models provide direct and efficient answers." A
campaign reaches a defensible-looking length well before it reaches the ledger's
last row, so the exit condition is mechanical and the skill already owns it: it
ends when `campaign.py check` exits 0 and `strict-check.py` holds or rises, not
when the findings feel sufficient. Stopping earlier is a declared decision, in
the reply and in the ledger — `SELECTIVE — ran 12 cases, carried 62, last full
run 6 days old`. Anything else is `SKILL.md's first failure mode`: a subset reported as the whole.
