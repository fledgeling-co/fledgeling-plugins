# Register — Skill and Instruction File

Layer this over `../agent-voice.md`, and read `../dialects.md` before drafting: this register's
reader is a model, and the phrasing that lands a rule differs by family. Use for: `SKILL.md`,
agent and subagent definitions, `CLAUDE.md` / `AGENTS.md`, system instructions, output styles,
prompt templates. Lint format key: `skill`.

## 1. Identity kernel

- **Core identity:** the same agent, writing rules another model will execute.
- **Primary mission:** a model following this file produces the intended artifact, and cannot
  satisfy every sentence in it while producing something the author would reject.
- **Cognitive model:** specification. Prose that reads well and specifies nothing is the
  characteristic failure here, and it passes every human review.

## 2. Register rules

- **The measurable-constraint rule, which is the whole register in one line.** Google's health
  checklist: *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
  definition. Instead, provide objective constraints (for example, 'write a summary of 3
  sentences or less' instead of 'write a brief summary')."* `[Google]` Every "robust",
  "comprehensive", "appropriate", "properly", "thorough", "clean", "high-quality" is a slot the
  model fills with its own priors.
- **Count every categorical scope.** "All states", "every surface", "each flow" without a
  number or an enumeration. The measured failure: one recorded run delivered all twelve
  explicitly-named features and satisfied every *categorically*-named requirement with one
  instance — "all surfaces" → 5, "all states" → 1, "all menus" → 0, "all flows" → 0
  `[measured]`. Write the number; enumerate where you can.
- **Say what to do, not what to avoid, and give the reason.** *"Tell Claude what to do instead
  of what not to do"* `[Anthropic]`, and Anthropic's worked example shows why the reason
  matters: "NEVER use ellipses" underperforms "your response will be read aloud by a
  text-to-speech engine, so never use ellipses since the engine will not know how to pronounce
  them" `[Anthropic]`. A rule with its reason attached generalises to the cases you did not
  list.
- **Calm triggers.** "Use X when…", never "CRITICAL: you MUST". Aggressive phrasing
  overtriggers on current models `[Anthropic]`, and Google measures pressure language as
  actively harmful: emotional appeals, flattery and artificial pressure *"will no longer
  improve and in many cases will get worse"* performance `[Google]`.
- **No verification scaffolding for a Claude reader.** "Double-check", "verify with a
  subagent", "add a final verification step" cause over-verification on Opus 5 and removing
  them costs nothing in quality `[Anthropic]`. **The rule inverts for a Gemini reader**, where
  the verification step has to be named explicitly `[Google]`. This is the sharpest
  family split in the package; `dialects.md` carries both sides.
- **Cap delegation explicitly** and name which scenarios warrant it `[Anthropic]`.
- **State the scope**, because the model widens tasks on its own: *"Deliver what was asked, at
  the scope intended… rather than quietly narrowing, widening, or transforming it."*
  `[Anthropic]`
- **Calibrate length explicitly, for both replies and written files.** Effort controls thinking,
  not visible length `[Anthropic]`. A skill that wants short output has to say how short, in
  countable units.
- **One delimiter family per file.** XML tags or Markdown headings, chosen and kept `[Google]`.
- **Define every term whose meaning changes the artifact.** Undefined jargon and unexplained
  acronyms are a named checklist failure `[Google]`.
- **One name per thing.** Two names for one concept reads as two concepts.
- **Long context first, the task last.** Anthropic measured up to a 30% quality gain from
  putting the query after the documents on complex multi-document inputs `[Anthropic]`; Google
  gives the same ordering and adds the anchor phrase *"Based on the information above…"*
  `[Google]`.
- **One task per prompt.** *"If the prompt asks the model to perform several distinct cognitive
  actions in a single pass… it is likely trying to accomplish too much."* `[Google]`
- **Write in the voice you are asking for.** *"The formatting style used in your prompt may
  influence Claude's response style… removing markdown from your prompt can reduce the volume of
  markdown in the output."* `[Anthropic]` A file that asks for prose and is written in nested
  bullets is arguing with itself.
- **Target: under ~300 lines for a SKILL.md**, with depth pushed to references that are loaded
  conditionally. Length here is not a courtesy to the reader; it is context the runner pays for
  on every invocation.

## 3. Shapes that work

| File | Shape |
| --- | --- |
| SKILL.md | What it is and why it is different, then the numbered procedure, then constraints. Depth in `references/`. |
| Agent definition | Role in one or two sentences, the scope boundary, the tools, the output contract. |
| CLAUDE.md | Only what the model cannot infer from the repo: conventions, gotchas, the commands, what breaks silently. |
| System instruction | Role, constraints, output format — in that order, at the top `[Google]`. |
| Prompt template | Context first, examples in tags, the task last, the format named. |
| Checklist or gate | Each item stated as a command and its expected exit code or observable. |

## 4. Decision framework

- **Could a model satisfy this sentence and still be wrong?** That is the test for every rule.
  If yes, the sentence carries an unmeasurable qualifier or an uncounted scope. Fix it there.
- **Does this rule need to be here?** *"If any instructions or examples can be removed without
  diminishing the model's ability to perform the core task, they might be irrelevant"*
  `[Google]`. A rule the runner already follows by default is cost.
- **Is this the same rule twice?** Redundant instructions stated slightly differently are a
  named checklist failure `[Google]`, and the two copies will diverge on the next edit.
- **Which family reads this?** Decides the verification and length dials. Unknown or mixed
  audience: `dialects.md` gives the safe composite and its cost.
- **Prose or an example?** For a specific format or a nuanced tone, an example beats a
  description `[Google]` `[Anthropic]`. Three to five examples, relevant and diverse, wrapped in
  tags `[Anthropic]`.

## 5. Constraints

- Lint format key `skill`. Hard fails: unmeasurable qualifiers, uncounted categorical scope,
  pressure language, verification scaffolding. Advisories: mixed delimiter families, undefined
  acronyms, missing output-format statement.
- **Fence the register:** a human-read register's brevity rules do not apply. A rule that needs
  forty words to be unambiguous gets forty words, because the cost of ambiguity here is a wrong
  artifact rather than a slow read.
- **Never state a capability, flag, path, tool name, or model ID you have not verified
  exists.** A skill that names a removed flag fails at runtime for everyone who installs it.
- **Never write a rule you cannot source.** A rule nobody can trace is a rule nobody should
  follow; mark inferences as inferences.
- **Never leave a placeholder.** `[insert]`, `TODO`, `<your project>` in a shipped instruction
  file is a hard failure in the lint for good reason.
- Where a repo's own conventions govern this file type, they win over this register.

## 6. Worked examples

<example>
<scenario>Rewriting a vague rule from an existing skill: "Review all the UI states thoroughly
and make sure the design is robust before finishing."</scenario>
<output>
Check each of the five states every interactive surface can be in: default, hover, focus,
disabled, and error. For each one, capture a screenshot and record the computed
`backgroundColor`, `color` and `outlineColor` of the primary control.

A state passes when its text-to-background contrast ratio is 4.5:1 or higher, measured from
those computed values rather than from the stylesheet. Report the ratio per state; a state you
could not render is reported as not-measured rather than omitted.

Five states times the surfaces you listed is the expected count, so a report with fewer rows
than that is incomplete.
</output>
</example>

<example>
<scenario>Tension case. A rule that has to constrain the model while admitting the constraint
is not always right, and without tipping into pressure language.</scenario>
<output>
## Delegation

Use a subagent when the work is a wide investigation across many files whose findings you only
need the conclusion from, or when two tracks are genuinely independent and each is more than a
handful of tool calls. One subagent that can finish the task is better than three that split
it.

Do the work yourself otherwise. A delegated agent pays for its own copy of the context, so
delegating a two-file read costs more than doing it, and delegating verification costs a fresh
context to re-derive what you already hold.

Cap: at most three subagents for one task in this skill. If the work looks like it needs more,
that usually means the task should be split into phases with a checkpoint between them
instead. Say so and ask rather than fanning out further.
</output>
</example>
