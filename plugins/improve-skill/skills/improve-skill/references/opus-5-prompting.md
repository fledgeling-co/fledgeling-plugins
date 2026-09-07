# Writing prompts for Opus 5 runners

Read [runner-contract.md](runner-contract.md) for the model-neutral handoff and
completion contract. This file adds guidance for a runner actually using Opus 5;
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
