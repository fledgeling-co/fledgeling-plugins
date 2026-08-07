"""The #4 deduction's own quantity, measured the way round 17's note measured it.

r17 halved how hard the curl's patch contrasts against the ground it covers (16px mean |dL|
0.0806 -> 0.0433, signed -0.0650 -> -0.0191) by giving the roll a bore. That fixed the curl
reading as a DARK blot. This round is the same deduction from the other side, so the same
number is taken again: patch against ground, with and without the shaving, at 16 and 32.
"""
import subprocess
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r18/work")


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def nat(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return gray(Image.open(t).convert("RGBA"))


for s in (32, 16):
    off = nat(str(WORK / "var_noshaving.svg"), s)
    print("\n%dpx" % s)
    for tag, svg in (("r17", str(WORK / "var_r17.svg")), ("r18", "icon.svg")):
        on = nat(svg, s)
        d = on - off
        patch = np.abs(d) > 0.004
        print("  %s  patch %d px   mean |dL| %.4f   worst %.4f   signed mean %+.4f"
              % (tag, patch.sum(), np.abs(d[patch]).mean(), np.abs(d).max(), d[patch].mean()))
