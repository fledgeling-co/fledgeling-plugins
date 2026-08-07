"""Budget the ground-field edit before a constant moves.

Applies a proposed per-plane luminance profile (as a function of the shared
light axis u = (x+y)/sqrt2, out of the top-left key corner) to the rendered 1024
candidate and recomputes every gate metric plus the measure.py polarity
invariant, so p90-p10 and the polarity are known before the build script moves.
Same approximation as r06/work/sim.py: small sizes come from a LANCZOS
downsample of the 1024 render, so the baseline row is printed both ways.
"""
import math
import sys
import json
import pathlib
import numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06'
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F  # noqa: E402

cand = Image.open(B / 'candidate-1024.png').convert('RGBA')
arr0 = np.asarray(cand, dtype=np.float64) / 255.0
H = W = 1024
Y, X = np.mgrid[0:H, 0:W]
U = (X + Y) / math.sqrt(2.0)

g0 = F.to_gray(cand)
ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang) * (X - 543))

GROUND = g0 > 0.45                       # everything that is not the block
ROUGH = (f_ours < 0) & GROUND
TRUED = (f_ours >= 0) & GROUND


def profile(mask, lo, hi, step):
    """current mean L per u bin inside mask"""
    xs, ys = [], []
    for u in range(lo, hi, step):
        m = mask & (U >= u) & (U < u + step)
        if m.sum() < 300:
            continue
        xs.append(u + step / 2.0)
        ys.append(g0[m].mean())
    return np.array(xs), np.array(ys)


PR_U, PR_L = profile(ROUGH, 0, 1000, 40)
PT_U, PT_L = profile(TRUED, 600, 1400, 40)


def ratio_field(mask, cu, cl, knots):
    """knots: list of (u, target L). Piecewise linear target; returns a
    multiplicative ratio field over the mask, 1.0 elsewhere."""
    ku = np.array([k[0] for k in knots], dtype=float)
    kl = np.array([k[1] for k in knots], dtype=float)
    tgt_at_bin = np.interp(cu, ku, kl)
    r_at_bin = tgt_at_bin / np.maximum(cl, 1e-6)
    r = np.interp(U, cu, r_at_bin)
    out = np.ones_like(U)
    out[mask] = r[mask]
    return out


def apply(rough_knots, trued_knots):
    a = arr0.copy()
    r = np.ones((H, W))
    if rough_knots:
        r *= ratio_field(ROUGH, PR_U, PR_L, rough_knots)
    if trued_knots:
        r *= ratio_field(TRUED, PT_U, PT_L, trued_knots)
    for c in range(3):
        a[..., c] = np.clip(a[..., c] * r, 0, 1)
    return Image.fromarray((a * 255).round().astype(np.uint8))


def srgb_to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lstar_img(img):
    a = np.asarray(img.convert('RGB'), dtype=np.float64) / 255.0
    y = (0.2126 * srgb_to_lin(a[..., 0]) + 0.7152 * srgb_to_lin(a[..., 1])
         + 0.0722 * srgb_to_lin(a[..., 2]))
    return np.where(y > 0.008856, (116 * np.cbrt(y) - 16) / 100.0, 903.3 * y / 100.0)


# measure.py's own geometry
UXa, UYa = math.cos(ang), -math.sin(ang)
NX, NY = -math.sin(ang), -math.cos(ang)
AX = 543.0 - UXa * 320.0
AY = 604.0 - UYa * 320.0
LY = NX * (X - AX) + NY * (Y - AY)
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


if __name__ == '__main__':
    real = json.loads((B / 'score.json').read_text())['sizes']
    base = metrics(cand)
    print('calibration -- simulated baseline vs the harness real render')
    print('%6s%10s%10s%9s%9s' % ('size', 'sim', 'real', 'sim sc', 'real sc'))
    for s in F.SIZES:
        print('%6d%10.4f%10.4f%9.4f%9.4f' % (s, base[s]['composite'], real[str(s)]['composite'],
                                             base[s]['self_contrast'], real[str(s)]['self_contrast']))
    d, rg, tr = polarity(cand)
    print('baseline polarity %+.3f (rough %.3f trued %.3f)' % (d, rg, tr))
    print('\ncurrent profiles')
    print('rough u/L:', ' '.join('%d:%.3f' % (u, l) for u, l in zip(PR_U[::2], PR_L[::2])))
    print('trued u/L:', ' '.join('%d:%.3f' % (u, l) for u, l in zip(PT_U[::2], PT_L[::2])))
    print('\np90/p10 owners at 16 and 32 px')
    for size in (32, 16):
        ci = cand.resize((size, size), Image.LANCZOS)
        gc = F.to_gray(ci)
        uu = ((np.mgrid[0:size, 0:size][1] + np.mgrid[0:size, 0:size][0]) + 0.5) * (1024.0 / size) / math.sqrt(2)
        yy, xx = np.mgrid[0:size, 0:size]
        cx, cy = (xx + 0.5) * 1024.0 / size, (yy + 0.5) * 1024.0 / size
        fo = cy - (604 - math.tan(ang) * (cx - 543))
        blk = gc < 0.45
        top = gc >= np.percentile(gc, 90)
        bot = gc <= np.percentile(gc, 10)
        print(' %2dpx p90=%.3f p10=%.3f | top10%%: trued %.0f%% rough %.0f%% block %.0f%%  (u range %.0f-%.0f)'
              % (size, np.percentile(gc, 90), np.percentile(gc, 10),
                 100 * (top & (fo > 0) & ~blk).sum() / top.sum(),
                 100 * (top & (fo <= 0) & ~blk).sum() / top.sum(),
                 100 * (top & blk).sum() / top.sum(), uu[top].min(), uu[top].max()))
        print('        bot10%%: block %.0f%% ground %.0f%%'
              % (100 * (bot & blk).sum() / bot.sum(), 100 * (bot & ~blk).sum() / bot.sum()))
