"""How much ORNAMENT does the reference actually carry, per region and per band?

Band-limited sd: blur(sigma=lo) - blur(sigma=hi) isolates a wavelength band.
Two bands are reported per region:
   fine   6-24px   (what a 128px render throws away)
   mid    24-190px (what a 128px render KEEPS - the band the master is judged on
                    at 128 and 256, and the band its mottle/blotch layers own)
Regions are masks common to both images, eroded so no region boundary leaks in.
"""
import sys, pathlib, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", 1024))
N = 1024


def gblur(a, sigma):
    if sigma <= 0:
        return a.copy()
    k = np.fft.fftfreq(N)[:, None] ** 2 + np.fft.fftfreq(N)[None, :] ** 2
    return np.real(np.fft.ifft2(np.fft.fft2(a) * np.exp(-2 * (np.pi ** 2) * (sigma ** 2) * k)))


def band(a, lo, hi):
    return gblur(a, lo) - gblur(a, hi)


def erode(mask, r):
    im = Image.fromarray((mask * 255).astype(np.uint8))
    while r > 0:
        s = min(9, 2 * r + 1)
        im = im.filter(ImageFilter.MinFilter(s))
        r -= s // 2
    return np.asarray(im) > 127


ys, xs = np.mgrid[0:N, 0:N]
B_L, B_R = 957.0, 292.0
bline = B_L + (B_R - B_L) * xs / N          # ground boundary y at each x
rough = ys < bline - 4
trued = ys > bline + 4

dark_c, dark_r = g < 0.44, h < 0.44         # each icon's own solid + curl shadowing
solid = erode(dark_c & dark_r, 26)          # inside BOTH blocks
free_c = erode(~F.dilate(dark_c | (h < 0.5), 1), 46)   # ground clear of either solid

rad = np.hypot(xs - 75, ys - 25)
REG = {
    "rough near-key": rough & free_c & (rad < 520),
    "rough far":      rough & free_c & (rad >= 520),
    "trued ground":   trued & free_c,
    "block face":     solid,
}
BANDS = {"micro 2-6px": (0.6, 2.0), "fine 6-24px": (2.0, 8.0), "mid 24-190px": (8.0, 64.0)}

for rname, m in REG.items():
    print(f"{rname:14s}  px% {100*m.mean():5.2f}")
    for bname, (lo, hi) in BANDS.items():
        bc, br = band(g, lo, hi), band(h, lo, hi)
        sc, sr = bc[m].std(), br[m].std()
        print(f"    {bname:13s} master {sc:.4f}   ref {sr:.4f}   ratio {sc/max(sr,1e-6):5.2f}x"
              f"   -> scale ornament by {sr/max(sc,1e-6):.2f}")
