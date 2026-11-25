# The starter kit

The engine of a delivered series: an overview of 1:41 and nine shorts of 21-25 s, made picture-first in HyperFrames
for an AI connector shown inside Claude and ChatGPT. Its brand, client and content have been taken out; what is left
is the code and the numbers that made it look and move the way it did. Start a series from it rather than from a blank
page, because how close a new series comes to that one depends on these values far more than on any description of
them.

```bash
python3 scripts/new_series.py ./acme-videos --fetch     # the kit into _kit/, the example series beside it
cd acme-videos
python3 states.py && open states/index.html            # every screen on one page: look before building scenes
python3 films.py                                       # the film table: prints every film's length, fails past the caps
export MOTION_CRAFT_SCRIPTS=<motion-craft base directory>/scripts
python3 _kit/engine/build.py . O --mute-only           # before the voice exists; drop --mute-only after gateway_audio.py
(cd films/O && "$MOTION_CRAFT_SCRIPTS/hf.sh" check && "$MOTION_CRAFT_SCRIPTS/hf.sh" snapshot --at 0.3,5,13.5,20,29 --no-end)
```

`--fetch` downloads the three files the kit does not ship, at pinned versions: Inter and Inter Tight (SIL Open Font
License) and GSAP 3.15.0. The example builds two films, checks clean in `hf.sh check`, and renders: its short came out
at 1920x1080 60 fps, 20.3 s, -14.0 LUFS, 0 pops and 0 still runs in `pop_scan.py`, `delivery: PASS 1/1`.

## What is engine and what is the series'

| File | Whose | What it does |
|---|---|---|
| `_kit/runtime/kit.js` | engine | K.play: window scenes as step lists over live HTML states; the camera, the cursor, the evidence marks, every window op |
| `_kit/runtime/kit3.js` | engine | K3.stage: stage scenes (the opener, the architecture, the end slide): arrivals, moveTo, wires and flowing dots, the focus walk |
| `_kit/runtime/kit.css`, `kit3.css` | engine, with tokens to set | the films' chrome: ground, windows, cursor, marks, labels, the lockup bar, the client's deck theme (`--cl-*`) |
| `_kit/runtime/frame.css` | half and half | the host frames (keep) and an example product's cards and side-panel views (replace with your product's own kit) |
| `_kit/engine/films_engine.py` | engine | step helpers, `intro_scene`, `outro_scene`, `pace`, `settle_push`, the length gate, the project writer |
| `_kit/engine/states_engine.py` | engine | the host window, the product's card, row, tool line and panel builders, the banned-name check, the sprite |
| `_kit/engine/build.py`, `score.py` | engine | one film's project, both timelines, the narration gates, the two soundtracks |
| `series.json` | series | product, lockup words, the ask, fonts, voice paths, music beds, host marks, pace factors, length caps |
| `states.py` | series | every screen, in the product's markup, with one scenario's names and figures |
| `films.py` | series | the film table: scenes, steps, effect beats, voice placements |
| `lockup.css`, `marks/` | series | the one source for the brand lockup and every mark, read by the films and the site alike |
| `lines.json`, `respell.json` | series | the narration and how the voice must say names (`scripts/gateway_audio.py lines`) |

When you change the engine for one series, change it in that series' `_kit/`, and say in `SERIES.md` which fork is
live. Carry a fix that would have helped any series back to this kit.

## The defaults it carries

These are the source series' measured values; `references/picture.md` says where each came from and when to move it.
The camera frames into the full 1920x1040 stage at 0.62 of its width for a chat exchange, 0.7 for a card and 0.9 for
the composer, capped at 0.92 of its height and 3.2x. Prompts type at 52 characters a second and hold 0.6 s before
the press. Every scene slows by one pace factor (1.3 for the overview, 1.22 for the shorts, 1.15 for the opener), with
per-op motion capped at 1.25x and travel at 1.2x. A short's last frame push runs from max(last frame + 1.4 s, end -
4.6 s) at fill x 1.07, under a 3.2 s lockup bar.
