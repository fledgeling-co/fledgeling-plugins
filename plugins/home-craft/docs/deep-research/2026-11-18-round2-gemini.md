# **Native Swift and SwiftUI Engineering & Policy Playbook: Apple CarPlay and Apple HomeView Across iOS 26 and iOS 27**

For a native Swift and SwiftUI engineering team deciding how to target Apple CarPlay and Apple HomeView (on sale 13 November 2026\) across iOS 26.x and iOS 27.x, the decisive architectural and policy strategy is to apply for a **single** primary CarPlay entitlement—specifically **com.apple.developer.carplay-audio** if your app delivers audio or hybrid audio/video playback, or **com.apple.developer.carplay-voice-based-conversation** (introduced in iOS 26.4) if your app is a voice-first AI assistant—while pairing it with a **WidgetFamily.systemSmall** WidgetKit extension that implements .containerBackground(for: .widget) \[Apple-documented: CarPlay Audio App Entitlement & CarPlay Developer Guide, 2026-10-13; High Confidence\] 1. Because Apple ships no dedicated HomeView SDK, App Store, or simulator at launch, third-party apps reach HomeView's 7-inch Liquid Retina display by streaming from a paired iPhone (iOS 27.2+) or iPad (iPadOS 27.2+) over local Wi-Fi via HomeView's CarPlay bridge daemon (PebblePlay) under Developer Program License Agreement (DPLA) Sections 6.4.1 and 6.4.2 \[Apple-documented: DPLA & Apple HomeView Tech Specs, 2026-10-13 / 2026-11-13; High Confidence\] 5.  
Crucially, you must **not** combine com.apple.developer.carplay-audio and com.apple.developer.carplay-video in the same app binary \[Apple-documented: CarPlay Audio & Video Entitlement Reference, 2026-10-13; High Confidence\] 2. Although WWDC26 Session 212 (June 2026\) verbally recommended including both entitlements for dual-media apps, Apple reversed that policy in iOS 26.3+ and the October 13, 2026 *CarPlay Developer Guide*, forbidding multiple CarPlay entitlements (except EV Charging \+ Fueling) and rejecting dual-entitlement builds under App Store Review Guideline 2.5.1 \[Apple-documented / Developer-observed: CarPlay Developer Guide & Apple Developer Forums, 2026-10-13 / 2026-11-12; High Confidence\] 3. Because com.apple.developer.carplay-audio explicitly permits playing *"audio-only content or video content with an audio component"* (via AirPlay video streaming and CPPlaybackConfiguration) and automatically surfaces on both standard CarPlay vehicles and HomeView, it is the optimal entitlement for any media app that is not strictly video-only \[Apple-documented: CarPlay Audio App Entitlement & CarPlay Developer Guide, 2026-10-13; High Confidence\] 2.  
For teams building voice-based conversational apps, your CarPlay experience can ship immediately on iOS 26.4+ and iOS 27.x using com.apple.developer.carplay-voice-based-conversation and CPVoiceControlTemplate (presented modally or as an iOS 27 overlay via showOverlayTemplate(\_:animated:completion:)) \[Apple-documented: CPInterfaceController Documentation & CarPlay Developer Guide, 2026-10-13; High Confidence\] 1. While conversational apps are excluded from HomeView at its November 13, 2026 launch (HomeView Software 27.2), developer-observed code in iOS 27.3 beta 1 confirms Apple has added the "ConversationalApps" category flag to HomeView's PebblePlay CarPlay bridge alongside bidirectional audio routing groundwork—positioning existing CarPlay conversational apps to surface on HomeView once Apple enables the flag in a subsequent 27.3+ update \[Developer-observed: iOS 27.3 Beta 1 / 9to5Mac, 2026-11-05; High Confidence\] 16.

## **Executive Summary**

