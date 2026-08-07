"""Face luminances on the block, in a coordinate both blocks share.

PCA the block mask to get its long axis, then profile L against the normalised
across-axis coordinate t (0 = the top-face's far edge, 1 = the foot). That gives the
top/front face split, each face's own ramp, and each face's darkest pixel and the hue
there, without needing the two blocks to sit in the same place.
"""
import math, sys, numpy as np
from PIL import Image
NEUTRAL = 128/255.0
def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64)/255.0
    rgb, al = a[...,:3], a[...,3:4]
    rgb = rgb*al + NEUTRAL*(1-al)
    return rgb, 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2]
B='loop-runs/r08/'
crgb, gc = load(B+'candidate-1024.png')
rrgb, gr = load(B+'reference-1024.png')
H, W = gc.shape
Y, X = np.mgrid[0:H, 0:W]
blk_c = np.load('loop-runs/r09/work/blk_c.npy'); blk_r = np.load('loop-runs/r09/work/blk_r.npy')

def sat(px):
    mx, mn = px.max(axis=-1), px.min(axis=-1)
    return np.where(mx > 0, (mx-mn)/np.maximum(mx, 1e-6), 0)

for name, rgb, g, blk in (('OURS', crgb, gc, blk_c), ('REF ', rrgb, gr, blk_r)):
    pts = np.argwhere(blk).astype(np.float64)      # (y, x)
    c = pts.mean(axis=0)
    cov = np.cov((pts-c).T)
    ev, evec = np.linalg.eigh(cov)
    long_v = evec[:, -1]; short_v = evec[:, 0]     # (y, x) components
    s = ((Y-c[1]*0-c[0])*short_v[0] + (X-c[1])*short_v[1])
    lo, hi = s[blk].min(), s[blk].max()
    if np.mean(g[blk & (s < lo+(hi-lo)*0.25)]) < np.mean(g[blk & (s > hi-(hi-lo)*0.25)]):
        s = -s; lo, hi = -hi, -lo                  # orient so t=0 is the BRIGHT (top-face) end
    t = (s-lo)/(hi-lo)
    print('\n=== %s ===  long axis %.1f deg, extent %.0f x %.0f px' % (
        name, math.degrees(math.atan2(-long_v[0], long_v[1])), 2*math.sqrt(ev[-1])*2, (hi-lo)))
    print('  t      :' + ' '.join('%6.2f' % x for x in np.arange(0.05, 1.0, 0.1)))
    row_l, row_s = [], []
    for t0 in np.arange(0.0, 1.0, 0.1):
        m = blk & (t >= t0) & (t < t0+0.1)
        row_l.append('%6.3f' % g[m].mean() if m.sum() > 200 else '     -')
        row_s.append('%6.3f' % sat(rgb[m]).mean() if m.sum() > 200 else '     -')
    print('  L      :' + ' '.join(row_l))
    print('  sat    :' + ' '.join(row_s))
    px = rgb[blk]; gg = g[blk]
    for q, lab in ((2, 'darkest 2%'), (50, 'median'), (98, 'brightest 2%')):
        if q == 50: sel = np.abs(gg-np.percentile(gg, 50)) < 0.005
        elif q == 2: sel = gg <= np.percentile(gg, 2)
        else: sel = gg >= np.percentile(gg, 98)
        print('  %-12s L=%.3f  RGB=(%.3f,%.3f,%.3f)  sat=%.3f' % (
            lab, gg[sel].mean(), px[sel][:,0].mean(), px[sel][:,1].mean(), px[sel][:,2].mean(), sat(px[sel]).mean()))
    print('  p90-p10 within block: %.3f   (p98/p02 ratio %.2f)' % (
        np.percentile(gg,90)-np.percentile(gg,10), np.percentile(gg,98)/max(np.percentile(gg,2),1e-6)))
