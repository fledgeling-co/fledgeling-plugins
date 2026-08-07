"""The occlusion fix, per-plane and distance-shaped, as m2 actually measured it.

sim4 applied one k to all occluded ground and lost 0.0082. That is not a verdict on the
physics, it is a verdict on a global constant: m2's per-plane ratios say the two planes
want opposite corrections.

  trued (shadow side)   ours 0.593 0.634 0.788 0.906 0.966 0.987  ->  depth .407 .366 .212 .094 .034
                        ref  0.746 0.814 0.888 0.953 0.996 1.012  ->  depth .254 .186 .112 .047 .004
                        => keep about HALF the depth, and let it die by ~70px

  rough (key side)      ours 0.911 0.936 0.954 0.970 0.979 0.983  ->  depth .089 .064 .046 .030 .021
                        ref  0.944 1.005 1.042 1.040 1.047 1.032  ->  depth .056 -.005 -.042 -.040 -.047
                        => almost no shadow past 8px, and then ~4% ABOVE far field to ~160px

The second row is the single-light violation: our ground darkens on the key side where C2's
brightens. Model it as target_depth(plane, d) and drive rho to it exactly, rather than
scaling by a constant.
"""
import math, sys, json, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F

B = 'loop-runs/r08/'
a = np.asarray(Image.open(B+'candidate-1024.png').convert('RGBA')).astype(np.float64)/255.0
rgb, alpha = a[..., :3].copy(), a[..., 3]
H = 1024
Y, X = np.mgrid[0:H, 0:H]
fline = Y - (604 - math.tan(math.radians(33.0))*(X-543))
blk  = np.load('loop-runs/r09/work/blk_c.npy')
dist = np.load('loop-runs/r09/work/dist_c.npy')
R = np.hypot(X-75.0, Y-25.0)
CURL = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
inside = alpha > 0.98
ground = inside & ~blk & ~CURL
TRUED  = ground & (fline > 0)
ROUGH  = ground & (fline <= 0)
g0 = 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2]

# rho = L / this plane's own far-field fit about the key, exactly as m2 built it
rb = np.arange(0, 1500, 25.0); idx = np.digitize(R, rb)
rho = np.ones_like(g0)
for pm in (ROUGH, TRUED):
    far = pm & (dist > 260)
    prof = np.full(len(rb)+2, np.nan)
    for i in range(1, len(rb)+1):
        s = far & (idx == i)
        if s.sum() > 200: prof[i] = g0[s].mean()
    ok = ~np.isnan(prof); xs = np.where(ok)[0]
    prof = np.interp(np.arange(len(prof)), xs, prof[ok])
    rho = np.where(pm, g0/np.maximum(prof[np.clip(idx, 0, len(prof)-1)], 1e-6), rho)

# the reference's own depth curves, read straight off m2, interpolated on band centres
BC        = np.array([4, 14, 30, 55, 90, 135, 190, 260, 400.0])
REF_TRUED = 1 - np.array([0.746, 0.814, 0.888, 0.953, 0.996, 1.012, 1.021, 1.015, 1.000])
REF_ROUGH = 1 - np.array([0.944, 1.005, 1.042, 1.040, 1.047, 1.032, 1.016, 1.000, 1.000])
tgt = np.where(TRUED, np.interp(dist, BC, REF_TRUED), np.interp(dist, BC, REF_ROUGH))
depth = 1 - rho

GLOW = np.array([1.0, 0.478, 0.235]); GLOW = GLOW/(GLOW[0]-GLOW[2])
def bloom(full=1.0, d0=14, d1=45):
    phi = np.clip((dist-d0)/max(d1-d0, 1e-6), 0, 1)*full
    excess = np.maximum((rgb[...,0]-rgb[...,2]) - 0.086, 0.0)
    return -np.where(TRUED, excess*phi, 0.0)[..., None]*GLOW

def occ(w):
    """Move each ground pixel a fraction w of the way from our depth to C2's."""
    want = depth + w*(tgt - depth)
    lift = np.where(ground, (1-want)/np.maximum(rho, 1e-6), 1.0)
    return rgb*lift[..., None] - rgb

base = json.loads(open(B+'score.json').read())['sizes']
def metrics(out):
    im = Image.fromarray((np.concatenate([np.clip(out,0,1), alpha[..., None]], axis=2)*255).astype(np.uint8), 'RGBA')
    res = {}
    for size in F.SIZES:
        ci = im.resize((size, size), Image.LANCZOS)
        ri = F.normalise_reference(pathlib.Path('icon-engineC-f5665d-2.png'), size)
        gc, gr = F.to_gray(ci), F.to_gray(ri)
        m = {'lum_delta': round(float(np.abs(gc-gr).mean()),4), 'ssim': round(F.ssim(gc,gr),4),
             'edge_f1': round(F.edge_f1(gc,gr),4), 'mask_iou': round(F.mask_iou(ci,ri),4),
             'self_contrast': round(float(np.percentile(gc,90)-np.percentile(gc,10)),4)}
        m['composite'] = F.composite_for(size, m)
        ch = np.asarray(ci).astype(np.float64)/255.0
        m['verm'] = round(float((((ch[...,0]-ch[...,2])>0.20)&(ch[...,3]>0.5)).mean()),4)
        res[size] = m
    return res
cal = metrics(rgb)
off = {s: {k: base[str(s)][k]-cal[s][k] for k in ('composite','self_contrast')} for s in F.SIZES}
FLOOR = {s: base[str(s)]['self_contrast']*0.94 for s in F.SIZES}

print('%-30s %8s   %s' % ('config', 'net', ' '.join('%9d' % s for s in F.SIZES)))
for nm, d in [('occ w=1.0 (C2 exactly)',      occ(1.0)),
              ('occ w=0.6',                   occ(0.6)),
              ('occ w=1.0, trued only',       np.where(TRUED[...,None], occ(1.0), 0)),
              ('occ w=1.0, rough only',       np.where(ROUGH[...,None], occ(1.0), 0)),
              ('bloom',                       bloom()),
              ('bloom + occ w=1.0',           bloom()+occ(1.0)),
              ('bloom + occ w=0.6',           bloom()+occ(0.6)),
              ('bloom + occ w=1.0 rough only', bloom()+np.where(ROUGH[...,None], occ(1.0), 0))]:
    m = metrics(rgb + d)
    net = sum(m[s]['composite']+off[s]['composite']-base[str(s)]['composite'] for s in F.SIZES)
    cells = []
    for s in F.SIZES:
        c = m[s]['composite']+off[s]['composite']; sc = m[s]['self_contrast']+off[s]['self_contrast']
        cells.append('%+.4f%s' % (c-base[str(s)]['composite'], '!' if sc < FLOOR[s] else ''))
    print('%-30s %+8.4f   %s   verm16 %.2f%%' % (nm, net, ' '.join('%9s' % c for c in cells), 100*m[16]['verm']))
