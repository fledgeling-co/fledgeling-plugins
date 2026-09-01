# `recover-claude-code` on Gemini

`SKILL.md` transfers whole, and most of it needs no help: six numbered sections passing a
concrete file between them, scripts read-only until told otherwise, and the one
irreversible mistake named twice. What does not transfer is the assumption that a rule
stated in prose gets executed — and this skill's rules are almost all *bounds*, the shape a
Gemini run has been measured failing while delivering everything else asked of it.

## Epistemic status

**Tiers used:** `[docs]` — Google's published guidance, quoted verbatim ·
`[measured-family]` — Gemini runs of *other* work · `[derived]` — reasoning from those
two. No `[measured-here]` appears below. **Every measured rate here is flash-tier**:
`gemini-3.7-flash` over 106 benchmark tasks at `medium` and `high`, plus `Egress Gemini`
(n=1) and `COD Dossier` (n=1, `gemini-3.7-flash-high`). On the Pro tier the overrides
stand as `[docs]`-grounded discipline and every `[measured-family]` number is open.

**Unmeasured on this skill:** no Gemini run of `recover-claude-code` at all — no scan
read, no tab opened, no transcript promoted, no journal spliced, so no evidence these
overrides work here. Nothing about a model *operating a machine* either: both measured
sources watch a model build an artifact. Override 5's spawn numbers and override 7's
four-way reading of a zero are prescribed, not measured. And what the target measured
(Ghostty 1.3.1, Claude Code 2.1.238/2.1.239) was measured under Claude.

**[docs]** This file's own limit: a conditional side-file is the shape the health
checklist warns about — "Avoid writing a prompt with non-linear logic or conditionals
that require the model to piece together fragmented instructions from multiple different
places in the prompt." Read it in one pass before §1; every override names the section of
`SKILL.md` it lands on.

**No route-out block, and why.** The shapes measured far enough behind to hand elsewhere
are all authoring shapes: `static-page`, `brownfield-integration`, `visual-design`,
`regression-sensitive`. This skill authors no page and edits no multi-file codebase; what
a run writes from prose is §5's `fresh run of only those` script, `greenfield-module`
shaped and measured level (75 against 75). `regression-sensitive` was the near miss, but
the corpus measured code contracts, not journal state on disk, so that is bound B3.

## What already transfers intact

- **The procedure is already a chain of file artifacts.** `scan_crashed.py --json >
  /tmp/scan.json` then `open_tabs.py --scan /tmp/scan.json` is the remedy **[docs]**
  prescribes for an overloaded pass: "make each step a prompt and chain the prompts
  together in a sequence." The scan finds zero qualitative skill references here.
- **§1's three-state table is already an objective constraint**, with a `What to do`
  column per row, and `--fresh-within` is a number where prose would have said
  `recently` — **[docs]** "Avoid using subjective or relative qualifiers that lack a
  concrete, measurable definition."
- **`splice_result.py` already refuses to fabricate** a result from a partial transcript;
  it writes a copy and asks for a real one.

## The two ledgers

Write both into the recovery workdir before a single tab opens and report their fractions
in §6; `$W` is the workdir `open_tabs.py` prints, and `n/a: <reason>` is a legitimate cell
where blank is not. **[docs]** The **Recap** component says where constraints belong:
"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."

**[measured-family]** Why a table and not a firmer sentence: on `Egress Gemini` every
requirement the brief *enumerated* arrived — 12 of 12 named features — while every
requirement it named *categorically* arrived once or not at all: all states → 1, all
menus → 0, all flows → 0, on a run whose skill named six states and a completeness
condition in prose.

### Quota ledger — the under-delivery half

| # | the scope, in `SKILL.md`'s own words | denominator command | filled with | report |
|---|---|---|---|---|
| Q1 | `Finds every session touched in a chosen window across all project directories` | `jq '.sessions \| length' /tmp/scan.json` | each classified LIVE / WRITING / STOPPED | `N of N classified` |
| Q2 | `The brief names every agent that was in flight, not only the ones that died loudly` | `jq '[.[].agents] \| add' $W/ledger.json` | each named in its session's brief | `N of N agents named` |
| Q3 | `A background agent outside a workflow → promote it the same way` | `jq '[.sessions[].loose_subagents \| length] \| add' /tmp/scan.json` | each promoted or explicitly declined | `N of N loose agents decided` |
| Q4 | `searching every project directory for the run id` (`references/mechanics.md`) | `ls ~/.claude/projects \| wc -l` | each searched for the run id | `N of N directories searched` |
| Q5 | §5's three-way choice, once per interrupted run | `jq '[.sessions[].unfinished_runs \| length] \| add' /tmp/scan.json` | promote / fresh run / splice, with the reason | `N of N runs decided` |

