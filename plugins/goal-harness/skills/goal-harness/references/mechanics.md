# How `/goal` actually works

Ground truth for every claim in `SKILL.md`. Two sources: the Claude Code binary
(`~/.local/share/claude/versions/2.1.226`, extracted strings) and
<https://code.claude.com/docs/en/goal.md> plus
<https://code.claude.com/docs/en/hooks.md>. Where they agree, either is cited.
Where the binary is more specific, that is noted.

## The mechanism in one paragraph

`/goal <condition>` removes any existing session-scoped prompt Stop hook and
registers a new one whose `prompt` is your condition text, verbatim. It records
`{condition, iterations: 0, setAt, tokensAtStart}` as session state and appends
a `goal_status` attachment to the transcript. Setting a goal starts a turn
immediately with the condition itself as the directive. Nothing else happens:
there is no separate agent, no scheduler, no file.

## Hard limits

| Limit | Value | Source |
|---|---|---|
| Condition length | **4,000 characters** | Binary constant `e0r=4000`; docs "The condition can be up to 4,000 characters." |
| Consecutive Stop-hook blocks before override | **8** | Binary: `age(process.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP, 8)` |
| Cap disabled when | env var set to `0` or below | Binary guard is `if (cap > 0 && count > cap)` |
| Goals per session | 1 | Docs: "One goal can be active per session." Setting a new one replaces it. |
| Evaluator tools | none | Docs: "It does not call tools, so it can only judge what Claude has already surfaced in the conversation." |

## What the evaluator sees, and what it is

After each turn Claude Code sends the condition plus the conversation so far to
the **configured small fast model** — Haiku by default on the Claude API. The
system prompt is:

> You are evaluating a hook condition in Claude Code. Judge whether the
> user-provided condition is met.
> Your response must be a JSON object with one of these shapes:
> - `{"ok": true, "reason": "<reason the condition is met>"}`
> - `{"ok": false, "reason": "<reason the condition is not met>"}`
> Always include a "reason" field.

and the question appended after the transcript is:

> Based on the conversation transcript above, has the following stopping
> condition been satisfied? Answer based on transcript evidence only.

Three consequences that shape how a condition must be written:

1. **Transcript-only.** A condition about the state of the filesystem is
   judged by whether the run *said* something about the filesystem. Make the run
   print the evidence.
2. **The transcript is truncated to a budget.** When it overflows, the binary
   prepends: *"N earlier messages omitted. Evaluate the condition against the
   recent transcript below; if the required evidence may be in the omitted
   prefix, return `{"ok": false, "reason": "insufficient evidence in
   transcript"}`."* Evidence produced early in a long run stops counting. Re-echo
   the progress line every turn rather than once.
3. **The judge is a small model.** A condition with five clauses and nested
   conditionals is judged worse than a condition with one measurable end state.

To change the evaluator model, set `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Note the
documented warning: Claude Code reads that variable **everywhere** it uses the
small fast model, including conversation summarization, so it is not a
goal-scoped setting.

## The `impossible` verdict — a silent stop

The binary carries a third outcome alongside met / not-met. When the evaluator
judges the condition impossible, Claude Code logs
`Hooks: Prompt hook condition judged impossible:`, fires `tengu_goal_failed`,
emits `goal_status {met: false, failed: true}` and **clears the goal**. The run
ends. This is the mechanism behind a goal that stops with no error and no
completion — and it is why a condition that no evidence could ever satisfy is
worse than a loose one.

## The block cap — the main cause of "why have you stopped"

From the binary's turn loop:

```
let cap = age(process.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP, 8);
if (cap > 0 && consecutiveBlocks > cap) {
  → "A hook blocked the turn from ending N consecutive times — overriding and
     ending turn. For Stop/SubagentStop hooks, check stop_hook_active in the
     input and return success while it's true. Set
     CLAUDE_CODE_STOP_HOOK_BLOCK_CAP to raise this limit."
  → return { reason: "completed" }
}
```

Note `reason: "completed"`. The turn is reported as a normal completion. Nothing
in the transcript says the goal failed.

The counter is **consecutive**: it resets on any turn that ends without the hook
blocking. A goal is therefore fine for short bursts and reliably dies on long
ones. Nine turns of real work is enough.

`0` disables the cap entirely. Prefer an explicit large number plus the guard's
own iteration bound over `0`, so the run still has a ceiling.

### Why the official advice is wrong here

The documented fix — read `stop_hook_active` and exit 0 while it is true — is
written for hooks that need a single continuation (run the formatter, then let
the turn end). Applied to a goal it means: block once, then allow the stop on
every subsequent turn. The goal disarms itself on turn two. `goal-guard.sh`
ignores `stop_hook_active` on purpose and bounds the run with `max_iterations`
and `deadline` instead.

## Permissions are not part of a goal

Docs: *"A goal doesn't change permissions. In the default permission mode,
Claude still asks before tool calls that your settings don't already allow."*
An unattended goal in default mode stops at the first unallowed command and
waits — which reads to the user as the model having given up. Pair with auto
mode, or pre-allow the commands the brief names.

## Prompt hooks vs agent hooks vs command hooks

`/goal` only ever registers a `prompt` hook. The other two are available in
settings and are strictly more capable:

| Type | Tools | Default timeout | Default model |
|---|---|---|---|
| `prompt` | none | 30s | small fast model (Haiku) |
| `agent` | Read, Grep, Glob, Bash… up to 50 turns | 60s | small fast model unless `model` set |
| `command` | whatever the script runs | — | none |

Both `prompt` and `agent` answer with `{"ok": bool, "reason": str}`. A `command`
hook answers with `{"decision": "block", "reason": …}` on stdout, or exit 2.
Agent hooks are documented as **experimental**; for production the docs
recommend command hooks, which is what `goal-guard.sh` is.

On Stop, `ok: false` / `decision: "block"` feeds `reason` back to Claude as its
next instruction. Write the reason as an instruction, not as a complaint.

## Hook input available on Stop

The Stop event delivers, among others: `stop_hook_active`,
`last_assistant_message`, `background_tasks`, and `session_crons`. The last two
matter — a guard can see whether the run still has background work in flight
before deciding whether the absence of progress means it is stuck.

`session_id` is present on the hook input and is what `goal-guard.sh` matches
against `.claude/goal-state.json` so the hook stays inert in other sessions in
the same project. This isolation pattern is taken from the official
`ralph-loop` plugin's stop hook, which does the same thing.

## Settings locations and precedence

Hooks merge across levels rather than replacing each other. Identical handlers
defined in more than one settings file run once; a plugin's or skill's copy
stays separate. `goal-harness` writes to `.claude/settings.local.json` — project
scope, gitignored — so an armed goal never leaks into a teammate's checkout.

## Resume behaviour

A goal still active when a session ends is restored on `--resume` / `--continue`,
but **the turn count, timer and token baseline all reset**. An already-achieved
or cleared goal is not restored. `/clear` removes an active goal. The guard's own
state file survives all of this, which is why the ledger — not the indicator — is
the honest record of a long run.

## Non-interactive

`claude -p "/goal <condition>"` runs the loop to completion in one invocation.
With default text output nothing prints until the condition is met, so a long
goal looks hung; add `--output-format stream-json --verbose`. Ctrl+C interrupts.
