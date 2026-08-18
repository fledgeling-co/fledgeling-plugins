# mac-craft, calibrated for Gemini

Read this in one pass before § Knowledge sources, then run the skill as written. Each
override below names the section of `SKILL.md` it lands on, because a conditional
side-file is exactly the shape Google's own health checklist warns about.

**[docs]** Under **Conflicting internal references**, Google asks you to avoid a prompt
whose logic requires the model to "piece together fragmented instructions from multiple
different places in the prompt." That is this file. So it is short, it is read once, and
it adds nothing the skill already enforces.

The delta is small: `references/model-calibration.md` is already a Gemini calibration for
this pipeline, and `scripts/mock_check.py` already turns seven prose audits into an exit
code. What is left is the gap between a check that fires once per mock and a scope stated
per control.

## Epistemic status

| Tier | Used here | Source |
|---|---|---|
| `[docs]` | yes, throughout | Google's published Gemini 3 guidance, quoted verbatim |
| `[measured-family]` | yes, **n=1** | `Egress Gemini`, 2026-08-17 — a Gemini run on a two-platform Mac/Windows mock, invoking this skill's **predecessor** (`mac-design-studio`) |
| `[measured-here]` | no | no Gemini run of `mac-craft` as it stands has been recorded |
| `[derived]` | yes | reasoning from the two above, plus reading `scripts/mock_check.py` |

The family evidence sits unusually close to this target: the measured artifact *was* a Mac
mock, so the 3.65:1 primary buttons and the 1.00:1 glyph were measured on the thing this
skill makes. Still one run, on the predecessor file, and not a rate.

**Unmeasured on this skill:**

- No Gemini run against the rebuilt `SKILL.md` or against `mock_check.py`. Every claim
  that the gate closes the measured gap is `[derived]`.
- No comparison of a run *with* this file in place against one without it. The overrides
  are derived from stated mechanisms, not proven remedies.
- Nothing about which Gemini version: cutoffs and `thinking_level` defaults differ across
  the 3.x family.
- The direction catalogue, the essence test, the lookalike check and the variety
  discipline are untested on this family in either direction.

## What transfers intact — do not re-derive these

- **The retry ceiling and the refusal rule** — `model-calibration.md:92-98` already says
  two attempts, one for a `command not found`, and never re-pitch a refused capability.
  **[docs]** matching Google's agentic rule to "change your strategy or arguments, not
  repeat the same failed call."
- **`thinking_level`** — `model-calibration.md:65-67` already sets it. **[docs]** a
  committed multi-surface design with a seven-row audit is what `HIGH` is described as
  being for: "multi-step planning, verified code generation". Gemini 3.7 Flash defaults
  to `MEDIUM`.
- **Recall is not a source** — `model-calibration.md:54-59` already states the January
  2025 floor and the read-never-remember rule, and `SKILL.md:151` already makes an
  untaggable cell a defect. **[docs]** the remedy is grounding: "Grounding with Google
  Search connects the Gemini model to real-time web content, and should be enabled
  whenever the model may need to know obscure or recent facts."
- **The untrusted-content guard** — `SKILL.md:255-256` already ships the verbatim
  sentence for any agent brief. **[docs]** that is the **Prompt injection risk** control:
  "Check if there are explicit safeguards surrounding untrusted user input that is
  inserted into the prompt, as this can be a major security risk." No `injection`
  override is written below because there is nothing to add.
- **Verification asked for, not assumed** — `SKILL.md:186` already says to paste the
  counters verbatim and that `examined=0` is never a pass. **[docs]** this is Google's
  own instruction, "Include specific verification steps in either the system
  instructions or your prompts directly," discharged by an exit code rather than prose.
- **The register.** The scan found zero shouted directives in 1,565 lines across
  `SKILL.md` and its references. Nothing to de-escalate; no `emphasis` module.

## Override 1 — the quota ledger, because a gate that fires once is not a denominator

**Lands on:** step 5 (build the artifact) and step 6 (gate it).

`SKILL.md:168` reads `Every control carries hover/focus/active/disabled`, and
`mac-essence.md:21` names six async states. **[derived]** Read `check_keyboard` and
`check_states` in `scripts/mock_check.py`: the keyboard check FAILs only when
`:focus-visible` **and** `:focus` are both zero across the whole file, and the states
check emits a NOTE per missing pseudo-class, at `examined=1`. So **one** focus rule and
**one** `:hover` rule anywhere in the mock clear both. The gate is a presence signal for
these two checks; the scope in the sentence is per control, and nothing counts it.

