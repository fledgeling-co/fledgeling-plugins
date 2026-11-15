# Review

You wrote the timeline, so you know what happens; the viewer sees it once, at full speed, often on a phone and often muted. Review is how you see the film as they will. `check` catches what is broken; this pass catches what is weak. You cannot watch video, but you can look at frames (rscb1DgJtNg), and every claim in the delivery note rests on a frame you opened or a number a command printed.

Run it after the first full build, after any edit that changes timing or layout, and before handing anything over.

## 1. Measure, then look

1. **Check.** `<skill>/scripts/hf.sh check --json` from the project. Fix every error. Its craft findings (in the JSON under `craft.findings`) are warnings worth reading one by one: a line on screen too briefly to read (`line_unread`), more than 3 s with nothing changing (`dead_stretch`), text under 2.6 % of the frame's short side (`text_below_floor`), an empty first frame (`first_frame_empty`), a film over 15 s with no sound (`film_silent`). Fix each one, or keep it on purpose and say why in REVIEW.md.
2. **Sheets.** `<skill>/scripts/hf.sh snapshot --review --json` writes a beat sheet (each scene at its start + 0.3 s and its middle, each `data-beat`), a strip across every cut, and a phone sheet at 360 px wide. Give scenes their own hosts or mark beats with `data-beat` so the sheet samples the moments that matter; with fewer than two scenes it falls back to evenly spaced frames and says so. Open all three images.
3. **Motion between the beats.** For the hero move and every transition: `scripts/hf.sh snapshot --range <start>,<end> --frames 8`. For a move that must arc or land: `scripts/hf.sh keyframes --shot motion.png --selector '#<id>'`. A sheet of settled frames cannot show a jump, a frame where everything has faded at once, or a seam that pops; only a range can.
4. **The rendered file.** `scripts/hf.sh render -q draft -o out/draft.mp4`, then `scripts/hf.sh audio out/draft.mp4 --json` for onsets and loudness (`sound.md` §6), and `scripts/hf.sh measure cuts out/draft.mp4 --json` to compare the film's actual cuts with the rhythm sheet in `SPEC.md`.

Trust the numbers over your eye where they disagree: a clipped label or a 0.6 s line looks fine on a contact sheet.

## 2. What to look for

First, describe each beat frame in one sentence the way a stranger would, naming every object. An object you would have to explain ("those bars are mirrors") is a P0. Then read the beat frames in order: does a stranger follow them, each one causing the next? Compare each with its shot line in `SPEC.md`; what does not match is a note. Then name every default the frames show, from the BANNED list in `SPEC.md` or new, add each to that list, and fix those first.

Then go through the sheets once per question:

| Question | What it catches |
|---|---|
| Coverage | each numbered must-carry fact in `SPEC.md` is on screen, legible on the phone sheet, and held 0.5 s + 0.3 s a word; a missing fact is a P0 |
| Says less? | picture a plain, competent version of this brief: would it tell the viewer more? If yes, the film traded information for style, and that is a P0 |
| Does it read as what it is? | a shape that reads as another object, a material that reads as plastic, a product screen that reads as a mock-up |
| Does the subject separate? | subject and ground too close in value, two focal points in one frame, nowhere for the eye to go |
| Framing and contact | crops, text at the edge or under platform UI, collisions at a seam, things floating that should touch |
| Timing as a first-time viewer | a read shorter than 0.5 s + 0.3 s a word, something popping on with no move, a jump at a cut, everything on one curve |
| Rhythm | the energy curve in `SPEC.md` against the measured cuts: a hook inside 3 s, a burst, nothing static past about two bars outside a planned stop |
| Tells | items from `craft.md` §8 and the BANNED list on screen |
| The pictures alone | with the words covered, do the beat frames still tell the storyline? |
| The phone sheet | can every line meant to be read be read at 360 px? |
| Frame 0 and the last frame | frame 0 is a poster with the subject in it; the last frame can hold indefinitely |

## 3. Notes and fixes

Write each problem as one line: `t=4.2s · where · problem → exact change · what stays`. Rank them:

- **P0** breaks the read or the contract: unreadable, wrong, broken, or a tell in the hero shot.
- **P1** weakens the film: a dead stretch, a soft payoff, a seam that jumps.
- **P2** polish.

Fix every P0 and the P1s worth their time: text first, then timing, then detail. Then snapshot only what you changed, once. Run a second full pass only when a P0 is still open, and stop after that: a third round that finds nothing new is churn. Never score the film out of 10; a score finds nothing to fix. When a fix does not hold, snapshot the frames either side of the problem, list every difference, and change only the line that causes it. A film that feels busy: remove a third of the motion and keep the moves that lead the eye. When a fix gives something up (a line cut, a shot dropped), note what was given up.

**A fresh pair of eyes, at most once.** For a film over about 15 s, before the delivery render, you may give one subagent only `SPEC.md` and the three sheet images, and ask for P0 and P1 lines in the format above; keep the editing to yourself. Its value is the question it arrives with ("what is wrong with this?"), so do not use it to re-check your own fixes. Commit or copy the project first so a fix that makes things worse can be rolled back.

## 4. Before you hand over

Render the delivery file (`engine.md` §7), then confirm on that file, not the draft: duration, resolution and frame rate (`ffprobe`); an audio stream present unless the film is silent on purpose; loudness from `hf.sh audio`. Open the Studio preview (`engine.md` §6) so the user can keep editing, and give them the URL.

## 5. REVIEW.md

Write `REVIEW.md` at the project root, at most 25 lines, and put its short form (3-6 lines) in your reply:

- the storyline built and the two not built, each in one line;
- the creative calls you made and any default you kept on purpose, with the reason;
- what you measured (commands and their numbers) and what you only looked at;
- what nobody checked, always including "sound measured, not heard" and "motion judged from frames, not watched at speed";
- the weakest shot and what you would change with more time;
- the replacement list: every placeholder or synthetic asset a real one should replace;
- which route rendered the film (HyperFrames version, or the design-craft fallback).

The next turn reads REVIEW.md before changing anything.
