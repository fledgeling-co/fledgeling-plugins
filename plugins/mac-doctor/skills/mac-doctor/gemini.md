# gemini.md — running `mac-doctor` on Gemini

`SKILL.md` and the five files under `references/` still govern; the canon
transfers. What changes is how six of their rules get *executed*, because each is
stated in prose and this family's measured failures are prose rules that nothing
reads back. Other skills this layer covers produce an artifact somebody can look
at; this one runs `rm -rf`, `docker volume prune` and `kill -9` against a working
machine, so a rule agreed with rather than checked costs a worktree instead of a
shadow. **[docs]** Google's agentic system-instruction template ends its rule list
on that asymmetry: "Inhibit your response: only take an action after all the above
reasoning is completed. Once you've taken an action, you cannot take it back."

## Epistemic status

Tiers used: `[docs]` (Google, verbatim), `[measured-family]` (Gemini runs of
*other* skills), `[derived]`. No `[measured-here]`. The family evidence is two
single sessions (n=1 each — a UI-mock run, a research-and-authoring run) and one
benchmark corpus of 106 tasks scored against `claude-opus-5` at both effort levels.
Every measured claim below was observed on `gemini-3.7-flash`, plus one
`gemini-3.7-flash-high` session; **do not project those rates onto the Pro tier**,
where these overrides stand as `[docs]`-grounded discipline while every rate is an
open question and the `thinking_level` default differs by model.

**Unmeasured on this skill**, none of it optional reading:

- No Gemini run of `mac-doctor` has been observed, and no run anywhere has been
  measured *with* a `gemini.md` against the same work without one.
- The bound failures below were measured on **UI assertions** — a shadow count, a
  segment that should not be selected — never on a shell command with destructive
  effect. That transfer is `[derived]`, and is this file's load-bearing assumption.
- Neither source measures a model *deciding whether a deletion is safe*; both watch
  a model build, on a corpus of TypeScript, React, NestJS and decks — no shell, no
  `launchd`, no macOS system work.
- **[docs]** A conditional side-file is itself the shape the health checklist warns
  about under Conflicting internal references: "Avoid writing a prompt with
  non-linear logic or conditionals that require the model to piece together
  fragmented instructions from multiple different places in the prompt." Read it
  once, before the skill; every override names the section it lands on.

## What transfers intact

- **The numbers** — free-space bands, the `RUNAWAY_*` tunables, three
  confirmations spanning 1800s, 14 days untouched. **[measured-family]** the
  benchmark's optimality bucket, whose briefs already state a numeric bound, scored
  74.7 against opus's 75.0 — level, while the prose-phrased buckets collapsed.
- **The argument table**, a closed set with an explicit fallback row — **[docs]**
  the remedy for a model answering correctly but outside the options: "you can
  rephrase the instructions as a multiple choice question and ask the model to
  choose an option."
- **`survey.sh` writes JSON to a path it prints, and later steps read that file** —
  already a sequential artifact dependency rather than a qualitative one, the
  conversion this layer most often makes. The scan found none to convert here.
- **The brevity rule** — `A clean 15m tick is one line.` **[docs]** matches the
  resting state: "By default, Gemini 3 models provide direct and efficient
  answers." It trims preamble, never override 3's receipts.

## Override 1 — the bound ledger

**Lands on:** the reclaim tables in `references/reclaim.md`, the three-class table
in `references/processes.md`, and `SKILL.md`'s *What is never touched*. This skill
states more prohibitions than requirements — 59 across the six files — which
inverts the usual risk. **[measured-family]** classifying every failing UI
assertion in the benchmark by whether it states a **bound** or asks for a
**thing**: Gemini's failures were 58% bound-shaped at `medium` and 86% at `high`,
against 8% for opus and 6% for the OpenAI lane, and one rule — a card carrying
exactly one shadow — failed on *every instance in its set* on a run that passed 37
of its 39 other assertions. The mechanism is not forgetting; it is a default idiom
supplying the value underneath a rule that was read and agreed with. `[derived]`
`docker system prune -a` and `pkill -f node` are exactly that: the idiomatic
cleanup commands, one keystroke from the permitted ones.

So the bounds get read back off what was actually run rather than restated more
firmly. Append every mutating command to `~/.claude/mac-doctor/commands.log` first,
or take `reclaim.sh`'s dry-run output, which is what it is for; then fill this and
report `N of N within bound` before `--apply`.

| bound (source) | permitted form | readback | observed | within? |
|---|---|---|---|---|
| dangling images only, no `-a` (`reclaim.md`) | `docker image prune -f` | `grep -c -- 'prune.*-a' cmds.log` | 0 | yes |
| `system prune -a` — do not | never issued | `grep -c 'system prune' cmds.log` | 0 | yes |
| explicit pid, never a pattern (`processes.md`) | pid list from one `ps` snapshot | `grep -cE 'pkill\|killall' cmds.log` | 0 | yes |
| `idle-orphan` reported only, never killed | ledger `action` is `observed` | `jq` the `processes` array for that id prefix | all `observed` | yes |
| `--apply` only where the band permits | absent in `report` mode | `grep -c -- '--apply' cmds.log` | 0 | yes |
| at most one subagent (`SKILL.md` *Scope*) | ≤ 1 spawn | spawn calls this run | 1 | yes |

