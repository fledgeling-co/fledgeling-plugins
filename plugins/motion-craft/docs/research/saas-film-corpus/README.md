# SaaS product film corpus (2026-11-16)

48 product films the owner picked as examples of good animated SaaS marketing, studied one film per analyst to ground `skills/motion-craft/references/saas-films.md`. 24 are Claude's (Anthropic), 19 Harvey's and 5 Muse's; together they run 84 minutes (19-290 s each, 82 s median).

## What is here

| Path | Contents |
|---|---|
| `films.tsv` | One row per film: id, brand, title, length, format, voice, cuts a minute, median and longest shot, integrated loudness, true peak, transcript source |
| `findings/<id>.md` | The analyst's write-up for the film under eight headings, every claim cited to a timestamp, frame, strip or measurement |
| `findings/<id>.json` | The same analysis in the fixed schema `tools/validate_findings.py` checks |
| `findings/<id>.metrics.json` | The deterministic measurements: cuts, shots, bursts, holds, static stretches, loudness, cut-to-onset alignment against chance |
| `digest.md`, `types.txt` | Corpus statistics by brand, format and film type, and every rule candidate the analysts proposed, grouped by the binding rule it confirms, contradicts or extends |
| `tools/` | The pipeline that produced all of the above |

The films themselves, their frames and their transcripts are third-party material and are not committed. They were kept at `~/Movies/motion-craft-corpus/` on the machine that ran the study.

## Method

Each film went through one headless Claude Sonnet 5.5 analyst (`claude -p --model claude-sonnet-5-5`), launched and awaited by a Workflow of 48 launcher agents running six at a time (`tools/workflow.js`, `tools/run-worker.sh`, `tools/wait-worker.sh`). Sonnet ran as a headless process because the session's settings pin every in-session subagent to Opus. Each analyst followed `tools/brief.md`:

1. fetched the transcript through the router's `yt-transcript` MCP with paid fallback off (22 films had captions, 6 were transcribed locally with Whisper, 20 have no speech);
2. ran `tools/prep.sh`, which downloads the film at 720p or lower with yt-dlp, samples one frame every 2 s and tiles them into labelled contact sheets, and measures it with HyperFrames 0.9.52 (`measure cuts`, `measure events --map`, `measure frames --events` for native-rate strips, `measure look`, local `audio` analysis) and ffmpeg's EBU R128 meter; `tools/scan_frames.py` runs be-my-witness's prescan on every frame plus a consecutive-frame pixel difference, and `tools/analyze.py` turns it all into `metrics.json`;
3. invoked `be-my-witness:be-my-witness` and used its looking protocol: each frame whole once, then 2x crops for anything to be read;
4. opened every contact sheet, the frames `metrics.json` selects (every frame for films up to 2 minutes; composition changes plus every third frame beyond, at most 70), 6-12 native-rate strips around transitions and text entrances, and at least 5 crops;
5. measured 3-8 title lines with `hyperframes measure ink`;
6. wrote `findings.json` and `findings.md` and ran the validator until it passed.

`tools/audit_worker.py` then read each analyst's own transcript to count what it actually did rather than what it reported. Totals: 2,512 frames sampled, 1,752 opened at full resolution, 400 strips, 284 crops, 144 ink readings, be-my-witness invoked in all 48. Six analysts skipped the skill on the first pass; they were re-run with the skill as their first tool call, and their first findings are not used. Worker cost was about $44.

## Limits

- One analyst per film, and no second reader. The measured numbers (cuts, holds, loudness, type heights) are deterministic; the judgements (route, hero moment, what makes it work) are one model's reading.
- Sound was measured, never heard. Music genre comes only from audio tags with their scores.
- Motion between the 2-second samples was seen only in the strips; no ease curve was fitted.
- Three brands. The corpus describes how these three companies make product films; it does not show how common their choices are elsewhere.
- The tools record the run as it happened: paths assume `~/Movies/motion-craft-corpus/`, Homebrew's `python3.14` (which had numpy and Pillow), and a `FLEDGELING_PLUGINS` environment variable pointing at this repository.
