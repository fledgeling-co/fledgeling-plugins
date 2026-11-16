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
