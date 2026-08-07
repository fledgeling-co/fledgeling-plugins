"""What is the hone's over-spill worth?

On the trued ground our R-B runs 0.274 / 0.369 / 0.231 / 0.169 / 0.145 / 0.129 / 0.101 at
0-6 / 6-14 / 14-25 / 25-40 / 40-60 / 60-90 / 90-130 px from the block's foot, reaching the
far-field 0.08 only past 130. C2's is FLAT at 0.055-0.082 the whole way -- its hone puts no
measurable light on the ground at all. Remove a distance-dependent fraction phi(d) of our
excess warm light, along the glow's own colour axis, and read the metrics.

phi keeps the seam (the icon's signature, and the 16px read) and collapses the tail, which
is also the right law: a thin emissive line falls off far faster than our blur does.
"""
import math, sys, json, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F

B = 'loop-runs/r08/'
cand = Image.open(B+'candidate-1024.png').convert('RGBA')
a = np.asarray(cand).astype(np.float64)/255.0
rgb, alpha = a[..., :3].copy(), a[..., 3]
H = 1024
Y, X = np.mgrid[0:H, 0:H]
ang = math.radians(33.0)
fline = Y - (604 - math.tan(ang)*(X-543))
blk = np.load('loop-runs/r09/work/blk_c.npy')
dist = np.load('loop-runs/r09/work/dist_c.npy')
CURL = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
inside = alpha > 0.98
TRUED = inside & ~blk & ~CURL & (fline > 0)
BASE_CHROMA = 0.086                      # our own far-field R-B, and C2's is 0.080

GLOW = np.array([1.0, 0.478, 0.235])     # #FF7A3C, the honeGlow stroke colour
GLOW = GLOW/(GLOW[0]-GLOW[2])            # normalise so a unit of R-B costs one unit

base = json.loads(open(B+'score.json').read())['sizes']
def metrics(out):
    im = Image.fromarray((np.concatenate([np.clip(out,0,1), alpha[..., None]], axis=2)*255).astype(np.uint8), 'RGBA')
    res = {}
    for size in F.SIZES:
        ci = im.resize((size, size), Image.LANCZOS)
        ri = F.normalise_reference(pathlib.Path('icon-engineC-f5665d-2.png'), size)
        gc, gr = F.to_gray(ci), F.to_gray(ri)
        m = {'lum_delta': round(float(np.abs(gc-gr).mean()), 4), 'ssim': round(F.ssim(gc, gr), 4),
             'edge_f1': round(F.edge_f1(gc, gr), 4), 'mask_iou': round(F.mask_iou(ci, ri), 4),
             'self_contrast': round(float(np.percentile(gc,90)-np.percentile(gc,10)), 4)}
        m['composite'] = F.composite_for(size, m)
        # the signature: share of tile carrying vermilion
        ch = np.asarray(ci).astype(np.float64)/255.0
        m['verm'] = round(float((((ch[...,0]-ch[...,2]) > 0.20) & (ch[...,3] > 0.5)).mean()), 4)
        res[size] = m
    return res
cal = metrics(rgb)
off = {s: {k: base[str(s)][k]-cal[s][k] for k in ('composite','self_contrast','ssim','edge_f1','lum_delta')} for s in F.SIZES}
FLOOR = {s: base[str(s)]['self_contrast']*0.94 for s in F.SIZES}

def strip(d0, d1, full=1.0):
    """phi = 0 inside d0, ramping to `full` by d1."""
    phi = np.clip((dist-d0)/max(d1-d0, 1e-6), 0, 1)*full
    excess = np.maximum((rgb[...,0]-rgb[...,2]) - BASE_CHROMA, 0.0)
    A = np.where(TRUED, excess*phi, 0.0)
    return rgb - A[..., None]*GLOW

print('%-30s %8s   %s' % ('phi(d)', 'net', ' '.join('%9d' % s for s in F.SIZES)))
for (d0, d1, full) in [(14, 45, 1.0), (14, 45, 0.7), (25, 80, 1.0), (8, 30, 1.0),
                       (14, 45, 0.5), (0, 25, 1.0), (14, 90, 1.0)]:
    out = strip(d0, d1, full)
    m = metrics(out)
    net = sum(m[s]['composite']+off[s]['composite']-base[str(s)]['composite'] for s in F.SIZES)
    cells, scs = [], []
    for s in F.SIZES:
        c = m[s]['composite']+off[s]['composite']
        sc = m[s]['self_contrast']+off[s]['self_contrast']
        cells.append('%+.4f%s' % (c-base[str(s)]['composite'], '!' if sc < FLOOR[s] else ''))
        scs.append(sc)
    print('%-30s %+8.4f   %s' % ('d0=%d d1=%d full=%.1f' % (d0, d1, full), net, ' '.join('%9s' % c for c in cells)))
    print('%-30s            %s' % ('  lum_delta', ' '.join('%+9.4f' % (m[s]['lum_delta']+off[s]['lum_delta']-base[str(s)]['lum_delta']) for s in F.SIZES)))
    print('%-30s            %s' % ('  ssim', ' '.join('%+9.4f' % (m[s]['ssim']+off[s]['ssim']-base[str(s)]['ssim']) for s in F.SIZES)))
    print('%-30s            %s' % ('  self_contrast', ' '.join('%9.4f' % v for v in scs)))
    print('%-30s            %s' % ('  vermilion %tile', ' '.join('%8.2f%%' % (100*m[s]['verm']) for s in F.SIZES)))
print('\nbaseline vermilion %%tile: ' + ' '.join('%d:%.2f%%' % (s, 100*cal[s]['verm']) for s in F.SIZES))
