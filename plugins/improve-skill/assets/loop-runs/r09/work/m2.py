"""AO / cast-shadow profile: ground luminance beside the block, with each image's own
global light falloff divided out.

For each image and each ground plane: fit L as a function of r = |p - (75,25)| using
only pixels FAR from the block (d > 260), then report the mean ratio L / f(r) in bands
of distance-from-block. Ratio < 1 near the block = occlusion. This separates the
contact/cast shadow from the global falloff, which distance-from-block otherwise
confounds with.
"""
import math, sys, numpy as np
from PIL import Image
sys.path.insert(0, 'loop-runs/r09/work')
import nd

NEUTRAL = 128/255.0
def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64)/255.0
    rgb, al = a[...,:3], a[...,3:4]
    rgb = rgb*al + NEUTRAL*(1-al)
    g = 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2]
    return rgb, g, a[...,3]
B='loop-runs/r08/'
crgb, gc, ac = load(B+'candidate-1024.png')
rrgb, gr, ar = load(B+'reference-1024.png')
H,W = gc.shape
Y,X = np.mgrid[0:H,0:W]
R = np.hypot(X-75.0, Y-25.0)
CURL = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang)*(X-543))
f_ref  = Y - (-0.8026*X + 991.2)
BANDS = [(0,8),(8,20),(20,40),(40,70),(70,110),(110,160),(160,220),(220,300),(300,9e9)]

def block_mask(g, alpha, thr=0.45):
    m = (g < thr) & (alpha > 0.98)
    m = nd.opening(m, 9)
    m = nd.convex_fill(m)
    return m

def analyse(name, g, alpha, fline, blk):
    dist = nd.edt(blk)
    ground = (alpha > 0.98) & (~blk) & (~CURL)
    print('\n=== %s ===  block frac %.3f' % (name, blk.mean()))
    out = {}
    for pname, pm in (('rough', fline <= 0), ('trued', fline > 0)):
        m = ground & pm
        far = m & (dist > 260)
        rb = np.arange(0, 1500, 25.0)
        idx = np.digitize(R, rb)
        prof = np.full(len(rb)+2, np.nan)
        for i in range(1, len(rb)+1):
            s = far & (idx == i)
            if s.sum() > 200: prof[i] = g[s].mean()
        ok = ~np.isnan(prof)
        if ok.sum() < 4:
            print('  %-6s: too few far pixels (%d)' % (pname, far.sum())); continue
        xs = np.where(ok)[0]; prof = np.interp(np.arange(len(prof)), xs, prof[ok])
        fit = prof[np.clip(idx, 0, len(prof)-1)]
        ratio = g / np.maximum(fit, 1e-6)
        print('  %-6s  n=%7d  far residual %.4f' % (pname, m.sum(), np.abs(g[far]-fit[far]).mean()))
        print('     band :' + ' '.join('%7s' % ('%d-%d'%(lo,hi) if hi<9e8 else '>300') for lo,hi in BANDS))
        row = []
        for lo, hi in BANDS:
            s = m & (dist >= lo) & (dist < hi)
            row.append('%7.3f' % ratio[s].mean() if s.sum() > 300 else '      -')
            out[(pname,lo)] = ratio[s].mean() if s.sum() > 300 else None
        print('     L/f  :' + ' '.join(row))
    return dist, out

blk_c = block_mask(gc, ac); blk_r = block_mask(gr, ar)
np.save('loop-runs/r09/work/blk_c.npy', blk_c); np.save('loop-runs/r09/work/blk_r.npy', blk_r)
dc, oc = analyse('OURS  ', gc, ac, f_ours, blk_c)
dr, orr = analyse('REF C2', gr, ar, f_ref, blk_r)
np.save('loop-runs/r09/work/dist_c.npy', dc); np.save('loop-runs/r09/work/dist_r.npy', dr)

print('\nratio-of-ratios (ref / ours) — <1 means the reference is darker there than we are')
for pname in ('rough','trued'):
    row=[]
    for lo,hi in BANDS:
        a,b = oc.get((pname,lo)), orr.get((pname,lo))
        row.append('%7.3f'%(b/a) if a and b else '      -')
    print('  %-6s:'%pname + ' '.join(row))
