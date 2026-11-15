# Research corpus for motion-craft

Read 2026-11-15. Every rule in `skills/motion-craft/` traces to a row here or to `skills/motion-craft/references/evidence.md`.

## 1. Video transcripts (18 read in full, YouTube auto or human captions)

| Id | Title | What it contributed |
|---|---|---|
| hbPvZvpu9KU | The New Claude Motion Is Awesome | Data-to-animation from a spreadsheet; screenshots of a film you like as the style input; SRT transcript to time graphics to speech; "you barely read that before it goes" as the commonest fix |
| en0GuyhieQk | Introducing Claude Dashboards and Claude Motion (Anthropic) | The reference film itself: dashboard → narrative, comment-to-edit, export to design tools |
| Eg08Lr3zqdw | Claude MOTION is Unreal for Video | Agree a plan and detailed prompt before building; tweaks panel lists every word, scene length, speed; comment on one element changes only it; code cannot make photoreal footage, so pair with an image/video model; storyboard-first then hand scenes to a video model |
| RSe268YFglA | Create FREE Motion Graphics with Claude Code + Javascript | The one-line prompt gives the same generic look; a real brief = role (director, animator, composer, sound designer) + banned list (no centred text, no default gradients, no generic fade-ins) + colours, fonts, spacing + a storyboard gate; reference film: "steal the rhythm, not the footage", pull frames with ffmpeg; music written in code with a visualiser reading its beat |
| Cft-TBQv_Y4 | I Tested Claude Motion vs. Claude Code for Motion Design | Professional motion designer's comparison; have Claude write the prompt first, then add a screenshot of a style you like; a library of approved frames as the starting point; Claude Motion's clips are silent; first try often plain, dark and empty; "every time it fixes something, it tells you what it had to give up" |
| yf2OwchM9nw | Claude Just Dropped MOTION | Tweaks and comment tools explained; code vs pixels; blend generated footage with code motion for a premium look |
| oTWUyW_bR-g | Insane GitHub Repos To 10x Claude Video Editing | Survey of huashu-motion, Take One, reanimate, Argo, explainroo, video-director, earshot: music-first cutting, hook in 3 s, a pause before the biggest moment, independent cold reviewer up to three rounds, layout and loudness checks |
| qZqZ02AsYiA | New Claude Motion is Insane | Screenshots as the strongest input; a brand's palette from a website screenshot; real images included in the film |
| AsvN_feasyY | How To Make Insane Motion Graphics With Opus 5.5 | References, brand assets and direction are "90% of the work"; iterate by locking what works and naming the one change |
| rscb1DgJtNg | Claude Now Does Video (FOR FREE) Thanks To JavaScript | The engine in one paragraph: a function of time t returns one picture; a headless browser draws each frame; ffmpeg stitches; Claude can check any frame. Effort level matters less than the prompt; storyboard before code; contact-sheet loop before calling it done |
| aD9X6Lc3dVk | 10 GitHub Repos to 10x Your AI Motion Graphics | three.js for 3D charts and particles, pixel FX, Blender MCP for real 3D, physics (Rapier), post-processing (glow, depth of field, grain), librosa beat sync, prompt packs of styles |
| cDb-wPq0Iyk | Claude Opus 5.5: How To Make Motion Graphics | Twelve tips from two weeks of testing: real high-resolution logo and UI assets; numbered storyboard approved first; every shot transforms into the next, no cross-dissolves; keep the focal point in one place; always some motion; visuals first, sound last; shallow depth of field; words slide up one after another, no bounce; write voiceover to the finished length; single light source in 3D |
| FJZkfjM8WhI | How To Make Insane Video Editing With Opus 5.5 | Talking-head edit: script + raw clip + references; pacing of the first 5 s and headline size are the usual notes |
| LlwhNla5eQg | Anthropic Just Dropped Claude Motion, Dashboards + More | Data CSV → explainer; a stronger result came from a reference film plus a step-by-step breakdown of it |
| v1Gwa1KyUaI | Claude FINALLY Unlocked AI Motion Graphics | One paragraph of direction ("deep navy, warm highlights, everything eases in like it has weight, numbers count up") separates a moving slide from a designed piece; describe feel, not milliseconds |
| T17ifmBD_6s | Claude Motion WITHOUT a Team Plan | The same film from Claude Design artifacts on Pro/Max; renders took 28-48 minutes; Sonnet results unusable for this |
| mJ6ZvGiwZEc | Claude Motion Explained | Under the hood all routes are the same: a page where each frame is a function of time, a headless browser screenshot per frame (300 for 10 s at 30 fps), ffmpeg; Remotion free until a company has four people; HyperFrames free and open source |
| IFL9MLPDN_U | How to Create Actually Useful Motion Graphics With Claude | Professional editor's sceptic view: something should change every 1-3 s in long-form; the useful cases are inside an editor workflow; often faster by hand for simple text |

