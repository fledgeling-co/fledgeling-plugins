<context>
You are one of 48 analysts studying animated SaaS product marketing films. The owner picked these films as examples of what good looks and sounds like. Your findings will be merged with the other 47 to improve `motion-craft`, a skill that directs short product films built from code: HTML compositions animated with GSAP and rendered frame by frame through HyperFrames, with procedurally generated sound. The skill already holds rules measured from 2 reference films and 18 creator videos. The films in this corpus come from three brands: Muse, Claude (Anthropic) and Harvey.

The skill's current binding rules, which your `rule_candidates` mark as confirmed, contradicted or extended:

1. Frame 0 is a poster with the subject in it, never black, empty or a lone logo; the hook lands within 3 s.
2. A line meant to be read holds 0.5 s plus 0.3 s a word; the last line holds at least 2 s; type never below 2.6 % of the short side.
3. Titles 4-9 % of frame height, one or two lines, at most 6 words a line, one accent word.
4. Exits 40-50 % shorter than entrances; the next element starts when the previous is 30-50 % done; a landed title holds dead still.
5. Every must-carry fact reaches the screen, legible at phone width; a plainer film that says more beats a stylish one that says less.
6. One focal point per frame; the hero fills at least 40 % of the frame's height or width; no region larger than a quarter of the frame stays empty for the whole film.
7. 3-5 kinds of transition per film, each caused by something on screen; at most a third of seams are hard cuts; no cross-dissolves between worlds.
8. An energetic film has a burst of 5-8 cuts in 5 s at 30-60 % of its length, and its hero moment on the strongest musical point.
9. Social masters at -14 LUFS, true peak at or below -1 dBTP.
10. Cuts every 1.8-3.5 s in launch films; the problem is shown, not named in a caption; real product UI beats invented UI.
</context>

<video>
Id: {{ID}}
Title: {{TITLE}}
Brand: {{BRAND}}
Duration: {{DURATION}} s
URL: https://www.youtube.com/watch?v={{ID}}
Working folder: {{DIR}}
</video>

<files>
After step 2 the working folder holds:
- `video.mp4` (720p or lower) and `video.info.json`
- `frames/fNNNN.jpg`: one frame every 2 s with no overlay at 1280 px wide; `fNNNN` is at t = (NNNN - 1) x 2 s, so `f0001.jpg` is frame 0
- `sheets/sheet-NN.jpg`: contact sheets of 16 frames each with the timestamp burned in
- `strips/window-NN-<t>s.jpg`: consecutive native-rate frames around each on-screen event; `measure/strips.json` says what changed in each window
- `measure/cuts.json` (hard cuts and shots), `measure/events.json` (appears, holds, sound onsets), `measure/audio.json` (sound kind, loudness, onsets, sections, describe tags), `measure/look.json`, `measure/ebur128.txt`
- `measure/frames-scan.json`: be-my-witness prescan of every sampled frame plus the pixel-difference share from the previous sampled frame
- `measure/metrics.json`: rhythm, bursts, holds, static stretches, loudness, cut-to-sound alignment, and `frames_to_open`, the list of frames you open at full resolution

Tools: `HF=<fledgeling-plugins>/plugins/motion-craft/skills/motion-craft/scripts/hf.sh` runs HyperFrames measurements locally. `BMW=<fledgeling-plugins>/plugins/be-my-witness/skills/be-my-witness/scripts` holds `crop.py`, `prescan.py` and `diffmask.py`. Run Python as `/opt/homebrew/bin/python3.14 -P` (the default python3 lacks numpy and Pillow).
</files>

<task>
Based on the film above, make your first tool call the Skill tool with `be-my-witness:be-my-witness`, then work through these seven steps in order, then write the two output files.

1. **Transcript.** Load the transcript tool with ToolSearch (`select:mcp__router__yt-transcript__youtube_transcript`), then call it with `url` = `{{ID}}`, `allowPaid` = false and `timestamps` = true. Save the returned text verbatim to `transcript.md`, with a first line naming the source it reported (human captions or auto-generated captions). When it reports no caption track, transcribe locally after step 2: `mlx_whisper video.mp4 --model mlx-community/whisper-large-v3-turbo --output-format srt --output-dir . --language en`, and save the result as `transcript.md` with source `local-whisper`. When the film has no speech, whisper invents lyrics or repeats a phrase; in that case record source `none` and voiceover `none-music-only`.

2. **Prepare.** Run `bash {{TOOLS}}/prep.sh {{ID}}` with a Bash timeout of 600000 ms. It downloads the film and writes every file listed above. Then read `measure/prep-status.json`: `{"prep":"ok"}` means continue. Any other value means stop here and write the failed form of `findings.json` described under the dead ends below.

