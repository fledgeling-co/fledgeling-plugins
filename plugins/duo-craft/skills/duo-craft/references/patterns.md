# Layout patterns for iPhone Duo in React Native

Each pattern names the template file that implements it and the failure it prevents. Every one was
built into a shipping Expo app (dAIolog's investor app) and run on the Xcode 27.1 iPhone Duo
simulator, except where marked *not yet seen running*. Patterns 13 to 16 come from 321 captures of
shipping apps on a real iPhone Duo (`device-captures.md`, cited as D01 to D34) and are marked
*observed on a device*: they say what apps do, not what a template has proved. Patterns 17 and 18,
and the parts of 6, 8, 13, 14 and 16 dated October and November 2026, come from what the owner
reported on a real Duo in 14 sessions after a run had called a screen done, and from the fixes that
cleared each report. For SwiftUI, `swiftui.md` maps every pattern.

## 1. Branch on space and on whether a fold exists — never on the model

`lib/layout.ts` → `useLayout()` returns `compact | regular | expanded` from the width the screen
actually has (window minus each side's inset, or the pane's width inside a split). `lib/fold.ts` →
`useFold()` returns `hasFold`, `posture` (`none | flat | book | tabletop`), `verticalFoldX`,
`horizontalFoldY` and `gap`.

- iPhone Duo is an iPhone to every API that names devices (`Platform.isPad` is false, `expo-device`
  says phone). A branch on the model either misses it or treats the open display as a phone.
- On a device with a fold, `regular` starts at 640pt so the open display in portrait (669pt) is
  regular, as iOS's size class says. iPad and phone tiers are unchanged.
- A fold is reported while flat too (inactive region, zero width). Decide one pane or two from
  `hasFold` once and do not switch as the hinge moves — Apple's grid example (prefer even columns
  whenever a fold exists) is the same rule. A list-and-detail divider is the exception: it moves from
  the 320pt list column to the fold when the device folds (pattern 2).
- Shipping apps re-flow one screen by the width it has: Stocks shows one news card beside its
  sidebar and two without it, Fitness one column closed and two open, Maps a leading panel open and a
  bottom sheet closed (D11).

## 2. List and detail, on the open display or a wide pane

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
- **Flat, the list is a fixed 320pt column; folded, the panes divide at the fold.** `twoPaneFor`
  returns `FLAT_LIST_WIDTH` (320pt) while `posture === 'flat'` and the fold with its gap for `book`.
  In 60 device captures across 21 apps the list or sidebar is a fixed 292–403pt column, 320pt in
  most, and the fold falls 72–183pt inside the detail (D01); Apple's own split is about 35/65 flat and
  50/50 folded (Mail, Reminders). A fold-aligned split appears only on pages of two equal halves
  (pattern 3). The divider moves when the hinge folds, which Mail does too. Versions before 0.4.0
  split at the fold in both poses to avoid that move, and the reference app still does.
- **Dense rows run the list to the fold.** 320pt suits plain rows. Rows that carry meters, figures
  or several values each need `DetailPaneLayout listWidth="fold"` (SwiftUI:
  `listColumnWidth(fold, .fold)`), which runs the list to the fold, about 476pt, while flat. The owner
  found Relay's 320pt list of agent accounts "too narrow, everything looks cramped" (28 November
  2026). In open portrait the same rows got one column capped at 620pt instead of two panes of about
  330pt each. Both changes went to TestFlight that day and the owner had not reported on them when
  this was written.
- **Opening keeps what is on screen.** The owner's rule (Lookout, 28 November 2026): opening the Duo
  shows the list on the left and whatever was on screen on the right, so a detail open on the closed
  display stays open as the right pane; a list on the closed display opens as the list beside its
  default detail; closing keeps the detail. They asked for it to be "a native function", and SwiftUI's
  `NavigationSplitView` with a selection behaves this way in both directions. `DetailPaneLayout` does
  the closing half (below). Opening with a detail pushed on top of the list does not yet return it to
  the right pane in React Native: pop the pushed detail and select its id when `split` turns true, and
  report that pose. Some screens are exceptions, such as a full-bleed viewer; decide per screen.
- **Selecting a row swaps the detail in place.** The sidebar keeps its scroll offset and shows the
  selection as a pill (Settings, Shortcuts, Journal; D22).
- **The alternative to a default selection is a labelled placeholder** ("No Event Selected",
  "Select a conversation"), centred on the detail pane rather than the fold, as Slack, Calendar,
  Siri and Termius do (D24).
- **A third column opens as an overlay.** Mail, Notes and Voice Memos slide a 280pt sidebar over the
  list with a scrim rather than resizing the panes (D26).

## 3. Two columns that meet at the fold

