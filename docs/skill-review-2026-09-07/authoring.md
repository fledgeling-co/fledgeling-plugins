# Authoring and support skill review

## Scope and reviewed evidence

Reviewed the active instruction/reference surfaces in these 15 plugins: braindump, trawl, improve-skill, create-skill, geminify, mac-doctor, stocktake, vouch, atlas-publish, code-review, recover-claude-code, defer, reckon, harbourmaster, tailings.
Inventory/reference scans covered all active Markdown in scope; the detailed content review focused on authoring pipelines, model-routing instructions, Gemini calibration, code-review runner prompts and generated skill-invocation strings. Historical docs/deep-research, eval runs/answers, EVALS.md, CHANGELOG.md, evidence.md and corpus quotations were excluded from edits.

Sources read: repo CLAUDE.md; https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md; https://platform.claude.com/docs/en/about-claude/models/migration-guide.md; https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md; https://platform.claude.com/docs/en/models/opus-5/migration-guide.md. Also live Claude Code CLI reference https://code.claude.com/docs/en/cli-reference (allowedTools is auto-approval, --tools controls availability).

## Main changes

- Bundled the same self-contained references/runner-contract.md in create-skill and improve-skill, then connected the main skill, public README and branding briefs to it. It defines current user model roles, real runtime selector discovery, exact plugin:skill lookup with standalone exceptions, bounded artifact handoffs, ownership, acceptance evidence, action/advice scope and stop conditions.
- Rewrote both Opus 5 prompting references from the current vendor guidance. Removed all-Opus assumptions, retained required acceptance/instrument/independent grading evidence while removing redundant generic rechecks, corrected --allowedTools security claims, and scoped the roughly 7 KB prompt incident to its original local environment.
- Qualified active code-span skill routes and slash invocations, including mac-doctor's generated launchd and proposal prompts and harbourmaster's generated ledger. Kept plugin distribution names, filesystem paths, CLI task classes and historical failure examples intact. Authoring now resolves the runtime's actual standalone skill-creator identifier rather than inventing a namespace. Removed Geminify's runtime dependency on an absent gemini-prompt-engineering skill in favor of its bundled corpus.
- Added a concise model-evidence boundary to the 15 owned Gemini companions. The historical Gemini 3.7 Flash measurements do not establish Gemini 3.8 limitations, routing penalties or thinking defaults. Updated Geminify's authoring core so new companion files preserve that distinction and the user's implementation preference.
- Added defer/references/runtime-preferences.md: an actionable sequence of discovery, exact supported selector mapping, authorization/availability checks, native dispatch and actual serving-model receipt. Labeled lane_pick/lane_run as compatibility paths with older IDs. Added active whole-line external-model opt-out semantics, excluding quoted/fenced examples, and preserving current user authorization. Updated stocktake's routing reference to consume this policy.
- Stopped code-review's low-finding-count trigger for repetitive passes; completion now follows selected coverage, including zero findings. Preserved its explicit independent candidate adjudication, gates and coverage ledger. Replaced universally mandated Sonnet alias prompts with runtime-resolved model selection (Sonnet remains an available Claude compatibility choice).
- Corrected improve-skill's stale claim that a missing root README row merely warns: the catalogue currently hard-fails because row debt is empty. Clarified current vs historical host availability in harbourmaster.
- Fixed Geminify session_calibrate.py's resolver: it previously dropped a plugin prefix and could green-light invented prefixes. It now matches exact manifest plugin plus declared skill name, permits true standalone bare IDs, does not drop namespaces for command fallback, sorts semantic versions numerically, and labels source discovery separately from actual runtime availability.
- Corrected defer's wrapper descriptions: lane_run.sh checks nonempty output and records usage; it does not itself verify the serving-model identity. The required separate receipt check is now explicit.

## Validation

- Six isolated regression tests in geminify/scripts/test_session_calibrate.py pass: exact declared identity, wrong/bare/invented namespace rejection, semver order, standalone IDs, command-prefix rejection, and source-only resolution label. No live model calls.
- bash -n passes for changed mac-doctor launch/proposal emitters and defer/lane_run.sh; harbourmaster ledger.py parses via ast.parse.
- Local Markdown link scan of all owned active files: 0 missing file targets. New local runner-contract links resolve.
- Root skill-reference checker executed; remaining owned findings were preserved historical excerpts: Geminify's dead create-test-suite output example, Tailings' original /proctor failure twice, and historical built-in code-review provenance. Root was notified of exact exemptions needed.

