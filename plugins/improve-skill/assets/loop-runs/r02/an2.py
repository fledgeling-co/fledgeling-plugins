#!/usr/bin/env python3
"""r02 analysis 2: grain orientation, per-line amplitude, and block-face detail."""
import numpy as np
from PIL import Image, ImageFilter
import math

D = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/"

def gray(p):
    im = Image.open(p).convert("RGB").resize((1024, 1024), Image.LANCZOS)
    return im, np.asarray(im.convert("L"), dtype=np.float64)

refim, R = gray(D + "loop-runs/r01/reference-1024.png")
cndim, C = gray(D + "loop-runs/r01/candidate-1024.png")

ys, xs = np.mgrid[0:1024, 0:1024]
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AX = 543.0 - UX * 320
AY = 604.0 - UY * 320
ly = NX * (xs - AX) + NY * (ys - AY)
lx = UX * (xs - AX) + UY * (ys - AY)

def orient(img, mask, label):
    """Structure-tensor dominant orientation of the high-pass detail, in canvas deg
    (0 = +x right, positive = counter-clockwise on screen)."""
    blur = np.asarray(Image.fromarray(img.astype(np.uint8)).filter(ImageFilter.GaussianBlur(7)), dtype=np.float64)
    h = img - blur
    gy, gx = np.gradient(h)
    m = mask
    Jxx, Jyy, Jxy = (gx[m]**2).mean(), (gy[m]**2).mean(), (gx[m]*gy[m]).mean()
    # dominant gradient direction; texture LINES run perpendicular to it
    th = 0.5 * math.atan2(2*Jxy, Jxx - Jyy)
    line = math.degrees(th) + 90.0
    coh = math.hypot(Jxx-Jyy, 2*Jxy) / (Jxx+Jyy+1e-9)
    line_screen = -((line + 90) % 180 - 90)   # flip y-down to conventional up-positive
    print(f"  {label:28s} line dir {line_screen:+7.1f} deg   coherence {coh:.3f}   hp sd {h[m].std():5.2f}")

darkR, darkC = R < 115, C < 115
gu = (ly > 90) & ~darkR & ~darkC
gt = (ly < -90) & ~darkR & ~darkC
print("dominant texture line direction (screen deg; boundary/hone runs +33, travel +57 i.e. -57...):")
print(" un-planed field:")
orient(R, gu, "reference")
orient(C, gu, "candidate")
print(" trued field:")
orient(R, gt, "reference")
orient(C, gt, "candidate")
print(" un-planed, near band (ly 90..300):")
orient(R, gu & (ly < 300), "reference")
orient(C, gu & (ly < 300), "candidate")

# block top face: use both-dark intersection
blk = darkR & darkC
print(" block (dark in both):")
orient(R, blk, "reference")
orient(C, blk, "candidate")

# --- spatial frequency of the grain: radial profile of |FFT| across a patch
def fftpeak(img, x0, y0, n, label):
    p = img[y0:y0+n, x0:x0+n].astype(np.float64)
    p = p - p.mean()
    w = np.outer(np.hanning(n), np.hanning(n))
    F = np.abs(np.fft.fftshift(np.fft.fft2(p*w)))
    fy, fx = np.mgrid[-n//2:n//2, -n//2:n//2]
    rad = np.hypot(fx, fy)
    prof = np.array([F[(rad >= k) & (rad < k+1)].mean() for k in range(1, n//2)])
    k = np.argmax(prof) + 1
    print(f"  {label:28s} peak k={k:3d} -> period {n/k:6.1f}px   energy@k {prof[k-1]:8.1f}")

print("\ngrain spatial frequency, 192px patch of un-planed ground at (120,470):")
fftpeak(R, 120, 470, 192, "reference")
fftpeak(C, 120, 470, 192, "candidate")
print("192px patch of trued ground at (700,760):")
fftpeak(R, 700, 760, 192, "reference")
fftpeak(C, 700, 760, 192, "candidate")

# --- edge density per region (Canny-ish: gradient magnitude over threshold)
def edens(img, m, label):
    gy, gx = np.gradient(img)
    g = np.hypot(gx, gy)
    print(f"  {label:28s} frac |grad|>4 : {(g[m] > 4).mean():.4f}   >8 : {(g[m] > 8).mean():.4f}")

print("\nedge density:")
edens(R, gu, "reference un-planed")
edens(C, gu, "candidate un-planed")
edens(R, gt, "reference trued")
edens(C, gt, "candidate trued")
edens(R, blk, "reference block")
edens(C, blk, "candidate block")
