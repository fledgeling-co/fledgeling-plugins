# Introducing Spaces in Muse (LrXnOKCr0mo), findings

## Hook and structure

The film opens on a finished poster. `f0001.jpg` (t=0) holds a cream plush mascot on the left, "Introducing Spaces" and "muse.ai" on the right, and a Meta logo bottom left. The blue Muse wordmark joins by t=2s (`f0002.jpg`). In `strips/window-01-0.126s.jpg` the mascot walks in from the left edge and is fully on screen by 0.7s. It waves at about 3.4–4.4s (`strips/window-04-3.254s.jpg`). Frame 0 contains the subject and the hook lands inside 3s, which agrees with binding rule 1.

The 90.3s runtime splits into eight beats. Title card runs 0–4.46s. A presenter intro runs 4.46–13.14s. The create-a-space demo runs 13.14–32.4s. The Jolly Mall reveal runs 32.45–49.9s. The drawer rearrangement runs 49.9–60.4s. The weekend-mode chat runs 60.4–82.6s. A presenter sign-off runs 82.6–85.8s. The end card runs 85.8–90.3s. Phone UI is on screen from 13.14s to 82.62s, about 77% of runtime. The hero moment is the hard cut at t=32.5s (share 0.36) to the full-bleed blue Jolly Mall feed (`f0017.jpg`).

## Rhythm

`metrics.json` reports 15 hard cuts, 9.96 cuts per minute, a median shot of 4.47s and a longest shot of 19.31s (21% of runtime). There are no bursts (`bursts: []`). The cuts do not follow the 1.8–3.5s launch cadence of rule 10. They sit at topic changes: 4.46s, 8.05s, 13.14s, 32.45s, 41.33s and so on. Some are flicker pairs (32.45/32.57 and 64.98/65.06/65.48), probably screen-capture joins. The longest static run is 4s, ending at 12s, which is the presenter segment.

This is a feature explainer, not a launch film. It shows that a slow rhythm works when the long shots carry real in-shot motion (scroll, drawer slide, typing). It also contradicts rule 8, since it has no burst and is still watchable.

## Look and type

The look is pale and low-contrast: `look.json` gives luma 179.5 and saturation 0.195, with 80% light frames (`dark_share` 0.2). The ground behind the phone is a sky-blue gradient. The one saturated screen is the royal-blue Jolly Mall feed (`f0017.jpg`, `f0021.jpg`), which makes the personalised space the focal point of the whole film.

Titles were measured with `hf measure ink`. "Introducing" is 62px of a 720px frame (8.6%) and "Spaces" is 59px (8.2%) at t=0.5s. The pixel-font "JOLLY MALL" is 35px (4.9%) at t=61s. The end-card "Muse" is 49px (6.8%) at t=86.8s. The title is one word a line over two lines, which fits rule 3. The crop `crops/title.png` shows a rounded humanist sans in dark slate. The lower third (`crops/lowerthird.png`) reads "Alex Cornell" in bold over "Muse Product Design" in regular.

## Product interface

Real product UI is on screen about 77% of the time (frames `f0007.jpg` to `f0010.jpg`, `f0016.jpg` to `f0031.jpg`). It sits in a phone bezel with soft shadow. Chat text is legible because the phone is punched in so it fills the frame height. In `f0007.jpg` the user bubble reads "Let's make a new space that works as dashboard for the family." In `f0010.jpg`, the lunchbox card reads "Lunchbox Planner" with "4 of 7 packed". `crops/lunchbox.png` and `crops/jollymall-title.png` confirm legibility at 2x.

Taps are drawn as a grey translucent circle (`f0010.jpg`, `f0023.jpg`). They are faint in some frames (`f0028.jpg`). The demo shows the output of a user request (a family dashboard, a 90s catalogue feed, a re-ordered tab bar), so the UI is the proof of the claim.

## Motion and transitions

Fifteen hard cuts account for most seams. Others are caused by a UI event: a drawer slide, a tap ripple, a row dragged out of the list (`strips/window-32-56.265s.jpg`), a send button. At about 32.5s the tap on Jolly Mall cuts to the full feed and the phone eases from a cropped detail to the full device over about 0.8s (`strips/window-21-32.241s.jpg`). The presenter-to-phone seams at 13.14s and the reverse at 82.62s are hard cuts (`strips/window-11-13.055s.jpg`, `strips/window-45-82.541s.jpg`). The only fade is at 85.84s: the presenter cuts to black, the app icon fades up between 86.04s and 86.42s, then the store badges and Meta logo (`strips/window-46-85.753s.jpg`). Seam types: hard cut, UI state change, continuous camera move, fade through black. That is four, inside rule 7's 3–5, and none is a cross-dissolve.

## Copy on screen

Very little text is added over the picture. The title "Introducing Spaces" with "muse.ai" holds 4.46s, far above the rule 2 hold of 0.5s plus 0.3s a word. The lower third appears around 4s and is full by 6s (`f0003.jpg`, `f0004.jpg`); its hold was not measured. In-world text carries the rest: "JOLLY MALL" holds about 17s, "BUY NOW" appears at about 41.3s (`f0023.jpg`), and the chat lines "Weekend mode please" and "Weekend mode is on — Chat, Feed, Family Dashboard, Memory Bank, Scotland Trip Planner up top, everything else down in Spaces." land at 60–64s. The end card shows "Muse", the Google Play and App Store badges (`crops/badges.png`) and the Meta logo for about 3.9s, over rule 2's 2s minimum for the last line.

## Sound

The transcript source is auto-generated captions: 254 words, about 169 words a minute, with `[music]` tags throughout. `audio.json` kind is music with speech. The describe tags are speech 0.808, music 0.64, percussion 0.27, keyboard_musical 0.259, synthesizer 0.214 and drum 0.204. Only speech and music score above 0.5; the instrument tags are weak, so no instrument is named. Tempo was estimated at 124.5 bpm with confidence 0.309, which I treat as unreliable.

Integrated loudness is -19 LUFS, short-term max -16.9, true peak -1.8 dBTP, and loudness range 3.7 LU. The loudness is below rule 9's -14 LUFS target; the true peak is within -1 dBTP. The cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.067 against a chance share of 0.11. Sections are A 0–4.5s, B 4.5–16.1s, C 16.1–84.9s and D 84.9–90.3s.

## What to steal

- Open on a finished title card and let one character animate in within 0.7s (`strips/window-01-0.126s.jpg`).
- Use one saturated screen as the reveal in a pale film, and hard-cut to it at about a third of the runtime (t=32.5s, share 0.36).
- Punch the phone in so text is legible, hold long takes (up to 19s) with in-shot motion, and cut only at topic changes.
- Tell the demo as one chat story whose result is the proof.
- End on black with the icon fade (about 0.4s) and a 3.9s hold with store badges.
- Do not copy the quiet mix (-19 LUFS) or the faint tap ripples.
