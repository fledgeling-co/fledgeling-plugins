# Evidence — where each rule in this skill came from

Every structural choice in `SKILL.md` and the five reference files traces to one of
four places: a research report, the Claude Code built-in review architecture, a fact
measured in the Atlas repo, or a trap recorded in this project's memory and then
re-verified. A rule nobody can source is a rule nobody should follow.

The research corpus is exported to `docs/deep-research/code-review-*.md` at the root
of this marketplace, so every claim below is readable without leaving the repo.

## The rules, and what each one rests on

| Rule in the skill | Source | Status |
|---|---|---|
| Each lane announces a one-line pipeline contract before Step 1 | The Claude Code built-in `code-review` skill states a budget line per effort tier (`high effort → 8 inline angles → dedup (no verify) → ≤10 findings`) at the top of its run | Adapted; `docs/deep-research/code-review-claude-code-builtin.md` |
| Six irreversible steps each name the observable to read back | `silent` — a driver returned ok and nothing happened | Direct; `docs/deep-research/code-review-silent.md` |
| Two witnesses that share a failure mode are not a cross-check | `silent` | Direct |
| Gates report passed, failed and not-run as three states | `vacuous` — a suite passed a guarantee it never ran | Direct; `docs/deep-research/code-review-vacuous.md` |
| The cert-parity gate must read `passed`, never `skipped` | `vacuous`, applied to `apps/atlas-api/tests/unit/lib/ota-cert-parity.test.ts` | **Measured in the repo.** The real comparison sits behind `it.runIf(!!parityKey)` and its companion asserts `expect(true).toBe(true)`, so with `OTA_CERT_PARITY_KEY` unset the file exits 0 having compared nothing |
| Step 4 reconciles PRs started against PRs merged | `workflows` — the wave finished and a third of it never came back | Direct; `docs/deep-research/code-review-workflows.md` |
| Draft is terminal, and the reason is reproducibility rather than caution | `cadence` — how much checking a thing earns tracks how reproducible it is. A draft can be rebuilt and discarded; a published bundle cannot, at any level of checking | Direct; `docs/deep-research/code-review-cadence.md` |
| Probe the capability the lane needs, never a generic green | `dispatch` — the runner was never the thing that failed | Direct; `docs/deep-research/code-review-dispatch.md` |
| The build runs on a credentialed Mac, and that is a trust boundary | `egress` — self-hosted runner security and economics | Partial; `docs/deep-research/atlas-publish-egress.md`. Atlas does not self-host Actions runners, so only the credentialed-machine note carried across, in `store-lane.md` |
| Rollback path stated before the deploy step, not after | `knowledge-work-plugins/engineering/skills/deploy-checklist` | Adapted |
| Three-state verdict phrasing in the hand-off | `knowledge-work-plugins/engineering/skills/incident-response` | Adapted |

## Facts measured in the Atlas repo

These were checked against the source rather than carried from memory or from the
skill this one replaces.

- **`ios.buildNumber` is inside the expo-updates fingerprint**, so bumping it alone
  forces a store release. Confirmed structurally: `app.json` sets
  `runtimeVersion: { policy: "fingerprint" }` and `ios.buildNumber: 3`, and the
  fingerprint's `DEFAULT_SOURCE_SKIPS` does not exclude it. The two hashes were not
  re-computed; that half is carried from the project memory note.
- **The OTA channel has never been used.** `ota/bundle.json` reads
  `{"bundleNumber": 0}` and no bundle has been published.
- **Both Fastlane `xcargs` traps and the CocoaPods PATH trap** are recorded verbatim
  in `apps/atlas-app/fastlane/Fastfile` comments.
- **The `VERCEL=1` pre-push gap** is real: `.husky/pre-push` and both
  `next.config.mjs` files confirm the config branch.
- **The connector URL is `/connector`**, not the older `/api/mcp/mcp`.

## One correction to the skill this replaces

The predecessor called `npx @expo/fingerprint`. That package is not a declared
dependency of the workspace (only a transitive `0.19.9`), so `npx` fetches a
floating version, and `expo-updates` passes its own `ignorePaths` — the two can
disagree, which is the worst possible failure for a classification step. This skill
uses `npx expo-updates runtimeversion:resolve` and `fingerprint:generate`, both
verified present in the installed CLI.

## What is not evidenced

The skill has not been run end to end against a real release, and no eval has been
executed. `../../../evals/EVALS.md` states that plainly and names the cases that would
settle it. The `@vercel/blob` `put` call shape is written against the installed
`2.4.0` type signature; no upload was executed to confirm it at runtime.
