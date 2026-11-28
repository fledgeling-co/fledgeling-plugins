---
name: duo-craft
description: Build or adapt a React Native / Expo or SwiftUI app for iPhone Duo, Apple's foldable iPhone — list and detail panes on the open display, actions in the vertical side bar, native sheets the system places, asymmetric safe-area insets, the split keyboard, book and tabletop poses, Split View halves, and the iOS 27 scene-lifecycle crash. Ships a tested native fold module and a SwiftUI fold reader, layout components, a keyboard lift, an audit script and a starter, builds mocks as native apps on the Duo simulator, and reviews each capture against the defects the owner has reported on a real Duo. Use when a React Native, Expo or SwiftUI app needs to work on iPhone Duo or a foldable iPhone, when someone mentions the fold, hinge, side bar, reserved regions, UIHingeInteraction, the inner or outer display, or an Expo app crashing at launch on the iOS 27 SDK — even if they only say "make it look right on the Duo".
---

# duo-craft

iPhone Duo is an iPhone to every API that names a device, so a React Native app runs on it
unchanged and looks wrong in ways no simulator other than the Duo shows. The bars stand down the
trailing edge and take 84pt off one side only. The open display is 951×669pt with a fold at
475.5pt, so a phone layout stretched across it puts a row's label 600 to 800pt from its value. Split View hands the app
a half whose side bar is on the *left*. And an Expo SDK 57 app built with the iOS 27 SDK does not
reach its first screen at all.

This skill turns that into code. It carries a native fold module that has run on the Duo simulator
in a shipping app, the layout components built on it, a static audit that finds the assumptions
that break, and a starter that a fresh `create-expo-app` becomes in one command. React Native has no
fold API of its own, and no third-party fold library has the adoption to depend on
(`references/libraries.md`), so the module ships here as source the app owns.

Runs have used this skill on SwiftUI apps as often as on React Native ones. The rules are the same;
for a SwiftUI app, copy `templates/swiftui/Fold.swift` into the target and read
`references/swiftui.md`, which maps each pattern to SwiftUI. The audit in step 1 and the installer
in step 3 are React Native only.

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

Open, the system keyboard is one 951pt panel split around the fold, its top at y 391 (y 428 without
a suggestion row); closed, it is 466pt wide from y 374. A modal sheet opens centred on the fold,
usually 653pt wide. Both come from 321 captures of shipping apps on a device
(`references/device-captures.md`).

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

It runs 14 checks, from `stale-dimensions` (a `Dimensions.get` snapshot that goes stale on the
first fold) to `no-scene-lifecycle` (Expo below 58 with no scene delegate: the launch crash) and
`sdk-too-old` (the active Xcode's iOS SDK is below 27.1; it names an installed Xcode 27.1 to point
`DEVELOPER_DIR` at, so run the audit with that set). Each finding carries its reason. Treat `error`
as visibly wrong on the Duo and `warn` as a defect to fix or to explain, one line each, in the
report. `hidden-header-own-buttons` and `drawn-bar-action` find buttons drawn where the side bar
should hold them, the defect the owner reported most; one run filed its five findings as notes and
shipped them.

For a new app, create it first (`npx create-expo-app@latest`), which gave Expo SDK 58 on 2026-10-30
(SDK 57 before that), with the `@/*` → `./src/*` alias. Its own web and CSS files fail `tsc` in 3
places on SDK 58 before anything is installed, so compare against a fresh app before blaming a change.

### 2. Mock the poses as a native app before changing layout

When the work changes how more than one screen lays out, or the user asks for a mock, build the mock
as a native app that runs on the Duo simulator: SwiftUI, or the app's own stack, with fixture data and
every screen and state reachable. Take direction and states from `design-craft:design-craft` and
`ux-craft:ux-craft`, show the app as it is beside each proposed state, and cover the nine poses in
`references/simulator.md`. Between 12 and 28 November 2026 the owner asked six times for the mock as
a real app ("Use real swift app in simulator for the mock"), often sent to TestFlight. The side bar,
native sheets, their placement and the split keyboard are drawn by iOS, so an HTML mock can only
imitate them, and the defects the owner rejected most (buttons drawn in the content, an overlay
standing in for a sheet) are ones an HTML mock builds in. Make an HTML mock only when the user asks
for one or Xcode 27.1 is missing.

