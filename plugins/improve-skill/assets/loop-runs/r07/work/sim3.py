"""Ground-field falloff budget, with the curl, the block and the hone masked out.

Same harness as loop-runs/r06/work/sim.py: apply a proposed per-plane target
profile along the shared light axis u = (x+y)/sqrt2 to the rendered 1024 PNG,
recompute fidelity.py's own metrics plus measure.py's polarity, and print the
p90/p10 the gate's contrast floor reads.
"""
import math
import sys
import json
import pathlib
import importlib.util
import numpy as np
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06'
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F  # noqa: E402

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec)
sys.modules['bi'] = bi
spec.loader.exec_module(bi)


def polymask(pts, grow=0):
    im = Image.new('L', (1024, 1024), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255,
                               outline=255, width=max(1, grow))
    a = np.asarray(im) > 127
    if grow:
        out = a.copy()
        for dy in range(-grow, grow + 1, max(1, grow // 3)):
            for dx in range(-grow, grow + 1, max(1, grow // 3)):
                out |= np.roll(np.roll(a, dy, 0), dx, 1)
        a = out
    return a


cand = Image.open(B / 'candidate-1024.png').convert('RGBA')
arr0 = np.asarray(cand, dtype=np.float64) / 255.0
H = W = 1024
Y, X = np.mgrid[0:H, 0:W]
U = (X + Y) / math.sqrt(2.0)
g0 = F.to_gray(cand)

ang = math.radians(33.0)
UXa, UYa = math.cos(ang), -math.sin(ang)
NX, NY = -math.sin(ang), -math.cos(ang)
AX, AY = 543.0 - UXa * 320.0, 604.0 - UYa * 320.0
LY = NX * (X - AX) + NY * (Y - AY)          # >0 rough, <0 trued (measure.py sign)

BLOCK = polymask(bi.SILHOUETTE, grow=6)
CURL = polymask(bi.SHAVING_SIL, grow=14) if bi.SHAVING else np.zeros((H, W), bool)
HONE = np.abs(LY) < 34
alpha = np.asarray(cand)[..., 3] > 240

PAINTABLE = alpha & ~BLOCK & ~CURL & ~HONE     # ground the two field gradients own
ROUGH = PAINTABLE & (LY > 0)
TRUED = PAINTABLE & (LY <= 0)


def profile(mask, lo, hi, step=40):
    xs, ys, ns = [], [], []
    for u in range(lo, hi, step):
        m = mask & (U >= u) & (U < u + step)
        if m.sum() < 250:
            continue
        xs.append(u + step / 2.0)
        ys.append(g0[m].mean())
        ns.append(int(m.sum()))
    return np.array(xs), np.array(ys), np.array(ns)


PR_U, PR_L, PR_N = profile(ROUGH, 0, 1040)
PT_U, PT_L, PT_N = profile(TRUED, 600, 1440)


def ratio_field(mask, cu, cl, knots):
    ku = np.array([k[0] for k in knots], float)
    kl = np.array([k[1] for k in knots], float)
    r_bin = np.interp(cu, ku, kl) / np.maximum(cl, 1e-6)
    r = np.interp(U, cu, r_bin)
    out = np.ones_like(U)
    out[mask] = r[mask]
    return out


def apply(rough_knots=None, trued_knots=None):
    a = arr0.copy()
    r = np.ones((H, W))
    if rough_knots:
        r = r * ratio_field(ROUGH, PR_U, PR_L, rough_knots)
    if trued_knots:
        r = r * ratio_field(TRUED, PT_U, PT_L, trued_knots)
    for c in range(3):
        a[..., c] = np.clip(a[..., c] * r, 0, 1)
    return Image.fromarray((a * 255).round().astype(np.uint8))


def srgb_to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lstar_img(img):
    a = np.asarray(img.convert('RGB'), float) / 255.0
    y = (0.2126 * srgb_to_lin(a[..., 0]) + 0.7152 * srgb_to_lin(a[..., 1])
         + 0.0722 * srgb_to_lin(a[..., 2]))
    return np.where(y > 0.008856, (116 * np.cbrt(y) - 16) / 100.0, 903.3 * y / 100.0)


BAND = np.abs(LY) >= 60


def polarity(img):
    L = lstar_img(img)
    rg = BAND & (LY > 0) & (L > 0.50)
    tr = BAND & (LY <= 0) & (L > 0.50)
    return L[tr].mean() - L[rg].mean(), L[rg].mean(), L[tr].mean()


def metrics(img):
    out = {}
    for size in F.SIZES:
        ci = img.resize((size, size), Image.LANCZOS) if size != 1024 else img
        ri = F.normalise_reference(B / 'reference-1024.png', size)
        gc, gr = F.to_gray(ci), F.to_gray(ri)
        m = {'lum_delta': float(np.abs(gc - gr).mean()), 'ssim': F.ssim(gc, gr),
             'edge_f1': F.edge_f1(gc, gr), 'mask_iou': F.mask_iou(ci, ri),
             'p90': float(np.percentile(gc, 90)), 'p10': float(np.percentile(gc, 10))}
        m['self_contrast'] = m['p90'] - m['p10']
        m['composite'] = F.composite_for(size, m)
        out[size] = m
    return out


BASE = metrics(cand)
REAL = json.loads((B / 'score.json').read_text())['sizes']
FLOOR = {s: REAL[str(s)]['self_contrast'] * 0.94 for s in (32, 16)}
BIAS = {s: BASE[s]['self_contrast'] - REAL[str(s)]['self_contrast'] for s in (32, 16)}


def report(name, img):
    m = metrics(img)
    net = sum(m[s]['composite'] - BASE[s]['composite'] for s in F.SIZES)
    d, rg, tr = polarity(img)
    ok = all(m[s]['self_contrast'] - BIAS[s] >= FLOOR[s] for s in (32, 16))
    print('%-34s net %+.4f  ' % (name, net)
          + ' '.join('%d:%.4f' % (s, m[s]['composite']) for s in F.SIZES)
          + '  sc32 %.3f sc16 %.3f %s  pol %+.3f  lum1024 %.4f ssim1024 %.4f'
          % (m[32]['self_contrast'], m[16]['self_contrast'], 'ok ' if ok else 'FLOOR',
             d, m[1024]['lum_delta'], m[1024]['ssim']))
    return m


if __name__ == '__main__':
    print('calibration: sim vs real composite / self_contrast')
    for s in F.SIZES:
        print('  %4d  %.4f / %.4f    sc %.4f / %.4f' % (s, BASE[s]['composite'],
              REAL[str(s)]['composite'], BASE[s]['self_contrast'], REAL[str(s)]['self_contrast']))
    print('floors (6%% below baseline real): 32 %.3f  16 %.3f' % (FLOOR[32], FLOOR[16]))
    d, rg, tr = polarity(cand)
    print('baseline polarity %+.3f (rough %.3f trued %.3f)' % (d, rg, tr))
    print('\nrough profile (u, L, n):')
    print('  ' + ' '.join('%d:%.3f' % (u, l) for u, l in zip(PR_U, PR_L)))
    print('  n ' + ' '.join('%d' % n for n in PR_N))
    print('trued profile (u, L, n):')
    print('  ' + ' '.join('%d:%.3f' % (u, l) for u, l in zip(PT_U, PT_L)))
    print('  n ' + ' '.join('%d' % n for n in PT_N))
