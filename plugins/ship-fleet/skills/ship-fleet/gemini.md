# gemini.md — `ship-fleet`

Read this once, then read `SKILL.md` and follow it with the overrides below; each names the section it lands on.
The canon transfers — the DAG, the serialized merge, the stop rules, the four failure channels, the
reconciliation exit. What does not is the assumption that a rule stated in prose gets executed. Almost nothing
this skill emits is compiled: a ledger row, a wave plan, a runner brief and a status are shapes with obvious
columns and no checker, and the skill names the consequence — `A fleet is where a Done column is built, so it is
where an unauditable one starts.` The risk is twenty rows reading `Done` because a dispatch returned.

## Epistemic status

**Tiers:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]` — no Gemini run of `ship-fleet` has
been observed at any tier. The family sources are two single sessions (n=1 each) and a 106-task benchmark at
two effort levels (`geminify/references/evidence.md`); neither watched a model conduct anything. Every measured
rate below is flash-tier (`gemini-3.7-flash`, one session on `-high`) and does not project onto Pro, where
these overrides hold as `[docs]`-grounded discipline while every number stays open.

**[docs]** The thinking defaults drift inside the family, so a file written against one tier gets a different
budget on another: *"If thinking_level is not specified, Gemini 3 will default to high."* against, from the 3.5
Flash release notes, *"The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."*
Conducting a fleet is what `HIGH` is described as being for — *"multi-step planning, verified code generation,
or advanced function calling scenarios."* — and 3.7 Flash defaults to `MEDIUM`, uplift unmeasured here. It is no
remedy for anything below: **[measured-family]** paired across 106 tasks, `high` beat `medium` on 24, lost on
24, tied on 58, mean **−1.7** points, and the bound-shaped failure share *rose* from 58% to 86% (§2.3).

**Unmeasured on this skill:** no Gemini run has kept a ledger, filled a slot, resolved a merge conflict or
written a runner brief · none anywhere has been measured *with* a `gemini.md` against the same work without one
· Override 6's rate came from UI assertions, so its transfer to `Five concurrent agents` is `[derived]` · Phase
6's reconciliation gate and the 0-of-409 context finding are new since this file's last pass and no run has been
seen against either · `SKILL.md` specifies **Claude** runners, so Override 2 is about the brief you write ·
under `tiered` the binding may seat a Gemini model as a worker, which nothing covers.

**[docs] The self-limitation.** A conditional side file is the shape the checklist warns about: *"Avoid writing
a prompt with non-linear logic or conditionals that require the model to piece together fragmented
instructions from multiple different places in the prompt."* One pass, before the skill. **One target, one
file:** `ship-fleet` is also in `diolog-plugins`, whose copy is an older 156-line SKILL.md; this one is
canonical and that mirror is left alone rather than drifted.

## Route out before you render or merge

**[docs]** The health checklist says it outright, under **Task outside of model capabilities**: *"Avoid using
prompts that ask the model to perform a task for which it has a known, fundamental limitation."* Two of this
skill's own deliverables — not its runners' — land in measured shapes.

| shape | where it lands here | measured |
|---|---|---|
| `static-page` | `orchestrator-hierarchy.html`: self-contained, inline CSS/JS, no build step, SVG dependency edges | 22 against opus's 67, a hard zero on 71% of decided rows |
| `regression-sensitive` | the serialized finalize — rebase, pre-merge gate, merge into an integration branch that currently passes, conflicts resolved by you in the worktree | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

A pointer rather than a pinned model, because the numbers move. **Omitted:** `brownfield-integration` (multi-file
edits are the runners' work; the conductor's one exception is the merge row) and `visual-design` (Phase 1's mock
comparison judges rather than builds). `greenfield-module`, `algorithmic`, `accessibility` and `react-ui` are
level with opus. Where no lane is free, this block names what to distrust first.

## What transfers intact

- **The three scheduler rules are already exit conditions** — `A null return is a death, not a completion.` ·
  `Never Promise.race an empty map.` · `done means merged.`
- **The 2026-08-26 measurements arrive as thresholds** — `Derive failure from started − results`, `under 1.2
  the wave ran serially`, per-item rather than per-wave verify. Each is a number with a comparison attached,
  the one shape §2.1 shows this family holds: where a brief states a numeric bound, Gemini scores 74.7 against
  opus's 75.0. Compute them; do not restate them.
- **The context contract now puts the binding half in the prompt**, the documented placement. **[docs]**
  *"Prioritize critical instructions: Place essential behavioral constraints, role definitions (persona), and
  output format requirements in the System Instruction or at the very beginning of the user prompt."*
- **The tiered block already carries Override 2's rule** — `Enumerate every deliverable rather than describing
  a category`, and `Never name a model in a runner prompt`. Follow both verbatim, and read the six shouted
  tokens across 962 scanned lines as the plain rules they are.

## Override 1 — write the denominators down before Phase 1 (Phases 1, 3, 5)

`SKILL.md` names its scopes categorically — `Classify every item`, `Update it after every state change`, `keep
every section`, `every item Done / parked-with-reason` — each a set with a knowable size that nothing states.
**[measured-family]** One run delivered **12 of 12** requirements its brief *enumerated* and satisfied every
requirement named *categorically* with one instance or none: all surfaces → 5, all states → **1**, all menus →
**0**, all flows → **0** (§1.1.1, n=1), while the skill it followed stated six states and an explicit
completeness condition in prose.

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition."* The
survey's inputs print their own denominator, so count first — filled here against a 23-item backlog:

| scope, in `ship-fleet`'s words | denominator | filled | reported |
|---|---|---|---|
| `Classify every item` | 23 = 11 ledger rows + 7 specs + 5 briefs | 23 | `23 of 23, 8 of 10 categories used` |
| deps · research · mock per item | 23 × 3 = 69 | 64 | `64 of 69, 5 n/a: no mock exists` |
| `every state change` written before acting | 47 events this run | 47 | `47 of 47 in the event log` |
| `keep every section` of the template | 7 sections | 7 | `7 of 7, none adapted away` |
| `every item Done / parked-with-reason` | 23 | 21 Done · 2 parked | `23 of 23 terminal, 2 with reasons` |

**[docs]** An unfillable cell reads `n/a: <reason>`, because Google asks for *"instructions for handling missing
data rather than assuming inserted data will always be present and well-formed."* The counting is itself a tool
call: *"Gemini's code execution tool enables the model to generate and run Python code, and should be enabled
whenever the model needs to perform any kind of arithmetic, counting, or calculation."*

## Override 2 — the runner brief is a prompt you are writing (Phase 5, the context contract, tiered)

The highest-leverage override here, because the base template carries the sentence shape that collapsed in
§1.1.1: `must still represent the feature's ENTIRE UI — every surface, state, user interaction, user flow, and
popup/modal/menu`. Five categorical nouns in one clause; the measured outcome was 5 · 1 · 0 · 0 · one generic
toast. Fill the `⟨⟩` with enumerations instead — surfaces from the spec, states from the design system, flows
from the brief, each numbered, the handback reporting `18 of 20 states built, 2 n/a: no error path`. Same for
`Sources — read all that exist, in full`: list the paths, count them, ask for `N of N`.

**The contract now names which half is text and which is a path, and that half is a count too.** `SKILL.md`
measured the project `CLAUDE.md` reaching **0 of 409** subagent contexts while 69 briefs named it by path, and
concludes `A path is a request. Text in the prompt is a constraint.` Its four-row table is a denominator:
`prohibitions 6 of 6 verbatim · acceptance criteria 9 of 9 named separately · design tokens 14 of 14 · gate
commands 4 of 4 with exit codes`.

**[docs]** *"We recommend to always include few-shot examples in your prompts."* and *"you can remove
instructions from your prompt if your examples are clear enough in showing the task at hand."* So the brief
ships one filled row of the coverage table it asks for, and the two lines the skill says to carry verbatim —
the git-identity rule, the never-strip-the-safeguards rule — are copied rather than summarised: a paraphrase of
a rule whose value is its exactness is another rule.

## Override 3 — every status carries the command that produced it (Operating discipline, Phases 0 and 2, Guardrails)

**[measured-family]** The §1.1.2 run (n=1) wrote itself a five-row review, all `PASS`, asserting a named
browser engine as verified when it had failed all four invocation attempts, and a 100% contrast pass rate from
a probe never executed — measured afterwards, every primary button 3.65:1 and one glyph 1.00:1, invisible. Not
dishonesty: a requested *shape* completed where the procedure was unspecified. `ORCHESTRATOR.md` is precisely
such a shape.

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* and *"Verify your claims by quoting the exact applicable information (including policies) when
referring to them."* So the header contract ships as receipts, filled:

```
codex   09:12 · perl alarm 600 codex exec -m gpt-5.6-sol … → OK; log has reasoning effort: medium
slots   09:14 · $HM/berths.py → {"available":6} · budget = min(5, 6, 16÷4) = 4 · measured
egress  09:12 · grep -rlE 'ANTHROPIC[- ]ONLY|…' CLAUDE.md AGENTS.md … → no hit → lane on
deaths  11:02 · started 6 − results 5 = 1 → MOT-0051 died; error_rows 0, ignored
fanout  11:02 · Σ agent durations 4h58m ÷ wall 1h12m = 4.1 → ≥ 1.2, fanned out
reckon  18:20 · reckon.py check docs/reckoning/…/ledger.json → exit 0 · 0/0/0/0
```

**A green exit proves what the gate checks, never what it does not.** **[measured-family]** On `COD Dossier` an
auditor validated tag counts, citations and contrast floors thoroughly, had no check that its prerequisite
artifacts existed, and passed two skipped skill invocations with exit code 0 (§1.2.2). Here: `git branch
--merged` proves a merge, not a passing gate; `berths.py` proves headroom, not that runners launched at that
number; `error_rows: 0` proves nothing at all — the skill's own point, 0 error rows across 147 journals while
146 agents failed to return. The flagship gap says the rest, `a verifier that exists but is never invoked
verifies nothing`: before a row turns `Done`, check the verdict comment exists and record its oracle rung. A
denominator of zero is a gate that never ran, never a pass.

## Override 4 — two attempts, then a different move (Phase 5 failure handling, the context contract)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed call."*
The skill's `max 2 restarts, then park` is the stricter rule; keep it.

**[measured-family]** Both n=1 sessions ran the loop: one invoked a banned, absent tool four consecutive times
with nothing changed between attempts (§1.1.2); the other hit a 25,000-token `Read` ceiling and retried four
times before pivoting to a Python split (§1.2.3). `gemini-cli` ships a loop detector whose halt message names
*"repetitive tool calls"* (§7.2). Four `ship-fleet` errors look transient and are not. **A deep-research doc
read `in full, not skimmed`** is §1.2.3's exact file class — chunk or line-range on the *first* capacity error.
**A held `.ledger.lock`** past ten minutes is arbitration, not a fifth attempt. **An empty codex `-o` file, or
a log missing `reasoning effort: medium`,** is a lane failure with a clean exit code: log the in-family
downgrade in the artifact and the ledger. **A runner returning `null`** has its counter already — park at three.

## Override 5 — a named instrument becomes a path in the ledger (Phase 5, Phase 6, Guardrails)

**[measured-family]** §1.2.1 (n=1): a skill instructed that every design decision `goes through` two named
skills, and the run invoked neither — its own diagnosis being that the guidance was already in context and
nothing downstream depended on a file only those skills produce. The same reclassification is recorded on the
**Pro** tier (§7.2). The scan found **0** qualitative skill references here — `ship-fleet` invokes by full
`plugin:skill` name — so this is `[derived]` from that mechanism, not a flagged phrase. Eight named instruments
are conditional and produce nothing a later step reads.

**[docs]** *"make each step a prompt and chain the prompts together in a sequence."* Chain them by writing each
output's path into `ORCHESTRATOR.md` before the next step runs:

```
harbourmaster berths.py     → slots + timestamp in the header      (re-read every refill)
better-goal (unattended)    → docs/goals/goal-<slug>.md, in the header, before slot 1
workflow-resume             → the recovered run id, in the event log, before any relaunch
capture-lineage.py --gate   → exit code + date in the header, once per repo
campaign.py check / reckon  → the campaign dir, then docs/reckoning/<date>/ledger.json
campaign.py export-warrant  → the warrant path, in the final row, once at fleet end
whats-left                  → whats-left-<repo>.html, path under Needs input
```

A header row naming no path is the declaration §1.2.1 produced: compliant-looking text where a tool call
should have been.

## Override 6 — the caps are bounds, and bounds are the measured failure (Operating discipline, scheduling §The fleet)

**[measured-family]** Bounds are what this family exceeds rather than forgets: classifying every failing UI
assertion by whether it states a bound or asks for a thing, **58%** of Gemini's failures at `medium` and **86%**
at `high` were bound-shaped, against 8% for opus and 6% for the OpenAI lane; one rule — `has exactly one soft
elevation shadow` — failed on *every* card and *every* toast in its set, on a run that passed 37 of its 39 other
assertions (§2.2). A bound is violated by what you did not write, so it survives every check of what you did.

**Take the smaller of the two numbers the target now carries.** `SKILL.md` states `Five concurrent agents is a
correctness limit, not a throughput preference` with 92 silent deaths behind it, while
`references/orchestrator-artifacts.md`'s resume template and the scheduler sketch still say `≤ 8 concurrent
runners` and `let slots = 8`. Copying the template writes the older, looser number into the file a fresh
session resumes from. Five, or berths if lower, and say which.

**[docs]** Google asks that *"Ensure that all requirements, constraints, options, and preferences are
exhaustively incorporated into your plan."*, and supplies the budget instruction directly: *"You have a limited
action budget of <n> tool calls. Use them efficiently."* Each cap becomes a row read back off what you
launched, never off `SKILL.md`:

| bound, in `ship-fleet`'s words | readback | observed | within? |
|---|---|---|---|
| `Five concurrent agents`, or berths if lower | `running.size` at each refill | 6 | **no — 5 is the limit** |
| `slots × wave ≤ ~16` | slots × the wave width in the brief | 5 × 4 = 20 | **no — lean the waves** |
| `under 1.2 the wave ran serially` | Σ agent durations ÷ wall clock | 4.1 | yes |
| `a runner touches only its own <ID>'s files` | `git diff --name-only main...ai/<id>` | 2 shared DS files | **no — fold back** |
| `max 2 restarts, then park` | the `attempts` map | 3 on MOT-0051 | **no — park it** |

