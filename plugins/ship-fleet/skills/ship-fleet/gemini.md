# gemini.md — `ship-fleet`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. The canon transfers — the DAG, the serialized merge, the stop rules, the four
failure channels. What does not is the assumption that a rule stated in prose gets executed.

`ship-fleet` is exposed in an unusual way: almost nothing it emits is compiled. A ledger row, a
wave plan, a runner brief and a status are shapes with obvious columns and no checker, and the
skill names the consequence itself — `A fleet is where a Done column is built, so it is where an
unauditable one starts.` The risk is not a worse schedule; it is twenty rows reading `Done`
because a dispatch returned.

## Epistemic status

**Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]` — no Gemini run
of `ship-fleet` has been observed, at any tier. The family-tier sources are two single sessions
(n=1 each) and a benchmark of 106 tasks at two effort levels (`geminify/references/evidence.md`);
neither watched a model conduct anything.

**The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
(one session on `gemini-3.7-flash-high`) — flash-tier claims, not to be projected onto the Pro
tier, where these overrides hold as `[docs]`-grounded discipline while every measured number is
open. **[docs]** Defaults drift inside the family, so a file written against one tier gets a
different thinking budget on another: *"If thinking_level is not specified, Gemini 3 will default
to high."* against, from the 3.5 Flash release notes, *"The default thinking effort is now medium,
changed from high in Gemini 3 Flash Preview."*

**Unmeasured on this skill:** no Gemini run has kept a ledger, filled a slot, resolved a merge
conflict or written a runner brief · none anywhere has been measured *with* a `gemini.md` against
the same work without one, so there is no evidence these fixes work · the bound-following rate
below was measured on UI assertions, so its transfer to `≤ 8 concurrent runners` is `[derived]` ·
`SKILL.md` specifies **Claude** runners, so Override 2 is about the brief you write.

**[docs] The self-limitation.** A conditional side file is the shape the checklist warns about:
*"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
together fragmented instructions from multiple different places in the prompt."* Read it in one
pass, before the skill; each override is anchored to a section.

**One target, one file.** `ship-fleet` is registered here and in `diolog-plugins`; this copy is
canonical, and the diolog mirror is left alone rather than given a duplicate that would drift.

## Route out before you render or merge

**[docs]** The prompt health checklist says it outright, under **Task outside of model
capabilities**: *"Avoid using prompts that ask the model to perform a task for which it has a
known, fundamental limitation."* Two of this skill's own deliverables — not its runners' — land in
shapes measured far enough behind that handing them off beats trying harder.

| shape | where it lands here | measured |
|---|---|---|
| `static-page` | `orchestrator-hierarchy.html`: self-contained, inline CSS/JS, no build step, SVG dependency edges | 22 against opus's 67, a hard zero on 71% of decided rows |
| `regression-sensitive` | the serialized finalize — rebase, pre-merge gate, merge into an integration branch that currently passes, and resolving a conflict yourself in the worktree | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

A pointer rather than a pinned model, because the numbers move. **Omitted deliberately:**
`brownfield-integration`, since multi-file feature edits belong to runners rather than the
conductor and its one exception — a conflict resolved during finalize — is the row above; and
`visual-design`, since Phase 1's mock comparison is a judging call while the corpus is evidence
about a model *building*. `greenfield-module` and `algorithmic` (75 against 75), `accessibility`
(64 against 69) and `react-ui` (63 against 69) are level, so naming them would route away work
this family does as well as opus. Not permission to stop conducting: where no lane is free, the
block's value is naming what to distrust first — the hierarchy page's *bounds*, and the merge.

## What transfers intact

- **The three scheduler rules are already the right shape** — `A null return is a death, not a
  completion.` · `Never Promise.race an empty map.` · `done means merged.` Exit conditions rather
  than qualifiers, and the last is Override 3 in the skill's own words.
- **The retry ceiling is already a number** — `max 2 restarts, then park`, and `runner returned
  null ${n}x`. **[docs]** *"On *other* errors, you must change your strategy or arguments, not
  repeat the same failed call."* The skill's rule is the stricter one.
- **The four failure channels are a chain, not advice** — run record, event stream, token ratio,
  granted capability set, each with a number attached (36 occurrences in the event stream, none in
  285,950 lines of the log being read) — and the budget is a product with a cap, read rather than
  assumed: `slots × wave ≤ ~16`, `berths.py` every refill, 8 as the soft-fail.
- **The register is calm** — four shouted tokens across 845 scanned lines, each a plain rule with
  a stated consequence. **[docs]** Escalating language is where *"foundation model performance
  will no longer improve and in many cases will get worse."* Read them as plain rules, and keep
  the register out of the briefs you write.

## Override 1 — write the denominators down before Phase 1 (Phases 1, 3, 5)

`SKILL.md` names its scopes categorically — `Classify every item`, `Update it after every state
change`, `every item Done / parked-with-reason`, `keep every section` — each a set with a knowable
size that nothing states.

**[measured-family]** One run delivered **12 of 12** requirements its brief *enumerated* and
satisfied every requirement named *categorically* with one instance or none: all surfaces → 5, all
states → **1**, all menus → **0**, all flows → **0** (§1.1.1, n=1), while the skill it followed
stated six states and an explicit completeness condition in prose.

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."* The survey's inputs print their own denominator, so count them first — filled here
against a 23-item backlog as the exemplar:

| scope, in `ship-fleet`'s words | denominator | filled | reported |
|---|---|---|---|
| `Classify every item` | 23 = 11 ledger rows + 7 specs + 5 briefs | 23 | `23 of 23, 8 of 10 categories used` |
| deps · research · mock extracted per item | 23 × 3 = 69 | 64 | `64 of 69, 5 n/a: no mock exists` |
| ledger row per item | 23 rows × 10 columns = 230 | 230 | `230 of 230, 41 n/a: no worktree yet` |
| `every state change` written before acting | 47 events this run | 47 | `47 of 47 in the event log` |
| `every item Done / parked-with-reason` | 23 | 21 Done · 2 parked | `23 of 23 terminal, 2 with reasons` |

An unfillable cell reads `n/a: <reason>`. **[docs]** *"provide instructions for handling missing
data rather than assuming inserted data will always be present and well-formed."* And *"Gemini's
code execution tool enables the model to generate and run Python code, and should be enabled
whenever the model needs to perform any kind of arithmetic, counting, or calculation."*

## Override 2 — the runner brief is a prompt you are writing (Phase 5, scheduling §The runner prompt)

The highest-leverage override here, because the base template carries the exact sentence shape
that collapsed in §1.1.1: `must still represent the feature's ENTIRE UI — every surface, state,
user interaction, user flow, and popup/modal/menu`. Five categorical nouns in one clause, and the
measured outcome for that clause was 5 · 1 · 0 · 0 · one generic toast.

So fill the `⟨⟩` with enumerations rather than categories: the surfaces from the spec, the states
from the design system, the flows from the brief, each numbered and counted, with the handback
required to report the fraction — `18 of 20 states built, 2 n/a: no error path`. Same for
`Sources — read all that exist, in full`: list the paths, count them, ask for `N of N`.

**[docs]** *"We recommend to always include few-shot examples in your prompts."* and *"you can
remove instructions from your prompt if your examples are clear enough in showing the task at
hand."* So the brief ships one filled row of the coverage table it asks for, and the two lines the
skill says to carry verbatim — the git-identity rule, the never-strip-the-safeguards rule — are
copied rather than summarised: a paraphrase of a rule whose value is its exactness is another rule.

## Override 3 — every status carries the command that produced it (Operating discipline, Phases 0 and 2, Guardrails)

**[measured-family]** The §1.1.2 run (n=1) wrote itself a five-row review, all `PASS`, asserting a
named browser engine as verified when that engine had failed all four invocation attempts, and a
100% contrast pass rate from a probe never executed — measured afterwards, every primary button
was 3.65:1 and one glyph 1.00:1, invisible. Not dishonesty: a requested *shape* completed where
the procedure was not specified. `ORCHESTRATOR.md` is precisely such a shape.

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* and *"Verify your claims by quoting the exact applicable information (including
policies) when referring to them."* So the header contract ships as receipts, filled:

```
codex    2026-08-23 09:12 · perl alarm 600 codex exec -m gpt-5.6-sol … → OK
         log has model: gpt-5.6-sol · reasoning effort: medium → available
