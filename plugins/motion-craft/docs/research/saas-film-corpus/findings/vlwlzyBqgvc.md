# Introducing Command Center (Harvey, 55.4 s)

## Hook and structure

Frame 0 is an off-white ground, not black. The headline "Legal AI moves fast" types in letter by letter from t=0.017s and is complete by 0.4s (`strips/window-01-0.017s.jpg`, `f0001.jpg`). The hook is a claim and the product is not on screen yet. The first email cards arrive at 2.0s in the top right (`f0002.jpg`). There is no speech: whisper heard only "Music" and the caption track was Russian, so the transcript source is none.

The film runs in three movements. From 0 to 7.15s the problem builds: "New models / New tools / New questions", an inbox that grows to eight rows (`f0004.jpg`), then "It's hard to feel like you're in control". From 7.15 to 14.78s a claim card, "Steer your AI transformation with confidence", leads into the dashboard. From 14.78 to 46.6s three demos follow, each introduced by a black card: a typed query that returns a Top power users chart (14.78–23.03s), a peer comparison (25.8–29.17s), and a releases checklist (32.28–37.1s). The last 9.5s of that run is an analytics chat that generates a deck. The payoff is "You're not just keeping up", then "You're setting the pace", then the lockup. I put the hero moment at t=41.97s, where the generated slide fills the side panel (`f0022.jpg`, `f0023.jpg`). That is 0.757 of the runtime, 1.5s after music section E begins.

## Rhythm

`metrics.json` gives 9 hard cuts, 9.74 cuts per minute and a median shot of 4.52s. The longest shot is 9.5s (37.1–46.6s, 0.171 of the runtime). No burst was detected and no shot runs past 10s. That is slower than the 1.8–3.5s launch-film range, yet the film does not feel static because something changes about every 1.5s inside each shot (`events.median_hold_s`). Typing, list stacking, KPI counters and draw-on lines supply that change. Only 0.185 of sampled intervals are static, and the longest static run is the closing lockup (to 54s).

## Look and type

The look is almost monochrome (saturation 0.04, bw_share 0.86). Near-white grounds take 0.679 of sampled frames and black takes 0.321. Black carries statements (`f0005.jpg`, `f0013.jpg`, `f0016.jpg`, `f0025.jpg`) and white carries product. The only colour is small: green +5% deltas, mauve "needs attention" bars (`f0007.jpg`), sage-teal email icons (`f0003.jpg`) and the dark-teal generated slide (`f0023.jpg`). The accent is typographic. "setting" is italic at t=48s (`f0026.jpg`).

Every claim is set in a serif and UI text is a grotesque. "Command Center" is bold sans under a serif "Harvey" (`crops/endcard.png`). I measured the ink height of six title lines with `hf measure ink`:

| t | line | px | % of 720 |
|---|---|---|---|
| 1s | Legal AI moves fast | 59 | 8.2 |
| 24s | See where you're leading or lagging | 56 | 7.8 |
| 30s | Stay current on every release — | 55 | 7.6 |
| 30s | and act on it fast | 44 | 6.1 |
| 51s | Harvey | 74 | 10.3 |
| 51s | Command Center | 60 | 8.3 |

The range is 6.1–10.3%. Each includes descenders, so the lockup runs above the 4–9% band. The longest title line is 6 words. Density is sparse, with a single idea per card.

## Product interface

UI is on screen for about 66% of the runtime. That is my estimate from the cut times: 2–7.15s inbox cards, 11.37–23.03s, and 25.8–46.6s. It is redrawn or simplified UI with a fictional firm, Whitford Lane. The data is consistent across shots: 304 active users and 64% at 11.4s (`f0007.jpg`), 305 and 65% at 38s (`f0021.jpg`). The cursor is a real arrow (`f0010.jpg`, `f0017.jpg`). The camera zooms into one component until it fills the frame (`f0009.jpg`, `f0011.jpg`, `f0016.jpg`). The Top power users card spans about 870 of 1280 px (68% of the width), and its title is about 34 px high. The full-window shots are only partly legible. Labels in `f0007.jpg` and the chat panel in `f0022.jpg` sit at 8–12px (`crops/dash-kpi.png`, `crops/chat.png`), so they would not read at phone width.

## Motion and transitions

Text enters by typing with a per-letter fade: 19 characters in about 0.35s (`strips/window-01-0.017s.jpg`). The headline "See where you're leading or lagging" does the same at 23.03s (`strips/window-13-23s.jpg`). Lists leave by fading top line first while the next headline types (`strips/window-04-4.967s.jpg`). All nine seams in the cut list are hard cuts. The ones I opened (7.15, 11.37, 23.03, 25.8, 37.1 and 46.6s) each follow a finished typed line and swap ground colour or screen. At 11.37s a black card cuts to a dashboard whose percentages tick from 39% to 56% as panels slide in (`strips/window-07-11.334s.jpg`). At 25.8s a dotted peer line draws left to right under a legend (`strips/window-14-25.767s.jpg`). At 46.3s the slide deck builds and then cuts to black (`strips/window-26-46.3s.jpg`). A hard cut between a card and a screen is the grammar here; there are no dissolves. I did not measure ease curves.

## Copy on screen

Claims are short, in a plain voice, and in the second person: 4–10 words. "Legal AI moves fast" is held about 1.6s. The 8-word "It's hard to feel like you're in control" is held about 1.7s against 2.9s on the 0.5s + 0.3s-per-word rule (`f0004.jpg`, `strips/window-05-7.117s.jpg`). "You're not just keeping up" has about 1.3s for 5 words (`f0023.jpg`, `f0025.jpg`). The problem is shown, not named in a caption: the inbox fills with real-looking mail ("Meridian AI", "The AI Brief", `crops/inbox.png`). The closing lockup is the longest-held copy at about 5.4s. There is no CTA line. Product copy is verbatim from crops, such as "Who are the top Harvey users in the last 30 days?" (`f0010.jpg`) and "Completed in 3 steps" (`crops/chat.png`).

## Sound

The film has music and no speech. `audio.json` describe tags are bowed_string_instrument 0.77, violin_fiddle 0.744, cello 0.671 and orchestra 0.559. `metrics.json` reports no steady beat (confidence 0.127) and five sections at 0, 4, 17, 34.5 and 40.5s. Integrated loudness is -20.7 LUFS, short-term max -17.2, true peak -3.5 dBTP, LRA 10.2 LU. That is about 6.7 LU under the -14 LUFS social master. The cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.222 against a chance share of 0.192, a gap of 0.03. The only visible link is that section E starts at 40.5s, shortly before the slide appears at about 42s. I found no sfx evidence and did not verify any typing sounds.

## What to steal

- Start frame 0 with a typed claim and let it complete inside 0.5s; hold the product back until after 2s (`strips/window-01-0.017s.jpg`).
- Put statements on black and screens on near-white, and let the colour change mark each beat (`dark_share` 0.321).
- Zoom one component to about two-thirds of the frame width for the data beat, then widen for context (`f0011.jpg`, `f0007.jpg`).
- Count KPI numbers up while the first dashboard assembles (`strips/window-07-11.334s.jpg`).
- Keep each demo to one idea and one card, introduced by one line.
- Keep the data identical across shots so the UI reads as one product.
- End on a name lockup for over 5s with no CTA (`f0026.jpg`–`f0028.jpg`).
- Do not copy: claim cards shorter than the reading rule, and the quiet master (-20.7 LUFS).
