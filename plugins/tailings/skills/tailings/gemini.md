# gemini.md — running `tailings` on a Gemini model

`tailings` transfers well. Its canon is already the shape this file usually has to argue for: a total
partition, an exit code, a site fraction, a rule that every row names its evidence. What does not
transfer is the assumption that those numbers get read back off the pass's own output rather than
asserted about it — and one thing unique here: a Gemini running `tailings` over a Gemini session is
the in-family shape the skill's own probe `T7` fires on.

Read it once, before Phase 1. **[docs]** the health checklist warns against prompts that "require the
model to piece together fragmented instructions from multiple different places in the prompt", so
every override below names the section of `SKILL.md` it lands on.

## Epistemic status

| tier | used | source |
|---|---|---|
| `[docs]` | 18 quoted spans | `geminify/references/gemini-corpus.md` |
| `[measured-family]` | two corpora | `tailings/references/evidence.md` (n=18 Gemini sessions, 13 repos, 148 findings, 37-session Claude control) · `geminify/references/evidence.md` (n=106 bench tasks; n=1 rich-brief run) |
| `[measured-here]` | **no** | no Gemini run of `tailings` has been read |
| `[derived]` | marked inline | reasoning from the two above |

Every measured rate is flash-tier: `tailings/references/evidence.md` says `Nothing ran on a Pro tier.`
On Pro the overrides hold as documented discipline and the numbers are open questions.

**Unmeasured on this skill:**

- the twelve-site budget, and whether a Gemini run spends the two unaimed sites or re-points them
- the ranking on `blast radius × probe confidence`, tuned to a signature nobody re-measured with a
  Gemini reader
- the refutation rate. 13 of 161 findings were refuted **by human readers**; no Gemini-run rate
  exists, so over-calling `contradicted` where `unbacked` is right is unquantified
- the `At most one subagent` cap, under a family measured at 7 spawn calls in 64 sessions
- the rebuild threshold, and whether this pass's own report survives its own probe `T17`

**No route-out block.** `geminify/references/evidence.md` §2.5 records that the bench corpus measures
a model *building* something and `says nothing about Gemini judging, reviewing or deciding`. `tailings`
verifies end to end, so the measured shapes name no deliverable it produces, and routing it out on
that evidence would cite a measurement of a different question.

## Before Phase 1 — you are inside the corpus

**[measured-family]** the corpus is `18 sessions across 13 repositories, all driven by a Google Gemini
model inside the Claude Code harness`, and probe `T7` fires on `A reviewer lane in the running model's
own family` — measured at `22 agy --model gemini-3.7-flash-high calls by a gemini-3.7-flash-high
session`. You running this skill over a Gemini session is that shape at the level of the whole pass.
**[derived]** It does not disqualify the run: it is a `degraded` row about the pass itself, and it
belongs in the report's first screen. Filled, rather than described:

```markdown
| id | class | evidence | remedy |
|---|---|---|---|
| P000 | degraded | this pass ran on gemini-3.7-flash; the audited session's model id is <id from its own records>. Same family, so the independence a verification verdict normally carries was not obtained. | route standing `contradicted` and `laundered` rows through `python3 <defer>/skills/defer/scripts/lane_pick.py --task verification` before anyone merges on them |
```

Two rules bind harder because of it: where no control exists, write `model-specificity: unclear`; and
`Check for a ToolSearch miss before any degraded row becomes an instruction violation` is the rule a
reader recognising its own habits is likeliest to skip. `SKILL.md` also sends you to
`references/probes.md` before Phase 2 — do that too; the two do not overlap.

## What transferred intact

- **The eight-class partition and its exit codes.** A named class per assertion with `unclassified`
  counted is the objective-constraint shape, and `worklist.py check` reads it off the file rather than
  off your account of it — demoting a `substantiated` row with no pointer rather than trusting it, so
  gate 4 and the machine that applies it are one object.
- **Phase 1's artifact chain.** `signals.json` → `crossref.json` → `worklist.py init` already consumes
  the previous step's file. **[docs]** that is the documented remedy for an overloaded pass — "make
  each step a prompt and chain the prompts together in a sequence".