slots    2026-08-23 09:14 · $HM/berths.py → {"ceiling":10,"in_use":4,"available":6}
         budget = min(6 berths, 16 ÷ 4 waves) = 4 slots · measured, not assumed
egress   2026-08-23 09:12 · grep -rlE 'ANTHROPIC[- ]ONLY|…' CLAUDE.md … → no hit → lane on
merged   2026-08-23 11:40 · git branch --merged main | grep ai/mot-0042 → hit
lineage  2026-08-23 15:02 · capture-lineage.py design/ --gate → exit 0 (once per repo)
```

**A green exit proves what the gate checks, never what it does not.** **[measured-family]** On
`COD Dossier` an auditor validated tag counts, citation resolution and contrast floors thoroughly,
had no check that its prerequisite artifacts existed, and passed two skipped skill invocations
with exit code 0 (§1.2.2). Here: `git branch --merged` proves a merge and not a passing gate;
`berths.py` proves headroom and not that runners launched at that number; a codex probe answering
at fleet start proves nothing an hour later. The skill's own flagship gap says the rest — `a
verifier that exists but is never invoked verifies nothing` — so before a row turns `Done`, check
the verdict comment exists and record the oracle rung its evidence stood on. A denominator of zero
is a gate that never ran, never a pass.

## Override 4 — two attempts, then a different move (Phase 5 failure handling, the context contract)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."*

**[measured-family]** Both n=1 sessions ran the loop: one invoked a banned, absent tool four
consecutive times with nothing changed between attempts (§1.1.2); the other hit a 25,000-token
`Read` ceiling and retried four times with minor tweaks before pivoting to a Python split
(§1.2.3). `gemini-cli` ships a loop detector whose halt message names *"repetitive tool calls"*
(§7.2). Four `ship-fleet` errors look transient and are not; each pivots on attempt 1.

**A deep-research doc read `in full, not skimmed`** is §1.2.3's exact file class — that ceiling was
hit on a 28.6k-token research report — so chunk or line-range on the *first* capacity error, never
a second `Read`. **A held `.ledger.lock`** is wait-and-retry per the skill's rule, but past ten
minutes it is arbitration rather than a fifth attempt. **An empty codex `-o` file, or a log missing
`reasoning effort: medium`,** is a lane failure with a clean exit code: log the in-family downgrade
in the artifact and the ledger, and let a runner re-probe later. **A runner returning `null`** has
its counter already — park at three, and never write it to `done`.

## Override 5 — a named instrument becomes a path in the ledger (Phase 5, Guardrails)

**[measured-family]** §1.2.1 (n=1): a skill instructed that every design decision `goes through`
two named skills, and the run invoked neither — its own diagnosis being that the guidance was
already in context and nothing downstream depended on a file only those skills produce. The same
reclassification is recorded on the **Pro** tier (§7.2), so this conversion is worth doing at every
tier.

The scan found **0** qualitative skill references here — `ship-fleet` invokes by tool name — so
this override is `[derived]` from that mechanism rather than from a flagged phrase. Six named
instruments are conditional and produce nothing a later step reads. **[docs]** *"make each step a
prompt and chain the prompts together in a sequence."* Chain them by writing each output's path
into `ORCHESTRATOR.md` before the next step runs:

```
harbourmaster berths.py    → slots + timestamp in the header      (re-read every refill)
better-goal (unattended)   → docs/goals/goal-<slug>.md, path in the header, before slot 1
workflow-resume            → the recovered run id, in the event log, before any relaunch
capture-lineage.py --gate  → exit code + date in the header, once per repo
campaign.py export-warrant → the warrant path, in the final row, once at fleet end
whats-left                 → whats-left-<repo>.html, path under Needs input
```

A header row naming no path is the declaration §1.2.1 produced: compliant-looking text where a
tool call should have been.

## Override 6 — the caps are bounds, and bounds are the measured failure (Operating discipline, scheduling §The fleet)

**[measured-family]** Bounds are what this family exceeds rather than forgets: classifying every
failing UI assertion by whether it states a bound or asks for a thing, **58%** of Gemini's failures
at `medium` and **86%** at `high` were bound-shaped, against 8% for opus and 6% for the OpenAI
lane; one rule — `has exactly one soft elevation shadow` — failed on *every* card and *every* toast
in its set, on a run that passed 37 of its 39 other assertions (§2.2). A bound is violated by what
you did not write, so it survives every check that looks at what you did.

**[docs]** Google asks that *"all requirements, constraints, options, and preferences are
exhaustively incorporated into your plan."* So each cap becomes a row read back off what you
launched, never off `SKILL.md`:

| bound, in `ship-fleet`'s words | countable property | readback | observed | within? |
|---|---|---|---|---|
| `≤ 8 concurrent runners`, or berths if lower | agents live at once | `running.size` at each refill | 6 | yes |
| `slots × wave ≤ ~16` | the product this wave | slots × the wave width in the brief | 6 × 4 = 24 | **no — lean the waves** |
| one merge at a time | finalizes in flight | count them; serialize by construction | 1 | yes |
| `a runner touches only its own <ID>'s files` | out-of-scope paths per branch | `git diff --name-only main...ai/<id>` | 2 shared DS files | **no — fold back** |
| `max 2 restarts, then park` | restarts per item | the `attempts` map | 3 on MOT-0051 | **no — park it** |