Keep the product's own look: its colours, type, components and tone from its design doc or live app.
This skill decides where things go on the Duo, not how the product looks, and a set of Duo mocks that
had swapped the product's design for stock iOS came back with "the aesthetic … seems to have been
lost in the app mocks".

The mock earns its cost when someone reviews it before the code; in a run with nobody to review it,
skip it and say so in the report. A single-screen fix or a new starter app skips it too.

`references/apple-reference-screens.md` records what Apple's own apps do in each pose, and
`references/device-captures.md` what 38 shipping apps do on a real device, with measurements. Read
the section you need before deciding a split ratio, where a control goes, what a sheet does on the
fold, how wide rows and text run, or how the keyboard meets the layout.

### 3. Install the module and the layout pieces

```bash
python3 scripts/install_templates.py <app-root>             # adapt: module, hooks, components
python3 scripts/install_templates.py <app-root> --starter   # new app: also the starter screens
```

It copies `modules/duo-fold` (Swift, autolinked from `./modules`), `lib/fold.ts` (`useFold`,
`useTwoPane`), `lib/foldHandoff.ts` with `components/FoldHandoff.tsx` (opening the Duo brings a
pushed detail back into its pane), `lib/keyboard.ts` (`useKeyboardLift`), `lib/layout.ts`
(`useLayout`, `titleTopPadding`, `PaneWidthContext`),
`components/DetailPaneLayout.tsx`, `FoldColumns.tsx` (with `FoldRows`) and `ScreenTitle.tsx`. It
rewrites imports to the app's own alias, never overwrites an existing file (a skipped file is yours
to merge by hand), and on Expo SDK 57 turns on Expo's own scene opt-in — `expo-build-properties`
with `"ios": { "enableSceneSupport": true }` — adding the package to `package.json` (then run
`npx expo install expo-build-properties`). That opt-in needs `expo` 57.0.23 or later; below it the
script says to upgrade the patch or move to SDK 58, which adopts scenes itself.
With `--starter` it replaces the fresh app's route files (keeping the originals in
`.duo-craft-backup/`) and changes create-expo-app's `"orientation": "portrait"` to `"default"`: the
outer display honours the lock and the inner display rotates regardless. An app that keeps regular
iPhones in portrait while the Duo and iPad turn needs the native rule in pattern 12 instead.
`--with-tests` adds the six test files; they need `jest-expo` and `@testing-library/react-native`,
and pass 37/37 on Expo SDK 58.
The templates take colours through `systemColor` in `lib/layout.ts`, never `PlatformColor` at module
scope: from SDK 58 a fresh app sets `"web": { "output": "server" }`, which loads every route on
react-native-web while the iOS app builds, and react-native-web has no `PlatformColor`. An app's own
routes that call it in `StyleSheet.create` fail the Release build the same way
(`PlatformColor is not a function`); route them through `systemColor` too.

### 4. Apply the patterns

`references/patterns.md` has the eighteen patterns with the template that implements each and the
failure it prevents; patterns 13 to 16 are observed on a device, and 17 and 18 come from what the
owner reported on one. The ones that decide most of the result:

