import numpy as np, math
from PIL import Image
def lum(p):
    a=np.asarray(Image.open(p).convert('RGB'),dtype=np.float64)/255.0
    return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
rl=lum('loop-runs/r04/reference-1024.png')
def sm(v,k):
    return np.convolve(v,np.ones(k)/k,mode='same')
pts=[]
# bottom-left run and right run, search a +-90px window around a rough guess line
def guess(x): return 1024 + (165-1024)*(x-60)/(1024-60)
for x in list(range(70,340,6))+list(range(760,1015,6)):
    g=guess(x); lo=int(max(6,g-90)); hi=int(min(1017,g+90))
    if hi-lo<40: continue
    col=sm(rl[:,x],9); d=np.diff(col)
    j=lo+int(np.argmax(d[lo:hi]))
    pts.append((x,j,d[j]))
pts=np.array(pts,dtype=float)
keep=pts[pts[:,2]>np.percentile(pts[:,2],25)]
A=np.polyfit(keep[:,0],keep[:,1],1)
res=keep[:,1]-(A[0]*keep[:,0]+A[1])
print("REF split: y=%.5f x + %.2f  angle=%.2f deg  n=%d  res std %.2f max %.1f"%(
    A[0],A[1],math.degrees(math.atan2(-A[0],1)),len(keep),res.std(),abs(res).max()))
print("  y(0)=%.1f  y(1024)=%.1f"%(A[1],A[0]*1024+A[1]))
np.save('loop-runs/r05/work/refsplit.npy',A)
