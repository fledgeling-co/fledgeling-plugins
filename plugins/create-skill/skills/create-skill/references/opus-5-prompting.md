# Writing prompts for Opus 5 and Opus 5.5 runners

Read [runner-contract.md](runner-contract.md) for the model-neutral handoff and
completion contract. This file adds guidance for a runner actually using Opus 5 or Opus 5.5;
it does not imply that all agents in this pipeline use Claude.

Sources reviewed 2026-09-07:

- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md)
- [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)
- [Migration guide index](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)
- [Migrating to Claude Opus 5](https://platform.claude.com/docs/en/models/opus-5/migration-guide.md)

Refresh the relevant source when changing model-specific behavior or API settings;
a normal run can use this reviewed guidance without re-fetching every document.

## Prompt shape

Give the complete specification, relevant state and explicit scope. Use descriptive
XML tags or headings to separate instructions, source context and examples; place
the ask after a long source bundle. Explain the reason behind consequential rules.
Use calm, direct wording and concrete output constraints rather than repeated
urgency, emotional pressure or open-ended requests to be more thorough.

Opus 5's built-in self-correction makes generic reminders to double-check or spawn
a verifier costly. Remove that redundant scaffolding. **Keep task acceptance
criteria and the evidence-producing steps that define the deliverable**: instrument
runs, required tests, visual comparison, independent eval grading and mandated
workflow gates. Run the appropriate checks once; repeat them after a relevant fix,
new failure or changed evidence. Do not treat self-verification as evidence that
an unrun gate passed.

Delegate sizeable independent work; keep single-track work local. State ownership,
concurrency and iteration limits in the brief. A cap remains a cap during
self-correction. If the requested scope seems mistaken, explain the consequence
briefly and preserve the user's intent instead of silently changing the work.

Give vision work the actual images and tools to inspect, crop or re-render them.
Ask for observable comparisons and sampled values when useful. Control response and
file length explicitly; effort controls reasoning, not reliable output brevity.
Keep progress updates brief and about material findings or changes of direction.

## Effort and API migration

Choose supported effort settings from the runtime. Opus 5's documented default is
`high`; evaluate `low` or `medium` for bounded work and `xhigh` for demanding
coding or agentic work. Do not declare one effort mandatory across all reviewers
without workload evidence. Recalibrate on representative evals after migration.

The Messages API enables adaptive thinking by default on Opus 5. Disabling it is
supported only at effort `high` or below. Prefer lower effort with thinking on
when cost is the concern. Size `max_tokens` for reasoning plus the useful answer;
do not copy a fixed output budget from an unrelated task. Read response content
by block type, and return assistant thinking blocks unchanged in tool-use loops.
If migrating from older than Opus 4.8, check the matching migration section for
sampling, manual-thinking and assistant-prefill changes. These are API concerns;
do not inject API fields into another provider's CLI or tool schema.

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

## CLI environment lessons, bounded to what was observed

One marketplace environment rejected a roughly 7 KB `-p` argument with "Prompt is
too long", yet accepted nearly identical text. That is a local incident, not an
Opus context limit or a universal CLI threshold. Inspect the actual error,
loaded context and harness. For large briefs, use supported stdin/file input or
an absolute file reference that the child can read; then confirm it read the file.

Only load the MCP servers and context needed for the child. Preserve required
tools and permissions when reducing inherited state; measured timing in one
environment is not a general speed guarantee.

`--allowedTools` grants permission without prompting; it is **not** an exclusive
tool whitelist or a git/network sandbox. Use `--tools` to restrict available
built-in tools and appropriate permission/sandbox controls for real isolation.
A shell can run git or network commands regardless of the tool's friendly name.
See the [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference).

Track each child through the harness's process/session lifecycle. Stop a
superseded child's owned session or process group and observe termination before
starting a replacement writer; killing only its launcher may leave it editing.
