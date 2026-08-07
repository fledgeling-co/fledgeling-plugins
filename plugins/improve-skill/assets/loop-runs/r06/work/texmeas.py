"""r06: the texture instrument. One high-pass, applied the same way to both images.

Relief is a MULTIPLICATIVE modulation, so the quantity that transfers between two
images at different brightness is relative amplitude - the high-passed standard
deviation over the local mean - not absolute sd. Everything here is measured that
way, in each image's own frame, with the block, its shadow and the curl masked out
so a boundary is never read as texture.

Usage: texmeas.py <png> [<png> ...]   - the reference is always measured too, so
every row has its target beside it.
"""
import importlib.util
import math
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw
from numpy.lib.stride_tricks import sliding_window_view

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
NEUTRAL = 128 / 255.
spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec)
sys.modules['bi'] = bi
spec.loader.exec_module(bi)


def load(p, n=1024):
    im = Image.open(p).convert('RGBA')
    if im.width != n:
        im = im.resize((n, n), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def polymask(pts, n=1024):
    q = Image.new('L', (n, n), 0)
    ImageDraw.Draw(q).polygon([(float(px), float(py)) for px, py in pts], fill=255)
    return np.asarray(q) > 127


def hp(g, w=9):
    """high-pass: the pixel minus its own 9x9 mean. Returns the full-size field with
    a NaN border, so it can be combined with masks without index bookkeeping."""
    out = np.full(g.shape, np.nan)
    v = sliding_window_view(g, (w, w)).mean(axis=(2, 3))
    out[w // 2:-(w // 2), w // 2:-(w // 2)] = g[w // 2:-(w // 2), w // 2:-(w // 2)] - v
    return out


def amp(g, h, m):
    m = m & ~np.isnan(h)
    if m.sum() < 400:
        return float('nan'), float('nan')
    return 100 * np.nanstd(h[m]) / g[m].mean(), g[m].mean()


# ---- our geometry, and local-frame coordinates for every pixel
y, x = np.mgrid[0:1024, 0:1024]
SOLID = polymask(bi.SILHOUETTE)
CURL = polymask(bi.SHAVING_SIL) if bi.SHAVING else np.zeros_like(SOLID)
TOPM = polymask(bi.TOP)
FRONTM = polymask(bi.FRONT_FACE) & ~TOPM
# the cast shadow is drawn from the silhouette offset by (30,34) and blurred; dilate
# generously so no shadow pixel is counted as ground texture
SHAD = polymask([(px + 30, py + 34) for px, py in bi.SILHOUETTE])
for _ in range(3):
    SHAD = SHAD | np.roll(SHAD, 14, 0) | np.roll(SHAD, 14, 1)
GND = ~SOLID & ~CURL & ~SHAD
LY = (x - bi.AX) * bi.NX + (y - bi.AY) * bi.NY          # N is a unit normal: local y

BANDS = [(20, 120), (120, 220), (220, 320), (320, 420), (420, 520), (520, 700)]

# ---- C2, in its own frame. Its cut is y = -0.8078x + 998 (found by its own step in
# profile.py); distance from the cut is the perpendicular, positive on the rough side.
SL, C0 = -math.tan(math.radians(38.93)), 998
gr = load(A / 'loop-runs/r04/reference-1024.png')
hr = hp(gr)
DR = (SL * x + C0 - y) / math.hypot(1, SL)
GND_R = (gr > 0.45) & (DR > 0)
REF_BANDS = {}
for a, b in BANDS:
    REF_BANDS[(a, b)] = amp(gr, hr, GND_R & (DR >= a) & (DR < b))
_t = np.zeros((1024, 1024), bool)
_t[330:430, 470:640] = True
REF_TOP = amp(gr, hr, _t)
_f = np.zeros((1024, 1024), bool)
_f[470:505, 430:610] = True
REF_FRONT = amp(gr, hr, _f)

for path in sys.argv[1:]:
    g = load(path)
    h = hp(g)
    print(f'\n=== {path} ===')
    print(f'{"rough ground band":<20}{"ourL":>7}{"our%":>7}{"refL":>7}{"ref%":>7}{"short":>8}')
    for a, b in BANDS:
        ca, cl = amp(g, h, GND & (LY >= a) & (LY < b))
        ra, rl = REF_BANDS[(a, b)]
        print(f'{f"ly {a}-{b}":<20}{cl:7.3f}{ca:7.2f}{rl:7.3f}{ra:7.2f}{ra/max(ca,1e-6):7.1f}x')
    ca, cl = amp(g, h, GND & (LY >= -420) & (LY < -40))
    print(f'{"trued ground":<20}{cl:7.3f}{ca:7.2f}' + ' ' * 14 + '(C2 trued 0.58-0.75%)')
    for nm, m, ref in (('top face', TOPM & ~CURL, REF_TOP), ('front face', FRONTM & ~CURL, REF_FRONT)):
        ca, cl = amp(g, h, m)
        print(f'{nm:<20}{cl:7.3f}{ca:7.2f}{ref[1]:7.3f}{ref[0]:7.2f}{ref[0]/max(ca,1e-6):7.1f}x')
