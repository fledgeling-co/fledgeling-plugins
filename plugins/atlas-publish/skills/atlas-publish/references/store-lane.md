# Store lane — Step 8 in full

The App Store lane builds a signed archive on the founder's Mac with Fastlane, uploads it to
TestFlight with the notes attached, and records the version as a **draft** through the MCP. Apple
releases the binary; this skill records that a version exists and stops.

Full background: `docs/atlas-app-FASTLANE.md` (this path) and `docs/atlas-app-XCODE_CLOUD.md` (the
cloud alternative, still authoritative for non-skill releases).

## The notes come first, and they block

Step 7 is not a formality. `TestFlight/WhatToTest.en-US.txt` at the repo root is read by Fastlane's
`upload_to_testflight` and by Xcode Cloud, the **whole file** is the note, and the same text seeds
the App Store version's "What's New". Nothing checks whether it describes this build.

So: ask the founder for the text, write it, commit it, and only then run the lane. A run that
drafts plausible notes from the merged diff and proceeds has shipped a testing brief nobody wrote to
external testers. The repo's own `CLAUDE.md` states this as a hard rule for any archive, release or
TestFlight request.

Brand in that file is **Bella**, not Atlas — the code is Atlas, the shipping product is Bella.

## The lane

```bash
cd apps/atlas-app
bundle exec fastlane release              # gate → prebuild → build number → archive → TestFlight
bundle exec fastlane release submit:true  # …and submit for App Store review
bundle exec fastlane beta                 # TestFlight internal only
```

Six stages inside it, in order:

1. **gate** — `pnpm --filter atlas-app typecheck` + `test`. Parity with the Xcode Cloud unit gate.
   `SKIP_GATE=1` exists; using it means the run reports the gate as **not-run**, never as passed.
2. **prebuild** — `expo prebuild --platform ios --clean` regenerates `ios/` from `app.json` +
   `plugins/`, and `withSigningTeam.js` re-pins `DEVELOPMENT_TEAM = 73P7R889WA`. Forces
   `EXPO_PUBLIC_API_URL` to the production host first. `SKIP_PREBUILD=1` reuses the existing `ios/`.
3. **build number** — `CFBundleVersion` = latest TestFlight build + 1, read from App Store Connect.
   This **overrides** `app.json`'s `ios.buildNumber`, so that value only matters on the Xcode GUI
   path and for the fingerprint.
4. **build** — `build_app` (gym): Release configuration, `app-store` export, automatic signing.
5. **upload** — `upload_to_testflight`, internal, changelog attached from the notes file. A log line
   reading "Successfully set the changelog for build" is the observable that the notes landed.
6. **submit** — only with `submit:true`. Sets What's New, selects the build, submits for review.

Run `bundle exec fastlane release` without `submit:true` unless the founder asked for submission in
this run. Submission is outward-facing and reversible only through Apple.

## What the lane needs, checked at Step 0

- **App Store Connect API key.** In 1Password as `Bella Apple Connect API` (Dossier vault) with
  `AuthKey_5KG3T4JM48.p8` attached and the issuer id in its notes. Passed as `ASC_KEY_ID` /
  `ASC_ISSUER_ID` / `ASC_KEY_FILEPATH` via `apps/atlas-app/fastlane/.env`. It authenticates as the
  key's own role rather than the founder's Apple ID, which is what clears the old
  `No Account for Team "73P7R889WA"` wall.
- **A signing identity** — the distribution certificate *and* its private key in the login keychain.
  `security find-identity -v -p codesigning` must list
  `Apple Distribution: Bella App Pty Ltd (73P7R889WA)`. A `.cer` alone cannot sign; the fix is a
  `.p12` from the Mac that made the CSR, or a fresh cert created from this Mac.
- **Xcode 26.4.** SDK 56 does not compile on 26.0.1.

That Mac holds both the signing key and the ASC API key, and it also runs `pnpm install` lifecycle
scripts for the whole monorepo. Treat it as a credentialed host: the release path and any untrusted
dependency install share one filesystem, and no `--ephemeral` flag exists locally to reset it.

## Reading back the upload

The lane's own summary is not independent evidence — the archive log and the fastlane summary come
from the same process. The independent witness is App Store Connect: the build number the lane
stamped, appearing in the TestFlight list. `open` the `.xcarchive` for the founder as well, so
there is a local artifact they can inspect.

If the upload is rejected for a duplicate build number, the previous attempt reached Apple. Re-run;
the lane reads the latest TestFlight build again and takes the next number. Never re-target the
same number.

## Recording the version

After the upload lands, call `create_app_version` with `confirm: true`:

| Argument | Value |
|---|---|
| `version` | `app.json` `expo.version`, semver, e.g. `1.3.1` |
| `runtimeVersion` | the value from `npx expo-updates runtimeversion:resolve --platform ios` on the merged tree |
| `buildNumber` | the `CFBundleVersion` the lane stamped, as a string |
| `gitTag` | `vX.Y.Z` |
| `notes` | the first line or two of the What's New text |

It writes `status: draft`. Read it back with `get_release { version: "X.Y.Z" }` and confirm the
status. A draft App Store version advertises nothing; the founder marks it published only once Apple
has actually released the build, and that publish is what prompts older apps to update.

## Then the OTA bundle

Every store release also runs Step 9, so the new binary has a bundle registered at its own
fingerprint. Skipping it leaves a runtimeVersion with no bundle lineage, and the first OTA fix for
that binary then has no predecessor to fall back to on retract.

## Not this skill's job

Setting up screenshots, description, keywords, privacy or pricing for a first `1.x` version; the
App Store Connect workflow reconfiguration that stops the double build; and the review submission
itself unless the founder asked for `submit:true` in this run.
