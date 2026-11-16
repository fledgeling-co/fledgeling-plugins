# Harvey Mobile with Voice for iOS and Android (Bn9Vv8e_WPk, 19.08 s)

## Hook and structure

Frame 0 is an off-white ground with a pale grey "Harvey" wordmark mid-fade, left of centre (f0001.jpg); the metrics file marks it not-evidence (`frames.not_evidence_frames`). The hook is a tagline, "Legal Work, On the Move.", which assembles word by word between 1.04 s and 1.25 s and is complete by 1.25 s (strips/window-01-1s.jpg). It fades out by about 2.46 s and a phone appears at 2.5 s, the film's only hard cut (`rhythm.cut_times_s`). The structure runs: wordmark (0-1.0 s), tagline (1.0-2.4 s), phone splash and wake (2.5-4.3 s), push into the input bar (4.3-5.0 s), dictated question (5.0-10.2 s), send (10.5-11.3 s), answer (11.3-13.4 s), "Work Without Boundaries" (13.8-15.3 s), "Coming Soon" with store badges (15.4-16.9 s), "AI Tailored for Law" (17.0-19.08 s). The hero moment is the answer screen at t=12.0 s (share 0.63): the phone is about 490 px of 720 tall, with "13 Australian Privacy Principles" in bold and a numbered list (f0007.jpg, crops/phone-answer.png).

## Rhythm

One hard cut in 19.08 s: 3.14 cuts per minute, median shot 9.54 s, longest shot 16.58 s or 0.869 of runtime, no burst (`metrics.json` rhythm). Change is paced by holds instead: the input card with dictation holds 5.71 s from t=4.875 (events.json holds), the answer holds 2.29 s from t=11.125, and the closing cards hold 1.08, 1.17 and 1.83 s. This falls well outside the 1.8-3.5 s cut cadence of launch films; it works here because the typing and waveform inside the long hold are the motion (strips/window-06-10.5s.jpg shows the card growing into a phone).

## Look and type

A single flat off-white ground fills every frame (`look.luma` 246.2, `look.saturation` 0.001, `frames.light_share` 1.0). Headlines are a large high-contrast serif; the app UI is a neutral grotesque (crops/askbar.png). Measured ink heights against the 720 px frame: "Legal Work, On the Move." 64 px (8.9 %) at t=2.0; "Work Without Boundaries" 50 px (6.9 %) at t=14.5; "Coming Soon" 61 px (8.5 %) at t=16.1; "AI Tailored for Law" 51 px (7.1 %) at t=18.0. These are one-line, at most five words, sitting at the same centre. The closing "Harvey" wordmark is 25 px (3.5 %) (crops/wordmark.png). The only colour is a purple accent on the stop button and waveform dots (crops/voice.png) and the send spinner (f0006.jpg). Depth is minimal: a soft shadow and a faint ghost outline on the phone while it zooms (strips/window-04-4.334s.jpg).

## Product interface

The UI is a device mockup with a simplified redrawn app, present about 60 % of runtime (2.5 s to roughly 14 s). The input bar reads cleanly in crops/askbar.png: "Ask Harvey anything", a plus button, a wand button, and a mic icon at right. The dictation state in crops/voice.png swaps the mic for a purple square stop button and adds a dotted bar beneath that becomes a waveform of bars by t=8 s (f0005.jpg). The question types word by word with the newest word grey: "Where are" (t=6 s) then "Where are the Australian Privacy Principles set out," (t=8 s). The answer screen is crisp in crops/phone-answer.png: title "Location of the Australian Privacy Principles (APPs)", a quotation from section 14 of the Privacy Act 1988 (Cth), and items 1-9 of 13. At phone playback size the phone is only 210 px wide and body text about 1 % of frame height, so I rate legibility "partly". No cursor appears anywhere.

## Motion and transitions

Every seam except one is soft. Title to phone: the tagline fades 2.29-2.46 s over the empty ground and a grey phone fades in at 2.5 s (strips/window-02-2.25s.jpg). Splash to home: the phone screen fades black to white over 3.33-3.63 s (strips/window-03-3.209s.jpg). Push-in: from t=4.67 s the phone scales up until the input bar fills the frame at 4.96 s (strips/window-04-4.334s.jpg). Pull-back: at 10.5-11.2 s the card shrinks into a phone with a ghost outline, the same object in a new scale (strips/window-06-10.5s.jpg). Phone to title: the phone shrinks and fades 13.5-13.9 s as "Work Without Boundaries" fades up (strips/window-07-13.375s.jpg). Title entrances take about 0.25-0.34 s and exits 0.2-0.33 s, so exits are not noticeably shorter than entrances (strips/window-07, window-08). Headline words appear in sequence within about 0.2 s.

## Copy on screen

Quoted from crops and strips: "Legal Work, On the Move." (5 words, held 1.08 s); "Ask Harvey anything" (placeholder, 3 words, about 0.6 s); "Where are the Australian Privacy Principles set out, and how many are there?" (13 words, typed 5-10 s); "Work Without Boundaries" (3 words, 1.08 s, crops/title1.png); "Coming Soon" with "Download on the App Store" and "GET IT ON Google Play" badges (2 words, 1.17 s); "AI Tailored for Law" (4 words, 1.83 s, crops/title2.png). Against the reading rule (0.5 s + 0.3 s per word), the tagline needs 2.0 s and gets 1.08 s, "Work Without Boundaries" needs 1.4 s and gets 1.08 s, "Coming Soon" needs 1.1 s and gets 1.17 s, and the last line gets 1.83 s against a 2 s minimum. Every claim line is short and the viewer already knows the product by then, but the rule is not met.

## Sound

Kind: music (`sound.kind`). Describe tags: music 0.87, orchestra 0.526, bowed_string_instrument 0.46, plucked_string_instrument 0.451, keyboard_musical 0.409, mandolin 0.403. There is no steady beat (confidence 0.114, bpm null), and sections are A 0-6.5 s, B 6.5-11.5 s, C 11.5-19.07 s. Integrated loudness -13.3 LUFS, short-term max -12.5, loudness range 2.7 LU, true peak -0.1 dBTP, above the -1 dBTP ceiling. `cuts_on_strong_onset_share` is 1.0 against a chance share of 0.158, but there is one cut, so the film shows no demonstrated locking between picture and sound. Whisper heard one segment, the dictated question, over 0-10.2 s (transcript.md); no narrator exists. I did not identify sound effects.

## What to steal

- Show one real query, typed as spoken, and its answer, and let the key fact ("13 Australian Privacy Principles") reach the screen at t=12 s.
- Join scenes by scaling one object (push-in at 4.7 s, pull-back at 10.6 s) instead of cutting; one hard cut in 19 s was enough.
- Keep the ground flat and monochrome, and save the one accent colour (purple) for the live recording state.
- Close with three cards in the same place and size: benefit line, availability with store badges, brand line.
- Do not copy: the 1.08 s hold on a five-word tagline, the 210 px-wide answer phone, or the -0.1 dBTP peak.
