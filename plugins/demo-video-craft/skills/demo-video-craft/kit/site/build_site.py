#!/usr/bin/env python3
"""The video site: an overview page (the lead video and the shorts, each opening in a modal that grows from its
thumbnail) and a shorts page (every short with its description and voiceover text), from the series' films.

    python3 _kit/site/build_site.py <series dir> [--posters]

Reads series.json (prefix, lockup words, the ask), site.json (the site's address, the ask's link, the nav, each film's
page description, the shorts' order, each page's heading and lede, the footer's disclosure, poster times), lines.json
(the voiceover text under each player) and the published voiced cuts in site/films/. Writes site/overview.html,
site/shorts.html, the posters and the share image (--posters regenerates them all from the current films: do it
whenever the picture changed), site/assets/ (fonts, lockup.css, the mark), and, when absent, vercel.json (videos
revalidate on every request, pages are never cached, nothing is indexed) and robots.txt.

Every video, poster and share-image reference carries ?v= and the file's SHA-1, so a republished file under its
permanent name is never served from a stale cache; run scripts/site_urls.py check over the site afterwards. Players are
voiced-only: the source series' owner removed the muted/voiced switch. The page, player and modal code is the source
series' own, as published and tested (FLIP open from the thumbnail, Previous/Next, arrow keys, Escape, reduced motion).
"""
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
if len(ARGS) != 1:
    sys.exit(__doc__.split('\n\n')[1])
ROOT = Path(ARGS[0]).resolve()
HERE = ROOT / 'site'
SERIES = json.loads((ROOT / 'series.json').read_text())
CFG_SITE = json.loads((ROOT / 'site.json').read_text())
PREFIX = SERIES['prefix']
BLOB = '/films'
SITE = CFG_SITE['origin'].rstrip('/')
DEMO = CFG_SITE['ask_url']
e = html.escape
_tag = re.compile(r"\[[^\]]+\]\s*")

films = {}
for ln in json.loads((ROOT / SERIES['voice']['lines']).read_text())['lines']:
    films.setdefault(ln['film'], {'lines': []})['lines'].append(ln['text'])
for fid in films:
    plan = json.loads((ROOT / 'films' / fid / 'plan.json').read_text())
    films[fid]['title'] = plan['title']
DESC, ORDER, OVERVIEW = CFG_SITE['descriptions'], CFG_SITE['order'], SERIES['overview']
missing = [f for f in [OVERVIEW, *ORDER] if f not in DESC]
if set(ORDER) | {OVERVIEW} != set(films) or missing:
    sys.exit(f'site.json must order every short and describe every film in lines.json (missing descriptions: {missing})')

HERE.mkdir(exist_ok=True)
(HERE / 'assets' / 'posters').mkdir(parents=True, exist_ok=True)
shutil.copytree(ROOT / 'assets' / 'fonts', HERE / 'assets' / 'fonts', dirs_exist_ok=True)
shutil.copy(ROOT / 'lockup.css', HERE / 'assets' / 'lockup.css')
shutil.copy(ROOT / 'marks' / 'mark.svg', HERE / 'assets' / 'mark.svg')
_mark = (ROOT / 'marks' / 'mark.svg').read_text()
_vb = re.search(r'viewBox="([^"]+)"', _mark).group(1)
_inner = re.search(r'<svg[^>]*>(.*)</svg>', _mark, re.S).group(1)
LOCKUP = (f'<span class="k-lock"><svg class="mk" viewBox="{_vb}" aria-hidden="true">{_inner}</svg>'
          f'<span class="wm">{e(SERIES["lockup"]["wordmark"])}</span><span class="sep" aria-hidden="true"></span>'
          f'<span class="pn">{e(SERIES["lockup"]["product"])}</span></span>')
FOOTER = '\n'.join(f'  <p>{p}</p>' for p in CFG_SITE['footer'])


def ver(rel):
    """A site path with ?v=<content hash>: the file name stays the same (it may be linked to) while a republished file
    is never served from an old cached copy."""
    f = HERE / rel.lstrip("/")
    if not f.exists():
        raise SystemExit(f"{rel} is missing")
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return f"{rel}?v={h.hexdigest()[:10]}"


def duration(fid):
    for name in (f"{PREFIX}-{fid}.mp4", f"{PREFIX}-{fid}-vo.mp4"):
        if not (HERE / "films" / name).exists():
            raise SystemExit(f"site/films/{name} is missing; publish it with _kit/engine/render.py --to delivery site/films")
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(HERE / "films" / f"{PREFIX}-{fid}.mp4")], check=True, capture_output=True, text=True).stdout)


SECONDS = {k: duration(k) for k in films}


