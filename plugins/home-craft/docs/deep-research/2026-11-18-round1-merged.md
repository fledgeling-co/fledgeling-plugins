# CarPlay and HomeView apps on iOS 26 and iOS 27: merged research (18 November 2026)

This merges two Dossier research runs that answered the same brief:

- **[C]** Codex CLI, run `dr_6fef7a2690355180`. Its final report cites 48 unique URLs; one, Apple's CarPlay request form, is login-gated.
- **[G]** Grok Build, run `dr_88706aa1c1a2da04`. It cites 47 sources: 39 opened, 5 were bot-blocked, and 3 that Dossier flagged as malformed (all 9to5Mac) returned HTTP 200 when re-fetched by hand.

**[C+G]** means both runs made the claim. Most claims rest on Apple's own pages, so two runs citing the same Apple page count as one source, not two. A claim tagged with one run is single-sourced: uncorroborated, not wrong. **[synth]** marks a conclusion drawn here by combining the two reports. Three other panel members produced no evidence: Antigravity's quota was exhausted, Claude Code returned 1,459 characters citing nothing, and Claude through Dossier's own loop got no usable source from any worker. The paid Gemini Deep Research run never started, because the API key returned 401.

The brief assumed one SwiftUI codebase and one React Native/Expo codebase. That assumption shapes the recommendations below; the platform facts do not depend on it.

## What to do

