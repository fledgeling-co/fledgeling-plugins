# The core, and the module catalogue

The core goes in every `gemini.md`. The modules are selected by
`scripts/scan_skill.py` from what the target skill demonstrably contains, so a
skill that renders nothing gets no capture protocol and a skill that ships no
probe gets no gate section. That selection is the mechanism by which design
guidance reaches design skills and general guidance reaches everything else,
without anyone classifying a skill by hand.

Quote the corpus, not this file — `references/gemini-corpus.md` holds the verbatim
sources, and `verify_quotes.py` checks against it.

---

# Part 1 — The core

## C1. The quota ledger

**Says:** every categorical quantifier in the skill becomes a row with a number.
Write the ledger into the deliverable before building, one cell per unit, each
filled with real content or `n/a: <reason>`; report the fraction at delivery
(`48 of 50 cells built, 2 n/a with reasons`).

**Why:** **[docs]** the checklist entry for **Ambiguity** prescribes objective
constraints over relative qualifiers, and **Too many tasks** explains why one
pass cannot satisfy five categorical nouns at once. **[measured-family]** a run
delivered 12/12 enumerated features and 1 of 6 named states.

**The trap worth naming in the file:** an enumeration stated in prose is not
enough. `ux-craft` names six states *and* an explicit completeness condition
(*"The mock is incomplete until all six exist"*) and the run delivered one. The
count has to become a cell to fill and a number to report, not a sentence to read.

## C2. Verification is asked for, not assumed

**Says:** every number in a delivery note carries the command that produced it and
that command's output. A denominator of zero is a gate that never ran, never a
pass. Never let the artifact assert its own verification — record what was run, or
record nothing. If a driver failed, the honest line names its absence.

**Why:** **[docs]** *"Include specific verification steps in either the system
instructions or your prompts directly"* and *"Verify your claims by quoting the
exact applicable information"*. **[measured-family]** the vacuum left by removing
verification scaffolding filled with a named engine that never ran, a contrast
pass rate that inverted the truth, and an audited-target count nothing produced.

**Note for the file:** say plainly that this reverses the house style. Removing
verification scaffolding is correct for a model that over-verifies; inheriting
that removal here is the defect.

## C3. The retry ceiling

**Says:** two attempts per tool, then change approach. A permanent error —
`command not found`, a `--help` that errors — gets one. Read the repo's own
constraints before the first call.

**Hard tool limits (capacity / token ceilings):** on the first capacity error
(e.g., `Read` tool returning `File content exceeds maximum allowed tokens (25000)`),
pivot immediately on attempt 1 to Python chunking, streaming, or line-ranged reads
rather than retrying the same call with minor offset tweaks.

**Why:** **[docs]** *"On *other* errors, you must change your strategy or
arguments, not repeat the same failed call."* **[measured-family]** four
consecutive invocations of one banned, absent tool with no change between them in
`Egress Gemini`, and four consecutive `Read` failures against a 25k token ceiling
in `COD Dossier` before pivoting. The class is documented beyond this repo:
`gemini-cli` carries a master tool-loop issue and ships a loop detector whose halt
message names *"repetitive tool calls"* (`references/evidence.md` §7.2).

## C4. Passes, not one sweep

**Says:** build in passes, one per axis, each output feeding the next.

**Sequential Artifact Dependencies (Tool Chaining):** When a skill composes other
skills (e.g. `design-craft`, `ux-craft`), never phrase the requirement as a
qualitative standard or lens (*"Every design decision goes through design-craft with
ux-craft's lens"*). On the one measured run carrying that phrasing (`COD Dossier`,
`references/evidence.md` §1.2.1), both skill invocations were skipped and the model's
own diagnosis named the mechanism: the rules were already in context, and nothing
downstream depended on a file only those skills produce.

Instead, model tool composition as an **executable dependency chain** where Phase N
outputs a concrete intermediate file artifact (e.g., `DESIGN.md`, `UX.md`,
`direction.json`) that Phase N+1 explicitly consumes:

```javascript
// Example Tool Sequence in gemini.md:
await Skill({ skill: "design-craft:design-craft" }) // outputs DESIGN.md
await Skill({ skill: "ux-craft:ux-craft" })         // outputs UX.md
// Phase N+1 reads DESIGN.md and UX.md before writing code:
await Write({ file_path: "index.html", content: ... })
await Bash({ command: "python3 scripts/audit_page.py index.html" })
```

**Why:** **[docs]** **Too many tasks**, and the chaining remedy: *"make each step
a prompt and chain the prompts together in a sequence."* **[measured-family]**
`COD Dossier` skipped both `design-craft` and `ux-craft` tool invocations because
the instruction was phrased as qualitative guidance and `index.html` did not
mechanically depend on an intermediate file output from those skills. The shape is
corroborated outside this repo (`references/evidence.md` §7.2): an Antigravity
user reporting subagents ignoring their instructed skills, and a Gemini 3 **Pro**
transcript reasoning past a GEMINI.md rule by reclassifying it — *"might be a
general guideline for agents"* — so the conversion from guidance to artifact-gated
step is worth doing on every tier, not only Flash. Where the caller controls the
API request, forced execution also exists natively — **[docs]** the
function-calling mode *"any: Model is constrained to always predict a function
call"* — but a skill file cannot set it, which is why the artifact dependency is
the lever this file prescribes.

## C5. One worked example before the set

**Says:** author one instance at full fidelity, in the artifact, and treat it as
the exemplar the rest are measured against. Every override that asks for a table
or a note ships one filled in.

**Why:** **[docs]** *"We recommend to always include few-shot examples in your
prompts … you can remove instructions from your prompt if your examples are clear
enough in showing the task at hand"*, plus **Missing output format
specification**, which asks for the structure to be shown in the examples.

## C6. `thinking_level`

**Says:** one line stating that this skill's work is what Google describes `HIGH`
as being for, and that Gemini 3.7 Flash defaults to `MEDIUM`. Only where true —
a lookup-shaped skill does not need `HIGH`.

**Why:** **[docs]** the `thinking_level` table and the `HIGH` description
(*"multi-step planning, verified code generation"*).

**And the measured caveat, which belongs in the same line rather than in a section
of its own.** **[measured-family]** `references/evidence.md` §2.3 — paired across
106 benchmark tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean
−1.7 points. So write this as what Google says the level is *for*, never as a
remedy: nothing in `bounded-constraint`, C1 or C2 gets better by raising it, and a
file that implies otherwise sells a more expensive run as a fix. Where the target's
work is genuinely multi-step planning, name `HIGH` and say the uplift is unmeasured
on this corpus.

**Name the tier the evidence is about.** Every measured rate in this skill is
flash-tier (`gemini-3.7-flash`, plus one `3.7-flash-high` session), and the
`thinking_level` defaults have drifted across the family — **[docs]** *"If
thinking_level is not specified, Gemini 3 will default to high"*, then from the
3.5 Flash release notes: *"The default thinking effort is now medium, changed from
high in Gemini 3 Flash Preview."* The corpus's defaults table has 3.7/3.6/3.5
Flash at `MEDIUM`, 3.5 Flash-Lite at `MINIMAL`, and 3.1 Pro preview at `HIGH` — so
a skill written against one tier's default silently gets a different thinking
budget on another. The level also couples to tool volume: **[docs]** *"Higher
thinking levels encourage the model to use more tools to explore and verify, so
lowering the level can reduce tool calls."* A `gemini.md` states which model its
measured claims were observed on and does not project flash-measured rates onto
the Pro tier: on Pro the overrides hold as `[docs]`-grounded discipline, while
every `[measured-family]` number is an open question. One sentence in the
epistemic-status block covers it.

## C7. Recall is not a source

**Says:** any value that a vendor publishes gets read, not remembered. The same rule
covers files: a skill or document *named in the prompt* gets loaded before the answer
is written — read, then answer, as two ordered steps, with neither substituting for
the other.

**Why:** **[docs]** the January 2025 knowledge floor for the Gemini 3 family
(March 2026 for 3.7 Flash, with some domains still at the earlier floor), and
Google's own remedy of stating the cutoff and grounding. **[measured-family]**
`references/evidence.md` §1.2.4 — asked a question naming three skills, the run
answered from memory without loading any of them; asked to fix it, it inverted the
error and launched a skill instead of answering.

