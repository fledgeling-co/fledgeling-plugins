I’ll verify the HomeView and iOS 27 premises against Apple’s sources first, then separate documented APIs from unverified claims so the build and submission plan doesn’t depend on assumed platform support.Apple confirms the paired-iPhone audio/video route to HomeView. The key complications are documentation conflicts: the current entitlement pages prohibit combining audio and video, while WWDC26 recommends both; widget disfavoring is not documented as a reliable hide switch. I also found an explicit video navigation-depth limit in the current API reference, despite its omission from the guide’s depth summary.## Executive Summary

- **(High Confidence) Build an iPhone integration, not a separate HomeView app.** **[Apple-documented]** Apple supports CarPlay audio and video apps on HomeView through an app running on a paired iPhone. Widgets are a separate route and do not require the containing app to qualify as a CarPlay media app. [developer.apple.com](https://developer.apple.com/carplay/) [developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) ([developer.apple.com](https://developer.apple.com/carplay/))

- **(High Confidence) Choose the entitlement that matches the app’s primary purpose.** **[Apple-documented]** Use audio for a genuine audio service, video for a primarily video service, and voice-based conversation for a conversational assistant. Voice-based conversation starts with iOS 26.4; the video-app entitlement starts with iOS 27. Do not apply for audio merely to get an unrelated app onto HomeView. [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation.md) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md) ([developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text))

- **(High Confidence) Do not ship combined audio and video entitlements without written clarification from Apple.** **[Apple-documented conflict]** WWDC26 recommends combining them, but the current entitlement reference pages prohibit combining either with another CarPlay entitlement. The audio entitlement itself explicitly permits audio-only content and video with an audio component. [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/))

- **(High Confidence) Treat widgets as potentially household-visible, not automatically private.** **[Apple-documented]** HomeView’s shared Modular face can contain widgets from different household members and displays their information to everyone. `disfavoredLocations` is not a documented security boundary or reliable exclusion mechanism; its effect on HomeView is unresolved. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) [developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets))

- **(High Confidence) Use physical iPhones for current CarPlay development and real HomeView hardware for acceptance testing.** **[Apple-documented]** Current CarPlay Simulator runs through Device Hub with a USB-connected iPhone; Xcode 27.2 explicitly says iOS Simulator is not supported for CarPlay. A simulated car is not a HomeView simulator. [developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md) [developer.apple.com](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes.md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md))

- **(Medium Confidence) HomeView’s conversational-app roadmap is real code evidence, not a shipping contract.** **[Developer-observed; future support rumoured]** Firmware research identifies an unused `ConversationalApps` flag and an iOS 27.3 beta category string, “Conversational Apps,” with audio/session groundwork. Apple has not thereby announced a public HomeView conversational-app API or release date. [pdfu.dev](https://pdfu.dev/) [github.com](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md?plain=1) ([pdfu.dev](https://pdfu.dev/))

- **(High Confidence) One previously unresolved limit is now explicit: video apps have a maximum stack depth of five, including the root.** **[Apple-documented]** This appears in the current `pushTemplate` reference even though the guide’s depth summary omits video. [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md))

## Detailed Findings

**Research cutoff: November 17, 2026.**

**Evidence notation:** **A/H** = Apple-documented, High confidence; **A/M** = Apple evidence with incomplete scope, Medium confidence; **D/M** or **D/L** = developer-observed, Medium or Low confidence; **R/L** = rumoured future availability, Low confidence. Undated live documentation below was checked at the cutoff; its publication date is not invented. Recommendations and original code are explicitly identified as synthesis.

### 1. Platform surface: which categories, entitlements, templates, depths, Ultra features, and HomeView routes exist?

#### Verification of the four premises