def poster_time(fid):
    t = CFG_SITE.get('poster_at', {}).get(fid)
    return float(t) if t is not None else max(0.5, SECONDS[fid] - 3.7)   # a short: 0.5 s before its lockup bar


def make_posters():
    """Every poster from the current voiced cut (the picture is the same in both), and the share image from the
    overview's poster frame, cropped to 1200 x 630."""
    for fid in films:
        out = HERE / 'assets' / 'posters' / f'{PREFIX}-{fid}.webp'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{poster_time(fid):.2f}', '-i', str(HERE / 'films' / f'{PREFIX}-{fid}-vo.mp4'),
                        '-frames:v', '1', '-vf', 'scale=1280:-1', '-c:v', 'libwebp', '-quality', '82', str(out)], check=True)
    w, h = (json.loads((ROOT / 'films' / OVERVIEW / 'plan.json').read_text()).get('size') or [1920, 1080])
    off = (round(1200 * h / w) - 630) // 2
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{poster_time(OVERVIEW):.2f}', '-i', str(HERE / 'films' / f'{PREFIX}-{OVERVIEW}-vo.mp4'),
                    '-frames:v', '1', '-vf', f'scale=1200:-2,crop=1200:630:0:{max(0, off)}', '-q:v', '3', str(HERE / 'og.jpg')], check=True)
    print(f'{len(films)} posters and og.jpg from the current films')


if '--posters' in sys.argv or not (HERE / 'og.jpg').exists():
    make_posters()
absent = [f for f in films if not (HERE / 'assets' / 'posters' / f'{PREFIX}-{f}.webp').exists()]
if absent:
    sys.exit(f'posters missing for {absent}; run with --posters')


def clock(s):
    s = int(s)
    return f"{s // 60}:{s % 60:02d}"


def spoken(s):
    s = int(s)
    m, r = divmod(s, 60)
    parts = ([f"{m} minute" + ("s" if m != 1 else "")] if m else []) + ([f"{r} seconds"] if r else [])
    return " ".join(parts)


def narration(fid):
    body = "".join(f"<p>{e(_tag.sub('', ln))}</p>" for ln in films[fid]["lines"])
    return (f'<details class="narration"><summary>Read the voiceover</summary>'
            f'<div class="narration-body">{body}</div></details>')


def player(fid, lead=False):
    title = films[fid]["title"]
    vo = ver(f"{BLOB}/{PREFIX}-{fid}-vo.mp4")
    return (f'<div class="player{" player-lead" if lead else ""}" data-player>'
            f'<video controls preload="none" playsinline width="1920" height="1080" '
            f'poster="{ver(f"/assets/posters/{PREFIX}-{fid}.webp")}" data-title="{e(title)}" '
            f'data-length="{e(clock(SECONDS[fid]))}" data-spoken="{e(spoken(SECONDS[fid]))}">'
            f'<source src="{vo}" type="video/mp4"><a href="{vo}">Download {e(title)} (MP4)</a></video>'
            f'<p class="player-error" hidden>This video did not load. <a href="{vo}">Open the MP4 directly</a> or reload the page.</p>'
            f'</div>')


def card(fid):
    title = films[fid]["title"]
    return (f'<article class="card" id="{fid.lower()}">{player(fid)}'
            f'<div class="card-text"><h3>{e(title)}</h3><p class="length">{clock(SECONDS[fid])}</p>'
            f'<p class="desc">{e(DESC[fid])}</p>{narration(fid)}</div></article>')


clips = "\n".join(card(f) for f in ORDER)
O = films[OVERVIEW]["title"]


def render(slug, title, desc, og, nav, main):
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{slug}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{og}">
<meta property="og:url" content="{SITE}/{slug}">
<meta property="og:image" content="{SITE}{ver("/og.jpg")}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F6F7F9">
<link rel="icon" href="assets/mark.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/InterTight.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/Inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{ver("/assets/lockup.css")}">
<style>
@font-face {{ font-family: "Inter Tight"; src: url("assets/fonts/InterTight.woff2") format("woff2"); font-weight: 100 900; font-display: swap; }}
@font-face {{ font-family: "Inter"; src: url("assets/fonts/Inter.woff2") format("woff2"); font-weight: 100 900; font-display: swap; }}

