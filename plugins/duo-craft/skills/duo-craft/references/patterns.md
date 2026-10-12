# Layout patterns for iPhone Duo in React Native

Each pattern names the template file that implements it and the failure it prevents. Every one was
built into a shipping Expo app (dAIolog's investor app) and run on the Xcode 27.1 iPhone Duo
simulator, except where marked *not yet seen running*.

## 1. Branch on space and on whether a fold exists — never on the model

`lib/layout.ts` → `useLayout()` returns `compact | regular | expanded` from the width the screen
actually has (window minus each side's inset, or the pane's width inside a split). `lib/fold.ts` →
`useFold()` returns `hasFold`, `posture` (`none | flat | book | tabletop`), `verticalFoldX`,
`horizontalFoldY` and `gap`.

- iPhone Duo is an iPhone to every API that names devices (`Platform.isPad` is false, `expo-device`
  says phone). A branch on the model either misses it or treats the open display as a phone.
- On a device with a fold, `regular` starts at 640pt so the open display in portrait (669pt) is
  regular, as iOS's size class says. iPad and phone tiers are unchanged.
- A fold is reported while flat too (inactive region, zero width). Decide the layout from `hasFold`
  once and do not rearrange as the hinge moves — Apple's grid example (prefer even columns whenever a
  fold exists) is the same rule.

## 2. List and detail, split at the fold or on a wide pane

`components/DetailPaneLayout.tsx` wraps a tab's list screen. The left pane keeps the tab's own screen
and the right pane renders what the list would have pushed. It splits in two cases:

- **With a fold:** at the fold, on the open display in landscape (flat or folded, at least 800pt wide).
- **Without a fold:** when the pane itself is at least 900pt wide (`SPLIT_MIN_WIDTH`), with the list
  about 36% of it, held between 320 and 420pt. The width comes from the pane's own `onLayout`, not the
  window, because on iPad the window includes the sidebar. iPad in landscape splits beside its sidebar
  (1180pt less 260pt); iPad in portrait (820pt) and a Split View half keep one pane, as Mail and
  Settings do.

With one pane `open(id)` pushes, exactly as before. A list opens rows through
`useOpenDetail(push, firstId)`, which opens beside the list when split, pushes otherwise, and offers
`firstId` as the default so the right pane is never blank.

What made it work in a real app:

- **Default the detail pane to the first item.** An empty right half reads as broken; Apple's Mail
  and Settings always show a selection, and Microsoft's dual-screen guidance says the same.
- **Closing the device on a chosen item pushes it full screen.** State survives the fold; a reader
  should not land back on the list. (`DetailPaneLayout` does this; its test fails without it.)
- **Each pane gets its own width and its own outer insets.** `PaneWidthContext` makes `useLayout`
  inside the left pane read 462pt, so the list lays out as the phone screen it is. The right pane
  stops at the side bar instead of padding for it, and neither pane pads for the fold.
- **Make detail screens embeddable.** Split the route file into the route (`useLocalSearchParams`)
  and a component taking `{ id }`, and set its options through `RouteOptions` (pattern 11), never
  `<Stack.Screen options>`. `Stack.Toolbar` items inside the embedded screen land in the tab's bar —
  show that bar transparent while split so the items reach the side column.
- **Require embedded detail screens on first use, not at import.** A static import of the company
  screen into the Following tab pulled `react-native-keyboard-controller`'s native module into every
  tab test and failed six suites. `require()` inside the render keeps the tab light and only loads
  the detail when split.
- Apple's own split ratio is about 35/65 flat and 50/50 folded (Mail, Reminders). Splitting at the
  fold in both poses matches the folded case and avoids a layout jump when the hinge moves.

## 3. Two columns that meet at the fold

`components/FoldColumns.tsx` measures its row in the window. If a vertical fold falls inside it with
room either side, the left column ends at `foldX - gap/2`; otherwise the columns share the row by
flex (a 3:2 iPad layout stays 3:2). Use it for dashboards and side-by-side sections that are not
list → detail. Without it, a 3:2 row puts a card across the hinge.

## 4. Tabletop: content up, controls down

`components/FoldColumns.tsx` → `FoldRows` puts `top` above an active horizontal fold and `bottom`
below the gap. Use it when `posture === 'tabletop'` on screens with something to watch (a chart, a
video): the viewable thing goes up, its range picker, transport or actions go down. Keep every
control the other poses have — rearrange, never remove. Other tabs keep their normal layout so
nothing is out of reach. Seen on the Duo simulator: the chart sat on the raised half and its range
picker below the fold.

Split a component whose controls are welded to its content (a chart with its range pills) into a
controlled pair (`range` / `onRangeChange` / `showRanges={false}` + a separate picker) so the two
halves can sit either side of the fold.

## 5. A companion pane

