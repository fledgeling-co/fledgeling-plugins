---
name: duo-craft
description: Build or adapt a React Native / Expo app for iPhone Duo, Apple's foldable iPhone — two panes split at the fold, the vertical side bar, asymmetric safe-area insets, book and tabletop poses, Split View halves, and the iOS 27 scene-lifecycle crash. Ships a tested native fold module, layout components, an audit script and a starter. Use when a React Native or Expo app needs to work on iPhone Duo or a foldable iPhone, when someone mentions the fold, hinge, reserved regions, UIHingeInteraction, the inner or outer display, or an Expo app crashing at launch on the iOS 27 SDK — even if they only say "make it look right on the Duo".
---

# duo-craft

iPhone Duo is an iPhone to every API that names a device, so a React Native app runs on it
unchanged and looks wrong in ways no simulator other than the Duo shows. The bars stand down the
trailing edge and take 84pt off one side only. The open display is 951×669pt with a fold at
475.5pt, so a phone column stretched across it puts a card over the hinge. Split View hands the app
a half whose side bar is on the *left*. And an Expo SDK 57 app built with the iOS 27 SDK does not
reach its first screen at all.

This skill turns that into code. It carries a native fold module that has run on the Duo simulator
in a shipping app, the layout components built on it, a static audit that finds the assumptions
that break, and a starter that a fresh `create-expo-app` becomes in one command. React Native has no
fold API of its own, and no third-party fold library has the adoption to depend on
(`references/libraries.md`), so the module ships here as source the app owns.

Deliver what was asked, at the scope intended. Adapting one screen means that screen and the shared
pieces it needs, not every screen in the app; a new app means the starter plus what the user
described; a crash fix is the fix, why it works and, when the user asks for it to stay fixed, the bundled
`scripts/check-scene-lifecycle.mjs`, which `install_templates.py` adds and runs before the `ios`
script. It fails when the opt-in leaves `app.json`, when `expo` drops below 57.0.23, and when a
generated `ios/` still starts its own window, the half-fix that launches to a black screen. Say in one sentence where a wider change would
help, then build what was asked.

Write the report for someone who has the app and not this skill: cite the app's files and Apple's or
Expo's documentation, never this skill's references or this machine's paths, and leave out findings
about parts of the app the task did not touch.

When the request is a question rather than a change — "should I use this library", "why does it
crash" — answer it in 25 lines or fewer: the answer first, the reason, and what to do instead. Claim only what
the evidence supports: a library's source read is a source read, not a test on a real device, so say
"its fold path is compiled out unless you set the flag", not "it reports no fold on a real Duo".
Recommend the bundled module by what it is and how to install it, since the reader may not have this
skill. Answer only
the question asked. Leave out other libraries, other Duo problems and the launch crash unless the
user asked about them; the user asked one thing, and an answer padded with neighbouring advice reads
as not having listened. The procedure below is for changing an app, not for answering a question.

## Facts to lay out against

Every number comes from Apple's iOS 27 design resource and the iPhone Duo Tech Talks; the poses were
confirmed on the Xcode 27.1 Duo simulator. Read them through the hooks, never as constants in a
layout: the window changes size every time the device opens, folds, rotates or enters Split View.

| Pose | Window (pt) | Bars and insets |
|---|---|---|
| Closed (outer display) | 466×678 | One vertical bar, 84pt trailing; top inset 0 |
| Open, landscape (flat or book) | 951×669, fold at x 475.5 | 84pt trailing bar; top inset 0 |
| Open, portrait (flat or tabletop) | 669×951, fold at y 475.5 | Horizontal bars: 84pt top, 95pt bottom |
| Split View half | about 475×669 | Bar on the half's outer edge, so the left app's inset is on its left |

The fold APIs — `UIView.reservedRegions(kind:options:)` and `UIHingeInteraction` — exist only in
the iOS 27.1 SDK. Build the whole app with Xcode 27.1 or the module fails to compile, which is the
point: it cannot quietly report no fold.

## Procedure

### 1. Read the app, then run the audit

For an existing app, read its root layout, tab layout, one list screen and one detail screen, then
run the audit from this skill's directory:

```bash
python3 scripts/duo_audit.py <app-root>           # file:line findings; exit 1 when any is an error
```

It runs 13 checks, from `stale-dimensions` (a `Dimensions.get` snapshot that goes stale on the
first fold) to `no-scene-lifecycle` (Expo below 58 with no scene delegate: the launch crash) and
`sdk-too-old` (the active Xcode's iOS SDK is below 27.1; it names an installed Xcode 27.1 to point
`DEVELOPER_DIR` at, so run the audit with that set). Each finding
carries its reason. Treat `error` as visibly wrong on the Duo, `warn` as a place to confirm on the
simulator, and `info` as somewhere to look rather than a defect.

For a new app, create it first (`npx create-expo-app@latest`), which today gives Expo SDK 57 with
the `@/*` → `./src/*` alias.

### 2. Mock the poses before changing layout

When the work changes how more than one screen lays out, mock it in HTML first with
`design-craft:design-craft` and `ux-craft:ux-craft`: the app as it is beside each proposed state, at
the point sizes above, covering the nine poses in `references/simulator.md`. The owner of the app
this skill came from asked for exactly that, and the mock showed the inner display in portrait
falling into the phone tier before any code existed. The mock earns its cost when someone reviews it
before the code; in a run with nobody to review it, skip it and say so in the report. A single-screen
fix or a new starter app skips it too.

