# Evidence: where each rule comes from

Corpus: `docs/deep-research/` in this plugin (Dossier, 18 November 2026; four round-2 members:
OpenAI Deep Research, Gemini Deep Research, Codex, Grok). **Checked** means confirmed directly
against Apple's documentation JSON or support pages during the merge, which outranks every
member. **Members** names the reports that made the claim; one name means single-sourced.

## Platform facts

| Claim | Basis | Members | Confidence |
|---|---|---|---|
| Max depth: Video = 5, root included | Checked: `pushTemplate(_:animated:completion:)` table lists Video 5 | OpenAI (others inferred or left it open) | High |
| Depths for all 11 categories | Checked: same table | all four | High |
| Any template may be the root | Checked: "You can install any template as the root template of your interface" | OpenAI; Gemini wrongly said Voice Control cannot be root | High |
| `showOverlayTemplate` / `hideOverlayTemplate` exist (iOS 27) | Checked: SDK header `API_AVAILABLE(ios(27.0))` and doc page | Gemini, Grok | High |
| `allowsMiniPlayer` (iOS 27), `playbackConfiguration` and `supportsVideoPlayback` (iOS 26.4), `actionButtons` (26.4) | Checked: iOS 27.1 SDK headers; templates type-check | all four | High |
| Don't mix NowPlaying with MPNowPlayingInfoCenter/MPRemoteCommandCenter | Checked: NowPlaying framework docs, "results in undefined behavior" | Gemini only | High |
| `disfavoredLocations` does not remove a widget | Checked: "Doing so doesn't exclude your widget from CarPlay or StandBy" | OpenAI, Codex, Grok; Gemini wrongly said it hides on CarPlay and HomeView | High |
| No `WidgetLocation` case for HomeView | `WidgetLocation` reference | all four | High |
| Tab limit depends on the entitlement (4 audio, 5 others) | Checked: `maximumTabCount` "depends on the app's entitlements"; numbers from the Guide | OpenAI, Grok; Gemini wrongly gave a flat 4 | High |
| Public safety may use Now Playing; no Map | Checked: `CPNowPlayingTemplate` page names public safety | Grok, OpenAI; Gemini wrongly listed Map | High |
| Navigation has no Now Playing or Point of Interest | Guide matrix | OpenAI, Grok; Gemini wrongly listed both | Medium (Search cell needs the PDF) |
| Contact for public safety | Guide tables include it; `CPContactTemplate` page omits it | OpenAI flagged the conflict | Disputed |
| Contact for charging/parking/fueling/food ordering | Gemini only | Gemini | Disputed |
| One entitlement since iOS 26.3; charging + fueling the only pair | Guide; audio and video entitlement pages | all four | High |
| WWDC26 told media apps to ship audio + video | WWDC26 session 212 | all four | High (that the conflict exists) |
| Audio entitlement covers "video content with an audio component", needs AirPlay video | Audio entitlement page; Guide | all four | High |
| Video entitlement cannot play audio-only content | Video entitlement page | Codex, Grok | High |
| Voice-based conversation category from iOS 26.4 | Entitlement page; Feb 2026 Guide | all four | High |
| Xcode 27.2: iOS Simulator not supported for CarPlay; Device Hub needs a USB iPhone | Xcode 27.2 release notes; testing article | all four | High |
| No public XCUITest route into CarPlay templates | Absence across Apple docs; forum thread 831782 | all four (absence) | Medium |
| Apple publishes no entitlement SLA | Forum thread 82791 (2018); absence since | all four | High |

## HomeView facts

| Claim | Basis | Members | Confidence |
|---|---|---|---|
| Software 27.2, build 24V526, released 12 Nov 2026; on sale 13 Nov | Apple developer releases; Newsroom | all four | High |
| tvOS 27.2 derivative | Firmware inspection (Troughton-Smith, Rambo, The Apple Wiki) | all four | Medium (developer-observed) |
| No SDK, store, destination, simulator, design kit | Absence; DTS forum reply 13 Oct 2026 | all four | High |
| Audio and video CarPlay apps run on HomeView unchanged, from a paired iPhone | developer.apple.com/carplay; licence agreement §6.4.2; Guide footnote | all four | High |
| An iPad companion cannot supply third-party audio/video apps | Checked: Apple Support 148407 | Codex, round-1 Grok; Gemini wrongly said iPad works | High |
| Widgets on the Home Screen and the shared Modular face; up to 4 on the face | Widgets HIG HomeView section; §6.4.1 | all four (count: OpenAI, Codex) | High |
| Third-party Live Activities on HomeView | not documented | all four | Open |
| "Conversational Apps" string in iOS 27.3 beta `PebblePlayCore` | ipsw-diffs; pdfu; 9to5Mac | all four | Medium (code exists; feature unannounced) |
| Up to six household members recognised by face | HomeView user guide, as cited | Gemini only | Low |

## Single-source developer reports (useful leads, not rules)

All Gemini unless noted, each traced to a forum thread or one article: App Review rejecting a
dual-entitlement build under 2.5.1; a profile issued without the approved key (thread 850675);
Now Playing freezing with `ApplicationMusicPlayer` (FB24840951); disappearing section headers
(FB24061858); a HomeView loading-spinner hang (17 Nov 2026); wireless `.playAndRecord` at 24 kHz
mono; most production cars reporting no video support; an app removed on 23 Oct 2026 for
browser-view video. A blank CarPlay screen after adding the video key to an audio app (Grok).

## What the research did not settle

Third-party Live Activities on HomeView; whether disfavoring a widget changes anything on
HomeView; whether Apple will grant audio plus video to one app; the Navigation Search and the
Contact cells above; whether a Voice Control root behaves on 26.4.
