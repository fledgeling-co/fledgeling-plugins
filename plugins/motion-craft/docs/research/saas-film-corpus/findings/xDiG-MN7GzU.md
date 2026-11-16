# Memory Is Now In Harvey (xDiG-MN7GzU), findings

## Hook and structure

The film has no speech. The caption track is missing and local whisper returned only "." segments, so `transcript.md` records source none and all meaning is on screen. Frame 0 is not blank: `f0001.jpg` shows the card "When you send me a contract, how do you want the review back?" centred on paper, 553 of 1280 px wide (43%). The hook is a question the product answers. At 2.9 s the card grows into four options and "Type something else..." (`f0003.jpg`). By 8 s the cursor has picked "Short summary the business can read" and a chip splits away (`f0005.jpg`).

The structure runs: question (0-11 s), orbit with Maya, Commercial Counsel (11-18 s), the hard cut to "Introducing / Harvey Memory" (18.04 s), real UI proof (21-44 s), "Applied everywhere you work" (44-52 s), four persona orbits (52-60.5 s), and a four-line sign-off (60.54-67.78 s). I picked t=38 s as the hero moment: the memo's "Executive Summary" heading is highlighted beside the chip "My GC prefers numbered lists" (`f0019.jpg`). There is no URL or button at the end (`f0034.jpg`).

## Rhythm

`metrics.json` gives 4 hard cuts (18.04, 18.21, 21, 60.54 s), 3.54 cuts per minute, a median shot of 7.24 s, a mean of 13.56 s and no bursts. The longest shot runs 21 s to 60.54 s, 39.54 s or 58% of runtime. This contradicts the 1.8-3.5 s cut rule, yet the film does not drag, because something on screen changes every 1-2 s inside the shot. The menu opens (2.9 s), slides off (10.7-11.7 s, `strips/window-05-10.709s.jpg`), rings arrive (12.9 s), the planet appears (13.67 s), memory text types out (24-25 s, `strips/window-12-24s.jpg`), chips stack in (38-44 s) and personas swap (54, 56, 58, 59.29 s). `frames.intervals_static_share` is 0.364, so a third of sample intervals hold still, mostly the closing type.

## Look and type

One ground throughout: off-white paper with soft grey painted blocks that move between scenes (`look.json` luma 238.7, `frames.light_share` 1.0, saturation 0.006). Cards are white with soft shadows. The only dark masses are the shaded planets (`f0007.jpg`, `f0028.jpg`). The only colour is teal, on the memory icon and the memo highlights (`f0020.jpg`). Colour therefore means "memory".

Titles are serif. I measured ink height on the video's 720 px frame: "Harvey Memory" 59 px at t=20 (8.2%), "Your Preferences." 42 px at t=61 (5.8%), "Your Work." 42 px at t=62 (5.8%) and "Harvey" 50 px at t=66 (6.9%). All sit within the 4-9% band. The longest title line is "Applied everywhere you work", 4 words (`f0024.jpg`). Density is sparse; large areas stay empty, but each frame has one clear subject.

## Product interface

Real Harvey UI is on screen from 21 to about 44 s (`f0011.jpg` to `f0020.jpg`). It shows the sidebar, a user message, "Finished in 4 steps", a "Memories saved" card, a memo with a Progress list, and a Context panel with Memory, Sources and Output tabs. The Properties list shows "Model: Claude Fable 5". Counting the floating chips and orbits that borrow the UI's cards, interface-derived content covers roughly 85% of runtime.

The cursor is a real arrow (`f0004.jpg`, `f0015.jpg`). Camera on the UI is a punch-in to the chat (`f0013.jpg`), a pull-out (`f0015.jpg`), then a pan to the memo (`f0018.jpg`). Legibility at phone width is partial. Memo and panel text is about 9 px on 720 p (`crops/ctx.png`, `crops/concl.png`). The chips beside the memo are about 21 px (`f0019.jpg`) and carry the facts: "My GC prefers numbered lists", "Prioritize EDGAR as the primary source over web or other sources", "Color code issues by priority".

