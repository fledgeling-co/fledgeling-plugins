"""What is the dark blot at the roll's tail, and does C2 have anything like it?

w10: our roll's four hottest 32px cells are a chain along its lower-right boundary -
(11,12) 0.367, (10,13) 0.362, (12,11) 0.347, (13,10) 0.305 - and the luminance grid says
why. Our roll's tail runs 0.611, 0.507, 0.455, 0.411 into the corner; C2's roll bottoms
out at 0.570 and never goes below it anywhere. Ours is 0.16 darker than the darkest thing
in C2's roll, and it is the single hottest gradient in our whole roll, 1.75x C2's hottest.

Interior contrast agrees between the two (p50 0.077 vs 0.080, p90 0.116 vs 0.133), so this
is not a general over-contrast: it is one dark blot at one end.

Print the same cells in the shaving-off twin to attribute the darkening, then write 1024px
crops of both images over the tail so the thing can be looked at rather than inferred.
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


def flat(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    return Image.fromarray(((a[..., :3] * a[..., 3:4] + NEUTRAL * (1 - a[..., 3:4])) * 255)
                           .astype(np.uint8))


def nat(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


O32 = gray(nat("icon.svg", 32))
F32 = gray(nat(str(WORK / "var_noshaving.svg"), 32))
print("cell        ours   shaving-off   delta")
for x, y in ((11, 12), (10, 13), (12, 11), (13, 10), (10, 12), (11, 11), (12, 12), (13, 11)):
    print("  (%2d,%2d)  %6.3f     %6.3f    %+.3f" % (x, y, O32[y, x], F32[y, x], O32[y, x] - F32[y, x]))

O = nat("icon.svg", 1024)
R = Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS)
og, rg = gray(O), gray(R)

# our tail region and C2's, each in its own frame: C2's roll sits (65,-98) from ours
BOX = (256, 288, 480, 480)
CBOX = (BOX[0] + 65, BOX[1] - 98, BOX[2] + 65, BOX[3] - 98)
print("\n1024px over the tail   ours%s   C2%s" % (BOX, CBOX))
print("  our patch   p01 %.3f  p10 %.3f  p50 %.3f   min %.3f"
      % tuple(list(np.percentile(og[BOX[1]:BOX[3], BOX[0]:BOX[2]], [1, 10, 50])) + [og[BOX[1]:BOX[3], BOX[0]:BOX[2]].min()]))
print("  C2  patch   p01 %.3f  p10 %.3f  p50 %.3f   min %.3f"
      % tuple(list(np.percentile(rg[CBOX[1]:CBOX[3], CBOX[0]:CBOX[2]], [1, 10, 50])) + [rg[CBOX[1]:CBOX[3], CBOX[0]:CBOX[2]].min()]))
flat(O).crop(BOX).resize((448, 384), Image.NEAREST).save(WORK / "crop_ours_tail.png")
flat(R).crop(CBOX).resize((448, 384), Image.NEAREST).save(WORK / "crop_ref_tail.png")

# and the 32px reads side by side, magnified, for the figure-ground check
flat(nat("icon.svg", 32)).resize((320, 320), Image.NEAREST).save(WORK / "crop_ours_32.png")
flat(R.resize((32, 32), Image.LANCZOS)).resize((320, 320), Image.NEAREST).save(WORK / "crop_ref_32.png")
print("wrote crop_ours_tail.png crop_ref_tail.png crop_ours_32.png crop_ref_32.png")
