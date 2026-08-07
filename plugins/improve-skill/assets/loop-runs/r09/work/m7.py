"""How far does the hone's light spill onto the ground, in ours and in C2?

The rendered crops show our trued plane carrying a wide orange wash where C2's stays
neutral grey a few px from the edge. Measure it as chroma (R-B, and saturation) against
distance from the block's foot, on the trued side only, so the hone CORE -- the icon's
signature -- is separated from the ground BLOOM, which is what looks wrong.
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
    return rgb, 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2], a[...,3]
B='loop-runs/r08/'
crgb, gc, ac = load(B+'candidate-1024.png')
rrgb, gr, ar = load(B+'reference-1024.png')
H, W = gc.shape
Y, X = np.mgrid[0:H, 0:W]
ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang)*(X-543))
f_ref  = Y - (-0.8026*X + 991.2)
blk_c = np.load('loop-runs/r09/work/blk_c.npy'); blk_r = np.load('loop-runs/r09/work/blk_r.npy')
d_c = np.load('loop-runs/r09/work/dist_c.npy'); d_r = np.load('loop-runs/r09/work/dist_r.npy')
CURL_C = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
CURL_R = (X>=178)&(X<=492)&(Y>=50)&(Y<=414)

BANDS = [(0,6),(6,14),(14,25),(25,40),(40,60),(60,90),(90,130),(130,190),(190,280),(280,9e9)]
print('%-6s %-10s' % ('img','stat') + ' '.join('%7s' % ('%d-%d'%(a,b) if b<9e8 else '>280') for a,b in BANDS))
for name, rgb, g, al, blk, dist, fl, curl in (
        ('OURS', crgb, gc, ac, blk_c, d_c, f_ours, CURL_C),
        ('REF ', rrgb, gr, ar, blk_r, d_r, f_ref, CURL_R)):
    m0 = (al>0.98) & (~blk) & (~curl) & (fl>0)      # trued ground only
    chroma = rgb[...,0]-rgb[...,2]
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    sat = np.where(mx>0, (mx-mn)/np.maximum(mx,1e-6), 0)
    for lab, arr in (('R-B', chroma), ('sat', sat), ('L', g)):
        row=[]
        for lo,hi in BANDS:
            s = m0 & (dist>=lo) & (dist<hi)
            row.append('%7.3f'%arr[s].mean() if s.sum()>200 else '      -')
        print('%-6s %-10s' % (name, lab) + ' '.join(row))
    print()

# how much of the tile carries a visible orange cast at all
for name, rgb, al in (('OURS', crgb, ac), ('REF ', rrgb, ar)):
    ch = rgb[...,0]-rgb[...,2]
    ins = al>0.98
    for t in (0.06, 0.10, 0.16, 0.24):
        print('  %s  fraction of tile with R-B > %.2f : %5.2f%%' % (name, t, 100*((ch>t)&ins).sum()/ins.sum()))
