# Evals

**No comparison against working without the skill has been run.** The create-skill pipeline asks for one: the same prompts given to a runner with the skill and to one without, graded on structural assertions and then judged blind by a model panel. For this release the owner chose mechanical checks only, so that comparison is still open and nothing below should be read as evidence that the skill makes better videos than no skill would.

What was verified is that the four scripts do what they say, on fixtures built to break them and on the finished files of the series the skill was built from.

## 1. Script self-tests

Each script builds its own fixtures and proves its check fails on a known-bad case. Run all four with:

```bash
evals/run_mechanical.sh        # mechanical: PASS 4/4, exit 0
```

| Script | Cases | What the failing fixtures are |
|---|---|---|
| `gateway_audio.py --self-test` | 6 of 6 | respelling rules in the wrong order (the possessive never fires), a word containing the name, caption tags, a stale cache key, a missing gateway key that must stop before any request |
| `duck.py --self-test` | 7 of 7 | ducking mid-line, two lines 0.8 s apart (the bed must not swell between them), silence at frame 0 and at the end, the muted master at full bed |
| `site_urls.py --self-test` | 6 of 6 | an unversioned reference, a page built before a republish (stale hash), a missing file, an absolute URL on the site's origin, a reference inside inline JSON, a page with no references at all (not a pass) |
| `delivery.py --self-test` | 5 of 5 | a missing voiced cut, a voiced cut rendered separately (different picture), a voiced cut 8 dB hot, a published name that disappeared |

24 cases, all passing, measured on 25 November 2026 with Python 3, ffmpeg and ffprobe.

## 2. Real data from the source run

The source run: an AI connector that works inside Claude and ChatGPT, made for one US advisory firm over four rounds on 24-25 November 2026, ending with a 1:41 overview and nine shorts of 21-25 s, each muted and voiced, on a small video site.

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

**`duck.py`** was written from the source run's mixing logic and its self-test failed on the first run: when two narration lines sat under about 0.9 s apart, the next line's pre-dip point landed inside the first line's span and the bed crept back up to about 0.18 under the voice. The source run's own scoring code had the same logic. The script now merges close dips.

## 3. What would settle it

`evals/evals.json` carries four prompts with their assertions, written for the with-skill and no-skill comparison:

1. **full-series-connector**: a Slack app's overview and six shorts, muted and voiced, published; 12 assertions, from the claims ledger to `delivery.py check` passing 7 of 7.
2. **revision-round-pronunciation-and-lockup**: a mispronounced name and a lockup still wrong in the videos after a page fix, republished under the same names; 8 assertions.
3. **republish-without-breaking-links**: one changed word on one short, re-rendered and pushed while a YouTube description links straight to the MP4; 5 assertions.
4. **near-miss-single-sting**: a 6 s logo sting, which should route to motion-craft rather than start a series; 2 assertions.

Prompts 2 and 3 are the ones most likely to separate the arms, because they test the failure the skill exists for: a fix that lands in one place and not the others.

## 4. Caveats

- One source run, made by the same session that wrote the skill. Its lessons are real, and they are also one product, one owner and one audience.
- Nobody has listened to the source run's final mix at full speed on speakers. The loudness figures above are measurements, not a listen.
- The icon was refined over two measured rounds against a raster reference, and no blind judge panel was run on it. Its audit sheet is `assets/audit.html`.
