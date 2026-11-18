# Code: the Swift shape of a CarPlay and HomeView app

Native Swift and SwiftUI on the iOS 27 SDK, deploying to iOS 26 or later. The bundled templates in
`templates/` implement everything below and type-check against the iOS 27.1 SDK at deployment
targets 26.0 and 27.0 under Swift 6 (`scripts/typecheck_templates.sh`).

## Scene routing

The phone UI and the car UI are two scenes of one process. Route the car scene one of two ways,
not both:

- **In code** (`templates/App/HomeCraftApp.swift`): `@UIApplicationDelegateAdaptor` on the SwiftUI
  `App`, and `application(_:configurationForConnecting:options:)` returning a
  `UISceneConfiguration` with `sceneClass = CPTemplateApplicationScene.self` and the CarPlay
  delegate class when `connectingSceneSession.role == .carTemplateApplication`.
- **In Info.plist** (`templates/Info.plist.fragment.xml`): a
  `CPTemplateApplicationSceneSessionRoleApplication` entry under `UIApplicationSceneManifest`,
  beside the phone's `UIWindowSceneSessionRoleApplication` entry, with
  `UIApplicationSupportsMultipleScenes` true as Apple's samples set it.

CarPlay and HomeView can cold-launch the app with only the car scene, so the `WindowGroup` never
appears. Start shared services in `application(_:didFinishLaunchingWithOptions:)` or in
`@MainActor` singletons, never in a view's `@StateObject`. A car-only launch that reaches for a
SwiftUI-owned object is the commonest crash developers report.

## Navigation

Keep a strong reference to the `CPInterfaceController` from `templateApplicationScene(_:didConnect:)`
and set the root there. Use the `async throws` forms (`try await controller.setRootTemplate(root,
animated: false)`) or the completion-handler forms. Apple deprecated the forms without a
completion: when one fails it throws an exception instead of returning an error. Any template may
be the root; a tab bar must be the root if used.

## Now Playing

`CPNowPlayingTemplate.shared` reads the system Now Playing session. Configure it at connect,
because the car's own Now Playing button can open it before the app's list is up.

Publish that session with **one** framework:

- **MediaPlayer** (iOS 26 and 27): `MPNowPlayingInfoCenter` for metadata and
  `MPRemoteCommandCenter` for transport, published from the player's observed state
  (`templates/App/PlaybackService.swift`).
- **NowPlaying** (new in iOS 27): `MediaSession` and its snapshot and command types.

Apple: "Don't mix the Now Playing framework with the MPNowPlayingInfoCenter and
MPRemoteCommandCenter APIs from the MediaPlayer framework for local playback. Doing so results in
undefined behavior." An app deploying to iOS 26 keeps MediaPlayer until it drops 26. One forum
report (FB24840951) describes Now Playing freezing on iOS 27 when `MPNowPlayingInfoCenter` is
combined with MusicKit's `ApplicationMusicPlayer`.

## Video

There is no video template. The browse UI is lists, grids and tabs; frames go to the car or
HomeView display over AirPlay (`AVPlayer.allowsExternalPlayback = true`). From iOS 26.4 set
`CPListItem.playbackConfiguration = CPPlaybackConfiguration(preferredPresentation: .video,
playbackAction: .play, elapsedTime:, duration:)` on each playable row; `.audio` opens Now Playing
instead. `CPSessionConfiguration.supportsVideoPlayback` (iOS 26.4) reports what the session can
do and holds for the session; it is not a parked signal. When the car stops allowing video the
system falls back to audio. Show a video tab only when the session supports it.

## Voice

For `voice-based-conversation` (iOS 26.4+) see `templates/App/CarPlayConversationSceneDelegate.swift`:

1. Set a lightweight list as the root.
2. Present `CPVoiceControlTemplate` over it: `presentTemplate` on 26.4,
   `showOverlayTemplate(_:animated:completion:)` on iOS 27 (dismiss with `hideOverlayTemplate`).
   Apple allows any template as the root, but no member found the voice template tested there, so
   the presented path is the documented one.
3. Activate a voice state only after the template is on screen; changes are rate-limited, so
   drive them from the engine's real phase changes rather than a timer.
4. Audio session: `.playAndRecord`, `.default` mode, no mixing (`.allowBluetoothHFP` is fine),
   active only during the turn, deactivated with `.notifyOthersOnDeactivation`.
5. Up to 2 `actionButtons` per `CPVoiceControlState` from 26.4.

## Widgets and Live Activities

`templates/Widget/HomeCraftWidgets.swift`: a `.systemSmall` widget with
`.containerBackground(for: .widget)`, and an `ActivityConfiguration` with
`.supplementalActivityFamilies([.small])`. Widget actions use App Intents; media actions use
`AudioPlaybackIntent` so they run in the app process.

## HomeKit and Matter

HomeView controls accessories through the Home app. There is no HomeView-specific HomeKit or
Matter API; an accessory app keeps using HomeKit (`NSHomeKitUsageDescription`) or Matter
pairing as on iPhone, and that does not put the app on HomeView.

## Swift 6

CarPlay templates are main-actor types in the iOS 27 SDK. Mark the scene delegate `@MainActor`,
`@preconcurrency import CarPlay` where Objective-C callbacks lack `Sendable`, and hop to the main
actor inside `MPRemoteCommandCenter` handlers and `CPListItem` handlers
(`MainActor.assumeIsolated` where the callback is documented to arrive on main). Implement
`CPSessionConfigurationDelegate` methods as `nonisolated`.
