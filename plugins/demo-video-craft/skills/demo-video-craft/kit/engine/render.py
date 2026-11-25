#!/usr/bin/env python3
"""Step 6 in one command: build, render once, remux the voiced cut, gate, and publish only on a pass.

    MOTION_CRAFT_SCRIPTS=<motion-craft>/scripts python3 _kit/engine/render.py <series dir> [--films O,K01]
        [--to delivery site/films] [--mute-only] [--published published.txt]

For each film (default: every film under films/) it runs build.py, renders the muted master with `hf.sh render -q
delivery` into staging/, and remuxes the voiced cut from assets/sound_vo.wav, through the 0.6 limiter when the film
table gives that film `limit` (a film whose voiced cut overshoots after AAC needs it on every render, so it lives in the
table, not in someone's memory). Then delivery.py publish gates the staged set and copies both cuts to every --to
folder only when every film passes. A build, render or remux failure stops the run before anything is copied, so last
round's file is never left live beside new ones under the same names.

File names are <series.json prefix>-<film>.mp4 and <prefix>-<film>-vo.mp4. Exit 0 only when the publish passed.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import delivery  # noqa: E402  (copied into the series kit by new_series.py)


def arg(name, default=None, many=False):
    a = sys.argv
    if name not in a:
        return default
    i = a.index(name)
    vals = []
    for x in a[i + 1:]:
        if x.startswith('--'):
            break
        vals.append(x)
    return vals if many else (vals[0] if vals else default)


def main():
    pos = [x for x in sys.argv[1:] if not x.startswith('--')]
    if not pos:
        sys.exit(__doc__.split('\n\n')[1])
    series = Path(pos[0]).resolve()
    mc = Path(os.environ.get('MOTION_CRAFT_SCRIPTS', ''))
    if not (mc / 'hf.sh').exists():
        sys.exit('Set MOTION_CRAFT_SCRIPTS to the scripts folder of motion-craft (it holds hf.sh).')
    cfg = json.loads((series / 'series.json').read_text())
    prefix = cfg['prefix']
    films = arg('--films', '').split(',') if arg('--films') else sorted(p.name for p in (series / 'films').iterdir() if (p / 'plan.json').exists())
    dests = [str((series / d).resolve()) for d in (arg('--to', many=True) or ['delivery'])]
    stage = series / 'staging'
    stage.mkdir(exist_ok=True)
    build = [sys.executable, str(HERE / 'build.py'), str(series)]
    for fid in films:
        F = series / 'films' / fid
        steps = [(build + [fid] + (['--mute-only'] if '--mute-only' in sys.argv else []), series, 'build'),
                 ([str(mc / 'hf.sh'), 'render', '-q', 'delivery', '-o', str(stage / f'{prefix}-{fid}.mp4')], F, 'render')]
        for cmd, cwd, what in steps:
            log = stage / f'{what}-{fid}.log'
            with open(log, 'w') as fh:
                rc = subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT, env=dict(os.environ)).returncode
            if rc:
                sys.exit(f'{fid}: {what} failed (exit {rc}); see {log}. Nothing was published.')
        plan = json.loads((F / 'plan.json').read_text())
        delivery.remux(stage / f'{prefix}-{fid}.mp4', F / 'assets' / 'sound_vo.wav', stage / f'{prefix}-{fid}-vo.mp4', plan.get('limit'))
        print(f'{fid}: built, rendered, remuxed' + (f' (limit {plan["limit"]})' if plan.get('limit') else ''))
        want = 'x'.join(str(v) for v in plan.get('size') or [1920, 1080])
        got = delivery.size(stage / f'{prefix}-{fid}.mp4')
        if got != want:
            sys.exit(f'{fid}: rendered at {got}, its film table says {want}. Nothing was published.')
    if '--mute-only' in sys.argv:
        print(f'--mute-only: staged in {stage}, not published (a voiced cut without a voice is not a voiced cut)')
        sys.exit(0)
    g = cfg.get('gate', {})
    # each film's size was checked against its own plan above, so a series can mix 16:9 and 9:16
    rc = delivery.publish(stage, dests, prefix, films, arg('--published'), None, g.get('lufs', -14.0),
                          g.get('lufs_tolerance', 0.5), g.get('true_peak', -1.0))
    sys.exit(rc)


if __name__ == '__main__':
    main()
