# Model calibration — running this skill on a non-Anthropic family

Read this in **one pass before Mode detection**, then follow SKILL.md with the overrides below. Do not consult it mid-build: a conditional side-file is exactly the "conflicting internal references" defect Google's own prompt-health checklist names — instructions the model must *piece together from multiple different places* — so reading it in fragments recreates the problem it exists to fix. Each override names the section it lands on.

**What this file is not.** The enforcement material that used to live here is gone from here on purpose. The state grid as a counted artifact, the destructive-action gate table, and the rule that you do not write a review section for a probe you did not run were all quarantined behind a model check in the predecessor version, and none of the three is family-specific: the failure each one fixes is that a categorical enumeration with no count in it ships as one item. They are now in SKILL.md for every family, which is where a generation fix belongs. What is left here is genuinely about one family's behaviour.

**Which families this covers.** Google's Gemini, with recorded evidence. Every other non-Anthropic family is **uncalibrated** — the canon transfers, and nothing here has been measured on it. Say so rather than assuming the Gemini overrides apply.

## Provenance

**`[measured]`** items come from one recorded Gemini run (`Egress Gemini`, 2026-08-17) that invoked this skill plus `design-craft` on a rich brief for a two-platform CI-runner app, producing `~/Dev/egress/design/mocks/html/index.html`; a run on a near-identical brief produced `interaction-mock.html` beside it, and both were probed with the same scripts. **n=1** — one honest data point, not a law.

**`[docs]`** items come from Google's published Gemini 3 prompting guidance **and are the stronger evidence.** That ordering is deliberate and worth stating: a single observed run is the weaker tier here, however specific its numbers, and a reader who does not know which tier is stronger will weight the vivid one.

## What did not transfer: a rule in prose is not a rule executed

The canon in this skill transfers to Gemini unchanged. What does not transfer is the assumption that a rule stated in prose gets executed. On this family a rule needs a cell to fill and a number to report.

**`[measured]`** Given Build mode's six named states and the sentence *"the mock is incomplete until all six exist"*, the run delivered **one** state — the populated one — across all five surfaces. Zero loading, zero empty, zero partial, zero error, zero done. No `data-state`, no state attribute of any kind, and a 48-line script with three functions, none of which changes a state. A comparison run on the same brief built 5 states × 10 surfaces × 2 platforms and verified that no two states of a surface render the same set of blocks.

So the enumeration was present and was still improvised away. **`[docs]`** Google's prompt-health checklist explains why, under **Ambiguity**: *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition. Instead, provide objective constraints (for example, 'write a summary of 3 sentences or less' instead of 'write a brief summary')."* "Incomplete until all six exist" is a completeness condition with no count in it — a relative qualifier. `10 surfaces × 6 states = 60 cells` is an objective constraint. The verbosity default compounds it: these models *"provide direct and efficient answers"* unless a fuller response is explicitly requested, so a list inside a paragraph of guidance reads as context rather than as a manifest.

**The override, on top of SKILL.md's counted grid:** apply the same conversion to *every* remaining enumeration in this skill — the twelve non-negotiables, the four walkthrough questions per step, each checklist. Each becomes a row with a verdict, not a paragraph you have read. Where SKILL.md asks for a count, report it; where it does not, add one.

## One pass is the wrong container

**`[docs]`** The same checklist warns against **Too many tasks** — *"several distinct cognitive actions in a single pass … Break the requests into separate prompts"* — with chaining as the remedy. So build the screens, then run a **states pass** across all of them, then a **flows pass**. Six states authored while you are still deciding what the screen is will lose to the screen every time.

**`[docs]`** And Google's strongest stated lever is few-shot: *"We recommend to always include few-shot examples … you can remove instructions from your prompt if your examples are clear enough in showing the task at hand"*, and on output structure, *"show the output structure in your few-shot examples"*. This is the mechanism behind SKILL.md's fill-one-row-first rule, and on this family it is load-bearing rather than advisory: author one surface's states at full fidelity and treat that row as the exemplar. A grid filled from a prose rule drifts by row four; a grid filled from a worked first row does not.

**`[docs]`** If you control `thinking_level`, flow and state work is what Google describes `HIGH` as being for (*"multi-step planning"*). Gemini 3.7 Flash defaults to `MEDIUM`.

## Underspecified edge cases are where this family stops

**`[measured]`** With one state built, the consequences followed mechanically — no error state existed, so the error-message rule had nothing to grade; the pairing surface showed a 6-digit code and a key fingerprint with nothing to compare either against, no expiry, and no interface at all for the receiving side, its primary button reading **"Simulate Pairing Complete"**; and the accessibility floor came back `aria-*` 0, `role=` 0, `tabindex` 0, `prefers-reduced-motion` 0, with 12 `<div onclick>` carrying the entire navigation of both apps, every nav item keyboard-dead on both platforms.

**`[docs]`** Google's checklist names the shape of this whole class — **Underspecified task**: *"Ensure that the prompt's instructions provide a clear path for handling edge cases and unexpected inputs, and provide instructions for handling missing data rather than assuming inserted data will always be present and well-formed."* It is written about prompts and it describes exactly a mock built on the assumption that its data always arrives present and well-formed. The unhappy paths *are* the edge-case path, and they are the part that has to be specified rather than inferred.

**The override:** run `scripts/ux-lint.py --static` on your own artifact before delivery and treat its counts as the finding, not as information. On this family, do it even when the surface feels finished — the run above felt finished.

And never ship a control whose label describes the mock rather than the product. "Simulate Pairing Complete" is the artifact admitting the flow is absent; the honest alternatives are to build the step or to label it as a harness jump, outside the app window.

## Verification is prompted, not automatic

**`[docs]`** Gemini's guidance asks the model to *"Verify your claims by quoting the exact applicable information"* — so verification happens when it is asked for and not otherwise. **`[measured]`** Left unasked, the run shipped a `DESIGN-REVIEW.md` about its own work: five surfaces, five rows, all PASS, one minor issue found and resolved, and a named browser engine that failed on all four attempts and never ran.

The correction is not "review harder". It is SKILL.md's rule — a self-review with no probe output in it should not be written at all — applied here with the family-specific note that on this family the quoting has to be demanded explicitly. When you write the Measured line, quote the command and its output rather than characterising it.

## A screen that mentions a flow is not a flow

**`[measured]`** Build step 3 asks for entry point → steps → completion signal → recovery paths, and *"map every exit"*. The run produced **zero** multi-step flows. Pairing was a single card with `Cancel` and `Simulate Pairing Complete` — no waiting-for-peer step, no code-mismatch branch, no success state, no inbound variant, no expiry — and it was rendered as a *nav destination* with a selected sidebar row, when a live expiring out-of-band code is modal by nature and both target platforms have a modality for it. Rendering a flow as a place removes its boundaries.

**The override:** SKILL.md already requires the numbered step list with its count before any screen. On this family, also capture each step as its own frame and check the two conditions per frame — the step indicator equals the rendered step, and the chrome around a first-run flow reflects the first-run state. Both failed here inside single frames.