- **Every screen-level action is a native bar item.** Close (`xmark`), Done or Save (`checkmark`),
  Send, Add a photo, New, Invite and Share go in `Stack.Toolbar` (SwiftUI: `ToolbarItem` with
  `.cancellationAction`, `.confirmationAction`, `.primaryAction`), with an SF Symbol (Apple's system
  icon set) and a label, and
  tabs go in `NativeTabs`. iOS stands them in the side bar on the Duo; a button drawn in a `View` stays
  across the content. The owner reported drawn buttons 13 times across 5 apps between 28 October and
  27 November 2026, more than any other defect, including in a run that had been handed this skill.
  Wire every item to its action, because an item with an empty handler is a dead control in the side
  bar, and put each action in one place. Closed, the side bar holds back and two actions before the
  rest fold into a ••• menu, so keep the primary action in those two. A pane drawn inside a split
  keeps its actions in its own top row, and Android keeps them inline (pattern 8).
- **Present sheets natively and let iOS place them.** Use the page sheet (`presentation: 'modal'`;
  SwiftUI `.sheet`) with Close and the affirmative action as bar items, and give every modal a way to
  close. iOS 27.1 then does what the App Store does on a Duo: a centred card open flat, one page half
  folded, full height with Close and ✓ in the side bar when closed or in portrait. Forcing modals full
  screen, a short form sheet floating with the app around it, a square background inside the rounded
  sheet, and a modal given a width or offset each broke it in one app (pattern 14).
- **Backgrounds run under the side bar; text and controls stop before it.** Put the screen's colour,
  banners and media on the outermost view and the per-side inset padding inside it. The owner
  reported a strip of a different colour beside the bar 6 times in 5 apps. When the app chooses light
  or dark itself, force the system's appearance to match, or iOS draws the bar in the other one
  (pattern 16).
- **Every top-level screen uses the open display.** Decide per screen: list and detail, columns,
  controls beside their result, or a capped column with something beside it. A phone layout
  stretched or centred across 951pt came back as "a giant iPhone app" and "a significant amount of
  wasted space" (pattern 17).
- **List and detail on the open display, and on any pane at least 900pt wide.** Wrap the tab's list
  in `DetailPaneLayout`; with two panes the right one renders what the list would have pushed. Open and
  flat, the list is a fixed 320pt column and the fold falls inside the detail, as in 21 apps measured
  on a device; folded like a book, the panes divide at the fold. Without a fold it measures the pane,
  not the window, so iPad's sidebar does not count. Rows with meters, figures or several values take
  `listWidth="fold"`, because the owner found 320pt cramped for them. Select the first item by
  default, because an empty right half reads as broken. Keep what is on screen across the fold: the
  chosen item goes full screen when the device closes, and a detail open on the closed display
  becomes the right pane, with the list beside it, when it opens. In React Native that takes
  `FoldHandoff` in the root layout and `handoffTab` on the list. Every tab that drills down is a
  split, Settings included: the owner reported a Settings page left full screen on opening in two
  apps (pattern 2).
- **Closed, the app is a phone app with a side bar.** Rows push with the standard animation, every
  pushed screen has a back item even when nothing is behind it, an action inside a screen pushes or
  presents rather than switching tabs, and no band of colour sits under a transparent header
  (pattern 18).
- **Lift composers above the split keyboard with `useKeyboardLift`.** The keyboard covers up to 42%
  of the open display and does not resize a sheet. `KeyboardAvoidingView` measures from a stale
  layout in a pane, so the owner saw the input clear the keys only "on occasion"; the hook measures in
  the window on every keyboard event. Keep the composer 16pt above the keys; the owner sent 8pt back
  (pattern 13).
- **Titles are the native navigation title.** The owner rejected drawn titles that sat differently
  from tab to tab. Draw one with `ScreenTitle` and `titleTopPadding()` (59 + 8pt) only where a screen
  has no native header, such as a pane in a split (pattern 6).
- **Branch on space and on `hasFold`, never on the model.** `Platform.isPad` is false and
  `expo-device` says phone, so a device branch either misses the Duo or treats the open display as
  a phone. `useLayout()` gives `compact | regular | expanded` from the width the screen actually has.
- **Pad each side for its own inset.** `paddingLeft: insets.left + margin`, `paddingRight:
  insets.right + margin`. Symmetric math is wrong on every pose here, and Split View flips which
  side carries the bar.
