"""r12 diagnostic 4: calibrate the relief filter in rsvg-convert itself.

The recipes file warns that filter support varies by renderer, and r08's constants were
never rendered. So: paint a flat patch at the iron face's own luminance, run the r08
relief_filter over it, render in the SCORING renderer, and measure hp-sd and the 1-D
spectral centroid exactly as d3.py measures them on C2. Sweep until they match.

C2's iron face, measured (d3): hp-sd 0.0133-0.0189, centroid 0.105-0.149 c/px along the
blade and 0.180-0.189 across it, anisotropy d/dy over d/dx 1.14-1.41.
"""
import sys, math, subprocess, tempfile, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

L = 0.246          # the master's own top-face luminance in the sampled patch
GREY = int(round(255 * L ** (1 / 1.0)))   # sRGB-ish; only the ratio matters for sd/L


def relief_filter(fid, bf, scale, elev, azimuth, seed):
    k1 = 1.0 / math.sin(math.radians(elev))
    return f"""  <filter id="{fid}" x="-200" y="-200" width="1400" height="1400"
          filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="{bf[0]} {bf[1]}" numOctaves="3"
                  seed="{seed}" result="height"/>
    <feDiffuseLighting in="height" surfaceScale="{scale}" diffuseConstant="1"
                       lighting-color="#FFFFFF" result="lit">
      <feDistantLight azimuth="{azimuth:.1f}" elevation="{elev:.0f}"/>
    </feDiffuseLighting>
    <feComposite in="lit" in2="SourceGraphic" operator="arithmetic"
                 k1="{k1:.4f}" k2="0" k3="0" k4="0"/>
  </filter>
"""


def render(bf, scale, elev=50.0, az=225.0, seed=7):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
<defs>
{relief_filter("rel", bf, scale, elev, az, seed)}</defs>
<rect width="1024" height="1024" fill="#000"/>
<g filter="url(#rel)"><rect x="0" y="0" width="1024" height="1024" fill="rgb({GREY},{GREY},{GREY})"/></g>
</svg>
"""
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False, mode="w") as t:
        t.write(svg); p = pathlib.Path(t.name)
    out = p.with_suffix(".png")
    subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", str(p), "-o", str(out)], check=True)
    a = np.asarray(Image.open(out).convert("RGB")).astype(np.float64) / 255.0
    p.unlink(); out.unlink()
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def stats(g):
    p = g[212:812, 212:812]
    q = p - F.box_mean(p, 13)
    def cent(axis):
        r = q * (np.hanning(q.shape[1])[None, :] if axis == 1 else np.hanning(q.shape[0])[:, None])
        P = (np.abs(np.fft.rfft(r, axis=axis)) ** 2).mean(axis=1 - axis)
        f = np.fft.rfftfreq(r.shape[axis]); P[0] = 0
        return (f * P).sum() / P.sum()
    return p.mean(), q.std(), cent(1), cent(0), np.diff(q, axis=0).std() / np.diff(q, axis=1).std()


print("flat source L = %.4f (grey %d)" % (L, GREY))
print("%-22s %7s %8s %9s %9s %7s" % ("bf / scale", "mean", "hp-sd", "cent-x", "cent-y", "dy/dx"))
for bf in [(0.55, 0.55), (0.30, 0.30), (0.18, 0.18), (0.12, 0.12), (0.09, 0.09), (0.06, 0.06)]:
    m, sd, cx, cy, r = stats(render(bf, 0.50))
    print("%-22s %.4f %8.4f %9.3f %9.3f %7.2f" % (f"{bf} s0.50", m, sd, cx, cy, r))
