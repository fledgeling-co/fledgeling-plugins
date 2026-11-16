# Claude Cowork is now your Chrome side panel (C-5wF6tkQ2Q, 41.24 s, Claude)

## Hook and structure

Frame 0 is a finished poster (`f0001.jpg`): one line of near-black serif on warm cream, "Claude Cowork is now your Chrome side panel", centred. The ink is 48 px tall in a 720 px frame, 6.67% (`$HF measure ink` at t=0.5 s). The subject is named, but the product is not on screen yet. The title holds about 2.25 s. Its words then leave one at a time, left to right, over about 0.7 s (`strips/window-02-2.125s.jpg`, 2.25 to 2.96 s). The frame is blank at 2.96 s and a hard cut at 3.0 s lands on a browser window.

The film runs in eleven beats. Setup runs 3 to 5 s. The click on the Claude toolbar icon is at 5.9 s (`strips/window-05-5.875s.jpg`). The side panel slides in at 7.1 to 8 s. The prompt is typed at 10 to 12 s (`f0006.jpg`, `f0007.jpg`) and sent at 14.4 s. Claude then works through tabs at 18 to 22 s (`f0010.jpg` to `f0012.jpg`). The reply and spreadsheet arrive at 28 to 30 s (`f0015.jpg`, `f0016.jpg`). The hero moment is the finished Invoice Log at t=30 s, 73% of runtime. The CTA runs about 33 to 37 s and the logo takes 37 to 41.24 s. The panel the title promises first appears at about 7.2 s, so the product payoff is slow.

## Rhythm

`metrics.json` gives 6 hard cuts at 3.0, 5.08, 5.96, 7.17, 14.5 and 19.33 s. That is 8.73 cuts a minute and a median shot of 3.0 s, and `bursts` is empty. Four of the six cuts fall in the first 4.2 s. After 19.33 s the detector sees one shot of 21.9 s (53% of runtime), so the rest of the film is paced by camera moves and UI state changes rather than cuts. Roughly 72% of runtime shows product UI.

## Look and type

There are two grounds. Cream carries the title, CTA and logo. A muted sage plate with faint wavy lines sits behind every product scene (`f0003.jpg`, `f0010.jpg`). All 21 sampled frames are light (`light_share` 1.0). Coral appears only on Claude elements: the toolbar asterisk, the send button, the spinner and the logo mark (`f0006.jpg`, `f0020.jpg`). The Claude tab group gets an orange outline (`f0004.jpg`).

Type is a high-contrast serif in sentence case, one line, no accent word. Measured ink heights:

| Line | Time | Height | Share of frame |
|---|---|---|---|
| Title | 0.5 s | 48 px | 6.67% |
| CTA | 35 s | 49 px | 6.81% |
| Logo lockup | 39 s | 78 px | 10.83% |


## Product interface

The UI is staged: fictional vendors, `.example` domains and invented invoice figures. It is still the real Claude look, and it fills the frame. The camera keeps picking a different scale for each job. The toolbar crop makes the 14 px icon in `f0003.jpg` about 60 px in `f0004.jpg`. The prompt is shown large enough to read (`f0007.jpg`: "Run my month-end close on these tabs. Pull each invoice and get it into the monthly report."). A pale red edge glow and a "Stop Claude" pill show the agent acting on a page (`f0010.jpg` to `f0012.jpg`). The log arrives with Pending, Overdue, Paid and Due today pills (`crops/table-status.png`).

Legibility at phone width is partial. The chat reply (`crops/reply.png`) and invoice rows are about 13 px, 1.8% of frame height, below the 2.6% floor. They work as texture. The readable facts are the title, the prompt and the CTA.

## Motion and transitions

The cuts are caused by action on screen. The cursor reaches the toolbar and the film cuts to a close crop at 5.08 s (`strips/window-04-4.292s.jpg`). The click is at 5.9 s, with the cut to the panel at 5.96 s (`strips/window-05-5.875s.jpg`). The send click at 14.4 s is followed by a cut at 14.5 s (`strips/window-11-14.417s.jpg`). Between cuts the camera does the work. From 8.2 to 10 s it pushes from the panel down to the message box (`strips/window-07-8.167s.jpg`). Panels slide in from the right at 7.1 s and about 29 to 30 s. Tab swaps under the red glow show a brief white wash (`strips/window-15-19.25s.jpg`, 19.3 to 19.7 s). I did not open the strips for the 22 to 24 s switch to the desktop window.

The end builds on a shared mark. The CTA lifts about 22 px and leaves at 36.75 to 37.0 s. A coral dot appears at 37.04 s, grows into the asterisk by about 37.6 s, and the wordmark types in letter by letter by about 37.9 s (`strips/window-25-36.75s.jpg`, `strips/window-26-37.5s.jpg`).

## Copy on screen

On-screen copy is minimal. Only two lines are written for the film: the title ("Claude Cowork is now your Chrome side panel", 7 words) and the CTA ("Try it now: claude.com/chrome", 4 words, `crops/cta.png`). The rest is the product's own text. The title holds about 2.3 s against 2.6 s from the rule, roughly on the line. The CTA holds at least 2.8 s (`f0018.jpg` at 34 s to 36.75 s) against 1.7 s by rule. The 17-word prompt has only 2.4 s in the large crop, but it stays in the chat bubble for 10 s or more after the send.

## Sound

There is no speech. The tool found no caption track, and local whisper returned only "Music" cues at 0 to 2 s and 30 to 38 s. `audio.json` reads the kind as music at about 128 bpm (beat confidence 0.547) in two sections, A 0 to 5 s and B 5 s to the end. Describe tags are brass_instrument 0.59, trombone 0.515, trumpet 0.463, percussion 0.388, orchestra 0.381 and drum 0.377. Loudness is integrated -15.4 LUFS against the -14 target, so about 1.4 LU quiet. Short-term max is -13.4, true peak -1.5 dBTP (inside the -1 limit) and loudness range 6.5 LU. Silence runs from 39.735 s to the end, under the held logo. Cut-to-onset share is 0.167 against 0.057 by chance, 0.11 above. That is 1 of 6 cuts, so I treat the cuts as not locked to the sound. I did not hear it.

## What to steal

- Cut after the cursor, to a crop on its target. Each cut here has a visible cause (5.08, 5.96, 14.5 s).
- Make the target about 5% of frame width before the click, not 1%.
- Dissolve a title card in reading order over about 0.7 s, then cut at once to the product.
- Show the agent working through state: red glow, a Stop pill and tab hops, no words (`f0010.jpg`).
- Finish on a real artifact, the ten-row log, and let tiny UI text be texture only when a larger crop has already carried the key line.
- End: a 4-word CTA held at least 2.5 s, a mark built from a dot, a 3.3 s logo hold, and silence for the final 1.5 s.
- Bring the promised panel in sooner than 7.2 s.
