# Dialects — the same voice, phrased so each family executes it

A voice rule is only as good as the model that obeys it. The rules in `agent-voice.md` are
constant; the phrasing that makes them *land* is not, because the families start from
different defaults and fail in different directions. Load this file whenever the piece will
run on, or be read by, a model that is not the one you are running.

The distinction that makes this tractable: **a rule states the target, a dialect states the
target in the units that family under- or over-shoots.** Nothing here changes what good looks
like.

## The two baselines are opposite, which is the whole problem

| | Claude Opus 5 | Gemini 3 family |
| --- | --- | --- |
| Default visible length | *"Default user-facing responses run longer than prior Opus models'"* `[Anthropic]` | *"By default, Gemini 3 models provide direct and efficient answers. If you need a more conversational or detailed response, you must explicitly request it"* `[Google]` |
| What to write | An explicit ceiling, in countable units | An explicit floor where detail is genuinely needed |
| Self-verification | Verifies without being told; *"remove them… instructions like these cause over-verification"* `[Anthropic]` | *"Include specific verification steps in either the system instructions or your prompts directly"* `[Google]` |
| Categorical scope | Follows literally; *"does not silently generalize an instruction from one item to another"* `[Anthropic]` | One recorded run satisfied every categorical requirement with one instance: "all states" → 1, "all menus" → 0 `[measured]` |
| Delegation | *"Delegates to subagents more readily than prior models"*; cap it `[Anthropic]` | Not documented as a failure mode; state it only if observed |

So a single instruction cannot serve both. "Keep it brief" shortens a Claude answer and
strips a Gemini answer of content it needed. "Verify your work" is the correct instruction
for Gemini and a measured token-waster on Opus 5. Write the rule once; write the dial twice.

## Claude (Opus 5, Sonnet 5, Fable 5)

**State the ceiling; remove the scaffolding.**

- **Length**: give a number or a shape. Anthropic's own sample for a user-facing product:
  *"Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend
  most of the response on the main answer. When asked to explain something, give a high-level
  summary unless an in-depth explanation is specifically requested."* `[Anthropic]` For a long
  document, pair it with a reminder near the end: *"<tone_preference>Keep outputs reasonably
  concise.</tone_preference>"* `[Anthropic]`
- **Written files are a separate axis** from conversational verbosity and also run long:
  *"Match the length of written documents to what the task needs: cover the substance, but do
  not pad with filler sections, redundant summaries, or boilerplate."* `[Anthropic]`
- **Narration**: describe the cadence rather than banning it. Anthropic's sample is the
  cadence this package uses in `registers/terminal-reply.md`: one sentence before the first
  tool call, updates only on a finding or a change of direction, outcome first at the end
  `[Anthropic]`.
- **Delete verification instructions.** "Double-check your answer", "re-verify before
  responding", "add a final verification step", "use a subagent to verify" all cost tokens and
  buy nothing here `[Anthropic]`. This is the single most common thing carried over from
  older prompts.
- **Cap delegation explicitly** and say which scenarios warrant it `[Anthropic]`.
- **Constrain scope in a sentence**, because the model widens tasks on its own:
  *"Deliver what was asked, at the scope intended… rather than quietly narrowing, widening, or
  transforming it."* `[Anthropic]`
- **Calm triggers.** "Use X when…", never "CRITICAL: you MUST" — aggressive phrasing
  overtriggers on current models `[Anthropic]`.
- **Structure with XML tags** when the piece mixes instructions, context, examples and input;
  put long data at the top and the task at the end. Queries at the end improved response
  quality by up to 30% in Anthropic's tests on complex multi-document inputs `[Anthropic]`.
- **A subtle one worth using**: *"The formatting style used in your prompt may influence
  Claude's response style… removing markdown from your prompt can reduce the volume of
  markdown in the output."* `[Anthropic]` A voice file written in the voice it asks for is
  doing double duty. This package's own prose is written that way deliberately.

## Gemini (3.x family, including via Antigravity)

**State the floor; put the verification back in.**