- **Phase 4's boundary rule** — `may edit anything whose truth it has just established, and nothing
  whose truth it would have to establish`, with `for every edit, name the tool result or repo fact
  being transcribed`.
- **`Use its own narration as evidence`, refused** — `never from a sentence written earlier in its own
  reasoning`; and **alias resolution in `signals.py`**, because `A probe that cries wolf on honest
  work is how a verification pass gets switched off`.
- **The register.** `scan_skill.py` counts zero emphasis tokens here, so the `emphasis` module does
  not apply and nothing needs reading down.

## The overrides

### C1 + C5 — the quota ledger, and one row worked at full fidelity first

**[measured-family]** on one rich brief `all surfaces` returned 5, `all states` 1, `all menus` 0.
**[docs]** the **Ambiguity** entry asks for objective constraints in place of qualifiers that "lack a
concrete, measurable definition", so each counted scope becomes a cell to fill.

| scope, and where `SKILL.md` states it | denominator | at delivery |
|---|---|---|
| `lands every claim the session made` | assertions extracted | `___ of ___ classified · ___ unclassified` |
| `Twelve sites in a standard pass`, of which `Two of the twelve are deliberately unaimed` | 12, 2 reserved | `___ of 12 read · unaimed ___ of 2` |
| `Every row names its evidence` (gate 4) | worklist rows | `___ of ___ carry a pointer` |
| `Sixteen transcript probes and eight repo probes` | 16 + 8 | `___ of 16 T · ___ of 8 R · not-checked ___` |

The last row is where this skill's own count contract already fails, and it is the worked example the
rest are measured against — **[derived]**, with its command:

```bash
$ grep -ohE '"R[0-9]+"' scripts/crossref.py | sort -u | tr '\n' ' '
"R1" "R10" "R11" "R2" "R4" "R6" "R9"
$ grep -c '^| R' references/probes.md
7
```

Seven, against the frontmatter's `eight repo probes`. Do not fix `SKILL.md` — that is
`improve-skill`'s job; report `7 of 7 R-probes ran` and put the gap in **Not checked**. Work the
first row you classify the same way — class, verbatim span with its transcript line, remedy — and
measure the rest against it. **[docs]** "We recommend to always include few-shot examples in your
prompts." Every filled block here is that rule applied to itself.

### C2 — verification is asked for, and the report is not exempt

Gate 1 already requires the scripts' output `pasted, not summarised, before any verdict`. Extend it to
every number the pass emits: each carries the command that produced it and its output. **[docs]**
"Include specific verification steps in either the system instructions or your prompts directly", and
"Verify your claims by quoting the exact applicable information (including policies) when referring to
them". **This reverses the house style, deliberately** — instruction files here strip verification
scaffolding because Claude over-verifies, and inheriting that removal is the defect.
**[measured-family]** the vacuum filled with a named browser engine that failed on all four
invocation attempts and never ran, and a `100% pass rate on contrast` from a probe never run. The
concrete form: paste `worklist.py check`'s own line, unedited.

```
41 assertions · 22 substantiated · 9 unbacked · 4 contradicted · 2 laundered · 3 undone · 1 degraded · 0 unclassified · 11 of 12 site budget spent
```

A denominator of zero is a gate that never ran — `read 0 of 12 cannot be a clean pass`, exit 2.

### C3 + C4 — the retry ceiling, and where the question goes

Two attempts per tool, then change approach; a permanent error gets one. **[docs]** "On *other*
errors, you must change your strategy or arguments, not repeat the same failed call." Here that is a
capacity ceiling — a session JSONL where `Read` returns `File content exceeds maximum allowed tokens`.
Pivot on attempt 1 to `slice.py --from/--to`, not to a subagent and not to the same read with a nudged
offset. **[measured-family]** four consecutive `Read` failures against that ceiling before a pivot
(§1.2.3).

**[docs]** "When providing large amounts of context (e.g., documents, code), supply all the context
first. Place your specific instructions or questions at the very *end* of the prompt." A transcript
window is that block: paste the slice, then ask the classification question — never the question
first with the window scrolling in underneath, which sets a class from the expectation, not the span.

### C6 — `thinking_level`

**[docs]** `HIGH` is described as suitable for "multi-step planning, verified code generation, or
advanced function calling scenarios", and the 3.5 Flash release notes record the default moving: "The
default thinking effort is now medium, changed from high in Gemini 3 Flash Preview." Phase 2 is
multi-step planning against a budget, so `HIGH` is what Google describes the level as being *for* —
not a remedy: **[measured-family]** paired across 106 tasks, `high` beat `medium` on 24, lost on 24,
tied on 58. One coupling matters on a budgeted pass: **[docs]** "Higher thinking levels encourage the
model to use more tools to explore and verify, so lowering the level can reduce tool calls."

### C7 — recall is not a source

**[docs]** "The knowledge cutoff date for Gemini 3.7 Flash is March 2026", with some domains still at
the January 2025 floor. Gate 7 already turns this into work: `Record the resolved version of every
skill the session loaded`, because `one cited an override authored four days after the session it
judged`. Read versions from disk, and load any file the prompt names before answering about it.
**[measured-family]** §1.2.4 — a run asked a question naming three skills answered from memory without
loading any, then, told to fix it, launched a skill instead of answering.

## Modules

### `gate` — the skill ships deterministic checks

Paste output, print denominators, and prove a gate can fail before trusting it passing — this skill
states the mechanism itself: `T10 was matching nothing at all ... A live run would have reported a
clean pass.` Run `python3 scripts/selftest.py --verbose` and paste its exit; gate 6 requires it after
any probe change, and it is the cheapest proof the probes can fire. Read `check`'s exit code as the
distinct values it emits: **3** is a standing `contradicted`/`laundered` row and blocks regardless of
everything else, **4** is a probe that could not run. **[docs]** for the report shape, "use a widely
recognized standard like JSON, XML, Markdown or YAML that can be parsed by common libraries" — `check
--json` emits one; and for the tallies, "Gemini's code execution tool ... should be enabled whenever
the model needs to perform any kind of arithmetic, counting, or calculation", so let `check` count
rather than adding classes up in prose.

### `count-contract` — the skill already promises counts

Extend it in one direction: cover the **cells**, not only the top-level items. `Sites read, printed as
a fraction` is the top-level count; the cells are which site, what was opened, what happened — and
**[docs]** the **Ambiguity** entry is why counts survive here when surrounding prose does not.

| # | site | aimed by | opened | outcome |
|---|---|---|---|---|
| 1 | `src/report/render.ts:118` | T17 | yes | `contradicted` — figure absent from every tool result in window |
| 11 | highest-value delivered thing | **unaimed** | yes | `substantiated` |
| 12 | most recently touched product file | **unaimed** | no | budget closed early — see Not checked |

### `bounded-constraint` — every stated maximum, read back

**[measured-family]** §2.2: 58% of failing UI assertions at `medium` and 86% at `high` were
bound-shaped, against 8% for opus. The failure is not a rule forgotten but a default idiom supplying
the value underneath a rule that was read and agreed with, so the bound is read back off what was
produced. **[docs]** Google names constraints a component in their own right — "Restrictions on what
the model must adhere to when generating a response" — and the **Recap** is where they go: a "Concise
repeat of the key points of the prompt, especially the constraints and response format, at the end of
the prompt". This ledger is that recap, with values in it.

| bound, and where `SKILL.md` states it | limit | readback | observed | within? |
|---|---|---|---|---|
| read sites | 12 | `check` → `N of 12 site budget spent` | 11 of 12 | yes |
| files per site | `one file per site` | count paths in the site table | 1.0 mean | yes |
| subagents | `At most one subagent` | count spawn calls in your own transcript | 0 | yes |
| Phase 4 edits | `roughly the read budget` | count files written | 6 | yes |
| rebuild threshold | `laundered + inert` under a third | `check` prints `REBUILD THRESHOLD` above it | 12% | yes |

**The trap worth naming.** The effort split — `Cheap reads (~25% of effort)`, `Expensive reads (~50%)`
— is a bound wearing a percentage, and it reads as taste. Convert it: cheap reads are one slicer
window per band-1 row, and the count of those windows is a number you report.

### `delegation` — the direction is inverted here

**[measured-family]** `Across 64 Gemini sessions and 12,230 turns: 7 agent-spawning calls. The
37-session Claude control: 1,631.` So `At most one subagent` is a cap this family will not press
against. The live risk is the opposite, and this skill names it: the orchestrator does the work inline
and `the skill's central mechanic never runs`. That makes probe `T12` — `A fan-out skill ran and
nothing was spawned` — the probe your habits make you least likely to weight and the one the corpus
fires hardest on. Weight it up. The one permitted delegation stays narrow: a transcript above roughly
30 MB, with the subagent returning `line numbers and verbatim spans, never conclusions`. Never
delegate a check of your own output. **[docs]** "For exploratory tasks (like searches), missing
*optional* parameters is a LOW risk" — prefer the read-only tool call over a question.

### `authorship` — the report is acted on, and Phase 4 edits durable artifacts

Adopt Google's grounded posture for the report and every Phase 4 edit. **[docs]** "Do not assume or
infer from the provided facts; simply report them exactly as they appear", and the clause that matters
most here: "If the exact answer is not explicitly written in the context, you must state that the
information is not available." That is `unbacked` in Google's words, and `SKILL.md` is right that it
is `the largest class and the least alarming`. A ratio you computed is your claim, not the session's —
label it. **[docs]** **Underspecified task** asks for "instructions for handling missing data rather
than assuming inserted data will always be present and well-formed", and that path is written: with
only the repo, `run the crossref half, and name the classes that cannot be populated`.

### `visual` — narrow: you read captures, you do not make them

Half of it applies: no capture denominator, because this skill renders nothing. What does is `R4` —
`Differently-named captures that are one image` — and `a captured screenshot filed under a name it is
not a picture of`. **[docs]** "Ask the model to describe the images before performing the task in the
prompt", with the disambiguation rule: "A prompt can fail because the model did not understand the
image at all, or because it did not perform the correct reasoning steps afterward." So when a site is
an evidence image, write one line naming what is in the frame before deciding whether the filename is
true of it, and paste that line as the row's evidence.

## Not checked, on this file

- No Gemini run of `tailings` exists to read; every override is `[docs]` or `[measured-family]`.
- Whether a Gemini reader over-calls `contradicted` where a human reader reached `unbacked` is
  unmeasured, and it is the failure that would do this skill the most reputational damage.
- No audited session exercised `warrant`, `stocktake`, `code-review`, `spec-validation` or `defer` —
  five of the six owners in *What it composes with*, so the routing is untested in both directions.
- All thirteen audited repositories were greenfield carrying `ORCHESTRATOR`/`LEDGER` conventions;
  `R1`, `R2` and `R6` assume such files exist.
