import numpy as np
from PIL import Image
R='loop-runs/r04/'
def lum(p):
    a=np.asarray(Image.open(p).convert('RGB'),dtype=np.float64)/255.0
    return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
rl=lum(R+'reference-1024.png'); cl=lum(R+'candidate-1024.png')
for name,L in (('REF',rl),('CAND',cl)):
    print('===',name)
    for x in (40,120,200,860,940,1000):
        col=L[:,x]
        s=np.convolve(col,np.ones(11)/11,mode='same')
        d=np.diff(s)
        j=int(np.argmax(d[40:990]))+40
        print(f"  x={x:4d} steepest rise at y={j:4d} (d={d[j]:+.4f})  L above={s[max(0,j-40)]:.3f} below={s[min(1023,j+40)]:.3f}")