**Q2, filled** — the shape, not a measurement: 14 agents across 5 sessions · 12 named in
briefs · 2 `n/a: finished before the crash window` · `12 of 14 agents named, 2 n/a`.

**[derived]** Q2 collapses most easily, and the target names the mechanism itself: an
agent that reached the end of its turn without returning a result `leaves no error
anywhere` and is `exactly the one whose context is worth promoting`, so listing only the
loud failures satisfies the sentence and misses the recovery. Q3 is the same failure from
the other side — an mcp-router session held six loose agents, none in any run's ledger.

### Bound ledger — the over-delivery half

**[measured-family]** This half rests on a rate. Across 106 benchmark tasks, 58% of
Gemini's failing UI assertions at `medium` and 86% at `high` stated a bound rather than
asking for a thing, against 8% for opus and 6% for the OpenAI lane, and the most-repeated
bound failed on *every* instance in its set on a run that passed 37 of its other 39 — a
bound is violated by what you did not write, so it survives checks that look at what you
did. **[docs]** Google treats these as a component in their own right — "Restrictions on
what the model must adhere to when generating a response, including what the model can
and can't do." — and asks for them in the plan: "Ensure that all requirements,
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

Report `N of N instances within bound`, per row, in §6. **[derived]** B2, B3 and B5 are
written as prohibitions, and a prohibition reads as style advice rather than as a number.
Converting each into a counted property with a command is the whole of the change;
restating them more firmly is not, because the failure is a default idiom supplying the
value underneath a rule that was read and agreed with.

## Override 1. The liveness bound is checked before the first tab, not after the last (§3, Scope)

`SKILL.md` says it plainly: resuming a live session is `the one irreversible mistake
available here`. **[docs]** The agentic template's last rule agrees: "Inhibit your
response: only take an action after all the above reasoning is completed. Once you've
taken an action, you cannot take it back."

**[measured-family]** Why B1's command rather than a careful re-reading of the scan: on
`Egress Gemini` the run's own review shipped five well-formed PASS rows, among them a
browser engine whose four invocation attempts had all failed and a 100% contrast pass rate
from a probe that never ran. `12 sessions recovered, 0 live touched` reads the same way
whenever nothing has compared the two id lists.

## Override 2. Verification carries the command that produced it (§6)

**[docs]** "Include specific verification steps in either the system instructions or your
prompts directly," and "Verify your claims by quoting the exact applicable information
(including policies) when referring to them." This reverses the house style deliberately:
stripping verification scaffolding is right for a model that over-verifies, and inheriting
that removal here is the defect. Every number in §6 carries its command and that command's
output; a denominator of zero is a gate that never ran, never a pass. §4 supplies the
source — `If a tab fails to open, the ledger records it` — so the report reads
`ledger.json`, and `Keep it to a few lines per session` becomes at most six, the last
always a fraction.

```
perch-4a (781039d7) — reopened, tab 3 of 10
  runs: wf_f7cd861f-b8c interrupted; 2 agents in flight, both promoted
  git:  ai/ord-0081 is 4 commits ahead of main — blocking finding committed
  left: wf_e313af91-67c not recovered — no script in any project dir
  scan: 5 of 5 classified · 12 of 14 named · 7 of 7 bounds within
```

**[docs]** Brevity trims preamble, never the fraction line: "By default, Gemini 3 models
provide direct and efficient answers" suits that six-line budget — what gets cut is
hedging, never pasted output or an `N of N`. And under **Underspecified task**, "provide
instructions for handling missing data rather than assuming inserted data will always be
present and well-formed": a session with no `cwd` in its tail, a run whose script was not
found, a tab that failed to open — each gets a named outcome rather than an omission.

## Override 3. Two attempts, then change approach (§1, §2, §4)

**[docs]** "On *other* errors, you must change your strategy or arguments, not repeat
the same failed call." State the ceiling up front — "You have a limited action budget of
<n> tool calls. Use them efficiently." — and note three places here where a call fails
while reporting success, or fails identically on retry:

- **The synthesised `cmd+T`**, which §4 says `is accepted on macOS and does nothing`.
  The tab-count confirmation is the fix; do not wrap a retry around it.
- **The `-1719` tab-group error on a single-tab window** — permanent, so one attempt.
- **Reading a large `agent-NNN.jsonl`.** **[measured-family]** on `COD Dossier` a
  28.6k-token file hit the harness's 25k ceiling and the run retried `Read` four times
  before pivoting to a Python split. Agent transcripts are that size class: pivot on
  attempt 1 to a line-ranged read.

## Override 4. Read what the prompt names; recall is not a source (References)

**[docs]** "Your knowledge cutoff date is January 2025" — and the 3.7 Flash model card's
March 2026 still predates the Claude Code versions this skill was measured against. The
target says the same: `references/mechanics.md` is pinned to 2.1.238 and warns that
`Behaviour changes between versions`, so the journal path, the registry shape, the cache
rule and the `normalisedOpts` key list are **read from that file**.

