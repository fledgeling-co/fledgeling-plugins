# Projects are now a conversation with Claude (5qt_aGyAsKk)

An 82.7 s music-only feature explainer from Claude, 1280x720 at 24 fps. Transcript source: auto-generated captions, which hold only `[music]` tags and a few "Woo!" lines, so every claim below comes from frames, strips and measurements.

## Hook and structure

Frame 0 (`f0001.jpg`) is dark, with two grey chat bubbles in the middle: "click-through on the pricing page CTA has cratered. add an experiment with a few new styles before the 2.0 launch." and "cold start is 4s?? was under 1 last week". The subject is there from the first frame, though 86% of cells are blank (`frames.frame0`). By t=2 there are five tilted bubbles (`f0002.jpg`), and at t=4 an orange asterisk and "Untangling…" appear (`f0003.jpg`). A hard cut at 5.33 s lands the title (`f0004.jpg`). The film then runs: UI tour (7.25-17 s), a monospace plan diagram (18-36 s), the UI with a choice thread (38-60 s), a five-cut zoom burst to "Nothing is waiting on you" (60-65 s), a tagline (74 s) and the wordmark (77.4 s). The hero moment sits at t=62 (share 0.75), where the Overview panel resets (`f0032.jpg`).

## Rhythm

The film has 12 hard cuts, 8.7 per minute, median shot 4.17 s and mean 6.36 s (`rhythm`). The longest shot runs 7.25 to 41.33 s, 34.08 s or 41.2% of runtime. It is a continuous camera move across sidebar, project grid, chat, dot field and plan diagram. Cuts bunch into one burst of 5 in 4.7 s from 60.08 to 64.79 s, centred at 75.5% of runtime (`bursts`). Cut-to-music alignment is 0.083 on strong onsets against 0.114 chance, so the cuts are not locked to the sound. The pace comes from on-screen change inside long shots: bubbles added, ticks flipping from `[~]` to `[x]`, panels regrouping.

## Look and type

Everything sits on near-black (luma 19.2, saturation 0.005 in `metrics.look`). Title cards are pure black and the end card a lighter grey-black (`f0004.jpg` against `f0040.jpg`). Terracotta appears only on the asterisk, the working status and inline code chips (`f0003.jpg`, `f0021.jpg`). Titles are a serif with one bold word, "big". I measured line heights with `hf measure ink`: 52 px (7.2%) and 39 px (5.4%) for the title at t=6.5, 39 px (5.4%) for the tagline at t=76, and a 78 px (10.8%) lockup at t=78.7. The longest title line is 5 words. The plan diagram is monospace at about 22 px glyph height (t=15, 3.1% of frame height), above the 2.6% floor.

## Product interface

UI is on screen for about 46% of runtime (my count from frames 7.25-17 s and 37.5-65 s). The shots show a dark chat client with a Projects page, a chat column, a right-hand Overview and a thread drawer (`f0007.jpg`, `f0022.jpg`, `f0024.jpg`). The cursor is a large white arrow that lands on "Projects New" at t=10 (`f0006.jpg`). The sidebar badge reads "New" in `f0005.jpg` and "Beta" at t=12 (`f0007.jpg`), a small continuity slip. Wide shots carry 9-12 px text that would not survive a phone (`f0007.jpg`, `f0009.jpg`). The film solves that by zooming: at `f0024.jpg` the variants list is large enough to read, and `crops/bubbles.png` and `crops/terminal.png` confirm the copy verbatim. From 18 to 36 s the screen is an invented diagram of three sessions `//cta`, `//perf`, `//checkout`, each labelled "runs on" and "uses" (`f0016.jpg`). I could not confirm whether the UI is a real capture or a mock.

## Motion and transitions

Strips read: `window-01`, `04`, `06`, `17`, `28`, `40`, `50`, `51`. In `window-01-0.209s.jpg` the bubbles appear staggered and settle by about 1.3 s. At 5.33 s the cut is hard, bubbles to title (`window-04-5.25s.jpg`). The title's second line arrives by 6.0 s (`f0004.jpg`). Around 18 s the UI dissolves into a pixel-dither field (`f0009.jpg`). In `window-17-22.625s.jpg` the "Claude is working…" label drifts up while dashed lines draw down, and the plan diagram follows. At 41.79 s, `window-28` shows the Overview panel regrouping as threads move between sections. At 60 s `window-40` shows motion-blurred zooms into the checklist, which is the burst. At 76.83 s the tagline hard-cuts to a lighter ground (`window-50`), and `window-51` shows a dot grow into the asterisk, then "Cla", "Claude", "Claude Cod", "Claude Code" typed over about 1.2 s. Transitions are mostly hard cuts and zoom blurs, and each follows an on-screen action such as a reply or a completed thread.

## Copy on screen

Verbatim from crops: "Start your next big project with one little conversation" (9 words, visible about 1.9 s, `crops/title.png`); "Needs your eye: pick a CTA variant"; "A · Ink (recommended)… B · Glow… C · Card…" (`f0024.jpg`); "less might be more here. try a simpler version" (`f0027.jpg`); "D · Outline (your request): hairline border, tracked caps, terracotta sweep fill on hover. Quietest." (`f0028.jpg`); "i like D, the sweep fill is gorgeous!" (`f0030.jpg`); "Welcome back, Casey. Nothing is waiting on you." (`f0032.jpg`); "Claude runs the sessions. You make the calls." (`f0038.jpg`). The opening title is too brief for nine words: the rule asks 3.2 s and the film gives about 1.9 s (cut at 7.25 s). The tagline (8 words) holds at least 2.8 s, from `f0038.jpg` at 74 s to the cut at 76.83 s, against 2.9 s asked. The wordmark holds 4.2 s.

## Sound

The describe tags rank music 0.851, keyboard_musical 0.671, synthesizer 0.608, percussion 0.389, drum 0.377 and piano 0.375, so keys and synth over light drums is supported; drum_kit is 0.261 and electric_piano 0.25. The estimated tempo is 120.2 BPM, but beat confidence is only 0.357, so treat it as soft. Integrated loudness is -15.5 LUFS, short-term max -11.9, loudness range 5.9 LU, true peak -0.8 dBTP, which is above the -1 dBTP limit and 1.5 LU under -14. Four sections: A 0-22 s, B 22-35.6, C 35.6-73.3, D 73.3-82.7. Audio is silent from 78.6 s, so the final logo hold runs 4.1 s over silence. I found no evidence of separate sound effects.

## What to steal

1. Open with the user's own typed messages, typos included, so the problem is shown rather than named (`f0001.jpg`, `f0003.jpg`).
2. Tell one feature as a loop with a human decision in it: variants, a one-line reply, a new option, "i like D" (`f0024.jpg` to `f0030.jpg`).
3. Zoom UI until its text is large, and let the camera stay in one shot for long stretches when state changes constantly (7.25-41.33 s).
4. Explain mechanics with a monospace tick list rather than more UI (`f0015.jpg`).
5. Keep colour to one accent and let the ground stay near-black (`metrics.look`).
6. End on a morph: dot to asterisk to typed wordmark, held 4.2 s.
7. Give titles their reading time; this film's nine-word opener is the one clear miss, and the master loudness needs checking (-15.5 LUFS, -0.8 dBTP).
