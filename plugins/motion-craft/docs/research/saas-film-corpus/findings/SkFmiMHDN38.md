# How an Anthropic engineer uses Claude Docs (Claude, 83 s)

## Hook and structure

Frame 0 is a poster: a cream document page on a flat blue ground, the serif title "How an Anthropic engineer uses Claude Docs", grey placeholder lines and a hand-drawn cursor mid-page (`f0001.jpg`). It is the product, not a logo or a black frame. The hook is a visual one, since nobody speaks until t=7 s (transcript, first caption at 00:07). The cursor selects the title and a formatting bar appears at t=2 s (`f0002.jpg`). The title enlarges to two lines and a file labelled "dougs-demo.mp4" is dragged in at t=4 s (`f0003.jpg`). The video then grows into a player at t≈5.7 s (`strips/window-06-5.417s.jpg`).

The structure is intro (0-14.5 s), stand-up demo (14.5-37 s), launch-review demo (37-69 s), a return to the presenter (69-73.6 s), then the tagline and logo (73.6-83 s). The hero moment is the stacked area chart filling the frame at t=52 s, share 0.626 (`f0026.jpg`). It lands right after "@Claude add a chart" is typed (`f0025.jpg`). Doug's voice-over is a first-person, plain-spoken account at 151 words a minute (209 words, auto-captions).

## Rhythm

`metrics.json` gives 13 hard cuts, 9.4 cuts a minute, a median shot of 4.56 s and no bursts. One shot runs 23 s (37.17-60.17 s, 27.7% of runtime). That is outside the 1.8-3.5 s launch-film cadence, but it is not static: the median hold is 1.17 s, so something on screen changes about every second (typing, a flag, a new card). The pace comes from live typing inside long shots, with cuts saved for topic changes. The longest static run is the 8-second logo.

## Look and type

The ground changes with the section: flat desaturated blue in the intro, white app UI in the demo, cream for the tagline and logo (`f0001.jpg`, `f0027.jpg`, `f0040.jpg`). `metrics.json` look.saturation is 0.072. The one accent is Claude's clay orange: the name flag, caret, send button (`f0022.jpg`, `f0023.jpg`) and the logo asterisk. "You" gets a blue flag (`f0038.jpg`), and other teammates have their own flag colours (`f0012.jpg`).

Type pairs a serif for titles and section heads with a grotesque sans for body and chips. Ink measures at 720 p: the opening title 31 px (4.3%) at t=1 s, "Suggested by Claude" 52 px (7.2%) at t=24 s, and the tagline 42 px (5.8%) at t=77 s. The opening title is 7 words on one line, and on its two-line form it splits 4 and 3. Its accent is the bold weight on "Claude Docs", not a colour.

## Product interface

The UI is on screen about 89% of the runtime (0-73.6 s). It looks like the real Claude Docs app with a chat panel on the left (`f0027.jpg`), and it carries floating comment cards and a live-action video of Doug. The cursor is a hand-outlined arrow, so it is stylised, not the system one (`f0001.jpg`, `f0034.jpg`).

The camera crops hard into one region at a time, so small UI reads well: menu rows around 20-25 px (`f0007.jpg`) and typed lines 36-52 px (`f0014.jpg`). It pulls back to the full window only at t=52-54 s and t=67 s (`f0027.jpg`, `strips/window-50-67.25s.jpg`). Those pull-backs shrink body and chart text to about 10 px, which would not hold up on a phone. Doug's three-comment thread (`f0035.jpg`) is only readable in the zoomed crop that follows (`f0036.jpg`).

## Motion and transitions

Seams are mostly hard cuts (13) with the cause on screen. The cut at 14.54 s follows the cursor landing on "Team standups" (`strips/window-12-14.459s.jpg`). The cut at 37.17 s follows the same menu click (`strips/window-28-37.084s.jpg`). Before the first menu, the camera drifts down the page for about 0.8 s and then cuts at 12.67 s (`strips/window-11-11.875s.jpg`). The dragged video thumbnail grows into the player (`strips/window-06-5.417s.jpg`), the only morph. At t=73.6 s a cut moves from Doug's card to the cream ground (`strips/window-56-73.125s.jpg`).

Text enters by being typed, letter by letter, with a coloured caret (`f0012.jpg`-`f0014.jpg`, `f0038.jpg`). Ease curves were not measured.

## Copy on screen

On-screen copy is real content, not slogans. Verbatim from frames: "Suggested by Claude" (`f0013.jpg`), "@Claude add a chart" (`f0022.jpg`), "Docs with a visual grew every week" (`f0026.jpg`) and "@Claude is this right?" (`f0030.jpg`). Claude's reply reads "Mostly. For: docs with a data chart get shared more often than docs without one. Against: docs with only a diagram get shared less often." (`f0031.jpg`). That is 26 words held for about 3 s, against 8.3 s by the reading rule; the voice-over carries it. The closing line is "Claude makes it. You steer it." (`f0039.jpg`), 6 words, typed by two labelled cursors (`f0038.jpg`), then still. After that the film shows the Claude logo for about 5 s (`f0040.jpg`-`f0042.jpg`). The spoken call to action, "Next time your team works on a doc together, consider asking Claude" (transcript, 01:10), is not on screen.

## Sound

Evidence is from `audio.json` and `metrics.json`; the sound was not heard. The kind is music. Describe tags: speech 0.659, music 0.617, keyboard_musical 0.405, typing 0.376, synthesizer 0.301, click 0.27, piano 0.213. I name a synth and a piano only on those scores. Tempo is 129.9 BPM at beat confidence 0.353, which is weak. The speech runs 7-72 s over music, with a section change at 7.0 s and a silence span from 78.8 s to 83.0 s under the logo.

Loudness is -17 LUFS integrated, short-term max -13.6, loudness range 11.0 LU and true peak +0.4 dB. That misses the -14 LUFS and -1 dBTP targets. Cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.077 against a chance share of 0.158. The typing and click tags suggest keystroke sounds, but sync to the typing is inferred, not checked.

## What to steal

1. Make the product do the animating. Five named cursors typing at once (`f0012.jpg`, `f0013.jpg`) show collaboration; narration would only describe it.
2. Hold one demo as a single 20 s+ shot when the action is typing, and change something about every 1.2 s. This contradicts the 1.8-3.5 s cut rule for walkthroughs.
3. Place each cut on a cursor click and show the result under the still cursor.
4. Crop to 2-4x on the region being acted on; pull back to the full window only once or twice, and expect small text there to fail on phones.
5. Let the metaphor become the tagline: "Claude" and "You" flags type the last line (`f0038.jpg`), then hold the logo still for about 5 s.
6. Show the product checking itself ("Mostly." with For and Against, `f0031.jpg`); it reads as more credible than a success shot.
7. Do not copy the audio: -17 LUFS and +0.4 dBTP would fail the skill's social targets.

Not checked: ease curves, colour hexes (read by eye), title ink at t=40 s and t=45 s (the regions missed), and whether keystroke sounds line up with the typing.