* **(High Confidence)** **HomeView OS & Zero-SDK Architecture Verified:** Apple HomeView launched on 13 November 2026 running **HomeView Software 27.2 (build 24V526)**, which internal firmware plists (HomeAccessory17,2) identify as an "Apple TVOS" 27.2 derivative \[Apple-documented / Developer-observed: Apple Releases & Reddit r/HomeKit IPSW Audit, 2026-11-12 / 2026-11-15\] 18. Apple ships no HomeView SDK, App Store, simulator, or design kit; third-party apps run on a paired iPhone (iOS 27.2+) or iPad (iPadOS 27.2+) and project to HomeView via its CarPlay bridge (PebblePlay) if they hold com.apple.developer.carplay-audio or com.apple.developer.carplay-video (DPLA §6.4.2), while WidgetFamily.systemSmall widgets bridge automatically under DPLA §6.4.1 \[Apple-documented: DPLA & CarPlay Developer Guide, 2026-10-13\] 3.  
* **(High Confidence)** **Single-Entitlement Mandate Resolves WWDC26 Conflict:** Despite WWDC26 Session 212 recommending both Audio and Video entitlements for hybrid apps, Apple's October 13, 2026 documentation and iOS 26.3+ runtime rules prohibit combining CarPlay entitlements (except EV Charging \+ Fueling), and App Review rejects dual-entitlement binaries under Guideline 2.5.1 \[Apple-documented / Developer-observed: CarPlay Audio/Video Entitlement Docs & Developer Forums, 2026-10-13 / 2026-11-12\] 2. Hybrid audio/video apps must request **only** com.apple.developer.carplay-audio, which legally and technically permits AirPlay video playback when parked while remaining visible on all CarPlay head units and HomeView \[Apple-documented: CarPlay Audio App Entitlement & CarPlay Developer Guide, 2026-10-13\] 2.  
* **(High Confidence)** **Platform Surface Expansion Across iOS 26.4 and iOS 27.0:** iOS 26.4 introduced the **Voice-Based Conversational** category (com.apple.developer.carplay-voice-based-conversation, max depth 3 templates, Siri exemption), CPPlaybackConfiguration, CPListTemplateDetailsHeader, and route sharing (CPRouteSegment) \[Apple-documented: CarPlay Developer Guide & CPPlaybackConfiguration Docs, 2026-10-13\] 1. iOS 27.0 added the **Video** category (com.apple.developer.carplay-video, max depth 5 templates), automatic Now Playing **MiniPlayer** (allowsMiniPlayer), CPMapPanel for navigation, CPSearchTemplate for audio/video, and expanded CPVoiceControlTemplate (including non-modal overlay presentation via showOverlayTemplate) to all 11 CarPlay categories \[Apple-documented: CarPlay Developer Guide & WWDC26 Session 212, 2026-06 / 2026-10-13\] 3.  
* **(High Confidence)** **iOS 27.3 Beta Unlocks Conversational Apps on HomeView Bridge:** Inspection of iOS 27.3 beta 1 code indicates PebblePlay (HomeView's CarPlay bridge) adds the "ConversationalApps" category (defaults write com.apple.HomeView DefaultAppCategory \-string "ConversationalApps") along with bidirectional audio routing and interruption management, laying the foundation for CarPlay conversational apps (e.g., ChatGPT, Claude, Gemini) to run on HomeView \[Developer-observed: iOS 27.3 Beta 1 / 9to5Mac, 2026-11-05\] 16.  
* **(High Confidence)** **Widget Opt-Out Coupling & Modular Face Requirements:** WidgetKit's .disfavoredLocations(\[.carPlay\], for: \[.systemSmall\]) (WidgetLocation.carPlay, iOS 26.0+) is the sole mechanism to disfavor a widget on both CarPlay and HomeView (grouping it as "not optimized" in Settings); no separate .homeView location exists in Xcode 27.0–27.2 \[Apple-documented / Developer-observed: DPLA §6.4.1 & CarPlay Developer Guide, 2026-10-13\] 3. Widgets on HomeView's **Modular face** (including Night Mode) scale up systemSmall and strip the background, requiring .containerBackground(for: .widget) \[Apple-documented: Widgets HIG, 2026-10-13\] 4.  
* **(High Confidence)** **Swift 6 Concurrency & iOS 27 NowPlaying Framework Transition:** In the iOS 27 SDK, all CPTemplate subclasses and CPPlaybackConfiguration are @MainActor-isolated \[Apple-documented: CPTemplate & CPPlaybackConfiguration Docs, 2026-10\] 12. Furthermore, iOS 27.0 introduces the native Swift NowPlaying framework (MediaSession, MediaPlaybackSnapshot) and MediaIntents (AudioSearch); mixing legacy MPNowPlayingInfoCenter/MPRemoteCommandCenter with the new NowPlaying framework causes undefined behavior, and hybrid MPNowPlayingInfoCenter \+ ApplicationMusicPlayer apps encounter a client-switching freeze (FB24840951) on iOS 27 \[Developer-observed: Apple Developer Forums & Platform APIs Audit, 2026-10 / 2026-11\] 13.  
* **(High Confidence)** **Xcode 27 Device Hub Requires Physical iPhone & Physical HomeView Testing:** Xcode 27 replaced Simulator.app with **Device Hub**, which requires a **physical iPhone connected via USB** to launch CarPlay Simulator (virtual iOS Simulators cannot open a CarPlay display in Device Hub, per forum thread 834440\) \[Apple-documented / Developer-observed: CarPlay Developer Guide & Apple Developer Forums, 2026-10-13 / 2026-11\] 3. Additionally, XCUITest cannot inspect the CarPlay display (AX tree unavailable), and developers report some working CarPlay audio apps hang on an indefinite loading spinner on physical HomeView units—making real HomeView hardware testing essential \[Developer-observed: Apple Developer Forums, 2026-06 / 2026-11-17\] 31.

## **Detailed Findings**

### **Primary Research Question 1: How should a native Swift/SwiftUI iOS team design, build, test and ship apps for Apple CarPlay and for HomeView across iOS 26 and iOS 27, as of November 2026?**

#### **Verification of the Four Context Claims Against Primary Sources**

Before committing engineering resources to an entitlement track or UI architecture, the team must ground its build-versus-buy and operational decisions in verified primary-source facts regarding HomeView's software stack and CarPlay bridge:

| Context Claim to Verify | Verification Status | Primary & Corroborating Evidence (with Source, Date, and Label) |
| :---- | :---- | :---- |
| **1\. HomeView runs "HomeView Software 27.2" (build 24V526), reported as a tvOS 27.2 derivative.** | **Confirmed** (High Confidence) | **Apple-documented:** Apple officially released *HomeView Software Version 27.2* (build 24V526) on November 12, 2026—patching 9 security vulnerabilities ahead of the November 13, 2026 retail launch (following factory software 26.5 and an earlier October 30 build 24V514) 19. **Developer-observed:** Inspection of the signed 24V526 IPSW for HomeAccessory17,2 confirms the OS's internal SystemVersion.plist identifies the platform as "Apple TVOS" 27.2, and the device inherits tvOS 27 bugs (such as a Podcasts feed rendering bug reported Nov 16, 2026\) 16. |
| **2\. Apple ships no HomeView SDK, App Store, simulator, or design kit at launch.** | **Confirmed** (High Confidence) | **Apple-documented / Developer-observed:** As of November 18, 2026 (across Xcode 27.0, 27.1, and 27.2 beta 1), Apple provides no dedicated HomeView SDK, no HomeView runtime or simulator in Xcode 27 Device Hub, no on-device App Store (HomeView ships with 14 built-in apps plus Settings), and no HomeView design kit (Apple's October 2026 design kits cover iOS/iPadOS 27, macOS 27, tvOS 18, watchOS 26, and visionOS 26 only) 8. |
| **3\. Third-party apps reach HomeView from a paired iPhone only if they hold the CarPlay audio or video entitlement (DPLA §§6.4.1 & 6.4.2), plus systemSmall widgets.** | **Confirmed (with iPad & Fallback Nuances)** (High Confidence) | **Apple-documented:** Under DPLA Section 6.4.2 (revised October 13, 2026\) and Footnote \*2 of the October 13, 2026 *CarPlay Developer Guide*, full third-party CarPlay apps surface on HomeView while running on a paired iPhone (iOS 27.2+) **or iPad (iPadOS 27.2+)** only if they hold com.apple.developer.carplay-audio or com.apple.developer.carplay-video 2. Under DPLA Section 6.4.1 and the Widgets HIG, any iOS/iPadOS app's WidgetFamily.systemSmall widget surfaces on HomeView's Home Screen and Modular face unless disfavored via .disfavoredLocations(\[.carPlay\]) 6. Non-native fallbacks include AirPlay, Proximity Handoff, and built-in Safari 38. |
| **4\. iOS 27.3 beta code adds a "ConversationalApps" string to HomeView's CarPlay bridge.** | **Confirmed** (High Confidence) | **Developer-observed:** Discovered by researcher pdfu in iOS 27.3 beta 1 (released November 3, 2026; reported November 5, 2026), HomeView's CarPlay bridge daemon **PebblePlay** adds the "ConversationalApps" category (defaults write com.apple.HomeView DefaultAppCategory \-string "ConversationalApps") along with bidirectional audio routing, session management, and interruption groundwork, though the feature is not yet wired up for end users 7. |

#### **1\. Platform Surface: CarPlay Categories, Entitlements, Templates, Max Depth, CarPlay Ultra, and HomeView Bridging (iOS 26.0–27.3 Beta)**

Across iOS 26.0–26.x and iOS 27.0–27.3 beta, Apple's CarPlay framework governs **11 active third-party app categories**, alongside two deprecated legacy entitlements (com.apple.developer.playable-content and com.apple.developer.carplay-messaging, both deprecated after iOS 14.0) \[Apple-documented: Apple Developer Entitlements Documentation, 2026-10-13; High Confidence\] 40. Every category is restricted to an explicit allowlist of the 12 system-rendered CPTemplate subclasses and a hard navigation hierarchy depth (which always counts the root template as level 1); attempting to push an unpermitted template or exceed the category's depth limit triggers an exception at runtime \[Apple-documented: CarPlay Developer Guide, 2026-10-13; High Confidence\] 3.  
Between June 2025 (iOS 26 announcement) and November 2026 (iOS 27.2 shipping and iOS 27.3 beta), Apple expanded the CarPlay platform surface across three distinct milestones. First, **iOS 26.0** brought WidgetFamily.systemSmall widgets (WidgetLocation.carPlay) and ActivityFamily.small Live Activities (.supplementalActivityFamilies(\[.small\])) from CarPlay Ultra to all standard CarPlay vehicles \[Apple-documented: CarPlay Developer Guide & WidgetKit Docs, 2026-10-13; High Confidence\] 3. Second, **iOS 26.4** (February 2026\) introduced the **Voice-Based Conversational** app category (com.apple.developer.carplay-voice-based-conversation)—the first new CarPlay category since iOS 16—enabling third-party AI voice assistants (such as ChatGPT, Claude, and Google Gemini Live) to operate in CarPlay without routing through Siri \[Apple-documented / Developer-observed: CarPlay Developer Guide & MacRumors / iDropNews, 2026-02-18 / 2026-10-13; High Confidence\] 1. iOS 26.4 simultaneously expanded the maximum template depth of **Driving Task** and **Quick Food Ordering** apps from 2 to **3 templates**, added action buttons to CPVoiceControlState, introduced CPPlaybackConfiguration and CPListTemplateDetailsHeader, enabled AirPlay video in the car, and added vehicle route sharing (CPRouteSegment, CPNavigationWaypoint) \[Apple-documented: CarPlay Developer Guide & CPPlaybackConfiguration Docs, 2026-10-13; High Confidence\] 3. Third, **iOS 27.0–27.2** (September–November 2026\) and **iOS 27.3 beta** added the native **Video** app category (com.apple.developer.carplay-video) for parked-vehicle playback and HomeView streaming, expanded CPVoiceControlTemplate to **all** CarPlay categories, added non-modal overlay presentation (CPInterfaceController.showOverlayTemplate(\_:animated:completion:)), added CPSearchTemplate to Audio and Video apps, introduced CPMapPanel (showPanel(\_:completion:)) for Navigation apps, and enabled an automatic **MiniPlayer** (CPNowPlayingTemplate.shared.allowsMiniPlayer) \[Apple-documented: CarPlay Developer Guide & WWDC26 Session 212, 2026-06 / 2026-10-13; High Confidence\] 3.  
![][image1]

##### **Deliverable (1): Platform Capability & Template Matrix Across iOS 26.x, iOS 27.x, and Apple HomeView**

The comparison table below maps all 11 CarPlay categories across iOS 26.x, iOS 27.x, and HomeView, specifying availability, entitlement keys, permitted CPTemplate subclasses, and maximum template hierarchy depth \[Apple-documented / Developer-observed: CarPlay Developer Guide, Entitlements Docs & 9to5Mac, 2026-10-13 / 2026-11-05; High Confidence\] 3:

| CarPlay Category | iOS 26.x | iOS 27.x | HomeView | Entitlement | Permitted Templates | Max Depth |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Audio** | Available (iOS 14.0+). Adds CPPlaybackConfiguration & CPListTemplateDetailsHeader in iOS 26.4+2. | Available. Adds automatic **MiniPlayer** (allowsMiniPlayer), portrait/landscape thumbnails, CPSearchTemplate, and CPVoiceControlTemplate10. | **Full App Supported at Launch (27.2)** via DPLA §6.4.2 & PebblePlay bridge from paired iPhone/iPad (iOS/iPadOS 27.2+). Also supports systemSmall widgets (§6.4.1)2. | com.apple.developer.carplay-audio (Cannot combine with other CarPlay entitlements in iOS 26.3+)2. | **iOS 26.x:** CPActionSheetTemplate (iOS 17+), CPAlertTemplate, CPGridTemplate, CPListTemplate, CPNowPlayingTemplate, CPTabBarTemplate. **iOS 27.0+ adds:** CPSearchTemplate, CPVoiceControlTemplate (modal or showOverlayTemplate). *(Only CPListTemplate can push onto CPNowPlayingTemplate)*3. | **5 templates** (incl. root)3 |
| **Video** | **Not available as a standalone category** (AirPlay video in car & CPPlaybackConfiguration added in iOS 26.4+)12. | **Added in iOS 27.0.** Hidden on CarPlay Home Screen unless vehicle hardware supports video-in-car (supportsVideoPlayback \== true)3. | **Full App Supported at Launch (27.2)** via DPLA §6.4.2 & PebblePlay bridge from paired iPhone/iPad, plus systemSmall widgets (§6.4.1)3. | com.apple.developer.carplay-video (Cannot combine with other CarPlay entitlements in iOS 26.3+)9. | **iOS 27.0+:** Same template column as Audio ("Audio, video"): CPActionSheetTemplate, CPAlertTemplate, CPGridTemplate, CPListTemplate, CPNowPlayingTemplate, CPSearchTemplate, CPTabBarTemplate, CPVoiceControlTemplate \+ AirPlay video streaming3. | **5 templates** (incl. root)3 |
| **Voice-Based Conversation** | **Added in iOS 26.4** (Feb 2026). Exempt from Siri requirement; voice must be primary modality on launch1. | Available. Gains showOverlayTemplate support in CPInterfaceController10. | **Not supported at 27.2 Launch** (widgets only). **Added in iOS 27.3 Beta** to PebblePlay bridge (ConversationalApps flag; not yet enabled in production)16. | com.apple.developer.carplay-voice-based-conversation9. | **iOS 26.4+ & 27.x:** CPActionSheetTemplate, CPAlertTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPPointOfInterestTemplate, CPTabBarTemplate, CPVoiceControlTemplate (up to 5 states; action buttons in iOS 26.4+). *(Excludes CPMapTemplate, CPNowPlayingTemplate, CPContactTemplate)*3. | **3 templates** (root \+ 2 levels)3 |
| **Communication** | Available (iOS 14.0+). Requires SiriKit messaging or CallKit VoIP41. | Available. Supports CPVoiceControlTemplate overlay14. | **No Full App Support.** systemSmall widgets only (DPLA §6.4.1); native FaceTime/Messages handle built-in comms38. | com.apple.developer.carplay-communication40. | **iOS 26.x & 27.x:** CPActionSheetTemplate, CPAlertTemplate, CPContactTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPTabBarTemplate, CPVoiceControlTemplate3. | **5 templates** (incl. root)3 |
| **Navigation** | Available (iOS 12.0+). iOS 26.4+ adds route sharing (CPRouteSegment, CPNavigationWaypoint)10. | Available. Adds CPMapPanel (showPanel/hidePanel) and non-blocking CPVoiceControlTemplate overlay over live CPMapTemplate3. | **No Full App Support.** systemSmall widgets only (DPLA §6.4.1)38. | com.apple.developer.carplay-maps24. | **iOS 26.x:** CPMapTemplate (root over CPWindow), CPActionSheetTemplate, CPAlertTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPNowPlayingTemplate, CPPointOfInterestTemplate, CPSearchTemplate, CPTabBarTemplate, CPVoiceControlTemplate. **iOS 27.0+ adds:** CPMapPanel & showOverlayTemplate3. | **5 templates** (incl. root)3 |
| **Public Safety** | Available (iOS 14.0+). Restricted to fire, police, ambulance, and public safety agencies; supports notifications3. | Available. Gains CPVoiceControlTemplate overlay (showOverlayTemplate) and CPMapPanel3. | **No Full App Support.** systemSmall widgets only (DPLA §6.4.1)38. | com.apple.developer.carplay-public-safety3. | **iOS 26.x:** CPMapTemplate (root with CPNavigationSession), CPActionSheetTemplate, CPAlertTemplate, CPContactTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPPointOfInterestTemplate, CPSearchTemplate, CPTabBarTemplate, CPVoiceControlTemplate. **iOS 27.0+ adds:** showOverlayTemplate & CPMapPanel3. | **5 templates** (incl. root)3 |
| **EV Charging** | Available (iOS 14.0+). Supports notifications; can combine with Fueling entitlement3. | Available. Gains CPVoiceControlTemplate in iOS 27.0+24. | **No Full App Support.** systemSmall widgets only (DPLA §6.4.1)38. | com.apple.developer.carplay-charging (May combine *only* with carplay-fueling)3. | **iOS 26.x:** CPActionSheetTemplate, CPAlertTemplate, CPContactTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPPointOfInterestTemplate, CPTabBarTemplate. **iOS 27.0+ adds:** CPVoiceControlTemplate3. | **5 templates** (incl. root)3 |
| **Parking** | Available (iOS 14.0+). Supports notifications3. | Available. Gains CPVoiceControlTemplate in iOS 27.0+24. | **No Full App Support.** systemSmall widgets only (DPLA §6.4.1)38. | com.apple.developer.carplay-parking3. | **iOS 26.x:** CPActionSheetTemplate, CPAlertTemplate, CPContactTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPPointOfInterestTemplate, CPTabBarTemplate. **iOS 27.0+ adds:** CPVoiceControlTemplate3. | **5 templates** (incl. root)3 |
| **Fueling** | Available (iOS 16.0+). Can combine with EV Charging entitlement3. | Available. Gains CPVoiceControlTemplate in iOS 27.0+24. | **No Full App Support.** systemSmall widgets only (DPLA §6.4.1)38. | com.apple.developer.carplay-fueling (May combine *only* with carplay-charging)3. | **iOS 26.x:** CPActionSheetTemplate, CPAlertTemplate, CPContactTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPPointOfInterestTemplate, CPTabBarTemplate. **iOS 27.0+ adds:** CPVoiceControlTemplate3. | **3 templates** (incl. root)3 |
| **Quick Food Ordering** | Available (iOS 14.0+). Depth increased from 2 to 3 in iOS 26.43. | Available. Retains 3-template depth; gains CPVoiceControlTemplate in iOS 27.0+3. | **No Full App Support.** systemSmall widgets only (DPLA §6.4.1)38. | com.apple.developer.carplay-quick-ordering40. | **iOS 26.x:** CPActionSheetTemplate, CPAlertTemplate, CPContactTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPPointOfInterestTemplate, CPTabBarTemplate. **iOS 27.0+ adds:** CPVoiceControlTemplate3. | **2** (iOS ≤26.3) / **3 templates** (iOS ≥26.4 & 27.x)3 |
| **Driving Task** | Available (iOS 16.0+). Depth increased from 2 to 3 in iOS 26.43. | Available. Retains 3-template depth; gains CPVoiceControlTemplate overlay3. | **No Full App Support.** systemSmall widgets only (DPLA §6.4.1)38. | com.apple.developer.carplay-driving-task40. | **iOS 26.x & 27.x:** CPActionSheetTemplate, CPAlertTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPPointOfInterestTemplate, CPTabBarTemplate, CPVoiceControlTemplate3. | **2** (iOS ≤26.3) / **3 templates** (iOS ≥26.4 & 27.x)3 |

##### **What CarPlay Ultra Changes for Third-Party Apps and How HomeView Bridging Works**

CarPlay Ultra is Apple's next-generation multi-screen vehicle architecture that renders across all driver displays (center console, instrument cluster, and head-up display) wirelessly from the driver's iPhone while built-in vehicle systems power core driving features \[Apple-documented: Apple CarPlay Developer Overview, 2026-10; High Confidence\] 50. For third-party native Swift developers, CarPlay Ultra requires no separate entitlement or SDK; adopting the standard CarPlay framework enables the app across both standard CarPlay and CarPlay Ultra vehicles \[Apple-documented: Apple CarPlay Developer Overview, 2026-10; High Confidence\] 31. Navigation apps (com.apple.developer.carplay-maps) gain the ability to project turn-by-turn maps and maneuver guidance directly into the instrument cluster and HUD by declaring a CPTemplateApplicationInstrumentClusterScene and implementing CPTemplateApplicationInstrumentClusterSceneDelegate alongside CPInstrumentClusterController and CPInstrumentClusterControllerDelegate \[Apple-documented: CarPlay Documentation, 2026-10; High Confidence\] 50. Small widgets (WidgetLocation.carPlay) and small Live Activities (.supplementalActivityFamilies(\[.small\])) render across both CarPlay Ultra and standard CarPlay (iOS 26+), whereas deep vehicle hardware integrations (such as climate controls or EnergyKit home-electricity optimization for EVs) remain restricted to **automaker apps** published under the MFi program \[Apple-documented: Apple CarPlay Developer Overview & CarPlay Developer Guide, 2026-10-13; High Confidence\] 3.  
On Apple HomeView, third-party apps surface over local Wi-Fi from a paired iPhone (iOS 27.2+) or iPad (iPadOS 27.2+) \[Apple-documented: Apple HomeView Tech Specs & User Guide, 2026-11-13; High Confidence\] 5. When HomeView's camera recognizes one of up to six enrolled household members by face and confirms their paired iPhone or iPad is present on the same Wi-Fi network and recently unlocked, it surfaces that user's personalized Home Screen, widgets, and eligible CarPlay Audio/Video apps (and Conversational apps in iOS 27.3 beta) via the PebblePlay CarPlay bridge \[Apple-documented / Developer-observed: Apple Newsroom & 9to5Mac, 2026-11-05 / 2026-11-13; High Confidence\] 16. Guests or unrecognized users can access shared built-in apps (Music via the Primary Account, Podcasts, Intercom, Alarms, Timers, Weather, World Clock, and optional Safari), and anyone on the Wi-Fi network can transfer media via Proximity Handoff (holding an iPhone near the display) or stream via AirPlay without facial recognition \[Apple-documented: Apple HomeView User Guide, 2026-11-13; High Confidence\] 39.

#### **2\. UI and UX: Apple Human Interface Guidelines for CarPlay and HomeView**

Designing for CarPlay and HomeView requires adhering to strict template limits and distance-viewing ergonomics. Because Apple has not published a standalone HomeView HIG section as of November 2026, HomeView UI rules are governed across the **CarPlay HIG**, the **Widgets HIG**, the **Live Activities HIG**, the **Apple HomeView User Guide**, and the **CarPlay Developer Guide (October 13, 2026\)** \[Apple-documented / Developer-observed: CarPlay HIG, Widgets HIG & Blake Crosley Audit, 2026-10-13; High Confidence\] 8.  
![][image2]

##### **Deliverable (2): UI/UX Rule List Citing the HIG Page and Developer Guide for Each Rule**

The table below codifies every UI/UX design requirement, quantitative template cap, widget/Live Activity rendering rule, and App Review UX rejection pattern, citing its exact HIG page or Developer Guide section:

| UI / UX Domain | Concrete Design & Engineering Rule | Cited HIG Page / Primary Source & Date | Epistemic Label & Confidence |
| :---- | :---- | :---- | :---- |
| **Liquid Glass Visual System** | Rely on system-provided CPTemplate chrome and Siri AI layers rather than custom opaque backgrounds so CarPlay and HomeView (which exposes Settings → Appearance → Liquid Glass) render the translucent **Liquid Glass** design language introduced in iOS 26 and evolved in iOS 27\. | *CarPlay HIG* (developer.apple.com/design/human-interface-guidelines/carplay); *Apple HomeView User Guide — Change settings* (2026-11-13); CNET WWDC26 Report (2026-06) 3 | **Apple-documented / Developer-observed** (High Confidence) |
| **Eliminate iPhone Interaction & Locked-Phone Autonomy** | Never require users to unlock or touch their iPhone while CarPlay is active. Your app must function when the iPhone is locked in a bag or trunk. Error alerts (CPAlertTemplate) must **never** include wording asking the driver to manipulate their iPhone; any required phone setup must occur before the vehicle moves or after it stops. | *CarPlay HIG* — General Design Guidelines (developer.apple.com/design/human-interface-guidelines/carplay); *CarPlay Developer Guide* p. 7–8 (2026-10-13) 3 | **Apple-documented** (High Confidence) |
| **Glanceability & Distance Viewing** | Place the most important content and actionable controls in the **upper half of the screen**, use large tap targets, maintain a consistent layout across similar elements, and use a limited color palette that coordinates with your app logo. For widgets in CarPlay, StandBy, and HomeView (7-inch display), use **larger typography** and show only glanceable data. | *CarPlay HIG* — General Design Guidelines (developer.apple.com/design/human-interface-guidelines/carplay); *WidgetKit Docs — Adding StandBy and CarPlay support to your widget* (2026-10-13) 51 | **Apple-documented** (High Confidence) |
| **Display Scaling & App Icon Contrast** | Support automatic display scaling across 800×480 @2x (16:9) and widescreen 1920×720 (8:3) displays. Provide CarPlay app icons at 120×120 px (@2x) and 180×180 px (@3x). **Never use pure black** for the icon background; lighten a black background or add a border so the icon does not blend into the dark display background. | *CarPlay HIG* — Layout (developer.apple.com/design/human-interface-guidelines/carplay, 2026-10-13) 13 | **Apple-documented** (High Confidence) |
| **Template Limits: Depth, Tabs, Lists, Grids, POIs, Icons** | Enforce hard bounds: **Depth:** max **5** templates (Audio, Video, Communication, EV Charging, Parking, Public Safety, Navigation), max **3** (Fueling, Voice-Based Conversational), max **2** in iOS ≤26.3 / **3** in iOS ≥26.4 (Driving Task, Quick Food Ordering). **Tabs:** max **4** (CPTabBarTemplate.maximumTabCount; exceeding 4 throws an exception). **Lists:** excess items beyond maximumItemCount are truncated, and OEM head units dynamically cap lists to **12 items**. **Grids:** max **8** buttons. **POIs:** max **12** CPPointOfInterest pins. **Now Playing:** max **5** nowPlayingButtons; only CPListTemplate may push onto CPNowPlayingTemplate. **Icon Sizes:** Contact action 50 pt, Grid 40 pt (maximumGridButtonImageSize), Tab bar 24 pt, Now Playing button 20 pt. | *CarPlay Developer Guide* p. 16 (2026-10-13); *CPPointOfInterest* & *CPListTemplate* API Reference; Platform APIs Audit (2026-10) 3 | **Apple-documented / Developer-observed** (High Confidence) |
| **Audio Playback & Interruption Discipline** | Let users choose when to start playback (avoid auto-play unless resuming interrupted audio or playing a single-source stream). Do **not** activate AVAudioSession until audio has buffered and is ready to play (starting a session silences the car's radio). Display CPNowPlayingTemplate immediately when audio starts without waiting for metadata/artwork to finish loading. Resume only after temporary interruptions (e.g., phone calls), not permanent ones (e.g., Siri music playlist). Never alter the master output volume. In iOS 27+, the **MiniPlayer** appears automatically unless CPNowPlayingTemplate.shared.allowsMiniPlayer \= false. | *CarPlay HIG* — General Design Guidelines (developer.apple.com/design/human-interface-guidelines/carplay, 2026-10-13); *CPNowPlayingTemplate* Docs & WWDC26 Session 212 (2026-06) 10 | **Apple-documented** (High Confidence) |
| **Voice, Siri & App Intents Interaction** | Communication apps must use SiriKit messaging/VoIP intents (INSendMessageIntent). Audio apps should support MediaIntents (AudioSearch in iOS 27.0) and Siri App Selection. In iOS 27.3, @AppIntent(.tool) enables foreground voice invocation without speaking the app name, and Siri AI on HomeView performs direct in-app actions. Voice-Based Conversational apps (iOS 26.4+) are **exempt from Siri**, must use voice as their primary modality on launch, must show CPVoiceControlTemplate (max **5** states; rate-limited state changes; up to 2–4 action buttons in iOS 26.4+) during audio input, and must hold AVAudioSession open only while voice is active. Physical steering wheel voice buttons remain locked to Siri. | *CarPlay Developer Guide* (2026-10-13); *CPVoiceControlTemplate* Docs; WWDC26 Session 212 (2026-06); Apple Developer Forums (2026-11); iDropNews (2026-02) 3 | **Apple-documented / Developer-observed** (High Confidence) |
| **Widgets on CarPlay and HomeView (Modular Face & Night Mode)** | CarPlay and HomeView use WidgetFamily.systemSmall widgets from the paired iPhone/iPad. On **HomeView's Home Screen**, widgets keep their standard iPhone appearance; on **HomeView's Modular face**, **Modular face in Night Mode**, **CarPlay** (stacks to the left of Dashboard in LHD, right in RHD), and **StandBy**, small widgets are scaled up with their **background removed** via .containerBackground(for: .widget). In CarPlay, widget buttons/toggles and app-launch taps work only on touchscreen vehicles (and app launch requires a CarPlay-integrated app); on non-touch vehicles, widgets are non-interactive. | *Widgets HIG* (developer.apple.com/design/human-interface-guidelines/widgets, 2026-10-13); *WidgetKit Docs — Adding StandBy and CarPlay support to your widget* & *Displaying the right widget background*; *CarPlay Developer Guide* p. 3–4 3 | **Apple-documented** (High Confidence) |
| **Live Activities on CarPlay and HomeView** | Support ActivityFamily.small via .supplementalActivityFamilies(\[.small\]) so Live Activities appear in CarPlay Dashboard or as notifications in iOS 26+ (CarPlay and CarPlay Ultra). While ActivityFamily.small is shared with Apple Watch (where Live Activities can be interactive), **CarPlay Live Activities are non-interactive**. On HomeView, the *Live Activities HIG* omits HomeView, though the *Apple HomeView User Guide* documents built-in Live Activities (timers, music) at the top of the screen. | *Live Activities HIG* (developer.apple.com/design/human-interface-guidelines/live-activities, 2026-10-13); *CarPlay Developer Guide* p. 3–4 (2026-10-13); *Apple HomeView User Guide* (2026-11-13) 3 | **Apple-documented** (High Confidence) |
| **Day / Night Appearance** | Observe CPSessionConfiguration.contentStyle and CPInterfaceController.carTraitCollection to adapt map tiles and interface assets to vehicle light/dark sensors, or set prefersDarkUserInterfaceStyle \= true. On HomeView, validate appearance across Light Mode, Dark Mode, **Ambient Dark Mode**, and **Modular face in Night Mode**. | *CPSessionConfiguration* & *CPInterfaceController* Docs; *Widgets HIG* (2026-10-13); *Apple HomeView User Guide — Change settings* (2026-11-13) 14 | **Apple-documented** (High Confidence) |
| **UX Patterns App Review Rejects** | **Audio:** Showing song lyrics on the CarPlay screen; omitting AirPlay video streaming when offering video. **Video:** Rendering video via an unentitled web browser view (e.g., *APTV* removal) or without AirPlay video streaming. **Conversational:** Showing text/imagery in response to voice queries instead of spoken dialog, or keeping AVAudioSession open when idle. **Navigation/Parking/Fueling/Food/Task:** Drawing non-map UI on the base CPWindow, omitting map panning mode, misusing maneuver icons, showing non-fueling POIs in a fueling app, showing a full menu in quick food ordering, or building tasks done *while* driving that do not *help with the drive*. | *CarPlay Developer Guide* p. 7–15 (2026-10-13); BigGo Finance *APTV* Enforcement Report (2026-11-06) 3 | **Apple-documented / Developer-observed** (High Confidence) |

#### **3\. Code: Current Swift 6 / iOS 27 SDK API Shape and Minimal Compilable Skeletons**

##### **Adding CPTemplateApplicationScene to an Existing SwiftUI App-Lifecycle Project and Handling CarPlay-Only Cold Launch**

Integrating CarPlay (and HomeView's PebblePlay bridge) into a native SwiftUI App-lifecycle application requires decoupling your core state from your SwiftUI view hierarchy \[Developer-observed: Platform APIs Audit, 2026-10; High Confidence\] 13. When a user enters their vehicle or launches your app from Apple HomeView while their iPhone remains locked in their pocket, iOS cold-launches your app process and connects **only** the CPTemplateApplicationScene—the SwiftUI WindowGroup scene never connects, and any @StateObject, @Environment, or database container initialized inside a SwiftUI View will not exist (a common cause of cold-launch crashes reported on the Apple Developer Forums) \[Apple-documented / Developer-observed: CarPlay HIG & Apple Developer Forums, 2026-10; High Confidence\] 13. To support both scenes cleanly, attach an NSObject application delegate via @UIApplicationDelegateAdaptor and either return a UISceneConfiguration dynamically in application(\_:configurationForConnecting:options:) when connectingSceneSession.role \== .carTemplateApplication (CPTemplateApplicationSceneSessionRoleApplication in CPTemplateApplicationScene.h:107), or declare both UIWindowSceneSessionRoleApplication and CPTemplateApplicationSceneSessionRoleApplication in Info.plist under UIApplicationSceneManifest → UISceneConfigurations \[Developer-observed: Platform APIs Audit, 2026-10; High Confidence\] 13:

XML  
\<\!-- Info.plist UIApplicationSceneManifest for a SwiftUI App \+ CarPlay / HomeView \--\>  
\<key\>UIApplicationSceneManifest\</key\>  
\<dict\>  
    \<key\>UIApplicationSupportsMultipleScenes\</key\>  
    \<true/\>  
    \<key\>UISceneConfigurations\</key\>  
    \<dict\>  
        \<key\>UIWindowSceneSessionRoleApplication\</key\>  
        \<array\>  
            \<dict\>  
                \<key\>UISceneConfigurationName\</key\>  
                \<string\>Default Phone Configuration\</string\>  
            \</dict\>  
        \</array\>  
        \<key\>CPTemplateApplicationSceneSessionRoleApplication\</key\>  
        \<array\>  
            \<dict\>  
                \<key\>UISceneClassName\</key\>  
                \<string\>CPTemplateApplicationScene\</string\>  
                \<key\>UISceneConfigurationName\</key\>  
                \<string\>CarPlayConfiguration\</string\>  
                \<key\>UISceneDelegateClassName\</key\>  
                \<string\>\$(PRODUCT\_MODULE\_NAME).CarPlaySceneDelegate\</string\>  
            \</dict\>  
        \</array\>  
    \</dict\>  
\</dict\>

##### **CPTemplateApplicationSceneDelegate, CPNowPlayingTemplate, and the iOS 27 NowPlaying Framework Transition**

When templateApplicationScene(\_:didConnect:) fires, your CPTemplateApplicationSceneDelegate must retain a strong reference to the passed CPInterfaceController and assign a root template using the 3-parameter setRootTemplate(\_:animated:completion:) or its async throws \-\> Bool overload (try await interfaceController.setRootTemplate(root, animated: false))—the legacy 2-parameter setRootTemplate(\_:animated:), pushTemplate(\_:animated:), and presentTemplate(\_:animated:) methods are officially **deprecated**, and omitting the completion handler throws an exception if presentation fails \[Apple-documented: CPInterfaceController Deprecated Symbols & setRootTemplate Docs, 2026-10; High Confidence\] 13.  
For media playback, CPNowPlayingTemplate.shared renders the active Now Playing session and in iOS 27 automatically displays a persistent **MiniPlayer** across your browse templates unless you opt out via CPNowPlayingTemplate.shared.allowsMiniPlayer \= false \[Apple-documented: CPNowPlayingTemplate Docs & WWDC26 Session 212, 2026-06 / 2026-10; High Confidence\] 10. When targeting both iOS 26.x and iOS 27.x, you must manage a critical framework transition: while iOS 26 relies on MPNowPlayingInfoCenter.default() and MPRemoteCommandCenter.shared(), **iOS 27.0** introduces the native Swift **NowPlaying framework** (MediaSession\<Representable: MediaSessionRepresentable\>, MediaPlaybackSnapshot, MediaCommand, Artwork, ArtworkRepresentation, and structured content types MusicContent, PodcastContent, BookContent, MovieContent, TVShowContent, RadioContent) alongside the MediaIntents framework (AudioSearch) \[Developer-observed: Platform APIs Audit, 2026-10; High Confidence\] 13. **Mixing legacy MPNowPlayingInfoCenter/MPRemoteCommandCenter calls with the iOS 27 NowPlaying framework causes undefined behavior**13. Furthermore, on iOS 27, apps that combine MPNowPlayingInfoCenter.default() with MusicKit's ApplicationMusicPlayer.shared trigger bug FB24840951, where CPNowPlayingTemplate remains frozen on whichever Now Playing client was active prior to switching \[Developer-observed: Apple Developer Forums, 2026-11; High Confidence\] 31.

##### **CPPlaybackConfiguration and AVKit/AVFoundation Video for CarPlay Video Apps and HomeView**

In iOS 26.4+ and iOS 27, apps do not embed a custom AVPlayerViewController or VideoPlayer view inside a CarPlay template; instead, the in-car and HomeView browsing UI is constructed entirely with CarPlay framework templates (CPListTemplate, CPGridTemplate, CPTabBarTemplate) while video frames stream to the head unit or HomeView display via **AirPlay video streaming** (AVPlayer.allowsExternalPlayback \= true) \[Apple-documented: WWDC26 Session 212 & CarPlay Developer Guide, 2026-06 / 2026-10-13; High Confidence\] 3. You bind media items and CPListTemplateDetailsHeader views to playback state using CPPlaybackConfiguration(preferredPresentation:playbackAction:elapsedTime:duration:), where CPPlaybackConfiguration.Presentation (conforming to Sendable) specifies .video, .audio, or .none \[Apple-documented: CPPlaybackConfiguration Docs, 2026-10; High Confidence\] 10. Your scene delegate must inspect CPSessionConfiguration.supportsVideoPlayback to conditionally display video tabs and automatically fall back to audio-only playback if supportsVideoPlayback becomes false when the driver shifts out of park \[Apple-documented: CPSessionConfiguration Docs & WWDC26 Session 212, 2026-06 / 2026-10; High Confidence\] 10.

##### **CPVoiceControlTemplate, AVAudioSession, and App Intents for Conversational Apps**

For voice-based conversational apps (com.apple.developer.carplay-voice-based-conversation, iOS 26.4+) and voice overlays in other categories (iOS 27.0+), instantiate CPVoiceControlTemplate(voiceControlStates:) with up to **5** CPVoiceControlState objects (any states after the first 5 are ignored) and up to 2–4 actionButtons (iOS 26.4+) \[Apple-documented: CPVoiceControlTemplate & CPVoiceControlState Docs, 2026-10; High Confidence\] 10. You must present the template via presentTemplate(\_:animated:completion:) (iOS 26.4+) or showOverlayTemplate(\_:animated:completion:) (iOS 27.0+) **before** calling activateVoiceControlState(withIdentifier:), and debounce state changes because CPVoiceControlTemplate enforces an internal rate limit that drops rapid state transitions \[Apple-documented: CPVoiceControlTemplate & CPInterfaceController Docs, 2026-10; High Confidence\] 14. Configure AVAudioSession.sharedInstance() with .playAndRecord, mode .default, and **no mixing** (\[\] or .allowBluetoothHFP), activating the session only while voice interaction is active \[Apple-documented: WWDC26 Session 212 & CarPlay Developer Guide, 2026-06 / 2026-10-13; High Confidence\] 3. While conversational apps are exempt from Siri, apps integrating with Siri AI in iOS 27.3 can adopt the @AppIntent(.tool) macro (which allows foreground voice invocation without speaking the app name) and AppIntentConfiguration for configurable widgets \[Apple-documented / Developer-observed: WidgetKit Docs & Apple Developer Forums, 2026-10 / 2026-11; High Confidence\] 11.

##### **WidgetKit, ActivityKit, HomeKit/Matter, and Swift 6 Strict Concurrency**

To support CarPlay and HomeView in WidgetKit and ActivityKit, configure your WidgetFamily.systemSmall widget with .containerBackground(for: .widget) (so CarPlay, StandBy, and HomeView's Modular face can strip the background) and apply .disfavoredLocations(\[.carPlay\], for: \[.systemSmall\]) (WidgetLocation.carPlay, iOS 26.0+) only if the widget requires an unlocked iPhone or heavy touch interaction \[Apple-documented: WidgetKit Docs & DPLA §6.4.1, 2026-10-13; High Confidence\] 4. For Live Activities, attach .supplementalActivityFamilies(\[.small\]) to your ActivityConfiguration \[Apple-documented: ActivityFamily Docs & CarPlay Developer Guide, 2026-10-13; High Confidence\] 3:

Swift  
// WidgetKit & ActivityKit Modifiers for CarPlay (iOS 26+) and HomeView (27.2+)  
struct AmbientStatusWidget: Widget {  
    var body: some WidgetConfiguration {  
        AppIntentConfiguration(kind: "AmbientStatus", intent: ConfigurationAppIntent.self, provider: Provider()) { entry in  
            AmbientStatusView(entry: entry)  
                .containerBackground(.fill.tertiary, for: .widget) // Removed on CarPlay & HomeView Modular Face  
        }  
        .supportedFamilies(\[.systemSmall\])  
        // Uncomment ONLY to disfavor on BOTH CarPlay and HomeView:  
        // .disfavoredLocations(\[.carPlay\], for: \[.systemSmall\])  
    }  
}

For **HomeKit and Matter**, Apple ships no HomeView-specific HomeKit SDK; HomeView natively syncs with the Apple Home app architecture to control lights, locks, and thermostats, and hidden firmware strings in HomeView 27.2 indicate built-in HomeKit security camera support \[Apple-documented / Developer-observed: Apple Newsroom & 9to5Mac, 2026-11-02 / 2026-11-13; High Confidence\] 16. \<MISSING\_DATA\>\[Apple has not published any HomeView-specific HomeKit or Matter API extensions in the iOS 27.0–27.2 SDK beyond standard iOS HomeKit and AccessorySetupKit APIs.\]\</MISSING\_DATA\> Under **Swift 6 strict concurrency**, CPTemplate, CPVoiceControlTemplate, CPPointOfInterestTemplate, and CPPlaybackConfiguration are explicitly annotated @MainActor in the iOS 27 SDK \[Apple-documented: CarPlay Framework Documentation, 2026-10; High Confidence\] 12. Annotate your CPTemplateApplicationSceneDelegate class @MainActor, use @preconcurrency import CarPlay and @preconcurrency import MediaPlayer where Objective-C completion signatures lack @Sendable annotations, and hop to Task { @MainActor in ... } inside synchronous MPRemoteCommandCenter target closures.

##### **Deliverable (3)(a): Minimal Swift 6 / iOS 27 SDK Skeleton — CarPlay & HomeView Audio App (with AirPlay Video & CPPlaybackConfiguration)**

Swift  
import SwiftUI  
import UIKit  
@preconcurrency import CarPlay  
@preconcurrency import MediaPlayer  
import AVFoundation  
import CoreMedia

// MARK: \- 1\. SwiftUI App Lifecycle Entry Point  
@main  
struct MediaStreamApp: App {  
    @UIApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate

    var body: some Scene {  
        WindowGroup {  
            ContentView()  
                .onAppear {  
                    // Phone UI shares the same @MainActor singleton used by CarPlay/HomeView cold launches  
                    PlaybackCoordinator.shared.prepareIfNeeded()  
                }  
        }  
    }  
}

struct ContentView: View {  
    var body: some View {  
        Text("Phone UI Active — CarPlay & HomeView Ready")  
    }  
}

// MARK: \- 2\. UIApplicationDelegate Routing Phone & CarPlay Scenes  
@MainActor  
final class AppDelegate: NSObject, UIApplicationDelegate {  
    func application(  
        \_ application: UIApplication,  
        configurationForConnecting connectingSceneSession: UISceneSession,  
        options: UIScene.ConnectionOptions  
    ) \-\> UISceneConfiguration {  
        if connectingSceneSession.role \== UISceneSession.Role.carTemplateApplication {  
            let config \= UISceneConfiguration(  
                name: "CarPlayConfiguration",  
                sessionRole: connectingSceneSession.role  
            )  
            config.sceneClass \= CPTemplateApplicationScene.self  
            config.delegateClass \= CarPlayAudioSceneDelegate.self  
            return config  
        }  
        let phoneConfig \= UISceneConfiguration(  
            name: "Default Phone Configuration",  
            sessionRole: connectingSceneSession.role  
        )  
        return phoneConfig  
    }  
}

// MARK: \- 3\. Scene-Independent @MainActor Playback Coordinator (Cold-Launch Safe)  
@MainActor  
final class PlaybackCoordinator: NSObject {  
    static let shared \= PlaybackCoordinator()  
    private let player \= AVPlayer()  
    private var isPrepared \= false

    func prepareIfNeeded() {  
        guard \!isPrepared else { return }  
        isPrepared \= true  
        // Enable AirPlay video streaming for CarPlay Video-in-Car & Apple HomeView  
        player.allowsExternalPlayback \= true  
        player.usesExternalPlaybackWhileExternalScreenIsActive \= true  
        configureRemoteCommands()  
    }

    private func configureRemoteCommands() {  
        let commandCenter \= MPRemoteCommandCenter.shared()  
        commandCenter.playCommand.isEnabled \= true  
        commandCenter.pauseCommand.isEnabled \= true

        // Swift 6 Strict Concurrency: handler closure is non-isolated; hop to @MainActor  
        commandCenter.playCommand.addTarget { \_ in  
            Task { @MainActor in  
                PlaybackCoordinator.shared.resumePlayback()  
            }  
            return .success  
        }  
        commandCenter.pauseCommand.addTarget { \_ in  
            Task { @MainActor in  
                PlaybackCoordinator.shared.pausePlayback()  
            }  
            return .success  
        }  
    }

    func startTrack(title: String, url: URL, isVideo: Bool) {  
        prepareIfNeeded()  
        // HIG Rule: Only activate AVAudioSession when ready to play audio  
        do {  
            let session \= AVAudioSession.sharedInstance()  
            try session.setCategory(.playback, mode: isVideo ? .moviePlayback : .default, policy: .longFormAudio)  
            try session.setActive(true)  
        } catch {  
            print("AVAudioSession activation failed: \\(error)")  
        }

        let item \= AVPlayerItem(url: url)  
        player.replaceCurrentItem(with: item)  
        player.play()

        MPNowPlayingInfoCenter.default().nowPlayingInfo \= \[  
            MPMediaItemPropertyTitle: title,  
            MPNowPlayingInfoPropertyElapsedPlaybackTime: 0.0,  
            MPMediaItemPropertyPlaybackDuration: 240.0,  
            MPNowPlayingInfoPropertyPlaybackRate: 1.0  
        \]  
    }

    func resumePlayback() {  
        player.play()  
    }

    func pausePlayback() {  
        player.pause()  
        try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)  
    }  
}

// MARK: \- 4\. CPTemplateApplicationSceneDelegate for Audio \+ HomeView  
@MainActor  
final class CarPlayAudioSceneDelegate: UIResponder, CPTemplateApplicationSceneDelegate, CPSessionConfigurationDelegate {  
    private var interfaceController: CPInterfaceController?  
    private var sessionConfiguration: CPSessionConfiguration?

    func templateApplicationScene(  
        \_ templateApplicationScene: CPTemplateApplicationScene,  
        didConnect interfaceController: CPInterfaceController  
    ) {  
        self.interfaceController \= interfaceController  
        self.sessionConfiguration \= CPSessionConfiguration(delegate: self)

        // Cold-launch initialization without relying on SwiftUI WindowGroup  
        PlaybackCoordinator.shared.prepareIfNeeded()

        // iOS 27 MiniPlayer configuration (enabled by default; set false only if preferring navbar button)  
        if \#available(iOS 27.0, \*) {  
            CPNowPlayingTemplate.shared.allowsMiniPlayer \= true  
        }  
        CPNowPlayingTemplate.shared.isUpNextButtonEnabled \= true  
        CPNowPlayingTemplate.shared.isAlbumArtistButtonEnabled \= true

        Task { @MainActor in  
            await rebuildRootTabs()  
        }  
    }

    func templateApplicationScene(  
        \_ templateApplicationScene: CPTemplateApplicationScene,  
        didDisconnectInterfaceController interfaceController: CPInterfaceController  
    ) {  
        self.interfaceController \= nil  
        self.sessionConfiguration \= nil  
    }

    nonisolated func sessionConfiguration(  
        \_ sessionConfiguration: CPSessionConfiguration,  
        contentStyleChanged contentStyle: CPContentStyle  
    ) {  
        Task { @MainActor in  
            // React to vehicle day/night sensor changes if using custom themed imagery  
        }  
    }

    private func rebuildRootTabs() async {  
        guard let interfaceController else { return }

        // Build Audio Library Tab (respecting OEM 12-item dynamic cap)  
        let audioItem \= CPListItem(text: "Morning Briefing Episode 42", detailText: "Audio • 4 mins")  
        if \#available(iOS 26.4, \*) {  
            let playbackConfig \= CPPlaybackConfiguration(  
                preferredPresentation: .audio,  
                playbackAction: .play,  
                elapsedTime: .zero,  
                duration: CMTime(seconds: 240, preferredTimescale: 1)  
            )  
            \_ \= playbackConfig // Attach to playable item / details header as configured  
        }  
        audioItem.handler \= { \[weak self\] \_, completion in  
            Task { @MainActor in  
                guard let url \= URL(string: "https\://example.com/audio.m4a") else {  
                    completion()  
                    return  
                }  
                PlaybackCoordinator.shared.startTrack(title: "Morning Briefing Episode 42", url: url, isVideo: false)  
                // HIG Rule: Push NowPlayingTemplate as soon as playback starts  
                \_ \= try? await self?.interfaceController?.pushTemplate(CPNowPlayingTemplate.shared, animated: true)  
                completion()  
            }  
        }

        let libraryList \= CPListTemplate(  
            title: "Library",  
            sections: \[CPListSection(items: \[audioItem\])\]  
        )  
        libraryList.tabTitle \= "Library"  
        libraryList.tabImage \= UIImage(systemName: "music.note.list")

        var tabs: \[CPTemplate\] \= \[libraryList\]

        // Conditionally add Video tab if vehicle/HomeView supports video playback (iOS 27+)  
        if sessionConfiguration?.supportsVideoPlayback \== true {  
            let videoItem \= CPListItem(text: "Studio Session (Parked / HomeView)", detailText: "Video • 1080p HEVC")  
            videoItem.handler \= { \[weak self\] \_, completion in  
                Task { @MainActor in  
                    if let url \= URL(string: "https\://example.com/video.m3u8") {  
                        PlaybackCoordinator.shared.startTrack(title: "Studio Session", url: url, isVideo: true)  
                        \_ \= try? await self?.interfaceController?.pushTemplate(CPNowPlayingTemplate.shared, animated: true)  
                    }  
                    completion()  
                }  
            }  
            let videoList \= CPListTemplate(title: "Videos", sections: \[CPListSection(items: \[videoItem\])\])  
            videoList.tabTitle \= "Videos"  
            videoList.tabImage \= UIImage(systemName: "film")  
            tabs.append(videoList)  
        }

        // Max 4 tabs allowed for Audio apps (CPTabBarTemplate.maximumTabCount)  
        let rootTabBar \= CPTabBarTemplate(templates: Array(tabs.prefix(CPTabBarTemplate.maximumTabCount)))  
        \_ \= try? await interfaceController.setRootTemplate(rootTabBar, animated: false)  
    }  
}

##### **Deliverable (3)(b): Minimal Swift 6 / iOS 27 SDK Skeleton — Voice-Based Conversational App (with CPVoiceControlTemplate Overlay & AVAudioSession Management)**

Swift  
import SwiftUI  
import UIKit  
@preconcurrency import CarPlay  
import AVFoundation  
import AppIntents

// MARK: \- 1\. Voice Conversation Engine (@MainActor Singleton for Cold-Launch Safety)  
@MainActor  
final class VoiceConversationEngine {  
    static let shared \= VoiceConversationEngine()  
    private var isSessionActive \= false

    /// CarPlay Developer Guide Rule: Only hold an audio session open when voice features are actively used.  
    /// WWDC26 Session 212 Rule: Configure with .playAndRecord, .default mode, and NO mixing.  
    func beginVoiceTurn(onStateChange: @escaping @MainActor (String) \-\> Void) {  
        do {  
            let session \= AVAudioSession.sharedInstance()  
            try session.setCategory(.playAndRecord, mode: .default, options: \[.allowBluetoothHFP, .defaultToSpeaker\])  
            try session.setActive(true)  
            isSessionActive \= true  
            onStateChange("listening")  
        } catch {  
            print("Failed to activate conversational AVAudioSession: \\(error)")  
        }  
    }

    func transitionToSpeaking(onStateChange: @escaping @MainActor (String) \-\> Void) {  
        guard isSessionActive else { return }  
        onStateChange("speaking")  
    }

    func endVoiceTurn() {  
        guard isSessionActive else { return }  
        isSessionActive \= false  
        try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)  
    }  
}

// MARK: \- 2\. CPTemplateApplicationSceneDelegate for Voice-Based Conversational App  
// Requires Entitlement: com.apple.developer.carplay-voice-based-conversation (iOS 26.4+)  
// Bridges to HomeView in iOS 27.3+ via PebblePlay "ConversationalApps" category  
@MainActor  
final class CarPlayConversationalSceneDelegate: UIResponder, CPTemplateApplicationSceneDelegate {  
    private var interfaceController: CPInterfaceController?  
    private var voiceTemplate: CPVoiceControlTemplate?

    func templateApplicationScene(  
        \_ templateApplicationScene: CPTemplateApplicationScene,  
        didConnect interfaceController: CPInterfaceController  
    ) {  
        self.interfaceController \= interfaceController

        // 1\. CPVoiceControlTemplate cannot be set via setRootTemplate; create a lightweight root list first  
        // Conversational apps are limited to a max depth of 3 templates (including root).  
        let startPromptItem \= CPListItem(  
            text: "Start New Voice Conversation",  
            detailText: "Tap to speak hands-free"  
        )  
        startPromptItem.handler \= { \[weak self\] \_, completion in  
            Task { @MainActor in  
                await self?.presentVoiceAssistantOverlay()  
                completion()  
            }  
        }

        let rootList \= CPListTemplate(  
            title: "Assistant",  
            sections: \[CPListSection(items: \[startPromptItem\])\]  
        )

        // 2\. Build CPVoiceControlTemplate (max 5 states; rate-limited state transitions)  
        let listeningState \= CPVoiceControlState(  
            identifier: "listening",  
            titleVariants: \["Listening...", "Speak now"\],  
            image: UIImage(systemName: "waveform.circle.fill"),  
            repeats: true  
        )  
        let processingState \= CPVoiceControlState(  
            identifier: "processing",  
            titleVariants: \["Thinking...", "Working on that..."\],  
            image: UIImage(systemName: "ellipsis.bubble.fill"),  
            repeats: true  
        )  
        let speakingState \= CPVoiceControlState(  
            identifier: "speaking",  
            titleVariants: \["Speaking response"\],  
            image: UIImage(systemName: "speaker.wave.3.fill"),  
            repeats: true  
        )

        // iOS 26.4+ supports action buttons on CPVoiceControlState for follow-up actions  
        if \#available(iOS 26.4, \*) {  
            let stopButton \= CPButton(image: UIImage(systemName: "xmark.circle")\!) { \[weak self\] \_ in  
                Task { @MainActor in  
                    await self?.dismissVoiceAssistant()  
                }  
            }  
            listeningState.actionButtons \= \[stopButton\]  
            speakingState.actionButtons \= \[stopButton\]  
        }

        let template \= CPVoiceControlTemplate(  
            voiceControlStates: \[listeningState, processingState, speakingState\]  
        )  
        self.voiceTemplate \= template

        // 3\. Set root template, then immediately launch voice modality as required by CarPlay Developer Guide:  
        // "Voice-based conversational apps must have a primary modality of voice upon launch"  
        Task { @MainActor in  
            \_ \= try? await interfaceController.setRootTemplate(rootList, animated: false)  
            await presentVoiceAssistantOverlay()  
        }  
    }

    func templateApplicationScene(  
        \_ templateApplicationScene: CPTemplateApplicationScene,  
        didDisconnectInterfaceController interfaceController: CPInterfaceController  
    ) {  
        VoiceConversationEngine.shared.endVoiceTurn()  
        self.voiceTemplate \= nil  
        self.interfaceController \= nil  
    }

    private func presentVoiceAssistantOverlay() async {  
        guard let interfaceController, let voiceTemplate else { return }

        // iOS 27.0+ supports presenting CPVoiceControlTemplate as an overlay via showOverlayTemplate;  
        // on iOS 26.4, present modally via presentTemplate(\_:animated:completion:)  
        if \#available(iOS 27.0, \*) {  
            \_ \= try? await interfaceController.showOverlayTemplate(voiceTemplate, animated: true)  
        } else {  
            \_ \= try? await interfaceController.presentTemplate(voiceTemplate, animated: true)  
        }

        // IMPORTANT: Must present CPVoiceControlTemplate BEFORE calling activateVoiceControlState  
        VoiceConversationEngine.shared.beginVoiceTurn { \[weak self\] newStateID in  
            self?.voiceTemplate?.activateVoiceControlState(withIdentifier: newStateID)  
        }  
    }

    private func dismissVoiceAssistant() async {  
        VoiceConversationEngine.shared.endVoiceTurn()  
        guard let interfaceController else { return }  
        if \#available(iOS 27.0, \*) {  
            \_ \= try? await interfaceController.hideOverlayTemplate(animated: true)  
        } else {  
            \_ \= try? await interfaceController.dismissTemplate(animated: true)  
        }  
    }  
}

