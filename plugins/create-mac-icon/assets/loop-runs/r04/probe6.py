#!/usr/bin/env python3
"""r04 probe 6: where the composite's biggest weight (SSIM, 0.40 at >=128) is
actually losing. Reproduces fidelity.py's ssim map exactly and ranks regions,
with the squircle rim excluded so the delivery-format boundary does not dominate.
"""
import numpy as np
from PIL import Image

BASE = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/loop-runs/r03/"
NEUTRAL = 128


def to_gray(im):
    a = np.asarray(im.convert("RGBA"), dtype=np.float64) / 255.0
    rgb, alpha = a[..., :3], a[..., 3:4]
    comp = rgb * alpha + (NEUTRAL / 255.0) * (1 - alpha)
    return 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2]


def box_mean(x, w):
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[: x.shape[0], : x.shape[1]]


def ssim_map(a, b):
    w = max(3, min(11, a.shape[0] // 4) | 1)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    mu_a, mu_b = box_mean(a, w), box_mean(b, w)
    va = box_mean(a * a, w) - mu_a ** 2
    vb = box_mean(b * b, w) - mu_b ** 2
    cov = box_mean(a * b, w) - mu_a * mu_b
    s = ((2 * mu_a * mu_b + c1) * (2 * cov + c2)) / ((mu_a ** 2 + mu_b ** 2 + c1) * (va + vb + c2))
    return np.clip(s, -1, 1)


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


gc = to_gray(Image.open(BASE + "candidate-1024.png"))
gr = to_gray(Image.open(BASE + "reference-1024.png"))
S = ssim_map(gc, gr)
keep = ~rim_mask(1024)
print(f"global ssim {S.mean():.4f}   ssim inside the squircle only {S[keep].mean():.4f}")

N = 8
cell = 1024 // N
rows = []
for j in range(N):
    for i in range(N):
        sl = (slice(j * cell, (j + 1) * cell), slice(i * cell, (i + 1) * cell))
        k = keep[sl]
        if k.sum() < 200:
            continue
        rows.append((S[sl][k].mean(), i, j, k.sum()))
rows.sort()
print("\n== worst 14 cells by local SSIM (rim excluded) ==")
for m, i, j, n in rows[:14]:
    print(f"  cell ({i},{j})  x {i*cell}..{(i+1)*cell}  y {j*cell}..{(j+1)*cell}"
          f"  ssim {m:.4f}   n={n}")
print("\n== best 6, for scale ==")
for m, i, j, n in rows[-6:]:
    print(f"  cell ({i},{j})  x {i*cell}..{(i+1)*cell}  y {j*cell}..{(j+1)*cell}  ssim {m:.4f}")

# Which term is hurting: variance mismatch or covariance?
w = 11
mu_a, mu_b = box_mean(gc, w), box_mean(gr, w)
va = np.sqrt(np.maximum(box_mean(gc * gc, w) - mu_a ** 2, 0))
vb = np.sqrt(np.maximum(box_mean(gr * gr, w) - mu_b ** 2, 0))
print(f"\nlocal contrast (sd) inside squircle: candidate {va[keep].mean():.4f}  "
      f"reference {vb[keep].mean():.4f}")
for j in range(0, 1024, 128):
    k = keep[j:j + 128, :]
    print(f"  y {j:4d}..{j+127:4d}  sd cand {va[j:j+128,:][k].mean():.4f}  "
          f"ref {vb[j:j+128,:][k].mean():.4f}")
