# The Codex lane — `gpt-5.6-sol` via the Codex CLI

The pipeline's **cross-family** lane. Everything else in this pipeline is Claude reviewing Claude, and an author-judged oracle is how a whole family's blind spot ships green. Codex runs `gpt-5.6-sol` from a genuinely different model family, so it gets the three jobs where independence (or cheap, well-specified typing) is worth more than familiarity:

| Role | Effort | Sandbox | What it does |
|---|---|---|---|
| **R1 — Spec / plan review** | `max` | `read-only` | Logical + technical review of `spec-<ID>.md` / `plan-<ID>.md` against the real codebase, at the triage and plan gates |
| **R2 — Completeness critic** | `max` | `read-only` | **Replaces** the Claude completeness critic that closes the work skill's Phase D acceptance review |
| **R3 — Implementation executor** | `medium` | `workspace-write` | Writes plan-scoped code in the feature worktree, under Claude's verify-fix loop |

R1 and R2 are **mandatory where Codex is available and the repo has not opted out** — they are verification, not cost optimization. R3 is an executor lane like the ones in `executor-lanes.md`, and is subject to the same verify-fix loop, kill-switch, and fallback rules.

Availability and the repo opt-out are the *only* licensed reasons to skip any of them (see "Fallback"). "It looked fine" is not.

## Read this first — every Codex call is data egress

**`-s read-only` restricts WRITES. It does nothing about network egress.** A read-only reviewer still transmits your prompt and the full text of every file it opens to OpenAI. On a plan review that means the spec, the plan, and every source file the prompt tells it to check — which, for a security feature, is exactly the code you would least want to send: auth guards, session handling, origin checks, the threat model.

This bit a real fleet: a plan-review gate on an OAuth feature sent `lib/auth/require.ts`, `lib/auth/session.ts`, `lib/auth/guest.ts` and `proxy.ts` to OpenAI before anyone framed it as an egress decision. The sandbox flag reads like a safety property and is not one, in this dimension.

So treat the lane as a **disclosed default, not an invisible one**: it is on unless the repo says otherwise, and the repo gets a first-class way to say otherwise.

### The repo opt-out (checked before EVERY invocation, not once)

Before any `codex` call, grep the repo's own policy documents for an opt-out marker:

```bash
grep -rlE 'ANTHROPIC[- ]ONLY|NO EXTERNAL MODEL CLIS?|external-model-clis:\s*off' \
  CLAUDE.md AGENTS.md ORCHESTRATOR.md docs/CODING_PRACTICES.md 2>/dev/null
```

Any hit ⇒ **this repo is opted out.** Every role falls back in-family (R1/R2 → the Claude reviewer, R3 → Claude writes the code), and you log the reason as `codex: opted out (<file>) → claude`. Do not argue with it, do not ask for an exception mid-run, and do not treat it as a degraded run needing escalation — an opted-out repo running fully in-family is a *correct* run.

**Check it per invocation, not once at startup.** This is the only kill-switch that reaches an agent already in flight: a fleet cannot message its own inner workflow agents, so an owner who bans external CLIs mid-run has no way to stop them except a file the next invocation re-reads. A once-at-startup check would let every in-flight runner keep shipping code to OpenAI for hours after the policy landed. The grep costs milliseconds; run it every time.

Adding the marker to `CLAUDE.md` (or `ORCHESTRATOR.md` for a fleet) is the supported way to turn the lane off for a repo, permanently or mid-flight.

## Availability check (once per run)

```bash
command -v codex && codex --version                       # expect codex-cli 0.145.0+
codex exec -m gpt-5.6-sol -c model_reasoning_effort="max" \
  -s read-only --skip-git-repo-check "Reply with exactly: OK" < /dev/null
```

A non-zero exit, an auth prompt, a usage-limit / rate-limit message, or a missing binary → the lane is **unavailable**: record it explicitly and route that role back to Claude (see "Fallback"). Don't install unprompted; offer `npm i -g @openai/codex` or the Codex desktop app, and `codex login` for auth.