#### **4\. Entitlements and Deployment: Request Flow, Approval Timelines, Provisioning, Review Rejections, and Submission Checklist**

Developers cannot self-enable CarPlay entitlements in Xcode; you must submit a request via the Apple CarPlay entitlement form (developer.apple.com/carplay), select the single category matching your app's primary driving function, and agree to the **CarPlay Entitlement Addendum** \[Apple-documented: Requesting CarPlay Entitlements & CarPlay Developer Guide, 2026-10-13; High Confidence\] 3. Because Apple evaluates CarPlay entitlement requests strictly against in-vehicle driving safety and utility, developers are advised **never** to apply for a CarPlay entitlement solely for Apple HomeView \[Developer-observed: Blake Crosley Day-One Audit & GadgetHacks, 2026-10-26; High Confidence\] 8. While Apple publishes no guaranteed turnaround SLA, developers on the Apple Developer Forums in September–October 2026 reported wait times of **15+ days to over 4 weeks** without a decision for com.apple.developer.carplay-video, complicated by a web form bug where the description field submitted empty (Case-IDs 22627198 and 22644963\) \[Developer-observed: Apple Developer Forums Entitlements Tag, 2026-10; High Confidence\] 47. Once approved, you must enable the managed capability on your App ID in Certificates, Identifiers & Profiles, regenerate your provisioning profiles, and add the boolean key to your .entitlements file \[Apple-documented: CarPlay Developer Guide, 2026-10-13; High Confidence\] 3. Watch out for a developer-observed portal synchronization bug (thread 850675, October–November 2026\) where newly generated provisioning profiles omit com.apple.developer.carplay-audio even after Apple grants approval, causing CPTemplateApplicationScene to silently never connect \[Developer-observed: Apple Developer Forums Thread 850675, 2026-10 / 2026-11; High Confidence\] 84.  
During App Store Review, rejections cluster around four policy enforcements. First, under **App Store Review Guideline 2.5.1** and the October 13, 2026 *CarPlay Developer Guide*, combining two CarPlay entitlements in the same app (other than carplay-charging and carplay-fueling) causes immediate rejection—even if one of the entitlements is inadvertently left in an App Store Connect profile \[Apple-documented / Developer-observed: CarPlay Audio/Video Entitlement Docs & Developer Forums, 2026-10-13 / 2026-11-12; High Confidence\] 2. Second, attempting to bypass the parked-only com.apple.developer.carplay-video restriction by rendering video inside an unentitled web view triggers app takedown, as demonstrated when Apple removed *APTV* from the App Store on October 23, 2026 and mandated permanent removal of its browser player in v1.5.13 on November 6, 2026 \[Developer-observed: BigGo Finance, 2026-11-06; High Confidence\] 46. Third, the *CarPlay Developer Guide* prohibits selectively hiding or feature-flagging CarPlay for subsets of users; once the entitlement ships in your production binary, your icon appears on the CarPlay Home Screen for all users \[Apple-documented: CarPlay Developer Guide, 2026-10-13; High Confidence\] 3. Fourth, DPLA Sections **3.3.3(A)** (voice recording privacy), **3.3.3(J)** (side-button voice app launch rules), **6.4.1** (developer responsibility to disfavor widgets requiring iPhone unlock or heavy driver interaction), and **6.4.2** (automatic HomeView bridging for designated CarPlay categories) govern legal compliance; no separate HomeView review queue, opt-in flag, or Info.plist key exists \[Apple-documented / Developer-observed: DPLA, Apple Developer News & Blake Crosley Audit, 2026-10-13; High Confidence\] 6.

