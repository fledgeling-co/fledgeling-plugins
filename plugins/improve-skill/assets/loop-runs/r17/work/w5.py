"""Edge audit at 32 and 16px: exactly which cells are false positives and false
negatives, and what feature owns each. edge_f1 is 0.35 of the 32/16 composite and
the only structural term left with headroom, so it is worth locating rather than
reasoning about."""
import subprocess
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def lum(im):
    a = np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0
    c = a[..., :3] * a[..., 3:4] + NEUTRAL * (1 - a[..., 3:4])
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def rsvg(svg, size):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


def sobel(g, thresh=0.10):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy), np.hypot(gx, gy) > thresh * 4


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


ref = Image.open('icon-engineC-f5665d-2.png')
for s in (32, 16, 128, 256):
    gc, gr = lum(rsvg('icon.svg', s)), lum(ref.resize((s, s), Image.LANCZOS))
    mc, ec = sobel(gc)
    mr, er = sobel(gr)
    keep = ~rim_mask(s)
    ec, er = ec & keep, er & keep
    fp = ec & ~dilate(er)
    fn = er & ~dilate(ec)
    prec = (ec & dilate(er)).sum() / max(ec.sum(), 1)
    rec = (er & dilate(ec)).sum() / max(er.sum(), 1)
    print(f'=== {s}px  cand edges {ec.sum()}  ref edges {er.sum()}  FP {fp.sum()}  FN {fn.sum()}'
          f'  prec {prec:.4f} rec {rec:.4f} f1 {2*prec*rec/max(prec+rec,1e-9):.4f}')
    if s <= 32:
        print('    map: . none  C cand-only(FP)  R ref-only(FN)  # both/near')
        for y in range(s):
            row = ''
            for x in range(s):
                if not keep[y, x]:
                    row += ' '
                elif fp[y, x]:
                    row += 'C'
                elif fn[y, x]:
                    row += 'R'
                elif ec[y, x] or er[y, x]:
                    row += '#'
                else:
                    row += '.'
            print('    ' + row)
        # for each FP, how strong is the reference's gradient there?
        ys, xs = np.nonzero(fp)
        if len(ys):
            print(f'    FP cells: cand |grad| mean {mc[fp].mean():.3f}  ref |grad| there mean {mr[fp].mean():.3f}'
                  f'  (threshold {0.10*4:.2f})')
        ys, xs = np.nonzero(fn)
        if len(ys):
            print(f'    FN cells: ref |grad| mean {mr[fn].mean():.3f}  cand |grad| there mean {mc[fn].mean():.3f}')
