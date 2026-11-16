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

## 4. SaaS product film corpus (48 films, 2026-11-16)

48 product films the owner picked as good examples, each studied by one headless Claude Sonnet 5.5 analyst: transcript through the router's yt-transcript MCP, the film downloaded at 720p or lower, one frame every 2 s on labelled contact sheets, native-rate strips around on-screen events, HyperFrames cut, event, look and loudness measurements, be-my-witness's looking protocol with 2x crops, and `measure ink` on title lines. Two of the films (en0GuyhieQk, To5nrYqvR44) are the reference films of section 3, now read in full. The method, the tools, every analyst's findings and the measured table are in `docs/research/saas-film-corpus/`. It is the source of `skills/motion-craft/references/saas-films.md` and of the rules marked with it.

| Id | Brand | Title | Length | Cuts a minute | Median shot | Loudness |
|---|---|---|---|---|---|---|
| -OH1y7CjIew | Claude | Coding on the go with Claude Code | 242 s | 7.9 | 5.5 s | -14.2 LUFS |
| 5qt_aGyAsKk | Claude | Projects are now a conversation with Claude | 83 s | 8.7 | 4.2 s | -15.5 LUFS |
| 7-1tNo8HAwk | Claude | New agents for legal professionals / Claude Cowork | 25 s | 0.0 | 25.2 s | -17.1 LUFS |
| C-5wF6tkQ2Q | Claude | Claude Cowork is now your Chrome side panel | 41 s | 8.7 | 3.0 s | -15.4 LUFS |
| COJAZQM1aeQ | Claude | Build an App With Claude Design | 102 s | 13.5 | 2.3 s | -24.5 LUFS |
| G3vwVsh9RtU | Claude | Claude Fable 5.1 builds the ops review in Slack | 86 s | 13.3 | 0.8 s | -19.3 LUFS |
| S9IJ1GgAAxE | Claude | Claude Fable 5.1 runs the forecast overnight | 74 s | 5.7 | 3.6 s | -16.1 LUFS |
| SkFmiMHDN38 | Claude | How an Anthropic engineer uses Claude Docs | 83 s | 9.4 | 4.6 s | -17.0 LUFS |
| SkpwzfR4A1E | Claude | Claude's new mobile app updates are here | 152 s | 6.3 | 8.2 s | -13.2 LUFS |
| To5nrYqvR44 | Claude | Meet Claude Slides, Claude Design and Claude Docs | 95 s | 11.4 | 2.5 s | -15.0 LUFS |
| XNbc2HhL7J4 | Claude | Claude Cowork: coming to mobile and web | 81 s | 8.9 | 2.8 s | -12.0 LUFS |
| YUYeHMsqbmY | Claude | Introducing Claude Meetings | 63 s | 11.5 | 2.7 s | -15.4 LUFS |
| YewAJPawE7I | Claude | Introducing Claude Whiteboards, Sheets, and Data | 58 s | 1.0 | 28.9 s | -15.5 LUFS |
| _f_rtbW_uFM | Claude | Getting started with Claude Tag | 179 s | 3.0 | 6.1 s | -14.0 LUFS |
| bVXiNb9RyyI | Claude | How an Anthropic designer uses Claude Slides | 104 s | 8.6 | 3.2 s | -25.7 LUFS |
| en0GuyhieQk | Claude | Introducing Claude Dashboards and Claude Motion | 82 s | 5.9 | 4.8 s | -15.9 LUFS |
| idJQMJwHtyM | Claude | Claude for Google Workspace™ | 60 s | 5.0 | 3.3 s | -15.4 LUFS |
| jKRl_CSVxyI | Claude | Using Claude Opus 5.5 as your daily driver | 212 s | 5.7 | 8.0 s | -16.0 LUFS |
| kJA3fQnntpY | Claude | Collaborate on artifacts in Claude | 160 s | 1.9 | 9.1 s | -15.8 LUFS |
| lCR9epzSNGc | Claude | Claude Opus 5.5 builds daydreams that hold together | 86 s | 8.3 | 4.3 s | -19.8 LUFS |
| mQZB0l-rhxE | Claude | Building verification loops in Claude Code | 188 s | 8.6 | 4.8 s | -23.9 LUFS |
| omihvjf0A2k | Claude | Getting started with Claude Code Projects | 273 s | 9.2 | 3.8 s | -23.7 LUFS |
| tYOI-WoLS_o | Claude | Delegate and schedule tasks in Claude Cowork | 257 s | 4.2 | 4.7 s | -16.5 LUFS |
| yUuFvL1lK4k | Claude | Mods in Claude Code: change how Claude Code works | 201 s | 0.9 | 40.7 s | -15.8 LUFS |
| 4tlIHJqGiRc | Harvey | Introducing Memory | 81 s | 5.2 | 3.5 s | -14.1 LUFS |
| 7M5TXyoJ-Jc | Harvey | Create and Edit Files in Harvey | 54 s | 1.1 | 27.0 s | -14.0 LUFS |
| B87ICNnr_GQ | Harvey | Harvey’s Legal AI Is Now Inside Microsoft 365 | 151 s | 4.0 | 4.6 s | -14.7 LUFS |
| Bn9Vv8e_WPk | Harvey | Harvey Mobile with Voice for iOS and Android | 19 s | 3.1 | 9.5 s | -13.3 LUFS |
| Jw6l1jgNVw8 | Harvey | Run End-to-End Legal Work with Harvey Agents | 67 s | 4.5 | 5.9 s | -13.9 LUFS |
| KLMl0ug_oK0 | Harvey | Introducing Command Center | 79 s | 4.6 | 4.2 s | -11.2 LUFS |
| TVbOAMAxC4Y | Harvey | How Harvey Graph Helps Deliver More Accurate Legal Work | 290 s | 0.6 | 9.9 s | -22.8 LUFS |
| _Qxh2NZcWuY | Harvey | Harvey’s Partnership with ElevenLabs | 23 s | 0.0 | 23.4 s | -13.5 LUFS |
| arDCe_F8vfk | Harvey | Harvey for Innovation Teams: Lead Firmwide AI Transformation | 109 s | 3.9 | 5.8 s | -13.9 LUFS |
| bOeWJRfYWWY | Harvey | Introducing Contract Intelligence | 50 s | 7.2 | 5.4 s | -19.1 LUFS |
| dUIuvfP2j2c | Harvey | Email Harvey and Get Answers On the Go | 26 s | 18.4 | 1.6 s | -22.7 LUFS |
| fFQM0LHOGBc | Harvey | Build Your Own Legal AI Agents with Harvey Workflow Builder | 177 s | 8.2 | 3.5 s | -24.2 LUFS |
| mTzRvY38xGw | Harvey | Visualize Legal Data on Demand in Harvey | 32 s | 17.1 | 0.4 s | -12.3 LUFS |
| o5PmFp8HYTM | Harvey | Stay in Flow From Document Intake to Final Deliverable | 51 s | 2.4 | 4.0 s | -14.4 LUFS |
| vD-iFCwmozc | Harvey | Harvey for Outlook: Draft, Summarize, and Respond with AI | 40 s | 1.5 | 20.1 s | -13.6 LUFS |
| vlwlzyBqgvc | Harvey | Introducing Command Center | 55 s | 9.7 | 4.5 s | -20.7 LUFS |
| wzrBFx0ONZg | Harvey | Create Tailored Legal Agents with Agent Builder | 40 s | 3.0 | 17.8 s | -13.9 LUFS |
| xDiG-MN7GzU | Harvey | Memory Is Now In Harvey | 68 s | 3.5 | 7.2 s | -16.0 LUFS |
| ydIT4EdLK54 | Harvey | Harvey Platform Overview | 232 s | 2.9 | 8.9 s | -14.1 LUFS |
| LrXnOKCr0mo | Muse | Introducing Spaces in Muse | 90 s | 10.0 | 4.5 s | -19.0 LUFS |
| We8BTITLvb4 | Muse | Introducing Muse: your personal AI agent | 83 s | 5.8 | 4.8 s | -16.0 LUFS |
| XO244jk7xH4 | Muse | Meet Muse: your personal AI agent | 120 s | 40.0 | 1.4 s | -17.2 LUFS |
| _E9c5P4EyhU | Muse | How people are using Muse | 38 s | 3.2 | 6.8 s | -16.2 LUFS |
| kuxha-8IHCQ | Muse | Plan your big day, make a space. | 61 s | 14.8 | 1.9 s | -16.3 LUFS |
