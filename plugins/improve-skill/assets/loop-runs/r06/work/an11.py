"""Rubric-side checks the gate does not make: figure-ground at 128 and the
vermilion's footprint at 16, before and after."""
import numpy as np, sys, importlib.util, pathlib
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
N = 128 / 255.
spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)


def pm(pts, n):
    im = Image.new('L', (n, n), 0)
    ImageDraw.Draw(im).polygon([(float(x) * n / 1024, float(y) * n / 1024) for x, y in pts], fill=255)
    return np.asarray(im) > 127


def load(p, n):
    a = np.asarray(Image.open(p).convert('RGBA').resize((n, n), Image.LANCZOS), dtype=np.float64) / 255.
    c = a[..., :3] * a[..., 3:4] + N * (1 - a[..., 3:4])
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2], c


SRC = (('was', A / 'loop-runs/r06/work/base/candidate-1024.png'), ('now', A / 'icon.png'))

for tag, src in SRC:
    g, c = load(src, 128)
    S, CU = pm(bi.SILHOUETTE, 128), pm(bi.SHAVING_SIL, 128)
    yy, xx = np.mgrid[0:128, 0:128]
    bnd = (bi.B_LEFT + (bi.B_RIGHT - bi.B_LEFT) * xx / 128.) / 1024. * 128
    TR = (yy > bnd + 3) & ~S & ~CU
    RO = (yy <= bnd - 3) & ~S & ~CU
    blk = g[S & ~CU].mean()
    print(f'{tag} 128px figure-ground: trued/block {g[TR].mean()/blk:.2f}:1'
          f'   rough/block {g[RO].mean()/blk:.2f}:1   (block L {blk:.3f})')

for tag, src in SRC + (('ref', A / 'icon-engineC-f5665d-2.png'),):
    g, c = load(src, 16)
    ch = c[..., 0] - (c[..., 1] + c[..., 2]) / 2
    print(f'{tag} 16px vermilion footprint: {(ch > 0.06).mean()*100:.2f}% of tile')
