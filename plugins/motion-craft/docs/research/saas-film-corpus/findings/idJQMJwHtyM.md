# Claude for Google Workspace™ (idJQMJwHtyM)

## Hook and structure

Frame 0 is already the poster: three Google app icons (Docs, Sheets, Slides) above "Introducing Claude for / Google Workspace" on a cream ground (`f0001.jpg`; `frames.frame0.isEvidence` is true). The icons shrink and drift up while the title fades in between 0.8 s and 1.1 s (`strips/window-01-0s.jpg`), and the card holds until the first hard cut at 4.54 s (`rhythm.first_cut_s`).

The film then runs as one demo per app. Docs at 4.5-18 s (open Extensions, choose Claude, ask for a tightened summary), Sheets at 18-34 s (drop two CSVs, ask for a budget-vs-actuals report), Slides at 34-50.8 s (open Connectors, toggle Salesforce and Google Drive, ask for a QBR deck). Then a tagline at 51-53.7 s and the logo from 54 s to the end. The hero moment is the coral sweep at t=30 s (share 0.5), where an empty sheet resolves into a finished report (`f0016.jpg`, `f0017.jpg`). There is no voiceover; the transcript holds only `[music]` tags.

## Rhythm

`metrics.json` gives 5 hard cuts, 5.0 cuts a minute, a median shot of 3.27 s and no burst. Four of the cuts fall in the first 10 s (4.54, 6.46, 8.08, 10.08 s). The fifth, at 50.79 s, is the window leaving. Between 10.08 and 50.79 s sits one shot of 40.71 s, 68 % of the runtime (`rhythm.longest_shot`). Change inside it comes from zooms and UI state changes, not cuts. About a quarter of sampled intervals are static (`frames.intervals_static_share` 0.241, longest static run 6 s ending at 42 s). The film is paced by what the user does next, not by edit rate.

## Look and type

Every sampled frame is light (`light_share` 1.0, luma 239.1). The ground is warm cream, the browser window floats on it with a soft shadow, and nothing else sits on the ground. Title lines measured with `hf measure ink` on the 720 px frame: "Introducing Claude for" 54 px (7.5 %), "Google Workspace" 52 px (7.2 %), "Claude wherever you work" 55 px (7.6 %), the logo lockup 79 px (11.0 %), and the generated deck's slide title 48 px (6.7 %). The serif titles sit inside the 4-9 % band. The longest title line is 4 words (tagline).

The title is two lines with a lighter second line (`crops/title.png`: dark "Introducing Claude for", grey "Google Workspace"). Coral appears only on the Claude sunburst, the "Working on it..." star (`f0015.jpg`) and the 28-30 s sweep. The Google colours show only in the icons and the app chrome. Generated documents use forest green (`f0009.jpg`, `f0025.jpg`).

## Product interface

The UI is real captured Google Workspace with Claude's panel, on screen from 4.54 to 50.79 s, about 77 % of runtime. A real-looking cursor clicks Extensions and then Claude (`strips/window-03-6.375s.jpg`, `strips/window-05-9.834s.jpg`). Wide shots are not legible at phone width: body text in `f0003.jpg` is about 10-14 px. The zoomed shots are: panel text is 25-35 px in `f0007.jpg`, `f0014.jpg` and `f0021.jpg`, and the connector toggles are readable in `f0021.jpg`. Results read as shape and colour: the KPI tiles ($7,300,000, $7,341,500, +$41,500, 7) and green/red status cells in `f0017.jpg`, and the green title slide in `f0025.jpg`. Phone-width legibility is "partly".

## Motion and transitions

Transitions by count: 4 hard cuts in the opening, about 5 continuous zooms, 1 coral mask sweep (28-30 s), 1 slide-out of the window at 50.4-51 s (`strips/window-29-50.375s.jpg`) and 2 fades through blank cream (title in at 0.8 s, tagline out at 53.5-53.7 s, `strips/window-30-53.334s.jpg`). That is five kinds, each caused by what is on screen: the zoom follows the next click, the sweep follows Claude finishing, the window leaves to clear the ground for the tagline.

Prompts are typed fast, about 88 characters a second (`strips/window-14-24.709s.jpg`: "Pull together Q3 budget vs. act" to "actuals report:" in 0.17 s). The side panel slides in from the right (`strips/window-07-11.917s.jpg`). The tagline's exit (about 0.2 s) is shorter than its entrance.

## Copy on screen

Five lines carry the copy, quoted from crops and frames. "Introducing Claude for Google Workspace" (5 words, held about 3.2 s). "Tighten up the executive summary and lead with recommendation. Then clean up the formatting with clean headings and put the next steps into a table." (`f0007.jpg`). "Pull together Q3 budget vs. actuals report: a tab for each team, plus a summary tab with a chart, and flag anything over budget." (`f0014.jpg`). "Build a QBR deck for Northfield from our Salesforce data and recent call notes." (`f0023.jpg`). "Claude wherever you work" (4 words, held about 2.6 s, `crops/tagline.png`).

The title needs 0.5 + 0.3 x 5 = 2.0 s and gets 3.2 s. The tagline needs 1.7 s and gets 2.6 s. The logo holds about 6.3 s against the 2 s minimum for a last line. There is no statistic or customer claim in copy, only the work shown in the panel.

## Sound

`audio.json` classes the sound as music. The describe tags are music 0.819, keyboard_musical 0.52, piano 0.372, wind_instrument 0.353, brass_instrument 0.316, synthesizer 0.309, saxophone 0.209, electric_piano 0.2. Piano is the only instrument named with support above 0.3. Tempo reads 90.2 BPM with beat confidence 0.217, which is low. Sections run 0-3.99, 3.99-48.03 and 48.03-60.01 s.

Loudness is -15.4 LUFS integrated (short-term max -13.7), true peak -0.6 dBTP, loudness range 8.8 LU: 1.4 LU under the -14 target and 0.4 dB over the -1 dBTP ceiling. `cuts_on_strong_onset_share` is 0.0 against a chance share of 0.135, so the cuts are not locked to the sound. The first section change (3.99 s) lands 0.55 s before the first cut. Silence runs from 58.46 s to the end. No sound effects are evidenced; I could not hear the film.

## What to steal

- Show one typed request and one finished result per surface, and zoom onto the prompt box so the text reads at 25 px or more.
- A film can hold one 40 s screen shot if zooms and state changes arrive every 2-6 s; put the hard cuts at the start.
- Use one non-UI graphic effect, once, for the reveal (the coral sweep), in the brand accent.
- Close with a short tagline (4 words, 2.6 s), fade through blank ground, then a 6 s logo hold.
- Start with the subject and title in frame 0 and make the first cut after 4.5 s.

Where this film departs from the skill: 5 cuts a minute is under the 1.8-3.5 s cadence (rule 10), and cuts do not meet the sound (rule 8). It also misses the true-peak limit (rule 9). Wide shots fail the phone-width test (rule 5), but the zoomed ones pass.
