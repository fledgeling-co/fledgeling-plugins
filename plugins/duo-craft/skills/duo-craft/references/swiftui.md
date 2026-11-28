# iPhone Duo in SwiftUI

The rules in `patterns.md` hold for a SwiftUI app; only the APIs change. This file maps them, and
records three traps that only SwiftUI hit. Its sources are six SwiftUI apps built for the Duo with
this skill between 17 and 28 November 2026 (FoldedIn, Rex Remote, Tumbler, Bullettime, Splice and
Tether's Duo UI). Rex Remote and Tumbler ran on the Xcode 27.1 Duo simulator and through TestFlight on
the owner's Duo; the facts below come from those two unless another app is named.

## Fold reading

Copy `templates/swiftui/Fold.swift` into the app target. It gives `FoldState` (`hasFold`, `fold`,
`vertical`, `folded`, `book`, `tabletop`), a `FoldReader` to place once at the root with
`.background(FoldReader(state: $fold))`, the `\.fold` environment value, `tier(width:fold:)` and
`listColumnWidth(_:)`. It reads the same `reservedRegions(kind: .division, options: .includeInactive)`
and `UIHingeInteraction` as the React Native module, so it needs the iOS 27.1 SDK. It typechecks
against that SDK at deployment targets 17.0 and 27.1.

Branch on `tier` and `hasFold`, never on `UIDevice.current.userInterfaceIdiom`: the Duo reports
`.phone` (pattern 1).

## List and detail (pattern 2)

- **Landscape, open:** `NavigationSplitView` with
  `.navigationSplitViewColumnWidth(listColumnWidth(fold))`. The system keeps the list clear of the
  side bar.
- **Portrait, open (669pt):** the size class is regular, and `NavigationSplitView` draws its list as
  an overlay at that width. Tile the panes yourself with an `HStack` of a `NavigationStack` list at
  `listColumnWidth(fold)`, a `Divider`, and the detail (Tumbler, 27 November).
- **Closed or a Split View half:** let `NavigationSplitView` collapse to a stack, which pushes.
- **Selection across the fold:** open, default the selection to the first row so the detail is never
  blank. Closed, a default selection pushes a detail the person never chose, so clear it on the
  change to compact unless they picked the row themselves (`.onChange(of: horizontalSizeClass,
  initial: true)`).
- **Closed, rows must push.** In Tumbler, every list was bound to a placeholder selection outside a
  `NavigationSplitView`; closed, tapping a row highlighted it and pushed nothing. Use the split view's
  own selection, or `NavigationLink(value:)` in a `NavigationStack`, and check the push on the closed
  display with a recording, because a still capture cannot show a missing animation.

## Bar items (pattern 8)

Actions are toolbar items with a symbol: `ToolbarItem(placement: .cancellationAction)` for Close or
Cancel, `.confirmationAction` with `Button("Save", systemImage: "checkmark")` for the affirmative
action, `.primaryAction` and `.secondaryAction` for the rest, `.topBarTrailing` for a `Menu`. Closed,
Tumbler's 24 screens showed these in the side bar with no further work. A `Button` placed in the view
body stays where it is drawn.

**A toolbar `Menu` closes by itself when its view re-renders.** Rex Remote's ••• menu on the closed
display kept refreshing while an agent updated the screen, so the owner could not select its items.
Making the menu its own `Equatable` view that compares only the values it shows
(`PaneMenu(...).equatable()`) kept it open through 9 seconds of updates.

## Sheets (pattern 14)

`.sheet` with the content in a `NavigationStack` whose toolbar carries `.cancellationAction` and
`.confirmationAction` items. iOS places the sheet in each pose itself (pattern 14 has what it does).
Give a sheet no fixed frame.

## Backgrounds, insets and the keyboard (patterns 7, 13, 16)

- Put the screen's colour on the container with `.background(color.ignoresSafeArea())`; SwiftUI
  keeps text and controls inside the safe area by default. Give cells and the screen one ground in
  both appearances: in Rex Remote, light mode showed no background on the cells, the content read as
  over-indented, and one ground with an 8pt text inset fixed it (24 November).
- Put a composer or a key toolbar in `.safeAreaInset(edge: .bottom, spacing: 0)` on the screen, so it
  rides the keyboard and the keyboard rising never rebuilds the field. Float it on the system glass
  material, as bar items are, and let a key toolbar span the keyboard's full width: Rex Remote's left
  an empty gap beside it on the open Duo until it did.
- Read side insets per edge (`GeometryReader`'s `safeAreaInsets.leading` / `.trailing`) for anything
  you pad by hand; Split View flips which side carries the bar.

## Titles (pattern 6)

`.navigationTitle` with `.toolbarTitleDisplayMode(.large)` on tab roots, so every tab's title sits in
the same place. Draw a title yourself only in a pane that has no navigation bar of its own.

## Building, capturing and driving

Build with `DEVELOPER_DIR` set to Xcode 27.1 and drive the simulator as `simulator.md` describes. The
audit script reads JavaScript and TypeScript only, so for a SwiftUI app the review list in `SKILL.md`
step 5 is the check.
