"""The band statistics were satisfied and the material was still wrong: slate vs stucco.
Fit the FILAMENT character instead - type="turbulence" gives |noise| ridges, which is
what a cleaved face's scratch network looks like - and keep the band amplitudes as a
constraint rather than the target.
"""
import math
import subprocess
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, ".")
import common as C

SRC = "#565351"
base_L = 0.2126 * (0x56 / 255) + 0.7152 * (0x53 / 255) + 0.0722 * (0x51 / 255)


def table(v0, s_lo, s_hi, n=33):
    return " ".join("%.4f" % min(1.0, max(0.0, v0 + (s_lo if i / (n - 1) < v0 else s_hi) * (i / (n - 1) - v0)))
                    for i in range(n))


def run(cases):
    defs, rects = [], []
    for i, (kind, bfx, bfy, scale, elev, s_lo, s_hi, oct_) in enumerate(cases):
        v0 = math.sin(math.radians(elev))
        tv = table(v0, s_lo, s_hi)
        ct = ('<feComponentTransfer in="lit" result="bent">'
              + "".join(f'<feFunc{ch} type="table" tableValues="{tv}"/>' for ch in "RGB")
              + "</feComponentTransfer>")
        defs.append(f"""<filter id="f{i}" x="-200" y="-200" width="6000" height="6000"
       filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
  <feTurbulence type="{kind}" baseFrequency="{bfx} {bfy}" numOctaves="{oct_}" seed="9" result="h"/>
  <feDiffuseLighting in="h" surfaceScale="{scale}" diffuseConstant="1"
                     lighting-color="#FFFFFF" result="lit">
    <feDistantLight azimuth="225" elevation="{elev}"/>
  </feDiffuseLighting>
  {ct}
  <feComposite in="bent" in2="SourceGraphic" operator="arithmetic"
               k1="{1.0 / v0:.4f}" k2="0" k3="0" k4="0"/>
</filter>""")
        rects.append(f'<rect x="{4 + i * 200}" y="4" width="192" height="512" '
                     f'fill="{SRC}" filter="url(#f{i})"/>')
    w = 200 * len(cases) + 8
    open("cal2.svg", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="520" viewBox="0 0 {w} 520">'
        f'<defs>{"".join(defs)}</defs>{"".join(rects)}</svg>')
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", "520", "cal2.svg", "-o", "cal2.png"], check=True)
    a = np.asarray(Image.open("cal2.png").convert("RGB")).astype(float) / 255
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    out = []
    for i in range(len(cases)):
        v = L[16:500, 4 + i * 200 + 20: 4 + i * 200 + 176]
        d = v - v.mean()
        bands = {}
        for tag, (k1, k2) in [("1-3", (0, 1)), ("3-5", (1, 2)), ("5-9", (2, 4)), ("9-17", (4, 8))]:
            b = (C.boxblur(v, k1) if k1 else v) - C.boxblur(v, k2)
            bands[tag] = b.std()
        out.append((v.mean(), v.std(), float((d ** 3).mean() / d.std() ** 3), bands))
    return out, w


cases = [
    ("turbulence", 0.020, 0.020, 1.6, 50, 0.30, 2.4, 2),
    ("turbulence", 0.035, 0.035, 1.2, 50, 0.30, 2.4, 2),
    ("turbulence", 0.055, 0.055, 0.9, 50, 0.30, 2.4, 2),
    ("turbulence", 0.035, 0.035, 1.2, 50, 0.30, 2.4, 3),
    ("turbulence", 0.012, 0.055, 1.4, 50, 0.30, 2.4, 2),
    ("turbulence", 0.008, 0.040, 1.6, 50, 0.30, 2.4, 2),
]
res, w = run(cases)
for c, (mn, sd, sk, bands) in zip(cases, res):
    print("%-11s bf %.3f/%.3f oct %d scale %.2f -> mean x%.4f  sd %.4f  skew %+.2f  bands %s"
          % (c[0], c[1], c[2], c[7], c[3], mn / base_L, sd, sk,
             " ".join("%s=%.4f" % kv for kv in bands.items())))
print("target bands on this patch: 1-3=0.0242 3-5=0.0116 5-9=0.0106 9-17=0.0075")
