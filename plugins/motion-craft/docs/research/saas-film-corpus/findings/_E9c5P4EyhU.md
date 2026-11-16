# How people are using Muse (38 s, Muse)

## Hook and structure

Frame 0 is a poster with a subject in it: one phone-shaped video card of a woman mid-sentence on the left, a caption pill reading "My Muse's name is Lizzie." and a white-to-blue gradient (`f0001.jpg`, `crops/caption.png`). The right half is empty, and the product is named in the first spoken sentence. By t=2 s portrait cards slide in with nickname captions ("Chippy.", "Noodles."), and a cream plush mascot arrives at 2.5 s (`f0002.jpg`, `strips/window-05-2.536s.jpg`).

The film runs in seven beats. A roll call and mascot chips fill 0-6.84 s. Hard cuts at 6.84 s and 7.47 s lead to a blank white title card at about 7.5-9.5 s. A drifting proof run of customer clips fills 9.5-31.7 s, a last customer card grows to full frame at about 32-34 s, and a closing line and small print end it at 34-37.84 s. I took the title card as the hero moment, t=8.7 s, share 0.23, because it is the only imagery-free frame and it states the premise (`f0005.jpg`).

## Rhythm

`metrics.json` gives 2 hard cuts, 3.17 cuts per minute and a 6.84 s median shot. The longest shot runs 7.47 s to the end, 30.37 s, 80.3% of runtime, and there are no bursts. That contradicts the 1.8-3.5 s cut cadence in rule 10, but change still arrives every couple of seconds: cards enter and leave the field, and `strips/window-06-5.872s.jpg` shows a woman's card whipping in from the right edge while chips fade in ("Booking ticket"). The two cuts sit 0.63 s apart (6.84 s, 7.47 s). The first (`strips/window-07-6.773s.jpg`) returns to the three-mascot composition seen at 2.5-6 s; the second (`strips/window-08-7.407s.jpg`) goes to blank white.

## Look and type

The ground is white fading to pale blue at the bottom on every sampled frame (`look.json`/`metrics.json`: mean luminance 0.915 at frame 0, light share 1.0). Type is a black, medium-weight geometric sans, centred. Ink measurement at 720 px frame height: "In the last few weeks" 55 px (7.6%), "And we are" 59 px (8.2%) and "just getting started." 75 px (10.4%, descenders included). Titles are 7.6-10.4%; the upper end is above rule 3's 9% band, partly because of descenders. The legal line "Muse for 18+, N. America only" is 18 px, 2.5% of frame height, just under rule 2's 2.6% floor (`crops/legal.png`). There is no colour accent in the type; "Muse" shows a blue tint only while the opening title is building (`strips/window-08-7.407s.jpg`). Depth blur keeps one speaker sharp while side cards stay blurred (`f0009.jpg`, `f0013.jpg`).

## Product interface

The app itself never appears. What does appear are floating chat chips and artifact cards beside the speakers: "Your flights dropped from $350 to $270" with a "Tracking / Flights to Ojai" status (`f0007.jpg`), "Splitting nap times can help." with a "Baby Sleeping Plan, Artifact" card (`f0009.jpg`, `crops/artifact.png`), "20-Day Content Calendar, Artifact" (`f0013.jpg`), "Your brand kit is ready!" (`f0015.jpg`) and "Here's themes for your ideas." (`f0017.jpg`). Mascot chips at 6 s read "Shopping your items", "Spa day booked" and "Workout ready" (`crops/chips.png`, `crops/chip-spa.png`). Far-field chips are blurred decoration and at 720 p the small ones are unreadable; they become legible only when a card scales up near the camera (`f0014.jpg`, `f0018.jpg`). I rate phone-width legibility "partly". My 70% presence figure is an estimate from the sheets, not a measurement.

## Motion and transitions

Title text enters word by word with small vertical offsets: the opening title builds over about 1.2 s (`strips/window-08-7.407s.jpg`), the closing line over about 1 s (`strips/window-14-35.368s.jpg`). Once landed, the closing line stays still (`f0019.jpg`). Customer cards slide in from an edge, sharpen from blur into the foreground, then scale up and exit past the camera; the last card grows from a small blurred thumbnail at 31.7 s to near full frame at 34.6 s (`strips/window-13-31.698s.jpg`). Transition mix in `findings.json`: 2 hard cuts, about 10 slides, about 8 blur-to-sharp swaps, about 6 chip fades. The slide, swap and chip counts are my estimates. I did not measure easing curves.

## Copy on screen

Every spoken line is captioned in a white condensed sans on a grey pill, bottom-centre, from `f0001.jpg` to `f0018.jpg` (`transcript.md`: 104 words, 164.9 words per minute). The only authored lines are the title, "In the last few weeks you've had your Muse hard at work." (11 words over three lines), and the close, "And we are just getting started." (6 words over two). The closing line completes about 36.17 s and the film ends at 37.84 s, a hold of about 1.67 s, below rule 2's 2 s floor. The title hold I could not measure at a 2 s sampling interval.

## Sound

`audio.json` classifies the soundtrack as music (0.74 confidence), with speech scoring 0.716 and music 0.659 among the describe tags. Percussion scores 0.266, keyboard_musical 0.242 and synthesizer 0.213; the 99.3 BPM estimate has beat confidence 0.207, so I treat it as weak. Integrated loudness is -16.2 LUFS, short-term max -15.2, true peak -5.1 dBTP and loudness range 1.3 LU, so the mix sits 2.2 LU under rule 9's -14 LUFS target and barely moves. One of 2 cuts lands on a strong onset (0.5 vs chance 0.326); two cuts are too few to show any lock to the sound. Silence runs 36.895-37.834 s. I cannot name sound effects: disc_scratching scores 0.236, which does not support one.

## What to steal

1. Open on a real customer saying the product name in the first sentence, caption burned in, as in `f0001.jpg`.
2. Insert one imagery-free title card at about a fifth of runtime (7.5-9.5 s here) to state the premise in 11 words.
3. Keep one long shot and change by swapping cards in a depth field. This film does that for 30.37 s with two cuts, which contradicts rule 10's cut cadence.
4. Blur the far field and keep one speaker sharp so a crowded frame keeps a focal point.
5. Caption every spoken line in a fixed bottom-centre pill.
6. Fix what this film misses: hold the last line for at least 2 s, keep legal text at 2.6% of the short side or more, end on a name or URL, and master to -14 LUFS.
