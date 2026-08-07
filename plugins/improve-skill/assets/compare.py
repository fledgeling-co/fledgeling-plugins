#!/usr/bin/env python3
"""Render the master and lay it beside both raster takes at 256, plus a 16px squint row."""
import pathlib
import subprocess
import sys
from PIL import Image, ImageDraw

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else A / "cmp.png"

for size in (1024, 256, 32):
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                    str(A / "icon.svg"), "-o", str(A / f"_a{size}.png")], check=True)

cols = [("A  new master", A / "_a256.png", A / "_a32.png"),
        ("C1  raster", A / "audit-renders/C1-256.png", A / "audit-renders/C1-32.png"),
        ("C2  whetstone", A / "audit-renders/C2-256.png", A / "audit-renders/C2-32.png")]

PAD, W, SQ = 22, 256, 128
sheet = Image.new("RGB", (PAD + (W + PAD) * 3, PAD + 20 + W + PAD + SQ + PAD + 18), (16, 22, 26))
d = ImageDraw.Draw(sheet)
for i, (label, big, small) in enumerate(cols):
    x = PAD + (W + PAD) * i
    d.text((x, PAD - 4), label, fill=(190, 210, 220))
    sheet.paste(Image.open(big).convert("RGB").resize((W, W), Image.LANCZOS), (x, PAD + 18))
    sq = Image.open(small).convert("RGB").resize((SQ, SQ), Image.NEAREST)
    sheet.paste(sq, (x + (W - SQ) // 2, PAD + 18 + W + PAD))
    d.text((x + (W - SQ) // 2, PAD + 18 + W + PAD + SQ + 2), "16px squint x8", fill=(120, 150, 160))
sheet.save(OUT)
print(f"wrote {OUT}")
