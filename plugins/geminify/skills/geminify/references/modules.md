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

**Why:** **[docs]** *"On *other* errors, you must change your strategy or
arguments, not repeat the same failed call."* **[measured-family]** four
consecutive invocations of one banned, absent tool with no change between them.

## C4. Passes, not one sweep

**Says:** build in passes, one per axis, each output feeding the next.

**Why:** **[docs]** **Too many tasks**, and the chaining remedy: *"make each step
a prompt and chain the prompts together in a sequence."*

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

## C7. Recall is not a source

**Says:** any value that a vendor publishes gets read, not remembered.

**Why:** **[docs]** the January 2025 knowledge floor for the Gemini 3 family
(March 2026 for 3.7 Flash, with some domains still at the earlier floor), and
Google's own remedy of stating the cutoff and grounding.

## C8. The epistemic-status block

**Says:** near the top, which tiers this file uses, `n=` for anything measured,
and an **unmeasured on this skill** list. Plus the self-limitation: **[docs]** a
conditional side-file is the *"conflicting internal references"* shape the
checklist warns about, so the file is read in one pass and each override names the
section it lands on.

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

## `gate` — the skill ships a deterministic check

**Trigger:** preflight, probe, lint, blocker, exit code, denominator, worklist,
a `scripts/` path.

**Says:** paste the gate's output, not a claim about it. Print the denominator.
Prove the gate can fail before trusting it passing — uniform numbers across
varied inputs are the signature of a predicate matching nothing. Assert against
the probe's real return shape. If the runner could not run, the artifact is
ungated and the delivery says so.

**Why:** **[measured-here]** on this skill's own quote gate, a one-line change
took the checked count to zero and turned every file green; only re-running the
negative control caught it. **[docs]** **Non-standard data format** for the output
shape, and the code-execution note for anything arithmetic.

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
