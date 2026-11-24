# Review

You wrote the timeline, so you know what happens; the viewer sees it once, at full speed, often on a phone and often muted. Review is how you see the film as they will. `check` catches what is broken; this pass catches what is weak. You cannot watch video, but you can look at frames (rscb1DgJtNg), and every claim in the delivery note rests on a frame you opened or a number a command printed.

Run it after the first full build, after any edit that changes timing or layout, and before handing anything over.

## 1. Measure, then look

1. **Check.** `<skill>/scripts/hf.sh check --json` from the project. Fix every error. Its craft findings (in the JSON under `craft.findings`) are warnings worth reading one by one: a line on screen too briefly to read (`line_unread`), more than 3 s with nothing changing (`dead_stretch`), text under 2.6 % of the frame's short side (`text_below_floor`), an empty first frame (`first_frame_empty`), a film over 15 s with no sound (`film_silent`). Fix each one, or keep it on purpose and say why in REVIEW.md.
2. **Sheets.** `<skill>/scripts/hf.sh snapshot --review --json` writes a beat sheet (each scene at its start + 0.3 s and its middle, each `data-beat`), a strip across every cut, and a phone sheet at 360 px wide. Give scenes their own hosts or mark beats with `data-beat` so the sheet samples the moments that matter; with fewer than two scenes it falls back to evenly spaced frames and says so. Open all three images. Sample every beat in `timeline.json` as well as any fixed grid, and check each frame-based finding against the timeline before acting on it: on a 2 s grid, reviewers reported a passkey click as happening off screen and an end card as a bare logo for 3 s, when the timeline put the click at 20.6 s, in shot, and the bare logo at 0.3 s.
3. **Motion between the beats.** For the hero move and every transition, look at every frame from 0.3 s before to 0.3 s after: `scripts/hf.sh snapshot --range <start>,<end> --frames <0.6 x fps>` (18 frames at 30 fps, 36 at 60). For a move that must arc or land: `scripts/hf.sh keyframes --shot motion.png --selector '#<id>'`. A sheet of settled frames cannot show a jump, a frame where everything has faded at once, or a seam that pops; only a full-rate strip can, because one frame a second shows the before and the after and never how it happens (prompt-motion's fix guide).
4. **The rendered file.** `scripts/hf.sh render -q draft -o out/draft.mp4`, then `scripts/hf.sh audio out/draft.mp4 --json` for onsets and loudness (`sound.md` §7), and `scripts/hf.sh measure cuts out/draft.mp4 --json` to compare the film's actual cuts with the rhythm sheet in `SPEC.md`. Read the render log too: `Audio lowered by N dB to stay under −1 dBTP` means one sound overshot after AAC encoding and the whole film was turned down, with no error (`sound.md` §6).
5. **Pops and dead stretches.** `python3 <skill>/scripts/pop_scan.py out/draft.mp4` lists every frame whose change from the frame before is at least three times the change on both sides of it, and every run of near-stillness of 4 s or more. Match each pop to the timeline: a planned cut, a keystroke or a pose held on twos is fine (pass those spans to `--ignore`); anything else is a frame shown before its tween starts, two texts swapping, or a flood that changes half the frame in one frame. On motionflare's Linear film it found the one hard cut at 27.0 s and two small spikes; a typed headline produces one pop a keystroke by design.

Trust the numbers over your eye where they disagree: a clipped label or a 0.6 s line looks fine on a contact sheet.

## 2. What to look for

First, describe each beat frame in one sentence the way a stranger would, naming every object. An object you would have to explain ("those bars are mirrors") is a P0. Then read the beat frames in order: does a stranger follow them, each one causing the next? Compare each with its shot line in `SPEC.md`; what does not match is a note. Then name every default the frames show, from the BANNED list in `SPEC.md` or new, add each to that list, and fix those first.

Then go through the sheets once per question. For each, name what the frame shows that decides it (the element and where it is) before marking it pass or fail: an answer that could be written without looking, such as "fine", decides nothing. AI-Video-Factory moved its frame critic to this after free scores bunched at 4-6 out of 10 and named nothing to fix.

| Question | What it catches |
|---|---|
| Coverage | each numbered must-carry fact in `SPEC.md` is on screen, legible on the phone sheet, and held 0.5 s + 0.3 s a word; a missing fact is a P0 |
| Carrier | the CARRIER in `SPEC.md` is on screen at every seam and each transition hands it over; a seam with nothing carried across is a P1 unless the cut is the point |
| Finish | motion blur on the fast moves, grain visible at full size, a far layer softer than the subject, the ground alive, the frame rate in `SPEC.md` (`craft.md` §9) |
| Look | a still per scene against the look's reference frame: ground, ink, palette, lightness, colourfulness, line and grain (`looks.md`) |
| Facts inside the interface | every must-carry line that lives in a capture appears in some frame whole, at reading size, with no composer, toolbar or caption band over it; one that never does is a P0, whatever the captions say |
| Settled reading time | for each caption, the time from its last word landing to the start of its exit, against 0.5 s + 0.3 s a word; a start-to-end window overstates it for a line built word by word |
| Says less? | picture a plain, competent version of this brief: would it tell the viewer more? If yes, the film traded information for style, and that is a P0 |
| Does it read as what it is? | a shape that reads as another object, a material that reads as plastic, a product screen that reads as a mock-up |
| Does the subject separate? | subject and ground too close in value, two focal points in one frame, nowhere for the eye to go |
| Framing and contact | crops, text at the edge or under platform UI, collisions at a seam, things floating that should touch |
| Timing as a first-time viewer | a read shorter than 0.5 s + 0.3 s a word, something popping on with no move, a jump at a cut, everything on one curve |
| Rhythm | the energy curve in `SPEC.md` against the measured cuts: a hook inside 3 s, a burst, nothing static past about two bars outside a planned stop |
| Tells | items from `craft.md` §8 and the BANNED list on screen |
| The pictures alone | with the words covered, do the beat frames still tell the storyline? |
| The phone sheet | can every line meant to be read be read at 360 px? |
| The interface | every wide shot of a product screen that the voice or a caption depends on is zoomed until its working text reaches 2.6 % of the short side; a whole-window shot lasts 2-4 s and carries nothing the viewer must read |
| Claims and pictures | each claim the voice or a title makes has the picture that proves it on screen at the same time |
| The end card | the ask is on screen as text (a URL, a command or store badges), the last line holds at least 2 s, and the mark holds still for 3-5 s |
| Frame 0 and the last frame | frame 0 is a poster with the subject in it; the last frame can hold indefinitely |

## 3. Notes and fixes

Write each problem as one line: `t=4.2s · where · problem → exact change · what stays`. Rank them:

- **P0** breaks the read or the contract: unreadable, wrong, broken, or a tell in the hero shot.
- **P1** weakens the film: a dead stretch, a soft payoff, a seam that jumps.
- **P2** polish.

Fix every P0 and the P1s worth their time: text first, then timing, then detail. Then snapshot only what you changed, once. Run a second full pass only when a P0 is still open, and stop after that: a third round that finds nothing new is churn. Never score the film out of 10; a score finds nothing to fix. When a fix does not hold, snapshot the frames either side of the problem, list every difference, and change only the line that causes it. A film that feels busy: remove a third of the motion and keep the moves that lead the eye. When a fix gives something up (a line cut, a shot dropped), note what was given up.

**A fresh pair of eyes, at most once.** For a film over about 15 s, before the delivery render, you may give one subagent only `SPEC.md` and the three sheet images, and ask for P0 and P1 lines in the format above; keep the editing to yourself. Its value is the question it arrives with ("what is wrong with this?"), so do not use it to re-check your own fixes. Brief it as a viewer, not with this skill's rules: frames at full size, a manifest giving each frame's time, what should be on screen, the caption expected and the design reference it pushes in on, the audience, and the one thing the film must leave behind. Briefed that way, a single reviewer in the production run found the missing must-carry line that every rule-based pass had cleared (`evidence.md` §8). Ask it to end on SHIP or ONE MORE PASS with at most three concrete fixes; if you run a second pass on the fixed cut, give it the first report and ask for FIXED, PARTLY or STILL PRESENT per item, then new defects (motion-educator's verification format). Commit or copy the project first so a fix that makes things worse can be rolled back.

## 4. Before you hand over

Render the delivery file (`engine.md` §7), then confirm on that file, not the draft: duration, resolution and frame rate (`ffprobe`); an audio stream present unless the film is silent on purpose; loudness from `hf.sh audio`. Open the Studio preview (`engine.md` §6) so the user can keep editing, and give them the URL.

## 5. REVIEW.md

Write `REVIEW.md` at the project root, at most 25 lines, and put its short form (3-6 lines) in your reply:

- the storyline built and the two not built, each in one line;
- the creative calls you made and any default you kept on purpose, with the reason;
- what you measured (commands and their numbers) and what you only looked at;
- what nobody checked, always including "sound measured, not heard" and "motion judged from frames, not watched at speed"; when Claude and a motion designer ranked the same 13 videos for prompt-motion.com they agreed only moderately, and Claude could not tell competent films from great ones, so the reply asks the user to watch the film at full speed;
- the weakest shot and what you would change with more time;
- the replacement list: every placeholder or synthetic asset a real one should replace;
- which route rendered the film (HyperFrames version, or the design-craft fallback).

The next turn reads REVIEW.md before changing anything.