- **A screen drawn in a pane sets its options through `RouteOptions`.** A `Stack.Screen` inside the
  right pane renames the tab that hosts it.
- **Tabletop puts content on the raised half and controls on the flat half** with `FoldRows`,
  keeping every control the other poses have.
- **The hinge angle drives effects only.** Layout keys on posture and fold geometry.

### 5. Build with Xcode 27.1 and look at every pose

`references/simulator.md` has the commands, the Device Hub repair, and the pose matrix. Set
`DEVELOPER_DIR` per command (`xcrun --sdk iphoneos --show-sdk-version` must print 27.1 or later)
rather than `xcode-select`, which changes the machine for every project. A Release build embeds
the JavaScript, so it needs no Metro.

Device Hub is the only way to fold or rotate. Drive it yourself, with `proctor:proctor` or the
bundled click tool: the owner said "You can operate the app yourself in future", and when a run
reported an unfold as unchecked because Device Hub "couldn't be driven", answered that it had complete
control of the computer. `references/simulator.md` has both routes and the pose-bar order. Say in one
line that you are taking the mouse, then set each pose. Device Hub has no control for Split
View or picture in picture, so report those three poses `not reached` on the simulator.

Open each capture and read it against these ten defects, every one of them reported by the owner on
a real Duo after a run had called the screen done. `be-my-witness:be-my-witness` gives a
region-by-region read when a pose is in doubt.

1. A close, confirm, send, new or share button drawn in the content instead of standing in the side bar.
2. A side bar with no items on a screen that has actions, side tabs missing at launch, or the primary action hidden in the closed ••• menu.
3. A strip beside the side bar in a different colour from the screen, or a light surface left in dark mode.
4. A modal with no close control, gaps or pale corners around a sheet, or a sheet forced full screen.
5. A focused field or composer under the keyboard or less than 16pt above it.
6. The open display used as a stretched or centred phone column, or a list too narrow for its rows, with space left unused.
7. A title missing, or a different size or position from the other tabs.
8. A row that highlights without pushing or lacks its chevron, a missing back item, an action that switches tabs, a detail lost on unfolding.
9. Controls sitting on the bottom edge of the open display, or full-bleed media that cannot hide its chrome.
10. A menu that closes by itself while the screen updates, or tab icons the wrong size in the side bar.

Capture again only the screens whose code changed since their last capture. The owner objected to
unchanged screens being tested "over and over" when nothing in their code had moved.

### 6. Report

Lead with what changed and what you observed, never with a prediction ("launching will work now" is a
claim nothing here measured). When the change affected layout, follow with a table of the nine poses with one status each —
`seen` (a capture you opened), `not reached` with the reason, or `not built`. Then the files
changed and anything the user has to do (switch Xcode for their release pipeline, check a pose only
their own Duo can reach).
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
| `references/swiftui.md` | The app is SwiftUI: each pattern in SwiftUI, and three SwiftUI-only traps |
| `references/apple-reference-screens.md` | Deciding a split, a control's place, or sheet behaviour |
| `references/device-captures.md` | The same decisions with measurements from 38 apps on a device, plus keyboard, row width and flows; read one section, not the whole file |
| `references/simulator.md` | Building, driving Device Hub, repairing it, capturing displays, the pose matrix |
| `references/libraries.md` | Someone names a fold library, or asks why the module is bundled; the SDK and scene table |
| `references/evidence.md` | A rule needs its source |
| `scripts/duo_audit.py` | Step 1; `--self-test` proves each check fires |
| `scripts/install_templates.py` | Step 3; `--dry-run` lists what it would write |
| `scripts/click.swift` | Step 5; the click tool for setting poses in Device Hub |
| `templates/swiftui/Fold.swift` | A SwiftUI app: the fold reader, tiers and list width, copied into the target by hand |
| `templates/` | The installed source, if a file needs merging by hand |
