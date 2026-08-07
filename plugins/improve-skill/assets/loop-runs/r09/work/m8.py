"""Who supplies p90 and p10 at 32 and 16px, split by distance from the block?

Round 9's trace said "98% trued ground", which is true and not fine-grained enough to
decide whether the near-block bloom band -- our trued ground reads L 0.868-0.873 at
90-190px from the foot against 0.795 in the far field, i.e. the bloom band is BRIGHTER
than the far field -- is itself supplying the percentile the contrast floor reads.
"""
import math, sys, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F

cand = Image.open('loop-runs/r08/candidate-1024.png').convert('RGBA')
H = 1024
Y, X = np.mgrid[0:H, 0:H]
ang = math.radians(33.0)
fline = Y - (604 - math.tan(ang)*(X-543))
blk = np.load('loop-runs/r09/work/blk_c.npy')
dist = np.load('loop-runs/r09/work/dist_c.npy')
CURL = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
al = np.asarray(cand)[...,3]/255.0 > 0.98
REG = {
  'block':        blk,
  'curl':         CURL & ~blk & al,
  'rough':        al & ~blk & ~CURL & (fline<=0),
  'trued d<40':   al & ~blk & ~CURL & (fline>0) & (dist<40),
  'trued 40-130': al & ~blk & ~CURL & (fline>0) & (dist>=40) & (dist<130),
  'trued 130-260':al & ~blk & ~CURL & (fline>0) & (dist>=130) & (dist<260),
  'trued >260':   al & ~blk & ~CURL & (fline>0) & (dist>=260),
  'outside':      ~al,
}
for size in (32, 16):
    ci = F.render_candidate(pathlib.Path('icon.svg'), size)
    g = F.to_gray(ci)
    p90, p10 = np.percentile(g, 90), np.percentile(g, 10)
    hi, lo = g >= p90, g <= p10
    # majority region of each 1024/size block
    k = H//size
    print('\n=== %dpx ===  p90 %.3f  p10 %.3f  spread %.4f' % (size, p90, p10, p90-p10))
    shares_hi, shares_lo = {}, {}
    lab = np.zeros((size, size), dtype=object)
    names = list(REG)
    frac = np.stack([REG[n].reshape(size, k, size, k).mean(axis=(1,3)) for n in names])
    top = frac.argmax(axis=0)
    for i, n in enumerate(names):
        sel = top == i
        shares_hi[n] = (sel & hi).sum()/max(hi.sum(),1)
        shares_lo[n] = (sel & lo).sum()/max(lo.sum(),1)
    print('  %-16s %8s %8s' % ('region', 'p90 own', 'p10 own'))
    for n in names:
        if shares_hi[n] or shares_lo[n]:
            print('  %-16s %7.1f%% %7.1f%%' % (n, 100*shares_hi[n], 100*shares_lo[n]))
    # how much headroom: what p90 becomes if the 40-130 bloom band is darkened by 8%
    i = names.index('trued 40-130')
    band = (top == i)
    for cut in (0.04, 0.08, 0.14):
        g2 = np.where(band, g*(1-cut), g)
        print('    darken the 40-130 band by %2.0f%%  ->  spread %.4f (floor %.4f)' % (
            100*cut, np.percentile(g2,90)-np.percentile(g2,10), {32:0.5864, 16:0.5719}[size]))
