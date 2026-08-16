# The tools

Every argument name, default and enum below comes from the server's tool
catalogue. An argument absent from this page is absent from the schema — the
server rejects unknown keys rather than ignoring them, so a guessed argument
fails the call. All example values are **illustrative**: plausible shapes, not
captured runs.

## What gets advertised, and what it costs

The server ships **20 tools** and advertises a subset chosen by the shim's
`--profile` flag. The catalogue is re-sent on every turn and survives context
compaction, so it is a standing cost paid before any work happens:

| Profile | Adds | Total | Roughly |
|---|---|---|---|
| `ax` | `apps` `snapshot` `find` `menu` `act` `wait` `assert` `doctor` | 8 | — |
| `core` | + `capture` `zoom` | 10 | 6.8k tokens |
| `scripting` | + `flow` `stability` `dictionary` | 13 | — |
| `full` | + `inspect` `policy` `kill` `unlock` `ios` `computer` `openai_computer` | 20 | — |

The profiles nest: `ax ⊂ core ⊂ scripting ⊂ full`. `core` is the ten that
actually drive a Mac and is the right default. `ax` drops capture and zoom, so
take it only when the campaign will never look at a pixel. Widen to `scripting`
for flows and determinism runs, and to `full` for the iOS lane, `inspect`, the
policy gate, `kill`, and the CUA schema façades.

`proctor_ios` is in `full` only, which is worth knowing before planning an iOS
campaign against a host launched with `--profile core`.

This page documents the tools a campaign uses directly. Five more exist and are
named here rather than specified, because their schemas belong to the profiles
that advertise them: `proctor_policy` and `proctor_kill` (the policy gate and
process control), `proctor_dictionary` and `proctor_unlock`
(scripting-dictionary introspection and the unlock path), and
`proctor_computer` / `proctor_openai_computer` (the CUA schema façades, which
exist so a model trained on Anthropic's or OpenAI's computer-use schema can
drive Proctor without translation). Read the live catalogue for their arguments
rather than guessing.

## `proctor_doctor`

Whether a campaign can run at all, before anything is attributed to the app.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `verbose` | boolean | false | Per-app observer and cache detail. |
| `requestAccessibility` | boolean | false | Ask macOS to show its Accessibility consent dialog if the grant is missing. |
| `requestScreenRecording` | boolean | false | Ask macOS for the Screen Recording consent dialog. |

Either request flag shows its dialog **once per app identity**. If the user has
already answered it, macOS shows nothing and returns the recorded answer
silently, so pair either one with the System Settings route rather than assuming
a prompt was seen, and read the result from a fresh `doctor` call.

Returns `agentVersion`, `agentBuild`, `protocolVersion`, `osVersion`,
`agentRunning`, `socketPath`, `grants[]`, `attachedApps[]`, `observersLive`,
`secureEventInputActive`, `shortcutsCLIAvailable`, `obscuraAvailable`,
`obscura`, `obscuraUnavailable`, `tools[]`, `lanes[]`, `policy`, `secondLane`,
`ready`, `blockers[]`.

**`grants[]` is three-state.** Each row carries `name`, `granted`, `required`,
`howToFix` and `state`. `state` is `granted`, `denied` or `unconfirmed`, and the
`granted` boolean is derived from it fail-closed, so an unconfirmed grant reads
`false` exactly as a denied one does. Read `state` before putting a remedy in
front of anybody: `unconfirmed` means a bounded probe did not get an answer, and
the permission may be perfectly in place. `howToFix` is version-specific because
the fix genuinely differs by OS version.

**`tools[]` is the toolchain Proctor depends on and does not ship** — Obscura,
`browser-use` when the second lane names it, `simctl`, `cua-driver`, `maestro`.
Each row carries where the tool was found, everywhere it was looked for, its
version, and a `usability` of `usable`, `unusable` or `unconfirmed`. **This call
runs none of them**, so `unconfirmed` is a fact about what Proctor established
rather than a fault, and calling again will not change it. `obscuraAvailable`
and `obscura` are the grandfathered flat spelling of this array's first entry and
agree with it. A launchd agent does not inherit a login shell's `PATH`, so
Proctor's answer and your shell's can legitimately differ; the recorded search
paths are how you settle that.

**`lanes[]` derives what this machine can actually do** from the grants and the
tool rows, so a lane cannot claim readiness while the thing it needs is missing.
Four rows — `mac`, `browser`, `ios`, `cua` — each with `state` (`ready` /
`unavailable` / `unconfirmed`), a fail-closed `ready` boolean, `requires`,
`blockers` and a `note`. The `mac` row turns on the grants alone, because that
lane needs no external tool. The `ios` row turns on `simctl`; `maestro` is named
in its note rather than in `requires`, because deep links and screenshots work
without it and only flow files need it. The `cua` row says whether the machine
is ready for the delegated lane, which is a different claim from anything using
it — its note says which of the two you are looking at.

A tool row's `available` and a lane row's `ready` are deliberately different
words: the first means a file of that name is there, the second means the lane
is confirmed usable.

**`policy` is posture, not rules**: `mode` (`allowList` / `blockOnly` / `open`),
the list sizes, `approvalTokenLive`, `fsJailDeclared` and `fsRootCount`, and the
trail's `auditWritable`, `auditSealed`, `auditSigned`, `auditClean`,
`auditKeyConfirmed` and `auditEntries`. The lists themselves, the filesystem
roots, the trail's path and any key are deliberately absent, because `doctor` is
called before anything is established and a health check is the wrong place to
hand out configuration. That is a convention rather than a boundary —
`proctor_policy` action `status` answers in full to any caller.

**Over its neighbour:** always before `apps`. An attach with no Accessibility
grant returns an empty tree, indistinguishable from an app that never adopted
accessibility — one costs thirty seconds in System Settings, the other an hour
of selector debugging. `secureEventInputActive: true` is not a blocker but
narrows the plan: process-directed steps all still run, synthetic-event steps
become unreliable. And with wave 7's lanes, `doctor` is now also the call that
tells you an iOS campaign is impossible on this machine before you plan one.

