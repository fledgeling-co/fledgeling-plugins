# Introducing Claude Dashboards and Claude Motion (en0GuyhieQk, 81.6 s, Claude)

## Hook and structure

Frame 0 is the payoff, not a setup: a full-frame 3D miniature city with a "6:10 am / Typical weekday" chip and two white labels, "Fernhill 21 bikes" and "Canal Street 6 bikes" (f0001.jpg, crops/hud.png). The Fernhill label pops in within 0.25 s (strips/window-01-0s.jpg). By t=2 s that same picture shrinks into a video-player frame with a scrub bar (f0002.jpg), and the presenter says "This is a short animation about empty bike docks" (transcript.md, 00:00-00:02). The hook lands inside 3 s.

After that the film runs as a story told in a player: the dashboard scrubs back at t=4 s (strips/window-03-4.042s.jpg), a presenter appears at t=6 s (f0004.jpg), a title card at t=10 s (f0006.jpg), and a comment joke at 14-24 s (f0009.jpg to f0012.jpg). The product beats begin late: data-source logos at 24-27 s (f0013.jpg), the Claude chat creating the dashboard at t=28 s (f0015.jpg), the map comment at t=40 s (f0021.jpg), the finished 3D film from 47 to 58 s (f0025.jpg to f0029.jpg), comments and export from 58 to 77 s, and the logo at 77.7 s. The hero is the 3D film around t=54 s (share 0.66, f0028.jpg).

## Rhythm

metrics.json gives 8 hard cuts, 5.88 cuts per minute, a median shot of 4.75 s and a mean of 9.07 s, with no burst (bursts is empty). The longest shot runs 10.29 to 42.08 s, 31.79 s or 38.9 % of the runtime, and is a continuous dashboard and comment scroll. Change inside long shots comes from UI state: comment cards grow, logo tiles slide, the scrub bar fills (f0009.jpg to f0012.jpg). This contradicts the 1.8-3.5 s launch cadence and the burst rule: the film holds attention with a story, not with edit speed. Only 5 % of sampled intervals are static (intervals_static_share 0.05), though the ending holds 4 s still (longest_static_run_s 4).

## Look and type

The ground is cream with a faint dot grid (f0003.jpg), near-black outlines on every container, and a restrained palette: dusty pink title card, amber, teal, coral (look.json saturation 0.06, luma 221). The 3D film is the only deep scene, with long shadows and a depth blur (f0001.jpg, f0028.jpg); inside the player everything is flat.

Type is a serif for titles, the tagline and the logo, a condensed bold grotesque for the film's clock and labels, a plain sans for interface text, and monospace for the filename above the player. Four title lines measured with `hf measure ink`: "Introducing" 44 px (6.11 % of 720) and "and Claude Motion" 38 px (5.28 %) at t=11 s, "You steer it." 41 px (5.69 %) at t=76 s, and the Claude wordmark 60 px (8.33 %) at t=78.5 s. That is a 5.28-8.33 % range, inside the 4-9 % rule. Title lines are at most 3 words, and the highlighted "Claude Dashboards" is the single accent (f0006.jpg, crops/title.png).

## Product interface

The interface is on screen for roughly 75 % of runtime (estimate from sheets 1-3), shown as real app captures (chat panel and Share button, f0015.jpg), simplified redrawn player chrome, and floating comment cards. The cursor is stylised: a hand with a dark outline (f0003.jpg) and a pointer arrow (f0036.jpg).

Legibility is mixed. The dashboard captions and axes are about 8-11 px tall in a 720 px frame and unreadable at phone width (f0016.jpg), but the six KPI numerals 445K, 2,999, 21%, 4,200, 71%, 92 are large (crops/kpis.png). The film solves the rest by scaling fragments up: the prompt box fills about 520 px of the 1280 px frame with 24 px text (f0021.jpg, crops/prompt.png), and comment cards sit at a similar scale (f0010.jpg, f0034.jpg).

## Motion and transitions

Transitions are caused by a cursor or a click. The player scrubs back at 4 s (the rewind glyph at the right of strips/window-03-4.042s.jpg), a comment sent at 59.2 s lets the chat panel slide in over the film (strips/window-41-59.209s.jpg, strips/window-43-61.667s.jpg), and the film shrinks into the player at 2 s. One hard cut at 42.08 s swaps the map card for the text card "Projecting dashboard coordinates into a 3D city grid", which then reveals word by word (strips/window-30-41.959s.jpg). The tagline "Claude makes it. You steer it." is selected in an edit box with a toolbar (strips/window-50-73.542s.jpg, crops/edit.png shows the Export button), and the logo builds letter by letter at 24 fps (strips/window-53-77.709s.jpg). The camera in the 3D film drifts, then drops to street level at the dock row (f0028.jpg to f0029.jpg).

## Copy on screen

Copy is long where it must be read and short where it labels. The 30-word prompt "Create a dashboard from a year of our ride data..." (f0015.jpg) and the 33-word map comment (crops/prompt.png) are the longest lines; the voice reads the same content, so the on-screen text acts as a caption. Quoted verbatim: "Hold on the empty dock a beat longer so it lands." (f0031.jpg); "Can we name the van route here? Ops will ask." (f0034.jpg); "Claude makes it. You steer it." (f0036.jpg to f0039.jpg). Build steps read "Tracing every morning ride from the hilltop to downtown" (f0024.jpg). Holds are estimates from the 2 s samples: the title holds about 4 s (f0006.jpg, f0007.jpg), above the 0.5 s plus 0.3 s a word rule; the prompt box holds about 3.5 s for 33 words, below that rule, because the narration carries it. The last line, the logo, holds about 3.6 s, above the 2 s rule.

## Sound

The film is on-camera presenter speech over music. Auto captions give 212 words in 82 s, about 155 words a minute, with [music] tags at 13 s and through to 75 s. audio.json describe tags: speech 0.744, music 0.678, keyboard_musical 0.381, percussion 0.357, synthesizer 0.287, mallet_percussion 0.249, glockenspiel 0.2, piano 0.198. Those support a light mallet and keys bed, nothing more; the 171.8 bpm estimate has confidence 0.379, so I do not use it. Integrated loudness is -15.9 LUFS, short-term max -13.9, true peak -1.2 dBTP, loudness range 3.7 LU: peak is inside the -1 dBTP limit, integrated loudness is 1.9 LU under the -14 target. cuts_on_strong_onset_share is 0.25 against chance 0.147, 10.3 points above, on 8 cuts, so cuts are only weakly locked to sound. Silence spans between 78.8 and 81.6 s mean the logo sits in near-silence.

## What to steal

1. Open on the finished output, then shrink it into an interface frame so the demo and the hook are the same image (f0001.jpg, f0002.jpg).
2. Use one container for every scene, so cuts read as state changes: 8 cuts in 82 s.
3. Scale a UI fragment until it fills about 40 % of the frame width where it must be read (f0021.jpg); do not show the whole dashboard and hope.
4. Give each colour one job: amber the problem, teal the contrast, coral only for Claude-owned buttons (f0017.jpg, f0035.jpg).
5. End on a typed tagline and a letter-by-letter logo that holds 3.6 s on a clean ground (strips/window-53-77.709s.jpg).
6. Skip the 24 s presenter intro (t=4-24 s) and the unreadable dashboard scroll (f0016.jpg).
