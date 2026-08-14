# The tools

Every argument name, default and enum below comes from the server's tool
catalogue. An argument absent from this page is absent from the schema — the
server rejects unknown keys rather than ignoring them, so a guessed argument
fails the call. All example values are **illustrative**: plausible shapes, not
captured runs.

## What gets advertised, and what it costs

The server ships **19 tools** and advertises a subset chosen by the shim's
`--profile` flag. The catalogue is re-sent on every turn and survives context
compaction, so it is a standing cost paid before any work happens:

| Profile | Tools | Roughly |
|---|---|---|
| `core` | `apps` `snapshot` `find` `act` `capture` `zoom` `wait` `assert` `menu` `doctor` | 6.8k tokens |
| `scripting` | core + `flow` `stability` `dictionary` `policy` | — |
| `full` | all 19 | 11.3k tokens |

`core` is the ten that actually drive a Mac and is the right default. Widen only
when the campaign genuinely needs flows, determinism runs, policy, `kill`, or
the CUA adapters.

This page documents the tools a campaign uses directly. Six more exist and are
named here rather than specified, because their schemas belong to the profiles
that advertise them: `proctor_flow` and `proctor_stability` (documented below),
`proctor_policy` and `proctor_kill` (the policy gate and process control),
`proctor_dictionary` and `proctor_unlock` (scripting-dictionary introspection
and the unlock path), and `proctor_computer` / `proctor_openai_computer` (the
CUA schema façades, which exist so a model trained on Anthropic's or OpenAI's
computer-use schema can drive Proctor without translation). Read the live
catalogue for their arguments rather than guessing.

## `proctor_doctor`

Whether a campaign can run at all, before anything is attributed to the app.

| Argument | Type | Default | Notes |
|---|---|---|---|
| `verbose` | boolean | false | Per-app observer and cache detail. |

Returns `agentVersion`, `protocolVersion`, `osVersion`, `agentRunning`,
`socketPath`, `grants[]` (`name`, `granted`, `required`, `howToFix`),
`attachedApps[]`, `observersLive`, `secureEventInputActive`,
`shortcutsCLIAvailable`, `ready`, `blockers[]`. `howToFix` is version-specific
because the fix genuinely differs by OS version.

**Over its neighbour:** always before `apps`. An attach with no Accessibility
grant returns an empty tree, indistinguishable from an app that never adopted
accessibility — one costs thirty seconds in System Settings, the other an hour
of selector debugging. `secureEventInputActive: true` is not a blocker but
narrows the plan: process-directed steps all still run, synthetic-event steps
become unreliable.

```jsonc
{ "verbose": true }
// → { "osVersion":"26.5.1", "ready":false, "secureEventInputActive":true,
//     "grants":[{"name":"Screen Recording","granted":false,"required":true,
//       "howToFix":"System Settings > Privacy & Security > Screen & System Audio Recording."}],
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
| `maxNodes` | integer | 2000 | Truncation reported in provenance. |
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
`modifiers`, `delta`, `point`, `label`, `settle`. Step kinds: `press`,
`setValue`, `focus`, `menu`, `type`, `key`, `scroll`, `increment`, `decrement`,
`pick`, `confirm`, `cancel`, `raise`, `close`, `resize`, `move`, `dragPath`,
`hover`, `click`, `shortcut`, `appleScript`, `waitFor`. Of these, `dragPath`,
`hover` and `click` are the synthetic-event kinds — they need the target
foreground and report `plane: "syntheticEvent"`. `shortcut` runs the app's
declared contract and reports `declared`; `appleScript` reports `appleEvents`;
everything else travels `accessibility`.

The `settle` object takes `quietFrames`, `dirtyThreshold`, `axQuietMs`,
`timeoutMs`, `requireReflectorIdle` — defaults 2, 0.002, 250 ms, 5000 ms,
false. Raise `timeoutMs` for a step that genuinely takes time rather than
accepting a `timeout` settle and reasoning over an unproven result.

Returns `window`, `steps[]`, `completed`, `failedAt`, `finalHash`; each step
result carries `index`, the submitted `step`, `ok`, `plane`, `error`, a
`SettleReport`, `stateHash`, `diff`, `elapsedMs`. On failure the batch stops, so
you get the state at the point of failure rather than a cascade.

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
`minHitSize`, `contrast`, `focusOrder`, `regionMatches`, `agree`.

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
seen), `notes[]`. `stepInstability` is the fraction of runs that did not reach
the modal state at that step. Three runs detects gross nondeterminism; five to
ten is the useful range for a flow about to become a gate.

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

---

## Reading results honestly

Five results whose obvious reading is wrong in a specific way.

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
starts with the step kind: if it is `dragPath`, `hover` or `click`, the plane is
correct and the narrower claim is what you have. If it is not, the accessibility
path did not exist for that node and the server fell back — itself a finding,
because a control reachable only by synthetic click is a control an assistive
technology cannot operate either.

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
