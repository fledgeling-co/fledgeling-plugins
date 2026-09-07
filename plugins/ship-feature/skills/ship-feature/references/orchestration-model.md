# Orchestration model — stage handoffs, memory and worktrees

The conductor owns one feature from intake to integration. It retains the user's
intent, sequences the stages, reads their artifacts and resolves the decisions
between them. It can run a stage locally or hand it to the model assigned to that
role; a skill invocation alone never changes the session's model.

## 1. One conductor, explicit stage boundaries

Read shipyard's `references/model-lanes.md` before routing. The usual preference
is GPT-6 for orchestration, Opus 5 for intake/triage/plan, then Gemini 3.8 for
implementation. Resolve actual supported model IDs and effort values from the
current runner; the measured fallback registry does not override this preference.

Keep prerequisite-dependent stages sequential. Plan and design may overlap only
where their files and decisions are independent, and both must land before their
implementation begins. Final `shipyard:verify` runs in fresh context on a capable
family different from the implementation writer's.

Do not add an agent that merely dispatches another agent. A whole-stage handoff
is useful when it realizes the selected model role or isolates substantial work;
a few local tool calls do not need a separate runner. For parallel work, assign
disjoint writable files and a concurrency cap within the observed host limits.

## 2. Every handoff carries the context needed to finish

The runner packet names the exact resolved skill, its arguments, the objective,
absolute repo/worktree path, allowed files, current source artifact revisions,
user decisions, required outputs, acceptance evidence and stopping boundary.
Use the contract in shipyard's `references/model-lanes.md`; pass reference paths
instead of copying a large routing table into every nested prompt.

For example, an implementation handoff contains the committed Opus plan, spec and
mock index; assigned acceptance rows; non-goals and architectural constraints;
the branch/worktree; checks to run; and the completion-record path. The Gemini
runner reports changed files, checks actually executed, artifacts and remaining
blockers. The conductor opens those artifacts before advancing the status.

An independent reviewer gets the original requirements and evidence, without the
author's verdict or build transcript. An empty result or missing artifact is an
unfinished stage, never an implicit pass. A fallback reports the actual model and
whether family independence was lost.

## 3. Durable artifacts are the pipeline's memory

| Stage | Durable artifact |
|---|---|
| `shipyard:intake` | Brief under `docs/features-to-triage/` |
| `shipyard:triage` | Spec, decisions/assumptions and ledger entry |
| `shipyard:plan` | Committed plan and acceptance/test strategy |
| `shipyard:design` | Mock index, surface/state matrix and design evidence |
| `shipyard:work` | Feature branch plus Clause/Reachability tables and completion record |
| `shipyard:gap-fix` | Disposition of remaining gaps and the specific evidence rerun |
| `test-campaign:test-campaign` or installed acceptance skill | Acceptance results tied to requirement and subject |
| `shipyard:verify` | Independent per-requirement verdict and remaining blockers |

At each boundary open the artifact the next stage depends on and confirm its
revision. After compaction or interruption, reconcile the recorded state against
the worktree, commits and check outputs, then resume the first incomplete stage.
Do not restart a green stage merely to refresh context. Re-run evidence only when
a change, failure or unresolved concern invalidates the prior result.

## 4. One feature, one branch, one worktree

`shipyard:work` uses `.worktrees/<ID>` on `ai/<id>` unless the repo or user specifies
another convention. The conductor passes the absolute existing worktree to later
stages; deferred and child implementation stay on that branch. Never open a second
worktree just because the next runner has a fresh context.

Follow the ownership recorded by the conductor: feature code and design edits in
the assigned worktree; shared ledger and orchestration files under the designated
single writer. Fleet mode establishes the worktree before any runner edit. A
single-feature stage does not unilaterally relocate untracked source documents.

Run acceptance against the app served from that worktree. Serialized finalization
requires the configured merge gate, then the authorized merge/push and cleanup.
Keep `ready-to-merge`, `merged`, `pushed` and `deployed` as separate evidence states.

## 5. Evidence earns a review step

Run the required tests, real-path exercises, visual measurements and independent
acceptance gates. Avoid generic extra same-author rereads and one agent per small
check. Findings need a location, affected requirement and evidence; after a fix,
repeat the checks it invalidated. Preserve unmet criteria and explicit waivers in
the handback rather than reducing the feature's scope to make it pass.
