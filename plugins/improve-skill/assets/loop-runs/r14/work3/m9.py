"""Final read: the curl against the ground immediately beside it, and the 16px
edge cells the guard was set on.
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
    t = W / f'.h{tag}{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(svg), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


def sobel_mag(g):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def ref(size):
    return Image.open(A / 'icon-engineC-f5665d-2.png').convert('RGBA').resize((size, size), Image.LANCZOS)


# un-planed ground immediately above-right of the curl, clear of block and curl
GND = (450, 120, 620, 240)
CURL = (170, 200, 330, 400)

for name, svg in (('r13', W / 'icon.baseline.svg'), ('r14', A / 'icon.svg')):
    print(name)
    for s in (16, 32, 1024):
        g = gray(rend(svg, s, name))
        k = s / 1024.0

        def box(b):
            x0, y0, x1, y1 = b
            a0, b0 = int(y0 * k), int(x0 * k)
            return g[a0:max(int(y1 * k), a0 + 1), b0:max(int(x1 * k), b0 + 1)]

        c, gd = box(CURL).mean(), box(GND).mean()
        print(f'  {s:5d}px curl {c:.4f}  ground beside it {gd:.4f}  '
              f'separation {gd-c:+.4f}  ratio {gd/c:.3f}')
    m16 = sobel_mag(gray(rend(svg, 16, name)))
    m32 = sobel_mag(gray(rend(svg, 32, name)))
    print(f'  16px curl cells |grad|>0.10: {(m16[2:6,2:6]>0.10).sum()}   '
          f'32px curl cells: {(m32[4:13,4:13]>0.10).sum()}')

gr16, gr32 = gray(ref(16)), gray(ref(32))
print(f'C2: 16px curl cells {(sobel_mag(gr16)[2:6,2:6]>0.10).sum()}   '
      f'32px curl cells {(sobel_mag(gr32)[4:13,4:13]>0.10).sum()}')