`components/FoldColumns.tsx` measures its row in the window. If a vertical fold falls inside it with
at least 120pt and 35% of the row on each side (`foldColumnLeftWidth` in `lib/fold.ts`), the left
column ends at `foldX - gap/2`; otherwise the columns share the row by flex (a 3:2 iPad layout stays
3:2). A row across the open display meets at the fold; a row in the detail pane beside the 320pt
list does not, because the fold sits only about 155pt into that pane and meeting there would leave a
128pt column, so its content crosses the fold as apps' content does (D07). Use it for dashboards and side-by-side sections that are not
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

## 6. Titles are the native navigation title, and clear the top

Give every screen the native title (`title` in the stack's options, with `headerLargeTitle` on tab
roots), so it sits in the same place on every tab. On 28 October 2026 the owner rejected drawn titles
that were missing in open portrait, smaller on one tab than the others, and placed differently from
tab to tab: "clearly isn't using native title / nav bar".

Two native-title failures have known causes:

- **A tab root's title is hidden on load** where the tabs sit along the top (iPad), because UIKit
  hides it once the content counts as scrolled, which a scroll view does immediately. Apple's fix is a
  `titleMenuProvider` on that navigation item (developer.apple.com/forums/thread/812133), which React
  Native Screens does not expose; one app set an empty one from a small native module on each tab
  root and its titles came back on the iPad simulator.
- **A band of the page colour shows under a transparent header** when a `ScrollView` adds automatic
  content insets for it, so the background starts one header-height down (closed display, 12 November
  2026). Turn the automatic insets off on that scroll view (`contentInsetAdjustmentBehavior="never"`)
  and pad the content yourself.