| Premise | Finding |
|---|---|
| HomeView went on sale November 13, 2026 | **Confirmed — A/H.** Apple’s availability announcement is dated November 13, 2026. [apple.com](https://www.apple.com/newsroom/2026/11/apple-homeview-available-today/) ([apple.com](https://www.apple.com/newsroom/2026/11/apple-homeview-available-today/)) |
| It runs HomeView Software 27.2, build 24V526, derived from tvOS | **Split the claim.** The software name, version and build are **A/H**, published November 12, 2026. The tvOS lineage is **D/M**, supported by developers inspecting/virtualizing the firmware—not an Apple promise that a tvOS target is supported. [developer.apple.com](https://developer.apple.com/news/releases/?id=11122026a) [mastodon.social](https://mastodon.social/@stroughtonsmith/117532557440780934) [fedi.ml](https://fedi.ml/profile/pvagner) ([developer.apple.com](https://developer.apple.com/news/releases/?id=11122026a)) |
| No HomeView SDK, App Store, simulator or design kit at launch | **Substantially correct, but not all four negatives have an explicit Apple statement.** **A/M:** Apple’s supported SDK inventory has no HomeView SDK; its documented development routes are CarPlay and widgets. **D/M:** firmware inspection found no App Store. No public dedicated simulator/design kit was established in this investigation. **Correction:** Apple *does* publish HomeView-specific widget design guidance. [developer.apple.com](https://developer.apple.com/xcode/system-requirements/) [developer.apple.com](https://developer.apple.com/carplay/) [reddit.com](https://www.reddit.com/r/HomeKit/comments/1xv7m8k/some_findings_after_digging_through_homeviews_ipsw/) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) ([developer.apple.com](https://developer.apple.com/xcode/system-requirements/)) |
| Third-party app UI comes from paired-iPhone CarPlay audio/video apps, plus small widgets | **Confirmed for these documented routes — A/H.** Agreement §6.4.2 authorizes eligible CarPlay applications while running on a paired iOS device; Apple identifies audio/video as supported categories. §6.4.1 separately covers widgets. The agreement itself does **not** enumerate the categories or widget sizes; those details come from documentation/HIG. [developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) [developer.apple.com](https://developer.apple.com/carplay/) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) ([developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)) |
| iOS 27.3 beta adds `ConversationalApps` to the bridge | **Partly correct — D/M.** Research posted November 1 and updated November 4 distinguishes the pre-existing unused `PebblePlay/ConversationalApps` flag from the beta’s added human-readable **“Conversational Apps”** category. The raw diff corroborates the latter string. **R/L:** interpreting this as future third-party assistant support is reasonable but unannounced. [pdfu.dev](https://pdfu.dev/) [github.com](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md?plain=1) ([pdfu.dev](https://pdfu.dev/)) |

<MISSING_DATA>No explicit Apple document was located collectively declaring “no HomeView SDK, App Store, simulator or design kit.” Absence from the public tooling inventory is not a permanent platform commitment.</MISSING_DATA>

#### Capability matrix

**A/H unless flagged.** Entitlements below use the prefix **`com.apple.developer.carplay-`** followed by the displayed suffix. Category/template compatibility comes from Apple’s current initial-interface article; historical version qualifications come from the October 13, 2026 guide. [developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md) [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) ([developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md))

**Template legend**

- **B** = `CPActionSheetTemplate`, `CPAlertTemplate`, `CPGridTemplate`, `CPListTemplate`, `CPTabBarTemplate`
- **C** = `CPContactTemplate`; **I** = `CPInformationTemplate`; **M** = `CPMapTemplate`
- **N** = `CPNowPlayingTemplate`; **P** = `CPPointOfInterestTemplate`
- **S** = `CPSearchTemplate`; **V** = `CPVoiceControlTemplate`

| CarPlay category | iOS 26.x: entitlement; templates | iOS 27.0–27.3 beta: entitlement; templates | HomeView app UI |
|---|---|---|---|
| Audio | `audio`; B,N | `audio`; B,N,S,V | Supported: `audio`; paired-iPhone media interface |
| Communication | `communication`; B,C,I,N | `communication`; B,C,I,N,V | Not an Apple-listed app category |
| Navigation | `maps`; B,C,I,M,S,V | `maps`; B,C,I,M,S,V | Not an Apple-listed app category |
| EV charging | `charging`; B,I,P | `charging`; B,I,P,S,V | Not an Apple-listed app category |
| Parking | `parking`; B,I,P | `parking`; B,I,P,S,V | Not an Apple-listed app category |
| Fueling | `fueling`; B,I,P | `fueling`; B,I,P,S,V | Not an Apple-listed app category |
| Quick food ordering | `quick-ordering`; B,I,P | `quick-ordering`; B,I,P,V | Not an Apple-listed app category |
| Driving task | `driving-task`; B,I,P; V from 26.4 | `driving-task`; B,I,P,V | Not an Apple-listed app category |
| Public safety | `public-safety`; B,C†,I,N,P | `public-safety`; B,C†,I,N,P,S,V | Not an Apple-listed app category |
| Voice-based conversation | From 26.4: `voice-based-conversation`; B,I,P,V | `voice-based-conversation`; B,I,P,V | Unannounced; beta-code evidence only |
| Video | No video-app entitlement | `video`; B,N,S,V | Supported: `video`; paired-iPhone media interface |

**Matrix attribution:** every CarPlay template set above is **Apple-documented** in the cited compatibility tables; HomeView category eligibility is **Apple-documented** in Apple’s developer overview and entitlement references. [developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md) [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) [developer.apple.com](https://developer.apple.com/carplay/) ([developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md))

**† Public-safety conflict — A/M.** The compatibility tables permit Contact; the `CPContactTemplate` reference still says communication/navigation only. Treat Contact in a public-safety implementation as requiring clarification and device validation. [developer.apple.com](https://developer.apple.com/documentation/carplay/cpcontacttemplate.md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpcontacttemplate.md))

<INFERENCE from="Apple's audio/video HomeView compatibility statement and CarPlay entitlement-controlled template tables">HomeView reuses the eligible app’s template-based media implementation. This does not establish identical behavior for every template, input method, voice feature, or vehicle-specific capability on HomeView.</INFERENCE>

**Widgets remain independent of this table.** An app in an unsupported HomeView app category can still supply an eligible small widget; “not listed” above does not mean its widgets are excluded. **A/H.** [developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) ([developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/))

#### Navigation-depth limits

**A/H; includes the root.** The current API reference explicitly provides the following limits. [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md))

| Category | Maximum depth |
|---|---:|
| Audio, communication, EV charging, parking, public safety, navigation | 5 |
| Video | 5 |
| Fueling, voice-based conversation | 3 |
| Driving task, quick food ordering: iOS 26.3 and earlier | 2 |
| Driving task, quick food ordering: iOS 26.4 and later | 3 |

All numeric entries: [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md).

**A/H:** a tab bar must be installed as the root, and its selected tab has its own navigation hierarchy. Template eligibility does not mean every template can be pushed, presented modally, or used as a tab child. [developer.apple.com](https://developer.apple.com/documentation/carplay/cptabbartemplate.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/presenttemplate(_:animated:completion:).md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cptabbartemplate.md))

#### What CarPlay Ultra changes

**A/H:** third-party apps still use CarPlay framework integration; Ultra is not a general-purpose alternative UI SDK. Navigation can participate in supported dashboard/instrument-cluster experiences, while automaker-specific vehicle controls are a separate integration. [developer.apple.com](https://developer.apple.com/carplay/) [developer.apple.com](https://developer.apple.com/documentation/carplay/integrating-carplay-with-your-navigation-app) ([developer.apple.com](https://developer.apple.com/carplay/))

**A/H:** the relevant recent progression is:

| Version | Material change |
|---|---|
| iOS 26 | System-updated appearance, Smart Display Zoom, widgets and Live Activities |
| iOS 26.4 | Conversational-app entitlement; route-sharing support on compatible vehicles |
| iOS 27 | Video-app browsing, expanded template eligibility, richer media lists, MiniPlayer, general-purpose navigation panels |

[developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/?time=605) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation.md) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/?time=605))

<MISSING_DATA>No additional publicly announced CarPlay app category beyond the matrix was established for iOS 27.1, 27.2 or 27.3 beta. Private symbols are not additional public categories.</MISSING_DATA>

### 2. UI and UX: which HIG rules and template limits should the team implement?

#### HIG-backed rules

The following are **A/H**, except where an implementation recommendation is explicitly marked.

| Rule | Required design treatment | HIG source |
|---|---|---|
| Minimize driver attention | Short, high-value flows; scannable content; no decorative clutter | CarPlay HIG, live/undated. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) |
| Do not require phone handling | Finish setup before driving; show errors in CarPlay; support locked-phone operation | CarPlay HIG. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) |
| Respect audio ownership | Do not seize the audio session at launch; start playback promptly after selection; resume interruptions only when appropriate | CarPlay HIG. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) |
| Support environmental appearance | Test daylight, darkness and changing light; preserve actionable contrast | CarPlay HIG. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) |
| Make widgets distance-readable | Large text, glanceable information, removable backgrounds; do not depend on rich imagery/color alone | Widgets HIG, updated October 13, 2026. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Design HomeView’s shared face as shared | A household has one Modular face, holding up to four widgets; a member’s widget data can be visible to everyone | Widgets HIG, October 13, 2026. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Support widget rendering variants | HomeView Home Screen appearances and background-free Modular presentation; monochromatic red treatment in low light | Widgets HIG, October 13, 2026. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Use Live Activities for bounded ongoing events | Show timely progress, not an indefinitely refreshed replacement for an app; adapt layouts to the presentation | Live Activities HIG, updated October 13, 2026. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/live-activities.md) |

HIG evidence: ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md))

**Liquid Glass — A/H:** iOS 26 updates template appearance automatically. Apple specifically advises checking map/bar-button images against Liquid Glass. Do not recreate the system material inside artwork or attempt to replace template chrome with custom SwiftUI controls. The final sentence is an implementation recommendation derived from system-rendered templates. [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/?time=605) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/?time=605))

#### Numeric limits: query APIs, do not hardcode assumptions

