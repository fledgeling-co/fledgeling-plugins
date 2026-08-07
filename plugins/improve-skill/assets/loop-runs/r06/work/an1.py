"""Region decomposition of the r06 baseline residual.

Masks come from the build's own geometry (imported, not re-derived), so every
region is exactly the shape the generator draws.
"""
import numpy as np, sys, pathlib, os
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06/work/base'
NEUTRAL = 128 / 255.


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    comp = rgb * al + NEUTRAL * (1 - al)
    L = 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2]
    return L, comp


gc, cc = load(B / 'candidate-1024.png')
gr, cr = load(B / 'reference-1024.png')
print(f'cand L mean {gc.mean():.4f}   ref L mean {gr.mean():.4f}   |d| {np.abs(gc-gr).mean():.4f}')
for name, g in (('cand', gc), ('ref ', gr)):
    print(name, 'pct', {q: round(float(np.percentile(g, q)), 3) for q in (2, 10, 25, 50, 75, 90, 98)})

# ---- masks from the generator's own geometry
sys.path.insert(0, str(A))
import importlib.util
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
CURL = np.zeros_like(SOLID)
if bi.SHAVING:
    CURL = polymask(bi.SHAVING_SIL)
y, x = np.mgrid[0:1024, 0:1024]
BOUND = bi.B_LEFT + (bi.B_RIGHT - bi.B_LEFT) * x / 1024.
TRUED = (y > BOUND) & ~SOLID & ~CURL
ROUGH = (y <= BOUND) & ~SOLID & ~CURL

regions = [('top face', TOPM & ~CURL), ('front face', FRONTM & ~CURL & ~TOPM),
           ('curl', CURL), ('ground trued', TRUED), ('ground rough', ROUGH)]

tot = np.abs(gc - gr).sum()
print(f'\n{"region":<14}{"area%":>7}{"candL":>8}{"refL":>8}{"signed":>9}{"|d|":>8}{"share%":>8}')
for nm, m in regions:
    if m.sum() == 0:
        continue
    d = (gc - gr)[m]
    print(f'{nm:<14}{100*m.mean():7.2f}{gc[m].mean():8.3f}{gr[m].mean():8.3f}'
          f'{d.mean():+9.3f}{np.abs(d).mean():8.3f}{100*np.abs(d).sum()/tot:8.1f}')

np.save(B / 'masks.npy', np.stack([TOPM, FRONTM, SOLID, CURL, TRUED, ROUGH]))
