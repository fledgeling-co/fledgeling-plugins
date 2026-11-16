# Introducing Command Center (Harvey, 78.7 s)

Sampled frames sit roughly 1 s off their nominal times (f0002 is black at 2 s, but the strips show the title until 2.9 s), so exact timings below come from strips and `metrics.json`; frame-based times are approximate.

## Hook and structure

Frame 0 is a finished poster: "Command Center" in heavy sans, centred on a pale grey ground, with four dashboard cards floating around it (`f0001.jpg`). The title blurs in and is sharp by 0.23 s, and the cards arrive by 0.77 s (`strips/window-01-0s.jpg`). The poster dims through black from about 2.7 s to 3.03 s (`strips/window-02-2.466s.jpg`), so the first cut at 2.97 s (`metrics.json` `first_cut_s`) is a fade, not a hard edge.

The film is a single demo session. From about 4 s the cursor presses Explore analytics (`f0003.jpg`). The panel opens, and a question is typed: "What use cases is my team using Harvey for?" (`f0006.jpg`, `f0007.jpg`). The reply lands with numbers: "Document Review and Due Diligence (23.1% of queries)" and "roughly 42,610 queries" (`f0010.jpg`). A second prompt asks for a presentation, and the deck renders in a side pane (`f0025.jpg`, about 48 s, 61% of runtime), which is the hero moment. The film then returns to the dashboard, clicks Enable on Web search and gets a success modal (`f0036.jpg`). It closes on a white card reading "AI Tailored for Law" over "Harvey" (`f0039.jpg`).

## Rhythm

There are 6 hard cuts, 4.57 per minute, median shot 4.17 s (`metrics.json` `rhythm`). That number misleads. The longest shot runs 36.5 s, from 29.13 to 65.63 s, which is 46.4% of runtime, and the five cuts after it fall in the last 13 s. There is no burst of cuts (`bursts` is empty). Change comes from typing, hovering, panels opening and camera push-ins. 22 holds over 1 s have a median of 1.44 s (`events`). The film is continuous rather than montage.

## Look and type

The window is off-white and sits on a dark olive painted texture (`f0004.jpg`). Saturation is 0.099 and 92% of pixels are near black-and-white (`look`). Green appears only in percentage deltas, the success check and the generated slide's dark green ground (`f0025.jpg`, `crops/my-modal.png`). Two typefaces: a heavy grotesque for the opener (`crops/my-title-open.png`) and a light serif for headings, big figures and the tagline (`crops/my-title-end.png`).

Measured line heights against 720 px frame height:

- "Command Center" 62 px, 8.6%, at 1.5 s.
- "AI Tailored for Law" 52 px, 7.2%, at 77.5 s.
- "Harvey" 41 px, 5.7%.
- "New releases" 29 px, 4.0%, at 70 s.
- "Whitford Lane's Command Center" 15 px, 2.1%, at 33 s.

The largest title is inside rule 3's 4-9% band and the dashboard headings sit below it. The title never exceeds four words.

## Product interface

The UI is on screen from 3.0 to 74.6 s plus the floating cards at the start, about 94% of runtime. It is a real-looking capture with a standard cursor and pointing-hand cursor (`f0003.jpg`, `f0034.jpg`). At full-window framing the sidebar and chart labels are about 8 px at 720p and would not survive a phone (`f0004.jpg`, `f0011.jpg`). The film fixes this by zooming in on every line that matters: the typed prompt (`crops/my-panel-head.png`, `f0006.jpg`), the chart tooltip (`f0013.jpg`), the Enable rows (`crops/my-releases-rows.png`, `f0034.jpg`) and the modal. The assistant's reply carries real figures ("287 active M&A users, 56,826 queries", `crops/my-chat-reply.png`), and the generated deck shows charts and totals (`f0027.jpg`, `f0028.jpg`).

## Motion and transitions

Seams read from strips:

- Fade through black at 2.7-3.03 s, and fade to white at 74.2-74.63 s (`strips/window-34-74.1s.jpg`): two world changes, about 0.6 s each.
- Camera push-ins and pull-backs on the single shot: zoom to the composer at 9.8-10.8 s (`strips/window-05-9.8s.jpg`), zoom on the line chart from 29.2 s (`strips/window-13-28.8s.jpg`), and a push on Enable at 65.9-66.8 s (`strips/window-29-65.2s.jpg`).
- UI state changes, each caused by a click: Enable gives a grey dim and a spinner modal at 68.1 s (`strips/window-30-67.633s.jpg`).
- One true hard cut: the dimmed modal vanishes between 73.533 and 73.567 s (`strips/window-33-73.5s.jpg`).

Camera moves ease over about 1 s (`strips/window-03-3s.jpg`, 4.0-4.6 s). The landed title does not move after 0.77 s.

## Copy on screen

All copy is interface text plus two cards. The prompts type character by character with a caret (`f0006.jpg`, `f0018.jpg`, `f0019.jpg`, `f0020.jpg`). The long reply at 18 s is not meant to be read in full. The shortest lines are the ones the film wants read: "Explore analytics" (`f0003.jpg`), "Web search succesfully enabled" (misspelled in the film, `crops/my-modal.png`) and "AI Tailored for Law". The tagline has 4 words, so rule 2 asks for 1.7 s and it holds about 2.7 s (`f0039.jpg`, end card from 74.6 s). There is no caption naming the problem; the dashboard and the typed question show it. There is no CTA button or URL; the last card is a tagline and a wordmark.

## Sound

No speech: whisper returned only "Music" for the whole film (`transcript.md`). `audio.json` classes it as music (confidence 0.81). Describe tags: bowed_string_instrument 0.514, keyboard_musical 0.507, orchestra 0.482, cello 0.446, violin_fiddle 0.397, piano 0.301. I take that as a string-and-piano score, and I could not hear it. There is no steady beat (confidence 0.01) and no sign of sound effects: 11 weak onsets, the strongest at t=0.015 s.

Integrated loudness is -11.2 LUFS, short-term max -9, loudness range 4.5 LU, true peak +0.2 dB with 17 clipped samples from 38.1 s (`metrics.json` `sound`). That is about 3 LU over the -14 LUFS social target and 1.2 dB over the -1 dBTP ceiling, so rule 9 is not met. The cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.0 against `chance_share` 0.003. Six sections (A 0-20 s through F 53.5-78.7 s) give a flat arc.

## What to steal

- Open on a poster with the title among the product's own cards; it satisfies rule 1 from frame 0 (`f0001.jpg`).
- Zoom the capture to the line being read, and pull back to the whole window only for orientation. A 62 px title at 8.6% and 15 px interface headings share one film (`f0004.jpg` against `f0006.jpg`).
- Show the AI's output as an artefact beside the chat, with a grey skeleton first (`f0024.jpg`, `f0025.jpg`). This is a new idea relative to the binding rules.
- Fade through black or white at the two seams where the film changes world, and let clicks cause every in-product change (rule 7).
- End on a plain card with a 4-word tagline at about 7% of frame height, held about 4 s.
- Do not copy: the 36.5 s single shot contradicts rule 10's cut cadence, and it works only because every 5-10 s there is a push-in or a typed line. Do not copy the loudness either; the film ends up clipped (+0.2 dBTP).
