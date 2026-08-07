"""Pick the pit-relief parameters: hit the reference's measured band profile and
its positive skew, with the mean held exactly (the drift the asymmetric transfer
introduces is folded into k1 as a filter constant, independent of the surface)."""
import math
import subprocess
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, ".")
import common as C

SRC = "#565351"
base_L = 0.2126 * (0x56 / 255) + 0.7152 * (0x53 / 255) + 0.0722 * (0x51 / 255)
FACE_L = 0.25            # the block face's measured mean luminance

# reference face, per band, on the clean interior tiles (w2.py, co-masked)
REF_BAND = {"1-3": 0.0186, "3-5": 0.0090, "5-9": 0.0084, "9-17": 0.0080}
CAND_BAND = {"1-3": 0.0023, "3-5": 0.0015, "5-9": 0.0023, "9-17": 0.0056}
NEED = {k: math.sqrt(max(REF_BAND[k] ** 2 - CAND_BAND[k] ** 2, 0)) for k in REF_BAND}
print("needed added sd per band on a %.2f face: %s"
      % (FACE_L, " ".join("%s=%.4f" % (k, v) for k, v in NEED.items())))
print("...which on a %.3f calibration patch is: %s\n"
      % (base_L, " ".join("%s=%.4f" % (k, v * base_L / FACE_L) for k, v in NEED.items())))


def table(v0, s_lo, s_hi, n=33):
    return " ".join("%.4f" % min(1.0, max(0.0, v0 + (s_lo if i / (n - 1) < v0 else s_hi) * (i / (n - 1) - v0)))
                    for i in range(n))


def run(cases):
    defs, rects = [], []
    for i, (bf, scale, elev, s_lo, s_hi, oct_) in enumerate(cases):
        v0 = math.sin(math.radians(elev))
        tv = table(v0, s_lo, s_hi)
        ct = ('<feComponentTransfer in="lit" result="bent">'
              + "".join(f'<feFunc{ch} type="table" tableValues="{tv}"/>' for ch in "RGB")
              + "</feComponentTransfer>")
        defs.append(f"""<filter id="f{i}" x="-200" y="-200" width="6000" height="6000"
       filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="{bf} {bf}" numOctaves="{oct_}" seed="9" result="h"/>
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
    open("cal.svg", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="520" viewBox="0 0 {w} 520">'
        f'<defs>{"".join(defs)}</defs>{"".join(rects)}</svg>')
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", "520", "cal.svg", "-o", "cal.png"], check=True)
    a = np.asarray(Image.open("cal.png").convert("RGB")).astype(float) / 255
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
    return out


cases = []
for bf, oct_ in ((0.30, 4), (0.30, 5), (0.35, 4)):
    for scale in (0.85, 1.00):
        for lo, hi in ((0.30, 2.4), (0.22, 3.0)):
            cases.append((bf, scale, 50, lo, hi, oct_))
for c, (mn, sd, sk, bands) in zip(cases, run(cases)):
    print("bf %.2f oct %d scale %.2f s(%.2f,%.2f) -> mean %+.4f (x%.4f)  sd %.4f  skew %+.2f  bands %s"
          % (c[0], c[5], c[1], c[3], c[4], mn - base_L, mn / base_L, sd, sk,
             " ".join("%s=%.4f" % (k, v) for k, v in bands.items())))
