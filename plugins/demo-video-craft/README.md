<p align="center">
  <img src="assets/banner.png" alt="demo-video-craft: a porcelain icon of a graphite video screen with a vermilion play triangle and a cursor pressing it, beside the wordmark and the line 'Product demo videos, muted and voiced from one render, published without breaking a link'" width="100%">
</p>

<h1 align="center"><img src="assets/icon-256.png" alt="" width="34" valign="middle" /> demo-video-craft</h1>

<p align="center"><strong>A product's demo video series, from brief to a published page.</strong><br />
One overview and a set of shorts, each muted and voiced from a single render, kept in step through every round of notes.</p>

<p align="center">
  <img alt="Version 0.3.0" src="https://img.shields.io/badge/version-0.3.0-D33C21">
  <img alt="Skill: demo video series" src="https://img.shields.io/badge/skill-demo_video_series-434A55">
  <img alt="Scripts: 9, each with a self-test" src="https://img.shields.io/badge/scripts-9_self--tested-756E60">
  <img alt="Ships a starter kit" src="https://img.shields.io/badge/starter_kit-included-434A55">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## The problem it solves

Making one good product video is a solved problem; `motion-craft:motion-craft` does that. A **series** is a different job. You need an overview and five to ten shorts that all show the same fictional customer and the same figures, each one with and without a narrator, all of it on a page a prospect can open, and then you need it to survive five rounds of notes from whoever owns the product.

That last part is where it falls over. In the run this skill was built from, the brand lockup got fixed on the pages and stayed wrong in the videos. A corrected voice line kept playing the old reading, because the browser had cached the file under the same name. The share image still showed the first round after the site had been rewritten three times. Every check that ran had passed.

So this skill keeps **one source for each thing that shows up in more than one place**, and it checks the finished files rather than the code that made them.

It also ships the source series' engine as a **starter kit**. How close a new series gets to the one this was built from depends on the actual values (how far the camera pushes in, how fast a prompt types, how long a result holds, how the pace stretches) far more than on a description of them, so a new series starts from the code rather than from prose.

## What it does

`demo-video-craft:demo-video-craft` runs a series through nine steps, routing each to the skill that already owns it:

1. **Brief and claims.** It reads the product's own record first and writes down what is actually built. Anything unbuilt stays off screen. It picks one fictional company, checks the name and ticker are free on the exchange's register, and reuses its people and figures on every screen. When the owner names a real company instead, every figure, date and holder comes from its filings, and nothing is invented about it.
2. **Plan with motion-craft, on the kit.** `new_series.py` copies the kit and a small example series into a new folder. Three storylines for the overview and one shared grammar for the shorts, all in a single film table with a **pace factor** and a **label switch** built in from the start. Owners change both, and in the source run one went from "pick up the pace" to "very fast, hard to keep track" in two rounds.
3. **Words** through the brand's own voice skill: second person, outcome first, at most 130 spoken words for the overview and one line of 24-35 words per short.
4. **Picture first.** Scenes are timed to the picture and the narration is placed afterwards, so one render serves both cuts. When the product lives inside another app (a Claude or ChatGPT connector, say), the films stay inside a lookalike of that app, with the product's own screens rebuilt as live HTML so the camera can push in 3x and stay sharp.
5. **Voice and music** from ElevenLabs through Vercel AI Gateway. **Respellings** change only what the voice is sent, never the captions or the pages, so a name said as "Clawd" is still written "Claude". The music bed ducks under the voice by about 11 dB.
6. **Render once, remux, gate, then publish.** The voiced cut is the muted master with its audio swapped, never a second render. Everything renders into a staging folder, and nothing is copied live until every film passes.
7. **Publish** a small video site: an overview page, a shorts modal that grows from its thumbnail, and **permanent file names** with a content hash on every URL, so a republish never breaks a shared link or serves a stale copy.
8. **Report**, including what nobody checked. Loudness numbers are not a listen.
9. **Rounds.** Read every queued note before rendering, search the whole series for the exact words a note quotes, check the same thing on every other surface it appears on, and when the owner says something is still wrong, look for the second place it lives.

## What it ships with

The starter kit in `skills/demo-video-craft/kit/`: the window and stage runtimes, the film table's pace and hold machinery, the screen builder, the build and the score, a one-command render-and-publish step, and the site builder. It works for a product shown inside a chat app or in its own browser window, desktop window or phone, at 16:9 or 9:16, with captions cut from the narration's own word timings when a film asks for them.

Two series come with it. The **example** is a fictional product in four films: a short inside Claude, one in its own browser window, a 9:16 one on a phone, and the overview. The **reference** is the series this skill was built from, its 36 screens and ten films ported unchanged, which the kit rebuilds almost frame for frame. Read its film table to see how any shot in the published series was made.

And nine Python scripts, each with `--self-test`, which builds its own fixtures and proves the check fails on a known-bad case. A `gemini.md` carries the extra steps for a run on Gemini.

