# Layout patterns for iPhone Duo in React Native

Each pattern names the template file that implements it and the failure it prevents. Every one was
built into a shipping Expo app (dAIolog's investor app) and run on the Xcode 27.1 iPhone Duo
simulator, except where marked *not yet seen running*. Patterns 13 to 16 come from 313 captures of
shipping apps on a real iPhone Duo (`device-captures.md`, cited as D01 to D34) and are marked
*observed on a device, not built here*: they say what apps do, not what a template has proved.

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
- Shipping apps re-flow one screen by the width it has: Stocks shows one news card beside its
  sidebar and two without it, Fitness one column closed and two open, Maps a leading panel open and a
  bottom sheet closed (D11).

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
- **On the flat open display, shipping apps fix the list instead of splitting at the fold.** In 60
  device captures across 21 apps the list or sidebar is a fixed 292–403pt column, 320pt in most, and
  the fold falls 72–183pt inside the detail (D01). A fold-aligned split appears only on pages of two
  equal halves (pattern 3). `DetailPaneLayout` splits at the fold whenever a fold exists, which
  matches book posture and is what the reference app's owner approved. When the user wants the flat
  display to match other apps, use `twoPaneForWidth`'s 320–420pt list while `posture === 'flat'` and
  keep the fold split for `book`, with a test for each posture; the template does not do this yet.
- **Selecting a row swaps the detail in place.** The sidebar keeps its scroll offset and shows the
  selection as a pill (Settings, Shortcuts, Journal; D22).
- **The alternative to a default selection is a labelled placeholder** ("No Event Selected",
  "Select a conversation"), centred on the detail pane rather than the fold, as Slack, Calendar,
  Siri and Termius do (D24).
- **A third column opens as an overlay.** Mail, Notes and Voice Memos slide a 280pt sidebar over the
  list with a scrim rather than resizing the panes (D26).

## 3. Two columns that meet at the fold

`components/FoldColumns.tsx` measures its row in the window. If a vertical fold falls inside it with
room either side, the left column ends at `foldX - gap/2`; otherwise the columns share the row by
flex (a 3:2 iPad layout stays 3:2). Use it for dashboards and side-by-side sections that are not
list → detail. Without it, a 3:2 row puts a card across the hinge.

Use it where you control the grid, not to keep every card off the fold. Shipping apps let ordinary
lists, text, charts and cards cross the fold with no gutter, Apple's own included (20 captures in 9
apps, D07); only Bear puts a grid's gutter on it (D29). Pages of two equal halves, such as a player
beside its queue or Calendar's Day view beside an event, divide at the fold with about a 50pt gutter
or a grabber on it (Music, Podcasts, Books, Calendar; D30), which is the case `FoldColumns` fits
best. A screenshot cannot show the crease or where a tap lands, so a gutter on the fold stays a
precaution rather than a measured need.

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

Device captures show the same for companions: Messages opens contact info as a 404pt pane and folds
its list into a toggle, Music opens the queue and lyrics, Podcasts the transcript (D33). They also
show the limit: a sheet about one list item (edit, share, settings for that item) opens centred on
the fold over both dimmed panes, not in the right pane (D13).

## 6. Titles clear the top even when the inset is 0

`components/ScreenTitle.tsx` + `titleTopPadding()`. With the status bar on the side, the top inset is
0 and `insets.top + 8` puts the title 8pt from the edge. Owner feedback rejected 20pt as still too
tight; 59 + 8 (where it sits on every other iPhone) matched iOS Settings, which starts content ~83pt
down on the same display. Device captures agree: system navigation rows sit at y 24–72pt with the
title centred on y 48, and the first card starts near y 82 (D21).

## 7. Pushed screens pad each side for its own inset

A native-stack screen fills the window; if its `contentStyle` only centres a reading column, its
content runs under the 84pt side bar to within 2pt of the back button. Pad
`paddingLeft: insets.left + column, paddingRight: insets.right + column`. Tab screens that wrap
their content in a page that already pads each side are fine. Shipping apps end text and controls
12–25pt before the bar's edge at x 867 in most captures (0–40pt across 23 apps), and at about x 382
when closed (D02, D10).

## 8. Bars go vertical only if they are native bar items

- Header actions as `Stack.Toolbar.Button` / `Menu` (icon + accessibility label), not buttons drawn
  in a `View`. An item with only text stays horizontal; give every item an icon and a title.
- Tabs as `NativeTabs` with an icon and a label per trigger. Keep `sidebarAdaptable` off when
  `hasFold`.