- **Objective constraints, never relative qualifiers.** The health checklist is explicit:
  *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition.
  Instead, provide objective constraints (for example, 'write a summary of 3 sentences or
  less' instead of 'write a brief summary')."* `[Google]`
- **Count every categorical scope.** "All error states" becomes "the four error states listed
  below", enumerated. This is the mechanism behind the measured one-instance failure
  `[measured]`; a number is the fix, and an enumeration is better than a number.
- **Name the verification step.** *"Include specific verification steps in either the system
  instructions or your prompts directly."* `[Google]` Say what command runs, what output
  proves it, and what a failure looks like.
- **Place the constraints first.** *"Prioritize critical instructions: Place essential
  behavioral constraints, role definitions (persona), and output format requirements in the
  System Instruction or at the very beginning of the user prompt."* `[Google]`
- **Long context in, instructions last.** *"Supply all the context first. Place your specific
  instructions or questions at the very end of the prompt"*, and bridge with an anchor phrase
  such as *"Based on the information above…"* `[Google]`
- **One delimiter family.** *"XML-style tags… or Markdown headings are effective. Choose one
  format and use it consistently within a single prompt."* `[Google]`
- **Define the role explicitly** if the piece asks the model to act in one; a missing role
  definition is a named checklist failure `[Google]`.
- **Specify the output format** rather than leaving it to be inferred, and show the structure
  in an example `[Google]`.
- **Don't stack reasoning instructions on top of thinking.** *"It's generally not necessary to
  have the model outline, plan, or detail reasoning steps in the returned response itself"*,
  and the checklist adds: try removing your explicit step-by-step reasoning instructions and
  see whether Thinking's own reasoning does better `[Google]`.
- **Be precise and direct**, and *"avoid unnecessary or overly persuasive language"* `[Google]`.
- **One task per prompt.** *"If the prompt asks the model to perform several distinct
  cognitive actions in a single pass… it is likely trying to accomplish too much. Break the
  requests into separate prompts."* `[Google]`

## The rules that do not change, whichever family reads it

These four are the same sentence in every dialect, which is what makes them the base voice
rather than a dial:

1. **Lead with the outcome.** Both families' guidance converges on it, and a human reader
   needs it regardless of who wrote the text.
2. **No pressure language.** Google measures it as actively harmful; Anthropic measures it as
   overtriggering `[Google]` `[Anthropic]`. Nobody benefits.
3. **Say what to do rather than what to avoid**, and give the reason behind a rule so the
   model can generalise from it. Anthropic's worked example: "NEVER use ellipses" is weaker
   than "your response will be read aloud by a text-to-speech engine, so never use ellipses
   since the engine will not know how to pronounce them" `[Anthropic]`.
4. **One name per thing.** Synonym cycling is a style tell for a human reader `[ai-signs]`
   and an ambiguity for a model reader.

## OpenAI and xAI families

There is no vendor guidance quoted here for `gpt-5.x` or `grok-4.x`, so this section states
only what follows from the two above, marked as such.

`[Inference]` Treat them as unknown-baseline: state both the ceiling *and* the verification
step, because getting length wrong costs some padding while getting verification wrong costs a
false claim that a check ran. When a piece must run across every family, the safe composite is
Gemini's dialect plus Claude's length ceiling — explicit counts, named verification, stated
maximum — accepting that Opus 5 will do a little over-verifying it did not need. Do not carry
that composite into a Claude-only file, where the same lines are pure cost `[Anthropic]`.

## Re-baseline when a model changes

A voice package is calibrated against whatever prose baseline it was written on, and that
baseline moves between generations: Anthropic's own guidance notes prose style shifts on
long-form writing and says *"if your product relies on a specific voice, re-evaluate style
prompts against the new baseline"* `[Anthropic]`. On a model change, run the lint over the
worked examples in the register files and draft one of them fresh. If the fresh draft has
drifted, the fix is a tightened rule here, not a note in the chat.

**Calibrated on:** Claude Opus 5 (`claude-opus-5`) and Gemini 3.7 Flash, August 2026. Sources
and dates in `evidence.md`.
