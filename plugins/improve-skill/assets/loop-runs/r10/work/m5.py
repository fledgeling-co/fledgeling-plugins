"""Ground texture: spatial-frequency content of the reference vs the master.

Patch chosen inside the un-planed (rough) plane, clear of block, curl and the
boundary.  Radially-averaged power spectrum of the detrended patch, reported as
energy per octave, plus the same patch's sd after a box-blur at each scale (a
direct read on "how much of this texture survives downsampling to N px").
"""
import sys, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", 1024))

PATCHES = {
    "rough-left":  (40, 470, 300, 260),    # x, y, w, h   left of the block, below the curl
    "rough-top":   (470, 40, 300, 200),    # above the block, right of the curl
    "trued-br":    (640, 780, 330, 200),   # trued plane, clear of the block
}


def spectrum(p):
    p = p - p.mean()
    yy, xx = np.mgrid[0:p.shape[0], 0:p.shape[1]]
    # remove a plane (the gradient) so we measure texture, not the field
    Amat = np.stack([np.ones_like(xx).ravel(), xx.ravel(), yy.ravel()], 1).astype(float)
    coef, *_ = np.linalg.lstsq(Amat, p.ravel(), rcond=None)
    p = p - (Amat @ coef).reshape(p.shape)
    win = np.hanning(p.shape[0])[:, None] * np.hanning(p.shape[1])[None, :]
    Ffт = np.fft.fftshift(np.fft.fft2(p * win))
    P = np.abs(Ffт) ** 2
    cy, cx = np.array(P.shape) // 2
    r = np.hypot(*np.mgrid[0:P.shape[0], 0:P.shape[1]] - np.array([[[cy]], [[cx]]]))
    out = {}
    n = min(p.shape)
    for lo, hi in [(2, 4), (4, 8), (8, 16), (16, 32), (32, 64), (64, 128), (128, 256)]:
        # feature wavelength band in px = n/r
        m = (r >= n / hi) & (r < n / lo)
        out[f"{lo}-{hi}px"] = P[m].sum()
    tot = sum(out.values())
    return {k: v / tot for k, v in out.items()}, p.std()


def blurred_sd(p, k):
    q = p - p.mean()
    if k > 1:
        h_, w_ = (q.shape[0] // k) * k, (q.shape[1] // k) * k
        q = q[:h_, :w_].reshape(h_ // k, k, w_ // k, k).mean(axis=(1, 3))
    return q.std()


for name, (x, y, w, hh) in PATCHES.items():
    for lbl, img in (("cand", g), ("ref ", h)):
        p = img[y:y + hh, x:x + w]
        sp, sd = spectrum(p)
        surv = " ".join(f"{k}:{blurred_sd(p,k):.4f}" for k in (1, 4, 8))
        print(f"{name:11s} {lbl}  sd={sd:.4f}  " +
              " ".join(f"{k}={v*100:4.1f}%" for k, v in sp.items()))
        print(f"{'':11s}      sd after box-downsample  x{surv}")
    print()
