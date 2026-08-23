# gemini.md — `shipyard`

Read this once, now, then read `SKILL.md` and answer from it. Each override names the section it
lands on.

`shipyard` is a map, not a machine. It has one job — say which stage fits a situation and point at
the shared canon — and one rule that everything else rests on: `It never performs a stage itself.`
That combination is the specific risk. A model that has read this file has the pipeline's shape in
context, and the shape is enough to write a plausible triage verdict, a plausible plan, a plausible
status move, without ever invoking the skill that owns them. So the failure to design against is not
a wrong route. It is a confident, well-formed answer about the pipeline that was recalled rather
than read, or a stage quietly performed here rather than handed over.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]` — **no Gemini run
  of `shipyard` has been observed**, at any tier. The `[measured-family]` sources are two single
  sessions (n=1 each) and a 106-task benchmark, in `geminify/references/evidence.md`.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — **flash-tier claims, not to be projected onto the Pro
  tier.** **[docs]** The defaults drift inside the family: *"If thinking_level is not specified,
  Gemini 3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking
  effort is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand
  as `[docs]`-grounded discipline; every `[measured-family]` number is an open question.
- **Unmeasured on this skill:** both measured sources watch a model *build* something, and this
  skill builds nothing — so **nothing here measures routing accuracy at all**. The overrides are
  about completeness and grounding, where the evidence does speak, and about the one behaviour
  §1.2.4 recorded directly (answering a question about named skills from memory). Also unmeasured:
  the retry rule on a lookup-shaped skill, and any run measured *with* a `gemini.md` against one
  without.
- **The self-limitation.** **[docs]** A conditional side file is the shape the health checklist
  warns about: *"Avoid writing a prompt with non-linear logic or conditionals that require the model
  to piece together fragmented instructions from multiple different places in the prompt."* Read it
  in one pass, before answering, never mid-answer.

## No route-out block, and which shapes were omitted

**[docs]** The health checklist says it outright: *"Avoid using prompts that ask the model to
perform a task for which it has a known, fundamental limitation."* No shape can honestly be named
here. This skill `routes and explains`; the four shapes the corpus measured far enough behind to
route out — `static-page`, `brownfield-integration`, `visual-design`, `regression-sensitive` — all
describe *producing* an artifact, and this one produces a sentence naming a stage. `lane_pick.py`
returns the policy answer unchanged for the judgement classes anyway. Where routing out belongs is
one layer down: `work` carries the two shapes that matter and the command that picks the lane, on
that stage's own account.

## What transfers intact

Three of this skill's rules are already written the way this family needs.

- **`The status machine (one enum, complete)`** names the enum and calls itself complete. A count
  that is claimed complete is an objective constraint, and **[docs]** the **Ambiguity** entry is why
  those survive on this family when prose around them does not: *"Avoid using subjective or relative
  qualifiers that lack a concrete, measurable definition."*
- **`Only verify sets Done`** is a bound stated as a fact rather than a preference — exactly one
  setter, no exceptions, nothing to weigh.
- **`Prefer a conductor whenever the goal is a finished feature rather than one stage's artifact`**
  is a closed set with a stated default across three named options. **[docs]** That is the
  multiple-choice remedy: *"The response is correct, but the model didn't stay within the bounds of
  the options."*

## The scan

`scan_skill.py` over `SKILL.md` (50 lines): **1 quota candidate, 0 bound rows, 1 relative qualifier,
0 qualitative skill references, 0 shouted passages.** No module reached the three-trigger threshold,
so this file is **core only** — no capture protocol, no gate section, no delegation cap, because
this skill renders nothing, ships no probe and spawns nothing. The single quota row (`Every
transition`) is row 3 of the ledger below; the other four rows are hand-added, because the scanner's
deliverable vocabulary does not contain `stage`, `status` or `reference`. The ledger is the scan
plus a read, never the scan alone. The `0 bound rows` is honest about the regex and not about the
skill: `Only verify sets Done` and `It never performs a stage itself` are bounds phrased as
prohibitions, and they are carried in overrides 2 and 3 rather than invented into a ledger row.

