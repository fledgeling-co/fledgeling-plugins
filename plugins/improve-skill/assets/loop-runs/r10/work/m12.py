"""The reference's un-planed lattice, measured properly:
  (a) power vs bearing at 2-degree resolution, pooled over several clean patches;
  (b) texture sd as a function of distance from the key at (75,25), which is what
      the amplitude has to follow.
"""
import sys, pathlib, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
N = 1024
g = F.to_gray(F.render_candidate(A / "icon.svg", N))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", N))

# clean 96px squares of un-planed ground: no block, no curl, no seam, no rim
PATCHES = [(30, 500, 96), (30, 620, 96), (30, 700, 96), (140, 700, 96),
           (470, 40, 96), (600, 30, 96), (740, 30, 96), (860, 40, 96),
           (30, 200, 96), (30, 330, 96), (250, 40, 96), (360, 40, 96)]
n = 96


def bearing_power(img):
    acc = np.zeros(90)
    for x0, y0, s in PATCHES:
        p = img[y0:y0+s, x0:x0+s].astype(float)
        yy, xx = np.mgrid[0:n, 0:n]
        M = np.stack([np.ones(n*n), xx.ravel(), yy.ravel(), (xx*xx).ravel(),
                      (yy*yy).ravel(), (xx*yy).ravel()], 1)
        c, *_ = np.linalg.lstsq(M, p.ravel(), rcond=None)
        p = p - (M @ c).reshape(n, n)
        w = np.hanning(n)[:, None]*np.hanning(n)[None, :]
        P = np.abs(np.fft.fftshift(np.fft.fft2(p*w)))**2
        fy, fx = np.mgrid[0:n, 0:n] - n//2
        r = np.hypot(fx, fy)
        keep = (r >= n/30) & (r <= n/4)            # 4..30px wavelengths
        th = (np.degrees(np.arctan2(fy, fx)) + 90) % 180
        b = np.zeros(90)
        for i in range(90):
            m = keep & (th >= i*2) & (th < (i+1)*2)
            if m.any():
                b[i] = P[m].mean()
        acc += b/b.sum()
    return acc/len(PATCHES)


for lbl, img in (("master", g), ("ref", h)):
    b = bearing_power(img)
    # smooth circularly over 5 bins
    bs = np.convolve(np.r_[b[-3:], b, b[:3]], np.ones(5)/5, "same")[3:-3]
    order = np.argsort(bs)[::-1]
    picks, used = [], []
    for i in order:
        d = min(abs(i-j) for j in used) if used else 99
        d = min(d, 90-d) if used else 99
        if d > 12:
            picks.append(i); used.append(i)
        if len(picks) == 3:
            break
    def canv(i):
        a = (i*2+1) + 90
        return a-180 if a > 90 else a
    print(f"{lbl:7s} ridge bearings (canvas deg):  " +
          ",  ".join(f"{canv(i):+5.0f} ({bs[i]/bs.mean():.2f}x mean)" for i in picks))

# --- amplitude vs distance from the key
def gblur(a, s):
    k = np.fft.fftfreq(N)[:, None]**2 + np.fft.fftfreq(N)[None, :]**2
    return np.real(np.fft.ifft2(np.fft.fft2(a)*np.exp(-2*np.pi**2*s**2*k)))


def erode(m, r):
    im = Image.fromarray((m*255).astype(np.uint8))
    while r > 0:
        s = min(9, 2*r+1); im = im.filter(ImageFilter.MinFilter(s)); r -= s//2
    return np.asarray(im) > 127


ys, xs = np.mgrid[0:N, 0:N]
u = (xs-511.5)/511.5; v = (ys-511.5)/511.5
inside = (np.abs(u)**5 + np.abs(v)**5)**0.2 < 0.82
bl = 957.0 + (292.0-957.0)*xs/N
clear = erode(~((g < 0.44) | (h < 0.44)), 40)
rough = (ys < bl-60) & clear & inside
rad = np.hypot(xs-75, ys-25)
bpr, bpm = gblur(h, 0.8)-gblur(h, 6.0), gblur(g, 0.8)-gblur(g, 6.0)
print("\n  r from key      px    master sd   ref sd    ref/master")
for lo in range(0, 1200, 120):
    m = rough & (rad >= lo) & (rad < lo+120)
    if m.sum() < 900:
        continue
    sm, sr = bpm[m].std(), bpr[m].std()
    print(f"   {lo:4d}-{lo+120:4d}   {m.sum():6d}   {sm:.5f}    {sr:.5f}    {sr/max(sm,1e-9):5.2f}x")