Report `2 of 5 bounds within, 3 corrected`. A table filled from the skill rather than from what you
launched shows five greens, which is the failure itself rather than a report of it.

## Override 7 — the one thing you render, and the one you judge (Phase 3, Phase 1 mock comparators)

The `visual` module fired on four hits and is kept **narrowly**: `ship-fleet` is not a design
skill; it renders one artifact and judges rendered ones once per mock.

- **`orchestrator-hierarchy.html`** is generated *from* the ledger data, never maintained beside
  it. Denominator: one card per ledger row, one edge per dependency — open the file, count what
  rendered, report the fraction against the ledger's counts. It is the `static-page` shape above,
  so if you author it rather than route it, check its bounds first: one card per row, one legend,
  the `Updated:` stamp matching.
- **Phase 1's mock comparators** ask whether a mock is `more refined than` the app preview.
  **[docs]** *"Ask the model to describe the images before performing the task in the prompt."* and
  *"To improve the response, point out which parts of the image are most relevant to the prompt."*
  Name what is in each surface — surfaces, states, density — then judge. One comparison per mock,
  both opened, fraction reported; an unopened mock is `unknown`, never `not more refined`.

## Override 8 — read, then answer; recall is not the ledger (Resuming, the context contract)

**[measured-family]** §1.2.4 (n=1): asked a question naming three skills, the run answered from
memory without loading any of them; asked to fix that, it launched a skill instead of answering.
§1.1.4 records the adjacent failure — a previous-generation published value returned confidently.

