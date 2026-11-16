# Getting started with Claude Tag (_f_rtbW_uFM)

## Hook and structure

Frame 0 is not black or empty. The sage ground with hand-drawn wavy lines is on screen and the first word of the title, "@Claude", appears by t=0.07s (strips/window-01-0.034s.jpg). The whole title, "@Claude works with your whole team", is complete by 0.77s, so the hook lands well inside 3 s. It sits on the same promise the narrator makes at [00:00]. A terracotta hand-drawn underline marks "@Claude" (f0001.jpg).

The film runs 179 s in thirteen beats. A title card (0-4.71s) is followed by an 83.5 s Slack screen recording (4.71-88.22s, 46.6 % of runtime, `metrics.json` rhythm.longest_shot). That recording runs setup, a long typed prompt, a checklist thread and a permission prompt. A phone chapter (88-97s) follows, then the chapter title "Claude learns your team over time" (97.18s). Memory demos run 103-139s, plan cards appear at 139.6s, the configuration card and privacy titles run 144-166s, and the CTA at 166.6s. Cream end cards close the film from 172.94s. I put the hero moment at t=44.98s (0.251 of the runtime): the zoomed thread panel where Claude's four-step list finishes and the outstanding-items report lands (f0045.jpg, f0049.jpg).

## Rhythm

`metrics.json` gives 9 hard cuts, 3.02 cuts a minute, a median shot of 6.09 s, a mean of 17.91 s and no bursts. Cuts are at 4.71, 88.22, 91.09, 97.18, 103.22, 139.61, 144.46, 166.62 and 172.94 s. Pace comes from change inside shots: typing, a panel sliding in, checklist items advancing, camera zooms. The cut rate is far from the 1.8-3.5 s the skill sets for launch films, and the film still holds attention because something on screen changes every 2-6 s while the narrator speaks. Static stretches reach 12 s at most (`intervals_static_share` 0.393, `longest_static_run_s` 12), mostly on the configuration card (f0073.jpg to f0082.jpg).

## Look and type

Two grounds are used: sage green with pale wavy lines for titles and device scenes, and cream for the end cards (f0088.jpg, f0090.jpg). `look.json` reads as bright and low-saturation (luma 224.9, saturation 0.044, light_share 0.978). White Slack and settings windows float on the sage with a soft shadow. The titles are a high-contrast serif in near-black, sentence case, no more than 6 words a line, with one accent only: the underline in the opening title.

Title ink lines, from `hf measure ink` on a 720 px frame: 82 px (11.4 %) at 1.5 s and at 100.5 s, 43 px (6.0 %) for "Claude Tag is available on" at 141 s, 32 px (4.4 %) for "You control which tools" at 145 s, and 48 px (6.7 %) for the CTA at 169 s. The range, 4.4-11.4 %, goes above the 4-9 % band for the openers and sits inside it for the mid-film chapter titles. The measure covers line ink including ascenders and descenders, so it overstates cap height. The mid-film titles share the frame with a UI card, which is why they are smaller (f0076.jpg, f0082.jpg).

## Product interface

Real Slack UI is on screen for about 80 % of runtime. It is shown as a full desktop window (f0004.jpg), a zoomed thread panel (f0019.jpg, f0022.jpg), an iPhone mockup (f0046.jpg-f0049.jpg), and a floating configuration card ("Configure Claude for #event-prep", crops/config-header.png). The cursor is a real arrow that hovers and clicks the send button and "Allow" (f0034.jpg).

The detail is concrete and readable in the zoomed views. The checklist reads "Read through 7 recent threads", "Read meeting notes in Drive", "Cross-checking Asana tasks", "Drafting status summary" (f0019.jpg). The report reads "Guest speaker briefs - (Due tomorrow - Sep 24) not yet sent" and "5 of 47 speakers unconfirmed" (f0022.jpg). The permission prompt shows "Allow" and "Don't allow" (f0034.jpg). Full-window views are small: the Slack UI text is about 8-10 px high, and the card's helper text is below 7 px (crops/channel-instr.png), so those views are only partly legible at phone width.

## Motion and transitions

Titles build one word at a time; each word fades from grey to black in about 0.1-0.2 s and the next starts before the last settles (strips/window-01-0.034s.jpg: six words between 0.07 and 0.53 s). They leave the same way in reading order, over about 0.5 s, before a hard cut (strips/window-02-4.054s.jpg, strips/window-48-102.536s.jpg).

Inside the recording, typing is character by character with a caret (f0013.jpg, f0016.jpg). Sending drops the message into the feed and the thread panel opens in 0.4 s (strips/window-10-36.27s.jpg). The phone chapter is introduced by a hand-drawn outline drawn on from 88.22s, a dot, the lock-screen fill at 88.96s, then a notification and a cross-fade to the app thread at 91.09s (strips/window-41-88.188s.jpg, strips/window-43-90.758s.jpg). At 125.9s the camera pans between panes with motion blur (strips/window-60-125.943s.jpg). Every cut follows the end of a title or a chapter, so each one has a cause on screen.

## Copy on screen

Titles are short and plain: "@Claude works with your whole team", "Claude learns your team over time", "Claude Tag is available on" (with Team and Enterprise cards), "You control which tools and data it can use", "Set what it has access to in each channel", "DMs and private channels stay private", "Tag @Claude in on your team's next task", and "claude.com/learn" (f0001.jpg, f0073.jpg-f0090.jpg). All quoted text was read from full-resolution frames or crops.

Holds are longer than the 0.5 s + 0.3 s per word rule: a 6-word title holds about 4-6 s against a 3.2-3.5 s minimum. The URL holds about 2 s, the minimum for a last line. The narration covers the claims that never appear on screen: the "Team and Enterprise" plan note, the logging of every change and "asking for permission every time" (transcript [00:56], [01:00]). Only the permission prompt itself is shown (f0034.jpg).

## Sound

The transcript source is human captions, 497 words, about 167 words a minute, spoken by one narrator. `audio.json` kind is music, with describe tags speech 0.842, music 0.628, keyboard_musical 0.282, plucked_string_instrument 0.242, guitar 0.193; only the first four are above 0.2. There is no steady beat (confidence 0.14, `beats.count` 0). Integrated loudness is -14 LUFS, the short-term max is -12.9 LUFS and the loudness range is 3.6 LU: a flat mix. True peak is +0.5 dBTP, which breaks the -1 dBTP ceiling. Cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.0 against `chance_share` 0.079. Silence runs from 174.1s to the end, spanning the Claude Academy and URL cards. I did not listen to the film.

## What to steal

- Show the product as it is used: a typed request, a visible checklist, a result with links, a permission prompt. These made up about 80 % of the runtime (f0019.jpg-f0034.jpg).
- Zoom to the panel being narrated and pull back to the full window to keep context (f0004.jpg vs f0022.jpg).
- Build titles word by word on a plain ground. One accent, one idea per card, and a hard cut afterwards (strips/window-01-0.034s.jpg).
- Hand off between devices with a drawn outline that fills with the next screen (strips/window-41-88.188s.jpg).
- End on a quiet card with the logo and one URL (f0088.jpg, f0090.jpg).
- Avoid this film's faults. Fix the true peak (+0.5 dBTP), keep full-window UI text above 7 px, and shorten the 22 s configuration scene.
