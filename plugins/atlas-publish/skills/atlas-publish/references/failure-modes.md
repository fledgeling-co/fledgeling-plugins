# Named failure modes

Nine traps that have each cost a real debugging cycle on this repo, plus the per-step abort paths.
Each entry gives the symptom, the detection, and the fix. They share one shape: the step reports
success and the damage appears somewhere the step was not looking.

When one of these fires, report three things: the trap by its number and name, the observable that
detected it, and whether you applied the fix or stopped.

## 1 — The buildNumber fingerprint trap

**Symptom.** A JS-only-looking change is classified OTA, the bundle registers without error, and
no device is ever offered it. Nothing errors.

**Cause.** `ios.buildNumber` is inside the expo-updates fingerprint. Measured: buildNumber 2 →
`4135716c…`, buildNumber 3 → `fd05b8d3…`. A bump alone moves the runtimeVersion, so the bundle
registers at a fingerprint no shipped binary carries.

**Detection.** Compute `npx expo-updates runtimeversion:resolve --platform ios` before and after the
merge wave and compare, rather than reasoning about the diff. Full detail: `classification.md`.

**Fix.** Different fingerprint means the store lane. Also check `plugins/`, `ci_scripts/` and a
from-scratch pnpm resolve, all of which move it without touching `app.json`.

## 2 — The OTA channel has never published

**Symptom.** The OTA lane is presented to the founder as the proven path when nothing has ever been
served over it.

**Detection.** `list_releases` returns no bundles and no versions; `apps/atlas-app/ota/bundle.json`
reads `bundleNumber: 0`. Re-check both at the start of a run rather than trusting this note.

**Fix.** Say plainly that the lane is unexercised, and that with no release record there is no way to
confirm what fingerprint an installed binary carries. Run the cert-parity gate before any export.

## 3 — The cert-parity gate that passes without checking

**Symptom.** `pnpm --filter atlas-api test tests/unit/lib/ota-cert-parity.test.ts` exits 0, the run
records the gate as passed, and every OTA update is rejected on-device after the next store release.

**Cause.** The live parity assertion runs under `it.runIf(!!parityKey)`, keyed on
`OTA_CERT_PARITY_KEY`. Without that env var it is skipped and a CI-safe sentinel test passes in its
place. The exit code cannot distinguish the two outcomes. This is the whole class in one file: a
gate whose pass and whose cannot-run look identical is not a measurement.

**Detection.** The test named
`the committed cert verifies a signature made with the configured private key` must read **passed**
in the vitest output. Reading `skipped` means the gate is not-run.

**Fix.** Supply the production key:

```bash
OTA_CERT_PARITY_KEY="$OTA_CODE_SIGNING_KEY" \
  pnpm --filter atlas-api test tests/unit/lib/ota-cert-parity.test.ts
```

Pull `OTA_CODE_SIGNING_KEY` from Vercel (atlas-api project, Sensitive) or atlas-api's `.env.local`.
A real failure means the committed `apps/atlas-app/certs/ota-cert.pem` and the server's private key
are not a pair. Stop: a JS-only OTA cannot fix a signing mismatch, because the manifest carrying the
fix is the thing being rejected. Restore the matching pair, or generate a fresh pair and ship a store
build.

## 4 — The two fastlane xcargs gotchas

**Symptom A.** The archive succeeds and `exportArchive` dies with `No Accounts` or
`No signing certificate "iOS Distribution" found`.

**Cause.** `-allowProvisioningUpdates` alone asks Xcode's *accounts* for authority, and this machine
may hold only Apple Development certs. gym has no `api_key` option (checked against 2.236.1) and
never emits the authentication flags itself.

**Fix.** Pass `-authenticationKeyPath` / `-authenticationKeyID` / `-authenticationKeyIssuerID` to
xcodebuild so it can provision signing on its own. Already wired in the Fastfile's
`asc_signing_xcargs`.

**Symptom B.** `option '-authenticationKeyPath' may only be provided once`.

**Cause.** gym's export command appends **both** `export_xcargs` and `xcargs`
(`package_command_generator_xcode7.rb`), so setting the flags in both sends each twice.

**Fix.** Put them in `xcargs` only — that alone reaches the archive *and* the export.

## 5 — The CocoaPods PATH trap

**Symptom.** The build dies on a missing `Atlas.xcworkspace` after `expo prebuild` reported success.

**Cause.** Prebuild's CocoaPods auto-install fails quietly — the gem install exits 1, and brew
installs without linking (its hint is `brew unlink cocoapods && brew link cocoapods`). `pod install`
then never runs, and prebuild does not treat that as fatal.

**Fix.** Run `pod install` in `apps/atlas-app/ios/` by hand, then re-run the lane with
`SKIP_PREBUILD=1` so the pods survive the next `--clean`.

## 6 — The dev .env inlining footgun

