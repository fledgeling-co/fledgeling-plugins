# OTA lane — Step 9 in full

Export the JS bundle, put the bytes in the public OTA Blob store, and register the result as a
**draft** bundle through the atlas-admin MCP. Runs on the OTA lane, and on the store lane too, so
every binary has a bundle lineage at its own fingerprint.

Background: `docs/atlas-app-OTA_UPDATES.md` and `docs/CONTRACTS.md` §5.

## 1 — Export with the production environment

```bash
cd apps/atlas-app
EXPO_PUBLIC_API_URL=https://atlas-api-orcin.vercel.app npx expo export --platform ios
```

`EXPO_PUBLIC_*` variables are **inlined into the JS at export time**, and Expo auto-loads
`apps/atlas-app/.env`. A dev `.env` carrying `EXPO_PUBLIC_API_URL=http://localhost:3000` therefore
bakes localhost into a bundle that will be served to phones, and nothing downstream notices: the
export succeeds, the upload succeeds, the registration succeeds, and the app fails to reach an API
only once a device downloads it.

Set the variable explicitly rather than trusting the unset-falls-back-to-prod default, and read the
observable before uploading:

```bash
grep -c "atlas-api-orcin.vercel.app" dist/_expo/static/js/ios/*.hbc   # expect ≥ 1
grep -c "localhost:3000"            dist/_expo/static/js/ios/*.hbc   # expect 0
```

## 2 — Read dist/metadata.json

`expo export` writes `dist/metadata.json` describing the platform's launch asset and its assets.
Map it to `register_bundle` like this:

| `register_bundle` field | Source |
|---|---|
| `launchAsset.key` | the iOS bundle entry's path in `metadata.json` |
| `launchAsset.hash` | the sha256 of the exported `.hbc` file, base64url, no padding |
| `launchAsset.url` | the Blob URL returned by that file's upload |
| `assets[].key` / `.hash` | the corresponding fields per asset in `metadata.json` |
| `assets[].contentType` | the asset's MIME type |
| `assets[].fileExtension` | the extension including the leading dot, as `metadata.json` records it |
| `assets[].url` | that asset's Blob URL |
| `runtimeVersion` | `npx expo-updates runtimeversion:resolve --platform ios` on the merged tree |
| `bundleNumber` | the new value in `apps/atlas-app/ota/bundle.json` |
| `commitSha` | `git rev-parse HEAD` |
| `gitTag` | `bundle-N` |
| `notes` | the founder's one-liner from Step 7 |
| `minAppVersion` | omit unless the merged JS depends on an API change tied to a specific app version |

The server builds the protocol manifest from these values and stores its serialization; atlas-api
reads that exact string and signs it at serve time. `buildManifestObject` is hand-mirrored in
`apps/atlas-admin/lib/ota.ts` and `apps/atlas-api/lib/ota.ts` and the two must stay byte-identical,
so do not construct a manifest yourself — pass the fields and let `register_bundle` build it.

Only **changed** assets need uploading. Paths are content-addressed, so re-uploading identical bytes
to the same path is a no-op (`allowOverwrite: true` with `addRandomSuffix: false`).

## 3 — Mint a token per file, immediately before that file's upload

```
request_bundle_upload { pathname: "ota/<runtimeVersion>/<bundleNumber>/<sha256>.hbc" }
request_bundle_upload { pathname: "ota/<runtimeVersion>/<bundleNumber>/assets/<hash>.<ext>" }
```

`request_bundle_upload` is a **non-mutating read** — it takes no `confirm` parameter. It returns
`{ token, pathname, validUntil }`, and the token is valid for **600 seconds**. On a bundle with many
changed assets, minting every token up front means the last uploads run against expired tokens. Mint,
upload, move on.

Two constraints the server enforces, so a malformed path fails at mint time rather than at
registration: the pathname must start with `ota/` and must not contain `..`. And
`register_bundle` re-checks every URL — it must be `https`, on a `*.blob.vercel-storage.com`
host, under the `ota/` prefix. This exists because the server signs a manifest pointing at these
URLs, and an arbitrary URL would let a signed manifest point anywhere.

## 4 — Upload the bytes directly

Bundle bytes never pass through MCP: the serverless body cap is 4.5 MB and a Hermes bundle exceeds
it. Upload with `@vercel/blob`'s `put`, which is already a dependency of atlas-admin and atlas-api,
using the minted token:

```js
// node, from the repo root
import { put } from '@vercel/blob';
const res = await put(pathname, fileBuffer, {
  access: 'public',
  token,                    // the client token from request_bundle_upload
  addRandomSuffix: false,
  allowOverwrite: true,
  contentType,
});
// res.url is what goes into register_bundle
```

Then read back the observable, per the evidence rule: `curl -sSI <res.url>` returns `200` and a
`content-length` equal to the local file's byte count. A `put` that resolves is not evidence the
object is readable at that URL — the manifest the server signs will point at it, and a signed
manifest pointing at a 404 is rejected on-device with no way to tell that apart from a signature
failure.

## 5 — Register the draft

```
register_bundle {
  confirm: true,
  bundleNumber, runtimeVersion, launchAsset, assets,
  commitSha, gitTag, notes            // minAppVersion only when it applies
}
```

It returns the new `updateId` (a UUID) and `status: draft`. Read it back with
`get_release { bundleNumber: N }` and check three things: it exists, `status` is `draft`, and
`launchAssetUrl` is the URL you uploaded rather than a stale one.

`bundleNumber` is unique-indexed. Re-registering an existing number returns a **409 conflict**, not
an overwrite. If a registration half-failed, the recovery is the next bundle number with a fresh
export — never a retry of the same one.

## Stop here

`register_bundle` leaves a draft, and a draft reaches nobody. That is the finished state of this
lane. The founder publishes from the admin web `/releases` page, the in-app admin Releases screen, or
`publish_bundle N` with confirm. Hand them the routes (`handoff.md`) rather than calling it.

## What a draft does not do

It does not bust the manifest cache for live clients, does not appear in `version-check`, and does
not affect any device. So a wrong draft costs an export and a bundle number — which is exactly why
this lane can run unattended and the publish cannot.
