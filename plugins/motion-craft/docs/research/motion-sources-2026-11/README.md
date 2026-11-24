# Motion sources study, 2026-11-24

What six sources show about films that look professional, and what changed in motion-craft 0.4.0 because of it. The rules themselves are in `skills/motion-craft/references/`; `evidence.md` §9 there summarises this record.

## What was studied

| Source | What was read or measured |
|---|---|
| [staryone/motlab](https://github.com/staryone/motlab) | Both skills (`motlab`, `motlab-assets`), every reference, the docs and the page runtime |
| [ersinkoc/AI-Video-Factory](https://github.com/ersinkoc/AI-Video-Factory) | The motion-film director prompt and schema, the film lint, the frame critic's checklist, the style, typography and shot-intent docs |
| [zeative/motion-educator](https://github.com/zeative/motion-educator) | The skill and its 11 references; its 13 sample films measured |
| [prompt-motion.com](https://prompt-motion.com) | All 240 gallery entries (videos and their prompt pages), its six guides and two templates; every video measured, contact sheets made for the top 40 and 10 of them opened |
| [motionflare.ai/showcase](https://motionflare.ai/showcase) | The 21 motion-graphics films, measured and opened as contact sheets. Its 21 Film-mode commercials come from a video model, which motion-craft does not make, and were skipped |
| [getcaruso.com](https://www.getcaruso.com/en-au) | The two homepage films; the investor-relations and private-equity pages carry no video files, so their 15 animated canvases were recorded in Chromium at 30 fps for 14 s each and cropped to each canvas |

## Method

- Cuts and shots: `hyperframes measure cuts` (0.9.52, telemetry off).
- Stillness, light share and colourfulness: frames at 10 a second, 160 px wide; a frame counts as still when its mean difference from the one before is under 0.6 of 255, and as light when its mean luma is over 128. Colourfulness is Hasler and Süsstrunk's measure, median over one frame a second.
- Looking: contact sheets of one frame every 0.5-1.25 s opened at full size, plus 8-frame strips at larger size for the Caruso loops.
- Prompts: word counts and tags parsed from each entry's page. The prompt texts belong to their creators and are not copied here; each row links to its entry.
- The downloaded films, the Caruso recordings and the contact sheets are kept beside this file in `media/`, which git ignores (about 3 GB). Gallery films are named by the `rank` in `prompt-motion-gallery.jsonl`.

## Measurements

The 240 gallery films, all made with Claude Opus 5.5 (per-film rows in `prompt-motion-gallery.jsonl`):

| Group | Films | Cuts a minute | Median shot | Light frames | At 60 fps | With sound |
|---|---|---|---|---|---|---|
| All | 240 | 14.4 | 2.5 s | 30 % | 137 | 208 |
| Prompt of 26 words or fewer | 136 | 12.9 | 2.9 s | 27 % | 65 | 121 |
| Prompt of 100 words or more | 24 | 6.0 | 6.4 s | 62 % | 17 | 21 |
| One viral showreel prompt or a close variant | 73 | 24.0 | 1.9 s | 30 % | 58 | 69 |
| Gallery top 40 by popularity | 40 | 12.0 | 2.2 s | 62 % | 28 | 37 |

Popularity reflects the poster's audience and timing as much as the film, and long prompts come from more practised creators, so neither split proves cause. What the numbers do show is the shape of the default: an undirected prompt gives a dark, fast-cut montage.

The 21 motionflare films (`motionflare-showcase.jsonl`): 15 s vertical or 30 s landscape, 20 at 60 fps, all with sound, a median of 2 hard cuts per film, 13 with two or fewer, and no still stretch longer than 3.6 s.

Caruso (`caruso.json`): the homepage films run 112 s and 75 s at 2.1 and 0.8 cuts a minute, stand still for 74 % and 78 % of their runtime, and hold one frame for up to 7.0 s and 4.5 s. The interface loops stand still for 71-96 % of their recordings, moving in short bursts between reading holds.

motion-educator's 13 sample films: 3.4-13.4 cuts a minute (one film, 41 s, has no cut at all), no still stretch longer than 2.6 s, 11 of 13 on its dark house stage.

## What changed in the skill

| Finding | Where it went |
|---|---|
| Each product film built on its brand's own signature device | `direction.md` §2; `looks.md` §1 |
| The best-received films carry one element through every seam | `direction.md` §4-5 (CARRIER); `review.md` §2 |
| Undirected films default to dark, fast-cut montage; a new default look to ban | `story-and-rhythm.md` §4; `direction.md` §5 |
| A finishing pass: motion blur, 60 fps, grain, light, depth | `craft.md` §9; `engine.md` §7; `formats.md` |
| Screen-studio framing, slow push through holds, nothing appearing from nowhere, exits before entries | `craft.md` §3, §5 |
| Transition builds: flood and contract, shape becomes the shot, foreground through the camera | `craft.md` §6 |
| Six looks written as numbers | `looks.md` |
| The agent card narrated by a status pill | `saas-films.md` §3, §12; `formats.md` §7 |
| Recorded effects placed by onset or peak, levels by role, spacing and variation | `sound.md` §3-4; `scripts/sfx/samples.py` |
| Single-frame pop scan, full-rate transition strips, evidence before each verdict, verification format | `review.md` §1-3; `scripts/pop_scan.py` |
| Browser traps from the gallery's gotchas | `engine.md` §4 |

## What nobody checked

- Every film was judged from frames by one model; none was watched at speed by a person, and no sound was heard.
- The gallery's popularity order was taken as published; likes were not re-fetched.
- The new rules have not yet been run through `evals/` against a no-skill film; the last blind evaluation is from 0.2.0.
