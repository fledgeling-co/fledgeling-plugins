# Workflow skill review — 2026-09-07

## Outcome

Reviewed the assigned 20-plugin active Markdown inventory (198 files, 42,821 original lines), with detailed reads of the cross-model conductors, pipeline contracts, review gates, clarification rules and model-specific sidecars. Scanned the complete inventory for prospective skill/model/tool references and studied the matched context; research/evaluation records were retained. Also reviewed the generated create-swe-project instruction fragments, which future projects consume as CLAUDE.md.

The inventory below is the static review boundary; it is not a claim that every skill was executed. No model task evaluation, live provider request, UI acceptance run, commit, push or release was performed. Executable implementations, manifests and version fields are left to the parent; changes here are instructions, references and generated instruction templates.

## Concrete changes

1. Replaced contradictory shared routing with explicit role policy: normally GPT-6 coordinates, Opus 5 produces intake/triage/plan, and Gemini 3.8 implements after those artifacts land. Resolve supported exact IDs from the real runner, honor user preferences before the historical fallback matrix, and record unavailable or substituted lanes. Model families are not assumed to form a universal capability ranking.
2. Permitted bounded whole-stage handoffs to realize those role choices. Every packet names exact skill/arguments separately, source revisions, absolute repo/worktree, exclusive writable scope, artifacts, checks, evidence and finish line. The conductor retains integration and reads artifacts at boundaries; loading a skill does not switch models.
3. Removed all-Opus fleet constraints and introspective model self-checks as proof. Model prose and headers echoing flags are not serving-model evidence. Prefer authoritative execution metadata; record unavailable identity. The Workflow example is explicitly harness-specific and must match exposed tool schemas.
4. Corrected fleet scheduling examples that forced one runner when capacity was zero, could use a negative slice count after capacity shrank, and fell back to eight despite a five-runner policy. Slots now respect user/tool/host caps, zero capacity returns resumable scheduling state, and missing telemetry uses a conservative fallback.
5. Removed the default D-prime fresh same-family rereview stacked after acceptance review; it now needs a named unresolved gap. Gap-fix closes the full requirement census with current typed evidence and targeted reruns, instead of requiring two generic dry audits. Required behavioral tests, visual/subject evidence and independent final acceptance gates remain.
6. Scoped Gemini sidecar routing exclusions to the actual Gemini 3.7 Flash data. They cannot prove Gemini 3.8 incapability or silently redirect the user's chosen implementation model. Preserved original benchmark numbers and source quotations. Updated current sidecar stage contracts for conditional follow-ups.
7. Simplified clarify: routine reversible calls stay local; a second opinion needs a material unresolved technical ambiguity; model opinions cannot supply the user's preference. Existing authorization carries forward. Prospective rigid model lists and unconditional reconfirmation are removed, while real user-axis decisions remain visible.
8. Qualified prospective skill references using the real local catalogue plus externally installed IDs supplied by the session. Kept tool names, CLI options, schema names, file paths, standalone/bundled commands and historical records distinct. Fixed future generated template invocation examples too. Container `/work/` remains a path.
9. Aligned provider-policy interpretation with the scaffold's `OPT-OUT: external-models` directive and explicit legacy directives. A quoted marker is not an active opt-out. Updated policy precedence and permitted fallback reporting; did not change provider settings.
10. Refreshed warrant's Opus authoring reference from the supplied primary docs and removed its assumption that all lanes are Opus. Opus-specific API migration advice is scoped to API harnesses, not copied as Gemini/GPT options.

## Sources read

- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md — Anthropic prompting best practices.
- https://platform.claude.com/docs/en/about-claude/models/migration-guide.md — migration index.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md — Opus 5 task scope, delegation, verbosity and self-correction.
- https://platform.claude.com/docs/en/models/opus-5/migration-guide.md — Opus 5 model ID, adaptive-thinking defaults, response block types, preserved thinking blocks and removed parameters.
- Repository CLAUDE.md, source skill frontmatter/catalogue, the pipeline's existing evidence contracts and observed incident descriptions.

## Validation and limits

- `python3 scripts/check_skill_references.py --json` completed with zero findings across the parent checker's active project inventory after these changes; result: `/tmp/skill-review-workflow-final-audit.json`.
- Scoped `git diff --check` is rerun before handback; no tests were added for prompt-only edits.
- Catalogue build/version synchronization are the parent's responsibility.
- These prompt edits have not been evaluated on Opus 5, Gemini 3.8 or GPT-6; the older measurements remain historical, not measured evidence for this revision.
- The fallback registry does not prove a currently supported Gemini 3.8/GPT-6 CLI route. Runtime discovery is required, not an invented model ID.