```jsonc
{ "verbose": true }
// → { "osVersion":"26.5.1", "ready":false, "secureEventInputActive":true,
//     "agentBuild":{"descriptor":"0.4.0+3f21ac9"},
//     "grants":[{"name":"Screen Recording","granted":false,"state":"denied","required":true,
//       "howToFix":"System Settings > Privacy & Security > Screen & System Audio Recording."},
//       {"name":"Accessibility","granted":false,"state":"unconfirmed","required":true,
//       "howToFix":"System Settings > Privacy & Security > Accessibility."}],
//     "tools":[{"tool":"obscura","available":true,"usability":"usable","path":"/opt/homebrew/bin/obscura"},
//       {"tool":"simctl","available":true,"usability":"usable"},
//       {"tool":"cua-driver","available":false,"usability":"none"},
//       {"tool":"maestro","available":true,"usability":"usable"}],
//     "lanes":[{"lane":"mac","state":"unavailable","ready":false,
//       "blockers":["Screen Recording is not granted."]},
//       {"lane":"ios","state":"ready","ready":true,"requires":["simctl"],
//       "note":"Maestro is installed, so flow files can run beside the deep-link actions."},
//       {"lane":"cua","state":"unavailable","ready":false,"requires":["cua-driver"],
//       "note":"Not the actuation lane in force: Proctor's own planes are performing steps."}],
//     "policy":{"mode":"blockOnly","blockCount":4,"auditSigned":true,"auditClean":true},
//     "blockers":["Screen Recording not granted — capture and its settle signal unavailable."] }
```


## `proctor_apps`

What is under test, and handles that keep resolving for the rest of the run.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `action` | `list` \| `attach` \| `activate` \| `detach` | — | Required. |
| `bundleId` | string | — | e.g. `com.apple.TextEdit`. |
| `pid` | integer | — | When the bundle identifier is ambiguous or absent. |
| `name` | string | — | Localised app name, matched case-insensitively. |
| `app` | string | — | An existing app handle, for `detach` or `activate`. |
| `includeWindowless` | boolean | false | Include background apps with no windows. |
| `timeoutMs` | integer | 5000 | `activate` only: how long to wait for a window to appear. |

Returns app handles (`id`, `pid`, `bundleId`, `name`), window handles (`id`,
`app`, `title`, `frame`, `isMain`, `isMinimized`, `isOnActiveSpace`,
`cgWindowID`) and a `TreeProvenance` per attachment
(`manualAccessibilityApplied`, `enhancedUserInterfaceApplied`, `warmupWalks`,
`truncatedAtDepth`, `truncatedAtCount`, `unsupportedAttributes`, `elapsedMs`).
`cgWindowID` is optional and its absence reported rather than guessed — capture
needs it, so a window without one is readable and actionable but not
screenshottable. `warmupWalks` above 1 means the first walk came back empty and
the server re-walked; that is the normal Chromium and Electron path.

When a browser renders the window the attach also returns a `browser` handoff:
`boundary`, `browser`, `bundleId`, `surface`, `use`, `why`, `flags`,
`continuity`, `url`, `notes`, `caveats` and `toolUnavailable`. **`surface` is
`browserWindow` or `installedWebApp`**, and it is what disambiguates `use ==
null`: that means "no lane", and `surface` says whether the reason is that
nothing should drive the page or that Proctor drives this one itself.
**`flags`** is the machine-readable half of the prose and names what the
recommended instrument commits you to — `actsOutsideThisWindow`, `autonomous`,
`canActAsThisPerson`, `outsideTheAuditTrail`, `billed` — present exactly when
there is such an instrument. `outsideTheAuditTrail` is the one that changes what
a campaign can later claim was recorded.

**Authenticated browsers, 1Password, and Sift OTPs:**
- **Chrome accessibility:** Chrome exposes web DOM elements to Proctor only when accessibility is active. If an attach returns an `AXWebArea` with zero children or `manualAccessibilityApplied: false`, launch Chrome with `--force-renderer-accessibility` so that all input fields, buttons, and links populate the accessibility tree.
- **browser-use, the second lane:** for navigation Proctor's own planes cannot express against a real signed-in browser. **Off unless `PROCTOR_SECOND_LANE` names it** — `doctor` reports `secondLane` as `off` / `enabled` / `unavailable`, and `off` is the standing default. Check that field before recommending it. Obscura, the default lane, runs its own engine and its own cookie jar, so it sees no session and no password manager.
- **1Password autofill:** extension suggestions are native accessibility elements, and the role differs by browser — measured on 2026-08-16, the same entry was an `AXButton` in Chrome and an `AXMenuItem` in Safari. `kind: "press"` on the Chrome button autofilled and signed in with `ranInForeground: false`; the same press and a `pick` on Safari's menu item both returned `ok: true` and left the `stateHash` byte-identical, which is how you tell an accepted action from an effective one. When an overlay ignores the accessibility plane, fall back to `kind: "click"` with `point: [x, y]` and `foreground: true`, which needs Secure Event Input inactive.
- **Mail for OTPs and magic links:** Proctor ships no mail tool and reads no mail. When a mail MCP server is connected to the same host, take the code or link from it and feed it back with `setValue` or a navigation. Discover its tool names from that server's own catalogue — they are not Proctor's, `doctor` does not report them, and a server configured elsewhere but not connected here fails identically to one that does not exist. With no mail tool connected, the OTP step is the person's and the report should say so.

**Over its neighbour:** `list` touches nothing and answers "what is running".
`attach` starts retaining element references, and a retained reference is the
only thing that keeps resolving after its window moves to another Space.
Attaching twice discards the first set, so attach once and carry the handles.

**`activate` is the answer to `"windows": []`.** Every actuating tool resolves a
window handle first, so an app whose windows are all closed cannot be driven —
and the menu item that would reopen one cannot be reached without the window it
creates. `activate` launches or reopens the app the way a Dock click does, waits
for a window, attaches, and returns the handles. An attach that comes back with
an empty `windows` array is the signal; reach for `activate` rather than
concluding the app is unreachable. It goes through the same policy gate and
audit trail as driving the app.

