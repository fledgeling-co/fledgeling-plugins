---
name: demo-video-craft
description: >-
  Make a product demo video series and publish it: one overview or launch video plus a set of 20-25 s shorts, one
  workflow each, built picture-first so a muted master and a voiced cut come from a single render, then publish them
  on a small video site with a gallery and a modal player. Ships the engine of a delivered series as a starter kit
  (window and stage runtimes, the pace and final-hold machinery, the screen builder, the build, the score, the render
  and publish step, the site build) and that whole series as a reference the kit rebuilds frame for frame (mean SSIM
  0.9994-0.9998 against the published files), so a new series starts from measured values rather than prose. Works for
  a product shown inside a chat host (a Claude or ChatGPT connector, an add-in) or in its own interface (a browser or
  desktop window, a phone app), at 16:9 or 9:16. Use it whenever someone asks for demo videos, an overview video and
  shorts, YouTube, LinkedIn or vertical clips of a product working, videos for a prospect or a launch page, or wants a
  narrated series revised (pace, pronunciation, music, end slide) or republished without breaking links, even when
  they never say "demo". Routes rendering and sound to motion-craft:motion-craft, pages to design-craft:design-craft
  and ux-craft:ux-craft, and words to the brand's voice skill. NOT for a single motion piece (motion-craft:motion-craft),
  a standalone animated demo inside a web page with no series around it (design-craft:design-craft), or slides.
---

# Demo Video Craft

You are producing a series, not a film: one overview that explains the product and a set of shorts (nine in the
source run) that each show one workflow ending on its result, all with the same customer and figures, each delivered
twice (muted and voiced), and all published where a prospect can watch them. The series then goes through rounds of
owner notes, often four or more, and some notes reverse earlier ones.

The failure this skill exists to prevent is the fix that lands in one place and not the others. In the run this
skill was built from, a brand lockup was fixed on the pages and stayed wrong in the videos. A corrected voice line
kept playing because the browser served its cached copy under the same file name. A share image still showed the
first round after three rewrites. Every check that ran passed. So the procedure keeps one source for each thing
that appears in more than one place, and it gates the delivery with scripts that look at the files themselves.

**What lives where.** This file holds the procedure, the binding numbers and the routing. `references/` holds the
depth, one file per job. `kit/` holds the code (`kit/README.md`): the runtimes, the engine, the site build, an example
series for a new product, and the reference series, the source run's ten films, which the kit rebuilds as published.
`scripts/` holds the tools, each with `--self-test`: `new_series.py` starts a series from the kit; `gateway_audio.py`
makes narration, word timings and music beds (`--dry-run` prices them first); `duck.py` gives the bed's gain curve;
`delivery.py` makes the voiced cut, gates a folder, publishes only on a pass and tiles stamped frames; `sync_table.py`
prints each narration line beside what is on screen; `series_lint.py` finds serif faces, film styles that reach the
product's markup, and retired values; `compare_films.py` measures a rebuild against published files frame by frame;
`site_urls.py` keeps the site's media URLs fresh; `edgar.py` sources a real US-listed client's filings. Rendering and
the sound engine belong to motion-craft: invoke `motion-craft:motion-craft`, then use `scripts/hf.sh`, `scripts/sfx/`
and `scripts/pop_scan.py` under the base directory that skill reports when it loads.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It gives the film table, the states, the step-boundary sheets and the five places a note can live a count each, turns the binding numbers into a ledger read back off the rendered files (naming the four no script reads: narration words, text size, baseline, end-slide hold), and makes each skill call leave the file the next step opens. Other models skip it.

## Two quick exits

- One film with no series around it (a launch film, a sting, an explainer) goes to `motion-craft:motion-craft`.
  Say so in one line and route it.
- An animated demo inside a web page with no video series around it goes to `design-craft:design-craft` and its
  `references/product-demo.md`. A features page that is part of a series follows `references/site.md` §3b.

## The series folder

Work in the folder the user names, or `./<product>-videos/`. One source per thing, read by everything that shows it:

| File | Holds | Read by |
|---|---|---|
| `BRIEF.md` | audience, where the videos play, the numbered must-carry facts, English variant, asked lengths, the ask | every step |
| `CLAIMS.md` | each capability shown, its source, built or not, and how it appears | the scripts, the narration, the pages |
| `SOURCES.md` | for a real company: every figure, date and holder with its filing, page and accession | the screens, the pages |
| `_kit/` | the series' fork of the kit (runtime, engine, site build) | the build |
| `series.json` | product, file prefix, lockup words, the ask, canvas size, fonts, voice paths, music beds, host marks, the label switch, pace factors, length caps | the build |
| `states.py` | every screen, with the scenario's names and figures (its one source), and the banned names | every film |
| `films.py`, `SERIES.md` | the film table (scenes, steps, effect beats, voice placements, tempo, lockbar, limit, size, captions), and its summary for people | the build |
| `lines.json`, `respell.json` | narration text per line, and the spoken spellings | voice generation, captions, pages |
| `lockup.css`, `marks/`, `theme.css` | the brand lockup's one spec, every mark (product, hosts, client), and the series' tokens | pages and films |
| `films/<id>/` | one HyperFrames project per film, written by `films.py` and `build.py` | motion-craft |
| `delivery/`, `published.txt` | the finished files, and every video file name already shared | `delivery.py`, the site |
| `site.json`, `site/` | the site's copy (descriptions, order, headings, footer), and the built site | `build_site.py`, `site_urls.py` |
| `ROUNDS.md`, `REVIEW.md` | the owner's notes as a numbered list per round, and what was built, measured and not checked | every round |

## Procedure

1. **Brief and claims.** Read `references/brief-and-claims.md` and follow it. Read the product's own record first
   (requirements, specs, what is built), then the audience notes, then the brand's site. Write `BRIEF.md`,
   `CLAIMS.md` and the names and pronunciation table; the scenario's names and figures go in `states.py`. When the
   owner names a real company, follow `references/brief-and-claims.md` §4b instead of inventing one. Invoke
   `clarify:clarify` before asking the user anything, and ask only what the material cannot answer. The questions
   that usually survive are the storyline pick, the aspect ratio, the voice, and any paid generation.

2. **Plan the series with motion-craft, on the kit.** Look for a series that came before
   (`references/brief-and-claims.md` §1), then start this one with `scripts/new_series.py <dir> --fetch`. To study the
   source series, or to rebuild it, start with `--reference` instead (`kit/reference/README.md`). Invoke
   `motion-craft:motion-craft` and read its `references/saas-films.md` and `references/story-and-rhythm.md`. Run its
   storyline step for the overview: three storylines, one recommended. The shorts share one grammar and need no
   storylines of their own. Write the film table in `films.py` and its summary in `SERIES.md` per
   `references/picture.md` §1. The pace factors and the label switch go in `series.json` from the start, because
   owners change both.

3. **Words.** Invoke the voice skill for the brand that bylines the videos: the one the user names, or the one their
   own instructions route that brand to. With no brand voice skill, write the copy yourself to
   `references/voice-and-music.md` §1. Write `lines.json` (narration) and `respell.json` (how the voice must say
   names), and draft the page copy in `site.json` in the same pass so the words agree.

4. **Build picture-first.** Follow `references/picture.md`. Scenes time to the picture, and narration is placed
   afterwards at scene offsets. Build the product's screens in `states.py` as live HTML from its own interface kit,
   inside a chat host's frame or the product's own window (`picture.md` §3), and open `states/index.html` before
   building a scene. Invoke `design-craft:design-craft` for the lockup, the end slide and any frame the product's kit
   does not cover. Invoke `ux-craft:ux-craft` on each workflow shown and write one line per workflow in `REVIEW.md`:
   its states, its approval step, and whether a real user could follow it in that order. Run `python3 films.py` on
   its own and read its exit, then `_kit/engine/build.py . <id> --mute-only` per film, `hf.sh check`, and
   `hf.sh snapshot --at <every step boundary> --no-end` for a contact sheet. Open each sheet and list every defect it
   shows (the checks in `picture.md` §9) under "Weakest shots" in `REVIEW.md`, with its time and measured text size,
   before the first render. Run `series_lint.py serif` and `collisions` too.

