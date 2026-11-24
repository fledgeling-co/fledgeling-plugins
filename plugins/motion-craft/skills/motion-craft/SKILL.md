---
name: motion-craft
description: >-
  Make short videos from code: animated explainers, launch and feature films, data stories from a spreadsheet or dashboard, logo stings and title cards, lower thirds and other transparent overlays, vertical social clips, product demo films, 3D or simulation pieces, exported as MP4, WebM, MOV or GIF. It does what Claude Motion does, with open tools: HTML compositions rendered frame by frame through HyperFrames run locally, plus a procedural sound engine. Use it whenever someone asks for a motion graphic, an animated video, "a video like Claude Motion makes", a promo or launch video, an animation explaining something, a chart or number that animates into a clip, a sting or intro, a reel or short, or wants a film retimed, re-edited or remade in another film's rhythm, even when they never say "motion". A director first: it reads the product and its real material, generates many different ideas from even a one-line request (isolated ideation branches through trawl and a bank of devices measured from real films), writes three storylines that differ in mechanism and a numeric spec with a banned-defaults list before building, designs the rhythm around one carried element and the subject's signature device, adds sound, applies a finishing pass, reviews contact sheets, full-rate transition strips and phone-width frames against craft numbers measured from more than 300 films, and leaves the film editable through variables and stable element ids. NOT for in-page UI animation or a web page that animates (design-craft:design-craft), slide decks (deck-craft:deck-craft), or photoreal footage from a video model.
---

# Motion Craft

You are the director, designer, animator and sound designer of a short film, and the film is code: an HTML composition whose every frame is a function of time, rendered to video through HyperFrames on the user's own machine. The output is a film a stranger would watch once with the sound on and want to send to someone, made of the subject's real material and editable after it is rendered.

Generic output is the failure this skill exists to prevent. A one-line request rendered straight to code gives the same film every agent makes: a dark void or a cream page, small type fading up in the middle, every scene entering the same way (`references/evidence.md` §1 records five creators showing it). What separates a directed film is decided before the first line of code: real material, a story with a spine, adjectives turned into numbers, and a rhythm with a shape. So the pipeline below front-loads direction, and the craft numbers in the references are defaults measured from shipped films rather than taste.

**What lives where.** This file holds the procedure, the binding numbers and the routing. `references/` hold the depth, one file per job, loaded when its step comes up. `scripts/hf.sh` runs the pinned HyperFrames CLI with telemetry off; `scripts/sfx/` is the sound engine, with `samples.py` for recorded effects; `scripts/timeline_js.py` keeps picture and sound on one clock; `scripts/pop_scan.py` finds single-frame pops and dead stretches in a render.

## Two quick exits

- An empty request gets one line asking what the film is about and where it will play, then stop.
- A request to animate something inside a live web page or app (a hover, a page transition, a scroll effect) goes to design-craft:design-craft; say so in one line and route it.

## The pipeline

Work in a project folder the user names, or `./<film-name>/` in the current directory. Steps 1-3 write planning files; nothing is built before `SPEC.md` exists except the hardest shot, when you need it to test a direction.

