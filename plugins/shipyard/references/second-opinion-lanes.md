# Second opinions and panels — settle it with a model before the human

**Canonical for the whole pipeline.** Triage, plan, design, and both conductors route open
decisions through this file. It carries the `clarify` skill's referral gate into the pipeline as
an ordered lane set plus a panel protocol, so the pipeline defers decisions to models instead of
stalling on a human — and so the deferral is evidence-shaped rather than vibes.

## The decision gate (run in order; the first step that resolves ends it)

1. **Look it up.** The conversation, the brief/ticket and its whole thread, the repo (CLAUDE.md,
   config, code that already made this decision once), work already done this session. A question
   about code you have not read is a substitute for reading. When you find it, use it and say
   where in one clause.
2. **Divergence test.** Sketch what you would build under each reading. Same sketch both ways
   means there is no question — pick the default, name it in a clause. (Measured: generating
   candidate solutions and asking only when they disagree lifted a code benchmark from 70.96% to
   80.80% — ClarifyGPT, FSE 2024.)
3. **Internal or external?** A gap is *essential* (human-only) only when ALL three hold: no safe
   default exists from any internal source; guessing wrong is expensive to undo; and the decision
   is genuinely the human's (taste, cost, scope, risk, compliance) or an external party's. Fail
   any one → it is internal: pick the obvious safe default, record it as an assumption naming the
   alternative it beat ("assuming X rather than Y"), and proceed.
4. **A model settles a technical question — this is a step, not an option.** Which design holds
   up, whether an approach has a flaw, which library fits this codebase: the human is not the only
   thing that can answer these, and is the most expensive thing that can. Use a lane (below), or a
   panel for the genuinely open forks. Note the scope: only forks that survived steps 1-3 reach
   here, so this is not every branching implementation detail.
5. **What survives reaches the human**: taste, cost, scope, risk tolerance, and their systems —
   plus the standing override: anything destructive, irreversible, outward-facing, or costly gets
   asked regardless, however certain you are and even when a conventional default exists. In an
   attended session, ask via `AskUserQuestion` in clarify's shape (batched, ≤3 questions, two
   options, consequence-not-mechanism wording, and **no `(Recommended)` mark unless the action is
   unrecoverable**, where it goes on the reversible path). In an unattended run, never block: park
   the item (`Needs More Info` with an "Easy reply" block, or a `proposed` row the human can mark
   approved) and continue with everything the question does not block.

**The step-5 test is whose axis it is, not how sure you are.** "If I can name a recommendation, I
take it" fails as a rule: you can nearly always name one, and a reason produced after the fact
converts the human's trade-off into your decision. Name what the losing option would have been
*better* at — nothing real means the call is yours, something real means the axis is theirs.

**Do not use a lane to avoid the thinking.** If you cannot say which option you would pick and
why, you are not ready to consult anyone — investigate first. And you still decide: a second
opinion is an input, not a verdict; forwarding two model answers to the user is the same
abdication as asking, with extra latency.

## The lanes (ordered; verified, not trusted)

Send the **evidence, not just the question** — the requirements, the constraints, the code paths.
A model asked "Clerk or WorkOS?" gives the blog-post answer; one given this codebase's constraints
gives a verdict on *this* codebase. Pin the model **and** the effort on every lane: a lane that
inherits its CLI config default is not the lane you routed.

```bash
# Lane A — a different Claude (fast; in-family)
claude --model claude-fable-5 --effort high -p "<question + evidence>"

# Lane B — a different family (default when independence is the point)
perl -e 'alarm shift @ARGV; exec @ARGV' 900 \
  codex exec -m gpt-5.6-sol -c model_reasoning_effort="high" \
  -s read-only -o /tmp/so-<slug>.md "<question + evidence>" < /dev/null \
  > /tmp/so-<slug>.log 2>&1
grep -qx "model: gpt-5.6-sol"     /tmp/so-<slug>.log || echo "WRONG-MODEL — lane failed"
grep -qx "reasoning effort: high" /tmp/so-<slug>.log || echo "WRONG-EFFORT — lane failed"

# Lane C — Google family (the effort is baked into the model id)
perl -e 'alarm shift @ARGV; exec @ARGV' 900 \
  agy --model gemini-3.7-flash-high -p "<question + evidence>" \
  > /tmp/so-<slug>-agy.md 2>/tmp/so-<slug>-agy.log

# Lane D — xAI family (efforts: xhigh|high|medium|low)
perl -e 'alarm shift @ARGV; exec @ARGV' 900 \
  grok -m grok-4.6 --effort xhigh -p "<question + evidence>" \
  > /tmp/so-<slug>-grok.md 2>/tmp/so-<slug>-grok.log
# fallback: cursor-agent -p --force --model grok-4.6 "<question + evidence>"
```

Lane rules (each one is a paid-for incident):

