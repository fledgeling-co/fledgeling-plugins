---
name: atlas-publish
description: >-
  Atlas/Bella release conductor — take the open PRs to a registered draft release, on the OTA lane or the App Store lane. Use when someone wants Atlas work in front of users: "ship an Atlas release", "publish an OTA update", "release the app", "cut a new Atlas build", "push a JS-only update to users", "do a full App Store release", "get the merged work out". Classifies OTA-only vs App Store from the expo-updates native fingerprint (ios.buildNumber is inside it, so a buildNumber bump alone forces a store release), runs the API back-compat and OTA cert-parity gates with not-run reported apart from passed, reviews and merges the open PRs by number with a started-vs-merged reconciliation, reconciles tests, bumps app.json version and ota/bundle.json, asks the founder for the TestFlight What-to-Test notes before any store build, archives via Fastlane, exports via expo export, uploads bundle bytes straight to Vercel Blob, and registers the result as a DRAFT through the atlas-admin MCP. Draft is where automation stops — publish_bundle, publish_app_version, retract and set_min_app_version are founder actions and this skill does not call them. NOT for reviewing a diff on its own (use the code-review skill) and NOT for publishing an already-registered bundle.
allowed-tools: Read, Grep, Glob, Bash, Agent, Write
---

# atlas-publish — Atlas release conductor

You take the currently-open PRs in the Atlas monorepo and drive them to a **registered draft
release** — either an over-the-air (OTA) JavaScript bundle or an App Store binary. The heavy
work is real: you merge branches, archive a binary, upload it to TestFlight, export a JS bundle,
put bytes in a public Blob store, and write release rows to production Mongo.
The one thing you do not do is make any of it reach an end user.

You run in the founder's Claude Code on their Mac, against production infrastructure.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It turns the zero-publish rule, the Step 0 gate states, the per-asset upload denominator and the review-per-PR count into ledgers with read-back commands, and names which of Steps 3 and 5 to hand to another model. Other models skip it.

## Why draft is where automation stops

Not because the step is hard, and not because you might get it wrong. A draft OTA bundle and a
TestFlight build are **re-buildable artifacts** — a bad one is deleted, re-exported and registered
again inside one export cycle. A published bundle is not: it lands on phones you do not
control, and retracting it changes what the *next* boot serves rather than undoing the one that
already happened. Tolerance tracks how reproducible the target is, not how good the checking is,
so no amount of extra checking moves a customer-facing publish inside the envelope.

Concretely, this skill calls `register_bundle` and `create_app_version`, each with `confirm: true`,
and each only ever writes `status: draft`. It does not call `publish_bundle`, `publish_app_version`,
`retract_bundle`, `retract_app_version` or `set_min_app_version`. When you reach the end of a run,
hand the founder the three publish routes (`references/handoff.md`) and stop.

The boundary is restated at Step 9 and Step 11, where the temptation actually sits — a rule stated
once in frontmatter and needed nine steps later is a rule the run has already forgotten. Measured
reason: instruction-following degrades 39% on average from single-turn to multi-turn across 15
models, which is why the gates below are exit codes rather than paragraphs.

## The two lanes, and their contracts

State the lane and its contract in the first message of the run, before Step 1 finishes, so the
founder knows what the run will do before it does any of it.

```
OTA lane   → classify → 2 gates → review+merge N PRs → tests → bundle bump → export → upload → register draft → push
Store lane → classify → 2 gates → review+merge N PRs → tests → version bump → notes ask (blocks) → archive → TestFlight → create_app_version draft → export+register draft → push
```

Every store release also produces an OTA bundle, so the new binary has a bundle lineage at its own
fingerprint. There is no store-only run.

Estimates are calibrated for an M4 Pro 14-core MacBook Pro; the ~104 s archive anchors Step 8.
Announce `Step k/N — <name> (~est)` with a running remaining total, and recompute it as you go.

## Evidence rule — read the observable, not the return value

A tool returning success is a statement that the call was well-formed. It is not evidence the thing
happened. The failure shape is always the same: a structurally valid call that lands nowhere, and
nothing refuses it. One audit of an MCP server found `stop_runner` reporting `ok=true` with the
runner still present, `restart_runtime` returning "restarted successfully" having restarted nothing,
and 230 passing tests that walked past both — because 26 of its 32 state-changing tests never
re-read what they had changed.

So after each irreversible step, read the thing the step was supposed to change:

| After | Read back | Fail if |
|---|---|---|
| `gh pr merge` | `git log --oneline origin/main` for the merge/squash commit, and `gh pr view <n> --json state,mergedAt` | the PR is not `MERGED`, or its commit is not an ancestor of `origin/main` |
| Blob upload | `curl -sSI <returned blob url>` | not `200`, or `content-length` differs from the local file's byte count |
| `register_bundle` | `get_release { bundleNumber: N }` | absent, `status` is not `draft`, or `launchAssetUrl` is not the URL you uploaded |
| `create_app_version` | `get_release { version: "X.Y.Z" }` | absent or `status` is not `draft` |
| Fastlane upload | the founder's App Store Connect TestFlight list, or the lane's own `upload_to_testflight` build number echoed back | the build number is not the one the lane stamped |
| `git push` | `git rev-parse origin/main` equals local `HEAD` | they differ |

Two witnesses that are both suspect are not a cross-check. A build log saying "Archive Succeeded"
and a fastlane summary line saying the same come from the same process; the independent witness is
the artifact on App Store Connect.

Also address things by id, never by pattern: bundle number, PR number, semver, commit sha. "The
latest build" and "the newest bundle" resolve to different things depending on when you look.

## Gate reporting — passed, failed, and not-run are three states

A gate that could not run reports **not-run**, with the reason and what would make it runnable. It
never reports passed. The worked example is in this repo:

`OTA_CERT_PARITY_KEY="$OTA_CODE_SIGNING_KEY" pnpm --filter atlas-api test tests/unit/lib/ota-cert-parity.test.ts`

Without that env var the file exits 0 with the live parity assertion **skipped** and a CI-safe
sentinel passing in its place. A green exit code therefore proves nothing about cert⇄key parity, and
parity failing in the field makes every signed manifest rejected on-device — which no OTA can fix,
because the rejection is of the manifest that would carry the fix.

The detection is mechanical: the run must show the test named
`the committed cert verifies a signature made with the configured private key` as **passed**, not
skipped. Report the gate as not-run whenever that line reads `skipped`, and stop the OTA lane there.

Apply the same rule to any preflight below: name the observable that proves it ran, not just the
exit code.

## Step 0 — Preconditions

Check these before any work, and report each as passed, failed, or not-run:

1. Clean working tree on `main` — `git status --porcelain` empty, `git rev-parse --abbrev-ref HEAD`
   is `main`.
2. `gh auth status` succeeds.
3. `pnpm doctor` exits 0 (`sh scripts/dev-doctor.sh --strict`) — this is what proves the `vercel` CLI
   and the three per-app project links the pre-push gate needs are present.
4. The `atlas-admin` MCP responds — call `list_releases`. If it does not, walk the founder through
   the admin console's **MCP** page (create a key, paste the `claude mcp add …` line) or the Claude
   app connector at `https://admin.atlasapp.au/connector`, then re-check.
5. **Store lane only:** `bundle exec fastlane --version` from `apps/atlas-app`, `fastlane/.env`
   present with the App Store Connect (ASC) API credentials `ASC_KEY_ID` / `ASC_ISSUER_ID` /
   `ASC_KEY_FILEPATH`, and
   `security find-identity -v -p codesigning` listing an `Apple Distribution: Bella App Pty Ltd
   (73P7R889WA)` identity.
6. **OTA lane only:** the cert-parity gate above, read for the passed line rather than the exit code.

Probe the specific capability the lane needs rather than asking a general "is everything fine".
Two surfaces of the same service are separately gated — an account that can write a commit status
can be blocked from running a job, and the generic check reports neither.

On a failed precondition, stop and tell the founder the one command that fixes it.

## Step 1 — Classify the release

The lane comes from the expo-updates fingerprint, and nothing else. Run it from `apps/atlas-app`:

```bash
npx expo-updates runtimeversion:resolve --platform ios   # the exact runtimeVersion a client sends
npx expo-updates fingerprint:generate --platform ios      # the same hash, plus its sources
```

Take the value on `main` at the merge base, then again after the merge wave, and compare. Identical
⇒ **OTA lane**. Different ⇒ **App Store lane**.

Use `expo-updates`, not `npx @expo/fingerprint`. `@expo/fingerprint` is not a declared dependency
here, so `npx` would fetch a floating version from the registry, and expo-updates passes its own
options and ignore paths — the two commands can return different hashes for the same tree, and only
the expo-updates one matches what the binary reports.

