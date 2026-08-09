#!/usr/bin/env python3
"""Montage helper: tile PNGs side by side on a dark ground for a quick look.

    python3 montage.py out.png 320 a.png b.png ...
"""
import sys

from PIL import Image

out, w = sys.argv[1], int(sys.argv[2])
srcs = sys.argv[3:]
sheet = Image.new("RGB", (w * len(srcs), w), (16, 16, 18))
for i, s in enumerate(srcs):
    im = Image.open(s).convert("RGBA").resize((w, w), Image.LANCZOS)
    bg = Image.new("RGBA", (w, w), (16, 16, 18, 255))
    bg.alpha_composite(im)
    sheet.paste(bg.convert("RGB"), (i * w, 0))
sheet.save(out)
print("wrote", out)
