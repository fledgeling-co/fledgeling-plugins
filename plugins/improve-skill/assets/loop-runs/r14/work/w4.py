import numpy as np
from PIL import Image

R = "loop-runs/r13/"
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGB")).astype(np.float32) / 255.
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB")).astype(np.float32) / 255.


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


Lc, Lr = lum(cand), lum(ref)
Y, X = np.mgrid[0:1024, 0:1024].astype(np.float32)


def scan(L, name, xlim=340, ylo=380):
    reg = (X < xlim) & (Y > ylo) & (L > 0.02)
    ys, xs = np.nonzero(reg)
    v = L[reg]
    best = None
    for deg in np.arange(10.0, 60.0, 0.5):
        t = np.radians(deg)
        s = ys * np.cos(t) + xs * np.sin(t)
        lo, hi = s.min(), s.max()
        for off in np.arange(lo + 40, hi - 40, 2.0):
            d = s - off
            a = (d < -6) & (d > -40)
            b = (d > 6) & (d < 40)
            if a.sum() < 800 or b.sum() < 800:
                continue
            step = v[b].mean() - v[a].mean()
            if best is None or step > best[0]:
                best = (step, deg, off)
    step, deg, off = best
    print(f"{name}: cut inclination {deg:.1f} deg, offset {off:.1f}, step {step:+.4f}")
    return deg, off, reg


def profile(L, deg, off, reg, half=16):
    t = np.radians(deg)
    ys, xs = np.nonzero(reg)
    s = ys * np.cos(t) + xs * np.sin(t) - off
    v = L[reg]
    out = []
    for d in range(-half, half + 1):
        m = (s >= d - 0.5) & (s < d + 0.5)
        out.append(v[m].mean() if m.sum() > 30 else np.nan)
    return np.array(out)


dc, oc, rgc = scan(Lc, "candidate")
dr, orf, rgr = scan(Lr, "reference")
pc = profile(Lc, dc, oc, rgc)
pr = profile(Lr, dr, orf, rgr)
print("\nmean luminance vs signed distance from the cut (neg = un-planed side)")
print("   d   cand     ref")
for i, d in enumerate(range(-16, 17)):
    print(f"{d:+4d}  {pc[i]:.4f}  {pr[i]:.4f}")
for nm, p in (("cand", pc), ("ref", pr)):
    up, dn = np.nanmean(p[:6]), np.nanmean(p[-6:])
    print(f"{nm}: un-planed plateau {up:.4f}  trued plateau {dn:.4f}  step {dn-up:+.4f}  "
          f"max {np.nanmax(p):.4f} @ d={np.nanargmax(p)-16}  min {np.nanmin(p):.4f} @ d={np.nanargmin(p)-16}")
np.save("loop-runs/r14/work/cutfit.npy", np.array([dc, oc, dr, orf]))
