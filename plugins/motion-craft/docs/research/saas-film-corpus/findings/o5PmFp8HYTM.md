# Harvey: Stay in Flow From Document Intake to Final Deliverable (51 s)

## Hook and structure

Frame 0 is a near-black card with the white serif wordmark "Harvey" centred, 59 px tall (`f0001.jpg`; `metrics.frames.frame0` luminance 0.059, 95% blank cells). It is a lone logo, so it breaks binding rule 1 on its face, but it lasts only 1.3 s: the wordmark fades out and a hard cut lands on a white card reading "Move Faster with Legal Agents" (`strips/window-01-1.233s.jpg`). By t=4 s the real product is on screen: the Harvey home with a prompt being typed (`f0003.jpg`). So the hook is a claim, then the product, inside 4 s.

The film then follows one job. Prompt typed and sent (4-9 s); the assistant suggests a review table and a cursor presses "Yes, build a Review table" (`f0008.jpg`, `f0009.jpg`); the workspace scales up with a 47-row table (18 s, `f0010.jpg`); a second prompt drafts a memo while reasoning steps stream (26-29 s, `f0014.jpg`, `f0015.jpg`); the memo opens with 35 tracked changes (`f0017.jpg`) and resolves to a clean draft (`f0019.jpg`); the camera zooms to Export (`f0022.jpg`). A white card "Stay in the Flow from Start to Finish" (`f0023.jpg`) cuts to a dark close, "AI Tailored for Law" with the wordmark added by 48 s (`f0025.jpg`). I picked t=18.0 s (share 0.353) as the hero moment.

## Rhythm

`metrics.rhythm`: 2 hard cuts (1.3 s and 46.97 s), 2.35 cuts a minute, median shot 4.05 s, and one shot of 45.67 s that is 89.5% of runtime. There is no burst. The mean shot (17.01 s) sits far from the median because the long shot dominates. Pace comes from change inside the shot: typing, cursor moves, scale-ups and camera pushes (`strips/window-04-9.866s.jpg`, `window-08-18s.jpg`, `window-12-22.566s.jpg`). 40% of sampled intervals are static (`intervals_static_share` 0.4), with a longest still run of 6 s ending at 8 s. This contradicts rule 10's 1.8-3.5 s cut cadence, and rule 8's burst: a film that is a single recording can carry a launch message without either.

## Look and type

The ground is white for the product section (84.6% of frames light, luma 222.8, saturation 0.019 in `metrics.look`) and near-black for the open and close. There is no accent colour; the one saturated element is the red tracked-change text in the memo (`f0017.jpg`). One serif face does all the titling and one grotesque the UI. Measured ink heights with `hf measure ink` (frame height 720): the opening wordmark 59 px (8.2%), "Move Faster with Legal Agents" 64 px (8.9%), "Stay in the Flow" 64 px (8.9%), "AI Tailored for Law" 51 px (7.1%), the closing wordmark 42 px (5.8%), and the small wordmark on the home screen 28 px (3.9%). Title lines are one line, at most five words, with no accent word. The three title lines sit at 7.1-8.9%, inside rule 3's 4-9%.

## Product interface

Real UI with a real cursor shows for about 87% of runtime. The home and reply views are large and readable: the prompt box text in `crops/prompt.png` and the assistant's reasoning steps in `crops/reasoning.png` read cleanly, and the review toolbar crop (`crops/review-toolbar.png`) shows "Track changes", "Show edits", "1 of 35", "Accept", "Reject", "Accept all", "Reject all" and a "Review 35" badge. The weak part is the workspace: at 18-40 s (`f0010.jpg`, `f0018.jpg`, `f0021.jpg`) table and memo text is about 5-7 px tall at 720p, so it is unreadable on a phone. It is legible only where the camera pushes in (`f0011.jpg`-`f0013.jpg`, `f0022.jpg`). The invented-looking content (Project Sandbar, 47 files, HVY Services memo) still comes across as real work, which supports rule 10's real-UI preference.

## Motion and transitions

Two hard cuts are the only cuts, and neither has an on-screen cause, so they fall outside rule 7's "caused by something on screen"; they join title cards to the product. Everything else is a product event: the cursor press on send leads to the reply view (9.9-10.1 s), the click on "Yes, build a Review table" leads to the thumbnail-to-full scale-up at 18.0-18.97 s (`strips/window-08-18s.jpg`), the finished reply opens the memo at about 30 s (`strips/window-16-28.966s.jpg`), and accepted edits turn red text to clean text at 34-38 s. Text enters by typing (`f0003.jpg` shows "contracts fro" mid-word) and by word-by-word streaming (`strips/window-04-9.866s.jpg`). The camera pushes toward the Export button at 41-43 s (`strips/window-20-41.166s.jpg`), and the last title card swaps white for dark at the 46.97 s cut (`strips/window-23-46.9s.jpg`). Exact easing was not measured.

## Copy on screen

There is no voiceover; transcript source is none (the YouTube video has no captions, and whisper only returned a repeated "The"). Verbatim titles: "Move Faster with Legal Agents", "Stay in the Flow" followed by "from Start to Finish", "AI Tailored for Law". The prompt reads "Extract each of the key terms and run a comprehensive change of control analysis over each of the attached material contracts from the data room." and the reply starts "This query would work best with a review table." The opener holds about 0.7 s (the home screen is already fading in at `f0002.jpg`), well short of rule 2's 2.0 s for five words. "Stay in the Flow from Start to Finish" holds about 3 s for seven words, which passes, and the closing line holds 4.0 s, which passes the 2 s rule for a last line. There is no URL or action line.

## Sound

Music only: `audio.json` kind music (confidence 0.68), describe tags music 0.727, keyboard_musical 0.478, synthesizer 0.359, gong 0.259, organ 0.258. No steady beat (beats confidence 0.033, bpm null) and no silence span. Loudness: -14.4 LUFS integrated, -12.9 short-term max, true peak -1.8 dBTP, LRA 2.1 LU. That meets rule 9 (-14 LUFS, at or below -1 dBTP). The cuts are not locked to the sound: `cuts_on_strong_onset_share` 0.0 against `chance_share` 0.066. The strongest onsets are at 17.25 s (0.92) and 36.485 s (1.0); the 17.25 s onset comes 0.75 s before the 18.0 s scale-up, so the hero is near but not on the music's peak. I could not hear the film, so these are tag scores, not heard instruments.

## What to steal

1. Treat a walkthrough as one continuous shot and move the camera every 3-6 s (scale-up, push, zoom) instead of cutting; it held 51 s with 2 cuts.
2. Give a decisive click its own beat: the "Yes, build a Review table" pill alone on white at 16 s (`f0009.jpg`), then scale the result in.
3. Push the camera into dense UI until text is at least 12 px at 720p; show the full workspace only briefly. This film's 5-7 px workspace is what to avoid.
4. Use a brand card to open and close, but keep the opener to 1.3 s and give the first title at least 0.5 s plus 0.3 s a word (2.0 s for five words).
5. Close with a 4 s dark tagline card and a smaller wordmark added about 1 s later, swapping ground light-to-dark at the cut.
6. Put a sound hit on the hero scale-up; here the music has no pulse and the peak lands 0.75 s early.