## Deliberately preserved references

- `anvil errand -p "review /work/ ..."`: `/work/` is the container workspace, not shipyard:work.
- better-goal/better-loop references to bundled `/verify` and `/code-review`: harness command invocation limitations, explicitly labelled at the usage site; not references to similarly named plugins.
- COD Dossier quotations in shipyard design/intake/gap-fix Gemini sidecars: historical evidence of skipped bare-name references.
- `docs/**/plan*.md`: a glob, not a `/plan` invocation.
- better-loop Gemini's preflight block was an illustrative future receipt, not a recorded run: now labelled as illustrative and uses qualified `better-goal:better-goal` in both the input and output example.
- Named external skill dependencies such as `acceptance-e2e:acceptance-e2e`, `spec-validation:spec-validation`, `mac-design-studio:mac-design-studio`, `macosify:macosify`, `design-md-from-website:design-md-from-website` resolve in the supplied session catalogue, but a future runner must confirm installation.
- Proctor and Dossier tool surfaces, CLI flags and historical runtime behavior must be rediscovered in the executing harness; this review does not certify those remote APIs.

## Changed plugins

anvil-errand, armada-sync, be-my-witness, better-goal, better-loop, clarify, create-swe-project, discipline, flagship, mockup-fidelity, proctor, resume-session, ship-armada, ship-feature, ship-fleet, shipyard, test-campaign, warrant, whats-left

## Changed files

