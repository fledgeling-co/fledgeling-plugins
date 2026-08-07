#!/usr/bin/env python3
"""Visual check of the calibrated relief: is it anisotropic in the LOCAL frame, and
does one noise field stay continuous across the amplitude step at the cut?"""
import subprocess, pathlib, sys
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from calib import build, OUT

p = OUT / "probe3.svg"
p.write_text(build(2.0, 1.5, 0.90, 1.5, 0.85))
subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", str(p), "-o", str(OUT / "probe3.png")], check=True)
im = Image.open(OUT / "probe3.png").convert("RGB")
# the step in the calib ramp sits at local y = 0, which passes through (220,700)
sheet = Image.new("RGB", (720, 360), "black")
sheet.paste(im.crop((150, 560, 390, 680)).resize((720, 360), Image.NEAREST), (0, 0))
sheet.save(OUT / "probe3-crop.png")
print("wrote probe3-crop.png (240x120 across the step, 3x)")
