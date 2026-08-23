# `recover-claude-code` on Gemini

`SKILL.md` transfers whole, and most of it needs no help: six numbered sections with
a concrete file passed between them, scripts read-only until told otherwise, and the
one irreversible mistake named twice in bold. What does not transfer is the
assumption that a rule stated in prose gets executed. This skill's rules are almost
all *bounds* — never touch a live session, never `--fork-session`, never edit the
original journal, never fabricate a result — and a bound is the shape a Gemini run
has been measured failing while delivering everything else the brief asked for.

## Epistemic status

**Tiers used:** `[docs]` — Google's published guidance, quoted verbatim ·
`[measured-family]` — Gemini runs of *other* work · `[derived]` — reasoning from
those two. No `[measured-here]` appears below. **Every measured rate here is
flash-tier**: `gemini-3.7-flash` across 106 benchmark tasks at `medium` and `high`,
plus two single sessions (`Egress Gemini`, n=1; `COD Dossier`, n=1, on
`gemini-3.7-flash-high`). Do not project it onto the Pro tier — there the overrides
stand as `[docs]`-grounded discipline and every `[measured-family]` number becomes
an open question.

**Unmeasured on this skill:** no Gemini run of `recover-claude-code` at all — no scan
read, no tab opened, no transcript promoted, no journal spliced. No evidence these
overrides work, here or on any target. Nothing about a model *operating a machine*:
both measured sources watch a model build an artifact. Override 5's numbers are
prescribed, not measured. And what the target measured (Ghostty 1.3.1, Claude Code
2.1.238/2.1.239) was measured under Claude.

**[docs]** This file's own limit: a conditional side-file is the shape the health
checklist warns about — "Avoid writing a prompt with non-linear logic or conditionals
that require the model to piece together fragmented instructions from multiple
different places in the prompt." Read it in one pass before §1; every override names
the section of `SKILL.md` it lands on.

**No route-out block, and why.** The four shapes measured far enough behind to hand
elsewhere are `static-page`, `brownfield-integration`, `visual-design` and
`regression-sensitive`. This skill authors no page, renders nothing anyone looks at,
edits no multi-file codebase; the one artifact a run writes from prose is §5's
`fresh run of only those` script, `greenfield-module` shaped and measured level (75
against 75), so naming it would route away work Gemini does as well as opus.
`regression-sensitive` was the near miss — §5's splice-and-relocate must not break a
run that currently resumes — but the corpus measured *code* contracts, not on-disk
journal state, so it is bound B3 here instead.

## What already transfers intact

- **The procedure is already a chain of file artifacts.** `scan_crashed.py --json >
  /tmp/scan.json` then `open_tabs.py --scan /tmp/scan.json` is the remedy **[docs]**
  prescribes for an overloaded pass: "make each step a prompt and chain the prompts
  together in a sequence." The scan found zero qualitative skill references here.
- **§1's three-state table is already an objective constraint**, with a `What to do`
  column per row, and `--fresh-within` is a number where prose would have said
  `recently`. **[docs]** the **Ambiguity** entry asks for exactly that: "Avoid using
  subjective or relative qualifiers that lack a concrete, measurable definition."
- **`--json`, `--dry-run` and `ledger.json` are the machine-readable contract**, and
  `splice_result.py` already refuses to fabricate: it writes a copy and will not
  distil a result from a partial transcript — which is why there is no authorship
  section.

## The two ledgers

Write both into the recovery workdir before a single tab opens and report their
fractions in §6; `$W` is the workdir `open_tabs.py` prints, and `n/a: <reason>` is a
legitimate cell where blank is not. **[docs]** The **Recap** component says where
constraints belong: "Concise repeat of the key points of the prompt, especially the
constraints and response format, at the end of the prompt."

**[measured-family]** Why a table and not a firmer sentence: on `Egress Gemini` every
requirement the brief *enumerated* arrived — 12 of 12 named features — while every
requirement it named *categorically* arrived once or not at all: all states → 1, all
menus → 0, all flows → 0. That run's skill named six states and a completeness
condition in prose, and one was built.

### Quota ledger — the under-delivery half

| # | the scope, in `SKILL.md`'s own words | denominator command | filled with | report |
|---|---|---|---|---|
| Q1 | `Finds every session touched in a chosen window across all project directories` | `jq '.sessions \| length' /tmp/scan.json` | each classified LIVE / WRITING / STOPPED | `N of N classified` |
| Q2 | `The brief names every agent that was in flight, not only the ones that died loudly` | `jq '[.[].agents] \| add' $W/ledger.json` | each named in its session's brief | `N of N agents named` |
| Q3 | `A background agent outside a workflow → promote it the same way` | `jq '[.sessions[].loose_subagents \| length] \| add' /tmp/scan.json` | each promoted or explicitly declined | `N of N loose agents decided` |
| Q4 | `searching every project directory for the run id` (`references/mechanics.md`) | `ls ~/.claude/projects \| wc -l` | each searched for the run id | `N of N directories searched` |
| Q5 | §5's three-way choice, once per interrupted run | `jq '[.sessions[].unfinished_runs \| length] \| add' /tmp/scan.json` | promote / fresh run / splice, with the reason | `N of N runs decided` |