1. **Apply for the one CarPlay category that is the app's real primary function.** Since iOS 26.3 an app may hold only one CarPlay entitlement; the one allowed pairing is EV charging with fueling. [C+G] [CarPlay Developer Guide, 13 Oct 2026, pp. 14–15](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf) [audio entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio)
2. **The app itself appears on HomeView only if it holds the audio or video entitlement.** It runs on the paired iPhone and HomeView displays it. Every other category gets no HomeView presence beyond a widget. [C+G] [developer.apple.com/carplay](https://developer.apple.com/carplay/) [Guide p. 14, footnote *2](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)
3. **For any app that isn't a media app, the HomeView route is a `.systemSmall` widget.** It needs no CarPlay entitlement. [C+G] [Widgets HIG](https://developer.apple.com/design/human-interface-guidelines/widgets)
4. **Do not build a HomeView conversational app yet.** The "Conversational Apps" evidence is a beta string, not an API. [C+G]
5. **Keep CarPlay scene registration and the audio lifecycle in native code in both codebases.** For Expo, that means a development build with a config plugin and a small Swift module, rather than relying on `react-native-carplay`. [C+G]
6. **Test on a USB-connected iPhone with CarPlay Simulator in Xcode 27's Device Hub, then on at least one real head unit.** HomeView has no simulator, so only a HomeView device proves HomeView behaviour. [C+G] [Testing your app in CarPlay Simulator](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator)

## The five premises, checked

| Premise | Verdict | Backing |
|---|---|---|
| HomeView runs "HomeView Software 27.2" | **Confirmed.** Build 24V526, released 12 November 2026. | [C] [Apple release listing](https://developer.apple.com/news/releases/?id=11122026a); [G] [MacRumors, 12 Nov](https://www.macrumors.com/2026/11/12/apple-homeview-software-27-2-24v526/). Two independent sources. |
| It is a tvOS 27.2 derivative | **Developer-observed, not Apple-stated.** Steve Troughton-Smith's VM inspection found tvOS 27.2 with device family 8; Apple's pages say only "HomeView software." | [C] [Troughton-Smith, 30 Oct](https://mastodon.social/@stroughtonsmith/117532557440780934); [G] [The Apple Wiki](https://theapplewiki.com/wiki/HomeView_Software), [AppleInsider, 2 Nov](https://appleinsider.com/articles/26/11/02/homeview-os-is-more-locked-down-for-developers-than-we-thought). Both runs trace back to the same original observation. |
| No SDK, App Store, simulator or design kit | **Confirmed, with one correction:** design guidance does exist. The Widgets HIG has a HomeView section. There is still no kit, device frame or HomeView HIG for projected apps. Apple developer support (DTS) told a developer on 13 Oct to keep the iPhone as the Xcode destination. | [C+G] [Widgets HIG](https://developer.apple.com/design/human-interface-guidelines/widgets); [G] [forums thread 850841](https://developer.apple.com/forums/thread/850841) |
| Apps reach HomeView via a CarPlay bridge (audio/video), plus widgets, Live Activities and HomeKit/Matter | **Media and widgets confirmed.** Developer Program License Agreement §6.4.2 says the app runs "on a paired iOS device." **Third-party Live Activities on HomeView are not documented:** Apple's examples are its own, and the ActivityKit page mentions CarPlay, not HomeView. **HomeKit/Matter are home-hub product features, not an app route.** An iPad pairing cannot supply third-party audio, video or remote widgets. | [C+G] [CarPlay page](https://developer.apple.com/carplay/), [agreement](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/); iPad limit [G] only, [Support 148407](https://support.apple.com/en-us/148407) |
| iOS 27.3 beta adds a "Conversational Apps" category | **Partly wrong.** The CarPlay voice-based conversation category already exists, since iOS 26.4. What iOS 27.3 beta adds is a `ConversationalApps` string on HomeView's bridge, alongside unfinished two-way audio. It is not in the 27.3 release notes. "PebblePlay" is a leaker's name for the bridge, not an Apple API. | [C] [ipsw-diffs, PebblePlayCore](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md) (inspectable diff, Medium); [G] [9to5Mac, 5 Nov](https://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/) (leaker report, Low). The diff is the stronger evidence that the string exists; neither source shows the feature working. |

HomeView facts single-sourced to [G]: $299, on sale 13 November in the US and seven other countries, not the EU; it needs an iPhone on iOS 27.2 or an iPad on iPadOS 27.2. [Newsroom, 13 Nov](https://www.apple.com/newsroom/2026/11/apple-homeview-available-today/)

## Capability matrix

The source for every row is the October 2026 CarPlay Developer Guide, pp. 10–15, which both runs read. Entitlement keys are `com.apple.developer.carplay-<suffix>`. A template the entitlement does not allow throws at runtime. [G] Guide p. 15

Abbreviations: **B** = list, grid, tab bar, action sheet, alert · **N** = Now Playing · **C** = contact · **I** = information · **P** = point of interest · **M** = map · **S** = search · **V** = voice control.

| Category (suffix) | iOS 26.x | iOS 27.0–27.3 beta | HomeView |
|---|---|---|---|
| Audio (`audio`) | B+N | B+N, plus S and V; MiniPlayer | **Yes**, no code changes, iPhone only |
| Video (`video`) | No entitlement. Parked AirPlay video is a separate vehicle feature | From 27.0: B+N+S+V. Parked only; hidden in cars without video support | **Yes**, same as audio |
| Voice-based conversation (`voice-based-conversation`) | From 26.4: B+I+P+V. No Now Playing | Same | Not enabled; beta string only |
| Communication (`communication`) | B+C+I+N | Adds V | No |
| Navigation (`maps`) | Map base view plus S, C, V, B. Cluster/HUD; route sharing from 26.4 | Adds map panels | No |
| EV charging (`charging`) | B+I+P. Combinable with fueling | Adds S and V | No |
| Fueling (`fueling`) | B+I+P | Adds S and V | No |
| Parking (`parking`) | B+I+P | Adds S and V | No |
| Quick food ordering (`quick-ordering`) | B+I+P | Adds V. No search | No |
| Driving task (`driving-task`) | B+I+P; V from 26.4 | Same | No |
| Public safety (`public-safety`) | B+C+I+N, plus P? and S? (see below) | Adds V | No |
| Widgets (no entitlement) | `.systemSmall`, Ultra included | Same | Home Screen and Modular face |
| Live Activities (no entitlement) | `ActivityFamily.small`, non-interactive | Same | Shown, but third-party coverage undocumented |

The runs disagree on two cells. For **public safety**, [C] lists P and S on iOS 26, while [G] omits P and says S arrives with iOS 27. For **navigation**, [C] includes the information template and [G] omits it. Check Guide pp. 14–15 before relying on either cell.

Both runs found 11 categories. [G]'s summary says "twelve" but its own matrix lists 11, so the summary count is wrong.

**CarPlay Ultra** adds no third-party SDK, template or entitlement. The same framework draws the app; navigation apps keep the cluster and HUD APIs. [C+G] [WWDC25 session 216](https://developer.apple.com/videos/play/wwdc2025/216/), [CarPlay page](https://developer.apple.com/carplay/)

### The audio-plus-video contradiction

WWDC26 session 212 (8 June 2026) told media apps to ship both the audio and video entitlements. The October 2026 Guide and the current entitlement pages forbid combining them. [C+G] Both runs recommend following the later October rule. If an audio app also plays video, it should support AirPlay video, which needs no video entitlement. [G] Get written confirmation from Apple before the architecture depends on holding both. [C] [WWDC26 212](https://developer.apple.com/videos/play/wwdc2026/212/) [video entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video)

## UI and UX rules

| Rule | Backing |
|---|---|
| Put primary content in the upper half and keep the screen scannable. Supply @2x and @3x art for light and dark. Common canvases are 800×480, 960×540, 1280×720 and 1920×720. | [C+G] [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay) |
| Work with the iPhone locked, and never tell the driver to pick it up. Files under `NSFileProtectionComplete`/`CompleteUnlessOpen` and when-unlocked keychain items are unavailable. | [C+G] HIG; Guide pp. 29–30 |
| Let the user start audio. Activate the session when playback is ready, so the car radio keeps playing until the user picks your audio. | [C+G] HIG, Audio |
| Read `contentStyle` on the scene and update on `contentStyleDidChange`. Check colours in a real car. | [C+G] HIG, Color |
| **Liquid Glass:** the CarPlay HIG doesn't mention it. Templates are system-drawn, so you don't apply materials yourself. iOS 26 gives `CPMapTemplate` buttons the glass treatment. On HomeView, clear widgets get the Liquid Glass material. | [C] WWDC25 216; [G] Widgets HIG |
| **Lists:** read `maximumItemCount` and `maximumSectionCount` at runtime. Some cars show only 12 items. An Apple engineer gave 500 as the app-side cap in Dec 2025 and said list images are not lazy-loaded. | [C+G] Guide p. 19; 500 cap [G] [thread 798894](https://developer.apple.com/forums/thread/798894) |
| **Tabs:** read `maximumTabCount`. It is currently 4 for audio and 5 for other categories; don't hard-code either. The Now Playing button may disappear above 4 tabs. | [C+G] Guide p. 26 |
| **Depth, root included:** 5 for audio, communication, EV charging, parking, public safety and navigation; 3 for fueling and voice conversation; for driving task and quick food ordering, 2 through 26.3 and 3 from 26.4. The Guide gives no depth for video. | [C+G] Guide p. 15; video gap [C] |
| **Voice control:** show the template the whole time the mic is open. From 26.4 it can carry 2 action buttons; from iOS 27 it can overlay other templates, including a map. Only navigation and conversational apps may record. | [C+G] Guide pp. 8, 27, 30 |
| **Conversational apps:** launch into voice, answer by speaking (not with text or images), and hold the audio session only while voice is in use. | [C+G] Guide p. 8 |
| **Siri and App Intents** are a voice path in their own right. The conversational entitlement is what unlocks templates beyond the system UI; App Intents does not grant that eligibility. | [C+G]; [G] [thread 831674](https://developer.apple.com/forums/thread/831674) |
| **HomeView widgets:** the shared Modular face holds up to 4 small widgets that every member of the household can see, so check what each one discloses. Below an ambient-light threshold the Modular face renders widgets in red monochrome. | 4-widget limit and household privacy [C]; red night mode [C+G]; [Widgets HIG](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView) |
| **HomeView's display:** 7 inches, 1088×1088, 220 ppi. It's a product spec, not a layout guide; Apple publishes no safe areas or type sizes for projected apps on a square screen. | [G] [specs](https://www.apple.com/apple-homeview/specs/) |
| **Observed on HomeView:** tabs become a menu, and the app depends on the phone being nearby. | [C] [Troughton-Smith, 1 Nov](https://mastodon.social/@stroughtonsmith/117542694509125589), developer-observed |

**What App Review and the entitlement addendum reject** [C+G], from the Guide's category rules, pp. 5–8:
- no games or social features
- no message or email bodies on screen
- no lyrics in audio apps
- no step that sends the driver back to the phone
- driving-task apps that refresh the UI more often than every 10 seconds or points of interest more often than every 60 seconds, or that are really store finders
- general retail presented as quick food ordering
- a category that doesn't match the app's actual function

The App Review Guidelines have no numbered CarPlay section. [G] The general sections still apply: §2.1, §2.5.1, §2.5.4, §2.5.11, §2.5.14 (recording consent), §2.5.17 (Matter), §§5.1.1–5.1.2, and §5.2. §5.1.2(i) requires explicit consent before sharing personal data with a third-party AI. [C] [Guidelines](https://developer.apple.com/app-store/review/guidelines/)

## Code

**Scene setup** [C+G]: list the phone scene and a `CPTemplateApplicationScene` under `CPTemplateApplicationSceneSessionRoleApplication` in `UIApplicationSceneManifest`, with `UIApplicationSupportsMultipleScenes` set to true. CarPlay can launch the app before any phone scene exists. Set the root template in `templateApplicationScene(_:didConnect:)`. Only navigation apps get a drawable `CPWindow`. [CPTemplateApplicationScene](https://developer.apple.com/documentation/carplay/cptemplateapplicationscene)

**Audio** [C+G]: Now Playing is `CPNowPlayingTemplate.shared`. Configure it at connect, because the car's Now Playing button can open it before your list exists. Publish metadata through `MPNowPlayingInfoCenter` and handle transport through `MPRemoteCommandCenter`, independently of templates. Since iOS 27, `allowsMiniPlayer` defaults to true. [G] Disconnecting the CarPlay scene should not stop playback on the phone. [C]

**Video** [C+G]: there is no video template. Play through AVKit/AVFoundation with AirPlay enabled, and set `CPPlaybackConfiguration` (iOS 26.4) per playable item, using `.video` to ask for the system player and `.audio` for Now Playing. `CPSessionConfiguration.supportsVideoPlayback` reports what the session can do and doesn't change mid-session; it does not tell you the car is parked. [C, from an Apple engineer in [thread 831710](https://developer.apple.com/forums/thread/831710)] Playback-speed control for CarPlay video is unavailable. [C]

**Voice conversation**: present `CPVoiceControlTemplate` while capturing, with an iOS 26.4 availability gate. [C] cites WWDC26 for `.playAndRecord`, `.default` mode and no mixing; [G]'s skeleton uses `.voiceChat` mode without citing anything, so prefer [C]'s sourced setting. The two skeletons also differ in structure: [C] sets a root list and presents the voice template on top of it, while [G] sets the voice template as the root. Historically the voice template could only be presented, never set as root. Neither run confirms that iOS 27 changed this, so treat [G]'s structure as unverified. [synth]

**Widgets and Live Activities** [C+G]: use `.systemSmall`. Widgets with App Intent buttons work on touchscreens; on non-touch screens they don't respond to input. For Live Activities, add `NSSupportsLiveActivities` and `.supplementalActivityFamilies([.small])`. To keep a widget out of the car, use `.disfavoredLocations([.carPlay], for: [.systemSmall])`. `WidgetLocation` has a `carPlay` case and no `homeView` case. [G] infers that you therefore can't allow a widget on HomeView while blocking it in the car, or the reverse. That inference is single-sourced and was not tested.

**HomeKit/Matter** [C+G]: add the HomeKit capability and `NSHomeKitUsageDescription` in the iOS app. Integrating accessories does not put the app on HomeView.

**Skeletons.** Both runs wrote one audio and one voice skeleton. Neither was compiled or run on a device. [C]'s versions are more complete: a singleton playback service, remote-command targets, and error paths that update the list row. They are in `dr_6fef7a2690355180`, section 3. [G]'s shorter versions are in `dr_88706aa1c1a2da04`, section 3. Both use `try?`, which swallows audio-session failures, and production code should surface those errors instead.

**React Native and Expo** [C+G]:
- `birkir/react-native-carplay` states "No Expo support due to Scenes" and a minimum of iOS 14. Its README covers none of `CPPlaybackConfiguration`, the iOS 27 MiniPlayer or voice action buttons. [G] Issues #236 (9 Jul 2025, black screen with Expo) and #238 (3 Sep 2025, templates missing on RN 0.81.1) show integration risk. Both predate iOS 26/27, so they are not evidence of a regression on those SDKs. [C]
- [G] reports that React Native 0.88's iOS template sets `UIApplicationSupportsMultipleScenes` to false. Pasting that manifest unchanged would drop the CarPlay scene. The source is a third-party porting blog, not React Native's own repo, so check the actual template diff.
- The workable setup: a development build (Expo Go can't carry entitlements or a scene delegate), a config plugin that *merges* the CarPlay scene role, entitlement and background modes, manual signing, and a Swift module that owns the scene delegate and starts without waiting for the JS runtime. [C+G] [Expo dev builds](https://docs.expo.dev/develop/development-builds/introduction/), [config plugins](https://docs.expo.dev/config-plugins/introduction/)
- Neither run found a test of the library against both iOS 26 and 27. Run a compatibility spike against your exact RN, Expo and library versions before adopting it. [C]

## Entitlements and deployment

- **Request** at developer.apple.com/contact/carplay as the account holder, and accept the CarPlay Entitlement Addendum. After the grant: enable the capability on the App ID, regenerate the profiles, turn **off** automatic signing, and add the Xcode capability so the entitlements file gets the boolean key. With automatic signing or a missing entitlements file, the app won't install into CarPlay. [C+G] [Preparing your iOS app for CarPlay development](https://developer.apple.com/documentation/carplay/preparing-your-ios-app-for-carplay-development)
- **Two apps means two App IDs and two requests.** The SwiftUI app and the Expo app don't share a grant. [G]
- **Timing:** Apple publishes no SLA. [C+G] Reported waits in 2026 [Low predictive value]:
  - audio approved in days [C, Reddit, Oct 2026]
  - driving task from about a day to several weeks, with one case over a year [C]
  - voice conversation granted in about a month [G, [thread 823974](https://developer.apple.com/forums/thread/823974)]
  - a video request undecided after 15 days [G]
- **The icon ships to everyone.** Once the entitlement is in a build, every user sees the CarPlay icon, TestFlight testers included. You can't show it to a subset of users, so add the entitlement only when the car UI is finished. [G] Guide p. 13
- **HomeView needs nothing extra.** There is no HomeView review queue, opt-in or Info.plist key. Presence follows from the audio or video entitlement plus agreement §6.4. [C+G] This is an absence finding: nothing was found, which is not proof that nothing exists.
- **Disclose CarPlay API use** in the App Store Connect review notes, per addendum §4. [G]

## Test matrix before submission

There are two different simulators. CarPlay Simulator (from Xcode's Additional Tools) is a Mac app that acts as the car screen while a real iPhone drives it; Xcode 27 builds it into Device Hub over USB. The Xcode 27.2 release notes exclude the iOS Simulator from this path. [C+G] [Xcode 27.2 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes)

| Lane | Cases | Pass condition |
|---|---|---|
| XCTest, app-side | Template selection per category, list and depth limits, voice states, playback command routing, cancellation | Assertions, including the failure paths |
| Device Hub + CarPlay Simulator, USB iPhone | Cold launch with the phone locked; light/dark; @2x/@3x; a 12-item list; tab count; depth cap; video app in a non-video configuration | App launches locked; video app hidden when the car lacks video; nothing throws at a limit |
| iOS 26.0–26.3 device | Existing categories; 26.4+ APIs gated off; widgets and Live Activities | No unavailable-API crash |
| iOS 26.4+ device | Voice conversation, new depths, voice action buttons | Voice starts, stops, survives an interruption, releases the session |
| iOS 27.x device (and 27.3 beta, logged separately) | MiniPlayer, `CPPlaybackConfiguration`, search and voice in more categories | `.audio` opens Now Playing; `.video` opens the system player only where the car supports video |
| Wireless aftermarket head unit | The same flows, with the phone cabled to the Mac; touch and rotary/non-touch input | Every flow completes without touching the phone |
| One production car (OEM) | Steering controls, Siri, calls, FM coexistence, reconnect | Interruptions and resumption behave correctly |
| CarPlay Ultra car | Only if you claim cluster/HUD or navigation behaviour | Same templates; route sharing works |
| TestFlight build | Fresh install, upgrade, distribution signing, release JS bundle, offline launch | The distributed build appears and works on the head units |
| HomeView on 27.2 + iPhone on 27.2 | Media launch, the tabs-as-menu adaptation, remote commands, phone locked or away; the widget on the shared Modular face, night red, guests | The app appears and works; the widget shows nothing it shouldn't to other household members; an iPad pairing shows no third-party app |

XCUITest: neither run found any Apple statement that it can drive system-rendered CarPlay templates. Keep XCTest for the phone-side code that feeds the templates. [C+G] Maestro was asked for CarPlay support on 29 Sep 2026, and its maintainers made no commitment. [C] [issue #3641](https://github.com/mobile-dev-inc/Maestro/issues/3641) Without a HomeView device you can't test the square canvas or the red night mode. [G]

## Submission checklist

1. One category that matches the primary task, with any audio/video question settled in writing with Apple. [C+G]
2. Entitlement requested early. There is no clock on approval. [C+G]
3. Capability on the App ID, manual profiles, boolean key present in the **signed archive**. [C+G]
4. Scene manifest merged so the phone scene survives, with multiple scenes enabled; on Expo, done by the config plugin. [C+G]
5. Root template set in `didConnect`; Now Playing configured at connect; voice template visible whenever the mic is open. [C+G]
6. Templates, depth, tab count and the 12-item car limit kept to what the category allows; no message bodies, lyrics or pick-up-your-phone prompts. [C+G]
7. `CPPlaybackConfiguration` set on every playable row; AirPlay video supported if the audio app plays video. [C+G]
8. `.systemSmall` widget with a removable background, checked for what it shows on the shared HomeView face; `.small` Live Activity. [C+G]
9. Microphone, speech, HomeKit and background-audio declarations present; AI data-sharing consent in place. [C]
10. Test-matrix lanes passed on the distributed TestFlight build. HomeView behaviour claimed only from a real HomeView device. [C+G]
11. CarPlay use disclosed in the review notes, with credentials, media samples and the category justification. [C+G]

## Roadmap

| Date | Event | Status |
|---|---|---|
| June 2025 | WWDC25: CarPlay widgets, Live Activities, Liquid Glass appearance | Announced [C+G] |
| 18 Feb 2026 | Voice-based conversation category appears in the iOS 26.4 beta guide | Announced [G] |
| 8 Jun 2026 | WWDC26: video apps, voice control in every category, MiniPlayer, map panels | Announced [C+G] |
| 13 Oct 2026 | HomeView announced; agreement §§6.4.1–6.4.2 | Announced [C+G] |
| 31 Oct–1 Nov 2026 | Security-camera configuration found in firmware; Troughton-Smith's reconstructed developer UI and critique | Developer-observed [C] |
| 3 Nov 2026 | Siri AI developer preview in the 27.3 betas, App Store submissions "in the spring". This is App Intents on iPhone, not a CarPlay category | Announced [G] |
| 5 Nov 2026 | `ConversationalApps` string on the HomeView bridge in the 27.3 beta | Beta code only [C+G] |
| 12 Nov 2026 | A HomeView Siri lock-control update planned for the following month | Reported [G] |

Developers' open asks: a HomeView build target (DTS answered "keep iPhone") [G]; an entitlement SLA and escalation path [C+G]; CarPlay UI automation [C]; and a way for conversational apps to show an active conversation in the instrument cluster (a CallKit attempt on iOS 27.2 beta changed nothing) [G]. Apple has given no date for a HomeView SDK, a HomeView App Store, conversational apps on HomeView, or a camera API. [C+G]

## Still open

- Whether disfavouring a widget for `.carPlay` also hides it on HomeView. [G]
- Template lists for the public safety and navigation rows, where the two runs disagree.
- Whether an app can legally hold both the audio and video entitlements. Apple's own documents contradict each other.
- Whether React Native 0.88's template really disables multiple scenes, which so far rests on one blog.
- Whether either Swift skeleton compiles against the iOS 27 SDK, which nobody has tested.
- Whether `CPVoiceControlTemplate` can be a root template on iOS 27.

Re-read the CarPlay Developer Guide PDF after iOS 27.3 ships. It is the document that withdrew the dual-entitlement advice, and the one most likely to add conversational apps to the HomeView footnote. [G]