**[measured-family]** That is the gap the run fell into: six `:hover` rules total for two
entire apps, `:focus-visible` 0, `:focus` 0, `:active` 0, `:disabled` 0, and 12
`<div onclick>` carrying the navigation.

**[docs]** Google's remedy is a number rather than a scope word. Under **Ambiguity**:
"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition. Instead, provide objective constraints (for example, 'write a summary of 3
sentences or less' instead of 'write a brief summary')."

So write this into the spec **before** the first line of CSS, filled the way it is
filled here — a two-surface commission, light and dark:

```
mac-craft:quota
axis                        formula                          due   built
surface × appearance        2 surfaces × 2 appearances         4     4
async states                6 × 2 async surfaces              12    11 + 1 n/a (no partial-load path)
control states              4 × 14 interactive controls       56    52 + 4 n/a (static labels, no :disabled)
captures opened             surface × state × appearance      16    16
metric rows, tier-tagged    1 per metric used                  9     9
audit rows                  7 rows × 2 surfaces               14    14
menu-bar commands           1 per toolbar command              6     6
```

Report the fraction in the delivery, in this form:
`52 of 56 control-state cells, 4 n/a with reasons · 11 of 12 async cells · 16 of 16 captures opened`.
An `n/a` carries its reason or it is an open cell.

**[docs]** The same checklist explains why one build pass will not cover seven axes: under
**Too many tasks**, "Break the requests into separate prompts", the remedy being to "make
each step a prompt and chain the prompts together in a sequence." Run step 5 as passes —
structure, tokens, states, words, keyboard — each reading the previous pass's output,
rather than as one sweep whose artifact happens to contain all five words.

## Override 2 — the state matrix is cells with copy, not a list in prose

**Lands on:** step 5, second bullet, and the state matrix in step 7's delivery.

`SKILL.md:168` already distinguishes rendered from specified states. Keep that, and make
the specified half an artifact. **[docs]** Under **Underspecified task**, Google asks you
to "provide instructions for handling missing data rather than assuming inserted data
will always be present and well-formed." A matrix of cells is that instruction; a
sentence naming six states is not.

One surface worked in full, as the exemplar every other surface is measured against:

```
surface   state     rendered   real copy shipped in the cell
Accounts  ideal     yes        4 accounts, live balances
Accounts  empty     yes        "No accounts yet" · "Add your first account" · illustration
Accounts  loading   spec       skeleton rows ×4, no spinner, 200ms delay before it shows
Accounts  partial   spec       "2 of 4 accounts synced" + per-row retry, list stays usable
Accounts  error     spec       "Couldn't reach Ledgerline. Check your connection." + Retry
Accounts  done      spec       toast "Synced 4 accounts", auto-dismiss 4s, undo not applicable
```

**[docs]** Authoring one instance in full before the set is the strongest single lever
Google names: "We recommend to always include few-shot examples in your prompts", and "you
can remove instructions from your prompt if your examples are clear enough in showing the
task at hand." Their **Missing output format specification** entry adds the corollary —
"show the output structure in your few-shot examples."

The same rule applies one level up: **build one surface in one appearance completely,
gate it, look at it, and only then build the rest.** A second surface authored before
the first is gated inherits every defect the gate would have named.

## Override 3 — the two provenance families, and the second-platform source

**Lands on:** the provenance marks at `SKILL.md:63-75`, and step 3's metric block.

`SKILL.md:151` already states that a cell you cannot tag is a value you invented, and
`mock_check.py [metrics]` already cross-checks `kit`-tagged rows against both the
published value and your stylesheet. Two additions, both **[derived]** from where this
family fails:

- **Do not collapse precision into strength.** `#ECECEE (estimated)(confirmed)` and
  `#ECECEE (specified)(canon)` carry the same hex and different authority. Emitting one
  mark is how a single-surface reading becomes a platform value one file downstream —
  and dropping a mark is invisible to the gate, which reads tier tags, not corpus marks.
- **A second platform needs its own published source.** **[measured-family]** the run's
  Windows theme was the macOS theme with the caption buttons moved and a 3px accent bar
  added: same 48px titlebar, same nav width, no Mica, and Windows **10**'s `#0078D4`
  accent on a Windows 11 app. That last one is not a guess; it is a superseded published
  value returned confidently.

