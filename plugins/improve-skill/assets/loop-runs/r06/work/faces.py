"""r06: is there a signed per-face brightness gap, alongside the texture gap?

Texture is mean-preserving, so it can only move ssim and edge_f1 - and at 1024 it
moves them in opposite directions. A face that is systematically too light or too
dark is the other kind of material error, it lands on lum_delta (weight 0.35 at the
large sizes, against edge's 0.25), and correcting it costs ssim nothing. This asks
whether one exists, measuring each material in ITS OWN image: our faces by our
geometry, C2's by C2's, so a placement difference is not read as a shading error.
"""
import importlib.util
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
R = A / 'loop-runs/r04'
NEUTRAL = 128 / 255.


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


gc = load(R / 'candidate-1024.png')
gr = load(R / 'reference-1024.png')

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec)
sys.modules['bi'] = bi
spec.loader.exec_module(bi)


def polymask(pts, n=1024):
    im = Image.new('L', (n, n), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(im) > 127


TOPM = polymask(bi.TOP)
FRONTM = polymask(bi.FRONT_FACE)
SOLID = polymask(bi.SILHOUETTE)
CURL = polymask(bi.SHAVING_SIL) if bi.SHAVING else np.zeros_like(SOLID)
y, x = np.mgrid[0:1024, 0:1024]
BOUND = bi.B_LEFT + (bi.B_RIGHT - bi.B_LEFT) * x / 1024.
OURS = {
    'top face':  TOPM & ~CURL,
    'front face': FRONTM & ~TOPM & ~CURL,
    'curl':      CURL,
    'trued':     (y > BOUND) & ~SOLID & ~CURL,
    'rough':     (y <= BOUND) & ~SOLID & ~CURL,
}

# C2's own regions, hand-boxed off its render in earlier probes: clean interior
# patches, chosen to sit inside one material and away from every boundary.
C2 = {
    'top face':  (330, 430, 470, 640),
    'front face': (450, 500, 430, 620),
    'curl':      (170, 300, 210, 330),
    'trued':     (700, 900, 300, 700),
    'rough':     (400, 520, 60, 260),
}

print(f'{"region":<12}{"ourL":>8}{"refL":>8}{"delta":>8}{"area%":>8}{"|d|share%":>11}')
tot = np.abs(gc - gr).sum()
for nm, m in OURS.items():
    y0, y1, x0, x1 = C2[nm]
    ref = gr[y0:y1, x0:x1]
    print(f'{nm:<12}{gc[m].mean():8.3f}{ref.mean():8.3f}{gc[m].mean()-ref.mean():+8.3f}'
          f'{100*m.mean():8.2f}{100*np.abs(gc-gr)[m].sum()/tot:11.1f}')

print(f'\nlum_delta now  {np.abs(gc-gr).mean():.4f}')
shift = gc.copy()
for nm, m in OURS.items():
    y0, y1, x0, x1 = C2[nm]
    shift[m] += gr[y0:y1, x0:x1].mean() - gc[m].mean()
print(f'if every face mean were matched exactly: {np.abs(shift-gr).mean():.4f}'
      f'   (upper bound on what a shading-only fix can win)')
