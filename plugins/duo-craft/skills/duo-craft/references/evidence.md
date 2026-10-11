# Evidence

Where each rule in this skill comes from. Four kinds of source, marked in the tables:

- **[measured]** — run here, on 2026-10-10 to 2026-10-12, with Xcode 27.1 RC (27A9274) and the iOS
  27.1 iPhone Duo simulator.
- **[Apple]** — the four iPhone Duo Tech Talks, read in full from their transcripts: 111462 (bars),
  111463 (adaptive layouts), 111464 (the device's unique features: hinge, fold, camera), 111466
  (design). Plus Apple's iOS 27 design resource for point sizes.
- **[witness]** — 34 captures of Apple's own apps on iPhone Duo, read with `be-my-witness:be-my-witness`;
  the verdict and every observation are in `apple-reference-screens.md`.
- **[research]** — the Dossier panel of 2026-10-11 (xAI, Perplexity, Gemini members), exported with
  sources to `../../docs/deep-research/`. Each claim used here was checked against a package or a
  build; the ones that failed the check are listed at the end.

## The platform

| Rule | Source |
|---|---|
| Outer 466×678pt, inner 951×669 / 669×951pt, fold at 475.5pt in both orientations; 84pt trailing bar; inner portrait 84pt top, 95pt bottom | [Apple] design resource; [measured] window sizes on the simulator; matches `mirzaaghazadeh/iphone-duo-skills` `reference/device-facts.md` |
| `reservedRegions(kind:options:)` and `UIHingeInteraction` exist only in the iOS 27.1 SDK; 27.0 and 27.1 share Swift 6.4, so `#if compiler` cannot gate them | [measured] compile against both SDKs |
| A region's frame already includes its margins; `.includeInactive` reports the fold while flat | [Apple] 111463; [measured] the module reads a zero-width inactive division when flat |
| Prefer even columns whenever a fold exists, and do not re-layout as the hinge moves | [Apple] 111463 grid example |
| Hinge angle drives effects; reset outside `partiallyOpen`; give hingeless devices the end state; honour Reduce Motion | [Apple] 111464 |
| Bar items go vertical only as system bar items with a symbol; text-only items stay horizontal; order is back → prominent → others → tabs | [Apple] 111462; [witness] #19 Mail `Select` stays horizontal |
| Only the detail column's bar goes vertical; a list keeps its own controls | [Apple] 111462; [witness] #8, #9, #15, #21 |
| Split ratio about 35/65 flat, 50/50 folded | [witness] #8 vs #14·p5 (Mail) |
| Split View: the bar sits on the half's outer edge, so the left app's inset is on its left | [witness] #12, #13 (Notes), #5 |
| Sheets move off the fold by themselves; PiP and alerts overlay without moving the layout | [witness] #25, #10 |
| Tabletop: content on the raised half, controls on the flat half | [Apple] 111464, 111466; [witness] #14·p6 |
| Content clears ~60–85pt from the top even with a zero top inset | [witness] #33, #34 (Settings ~83pt) |
| Device Hub "No Devices" is a stale `CoreDeviceService`; quit, `killall -9`, reopen | [measured] log line and fix; source: a Simulator engineer at WWDC labs via RocketSim |

## React Native and Expo

| Rule | Source |
|---|---|
| iPhone Duo reads as a phone: `Platform.isPad` false, `expo-device` phone | [measured] |
| Expo SDK ≤57 built with the iOS 27 SDK crashes at launch (`_UIApplicationEvaluateRuntimeIssueForNoSceneLifecycleAdoption`); SDK 58 prebuild writes a scene delegate | [measured] fresh `create-expo-app` (SDK 57, RN 0.86) crashed on every launch; dAIolog on SDK 58 ran. [research] the xAI and Gemini reports predicted the crash; Perplexity named scene geometry only |
| `expo-build-properties` `ios.enableSceneSupport` fixes SDK 57 | [measured] same fresh app, `prebuild --clean`: Info.plist names `EXExpoAppSceneDelegate`, AppDelegate conforms to `ExpoReactNativeFactoryProvider`, no `UIWindow(frame:)`; Release build launched with the two-pane split, Share and tabs in the side bar (2026-10-12). Found by the eval-3 no-skill run; the skill's own earlier plugin also ran, and was dropped for the official flag |
| `NativeTabs` and `Stack.Toolbar` items reach the side bar; a JS header does not | [measured] in dAIolog and the starter; the starter's toolbar reached the side column only once the tab had its own Stack with a transparent header while split |
| `sidebarAdaptable` off when a fold exists | [measured] dAIolog: the sidebar took most of the left pane |
| Pane-scoped width (`PaneWidthContext`) so the list lays out as a phone | [measured] dAIolog Following, Inbox, Discover |
| Default the detail pane to the first item; keep the chosen item open on close | [measured] owner review of dAIolog; Microsoft's dual-screen guidance; `detailPaneLayout.test.tsx` fails without it |
| Lazy `require` of embedded detail screens | [measured] static import failed six dAIolog test suites on a native dependency |
| Title top 59 + 8pt when the top inset is 0 | [measured] owner rejected 8pt and then 20pt on the Duo (commits `0d3cdeb5fc`, `c6329e4367`) |
| Pushed screens pad each side for its own inset | [measured] content ran to within 2pt of the back button; owner flagged it on every screen (commit `6513385fe0`) |
| A starter with no `/` route opens on Expo Router's 404 | [measured] 2026-10-12, fixed with `app/index.tsx` |

## Libraries

Read by unpacking each npm tarball and reading the iOS source on 2026-10-11; stars read 2026-10-12.
Details in `libraries.md`.

| Claim | Result |
|---|---|
| `react-native-nitro-hinge` provides the fold | Its fold path is compiled out unless `HINGE_IOS_27_1_SDK` is set; `hingeAngle` always returns `null`; 3 GitHub stars. Not used as a dependency, at the user's direction and on this reading |
| `expo-display-features` is an Expo module | 404 on npm; an unmerged PR. [research] claim failed |
| Fold width is 40pt | Not confirmed: the flat fold reports zero width; the folded band was not measured. [research] claim unverified, so no rule depends on it |
| `mirzaaghazadeh/iphone-duo-skills` covers React Native | Guidance only (per-edge insets, `useWindowDimensions`, width breakpoints, native-module shape); no module, components or scene fix. Used to cross-check device facts |

## Not yet seen running

Built and unit-tested, not yet captured on the simulator: tabletop (`FoldRows`), book pose with an
active division, Split View left and right, PiP pinned. `SKILL.md` asks the runner to mark these
`not reached` rather than assume them.
