# The executor coding lanes — agy, grok, codex, and the Claude fail-back

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

Delegate mechanical, plan-scoped code writing to an external executor CLI, and spend the
session model on orchestration, verification, and fixes. This file owns the **shared** delegation
criteria, prompt contract, verify-fix loop, fallback, and accounting for every lane; per-lane
mechanics follow, and the Codex-specific harness lives in `codex-cli.md`.

## Picking the lane: name the slice's shape, then ask

There is no fixed lane order any more. Which executor is right depends on what the
slice **is**, and `defer` measured that over 106 tasks rather than assuming it:

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape <shape>
```

Read the shape off the plan you are already holding. The four that decide most slices:

| The slice… | `--shape` |
|---|---|
| edits code that already exists, spans more than two files, or has several acceptance criteria at once | `brownfield-integration` |
| adds a new self-contained module behind one acceptance surface | `greenfield-module` |
| must not break a suite, a public API or a live consumer that currently passes | `regression-sensitive` |
| builds a React component and its interaction states | `react-ui` |

`lane_pick.py --matrix` lists all eleven with their measured numbers. When a slice
genuinely spans two, name the stricter one — `brownfield-integration` and
`regression-sensitive` are the two where a wrong lane costs the most.

**Why the old fixed order went.** This file used to pin agy → grok → codex → Claude,
preferring agy for having "the highest tokens/sec of the set". Measured, that order
cost an average of **16 points** against the best lane available per shape, reaching
54 on a from-scratch page and 38 on regression-sensitive work, and its first choice
grades RED on five of eleven shapes. The throughput premise did not survive either:
per whole task, gemini runs 4.0 minutes against `gpt-5.6-terra@medium`'s 2.2 at half
the cost. The order was right on the three shapes it was tuned against — greenfield
modules, api surfaces, React components, where gemini is still the top lane — and
expensive everywhere else. Asking per shape keeps the wins and drops the losses.

Two things the router does that this file used to do by hand: it skips a lane that is
out of allowance, and it refuses a lane measured too far behind for that shape rather
than falling through to it. If you cannot classify the slice, omit `--shape` — the
router falls back to headroom alone, which is the behaviour this file had before.

**Two overrides the score matrix cannot see.** The bench scores one bounded task per
run, so it measures neither of these; both still hold:

- **A slice long enough to compact goes to the codex lane** whatever the shape says.
  Its post-compaction re-context harness (`codex-cli.md` §R3) re-injects the spec and
  plan verbatim after every compaction, and no other lane has an equivalent. A lane
  that drifts after compaction produces confident work against a forgotten spec, which
  is worth more than the few points a better-scoring lane would add.
- **The grok lane keeps its harness fallback** — the same model via `cursor-agent`
  when the grok CLI cannot run headless. An honest substitute, and the accounting says
  which harness ran.

**Claude remains the fail-back, unchanged.** Any lane failing for any reason routes to
the session model: never to a sibling cheap lane (a lane that failed on quality doesn't
get a stand-in carrying the same review debt), and never dropped or deferred because
the cheap path was down.

The **review gates are a different job and do not use `--shape`**: the out-of-family spec/plan
reviews and the completeness critic run per `second-opinion-lanes.md` and `codex-cli.md` §R1/R2
(codex `gpt-5.6-sol` at `medium` first, then agy, then grok). `defer`'s shape gate abstains for
those classes by design — the benchmark measures a model *building* something, which is no
evidence about how well it grades someone else's work. Don't apply this file's cost reasoning
to them either: an unavailable executor costs tokens; an unavailable reviewer costs evidence.

## Availability check (once per run, per lane you intend to use)

```bash
command -v agy && agy --version
command -v grok && grok --version          # PATH-order trap: a third-party npm package also
                                           # installs a `grok` binary; confirm it is xAI's
command -v codex && codex --version
command -v cursor-agent && cursor-agent --version
```

A missing lane → one ledger line (`<lane>: unavailable → <next>`) and the next lane. Don't
install unprompted. Flags below are verified against the versions on this machine at the time of
writing — **confirm against each CLI's `--help` before first use in a session**, and prefer what
`--help` says over this file.

## What to delegate (and what never to)

Delegate when ALL hold — the plan has already made the decisions, the executor just types:

- The plan specifies the change at file level (a component per an existing pattern, a route
  handler matching a template, repetitive wiring, test scaffolding from existing examples).
- The files involved fit comfortably in the executor's window alongside the context contract.
- Success is mechanically checkable (typecheck/tests/lint or a straightforward diff-read).

Never delegate: architectural or data-model decisions; security-sensitive code of any kind
(auth, secret custody, webhook signature verification, tenancy/authz boundaries, payment);
maker≠checker and idempotency logic; provenance-honesty judgment calls; contract-version changes;
cross-cutting refactors; merge-conflict resolution; e2e debugging; anything the plan marks
"investigate"; and **design work** (page assembly, composites, anything aesthetic — executor
design ability is weak; design routes per the `shipyard:design` skill). Two failed verify-fix cycles on a
task → take it back to Claude and note it; executor thrash costs more than it saves.

## Egress and the repo opt-out (checked per invocation)

Every external-lane call transmits the spec, the plan, and every file the executor opens to that
vendor — a sandbox flag restricts *writes*, not the network (a real fleet sent four auth files to
a vendor before anyone framed it as an egress decision). Before each invocation, grep
`CLAUDE.md` / `AGENTS.md` / `ORCHESTRATOR.md` for `ANTHROPIC-ONLY`, `NO EXTERNAL MODEL CLIS`, or
`external-model-clis: off`. A hit means Claude writes the code and the ledger reads
`<lane>: opted out (<file>) → claude`. Per-invocation because it is the only kill-switch that can
reach a run already in flight — a fleet cannot message its own inner workflow agents.

## Invocation — agy lane (preferred)

Run inside the feature's worktree so edits land on the branch:

```bash
cd "$WT" && perl -e 'alarm shift @ARGV; exec @ARGV' 1800 \
  agy -p "<prompt>" > "$WT/.executor/agy-<slice>.md" 2> "$WT/.executor/agy-<slice>.log"