| Surface | Documented constraint |
|---|---|
| Lists | Query `CPListTemplate.maximumItemCount` and `maximumSectionCount`; excess content can be discarded. Vehicle restrictions can change the effective allowance. **A/H.** [developer.apple.com](https://developer.apple.com/documentation/carplay/cplisttemplate.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cplisttemplate/maximumitemcount.md) |
| Restricted list presentation | Be prepared for only **12** items. **A/H**, October 2026 guide. [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) |
| Tabs | Query `CPTabBarTemplate.maximumTabCount`. The guide currently describes **4** for audio and **5** for other categories, explicitly warning these may change. **A/H.** [developer.apple.com](https://developer.apple.com/documentation/carplay/cptabbartemplate/maximumtabcount.md) [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) |
| Grid | Only the first **8** buttons appear. **A/H.** [developer.apple.com](https://developer.apple.com/documentation/carplay/cpgridtemplate?language=objc%2Cobjc) |
| Voice navigation bar | The trailing region displays at most **2** buttons; availability begins at iOS **26.4**. **A/H.** [developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate/trailingnavigationbarbuttons.md) |
| Navigation stacks | Apply the category-specific limits above, including the root. **A/H.** [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md) |

([developer.apple.com](https://developer.apple.com/documentation/carplay/cplisttemplate.md))

**Category-specific refresh limits — A/H:** driving-task data must not be periodically refreshed more than **“once every 10 seconds”**; POIs more than **“once every 60 seconds.”** Quick-food ordering is a simplified recent/favorites flow, not a full restaurant menu. [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) ([developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text))

#### Voice, widgets and Live Activities

- **A/H:** App Intents expose actions to Siri/Shortcuts and power widget buttons/toggles. Media actions should use `AudioPlaybackIntent`; this causes execution in the app process rather than the widget extension. [developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities) [developer.apple.com](https://developer.apple.com/documentation/appintents/audioplaybackintent?changes=lat_3_1__1&language=objc) ([developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities))
- **A/H:** communication eligibility still involves SiriKit messaging/calling support; adding generic App Intents is not a substitute for that category’s requirements. [developer.apple.com](https://developer.apple.com/documentation/sirikit/messaging.md) [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) ([developer.apple.com](https://developer.apple.com/documentation/sirikit/messaging.md))
- **A/H:** touchscreen CarPlay widgets can perform supported actions; launching the containing app requires CarPlay integration. Non-touchscreen behavior is more limited. [developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md) ([developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md))
- **A/H:** CarPlay Live Activities use the compact presentation by default; `.supplementalActivityFamilies([.small])` enables a custom small layout shared with the Apple Watch presentation. [developer.apple.com](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities) ([developer.apple.com](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities))
- **A/M:** Apple describes HomeView system Live Activities, but this does not establish automatic display of arbitrary third-party ActivityKit activities. See the explicit answer in question 7(e). [apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/) ([apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/))

<INFERENCE from="Widgets HIG shared-Modular-face behavior and the lack of a documented HomeView-specific exclusion control">Use explicitly household-safe widget content by default. Do not rely on recognition, redaction, or widget disfavoring to prevent disclosure unless that exact behavior has been documented and tested.</INFERENCE>

### 3. Code: what native Swift API shape should the team use?

#### Architecture and lifecycle

**A/H:** CarPlay is an additional scene of the existing iOS application. The scene delegate is `@MainActor`; non-navigation apps receive `templateApplicationScene(_:didConnect:)`, and Apple requires installing a root before that callback returns. [developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate/templateapplicationscene(_:didconnect:).md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md))

<INFERENCE from="CarPlay's scene-based launch and SwiftUI UIApplicationDelegateAdaptor documentation">Keep shared services independent of the phone view hierarchy. A CarPlay-only cold launch must not depend on a phone window, `ContentView.onAppear`, a selected SwiftUI tab, or a phone-only environment object having initialized playback/account state.</INFERENCE> [developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md) [developer.apple.com](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md))

**A/H:** SwiftUI can retain the iPhone lifecycle through `UIApplicationDelegateAdaptor`. The CarPlay UI itself uses native `CPTemplate` objects; this is not mirroring an arbitrary SwiftUI view tree. [developer.apple.com](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md))

#### Common lifecycle and manifest

**Original synthesis from Apple APIs; confidence Medium until built in the team’s project.** Include the common file plus **either** audio **or** conversational implementation below—not both entitlement examples in a single target.

<MISSING_DATA>I cannot run Xcode here. These are SDK-27-oriented, compile-intended skeletons using verified public declarations, not a claim of an executed successful build. The conversational example intentionally omits the team’s speech/model transport.</MISSING_DATA>

```swift
import SwiftUI
import UIKit

@main
@MainActor
struct ExistingApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self)
    private var appDelegate

    var body: some Scene {
        WindowGroup {
            Text("Existing SwiftUI interface")
        }
    }
}

@MainActor
final class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions options:
            [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        bootstrapCarServices()
        return true
    }
}
```

**A/H API basis:** [developer.apple.com](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md). ([developer.apple.com](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md))

Merge the following into the existing scene manifest. Preserve existing phone-scene configuration and any existing app-delegate scene-routing logic; do not replace it with a new phone delegate accidentally.

```xml
<key>UIApplicationSceneManifest</key>
<dict>
    <key>UIApplicationSupportsMultipleScenes</key>
    <true/>
    <key>UISceneConfigurations</key>
    <dict>
        <!-- Preserve existing iPhone scene entries here. -->

        <key>CPTemplateApplicationSceneSessionRoleApplication</key>
        <array>
            <dict>
                <key>UISceneClassName</key>
                <string>CPTemplateApplicationScene</string>
                <key>UISceneConfigurationName</key>
                <string>CarPlay</string>
                <key>UISceneDelegateClassName</key>
                <string>$(PRODUCT_MODULE_NAME).CarSceneDelegate</string>
            </dict>
        </array>
    </dict>
</dict>
```

**A/H API basis:** [developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md). ([developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md))

#### (a) Minimal audio implementation

**Configuration:** use the approved `com.apple.developer.carplay-audio` entitlement and the Audio background mode where the app actually supports background playback. `CPNowPlayingTemplate` gets content/control behavior from the playback frameworks, not from assigning arbitrary labels to the template. **A/H.** [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cpnowplayingtemplate.md) ([developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md))

```swift
import AVFoundation
import CarPlay
import MediaPlayer

@MainActor
func bootstrapCarServices() {
    _ = AudioPlayback.shared
}

@MainActor
final class AudioPlayback {
    static let shared = AudioPlayback()

    private var player: AVAudioPlayer?
    private var commandTokens: [Any] = []

    private init() {
        let commands = MPRemoteCommandCenter.shared()
        commands.playCommand.isEnabled = true
        commands.pauseCommand.isEnabled = true

        commandTokens.append(
            commands.playCommand.addTarget { @Sendable _ in
                Task { @MainActor in
                    _ = AudioPlayback.shared.play()
                }
                return .success
            }
        )
        commandTokens.append(
            commands.pauseCommand.addTarget { @Sendable _ in
                Task { @MainActor in
                    AudioPlayback.shared.pause()
                }
                return .success
            }
        )
    }

    @discardableResult
    func play() -> Bool {
        do {
            if player == nil {
                guard let url = Bundle.main.url(
                    forResource: "sample",
                    withExtension: "m4a"
                ) else {
                    return false
                }
                player = try AVAudioPlayer(contentsOf: url)
            }

            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .default)
            try session.setActive(true)

            guard player?.play() == true else { return false }
            publish(rate: 1)
            return true
        } catch {
            print("Playback failed:", error)
            return false
        }
    }

    func pause() {
        player?.pause()
        publish(rate: 0)
        try? AVAudioSession.sharedInstance().setActive(
            false,
            options: .notifyOthersOnDeactivation
        )
    }

    private func publish(rate: Double) {
        MPNowPlayingInfoCenter.default().nowPlayingInfo = [
            MPMediaItemPropertyTitle: "Sample",
            MPMediaItemPropertyPlaybackDuration: player?.duration ?? 0,
            MPNowPlayingInfoPropertyElapsedPlaybackTime:
                player?.currentTime ?? 0,
            MPNowPlayingInfoPropertyPlaybackRate: rate
        ]
    }
}

@MainActor
final class CarSceneDelegate:
    NSObject, CPTemplateApplicationSceneDelegate {

    private var controller: CPInterfaceController?

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didConnect interfaceController: CPInterfaceController
    ) {
        controller = interfaceController
        _ = AudioPlayback.shared

        let item = CPListItem(text: "Play sample", detailText: nil)
        item.handler = { [weak self] _, finished in
            defer { finished() }
            guard AudioPlayback.shared.play() else { return }

            self?.controller?.pushTemplate(
                CPNowPlayingTemplate.shared,
                animated: true,
                completion: { _, error in
                    if let error { print(error) }
                }
            )
        }

        let root = CPListTemplate(
            title: "Audio",
            sections: [CPListSection(items: [item])]
        )
        interfaceController.setRootTemplate(
            root,
            animated: false,
            completion: { _, error in
                if let error { print(error) }
            }
        )
    }

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didDisconnectInterfaceController interfaceController:
            CPInterfaceController
    ) {
        controller = nil
    }
}
```

**Verified API basis — A/H:** Now Playing metadata, remote-command registration, list-item completion handling, and the current non-navigation disconnect selector. [developer.apple.com](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter.md) [developer.apple.com](https://developer.apple.com/documentation/mediaplayer/mpremotecommand/addtarget(handler:).md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cplistitem/handler.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate/templateapplicationscene(_:diddisconnectinterfacecontroller:).md) ([developer.apple.com](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter.md))

**Implementation limits:** bundle a licensed `sample.m4a`. Replace the sample player with the existing playback engine; add artwork, queue/seek support, readiness/buffering state, interruption handling and end-of-item updates. Remote callbacks above synchronously acknowledge an enqueued request; production command eligibility/status must reflect actual available content.

#### (b) Minimal voice-based conversational implementation

**A/H:** the entitlement starts at iOS 26.4. Apple recommends `.playAndRecord`, `.default`, and no mixing for conversational audio. Microphone consent and a usage description remain required. [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation.md) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) [developer.apple.com](https://developer.apple.com/documentation/avfaudio/avaudioapplication/requestrecordpermission(completionhandler:).md) ([developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation.md))

This version uses a list root and the explicitly documented modal voice presentation, avoiding reliance on the root-template ambiguity discussed later.

```swift
import AVFoundation
import CarPlay
import UIKit

@MainActor
func bootstrapCarServices() {}

@available(iOS 26.4, *)
@MainActor
final class CarSceneDelegate:
    NSObject, CPTemplateApplicationSceneDelegate {

    private var controller: CPInterfaceController?
    private var voice: CPVoiceControlTemplate?

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didConnect interfaceController: CPInterfaceController
    ) {
        controller = interfaceController

        let talk = CPListItem(text: "Talk", detailText: nil)
        talk.handler = { [weak self] _, finished in
            finished()
            self?.presentConversation()
        }

        let root = CPListTemplate(
            title: "Assistant",
            sections: [CPListSection(items: [talk])]
        )

        interfaceController.setRootTemplate(
            root,
            animated: false
        ) { [weak self] installed, error in
            if let error { print(error) }
            if installed { self?.presentConversation() }
        }
    }

    private func presentConversation() {
        guard let controller,
              controller.presentedTemplate == nil else { return }

        let ready = CPVoiceControlState(
            identifier: "ready",
            titleVariants: ["Ready"],
            image: UIImage(systemName: "mic.fill")!,
            repeats: false
        )
        let unavailable = CPVoiceControlState(
            identifier: "unavailable",
            titleVariants: ["Microphone unavailable"],
            image: UIImage(systemName: "mic.slash.fill")!,
            repeats: false
        )

        let template = CPVoiceControlTemplate(
            voiceControlStates: [ready, unavailable]
        )
        template.trailingNavigationBarButtons = [
            CPBarButton(title: "End") { [weak self] _ in
                self?.endConversation()
            }
        ]
        voice = template

        controller.presentTemplate(
            template,
            animated: false
        ) { [weak self] presented, error in
            if let error { print(error) }
            if presented { self?.beginAudio() }
        }
    }

    private func beginAudio() {
        guard AVAudioApplication.shared.recordPermission == .granted else {
            voice?.activateVoiceControlState(
                withIdentifier: "unavailable"
            )
            return
        }

        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(
                .playAndRecord,
                mode: .default,
                options: []
            )
            try session.setActive(true)

            // Connect the app's speech/model transport here.
            // Show "Listening" only after real input is running.
            // Add processing/speaking states for the actual engine.
            voice?.activateVoiceControlState(withIdentifier: "ready")
        } catch {
            print("Conversation audio failed:", error)
            stopAudio()
            voice?.activateVoiceControlState(
                withIdentifier: "unavailable"
            )
        }
    }

    private func stopAudio() {
        // Cancel capture, model/network work and speech output here.
        try? AVAudioSession.sharedInstance().setActive(
            false,
            options: .notifyOthersOnDeactivation
        )
    }

    private func endConversation() {
        stopAudio()
        if controller?.presentedTemplate != nil {
            controller?.dismissTemplate(
                animated: false,
                completion: { _, error in
                    if let error { print(error) }
                }
            )
        }
        voice = nil
    }

    func sceneWillResignActive(_ scene: UIScene) {
        stopAudio()
    }

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didDisconnectInterfaceController interfaceController:
            CPInterfaceController
    ) {
        stopAudio()
        voice = nil
        controller = nil
    }
}
```

**Verified API basis — A/H:** voice states, voice presentation, navigation-bar buttons and current microphone-permission property. [developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontrolstate/init(identifier:titlevariants:image:repeats:).md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/presenttemplate(_:animated:completion:).md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate/trailingnavigationbarbuttons.md) [developer.apple.com](https://developer.apple.com/documentation/avfaudio/avaudioapplication/recordpermission-swift.property.md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate.md))

**Not submission-ready:** this is a scene/audio-session shell, not an implemented conversational service. Add `NSMicrophoneUsageDescription`, obtain permission during safe phone onboarding, implement actual voice responses, handle audio interruptions and modal dismissal, and stop capture when voice interaction ends. Apple’s category requires voice as the primary launch modality and prohibits displaying query-response text/images as a substitute for voice. **A/H.** [developer.apple.com](https://developer.apple.com/documentation/avfaudio/avaudioapplication/requestrecordpermission(completionhandler:).md) [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) ([developer.apple.com](https://developer.apple.com/documentation/avfaudio/avaudioapplication/requestrecordpermission(completionhandler:).md))

#### Video and `CPPlaybackConfiguration`

**A/H:** the exact initializer uses `CMTime`, not `Double`, for elapsed time and duration. The symbol is documented from iOS 26.4 even though the video-app entitlement begins with iOS 27—API availability and category eligibility are separate. [developer.apple.com](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration/init(preferredpresentation:playbackaction:elapsedtime:duration:)) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration.md))

```swift
import CarPlay
import CoreMedia

@available(iOS 26.4, *)
@MainActor
func configureMediaItem(
    _ item: CPListItem,
    session: CPSessionConfiguration
) {
    item.playbackConfiguration = CPPlaybackConfiguration(
        preferredPresentation:
            session.supportsVideoPlayback ? .video : .audio,
        playbackAction: .play,
        elapsedTime: .zero,
        duration: .zero
    )
}
```

**A/H:** this object supplies metadata/system presentation behavior; it does not contain a media URL or replace the playback engine. Use AVFoundation/AVKit and AirPlay-capable playback, with metadata and remote commands. Do not install an arbitrary video view controller as a custom non-navigation CarPlay scene. [developer.apple.com](https://developer.apple.com/documentation/carplay/cpplayableitem.md) [developer.apple.com](https://developer.apple.com/documentation/avkit/avplayerviewcontroller.md) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpplayableitem.md))

**Important correction — A/H:** `supportsVideoPlayback` is a session capability, **not** a parked/moving Boolean. It remains constant during the session; the system can independently suppress video and continue audio. Apple’s engineer confirms automatic transition using the same HLS source. [developer.apple.com](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback.md) [developer.apple.com](https://developer.apple.com/forums/thread/831710) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback.md))

#### App Intents, widgets, ActivityKit, HomeKit and Matter

**A/H API shape:**

```swift
import AppIntents
import Foundation

struct ResumeAudioIntent: AudioPlaybackIntent {
    static var title: LocalizedStringResource { "Resume audio" }

    func perform() async throws -> some IntentResult {
        let started = await MainActor.run {
            AudioPlayback.shared.play()
        }
        guard started else { throw CocoaError(.fileReadUnknown) }
        return .result()
    }
}
```

Expose discoverable phrases through `AppShortcutsProvider`; use app/account authorization appropriate to the action. This does not independently grant CarPlay or HomeView app eligibility. [developer.apple.com](https://developer.apple.com/documentation/appintents/audioplaybackintent?changes=lat_3_1__1&language=objc) [developer.apple.com](https://developer.apple.com/documentation/appintents/appshortcutsprovider.md) ([developer.apple.com](https://developer.apple.com/documentation/appintents/audioplaybackintent?changes=lat_3_1__1&language=objc))

Relevant modifiers on existing configurations are:

```swift
// WidgetConfiguration:
.supportedFamilies([.systemSmall])

// Only when unsuitable for CarPlay; not a HomeView exclusion promise:
.disfavoredLocations([.carPlay], for: [.systemSmall])

// ActivityConfiguration:
.supplementalActivityFamilies([.small])
```

**A/H:** the correct widget modifier includes `for:` families. `WidgetLocation` has no documented HomeView-specific member. Live Activity layouts can branch on `@Environment(\.activityFamily)`. [developer.apple.com](https://developer.apple.com/documentation/swiftui/widgetconfiguration/disfavoredlocations(_:for:)?changes=_8) [developer.apple.com](https://developer.apple.com/documentation/widgetkit/widgetlocation.md) [developer.apple.com](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/widgetconfiguration/disfavoredlocations%28_%3Afor%3A%29?changes=_8))

**A/H:** HomeKit controls/configures home accessories; using it requires the HomeKit entitlement and purpose description. MatterSupport handles adding compatible accessories to an ecosystem, with Matter APIs for commissioning/control. These are accessory integrations—not a HomeView app runtime. [developer.apple.com](https://developer.apple.com/documentation/homekit.md) [developer.apple.com](https://developer.apple.com/documentation/mattersupport.md) ([developer.apple.com](https://developer.apple.com/documentation/homekit.md))

#### Swift 6 strict concurrency

**A/H:** the scene delegate and template UI are main-actor isolated. Remote-command handlers are synchronous callbacks returning `MPRemoteCommandHandlerStatus`; their declaration is not an asynchronous main-actor command interface. [developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md) [developer.apple.com](https://developer.apple.com/documentation/mediaplayer/mpremotecommand/addtarget(handler:).md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md))

<INFERENCE from="MainActor CarPlay declarations, synchronous remote-command handlers, and Swift 6 strict-concurrency guidance">Keep template/coordinator mutation on MainActor; explicitly hop from nonisolated callbacks; avoid capturing command-event objects into asynchronous tasks; register handlers once and retain/remove their tokens according to service lifetime. Do not solve isolation errors with blanket `@unchecked Sendable` or unchecked main-thread assumptions.</INFERENCE> [developer.apple.com](https://developer.apple.com/documentation/swift/adoptingswift6.md) ([developer.apple.com](https://developer.apple.com/documentation/swift/adoptingswift6.md))

### 4. Entitlements and deployment: how should the team obtain approval and submit?

#### Request and signing process

**A/H; current setup documentation:** request the matching category through Apple’s CarPlay contact form, supply organization/app information and accept the terms. After approval, enable the capability on the App ID, regenerate the profile, select it in Xcode and add the matching CarPlay capability. The current article explicitly instructs **manual provisioning**, rather than assuming automatic signing will handle it. [developer.apple.com](https://developer.apple.com/documentation/carplay/preparing-your-ios-app-for-carplay-development.md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/preparing-your-ios-app-for-carplay-development.md))

**A/H:** the guide also requires agreement to the **CarPlay Entitlement Addendum**. [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) ([developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text))

<MISSING_DATA>The authenticated request flow could not be inspected sufficiently to verify the current addendum’s complete clause text/version. Do not substitute an old mirrored addendum or invent clause numbers; archive the exact agreement accepted by the Account Holder.</MISSING_DATA>

**A/H:** verify the signed application and embedded profile, not just the project’s `.entitlements` file. Apple documents these inspection commands: [developer.apple.com](https://developer.apple.com/library/archive/qa/qa1798/_index.html) ([developer.apple.com](https://developer.apple.com/library/archive/qa/qa1798/_index.html))

```sh
codesign -d --entitlements :- "Payload/YourApp.app"
security cms -D -i "Payload/YourApp.app/embedded.mobileprovision"
```

#### Approval timing: reports, not an SLA

**D/L:** a firsthand October 6–9, 2026 discussion reports audio approvals in days, driving-task approvals ranging from roughly 24 hours to 2–3 weeks, navigation within 2 days, and video still pending after a week. One commenter reports an extreme wait exceeding a year. These are anonymous anecdotes, not a defensible expected duration. [reddit.com](https://www.reddit.com/r/CarPlay/comments/1wyuqv5/how_long_does_apple_take_to_approve_carplay/) ([reddit.com](https://www.reddit.com/r/CarPlay/comments/1wyuqv5/how_long_does_apple_take_to_approve_carplay/))

<INFERENCE from="Apple's requirement for approved entitlements before CarPlay execution and the highly variable firsthand approval reports">Request access before committing the delivery date. Make entitlement approval a project dependency, not an assumed final-week administrative task.</INFERENCE>

#### Review rules and rejection risks

**A/H; App Review Guidelines updated October 16, 2026:**

| Relevant section | Shipping implication |
|---|---|
| §2.1 | Complete, stable app; working backend and reviewer access |
| §2.3.1 | Explain the new feature specifically in review notes |
| §2.5.1 | Public APIs used for their intended purposes |
| §2.5.4 | Background services only for legitimate purposes |
| §2.5.11 | Handle Siri/Shortcuts requests directly and accurately |
| §2.5.14 | Explicit recording consent and a clear indication |
| §2.5.17 | Follow Apple’s Matter pairing requirements |
| §5.1 | Privacy/data-handling obligations |
| §5.2.2–5.2.3 | Rights to third-party services and media |

Each legal reference: [developer.apple.com](https://developer.apple.com/app-store/review/guidelines/). ([developer.apple.com](https://developer.apple.com/app-store/review/guidelines/))

**A/H, CarPlay-specific risks:** category misrepresentation; phone-dependent driving flows; message/email bodies or lyrics on the car display; using artwork/templates as arbitrary UI; games/social experiences; conversational response transcripts; and unrelated settings/store-finder functionality under a driving-task entitlement. [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) ([developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text))

**A/M:** no separate public HomeView submission, opt-in entitlement, review lane or HomeView-specific Info.plist key was established. Apple instead says eligible audio/video apps work without modification. This is not proof that Apple will never add such controls. [developer.apple.com](https://developer.apple.com/carplay/) [developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md) ([developer.apple.com](https://developer.apple.com/carplay/))

#### Submission checklist

<INFERENCE from="Apple's entitlement setup, scene, HIG, App Review and testing requirements cited above">

- [ ] Category matches the app’s genuine primary service; no entitlement selected merely as a HomeView workaround.
- [ ] Apple approval recorded; accepted addendum archived; development and distribution profiles regenerated.
- [ ] Signed archive contains the approved entitlement; no unapproved audio/video combination.
- [ ] Existing SwiftUI lifecycle preserved; CarPlay root installed synchronously; cold launch does not depend on phone UI.
- [ ] Locked-phone, interruption, reconnect and offline flows pass.
- [ ] Widget content is safe for a shared household display; unsupported exclusion assumptions removed.
- [ ] Media rights, microphone disclosure, privacy policy and backend/reviewer credentials are complete.
- [ ] TestFlight-installed build passes on actual target hardware.
- [ ] Review notes explain CarPlay category, supported OS versions, video-capable-vehicle requirement and tested HomeView route.
- [ ] No private Pebble/PebblePlay APIs, patched runtimes or firmware flags in the shipping application.

</INFERENCE>

**A/H build-channel distinction:** App Store Connect accepted Xcode 27.2 builds for App Store submission on October 30, 2026; Xcode 27.3 beta 2 uploads became available for internal/external testing on November 16, 2026. Beta testing acceptance is not the same as production submission acceptance. [developer.apple.com](https://developer.apple.com/help/app-store-connect/release-notes/) ([developer.apple.com](https://developer.apple.com/help/app-store-connect/release-notes/))

### 5. Testing before publishing: which tools and concrete acceptance matrix should be used?

#### Tooling reality

| Environment | Reach and limitation |
|---|---|
| **Current CarPlay Simulator** | **A/H:** physical iPhone → Mac → Device Hub → **Device > CarPlay Simulator**. Supports display/environment configurations and simulated controls. [developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md) |
| **Additional Tools for Xcode** | **A/H:** standalone CarPlay Simulator remains a fallback; WWDC26 specifically directs video-app developers to the Additional Tools package. [developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) |
| **Older iOS Simulator path** | **A/H historical:** Apple documented **I/O > External Displays > CarPlay** for older tooling. **A/H current correction:** Xcode 27.2 says iOS Simulator is not supported for CarPlay. Do not make the old path the current CI plan. [developer.apple.com](https://developer.apple.com/documentation/carplay/using-the-carplay-simulator) [developer.apple.com](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes.md) |
| **Aftermarket/OEM hardware** | **A/H:** Apple recommends real vehicle/head-unit testing; wireless CarPlay allows simultaneous wired Xcode debugging. [developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md) |
| **Ultra hardware** | **A/H:** an actual Ultra-equipped OEM vehicle is a separate acceptance environment. Apple’s confirmed initial hardware route was compatible Aston Martin vehicles; confirm the specific vehicle’s installed support rather than inferring from its badge/model year. [apple.com](https://www.apple.com/newsroom/2025/05/carplay-ultra-the-next-generation-of-carplay-begins-rolling-out-today/) |
| **HomeView** | **A/M:** no public simulator established. Use the paired-iPhone implementation for development, then actual HomeView for presentation, pairing, household and audio-route acceptance. [developer.apple.com](https://developer.apple.com/carplay/) |

([developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md))

**XCTest/XCUITest — evidence boundary:** **A/H:** ordinary app logic and iPhone UI can use Apple’s testing frameworks. [developer.apple.com](https://developer.apple.com/support/forums-tags/) ([developer.apple.com](https://developer.apple.com/support/forums-tags/))

<MISSING_DATA>No Apple primary source was found establishing a supported end-to-end XCUITest mechanism for addressing every system-rendered CarPlay template or driving a real head unit/HomeView. Do not claim either universal support or absolute impossibility.</MISSING_DATA>

<INFERENCE from="CarPlay system rendering, separate Simulator presentation and the absence of an established public automation contract">Unit-test domain logic, template construction and navigation policies; automate phone onboarding and intent behavior where supported; retain manual CarPlay/HomeView interaction tests as release gates.</INFERENCE>

**TestFlight — A/H/A/M:** distribute the iOS app through normal TestFlight. External testing requires review and does not waive entitlement requirements. Test the installed distribution build, because local development success does not validate distribution signing. [developer.apple.com](https://developer.apple.com/testflight/) [developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) [developer.apple.com](https://developer.apple.com/documentation/carplay/preparing-your-ios-app-for-carplay-development.md) ([developer.apple.com](https://developer.apple.com/testflight/))

#### Concrete pre-submission test matrix

**Proposed release gates, not claimed empirical results.**

<INFERENCE from="Apple's scene, audio, widget, video-capability, HIG and physical-testing requirements">

| Test area | Configuration | Pass condition |
|---|---|---|
| OS boundaries | Retained iOS 26.0/26.3 devices; 26.4; latest supported 26.x; 27.0/27.1; current production; current beta | Correct category/template gating; no unavailable-API execution |
| Cold launch | Terminated process; launch from CarPlay without opening phone app | Root appears; services initialize; no phone-window dependency |
| Lifecycle | Connect/disconnect, reconnect, scene replacement, process termination | No stale controller, duplicate handlers or leaked microphone session |
| Locked phone | After first unlock and while locked; expired credentials; protected storage unavailable | Primary function succeeds or fails safely in CarPlay |
| Display/input | Small, wide and portrait presets; different scales; touch and rotary controls | Important actions remain reachable; no reliance on touchscreen-only interaction |
| Limits | Runtime list/tab limits; deepest valid navigation path | Required actions survive truncation; stack limits are enforced before pushes |
| Appearance | Day/night transitions, bright sunlight, reduced transparency and relevant accessibility settings | Artwork, symbols and text remain legible |
| Audio | FM/radio active, Siri, incoming call, navigation prompt, route change, network stall | No audio theft at launch; correct pause/resume and metadata |
| Video | Video-capable and audio-only sessions; playback becomes unavailable; leave player | System-controlled video suppression; audio/metadata remain coherent |
| Conversation | Permission denied/granted, interruption, cancellation, slow model response, disconnect | Truthful state indicator; no transcript UI; no capture after session ends |
| Widgets/activities | Small widget, background removed, clear/tinted/red appearances; compact and custom-small activity | Readable content; useful supported actions; no false HomeView Live Activity promise |
| HomeView media | Real HomeView; phone locked, absent/reconnected, app terminated, account expired | Correct discovery, playback, routing and safe failure |
| HomeView privacy | Shared Modular face, personalized Home Screen, another household member/guest present | No unintended personal information exposed visually or audibly |
| Navigation, if applicable | Dashboard/cluster, route sharing and vehicle waypoint requests | Map-only base; correct guidance cancellation and vehicle integration |
| Distribution | Fresh TestFlight install; upgrade from live version | Entitlement-backed discovery and all principal flows work without debugger |

</INFERENCE>

**A/H current-version anchor:** Apple lists iOS 27.2.1 production builds dated November 9, 2026; iOS 27.3 beta 2 and Xcode 27.3 beta 2 are dated November 16, 2026. Record the exact builds actually tested. [developer.apple.com](https://developer.apple.com/news/releases/?id=10262026h) [developer.apple.com](https://developer.apple.com/news/releases/?id=10262026g) ([developer.apple.com](https://developer.apple.com/news/releases/?id=10262026h))

**HomeView without a simulator — D/M:** developers have virtualized the firmware and run experimental native builds, including a SwiftUI watchOS-derived Broadcasts port reported October 31, 2026. These experiments are not an Apple-supported simulator, SDK or App Store distribution route. [mastodon.social](https://mastodon.social/@stroughtonsmith/117536616441953447) [fedi.ml](https://fedi.ml/profile/pvagner) ([mastodon.social](https://mastodon.social/@stroughtonsmith/117536616441953447))

### 6. Gaps and roadmap: what is requested, announced, observed or rumoured?

| Date | Evidence/status | Consequence |
|---|---|---|
| June 2026 | **D/M request; A/H response:** developers asked about captions, speed, controls and fallback in video Now Playing. Apple’s engineer says playback-speed control is unavailable in CarPlay video and invites feedback. [developer.apple.com](https://developer.apple.com/forums/thread/831710) | Do not promise parity with every iPhone/AVKit control |
| October 13, 2026 | **A/H:** Apple announces HomeView and documents audio/video compatibility plus widget guidance. [apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) | Supported launch routes exist without a native HomeView target |
| October 30–31, 2026 | **D/M:** developers demonstrate firmware virtualization/native app experimentation. [mastodon.social](https://mastodon.social/@stroughtonsmith/117532557440780934) [mastodon.social](https://mastodon.social/@stroughtonsmith/117536616441953447) | Evidence of technical possibility, not supported distribution |
| October 31–November 1, 2026 | **D/M observation; R/L roadmap:** pdfu identifies unused HomeKit Secure Video-related HomeView settings/configuration. [pdfu.dev](https://pdfu.dev/) | Do not treat HomeView-as-security-camera or third-party camera APIs as announced |
| November 1; updated November 4, 2026 | **D/M observation; R/L roadmap:** conversational category/audio groundwork in the bridge. [pdfu.dev](https://pdfu.dev/) [github.com](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md?plain=1) | Build the valid CarPlay conversational product, but do not promise HomeView availability |
| November 3, 2026 | **A/H:** Apple opens a Siri AI Developer Preview with iOS 27.3 betas, describing customer availability later and App Store submissions opening “in the spring.” [developer.apple.com](https://developer.apple.com/news/) | Separate this preview from existing shippable App Intents and from a HomeView SDK |
| At cutoff | **A/M:** no public native HomeView SDK release date established | Keep a native port off the committed shipping critical path |

([developer.apple.com](https://developer.apple.com/forums/thread/831710))

**Camera distinction — A/H:** Apple already announces *viewing accessory camera feeds* on HomeView. That is different from exposing HomeView’s own camera as a HomeKit security camera or providing third-party access to its recognition pipeline. [apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/) ([apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/))

<MISSING_DATA>No representative survey or Apple commitment was located quantifying developer demand for a native SDK, separate widget targeting, HomeView UI automation or general third-party Live Activities. These are concrete engineering gaps, not demonstrated industry consensus.</MISSING_DATA>

#### Route comparison and build-versus-buy decision

<INFERENCE from="Documented execution locations, eligible categories, widget behavior and absent native HomeView distribution path">

| Route | Execution/UI surface | Access/license dependency | Principal trade-off | Decision |
|---|---|---|---|---|
| Audio | iPhone service + CarPlay templates + HomeView media UI | Approved audio entitlement/addendum | Broad media route; must genuinely be an audio service | Preferred for existing audio products |
| Video | iPhone playback/AirPlay + template browsing | Approved video entitlement/addendum | Vehicle support/policy gates display | Preferred for primarily video products |
| Conversation | iPhone voice engine + voice template | Approved conversational entitlement | Valid CarPlay product; HomeView unannounced | Ship CarPlay independently |
| Small widget | WidgetKit extension and system presentation | Existing app/widget distribution; no media-category prerequisite | Limited UI and shared-display privacy | Preferred non-media HomeView starting point |
| HomeKit/Matter | Accessory and ecosystem integration | Relevant capabilities, consent and accessory requirements | Controls the home, not arbitrary HomeView UI | Use for genuine smart-home functions |
| Experimental native HomeView port | Unsupported firmware/runtime work | No established public distribution contract | High maintenance and review risk | Research only |

</INFERENCE>

<MISSING_DATA>Apple-published comparative bridge latency, HomeView app execution quotas, entitlement turnaround SLAs and route-specific operating costs were not established. Parameter count/context window are not meaningful comparison dimensions for these platform routes.</MISSING_DATA>

### 7. Open questions: what can now be answered from Apple primary sources?

#### (a) Can one app hold both audio and video entitlements?

**Not safely answerable as an unconditional yes — A/H conflict.**

<CONFLICTING_EVIDENCE>WWDC26 session 212 recommends both for content suitable for audio and video. The current audio and video entitlement pages prohibit combination with other CarPlay entitlements; the October guide allows category combination only for EV charging/fueling.</CONFLICTING_EVIDENCE> [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md) [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md) [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/))

<INFERENCE from="The conflicting Apple instructions and the audio entitlement's explicit permission for video with an audio component">Use one approved category matching the product. For an audio-first service, ask Apple whether the audio entitlement alone covers the intended video experience. Do not add both until Apple resolves the conflict in writing for the app.</INFERENCE>

#### (b) Does `.disfavoredLocations([.carPlay], for: [.systemSmall])` hide the widget on HomeView?

**Unknown; do not rely on it — A/M.** The API describes gallery demotion, and the WidgetKit article explicitly says disfavoring does not exclude a widget. `WidgetLocation` has no documented HomeView-specific member. Neither establishes a cross-device hide effect. [developer.apple.com](https://developer.apple.com/documentation/swiftui/widgetconfiguration/disfavoredlocations(_:for:)?changes=_8) [developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md) [developer.apple.com](https://developer.apple.com/documentation/widgetkit/widgetlocation.md) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/widgetconfiguration/disfavoredlocations%28_%3Afor%3A%29?changes=_8))

<CONFLICTING_EVIDENCE>The CarPlay overview uses stronger “prevent it from being shown” wording, while the detailed WidgetKit documentation describes non-exclusion. That inconsistency does not establish HomeView behavior.</CONFLICTING_EVIDENCE> [developer.apple.com](https://developer.apple.com/carplay/) ([developer.apple.com](https://developer.apple.com/carplay/))

<MISSING_DATA>An Apple statement specifying HomeView propagation and a separate supported HomeView targeting mechanism is still required.</MISSING_DATA>

#### (c) Exact public-safety and navigation template sets?

**The matrix above supplies the guide’s exact sets — A/H for the table, A/M for the conflicting Contact restriction.**

- Public safety gains Search and Voice Control in the iOS 27 compatibility table.
- Navigation already has its listed Contact/Information/Search/Voice Control support in the iOS 26 scope; POI and Now Playing are not permitted by that table.

[developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) [developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md) ([developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text))

<CONFLICTING_EVIDENCE>The Contact reference excludes public safety despite both compatibility tables including it. Do not silently treat that discrepancy as resolved.</CONFLICTING_EVIDENCE> [developer.apple.com](https://developer.apple.com/documentation/carplay/cpcontacttemplate.md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpcontacttemplate.md))

#### (d) Can `CPVoiceControlTemplate` be root from iOS 26.4, or must it be modal?

**A blanket “must be modal” assertion is not supported by current Apple documentation — A/M.** Apple’s initial-interface article says: **“You can install any template as the root template of your interface”**; separately, `presentTemplate` explicitly permits Voice Control modally. [developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md) [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/presenttemplate(_:animated:completion:).md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md))

<INFERENCE from="Apple's general root-template rule and conversational-category Voice Control eligibility from iOS 26.4">The current general documentation permits the root interpretation for an entitled conversational app. However, it is not a Voice-Control-specific, versioned statement proving behavior on every retained iOS 26.4 build.</INFERENCE>

**Shipping decision:** the supplied skeleton uses the explicitly documented modal path. If root Voice Control is important, obtain Apple confirmation and test the minimum supported device build; do not present an old modal-only assumption as authoritative.

#### (e) Do arbitrary third-party Live Activities appear on HomeView?

**Not established — A/M.** Apple’s HomeView announcement mentions system activities such as media, timers and Intercom. The current Live Activities HIG’s automatic cross-device table lists iPhone/iPad, Mac, Apple Watch and CarPlay—not HomeView. [apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/live-activities.md) ([apple.com](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/))

<INSUFFICIENT_EVIDENCE>“HomeView has Live Activities” does not prove that arbitrary third-party ActivityKit activities are forwarded there. Do not advertise that capability without an Apple source and hardware verification.</INSUFFICIENT_EVIDENCE>

#### (f) Maximum navigation depth for video apps?

**Resolved: five templates, including the root — A/H.** The current `pushTemplate(_:animated:completion:)` API table explicitly lists Video. This is stronger evidence than extrapolating from the shared audio/video template column or interpreting the guide’s omission. [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md) ([developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md))

## Evidence Table

Dates marked **undated** mean the live page does not supply a reliable publication date; checked November 17, 2026. The evidence-type column also explains why the source meets the requested discipline.

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---|---|---|
| HomeView launch | Apple Newsroom | Nov. 13, 2026 | First-party release announcement | [apple.com](https://www.apple.com/newsroom/2026/11/apple-homeview-available-today/) |
| HomeView software/build | Apple Developer Releases | Nov. 12, 2026 | First-party release record | [developer.apple.com](https://developer.apple.com/news/releases/?id=11122026a) |
| tvOS lineage/native experiment | Steve Troughton-Smith | Oct. 30–31, 2026 | Original developer observation; not platform authorization | [mastodon.social](https://mastodon.social/@stroughtonsmith/117532557440780934) |
| Paired-device legal route | Apple Developer Program License Agreement | HomeView revision announced Oct. 13, 2026 | Governing first-party agreement | [developer.apple.com](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) |
| Revision date | Apple Developer News | Oct. 13, 2026 | First-party change notice | [developer.apple.com](https://developer.apple.com/news/?id=17mwd36z) |
| Categories/templates/version qualifications | CarPlay Developer Guide | Oct. 13, 2026 | First-party technical/policy specification | [developer.apple.com](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text) |
| Current template table/root rule | Building initial CarPlay interface | Undated | First-party API guidance | [developer.apple.com](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md) |
| All stack limits, including video | `pushTemplate` reference | Undated | Explicit first-party API table | [developer.apple.com](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md) |
| Audio entitlement scope/restriction | Audio entitlement reference | Undated | First-party entitlement contract | [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md) |
| Video availability/restriction | Video entitlement reference | Undated | First-party entitlement contract | [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video.md) |
| Conversational availability | Conversation entitlement reference | Undated | First-party availability metadata | [developer.apple.com](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation.md) |
| WWDC combination recommendation/new features | WWDC26 session 212 | June 2026 | First-party engineering presentation | [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/212/) |
| Liquid Glass/system appearance | WWDC25 session 216 | June 2025 | First-party engineering presentation | [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/216/?time=605) |
| Driving UX | CarPlay HIG | Undated | First-party design requirements | [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/carplay.md) |
| HomeView widgets/shared face/night rendering | Widgets HIG | Updated Oct. 13, 2026 | First-party HomeView design guidance | [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/widgets) |
| Live Activity supported surfaces | Live Activities HIG | Updated Oct. 13, 2026 | First-party cross-device guidance | [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/live-activities.md) |
| Widget disfavoring semantics | WidgetKit/SwiftUI references | Undated | Direct API documentation | [developer.apple.com](https://developer.apple.com/documentation/swiftui/widgetconfiguration/disfavoredlocations(_:for:)?changes=_8) |
| No documented HomeView location member | `WidgetLocation` | Undated | Direct public API inventory | [developer.apple.com](https://developer.apple.com/documentation/widgetkit/widgetlocation.md) |
| Small Live Activity layout | ActivityKit custom-views article | Undated | First-party implementation guidance | [developer.apple.com](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities) |
| Media execution through intents | WidgetKit interactivity article | Undated | First-party process/execution guidance | [developer.apple.com](https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities) |
| Video capability versus temporary policy | `supportsVideoPlayback` | Undated | Direct API semantics | [developer.apple.com](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback.md) |
| Video fallback/speed-control limitations | Apple Frameworks Engineer | June 2026 | Identified Apple staff response | [developer.apple.com](https://developer.apple.com/forums/thread/831710) |
| Approval/signing workflow | CarPlay preparation article | Undated | First-party deployment procedure | [developer.apple.com](https://developer.apple.com/documentation/carplay/preparing-your-ios-app-for-carplay-development.md) |
| Approval timing anecdotes | Requesting developers | Oct. 6–9, 2026 | Firsthand reports; low-confidence timing only | [reddit.com](https://www.reddit.com/r/CarPlay/comments/1wyuqv5/how_long_does_apple_take_to_approve_carplay/) |
| Review rules | App Review Guidelines | Oct. 16, 2026 | Governing first-party review policy | [developer.apple.com](https://developer.apple.com/app-store/review/guidelines/) |
| Current simulator workflow | CarPlay testing article | Undated | First-party testing procedure | [developer.apple.com](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md) |
| USB requirement/no iOS Simulator | Xcode 27.2 Release Notes | Xcode 27.2 release | First-party tool limitation | [developer.apple.com](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes.md) |
| SDK inventory | Xcode system requirements | Live inventory | First-party supported-toolchain list | [developer.apple.com](https://developer.apple.com/xcode/system-requirements/) |
| Beta versus production uploads | App Store Connect release notes | Oct. 30; Nov. 16, 2026 | First-party distribution acceptance record | [developer.apple.com](https://developer.apple.com/help/app-store-connect/release-notes/) |
| Conversational bridge string | blacktop firmware diff | iOS 27.2 → 27.3 beta comparison | Original extracted code artifact; not API documentation | [github.com](https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_2_24B115_vs_27_3_24C5037i/DYLIBS/System/Library/PrivateFrameworks/PebblePlayCore.framework/PebblePlayCore.md?plain=1) |
| Conversational/camera discoveries | pdfu | Oct. 31–Nov. 4, 2026 | Original research report; future behavior unconfirmed | [pdfu.dev](https://pdfu.dev/) |

## Knowledge Gaps

### Conflicting Apple documentation

- **Audio + video combination:** WWDC recommendation conflicts with current entitlement restrictions.
- **Public-safety Contact template:** compatibility tables conflict with the class reference.
- **Widget disfavoring:** overview wording suggests suppression; detailed API guidance describes demotion/non-exclusion.

These are **High-confidence conflicts**, not permission to choose whichever document is more convenient.

### Missing public platform contracts

- HomeView-specific widget targeting or exclusion.
- Automatic forwarding of arbitrary third-party Live Activities.
- A HomeView conversational-app launch commitment.
- Native HomeView app SDK, supported simulator and distribution roadmap.
- An app-facing recognition/identity contract suitable for authorizing private content.

### Missing validation

- Compilation of the supplied skeletons in the team’s exact SDK/project settings.
- Voice-template root behavior on each retained minimum-OS build.
- HomeView behavior across paired-device loss, household transitions and distribution builds.
- Supported end-to-end CarPlay/HomeView UI-automation coverage.

### Missing operational data

<MISSING_DATA>No reliable Apple SLA for entitlement approval, bridge latency benchmark, HomeView-specific execution quota or route-specific cost model was located. Anonymous turnaround reports cannot supply these values.</MISSING_DATA>

## Recommended Next Steps

1. **Obtain a written category ruling before implementation expands.**  
   <INFERENCE from="Conflicting audio/video entitlement instructions and category-specific restrictions">Send Apple the bundle ID, primary user journey, audio/video content mix and desired HomeView behavior. Ask explicitly about combined entitlements, audio-only entitlement video support and any category-specific template discrepancy.</INFERENCE>

2. **Build and sign a minimal vertical slice immediately.**  
   <INFERENCE from="Physical-iPhone development requirements and entitlement/profile dependencies">Integrate the additional scene into the existing SwiftUI app, compile under strict concurrency, install through both development signing and TestFlight, and verify CarPlay-only cold launch before adding catalog complexity.</INFERENCE>

3. **Run a physical HomeView privacy and compatibility investigation.**  
   <INFERENCE from="Shared Modular-face behavior and undocumented HomeView exclusion semantics">Test widget disfavoring, personalized versus shared placements, paired-phone absence, account changes and media routing. Record observed results separately from Apple-guaranteed behavior.</INFERENCE>

4. **Ask Apple narrowly scoped API questions with reproducible projects.**  
   <INFERENCE from="Unresolved Voice Control root behavior, public-safety Contact restrictions and UI-automation coverage">Submit separate questions/feedback for each issue rather than one broad HomeView request. Preserve the OS/Xcode builds and exact entitlement profile with every reproduction.</INFERENCE>

5. **Keep roadmap work behind an uncommitted research track.**  
   <INFERENCE from="Beta conversational/camera code without public shipping contracts">Ship the supported CarPlay/widget product independently. Reassess HomeView conversation, arbitrary Live Activities and native apps only when Apple publishes an actionable SDK or documented availability contract.</INFERENCE>

## Sources

- [CarPlay - Apple Developer](https://developer.apple.com/carplay/)
- [PDF](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf?trk=public_post_comment-text)
- [Rev up your CarPlay app - WWDC26 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2026/212/)
- [Widgets | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/widgets)
- [https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator.md)
- [pdfu](https://pdfu.dev/)
- [https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:).md)
- [Apple HomeView available today - Apple](https://www.apple.com/newsroom/2026/11/apple-homeview-available-today/)
- [HomeView Software 27.2 (24V526) - Releases - Apple Developer](https://developer.apple.com/news/releases/?id=11122026a)
- [SDK and system requirements - Xcode - Apple Developer](https://developer.apple.com/xcode/system-requirements/)
- [Apple Developer Program License Agreement - Agreements and Guidelines - Support - Apple Developer](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)
- [https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface.md)
- [https://developer.apple.com/documentation/carplay/cpcontacttemplate.md](https://developer.apple.com/documentation/carplay/cpcontacttemplate.md)
- [https://developer.apple.com/documentation/carplay/cptabbartemplate.md](https://developer.apple.com/documentation/carplay/cptabbartemplate.md)
- [Turbocharge your app for CarPlay - WWDC25 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2025/216/?time=605)
- [https://developer.apple.com/design/human-interface-guidelines/carplay.md](https://developer.apple.com/design/human-interface-guidelines/carplay.md)
- [https://developer.apple.com/documentation/carplay/cplisttemplate.md](https://developer.apple.com/documentation/carplay/cplisttemplate.md)
- [Adding interactivity to widgets and Live Activities | Apple Developer Documentation](https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities)
- [https://developer.apple.com/documentation/sirikit/messaging.md](https://developer.apple.com/documentation/sirikit/messaging.md)
- [https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget.md)
- [Creating custom views for Live Activities | Apple Developer Documentation](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities)
- [Meet Apple HomeView, a new way to enjoy entertainment and manage the home - Apple](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/)
- [https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md](https://developer.apple.com/documentation/carplay/cptemplateapplicationscenedelegate.md)
- [https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor.md)
- [https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio.md)
- [https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter.md](https://developer.apple.com/documentation/mediaplayer/mpnowplayinginfocenter.md)
- [https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation.md](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation.md)
- [https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate.md](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate.md)
- [https://developer.apple.com/documentation/avfaudio/avaudioapplication/requestrecordpermission(completionhandler:).md](https://developer.apple.com/documentation/avfaudio/avaudioapplication/requestrecordpermission(completionhandler:).md)
- [https://developer.apple.com/documentation/carplay/cpplaybackconfiguration.md](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration.md)
- [https://developer.apple.com/documentation/carplay/cpplayableitem.md](https://developer.apple.com/documentation/carplay/cpplayableitem.md)
- [https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback.md](https://developer.apple.com/documentation/carplay/cpsessionconfiguration/supportsvideoplayback.md)
- [AudioPlaybackIntent | Apple Developer Documentation](https://developer.apple.com/documentation/appintents/audioplaybackintent?changes=lat_3_1__1&language=objc)
- [disfavoredLocations(_:for:) | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/widgetconfiguration/disfavoredlocations%28_%3Afor%3A%29?changes=_8)
- [https://developer.apple.com/documentation/homekit.md](https://developer.apple.com/documentation/homekit.md)
- [https://developer.apple.com/documentation/swift/adoptingswift6.md](https://developer.apple.com/documentation/swift/adoptingswift6.md)
- [https://developer.apple.com/documentation/carplay/preparing-your-ios-app-for-carplay-development.md](https://developer.apple.com/documentation/carplay/preparing-your-ios-app-for-carplay-development.md)
- [Technical Q&A QA1798: Checking Distribution Entitlements](https://developer.apple.com/library/archive/qa/qa1798/_index.html)
- [How long does Apple take to approve CarPlay access for a developer account?](https://www.reddit.com/r/CarPlay/comments/1wyuqv5/how_long_does_apple_take_to_approve_carplay/)
- [App Review Guidelines - Apple Developer](https://developer.apple.com/app-store/review/guidelines/)
- [App Store Connect - Help - Apple Developer](https://developer.apple.com/help/app-store-connect/release-notes/)
- [Developer Forums Tags - Support - Apple Developer](https://developer.apple.com/support/forums-tags/)
- [TestFlight - Apple Developer](https://developer.apple.com/testflight/)
- [Releases - Apple Developer](https://developer.apple.com/news/releases/?id=10262026h)
- [Steve Troughton-Smith: "Ported the SwiftUI watchOS version of Broadcasts …" - Mastodon.social](https://mastodon.social/@stroughtonsmith/117536616441953447)
- [Video Now Playing View Configurati… | Apple Developer Forums](https://developer.apple.com/forums/thread/831710)