**Symptom.** A registered bundle points at `localhost:3000`. Export, upload and registration all
succeeded.

**Cause.** `EXPO_PUBLIC_*` are inlined at export time and Expo auto-loads `apps/atlas-app/.env`.
Xcode Cloud avoids this only because its clone has no `.env`; a local export does not.

**Detection and fix.** Export with `EXPO_PUBLIC_API_URL` set explicitly to the production host, then
grep the emitted `.hbc` for the prod host (expect at least one hit) and for `localhost:3000` (expect
zero) before uploading. Commands in `ota-lane.md`.

## 7 — The VERCEL=1 pre-push gap

**Symptom.** The pre-push gate passes and the Vercel cloud build fails on the same commit with
`ENOENT … next-server.js.nft.json`.

**Cause.** Next 16.3 + Turbopack skips `collectBuildTraces`, so the trace file is never written and
`output: 'standalone'` dies reading it. It only fires on Vercel, because `modifyConfig` there takes a
different path than a local build. The four Next apps therefore set
`output: process.env.VERCEL ? undefined : 'standalone'`, and the pre-push hook exports `VERCEL=1` so
its `vercel build` exercises the same branch the cloud does.

**Detection.** The hook already does this. It matters here because `SKIP_VERCEL_BUILD=1` skips the
stage entirely — an app-only push is the only case that justifies it, and using it means the gate is
reported as not-run.

**Fix if a deploy fails anyway.** Iterate against the real builder, not locally: copy
`apps/<app>/.vercel` to the repo root, then from the root run
`vercel deploy --scope bella-app --archive=tgz` (the archive flag is required; the repo exceeds the
15,000-file upload limit). Read a failed build with
`vercel inspect --logs --scope bella-app <url>` — without `--scope bella-app` the CLI looks in
`luke-personal` and reports the deployment as not found.

## 8 — The stacked-branch delete

**Symptom.** Merging a PR with `--delete-branch` orphans the PRs stacked on top of it; their base ref
disappears and they close or retarget silently.

**Detection.** Before merging, `gh pr list --json number,baseRefName` and note any PR whose base is
another PR's head.

**Fix.** Omit `--delete-branch` on any PR that is a base for another. Merge parents first, then
rebase each child onto `main` before merging it.

## 9 — The duplicate bundle number

**Symptom.** `register_bundle` returns a 409 conflict.

**Cause.** `bundleNumber` is unique-indexed; a previous attempt already registered it.

**Fix.** `get_release { bundleNumber: N }` to see what is actually stored. If it is the bundle you
intended, the earlier attempt succeeded and the recovery is to stop, not to re-register. If it is a
different bundle, bump `ota/bundle.json` again and register the next number with a fresh export.
Never re-target a consumed id.

## The merge wave loses work quietly

Not a trap in one command, but the shape a multi-PR wave fails in: a fan-out reports `completed`
while a fraction of its items never came back, and the truth sits beside the status rather than in
it. One measured set of runs: 96 started against 61 returned, 128 against 78, 107 against 55.

The completion test is **started-versus-returned parity**, so record the PR numbers at Step 1 and
reconcile them at Step 4:

```bash
gh pr view <n> --json number,state,mergedAt,mergeCommit
git merge-base --is-ancestor <mergeCommitSha> origin/main && echo on-main
```

A PR is merged when it reports `MERGED` **and** its commit is an ancestor of `origin/main`. A
process exiting zero is not the same claim. List by number every PR from the Step 1 set that is not in the
merged set, and stop rather than continuing with a partial wave.

## Per-step abort paths

| Step | If it fails | Abort |
|---|---|---|
| 0 preconditions | any check failed or not-run | stop before any write; report the one fixing command |
| 1 classify | fingerprint unresolvable | stop; fix the config, do not infer the lane from the diff |
| 2 back-compat | a DTO field removed or renamed | stop; explain the field-level break and the additive alternative; continue only on explicit founder override |
| 3 review | a review finds a defect | fix on the PR branch and push; the wave has not started, so nothing to unwind |
| 4 merge | conflict or a lost PR | `git merge --abort` or `git rebase --abort`, leave `main` at its pre-step ref, report the PR numbers not merged |
| 5 tests | a suite fails | fix or revert the offending commit on `main`; `main` is unpushed at this point, so `git reset --hard` to the pre-step ref is available |
| 6 versions | wrong bump | amend before pushing; unpushed tags delete with `git tag -d` |
| 7 notes | founder unavailable | stop the store lane here; the OTA lane can proceed with a one-line note |
| 8 archive | build or signing fails | nothing has reached Apple; fix and re-run. Past the TestFlight upload the build number is consumed — go forward to the next number, never retry the same one |
| 9 register | 409, or a read-back mismatch | see trap 9; forward to the next bundle number |
| 10 push | gate fails | fix on `main` and re-run the gate; `--no-verify` is not the fix |
