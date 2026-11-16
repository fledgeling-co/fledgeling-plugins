# Harvey for Innovation Teams (arDCe_F8vfk) — findings

## Hook and structure

The film is a 109 s music-only feature tour with no speech (transcript.md: source none; whisper returned only "The"). Frame 0 is a lone Harvey wordmark on near-black (f0001.jpg; metrics.json frame0 meanLuminance 0.059, contentfulCells 0.05), which breaks the poster rule. The hook comes at 1.46 s: a hard cut to white and "You've built the knowledge." (f0002.jpg, strips/window-01-1.377s.jpg). A black knowledge graph follows (f0003.jpg, f0005.jpg), then a pale "Now" at 6.96 s (f0004.jpg, window-04-6.34s.jpg). Four task titles light paths through the graph, from "Draft a Client Alert" at 10.05 s to "Build Case Strategy for Litigation" at 16.4 s (f0006-f0008, window-12-16.392s.jpg). The hero moment is the 16.81 s hard cut from the dark graph to the light product world, 15% into the runtime. Five chapter titles then run on blank ground, each followed by one UI scene: "Manage Templates Across Teams" (f0020), "Deploy Your Playbooks" (f0026), "Curate Firm Knowledge" (f0034), "Control Access and Usage" (f0039), "Track Usage and Adoption" (f0045). "Lead your firm's transformation." (f0050.jpg) leads to the wordmark again at 98.97 s (f0051.jpg) and a black, silent tail (f0054, f0055).

## Rhythm

metrics.json gives 7 hard cuts, 3.85 per minute, a median shot of 5.8 s and three shots over 10 s. The longest runs 43.96 s (16.81-60.77 s, 40.3% of runtime). There are no bursts. All seven cuts fall at 1.46, 3.42, 6.96, 8.76, 16.81, 60.77 and 98.97 s, so after 16.81 s the pacing is internal: camera push and pull, cursor moves, typing and fades. About 30% of sampled intervals are static (intervals_static_share 0.296; longest static run 8 s ending at 52 s), and f0024 and f0025 are visually identical. This film contradicts the 1.8-3.5 s cut rule, and it does so on purpose: a long take that keeps changing inside the frame.

## Look and type

Dark brand beats (near-black, 20% of sampled frames) bracket a long off-white UI middle (light_share 0.8; look.json saturation 0.019). Teal appears only in the graph nodes (f0005.jpg) and the analytics charts (f0046.jpg, crops/usage-table.png). Titles are a high-contrast serif, centred, and ink-measured at 58-70 px on a 720 px frame: 9.7% at 2 s, 9.3% at 40 s, 9.2% at 50 s and 67 s, 9.3% at 89 s, 8.1% at 98 s. That sits at or slightly above the 4-9% band. Single-line titles run to 4 words ("Track Usage and Adoption"), and two-line titles stay at 2-3 words a line (f0007, f0021). Titles build word by word with the later words greyer (f0007 "Calls", f0009 "Your Workspace"); no word carries an accent colour. The density is sparse, and the only depth is dimmed nodes behind the title in f0006.

## Product interface

Roughly 70% of runtime is real-looking product UI (my estimate from f0010-f0049: about 20-98 s, f0011-f0049). It shows Workflows, Vault, Playbooks, Roles, Users and Analytics on the fictional Whitford Lane workspace. A black arrow cursor, typed text and drag ghosts do the demonstrating: "Ask user to upload a pater" completes to "patent application" between f0014 and f0015, and a folder (f0036) and a PDF (f0027) are dragged with a green plus. Camera work is crop-in, pull-back, then isolate: a corner of the sidebar at 20 s (f0011), the full window at 22 s (f0012), a single control at 82 s (f0042). Legibility is partial. Whole-window frames (f0012, f0027, f0043) carry UI text about 7-9 px tall, which will not read at phone width, while the isolated cards read cleanly (crops/card-fileupload.png, crops/users-table.png, crops/playbook-form.png).

## Motion and transitions

Strips show a 0.38 s word-by-word hook (window-01-1.377s.jpg) and a title built in about 0.3 s over a lit graph path (window-07-10.052s.jpg). The title then holds still while the graph underneath changes (window-12-16.392s.jpg), which confirms the landed-title rule. Transition counts from my reading: 7 hard cuts, about 8 camera pushes and pulls, about 10 UI state changes caused by a click or typing, and 13 word-by-word title builds; these are my counts, not metrics.json. The hard cut at 60.77 s is only two frames and low-change (cuts.json change 15.2), a soft step into the playbook form (window-41-60.519s.jpg). The graph-to-UI cut at 16.81 s is fully visible (change 246). The final scene fades table rows in one by one (window-60-94.512s.jpg, f0048.jpg). Eases look like smooth settles with no overshoot, a judgement from strips that I did not measure numerically.

## Copy on screen

Thirteen lines carry all the copy: "You've built the knowledge." / "Now" / "Draft a Client Alert" / "Summarize Interview Calls" / "Conduct Post-Merger Compliance Review" / "Build Case Strategy for Litigation" / "Design Your Workspace" / "Manage Templates Across Teams" / "Deploy Your Playbooks" / "Curate Firm Knowledge" / "Control Access and Usage" / "Track Usage and Adoption" / "Lead your firm's transformation." Titles never exceed 4 words a line. The hook holds about 1.6 s (1.84-3.42 s), against 1.7 s from the 0.5 s plus 0.3 s a word rule. "Manage Templates Across Teams" shows at both 38 s and 40 s, so it holds 2 s or more. The closing line is on screen at 98 s (f0050.jpg) and replaced at 98.97 s; its start was not sampled, so its hold is unmeasured. There is no URL or call-to-action button anywhere (f0050-f0055).

## Sound

Music only. audio.json kind is music, with describe tags music 0.775, keyboard_musical 0.442, synthesizer 0.375, percussion 0.33, singing_bowl 0.329 and mallet_percussion 0.205. Tempo reads 120.2 BPM but beat confidence is 0.158, so I would not build on it. Loudness meets the social master: integrated -13.9 LUFS, true peak -4.5 dBTP, loudness range 6.2 LU. The cuts are not locked to the sound: cuts_on_strong_onset_share 0.143 against chance_share 0.088 is a 0.055 margin. Sections run A 0-17 s, B 17-47 s, C 47-100 s, D 100-109 s, and the A to B boundary (16.995 s) lands within 0.19 s of the hero cut at 16.81 s. Silence covers 0-0.23 s and 106.1-109.0 s. I cannot hear the film and list no sound effects.

## What to steal

1. Pair a short verb-led title on blank ground with a single UI scene for that feature; repeat five times (f0020, f0026, f0034, f0040, f0045).
2. Show the whole app window briefly, then crop to one card or control at 2x or more before the viewer has to read (f0012 then f0042).
3. Prove the interface with a real cursor, typed text and drag ghosts rather than captions (f0014-f0015, f0036).
4. Build titles word by word and then leave them still (window-01, window-07, window-12).
5. Bookend a long light middle with the same dark wordmark frame at 0 s and 99 s (f0001, f0051), and fade to 2-3 s of silence.
6. Fix the weak spots: add a legibility-safe crop for every whole-window shot, and put a URL or button on the closing card.
