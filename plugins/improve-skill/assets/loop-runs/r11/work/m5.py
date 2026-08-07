"""Is the reference's y-dependence a perspective effect or an amplitude effect?

If the rough plane recedes from the camera, a fixed physical grain pitch projects to a
wavelength that GROWS with canvas y, and near the top of the frame it compresses below
the point where the scorer's Sobel can see it. If instead the pitch is constant and only
the contrast changes, the cause is light or material, not geometry. Measure the dominant
relief wavelength and its rms in horizontal strips of the reference's un-planed plane.
"""
import numpy as np

W = 1024
h = np.load("h1024.npy"); g = np.load("g1024.npy")
rough = np.load("rough.npy")


def strip_spectrum(img, mask, y0, y1):
    """1-D power spectrum across x, averaged over the rows of the strip, using only
    rows with a long enough run of mask so a window is legal."""
    P, n = None, 0
    for y in range(y0, y1):
        row = mask[y]
        if row.sum() < 160:
            continue
        xs = np.flatnonzero(row)
        a, b = xs[0], xs[-1] + 1
        if not row[a:b].all():
            b = a + np.argmin(row[a:b]) if not row[a:b].all() else b
        if b - a < 160:
            continue
        v = img[y, a:b].astype(float)
        m = min(256, (b - a) // 1)
        v = v[:m]
        v = v - np.polyval(np.polyfit(np.arange(m), v, 3), np.arange(m))
        v = v * np.hanning(m)
        p = np.abs(np.fft.rfft(v, 256)) ** 2
        P = p if P is None else P + p
        n += 1
    if n == 0:
        return None
    P /= n
    f = np.fft.rfftfreq(256)
    keep = (f > 1/60.0) & (f < 0.45)
    lam = 1.0 / f[keep][np.argmax(P[keep])]
    # power-weighted mean wavelength, a more stable summary than the peak
    wl = (P[keep] / f[keep]).sum() / P[keep].sum()
    return lam, wl, P[keep].sum() ** 0.5 / 16, n


print(f"{'strip y':>11s} {'  reference: peak_l  mean_l  energy  rows':<44s} "
      f"{'candidate: peak_l  mean_l  energy  rows'}")
for y0 in range(80, 880, 80):
    r = strip_spectrum(h, rough, y0, y0 + 80)
    c = strip_spectrum(g, rough, y0, y0 + 80)
    if r is None or c is None:
        continue
    print(f"{y0:4d}-{y0+80:4d}  {r[0]:8.1f} {r[1]:7.1f} {r[2]:8.4f} {r[3]:5d}     "
          f"     {c[0]:8.1f} {c[1]:7.1f} {c[2]:8.4f} {c[3]:5d}")