- plugins/anvil-errand/README.md
- plugins/anvil-errand/skills/anvil-errand/SKILL.md
- plugins/armada-sync/.claude-plugin/plugin.json
- plugins/armada-sync/README.md
- plugins/armada-sync/skills/armada-sync/SKILL.md
- plugins/be-my-witness/README.md
- plugins/be-my-witness/skills/be-my-witness/SKILL.md
- plugins/better-goal/.claude-plugin/plugin.json
- plugins/better-goal/README.md
- plugins/better-goal/skills/better-goal/SKILL.md
- plugins/better-goal/skills/better-goal/references/failure-modes.md
- plugins/better-goal/skills/better-goal/references/gate-craft.md
- plugins/better-goal/skills/better-goal/references/mechanics.md
- plugins/better-loop/.claude-plugin/plugin.json
- plugins/better-loop/README.md
- plugins/better-loop/skills/better-loop/SKILL.md
- plugins/better-loop/skills/better-loop/gemini.md
- plugins/better-loop/skills/better-loop/references/failure-modes.md
- plugins/better-loop/skills/better-loop/references/mechanics.md
- plugins/clarify/.claude-plugin/plugin.json
- plugins/clarify/README.md
- plugins/clarify/skills/clarify/SKILL.md
- plugins/clarify/skills/clarify/gemini.md
- plugins/clarify/skills/clarify/references/patterns.md
- plugins/create-swe-project/.claude-plugin/plugin.json
- plugins/create-swe-project/README.md
- plugins/create-swe-project/skills/create-swe-project/SKILL.md
- plugins/create-swe-project/skills/create-swe-project/gemini.md
- plugins/create-swe-project/skills/create-swe-project/references/launch-pipeline.md
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/footer.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/header.tmpl
- plugins/discipline/skills/discipline/gemini.md
- plugins/flagship/.claude-plugin/plugin.json
- plugins/flagship/README.md
- plugins/flagship/skills/flagship/SKILL.md
- plugins/flagship/skills/flagship/references/decisions.md
- plugins/flagship/skills/flagship/references/dispatch.md
- plugins/flagship/skills/flagship/references/lanes.md
- plugins/flagship/skills/flagship/references/roster-and-briefs.md
- plugins/flagship/skills/flagship/references/spawning.md
- plugins/flagship/skills/flagship/references/tiered-delegation.md
- plugins/mockup-fidelity/skills/mockup-fidelity/SKILL.md
- plugins/mockup-fidelity/skills/mockup-fidelity/gemini.md
- plugins/proctor/README.md
- plugins/proctor/skills/proctor/SKILL.md
- plugins/proctor/skills/proctor/gemini.md
- plugins/proctor/skills/proctor/references/methodology.md
- plugins/resume-session/README.md
- plugins/resume-session/skills/resume-session/SKILL.md
- plugins/ship-armada/.claude-plugin/plugin.json
- plugins/ship-armada/README.md
- plugins/ship-armada/skills/ship-armada/SKILL.md
- plugins/ship-armada/skills/ship-armada/gemini.md
- plugins/ship-feature/.claude-plugin/plugin.json
- plugins/ship-feature/skills/ship-feature/SKILL.md
- plugins/ship-feature/skills/ship-feature/gemini.md
- plugins/ship-feature/skills/ship-feature/references/deferred-work-loop.md
- plugins/ship-feature/skills/ship-feature/references/e2e-and-finalize.md
- plugins/ship-feature/skills/ship-feature/references/orchestration-model.md
- plugins/ship-fleet/.claude-plugin/plugin.json
- plugins/ship-fleet/skills/ship-fleet/SKILL.md
- plugins/ship-fleet/skills/ship-fleet/gemini.md
- plugins/ship-fleet/skills/ship-fleet/references/preflight.md
- plugins/ship-fleet/skills/ship-fleet/references/scheduling-and-concurrency.md
- plugins/shipyard/.claude-plugin/plugin.json
- plugins/shipyard/README.md
- plugins/shipyard/references/codex-cli.md
- plugins/shipyard/references/evidence-rules.md
- plugins/shipyard/references/executor-lanes.md
- plugins/shipyard/references/model-and-effort.md
- plugins/shipyard/references/model-lanes.md
- plugins/shipyard/references/second-opinion-lanes.md
- plugins/shipyard/references/test-strategy.md
- plugins/shipyard/references/tracker-adapter.md
- plugins/shipyard/skills/design/SKILL.md
- plugins/shipyard/skills/design/gemini.md
- plugins/shipyard/skills/gap-fix/SKILL.md
- plugins/shipyard/skills/gap-fix/gemini.md
- plugins/shipyard/skills/plan/SKILL.md
- plugins/shipyard/skills/plan/references/plan-tiers.md
- plugins/shipyard/skills/shipyard/SKILL.md
- plugins/shipyard/skills/triage/SKILL.md
- plugins/shipyard/skills/triage/references/spec-format.md
- plugins/shipyard/skills/verify/SKILL.md
- plugins/shipyard/skills/verify/gemini.md
- plugins/shipyard/skills/work/SKILL.md
- plugins/shipyard/skills/work/gemini.md
- plugins/test-campaign/README.md
- plugins/test-campaign/skills/test-campaign/SKILL.md
- plugins/test-campaign/skills/test-campaign/gemini.md
- plugins/test-campaign/skills/test-campaign/references/capture-lineage.md
- plugins/test-campaign/skills/test-campaign/references/harness-lanes.md
- plugins/test-campaign/skills/test-campaign/references/inert-ui.md
- plugins/test-campaign/skills/test-campaign/references/sweeps.md
- plugins/warrant/.claude-plugin/plugin.json
- plugins/warrant/README.md
- plugins/warrant/references/opus5-authoring.md
- plugins/warrant/references/script-contract.md
- plugins/warrant/skills/assay/SKILL.md
- plugins/warrant/skills/charter/SKILL.md
- plugins/warrant/skills/ledger/SKILL.md
- plugins/warrant/skills/lot/SKILL.md
- plugins/warrant/skills/lot/gemini.md
- plugins/warrant/skills/oracle/SKILL.md
- plugins/warrant/skills/oracle/gemini.md
- plugins/warrant/skills/ratchet/gemini.md
- plugins/warrant/skills/warrant/SKILL.md
- plugins/whats-left/README.md
- plugins/whats-left/skills/whats-left/SKILL.md
- plugins/whats-left/skills/whats-left/gemini.md
- plugins/whats-left/skills/whats-left/references/reading-the-answers.md
- plugins/whats-left/skills/whats-left/references/the-item-model.md
- plugins/whats-left/skills/whats-left/references/the-question-model.md

## Reviewed Markdown inventory

