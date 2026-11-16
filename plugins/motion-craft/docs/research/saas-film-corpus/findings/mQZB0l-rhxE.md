# Building verification loops in Claude Code (mQZB0l-rhxE)

A 187.5 s tutorial: a presenter on camera, cut with typographic cards, a loop diagram and real app recordings. Captions are human-written (`transcript.md`).

## Hook and structure

Frame 0 is the presenter at a desk with a lower-third reading "Delba de Oliveira" over "Claude Code" (`f0001.jpg`, `crops/lowerthird.png`). `frame0.isEvidence` is true and the subject is present, so it passes the poster rule. She speaks the first line, "For every prompt you send, Claude Code runs a loop", and at t=2.58 a dissolve brings in a cream card with a single "Prompt" box (`strips/window-02-1.417s.jpg`, `f0002.jpg`). The loop diagram completes by t=8 (`f0004.jpg`).

The order is: loop (0-8 s), the problem of manual checking (8-34 s), a "Manual QA" table (37-50 s), a mobile proof (56-61 s), the verify skill demo (61-113 s), the Like-button demo (113-156 s), then two summary cards and the presenter closing (156-187 s). The proof moment I chose is t=142 (share 0.757), where the chat reads "CLS went from 0.19 to 0.00". The end has no CTA text, URL or logo (`f0094.jpg`).

## Rhythm

`metrics.json` gives 27 hard cuts, 8.64 cuts a minute, median shot 4.81 s, and no burst (`bursts` is empty). The longest shot is 42.5 s, from 113.21 to 155.71 (22.7 % of runtime). `intervals_static_share` is 0.495 and the longest static run is 10 s ending at 48 s, which is the Manual QA table assembling. The voice sets the pace: cards change when a sentence ends, slower than the 1.8-3.5 s launch range.

## Look and type

Graphics sit on a cream ground (`f0013.jpg`) or a tan one (`f0056.jpg`). Screen recordings sit as a window on a mid-blue ground (`f0034.jpg`). The diagram uses sage green, pale blue and a grey-beige box (`crops/diagram.png`). The terracotta accent appears only inside the product UI: the "ACME COFFEE" label and the "Liked 13" pill (`crops/simulator.png`, `f0067.jpg`).

Titles are a high-contrast serif, left-aligned at an indented margin; list rows are a grotesque sans in two columns (`crops/manualqa.png`). Measured with `hf measure ink` against 720 px: "Verifying a change" at t=24 is 39 px (5.4 %), "Manual QA" at t=40 is 36 px (5.0 %), "The verification loop" at t=110 is 65 px (9.0 %), "What to codify next" at t=166.5 is 38 px (5.3 %). That range, 5.0-9.0 %, sits inside the 4-9 % rule. "When Claude can verify its own work" (`f0080.jpg`) is seven words on one line, one over the six-word limit; its height was not measured because the ink region clipped.

## Product interface

Screen recordings run from 11 s to 17 s, 56-61 s, 63.5-75.6 s, 88.9-94.3 s, 97.6-104.8 s and 113.2-155.7 s, about 42 % of runtime. All are real captures with a real cursor (`f0007.jpg`, `f0070.jpg`) and a native iOS Simulator panel (`f0029.jpg`). The chat text is small. At 1280x720 body lines are about 17 px, and code lines are smaller (`crops/skillmd.png`), so only bold lines such as "Done." and the $4.50 / $9.00 totals would read at phone width. The voice carries the rest.

The strongest proof is a visible fail then pass: quantity 1 and $4.50 at 56 s (`f0029.jpg`); at 58 s the quantity is 2 but the total still reads $4.50 (`sheet-02.jpg`); then "Two flat whites now total $9.00. The order screen passes." (`f0031.jpg`). In the long shot, old lines fade to grey as new lines arrive (`f0067.jpg`, `f0070.jpg`) and a cursor sits near the result text (`f0073.jpg`, `f0076.jpg`).

## Motion and transitions

The detector counts 27 hard cuts, but the strips show most are short dissolves or fades. Presenter to card is a one- or two-frame blend: `strips/window-02-1.417s.jpg` shows a half-transparent frame at 2.625 s between the presenter at 2.583 s and the card at 2.75 s. Presenter to browser at 11.08 s is the same (`strips/window-07-10.834s.jpg`). Card to card fades text out word by word left to right over about 0.35 s, then the tan ground changes to cream and the next title blurs in (`strips/window-14-20.5s.jpg`). Card to app window is a blurred window that sharpens over about 0.15 s (`strips/window-33-63s.jpg`). Inside the windows, change is UI state: the slash menu opening as "/" is typed (`strips/window-33-63s.jpg`) and the diagram adding "Verify results" (`strips/window-03-5.709s.jpg`).

I count roughly five kinds of seam (dissolve, fade-through-colour, UI state, hard cut, blur-to-sharp), inside the 3-5 range. The presenter shot is locked off (`strips/window-26-53.292s.jpg`) and cards and UI have no camera moves. Cuts are caused by sentence ends rather than by an on-screen event.

## Copy on screen

Card copy is short and mirrors the voice: "Hand off your manual checks" (t=19.5-21), "Verifying a change", "Manual QA" with rows "Web app / Open the page, click around, watch the console", "Back end / Call an endpoint, read the response", "Mobile app / Tap through the screens in a simulator" (`f0025.jpg`), "Codify your checks", "The verification loop", "When Claude can verify its own work" with "It gets further on its own", "The result is better", "It takes fewer rounds of back and forth" (`f0082.jpg`), and "What to codify next" with "A performance budget", "An accessibility checklist", "Your design system's rules".

Holds follow the voice, so they are long: the table holds 12 s, the three-item list rows 5-11 s each. The last list line, "Your design system's rules", is on screen for about 1.8 s before the cut at 182.29, under the 2 s floor for the last line. The problem is shown as the manual table and the browser at 11 s, not named in a caption. The second half of the first row is grey until its words are spoken (`f0020.jpg`).

## Sound

The film is voice only. `audio.json` kind is voice; the describe tags are speech 0.916, writing 0.155, click 0.113, music 0.105. Nothing above 0.2 except speech, so I do not claim music or sound effects, and `bpm` is null with no steady beat. Integrated loudness is -23.9 LUFS, short-term max -21.2, true peak -4.6 dBTP and loudness range 3.5 LU, so the master is about 10 LU under the -14 LUFS social target. `cuts_on_strong_onset_share` is 0.111 against a chance share of 0.077, a gap of 0.034, below 0.10, so the cuts are not locked to the sound; they fall in speech pauses (silence spans such as 2.71-3.41 s near the cut at 2.58 s).

## What to steal

- Build a list card one row per spoken item and leave earlier rows on screen (39, 42 and 45 s in the Manual QA card).
- Show verification as a fail then pass state in real UI with one changed number ($4.50 to $9.00; CLS 0.19 to 0.00).
- Put the speaker and a lower-third on frame 0 and reach the first graphic by 2.6 s.
- Fade card text out word by word left to right in about 0.35 s.
- Keep the long demo as one uncut 42.5 s shot with old lines greyed and a cursor pointing at the answer.
- Fix what it misses: master to -14 LUFS, titles of six words or fewer, last line held 2 s or more, larger chat text.