When a screen opens a sheet that is about the screen (Ask about this company, a transcript, a
filter), open it in the right pane instead while split: the subject stays readable beside it. The
same `TwoPane` geometry applies. From an embedded detail pane, push the full screen with the
companion open (`?tab=…`) rather than nesting splits.

## 6. Titles clear the top even when the inset is 0

`components/ScreenTitle.tsx` + `titleTopPadding()`. With the status bar on the side, the top inset is
0 and `insets.top + 8` puts the title 8pt from the edge. Owner feedback rejected 20pt as still too
tight; 59 + 8 (where it sits on every other iPhone) matched iOS Settings, which starts content ~83pt
down on the same display.

## 7. Pushed screens pad each side for its own inset

A native-stack screen fills the window; if its `contentStyle` only centres a reading column, its
content runs under the 84pt side bar to within 2pt of the back button. Pad
`paddingLeft: insets.left + column, paddingRight: insets.right + column`. Tab screens that wrap
their content in a page that already pads each side are fine.

## 8. Bars go vertical only if they are native bar items

- Header actions as `Stack.Toolbar.Button` / `Menu` (icon + accessibility label), not buttons drawn
  in a `View`. An item with only text stays horizontal; give every item an icon and a title.
- Tabs as `NativeTabs` with an icon and a label per trigger. Keep `sidebarAdaptable` off when
  `hasFold`.
- Order down the side bar is back → prominent action → other actions → tabs (Apple).
- Controls that act on one pane stay with that pane (Mail keeps the list's filter above the list).

## 9. Split View, PiP and resizing need nothing special if 1–8 hold

Split View halves (~475pt) are compact, so the phone layout applies; the bar sits on the outer edge,
which flips the side insets. PiP pinned shrinks the height live. Both only break apps that cache
sizes: replace `Dimensions.get` with `useWindowDimensions`, and size things inside sheets with
`onLayout` (a sheet is narrower than the window).

## 10. The hinge is for effects, not layout

Read hinge angle only to drive an effect (a reveal, a parallax, a whammy bar), reset it when the
status leaves `partiallyOpen`, give devices without a hinge the end state, and honour Reduce Motion.
Layout keys on `posture` and the fold geometry, which the system already decided from angle and
orientation.

## 11. A screen drawn in a pane sets its options through `RouteOptions`

A detail screen shown in the right pane is still a route's component, and a `<Stack.Screen options>`
inside it sets options on the stack that hosts the pane: the tab's own screen, whose title and header
actions it then replaces. Give every embeddable screen a `RouteOptions` wrapper instead. Pushed, it
renders `<Stack.Screen options>` unchanged. Inside a pane (an `EmbeddedRouteContext` that
`DetailPaneLayout`'s right pane provides) it draws the title and `headerRight` as the pane's own top
row, padded with `titleTopPadding()`, so a screen's actions stay with that screen whichever way it is
shown. Keep one registry of the routes a pane can draw, so a route added later is either registered
or pushes rather than half-rendering.

A pushed screen that is itself a list splitting into list and detail needs the whole window. When the
root stack caps pushed screens at a reading-column width through `contentStyle`, exempt those routes
by name whenever the window can split (a fold pane exists, or the window is at least
`SPLIT_MIN_WIDTH`); capped, the pane never reaches 900pt and never splits.

## 12. Phones stay portrait; the Duo and iPad turn

To keep a regular iPhone in portrait while the Duo and iPad rotate, decide in native code, because
the Duo is an iPhone to Info.plist as to every other API:

- Allow all four orientations on iPhone in `ios.infoPlist.UISupportedInterfaceOrientations`, and keep
  `"orientation": "portrait"` in `app.json`, which then only governs Android.
- Add an `ExpoAppDelegateSubscriber` implementing `application(_:supportedInterfaceOrientationsFor:)`
  and register it under `apple.appDelegateSubscribers` in the fold module's `expo-module.config.json`.
  It returns `.all` off iPhone, `.allButUpsideDown` once a fold has been seen, and portrait otherwise.
- Detect the fold from the window (`reservedRegions(kind: .division, options: .includeInactive)` is
  non-empty) and from the module's first reading. When the module first sees one, call
  `setNeedsUpdateOfSupportedInterfaceOrientations()` on the root view controller, so the outer display
  turns without a relaunch.

Seen on the Xcode 27.1 simulators: an iPhone 18 Pro held portrait when rotated, and the Duo's outer
and inner displays both turned. This is not in the templates, because an app that rotates on every
iPhone does not want it; the starter sets `"orientation": "default"` instead.

## Design before code

Mock every pose in HTML first, through `design-craft:design-craft` with `ux-craft:ux-craft`, at
Apple's point sizes (outer 466×678, inner 951×669 / 669×951, fold at 475.5, 84pt bar). Show the app
as it is today beside each proposed state. The owner of the reference app asked for exactly this,
and the mock caught that the inner display in portrait fell into the phone tier before any code was
written. `apple-reference-screens.md` records what Apple's own apps do in each pose.
