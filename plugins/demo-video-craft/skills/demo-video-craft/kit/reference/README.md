# The reference series

The series this skill was built from, as published on 25 Nov 2026: an overview of 1:41 and nine shorts of 21.1-25.0 s
for Diolog Guardian, an AI connector shown inside Claude and ChatGPT, every screen filled with lululemon athletica inc.
(Nasdaq: LULU) from its public filings (`SOURCES.md`). Its screens (`states.py`) and film table (`films.py`) are the
published ones, ported onto the kit unchanged; only the machinery is the kit's.

It is here for two jobs. It is the fullest example of the grammar: every op in `picture.md` is used in one of its
films, so read `films.py` for how a deck rolls forward, a document is dragged in, a side panel opens, two windows share
a camera, or a figure is caught and fixed. And it proves the kit: rebuilt with nothing but the kit, its ten films
match the published files almost frame for frame.

## Rebuild it

```bash
python3 scripts/new_series.py ./guardian --reference --fetch   # the kit, this series, the fonts it rendered with
cd guardian
python3 fetch_marks.py            # Claude, ChatGPT and lululemon's marks, fetched rather than committed
python3 states.py && python3 films.py
```

Its voice and music are generative, so they are not committed and cannot be regenerated identically. Either copy the
series' own files into `voice/` (the 18 lines `gateway_audio.py` made: `<line>.wav`, `.json`, `.mp3`) and `music/`
(`overview.wav`, `shorts.wav`), or regenerate them: `gateway_audio.py lines --script lines.json --out-dir voice
--respell respell.json` (18 lines, 2,566 characters, about US$0.22; `--dry-run` prints that before anything is sent) and the two beds with the prompt in
`references/voice-and-music.md` §5 (about US$0.33). Regenerated audio places the same lines at the same offsets; the
picture does not depend on it. Then:

```bash
MOTION_CRAFT_SCRIPTS=<motion-craft>/scripts python3 _kit/engine/render.py . --to out
python3 <skill>/scripts/compare_films.py --a out --b <the published films> --prefix guardian3 \
    --films O,K02,K03,K04,K05,K06,K07,K08,K09,K10
```

## What it measured

On 25 Nov 2026, with the series' own voice and music files, `render.py` published all ten (`delivery: PASS 10/10`;
K07 through its film-table limiter, -14.3 LUFS / -3.6 dBTP), and `compare_films.py` against the published files:

| Film | Mean SSIM | Lowest frame |
|---|---|---|
| O (1:41) | 0.9997 | 0.9986 at 64.4 s |
| K02 | 0.9996 | 0.9990 |
| K03 | 0.9998 | 0.9985 |
| K04 | 0.9997 | 0.9987 |
| K05 | 0.9994 | 0.9988 |
| K06 | 0.9997 | 0.9987 |
| K07 | 0.9994 | 0.9987 |
| K08 | 0.9997 | 0.9986 |
| K09 | 0.9995 | 0.9988 |
| K10 | 0.9997 | 0.9990 |

SSIM 1.0 is identical. The residue is encoder noise and one deliberate change: the kit's opener hides the node's
lockup until the travelling one lands, where the published opener let the two overlap for about 0.2 s (HyperFrames
flagged it as `content_overlap`). The audio differs slightly too: the kit's duck merges dips for lines under 1.5 s
apart, which the published mix did not.

## What is not here

The features page (`guardian.diolog.app/features`, an interactive tour of the product's cards) is not a video and the
kit does not build it; `references/site.md` §3b holds the rules it was built to. The voice, the music beds and the
third-party marks are fetched or regenerated rather than committed.
