## Executive Summary

- (High Confidence) **Choose the CarPlay entitlement for the app’s actual primary function.** Use audio for a genuine media app and voice-based conversation for a genuine assistant. A general dashboard cannot adopt either category merely to reach HomeView. **Apple-documented**, CarPlay Developer Guide, 13 October 2026. [Guide](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)
- (High Confidence) **HomeView’s supported full-app route is the existing iPhone CarPlay audio/video experience.** Apple confirms automatic availability; its agreement specifies that the application runs on the paired iOS device. **Apple-documented**, current documentation accessed 18 November 2026. [CarPlay](https://developer.apple.com/carplay/), [agreement §6.4.2](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)[developer.apple.com](https://developer.apple.com/carplay/)[developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)
- (High Confidence) **CarPlay conversational apps start at iOS 26.4; the dedicated video entitlement starts at iOS 27.** Parked AirPlay playback and a browsable CarPlay video application are different capabilities. **Apple-documented**, Guide, 13 October 2026. [Guide](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)
- (Medium Confidence) **HomeView conversational apps remain a roadmap dependency.** Public firmware differences contain “Conversational Apps” and related audio-session work. They establish implementation groundwork, not enabled functionality, an approval route or a release date. **Developer-observed** code; shipping outcome **rumoured**, November 2026. [Firmware diff](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md), [pdfu](https://pdfu.dev/)[github.com](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md)[pdfu.dev](https://pdfu.dev/)
- (High Confidence) **Small widgets are the defensible HomeView launch route for general-purpose apps.** Apple explicitly documents connected-device widgets and the shared Modular face. <INFERENCE from="HomeView supports connected-device small widgets; projected full apps are limited to audio/video">Build the useful widget first when the app does not qualify as a media app.</INFERENCE> **Apple-documented basis**, current Widgets HIG. [HIG](https://developer.apple.com/design/human-interface-guidelines/widgets)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets)
- (High Confidence) **Plan physical-device testing.** Xcode 27’s CarPlay development path uses a USB-connected iPhone through Device Hub; Apple recommends additional vehicle or aftermarket testing. **Apple-documented**, current testing documentation and Xcode 27.2 notes. [Testing](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator), [release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes)[developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator)[developer.apple.com](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes)
- (Medium Confidence) <INFERENCE from="CarPlay requires native scenes/templates; react-native-carplay disclaims Expo support; its issues record scene integration failures">Keep scene registration and audio lifecycle native in both codebases. For Expo, use a custom native build and config plugin; adopt the community library only after a compatibility spike.</INFERENCE> **Developer-observed basis**, library documentation and issues; Expo documentation updated 2 November 2026. [Library](https://github.com/birkir/react-native-carplay), [Expo](https://docs.expo.dev/develop/development-builds/introduction/)[github.com](https://github.com/birkir/react-native-carplay)[docs.expo.dev](https://docs.expo.dev/develop/development-builds/introduction/)

## Detailed Findings

Evidence cutoff: **18 November 2026**. Undated living documentation is identified by access date rather than assigned a publication date. “Developer-observed” means firsthand reporting, not independently reproduced behavior. Recommendations and constructed examples are marked as inferences.

### 1. Platform surface: which categories, entitlements and templates exist, and what reaches HomeView?

**The launch date is confirmed.** Apple announced HomeView on **13 October 2026**, with availability beginning **13 November 2026**. **Apple-documented; High confidence.** [Announcement](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/)[apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/)

The five assumptions need these qualifications:

| Claim | Verdict | Source and date |
|---|---|---|
| Shipping software is “HomeView Software 27.2” | **Confirmed. Apple-documented; High.** Apple lists build **24V526**. | [Apple release listing](https://developer.apple.com/news/releases/?id=11122026a), 12 November 2026.[developer.apple.com](https://developer.apple.com/news/releases/?id=11122026a) |
| It derives from tvOS 27.2 | **Developer-observed; Medium.** Steve Troughton-Smith identifies tvOS 27.2 and device family 8. This is not a public HomeView SDK contract. | [Firsthand firmware experiment](https://mastodon.social/@stroughtonsmith/117532557440780934), 30 October 2026.[mastodon.social](https://mastodon.social/@stroughtonsmith/117532557440780934) |
| No SDK, App Store, simulator or design kit at launch | **Supported with qualification; Medium.** No public native deployment toolchain, dedicated simulator or design kit was located. Community reconstructed tooling is separate. **“No design guidance” is incorrect:** Apple’s Widgets HIG covers HomeView. | [Apple resources](https://developer.apple.com/design/resources/), accessed 18 November; [developer tooling experiment](https://mastodon.social/@stroughtonsmith/117536684546935309), 31 October; [Widgets HIG](https://developer.apple.com/design/human-interface-guidelines/widgets).[developer.apple.com](https://developer.apple.com/design/resources/)[mastodon.social](https://mastodon.social/@stroughtonsmith/117536684546935309)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Third-party routes include CarPlay media, widgets, Live Activities and accessories | **Partly confirmed. High for media/widgets/accessories; insufficient for arbitrary third-party Live Activities.** Apple documents HomeView Live Activities, but that does not establish general ActivityKit mirroring. | [CarPlay](https://developer.apple.com/carplay/), [agreement §6.4](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/), [HomeView](https://www.apple.com/apple-homeview/), accessed 18 November.[developer.apple.com](https://developer.apple.com/carplay/)[developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)[apple.com](https://www.apple.com/apple-homeview/) |
| iOS 27.3 beta adds “Conversational Apps” | **Confirmed as a code observation; Medium. Unconfirmed as shipping functionality.** A private-framework diff contains the category string and related audio-session symbols. | [Firmware comparison](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md); [pdfu’s November update](https://pdfu.dev/).[github.com](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md)[pdfu.dev](https://pdfu.dev/) |

<MISSING_DATA>A public HomeView native SDK, App Store submission route, simulator and dedicated design kit were sought but not found. This does not establish what internal tools Apple has.</MISSING_DATA>

**Capability matrix**

All category/template permissions below are **Apple-documented, High confidence**, from the Guide dated **13 October 2026**, particularly pages 14–15. Entitlement suffixes expand to `com.apple.developer.carplay-<suffix>`.

Template abbreviations:

- **B:** `CPActionSheetTemplate`, `CPAlertTemplate`, `CPGridTemplate`, `CPListTemplate`, `CPTabBarTemplate`
- **V:** `CPVoiceControlTemplate`; **C:** `CPContactTemplate`; **I:** `CPInformationTemplate`
- **M:** `CPMapTemplate`; **N:** `CPNowPlayingTemplate`; **P:** `CPPointOfInterestTemplate`; **S:** `CPSearchTemplate`

Permission to use a template does not make it a valid root, pushed template or tab in every context. [Guide](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)

| Category | iOS 26.x: availability / entitlement / templates | iOS 27.0–27.3 beta: availability / entitlement / templates | HomeView launch: availability / entitlement / templates |
|---|---|---|---|
| Audio | Yes / `audio` / B+N | Yes / `audio` / B+N+V+S | Yes / `audio` / existing media templates, adapted by system |
| Communication: messaging/VoIP | Yes / `communication` / B+C+I+N | Yes / `communication` / B+C+I+N+V | No documented projected-app route / none / none |
| Navigation | Yes / `maps` / B+C+I+M+S+V | Yes / `maps` / same | No documented projected-app route / none / none |
| EV charging | Yes / `charging` / B+I+P | Yes / `charging` / B+I+P+V+S | No documented projected-app route / none / none |
| Parking | Yes / `parking` / B+I+P | Yes / `parking` / B+I+P+V+S | No documented projected-app route / none / none |
| Fueling | Yes / `fueling` / B+I+P | Yes / `fueling` / B+I+P+V+S | No documented projected-app route / none / none |
| Quick food ordering | Yes / `quick-ordering` / B+I+P | Yes / `quick-ordering` / B+I+P+V | No documented projected-app route / none / none |
| Driving task | Yes / `driving-task` / B+I+P; V from 26.4 | Yes / `driving-task` / B+I+P+V | No documented projected-app route / none / none |
| Voice-based conversational | From 26.4 / `voice-based-conversation` / B+I+P+V | Yes / same entitlement and templates | Not publicly enabled/documented; beta groundwork / no published HomeView entitlement / no guaranteed surface |
| Video | Dedicated category unavailable; distinguish AirPlay transport / no video-category entitlement / none | From 27.0 / `video` / B+N+V+S | Yes / `video` / media templates and system video presentation |
| Public safety | Yes / `public-safety` / B+C+I+N+P+S | Yes / `public-safety` / B+C+I+N+P+S+V | No documented projected-app route / none / none |

Sources for the matrix: [Apple Guide](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf), [Apple’s explicit HomeView media support statement](https://developer.apple.com/carplay/).[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/carplay/)

**Version boundaries:** No additional publicly documented category was found specifically for iOS 27.1, 27.2 or 27.3 beta. Some APIs presented in the iOS 27 WWDC session actually declare **iOS 26.4** availability, including `CPPlaybackConfiguration` and `CPSessionConfiguration.supportsVideoPlayback`. Symbol availability does not move the dedicated video entitlement’s documented minimum. **Apple-documented; High.** [Playback configuration](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration), [video capability](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback)

**A material entitlement contradiction remains.**

<CONFLICTING_EVIDENCE>WWDC26 recommends combining audio and video entitlements for suitable media apps. The later Guide identifies only charging-plus-fueling as a permitted combination. The current audio-entitlement reference expressly prohibits combining audio with other CarPlay entitlements from iOS 26.3.</CONFLICTING_EVIDENCE>

**Apple-documented conflict; High confidence.** <INFERENCE from="The later Guide and current entitlement reference prohibit a combination recommended at WWDC">Use the single audio entitlement for audio and audio-bearing video when that matches the product. Obtain written Apple clarification before making a dual-entitlement release an architectural requirement.</INFERENCE> [WWDC26](https://developer.apple.com/videos/play/wwdc2026/212/), [audio entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/)[developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio)

**CarPlay Ultra uses the same app framework and category permissions.** It adds vehicle-integrated screens and controls, not unrestricted third-party cluster UI. Navigation apps can use supported cluster/HUD APIs; ordinary apps retain their template surface. **Apple-documented; High**, WWDC25, June 2025. [Session](https://developer.apple.com/videos/play/wwdc2025/216/)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/)

### 2. UI and UX: which rules govern CarPlay and HomeView?

HIG sources below are living Apple documents accessed **18 November 2026**.

| Rule | Classification, confidence and source |
|---|---|
| Keep tasks brief and scannable; prioritize important controls and remove unnecessary detail. | **Apple-documented; High.** [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay) |
| Complete phone setup beforehand. Support locked-iPhone operation and report errors in CarPlay without directing the driver to manipulate the phone. | **Apple-documented; High.** [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay) |
| Use system templates for their intended content; let the system handle layout and vehicle-input adaptation. | **Apple-documented; High.** [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay) |
| Let people initiate audio. Activate the session when playback is ready; distinguish resumable interruptions from replacement by another source. | **Apple-documented; High.** [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay) |
| Support light/dark appearances and inspect colors under actual vehicle sunlight/night conditions. | **Apple-documented; High.** [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay) |
| Widgets need concise information, large typography, removable backgrounds and rendering-mode adaptation for distance viewing. | **Apple-documented; High.** [Widgets HIG](https://developer.apple.com/design/human-interface-guidelines/widgets), [implementation guidance](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets)[developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget) |
| HomeView’s shared Modular face supports up to **four small widgets**. They can expose different household members’ information to everyone; the personalized Home Screen is a separate context. | **Apple-documented; High.** [Widgets HIG](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets#Apple-HomeView) |
| Test HomeView widgets in full color, clear/tinted appearances, background-free Modular presentation and red-tinted Night Mode. | **Apple-documented; High.** [Widgets HIG](https://developer.apple.com/design/human-interface-guidelines/widgets)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Live Activities represent bounded ongoing tasks, avoid advertising/sensitive information, and end when the task ends. | **Apple-documented; High.** [Live Activities HIG](https://developer.apple.com/design/human-interface-guidelines/live-activities)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/live-activities) |

**Liquid Glass:** CarPlay receives system appearance updates automatically; iOS 26 specifically gives `CPMapTemplate` buttons Liquid Glass treatment. <INFERENCE from="System-rendered templates receive the appearance update">Supply appropriate icons and content rather than recreating glass in custom CarPlay views.</INFERENCE> **Apple-documented basis; High**, WWDC25. [Session](https://developer.apple.com/videos/play/wwdc2025/216/)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/)

**Hard limits come from the APIs and Guide, not a universal HIG number:**

| Constraint | Documented rule |
|---|---|
| List length | Read `CPListTemplate.maximumItemCount` and `maximumSectionCount`. Vehicles can restrict lists to **12 items**; do not treat “500 rows” as a universal contract. **Apple-documented; High.** [API](https://developer.apple.com/documentation/carplay/cplisttemplate/maximumitemcount), [Guide p.19](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/documentation/carplay/cplisttemplate/maximumitemcount)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf) |
| Tab count | Read `CPTabBarTemplate.maximumTabCount`. The Guide describes **4 audio tabs** and **5 for other categories**, subject to change. **Apple-documented; High.** [Guide p.26](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf) |
| Stack depth, including root | Audio/communication/charging/parking/public safety/navigation: **5**. Fueling/conversation: **3**. Driving task/quick ordering: **2 through 26.3**, **3 from 26.4**. **Apple-documented; High.** [Guide p.15](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf) |
| Voice action buttons | Up to **2 from iOS 26.4**. **Apple-documented; High.** [API](https://developer.apple.com/documentation/carplay/cpvoicecontrolstate/actionbuttons)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontrolstate/actionbuttons) |

<MISSING_DATA>The Guide’s stack-depth paragraph omits video. Verify the intended hierarchy rather than assuming the audio limit applies.</MISSING_DATA>

**Voice interaction:** A conversational app’s primary modality must be voice from launch. Show the voice-control template during active voice use and avoid displaying textual or illustrated answers. App Intents exposes app actions to Siri/Shortcuts; it does not grant conversational-app eligibility or replace Siri’s system role. **Apple-documented; High**, Guide October 2026 and WWDC25. [Voice template](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate), [App Intents](https://developer.apple.com/videos/play/wwdc2025/275/)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/275/)

**Widgets and Live Activities differ:** Small widgets work without a CarPlay app entitlement. Touchscreen widgets can perform App Intent actions; non-touchscreen widgets are noninteractive. CarPlay Live Activities are **noninteractive**, using the small activity family or compact Dynamic Island fallback. **Apple-documented; High**, WWDC25. [Widget behavior](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget), [session](https://developer.apple.com/videos/play/wwdc2025/216/)[developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/)

### 3. Code: what should the SwiftUI and React Native/Expo teams build?

<INFERENCE from="CarPlay scenes provide system templates; HomeView reuses eligible media interfaces">Keep the existing phone UI and domain services. Add a native scene adapter, with playback/conversation owned by an app-lifetime service. Do not put the phone’s SwiftUI or React view tree into a non-navigation CarPlay window.</INFERENCE> **Recommendation; High.** [Scene API](https://developer.apple.com/documentation/carplay/cptemplateapplicationscene)[developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscene)

**Scene manifest**

Merge this with the existing manifest, preserving the phone scene and its SwiftUI/Expo lifecycle. Substitute the delegate class for the selected category. CarPlay can launch the process before the phone scene exists. **Apple-documented; High.** [Scene documentation](https://developer.apple.com/documentation/carplay/cptemplateapplicationscene)[developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscene)

```xml
<key>UIApplicationSceneManifest</key>
<dict>
  <key>UIApplicationSupportsMultipleScenes</key><true/>
  <key>UISceneConfigurations</key>
  <dict>
    <!-- Preserve the existing phone scene configuration here. -->
    <key>CPTemplateApplicationSceneSessionRoleApplication</key>
    <array><dict>
      <key>UISceneClassName</key>
      <string>CPTemplateApplicationScene</string>
      <key>UISceneConfigurationName</key><string>CarPlay</string>
      <key>UISceneDelegateClassName</key>
      <string>$(PRODUCT_MODULE_NAME).AudioCarScene</string>
    </dict></array>
  </dict>
</dict>
```

The following are **authored integration skeletons, not compiled or device-tested implementations**. <INFERENCE from="Apple scene, template, AVAudioSession and MediaPlayer contracts">Supply the real catalogue/voice engine, permission handling, serialized commands, player-state observation, interruption handling and production error presentation.</INFERENCE> **Implementation recommendation; High.**

**(a) Audio app**

Requires the approved audio entitlement, appropriate background-audio capability and, for this example, a bundled `sample.m4a`. Template, metadata and remote-command responsibilities are separate. **Apple-documented APIs; High.** [Now Playing](https://developer.apple.com/documentation/carplay/cpnowplayingtemplate), [metadata](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter), [commands](https://developer.apple.com/documentation/mediaplayer/mpremotecommandcenter)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpnowplayingtemplate)[developer.apple.com](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter)[developer.apple.com](https://developer.apple.com/documentation/mediaplayer/mpremotecommandcenter)

```swift
import AVFoundation
import CarPlay
import MediaPlayer
import UIKit

@MainActor
final class AudioPlayback: NSObject {
    static let shared = AudioPlayback()
    private let player = AVPlayer()

    override private init() {
        super.init()
        let commands = MPRemoteCommandCenter.shared()
        commands.playCommand.addTarget(self, action: #selector(remotePlay(_:)))
        commands.pauseCommand.addTarget(self, action: #selector(remotePause(_:)))
    }

    func select(_ url: URL) throws {
        player.replaceCurrentItem(with: AVPlayerItem(url: url))
        try resume()
    }

    private func resume() throws {
        let session = AVAudioSession.sharedInstance()
        try session.setCategory(.playback, mode: .default)
        try session.setActive(true)
        player.play()
        publish(rate: 1)
    }

    private func publish(rate: Double) {
        MPNowPlayingInfoCenter.default().nowPlayingInfo = [
            MPMediaItemPropertyTitle: "Sample",
            MPNowPlayingInfoPropertyElapsedPlaybackTime:
                player.currentTime().seconds,
            MPNowPlayingInfoPropertyPlaybackRate: rate
        ]
    }

    @objc private func remotePlay(
        _ event: MPRemoteCommandEvent
    ) -> MPRemoteCommandHandlerStatus {
        guard player.currentItem != nil else { return .noSuchContent }
        do { try resume(); return .success }
        catch { return .commandFailed }
    }

    @objc private func remotePause(
        _ event: MPRemoteCommandEvent
    ) -> MPRemoteCommandHandlerStatus {
        player.pause()
        publish(rate: 0)
        return .success
    }
}

@MainActor
final class AudioCarScene: UIResponder, CPTemplateApplicationSceneDelegate {
    private var interface: CPInterfaceController?

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didConnect controller: CPInterfaceController
    ) {
        interface = controller
        let item = CPListItem(text: "Sample", detailText: nil)

        item.handler = { _, completion in
            defer { completion() }

            guard let url = Bundle.main.url(
                forResource: "sample", withExtension: "m4a"
            ) else {
                item.detailText = "Audio unavailable"
                return
            }

            do {
                try AudioPlayback.shared.select(url)
                controller.pushTemplate(
                    CPNowPlayingTemplate.shared, animated: true
                ) { ok, _ in
                    if !ok { NSLog("CarPlay presentation failed") }
                }
            } catch {
                item.detailText = "Playback unavailable"
            }
        }

        let root = CPListTemplate(
            title: "Listen", sections: [CPListSection(items: [item])]
        )
        controller.setRootTemplate(root, animated: false) { ok, _ in
            if !ok { NSLog("CarPlay root installation failed") }
        }
    }

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didDisconnect controller: CPInterfaceController
    ) {
        interface = nil
    }
}
```

<INFERENCE from="Player requests and actual playback state differ; metadata and remote controls are independent of templates">Publish real title/artwork/duration/elapsed time/rate from observed player state. Marshal remote callbacks to the playback executor, register targets once and balance audio-session activation. Scene disconnect should not automatically destroy ongoing phone playback.</INFERENCE> **Recommendation; High.** [Metadata API](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter), [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay)[developer.apple.com](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter)[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay)

**(b) Voice-based conversational app**

Requires the approved `voice-based-conversation` entitlement, an **iOS 26.4** availability gate, microphone permission and any speech permission required by the selected engine. The protocol below is an application-owned dependency, not an Apple API. **Apple-documented API basis; High.** [Voice APIs](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate), [action availability](https://developer.apple.com/documentation/carplay/cpvoicecontrolstate/actionbuttons)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontrolstate/actionbuttons)

```swift
import AVFoundation
import CarPlay
import UIKit

@MainActor
protocol ConversationEngine: AnyObject {
    var phaseChanged: ((String) -> Void)? { get set }
    func start() throws  // Real capture, recognition and spoken responses.
    func stop()          // Cancels capture, network work and speech.
}

@MainActor
enum ConversationServices {
    static var engine: (any ConversationEngine)?
}

@available(iOS 26.4, *)
@MainActor
final class ConversationCarScene: UIResponder,
                                  CPTemplateApplicationSceneDelegate {
    private var interface: CPInterfaceController?
    private var engine: (any ConversationEngine)?

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didConnect controller: CPInterfaceController
    ) {
        interface = controller
        guard let engine = ConversationServices.engine else { return }
        self.engine = engine

        let states = ["Listening", "Thinking", "Speaking"].map {
            CPVoiceControlState(
                identifier: $0, titleVariants: [$0],
                image: nil, repeats: false
            )
        }
        let voice = CPVoiceControlTemplate(voiceControlStates: states)
        voice.trailingNavigationBarButtons = [
            CPBarButton(title: "End") { [weak self] _ in self?.end() }
        ]
        engine.phaseChanged = { phase in
            voice.activateVoiceControlState(withIdentifier: phase)
        }

        let root = CPListTemplate(title: "Voice", sections: [])
        controller.setRootTemplate(root, animated: false) { [weak self] ok, _ in
            guard ok else { return }
            controller.presentTemplate(voice, animated: false) { shown, _ in
                guard shown else { return }
                do {
                    let session = AVAudioSession.sharedInstance()
                    try session.setCategory(.playAndRecord, mode: .default)
                    try session.setActive(true)
                    voice.activateVoiceControlState(withIdentifier: "Listening")
                    try engine.start()
                } catch {
                    self?.end()
                }
            }
        }
    }

    private func end() {
        engine?.stop()
        engine?.phaseChanged = nil
        do {
            try AVAudioSession.sharedInstance().setActive(
                false, options: .notifyOthersOnDeactivation
            )
        } catch {
            NSLog("Voice audio-session deactivation failed")
        }
        interface?.dismissTemplate(animated: true) { ok, _ in
            if !ok { NSLog("Voice template dismissal failed") }
        }
    }

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didDisconnect controller: CPInterfaceController
    ) {
        end()
        interface = nil
        engine = nil
    }
}
```

<INFERENCE from="Voice UI is required during capture; sessions should exist only during active voice use">Install the real engine during process startup, including CarPlay-only launches. Replace missing-engine/error paths with usable recovery UI; validate phase identifiers, check permission before capture, and cancel pending connection work on disconnect. Handle interruptions and stop capture promptly.</INFERENCE> **Recommendation; High.** Apple’s conversational guidance specifies `.playAndRecord`, default mode and no mixing. **Apple-documented**, WWDC26. [Session](https://developer.apple.com/videos/play/wwdc2026/212/)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/)

**Video**

Use AirPlay-capable `AVPlayer` playback, with `AVPlayerViewController` for the phone experience. There is no documented `CPVideoTemplate` to instantiate. Configure playable items using `CPPlaybackConfiguration`, including `.video` as the preferred presentation. **Apple-documented; High**, current references and Apple-staff Q&A, June 2026. [AVPlayer](https://developer.apple.com/documentation/avfoundation/avplayer/allowsexternalplayback), [configuration](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration), [Q&A](https://developer.apple.com/forums/thread/831710)[developer.apple.com](https://developer.apple.com/documentation/avfoundation/avplayer/allowsexternalplayback)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration)[developer.apple.com](https://developer.apple.com/forums/thread/831710)

`supportsVideoPlayback` describes session capability and remains stable during a session. It is **not the current parked-state permission signal**. The system can suppress video and continue audio from the same source; maintain metadata and remote controls. **Apple-documented; High.** [Capability API](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback), [Apple engineer](https://developer.apple.com/forums/thread/831710)[developer.apple.com](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback)[developer.apple.com](https://developer.apple.com/forums/thread/831710)

**App Intents, widgets, Live Activities and accessories**

App Intents/App Shortcuts exposes meaningful app actions; communication also uses the relevant SiriKit/CallKit contracts. WidgetKit uses `.systemSmall` and App Intent buttons/toggles. ActivityKit uses the normal iPhone implementation, `NSSupportsLiveActivities`, and `.supplementalActivityFamilies([.small])` for CarPlay. HomeKit requires its capability and `NSHomeKitUsageDescription`; integrating accessories does not install an application on HomeView. **Apple-documented; High.** [App Intents](https://developer.apple.com/videos/play/wwdc2025/275/), [WidgetKit](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget), [ActivityKit](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities), [HomeKit](https://developer.apple.com/documentation/homekit/enabling-homekit-in-your-app)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/275/)[developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget)[developer.apple.com](https://developer.apple.com/documentation/activitykit/displaying-live-data-with-live-activities)[developer.apple.com](https://developer.apple.com/documentation/homekit/enabling-homekit-in-your-app)

**React Native and Expo**

The library README explicitly disclaims Expo support because of scenes. Issue **#236**, dated **9 July 2025**, reports an Expo black screen on iOS 18.5; **#238**, dated **3 September 2025**, reports missing templates with RN 0.81.1 on iOS 18.2. These demonstrate integration risk, **not an iOS 26/27 SDK regression**. **Developer-observed; Medium.** [README](https://github.com/birkir/react-native-carplay), [#236](https://github.com/birkir/react-native-carplay/issues/236), [#238](https://github.com/birkir/react-native-carplay/issues/238)[github.com](https://github.com/birkir/react-native-carplay)[github.com](https://github.com/birkir/react-native-carplay/issues/236)[github.com](https://github.com/birkir/react-native-carplay/issues/238)

<INFERENCE from="Expo supports custom native builds/config plugins; CarPlay needs native scenes, entitlements and lifecycle">For Expo, add a native module and idempotent config plugin that merges scenes, entitlement declarations, source files and relevant background modes. Build a custom development client and distribution archive. Expo Go and JavaScript-only updates cannot supply missing native integration. Keep scene startup independent of JS readiness.</INFERENCE> **Recommendation; High.** [Expo builds](https://docs.expo.dev/develop/development-builds/introduction/), [plugins](https://docs.expo.dev/config-plugins/introduction/)[docs.expo.dev](https://docs.expo.dev/develop/development-builds/introduction/)[docs.expo.dev](https://docs.expo.dev/config-plugins/introduction/)

<INSUFFICIENT_EVIDENCE>No maintained certification of react-native-carplay across both iOS 26 and 27 was established. Test the exact Expo/RN/library versions, New Architecture configuration, Swift concurrency settings and scene lifecycle rather than asserting universal compatibility or breakage.</INSUFFICIENT_EVIDENCE>

| Approach | Execution / SDK | UI ownership | Cost / license evidence | Decision |
|---|---|---|---|---|
| SwiftUI plus native adapter | Existing iOS process; public CarPlay SDK | Apple templates | Apple distribution terms; maintenance cost unmeasured | **Recommended; High inference** |
| Expo plus native module/plugin | Custom iOS build; native scene with JS domain integration | Apple templates | Native-build maintenance unmeasured | **Recommended for Expo; High inference** |
| `react-native-carplay` | Community native bridge | Templates exposed by library | MIT repository; integration effort unmeasured | **Conditional; Medium** |
| Standalone HomeView app | No public shipping target established | No supported native third-party UI route established | No public distribution contract established | **No launch commitment; Medium** |

Sources: [Apple scenes](https://developer.apple.com/documentation/carplay/cptemplateapplicationscene), [Expo](https://docs.expo.dev/config-plugins/introduction/), [library](https://github.com/birkir/react-native-carplay).[developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscene)[docs.expo.dev](https://docs.expo.dev/config-plugins/introduction/)[github.com](https://github.com/birkir/react-native-carplay)

### 4. Entitlements and deployment: how does the team obtain approval and submit?

**The application route is shared across categories.** Apply through Apple’s CarPlay contact flow, explain the actual category/use case and accept the entitlement addendum. Following approval, enable the granted capability on the App ID, regenerate development/distribution profiles, add the matching Xcode capability and inspect the signed archive. A local entitlement Boolean does not confer approval. **Apple-documented; High**, Guide, October 2026. [Request](https://developer.apple.com/contact/carplay/), [development requirements](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator)[developer.apple.com](https://developer.apple.com/contact/carplay/)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator)

**Approval timing has no established SLA.** Firsthand reports dated **6–9 October 2026** describe audio approval in days, driving-task approval from about a day to several weeks, and an outlier exceeding a year. This uncontrolled sample cannot support a forecast or percentile. **Developer-observed; Low predictive confidence.** [Reports](https://www.reddit.com/r/CarPlay/comments/1wyuqv5/how_long_does_apple_take_to_approve_carplay/)[reddit.com](https://www.reddit.com/r/CarPlay/comments/1wyuqv5/how_long_does_apple_take_to_approve_carplay/)

**Rejection-prone behavior** includes category mismatch, repurposed template fields, lyrics/message bodies, social/game features, directing drivers to the phone, general retail masquerading as quick food ordering, or location-finding masquerading as a driving task. **Apple-documented; High**, Guide’s category guidelines. [Guide](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)

Entitlement approval does not replace App Review. Relevant rules include:

| Rule | Application |
|---|---|
| §2.1 | Complete, functioning app and accessible review experience |
| §2.5.1 | Public APIs used for their intended purposes |
| §2.5.4 | Legitimate background-service use |
| §2.5.11 | Relevant, supported SiriKit/Shortcuts functionality |
| §2.5.14 | Recording consent and clear indication |
| §2.5.17 | Apple-supported Matter pairing requirements |
| §§5.1.1–5.1.2 | Privacy, collection and sharing disclosures/permission |
| §5.2 | Rights to media and other intellectual property |

**Apple-documented; High**, living guidelines accessed 18 November 2026. In particular, §5.1.2(i) requires disclosure and explicit permission when sharing personal data with third-party AI. [Guidelines](https://developer.apple.com/app-store/review/guidelines/)[developer.apple.com](https://developer.apple.com/app-store/review/guidelines/)

**HomeView has explicit contractual coverage:** agreement **§§6.4.1–6.4.2** addresses widgets and eligible CarPlay applications running on a paired device. No separate public HomeView entitlement, required opt-in plist key or separate store submission was located. **Positive contractual coverage: Apple-documented, High. Absence finding: Medium.** [Agreement](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)[developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)

**Submission checklist**

<INFERENCE from="Apple entitlement, signing, review and testing requirements">Use these release gates.</INFERENCE> **Recommendation; High.**

- [ ] Primary function matches the approved category; resolve any audio/video combination with Apple.
- [ ] App ID, development/distribution profiles and signed archive carry matching entitlements.
- [ ] Phone scenes remain intact; direct CarPlay cold launch works.
- [ ] Appropriate audio, microphone, speech and HomeKit declarations/capabilities are present.
- [ ] Locked-phone operation, interruptions, route changes and disconnects pass.
- [ ] The actual TestFlight build appears and functions on the target receivers.
- [ ] Review notes provide credentials, media samples, connection instructions and category justification.
- [ ] The archive uses Apple’s accepted release toolchain; shipping behavior does not depend on beta-only flags.
- [ ] Shared-screen privacy, AI consent, media rights, purchases and metadata have been checked.
- [ ] HomeView compatibility claims describe behavior demonstrated on shipping hardware.

### 5. Testing before publishing: what is the concrete pre-submission matrix?

**Distinguish the two simulator concepts.** Additional Tools’ CarPlay Simulator is a Mac receiver driven by a real iPhone. Xcode 27 integrates it into Device Hub and requires USB. Xcode 27.2 notes expressly exclude iOS Simulator from that CarPlay path. Older external-display workflows, where available, are not iOS 27 acceptance evidence. **Apple-documented; High.** [Testing](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator), [release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes)[developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator)[developer.apple.com](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes)

**Automation:** XCTest can exercise app-owned state, presenters and domain services. No general supported XCUITest contract for driving arbitrary system-rendered CarPlay/HomeView receiver UI was established. <INSUFFICIENT_EVIDENCE>A device-specific accessibility workaround does not establish portable receiver automation.</INSUFFICIENT_EVIDENCE> Developers requested CarPlay support in Maestro on **29 September 2026**; maintainers did not promise support. **Developer-observed; Medium.** [Issue](https://github.com/mobile-dev-inc/Maestro/issues/3641)[github.com](https://github.com/mobile-dev-inc/Maestro/issues/3641)

**Hardware:** Apple recommends vehicle or aftermarket testing; a wireless receiver lets the phone remain cabled to Xcode. Ultra needs confirmed equipped hardware, such as an appropriately configured Aston Martin. An ordinary receiver does not establish Ultra compatibility. **Apple-documented; High.** [Testing guidance](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator), [Apple hardware announcement, 15 May 2025](https://www.apple.com/newsroom/2025/05/carplay-ultra-the-next-generation-of-carplay-begins-rolling-out-today/)[developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator)[apple.com](https://www.apple.com/newsroom/2025/05/carplay-ultra-the-next-generation-of-carplay-begins-rolling-out-today/)

**TestFlight:** distribute the signed iOS app with its CarPlay entitlement. External beta review and entitlement approval are separate. **Apple-documented; High**, agreement §6.5 and development requirements. [Agreement](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/), [distribution instructions](https://github.com/birkir/react-native-carplay/blob/master/CarPlay.md)[developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)[github.com](https://github.com/birkir/react-native-carplay/blob/master/CarPlay.md)

**Proposed matrix—not executed results**

<INFERENCE from="Documented version gates, receiver differences, locked-device operation and HomeView privacy risks">Run these lanes for each codebase. Record application build, OS build, receiver model/firmware, connection type and outcome.</INFERENCE> **Recommendation; High.**

| Environment | Required cases | Pass evidence |
|---|---|---|
| Native/unit tests | Category/template selection, list limits, depth, voice states, cancellation, playback command routing | App-owned assertions including negative paths |
| iOS 26.0 and supported 26.3 device/runtime | Existing categories; unavailable conversation/video paths excluded; widgets/Live Activities | No unavailable API or unsupported-template failure |
| iOS 26.4 and latest supported 26.x device | Conversation entitlement/UI; changed depth; availability guards | Voice launch, stop, interruptions and disconnect work |
| iOS 27.0 and shipping 27.x device | New template options, MiniPlayer, expanded search/voice, media eligibility | Cold-launch and playback recordings |
| iOS 27.3 beta device | Reconnect, audio routing, widgets, conversation regressions | Separate beta issue log; no hidden-flag dependency |
| Mac CarPlay Simulator/Device Hub | USB phone; small/large, portrait/wide layouts; light/dark; imposed limits | Screenshots and lifecycle logs |
| Aftermarket receiver | Wired/wireless; touch and rotary/non-touch; reconnect | Physical-input and audio verification |
| OEM standard CarPlay | Steering controls, Siri, calls, navigation prompts, FM coexistence | Correct interruption/resumption behavior |
| Video-capable receiver | Video available/unavailable; audio fallback; unsupported car; captions/language/DRM/network loss | System-controlled fallback and usable metadata |
| Confirmed Ultra vehicle | Templates, dashboard, widgets; navigation cluster/HUD if applicable | Evidence from equipped hardware |
| Shipping HomeView + shipping paired iPhone | Media launch, menu adaptation, commands, video/AirPlay, phone locked/away | Real-device recording |
| HomeView widgets/privacy | Shared Modular versus personal Home Screen; user switching; guests; night/tint; stale data; actions | No unintended disclosure; useful unavailable states |
| Distribution/TestFlight | Fresh install, upgrade, signing, release JS bundle, offline launch | Actual distributed build works on receivers |

These coverage choices are engineering recommendations, not an Apple certification matrix. <MISSING_DATA>No Apple numeric startup/reconnect SLA was located. Measure target-device behavior and set product acceptance thresholds before beta sign-off.</MISSING_DATA>

### 6. Gaps and roadmap: what are developers requesting, and what is announced versus rumoured?

| Date | Evidence and confidence | Implication |
|---|---|---|
| June 2025 | **Apple-documented; High:** widgets, Live Activities, template enhancements and updated appearance. [WWDC25](https://developer.apple.com/videos/play/wwdc2025/216/)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/) | Supported iOS 26 baseline |
| 8 June 2026 | **Apple-documented; High:** browsable video apps, MiniPlayer, expanded voice templates and navigation panels. [WWDC26](https://developer.apple.com/videos/play/wwdc2026/212/)[developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) | Receiver-aware media enhancement path |
| June 2026 | **Apple-documented; High:** Apple engineer says CarPlay video playback-speed control is unavailable and invites feedback. [Q&A](https://developer.apple.com/forums/thread/831710)[developer.apple.com](https://developer.apple.com/forums/thread/831710) | Do not promise that control |
| 29 September 2026 | **Developer-observed; High on existence of request:** CarPlay automation support requested. [Maestro issue](https://github.com/mobile-dev-inc/Maestro/issues/3641)[github.com](https://github.com/mobile-dev-inc/Maestro/issues/3641) | Retain physical receiver testing |
| 13 October 2026 | **Apple-documented; High:** HomeView announcement and documented media projection route. [Announcement](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/)[apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/) | Build within public launch surfaces |
| 31 October–1 November 2026 | **Developer-observed; Medium:** Troughton-Smith demonstrates reconstructed UI and criticizes phone-dependent CarPlay/WatchKit-like constraints. [Demo](https://mastodon.social/@stroughtonsmith/117542694509125589), [opinion](https://mastodon.social/@stroughtonsmith/117542873027178404)[mastodon.social](https://mastodon.social/@stroughtonsmith/117542694509125589)[mastodon.social](https://mastodon.social/@stroughtonsmith/117542873027178404) | Evidence of demand for a better SDK, not a promised SDK |
| 31 October, updated 1 November 2026 | **Developer-observed code; Medium. Shipping outcome rumoured; Low:** pdfu finds security-camera settings/configuration. [Researcher](https://pdfu.dev/)[pdfu.dev](https://pdfu.dev/) | Showing external cameras is distinct from using HomeView itself as an HKSV camera |
| November 2026 beta | **Developer-observed code; Medium. Shipping outcome rumoured; Low:** conversational category and audio-session groundwork. [Diff](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md)[github.com](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md) | Keep HomeView conversation behind a roadmap gate |

<CONFLICTING_EVIDENCE>Apple’s automatic-compatibility statement concerns eligibility and reuse. Developers observe UI reconstruction, tabs becoming a menu and dependence on a nearby phone. These address different layers: automatic availability does not establish identical presentation or measured reliability.</CONFLICTING_EVIDENCE>

**Apple-documented promise: High; developer-observed implementation: Medium.** [Apple](https://developer.apple.com/carplay/), [firsthand demonstration, 1 November 2026](https://mastodon.social/@stroughtonsmith/117542694509125589)[developer.apple.com](https://developer.apple.com/carplay/)[mastodon.social](https://mastodon.social/@stroughtonsmith/117542694509125589)

<INSUFFICIENT_EVIDENCE>No Apple-announced delivery date for a public native HomeView SDK/App Store, third-party conversational launch or HomeView-as-camera API was established.</INSUFFICIENT_EVIDENCE>

## Evidence Table

Source selection follows ownership: Apple establishes API and distribution rules; original repositories and firsthand developers establish their reported observations. Consumer reviews and aggregators were excluded from technical conclusions.

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---|---|---|
| HomeView launch | Apple Newsroom | 13 October 2026 | Apple-documented; original announcement | [Announcement](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/) |
| Shipping software/build | Apple Developer Releases | 12 November 2026 | Apple-documented; release record | [Release](https://developer.apple.com/news/releases/?id=11122026a) |
| Categories, entitlements, templates, limits | Apple CarPlay Developer Guide | 13 October 2026 | Apple-documented; platform contract | [Guide](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf) |
| HomeView media projection | Apple CarPlay developer page | Undated; accessed 18 November 2026 | Apple-documented; supported route | [CarPlay](https://developer.apple.com/carplay/) |
| HomeView widgets/paired-app terms | Apple Developer Program License Agreement §6.4 | Living version; accessed 18 November 2026 | Apple-documented; governing agreement | [Agreement](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) |
| Glanceability, audio, appearance | Apple CarPlay HIG | Undated; accessed 18 November 2026 | Apple-documented; design authority | [HIG](https://developer.apple.com/design/human-interface-guidelines/carplay) |
| HomeView widget behavior/privacy | Apple Widgets HIG | Undated; accessed 18 November 2026 | Apple-documented; explicit HomeView guidance | [HIG](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Live Activity design | Apple Live Activities HIG | Undated; accessed 18 November 2026 | Apple-documented; design authority | [HIG](https://developer.apple.com/design/human-interface-guidelines/live-activities) |
| iOS 26 changes | Apple WWDC25 session 216 | June 2025 | Apple-documented; engineering presentation | [Session](https://developer.apple.com/videos/play/wwdc2025/216/) |
| iOS 27 changes | Apple WWDC26 session 212 | 8 June 2026 | Apple-documented; engineering presentation | [Session](https://developer.apple.com/videos/play/wwdc2026/212/) |
| Audio entitlement restriction | Apple entitlement reference | Undated; accessed 18 November 2026 | Apple-documented; exact key contract | [Reference](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio) |
| Video capability/current permission | Apple API reference and Apple engineer | Undated API; June 2026 Q&A | Apple-documented; resolves semantic ambiguity | [API](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback), [Q&A](https://developer.apple.com/forums/thread/831710) |
| Scene/voice implementation shape | Apple CarPlay API references | Undated; accessed 18 November 2026 | Apple-documented; symbol declarations | [Scenes](https://developer.apple.com/documentation/carplay/cptemplateapplicationscene), [voice](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate) |
| Metadata and remote controls | Apple MediaPlayer references | Undated; accessed 18 November 2026 | Apple-documented; framework contracts | [Metadata](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter), [commands](https://developer.apple.com/documentation/mediaplayer/mpremotecommandcenter) |
| Device Hub testing requirements | Apple testing guide/Xcode notes | Undated; accessed 18 November 2026 | Apple-documented; current tooling | [Testing](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator), [notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes) |
| Review restrictions | Apple App Review Guidelines | Living version; accessed 18 November 2026 | Apple-documented; distribution rules | [Guidelines](https://developer.apple.com/app-store/review/guidelines/) |
| tvOS derivation | Steve Troughton-Smith | 30 October 2026 | Developer-observed; firsthand experiment | [Post](https://mastodon.social/@stroughtonsmith/117532557440780934) |
| Reconstructed UI/developer criticism | Steve Troughton-Smith | 1 November 2026 | Developer-observed; demo/opinion | [Demo](https://mastodon.social/@stroughtonsmith/117542694509125589), [opinion](https://mastodon.social/@stroughtonsmith/117542873027178404) |
| Conversation groundwork | blacktop/ipsw-diffs; pdfu | November 2026 beta comparison | Developer-observed; inspectable diff | [Diff](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md), [researcher](https://pdfu.dev/) |
| Camera groundwork | pdfu | 31 October; updated 1 November 2026 | Developer-observed; original investigation | [Researcher](https://pdfu.dev/) |
| Expo native route | Expo documentation | Builds page updated 2 November 2026 | Vendor-authored; authoritative for Expo | [Builds](https://docs.expo.dev/develop/development-builds/introduction/), [plugins](https://docs.expo.dev/config-plugins/introduction/) |
| Community library limitations | birkir/react-native-carplay | Current README; July/September 2025 issues | Developer-observed; project-owned evidence | [Repository](https://github.com/birkir/react-native-carplay), [Expo issue](https://github.com/birkir/react-native-carplay/issues/236), [RN issue](https://github.com/birkir/react-native-carplay/issues/238) |
| Approval anecdotes | Original developer replies | 6–9 October 2026 | Developer-observed; uncontrolled self-report | [Thread](https://www.reddit.com/r/CarPlay/comments/1wyuqv5/how_long_does_apple_take_to_approve_carplay/) |
| Automation demand | Maestro issue #3641 | 29 September 2026 | Developer-observed; request/maintainer response | [Issue](https://github.com/mobile-dev-inc/Maestro/issues/3641) |

## Knowledge Gaps

- **Unpublished platform contract:** <MISSING_DATA>No public native HomeView deployment SDK/store/simulator contract, dedicated native-app HIG or HomeView-only opt-in key was located. Explicit widget guidance exists.</MISSING_DATA>
- **Conflicting Apple instructions:** <CONFLICTING_EVIDENCE>Audio-plus-video entitlement combination: WWDC26 versus the current entitlement reference and later Guide.</CONFLICTING_EVIDENCE>
- **Unsupported extrapolation:** <INSUFFICIENT_EVIDENCE>Arbitrary third-party ActivityKit mirroring to HomeView; enabled beta conversation; SDK/store/camera delivery dates.</INSUFFICIENT_EVIDENCE>
- **Missing empirical validation:** <MISSING_DATA>The two actual app codebases, skeleton compilation, shipping HomeView, target vehicles and distribution-signed builds were not tested in this investigation.</MISSING_DATA>
- **Missing quantitative baseline:** <MISSING_DATA>No Apple entitlement turnaround SLA, startup/reconnect requirement, representative approval-time distribution or measured maintenance-cost comparison was established.</MISSING_DATA>
- **Historical patch coverage:** <MISSING_DATA>The current Guide establishes documented version gates, not a historical snapshot for every iOS 26/27 patch. Verify exact SDK declarations and receiver behavior during implementation.</MISSING_DATA>

## Recommended Next Steps

1. **Audit each app’s primary function against entitlement criteria.** <INFERENCE from="Eligibility follows primary function; HomeView full-app projection is limited">Apply for audio for genuine media, conversation for a genuine assistant, or ship widgets/accessory integration when no full-app category fits.</INFERENCE> **High confidence.**
2. **Resolve the audio/video contradiction with Apple Developer Support.** <INFERENCE from="Official entitlement instructions conflict">Obtain guidance for the exact App ID and content model before signing architecture depends on a combination.</INFERENCE> **High confidence.**
3. **Build a native cold-launch spike in both codebases.** <INFERENCE from="CarPlay can launch before phone UI; Expo requires native integration">Prove scene registration, native service ownership, locked-device access and release-build operation before expanding templates.</INFERENCE> **High confidence.**
4. **Run the receiver and TestFlight matrix.** <INFERENCE from="Apple recommends hardware tests; HomeView adapts UI and exposes shared information">Make actual HomeView/vehicle evidence the gate for compatibility claims.</INFERENCE> **High confidence.**
5. **Monitor public HomeView contracts separately from beta discoveries.** <INFERENCE from="Conversation/camera groundwork lacks a shipping contract">Revisit assistant projection, arbitrary Live Activities and native apps when Apple publishes support or shipping behavior is demonstrated.</INFERENCE> **Medium confidence.**

🌱 graft saved ~113k tokens this turn, 1 call.