/* The series register, as the films use it (override in site.json "css") */
:root {{
  color-scheme: light;
  --bg: #F6F7F9; --surface: #FFFFFF; --ink: #12151C; --ink-2: #3F4654; --muted: #5C6371; --rule: #E4E6EB;
  --navy: #0A1733; --accent: #1F3FA6; --accent-press: #18338A; --ok: #16774A;
  --float: 0 2px 4px rgba(18,21,28,.06), 0 16px 32px -12px rgba(18,21,28,.22);
  --win: 0 2px 6px rgba(18,21,28,.06), 0 40px 80px -30px rgba(10,23,51,.38);
  --r-win: 14px; --r-ctl: 10px;
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-5: 24px; --space-6: 32px;
  --space-7: 48px; --space-8: 64px; --space-9: 96px;
  --measure: 1120px; --gutter: 16px;
  --sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --display: "Inter Tight", "Inter", ui-sans-serif, system-ui, sans-serif;
}}
*, *::before, *::after {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 400 16px/1.55 var(--sans); font-feature-settings: "cv11", "ss01"; }}
::selection {{ background: #DCE4F6; color: var(--navy); }}
a {{ color: var(--accent); text-underline-offset: 3px; text-decoration-thickness: 1px; }}
a:hover {{ color: var(--accent-press); }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 4px; }}
img, video, svg {{ display: block; max-width: 100%; }}
h1, h2, h3 {{ font-family: var(--display); font-weight: 600; color: var(--navy); margin: 0; text-wrap: balance; }}
p {{ margin: 0; text-wrap: pretty; }}
.wrap {{ max-width: calc(var(--measure) + 2 * var(--gutter)); margin: 0 auto; padding: 0 var(--gutter); }}
.skip {{ position: absolute; left: var(--space-4); top: var(--space-4); transform: translateY(-200%); background: var(--surface); padding: var(--space-3) var(--space-4); border-radius: var(--r-ctl); z-index: 10; }}
.skip:focus {{ transform: none; box-shadow: var(--float); }}
.sr-only {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }}

/* Header */
/* The lockup and the nav share one text baseline (owner, 25 Nov: "this alignment is bad"; centring the boxes put the
   wordmark 4.4 px above the links). First baseline, so a nav that wraps on a narrow screen aligns on its first line. */
