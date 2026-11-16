# Introducing Contract Intelligence (Harvey, 49.96 s)

## Hook and structure

The film opens on a ring of white dots on near-black (`f0001.jpg`, t=0): no logo, no text, no product. By t=2.0 s the ring has shrunk into Harvey's H badge and the wordmark starts to type beside it (`f0002.jpg`, `strips/window-01-1.384s.jpg`). So frame 0 is a motif poster, not the product, and the first claim about the product arrives at t=12.9 s, when a toggle is captioned "Contract Intelligence" (`f0007.jpg`).

The film has five chapters on alternating grounds. Dark, 0-12.6 s: documents fall past an Approve line (`f0003.jpg`-`f0006.jpg`). Light, 12.6-28.68 s: the toggle, then a document orbited by dots and labelled "Scoring risk" and "Drafting redlines" (`f0011.jpg`), then a column of H documents coming out signed (`f0014.jpg`). Dark, 28.68-39.6 s: a dotted sphere with five verbs and "Upgrading Intelligence." (`f0016.jpg`-`f0019.jpg`). Light, 39.6-44.6 s: "Sign faster" and "Sign smarter" beside product screens (`f0020.jpg`, `f0021.jpg`). Dark, 44.6-49.96 s: the end card. The hero moment is the toggle flip at about t=12.7 s (share 0.254), where the ground inverts in about 0.4 s (`strips/window-10-12.584s.jpg`).

## Rhythm

`metrics.json` gives 6 hard cuts, 7.21 cuts a minute, a median shot of 5.36 s and no burst. The longest shot runs 15.02 s (13.67-28.68 s, 30.1% of runtime) and three shots exceed 10 s. Cuts land at 11.8, 12.65, 13.67, 28.68, 39.6 and 44.6 s; three of them fall inside a 1.9 s span around the toggle. Pace comes from motion inside each scene, not from cutting. The longest static run is 10 s ending at 38 s (the rotating sphere with labels, which the pixel measure reads as static), and 41.7% of sampled intervals are static. This contradicts the 1.8-3.5 s cut rhythm in rule 10 for a film that still holds attention.

## Look and type

Two grounds, near-black and off-white, swap five times (`f0006.jpg`, `f0007.jpg`, `f0016.jpg`, `f0020.jpg`, `f0022.jpg`). The look block reports `bw_share` 1 and saturation 0.098, so the motion layer is monochrome; colour appears only inside the product UI at 40-44 s (blue "Needs your judgment", green "Ready for approval", `crops/ui-table.png`).

Ink measurements against the 720 px frame height: "Sign faster" 84 px, 11.7% (t=40.5 s); "Sign smarter" 80 px, 11.1% (t=42 s); end-card wordmark 80 px, 11.1% (t=46 s); "Upgrading Intelligence." 36 px, 5.0% (t=32 s); the toggle caption "Contract Intelligence" 27 px, 3.75% (t=12.9 s). Titles run from 3.75% to 11.7%, above rule 3's 4-9% band at the top, with at most two words a line. The sphere's verb labels are far smaller (about 10-12 px by eye, not ink-measured).

## Product interface

Real screens appear only from 40.2 to 44.6 s, about 9% of runtime. The panel sits in the right half and bleeds off the right edge (`f0020.jpg`), so the right-hand columns are cut. Row text is crisp at 720p ("Nova Corp · MSA", "Ready for approval", "Needs your judgment", "Uncapped liability, broad indemnity", `crops/ui-table.png`) but is about 1.5% of frame height, so it will not read at phone width. A second screen at 42 s shows "Contracts reviewed 487", "11 hours" and "92%" (`f0021.jpg`). The Approve button and falling documents earlier are redrawn, simplified illustrations. There is no cursor.

## Motion and transitions

Objects move; the frame does not. Documents fall at constant spacing past a fixed line and darken with a check as they cross (`f0004.jpg`). The funnel of pages rebuilds row by row over 2 s (`strips/window-08-9.9s.jpg`). Transitions: six hard cuts, two fade-throughs-colour (12.6 s and 44.55 s), one toggle state change. Hard cuts are 6 of 8 seams, well over rule 7's one-third. Two of the cuts switch worlds (28.68 s light to dark, `strips/window-17-28.65s.jpg`; 39.6 s dark to light, `strips/window-20-39.484s.jpg`), and each is caused by the end of a scene, not by an on-screen action. Text enters by type-on: "faster" over 40.17-40.65 s (`strips/window-21-39.95s.jpg`) and the end wordmark over 44.6-45.1 s (`strips/window-24-44.384s.jpg`).

## Copy on screen

There is no voiceover; whisper returned only a stray "The" and the caption tool found no track, so the transcript source is `none`. On-screen copy is two or three words at a time: "Approve"; "Contract Intelligence"; "Extracting", "Scoring risk", "Comparing terms", "Drafting redlines" (`f0011.jpg`); "Upgrading Intelligence."; "drafting amendments", "rewriting playbooks", "learning counterparty", "reweighing risks", "appending exclusivity" (`f0019.jpg`, `crops/labels-sphere.png`); "Sign faster"; "Sign smarter". Labels scramble on entry ("vfweighing risks", "hsafting amendments", "Eomparing terms" in `f0011.jpg`), which reads as typos at the 2 s sampling. The headline pair and the end card pass the rule 2 hold: the end card is on for 4.9 s after it finishes typing. The sphere labels hold 1.6-5.6 s, but at about 1.5% of frame height they fail the 2.6% floor.

## Sound

Music only. `audio.json` tags: music 0.887, bowed_string_instrument 0.768, violin_fiddle 0.768, orchestra 0.649, cello 0.629; keyboard 0.207 and double bass 0.198 are weak. There is no steady beat (confidence 0.099, bpm null). Sections: 0-13 s, 13-40 s, 40-49.95 s. Integrated loudness -19.1 LUFS, short-term max -16.8, true peak -5.2 dBTP, loudness range 16.8 LU, so the track misses the -14 LUFS target by 5.1 LU while staying clear of the peak ceiling. Cuts on strong onsets: 0.333 against a chance share of 0.158, a gap of 0.175, so the cuts are moderately locked to the sound on six cuts. Four 0.4 s silences fall at 41.6, 43.75, 45.75 and 47.8 s; I could not identify what causes them. Sound effects: none identified.

## What to steal

- One recurring motif (the dotted orbit at `f0001.jpg`, `f0010.jpg`, `f0018.jpg`) turns a metaphor film into one idea.
- Invert the ground between chapters, at a hard cut or a 0.4 s fade-through, instead of adding scenery.
- Put the headline pair at 11% of frame height and swap only the second word ("faster" to "smarter").
- End on a wordmark held 5.4 s with nothing else.
- Fix what this film leaves open: show the product by 12 s rather than 40.2 s, keep UI rows above 2.6% of frame height and inside the frame, and master near -14 LUFS rather than -19.1.