Report `2 of 5 bounds within, 3 corrected`. A table filled from the skill rather than from what you launched
shows five greens, which is the failure itself rather than a report of it. **The forks are closed sets:** combine
a dependency cycle or ask; slot-refill or batched workflows; retry sharper, resume in-worktree, or park.
**[docs]** *"you can rephrase the instructions as a multiple choice question and ask the model to choose an
option."* Record the option chosen; invent no sixth.

## Override 7 — the exit condition is four zeros, not a drained ledger (Phase 6)

`Say the shape of the finish in the report.` The skill measured seven projects it orchestrated in one week, every
one reporting its backlog implemented and verified, and every one wrong — because `49 of 49 merged` counts rows
rather than working features. That is the §1.1.2 shape at fleet scale: a requested shape completed where the
procedure was unspecified. Phase 6 is the only place the run's claim is checked by something it did not write,
so both commands run, both exit codes go in the header, and `Any of unbuilt, broken, unmeasured or undecided
above zero is another wave, not a footnote.` `unmeasured` is likeliest to be reported as zero without being
zero, because a blocked check reads as neither a pass nor a failure.

```
campaign.py check <dir>        → exit 0   (a stale campaign carries evidence and measures none)
strict-check.py <dir>          → exit 0
reckon.py check …/ledger.json  → exit 0 · unbuilt 0 · broken 0 · unmeasured 0 · undecided 0
```

