"""(a) Where our p90 pixels live. (b) The reference's own block and its shadow.

Coarse L grids for both images so the fields can be read rather than guessed,
plus the reference's block found by its own darkness rather than by our mask.
"""
import numpy as np, sys, pathlib, importlib.util
from PIL import Image, ImageDraw
from collections import deque

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06/work/base'
NEUTRAL = 128 / 255.


def load(p, n=1024):
    im = Image.open(p).convert('RGBA')
    if n != im.width:
        im = im.resize((n, n), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    comp = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2], comp


gc, cc = load(B / 'candidate-1024.png')
gr, cr = load(B / 'reference-1024.png')

print('=== (a) 16px map: c = candidate L, r = reference L, . = our p90 pixels ===')
g16c, _ = load(B / 'candidate-1024.png', 16)
g16r, _ = load(B / 'reference-1024.png', 16)
p90 = np.percentile(g16c, 90); p10 = np.percentile(g16c, 10)
print('candidate 16px (H = in the top 10%, L = in the bottom 10%)')
for r in range(16):
    print(' '.join(('H' if g16c[r, c] >= p90 else 'L' if g16c[r, c] <= p10 else f'{int(g16c[r,c]*9)}')
                   for c in range(16)))
print('reference 16px')
for r in range(16):
    print(' '.join(f'{int(g16r[r,c]*9)}' for c in range(16)))

# ---- the reference's own block
dark = gr < 0.42
lab = np.zeros(dark.shape, np.int32)
n = 0
for sy in range(0, 1024, 8):
    for sx in range(0, 1024, 8):
        if dark[sy, sx] and lab[sy, sx] == 0:
            n += 1
            q = deque([(sy, sx)]); lab[sy, sx] = n; sz = 0
            while q:
                cy, cx = q.popleft(); sz += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < 1024 and 0 <= nx < 1024 and dark[ny, nx] and lab[ny, nx] == 0:
                        lab[ny, nx] = n; q.append((ny, nx))
sizes = [(int((lab == i).sum()), i) for i in range(1, n + 1)]
sizes.sort(reverse=True)
big = lab == sizes[0][1]
ys, xs = np.nonzero(big)
print(f'\n=== (b) reference block: {big.sum()} px ({100*big.mean():.1f}% of tile), '
      f'bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] '
      f'({xs.max()-xs.min()}x{ys.max()-ys.min()})  centroid ({xs.mean():.0f},{ys.mean():.0f})')
print(f'    ref block L: mean {gr[big].mean():.3f}  p5 {np.percentile(gr[big],5):.3f}'
      f'  p50 {np.percentile(gr[big],50):.3f}  p95 {np.percentile(gr[big],95):.3f}')
d = cr[big]
i = np.argmin(gr[big])
print(f'    ref block darkest pixel rgb {d[i].round(3)}  sat {(d[i].max()-d[i].min())/max(d[i].max(),1e-6):.3f}')

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)


def polymask(pts, nn=1024):
    im = Image.new('L', (nn, nn), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(im) > 127


OURS = polymask(bi.SILHOUETTE)
oys, oxs = np.nonzero(OURS)
print(f'    our block:  {OURS.sum()} px ({100*OURS.mean():.1f}%), bbox x[{oxs.min()},{oxs.max()}]'
      f' y[{oys.min()},{oys.max()}]  centroid ({oxs.mean():.0f},{oys.mean():.0f})')
print(f'    our block L: mean {gc[OURS].mean():.3f}  p5 {np.percentile(gc[OURS],5):.3f}'
      f'  p50 {np.percentile(gc[OURS],50):.3f}  p95 {np.percentile(gc[OURS],95):.3f}')
d = cc[OURS]; i = np.argmin(gc[OURS])
print(f'    our block darkest pixel rgb {d[i].round(3)}  sat {(d[i].max()-d[i].min())/max(d[i].max(),1e-6):.3f}')
np.save(B / 'refblock.npy', big)
