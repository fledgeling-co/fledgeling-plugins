# Model lanes — role, availability, and evidence

Canonical routing for the shipyard stages and their conductors. Read
`model-and-effort.md` for effort, `executor-lanes.md` for implementation packets,
and `second-opinion-lanes.md` for review packets. A model preference is not a
promise that this harness exposes that model or can switch it in the current session.

## Resolve the role before selecting a runner

1. Follow the user's explicit model and provider constraints first. The usual
   workflow for this project is **GPT-6 for orchestration, Claude Opus 5 for
   intake, triage and planning, and Gemini 3.8 for implementation after those
   artifacts land**. These are role preferences, not a universal capability ranking.
2. Read the actual session model, available model catalogue, tool schemas and
   project restrictions. Resolve the requested display name to an exact supported
   model identifier and a supported effort value. Do not invent an identifier,
   infer identity from the model's prose, or pass one harness's options to another.
3. Keep an existing conductor in-session unless the user requested a transfer.
   Loading a skill does not switch the model. When a stage belongs on another
   model, dispatch that bounded stage with the artifact contract below and keep
   the conductor responsible for sequencing and integration.
4. When the user has not selected a lane, use `defer:defer` and its available
   routing interface. `lane_pick.py --task implementation --shape <shape>` is a
   fallback recommendation over its registered, measured models. A registry that
   lacks Gemini 3.8 or GPT-6 cannot decide that an older model supersedes the
   user's preference; discover a supported route or report the missing route.
5. If the preferred route is unavailable, record the failure and follow any
   already-authorized fallback. Otherwise keep useful independent work moving
   and surface the model choice once. Never silently relabel an older model.

| Work | Preferred role | Boundary |
|---|---|---|
| Portfolio/fleet/feature coordination | GPT-6 or the current authorized conductor | Holds dependency map, resolves findings, serializes merges |
| Intake, triage verdict, plan synthesis | Claude Opus 5 | Produces the full brief/spec/plan and acceptance criteria before implementation |
| Implementation and scoped fixes | Gemini 3.8 | Receives the committed plan, constraints, allowed files and required checks |
| Readers and mechanical gates | Current runner or a supported economical lane | Delegate only when the work is sizeable and independent |
| Acceptance review and final verification | A capable reviewer from a family different from the artifact's writer | Receives requirements and evidence, with no author verdict or build transcript |
| Design direction and visual judgement | User-selected or currently validated design lane | Inspect the rendered subject and reference; a model name proves no visual result |

A reviewer must have demonstrated capability for the task. There is no total
ordering of model families, and a newer name or lower effort is not evidence of
review quality. Record the actual writer and reviewer so independence is testable:
Gemini-built code can be reviewed by Opus; Opus-authored plans need a non-Claude
reviewer when an independent gate is required; GPT-authored artifacts need a
non-GPT reviewer. Skip the writer's family when choosing an independent lane.

## Stage handoff contract

Every dispatched stage gets one compact packet:

- Exact skill identifier, resolved from the installed catalogue (for example
  `shipyard:plan`), with its arguments in the tool's argument field. If no Skill
  tool exists, give the verified SKILL.md path and its required reference paths.
- Objective and intended scope; source brief/spec/plan paths and their current
  revisions; user decisions and constraints that affect the stage.
- Absolute repo/worktree path and branch; exclusive writable files or surfaces;
  shared state the conductor owns and the runner must not edit.
- Prior-stage artifact paths, required output paths, acceptance criteria, checks
  to execute, and the evidence format that closes each criterion.
- Completion boundary, next consumer, unresolved blockers, and return shape:
  changed files, artifact paths, checks actually run with results, remaining work.

The next stage reads those artifacts before acting. A successful tool return or
an eloquent handback does not establish that the required artifact exists. Keep
prerequisite-dependent stages sequential; parallelize only disjoint work. Never
turn a stage handoff into an extra coordinator that merely forwards another prompt.

## Availability and execution evidence

Probe a lane before first use: verify the binary/API exists, supported options,
a successful inert request, and usable output. For a gate, capture the actual
request/response metadata or authoritative runtime trace with model and effort.
A CLI header that merely echoes requested flags is configuration evidence; a
model saying what powers it is not execution evidence. If actual identity cannot
be observed, record `model execution: unverified`; do not invent a pass.

On a failure, write `<lane>: unavailable (<observed reason>) -> <fallback>`.
Retry once only for a plausibly transient failure, then take an authorized
fallback. Empty output, missing required artifacts, or a timed-out request is a
lane failure. Keep failed and unrun checks visible in the completion record.

If no independent reviewer is available, run the best authorized review and
label it `verification: in-family (degraded)`. Same-family review does not become
independent by repetition. Add a targeted adversarial exercise only for a
specific unresolved risk; preserve all required test, measurement and real-path
evidence, and do not grant an independence-gated status until that gate is met.

## Prompting calibration

Give Opus 5 the complete task and concrete finish line, use supported effort as
the cost dial, and keep written artifacts proportional to the work. Remove generic
"double-check yourself" passes and extra coordinator layers; retain explicit
acceptance, external measurement and independent-review requirements because those
acquire evidence beyond the author's reasoning. Source: [Opus 5 prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
and [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

When editing an API harness, follow the [Opus 5 migration guide](https://platform.claude.com/docs/en/models/opus-5/migration-guide):
adaptive thinking is on by default; preserve assistant/thinking blocks unchanged
through tool loops; consume response blocks by type; and verify supported request
parameters. These API settings are not skill instructions that a runner can enact
by writing them in prose, and they do not apply automatically to Gemini or GPT.
