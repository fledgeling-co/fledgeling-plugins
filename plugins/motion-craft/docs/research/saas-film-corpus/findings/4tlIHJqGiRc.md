# Introducing Memory (Harvey, 80.7 s)

## Hook and structure
The film has no speech and no caption track (`transcript.md`, source none), so everything is carried by picture, text and music. Frame 0 is a lone white serif H on near-black: `strips/window-01-0.367s.jpg` shows black until 0.4 s, then the H, and `metrics.json` frames.frame0 marks it not evidence (97.5% blank cells). The product subject does not arrive until 2.2 s, when a grey card with concentric rectangles slides in over the H (`strips/window-02-2.2s.jpg`). It cuts to the full card on white at 2.97 s and flips apart into six MEMORY tiles at about 4.1 s (`strips/window-03-3.984s.jpg`). Three claims follow, each on a black card with a white UI scene after it: Harvey Learns From Your Actions (7.48 s), And Uses its Memory to Improve its Answers (39.57 s), You Reason / Harvey Remembers (72 s). The hero moment is t=52 s (share 0.644), where the Memory Used chip appears while phrases in Searching Memory highlight in the same teal and rose as the stored cells (`f0027.jpg`). The film ends on the tiles, the line Never Start From Scratch Again. and a small H, held about 3.8 s (`f0039.jpg`, `f0040.jpg`).

## Rhythm
`metrics.json` reports 7 hard cuts, 5.2 cuts a minute, a median shot of 3.52 s but a mean of 10.09 s, and no burst. The longest shot runs 42.1 to 75.27 s, 33.17 s or 41% of runtime. It does not feel static because something changes about every 2 s (median_hold_s 2.15, 41 change events): prompts type, highlights grow, cells tint, chips appear. The static share of sampled intervals is still 0.667, and the longest static run is 30 s ending at 72 s, so the pacing rests on small changes. Cuts fall only at claim cards and the end: 7.48, 9.38, 39.57, 42.1 and 75.27 s.

## Look and type
Light ground in 92.5% of sampled frames (dark_share 0.075), black only for claim cards. Saturation is 0.016 and warmth 0.4, so the colour comes from three pastel highlights: teal, dusty rose and lilac (`f0016.jpg`, `f0026.jpg`, `f0028.jpg`). Titles are a high-contrast serif in Title Case; prompts are a grotesque. Ink measurements on 720 px: Harvey Learns From Your Actions 41 px (5.7%) at 8 s; And Uses its Memory... 43 px (6.0%) at 40 s; You Reason 62 px (8.6%) and Harvey Remembers 77 px (10.7%, descender included) at 74 s; the tagline 32 px (4.4%) at 78 s; MEMORY tile letters 34 px (4.7%) at 6 s. The 8-word card is one line, wider than the 6-word-a-line rule. In `crops/title-reason.png` the second line is grey, the only type accent. The space is sparse and flat; only the card and tile flips show 3D tilt.

## Product interface
UI is on screen from 9.4 to 39.5 s and 42.1 to 72 s, about 74% of runtime. It is a redrawn, simplified Ask Harvey composer plus a 6x6 grid of memory cells, not a capture. No cursor is drawn, only a text caret (`f0007.jpg`). Prompt text at t=52 is 16 to 18 px ink on 720 (2.2 to 2.5%), under the 2.6% floor, and the chips are about 14 px, so legibility at phone width is partial. The colour match between highlighted phrases and cells (`crops/composer.png`) carries the meaning when the type is small. Prompts are specific: Acme, a Delaware C-corp, 2019-2021, 3x cap.

## Motion and transitions
Seams are mostly hard cuts on a black/white flip, with two match cuts at 2.23 and 2.97 s, two card-to-tiles flips (4.1 s and 76.6 s, about 0.3 s each, `strips/window-32-76.417s.jpg`), and a slide of the prompt left as the grid fades in at 14.9 s (`strips/window-08-14.934s.jpg`). Claim cards fade in word by word: `strips/window-05-7.45s.jpg` shows Harvey at 7.5 s and the full line by about 7.9 s. The 6 other strips read (`window-06`, `-17`, `-18`, `-28`, `-31`) show cuts landing as clean frame swaps with no dissolve. Easing curves were not fitted.

## Copy on screen
Verbatim lines from crops: "Harvey Learns From Your Actions"; "Draft a letter requesting an extension on the due diligence review period. Keep it concise and direct."; "Memory Stored"; "And Uses its Memory to Improve its Answers"; "Searching Memory"; "User prefers concise and direct language"; "Acme is a Delaware C-Corp and you are representing the buyer"; "Memory Used"; "You Reason"; "Harvey Remembers"; "Never Start From Scratch Again." Holds estimated from strips: the first claim about 1.5 s against 2.0 s by the reading rule, the second about 2.5 s against 2.9 s, the tagline 3.9 s against a 2 s minimum. Both claim cards run a little short; the tagline does not.

## Sound
Music only. `audio.json` kind is music; describe tags are synthesizer 0.652, keyboard_musical 0.644, percussion 0.405, piano 0.321 and electric_piano 0.277. There is no steady beat (confidence 0.103). Sections change at 11, 33, 40, 57.5 and 72.5 s. Integrated loudness is -14.1 LUFS, short-term max -10.7, true peak -1.0 dBTP, LRA 4.0 LU: on the social master target. Silence covers 0 to 0.395 s and 78.9 to 80.7 s. `cuts_on_strong_onset_share` is 0.0 against a chance share of 0.125, so the cuts are not locked to the sound. I could not hear the film; no sound effects were identified.

## What to steal
- Tint a phrase and the matching cell in a diagram with the same colour, so stored information is visible without extra copy (`f0027.jpg`).
- Cut between worlds by flipping polarity on a hard cut, not a dissolve; four times in 81 s.
- Prove a feature by running one layout three times with new inputs (t=44, 54, 62).
- Open and close on the same flip, and hold the tagline 3.9 s.
- Do not copy: the black silent first 0.4 s, a lone logo as frame 0, or 16 px proof text.
