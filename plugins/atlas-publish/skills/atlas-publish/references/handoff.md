# Hand-off — Step 11

The run ends by handing the founder a decision, not a report. They have artifacts that reach nobody
yet, and three ways to change that. Keep the message to 20 lines.

## The template

```
Release <lane> — <N> PRs merged, draft registered.

Merged:  #12 <title>  ·  #14 <title>  ·  #15 <title>
Lane:    OTA (fingerprint unchanged: 4135716c…) | App Store (fingerprint moved: 4135716c… → fd05b8d3…, ios.buildNumber)
Gates:   back-compat passed · cert-parity passed (live assertion ran) · lint/typecheck/test passed
         <or: cert-parity NOT-RUN — OTA_CERT_PARITY_KEY unset>

Registered as DRAFT — nobody has this yet:
  bundle 4   runtimeVersion fd05b8d3…   updateId <uuid>   commit <sha>   tag bundle-4
  version 1.3.1  build 7  on TestFlight   tag v1.3.1

To publish, once you've checked it on a device:
  · admin web → https://admin.atlasapp.au/releases → Publish
  · in-app admin → Releases screen
  · ask Claude: publish_bundle 4

Store versions: mark v1.3.1 published only after Apple releases it — that's what
prompts older apps to update.

Open: <anything not done, by name — a not-run gate, a PR that did not merge, a skipped step>
```

Report each claim from what you read back rather than from what a step returned. A gate that could
not run appears as NOT-RUN with its reason; a step that was skipped appears under Open. An empty
Open line is omitted, not padded.

## The three publish routes

| Route | Where | Gate |
|---|---|---|
| Admin web | `/releases` on the admin console | Publish / Retract per bundle and per version, with confirm copy |
| In-app admin | the founder mobile **Releases** screen (`app/admin/more/releases.tsx`) | a native confirm alert |
| MCP | `publish_bundle N` / `publish_app_version X.Y.Z` | `confirm: true` on a second call, previewed and audited |

All three are founder actions. This skill calls none of them, and the MCP route being available in
the same session does not make it this skill's to call.

## What publishing actually does

A published bundle is served to any binary whose fingerprint matches the bundle's `runtimeVersion`
and whose app version clears `minAppVersion`, on that device's next update check — a cold boot
inside a 3-second budget, or a foregrounding throttled to 15 minutes.

Publishing an App Store version does not ship a binary. Apple does that. The publish only flips the
"a new version of Atlas is on the App Store" prompt for older apps, which is why it is marked
published after Apple releases, not before.

## Retract, and the incident playbook

Retract is a founder action too. Include this table in the hand-off only when the founder asks what
to do if the release goes wrong; otherwise point at `docs/atlas-app-OTA_UPDATES.md`.

| Symptom | Action |
|---|---|
| A just-published bundle crashes on launch | expo-updates error recovery relaunches the embedded store bundle and fires an `ota_rollback` event. Retract the bad bundle, then publish a fix. |
| A published bundle has a bug but does not crash | Retract it. Clients fall back to the previous published bundle for that runtimeVersion on their next check, or a `rollBackToEmbedded` directive if none remains. |
| `ota_update_failed` events spike | Check the Blob store and `OTA_CODE_SIGNING_KEY` — a signature mismatch makes clients reject the manifest. Retract if the manifest is bad. |
| Every update rejected right after a new store release | The committed cert and the server key are not a pair. Run the parity gate; a JS-only OTA cannot fix this, so restore the pair or ship a store build. |
| Manifest 500s | Redis fails open to Mongo for reads and still returns 200; check `OTA_CODE_SIGNING_KEY` is set. Mutations fail closed. |
| Nothing served for a runtimeVersion | Expected when no bundle is published for that fingerprint. Clients stay on their current bundle. |

The founder-visible health signal for a published bundle is the analytics stream:
`ota_update_downloaded` / `ota_update_applied` / `ota_update_failed` / `ota_rollback`, through
`POST /events`. Point them at it in the hand-off when they publish in the same session.

## The tag decision, if it is still open

Pushing `vX.Y.Z` starts both the Xcode Cloud Release workflow and this skill's Fastlane archive, so
one release produces two TestFlight builds. The fix is a one-time change the founder makes in App
Store Connect — set the Release workflow to manual start, keep Beta-on-`main` as the safety net.
Mention it once per run in which a `v*` tag was pushed, not every run.

## What is not in the hand-off

A summary of what the message just said, an assessment of how the release went, or an offer to
publish. The founder now owns one decision; the message ends when they have what they need to make
it.
