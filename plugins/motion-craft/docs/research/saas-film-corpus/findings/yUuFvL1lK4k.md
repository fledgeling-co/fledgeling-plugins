# Mods in Claude Code: change how Claude Code works (yUuFvL1lK4k)

A 200.6 s Claude tutorial: an on-camera presenter opens, a desktop-app screen recording carries the next 192 s, and a logo card closes.

## Hook and structure

Frame 0 is the presenter's face, mid-word, filling the frame (`f0001.jpg`; frame0 luminance 0.30, contentfulCells 0.2). The caption track puts the promise in the first two seconds: "We just added mods to Claude Code and with a mod, you can directly change how Claude Code itself works" (transcript 00:00-00:02). There is no title card or caption in the first 5.7 s (`strips/window-01-0.1s.jpg`).

The cut to the app lands at 5.71 s (`strips/window-04-5.639s.jpg`). From there the film is one long walk with these beats:

- Three examples: context bar, agents panel, email hiding (11-36 s).
- The anatomy of a mod: plugin.json, hooks.json, register.tsx (36-62 s).
- The three arguments `$`, `e`, `next` (62-122 s).
- Loading the mod (122-136 s).
- Building the email mod (136-166 s).
- Proof (166-190 s) and sharing (190-197 s).

The email example is announced at 00:29 and rebuilt at 02:16, so the film opens and closes on the same item. The payoff frames are `f0088.jpg` (t=174 s, masked email) and `f0091.jpg` (t=180 s, real address used in the command). The ending is the install command, then a 3.2 s logo card (`f0100.jpg`, cut at 197.43 s).

## Rhythm

The film cuts three times (5.71, 121.72 and 197.43 s), which is 0.9 cuts per minute with a median shot of 40.71 s (`metrics.json` rhythm). The longest shot runs 116.02 s, 57.8% of runtime. There is no burst and no flash. 63.6% of the 2 s samples are static, with a 28 s static run ending at 102 s (`frames.intervals_static_share`, `longest_static_run_s`). Pace comes from a virtual camera that zooms and re-centres about every 2-6 s on whatever the narrator names, not from edits. The presenter is on camera for only the first 5.7 s (2.8% of runtime). Speech runs 734 words in 200.6 s, about 220 words per minute.

## Look and type

The ground is near-black (dark_share 0.99): a dark chat and editor window floating on a cream desktop with a soft shadow (`f0004.jpg`). The presenter shot is warm brown; the logo card is cream with a coral starburst (`crops/logo.png`). The accent is coral (diamond bullets, starburst) plus a green "9%" pill and a six-colour segmented bar (`crops/context-bar.png`).

Measured text heights against the 720 px frame:

| Text | t (s) | Height | Share of frame |
|---|---|---|---|
| "Claude Code" wordmark | 199 | 82 px | 11.4% |
| Zoomed code line `on('ui.render'…` | 62 | 27 px | 3.75% |
| "Tool timeline" label | 6.5 | 10 px | 1.4% |

There are no written titles. The only large type is the wordmark. Whole-window chat and sidebar text is 10 px or less at 1280 wide, readable only after zoom (`crops/timeline.png` was needed at 2x).

## Product interface

Real UI is on screen for about 93% of the runtime, with a real cursor (`f0043.jpg`, `f0088.jpg`). The cursor selects, and the camera follows it. Content is real product text: a tool timeline with timings "0.2s / 1.1s / 42 ✓" (`crops/timeline.png`), an agents panel with seven rows, each with a "run" button (`crops/agents.png`), and a context breakdown "90k of 1M · compacts at 987k" (`crops/context-bar.png`). `crops/plugin-json.png` shows the manifest as plain editor text.

The UI has its own motion. "context measuring…" fills into a bar (`f0010.jpg` to `f0013.jpg`), a command menu appears while "/agents-" is typed (`strips/window-13-24.291s.jpg`), and a "running · 2s" spinner runs on one agent (`f0016.jpg`). The hover reveal itself is never shown, only the masked state (`f0088.jpg`), so the film's stated payoff is told, not shown. Phone-width legibility is partial: zoomed frames pass, full-window frames fail.

## Motion and transitions

Transitions are of four kinds: hard cut (3, at 5.71 s, 121.72 s, 197.43 s), continuous camera move (zoom to a line, for example `f0028`-`f0031` and `f0037`), UI state change (chat clears at 12.65-13.11 s, `strips/window-09-12.646s.jpg`), and a zoom-to-blur into a terminal at 121.7 s (`strips/window-44-121.421s.jpg`). Each is caused by something on screen or in narration: the cut at 5.71 s lands when the presenter finishes the promise, and the blur arrives as the loading method is introduced. Dimming non-focus lines to a low contrast leaves one focal point per frame (`f0040.jpg`, `f0049.jpg`). Easing curves were not measured; the moves read as eased with soft settles in the strips.

## Copy on screen

No copy is written for the film. Every line is product text: "clean up the old build and rerun the tests", "Cleared the old build output and reran the suite. All 42 tests pass." (`crops/timeline.png`), "hide-email: reloaded (1 hook: ui.render)" (`crops/chat-masked.png`), "write Sam a short thank-you message" (`f0091.jpg`), and the wordmark "Claude Code" (`crops/logo.png`). Holds follow the narration and run 4-12 s per line, so the 0.5 s + 0.3 s a word rule is exceeded everywhere. The last line, the wordmark, holds 3.2 s, above the 2 s floor. Caption word count is 734, and nothing on screen restates the jargon the narrator speaks fast ($send, middleware, next).

## Sound

Transcript source is human captions (en). Voice dominates: kind "voice", integrated -15.8 LUFS, short-term max -14.4, true peak -2.7 dBTP, loudness range 1.9 LU (`metrics.json` sound). That is about 1.8 LU quieter than the -14 LUFS target, with 1.7 dB of true-peak headroom to spare. No steady beat was found (bpm null, confidence 0.003). Describe tags: speech 0.873, music 0.489, plucked_string_instrument 0.232, keyboard_musical 0.205; the two instrument tags sit just above 0.2, so a quiet bed is possible but unconfirmed, and no genre is named. Typing is 0.161, below the naming threshold. Cuts are not locked to the sound: 0.0 of cuts land on strong onsets against a chance share of 0.072. Silences occur at 103.36-103.64 s, 182.45-182.77 s and 199.58-200.63 s. I could not hear the film; all of this is from measurements.

## What to steal

- Start with the speaker already talking, and put the promise in the first 2 s (`f0001.jpg`).
- Keep one long continuous screen shot and move a virtual camera: zoom to about 3x on the named token and dim everything else (`f0043.jpg`). This is the film's main device.
- Announce the examples first, then build one of them later; the loop gives structure to a 3 minute explainer.
- Prove a limit as well as a claim: the masked email, then the command that still uses the real one (`f0088.jpg`, `f0091.jpg`).
- Give the screen its own motion (measuring bar, typing, spinner) so static stretches still change.
- Close on a quiet logo card held at least 3 s (`f0100.jpg`).
- Avoid: window-level text below 12 px, and a promised payoff (hover) that is never shown. Also avoid 28 s runs where nothing changes (`longest_static_run_s`).

Not checked: audio itself, music presence beyond describe tags, easing values, strips after 157 s, and the terminal install frame between samples.
