# Model lanes — who does what, on which CLI, and what happens when a lane is down

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
| **Implementation — preferred** | gemini-flash-3.7 | `agy` | high | Preferred for throughput (high tokens/sec); see `executor-lanes.md` §agy |
| **Implementation — fallback 1** | grok-4.6 | `grok` (harness fallback: `cursor-agent`) | high | Same model through a different harness is an honest substitute — say which harness ran |
| **Implementation — fallback 2** | gpt-5.6-terra | `codex` | medium | Mechanics in `codex-cli.md` §R3 |
| **Implementation — fail-back** | session model (Claude) | in-session | high | Any executor lane failing routes work back to Claude — never to a sibling cheap lane, never dropped |
| Same-family validation (vs plan + tests) | same family as the implementer, equal-or-stronger tier | same CLI, fresh context | high | The writer's family checks the work against the plan before a stranger does; see `work` Phase D′ |
| **Cross-family verification** | gemini / gpt / grok — MUST differ from the implementer's family | `agy` / `codex` / `grok` | high–max | The acceptance authority; see the `verify` skill |
| Verification fail-back | Opus 5 agents | `claude` | high | Recorded as a degraded (in-family) verification — see "What a degraded lane buys back" |
| Spec/plan review gates, completeness critic | out-of-family, ordered: `codex gpt-5.6-sol` → `agy` → `grok` | per `second-opinion-lanes.md` | max (gates) / high | REVIEWER ≥ WRITER holds at every hop |
| A single frontier judgement call | strongest available | in-session | max | Reserve it |

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
