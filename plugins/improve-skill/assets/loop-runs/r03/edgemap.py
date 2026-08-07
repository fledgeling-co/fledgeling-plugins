"""Where do the 32/16px edges disagree? Split into recall misses (reference edges the
candidate does not cover) and precision misses (candidate edges near no reference edge),
and localise both, so a small-size repair can be aimed rather than guessed."""
import subprocess, tempfile, pathlib, sys
import numpy as np
from PIL import Image

NEUTRAL = 128


def rend(p, s):
    p = pathlib.Path(p)
    if p.suffix.lower() == '.svg':
        t = pathlib.Path(tempfile.mktemp(suffix='.png'))
        subprocess.run(['rsvg-convert', '-w', str(s), '-h', str(s), str(p), '-o', str(t)], check=True)
        im = Image.open(t).convert('RGBA')
        t.unlink()
        return im
    return Image.open(p).convert('RGBA').resize((s, s), Image.LANCZOS)


def gray(im):
    a = np.asarray(im, dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (NEUTRAL / 255.) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def sob(g, th=0.10):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > th * 4


def dil(m, r=1):
    o = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o


cand = sys.argv[1] if len(sys.argv) > 1 else 'icon.svg'
ref = 'icon-engineC-f5665d-2.png'
for s in (32, 16):
    gc, gr = gray(rend(cand, s)), gray(rend(ref, s))
    ea, eb = sob(gc), sob(gr)
    miss = eb & ~dil(ea)      # reference edges the candidate misses  -> recall loss
    false_ = ea & ~dil(eb)    # candidate edges near no reference edge -> precision loss
    print('%dpx  cand edges %d  ref edges %d   recall misses %d   precision misses %d'
          % (s, ea.sum(), eb.sum(), miss.sum(), false_.sum()))
    print('  recall-miss map (. none, # missed ref edge, o candidate false edge):')
    for y in range(s):
        row = ''
        for x in range(s):
            row += '#' if miss[y, x] else ('o' if false_[y, x] else ('+' if (ea[y, x] and eb[y, x]) else '.'))
        print('   %2d %s' % (y, row))
