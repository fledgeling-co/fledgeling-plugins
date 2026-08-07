"""m8 corrected: the earlier masks let the tile rim and the ground boundary in, and
those two hard steps swamped every band statistic.  Excluded here: outside the
squircle (superellipse < 0.80), a +-70px band about the ground boundary, and
everything within 46px of either icon's solid.
"""
import sys, re, pathlib, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
Wd = A / "loop-runs/r10/work"
N = 1024
SVG = (A / "icon.svg").read_text()

ORNAMENT = [
    r'<path d="[^"]*" stroke="#6A5F4C"[^/]*/>',
    r'<path d="[^"]*" stroke="#8A7C64"[^/]*/>',
    r'<path d="M [-\d.]+ -8 L [-\d.]+ [-\d.]+" stroke="#FFFFFF"[^/]*/>',
    r'<ellipse [^/]*fill="#8C7A5E"[^/]*/>', r'<ellipse [^/]*fill="#FFF6E4"[^/]*/>',
    r'<ellipse [^/]*fill="#9C8A6C"[^/]*/>',
    r'<ellipse cx="[-\d]+" cy="[-\d]+" rx="\d+" ry="\d+" fill="#FFFFFF"[^/]*/>',
    r'<ellipse [^/]*fill="#9A968C"[^/]*/>', r'<ellipse [^/]*fill="#191714"[^/]*/>',
]
bare = SVG
for p in ORNAMENT:
    bare = re.sub(p, "", bare)
(Wd / "probe-bare.svg").write_text(bare)

g = F.to_gray(F.render_candidate(A / "icon.svg", N))
b = F.to_gray(F.render_candidate(Wd / "probe-bare.svg", N))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", N))


def gblur(a, s):
    k = np.fft.fftfreq(N)[:, None]**2 + np.fft.fftfreq(N)[None, :]**2
    return np.real(np.fft.ifft2(np.fft.fft2(a) * np.exp(-2*np.pi**2*s**2*k)))


def band(a, lo, hi):
    return gblur(a, lo) - gblur(a, hi)


def erode(m, r):
    im = Image.fromarray((m*255).astype(np.uint8))
    while r > 0:
        s = min(9, 2*r+1); im = im.filter(ImageFilter.MinFilter(s)); r -= s//2
    return np.asarray(im) > 127


ys, xs = np.mgrid[0:N, 0:N]
u = (xs - 511.5)/511.5; v = (ys - 511.5)/511.5
inside = (np.abs(u)**5 + np.abs(v)**5)**0.2 < 0.80          # well inside the squircle
bl = 957.0 + (292.0 - 957.0)*xs/N
seam = np.abs(ys - bl) < 70
dark_c, dark_r = g < 0.44, h < 0.44
clear = erode(~(dark_c | dark_r), 46)
REG = {"rough ground": (ys < bl) & ~seam & clear & inside,
       "trued ground": (ys > bl) & ~seam & clear & inside,
       "block face":   erode(dark_c & dark_r, 26)}
BANDS = {"micro 2-6px": (0.6, 2.0), "fine 6-24px": (2.0, 8.0), "mid 24-190px": (8.0, 64.0)}

for rn, m in REG.items():
    print(f"{rn}   px% {100*m.mean():.2f}")
    for bn, (lo, hi) in BANDS.items():
        mm, ff, rr = band(g, lo, hi)[m].std(), band(b, lo, hi)[m].std(), band(h, lo, hi)[m].std()
        num, den = rr**2 - ff**2, mm**2 - ff**2
        k = (num/den)**0.5 if num > 0 and den > 0 else 0.0
        print(f"   {bn:13s} master {mm:.5f}  bare {ff:.5f}  ref {rr:.5f}"
              f"   master/ref {mm/rr:5.2f}x   k = {k:.2f}")
