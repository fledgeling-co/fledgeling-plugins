#!/usr/bin/env python3
"""Make the voiced cut of a rendered film, and gate a delivery folder before anything is published.

    delivery.py remux --master out/acme-K02.mp4 --audio assets/sound_vo.wav --out out/acme-K02-vo.mp4
    delivery.py check --dir delivery/ --prefix acme --films O,K02,K03 [--published published.txt]
                      [--size 1920x1080] [--lufs -14] [--lufs-tolerance 0.5] [--true-peak -1.0]
    delivery.py --self-test

A series ships two files per film from ONE render: <prefix>-<id>.mp4 (the muted master, music and effects) and
<prefix>-<id>-vo.mp4 (the same picture, the voiced mix). `remux` copies the video stream untouched and swaps the
audio, so the two cuts share every frame and a player switching between them keeps its place.

`check` reads every file and exits 0 only when each film has:
  - both files, at the stated size;
  - the same picture in both, compared as an MD5 of the copied video stream;
  - integrated loudness within tolerance of the target and true peak at or below the ceiling, on both;
and every name in --published (one file name per line, the names already linked from somewhere) still exists.
It prints one line per film and a verdict line, `delivery: PASS 10/10` or `delivery: FAIL 8/10`.
Exit 1 is a failed check, exit 2 a usage error or a missing tool.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def need(tool):
    if not shutil.which(tool):
        print(f'{tool} is not on PATH', file=sys.stderr)
        sys.exit(2)


def remux(master, audio, out):
    r = run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(master), '-i', str(audio), '-map', '0:v', '-map', '1:a',
             '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', str(out)])
    if r.returncode:
        sys.exit(f'remux failed: {r.stderr.strip()[:400]}')


def picture_md5(path):
    r = run(['ffmpeg', '-loglevel', 'error', '-i', str(path), '-map', '0:v:0', '-c', 'copy', '-f', 'md5', '-'])
    return r.stdout.strip() if r.returncode == 0 else None


def size(path):
    r = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of',
             'csv=p=0:s=x', str(path)])
    return r.stdout.strip()


def loudness(path):
    """(integrated LUFS, true peak dBTP) from ffmpeg's EBU R128 meter, or (None, None)."""
    r = run(['ffmpeg', '-nostats', '-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'])
    tail = r.stderr[r.stderr.rfind('Summary:'):]
    i = re.search(r'I:\s*(-?[\d.]+|-inf)\s*LUFS', tail)
    p = re.search(r'True peak:\s*Peak:\s*(-?[\d.]+|-inf)\s*dBFS', tail, re.S)
    f = lambda m: None if not m or m.group(1) == '-inf' else float(m.group(1))
    return f(i), f(p)


def check(d, prefix, films, published, want_size, lufs, tol, tp_max):
    d = Path(d)
    ok_count, lines = 0, []
    for fid in films:
        mute, vo = d / f'{prefix}-{fid}.mp4', d / f'{prefix}-{fid}-vo.mp4'
        problems = []
        for f in (mute, vo):
            if not f.exists():
                problems.append(f'{f.name} missing')
        if not problems:
            for f in (mute, vo):
                s = size(f)
                if want_size and s != want_size:
                    problems.append(f'{f.name} is {s}, not {want_size}')
                li, tp = loudness(f)
                if li is None or abs(li - lufs) > tol:
                    problems.append(f'{f.name} integrated {li} LUFS, target {lufs}±{tol}')
                if tp is None or tp > tp_max:
                    problems.append(f'{f.name} true peak {tp} dBTP, ceiling {tp_max}')
            a, b = picture_md5(mute), picture_md5(vo)
            if not a or a != b:
                problems.append('the two cuts do not share one picture (render once, then remux)')
        if problems:
            lines.append(f'  FAIL {fid}: ' + '; '.join(problems))
        else:
            ok_count += 1
            li, tp = loudness(vo)
            lines.append(f'  ok   {fid}: {want_size or size(vo)}, voiced {li} LUFS / {tp} dBTP, picture shared')
    missing = []
    if published:
        names = [n.strip() for n in Path(published).read_text().splitlines() if n.strip() and not n.startswith('#')]
        missing = [n for n in names if not (d / n).exists()]
        for n in missing:
            lines.append(f'  FAIL published name gone: {n} (something may already link to it; keep the name)')
    print('\n'.join(lines))
    passed = ok_count == len(films) and not missing
    print(f'delivery: {"PASS" if passed else "FAIL"} {ok_count}/{len(films)}'
          + (f', {len(missing)} published names missing' if missing else ''))
    return 0 if passed else 1


