# CarPlay and HomeView in native Swift/SwiftUI on iOS 26 and 27: merged research, round 2 (18 November 2026)

Four reports answered one brief, scoped to Swift and SwiftUI with no Expo or React Native:

| Member | Run | Cost | Sources | Citation check |
|---|---|---|---|---|
| **OpenAI** Deep Research (API, gpt-6.1-sol) | `dr_7d0cae34fa334dc7` | $9.00 reserved (top of its estimate); actual cost is on the OpenAI billing page | 77 | 8 links flagged dead were Apple symbol URLs the checker cut off at a closing parenthesis. Restored, they open, and a made-up symbol returns 404. One fediverse profile didn't respond. |
| **Gemini** Deep Research (web app, run by hand) | `dr_3b39ed9ab20917fa` | subscription | 97 | Same cut-off pattern on 6 Apple URLs. Four news sites resolve to a private address in Dossier's DNS but open normally. |
| **Codex** CLI | `dr_4f3b8dcf8bc4528f` | subscription | 56 | The dead links come from its working transcript, not the report. |
| **Grok** CLI | `dr_9544137a6740506d` | subscription | 40 | Two news links hit the same DNS issue. |

None of the four reports cites a link that doesn't exist. Two members didn't run: **Perplexity** returned `insufficient_quota` (out of credit, so no charge). **xAI** failed after exactly 5 minutes with `fetch failed`. Its outcome is unknown, so Dossier is holding a $2.50 reservation; check the xAI console for an in-flight job.

Tags in this report:
- **[Apple ✓]**: I checked the claim against Apple's own documentation JSON or support pages while merging. It outranks every member.
- **[OpenAI]**, **[Gemini]**, **[Codex]**, **[Grok]**: the member or members that made the claim. A single name means single-sourced.
- **[synth]**: a conclusion I drew by combining sources.

## What to do

1. **Request one CarPlay entitlement: the one that matches what the app is for.** Use audio for a media app, video for a video-first app, and voice-based conversation for an assistant. The audio entitlement explicitly covers "audio-only content or video content with an audio component", so a mixed-media app needs audio alone, plus AirPlay video. [all four; Apple entitlement pages]
2. **Ship an app on HomeView only through the audio or video entitlement, running on a paired iPhone.** An iPad pairing cannot supply third-party audio or video apps. [Apple ✓ Support 148407; Codex; Gemini is wrong here]
3. **For any other kind of app, the HomeView surface is a `.systemSmall` widget.** HomeView's Modular face is shared by the household, so design the widget to show only what everyone in the home may see. [OpenAI, Codex, Grok; Widgets HIG]
4. **Keep the CarPlay scene independent of SwiftUI.** CarPlay and HomeView can launch the app with no phone scene, so a `@StateObject` created inside a SwiftUI view won't exist yet. Hold state in an app-lifetime `@MainActor` service. [Gemini, OpenAI, Codex]
5. **Pick one Now Playing stack.** Either keep MediaPlayer (`MPNowPlayingInfoCenter`/`MPRemoteCommandCenter`), or adopt iOS 27's new NowPlaying framework (`MediaSession`); never both. Apple: "Don't mix… Doing so results in undefined behavior." [Apple ✓ NowPlaying docs; Gemini was the only member to find this]
6. **Test on a USB-connected iPhone with CarPlay Simulator in Device Hub, then on a real car head unit, then on a real HomeView.** Xcode 27.2 doesn't support CarPlay in the iOS Simulator, and HomeView has no simulator at all. [all four]
7. **Request the entitlement before writing UI.** Apple publishes no approval time, and 2026 reports run from days to more than 4 weeks. [all four]

## Settled during the merge against Apple's own pages

The brief carried six open questions, and the members disagreed on several other points. Apple's documentation, checked directly, settles most of them:

| Question | Answer | Who had it right |
|---|---|---|
| Can one app hold both audio and video? | **No, in practice.** The Oct 2026 Guide and both entitlement pages forbid combining them (EV charging plus fueling is the only exception). WWDC26 session 212 said to ship both, and no Apple document reconciles the two. | All four agree the documents conflict. Gemini adds that App Review rejected a dual-entitlement build under §2.5.1, but that rests on a single forum report. Grok cites a Sept 2026 report that adding the video key to an audio app gave a blank CarPlay screen. |
| Does `.disfavoredLocations([.carPlay])` hide the widget on HomeView? | **No.** It doesn't hide the widget even in CarPlay. Apple: disfavoring "doesn't exclude your widget from CarPlay or StandBy, but it communicates… these locations aren't the best fit." `WidgetLocation` has no HomeView case, and its effect on HomeView is undocumented. | [Apple ✓] OpenAI, Codex and Grok were right. **Gemini was wrong** to say it hides the widget on both. |
| Can `CPVoiceControlTemplate` be the root template? | **Not forbidden.** Apple: "You can install any template as the root template of your interface." The voice template's own page describes presenting it, and iOS 27 adds `showOverlayTemplate`/`hideOverlayTemplate`. The documented, safe path is a list as root with the voice template presented over it. | [Apple ✓] OpenAI was right; Codex and Grok said it was unsettled. **Gemini was wrong** to say it cannot be root. |
| Do third-party Live Activities appear on HomeView? | **Not documented.** The Live Activities HIG lists CarPlay but not HomeView, and Apple's HomeView examples are its own (timers, media, Intercom). | All four agree. |
| Maximum depth for video apps? | **5 templates, root included.** The `pushTemplate` reference table lists Video = 5. | [Apple ✓] OpenAI was right. Gemini and Grok got there by inference, and Codex left it open. |
| Tab limit? | **It depends on the entitlement.** Read `maximumTabCount` at runtime. The Guide gives 4 for audio and 5 for everything else. | [Apple ✓] OpenAI and Grok were right. **Gemini was wrong** to give a flat 4 for every category. |
| Public safety templates | Action sheet, alert, grid, list, tab bar, contact, information, Now Playing and point of interest; iOS 27 adds search and voice control. **No map template.** Apple's Now Playing page confirms public safety may use it. OpenAI notes the contact template's own page omits public safety, contradicting the Guide. | [Apple ✓ Now Playing page] Grok and OpenAI were right. **Gemini was wrong** to list a map root and omit Now Playing. |
| Navigation templates | Map (root, over the `CPWindow`), action sheet, alert, grid, list, tab bar, contact, information, voice control and search. **No Now Playing, no point of interest.** iOS 27 adds map panels (`showPanel`); route sharing needs iOS 26.4. | OpenAI and Grok. **Gemini wrongly includes Now Playing and point of interest.** Grok says to check the search cell in the PDF table. |
| HomeView's operating system | "HomeView Software 27.2", build 24V526, released 12 Nov. The tvOS 27.2 lineage comes from developers inspecting the firmware; Apple hasn't stated it. | All four. |
| `ConversationalApps` in the iOS 27.3 beta | A private string in `PebblePlayCore` ("Conversational Apps") with two-way audio work started. It is not an API and has not been announced. | All four. OpenAI separates an older, unused `PebblePlay/ConversationalApps` flag from the new category string added in 27.3. |

Gemini gets the most wrong of the four: five of the rows above. It was also the only member to find the NowPlaying-framework rule, and that one checked out. Treat its other claims that only it makes as leads to check, not as facts.

## Capability matrix

Every category entitlement is `com.apple.developer.carplay-<suffix>`, and a template outside the category's list throws at runtime. "B" means the base set: list, grid, tab bar, action sheet and alert.

| Category (suffix) | iOS 26.x | iOS 27.x adds | HomeView | Depth |
|---|---|---|---|---|
| Audio (`audio`) | B, Now Playing | search, voice control, MiniPlayer (`allowsMiniPlayer`, default on) | **Yes**, from an iPhone | 5 |
| Video (`video`) | none (parked AirPlay video is a vehicle feature) | new in 27.0: B, Now Playing, search, voice control; parked only, and hidden in cars without video support | **Yes**, from an iPhone | 5 |
| Voice conversation (`voice-based-conversation`) | from 26.4: B, information, point of interest, voice control | overlay presentation | No (beta string only) | 3 |
| Communication (`communication`) | B, contact, information, Now Playing | voice control | No | 5 |
| Navigation (`maps`) | see table above | map panels | No | 5 |
| Public safety (`public-safety`) | see table above | search, voice control | No | 5 |
| EV charging (`charging`) | B, information, point of interest | search, voice control | No | 5 |
| Parking (`parking`) | B, information, point of interest | search, voice control | No | 5 |
| Fueling (`fueling`) | B, information, point of interest | search, voice control | No | 3 |
| Quick food ordering (`quick-ordering`) | B, information, point of interest | voice control | No | 2 → 3 from 26.4 |
| Driving task (`driving-task`) | B, information, point of interest; voice control from 26.4 | none | No | 2 → 3 from 26.4 |
| Widgets | `.systemSmall`, no entitlement | none | Home Screen and the shared Modular face | none |
| Live Activities | `.supplementalActivityFamilies([.small])`, non-interactive | none | undocumented for third parties | none |

