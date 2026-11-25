#!/usr/bin/env python3
"""Make the voiced cut of a rendered film, and gate a delivery folder before anything is published.

    delivery.py remux --master out/acme-K02.mp4 --audio assets/sound_vo.wav --out out/acme-K02-vo.mp4 [--limit 0.6]
    delivery.py check --dir delivery/ --prefix acme --films O,K02,K03 [--published published.txt]
                      [--size 1920x1080] [--lufs -14] [--lufs-tolerance 0.5] [--true-peak -1.0]
    delivery.py publish --from out/ --to delivery/ site/films/ --prefix acme --films O,K02 [--published published.txt]
    delivery.py sheet --file out/acme-O-vo.mp4 --at 1.5,99 [--crop 0.3,0.08,0.4,0.2] --out sheet.png
    delivery.py sheet --file out/acme-O-vo.mp4 --lines films/O/timeline.json --out align.png
    delivery.py --self-test

A series ships two files per film from ONE render: <prefix>-<id>.mp4 (the muted master, music and effects) and
<prefix>-<id>-vo.mp4 (the same picture, the voiced mix). `remux` copies the video stream untouched and swaps the
audio, so the two cuts share every frame and a player switching between them keeps its place. AAC encoding can push
a mix past its measured peak: a voiced mix at -2.4 dBTP came out at +1.3 dBTP after encoding. When `check` fails a
file on true peak, remux it with `--limit 0.6`, a limiter ahead of the encoder (that file then measured -3.5 dBTP and
-14.3 LUFS).

`check` reads every file and exits 0 only when each film has:
  - both files, at the stated size;
  - the same picture in both, compared as an MD5 of the copied video stream;
  - integrated loudness within tolerance of the target and true peak at or below the ceiling, on both;
and every name in --published (one file name per line, the names already linked from somewhere) still exists.
It prints one line per film and a verdict line, `delivery: PASS 10/10` or `delivery: FAIL 8/10`.
Exit 1 is a failed check, exit 2 a usage error or a missing tool. Read the exit code on its own line: a pipe into
`tail` reports tail's status, and a FAIL once printed beside rc=0 that way.

`publish` runs the same check over a staging folder and copies both cuts of every film to each destination only when
it passes, so a failed render never leaves last round's file live beside new ones under the same names.

`sheet` pulls frames from a finished file, each stamped with its time, optionally cropped by fractions of the frame
(x, y, w, h), and tiles them into one image to open: the lockup in each place it appears, a poster candidate, a
seam. With --lines it takes one frame 1 s after each narration line starts, labelled with the line id, which is the
check that the voice lands on the frame it describes.
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


def remux(master, audio, out, limit=None):
    af = ['-af', f'alimiter=limit={limit}:attack=1:release=40:level=false'] if limit else []
    r = run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(master), '-i', str(audio), '-map', '0:v', '-map', '1:a',
             '-c:v', 'copy', *af, '-c:a', 'aac', '-b:a', '192k', '-shortest', str(out)])
    if r.returncode:
        sys.exit(f'remux failed: {r.stderr.strip()[:400]}')


def picture_md5(path):
    r = run(['ffmpeg', '-loglevel', 'error', '-i', str(path), '-map', '0:v:0', '-c', 'copy', '-f', 'md5', '-'])
    return r.stdout.strip() if r.returncode == 0 else None


def momentary(path):
    """Momentary loudness every 100 ms (LUFS), from ffmpeg's EBU R128 meter."""
    r = run(['ffmpeg', '-nostats', '-i', str(path), '-af', 'ebur128=metadata=1,ametadata=print:key=lavfi.r128.M',
             '-f', 'null', '-'])
    return [float(v) for v in re.findall(r'lavfi\.r128\.M=(-?[\d.]+)', r.stderr + r.stdout)]


def same_sound(a, b):
    """True when two files carry the same mix: their momentary loudness differs by under 0.5 LU on average. Compared
    through the meter rather than the bytes, because the two cuts' audio is encoded by different encoders."""
    ma, mb = momentary(a), momentary(b)
    n = min(len(ma), len(mb))
    pairs = [(x, y) for x, y in zip(ma[:n], mb[:n]) if x > -70 and y > -70]
    return bool(pairs) and sum(abs(x - y) for x, y in pairs) / len(pairs) < 0.5


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
    d, prefix = Path(d), prefix.rstrip('-')
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
                    problems.append(f'{f.name} true peak {tp} dBTP, ceiling {tp_max} (remux with --limit 0.6)')
            a, b = picture_md5(mute), picture_md5(vo)
            if not a or a != b:
                problems.append('the two cuts do not share one picture (render once, then remux)')
            if same_sound(mute, vo):
                problems.append('the voiced cut has the muted master\'s sound (no narration was mixed in)')
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


