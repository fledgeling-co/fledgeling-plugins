# wzrBFx0ONZg — Harvey, "Create Tailored Legal Agents with Agent Builder" (40.2 s)

## Hook and structure

The film opens on the "Harvey" wordmark, centred on an off-white ground (f0001.jpg). Strip window-01-0.36s.jpg shows the ground blank until t=0.40 s and the wordmark by 0.44 s, so I could not settle whether t=0 itself is blank or the poster. The name arrives fast: "Workflow Builder" with "Workflow" struck through at t=2 s (f0002.jpg), then "Agent Builder" by t=4 s (f0003.jpg).

The rest is one feature per beat: off-the-shelf cards (t=7–10), "Or Create Your Own" (10–14), a scheduled run (14–19), a notification (19–22), a result table (22–25), deploy in chat (25–30), human-in-the-loop control (30–34.5), a quality line (34.6–36.9) and a black tagline card (36.9–40.2). The hero moment is the dark "Your Harvey Workflow Agent has finished" banner at t=20 s, share 0.497 (f0011.jpg). The film has no speech: local whisper returned only "Music" for every segment, so the transcript source is `none`.

## Rhythm

metrics.json gives 2 hard cuts (19.12 s and 36.88 s), 2.98 cuts per minute, median shot 17.76 s, and no bursts. That breaks the cut-every-1.8–3.5 s habit of launch films, and the film still does not feel idle, because content changes inside each shot: 23 change events and a median hold of 1.36 s. A new headline or UI state arrives about every 3–4 s. The cost is stillness: intervals_static_share is 0.421 and the longest static run is 6 s, ending at 6 s.

## Look and type

The ground is off-white (frame-0 luminance 0.978). From t=7 to t=34 it splits into a left text half and a right half in warm grey or white (f0005.jpg, f0014.jpg). Saturation is 0.015 and the black-and-white share is 0.94, so there is no colour accent. The only hue lives in small icons inside the UI (crops/modal.png, crops/agent-chat.png). One high-contrast serif carries every headline. The film ends on near-black (f0019.jpg, f0020.jpg).

I measured seven title lines with `hf measure ink` on the 720 px frame: Harvey 55 px (7.6 %), Agent Builder 59 px (8.2 %), "Scale Work With" 38 px (5.3 %), "Off The Shelf Agents" 49 px (6.8 %), the Deploy headline 48 px (6.7 %), the Build Agents headline 48 px (6.7 %) and "AI Tailored for Law" 51 px (7.1 %). The range is 5.3–8.2 %, with at most five words on a line, so it sits inside the 4–9 % title rule. Accent is tonal, not a single word: the second line begins pale grey and darkens to black (f0004.jpg, strips/window-20-34.16s.jpg).

## Product interface

UI is on screen for roughly 66 % of runtime (about 26 s of 40 s, counted from the sheets). It is redrawn and simplified: template cards (crops/cards.png), a stack of "File upload" step cards (crops/modal.png), a "Scheduled run" form (f0009.jpg), a result table (crops/table.png) and an agent chat (crops/agent-chat.png). A real-looking cursor clicks "Create New Agent" (f0006.jpg), the cadence field (f0009.jpg) and the agent chip (f0014.jpg). The camera never moves on the UI.

Legibility is mixed. Card titles and the notification banner read clearly (crops/cards.png, crops/notification.png). The table and chat text is about 10 px tall at native size, judged from the 2× crops rather than measured, and would not read at phone width. The UI panels are also small: the schedule panel is about 360 px wide on a 1280 px frame, well under the 40 % hero fill, which the title text partly compensates for.

## Motion and transitions

Headlines fade in as a line. Two-line titles show line 1 in black and line 2 pale, then line 2 darkens (f0004.jpg and the second line in strips/window-05-6.56s.jpg). The end card builds word by word at 36.88, 36.92, 37.04 and 37.20 s (strips/window-21-36.8s.jpg). The left title holds still while the right side changes (strips/window-07-9.52s.jpg, strips/window-15-25.4s.jpg), which matches the landed-title rule.

Transitions I counted: 2 hard cuts, 1 panel wipe when the grey half slides in at about 8.2 s (strips/window-05-6.56s.jpg), about 6 cursor-driven UI state changes, and 1 dissolve from banner to table at 21.76 s on the same white ground (strips/window-13-20.84s.jpg). That is four types. Both hard cuts follow a beat that ends on its own (a held panel, a held headline), so neither is arbitrary. I did not measure easing curves; strips show soft ease-out with no overshoot.

## Copy on screen

Thirteen text lines, all quoted from frames and crops: "Workflow Builder", "Agent Builder", "Your Workflows, Now Agents" (strip only, about 0.5 s), "Scale Work With / Off The Shelf Agents", "Or Create Your Own", "Keep Work Running in the Background", "And Get Notified When Work Product is Done", the banner "Your Harvey Workflow Agent has finished / Check out the results, and let me know if there's anything you'd like me to change.", "Deploy the Right Agent, Exactly When You Need It", "Stay in Control When it Matters Most", "Build Agents that Deliver Quality, Without Sacrificing Speed" and "AI Tailored for Law".

Holds are read from 2 s samples and strips, so each is good to about 0.5 s. "And Get Notified When Work Product is Done" is nine words and holds about 2.1 s, short of the 3.2 s the reading rule asks. The last line holds about 3.3 s and passes the 2 s minimum. The film shows the product's behaviour and does not name a problem in a caption.

## Sound

I could not hear the film. audio.json classes it as music, with describe tags music 0.924, percussion 0.67, synthesizer 0.585, keyboard 0.559, gong 0.508, singing_bowl 0.364, drum 0.293 and cymbal 0.235. Tempo is about 97.8 bpm at beat confidence 0.4, which is low. Sections run A 0–22.4 s, B 22.4–34.5 s, C 34.5–40.2 s. Integrated loudness is −13.9 LUFS, short-term max −11.3 LUFS and loudness range 6.4 LU; true peak is −0.9 dBTP, 0.1 dB over a −1 dBTP ceiling.

The cuts are not locked to the sound: cuts_on_strong_onset_share is 0.0 against a chance share of 0.28. There is no voiceover. Sound-effect content cannot be established from the evidence.

## What to steal

1. Pair every headline with one UI action that proves it, and hold the headline still while the UI changes (f0006.jpg, f0009.jpg, f0014.jpg).
2. Show a rename or reframing by striking the old word through, as at t=2 s (f0002.jpg), instead of explaining it.
3. Stage a two-line headline in two reads: line 1 black, line 2 pale grey darkening to black (f0004.jpg). This is a second-line accent in place of one accent word.
4. Break a run of split-screen beats with one full-frame element at mid-runtime; here the banner at t=20 s, share 0.497 (f0011.jpg).
5. End on a hard cut to a black card, build the tagline word by word at roughly 0.12–0.16 s a word and hold about 3 s (strips/window-21-36.8s.jpg).
6. Do not copy the small proof text: crop or zoom any UI line the viewer must read to at least 2.6 % of frame height; crops/table.png shows what fails.
7. Calm films can skip bursts: this one has none and lets 2 hard cuts and 23 in-shot changes carry it (metrics.json).
