#!/usr/bin/env python3
"""Build one film's HyperFrames project from its plan, picture first.

    MOTION_CRAFT_SCRIPTS=<motion-craft base>/scripts python3 _kit/engine/build.py <series dir> <film> [--mute-only] [--no-sound]

Reads films/<film>/plan.json (written by the series' films.py), series.json, the voice lines gateway_audio.py made
(voice/<line>.wav and .json), and the series' lockup.css and marks/. Writes timeline.json (with the narration) and
timeline_mute.json (without), assets/ (the runtime, fonts, GSAP, the lockup, the states spliced into each
composition), compositions/lock.html (a short's lockup bar), index.html, and two soundtracks from one cue sheet:
assets/sound.wav for the muted master the picture renders with, and assets/sound_vo.wav for the voiced cut, which
delivery.py remuxes onto the same picture.

The build fails, before anything renders, when a narration line starts within 0.2 s of the previous line's end, runs
more than 0.1 s past the end of the scene it was placed in, or ends within 0.6 s of the film's end. --mute-only
builds a film whose voice has not been generated yet: both timelines then carry no lines.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith('--')]
if len(args) != 2:
    sys.exit(__doc__.split('\n\n')[1])
SERIES, FID = Path(args[0]).resolve(), args[1]
MUTE_ONLY, SOUND = '--mute-only' in sys.argv, '--no-sound' not in sys.argv
KIT = SERIES / '_kit'
MC = Path(os.environ.get('MOTION_CRAFT_SCRIPTS', ''))
if not (MC / 'timeline_js.py').exists():
    sys.exit('Set MOTION_CRAFT_SCRIPTS to motion-craft\'s scripts/ folder (the base directory motion-craft:motion-craft '
             'reports when it loads, plus /scripts). It holds timeline_js.py, hf.sh and the sfx sound engine.')

cfg = json.loads((SERIES / 'series.json').read_text())
F = SERIES / 'films' / FID
plan = json.loads((F / 'plan.json').read_text())
FPS = plan.get('fps', 60)
TAG = re.compile(r'\s*\[[a-z][a-z \-]*\]\s*', re.I)

# ---- 1. scenes end to end, each its own length -------------------------------------------------------------------
scenes, t = {}, 0.0
for sc in plan['scenes']:
    scenes[sc['id']] = {'start': round(t, 3), 'dur': sc['dur']}
    t += sc['dur']
duration = round(t, 3)
lockbar = plan.get('lockbar', True)
lock_start = round(duration - plan['lock'], 3)
beats, n = {}, 0
for sc in plan['scenes']:
    for at, kind in sc['sfx']:
        beats[f'{kind}_{n:03d}'] = round(scenes[sc['id']]['start'] + at, 3)
        n += 1

# ---- 2. the narration, placed on the picture ----------------------------------------------------------------------
voice_dir = SERIES / cfg['voice']['dir']
VO = F / 'assets' / 'voice'
VO.mkdir(parents=True, exist_ok=True)
tempo = plan.get('tempo', 1.0)
if not 0.92 <= tempo <= 1.08:
    sys.exit(f'{FID}: tempo {tempo} is outside 0.92-1.08; past that, shorten the line instead of stretching it')
lines = {}
if not MUTE_ONLY:
    missing = [lid for lid, _, _ in plan['voice'] if not (voice_dir / f'{lid}.json').exists()]
    if missing:
        sys.exit(f'{FID}: no voice for {", ".join(missing)} in {voice_dir}. Generate it with gateway_audio.py lines '
                 f'(paid: show the cost first), or build with --mute-only.')
    for lid, sid, off in plan['voice']:
        meta = json.loads((voice_dir / f'{lid}.json').read_text())
        dst = VO / f'{lid}.wav'
        if tempo != 1.0:
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(voice_dir / f'{lid}.wav'), '-filter:a', f'atempo={tempo}', str(dst)], check=True)
        else:
            shutil.copy(voice_dir / f'{lid}.wav', dst)
        start = round(scenes[sid]['start'] + off, 3)
        lines[lid] = {'scene': sid, 'text': TAG.sub(' ', meta['script']).strip(), 'start': start, 'end': round(start + meta['duration'] / tempo, 3),
                      'words': [[w['w'], round(start + w['start'] / tempo, 3), round(start + w['end'] / tempo, 3)] for w in meta['words']]}
    order = sorted(lines.items(), key=lambda kv: kv[1]['start'])
    bad = []
    for (a, la), (b, lb) in zip(order, order[1:]):
        if lb['start'] < la['end'] + 0.2:
            bad.append(f'{b} starts at {lb["start"]} s, within 0.2 s of {a} ending at {la["end"]} s')
    for lid, ln in lines.items():
        sc_end = scenes[ln['scene']]['start'] + scenes[ln['scene']]['dur']
        if ln['end'] > sc_end + 0.1:
            bad.append(f'{lid} ends at {ln["end"]} s, {ln["end"] - sc_end:.2f} s past its scene {ln["scene"]} (ends {sc_end:.2f} s): '
                       f'lengthen that scene\'s hold, or move the line')
    if order and order[-1][1]['end'] > duration - 0.6:
        bad.append(f'the last line ends at {order[-1][1]["end"]} s, within 0.6 s of the end ({duration} s)')
    if bad:
        sys.exit(f'{FID}: the narration does not sit on its picture:\n  ' + '\n  '.join(bad))

bed = (cfg.get('beds') or {}).get('overview' if FID == cfg['overview'] else 'short')
tl = {'duration': duration, 'fps': FPS, 'fonts': cfg['fonts'], 'voiceDir': str(VO), 'scenes': scenes, 'lines': lines,
      'beats': beats, 'lock': {'start': lock_start}, 'title': plan['title'], 'bed': str(SERIES / bed) if bed else None}
(F / 'timeline.json').write_text(json.dumps(tl, indent=1, ensure_ascii=False))
(F / 'timeline_mute.json').write_text(json.dumps(dict(tl, lines={}), indent=1, ensure_ascii=False))
subprocess.run([sys.executable, str(MC / 'timeline_js.py'), str(F / 'timeline.json'), str(F / 'assets' / 'timeline.js')], check=True)

# ---- 3. assets and the live states ---------------------------------------------------------------------------------
A = F / 'assets'
for sub in ('fonts', 'vendor'):
    if not (SERIES / 'assets' / sub).is_dir():
        sys.exit(f'{SERIES / "assets" / sub} is missing: run new_series.py --fetch, or copy the fonts and GSAP in by hand')
    shutil.copytree(SERIES / 'assets' / sub, A / sub, dirs_exist_ok=True)
for f in ('kit.css', 'kit.js', 'frame.css', 'kit3.css', 'kit3.js'):
    shutil.copy(KIT / 'runtime' / f, A / f)
shutil.copy(SERIES / 'lockup.css', A / 'lockup.css')
subprocess.run([sys.executable, str(SERIES / 'states.py')], check=True, cwd=SERIES)
for comp in (F / 'compositions').glob('*.html'):
    s = comp.read_text()
    s2 = re.sub(r'<!--state:([a-z0-9-]+)-->.*?<!--/state:\1-->',
                lambda m: f'<!--state:{m.group(1)}-->{(SERIES / "states" / f"{m.group(1)}.html").read_text()}<!--/state:{m.group(1)}-->', s, flags=re.S)
    if s2 != s:
        comp.write_text(s2)

# ---- 4. the lockup bar over a short's last seconds, and the root composition --------------------------------------
sys.path.insert(0, str(KIT / 'engine'))
import states_engine as E  # noqa: E402

lock_html = E.lockup(cfg['lockup']['wordmark'], cfg['lockup']['product'])
(F / 'compositions' / 'lock.html').write_text(f'''<template id="lock-template">
  <div id="lockroot" data-composition-id="lock" data-width="1920" data-height="1080">
    <div class="k-lockband" id="lkb" data-layout-ignore="a soft scrim that fades the product under the lockup bar, on purpose"></div>
    <div class="k-lockup" id="lk">{lock_html}
      <div class="k-cta" data-var-text="cta">{cfg["cta"]}</div><div class="k-url" data-var-text="url">{cfg["url"]}</div></div>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        gsap.set('#lkb', {{ opacity: 0 }});
        gsap.set('#lk', {{ opacity: 0, y: 18, xPercent: -50, filter: 'blur(8px)' }});   // GSAP owns the transform: keep the bar centred
        tl.to('#lkb', {{ opacity: 1, duration: 0.5, ease: 'power2.out' }}, 0);
        tl.to('#lk', {{ opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.6, ease: 'expo.out' }}, 0.1);
        window.__timelines = window.__timelines || {{}};
        window.__timelines['lock'] = tl;
      }})();
    </script>
  </div>
</template>
''')
icons = E.sprite(KIT / 'runtime', SERIES / 'marks', ['mark'] + (['claude', 'chatgpt'] if cfg.get('host_marks') else []))
hosts = '\n'.join(
    f'      <div id="{sc["id"]}-host" class="scene clip" data-hf-scene-no-swap="its script measures the live states once, at load" '
    f'data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["src"]}" data-start="{scenes[sc["id"]]["start"]}" '
    f'data-duration="{sc["dur"]}" data-track-index="{1 + (i % 2)}" data-width="1920" data-height="1080"></div>' for i, sc in enumerate(plan['scenes']))
LOCK_HOST = (f'      <div id="lock-host" class="scene clip" data-composition-id="lock" data-composition-src="compositions/lock.html" '
             f'data-start="{lock_start}" data-duration="{round(duration - lock_start, 3)}" data-track-index="3" data-width="1920" data-height="1080"></div>') if lockbar else ''
variables = [{'id': 'cta', 'type': 'string', 'label': 'Call to action', 'default': cfg['cta']},
             {'id': 'url', 'type': 'string', 'label': 'Web address', 'default': cfg['url']}]
(F / 'index.html').write_text(f'''<!doctype html>
<html lang="{cfg.get("lang", "en-US")}" data-resolution="landscape" data-composition-variables='{json.dumps(variables)}'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>{cfg["title_prefix"]} · {plan["title"]}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script src="assets/timeline.js"></script>
    <script src="assets/kit.js"></script>
    <script src="assets/kit3.js"></script>
    <link rel="stylesheet" href="assets/frame.css" />
    <link rel="stylesheet" href="assets/kit.css" />
    <link rel="stylesheet" href="assets/kit3.css" />
    <link rel="stylesheet" href="assets/lockup.css" />
    <style>
      * {{ box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: var(--g-bg); }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: var(--g-bg); }}
    </style>
  </head>
  <body data-theme="light" class="embed">
{icons}
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1920" data-height="1080" data-fps="{FPS}">
{hosts}
{LOCK_HOST}
      <audio id="score" class="clip" src="assets/sound.wav" data-start="0" data-duration="{duration}" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines['main'] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')

# ---- 5. two soundtracks from one cue sheet -------------------------------------------------------------------------
if SOUND:
    cues = F / 'sound' / 'cues.py'
    cues.parent.mkdir(exist_ok=True)
    cues.write_text('# The film\'s score from timeline.json; see _kit/engine/score.py.\n'
                    f'import sys\nsys.path.insert(0, {str(KIT / "engine")!r})\nfrom score import score, TARGET_LUFS  # noqa: E402,F401\n')
    if not bed:
        print(f'{FID}: no music bed in series.json; the score is effects only')
    for tlf, out in (('timeline_mute.json', 'sound.wav'), ('timeline.json', 'sound_vo.wav')):
        subprocess.run([sys.executable, '-m', 'sfx', str(cues), '--timeline', str(F / tlf), '--out', str(A / out)], check=True, cwd=MC)
print(json.dumps({'film': FID, 'duration': duration, 'lock': lock_start if lockbar else None,
                  'scenes': {k: [v['start'], v['dur']] for k, v in scenes.items()},
                  'voice': {k: [v['start'], v['end']] for k, v in lines.items()}}))
