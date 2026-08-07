import numpy as np
from PIL import Image

R = "loop-runs/r13/"
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGB")).astype(np.float32) / 255.
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB")).astype(np.float32) / 255.


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def blur(a, k):
    # separable box blur, k odd
    p = k // 2
    b = np.pad(a, p, mode="edge")
    c = np.cumsum(b, axis=0)
    a1 = (c[k:, :] - c[:-k, :]) / k
    c = np.cumsum(np.pad(a1, ((0, 0), (p, p)), mode="edge"), axis=1)
    return (c[:, k:] - c[:, :-k]) / k


def find_cut(L, xs, ylo, yhi):
    """for each column, y of steepest downward-in-y darkening (un-planed above -> trued below
    is a step in either direction); return (slope, intercept) least squares."""
    Ls = blur(L, 5)
    gy = Ls[1:, :] - Ls[:-1, :]
    pts = []
    for x in xs:
        col = gy[ylo:yhi, x]
        i = int(np.argmax(np.abs(col)))
        pts.append((x, ylo + i + 0.5, col[i]))
    P = np.array(pts)
    A = np.vstack([P[:, 0], np.ones(len(P))]).T
    m, b = np.linalg.lstsq(A, P[:, 1], rcond=None)[0]
    resid = P[:, 1] - (m * P[:, 0] + b)
    return m, b, np.abs(resid).mean(), P[:, 2].mean()


Lc, Lr = lum(cand), lum(ref)
# candidate: cut known analytically -> 33 deg rising to the right; sample left half only
# (right half is occluded by the block). same window for the reference.
xs = list(range(20, 300, 6))
mc, bc, rc, sc = find_cut(Lc, xs, 500, 1000)
mr, br, rr, sr = find_cut(Lr, xs, 500, 1000)
print(f"candidate cut: y = {mc:.4f} x + {bc:.1f}   angle {np.degrees(np.arctan(-mc)):.1f} deg  fitresid {rc:.2f}  step {sc:+.4f}")
print(f"reference cut: y = {mr:.4f} x + {br:.1f}   angle {np.degrees(np.arctan(-mr)):.1f} deg  fitresid {rr:.2f}  step {sr:+.4f}")


def cross_profile(L, m, b, xs, half=14):
    """average luminance profile perpendicular-ish (sampled in y) across the cut."""
    out = np.zeros(2 * half + 1)
    n = 0
    for x in xs:
        y0 = m * x + b
        for i, d in enumerate(range(-half, half + 1)):
            yy = y0 + d
            iy = int(np.floor(yy))
            f = yy - iy
            if 0 <= iy < L.shape[0] - 1:
                out[i] += L[iy, x] * (1 - f) + L[iy + 1, x] * f
        n += 1
    return out / n


pc = cross_profile(Lc, mc, bc, xs)
pr = cross_profile(Lr, mr, br, xs)
print("\nluminance across the cut (d = px below the fitted line; -=un-planed side, +=trued side)")
print("  d   cand    ref")
for i, d in enumerate(range(-14, 15)):
    print(f"{d:+4d}  {pc[i]:.4f}  {pr[i]:.4f}")
print(f"\ncand: far-above {pc[:5].mean():.4f}  far-below {pc[-5:].mean():.4f}  peak-in-window {pc.max():.4f} at d={np.argmax(pc)-14}  min {pc.min():.4f} at d={np.argmin(pc)-14}")
print(f"ref : far-above {pr[:5].mean():.4f}  far-below {pr[-5:].mean():.4f}  peak-in-window {pr.max():.4f} at d={np.argmax(pr)-14}  min {pr.min():.4f} at d={np.argmin(pr)-14}")