## Override 8 — the one thing you render, and the one you judge (Phase 3, Phase 1 mock comparators)

`orchestrator-hierarchy.html` is generated *from* the ledger data, never maintained beside it — one card per
ledger row, one edge per dependency; open the file, count what rendered, report the fraction against the
ledger's counts, and if you author rather than route it, check its bounds first (one card per row, one legend,
the `Updated:` stamp). Phase 1's mock comparators ask whether a mock is `more refined than` the app preview.
**[docs]** *"Ask the model to describe the images before performing the task in the prompt."* and *"To improve
the response, point out which parts of the image are most relevant to the prompt."* Name what is in each
surface — surfaces, states, density — then judge; one comparison per mock, both opened, fraction reported, and
an unopened mock is `unknown` rather than `not more refined`.

## Override 9 — read, then answer; recall is not the ledger (Resuming, the context contract)

**[measured-family]** §1.2.4 (n=1): asked a question naming three skills, the run answered from memory without
loading any of them; §1.1.4 records a previous-generation published value returned confidently. What goes stale
here is `codex-cli 0.145.0+`, the lane model ids, and the ~1-hour prompt cache TTL the scheduling reference
itself calls an observation, not a guarantee.

**[docs]** *"Your knowledge cutoff date is January 2025."* and, from the strictly-grounded system instruction's
last clause, *"If the exact answer is not explicitly written in the context, you must state that the
information is not available."*

`ship-fleet` states both halves — `ORCHESTRATOR.md exists → never re-survey from scratch` and `After
compaction: re-read it, the DESIGN md, and the ledger before acting` — and measured what happens when only the
second is stated: three compactions in one window, none followed by a re-read of any instruction file. Make
them ordered steps: read `ORCHESTRATOR.md`, run `git worktree list` and `git branch --merged`, *then*
reconcile. A status you cannot re-derive is unavailable, not zero.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response format, at
the end of the prompt."*

1. Count the backlog before classifying it; report `N of N` at every phase boundary.
2. Enumerate in the runner brief what `SKILL.md` states categorically, inline what must bind, count both.
3. Every header field and status carries its command, that command's output and a timestamp.
4. One retry on a transient error; none on a read ceiling, an empty `-o` file or a held lock.
5. Each named instrument writes a path into `ORCHESTRATOR.md` that a later step reads.
6. Fill the bound table from what you launched; five concurrent, not eight.
7. The fleet finishes at four zeros from `reckon`, not at a drained ledger.