## C8. The epistemic-status block

**Says:** near the top, which tiers this file uses, `n=` for anything measured,
and an **unmeasured on this skill** list. Plus the self-limitation: **[docs]** a
conditional side-file is the *"conflicting internal references"* shape the
checklist warns about, so the file is read in one pass and each override names the
section it lands on.

## C9. The route-out block

**Says:** name the work this skill does that a Gemini run should hand to another
model rather than attempt, and give the command that picks the lane. Two or three
sentences and a short table, near the top, before the overrides — because a reader
who is about to route the work out should not first read four pages about how to do
it well.

The shapes measured far enough behind to name, and what they are:

| shape | what it is | measured |
|---|---|---|
| `static-page` | a self-contained page authored from nothing | 22 against opus's 67 |
| `brownfield-integration` | editing existing multi-file code under several acceptance criteria at once | 24 against 50 |
| `visual-design` | judged aesthetic quality of a rendered surface | 35 against 63 |
| `regression-sensitive` | it must not break a contract that currently passes | 42 against 65 |

And the shapes that must **not** appear in that block, because naming them would
route away work Gemini does as well as opus: `greenfield-module` (75 against 75),
`algorithmic` (75 against 75), `accessibility` (64 against 69), `react-ui` (63
against 69).

The handoff itself is one line, and it is a pointer rather than a pinned model,
because the numbers move and a lane restated in fourteen files is a policy nobody
can change:

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape <shape>
```

**Why:** **[docs]** the prompt health checklist says it outright, under **Task
outside of model capabilities**: *"Avoid using prompts that ask the model to perform
a task for which it has a known, fundamental limitation."* This section is where a
`gemini.md` names which of the target skill's work that sentence applies to.
**[measured-family]** `references/evidence.md` §2.1 — four of eight work buckets are
level and two produce hard zeros on 71% and 79% of decided rows, so a file that
treats the gap as uniform spends its overrides in the wrong place. And the
**Ambiguity** entry's preference for objective constraints applies to the routing
rule as much as to the work: `when this is hard, get help` is a qualifier, and a
named shape with a number is not.

**Two conditions on writing this section at all.**

**Only for skills whose work the corpus measured.** The bench measures a model
*building* something, so `implementation` and `general` are the shape-gated
classes. A skill whose work is judging, referring, critiquing for completeness or
reviewing rendered UI gets no route-out block — the corpus is evidence about a
different question, and `lane_pick.py` returns the policy answer unchanged for
those classes anyway. Say in one clause that you omitted it and why.

**Only for shapes the target actually produces.** A skill that never authors a
standalone page does not need the `static-page` row. Map the target's own
deliverables onto the table and drop the rows that do not land; a four-row table
copied whole is the same defect as a module that fires on a skill it does not fit.

**What it is not.** Not an instruction to give up, and not a preamble asking
permission. The rest of the file still applies to the work that stays. Where the
run is going to do the work anyway — no lane available, the user asked for this
model specifically — the block's value is that it says which part of the output to
distrust, which is worth more than a routing suggestion nobody can act on.

---

# Part 2 — The modules

## `visual` — the skill renders something

**Trigger:** screenshot, capture, crop, viewport, computed style, DPR, mockup,
contrast ratio, a named browser driver.

**Says:** a capture denominator (one per unit × state × platform, all opened, the
fraction reported), and **describe the crop before judging it** — name what is in
it, then judge. Point at the region rather than handing over a whole frame. When a
finding looks wrong, ask what is in the image first.

**Why:** **[docs]** *"Ask the model to describe the images before performing the
task in the prompt"*, the airport-board example where naming what to extract turns
a one-line caption into thirteen rows, *"point out which parts of the image are
most relevant"*, and the disambiguation step separating *"the model did not
understand the image at all"* from *"it did not perform the correct reasoning
steps afterward"*. **[measured-family]** 3 render calls and 4 images opened for a
10-cell artifact.

**Second lever, added from the bench evidence:** where the skill can supply a
**reference input**, say so and say what to supply. **[docs]** Google's launch
material for this model claims *"For UI generation, the model shows high design
adherence and parity based on a reference input, whether it's a screenshot, an image,
or a full design system."* **[measured-family]** every static-page task in
`references/evidence.md` §2.2 was a prose brief with no reference, and that is the
bucket that collapsed. The two together are suggestive rather than settled — nobody
has measured the with-reference case on this corpus — so write it as the documented
strong path and mark it unmeasured.

## `gate` — the skill ships a deterministic check

**Trigger:** preflight, probe, lint, blocker, exit code, denominator, worklist,
a `scripts/` path.

**Says:** paste the gate's output, not a claim about it. Print the denominator.
Prove the gate can fail before trusting it passing — uniform numbers across
varied inputs are the signature of a predicate matching nothing. Assert against
the probe's real return shape. If the runner could not run, the artifact is
ungated and the delivery says so.

**Prerequisite artifact & execution receipt checks:** Deterministic audit scripts
(`scripts/audit_*.py`) must check that required upstream artifacts (e.g.,
`DESIGN.md`, `UX.md`, `claims.json`) exist and are non-empty before checking final
properties. If an upstream skill or tool call was skipped, the gate must fail with
an explicit error and exit code 1.

**Why:** **[measured-here]** on this skill's own quote gate, a one-line change
took the checked count to zero and turned every file green; only re-running the
negative control caught it. **[measured-family]** on `COD Dossier`, `audit_page.py`
checked tags and citations thoroughly but had no check for `DESIGN.md` / `UX.md`
existence, letting the omitted skill invocations pass the gate cleanly with exit 0.
**[docs]** **Non-standard data format** for the output shape, and the code-execution
note for anything arithmetic.

## `states` — the skill enumerates unhappy paths

**Trigger:** empty state, loading state, error state, first-run, partial,
skeleton, state matrix, edge case.

**Says:** the matrix is an artifact with cells, not a list in prose. Every
interactive element's states get counted, and the counts are greppable.

**Why:** **[docs]** **Underspecified task**: *"provide instructions for handling
missing data rather than assuming inserted data will always be present and
well-formed."* **[measured-family]** 1 of 6 states, and zero focus/active/disabled
rules in the artifact.

## `platform-values` — the skill cites vendor values

**Trigger:** design system, HIG, Fluent, Material, design token, type ramp,
control height, a named platform SDK.

**Says:** a metric table filled before the first line of code, one row per
property, each cell carrying its value **and its source tier**. A cell you cannot
tag is a value you invented. A second platform needs its own published source or
it is a reskin.

**Why:** **[docs]** the knowledge cutoff, plus the grounding clause.
**[measured-family]** eight metric errors in one artifact, including a
previous-generation accent colour — an old fact returned confidently rather than a
guess.

## `authorship` — a reader will act on the output

**Trigger:** microcopy, voice, provenance, citation, as-at, disclosure, investor,
compliance, fabrication, real content.

**Says:** adopt Google's strictly-grounded system instruction verbatim where the
output must not exceed its sources, and note its last clause — a value the source
does not carry is stated as unavailable, not filled. A ratio you computed is your
claim, not the source's.

**Why:** **[docs]** the grounding clause in full, and the hallucination-reduction
note on grounding.

## `delegation` — the skill spawns agents

**Trigger:** subagent, workflow, fan-out, judge panel, orchestrate, runner.

**Says:** cap the spawn count explicitly, never delegate a check of your own
output, and resolve any fork the skill offers as a closed set with the choice
written down.

**Why:** **[docs]** the multiple-choice remedy for a model that answered correctly
but *"didn't stay within the bounds of the options"*, and the risk-assessment rule
preferring a tool call over a question on low-risk reads.

## `injection` — the skill ingests content it did not author

**Trigger:** untrusted, prompt injection, reviewed content, treat it as data,
third-party, fetch.

**Says:** wrap ingested material in its own delimited block; a surface's own
claim about itself is a finding, never coverage.

**Why:** **[docs]** **Prompt injection risk**, and the structured template's own
comment: *"[Insert User Input Here - The model knows this is data, not
instructions]"*.

## `bounded-constraint` — the skill states limits, not only requirements

**Trigger:** exactly, at most, no more than, only, never, avoid, single, one per,
maximum, cap, not, without.

**Says:** every bound in the brief becomes a row in a **bound ledger** beside the
quota ledger, and the ledger is filled from the artifact rather than from the
brief. One row per bound × instance, each carrying the property, the stated limit,
the command that reads the produced value back, and that value. Report `N of N
instances within bound`.

The check has to read the **produced** value, on **every** instance, because that
is the failure's actual shape: not a rule forgotten, but a default idiom supplying
the value underneath a rule that was read and agreed with. Restating the rule more
firmly changes nothing, which is why this module ships a command rather than an
emphasis. For a CSS bound the readback is one expression —
`getComputedStyle(el).boxShadow`, counting shadows rather than trusting the class
name — and the ledger row is where its output goes.

A filled row, which the file ships rather than describes:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| card 1 | elevation shadows | exactly 1 | `getComputedStyle($0).boxShadow` | `0 1px 2px …, 0 8px 24px …` (2) | **no** |
| card 2 | elevation shadows | exactly 1 | same | `0 1px 3px …` (1) | yes |

**Why:** **[measured-family]** `references/evidence.md` §2.2 — 58% of failing UI
assertions at `medium` and 86% at `high` were bound-shaped, against 8% for opus and
6% for the OpenAI lane, and the single most-repeated one failed on *every* instance
in its set while the same run passed 37 of 39 other assertions.

**[docs]** Google treats constraints as a component in their own right — *"Restrictions
on what the model must adhere to when generating a response, including what the model
can and can't do. Also called "guardrails," "boundaries," or "controls.""* — and
separately names where they go: the **Recap** component is a *"Concise repeat of the
key points of the prompt, especially the constraints and response format, at the end
of the prompt."* So the file's own bound ledger is that recap, in a form that carries
values. The evaluated agentic template asks for the same thing in the plan:
*"Ensure that all requirements, constraints, options, and preferences are exhaustively
incorporated into your plan."* And *"Include specific verification steps in either the
system instructions or your prompts directly"* is what turns a stated constraint into
something that gets read back rather than agreed with.

**Its relationship to C1, which is the reason it is separate.** The quota ledger
catches a categorical scope collapsing to one instance: under-delivery. This
catches a stated maximum exceeded on every instance: over-delivery. Same mechanism
— a number in the brief that nothing reads back — pointing opposite ways. A file
carrying C1 alone covers half of it, and the half it misses is the one that reaches
a passing-looking artifact.

**The trap worth naming in the file:** a bound stated as a prohibition reads as
style advice. *"Avoid heavy or doubled shadows"* and *"exactly one soft shadow"*
are the same requirement, and the run treated both as taste. Convert a prohibition
into a counted property with a readback, and say in the file which of the target
skill's own sentences you converted.

## `count-contract` — the skill already promises a count

**Trigger:** slide count, whole count, worklist, ledger, inventory, enumerate.

**Says:** the easiest module to write, because the skill already has the right
shape. Extend it: derive the count when the brief omits one, and cover the cells
rather than only the top-level items.

**Why:** **[docs]** **Ambiguity** — a named count is already an objective
constraint, which is why these rules survive on this family when the prose around
them does not.

## `emphasis` — the skill shouts

**Trigger:** MANDATORY, CRITICAL, REQUIRED, ABSOLUTE, FORBIDDEN, or MUST in caps
(`scan_skill.py` counts them).

**Says:** read the emphasised passage as a plain rule and give the capitals no
extra weight — in particular, do not read urgency as a substitute for the run.
Do not reproduce the register in anything you write downstream.

**Why:** **[docs]** **Overt manipulation**: *"foundation model performance will no
longer improve and in many cases will get worse"*, and *"Avoid unnecessary or
overly persuasive language."*

---

## Two things a module must never do

**Fire on a skill that does not earn it.** The trigger threshold exists because
single-keyword matching put seven of eight modules on a skill that renders
nothing. If a module fires and the skill's subject does not support it, drop it
and say you did.

**Restate the core.** If a module's content is already covered by C1–C8, it is not
a module; it is the core applied to this subject, and it belongs in the sentence
where the core names the target's own rule.
