#!/usr/bin/env python3
"""Compare rebuilt films against the published ones, frame by frame, with SSIM.

    compare_films.py --a out/ --b published/ --prefix acme --films O,K02 [--every 6] [--floor 0.98]
    compare_films.py --self-test

For each film it decodes both files' pictures together, takes every Nth frame (6 at 60 fps is ten a second), and
measures SSIM (structural similarity, 1.0 = identical) for each pair through ffmpeg's ssim filter. It prints the mean,
the lowest frame and where it is, and every stretch below the floor, then a verdict line `compare: PASS 10/10` or
`compare: FAIL 8/10`. A film passes when its mean is at or above the floor and no frame falls below floor - 0.05.

Use it to prove a kit reproduces a series (the reference series was checked this way against its published files), to
confirm a re-render changed only what a note asked for, and to find the second place a fix did not reach. Pixels
that move by a frame read low at a cut; look at the stretch before calling it a defect. Exit 1 on a failed film.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def ssim_frames(a, b, every):
    vf = f"[0:v]select='not(mod(n\\,{every}))',setpts=N/TB[x];[1:v]select='not(mod(n\\,{every}))',setpts=N/TB[y];[x][y]ssim=stats_file=-"
    r = subprocess.run(['ffmpeg', '-nostats', '-loglevel', 'error', '-i', str(a), '-i', str(b), '-lavfi', vf, '-f', 'null', '-'],
                       capture_output=True, text=True)
    vals = [float(m) for m in re.findall(r'All:([0-9.]+)', r.stdout)]
    if not vals:
        sys.exit(f'no SSIM for {a} against {b}: {r.stderr.strip()[:300]}')
    return vals


def fps(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', str(path)],
                       capture_output=True, text=True)
    n, d = r.stdout.strip().split('/')
    return float(n) / float(d)


def compare(a_dir, b_dir, prefix, films, every, floor):
    ok = 0
    for fid in films:
        a, b = Path(a_dir) / f'{prefix}-{fid}.mp4', Path(b_dir) / f'{prefix}-{fid}.mp4'
        if not a.exists() or not b.exists():
            print(f'  FAIL {fid}: {"" if a.exists() else a.name + " missing in --a "}{"" if b.exists() else b.name + " missing in --b"}')
            continue
        vals, rate = ssim_frames(a, b, every), fps(b)
        mean, low = sum(vals) / len(vals), min(vals)
        at = vals.index(low) * every / rate
        stretches, cur = [], None
        for k, v in enumerate(vals):
            t = k * every / rate
            if v < floor:
                cur = [t, t] if cur is None else [cur[0], t]
            elif cur:
                stretches.append(cur)
                cur = None
        if cur:
            stretches.append(cur)
        good = mean >= floor and low >= floor - 0.05
        ok += good
        where = ', '.join(f'{s:.1f}-{e:.1f}s' for s, e in stretches[:6]) or 'none'
        print(f'  {"ok  " if good else "FAIL"} {fid}: mean SSIM {mean:.4f}, lowest {low:.4f} at {at:.1f}s, {len(vals)} frames; below {floor}: {where}')
    print(f'compare: {"PASS" if ok == len(films) else "FAIL"} {ok}/{len(films)}')
    return 0 if ok == len(films) else 1


def self_test():
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            sys.exit(f'{tool} is not on PATH')
    import contextlib
    import io
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for sub in ('a', 'b', 'c'):
            (d / sub).mkdir()
        src = ['-f', 'lavfi', '-i', 'testsrc2=size=320x180:rate=30:duration=2']
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *src, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(d / 'a' / 'x-F.mp4')], check=True)
        shutil.copy(d / 'a' / 'x-F.mp4', d / 'b' / 'x-F.mp4')
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *src, '-vf', "drawbox=x=40:y=40:w=200:h=100:color=red:t=fill:enable='gt(t,1)'",
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(d / 'c' / 'x-F.mp4')], check=True)
        res = []
        for name, b, want in (('an identical film passes', 'b', 0), ('a film with a changed second half fails', 'c', 1)):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = compare(d / 'a', d / b, 'x', ['F'], 3, 0.98)
            res.append((name, rc == want, buf.getvalue()))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = compare(d / 'a', d / 'b', 'x', ['G'], 3, 0.98)
        res.append(('a missing film fails', rc == 1 and 'missing' in buf.getvalue(), buf.getvalue()))
    failed = [n for n, ok, _ in res if not ok]
    for n, ok, out in res:
        if not ok:
            print(f'--- {n}\n{out}')
    print(f'compare_films: {len(res) - len(failed)}/{len(res)} checks passed' + (f'; failed: {failed}' if failed else ''))
    sys.exit(1 if failed else 0)


def main():
    if sys.argv[1:] == ['--self-test']:
        self_test()
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--a', required=True, help='the rebuilt films')
    ap.add_argument('--b', required=True, help='the published films')
    ap.add_argument('--prefix', required=True)
    ap.add_argument('--films', required=True)
    ap.add_argument('--every', type=int, default=6)
    ap.add_argument('--floor', type=float, default=0.98)
    a = ap.parse_args()
    sys.exit(compare(a.a, a.b, a.prefix.rstrip('-'), [f for f in a.films.split(',') if f], a.every, a.floor))


if __name__ == '__main__':
    main()