Gemini lists the contact template for EV charging, parking, fueling and food ordering; the other three members don't. Check the Guide PDF before using a contact template in those categories. CarPlay Ultra adds no SDK, template or entitlement for third-party apps; navigation apps keep the instrument-cluster and head-up display APIs. [all four]

## UI and UX rules

- **Glanceability.** Put the primary content in the upper half of the screen, and support 800×480 through 1920×720 displays with @2x and @3x art in light and dark. [all four; CarPlay HIG] App icons are 120 px (@2x) and 180 px (@3x) and must not have a pure-black background. [Gemini; CarPlay HIG layout]
- **The iPhone stays locked and untouched.** Never ask the driver to pick it up. Files and keychain items that are only readable while the phone is unlocked aren't available. [all four]
- **Audio.** Let the user start playback. Activate the audio session only once audio is ready, because activating it silences the car radio. Show Now Playing immediately. Only a list may be pushed on top of Now Playing. [all four]
- **List and grid limits.** Read `maximumItemCount` at runtime, and expect some cars to show only 12 items. A grid shows its first 8 buttons. A point-of-interest template holds at most 12 locations. [OpenAI, Grok, Gemini]
- **Voice.** Show the voice template whenever the microphone is open. It holds up to 5 states and rate-limits rapid changes. From 26.4 it can carry action buttons; its trailing navigation bar shows at most 2 buttons. Conversational apps launch straight into voice, answer by speaking rather than with text, and release the audio session between turns. [OpenAI, Gemini, Grok; Guide] For conversational audio, Gemini quotes WWDC26 as `.playAndRecord` with `.default` mode and no mixing.
- **Day and night.** Read `contentStyle` and update on `contentStyleDidChange`. On HomeView, check Light, Dark, Ambient Dark, and the Modular face's red night mode. [all four; the Ambient Dark mode name comes only from Gemini]
- **Widgets.** Use `.containerBackground(for: .widget)` so CarPlay, StandBy and the Modular face can remove the background. A widget with `containerBackgroundRemovable(false)` is left out of the galleries that need removable backgrounds. [Gemini; WidgetKit docs] The Modular face holds 4 small widgets that everyone in the household can see. [OpenAI, Codex]
- **Liquid Glass.** Templates are drawn by the system, so don't paint opaque custom backgrounds over them. [all four]
- **What review rejects**, from the Guide's rules: lyrics in audio apps, message bodies on screen, any step that sends the driver to the phone, games or social features, a full menu in quick food ordering, driving-task UI refreshing more often than every 10 s or points of interest more often than every 60 s, and video played without the video entitlement. Gemini cites one case of that last rule: the app APTV was removed from the App Store on 23 Oct 2026 for playing video in a browser view (single source). [all four]

## Code: SwiftUI app plus a CarPlay scene

