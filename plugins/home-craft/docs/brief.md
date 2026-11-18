# home-craft brief (agreed 18 November 2026)

- **Trigger:** building, adapting or reviewing a native Swift/SwiftUI iOS app for CarPlay or Apple
  HomeView on iOS 26/27; choosing a CarPlay entitlement; a car scene that never connects; CarPlay
  widgets and Live Activities; testing and submitting a CarPlay app.
- **Output:** code changes from bundled templates, a static audit result, and a report of at most
  40 lines with each test lane marked seen, not reached or not built.
- **Done:** `home_audit.py` exits 0, the app builds, and the report claims no lane that did not run.
- **Never:** request entitlements, change portal signing or submit on the user's behalf; combine
  CarPlay entitlements; claim a HomeView SDK; present a single forum report as Apple policy.
- **Scope:** native Swift and SwiftUI only. The user ruled out Expo and React Native.
- **Routing:** `app-store-connect:app-store-connect`, `proctor:proctor`, `design-craft:design-craft`,
  `ux-craft:ux-craft`, `duo-craft:duo-craft`.
- **Research:** reused, not re-bought: two Dossier rounds run earlier the same day
  (`docs/deep-research/`).
- **Decided by the user:** ship without a with/without-skill benchmark run; icon concept "one tile,
  two screens".
- **Decided without asking:** a full kit (templates, audit, references) rather than references only,
  following the `-craft` family and create-skill's rule to script what is deterministic.