- plugins/flagship/README.md
- plugins/flagship/skills/flagship/SKILL.md
- plugins/flagship/skills/flagship/gemini.md
- plugins/flagship/skills/flagship/references/authority.md
- plugins/flagship/skills/flagship/references/propagation.md
- plugins/flagship/skills/flagship/references/evidence.md
- plugins/flagship/skills/flagship/references/roster-and-briefs.md
- plugins/flagship/skills/flagship/references/spawning.md
- plugins/flagship/skills/flagship/references/tiered-delegation.md
- plugins/flagship/skills/flagship/references/dispatch.md
- plugins/flagship/skills/flagship/references/lanes.md
- plugins/flagship/skills/flagship/references/decisions.md
- plugins/ship-armada/README.md
- plugins/ship-armada/skills/ship-armada/SKILL.md
- plugins/ship-armada/skills/ship-armada/gemini.md
- plugins/ship-armada/skills/ship-armada/references/manifest.md
- plugins/armada-sync/README.md
- plugins/armada-sync/skills/armada-sync/SKILL.md
- plugins/armada-sync/skills/armada-sync/gemini.md
- plugins/create-swe-project/README.md
- plugins/create-swe-project/skills/create-swe-project/SKILL.md
- plugins/create-swe-project/skills/create-swe-project/gemini.md
- plugins/create-swe-project/skills/create-swe-project/references/research-notes.md
- plugins/create-swe-project/skills/create-swe-project/references/apple-commercialization.md
- plugins/create-swe-project/skills/create-swe-project/references/launch-pipeline.md
- plugins/be-my-witness/README.md
- plugins/be-my-witness/skills/be-my-witness/SKILL.md
- plugins/be-my-witness/skills/be-my-witness/gemini.md
- plugins/be-my-witness/skills/be-my-witness/references/looking-protocol.md
- plugins/be-my-witness/skills/be-my-witness/references/difference-classes.md
- plugins/be-my-witness/skills/be-my-witness/references/harness-integration.md
- plugins/be-my-witness/skills/be-my-witness/references/evidence.md
- plugins/be-my-witness/skills/be-my-witness/references/bias-controls.md
- plugins/be-my-witness/skills/be-my-witness/references/verdict-schema.md
- plugins/mockup-fidelity/README.md
- plugins/mockup-fidelity/skills/mockup-fidelity/SKILL.md
- plugins/mockup-fidelity/skills/mockup-fidelity/gemini.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/browser-measurement.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/scope-and-asking.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/react-native.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/measurement-enforcement.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/functional-gaps.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/native-lane.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/evidence.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/issue-to-check-map.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/mechanical-conversion.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/engine-capability-matrix.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/batch-orchestration.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/fidelity-probe.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/react-web.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/structure-and-content-diff.md
- plugins/mockup-fidelity/skills/mockup-fidelity/references/component-visual-regression.md
- plugins/discipline/README.md
- plugins/discipline/skills/discipline/SKILL.md
- plugins/discipline/skills/discipline/gemini.md
- plugins/discipline/skills/discipline/references/v5-proposal.md
- plugins/discipline/skills/discipline/references/injected-block.md
- plugins/discipline/skills/discipline/references/evidence.md
- plugins/discipline/skills/discipline/references/provenance.md
- plugins/better-goal/README.md
- plugins/better-goal/skills/better-goal/SKILL.md
- plugins/better-goal/skills/better-goal/gemini.md
- plugins/better-goal/skills/better-goal/references/failure-modes.md
- plugins/better-goal/skills/better-goal/references/templates.md
- plugins/better-goal/skills/better-goal/references/gate-craft.md
- plugins/better-goal/skills/better-goal/references/mechanics.md
- plugins/better-goal/skills/better-goal/references/presets.md
- plugins/better-loop/README.md
- plugins/better-loop/skills/better-loop/SKILL.md
- plugins/better-loop/skills/better-loop/gemini.md
- plugins/better-loop/skills/better-loop/references/failure-modes.md
- plugins/better-loop/skills/better-loop/references/templates.md
- plugins/better-loop/skills/better-loop/references/mechanism-choice.md
- plugins/better-loop/skills/better-loop/references/mechanics.md
- plugins/clarify/README.md
- plugins/clarify/skills/clarify/SKILL.md
- plugins/clarify/skills/clarify/gemini.md
- plugins/clarify/skills/clarify/references/evidence.md
- plugins/clarify/skills/clarify/references/patterns.md
- plugins/should-compact/README.md
- plugins/should-compact/skills/should-compact/SKILL.md
- plugins/should-compact/skills/should-compact/gemini.md
- plugins/should-compact/skills/should-compact/references/evidence.md
- plugins/whats-left/README.md
- plugins/whats-left/skills/whats-left/SKILL.md
- plugins/whats-left/skills/whats-left/gemini.md
- plugins/whats-left/skills/whats-left/references/the-question-model.md
- plugins/whats-left/skills/whats-left/references/reading-the-answers.md
- plugins/whats-left/skills/whats-left/references/evidence.md
- plugins/whats-left/skills/whats-left/references/the-item-model.md
- plugins/proctor/README.md
- plugins/proctor/skills/proctor/SKILL.md
- plugins/proctor/skills/proctor/gemini.md
- plugins/proctor/skills/proctor/references/evidence.md
- plugins/proctor/skills/proctor/references/methodology.md
- plugins/proctor/skills/proctor/references/tools.md
- plugins/test-campaign/README.md
- plugins/test-campaign/schemas/README.md
- plugins/test-campaign/skills/test-campaign/SKILL.md
- plugins/test-campaign/skills/test-campaign/gemini.md
- plugins/test-campaign/skills/test-campaign/references/oracle-construction.md
- plugins/test-campaign/skills/test-campaign/references/progress-reporting.md
- plugins/test-campaign/skills/test-campaign/references/evidence-and-ids.md
- plugins/test-campaign/skills/test-campaign/references/task-bound-flows.md
- plugins/test-campaign/skills/test-campaign/references/harness-lanes.md
- plugins/test-campaign/skills/test-campaign/references/coverage-model.md
- plugins/test-campaign/skills/test-campaign/references/detector-defects.md
- plugins/test-campaign/skills/test-campaign/references/evidence.md
- plugins/test-campaign/skills/test-campaign/references/differential.md
- plugins/test-campaign/skills/test-campaign/references/selection.md
- plugins/test-campaign/skills/test-campaign/references/flow-coverage-axes.md
- plugins/test-campaign/skills/test-campaign/references/sweeps.md
- plugins/test-campaign/skills/test-campaign/references/campaign-prohibitions.md
- plugins/test-campaign/skills/test-campaign/references/project-comprehension.md
- plugins/test-campaign/skills/test-campaign/references/inert-ui.md
- plugins/test-campaign/skills/test-campaign/references/campaign-estimates.md
- plugins/test-campaign/skills/test-campaign/references/effect-boundary.md
- plugins/test-campaign/skills/test-campaign/references/journeys.md
- plugins/test-campaign/skills/test-campaign/references/on-glass.md
- plugins/test-campaign/skills/test-campaign/references/capture-lineage.md
- plugins/test-campaign/skills/test-campaign/references/instrument-calibration.md
- plugins/anvil-errand/README.md
- plugins/anvil-errand/skills/anvil-errand/SKILL.md
- plugins/anvil-errand/skills/anvil-errand/gemini.md
- plugins/shipyard/README.md
- plugins/shipyard/references/operational-rules.md
- plugins/shipyard/references/evidence.md
- plugins/shipyard/references/test-strategy.md
- plugins/shipyard/references/codex-cli.md
- plugins/shipyard/references/evidence-rules.md
- plugins/shipyard/references/tracker-adapter.md
- plugins/shipyard/references/executor-lanes.md
- plugins/shipyard/references/model-lanes.md
- plugins/shipyard/references/second-opinion-lanes.md
- plugins/shipyard/references/model-and-effort.md
- plugins/shipyard/references/comment-format.md
- plugins/shipyard/skills/design/SKILL.md
- plugins/shipyard/skills/design/gemini.md
- plugins/shipyard/skills/verify/SKILL.md
- plugins/shipyard/skills/verify/gemini.md
- plugins/shipyard/skills/plan/SKILL.md
- plugins/shipyard/skills/plan/gemini.md
- plugins/shipyard/skills/triage/SKILL.md
- plugins/shipyard/skills/triage/gemini.md
- plugins/shipyard/skills/intake/SKILL.md
- plugins/shipyard/skills/intake/gemini.md
- plugins/shipyard/skills/shipyard/SKILL.md
- plugins/shipyard/skills/shipyard/gemini.md
- plugins/shipyard/skills/gap-fix/SKILL.md
- plugins/shipyard/skills/gap-fix/gemini.md
- plugins/shipyard/skills/work/SKILL.md
- plugins/shipyard/skills/work/gemini.md
- plugins/shipyard/skills/work/references/miss-classes.md
- plugins/shipyard/skills/triage/references/spec-format.md
- plugins/shipyard/skills/triage/references/sentinel-review.md
- plugins/shipyard/skills/plan/references/plan-tiers.md
- plugins/warrant/README.md
- plugins/warrant/references/evidence.md
- plugins/warrant/references/script-contract.md
- plugins/warrant/references/tiers.md
- plugins/warrant/references/opus5-authoring.md
- plugins/warrant/references/positioning.md
- plugins/warrant/references/admissibility.md
- plugins/warrant/references/measurement.md
- plugins/warrant/references/why-not-a-jury.md
- plugins/warrant/skills/warrant/SKILL.md
- plugins/warrant/skills/warrant/gemini.md
- plugins/warrant/skills/ledger/SKILL.md
- plugins/warrant/skills/ledger/gemini.md
- plugins/warrant/skills/panel/SKILL.md
- plugins/warrant/skills/panel/gemini.md
- plugins/warrant/skills/ratchet/SKILL.md
- plugins/warrant/skills/ratchet/gemini.md
- plugins/warrant/skills/oracle/SKILL.md
- plugins/warrant/skills/oracle/gemini.md
- plugins/warrant/skills/feedback/SKILL.md
- plugins/warrant/skills/feedback/gemini.md
- plugins/warrant/skills/lot/SKILL.md
- plugins/warrant/skills/lot/gemini.md
- plugins/warrant/skills/charter/SKILL.md
- plugins/warrant/skills/charter/gemini.md
- plugins/warrant/skills/assay/SKILL.md
- plugins/warrant/skills/assay/gemini.md
- plugins/ship-feature/README.md
- plugins/ship-feature/skills/ship-feature/SKILL.md
- plugins/ship-feature/skills/ship-feature/gemini.md
- plugins/ship-feature/skills/ship-feature/references/deferred-work-loop.md
- plugins/ship-feature/skills/ship-feature/references/orchestration-model.md
- plugins/ship-feature/skills/ship-feature/references/e2e-and-finalize.md
- plugins/ship-fleet/README.md
- plugins/ship-fleet/skills/ship-fleet/SKILL.md
- plugins/ship-fleet/skills/ship-fleet/gemini.md
- plugins/ship-fleet/skills/ship-fleet/references/preflight.md
- plugins/ship-fleet/skills/ship-fleet/references/orchestrator-artifacts.md
- plugins/ship-fleet/skills/ship-fleet/references/scheduling-and-concurrency.md
- plugins/resume-session/README.md
- plugins/resume-session/skills/resume-session/SKILL.md
- plugins/resume-session/skills/resume-session/gemini.md