##### **Deliverable (5): Pre-Submission App Store & Entitlement Checklist**

> 1. **Single Entitlement Binary Audit (Guideline 2.5.1):** Run codesign \-d \--entitlements \- YourApp.app on the exported archive and every embedded extension (WidgetKit, Live Activities) to verify that **only one** com.apple.developer.carplay-\* boolean key is present (unless combining carplay-charging and carplay-fueling)2.  
> 2. **Provisioning Profile Key Verification (Thread 850675):** Run security cms \-D \-i embedded.mobileprovision to verify that Apple's Developer Portal actually injected your approved com.apple.developer.carplay-\* key into the signed profile85.  
> 3. **Cold-Launch & Locked-iPhone Autonomy Check:** Boot the CarPlay scene while the iPhone is locked (⌘L or physical lock button) with the app force-closed; verify that Keychain items use kSecAttrAccessibleAfterFirstUnlock and that all flows succeed without unlocking the iPhone or initializing the SwiftUI WindowGroup3.  
> 4. **Alert Copy Audit:** Inspect every CPAlertTemplate and CPActionSheetTemplate string to confirm zero messages instruct the user to unlock, check, or manipulate their iPhone while driving3.  
> 5. **Category-Specific Prohibition Check:** For Audio apps, confirm no song lyrics are rendered on CarPlay templates, CPTabBarTemplate has ≤4 tabs, and AVPlayer.allowsExternalPlayback \= true is set if offering video-with-audio3. For Conversational apps, confirm voice activates immediately upon launch, CPVoiceControlTemplate is presented before calling activateVoiceControlState(withIdentifier:), and AVAudioSession deactivates immediately after each turn3.  
> 6. **Widget Suitability & Removable Background Audit (DPLA §6.4.1):** Verify that every WidgetFamily.systemSmall widget either uses .containerBackground(for: .widget) and functions without unlocking the iPhone, or explicitly sets .disfavoredLocations(\[.carPlay\], for: \[.systemSmall\])4.  
> 7. **NowPlaying Framework Exclusivity (iOS 27):** Confirm the codebase does not mix legacy MPNowPlayingInfoCenter/MPRemoteCommandCenter calls with the iOS 27 NowPlaying (MediaSession) framework13.  
> 8. **iPhone Duo Screenshot Readiness (April 2027 Deadline):** If building with the iOS 27.1+ SDK for spring 2027 updates, prepare iPhone Duo screenshots as required by App Store Connect starting April 202713.