## Motion and transitions

Four hard cuts, all with a scene change underneath: 18.04 s to the title, 18.21 s within the title build, 21 s into the product window (`strips/window-10-20.917s.jpg`, a white window that fills in over about 0.5 s) and 60.54 s into the sign-off (`strips/window-29-59.917s.jpg`). Everything else is caused by something on screen. The menu leaves after the cursor picks an option (`strips/window-05-10.709s.jpg`). Rings and the planet arrive as the view pulls back (`strips/window-06-12.875s.jpg`). Planet, name and chips swap together on the same orbit when Rob becomes Priya at 59.29 s (`strips/window-28-58.375s.jpg`). "Introducing" appears first and "Harvey Memory" about 0.33 s later (`strips/window-09-17.417s.jpg`). The chip icons change from the memory glyph to Outlook (48 s) and Word (50 s) (`f0025.jpg`, `f0026.jpg`). No cross-dissolves between worlds appear in the strips I opened.

## Copy on screen

The copy is short and written as the user's own words. Verbatim from crops and full frames: "When you send me a contract, how do you want the review back?" (`crops/q.png`); "Precise "commitment" vs. "contribution"" (`crops/orbit.png`); "No "we believe" in filings", "Short paragraphs, no footnotes in memos" (`f0028.jpg`). Role lines: "Commercial Counsel", "Senior Associate, Litigation", "Deputy General Counsel", "Partner, Private Equity".

Persona chips are held 1.4-2 s each and some are truncated ("Refer US state privacy to Ba...", `f0029.jpg`), so those fall below the 0.5 s + 0.3 s per word rule. Titles hold well above it: the 4-word "Applied everywhere you work" shows across `f0024.jpg` to `f0026.jpg`, about 6 s. I did not open the strips for the final four lines, so their hold times are -1 in the JSON. The sign-off reads "Your Preferences." then "Your Work." then "Your Harvey." then "Harvey" (`f0031.jpg` to `f0034.jpg`).

## Sound

Music only. `audio.json` kind is music, with describe tags bowed_string_instrument 0.797, cello 0.721, violin_fiddle 0.715 and orchestra 0.568, so I describe it as bowed-string orchestral. wind_instrument is 0.394 and double_bass 0.33, both too weak to name. There is no steady beat (confidence 0.099) and no silence span. Integrated loudness is -16 LUFS, short-term maximum -11.8, true peak -2.4 dBTP and loudness range 5.8 LU. That is 2 LU quieter than the -14 LUFS target; the peak is within the limit. Sections are A 0-5.5 s, B 5.5-14 s, C 14-58 s and D 58-67.8 s. Strong onsets arrive 6.2 times a minute. `cuts_on_strong_onset_share` is 0.25 against `chance_share` 0.023, a margin of 0.227, so the cuts are locked to the music. I found no evidence of sound effects and claim none.

## What to steal

1. Open on the question the product answers, in a single card already on screen at frame 0 (`f0001.jpg`).
2. Let the cursor make the choice and let the choice stay as the next scene's object (`strips/window-05-10.709s.jpg`).
3. One orbit template, many people: swap planet, name, role and three chips every 1.4-2 s (`strips/window-28-58.375s.jpg`). Give each chip a longer hold than this film did.
4. When real UI text is too small, echo its fact in a 20 px chip and highlight the matching spot (`f0019.jpg`, `f0020.jpg`).
5. Hold one long shot of real UI (39.5 s here) and keep something on screen changing every 1-2 s.
6. End on lines that change one word at a time and finish on the brand alone, then add the missing call to action (`f0034.jpg` has none).
7. Use one accent colour for one meaning; here teal means memory.

What I could not check: closing-line hold times, the sound by ear, a phone-size render, and the font identity.