- **Verify the wire, not the flags.** The captured header lines are the evidence a lane ran as
  routed; launch parameters have been observed not to stick (a shipped gate once ran at `high`
  because one invocation dropped the flag). An **absent or empty output file is a lane failure,
  not a quiet pass.** A failed lane means you decide alone, and say so. Note that **codex
  validates neither `-m` nor `model_reasoning_effort`** — `-m bogus` prints `model: bogus` in the
  header and fails later at the API — so on that lane a clean header is necessary and not
  sufficient, and the empty output file is the signal that matters.
- **Bound every call** (`perl -e 'alarm …' 900`; no `timeout(1)` on macOS; codex has no timeout
  flag; exit 142 = deadline). Codex needs `< /dev/null` or it waits on stdin forever. Scope the
  packet small — `max` effort on an over-scoped review burns its turn budget and emits nothing,
  and that failure is the default outcome, not a rare one. On an empty result, narrow the packet
  before you widen the deadline.
- **`agy` buffers `--print` output to the end** — never read its stdout for progress; wait for
  exit.
- **Every out-of-family call is egress.** `-s read-only` restricts writes, not the network:
  everything in the packet and every file the lane opens is transmitted to that vendor. Check the
  repo opt-out markers (`ANTHROPIC-ONLY`, `NO EXTERNAL MODEL CLIS`, `external-model-clis: off` in
  CLAUDE.md / AGENTS.md / ORCHESTRATOR.md) **per invocation** — it is the only kill-switch that
  reaches a run already in flight. An opted-out repo runs in-family and logs it: a correct run,
  not a degraded one needing escalation.
- Pick the lane by what you need: **independence** → B/C/D (a different family does not share the
  blind spot — that is its whole value as an oracle); **speed** → A.

## Panels — for forks worth more than one opinion

Use a panel only at a high-leverage, genuinely open fork: a triage verdict on an ambiguous brief,
a plan-shape decision that everything downstream amplifies, a design direction, a verification
disagreement. Never for routine edits — panels at every step buy coordination failure, not
quality (the multi-agent failure literature's central finding).

Protocol, and each rule has a measured bias behind it:

1. **Three lanes from three families** (e.g. B + C + D; add A only as a fourth voice). Diverse
   panels outperform a single large judge and dilute intra-model bias — measured at roughly
   one-seventh the cost of a frontier single judge (PoLL, 2024).
2. **Blind and structural.** Each member gets the same packet: the fork, the evidence, the
   candidate options — no authorship attribution, no "which of these did Claude write", no
   scores out of 10. Ask for a verdict line plus the load-bearing reason:
   `VERDICT: <option>` / `REASON: <one sentence>`. Structural verdicts beat numeric scores, which
   collapse under position and verbosity bias (Shi et al. 2024; Zhou et al. 2024).
3. **Ask each member for the option you did not list.** One extra line in the packet: *is there a
   better approach than the ones here?* A missing option fails invisibly — the reader picks the
   least-bad listed one and nobody learns the set was incomplete — and an out-of-family model is
   the cheapest instrument that finds it. A panel that only ranks your options can only ever
   confirm your framing.
4. **Swap the order** of options between members (position bias is non-random and model-specific).
5. **Tally without dropping.** A member that returned nothing is counted as NONE and reported —
   a silent exclusion turns a broken harness into a clean-looking result. Majority decides;
   report the split per family.
6. **Disagreement is the signal, not noise.** A split panel on a high-severity fork is exactly
   the item that escalates to the human (attended) or parks as `Needs More Info` (unattended) —
   the panel just spent three model calls locating the genuinely hard decision, which is the
   cheapest thing that ever did.
7. **Record it**: one line in the artifact — `panel: B/C/D → 2-1 <option> (D dissented: <reason>)`
   — so the decision's provenance survives the session.

## Deep research (Dossier) — a different branch, not a higher rung

A fork that turns on external facts (market norms, a vendor's real behaviour, prior art) is a
research question, not an opinion question. Residual uncertainty about a *design* call is not:
sending that to Dossier buys latency and a bill rather than an answer.

Free lane first, paid on purpose:

1. `research_plan` — free, shows the panel it would assemble and what it would cost.
2. `research_local_start` → `research_local_note` → `research_local_submit` — free; the loop runs
   on your own web search. Right when the answer needs sourcing but the decision is not
   load-bearing enough to buy.
3. `research_start` with no provider — assembles the free-CLI + paid panel, roughly $1-3 at
   `fast` and $3-7 at `max`. Say the estimated cost in the ledger line.

Export and **read the reports in full**, run `research_verify_citations` before relying on a
finding (a resolving URL is not a supporting one), and write the report to the repo's
`docs/deep-research/<slug>.md` so the brief can point at it. Support is counted in independent
domains, never in how many backends agree.
