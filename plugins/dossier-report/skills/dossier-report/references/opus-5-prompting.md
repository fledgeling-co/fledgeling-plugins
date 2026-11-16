# Writing prompts for Opus 5 and Opus 5.5 runners

Use this guide for an Opus 5 runner. The pipeline does not require every stage to use Opus: preserve the user's selected orchestration, planning and implementation lanes. An Opus planning stage may hand a complete brief to Gemini 3.8, coordinated by GPT-6; resolve their actual IDs and controls from the current harness.

For an Opus 5 prompt revision, consult these sources once per review, or reuse a current copy already read in this session:

- <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md>
- <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md>
- <https://platform.claude.com/docs/en/about-claude/models/migration-guide.md>

They change between model releases, and a pattern that was right for a prior
Opus can be actively wrong now. The patterns below are what those documents say,
plus the failures this marketplace has actually measured against them.

## The patterns that change what comes back

**Structure the brief with XML tags: longform state first, the task last.**
Context, fixture, current numbers and prior learnings up top; the ask at the
end. Queries placed after long context measurably outperform the reverse, by up
to 30% on complex multi-document inputs.

**Remove verification scaffolding.** Opus 5 verifies its own work. "Double
check", "re-verify before reporting", "use a subagent to confirm" compound with
that behaviour and cause over-verification, spending tokens for no gain. The
migration guide is explicit that these should be *removed* rather than
rewritten. Measured here: an agent given a four-round cap ran seven, and the
extra rounds were self-correction the model would have done anyway.

Instrument runs are not self-checks. A scorer, a gate, a polarity measurement
is what the round is *made of*; keep those.

**Cap delegation explicitly.** Opus 5 delegates more readily than prior models.
If a task is a single track, say so: "do not delegate to subagents; spawn none."
Otherwise name which scenarios warrant it.

**Constrain scope in the brief's own words.** State what is in and out of scope,
then: deliver what was asked at the scope intended, make routine judgment calls
yourself, and if the brief looks mistaken say so in a sentence and carry on
rather than quietly narrowing, widening or transforming it.

**Give vision work its tools.** Vision performance is strongest when the model
can crop, zoom and re-render rather than reason about what an image probably
looks like, and tool use is a more cost-effective lever than thinking alone.
Point the brief at the artifacts and ask for values sampled out of them. This is
not "check your work"; it is where the evidence comes from.

**Calibrate deliverable length explicitly.** Both visible responses and files
written to disk run longer on Opus 5 than on prior models, and lowering effort
reduces thinking without reliably shortening output. Ask for the substance
without padding, and give the final report a rough word budget.

**Calm trigger language.** "Use X when…" outperforms "CRITICAL: you MUST…",
which overtriggers on current models. If a rule matters, explain why it matters;
the model generalises from the reason.

**Name the gaming risk when a proxy is involved.** Any loop with a score invites
tuning constants against the score. Say plainly that the artifact should be made
right and the number allowed to follow, and that the score is a proxy for a
human judgment.

**Correction narration.** Opus 5 narrates corrections to its earlier statements
more than prior models. If that is noise in your context, say: correct an
earlier statement only when the error changes the reader's decisions; otherwise
fix it and move on.

## Effort and thinking

Effort defaults to `high`. `low` and `medium` are the primary cost and latency
controls and hold quality on mechanical or read-only passes; `xhigh` suits
demanding agentic and coding work. Use only effort values the selected runtime model supports; do not carry a previous model's `max` setting over by name. Run a fresh sweep on your own evals rather than
carrying a setting over from an earlier model — the levels were recalibrated.

When using the Messages API, choose an output-token budget that fits the task and the selected model's documented limits. A CLI may not expose `max_tokens`; do not invent a flag or force a fixed 64k budget for every runner.

Thinking is on by default and can only be disabled at effort `high` or below;
`disabled` plus an unsupported higher-effort setting is invalid. Prefer lower effort with thinking
on over disabling it: with thinking off, the model occasionally emits tool calls
as plain text or leaks internal XML tags into visible output.

## Opus 5.5 runners

