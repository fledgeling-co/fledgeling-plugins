# SkpwzfR4A1E: Claude's new mobile app updates are here

## Hook and structure
The film opens on a presenter already speaking, in a warm window-lit room, with a foldable-phone card showing a "4,406" chart at right (f0001.jpg, t=0). The card slides in at 0.57s and a cream panel grows from it to fill the frame at 2.8-3.0s (strips/window-03-2.666s.jpg). The Duo then unfolds in 3D between 3.4s and 4.4s, which is the hero moment (t=3.7s, share 0.024). The first hard cut is at 2.97s (metrics rhythm.first_cut_s).

The rest is a platform tour that follows the voiceover: an index card "Upgrades across the Claude apps" (t=6s), accounts (11.6s), photos (22.8s), Duo and iPad artifacts (29.8-69.9s), Android laptop mode (69.9s), voice (83s), CarPlay (98.7s), languages (109.8s), search "Coming soon" (127s), a Command-K tip (138s), a comment request (144s) and the logo (147.2s). The unshipped search is held back for last, so the shipped upgrades come first.

## Rhythm
There are 16 hard cuts in 152s, 6.31 a minute, with a median shot of 8.2s and a longest shot of 25.6s (44.2-69.9s, 16.9% of runtime). There is no burst (rhythm.bursts is empty). This is slower than the 1.8-3.5s launch-film range, and it works because change comes from overlays: events.counts shows 30 appear events and 135 changes. The longest static run is 10s (frames.longest_static_run_s) and 29% of sampled intervals are static.

## Look and type
Cream cards (luma 182, warmth 11.4 in measure/look.json) sit over blurred golden-hour footage; voice and CarPlay move to a charcoal ground (f0044.jpg, f0050.jpg). Terracotta is the only accent: the dot before each label, the starburst, the underline under "most requested" (f0010.jpg), and the large "24" (f0058.jpg). One yellow bar marks the data point in the chart.

Titles are a high-contrast serif in two lines, three words a line at most. In crops/w-title-upgrades.png the label "Claude apps" sits over the title "Upgrades across / the Claude apps". The ink measure gives line heights of 58px (8.1% of 720) at t=9s, 62px (8.6%) at t=24s, and 41px (5.7%) for side-card titles at t=16s, 78s and 90s. The numeral "24" is 127px (17.6%) at t=118s. Titles stay inside the 4-9% range; the numeral goes far above it. Density is sparse.

## Product interface
Product UI is on screen for roughly 85% of the runtime (my estimate from the sheets). Every screen is a designed, simplified rendering with sample data: Q3 orders, a summer-reading poster, a Kyoto itinerary, ceramics-studio chats. None looks like a screen capture. They appear inside device mockups (Duo, iPad, laptop, phone, CarPlay screen) or on floating cards.

The best demo is the chart edit: at t=36s a request, "Drop week 12. Trade show.", is typed (f0019.jpg), and by t=42s the chart reads 3,886 with a dashed ghost bar (f0022.jpg). Legibility is partial. Full-frame cards read at phone width; the chart rows in the shoulder card at t=0 are about 10px tall (f0001.jpg), and the iPad overlay at 44-70s is too small to read (f0025.jpg). In crops/w-stay-signed.png, the card text ("Q3 review", "Reply to Claude", "Opus 5.5 Medium") is crisp at 2x but small at frame size.

## Motion and transitions
I read 8 strips. Scene changes are caused by the object on screen. The card widens to full frame (window-03, 2.7-3.0s). A cream panel sweeps in from a thin vertical line at 22.5-23.0s (window-16). The laptop draws from a dot to a bar to a black screen to a populated laptop in 0.9s (window-52, 70.5-71.4s). A black dot becomes the voice card at 86.5-86.7s (window-60). At 82.7-83.0s the Android card fades and a cream panel shrinks to reveal the presenter (window-57). The tablet unfolds with a hinge swing (window-04). Seams I counted in findings.json: 16 hard cuts, about 6 wipes, 3 shared-element draws and 2 UI state changes. I saw no cross-dissolve between worlds.

## Copy on screen
Twenty-one lines are listed in findings.json. Titles are 3-8 words and held 5-16s, so the reading rule (0.5s + 0.3s a word) is exceeded many times over; small pills such as "Hears you in a noisy room" hold about 2s (f0046.jpg). From crops/w-works-like.png, verbatim: "Android · Chromebooks and foldables", "Works like a laptop app", "Resizable sidebar", "Mouse and trackpad, with right-click". The Vietnamese welcome menu reads "Đính kèm tệp hoặc ảnh", "Chụp màn hình", "Thêm vào dự án", "Tìm kiếm trên web" (crops/w-24-more.png). The ending line "What would you like to see next?" (f0073.jpg) holds about 3s, which meets the 2s minimum. Hold times are read from 2s samples, so they carry about two seconds of error.

## Sound
Only voice is evidenced. audio.json kind is voice (0.763); the describe tags give speech 0.891 and music 0.105, so I name no music or genre. "click" 0.183 and "typing" 0.11 are under 0.2, so I claim no sound effects. Integrated loudness is -13.2 LUFS, short-term max -11.8, loudness range 2.4 LU, true peak -0.9 dBTP, which is 0.1 dB over the -1 dBTP ceiling. Speaking rate is about 204 words a minute (518 words in 152s, local whisper). Cuts are not locked to the sound: cuts_on_strong_onset_share is 0.0 against chance_share 0.094. There are 65 silence spans, the longest 3.3s at the very end.

## What to steal
1. One card per feature: label, two-line serif title, one proof UI, placed in the free right third from 0.5s and at least 40% of frame height (f0007.jpg).
2. Open on the finished result and animate the device within 5s (window-03).
3. Cause each seam with the object on screen: grow the card, or draw the device from a dot (window-52).
4. Change ground colour with topic: charcoal for audio, cream for visual (f0044.jpg versus f0040.jpg).
5. Make a numeral the hero for a statistic: "24" at 17.6% of height, with "33 in total" below (f0061.jpg).
6. Give the demo a story with a visible state change (4,406 to 3,886).
7. End on a held prompt and a 4.8s logo.
8. Avoid the weak points: keep shoulder-card UI above 2.6% of height and skip blank panels (f0012.jpg, f0050.jpg).
