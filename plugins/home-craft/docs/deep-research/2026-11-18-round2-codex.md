## Executive Summary

- (High Confidence) **Choose the CarPlay category that matches the app’s primary function.** Apple’s current audio entitlement permits audio-only **and audiovisual** content; the video entitlement permits audiovisual content but excludes audio-only content. Both enable HomeView. **Apple-documented; references undated, checked 18 November 2026.** [Audio](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md), [video](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md). [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md)
- (High Confidence) **Do not submit combined audio/video entitlements without written Apple clarification.** <CONFLICTING_EVIDENCE>[WWDC26 recommends both; the October guide and current canonical entitlement references prohibit combining them.]</CONFLICTING_EVIDENCE> **Apple-documented conflict, unresolved.** [WWDC26](https://developer.apple.com/videos/play/wwdc2026/212/). [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/)
- (High Confidence) **HomeView’s documented media-app route runs through a paired iPhone.** Apple requires iOS 27.2 or later; an iPad companion does not enable third-party audio/video apps. **Apple-documented, 12 November 2026.** [Compatibility requirements](https://support.apple.com/en-us/127246). [support.apple.com](https://support.apple.com/en-us/127246)
- (Medium Confidence) <INFERENCE from="Apple’s documented media/widget routes and public SDK/design catalogs">**For a non-media app, build a useful small widget and applicable App Intents/HomeKit integrations.** No public general-purpose native HomeView app target, SDK, simulator or dedicated design kit was located. Do not make a native HomeView port a committed release dependency.</INFERENCE> [Design resources](https://developer.apple.com/design/resources/), [Widget HIG](https://developer.apple.com/design/human-interface-guidelines/widgets). [developer.apple.com](https://developer.apple.com/design/resources/) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets)
- (High Confidence) **Use a physical iPhone for current CarPlay acceptance testing.** Device Hub’s CarPlay Simulator is a receiver for a USB-connected iPhone; current Xcode release notes explicitly say iOS Simulator is unsupported for CarPlay. **Apple-documented; release-note publication date unstated.** [Xcode release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes.md). [developer.apple.com](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes.md)
- (Low Confidence) **HomeView chatbot and security-camera extensions remain roadmap signals, not shipping developer contracts.** The reported beta strings were not independently reproduced, and no corresponding Apple API announcement was verified. **Rumoured, reported 2 and 5 November 2026.** [Conversational apps](https://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/), [camera features](https://9to5mac.com/2026/11/02/homeview-could-double-as-a-homekit-security-camera-shows-code/). [9to5mac.com](https://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/) [9to5mac.com](https://9to5mac.com/2026/11/02/homeview-could-double-as-a-homekit-security-camera-shows-code/)

## Detailed Findings

### 1. Platform surface: which categories, entitlements, templates and HomeView routes exist?

**Notation:** **A/H** means Apple-documented, High confidence in the cited text; **D/M** means developer-observed, Medium confidence; **R/L** means rumoured, Low confidence. Undated references were checked on 18 November 2026; that is an access date, not a publication date.

#### Verification of the four premises

| Premise | Finding |
|---|---|
| HomeView runs Software 27.2, build 24V526, derived from tvOS | **Partly confirmed, A/H.** Apple lists that version/build on **12 November 2026**. <INSUFFICIENT_EVIDENCE>[No Apple primary source establishing its precise tvOS ancestry was verified.]</INSUFFICIENT_EVIDENCE> [Release listing](https://developer.apple.com/news/releases/?id=11122026a). [developer.apple.com](https://developer.apple.com/news/releases/?id=11122026a) |
| No SDK, App Store, simulator or design kit at launch | **Bounded absence, Medium confidence.** No public native development/distribution route or dedicated kit was located. This is not an explicit Apple statement that none exists internally or will ship later. The broader claim “no design guidance” is incorrect: Apple added HomeView guidance to the Widget HIG on **13 October 2026**. [developer.apple.com](https://developer.apple.com/design/resources/) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Third-party apps arrive through paired-iPhone CarPlay audio/video entitlements, plus small widgets | **Confirmed as documented launch routes, A/H.** Agreement **§6.4.1** covers widgets; **§6.4.2** covers eligible CarPlay apps running on a paired iOS device. Entitlement references identify audio/video; the HIG identifies system-small widgets. This does not enumerate every HomeView system integration. [developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| iOS 27.3 beta adds `ConversationalApps` to the bridge | **Reported, R/L.** Ben Lovejoy’s **5 November 2026** report attributes this to pdfu. The original X post was inaccessible and the binaries were not independently inspected. The report also contains an inconsistent “26.3” reference alongside “27.3.” It establishes a reported discovery, not eligibility or activation. [9to5mac.com](https://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/) |

Apple separately confirms HomeView’s retail availability beginning **13 November 2026 — A/H**. [Launch announcement](https://www.apple.com/newsroom/2026/11/apple-homeview-available-today/). [apple.com](https://www.apple.com/newsroom/2026/11/apple-homeview-available-today/)

#### Capability matrix

**A/H; Apple’s guide dated 13 October 2026.** Entitlement suffixes below follow `com.apple.developer.carplay-`.

Template notation:

- **B:** `CPActionSheetTemplate`, `CPAlertTemplate`, `CPGridTemplate`, `CPListTemplate`, `CPTabBarTemplate`
- **C:** `CPContactTemplate`; **I:** `CPInformationTemplate`; **M:** `CPMapTemplate`
- **N:** `CPNowPlayingTemplate`; **P:** `CPPointOfInterestTemplate`
- **S:** `CPSearchTemplate`; **V:** `CPVoiceControlTemplate`

**d** is maximum pushed hierarchy including root; **?** means undocumented. Template eligibility does not establish root/modal/tab eligibility.

| Category / entitlement suffix | iOS 26.x | iOS 27.x through documented 27.3-beta surface | HomeView |
|---|---|---|---|
| Audio / `audio` | B+N; d5 | B+N+S+V; d5 | Eligible media interface |
| Communication / `communication` | B+C+I+N; d5 | B+C+I+N+V; d5 | No documented category route |
| Navigation / `maps` | B+C+I+M+S+V; d5 | Same; additional map panels; d5 | No documented category route |
| EV charging / `charging` | B+I+P; d5 | B+I+P+S+V; d5 | No documented category route |
| Parking / `parking` | B+I+P; d5 | B+I+P+S+V; d5 | No documented category route |
| Fueling / `fueling` | B+I+P; d3 | B+I+P+S+V; d3 | No documented category route |
| Quick food ordering / `quick-ordering` | B+I+P; d2→d3 at 26.4 | B+I+P+V; d3 | No documented category route |
| Driving task / `driving-task` | B+I+P; V from 26.4; d2→d3 at 26.4 | B+I+P+V; d3 | No documented category route |
| Public safety / `public-safety` | B+C+I+N+P; d5 | B+C+I+N+P+S+V; d5 | No documented category route |
| Voice conversation / `voice-based-conversation` | From 26.4: B+I+P+V; d3 | B+I+P+V; d3 | R/L beta report only |
| Video / `video` | No video-app category | B+N+S+V; d? | Eligible media interface |

[Apple category/template matrix](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf). [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)

**HomeView qualification — A/H:** eligible audio/video apps use their existing interface without required modifications. <MISSING_DATA>[Apple did not provide a separate HomeView per-template compatibility/depth table in the sources inspected; full behavioral parity should not be assumed.]</MISSING_DATA> [Developer overview](https://developer.apple.com/carplay/). [developer.apple.com](https://developer.apple.com/carplay/)

**Mechanism — D/M, 1 November 2026:** Steve Troughton-Smith observed templates reconstructed on HomeView and a tab template becoming a menu. That observation supports testing the actual destination rather than assuming vehicle screenshots represent HomeView. [First-hand account](https://mastodon.social/@stroughtonsmith/117542694509125589). [mastodon.social](https://mastodon.social/@stroughtonsmith/117542694509125589)

**CarPlay Ultra — A/H, WWDC25/26:** third-party apps continue using the CarPlay framework. Ultra does not provide arbitrary SwiftUI access to vehicle controls or instrument-cluster layouts. Navigation apps can supply supported guidance metadata; widgets and Live Activities participate. [WWDC25](https://developer.apple.com/videos/play/wwdc2025/216/), [developer overview](https://developer.apple.com/carplay/). [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/) [developer.apple.com](https://developer.apple.com/carplay/)

### 2. UI and UX: what rules should the team implement?

The following rules are **Apple-documented, High confidence**. HIG references are live and undated except the Widget HIG’s HomeView update.

| Rule | Implementation consequence | HIG/source |
|---|---|---|
| Glanceable, minimal interaction | Prioritize useful actions and short content; let templates handle geometry and vehicle input. | [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay.md). [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) |
| Locked/inaccessible iPhone support | Complete setup beforehand; report destination errors without asking the driver to manipulate the phone. | [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay.md). [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) |
| Platform appearance | Existing templates automatically adopt iOS 26’s updated appearance. <INFERENCE from="Automatic template appearance described at WWDC25">Use system Liquid Glass chrome rather than reproducing it in custom overlays.</INFERENCE> | [WWDC25](https://developer.apple.com/videos/play/wwdc2025/216/). [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/) |
| Day/night legibility | Test light/dark appearances, sunlight, glare and night brightness in a vehicle; provide appropriate artwork variants. | [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay.md). [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) |
| Distance-viewing widgets | Use focused content, larger typography and removable backgrounds. Preserve useful passive content when interaction is unavailable. | [Widget HIG](https://developer.apple.com/design/human-interface-guidelines/widgets), [CarPlay widget guidance](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md). [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) [developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md) |
| Shared HomeView Modular face | It can contain **four widgets** from different household members on **one household face**; personal Home Screens are separate. | Widget HIG, **13 October 2026**. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| HomeView widget appearance | Support removed backgrounds, full-color/accented appearances and monochromatic red low-light rendering on the Modular face. | [Widget HIG](https://developer.apple.com/design/human-interface-guidelines/widgets). [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Live Activities | Use them for bounded ongoing events; supply the standard presentations and a useful small-family layout for CarPlay. | [Live Activity HIG](https://developer.apple.com/design/human-interface-guidelines/live-activities.md). [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/live-activities.md) |

**Template limits — A/H:** runtime limits govern; the guide describes restricted lists of **12 items**, currently **4 audio tabs versus 5 for other categories**, and recent/favorite quick orders limited to **12 entries**. [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf) Read `CPListTemplate.maximumItemCount` and `CPTabBarTemplate.maximumTabCount` instead of hard-coding universal values. [List limit](https://developer.apple.com/documentation/carplay/cplisttemplate/maximumitemcount.md), [tab limit](https://developer.apple.com/documentation/carplay/cptabbartemplate/maximumtabcount.md). [developer.apple.com](https://developer.apple.com/documentation/carplay/cplisttemplate/maximumitemcount.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cptabbartemplate/maximumtabcount.md)

**Voice — A/H, WWDC26:** show voice-state UI while voice services operate; use audible status feedback. Apple specifies `.playAndRecord`, `.default`, and no mixing, and describes an iOS 27 voice-overlay presentation. [Session](https://developer.apple.com/videos/play/wwdc2026/212/). [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/)

**Review-sensitive patterns — A/H:** category misuse, message bodies, lyrics, social/game experiences, unrelated settings and inappropriate template content violate the guide; conversational answers should not become visual transcripts. [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf) Recording requires consent and an indication; sharing personal data with third-party AI requires disclosure and permission under **§§2.5.14 and 5.1.2(i)**. [Review Guidelines](https://developer.apple.com/app-store/review/guidelines/). [developer.apple.com](https://developer.apple.com/app-store/review/guidelines/)

<INFERENCE from="Widget HIG’s shared Modular face">Choose household-safe widget defaults. Face recognition protecting personal screens does not make a deliberately shared widget private.</INFERENCE>

### 3. Code: how should an existing SwiftUI app integrate these surfaces?

**A/H:** retain the SwiftUI app lifecycle. Use `UIApplicationDelegateAdaptor` for process bootstrap and a separate, main-actor `CPTemplateApplicationSceneDelegate` for CarPlay. [Adaptor](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md), [scene delegate](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md). [developer.apple.com](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md)

<INFERENCE from="Apple’s independent scene lifecycle">Initialize shared playback/conversation services before either scene connects. A CarPlay-only cold launch must not depend on the phone view’s `onAppear`. Merge the CarPlay scene role into the existing manifest while preserving SwiftUI’s phone configuration.</INFERENCE>

Complete original skeletons are supplied here:

- [AudioExample.swift](/tmp/carplay-homeview-research-20261118/AudioExample.swift)
- [VoiceExample.swift](/tmp/carplay-homeview-research-20261118/VoiceExample.swift)
- [CarPlay scene-manifest fragment](/tmp/carplay-homeview-research-20261118/CarPlaySceneManifest.plist)

Build the examples separately: each defines its own app entry point and scene delegate. The audio example expects a bundled `Example.m4a`; the voice example requires the existing app’s real `ConversationBackend`.

**Verification limitation:** these files were reviewed against SDK headers, but **were not compiler-verified**. The installed iOS 27.1 SDK was identified; build admission refused execution before Swift ran. The plist passed `plutil -lint`. No physical receiver, HomeView or distribution test ran. [Verification record](/tmp/carplay-homeview-research-20261118/verification.json). `UNVERIFIED (unusable citation URL)`

#### Shared integration

```swift
@main
struct ExistingApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self)
    private var appDelegate

    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

Merge this under `UIApplicationSceneManifest → UISceneConfigurations`:

```xml
<key>CPTemplateApplicationSceneSessionRoleApplication</key>
<array>
    <dict>
        <key>UISceneClassName</key>
        <string>CPTemplateApplicationScene</string>
        <key>UISceneConfigurationName</key>
        <string>CarPlay</string>
        <key>UISceneDelegateClassName</key>
        <string>$(PRODUCT_MODULE_NAME).CarPlaySceneDelegate</string>
    </dict>
</array>
```

#### Audio skeleton

The complete linked file owns an `AVPlayer`, installs remote-command handlers once, publishes metadata, installs a list root and handles presentation errors. Its central path is:

```swift
@MainActor
func play(url: URL, title: String) throws {
    let session = AVAudioSession.sharedInstance()
    try session.setCategory(.playback, mode: .default)
    try session.setActive(true)

    player.replaceCurrentItem(with: AVPlayerItem(url: url))
    MPNowPlayingInfoCenter.default().nowPlayingInfo = [
        MPMediaItemPropertyTitle: title,
        MPNowPlayingInfoPropertyPlaybackRate: 1.0
    ]
    player.play()
}
```

After selection, push the shared `CPNowPlayingTemplate`. **A/H:** its content and transport behavior come from the media frameworks; actual background playback requires the Audio/AirPlay background mode. [Now Playing](https://developer.apple.com/documentation/carplay/cpnowplayingtemplate.md), [media configuration](https://developer.apple.com/documentation/avfoundation/configuring-your-app-for-media-playback.md). [developer.apple.com](https://developer.apple.com/documentation/carplay/cpnowplayingtemplate.md) [developer.apple.com](https://developer.apple.com/documentation/avfoundation/configuring-your-app-for-media-playback.md)

#### Voice-based conversational skeleton

The complete linked file installs a list root, immediately presents the voice template, checks existing microphone consent and starts the injected backend only after presentation succeeds.

```swift
@MainActor
protocol ConversationBackend: AnyObject {
    func start() throws
    func stop()
}
```

The voice presentation uses:

```swift
let listening = CPVoiceControlState(
    identifier: "listening",
    titleVariants: ["Listening"],
    image: nil,
    repeats: false
)

let voice = CPVoiceControlTemplate(
    voiceControlStates: [listening]
)
```

The owning main-actor service activates audio only after successful presentation:

```swift
let session = AVAudioSession.sharedInstance()
try session.setCategory(
    .playAndRecord,
    mode: .default,
    options: []
)
try session.setActive(true)
try backend.start()
```

On End, interruption, scene resignation or disconnect:

```swift
backend.stop()
try session.setActive(
    false,
    options: .notifyOthersOnDeactivation
)
```

**A/H:** `CPVoiceControlTemplate` supplies state UI, not recognition, microphone capture or an assistant backend. [Voice template](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate.md). [developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate.md)

<INFERENCE from="Voice UI, recording-consent and scene-lifecycle contracts">Connect listening/processing/speaking states, Speech authorization where applicable, backend failures and cancellation to the real engine. The example’s list-plus-modal arrangement avoids depending on unresolved voice-root eligibility; it is not proof that voice roots are forbidden.</INFERENCE>

#### Video and AVKit

**A/H:** `CPPlaybackConfiguration` is available from **iOS 26.4**, earlier than the video-app category. Its initializer uses `CMTime`:

```swift
row.playbackConfiguration = CPPlaybackConfiguration(
    preferredPresentation: .video,
    playbackAction: .play,
    elapsedTime: .zero,
    duration: CMTime(
        seconds: durationSeconds,
        preferredTimescale: 600
    )
)
```

[Playback configuration](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration.md). [developer.apple.com](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration.md)

**A/H:** support AirPlay video through AVFoundation/AVKit. `AVPlayerViewController` provides standard AirPlay playback; it is not a `CPTemplate` to push onto the CarPlay stack. [AVKit](https://developer.apple.com/documentation/avkit/avplayerviewcontroller.md). [developer.apple.com](https://developer.apple.com/documentation/avkit/avplayerviewcontroller.md)

**Important API distinction — A/H:** use `CPSessionConfiguration.supportsVideoPlayback`. It remains constant during a session even when vehicle policy suppresses video and leaves audio playing. Do not expect it to become false when the vehicle moves. [Property contract](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback.md). [developer.apple.com](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback.md)

#### Widgets, activities, intents and home integration

**A/H:** relevant configuration shapes are:

```swift
.supportedFamilies([.systemSmall])

// Only when unsuitable for CarPlay:
.disfavoredLocations([.carPlay], for: [.systemSmall])

// Separately, on ActivityConfiguration:
.supplementalActivityFamilies([.small])
```

[Widget contexts](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md), [activity layouts](https://developer.apple.com/documentation/activitykit/creating-custom-views-for-live-activities.md). [developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md) [developer.apple.com](https://developer.apple.com/documentation/activitykit/creating-custom-views-for-live-activities.md)

**A/H:** expose real actions through `AppIntent.perform()` and appropriate entities/shortcuts. App Intents do not grant a CarPlay app category. [AppIntent](https://developer.apple.com/documentation/appintents/appintent.md). [developer.apple.com](https://developer.apple.com/documentation/appintents/appintent.md)

**A/H:** use HomeKit for authorized home/accessory control, including its capability and usage description; use MatterSupport for onboarding and Matter for commissioning/control. These are accessory integrations, not a general HomeView app runtime. [HomeKit](https://developer.apple.com/documentation/homekit.md), [MatterSupport](https://developer.apple.com/documentation/mattersupport.md). [developer.apple.com](https://developer.apple.com/documentation/homekit.md) [developer.apple.com](https://developer.apple.com/documentation/mattersupport.md)

#### Swift strict concurrency

**A/H:** CarPlay scene/UI APIs are main-actor isolated. Remote-command callbacks synchronously return `MPRemoteCommandHandlerStatus`; retain their tokens and remove handlers when ownership ends. [Scene isolation](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md), [remote-command API](https://developer.apple.com/documentation/mediaplayer/mpremotecommand/addtarget%28handler%3A%29.md). [developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md) [developer.apple.com](https://developer.apple.com/documentation/mediaplayer/mpremotecommand/addtarget(handler:).md)

<INFERENCE from="MainActor UI APIs and synchronous remote callbacks">Keep templates on the main actor and expensive work in service actors. A callback may enqueue `Task { @MainActor in … }`; returning success then acknowledges acceptance, not completed execution. Avoid unchecked actor assumptions and blocking hops to the main thread.</INFERENCE>

### 4. Entitlements and deployment: how should the app be approved and submitted?

**A/H:** request the genuine category through Apple’s [CarPlay entitlement process](https://developer.apple.com/carplay/). A Boolean entitlement in a local file does not constitute approval. [developer.apple.com](https://developer.apple.com/carplay/)

**Current signing correction — A/H:** approved managed CarPlay capabilities support **automatic signing**. Enable the capability on the App ID and target, refresh profiles and inspect the signed product. Apple warns that grants may cover only particular distribution types. The guide’s manual-signing recipe is not the only supported workflow. [Managed capabilities](https://developer.apple.com/help/account/reference/provisioning-with-managed-capabilities). [developer.apple.com](https://developer.apple.com/help/account/reference/provisioning-with-managed-capabilities)

**Approval timelines:** <MISSING_DATA>[No Apple SLA or reliable contemporary request-to-approval dataset was verified. Older anecdotes and unsourced “weeks” estimates cannot establish a release schedule.]</MISSING_DATA>

<INFERENCE from="Approval is required before managed-capability provisioning">File the entitlement request before promising a release date, while preparing implementation and review material in parallel.</INFERENCE>

**Review requirements — A/H:** relevant sections include completeness **2.1**, feature disclosure **2.3.1**, public/intended APIs **2.5.1**, background execution **2.5.4**, Siri/Shortcuts **2.5.11**, recording **2.5.14**, widgets **2.5.16**, Matter pairing **2.5.17**, and privacy **5.1.1–5.1.2**. [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/). [developer.apple.com](https://developer.apple.com/app-store/review/guidelines/)

<MISSING_DATA>[The authenticated current CarPlay Entitlement Addendum was not retrieved. Review the version attached to the team’s grant; no additional clauses are asserted here.]</MISSING_DATA>

**HomeView-specific approval — Medium confidence:** no separate native submission track, entitlement application or Info.plist opt-in key was located. The agreement permits the documented iPhone routes; it does not authorize disguising an unrelated app as media. [Developer agreement](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/). [developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)

**Submission checklist — proposed release gate:**

- Approved category matches the primary product function; development and distribution products contain the correct grants.
- CarPlay-only cold launch, merged manifest and locked-phone access work.
- Actual media/conversation engine, remote controls, interruptions, cancellation and disconnect pass.
- Destination errors work without phone manipulation.
- HomeView household privacy and supported appearances pass on hardware.
- Review account, backend/media access, reproducible steps and privacy disclosures are supplied.
- TestFlight-installed behavior passes the applicable matrix.
- Archive and metadata describe only verified features.

<INFERENCE from="Review Guidelines, managed-capability restrictions and destination lifecycle contracts">These are proposed acceptance criteria, not evidence that an application has passed them.</INFERENCE>

### 5. Testing before publishing: what is the concrete test matrix?

**A/H:** current Device Hub CarPlay testing requires a USB-connected physical iPhone. The standalone receiver remains available through Additional Tools for Xcode. A legacy simulated external-display menu is not evidence of a supported current path. [Xcode notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes.md). [developer.apple.com](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes.md)

**D/M, June 2026:** a developer reported no public CLI/AX route for driving either CarPlay surface; Apple requested an enhancement report. This does not prove all automation is impossible. [Forum exchange](https://developer.apple.com/forums/thread/831782). [developer.apple.com](https://developer.apple.com/forums/thread/831782)

<INFERENCE from="System-rendered UI and reported automation limitations">Use XCTest/Swift Testing for app-owned state, catalogue, commands and coordinators; XCUITest for the phone UI. Treat receiver interaction/pixel checks and physical controls as a separate acceptance layer unless your harness demonstrates reliable access.</INFERENCE>

**The matrix below is proposed and was not executed.**

| Lane | Configuration | Required observable result |
|---|---|---|
| Version boundaries | Supported earliest/latest releases; specifically either side of category/API changes; stable and beta lanes separated | Correct availability gating and template selection |
| Cold launch | Terminated app; receiver launches before phone scene | Root and services initialize without phone-view dependency |
| Lock/authentication | Locked phone, expired login, denied consent, inaccessible protected data | No hang, disclosure or request to manipulate the phone |
| Geometry/input | Compact, wide and portrait receiver configurations; touch and knob input | Legible layout, correct focus/back behavior and runtime limits |
| Physical CarPlay | Aftermarket head unit and OEM vehicle; wired/wireless where supported | Correct audio routing, steering controls and reconnect |
| Ultra | Actual supported Ultra vehicle | Main UI, guidance metadata and display transitions work |
| Audio | Buffering/failure, seek, track changes, phone/Siri/navigation interruptions | Playback and Now Playing agree; appropriate resume behavior |
| Video | Supporting/non-supporting receivers; allowed/prohibited playback | Correct discovery, audio fallback and captions/tracks; no policy bypass |
| Conversation | Listen/process/speak; End; interruption; disconnect; slow/offline backend | Accurate state, bounded microphone lifetime and effective cancellation |
| Widgets/activities | Touch/non-touch, disfavored widget, compact fallback/small layout | Useful passive content and only supported interactions |
| HomeView media | HomeView Software 27.2; iPhone 27.2+; iPad negative control | Eligible iPhone media works; iPad media route remains unavailable. [support.apple.com](https://support.apple.com/en-us/127246) |
| HomeView household | Personal/shared surfaces, account switch, face recognition, phone absent/restricted/offline, night mode | Correct owner/content boundaries and graceful unavailable states |
| Distribution | Clean TestFlight install and upgrade without Xcode attached | Destination behavior and approved distribution entitlements survive signing |

<INFERENCE from="Apple destination requirements, HIG and managed-capability restrictions">Record OS/build, receiver model, signed entitlements, steps and captures. TestFlight is a distribution check, not an entitlement bypass. Physical HomeView acceptance remains necessary; unofficial virtualization does not establish supported-platform behavior.</INFERENCE> [developer.apple.com](https://developer.apple.com/help/account/reference/provisioning-with-managed-capabilities)

### 6. Gaps and roadmap: what changed, and what should influence planning?

| Date | Evidence/confidence | Finding |
|---|---|---|
| June 2025 | Apple-documented / High | Widgets, Live Activities and automatic appearance changes announced for iOS 26. [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/) |
| June 2026 | Apple-documented / High | Video browsing, richer media lists, MiniPlayer, voice overlay and navigation panels described. Route sharing requires iOS 26.4 and supporting vehicles. [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) |
| 13 October 2026 | Apple-documented / High | HomeView media/widget integration documented; HomeView widget HIG added. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| 1 November 2026 | Developer-observed / Medium | Troughton-Smith asks for destination-aware layouts and alternatives to phone-dependent templates. This is feedback, not Apple’s roadmap. [mastodon.social](https://mastodon.social/@stroughtonsmith/117542721617795300) [mastodon.social](https://mastodon.social/@stroughtonsmith/117542873027178404) |
| 2 November 2026 | Rumoured / Low | Camera streaming/recording settings reported from code; no third-party camera SDK or delivery date established. [9to5mac.com](https://9to5mac.com/2026/11/02/homeview-could-double-as-a-homekit-security-camera-shows-code/) |
| 3 November 2026 | Apple-documented / High | Expanded Siri AI/App Intents developer preview announced; Apple describes App Store submission opening in spring. [developer.apple.com](https://developer.apple.com/news/?id=gdk2umrf) |
| 5 November 2026 | Rumoured / Low | `ConversationalApps` and bidirectional-audio groundwork reported; activation and public API remain unverified. [9to5mac.com](https://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/) |

**Important separation — A/H:** the expanded Siri AI developer preview is not the same as existing shipping App Intents, and does not establish HomeView eligibility for third-party conversational assistants. [Apple announcement](https://developer.apple.com/news/?id=gdk2umrf). [developer.apple.com](https://developer.apple.com/news/?id=gdk2umrf)

<INFERENCE from="Documented routes and absent native distribution contract">Build on existing iPhone services now, keeping destination presentation separate. An eventual HomeView API could reuse those services; its arrival should not determine the present release plan.</INFERENCE>

#### Engineering comparison

| Route | Execution / UI | Approval and license | Latency / cost evidence | Appropriate use |
|---|---|---|---|---|
| Audio → HomeView | iPhone services; host media templates | Audio grant; Developer Program/Addendum | No bridge SLA or separate per-app HomeView charge located | Genuine audio/mixed-media product |
| Video → HomeView | iPhone playback/AirPlay; host browsing/player | Video grant; audiovisual content | Same evidence gap; media/backend costs are product-specific | Video-primary product |
| Small widget → HomeView | WidgetKit extension; host rendering | Existing iOS widget distribution/agreement | Timeline-driven; no measured end-to-end latency established | Focused information/actions |
| HomeKit/Matter/App Intents | iPhone integrations and Apple system experiences | Applicable capabilities, consent and terms | No universal latency/cost figure | Accessory control/discrete actions |
| Native HomeView executable | No supported public target verified | No public submission contract verified | Unavailable | No committed shipping implementation |

<INFERENCE from="Entitlement references, Widget HIG and HomeKit/MatterSupport contracts">These are architectural choices, not measured benchmarks. Model parameter counts and context windows do not characterize these platform routes.</INFERENCE>

### 7. Open questions: what can Apple primary sources settle?

**(a) Combining audio and video — unresolved conflict; High confidence that the conflict exists.**

WWDC26 recommends both; current canonical references prohibit combining them. The audio entitlement independently permits audiovisual content. <CONFLICTING_EVIDENCE>[No verified Apple correction reconciles the session and current policy.]</CONFLICTING_EVIDENCE> [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md)

<INFERENCE from="Current entitlement contracts">Use audio alone for a qualifying mixed-media product, video for a video-primary product, and obtain written approval before combining grants.</INFERENCE>

**(b) CarPlay widget disfavor on HomeView — not established.**

**A/H:** disfavor does not categorically hide a widget even in CarPlay: people can still select it, with interaction disabled. No HomeView-specific `WidgetLocation` appears in the reference inspected. <INSUFFICIENT_EVIDENCE>[Apple does not document propagation to HomeView or a separate HomeView targeting/opt-out API.]</INSUFFICIENT_EVIDENCE> [Widget behavior](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md), [locations](https://developer.apple.com/documentation/widgetkit/widgetlocation.md). [developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md) [developer.apple.com](https://developer.apple.com/documentation/widgetkit/widgetlocation.md)

**(c) Public-safety/navigation templates — answered, A/H.**

The matrix gives their exact sets and version changes. Public safety gains Search and Voice Control; navigation gains map-panel functionality without a new category. [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)

**(d) Voice Control as root — not settled by the inspected Apple contract.**

The generic root setter does not enumerate eligible root classes; the voice reference describes presentation. Added navigation/action buttons do not establish root eligibility. <INSUFFICIENT_EVIDENCE>[No explicit Apple guarantee permitting voice-root installation from iOS 26.4 was verified.]</INSUFFICIENT_EVIDENCE> [Root setter](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/setroottemplate%28_%3Aanimated%3Acompletion%3A%29.md), [voice template](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate.md). [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/setroottemplate(_:animated:completion:).md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate.md)

<INFERENCE from="Documented modal presentation and unresolved root eligibility">Use a list root with immediately presented voice UI. Do not describe that conservative implementation as proof that all voice roots are prohibited.</INFERENCE>

**(e) Arbitrary third-party Live Activities on HomeView — not established.**

Apple’s launch examples describe system activities; its third-party Live Activity destination table lists CarPlay, not HomeView. <INSUFFICIENT_EVIDENCE>[Timers, media and Intercom examples do not establish general ActivityKit forwarding.]</INSUFFICIENT_EVIDENCE> [Launch material](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/), [HIG](https://developer.apple.com/design/human-interface-guidelines/live-activities.md). [apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/live-activities.md)

**(f) Video hierarchy depth — missing.**

<MISSING_DATA>[The guide supplies video template eligibility but omits video from its depth rule; no explicit limit was verified.]</MISSING_DATA> [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)

<INFERENCE from="Eligibility and hierarchy depth being separate rules">Do not inherit audio’s depth by analogy. Keep the proposed video flow shallow pending Apple clarification.</INFERENCE>

## Evidence Table

Apple sources qualify because they define the APIs, legal terms or supported behavior. First-hand posts qualify only as observations. The news reports qualify solely as evidence of dated rumors; they do not establish technical availability.

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---|---|---|
| Category/template/depth matrix | Apple CarPlay Developer Guide | 13 Oct 2026 | Official implementation contract | [Guide](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf) |
| Audio content and combination policy | Apple entitlement reference | Undated; checked 18 Nov 2026 | Official eligibility contract | [Audio](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md) |
| Video/HomeView eligibility | Apple entitlement reference | Undated; checked 18 Nov 2026 | Official eligibility contract | [Video](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md) |
| Competing entitlement advice; new APIs | Apple WWDC26 session | June 2026 | First-party engineering presentation | [Session](https://developer.apple.com/videos/play/wwdc2026/212/) |
| HomeView version/build | Apple Developer Releases | 12 Nov 2026 | Official release listing | [Release](https://developer.apple.com/news/releases/?id=11122026a) |
| Companion prerequisites | Apple Support | 12 Nov 2026 | Official operating requirements | [Support](https://support.apple.com/en-us/127246) |
| HomeView legal availability | Developer Program License Agreement | Live text checked 18 Nov 2026 | Primary legal text | [Agreement](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) |
| Shared widgets/night appearance | Apple Widget HIG | HomeView update 13 Oct 2026 | Official design guidance | [Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Activity destinations | Apple Live Activity HIG | Undated; checked 18 Nov 2026 | Official guidance; omission bounded | [Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities.md) |
| Video support versus policy | Apple CarPlay reference | Undated; checked 18 Nov 2026 | Exact property semantics | [Video support](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback.md) |
| Automatic signing | Apple Account Help | Undated; checked 18 Nov 2026 | Official provisioning procedure | [Signing](https://developer.apple.com/help/account/reference/provisioning-with-managed-capabilities) |
| Receiver requirements | Apple Xcode release notes | Publication date unstated | Official tool limitation | [Xcode](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes.md) |
| Automation limitations | Developer and Apple engineer | June 2026 | First-hand issue/staff response | [Forum](https://developer.apple.com/forums/thread/831782) |
| HomeView template behavior | Steve Troughton-Smith | 1 Nov 2026 | First-hand experiment | [Observation](https://mastodon.social/@stroughtonsmith/117542694509125589) |
| Siri AI preview timing | Apple Developer News | 3 Nov 2026 | Official announcement | [Preview](https://developer.apple.com/news/?id=gdk2umrf) |
| Conversational-app rumor | pdfu, reported by Ben Lovejoy | 5 Nov 2026 | Secondary report of inaccessible original | [Report](https://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/) |
| Camera-feature rumor | pdfu, reported by Ben Lovejoy | 2 Nov 2026 | Secondary code-discovery report | [Report](https://9to5mac.com/2026/11/02/homeview-could-double-as-a-homekit-security-camera-shows-code/) |

## Knowledge Gaps

- **Conflicting policy:** audio/video entitlement combination still requires Apple’s written resolution.
- **Undocumented behavior:** HomeView widget targeting, disfavor propagation, arbitrary third-party Live Activities, voice-root eligibility and video depth remain unsettled.
- **Unavailable evidence:** precise Apple-confirmed OS ancestry, original beta-code reproduction, the team’s authenticated Addendum and reliable approval-turnaround data.
- **Unperformed verification:** Swift compilation, application archive, physical destinations, TestFlight and submission testing. Source review covered both Swift examples and the manifest; repository TypeScript tests would not validate them.
- **No measured performance evidence:** no verified bridge/voice latency, throughput SLA or universal update-rate figure was available.

## Recommended Next Steps

1. <INFERENCE from="Contradictory entitlement sources and omitted video depth">Ask Apple for written mixed-media entitlement and video-depth clarification, attaching the exact conflicting references. This prevents implementation against incompatible distribution rules.</INFERENCE>
2. <INFERENCE from="Undocumented widget and activity propagation">Run a HomeView hardware probe with suitable/disfavored widgets and a known third-party Live Activity, recording build and household state. Treat results as build-specific observations.</INFERENCE>
3. <INFERENCE from="Unresolved voice-root contract">Submit a minimal native reproduction comparing voice-root and list-plus-modal presentation on the intended releases. This separates template eligibility from presentation eligibility.</INFERENCE>
4. <INFERENCE from="Unperformed compilation and acceptance testing">Run the supplied [compiler-check script](/tmp/carplay-homeview-research-20261118/check-examples.sh), connect the real engines and execute the applicable matrix before submission.</INFERENCE>

Compiler verification remains blocked by the harbourmaster skill (`harbourmaster:harbourmaster`), which requires “Local work goes through the wrapper.” Admission refused the compiler run; the supplied skeletons cannot yet be claimed to compile.

🌱 graft reported approximately 93.5k tokens saved, one call. `UNVERIFIED (unusable citation URL)`