Draw a title only where a screen has no native header, such as a pane inside a split (pattern 11):
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
12–25pt before the bar's edge at x 867 in most captures (0–40pt across 23 apps), and 15–45pt before
x 382 when closed (Codex's cards end at x 366; D02, D10).

## 8. Bars go vertical only if they are native bar items

This is the rule the owner enforced most: between 28 October and 27 November 2026 they reported
buttons that should have stood in the side bar 13 times across 5 apps, more than any other defect.
The actions they named were close, Done and other affirmative actions (with a checkmark), Send, Add a
photo, New message, Invite, Import's Done, a PDF viewer's close, a live-voice screen's close, and a
camera's capture and review controls. One run that had been handed this skill drew a sheet's close
and primary buttons in the content; the audit had listed the five screens and the run filed them as
notes. Treat every screen-level action as a bar item unless it is one of the exceptions below.

- Header actions as `Stack.Toolbar.Button` / `Menu` (icon + accessibility label), not buttons drawn
  in a `View`. An item with only text stays horizontal; give every item an icon and a title. Use SF
  Symbols: `xmark` to close, `checkmark` for the affirmative action, `arrow.up.circle.fill` to send.
- Moving Send and Add a photo into the bar frees the composer to run the full width, as Mail does
  (dAIolog, 18 November 2026).
- Exceptions: a pane drawn inside a split has no bar of its own and keeps its actions in its own top
  row (pattern 11); Android keeps them inline; a full-bleed canvas puts its controls in the bar when
  there is one and over the picture when there is not (pattern 16).
- Put each action in one place. A keyboard button in the bar and another in the bottom bar was sent
  back (24 November 2026).
- The side bar standing empty on a screen with actions means those actions were drawn, not declared
  (Fullframe, 30 October 2026).
- Tabs as `NativeTabs` with an icon and a label per trigger, the icon an SF Symbol (`sf=`): the
  owner reported tab icons at the wrong size in the side bar while they were custom images
  (27 October 2026). Keep `sidebarAdaptable` off when `hasFold`. On Expo SDK 58, import from
  `expo-router/native-tabs`; `expo-router/unstable-native-tabs` still works and Metro warns that it
  is deprecated.
- If the side tabs are missing on the open display until the app is backgrounded and brought back,
  set `minimizeBehavior="never"` on `NativeTabs`. It defaults to `automatic` from iOS 26, and screens
  that count as scrolled on load minimise the tabs at launch. The owner reported this on four
  consecutive builds of one app on 28 October 2026; it stopped after a build that set
  `minimizeBehavior="never"` and re-laid out the tab bar once at launch, and which of the two cured it
  was not isolated.
- Order down the side bar is back → prominent action → other actions → tabs (Apple).
- Controls that act on one pane stay with that pane (Mail keeps the list's filter above the list).
- The system places the items: 47–48pt circles and pills centred near x 903, the first action at
  y 125 open and y 175 closed, tabs bottom-aligned (D03). Screen actions (back, close, share, more,
  Done) take the top group and keep the same first slot from screen to screen; tabs and creation
  take the bottom group (D06).
- **Closed, the side bar holds back and two actions.** A third action goes into a ••• overflow, which
  in one app swallowed the prominent Mark Seen (Lookout on the Duo simulator, 28 November 2026). Rank
  each screen's actions, keep the primary one visible, and show a contextual action only while it
  applies: Send appeared only while the person was typing feedback, and Mark Seen took its place
  otherwise.
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

## 13. The keyboard splits around the fold — *observed on a device; the lift is built*

Open, the system keyboard is one 951pt panel holding two key blocks (x 85–388 and 563–866) with a
175pt gap centred on the fold. Its top is at y 391 with a suggestion row and y 428 without, so it
covers up to 42% of the height. Closed, it is one 466pt piece from y 374 (D05). It runs under both panes
and the bar, and nothing in the app has to draw it.

- Keep the focused field or composer 16pt above the keyboard's top, read from keyboard events
  rather than a constant. ChatGPT, Claude, Messages and Shortcuts lift theirs 8–20pt (D09); the owner
  sent 8pt back as "very close to the keyboard" and kept 16pt (18 November 2026).
- Lift with `lib/keyboard.ts` → `useKeyboardLift()`: put `ref` on the composer's container and
  `paddingBottom: lift` on it. It measures the container in the window on every keyboard event.
  `KeyboardAvoidingView` measures from the view's last layout, which goes stale in a pane on the open
  Duo, in a sheet and after a fold, so the owner saw the input move clear "on occasion" and otherwise
  sit under the keys; the hook fixed both chat screens in that app. While the keyboard is up, drop the
  composer's home-indicator inset, or it floats too high.
- A keyboard-avoiding container also replaces its child's bottom padding with the keyboard height,
  which is 0 with no keyboard up, so a bottom gap set there never shows. Put the gap on an inner view.
  That is why one app's buttons still sat on the bottom edge of the open display after a fix
  (28 October 2026).
- The keyboard covers a form sheet without resizing it, so Calendar's New Event sheet hides its
  lower fields behind the keys. Make sheet content a `ScrollView` (D09).
- Float a keyboard accessory (a format toolbar, a search pill) 8–12pt above the keys, 44–48pt tall,
  ending before the bar: x 866 open, x 381 closed (D25).
- No capture here measured what `react-native-keyboard-controller` reports for the split panel.
  Check the reported frame on the Duo simulator before relying on it.

## 14. Sheets, alerts and menus are native, and their size is the system's — *observed on a device*

- **Let iOS place the sheet.** The owner photographed the App Store's sheets on a Duo (28 October
  2026), and iOS 27.1 does all of this by itself for a native sheet whose buttons are bar items:
  - open flat, a centred card with Close and ✓ inside it, the tabs still in the side bar;
  - half folded, the same sheet on one page;
  - closed or in portrait, full height, with Close and ✓ in the side bar.

  Present with the page sheet (`presentation: 'modal'`) and give it a native header with Close
  (`xmark`) and the affirmative action (`checkmark`) as bar items. One app forced every modal full
  screen and pushed its buttons into the bar by hand, which blocked the system's placement; the owner
  sent it back the same day. A sheet on one page while the Duo is half folded is that placement, not
  a bug to correct with a width.
- **Every modal has a way to close.** "There's often no close button on modals or popup screens"
  (27 October 2026).
- **No gaps around the sheet.** Two causes, both reported as "gaps between the modal and screen
  behind it": a short `formSheet` with detents, which floats with the app showing around it (use the
  page sheet), and a square background painted on the sheet's content, which shows in the corners of
  iOS 26's rounded sheet (let the sheet's own background or `contentStyle` colour it).
- **Sizes.** Open, a modal sheet is centred on the fold: usually 653pt wide (x 149–802), top y 8,
  stopping 65pt short of the bar; partial-height sheets start at y 82 (D04, 83 captures in 24 apps).
  In some states the same sheet sits in the left half, 459pt wide (Calendar, Claude; D31). Lay its
  content out with flex so it holds at 459pt and 653pt, and never give a modal a width or a left
  offset.
- **Scrim.** A native modal's scrim dims the bar's buttons and tab pill and leaves the status items
  bright (D19). An overlay drawn inside the app's own tree cannot reach the bar.
- **Sheet header.** A 48pt round close or back button at the sheet's leading edge, the title centred
  on the fold, the action at the trailing edge, in a row at y 24–72; some apps put close at the
  trailing edge (D20). Closed, a sheet spans x 8–458 and its buttons go one of three ways: into the
  bar from y 175 (Calendar), a close button kept inside the sheet, or none, leaving the bar's back
  button to close it (Codex; D10, D20). Take Calendar's way, which the owner accepted after rejecting
  drawn buttons: close at the top of the side bar, the primary action under it as a prominent button,
  any secondary action below that (12 November 2026).
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
  pane (D14). Closed, floating pills such as a composer centre on the 0–382pt content column (x 191),
  not the window (Codex, D14). Take the container's width from `onLayout`, never from half the window.

