import numpy as np, math
from PIL import Image
def load(p): return np.asarray(Image.open(p).convert('RGB'),dtype=float)
def rep(name,path):
    I=load(path); ys,xs=np.mgrid[0:1024,0:1024]; rr=np.hypot(xs-512,ys-512)
    Lm=(0.2126*I[...,0]+0.7152*I[...,1]+0.0722*I[...,2])/255
    band=(rr>150)&(rr<400)
    blue=band&(I[...,2]>I[...,0]+8)
    warm=(I[...,0]>140)&(I[...,0]>I[...,2]+55)
    gr=(rr>430)
    print(f"--- {name}")
    for lbl,m in (('ring',blue),('ember',warm)):
        if m.sum()<500: print(f"  {lbl}: n={m.sum()}"); continue
        L=Lm[m]; px=I[m]
        print(f"  {lbl}: n={m.sum():6d} meanRGB={px.mean(0).round(0)} L p5={np.percentile(L,5):.3f} p50={np.percentile(L,50):.3f} p95={np.percentile(L,95):.3f} spread={np.percentile(L,95)-np.percentile(L,5):.3f} min={L.min():.3f} max={L.max():.3f}")
        d=px[L.argmin()]; b=px[L.argmax()]
        print(f"        darkest={tuple(int(v) for v in d)} sat={(max(d)-min(d))/max(max(d),1):.2f} | brightest={tuple(int(v) for v in b)}")
    gl=Lm[gr].mean()
    ringL=np.percentile(Lm[blue],50)
    print(f"  ground L={gl:.3f}  figure-ground (ring median) = {(gl+0.05)/(ringL+0.05):.2f}:1")
for n,p in (('MASTER','icon.png'),('REF C','icon-engineC-clean.png')): rep(n,p)