- Order down the side bar is back → prominent action → other actions → tabs (Apple).
- Controls that act on one pane stay with that pane (Mail keeps the list's filter above the list).
- The system places the items: 47–48pt circles and pills centred near x 903, the first action at
  y 125 open and y 175 closed, tabs bottom-aligned (D03). Screen actions (back, close, share, more,
  Done) take the top group and keep the same first slot from screen to screen; tabs and creation
  take the bottom group (D06).
- The first button moves down when the status stack grows (a low-battery banner, a microphone
  indicator), so a control positioned at a fixed y in the bar's column lands on the status items
  (D28). Declare it as a native item instead.
- The open keyboard covers the bar's lower half; tab pills stay blurred under it. Put a control that
  typing needs in the top group or in a keyboard accessory (D12).

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

## 13. The keyboard splits around the fold — *observed on a device, not built here*

Open, the system keyboard is one 951pt panel holding two key blocks (x 85–388 and 563–866) with a
175pt gap centred on the fold. Its top is at y 391 with a suggestion row and y 428 without, so it
covers up to 42% of the height. Closed, it is one 466pt piece from y 374 (D05). It runs under both panes
and the bar, and nothing in the app has to draw it.

- Keep the focused field or composer 8–20pt above the keyboard's top, read from keyboard events
  rather than a constant. ChatGPT, Claude, Messages and Shortcuts lift their composer this way (D09).
- The keyboard covers a form sheet without resizing it, so Calendar's New Event sheet hides its
  lower fields behind the keys. Make sheet content a `ScrollView` (D09).
- Float a keyboard accessory (a format toolbar, a search pill) 8–12pt above the keys, 44–48pt tall,
  ending before the bar: x 866 open, x 381 closed (D25).
- No capture here measured what `KeyboardAvoidingView` or `react-native-keyboard-controller` report
  for the split panel. Check the reported frame on the Duo simulator before relying on it.

## 14. Sheets, alerts and menus are native, and their size is the system's — *observed on a device*

- **Sheets.** Open, a modal sheet is centred on the fold: usually 653pt wide (x 149–802), top y 8,
  stopping 65pt short of the bar; partial-height sheets start at y 82 (D04, 83 captures in 24 apps).
  In some states the same sheet sits in the left half, 459pt wide (Calendar, Claude; D31). Present
  with the native `formSheet` or `pageSheet`, lay its content out with flex so it holds at 459pt and
  653pt, and never give a modal a width or a left offset.
- **Scrim.** A native modal's scrim dims the bar's buttons and tab pill and leaves the status items
  bright (D19). An overlay drawn inside the app's own tree cannot reach the bar.
- **Sheet header.** A 48pt round close or back button at the sheet's leading edge, the title centred
  on the fold, the action at the trailing edge, in a row at y 24–72; some apps put close at the
  trailing edge (D20). Closed, these buttons move into the bar from y 175 (D10).
- **Alerts.** Use the system alert: 319pt wide, centred on the 0–867pt content area at x 433.5.
  Permission prompts are 320pt and centre on the fold instead (D15).
- **Menus.** A menu is anchored to its trigger, usually 250pt wide; a menu from a bar button
  overlaps the bar, and one from a trigger near x 400–434 crosses the fold (D08). Attach a native
  menu to a `Stack.Toolbar` item so UIKit anchors and clamps it.

## 15. Wide panes need width limits — *observed on a device*

- Cap label-and-value and toggle rows at about 620–700pt, centred or inside a pane. Stretched to
  the full 867pt, a label sits 600–800pt from its value (ChatGPT, Apple TV, Fitness+, Screens; D16).
  Rows that are real table columns, as in Files, may fill the width.
- Keep reading text in chat and article panes to 300–570pt, about 30–70 characters: Claude 480pt,
  ChatGPT 437, Slack 427, Messages 381 (D17).
- Centre an element on the container that holds it: sheets and pages without a sidebar on the fold
  (x 475.5), in-app alerts and some empty states on the 0–867pt area (x 433.5), detail content on its
  pane (D14). Take the container's width from `onLayout`, never from half the window.

## 16. Backgrounds may run under the bar; text and controls stop before it — *observed on a device*

- Maps, artwork, hero images, separators and scroll indicators run under the trailing bar; text and
  controls stop at x 867 open and x 382 closed. Pad a horizontal carousel's content by the right
  inset so its last card scrolls clear of the bar's buttons (D18, 33 captures in 19 apps).
- The status items sit on a blur capsule over anything drawn beneath them, and text there is cut
  (Siri, D27). They stay in every view except full-bleed canvases: Calculator, a remote desktop, a
  camera.
- A camera view runs its preview to x 951 with the status bar hidden, puts its round controls in
  the bar from y 24, and keeps the shutter in the bar or left of x 867 (Measure, Translate, a
  document scanner; D34).

## Design before code

Mock every pose in HTML first, through `design-craft:design-craft` with `ux-craft:ux-craft`, at
Apple's point sizes (outer 466×678, inner 951×669 / 669×951, fold at 475.5, 84pt bar). Show the app
as it is today beside each proposed state. The owner of the reference app asked for exactly this,
and the mock caught that the inner display in portrait fell into the phone tier before any code was
written. `apple-reference-screens.md` records what Apple's own apps do in each pose, and
`device-captures.md` what 38 shipping apps do on a real device, with measurements.
