# Research notes — what the 5-backend Dossier panel found (2026-08-07)

Panel `dr_63ac10b56c131b28`: openai `dr_49b878ae294d4343` · local-claude `dr_98174bc9e00836f7` · gemini `dr_581a057f4d4fcf5f` · perplexity `dr_f458d3193c7c1a33` · xai `dr_ad1f8d171eadfa76` (full reports: `~/.dossier-research-mcp/reports/<runId>.md`). All five read in full; 165 sources, 62 domains, 7% overlap. This file records what slipway already encodes, and the prioritized roadmap the research argues for — read it before making structural changes to the skill.

## Findings already encoded in slipway

- **Script-first / interview-only is the documented best practice, not a style choice.** Vercel's evals: 53% baseline → 79% skills → 100% always-on AGENTS.md facts on post-cutoff Next 16 APIs; Anthropic classifies fragile batch operations as "low freedom — run exactly this script". Bundled templates cost zero context until executed.
- **Provenance is the cheapest insurance** (shadcn's `diff` is broken because it records no versions) → `.slipway/manifest.json` in every generated project.
- **Template rot is operationally real** (turborepo#5592 pinned a broken pnpm; next.js#71703 shipped a broken default template; fresh Expo scaffolds rejected by Expo Go) → `scripts/canary.sh` scaffolds all modules and runs the gate; run it weekly (ship-armada daemon).
- **One defaults gate, few questions** (create-next-app 16 collapsed 7 prompts → 1; T3's "must solve a core problem" policy) → single AskUserQuestion round; only architecture-altering questions.
- **Dry-run + refuse-to-overwrite are table stakes** → `--dry-run`, existing-dir refusal.
- **notarytool-only pipeline** with `ditto` (zip/cp break the seal), staple, `stapler validate`, `spctl` assess; CI passes ASC API-key creds (keychain profiles aren't exportable).
- **Known ecosystem facts baked into templates**: Next 16 removed `next lint` (direct flat ESLint), Node ≥20.9 floor, `proxy.ts` not `middleware.ts` (noted in next.config comment), Next 16.2+ vendors docs at `node_modules/next/dist/docs/` (noted in generated CLAUDE.md), pnpm 10 `onlyBuiltDependencies` (pnpm 11 renames to `allowBuilds`, Node ≥22 — comment in pnpm-workspace.yaml), Nest SWC monorepo caveat only applies to Nest CLI's own monorepo mode.

## Prioritized roadmap (not yet built — implement in this order)

1. **Idempotent re-run + state inventory** (openai's "required contract"): `.slipway/state.json` with generated-file hashes; re-run of unchanged config = zero changes; refuse changes to user-modified files without `--diff`/`--force`. This is the gateway to everything below.
2. **Plan artifact**: `slipway plan` emitting the JSON file/port/package plan before mutation (Nx virtual-FS precedent; Anthropic plan-validate-execute). Today `--dry-run` prints a summary; a machine-readable plan enables confirmation UIs and eval assertions.
3. **Upgrade lifecycle** (Copier's model — the "update story" is the defining feature of surviving scaffolders): tagged template versions + `slipway upgrade` three-way diff against the provenance manifest. CRA died and Yeoman froze without one.
4. **pnpm catalogs** (`catalog:` in pnpm-workspace.yaml) for shared external ranges across apps — the pinning middle ground (policy ranges + exact lockfile).
5. **Ownership markers**: label generated files as generator-owned vs user-owned starter code (projen vs shadcn poles; the market rewards a dial). Prerequisite for safe upgrades.
6. **Wildcard local HTTPS profile**: Caddy's internal CA covers `.localhost`/`.local` automatically — an opt-in `--https` profile after a doctor check, never a prerequisite.
7. **`doctor` subcommand**: report Node/pnpm/Docker/Xcode/xcodegen/cargo/op/caddy availability before scaffolding, machine-readable.
8. **Sentry/observability module** — dAIolog runs @sentry/nextjs + node everywhere; wiring needs instrumentation files + DSN env, so it's a real module, not a dep line. Ask-at-interview once built.
9. **Standardize the loupe/tare operating-rules/kill-switch section** — the portfolio survey flagged their CLAUDE.md agent kill-switch/egress policies as worth rolling out; distill into a claude fragment once read.
10. **Eval harness** (skill-creator style): assert fresh scaffold → `pnpm install && turbo build` + `xcodegen generate && xcodebuild build` pass — the canary generalized into per-module permutations.

## Cautions the research flags

- Vercel's 53/79/100 eval is Vercel grading its own approach — directionally strong, no independent replication.
- Port-allocation conventions have **no** primary source — slipway's Caddy-scan allocation + recording in the manifest is itself a differentiator; keep it.
- Supply-chain: the Nx s1ngularity attack specifically weaponized local AI CLIs — keep slipway's dependency count at zero (bash+python+node stdlib only) and the marketplace private.
- Don't add Nx/projen as runtime deps to inherit their generator semantics — reproduce the guarantees (dry-run, state, composition) in the script instead.
