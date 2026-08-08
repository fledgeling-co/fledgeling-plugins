"""What carries edge_f1 at 16 and 32, cell by cell.

edge_f1 is 1.0000 at 16 today, so any small-size edit has to know which cells are
holding it up before it changes their contrast.
"""
import subprocess, pathlib, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent
NEUTRAL = 128


def render(svg, size):
    t = OUT / f'.e{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(svg), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


def ref(size):
    return Image.open(A / 'icon-engineC-f5665d-2.png').convert('RGBA').resize((size, size), Image.LANCZOS)


def to_gray(im):
    a = np.asarray(im, dtype=np.float64)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + NEUTRAL * (1 - al)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255.0


def sobel_mag(g):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


for s in (16, 32):
    gc = to_gray(render(A / 'icon.svg', s))
    gr = to_gray(ref(s))
    mc, mr = sobel_mag(gc), sobel_mag(gr)
    keep = ~rim_mask(s)
    ec, er = (mc > 0.10) & keep, (mr > 0.10) & keep
    print(f'\n=== {s}px: candidate edges {ec.sum()}, reference edges {er.sum()} (rim excluded)')
    # the curl region in this size's coords
    lo, hi = int(150 * s / 1024), int(430 * s / 1024)
    print(f'  curl rows/cols {lo}..{hi}: cand edges {ec[lo:hi, lo:hi].sum()}, ref {er[lo:hi, lo:hi].sum()}')
    print('  candidate |grad| in the curl box (x100):')
    for y in range(lo, hi):
        print('   ', ' '.join(f'{mc[y, x]*100:4.0f}' for x in range(lo, hi)))
    print('  reference |grad| in the curl box (x100):')
    for y in range(lo, hi):
        print('   ', ' '.join(f'{mr[y, x]*100:4.0f}' for x in range(lo, hi)))