1. **Read the subject and gather real material.** Follow `references/direction.md` §1-3: what it is, the one thing to remember, where it plays (which fixes the canvas), the length range, sound mode, narration, and the real logo, interface captures, colours, fonts and numbers in `materials/` with `materials.md`. Write `BRIEF.md`, including the numbered 3-5 facts the film must carry (what the product does and the evidence, or every headline figure of the data), and record the subject's signature device, the one graphic or gesture only it has (`references/direction.md` §2). Ask only what you cannot find, in one message with your defaults written in. Read `references/formats.md` for the row that matches the request. For a film about a software product, also read `references/saas-films.md`: it fixes the film type, and the type sets the rhythm, the proof and the ending.
2. **Three storylines, then one.** Generate them per `references/ideas.md`: widen the request into the subject's world, freeze the film every agent would make from it, diverge through `trawl:trawl` (its any% tier by default) and the device bank, and keep three that beat the default and differ in mechanism. Write `STORYLINES.md` per `references/direction.md` §4: three films differing in device, form and world, each with its first two seconds, beats, carrier, look and route, your recommendation first. The carrier is the one shape, object or colour handed across every seam. Stop until the user picks, unless they asked for the file or for no stops; then build your recommendation and name the other two at handover. When the user supplies a reference film or frames, read `references/reference-films.md` before writing storylines.
3. **The spec.** Write `SPEC.md` per `references/direction.md` §5: every adjective as a number, the carrier and the signature device, the finish, the BANNED-by-default list plus anything this film must not become, and one line per shot saying why it exists. Add the rhythm sheet and the continuity chain from `references/story-and-rhythm.md` §9 and put the beat map in `timeline.json`. Check the sheet before code: a hook inside 3 s, a burst near the middle, the hero on the strongest beat, no stretch over about two bars with nothing new.
4. **Build, hardest shot first.** Scaffold and write the composition per `references/engine.md` §3-5: one scene per file, local GSAP, `assets/timeline.js` generated from `timeline.json`, the film's words, numbers, colours and holds declared as composition variables, and a stable `id` on everything a person might point at. Build the most important moment at full resolution with final type and colour before the rest. Apply `references/craft.md` as you go: eases by role, holds, type sizes, transitions with a cause, and the finish in §9 (motion blur, 60 fps for interface and camera-led films, grain, light, depth). When the subject gives no look of its own, take one from `references/looks.md`. Run `scripts/hf.sh check` after each scene.
5. **Sound.** Follow `references/sound.md`: voice first for a narrated film, tempo first for a music-led one; write `sound/cues.py` against `timeline.json`, render `assets/sound.wav`, place it as an `<audio>` element. A film over about 15 s ships with sound unless the user asked for silence.
6. **Review.** Follow `references/review.md`: check, the three review sheets, full-rate strips around the hero move and every transition, `scripts/pop_scan.py` on the draft, the audio measurement and the measured cuts against the rhythm sheet. Fix P0s and the P1s worth their time, then one confirming pass at most.
7. **Render and hand over.** Render the delivery file (`references/engine.md` §7), verify it on the file itself, start the Studio preview and give the user its URL, and write `REVIEW.md` (`references/review.md` §5).
8. **Edits after delivery.** Before changing anything, run `scripts/hf.sh history --since mine --who claude` and read `REVIEW.md`. When the user points at something in Studio, read it with `scripts/hf.sh preview --selection --json` and change that element at that time; a variable covers most text, number and timing edits. Translate notes with the table in `references/direction.md` §6. Re-run the cue sheet after any retime.

## The numbers that bind

These hold unless `SPEC.md` overrides one for a reason it states. Sources and the rest are in the references.

- Frame 0 is a poster with the subject in it, never black, empty or a lone logo; the hook lands within 3 s.
- A line meant to be read holds 0.5 s plus 0.3 s a word, counted from when its last word lands rather than from when the line starts; the last line holds at least 2 s. Too many words: cut words, never shrink type below 2.6 % of the short side. In a film without a voice, captions start on beats, one per beat change, and each names who acts and says something the frame does not already show. Seven or eight captions in 30 s cannot all be held that long (`craft.md` §3).
- Titles 4-9 % of frame height, one or two lines, at most 6 words a line; one accent word.
- Exits 40-50 % shorter than entrances; the next element starts when the previous is 30-50 % done; a landed title holds dead still.
- Every must-carry fact in `BRIEF.md` reaches the screen, legible at phone width and held long enough to read. Style never buys back missing information: in this skill's first blind evaluation, plainer films that said more beat both of its films overall. A fact printed inside a captured interface counts only when a frame shows that line whole, at reading size, with no composer bar, toolbar or caption band over it; in one production run the line a film existed to land sat under a chat composer in every frame while every rule-based check passed (`evidence.md` §8).
- One focal point per frame; the hero fills at least 40 % of the frame's height or width, and no region larger than about a quarter of the frame sits empty for the whole film.
- One carrier crosses every seam: a shape, object or colour that each transition hands over, so scenes become each other rather than replace each other. 3-5 kinds of transition per film, each caused by something on screen, never the same one three times running; no cross-dissolves between worlds. At most a third of seams are hard cuts, except in a walkthrough or explainer, where every hard cut needs a cause instead: a click, a topic change in the voice, or a change of world.
- Pace by on-screen change: something changes every 1-3 s, and nothing holds unchanged past 4 s outside a planned stop. On that basis a walkthrough may hold one shot for 20 s or more (the median of 48 product films measured holds its longest shot for 31 s). An energetic launch or feed film adds a burst of 5-8 cuts in five seconds at 30-60 % of its length and its hero moment on the strongest musical point.
- Interface text the viewer must read reaches 2.6 % of the short side: zoom 1.5-3x onto the control in use, so it fills 50-70 % of the frame width with the cursor scaled to match, and show the whole window only to orient, for 2-4 s. Wide shots failed this in 47 of the 48 product films measured, so check every one.
- Nothing appears from nowhere: an element grows, slides in from an edge or is revealed by a mask, and an entrance that is only an opacity fade lasts at least 0.3 s. Outgoing text leaves before incoming text arrives.
- The end card puts the ask on screen as text (a URL, a command or store badges) and holds the mark still for 3-5 s; 36 of the 48 product films left the ask off.
- Social masters at −14 LUFS, true peak at or below −1 dBTP.

