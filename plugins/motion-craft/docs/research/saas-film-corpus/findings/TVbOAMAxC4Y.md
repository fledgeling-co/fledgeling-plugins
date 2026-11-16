# TVbOAMAxC4Y: How Harvey Graph Helps Deliver More Accurate Legal Work (Harvey, 290 s)

## Hook and structure

Frame 0 is already a poster with the subject in it: a dark textured ground, a grey "Harvey Graph" title on the left and about ten white nodes on the right, with a caption at the bottom (`frames/f0001.jpg`, `frame0.isEvidence` true in `metrics.json`). By t=6 s the title is full white, a subtitle "Overview and early results" has appeared and the nodes are joined by edges (`f0004.jpg`, `strips/window-01-5.166s.jpg`). The hook is the cover plus "This video covers an experiment on Harvey's Legal Agent Benchmark." (transcript 00:00): a topic, not a payoff.

The film then runs as an argument. Context runs 12-37 s (`f0019.jpg`), the definition 37-92 s, worked graphs 92-144 s, law-firm scale 144-166 s, method 168-190 s, one question 190-226 s, charts 226-282 s, and the cover returns at 282-290 s. The hero moment is the dot grid becoming 21 folder circles at t=124 s, share 0.43 (`strips/window-20-122.866s.jpg`). The ending has no call to action: the closing caption holds about 8 s over the returned cover (`f0145.jpg`).

## Rhythm

This is one continuous shot. `metrics.json` reports 3 hard cuts (12.03, 281.53 and 282.33 s), 0.62 cuts per minute, a median shot of 9.88 s and a longest shot of 269.5 s, which is 92.9% of runtime. There are no bursts. 86.1% of sampled intervals are static and the longest static run is 26 s (ending at 90 s). Change comes from builds inside a slide (cards appearing about 2 s apart at `f0010.jpg` and `f0013.jpg`, counters at 128, 134 and 140 s on `sheets/sheet-05.jpg`) and from caption swaps every 3-14 s. The median hold is 5.65 s and the longest 21.77 s (`events`).

This contradicts binding rule 10 (cuts every 1.8-3.5 s) and rule 8 (a burst of cuts). The narration carries the pacing; something on screen still changes every few seconds to match the sentence.

## Look and type

93.1% of frames are light, with luma 230 and saturation 0.015 (`look.json` values in `metrics.json`). The dark charcoal card appears only at the cover and sign-off. Type is a high-contrast serif for titles and card headlines and a small grotesque sans for labels, captions and numerals. Colour is reserved for data. Rust-red nodes are organizations and people, blue squares are clauses and events (`f0052.jpg`), and bars are mid grey versus near-black (`f0121.jpg`).

Ink measurement (`hf measure ink`, frame height 720 px): the cover title is 68 px, 9.4% (t=7 s); the running header "Harvey Graph" is 30 px, 4.2% (t=20 s); "What's in the Knowledge Graph" is 31 px, 4.3% (t=70 s); "M&A Diligence" is 31 px, 4.3% (t=130 s); the card headline "Legal work depends on how documents relate to one another" is 21 px, 2.9% (t=13 s); the bottom caption first line is 20 px, 2.8% (t=130 s). Titles sit in rule 3's 4-9% band, and the cover is just over it. Crops `crops/title-cover.png` and `crops/header-light.png` show the serif at 2x. The longest title line is 5 words.

## Product interface

There is no product capture. Interface-like objects are redrawn: a matter card ("Solara / Pinnacle Cloud Systems: FTC Second Request", `crops/matter-card.png` frame `f0067.jpg`), a question card, a table of results, and graph explorers on synthetic data. The film labels them honestly with a dark tag, "Simulated with synthetic benchmark data" (`f0028.jpg`, t=54-62 s).

Phone-width legibility is partial. Captions and headlines pass. Node labels, folder names and the matter card timeline are about 10-14 px high on a 720 px frame, which is under rule 2's 2.6% of the short side (18.7 px). Rule 10 prefers real UI over invented UI; this invented UI is data-led, but its small text fails the floor.

## Motion and transitions

Strips read: `window-01`, `-02`, `-03`, `-09`, `-20`, `-23`, `-40`, `-48`. In `window-02-10.933s.jpg` the dark cover fades to mid grey between t=11.2 and 11.9 s, holds near-flat grey, and resolves to the light slide by 12.4 s. `window-48-281.166s.jpg` runs the same fade backward from 281.4 s to the dark cover at 282.6 s, so frame 0 and the last frame rhyme (`f0004.jpg` and `f0145.jpg`).

Inside the film, whole slides fade to near-blank before the next title. `window-23-142.5s.jpg` fades M&A Diligence out over about 0.4 s (142.5-142.9 s), and f0072 is a blank, non-evidence frame. These are dissolves, but between slides of the same world, not between unrelated scenes. Rule 7 forbids dissolves between worlds, so this is consistent with it. Rule 4 asks for exits 40-50% shorter than entrances. Here the exit is about 0.4 s against entrances of about 1-1.3 s (circle pack in `window-20-122.866s.jpg`, bars in `window-40-227.933s.jpg`), so exits are 60-70% shorter, steeper than the band. Caption changes (`window-03-15.766s.jpg`, `window-09-55.133s.jpg`) are quick swaps with no travel. The one camera-like move is a zoom from practice-area clusters into a single matter circle at about t=132-142 s (`f0067.jpg`).

## Copy on screen

The on-screen caption is the spoken script, line for line, at the bottom of the frame (`crops/caption-dark.png`: "We evaluated agents on complex legal tasks with and without the Harvey Graph."). Captions hold for as long as the sentence takes to say, about 3-14 s for 8-27 words, far above rule 2's 0.5 s plus 0.3 s per word. Numerals such as 302 facts and 72 entities (`f0052.jpg`) and 402,772 links (`sheets/sheet-06.jpg`, t=2:44) appear on screen without being spoken.

The facts reach the screen: 23 vs 10 turns, 19 vs 6 documents, 0% vs 75% criteria (`f0109.jpg`); quality 65 to 80%, 67 to 80% and 53 to 83% (`f0115.jpg`); cost $3.27 to $1.70, $2.31 to $1.34 and $63.93 to $33.88 (`f0121.jpg`). That matches rule 5. The final caption has no next step (`f0145.jpg`).

## Sound

The film is voice with no identified music. `audio.json` tags speech at 0.895, sigh 0.237, music 0.126 and click 0.052. Music is below the 0.2 floor for naming an instrument or genre, and `sound.beats` finds no steady beat (confidence 0.018, bpm null). Loudness is -22.8 LUFS integrated, -21.7 short-term max, true peak -4.7 dBTP and loudness range 2.7 LU. That is 8.8 LU under rule 9's -14 LUFS target, though the peak is within the -1 dBTP ceiling.

Cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.0 against `chance_share` 0.051. With three cuts that is thin evidence. I cannot hear the film, so everything here comes from tags and numbers.

## What to steal

- Caption every spoken sentence and put the proving picture on screen with it. Change the picture on the sentence boundary (transcript 01:50 against `f0058.jpg`).
- Reveal stats as large numerals, one at a time about 6 s apart, next to the diagram they measure (`sheets/sheet-05.jpg`, 2:08-2:20).
- Show the argument in one before-and-after card, same question and same model (`f0109.jpg`).
- Close on the opening card, reached by a fade through grey, so the end rhymes with frame 0 (`window-02`, `window-48`).
- Label simulated data on screen at the moment the narration says it (`f0028.jpg`).
- Don't copy the pacing for a launch film (86% static, 3 cuts, no music), the small in-graph labels or the missing call to action.
