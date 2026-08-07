#!/usr/bin/env python3
"""Calibrate the noise-relief overlay in the SCORING renderer before it goes near
build_icon.py: (a) does the filter run in the group's local frame, (b) what
surfaceScale / alpha coefficients land on the reference's measured hp sd and edge
density, (c) does one noise field stay continuous across an amplitude step."""
import math, subprocess, pathlib
import numpy as np
from PIL import Image, ImageFilter

OUT = pathlib.Path(__file__).resolve().parent
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
# light from canvas top-left, expressed in the local frame
dx, dy = -0.7071, -0.7071
AZ = math.degrees(math.atan2(NX * dx + NY * dy, UX * dx + UY * dy)) % 360
print(f"local azimuth for a top-left key: {AZ:.1f} deg")

MATRIX = f"matrix({UX:.5f},{UY:.5f},{NX:.5f},{NY:.5f},220,700)"


def fibre_filter(fid, bfx, bfy, oct_, seed, ss, elev, kd, bd, kl, bl, dark, light):
    return f'''  <filter id="{fid}" x="-900" y="-900" width="2600" height="2600"
          filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="{bfx} {bfy}" numOctaves="{oct_}" seed="{seed}" result="n"/>
    <feDiffuseLighting in="n" surfaceScale="{ss}" diffuseConstant="1" lighting-color="#ffffff" result="lit">
      <feDistantLight azimuth="{AZ:.1f}" elevation="{elev}"/>
    </feDiffuseLighting>
    <feColorMatrix in="lit" type="matrix" result="valley"
        values="0 0 0 0 {dark[0]}  0 0 0 0 {dark[1]}  0 0 0 0 {dark[2]}  {-kd} 0 0 0 {bd}"/>
    <feColorMatrix in="lit" type="matrix" result="crest"
        values="0 0 0 0 {light[0]}  0 0 0 0 {light[1]}  0 0 0 0 {light[2]}  {kl} 0 0 0 {-bl}"/>
    <feMerge><feMergeNode in="valley"/><feMergeNode in="crest"/></feMerge>
  </filter>
'''


def build(ss, kd, bd, kl, bl, elev=42, bfx=0.30, bfy=0.045):
    f = fibre_filter("fib", bfx, bfy, 3, 5, ss, elev, kd, bd, kl, bl,
                     (0.243, 0.204, 0.153), (1.0, 0.976, 0.925))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
<defs>
{f}  <linearGradient id="ramp" gradientUnits="userSpaceOnUse"
      x1="{220 + NX * -400:.1f}" y1="{700 + NY * -400:.1f}" x2="{220 + NX * 600:.1f}" y2="{700 + NY * 600:.1f}">
    <stop offset="0" stop-color="#fff" stop-opacity="0.14"/>
    <stop offset="0.399" stop-color="#fff" stop-opacity="0.20"/>
    <stop offset="0.401" stop-color="#fff" stop-opacity="1"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0.34"/>
  </linearGradient>
  <mask id="rampMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">
    <rect width="1024" height="1024" fill="url(#ramp)"/>
  </mask>
</defs>
  <rect width="1024" height="1024" fill="#D8D2C4"/>
  <rect x="0" y="0" width="1024" height="1024" fill="#F4EFE3"
        transform="{MATRIX}" opacity="0"/>
  <g mask="url(#rampMask)"><g transform="{MATRIX}" filter="url(#fib)">
    <rect x="-900" y="-900" width="2600" height="2600" fill="#808080"/>
  </g></g>
</svg>
'''


def measure(png, boxes):
    im = Image.open(png).convert("L")
    g = np.asarray(im, float)
    h = g - np.asarray(im.filter(ImageFilter.GaussianBlur(6)), float)
    out = []
    for (x, y, n) in boxes:
        p = g[y:y+n, x:x+n]
        gy, gx = np.gradient(p)
        out.append((h[y:y+n, x:x+n].std(), (np.hypot(gx, gy) > 4).mean(), p.mean()))
    return out


print(f"\n{'ss':>5s} {'kd':>5s} {'bd':>5s} {'kl':>5s} {'bl':>5s} | "
      f"{'rough hp':>8s} {'rough e>4':>9s} {'rough L':>7s} | {'trued hp':>8s} {'trued e>4':>9s} {'trued L':>7s}")
print(" reference target                 |    18.28     0.885   155.5 |     1.23     0.000   155.7")
for ss, kd, bd, kl, bl in [(2.0, 1.5, 0.90, 1.5, 0.85),
                           (3.0, 1.8, 1.05, 1.8, 1.00),
                           (4.0, 2.2, 1.30, 2.2, 1.25),
                           (5.0, 2.6, 1.55, 2.6, 1.50)]:
    p = OUT / "probe2.svg"
    p.write_text(build(ss, kd, bd, kl, bl))
    subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", str(p), "-o", str(OUT / "probe2.png")], check=True)
    (r_hp, r_e, r_L), (t_hp, t_e, t_L) = measure(OUT / "probe2.png", [(120, 300, 160), (700, 800, 160)])
    print(f"{ss:5.1f} {kd:5.2f} {bd:5.2f} {kl:5.2f} {bl:5.2f} | {r_hp:8.2f} {r_e:9.3f} {r_L:7.1f} | "
          f"{t_hp:8.2f} {t_e:9.3f} {t_L:7.1f}")
