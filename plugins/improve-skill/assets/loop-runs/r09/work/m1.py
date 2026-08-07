"""Region breakdown of the r08 residual, with the curl broken out as its own region."""
import math, numpy as np
from PIL import Image
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
d = np.abs(gc-gr)
H,W = gc.shape
Y,X = np.mgrid[0:H,0:W]
ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang)*(X-543))
blk_c, blk_r = gc<0.45, gr<0.45
alp = ac>0.98
# curl: ours near (308,278) r~115 sweep 93; ref bbox measured in r08/work/m8.py
CURL_C = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
regions = [
 ('curl-box',       CURL_C & (~blk_c) & (~blk_r) & alp),
 ('both-block',     blk_c & blk_r & ~CURL_C),
 ('ours-block-only', blk_c & ~blk_r & ~CURL_C),
 ('ref-block-only', ~blk_c & blk_r & ~CURL_C),
 ('ground-trued',   (~blk_c)&(~blk_r)&(f_ours>0)&(~CURL_C)&alp),
 ('ground-rough',   (~blk_c)&(~blk_r)&(f_ours<=0)&(~CURL_C)&alp),
 ('outside-tile',   ~alp),
]
print('lum_delta whole %.4f  (signed mean %+.4f)'%(d.mean(), (gc-gr).mean()))
print('%-18s %6s %8s %8s %6s %7s %7s %8s'%('region','frac','mean|d|','contrib','share','ourL','refL','signed'))
for k,m in regions:
    if m.sum()==0: continue
    print('%-18s %6.3f %8.4f %8.4f %5.1f%% %7.3f %7.3f %+8.4f'%(
        k,m.mean(),d[m].mean(),d[m].sum()/d.size,100*d[m].sum()/d.sum(),gc[m].mean(),gr[m].mean(),(gc-gr)[m].mean()))
