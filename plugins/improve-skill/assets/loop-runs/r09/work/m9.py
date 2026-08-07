"""Did the edit land on the profile it was designed for?

The target was fixed by measurement before the edit: trued-ground R-B within ~0.02 of its
far-field 0.086 by 45-60px from the block's foot, with the seam (0-14px) untouched. The
block geometry did not change this round, so blk_c/dist_c carry over unchanged.
"""
import math, sys, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F
NEUTRAL = 128/255.0
def load(im):
    a = np.asarray(im.convert('RGBA')).astype(np.float64)/255.0
    rgb, al = a[..., :3], a[..., 3:4]
    return rgb*al + NEUTRAL*(1-al), a[..., 3]
new, an = load(F.render_candidate(pathlib.Path('icon.svg'), 1024))
old, ao = load(Image.open('loop-runs/r08/candidate-1024.png'))
ref, ar = load(Image.open('loop-runs/r08/reference-1024.png'))
H = 1024
Y, X = np.mgrid[0:H, 0:H]
fl = Y - (604 - math.tan(math.radians(33.0))*(X-543))
blk = np.load('loop-runs/r09/work/blk_c.npy'); dist = np.load('loop-runs/r09/work/dist_c.npy')
CURL = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
BANDS = [(0,6),(6,14),(14,25),(25,40),(40,60),(60,90),(90,130),(130,190),(190,280),(280,9e9)]
print('%-12s' % 'R-B band' + ' '.join('%7s' % ('%d-%d'%(a,b) if b<9e8 else '>280') for a,b in BANDS))
for nm, rgb, al in (('was', old, ao), ('now', new, an)):
    m0 = (al>0.98) & ~blk & ~CURL & (fl>0)
    ch = rgb[...,0]-rgb[...,2]
    print('%-12s' % nm + ' '.join('%7.3f' % ch[m0&(dist>=lo)&(dist<hi)].mean() for lo,hi in BANDS))
print('%-12s' % 'C2 (flat)' + ' '.join('%7.3f' % v for v in
      [0.058,0.056,0.055,0.058,0.063,0.069,0.075,0.080,0.082,0.080]))
print()
for nm, rgb, al in (('was', old, ao), ('now', new, an), ('C2 ', ref, ar)):
    ch = rgb[...,0]-rgb[...,2]; ins = al>0.98
    print('  %s  tile fraction R-B>0.16 %5.2f%%   >0.24 %5.2f%%' % (
        nm, 100*((ch>0.16)&ins).mean()/ins.mean(), 100*((ch>0.24)&ins).mean()/ins.mean()))
print()
for size in (32, 16):
    for nm, src in (('was', 'loop-runs/r08/candidate-%d.png' % size), ('now', None)):
        im = F.render_candidate(pathlib.Path('icon.svg'), size) if src is None else Image.open(src)
        c = np.asarray(im.convert('RGBA')).astype(np.float64)/255.0
        v = (((c[...,0]-c[...,2]) > 0.20) & (c[...,3] > 0.5)).mean()
        print('  %dpx vermilion footprint %s: %.2f%% of tile' % (size, nm, 100*v))
