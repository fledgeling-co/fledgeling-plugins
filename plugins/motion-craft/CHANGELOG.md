## 0.1.0 - 2026-11-15

First release. Short films from code, rendered locally through HyperFrames 0.9.52 with telemetry off.

- **Directing before building.** The skill reads the product, collects real material, and lists the facts the film has to get across. It then writes three storylines and a spec in numbers, with a banned-defaults list and a rhythm sheet, before it writes any scene code.
- **One clock.** `timeline.json` drives the picture (through `scripts/timeline_js.py`), the sound cue sheet and the review.
- **Sound.** A vendored copy of claude-motion's stdlib-only procedural engine (MIT), mastered to −14 LUFS and checked with `hyperframes audio` onsets, since the agent can't listen.
- **Review from frames.** It reads HyperFrames' `check` craft findings, the beat, cut and 360 px phone sheets, ranges around every transition, and the measured cuts compared with the rhythm sheet. Then it writes a `REVIEW.md` that names what nobody checked.
- **Editable after render.** Words, numbers, colours and holds are composition variables, and everything a person might point at has a stable id that the Studio preview can select.
- **Tested against no skill.** Two briefs were judged blind by four model families. The first round lost on information density, and the rules added after it are recorded in `evals/EVALS.md`.