def publish(src, dests, prefix, films, published, want_size, lufs, tol, tp_max):
    rc = check(src, prefix, films, None, want_size, lufs, tol, tp_max)
    if rc:
        print('publish: nothing copied; fix the staged files first')
        return rc
    prefix = prefix.rstrip('-')
    for dest in dests:
        Path(dest).mkdir(parents=True, exist_ok=True)
        for fid in films:
            for name in (f'{prefix}-{fid}.mp4', f'{prefix}-{fid}-vo.mp4'):
                shutil.copy2(Path(src) / name, Path(dest) / name)
    print(f'publish: {2 * len(films)} files copied to {", ".join(str(x) for x in dests)}')
    if published:
        return check(dests[0], prefix, films, published, want_size, lufs, tol, tp_max)
    return 0


FONT = next((f for f in ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc',
                         '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') if Path(f).exists()), None)


def sheet(path, times, out, labels=None, crop=None, cols=4, width=480):
    """Frames at `times` (seconds), stamped, cropped by fractions (x, y, w, h), tiled `cols` wide."""
    labels = labels or [f'{t:.2f}s' for t in times]
    with tempfile.TemporaryDirectory() as d:
        for k, (t, lab) in enumerate(zip(times, labels)):
            vf = []
            if crop:
                x, y, w, h = crop
                vf.append(f'crop=iw*{w}:ih*{h}:iw*{x}:ih*{y}')
            vf.append(f'scale={width}:-2')
            font = f":fontfile='{FONT}'" if FONT else ''
            vf.append(f"drawtext=text='{lab}'{font}:x=8:y=8:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=4")
            r = run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(path), '-frames:v', '1',
                     '-vf', ','.join(vf), str(Path(d) / f'f{k:03d}.png')])
            if r.returncode:
                sys.exit(f'sheet: frame at {t}s failed: {r.stderr.strip()[:300]}')
        n = len(times)
        rows = (n + cols - 1) // cols
        r = run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(Path(d) / 'f%03d.png'), '-vf',
                 f'tile={min(cols, n)}x{rows}:padding=4:color=white', '-frames:v', '1', str(out)])
        if r.returncode:
            sys.exit(f'sheet: tiling failed: {r.stderr.strip()[:300]}')
    print(f'{out}: {n} frames from {path}')