**Q2, filled** — the shape, not a measurement: 14 agents across 5 sessions · 12
named in briefs · 2 `n/a: runs finished before the crash window, per
--fresh-within` · reported `12 of 14 agents named, 2 n/a with reasons`.

**[derived]** Q2 collapses most easily, and the target names the mechanism itself:
an agent that reached the end of its turn without returning a result `leaves no
error anywhere` and is `exactly the one whose context is worth promoting`. Listing
only the loud failures satisfies the sentence and misses the recovery. Q3 is the
same failure from the other side — an mcp-router session held six loose agents on
2026-08-22, none in any run's ledger.

### Bound ledger — the over-delivery half

**[measured-family]** This half rests on a rate. Across 106 benchmark tasks, 58% of
Gemini's failing UI assertions at `medium` and 86% at `high` stated a bound rather
than asking for a thing, against 8% for opus and 6% for the OpenAI lane, and the
most-repeated bound failed on *every* instance in its set on a run that passed 37 of
its other 39. A bound is violated by what you did not write, so it survives checks
that look at what you did.

**[docs]** Google treats these as a component in their own right — "Restrictions on
what the model must adhere to when generating a response, including what the model
can and can't do." — and asks for them in the plan: "Ensure that all requirements,
constraints, options, and preferences are exhaustively incorporated into your plan."

| # | the bound, in `SKILL.md`'s own words | readback | expected |
|---|---|---|---|
| B1 | `Do not resume a session that is live in a terminal` (§3, Scope) | `comm -12 <(jq -r '.[].session_id' $W/ledger.json \| sort) <(jq -r '.sessions[] \| select(.state != "STOPPED") \| .session_id' /tmp/scan.json \| sort)` | no output |
| B2 | `The original session id, and never --fork-session` (§4) | `grep -c -- --fork-session $W/tab-*.sh` | `0` on every file |
| B3 | `Never edit the original journal` (§5) | `shasum $BASE/$RUN.as-the-crash-left-it/journal.jsonl` before and after | byte-identical |
| B4 | `Do not fabricate a journal result` (§5) | the `--result-file` path and the transcript line it came from | 1 real source per splice, both paths recorded |
| B5 | `SIGTERM, not SIGKILL` (§2) | `kill_orphans.py --kill` first, `--force` only after `--wait` | 0 SIGKILL on the first pass |
| B6 | `never more than one per repository` (Scope) | your own spawn count, per repo | ≤ 1 per repo, ≤ 3 total |
| B7 | `A detached session that is busy is left alone`, `A session with no transcript is left alone` (§2) | the read-only listing from the same script | 0 busy, 0 transcript-less, unless `--all-detached` was chosen deliberately |

Report `N of N instances within bound`, per row, in §6. **[derived]** B2, B3 and B5
are written in `SKILL.md` as prohibitions, and a prohibition reads as style advice
rather than as a number. Converting each into a counted property with a command is
the whole of the change; restating them more firmly is not, because the failure is a
default idiom supplying the value underneath a rule that was read and agreed with.

## Override 1. The liveness bound is checked before the first tab, not after the last (§3, Scope)

`SKILL.md` says it plainly: resuming a live session is `the one irreversible
mistake available here`. **[docs]** The agentic template's last rule is the same
rule: "Inhibit your response: only take an action after all the above reasoning is
completed. Once you've taken an action, you cannot take it back."

**[measured-family]** Why B1's command rather than a careful re-reading of the scan:
`Egress Gemini`'s own review shipped five well-formed PASS rows, including a browser
engine that failed all four invocation attempts and a 100% contrast pass rate from a
probe that never ran — measured afterwards, every primary button sat at 3.65:1 and
one glyph at 1.00:1. `12 sessions recovered, 0 live touched` has that shape when
nothing compared the two id lists.

## Override 2. Verification carries the command that produced it (§6)

**[docs]** "Include specific verification steps in either the system instructions or
your prompts directly." And from the agentic template: "Verify your claims by
quoting the exact applicable information (including policies) when referring to
them."

This reverses the house style deliberately: stripping verification scaffolding is
right for a model that over-verifies, and inheriting that removal here is the defect.
Every number in §6 carries its command and that command's output; a denominator of
zero is a gate that never ran, never a pass. §4 supplies the source — `If a tab fails
to open, the ledger records it` — so the report reads `ledger.json` rather than the
intention, and `Keep it to a few lines per session` becomes at most six, the last
always a fraction.

```
perch-4a (781039d7) — reopened, tab 3 of 10
  runs: wf_f7cd861f-b8c interrupted; 2 agents in flight, both promoted
  git:  ai/ord-0081 is 4 commits ahead of main — blocking finding committed
  left: wf_e313af91-67c not recovered — no script in any project dir
  scan: 5 of 5 classified · 12 of 14 named · 7 of 7 bounds within
```

