# Visualize Legal Data on Demand in Harvey (mTzRvY38xGw)

Silent, music-only 31.56 s film. It shows one feature: Harvey turns a typed request into an interactive HTML artifact. Transcript source is none: the transcript tool was unavailable and local whisper returned only "Music" tags.

## Hook and structure

Frame 0 is already the subject: a zoomed prompt box on light grey reading "Ask Harvey anything", with a caret, Files and Sources (f0001.jpg, crops/askharvey.png). The first hard cut comes at 1.93 s (`first_cut_s`), so the opening is a 1.9 s push-in on the input field. From 1.93 s the same prompt is re-typed at poster scale: a giant "C" with a caret at t=2 (f0002.jpg), then "Create a" at t=4 (f0003.jpg).

The film then runs the same sequence three times. Round 1 (4.9-15 s): the prompt scrolls left to "...tive litigation timeline" (f0004.jpg), the cursor presses the black send arrow at t=8 (f0005.jpg), the answer reads "I've created an interactive timeline of all 32 key events in Project Southfield." (f0006.jpg), and a file chip appears. The camera pulls out at about 14.4 s to the full app (f0007.jpg). Round 2 (15-20.5 s): the prompt box types "Create a structure", the chip "harborview-tidewater-structure-chart.html" opens a Corporate Structure Chart (f0009.jpg, f0010.jpg). Round 3 (20.5-26 s): "Create a compliance |" (f0011.jpg), chip "meridian-compliance-dashboard.html" clicked at 22.5 s (f0012.jpg), then the dashboard (f0013.jpg). 

I take the hero as the dashboard at t=24 s, 76% of runtime, and did not measure whether it is the strongest musical point. Then "Create" beside cycling chips such as relationship_map (f0014.jpg, strips/window-21-28.433s.jpg) and a "Harvey" wordmark held from 28.7 s to the end (f0015.jpg, f0016.jpg; `longest_hold_s` 2.83).

## Rhythm

`metrics.json` gives 9 hard cuts, 17.11 cuts per minute and a median shot of 0.37 s. Those numbers describe two things. One is a burst of 8 cuts between 1.93 s and 4.83 s, about 0.35 s apart, with one cut per typed letter (strips/window-02-1.866s.jpg, strips/window-03-3.4s.jpg). The other is a single shot from 9.03 s to the end, 22.53 s or 71.4% of runtime (`longest_shot`). The burst sits at `mid_share` 0.107, not at 30-60% of the film, and it works because every cut shows a new letter. Between 9 s and 31 s the film stays in one continuous take and uses zooms and UI changes as pacing. 20% of sampled intervals are static (`intervals_static_share` 0.2), the longest 4 s ending at 22 s, when the cursor drifts to the dashboard chip (strips/window-18-22s.jpg).

## Look and type

The ground is white throughout, apart from the grey opening (f0001.jpg). `look.json` reports luma 245, saturation 0.004 and `light_share` 1.0. The only colour sits inside the product: green, amber and red status cells and a blue "Pre-Merger" tab (crops/heatmap.png, crops/merger.png). Type is a neo-grotesque sans; the wordmark is a serif (f0015.jpg).

Title lines measured with `measure ink` on a 720 px frame: "Create a compliance dashb" 76 px (10.6%) at t=21; "Create" 93 px (12.9%) at t=26; "Harvey" 60 px (8.3%) at t=29. Range 8.3-12.9%, above the 4-9% title rule; the prompt text is deliberately oversized, the logo is inside the band. The giant "C" at t=2 is about 480 px tall by eye on f0002.jpg (about 67%), not tool-measured. Title lines are at most 4 words.

## Product interface

Product UI is on screen for about 91% of the runtime, everything except the 2.8 s wordmark. It is a real-looking screen capture with a real cursor (f0005.jpg, f0012.jpg). The artifacts carry specific content: KPI cards "14 / 23% of rated", "23 / 37% of rated", "25 / 40% of rated" and a heat map with columns Licensing, Rate Caps, Disclosures, Data Privacy, Consumer Prot., AML/KYC, Recordkeeping (crops/kpis.png, crops/heatmap.png). The timeline lists dated events such as "License & Distribution Agreement Executed" (crops/timeline.png).

Phone-width legibility is partial. File chips and prompts are large; the full-app shot at 14.4 s (f0007.jpg) and heat-map cells at 24 s (f0013.jpg) are small. The timeline text also shows smeared overlapping glyphs while rows animate (crops/timeline.png).

## Motion and transitions

Text enters by typing with a caret, both in the real box (f0011.jpg) and at poster scale (f0003.jpg). In the 15.0-16.0 s strip the prompt types "Create a structure" letter by letter (strips/window-11-14.433s.jpg). Transitions are caused by something on screen: hard cuts reveal letters (9), the send click leads to the answer (strips/window-08-8.9s.jpg), and continuous zooms connect the app view and the prompt box (strips/window-11-14.433s.jpg). File chips show a light shimmer sweep (f0006.jpg, f0012.jpg). At 28.4-28.7 s chip names swap (litigation_dashboard, witness_network) before a hard cut to the wordmark (strips/window-21-28.433s.jpg). I did not measure easing curves.

## Copy on screen

All copy is product text. Lines, with measured or estimated holds: "Ask Harvey anything" (1.9 s), "Create a" (about 1.5 s), the 13-word answer "I've created an interactive timeline of all 32 key events in Project Southfield." (about 1.5 s, short of a 4.4 s reading rule, though it is also visible during the 9-10.5 s scroll), "Create a compliance dashboard" (about 1.1 s), file names, the dashboard title (about 2 s) and "Harvey" (2.8 s, above the 2 s last-line rule). No headline copy states a benefit; the prompt wording does that work. The film never names the problem in a caption. `transcript.md` is empty of speech.

## Sound

The audio is music: `audio.json` kind music, confidence 0.9; describe tags music 0.689, percussion 0.355, tabla 0.311, drum 0.282, mallet_percussion 0.235 (marimba_xylophone 0.197, below the 0.2 line). Tempo 136.3 BPM with beat confidence 0.506, so treat the tempo as approximate. Two sections: A 0-14.635 s and B 14.635-31.554 s. Loudness: -12.3 LUFS integrated, short-term max -10, loudness range 4.0 LU, true peak +0.7 dBTP, with 894 clipping events starting at 0.533 s. That misses the -14 LUFS / -1 dBTP social master. 

Cuts are partly locked to the sound: `cuts_on_strong_onset_share` 0.222 against `chance_share` 0.061, a gap of 0.161, above the 0.10 line. The B section starts at 14.635 s, matching the zoom-out/zoom-in at 14.4-15.0 s (strips/window-11-14.433s.jpg). There is a 0.44 s silence from 31.11 s (`silence_spans`). No voiceover or separable effects can be identified from the evidence.

## What to steal

1. Type the prompt big. At t=2 the first letter fills about two thirds of the frame, so the request reads without narration (f0002.jpg).
2. Give each cut a cause: 8 cuts in 2.9 s, one per letter, with 22% landing on strong onsets.
3. After the burst, switch to one continuous take (22.5 s here) so zooms carry the film.
4. Repeat one grammar (prompt, chip, artifact) three times so rounds 2 and 3 are quick to read.
5. Show real output text and numbers (14 / 23 / 25, the heat-map labels) rather than blocks of grey.
6. End on a lone wordmark for 2.8 s followed by 0.44 s of silence.

Avoid: tiny wide shots (f0007.jpg), a dashboard held only about 2 s, no call to action, and a master peaking at +0.7 dBTP.
