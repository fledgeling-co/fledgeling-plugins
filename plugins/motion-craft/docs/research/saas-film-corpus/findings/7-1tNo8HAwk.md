# New agents for legal professionals | Claude Cowork (7-1tNo8HAwk)

## Hook and structure

The film opens on its thesis. At t=0 `f0001.jpg` shows "Claude works where lawyers work" in dark serif, centred on a flat cream ground, and `strips/window-01-0s.jpg` shows it unchanged across the first 0.25 s. The hook is a claim and not a logo or a blank. The 25.24 s runtime splits into six beats: headline one (0-2.4 s), headline two (2.4-5.8 s), a partner-logo carousel (5.8-14 s), headline three "With 12 plugins tailored to different practices" (14-15.5 s), a wheel of 12 practice chips (15.5-21.1 s), and the Claude wordmark (21.1-25.24 s). The hero moment is the carousel at t=12 s (share 0.475), `f0007.jpg`, about 14 tiles in a wavy row. The ending is a still asterisk-and-wordmark hold of about 3.4 s (`f0012.jpg`, `f0013.jpg`) with no call to action.

## Rhythm

`metrics.json` reports `hard_cuts` 0, `cuts_per_min` 0.0 and `median_shot_s` 25.24: the film is one continuous shot, with no cut and no burst. Change arrives as a new composition every 4-7 s, at about t=3.5, 5.8, 14, 15.5 and 21.1 s. 41.7 % of the sampled 2 s intervals are static (`intervals_static_share` 0.417) and the longest static run is 6 s, ending at 24 s. This contradicts the 1.8-3.5 s cut cadence in rule 10 for this film. Pacing comes from word-staggered motion inside each composition, not from seams.

## Look and type

The ground is a flat warm cream with no gradient (`look.json` luma 224.3, saturation 0.058, `light_share` 1.0). Ink is near-black, and coral appears only in the dot and asterisk from t=20 s (`f0011.jpg`, `f0012.jpg`). Partner brand colours in the tiles are the only other colour. Headlines are a tight serif at 54-56 px of a 720 px frame: 7.8 % at t=1 s, 7.5 % at t=4 s, 7.5 % at t=14.3 s (`$HF measure ink`); the wordmark is 78 px, 10.8 % at t=22.5 s. All three headlines are one line. Lengths are 5, 5 and 7 words, so the third exceeds six words a line. No accent word is used. Chips use a grotesque sans, large and legible in `crops/chips.png`. Density is sparse: one subject per frame, with the headline or the logo row filling roughly 65-85 % of the frame width (`f0001.jpg`, `f0005.jpg`).

## Product interface

No Claude interface appears in any of the 13 frames. The integrations claim is carried by partner marks on white or brand-coloured rounded tiles: docusign, Thomson Reuters, box, FREE LAW PROJECT, netdocuments and Consilio are legible in `crops/icons-left.png`, `crops/icons-right.png` and `f0005.jpg`, `f0007.jpg`. The 12 chips, from "AI governance legal" to "Regulatory legal", are simplified UI cards (`f0010.jpg`, `crops/chips.png`). Together the tiles and chips are on screen about 55 % of the runtime (5.8-14 s plus 15.5-21.1 s). There is no cursor and no camera on a screen. The chips read at phone width; the marks inside the tiles are about 100 px tiles on a 1280 px frame and several carry only small wordmarks, so legibility is partial.

## Motion and transitions

The frame is locked; objects move through it. Text builds word by word, each word fading from grey to ink in 0.04-0.08 s steps (`strips/window-05-14.042s.jpg`, `strips/window-02-2.375s.jpg`). At 2.4-3.5 s the first headline fades out in order while the second builds, with no cut between them. The Docusign tile at t=6.96 s pushes the headline off left (`strips/window-03-5.834s.jpg`). The tile row then bobs in a staggered wave moving left to right from 9.8 s (`strips/window-04-9.792s.jpg`) and streams out left by 14.4 s. At 15.5-21 s the headline drifts up while chips scroll up through a blurred focus band, the centre chip white and sharp (`strips/window-06-15.459s.jpg`). At 21.1-21.8 s a coral dot grows into the asterisk and the wordmark types in, letter by letter in about 0.25 s (`strips/window-07-21.417s.jpg`). Transition kinds: slide, word-fade state change, camera-style drift, morph. Every move is caused by the previous object leaving. Easing curves were not measured.

## Copy on screen

On-screen copy is 17 headline words, 26 chip words and the wordmark, 44 in all. Verbatim from `crops/title1.png` and the frames: "Claude works where lawyers work" (5 words, holds about 2.4 s), "Connected across your legal stack" (5 words, about 2.3 s), "With 12 plugins tailored to different practices" (7 words, about 1.1 s at full opacity). The reading rule needs 2.0 s for five words, so the first two pass; seven words need 2.6 s and the third gets about 1.1 s, a miss. The last line holds 3.4 s, above the 2 s floor. The count claim "12 plugins" is followed by exactly 12 chips, so the number can be checked on screen (`strips/window-06-15.459s.jpg`).

## Sound

There is no speech: whisper returned a lone "I", recorded as `none`. `audio.json` classes it as music, about 89.9 BPM with beat confidence 0.423. Describe tags: music 0.858, keyboard_musical 0.594, piano 0.48, synthesizer 0.477, percussion 0.471, mallet_percussion 0.422, marimba_xylophone 0.349, electric_piano 0.345. Two sections: A 0-5.4 s and B 5.4-25.2 s, so the change lands near the handoff to the logos at 5.8 s. Loudness is -17.1 LUFS integrated, short-term max -15.5, true peak -4.3 dBTP, loudness range 6.4 LU. This is 3 LU under the -14 LUFS master rule. Audio goes silent from 23.19 s, so the last 2.0 s of the logo hold has no music. With no cuts, the cut-to-sound share is not measurable and the picture is not locked to the sound. No sfx tag was found.

## What to steal

- Put the full claim on frame 0 (`f0001.jpg`) and hold it still for about 2.4 s.
- Use the word-by-word build as the film's one repeated text device, and change composition every 4-7 s when you use no cuts.
- Prove a number with that many objects: 12 plugins, 12 chips.
- Carry an integrations claim with real partner marks on uniform rounded tiles, and make the hero moment a dense moving field of them (t=12 s).
- Hold the third headline at least 2.6 s if it runs seven words; this film gave it about 1.1 s.
- Keep music under the final logo hold; this film leaves 2.0 s of silence.
- Show at least one real product frame; this film shows none.