```jsonc
{ "action": "attach", "bundleId": "com.example.Ledger" }
// → { "app":{"id":"app:4821:17301","pid":4821,"name":"Ledger"},
//     "windows":[{"id":"win:17301:0","title":"Ledger — 2026","frame":{"x":220,"y":140,"w":1180,"h":760},
//                 "isMain":true,"isOnActiveSpace":true,"cgWindowID":9931}],
//     "provenance":{"manualAccessibilityApplied":true,"warmupWalks":3,"elapsedMs":412} }
```

## `proctor_snapshot`

What is in this window right now, as structure rather than as a picture.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `window` | string | — | Required. Handle from `proctor_apps`. |
| `sinceRevision` | integer | — | Return a diff from this revision instead of the whole tree. |
| `maxDepth` | integer | 24 | Truncation reported in provenance. |
| `maxNodes` | integer | 600 | Truncation reported in provenance. |
| `includeInvisible` | boolean | false for reading, true when auditing | Keeps zero-area and offscreen nodes. |
| `root` | string | — | Walk from this node id instead of the window root. |

Returns `window`, a monotonic `revision`, either `root` or a `diff` (`added`,
`removed`, `changed`, `unchangedCount`), the `provenance`, and a canonical
`stateHash`. Each node carries `id`, `role`, `subrole`, `roleDescription`,
`title`, `label`, `value`, `help`, `identifier`, `frame`, `enabled`, `focused`,
`selected`, `actions`, `writableAttributes`, `children`, `childCount`. An empty
`actions` array with no writable attributes means the node cannot be operated
through the accessibility plane at all, whatever it looks like on screen.
`stateHash` masks volatile fields, so two snapshots with the same hash are the
same state — the identity `proctor_stability` counts.

**Over its neighbour:** `snapshot` for the exploratory pass, before you know the
window's shape; `find` once you do. A full snapshot of a rich window approaches
the 2000-node budget where a `find` for one button costs a handful. Mid-flow,
pass `sinceRevision`: the diff costs tokens proportional to what changed, and it
is the more legible report artifact, because a reader sees what the step did
without holding two trees in mind. `includeInvisible: true` is how the audit
pass finds invisible-but-focusable nodes; auditing with it off means never
seeing the class of defect it exists to expose.

```jsonc
{ "window": "win:17301:0", "sinceRevision": 41, "maxDepth": 18 }
// → { "revision":42, "stateHash":"b3f0…9c1", "diff":{ "fromRevision":41, "unchangedCount":318,
//     "added":[{"id":"n:884","role":"AXSheet","title":"Delete 3 entries?","childCount":4}],
//     "changed":[{"id":"n:210","fields":{"enabled":{"before":true,"after":false}}}], "removed":[] } }
```

## `proctor_find`

Locating one node without paying for the tree around it.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `window` | string | — | Required. |
| `role` | string | — | AX role, e.g. `AXButton`, `AXTextField`. |
| `subrole` | string | — | |
| `title` | string | — | Matched per `match`. |
| `label` | string | — | |
| `identifier` | string | — | AXIdentifier. The most durable selector available. |
| `valueContains` | string | — | |
| `enabled` | boolean | — | |
| `focused` | boolean | — | |
| `hasAction` | string | — | Only nodes offering this AX action, e.g. `AXPress`. |
| `match` | `substring` \| `exact` \| `regex` | `substring` | |
| `limit` | integer | 25 | |

All supplied conditions must hold; there is no `or`. Returns matching nodes in
the same shape a snapshot uses.

**Over its neighbour:** prefer `identifier` to `title` whenever the app sets
one. An AXIdentifier is the only selector a developer chose deliberately, so it
survives copy changes, localisation and design passes; a title-matched flow that
breaks after a wording change reports as a defect in the app when it is a defect
in the test. `hasAction: "AXPress"` finds the thing that can be pressed rather
than the thing that looks like a button — a decorative group and a real control
often share a role.

```jsonc
{ "window": "win:17301:0", "identifier": "ledger.entry.delete", "enabled": true }
// → { "matches":[{"id":"n:512","role":"AXButton","identifier":"ledger.entry.delete","label":"Delete entry",
//     "frame":{"x":1040,"y":212,"w":28,"h":22},"actions":["AXPress","AXShowMenu"],
//     "writableAttributes":["AXFocused"]}] }
```

That frame is 28 × 22 points — under the hit-target floor, surfaced incidentally
by a lookup that was not asking about it.

## `proctor_act`

Driving the app in as few round trips as the logic allows, with each step's
honesty recorded.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `window` | string | — | Required. |
| `steps` | array | — | Required. Each step has a `kind` plus the fields that kind needs. |
| `settle` | object | see below | Default settle policy for every step. |
| `foreground` | boolean | false | Activate the app first. Required for synthetic-event kinds. |
| `captureEach` | boolean | false | Capture a frame after every step. |
| `diffEach` | boolean | true | Return a tree diff after every step. |
| `pointerMarks` | boolean | false | With `captureEach`, composite a marker at each step's target onto that step's frame, as a marked sibling PNG. |
| `record` | string | — | Append these steps to the named flow as they run. |

Step fields: `kind` (required), `node`, `value`, `menuPath`, `text`, `key`,
`modifiers`, `delta`, `point`, `path`, `durationMs`, `label`, `settle`. Step
kinds: `press`, `setValue`, `focus`, `menu`, `type`, `key`, `scroll`,
`increment`, `decrement`, `pick`, `confirm`, `cancel`, `raise`, `close`,
`resize`, `move`, `dragPath`, `hover`, `click`, `shortcut`, `appleScript`,
`waitFor`.

