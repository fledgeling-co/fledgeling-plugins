"""Image-space simulator for the round-9 candidate edit.

Two effects, both applied to the r08 1024 render exactly as the SVG layers would:

  shadow scale k : the cast+contact shadows are alpha composites over the ground, so
                   L' = L(1-a) + Ls*a and the ratio to the unoccluded field is
                   rho = 1 - a(1 - Ls/L). Scaling every shadow opacity by k gives
                   rho_k = 1 - k(1 - rho), i.e. exactly linear in k.
  bounce beta    : the block's lit faces throwing light back onto the ground on the
                   KEY side. Modelled as the block silhouette offset UP-light, blurred,
                   drawn under the block: L'' = L'(1-b) + Lb*b.

Calibrated: metrics recomputed on the unmodified downsample are compared to the real
r08 score, and the per-size offset is carried onto the modified numbers.
"""
import math, sys, json, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, 'loop-runs/r09/work')
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F

NEUTRAL = 128/255.0
B = 'loop-runs/r08/'
cand = Image.open(B+'candidate-1024.png').convert('RGBA')
a = np.asarray(cand).astype(np.float64)/255.0
rgb, alpha = a[..., :3].copy(), a[..., 3]
g = 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2]
H, W = g.shape
Y, X = np.mgrid[0:H, 0:W]
R = np.hypot(X-75.0, Y-25.0)
CURL = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
ang = math.radians(33.0)
fline = Y - (604 - math.tan(ang)*(X-543))
blk = np.load('loop-runs/r09/work/blk_c.npy')
dist = np.load('loop-runs/r09/work/dist_c.npy')

# --- rho: our current ground / our own far-field fit, per plane -------------
ground = (alpha > 0.98) & (~blk) & (~CURL)
rb = np.arange(0, 1500, 25.0); idx = np.digitize(R, rb)
rho = np.ones_like(g)
for pm in (fline <= 0, fline > 0):
    far = ground & pm & (dist > 260)
    prof = np.full(len(rb)+2, np.nan)
    for i in range(1, len(rb)+1):
        s = far & (idx == i)
        if s.sum() > 200: prof[i] = g[s].mean()
    ok = ~np.isnan(prof); xs = np.where(ok)[0]
    prof = np.interp(np.arange(len(prof)), xs, prof[ok])
    fit = prof[np.clip(idx, 0, len(prof)-1)]
    rho = np.where(pm, g/np.maximum(fit, 1e-6), rho)
OCC = ground & (dist < 260) & (rho < 1.0)          # only where we are actually occluding

# --- bounce field: block silhouette pushed toward the key, blurred ----------
KEY = np.array([75.0-492.0, 25.0-449.0]); KEY /= np.linalg.norm(KEY)   # up-light unit vector
def bounce_field(push, sigma):
    m = Image.fromarray((blk*255).astype(np.uint8))
    m = m.transform(m.size, Image.AFFINE, (1, 0, -KEY[0]*push, 0, 1, -KEY[1]*push), resample=Image.BILINEAR)
    m = m.filter(ImageFilter.GaussianBlur(sigma))
    b = np.asarray(m).astype(np.float64)/255.0
    b[blk] = 0.0
    return b * (alpha > 0.98) * (~CURL)

def simulate(k, beta, push, sigma, Lb=0.93):
    lift = np.where(OCC, (1 - k*(1 - rho))/np.maximum(rho, 1e-6), 1.0)
    out = rgb * lift[..., None]
    b = bounce_field(push, sigma) * beta
    out = out*(1-b[..., None]) + Lb*b[..., None]
    return np.clip(out, 0, 1)

def metrics(out):
    im = Image.fromarray((np.concatenate([out, alpha[..., None]], axis=2)*255).astype(np.uint8), 'RGBA')
    res = {}
    for size in F.SIZES:
        ci = im.resize((size, size), Image.LANCZOS)
        ri = F.normalise_reference(__import__('pathlib').Path('icon-engineC-f5665d-2.png'), size)
        gc, gr = F.to_gray(ci), F.to_gray(ri)
        m = {'lum_delta': round(float(np.abs(gc-gr).mean()), 4), 'ssim': round(F.ssim(gc, gr), 4),
             'edge_f1': round(F.edge_f1(gc, gr), 4), 'mask_iou': round(F.mask_iou(ci, ri), 4),
             'self_contrast': round(float(np.percentile(gc, 90)-np.percentile(gc, 10)), 4)}
        m['composite'] = F.composite_for(size, m)
        res[size] = m
    return res

base = json.loads(open(B+'score.json').read())['sizes']
cal = metrics(rgb)
off = {s: {kk: base[str(s)][kk]-cal[s][kk] for kk in ('composite', 'self_contrast', 'lum_delta', 'ssim', 'edge_f1')} for s in F.SIZES}
print('calibration offset (real r08 - downsample sim):')
for s in F.SIZES:
    print('  %4d comp %+.4f  sc %+.4f' % (s, off[s]['composite'], off[s]['self_contrast']))

FLOOR = {s: round(base[str(s)]['self_contrast']*0.94, 4) for s in F.SIZES}
print('\nself_contrast floors (6%% below r08): ' + '  '.join('%d:%.4f' % (s, FLOOR[s]) for s in F.SIZES))

print('\n%-28s %8s %s' % ('k / beta / push / sigma', 'net', ' '.join('%9d' % s for s in F.SIZES)))
for (k, beta, push, sigma) in [
        (1.00, 0.00,  0, 1),
        (0.80, 0.00,  0, 1),
        (0.65, 0.00,  0, 1),
        (1.00, 0.10, 130, 55),
        (0.80, 0.10, 130, 55),
        (0.65, 0.10, 130, 55),
        (0.65, 0.16, 130, 55),
        (0.55, 0.16, 130, 55),
        (0.65, 0.16, 100, 70),
]:
    out = simulate(k, beta, push, sigma)
    m = metrics(out)
    net = sum(m[s]['composite']+off[s]['composite']-base[str(s)]['composite'] for s in F.SIZES)
    cells = []
    for s in F.SIZES:
        c = m[s]['composite']+off[s]['composite']
        sc = m[s]['self_contrast']+off[s]['self_contrast']
        cells.append('%+.4f%s' % (c-base[str(s)]['composite'], '!' if sc < FLOOR[s] else ' '))
    print('%-28s %+8.4f %s' % ('k=%.2f b=%.2f p=%d s=%d' % (k, beta, push, sigma), net, ' '.join('%9s' % c for c in cells)))