3. **Apply be-my-witness.** Use the skill you loaded first. Use its looking protocol: each frame once whole for layout and structure, then region crops at 2x or more for anything you need to read, because text below about 7 px of glyph height is unreadable to you in a downscaled frame. Its prescan has already run on every frame (`measure/frames-scan.json`). This film has no design mock and no test expectation, so its gate, verdict schema, blinding and two-order comparison do not apply; use it for the looking protocol and the crop script, not to grade.

4. **Look.** Read `measure/metrics.json` first. Then:
   - count the contact sheets with `ls sheets | wc -l` and open each one;
   - count the frames named in `frames_to_open` (between 10 and 70, depending on the film's length) and open each one at full resolution with the Read tool, one Read call per frame;
   - choose 6-12 strips from `strips/` using `measure/strips.json`, covering the opening, the hero moment, at least 3 transitions, at least 2 text entrances and the ending, and open each one; strips are the only place you see how things move between the 2-second samples;
   - make at least 5 crops with `/opt/homebrew/bin/python3.14 -P $BMW/crop.py frames/fNNNN.jpg --region x,y,w,h --scale 2 --out crops/<name>.png` on titles, interface text and small labels, and open each crop.

5. **Measure titles.** For 3-8 headline or title lines, run `$HF measure ink video.mp4 --at <seconds> --roi x,y,w,h` with the region in the video's own pixels (`measure/probe.json` gives its size; the frames are 1280 px wide, so scale a region found on a frame by video width / 1280). Record each line's height in pixels against the frame height as `title_measurements`, and the smallest and largest percentage as `title_height_pct`.

6. **Sound.** You cannot hear the film. Describe its sound only from evidence: the transcript and its `[music]`-style tags, `measure/audio.json` (kind, describe tags with their scores, sections, onsets) and the sound block of `metrics.json` (integrated LUFS, true peak, loudness range, and `cuts_on_strong_onset_share` against `chance_share`). When the cut share is less than 0.10 above the chance share, write that the cuts are not locked to the sound. Name an instrument or genre only when a describe tag above 0.2 supports it, and quote the score.

7. **Judge what makes it work.** From what you saw, write 3-8 `good` observations, 0-5 `weak` ones and 3-8 `rule_candidates`. A rule candidate is an instruction another film-maker could follow and a reviewer could check from a frame or a measurement, with a number wherever the film gives one (a duration, a share of runtime, a size, a count). Mark each one `confirms`, `contradicts` or `extends` against the numbered binding rules above, naming the rule number in `skill_rule`, or `new` with `skill_rule` = "none".

Then write the outputs:

- **`findings.json`**, following `{{TOOLS}}/findings.skeleton.json` exactly: every key present, values of the type and length shown there. `hero_moment.share` is `t_s` divided by `duration_s`. Copy measured numbers (hard cuts, cuts per minute, median shot, loudness) from `metrics.json` rather than recomputing them. Use -1 for a number you could not measure and say why in `unchecked`. Run `/opt/homebrew/bin/python3.14 -P {{TOOLS}}/validate_findings.py findings.json` and fix the file until it prints `OK`.
- **`findings.md`**, 600-1,200 words, with these eight headings in this order: Hook and structure; Rhythm; Look and type; Product interface; Motion and transitions; Copy on screen; Sound; What to steal. Under each heading, prose that cites a timestamp, a frame file, a strip file or a measured number for every claim.
</task>

<rules>
- Each claim in both output files cites its evidence: `t=12.4s`, `f0007.jpg`, `strips/window-09-9.885s.jpg`, or a key in `metrics.json`. A claim you did not observe stays out; say what you could not check in `unchecked`.
- Quote on-screen copy verbatim from crops, not from memory of a downscaled frame.
- Describe what is on screen, never the tool you guess made it.
- Write only inside {{DIR}}. Leave `{{TOOLS}}`, the skill folders and every other video folder unchanged.
- Spend nothing: keep `allowPaid` false, never pass `--quality best` to HyperFrames, and make no network calls beyond the download inside `prep.sh` and the transcript tool.
- Run no git commands and start no subagents.
</rules>

<dead_ends>
- Download refused or prep failed: write `findings.json` with only `id`, `title`, `brand`, `duration_s`, `status` = "failed" and `unchecked` holding the reason and the last line of the prep output; validate it, then finish.
- Transcript tool missing from ToolSearch or erroring: use the local whisper route in step 1 and name the tool failure in `unchecked`.
- A measurement file missing or empty: continue with what exists, set the dependent numbers to -1, set `status` = "partial", and name the missing file in `unchecked`.
</dead_ends>

<finish>
The work is finished when you have invoked `be-my-witness:be-my-witness`, `validate_findings.py` prints `OK` for `findings.json`, and `findings.md` exists with its eight headings. A progress update is not a finish: keep going until both files exist. Your final message is one line: `DONE {{ID}} <status> frames_opened=<n> crops=<n> strips=<n>`.
</finish>
