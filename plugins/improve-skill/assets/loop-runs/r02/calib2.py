#!/usr/bin/env python3
"""Second calibration: centre both alpha branches on the FLAT-surface lighting value
(sin elevation) so untextured ground comes out unchanged, then sweep gain against the
reference's measured hp sd / edge density. A relief that shifts the field's mean would
move polarity and figure-ground, which a detail round has no business doing."""
import math, subprocess, pathlib
import numpy as np
from PIL import Image, ImageFilter

OUT = pathlib.Path(__file__).resolve().parent
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AZ = 102.0
MATRIX = f"matrix({UX:.5f},{UY:.5f},{NX:.5f},{NY:.5f},220,700)"


def svg(scale, gain, elev, bfx, bfy, base="#C2BAA8"):
    bias = gain * math.sin(math.radians(elev))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
<defs>
  <filter id="fib" x="-900" y="-900" width="2600" height="2600"
          filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="{bfx} {bfy}" numOctaves="3" seed="9" result="n"/>
    <feDiffuseLighting in="n" surfaceScale="{scale}" diffuseConstant="1" lighting-color="#ffffff" result="lit">
      <feDistantLight azimuth="{AZ}" elevation="{elev}"/>
    </feDiffuseLighting>
    <feColorMatrix in="lit" type="matrix" result="valley"
        values="0 0 0 0 0.243  0 0 0 0 0.204  0 0 0 0 0.153  {-gain} 0 0 0 {bias:.4f}"/>
    <feColorMatrix in="lit" type="matrix" result="crest"
        values="0 0 0 0 1  0 0 0 0 0.976  0 0 0 0 0.925  {gain} 0 0 0 {-bias:.4f}"/>
    <feMerge><feMergeNode in="valley"/><feMergeNode in="crest"/></feMerge>
  </filter>
</defs>
  <rect width="1024" height="1024" fill="{base}"/>
  <g transform="{MATRIX}" filter="url(#fib)"><rect x="-900" y="-900" width="2600" height="2600"/></g>
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


BASE = {"#C2BAA8": 187.2, "#5A564E": 88.0}
print("target: un-planed peak hp 18.3 / e>4 0.885 ; block pit hp 4.5 / e>4 0.27")
print(f"{'scale':>6s} {'gain':>5s} {'elev':>5s} {'bfx':>6s} {'bfy':>6s} {'base':>9s} | {'hp sd':>6s} {'e>4':>6s} {'mean':>7s} {'shift':>6s}")
for scale, gain, elev, bfx, bfy, base in [
        (1.6, 1.5, 42, 0.26, 0.038, "#C2BAA8"),
        (2.0, 1.5, 42, 0.26, 0.038, "#C2BAA8"),
        (2.4, 1.5, 42, 0.26, 0.038, "#C2BAA8"),
        (2.0, 1.9, 42, 0.26, 0.038, "#C2BAA8"),
        (2.0, 1.5, 36, 0.26, 0.038, "#C2BAA8"),
        (1.1, 1.5, 50, 0.55, 0.55, "#5A564E"),
        (1.5, 1.5, 50, 0.55, 0.55, "#5A564E"),
        (2.0, 1.5, 50, 0.55, 0.55, "#5A564E"),
        (1.5, 1.5, 50, 0.80, 0.80, "#5A564E")]:
    p = OUT / "probe4.svg"
    p.write_text(svg(scale, gain, elev, bfx, bfy, base))
    subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", str(p), "-o", str(OUT / "probe4.png")], check=True)
    hp, e, m = stats(OUT / "probe4.png", (300, 300, 200))
    print(f"{scale:6.1f} {gain:5.2f} {elev:5d} {bfx:6.3f} {bfy:6.3f} {base:>9s} | "
          f"{hp:6.2f} {e:6.3f} {m:7.1f} {m - BASE[base]:+6.1f}")
