# Historical Gemini calibration notes

Read this alongside SKILL.md before Mode detection when routed here. The observations below explain specific failure modes and possible mitigations; they do not establish current model capabilities or override the user's selected lane. Apply the matching mitigation when the task needs it or current evidence reproduces the failure.

**Shared acceptance rules.** The counted state grid, destructive-action gate table and prohibition on reporting unrun probes are in SKILL.md for every family. These historical notes do not require duplicate passes or extra artifacts where the main contract already supplies the evidence.

**Scope of the evidence.** One recorded Gemini run and the documentation available when it was reviewed. This is not a calibration of Gemini 3.8, GPT-6, or an entire model family. None of those models' current performance is established here.

## Provenance

**`[measured]`** items come from one recorded Gemini run (`Egress Gemini`, 2026-08-17) that invoked this skill plus `design-craft:design-craft` on a rich brief for a two-platform CI-runner app, producing `~/Dev/egress/design/mocks/html/index.html`; a run on a near-identical brief produced `interaction-mock.html` beside it, and both were probed with the same scripts. **n=1** — one honest data point, not a law.

**`[docs]`** items preserve excerpts from Google's Gemini 3 prompting guidance consulted for the original review. They are guidance, not measured results for a newer model. Recheck current vendor documentation and the receiving runtime before changing model-specific settings.

## Enumeration coverage in the recorded run

The skill's domain requirements apply across models. The recorded failure shows why an explicit coverage artifact can help; it does not show that a model family cannot follow prose instructions.

**`[measured]`** Given Build mode's six named states and the sentence *"the mock is incomplete until all six exist"*, the run delivered **one** state — the populated one — across all five surfaces. Zero loading, zero empty, zero partial, zero error, zero done. No `data-state`, no state attribute of any kind, and a 48-line script with three functions, none of which changes a state. A comparison run on the same brief built 5 states × 10 surfaces × 2 platforms and verified that no two states of a surface render the same set of blocks.

The run omitted explicitly enumerated states. **`[docs]`** Google's prompt-health checklist offers relevant guidance under **Ambiguity**: *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition. Instead, provide objective constraints (for example, 'write a summary of 3 sentences or less' instead of 'write a brief summary')."* Six named states were already a concrete constraint; the observed omission does not establish its cause. A matrix such as `10 surfaces × 6 states = 60 cells` makes coverage easier to inspect. The quoted preference for *"direct and efficient answers"* does not prove that brevity caused the failure.

**Application:** use SKILL.md's counted grid. Extend the coverage record only when an additional enumeration is part of the task's acceptance criteria or a reproduced omission requires it. Do not turn every prose list into a separate mandatory report.

## Task decomposition and examples

**`[docs]`** The same checklist warns against **Too many tasks** — *"several distinct cognitive actions in a single pass … Break the requests into separate prompts"*. For a complex build, separate screen design, state implementation and flow exercise when doing so makes the work tractable. These are possible work phases, not mandatory repeated reviews of an already accepted artifact.

**`[docs]`** The archived guidance recommends few-shot examples: *"We recommend to always include few-shot examples … you can remove instructions from your prompt if your examples are clear enough in showing the task at hand"*, and on output structure, *"show the output structure in your few-shot examples"*. SKILL.md's fill-one-row-first rule supplies a concrete exemplar. The recorded run does not establish a universal drift threshold or prove that examples eliminate omissions.

**`[docs]`** The original notes associated `HIGH` thinking with *"multi-step planning"* and recorded a Gemini 3.7 Flash default of `MEDIUM`. Treat those as historical settings. Discover the actual runtime's supported controls and choose effort for the current task; do not copy these values into another model's request.

## Missing edge cases in the recorded artifact

**`[measured]`** With one state built, the consequences followed mechanically — no error state existed, so the error-message rule had nothing to grade; the pairing surface showed a 6-digit code and a key fingerprint with nothing to compare either against, no expiry, and no interface at all for the receiving side, its primary button reading **"Simulate Pairing Complete"**; and the accessibility floor came back `aria-*` 0, `role=` 0, `tabindex` 0, `prefers-reduced-motion` 0, with 12 `<div onclick>` carrying the entire navigation of both apps, every nav item keyboard-dead on both platforms.

**`[docs]`** Google's checklist names the shape of this whole class — **Underspecified task**: *"Ensure that the prompt's instructions provide a clear path for handling edge cases and unexpected inputs, and provide instructions for handling missing data rather than assuming inserted data will always be present and well-formed."* It is written about prompts and it describes exactly a mock built on the assumption that its data always arrives present and well-formed. The unhappy paths *are* the edge-case path, and they are the part that has to be specified rather than inferred.

**Application:** run the applicable `scripts/ux-lint.py --static` gate as required by SKILL.md, inspect its findings and resolve actual defects. Its static counts have a bounded scope; they do not establish rendered or behavioural acceptance. This requirement is not model-specific.

And never ship a control whose label describes the mock rather than the product. "Simulate Pairing Complete" is the artifact admitting the flow is absent; the honest alternatives are to build the step or to label it as a harness jump, outside the app window.

## A reported pass needs executed evidence

**`[docs]`** Gemini's guidance asks the model to *"Verify your claims by quoting the exact applicable information"*. This instruction does not establish whether a model verifies spontaneously. **`[measured]`** Left unasked, the run shipped a `DESIGN-REVIEW.md` about its own work: five surfaces, five rows, all PASS, one minor issue found and resolved, and a named browser engine that failed on all four attempts and never ran.

Apply SKILL.md's reporting rule: an unrun or failed probe cannot support a passing verdict. When writing the Measured line, identify the command, observed output and limits. Do not add generic self-check rounds or claim a model-family limitation from this one incident.

## A screen that mentions a flow is not a flow

**`[measured]`** Build step 3 asks for entry point → steps → completion signal → recovery paths, and *"map every exit"*. The run produced **zero** multi-step flows. Pairing was a single card with `Cancel` and `Simulate Pairing Complete` — no waiting-for-peer step, no code-mismatch branch, no success state, no inbound variant, no expiry — and it was rendered as a *nav destination* with a selected sidebar row, when a live expiring out-of-band code is modal by nature and both target platforms have a modality for it. Rendering a flow as a place removes its boundaries.

**Application:** SKILL.md already requires the numbered step list with its count before any screen. When verifying a multi-step flow, capture evidence that exercises its required transitions, including step indicators and first-run chrome where applicable. A static frame cannot prove a transition occurred. Both presentation checks failed in the recorded artifact; that does not establish a family-wide limitation.