- **Scene routing.** Add `@UIApplicationDelegateAdaptor`. Then either return a `UISceneConfiguration` for role `.carTemplateApplication` from `application(_:configurationForConnecting:options:)`, or declare both scene roles in `UIApplicationSceneManifest`, with `UIApplicationSupportsMultipleScenes` set to true. [Gemini, OpenAI, Codex]
- **Cold launch.** CarPlay or HomeView can launch the app before the `WindowGroup` exists. Create shared services in the app delegate or as `@MainActor` singletons, not inside SwiftUI views. [Gemini, OpenAI]
- **Root and navigation.** Use the completion-handler or `async` forms of `setRootTemplate`, `pushTemplate` and `presentTemplate`; Apple has deprecated the older forms without a completion. Gemini's claim that leaving out the completion handler "throws" is single-sourced. [Gemini; Apple docs]
- **Now Playing.** `CPNowPlayingTemplate.shared`, configured when the scene connects. Use MediaPlayer *or* NowPlaying (`MediaSession`) as one consistent stack (see What to do, step 5). Gemini reports a freeze, FB24840951, when `MPNowPlayingInfoCenter` is combined with MusicKit's `ApplicationMusicPlayer` on iOS 27; that is a single forum source.
- **Video.** There is no video template. Build the browsing UI from list, grid and tab templates, stream frames over AirPlay (`allowsExternalPlayback`), and set `CPPlaybackConfiguration(preferredPresentation:…)` (iOS 26.4) on each playable item. `supportsVideoPlayback` reports what the session can do; it doesn't say the car is parked. When video drops out, the system falls back to audio. [all four; Codex adds the engineer's quote]
- **Voice.** Set a list as the root and present `CPVoiceControlTemplate` over it on connect: modally on 26.4, or with `showOverlayTemplate` on iOS 27 [Apple ✓ API exists]. Activate a voice state only after the template is on screen. [Gemini, OpenAI]
- **Swift 6 concurrency.** CarPlay templates are `@MainActor` in the iOS 27 SDK. Make the scene delegate `@MainActor`, use `@preconcurrency import CarPlay`/`MediaPlayer` where callbacks lack `@Sendable`, and hop to the main actor inside `MPRemoteCommandCenter` handlers. [Gemini, OpenAI]
- **Skeletons.** All four reports wrote an audio skeleton and a voice skeleton, and none was compiled. Gemini's are the most complete for this setup: SwiftUI app delegate routing, a cold-launch-safe coordinator, a video tab added only when `supportsVideoPlayback` is true, and the voice overlay with a 26.4 fallback. They're in its section 3, but they swallow errors with `try?` and `print`, which production code should report instead. OpenAI's are in its section 3(a)/(b).

## Entitlements and deployment

- **Request** through Apple's CarPlay form as the Account Holder, choosing the single category, and accept the CarPlay Entitlement Addendum. After the grant: enable the capability on the App ID, regenerate the profiles, use manual signing, and add the Xcode capability. [all four]
- **Check the signed build, not the project file.** Run `codesign -d --entitlements :- YourApp.app` and `security cms -D -i embedded.mobileprovision` on the archive and every extension. OpenAI cites Apple's QA1798 for these. Gemini reports the portal sometimes issues profiles without the approved CarPlay key, which leaves the CarPlay scene silently never connecting (forum thread 850675, which exists; single source).
- **Timing.** There is no SLA. Reported waits: audio in days; driving task from a day to 3 weeks; video undecided after 15 days or more; one wait of over a year. [OpenAI, Grok, Codex, Gemini] Gemini adds a web-form bug that submitted the description field empty (single source).
- **HomeView needs nothing extra.** There is no separate review, opt-in or Info.plist key. Don't request an entitlement only to get onto HomeView, because Apple judges requests on in-car use. [all four]
- **The icon goes to every user** once the key is in the binary, TestFlight included. [Grok, Gemini; Guide]

## Test matrix

| Lane | What to cover | Watch for |
|---|---|---|
| XCTest (`@MainActor`) | Scene delegate cold launch with no `WindowGroup`; template choice per category; depth, tab count and voice-state counts | A crash from an uninitialised SwiftUI state object; exceptions from unpermitted templates or exceeded limits |
| Device Hub + CarPlay Simulator over USB | 800×480 and 1920×720 layouts; video toggled on and off mid-session; voice overlay; MiniPlayer; light and dark | Gemini reports disappearing section headers (FB24061858) and single-line list truncation on iOS 27 (single source) |
| Standalone CarPlay Simulator (Additional Tools) | Video-app checks, as WWDC26 directs | none |
| Real head unit, wired and wireless, using a TestFlight build | Cold launch with the phone locked in a pocket; interruptions; the 12-item list cap; FM radio coexistence | Gemini reports wireless `.playAndRecord` dropping to 24 kHz mono (~160 ms) against ~1100 ms latency on `.playback` (single source) |
| CarPlay Ultra car | Only if you claim instrument-cluster or head-up display behaviour | none |
| HomeView on 27.2 + iPhone on 27.2 | The app launching from HomeView; widgets on the Home Screen, the Modular face and in night mode; household privacy; an iPad pairing showing no third-party app | Gemini reports working CarPlay audio apps hanging on a loading spinner on HomeView (forum post, 17 Nov, no replies, single source) |