To5nrYqvR44 has no caption track; it was studied as frames (section 3).

## 2. Open-source motion skills (all read at their SKILL.md and main references)

| Repo | Licence | What it contributed |
|---|---|---|
| whaleyxbt/claude-motion | MIT | `timeline.json` as the single clock for picture, sound and review; easing and spring tables with numbers; reading holds; review loop with beat contact sheets taken 0.3 s after each beat; pure-stdlib procedural sound engine mastered to −14 LUFS; web sims with `render(t)` pure in t captured frame by frame |
| alchaincyf/huashu-motion | MIT | Director method: read the product, message shape, five personality sliders, three directions differing in language or material, treatment with rhythm sheet, four stills and continuity chain; rhythm measured on 21 launch films (cuts every 1.8-3.5 s, a burst of 5-8 cuts at ~37 % of length); taste rules from 142 films; comment-to-edit loop |
| alchaincyf/huashu-art-motion | MIT | Shot list before code; camera as punctuation (slow push for transition, fast push only for accents, push in then come back out); six ways a film goes wrong (PPT page-flip, copied demo, no concrete object, dead background, drawing what real material exists for, the AI look) |
| Leonxlnx/earshot | MIT | An agent cannot hear; measure sound (LUFS, onsets, sync per cut) and read a sound sheet before claiming a mix works |
| NiazMorshed2007/reanimate | MIT | Clone a reference's motion: capture frames, write a motion spec table (trigger, start, duration, from → to, easing), rebuild, capture the clone the same way, compare, iterate 2-5 rounds |
| vincentsch/explainroo | MIT | Narration first: script → local voice → word timings (Whisper) → each picture appears on a spoken word; check layout, loudness and intelligibility before handover |
| heygen-com/hyperframes | Apache-2.0 | Motion numbers measured from its launch films (eases by role, springs by damping ratio, exits 40-50 % shorter, overlap 30-50 %, stagger, holds 0.5 s + 0.3 s a word, title 4-9 % of frame height); transitions with a cause; story beats with shares; spec template turning adjectives into numbers; BANNED-by-default list grown after each render; P0/P1/P2 review notes and REVIEW.md |

## 3. Reference films measured frame by frame (2026-11-15)

Downloaded at 640×360, one frame a second tiled into contact sheets. Hard cuts measured with `hyperframes measure cuts` (frame-to-frame difference). A first pass with ffmpeg's scene score above 0.28 found only 11 and 1 cuts respectively; the scene score misses cuts between similar frames, so the HyperFrames numbers are the ones used.

**en0GuyhieQk, Anthropic's Claude Motion launch (82 s).** 8 hard cuts in 82 s (5.9 a minute), median shot 4.75 s, and a 32-second unbroken stretch from 10.3 s to 42.1 s: a continuous spine with few cuts. Opens on the result (a 3D city of bike docks with real labels and a running clock, 6:10 → 7:05 am), pulls back to reveal it is a video in a player, then a presenter in frame with information cards growing beside him, a dashboard that becomes the 3D grid, the process stated as type on a curved path ("Tracing every morning ride from the hilltop to downtown"), the comment-to-edit loop shown in product, and an ending where app icons burst out around one Export button.

**To5nrYqvR44, a product film the owner chose as a good example (95 s).** 20 hard cuts (12.7 a minute), median shot 2.13 s: an unbroken 20.6-second opening, then nine cuts between 24 and 37 s and six between 42 and 58 s, plus three fast moves the measure lists apart from cuts. A continuous spine broken by two bursts. Frame 0 is a full sentence, not a logo. The words of the title turn into product chips inline. Real product UI throughout with a cursor doing real clicks. Shot scale swings from whole window to extreme close-ups of one toolbar and one Share button. One asset (a jacket and its line "Rain is a given") is carried through deck, social sizes and document. A motion-blurred whip (1:24) carries into the closing line "Claude makes it. You steer it.", typed by two labelled cursors, then the mark holds about four seconds.
