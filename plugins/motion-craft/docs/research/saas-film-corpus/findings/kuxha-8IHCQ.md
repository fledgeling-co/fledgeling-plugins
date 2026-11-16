# kuxha-8IHCQ — Muse, "Plan your big day, make a space." (60.7 s)

## Hook and structure

The film opens on a poster, not a logo. `f0001.jpg` (t=0) shows a soft-fur mascot at left and "FEATURED SPACE / Wedding Planner / Built by Beverly with her Muse" at right on white. The native strip `strips/window-01-0.126s.jpg` shows the mascot absent at 0.125 s and walking in from the left by 0.2 s; the title text is fixed throughout. The "Mus" wordmark writes on near t=2 (`f0002.jpg`) and the mascot waves by 4.4 s (`strips/window-05-4.38s.jpg`). The hook is a title card, and the person arrives at the first cut, t=4.96 s.

Structure: card 0–4.96 s; Beverly introduces herself 4.96–15.1 s; a spoken problem list 15.1–19.31 s; a single phone shot 19.31–47.63 s (28.32 s, 46.7% of runtime per `metrics.json` rhythm.longest_shot); Beverly's payoff 47.63–56.22 s; end card 56.22–60.7 s. The phone shot is a demo of RSVP (tap at 24 s), Vendors/budget (30 s), Recent email (34 s) and the menu drawer (43.6 s).

## Rhythm

`metrics.json`: 15 hard cuts, 14.83 cuts a minute, median shot 1.88 s, mean 3.79 s. The gap between those two is the 28.32 s phone shot. One burst exists: 5 cuts at 15.1–19.31 s (`rhythm.bursts`, mid_share 0.283, so just before the 30% band in rule 8). The cuts at 15.1, 16.27, 17.1, 18.02 and 19.31 fall on the spoken list "RSVPs, vendors, invoices, emails, it's all everywhere" (transcript 15–19 s); `strips/window-13-15.015s.jpg` shows the first of them, a wide shot cutting to a close one. The interview halves cut every 1.1–3 s (4.96, 6.96, 9.97, 11.97 and 47.63, 49.09, 50.84, 53.84, 54.89, 56.22).

## Look and type

Three grounds: a white studio card, a dark warm bookshelf interview (dark share 0.467, light 0.533), and a white-to-sky-blue gradient behind the phone. The end card is black. Title measurements with `hf measure ink`: "Wedding Planner" 61 px of 720 (8.5%, t=1 s), its subline 27 px (3.75%), the "Mus" wordmark 70 px (9.7%, t=2 s) and the end wordmark "Muse" 50 px (6.9%, t=57 s). `look.title_height_pct` is [6.9, 8.5]. The longest title line is 2 words. Inside the phone, the type is much smaller: the email and budget text in `crops/email-card.png` is about 11–14 px on a 720 px frame, under the 2.6% floor in rule 2. The accent is disciplined. Magenta sits on the ampersand in "Beverly & Forrest", the "319" and the active filter (`crops/hero-countdown.png`), while Muse blue appears only on logos.

## Product interface

Product UI is on screen for 46.7% of runtime, as a screen recording inside a device frame on a gradient (`f0011.jpg`). The phone is about 650 px tall, 90% of frame height, but only 316 px (24.7%) wide, so two gradient flanks of about 37% of the width stay empty for 28 s. This breaks the quarter-empty limit in rule 6. The data is detailed and plausible: names, $24,200 total cost, $17,825 still owed, "4 threads are waiting on a reply" (`crops/rsvp-list.png`, `crops/email-card.png`). Headlines, numbers and chips read at phone width. Body copy does not, so the voice carries the content. One thing the voice claims is not shown: "I just tell Muse and it makes the change" (38–42 s) plays over a dashboard scrolling back to the top (`f0021.jpg`) and a menu (`f0023.jpg`), with no prompt interface in sight. The drawer header reads "Meep" and the active tab is cut to "Wedding September 2…" (`crops/sidebar.png`).

## Motion and transitions

Each tap gets a grey translucent ripple on the control: RSVP at 24 s (`f0013.jpg`), Vendors at 30 s (`f0016.jpg`), Recent email at 34 s (`f0017.jpg`), the menu button at 42 s (`f0022.jpg`). The camera pushes in on each tap: phone width goes from 316 px to about 402 px (about 1.27x) in those frames, and returns in `f0014.jpg` and `f0015.jpg` once the new page has landed. The page itself changes within a few frames (`strips/window-21-25.484s.jpg`, RSVP at 25.48–25.61 s). The drawer slides in over about 1 s (`strips/window-36-43.544s.jpg`). Seams between shots are all hard cuts (15 of 15). The cut into the phone at 19.31 s and out at 47.63 s (`strips/window-16-18.352s.jpg`, `strips/window-38-47.548s.jpg`) are both plain cuts with no transition effect. The film ends by cutting to black at 56.22 s (`strips/window-43-55.139s.jpg`) with the Meta logo fading up from dim in `f0029.jpg` to full in `f0030.jpg`.

## Copy on screen

There are no captions and no lower thirds; the speech is not subtitled (`f0003.jpg`–`f0010.jpg`). On-screen copy is the title card (10 words, held 4.96 s), the in-UI text, and the end card ("Muse", "GET IT ON Google Play", "Download on the App Store", held 4.5 s; `crops/endcard.png`). The title card clears the 0.5 s + 0.3 s a word rule (3.5 s needed, 4.96 s given) and the end card clears the 2 s last-line rule. UI copy is read by the narrator, not the viewer. The transcript is 154 words, 152 a minute over the full runtime (`transcript.md`).

## Sound

Evidence is limited to `measure/audio.json` and `metrics.json`. Kind is music, with speech tagged 0.811 and music 0.624. Instrument tags above 0.2: keyboard_musical 0.289 and synthesizer 0.218; percussion is 0.154, below the naming threshold. No steady beat (confidence 0.148). Integrated loudness is -16.3 LUFS, short-term max -13.8, loudness range 4.9 LU, true peak -2 dBTP, which is 2.3 LU under the -14 target in rule 9 and inside its true-peak limit. Sections split at 5 s and 55.5 s. Cuts on strong onsets 0.333 against chance 0.193, a margin of +0.14, so mildly locked; with 51.4 strong onsets a minute, mostly speech, the cuts follow phrasing, not a beat. I cannot confirm sound effects: none appear in the tags.

## What to steal

- Start with a poster card whose subject moves within 0.2 s, and hold the text still (`f0001.jpg`, `strips/window-01-0.126s.jpg`).
- Cut a spoken list at the speed of its items: 5 cuts in 4.2 s (15.1–19.31 s).
- On every demo tap, show a ripple, push in about 1.27x, and release when the page lands (`f0013.jpg`, `f0014.jpg`).
- Start each tap on the phrase that names it: 24 s, 30 s, 34 s against the transcript.
- Put a claim on screen when the voice makes it; the change-by-prompt line has no picture (`f0021.jpg`).
- Fill the side margins when a phone is only a quarter of the frame width, or scale the device up.
- End on a black card for 4.5 s with icon, wordmark and two store badges (`f0029.jpg`, `f0030.jpg`).