XCUITest: Gemini cites a forum thread (831782) saying it can't see CarPlay's accessibility tree. OpenAI, Codex and Grok found no Apple statement either way. Treat CarPlay and HomeView interaction tests as manual release gates. [all four]

## Single-source claims worth knowing

All from Gemini unless marked; none independently checked beyond confirming the cited page exists:
- **Video apps mostly show video on HomeView today.** Major streaming apps hadn't shipped CarPlay video apps by November, and most production cars report `supportsVideoPlayback == false`, so HomeView is where CarPlay video apps actually render video.
- **HomeView personalises by face.** It recognises up to 6 household members and shows each one's Home Screen when their phone is nearby and recently unlocked. Guests get shared built-in apps only.
- **iPhone Duo screenshots required from April 2027** for apps built with the iOS 27.1+ SDK. This rests on a third-party GitHub research document, not Apple.
- **WWDC26 sent video developers to the standalone CarPlay Simulator** in Additional Tools for Xcode. [OpenAI]

## Roadmap

| Date | Event | Status |
|---|---|---|
| Feb 2026 | Voice-based conversation category (iOS 26.4) | Apple-documented |
| 8 Jun 2026 | WWDC26: video category, voice in every category, MiniPlayer, map panels | Apple-documented |
| 13 Oct 2026 | HomeView announced; license agreement §§6.4.1–6.4.2; Guide reissued | Apple-documented |
| 18 Oct / 2 Nov 2026 | Robotic-arm HomeView, and a larger "HomeView Ultra", for 2027 | Rumoured [Gemini] |
| 2 Nov 2026 | Firmware code suggests HomeView can act as a HomeKit security camera | Developer-observed |
| 3–5 Nov 2026 | "Conversational Apps" string on the HomeView bridge in the iOS 27.3 beta | Developer-observed |
| 12–13 Nov 2026 | HomeView Software 27.2 released; on sale | Apple-documented |

The agreement's §6.4.2 allows HomeView access for CarPlay categories "identified by Apple in the Documentation". So Apple could add voice-conversation apps to HomeView by editing its documentation, without changing the agreement. [Grok] Re-read the Guide's HomeView footnote when iOS 27.3 ships.

## Still open

- Whether disfavoring a widget for `.carPlay` changes anything on HomeView. This needs hardware to test.
- Whether third-party Live Activities appear on HomeView.
- Whether Apple will ever approve audio plus video in one app. Ask in the entitlement request and keep the answer.
- The search cell for navigation, and the contact cell for public safety and the location-based categories, in the Guide PDF's table.
- Whether a voice template set as the root works on iOS 26.4. Apple doesn't forbid it, but nobody has tested it.
- None of the skeletons have been compiled against the iOS 27 SDK.

## Key Apple sources

- [CarPlay Developer Guide, Oct 2026 (PDF)](https://developer.apple.com/download/files/CarPlay-Developer-Guide.pdf)
- [`pushTemplate` depth table](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/pushtemplate(_:animated:completion:))
- [Building your app's initial CarPlay interface](https://developer.apple.com/documentation/carplay/building-your-apps-initial-carplay-interface)
- [`showOverlayTemplate`](https://developer.apple.com/documentation/carplay/cpinterfacecontroller/showoverlaytemplate(_:animated:completion:))
- [NowPlaying framework](https://developer.apple.com/documentation/nowplaying)
- [Adding StandBy and CarPlay support to your widget](https://developer.apple.com/documentation/widgetkit/adding-standby-and-carplay-support-to-your-widget)
- [Audio entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-audio)
- [Video entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.carplay-video)
- [Apple Support 148407 (iPad limits on HomeView)](https://support.apple.com/en-us/148407)
- [Testing your app in CarPlay Simulator](https://developer.apple.com/documentation/carplay/testing-your-app-in-carplay-simulator)
- [Widgets HIG](https://developer.apple.com/design/human-interface-guidelines/widgets)
- [CarPlay HIG](https://developer.apple.com/design/human-interface-guidelines/carplay)
