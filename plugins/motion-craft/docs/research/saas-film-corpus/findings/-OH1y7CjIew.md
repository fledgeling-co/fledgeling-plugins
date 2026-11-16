# Coding on the go with Claude Code (-OH1y7CjIew)

## Hook and structure

The film opens on a presenter, not a logo. f0001.jpg (t=0) shows her smiling at a desk, half-faded under a ghost of the task input; the prescan marks it not-evidence (`frames.frame0` contentfulCells 0.0063), so the poster is murky rather than clean. The hook still lands inside 3 s: "Watch this." (t=0), the task typed into the desktop app (strips/window-02-1.625s.jpg shows the sentence "The newsletter sign-up form accepts an invalid email address…" and "Setting up a cloud container"), then the laptop closing (f0003.jpg, t=4). The hero moment is the phone question at t=10: "The footer has a second sign-up form with the same check. Should I fix both?" (f0005.jpg-f0007.jpg), 4.1% of runtime in.

After that the film is a tutorial: define the term (t=16-41), when to use it (t=43-70), GitHub setup (t=70-100), environments (t=100-126), what is cloned (t=126-152), then one worked example from t=152 to t=228 (newsletter bug, phone question, diff, PR #128), and a teleport recap at t=228-238. It ends on the presenter with a docs chip (f0121.jpg, t=240). There is no logo end card.

## Rhythm

`metrics.json` gives 32 hard cuts, 7.93 per minute, median shot 5.54 s, 6 shots over 10 s and no burst. The longest shot is 26.7 s (t=201.4-228.1, the phone diff and PR). 32.5% of sampled intervals are static (`intervals_static_share`), and the longest static run is 10 s ending at t=170. The cadence is far slower than the 1.8-3.5 s launch rule because narration carries the content. Cuts land on sentence ends, not on sound: `cuts_on_strong_onset_share` 0.094 against `chance_share` 0.06.

## Look and type

Two worlds: a dark wood-panelled presenter room, and a warm cream ground for diagrams and UI (light share 0.76, dark 0.21). Coral appears only on Claude's asterisk, send button and status dots (f0016.jpg, f0058.jpg); the one blue element is the recorded GitHub banner (crops/popover.png, "Two steps to work in your repository"). Titles are a serif, sentence case, with a geometric sans for cards and a mono for code (crops/diff.png).

Measured with `hf measure ink` on 1280x720: "When to use a cloud session" 29 px = 4.03% (t=44.5), "On Team and Enterprise plans" 32 px = 4.44% (t=126), "The Acme newsletter" 50 px = 6.94% (t=168, inside the demo site) and the small label "Cloud session" 22 px = 3.06% (t=190). Range 3.06-6.94%. The lower thirds ("Connecting GitHub", crops/lowerthird.png) could not be measured over the photo background. Longest title line is 6 words.

## Product interface

Product UI is on screen about 44% of runtime (frame-count estimate). It is scripted: a fictional Acme repo and "ada@example" as the bad email (crops/acme-error.png). The same bug runs through the desktop app, phone and diff, so every feature is a step in one story. Recordings are cropped to the active region: the phone question text in f0087.jpg is large, while the whole-phone shot in f0005.jpg has about 12 px text, under 2.6% of height. GitHub install text at t=86-92 (f0046.jpg) is also small. The error line "Something went wrong on our end. Please try again." is a pale pink on cream (crops/acme-error.png) and easy to miss. The cursor is a stylised hand with motion blur (f0040.jpg) and a grey tap circle (f0102.jpg).

## Motion and transitions

Most presenter-to-graphic seams are dissolves of about 3 frames. In strips/window-12-18.875s.jpg the blend exists only at f455 (t=18.958) between f454 (diagram) and f456 (presenter); strips/window-13-20.875s.jpg and strips/window-01-0.375s.jpg show the same. They read as cuts but are technically cross-dissolves between worlds. Inside diagrams, cards slide into new positions and connectors draw after they land (strips/window-13-20.875s.jpg, t=21.0-21.75). A UI state change dims the laptop panel to grey to show it can be off (strips/window-29-50.75s.jpg). The phone-to-presenter seam at t=7.9 is also a dissolve (strips/window-06-7.792s.jpg, blend at f189); I did not confirm any seam as a true hard cut in a strip. Per-type counts in `findings.json` are estimates.

## Copy on screen

On-screen text is a short chapter label plus diagram labels: "What is a cloud session?" (t=19.2, held about 1.8 s against 1.7 s needed), "When to use a cloud session" (t=43, held about 27 s) with chips "Long tasks", "Away from your computer", "Several at once" appended (f0034.jpg, t=66), "Connecting GitHub" (t=70), "How environments work" (t=100), "From your phone" (t=172), "Reviewing the work" (t=200) and the URL chip "code.claude.com/docs/en/claude-code-on-the-web" (crops/url-chip.png, about 4 s). The title stays dead still while chips add beneath it. The spoken facts (two-step setup, branch per session, teleport flag) all reach the screen as UI or diagram labels.

## Sound

Voice only. `audio.json` kind is voice and the top describe tag is speech at 0.922; music scores 0.106, below 0.2, and there is no steady beat (`beats.count` 0), so no music claim is made. Integrated loudness is -14.2 LUFS, true peak -1.4 dBTP, loudness range 2.1 LU, short-term max -12.4. That meets the -14 LUFS, -1 dBTP target. The cuts are not locked to the sound: 0.094 against chance 0.06 is a gap of 0.034, under the 0.10 threshold. I could not hear the film, so tone and room sound come from tags only.

## What to steal

- Build diagrams one card per spoken item and hold the title still while chips append (t=43-70).
- Carry one fictional example through every UI scene.
- Label each topic change with a 2-5 word serif lower third, six in 242 s.
- Crop UI to the active control so text clears 2.6% of frame height.
- Keep voice-only mixes at -14 LUFS with true peak near -1.4 dBTP.
- A 0.125 s dissolve between on-camera and graphics works for a talk-led film.
