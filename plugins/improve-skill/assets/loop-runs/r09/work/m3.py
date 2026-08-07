"""Is the occlusion directional? Ratio L/f(r) in angular sectors about the block
centroid, at a fixed distance band, for both images. Plus the hue of each image's
darkest contact pixels.
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
blk_c = np.load('loop-runs/r09/work/blk_c.npy'); blk_r = np.load('loop-runs/r09/work/blk_r.npy')
dist_c = np.load('loop-runs/r09/work/dist_c.npy'); dist_r = np.load('loop-runs/r09/work/dist_r.npy')

ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang)*(X-543))
f_ref  = Y - (-0.8026*X + 991.2)

def field_ratio(g, alpha, blk, dist, fline):
    """Per-PLANE fit of L vs r on far pixels; pooling the two planes makes the trued
    side read >1 and the rough side <1 purely from the finish step."""
    ground = (alpha > 0.98) & (~blk) & (~CURL)
    ratio = np.ones_like(g)
    rb = np.arange(0, 1500, 25.0); idx = np.digitize(R, rb)
    for pm in (fline <= 0, fline > 0):
        far = ground & pm & (dist > 260)
        prof = np.full(len(rb)+2, np.nan)
        for i in range(1, len(rb)+1):
            s = far & (idx == i)
            if s.sum() > 200: prof[i] = g[s].mean()
        ok = ~np.isnan(prof); xs = np.where(ok)[0]
        prof = np.interp(np.arange(len(prof)), xs, prof[ok])
        fit = prof[np.clip(idx, 0, len(prof)-1)]
        ratio = np.where(pm, g/np.maximum(fit,1e-6), ratio)
    return ratio, ground

SECT = [(-180,-135),(-135,-90),(-90,-45),(-45,0),(0,45),(45,90),(90,135),(135,180)]
NAMES = ['upleft','up','upright','right','downright','down','downleft','left']
for name, g, alpha, blk, dist, fl in (('OURS', gc, ac, blk_c, dist_c, f_ours), ('REF ', gr, ar, blk_r, dist_r, f_ref)):
    ratio, ground = field_ratio(g, alpha, blk, dist, fl)
    cy, cx = np.argwhere(blk).mean(axis=0)
    th = np.degrees(np.arctan2(Y-cy, X-cx))
    print('\n=== %s === block centroid (%.0f, %.0f)' % (name, cx, cy))
    for lo, hi in ((8,45),(45,110),(110,200)):
        band = ground & (dist>=lo) & (dist<hi)
        row=[]
        for (a0,a1) in SECT:
            s = band & (th>=a0) & (th<a1)
            row.append('%6.3f'%ratio[s].mean() if s.sum()>200 else '     -')
        print('  d %3d-%3d : '%(lo,hi) + ' '.join('%s=%s'%(n,v) for n,v in zip(NAMES,row)))

# darkest contact pixels: hue and saturation
print('\ncontact-shadow colour (ground pixels, dist 0-25, darkest 5%)')
for name, rgb, g, alpha, blk, dist in (('OURS', crgb, gc, ac, blk_c, dist_c), ('REF ', rrgb, gr, ar, blk_r, dist_r)):
    ground = (alpha>0.98) & (~blk) & (~CURL) & (dist>0) & (dist<25)
    v = g[ground]; thr = np.percentile(v, 5)
    s = ground & (g<=thr)
    px = rgb[s]
    mx, mn = px.max(axis=1), px.min(axis=1)
    sat = np.where(mx>0, (mx-mn)/np.maximum(mx,1e-6), 0)
    print('  %s L=%.3f  RGB=(%.3f,%.3f,%.3f)  sat=%.3f  n=%d' % (
        name, g[s].mean(), px[:,0].mean(), px[:,1].mean(), px[:,2].mean(), sat.mean(), s.sum()))
    # and the same image's far ground colour for reference
    fg = (alpha>0.98)&(~blk)&(~CURL)&(dist>300)
    fp = rgb[fg]; mx, mn = fp.max(axis=1), fp.min(axis=1)
    print('       far ground L=%.3f RGB=(%.3f,%.3f,%.3f) sat=%.3f' % (
        g[fg].mean(), fp[:,0].mean(), fp[:,1].mean(), fp[:,2].mean(), np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0).mean()))
