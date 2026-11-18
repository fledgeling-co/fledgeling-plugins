# Entitlements, review and shipping

## One entitlement

Choose the single category that matches what the app is for, not the one that reaches the most
screens:

- Audio for a media app, including one that also plays video with sound (it must then support
  AirPlay video). The audio entitlement explicitly covers "audio-only content or video content
  with an audio component", and audio apps appear on HomeView.
- Video for an app that exists to play video (iOS 27+). The video entitlement cannot play
  audio-only content. Video apps appear on HomeView and in parked cars that support video.
- Voice-based conversation for an assistant whose primary modality is voice (iOS 26.4+). Not on
  HomeView today.
- The category the app's real job matches for everything else: communication, navigation,
  charging, parking, fueling, quick food ordering, driving task, public safety.

Since iOS 26.3 an app holds one CarPlay entitlement; EV charging plus fueling is the only allowed
pair. WWDC26 session 212 told media apps to ship audio and video together; the October 2026 Guide
and the entitlement pages forbid it. Follow the written rule, and if the product needs both icons,
ask Apple in the entitlement request which document governs and keep the answer. Two developer
reports describe what happens otherwise: one App Review rejection under guideline 2.5.1 (Nov 2026)
and one blank CarPlay screen after adding the video key to a working audio app (Sept 2026).

Never request an entitlement only to reach HomeView: Apple judges requests on in-car use.

## Requesting it

The Account Holder requests the category through Apple's CarPlay entitlement form and accepts the
CarPlay Entitlement Addendum. Each App ID is its own request. Apple publishes no turnaround time;
2026 reports run from days (audio) to weeks (driving task, video), with one wait of over a year,
and Developer Support has told developers it cannot reach the reviewing team. Request it before
building the car UI.

Requesting the entitlement and submitting to App Review are the user's actions, taken from their
Apple Developer account. Prepare the text; do not send it.

## After approval

1. Enable the granted capability on the App ID in Certificates, Identifiers & Profiles.
2. Regenerate the development and distribution profiles. Apple's setup article uses manual
   signing; automatic signing does not install the app into CarPlay.
3. Add the matching capability in Xcode so the `.entitlements` file carries the boolean key.
4. Check the signed build, not the project file:

   ```sh
   codesign -d --entitlements :- "Payload/YourApp.app"
   security cms -D -i "Payload/YourApp.app/embedded.mobileprovision"
   ```

   Run it on the app and every embedded extension. One developer report (forum thread 850675)
   describes a portal-issued profile missing the approved CarPlay key, which leaves the car scene
   silently never connecting.

## Shipping

- Once the key is in a build, the CarPlay icon appears for every user of that build, TestFlight
  testers included. There is no per-user flag. Ship the key only when the car UI is finished.
- Disclose CarPlay API use in the App Store Connect review notes, with sign-in credentials, media
  samples, how to reach the car UI, and why the category fits.
- HomeView has no separate review, opt-in or Info.plist key. An audio or video app appears there
  under the Developer Program License Agreement §6.4.2; widgets under §6.4.1.
- Review guidelines that apply beyond the CarPlay rules: §2.1 (complete app), §2.5.1 (public APIs
  for their intended purpose), §2.5.4 (background modes), §2.5.14 (recording consent),
  §2.5.17 (Matter), §§5.1.1–5.1.2 (privacy; 5.1.2(i) requires consent before sharing personal
  data with a third-party AI), §5.2 (media rights).
- For TestFlight and App Store Connect work, route to `app-store-connect:app-store-connect`.
