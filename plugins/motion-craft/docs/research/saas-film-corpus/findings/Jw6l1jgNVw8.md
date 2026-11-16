# Run End-to-End Legal Work with Harvey Agents (Jw6l1jgNVw8)

## Hook and structure

The film runs 67.3 s and follows one task, a red-flag report for "Project Alpha's diligence review", from request to accepted edit. Frame 0 is pure white with a small serif "Harvey" wordmark (`f0001.jpg`). The first two frames are blank and the wordmark arrives at 0.1 s (`strips/window-01-0.033s.jpg`). That breaks the poster-with-subject habit. The product appears early anyway. "Harvey Agents" is on screen by 1.9 s and a prompt box types "Hey, Harvey - Help me prepare a red flag report for Project Alpha's diligence review" from 2.3 s (`strips/window-03-1.933s.jpg`, `crops/prompt.png`). A cursor clicks send at about 5 s.

The structure is a dark intro card (5.17–7.77 s), a chapter index "01 Plan … 05 Review" (7.8–12 s, `f0005.jpg`, `f0006.jpg`), then five chapters titled "Agents that plan", "Agents that research", "Agents that work async", "Agents that deliver" and "Agents that work with you". The payoff is "Delegate the Work. Own the Judgment." (60 s, `crops/closing-lines.png`), and a "Harvey Agents" wordmark holds from 62 s. I put the hero moment at t=56 s, 83% of the runtime. There the cursor clicks Accept on the "Harvey made an edit" card over the redlined memo (`f0028.jpg`).

## Rhythm

`metrics.json` reports 5 hard cuts, 4.46 cuts per minute and a median shot of 5.94 s. The longest shot runs 40.4 s (7.77–48.17 s), which is 60% of the runtime, and there are no bursts. I opened the strips for three of the cuts. They fall at 5.17 s (`window-04-5.1s.jpg`), 7.77 s (`window-06-7.7s.jpg`) and 57.7 s (`window-25-57.633s.jpg`). The 48.17 s detection is a panel slide in `window-21-47.566s.jpg`, so I read it as a UI move, not a cut. I did not open the strip for 51 s. About 60.6% of sampled intervals are static (`intervals_static_share`), and the longest static run is 12 s, ending at 20 s.

Change comes inside the long shot on a 6–8 s beat. A title swaps and a new card arrives, at 12, 22, 28, 36 and 52 s. The pace is calm and enterprise, with no energy burst. It contradicts the cut-density and burst rules, and the film still reads clearly.

## Look and type

The ground is near-white for the body (light share 0.765) with near-black bookends (dark share 0.176). Saturation is 0.042 and contrast 20. All colour lives inside the product UI. That includes the amber "Awaiting response" pill, the blue "Ready for review" pill, the navy slide with gold headings, and the magenta strike-through with lilac replacement text in the memo (`crops/redline.png`, `crops/async-table.png`).

Chapter titles are a grotesque sans, and "Harvey" and the closing lines are a high-contrast serif. "Harvey Agents" sets serif beside bold sans. Ink measurements on the 720 px frame:

| t | line | height |
|---|---|---|
| 6 s | Agents that work end-to-end | 50 px (6.9%) |
| 13 s | Agents that plan | 50 px (6.9%) |
| 40 s | Agents that deliver | 50 px (6.9%) |
| 54 s | Agents that work with you (two lines, 102 px total) | about 51 px each (7.1%) |
| 58.5 s | Delegate the Work. | 69 px (9.6%) |
| 65 s | Harvey Agents | 60 px (8.3%) |

The range is 6.9–9.7%, and no title line is longer than 5 words. Density is sparse: one title and at most one card per frame.

## Product interface

UI is on screen for about 70% of the runtime (about 3.2 s of prompt plus about 44 s from 14 s to 57.7 s). It appears as real-looking captures, shown as floating cards that bleed off the right edge. The content is specific. The Agent Plan lists "Ingest dataroom", "Extract key terms" and "Benchmark against Merger Agreement" (`f0010.jpg`). The research log names "JJD-HOV ELK GROVE v. JO-ANN STORES" and "VornadoRealtyTrust_20230915_10-K_EX-10.3_MasterLeaseAgreement.pdf" (`crops/research-log.png`). A real cursor hovers and clicks rows (`f0021.jpg`, `f0026.jpg`, `f0028.jpg`).

Legibility is partial. Title text is large. Task-table rows measure about 14 px on a 720 px frame (1.9% of height) and the research log is smaller, and nothing zooms in to help. The slide viewer and memo are readable only because they fill the right half (`f0025.jpg`, `f0027.jpg`).

## Motion and transitions

The prompt types character by character with a caret (`window-03-1.933s.jpg`). The chapter index builds left to right (`f0005.jpg`, `f0006.jpg`). Titles swap in place at centre. When UI arrives, the title slides to the left rail while a card enters from the right, as in `strips/window-08-13.6s.jpg`. The file list types "Due Diligence Memo.do" with the "cx" fading in (`f0021.jpg`). Status pills change state across `f0014.jpg`, `f0015.jpg` and `f0018.jpg`.

The only camera-like move is at 48 s. The file panel slides left and the slide viewer fades up (`window-21-47.566s.jpg`), after the cursor clicks "Q4 Board Presentation.pptx" (`f0023.jpg`). The seams are 3 verified hard cuts, about 8 title-swap UI changes and 1 slide. Ease curves were not measured.

## Copy on screen

All copy is on screen. Lines and holds:

- "Introducing Agents that work end-to-end", 5 words, 2.6 s
- The chapter index, 5 words, about 2 s
- The five chapter titles, 3–5 words, held 5.7–15 s
- "Delegate the Work.", 3 words, about 1.5 s
- "Delegate the Work. Own the Judgment.", 6 words, about 2 s
- "Harvey Agents", 5.3 s

By the reading rule a 3-word title needs about 1.4 s, so chapter titles hold far longer because they sit beside moving UI. The two-line closing statement holds about 2 s, close to the minimum.

## Sound

There is no speech, and the transcript is source `none`. The only caption track is not English. Local whisper returned the single repeated word "The", which I took as no speech.

The audio is music. The describe tags are bowed_string_instrument 0.797, violin_fiddle 0.796, cello 0.675 and orchestra 0.62, with no steady beat (confidence 0.051). Loudness is -13.9 LUFS integrated, short-term max -10.2, true peak -2.2 dBTP and LRA 9.7 LU (`metrics.sound`). Sections change at 5, 13.5, 30.5, 39.5, 45.5 and 62 s, and silence runs from 66.0 s to the end.

`cuts_on_strong_onset_share` is 0.40 against a chance share of 0.149. That is 0.25 above chance, but with 5 cuts it is only 2 hits, so I don't read it as a locked track. I can't confirm any sound effects, because no describe tag above 0.2 names one.

## What to steal

- Hold a title still on a left rail and move only the UI beside it. The title holds about 9.7 s while the question and plan cards enter.
- Preview the structure with a numbered index, then name each chapter with one parallel 3–5 word title.
- Flip the ground for bookends: dark intro and dark close around a white product body. Each flip is a hard cut after a click.
- Write the thesis as two short sentences and hold the wordmark about 5 s.
- Fix what is weak here: bring UI text to at least 2.6% of frame height, put the subject in frame 0, and add a stronger peak than the flat 6–8 s change cadence.