`ios.buildNumber` is **inside** the fingerprint. Measured on this repo: buildNumber 2 →
`4135716c5839e5fa58bd3854580e57a0ca3ef814`, buildNumber 3 → `fd05b8d3980fae3c9b98345f048203726fd0653b`.
So bumping the build number alone forces a store release. The failure mode this prevents: a run
that reasons "this is only a JS change, so it is OTA-able", registers a bundle at the new
fingerprint, and ships a bundle no binary in the field will ever be offered.

The full decision, the source-level reason `ios.buildNumber` is not stripped, and what to do when the
resolve command fails: `references/classification.md`.

## Pipeline

| # | Step | Lane | ~est |
|---|---|---|---|
| 1 | **Classify.** `gh pr list --json number,title,headRefName` — record the PR numbers now; they are the completion set for Step 4. Fingerprint before/after per Step 1. Announce the verdict and the reasoning in plain English. | both | 1–2 min |
| 2 | **API back-compat gate.** If any PR touches `apps/atlas-api/lib/dto.ts`, `lib/zod.ts` or `app/api/**/route.ts`, run the §1 guards (`pnpm --filter atlas-api test tests/unit/lib/dto-contract.test.ts` and `apps/atlas-app/lib/api/contract.test.ts`) and diff the key-sets of the server's data transfer objects (DTOs) against the client's wire types. atlas-api deploys on push to `main`, so a merged API change is live before any client update — a removed or renamed field breaks phones that have not updated yet. A breaking change stops the run; explain to the founder what an old app would see and what the additive alternative is, and continue only on an explicit override. | both | 1–3 min |
| 3 | **Review every open PR** with the `code-review:code-review` skill, one review per PR number from Step 1. Post the review with `gh pr comment <n>`, apply fixes for real findings, push to the PR branch. | both | 3–8 min/PR |
| 4 | **Merge wave.** Rebase each PR onto `main`, resolve conflicts, merge, `git pull` after each. Omit `--delete-branch` on a stacked child, which orphans its siblings. Then reconcile: the set of PR numbers from Step 1 against the set now `MERGED` with an ancestor commit on `origin/main`. A wave that reports done with a smaller returned set than started set has lost work; name the missing numbers rather than continuing. | both | 1–2 min/PR |
| 5 | **Test reconciliation** on the merged diff — add or update the vitest suites (pure `lib/`) and the Maestro flows the change needs, then `pnpm turbo run lint typecheck test`, fix failures, commit to `main`. Pre-warm the turbo cache before pushing; the bash tool caps at 10 minutes. | both | 5–15 min |
| 6 | **Version bookkeeping.** Store: bump `app.json` `version` (user-visible feature ⇒ minor, fix or copy ⇒ patch), commit `chore(atlas-app): bump app version to X.Y.Z`, tag `vX.Y.Z` after reading the tag decision below. Both lanes: bump `apps/atlas-app/ota/bundle.json`, commit `chore(atlas-app): OTA bundle N`, tag `bundle-N`. | both | <1 min |
| 7 | **Release notes — blocking.** Store lane: ask the founder for the What's New / TestFlight What to Test text, write the whole of it to `TestFlight/WhatToTest.en-US.txt`, commit before tagging or pushing. This is a hard rule from the repo's own `CLAUDE.md`, and Xcode Cloud and Fastlane both read that exact file, so stale notes ship silently. Do not draft the notes and proceed. OTA lane: ask for a one-line `notes` string for the release record. | both | founder-paced |
| 8 | **Store build.** `bundle exec fastlane release` from `apps/atlas-app` — gate, prebuild with prod env, ASC-derived build number, archive, TestFlight upload with the notes attached. Read back the TestFlight build per the evidence rule, `open` the `.xcarchive`, then `create_app_version` (`confirm: true`, status draft, with the resolved runtimeVersion). Procedure and its four named traps: `references/store-lane.md`. | store | archive ~2 min; gates+prebuild+pods ~4–6 min; upload ~2–4 min |
| 9 | **OTA bundle.** `npx expo export --platform ios` with the production env, read `dist/metadata.json`, `request_bundle_upload` once per file, PUT the bytes straight to Blob, then `register_bundle` (`confirm: true`, draft). The upload token is valid 600 seconds — mint it per file, immediately before that file's upload. Procedure and the metadata mapping: `references/ota-lane.md`. **This registers a draft. Do not follow it with `publish_bundle`.** | both | export ~1–2 min; upload seconds |
| 10 | **Push `main`** through the husky pre-push gate (lint · typecheck · test · `pnpm audit` · a real `vercel build` of the three web apps with `VERCEL=1`), then push tags. `SKIP_VERCEL_BUILD=1` is for an app-only push and nothing else. | both | 3–8 min (gate) |
| 11 | **Hand off.** What merged, the lane and why, the draft artifacts by id, and the three publish routes — the founder publishes, you do not. Template: `references/handoff.md`. | both | — |

