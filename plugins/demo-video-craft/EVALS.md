# Evals

**No comparison against working without the skill has been run.** The create-skill pipeline asks for one: the same prompts given to a runner with the skill and to one without, graded on structural assertions and then judged blind by a model panel. For this release the owner chose mechanical checks only, so that comparison is still open and nothing below should be read as evidence that the skill makes better videos than no skill would.

What was verified is that the eight scripts and the starter kit do what they say, on fixtures built to break them, on the kit's own example series, and on the finished files of the series the skill was built from.

## 1. Script self-tests

Each script builds its own fixtures and proves its check fails on a known-bad case. Run all eight with:

```bash
evals/run_mechanical.sh        # mechanical: PASS 8/8, exit 0
```

| Script | Cases | What the failing fixtures are |
|---|---|---|
| `gateway_audio.py --self-test` | 6 of 6 | respelling rules in the wrong order (the possessive never fires), a word containing the name, caption tags, a stale cache key, a missing gateway key that must stop before any request |
| `duck.py --self-test` | 7 of 7 | ducking mid-line, two lines 0.8 s apart (the bed must not swell between them), silence at frame 0 and at the end, the muted master at full bed |
| `site_urls.py --self-test` | 6 of 6 | an unversioned reference, a page built before a republish (stale hash), a missing file, an absolute URL on the site's origin, a reference inside inline JSON, a page with no references at all (not a pass) |
| `delivery.py --self-test` | 8 of 8 | a missing voiced cut, a voiced cut rendered separately (different picture), a voiced cut 8 dB hot, a published name that disappeared, a publish with one failing film (nothing may be copied), a publish to two destinations, a tiled frame sheet's size |
| `edgar.py --self-test` | 3 of 3 | a 13G cover page parsed, a release's text unescaped and split, a missing tag read as empty rather than an error |
| `new_series.py --self-test` | 10 of 10 | a series started in a temporary folder: the screens and the film table run, the preview carries the mark and the icons, the overview's scenes, both films' lengths, the lockbar switches, the short ends on its settling push, a card landing carries a pop, the opener is a stage scene, a second start refuses to overwrite, and the length gate refuses a short outside its range before writing anything |
| `sync_table.py --self-test` | 3 of 3 | a line on its picture, a line running past its scene, two lines overlapping |
| `series_lint.py --self-test` | 6 of 6 | serif declarations in CSS and in a Python string, an allowed lockup file, an unscoped film rule on a product class, a retired name, ticker and colour, a word inside another word (not a hit) |

49 cases, all passing, measured on 25 November 2026 with Python 3, ffmpeg and ffprobe.

## 1b. The starter kit, end to end

```bash
MOTION_CRAFT_SCRIPTS=<motion-craft>/scripts evals/run_kit_example.sh
check-O.json: ok=True errors=0 warnings=0
check-K01.json: ok=True errors=0 warnings=1        # container_overflow on the camera during a push, which is the camera
delivery: PASS 1/1
kit example: PASS
```

From a clean folder it fetches the pinned fonts and GSAP, writes the example's screens and film table (a 30.6 s overview and a 20.3 s short), builds both, checks both, renders the short in 17 s and gates it. `pop_scan.py` on the render: 0 pops, 0 still runs. The first build raised four warnings that went back into the kit as fixes: a stage step leaking `dur` into GSAP, a travelling lockup overlapping its twin, a 451-line composition, and a review tint over a grey caption at 4.15:1.

## 2. Real data from the source run

The source run: an AI connector that works inside Claude and ChatGPT, made for one US advisory firm over five rounds on 24-25 November 2026, ending with a 1:41 overview and nine shorts of 21-25 s, each muted and voiced, on a small video site, the last round on a real US-listed company's filings.

**`delivery.py check` on the finished files:**

```text
delivery.py check --dir films --prefix <series> --films O,K02,…,K10 --published published.txt
delivery: PASS 10/10
```

Every pair shares one video stream, both cuts are 1920x1080, every file measures -14.0 LUFS, and true peak sits between -1.1 and -2.6 dBTP.

**`site_urls.py check` on the live site's pages** found three stale references: the share image on the overview and shorts pages, and the menu page's poster. All three files had been replaced under the same name during that day's republish, and none of the references carried a hash, so a cached copy would still be served. The menu poster still showed the brand lockup the owner had already rejected.

```text
urls: FAIL 67/69 references current      # overview and shorts pages, share image unversioned
urls: FAIL 0/1 references current        # menu page, poster unversioned
urls: PASS 70/70 references current      # after versioning all three
```

**The kit's checks, pointed back at the source run**, found two faults in films the owner had already seen. Measured inside the text, the lockup sat 6.7 px above the nav links on one page and 4.4 px on the others, and about 5 px below the button text in every short's lockup bar; and every short's bar sat with its left edge at the frame's centre, because one `gsap.set` cancelled its centring. Both fixed, the nine shorts re-rendered under the same names, and `delivery.py publish` refused the set until one voiced cut at +1.3 dBTP had been limited:

```text
delivery: FAIL 8/9          # K07 voiced cut, true peak +1.3 dBTP after AAC
delivery: PASS 9/9          # after remux --limit 0.6; publish copied 18 files
delivery: PASS 10/10        # the whole published set
```

**`series_lint.py serif`** on the source run's kit and pages found 10 serif declarations, among them base rules in the host frame that later rules overrode. They are a trap rather than a defect in the films as rendered, and the owner had asked twice for every serif to go.

**`duck.py`** was written from the source run's mixing logic and its self-test failed on the first run: when two narration lines sat under about 0.9 s apart, the next line's pre-dip point landed inside the first line's span and the bed crept back up to about 0.18 under the voice. The source run's own scoring code had the same logic. The script now merges close dips.

## 3. What would settle it

`evals/evals.json` carries four prompts with their assertions, written for the with-skill and no-skill comparison:

1. **full-series-connector**: a Slack app's overview and six shorts, muted and voiced, published; 12 assertions, from the claims ledger to `delivery.py check` passing 7 of 7.
2. **revision-round-pronunciation-and-lockup**: a mispronounced name and a lockup still wrong in the videos after a page fix, republished under the same names; 8 assertions.
3. **republish-without-breaking-links**: one changed word on one short, re-rendered and pushed while a YouTube description links straight to the MP4; 5 assertions.
4. **near-miss-single-sting**: a 6 s logo sting, which should route to motion-craft rather than start a series; 2 assertions.

Prompts 2 and 3 are the ones most likely to separate the arms, because they test the failure the skill exists for: a fix that lands in one place and not the others.

## 4. Caveats

- The starter kit's example proves the kit runs, not that a new series made from it is good. It has one workflow and no voice, and no new series has yet been made from the kit.
- One source run, made by the same session that wrote the skill. Its lessons are real, and they are also one product, one owner and one audience.
- Nobody has listened to the source run's final mix at full speed on speakers. The loudness figures above are measurements, not a listen.
- The icon was refined over two measured rounds against a raster reference, and no blind judge panel was run on it. Its audit sheet is `assets/audit.html`.
