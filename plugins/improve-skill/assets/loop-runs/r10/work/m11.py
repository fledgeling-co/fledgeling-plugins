"""The reference's un-planed lattice: how many families, at what bearings, what pitch,
what amplitude - and how anisotropic it is compared with the master's.

Patch is a clean square of un-planed ground (no block, no shadow, no seam, no rim).
Band-passed, windowed, 2-D power spectrum, then power vs bearing and the pitch of
each peak.
"""
import sys, pathlib, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", 1024))

PATCH = {"rough-far":  (25, 690, 153, 818),    # dark corner, strongest tearing
         "rough-mid":  (60, 300, 188, 428),    # left of the curl
         "rough-near": (620, 30, 748, 158),    # up by the key
         "trued":      (700, 820, 828, 948)}
n = 128


def spec(img, box):
    x0, y0, x1, y1 = box
    p = img[y0:y1, x0:x1].astype(float)
    yy, xx = np.mgrid[0:n, 0:n]
    M = np.stack([np.ones(n*n), xx.ravel(), yy.ravel(), (xx*xx).ravel(),
                  (yy*yy).ravel(), (xx*yy).ravel()], 1)
    c, *_ = np.linalg.lstsq(M, p.ravel(), rcond=None)
    p = p - (M @ c).reshape(n, n)                    # quadratic detrend: kill the field
    sd = p.std()
    w = np.hanning(n)[:, None]*np.hanning(n)[None, :]
    P = np.abs(np.fft.fftshift(np.fft.fft2(p*w)))**2
    fy, fx = np.mgrid[0:n, 0:n] - n//2
    r = np.hypot(fx, fy)
    keep = (r >= n/40) & (r <= n/3)                  # 3..40px wavelengths
    th = (np.degrees(np.arctan2(fy, fx)) + 90) % 180  # ridge bearing = grad bearing + 90
    bins = np.zeros(18)
    for i in range(18):
        m = keep & (th >= i*10) & (th < (i+1)*10)
        bins[i] = P[m].sum()
    bins /= bins.sum()
    lam = n / r[keep][np.argmax(P[keep])]
    return sd, bins, lam


for name, box in PATCH.items():
    for lbl, img in (("master", g), ("ref   ", h)):
        sd, bins, lam = spec(img, box)
        top = np.argsort(bins)[::-1][:3]
        bearing = lambda i: ((i*10+5) + 90) % 180 - 90   # convert to canvas deg, -90..90
        pk = ", ".join(f"{bearing(i):+4.0f}deg {bins[i]*100:.0f}%" for i in top)
        print(f"{name:11s} {lbl}  sd(3-40px) {sd:.4f}  peak lambda {lam:5.1f}px  "
              f"aniso {bins.max()/bins.mean():.2f}  families: {pk}")
    print()