## Override 3. Two attempts, then change approach (§1, §2, §4)

**[docs]** "On *other* errors, you must change your strategy or arguments, not
repeat the same failed call." And state the ceiling up front: "You have a limited
action budget of <n> tool calls. Use them efficiently." Three places here where a
call fails while reporting success, or fails identically on retry:

- **The synthesised `cmd+T`**, which §4 says `is accepted on macOS and does
  nothing`. The tab-count confirmation is the fix; do not wrap a retry around it.
- **The `-1719` tab-group error on a single-tab window** — permanent, so one attempt.
- **Reading a large `agent-NNN.jsonl`.** **[measured-family]** on `COD Dossier` a
  28.6k-token file hit the harness's 25k ceiling and the run retried `Read` four
  consecutive times before pivoting to a Python split. Agent transcripts are that
  size class: pivot on attempt 1 to a line-ranged read.

## Override 4. Read what the prompt names; recall is not a source (References)

**[docs]** "Your knowledge cutoff date is January 2025." The 3.7 Flash model card
moves that to March 2026 for some domains; both predate the Claude Code versions
this skill was measured against.

The target says the same: `references/mechanics.md` is pinned to Claude Code 2.1.238
and warns that `Behaviour changes between versions`, so the journal path, the registry
shape, the cache rule and the `normalisedOpts` key list are **read from that file**.

**[measured-family]** The same failure with a document named in the prompt: on `COD
Dossier`, asked a question naming three skills, the run answered from memory without
loading any; asked to fix it, it inverted the error and launched a skill instead of
answering. Load-then-answer is two ordered steps — `use the workflow-resume skill`
means read it, then decide. That confident-recall shape put Windows 10's `#0078D4` on
a Windows 11 surface in `Egress Gemini`; here it lands in an `mv`.

## Override 5. Delegation is capped, and the three-way choice is a closed set (Scope, §5)

`SKILL.md` already caps it: `One subagent is justified only when several repositories
each need their branch state reconciled ... never more than one per repository, and
never to check work already done.` As numbers: **at most one subagent per repository,
at most three in total, none for §1–§4.** Never delegate the liveness check.

**[docs]** §5's promote / fresh run / splice is a closed set of three, and the remedy
for a model that answers correctly but outside the offered options is to make it one:
"you can rephrase the instructions as a multiple choice question and ask the model to
choose an option." Record the choice and its reason per run, before acting, in Q5's
cell. On acting without checking in: "For exploratory tasks (like searches), missing
*optional* parameters is a LOW risk." §1's read-only scan is that class; the tab
open, the `--kill` and §5's `mv` are not.

## Override 6. `thinking_level` is set for what the work is, not as a remedy

**[docs]** `HIGH` is "suitable for complex prompts requiring deep reasoning, such as
multi-step planning, verified code generation, or advanced function calling
scenarios." A multi-session recovery is multi-step planning under an irreversible
action, so that is what the level is for here.

**[measured-family]** It is not a fix: paired across 106 tasks, `high` beat `medium`
on 24, lost on 24 and tied on 58, mean −1.7 points.

**[docs]** State the level rather than inherit it: the default drifts across the
family, from "If thinking_level is not specified, Gemini 3 will default to high" to
"The default thinking effort is now medium, changed from high in Gemini 3 Flash
Preview."

## Override 7. Brevity trims preamble, never the fraction line (§6)

**[docs]** "By default, Gemini 3 models provide direct and efficient answers." Direct
is the resting state and suits §6's six-line budget: what gets cut is preamble and
hedging, never pasted output or an `N of N`. And from **Underspecified task**:
"provide instructions for handling missing data rather than assuming inserted data
will always be present and well-formed." A session with no `cwd` in its tail, a run
whose script was not found, a tab that failed to open — each gets a named outcome.

## Modules not written, and what the scan dropped

`scan_skill.py --refs` fired two modules at the three-trigger threshold: `delegation`
(5 hits) and `bounded-constraint` (5). `gate` scored 2 (`probe`, `scripts/`) and is
not written — its content would restate override 2 against this skill's own scripts.
`count-contract` scored 1 (`ledger`). `visual`, `states`, `platform-values`,
`authorship` and `injection` scored nothing: this skill renders nothing, enumerates
no UI states, cites no vendor design values, publishes no prose a reader acts on,
ingests no third-party content. `emphasis` found no shouted tokens — `SKILL.md`
states its bounds in bold lower case, the register this file keeps.

Eleven scan rows were dropped as prose rather than deliverable scope: both quota rows
(`each claim`, at `SKILL.md:266` and `references/mechanics.md:7`, describing how the
reference files document themselves), one bound row (`One file per` live session —
Claude Code's disk layout, not this skill's output), and eight of the fourteen
relative-qualifier rows, where `brief` is the noun for the recovery brief. The three
that stand — `enough` at `:133`, `short` at `:201` and `:239` — are answered by
override 2's budget. Both ledgers are built from the target's own deliverables.