`path` and `durationMs` belong to `dragPath`. `path` is the route as
`[[x,y], ...]` in window coordinates; a press and a release at two positions is
a click, so the gesture is interpolated to intermediate movements no more than
10 points apart and capped at 240 events. Omit it and the drag runs from `point`
(or the node's centre) to `point + delta`. `durationMs` defaults to 300 and is
clamped to 30s; events are spaced evenly across it with a 2 ms floor each, so a
long path can take longer than asked — raise it for an application that drops
fast drags.

**Which kinds need the foreground is a question for the backend, not a property
of the step.** On the native backend `dragPath`, `hover`, `click` and `key` are
the synthetic-event kinds and report `plane: "syntheticEvent"`; `shortcut` runs
the app's declared contract and reports `declared`; `appleScript` reports
`appleEvents`; everything else travels `accessibility`. A delegated backend can
answer differently, which is why the refusal, the foreground disclosure and the
queue's lane demand all ask the backend rather than consulting a list of kinds.

The `settle` object takes `quietFrames`, `dirtyThreshold`, `axQuietMs`,
`timeoutMs`, `requireReflectorIdle` — defaults 2, 0.002, 250 ms, 5000 ms,
false. Raise `timeoutMs` for a step that genuinely takes time rather than
accepting a `timeout` settle and reasoning over an unproven result.

Returns `window`, `steps[]`, `completed`, `failedAt`, `finalHash`, and a
foreground block; each step result carries `index`, the submitted `step`, `ok`,
`plane`, `route`, `error`, a `SettleReport`, `stateHash`, `diff`, `elapsedMs`,
and `backend`. On failure the batch stops, so you get the state at the point of
failure rather than a cascade.

**Read the foreground block's `measured` count rather than re-deriving it from
the kinds.** It reports how many steps were known before the run to need the app
in front, how many might have, and how many actually travelled as synthetic
events. A `type` or `scroll` into an element the accessibility plane cannot
write falls back to the event stream, and no count made from the step list would
show it. A run whose `measured` count is above zero cannot be repeated
unattended.

**Delegated steps carry five more fields, absent on a native run**:
`reportedMode` (the backend's own word for the delivery mode, verbatim),
`effect` (`confirmed` / `unverifiable` / `suspectedNoOp` — nil natively, because
the native backend judges a write by reading it back rather than reporting a
confidence), `unrequestedForeground` (the backend took the front for a step that
asked to stay in the background), `retriedOnStale` (the handle went stale and
was re-resolved before the step ran, which is a determinism signal about a
moving target), and `transportMs` (round trip to the backend, separate from
`elapsedMs`, which already includes settle).

`hashSubject` appears on a step that ran in a window a browser renders, and says
which side of the page boundary the target fell on — `pageContent`,
`browserChrome` or `unclassified` — and therefore which tree the state hash was
taken over. It is measured at the step while it ran rather than scanned before
the batch, because a step's target usually does not exist until the steps before
it have run. Its absence on a step that ran means one thing: no browser renders
this window.

**`diffEach` is the argument that will blow your tool result.** It defaults to
true, and on a rich Electron or Chromium tree a per-step diff of several hundred
nodes across a six-step batch overruns the result limit and gets spilled to a
file you then have to read back. Pass `diffEach: false` whenever you are driving
a browser-shaped app and do not need the per-step delta; `stateHash` still tells
you whether anything changed, and `proctor_snapshot` with `sinceRevision` gives
you the diff on demand when it matters.

`pointerMarks` annotates the point each step *acted on*, which is not the same
claim as a cursor: Proctor does not move the system pointer, and the marker is
composited into the evidence rather than photographed from the screen.

**Over its neighbour:** batch aggressively. Six steps in one call settle six
times regardless, so splitting them buys six round trips and six chances to
reason about an intermediate state that does not matter. Split where the logic
branches. Leave `foreground` false unless a step needs the front: a flow that
passes in the background has proven the stronger thing, that it works while
someone else is using the machine.

```jsonc
{ "window":"win:17301:0", "record":"delete-entry-confirmed", "steps":[
    {"kind":"press","node":"n:512","label":"open delete confirmation"},
    {"kind":"waitFor","node":"n:884","label":"sheet appears"},
    {"kind":"setValue","node":"n:901","value":"DELETE","label":"type confirmation word"},
    {"kind":"confirm","node":"n:903","label":"confirm","settle":{"timeoutMs":12000}} ] }
// → { "completed":4, "failedAt":null, "finalHash":"7a12…40e", "steps":[
//     {"index":0,"ok":true,"plane":"accessibility","elapsedMs":340,"settle":{"reason":"allSignalsQuiet",
//       "quietFrames":2,"lastDirtyArea":0.0004,"axNotificationsSeen":6,"reflectorIdle":null,
//       "signals":["captureQuiet","axQuiet"]}},
//     {"index":3,"ok":true,"plane":"accessibility","elapsedMs":8120,"settle":{"reason":"captureQuietOnly",
//       "axNotificationsSeen":0,"signals":["captureQuiet"]}} ] }
```

Step 3 settled on pixels alone with zero notifications over eight seconds. That
is adequate, and worth a line if the result surprises you: a window emitting
nothing during a destructive operation is a window whose tree may be lagging its
pixels.

## `proctor_capture`

What the window looked like, with enough metadata to tell a fresh frame from a
stale one.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `window` | string | — | Required. |
| `path` | string | session temp dir | Where to write the image. |
| `waitForComplete` | boolean | true | Pull frames until one is `.complete` or the timeout expires. |
| `timeoutMs` | integer | 3000 | |
| `scale` | number | display backing scale | |
| `format` | enum | `png` | `png` or `jpeg`. |
| `quality` | integer | 90 | 60–100. Ignored for PNG. |
| `normalize` | boolean | true | Fit the frame to the vision ceiling and report the exact scale. |
| `normalizeMaxLongEdge` | integer | 1568 | Long-edge ceiling in pixels. |
| `normalizeMaxPixels` | integer | 1150000 | Total-pixel ceiling. |
| `annotate` | boolean | false | Burn numbered marks over interactable elements and return the mark→node map. |
| `annotateAll` | boolean | false | Mark every element carrying a frame. Implies `annotate`. |
| `maxMarks` | integer | 150 | Overflow is dropped in reading order and reported as `truncated`. |
| `grid` | boolean | false | Overlay reference grid lines. Independent of `annotate`. |
| `gridSpacing` | number | 100 | Points between grid lines. |
| `tileHashes` | boolean | false | Per-tile perceptual hashes, for determinism comparison. |
| `includeCursor` | boolean | false | A cursor in the frame is a source of false diffs. |

Returns `path`, `width`, `height`, `scale`, `status` (`complete` \| `idle` \|
`blank` \| `suspended` \| `stopped` \| `unknown`), `contentRect`,
`dirtyRectCount`, `dirtyArea` (0–1), `capturedAt`, `framesWaited`,
`trustworthy`, `caveat`, `normalization`, `annotation` when marks were drawn,
and `tileHashes` when requested. The filter is window-scoped, so the image holds
that window and not what is on top of it, which is what makes an occluded window
capturable. Bytes are never inline.

**Normalisation is on by default and you must map coordinates back through it.**
An oversized frame gets downsampled by the vision API anyway; the only question
was whether that happens where the factor is measured and reported or where it
is invisible. `normalization.scale` carries the exact factor, so a coordinate
returned by a model maps to the real screen with `native = normalised / scale`.
Pass `normalize: false` when you want native pixels for a pixel-plane assertion,
or set the two ceilings to a provider's tile grid (768 for Gemini, where
crossing a tile boundary by a few pixels can double the token cost).

**PNG is the default because it is what keeps small UI text readable.** On a
3456x2234 retina capture normalised to the vision ceiling, macOS Vision OCR
recovered 94% of the native-resolution words from PNG, 91% at JPEG q85 and 78%
at q50 — and the count of words misread as a *different real word*, which a
model will act on rather than flag, rose from 11 to 20 to 66. Treat JPEG as a
way to archive many frames, not a way to read a UI.

**Over its neighbour:** `capture` answers "what does it look like"; `inspect`
answers "what are the values"; `zoom` answers "what does that small thing say".
For an app embedding `ProctorReflector` a colour question goes to `inspect`,
because a colour sampled from a PNG has been through the compositor, the display
profile and any scaling, and is not the number the developer wrote. For an app
you do not own there is no such source — a limit to state, not a number to
approximate. Use `tileHashes` when you intend to compare two captures rather
than look at one.

```jsonc
{ "window":"win:17301:0", "path":"/tmp/proctor/dark-empty.png", "tileHashes":true }
// → { "width":2360,"height":1520,"scale":2.0,"status":"complete","framesWaited":2,
//     "contentRect":{"x":0,"y":0,"w":1180,"h":760},"dirtyRectCount":3,"dirtyArea":0.017,
//     "trustworthy":true,"caveat":null,"tileHashes":["9f31…","0ab7…"] }
```

## `proctor_zoom`

A native-resolution crop of one region or one element, for reading small text or
fine detail a whole-window capture loses.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `window` | string | — | Required. |
| `region` | `[x,y,w,h]` | — | Points from the window's top-left. Supply this or `node`. |
| `node` | string | — | A node id from `find`; its frame is resolved and cropped. |
| `padding` | number | 0 | Context points added on every side. |
| `scale` | number | display backing scale | Defaults to native, which is the point. |
| `format` | enum | `png` | PNG is what makes small text readable. |
| `quality` | integer | 90 | Ignored for PNG. |
| `waitForComplete` | boolean | true | |
| `timeoutMs` | integer | 3000 | |
| `path` | string | session temp dir | |

**Why this exists.** `capture` normalises to the vision ceiling by default, and
the pixels a label, glyph or numeric field is written in do not survive that
downscale. `zoom` restores them without shipping a full 2x screenshot.
Published benchmarks put the gain large: iterative crop-and-zoom lifts GUI
grounding accuracy on high-resolution desktop software from roughly 19% to
48–73%. Aim for a region around 1000px on its long edge; much smaller and the
surrounding context that disambiguates the target is gone too. The compose path
is **find → zoom → assert**.

The crop is cut from a native-scale window capture, so it carries that capture's
freshness metadata unchanged: check `trustworthy` and `caveat` exactly as with
`capture`. The descriptor names the pixel rect actually cut, whether it was
clamped to the window, and the path to the un-cropped image. Reading the text is
left to you; this restores the pixels, it does not OCR them.

```jsonc
{ "window":"win:17301:0", "node":"n:882", "padding":24 }
// → { "path":"/tmp/proctor/zoom-882.png","pixelRect":{"x":248,"y":712,"w":416,"h":96},
//     "clamped":false,"trustworthy":true,"fullPath":"/tmp/proctor/zoom-882.full.png" }
```

## `proctor_menu`

The application's whole menu bar, with each item's path, enabled state, and the
keyboard shortcut reconstructed from its accessibility attributes.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `app` | string | — | An app handle. Supply this or `window`. |
| `window` | string | — | A window handle; its owning application's menu bar is read. |

**Why the shortcut matters.** Walking `AXMenuBar` to a submenu item is slow,
focus-sensitive and brittle across localisations. Each item carries its shortcut
two ways: the normalised string (`cmd+shift+n`) and a `key` plus `modifiers`
pair in exactly the shape `proctor_act`'s `key` step reads, so an item can be
invoked straight from this enumeration.

Note the plane difference. A `key` step is a synthetic event and needs the app
frontmost; a `menu` step with the `menuPath` this tool returns actuates the same
command through the accessibility plane without stealing focus. Both routes come
from the one walk, and the background-safe one is usually the one you want.

This is a pure accessibility read: no synthetic events, no permission beyond the
Accessibility grant, and it reaches a background or other-Space app. macOS
builds some submenus only when they are opened; such a submenu is reported as a
single item with `submenuPopulated: false` rather than fabricating contents that
were never read. Open it with a `menu` or `press` step and re-read to see inside.

## `proctor_wait`


Blocking on something nameable, when "the UI stopped moving" is not the thing
you are waiting for.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `window` | string | — | Required. |
| `condition` | enum | — | Required. `nodeExists`, `nodeGone`, `valueEquals`, `valueContains`, `enabled`, `focused`, `regionQuiet`, `reflectorIdle`. |
| `node` | string | — | |
| `find` | object | — | A find predicate, when the node does not exist yet and so has no id. |
| `value` | any | — | Target for `valueEquals` / `valueContains`. |
| `region` | `[x,y,w,h]` | — | Window coordinates, for `regionQuiet`. |
| `timeoutMs` | integer | 10000 | |
| `pollMs` | integer | 100 | |

Returns whether the condition held, how long it took, and the state when it
resolved.

**Over its neighbour:** settle already runs after every action, so waiting for
the UI to go quiet is redundant and slows the flow. Reach for `wait` when the
thing has a name — a row that arrives from the network after the UI already went
still, a progress value reaching 100, a spinner disappearing. Those are exactly
the cases where a settle reports success and the app is not finished, because a
quiet frame during a network fetch is genuinely quiet.

```jsonc
{ "window":"win:17301:0", "condition":"nodeExists", "timeoutMs":20000,
  "find":{"role":"AXRow","valueContains":"Q3 reconciliation"} }
// → { "held":true, "elapsedMs":6410, "node":"n:1204",
//     "state":{"role":"AXRow","enabled":true,"frame":{"x":24,"y":388,"w":1132,"h":34}} }
```

## `proctor_assert`

Turning an observation into a verdict a report can carry.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `window` | string | — | Required. |
| `assertions` | array | — | Required. |
| `captureEvidence` | boolean | true | Attach a capture to each failure. |

Assertion fields: `kind` (required), `node`, `find`, `expected`, `tolerance`,
`reference` (path to a reference PNG, for `regionMatches`), `label`. Kinds:
`exists`, `absent`, `valueEquals`, `valueContains`, `enabled`, `disabled`,
`focused`, `hasLabel`, `frameEquals`, `containedIn`, `alignedWith`,
`horizontalAlignment`, `minHitSize`, `contrast`, `focusOrder`, `regionMatches`,
`agree`.

Returns pass or fail per assertion with the observed value beside the expected
one. `agree` returns `Disagreement` records: `kind` (`unexposedControl`,
`ghostNode`, `invisibleButFocusable`, `frameMismatch`, `staleFrame`,
`hitTargetMismatch`, `contrastBelowThreshold`, `missingLabel`), `node`,
`detail`, `axSays`, `layerSays`, `pixelsSay`, `severity`.

**Over its neighbour:** `wait` gives a timeout, `assert` gives a verdict. A test
ending in a wait reports "it eventually happened", which cannot be ranked by
severity or reproduced from a report. Wait for the precondition, assert the
outcome. `agree` is the only assertion looking for a disagreement rather than at
a value, which is why it finds a control the tree does not know about or a node
with no pixels behind it — neither a tree dump nor a screenshot review finds
those alone, because each is one observer agreeing with itself.

```jsonc
{ "window":"win:17301:0", "assertions":[
    {"kind":"absent","find":{"identifier":"ledger.entry.row","valueContains":"Q3"},"label":"deleted row gone"},
    {"kind":"hasLabel","find":{"role":"AXButton"},"label":"every button is named"},
    {"kind":"minHitSize","expected":24,"find":{"role":"AXButton"},"label":"24pt floor"},
    {"kind":"agree","label":"tri-observer"} ] }
// → { "results":[ {"label":"deleted row gone","passed":true},
//     {"label":"every button is named","passed":false,"nodes":["n:512","n:641","n:702"],
//      "observed":"3 of 19 AXButton nodes have neither title nor label","evidence":"/tmp/proctor/fail-2.png"},
//     {"label":"24pt floor","passed":false,"expected":24,"observed":{"n:512":[28,22]}},
//     {"label":"tri-observer","passed":false,"disagreements":[{"kind":"unexposedControl","severity":"defect",
//      "detail":"A 96×28 control-shaped region at (880,120) has no AX node.",
//      "axSays":null,"pixelsSay":{"rect":[880,120,96,28]}}]} ], "skipped":[] }
```

## `proctor_flow`

Making a step sequence a named, reusable thing — the unit a campaign is built
from and a report refers to.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `action` | `start` \| `stop` \| `replay` \| `list` \| `show` \| `delete` | — | Required. |
| `name` | string | — | |
| `window` | string | — | Target for replay; the recorded window otherwise. |
| `description` | string | — | What this flow covers, carried into the report. |
| `captureEach` | boolean | — | |
| `settle` | object | — | |

Recording is two tools together: `action: "start"` opens the recording,
`proctor_act` with `record: "<name>"` appends steps as they run, `action:
"stop"` closes it. A flow stores the step list, the selector each step resolved
through, and the per-step state hashes from the recording run — so `replay`
reports where and how a run diverged, not only that it failed. Flows persist
under the session directory and survive the MCP host restarting.

**Over its neighbour:** a bare `act` proves the app did something once. A flow
makes it repeatable by name, which is what a defect's reproduction line needs
and what `proctor_stability` takes as input. A flow holds steps, not assertions
— pair each with the `proctor_assert` call that gives it a verdict, under the
same name, so a reader finds both.

```jsonc
{ "action":"replay", "name":"delete-entry-confirmed", "window":"win:17301:0" }
// → { "steps":4, "matched":3, "divergedAt":2, "detail":[{"index":2,
//     "recordedHash":"e19b…7c2","replayHash":"44af…013",
//     "note":"confirmation field pre-filled on replay; recording started from an empty field"}] }
```

A divergence tracing to a different start state is a reset problem, not an app
defect — which is what `resetBetween` exists for.

## `proctor_stability`

Whether a flow is deterministic enough to trust as a gate, as a number.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `flow` | string | — | Required. |
| `runs` | integer | 5 | |
| `window` | string | — | |
| `resetBetween` | object | — | Steps to run between replays to return the app to its start state. |
| `includeTiles` | boolean | false | Compare pixel tile hashes as well as the tree. Slower; catches rendering nondeterminism the tree cannot see. |

Returns `flow`, `runs`, `stepCount`, `firstDivergence`, `stepInstability` (0–1
per step), `deterministic`, `divergenceDetail` (step index to distinct hashes
seen), `notes[]`, `backend`, and — when there is anything to disclose —
`stepBasis`, `pageContent` and `captures`. `stepInstability` is the fraction of
runs that did not reach the modal state at that step. Three runs detects gross
nondeterminism; five to ten is the useful range for a flow about to become a
gate.

**The score is unreadable without the three disclosure fields beside it.**
`backend` names the actuation lane every pass was measured on — one value for
the report, because a session's lane is fixed — and a comparison whose halves
ran through different lanes is measuring the lanes rather than the application.
`pageContent` is present when at least one step in at least one repeat was
measured over a browser's render tree, and names the browser, the steps
affected, and what that does to their numbers; a page's own render churn is not
the application's nondeterminism. `stepBasis` holds one entry per step saying
what that number was taken over and what it was computed from, including where a
repeat withheld a hash, and reads in parallel with `stepInstability`. Quote the
pair rather than the number alone.

**Over its neighbour:** re-running a flow by hand and watching it pass twice
tells you almost nothing — a 20% flake passes twice in a row 64% of the time.
It also yields no step index, so a failure at step 9 sends someone to step 9
when the run stopped being reproducible at step 3. Run stability before
reporting failures; it is cheaper than the investigation it prevents. Use
`includeTiles` when the suspicion is rendering rather than logic: a chart that
lays out differently on alternate runs produces identical trees and different
pixels.

```jsonc
{ "flow":"delete-entry-confirmed", "runs":7, "includeTiles":true,
  "resetBetween":{"steps":[{"kind":"menu","menuPath":["File","Revert to Saved"]}]} }
// → { "stepCount":4, "firstDivergence":2, "deterministic":false,
//     "stepInstability":[0.0,0.0,0.43,0.43], "divergenceDetail":{"2":["e19b…7c2","44af…013","9d80…5fa"]},
//     "notes":["Run 5 ended early: settle reason `timeout` at step 2 (12000 ms).",
//              "Tile comparison enabled; 2 of 7 runs differed in tiles only at step 3."] }
```

## `proctor_inspect`

Reading a resolved value rather than inferring one, for an app that embeds
`ProctorReflector`.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `window` | string | — | Required. |
| `node` | string | — | Accessibility node id to correlate; omit for the whole hierarchy. |
| `maxDepth` | integer | — | |
| `includeConstraints` | boolean | false | Layout constraint dumps are large. |
| `presentation` | boolean | true | Include CALayer presentation values alongside model values. |

Returns the view and layer hierarchy with resolved colours, fonts, corner radii,
opacity, constraints, both CALayer model and presentation values, and a
monotonic render revision. Without a reflector it returns `reflectorUnavailable`
rather than approximating.

**Over its neighbour:** this is the only route to anything resembling computed
styles on macOS — there is no cross-process `getComputedStyle`. Where it is
available a fidelity finding is a measurement; where it is not, the ceiling is
the accessibility tree plus pixels, and the honest move is to say so rather than
report an eyedropped colour as a declared value. The model-versus-presentation
split matters during animation: the two differ exactly while something is in
flight, making their agreement a settle signal in its own right.

```jsonc
{ "window":"win:17301:0", "node":"n:512", "presentation":true }
// → { "renderRevision":8841, "view":{"class":"LedgerDestructiveButton","frame":{"x":1040,"y":212,"w":28,"h":22}},
//     "layer":{"model":{"backgroundColor":"#C6362Cff","cornerRadius":6.0,"opacity":1.0},
//              "presentation":{"backgroundColor":"#C6362Cff","cornerRadius":6.0,"opacity":0.62}},
//     "text":{"font":"SF Pro Text Semibold 11.0","color":"#FFFFFFff"} }
```

Model opacity 1.0 against presentation 0.62 means a fade is in flight. The model
value alone would report a state the user cannot yet see.

## `proctor_ios`

Putting an iOS app into a named state on a booted Simulator, and reading back
what actually happened. `--profile full` only, and it needs Xcode, which is
where `simctl` lives.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `action` | `list` \| `boot` \| `open` \| `screenshot` \| `flow` | `list` | |
| `device` | string | the single booted device | A `dev-` handle from `list`, a udid, or a name like `iPhone 16 Pro`. Ambiguity is an error naming the candidates rather than a guess. |
| `url` | string | — | The deep link to open. |
| `bundleId` | string | — | The app you expect to receive it. A consistency check, not the gate key. |
| `pixelEvidence` | boolean | true | Capture the device screen before and after the open and compare. |
| `changeThreshold` | number | 0.0005 | Fraction of changed pixels before the screen counts as changed. |
| `path` | string | session temp dir | Where to write a screenshot; for `flow`, the absolute path of the Maestro flow file. |
| `runs` | integer | 1 | For `flow`. Above 1, repeats are scored against each other. |
| `timeoutMs` | integer | 15000 (120000 for `boot`) | Bound on the simctl call. |

**A device handle is not a window handle, and the difference is not cosmetic.**
`proctor_snapshot`, `proctor_find`, `proctor_assert`, `proctor_act` and
`proctor_capture` refuse a `dev-` handle by name. The Mac's accessibility API
does not cross into a simulated device, so there is no tree, no elements, no
geometry and no actuation steps. What exists instead is three channels —
whether the app's process is running, what the device screen looks like, and
what `simctl` said — reported separately rather than blended.

**`open` returns a verdict, and a zero exit is not one.** The same open run twice
exits zero both times and only the first changes anything. `targetChanged` means
delivered, the resolved app is running, and the screen changed; `screenChanged`
means the screen moved but the change cannot be attributed to the app the URL
named; `deliveredOnly` means nothing observable changed, which is inconclusive
rather than failed, because a deep link to the screen the app is already on looks
exactly like one the app ignored; `refused` means the gate or the device declined
it. None of them claims the app reached a particular screen — the frontmost app
on the device is not observable through this lane.

`changeThreshold`'s default is calibrated against an idle floor measured at
exactly 0 and a smallest real navigation at 0.002.

`open` never boots anything and refuses a device that is not booted, because
folding a stateful minute-long side effect into a call whose result is "did this
navigate" would make both meaningless. `boot` is explicit, gated and audited.
Nothing here shuts a device down or reboots one; a device this session booted is
marked in `list`.

**A device screenshot carries no ScreenCaptureKit frame status**, so its
freshness cannot be established and it comes back marked untrustworthy with that
as the reason. The pixels are real; the guarantee a window capture carries is
not.

**`flow` runs a Maestro file, and the unit is the file.** Maestro is a separate
binary that executes the whole file and reports at the end, so `flowPassed`
means the driver executed the sequence and reported success — not that Proctor
observed the app reach any state. Proctor did not run these commands and has no
independent observation of any of them; the only observer of the steps is
Maestro. Individual Maestro commands are never routed through `proctor_act`,
because a tool driving its own engine is not driving what Proctor is attached to.

With `runs` above 1 the repeats are scored **against each other**, never against
a recording, because there is none. `firstDivergence` is where two repeats
stopped agreeing, indexed by Maestro's own sequence numbering. Maestro prepends
two commands present in no flow file, marked `injected`, so an index does not map
onto a line of your YAML without checking. Durations sit beside the score and are
never folded into it: one unchanged command measured 634, 91, 88, 96 and 91 ms
across five repeats. A repeat that failed in the driver rather than the app — no
per-command record, a failed launch, a device that went away — is excluded and
makes the sweep `truncated`, so driver flake is never published as the app's
nondeterminism. Budget 70 to 90 seconds for a five-run sweep, most of it driver
start-up.

**Gating keys on the device, not on what you passed.** `open` is gated on the app
the URL actually resolves to on the device; `bundleId` is a consistency check and
a disagreement is reported. iOS targets are named `ios:<bundleId>`, so a Mac app
on an allow list does not silently authorise the iOS app of the same identifier,
and a block on either spelling blocks both. A flow's gate judges the apps the
flow **declares**, which is weaker, and the result says `declared` for that
reason; a construct Proctor cannot resolve — a script, an interpolated app id, an
unreadable include — is refused whenever an application policy is in force. An
`openLink` inside a flow is gated on what the device resolves it to.

The trail records a URL's scheme and host in the clear and reduces its path and
query to a length and a hash, because a deep link routinely carries a token. For
a flow it records the file's path and a hash of its contents.

**Over its neighbour:** there is no neighbour. Nothing else in this catalogue
reaches a simulated device, and nothing in this catalogue gives an iOS target the
tree, elements or geometry the Mac tools give a window. Plan the iOS half of a
campaign around the verdicts above rather than around what the Mac lane can do.

---

## Reading results honestly

Seven results whose obvious reading is wrong in a specific way.

**A capture with `trustworthy: false`.** The wrong read is to open the PNG, see
a window that looks right, and use it as evidence — a stale frame is
pixel-identical to a correct one, which is the entire reason the field exists.
The `caveat` names the cause, and the common one is real ScreenCaptureKit
behaviour rather than a fault in the run: an off-screen window may emit complete
frames only when the pointer moves on its display, so a background capture on an
idle machine can receive nothing. The right read is that this capture is not
evidence of anything. Capture again with the window raised, use that, and say so
in the methods note — a raised window is a different configuration from the one
the rest of the campaign ran in.

**A settle with `reason: "timeout"`.** The wrong read is that the step completed
and the following assertion is meaningful. Nothing went quiet; the server
stopped waiting. A failure observed after a timeout settle is unproven, not a
defect, and reporting it as one sends someone hunting a bug in code that was
still working when you photographed it. The right read is to re-run with a
longer `timeoutMs`, or replace the settle with a `proctor_wait` on the thing you
were actually waiting for, and report the original as inconclusive if neither
resolves it. A step that times out consistently is itself a finding: the app
never goes quiet after that action.

**A step with `plane: "syntheticEvent"` where you expected process-directed.**
The wrong read is that it is equivalent to the rest of the flow. It travelled
the single system event stream, so it needed the app in front, it interfered
with anyone using the machine, and Secure Event Input can stop it arriving — it
proves the narrower thing, that the app works when frontmost. The right read
starts with the step kind: if it is `dragPath`, `hover`, `click` or `key`, the
plane is correct and the narrower claim is what you have. If it is a `type` or a
`scroll`, every accessibility route was tried and conceded to the event stream,
which is itself a finding, because a control reachable only by synthetic input
is a control an assistive technology cannot operate either. What does not
happen is a silent fallback on an outright refusal: a node whose accessibility
route is refused fails the step and names both ways forward.

**A delegated step reporting `effect: "unverifiable"` or
`effect: "suspectedNoOp"`.** The wrong read is to take `ok: true` beside it and
count the step as done. `ok` says the call completed; `effect` is what the
backend claims about the action landing, and these two values are its way of
saying it cannot vouch for the second. Read `suspectedNoOp` as a step that
probably changed nothing and `unverifiable` as unproven, and settle it the way
you would settle any unproven claim — a `find` or an `assert` on the change the
step was supposed to make. This field is absent on a native run rather than
false, because the native backend judges a write by reading it back and has no
equivalent concept.

**A step or run recorded with the outcome `indeterminate`.** The wrong read is
to sort it into either pile. It means the delegated subprocess died mid-step or
answered too late, so nothing here can say whether the machine was touched.
Reporting it as a defect sends someone hunting a bug that may not exist;
counting it as a pass claims something nobody observed. The right read is
unproven in both directions: report it beside the skipped assertions, and re-run
the step if the answer matters.

**An assertion returned as skipped.** The wrong read is to count it with the
passes, or omit it because nothing failed. A skipped assertion was never
evaluated: the node did not resolve, the reference PNG was missing, the
reflector was unavailable, the capture was untrustworthy. The right read is that
the thing it was meant to check is unknown, and it belongs in the report as
unproven with its reason, alongside the matrix cells you did not run — a reader
who sees only passes and failures assumes the rest was checked.

**A stability run whose `notes` mention a run ending early.** The wrong read is
to take `firstDivergence` and `stepInstability` at face value. A run that ended
early contributed no hashes past its stopping point, so instability for the
later steps was computed over fewer runs than `runs` says, and a 0.0 over three
surviving runs is much weaker evidence than the same 0.0 over seven. The right
read is to treat the post-exit steps as measured at the surviving sample size,
fix what ended the run — usually a reset that did not restore the start state,
or a settle timeout — and re-run. If the early exit *is* the nondeterminism, the
app sometimes failing to reach step 2 at all, that is the finding, and it
belongs under flaky rather than defects until a completing run shows the same
failure.