**Always pass `-m` and `-c model_reasoning_effort` explicitly — then VERIFY them on the wire.** `~/.codex/config.toml` carries the user's own `model` / `model_reasoning_effort` / `sandbox_mode` defaults, and a role that silently inherits `high` instead of `max`, or `danger-full-access` instead of `read-only`, is not the role you specified. This is not hypothetical: a shipped plan-review gate ran at `high` because one invocation dropped the flag, and nothing caught it until the session log was read afterwards.

Codex prints its resolved settings in a header, so the check is cheap. Capture the run and assert:

```bash
codex exec … "<prompt>" < /dev/null > "$LOG" 2>&1
grep -qx "model: gpt-5.6-sol"   "$LOG" || echo "WRONG-MODEL — treat as lane failure"
grep -qx "reasoning effort: max" "$LOG" || echo "WRONG-EFFORT — treat as lane failure"
```

This is the same wire-level verification the pipeline already applies to every routed model lane — launch parameters have been observed not to stick, so the header is the evidence, not the command you typed.

Three more invocation details that bite:
- **`< /dev/null` on every call.** With stdin open, `codex exec` prints `Reading additional input from stdin...` and waits for input it will never get.
- **`-o <file>` to capture the verdict** — and then **check the file is non-empty.** `--output-last-message` only gets written when the run produces a final assistant message. A run that exits on its turn budget writes **nothing**, and an absent or empty file is a lane failure, not a silent pass. A real gate lost 10 minutes to exactly this and reported "no output — abandoned".
- **Bound the wall clock.** `codex exec` has no timeout flag and macOS has no `timeout(1)`; use perl's alarm, which is present everywhere:
  ```bash
  perl -e 'alarm shift @ARGV; exec @ARGV' 600 codex exec … < /dev/null > "$LOG" 2>&1
  ```
  Exit 142 means the deadline fired. **Never poll a Codex run in an unbounded loop** — a blocked runner holds a fleet slot doing nothing, and one gate cost ~15 minutes of a slot across two attempts before returning anything at all.

Flags below are verified against codex-cli 0.145.0 — confirm against `codex exec --help` before first use and prefer what `--help` says over this file.

## R1 — the spec / plan review gate (`max`, read-only)

Run **after** the artifact is written and **before** the status flips. Codex reads the repo, so its review is grounded in the same code the plan claims to build on — that is the point: it catches the plan that references a file that doesn't do what the plan says.

```bash
perl -e 'alarm shift @ARGV; exec @ARGV' 600 \
  codex exec -C "<repo root>" -m gpt-5.6-sol -c model_reasoning_effort="max" \
  -s read-only -o /tmp/codex-review-<ID>.md "<prompt>" < /dev/null \
  > /tmp/codex-review-<ID>.log 2>&1
```

`-s read-only` is load-bearing for one thing only: the reviewer must not be able to "helpfully" fix the artifact it is reviewing — you apply the changes, so you stay accountable for them. It is **not** a privacy control; see "every Codex call is data egress" above.

**Keep the review scope small enough to finish.** `max` effort on a large artifact plus a dozen source files plus web search will burn its turn budget and emit nothing — the failure is not rare, it is the default outcome for an over-scoped review. Name the artifact and **the handful of files whose claims actually need checking**, not every file the plan mentions. If a plan is big enough that one review can't cover it, run two narrower reviews (say, security clauses and then completeness) rather than one that dies at the end and returns nothing.

**The effort ladder, when a run returns nothing.** Do not retry `max` unchanged and do not silently drop to `high`:

1. `max` with a 600s deadline. Non-empty output → done.
2. Empty output or deadline → retry **once** at `high`, with the scope **narrowed** (fewer files, fewer questions). Record this in the gate note as an explicit, logged downgrade — `high` is not what the gate specifies, so a reader must be able to see they got the cheaper pass.
3. Still nothing → the lane has **failed**, not "returned clean". Fall back in-family per "Fallback" and log it. A gate that produced findings but never emitted its verdict line is **PARTIAL**: treat its findings as evidence, and never treat the missing verdict as a pass.

