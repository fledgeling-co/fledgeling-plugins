# Introducing Claude Meetings (YUYeHMsqbmY, 62.56 s)

## Hook and structure

The film opens on a real-looking video call, not a title. In `strips/window-01-0s.jpg` frame 0 holds one webcam tile and a call toolbar on black, and the grid fills to six faces by 2 s (`f0002.jpg`). The subject is on screen from the first frame, but the product name does not appear until t=9.42 s (`f0006.jpg`), 15% into the runtime. The first 9 s are greetings: the caption track reads "What's up, everybody?", "Hey, good morning" and "Hi, Claude" (`transcript.md`, source auto-captions, 22 words in total).

The story runs in four moves. A spoken request ("Hey Claude, can you start a whiteboard please?", `f0007.jpg`) starts the whiteboard at 17.08 s. A card at 25.83 s says "So the work starts before the meeting ends" and a second request asks Claude to sort. The board resolves into three columns at about 34.5 s (`f0018.jpg`), which I take as the hero moment (share 0.552). A chat thread (39.21-47.38 s) settles on "Huckleberry it is!", and a notes document with a Gantt plan appears at 47.38 s (`f0025.jpg`). The ending is a typed tagline and the wordmark, with no call to action.

## Rhythm

`metrics.json` gives 12 hard cuts, 11.51 cuts a minute and a median shot of 2.71 s, but the mean is 4.81 s and the film has four shots of 7.7 s or longer (17.08-25.83, 31.54-39.21, 39.21-47.38, and 47.38-62.56 at 15.19 s, 24% of runtime). Early cuts come at 7.46, 9.42, 12.75, 14.79 and 17.08 s, a 2-3 s pulse; after that the pace drops. `bursts` is empty, so there is no 5-8 cut burst. Energy comes from inside the shots: median hold 0.83 s and 66 "change" events. Between 20 s and 24 s the board goes from 6 stickies to about 15 with five name-tagged cursors moving (`f0011.jpg` to `f0013.jpg`).

## Look and type

Two grounds alternate: near-black for the call and chat, warm cream with a faint grid for the whiteboard, cards and ending. 61% of sampled frames are light (`dark_share` 0.387). Coral is reserved for Claude: the blob (`f0008.jpg`), the star (`f0030.jpg`), the name tag and the word "Claude" in the "Hey Claude," bubble (`crops/title-meetings.png`). Titles use a high-contrast serif; UI and stickies use a plain sans.

Ink measurements on the 720 px frame: "Claude Meetings" 69 px (9.58%, t=10.5), "and builds alongside you" 49 px (6.81%, t=19), "before the meeting ends" 47 px (6.53%, t=27), "Work at the speed of thought" 68 px (9.44%, t=55). The two largest include descenders, which pushes them just over a 9% cap. Longest title line is 6 words. Layouts are medium density and flat, with soft shadows on cards and a coral glow behind the plan card at 48 s (`f0024.jpg`).

## Product interface

The interface is on screen for about 85% of the runtime, all redrawn and simplified: call tiles with real people, a whiteboard with pastel stickies, a chat panel, a document and a Gantt chart. It is invented, but it is one story. Geegolly Good Pies, Huckleberry, Teo, June and Vinny recur from the board (`f0011.jpg`) to the chat (`crops/chat-link.png`) to the plan (`f0025.jpg`, "Huckleberry Hootenanny Launch Plan", owners and dates such as Nov 16 and Nov 20). Cursors are labelled with names. Claude's own presence is a tile whose status text narrates the work: "Taking notes...", "Starting whiteboard", "Organizing ideas" (`f0008.jpg`, `f0009.jpg`, `f0015.jpg`).

Legibility at phone width is partial. Chat text is large (`crops/chat-link.png`), but the call-widget buttons (`crops/call-widget.png`), sticky text and Gantt row labels (`crops/gantt-head.png`) are about 14 px on a 720 px frame, an estimate from the crops rather than an hf measurement, and under 2.6% of the short side.

## Motion and transitions

All 11 seams after the first are hard cuts, and no cross-dissolves appear in `measure/cuts.json`. Each cut follows something on screen: a request card, a status tile or a change of world (call to cream card at 9.42 s, board to card at 25.83 s, card to dark tile at 29.54 s). Inside shots the interface moves: the board pans sideways at 34-38 s (`f0019.jpg`, `f0020.jpg`), the chat scrolls at 39-47 s and the plan card scales up between 48 s and 50 s (`f0024.jpg` to `f0025.jpg`). Two shape morphs exist: the blob becomes a doodle (`f0008.jpg` to `f0009.jpg`), and the star grows into the wordmark between 59.33 s and 59.75 s (`strips/window-49-59.334s.jpg`). Text enters word by word, grey to ink; the nine-word command at 27.79 s completes in about 0.4 s (`strips/window-25-27.792s.jpg`). Exit durations and ease curves were not measured.

## Copy on screen

Copy is short and sentence-case. Cards hold 2-8 s: "Claude Meetings" about 3.3 s, "Claude joins your call and builds alongside you" about 8 s, "So the work starts before the meeting ends" 3.7 s. All clear the 0.5 s + 0.3 s a word rule except the sort command, which is complete for 1.37 s (28.17 to 29.54 s) against 3.2 s required. It is a spoken line mirrored on screen rather than a headline. The tagline "Sync at the speed of thought" becomes "Sort" then "Work" under Claude's cursor tag (`f0027.jpg`, `f0028.jpg`, `strips/window-45-55.334s.jpg`). The wordmark holds 2.8 s, above the 2 s floor. The problem is never named; it is shown as a team that has to organise ideas after the call.

## Sound

Music runs underneath (describe tag music 0.856), with keyboard_musical 0.782, piano 0.661, synthesizer 0.634, electric_piano 0.48, mallet_percussion 0.357 and glockenspiel 0.351 in `audio.json`; bpm 130.1 at beat confidence 0.54. The caption track has speech only in the first 11 s, plus [snorts] at 6 s and 14 s. Loudness: integrated -15.4 LUFS, short-term max -13.6, true peak -1.4 dBTP, range 6.5 LU. The true peak meets the -1 dBTP ceiling; integrated loudness sits 1.4 LU under -14, with a silent tail from 60.01 s to the end. Cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.083 against `chance_share` 0.22. Sections change at 14.3, 27.7, 33.7, 40.6 and 53.5 s; I did not compare them with picture changes. I cannot hear sound effects.

## What to steal

1. Give every assistant action the same three beats: a typed request card, a status tile of about 2 s that names the work, then the result (9.42, 12.75 and 14.79 s; 25.83, 29.54 and 31.54 s).
2. Let long shots (8-15 s) carry the demo when something on screen changes every second or so; the film's median hold is 0.83 s.
3. Use one invented story with named people, dates and a brand across at least four surfaces, so invented UI reads as real work.
4. Reserve one accent colour for the product (coral for Claude) and keep everything else neutral or pastel.
5. Close on a tagline that is itself a demo: a labelled cursor retypes one word (Sync, Sort, Work), then a wordmark held 2.8 s.
6. Fix before copying: keep UI text above 2.6% of frame height, name the product before 9 s, and check integrated loudness when the logo tail is silent (-15.4 LUFS here).
