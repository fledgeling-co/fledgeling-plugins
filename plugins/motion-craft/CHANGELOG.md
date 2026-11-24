## 0.4.0 - 2026-11-24

What makes a film look made rather than generated, from six more sources: the motlab, AI-Video-Factory and motion-educator repositories, 240 films made with Claude on prompt-motion.com with their prompts, 21 product films motionflare.ai made from websites, and Caruso's films and interface loops. The method and the measurements are in `docs/research/motion-sources-2026-11/`, summarised in `evidence.md` §9.

- **One carrier and one signature device.** Every storyline names the shape, object or colour it hands across every seam, and every film records the subject's own signature graphic (Stripe's ribbon, Raycast's light bars) as its ground, carrier or hook. The best-received gallery films and all 21 motionflare films are built this way (`direction.md` §2, §4-5; binding rule 7).
- **A finishing pass, `craft.md` §9.** Motion blur on, 60 fps for interface and camera-led films, 2-4 % grain, one soft light and a sweep over the final mark, a living ground and two or three depth layers. Launch, vertical and demo films now default to 60 fps (`formats.md`).
- **Six looks written as numbers, new `looks.md`**: brand motif ground, fine-art backdrop, product glass, interface in space, graphite stage, monochrome editorial.
- **The default named.** Undirected prompts give a dark, fast-cut montage (12.9 cuts a minute, 27 % light frames, against 6.0 and 62 % from long directed prompts), and the showreel default joins the banned list with shockwave rings, camera shake, a selection-box highlight and motion connected to nothing (`story-and-rhythm.md` §4, `direction.md` §5).
- **Craft.** Screen-studio framing at 50-70 % of the frame width; a 3-5 % push through holds carried into the next shot; nothing appearing from nowhere; exits before entries; flood-and-contract, shape-becomes-the-shot and foreground-through-camera transitions; word-swap, decode and mask-roll headlines; font choice by vibe (`craft.md` §3-6).
- **Interface staging.** The agent card narrated by a status pill, with skeleton filler and a human approval, and Caruso and motionflare added to the house styles (`saas-films.md` §3, §12).
- **Sound.** Recorded effects placed by audible onset, peak or end through the new `scripts/sfx/samples.py`, levels by role, spacing limits and pitch variation (`sound.md` §3-4).
- **Review.** Full-rate strips around every transition, the new `scripts/pop_scan.py` for single-frame pops and dead stretches, a carrier, finish and look row, evidence before each verdict, and a verification format for a second cold pass (`review.md`).
- **Engine.** Six browser traps from the gallery's gotchas, and HyperFrames' motion-blur attributes and checks (`engine.md` §4, §7).

These rules have not yet been run through `evals/`.

## 0.3.0 - 2026-11-16

What a production run taught once other models reviewed it frame by frame. The run was seven 25-32 s product films, reviewed twice by a four-family panel and once by Sonnet 5.5 under be-my-witness. One series, so each change is an observed failure with its fix (`evidence.md` §8).

- **Reading time counts from the last word.** A line built word by word settles when its last word lands. Counted from the start, 33 of 35 captions met the hold; counted from the last word, about 28 missed. In a film without a voice, captions now start on beats, one per beat change, and say what the frame does not already show (binding rules, `craft.md` §3, `saas-films.md` §6).
- **A fact inside the interface has to reach a frame.** The film's one message sat in a card footer under the chat composer in every sampled frame, while every rule-based check passed. Binding rule 5 now says a captured line counts only when a frame shows it whole and uncovered, and review gains a row for it.
- **Interface staging, `saas-films.md` §5.** Show the whole card before pushing in. Keep chrome off the line that carries the point. Give a decision 1.5 s before the tap. Veil the pane the camera leaves. Fade system sheets in within 0.15 s. Use the product's real mark in notifications. Open on content rather than an empty app.
- **Line breaks by sense** (`craft.md` §4): no one-letter word alone at the end of a line.
- **Review.** Sample every beat as well as a grid, and check frame findings against the timeline: two from a 2 s grid were wrong. Brief the one fresh reviewer as a viewer, with a per-frame manifest and none of this skill's rules.
- **Sound.** When the render log says the audio was lowered to stay under −1 dBTP, lower the one cue that overshoots after AAC encoding instead of shipping a quiet master (`sound.md` §5).
- **Engine.** Starting states go in `gsap.set` or CSS, not a zero-time `tl.set`; GSAP 3 has no `className` tween; the lint rejects template literals in `querySelector` (`engine.md` §4).

## 0.2.0 - 2026-11-16

What good looks and sounds like in SaaS product films, measured from 48 of them.

- **New reference, `saas-films.md`.** 48 films the owner picked as good examples (24 Claude, 19 Harvey, 5 Muse; 84 minutes), each studied by its own Sonnet 5.5 analyst from the transcript, a frame every 2 s, native-rate strips around 400 on-screen events, 284 crops under be-my-witness's looking protocol and HyperFrames' cut, event, look, ink and loudness measurements. It covers the four film types and their rhythm, openings, proof devices, showing an interface legibly, measured type sizes, transitions, colour, sound, endings, the faults even these films share, and the three brands' house styles.
- **Rhythm by film type.** Walkthroughs and explainers are now paced by change on screen, every 1-3 s with nothing still past 4 s, instead of a cut every 1.8-3.5 s. The measured films cut 5.7 times a minute and hold their longest shot 31 s, and only 7 of 48 have a burst, so the burst rule now applies to energetic launch and feed films only. In a walkthrough a hard cut is judged by its cause, not by the one-third share.
- **Interface legibility.** A new binding rule: zoom 1.5-3x onto the control in use until its text reaches 2.6 % of the short side, and keep whole-window shots to 2-4 s of orientation. Wide shots failed this in 47 of the 48 films. Review and the tells list check it.
- **Endings.** The end card puts the ask on screen as text and holds the mark 3-5 s; 36 of the 48 films left the ask off.
- **Loudness stays a spec.** The films' masters measured −15.8 LUFS at the median and 18 broke −1 dBTP, so −14 LUFS and −1 dBTP stay the delivery target rather than following the references.
- **Evidence.** Method, tools, per-film findings, measurements and the corpus digest are in `docs/research/saas-film-corpus/`; `evidence.md` §7 and `docs/research/CORPUS.md` §4 summarise them.

## 0.1.0 - 2026-11-15

First release. Short films from code, rendered locally through HyperFrames 0.9.52 with telemetry off.

- **Directing before building.** The skill reads the product, collects real material, and lists the facts the film has to get across. It then writes three storylines and a spec in numbers, with a banned-defaults list and a rhythm sheet, before it writes any scene code.
- **One clock.** `timeline.json` drives the picture (through `scripts/timeline_js.py`), the sound cue sheet and the review.
- **Sound.** A vendored copy of claude-motion's stdlib-only procedural engine (MIT), mastered to −14 LUFS and checked with `hyperframes audio` onsets, since the agent can't listen.
- **Review from frames.** It reads HyperFrames' `check` craft findings, the beat, cut and 360 px phone sheets, ranges around every transition, and the measured cuts compared with the rhythm sheet. Then it writes a `REVIEW.md` that names what nobody checked.
- **Editable after render.** Words, numbers, colours and holds are composition variables, and everything a person might point at has a stable id that the Studio preview can select.
- **Tested against no skill.** Two briefs were judged blind by four model families. The first round lost on information density, and the rules added after it are recorded in `evals/EVALS.md`.
