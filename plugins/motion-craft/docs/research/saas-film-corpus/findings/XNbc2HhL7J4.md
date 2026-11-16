# Claude Cowork: coming to mobile and web (XNbc2HhL7J4)

An 80.7 s launch film with no voiceover. A music bed and on-screen type carry one scenario: a user briefs Cowork about an Acme QBR on a laptop, the work runs overnight, and the finished brief arrives on a phone.

## Hook and structure

Frame 0 is not black or empty. `strips/window-01-0.042s.jpg` shows the white serif words "Claude keeps working," on a mid-blue ground, assembling word by word and complete by 0.25 s. `window-02-1.042s.jpg` adds "even when you're not" at 1.29-1.7 s. At 2.0 s an empty white card appears (`f0002.jpg`) and fills with a typed prompt by 2.6 s (`f0003.jpg`). The hook therefore lands inside 3 s, and the first cut comes at 5.0 s (`metrics.json` rhythm.first_cut_s).

The structure is hook (0-5 s), setup by typing (2.6-12.6 s), demo of scheduling (12.6-24.9 s), a pull-back to a laptop frame (24.9 s), an abstract "working" cloud (26.3-35.8 s), the phone payoff (35.8-57 s), a second cloud (58-66 s), a recap proof on the laptop (67.4-73.9 s), a tagline (74 s) and the logo (77.7 s). The hero moment is the lock screen "Your Acme brief is ready" (`f0019.jpg`, t=36 s, share 0.446).

## Rhythm

`metrics.json` gives 12 hard cuts, 8.92 cuts a minute and a 2.79 s median shot, inside the 1.8-3.5 s launch range. The mean is 6.21 s because five shots exceed 10 s, and the longest runs 15.96 s (51.46-67.42 s, 19.8% of runtime). There is no burst (`rhythm.bursts` is empty). Instead there are two clusters: four reframes while the prompt types (5.0, 6.75, 8.29, 9.79 s) and three punch-ins on the email text (49.71, 50.88, 51.46 s). A film this calm does not need the 5-8 cut burst the skill asks for, and nothing in it feels slack.

## Look and type

Ground colours change by scene: mid blue for the composer and laptop (`f0014.jpg`), pale grey-blue for the phone (`f0020.jpg`), cream for chat and the end card (`f0040.jpg`). Coral is the single accent: send button, star, pills, halftone dots. `look.json` saturation is 0.111 and the light share of frames is 0.825.

Measured line heights against the 720 px frame: "Claude keeps working," 54 px (7.5%) at 0.6 s, "Got it." 48 px (6.7%) at 13 s, "Running your recap" 51 px (7.1%) at 60 s, the tagline's first line 39 px (5.4%) at 74 s, and the logo 78 px (10.8%) at 79.5 s. The opening line is 7 words on one line, one more than the skill's limit of 6. It is the only element on screen, which is why it works.

## Product interface

UI is on screen for roughly 65% of runtime (an estimate from sampled frames). It is rendered as detailed device frames, not simplified art: a laptop with Cowork's Progress, Outputs and Context panels (`crops/laptop-ui.png`) and a phone showing the brief with a "NEEDS YOUR ATTENTION" card and source tags Gmail, Slack and Transcript (`crops/attention-card.png`). The only pointer is a hand cursor pressing Schedule at 22 s (`f0012.jpg`).

Legibility splits. Macro and phone shots are readable at 720p (`f0021.jpg`, `f0026.jpg`). The laptop-framed shots at 25-27 s and 66-67 s carry about 9 px text (`f0013.jpg`, `f0014.jpg`), and the Schedule task details at 16-20 s are faded (`f0011.jpg`). Those would not read at phone width.

## Motion and transitions

Five transition kinds appear: hard cuts (12), continuous camera moves (about 3), one push (the chat scrolls off at 74 s, `window-43-72.375s.jpg`), one short dissolve inside the phone (37.42-37.54 s, `window-24-37.084s.jpg`) and UI state changes. Each has an on-screen cause. The best seam is `window-35-58.667s.jpg`: the phone slides down over 58.67-58.92 s while the star pill rises, then "Acme QBR ended" types in. Nothing dissolves between worlds.

Text enters by word fade (headline), caret typing with a coral highlight on the newest clause (`f0005.jpg`) and letter-by-letter pills ("Searc", "Finishing up your ta", `f0016.jpg`, `f0017.jpg`). At 24.9 s the full-bleed UI cuts to the laptop frame in 0.04 s (`window-18-24.834s.jpg`).

## Copy on screen

Copy is sparse and sits in three places: the headline, the typed UI text, and the closing tagline "Your thinking sets the direction. Claude keeps it moving." (9 words, two lines, `f0038.jpg`). The opening line is held 3.3 s against the 2.6 s the reading rule needs (0.5 s plus 0.3 s a word for 7 words). The logo is held 2.6 s, above the 2 s floor. I could not measure the tagline's hold because its exit falls between samples. The long phone text is there to be scrolled, not read, and the facts that matter (8:14, "Your Acme brief is ready", ticket counts, dates) are shown at large size.

## Sound

The track is music only. The captions contain `[music]` tags and two "Heat." lines that are caption errors, so there is no speech and no word count. `audio.json` tags: keyboard_musical 0.564, synthesizer 0.491, percussion 0.353, theremin 0.281, drum 0.277. Tempo is 96 bpm, but beat confidence is only 0.415. Integrated loudness is -12 LUFS, short-term max -10.4, loudness range 7.7 LU and true peak +1 dBTP, which is over the -1 dBTP ceiling.

`cuts_on_strong_onset_share` is 0.083 against a chance share of 0.072, so the cuts are not locked to the sound. Picture changes do track sections: cuts at 5.0 and 26.25 s fall within 0.15 s of section starts at 5.135 and 26.395 s, and the lock screen is up by 36 s (`f0019.jpg`) as section B returns at 35.775 s. The music falls silent from 78.235 s, under the logo.

## What to steal

- Show waiting as an abstract field with a central pill that types its status and a few blurred satellites (`f0015.jpg` to `f0018.jpg`). It replaces a caption about time passing.
- Make the proof a named scenario with specific numbers and let the user edit the output (`f0028.jpg` to `f0029.jpg`).
- Zoom text until its line pitch is over 10% of frame height (118 px at `f0004.jpg`), then cut back to the wide shot.
- Hand scenes over with a moving element, not a dissolve (`window-35-58.667s.jpg`).
- Put the reveal on a music section return (36 s against 35.775 s), and let the logo sit in silence for 2.5 s.
- Do not copy the master level: +1 dBTP breaks the -1 dBTP rule.
