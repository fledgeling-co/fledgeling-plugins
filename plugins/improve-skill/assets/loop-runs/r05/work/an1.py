import numpy as np
from PIL import Image
R='loop-runs/r04/'
def L(p):
    a=np.asarray(Image.open(p).convert('RGB'),dtype=np.float64)/255.0
    return a, 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
ca,cl=L(R+'candidate-1024.png'); ra,rl=L(R+'reference-1024.png')
res=np.abs(cl-rl)
# 8x8 block grid of residual
N=8; s=1024//N
print("residual mean, 8x8 grid (rows top->bottom):")
for i in range(N):
    print(' '.join(f"{res[i*s:(i+1)*s, j*s:(j+1)*s].mean():.3f}" for j in range(N)))
print()
print("cand L 8x8:")
for i in range(N):
    print(' '.join(f"{cl[i*s:(i+1)*s, j*s:(j+1)*s].mean():.3f}" for j in range(N)))
print()
print("ref L 8x8:")
for i in range(N):
    print(' '.join(f"{rl[i*s:(i+1)*s, j*s:(j+1)*s].mean():.3f}" for j in range(N)))