| Script | What it does |
|---|---|
| `new_series.py` | Starts a series from the kit, and fetches the pinned fonts and GSAP |
| `delivery.py` | Makes the voiced cut; `check` gates a folder (both cuts, one shared picture, -14 LUFS ±0.5, true peak at or below -1 dBTP, no published name gone); `publish` copies only when everything passes; `sheet` tiles stamped frames to look at |
| `sync_table.py` | Prints each narration line beside what is on screen while it plays, and fails a line that runs past its scene |
| `series_lint.py` | Finds serif faces in any font declaration, film styles that reach the product's own markup, and retired colours or names |
| `site_urls.py` | Every video, poster and share-image reference on every page carries `?v=` and the hash of the file now on disk |
| `gateway_audio.py` | Narration, word timings and music through the gateway, with respellings applied in order and the cost printed before you spend more |
| `duck.py` | The music bed's gain curve under the narration |
| `compare_films.py` | Measures a rebuilt film against the published one frame by frame, and shows where a re-render changed |
| `edgar.py` | A real US-listed client's figures, filing dates and holders from SEC EDGAR, when the owner wants a real company on screen |

## Does it actually work?

**No comparison against working without the skill has been run.** For this release the owner chose mechanical checks only, so there is no blind taste test and no report card yet. What has been verified:

- **The kit rebuilds the series it came from almost frame for frame.** Rebuilt with nothing but the kit and the series' own voice and music files, the ten films measure a mean SSIM of 0.9994-0.9998 against the published files, where 1.0 is identical, and no frame falls below 0.9985. That's `evals/run_reference.sh`.
- All nine self-tests pass, 57 cases between them. Run `evals/run_mechanical.sh` to repeat it.
- The kit's example series builds, checks and renders from a clean start: four films with 0 errors in HyperFrames' check, and a 16:9 short and a 9:16 short rendered with 0 pops and 0 still frames. That's `evals/run_kit_example.sh`.
- `delivery.py check` on the source run's finished files: **PASS 10/10**, every pair sharing one picture, every file at -14.0 LUFS with true peak between -1.1 and -2.6 dBTP.
- `site_urls.py check` on the source run's live site found **3 stale references** nobody had noticed: the share image on two pages and the menu page's poster, all carrying no hash after their files had been replaced. After the fix it reads 70 of 70 current.
- Building the kit, and measuring the way the skill now asks, found two faults in the source run's own published films: every short's closing lockup bar sat off centre, and the lockup sat off its neighbouring text's baseline in every short and on every page header (6.7 px on one page). Both were fixed and republished. `delivery.py publish` then held back the whole set while one voiced cut measured +1.3 dBTP, and published 9 of 9 once it was fixed.
- `series_lint.py serif` on the source run's kit found 10 serif declarations still on disk after the owner had asked for every serif to go; the films rendered in sans only because later rules overrode them.
- Writing `duck.py` found a bug in the source run's own mixing logic: when two narration lines sat less than about 0.9 s apart, the bed crept back up under the first one. The script merges those dips, and a self-test case holds it there.

The source run was a real one: an AI connector that works inside Claude and ChatGPT, made for one US advisory firm over five rounds on 24-25 November 2026, ending with a 1:41 overview and nine shorts of 21-25 s, the last round on a real US-listed company's public filings. Fifteen agents read the whole session, about 12,300 lines, to find what this version adds. `evals/evals.json` carries the six prompts that would settle the open question. [EVALS.md](EVALS.md) has the detail.

## What it won't do without asking

It shows the cost of every paid voice and music call and waits for a yes. It never publishes or deploys without your authorization, never prints the gateway key, and never pushes a repository.

## Install

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install demo-video-craft@fledgeling-plugins
/plugin install motion-craft@fledgeling-plugins
```

Needs motion-craft (it renders through motion-craft's HyperFrames wrapper and sound engine), plus Node, ffmpeg and Python 3, and a Vercel AI Gateway key in `AI_GATEWAY_API_KEY` for the voice and music.

## References

- [`skills/demo-video-craft/SKILL.md`](skills/demo-video-craft/SKILL.md): the procedure and the numbers that bind.
- [`kit/README.md`](skills/demo-video-craft/kit/README.md): what the starter kit holds and the defaults it carries.
- [`references/brief-and-claims.md`](skills/demo-video-craft/references/brief-and-claims.md), [`picture.md`](skills/demo-video-craft/references/picture.md), [`voice-and-music.md`](skills/demo-video-craft/references/voice-and-music.md), [`site.md`](skills/demo-video-craft/references/site.md), [`rounds.md`](skills/demo-video-craft/references/rounds.md): the depth, one file per job.
- [`references/evidence.md`](skills/demo-video-craft/references/evidence.md): where each rule comes from, from the source run and from motion-craft's study of 48 shipped SaaS product films.
