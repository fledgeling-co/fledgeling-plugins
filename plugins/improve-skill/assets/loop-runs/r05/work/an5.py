import numpy as np, math
from PIL import Image
W=1024
def rgb(p): return np.asarray(Image.open(p).convert('RGB'),dtype=np.float64)/255.0
def lin(c): return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
def Lstar(a):
    y=0.2126*lin(a[...,0])+0.7152*lin(a[...,1])+0.0722*lin(a[...,2])
    return np.where(y>0.008856,(116*np.cbrt(y)-16)/100,903.3*y/100)
ra=rgb('loop-runs/r04/reference-1024.png'); ca=rgb('loop-runs/r04/candidate-1024.png')
RL=Lstar(ra); CL=Lstar(ca)
Y,X=np.mgrid[0:W,0:W]

def frame(angle_deg, y_at_0):
    a=math.radians(angle_deg)
    ux,uy=math.cos(a),-math.sin(a)      # along the split, up-right
    nx,ny=-math.sin(a),-math.cos(a)     # normal, into the un-planed side (up-left)
    ax,ay=0.0,y_at_0
    u=ux*(X-ax)+uy*(Y-ay)
    v=nx*(X-ax)+ny*(Y-ay)
    return u,v

# reference frame from the fit
RU,RV=frame(39.59,1007.85)
# candidate frame: ANGLE 33, boundary_at_x(0)
import subprocess
ANG=33.0
# build_icon: AX,AY origin at cutting-edge leading end; boundary is local y=0 line.
UX,UY=math.cos(math.radians(ANG)),-math.sin(math.radians(ANG))
NX,NY=-math.sin(math.radians(ANG)),-math.cos(math.radians(ANG))
EDGE_MID=(543.0,604.0); BLADE_LEN=640.0
AX=EDGE_MID[0]-UX*BLADE_LEN/2; AY=EDGE_MID[1]-UY*BLADE_LEN/2
B_LEFT=AY-NX*(0-AX)/NY
print("cand B_LEFT=%.1f B_RIGHT=%.1f"%(B_LEFT, AY-NX*(W-AX)/NY))
CU,CV=frame(ANG,B_LEFT)

# object exclusion boxes (block+curl), generous
def box(x0,y0,x1,y1): return (X>=x0)&(X<=x1)&(Y>=y0)&(Y<=y1)
ref_obj = box(100,30,830,700)
cand_obj= box(120,60,830,800)

def report(name,L,U,V,obj):
    ground=(~obj)&(np.abs(V)>60)
    print("===",name)
    # bands in v, and quartiles along u
    for lo,hi,side in ((60,200,'un-planed near'),(200,400,'un-planed mid'),(400,900,'un-planed far'),
                       (-200,-60,'trued near'),(-400,-200,'trued mid'),(-900,-400,'trued far')):
        m=ground&(V>=min(lo,hi))&(V<max(lo,hi))
        if m.sum()<500: print(f"  {side:16s} n<500"); continue
        # split along u into 3
        us=U[m]; ls=L[m]
        qs=np.percentile(us,[0,33,66,100])
        parts=[]
        for i in range(3):
            mm=(us>=qs[i])&(us<=qs[i+1])
            parts.append(ls[mm].mean())
        print(f"  {side:16s} mean {ls.mean():.3f}   along-split (down-left->up-right): {parts[0]:.3f} {parts[1]:.3f} {parts[2]:.3f}   n={m.sum()}")
    # measure.py-style global polarity, ground only L>0.50
    gr=L[(V>60)&(L>0.50)]; gt=L[(V<-60)&(L>0.50)]
    print(f"  POLARITY (measure.py style, no obj box): un-planed {gr.mean():.3f} trued {gt.mean():.3f} delta {gt.mean()-gr.mean():+.3f}")
report('REFERENCE',RL,RU,RV,ref_obj)
report('CANDIDATE',CL,CU,CV,cand_obj)