## Limits and independent checker feedback

No manifests, version fields, commits, root files, source research records or measured eval results were changed by this agent. Parent owns catalogue/version checks. No claim of new live Opus/Gemini/GPT behavior evaluation is made.

The executable defer registry remains on the recorded model IDs. Current preferred roles are actionable through the documented native-runtime path; direct legacy wrapper callers remain compatibility callers until migrated. The wrapper does not inspect project opt-out files itself; the conductor must do so before dispatch. It also does not prove serving-model identity; that is an explicit separate evidence requirement.

Root checker independent feedback: whole blockquote skipping misses active runner prompt templates; whole-line skips on words like failed/measured/Unknown skill can skip active calls too. Suggested explicit historical paragraph/file exemptions plus regression tests. Catalogue should inspect/validate declared SKILL frontmatter names rather than assume directory basename.

## Reviewed inventory

- plugins/atlas-publish/README.md
- plugins/atlas-publish/skills/atlas-publish/SKILL.md
- plugins/atlas-publish/skills/atlas-publish/gemini.md
- plugins/atlas-publish/skills/atlas-publish/references/classification.md
- plugins/atlas-publish/skills/atlas-publish/references/failure-modes.md
- plugins/atlas-publish/skills/atlas-publish/references/handoff.md
- plugins/atlas-publish/skills/atlas-publish/references/ota-lane.md
- plugins/atlas-publish/skills/atlas-publish/references/store-lane.md
- plugins/braindump/README.md
- plugins/braindump/SKILL.md
- plugins/braindump/gemini.md
- plugins/braindump/references/compact-addendum.md
- plugins/code-review/README.md
- plugins/code-review/skills/code-review/SKILL.md
- plugins/code-review/skills/code-review/gemini.md
- plugins/code-review/skills/code-review/references/angles.md
- plugins/code-review/skills/code-review/references/coverage.md
- plugins/code-review/skills/code-review/references/frontend-web-checklist.md
- plugins/code-review/skills/code-review/references/logic-bugs-checklist.md
- plugins/code-review/skills/code-review/references/nestjs-checklist.md
- plugins/code-review/skills/code-review/references/nextjs-checklist.md
- plugins/code-review/skills/code-review/references/output-format.md
- plugins/code-review/skills/code-review/references/prepush.md
- plugins/code-review/skills/code-review/references/process.md
- plugins/code-review/skills/code-review/references/quality-lenses.md
- plugins/code-review/skills/code-review/references/react-native-checklist.md
- plugins/code-review/skills/code-review/references/repo-discovery.md
- plugins/code-review/skills/code-review/references/security-checklist.md
- plugins/code-review/skills/code-review/references/typescript-checklist.md
- plugins/code-review/skills/code-review/references/verification-loop.md
- plugins/create-skill/README.md
- plugins/create-skill/skills/create-skill/SKILL.md
- plugins/create-skill/skills/create-skill/gemini.md
- plugins/create-skill/skills/create-skill/references/brand-and-docs.md
- plugins/create-skill/skills/create-skill/references/discovery.md
- plugins/create-skill/skills/create-skill/references/evals-and-judging.md
- plugins/create-skill/skills/create-skill/references/opus-5-prompting.md
- plugins/create-skill/skills/create-skill/references/research.md
- plugins/defer/README.md
- plugins/defer/skills/defer/SKILL.md
- plugins/defer/skills/defer/gemini.md
- plugins/defer/skills/defer/references/capability.md
- plugins/defer/skills/defer/references/lanes.md
- plugins/defer/skills/defer/references/usage-sources.md
- plugins/defer/skills/defer/references/wire-verify.md
- plugins/defer/skills/defer/scripts/lane_run.sh
- plugins/geminify/README.md
- plugins/geminify/skills/geminify/SKILL.md
- plugins/geminify/skills/geminify/gemini.md
- plugins/geminify/skills/geminify/references/modules.md
- plugins/geminify/skills/geminify/scripts/session_calibrate.py
- plugins/harbourmaster/README.md
- plugins/harbourmaster/skills/harbourmaster/SKILL.md
- plugins/harbourmaster/skills/harbourmaster/gemini.md
- plugins/harbourmaster/skills/harbourmaster/references/admission.md
- plugins/harbourmaster/skills/harbourmaster/references/integration.md
- plugins/harbourmaster/skills/harbourmaster/references/routing.md
- plugins/harbourmaster/skills/harbourmaster/references/thermal.md
- plugins/harbourmaster/skills/harbourmaster/scripts/ledger.py
- plugins/improve-skill/README.md
- plugins/improve-skill/skills/improve-skill/SKILL.md
- plugins/improve-skill/skills/improve-skill/gemini.md
- plugins/improve-skill/skills/improve-skill/references/brand-and-docs.md
- plugins/improve-skill/skills/improve-skill/references/evals-and-judging.md
- plugins/improve-skill/skills/improve-skill/references/opus-5-prompting.md
- plugins/improve-skill/skills/improve-skill/references/research.md
- plugins/mac-doctor/README.md
- plugins/mac-doctor/skills/mac-doctor/SKILL.md
- plugins/mac-doctor/skills/mac-doctor/gemini.md
- plugins/mac-doctor/skills/mac-doctor/references/ledger.md
- plugins/mac-doctor/skills/mac-doctor/references/processes.md
- plugins/mac-doctor/skills/mac-doctor/references/reclaim.md
- plugins/mac-doctor/skills/mac-doctor/references/scheduling.md
- plugins/mac-doctor/skills/mac-doctor/references/tiers.md
- plugins/mac-doctor/skills/mac-doctor/scripts/install-agents.sh
- plugins/mac-doctor/skills/mac-doctor/scripts/reclaim.sh
- plugins/reckon/README.md
- plugins/reckon/skills/reckon/SKILL.md
- plugins/reckon/skills/reckon/gemini.md
- plugins/reckon/skills/reckon/references/estimation.md
- plugins/reckon/skills/reckon/references/joining.md
- plugins/reckon/skills/reckon/references/no-campaign.md
- plugins/reckon/skills/reckon/references/partition.md
- plugins/recover-claude-code/README.md
- plugins/recover-claude-code/skills/recover-claude-code/SKILL.md
- plugins/recover-claude-code/skills/recover-claude-code/gemini.md
- plugins/recover-claude-code/skills/recover-claude-code/references/mechanics.md
- plugins/stocktake/README.md
- plugins/stocktake/skills/stocktake/SKILL.md
- plugins/stocktake/skills/stocktake/gemini.md
- plugins/stocktake/skills/stocktake/references/column-policy.md
- plugins/stocktake/skills/stocktake/references/running-long.md
- plugins/stocktake/skills/stocktake/references/testing-adequacy.md
- plugins/stocktake/skills/stocktake/references/the-oracle-order.md
- plugins/stocktake/skills/stocktake/references/verification-lanes.md
- plugins/tailings/README.md
- plugins/tailings/skills/tailings/SKILL.md
- plugins/tailings/skills/tailings/gemini.md
- plugins/tailings/skills/tailings/references/probes.md
- plugins/trawl/README.md
- plugins/trawl/skills/trawl/SKILL.md
- plugins/trawl/skills/trawl/gemini.md
- plugins/trawl/skills/trawl/references/convergence.md
- plugins/trawl/skills/trawl/references/frames.md
- plugins/vouch/README.md
- plugins/vouch/skills/vouch/SKILL.md
- plugins/vouch/skills/vouch/gemini.md
- plugins/vouch/skills/vouch/references/configuration.md
- plugins/vouch/skills/vouch/references/extraction.md
- plugins/vouch/skills/vouch/references/gates.md
- plugins/vouch/skills/vouch/references/inclusion-rules.md
- plugins/vouch/skills/vouch/references/matching.md
- plugins/vouch/skills/vouch/references/outputs.md
- plugins/vouch/skills/vouch/references/portals.md
- plugins/vouch/skills/vouch/references/sources.md