5. **Voice, music and the mix.** Follow `references/voice-and-music.md`. Price the narration with
   `scripts/gateway_audio.py lines --dry-run` and the music beds with `gateway_audio.py music --dry-run`, show the
   user the cost, and generate after their yes. Each film gets two mixes from one cue sheet: `sound.wav` (bed and
   effects) and `sound_vo.wav` (the bed ducked under the voice by `duck.py`).

6. **Render once, remux, gate, then publish.** Rebuild with the voice, then read `sync_table.py films/<id>` for every
   film. Then `_kit/engine/render.py . --to delivery site/films` builds, renders each film once into `staging/`,
   remuxes its voiced cut from the same picture (through the limiter when the film table gives it `limit`), checks
   each film's size, and publishes both cuts only when `delivery.py` passes every film. `delivery.py check --dir
   delivery … --published published.txt` then confirms no shared name is gone. Read each exit code on its own line; a
   pipe into `tail` reports tail's.

7. **Publish the site.** Follow `references/site.md`. `_kit/site/build_site.py . --posters` writes the overview and
   shorts pages, the posters, the share image, the cache headers and `robots.txt` from `site.json`. Invoke
   `design-craft:design-craft` and `ux-craft:ux-craft` for any page the builder does not make and for changes to it,
   and `design-review:design-review` on the rendered pages before deploying. Run `scripts/site_urls.py check site`
   after every page build. Deploy only when the user has authorized publishing this series. That yes carries across
   rounds until they withdraw it. After a deploy, fetch the live URLs and confirm they serve the new bytes.

8. **Report.** Inside a `~/Dev` project, invoke `status-update:status-update` and reply in its two lines.
   Elsewhere, invoke `agent-voice:agent-voice` for the work-report register and reply in 3-6 lines: what changed,
   where it is live, what was measured, and what nobody checked. Nobody has listened to the mix at full speed on
   speakers unless someone did, so say that.

9. **Rounds.** Read `references/rounds.md` before acting on any note. Re-read every message since the last render,
   tool results included, before planning and before rendering. Search the whole series for the exact string a note
   quotes (scripts, voice input, pages, posters, share image). When the owner flags something on one surface, check
   its twin on the others; when they say it is still wrong, look for the second place it lives. After a re-render,
   `compare_films.py` against the previous published files shows what changed, and where.

## The numbers that bind

These hold unless `SERIES.md` overrides one and says why. The sources are in `references/evidence.md`.

- **Lengths.** The overview runs 80-110 s and the shorts 20-25 s each; no scene runs past 25 s. Narration is at
  most 130 spoken words for the overview and one line of 24-35 words for each short.
- **Reading.** A line or result meant to be read holds 0.5 s plus 0.3 s a word, counted from when its last word
  lands. A typed prompt types at 52 characters a second and holds 0.6 s before the press; the sent message stays in
  the thread, so its reading hold runs on from the send. Interface text the viewer must read reaches 2.6 % of the
  frame's short side, 28 px at 1080p.
- **Pace.** Something on screen changes every 1-3 s, and nothing holds still past 4 s. The one exception is a short's
  closing push: a still run that starts at or after its `settle_push` and runs to the end is disclosed as accepted;
  every other still run past 4 s is fixed. The pace factors live in `series.json`; start at 1.2-1.3: in the source run
  the owner called factor 1.0 "very fast, … hard to keep track of" and approved 1.3 for the overview, 1.22 for the
  shorts and 1.15 for the opener.
- **Openings.** Frame 0 shows a complete line or the product working, never text partway through typing in. The
  overview's first screen carries the brand mark.
- **Endings.** The overview ends on an end slide: the lockup, one line, and the ask as text (a URL or "Book a
  demo"), with the mark held still for 3-5 s. A short ends on its own result, held with a slow push under a small
  lockup bar over its last 3.2 s, and never on a card that repeats the headline.
- **Vertical.** A 9:16 film keeps every must-carry fact, the lockup bar and the end slide inside the area TikTok,
  Reels and Shorts all leave clear, about x 120-780 and y 290-1250 on 1080 x 1920; the kit frames into it.
- **Sound.** Every encoded file measures -14 LUFS (loudness units relative to full scale) integrated (±0.5) with true
  peak at or below -1 dBTP; that ceiling is the gate. The voice sits about 11 dB over the ducked bed: bed gain 0.28,
  0.10 under the voice.
- **Cuts.** The muted master and the voiced cut of a film are one render and one remux. `delivery.py check` fails when
  their pictures differ, and when the voiced cut's sound is the master's (no narration mixed in).
- **Names.** A published file name never changes. Every page reference carries `?v=` plus the first 10 hex digits
  of the file's SHA-1, so a republished file under the same name is fetched fresh.
- **Alignment.** A lockup beside text (a page header, the lockup bar) shares that text's baseline, measured inside the
  text, within 1 px.

## Routing

| Need | Use |
|---|---|
| Storylines, rendering, the sound engine, the pop scan | `motion-craft:motion-craft` |
| The lockup, the end slide, frames the product's kit lacks, pages the site builder does not make | `design-craft:design-craft` |
| Whether a workflow shown is real and followable; the site's player and modal | `ux-craft:ux-craft` |
| Review of the rendered site before deploy | `design-review:design-review` |
| Narration, page copy and short descriptions in the brand's voice | the brand's voice skill, the one the user names |
| Any question for the user | `clarify:clarify` first |
| The end-of-work report in a `~/Dev` project | `status-update:status-update` |
| This skill's own written files (REVIEW.md, SERIES.md) and the reply | `agent-voice:agent-voice` |

## Constraints

- **No spending without a yes.** Narration, transcription and music are paid calls. Show the `--dry-run` line count,
  characters or seconds, and cost, then wait, every time, unless `SERIES.md` records the owner's standing yes for
  re-voices and its cap in their words. The source run spent under US$2 on voice and US$0.33 on music across five
  rounds.
- **The gateway key stays secret.** Read it from `AI_GATEWAY_API_KEY`, which the scripts never print or write.
  Export it from wherever the project keeps it without echoing it, and never paste it into a brief, a file or a
  command line.
- **Show only what is built.** Every capability on screen has a row in `CLAIMS.md` marked built. An owner can
  override that, and the override goes in `CLAIMS.md` with the date and their words.
- **Invent nothing about a real company.** With a real client on screen, every figure, date and holder comes from its
  filings, and no event, statement, plan, deal, meeting or trade is invented for it or for any named real person or
  institution. This holds whatever the owner's tolerance for risk, because the page is public and the fabrication
  would be about someone else. Whether a public page may show the company at all is the owner's call: ask.
- **Hold the scope.** Make the films and pages asked for. Add no extra aspect ratios, captions, languages or
  pages unless asked.
- **One session builds every film.** Continuity (one scenario, one lockup, one pace) breaks when films are split
  across agents. The only delegation is the ideation branches motion-craft spawns at its storyline step.
- **Never publish without authorization**, and never push a repository without being asked.
- **Shell habits that cost rounds.** Run loops that split a variable under `bash -c` (zsh does not word-split, so a
  loop over film ids processed one item). Use absolute paths in every build and render command (the working
  directory resets between calls, and edits ran twice in the wrong folder). Write patches to JavaScript as a script
  file (a heredoc containing `.delete(` was refused by a safety check). Read every gate's exit code on its own line.

## References

| File | Read it when |
|---|---|
| `references/brief-and-claims.md` | Step 1: the brief, the claims ledger, the scenario, a real company, names and pronunciation, labels |
| `kit/README.md` | Step 2: what the kit holds, which files are the series', and the defaults it carries |
| `kit/reference/README.md` | Rebuilding or studying the source series, and what it proves |
| `references/picture.md` | Steps 2 and 4: the film table, frames for any product, motion, holds, openings and endings, 9:16, captions, the lockup, traps |
| `references/voice-and-music.md` | Steps 3 and 5: the narration register, voices, generation, placement, music beds, the mix |
| `references/site.md` | Step 7: the site builder, players, the shorts modal, an interactive demos page, posters, caches, copy, access, deploy |
| `references/rounds.md` | Step 9 and every owner note: reading notes, finding the second place, reversals, reporting |
| `references/evidence.md` | Where a number or rule comes from |