def line_times(timeline):
    import json
    tl = json.loads(Path(timeline).read_text())
    ls = sorted(tl['lines'].items(), key=lambda kv: kv[1]['start'])
    if not ls:
        sys.exit(f'{timeline} places no narration (a --mute-only build?)')
    return [round(l['start'] + 1.0, 2) for _, l in ls], [f'{lid} @ {l["start"] + 1.0:.1f}s' for lid, l in ls]


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
        # the good voiced cut carries a different mix at the master's level: the tone, plus a second voice in its second
        # half, brought to the same integrated loudness
        run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i',
             'aevalsrc=0.25*sin(2*PI*440*t)+if(gt(t\\,1)\\,0.6*sin(2*PI*660*t)\\,0):s=48000:d=2', str(t / 'raw.wav')])
        li, _ = loudness(t / 'raw.wav')
        run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(t / 'raw.wav'), '-af', f'volume={base_lufs - li:.2f}dB', str(t / 'tone.wav')])
        tp_ceiling = max(base_tp, loudness(t / 'tone.wav')[1]) + 1.0   # the fixtures' own peaks, with headroom
        run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=330:duration=2:sample_rate=48000',
             str(t / 'vo.wav')])
        # the voiced cut gets the same level as the master so the good case passes the loudness checks
        run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(t / 'x-A.mp4'), '-map', '0:a', str(t / 'same.wav')])
        remux(t / 'x-A.mp4', t / 'tone.wav', t / 'x-A-vo.mp4')

        def gate(films, published=None):
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = check(t, 'x', films, published, '320x180', base_lufs, 0.5, tp_ceiling)
            return rc, buf.getvalue()

        rc, out = gate(['A'])
        results.append(('a remuxed pair passes', rc == 0, out))

        clip('x-S.mp4')
        remux(t / 'x-S.mp4', t / 'same.wav', t / 'x-S-vo.mp4')
        rc, out = gate(['S'])
        results.append(('a voiced cut with the master\'s own sound fails', rc == 1 and 'no narration' in out, out))

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

        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = publish(t, [t / 'live'], 'x', ['A', 'C'], None, '320x180', base_lufs, 0.5, tp_ceiling)
        out = buf.getvalue()
        results.append(('publish copies nothing when one film fails', rc == 1 and not (t / 'live' / 'x-A.mp4').exists(), out))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = publish(t, [t / 'live', t / 'site'], 'x-', ['A'], None, '320x180', base_lufs, 0.5, tp_ceiling)
        out = buf.getvalue()
        results.append(('publish copies both cuts to every destination on a pass (and forgives a trailing dash)',
                        rc == 0 and all((t / d / n).exists() for d in ('live', 'site') for n in ('x-A.mp4', 'x-A-vo.mp4')), out))

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sheet(t / 'x-A.mp4', [0.2, 1.0, 1.8], t / 'sheet.png', crop=(0, 0, 0.5, 0.5), cols=2, width=160)
        dims = run(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x', str(t / 'sheet.png')]).stdout.strip()
        results.append(('sheet tiles three stamped crops two wide', dims == '324x184', f'sheet is {dims} (2 x 160 + a 4 px gap, by 2 x 90 + 4)'))

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
    p.add_argument('--limit', type=float, help='linear limiter ceiling ahead of the AAC encoder, e.g. 0.6')
    p = sub.add_parser('check')
    p.add_argument('--dir', required=True)
    p.add_argument('--prefix', required=True)
    p.add_argument('--films', required=True, help='comma-separated film ids, e.g. O,K02,K03')
    p.add_argument('--published')
    p.add_argument('--size', default='1920x1080')
    p.add_argument('--lufs', type=float, default=-14.0)
    p.add_argument('--lufs-tolerance', type=float, default=0.5)
    p.add_argument('--true-peak', type=float, default=-1.0)
    p = sub.add_parser('publish')
    p.add_argument('--from', dest='src', required=True)
    p.add_argument('--to', nargs='+', required=True)
    p.add_argument('--prefix', required=True)
    p.add_argument('--films', required=True)
    p.add_argument('--published')
    p.add_argument('--size', default='1920x1080')
    p.add_argument('--lufs', type=float, default=-14.0)
    p.add_argument('--lufs-tolerance', type=float, default=0.5)
    p.add_argument('--true-peak', type=float, default=-1.0)
    p = sub.add_parser('sheet')
    p.add_argument('--file', required=True)
    p.add_argument('--at', help='comma-separated seconds')
    p.add_argument('--lines', help='a built timeline.json: one frame 1 s after each line starts')
    p.add_argument('--crop', help='x,y,w,h as fractions of the frame')
    p.add_argument('--cols', type=int, default=4)
    p.add_argument('--width', type=int, default=480)
    p.add_argument('--out', required=True)
    a = ap.parse_args()
    need('ffmpeg')
    need('ffprobe')
    if a.cmd == 'remux':
        remux(a.master, a.audio, a.out, a.limit)
        print(f'{a.out}: picture copied from {a.master}, audio from {a.audio}')
    elif a.cmd == 'publish':
        sys.exit(publish(a.src, a.to, a.prefix, [f for f in a.films.split(',') if f], a.published, a.size, a.lufs,
                         a.lufs_tolerance, a.true_peak))
    elif a.cmd == 'sheet':
        if bool(a.at) == bool(a.lines):
            sys.exit('sheet: pass --at or --lines')
        times, labels = line_times(a.lines) if a.lines else ([float(x) for x in a.at.split(',')], None)
        crop = tuple(float(x) for x in a.crop.split(',')) if a.crop else None
        sheet(a.file, times, a.out, labels, crop, a.cols, a.width)
    else:
        sys.exit(check(a.dir, a.prefix, [f for f in a.films.split(',') if f], a.published, a.size, a.lufs,
                       a.lufs_tolerance, a.true_peak))


if __name__ == '__main__':
    main()