def self_test():
    need('ffmpeg')
    need('ffprobe')
    results = []
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)

        def clip(name, pattern='testsrc', vol=0.0, src=None):
            # 2 s, 320x180, 10 fps, a 440 Hz tone; vol is a gain in dB
            v = ['-f', 'lavfi', '-i', f'{pattern}=size=320x180:rate=10:duration=2']
            a = ['-f', 'lavfi', '-i', 'sine=frequency=440:duration=2:sample_rate=48000']
            run(['ffmpeg', '-loglevel', 'error', '-y', *v, *a, '-af', f'volume={vol}dB', '-c:v', 'libx264', '-pix_fmt',
                 'yuv420p', '-c:a', 'aac', '-shortest', str(t / name)])

        clip('x-A.mp4')
        base_lufs, base_tp = loudness(t / 'x-A.mp4')
        tp_ceiling = base_tp + 0.5
        run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=330:duration=2:sample_rate=48000',
             str(t / 'vo.wav')])
        # the voiced cut gets the same level as the master so the good case passes the loudness checks
        run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(t / 'x-A.mp4'), '-map', '0:a', str(t / 'same.wav')])
        remux(t / 'x-A.mp4', t / 'same.wav', t / 'x-A-vo.mp4')

        def gate(films, published=None):
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = check(t, 'x', films, published, '320x180', base_lufs, 0.5, tp_ceiling)
            return rc, buf.getvalue()

        rc, out = gate(['A'])
        results.append(('a remuxed pair passes', rc == 0, out))

        clip('x-B.mp4')
        rc, out = gate(['B'])
        results.append(('a missing voiced cut fails', rc == 1 and 'x-B-vo.mp4 missing' in out, out))

        clip('x-C.mp4')
        clip('x-C-vo.mp4', pattern='smptebars')
        rc, out = gate(['C'])
        results.append(('a voiced cut rendered separately fails', rc == 1 and 'share one picture' in out, out))

        clip('x-D.mp4')
        run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(t / 'x-D.mp4'), '-map', '0:a', '-af', 'volume=8dB',
             str(t / 'loud.wav')])
        remux(t / 'x-D.mp4', t / 'loud.wav', t / 'x-D-vo.mp4')
        rc, out = gate(['D'])
        results.append(('a voiced cut 8 dB hot fails loudness', rc == 1 and 'integrated' in out, out))

        (t / 'published.txt').write_text('x-A.mp4\nx-A-vo.mp4\nx-renamed.mp4\n')
        rc, out = gate(['A'], t / 'published.txt')
        results.append(('a published name that disappeared fails', rc == 1 and 'x-renamed.mp4' in out, out))

    failed = [n for n, ok, _ in results if not ok]
    for n, ok, out in results:
        if not ok:
            print(f'--- {n}\n{out}')
    print(f'self-test: {len(results) - len(failed)}/{len(results)} passed' +
          (f'; failed: {", ".join(failed)}' if failed else ''))
    sys.exit(1 if failed else 0)


def main():
    if '--self-test' in sys.argv:
        self_test()
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('remux')
    p.add_argument('--master', required=True)
    p.add_argument('--audio', required=True)
    p.add_argument('--out', required=True)
    p = sub.add_parser('check')
    p.add_argument('--dir', required=True)
    p.add_argument('--prefix', required=True)
    p.add_argument('--films', required=True, help='comma-separated film ids, e.g. O,K02,K03')
    p.add_argument('--published')
    p.add_argument('--size', default='1920x1080')
    p.add_argument('--lufs', type=float, default=-14.0)
    p.add_argument('--lufs-tolerance', type=float, default=0.5)
    p.add_argument('--true-peak', type=float, default=-1.0)
    a = ap.parse_args()
    need('ffmpeg')
    need('ffprobe')
    if a.cmd == 'remux':
        remux(a.master, a.audio, a.out)
        print(f'{a.out}: picture copied from {a.master}, audio from {a.audio}')
    else:
        sys.exit(check(a.dir, a.prefix, [f for f in a.films.split(',') if f], a.published, a.size, a.lufs,
                       a.lufs_tolerance, a.true_peak))


if __name__ == '__main__':
    main()
