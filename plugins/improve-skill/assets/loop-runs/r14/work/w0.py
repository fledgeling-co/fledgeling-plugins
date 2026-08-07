import numpy as np
from PIL import Image

R = "loop-runs/r13/"
res = np.asarray(Image.open(R + "residual-1024.png").convert("L")).astype(np.float32) / 255.
print("residual shape", res.shape, "mean", res.mean().round(4), "p90", np.percentile(res, 90).round(4))
h, w = res.shape
bs = h // 16
grid = res[:bs * 16, :bs * 16].reshape(16, bs, 16, bs).mean(axis=(1, 3))
print("\nblock-mean residual grid (64px blocks), values *100:")
print("     " + " ".join(f"{c*bs:4d}" for c in range(16)))
for r in range(16):
    print(f"{r*bs:4d} " + " ".join(f"{v*100:4.0f}" for v in grid[r]))
order = np.dstack(np.unravel_index(np.argsort(-grid, axis=None), grid.shape))[0]
print("\nworst 14 blocks (y0,x0,mean*100):")
for r, c in order[:14]:
    print(f"  y {r*bs:4d}-{(r+1)*bs:4d}  x {c*bs:4d}-{(c+1)*bs:4d}   {grid[r,c]*100:.1f}")
