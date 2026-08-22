# Model lanes — who does what, on which CLI, and what happens when a lane is down

> **Lane assignments are `defer`'s now.** Run
> `python3 <defer>/skills/defer/scripts/lane_pick.py --task <class> [--shape <shape>]`
> for the model, the effort and the exact argv, or `lane_run.sh <class> "<prompt>"`
> to run and wire-verify it in one step. The classes are `implementation`,
> `completeness`, `general`, `referral`, `verification` and `design-review`.
> **Pass `--shape` whenever you know what the work is** — `defer --matrix` lists
> the shapes. It narrows the class to the lanes measured good enough for that kind
> of work before headroom picks, which is where the cost saving lives; the two
> gated classes are `implementation` and `general`, and the judgement classes
> abstain by design. Three rules bind everywhere: `gpt-5.6-sol` never runs at
> `max` (it is the referral lane at `medium` and the implementation lane at
> `high`), Fable judges but never grades code or a ticket, and design review stays
> on Opus and Fable. What follows is this pipeline's reading of that policy, not a
> second copy of it.

**Canonical for the whole pipeline.** Every stage skill and both conductors point here for lane
assignments. Effort discipline (the second dial) is canonical in `model-and-effort.md`; per-lane
CLI mechanics are in `executor-lanes.md` and `codex-cli.md`. Change lane assignments here, once.

## The lane table

| Lane | Model | Harness | Effort | Notes |
|---|---|---|---|---|
| Conductor / orchestration | session model (Opus 5 / Fable 5) | in-session | high | Holds the map; never delegated |
| Triage verdict, plan synthesis, design direction | Opus 5 (`claude-opus-5`) or the session model when it is Opus/Fable-class | in-session or `claude` | high | Always a frontier Claude — these artifacts are amplified by everything downstream |
| Leaf readers, gate-runners, index scanners | cheapest session tier (haiku-class) | Workflow subagents | low | Read, report, stop |
| Evidence lenses, finding-verifiers | mid tier (sonnet-class) | Workflow subagents | low–medium | Structured work against an explicit oracle |
| **Implementation** | picked by measured capability for the slice's shape, then headroom | `codex` · `agy` · `grok` · `claude`+Perch | pinned per lane | `defer --task implementation --shape <shape>` picks. Name the shape (`executor-lanes.md`) — the lane that wins varies by 16 points across shapes, so a class-only call leaves that on the table |
| Implementation — Claude fail-back | claude-opus-5 | in-session | xhigh | Any executor lane failing routes work here — never to a sibling cheap lane, never dropped |
| **General** — neither referred nor a verdict | gpt-5.6-terra | `codex` | **high** | Mechanics in `codex-cli.md` §R3. Not `sol` at `medium`: that is the referral lane |
| Same-family validation (vs plan + tests) | claude-opus-5 | same CLI, fresh context | high | The writer's family checks the work against the plan before a stranger does; see `work` Phase D′ |
| **Task and same-family verification** | claude-opus-5 | `claude` | **xhigh** | The acceptance authority; see the `verify` skill. Fable does not do this |
| Verification fail-back | Opus 5 agents | `claude` | high | Recorded as a degraded (in-family) verification — see "What a degraded lane buys back" |
| **Referral** — spec/plan review gates, a fork put to another model | `gpt-5.6-sol` → `claude-fable-5` | `codex` · `claude` | **medium** · **high** | REVIEWER ≥ WRITER holds at every hop; sol never runs at `max` |
| **Completeness critic** | grok-4.6 · glm-5.3 · gemini-3.7-flash-high | `grok` · `claude`+Perch · `agy` | **xhigh** · high · high | out of Claude's family by construction |
| **Design review** | claude-opus-5 · claude-fable-5 | `claude` | xhigh · high | never leaves Anthropic's family |
| A single frontier judgement call | claude-opus-5 | in-session | max | Reserve it |

Two invariants govern every substitution:

- **REVIEWER ≥ WRITER.** For every artifact, the strongest reviewer is at least as strong as the
  strongest model that wrote it. Lowering a reviewer's *effort* keeps the invariant; lowering its
  *model* breaks it (`model-and-effort.md` §3).
- **VERIFIER ∉ WRITER's family.** The final acceptance verdict comes from a different model family
  than the implementation. This is an independence control, not a quality ranking: same-family
  judges measurably favour their own family's outputs (Anthropic's Petri observed GPT-5 judges
  rating GPT-5-family targets more leniently; a pre-registered 2026 cross-family re-grade found a
  17.6-point inflation from same-family self-grading — held loosely, but the direction is
  consistent across every source the research panel read). When every out-of-family lane is down,
  verification still runs — in-family — and is **recorded as degraded**, never silently promoted.

## Availability and fallback — a procedure, not a vibe

A lane is "available" when a cheap probe says so, not when you remember it working:

1. **Probe before first use in a session**: the binary resolves, `--version` answers, and — for a
   lane about to carry a gate — a parse-check invocation with an inert prompt exits clean.
2. **Wire-verify every run that matters.** The evidence a lane ran as routed is its own captured
   header/transcript, never the flags you passed — launch parameters have been observed not to
   stick. Grep the log for the model and effort lines; check the output file is **non-empty**. An
   absent or empty output file is a **lane failure, not a quiet pass** (a real gate once reported
   "no output — abandoned" after 10 minutes of exactly this).
3. **On failure** (binary missing, not signed in, usage/rate limit, empty artifact, deadline
   fired, repeated errors): record one ledger line — `<lane>: unavailable (<reason>) → <next>` —
   and take the next lane in the table. Availability failures are logged and routed around, never
   retried into the ground: one retry with the failure quoted, then move on.
4. **Never silently degrade below a family constraint.** Implementation lanes may fail all the way
   back to Claude. Verification lanes may not: an all-in-family verification is a *degraded* run
   (see below), and the completion artifact says so.

## What a degraded lane buys back

An `ANTHROPIC-ONLY` repo (the opt-out markers in `executor-lanes.md` §opt-out) or a day when every
out-of-family CLI is rate-limited leaves the pipeline all-Claude. That run is *correct* — the
opt-out is a policy, not a failure — but it loses the independence layer, so it buys back one
compensating control: the verification stage adds **one extra adversarial round with fresh
reviewers at `high` effort**, and the verdict comment carries `verification: in-family (degraded)`
so the reader knows which evidence class they got. Same-family review is weaker evidence, not no
evidence, and the artifact must say which it is.

## Recording

Every completion artifact (progress note or ticket comment) carries a **Reviewing models** line —
the wire-verified model per gate — so both invariants are checkable from the artifact, not from
memory. Never hardcode a dated model id in a self-check; write checks against the lane's expected
capability tier (`model-and-effort.md` §5).
