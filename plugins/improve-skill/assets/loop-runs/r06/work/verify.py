"""r06: verify the sample boxes sit where I claim, and check the block's own level.

Two things faces.py could get wrong. (a) The C2 patch boxes are hand-placed; if one
strays onto the ground its "face" reading is fiction. (b) A block that is globally too
light matters differently from one face being too light, because p10 - the bottom of
the self_contrast term - lives in the block, so darkening it is one of the few edits
that lowers lum_delta and RAISES the legibility floor's headroom at the same time.
C2's block is found by its own darkness, not by our mask.
"""
import importlib.util
import pathlib
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
R = A / 'loop-runs/r04'
W = A / 'loop-runs/r06/work'
NEUTRAL = 128 / 255.


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2], c


gc, cc = load(R / 'candidate-1024.png')
gr, cr = load(R / 'reference-1024.png')

BOXES = {'top face': (330, 430, 470, 640), 'front face': (450, 500, 430, 620),
         'rough': (400, 520, 60, 260), 'trued': (700, 900, 300, 700)}
im = Image.open(R / 'reference-1024.png').convert('RGB')
d = ImageDraw.Draw(im)
for nm, (y0, y1, x0, x1) in BOXES.items():
    d.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=3)
    d.text((x0 + 4, y0 + 4), nm, fill=(255, 0, 0))
im.save(W / 'boxes-ref.png')

# ---- C2's block, by its own darkness
dark = gr < 0.42
lab = np.zeros(dark.shape, np.int32)
n = 0
for sy in range(0, 1024, 6):
    for sx in range(0, 1024, 6):
        if dark[sy, sx] and lab[sy, sx] == 0:
            n += 1
            q = deque([(sy, sx)])
            lab[sy, sx] = n
            while q:
                cy, cx = q.popleft()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < 1024 and 0 <= nx < 1024 and dark[ny, nx] and lab[ny, nx] == 0:
                        lab[ny, nx] = n
                        q.append((ny, nx))
sizes = sorted(((int((lab == i).sum()), i) for i in range(1, n + 1)), reverse=True)
BIG = lab == sizes[0][1]

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec)
sys.modules['bi'] = bi
spec.loader.exec_module(bi)


def polymask(pts, nn=1024):
    q = Image.new('L', (nn, nn), 0)
    ImageDraw.Draw(q).polygon([(float(px), float(py)) for px, py in pts], fill=255)
    return np.asarray(q) > 127


OUR = polymask(bi.SILHOUETTE)
print(f'{"block":<8}{"area%":>7}{"mean":>7}{"p2":>7}{"p10":>7}{"p50":>7}{"p90":>7}{"p98":>7}')
for nm, g, m in (('ref', gr, BIG), ('cand', gc, OUR)):
    v = [np.percentile(g[m], p) for p in (2, 10, 50, 90, 98)]
    print(f'{nm:<8}{100*m.mean():7.2f}{g[m].mean():7.3f}' + ''.join(f'{q:7.3f}' for q in v))

print('\nwhole-image percentiles (what self_contrast is made of)')
for nm, g in (('cand', gc), ('ref ', gr)):
    print(nm, {q: round(float(np.percentile(g, q)), 3) for q in (2, 10, 50, 90, 98)})
print(f'\nwrote {W}/boxes-ref.png')
