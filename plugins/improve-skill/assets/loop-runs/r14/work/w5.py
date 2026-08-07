import numpy as np
from PIL import Image

R = "loop-runs/r13/"
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGB")).astype(np.float32) / 255.
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB")).astype(np.float32) / 255.


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def box(a, k):
    p = k // 2
    b = np.pad(a, ((p, p), (0, 0)), mode="edge")
    c = np.concatenate([np.zeros((1, b.shape[1]), np.float32), np.cumsum(b, axis=0)], 0)
    a1 = (c[k:, :] - c[:-k, :]) / k
    b = np.pad(a1, ((0, 0), (p, p)), mode="edge")
    c = np.concatenate([np.zeros((b.shape[0], 1), np.float32), np.cumsum(b, axis=1)], 1)
    return (c[:, k:] - c[:, :-k]) / k


Lc, Lr = lum(cand), lum(ref)
# 3-13px band-pass, the loop's own relief band
hp_c = box(Lc, 3) - box(Lc, 13)
hp_r = box(Lr, 3) - box(Lr, 13)
Y, X = np.mgrid[0:1024, 0:1024]

# the block occupies roughly this; exclude it and the curl and the tile margin
block = (Lc < 0.30) & (X > 120) & (X < 940) & (Y > 250) & (Y < 720)
curl = (X > 90) & (X < 400) & (Y > 20) & (Y < 340)
valid = (Lc > 0.02) & ~block & ~curl & (X > 40) & (X < 984) & (Y > 40) & (Y < 984)

print("3-13px high-pass rms, by 128px cell.  cand / ref  (ratio)")
print("        " + "".join(f"{c*128:>16d}" for c in range(8)))
for r in range(8):
    row = f"{r*128:5d}  "
    for c in range(8):
        m = np.zeros_like(valid)
        m[r * 128:(r + 1) * 128, c * 128:(c + 1) * 128] = True
        m &= valid
        if m.sum() < 900:
            row += f"{'--':>16}"
            continue
        a, b = hp_c[m].std(), hp_r[m].std()
        row += f"{a:.4f}/{b:.4f}({a/b:4.1f})".rjust(16)
    print(row)

# whole-plane split about the candidate's own cut (34 deg, off 791.9)
t = np.radians(34.0)
s = Y * np.cos(t) + X * np.sin(t) - 791.9
for nm, m in (("un-planed", valid & (s < -20)), ("trued", valid & (s > 20))):
    print(f"\n{nm}: n={m.sum()}  cand hp rms {hp_c[m].std():.4f}   ref hp rms {hp_r[m].std():.4f}   ratio {hp_c[m].std()/hp_r[m].std():.2f}")
    for nm2, hp in (("cand", hp_c), ("ref", hp_r)):
        th = np.abs(hp[m]) > 1.1 * hp[m].std()
        print(f"   {nm2}: coverage above 1.1 sigma {100*th.mean():.1f}%   p99 |hp| {np.percentile(np.abs(hp[m]),99):.4f}")
