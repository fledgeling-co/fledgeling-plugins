import math, numpy as np
from PIL import Image
NEUTRAL = 128/255.0
def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64)/255.0
    rgb, al = a[...,:3], a[...,3:4]
    rgb = rgb*al + NEUTRAL*(1-al)
    return rgb, 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2]
crgb, gc = load('loop-runs/r07/candidate-1024.png')
rrgb, gr = load('loop-runs/r07/reference-1024.png')
H,W = gc.shape; Y,X = np.mgrid[0:H,0:W]
ang = math.radians(33.0)
f_o = Y - (604 - math.tan(ang)*(X-543))
f_r = Y - (-0.8026*X + 991.2)
blk_c, blk_r = gc<0.45, gr<0.45
def dilate(m,r):
    out=m.copy()
    for dy in range(-r,r+1,max(1,r//6)):
        for dx in range(-r,r+1,max(1,r//6)):
            out |= np.roll(np.roll(m,dy,0),dx,1)
    return out
bc,br = dilate(blk_c,45), dilate(blk_r,45)
alp = np.asarray(Image.open('loop-runs/r07/candidate-1024.png').convert('RGBA'))[...,3]>250
inner = alp & (X>28)&(X<996)&(Y>28)&(Y<996)
u = (X+Y)/math.sqrt(2.0)
print('mean L along key axis u=(x+y)/sqrt2, ground only, blocks dilated out')
print('%6s | %7s %7s %6s | %7s %7s %6s'%('u','o_rough','r_rough','ratio','o_trued','r_trued','ratio'))
for u0 in range(0,1460,80):
    m = (u>=u0)&(u<u0+80)
    row=[u0]
    for fo,fr,lab in ((f_o<-40,f_r<-40,'rough'),(f_o>40,f_r>40,'trued')):
        mo = m & inner & fo & (~bc); mr = m & inner & fr & (~br)
        a = gc[mo].mean() if mo.sum()>300 else float('nan')
        b = gr[mr].mean() if mr.sum()>300 else float('nan')
        row += [a,b,a/b if b==b and a==a else float('nan')]
    print('%6d | %7.3f %7.3f %6.3f | %7.3f %7.3f %6.3f'%tuple(row))
