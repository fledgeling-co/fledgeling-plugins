"""The 32px cells themselves, read out as numbers, around the roll.

w2's radial profiles are contaminated: C2 carries a soft light bloom in the upper-left
CORNER, so its board up-left of the roll is brighter than ours for reasons that have
nothing to do with the curl, and any inside-minus-outside comparison along that bearing
mixes the two. The scored quantity is not a profile anyway - it is the 32px cell grid.
So read that grid directly, in ours, in C2, and in our SHAVING=0 twin.
"""
import subprocess
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r19/work")


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def nat(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return gray(Image.open(t).convert("RGBA"))


REF = Image.open("icon-engineC-f5665d-2.png").convert("RGBA")
X0, X1, Y0, Y1 = 3, 14, 2, 13


def show(tag, g):
    print("\n%s" % tag)
    print("      " + "".join("%6d" % x for x in range(X0, X1)))
    for y in range(Y0, Y1):
        print("  y%2d " % y + "".join("%6.3f" % g[y, x] for x in range(X0, X1)))


for s in (32,):
    ours = nat("icon.svg", s)
    off = nat(str(WORK / "var_noshaving.svg"), s)
    ref = gray(REF.resize((s, s), Image.LANCZOS))
    show("%dpx OURS" % s, ours)
    show("%dpx OURS, shaving off (the board it covers)" % s, off)
    show("%dpx C2 reference" % s, ref)
    show("%dpx ours - board (what the shaving does)" % s, ours - off)

    # and the same neighbourhood expressed against each image's own local board:
    # cells the shaving does not touch, inside the same 11x11 window
    d = ours - off
    touched = np.abs(d) > 0.004
    win = np.zeros_like(ours, bool)
    win[Y0:Y1, X0:X1] = True
    board_ours = np.median(ours[win & ~touched])
    board_ref = np.median(ref[win & ~touched])
    print("\n  local board (untouched cells in the window): ours %.4f   C2 %.4f"
          % (board_ours, board_ref))
    print("  cells the shaving occupies, minus own board:")
    print("    ours  p10 %+.3f  p50 %+.3f  p90 %+.3f  max %+.3f  mean %+.3f"
          % (*[np.percentile(ours[touched] - board_ours, p) for p in (10, 50, 90)],
             (ours[touched] - board_ours).max(), (ours[touched] - board_ours).mean()))
    print("    C2    p10 %+.3f  p50 %+.3f  p90 %+.3f  max %+.3f  mean %+.3f"
          % (*[np.percentile(ref[touched] - board_ref, p) for p in (10, 50, 90)],
             (ref[touched] - board_ref).max(), (ref[touched] - board_ref).mean()))