.top {{ display: flex; align-items: baseline; justify-content: space-between; gap: var(--space-5); padding-top: var(--space-5); padding-bottom: var(--space-5); }}
/* The lockup is the series' lockup.css (the films read the same file); the link around it is the tap target */
.lockup {{ display: inline-flex; align-items: baseline; min-height: 44px; padding-top: .1em; text-decoration: none; flex: none; }}
.lockup .k-lock {{ font-size: var(--lk, 22px); }}
.top .lockup {{ --lk: 24px; }}
.nav a.link[aria-current="page"] {{ color: var(--navy); background: rgba(10,23,51,.06); }}
/* The way into the shorts from the overview */
.shorts {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-5); list-style: none; margin: 0; padding: 0; }}
.short {{ display: grid; gap: var(--space-3); text-decoration: none; color: var(--ink); border-radius: var(--r-ctl); }}
.short .thumb {{ position: relative; display: block; aspect-ratio: 16 / 9; border-radius: var(--r-ctl); overflow: hidden; box-shadow: var(--float); background: var(--navy); transition: transform .2s ease, box-shadow .2s ease; }}
.short img {{ width: 100%; height: 100%; object-fit: cover; filter: blur(2px); transform: scale(1.03); }}
.short .thumb::after {{ content: ""; position: absolute; inset: 0; background: rgba(10,23,51,.08); }}
.short .play-face {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 1; min-height: 44px; font-size: 15px; padding: 0 var(--space-4) 0 var(--space-3); gap: var(--space-2); }}
.short .play-face .len {{ padding-left: var(--space-2); }}
.short:hover .thumb {{ transform: translateY(-2px); box-shadow: var(--win); }}
.short:hover .play-face {{ background: var(--accent-press); }}
.short .t {{ font: 600 17px/1.3 var(--display); color: var(--navy); letter-spacing: -.01em; }}
.short:hover .t {{ color: var(--accent); }}
.section-head a.more {{ font-weight: 600; font-size: 15px; text-decoration: none; min-height: 44px; display: inline-flex; align-items: center; }}
.back {{ display: inline-flex; align-items: center; gap: var(--space-2); margin-top: var(--space-4); font-weight: 600; font-size: 15px; text-decoration: none; min-height: 44px; }}
@media (max-width: 860px) {{ .shorts {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
@media (max-width: 480px) {{ .shorts {{ grid-template-columns: 1fr; }} }}
.nav {{ display: flex; align-items: center; gap: var(--space-2); }}
.nav a.link {{ color: var(--ink-2); text-decoration: none; font-weight: 500; font-size: 15px; padding: 0 var(--space-3); min-height: 44px; display: inline-flex; align-items: center; border-radius: var(--r-ctl); transition: color .2s ease, background-color .2s ease; }}
.nav a.link:hover {{ color: var(--navy); background: rgba(10,23,51,.05); }}
.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2); min-height: 44px; padding: 0 var(--space-5); border-radius: var(--r-ctl); background: var(--accent); color: #fff; font: 600 15px/1 var(--sans); text-decoration: none; border: 0; cursor: pointer; transition: background-color .2s ease, transform .2s ease; }}
.btn:hover {{ background: var(--accent-press); color: #fff; }}
.btn:active {{ transform: translateY(1px); }}

/* Hero */
.hero {{ padding-top: var(--space-6); }}
.hero h1 {{ font-size: clamp(30px, 3.4vw, 46px); line-height: 1.1; letter-spacing: -0.03em; }}
.hero h1 .beat {{ display: block; }}
.hero h1 .checked {{ display: inline; background-image: linear-gradient(var(--ok), var(--ok)); background-repeat: no-repeat; background-size: 100% 3px; background-position: 0 100%; padding-bottom: 4px; box-decoration-break: clone; -webkit-box-decoration-break: clone; }}
.lede {{ margin-top: var(--space-5); font-size: 19px; line-height: 1.5; color: var(--ink-2); max-width: 70ch; }}
.lead-film {{ margin-top: var(--space-6); }}
.lead-meta {{ display: grid; grid-template-columns: minmax(0, 4fr) minmax(0, 7fr); gap: var(--space-4) var(--space-7); margin-top: var(--space-5); }}
.lead-meta h2 {{ font-size: 28px; line-height: 1.15; letter-spacing: -0.02em; }}

/* Players */
.player {{ position: relative; border-radius: var(--r-win); overflow: hidden; background: var(--navy); box-shadow: var(--float); aspect-ratio: 16 / 9; }}
.player-lead {{ box-shadow: var(--win); }}
.player video {{ width: 100%; height: 100%; object-fit: cover; background: var(--navy); }}
.play {{ position: absolute; inset: 0; width: 100%; display: flex; align-items: center; justify-content: center; background: transparent; border: 0; padding: 0; cursor: pointer; }}
.play-face {{ display: inline-flex; align-items: center; gap: var(--space-3); min-height: 48px; padding: 0 var(--space-5) 0 var(--space-4); border-radius: var(--r-ctl); background: var(--accent); color: #fff; font: 600 16px/1 var(--sans); box-shadow: 0 2px 4px rgba(10,23,51,.18), 0 12px 24px -10px rgba(10,23,51,.45); transition: background-color .2s ease, transform .2s ease; }}
.play-face svg {{ width: 18px; height: 18px; }}
.play-face .len {{ font-weight: 500; opacity: .86; font-variant-numeric: tabular-nums; padding-left: var(--space-3); border-left: 1px solid rgba(255,255,255,.35); }}
.play:hover .play-face {{ background: var(--accent-press); }}
.play:active .play-face {{ transform: translateY(1px); }}
.play:focus-visible {{ outline-offset: -4px; border-radius: var(--r-win); }}
.player-lead .play-face {{ min-height: 56px; font-size: 17px; padding: 0 var(--space-6) 0 var(--space-5); }}
.card .play {{ align-items: flex-end; justify-content: flex-start; padding: var(--space-4); }}
.card .play-face {{ min-height: 44px; font-size: 15px; padding: 0 var(--space-4) 0 var(--space-3); gap: var(--space-2); }}
.card .play-face .len {{ padding-left: var(--space-2); }}
.player-error {{ position: absolute; left: var(--space-4); right: var(--space-4); bottom: var(--space-4); background: var(--surface); color: var(--ink); padding: var(--space-3) var(--space-4); border-radius: var(--r-ctl); font-size: 15px; box-shadow: var(--float); }}
.player-error[hidden] {{ display: none; }}


/* Film and clip text */
.length {{ margin-top: var(--space-2); font-size: 14px; font-weight: 500; color: var(--muted); font-variant-numeric: tabular-nums; }}
.desc {{ color: var(--ink-2); font-size: 16px; }}
.lead-meta .desc {{ font-size: 17px; }}
.narration {{ margin-top: var(--space-3); }}
.narration summary {{ display: inline-flex; align-items: center; gap: var(--space-2); min-height: 44px; cursor: pointer; color: var(--accent); font-weight: 500; font-size: 15px; list-style: none; border-radius: 6px; transition: color .2s ease; }}
.narration summary::-webkit-details-marker {{ display: none; }}
.narration summary::after {{ content: ""; width: 7px; height: 7px; border-right: 1.5px solid currentColor; border-bottom: 1.5px solid currentColor; transform: translateY(-2px) rotate(45deg); transition: transform .2s ease; }}
.narration[open] summary::after {{ transform: translateY(2px) rotate(225deg); }}
.narration summary:hover {{ color: var(--accent-press); }}
.narration-body {{ display: grid; gap: var(--space-3); padding: var(--space-4) var(--space-5); margin-top: var(--space-1); background: var(--surface); border: 1px solid var(--rule); border-radius: var(--r-ctl); font-size: 15px; color: var(--ink-2); }}

/* Sections */
.section {{ padding-top: var(--space-9); }}
.section-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: var(--space-5); padding-bottom: var(--space-4); border-bottom: 1px solid var(--rule); margin-bottom: var(--space-6); }}
.section-head h2 {{ font-size: clamp(26px, 2.6vw, 32px); line-height: 1.15; letter-spacing: -0.02em; }}
.section-head p {{ color: var(--muted); font-size: 15px; }}
.grid {{ display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--space-7) var(--space-6); }}
.card {{ display: grid; gap: var(--space-4); align-content: start; scroll-margin-top: var(--space-6); }}
.card h3 {{ font-size: 21px; line-height: 1.2; letter-spacing: -0.015em; }}
.card-text {{ display: grid; gap: var(--space-2); }}
.card-text .length {{ margin-top: 0; }}
.card-text .narration {{ margin-top: 0; }}

/* Ask */
.ask {{ margin-top: var(--space-9); background: var(--surface); border-radius: var(--r-win); box-shadow: var(--float); padding: var(--space-8) var(--space-7); display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 4fr); gap: var(--space-6); align-items: center; }}
.ask h2 {{ font-size: clamp(28px, 3vw, 38px); line-height: 1.1; letter-spacing: -0.025em; }}
.ask p {{ margin-top: var(--space-4); color: var(--ink-2); font-size: 17px; max-width: 54ch; }}
.ask-actions {{ display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-4); }}
.ask-actions .btn {{ min-height: 52px; padding: 0 var(--space-6); font-size: 16px; }}
.ask-actions .site {{ color: var(--navy); font-weight: 500; min-height: 44px; display: inline-flex; align-items: center; }}

/* Footer */
.foot {{ padding-top: var(--space-7); padding-bottom: var(--space-8); color: var(--muted); font-size: 14px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: var(--space-3) var(--space-6); }}
.foot p {{ max-width: 70ch; }}

@media (min-width: 760px) {{
  :root {{ --gutter: 32px; }}
  .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
}}
@media (max-width: 860px) {{
  .lead-meta, .ask {{ grid-template-columns: minmax(0, 1fr); }}
  .ask {{ padding: var(--space-7) var(--space-5); }}
}}
@media (max-width: 560px) {{
  .nav a.link {{ display: none; }}
  .hero {{ padding-top: var(--space-5); }}
  .lede {{ font-size: 17px; }}
  .lead-film {{ margin-top: var(--space-6); }}
  .section {{ padding-top: var(--space-8); }}
  .section-head {{ flex-direction: column; gap: var(--space-1); }}
  .play-face, .player-lead .play-face {{ min-height: 44px; font-size: 15px; padding: 0 var(--space-4); }}
  .top .lockup {{ --lk: 21px; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ transition: none !important; scroll-behavior: auto !important; }}
}}
{CFG_SITE.get("css", "")}
</style>

</head>
<body>
<a class="skip" href="#main">Skip to the videos</a>
<header class="wrap top">
  <a class="lockup" href="/" aria-label="{e(SERIES["title_prefix"])}, all pages">{LOCKUP}</a>
  <nav class="nav" aria-label="Page">
{nav}
  </nav>
</header>

<main id="main">
{main}</main>

<p class="sr-only" role="status" id="player-status"></p>
<footer class="wrap foot">
{FOOTER}
</footer>

<script>
(function () {{
  var videos = Array.prototype.slice.call(document.querySelectorAll('[data-player] video'));
  videos.forEach(function (v) {{
    var box = v.parentNode;
    var err = box.querySelector('.player-error');
    var status = document.getElementById('player-status');
    var showError = function () {{
      v.controls = true;
      if (err.hidden) {{ err.hidden = false; status.textContent = v.dataset.title + ' did not load.'; }}
    }};
    v.querySelector('source').addEventListener('error', showError);
    v.addEventListener('error', showError);
    v.addEventListener('play', function () {{
      videos.forEach(function (o) {{ if (o !== v && !o.paused) o.pause(); }});
    }});
    // Replace the browser's poster controls with one labelled button; the native
    // controls return the moment the film starts.
    v.controls = false;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'play';
    b.setAttribute('aria-label', 'Play ' + v.dataset.title + ', ' + v.dataset.spoken);
    b.innerHTML = '<span class="play-face"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M5 3.2v11.6c0 .6.66.97 1.17.65l9.1-5.8a.77.77 0 0 0 0-1.3l-9.1-5.8A.77.77 0 0 0 5 3.2Z" fill="currentColor"/></svg>Play<span class="len">' + v.dataset.length + '</span></span>';
    b.addEventListener('click', function () {{
      v.controls = true;
      b.remove();
      v.focus({{ preventScroll: true }});
      var p = v.play();
      if (p && p.catch) p.catch(function () {{ /* the native controls are showing; the person can press play there */ }});
    }});
    box.insertBefore(b, err);
  }});

}})();
</script>
</body>
</html>
"""

LEAD = f"""    <div class="lead-film" id="o">
      {player(OVERVIEW, lead=True)}
      <div class="lead-meta">
        <div><h2>{e(O)}</h2><p class="length">{clock(SECONDS[OVERVIEW])}</p></div>
        <div><p class="desc">{e(DESC[OVERVIEW])}</p>{narration(OVERVIEW)}</div>
      </div>
    </div>
"""
NAV_ITEMS = [tuple(x) for x in CFG_SITE['nav']]


def nav(current):
    cur = lambda key: ' aria-current="page"' if key == current else ''   # noqa: E731
    links = "".join(f'    <a class="link" href="{href}"{cur(key)}>{label}</a>\n' for key, href, label in NAV_ITEMS)
    return links + f'    <a class="btn" href="{DEMO}">{e(SERIES["cta"])}</a>'


ASK = f"""  <div class="wrap">
    <section class="ask" aria-labelledby="ask-title">
      <div>
        <h2 id="ask-title">{e(CFG_SITE["ask"]["title"])}</h2>
        <p>{e(CFG_SITE["ask"]["text"])}</p>
      </div>
      <div class="ask-actions">
        <a class="btn" href="{DEMO}">{e(SERIES["cta"])}</a>
        <a class="site" href="https://{SERIES["url"]}">{e(SERIES["url"])}</a>
      </div>
    </section>
  </div>
"""
PLAY_ICON = '<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M5 3.2v11.6c0 .6.66.97 1.17.65l9.1-5.8a.77.77 0 0 0 0-1.3l-9.1-5.8A.77.77 0 0 0 5 3.2Z" fill="currentColor"/></svg>'


def short_link(fid):
    return (f'      <li><a class="short" href="/shorts#{fid.lower()}" data-short="{ORDER.index(fid)}" aria-haspopup="dialog"><span class="thumb"><img src="{ver(f"/assets/posters/{PREFIX}-{fid}.webp")}" alt="" width="1280" height="720" loading="lazy">'
            f'<span class="play-face" aria-hidden="true">{PLAY_ICON}Play<span class="len">{clock(SECONDS[fid])}</span></span></span>'
            f'<span class="t">{e(films[fid]["title"])}</span></a></li>')


SHORTS_DATA = json.dumps([{"title": films[f]["title"], "len": clock(SECONDS[f]), "desc": DESC[f],
                           "src": ver(f"{BLOB}/{PREFIX}-{f}-vo.mp4"), "poster": ver(f"/assets/posters/{PREFIX}-{f}.webp")} for f in ORDER],
                         ensure_ascii=False).replace("</", "<\\/")
MODAL = """
<dialog class="sm" id="short-modal" aria-labelledby="sm-title">
  <div class="sm-in" tabindex="-1">
    <div class="sm-frame"><video id="sm-video" playsinline controls preload="none" width="1920" height="1080"></video></div>
    <div class="sm-bar">
      <div class="sm-meta"><p class="sm-count" id="sm-count"></p><h2 id="sm-title"></h2><p class="sm-desc" id="sm-desc"></p></div>
      <div class="sm-nav">
        <button type="button" class="sm-btn" data-sm="prev"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M11 4 6 9l5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Previous</button>
        <button type="button" class="sm-btn" data-sm="next">Next<svg viewBox="0 0 18 18" aria-hidden="true"><path d="m7 4 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
      </div>
    </div>
    <button type="button" class="sm-close" data-sm="close" aria-label="Close"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M4.5 4.5l9 9m0-9-9 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button>
  </div>
</dialog>
<script type="application/json" id="shorts-data">""" + SHORTS_DATA + """</script>
<style>
.sm { padding: 0; border: 0; background: transparent; max-width: none; max-height: none; width: min(1120px, calc(100vw - 32px), calc((100vh - 250px) * 16 / 9 + 32px)); min-width: min(560px, calc(100vw - 32px)); overflow: visible; color: var(--ink); }
.sm-in:focus { outline: none; }
.sm::backdrop { background: rgba(10,23,51,.72); backdrop-filter: blur(6px); opacity: 0; transition: opacity .32s ease; }
.sm.on::backdrop { opacity: 1; }
.sm-in { position: relative; background: var(--surface); border-radius: var(--r-win); box-shadow: var(--win); padding: var(--space-4); transition: background-color .3s ease, box-shadow .3s ease; }
.sm-frame { aspect-ratio: 16 / 9; border-radius: var(--r-ctl); overflow: hidden; background: var(--navy) center / cover no-repeat; transform-origin: 0 0; }
.sm-frame video { width: 100%; height: 100%; display: block; object-fit: cover; }
.sm-bar { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--space-5); padding: var(--space-4) var(--space-2) var(--space-2); }
.sm-count { font-size: 14px; font-weight: 500; color: var(--muted); font-variant-numeric: tabular-nums; }
.sm-meta h2 { font-size: 22px; line-height: 1.2; letter-spacing: -.015em; margin-top: 2px; }
.sm-desc { margin-top: var(--space-2); color: var(--ink-2); font-size: 16px; max-width: 68ch; }
.sm-nav { display: flex; gap: var(--space-2); flex: none; }
.sm-btn { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 0 var(--space-4); border-radius: var(--r-ctl); border: 1px solid var(--rule); background: var(--surface); color: var(--navy); font: 600 15px/1 var(--sans); cursor: pointer; transition: background-color .2s ease, border-color .2s ease; }
.sm-btn svg { width: 16px; height: 16px; }
.sm-btn:hover { border-color: #AEB4C0; background: #F6F7F9; }
.sm-btn:disabled { opacity: .4; cursor: default; }
.sm-close { position: absolute; top: -14px; right: -14px; width: 44px; height: 44px; border-radius: 50%; border: 0; background: var(--navy); color: #fff; display: grid; place-items: center; cursor: pointer; box-shadow: var(--float); }
.sm-close svg { width: 18px; height: 18px; }
.sm-close:hover { background: var(--accent); }
.sm:not(.on) .sm-bar, .sm:not(.on) .sm-close { opacity: 0; }
.sm-bar, .sm-close { transition: opacity .28s ease .12s; }
.sm-in.morph { background: transparent; box-shadow: none; }
@media (max-width: 640px) { .sm-bar { flex-direction: column; } .sm-close { top: -18px; right: -6px; } }
@media (prefers-reduced-motion: reduce) { .sm::backdrop, .sm-bar, .sm-close { transition: none; } }
button.more { border: 0; background: none; color: var(--accent); cursor: pointer; padding: 0; font-family: var(--sans); }
button.more:hover { color: var(--accent-press); }
</style>
<script>
(function () {
  var d = document.getElementById('short-modal');
  if (!d || !d.showModal) return;
  var data = JSON.parse(document.getElementById('shorts-data').textContent);
  var frame = d.querySelector('.sm-frame'), v = document.getElementById('sm-video'), inner = d.querySelector('.sm-in');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var i = 0, opener = null, busy = false;
  var thumbs = Array.prototype.slice.call(document.querySelectorAll('a.short[data-short]'));
  var ease = 'cubic-bezier(.2,.8,.2,1)';
  function show(n, play) {
    i = n; var s = data[i];
    document.getElementById('sm-count').textContent = (i + 1) + ' of ' + data.length + ' · ' + s.len;
    document.getElementById('sm-title').textContent = s.title;
    document.getElementById('sm-desc').textContent = s.desc;
    d.querySelector('[data-sm="prev"]').disabled = i === 0;
    d.querySelector('[data-sm="next"]').disabled = i === data.length - 1;
    frame.style.backgroundImage = 'url("' + s.poster + '")';
    v.poster = s.poster; v.src = s.src;
    if (play) { var p = v.play(); if (p && p.catch) p.catch(function () { /* the controls are showing; the person can press play */ }); }
  }
  function flip(from, to, reverse) {
    var dx = from.left - to.left, dy = from.top - to.top, sx = from.width / to.width, sy = from.height / to.height;
    var a = 'translate(' + dx + 'px,' + dy + 'px) scale(' + sx + ',' + sy + ')', b = 'none';
    return frame.animate([{ transform: reverse ? b : a }, { transform: reverse ? a : b }], { duration: 440, easing: ease, fill: 'both' });
  }
  function open(n, link) {
    if (busy) return;
    opener = link; show(n, true);
    d.showModal(); inner.focus({ preventScroll: true });   // arrows then step between shorts; inside the video they seek
    var thumb = link && link.querySelector('.thumb');
    if (reduce || !thumb) { d.classList.add('on'); return; }
    busy = true; inner.classList.add('morph');
    var anim = flip(thumb.getBoundingClientRect(), frame.getBoundingClientRect(), false);
    requestAnimationFrame(function () { d.classList.add('on'); });
    anim.onfinish = function () { anim.cancel(); inner.classList.remove('morph'); busy = false; };
  }
  function close() {
    if (busy) return;
    v.pause();
    var link = thumbs[i], thumb = link && link.querySelector('.thumb');
    var done = function () { d.close(); frame.getAnimations().forEach(function (x) { x.cancel(); }); inner.classList.remove('morph'); v.removeAttribute('src'); v.load(); busy = false; if (opener) opener.focus({ preventScroll: true }); };
    d.classList.remove('on');
    var r = thumb && thumb.getBoundingClientRect();
    if (reduce || !r || r.bottom < 0 || r.top > innerHeight) { setTimeout(done, reduce ? 0 : 200); return; }
    busy = true; inner.classList.add('morph');
    flip(r, frame.getBoundingClientRect(), true).onfinish = done;
  }
  function step(k) {
    var n = i + k; if (n < 0 || n >= data.length || busy) return;
    var anim = reduce ? null : frame.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 140, easing: 'ease-out', fill: 'forwards' });
    var go = function () { show(n, true); opener = thumbs[n]; if (anim) { anim.cancel(); frame.animate([{ opacity: 0, transform: 'translateX(' + (k * 24) + 'px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: ease }); } };
    if (anim) anim.onfinish = go; else go();
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-short]');
    if (!t || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault();
    var n = +t.dataset.short;
    open(n, t.matches('a') ? t : thumbs[n]);
  });
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-sm]');
    if (b) { var a = b.dataset.sm; if (a === 'close') close(); else step(a === 'next' ? 1 : -1); return; }
    if (e.target === d) close();                 // a press on the backdrop
  });
  d.addEventListener('cancel', function (e) { e.preventDefault(); close(); });
  d.addEventListener('keydown', function (e) {
    if (e.target === v) return;                  // arrows seek inside the video
    if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
  });
})();
</script>
"""


P = CFG_SITE['pages']
n_shorts = len(ORDER)
overview_main = f"""  <section class="wrap hero" aria-labelledby="page-title">
    <h1 id="page-title"><span class="beat">{P["overview"]["h1"][0]}</span> <span class="beat"><span class="checked">{P["overview"]["h1"][1]}</span></span></h1>
    <p class="lede">{P["overview"]["lede"]}</p>
{LEAD}  </section>

  <section class="wrap section" id="shorts" aria-labelledby="shorts-title">
    <div class="section-head"><h2 id="shorts-title">{P["overview"]["shorts_heading"]}</h2><button type="button" class="more" data-short="0" aria-haspopup="dialog">Play all {n_shorts}</button></div>
    <ul class="shorts">
{chr(10).join(short_link(f) for f in ORDER)}
    </ul>
  </section>

{ASK}""" + MODAL

shorts_main = f"""  <section class="wrap hero" aria-labelledby="page-title">
    <h1 id="page-title"><span class="beat">{P["shorts"]["h1"][0]}</span> <span class="beat"><span class="checked">{P["shorts"]["h1"][1]}</span></span></h1>
    <p class="lede">{P["shorts"]["lede"]}</p>
  </section>

  <section class="wrap section" id="clips" aria-labelledby="clips-title">
    <div class="section-head"><h2 id="clips-title">{P["shorts"]["clips_heading"]}</h2><p>{P["shorts"]["clips_note"]}</p></div>
    <div class="grid">
{clips}
    </div>
  </section>

{ASK}"""

for slug, main in (('overview', overview_main), ('shorts', shorts_main)):
    pg = P[slug]
    page = render(slug, pg['title'], pg['description'], pg['og'], nav(slug), main)
    (HERE / f"{slug}.html").write_text(page, encoding="utf-8")
    print(f"site/{slug}.html: {len(page):,} bytes")

if not (HERE / 'vercel.json').exists():
    (HERE / 'vercel.json').write_text(json.dumps({'cleanUrls': True, 'headers': [
        {'source': '/films/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=0, must-revalidate'}]},
        {'source': '/assets/fonts/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=31536000, immutable'}]},
        {'source': '/((?!assets/).*)', 'headers': [{'key': 'Cache-Control', 'value': 'private, no-store'}]},
        {'source': '/(.*)', 'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex, nofollow'}, {'key': 'X-Content-Type-Options', 'value': 'nosniff'},
                                         {'key': 'Referrer-Policy', 'value': 'no-referrer'}, {'key': 'X-Frame-Options', 'value': 'DENY'}]}]}, indent=1))
if not (HERE / 'robots.txt').exists():
    (HERE / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