```

Three agy facts that bite: **`--print` output buffers to the end** — never read its stdout for
progress, wait for exit; the model/effort selection follows the agy config — confirm the lane's
expected model in the captured output (`grep -i "gemini"` the log; a mismatch is `WRONG-MODEL`,
lane failure); and an empty output file is a lane failure, not a pass.

## Invocation — grok lane

```bash
cd "$WT" && perl -e 'alarm shift @ARGV; exec @ARGV' 1800 \
  grok -p "<prompt>" > "$WT/.executor/grok-<slice>.md" 2>&1
```

Harness fallback when the grok CLI can't run headless (auth prompt, TTY requirement):

```bash
cd "$WT" && cursor-agent -p --force --output-format json --model grok-4.6 "<prompt>"
```

(`--force` applies edits without confirmation — required in print mode; the final JSON's
`is_error: false` / `subtype: "success"` means *completed*, never *correct*. Confirm the model
name with `cursor-agent --list-models`; record `harness: cursor-agent` in the accounting.)

## Invocation — codex lane

`codex-cli.md` §R3 carries the full recipe (invocation, prompt contract, the mandatory re-context
harness and its self-test). The implementation model on this lane is **`gpt-5.6-terra` at
`medium`** — pass `-m` and the effort explicitly; a lane that silently inherits
`~/.codex/config.toml` defaults is not the lane you specified. The shape:

```bash
cd "$WT" && codex exec -m gpt-5.6-terra -c model_reasoning_effort="medium" \
  -s workspace-write --dangerously-bypass-hook-trust \
  -o "$WT/.codex/last-<slice>.md" "<prompt>" < /dev/null
```

## The prompt contract (every lane)

The prompt contains, with verbatim **absolute** paths, every time (an executor starts cold and —
under a worktree `-C`/`--cwd` — a relative `docs/...` resolves inside the worktree, finds nothing,
and the run quietly builds from the task description alone, looking successful and grounded in
nothing):

```
Read these files completely before writing any code:
  <ABS>/docs/specs/spec-<ID>.md (or the ticket text, pasted), <ABS>/docs/plans/<id>.md,
  <design mock index / DESIGN md>, <the repo's practices docs>.
Report one distinctive fact from the plan (its tier, its step count, this slice's file list)
so the caller can confirm the read landed.
Task: <the specific plan step(s), file list, and acceptance criteria>.
Follow the practices docs exactly; match surrounding code style; do not touch files outside
the listed set; do not edit shared design-system tokens/base elements.
IMPORTANT — your context window will compact on long tasks: after any compaction or
summarization, STOP and re-read the spec, plan, and design docs before continuing. The
on-disk files are your memory, not the conversation.
```

Keep each invocation to one coherent plan step. Many small runs beat one sprawling session —
cheaper retries, cleaner verification, far less compaction. On the agy and grok lanes the re-read
instruction is all you get (which is why it is in every prompt); the codex lane adds the
mechanical harness — prefer it for long slices.

## The verify-fix loop (the caller's half — identical for every lane)

After each executor invocation:

1. `git diff` — read the whole diff. Out-of-scope files touched → revert those hunks.
2. Run the repo gates that cover the change (typecheck, affected tests, lint).
3. Judge against spec/plan/design — correctness, not just compilation — and hold the slice to
   the self-certification bar in the `shipyard:work` skill (checklist rows at `file:line`, a real caller,
   the real-path exercise for critical seams).
4. Small gaps → fix directly (don't round-trip trivia). Substantive gaps → one executor retry
   with the failure quoted. Second failure → Claude rewrites; log `<lane>: reverted`.
5. Commit with the normal discipline once green (stage only files you created/modified — never
   `git add .`).

## Accounting and the kill-switch

Per item, per lane, never pooled: `<lane>: N tasks, M retries, K reverted (harness: <cli>)`.
An executor lane reverting more than roughly **1 task in 3** in a repo stops being used for that
repo — its work routes to Claude and the ledger says why. The whole justification for a lane is
savings net of verification; thrash erases it. Review gates are exempt (a reviewer that keeps
finding real defects is working) — track their *rejection* rate instead, and treat a reviewer
whose findings are mostly rejected as mis-prompted or under-grounded, worth fixing rather than
tolerating.
