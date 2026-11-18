# Capability matrix: CarPlay categories, templates and depth (iOS 26.x, iOS 27.x, HomeView)

Source: Apple's CarPlay Developer Guide (13 October 2026), the `pushTemplate(_:animated:completion:)`
depth table, and Apple's per-template pages, as read by four research members and cross-checked
directly where they disagreed. `evidence.md` has the provenance for each contested cell.

Every category is one entitlement key, `com.apple.developer.carplay-<suffix>`. A template outside
the category's list throws at runtime when pushed or presented. Depth counts the root template.

**B** = `CPListTemplate`, `CPGridTemplate`, `CPTabBarTemplate`, `CPActionSheetTemplate`, `CPAlertTemplate`.

| Category (suffix) | iOS 26.x templates | Added in iOS 27 | On HomeView | Max depth |
|---|---|---|---|---|
| Audio (`audio`) | B, Now Playing | Search, Voice Control; MiniPlayer (`allowsMiniPlayer`, on by default) | **Yes**: the app itself, from a paired iPhone | 5 |
| Video (`video`) | not a category before 27.0 | New in 27.0: B, Now Playing, Search, Voice Control. Parked only; hidden in cars that cannot play video | **Yes**: the app itself, from a paired iPhone | 5 |
| Voice-based conversation (`voice-based-conversation`) | From 26.4: B, Information, Point of Interest, Voice Control. No Now Playing, Map or Contact | overlay presentation of Voice Control | No (iOS 27.3 beta string only) | 3 |
| Communication (`communication`) | B, Contact, Information, Now Playing | Voice Control | No | 5 |
| Navigation (`maps`) | Map (root over the `CPWindow`), B, Search, Contact, Information, Voice Control. No Now Playing, no Point of Interest | Map panels (`showPanel`) | No | 5 |
| Public safety (`public-safety`) | B, Contact\*, Information, Now Playing, Point of Interest. No Map | Search, Voice Control | No | 5 |
| EV charging (`charging`) | B, Information, Point of Interest (Contact\*) | Search, Voice Control | No | 5 |
| Parking (`parking`) | B, Information, Point of Interest (Contact\*) | Search, Voice Control | No | 5 |
| Fueling (`fueling`) | B, Information, Point of Interest (Contact\*) | Search, Voice Control | No | 3 |
| Quick food ordering (`quick-ordering`) | B, Information, Point of Interest (Contact\*) | Voice Control (no Search) | No | 2 through 26.3, 3 from 26.4 |
| Driving task (`driving-task`) | B, Information, Point of Interest; Voice Control from 26.4 | (none) | No | 2 through 26.3, 3 from 26.4 |
| Widgets (no entitlement) | `.systemSmall` in the CarPlay widget stack, CarPlay Ultra included | (none) | **Yes**: Home Screen and the shared Modular face | n/a |
| Live Activities (no entitlement) | `.supplementalActivityFamilies([.small])`, non-interactive | (none) | Not documented for third-party apps | n/a |

\* Disputed cell. Contact for public safety: both Guide tables include it, but `CPContactTemplate`'s
own page omits public safety. Contact for charging, parking, fueling and food ordering: one research
member listed it and three did not. The Navigation Search cell is easy to misread in a text extract
of the Guide's table. Check the Guide PDF before shipping any of these; `home_audit.py` warns on them.

## Combining categories

Since iOS 26.3 an app holds one CarPlay entitlement. The single exception is EV charging plus
fueling. WWDC26 session 212 (June 2026) told media apps to ship audio and video together; the
October Guide and both entitlement pages forbid it, and no Apple document reconciles them. The
audio entitlement already covers "audio-only content or video content with an audio component",
provided the app supports AirPlay video.

## What CarPlay Ultra changes for a third-party app

Nothing in the template list or the entitlement. The same CarPlay framework draws the app on an
Ultra car. Navigation apps keep the instrument-cluster and head-up-display scenes
(`CPTemplateApplicationInstrumentClusterScene`). Climate and vehicle controls are the automaker's,
not an App Store app's.

## Other numeric limits

- Lists: read `CPListTemplate.maximumItemCount` and `maximumSectionCount`; some cars show 12 rows.
  An Apple engineer gave 500 as the app-side cap (December 2025). Only a list may be pushed on top
  of Now Playing.
- Tabs: read `CPTabBarTemplate.maximumTabCount`. It depends on the entitlement: 4 for audio and 5
  for every other category today, and Apple says it may change.
- Grid: the first 8 buttons show.
- Point of interest: at most 12 locations. Quick food ordering shows at most 12 recent orders or
  favourites, never a full menu.
- Voice Control: up to 5 states; from 26.4 up to 2 action buttons per state and up to 2 trailing
  navigation bar buttons; state changes are rate-limited.
- Driving task: refresh the UI no more often than every 10 s, points of interest no more often
  than every 60 s.
