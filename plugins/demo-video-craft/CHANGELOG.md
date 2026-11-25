# Changelog

## 0.3.1 - 2026-11-26

The plugin installs. Its Claude manifest carried two fields from the Cursor manifest, `logo` and `"skills": "skills"`, and Claude Code refuses a `skills` path that does not start with `./`, so every version from 0.1.0 failed to install with "invalid manifest file". Both are gone; `skills/` is found by default, as in every other plugin here, and `claude plugin validate plugins/demo-video-craft` now passes.

## 0.3.0 - 2026-11-25

The kit now rebuilds the series it came from. `kit/reference/` holds that series' 36 screens and ten-film table, ported unchanged, and `new_series.py --reference` starts from it. Rebuilt with nothing but the kit and the series' own voice and music files, its ten films measure a mean SSIM (structural similarity, 1.0 is identical) of 0.9994-0.9998 against the published files, lowest frame 0.9985 (`evals/run_reference.sh`). The self-test checks the ten film lengths against the published ones.

The kit now works for any product, not only one shown inside a chat app: frames for the product's own browser window, desktop window or phone; typing into any field (`typein`); any canvas size, including 9:16, where the camera frames into the area TikTok, Reels and Shorts all leave clear and the opener and end slide have portrait layouts; and captions cut from the narration's own word timings. `engine/render.py` runs step 6 in one command (build, render once, remux, check sizes, publish only on a pass), and `site/build_site.py` builds the overview and shorts pages, posters and share image from `site.json`. The example series has four films: a short in Claude, one in the product's own browser window, a 9:16 one on a phone, and the overview.

New script `compare_films.py` measures a rebuild against published files frame by frame. `delivery.py` now catches a voiced cut that carries the master's sound by comparing momentary loudness; the byte comparison it replaced always differed across encoders, so it could never fail. `gateway_audio.py --dry-run` prices a batch before anything is sent. 57 self-test cases across nine scripts.

The references now agree with the kit where they had drifted (the press ring is 64 px; where the limiter, the pace factors and the label switch live), and `gemini.md` carries the extra steps for a run on Gemini: a count for each categorical scope, the four binding numbers no script reads back, and the file each skill call has to leave.

## 0.2.0 - 2026-11-25

Ships the source series' engine as a starter kit (`skills/demo-video-craft/kit/`): the window runtime (K.play) and the stage runtime (K3.stage), the film table's machinery (step helpers, the overview's opening and end slide, the pace function, the settling push, the length gate), the screen builder, the build with its narration gates, and the score. Brand and content are taken out; an example series builds, checks clean and renders (`evals/run_kit_example.sh`). `new_series.py` starts a series from it.

Four new scripts, each with a self-test: `new_series.py`; `sync_table.py`, which prints each narration line beside what is on screen; `series_lint.py`, which finds serif faces, film styles that reach the product's markup, and retired values; and `edgar.py`, for a real US-listed client's figures and holders from SEC EDGAR. `delivery.py` gains `publish` (copies only when every film passes) and `sheet` (stamped, cropped frames tiled to look at, including one frame per narration line). 49 self-test cases across eight scripts.

The references take in what fifteen agents found reading the whole source session: the camera, cursor, focus, arrival and typing numbers; the pace function and the settling push as formulas; the highlight, the lockup bar and the end slide as specs; the interactive demos page; a sweep for vendor apparatus on a prospect's page; working with a real company's filings; a dozen more HyperFrames and shell traps. Aligning a lockup with its neighbouring text on the baseline is now a binding number, after the owner's "this alignment is bad", and the check that found every short's lockup bar off centre is in the procedure.

## 0.1.0 - 2026-11-25

First release. A nine-step procedure for a product's demo video series (one overview, a set of shorts, each muted and voiced from one render, published on a small video site), routing rendering and sound to `motion-craft:motion-craft`, pages to `design-craft:design-craft` and `ux-craft:ux-craft`, review to `design-review:design-review`, words to the brand's voice skill, questions to `clarify:clarify` and the report to `status-update:status-update`.

Four scripts, each with a self-test (24 cases): `gateway_audio.py` for narration, word timings and music beds through Vercel AI Gateway; `duck.py` for the bed's gain curve; `delivery.py` to make the voiced cut and gate a delivery folder; `site_urls.py` to keep a site's media URLs fresh under permanent file names.

Built from one four-round production run on 24-25 November 2026 and from motion-craft's study of 48 shipped SaaS product films. No comparison against working without the skill has been run yet; `EVALS.md` says what was verified instead.
