---
name: home-craft
description: Build, adapt or review a native Swift/SwiftUI iOS app for Apple CarPlay and Apple HomeView, the countertop display that runs CarPlay audio and video apps from a paired iPhone, on iOS 26 and iOS 27. Covers choosing the one CarPlay entitlement, the car scene and its templates, Now Playing, video over AirPlay, voice-based conversational apps, system-small widgets and Live Activities, testing in Xcode 27's Device Hub, and the entitlement and App Review rules. Ships Swift templates that type-check against the iOS 27 SDK and a static audit of a project. Use when someone wants an app in the car or on HomeView, asks which CarPlay entitlement to request, hits a car scene that never connects, a template exception, a blank Now Playing screen or a widget that looks wrong in CarPlay, or mentions CPTemplateApplicationScene, CarPlay Simulator, CarPlay Ultra or HomeView, even if they only say "add CarPlay" or "make it show up on HomeView". Not for React Native or Expo apps, Android Auto, or HomeKit accessory firmware.
---

# home-craft

HomeView has no SDK. An app reaches Apple's countertop display in exactly two ways, both from a
paired iPhone: as a CarPlay app holding the audio or video entitlement, which HomeView draws
unchanged, or as a system-small widget. So building for HomeView is building for CarPlay, with a
kitchen counter as the second screen, and the CarPlay rules decide almost everything: one
entitlement per app, a fixed list of system-drawn templates per category, a phone that stays
locked in a pocket, and a car-only cold launch that never creates the SwiftUI window.

Much of this changed in iOS 26.4 and iOS 27, after most training data, and one of the four
research reports behind this skill got five points wrong that Apple's own pages settle. Work from
`references/`, checked against Apple's documentation in November 2026, and from the installed SDK,
rather than from memory.

Deliver what was asked, at the scope intended. Adding CarPlay to an audio app means the car scene,
Now Playing and the widget it needs, not a redesign of the phone app; a review means findings, not
edits. Say in one sentence where a wider change would help, then build what was asked.

## 1. Read the project before deciding anything

Open the app's `.entitlements` files, its Info.plist scene manifest or `configurationForConnecting`
code, how it plays media and publishes Now Playing, and any widget extension. Then run the audit:

```bash
python3 scripts/home_audit.py <project-dir>          # exit 1 on any error
```

It checks 24 rules, among them more than one CarPlay entitlement, a template the category does not allow,
a missing car scene, NowPlaying mixed with MediaPlayer, a conversational app with no voice
template, hard-coded tab and list limits, navigation calls with no completion, car text that
sends the driver to the phone, data unreadable while the phone is locked, widgets without a
removable background, and more. Each finding names the reference section that explains it.

## 2. Choose the route

Pick the single CarPlay category that matches what the app is for, using
`references/entitlements-and-shipping.md`. The short version:

| The app is | Entitlement | In the car | On HomeView |
|---|---|---|---|
| media, including video with sound | `carplay-audio` (+ AirPlay video) | yes | the app itself |
| video first (iOS 27+) | `carplay-video` | parked, where the car supports it | the app itself |
| a voice assistant (iOS 26.4+) | `carplay-voice-based-conversation` | yes | widget only |
| one of the other 8 categories | its own key | yes | widget only |
| none of the 11 | none | widget only | widget only |

Never combine two keys (charging plus fueling is the one exception) and never request one only to
reach HomeView. If the app fits no category, say so and build the widget.

## 3. Build it

Start from the bundled templates and adapt them to the app; they type-check against the iOS 27.1
SDK at deployment targets 26.0 and 27.0 in Swift 6:

| Template | Use for |
|---|---|
| `templates/App/HomeCraftApp.swift` | routing the car scene from a SwiftUI app; starting shared services at launch |
| `templates/App/PlaybackService.swift` | one app-lifetime player publishing Now Playing from observed state, AirPlay on |
| `templates/App/CarPlayMediaSceneDelegate.swift` | audio or video apps: tab bar within `maximumTabCount`, lists within `maximumItemCount`, `CPPlaybackConfiguration` rows, a video tab only when the session supports video |
| `templates/App/CarPlayConversationSceneDelegate.swift` | voice-based conversational apps: list root, voice template presented (26.4) or overlaid (27), audio session only during a turn |
| `templates/Widget/HomeCraftWidgets.swift` | the system-small widget every app gets on HomeView, and a small-family Live Activity |
| `templates/Info.plist.fragment.xml`, `templates/CarPlay.entitlements.fragment.plist` | the plist side, if the app routes scenes in Info.plist |

Read `references/code.md` for the API shape and the iOS 26/27 differences, and
`references/design-rules.md` before writing any car-facing text or widget. Two rules carry the most
weight. First, whatever the car needs must exist on a car-only cold launch, so it lives in the app
delegate or a `@MainActor` service, never in a SwiftUI view. Second, Now Playing comes from exactly
one of MediaPlayer or the iOS 27 NowPlaying framework.

Keep every gated API behind `#available`; an app deploying to iOS 26 cannot call iOS 27 overlay or
MiniPlayer APIs unguarded, and the type-check catches it.

## 4. Check what can be checked here

Run these and quote their final lines in the report:

```bash
python3 scripts/home_audit.py <project-dir>
xcodebuild -scheme <scheme> -destination 'generic/platform=iOS' build   # the app's own build
scripts/typecheck_templates.sh            # only when the bundled templates were edited in place
```

Then work through `references/testing.md`. Most of its lanes need hardware an agent rarely has:
CarPlay Simulator needs a USB-connected iPhone, a head unit needs a car, and HomeView has no
simulator at all. Record each lane as **seen**, **not reached** or **not built**, and never write
that the app works in the car or on HomeView unless that lane was seen. To drive the CarPlay
Simulator window or an iOS simulator from an agent, use `proctor:proctor`.

## 5. Report

Write for someone who has the app and not this skill: cite the app's files and Apple's
documentation, not this skill's references or local paths. Up to 40 lines:

1. The outcome in one or two sentences, including the category chosen and why.
2. What changed, file by file.
3. The audit and type-check results, quoted.
4. Each test lane: seen, not reached, or not built.
5. What only the user can do: request the entitlement (the Account Holder, on Apple's form; draft
   the justification, do not send it), regenerate profiles, run the hardware lanes, and anything
   the research left open that touches this app (`references/evidence.md`, last section).

## Constraints

- Requesting an entitlement, changing signing in the developer portal and submitting to App Review
  are the user's actions. Prepare them; do not take them.
- State a claim with the confidence `references/evidence.md` gives it. A single forum report is a
  lead to check, not an Apple rule, and HomeView behaviour Apple has not documented (third-party
  Live Activities, a widget opt-out, conversational apps) is reported as open.
- This skill is native Swift and SwiftUI. For a React Native or Expo app, say that this skill does
  not cover it; for iPhone Duo layout, route to `duo-craft:duo-craft`; for the phone app's own
  screens, `design-craft:design-craft` and `ux-craft:ux-craft`; for TestFlight and App Store
  Connect, `app-store-connect:app-store-connect`.

## References

| File | Read it when |
|---|---|
| `references/capability-matrix.md` | choosing templates, checking depth, tab, list and grid limits |
| `references/entitlements-and-shipping.md` | choosing the category, the request, signing, review |
| `references/code.md` | writing the scene, Now Playing, video, voice, widgets, Swift 6 |
| `references/design-rules.md` | writing car-facing text, layout, voice UX, widgets |
| `references/testing.md` | planning or reporting tests |
| `references/homeview.md` | anything specific to HomeView, its routes and roadmap |
| `references/evidence.md` | judging how firm a rule is, or what is still open |
