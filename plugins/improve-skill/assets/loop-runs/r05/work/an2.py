import numpy as np
from PIL import Image
R='loop-runs/r04/'
def lum(p):
    a=np.asarray(Image.open(p).convert('RGB'),dtype=np.float64)/255.0
    return a, 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
ra,rl=lum(R+'reference-1024.png')
# find the split: for each column, the y of max |d/dy| of a column-smoothed profile,
# searching only where the block isn't (block is dark, L<0.45)
def smooth(v,k=9):
    ker=np.ones(k)/k
    return np.convolve(v,ker,mode='same')
pts=[]
for x in range(20,1004,8):
    col=smooth(rl[:,x],15)
    d=np.diff(col)
    # restrict to y range that is ground: exclude rows where col<0.42 (block)
    best=None
    for y in range(40,980):
        if col[y]<0.42 or col[y+1]<0.42: continue
        if best is None or d[y]>d[best]: best=y
    if best is not None and d[best]>0.002:
        pts.append((x,best,d[best]))
pts=np.array(pts)
# keep the strongest half
thr=np.percentile(pts[:,2],55)
sel=pts[pts[:,2]>=thr]
A=np.polyfit(sel[:,0],sel[:,1],1)
import math
print("split fit: y = %.5f x + %.2f   angle=%.2f deg  n=%d"%(A[0],A[1],math.degrees(math.atan2(-A[0],1)),len(sel)))
res=sel[:,1]-(A[0]*sel[:,0]+A[1])
print("residual std %.2f px, max %.1f"%(res.std(),np.abs(res).max()))
print("x=0 -> y=%.1f ; x=1024 -> y=%.1f"%(A[1],A[0]*1024+A[1]))
np.save('loop-runs/r05/work/refsplit.npy',A)
