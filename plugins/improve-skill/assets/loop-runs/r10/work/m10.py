"""Which way does the reference's ground texture actually run, and at what pitch?

Structure tensor over the masked rough / trued ground on the band-passed image,
reported as the dominant ORIENTATION of the texture's gradient (so the streaks
themselves run 90 degrees off it), plus a directional power spectrum giving the
across-streak pitch.  Master measured the same way for comparison.
"""
import sys, pathlib, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
N = 1024
g = F.to_gray(F.render_candidate(A / "icon.svg", N))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", N))


def gblur(a, s):
    k = np.fft.fftfreq(N)[:, None]**2 + np.fft.fftfreq(N)[None, :]**2
    return np.real(np.fft.ifft2(np.fft.fft2(a) * np.exp(-2*np.pi**2*s**2*k)))


def erode(m, r):
    im = Image.fromarray((m*255).astype(np.uint8))
    while r > 0:
        s = min(9, 2*r+1); im = im.filter(ImageFilter.MinFilter(s)); r -= s//2
    return np.asarray(im) > 127


ys, xs = np.mgrid[0:N, 0:N]
u = (xs-511.5)/511.5; v = (ys-511.5)/511.5
inside = (np.abs(u)**5 + np.abs(v)**5)**0.2 < 0.80
bl = 957.0 + (292.0-957.0)*xs/N
clear = erode(~((g < 0.44) | (h < 0.44)), 46)
ROUGH = (ys < bl-70) & clear & inside
TRUED = (ys > bl+70) & clear & inside


def orient(img, mask, lo, hi):
    bp = gblur(img, lo) - gblur(img, hi)
    gy, gx = np.gradient(bp)
    Jxx, Jyy, Jxy = (gx*gx)[mask].mean(), (gy*gy)[mask].mean(), (gx*gy)[mask].mean()
    # dominant gradient direction; streaks run perpendicular to it
    th = 0.5*np.arctan2(2*Jxy, Jxx-Jyy)
    coh = np.hypot(Jxx-Jyy, 2*Jxy)/max(Jxx+Jyy, 1e-12)
    streak = np.degrees(th) + 90.0
    while streak > 90: streak -= 180
    while streak <= -90: streak += 180
    return streak, coh


print("streak bearing in CANVAS degrees (0 = +x to the right, positive = down-right;")
print("the blade / boundary runs at -33.0, the travel direction at +57.0)\n")
for rn, mask in (("rough", ROUGH), ("trued", TRUED)):
    for bn, (lo, hi) in (("fine 6-24px", (2.0, 8.0)), ("mid 24-190px", (8.0, 64.0))):
        sm, cm = orient(g, mask, lo, hi)
        sr, cr = orient(h, mask, lo, hi)
        print(f"{rn:6s} {bn:13s}  master {sm:+7.1f} deg (coh {cm:.3f})   "
              f"ref {sr:+7.1f} deg (coh {cr:.3f})")

# directional pitch: project the band-passed field onto the reference's own streak
# normal and take its 1-D power spectrum
def pitch(img, mask, ang_deg, lo, hi):
    bp = (gblur(img, lo) - gblur(img, hi)) * mask
    a = np.radians(ang_deg + 90.0)          # across the streaks
    s = xs*np.cos(a) + ys*np.sin(a)
    bins = np.round(s).astype(int); bins -= bins.min()
    prof = np.bincount(bins.ravel(), weights=bp.ravel(), minlength=bins.max()+1)
    cnt = np.bincount(bins.ravel(), weights=mask.ravel().astype(float), minlength=bins.max()+1)
    ok = cnt > 200
    p = np.zeros_like(prof); p[ok] = prof[ok]/cnt[ok]
    P = np.abs(np.fft.rfft(p*np.hanning(len(p))))**2
    f = np.fft.rfftfreq(len(p))
    band = (f > 1/60) & (f < 1/3)
    return 1.0/f[band][np.argmax(P[band])]

print()
for rn, mask in (("rough", ROUGH), ("trued", TRUED)):
    sr, _ = orient(h, mask, 2.0, 8.0)
    print(f"{rn}: across-streak pitch at the reference's own bearing {sr:+.1f} deg -> "
          f"master {pitch(g,mask,sr,2.0,8.0):.1f}px   ref {pitch(h,mask,sr,2.0,8.0):.1f}px")