## Reviewed generated instruction fragments

- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/admin.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/api.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/footer.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/header.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/ios.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/macos.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/rn.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/rust.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/tokens.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/arch/web.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/caddy/admin.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/caddy/api.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/caddy/header.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/caddy/web.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/admin.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/api.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/auth.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/data.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/footer.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/header.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/ios.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/macos.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/observability.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/push.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/rn.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/rust.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/tokens.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/waitlist.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/claude/web.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/compose/api.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/compose/data.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/compose/footer.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/compose/header.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/compose/web.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/deploy/admin.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/deploy/api.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/deploy/header.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/deploy/ios.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/deploy/macos.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/deploy/rn.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/deploy/web.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/next-steps/header.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/admin.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/api.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/auth.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/data.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/header.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/ios.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/macos.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/observability.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/push.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/rn.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/rust.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/tokens.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/waitlist.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/readme/web.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/testing/api.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/testing/footer.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/testing/header.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/testing/ios.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/testing/macos.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/testing/rn.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/testing/rust.tmpl
- plugins/create-swe-project/skills/create-swe-project/templates/fragments/testing/web.tmpl

## Independent-review correction pass

An independent review found missed consumer contradictions and a malformed deferred-work reference introduced during normalization. Corrected the exact `shipyard:work`/`shipyard:plan` invocation spans, restored `docs/plans/plan-<CHILD_ID>.md` and spec/plan prose, and scanned changed workflow documents for the same malformed shapes (zero remaining).

Propagated the new policy through e2e-and-finalize.md, verify's Gemini sidecar, triage/plan review consumers, operational-rules.md, executor retry/kill-switch prose, fleet preflight and the generated ORCHESTRATOR.md resume template. These now use actual writer-relative independence, authorized capable fallbacks, conditional evidence-driven follow-up and the same conservative/zero-capacity scheduling rule. No same-family extra round is portrayed as restoring independence. The wire-evidence contract now consistently distinguishes requested/resolved/actual serving metadata from config-echo headers and broad tier strings.

Final repair checks: `/tmp/skill-review-workflow-repair-audit.json` has zero reference findings; scoped `git diff --check` exits 0. No versions were bumped by this correction pass.
