# We8BTITLvb4: Introducing Muse: your personal AI agent

## Hook and structure

The film is 82.58 s of music with no voiceover (transcript.md: source none; whisper returned only sung lyrics). Frame 0 (`f0001.jpg`) is the Muse app icon, about 21 % of frame height, centred on pale grey with the edge of a yellow sticky note entering at left. That is close to the lone-logo poster the skill warns against: `frames.frame0` reports blankCells 0.919. In `strips/window-01-0.959s.jpg` the icon holds still while 3D objects fly in, and a grid of about 40 fills the frame by 1.7 s. "Introducing" is on screen at t=2 (`f0002.jpg`), so the subject and the claim both land inside 3 s.

After that the film runs as five product vignettes: school-email shopping (17.5 to 30 s), race sign-up (34 to 47 s), flight delay (52 to 67 s), then a calendar update. Title cards in one template sit between them, "AI that [verb phrase] for you", at t=32, 48, 50, 70, 72 and 80. Hero moment: confetti over "Your Muse gets it done" at t=68 (`f0035.jpg`), 0.823 of runtime. The film ends on "AI that keeps you in control" (`f0041.jpg`, t=80), then a hard cut at 81.67 s to a black end card with store badges.

## Rhythm

`metrics.json` gives 8 hard cuts, 5.81 cuts per minute and a median shot of 4.75 s. Four shots run over 10 s. The longest shot lasts 27.67 s (17.5 to 45.17 s, 33.5 % of runtime). That is well outside the 1.8 to 3.5 s launch range, yet `intervals_static_share` is 0.1: 90 % of 2 s intervals show change. The change is camera push-ins and UI state swaps. `bursts` is empty, so there is no cluster of rapid cuts. Colour carries the peak: the confetti at 68 s.

## Look and type

Title cards sit on a near-white to pale-blue gradient (`f0002.jpg`), chat scenes on light grey (`f0028.jpg`). Black appears only inside the browser frame (`f0022.jpg`) and the end card. `look.saturation` is 0.039. Blue is the only accent: the word "Muse" in "Introducing Muse" (`strips/window-03-3.834s.jpg`), the Allow and Submit buttons, and the check icons.

Titles are centred black sans, two or three lines, at most three words a line. I measured four lines with `hf measure ink`: "Introducing" at t=2.5 is 91 px (12.6 % of 720, including the descender of "g"), "AI that" at t=32 is 75 px (10.4 %), and "AI that" and "keeps you in control" at t=78 are 57 and 58 px (7.9 % and 8.1 %). The largest title is therefore above the skill's 4 to 9 % range, and the closing claim sits inside it. In `crops/title-personal-agent.png` a 3D emoji takes the place of a word in "Muse [avatar] is your [calendar] personal AI [pen] agent", which breaks the one-accent-word rule: the emoji do the accenting.

## Product interface

Product UI is on screen for roughly half of the film (about 52 %, estimated from the 2 s samples). It is redrawn, simplified UI: an inbox with named senders (`f0010.jpg`), an order card with "Estimated total $47.80" (`f0014.jpg`), a form with "Autumn Trail 10K Entry Form" (`f0022.jpg`) and a flight card, SFO to DEN, 2h 30m (`f0030.jpg`). No cursor appears ("Yes, sign me up!" bubble, `f0021.jpg`).

The camera crops hard so the active line fills the frame. The Submit button grows to full width between 45 and 46 s (`strips/window-29-44.959s.jpg`), and a chat bubble fills the frame at 62 s (`strips/window-42-62.542s.jpg`). Legibility is partial. The email body at t=20 (`f0011.jpg`) is about 1.5 % of frame height and works as texture; the next beat restates its gist in a large bubble (`f0012.jpg`). The consent controls are large and clear: "Deny" and "Allow" (`f0015.jpg`, t=28) and "Take control of the browser" over "Stop the task" (`crops/take-control.png`, t=44).

## Motion and transitions

Cuts are rare; zooms connect the scenes. At 17.417 to 17.5 s the prompt bar "Help me stay on top of school emails" (`crops/inbox.png`) squeezes to a sliver in two frames and the inbox is there at 17.5 s (`strips/window-09-17.417s.jpg`). At 65.8 s calendar tile 19 empties and becomes the Muse card "Updated flight SFO to DEN" (`strips/window-44-65.709s.jpg`), a shared-element morph. At 76.9 s "It's your Muse" appears oversized, shrinks, and 3D objects fill in around it (`strips/window-50-76.834s.jpg`).

Five transition kinds: hard cut (8), zoom-through (2), continuous camera move (2), shared-element morph (1) and UI state change (4 label swaps). Every one is caused by something on screen. Text builds word by word: "Introducing" becomes "Muse" then "Muse is" over about 1.3 s, and the avatar pops into the gap by 5.33 s. The status chip under the avatar swaps its verb ("working", "Creating shopping list", "Waiting for permission", `f0012.jpg` to `f0015.jpg`) every 2 to 3 s. Easing curves were not measured.

## Copy on screen

All meaning is carried by text. Chat bubbles and the agent's status chip tell the story: "I found a list of school supplies that need to be ordered based on Joan's email." (`f0012.jpg`, 16 words), "Your flight is delayed 2hrs due to storms in Denver..." (`f0029.jpg`). Titles are short and parallel: "Muse is your personal AI agent" (`f0004.jpg`) and "AI that keeps you in control" (`crops/closing-title.png`) are 6 words each. I could not time most holds at native rate. The closing claim is visible at t=80 and cut to black at 81.67 s, so it holds under 3.7 s against a 2.3 s reading need, and it may be shorter. The end card holds 0.91 s with badges about 20 px wide (`strips/window-54-81.584s.jpg`).

## Sound

I did not hear the film. `audio.json` classes it as music at 115.2 bpm (beat confidence 0.502). Describe tags are music 0.713, disc_scratching 0.518, keyboard_musical 0.383, rapping 0.371, synthesizer 0.362, singing 0.331 and percussion 0.322. Whisper heard sung lines ("I got the sauce to make you go"), which fit the singing and rapping tags and are not narration. Six sections run A to F, with F covering the last 47 s (35.5 to 82.57 s). Integrated loudness is -16 LUFS, short-term maximum -14.3 LUFS, true peak -3.1 dBTP, loudness range 5.7 LU. The true peak is inside the limit; loudness sits 2 LU under -14. The cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.125 against a `chance_share` of 0.17.

## What to steal

- Without voiceover, repeat one title template between vignettes ("AI that ___ for you", six times) so the film has a chorus. Put an inline emoji on the middle line.
- Show consent controls before the trust claim, then make the claim the closing line: Allow/Deny at 28 s and "Take control of the browser" at 44 s set up "AI that keeps you in control" at 80 s.
- Narrate with a status chip: one present-tense verb phrase, changed every 2 to 3 s.
- Connect screens with push-ins and morphs so a 27.67 s shot never goes static (90 % of 2 s intervals changed).
- Keep colour for the payoff: confetti at 68 s.
- Skip the 0.91 s badge end card and the tiny email text; give the call to action at least 2 s.
