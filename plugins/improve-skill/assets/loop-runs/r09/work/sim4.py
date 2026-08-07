"""Bloom collapse and the directional-occlusion fix, together and apart.

The occlusion fix is the rubric edit (our shadow is omnidirectional and 1.6x too deep;
C2's is a down-light lobe with a measured up-light bounce at 1.09-1.11x). The bloom
collapse is the fundable one. The question here is only whether the pair costs the 32px
cell more than the gate's 0.005 per-size tolerance.
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
ang = math.radians(33.0)
fline = Y - (604 - math.tan(ang)*(X-543))
blk = np.load('loop-runs/r09/work/blk_c.npy')
dist = np.load('loop-runs/r09/work/dist_c.npy')
R = np.hypot(X-75.0, Y-25.0)
CURL = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
inside = alpha > 0.98
TRUED = inside & ~blk & ~CURL & (fline > 0)
g0 = 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2]
ground = inside & ~blk & ~CURL
rb = np.arange(0, 1500, 25.0); idx = np.digitize(R, rb)
rho = np.ones_like(g0)
for pm in (fline <= 0, fline > 0):
    far = ground & pm & (dist > 260)
    prof = np.full(len(rb)+2, np.nan)
    for i in range(1, len(rb)+1):
        s = far & (idx == i)
        if s.sum() > 200: prof[i] = g0[s].mean()
    ok = ~np.isnan(prof); xs = np.where(ok)[0]
    prof = np.interp(np.arange(len(prof)), xs, prof[ok])
    rho = np.where(pm, g0/np.maximum(prof[np.clip(idx,0,len(prof)-1)], 1e-6), rho)
OCC = ground & (dist < 260) & (rho < 1.0)
GLOW = np.array([1.0, 0.478, 0.235]); GLOW = GLOW/(GLOW[0]-GLOW[2])
KEY = np.array([75.0-492.0, 25.0-449.0]); KEY /= np.linalg.norm(KEY)

def blurf(g, s):
    rad = int(math.ceil(3*s)); k = np.exp(-0.5*(np.arange(-rad, rad+1)/s)**2); k /= k.sum()
    p = np.pad(g, ((rad, rad), (0, 0)), mode='edge')
    o = sum(k[i]*p[i:i+g.shape[0]] for i in range(2*rad+1))
    p = np.pad(o, ((0, 0), (rad, rad)), mode='edge')
    return sum(k[i]*p[:, i:i+g.shape[1]] for i in range(2*rad+1))

_bf = {}
def bounce(push, sigma):
    if (push, sigma) in _bf: return _bf[(push, sigma)]
    m = np.zeros((H, H))
    ys, xs = np.nonzero(blk)
    yy = np.clip((ys - KEY[1]*push).astype(int), 0, H-1); xx = np.clip((xs - KEY[0]*push).astype(int), 0, H-1)
    m[yy, xx] = 1.0
    b = blurf(m, sigma); b[blk] = 0.0
    b *= inside & ~CURL
    _bf[(push, sigma)] = b
    return b

def build(strip_full, k_occ, beta):
    out = rgb.copy()
    if strip_full:
        phi = np.clip((dist-14)/31.0, 0, 1)*strip_full
        excess = np.maximum((rgb[...,0]-rgb[...,2]) - 0.086, 0.0)
        out = out - np.where(TRUED, excess*phi, 0.0)[..., None]*GLOW
    if k_occ != 1.0:
        lift = np.where(OCC, (1-k_occ*(1-rho))/np.maximum(rho,1e-6), 1.0)
        out = out*lift[..., None]
    if beta:
        b = bounce(130, 55)*beta
        out = out*(1-b[..., None]) + 0.93*b[..., None]
    return out

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
print('%-34s %8s   %s' % ('config', 'net', ' '.join('%9d' % s for s in F.SIZES)))
for nm, args in [('bloom only',              (1.0, 1.00, 0.00)),
                 ('AO only  k=0.60 b=0.22',  (0.0, 0.60, 0.22)),
                 ('bloom + AO k=0.60 b=0.22',(1.0, 0.60, 0.22)),
                 ('bloom + AO k=0.75 b=0.14',(1.0, 0.75, 0.14)),
                 ('bloom + AO k=0.85 b=0.10',(1.0, 0.85, 0.10))]:
    m = metrics(build(*args))
    net = sum(m[s]['composite']+off[s]['composite']-base[str(s)]['composite'] for s in F.SIZES)
    cells = []
    for s in F.SIZES:
        c = m[s]['composite']+off[s]['composite']; sc = m[s]['self_contrast']+off[s]['self_contrast']
        cells.append('%+.4f%s' % (c-base[str(s)]['composite'], '!' if sc < FLOOR[s] else ''))
    print('%-34s %+8.4f   %s' % (nm, net, ' '.join('%9s' % c for c in cells)))
    print('%-34s            %s' % ('  vermilion %tile', ' '.join('%8.2f%%' % (100*m[s]['verm']) for s in F.SIZES)))