## 16. Backgrounds run under the bar; text and controls stop before it — *observed on a device*

- Maps, artwork, hero images, separators and scroll indicators run under the trailing bar; text and
  controls stop at x 867 open and x 382 closed. Pad a horizontal carousel's content by the right
  inset so its last card scrolls clear of the bar's buttons (D18, 33 captures in 19 apps).
- **The screen's own colour runs under the bar too.** The owner reported a strip beside the side bar
  in a different colour from the screen 6 times in 5 apps between 27 October and 24 November 2026: an
  onboarding background, a banner, a remote desktop, a form in open portrait, a toolbar, and dark
  content beside a white bar. Put the background on the outermost view of the screen with no padding,
  and the per-side inset padding on the view inside it. A layout that pads the whole screen by 84pt
  for the bar leaves exactly this strip.
- **Force the system's appearance to the app's theme.** In the dark-beside-white case the app had
  a "System" theme beside its own light and dark ones; once it had forced an appearance, React Native
  reported dark while iOS drew the bar light (12 November 2026). The fix calls
  `Appearance.setColorScheme('light' | 'dark')` on every theme change and dropped the "System"
  choice, so the bar, status items and sheets follow the app (SwiftUI: `.preferredColorScheme`).
- **Full-bleed media hides its chrome on a tap.** Closed, a photo or video viewer with no way to hide
  its buttons, or that stops short of the screen, was sent back; its caption and controls overlay the
  picture rather than shrinking it (28 October 2026).
- The status items sit on a blur capsule over anything drawn beneath them, and text there is cut
  (Siri, D27). They stay in every view except full-bleed canvases: Calculator, a remote desktop, a
  camera.
- A camera view runs its preview to x 951 with the status bar hidden, puts its round controls in
  the bar from y 24, and keeps the shutter in the bar or left of x 867 (Measure, Translate, a
  document scanner; D34). Floating controls over a picture use the same glass as the bar's buttons
  (28 October 2026).

## 17. Every top-level screen uses the open display — *from owner reports*

Decide, for each tab and each pushed screen that is a list, what it does at 951×669 and 669×951:
list and detail (pattern 2), columns (pattern 3), or a capped column with something useful beside
it. A phone layout stretched or centred across the open display was sent back as "a giant iPhone app"
(27 October 2026) and "a significant amount of wasted space when the duo is open" (27 November 2026),
and the fix in the second app was a new hierarchy (Items, Watchtower, Generator, Settings, each a
list beside its detail open and a push stack closed), not wider cards. Two more reports in the same
family: a split with a wide list and a narrow detail where the detail held the content, and a photo
grid kept to one column in open landscape. A tool or form screen splits too: Tumbler's password
generator kept its options and result together on the left and left the right side nearly empty ("an
odd use of space", 28 November 2026); the fix put the options in the left column and the generated
value, large, with its strength and recent values, on the right. Write the decision per screen in the
plan, so a reviewer can see each screen was considered.

## 18. Closed, the app is a phone app with a side bar — *from owner reports*

- **Rows push, with the animation.** A list built for the split must still push when closed; in one
  SwiftUI app tapping a row highlighted it and pushed nothing (27 November 2026, `swiftui.md`). Check
  the push with a recording, because a still capture cannot show it.
- **Every pushed screen has a back item,** including one opened with nothing behind it, from a sheet
  or a deep link: give those a Back item that returns to their tab (12 November 2026).
- **An action inside a screen pushes or presents; it never switches tabs.** Bullettime's "Measure
  against" row jumped to another tab, and the owner asked for a push or a modal instead (28 November
  2026); the run found two more rows doing the same and fixed all three.
- **No band at the top** (pattern 6) and **no strip beside the bar** (pattern 16).

## Design before code

Build the mock as a native app on the Duo simulator, with direction from `design-craft:design-craft`
and `ux-craft:ux-craft`, and show the app as it is today beside each proposed state. The side bar,
native sheets, the split keyboard and sheet placement are drawn by iOS, so only a native mock shows
them. The first mocks were HTML at Apple's point sizes, and one caught the inner display in portrait
falling into the phone tier before any code was written; from 12 November 2026 the owner asked for
the mock as a real app instead, in six sessions. `apple-reference-screens.md` records what Apple's own
apps do in each pose, and `device-captures.md` what 38 shipping apps do on a real device, with
measurements.