Everything above still applies to Opus 5.5 (`claude-opus-5-5`). These are the
differences, from [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5.md)
and its linked pages, reviewed 2026-11-16.

**Effort.** The default is `medium`, not `high`, and the level names do not carry
across: in Anthropic's testing 5.5 at `medium` matches or beats Opus 5 at `high`
on coding and knowledge work, and `low` comes close on several coding evals. Set
effort explicitly, start at `medium`, and keep `xhigh` and `max` for work where a
quality gain was measured, because 5.5 thinks more per turn at those levels. To
get less thinking, lower effort; a prompt line does it less reliably. A top-level
effort change mid-conversation invalidates the cache.

**Thinking.** It is always on; `thinking: disabled` returns a 400. Size
`max_tokens` for thinking plus the reply and read responses by block type. Drop
lines that tell the model to think carefully or step by step: it decides how much
to think, and such lines only delay the first token.

**No reasoning in the reply.** A brief that asks the runner to write out its
reasoning, verbatim or in a fixed format, can be declined (`reasoning_extraction`).
Ask for a short explanation of the answer or a summary of what it did.

**Unattended runs.** On long multi-part tasks 5.5 reports progress, and some of
those reports end the turn with no tool call. A loop that reads that as "done"
stops early. In the harness: keep the task's parts in a checklist the runner
updates, treat a text-only end of turn as a report, send one short message naming
the open items, wait for any background command or child still running, and stop
after two or three automatic continuations so a stuck run ends and gets reviewed.
In the brief, for runs nobody is watching: name the stops you do not want (a
summary that announces the next step without taking it, an offer to continue
unless told otherwise, a list of decisions that block nothing, stopping because
the turn has been long) and the stops you do (nothing can move without the user,
or the blocker is deliberately protected). Status notes go in the same message as
the next tool call. Keep confirmation for risky or destructive actions, and leave
this out when a person is there to answer.

**Progress updates.** Ask for the cadence you want in the brief (one line of
intent before the first tool call, a short recap at the end). The runner follows
it.

**Look before acting across apps.** When the task spans mail, documents, sheets
or records and is loosely specified, tell the runner to list and open the sources
that could be relevant, including ones the task does not name, before it changes
anything. Keep untrusted content out of what it searches, since it will act on
what it finds.

**Time signals for agent teams.** 5.5 paces itself to elapsed time. Where the
harness can, end each message back to the runner with `elapsed 340s / 1200s`, with
the budget set somewhat above the time you want spent. With no sensible budget,
show elapsed time alone and say that time matters. The budget is advisory: keep a
real timeout, and check quality, because under time pressure it verifies a little
less.

**Pasted text.** Wrap text the user copied from elsewhere in
`<pasted_content id="…">` tags with a matching random id on the closing tag, and
tell the runner to follow instructions inside only where the user's own words ask
it to.

**Vision.** 5.5 reads charts, diagrams and screenshots more accurately without
tools, so re-test scaffolding built for earlier models before keeping it.
Higher-resolution images and a crop tool still add accuracy on the densest inputs.

**Frontend defaults.** Without design direction 5.5 falls back on a few default
styles, and "avoid a generic AI look" swaps one default for another. Name the
specific patterns to avoid (a cream ground, italic accent words, numbered
"01/02/03" labels, monospace labels, pill buttons), look at what came back, and
extend the list.

## Environment traps when spawning via `claude -p`

Measured in this marketplace, and each one cost a debugging cycle:

- **Pass the brief's path, not its text.** ~7KB as the `-p` argument fails in 13
  seconds with "Prompt is too long", deterministically, while the same bytes
  plus a one-line suffix succeed. Write it to disk and say to read it.
- **Give the child a clean context.** Configured MCP servers load their tool
  definitions into every child; on a machine with 13 of them the agent starts
  near its limit. Use `--strict-mcp-config` and strip session-scoped
  environment variables. Measured: 88s inherited versus 14s clean on one task.
- **Whitelist tools rather than asking for restraint.** `--allowedTools` with no
  git and no network enforces "subagents never run git" structurally.
- **Killing the parent does not kill the child.** A superseded agent kept
  editing files and collided with its replacement. Run it in its own process
  group and kill the group.
