# Meet Claude Slides, Claude Design and Claude Docs (To5nrYqvR44, 94.6 s)

## Hook and structure

Frame 0 is a poster, not a blank: the strip at 0 s shows the "Now in beta" pill and "Create docs," already typing on warm cream (`strips/window-01-0s.jpg`), and the full three-line headline "Create docs, slides, and designs. Same conversation." is complete by 0.458 s. `metrics.json` frame0 records contentfulCells 0.25, so the frame is evidence. At 2 s the three product names become icon chips inside the sentence (`f0002.jpg`); by 3.67 s they collapse into the Output menu on the Claude home screen (`strips/window-03-3.209s.jpg`).

From there the film is one scripted session. The user drops a zip and types "here's the launch kit for the Varde 2.0. build the reveal deck for fri's readiness review." (`f0006.jpg`, t=10). The deck opens at t=18 (`f0009.jpg`). Slide edits run to t=30, a comment asks for social images at t=34 (`f0018.jpg`), a design canvas appears by t=44-46 (`f0023.jpg`, `f0024.jpg`), a Docs one-pager is written t=66-80, and the line "Claude makes it. You steer it." lands at t=85-89 (`f0045.jpg`), followed by the logo (`f0046.jpg`, t=90). The hero moment is the slide flipping from dark to cyan at t=28.17 (share 0.298), on the start of music section D at 27.985 s (`strips/window-20-28.084s.jpg`, `metrics.json` sections).

## Rhythm

`metrics.json` gives 18 hard cuts, 11.41 per minute, median shot 2.54 s, mean 4.98 s, and 3 shots over 10 s. The first cut is at 20.58 s and the longest shot is 20.58 s (21.7 % of runtime). `bursts` is empty, so there is no cut burst. Pace comes from the UI instead: static share is 0.13 and the longest static run is 4 s, ending at 8 s. Several detected "cuts" (24.46, 27.0, 28.17, 29.5 s) are camera pushes inside a continuous session, not scene changes (`strips/window-20-28.084s.jpg`).

## Look and type

The ground is warm cream with near-black ink and one terracotta accent used for Claude itself: the spark, the send button and the Claude cursor tag (`f0006.jpg`, `f0043.jpg`). Inside the product, the demo brand's world is near-black teal with cyan and ember accents (`f0011.jpg`, `f0026.jpg`).

Measured with `hf measure ink`: the tagline lines are 76, 83 and 64 px of a 720 px frame at t=1 (10.6, 11.5 and 8.9 %), three lines, at most three words a line. The demo slide headline measures 66 and 71 px at t=21 (9.2 and 9.9 %). The typed end line measures 46 px at t=85 (6.4 %). The longest title line is six words ("Claude makes it. You steer it."). That sits above the 4-9 % band in the tagline, and it works because nothing else shares the frame (`crops/c-title.png`).

## Product interface

About 82 % of runtime is product UI (4 s to roughly 82 s). It is a redrawn, simplified interface with a stylised cursor, not a capture: the same Claude layout carries a fictional user, "Good morning, Frankie" (`f0003.jpg`), and a fictional brand, Talvik, with a Varde 2.0 jacket. The camera pushes into the active control until it fills the frame: the share toolbar at t=32 (`f0017.jpg`), the palette at t=50 (`f0026.jpg`), the comment box at t=56 (`f0029.jpg`). Those zoomed frames read at 25-30 px glyphs. Wide frames do not: at t=18 (`f0009.jpg`) and t=44 (`f0023.jpg`) the chat text is about 7-8 px, so only the slide headlines survive phone width. The doc page shows real-looking data: a 5-bar chart "Claimed weight, waterproof shells" with Varde 2.0 at 11.2 oz in green against grey competitors (`crops/c-chart.png`, `f0040.jpg`).

## Motion and transitions

Most change is a UI state change, not a cut. Headline lines enter within 0.46 s, staggered about 0.1 s (`strips/window-01-0s.jpg`). The chips collapse out in about 0.25 s (3.67-3.92 s), against 0.46 s for the headline in (`strips/window-03-3.209s.jpg`). The recolor at 28.08-28.38 s is a 0.3 s state change under a zoom. The hard jump at 20.58 s goes from the full window to the same slide filling the frame in one frame (`strips/window-13-20.5s.jpg`), so the subject stays centred across the seam. At 81.375 s the doc zooms to the toolbar where avatars go from 7 to 8 comments, then at 82.208 s the Share button is alone and enlarged with confetti outlines in orange, blue and purple (`strips/window-58-81.292s.jpg`, `f0042.jpg`). Each seam is caused by something on screen: a click, a typed command or a finished task.

Text is typed character by character with a live cursor throughout. The ending uses two labelled cursors, Claude (orange) and You (blue), typing "Claude makes it. You steer it." in parallel between 85.17 and 86.63 s (`strips/window-60-85.167s.jpg`).

## Copy on screen

All copy is short UI-style text, quoted from frames and crops: "Create docs, slides, and designs. Same conversation." (`crops/c-title.png`); "Your deck is ready — eight slides, one job each." (`f0008.jpg`); "Rain is a given. Shells should come prepared." (`f0009.jpg`), later retyped to "Shells should act like it." (`f0015.jpg`); "@Claude lets use this slide design and mock up the social images, the typical sizes" (`f0019.jpg`); "Should the one-pager lead with the taped seams or the weight?" (`f0034.jpg`); "Claude makes it. You steer it." (`crops/c-endline.png`). The tagline's 7 words hold about 3.1 s, above the 2.6 s the reading rule needs. The 22-word Claude reply at t=40 holds about 3 s and is not meant to be read in full (`f0021.jpg`); those hold estimates come from 2 s frames and strips, not per-line measurement. The only product claim stated numerically is 11.2 oz, repeated in the chat, the doc lead and the chart (`f0036.jpg`, `f0039.jpg`).

## Sound

There is no speech: whisper returned only repeated "The" and the transcript source is `none`. `audio.json` kind is music, with describe tags music 0.781, keyboard_musical 0.509, percussion 0.448, piano 0.390, drum 0.345, synthesizer 0.339 and mallet_percussion 0.304. Tempo is reported as 115.5 bpm, but beat confidence is only 0.293, so treat the pulse as soft. Integrated loudness is -15 LUFS, short-term max -11.6 LUFS, loudness range 5.5 LU, and true peak is +0.1 dBTP, which is over the -1 ceiling. The last 3.6 s (91.01-94.63 s) are silent under the held logo. Cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.167 against `chance_share` 0.128, a 0.039 difference. Section starts do line up with two story points (27.985 s recolor, 89.905 s logo).

## What to steal

1. Make the headline the first frame and type it in, so frame 0 already carries the subject (`strips/window-01-0s.jpg`).
2. Turn the product names in the tagline into the next screen's menu (`f0002.jpg` to `f0003.jpg`), so the hook is also the transition.
3. Carry one phrase and one fixture through every surface: "Rain is a given." appears on the slide, the social boards and the doc (`f0009.jpg`, `f0024.jpg`, `f0038.jpg`).
4. Push in until the control being used fills the frame; keep wide frames short, since their text drops to 7-8 px.
5. Let a single state change be the hero: the 0.3 s recolor on a music section start, not a cut burst.
6. Show collaboration with labelled cursors, and reuse the device for the slogan (`strips/window-60-85.167s.jpg`).
7. End with a held plain line, a logo of 4 s or more, and silence under it.