`references/apple-reference-screens.md` records what Apple's own apps do in each pose — read it
before deciding a split ratio, where a control goes, or what a sheet does on the fold.

### 3. Install the module and the layout pieces

```bash
python3 scripts/install_templates.py <app-root>             # adapt: module, hooks, components
python3 scripts/install_templates.py <app-root> --starter   # new app: also the starter screens
```

It copies `modules/duo-fold` (Swift, autolinked from `./modules`), `lib/fold.ts` (`useFold`,
`useTwoPane`), `lib/layout.ts` (`useLayout`, `titleTopPadding`, `PaneWidthContext`),
`components/DetailPaneLayout.tsx`, `FoldColumns.tsx` (with `FoldRows`) and `ScreenTitle.tsx`. It
rewrites imports to the app's own alias, never overwrites an existing file (a skipped file is yours
to merge by hand), and on Expo SDK 57 turns on Expo's own scene opt-in — `expo-build-properties`
with `"ios": { "enableSceneSupport": true }` — adding the package to `package.json` (then run
`npx expo install expo-build-properties`). That opt-in needs `expo` 57.0.23 or later; below it the
script says to upgrade the patch or move to SDK 58, which adopts scenes itself.
With `--starter` it replaces the fresh app's route files (keeping the originals in
`.duo-craft-backup/`) and changes create-expo-app's `"orientation": "portrait"` to `"default"`: the
outer display honours the lock and the inner display rotates regardless.
`--with-tests` adds the two test files; they need `jest-expo` and `@testing-library/react-native`.

### 4. Apply the patterns

`references/patterns.md` has the ten patterns with the template that implements each and the
failure it prevents. The ones that decide most of the result:

- **Branch on space and on `hasFold`, never on the model.** `Platform.isPad` is false and
  `expo-device` says phone, so a device branch either misses the Duo or treats the open display as
  a phone. `useLayout()` gives `compact | regular | expanded` from the width the screen actually has.
- **Pad each side for its own inset.** `paddingLeft: insets.left + margin`, `paddingRight:
  insets.right + margin`. Symmetric math is wrong on every pose here, and Split View flips which
  side carries the bar.
- **List and detail split at the fold.** Wrap the tab's list in `DetailPaneLayout`; with two panes
  the right one renders what the list would have pushed. Select the first item by default, because
  an empty right half reads as broken, and push the chosen item full screen when the device closes.
- **Bars move to the side only as native bar items.** Use `NativeTabs` triggers with an icon and a
  label and `Stack.Toolbar` buttons with an SF Symbol (Apple's system icon set). A header or tab bar
  drawn in a `View` stays where it was drawn, across the content. Wire every item to its action —
  `Share.share`, a navigation, a mutation — because an item with an empty handler is a dead control
  standing in the side bar.
- **Titles clear the top when the inset is 0.** Use `titleTopPadding()` (59 + 8pt). The owner
  rejected 20pt as touching the edge and accepted 67pt; Settings starts its content about 83pt down.
- **Tabletop puts content on the raised half and controls on the flat half** with `FoldRows`,
  keeping every control the other poses have.
- **The hinge angle drives effects only.** Layout keys on posture and fold geometry.

### 5. Build with Xcode 27.1 and look at every pose

`references/simulator.md` has the commands, the Device Hub repair, and the pose matrix. Set
`DEVELOPER_DIR` per command (`xcrun --sdk iphoneos --show-sdk-version` must print 27.1 or later)
rather than `xcode-select`, which changes the machine for every project. A Release build embeds
the JavaScript, so it needs no Metro.

Device Hub is the only way to fold, rotate or enter Split View, and driving it takes the user's
mouse and focus. Ask before clicking through it, or have the user set each pose while you capture.
Open each capture and read it; `be-my-witness:be-my-witness` gives a region-by-region read when a
pose is in doubt.

### 6. Report

Lead with what changed and what you observed, never with a prediction ("launching will work now" is a
claim nothing here measured). When the change affected layout, follow with a table of the nine poses with one status each —
`seen` (a capture you opened), `not reached` with the reason, or `not built`. Then the files
changed and anything the user has to do (switch Xcode for their release pipeline, set a pose).
A fix that does not touch layout, such as the launch crash, skips the pose
table. Keep it under 40 lines. A pose marked `seen` without an opened capture behind it is the one claim
this report cannot carry.

## When the toolchain is missing

Without Xcode 27.1 or the iOS 27.1 simulator runtime (a 7.85 GB download), do steps 1–4, run
`npx tsc --noEmit` and the template tests, and report every pose as `not built` with that reason.
The code is still right; nothing about it has been seen running, and the report says so.

## Delegation

Do this in one session. The steps depend on each other in order, and a subagent would have to
re-read the app to make a layout call. One subagent pays for itself only on a wide audit across an
app with more than about 40 screens, returning the list of screens that need each pattern. Use at
most one.

## Files

| Path | Read it when |
|---|---|
| `references/patterns.md` | Applying any layout change (step 4) |
| `references/apple-reference-screens.md` | Deciding a split, a control's place, or sheet behaviour |
| `references/simulator.md` | Building, repairing Device Hub, capturing displays, the pose matrix |
| `references/libraries.md` | Someone names a fold library, or asks why the module is bundled; the SDK and scene table |
| `references/evidence.md` | A rule needs its source |
| `scripts/duo_audit.py` | Step 1; `--self-test` proves each check fires |
| `scripts/install_templates.py` | Step 3; `--dry-run` lists what it would write |
| `templates/` | The installed source, if a file needs merging by hand |