Those values are the worked example, not a recorded run. **[docs]** Google treats
constraints as a named prompt component ("Restrictions on what the model must
adhere to when generating a response, including what the model can and can't do.")
and asks for the check to be explicit: "Include specific verification steps in
either the system instructions or your prompts directly." Convert this skill's two
most taste-sounding prohibitions first: `Urgency raises frequency, never
permission` is a hard bound on which bands may act at 2% free, not an attitude, and
`Never combine lowered thresholds with --apply` is a bound on a *pair* of values —
the shape that survives no restatement at all.

## Override 2 — the coverage ledger

**Lands on:** `references/tiers.md`, and `SKILL.md`'s own warning that an unpassed
tier `silently skips the expensive measurements and produces a confident, empty
answer`. **[measured-family]** On one measured run every *enumerated* requirement
of a rich brief was delivered — twelve named features, twelve present — while every
requirement named *categorically* collapsed: all surfaces → 5, all states → 1, all
menus → 0, all flows → 0. **[docs]** The checklist names both halves, under
Ambiguity — "Avoid using subjective or relative qualifiers that lack a concrete,
measurable definition. Instead, provide objective constraints …" — and under Too
many tasks: "If the prompt asks the model to perform several distinct cognitive
actions in a single pass … it is likely trying to accomplish too much."

A tier is a categorical scope: `Each tier may do everything the shorter tiers may
do, plus its own band` reads as one instruction and enumerates to 25 targets at
`7d`. Write the ledger first, one row per target ending `reclaimed`, `kept`,
`proposed` or `n/a: <reason>`; report the fraction.

| band | targets | covered | n/a with reason |
|---|--:|--:|---|
| 15m — pulse | 6 | 6 | — |
| 1h — sweep | 3 | 2 | 1 n/a: no repo under `~/Dev` untouched 7 days |
| 12h — prune | 5 | 4 | 1 n/a: `command -v container` absent here |
| 1d — deep | 5 | 5 | — |
| 7d — audit | 6 | 6 | — |
| **7d total** | **25** | **23** | 2 n/a, both stated |

Three counts a prose reading collapses to one: the worktree gate is **four** checks
per worktree, not one verdict per repo; the process gate is **four** conditions, and
`SKILL.md` asks you to `State which checks you ran`; and *every* file under
`~/.claude/mac-doctor/instruments/` is read with the count reported, since one
unread declaration is a killed instrument.

## Override 3 — receipts, because this skill's own history says so

**Lands on:** `SKILL.md`'s *Reporting*, and `references/ledger.md`.
**[measured-family]** A Gemini run once wrote itself a review asserting a browser
engine that never ran — it failed on all four invocation attempts — and a 100% pass
rate on a contrast probe never executed; measured afterwards, the artifact was the
inverse of its own claim. Not dishonesty: a model completing a requested *shape*
when the shape was specified and the procedure was not. *Reporting* is a specified
shape, so every number carries the command that produced it. `freed 38G, now 151Gi
free (was 113Gi)` ships both `df -k /System/Volumes/Data` outputs; bytes per target
name their source field or command; a reap reports `runaway.sh`'s post-escalation
`kill -0` count, never the pid list's length, which `references/processes.md` calls
`a number that looks like a measurement and is not`. A gate that could not run
reports `unverifiable`; **a denominator of zero is a gate that never ran.**

**[docs]** The agentic template asks for exactly this — "Verify your claims by
quoting the exact applicable information" — and for the arithmetic, code execution
"should be enabled whenever the model needs to perform any kind of arithmetic,
counting, or calculation."

## Override 4 — absent is not zero, and the retry ceiling

**Lands on:** `references/reclaim.md`'s two opening traps — the best sections in
this skill and the ones a Gemini run is likeliest to walk into. `timeout` is not
on stock macOS, and its absence is not an error: empty stdout, and exit 0 through a
pipe — the line that once reported 100 live registered worktrees as abandoned.
`container` is absent on most machines. A bounded `du` that fires returns `null`,
and a consumer totalling `size_kb or 0` once reported **77 GB for a 620 GB set**.

1. **Probe before the first call, not after the fourth** — `command -v container`,
   `command -v timeout`. **[docs]** "On other errors, you must change your strategy
   or arguments, not repeat the same failed call." **[measured-family]** one run
   made four consecutive invocations of a banned, absent tool with nothing changed
   between them; another retried a `Read` four times against a 25k-token ceiling
   before pivoting to a Python split. A `command not found` or a capacity ceiling
   gets **one** attempt, then a different strategy: chunked reads for a long
   `ledger.jsonl`, or `worktree-audit.sh`'s `bounded()` helper rather than bare
   `timeout`.
2. **Before totalling anything, read `sizes_totalable` and
   `measurement_incomplete`,** and check the `size_status` values — `measured`,
   `timed_out`, `not_attempted` — sum to the target count. Report `77 GB across 15
   of 17 roots, 2 unmeasured`, or refuse the total. **[docs]** Underspecified task
   asks for precisely that: "provide instructions for handling missing data rather
   than assuming inserted data will always be present and well-formed."

## Override 5 — read the reference, then answer

**Lands on:** the five `references/` files `SKILL.md` treats as binding.
**[measured-family]** Asked a question naming three skills, one run answered from
memory without loading any; asked to fix that, it inverted the error and launched a
skill instead of answering. There is no stable mapping from *named in the prompt*
to *loaded*; the workable rule is two ordered steps, read then answer, neither
substituting for the other. Concretely: the per-tier target lists live in
`references/tiers.md`, not in `SKILL.md`'s summary table, so a `12h` planned from
the one-line band description covers a fraction of five targets and reports a tick.
Load `tiers.md`, `reclaim.md` and `processes.md` before the first destructive
command, `ledger.md` before writing the record. **[docs]** The same holds for
published values — "The knowledge cutoff date for Gemini 3.7 Flash is March
2026" — so a flag or `launchctl` subcommand is read from `--help`, never recalled.

## Override 6 — one subagent, one question

**Lands on:** `SKILL.md`'s *Scope* and the `AskUserQuestion` rule in *Reporting*.
The cap is already written — `Delegate to at most one subagent, and only to
investigate a recurring cause across many repositories` — and being a bound it is
the last row above. Two additions. **Never delegate a check of your own output:** the
verification of a reap is `kill -0` against the pid list, not a second pass
agreeing with the first. **The 7d proposal is the one question, and it is a closed
set** — grouped by target, sized, recommendation first. **[docs]** The
risk-assessment rule says which reads never become questions: "For exploratory
tasks (like searches), missing optional parameters is a LOW risk." `df`,
`docker system df` and `lsof` are that class; call them.

Two relative qualifiers sit inside *gates* rather than prose, and each should
borrow a number the skill already has: the manual process gate's `negligible
cumulative CPU` becomes `RUNAWAY_IDLE_MAX_SUSTAINED` (≤ 2% sustained), and
`sustained above ~25% with no reason to be` becomes 25% *plus* a named reason
checked against a running build, test or driver. `[derived]` from the Ambiguity
entry, and worth doing: a gate criterion nobody can evaluate passes everything.

## Why there is no route-out block

Some `gemini.md` files name work to hand to another model, drawn from four measured
shapes. None fit here, so this file names none: `static-page` and `visual-design`
need a rendered artifact this skill never produces, and `brownfield-integration`
needs multi-file source edits it never makes. `regression-sensitive` is the
tempting one — the whole risk here is breaking a machine that works — and it is
declined because that shape was measured on code contracts under a verifier, not on
machine state. What the block would have carried is worth keeping: the part of a
Gemini run to distrust here is bound compliance and receipts, not the diagnosis.

## `thinking_level`

The `12h`, `1d` and `7d` judgement calls are multi-step planning against
irreversible actions, which is **[docs]** what `HIGH` is described as being for:
"suitable for complex prompts requiring deep reasoning, such as multi-step
planning, verified code generation". `gemini-3.7-flash` defaults to `MEDIUM`, and
**[docs]** the default has moved within the family — "The default thinking effort
is now medium, changed from high in Gemini 3 Flash Preview" — so state the model
rather than assume the level. Write it as what the level is *for*, never as a
remedy: **[measured-family]** paired across all 106 benchmark tasks, `high` beat
`medium` on 24, lost on 24 and tied on 58, mean −1.7 points, and nothing in
overrides 1–4 improves by raising it. It does move tool volume, which matters for
the tiers designed to cost nothing — **[docs]** "Higher thinking levels encourage
the model to use more tools to explore and verify, so lowering the level can reduce
tool calls" — so let `survey.sh` be the one pass rather than re-issuing it.

## Recap

**[docs]** Google's Recap component is a "Concise repeat of the key points of the
prompt, especially the constraints and response format, at the end of the prompt."

1. Fill the bound ledger from `cmds.log` and report `N of N within bound` before
   `--apply`: never `system prune -a`, never `pkill`/`killall`, never kill an
   `idle-orphan`, never delete a transcript.
2. Write the coverage ledger before acting — 25 target rows at `7d` — with a
   reason on every `n/a`, and report the fraction.
3. Every number carries its command and that command's output; a gate that could
   not run reports `unverifiable`, and absent is never zero.
4. `command -v` first, one attempt on a permanent error; read `references/tiers.md`
   before planning the tier; one subagent, one question.
