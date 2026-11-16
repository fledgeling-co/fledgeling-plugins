# Build an App With Claude Design (COJAZQM1aeQ, 102.2 s, Claude)

## Hook and structure

Frame 0 is a poster with its subject in it: the presenter, in a framed box labelled `Claude-Design-Demo.mov`, with corner handles and a cursor on a light dotted canvas (f0001.jpg). The box grows from small to about 750 px wide during the first second (strips/window-01-0s.jpg). The hook is a joke pitch, spoken as "Me and my friend have this dumb idea" (transcript 00:00), and the product does not appear until t=40.7 s. The film runs in four parts: pitch and title card (0-17 s), presenter intro and problem (17-40 s), the product walkthrough (40.7-89.8 s) and the payoff (94-102 s). The hero moment is t=58 s, share 0.567, where five generated onboarding artboards appear beside the current screen (f0030.jpg, crops/artboards.png). The ending types "Claude makes it." into an editor, trims it to "it." (f0050.jpg) and lands on the logo at t=100 s, which holds 2.2 s (f0051.jpg).

## Rhythm

metrics.json gives 23 hard cuts, 13.5 cuts a minute and a median shot of 2.31 s. The mean shot is 4.26 s, and four shots run over 10 s. The longest, 9.38-29.12 s, is 19.75 s or 19.3 % of runtime. It holds because something on screen changes every few seconds: a title card is recoloured, a phone artboard is edited, a typed comment card grows ("Hi, I'm Na" at t=18, the full sentence by t=20, f0009.jpg to f0011.jpg). The only burst is 7 cuts between 73.42 s and 80.75 s, at a mid_share of 0.754, so it sits at about 72-79 % of the film rather than 30-60 %. It matches the narration listing steps: reply, prompt typing, coffee clip, Click-through artboard, Play (strips/window-54-73.334s.jpg, window-58-78.417s.jpg, window-60-80.667s.jpg). The cuts are not locked to the sound. The cut share on strong onsets is 0.13 against a chance share of 0.137.

## Look and type

The ground is a warm grey dotted canvas (f0001.jpg), cream at the end (f0051.jpg) and near-white inside the app. The light share is 0.882 and the dark share 0.0. Saturated colour appears only inside the designed artboards: sage, lavender, violet, yellow, sky blue and coral (f0030.jpg). The Claude starburst is the only accent on the closing card. The title card sets a serif in two lines, "How an Anthropic designer / uses Claude Design", with the last phrase in bold (crops/title.png). Measured at t=6 s with `hf measure ink`, line 1 is 57 px of 720 (7.9 %) and line 2 is 44 px (6.1 %). "Draw a picture" measures 51 px (7.1 %) at t=10 s and "Upload bird noises" 73 px (10.1 %) at t=14 s. The in-app headline "You're in. Go make bird noises." is 28 px (3.9 %) at t=84 s. The maximum is 4 words a line. Mockup type is a heavy grotesque, and filename labels above each frame are monospace. Outlines are black and about 3 px, with hard offset shadows on the buttons (crops/prototype-screen.png).

## Product interface

Real Claude app capture covers about 48 % of runtime (40.7-89.8 s), with real labels: "What's up next, Nate?", the folder list, "Silly onboarding designs", the "Sonnet 5.5 Medium" selector (f0022.jpg to f0028.jpg). The film punches in about 2x on the prompt box (f0024.jpg, f0025.jpg) and on the chat reply (f0038.jpg, f0044.jpg). Where it does not, the chat pane, sidebar and properties panel are small (f0030.jpg, f0037.jpg) and would not read at phone width. The designed screens do read: the prototype shows "Today you may only make bird noises.", the time picker "When should we bother you?" and a "CAWS TODAY 0" counter (f0041.jpg to f0043.jpg, crops/prototype-screen.png).

## Motion and transitions

Transitions follow the canvas metaphor. At 4.58 s the presenter frame slides up off the canvas to reveal the green title card (strips/window-03-3.667s.jpg). At 28.7-30.1 s the selected box scales to full frame (strips/window-22-28.709s.jpg). At 40.4-40.7 s the presenter clip blurs, shows a play icon and gives way to the app window (strips/window-30-40.375s.jpg). In between are 23 hard cuts, most following a click or typed action. Text enters by typing with a caret, and is then edited in place. "Draw a picture" is cut to "Dra" with a selection highlight at t=12 (strips/window-08-11.375s.jpg, f0006.jpg) and becomes "Upload bird noises" at t=14 (f0007.jpg). The title card changes from green to lavender after a cursor click on the swatch (f0003.jpg, f0004.jpg). I did not measure ease curves. The movement reads as ease-out over roughly 0.4-1 s from the strips.

## Copy on screen

Every line on screen is either the product's own text or a typed comment, with no separate captions. The lines I read from frames and crops: "How an Anthropic designer uses Claude Design" (7 words, about 4.8 s hold against 2.6 s needed), "Hi, I'm Nate. I'm a designer at Anthropic." (crops/comment.png shows the card mid-typing, "Hi, I'm Na"), "design a silly onboarding for this silly app. start from what we have currently, and do a series of designs for new ideas" (f0027.jpg, f0028.jpg), "Bigger bird. Much bigger. It should be uncomfortable." (f0033.jpg), "Bet you won't." (f0035.jpg), "ok claude. build it." (f0045.jpg) and "Claude makes it." (f0048.jpg). The tail of the closing line is "You steer i" at t=96 s (crops/closing-type.png), and I did not see its last frame. "Claude makes it." holds about 1.5 s against 1.4 s needed, and the logo 2.2 s against the 2 s minimum. The spoken words are a casual first-person script of 284 words at 166.7 words a minute (human captions).

## Sound

The film is presenter speech over a low music bed. audio.json tags music at 0.682, speech 0.680, keyboard_musical 0.449, synthesizer 0.413, percussion 0.342 and drum 0.269. At about 103 BPM with beat confidence 0.236, any pulse is faint. Sections change at 4.7, 19.9, 54.2 and 95.6 s, and the last starts under the ending. The integrated loudness is -24.5 LUFS, short-term max -22.5, true peak -7 dB and loudness range 2.6 LU. That is about 10 LU quieter than a -14 LUFS social master. I could not hear the film, so the sound effects are unchecked.

## What to steal

1. Put the speaker or hero footage on the product's canvas with a filename, handles and cursor, and let the product's editing gestures be the transitions (f0001.jpg, strips/window-22-28.709s.jpg).
2. Show the real product for each step and keep a screen only as long as its action takes (48 % of runtime; median shot 2.31 s).
3. Type the exact prompt on screen as it is spoken, with a 2x punch-in so the words read (f0025.jpg to f0027.jpg).
4. Edit a headline live so the edit carries the idea: "Draw a picture" to "Dra" to "Upload bird noises" (strips/window-08-11.375s.jpg).
5. A long talking shot of about 20 s works if text cards change every 2-4 s. Place the cut burst near the payoff (73.4-80.75 s) where the narration lists steps.
6. Close with the tagline typed, selected, trimmed, then the logo held 2.2 s.
7. Fix what this film misses: raise loudness toward -14 LUFS for social, and zoom in on small panels, which are unreadable at phone width in f0030.jpg.
