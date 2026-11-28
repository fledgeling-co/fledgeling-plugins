# Evidence

Where each rule in this skill comes from. Six kinds of source, marked in the tables:

- **[measured]** — run here, on 2026-10-10 to 2026-10-12, with Xcode 27.1 RC (27A9274) and the iOS
  27.1 iPhone Duo simulator.
- **[Apple]** — the four iPhone Duo Tech Talks, read in full from their transcripts: 111462 (bars),
  111463 (adaptive layouts), 111464 (the device's unique features: hinge, fold, camera), 111466
  (design). Plus Apple's iOS 27 design resource for point sizes.
- **[witness]** — 34 captures of Apple's own apps on iPhone Duo, read with `be-my-witness:be-my-witness`;
  the verdict and every observation are in `apple-reference-screens.md`.
- **[device]** — 321 captures of 38 shipping apps, Apple's and third-party, on a real iPhone Duo:
  313 on 2026-10-29 and 8 of the closed display on 2026-10-31. 40 `claude-sonnet-5-5` runners read
  them with `be-my-witness:be-my-witness`, three merge passes produced 34 practices, and verifiers opened the cited frames plus at least 2 more for each
  (5 confirmed as written, 29 amended, none refuted). Cited as D01 to D34 from `device-captures.md`;
  the export with every frame list is `../../docs/device-captures/2026-10-29-witness.json`.
- **[research]** — the Dossier panel of 2026-10-11 (xAI, Perplexity, Gemini members), exported with
  sources to `../../docs/deep-research/`. Each claim used here was checked against a package or a
  build; the ones that failed the check are listed at the end.
- **[owner]** — what the owner of the apps this skill was used on reported from a real iPhone Duo,
  read from 45 Claude Code sessions that invoked this skill between 11 October and 28 November 2026,
  together with the fix that cleared each report (read from the session and the app's code). For
  0.6.0, the messages sent between 04:47 and 08:47 UTC on 28 November in the 6 sessions that had run
  it, 5 of them among the 45. Dated in each row.

## Owner reports on a device (0.5.0 and 0.6.0)

| Rule | Source |
|---|---|
| Every screen-level action is a native bar item; the audit's drawn-button findings are defects, not notes | [owner] 13 reports in 5 apps, 28 Oct to 27 Nov: Scav (modal close and done, a tick for affirmative actions, camera controls), Fullframe (side-bar buttons misused, an empty side bar), Weft (a sheet's close and primary drawn in the content after `hidden-header-own-buttons` listed 5 screens as info), dAIolog investor app (PDF close, Send and Add a photo, live-voice close, new message), Tumbler (buttons, Invite, Import's Done) |
| iOS 27.1 places a native page sheet itself: centred card open flat, one page half folded, full height with Close and ✓ in the side bar closed or in portrait; forcing full-screen modals blocked it | [owner] the owner's photos of the App Store on a Duo, 28 Oct; Scav build 34 removed the forced full-screen modals |
| Gaps around a sheet come from a short form sheet with detents or a square background inside the rounded sheet | [owner] Scav, 28 Oct; fixed by page sheets and by not painting the sheet's content background |
| Closed, a sheet's close tops the side bar with the primary under it as a prominent button | [owner] Weft, 12 Nov, accepted after the drawn version was rejected; matches [device] D10, D20 (Calendar) |
| The screen's background runs under the side bar | [owner] 6 reports in 5 apps, 27 Oct to 24 Nov (Scav banner and form, dAIolog onboarding, Fullframe remote desktop, Weft, Rex Remote toolbar); matches [device] D18 |
| Force the system appearance to the app's theme | [owner] Weft, 12 Nov: a "System" theme left React Native reporting dark while iOS drew the bar light; fixed with `Appearance.setColorScheme` on every change |
| Lift composers with a window measurement on each keyboard event, 16pt above the keys | [owner] dAIolog, 18 Nov: the input cleared the keyboard "on occasion" with `KeyboardAvoidingView`; `useKeyboardLift` fixed both chat screens (commit `4eb986b51b`), and 8pt was sent back for 16pt (`aa25bc90f8`). The template's test passes 2/2 under jest-expo |
| A keyboard-avoiding container replaces its child's bottom padding, so a gap set there never shows | [owner] Scav, 28 Oct: buttons stayed on the bottom edge until the gap moved to an inner view |
| Native titles; a tab root's title hidden where tabs sit on top needs a `titleMenuProvider` | [owner] Scav, 27 to 28 Oct; Apple forum thread 812133; seen fixed on the iPad simulator |
| A band under a transparent header comes from a scroll view's automatic content insets | [owner] Weft, 12 Nov, closed display |
| `NativeTabs` `minimizeBehavior="never"` when side tabs vanish at launch | [owner] Scav builds 21–23 on 28 Oct; it stopped after builds 24–25, which also re-laid out the tab bar, so the cause is not isolated |
| SF Symbol tab icons | [owner] Scav, 27 Oct: custom tab images sat at the wrong size in the side bar |
| Every top-level screen uses the open display | [owner] Scav, 27 Oct ("a giant iPhone app"); Tumbler, 27 Nov ("a significant amount of wasted space"), fixed with a new list-and-detail hierarchy; Fullframe, 28 Oct (sidebars collapsed with no need) |
| Closed, rows push and every pushed screen has a back item | [owner] Tumbler, 27 Nov (a placeholder selection swallowed taps; confirmed fixed by a recording); Weft, 12 Nov (screens opened without history had no back item) |
| A toolbar menu that re-renders closes; make it an `Equatable` view | [owner] Rex Remote, 24 Nov; the menu then stayed open through 9 seconds of updates |
| Mock as a native app on the Duo simulator; keep the product's look | [owner] six requests for a real-app mock, 12 to 28 Nov ("Use real swift app in simulator for the mock"); dAIolog, 26 Nov ("the aesthetic … seems to have been lost in the app mocks") |
| Drive Device Hub yourself with a CGEvent click through Terminal; Maestro for in-app taps | [owner] Rex Remote, 24 Nov ("You can operate the app yourself in future"); method measured that day on Xcode 27.1, and reused for Tumbler on 27 Nov |
| Recapture only screens whose code changed | [owner] Splice and Bullettime, 12 Nov: unchanged screens tested "over and over" |
| Dense rows run the list to the fold (`listWidth="fold"`, `.fold`); one 620pt column in open portrait | [owner] Relay, 28 Nov: 320pt "too narrow, everything looks cramped"; the wider build went to TestFlight unconfirmed. `fold.test.ts` covers the option (23/23 template tests pass under jest-expo); `Fold.swift` typechecks with it |
| Opening keeps what is on screen; closing keeps the detail | [owner] Lookout, 28 Nov, stated as the rule to apply across the app's screens; the RN template's opening half is not built |
| Closed, the side bar holds back and two actions before a ••• overflow | [owner] Lookout on the Xcode 27.1 Duo simulator, 28 Nov: a third action pushed Mark Seen into the overflow |
| A tool or form screen puts its controls left and its result right when open | [owner] Tumbler, 28 Nov: the generator left the right side nearly empty ("an odd use of space") |
| An action inside a screen pushes or presents, never switches tabs | [owner] Bullettime, 28 Nov ("Measure against"); two more rows fixed in the same pass |
| Own Device Hub window when others share it; Maestro cannot tap the inner display | [owner] Tumbler and Lookout runs, 28 Nov |
| SwiftUI: tile the panes yourself at 669pt portrait; clear a default selection when compact | Tumbler's `TwoPane` and `FoldSelection`, 27 Nov; `templates/swiftui/Fold.swift` adapted from Rex Remote's and typechecked against the iOS 27.1 SDK at deployment targets 17.0 and 27.1 |

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
| Split ratio about 35/65 flat, 50/50 folded | [witness] #8 vs #14·p5 (Mail); [device] D01: flat, the list is a fixed 292–403pt column (320pt in most) in 60 captures across 21 apps; D30: a fold split appears on two-half pages (Music, Podcasts, Books, Calendar Day) |
| Split View: the bar sits on the half's outer edge, so the left app's inset is on its left | [witness] #12, #13 (Notes), #5 |
| Sheets move off the fold by themselves; PiP and alerts overlay without moving the layout | [witness] #25, #10 |
| Tabletop: content on the raised half, controls on the flat half | [Apple] 111464, 111466; [witness] #14·p6 |
| Content clears ~60–85pt from the top even with a zero top inset | [witness] #33, #34 (Settings ~83pt) |
| Device Hub "No Devices" is a stale `CoreDeviceService`; quit, `killall -9`, reopen | [measured] log line and fix; source: a Simulator engineer at WWDC labs via RocketSim |
| Open keyboard: one 951pt panel, key blocks either side of a 175pt gap on the fold, top y 391 (428 without suggestions); closed 466pt from y 374; it covers the bar's lower group and does not resize sheets | [device] D05 (52 captures, 25 apps), D09, D12, D25 |
| Modal sheets centre on the fold at 653pt (x 149–802), top y 8; some states use the left half at 459pt; the scrim dims bar buttons, not status items | [device] D04 (83 captures, 24 apps), D31, D19, D20 |
| System alerts are 319pt and centre on x 433.5; permission prompts centre on the fold; menus anchor to their trigger at about 250pt | [device] D15, D08 |
| Ordinary content crosses the fold with no gutter in Apple's own apps; gutters on the fold are a grid-level choice | [device] D07, D29; a screenshot cannot show the crease or touch, so the gutter stays a precaution |
| Rows cap near 620–700pt and reading text runs 300–570pt in wide panes | [device] D16, D17 |
| Bar items sit at x 879–927, first action y 125 open and y 175 closed, and follow the status stack down | [device] D03 (61 captures, 23 apps), D06, D28 |
| Backgrounds run under the bar, text and controls stop at x 867 open and x 382 closed | [device] D02, D18, D10, D27 |
| Companions open as a right pane; sheets about one list item open over both panes | [device] D33, D13; agrees with pattern 5 |

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
| Colours go through `systemColor`, not `PlatformColor` at module scope | [measured] 2026-10-30: a fresh `create-expo-app` (SDK 58, RN 0.88.1, `web.output: "server"`) with the 0.3.0 starter failed its Release build in `export:embed` with `PlatformColor is not a function` from `item/[id].tsx`; with `systemColor` it builds |
| Flat open display: a fixed 320pt list; book: the panes divide at the fold | [device] D01; [measured] `fold.test.ts` under bun (15/15; the flat case fails against the 0.3.0 split); a fresh SDK 58 starter on the Xcode 27.1 Duo simulator, opened flat in landscape, drew its divider at x 960px = 320.0pt with the fold inside the detail (2026-10-30). Book pose not re-captured this round |
| `FoldColumns` meets at the fold only with 120pt and 35% of the row on each side | [measured] the same capture before the rule: the starter's detail columns met at the fold and left a 128pt column; after it they share the pane. The detail-pane case in `fold.test.ts` fails with the 35% rule removed |
| Split without a fold once the pane is 900pt wide, list about 36% (320–420pt), measured from the pane so iPad's sidebar is excluded | [measured] dAIolog `lib/fold.ts` (`twoPaneForWidth`) and `DetailPaneLayout`, unit-tested in the app and in this skill's templates; the iPad pose itself was not captured in this skill's runs |
| A screen drawn in a pane sets its options through `RouteOptions`, never `Stack.Screen` | [measured] dAIolog 2026-10-12: `Stack.Screen` inside an embedded detail renamed the tab hosting it; `components/flow/RouteOptions.tsx` draws the title and `headerRight` in the pane instead |
| A pushed list that splits is exempt from the reading-column cap on pushed screens | [measured] dAIolog `app/_layout.tsx` `SPLIT_ROUTES`: capped, the pane never reached the split width |
| iPhones without a fold stay portrait while the Duo and iPad turn, decided in an `ExpoAppDelegateSubscriber` | [measured] 2026-10-12 on the Xcode 27.1 simulators: iPhone 18 Pro held portrait when rotated; the Duo's outer and inner displays turned (dAIolog `DiologFoldAppDelegateSubscriber.swift`) |
| Device Hub has no Split View or picture-in-picture control | [measured] Xcode 27.1 RC Device Hub, 2026-10-12 |

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

Seen on the Duo simulator in dAIolog on 2026-10-12: closed, open portrait, open landscape, book
with an active division (the split held with nothing in the fold band) and tabletop (the chart on the
raised half, its controls below the fold).

Not reached: Split View left and right, and PiP pinned, because Device Hub has no control for either.
`SKILL.md` asks the runner to mark these `not reached` rather than assume them.