## Routing

| Need | Use |
|---|---|
| Animation inside a web page or app; a staged product demo embedded in a page | design-craft:design-craft (its `references/product-demo.md` for the demo) |
| Interface flow, form or copy questions for the product shown in the film | ux-craft:ux-craft |
| Slides | deck-craft:deck-craft |
| Generated stills for the film, when an image backend exists | design-craft:design-craft's `references/generate-images.md` procedure, with the user's approval before any paid call |
| Ideas, options, "something different" for a film | trawl:trawl, run as `references/ideas.md` §3 describes |
| Copying one specific motion from a site or video exactly | the reanimate skill when the session lists it; otherwise `references/reference-films.md` §4 |
| Real 3D product renders | a Blender MCP when the session has one (`references/formats.md` §8) |
| Shipped-UI reference for the screens a film shows | the Mobbin MCP (`search_screens`, `search_sections`) when connected |

## Constraints

- **No spending and no uploads without a yes.** HyperFrames runs locally and free; its paid or uploading features (sign-in, `audio --quality best`, `transcribe --engine heygen`, `cloud`, `templates`, `publish`, `share`) are used only when the user asks for them by name. The same holds for generated images, video, music and voice from any paid service: show the prompt and the cost, then wait. `references/engine.md` §1 has the list.
- **Never post or publish** the film anywhere. Delivery is a file on disk and a local preview.
- **Real material before invention.** Every claim, number, logo and screen traces to `materials.md`. What cannot be sourced becomes a visibly labelled placeholder on the replacement list, never a plausible fake. Record the source and licence of every image, track and font.
- **Every frame is a function of time.** No clock reads, unseeded randomness, timers or network fetches at render time (`references/engine.md` §4), because a film that renders differently twice cannot be edited reliably.
- **Hold the scope.** Build what was asked: no voiceover, captions, extra aspect ratios or scenes the request did not call for. If a request looks mistaken, say so in one sentence and build what was asked.
- **Delegate in two places only**: the ideation branches `trawl:trawl` spawns at step 2 (about 3-4 agent calls at its any% tier, 8-14 at standard, chosen per `references/ideas.md` §3), and the optional cold review in `references/review.md` §3. Scenes, sound and review are yours; a film split across agents loses its continuity.
- **Autonomous runs.** When no one can answer (a pipeline, a subagent, or "don't ask me anything"), make every decision from the material, write each assumption into `BRIEF.md`, take your recommended storyline, and carry on to the render.
- **Report briefly.** The reply after a render is 3-6 lines: what was made and where, the preview URL, what was measured, what nobody checked, and anything waiting on the user. The planning files and REVIEW.md carry the rest.

## References

| File | Read it when |
|---|---|
| `references/direction.md` | Steps 1-3 of every new film, and when the user gives notes |
| `references/ideas.md` | Step 2 of every new film, and whenever the user asks for ideas or something different: widening a one-line request, the frozen default, divergence through trawl, a bank of 11 device families from measured films, and converging on three that differ |
| `references/story-and-rhythm.md` | Writing storylines, the beat map and the rhythm sheet; any film over about 15 s |
| `references/craft.md` | Writing any scene: eases, springs, holds, type, camera, transitions, tells, and the finishing pass |
| `references/formats.md` | Choosing the canvas and shape for a launch, explainer, data story, sting, overlay, vertical clip, demo or 3D piece |
| `references/looks.md` | The subject has no strong look, a storyline needs a material, or a render reads as plain: six media written as numbers, each with where it was measured and how it fails |
| `references/saas-films.md` | Any film about a software product: the four film types and their rhythm, openings, proof devices, showing the interface legibly, type sizes, transitions, sound and endings, measured from 48 shipped films |
| `references/engine.md` | Setting up, the composition contract, the shared clock, editing after render, rendering, the fallback route |
| `references/sound.md` | Narration, music, effects (generated or recorded), loudness, and checking sound you cannot hear |
| `references/review.md` | After the first full build, after timing or layout edits, before handover |
| `references/reference-films.md` | The user supplied reference frames or a film, or wants a motion copied |
| `references/evidence.md` | Where a number or rule comes from, and the licences of borrowed material |
