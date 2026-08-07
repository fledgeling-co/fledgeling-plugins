"""Eyes on the round: the shaving before and after, at 1024, 32 and 16, beside C2.

The gate is a number; rubric 1 (figure-ground) and the 16px read are not. This rebuilds the
r17 constant into a throwaway SVG and puts the two side by side at the sizes that matter.
"""
import subprocess
import tempfile
import pathlib
import re
from PIL import Image

TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r18/work")
SRC = pathlib.Path("build_icon.py").read_text()

src, n = re.subn(r"OUT_LIT   = \(216, 208, 192\)", "OUT_LIT   = (243, 234, 216)", SRC, count=1)
assert n == 1
src = src.replace("ASSETS = pathlib.Path(__file__).resolve().parent",
                  "ASSETS = pathlib.Path(__file__).resolve().parent.parent.parent.parent")
(WORK / "gen_r17.py").write_text(src)
subprocess.run(["python3", str(WORK / "gen_r17.py")], check=True, capture_output=True)
(WORK / "var_r17.svg").write_bytes(pathlib.Path("icon.svg").read_bytes())
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)


def nat(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


ref = Image.open("icon-engineC-f5665d-2.png").convert("RGBA")

# 1: the curl at 1024, r17 | r18 | C2, 2x on the same crop
box = (130, 160, 430, 460)
tiles = [nat(str(WORK / "var_r17.svg"), 1024).crop(box),
         nat("icon.svg", 1024).crop(box),
         ref.resize((1024, 1024), Image.LANCZOS).crop(box)]
w, h = box[2] - box[0], box[3] - box[1]
out = Image.new("RGB", (3 * w * 2 + 24, h * 2), (20, 20, 20))
for i, t in enumerate(tiles):
    out.paste(t.convert("RGB").resize((w * 2, h * 2), Image.NEAREST), (i * (w * 2 + 12), 0))
out.save(str(WORK / "r18-curl-1024.png"))

# 2: whole tile at 32 and 16, r17 | r18 | C2, nearest-scaled to 256
rows = []
for s in (32, 16):
    ims = [nat(str(WORK / "var_r17.svg"), s), nat("icon.svg", s), ref.resize((s, s), Image.LANCZOS)]
    row = Image.new("RGB", (3 * 256 + 24, 256), (20, 20, 20))
    for i, im in enumerate(ims):
        row.paste(im.convert("RGB").resize((256, 256), Image.NEAREST), (i * 268, 0))
    rows.append(row)
out = Image.new("RGB", (3 * 256 + 24, 2 * 256 + 12), (20, 20, 20))
out.paste(rows[0], (0, 0))
out.paste(rows[1], (0, 268))
out.save(str(WORK / "r18-small.png"))
print("wrote r18-curl-1024.png and r18-small.png")
