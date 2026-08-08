"""r12 diagnostic 2: what IS the reference's iron-face texture?

Before authoring it (r11's recipe), count the lobes of its gradient-energy bearing
histogram and read its scale off the radial power spectrum. Patches are hand-sited
inside each image's OWN block, because the two blocks are not in register.
"""
import sys, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

g = np.load("d_g.npy"); h = np.load("d_h.npy")

# hand-sited interior patches, checked for mean luminance below
PATCHES = {
    "ref  face-mid":  (h, 470, 320, 150, 110),
    "ref  face-lead": (h, 330, 430, 120, 100),
    "cand face-mid":  (g, 430, 380, 150, 110),
    "cand face-lead": (g, 300, 500, 120, 100),
}

def hp(x):
    return x - F.box_mean(x, 13)

def bearings(p, nbin=18):
    """gradient ENERGY binned by RIDGE bearing (perpendicular to the gradient)."""
    q = hp(p)
    gy, gx = np.gradient(q)
    e = gx * gx + gy * gy
    ang = (np.degrees(np.arctan2(gy, gx)) + 90.0) % 180.0
    idx = np.clip((ang / (180.0 / nbin)).astype(int), 0, nbin - 1)
    hist = np.bincount(idx.ravel(), weights=e.ravel(), minlength=nbin)
    return hist / hist.sum()

def radial_spectrum(p):
    q = hp(p) * np.outer(np.hanning(p.shape[0]), np.hanning(p.shape[1]))
    P = np.abs(np.fft.fftshift(np.fft.fft2(q))) ** 2
    n0, n1 = p.shape
    yy, xx = np.mgrid[0:n0, 0:n1]
    r = np.hypot((yy - n0 / 2) / (n0 / 2), (xx - n1 / 2) / (n1 / 2))
    out = []
    for lo, hi in ((0.0, .12), (.12, .25), (.25, .40), (.40, .60), (.60, .85), (.85, 1.3)):
        m = (r >= lo) & (r < hi)
        out.append(P[m].sum())
    out = np.array(out) / np.sum(out)
    return out

print("%-16s %6s %8s %8s | %7s %7s %7s" % ("patch", "mean", "hp-sd", "grad%", "pk/mean", "pk/cross", "pk-bear"))
for name, (img, x0, y0, w, hgt) in PATCHES.items():
    p = img[y0:y0 + hgt, x0:x0 + w]
    b = bearings(p)
    pk = int(np.argmax(b))
    cross = b[(pk + 9) % 18]
    q = hp(p)
    gy, gx = np.gradient(p)
    dens = (np.hypot(gx, gy) > 4 / 255).mean()
    print("%-16s %.4f %8.4f %7.1f%% | %7.2f %8.2f %6.0f deg"
          % (name, p.mean(), q.std(), 100 * dens, b[pk] / b.mean(), b[pk] / max(cross, 1e-9),
             pk * 10 + 5))
    print("      bins:", " ".join("%.3f" % v for v in b))
    print("      spectrum (coarse->fine):", " ".join("%.3f" % v for v in radial_spectrum(p)))