**[docs]** Which is a cutoff artifact, not carelessness: "Your knowledge cutoff date is
January 2025", and for the newer model, "The knowledge cutoff date for Gemini 3.7 Flash
is March 2026 — users can expect updated information for some domains while in others
they may experience the model's knowledge is limited to January 2025 (in line with the
Gemini 3 Model Family)."

## Override 4 — open the render, and describe the crop before scoring it

**Lands on:** step 6, after the gate.

`SKILL.md:193-197` already asks for one capture per surface × state × appearance, all
opened, with the fraction reported. **[measured-family]** the run made 3 render calls and
opened 4 images for 5 surfaces × 2 platforms, then scored all five PASS.

**[docs]** Google gives a method rather than a caution: "Ask the model to describe the
images before performing the task in the prompt." Their worked example is the whole
argument — "Describe this image." of an airport board returns a one-line caption, while
naming the extraction returns the thirteen rows. Two corollaries they state directly:
"To improve the response, point out which parts of the image are most relevant to the
prompt", and, when a verdict looks wrong, a disambiguation step separating "the model
did not understand the image at all" from "it did not perform the correct reasoning
steps afterward".

Per capture, in order: name the chrome height, control heights, casing, radii, focus ring
and the copy you can **see** — then score. `SKILL.md:306-308` is the case where this
pays: a native radio or checkbox photographs as nothing in this house's browser, and a
described crop calls that a rendering fact rather than a missing affordance.

## Override 5 — prove the gate can fail before you trust it passing

**Lands on:** step 6, and `scripts/gate_tests.sh`.

Run the adversarial suite, not only the gate, and paste both:

```
bash scripts/gate_tests.sh                 # 19 mocks, each built to defeat one check
python3 scripts/mock_check.py ledgerline-accounts.html; echo "exit $?"
gate  exit 0  examined=76 failures=0 unresolved=0 contexts=4
```

**[derived]** A green gate and an inert gate are the same output. The signature of an inert
one is uniform numbers across varied inputs — identical `examined=` counts on mocks that
differ — so read the counters against each other, not only against zero. `examined=0` exits
2 by design; record it as unperformed, and never pipe the gate through `grep`, which
replaces its exit code with grep's.

**[docs]** Where the delivery needs arithmetic — contrast ratios, cell fractions — do it
in code: Google's note is that code execution "should be enabled whenever the model needs
to perform any kind of arithmetic, counting, or calculation."

## Override 6 — what the spec may claim, and what it may not

**Lands on:** step 5's placeholder rule and step 7's delivery.

`SKILL.md:171` already says a fact you do not have goes in as `[ACCOUNT NAME]`, visible.
Extend the same discipline to the spec's own prose. **[docs]** Google's strictly grounded
system instruction ends on the clause that matters here: "If the exact answer is not
explicitly written in the context, you must state that the information is not available."

So: a token value comes from the kit, the corpus or the direction, with its tier; a
contrast ratio comes from the gate's output; a native-tells score is a list of documented
expectations presented as that, never as perception research (`SKILL.md:309-311`). The
**what you did not check** section is never empty — `SKILL.md:283-284` names motion and
type fidelity as unverifiable here, so those two lines are its floor, not its ceiling.

## Override 7 — the direction fork is a closed set, and delegation is capped

**Lands on:** step 2 (settle the direction) and § When you spawn an agent.

`SKILL.md:258-259` already caps the agent budget and names what an agent may not do — no
git, no directories beyond its own, no subagents of its own. Keep it verbatim in the brief,
and add one rule: never delegate a check of your own output.

**[docs]** For the direction fork, Google's iteration guidance is to reframe as multiple
choice when a model answers correctly but "didn't stay within the bounds of the options".
`SKILL.md:106-107` already requires option identity to stay stable once named. Present
2–3 directions as A/B/C with one paragraph and one trade-off each, take the user's
letter, and write the chosen letter and its name into the spec before building — a
direction re-litigated mid-build is the same failure as a renamed option.

## Modules considered and not written

`injection` and `emphasis` did not fire on the scan, and both are covered above under what
transfers intact. `count-contract` did not fire either: this skill promises tier tags and
audit rows, not a count — which is why Override 1 has to create one rather than extend one.
