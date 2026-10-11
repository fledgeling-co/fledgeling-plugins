#!/usr/bin/env python3
"""Compose the shipped icon from the Arrow take (icon-engineB-arrow.svg), which the owner chose.

    python3 compose_icon.py          # writes icon.svg

Arrow drew its artwork on a square tile with a squircle inset inside it, which fails the family's
mask rule (siblings share plugins/create-mac-icon/assets/squircle-path.txt). This keeps Arrow's
artwork and its own defs, drops its square tile and inset squircle, and places the artwork on the
family's porcelain ground and squircle. build_icon.py remains the hand-authored alternate.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt").read_text().strip()
SRC = (HERE / "icon-engineB-arrow.svg").read_text()

SCALE = 11.6                 # 80-unit artboard -> about 0.9 of the 1024 tile
ART_CX, ART_CY = 42.6, 34.5  # centre of Arrow's artwork bounding box (x 12-73, y 4-65)
CX, CY = 512.0, 524.0

defs = re.search(r"<defs>.*?</defs>", SRC, re.S).group(0)
body = SRC.split("</defs>", 1)[1].rsplit("</svg>", 1)[0]
body = re.sub(r"^\s*<rect[^>]*/>\s*", "", body, count=1)          # Arrow's square tile
body = re.sub(r"^\s*<path[^>]*/>\s*", "", body, count=1)          # Arrow's inset squircle
tx, ty = CX - ART_CX * SCALE, CY - ART_CY * SCALE

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
{defs}
<defs>
  <linearGradient id="ground" gradientUnits="userSpaceOnUse" x1="350" y1="0" x2="600" y2="1024">
    <stop offset="0" stop-color="#FDFCF9"/><stop offset="0.55" stop-color="#F3EFE7"/><stop offset="1" stop-color="#E7E1D5"/>
  </linearGradient>
  <radialGradient id="vig" cx="0.42" cy="0.30" r="0.85">
    <stop offset="0.62" stop-color="#C4B899" stop-opacity="0"/><stop offset="1" stop-color="#C4B899" stop-opacity="0.22"/>
  </radialGradient>
  <clipPath id="tile"><path d="{SQUIRCLE}"/></clipPath>
</defs>
<g clip-path="url(#tile)">
  <g id="bg">
    <rect width="1024" height="1024" fill="url(#ground)"/>
    <rect width="1024" height="1024" fill="url(#vig)"/>
    <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-opacity="0.55"/>
  </g>
  <g id="fg" transform="translate({tx:.1f} {ty:.1f}) scale({SCALE})">
{body}
  </g>
</g>
</svg>
"""
(HERE / "icon.svg").write_text(svg)
print(f"wrote {HERE / 'icon.svg'}")
