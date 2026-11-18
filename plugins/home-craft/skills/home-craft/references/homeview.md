# HomeView: what it is to a developer

Apple HomeView is a 7-inch square smart display (1088×1088, 220 ppi), announced 13 October 2026
and on sale 13 November 2026 at US$299, outside the EU. It runs **HomeView Software 27.2**
(build 24V526). Firmware inspection by developers shows a tvOS 27.2 derivative (device family 8,
launcher "BreadBoard"); Apple calls it only "HomeView software".

## How a third-party app reaches it

There is no HomeView SDK, App Store, Xcode destination, simulator or design kit. Apple Developer Technical Support (DTS) told a
developer to keep the iPhone as the destination. Two routes exist, both from a **paired iPhone**:

1. **The app itself**, if it holds the CarPlay **audio** or **video** entitlement. It runs on the
   iPhone and HomeView shows its CarPlay templates, adapted by the system (tabs become a menu).
   Apple: CarPlay audio and video apps "work on HomeView without requiring you to make any
   modifications". Licence agreement §6.4.2 allows any category Apple's documentation names;
   today the documentation names those two.
2. **A system-small widget**, for any app, under licence agreement §6.4.1: on HomeView's
   personalised Home Screen and on the shared Modular face.

An iPad can be HomeView's companion, but Apple Support (148407) says an iPad cannot supply
third-party audio or video apps or remote widgets that control devices. HomeView recognises up to
six household members by face and shows each one's Home Screen when their phone is nearby and
recently unlocked (one source); guests get the shared built-in apps.

## What is not a route

- Live Activities: HomeView shows Apple's own (timers, media, Intercom). Third-party ActivityKit
  activities are not documented there.
- HomeKit and Matter: accessories show in the Home app on HomeView; integrating them does not put
  the app on HomeView.
- Voice-based conversational CarPlay apps: not at launch. iOS 27.3 beta adds a private
  "Conversational Apps" category string to the bridge (`PebblePlayCore`) with two-way audio work
  started. Apple has announced nothing. Because §6.4.2 defers to the documentation, Apple could
  enable it with a documentation change; re-read the CarPlay Developer Guide's HomeView footnote
  when iOS 27.3 ships.

## Design consequences

- HomeView sits on a kitchen counter, not in a car: the same app is read at a distance by
  whoever walks past. Treat the shared Modular face as public.
- A video app's real audience today may be HomeView rather than the car, because most production
  cars do not yet report video support (one source).
- An app outside audio and video should not request a CarPlay entitlement to reach HomeView; build
  the widget.

## Roadmap, labelled

| Date | Item | Status |
|---|---|---|
| 13 Oct 2026 | HomeView announced; licence agreement §§6.4.1–6.4.2 | Apple-documented |
| 2 Nov 2026 | Firmware suggests HomeView can act as a HomeKit security camera | Developer-observed |
| 3–5 Nov 2026 | "Conversational Apps" string on the bridge, iOS 27.3 beta | Developer-observed |
| 12–13 Nov 2026 | Software 27.2 released; on sale | Apple-documented |
| Oct to Nov 2026 | A larger "HomeView Ultra" and a robotic-arm model for 2027 | Rumoured |
