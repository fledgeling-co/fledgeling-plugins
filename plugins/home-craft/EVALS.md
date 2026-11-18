# home-craft evals

**No with-skill versus no-skill comparison has run.** The owner chose to ship without one on 18 November 2026, so there's no report card and no blind taste test, and this skill's value against having no skill at all is unproven. Everything below is what was checked mechanically, and the seven tasks that would settle the rest.

## What was verified, and how

| Check | Command | Result |
|---|---|---|
| The Swift templates compile against the iOS 27.1 SDK, Swift 6 language mode | `scripts/typecheck_templates.sh` | 4 of 4 passes: the app and widget templates, each at deployment targets iOS 26.0 and 27.0, no warnings |
| That type-check can fail | the iOS 27 availability guard around `allowsMiniPlayer` removed in a copy, then type-checked at 26.0 | failed as it should: `'allowsMiniPlayer' is only available in iOS 27.0 or newer` |
| The audit's 24 rules fire where they should and stay quiet where they shouldn't | `python3 scripts/home_audit.py --self-test` | 6 of 6 fixtures pass: two CarPlay entitlements in one target, an audio app using a point-of-interest template, NowPlaying mixed with MediaPlayer, a voice assistant with no voice template and no car scene, a widget with no removable background, and the skill's own templates as the clean case (0 errors, 0 warnings) |
| The self-test can fail | one fixture's expected result set to empty | failed as it should: `self-test: 5/6 passed`, exit 1 |
| The research holds up | Dossier's citation check on each report, then the flagged links fetched by hand | no fabricated source in the four round-2 reports; every dead link was a link-checker artefact (Apple URLs cut at a closing parenthesis, or news sites Dossier's DNS resolves to a private address) |
| Disputed rules | Apple's documentation read directly | settled six points one research member had wrong; see `skills/home-craft/references/evidence.md` |

What none of this shows: that a model with the skill builds a better CarPlay app than a model without it, and that any template behaves correctly on a real car, the CarPlay Simulator or a HomeView. Nothing here ran on hardware.

## The seven tasks that would settle it

Each runs once with the skill and once with nothing, graded on checkable properties and then judged blind by three model families in both orders. Prompts and assertions are in `skills/home-craft/evals/evals.json`.

| Task | What a good answer does |
|---|---|
| **podcast-app-carplay-homeview**: add CarPlay and HomeView to a SwiftUI podcast app deploying to iOS 26 | the audio entitlement only; the car scene routed for a car-only launch; Now Playing from one framework; iOS 27 calls behind availability checks; a small widget; the audit run and quoted; hardware lanes reported as not reached |
| **dual-entitlement-question**: "WWDC said to include both. Should we?", briefly | no; names the conflict between WWDC26 and the written rule; audio plus AirPlay video; 10 lines or fewer |
| **parking-app-homeview**: a parking app's PM wants it on HomeView | parking doesn't appear on HomeView; build a small widget; don't request another entitlement to get there; the shared face is visible to the household |
| **review-conversational-scene**: review a voice assistant's CarPlay scene before submission | findings, not edits: no voice template, no car scene routing, alert text telling the driver to unlock the phone, keychain data unreadable while locked, no record-and-play audio session |
| **expo-app-out-of-scope** (adversarial): add CarPlay to an Expo app with this skill | says the skill is native Swift only; edits nothing |
| **submit-entitlement-for-us** (adversarial): fill in Apple's form, push to TestFlight, get a banking app on HomeView by Friday | submits and uploads nothing; a banking app fits no CarPlay category, so HomeView means a small widget |
| **car-scene-never-connects**: entitlement approved, app missing from CarPlay Simulator | inspects the signed build and its profile, names automatic signing and the scene role key |

The second is the one a strong model may manage without help, because the WWDC conflict is on Apple's current entitlement page. The first and fourth turn on rules that changed after most training data, which is where the skill should show its worth.

## Decided without a run

- **A full kit rather than references only.** Templates, an audit and references, following the other craft skills in this marketplace and the rule that whatever is deterministic gets a script. The owner wasn't asked; it's the call the family had already made.
- **The icon is the raster take.** The owner chose it over the hand-built vector; `assets/audit.html` has all four takes scored, and `assets/icon.svg` stays as the editable alternative.
