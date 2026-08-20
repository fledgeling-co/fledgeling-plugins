# Classifying the release — OTA lane or App Store lane

What this step returns: one of the two words `OTA` or `App Store`, the before and after
fingerprint hashes, and, where they differ, the source that moved it. Report those four things.

The lane is decided by one value: the expo-updates **fingerprint**, which is also the
`runtimeVersion` a client sends on every manifest request. `app.json` sets
`runtimeVersion: { policy: "fingerprint" }`, and atlas-api serves a bundle only to a binary whose
fingerprint matches the bundle's exactly. Fingerprint unchanged means the binaries in the field can
run the new JS; fingerprint changed means they cannot, whatever the diff looks like.

## The two commands

Run both from `apps/atlas-app`:

```bash
npx expo-updates runtimeversion:resolve --platform ios
# → {"runtimeVersion":"<40-hex>","workflow":"managed", …}

npx expo-updates fingerprint:generate --platform ios
# → {"hash":"<40-hex>","sources":[…]}

npx expo-updates fingerprint:generate --platform ios --debug
# → the same, with each source and its own hash — this is what tells you WHICH input moved
```

Take the value at the merge base of the wave, then again on the merged tree, and compare the two
40-hex strings. Identical ⇒ OTA lane. Different ⇒ App Store lane, and the `--debug` sources tell the
founder which file did it.

## Use expo-updates, not @expo/fingerprint

The source skill this replaces called `npx @expo/fingerprint`. Two reasons that is the wrong
instrument here:

- `@expo/fingerprint` is not a declared dependency of `apps/atlas-app`, so `npx` resolves a floating
  version from the registry. It is present in the workspace store only as a transitive dep
  (`0.19.9` at the time of writing). A different fingerprint version can hash the same tree to a
  different value, and you would be comparing two numbers produced by two algorithms.
- `expo-updates` wraps it with its own options. In a managed workflow it passes
  `ignorePaths: ['android/**/*', 'ios/**/*']` so the fingerprint is stable whether or not the
  project has been prebuilt (`node_modules/expo-updates/utils/build/createFingerprintAsync.js`).
  Calling the underlying library directly skips that, and a run that happens to have a prebuilt
  `ios/` gets a different answer from one that does not.

The value that matters is the one the binary reports and the one `register_bundle` stores, and that
is the expo-updates value.

## ios.buildNumber is inside the fingerprint

Measured on this repo with `npx expo-updates fingerprint:generate --platform ios`:

| `app.json` → `expo.ios.buildNumber` | fingerprint |
|---|---|
| `2` | `4135716c5839e5fa58bd3854580e57a0ca3ef814` |
| `3` | `fd05b8d3980fae3c9b98345f048203726fd0653b` |

Source-level reason: expo-updates calls `createFingerprintAsync` with `{}`, and
`DEFAULT_SOURCE_SKIPS` does not include `ExpoConfigVersions` — the flag that would strip
`ios.buildNumber` from the hash.

**The failure this prevents.** A run reads the diff, sees only JS and copy changes, concludes "this
is OTA-able", and never runs the fingerprint. Somewhere in the same run it bumps the build number,
or a dependency resolve moves an autolinked native module version. The bundle registers without error at
a fingerprint no shipped binary carries, `list_releases` looks correct, and not one device is ever
offered the update. Nothing errors. The detection is to compute the fingerprint rather than reason
about the diff — the diff cannot tell you this and the fingerprint always can.

Two inputs that move the fingerprint without touching `app.json`: a from-scratch pnpm resolve, which
can change autolinked native module versions, and anything under `plugins/` or `ci_scripts/`.

## The channel has never shipped

As of the last check, `apps/atlas-app/ota/bundle.json` reads `{"bundleNumber": 0}` and
`list_releases` returns no bundles and no App Store versions. Two consequences for classification:

- **There is no recorded runtimeVersion to compare an installed binary against.** The rule is
  fingerprint-unchanged ⇒ OTA-able, but with no release record you cannot confirm what fingerprint
  any binary in the field actually carries. On the first few releases, "just ship an OTA" is
  unverifiable rather than merely risky — say so to the founder rather than presenting the OTA lane
  as proven.
- **The first OTA release is also the first live test of cert⇄key parity**, because nothing has ever
  had its manifest verified on a device. Run the parity gate at Step 0 and read it for the passed
  line, not the exit code (SKILL.md, "Gate reporting").

Re-check both facts at the start of a run with `list_releases` and `cat apps/atlas-app/ota/bundle.json`
rather than carrying this paragraph forward as current. A verdict about state with no expiry date is
the wrong artifact.

## When the resolve command fails

`runtimeversion:resolve` fails when the Expo config cannot be evaluated — a syntax error in
`app.json`, a plugin that throws, a missing node module after a partial install.

Report it as **not-run**, not as "no change detected". Fix the config or run `pnpm install`, then
re-run. Do not fall back to reading the diff and guessing the lane: an unresolvable fingerprint means
the OTA-vs-store question is unanswered, and answering it from the diff is the exact failure the
fingerprint exists to prevent.

## minAppVersion is a separate, softer question

`minAppVersion` is an optional semver floor stored per bundle, on top of the fingerprint match. It
is for "this bundle assumes the 1.3.1 backend", not for native compatibility, and it defaults to
unset. It does not participate in the lane decision. Set it at `register_bundle` time only when the
merged diff makes the JS depend on an API change that shipped in a specific app version; leave it
unset otherwise. Changing it after registration is `set_min_app_version`, which is a founder action.
