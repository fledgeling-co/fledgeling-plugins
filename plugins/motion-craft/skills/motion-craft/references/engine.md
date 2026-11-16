# Engine: HyperFrames, run locally

motion-craft renders through HyperFrames (HeyGen, Apache-2.0), which turns an HTML composition into video by seeking a paused timeline frame by frame, so every render of the same files is identical. The choice was made by a four-family decision panel on 2026-11-15 (`docs/decisions/2026-11-15-motion-craft-engine.html` in the fledgeling-plugins repo), on the conditions below; each was checked on a real install before the decision.

## 1. The wrapper, and what it switches off

Every HyperFrames command goes through `scripts/hf.sh`, never a bare `npx hyperframes`:

```bash
<skill>/scripts/hf.sh <command> [args…]
```

It pins the CLI to a validated release (0.9.52; `HYPERFRAMES_VERSION` overrides it once a newer release has been tried), and sets `HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1` and `HYPERFRAMES_SKIP_SKILLS=1`, the opt-outs HyperFrames documents. The pin exists because the CLI is pre-1.0 and its composition contract can change between releases; a film made under one version should re-render under the same one.

What motion-craft deliberately does not do, because each sends data to HeyGen or can bill the user's account:

- never run `hyperframes events` (the "usage beacon" HyperFrames' own skill starts with), and never pass `--skill` to `init` or `render`;
- never use `audio --quality best`, `transcribe --engine heygen`, `cloud`, `lambda`, `cloudrun`, `templates`, `reverse` or `billing`, and never sign in, unless the user asks for that feature by name and has agreed to the cost;
- never run `publish` or `share`, which upload the project or the video; delivery is a file on disk.

All of this works without an account: HyperFrames' docs say "You can create and render locally without an account", and a 10-second 1080p test film rendered locally in 19 seconds on 2026-11-15 with telemetry off.

## 2. Setup, once per machine

Needs Node 20 or later and ffmpeg on the PATH; HyperFrames fetches its own headless Chrome on first use.

```bash
<skill>/scripts/hf.sh doctor        # Node, FFmpeg, Chrome; whisper-cpp and Kokoro are optional
```

`doctor` lists whisper-cpp (word timings), Kokoro (local speech) and MusicGen (local music) as optional; install one only when a film needs it, and say so to the user first because each is a large download.

## 3. A new project

```bash
<skill>/scripts/hf.sh init <dir> --non-interactive --skip-skills --resolution landscape   # or portrait, square
```

`init` writes `index.html`, `hyperframes.json`, `package.json`, and a `CLAUDE.md` and `AGENTS.md` that point at HyperFrames' own skills. Leave those two files in place for anyone who uses HyperFrames directly; motion-craft's references carry what this skill needs, and when the session lists HyperFrames' own skill you may read it for contract detail, skipping its usage-beacon line.

Lay the project out as:

```
<dir>/
  index.html                  root composition: variables, scene hosts, audio
  compositions/<scene>.html   one scene per file, everything inside <template>
  assets/                     fonts/, vendor/, media, sound.wav, timeline.js
  materials/  materials.md    real material and its sources (direction.md §2)
  BRIEF.md  STORYLINES.md  SPEC.md  timeline.json  sound/cues.py  REVIEW.md
```

The scaffold loads GSAP from a CDN. Copy it into the project so renders do not depend on the network: `mkdir -p <dir>/assets/vendor && curl -sL https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js -o <dir>/assets/vendor/gsap.min.js`, then point the `<script>` at `assets/vendor/gsap.min.js`. GSAP is free for this use under its standard licence; the file lives in the user's project, not in this skill.

## 4. The contract

`scripts/hf.sh check --json` reports most violations with a `Fix:` line. The rules that matter most when writing scenes (HyperFrames `SKILL.md` contract and `format.md`):

1. Every timed element has `class="clip"`, `data-start` and `data-duration` in seconds, and shows over `[start, start + duration)`; an end state that lands exactly on its end is never rendered.
2. The film's length is the root's `data-duration`; overrun is cut, an early end holds the last frame.
3. Each composition builds one paused GSAP timeline and registers it last: `window.__timelines["<data-composition-id>"] = tl`. The scene host, the scene root and the timeline key share one id, or every render waits 45 s per scene and then shows static frames.
4. Nothing reads the clock: no `Date.now()`, unseeded `Math.random()` (use a seeded generator such as mulberry32), network fetches, timers, `requestAnimationFrame` loops or `repeat: -1`. Everything visible is a function of timeline time.
5. Use `fromTo` inside scenes, never `from`: a scene is re-seeked each time it shows, and `from` drifts on seek-back.
6. Animate transforms and opacity, never `left`, `top`, `width` or `height`; never tween `display`, `visibility` or `autoAlpha` on a `.clip` (animate a child); no CSS `transform` on an element GSAP transforms.
7. Media: `<video>` gets `data-has-audio="true"` or `muted`; every `<audio>` has an `id`; never `play()`, `pause()` or seek media yourself.
8. Fonts: only the bundled families resolve by name (Inter, Montserrat, Outfit, Nunito, Oswald, League Gothic, Archivo Black, Space Mono, IBM Plex Mono, JetBrains Mono, EB Garamond, Playfair Display, Source Code Pro, Noto Sans JP, Roboto, Open Sans, Lato, Poppins). Every other family needs `@font-face` pointing at a file in `assets/fonts/`.
9. Asset paths are `assets/...` with no leading slash, in scene files too.
10. Scene files put their styles, markup and scripts inside `<template>` and style their root as `#root`, sized with `inset: 0`.
11. Content stays inside the 90 % action-safe box, key text inside 80 % title-safe.
12. Canvas, three.js or WebGL layers draw from the `hf-seek` event: `window.addEventListener("hf-seek", e => renderAt(e.detail.time))`, with all stateful simulation done once at load.
13. Set every element's starting state with `gsap.set` or CSS, never a `tl.set` at time 0: frame 0 renders before a zero-time `tl.set` applies, so the poster frame shows the wrong camera, scroll or visibility.
14. GSAP 3 has no `className` tween; swap a class with `tl.set(el, { attr: { class: '…' } }, t)`.
15. The lint rejects a template literal inside `querySelector`; reach a child through an element you already hold, `el.querySelector('.label')`.

Intended overflow, overlap or crop is declared on the narrowest element (`data-layout-allow-overflow`, `data-layout-allow-overlap`, `data-layout-bleed="true"`) so the layout audit can still see everything else.

## 5. One clock for picture, sound and review

The beat map lives in `timeline.json` as film-absolute seconds (a top-level `"duration"` plus named beats grouped by scene). Scenes read it through `assets/timeline.js`, generated from the JSON so the two never disagree:

```bash
python3 <skill>/scripts/timeline_js.py <dir>/timeline.json <dir>/assets/timeline.js
```

Load `assets/timeline.js` from `index.html` before any scene; scenes read `window.TL` and convert to their own clock with `TL.<scene>.<beat> - <scene host's data-start>`. The sound cue sheet reads the same JSON (`sound.md` §2). A retime is an edit to `timeline.json`, a regeneration of `timeline.js`, and a re-run of the cue sheet; never a hard-coded time inside a scene.

## 6. Editable after the render: the Claude Motion loop

Claude Motion's value is that a finished film stays editable: a tweaks panel listing every word, scene length and speed, and comments pinned to one element (`references/evidence.md` §1). Build every film so the same loop works here:

- **Tweaks are composition variables.** Declare the film's words, key numbers, brand colours and hold durations on `index.html`'s `<html data-composition-variables='[{"id":…,"type":"string|number|color|boolean|enum","label":…,"default":…}]'>` and bind them with `data-var-text="id"`, `data-var-src="id"`, or `var(--id)` in CSS. Studio's Variables panel then edits them live.
- **Comments are stable ids.** Give every element a person might point at a short readable `id` and keep it when the text changes.
- **Open the preview** with `<skill>/scripts/hf.sh preview --background` from the project folder; it prints the Studio URL. Studio shows the timeline, the variables and a keyframe editor.
- **Read what the user pointed at**: `scripts/hf.sh preview --selection --json` returns the element selected in the running Studio. Change that element at that time and nothing else.
- **Respect their edits**: before any change to an existing project, run `scripts/hf.sh history --since mine --who claude` (or `catch-up` when a command tells you to) and build on what the user changed; Studio rewrites the files you wrote.

## 7. Render

```bash
<skill>/scripts/hf.sh render -q draft -o out/draft.mp4                 # fast, for review rounds
<skill>/scripts/hf.sh render -q delivery -o out/<name>.mp4             # the file you hand over
<skill>/scripts/hf.sh render --format webm -o out/<name>.webm          # transparent overlay (or --format mov for ProRes 4444)
<skill>/scripts/hf.sh render --format gif --fps 15 -o out/<name>.gif   # README or chat GIF
<skill>/scripts/hf.sh render --start 8 --end 14 -o out/range.mp4       # re-render one stretch
```

Name the file after the film, never `output.mp4`. `--fps` defaults to the root's `data-fps`, else 30. Add `data-motion-blur="on"` to the composition root for fast 2D moves when the look calls for blur.

## 8. Tools worth reaching for

- `scripts/hf.sh catalog --query "<the effect>" --json` and `scripts/hf.sh add <block>` before hand-writing a named effect, chart, transition or caption style: registry blocks install as editable source.
- `scripts/hf.sh capture <url> --json` when a website is the subject: real screenshots, fonts and colours into the project.
- `scripts/hf.sh tts --text-file script.txt -v <voice> -o assets/voice.wav` for local speech (Kokoro, free, once installed); `scripts/hf.sh transcribe <file> --json` for word-level timings (whisper-cpp or Parakeet, local).
- `scripts/hf.sh beats <audio> --json` for a supplied track's beats and BPM.
- `scripts/hf.sh measure cuts|events|curve|frames <video> --json` to read a reference film (`reference-films.md`).
- `scripts/hf.sh remove-background` for a talking-head matte.

## 9. When the user declines HyperFrames

When the user does not want the vendor CLI, or it cannot run (no Node, offline, a locked-down machine), fall back to design-craft:design-craft's plain timeline engine in its `references/make-an-animation.md`: one self-contained HTML file whose every frame is a pure function of t, exported by seeking `window.__animStage.setTime()` and piping screenshots into ffmpeg. Everything in `direction.md`, `story-and-rhythm.md`, `craft.md` and `sound.md` applies unchanged; the review loses `check`, `snapshot` and `audio`, so build contact sheets with ffmpeg (`reference-films.md` §2 recipe, pointed at your own render) and measure loudness with `ebur128` (`sound.md` §6). Say in REVIEW.md which route rendered the film.
