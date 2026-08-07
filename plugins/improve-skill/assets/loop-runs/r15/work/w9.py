"""Calibrate the pit-relief filter in rsvg against the reference's measured face
texture: high-pass sd ~0.018 and POSITIVE skew (+1.2..+2.1 on clean patches).

A plain diffuse-lit fractalNoise field comes out skew -0.25 -- dark-biased noise,
which is not what the reference has. The lever is an asymmetric transfer on the
lit result: slope s_hi above the flat value, s_lo below, so crests flare and
troughs stay shallow. g(v0) = v0 keeps the flat-surface normalisation exact, so
the surface mean does not move.
"""
import math
import subprocess
import numpy as np
from PIL import Image

FACE_L = 0.25


def table(v0, s_lo, s_hi, n=33):
    vals = []
    for i in range(n):
        x = i / (n - 1)
        y = v0 + (s_lo if x < v0 else s_hi) * (x - v0)
        vals.append(min(1.0, max(0.0, y)))
    return " ".join("%.4f" % v for v in vals)


def build(cases):
    defs, rects = [], []
    for i, (kind, bf, scale, elev, s_lo, s_hi) in enumerate(cases):
        v0 = math.sin(math.radians(elev))
        k1 = 1.0 / v0
        ct = ""
        src = "lit"
        if s_lo != 1.0 or s_hi != 1.0:
            tv = table(v0, s_lo, s_hi)
            ct = ('<feComponentTransfer in="lit" result="bent">'
                  + "".join(f'<feFunc{c} type="table" tableValues="{tv}"/>' for c in "RGB")
                  + "</feComponentTransfer>")
            src = "bent"
        defs.append(f"""<filter id="f{i}" x="-200" y="-200" width="4000" height="4000"
       filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
  <feTurbulence type="{kind}" baseFrequency="{bf}" numOctaves="3" seed="9" result="h"/>
  <feDiffuseLighting in="h" surfaceScale="{scale}" diffuseConstant="1"
                     lighting-color="#FFFFFF" result="lit">
    <feDistantLight azimuth="225" elevation="{elev}"/>
  </feDiffuseLighting>
  {ct}
  <feComposite in="{src}" in2="SourceGraphic" operator="arithmetic"
               k1="{k1:.4f}" k2="0" k3="0" k4="0"/>
</filter>""")
        rects.append(f'<rect x="{4 + i * 132}" y="4" width="128" height="512" '
                     f'fill="#565351" filter="url(#f{i})"/>')
    w = 132 * len(cases) + 8
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="520" '
            f'viewBox="0 0 {w} 520"><defs>' + "\n".join(defs) + "</defs>" +
            "\n".join(rects) + "</svg>"), w


def run(cases):
    svg, w = build(cases)
    open("cal.svg", "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", "520", "cal.svg", "-o", "cal.png"],
                   check=True)
    a = np.asarray(Image.open("cal.png").convert("RGB")).astype(float) / 255
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    out = []
    for i in range(len(cases)):
        v = L[16:500, 4 + i * 132 + 16: 4 + i * 132 + 112]
        d = v - v.mean()
        out.append((v.mean(), v.std(), float((d ** 3).mean() / d.std() ** 3)))
    return out


base_L = 0.2126 * (0x56 / 255) + 0.7152 * (0x53 / 255) + 0.0722 * (0x51 / 255)
print("source L (sRGB-linear-free, same formula as the metric): %.4f" % base_L)
print("target: added sd ~0.016 on a %.2f face, skew ~ +1.5\n" % base_L)

cases = [
    ("fractalNoise", "0.55 0.55", 0.50, 50, 1.0, 1.0),
    ("turbulence",   "0.55 0.55", 0.50, 50, 1.0, 1.0),
    ("fractalNoise", "0.55 0.55", 0.50, 50, 0.45, 1.9),
    ("fractalNoise", "0.55 0.55", 0.50, 50, 0.30, 2.4),
    ("fractalNoise", "0.55 0.55", 0.70, 50, 0.30, 2.4),
    ("fractalNoise", "0.40 0.40", 0.50, 50, 0.30, 2.4),
    ("fractalNoise", "0.55 0.55", 0.50, 38, 0.30, 2.4),
]
for c, (mn, sd, sk) in zip(cases, run(cases)):
    print("%-13s bf=%-11s scale=%.2f elev=%2d s=(%.2f,%.2f) -> mean %.4f (%+.4f) sd %.4f skew %+.2f"
          % (c[0], c[1], c[2], c[3], c[4], c[5], mn, mn - base_L, sd, sk))
