"""Rubric guards: the curl's own figure-ground at small size, and the block's,
before and after. The block must not have moved at all -- this was a curl-only edit.
"""
import subprocess, pathlib, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
W = A / 'loop-runs/r14/work3'
NEUTRAL = 128


def gray(im):
    a = np.asarray(im, dtype=np.float64)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + NEUTRAL * (1 - al)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255.0


def rend(svg, size, tag):
    t = W / f'.g{tag}{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(svg), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


for name, svg in (('r13', W / 'icon.baseline.svg'), ('r14', A / 'icon.svg')):
    print(name)
    for s in (16, 32, 128):
        g = gray(rend(svg, s, name))
        k = s / 1024.0

        def box(x0, y0, x1, y1):
            a0, b0 = int(y0 * k), int(x0 * k)
            return g[a0:max(int(y1 * k), a0 + 1), b0:max(int(x1 * k), b0 + 1)]

        curl = box(170, 200, 330, 400).mean()
        gnd = box(560, 120, 760, 260).mean()
        blk = box(520, 430, 700, 560).mean()
        print(f'  {s:4d}px  curl {curl:.4f}  un-planed ground {gnd:.4f}  '
              f'ground:curl {gnd/curl:.3f}  |  block {blk:.4f}  ground:block {gnd/blk:.2f}:1')
