import math, numpy as np
from PIL import Image
NEUTRAL = 128/255.0
def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64)/255.0
    rgb, al = a[...,:3], a[...,3:4]
    rgb = rgb*al + NEUTRAL*(1-al)
    g = 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2]
    return rgb, g
crgb, gc = load('loop-runs/r07/candidate-1024.png')
rrgb, gr = load('loop-runs/r07/reference-1024.png')
d = np.abs(gc-gr)
H,W = gc.shape
Y,X = np.mgrid[0:H,0:W]
ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang)*(X-543))
f_ref  = Y - (-0.8026*X + 991.2)
blk_c, blk_r = gc<0.45, gr<0.45
alp = np.asarray(Image.open('loop-runs/r07/candidate-1024.png').convert('RGBA'))[...,3]>250
print('lum_delta whole %.4f  (signed mean %.4f)'%(d.mean(), (gc-gr).mean()))
regions = [
 ('both-block', blk_c & blk_r),
 ('ours-block-only', blk_c & ~blk_r),
 ('ref-block-only', ~blk_c & blk_r),
 ('ground-trued', (~blk_c)&(~blk_r)&(f_ours>0)),
 ('ground-rough', (~blk_c)&(~blk_r)&(f_ours<=0)),
 ('outside-tile', ~alp),
]
print('%-18s %6s %8s %8s %7s %7s %8s'%('region','frac','mean|d|','contrib','ourL','refL','signed'))
for k,m in regions:
    if m.sum()==0: continue
    print('%-18s %6.3f %8.4f %8.4f %7.3f %7.3f %+8.4f'%(m.mean(), 0,0,0,0,0) if False else
          '%-18s %6.3f %8.4f %8.4f %7.3f %7.3f %+8.4f'%(k,m.mean(),d[m].mean(),d[m].sum()/d.size,gc[m].mean(),gr[m].mean(),(gc-gr)[m].mean()))
# quadrant breakdown of the ROUGH ground only, 4x4 tiles of the whole tile
print('\n4x4 tile of |d| (contribution share %) / signed')
for iy in range(4):
    row=[]
    for ix in range(4):
        m = (Y>=iy*256)&(Y<(iy+1)*256)&(X>=ix*256)&(X<(ix+1)*256)
        row.append('%5.1f%%/%+.3f'%(100*d[m].sum()/d.sum(), (gc-gr)[m].mean()))
    print('  '.join(row))
