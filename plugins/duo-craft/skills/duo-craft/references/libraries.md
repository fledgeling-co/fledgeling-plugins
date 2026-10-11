# Libraries: what exists, and why this skill ships its own module

Read 2026-10-11 by unpacking each package from npm and reading its iOS source, not its README.
Every one of them is weeks old. Adoption figures are GitHub stars on 2026-10-12.

| Package | Stars | Fold region | Hinge | What reading the source found |
|---|---|---|---|---|
| bundled `duo-fold` (`templates/modules/duo-fold`) | — (yours) | `reservedRegions(kind: .division, options: .includeInactive)` on a window overlay, re-read on layout and hinge change | status + angle via `UIHingeInteraction`, as events | Ran on the iPhone Duo simulator in a shipping app and in a fresh SDK 57 starter. Needs the 27.1 SDK and fails at compile without it, so a fold signal cannot silently vanish |
| `react-native-nitro-hinge` (Gautham495) | 3 | `reservedRegions` with `.includeInactive` | `hingeAngle` always returns `null` | **The fold path sits behind `#if … HINGE_IOS_27_1_SDK`, off by default.** It builds clean and its fold path is absent from the binary unless the podspec gains that compilation condition (read from source; not run on a device here). Needs `react-native-nitro-modules` |
| `@garrettmacmac/react-native-duo` | 0 | Obj-C `reservedRegionsOfKind:` behind `@available(iOS 27.1, *)` | yes | `0.1.0-beta.0`, published 2026-10-03 |
| `react-native-arrangement-view` (thiagobrez) | 33 | via `ArrangementView` | hinge observation | Wraps Apple's `ArrangementView` (RN ≥ 0.83) |
| `react-native-dualscreeninfo` | — | — | — | Surface Duo (Android) only. Prior art |
| `expo-display-features` | — | — | — | **Not on npm** (404). One research report cited it as a module; it is an unmerged PR |

## Which to use

**Use the bundled module.** It is about 150 lines of Swift the app owns, so there is no
dependency to vet, nothing to wait on upstream, and nothing a maintainer can abandon. It ran on the
Duo simulator in two apps, and the hooks above it (`useFold`, `useTwoPane`) are tested.

**Do not add a third-party fold library as a dependency.** None has the adoption a production app
should lean on — the fold library most likely to be found, `react-native-nitro-hinge`, has 3 stars
and compiles its fold path out by default — and a fold source that quietly returns nothing produces an app that
looks finished on every simulator except the one that matters. When a user asks for one by name,
read its native source the way this table did, say what you found, and offer the bundled module.
Their source is still worth reading as prior art; nitro-hinge's Android path is the only one of
these covering Android foldables.

**`react-native-arrangement-view` is the exception worth knowing**, not a default: it wraps a
system view rather than reimplementing fold geometry, so its failure surface is small. Consider it
only for a genuine split/overlay pair that maps onto Apple's arrangement rules (player and
transcript, canvas and tools), and vendor it into `modules/` rather than depending on the package
at 33 stars. Apple: never inside a `ScrollView`/`List`, never wrapping a split view. For list →
detail, the bundled `DetailPaneLayout` keeps routing, deep links and the push fallback in JS where
the app's navigation already lives.

Whatever the source, layout code reads the fold through one hook, so swapping the source later is a
one-file change.

## Guidance repos

`mirzaaghazadeh/iphone-duo-skills` (150 stars, 2026-10-11) is a set of eleven platform-neutral
skills with a device-facts sheet and an API index, kept current by a CI job that watches Apple's
docs. Its React Native skill is guidance only: per-edge insets, `useWindowDimensions`, width
breakpoints, and the shape a native module should take. It ships no module, no layout components
and no Expo scene fix. Use its `reference/device-facts.md` and `reference/api-index.md` to check a
number or an API name; this skill supplies the code.

## Navigation and bars

- `expo-router/unstable-native-tabs` (`NativeTabs`) and `Stack.Toolbar` items render as real
  `UITabBarController` / `UINavigationItem` bar items, which is what lets iPhone Duo stand them in
  the side bar. A JS tab bar (`@react-navigation/bottom-tabs` with a custom `tabBar`) or a header
  drawn in a `View` cannot move there.
- `NativeTabs` `sidebarAdaptable` turns the tabs into an iPad sidebar in a wide window. On a device
  with a fold, keep it off: a sidebar takes most of the open display's left half, which the list
  needs in a two-pane split.
- `expo-router/unstable-split-view` (alpha, iOS, SDK 55+) is a native `UISplitViewController`.
  Not yet exercised on the Duo simulator in this skill's evidence; prefer `DetailPaneLayout` until
  it has been.

## Expo SDK and the scene lifecycle

Built against the iOS 27 SDK, an app with no scene delegate is stopped at launch
(`_UIApplicationEvaluateRuntimeIssueForNoSceneLifecycleAdoption`, EXC_BREAKPOINT). Measured:

| Expo SDK | Scene delegate after prebuild | Built with Xcode 27.1, on the Duo simulator |
|---|---|---|
| 58 (RN 0.88) | written by prebuild | runs |
| 57 (RN 0.86), today's `create-expo-app` | none | **crashes on every launch** |
| 57 (expo 57.0.27) + `expo-build-properties` 57.0.22 with `ios.enableSceneSupport` | written by prebuild (`EXExpoAppSceneDelegate`) | runs, two-pane split and side-bar items correct |

`ios.enableSceneSupport` is Expo's own SDK 57 opt-in (expo/fyi `ios-scene-lifecycle.md`). It needs
`expo` 57.0.23 or later, the first patch shipping `ExpoAppSceneDelegate`, and throws at prebuild
below it. `install_templates.py` turns it on and adds the package when it finds SDK 57. On SDK 58 it
is a no-op with a warning, so remove it when upgrading.

An earlier draft of this skill shipped its own config plugin making the same three edits. It ran,
but a no-skill eval run found the official flag, so the skill uses that instead: one less file the
app owns, and Expo maintains it.
