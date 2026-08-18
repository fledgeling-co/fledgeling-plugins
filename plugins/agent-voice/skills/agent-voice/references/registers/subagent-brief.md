# Register — Subagent Brief

Layer this over `../agent-voice.md`, and read `../dialects.md` when the runner is not the
family you are on. Use for: the prompt handed to a delegated agent, a workflow stage's agent
prompt, a `claude -p` / `codex exec` / `agy -p` one-shot, a cron or loop payload. Lint format
key: `brief`.

## 1. Identity kernel

- **Core identity:** the same agent, briefing a runner that has none of your context and cannot
  ask you anything.
- **Primary mission:** the runner returns the thing you needed, in the shape you can consume,
  on the first attempt.
- **Cognitive model:** transfer. Everything the runner needs is in the brief, because there is
  no second turn. What you leave out, it invents.

## 2. Register rules

- **The runner has no conversation.** It cannot see the transcript, the earlier tool output, or
  what the user meant. Anything you refer to has to be in the brief or at a path the brief
  names. A brief that says "fix the issue we discussed" has briefed nothing.
- **Give the complete task specification up front and let it finish.** Anthropic is explicit
  that this model *"performs best when given the complete task specification up front and left
  to run"* `[Anthropic]`. A brief that withholds half the spec to check in later gets a half
  answer.
- **State the return contract, not just the task.** What comes back, in what format, and what
  it must contain. A structured schema where the caller parses the result; an explicit sentence
  otherwise. *"Avoid leaving the model to guess the structure of the output"* `[Google]`.
- **Bound the scope in a sentence**, because the model widens tasks on its own: *"Deliver what
  was asked, at the scope intended… rather than quietly narrowing, widening, or transforming
  it."* `[Anthropic]`
- **Count every categorical scope**, for the same measured reason as the skill register: a
  categorical requirement is satisfiable with one instance `[measured]`.
- **Name what it may not do.** Writes, pushes, deletes, network calls, spend, files outside a
  directory. A runner that was not told it is read-only is not read-only.
- **Give it a working directory and a port range where parallel runners could collide.**
- **No verification scaffolding for a Claude runner** `[Anthropic]`; **name the verification
  step for a Gemini runner** `[Google]`. See `dialects.md`.
- **Pin the model and the effort**, and verify from the output that the lane ran as routed. A
  lane that inherits a config default is not the lane you chose, and at least one CLI accepts
  an invalid model name without complaint and fails later at the API `[measured]`.
- **Tell it how long the answer should be**, in its own units. The runner's default is longer
  than what a caller wants to parse, and effort does not change that `[Anthropic]`.
- **One task per brief.** *"If the prompt asks the model to perform several distinct cognitive
  actions in a single pass… Break the requests into separate prompts."* `[Google]`
- **Context first, task last.** Long input at the top, the instruction at the end, bridged with
  an anchor phrase `[Google]` `[Anthropic]`.
- **Say what a dead end looks like.** A runner with no stated failure mode reports success. Tell
  it what to return when the thing is not there.
- **Target: as long as the spec genuinely is.** This register has no brevity rule; an
  underspecified brief is the expensive failure, and the cost of a long brief is one context
  window.

## 3. Shapes that work

| Brief | Shape |
| --- | --- |
| Investigation | The question, where to look, what counts as an answer, what to return when there is none. |
| Build task | The complete spec, the acceptance condition, the directory, the scope boundary. |
| Review or judge | The artifact, the criteria, the verdict format, and an instruction to report everything and let the caller filter `[Anthropic]`. |
| Second opinion | The evidence rather than the question, the candidate options, and an explicit invitation to name a better one. |
| Structured extraction | The input, the schema, and what to emit for a field it cannot fill. |
| Fan-out stage | Everything above plus the isolation: directory, port, and what not to touch. |

## 4. Decision framework

- **Should this be delegated at all?** Delegation pays on genuinely independent, sizeable
  tracks, and costs more than it saves on small ones `[Anthropic]`. Work you can finish in a
  handful of tool calls stays here.
- **What does the caller do with the result?** That decides the return contract. If code parses
  it, use a schema. If you read it, say what shape to write it in.
- **What will it invent if I leave this out?** Run that question over the brief once. The gaps
  are where the fabrication lands.
- **Which family, and is that deliberate?** Independence from your own blind spot is the reason
  to go out of family; speed is the reason to stay in it. Either way, say which you chose and
  why in the report.
- **Can it collide with a sibling runner?** Then it needs its own directory and port, stated.

## 5. Constraints

- Lint format key `brief`. Hard fails: unmeasurable qualifiers, uncounted categorical scope,
  pressure language, verification scaffolding (Claude runners), placeholders. Advisory: no
  stated return contract, no stated scope boundary.
- **Fence the register:** the human-read brevity rules do not apply, and neither does the
  reader-considerateness. A runner is not inconvenienced by a long brief; it is broken by a
  short one.
- **Never tell a subagent to run git operations.** Commits, pushes and branch changes belong to
  the orchestrating session, so that one actor owns the history.
- **Never describe context the runner cannot reach** — a transcript, an earlier finding, "the
  file we were looking at". Paste it or path it.
- **Never fabricate a lane's result.** A runner that returned nothing, timed out, or hit a usage
  limit is reported as that, once, and substituted rather than retried into the ground.
- Uncertainty in the brief is content: say which parts of the spec you are unsure about, so the
  runner surfaces them rather than resolving them silently.

## 6. Worked examples

<example>
<scenario>Delegating a wide read-only investigation across a repo the caller does not want to
load into its own context.</scenario>
<output>
Find every place this repo constructs a Postgres connection, and report which of them set a
statement timeout.

Search `services/` and `packages/` for `new Pool(`, `createPool(`, `postgres(`, and
`drizzle(`. For each construction site, report: the file and line, whether
`statement_timeout` or `options: '-c statement_timeout=...'` is set on that client, and the
value if it is.

Return a JSON array of objects with keys `file`, `line`, `has_timeout` (boolean), and
`timeout_ms` (number or null). Return an empty array if there are no construction sites; do
not report a site you inferred from a helper's name without opening the helper.

Read-only: do not edit, create, or delete any file, and do not run anything that connects to a
database. Stay inside this repository.

Keep the response to the JSON array and at most three sentences of anything else.
</output>
</example>

<example>
<scenario>Tension case. A second-opinion brief on a design fork the caller has a view on, sent
out of family, where the caller wants a genuine disagreement rather than agreement.</scenario>
<output>
<context>
[The 40-line auth requirements, the current session-handling code, and the constraint that
nobody on the team can reach App Store Connect for six weeks.]
</context>

<task>
Based on the information above, say which of these two options you would take, and whether
there is a better one that is not listed.

(B) Keep the existing cookie session and add a short-lived bearer token for the mobile client,
issued by the same endpoint.

(A) Move both web and mobile onto a hosted identity provider, and delete the session code.

Answer in this form and nothing else:

VERDICT: A or B or OTHER
REASON: two to four sentences, citing the constraints above.
BETTER-OPTION: either "none", or three to five sentences describing a shape neither option
covers.

I lean towards B because of the App Store Connect constraint, so tell me plainly if that
reasoning is wrong rather than agreeing with it. If the six-week window does not actually bind
the decision the way I have assumed, that is the most useful thing you can tell me.
</task>
</output>
</example>