## Override 1 — the map is a count, and a partial map reads as a complete one

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."* **[measured-family]** Why this comes first: one run delivered **12 of 12**
requirements a brief *enumerated* and satisfied every requirement named *categorically* with one
instance or none — all surfaces → 5, all states → **1**, all menus → **0**, all flows → **0**
(§1.1.1, n=1). A router's whole output is enumerations, and an enumeration missing two rows reads
exactly like one missing none.

Fill this before answering any question about the pipeline's shape; report the fractions only when
the answer claims to be complete:

| # | categorical, in the skill's words | denominator | filled | reported |
|---|---|---|---|---|
| 1 | `Seven stage skills` in the stages table | 7 | intake · triage · plan · design · work · verify · gap-fix | `7 of 7` |
| 2 | `The status machine (one enum, complete)` | 8 states | (untriaged) · Needs More Info · To Do · Ready for AI · In Progress · Developer Review · Done · Needs More Work | `8 of 8` |
| 3 | `Every transition requires its artifact` | 8 arrows in the enum | each named with the artifact that gates it | `8 of 8 gated` |
| 4 | `the shared canon` in `references/` | 8 files in that paragraph + `tracker-adapter.md` | model-lanes · second-opinion-lanes · evidence-rules · test-strategy · executor-lanes · codex-cli · operational-rules · evidence · tracker-adapter | `9 of 9 named` |
| 5 | the conductors above the stages | 3 | ship-feature (one feature) · ship-fleet (a backlog) · ship-armada (a portfolio) | `3 of 3` |

A cell that cannot be filled reads `n/a: <reason>` — **[docs]** *"provide instructions for handling
missing data rather than assuming inserted data will always be present and well-formed."* Row 2 is
the one to guard: the skill calls that enum **complete**, so an answer listing six states is not a
short answer, it is a false one.

**And the tension this creates with the family's default.** **[docs]** *"By default, Gemini 3 models
provide direct and efficient answers. If you need a more conversational or detailed response, you
must explicitly request it in your instructions."* That default is right for this skill — a router's
answer should be two sentences, not four pages. Brevity trims **prose**, never **rows**: cut the
explanation, keep the count.

## Override 2 — read the canon, then answer (`## The status machine`, `## The shared canon`)

This is the override that matters most on this target, because a router is a question-answering
surface and the recorded failure is precisely about answering questions.

**[measured-family]** §1.2.4 (n=1) recorded both halves failing in one session. Asked a question
naming three skills, the run produced prose analysis from internal memory **without loading any of
them**; asked why, it confirmed it had pattern-matched the prompt as a conversational reasoning
question. Then, asked how to fix that, it inverted the error — launching a skill instead of
answering, and being interrupted with a request for the answer. There is no stable mapping from
*named in the prompt* to *loaded before the answer*, so make it two ordered steps: **read what the
prompt names, then produce the answer yourself.** Never one without the other, and never the
invocation as a substitute for the answer.

Concretely, for this skill:

- A question about statuses, transitions or the two substrates is answered from
  `${CLAUDE_PLUGIN_ROOT}/references/tracker-adapter.md`, opened now. It carries the markdown-lane
  surface forms (`To Do` ↔ `Ready for Plan`, `Ready for AI` ↔ `Ready for Work`, `Developer Review` ↔
  `In Review`) that a remembered answer reliably flattens.
- A question about lanes, effort or a second opinion is answered from `model-lanes.md` and
  `second-opinion-lanes.md`, both of which open by saying the assignments are `defer`'s now — so a
  lane table quoted from memory is quoting a layer that has moved.
- **Which lane this repo is on is read, not assumed.** `tracker-adapter.md` says to resolve the
  substrate once and `State it in your first status line`. Whether a tasks MCP is configured is a
  fact about the repo in front of you.
- **[docs]** *"Your knowledge cutoff date is January 2025."* A stage list you remember is a stage
  list from a version of this plugin you have no way to date.

