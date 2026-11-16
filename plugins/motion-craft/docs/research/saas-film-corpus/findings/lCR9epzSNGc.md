# Claude Opus 5.5 builds daydreams that hold together (lCR9epzSNGc)

## Hook and structure

Frame 0 is the finished product in its app: the Canal Clock Square model centred in a floating window on sage green, with the library list at left and a red Download button (`f0001.jpg`). The film has no voice, headline or caption. At about 1.9 s it switches to a bare cream stage where an orange frame scans the model (`strips/window-01-1.75s.jpg`). The film then runs in four movements. From 2 to 26 s it is a cutaway proof that the model is sound: size at 5 s, joint counts at 6 to 10 s, a weak-joint test at 12 s, a parts tree at 16 s, and a stat row at 22 s. From 26 to 60 s it is one screen recording, where the Alpine Chalet builds from an empty baseplate and a prompt, "Create a medieval castle", is typed. A longer request follows for a watch tower, drawbridge and moat. The hero moment is the swap to the revised castle at t=60.77 s (share 0.705), with the moat and a blue-spire watchtower (`strips/window-40-60.734s.jpg`). The manual and library follow at 69 to 82 s. The film ends on the Claude mark at 83.9 s, with the wordmark typed on by 84.3 s (`strips/window-56-83.9s.jpg`).

## Rhythm

`metrics.json` gives 12 hard cuts, 8.34 cuts a minute, a median shot of 4.3 s, and no burst. The pace is two-speed. Shots of 1 to 6 s run to 26.7 s (cuts at 5.58, 11.62, 15.0, 19.3, 25.67). Then one continuous shot runs 34.08 s, 39.5% of the runtime. A cluster of cuts sits at 60.8 to 77.6 s: 60.77, 63.65, 64.78, 68.9, 74.6, 77.62. The first shot of 5.58 s is longer than the 1.8 to 3.5 s launch norm, and the film still never reads as slow because counters tick inside each shot (`strips/window-03-5.067s.jpg` shows the counter from 6,894 to 17,452 within 1.2 s).

## Look and type

There are two grounds: sage green around a floating app card, and a warm cream gradient with a vignette for the cutaways. Palette saturation is low (`look.saturation` 0.067) and the models supply all the colour. Orange is the one accent, used for the scan frame, the joint wireframe, the weak-joint ring (`crops/weakjoint.png`), Send and Download, progress bars, and the underline at 21 s. Numerals are heavy grotesque with small tracked uppercase labels. Measured ink heights are 37 px at 5 s (5.1% of the 720 px frame), 44 px at 8 s (6.1%) and 50 px at 21 s (6.9%, clipped by the region, so an upper bound). The longest line is 3 words, apart from the stat row. The frame is sparse: a corner counter on one side, the subject on the other (`f0005.jpg` to `f0007.jpg`).

## Product interface

The interface appears as real UI capture for about 68% of runtime (0 to 1.9 s and 25.7 to 82 s). The cutaways are illustrations drawn from the same models. The cursor is real and visible (`f0016.jpg`, `f0018.jpg`). Whole-window shots show chat, tab and button text at roughly 7 to 10 px, which is not legible at phone width. The film fixes this by pushing into the input box: the typed prompt reads at about 20 px (`crops/chatcopy.png` is the idle state; `f0019.jpg` and `f0027.jpg` show the typing). Claude's reply card reads "Updated to a 2,057-piece Stone Castle with 11 sub-builds" with "Checked: buildable, 4 warnings" (`crops/claudereply.png`). A fixed note at bottom right reads "Some sections of demo are accelerated" (`crops/disclaimer.png`) and stays through the film.

## Motion and transitions

Counters tick up and new rows stack under them. Chat text types with a caret. The model assembles piece by piece with a step counter and a progress bar. The orbit view spins. Transitions are mostly hard cuts (about 10) and each follows a completed step: the explode finishing at 5.58 s, and the same silhouette cutting to the app at 25.67 s (`strips/window-16-25.634s.jpg`). Two camera moves are continuous: a blur push into the chat box at 34.4 to 36 s (`strips/window-22-34.417s.jpg`) and a blurred pull back before 60 s (`f0029.jpg`). The one dissolve, at about 82 s, goes from the app to a plain ground before the logo (`f0042.jpg`). That is a dissolve from the UI to a blank ground, not between two worlds. The spinner ("Planning the shape... 1 min 21 s", `f0030.jpg`) is left on screen, which makes the wait part of the story.

## Copy on screen

There is no headline. Verbatim lines read from crops: "38.4 × 38.4 × 50.9 cm" with "48 × 48" and "159" (`crops/dims.png`); "WEAK JOINT" (`crops/weakjoint.png`); "What should we build?" with six suggestion chips (`crops/chatcopy.png`); "Create a medieval castle" (`f0021.jpg`); and the user's long request ending "where the drawbridge goes over the moat?" (`f0028.jpg` to `f0032.jpg`). The stat captions are 1 to 3 words and hold 1.3 to 3.7 s, within the 0.5 s + 0.3 s a word rule. The 33-word prompt would need 10.4 s under that rule and is on screen for about 8 s of typing (t=46 to 54 s), so the end of the request is read as it is typed. The closing frame has the wordmark alone, held about 2.1 s, with no call to action and no URL (`f0043.jpg`).

## Sound

The film is music only. The captions contain [music] tags and a single ">> Ah!" at 00:22, with no speech (`transcript.md`). `audio.json` tags are keyboard_musical 0.611, synthesizer 0.529, plucked_string_instrument 0.399, guitar 0.395 and piano 0.392. Tempo is 83.1 bpm with beat confidence 0.361, so the beat grid is weak evidence. Sections change at 10.5, 21.7, 42.7 and 67.3 s. Integrated loudness is -19.8 LUFS, short-term peak -16.1 LUFS, true peak -3.6 dBTP, loudness range 5.6 LU. That is 5.8 LU quieter than a -14 LUFS social master. `cuts_on_strong_onset_share` is 0.167 against a chance share of 0.084, a gap of 0.083, under 0.10. The cuts are not locked to the sound, and the 60.8 s swap sits inside section D rather than on a section boundary.

## What to steal

- Show verification as a before and after on one tiny object, then repeat the counters at full scale: one flagged joint (`f0007.jpg`), then ticks and six models at 0 (`f0008.jpg`), then 0 errors and 0 warnings (`f0012.jpg`).
- Put numbers at 5 to 7% of frame height in one corner with icon and tracked label, and the subject on the other side. Hold each for at least 1.3 s.
- Push 2x into the input box before typing, because whole-window UI text is too small at phone width.
- Leave the real wait on screen (spinner, 47 s and 1 min 21 s), then swap the result in a single frame.
- Show a short disclosure caption when the demo is sped up.
- End on a typed-on wordmark with a 2 s hold.
- Avoid: a 34 s continuous recording without a cut, quiet audio at -19.8 LUFS, and music that does not meet the cuts.
