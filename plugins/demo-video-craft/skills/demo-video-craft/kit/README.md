# The kit

The engine of a delivered series (an overview of 1:41 and nine shorts of 21-25 s, made picture-first in HyperFrames
for an AI connector shown inside Claude and ChatGPT), with two series built on it: an example for a new product, and
the delivered series itself as a reference. How close a new series comes to that one depends on these values far more
than on any description of them, so a series starts from this code rather than from a blank page.

```bash
python3 scripts/new_series.py ./acme-videos --fetch          # the kit into _kit/, the example series beside it
python3 scripts/new_series.py ./guardian --reference --fetch # or the reference series (kit/reference/README.md)
cd acme-videos
python3 states.py && open states/index.html                  # every screen on one page: look before building scenes
python3 films.py                                             # the film table: every film's length, the gates
export MOTION_CRAFT_SCRIPTS=<motion-craft base directory>/scripts
python3 _kit/engine/build.py . K01 --mute-only               # before the voice exists
(cd films/K01 && "$MOTION_CRAFT_SCRIPTS/hf.sh" check && "$MOTION_CRAFT_SCRIPTS/hf.sh" snapshot --at 0.3,5,10,19 --no-end)
python3 _kit/engine/render.py . --to delivery site/films     # with the voice: build, render, remux, gate, publish
python3 _kit/site/build_site.py . --posters                  # the overview and shorts pages, posters, share image
```

`--fetch` downloads what the kit does not ship, at pinned versions: Inter, Inter Tight (and Newsreader for the
reference) as Google Fonts' own Latin files, the ones the source series rendered with, and GSAP 3.15.0.

## What it holds

| File | Whose | What it does |
|---|---|---|
| `runtime/kit.js` | engine | K.play: window scenes as step lists over live HTML states: the camera, the cursor, the evidence marks, typing into a chat or any field, captions |
| `runtime/kit3.js` | engine | K3.stage: stage scenes (the opener, the architecture, the end slide): arrivals, moveTo, wires across or down, flowing dots, the focus walk |
| `runtime/kit.css`, `kit3.css` | engine | the films' chrome: ground, windows, the product's own app and phone frames, cursor, marks, labels, captions, the lockup bar |
| `runtime/frame.css` | half and half | the chat-host frames (keep) and an example product's cards and side-panel views (replace with your product's own kit) |
| `engine/films_engine.py` | engine | step helpers, `intro_scene` / `outro_scene` (landscape and portrait), `pace`, `settle_push`, the label switch, the length gate, the project writer |
| `engine/states_engine.py` | engine | the chat-host window (`frame`, `register_host`), the product's own window (`app`: browser, desktop, phone), the card, row, tool line and panel builders, the lockup, the sprite, the banned-name check |
| `engine/build.py`, `score.py` | engine | one film's project at its canvas size, both timelines, the narration gates, captions, the two soundtracks (a paid bed, the procedural groove, or effects only) |
| `engine/render.py` | engine | step 6 in one command: build, render once, remux the voiced cut (with the film's limiter), check sizes, publish only on a pass |
| `site/build_site.py` | engine | the overview and shorts pages, player, shorts modal, posters, share image, cache headers and robots.txt, from `site.json` |
| `example/` | an example series | a fictional product in Claude (O, K01), in its own browser window (K02) and on a phone at 9:16 (K03) |
| `reference/` | the delivered series | its ten films' screens and film table, ported unchanged; the kit rebuilds them as published |

A series' own files are `series.json`, `states.py`, `films.py`, `lines.json`, `respell.json`, `lockup.css`, `marks/`,
`theme.css` and `site.json`. When you change the engine for one series, change it in that series' `_kit/`, and say in
`SERIES.md` which fork is live. Carry a fix that would have helped any series back to this kit.

## The defaults it carries

These are the source series' measured values; `references/picture.md` says where each came from and when to move it.
The camera frames into the full 1920x1040 stage at 0.62 of its width for a chat exchange, 0.7 for a card and 0.9 for
the composer, capped at 0.92 of its height and 3.2x; on a 9:16 canvas it frames into the area every vertical platform
leaves clear. Prompts type at 52 characters a second and hold 0.6 s before the press. Every scene slows by one pace
factor (1.3 for the overview, 1.22 for the shorts, 1.15 for the opener), with per-op motion capped at 1.25x and travel
at 1.2x. A short's last frame push runs from max(last frame + 1.4 s, end - 4.6 s) at fill x 1.07, under a 3.2 s lockup
bar. The press ring is 64 px.

## How it was checked

The example's four films build and pass `hf.sh check` with 0 errors; its K01 short renders at 1080p60 with 0 pops and 0
still runs (`evals/run_kit_example.sh`). The reference series' ten films rebuild at a mean SSIM of 0.9994-0.9998 against
the published files, lowest frame 0.9985 (`kit/reference/README.md`).