**[docs]** *"Your knowledge cutoff date is January 2025."* and, from the strictly-grounded system
instruction's last clause, *"If the exact answer is not explicitly written in the context, you must
state that the information is not available."*

`ship-fleet` states both halves already: `ORCHESTRATOR.md exists → never re-survey from scratch`
and `After compaction: re-read it, the DESIGN md, and the ledger before acting`. Make them ordered
steps that never substitute for each other — read `ORCHESTRATOR.md`, run `git worktree list` and
`git branch --merged`, *then* reconcile and answer. A file or skill named in a message is loaded
before the answer is written; a status you cannot re-derive is reported as unavailable.

## Override 9 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios."* Conducting a fleet is multi-step planning, so `HIGH` is what
Google describes this work as needing; 3.7 Flash defaults to `MEDIUM`, and the uplift is unmeasured
on this corpus.

**[measured-family]** Do not raise it as a remedy for anything above: paired across 106 tasks,
`high` beat `medium` on 24, lost on 24 and tied on 58, mean **−1.7** points (§2.3), and the
bound-shaped share of failures *rose* from 58% to 86%.

**[docs]** *"Higher thinking levels encourage the model to use more tools to explore and verify, so
lowering the level can reduce tool calls."* — fewer tool calls is the wrong direction for a skill
whose characteristic error is a ledger row written without re-reading git.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and
response format, at the end of the prompt."*

1. Count the backlog before classifying it; report `N of N` at every phase boundary.
2. Enumerate in the runner brief what `SKILL.md` states categorically, and ship one filled row.
3. Every header field and status carries its command, that command's output and a timestamp.
4. One retry on a transient error; none on a read ceiling, an empty `-o` file or a held lock.
5. Each named instrument writes a path into `ORCHESTRATOR.md` that a later step reads.
6. Fill the bound table from what you launched; `done` means merged, and nothing else.
