# Email Harvey and Get Answers On the Go (dUIuvfP2j2c)

## Hook and structure

The film opens on a black frame with a small white serif "Harvey" wordmark (f0001.jpg). Its ink is 59 px tall at t=0.8 s, and `frames.frame0.contentfulCells` is 0.05, so the frame is mostly empty. A hard cut at 1.46 s lands on white, and "Now An Email Away" builds word by word (strips/window-01-1.375s.jpg). That is the hook, and it arrives at 1.5 s, inside the 3 s limit. The first product frame is a notification toast at 3.04 s.

The story runs as one scenario:

- 3.04-7.46 s: an email arrives with a PDF redline attached (f0003.jpg).
- 7.46-8.58 s: a close-up of the Forward button.
- 9.25-11.2 s: the address typed in giant letters.
- 11.2-15.1 s: the compose window.
- 15.1-16.4 s: oversized blurred answer text (f0009.jpg).
- ~18.5 s: an "H Done." card.
- 18.58-22.04 s: the reply with a comparison table.
- 22.04-26.1 s: a black end card, "AI Tailored for Law".

I place the hero moment at 18.58 s (share 0.712), when the answer arrives. The transcript is `none`: whisper returned only "Music".

## Rhythm

`metrics.json` gives 8 hard cuts, 18.39 cuts a minute and a median shot of 1.58 s. Cuts fall at 1.46, 3.04, 4.54, 7.46, 8.58, 9.25, 18.58 and 22.04 s. Six of the eight sit in the first 9.3 s. After that comes one 9.33 s shot, 35.7 % of runtime, from 9.25 to 18.58 s, so there is no burst (`bursts` is empty) and no 5-8-cut cluster. The pacing is quick setup, then a long calm demo. The longest static run is 2 s, ending at 24 s.

## Look and type

The film uses two grounds, white for the product and black for the cards (light share 0.769, dark share 0.231). Saturation is 0.007; the only colour is the small red PDF icons (crops/attach.png). The active control takes a near-black fill: Forward at 8.58 s (strips/window-05-8.209s.jpg) and Send (f0008.jpg). Titles are a high-contrast serif on one line, and I found no accent word. Measured with `hf measure ink` against the 720 px frame height:

| t | line | height | % of frame |
|---|---|---|---|
| 0.8 s | Harvey | 59 px | 8.2 |
| 2.5 s | Now An Email Away | 62 px | 8.6 |
| 23 s | AI Tailored for Law | 51 px | 7.1 |
| 23 s | Harvey (end-card wordmark) | 39 px | 5.4 |

The longest title line is 4 words. The interface is set in a grotesque sans (crops/compose-head.png).

## Product interface

The interface is on screen from 3.04 to 22.04 s, about 72.8 % of runtime. It reads as a redrawn, simplified Outlook-style mail client with a real-looking cursor (strips/window-05-8.209s.jpg). The content is fictional: Acme Corp, John Doe, jane@whitfordlane.com. The full-window shots are small: body text is about 8-10 px at 1280 px width (f0003.jpg, f0007.jpg), and the table is unreadable at phone width. The two close-ups carry the legibility. "Forward" glyphs are about 70 px tall (f0005.jpg) and "ask@harvey.ai" about 100 px (f0006.jpg). The table text only becomes readable in the 2x crop (crops/table.png: "Strongly Buyer-favorable control pre-closing…"). Legibility at phone width is therefore partial.

## Motion and transitions

Every one of the 8 seams is a hard cut. Some are paired with a content logic:

- **Zoom by cut:** 7.46 s into the Forward close-up and 9.25 s into the address close-up.
- **State change:** Forward turns black when the cursor arrives, at 8.58 s.
- **Blur transition:** at 15.1-16.4 s the compose window gives way to giant faded answer text drifting in blur (strips/window-11-15.084s.jpg).

Text enters by words fading in left to right over about 0.4 s. The address types at about 0.1 s a character, with a caret (strips/window-07-9.417s.jpg). The cursor takes 11 frames (about 0.46 s) to travel into Forward and decelerates on arrival. Window shots drift slightly larger between f0003.jpg and f0004.jpg. I count 4 kinds of transition. I did not open strips/window-12, so the start of the "Done." card is untimed.

## Copy on screen

The full set of on-screen lines:

- "Harvey" (0-1.46 s).
- "Now An Email Away" (1.5-3.04 s, 1.54 s hold against the 1.7 s the reading rule asks for for 4 words, so slightly short).
- "ask@harvey.ai" (9.25-11.2 s).
- "Done." (seen at 18.5 s).
- "AI Tailored for Law" (22.04-26.1 s, 4.06 s hold).

The email body is the only prose: "Compare this latest version of redlines to the prior version from Acme Corp. Summarize material changes, focusing on key obligations, duration, scope, and exceptions." (f0007.jpg). It stays on screen about 4 s as small type, so it is more set dressing than a line meant to be read.

## Sound

There is no speech. `audio.json` classes it as music with describe tags music 0.752, singing_bowl 0.351, keyboard_musical 0.326, percussion 0.254, gong 0.247 and synthesizer 0.242. No steady beat was found (confidence 0.016). Loudness is -22.7 LUFS integrated, -19.8 short-term max, true peak -3.5 dBTP and LRA 4.7 LU, so the film is far quieter than a -14 LUFS social master. `cuts_on_strong_onset_share` is 0.125 against a `chance_share` of 0.028, a lead of 0.097, below 0.10, so the cuts are not locked to the sound. Sections run A 0-8.5 s, B 8.5-18.5 s and C 18.5-26.09 s. Those edges sit within 0.1 s of the cuts at 8.58 and 18.58 s, which suggests the edit follows the music's structure rather than its onsets. I could not identify sound effects.

## What to steal

- Show the one thing to copy as an extreme close-up, typed live: the address at about 100 px (f0006.jpg).
- Prove the result with a reply that appears in the same email client, not a separate graphic (f0010.jpg, f0011.jpg).
- Bridge from question to answer with giant blurred answer text, then reveal the full reply (strips/window-11-15.084s.jpg).
- Hold the end card for 4 s with a one-line serif title at 7.1 % of frame height (f0012.jpg, f0013.jpg).
- Line up music sections with cuts even when onsets do not match.
- Avoid: a wordmark-only frame 0 and full-window UI shots at 8-10 px type. The film opens on a black frame with only a wordmark, which breaks binding rule 1, and the table payoff is unreadable at phone width.
