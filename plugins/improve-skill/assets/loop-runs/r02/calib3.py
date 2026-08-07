#!/usr/bin/env python3
"""Third calibration: relief as a MULTIPLY against the surface's own fill, normalised on
the flat-surface lighting value so untextured areas come out bit-identical. Sweeps
surfaceScale for the ground fibre and the block pitting against measured targets."""
import math, subprocess, pathlib
import numpy as np
from PIL import Image, ImageFilter

OUT = pathlib.Path(__file__).resolve().parent
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
M = f"matrix({UX:.5f},{UY:.5f},{NX:.5f},{NY:.5f},220,700)"
# inverse of the same frame (orthonormal, det -1)
det = UX * NY - NX * UY
iA, iB, iC, iD = NY / det, -UY / det, -NX / det, UX / det
iE = -(iA * 220 + iC * 700)
iF = -(iB * 220 + iD * 700)
MI = f"matrix({iA:.5f},{iB:.5f},{iC:.5f},{iD:.5f},{iE:.3f},{iF:.3f})"


def svg(scale, elev, bfx, bfy, base, seed=9):
    k1 = 1.0 / math.sin(math.radians(elev))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
<defs>
  <filter id="fib" x="-900" y="-900" width="2600" height="2600"
          filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="{bfx} {bfy}" numOctaves="3" seed="{seed}" result="n"/>
    <feDiffuseLighting in="n" surfaceScale="{scale}" diffuseConstant="1" lighting-color="#ffffff" result="lit">
      <feDistantLight azimuth="102" elevation="{elev}"/>
    </feDiffuseLighting>
    <feComposite in="lit" in2="SourceGraphic" operator="arithmetic" k1="{k1:.4f}" k2="0" k3="0" k4="0"/>
  </filter>
  <linearGradient id="fld" x1="0" y1="0" x2="1024" y2="1024" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{base[0]}"/><stop offset="1" stop-color="{base[1]}"/>
  </linearGradient>
</defs>
  <rect width="1024" height="1024" fill="url(#fld)"/>
  <g transform="{M}" filter="url(#fib)"><g transform="{MI}">
    <rect x="0" y="0" width="1024" height="1024" fill="url(#fld)"/>
  </g></g>
</svg>
'''


def stats(png, box):
    im = Image.open(png).convert("L")
    g = np.asarray(im, float)
    h = g - np.asarray(im.filter(ImageFilter.GaussianBlur(6)), float)
    x, y, n = box
    p = g[y:y+n, x:x+n]
    gy, gx = np.gradient(p)
    return h[y:y+n, x:x+n].std(), (np.hypot(gx, gy) > 4).mean(), p.mean()


def run(tag, cases, box):
    print(f"\n{tag}")
    print(f"{'scale':>6s} {'elev':>5s} {'bfx':>6s} {'bfy':>6s} | {'hp sd':>6s} {'e>4':>6s} {'mean':>7s} {'shift':>6s}")
    for scale, elev, bfx, bfy, base in cases:
        p = OUT / "probe5.svg"
        p.write_text(svg(scale, elev, bfx, bfy, base))
        subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", str(p), "-o", str(OUT / "probe5.png")], check=True)
        hp, e, m = stats(OUT / "probe5.png", box)
        p.write_text(svg(0.0001, elev, bfx, bfy, base))
        subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", str(p), "-o", str(OUT / "probe5f.png")], check=True)
        _, _, m0 = stats(OUT / "probe5f.png", box)
        print(f"{scale:6.2f} {elev:5d} {bfx:6.3f} {bfy:6.3f} | {hp:6.2f} {e:6.3f} {m:7.1f} {m - m0:+6.2f}")


G = ("#DBD5C7", "#A19881")
B = ("#6A655C", "#2E2B26")
run("ground fibre  (target hp 18.3, e>4 0.885 at full strength)",
    [(0.8, 42, 0.26, 0.038, G), (1.2, 42, 0.26, 0.038, G), (1.6, 42, 0.26, 0.038, G),
     (2.2, 42, 0.26, 0.038, G), (1.6, 42, 0.20, 0.030, G), (1.6, 34, 0.26, 0.038, G)],
    (300, 300, 200))
run("block pitting (target hp 4.5, e>4 0.27)",
    [(0.5, 50, 0.50, 0.50, B), (0.8, 50, 0.50, 0.50, B), (1.2, 50, 0.50, 0.50, B),
     (0.8, 50, 0.85, 0.85, B), (0.8, 50, 0.30, 0.30, B)],
    (300, 300, 200))
