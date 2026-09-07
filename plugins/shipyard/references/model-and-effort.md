# Model, effort, and what still needs verifying — the pipeline-wide calibration

**Canonical for the whole pipeline.** Every stage skill and both conductors point here rather than re-deriving this; the Codex lane's own mechanics stay in `codex-cli.md`, and the fleet's launch/propagation mechanics stay in ship-fleet's `references/scheduling-and-concurrency.md`. Change it here.

Three things in this pipeline were calibrated against an older model generation and are worth re-reading before a long run: which dial you turn to control spend, how much of the built-in verification is still buying anything, and how long the written artifacts should be.

## 1. Two dials, not one

Every routed agent has **two** independent settings, and the lane tables historically named only the first:

- **Model** — the capability class (haiku → sonnet → opus, or sideways to an out-of-family reviewer).
- **Effort** (`low` / `medium` / `high` / `xhigh` / `max`) — how much work the model does *inside* that class. It is a model-specific reasoning control rather than a token cap. Supported values and effects depend on the model and harness. For Opus 5, lowering effort reduces thinking but does not reliably shorten visible responses; specify response length separately.

Opus 5's API default is `high`; a CLI, proxy or agent harness can choose a different default. Read the selected harness's supported settings and observe the run before assigning an effort value. Do not extrapolate this default to Gemini or GPT.

## 2. Opus 5 effort starting points

These are task-shaped starting points to evaluate, not universal settings for Gemini, GPT or every harness. Use only supported values and explicit user preferences; lower effort retaining quality on one review does not establish it for another.

| Lane | Effort | Why |
|---|---|---|
| Leaf readers, gate-runners, ledger/index scanners | `low` | This is the level built for subagents: read, report, stop. Fewer tool calls is the point, not a side effect |
| Evidence lenses (clause table, reachability, UI fidelity), finding-verifiers, mechanical checks | `low`–`medium` | Structured work against an explicit oracle. Review accuracy holds up at lower effort, so a table gets filled just as well and far cheaper |
| Synthesis, judgement lenses (security / guardrails / client-asserted identity), conflict resolution, plan synthesis | `high` | The default, and the floor for anything whose miss amplifies downstream |
| Feature runners and other long-horizon agentic work (>30 min, multi-phase, million-token budgets) | `xhigh` | The level built for exactly this shape. Pair it with a large `max_tokens` — start at 64k — or the run truncates mid-phase, since `max_tokens` caps thinking **plus** response text |
| A single genuinely frontier judgement call | `max` | Reserve it. On ordinary work it adds cost for small gains and can overthink structured tasks |

**Effort is the primary cost dial; model is the second.** Step effort down before you step capability down — a strong model at `low` costs less than it looks and stays in its capability class.

## 3. Reviewer capability is task-specific

`REVIEWER ≥ WRITER` is shorthand for choosing a reviewer capable of evaluating the artifact at its actual complexity. It is not a total ordering across model families or a guarantee from a newer name. Establish task suitability and the required family independence separately. Two consequences:

- **Measure review quality at the proposed effort and model.** Lower effort may retain quality for a bounded review, but it is not a proof. Choose a capable reviewer with the required family independence and re-evaluate when the model or task changes.
- **A fast pass and a thorough pass are both available.** Review accuracy holds at lower effort, which licenses a cheap early sweep (a `low`-effort lens over each slice as it lands) and one `high`-effort pass at the end — rather than one expensive pass that arrives too late to be cheap to fix.

## 4. Operating rules for effort

- **Set it explicitly at spawn.** Never rely on a default you didn't choose, and never pass `adaptive` as an effort value — that is a thinking mode, not a level.
- **Hold it constant for the life of an agent.** Effort is part of the rendered prompt, so changing it between requests forfeits the prompt-cache prefix. Vary effort *across* lanes, never *within* one agent's conversation.
- **Re-sweep, don't inherit.** Effort settings tuned on an earlier model generation don't transfer. When the session model changes, re-measure a lane's quality at one level down before assuming the old setting is still right.
- **Raising effort is the fix for shallow work, not more prompting.** If a lane keeps under-reasoning, raise its effort before you add instructions telling it to try harder.

## 5. Never hardcode a dated model id

Resolve the requested display name to an exact supported model selector, then compare requested, resolved and actual serving identities where authoritative execution metadata exposes them. Do not hardcode an obsolete selector or replace exact routing evidence with a broad tier-name self-check. A newer model can be a valid authorized substitute, but requires recording the substitution rather than silently passing a family-name check. A model's self-description and a CLI header echoing flags are not wire evidence.

## 6. What still needs verifying — oracle checks vs re-reading your own work

The pipeline's verification is deliberately heavy, and most of it earns its place. But the two kinds are worth separating, because only one of them is still buying something:

**Oracle checks — always run, never infer.** These acquire evidence the model cannot produce by thinking:
- Actually running the gates (typecheck, codegen, validate, lint, the e2e suite).
- **Exercising the real, un-stubbed path** — round-tripping a persisted write, calling the endpoint, rendering the page, feeding a hostile input.
- Filling the Clause and Reachability tables with real `file:line` values, which is falsifiable in a way "I reviewed it" is not.
- The out-of-family review gates. An author-judged oracle catches what a same-family reviewer shares the blind spot for; that argument is unaffected by any model improvement within the family.
- The mechanical path check on a plan's referenced files.

**Self-re-reading — fold it in, don't stack it.** A separate pass whose only job is the model re-reading its own diff and asking "is this right?" now largely duplicates work the model does inside the phase, and stacking it costs tokens without adding recall. Concretely:
- The per-phase gate is a **conformance** check against the plan and the spec — did this phase drift from, drop, or half-build a stated requirement? Keep that, and keep it evidence-shaped (name the clause, name the `file:line`). What it should *not* become is a general "review your work again" round on top of the phase that just reviewed itself.
- **Don't spawn an agent to re-check findings you just produced**, and don't add a verifier layer above a verifier.
- **Adversarial finding-verification is a precision filter, so aim it where a false positive is expensive** — a Critical, a finding whose fix is a structural change, anything that would reverse a locked decision. Verifying every Low 1:1 spends a whole agent to avoid a cheap edit; current review passes already carry high precision, so the blanket 1:1 pass is the part to trim, not the Criticals.
- The rule that survives all of this: **never report a gate you did not run**, and never merge "the lint passed" into "it is verified" — those are two claims and the second one requires the real path.

## 7. Length calibration for the written artifacts

Written deliverables run long by default, and this pipeline produces a lot of them. Length is a constraint to design to, not an outcome to accept:

- **Plans** get the length their tier allows (`plan-tiers.md`), and a 10-line diff gets a ~30-line plan. Padding a plan with empty sections is worse than omitting them — a downstream phase treats every section as work.
- **Progress notes, gate notes, and completion comments** carry the tables, the counts, the assumptions, the drops, and the gate results. They are not a narrative of the run.
- **Triage review sections** stay short and non-technical; the Assumptions block is a list of decisions, not an essay defending each one.
- **`ORCHESTRATOR.md`** is a resumable state file. Rows and status, not prose.
- **Your own turn-by-turn output** is thinner still: one line before the first tool call saying what you're about to do, an update only when you find something material or change direction, and an outcome-first close. A recap of the phases the user just watched scroll past is not a report.