The prompt must be self-contained — Codex starts cold and shares no memory with you:

```
Read these files completely, then review:
  docs/specs/spec-<ID>.md            (the spec: original feature description + triage assumptions/answers)
  docs/plans/plan-<ID>.md            (the implementation plan — omit at the triage gate, it does not exist yet)
  <root DESIGN md>, docs/CODING_PRACTICES.md, docs/NEW_PROJECT_BEST_PRACTICES.md (if present)
You are a LOGICAL and TECHNICAL reviewer from a different model family than the author.
Ground every claim in the actual codebase — open the files the artifact names and check them.
Report, each as: SEVERITY (Critical/High/Medium/Low) · location · the defect · the recommended change.
  1. Logical defects — internal contradictions, a step that cannot follow from the one before it,
     circular dependencies, an ordering that cannot work, an assumption that contradicts another.
  2. Technical defects — a named file/function/component that does not exist or does not do what the
     artifact claims; a wrong analogue; a missing dependency, migration, or codegen step; an
     interface/contract mismatch against the real code.
  3. Completeness — a requirement in the feature description or triage answers that the artifact
     never addresses, or silently shrinks.
  4. Testability — an acceptance criterion that is not a checkable outcome.
Do NOT rewrite the artifact and do NOT edit any file. Do NOT invent requirements the source
documents do not state. If a section is sound, say so briefly rather than manufacturing a finding.
End with: VERDICT: SOUND | CHANGES RECOMMENDED | MATERIAL DEFECTS
```

**Then act on it — the gate is the acting, not the running.** Triage every finding on its merits and record the disposition:

- **Accept** → make the change to the spec/plan yourself, then re-run the failed mechanical check (e.g. the plan gate's path check).
- **Reject** → only with a stated reason (it contradicts a human's authoritative answer; it's a scope expansion the source documents don't ask for; it's wrong about the code and you verified that). Codex is a reviewer, not an authority: a finding you have checked and disproved is a false positive, and adopting it because a model said it is how a spec acquires requirements nobody asked for.
- **Escalate** → a `Critical`/`High` finding that reveals a genuine **external** dependency converts to an Essential Question (triage) or `NEEDS TRIAGE` (plan), per that skill's own rules.

Never flip the status on `MATERIAL DEFECTS` without resolving them. Record the verdict and what you did about each finding in the artifact (the triage section, or the plan's gate note) so the next stage can see the review happened and how it landed.

## R2 — the completeness critic (`max`, read-only)

This **replaces** the Claude completeness critic in the work skill's Phase D. Same job, different family: attack the *audit*, not the code. It runs last, after the dimension reviewers and the adversarial verification, and its output seeds the next Phase D → E round.

```bash
codex exec -C "$WT" -m gpt-5.6-sol -c model_reasoning_effort="max" \
  -s read-only -o /tmp/codex-critic-<ID>.md "<prompt>" < /dev/null
```

Give it the audit's own artifacts — it cannot critique an audit it cannot see. Write the filled Clause and Reachability tables and the findings list to a temp file and name it in the prompt:

Because this role runs with `-C "$WT"`, name every document by **absolute path** — the spec and plan are untracked and live in the main working tree, so a relative path resolves inside the worktree and finds nothing (reads outside the workspace are permitted under `read-only`, so absolute paths work).

```
Read these files completely:
  <ABS>/docs/specs/spec-<ID>.md, <ABS>/docs/plans/plan-<ID>.md, <ABS path to the audit tables + findings file>.
You are auditing THE AUDIT, not the code. It was produced by a different model family; assume it is
over-confident and under-enumerated. The worktree is at $WT — open the code to check its claims.
Answer only these:
  1. Which acceptance-checklist / Clause row was never matched to a real file:line — or matched to a
     file:line that does not actually satisfy the clause when you read it?
  2. Which Reachability hop was never traced, or traced to a caller that is a test, a definition, or
     an optional seam the host never populates?
  3. Which critical seam (persisted round-trip, auth/scope/visibility gate, sanitiser, external
     adapter, served page/endpoint) was reviewed by READING but never EXERCISED?
  4. Which contract arm — enum value, artifact/job kind, switch case, schema variant — the branch
     adds has no in-product producer, and is not declared producer-less/deferred?
  5. Which review dimension returned "nothing found" on a surface large enough that silence is
     itself suspicious?
Your output is not a findings list — it is the seed for the next audit round. For each item name the
specific unchecked thing and the exact check that would settle it. If you genuinely cannot poke a
hole, say so explicitly; do not manufacture one.
```

A clean pass here is only meaningful because it came from outside the family that did the audit. Treat every item as a real Phase D round: it goes back through the reviewers, not straight into "resolved".

## R3 — the implementation executor (`medium`, workspace-write)

Codex writes plan-scoped code inside the feature worktree; Claude keeps the phases, the gates, and the judgment. Run it **inside the worktree** so edits land on the branch.

```bash
codex exec -C "$WT" -m gpt-5.6-terra -c model_reasoning_effort="medium" \
  -s workspace-write --dangerously-bypass-hook-trust \
  -o "$WT/.codex/last-<slice>.md" "<prompt>" < /dev/null
```

- `-s workspace-write` — Codex *writes* only inside the worktree (plus the temp dirs) and cannot touch the rest of the disk. **Reads are not restricted**, which is what makes the next point workable. Do **not** use `--dangerously-bypass-approvals-and-sandbox`; nothing about this role needs it.
- **Give the spec and plan as ABSOLUTE main-tree paths.** This is the single easiest way to make an R3 run silently worthless. The spec and plan are untracked docs that live in the **main working tree** — the worktree is branched from `INT` and does not contain them. With `-C "$WT"`, a relative `docs/specs/spec-<ID>.md` resolves inside the worktree, finds nothing, and Codex proceeds to build from the task description alone: it looks like a successful run and produces code grounded in nothing. Resolve both docs to absolute paths once, and use those same absolute paths in the prompt *and* in the hook harness below.
- `--dangerously-bypass-hook-trust` — required, and narrower than it sounds: it only skips the interactive "trust these hooks?" review, which cannot be answered in a non-interactive run. It does not widen the sandbox. The hooks it lets run are the two you generate below, in this worktree.
- **Claude runs the gates, not Codex.** `workspace-write` has no network, so treat Codex's output as *typed*, never as *verified* — the typecheck/codegen/lint/test gates are yours.

What to delegate follows `executor-lanes.md` §"What to delegate" unchanged — the plan has already made the decisions, the executor just types. In particular the **never-delegate** list still holds in full: no architectural or data-model decisions, no security-sensitive code (auth, secret custody, webhook signature verification, tenancy/authz boundaries, payment), no maker≠checker or atomic-claim idempotency logic, no provenance-honesty judgment, no contract-version changes, no cross-cutting refactors, no merge-conflict resolution, no e2e debugging, no design work, and nothing the plan marks "investigate".

Keep each invocation to **one coherent plan step**. Many small runs beat one sprawling session: cheaper retries, cleaner verification, and far less compaction.

### The prompt contract

Verbatim **absolute** paths, every time — the executor starts cold, and per the note above a relative docs path resolves against the worktree and silently finds nothing:

```
Read these files completely before writing any code:
  <ABS repo root>/docs/specs/spec-<ID>.md, <ABS repo root>/docs/plans/plan-<ID>.md,
  <ABS brief path if any>, <ABS root DESIGN md> (design authority),
  <ABS>/docs/CODING_PRACTICES.md, <ABS>/docs/NEW_PROJECT_BEST_PRACTICES.md,
  <ABS matched deep-research doc(s) — read IN FULL>.
Task: <the specific plan step(s), the exact file list, and the acceptance-checklist rows it must satisfy>.
Follow the practices docs exactly; match surrounding code style; do not touch files outside the
listed set; do not edit shared design-system tokens or base elements.
Production code only — no mocks, stubs, placeholders, or fallbacks.
Report at the end: the checklist row(s) you satisfied at file:line, and the real (non-test) caller
that reaches each piece of new code.
CONTEXT DISCIPLINE: this session will compact on a long task. The on-disk documents are your memory,
not the conversation. After ANY compaction or summarisation, re-orient to spec-<ID>.md and
plan-<ID>.md before your next action — a re-supplied copy is injected automatically; prefer it over
anything you remember.
```

**Verify Codex actually read them.** A first-action instruction to read the spec is only evidence if you check it landed: have the run report one distinctive fact from the plan (its tier, the step count, the exact file list for this slice) and confirm it against the file yourself. A wrong or vague answer means the paths didn't resolve — fix the paths and re-run rather than accepting the slice.

### The re-context harness (mandatory for R3)

The in-prompt rule above is belt; this is braces. Codex's auto-compaction summarises the conversation, and a summarised spec is a **diluted** spec — the exact mechanism by which a long build drifts off its requirements. Two generated hooks make re-supply automatic and unskippable:

- **`PostCompact`** fires on every compaction and drops a flag file. It *cannot* inject context itself (the event has no `additionalContext` channel).
- **`PostToolUse`** fires on the next tool call, sees the flag, clears it, and emits the spec + plan **verbatim** as `additionalContext`.

Net effect: within one tool call of every compaction, the authoritative documents are back in context — as text Codex did not have to choose to re-read.

Generate all four files in `$WT/.codex/` before the first R3 invocation, with **absolute paths baked in** (hooks must not depend on an inherited environment):

```bash
mkdir -p "$WT/.codex"

cat > "$WT/.codex/recontext-mark.sh" <<EOF
#!/usr/bin/env bash
# PostCompact — record that a compaction happened. Must never block the turn.
cat > /dev/null 2>&1
: > "$WT/.codex/recontext.flag" 2>/dev/null
exit 0
EOF

cat > "$WT/.codex/recontext-inject.sh" <<EOF
#!/usr/bin/env bash
# PostToolUse — after a compaction, re-inject the source documents verbatim.
cat > /dev/null 2>&1
FLAG="$WT/.codex/recontext.flag"
if [ ! -f "\$FLAG" ]; then printf '{}\n'; exit 0; fi
rm -f "\$FLAG"
python3 "$WT/.codex/recontext-emit.py" \\
  "<abs path>/docs/specs/spec-<ID>.md" \\
  "<abs path>/docs/plans/plan-<ID>.md"
exit 0
EOF

cat > "$WT/.codex/recontext-emit.py" <<'PYEOF'
#!/usr/bin/env python3
"""Emit a Codex PostToolUse hook payload that re-supplies source docs verbatim."""
import json, os, sys

HEADER = (
    "CONTEXT RECOVERY (automatic, emitted because the context was just compacted).\n"
    "The authoritative source documents for this task are re-supplied below VERBATIM.\n"
    "Treat them as the single source of truth and prefer them over any summarised\n"
    "recollection. Where a remembered paraphrase conflicts with the text below, the\n"
    "text below wins. Re-orient to it before your next action.\n"
)

parts = [HEADER]
for path in sys.argv[1:]:
    if not path or not os.path.isfile(path):
        continue
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            body = fh.read()
    except OSError:
        continue
    parts.append("\n===== BEGIN %s =====\n%s\n===== END %s =====\n" % (path, body, path))

if len(parts) == 1:
    print("{}")
else:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "".join(parts),
    }}))
PYEOF

chmod +x "$WT/.codex/recontext-mark.sh" "$WT/.codex/recontext-inject.sh"

cat > "$WT/.codex/hooks.json" <<EOF
{
  "hooks": {
    "PostCompact": [
      { "hooks": [ { "type": "command", "command": "$WT/.codex/recontext-mark.sh" } ] }
    ],
    "PostToolUse": [
      { "hooks": [ { "type": "command", "command": "$WT/.codex/recontext-inject.sh" } ] }
    ]
  }
}
EOF
```

Then **verify the harness before trusting a long run** — a silently-failed hook looks exactly like a working one:

```bash
"$WT/.codex/recontext-inject.sh" </dev/null                     # no flag  → {}
: > "$WT/.codex/recontext.flag"
"$WT/.codex/recontext-inject.sh" </dev/null | head -c 200       # flag set → the payload
rm -f "$WT/.codex/recontext.flag"
```

Watch the run's output for `hook: PostCompact` / `hook: PostToolUse` followed by **`Completed`**. `Failed` means the payload was rejected and **nothing was injected** — the run is now drifting. The overwhelmingly common cause: the wire field is **`hookEventName`** (camelCase). `hook_event_name` is what the hook *receives*; it is not what it may *emit*, and emitting it fails the whole payload.

Notes: paths are project-local (`$WT/.codex/hooks.json` is discovered from the working root, so each worktree carries its own harness); a spec + plan larger than ~2,500 tokens spills to a file that Codex reads instead of being inlined, which is intended behaviour, not a failure; and `.codex/` is generated scaffolding — keep it out of the commit (stage only files you created or modified, never `git add .`).

## The verify-fix loop (R3 — Claude's half)

Codex output counts only once you've checked it. After each invocation:

1. `git -C "$WT" diff` — read the **whole** diff. Files outside the slice's scope → revert those hunks.
2. Run the repo gates that cover the change (typecheck, codegen, affected tests, lint).
3. Judge against spec / plan / DESIGN / practices — correctness, not compilation. Apply the work skill's own self-certification bar: the checklist row satisfied at `file:line`, a real non-test caller, and a real-path exercise for any critical seam.
4. Small gaps → fix directly (don't round-trip trivia). Substantive gaps → **one** Codex retry with the failure quoted verbatim. Second failure → Claude rewrites the slice and you log `codex: reverted` for that task.
5. Commit with the skill's normal discipline once green.

## Fallback — availability is the only licensed skip

Codex is a **verification upgrade with a Claude fallback, never a dependency the pipeline can stall on or silently skip work over.** If the lane isn't working for *any* reason — the repo opted out, binary missing, not logged in, usage-limit or rate-limit response, wrong model *or wrong effort* on the wire, an empty `-o` file, the deadline firing, repeated CLI errors, the harness failing its own verification, or the kill-switch below tripped — then:

- **R1 / R2** fall back to the Claude reviewer the skill originally specified (the strong-model one-shot review; the Claude completeness critic). The gate still runs — it just runs in-family. **Record the downgrade prominently** in the artifact's gate note, because an in-family review of in-family work is measurably weaker evidence and the next reader deserves to know which one they got.
- **R3** falls back to Claude writing the code, per the standing rule: never to another cheap lane, never dropped, never deferred because the executor was down.

An unavailable lane is a logged downgrade. A skipped gate is a defect. **An opted-out repo is neither** — it is a correct run that used the in-family reviewer by the owner's instruction, and it needs no escalation, no exception request, and no apology in the report.

## Accounting honesty

Record per run, in the artifact's progress/gate note and (in a fleet) the ORCHESTRATOR.md ledger Notes:

```
codex-review:  <SOUND | CHANGES RECOMMENDED | MATERIAL DEFECTS | PARTIAL (no verdict emitted)>
               · effort actually on the wire · N findings · A accepted / R rejected
codex-critic:  N seed items · M converted to confirmed findings
codex-exec:    N tasks · M retries · K reverted
               (or: codex: unavailable → claude · codex: opted out (<file>) → claude)
```

Record the **effort that was on the wire**, not the one you asked for — that is the whole point of the header check, and a gate note reading `max` when the run was `high` is a false record of how strong the evidence was.

The R3 lane carries the same **per-lane revert-rate kill-switch** as every other downgraded lane (`executor-lanes.md` §"Accounting and the kill-switch"): if a repo's early items show Codex reverting more than roughly **1 task in 3**, stop using it as an executor for that repo, route its work to Claude, and note why. R1/R2 are exempt from the kill-switch — they are verification, and a reviewer that keeps finding real defects is *working*, not thrashing. But do track the **rejection rate**: a reviewer whose findings you reject far more often than you accept is either mis-prompted or being handed artifacts it can't ground, and both are worth fixing rather than tolerating.