## The tag decision

Pushing `vX.Y.Z` starts the Xcode Cloud **Release** workflow as well as this skill's Fastlane
archive, producing two TestFlight builds from one release. The fix is a one-time App Store Connect
change the founder makes: set the Release workflow to **manual start** and keep Beta-on-`main` as the
safety net. Until they have, warn before pushing any `v*` tag that a cloud build will also start,
and prefer the OTA lane where the fingerprint allows it.

## Named failure modes

Nine traps with their detection and their fix live in `references/failure-modes.md`: the
buildNumber fingerprint trap, the never-published OTA channel, the cert-parity skip, the two
fastlane `xcargs` gotchas, the CocoaPods PATH trap, the dev `.env` inlining footgun, the
`VERCEL=1` pre-push gap, the stacked-branch delete, and the duplicate bundle number. Read it before
Step 8 on the store lane and before Step 9 on either lane.

## Abort and rollback

Decide the abort before the step, not during it. Each step's named abort path is in
`references/failure-modes.md`; the OTA incident playbook, including retract, is in
`references/handoff.md` because retract is a founder action.

Two steps have no local undo, so treat them as the run's commit points: the TestFlight upload
(the build number is consumed and a re-run takes the next one) and a `register_bundle` that
succeeded (the bundle number is unique-indexed, and re-registering it returns a 409 conflict rather
than overwriting). Past either one, the recovery is forward — register the next number, or upload
the next build — never a retry of the same id.

## Delegation, narration, and length

Delegate to a subagent for two things only: the per-PR `code-review` pass when there are three
or more open PRs, and a wide investigation across the four apps when the back-compat gate at Step 2
flags a change you cannot trace by reading two files. Cap: 3 subagents for one release run. Do the
merge wave, the version bumps, the export and every MCP call in this session — subagents never run
git operations here, because the reconciliation at Step 4 depends on one process owning the ref.

Narration: announce the lane and its contract before Step 1 finishes, then one line per step in the
`Step k/N` form, plus a line whenever a gate reports not-run or a step changes the plan. The
hand-off at Step 11 is the only long message; hold it to 20 lines.

## References

- `references/classification.md` — the fingerprint decision, its commands, and what to do when it cannot be resolved.
- `references/store-lane.md` — Step 8 in full: the Fastlane lanes, the gates, signing, and the notes file.
- `references/ota-lane.md` — Step 9 in full: export, the `metadata.json` mapping, Blob paths, `register_bundle` arguments.
- `references/failure-modes.md` — the nine named traps, each with its detection and its fix, plus the per-step aborts.
- `references/handoff.md` — the Step 11 template, the three publish routes, and the retract/incident playbook.
- `references/evidence.md` — where each rule above came from, what was measured in the repo, and what is not evidenced.

Authoritative repo docs — open the one the current step names rather than reconstructing it: team rules in
`bella-team-files/CODING_PRACTICES.md`; the OTA runbook in `docs/atlas-app-OTA_UPDATES.md`; the store
pipeline in `docs/atlas-app-XCODE_CLOUD.md` and `docs/atlas-app-FASTLANE.md`; wire boundaries in
`docs/CONTRACTS.md` (§1 app↔api, §5 update channel); the MCP surface in
`docs/atlas-admin-CLAUDE_CONNECTOR.md`.

**Two containers, one skill.** On the plugin install path this triggers from a natural-language
request and the references above are bundled files. On the MCP path it is the slash command
`/mcp__atlas-admin__atlas-publish`, and the same content arrives as `get_atlas_skill_reference`
tool calls or `atlas://skills/…` resources. Use whichever of the two the session has; absolute
plugin paths resolve on neither.

Deliver the release at the scope asked. Make routine judgment calls yourself — patch versus minor,
which tests the diff needs, whether a review finding is worth a fix — and check in where two
readings would produce materially different work, such as a back-compat break at Step 2 or a
missing precondition. If the request looks mistaken, say so in a sentence and continue as asked
rather than quietly widening or narrowing it.
