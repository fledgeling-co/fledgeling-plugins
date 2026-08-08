"""r12 diagnostic 3: the reference iron face's texture SCALE, along and across the blade.

Rotates each patch into the block's own frame first, then takes the 1-D power spectrum
separately along local x (the blade's length) and local y (its depth). That gives the two
numbers an feTurbulence baseFrequency pair wants, measured rather than chosen.
"""
import sys, math, numpy as np
from PIL import Image
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

g = np.load("d_g.npy"); h = np.load("d_h.npy")

# the top face's own bearing in image coords (build_icon's MATRIX_TOP first column)
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
K_RISE = (132.0 - 48.0) / 640.0
CAND_DEG = math.degrees(math.atan2(-(UY - K_RISE), UX))      # +38.9
REF_DEG = 38.9   # C2's own top-face edges, measured in the notes at the same 38.9


def rot_patch(img, cx, cy, w, hgt, deg):
    """Sample a w x hgt patch centred at (cx,cy) with its x axis along `deg` (CCW, screen)."""
    a = math.radians(deg)
    ex, ey = math.cos(a), -math.sin(a)
    px, py = -ey, ex
    j, i = np.meshgrid(np.arange(w) - w / 2.0, np.arange(hgt) - hgt / 2.0)
    X = cx + ex * j + px * i
    Y = cy + ey * j + py * i
    x0, y0 = np.floor(X).astype(int), np.floor(Y).astype(int)
    fx, fy = X - x0, Y - y0
    def at(yy, xx):
        return img[np.clip(yy, 0, 1023), np.clip(xx, 0, 1023)]
    return ((at(y0, x0) * (1 - fx) + at(y0, x0 + 1) * fx) * (1 - fy) +
            (at(y0 + 1, x0) * (1 - fx) + at(y0 + 1, x0 + 1) * fx) * fy)


def spec1d(p, axis):
    """Mean 1-D power spectrum along `axis`, high-passed, returned per cycles/px."""
    q = p - F.box_mean(p, 13)
    if axis == 1:
        q = q * np.hanning(q.shape[1])[None, :]
        P = (np.abs(np.fft.rfft(q, axis=1)) ** 2).mean(axis=0)
        n = q.shape[1]
    else:
        q = q * np.hanning(q.shape[0])[:, None]
        P = (np.abs(np.fft.rfft(q, axis=0)) ** 2).mean(axis=1)
        n = q.shape[0]
    f = np.fft.rfftfreq(n)
    P[0] = 0
    return f, P


def report(name, img, cx, cy, w, hgt, deg):
    p = rot_patch(img, cx, cy, w, hgt, deg)
    q = p - F.box_mean(p, 13)
    print("%-18s mean %.4f  hp-sd %.4f" % (name, p.mean(), q.std()))
    for axis, lab in ((1, "along-x (blade)"), (0, "across-y (depth)")):
        f, P = spec1d(p, axis)
        c = (f * P).sum() / P.sum()                      # centroid frequency, cyc/px
        pk = f[int(np.argmax(P))]
        # cumulative: fraction of power above 1/6 cyc/px (period < 6px)
        fine = P[f > 1 / 6].sum() / P.sum()
        print("     %-16s peak %.3f c/px (%.1f px)  centroid %.3f (%.1f px)  fine>1/6: %.0f%%"
              % (lab, pk, 1 / max(pk, 1e-6), c, 1 / max(c, 1e-6), 100 * fine))
    return q


print("candidate frame bearing %.1f deg" % CAND_DEG)
qr1 = report("ref face-mid",   h, 545, 375, 160, 110, REF_DEG)
qr2 = report("ref face-lead",  h, 390, 480, 130,  90, REF_DEG)
qc1 = report("cand face-mid",  g, 505, 435, 160, 110, CAND_DEG)
qc2 = report("cand face-lead", g, 360, 550, 130,  90, CAND_DEG)

print()
print("anisotropy (sd of the 1st difference across vs along; >1 = ridges run along x):")
for nm, q in (("ref  mid", qr1), ("ref  lead", qr2), ("cand mid", qc1), ("cand lead", qc2)):
    dax = np.diff(q, axis=1).std()
    day = np.diff(q, axis=0).std()
    print("   %-10s d/dx %.5f  d/dy %.5f   ratio dy/dx %.2f" % (nm, dax, day, day / dax))

Image.fromarray((np.clip(qr1 * 6 + 0.5, 0, 1) * 255).astype(np.uint8)).resize((480, 330), Image.NEAREST).save("z-ref-face-hp.png")
Image.fromarray((np.clip(qc1 * 6 + 0.5, 0, 1) * 255).astype(np.uint8)).resize((480, 330), Image.NEAREST).save("z-cand-face-hp.png")