## Changed/new files

- plugins/atlas-publish/README.md
- plugins/atlas-publish/skills/atlas-publish/SKILL.md
- plugins/atlas-publish/skills/atlas-publish/gemini.md
- plugins/braindump/gemini.md
- plugins/code-review/README.md
- plugins/code-review/skills/code-review/SKILL.md
- plugins/code-review/skills/code-review/gemini.md
- plugins/code-review/skills/code-review/references/process.md
- plugins/code-review/skills/code-review/references/verification-loop.md
- plugins/create-skill/README.md
- plugins/create-skill/skills/create-skill/SKILL.md
- plugins/create-skill/skills/create-skill/gemini.md
- plugins/create-skill/skills/create-skill/references/brand-and-docs.md
- plugins/create-skill/skills/create-skill/references/evals-and-judging.md
- plugins/create-skill/skills/create-skill/references/opus-5-prompting.md
- plugins/create-skill/skills/create-skill/references/runner-contract.md
- plugins/defer/README.md
- plugins/defer/skills/defer/SKILL.md
- plugins/defer/skills/defer/gemini.md
- plugins/defer/skills/defer/references/capability.md
- plugins/defer/skills/defer/references/lanes.md
- plugins/defer/skills/defer/references/runtime-preferences.md
- plugins/defer/skills/defer/scripts/lane_run.sh
- plugins/geminify/README.md
- plugins/geminify/skills/geminify/SKILL.md
- plugins/geminify/skills/geminify/gemini.md
- plugins/geminify/skills/geminify/references/modules.md
- plugins/geminify/skills/geminify/scripts/session_calibrate.py
- plugins/geminify/skills/geminify/scripts/test_session_calibrate.py
- plugins/harbourmaster/README.md
- plugins/harbourmaster/skills/harbourmaster/SKILL.md
- plugins/harbourmaster/skills/harbourmaster/gemini.md
- plugins/harbourmaster/skills/harbourmaster/references/integration.md
- plugins/harbourmaster/skills/harbourmaster/references/routing.md
- plugins/harbourmaster/skills/harbourmaster/scripts/ledger.py
- plugins/improve-skill/README.md
- plugins/improve-skill/skills/improve-skill/SKILL.md
- plugins/improve-skill/skills/improve-skill/gemini.md
- plugins/improve-skill/skills/improve-skill/references/brand-and-docs.md
- plugins/improve-skill/skills/improve-skill/references/opus-5-prompting.md
- plugins/improve-skill/skills/improve-skill/references/runner-contract.md
- plugins/mac-doctor/README.md
- plugins/mac-doctor/skills/mac-doctor/SKILL.md
- plugins/mac-doctor/skills/mac-doctor/gemini.md
- plugins/mac-doctor/skills/mac-doctor/scripts/install-agents.sh
- plugins/mac-doctor/skills/mac-doctor/scripts/reclaim.sh
- plugins/reckon/README.md
- plugins/reckon/skills/reckon/gemini.md
- plugins/reckon/skills/reckon/references/no-campaign.md
- plugins/reckon/skills/reckon/references/partition.md
- plugins/recover-claude-code/README.md
- plugins/recover-claude-code/skills/recover-claude-code/gemini.md
- plugins/recover-claude-code/skills/recover-claude-code/references/mechanics.md
- plugins/stocktake/README.md
- plugins/stocktake/skills/stocktake/SKILL.md
- plugins/stocktake/skills/stocktake/gemini.md
- plugins/stocktake/skills/stocktake/references/running-long.md
- plugins/stocktake/skills/stocktake/references/testing-adequacy.md
- plugins/stocktake/skills/stocktake/references/verification-lanes.md
- plugins/tailings/README.md
- plugins/tailings/skills/tailings/SKILL.md
- plugins/tailings/skills/tailings/gemini.md
- plugins/tailings/skills/tailings/references/probes.md
- plugins/trawl/README.md
- plugins/trawl/skills/trawl/SKILL.md
- plugins/trawl/skills/trawl/gemini.md
- plugins/trawl/skills/trawl/references/convergence.md
- plugins/vouch/skills/vouch/SKILL.md
- plugins/vouch/skills/vouch/gemini.md
- plugins/vouch/skills/vouch/references/gates.md
- plugins/vouch/skills/vouch/references/outputs.md
- plugins/vouch/skills/vouch/references/portals.md
