# Operational rules — the incident ledger

**Canonical for the whole pipeline.** Every rule here encodes a specific, dated incident from the
predecessor pipelines' fleets; none is re-derivable from principles. They are grouped by the layer
they protect. Do not soften them when editing — each one was paid for once already.

## Git and worktrees

- **Never pass `-c user.email` or `-c user.name` to git.** A run that "helpfully" attributed its
  commits to a bot address blocked every deployment across a whole team with
  `TEAM_ACCESS_REQUIRED` until the history was rewritten. Attribution rides in the
  `Co-Authored-By:` trailer only.
- **Never `git add .` / `git add -A`.** One `-A` swept 1,164 insertions of three sibling runners'
  work onto main. Stage only files you created or modified.
- **Worktree-first, universally.** N concurrent runners sharing the main tree means one runner's
  mid-edit file breaks main's typecheck for everyone — this recurred three times in one fleet
  before being diagnosed as structural. Every phase of every feature runs inside its worktree;
  the only main-tree writes are the spec/ledger docs.
- **Detect the integration branch; never hardcode it.** Prefer `origin/staging` if it exists,
  else `git remote show origin | sed -n 's/.*HEAD branch: //p'`. A hardcoded `origin/staging` in
  a repo without one silently branches from a stale local `main` and skips the rebase — the
  "based on a month-old base, re-created an already-merged module" failure. `git fetch origin`
  (all refs), and check `git merge-base --is-ancestor "$INT" HEAD` before trusting a reused
  worktree.
- **Kill by process group, not pid.** A superseded agent kept editing files and collided with its
  replacement; run children in their own process group and kill the group. Never `pkill -f` a
  generic pattern — one `pkill -f vitest` killed a sibling runner's live test run.

## Workflow / fan-out

- **`agent()` returns `null` on a terminal API error with zero retries, and the run still reports
  `completed`.** `.filter(Boolean)` hides the deaths. **`done` means merged/verified per the
  ledger — never "the dispatch returned".** Before ticking an item, read its ledger row and check
  the integration branch for the merge it claims.
- **Cap each wave at ≤4 concurrent agents** — ~10+ at once trips a server-side rate limit
  ("temporarily limiting requests") that fails most of the wave. Chunk into sequential
  `parallel(...)` batches. Under a fleet, the wave cap and the runner-slot count multiply:
  **budget globally** (runners × wave ≤ ~16) rather than letting 8 runners × 4 agents stampede
  the same limiter.
- **Retry transient failures** ("API Error / Rate limited" strings, `null`s) in a later small
  batch; never treat one as a result or finding. Two retry failures → park with a reason.
- **`Promise.race` over an empty iterable never settles** — check before racing.
- **`args` can arrive JSON-encoded** — a missing prompt burned ~60k tokens per runner; validate
  before spawning.
- **Prefer plain-text returns for long, file-reading subagents** — schema-forced agents that read
  many files often finish without emitting the structured output; reserve `schema` for the single
  synthesis step.
- **Workflow-inner agents cannot be re-invoked** (SendMessage: "No transcript found"), and a
  runner that ends its turn to wait for a background task is dead the moment it stops.

## External CLIs (the shared traps; per-lane detail in `executor-lanes.md` / `codex-cli.md`)

- **Wire-verify, never trust flags**: grep the captured header/transcript for model and effort; a
  dropped flag silently inherits the user's config default (a shipped gate ran at `high` this
  way). Never hardcode a dated model id in the check — a pinned id fires `WRONG-MODEL` on every
  correctly-routed newer model and stops a fleet before it starts; check the tier.
- **An empty output file is a lane failure, not a pass.** Bound every call with
  `perl -e 'alarm shift @ARGV; exec @ARGV' <secs>` (macOS has no `timeout(1)`; exit 142 =
  deadline). `< /dev/null` on codex or it waits on stdin forever. `agy --print` buffers to the
  end — wait for exit, never poll its stdout.
- **Absolute paths under `-C`** — a relative `docs/...` resolves inside the worktree, finds
  nothing, and the run builds from the task description alone, looking successful and grounded in
  nothing. Have the run report one distinctive fact from the plan to confirm the read landed.
- **The hook wire field is `hookEventName`** (camelCase) — `hook_event_name` fails the payload
  silently, and a silently-failed hook looks exactly like a working one; self-test it.
- **Over-scoped `max` reviews emit nothing** — the failure is the default outcome, not rare.
  Narrow the packet before widening the deadline.

## Ledgers and state

- **The ledger is the memory, not the transcript.** A state change not recorded did not happen;
  a fresh session must be able to resume the whole run from the on-disk artifacts alone.
- **Append, never truncate, shared ledger files; recount, never increment** — derive counts by
  reading the rows back, because a crashed writer leaves the count wrong and the rows right.
- **Post intent before attempting** (the crash-safe counter in `tracker-adapter.md`): a run that
  dies mid-fix still leaves its marker for the next run to count.
- **A transcript is a log, not a knowledge state.** On pause/handover, convert the non-redundant
  residue into a handover doc; the tail-harvest alone once recovered a fully-diagnosed bug.
- **Verdicts are deliverables — commit them.** A 110-ticket audit's per-ticket verdicts written
  outside git were lost entirely; the rebuild was committed precisely so it can't repeat.

## Reviews

- **Never brief a reviewer to be conservative or to report only serious findings** — it is
  followed literally and lowers recall. Report everything; filter at disposition.
- **A prior self-review commit does not certify the code.** The pattern that most often survives
  a self-review is a governance/authorization bypass, because the author trusts their own
  attribution.
- **One quiet audit pass is a shallow fixpoint, not a dry one** — remediation loops exit on two
  consecutive dry audits with different lenses.
- **Never strip the pipeline's safeguards to make a runner cheaper.** The hand-rolled "SOLO
  runner" brief that stripped fan-out and review phases is how a fix ships "verified by code
  reading" — the audit corpus's most common failure. Cost is cut by model/effort routing and
  scope, never by deleting verification. The sanctioned low-cost runner shape is published in
  ship-fleet; operators improvising cheaper ones is the failure this rule prevents.
- **A follow-up you recommend is created (cite its id) or explicitly declined — never left as
  "recommend raising a separate task".**

## Cache and effort

- Effort defaults to `high` when unset; backgrounded agents on some launch paths default to
  `xhigh` with no knob. Set effort explicitly at spawn; hold it constant per agent (changing it
  forfeits the prompt-cache prefix). `xhigh`/`max` pair with `max_tokens` ≥ 64k.
- The prompt cache keys on the exact byte prefix and its TTL is a harness choice — never build a
  pause strategy that only works at one TTL.