## Override 3 — point at the stage; never perform it (`# Shipyard — the map`)

The scan's `0 qualitative skill references` is what makes this necessary, not unnecessary.
**[measured-family]** §1.2.1 (n=1): a skill instructed that every design decision `goes through` two
named skills, and the run invoked **neither** — its own diagnosis being that the rules were already
in context and nothing downstream depended on a file only those skills produce, so it treated the
instruction as a standard satisfied by writing compliant output. Corroborated outside this repo
(§7.2) by a Gemini 3 **Pro** transcript reclassifying a `GEMINI.md` rule as a general guideline, so
this binds on every tier.

`shipyard` creates that exact condition. Reading the map puts enough of the pipeline in context to
improvise any stage's artifact, and an improvised triage verdict looks like a triage verdict. The
skill's own sentence is the rule — `It never performs a stage itself` — and the mechanical form of
it is that **each stage is a real invocation whose completion is a path**:

```
intake   → docs/features-to-triage/<slug>.md      triage opens it
triage   → the verdict section/comment            → To Do        ; plan opens it
plan     → docs/plans/<id>.md, committed (sha)    → Ready for AI ; work opens it
design   → design/mocks/<ID>/INDEX.md             (parallel with plan)
work     → the branch in .worktrees/<ID> + tables → Developer Review
verify   → the per-requirement verdict comment    → Done | Needs More Work
gap-fix  → the gaps closed in code                → back to Developer Review
```

**[docs]** The remedy Google names for a multi-step task is the same shape: *"make each step a
prompt and chain the prompts together in a sequence."* A missing artifact means the stage did not
run, whatever the transcript says — which is the skill's own line, `Every transition requires its
artifact`, promoted into the thing that decides whether the next stage may begin. Two bounds ride
with it, both phrased as prohibitions and both meaning a count: **exactly one skill sets `Done`**,
and **exactly zero stages are performed here**.

## Override 4 — two attempts, then a different move

**[docs]** *"On other errors, you must change your strategy or arguments, not repeat the same failed
call."* **[measured-family]** Both n=1 sessions ran the loop: one invoked a banned, absent tool four
consecutive times with nothing changed between attempts (§1.1.2); the other hit a 25,000-token
`Read` ceiling and retried four times with minor tweaks before pivoting to a Python split (§1.2.3).
Two failures here pivot on **attempt 1**. **A missing reference file** — `${CLAUDE_PLUGIN_ROOT}`
unset in a spawned agent is the ordinary cause — is resolved by locating the plugin root once rather
than re-reading the same absent path; say plainly which file you could not open. **A reference over
the `Read` ceiling** takes line-ranged reads on the first refusal, not a fourth offset tweak.

## Override 5 — `thinking_level`, and why this one does not need `HIGH`

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios."* **This skill is none of those.** It is lookup-shaped: read a
situation, match it to one of seven rows, name the stage and the artifact. `MEDIUM` — Gemini 3.7
Flash's default — is the right level here, and the honest note is that raising it buys nothing:
**[measured-family]** paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on
58, mean **−1.7 points** (§2.3). **[docs]** *"Higher thinking levels encourage the model to use more
tools to explore and verify, so lowering the level can reduce tool calls."* — and here the tool
calls that matter are the four or five reference reads override 2 asks for, which are cheap and
should happen at any level. Where the work turns out to be a whole feature rather than a routing
question, the answer is to hand it to a conductor, not to think harder about it in this skill.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Seven stages, eight statuses, eight transitions, nine canon files, three conductors — an answer claiming completeness carries the count.
2. Read `tracker-adapter.md`, `model-lanes.md` and `second-opinion-lanes.md` before answering about statuses or lanes; a remembered map is undated.
3. Read what the prompt names, then answer. Neither substitutes for the other.
4. Name the stage and its artifact; never produce that artifact here. Exactly one skill sets `Done`.
5. `MEDIUM` is the right level for this skill; a routing question that turns out to be a feature goes to a conductor.
