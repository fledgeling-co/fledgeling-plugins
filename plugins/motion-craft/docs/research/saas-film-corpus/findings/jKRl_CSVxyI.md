# jKRl_CSVxyI: Using Claude Opus 5.5 as your daily driver (Claude, 212.5 s)

## Hook and structure

A presenter-led walkthrough that opens on the subject. The first frame is the presenter mid-smile (strips/window-01-0s.jpg, f0); the wordmark "Claude Opus 5.5" is on by 1.17 s (same strip, frame 8), and "Compared to Opus 5" and "Faster" follow by about 3.5 s while she says the release line. The film runs claims first (0-18 s), then a proof (side-by-side run, 22.8-66.8 s; usage popover at 72 s, 5-hour limit 4% for 5.5 in f0037.jpg), a counter-case where medium effort misses a file (98-137 s), the fix on High (137.6-151.9 s), two configuration tips, a spoken sign-off and a logo card from 205.4 s. The hero moment is at 44 s (share 0.207): Opus 5.5's whole answer fits on screen while Opus 5 is still listing file reads (f0023.jpg).

## Rhythm

metrics.json gives 20 hard cuts, 5.65 cuts a minute, a median shot of 8 s, 7 shots over 10 s and no burst (`bursts` is empty). The longest shot is 32.17 s (34.63-66.8 s, 15.1% of runtime), a split-screen where typing, step lists and diffs supply the change. The first cut is at 22.87 s, so the opening 22.9 s is one continuous presenter shot with overlay. 28.6% of 2-second intervals are static, the longest run 6 s ending at 96 s. This is a tutorial pace, well outside the 1.8-3.5 s launch-film cadence.

## Look and type

Two grounds alternate: warm dark home-office footage with a dark left vignette that carries the text (f0004.jpg), and a cream stage holding near-black app windows (f0019.jpg). Overlay type is a serif for headings with a sans caption under each. I measured ink heights on the 720 px frame: title "Claude Opus 5.5" 50 px (6.9%) at t=1 s; "20% cheaper per token" and "25% more usage" 38 px (5.3%) at t=17 s; "Faster" 29 px (4.0%); the end wordmark 80 px (11.1%) at t=210 s; the sans captions 19-21 px (2.6-2.9%), the lowest-contrast text in the film. The list never exceeds four words a heading. Coral is used for the Claude star and inline code only; green and red appear only as diff counts (f0075.jpg). Crop crops/lower-third-list.png confirms the copy verbatim.

## Product interface

Real application captures with a real cursor, real file names and real numbers: "Read 3 files, edited 2 files, ran 2 commands +190 -12" and "30 of 30 passing" (f0023.jpg), "5-hour limit ... 4%" (f0037.jpg), "41 of 41 passing" (f0075.jpg). Full-window frames carry 11-13 px text and are not phone-legible (f0032.jpg, strips/window-34-66.733s.jpg); the film solves this with scale-up crops of the prompt box (f0019.jpg), the usage popover (f0037.jpg) and the effort slider (f0045.jpg, f0046.jpg), where text is about double size. A code card (sheet-04 at 1:56-2:02) shows `customer_ref` highlighted in the file the agent missed, which is the whole point of that segment.

## Motion and transitions

Twenty hard cuts alternate presenter and screen, each on a topic change: the cut at 22.87 s lands on "let's run them side by side" (strips/window-08-22.8s.jpg). After it, one app window slides in from the right over an empty cream stage (same strip, frames 4-9). At 26.9 s a push scales the two windows up to the prompt box (strips/window-09-26.666s.jpg). Inside windows, list rows append one by one, a "sped up" pill marks compressed time (f0019.jpg), popovers fade in and the chat dims about half when a code card lies over it (sheet-04 at 2:02). Overlay lines enter one at a time from 1.2 s and do not exit before the cut at 17.9 s. I did not open a strip after 127.7 s; later motion is read from sheets only.

## Copy on screen

Overlay list, verbatim from crops/lower-third-list.png and crops/usage-line.png: "Faster / than Opus 5 on the same task", "Better answers / shorter, clearer about what to do next", "20% cheaper per token / $4 in, $20 out per million tokens", "25% more usage / on Pro, Max and Team limits". The sixth line, "~40% cheaper per task / it needs fewer tokens to get to a result", is seen in sheet-01 at 16 s. Holds run 2.9-16.7 s against a 1.1-3.5 s floor, so all pass. One weakness: the 25% line appears after the spoken "25% further" at 8 s; it is absent in sheet-01 at 8 s and present in strips/window-04-9.8s.jpg at 10.47 s, a lag of about 2.4 s. The summary answer text ("Want me to close that in this change, or open the PR as is?", f0023.jpg) is real UI copy. The ending carries no on-screen call to action (f0106.jpg).

## Sound

I did not hear the film. audio.json classes it as voice, with describe tags speech 0.864 and music 0.47; plucked_string_instrument 0.242 and keyboard_musical 0.202 are the only instrument tags above 0.2, so a quiet bed is possible but unconfirmed. Beats: count 0, confidence 0.015 ("no steady beat"). typing 0.169 and typewriter 0.143 sit below the threshold, so no keyboard sound is claimed. metrics.json: integrated -16 LUFS, short-term max -14, true peak -3.5 dB, loudness range 2.6 LU. `cuts_on_strong_onset_share` is 0.0 against `chance_share` 0.067, so the cuts are not locked to the sound; they follow the speech. Delivery is about 204 words a minute (721 words, human-written captions). Silence spans occur only at 207.5-212.5 s.

## What to steal

1. Prove a comparison with identical input in two windows and cut to the result when the faster side finishes (34.6-66.8 s; f0023.jpg).
2. Build must-carry numbers as a persistent list that adds a line per spoken claim: five lines, headings 4.0-6.9% of frame height, captions about 2.9% (f0004.jpg, f0007.jpg). Sync each line to its spoken claim; this film lags by 2.4 s on one.
3. Zoom small UI to fill much of the frame before asking anyone to read it (f0045.jpg versus f0032.jpg).
4. Show the counter-case before the advice: medium effort misses `customer_ref`, then High finds it (98-152 s).
5. Mark compressed time with a "sped up" pill (f0019.jpg).
6. Close on a brand card held 7.1 s, star before wordmark (f0104.jpg, f0106.jpg), and put the ask on screen as well.
