import subprocess, tempfile, pathlib, sys
import numpy as np
from PIL import Image
NEUTRAL=128
def rend(p,s):
    p=pathlib.Path(p)
    if p.suffix.lower()=='.svg':
        t=pathlib.Path(tempfile.mktemp(suffix='.png'))
        subprocess.run(['rsvg-convert','-w',str(s),'-h',str(s),str(p),'-o',str(t)],check=True)
        im=Image.open(t).convert('RGBA'); t.unlink(); return im
    return Image.open(p).convert('RGBA').resize((s,s),Image.LANCZOS)
def refim(p,s):
    return Image.open(p).convert('RGBA').resize((s,s),Image.LANCZOS)
def gray(im):
    a=np.asarray(im,dtype=np.float64)/255.
    rgb,al=a[...,:3],a[...,3:4]
    c=rgb*al+(NEUTRAL/255.)*(1-al)
    return 0.2126*c[...,0]+0.7152*c[...,1]+0.0722*c[...,2]
cand=sys.argv[1] if len(sys.argv)>1 else 'icon.svg'
ref='icon-engineC-f5665d-2.png'
for s in (32,16):
    gc=gray(rend(cand,s)); gr=gray(refim(ref,s))
    d=np.abs(gc-gr)
    print(f"== {s}px  meanΔ {d.mean():.4f}")
    # top-10 worst pixels
    idx=np.dstack(np.unravel_index(np.argsort(d.ravel())[::-1][:12], d.shape))[0]
    print("  worst px (y,x, cand, ref, d):", ", ".join(f"({y},{x},{gc[y,x]:.2f},{gr[y,x]:.2f},{d[y,x]:.2f})" for y,x in idx[:8]))
    # region means: quadrant grid 4x4
    q=s//4
    print("  4x4 grid |cand-ref| :")
    for r in range(4):
        print("   ", " ".join(f"{d[r*q:(r+1)*q, c*q:(c+1)*q].mean():.3f}" for c in range(4)))
