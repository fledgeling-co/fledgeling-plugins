# Design rules for CarPlay and HomeView

From the CarPlay Human Interface Guidelines (HIG), the Widgets HIG, the Live Activities HIG and the CarPlay Developer Guide's
category rules. Apple has no HomeView HIG for projected apps; HomeView design guidance exists only
for widgets.

## Phone

The driver never touches the phone.

- Every flow completes on the car screen. Error and alert text never asks the driver to unlock,
  open or look at the iPhone; App Review rejects it. Do setup on the phone before the drive.
- The phone is usually locked in a pocket or bag. Files written with `.completeFileProtection` /
  `NSFileProtectionComplete` and keychain items with `kSecAttrAccessibleWhenUnlocked` are
  unreadable then. Store what the car needs under an after-first-unlock class.
- CarPlay or HomeView can launch the app with only the car scene connected. Nothing the car needs
  may be created inside a SwiftUI view.

## Glanceability

- Put the primary content and actions in the upper half of the screen.
- Support 800×480 through 1920×720 car displays; supply @2x and @3x art in light and dark.
- App icon: 120 px (@2x) and 180 px (@3x), never a pure-black background (it vanishes against the
  dark CarPlay home screen).
- Templates are system-drawn and take Liquid Glass from the system. Do not paint opaque custom
  backgrounds or recreate glass in custom views. iOS 26 gave `CPMapTemplate` buttons the glass
  treatment.

## Limits

Read the limits at runtime instead of hard-coding them: `CPTabBarTemplate.maximumTabCount`
(depends on the entitlement), `CPListTemplate.maximumItemCount` and `maximumSectionCount`.
The full table is in `capability-matrix.md`.

## Audio

- The user starts playback. Activate the audio session only once audio is ready to play, because
  activating it silences the car's radio.
- Show Now Playing as soon as playback starts, before artwork finishes loading.
- Resume after temporary interruptions such as a phone call; do not resume after a permanent one
  such as the user choosing another source. Never change the system volume.
- iOS 27 adds a MiniPlayer over browse templates, on by default
  (`CPNowPlayingTemplate.shared.allowsMiniPlayer`).

## Voice

- A voice-based conversational app launches straight into voice and answers by speaking. It never
  answers a query with text or imagery on the car screen.
- `CPVoiceControlTemplate` is on screen for the whole time the microphone is open: presented
  modally on 26.4, or as an overlay with `showOverlayTemplate` on iOS 27. Activate a state only
  after the template is on screen.
- Hold the audio session only while voice is in use: `.playAndRecord`, `.default` mode, no mixing.
- Recording is otherwise forbidden in CarPlay; navigation and conversational apps may record only
  while the voice template is visible.
- Siri and App Intents are a separate voice path. The steering-wheel voice button stays Siri's.
  App Intents do not make an app eligible for the conversational category.

## Day and night

Read `contentStyle` from `CPSessionConfiguration` and update on `contentStyleChanged`. Check
colour in a real car. On HomeView check light, dark, and the Modular face's red night mode.

## Widgets

- `.systemSmall` only. Use `.containerBackground(for: .widget)`: CarPlay, StandBy and HomeView's
  Modular face remove the background, so the content must read without it.
  `containerBackgroundRemovable(false)` keeps the widget out of all three.
- HomeView's Modular face holds up to 4 small widgets and is shared by the household: anything on
  it is visible to everyone at home. Show only what everyone may see.
- `.disfavoredLocations([.carPlay], for: [.systemSmall])` marks the widget as not optimised for
  CarPlay and greys its interaction. It does not remove the widget, and Apple documents no effect
  on HomeView. There is no HomeView case in `WidgetLocation`.
- In CarPlay, widget buttons work only on touchscreen cars; launching the app from a widget needs
  a CarPlay-integrated app.

## Live Activities

`.supplementalActivityFamilies([.small])` puts a Live Activity in the CarPlay Dashboard from
iOS 26, non-interactive. HomeView shows Apple's own activities (timers, media, Intercom); Apple
does not document third-party Live Activities there.

## What App Review rejects

Lyrics on the car screen; message or email bodies on screen; games or social features; any step
that sends the driver to the phone; a category that does not match the app's real function; a
full menu in quick food ordering; driving-task apps that are store finders or refresh too often;
video played without the video entitlement (an app played video in a browser view and was removed
on 23 October 2026, per one source); non-map UI drawn on a navigation app's base window.