#### **5\. Testing Before Publishing: Xcode 27 Device Hub, Simulators, Head Units, XCTest Limits, TestFlight, and HomeView Hardware**

In Xcode 27.0–27.2, Apple eliminated the standalone Simulator.app and replaced it with **Device Hub** (DeviceHub.app), unifying virtual simulators and physical devices into a single sidebar \[Developer-observed: Apple Developer Forums & RocketSim, 2026-09 / 2026-10; High Confidence\] 32. Crucially, as documented in the October 13, 2026 *CarPlay Developer Guide* and verified in Apple Developer Forum thread 834440, **Device Hub does not support opening a CarPlay display on a virtual iOS 27 Simulator**; instead, you must connect a **physical iPhone via a USB cable**, select the physical iPhone in Device Hub, and choose **CarPlay Simulator** from the **Device** menu \[Apple-documented / Developer-observed: CarPlay Developer Guide & Apple Developer Forums, 2026-10-13 / 2026-11; High Confidence\] 3. The legacy virtual simulator path (I/O → External Displays → CarPlay with defaults write com.apple.iphonesimulator CarPlayExtraOptions \-bool YES, or the standalone *CarPlay Simulator* app in *Additional Tools for Xcode*) remains usable only on Xcode 26.x environments \[Developer-observed: Platform APIs Audit, 2026-10; High Confidence\] 10.  
Because XCUITest cannot query accessibility (AX) elements or synthesize gestures on either the CarPlay external display or CarPlay Simulator (thread 831782), automated testing must combine @MainActor XCTest unit tests (which instantiate CarPlaySceneDelegate and assert against the CPTemplate hierarchy in memory) with macOS window-level screenshot/gesture automation \[Developer-observed: Apple Developer Forums Thread 831782, 2026-06-10; High Confidence\] 33. Before App Store submission, teams must also test signed TestFlight builds on physical vehicle head units and physical **Apple HomeView (\$299)** hardware: real vehicles expose wireless audio route latency (\~1100 ms on .playback \+ .default vs. \~160 ms on .playAndRecord \+ .default, which drops audio quality to 24 kHz mono) and supportsVideoPlayback \== false (vehicle doesn't support features requiring asset) on cars lacking the 1920×1080 / HEVC / 4 GB RAM video hardware floor \[Developer-observed: BigGo Finance & Apple Developer Forums, 2026-10 / 2026-11; High Confidence\] 31, while physical HomeView units are required to catch the developer-observed PebblePlay bug where certain working CarPlay audio apps hang on an indefinite loading spinner upon launch \[Developer-observed: Apple Developer Forums, 2026-11-17; High Confidence\] 31.

##### **Deliverable (4): Concrete Pre-Submission Test Matrix**

| Test Environment | Target OS / Build | Hardware Required | Primary Scenarios to Validate | Known Failure Modes to Check |
| :---- | :---- | :---- | :---- | :---- |
| **1\. @MainActor XCTest Suite** | iOS 26.4 & iOS 27.2 SDK | Mac (Xcode 27.1 / 27.2) | Unit-test CarPlaySceneDelegate cold launch (without initializing SwiftUI WindowGroup); verify template depth ≤5 (Audio/Video) or ≤3 (Conversational); verify tab count ≤4 and voice states ≤53. | Crash when accessing uninitialized SwiftUI @StateObject; runtime exception on \>4 tabs or unpermitted template3. |
| **2\. Xcode Previews (WidgetKit & ActivityKit)** | iOS 26.0+ & iOS 27.2 SDK | Mac (Xcode 27.1 / 27.2) | Preview WidgetFamily.systemSmall in StandBy and standard Home Screen contexts; preview ActivityFamily.small Live Activity4. | Missing .containerBackground(for: .widget) warning overlay; clipped typography at distance; interactive buttons left on CarPlay Live Activity4. |
| **3\. Xcode 27 Device Hub → CarPlay Simulator** | iOS 26.4 & iOS 27.2 (on USB iPhone) | Mac \+ **Physical iPhone via USB cable**3 | Test 800×480 @2x (16:9) and 1920×720 (8:3) layouts; toggle "Standard Video Playback" / supportsVideoPlayback mid-session to verify automatic video-to-audio fallback; test CPVoiceControlTemplate showOverlayTemplate and MiniPlayer10. | CPListSection header disappearing when detailText/headerImage is set (FB24061858); CPListItem single-line truncation on iOS 27; CPNowPlayingTemplate client freeze (FB24840951)31. |
| **4\. Physical Vehicle Head Unit (Wired & Wireless)** | iOS 26.5 & iOS 27.2 (TestFlight build) | Physical iPhone \+ OEM / Aftermarket Head Unit | Cold-launch CarPlay with iPhone locked in pocket; test wired vs. wireless audio latency and interruption recovery (phone call vs. Siri music); test dynamic 12-item list limit while driving13. | 24 kHz mono audio degradation on wireless .playAndRecord; supportsVideoPlayback \== false on head units without theme assets support; missing A–Z sectionIndexTitle index bar on iOS 2731. |
| **5\. Physical Apple HomeView Hardware** | **HomeView Software 27.2 (24V526)** \+ iOS 27.2+ | Physical HomeView (\$299) \+ Paired iPhone on same Wi-Fi5 | Face-recognition profile switch (up to 6 users); launch CarPlay Audio/Video app from HomeView Home Screen via PebblePlay; test systemSmall widget on Home Screen, Modular face, and Modular face in Night Mode / Ambient Dark Mode; test Proximity Handoff16. | **Indefinite loading spinner** when launching CarPlay audio app on HomeView (PebblePlay handshake timeout); private personal widget data exposed on shared kitchen counter31. |

#### **6\. Gaps and Roadmap: Developer Requests vs. Announced and Rumoured HomeView Features**

Across the Apple Developer Forums and WWDC26 Q\&A sessions (June–November 2026), third-party developers are pressing Apple to address four primary tooling and API gaps: (1) restoring **virtual CarPlay Simulator support inside Xcode 27 Device Hub** so engineers and CI servers do not require a physical USB-connected iPhone (thread 834440\) \[Developer-observed: Apple Developer Forums, 2026-10 / 2026-11; High Confidence\] 11; (2) shipping a **dedicated HomeView Simulator, native SDK, and WidgetLocation.homeView enum case** so developers can debug the PebblePlay indefinite loading spinner and opt personal lock-screen widgets out of shared household counters without hiding them in the user's car \[Developer-observed: Apprankr, Daily.dev & Apple Developer Forums, 2026-10-22 / 2026-11-17; High Confidence\] 8; (3) exposing **CarPlay XCUITest accessibility (AX) elements and pre-render CPGridTemplate column counts** (thread 831782, June 10, 2026\) \[Developer-observed: Apple Developer Forums WWDC26 CarPlay Q\&A, 2026-06-10; High Confidence\] 33; and (4) fixing iOS 27 regressions including FB24840951 (CPNowPlayingTemplate client freeze), FB24061858 (disappearing CPListSection headers), single-line CPListItem truncation, missing A–Z list index bars, and zero safeAreaInsets on CPWindow when running on iPhone Duo (iOS 27.1) \[Developer-observed: Apple Developer Forums, 2026-10 / 2026-11; High Confidence\] 31.

| Date | Feature / Milestone | Epistemic Status & Source |
| :---- | :---- | :---- |
| **2026-10-13** | Apple announces **Apple HomeView** (\$299, 7-inch display, Tabletop & Wall-Mounted), updates DPLA §§6.4.1–6.4.2, and publishes the October 2026 *CarPlay Developer Guide* bridging CarPlay Audio/Video apps and systemSmall widgets to HomeView. | **Apple-documented** (Apple Newsroom, DPLA & CarPlay Developer Guide, 2026-10-13; High Confidence) 3. |
| **2026-10-18** | Next-generation HomeView model featuring a **robotic arm** that swivels the screen to track users around a room, targeted for 2027\. | **Rumoured** (*Bloomberg Power On* newsletter via 9to5Mac, 2026-10-18; Medium Confidence) 16. |
| **2026-11-02** | Hidden firmware code reveals HomeView can function as a **HomeKit security camera** with built-in household privacy protections. | **Developer-observed** (Firmware code leak by pdfu via 9to5Mac, 2026-11-02; High Confidence) 16. |
| **2026-11-02** | Larger, higher-end **"HomeView Ultra"** smart display model in development for 2027 release. | **Rumoured** (*The Information* via 9to5Mac, 2026-11-02; Medium Confidence) 16. |
| **2026-11-03 to 2026-11-05** | **iOS 27.3 Beta 1** adds "ConversationalApps" category flag to HomeView's PebblePlay CarPlay bridge (defaults write com.apple.HomeView DefaultAppCategory \-string "ConversationalApps") plus bidirectional audio and interruption groundwork for third-party AI chatbots (ChatGPT, Claude, Gemini). | **Developer-observed** (iOS 27.3 beta 1 code inspected by pdfu via 9to5Mac & TechBytes, 2026-11-05; High Confidence) 16. |
| **2026-11-10** | Two major unannounced software features in development for upcoming HomeView software updates. | **Rumoured** (Industry leaks via 9to5Mac, 2026-11-10; Low Confidence) 16. |
| **2026-11-12 to 2026-11-13** | Apple releases **HomeView Software 27.2 (24V526)** and launches HomeView in retail stores (US, UK, AU, CA, IN, NZ, SG; excluded from EU due to Siri AI regulatory hold). | **Apple-documented** (Apple Newsroom & Apple Support 149851, 2026-11-12 / 2026-11-13; High Confidence) 35. |
| **Early 2027** | Launch of **Schneider Home Power Mount PoE Wired** accessory for wall-mounted HomeView models. | **Apple-documented** (Apple Newsroom, 2026-11-13; High Confidence) 51. |
| **April 2027** | Mandatory App Store Connect requirement: all apps compiled with the **iOS 27.1+ SDK** must supply **iPhone Duo** screenshots upon submission. | **Apple-documented** (Platform APIs Audit, 2026-10; High Confidence) 13. |

#### **7\. Deliverable (6): Answers to the Six Open Questions from Earlier Research**

##### **(a) Can one app hold both the audio and video CarPlay entitlements, given WWDC26 session 212 recommended both while the October 2026 CarPlay Developer Guide and entitlement reference pages forbid combining them?**

**No (High Confidence).** \<CONFLICTING\_EVIDENCE\>\[In June 2026, WWDC26 Session 212 ("Rev up your CarPlay app") recommended that apps with content useful as both video and audio include both com.apple.developer.carplay-video and com.apple.developer.carplay-audio so the app remains visible on the CarPlay Home Screen in cars without video support. However, Apple's October 13, 2026 CarPlay Developer Guide (p. 6\) and the official Apple Developer Documentation pages for both com.apple.developer.carplay-audio and com.apple.developer.carplay-video explicitly prohibit combining them: "In iOS 26.3 and later, you can't combine this entitlement with other CarPlay entitlements" and "Multiple categories cannot be combined in a single app, with the exception of EV charging and fueling apps." Furthermore, in November 2026, App Review rejected builds combining CarPlay Video with another entitlement under Guideline 2.5.1.\]\</CONFLICTING\_EVIDENCE\> \[Apple-documented / Developer-observed: WWDC26 Session 212, CarPlay Audio & Video Entitlement Docs, CarPlay Developer Guide & Apple Developer Forums, 2026-06 / 2026-10-13 / 2026-11-12\] 2. To support both audio and video in a single app, request **only com.apple.developer.carplay-audio**: as documented on the com.apple.developer.carplay-audio reference page and Page 10 of the October 13, 2026 *CarPlay Developer Guide*, the Audio entitlement explicitly *"permits the app to play audio-only content or video content with an audio component. Apps with this entitlement can also run on HomeView"* provided the app supports AirPlay video streaming \[Apple-documented: CarPlay Audio App Entitlement & CarPlay Developer Guide, 2026-10-13; High Confidence\] 2. Reserve com.apple.developer.carplay-video exclusively for pure video streaming apps that have no audio-only CarPlay browsing experience3.

##### **(b) Does disfavoredLocations(\[.carPlay\]) also hide a widget on HomeView, and is there any way to target HomeView separately?**

**Yes, .disfavoredLocations(\[.carPlay\], for: \[.systemSmall\]) applies to both CarPlay and HomeView simultaneously, and there is no API in Xcode 27.0–27.2 to target or opt out of HomeView separately (High Confidence).** Under DPLA Section 6.4.1 (revised October 13, 2026), Apple binds CarPlay and HomeView widget availability to the single WidgetLocation.carPlay (iOS 26.0+) location modifier \[Apple-documented: DPLA §6.4.1 & WidgetLocation.carPlay Docs, 2026-10-13\] 6. Per the October 13, 2026 *CarPlay Developer Guide*, calling .disfavoredLocations(\[.carPlay\]) causes the widget to be *"grouped in Settings with an indication that your widget is not optimized for CarPlay"* (and suppresses default promotion on HomeView) \[Apple-documented: CarPlay Developer Guide, 2026-10-13; High Confidence\] 3. Note that if a widget sets .containerBackgroundRemovable(false), WidgetKit excludes it from galleries that require removable backgrounds—which includes StandBy, CarPlay, and HomeView's **Modular face**, while still permitting it on the iPhone Home Screen \[Apple-documented: WidgetKit Docs & Widgets HIG, 2026-10-13; High Confidence\] 4.

##### **(c) What are the exact templates allowed for the Public Safety and Navigation categories on iOS 26 versus iOS 27?**

Both categories have a maximum depth of **5 templates** (including the root CPMapTemplate) \[Apple-documented: CarPlay Developer Guide, 2026-10-13; High Confidence\] 3. For **Navigation (com.apple.developer.carplay-maps)**, **iOS 26.x** allows CPMapTemplate (root over CPWindow), CPActionSheetTemplate, CPAlertTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPNowPlayingTemplate, CPPointOfInterestTemplate, CPSearchTemplate, CPTabBarTemplate, and CPVoiceControlTemplate (full-screen modal), plus CPRouteSegment / CPNavigationWaypoint route sharing in iOS 26.4+ \[Apple-documented: CarPlay Framework Docs & WWDC26 Session 212, 2026-06 / 2026-10; High Confidence\] 10; **iOS 27.x** adds CPMapPanel (CPMapTemplate.showPanel(\_:completion:) / hidePanel(completion:)) for custom panels over the map and non-blocking overlay presentation of CPVoiceControlTemplate over CPMapTemplate via CPInterfaceController.showOverlayTemplate(\_:animated:completion:) \[Apple-documented: CarPlay Developer Guide & CPInterfaceController Docs, 2026-10-13; High Confidence\] 3. For **Public Safety (com.apple.developer.carplay-public-safety)**, **iOS 26.x** allows CPMapTemplate (assigned as root template with CPNavigationSession for emergency dispatch and routing), CPActionSheetTemplate, CPAlertTemplate, CPContactTemplate, CPGridTemplate, CPInformationTemplate, CPListTemplate, CPPointOfInterestTemplate, CPSearchTemplate, CPTabBarTemplate, and CPVoiceControlTemplate (plus CarPlay notification support, which Navigation lacks) \[Apple-documented: CarPlay Developer Guide, 2026-10-13; High Confidence\] 3; **iOS 27.x** adds CPInterfaceController.showOverlayTemplate(\_:animated:completion:) for presenting CPVoiceControlTemplate over the dispatch map and CPMapPanel support \[Apple-documented: CarPlay Developer Guide & CPInterfaceController Docs, 2026-10-13; High Confidence\] 3.

##### **(d) May CPVoiceControlTemplate be set as the root template on iOS 26.4 or later, or must be presented over another root?**

**It must be presented over another root template (presentTemplate(\_:animated:completion:) on iOS 26.4+ or showOverlayTemplate(\_:animated:completion:) on iOS 27.0+); it cannot be set as the root template (High Confidence).** Apple's CPVoiceControlTemplate documentation (activateVoiceControlState(withIdentifier:)) and CPInterfaceController documentation explicitly specify that CPVoiceControlTemplate is a modal or overlay template presented via CPInterfaceController over the root navigation hierarchy, and that calling activateVoiceControlState(withIdentifier:) before presenting the template has no effect \[Apple-documented: CPVoiceControlTemplate & CPInterfaceController Docs, 2026-10; High Confidence\] 10. In a Voice-Based Conversational app (which has a 3-template hierarchy depth including the root), set a lightweight CPListTemplate, CPGridTemplate, or CPTabBarTemplate as the root via setRootTemplate(\_:animated:completion:) and immediately present CPVoiceControlTemplate on connect so voice is the primary modality upon launch \[Apple-documented: CarPlay Developer Guide, 2026-10-13; High Confidence\] 3.

##### **(e) Do arbitrary third-party Live Activities appear on HomeView?**

**Unconfirmed for third-party apps due to conflicting Apple primary sources (Medium Confidence).** \<CONFLICTING\_EVIDENCE\>\[Apple's October/November 2026 consumer press releases and the Apple HomeView User Guide ("View Live Activities") state that HomeView supports Live Activities at the top of the screen (specifically highlighting timers and Now Playing music controls). Conversely, Apple's October 2026 Live Activities Human Interface Guidelines list only iPad, iPhone, Mac, Apple Watch, and CarPlay (omitting HomeView), and DPLA Section 6.4 explicitly authorizes third-party iOS widgets (§6.4.1) and CarPlay apps (§6.4.2) on HomeView while omitting any mention of third-party Live Activities.\]\</CONFLICTING\_EVIDENCE\> \[Apple-documented / Developer-observed: Apple Newsroom, Apple HomeView User Guide, Live Activities HIG, DPLA §6.4 & Blake Crosley Audit, 2026-10-13 / 2026-11-13\] 6. Consequently, while built-in HomeView activities (timers, alarms, media playback) render in HomeView's top activity slot, teams cannot rely on arbitrary third-party iPhone ActivityKit activities bridging to HomeView and should implement WidgetFamily.systemSmall widgets alongside .supplementalActivityFamilies(\[.small\])3.

##### **(f) What is the maximum navigation depth for Video apps?**

**5 templates, including the root template (High Confidence).** In the October 13, 2026 *CarPlay Developer Guide* (Page 16), Apple groups Audio and Video together under a single specification column ("Audio, video") \[Apple-documented: CarPlay Developer Guide p. 16, 2026-10-13\] 3. \<INFERENCE from="CarPlay Developer Guide (2026-10-13) Page 16 grouping 'Audio, video' into a single template specification column and CarPlay Audio entitlement documentation permitting video playback under the same 5-template hierarchy"\>Because Audio and Video share the exact same template column ("Audio, video") in the CarPlay Developer Guide and the Audio entitlement itself supports video playback up to 5 templates deep, Video apps are governed by the 5-template maximum navigation depth (including the root template).\</INFERENCE\>2.

### **Secondary Research Question 2: What is the current state, and what is the strongest supporting evidence for it?**

As of November 18, 2026, Apple has unified in-vehicle (CarPlay and CarPlay Ultra) and ambient smart-home (Apple HomeView) third-party app distribution around a single template-and-widget projection architecture hosted on the user's paired iPhone or iPad \[Apple-documented: DPLA §6.4 & CarPlay Developer Guide, 2026-10-13; High Confidence\] 3. The strongest supporting evidence for this architecture is the coordinated October 13, 2026 revision of three primary Apple legal and technical artifacts, corroborated by shipping HomeView firmware on November 12–13, 2026: first, **DPLA Sections 6.4.1 and 6.4.2**, which establish the legal mechanism for Apple to surface iOS systemSmall widgets and designated CarPlay-entitled apps on HomeView without a separate store submission6; second, the **October 2026 *CarPlay Developer Guide*** (Footnote \*2) and **CarPlay HIG**, which confirm verbatim that *"CarPlay audio and video apps also work on Apple HomeView without requiring you to make any modifications to your app"*3; and third, binary inspection of **HomeView Software 27.2 (build 24V526)** on HomeAccessory17,2 and **iOS 27.3 beta 1**, which verify that HomeView runs a tvOS 27.2 derivative whose PebblePlay daemon acts as a CarPlay receiver bridging category-allowlisted apps from the paired iOS device7.

### **Secondary Research Question 3: What are the contrasting viewpoints or competing evidence?**

Three substantive areas of competing evidence and policy tension shape engineering decisions in November 2026\. First, on **dual Audio and Video entitlements**, WWDC26 Session 212 (June 2026\) explicitly advised developers of dual-media apps to include both com.apple.developer.carplay-audio and com.apple.developer.carplay-video, whereas the October 13, 2026 *CarPlay Developer Guide*, the official entitlement documentation pages (for iOS 26.3+), and November 2026 App Store Review Guideline 2.5.1 rejections forbid combining them—requiring teams to follow the written October 2026 policy and use carplay-audio alone \[Apple-documented / Developer-observed: WWDC26 Session 212, CarPlay Entitlement Docs & Apple Developer Forums, 2026-06 / 2026-10-13 / 2026-11-12; High Confidence\] 2. Second, on **HomeView Live Activities**, Apple's consumer press releases and the *Apple HomeView User Guide* feature "View Live Activities" prominently, while the *Live Activities HIG* and DPLA Section 6.4 omit HomeView entirely, leaving third-party ActivityKit bridging undocumented6. Third, on **CarPlay Video adoption**, while Apple markets parked video playback (com.apple.developer.carplay-video) in iOS 27 and CarPlay Simulator renders it smoothly, industry analyses and developer forum diagnostics (DTS Case-ID 23112107\) show that major streaming services (Netflix, YouTube, Disney+) have not shipped CarPlay Video apps as of November 2026, and production wireless CarPlay vehicles return CPSessionConfiguration.supportsVideoPlayback \== false (vehicle doesn't support features requiring asset) because automakers have not yet deployed the required vehicle firmware handshake—making Apple HomeView the primary real-world display where CarPlay Video apps actually render video today \[Developer-observed: Macworld, BigGo Finance & Apple Developer Forums, 2026-10 / 2026-11; High Confidence\] 31.

### **Secondary Research Question 4: What changed recently, and what is the trajectory?**

Between February and November 2026, Apple transformed CarPlay from an in-dash menu hierarchy into a cross-device ambient app and AI assistant runtime. The catalyst was the February 2026 debut of com.apple.developer.carplay-voice-based-conversation in iOS 26.4, followed in September 2026 (iOS 27.0) by non-blocking CPVoiceControlTemplate overlays (showOverlayTemplate) across all 11 CarPlay categories—rapidly adopted by Anthropic's Claude (September 4, 2026), OpenAI's ChatGPT, and Google's Gemini Live (November 11, 2026)—and the October–November 2026 launch of Apple HomeView \[Apple-documented / Developer-observed: CarPlay Developer Guide, Mapbox & 9to5Mac, 2026-08-21 / 2026-10-13 / 2026-11-11; High Confidence\] 1. Looking ahead into 2027, the discovery of "ConversationalApps" and bidirectional audio plumbing in iOS 27.3 beta 1's PebblePlay bridge demonstrates that Apple's trajectory is to selectively unlock additional CarPlay entitlement categories on HomeView over time (while preparing higher-end hardware such as HomeView Ultra and a robotic-arm tabletop display rumoured for 2027), rather than fragmenting its developer ecosystem with a standalone HomeView App Store16.

## **Evidence Table**

Every source integrated into this synthesis was validated against the source-discipline criteria: Apple official developer documentation, legal agreements (DPLA), support guides, and WWDC sessions serve as primary authoritative evidence; developer forum bug reports with Feedback/Case IDs (FB24840951, FB24061858, thread 834440, thread 850675, DTS 23112107\) and IPSW binary inspections provide primary empirical engineering observations.

| Claim | Primary Source | Publication Date | Evidence Type | URL |
| :---- | :---- | :---- | :---- | :---- |
| HomeView runs HomeView Software 27.2 (24V526), internally identified as "Apple TVOS" 27.2 on HomeAccessory17,2. | Apple Developer Releases; Apple Support 149851; IPSW.me / Reddit r/HomeKit IPSW Audit *(Meets criteria: official release feed & direct firmware plist inspection)* | 2026-11-12 | Apple-documented / Developer-observed | https\://developer.apple.com/news/releases/ ; https\://support.apple.com/en-us/149851 ; https\://ipsw.me/download/HomeAccessory17,2/24V526/18 |
| Apple HomeView launched Nov 13, 2026 (\$299, 7-inch display, 6-user face recognition, Siri AI beta in 27.2, no EU availability at launch). | Apple Newsroom *(Meets criteria: official vendor announcement)* | 2026-11-13 | Apple-documented | https\://www\.apple.com/au/newsroom/2026/11/apple-homeview-available-today/51 |
| DPLA §6.4.1 authorizes iOS app widgets on CarPlay and HomeView (with disfavoredLocations opt-out); §6.4.2 authorizes CarPlay-entitled apps in designated categories on HomeView. | Apple Developer Program License Agreement (DPLA) & Apple Developer News *(Meets criteria: primary legal contract)* | 2026-10-13 | Apple-documented | https\://developer.apple.com/support/terms/apple-developer-program-license-agreement/ ; https\://developer.apple.com/news/?id=17mwd36z6 |
| All 11 CarPlay categories, permitted CPTemplate matrices, max depths (5, 3, and 2-\>3), HomeView Audio/Video bridging (\*2), and Xcode 27 Device Hub USB iPhone steps. | Apple *CarPlay Developer Guide* (October 2026 Edition) *(Meets criteria: primary official engineering specification)* | 2026-10-13 | Apple-documented | https\://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf3 |
| com.apple.developer.carplay-audio permits audio or video-with-audio, runs on HomeView, and cannot be combined with other CarPlay entitlements in iOS 26.3+. | Apple Developer Documentation — com.apple.developer.carplay-audio & com.apple.developer.carplay-video *(Meets criteria: official API entitlement spec)* | 2026-10-13 | Apple-documented | https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio ; https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video2 |
| WWDC26 Session 212 recommended both Audio and Video entitlements, introduced MiniPlayer (allowsMiniPlayer), CPPlaybackConfiguration, and AVAudioSession .playAndRecord rules. | WWDC26 Session 212 ("Rev up your CarPlay app") via wwdc.ai & Apple Developer Forums *(Meets criteria: official conference session record)* | 2026-06 | Apple-documented | https\://wwdc.ai/2026/21210 |
| App Review rejects apps combining CarPlay Video with another CarPlay entitlement under Guideline 2.5.1; Apple removed *APTV* (Oct 23, 2026\) for unentitled browser video. | Apple Developer Forums & BigGo Finance *(Meets criteria: direct empirical App Review rejection log & verified takedown report)* | 2026-11-06 / 2026-11-12 | Developer-observed | https\://developer.apple.com/forums/tags/carplay ; https\://finance.biggo.com/news/3ed0b1f7-b43b-4637-8ff4-4949401ad21111 |
| CPVoiceControlTemplate (max 5 states, rate-limited, actionButtons in iOS 26.4+) must be presented via presentTemplate or showOverlayTemplate (iOS 27+) before activating states. | Apple Developer Documentation — CPVoiceControlTemplate, CPVoiceControlState, & CPInterfaceController *(Meets criteria: official API reference)* | 2026-10 | Apple-documented | https\://developer.apple.com/documentation/carplay/cpvoicecontroltemplate ; https\://developer.apple.com/documentation/carplay/cpinterfacecontroller14 |
| HomeView widgets use WidgetFamily.systemSmall on Home Screen and Modular face (with background removed on Modular face and in Night Mode); CarPlay uses WidgetLocation.carPlay. | Apple Human Interface Guidelines — Widgets & CarPlay; WidgetKit Docs *(Meets criteria: official design & API documentation)* | 2026-10-13 | Apple-documented | https\://developer.apple.com/design/human-interface-guidelines/widgets ; https\://developer.apple.com/design/human-interface-guidelines/carplay ; https\://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget26 |
| iOS 27.3 beta 1 adds "ConversationalApps" category to PebblePlay (HomeView's CarPlay bridge) plus bidirectional audio routing groundwork. | 9to5Mac & TechBytes (citing iOS 27.3 beta 1 code inspection by pdfu) *(Meets criteria: verifiable beta binary string & defaults key extraction)* | 2026-11-05 | Developer-observed | https\://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/ ; https\://techbytes.app/posts/chatbots-might-be-coming-to-apples-homeview/16 |
| Xcode 27 replaces Simulator.app with Device Hub, requiring a physical USB iPhone for CarPlay Simulator (thread 834440); XCUITest cannot inspect CarPlay (thread 831782). | Apple Developer Forums & Platform APIs Research Report *(Meets criteria: primary engineering forum confirmation & SDK header audit)* | 2026-06-10 / 2026-11 | Developer-observed | https\://developer.apple.com/forums/forums/topics/app-and-system-services/app-and-system-services-carplay ; https\://developer.apple.com/forums/thread/831782 ; https\://github.com/djensenius/audiobookshelf-apple/blob/main/docs/research/platform-apis.md13 |

## **Knowledge Gaps**

> 1. **Root Cause of the HomeView PebblePlay Indefinite Loading Spinner (Hardware/Runtime Opacity):** \<MISSING\_DATA\>\[Exact diagnostic logs or Apple DTS resolution for why certain working CarPlay audio apps display an indefinite loading spinner when launched on physical HomeView units running 27.2 (build 24V526), reported on the Apple Developer Forums on November 17, 2026 (0 replies as of November 18, 2026); requires sysdiagnose inspection from a paired iPhone and HomeView during a failed PebblePlay scene connection.\]\</MISSING\_DATA\>31.  
> 2. **Public Activation Date for ConversationalApps on HomeView (Unreleased Beta Feature):** \<INSUFFICIENT\_EVIDENCE\>\[Whether Apple will enable the "ConversationalApps" flag in PebblePlay for the public release of iOS 27.3 / HomeView Software 27.3 (expected December 2026\) or hold it for a 27.4+ update; researcher pdfu noted on November 5, 2026 that the bidirectional audio and interruption plumbing in iOS 27.3 beta 1 is "still not fully wired up."\]\</INSUFFICIENT\_EVIDENCE\>16.  
> 3. **Third-Party ActivityKit Live Activities Rendering Rules on HomeView (Documentation Omission):** \<MISSING\_DATA\>\[Official Apple developer documentation clarifying whether third-party iPhone ActivityKit Live Activities (with .supplementalActivityFamilies(\[.small\])) bridge to HomeView's top activity slot alongside built-in Timers and Apple Music, as the Live Activities HIG and DPLA §6.4 omit HomeView while the consumer Apple HomeView User Guide includes "View Live Activities".\]\</MISSING\_DATA\>8.  
> 4. **Exact Numeric Rate-Limit Threshold for CPVoiceControlTemplate.activateVoiceControlState(withIdentifier:) (Undocumented Constant):** \<MISSING\_DATA\>\[The exact millisecond cooldown interval enforced by CPVoiceControlTemplate when throttling rapid calls to activateVoiceControlState(withIdentifier:); Apple's documentation states that the template applies a rate limit and ignores rapid changes without publishing the numeric threshold in header files.\]\</MISSING\_DATA\>53.

## **Recommended Next Steps**

> 1. **Submit the Single Primary CarPlay Entitlement Request Immediately (com.apple.developer.carplay-audio or com.apple.developer.carplay-voice-based-conversation):**  
   * *Rationale:* Because entitlement approvals currently take **15 to 30+ days** and suffer from web-form submission glitches84, submitting the request immediately unblocks provisioning profile generation. Frame the application strictly around in-vehicle safety and utility (never HomeView alone)8, and apply for **only one** entitlement to avoid App Review Guideline 2.5.1 rejection2.  
> 2. **Procure Physical Retail HomeView Hardware (\$299) and Verify PebblePlay Cold-Launch Handshake on Software 27.2 (24V526):**  
   * *Rationale:* Because Xcode 27 ships no HomeView simulator and developers have observed working CarPlay audio apps hanging on an indefinite loading spinner on physical HomeView units8, the team must test CPTemplateApplicationSceneDelegate.templateApplicationScene(\_:didConnect:) latency and setRootTemplate(\_:animated:completion:) completion timing against a real HomeView before marketing HomeView support.  
> 3. **Audit and Migrate Media Playback State to Isolate Legacy MPNowPlayingInfoCenter from iOS 27 NowPlaying (MediaSession):**  
   * *Rationale:* Mixing legacy MediaPlayer APIs with the new iOS 27 NowPlaying framework produces undefined runtime behavior13, and apps combining MPNowPlayingInfoCenter with ApplicationMusicPlayer hit the FB24840951 frozen Now Playing template bug on iOS 2731. Standardize on a single Now Playing pipeline and test with CPNowPlayingTemplate.shared.allowsMiniPlayer both enabled and disabled10.  
> 4. **Benchmark AVAudioSession Latency and State-Transition Throttling on a Wireless CarPlay Head Unit and iOS 27.3 Beta:**  
   * *Rationale:* If building a conversational or voice-enabled app, test .playAndRecord \+ .default on a physical wireless CarPlay unit to verify acceptable speech clarity under the 24 kHz mono duplex route (\~160 ms latency)10, debounce activateVoiceControlState(withIdentifier:) calls so state transitions are never silently dropped by Apple's rate limiter53, and test against iOS 27.3 beta as PebblePlay wires up "ConversationalApps" for HomeView16.

#### **Works cited**

> 1. flutter\_carplay 1.7.0+2 \| Flutter package \- Pub.dev, [https\://pub.dev/packages/flutter\_carplay/versions/1.7.0+2](https://pub.dev/packages/flutter_carplay/versions/1.7.0+2)  
> 2. CarPlay Audio App \| Apple Developer Documentation, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio)  
> 3. CarPlay Developer Guide, [https\://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)  
> 4. Displaying the right widget background \- Apple Developer, [https\://developer.apple.com/documentation/widgetkit/displaying-the-right-widget-background](https://developer.apple.com/documentation/widgetkit/displaying-the-right-widget-background)  
> 5. Apple HomeView \- Technical Specifications, [https\://www\.apple.com/au/apple-homeview/specs/](https://www.apple.com/au/apple-homeview/specs/)  
> 6. Apple Developer Program License Agreement \- Support, [https\://developer.apple.com/support/terms/apple-developer-program-license-agreement/](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)  
> 7. Apple HomeView, supporto ai chatbot terzi sempre più probabile, [https\://www\.hdblog.it/apple/articoli/n676084/apple-homeview-chatbot-terze-parti/](https://www.hdblog.it/apple/articoli/n676084/apple-homeview-chatbot-terze-parti/)  
> 8. Apple HomeView for Developers: What Apple Said on Day One, [https\://blakecrosley.com/blog/apple-homeview-developers-day-one](https://blakecrosley.com/blog/apple-homeview-developers-day-one)  
> 9. CarPlay Video App \| Apple Developer Documentation, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video)  
> 10. Rev up your CarPlay app (Session 212\) \- WWDC 2026, [https\://wwdc.ai/2026/212](https://wwdc.ai/2026/212)  
> 11. CarPlay \| Apple Developer Forums, [https\://developer.apple.com/forums/tags/carplay](https://developer.apple.com/forums/tags/carplay)  
> 12. CPPlaybackConfiguration \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpplaybackconfiguration](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration)  
> 13. [https\://github.com/djensenius/audiobookshelf-apple/blob/main/docs/research/platform-apis.md](https://github.com/djensenius/audiobookshelf-apple/blob/main/docs/research/platform-apis.md)  
> 14. CPInterfaceController \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpinterfacecontroller](https://developer.apple.com/documentation/carplay/cpinterfacecontroller)  
> 15. showOverlayTemplate(\_:animated:completion:) \| Apple Developer, [https\://developer.apple.com/documentation/carplay/cpinterfacecontroller/showoverlaytemplate(\_:animated:completion:)](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/showoverlaytemplate\(_:animated:completion:\))  
> 16. HomeView will support third-party AI chatbots, suggests code, [https\://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/](https://9to5mac.com/2026/11/05/homeview-will-support-third-party-ai-chatbots-suggests-code/)  
> 17. Chatbots might be coming to Apple's HomeView \- Tech Bytes, [https\://techbytes.app/posts/chatbots-might-be-coming-to-apples-homeview/](https://techbytes.app/posts/chatbots-might-be-coming-to-apples-homeview/)  
> 18. HomeView software 27.2 (24V526) for Apple ... \- IPSW Downloads, [https\://ipsw.me/download/HomeAccessory17,2/24V526/](https://ipsw.me/download/HomeAccessory17,2/24V526/)  
> 19. Releases \- Apple Developer, [https\://developer.apple.com/news/releases/](https://developer.apple.com/news/releases/)  
> 20. r/HomeKit \- Reddit, [https\://www\.reddit.com/r/HomeKit/top/?after=dDNfMXh1bTZ3dA%3D%3D\&sort=top\&t=DAY](https://www.reddit.com/r/HomeKit/top/?after=dDNfMXh1bTZ3dA%3D%3D&sort=top&t=DAY)  
> 21. Some findings after digging through HomeView's IPSW : r/HomeKit, [https\://www\.reddit.com/r/HomeKit/comments/1xv7m8k/some\_findings\_after\_digging\_through\_homeviews\_ipsw/](https://www.reddit.com/r/HomeKit/comments/1xv7m8k/some_findings_after_digging_through_homeviews_ipsw/)  
> 22. iOS 26.4 Paves the Way for ChatGPT and Gemini in CarPlay, [https\://www\.idropnews.com/news/ios-26-4-carplay-ai-chatbots-chatgpt-gemini/260078/](https://www.idropnews.com/news/ios-26-4-carplay-ai-chatbots-chatgpt-gemini/260078/)  
> 23. bradford-tech/expo-carplay CDN by jsDelivr, [https\://www\.jsdelivr.com/package/npm/@bradford-tech/expo-carplay](https://www.jsdelivr.com/package/npm/@bradford-tech/expo-carplay)  
> 24. CarPlay on iOS 27 lets a voice assistant run over a live map, [https\://www\.mapbox.com/blog/carplay-on-ios-27-lets-a-voice-assistant-run-over-a-live-map](https://www.mapbox.com/blog/carplay-on-ios-27-lets-a-voice-assistant-run-over-a-live-map)  
> 25. [https\://9to5mac.com/2026/10/14/homeview-can-display-third-party-widgets-from-your-iphone/](https://9to5mac.com/2026/10/14/homeview-can-display-third-party-widgets-from-your-iphone/)  
> 26. carPlay \| Apple Developer Documentation, [https\://developer.apple.com/documentation/widgetkit/widgetlocation/carplay?changes=\_\_9](https://developer.apple.com/documentation/widgetkit/widgetlocation/carplay?changes=__9)  
> 27. Issue \#92: Xcode 27.1 is final, App Review names... \- daily.dev, [https\://daily.dev/posts/issue-92-xcode-27-1-is-final-app-review-names-bait-and-switch-and-your-widgets-are-headed-to-hom-cxz0z4p5a](https://daily.dev/posts/issue-92-xcode-27-1-is-final-app-review-names-bait-and-switch-and-your-widgets-are-headed-to-hom-cxz0z4p5a)  
> 28. Widgets \| Apple Developer Documentation, [https\://developer.apple.com/design/human-interface-guidelines/widgets](https://developer.apple.com/design/human-interface-guidelines/widgets)  
> 29. CPVoiceControlTemplate \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpvoicecontroltemplate](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate)  
> 30. CPTemplate \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cptemplate](https://developer.apple.com/documentation/carplay/cptemplate)  
> 31. CarPlay \| Apple Developer Forums, [https\://developer.apple.com/forums/forums/topics/app-and-system-services/app-and-system-services-carplay](https://developer.apple.com/forums/forums/topics/app-and-system-services/app-and-system-services-carplay)  
> 32. Xcode \| Apple Developer Forums, [https\://developer.apple.com/forums/forums/topics/developer-tools-and-services/developer-tools-and-services-xcode?page=5](https://developer.apple.com/forums/forums/topics/developer-tools-and-services/developer-tools-and-services-xcode?page=5)  
> 33. CarPlay Q\&A \- Apple Developer, [https\://developer.apple.com/forums/activities/1588080](https://developer.apple.com/forums/activities/1588080)  
> 34. Apple HomeView: Update 27.2 schließt neun Sicherheitslücken vor der Einrichtung, [https\://borncity.com/news/apple-homeview-update-27-2-schliesst-neun-sicherheitsluecken-vor-der-einrichtung/](https://borncity.com/news/apple-homeview-update-27-2-schliesst-neun-sicherheitsluecken-vor-der-einrichtung/)  
> 35. About the security content of HomeView Software Version 27.2, [https\://support.apple.com/en-us/149851](https://support.apple.com/en-us/149851)  
> 36. Apple HomeView \- AppleDB, [https\://appledb.dev/device/Apple-HomeView.html](https://appledb.dev/device/Apple-HomeView.html)  
> 37. Tech Bytes blog: AI, engineering, and developer news, [https\://techbytes.app/posts/](https://techbytes.app/posts/)  
> 38. [https\://www\.macworld.com/article/3261804/homeview-and-third-party-apps-what-works-what-doesnt-and-what-we-dont-know.html](https://www.macworld.com/article/3261804/homeview-and-third-party-apps-what-works-what-doesnt-and-what-we-dont-know.html)  
> 39. Hand off calls, music, and more between your iPhone and Apple, [https\://support.apple.com/en-kw/guide/apple-homeview/dev70189d34b/homeview](https://support.apple.com/en-kw/guide/apple-homeview/dev70189d34b/homeview)  
> 40. com.apple.developer.playable-content, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.playable-content](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.playable-content)  
> 41. CarPlay Communication App \| Apple Developer Documentation, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-communication](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-communication)  
> 42. com.apple.developer.carplay-messaging, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-messaging](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-messaging)  
> 43. CarPlay \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay](https://developer.apple.com/documentation/carplay)  
> 44. iOS 26.4 Brings CarPlay Support for ChatGPT, Claude and Gemini, [https\://www\.macrumors.com/2026/02/18/ios-26-4-carplay-support/](https://www.macrumors.com/2026/02/18/ios-26-4-carplay-support/)  
> 45. isPanningInterfaceVisible \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpmaptemplate/ispanninginterfacevisible](https://developer.apple.com/documentation/carplay/cpmaptemplate/ispanninginterfacevisible)  
> 46. [https\://finance.biggo.com/news/3ed0b1f7-b43b-4637-8ff4-4949401ad211](https://finance.biggo.com/news/3ed0b1f7-b43b-4637-8ff4-4949401ad211)  
> 47. [https\://apple.gadgethacks.com/news/carplay-entitlements-for-homeview-what-app-support-means/](https://apple.gadgethacks.com/news/carplay-entitlements-for-homeview-what-app-support-means/)  
> 48. CarPlay Voice-Based Conversation App \- Apple Developer, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation?changes=\_7](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-voice-based-conversation?changes=_7)  
> 49. init(voiceControlStates:) \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpvoicecontroltemplate/init(voicecontrolstates:)](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate/init\(voicecontrolstates:\))  
> 50. CarPlay \- Apple Developer, [https\://developer.apple.com/carplay/](https://developer.apple.com/carplay/)  
> 51. Apple HomeView available today, [https\://www\.apple.com/au/newsroom/2026/11/apple-homeview-available-today/](https://www.apple.com/au/newsroom/2026/11/apple-homeview-available-today/)  
> 52. CarPlay Navigation app \| Apple Developer Documentation, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-maps](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-maps)  
> 53. activateVoiceControlState(withIdentifier:) \- Apple Developer, [https\://developer.apple.com/documentation/carplay/cpvoicecontroltemplate/activatevoicecontrolstate(withidentifier:)](https://developer.apple.com/documentation/carplay/cpvoicecontroltemplate/activatevoicecontrolstate\(withidentifier:\))  
> 54. CarPlay Public Safety App \| Apple Developer Documentation, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-public-safety?language=objc,objc](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-public-safety?language=objc,objc)  
> 55. com.apple.developer.carplay-parking, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-parking](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-parking)  
> 56. CarPlay Quick Food Ordering App \| Apple Developer Documentation, [https\://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-quick-ordering](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-quick-ordering)  
> 57. 将CarPlay 车载集成到你的快速下单App, [https\://developer.apple.com/cn/documentation/carplay/integrating-carplay-with-your-quick-ordering-app](https://developer.apple.com/cn/documentation/carplay/integrating-carplay-with-your-quick-ordering-app)  
> 58. Change settings on Apple HomeView, [https\://support.apple.com/ro-md/guide/apple-homeview/dev07f18f669/homeview](https://support.apple.com/ro-md/guide/apple-homeview/dev07f18f669/homeview)  
> 59. Explore Apple HomeView \- Apple Support (KW), [https\://support.apple.com/en-kw/guide/apple-homeview/dev0fa173cd8/homeview](https://support.apple.com/en-kw/guide/apple-homeview/dev0fa173cd8/homeview)  
> 60. Control what guests can access on Apple HomeView, [https\://support.apple.com/en-am/guide/apple-homeview/devb96eff743/27/homeview/27](https://support.apple.com/en-am/guide/apple-homeview/devb96eff743/27/homeview/27)  
> 61. Control what guests can access on Apple HomeView, [https\://support.apple.com/en-kw/guide/apple-homeview/devb96eff743/homeview](https://support.apple.com/en-kw/guide/apple-homeview/devb96eff743/homeview)  
> 62. CarPlay \| Apple Developer Documentation, [https\://developer.apple.com/design/human-interface-guidelines/carplay](https://developer.apple.com/design/human-interface-guidelines/carplay)  
> 63. Apple Buried the Best CarPlay News in the iOS 27 Developer Notes, [https\://www\.cnet.com/roadshow/auto-tech/apple-carplay-and-automotive-updates-ios-27-wwdc-2026/](https://www.cnet.com/roadshow/auto-tech/apple-carplay-and-automotive-updates-ios-27-wwdc-2026/)  
> 64. Adding StandBy and CarPlay support to your widget, [https\://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget)  
> 65. CPPointOfInterest \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cppointofinterest](https://developer.apple.com/documentation/carplay/cppointofinterest)  
> 66. maximumGridButtonImageSize \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cplisttemplate/maximumgridbuttonimagesize](https://developer.apple.com/documentation/carplay/cplisttemplate/maximumgridbuttonimagesize)  
> 67. allowsMiniPlayer \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpnowplayingtemplate/allowsminiplayer](https://developer.apple.com/documentation/carplay/cpnowplayingtemplate/allowsminiplayer)  
> 68. Integrating CarPlay with Your Music App \- Apple Developer, [https\://developer.apple.com/documentation/carplay/integrating-carplay-with-your-music-app](https://developer.apple.com/documentation/carplay/integrating-carplay-with-your-music-app)  
> 69. ActivityFamily \| Apple Developer Documentation, [https\://developer.apple.com/documentation/widgetkit/activityfamily](https://developer.apple.com/documentation/widgetkit/activityfamily)  
> 70. Play music on Apple HomeView, [https\://support.apple.com/guide/apple-homeview/play-music-deva10579d32/homeview](https://support.apple.com/guide/apple-homeview/play-music-deva10579d32/homeview)  
> 71. Live Activities \| Apple Developer Documentation, [https\://developer.apple.com/design/human-interface-guidelines/live-activities](https://developer.apple.com/design/human-interface-guidelines/live-activities)  
> 72. carTraitCollection \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpinterfacecontroller/cartraitcollection](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/cartraitcollection)  
> 73. CPSessionConfiguration \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpsessionconfiguration](https://developer.apple.com/documentation/carplay/cpsessionconfiguration)  
> 74. CarPlay \| Apple Developer Forums, [https\://developer.apple.com/forums/tags/carplay?page=3](https://developer.apple.com/forums/tags/carplay?page=3)  
> 75. Deprecated Symbols \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpinterfacecontroller-deprecated-symbols?changes=lates\_3](https://developer.apple.com/documentation/carplay/cpinterfacecontroller-deprecated-symbols?changes=lates_3)  
> 76. setRootTemplate(\_:animated:completion:) \- Apple Developer, [https\://developer.apple.com/documentation/carplay/cpinterfacecontroller/setroottemplate(\_:animated:completion:)](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/setroottemplate\(_:animated:completion:\))  
> 77. presentTemplate(\_:animated:completion:) \- Apple Developer, [https\://developer.apple.com/documentation/carplay/cpinterfacecontroller/presenttemplate(\_:animated:completion:)](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/presenttemplate\(_:animated:completion:\))  
> 78. CPPlaybackConfiguration.Presentation \- Apple Developer, [https\://developer.apple.com/documentation/carplay/cpplaybackconfiguration/presentation?changes=l\_1,l\_1](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration/presentation?changes=l_1,l_1)  
> 79. init(preferredPresentation:playbackAction:elapsedTime:duration, [https\://developer.apple.com/documentation/carplay/cpplaybackconfiguration/init(preferredpresentation:playbackaction:elapsedtime:duration:)](https://developer.apple.com/documentation/carplay/cpplaybackconfiguration/init\(preferredpresentation:playbackaction:elapsedtime:duration:\))  
> 80. CPVoiceControlState \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cpvoicecontrolstate](https://developer.apple.com/documentation/carplay/cpvoicecontrolstate)  
> 81. Widgets and watch complications \| Apple Developer Documentation, [https\://developer.apple.com/documentation/widgetkit/widgets-and-complications-collection](https://developer.apple.com/documentation/widgetkit/widgets-and-complications-collection)  
> 82. CPPointOfInterestTemplate \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/cppointofinteresttemplate](https://developer.apple.com/documentation/carplay/cppointofinteresttemplate)  
> 83. Requesting CarPlay Entitlements \| Apple Developer Documentation, [https\://developer.apple.com/documentation/carplay/requesting-carplay-entitlements](https://developer.apple.com/documentation/carplay/requesting-carplay-entitlements)  
> 84. Entitlements \| Apple Developer Forums, [https\://developer.apple.com/forums/tags/entitlements?page=2](https://developer.apple.com/forums/tags/entitlements?page=2)  
> 85. CarPlay audio entitlement approved… \| Apple Developer Forums, [https\://developer.apple.com/forums/thread/850675](https://developer.apple.com/forums/thread/850675)  
> 86. Updated Apple Developer Program License Agreement now available, [https\://developer.apple.com/news/?id=76371du6](https://developer.apple.com/news/?id=76371du6)  
> 87. Xcode 27 replaced the Simulator app with Device Hub. The data, [https\://www\.reddit.com/r/reactnative/comments/1wmjy37/xcode\_27\_replaced\_the\_simulator\_app\_with\_device/](https://www.reddit.com/r/reactnative/comments/1wmjy37/xcode_27_replaced_the_simulator_app_with_device/)  
> 88. Xcode 27: where is the Simulator? Now in Device Hub \- VibeView, [https\://vibeview.io/guides/xcode-27-where-is-the-simulator/](https://vibeview.io/guides/xcode-27-where-is-the-simulator/)  
> 89. Xcode 27 Device Hub vs Simulator: What Changed \- RocketSim, [https\://www\.rocketsim.app/blog/fixing-devicehub-xcode-simulator/](https://www.rocketsim.app/blog/fixing-devicehub-xcode-simulator/)  
> 90. Simulator and automatization \| Apple Developer Forums, [https\://developer.apple.com/forums/thread/831782](https://developer.apple.com/forums/thread/831782)  
> 91. CarPlay \| Apple Developer Forums, [https\://developer.apple.com/forums/tags/carplay?page=2](https://developer.apple.com/forums/tags/carplay?page=2)  
> 92. [https\://www\.apprankr.in/blog/apple-homeview-widgets-carplay-developer-agreement](https://www.apprankr.in/blog/apple-homeview-widgets-carplay-developer-agreement)  
> 93. Updated Apple Developer Program License Agreement now available, [https\://developer.apple.com/news/?id=17mwd36z](https://developer.apple.com/news/?id=17mwd36z)  
> 94. [https\://en.wikipedia.org/wiki/HomeView](https://en.wikipedia.org/wiki/HomeView)  
> 95. Loading Indicator using \`CPLis… \| Apple Developer Forums, [https\://developer.apple.com/forums/thread/719953](https://developer.apple.com/forums/thread/719953)  
> 96. Meet Apple HomeView, a new way to enjoy entertainment and, [https\://www\.apple.com/au/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/](https://www.apple.com/au/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/)  
> 97. 10 HomeView Features You Might Have Missed \- MacRumors, [https\://www\.macrumors.com/2026/10/14/homeview-tidbits/](https://www.macrumors.com/2026/10/14/homeview-tidbits/)


