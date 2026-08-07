import subprocess, tempfile, pathlib, sys
import numpy as np
from PIL import Image
NEUTRAL=128
def rend(p,s):
    p=pathlib.Path(p)
    if p.suffix.lower()=='.svg':
        t=pathlib.Path(tempfile.mktemp(suffix='.png'))
        subprocess.run(['rsvg-convert','-w',str(s),'-h',str(s),str(p),'-o',str(t)],check=True)
        im=Image.open(t).convert('RGBA'); t.unlink()
        return im
    return Image.open(p).convert('RGBA').resize((s,s),Image.LANCZOS)
def refim(p,s):
    im=Image.open(p).convert('RGBA')
    return im.resize((s,s),Image.LANCZOS)
def comp(im):
    a=np.asarray(im,dtype=np.float64)/255.
    rgb,al=a[...,:3],a[...,3:4]
    return rgb*al+(NEUTRAL/255.)*(1-al)
cand=sys.argv[1] if len(sys.argv)>1 else 'icon.svg'
out=sys.argv[2] if len(sys.argv)>2 else 'loop-runs/r03/small.png'
ref='icon-engineC-f5665d-2.png'
sizes=[32,16]
CELL=384
rows=[]
for s in sizes:
    c=comp(rend(cand,s)); r=comp(refim(ref,s))
    row=[]
    for img in (c,r):
        big=Image.fromarray((np.clip(img,0,1)*255).astype(np.uint8)).resize((CELL,CELL),Image.NEAREST)
        row.append(np.asarray(big))
    rows.append(np.concatenate(row,axis=1))
sheet=np.concatenate(rows,axis=0)
Image.fromarray(sheet).save(out)
print('wrote',out)
