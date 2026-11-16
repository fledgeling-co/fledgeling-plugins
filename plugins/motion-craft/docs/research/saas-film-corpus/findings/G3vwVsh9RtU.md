# G3vwVsh9RtU: Claude Fable 5.1 builds the ops review in Slack (85.5 s)

## Hook and structure

Frame 0 (f0001.jpg) is a beige desktop with blue folders ("Q3 Materials", "Past Reviews"), a half-faded Slack toast from Fabian and a cursor. It is not black and not a lone logo. By t=2 s the toast is sharp over a blurred desktop (f0002.jpg), and at 3.7 s it gains a second line: "Any chance you can have the deck by 8AM?" (f0003.jpg). The problem is shown as a person's message, not named in a caption, and it lands inside 3 s.

The film then runs eleven beats: a title card at 6.1 s ("Let Claude handle more", f0004.jpg); Vickie typing her ask and @-mentioning Claude (8.6-16.4 s); teammates dropping files with Claude's emoji reactions (16.4-24 s); a gridded canvas where the agent reads (24-55 s); an "ISSUE DETECTED" turn and Vickie's decision, "Take the second report. Split the spend 40-60." (f0030.jpg); the finished deck (65-71 s); a share to #leadership-team (71-78 s); a tagline; and the logo. The hero moment is the deck landing with three reaction pills and confetti at about 70 s (f0036.jpg, share 0.82).

## Rhythm

metrics.json gives 19 hard cuts, 13.33 per minute, a median shot of 0.83 s and a mean of 4.28 s. Those numbers hide two very different regimes. One burst holds 13 of the 19 cuts between 37.62 s and 41.79 s, centred at 46% of the runtime (bursts[0].mid_share 0.464). The longest shot then runs 29.33 s, 34.3% of the film (41.79-71.12 s). The first cut is at 6.12 s. So the film is a hybrid: slow state changes, one short burst, one long continuous move. The 1.8-3.5 s cut rhythm is not what drives it.

## Look and type

The film is light: 97.7% of sampled frames are light and none are dark (frames.light_share 0.977), with a mean saturation of 0.056 (look.saturation). The ground is warm beige for the title cards, white for Slack panels and a grid-paper beige for the work section. The one saturated element is a coral-red line, drawn by hand, that runs through f0018.jpg to f0034.jpg, plus the coral starburst on status labels and the logo.

Titles are a serif on a plain card. `hf measure ink` gave: "Let Claude handle more" 47 px at t=7.5 s (6.5% of the 720 px frame); the tagline lines 59 px and 46 px at t=80 s (8.2% and 6.4%); the wordmark 60 px at t=84 s (8.3%). The title range is 6.4-8.3%, inside the 4-9% rule. The longest title line is 5 words ("Fable 5.1 runs bigger projects."). crops/title1.png confirms the title text verbatim.

## Product interface

The UI is on screen for most of the film (about 88% of runtime by my estimate from the sampled frames). It is Slack, redrawn or captured cleanly: channel header "# august-ops-review", the "Claude AGENT" tag, file cards ("August ops review.pptx", "PowerPoint Presentation"), emoji pills (f0035.jpg). The cursor is a stylised outline with a hand-drawn feel (f0006.jpg). Messages and file names are large and legible (f0007.jpg). In the work section the card sub-labels ("read · variables logged", f0021.jpg) are about 10-14 px high at 720p, which is roughly 1.4-1.9% of frame height and under the 2.6% floor. The table and log text inside the iris (f0019.jpg, f0020.jpg) reads only at full size. I could not tell whether the Slack UI is a capture or a redraw.

## Motion and transitions

Text enters gently. The title fades in word by word over about 0.4 s (strips/window-03-6.042s.jpg, 6.125-6.54 s). Slack messages fade up from a blur. The wordmark builds letter by letter (f0042.jpg, "Clau", then f0043.jpg, "Claude").

Transitions are caused by something on screen. A vertical streak leaves the reactions at about 24 s (f0013.jpg). A circular iris opens as the agent starts reading the spreadsheet (strips/window-19-37.542s.jpg, 37.5-38.7 s). A horizontal whip streak carries the message into #leadership-team at 73.4 s (strips/window-41-73.375s.jpg). The long section (41.8-71.1 s) is a continuous pan following the red line past stacked file cards (strips/window-23-41.792s.jpg). The cut to the title at 6.12 s is a hard cut from a UI card to a flat card (strips/window-03-6.042s.jpg). The tagline cuts straight to a starburst dot at 82.125 s (strips/window-48-82.042s.jpg). I did not measure ease curves.

## Copy on screen

All copy is the UI itself plus two cards. The title "Let Claude handle more" holds about 2.1 s (4 words; the rule asks 1.7 s). The tagline "Fable 5.1 runs bigger projects. You still run the show." holds about 3.7 s (9 words; the rule asks 3.2 s). Agent status labels are short and italic: "Analyzing data...", "Understanding incidents...", "Channel analysis complete", "ISSUE DETECTED: Conflicting totals for Week 2 spend! Flagging to the team." (crops/issue.png). Long messages are not meant to be read in full: the "Done" message is 35 words and is on screen for about 3 s (f0035.jpg), well under an 11 s read. Holds come from 2 s samples and strips, so they are approximate.

## Sound

No speech: the transcript tool found no caption track and local whisper returned only repeated "Music" lines, so source is `none`. The audio kind is music (audio.json). Describe tags: keyboard_musical 0.589, synthesizer 0.573, percussion 0.534, drum 0.493, piano 0.352, electric_piano 0.345, drum_kit 0.33. BPM is 110.1 with beat confidence 0.54, so treat it as approximate. Integrated loudness is -19.3 LUFS, short-term max -15.6, true peak -0.2 dBTP, loudness range 5.5 LU. That sits under the -14 LUFS social target and above the -1 dBTP ceiling. Cuts on strong onsets are 0.158 against a chance share of 0.061, a gap of 0.097, which is under 0.10: the cuts are not locked to the sound. A silent tail runs 83.685-85.514 s under the logo. I cannot hear the film, and I have no evidence about sound effects.

## What to steal

- Show the problem as a named person's message inside the product UI at 2-4 s (f0003.jpg).
- Hold a 9-word tagline for 3.7 s, then build the wordmark, then leave about 1.8 s of silence.
- Run one hand-drawn accent line through the long section so a 29 s move has a spine (f0018.jpg to f0034.jpg).
- Put a human decision in the middle of the machine's work (f0030.jpg) and pay it off in the tagline.
- Use a short burst (13 cuts in 4.2 s at 46% of runtime) and follow it with one long calm shot.
- Do not copy the loudness (-19.3 LUFS, -0.2 dBTP), the sub-2.6% card text, or cuts that miss the music.
