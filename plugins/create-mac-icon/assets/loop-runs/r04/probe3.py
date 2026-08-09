#!/usr/bin/env python3
"""r04 probe 3: rank the residual by region so the round targets a measured gap."""
import numpy as np
from PIL import Image

BASE = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/"


def load(p):
    return np.asarray(Image.open(BASE + p).convert("RGB")).astype(np.float64) / 255.0


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


ref, cand = load("reference-1024.png"), load("candidate-1024.png")
Lr, Lc = lum(ref), lum(cand)
diff = np.abs(Lr - Lc)

N = 8
cell = 1024 // N
rows = []
for j in range(N):
    for i in range(N):
        blk = diff[j * cell:(j + 1) * cell, i * cell:(i + 1) * cell]
        rows.append((blk.mean(), i, j))
rows.sort(reverse=True)
print("== worst 16 cells of an 8x8 grid (mean |dL|) ==")
for m, i, j in rows[:16]:
    print(f"  cell ({i},{j})  x {i*cell}..{(i+1)*cell}  y {j*cell}..{(j+1)*cell}  mean|dL| {m:.4f}")

print()
print("== row and column profiles of mean |dL| (32px bands) ==")
for j in range(0, 1024, 32):
    band = diff[j:j + 32, :]
    print(f"  y {j:4d}..{j+31:4d}  {band.mean():.4f}  " + "#" * int(band.mean() * 200))

print()
for i in range(0, 1024, 32):
    band = diff[:, i:i + 32]
    print(f"  x {i:4d}..{i+31:4d}  {band.mean():.4f}  " + "#" * int(band.mean() * 200))