**[measured-family]** The same failure with a document named in the prompt: on `COD
Dossier`, asked a question naming three skills, the run answered from memory without
loading any; asked to fix it, it inverted the error and launched a skill instead of
answering. The last line of `SKILL.md` now writes its referral as a full name — `use the
workflow-resume:workflow-resume skill` — a Skill call to make, not a skill to remember:
read it, then decide. That confident-recall shape put Windows 10's `#0078D4` on a Windows
11 surface in `Egress Gemini`; here it lands in an `mv`.

## Override 5. Delegation is capped, and the three-way choice is a closed set (Scope, §5)

`SKILL.md` already caps it: `One subagent is justified only when several repositories each
need their branch state reconciled ... never to check work already done.` As numbers: **at
most one per repository, at most three in total, none for §1–§4** — and never the liveness
check.

**[docs]** §5's promote / fresh run / splice is a closed set of three, and the remedy for
a model that answers correctly but outside the offered options is to make it one: "you
can rephrase the instructions as a multiple choice question and ask the model to choose
an option." Record the choice and its reason per run, before acting, in Q5's cell. And on
acting without checking in — "For exploratory tasks (like searches), missing *optional*
parameters is a LOW risk" — §1's read-only scan is that class; the tab open, the `--kill`
and §5's `mv` are not.

## Override 6. `thinking_level` is set for what the work is, not as a remedy

**[docs]** `HIGH` is "suitable for complex prompts requiring deep reasoning, such as
multi-step planning, verified code generation, or advanced function calling scenarios."
A multi-session recovery under an irreversible action is that. **[measured-family]** It
is not a fix: paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on
58, mean −1.7 points. **[docs]** State the level rather than inherit it — the default
drifts across the family, from "If thinking_level is not specified, Gemini 3 will default
to high" to "The default thinking effort is now medium, changed from high in Gemini 3
Flash Preview."

## Override 7. The scan is an upstream artifact; check it in, and know what its zero means (§1, §4)

`open_tabs.py --scan /tmp/scan.json` consumes a file `scan_crashed.py` wrote, already in
what **[docs]** asks for — "a widely recognized standard like JSON, XML, Markdown or YAML
that can be parsed by common libraries" — and what is missing is the check on the way in.
**[measured-family]** On `COD Dossier` the run's own audit script checked tags and
citations thoroughly and nothing about whether its upstream artifacts existed, so two
skipped steps passed it at exit 0. Here a stale, empty or wrong-window `/tmp/scan.json`
opens zero tabs and reports success.

```bash
jq '[.sessions[] | select(.state=="STOPPED" and (.unfinished_runs|length)>0)] | length' /tmp/scan.json
```

**[derived]** A zero there is four facts wearing one number: `--minutes` did not reach the
crash, `--fresh-within` excluded its agents, the survivors have not been stopped yet (§2's
`Then scan again`), or nothing was owed. Widen the window and rescan before writing
`nothing to recover`, and run `scripts/selftest.py` first — its fixture `in the shapes a
real crash leaves` is the only negative control a zero can be checked against here.
**[docs]** Count with the command, "whenever the model needs to perform any kind of
arithmetic, counting, or calculation."

## Modules written, and what the scan dropped

`scan_skill.py --refs` fires three modules at the three-trigger threshold: `delegation`
(5 hits — override 5), `bounded-constraint` (5 — the bound ledger) and `gate` (3 —
override 7). `gate` scored 2 when this file was first written and crossed on the word
`denominator`, which sits in the pointer paragraph geminify installed at the top of
`SKILL.md` rather than in the skill's own subject; it is written on the content — §1's
scan, `--dry-run`, `ledger.json` and `scripts/selftest.py` are a real deterministic check
with a real silent-zero failure. `count-contract` scored 1 (`ledger`); `visual`, `states`,
`platform-values`, `authorship` and `injection` scored nothing — nothing rendered, no UI
states, no vendor values cited, no prose a reader acts on, nothing third-party ingested —
and `emphasis` found no shouted tokens, `SKILL.md` stating its bounds in bold lower case.

Dropped as prose rather than deliverable scope: both quota rows (`each claim`, at
`SKILL.md:268` and `references/mechanics.md:7`, describing how the reference files document
themselves), one bound row (`One file per` live session at `references/mechanics.md:22` —
Claude Code's disk layout, not this skill's output), and eight of the fourteen
relative-qualifier rows, where `brief` is the noun for the recovery brief. The ones that
stand — `enough` at `:135`, `short` at `:203`, `:207` and `:241` — are answered by override
2's six-line budget. Both ledgers are built from the target's own deliverables.
